"""Aggregate sealed, previously validated outcomes on NOTS; never fit models."""
import pathlib,csv,json,hashlib,statistics,itertools,datetime,os,platform,math
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'outputs'/('comparison_'+os.environ['SLURM_JOB_ID']);OUT.mkdir(parents=True,exist_ok=False)
config=json.loads((ROOT/'imports.json').read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
for role in config['json_roles']:
 r=config['inputs'][role];p=ROOT/r['file'];assert sha(p)==r['sha256'];j=json.loads(p.read_text(encoding='utf-8-sig'))
 if role.endswith('_archive_receipt'):assert j['all_member_sha256_verified'] and j['local_readback_verified'] and j['physical_files_only']
 if role=='final_receipt':assert j['status']=='FINAL_STRICT_SUMMARY_PASS' and j['verified_cases']==3000 and j['failed_cases']==0
 if role=='final_provenance':assert j['mixture_rows_sha256']==config['inputs']['mixture']['sha256'] and j['inventory_sha256']==config['inputs']['mixture_inventory']['sha256']
for role,binding in config['archive_bindings'].items():
 m=config['inputs'][binding['manifest_role']];p=ROOT/m['file'];assert sha(p)==m['sha256']
 entries=json.loads(p.read_text(encoding='utf-8-sig'))['entries'];found=[e for e in entries if e['path']==binding['member']]
 assert len(found)==1 and found[0]['sha256']==config['inputs'][role]['sha256'],role
def read(role):
 r=config['inputs'][role];p=ROOT/r['file'];assert sha(p)==r['sha256'],role
 return list(csv.DictReader(p.open(newline='',encoding='utf-8-sig')))
def write(name,rows):
 rows=list(rows);assert rows,name
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def boolean(v):assert str(v).upper() in ('TRUE','FALSE');return str(v).upper()=='TRUE'
TRUTH={3,97,194,286,385,478};SCALES=['c100','c075','c050','c035','c025'];SCALE_VALUE=dict(zip(SCALES,[1,.75,.5,.35,.25]))
METHODS=['Original BB+HPM','Mixture BB+HPM','Lasso EBIC gamma=0.5','Lasso EBIC gamma=1','Lasso CV minimum','Lasso CV 1SE','MCP EBIC gamma=0.5','MCP EBIC gamma=1','ABESS EBIC gamma=0.5','ABESS EBIC gamma=1']
LOOKUP={('Lasso','EBIC_0.5'):METHODS[2],('Lasso','EBIC_1'):METHODS[3],('Lasso','CV_min'):METHODS[4],('Lasso','CV_1se'):METHODS[5],('MCP','EBIC_0.5'):METHODS[6],('MCP','EBIC_1'):METHODS[7],('ABESS','EBIC_0.5'):METHODS[8],('ABESS','EBIC_1'):METHODS[9]}
def support(s):
 if s=='':return set()
 parts=s.split(';');assert all(x.isdigit() and str(int(x))==x and 1<=int(x)<=500 for x in parts),s
 v=list(map(int,parts));assert len(v)==len(set(v));return set(v)
expected={f'{key}_S{s}_r{r:03}' for key in SCALES for s in range(1,7) for r in range(1,101)}
pair_rows=read('pairing');pair={r['case_id']:r for r in pair_rows};assert len(pair_rows)==len(pair)==3000 and set(pair)==expected
inventory=read('mixture_inventory');assert len(inventory)==3000 and {r['case_id'] for r in inventory}==expected
assert all(boolean(r['completed']) and not boolean(r['failed']) and not boolean(r['pending_or_unknown']) and r['exit_status']=='0' and not r['validation_error'] for r in inventory)
rows=[];sets={};family_times={}
def normalize(raw,method,family,kind):
 id=raw['case_id'];assert id in expected;p=pair[id];key=id.split('_')[0];s=int(raw['scenario']);rep=int(raw['replicate'])
 assert id==f'{key}_S{s}_r{rep:03}' and raw['base_input_sha256']==p['base_input_sha256']
 assert raw['scale_key']==key and float(raw['scale'])==SCALE_VALUE[key]
 for f in ['response_sha256','noise_sha256','components_sha256','signal_sha256','input_manifest_sha256']:
  if raw.get(f):assert raw[f]==p[f],(id,method,f)
 selected=support(raw['support'] if kind=='benchmark' else raw['selected'])
 if kind!='benchmark' or 'EBIC' in method:assert len(selected)<=100
 fp=len(selected-TRUTH);fn=len(TRUTH-selected);exact=fp==fn==0
 assert fp==int(raw['fp']) and fn==int(raw['fn']) and exact==boolean(raw['exact'] if kind=='benchmark' else raw['exact_recovery'])
 status=raw['status'] if kind=='benchmark' else 'ok';assert status in ('ok','warning')
 if kind=='benchmark':assert boolean(raw['success'])
 else:assert not raw.get('exit_status') or int(raw['exit_status'])==0
 seconds=float(raw['seconds']);assert math.isfinite(seconds) and seconds>=0
 k=(id,family)
 if k in family_times:assert family_times[k]==seconds
 family_times[k]=seconds
 source=config['source_seals']['benchmark' if kind=='benchmark' else ('mixture' if method==METHODS[1] else 'original')]
 if isinstance(source,dict):source=source[key]
 if raw.get('source_sha256'):assert raw['source_sha256']==source
 search=boolean(raw['search_failure']) if raw.get('search_failure') else None
 row=dict(case_id=id,method_id=method,scale_key=key,scale=SCALE_VALUE[key],scenario=s,replicate=rep,
  canonical_support=';'.join(map(str,sorted(selected))),selected_size=len(selected),exact_recovery=exact,fp=fp,fn=fn,
  error_category='exact' if exact else ('extra_only' if fn==0 else ('missed_only' if fp==0 else 'mixed')),
  execution_status=status,search_failure=search,elapsed_seconds=seconds,
  runtime_scope='shared benchmark family path+tuning+selection cost' if kind=='benchmark' else 'BB case setup+compilation+schedule pilot+four islands; excludes final write',
  family=family,source_sha256=source,source_artifact_sha256=config['inputs'][kind if kind=='benchmark' else ('mixture' if method==METHODS[1] else 'original')]['sha256'])
 for f in ['base_input_sha256','response_sha256','noise_sha256','components_sha256','signal_sha256','input_manifest_sha256']:row[f]=p[f]
 rows.append(row);assert (id,method) not in sets;sets[id,method]=selected
for r in read('original'):normalize(r,METHODS[0],METHODS[0],'bb')
for r in read('mixture'):normalize(r,METHODS[1],METHODS[1],'bb')
for r in read('benchmark'):normalize(r,LOOKUP[r['method'],r['selector']],r['method'],'benchmark')
assert len(rows)==len(sets)==30000
for m in METHODS:assert {r['case_id'] for r in rows if r['method_id']==m}==expected
write('comparison_case_rows.csv',rows)
def metrics(z,den):
 assert len(z)==den
 cats={c:sum(r['error_category']==c for r in z) for c in ['exact','extra_only','missed_only','mixed']};assert sum(cats.values())==den
 times=[r['elapsed_seconds'] for r in z];sizes=[r['selected_size'] for r in z]
 return dict(expected=den,verified=len(z),failed=0,pending=0,exact=cats['exact'],extra_only=cats['extra_only'],missed_only=cats['missed_only'],mixed=cats['mixed'],
  total_fp=sum(r['fp'] for r in z),total_fn=sum(r['fn'] for r in z),mean_fp=statistics.mean(r['fp'] for r in z),mean_fn=statistics.mean(r['fn'] for r in z),
  cases_any_fp=sum(r['fp']>0 for r in z),cases_any_fn=sum(r['fn']>0 for r in z),mean_selected_size=statistics.mean(sizes),median_selected_size=statistics.median(sizes),
  runtime_seconds_sum=sum(times),runtime_seconds_median=statistics.median(times),search_failures=sum(r['search_failure'] is True for r in z),
  search_flag_applicable=any(r['search_failure'] is not None for r in z),warning_successes=sum(r['execution_status']=='warning' for r in z))
scenario=[];scale=[];overall=[];active=[]
for m in METHODS:
 z=[r for r in rows if r['method_id']==m];overall.append(dict(method_id=m,**metrics(z,3000)))
 for key in SCALES:
  q=[r for r in z if r['scale_key']==key];scale.append(dict(method_id=m,scale_key=key,scale=SCALE_VALUE[key],**metrics(q,600)))
  for s in range(1,7):
   t=[r for r in q if r['scenario']==s];scenario.append(dict(method_id=m,scale_key=key,scenario=s,**metrics(t,100)))
   for v in sorted(TRUTH):active.append(dict(method_id=m,scale_key=key,scenario=s,variable=v,denominator=100,selected=sum(v in sets[r['case_id'],m] for r in t)))
write('scenario_comparison.csv',scenario);write('scale_comparison.csv',scale);write('overall_comparison.csv',overall);write('active_selection_counts.csv',active)
scenario_index={(r['method_id'],r['scale_key'],str(r['scenario'])):r for r in scenario}
reconciled=[]
for r in read('benchmark_scenario'):
 m=LOOKUP[r['method'],r['selector']];q=scenario_index[m,r['scale_key'],r['scenario']]
 for imported,derived in [('exact','exact'),('fp','total_fp'),('fn','total_fn'),('mixed','mixed'),('extra_only','extra_only'),('missed_only','missed_only')]:assert int(r[imported])==q[derived],(m,r['scale_key'],r['scenario'],imported)
 reconciled.append(dict(method_id=m,scale_key=r['scale_key'],scenario=r['scenario'],exact=q['exact'],passed=True))
for r in read('final_bb_scenario'):
 if r['scenario']=='total':continue
 m=r['method'];q=scenario_index[m,r['scale_key'],r['scenario']]
 for field in ['exact','extra_only','missed_only','mixed','total_fp','total_fn']:assert int(r[field])==q[field]
 reconciled.append(dict(method_id=m,scale_key=r['scale_key'],scenario=r['scenario'],exact=q['exact'],passed=True))
assert len(reconciled)==300 and len({(r['method_id'],r['scale_key'],r['scenario']) for r in reconciled})==300
write('independent_scenario_reconciliation.csv',reconciled)
def wide(key=None):
 result=[]
 for m in METHODS:
  d={'method':m}
  if key is None:
   for k in SCALES:d[k]=f"{next(r['exact'] for r in scale if r['method_id']==m and r['scale_key']==k)}/600"
   d['total']=f"{next(r['exact'] for r in overall if r['method_id']==m)}/3000"
  else:
   for s in range(1,7):d[f'S{s}']=f"{next(r['exact'] for r in scenario if r['method_id']==m and r['scale_key']==key and r['scenario']==s)}/100"
  result.append(d)
 return result
tables={'recovery_10methods_5scales.csv':wide()};tables.update({f'recovery_{k}_10methods_6scenarios.csv':wide(k) for k in SCALES})
for name,t in tables.items():write(name,t)
with (OUT/'recovery_tables.md').open('w',encoding='utf-8') as f:
 for name,t in tables.items():
  f.write(name+'\n\n');cols=list(t[0]);f.write('| '+' | '.join(cols)+' |\n| '+' | '.join(['---']*len(cols))+' |\n')
  for r in t:f.write('| '+' | '.join(str(r[c]) for c in cols)+' |\n')
  f.write('\n')
paired=[];changes=[];active_changes=[]
rowmap={(r['case_id'],r['method_id']):r for r in rows}
for key in SCALES:
 for s in list(range(1,7))+['total']:
  ids=sorted(i for i in expected if i.startswith(key+'_') and (s=='total' or f'_S{s}_' in i));n=len(ids)
  for a,b in itertools.combinations(METHODS,2):
   av=[rowmap[i,a]['exact_recovery'] for i in ids];bv=[rowmap[i,b]['exact_recovery'] for i in ids]
   paired.append(dict(scale_key=key,scenario=s,method_a=a,method_b=b,paired_n=n,both_correct=sum(x and y for x,y in zip(av,bv)),
    a_only=sum(x and not y for x,y in zip(av,bv)),b_only=sum(not x and y for x,y in zip(av,bv)),both_wrong=sum(not x and not y for x,y in zip(av,bv))))
 for id in sorted(i for i in expected if i.startswith(key+'_')):
  a=sets[id,METHODS[0]];b=sets[id,METHODS[1]];oa=a-TRUTH;mb=b-TRUTH;rescue=(b-a)&TRUTH;miss=(a-b)&TRUTH;added=mb-oa;removed=oa-mb
  changes.append(dict(case_id=id,scale_key=key,scenario=rowmap[id,METHODS[0]]['scenario'],rescues=len(rescue),new_misses=len(miss),
   added_inactive=len(added),removed_inactive=len(removed),more_fp=len(mb)>len(oa),fewer_fp=len(mb)<len(oa),equal_fp=len(mb)==len(oa),
   noise_identity_swap=len(mb)==len(oa) and mb!=oa,identical_support=a==b,
   rescued_ids=';'.join(map(str,sorted(rescue))),new_miss_ids=';'.join(map(str,sorted(miss))),added_inactive_ids=';'.join(map(str,sorted(added))),removed_inactive_ids=';'.join(map(str,sorted(removed)))))
  assert len(rescue)-len(miss)==rowmap[id,METHODS[0]]['fn']-rowmap[id,METHODS[1]]['fn']
  assert len(added)-len(removed)==rowmap[id,METHODS[1]]['fp']-rowmap[id,METHODS[0]]['fp']
  for v in sorted(TRUTH):active_changes.append(dict(case_id=id,scale_key=key,scenario=rowmap[id,METHODS[0]]['scenario'],variable=v,rescued=v in rescue,new_miss=v in miss))
for a,b in itertools.combinations(METHODS,2):
 t=[r for r in paired if r['scenario']=='total' and r['method_a']==a and r['method_b']==b]
 paired.append(dict(scale_key='overall',scenario='total',method_a=a,method_b=b,paired_n=3000,
  **{f:sum(r[f] for r in t) for f in ['both_correct','a_only','b_only','both_wrong']}))
write('paired_discordance.csv',paired);write('paired_support_changes.csv',changes);write('paired_active_changes.csv',active_changes)
change_summaries=[];active_change_summaries=[];active_totals=[]
for key in SCALES+['overall']:
 for s in list(range(1,7))+['total']:
  t=[r for r in changes if (key=='overall' or r['scale_key']==key) and (s=='total' or r['scenario']==s)]
  change_summaries.append(dict(scale_key=key,scenario=s,paired_n=len(t),**{f:sum(r[f] for r in t) for f in ['rescues','new_misses','added_inactive','removed_inactive','more_fp','fewer_fp','equal_fp','noise_identity_swap','identical_support']}))
  for v in sorted(TRUTH):
   q=[r for r in active_changes if (key=='overall' or r['scale_key']==key) and (s=='total' or r['scenario']==s) and r['variable']==v]
   active_change_summaries.append(dict(scale_key=key,scenario=s,variable=v,paired_n=len(q),rescues=sum(r['rescued'] for r in q),new_misses=sum(r['new_miss'] for r in q)))
 for m in METHODS:
  for v in sorted(TRUTH):
   ids=[i for i in expected if key=='overall' or i.startswith(key+'_')]
   active_totals.append(dict(method_id=m,scale_key=key,variable=v,denominator=len(ids),selected=sum(v in sets[i,m] for i in ids)))
write('paired_support_change_summary.csv',change_summaries);write('paired_active_change_summary.csv',active_change_summaries);write('active_selection_totals.csv',active_totals)
runtime=[]
for family in [METHODS[0],METHODS[1],'Lasso','MCP','ABESS']:
 for key in SCALES+['overall']:
  t=[v for (id,f),v in family_times.items() if f==family and (key=='overall' or id.startswith(key+'_'))];assert len(t)==(3000 if key=='overall' else 600)
  quart=statistics.quantiles(t,n=4,method='inclusive');runtime.append(dict(family=family,scale_key=key,cases=len(t),sum_seconds=sum(t),median_seconds=statistics.median(t),q25=quart[0],q75=quart[2],maximum_seconds=max(t),
   scope='counted once per case; shared whole family pipeline' if family in ('Lasso','MCP','ABESS') else 'whole BB case setup+compile+schedule+islands; before final writing'))
write('runtime_by_family.csv',runtime)
failures=[]
for m in METHODS:
 for status in ('ok','warning','failed','pending'):
  failures.append(dict(method_id=m,status=status,cases=sum(r['method_id']==m and r['execution_status']==status for r in rows),expected=3000,
   diagnostic_text='Benchmark detailed warning/error text unavailable in validated import; retained status counts. Search flag not applicable to penalized selectors.' if m not in METHODS[:2] else 'truth score exceeds discovered HPM is separate from execution failure'))
write('failure_and_warning_status.csv',failures)
for role,r in config['inputs'].items():assert sha(ROOT/r['file'])==r['sha256'],role
output_hashes={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file()}
provenance=dict(status='PASS',job=os.environ['SLURM_JOB_ID'],utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=config,
 expected_case_method_rows=30000,actual_rows=len(rows),all_keys_and_support_metrics_verified=True,output_sha256=output_hashes,
 script_sha256=sha(__file__),python=platform.python_version(),command=__import__('sys').argv,
 original_response_binding='Original import response/component identities assigned through sealed case/base-input pairing reference and prior3000response verification; not independently invented.',
 timing_caveat='Benchmark selector rows share family cost; runtime_by_family deduplicates. BB includes compilation/setup. No isolated selector/kernel timings.',
 limitations=['All five scales reuse600paired datasets; descriptive counts are not independent significance tests.','Approximate HPM and ABESS have no global optimum certificate.','Detailed benchmark warning text not present in validated import; status counts retained and diagnostic extraction extension is separate.'])
(OUT/'comparison_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print('COMPARISON PASS',len(rows),'rows; outputs',OUT)
print((OUT/'recovery_tables.md').read_text())
