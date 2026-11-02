from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
C=Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign')
S=C/'code/bench_v2/review/sol_scripts_r3'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lines=['FINAL UTC '+datetime.datetime.now(datetime.timezone.utc).isoformat()]
for filename,base in [('DELIVERABLE_SNAPSHOT_SHA256.txt',C),('RETAINED_CORRUPTIONS_SHA256.txt',None)]:
 count=0
 for line in (S/filename).read_text(encoding='utf-8').splitlines():
  h,rel=line.split('  ',1);p=base/rel if base else Path(rel)
  assert sha(p)==h,str(p);count+=1
 lines.append(f'UNCHANGED {filename} {count}/{count}')
for stem in ['check_narrow','check_python_integrity']:
 assert (S/(stem+'.exit')).read_text(encoding='utf-8-sig').strip()=='0'
 lines.append(f'EXIT {stem} 0')
study=Path('C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev')
inputs=[study/'inputs/p0500/dev_p0500_S1_r001.rds',study/'manifests/dev_inputs_manifest.csv',C/'code/bench_v2/tests/runner_output/results/v2_local_e2e/p0500/dev_p0500_S1_r001_c100/F3.rds']
(S/'INPUT_SHA256.txt').write_text(''.join(f'{sha(p)}  {p.as_posix()}\n' for p in inputs),encoding='utf-8')
report=C/'code/bench_v2/review/SOL_NARROW_CHECK_R2.md'
lines.append(f'REPORT_SHA256 {sha(report)}')
(S/'FINAL_AUDIT.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
paths=sorted(p for p in S.rglob('*') if p.is_file() and p.name!='REVIEW_EVIDENCE_SHA256.txt')
(S/'REVIEW_EVIDENCE_SHA256.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(S).as_posix()}\n' for p in paths),encoding='utf-8')
print('\n'.join(lines));print('SEALED_EVIDENCE_FILES',len(paths))
