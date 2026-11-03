import csv, subprocess, sys
from pathlib import Path
from functools import lru_cache

WORK = Path(__file__).resolve().parent.parent
ROOT = WORK.parents[4]
INPUT = ROOT / '02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs'
TRUTH = INPUT / 'truth_scoring'
RUNS = ROOT / '02_Experiments/H_2026-10-22_smcbvs_v3_deploy/D_analysis/reproduction/runs.tsv'
BENCH = Path(r'C:\Users\felip\Documents\NOTS_BVS\NOTS_projects_ml75\BVS\bench20261019')
SMC = Path(r'C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\claude')
RSCRIPT = r'C:\Program Files\R\R-4.4.1\bin\Rscript.exe'
SPECIAL = {'20261021T1818Z_bench20261019_prodc050_A3_Horseshoe','20261021T1818Z_bench20261019_prodc050_SuSiErefine','20261021T1819Z_bench20261019_prodc100_SuSiErefine'}

def read(path, delim=','):
    with path.open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f, delimiter=delim))
def support(x):
    if x in ('', 'NA', None): return frozenset()
    return frozenset(int(z) for z in x.split(';'))
def ids(p, scenario):
    for s in (range(1,7) if scenario == 'pooled' else [int(scenario)]):
        for r in range(1,101): yield f'p{int(p):04d}_S{s}_r{r:03d}'

subprocess.run([RSCRIPT, str(WORK/'code/truth.R'), str(TRUTH), str(WORK/'code/truth_extracted.csv')], check=True)
extracted = read(WORK/'code/truth_extracted.csv')
truth = {r['dataset_id']:support(r['active']) for r in extracted}
manifest = {r['dataset_id']:support(r['active']) for r in read(TRUTH/'truth_manifest.csv')}
disagreements = sorted(k for k in set(truth)|set(manifest) if truth.get(k)!=manifest.get(k))
if len(truth)!=1200: raise ValueError('unexpected truth count')
runs = {}
for r in read(RUNS, '\t'):
    for method in r['methods'].split(','):
        key=(r['scale_key'],method)
        if key in runs: raise ValueError(f'duplicate run map {key}')
        runs[key]=r['run_id']

@lru_cache(None)
def get_rows(path):
    return read(path) if path.is_file() else []
@lru_cache(None)
def derived(path):
    result={}
    for row in get_rows(path):
        key=(row['case_id'],row['method_id'],row['rule_id'])
        if key in result: raise ValueError(f'duplicate derived row {key}')
        result[key]=row
    return result
def fit(method, rule, scale, dataset):
    case = dataset+'_'+scale
    pdir=dataset.split('_')[0]
    if method=='SMCBVS':
        path=SMC/f'prod_{pdir}_20261023T1227Z'/pdir/case/'SMCBVS.csv'
    else:
        run=runs[(scale,method)]
        if rule.endswith('_K37') or rule in ('ebic1_lam005','sic_smax'):
            base=BENCH/'derived' if scale=='c100' else INPUT/'derived'
            path=base/run/'derived_rules/derived_rule_rows.csv'
            return derived(path).get((case,method,rule)),path
        base=INPUT/'results' if run in SPECIAL else BENCH/'results'
        path=base/run/pdir/case/(method+'.csv')
    rows=[r for r in get_rows(path) if r['rule_id']==rule and r['method_id']==method]
    if len(rows)>1: raise ValueError(f'duplicate row {path} {rule}')
    if rows and rows[0]['dataset_id']!=dataset: raise ValueError(f'dataset mismatch {path}')
    return (rows[0] if rows else None),path
def exact(row, target):
    return bool(row and row['status'] in ('ok','warning') and support(row['support'])==target)

