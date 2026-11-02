import subprocess,pathlib,hashlib,json
root=pathlib.Path('theory_campaign/A-REV8/sources'); rows=[]
items={'W8-SYNTH':['SYNTHESIS.md'],'W4-T38FULL':['T38_PROOF.md','T38_STATEMENT.md'],'W6-FIXREV1':['T38_PROOF.md','T38_STATEMENT.md','CONSOLIDATED.md'],'W5-VMASK':['REPORT.md','REPAIRS.md'],'W5-VPGD':['REPAIRS.md'],'W3-PXN':['PROOF.md','REPORT.md'],'A-REV1':['REVIEW.md'],'A-REV3':['REVIEW.md'],'O-LS0':['REPORT.md']}
for branch,files in items.items():
 ref='origin/theory/'+branch; sha=subprocess.check_output(['git','rev-parse',ref],text=True).strip()
 for f in files:
  path='theory_campaign/'+branch+'/'+f
  r=subprocess.run(['git','show',ref+':'+path],capture_output=True)
  if r.returncode: continue
  out=root/(branch+'__'+f); out.write_bytes(r.stdout); rows.append(dict(ref=ref,head=sha,path=path,sha256=hashlib.sha256(r.stdout).hexdigest()))
for f in ['Docs/Methodology/METHODOLOGY_v3.md','Docs/Theory/theorems/00_COMMON.md','Docs/Theory/proofs/LOCKED_PROOFS.md','Scripts/SMC_BVS/core/cpp/v3_engine.h']:
 b=pathlib.Path(f).read_bytes(); (root/pathlib.Path(f).name).write_bytes(b); rows.append(dict(path=f,sha256=hashlib.sha256(b).hexdigest()))
(root/'manifest.json').write_text(json.dumps(rows,indent=2))
