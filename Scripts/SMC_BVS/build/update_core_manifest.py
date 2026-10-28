"""Refresh live v2 source identity only; immutable snapshots are never touched."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
b=Path(__file__).resolve().parents[1]; core=b/'code/core'; p=core/'source_manifest.json'
m=json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=sorted(p for p in core.rglob('*') if p.is_file() and (p.suffix in {'.R','.cpp','.h'} or p.name=='Makevars.v3') and '.cpp_cache' not in p.parts)
m['created_utc']=datetime.now(timezone.utc).isoformat()
m['production_source']={p.relative_to(core).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in files}
m['production_tree_sha256']=hashlib.sha256(''.join(n+' '+r['sha256']+'\n' for n,r in m['production_source'].items()).encode()).hexdigest()
m['byte_identical_to_prototype']=[n for n,r in m['production_source'].items() if m['prototype_source_sha256'].get(n)==r['sha256']]
m['documentation']={'README.md':dict(sha256=sha(core/'README.md'),bytes=(core/'README.md').stat().st_size)}
m['revision']='v2 R-5 repairs of rejected v1'
m['lead_rulings_sha256']=sha(b.parent/'RULINGS_LEAD.md')
m['static_checks']=['Source hashes refreshed from live v2; actual execution evidence is in HANDOFF_v2.md and per-job records.']
m['numerical_validation']='Pending frozen v2 execution; no pass inferred from source hash or historical v1.'
m['execution_authority']='BRIEF Amendments1/2, RULINGS_LEAD R3/R4/R5; Owls capped development; NOTS separately gated.'
p.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(core_source_files=len(files),production_tree_sha256=m['production_tree_sha256'],manifest_sha256=sha(p))))
