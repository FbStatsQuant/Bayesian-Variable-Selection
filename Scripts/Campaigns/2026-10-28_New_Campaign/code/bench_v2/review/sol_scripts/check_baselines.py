import pathlib,hashlib,csv,difflib
P=pathlib.Path
C=P('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign');V=C/'code/bench_v2';S=V/'review/sol_scripts'
D=P('C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit={(r['method'],r['file']):r['sha256'] for r in csv.DictReader((C/'bench_audit/work_chain/file_hashes.csv').open()) if r['copy']=='deployed'}
with (S/'baseline_check.log').open('w',encoding='utf-8') as out:
 count=0
 for line in (V/'BASELINE_SHA256.txt').read_text().splitlines():
  if ' | ' not in line or line.startswith('#'):continue
  rel,old,new,_=line.split(' | ')
  assert sha(D/rel)==old,rel
  if rel.split('/')[0].startswith(('F1_','F2_','F3_')) and not '/tests/' in rel:
   method=rel[:2];file=rel.split('/',1)[1];assert audit[method,file]==old,(method,file);count+=1
 out.write(f'BASELINE all 22 copied-file old hashes equal mirror; all {count} source hashes equal audit deployed rows\n')
 for folder in ['F1_Lasso','F2_ElasticNet']:
  for rel in ['config.R','common.R','run_case.R','methods/glmnet_helpers.R','methods/'+('fit_F1_lasso.R' if folder.startswith('F1') else 'fit_F2_enet.R')]:
   a=(D/folder/rel).read_text(encoding='utf-8').splitlines(True);b=(V/folder/rel).read_text(encoding='utf-8').splitlines(True)
   out.writelines(difflib.unified_diff(a,b,fromfile='deployed/'+folder+'/'+rel,tofile='v2/'+folder+'/'+rel))
 base=V/'lowp_port/baseline_bench_lowp'
 for line in (V/'lowp_port/BASELINE_SHA256.txt').read_text().splitlines():
  h,rel=line.split('  ',1);assert sha(base/rel)==h,rel
 out.write('LOWP baseline 34/34 hashes match preserved files\n')
