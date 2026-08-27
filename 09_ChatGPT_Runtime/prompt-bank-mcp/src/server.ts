import express from "express";
import cors from "cors";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const VERSION = "0.1.0";
const EXPECTED_CORPUS_VERSION = process.env.PROMPT_BANK_CORPUS_VERSION ?? "v3.4";
const EXPECTED_CORPUS_COUNT = Number(process.env.PROMPT_BANK_EXPECTED_COUNT ?? "554");
const PORT = Number(process.env.PORT ?? "3000");
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const DEFAULT_SOURCE_PATH = path.resolve(ROOT, "..", "..", "01_Prompt_Library", "PROMPT_BANK_CANONICAL_SOURCE_v3.4.jsonl");
const SOURCE_PATH = process.env.PROMPT_BANK_SOURCE_PATH ?? DEFAULT_SOURCE_PATH;

type PromptRecord = Record<string, unknown> & {
  record_id?: string; prompt_id?: string; title?: string; source_text?: string;
  source_role?: string; source_type?: string; conversation_id?: string; message_id?: string;
  source_timestamp?: string; semantic_status?: string; runtime_status?: string;
  canonical_status?: string; lifecycle?: string; lineage_status?: string;
};

function loadPrompts(): PromptRecord[] {
  if (!fs.existsSync(SOURCE_PATH)) throw new Error(`Prompt corpus not found at ${SOURCE_PATH}`);
  return fs.readFileSync(SOURCE_PATH, "utf8").split(/\r?\n/).filter(Boolean).map((line, i) => {
    try { return JSON.parse(line) as PromptRecord; }
    catch (e) { throw new Error(`Invalid JSONL at line ${i + 1}: ${String(e)}`); }
  });
}

function normalize(value: string): string { return value.toLocaleLowerCase().replace(/\s+/g, " ").trim(); }
function idOf(r: PromptRecord): string | null { return (r.prompt_id ?? r.record_id ?? null) as string | null; }
function searchableText(r: PromptRecord): string {
  return normalize([r.prompt_id, r.title, r.source_text, r.source_type, r.source_role, r.lifecycle, r.semantic_status, r.runtime_status, r.canonical_status].filter(Boolean).join(" "));
}
function rank(r: PromptRecord, query: string): number {
  const q = normalize(query), text = searchableText(r); if (!q) return 0;
  let score = normalize(String(r.title ?? "")).includes(q) ? 100 : 0;
  if (text.includes(q)) score += 40;
  for (const t of q.split(/\s+/).filter((x) => x.length > 2)) if (text.includes(t)) score += 5;
  if (["VERIFIED", "TESTED"].includes(String(r.runtime_status))) score += 4;
  if (String(r.canonical_status ?? "").includes("CANONICAL")) score += 2;
  return score;
}

