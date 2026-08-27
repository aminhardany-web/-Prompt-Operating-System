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
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DEFAULT_SOURCE_PATH = path.resolve(ROOT, "..", "..", "01_Prompt_Library", "PROMPT_BANK_CANONICAL_SOURCE_v3.4.jsonl");
const SOURCE_PATH = process.env.PROMPT_BANK_SOURCE_PATH ?? DEFAULT_SOURCE_PATH;

interface PromptRecord {
  record_id?: string;
  prompt_id?: string;
  title?: string;
  source_text?: string;
  source_role?: string;
  source_type?: string;
  conversation_id?: string;
  message_id?: string;
  source_file?: string;
  source_timestamp?: string;
  source_sha256?: string;
  prompt_text_sha256?: string;
  discovery_status?: string;
  semantic_status?: string;
  runtime_status?: string;
  canonical_status?: string;
  lifecycle?: string;
  lineage_status?: string;
  parent_message_id?: string;
  source_segment_index?: number;
  [key: string]: unknown;
}

function loadPrompts(): PromptRecord[] {
  if (!fs.existsSync(SOURCE_PATH)) {
    throw new Error(`Prompt corpus not found at ${SOURCE_PATH}. Set PROMPT_BANK_SOURCE_PATH to the deployed corpus path.`);
  }
  const lines = fs.readFileSync(SOURCE_PATH, "utf8").split(/\r?\n/).filter(Boolean);
  const records: PromptRecord[] = [];
  for (const [index, line] of lines.entries()) {
    try {
      const value = JSON.parse(line) as PromptRecord;
      if (typeof value === "object" && value !== null) records.push(value);
    } catch (error) {
      throw new Error(`Invalid JSONL at line ${index + 1}: ${String(error)}`);
    }
  }
  return records;
}

function normalize(value: string): string {
  return value.toLocaleLowerCase().replace(/\s+/g, " ").trim();
}

function searchableText(record: PromptRecord): string {
  return normalize([
    record.prompt_id,
    record.title,
    record.source_text,
    record.source_type,
    record.source_role,
    record.discovery_status,
    record.semantic_status,
    record.runtime_status,
    record.canonical_status,
    record.lifecycle,
  ].filter(Boolean).join(" "));
}

function rankRecord(record: PromptRecord, query: string): number {
  const q = normalize(query);
  if (!q) return 0;
  const text = searchableText(record);
  let score = 0;
  if (normalize(record.title ?? "").includes(q)) score += 100;
  if (text.includes(q)) score += 40;
  for (const token of q.split(/\s+/).filter((t) => t.length > 2)) {
    if (text.includes(token)) score += 5;
  }
  if (record.runtime_status === "VERIFIED" || record.runtime_status === "TESTED") score += 4;
  if (record.canonical_status?.includes("CANONICAL")) score += 2;
  return score;
}

