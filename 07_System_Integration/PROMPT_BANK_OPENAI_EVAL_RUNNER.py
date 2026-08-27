#!/usr/bin/env python3
"""Fail-closed evaluator for Prompt Bank.

Modes:
  preflight = deterministic structural checks.
  runtime   = refuses to invent a model result; requires a real adapter.
The canonical source file is read-only by this tool.
"""
import argparse, csv, json, re
from pathlib import Path

def load_rows(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            r=json.loads(line)
            r['_text']=r.get('source_text', r.get('prompt_text',''))
            yield r

def audit(text):
    checks={
      'role': bool(re.search(r'(?i)(role|نقش|persona|you are|تو یک|تو فقط)', text)),
      'mission': bool(re.search(r'(?i)(mission|مأموریت|هدف|وظیفه)', text)),
      'inputs': bool(re.search(r'(?i)(input|ورودی|اطلاعات|داده|موضوع)', text)),
      'constraints': bool(re.search(r'(?i)(constraint|محدودیت|قواعد|نباید|الزام)', text)),
      'process': bool(re.search(r'(?i)(مرحله|گام|workflow|pipeline|ابتدا|سپس|→)', text)),
      'output': bool(re.search(r'(?i)(خروجی|output|نتیجه نهایی|فرمت|قالب|schema)', text)),
      'evidence': bool(re.search(r'(?i)(منبع|شواهد|evidence|cite|ارجاع|راستی.?آزمایی|صحت.?سنجی)', text)),
      'examples': bool(re.search(r'(?i)(مثال|example|نمونه)', text)),
      'variables': bool(re.search(r'(\[[^\]]+\]|\{[^}]+\}|placeholder|وارد کنید|اختیاری)', text)),
    }
    defects=[]
    if not checks['mission']: defects.append('MISSING_MISSION_SIGNAL')
    if not checks['output']: defects.append('MISSING_OUTPUT_SIGNAL')
    if len(re.findall(r'\S+', text))>3000: defects.append('MONOLITHIC_LONG_PROMPT')
    return checks,defects

def main():
    p=argparse.ArgumentParser(); p.add_argument('--bank',required=True); p.add_argument('--out',required=True); p.add_argument('--mode',choices=['preflight','runtime'],default='preflight'); a=p.parse_args(); Path(a.out).mkdir(parents=True,exist_ok=True)
    rows=list(load_rows(a.bank))
    if not rows: raise SystemExit('Empty bank')
    if a.mode=='preflight':
        out=[]
        for r in rows:
            c,d=audit(r['_text']); out.append({'prompt_id':r.get('prompt_id',r.get('record_id')),'source_sha256':r.get('prompt_text_sha256',r.get('prompt_sha256','')),'structural_score':sum(c.values()),'defects':'|'.join(d),'static_status':'PASS' if not d else 'REVIEW','semantic_status':'STATIC_PRECHECK_ONLY','runtime_status':'NOT_EXECUTED','release_status':'NOT_RELEASED'})
        with open(Path(a.out)/'static_audit.csv','w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=out[0]); w.writeheader(); w.writerows(out)
        print(json.dumps({'records':len(out),'static_pass':sum(x['static_status']=='PASS' for x in out),'review':sum(x['static_status']=='REVIEW' for x in out)},ensure_ascii=False))
    else:
        out=[]
        for r in rows:
            out.append({'test_id':'RT-'+r.get('prompt_id',r.get('record_id')),'prompt_id':r.get('prompt_id',r.get('record_id')),'source_sha256':r.get('prompt_text_sha256',r.get('prompt_sha256','')),'runtime_status':'BLOCKED_NO_REAL_MODEL_ADAPTER','reason':'A real model endpoint/API adapter and approved fixture are required; no runtime result is fabricated.'})
        with open(Path(a.out)/'runtime_blocked_registry.csv','w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=out[0]); w.writeheader(); w.writerows(out)
        print(json.dumps({'records':len(out),'runtime_status':'BLOCKED_NO_REAL_MODEL_ADAPTER'},ensure_ascii=False))

if __name__=='__main__': main()
