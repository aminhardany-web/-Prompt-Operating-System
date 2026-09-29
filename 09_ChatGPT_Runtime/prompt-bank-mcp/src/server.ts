import express from "express";
import cors from "cors";
import fs from "node:fs";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const app = express();
const port = Number(process.env.PORT ?? 3000);
const sourcePath = process.env.PROMPT_BANK_SOURCE_PATH ?? "./PROMPT_BANK_CANONICAL_SOURCE_v3.4.jsonl";
const expectedCount = Number(process.env.PROMPT_BANK_EXPECTED_COUNT ?? 554);
const corpusVersion = process.env.PROMPT_BANK_CORPUS_VERSION ?? "v3.4";

type RecordT = { prompt_id?: string; record_id?: string; title?: string; source_text?: string; [k:string]: unknown };
const id = (r: RecordT) => String(r.prompt_id ?? r.record_id ?? "");
const norm = (s: string) => s.toLocaleLowerCase().replace(/\s+/g," ").trim();
const load = (): RecordT[] => {
  if (!fs.existsSync(sourcePath)) throw new Error(`Prompt corpus not found: ${sourcePath}`);
  return fs.readFileSync(sourcePath,"utf8").split(/\r?\n/).filter(Boolean).map((x,i)=>{try{return JSON.parse(x) as RecordT}catch(e){throw new Error(`Invalid JSONL line ${i+1}: ${String(e)}`)}});
};
const stopWords = new Set(["برای","از","به","در","با","را","که","این","آن","یک","و","یا","the","for","and","with","find","prompt"]);
const tokens = (s:string) => norm(s).split(/\s+/).filter(x=>x.length>2 && !stopWords.has(x));
const intentAction = (q:string) => {
  const x=norm(q);
  if(/ممیزی|audit|بررسی|کنترل کیفیت|بازبینی/.test(x)) return "AUDIT_SOURCE";
  if(/بهینه|اصلاح|ارتقا|rewrite|optimi/.test(x)) return "DERIVE_OPTIMIZED";
  if(/تست|آزمون|ارزیابی|test|evaluate/.test(x)) return "TEST_PROMPT";
  return "USE_SOURCE";
};
const searchScore = (r: RecordT,q: string) => {
  const query=norm(q); if(!query)return 0;
  const title=norm(String(r.title??"")); const body=norm(String(r.source_text??""));
  const meta=norm([r.record_id,r.prompt_id,r.canonical_status,r.semantic_status,r.runtime_status].filter(Boolean).join(" "));
  const ts=tokens(q); let s=0;
  if(title===query) s+=160; else if(title.includes(query)) s+=100;
  if(body.includes(query)) s+=45;
  for(const t of ts) {
    if(title.includes(t)) s+=14;
    else if(body.includes(t)) s+=4;
    if(meta.includes(t)) s+=3;
  }
  const coverage=ts.length ? ts.filter(t=>title.includes(t)||body.includes(t)).length/ts.length : 0;
  s += Math.round(coverage*30);
  return s;
};

