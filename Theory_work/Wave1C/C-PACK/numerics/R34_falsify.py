"""Independent exhaustive finite-state falsification of SL0; writes beside itself.

Run: py -3.13 Theory_work/Wave1C/C-PACK/numerics/R34_falsify.py
Needs NumPy. No repo imports, production mutations, git commands, or simulation
of posterior draws. Every feasible model is scored with the SoP D0 formula.
Probability sums use binary64, with explicit tolerance; this is enumeration,
not a symbolic or interval-arithmetic certificate. Synthetic boundary laws
separately test sharpness and deliberately false strengthened conclusions.
"""
from __future__ import annotations

import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

TOL = 8e-12
COUNTS = Counter()
WORST = defaultdict(float)
LINES: list[str] = []


def say(s: str) -> None:
    LINES.append(s)


def check(name: str, excess: float) -> None:
    COUNTS[name] += 1
    WORST[name] = max(WORST[name], float(excess))
    if not math.isfinite(float(excess)) or excess > TOL:
        raise AssertionError((name, excess))


def standardize(x: np.ndarray) -> np.ndarray:
    z = x - x.mean(axis=0)
    return z / z.std(axis=0, ddof=1)


def model_space(p: int, k: int):
    masks = np.arange(1 << p, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(p)) & 1).astype(bool)
    sizes = bits.sum(axis=1)
    feasible = sizes <= k
    return masks, bits, sizes, feasible


