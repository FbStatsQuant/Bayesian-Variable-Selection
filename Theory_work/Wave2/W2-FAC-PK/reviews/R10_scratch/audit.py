"""Independent R10 checks; writes only this scratch directory; run with -B."""
from pathlib import Path
import ast
import hashlib
import itertools
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
PK = ROOT / 'Theory_work/Wave2/W2-FAC-PK'
OUT = Path(__file__).resolve().parent
log = []
def record(s):
    log.append(s)
    print(s, flush=True)

protected = [PK / x for x in ['STATEMENT.md', 'REPORT.md', 'METHOD_REQUIREMENTS.md']]
protected += sorted((PK / 'lemmas').glob('*.md'))
protected += [ROOT / ('Scripts/SMC_BVS/core/' + x) for x in
              ['v3_fit.R', 'v3_run.R', 'cpp/v3_core.cpp', 'cpp/v3_engine.h']]
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
(OUT / 'protected_hashes.json').write_text(json.dumps(before, indent=2), encoding='utf-8')

# Read only the literal citation registry; do not execute its output-writing code.
registry = ast.parse((PK / 'reviews/citecheck.py').read_text(encoding='utf-8'))
entries = next(ast.literal_eval(node.value) for node in registry.body
               if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'C' for t in node.targets))
misses = []
for path, rng, sub, where in entries:
    lines = (ROOT / path).read_text(encoding='utf-8', errors='replace').split('\n')
    seg = lines[rng[0]-1:rng[1]] if rng else lines
    ok = sub in '\n'.join(seg) if sub else bool(seg) and (not rng or len(lines) >= rng[1])
    if not ok:
        misses.append((path, rng, where))
record(f'Citation registry: {len(entries)} checked, {len(misses)} misses; {misses}')
assert not misses

for line in (PK / 'numerics/FROZEN_SNAPSHOTS.sha256').read_text().splitlines():
    expected, name = line.split()
    p = PK / 'numerics' / name.lstrip('*')
    assert hashlib.sha256(p.read_bytes()).hexdigest() == expected
    record(f'Frozen SHA256 matches: {p.name}')
for name in ['N1_raw.jsonl', 'N3_raw_final360.jsonl']:
    rows = [json.loads(x) for x in (PK / 'numerics' / name).read_text().splitlines() if x.strip()]
    if name.startswith('N1'):
        result = dict(rows=len(rows), saturated=sum(r['start'] == r['K'] for r in rows),
                      MR1_misses=sum(not r['MR1_scores'] for r in rows),
                      doubled_misses=sum(r['k_hit'] > r['cap_2K'] for r in rows))
    else:
        result = dict(rows=len(rows), nontruth_endpoints=sum(not r['final_is_S0'] for r in rows),
                      doubled_misses=sum(r['k_hit'] is None or r['k_hit'] > r['cap_2'] for r in rows),
                      swaps_after_first_deletion=sum(r['swaps_after_first_del'] for r in rows))
    record(f'{name}: {result}')

rng = np.random.default_rng(20261109)
max_error = 0.0
comparisons = 0
prefix_checks = 0
generic_checks = 0

def neighbours(T, p, K):
    Ts = set(T)
    for j in range(p):
        if j in Ts:
            yield tuple(i for i in T if i != j), ('del', j)
        elif len(T) < K:
            yield tuple(sorted((*T, j))), ('add', j)
    for j in T:
        for l in range(p):
            if l not in Ts:
                yield tuple(sorted((Ts - {j}) | {l})), ('swap', j, l)

