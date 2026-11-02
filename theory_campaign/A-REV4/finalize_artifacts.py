import pathlib,json,hashlib
r=pathlib.Path('theory_campaign/A-REV4')
paths=['Scripts/SMC_BVS/core/cpp/v3_engine.h','Scripts/SMC_BVS/core/v3_fit.R','Scripts/SMC_BVS/core/v3_calib.R']
paths += [str(p) for p in pathlib.Path('Docs/Theory/proofs').glob('*/STATEMENT.md') if p.parent.name.startswith(('T09_','T12_','T14_','T15_','T22_','T22iii_','T23_','T03_','T01_'))]
records={}
for name in paths:
 p=pathlib.Path(name); data=p.read_bytes(); target=r/'snapshots'/(p.parent.name+'_'+p.name);target.write_bytes(data);records[name]=hashlib.sha256(data).hexdigest()
(r/'ADDITIONAL_SOURCE_HASHES.json').write_text(json.dumps(records,indent=2))
# Verify saved rerun aggregates reproduce the initial run (timestamps differ).
a=json.loads((r/'results/nm_results.txt').read_text());b=json.loads((r/'results/nm_raw_summary.txt').read_text());assert a['NM']==b['NM']
# This is artifact integrity checking, not rerunning numerical experiments.
(r/'ARTIFACT_HASHES.json').write_text(json.dumps({str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob('*') if p.is_file() and p.name!='ARTIFACT_HASHES.json'},indent=2))
