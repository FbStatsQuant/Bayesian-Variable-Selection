"""Adversarial design-level checks of L8; Python standard library only.

Run: python -B Theory_work/Wave1C/C-PACK/numerics/item3_L8_falsify.py
No files are written by this script. Redirect stdout to the companion _out.txt.
Twelve independent seeds, no noise simulations, no external data/dependencies.

All calculations use the exact Gram formulas for the Euclidean projections in
STATEMENT.md:32-35,67-75. Any SPD correlation matrix R of order p<n has a
centered realization X=sqrt(n-1)*Q*chol(R).T with Q.T Q=I and Q.T 1=0.
Consequently Gram calculations describe actual standardized fixed designs.
The randomized designs have four recovered blocks of size 4 (p=16, B=4):
all within-block absolute correlations exceed all between-block correlations.
The deterministic examples likewise have blocks recovered by the actual rule.
This tests C1-prime/L8, not all H0/H1 or any stochastic start-mode theorem.
"""

import itertools
import math
import random


def dot(x, y):
    return math.fsum(a * b for a, b in zip(x, y))


def mv(a, x):
    return [dot(row, x) for row in a]


def sub(a, ids, js=None):
    js = ids if js is None else js
    return [[a[i][j] for j in js] for i in ids]


def chol(a):
    """Cholesky, also used to certify a stated eigenvalue floor via R-floor*I."""
    m = len(a)
    out = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1):
            z = a[i][j] - dot(out[i][:j], out[j][:j])
            if i == j:
                if z <= 0:
                    raise ValueError("Not positive definite")
                out[i][j] = math.sqrt(z)
            else:
                out[i][j] = z / out[j][j]
    return out


def solve(a, b):
    if not b:
        return []
    low = chol(a)
    m = len(b)
    y = [0.0] * m
    x = [0.0] * m
    for i in range(m):
        y[i] = (b[i] - dot(low[i][:i], y[:i])) / low[i][i]
    for i in reversed(range(m)):
        x[i] = (y[i] - math.fsum(low[j][i] * x[j] for j in range(i + 1, m))) / low[i][i]
    return x


def subsets(ids):
    for k in range(len(ids) + 1):
        yield from itertools.combinations(ids, k)


def projection(r, d, ids):
    """||P_ids mu||^2/(n-1), where d=X.T mu/(n-1)."""
    ds = [d[i] for i in ids]
    return dot(ds, solve(sub(r, ids), ds))


