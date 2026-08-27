import express from "express";
import cors from "cors";
import crypto from "node:crypto";
import fs from "node:fs";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const app = express();
const port = Number(process.env.PORT ?? 3000);
const sourcePath = process.env.PROMPT_BANK_SOURCE_PATH ?? "./PROMPT_BANK_CANONICAL_SOURCE_v3.4.jsonl";
const expectedCount = Number(process.env.PROMPT_BANK_EXPECTED_COUNT ?? 554);
const corpusVersion = process.env.PROMPT_BANK_CORPUS_VERSION ?? "v3.4";

type RecordT = { prompt_id?: string; record_id?: string; title?: string; source_text?: string; sha256?: string; [k: string]: unknown };
const id = (r: RecordT) => String(r.prompt_id ?? r.record_id ?? "");
const norm = (s: string) => s.normalize("NFKC").toLocaleLowerCase().replace(/\s+/g, " ").trim();
const digest = (s: string) => crypto.createHash("sha256").update(s, "utf8").digest("hex");

const load = (): RecordT[] => {
  if (!fs.existsSync(sourcePath)) throw new Error(`Prompt corpus not found: ${sourcePath}`);
  const rows = fs.readFileSync(sourcePath, "utf8").split(/\r?\n/).filter(Boolean);
  const seen = new Set<string>();
  return rows.map((line, i) => {
    let r: RecordT;
    try { r = JSON.parse(line) as RecordT; } catch (e) { throw new Error(`Invalid JSONL line ${i + 1}: ${String(e)}`); }
    const rid = id(r);
    if (!rid) throw new Error(`Missing prompt_id/record_id at JSONL line ${i + 1}`);
    if (seen.has(rid)) throw new Error(`Duplicate prompt_id/record_id ${rid} at JSONL line ${i + 1}`);
    seen.add(rid);
    if (typeof r.source_text !== "string" || !r.source_text.trim()) throw new Error(`Missing source_text for ${rid}`);
    return r;
  });
};

const corpus = () => load();
const searchScore = (r: RecordT, q: string) => {
  const query = norm(q);
  if (!query) return 0;
  const title = norm(String(r.title ?? ""));
  const source = norm(String(r.source_text ?? ""));
  const identifier = norm(id(r));
  const tokens = query.split(/\s+/).filter(t => t.length > 2);
  let score = 0;
  if (title === query) score += 160;
  else if (title.includes(query)) score += 100;
  if (identifier === query) score += 140;
  if (source.includes(query)) score += 60;
  for (const token of tokens) {
    if (title.includes(token)) score += 12;
    if (source.includes(token)) score += 4;
  }
  return score;
};

const result = (out: unknown) => ({ content: [{ type: "text" as const, text: JSON.stringify(out, null, 2) }], structuredContent: out });

