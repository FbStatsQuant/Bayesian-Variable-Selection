"""Transfer one frozen revision and two saved dev records; launch persistent R-1 audit.
No NOTS access. One SSH call. Parent must inspect remote AGENTS/capacity first.
"""
from pathlib import Path
import hashlib,json,shlex,subprocess,sys,tarfile,io
b=Path(__file__).resolve().parents[1]
tag=sys.argv[1]
assert tag.replace("_", "").isalnum()
archive=b/"artifacts"/(tag+".tar.gz")
records=Path(r"C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\A_build\smoke_records")
bundle=b/"artifacts"/(tag+"_audit_upload.tar.gz")
checks=[]
with tarfile.open(bundle,"w:gz") as t:
 t.add(archive,arcname=tag+".tar.gz")
 checks.append((hashlib.sha256(archive.read_bytes()).hexdigest(),tag+".tar.gz"))
 for p in (500,1000):
  paths=list((records/("dev"+str(p))).rglob("SMCBVS.rds"));assert len(paths)==1
  name="r1_audit_inputs/smoke"+str(p)+".rds"
  t.add(paths[0],arcname=name)
  checks.append((hashlib.sha256(paths[0].read_bytes()).hexdigest(),name))
 data="".join(h+"  "+n+"\n" for h,n in checks).encode()
 info=tarfile.TarInfo("r1_upload.sha256");info.size=len(data);t.addfile(info,io.BytesIO(data))
root="/home/fb31/smcbvs_v3_deploy_20261022/A_build"
h=hashlib.sha256(bundle.read_bytes()).hexdigest()
script=f"""set -euo pipefail
cd {root}
test ! -e {tag}
test ! -e runs/{tag}checks01
cat > {tag}_audit_upload.tar.gz
printf '%s  %s\n' {h} {tag}_audit_upload.tar.gz | sha256sum -c -
tar -xzf {tag}_audit_upload.tar.gz
sha256sum -c r1_upload.sha256
tar -xzf {tag}.tar.gz
cd {tag}
sha256sum -c SHA256SUMS > ../r1_source_validation.txt
cd ..
bash {tag}/build/launch.sh {root}/{tag} {tag}checks01 r1checks
bash {tag}/build/launch.sh {root}/{tag} {tag}build build
bash {tag}/build/launch.sh {root}/{tag} {tag}regression tests
"""
with bundle.open("rb") as f:
 r=subprocess.run(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=15","owls","nice -n 19 bash -c "+shlex.quote(script)],stdin=f,capture_output=True)
receipt={"snapshot":tag,"bundle_sha256":h,"members":checks,"returncode":r.returncode,"stdout":r.stdout.decode(),"stderr":r.stderr.decode()}
(b/"evidence"/(tag+"_upload.json")).write_text(json.dumps(receipt,indent=2),encoding="utf-8")
print(json.dumps(receipt,indent=2));sys.exit(r.returncode)