def check(n, r, blocks, gamma, large, eta, mn, energy_m, phi2, eps0):
    sigma2 = 1.0
    logn = math.log(n)
    p = len(r)
    # Specify each block's regression, then construct the single common mean.
    d = [0.0] * p
    for b, ids in enumerate(blocks):
        for i, z in zip(ids, mv(sub(r, ids), gamma[b])):
            d[i] = z
    theta = solve(r, d)
    mu2_scaled = dot(d, theta)
    energy_ratio = (n - 1) * mu2_scaled / (energy_m * n)
    assert energy_ratio <= 1 + 1e-10, energy_ratio
    # Stronger than H2a: certify the normalized FULL Gram floor, hence all subsets.
    chol([[r[i][j] - (phi2 if i == j else 0.0) for j in range(p)] for i in range(p)])
    star = set().union(*map(set, large))
    h = math.sqrt(2 * (1 + eps0) * logn)  # A=1
    max_e = {}
    vis_ratios = []
    small_ratios = []
    leakage_ratios = []
    recovery_error = 0.0
    root_margin = math.sqrt(eta * logn) + math.sqrt(mn * (1 + 2 * energy_m) * logn)
    margin_ratios = []
    for b, ids in enumerate(blocks):
        rr = sub(r, ids)
        recovered = solve(rr, [d[i] for i in ids])
        recovery_error = max(recovery_error, max(abs(x-y) for x, y in zip(recovered, gamma[b])))
        ss = [0.0 if i in large[b] else gamma[b][k] for k, i in enumerate(ids)]
        small2 = (n - 1) * dot(ss, mv(rr, ss))
        if eta:
            small_ratios.append(small2 / (eta * logn))
            assert small_ratios[-1] <= 1 + 1e-9
        else:
            assert small2 == 0
        if large[b]:
            mincoeff = min(abs(gamma[b][ids.index(i)]) for i in large[b])
            margin_ratios.append(math.sqrt((n - 1) * phi2) * mincoeff / root_margin)
            assert margin_ratios[-1] >= 1 - 1e-9
        for t in subsets(ids):
            pt = projection(r, d, t)
            if eta == 0:
                # Exact certificate (a): equality of residual energies iff support included.
                full = projection(r, d, ids)
                if set(large[b]).issubset(t):
                    assert abs(full - pt) <= 1e-11 * max(1.0, full)
                else:
                    assert full > pt + 1e-12
            # Exact g = (n-1)*(||P_(t union U*) mu||^2-||P_t mu||^2)/(n-1).
            if not set(large[b]).issubset(t):
                comp = sorted(set(t).union(large[b]))
                gain = (n - 1) * (projection(r, d, comp) - pt)
                v_t = sigma2 + max(0.0, mu2_scaled - pt)
                vis_ratios.append(gain / (mn * v_t * logn))
                missing2 = math.fsum(gamma[b][ids.index(i)]**2 for i in large[b] if i not in t)
                geom_lower = math.sqrt((n-1) * phi2 * missing2) - math.sqrt(small2)
                if geom_lower > 0:
                    assert math.sqrt(max(0.0, gain)) >= geom_lower - 1e-8
            if not set(large[b]).issubset(t):
                continue
            for ell in ids:
                if ell in t or ell in star:
                    continue
                # Exact u_(t,ell).T mu via the partial covariance and variance.
                rtell = [r[i][ell] for i in t]
                coeff = solve(sub(r, t), rtell)
                partial_cov = d[ell] - dot(coeff, [d[i] for i in t])
                partial_var = r[ell][ell] - dot(rtell, coeff)
                delta2 = (n - 1) * partial_cov**2 / partial_var
                delta = math.sqrt(delta2)
                delta_t = max(0.0, mu2_scaled - pt)
                v_t = sigma2 + delta_t
                # Suppress roundoff only when theoretical leakage is identically zero.
                if eta == 0 and abs(partial_cov) < 1e-12:
                    delta2 = delta = 0.0
                if delta2 == 0:
                    exponent = 0.0
                else:
                    assert delta_t > 0
                    exponent = min(delta2 / (2 * delta_t), delta2 / (2 * v_t) + delta * h / v_t)
                max_e[ell] = max(max_e.get(ell, 0.0), exponent)
                if eta:
                    leakage_ratios.append(delta2 / (eta * logn))
                else:
                    assert delta2 == 0
    avg = math.fsum(math.exp(x) for x in max_e.values()) / (p - len(star)) if p > len(star) else 0
    c_eta = eta / 2 + math.sqrt(2 * eta * (1 + eps0))
    kappa = (0.5 - c_eta) / 2
    assert kappa > 0
    avg_ratio = avg / n**(0.5 - kappa) if avg else 0
    assert min(vis_ratios, default=math.inf) >= 1 - 1e-8
    assert max(leakage_ratios, default=0) <= 1 + 1e-8
    assert avg_ratio <= 1 + 1e-8
    return {
        "vis_min": min(vis_ratios, default=math.inf),
        "nl_max": max(leakage_ratios, default=0),
        "small_max": max(small_ratios, default=0),
        "root_margin_min": min(margin_ratios, default=math.inf),
        "avg_ratio": avg_ratio,
        "energy_ratio": energy_ratio,
        "recovery_error": recovery_error,
        "vis_checks": len(vis_ratios),
        "leak_checks": sum(1 for ids, ls in zip(blocks, large) for t in subsets(ids)
                           if set(ls).issubset(t) for ell in ids if ell not in t and ell not in star),
    }


