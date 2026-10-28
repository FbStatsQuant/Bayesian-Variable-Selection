"""Exercise the exact NOTS EXIT function locally on Owls; no NOTS/modules/Slurm."""
from pathlib import Path
import hashlib,json,shlex,shutil,subprocess,sys
base=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
assert not out.exists();out.mkdir(parents=True)
text=(base/"build/nots_job.sh").read_text()
body=text[text.index("finish() {"):text.index("trap finish EXIT")]
reports=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for mode in ("success","job_failure","source_failure","hash_failure"):
 root=out/mode;root.mkdir();snap=root/"snapshot";snap.mkdir();run=root/"run";run.mkdir();receipt=root/"receipt";receipt.mkdir()
 (snap/"file.txt").write_text("frozen\n");(snap/"manifest.json").write_text('{}\n')
 (snap/"SHA256SUMS").write_text(''.join(sha(snap/n)+'  '+n+'\n' for n in ('file.txt','manifest.json')))
 config=dict(manifest_sha256=sha(snap/'manifest.json'),inventory_sha256=sha(snap/'SHA256SUMS'))
 (run/'launch.json').write_text(json.dumps(config));shutil.copytree(snap,run/'work')
 (run/'VALIDATION_PASS.json').write_text('{}')
 if mode=='source_failure': (run/'work/file.txt').write_text('corrupt')
 if mode=='hash_failure': (run/'output_sha256.json').mkdir()
 script='set -euo pipefail\n'+''.join(k+'='+shlex.quote(str(v))+'\n' for k,v in dict(SNAPSHOT=snap,OUT=run,RECEIPT=receipt).items())+body+'trap finish EXIT\nexit '+('7' if mode=='job_failure' else '0')+'\n'
 r=subprocess.run(['bash','-c',script],capture_output=True)
 expected=0 if mode=='success' else (7 if mode=='job_failure' else 1)
 assert r.returncode==expected,(mode,r.returncode,r.stderr)
 assert (run/'VALIDATION_PASS.json').exists()==(mode=='success'),mode
 assert (run/'exit_status.txt').read_text().strip()==str(expected)
 assert (receipt/'job_exit_status.txt').read_text().strip()==str(expected)
 reports.append(dict(mode=mode,status='PASS',exit_status=r.returncode,marker_retained=mode=='success'))
(out/'summary.json').write_text(json.dumps(dict(status='PASS',checks=reports,source_sha256=sha(base/'build/nots_job.sh')),indent=2))
print('NOTS_EXIT_TRAP_PASS',len(reports))
