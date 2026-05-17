#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
INTAKE=ROOT/'docs/executions/source-intake-packs'
OUT=ROOT/'docs/executions/approved-source-inventories'
SITE=ROOT/'site/data/source_inventory_progress.json'
INDEX=OUT/'source_inventory_index.csv'


def read_csv(path: Path) -> list[dict[str,str]]:
    if not path.exists():
        return []
    with path.open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))

def main():
    now=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    intake_rows = read_csv(INTAKE/'source_intake_index.csv')
    idx = read_csv(INDEX)
    previous = read_json(SITE)

    by=[]
    candidate_links_total=0
    inventories_with_candidate_links=0
    inventories_needing_attention=0
    for r in idx:
        cnt=int((r.get('candidate_links_count') or '0').strip() or '0')
        candidate_links_total += cnt
        if cnt>0:
            inventories_with_candidate_links += 1
        if r.get('requires_human_attention')=='yes':
            inventories_needing_attention += 1
        by.append({
            'university_id':r.get('university_id',''),
            'university_name':r.get('university_name',''),
            'intake_pack_exists':r.get('intake_pack_exists',''),
            'inventory_exists':r.get('inventory_exists',''),
            'homepage_url':r.get('homepage_url',''),
            'recruitment_url':r.get('recruitment_url',''),
            'fetch_status':r.get('fetch_status','pending_fetch'),
            'candidate_links_count':cnt,
            'requires_human_attention':r.get('requires_human_attention','yes'),
            'blocking_status':r.get('blocking_status',''),
            'last_updated_utc':r.get('last_updated_utc','')
        })

    progress={
      'updated_at_utc':now,
      'total_intake_packs':len(intake_rows),
      'inventories_created':len(idx),
      'inventories_pending':sum(1 for r in idx if r.get('fetch_status')!='fetched'),
      'inventories_with_recruitment_url':sum(1 for r in idx if r.get('recruitment_url')),
      'inventories_with_candidate_links':inventories_with_candidate_links,
      'inventories_needing_attention':inventories_needing_attention,
      'fetch_errors':previous.get('fetch_errors', previous.get('errors', 0)),
      'candidate_links_total':candidate_links_total,
      'progress_events':['Rebuilt source-inventory rollup from approved-source inventory index.'],
      'run_mode': previous.get('run_mode','bounded_approved_source_fetch'),
      'universities_selected': previous.get('universities_selected',0),
      'universities_fetched': previous.get('universities_fetched',0),
      'seed_urls_attempted': previous.get('seed_urls_attempted',0),
      'depth_1_pages_followed': previous.get('depth_1_pages_followed',0),
      'candidate_links_found': previous.get('candidate_links_found',0),
      'output_files_changed': previous.get('output_files_changed',0),
      'run_status': previous.get('run_status','completed_no_links'),
      'no_progress_reason': previous.get('no_progress_reason',''),
      'by_university':by
    }
    SITE.write_text(json.dumps(progress,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')

if __name__=='__main__':
    main()
