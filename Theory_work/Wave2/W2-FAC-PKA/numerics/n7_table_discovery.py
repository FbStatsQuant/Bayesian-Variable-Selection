"""Exhaustive partition/mask inclusion and transfer check; not a C++ ledger test."""
from n1_exact_grid import *
import itertools

def partitions(seq):
    if not seq:yield [];return
    first=seq[0]
    for rest in partitions(seq[1:]):
        yield [[first]]+[b[:] for b in rest]
        for i in range(len(rest)):
            yield [([first]+b if j==i else b[:]) for j,b in enumerate(rest)]

p=6;n=80;parts=list(partitions(list(range(p))))
count=0;contained=0
for blocks in parts:
    models={tuple(S) for b in blocks for k in range(len(b)+1) for S in itertools.combinations(sorted(b),k)}
    for s in (1,2,3):
        for truth in itertools.combinations(range(p),s):
            hit=any(set(truth)<=set(b) for b in blocks)
            assert (truth in models)==hit
            count+=1;contained+=hit
rng=np.random.default_rng(42)
X=bc.standardize_X(rng.normal(size=(n,p)));theta=np.array([4.,4.,0,0,0,0])
y=bc.standardize_y(X@theta+rng.normal(size=n));P=bc.Problem(X,y)
sets=[S for k in range(p+1) for S in itertools.combinations(range(p),k)]
scores=P.F_many(sets);weights=np.exp(scores-scores.max());mass=weights/weights.sum()
truth=(0,1);prob=float(mass[sets.index(truth)]);assert prob>.5
hits=0
for blocks in parts:
    if not any(set(truth)<=set(b) for b in blocks):continue
    models={tuple(S) for b in blocks for k in range(len(b)+1) for S in itertools.combinations(sorted(b),k)}
    best=max(models,key=P.F)
    assert best==truth;hits+=1
out=dict(partitions=len(parts),subset_inclusion_cases=count,contained_cases=contained,
    inclusion_failures=0,posterior_truth=prob,hpm_controls=hits,hpm_failures=0,
    qualification='mathematical enumeration control; production fidelity is source-reviewed separately')
(HERE/'N7_table_discovery.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out))