def randomized(seed, n, eta, margin_factor):
    rng = random.Random(seed)
    p = 16
    blocks = [list(range(4*b, 4*b+4)) for b in range(4)]
    r = [[0.0] * p for _ in range(p)]
    for ids in blocks:
        v = [[rng.gauss(0, 1) for _ in range(12)] for _ in ids]
        v = [[a / math.sqrt(dot(z, z)) for a in z] for z in v]
        for i, ii in enumerate(ids):
            for j, jj in enumerate(ids):
                r[ii][jj] = 0.55 * (i == j) + 0.4 + 0.05 * dot(v[i], v[j])
    signs = [rng.choice([-1, 1]) for _ in range(p)]
    r = [[0.97 * r[i][j] + 0.03 * signs[i] * signs[j] for j in range(p)] for i in range(p)]
    # Recovery by complete linkage, size cut, next-fit is forced by this gap.
    within = min(abs(r[i][j]) for ids in blocks for i in ids for j in ids if i != j)
    between = max(abs(r[i][j]) for b, ids in enumerate(blocks) for c, js in enumerate(blocks)
                  if b != c for i in ids for j in js)
    assert within > between and math.isqrt(p) == 4
    large = [[0], [4, 5], [], [12]]
    phi2, energy_m, mn = 0.5, 2.0, math.log(n)
    threshold = (math.sqrt(eta * math.log(n)) + math.sqrt(mn * (1+2*energy_m)*math.log(n))) / math.sqrt((n-1)*phi2)
    gamma = []
    for b, ids in enumerate(blocks):
        ss = [0 if i in large[b] or eta == 0 else rng.uniform(-1, 1) for i in ids]
        if eta:
            norm = math.sqrt((n-1) * dot(ss, mv(sub(r, ids), ss)))
            ss = [z * math.sqrt(eta * math.log(n)) / norm for z in ss]
        gamma.append([rng.choice([-1, 1]) * threshold * margin_factor if i in large[b] else ss[k]
                      for k, i in enumerate(ids)])
    return check(n, r, blocks, gamma, large, eta, mn, energy_m, phi2, eps0=0.001)


def fixed_epsilon_counterexample(n):
    # Actual two blocks of size 2: within r=.5, between 0, p=4 and B=2.
    eta, phi2, energy_m, mn = 0.1, 0.49, 1.0, math.log(n)
    strong = (math.sqrt(eta * math.log(n)) + math.sqrt(3 * mn * math.log(n))) / math.sqrt((n-1)*phi2)
    weak = math.sqrt(eta * math.log(n) / (n-1))
    r = [[1, .5, 0, 0], [.5, 1, 0, 0], [0, 0, 1, .5], [0, 0, .5, 1]]
    blocks, gamma, large = [[0, 1], [2, 3]], [[strong, 0], [weak, 0]], [[0], []]
    # Valid certificate, NL at the sufficiently small epsilon0.
    checked = check(n, r, blocks, gamma, large, eta, mn, energy_m, phi2=phi2, eps0=.001)
    # Then use precisely the same design with epsilon0=1: T=empty, ell=2.
    delta2 = eta * math.log(n)
    delta_t = strong**2 + weak**2
    vt = 1 + delta_t
    e = min(delta2 / (2 * delta_t), delta2 / (2 * vt) + math.sqrt(delta2) * math.sqrt(4 * math.log(n)) / vt)
    # One term suffices: true average >= exp(E)/3, since p-s*=3.
    lower_ratio = math.exp(e) / (3 * math.sqrt(n))
    return checked, e / math.log(n), lower_ratio