function serverFactory() {
  const s = new McpServer({ name: "prompt-bank-mcp", version: "0.2.0" });

  s.tool("search", "Retrieve reusable engineered instructions by natural-language goal, task, role, topic, or need. Never require the user to know a Prompt ID.",
    { query: z.string().min(1), limit: z.number().int().min(1).max(25).default(8) }, async ({ query, limit }) => {
      const rows = corpus();
      const results = rows.map(r => ({ r, score: searchScore(r, query) })).filter(x => x.score > 0)
        .sort((a, b) => b.score - a.score || id(a.r).localeCompare(id(b.r))).slice(0, limit)
        .map(x => ({ prompt_id: id(x.r), title: x.r.title ?? null, score: x.score, source_text: x.r.source_text ?? null, metadata: x.r }));
      return result({ corpus_version: corpusVersion, corpus_count: rows.length, query, results });
    });

  s.tool("fetch", "Return the complete frozen source text for a known Prompt Bank item. Never rewrite, summarize, normalize, or silently modify source_text.",
    { prompt_id: z.string().min(1) }, async ({ prompt_id }) => {
      const r = corpus().find(x => id(x) === prompt_id);
      if (!r) return result({ found: false, prompt_id });
      return result({ found: true, ...r, source_integrity: { source_text_is_verbatim: true, sha256_computed: digest(String(r.source_text)), sha256_recorded: r.sha256 ?? null } });
    });

  s.tool("compare", "Compare Prompt Bank items for exact duplicates, normalized duplicates, variants, complements, or conflicts. Topic similarity alone is never treated as duplication.",
    { prompt_ids: z.array(z.string()).min(2).max(8) }, async ({ prompt_ids }) => {
      const rows = corpus();
      const records = prompt_ids.map(prompt_id => rows.find(r => id(r) === prompt_id));
      const missing = prompt_ids.filter((_, i) => !records[i]);
      const items = records.filter(Boolean).map(r => ({ prompt_id: id(r!), title: r!.title ?? null, source_text: r!.source_text ?? "", metadata: r }));
      const exact = new Set(items.map(x => x.source_text)).size === 1 && items.length > 0;
      const normalized = new Set(items.map(x => norm(x.source_text))).size === 1 && items.length > 0;
      return result({ same_text: exact, same_normalized_text: normalized, missing, records: items });
    });

  s.tool("ingest_prompt", "Perform a read-only intake gate for a supplied new instruction. Preserve source text, detect exact/normalized duplicates and related titles, and never claim persistence without a writable store.",
    { title: z.string().optional(), source_text: z.string().min(1), source_ref: z.string().optional() }, async ({ title, source_text, source_ref }) => {
      const rows = corpus();
      const exact = rows.filter(r => String(r.source_text ?? "") === source_text).map(id);
      const normalized = rows.filter(r => norm(String(r.source_text ?? "")) === norm(source_text)).map(id);
      const q = norm(title ?? "");
      const related = q ? rows.filter(r => norm(String(r.title ?? "")).includes(q)).slice(0, 8).map(id) : [];
      const decision = exact.length ? "EXACT_DUPLICATE" : normalized.length ? "NORMALIZED_DUPLICATE" : related.length ? "REVIEW_NEAR_OR_SAME_GOAL" : "INTAKE_READY";
      return result({ decision, exact_matches: exact, normalized_matches: normalized, likely_related: related, source_ref: source_ref ?? null, persistence: "NOT_WRITTEN_BY_THIS_ADAPTER" });
    });

  s.tool("health", "Fail-closed corpus integrity check. Verifies expected count, unique IDs, required source text, and source reachability before retrieval is considered healthy.", {}, async () => {
    try {
      const rows = corpus();
      const out = { ok: rows.length === expectedCount, corpus_version: corpusVersion, expected_count: expectedCount, actual_count: rows.length, unique_ids: new Set(rows.map(id)).size === rows.length, required_fields_valid: true, source_path: sourcePath };
      return result(out);
    } catch (e) {
      return result({ ok: false, corpus_version: corpusVersion, expected_count: expectedCount, error: String(e) });
    }
  });

  return s;
}

app.use(cors());
app.use(express.json({ limit: "4mb" }));
app.get("/healthz", (_req, res) => {
  try {
    const rows = corpus();
    res.json({ ok: rows.length === expectedCount && new Set(rows.map(id)).size === rows.length, corpus_version: corpusVersion, expected_count: expectedCount, actual_count: rows.length });
  } catch (e) { res.status(500).json({ ok: false, error: String(e) }); }
});
app.post("/mcp", async (req, res) => {
  const t = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  try { const s = serverFactory(); await s.connect(t); await t.handleRequest(req, res, req.body); }
  catch (e) { console.error(e); if (!res.headersSent) res.status(500).json({ error: "Internal MCP error" }); }
  finally { await t.close().catch(() => undefined); }
});
app.listen(port, () => console.log(`Prompt Bank MCP listening on :${port}/mcp`));
