"""Local falsification checks; Python 3.13, no writes outside this directory.

The large-p extremal-set check is NOT a greedy-path counterexample.
"""
from pathlib import Path
import itertools
import json
import math
import numpy as np
from scipy.special import log_ndtr

OUT = Path(__file__).resolve().parent
RB, B, D, A = .3, .4, .3, .7


def error(y, h, groups, kept):
    ng = int(groups.max()) + 1
    u = np.bincount(groups[kept], minlength=ng)
    sy = np.bincount(groups[kept], weights=y[kept], minlength=ng)
    phi = 1 / (D + B * u)
    var = 1 / (1 / RB + np.sum(u * phi))
    return float(var * (h / RB - np.sum(sy * phi))), float(var)


def exhaustive(rng):
    # Enumerate every subset and check the grouping/variance algebra.
    p, q = 15, 5
    groups = np.arange(p) // q
    G = int(groups.max()) + 1
    y = math.sqrt(B) * rng.normal(size=G)[groups] + math.sqrt(D) * rng.normal(size=p)
    h = math.sqrt(RB) * float(rng.normal())
    worst_var_ratio = 0.
    violations = []
    cp = math.e * (2**q - 1) * q
    L = math.log(math.log(p))
    for bits in itertools.product((False, True), repeat=p):
        kept = np.asarray(bits)
        k = int(kept.sum())
        if not k:
            continue
        ell = len(np.unique(groups[kept]))
        e, V = error(y, h, groups, kept)
        worst_var_ratio = max(worst_var_ratio, V * (ell / A + 1 / RB))
        bound = math.sqrt(2 * math.log(cp * p / k) + 2 * L + 4 * math.log(2))
        if abs(e) / math.sqrt(A) > bound:
            violations.append(dict(k=k, ell=ell, normalized_error=abs(e)/math.sqrt(A), bound=bound))
    return dict(p=p, subsets=2**p-1, max_variance_ratio=worst_var_ratio,
                lattice_event_violations=violations)


def extremal_set(rng, p, theta, alpha):
    # One predetermined coordinate per truth-free group is iid N(0,1).
    G = p // 5
    x = rng.normal(size=G-4)
    m = max(1, math.ceil(p**theta))
    chosen = np.partition(x, len(x)-m)[-m:]
    lam = 19 / 3
    anchor = float(rng.normal())
    t = -(chosen.sum()+anchor)/(m+lam)
    H = math.sqrt(2*math.log(p))
    logn = math.log(p)/alpha
    Hq = math.sqrt(2*math.log(32*p)+2*math.log(logn))
    k = m+4
    ratio = (Hq+abs(t))**2/(logn+2*math.log((2*p-k)/(k+1)))
    beta = 1-theta
    limiting_ratio = 2*alpha*(1+math.sqrt(beta))**2/(1+2*alpha*beta)
    return dict(p=p, theta=theta, alpha=alpha, m=m,
                normalized_field=abs(t)/H, predicted_limit=math.sqrt(beta),
                CC_ratio=ratio, predicted_CC_limit=limiting_ratio)


