import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import datetime,hashlib,importlib.util,io,json,os,shlex,shutil,subprocess,tarfile
from types import SimpleNamespace
from unittest.mock import patch
C=Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign')
S=C/'code/bench_v2/review/sol_scripts_r2'; P=C/'bench_audit/jobs/BENCH_F3_PROD'; D=P.parent/'BENCH_F3_DEV'
BASH='C:/Program Files/Git/bin/bash.exe'; code=C/'code/bench_v2'
print('START',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
sys.path.insert(0,str(P/'runner'));prepare=load('prepare_r2',P/'prepare.py')
jobs=S/'packaging_pass2';prod=jobs/'BENCH_F3_PROD';dev=jobs/'BENCH_F3_DEV'
shutil.copytree(P/'runner',prod/'runner',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copy2(P/'JOB.md',prod/'JOB.md');(dev/'runner').mkdir(parents=True);shutil.copy2(D/'runner/sizing.py',dev/'runner/sizing.py');shutil.copy2(D/'JOB.md',dev/'JOB.md')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,expected=0):
    env=dict(os.environ,MSYS_NO_PATHCONV='1')
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=90,env=env)
    print('COMMAND',shlex.join(map(str,cmd)),'EXIT',r.returncode,flush=True)
    print(r.stdout,r.stderr,flush=True)
    if expected==0:assert r.returncode==0
    else:assert r.returncode!=0
    return r
uploads=[]
for kind in ['dev','prod']:
    rid='20261030T154800Z_bench_f3v2_'+kind
    with patch.object(prepare,'HERE',prod),patch.object(sys,'argv',['prepare.py',kind,rid,str(code)]): prepare.main()
    upload=jobs/'staging'/rid;uploads.append(upload);digest=sha(upload/'UPLOAD_SHA256.txt')
    before={p.relative_to(upload).as_posix():sha(p) for p in upload.rglob('*') if p.is_file()}
    install=(S/'installed'/kind/'F3_AdaptiveLasso').as_posix()
    text=(P/'runner/stage.sh').read_text()
    lines=text.splitlines();assert lines[6].startswith('[[')
    lines[6]='test "$UPLOAD" = '+shlex.quote(upload.as_posix())
    text='\n'.join(lines)+'\n'
    guard='bash "$UPLOAD/runner/guard_check.sh" 30';assert text.count(guard)==1;text=text.replace(guard,': # local-only path-mapped check; remote disk guard separately unit-tested')
    text=text.replace('python3 ',shlex.quote(Path(sys.executable).as_posix())+' ')
    orig='"$UPLOAD/runner/frozen.py"';assert text.count(orig)==2
    mapped=' '.join(map(shlex.quote,[(S/'mapped_frozen.py').as_posix(),(P/'runner/frozen.py').as_posix(),install]))
    text=text.replace(orig,mapped)
    script=S/('stage_local_'+kind+'.sh');script.write_text(text,encoding='utf-8',newline='\n')
    run([BASH,str(script),upload.as_posix(),digest]);run([BASH,str(script),upload.as_posix(),digest])
    run([sys.executable,'-B',str(P/'runner/upload_check.py'),str(upload),digest])
    after={p.relative_to(upload).as_posix():sha(p) for p in upload.rglob('*') if p.is_file()};assert before==after
    print('REAL_FREEZE_STAGE_REPEAT_IMMUTABLE',kind,'PASS',len(after),'files',flush=True)
    extra=upload/'unexpected_review_file';extra.write_text('extra')
    run([sys.executable,'-B',str(P/'runner/upload_check.py'),str(upload),digest],1);extra.unlink()
    installed=Path(install);extra=installed/'unexpected_review_file';extra.write_text('extra')
    run([BASH,str(script),upload.as_posix(),digest],1);extra.unlink()
    print('EXACT_EXTRA_MEMBERS_REFUSED',kind,'PASS',flush=True)
# Execute actual transfer receiver with a local manifest/tar transport substitute.
# No SSH or scp process is started; receipts are review-local.
pull=load('nots_pull_r2',C/'ops/transfer/nots_pull.py')
upload=uploads[0];files=sorted(p for p in upload.rglob('*') if p.is_file())
manifest=(''.join(sha(p)+'  ./'+p.relative_to(upload).as_posix()+'\n' for p in files)+f'#TOTAL files={len(files)} bytes={sum(p.stat().st_size for p in files)}\n').encode()
(S/'transfer_manifest_source.txt').write_bytes(manifest)
buffer=io.BytesIO()
with tarfile.open(fileobj=buffer,mode='w') as tf:
    for p in files:tf.add(p,arcname='./'+p.relative_to(upload).as_posix(),recursive=False)
blob=buffer.getvalue();(S/'transfer_source.tar').write_bytes(blob)
def fake_transport(cmd,stdout=None,timeout=None):
    assert cmd[0]=='ssh'
    if ' manifest ' in cmd[-1]: return SimpleNamespace(returncode=0,stdout=manifest,stderr=b'')
    if ' tar ' in cmd[-1]: stdout.write(blob);return SimpleNamespace(returncode=0,stdout=None,stderr=b'')
    raise AssertionError('unexpected transport: '+str(cmd))
receipts=S/'transfer_receipts';download=S/'downloaded_upload'
with patch.object(pull,'run',side_effect=fake_transport),patch.object(pull,'RECEIPTS',str(receipts)),patch.object(pull,'OPS_LOG',str(S/'MOCK_OPS_LOG.md')),patch.object(sys,'argv',['nots_pull.py','/scratch/fb31/New_Campaign/upload/'+upload.name,'--local',str(download)]):pull.main()
reports=list(receipts.glob('*.verify.json'));assert len(reports)==1
receipt=json.loads(reports[0].read_text());assert receipt['verdict']=='VERIFIED' and receipt['manifest_sha256']==hashlib.sha256(manifest).hexdigest()
run([sys.executable,'-B',str(P/'runner/upload_check.py'),str(download),sha(upload/'UPLOAD_SHA256.txt')])
print('MOCK_TRANSPORT_ACTUAL_RECEIVER_UPLOAD_MANIFEST_ROUNDTRIP PASS',len(files),flush=True)
# A result-folder archival manifest also survives a copy and detects changed membership.
result=S/'manifest_result';result.mkdir();real=code/'tests/runner_output/results/v2_local_e2e/p0500/dev_p0500_S1_r001_c100'
for p in real.iterdir():
    if p.is_file():shutil.copy2(p,result/p.name)
run([sys.executable,'-B',str(P/'runner/manifests.py'),str(result)])
download_result=S/'downloaded_result';shutil.copytree(result,download_result)
run([sys.executable,'-B',str(P/'runner/manifests.py'),str(download_result),'--verify'])
(download_result/'extra').write_text('extra')
run([sys.executable,'-B',str(P/'runner/manifests.py'),str(download_result),'--verify'],1)
print('RESULT_MANIFEST_COPY_VERIFY_AND_EXTRA_REFUSAL PASS',flush=True)
print('END',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