for n, p, repeats in [(10, 9, 1), (80, 79, 30)]:
    K = n // 2
    for rho in [0.2, 0.8, 0.95]:
        sigma = (1-rho)*np.eye(p) + rho*np.ones((p,p))
        gram = (n-1)*sigma
        # Actual centred n-by-p matrix, including the rank boundary p=n-1.
        basis = np.linalg.qr(np.column_stack((np.ones(n), rng.normal(size=(n,p)))))[0][:,1:p+1]
        X = np.sqrt(n-1)*basis @ np.linalg.cholesky(sigma).T
        assert np.max(np.abs(X.T @ X - gram)) < 1e-10
        theta = np.zeros(p); theta[0], theta[-1] = 1.0, -0.7
        eps = rng.normal(size=n); eps -= eps.mean()
        Y = X @ theta + eps
        y = Y / np.sqrt(Y @ Y / (n-1))
        z = X.T @ y
        nu = n/2 + 0.01
        alpha = (n*n-1)*(1-rho) + 1
        beta = (n*n-1)*rho
        def gamma(k): return beta/(alpha+k*beta)
        def prior(k): return -math.log(2)-math.log(math.comb(2*p-1,k))
        def direct(T):
            if not T: return prior(0)-nu*math.log(0.02+n-1)
            ix = np.array(T)
            G = gram[np.ix_(ix,ix)]
            H = (n+1)*G+np.eye(len(T))
            L = np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1]
            Q = n-1-n*z[ix] @ np.linalg.solve(H,z[ix])
            return prior(len(T))-L/2-nu*math.log(0.02+Q)
        def L(k):
            if k == 0: return 0.0
            ap = (n-1)*(1-rho)+1; bp=(n-1)*rho
            return (k-1)*math.log(alpha/ap)+math.log((alpha+k*beta)/(ap+k*bp))
        def delta(k): return math.log((2*p-k)/k)+(L(k)-L(k-1))/2
        if n == 10:
            sets = [T for k in range(K+1) for T in itertools.combinations(range(p),k)]
        else:
            sets = [tuple(sorted(rng.choice(p,size=int(rng.integers(1,K+1)),replace=False))) for _ in range(repeats)]
        scores = {T: direct(T) for T in sets}
        for T in sets:
            if not T: continue
            k=len(T); zz=z[list(T)]; B=zz.sum()
            quad=(zz@zz-gamma(k)*B*B)/alpha
            psi=0.02+n-1-n*quad
            t=z-gamma(k)*B
            ns=list(neighbours(T,p,K))
            if n != 10:
                # One deletion, one feasible addition and one swap where available.
                ns=[next(v for v in ns if v[1][0]==typ) for typ in ['del','add','swap'] if any(v[1][0]==typ for v in ns)]
            for U, move in ns:
                if U not in scores: scores[U]=direct(U)
                observed=scores[U]-scores[T]
                if move[0]=='del':
                    j=move[1]; gain=delta(k)-nu*math.log1p(n*(1+gamma(k-1))*t[j]**2/(alpha*psi))
                elif move[0]=='add':
                    l=move[1]; gain=-delta(k+1)-nu*math.log1p(-n*(1-gamma(k+1))*t[l]**2/(alpha*psi))
                else:
                    j,l=move[1:]; V=t[l]**2-t[j]**2-gamma(k)*(t[l]-t[j])**2
                    gain=-nu*math.log1p(-n*V/(alpha*psi))
                max_error=max(max_error,abs(observed-gain)); comparisons+=1
                assert abs(observed-gain)<1e-8
        if n == 10:
            # Exercise the cap test after the complete scan, including a=0 and ties.
            def run(start,cap):
                T=start; scanned=[]; scored={start}; moves=0
                while True:
                    ns=list(neighbours(T,p,K)); scanned.append(T); scored.update(U for U,_ in ns)
                    best=min((U for U,_ in ns),key=lambda U:(-scores[U],U))
                    if scores[best]<=scores[T]: return scanned,scored,True
                    if moves>=cap: return scanned,scored,False
                    T=best; moves+=1
            for start in sets[::11]:
                full,_,_=run(start,10000)
                m=len(full)-1
                for cap in range(m+2):
                    scanned,scored,cert=run(start,cap)
                    expected=full[:min(cap,m)+1]
                    expected_scores={start}
                    for T in expected: expected_scores.update(U for U,_ in neighbours(T,p,K))
                    assert scanned==expected and scored==expected_scores and cert==(m<=cap)
                    prefix_checks+=1

# Check G1 for generic, including singular and p>n, standardized designs.
for n,p in [(12,9),(12,20),(30,50)]:
    for _ in range(20):
        X=rng.normal(size=(n,p)); X-=X.mean(axis=0)
        X*=np.sqrt(n-1)/np.linalg.norm(X,axis=0)
        theta=np.zeros(p); theta[0]=1.0
        Y=X@theta+rng.normal(size=n); Y-=Y.mean(); y=Y*np.sqrt(n-1)/np.linalg.norm(Y)
        def generic(T):
            G=X[:,T].T@X[:,T]; z=X[:,T].T@y
            H=(n+1)*G+np.eye(len(T))
            det=np.linalg.slogdet(H)[1]-np.linalg.slogdet(G+np.eye(len(T)))[1]
            Q=y@y-n*z@np.linalg.solve(H,z)
            return det,Q
        S=[0]; T=[0]+list(rng.choice(np.arange(1,p),size=n//2-1,replace=False))
        Ls,Qs=generic(S); Lt,Qt=generic(T)
        assert Qt<=Qs+1e-9
        assert Lt-Ls <= (len(T)-len(S))*math.log(n+1)+1e-9
        generic_checks+=1
record(f'Direct-matrix neighbour gain comparisons: {comparisons}; maximum absolute error {max_error:.3e}')
record(f'Complete-scan cap-prefix checks: {prefix_checks}')
record(f'Generic nested Q/determinant checks, including p>n: {generic_checks}')
after={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
assert before==after
record(f'Protected package/code files unchanged during audit: {len(before)}')
record('These are identity, control-flow and reporting checks, not numerical proofs of asymptotic claims.')
(OUT/'audit_output.txt').write_text('\n'.join(log)+'\n',encoding='utf-8')
