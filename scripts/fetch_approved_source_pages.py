#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from datetime import datetime,timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlparse
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError

ROOT=Path(__file__).resolve().parents[1]
INV_ROOT=ROOT/'docs/executions/approved-source-inventories'
INTAKE_INDEX=ROOT/'docs/executions/source-intake-packs/source_intake_index.csv'
SOURCE_INDEX=INV_ROOT/'source_inventory_index.csv'
SOURCE_PROGRESS=ROOT/'site/data/source_inventory_progress.json'
CAND_PROGRESS=ROOT/'site/data/document_link_classification_progress.json'

CAND_HDR=['university_id','source_url','link_url','link_text','link_type_hint','same_domain','confidence_level','requires_human_attention','blocking_status','notes','observed_at_utc']
OBS_HDR=['university_id','source_url','http_status','content_type','page_title','observed_at_utc','error']
ALLOWED_HINTS={'call_notice_candidate','committee_appointment_candidate','evaluation_criteria_candidate','admission_or_candidate_list_candidate','final_acts_approval_candidate','recruitment_page','competition_listing','other_official_document_candidate','unknown'}

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self._href=None; self._txt=[]; self.title=''
        self._in_title=False
    def handle_starttag(self,tag,attrs):
        if tag=='a': self._href=dict(attrs).get('href'); self._txt=[]
        if tag=='title': self._in_title=True
    def handle_endtag(self,tag):
        if tag=='a' and self._href:
            self.links.append((self._href,' '.join(''.join(self._txt).split())))
            self._href=None; self._txt=[]
        if tag=='title': self._in_title=False
    def handle_data(self,data):
        if self._href is not None: self._txt.append(data)
        if self._in_title: self.title += data

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def read_csv(path):
    if not path.exists(): return []
    with path.open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))

def write_csv(path,rows,header):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=header); w.writeheader(); w.writerows(rows)

def hint(url,text):
    t=f"{url} {text}".lower()
    if any(k in t for k in ['bando','call']): return 'call_notice_candidate'
    if any(k in t for k in ['commissione','committee']): return 'committee_appointment_candidate'
    if any(k in t for k in ['criteri','criteria']): return 'evaluation_criteria_candidate'
    if any(k in t for k in ['graduatoria','ammissione','ammessi']): return 'admission_or_candidate_list_candidate'
    if any(k in t for k in ['approvazione atti','atti finali']): return 'final_acts_approval_candidate'
    if any(k in t for k in ['concorsi','reclutamento','lavora-con-noi']): return 'competition_listing'
    if any(k in t for k in ['pdf','.doc','.odt']): return 'other_official_document_candidate'
    return 'unknown'

def fetch(url):
    req=Request(url,headers={'User-Agent':'atlante-agent/1.0'})
    with urlopen(req,timeout=20) as r:
        ctype=r.headers.get('content-type','')
        status=getattr(r,'status',200)
        data=r.read(1_000_000)
    return status,ctype,data

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--batch-size',type=int,default=5)
    ap.add_argument('--university-id',default='')
    ap.add_argument('--max-links-per-page',type=int,default=40)
    args=ap.parse_args()

    intake=read_csv(INTAKE_INDEX)
    source_idx=read_csv(SOURCE_INDEX)
    picks=[]
    for r in intake:
        if args.university_id and r['university_id']!=args.university_id: continue
        picks.append(r)
    picks=picks[:max(args.batch_size,0)]
    stamp=now()
    errors=0
    for r in picks:
        uid=r['university_id']; inv=INV_ROOT/uid
        urls=[u for u in [r.get('recruitment_page_url',''),r.get('official_homepage_url','')] if u and u!='MISSING']
        source_url=urls[0] if urls else ''
        obs=read_csv(inv/'observed_links.csv'); cand=read_csv(inv/'candidate_document_links.csv')
        log_lines=[f"- {stamp} | uid={uid}"]
        if not source_url:
            obs.append({'university_id':uid,'source_url':'','http_status':'','content_type':'','page_title':'','observed_at_utc':stamp,'error':'missing_approved_url'})
            log_lines.append('  - skipped: missing approved URL in intake index')
            errors+=1
        else:
            try:
                status,ctype,data=fetch(source_url)
                body=data.decode('utf-8',errors='ignore')
                p=LinkParser(); p.feed(body)
                obs.append({'university_id':uid,'source_url':source_url,'http_status':str(status),'content_type':ctype,'page_title':p.title.strip(),'observed_at_utc':stamp,'error':''})
                srcdom=urlparse(source_url).netloc
                count=0
                for href,text in p.links:
                    if count>=args.max_links_per_page: break
                    absu=urljoin(source_url,href)
                    scheme=urlparse(absu).scheme
                    if scheme not in {'http','https'}: continue
                    h=hint(absu,text)
                    if h not in ALLOWED_HINTS: h='unknown'
                    same='yes' if urlparse(absu).netloc==srcdom else 'no'
                    cand.append({'university_id':uid,'source_url':source_url,'link_url':absu,'link_text':text[:300],'link_type_hint':h,'same_domain':same,'confidence_level':'low' if h=='unknown' else 'medium','requires_human_attention':'yes','blocking_status':'needs_human_review','notes':'Observed on approved source page without recursive crawling.','observed_at_utc':stamp})
                    count+=1
                log_lines.append(f'  - fetched: {source_url} status={status} links_recorded={count}')
            except (HTTPError,URLError,TimeoutError,ValueError) as e:
                obs.append({'university_id':uid,'source_url':source_url,'http_status':'','content_type':'','page_title':'','observed_at_utc':stamp,'error':str(e)[:240]})
                log_lines.append(f'  - error: {source_url} err={e}')
                errors+=1
        write_csv(inv/'observed_links.csv',obs,OBS_HDR)
        write_csv(inv/'candidate_document_links.csv',cand,CAND_HDR)
        flog=inv/'fetch_log.md'
        existing=flog.read_text(encoding='utf-8') if flog.exists() else '# Fetch log\n\n'
        flog.write_text(existing+'\n'+'\n'.join(log_lines)+'\n',encoding='utf-8')
        for row in source_idx:
            if row.get('university_id')==uid:
                row['fetch_status']='fetched' if source_url else 'pending_fetch'
                row['candidate_links_count']=str(len(cand))
                row['requires_human_attention']='yes'
                row['blocking_status']='needs_human_review'
                row['last_updated_utc']=stamp
    write_csv(SOURCE_INDEX,source_idx,list(source_idx[0].keys()))

    progress={'updated_at_utc':stamp,'run_mode':'bounded_approved_source_fetch','batch_size':len(picks),'errors':errors,'notes':['Fetched only approved intake URLs; no recursive crawling; no raw document capture.']}
    SOURCE_PROGRESS.write_text(json.dumps(progress,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    CAND_PROGRESS.write_text(json.dumps({'updated_at_utc':stamp,'status':'candidate_links_populated_for_batch','batch_size':len(picks),'errors':errors},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
