"""Independent council diagnostics; no imports from the submitted implementation."""
import itertools
import json
import math
from pathlib import Path
import runpy
import contextlib
import io
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
TICKET = ROOT / 'Theory_work/Wave2/W2-FAC-B'
OUT = Path(__file__).parent
rng = np.random.default_rng(8061)
counts = dict(data_sets=0, models=0, gains=0, paths=0, masked_starts=0,
              interval_configurations=0)
errors = dict(score=0.0, gain=0.0, centre=0.0)

for p, rho, masked, seed in itertools.product((4, 7), (.2, .5, .9), (False, True), range(2)):
    n = 10_000_000
    sigma = 1.3
    theta = np.zeros(p)
    theta[:2] = (1.0, -1.0/rho) if masked else (.8, 1.1)
    truth = frozenset((0, 1))
    blocks_list = [((0, 1, 2), tuple(range(3, p))),
                   ((0, 2), tuple(j for j in range(p) if j not in (0, 2)))]
    Sigma = (1-rho)*np.eye(p) + rho*np.ones((p, p))
    eta, xi = rng.normal(), rng.normal(size=p)
    g = math.sqrt(rho)*eta + math.sqrt(1-rho)*xi
    norm_e = sigma*sigma*(g @ np.linalg.solve(Sigma, g) + rng.chisquare(n-1-p))
    s2 = ((n-1)*(theta @ Sigma @ theta) +
          2*sigma*math.sqrt(n-1)*(theta @ g) + norm_e)/(n-1)
    s = math.sqrt(s2)
    z = ((n-1)*Sigma @ theta + sigma*math.sqrt(n-1)*g)/s
    G = (n-1)*Sigma
    alpha, beta = (n*n-1)*(1-rho)+1, (n*n-1)*rho
    ap, bp = (n-1)*(1-rho)+1, (n-1)*rho
    nu = n/2+.01
    kap = alpha/beta
    kc = ((n-1)*rho*theta.sum()+sigma*math.sqrt((n-1)*rho)*eta)/s
    k1 = sigma*math.sqrt((n-1)*(1-rho))/s
    varrho = (math.sqrt(n-1)*rho*theta.sum()/(sigma*math.sqrt(1-rho))+
              math.sqrt(rho/(1-rho))*alpha*eta)/beta
    sets = [frozenset(j for j in range(p) if mask & (1 << j)) for mask in range(1 << p)]

    def prior(k):
        return -math.log(2*math.comb(2*p-1, k))

    def detterm(k):
        return 0. if not k else ((k-1)*math.log(alpha/ap) + math.log((alpha+k*beta)/(ap+k*bp)))

    def direct(A, sign=None):
        ids = sorted(A)
        if not ids:
            return prior(0)-nu*math.log(.02+n-1)
        GA, za = G[np.ix_(ids, ids)], z[ids]
        if sign is not None:
            sg = sign[ids]
            GA, za = GA*sg[:, None]*sg[None, :], za*sg
        H = (n+1)*GA+np.eye(len(ids))
        Q = n-1-n*(za @ np.linalg.solve(H, za))
        L = np.linalg.slogdet(H)[1]-np.linalg.slogdet(GA+np.eye(len(ids)))[1]
        return prior(len(ids))-.5*L-nu*math.log(.02+Q)

    F = {A: direct(A) for A in sets}
    flips = rng.choice((-1., 1.), size=p)
    for A in sets:
        k = len(A)
        ids = sorted(A)
        B = z[ids].sum()
        gamma = 1/(k+kap)
        quad = (z[ids] @ z[ids]-gamma*B*B)/alpha
        psi = .02+n-1-n*quad
        closed = prior(k)-.5*detterm(k)-nu*math.log(psi)
        errors['score'] = max(errors['score'], abs(closed-F[A]), abs(direct(A, flips)-F[A]))
        counts['models'] += 1
        t = z-gamma*B
        delta = lambda u: math.log((2*p-u)/u)+.5*(detterm(u)-detterm(u-1))
        candidates = []
        for j in A:
            gain = delta(k)-nu*math.log1p(n/alpha*(1+1/(k-1+kap))*t[j]**2/psi)
            candidates.append((A-{j}, gain))
        for l in set(range(p))-A:
            gain = -delta(k+1)-nu*math.log1p(-n/alpha*(1-1/(k+1+kap))*t[l]**2/psi)
            candidates.append((A|{l}, gain))
            for j in A:
                V = t[l]**2-t[j]**2-gamma*(t[l]-t[j])**2
                candidates.append(((A-{j})|{l}, -nu*math.log1p(-n/alpha*V/psi)))
        for C, gain in candidates:
            errors['gain'] = max(errors['gain'], abs(gain-(F[C]-F[A])))
            counts['gains'] += 1
        if truth <= A:
            x = (xi[ids].sum()-varrho)/(k+kap)
            errors['centre'] = max(errors['centre'], abs(x-(gamma*B-kc)/k1))

    def neighbours(A):
        for j in A:
            yield A-{j}
        for l in set(range(p))-A:
            yield A|{l}
            for j in A:
                yield (A-{j})|{l}

    for blocks in blocks_list:
        blocks = [frozenset(b) for b in blocks if b]
        N0 = frozenset().union(*(b-truth for b in blocks if truth <= b))
        star = frozenset(range(p))-N0
        # Remove the size prior from each block score; common constants do not affect the maximiser.
        def start_score(A):
            return prior(len(A))+sum(F[A & b]-prior(len(A & b))-F[frozenset()]+prior(0) for b in blocks)
        ranked = sorted(sets, key=lambda A: (-start_score(A), len(A), tuple(sorted(A))))
        assert ranked[0] == star and start_score(ranked[0]) > start_score(ranked[1])
        counts['masked_starts'] += int(masked)
        A, path = star, [star]
        while True:
            best = min(neighbours(A), key=lambda B: (-F[B], tuple(sorted(B))))
            if F[best] <= F[A]:
                break
            assert best < A and len(A-best) == 1 and truth <= best
            nulls = A-truth
            x = (sum(xi[j] for j in A)-varrho)/(len(A)+kap)
            nearest = min(nulls, key=lambda j: abs(xi[j]-x))
            assert A-best == {nearest}
            lo = max((xi[j] for j in nulls if xi[j] < x), default=-np.inf)
            hi = min((xi[j] for j in nulls if xi[j] > x), default=np.inf)
            assert star-A == {j for j in star-truth if lo < xi[j] < hi}
            A = best
            path.append(A)
        assert A == truth and len(path)-1 == len(star-truth)
        for cap in range(len(path)+1):
            visited = path[:min(cap, len(path)-1)+1]
            scored = {path[0]}.union(*(set(neighbours(B)) for B in visited))
            assert (truth in scored) == (cap >= len(path)-2)
        counts['paths'] += 1
    counts['data_sets'] += 1