claims=read(WORK/'CLAIMS.csv')
results=[]
problems=[]
for cell in claims:
    n=int(cell['cell_no']); typ=cell['cell_type']; files=set(); missing=failed=0; notes=[]
    if typ=='reconciliation':
        folders=csvs=rds=resource=0
        for p in (500,1000):
            for scale in ('c050','c100'):
                for ds in ids(p,'pooled'):
                    folder=SMC/f'prod_p{p:04d}_20261023T1227Z'/f'p{p:04d}'/(ds+'_'+scale)
                    folders+=folder.is_dir(); rds+=(folder/'SMCBVS.rds').is_file()
                    row,path=fit('SMCBVS','hpm',scale,ds)
                    if path.is_file(): files.add(path); csvs+=1
                    if row and row['v3_status']=='resource_limit': resource+=1
                    if not row: missing+=1
        value=resource if n==43 else folders
        notes.append(f'{folders} case folders; {csvs} CSVs; {rds} RDS files; {missing} missing hpm rows; resource_limit counted once per hpm row')
    else:
        dslist=list(ids(cell['p'],cell['scenario']))
        files.add(TRUTH/'truth_manifest.csv')
        if cell['method_id']!='SMCBVS': files.add(RUNS)
        values=[]
        for ds in dslist:
            files.add(TRUTH/ds.split('_')[0]/(ds+'.rds'))
            if typ=='paired':
                left,right=cell['method_id'].split(' vs ')
                lm,lr=left.split(':'); rm,rr=right.split(':')
                files.add(RUNS)
                a,ap=fit(lm,lr,cell['scale'],ds); b,bp=fit(rm,rr,cell['scale'],ds)
                for path in (ap,bp):
                    if path.is_file(): files.add(path)
                missing+=int(a is None)+int(b is None)
                failed+=int(a is not None and a['status'] not in ('ok','warning'))+int(b is not None and b['status'] not in ('ok','warning'))
                values.append(int(exact(a,truth[ds]) and not exact(b,truth[ds])))
                continue
            row,path=fit(cell['method_id'],cell['rule_id'],cell['scale'],ds)
            if path.is_file(): files.add(path)
            if row is None: missing+=1
            elif row['status'] not in ('ok','warning'): failed+=1
            if typ=='exact_count': values.append(int(exact(row,truth[ds])))
            elif typ=='diag_flag': values.append(int(bool(row and row['diag_flag'].upper()=='TRUE')))
            elif typ=='error_breakdown' and row and row['status'] in ('ok','warning'):
                sel=support(row['support']); fp=len(sel-truth[ds]); fn=len(truth[ds]-sel)
                q=cell['quantity']
                if q.startswith('mean FP'): values.append(fp)
                elif q.startswith('mean FN'): values.append(fn)
                elif q.startswith('fits with all truth'): values.append(int(fn==0 and fp>=1))
                elif q.startswith('fits with a strict subset'): values.append(int(fp==0 and fn>=1))
                else: raise ValueError(q)
        if typ=='error_breakdown' and cell['quantity'].startswith('mean '):
            if not values: raise ValueError(f'no successful fits for cell {n}')
            value=sum(values)/len(values)
            notes.append(f'{len(values)} successful fits')
        else: value=sum(values)
        if missing or failed: notes.append(f'missing rows={missing}; unsuccessful rows={failed}')
        if missing: problems.append(f'cell {n}: {missing} missing fit rows')
    match=abs(value-float(cell['claimed']))<0.0005
    results.append({'cell_no':n,'claimed':cell['claimed'],'recomputed':f'{value:.4f}' if typ=='error_breakdown' and cell['quantity'].startswith('mean ') else str(value),'match':str(match).upper(),'files_used_count':len(files),'notes':'; '.join(notes)})

with (WORK/'TIEOUT_RESULT.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['cell_no','claimed','recomputed','match','files_used_count','notes']); w.writeheader(); w.writerows(results)
mismatches=[r for r in results if r['match']=='FALSE']
command=f'py -3 -I "{WORK / "code/tieout.py"}"'
details=', '.join('{}: {} -> {}'.format(r['cell_no'],r['claimed'],r['recomputed']) for r in mismatches)
lines=['# Independent tie-out', '', f'Cells checked: {len(results)}. Matches: {len(results)-len(mismatches)}. Mismatches: {len(mismatches)} (cells '+', '.join(str(r['cell_no']) for r in mismatches)+').', '', 'Mismatches (claimed -> recomputed): '+details+'.', '', f'Truth: {len(truth)} RDS files independently read by R and compared as sets against manifest; {len(disagreements)} disagreements'+(': '+', '.join(disagreements) if disagreements else '')+'.', '', 'Reconciliation: a bundle is a case folder, whether or not its files are present; resource limits count hpm rows once per case. Presence of CSV and RDS files is recorded in result notes. Paired comparisons treat missing or unsuccessful comparator fits as not exact, as specified.', '', 'Files used count includes distinct existing fit/derived CSV files, truth RDS files and the manifest and run map where applicable; reconciliation counts only existing SMC CSVs. Missing expected fit rows are treated as misses.', '', 'Data problems: '+('; '.join(problems) if problems else 'none identified')+'.', '', 'Reproduce all results (Python invokes the R helper):', '', '```powershell', command, '```', '', f'R subprocess: "{RSCRIPT}" "{WORK / "code/truth.R"}" "{TRUTH}" "{WORK / "code/truth_extracted.csv"}"', '']
(WORK/'TIEOUT_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines[:8]))