def d0_posterior(x: np.ndarray, y: np.ndarray):
    n, p = x.shape
    k = min(p, n // 2)
    masks, bits, sizes, feasible = model_space(p, k)
    gram, z, yy = x.T @ x, x.T @ y, float(y @ y)
    logmass = np.full(1 << p, -np.inf)
    # Normalized cap-prior constant and common c_n cancel in normalization.
    for mask in masks[feasible]:
        ix = np.flatnonzero(bits[mask])
        g = gram[np.ix_(ix, ix)]
        h = (n + 1) * g + np.eye(len(ix))
        if len(ix):
            sh, lh = np.linalg.slogdet(h)
            sg, lg = np.linalg.slogdet(g + np.eye(len(ix)))
            assert sh == sg == 1
            q = yy - n * float(z[ix] @ np.linalg.solve(h, z[ix]))
        else:
            lh = lg = 0.0
            q = yy
        assert q > -1e-9 and 0.02 + q > 0
        logprior = -math.log(2) - math.log(math.comb(2 * p - 1, len(ix)))
        logmass[mask] = logprior - 0.5 * (lh - lg) - (0.01 + n / 2) * math.log(0.02 + q)
    mass = np.exp(logmass - np.max(logmass))
    mass /= mass.sum()
    check('D0 normalization', abs(float(mass.sum()) - 1))
    assert np.all(mass[feasible] > 0), 'test range unexpectedly underflowed'
    assert np.all(mass[~feasible] == 0)
    return mass, masks, bits, sizes, feasible


def check_law(mass, p, k, truths=None):
    masks, bits, sizes, feasible = model_space(p, k)
    pip = mass @ bits
    # Fast upper-subset zeta transform: joint[a] = P(a subset S), ALL A.
    joint = mass.copy()
    for j in range(p):
        for a in masks[(masks & (1 << j)) == 0]:
            joint[a] += joint[a | (1 << j)]
    size_mass = np.bincount(sizes, weights=mass, minlength=p + 1)
    rng = np.random.default_rng(912345 + p + k)
    hs = [sizes.astype(float), rng.normal(size=len(mass)),
          (masks % 3 == 0).astype(float)]
    for truth in (masks if truths is None else truths):
        truth = int(truth)
        tb = bits[truth]
        delta = 1 - mass[truth]  # zero extension for an infeasible truth
        err = np.abs(pip - tb)
        check('SL0(i) coordinate', float(err.max() - delta))
        # Explicit empty-index convention; original text does not specify it.
        miss = float((1 - pip[tb]).max()) if tb.any() else 0.0
        false = float(pip[~tb].max()) if (~tb).any() else 0.0
        check('SL0(i) max sum', miss + false - 2 * delta)
        indicator = ((masks & truth) == masks).astype(float)
        check('SL0(ii) all joint inclusions', float(np.abs(joint - indicator).max() - delta))
        if feasible[truth]:
            for h in hs:
                osc = float(np.ptp(h[feasible]))
                check('SL0(ii) bounded h', abs(float(mass @ h - h[truth])) - delta * osc)
            # Sup over ALL [0,1]-valued h equals TV to the truth point mass.
            tv = 0.5 * (abs(mass[truth] - 1) + float(mass.sum() - mass[truth]))
            check('SL1(d) finite TV identity', abs(tv - delta))
        qs = [np.nextafter(0., 1.), .001, .1, .25, .5, .75, .9, .999,
              np.nextafter(1., 0.)]
        if 0 < delta < 1:
            qs += [delta, 1 - delta]
        for q in qs:
            if delta < min(q, 1 - q):
                chosen = int(sum(1 << j for j in range(p) if pip[j] > q))
                check('SL0(iii) strict threshold implication', float(chosen != truth))
        if delta < .5:
            modes = masks[mass == mass.max()]
            check('SL0(iv) unique HPM', float(len(modes) != 1 or modes[0] != truth))
        check('SL0(v) size concentration', (1 - delta) - float(size_mass[sizes[truth]]))
    return pip


def design(rng, n, p, kind):
    a = np.eye(p)
    if kind == 'equicorrelation':
        a = .85 * np.ones((p, p)) + .15 * np.eye(p)
    elif kind == 'AR1':
        a = .9 ** np.abs(np.arange(p)[:, None] - np.arange(p))
    elif kind == 'blocks':
        a = np.where(np.arange(p)[:, None] // 3 == np.arange(p) // 3, .6, 0.) + .4 * np.eye(p)
    elif kind == 'masking_pair':
        a[0, 1] = a[1, 0] = .4
    x = rng.normal(size=(n, p)) @ np.linalg.cholesky(a).T
    if kind == 'duplicate':
        x[:, 1] = x[:, 0]  # singular Gram; D0 ridge score still defined
    return standardize(x)


def enumerate_designs():
    kinds = ['independent', 'equicorrelation', 'AR1', 'blocks', 'masking_pair', 'duplicate']
    npost = ntruth = nmodels = 0
    for n in [6, 12, 24, 60]:
        for p in [4, 7, 10]:
            for kind in kinds:
                for signal in [0., .7, 5.]:
                    seed = 342026 + n * 1000 + p * 100 + kinds.index(kind) * 10 + int(signal * 10)
                    rng = np.random.default_rng(seed)
                    x = design(rng, n, p, kind)
                    beta = np.zeros(p)
                    beta[0] = signal
                    beta[1] = -.4 * signal if kind == 'masking_pair' else -.5 * signal
                    y = standardize(x @ beta + rng.normal(size=n))
                    mass, masks, bits, sizes, feasible = d0_posterior(x, y)
                    check_law(mass, p, min(p, n // 2))
                    npost += 1
                    ntruth += len(masks)
                    nmodels += int(feasible.sum())
    say(f'D0 exhaustive designs: {npost} posteriors; {nmodels} feasible model scores; {ntruth} truth-law pairs.')
    say('n = 6,12,24,60; p = 4,7,10; signals = 0,.7,5; 6 correlation structures.')
    say('Every truth subset and every joint-inclusion A checked, including empty/full/infeasible truths.')
    say('Singular duplicate columns and p > n included. Empty maxima use ZERO by explicit convention.')


def boundaries():
    cases = 0
    for p in [2, 4, 7, 10]:
        k = min(p, 3)
        for s in range(1, min(k, p - 1) + 1):
            truth = (1 << s) - 1
            replacement = (truth ^ 1) | (1 << s)
            for delta in [0., .01, .1, .25, .49, .5, .75, 1.]:
                mass = np.zeros(1 << p)
                mass[truth], mass[replacement] = 1 - delta, delta
                pip = check_law(mass, p, k, truths=[truth])
                lhs = float((1 - pip[:s]).max() + pip[s:].max())
                check('SL0(vi) arbitrary-law attainment', abs(lhs - 2 * delta))
                cases += 1
    say(f'Attainment: {cases} two-point probability laws satisfy max-sum = 2*delta.')
    say('These laws have zero off-pair masses and are NOT finite-data D0 posteriors.')
    # Exact binary-rational counterexamples; no floating threshold ambiguity.
    p, k = 2, 1
    mass = np.array([0., .5, .5, 0.])
    pip = check_law(mass, p, k)
    assert list(np.flatnonzero(mass == mass.max())) == [1, 2]
    assert not pip[0] > .5  # MPM misses truth 1 at equality delta=1/2
    say('Negative control: delta=.5, truth={0}, masses({0},{1})=(.5,.5): HPM ties and MPM empty.')
    mass = np.array([0., .75, .25, 0.])
    pip = check_law(mass, p, k)
    assert not pip[0] > .75
    assert pip[1] > .24
    say('Negative controls: q=1-delta=.75 loses a true variable; q=.24<delta includes the false variable.')
    say('At q=delta=.25 the strict > rule excludes the tied false variable (the sufficient condition is conservative).')
    # A strictly positive law illustrates why the D0 attainment claim needs scope.
    mass = np.array([.125, .625, .25, 0.])
    pip = check_law(mass, 2, 1)
    delta = 1 - mass[1]
    lhs = 1 - pip[0] + pip[1]
    assert lhs < 2 * delta
    say(f'Full-support law p=2,K=1: pi(empty)=.125, pi({{0}})=.625, pi({{1}})=.25; max-sum={lhs}, 2delta={2*delta}.')
    say('General obstruction: for a nonempty proper truth and full support, pi(empty)>0 gives max_false < delta, so equality is impossible.')
    for truth in [0, 3]:
        mass = np.array([.125, .25, .375, .25])
        pip = check_law(mass, 2, 2, truths=[truth])
        delta = 1 - mass[truth]
        lhs = float(pip.max()) if truth == 0 else float((1 - pip).max())
        assert lhs <= delta and delta < 2 * delta
        say(f'Empty/full truth boundary truth_mask={truth}: max-sum={lhs}; delta={delta}; universal 2delta-attainment false for this truth.')


def main():
    say('R34 independent SL0 falsification; no posterior sampling; NumPy ' + np.__version__)
    say(f'Absolute numerical tolerance = {TOL:g}; deterministic seeds embedded in script.')
    enumerate_designs()
    boundaries()
    say('CHECK COUNTS AND MAX POSITIVE RESIDUALS:')
    for name in sorted(COUNTS):
        say(f'  {name}: checks={COUNTS[name]}, max_excess={WORST[name]:.3e}')
    say('PASS: SL0(i)-(v), h/TV identities, and qualified arbitrary-law attainment; all negative controls detected.')
    say('NOT ESTABLISHED BY NUMERICS: asymptotic rates, Song-Liang theorems, code integration, or D0 exact attainment.')
    here = Path(__file__).resolve()
    say('Script SHA256: ' + hashlib.sha256(here.read_bytes()).hexdigest())
    output = '\n'.join(LINES) + '\n'
    here.with_name('R34_falsify_out.txt').write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