function createServer(): McpServer {
  const server = new McpServer({ name: "prompt-bank-mcp", version: VERSION });

  server.tool("search",
    "Use this when the user asks to find a Prompt Bank item by goal, task, role, topic, wording, or natural-language need. Do not require a Prompt ID or the word 'prompt'.",
    { query: z.string().min(1), limit: z.number().int().min(1).max(25).default(8), include_source_text: z.boolean().default(false) },
    async ({ query, limit, include_source_text }) => {
      const records = loadPrompts();
      const results = records.map((r) => ({ r, score: rank(r, query) })).filter((x) => x.score > 0).sort((a, b) => b.score - a.score).slice(0, limit).map(({ r, score }) => ({
        prompt_id: idOf(r), title: r.title ?? null, score, source_role: r.source_role ?? null,
        semantic_status: r.semantic_status ?? null, runtime_status: r.runtime_status ?? null,
        canonical_status: r.canonical_status ?? null, source_text: include_source_text ? r.source_text ?? null : undefined,
        conversation_id: r.conversation_id ?? null, message_id: r.message_id ?? null,
      }));
      const out = { corpus_version: EXPECTED_CORPUS_VERSION, corpus_count: records.length, query, results };
      return { content: [{ type: "text", text: JSON.stringify(out, null, 2) }], structuredContent: out };
    });

  server.tool("fetch",
    "Use this when the user asks for the exact full source text or exact record of a Prompt Bank item. Return the stored source verbatim; never silently rewrite it.",
    { prompt_id: z.string().min(1) },
    async ({ prompt_id }) => {
      const r = loadPrompts().find((x) => idOf(x) === prompt_id);
      if (!r) return { content: [{ type: "text", text: `Prompt ${prompt_id} was not found.` }] };
      const out = { ...r, source_integrity: { source_text_is_verbatim: true } };
      return { content: [{ type: "text", text: JSON.stringify(out, null, 2) }], structuredContent: out };
    });

  server.tool("compare",
    "Use this when the user asks whether Prompt Bank items are duplicates, near-duplicates, variants, complementary prompts, or potential conflicts. Topic similarity alone is not duplication.",
    { prompt_ids: z.array(z.string()).min(2).max(8) },
    async ({ prompt_ids }) => {
      const records = loadPrompts();
      const found = prompt_ids.map((id) => records.find((r) => idOf(r) === id));
      const missing = prompt_ids.filter((_, i) => !found[i]);
      const items = found.filter(Boolean).map((r) => ({ prompt_id: idOf(r!), title: r!.title ?? null, source_text: r!.source_text ?? "", semantic_status: r!.semantic_status ?? null, runtime_status: r!.runtime_status ?? null, lifecycle: r!.lifecycle ?? null, lineage_status: r!.lineage_status ?? null }));
      const same_text = new Set(items.map((x) => normalize(x.source_text))).size === 1;
      const out = { same_text, missing, records: items };
      return { content: [{ type: "text", text: JSON.stringify(out, null, 2) }], structuredContent: out };
    });

  server.tool("ingest_prompt",
    "Use this when the user supplies a new structured instruction or asks to add one. Preserve the text, detect exact duplicates and likely related items, and return an intake decision. Do not claim persistence unless a writable store confirms it.",
    { title: z.string().optional(), source_text: z.string().min(1), source_role: z.string().default("user"), source_ref: z.string().optional() },
    async ({ title, source_text, source_role, source_ref }) => {
      const records = loadPrompts(), incoming = normalize(source_text);
      const exact = records.filter((r) => normalize(String(r.source_text ?? "")) === incoming).map(idOf).filter(Boolean);
      const q = normalize(title ?? "");
      const related = q ? records.filter((r) => normalize(String(r.title ?? "")).includes(q)).slice(0, 8).map(idOf).filter(Boolean) : [];
      const decision = exact.length ? "EXACT_DUPLICATE" : related.length ? "REVIEW_NEAR_OR_SAME_GOAL" : "INTAKE_READY";
      const out = { decision, exact_matches: exact, likely_related: related, source_role, source_ref: source_ref ?? null, persistence: "NOT_WRITTEN_BY_READ_ONLY_ADAPTER" };
      return { content: [{ type: "text", text: JSON.stringify(out, null, 2) }], structuredContent: out };
    });

  server.tool("health", "Use this to verify that the Prompt Bank corpus is reachable and that the loaded version and record count match the configured expectation.", {}, async () => {
    const records = loadPrompts();
    const out = { ok: records.length === EXPECTED_CORPUS_COUNT, service: "prompt-bank-mcp", version: VERSION, corpus_version: EXPECTED_CORPUS_VERSION, expected_count: EXPECTED_CORPUS_COUNT, actual_count: records.length };
    return { content: [{ type: "text", text: JSON.stringify(out, null, 2) }], structuredContent: out };
  });

  return server;
}

const app = express();
app.use(cors());
app.use(express.json({ limit: "4mb" }));
app.get("/healthz", (_req, res) => { try { const n = loadPrompts().length; res.json({ ok: n === EXPECTED_CORPUS_COUNT, corpus_version: EXPECTED_CORPUS_VERSION, expected_count: EXPECTED_CORPUS_COUNT, actual_count: n, version: VERSION }); } catch (e) { res.status(500).json({ ok: false, error: String(e) }); } });
app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  try { const server = createServer(); await server.connect(transport); await transport.handleRequest(req, res, req.body); }
  catch (e) { console.error(e); if (!res.headersSent) res.status(500).json({ error: "Internal MCP error" }); }
  finally { await transport.close().catch(() => undefined); }
});
app.listen(PORT, () => console.log(`Prompt Bank MCP listening on http://localhost:${PORT}/mcp`));
