import sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import datetime, hashlib, json, os, platform, shutil, subprocess, tempfile, unittest
from unittest.mock import patch
C = Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign')
S = C/'code/bench_v2/review/sol_scripts_r3'
J = C/'bench_audit/jobs'; P = J/'BENCH_F3_PROD'; D = J/'BENCH_F3_DEV'
T = S/'tmp'; T.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
print('START UTC',datetime.datetime.now(datetime.timezone.utc).isoformat(), 'PID',os.getpid(), flush=True)
checks = [
 ('HIGH',C/'code/bench_v2',C/'code/bench_v2/MANIFEST_SHA256.txt',23,'8905f52e314f706b54f985994d7915052301c9e22912690264b7b27ab58b0373'),
 ('LOW_R2',C/'code/bench_lowp',C/'code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt',34,'85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7'),
 ('DEV_FINAL',D,D/'BUNDLE_SHA256SUMS_FINAL',28,None),
 ('PROD_FINAL',P,P/'BUNDLE_SHA256SUMS_FINAL',65,None)]
snapshot_paths = set()
for label,base,mf,num,digest in checks:
 entries=[]
 for line in mf.read_text(encoding='utf-8-sig').splitlines():
  h,rel=line.split('  ',1); f=base/rel; entries.append((rel,sha(f)==h)); snapshot_paths.add(f)
 assert len(entries)==num and len({n for n,_ in entries})==num and all(ok for _,ok in entries)
 if digest: assert sha(mf)==digest
 if label=='DEV_FINAL': assert sha(mf).startswith('d5da3b0d') and sha(mf).endswith('c4d4')
 if label=='PROD_FINAL': assert sha(mf).startswith('9129e5df') and sha(mf).endswith('4827')
 snapshot_paths.add(mf)
 print(label,'SHA256',sha(mf),'PASS',len(entries),'/',num,flush=True)
# Keep exact source/configuration snapshots and before/after hashes. Review-local
# snapshots are the only writes; all original retained corruptions are read-only.
for base in (P,D):
 snapshot_paths.update(p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
snapshot_paths.add(J/'REVIEW2_FIXES.md')
for p in sorted(snapshot_paths):
 dest=S/'source_snapshot'/p.relative_to(C); dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
before={p:sha(p) for p in snapshot_paths}
(S/'DELIVERABLE_SNAPSHOT_SHA256.txt').write_text(''.join(f'{h}  {p.relative_to(C).as_posix()}\n' for p,h in sorted(before.items())),encoding='utf-8')
old=C/'code/bench_v2/review/sol_scripts_r2/corruptions'
retained={p:sha(p) for p in old.rglob('*') if p.is_file()}
(S/'RETAINED_CORRUPTIONS_SHA256.txt').write_text(''.join(f'{h}  {p.as_posix()}\n' for p,h in sorted(retained.items())),encoding='utf-8')
cmd=[sys.executable,'-B',str(P/'runner/frozen.py'),'check',str(C/'code/bench_v2/F3_AdaptiveLasso'),str(C/'code/bench_v2/MANIFEST_SHA256.txt'),str(P/'runner/freeze.json')]
print('LAUNCH',json.dumps(cmd),flush=True)
proc=subprocess.run(cmd,text=True,capture_output=True)
print(proc.stdout,proc.stderr,'EXIT',proc.returncode,flush=True)
assert proc.returncode==0 and 'FROZEN_OK' in proc.stdout
sentence='A zero-runtime whole-fit failure is refused with `runtime_s not one positive value per fit`; OPS retains or quarantines its four files and logs, records the refusal and escalates it under the failed-unit policy, never counting it as accepted or silently omitting it.'
for base in (D,P):
 text=(base/'JOB.md').read_text(encoding='utf-8')
 assert sentence in text
 print('JOB_SENTENCE',base.name,'line',text.splitlines().index(sentence)+1,'PASS',flush=True)
orig_td=tempfile.TemporaryDirectory
def scoped_tmp(*a,**kw):
 kw['dir']=str(T)
 return orig_td(*a,**kw)
# Tests' explicit bundle-local temp paths are redirected without changing source.
# Suites execute sequentially, with at most one child process at any instant.
with patch.object(tempfile,'TemporaryDirectory',side_effect=scoped_tmp):
 for base,wanted in [(P,19),(D,2)]:
  suite=unittest.defaultTestLoader.discover(str(base/'tests'),pattern='test_*.py',top_level_dir=str(base/'tests'))
  result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(suite)
  print('SUITE',base.name,'RUN',result.testsRun,'EXPECTED',wanted,'SUCCESS',result.wasSuccessful(),flush=True)
  assert result.wasSuccessful() and result.testsRun==wanted
  unittest.defaultTestLoader._top_level_dir=None
changed=[str(p) for p,h in before.items() if sha(p)!=h]
assert not changed,changed
assert all(sha(p)==h for p,h in retained.items())
print('UNCHANGED_DELIVERABLES',len(before),'UNCHANGED_RETAINED_CORRUPTION_FILES',len(retained),flush=True)
env={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'pid':os.getpid(),'R':'C:/Program Files/R/R-4.4.1/bin/Rscript.exe --vanilla','threads':{k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},'remote_connections':0,'fits':0,'workload_process_limit':2,'delegation':False,'frozen_command':cmd}
(S/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2),encoding='utf-8')
print('END UTC',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
