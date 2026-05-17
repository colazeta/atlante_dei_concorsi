#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
INTAKE=ROOT/'docs/executions/source-intake-packs'
OUT=ROOT/'docs/executions/approved-source-inventories'
SITE=ROOT/'site/data/source_inventory_progress.json'
INDEX=INTAKE/'source_intake_index.csv'

HDR=["university_id","source_url","link_url","link_text","link_type_hint","same_domain","confidence_level","requires_human_attention","blocking_status","notes","observed_at_utc"]


def extract_url(md:Path,label:str)->str:
    if not md.exists(): return ""
    t=md.read_text(encoding='utf-8',errors='ignore')
    m=re.search(rf"- \*\*{re.escape(label)}\*\*: (.+)",t)
    return m.group(1).strip() if m else ""

def parse_index():
    rows=[]
    with INDEX.open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f): rows.append(r)
    return rows

def write_csv(path:Path,rows:list[dict],header:list[str]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=header); w.writeheader(); w.writerows(rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    now=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    rows=parse_index()
    by=[]; idx=[]
    for r in rows:
        uid=r['university_id']
        pack=INTAKE/uid
        inv=OUT/uid
        homepage=extract_url(pack/'official_urls.md','Official homepage')
        recruitment=extract_url(pack/'official_urls.md','Recruitment/concorsi page')
        inv.mkdir(parents=True,exist_ok=True)
        (inv/'README.md').write_text(f"# Approved source inventory — {uid}\n\nGenerated from intake pack only; no broad crawling, no raw document downloads.\n",encoding='utf-8')
        (inv/'fetch_log.md').write_text(f"# Fetch log\n\n- Generated at: {now}\n- Mode: intake-pack derived scaffold (no network fetch in this run).\n- Blocking status: pending_fetch\n",encoding='utf-8')
        write_csv(inv/'observed_links.csv',[],['university_id','source_url','http_status','content_type','page_title','observed_at_utc'])
        write_csv(inv/'candidate_document_links.csv',[],HDR)
        (inv/'source_limits.md').write_text("# Source limits\n\n- Official URLs from intake pack only.\n- No PDF/raw-document download.\n- Candidate links remain neutral hints pending human review.\n",encoding='utf-8')
        (inv/'handoff.md').write_text("# Handoff\n\nNext step: bounded approved URL fetch with human review of uncertain cases.\n",encoding='utf-8')
        idx.append({'university_id':uid,'university_name':r.get('university_name',''),'intake_pack_exists':'yes','inventory_exists':'yes','homepage_url':homepage,'recruitment_url':recruitment,'fetch_status':'pending_fetch','candidate_links_count':'0','requires_human_attention':'yes' if not recruitment else 'no','blocking_status':'awaiting_bounded_fetch','last_updated_utc':now})
        by.append({**idx[-1]})
    write_csv(OUT/'source_inventory_index.csv',idx,list(idx[0].keys()) if idx else [])
    (OUT/'README.md').write_text(f"# Approved source inventories\n\nGenerated inventories: {len(idx)}\nUpdated: {now}\n",encoding='utf-8')
    progress={
      'updated_at_utc':now,'total_intake_packs':len(rows),'inventories_created':len(rows),'inventories_pending':len(rows),
      'inventories_with_recruitment_url':sum(1 for x in by if x['recruitment_url']),'inventories_with_candidate_links':0,
      'inventories_needing_attention':sum(1 for x in by if x['requires_human_attention']=='yes'),'fetch_errors':0,'candidate_links_total':0,
      'progress_events':['Scaffolded approved source inventories from intake packs without broad crawling or raw downloads.'],'by_university':by
    }
    SITE.write_text(json.dumps(progress,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')

if __name__=='__main__': main()
