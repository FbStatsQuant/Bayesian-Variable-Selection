import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import hashlib,json,platform,datetime,subprocess,shutil
C=Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign');S=C/'code/bench_v2/review/sol_scripts_r2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bad=[];count=0
for line in (S/'DELIVERABLE_SNAPSHOT_SHA256.txt').read_text().splitlines():
    h,rel=line.split('  ',1);count+=1
    if sha(C/rel)!=h:bad.append(rel)
print('UNCHANGED_REVIEWED_DELIVERABLES',count,'bad',bad);assert not bad
for mf,base in [(C/'code/bench_v2/MANIFEST_SHA256.txt',C/'code/bench_v2'),(C/'code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt',C/'code/bench_lowp')]:
    count=0
    for line in mf.read_text().splitlines():
        h,rel=line.split('  ',1);p=base/rel;assert sha(p)==h;count+=1
        dest=S/'source_snapshot'/p.relative_to(C);dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():shutil.copy2(p,dest)
    print('FROZEN_MEMBERS',str(mf),sha(mf),'PASS',count)
env={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'shell':'PowerShell','R':'C:/Program Files/R/R-4.4.1/bin/Rscript.exe --vanilla','numerical_threads':1,'remote_connections':0,'delegation':False}
(S/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2),encoding='utf-8')
for p in sorted(S.glob('*.exit')):assert p.read_text(encoding='utf-8-sig').strip()=='0',str(p)
print('ALL_SEVEN_CHECK_EXITS_ZERO')