function createServer(): McpServer {
  const server = new McpServer({ name: "prompt-bank-mcp", version: VERSION });

  server.tool(
    "search",
    "Use this when the user asks to find a Prompt Bank item by goal, task, role, topic, wording, or natural-language need. Search semantically across titles, source text, lifecycle and status; do not require the user to know a prompt ID or to say the word prompt.",
    {
      query: z.string().min(1),
      limit: z.number().int().min(1).max(25).default(8),
      include_source_text: z.boolean().default(false),
    },
    async ({ query, limit, include_source_text }) => {
      const records = loadPrompts();
      const results = records
        .map((record) => ({ record, score: rankRecord(record, query) }))
        .filter(({ score }) => score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, limit)
        .map(({ record, score }) => ({
          prompt_id: record.prompt_id ?? record.record_id ?? null,
          title: record.title ?? null,
          score,
          source_role: record.source_role ?? null,
          semantic_status: record.semantic_status ?? null,
          runtime_status: record.runtime_status ?? null,
          canonical_status: record.canonical_status ?? null,
          source_text: include_source_text ? record.source_text ?? null : undefined,
          conversation_id: record.conversation_id ?? null,
          message_id: record.message_id ?? null,
        }));

      return {
        content: [{ type: "text", text: JSON.stringify({ corpus_version: EXPECTED_CORPUS_VERSION, corpus_count: records.length, query, results }, null, 2) }],
        structuredContent: { corpus_version: EXPECTED_CORPUS_VERSION, corpus_count: records.length, query, results },
      };
    },
  );

  server.tool(
    "fetch",
    "Use this when the user asks for the full text or exact record of a Prompt Bank item after it has been identified. Return source text verbatim; never silently rewrite the stored source.",
    {
      prompt_id: z.string().min(1),
    },
    async ({ prompt_id }) => {
      const records = loadPrompts();
      const record = records.find((item) => (item.prompt_id ?? item.record_id) === prompt_id);
      if (!record) {
        return { content: [{ type: "text", text: `Prompt ${prompt_id} was not found in corpus ${EXPECTED_CORPUS_VERSION}.` }] };
      }
      const result = {
        ...record,
        source_integrity: {
          source_text_is_verbatim: true,
          semantic_status: record.semantic_status ?? "UNKNOWN",
          runtime_status: record.runtime_status ?? "UNKNOWN",
        },
      };
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        structuredContent: result,
      };
    },
  );

  server.tool(
    "compare",
    "Use this when the user asks whether two or more Prompt Bank items are duplicates, near-duplicates, variants, complementary prompts, or potentially conflicting versions. Compare exact source text and task intent without assuming that topic similarity means duplication.",
    {
      prompt_ids: z.array(z.string()).min(2).max(8),
    },
    async ({ prompt_ids }) => {
      const records = loadPrompts();
      const selected = prompt_ids.map((id) => records.find((item) => (item.prompt_id ?? item.record_id) === id));
      const missing = prompt_ids.filter((_, index) => !selected[index]);
      const comparisons = selected.filter(Boolean).map((record) => ({
        prompt_id: record!.prompt_id ?? record!.record_id ?? null,
        title: record!.title ?? null,
        source_text: record!.source_text ?? "",
        semantic_status: record!.semantic_status ?? null,
        runtime_status: record!.runtime_status ?? null,
        lifecycle: record!.lifecycle ?? null,
        lineage_status: record!.lineage_status ?? null,
      }));
      const sameText = new Set(comparisons.map((r) => normalize(r.source_text))).size === 1;
      return {
        content: [{ type: "text", text: JSON.stringify({ same_text: sameText, missing, records: comparisons }, null, 2) }],
        structuredContent: { same_text: sameText, missing, records: comparisons },
      };
    },
  );

  server.tool(
    "ingest_prompt",
    "Use this when the user supplies a new structured instruction or asks to add one to the Prompt Bank. Preserve the submitted text, compute identity metadata, check for likely duplicates, and return an intake decision. Persistence must be supplied by the deployment's configured writable store; never claim a write succeeded unless it did.",
    {
      title: z.string().optional(),
      source_text: z.string().min(1),
      source_role: z.string().default("user"),
      source_ref: z.string().optional(),
    },
    async ({ title, source_text, source_role, source_ref }) => {
      const records = loadPrompts();
      const incoming = normalize(source_text);
      const exact = records.filter((record) => normalize(record.source_text ?? "") === incoming);
      const sameGoal = records.filter((record) => {
        const q = normalize(title ?? "");
        return q.length > 2 && normalize(record.title ?? "").includes(q);
      }).slice(0, 8);
      const decision = exact.length ? "EXACT_DUPLICATE" : sameGoal.length ? "REVIEW_NEAR_OR_SAME_GOAL" : "INTAKE_READY";
      return {
        content: [{ type: "text", text: JSON.stringify({ decision, exact_matches: exact.map((r) => r.prompt_id ?? r.record_id), likely_related: sameGoal.map((r) => r.prompt_id ?? r.record_id), preserved_source_sha256: null, source_role, source_ref: source_ref ?? null, persistence: "NOT_WRITTEN_BY_THIS_READ_ONLY_ADAPTER" }, null, 2) }],
        structuredContent: { decision, exact_matches: exact.map((r) => r.prompt_id ?? r.record_id), likely_related: sameGoal.map((r) => r.prompt_id ?? r.record_id), source_role, source_ref: source_ref ?? null, persistence: "NOT_WRITTEN_BY_THIS_READ_ONLY_ADAPTER" },
      };
    },
  );

  server.tool(
    "health",
    "Use this to verify that the Prompt Bank corpus is reachable and that the runtime loaded the expected corpus version and record count.",
    {},
    async () => {
      const records = loadPrompts();
      const ok = records.length === EXPECTED_CORPUS_COUNT;
      return {
        content: [{ type: "text", text: JSON.stringify({ ok, service: "prompt-bank-mcp", version: VERSION, corpus_version: EXPECTED_CORPUS_VERSION, expected_count: EXPECTED_CORPUS_COUNT, actual_count: records.length, source_path: SOURCE_PATH }, null, 2) }],
        structuredContent: { ok, service: "prompt-bank-mcp", version: VERSION, corpus_version: EXPECTED_CORPUS_VERSION, expected_count: EXPECTED_CORPUS_COUNT, actual_count: records.length },
      };
    },
  );

  return server;
}

const app = express();
app.use(cors());
app.use(express.json({ limit: "4mb" }));

app.get("/healthz", (_req, res) => {
  try {
    const records = loadPrompts();
    res.json({ ok: records.length === EXPECTED_CORPUS_COUNT, service: "prompt-bank-mcp", version: VERSION, corpus_version: EXPECTED_CORPUS_VERSION, expected_count: EXPECTED_CORPUS_COUNT, actual_count: records.length });
  } catch (error) {
    res.status(500).json({ ok: false, error: String(error) });
  }
});

app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  try {
    const server = createServer();
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    console.error(error);
    if (!res.headersSent) res.status(500).json({ error: "Internal MCP error" });
  } finally {
    await transport.close().catch(() => undefined);
  }
});

app.listen(PORT, () => {
  console.log(`Prompt Bank MCP listening on http://localhost:${PORT}/mcp`);
});
