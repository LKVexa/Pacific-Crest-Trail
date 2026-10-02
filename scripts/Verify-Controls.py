"""Verify complete control registration; full acceptance is a separate strict gate."""
import argparse
import json
from collections import Counter
from pathlib import Path

def assess(root):
    current=json.loads((root/'content'/'controls.json').read_text(encoding='utf-8'))
    original=json.loads((root/'requirements'/'original_control_register.json').read_text(encoding='utf-8'))
    expected={c['id']:c['text'] for g in original['groups'] for p in g['controls'] for c in p['children']}
    rows=[c for g in current['groups'] for p in g['controls'] for c in p['children']]
    ids=[r['id'] for r in rows]
    errors=[]
    if len(rows)!=3720 or len(set(ids))!=3720 or set(ids)!=set(expected):errors.append('All 3,720 original child IDs must occur exactly once.')
    for row in rows:
        if row['text']!=expected.get(row['id']):errors.append(row['id']+': original requirement text differs.')
        if row.get('applicability')!='applicable':errors.append(row['id']+': full requested scope requires a reviewed explicit disposition before exclusion.')
        if not row.get('component_artifacts') or not row.get('owner'):errors.append(row['id']+': missing component binding or owner role.')
        if row.get('status')=='verified' and (not row.get('implementation_reference') or not row.get('evidence_references') or not row.get('reviewer') or not row.get('review_date')):
            errors.append(row['id']+': verification claim lacks required evidence/reviewer/date.')
        if row.get('status')=='exception_accepted':errors.append(row['id']+': no exception may be invented on the product owner\'s behalf.')
    statuses=Counter(row.get('status','missing') for row in rows)
    return {'registered':len(rows),'unique_ids':len(set(ids)),'original_requirements_unchanged':not errors,'registration_errors':errors,'statuses':dict(statuses),'unverified':sum(row.get('status')!='verified' for row in rows),'full_release_allowed':not errors and all(row.get('status')=='verified' for row in rows)}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--require-all-verified',action='store_true')
    args=parser.parse_args()
    result=assess(args.root.resolve())
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if result['registration_errors'] else 2 if args.require_all_verified and not result['full_release_allowed'] else 0)
