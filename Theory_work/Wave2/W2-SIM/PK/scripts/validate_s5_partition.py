"""validate_s5_partition.py -- W2-SIM family PK: the closed-form partition s5_exact.s5_partition(p, B) (consecutive groups of 5
packed next-fit into blocks of size <= B) equals the method's partition bvs_core.partition_from_corr(Sigma_S5, B) (complete
linkage on 1-|r| with the union-lexicographic tie rule, cut at B, next-fit packing) on the exact S5 correlation matrix.
usage: python validate_s5_partition.py OUT.jsonl"""
import sys
import json
import time
import pk_common as pc
import bvs_core as bc
import fac_core as fc
from s5_exact import s5_partition

outf = sys.argv[1]
open(outf, "w").close()
ok = 0
cases = [(p, B) for p in (77, 96, 250, 333, 600, 1001, 1500, 2003, 3001) for B in (10, 14, 16)]
for p, B in cases:
    S, _, _ = fc.s5_sigma(p)
    t0 = time.time()
    bl = bc.partition_from_corr(S, B)
    eq = bl == s5_partition(p, B)
    ok += eq
    d = dict(p=p, B=B, equal=eq, n_blocks=len(bl), t=round(time.time() - t0, 1))
    pc.write_jsonl(outf, d)
    print(json.dumps(d), flush=True)
d = dict(summary=True, cases=len(cases), agree=ok, module_sha=pc.module_sha())
pc.write_jsonl(outf, d)
print(json.dumps(d))
if ok != len(cases):
    sys.exit(1)