def exact_path(rng, p=2000):
    groups = np.arange(p)//5
    G = p//5
    y = math.sqrt(B)*rng.normal(size=G)[groups]+math.sqrt(D)*rng.normal(size=p)
    h = math.sqrt(RB)*float(rng.normal())
    truth = np.zeros(p, bool)
    truth[np.linspace(0, G-1, 6, dtype=int)[1:-1]*5] = True
    kept = np.ones(p, bool)
    x = y/math.sqrt(A)
    E, level_record = 0., 0.
    singleton_core_counterexample = None
    max_record_deficit = 0.
    birth_identity_error = 0.
    birth_count = 0
    singleton_crossings = 0
    largest_no_crossing_ratio = 0.
    cohort = None
    cohort_interval_failures = 0
    raw_exception_pair_failures = 0
    H = math.sqrt(2*math.log(p))
    max_field = 0.
    for step in range(p-4):
        ids = np.flatnonzero(kept)
        u = np.bincount(groups[ids], minlength=G)
        sy = np.bincount(groups[ids], weights=y[ids], minlength=G)
        phi = 1/(D+B*u)
        e, V = error(y, h, groups, kept)
        E = max(E, abs(e)/math.sqrt(A))
        max_field = max(max_field, abs(e)/math.sqrt(A)/H)
        z = y[ids]+e
        precision_g = (z-B*phi[groups[ids]]*(sy[groups[ids]]+u[groups[ids]]*e))/D
        diag = (1-B*phi[groups[ids]])/D-V*phi[groups[ids]]**2
        tau = precision_g/np.sqrt(diag)
        tau[truth[ids]] = np.inf
        pos = int(np.argmin(np.abs(tau)))
        j = int(ids[pos])
        level = abs(float(tau[pos]))
        level_record = max(level_record, level)
        members = ids[groups[ids] == groups[j]]
        if len(members) >= 2 and not truth[members].any() and abs(x[j]) > E:
            signed_mates = np.sign(x[j])*x[members[members != j]]
            pair_condition = (signed_mates >= abs(x[j])) | (signed_mates <= 2*E-abs(x[j]))
            raw_exception_pair_failures += int(not np.any(pair_condition))
        if cohort is None and len(ids) <= p//5:
            cohort = kept & (u[groups] == 1) & ~truth
        if cohort is not None:
            ck = np.flatnonzero(cohort & kept)
            cd = np.flatnonzero(cohort & ~kept)
            center = -e/math.sqrt(A)
            lo = np.max(x[ck][x[ck] <= center], initial=-np.inf)
            hi = np.min(x[ck][x[ck] > center], initial=np.inf)
            if np.any((x[cd] <= lo) | (x[cd] >= hi)):
                cohort_interval_failures += 1
        max_record_deficit = max(max_record_deficit, (level_record-level)/H)
        # A literal singleton-coordinate core can lose members as multimember deletions.
        if abs(x[j]) > level_record+E and u[groups[j]] > 1 and singleton_core_counterexample is None:
            singleton_core_counterexample = dict(step=step, k=len(ids), j=j, X=float(x[j]),
                                                 level_record=level_record, E=E,
                                                 members=y[ids[groups[ids]==groups[j]]].tolist(),
                                                 field=e/math.sqrt(A))
        if u[groups[j]] == 2:
            l = int(ids[(groups[ids]==groups[j]) & (ids!=j)][0])
            c = D/A
            s = math.sqrt(D*(D+2*B)/A)
            Aj = (y[j]-(B/A)*y[l])/s
            d1 = c/s
            predicted = (Aj+d1*e)/math.sqrt(1-d1*d1*V)
            birth_identity_error = max(birth_identity_error, abs(float(tau[pos])-predicted))
            birth_count += 1
        singles = ids[(u[groups[ids]] == 1) & (ids != j) & ~truth[ids]]
        oldt = e/math.sqrt(A)
        kept[j] = False
        enew, _ = error(y, h, groups, kept)
        newt = enew/math.sqrt(A)
        singleton_crossings += int(np.count_nonzero((x[singles]+oldt)*(x[singles]+newt) <= 0))
        if len(singles):
            largest_no_crossing_ratio = max(largest_no_crossing_ratio,
                                            abs(newt-oldt)/float(np.min(np.abs(x[singles]+oldt))))
    return dict(p=p, max_field_over_H=max_field,
                max_deletion_level_record_deficit_over_H=max_record_deficit,
                singleton_coordinate_core_counterexample=singleton_core_counterexample,
                birth_count=birth_count, birth_identity_max_error=birth_identity_error,
                singleton_crossings=singleton_crossings,
                largest_singleton_drift_distance_ratio=largest_no_crossing_ratio,
                cohort_interval_failures=cohort_interval_failures,
                raw_exception_pair_failures=raw_exception_pair_failures)


def analytic_witness():
    # A certified tail-count calculation at an enormous p, not a simulated path.
    # Conditional on |B_anchor|<=50, any m qualifying designated coordinates work.
    logp, theta, alpha, threshold, lam = 10000., .01, .17, .99, 19/3
    logm = theta*logp
    H = math.sqrt(2*logp)
    log_mu = logp-math.log(5)+float(log_ndtr(-threshold*H))
    Hq = math.sqrt(2*(logp+math.log(32))+2*math.log(logp/alpha))
    field_lower = (threshold*H-50*math.exp(-logm))/(1+lam*math.exp(-logm))
    denominator_upper = logp/alpha+2*(math.log(2)+logp-logm)
    return dict(log_p=logp, theta=theta, alpha=alpha, threshold=threshold,
                log_expected_exceedances=log_mu, log_selected_count=logm,
                log_expected_count_over_selected=log_mu-logm,
                anchor_failure_bound=2*math.exp(-50**2/(2*lam)),
                CC_ratio_lower_bound=(Hq+field_lower)**2/denominator_upper,
                caveat='All-set witness; neither a realized sample nor a greedy-path counterexample.')


