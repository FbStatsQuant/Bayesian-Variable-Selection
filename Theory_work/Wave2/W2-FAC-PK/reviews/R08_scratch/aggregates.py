import json, hashlib
from pathlib import Path
p=Path('Theory_work/Wave2/W2-FAC-PK/numerics')
for line in (p/'FROZEN_SNAPSHOTS.sha256').read_text().splitlines():
    if not line.strip():continue
    digest,name=line.split(); name=name.lstrip('*')
    print(name, 'sha256_matches', hashlib.sha256((p/name).read_bytes()).hexdigest()==digest)
rows=[json.loads(x) for x in (p/'N1_raw.jsonl').read_text().splitlines()]
print('N1',len(rows),'saturated',sum(x['saturated'] for x in rows),'MR1_misses',sum(not x['MR1_scores'] for x in rows),'doubled_discoveries',sum(x['k_hit'] is not None and x['k_hit']<=x['cap_2K'] for x in rows))
rows=[json.loads(x) for x in (p/'N3_raw_final360.jsonl').read_text().splitlines()]
print('N3',len(rows),'endpoint_misses',sum(not x['final_is_S0'] for x in rows),'doubled_discoveries',sum(x['k_hit'] is not None and x['k_hit']<=x['cap_2'] for x in rows),'max_moves_over_K',max(x['moves']/x['K'] for x in rows))
print('N3 move counts',rows[0]['counts'])
