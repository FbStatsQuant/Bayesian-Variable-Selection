import pathlib,subprocess,json,hashlib
r=pathlib.Path('theory_campaign/A-REV8/sources'); m=json.loads((r/'manifest.json').read_text())
for branch,files in {'W1-EXP':['PROOF.md'],'O-LS0':['results/paired_totals.txt','results/data_hash_check.csv']}.items():
 ref='origin/theory/'+branch
 for f in files:
  p='theory_campaign/'+branch+'/'+f;b=subprocess.check_output(['git','show',ref+':'+p]);(r/(branch+'__'+f.replace('/','__'))).write_bytes(b);m.append(dict(ref=ref,head=subprocess.check_output(['git','rev-parse',ref],text=True).strip(),path=p,sha256=hashlib.sha256(b).hexdigest()))
for p in ['Scripts/SMC_BVS/core/cpp/v3_score.h','Scripts/SMC_BVS/core/cpp/v3_ledger.h','Scripts/SMC_BVS/core/cpp/v3_runtime.h','Scripts/SMC_BVS/core/cpp/v3_core.cpp']:
 b=pathlib.Path(p).read_bytes();(r/pathlib.Path(p).name).write_bytes(b);m.append(dict(path=p,sha256=hashlib.sha256(b).hexdigest()))
(r/'manifest.json').write_text(json.dumps(m,indent=2))
