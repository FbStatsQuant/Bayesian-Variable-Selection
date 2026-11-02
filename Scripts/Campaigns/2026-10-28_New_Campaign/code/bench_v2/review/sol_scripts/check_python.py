import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import hashlib, json, pathlib, importlib.util, tempfile, unittest, contextlib, shutil, csv, subprocess, io
from unittest.mock import patch
P=pathlib.Path
C=P('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign')
V=C/'code/bench_v2'; S=V/'review/sol_scripts'; J=C/'bench_audit/jobs'; R=J/'BENCH_F3_PROD/runner'
sys.path.insert(0,str(R))
import frozen, units
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check_manifest(m,root):
    rows=[line.split('  ',1) for line in m.read_text(encoding='utf-8-sig').splitlines()]
    bad=[rel for h,rel in rows if sha(root/rel.removeprefix('./'))!=h]
    print('MANIFEST',m.relative_to(C),sha(m),'entries',len(rows),'mismatch',bad)
    return rows
with (S/'check_python.log').open('w',encoding='utf-8') as logfile,contextlib.redirect_stdout(logfile),contextlib.redirect_stderr(logfile):
    print('Frozen:',frozen.check(V/'F3_AdaptiveLasso',V/'MANIFEST_SHA256.txt',R/'freeze.json'))
    high=check_manifest(V/'MANIFEST_SHA256.txt',V)
    low=check_manifest(V/'lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt',C/'code/bench_lowp')
    for name in ['BENCH_F3_DEV','BENCH_F3_PROD']:
        check_manifest(J/name/'BUNDLE_SHA256SUMS',J/name)
    snap=V/'repro/snapshot_2a8362b2f348'
    files=[f for f in snap.rglob('*') if f.is_file()]
    print('snapshot',len(files),'differences',[str(f.relative_to(snap)) for f in files if (V/f.relative_to(snap)).is_file() and sha(f)!=sha(V/f.relative_to(snap))])
    for tag,folder,fit in [('F1','F1_Lasso','fit_F1_lasso.R'),('F2','F2_ElasticNet','fit_F2_enet.R'),('F3','F3_AdaptiveLasso','fit_F3_alasso.R')]:
        for a,b in [(V/folder/'methods'/fit,C/'code/bench_lowp/R/methods'/fit),(V/folder/'common.R',C/f'code/bench_lowp/R/production_helpers/common_{tag}.R'),(V/folder/'methods/glmnet_helpers.R',C/f'code/bench_lowp/R/methods/glmnet_helpers_{tag}.R')]:
            assert sha(a)==sha(b),(a,b)
    print('lowp copies 9/9 identical')
    manifest=P('C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/manifests/inputs_manifest.csv')
    ids={r['dataset_id'] for r in csv.DictReader(manifest.open(encoding='utf-8-sig'))}
    prod=units.units('prod'); dev=units.units('dev')
    assert len(prod)==2400 and len({(r[5],r[4]) for r in prod})==2400
    assert {r[5] for r in prod}==ids
    print('production mapping 2400 unique; 1200 dataset ids equal frozen manifest; dev units',len(dev))
    # Original tests may request temporary directories beside their own files; redirect
    # all of these temporary writes to the review directory without editing tests.
    original=tempfile.TemporaryDirectory
    def temp(*args,**kwargs):
        kwargs['dir']=str(S/'tmp'); return original(*args,**kwargs)
    with patch.object(tempfile,'TemporaryDirectory',side_effect=temp):
        suite=unittest.TestLoader().discover(str(J/'BENCH_F3_PROD/tests'),pattern='test_*.py')
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        assert result.wasSuccessful()
        suite=unittest.TestLoader().discover(str(J/'BENCH_F3_DEV/tests'),pattern='test_*.py',top_level_dir=str(J/'BENCH_F3_DEV/tests'))
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        assert result.wasSuccessful()
    # Exercise real frozen packaging, but redirect the output staging hierarchy here.
    spec=importlib.util.spec_from_file_location('real_prepare',J/'BENCH_F3_PROD/prepare.py')
    prepare=importlib.util.module_from_spec(spec); spec.loader.exec_module(prepare)
    testroot=S/'packaging'; testroot.mkdir(exist_ok=True)
    prodroot=testroot/'BENCH_F3_PROD'; prodroot.mkdir(exist_ok=True)
    shutil.copytree(R,prodroot/'runner',dirs_exist_ok=True)
    shutil.copy2(J/'BENCH_F3_PROD/JOB.md',prodroot/'JOB.md')
    (testroot/'BENCH_F3_DEV/runner').mkdir(parents=True,exist_ok=True)
    shutil.copy2(J/'BENCH_F3_DEV/runner/sizing.py',testroot/'BENCH_F3_DEV/runner/sizing.py')
    run='20261030T235959Z_bench_f3v2_prod'
    with patch.object(prepare,'HERE',prodroot),patch.object(sys,'argv',['prepare.py','prod',run,str(V)]): prepare.main()
    target=testroot/'staging'/run
    out=subprocess.run([sys.executable,'-B',str(R/'upload_check.py'),str(target),sha(target/'UPLOAD_SHA256.txt')],capture_output=True,text=True)
    print('REAL_FROZEN_PACKAGE',out.returncode,out.stdout,out.stderr)
    assert out.returncode==0
    # Reproduce the stage-time addition without running any remote shell code.
    shutil.copy2(target/'MANIFEST_SHA256.txt',target/'runner/MANIFEST_SHA256.txt')
    out=subprocess.run([sys.executable,'-B',str(R/'upload_check.py'),str(target),sha(target/'UPLOAD_SHA256.txt')],capture_output=True,text=True)
    print('POST_STAGE_UPLOAD_CHECK',out.returncode,out.stdout,out.stderr)
    out=subprocess.run([sys.executable,'-B',str(R/'manifests.py'),str(target),'--verify'],capture_output=True,text=True)
    print('DOCUMENTED_UPLOAD_FOLDER_VERIFY',out.returncode,out.stdout,out.stderr)
    print('DONE')