# Arbitrary real configurations and offsets: test the deterministic interval lemma independently of gains.
for seed in range(20):
    vals = rng.normal(size=13)
    for offset in (-100., -2., 0., 3., 100.):
        for kap in (.01, .3, 4.):
            kept, removed = set(range(13)), set()
            while kept:
                x = (sum(vals[j] for j in kept)-offset)/(len(kept)+1+kap)
                lo = max((vals[j] for j in kept if vals[j] < x), default=-np.inf)
                hi = min((vals[j] for j in kept if vals[j] > x), default=np.inf)
                assert removed == {j for j in range(13) if lo < vals[j] < hi}
                j = min(kept, key=lambda j: abs(vals[j]-x))
                kept.remove(j)
                removed.add(j)
                counts['interval_configurations'] += 1

assert errors['score'] < 2e-6 and errors['gain'] < 2e-6 and errors['centre'] < 1e-9
report = dict(counts=counts, maximum_absolute_errors=errors, result='PASS')
print(json.dumps(report, indent=2))
(OUT/'independent_check_out.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    runpy.run_path(str(TICKET/'reviews/citecheck.py'), run_name='__main__')
(OUT/'citecheck_rerun.txt').write_text(buf.getvalue(), encoding='utf-8')
print(buf.getvalue().splitlines()[-1])
