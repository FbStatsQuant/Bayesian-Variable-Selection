import sys
sys.dont_write_bytecode = True
from pathlib import Path
from itertools import combinations
import random

NUM = Path(__file__).resolve().parents[2] / 'numerics'
sys.path.insert(0, str(NUM))
from n3lib import Inst, all_sets, prescribed, dfs_key, predict, run_tables

rng = random.Random(303)
instances = [
    Inst(2, 0, [[1], [0]], [7], [{0:0}, {0:0}], iid='K0'),
    Inst(2, 1, [[0], [1]], [-10,0], [{0:0,1:1}, {0:0,1:2}], iid='old_A_cex'),
    Inst(2, 1, [[1], [0]], [-10,0], [{0:0,1:1}, {0:0,1:1}], iid='reverse_blocks'),
    Inst(4, 2, [[0,1,2,3]], [-10,-10,0], [{c:0 for c in range(16)}], iid='code_vs_lex'),
]
for i in range(150):
    p = rng.randint(1,7)
    K = rng.randint(0,p)
    groups = [[] for _ in range(rng.randint(1,p))]
    for x in range(p):
        rng.choice(groups).append(x)
    blocks = [g for g in groups if g]
    rng.shuffle(blocks)
    rho = [{c:(rng.randint(-2,2) if c else 0) for c in range(1 << len(b))} for b in blocks]
    instances.append(Inst(p,K,blocks,[rng.randint(-2,2) for _ in range(K+1)],rho,iid=f'random{i}'))

checks = 0
jobs = []
for I in instances:
    J = len(I.blocks)
    # Define M by brute-force prefix subsets, independently of the DP recurrence.
    M = []
    for b in range(J+1):
        prefix = sorted(x for C in I.blocks[:b] for x in C)
        row = [None]*(I.K+1)
        for k in range(min(len(prefix),I.K)+1):
            row[k] = max(sum(I.rho[c][code] for c,code in enumerate(I.parts(S)[:b])) for S in combinations(prefix,k))
        M.append(row)
    mu = [{j:max(v for code,v in I.rho[b].items() if code.bit_count()==j) for j in range(min(len(C),I.K)+1)} for b,C in enumerate(I.blocks)]
    _,ks,A,_ = prescribed(I)
    aset = {tuple(S) for S in A}
    for S in all_sets(I):
        codes = I.parts(S)
        tight = len(S)==ks
        if tight:
            for b in range(J+1):
                r = sum(c.bit_count() for c in codes[:b])
                P = sum(I.rho[c][code] for c,code in enumerate(codes[:b]))
                tight = tight and P == M[b][r]
            tight = tight and all(I.rho[b][code]==mu[b][code.bit_count()] for b,code in enumerate(codes))
        assert tight == (tuple(S) in aset), (I.iid,S)
        checks += 1
    for cap in sorted({1,max(1,len(A)-1),len(A),len(A)+1}):
        jobs.append(Inst(I.p,I.K,I.blocks,I.lam,I.rho,cap,f'{I.iid}_cap{cap}'))

results = run_tables(jobs)
for I,R in zip(jobs,results):
    P = predict(I)
    for field in ('lg0','S','ties','truncated'):
        assert R[field] == P[field], (I.iid,field,R,P)
    if not I.iid.startswith('random'):
        print(I.iid, 'N=',P['nA'], 'S=',R['S'], 'ties=',R['ties'], 'truncated=',R['truncated'])
print('L5(A) both-direction checks:', checks, '; instances:',len(instances), '; failures: 0')
print('Frozen existing harness output/count/flag/value checks:',len(jobs),'; failures: 0')
print('Full visiting order was checked by proof, not observed by this harness.')