def band_scalar_checks(rng):
    a0, w = .8995, (1-.8995)/2
    violations = 0
    worst_neighbour = 0.
    for _ in range(200):
        lam = (217/57, 19/3)[int(rng.integers(2))]
        xdata = rng.uniform(a0, 1., 400)*np.tile((-1., 1.), 200)
        anchor = float(rng.uniform(-.001, .001))
        kept = np.ones(400, bool)
        sm = float(xdata.sum())
        for m in range(400, 0, -1):
            ids = np.flatnonzero(kept)
            center = (sm+anchor)/(m+lam)
            f = w+(1+w)/(m+lam)
            violations += int(abs(center) > f+1e-12)
            neigh = (sm-xdata[ids]+anchor)/(m-1+lam)
            if m >= 2:
                c = w+2*(1+w)/(m-1+lam)
                violations += int(np.max(np.abs(neigh)) > c+1e-12)
            worst_neighbour = max(worst_neighbour, float(np.max(np.abs(neigh))))
            j = int(ids[np.argmin(np.abs(xdata[ids]-center))])
            kept[j] = False
            sm -= float(xdata[j])
    return dict(paths=200, violations=violations, max_neighbour=worst_neighbour)


def matrix_checks(rng):
    largest_tau_error = 0.
    largest_update_error = 0.
    for _ in range(1200):
        p = 15
        groups = np.arange(p)//5
        y = math.sqrt(B)*rng.normal(size=3)[groups]+math.sqrt(D)*rng.normal(size=p)
        h = math.sqrt(RB)*float(rng.normal())
        kept = rng.random(p) < .6
        if not kept.any():
            kept[0] = True
        ids = np.flatnonzero(kept)
        Sigma = RB*np.ones((len(ids), len(ids)))+B*(groups[ids, None]==groups[None, ids])+D*np.eye(len(ids))
        Q = np.linalg.inv(Sigma)
        dense_tau = Q@(y[ids]+h)/np.sqrt(np.diag(Q))
        e, V = error(y, h, groups, kept)
        for pos, j in enumerate(ids):
            mates = ids[(groups[ids]==groups[j]) & (ids!=j)]
            u = len(mates)
            c = D/(D+B*u)
            s = math.sqrt(D*(D+B*(u+1))/(D+B*u))
            Aj = (y[j]-B*float(y[mates].sum())/(D+B*u))/s
            kappa = c/s
            tau = (Aj+kappa*e)/math.sqrt(1-kappa*kappa*V)
            largest_tau_error = max(largest_tau_error, abs(tau-dense_tau[pos]))
            retained = kept.copy()
            retained[j] = False
            enew, _ = error(y, h, groups, retained)
            update = kappa*V*tau/math.sqrt(1-kappa*kappa*V)
            largest_update_error = max(largest_update_error, abs(enew-e-update))
    return dict(states=1200, max_tau_error=largest_tau_error, max_update_error=largest_update_error)


def main():
    rng = np.random.default_rng(2026110902)
    ex = exhaustive(rng)
    paths = [exact_path(rng) for _ in range(12)]
    extreme = [extremal_set(rng, p, theta, .17) for p in (10000, 100000, 1000000)
               for theta in (.01, .06, .1)]
    alpha = .17
    theta_min = 1-((1/(2*alpha)-1)/2)**2
    constants = dict(alpha=alpha, theta_infimum=theta_min,
                     theta_point_one_alpha_cutoff=1/(2+4*math.sqrt(.9)),
                     theta_point_zero_six_alpha_cutoff=1/(2+4*math.sqrt(.94)),
                     pair_shift_coefficient=math.sqrt(3/11),
                     endpoint_250_ratio=.34/1.34*(1+250/(250+217/57))**2)
    witness = analytic_witness()
    band = band_scalar_checks(rng)
    matrix = matrix_checks(rng)
    raw = dict(constants=constants, exhaustive=ex, paths=paths, extremal_sets=extreme,
               analytic_all_set_witness=witness, band_scalar=band, dense_matrix_checks=matrix)
    (OUT/'numerics_raw.json').write_text(json.dumps(raw, indent=2), encoding='utf-8')
    summary = dict(constants=constants, exhaustive=ex,
                   exact_paths=len(paths),
                   path_birth_formula_max_error=max(z['birth_identity_max_error'] for z in paths),
                   path_max_level_deficit=max(z['max_deletion_level_record_deficit_over_H'] for z in paths),
                   singleton_crossings=sum(z['singleton_crossings'] for z in paths),
                   cohort_interval_failures=sum(z['cohort_interval_failures'] for z in paths),
                   raw_exception_pair_failures=sum(z['raw_exception_pair_failures'] for z in paths),
                   largest_singleton_drift_distance_ratio=max(z['largest_singleton_drift_distance_ratio'] for z in paths),
                   literal_core_failures=sum(z['singleton_coordinate_core_counterexample'] is not None for z in paths),
                   first_literal_core_counterexample=next(z['singleton_coordinate_core_counterexample'] for z in paths
                                                         if z['singleton_coordinate_core_counterexample'] is not None),
                   extremal_sets=extreme, analytic_all_set_witness=witness, band_scalar=band,
                   dense_matrix_checks=matrix)
    (OUT/'numerics_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