def example_checks():
    # Independent Gram algebra check of L8.3 finite-core cancellation, split/joint.
    r = .6
    gram = [[1, r, 0], [r, 1, 0], [0, 0, 1]]
    theta = [1, -r, 0]
    d = mv(gram, theta)
    split1, split2 = solve([[1]], [d[0]]), solve([[1]], [d[1]])
    joint = solve(sub(gram, [0, 1]), d[:2])
    assert abs(split1[0] - (1-r*r)) < 1e-14 and abs(split2[0]) < 1e-14
    assert max(abs(a-b) for a, b in zip(joint, theta[:2])) < 1e-14
    print("Finite-core r=.6: split gamma1=", split1, "gamma2=", split2, "joint gamma=", joint)
    # W: inverse of the 9x9 .25 equicorrelation matrix sends eps*1 to eps/3*1.
    q = 9
    rc = [[1.0 if i == j else .25 for j in range(q)] for i in range(q)]
    eps = .001
    z = solve(rc, [eps]*q)
    actual = [1+z[0]] + z[1:]
    assert max(abs(x - eps/3) for x in z) < 1e-14
    small = [0] + z[1:]
    print("W normalized theta=1: gamma_active=", actual[0], "off_active=", z[1],
          "small energy/(n-1)=", dot(small, mv(rc, small)))
    print("W stale L6(c): gammaL=theta*e_j leaves small coefficient eps/3 on j; not disjoint.")


def main():
    print("L8 falsification: design-level exact Gram projections, standard library, 12 seeds.")
    print("A=1; sigma^2=1; M_n=log(n); random M=2, phi0^2=.5; epsilon0=.001.")
    print("Exact and small-part-boundary cases, root margins 1 and 1+1e-10.")
    totals = {"vis_checks": 0, "leak_checks": 0}
    all_results = []
    for n in [4096, 16384, 65536]:
        results = []
        for seed in range(12):
            for eta, margin in [(0., 1.), (.1, 1.), (.1, 1+1e-10)]:
                result = randomized(seed, n, eta, margin)
                results.append(result)
                all_results.append(result)
                for name in totals:
                    totals[name] += result[name]
        print("n=%d designs=%d min_VIS_ratio=%.9f max_NL_eta_ratio=%.9f max_avg_ratio=%.9f max_energy_ratio=%.9f" %
              (n, len(results), min(z["vis_min"] for z in results), max(z["nl_max"] for z in results),
               max(z["avg_ratio"] for z in results), max(z["energy_ratio"] for z in results)))
    print("Total random designs:", len(all_results), "checks:", totals)
    print("Min root margin ratio=%.12f; max small-part ratio=%.12f; max regression recovery error=%.3g" %
          (min(z["root_margin_min"] for z in all_results), max(z["small_max"] for z in all_results),
           max(z["recovery_error"] for z in all_results)))
    print("Randomized falsifications of the correctly quantified certificate: 0.")
    eta = .1
    c = eta/2 + math.sqrt(2*eta*(1+.001))
    print("eta=.1 epsilon0=.001: c_eta=%.12f, kappa=%.12f; valid avg upper bound n^c_eta." % (c, (.5-c)/2))
    print("Fixed-epsilon diagnostic: eta=.1 satisfies eta<(sqrt(3)-sqrt(2))^2=%.12f." % (math.sqrt(3)-math.sqrt(2))**2)
    print("Same valid certificate with epsilon0=1: c_eta limit=.05+sqrt(.4)=%.12f > .5." % (.05+math.sqrt(.4)))
    for n in [10**4, 10**6, 10**9]:
        checked, exp_ratio, lower = fixed_epsilon_counterexample(n)
        print("n=%d epsilon0=1 E/log(n)=%.9f avg/sqrt(n)>=%.9f certificate_energy_ratio=%.9f" %
              (n, exp_ratio, lower, checked["energy_ratio"]))
    print("A lower ratio >1 violates NL_avg for EVERY kappa>0 at that n.")
    print("As n grows this lower ratio diverges: a counterexample to keeping arbitrary epsilon0 fixed,")
    print("not to the existential sufficiently-small-epsilon0 implication acknowledged in L2:62.")
    example_checks()
    print("PASS: all assertions; 12 distinct random seeds; no noise and no start-score simulation.")


if __name__ == "__main__":
    main()
