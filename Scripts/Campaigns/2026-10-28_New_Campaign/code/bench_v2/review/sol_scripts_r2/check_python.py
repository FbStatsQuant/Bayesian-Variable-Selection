import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import datetime, hashlib, importlib.util, io, json, shutil, subprocess, tempfile, unittest
from unittest.mock import patch
C=Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign')
S=C/'code/bench_v2/review/sol_scripts_r2'
J=C/'bench_audit/jobs'; P=J/'BENCH_F3_PROD'; D=J/'BENCH_F3_DEV'
T=S/'tmp'; T.mkdir(exist_ok=True)
print('START',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
snapshot=S/'source_snapshot';snapshot.mkdir(exist_ok=True)
paths=list(P.rglob('*'))+list(D.rglob('*'))
paths += [C/'code/bench_v2'/n for n in ['MANIFEST_SHA256.txt','CHANGES_v2.md','CONSUMERS.md','PROGRESS.md','tests/TEST_REPORT.md','tests/run_all_tests.R','tests/review1_suite.log','tests/review1_suite.stderr.log','tests/review1_suite.script_exit']]
paths += [C/'code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt',J/'REVIEW1_FIXES.md',J/'TESTS.md',C/'code/bench_v2/review/REVIEW1_FIXES_W1.md']
lines=[]
for p in paths:
    if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
        rel=p.relative_to(C); dest=snapshot/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
        lines.append(f'{sha(p)}  {rel.as_posix()}\n')
(S/'DELIVERABLE_SNAPSHOT_SHA256.txt').write_text(''.join(sorted(set(lines))),encoding='utf-8')
for label,base,mf in [('HIGH',C/'code/bench_v2',C/'code/bench_v2/MANIFEST_SHA256.txt'),('LOW',C/'code/bench_lowp',C/'code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt'),('PROD_FINAL',P,P/'BUNDLE_SHA256SUMS_FINAL'),('DEV_FINAL',D,D/'BUNDLE_SHA256SUMS_FINAL')]:
    entries=[]
    for line in mf.read_text(encoding='utf-8-sig').splitlines():
        h,rel=line.split('  ',1); entries.append((rel,sha(base/rel)==h))
    print(label,'manifest',sha(mf),'entries',len(entries),'valid',sum(ok for _,ok in entries),'bad',[n for n,ok in entries if not ok],flush=True)
    assert all(ok for _,ok in entries)
orig_td=tempfile.TemporaryDirectory
def scoped_tmp(*a,**kw):
    kw['dir']=str(T)
    return orig_td(*a,**kw)
with patch.object(tempfile,'TemporaryDirectory',side_effect=scoped_tmp):
    for base in [P,D]:
        suite=unittest.defaultTestLoader.discover(str(base/'tests'),pattern='test_*.py',top_level_dir=str(base/'tests'))
        result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(suite)
        assert result.wasSuccessful()
        unittest.defaultTestLoader._top_level_dir=None
print('END',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
