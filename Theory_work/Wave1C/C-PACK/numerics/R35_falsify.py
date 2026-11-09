"""Read-only source review companion; writes only its adjacent *_out.txt.

Exact specification: SoP/sections/02_method.tex:187-192,205-206 and
Campaign core/cpp/v3_blocks.h:39-143. No R fit or git operations are run.
Six RNG seeds, reused as six sequential streams over 24 configurations.
No inference of an all-subset bound from a finite collection of probes.
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import heapq
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.special import gammaln, logsumexp


def lh_cov(g, groups, c, rho=0.7, psi=0.5):
    """Rank-one hub links, NOT constant cross-group correlation."""
    E = (1-rho)*np.eye(g) + rho*np.ones((g, g))
    S = np.kron(np.eye(groups), E)
    link = psi*np.outer(E[:, 0], E[0, :])
    for i in range(c):
        a, b = slice(2*i*g, (2*i+1)*g), slice((2*i+1)*g, (2*i+2)*g)
        S[a, b], S[b, a] = link, link.T
    return S


def make_blocks(R, B):
    """Complete linkage, union-lex ties, min-index children, whole-cluster next fit."""
    p = len(R)
    dist = np.zeros((2*p-1, 2*p-1))
    dist[:p, :p] = 1-np.abs(R)
    members = [tuple([j]) for j in range(p)] + [None]*(p-1)
    children = [None]*(2*p-1)
    active = set(range(p))
    heap = [(float(dist[a, b]), (a, b), a, b)
            for a in range(p) for b in range(a+1, p)]
    heapq.heapify(heap)
    for new in range(p, 2*p-1):
        while True:
            _, _, a, b = heapq.heappop(heap)
            if a in active and b in active:
                break
        if members[a][0] > members[b][0]:
            a, b = b, a
        children[new] = (a, b)
        members[new] = tuple(sorted(members[a]+members[b]))
        active.remove(a)
        active.remove(b)
        for x in active:
            d = max(dist[a, x], dist[b, x])
            dist[new, x] = dist[x, new] = d
            union = tuple(sorted(members[new]+members[x]))
            heapq.heappush(heap, (float(d), union, new, x))
        active.add(new)
    retained, stack = [], [2*p-2]
    while stack:
        node = stack.pop()
        if len(members[node]) <= B:
            retained.append(members[node])
        else:
            a, b = children[node]
            stack.extend([b, a])
    blocks, current = [], []
    for cluster in retained:
        if len(current)+len(cluster) > B:
            blocks.append(tuple(sorted(current)))
            current = []
        current.extend(cluster)
    if current:
        blocks.append(tuple(sorted(current)))
    assert sorted(x for block in blocks for x in block) == list(range(p))
    assert all(0 < len(block) <= B for block in blocks)
    return blocks


def msharp(n, p, s0):
    K = min(p, n//2)
    ks = np.arange(K+1)
    logchoose = lambda m, k: gammaln(m+1)-gammaln(k+1)-gammaln(m-k+1)
    logterms = logchoose(p, ks)-logchoose(2*p-1, ks)+logchoose(2*p-1, s0)
    target = -(s0+2)*math.log(n)/2
    for m in range(s0, K+1):
        if m == K or logsumexp(logterms[m+1:]) <= target:
            return m
    raise AssertionError('cutoff missing')


def minimum(R, indices):
    return float(np.linalg.eigvalsh(R[np.ix_(indices, indices)])[0])


def main():
    start = time.perf_counter()
    lines = []
    def emit(s=''):
        lines.append(s)
        print(s, flush=True)
    emit('R35 falsification: LH-iid partition and sparse eigenvalues')
    emit(f'Python {platform.python_version()}; NumPy {np.__version__}; SciPy {scipy.__version__}')
    emit('Seeds: 0..5 (6 sequential RNG streams); n=200,800,3200; g=9,10,11,12; c=1,2; G=24; v=0; rho=.7; psi=.5; A=2.')
    emit('p=24g (216..288), including p>n at n=200; SIZE checked at every configuration.')
    emit('lambda0=(1-.5)(1-.7)=.15; target=lambda0/2=.075.')
    emit('L=min(p,msharp+s0+j0+g*s0+1), s0=2c, j0=ceil((2A+1)s0)+1.')
    emit('Probes: every whole group, all signal-unit columns, first L columns,')
    emit('plus 12 random subsets at each of sizes min(p,16), min(p,ceil(log n)), L.')
    emit('A full-Gram eigenvalue >=.075 certifies ALL subsets by interlacing;')
    emit('otherwise finite probes do NOT certify the universal statement.')
    emit('delta_n and the stated onset are computed literally; failures before onset are not theorem counterexamples.')
    emit('All partitions are hypothetical make_blocks functions even if production dispatch would be exact.')
    # Deterministic mechanism checks, including deliberate violation of SIZE.
    S = lh_cov(10, 24, 2)
    canonical = {tuple(range(h*10, (h+1)*10)) for h in range(24)}
    assert set(make_blocks(S, 14)) == canonical
    assert set(make_blocks(S, 16)) == canonical
    assert set(make_blocks(S, 20)) != canonical
    emit('Deterministic checks: population recovery at B=14,16; nonrecovery at B=20=2g: PASS.')
    # An exact tie verifies the union-lex comparison and smallest-index traversal.
    assert make_blocks(np.eye(4), 2) == [(0, 1), (2, 3)]
    emit('Deterministic tie fixture: identity correlation, p=4,B=2 -> [(0,1),(2,3)]: PASS.')
    emit('')
    emit('n g c p B L | recovery/6 strict-margin/6 eig-probe-fail/6 full-cert/6 | min-probe min-full max-entry-error delta onset/6')
    results = {}
    for seed in range(6):
        rng = np.random.default_rng(seed)
        for n in (200, 800, 3200):
            for g in (9, 10, 11, 12):
                for c in (1, 2):
                    p, A, s0 = 24*g, 2, 2*c
                    B = min(math.isqrt(n), math.isqrt(p), 16)
                    assert g <= B < 2*g and 18 <= p <= n**A
                    S = lh_cov(g, 24, c)
                    X = rng.standard_normal((n, p)) @ np.linalg.cholesky(S).T
                    X -= X.mean(axis=0)
                    X /= np.sqrt(np.sum(X**2, axis=0)/(n-1))
                    R = X.T @ X/(n-1)
                    np.fill_diagonal(R, 1.0)
                    blocks = make_blocks(R, B)
                    groups = {tuple(range(h*g, (h+1)*g)) for h in range(24)}
                    recovery = set(blocks) == groups
                    within = np.equal.outer(np.arange(p)//g, np.arange(p)//g)
                    np.fill_diagonal(within, False)
                    cross = np.not_equal.outer(np.arange(p)//g, np.arange(p)//g)
                    margin = float(np.abs(R)[within].min()-np.abs(R)[cross].max())
                    if margin > 0:
                        assert recovery, 'COUNTEREXAMPLE to deterministic recovery implication'
                    j0 = math.ceil((2*A+1)*s0)+1
                    L = min(p, msharp(n, p, s0)+s0+j0+g*s0+1)
                    subsets = [np.arange(h*g, (h+1)*g) for h in range(24)]
                    subsets += [np.arange(g*s0), np.arange(L)]
                    for k in sorted({16, math.ceil(math.log(n)), L}):
                        subsets += [rng.choice(p, min(p, k), replace=False) for _ in range(12)]
                    probe = min(minimum(R, t) for t in subsets)
                    full = float(np.linalg.eigvalsh(R)[0])
                    error = float(np.abs(R-S).max())
                    delta = 32*math.sqrt(2*(A+1)*math.log(n)/(n-1))
                    onset = delta <= 2 and L*delta <= .075
                    # Deterministic Weyl certificate, using actual error, is separately testable.
                    if L*error <= .075:
                        assert probe >= .075-1e-10
                    if onset and error <= delta:
                        assert probe >= .075-1e-10, 'COUNTEREXAMPLE to I2(ii) implication'
                    key = (n, g, c, p, B, L)
                    results.setdefault(key, []).append((recovery, margin > 0, probe < .075-1e-10,
                                                       full >= .075, probe, full, error, delta, onset))
        emit(f'Completed seed {seed}; elapsed {time.perf_counter()-start:.1f}s')
    for key, data in sorted(results.items()):
        x = np.asarray(data, float)
        sums = x.sum(axis=0)
        emit(' '.join(map(str, key))+' | '+
             ' '.join(f'{int(sums[j])}/6' for j in range(4))+' | '+
             f'{x[:,4].min():.8f} {x[:,5].min():.8f} {x[:,6].max():.8f} {x[0,7]:.8f} {int(sums[8])}/6')
    x = np.asarray([r for rows in results.values() for r in rows], float)
    emit('')
    emit(f'TOTAL draws={len(x)}; recovery={int(x[:,0].sum())}; strict margins={int(x[:,1].sum())}; '+
         f'eigen-probe failures={int(x[:,2].sum())}; full-Gram certificates={int(x[:,3].sum())}; onset met={int(x[:,8].sum())}.')
    emit('No failed assertion: no deterministic recovery/Weyl-implication counterexample found.')
    emit('No asymptotic or high-probability theorem is proved by this small simulation.')
    emit(f'Elapsed seconds: {time.perf_counter()-start:.2f}')
    Path(__file__).with_name('R35_falsify_out.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
