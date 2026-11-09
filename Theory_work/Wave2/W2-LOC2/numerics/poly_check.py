"""Small local falsification checks; standard library only; not a proof."""
import itertools
import math
import pathlib
import random
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent


def inv(a):
    n = len(a)
    z = [list(row) + [float(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        k = max(range(j, n), key=lambda k: abs(z[k][j]))
        z[j], z[k] = z[k], z[j]
        t = z[j][j]
        assert abs(t) > 1e-12
        z[j] = [x / t for x in z[j]]
        for i in range(n):
            if i != j:
                t = z[i][j]
                z[i] = [x - t * y for x, y in zip(z[i], z[j])]
    return [row[n:] for row in z]


def regress(s, target, cond):
    if not cond:
        return []
    a = inv([[s[i][j] for j in cond] for i in cond])
    return [sum(row[k] * s[cond[k]][target] for k in range(len(cond)))
            for row in a]


def partial(s, i, j, cond):
    beta = regress(s, j, cond)
    return s[i][j] - sum(s[i][v] * t for v, t in zip(cond, beta))


def main():
    out = []
    err_identity = err_variance = 0.0
    worst_l1_ratio = worst_bc_ratio = 0.0
    count = 0
    inverse_cases = 0
    for seed in range(12):
        rng = random.Random(seed)
        p = 8
        alpha = [2.2, 8.6, 10.0][seed % 3]
        positions = sorted(rng.sample(range(1, 22), p))
        # Absolute off-diagonal row sum < .4, so spectral floor > .6.
        s = [[float(i == j) for j in range(p)] for i in range(p)]
        for i in range(p):
            for j in range(i):
                s[i][j] = s[j][i] = (
                    rng.uniform(-0.2, 0.2)
                    * (1 + abs(positions[i] - positions[j])) ** -alpha)
        c = min(1 - sum(abs(s[i][j]) for j in range(p) if i != j)
                for i in range(p))
        upper = max(1 + sum(abs(s[i][j]) for j in range(p) if i != j)
                    for i in range(p))
        assert c > 0.6
        si = inv(s)
        for bandwidth in [1, 3, 7]:
            sb = [[s[i][j] if abs(positions[i]-positions[j]) <= bandwidth else 0
                   for j in range(p)] for i in range(p)]
            sbi = inv(sb)
            tail_bound = 0.4 / (alpha-1) * bandwidth ** (1-alpha)
            max_error = max(abs(si[i][j]-sbi[i][j])
                            for i in range(p) for j in range(p))
            assert max_error <= 2 * tail_bound / (c*c) + 1e-12
            kappa = min(0.01, c * (alpha-2) / 100)
            rate = kappa / bandwidth
            schur = max(sum(abs(sb[i][j]) * math.expm1(
                rate*abs(positions[i]-positions[j])) for j in range(p))
                for i in range(p))
            assert schur < c/4
            for i in range(p):
                for j in range(p):
                    ct_bound = 4/c * math.exp(-rate*abs(positions[i]-positions[j]))
                    assert abs(sbi[i][j]) <= ct_bound + 1e-12
            inverse_cases += 1
        for l in range(p):
            others = [i for i in range(p) if i != l]
            for mask in range(1 << len(others)):
                t = [v for k, v in enumerate(others) if (mask >> k) & 1]
                near = [v for v in t if abs(positions[l] - positions[v]) <= 3]
                far = [v for v in t if v not in near]
                bt = dict(zip(t, regress(s, l, t)))
                bn = dict(zip(near, regress(s, l, near)))
                lam = [bt.get(v, 0) - bn.get(v, 0) for v in range(p)]
                gamma_l1 = 0.0
                for w in far:
                    g = dict(zip(near, regress(s, w, near)))
                    gamma_l1 = max(gamma_l1, sum(abs(x) for x in g.values()))
                for v in near:
                    rhs = -sum(bt[w] * dict(zip(near, regress(s, w, near)))[v]
                               for w in far)
                    err_identity = max(err_identity, abs(lam[v] - rhs))
                tail = sum(abs(bt[w]) for w in far)
                bound = (1 + gamma_l1) * tail
                l1 = sum(abs(x) for x in lam)
                assert l1 <= bound + 1e-12
                if bound:
                    worst_l1_ratio = max(worst_l1_ratio, l1 / bound)
                var_d = sum(lam[i] * s[i][j] * lam[j]
                            for i in range(p) for j in range(p))
                vt = partial(s, l, l, t)
                vn = partial(s, l, l, near)
                err_variance = max(err_variance, abs(vn - vt - var_d))
                assert var_d <= l1 * l1 + 1e-12
                assert abs(vn - vt - var_d) < 1e-12
                # BC bound derived in P1, with K0=1. Check every j outside t.
                for j in others:
                    if j in t:
                        continue
                    m = len(t) + 2
                    bc = (upper ** 2 * math.factorial(m - 1)
                          * (m - 1) ** alpha * c ** -m
                          * (1 + abs(positions[l] - positions[j])) ** -alpha)
                    ratio = abs(partial(s, l, j, t)) / bc
                    worst_bc_ratio = max(worst_bc_ratio, ratio)
                    assert ratio <= 1 + 1e-12
                count += 1
    out += [f'Population cases: {count}; seeds=12; p=8; no simulation claim.',
            f'Banded inverse Schur/conjugation and resolvent cases: {inverse_cases}',
            f'Projection-tower coefficient identity max error: {err_identity:.3g}',
            f'Variance decomposition max error: {err_variance:.3g}',
            f'Max l1 difference / finite tail bound: {worst_l1_ratio:.8g}',
            f'Max conditional covariance / explicit BC bound: {worst_bc_ratio:.8g}']
    for alpha in [8.5001, 8.6, 9.0, 12.0]:
        b = 1 / (2 * alpha)
        rho = (1 / (4 * alpha) + (0.5 - b) / 15) / 2
        lam = 15 * rho
        tau = (2 * lam + 1 - 1 / alpha) / 2
        assert alpha * rho > 0.25
        assert lam < tau / 2
        assert (1 - tau) / 2 > b
        out.append(f'alpha={alpha:g}: selection exponent={0.5-2*alpha*rho:.7g}; '
                   f'max-tail exponent={lam-tau/2:.7g}; '
                   f'deletion slack={(1-tau)/2-b:.7g}')
    # Recursive correlation identity, with vanishing a,b and z0 in a valid
    # correlation matrix; this is an algebra check, not random-design data.
    alpha = 9.0
    rho = (1 / (4 * alpha) + (0.5 - 1 / (2 * alpha)) / 15) / 2
    for exponent in [8, 16, 32, 64]:
        n = 10.0 ** exponent
        a = n ** (-alpha * rho)
        z0 = math.sqrt(math.log(n) / n)
        assert 1 + 2 * z0 * a * a - z0*z0 - 2*a*a > 0
        zu = (z0 - a*a)/(1-a*a)
        actual = n * abs(zu*zu-z0*z0)
        envelope = math.sqrt(n*math.log(n))*a*a+n*a**4
        assert actual <= 4 * envelope
        out.append(f'Recursive algebra n=1e{exponent}: error={actual:.8g}, '
                   f'rate envelope={envelope:.8g} (check: error <= 4 x envelope; ratio={actual/envelope:.3g}; only O(1) is used, L6 Sec. 4)')
    proof = ROOT / 'Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md'
    prefixes = {'LOC2': 'Theory_work/Wave2/W2-LOC2',
                'APP': 'Theory_work/Wave2/W2-APP',
                'GROW': 'Theory_work/Wave1C/C-GROW',
                'GEN': 'Theory_work/Wave1/W1-GEN'}
    refs = sorted(set(re.findall(r'((?:LOC2|APP|GROW|GEN)/[^`\s:]+):(\d+)',
                                 proof.read_text(encoding='utf-8'))))
    out.append('Citation existence and line text audit (human semantic check still required):')
    for path, num in refs:
        prefix, suffix = path.split('/', 1)
        full = ROOT / prefixes[prefix] / suffix
        lines = full.read_text(encoding='utf-8').splitlines()
        assert 1 <= int(num) <= len(lines), (path, num)
        out.append(f'{path}:{num}: {lines[int(num)-1]}')
    out.append('PASS: all local assertions; no independent review or asymptotic verification claimed.')
    result = '\n'.join(out) + '\n'
    (HERE / 'poly_out.txt').write_text(result, encoding='utf-8')
    print(result)


if __name__ == '__main__':
    main()
