import subprocess,pathlib,hashlib,json
root=pathlib.Path('theory_campaign/A-REV4'); refs={}
for branch, files in {'W2-T26':['PROOF.md','REPORT.md'],'W2-BOOK':['PROOF.md','REPORT.md','NOTES.md'],'F-DRAFT':['NEW_TARGETS.md'],'A-DRAFT':['REPORT.md']}.items():
 ref='origin/theory/'+branch; refs[ref]=subprocess.check_output(['git','rev-parse',ref],text=True).strip()
 for f in files:
  data=subprocess.check_output(['git','show',ref+':theory_campaign/'+branch+'/'+f]); (root/'snapshots'/f'{branch}_{f}').write_bytes(data)
paths=['Docs/Methodology/METHODOLOGY_v3.md','Docs/Theory/theorems/00_COMMON.md','Docs/Theory/proofs/LOCKED_PROOFS.md','Docs/Theory/proofs/COLLECTED_PROOFS_v2.tex','Scripts/SMC_BVS/core/cpp/v3_runtime.h','Scripts/SMC_BVS/core/cpp/v3_core.cpp']
for p in paths:
 data=pathlib.Path(p).read_bytes(); (root/'snapshots'/pathlib.Path(p).name).write_bytes(data)
(root/'SOURCE_MANIFEST.json').write_text(json.dumps({'refs':refs,'base':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'snapshots').iterdir()}},indent=2))