function serverFactory(){
  const s=new McpServer({name:"prompt-bank-mcp",version:"0.1.0"});
  s.tool("search","Use when the user asks to find a prompt or reusable engineered instruction by goal, task, role, topic, or natural-language need. Do not require the word prompt or a Prompt ID.",
    {query:z.string().min(1),limit:z.number().int().min(1).max(25).default(8)},async({query,limit})=>{
      const rs=load().map(r=>({r,score:searchScore(r,query)})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,limit).map(x=>({prompt_id:id(x.r),title:x.r.title??null,score:x.score,source_text:x.r.source_text??null,metadata:x.r}));
      const out={corpus_version:corpusVersion,corpus_count:load().length,query,action:intentAction(query),results:rs}; return {content:[{type:"text",text:JSON.stringify(out,null,2)}],structuredContent:out};
    });
  s.tool("toolbox","Use when the user describes a work need and wants a reusable starting point. Return candidate source prompts plus the suggested operational action. Do not modify or promote the canonical corpus.",{query:z.string().min(1),limit:z.number().int().min(1).max(10).default(5)},async({query,limit})=>{
    const rs=load().map(r=>({r,score:searchScore(r,query)})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,limit).map(x=>({prompt_id:id(x.r),title:x.r.title??null,score:x.score,match_reason:"lexical/field-aware match; semantic equivalence not proven"}));
    const out={corpus_version:corpusVersion,corpus_count:load().length,query,suggested_action:intentAction(query),results:rs,scope:"Canonical-554 only; broader Library/Project assets require a separate authorized search."};
    return {content:[{type:"text",text:JSON.stringify(out,null,2)}],structuredContent:out};
  });
  s.tool("fetch","Use when the user asks for the full source text of a known Prompt Bank item. Return it verbatim and do not rewrite it.",{prompt_id:z.string().min(1)},async({prompt_id})=>{
    const r=load().find(x=>id(x)===prompt_id); if(!r)return{content:[{type:"text",text:`Prompt ${prompt_id} not found.`}]};
    const out={...r,source_integrity:{source_text_is_verbatim:true}}; return{content:[{type:"text",text:JSON.stringify(out,null,2)}],structuredContent:out};
  });
  s.tool("compare","Use when the user asks whether Prompt Bank items are duplicates, near-duplicates, variants, complementary prompts, or conflicts. Similar topic alone is not duplication.",{prompt_ids:z.array(z.string()).min(2).max(8)},async({prompt_ids})=>{
    const rs=load(); const found=prompt_ids.map(x=>rs.find(r=>id(r)===x)); const missing=prompt_ids.filter((_,i)=>!found[i]);
    const items=found.filter(Boolean).map(r=>({prompt_id:id(r!),title:r!.title??null,source_text:r!.source_text??"",metadata:r}));
    const same_text=new Set(items.map(x=>norm(x.source_text))).size===1; const out={same_text,missing,records:items}; return{content:[{type:"text",text:JSON.stringify(out,null,2)}],structuredContent:out};
  });
  s.tool("ingest_prompt","Use when the user supplies a new structured instruction. Preserve the source, check exact duplicates and related titles, and report an intake decision. Do not claim that a write happened unless a writable store confirms it.",{title:z.string().optional(),source_text:z.string().min(1),source_ref:z.string().optional()},async({title,source_text,source_ref})=>{
    const rs=load(); const exact=rs.filter(r=>norm(String(r.source_text??""))===norm(source_text)).map(id); const q=norm(title??""); const related=q?rs.filter(r=>norm(String(r.title??"")).includes(q)).slice(0,8).map(id):[];
    const decision=exact.length?"EXACT_DUPLICATE":related.length?"REVIEW_NEAR_OR_SAME_GOAL":"INTAKE_READY"; const out={decision,exact_matches:exact,likely_related:related,source_ref:source_ref??null,persistence:"NOT_WRITTEN_BY_THIS_ADAPTER"}; return{content:[{type:"text",text:JSON.stringify(out,null,2)}],structuredContent:out};
  });
  s.tool("health","Use to verify that the configured Prompt Bank corpus is reachable and matches the expected record count.",{},async()=>{const n=load().length;const out={ok:n===expectedCount,corpus_version:corpusVersion,expected_count:expectedCount,actual_count:n};return{content:[{type:"text",text:JSON.stringify(out,null,2)}],structuredContent:out};});
  return s;
}

app.use(cors()); app.use(express.json({limit:"4mb"}));
app.get("/healthz",(_req,res)=>{try{const n=load().length;res.json({ok:n===expectedCount,corpus_version:corpusVersion,expected_count:expectedCount,actual_count:n});}catch(e){res.status(500).json({ok:false,error:String(e)});}});
app.post("/mcp",async(req,res)=>{const t=new StreamableHTTPServerTransport({sessionIdGenerator:undefined,enableJsonResponse:true});try{const s=serverFactory();await s.connect(t);await t.handleRequest(req,res,req.body);}catch(e){console.error(e);if(!res.headersSent)res.status(500).json({error:"Internal MCP error"});}finally{await t.close().catch(()=>undefined);}});
app.listen(port,()=>console.log(`Prompt Bank MCP listening on :${port}/mcp`));
