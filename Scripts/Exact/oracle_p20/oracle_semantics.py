"""Independent deterministic Part-I decision/flag oracle; no fit implementation.

Authority: MASTER_Methodology_and_Plan.md §§I.1--I.3, I.5--I.6, I.9;
METHODOLOGY_v3.md §§2, 6.9--6.12 supplies background only. Part I governs.
Original variable indices in this PUBLIC interface are 0-based, possibly with
gaps for dropped columns. Convert Part I's 1-based indices by subtracting 1;
add 1 for method reports. Strict ordering is unchanged by this conversion.
No production/prototype imports; no numerical experiments on import.
"""
import math
import numpy as np

STATUSES = frozenset({"exact", "completed", "schedule_limit", "numerical_failure",
                      "resource_limit", "y_constant", "no_predictors", "invalid_input"})


def model(indices):
    s = tuple(indices)
    if any(not isinstance(j, (int, np.integer)) or j < 0 for j in s) or len(set(s)) != len(s):
        raise ValueError("distinct nonnegative integer original IDs required")
    return tuple(sorted(s))


def _scores(pairs):
    out = {}
    for s, f in pairs:
        s, f = model(s), float(f)
        if not math.isfinite(f):
            raise ValueError("scored models must have finite scores")
        if s in out and out[s] != f:
            raise ValueError("inconsistent repeated score for a model")
        out[s] = f
    if not out:
        raise ValueError("at least one scored model required")
    return out


def hpm(scored_pairs):
    """I.6 exact F ordering, then smaller size, then lexicographic original IDs."""
    scores = _scores(scored_pairs)
    selected = min(scores, key=lambda s: (-scores[s], len(s), s))
    return {"selected": selected, "score": scores[selected]}


def all_scored_hpm(events):
    """I.4/I.6: phase, mechanism, acceptance and cache retention never filter HPM.

    Events carry model, score and optional provenance. First occurrence supplies
    provenance. This API deliberately accepts rejected/evicted/table events.
    """
    events = list(events)
    best = hpm((e["model"], e["score"]) for e in events)
    first = next(e for e in events if model(e["model"]) == best["selected"])
    return dict(best, first_score_provenance=first.get("provenance"))


def near_ties(scored_pairs, p):
    """I.6 inclusive absolute 1e-9 window; truncation is the STORE predicate.

    Feed every scored model for a full independent store reconstruction. Display
    ties use size then lexicographic order; this does not reorder the HPM.
    """
    if not isinstance(p, (int, np.integer)) or p < 1:
        raise ValueError("retained p must be positive")
    scores = _scores(scored_pairs)
    best = hpm(scores.items())["score"]
    capacity = 40 * p + 1
    stored = sorted(scores, key=lambda s: (-scores[s], len(s), s))[:capacity]
    threshold = best - 1e-9
    return {"models": [s for s in stored if scores[s] >= threshold],
            "near_tie_truncated": len(stored) == capacity and scores[stored[-1]] >= threshold,
            "stored_count": len(stored), "capacity": capacity}


def pip05(pips, original_indices):
    """I.6, DP2 D2: strictly >0.5, with no K truncation."""
    ids = model(original_indices)
    if tuple(original_indices) != ids:
        raise ValueError("PIP axis requires sorted original IDs")
    pips = np.asarray(pips, dtype=float)
    if pips.shape != (len(ids),) or not np.all(np.isfinite(pips)) or np.any((pips < 0) | (pips > 1)):
        raise ValueError("finite PIPs in [0,1] aligned to IDs required")
    return tuple(j for j, probability in zip(ids, pips) if probability > 0.5)


def primary_pips(recordings):
    """I.6: array [4 final islands, 4 measured rounds, N particles, p].

    Values must be the immediately-pre-draw o_j, not inclusion indicators.
    Burn-in and calibration must be excluded by the parent adapter.
    """
    x = np.asarray(recordings, dtype=float)
    if (x.ndim != 4 or x.shape[0:2] != (4, 4) or min(x.shape[2:]) < 1
            or not np.all(np.isfinite(x)) or np.any((x < 0) | (x > 1))):
        raise ValueError("expected [4,4,N,p] finite conditional probabilities")
    islands = x.mean(axis=(1, 2))
    return {"islands": islands, "primary": islands.mean(axis=0)}


def feasible_neighbours(centre, original_indices, K):
    """I.6 full feasible single flips and included/excluded swaps, frozen centre."""
    ids = model(original_indices)
    s = model(centre)
    if not set(s) <= set(ids) or not 0 <= len(s) <= K <= len(ids):
        raise ValueError("infeasible model or cap")
    out = set()
    for j in ids:
        t = tuple(sorted(set(s) ^ {j}))
        if len(t) <= K:
            out.add(t)
    for j in s:
        for l in set(ids) - set(s):
            out.add(tuple(sorted((set(s) - {j}) | {l})))
    return tuple(sorted(out))


def local_certificate(selected, scans, enumeration_complete=False, status=None):
    """I.3/I.6: returned HPM itself must have a complete no-improvement scan.

    An equal-F HPM change to an unscanned model never inherits a certificate.
    Completed enumeration may certify directly; caller owns completeness proof.
    """
    if enumeration_complete and status == "exact":
        return True
    selected = model(selected)
    return any(model(scan["centre"]) == selected and scan["complete"]
               and not scan["has_strict_improvement"] for scan in scans)


def local_search(score, original_indices, K, ell, initial_scores):
    """I.6 reference search from current all-scored HPM; <=ell moves+extra scan.

    score is a pure callback on sorted original-ID tuples; initial_scores is an
    iterable of (model,F), containing all pre-search scored models for this test.
    Returned all_scores is audit evidence, not a production scoring ledger.
    """
    if not isinstance(ell, (int, np.integer)) or ell < 0:
        raise ValueError("nonnegative move budget required")
    ids = model(original_indices)
    scores = _scores(initial_scores)
    for s in scores:
        if not set(s) <= set(ids) or len(s) > K:
            raise ValueError("initial model infeasible")
    centre = hpm(scores.items())["selected"]
    initial_best = scores[centre]
    scans, path = [], [centre]
    local_limit = False
    for scan_number in range(ell + 1):
        neighbours = feasible_neighbours(centre, ids, K)
        for s in neighbours:
            f = float(score(s))
            if not math.isfinite(f) or (s in scores and scores[s] != f):
                raise ValueError("nonfinite or inconsistent score")
            scores[s] = f
        improving = [s for s in neighbours if scores[s] > scores[centre]]
        # Local candidate ties use lexicographic order ONLY (not HPM size order).
        next_centre = min(improving, key=lambda s: (-scores[s], s)) if improving else None
        scans.append({"centre": centre, "neighbours": neighbours, "complete": True,
                      "has_strict_improvement": bool(improving), "next": next_centre})
        if next_centre is None:
            break
        if scan_number == ell:
            local_limit = True
            break
        centre = next_centre
        path.append(centre)
    best = hpm(scores.items())
    return dict(best, path=path, scans=scans, local_limit=local_limit,
                local_certified=local_certificate(best["selected"], scans),
                E3=best["score"] > initial_best,
                all_scores=[(s, scores[s]) for s in sorted(scores)])


def diagnostic_checks(own_best, overall_best, log_evidence, before_local, after_local,
                      final_ess=(), N=None):
    """I.5: strict E1/E2/E3 and low-ESS thresholds; sample SD denominator 3."""
    own = np.asarray(own_best, float)
    z = np.asarray(log_evidence, float)
    scalars = np.asarray([overall_best, before_local, after_local], float)
    ess = np.asarray(final_ess, float)
    if (own.shape != (4,) or z.shape != (4,) or ess.ndim != 1
            or not all(np.all(np.isfinite(x)) for x in (own, z, scalars, ess))):
        raise ValueError("four finite island scores/evidences and finite scalar inputs required")
    if len(ess) and (N is None or not math.isfinite(N) or N <= 0 or np.any(ess < 0)):
        raise ValueError("positive N required for ESS checking")
    flags = {"E1": bool(np.any(overall_best - own > 1)),
             "E2": bool(z.std(ddof=1) > 1),
             "E3": bool(after_local > before_local),
             "low_empirical_ESS": bool(len(ess) and np.any(ess < 0.5 * N))}
    return dict(flags, checks_passed_final=not any(flags.values()),
                sample_sd_log_evidence=float(z.std(ddof=1)))


def calibration_checks(E1, E2, E3_any, forced_pilot_steps, grid_failed,
                       grid_unconverged, local_limit_any):
    """I.5: E1/E2 from last rebuild; E3/local_limit OR over tier searches.

    This consumes the already-aggregated values; never guesses an iteration.
    Selected-tier calibration pass excludes every listed trigger.
    """
    if not isinstance(forced_pilot_steps, (int, np.integer)) or forced_pilot_steps < 0:
        raise ValueError("nonnegative forced-step count required")
    trigger = any((E1, E2, E3_any, forced_pilot_steps > 0, grid_failed,
                   grid_unconverged, local_limit_any))
    return {"trigger": bool(trigger), "checks_passed_calibration": not trigger}


def heuristic_certificate(scored_pairs, eta, status, enumeration_complete):
    """I.2/I.9: strict numerical separation; this is explicitly heuristic.

    eta maps each enumerated model to its own nonnegative log-score error.
    Does not implement the scorer's eta formula; parent scorer oracle owns that.
    """
    scores = _scores(scored_pairs)
    errors = {model(s): float(e) for s, e in eta.items()}
    if set(errors) != set(scores) or any(not math.isfinite(e) or e < 0 for e in errors.values()):
        raise ValueError("one finite nonnegative eta per scored model required")
    selected = hpm(scores.items())["selected"]
    others = [s for s in scores if s != selected]
    upper = max((scores[s] + errors[s] for s in others), default=-math.inf)
    competitor = max((scores[s] for s in others), default=-math.inf)
    bound = scores[selected] - upper
    return {"global_certified": bool(status == "exact" and enumeration_complete
                                     and scores[selected] - errors[selected] > upper),
            "certificate_bound": bound, "margin": scores[selected] - competitor,
            "eta_selected": errors[selected],
            "label": "heuristic (not a validated interval bound)"}


def status_violations(result):
    """I.6 method-only contract; never invents benchmark role/converged mapping.

    Normalized parent adapter schema: status, selected, pips, log_evidence;
    unavailable values are None. A numerical-failure selected model requires
    incomplete=True. Optional global_certified, cut_group, partial.
    Resource-limit partial estimates require partial=True. Missing exact-branch
    cut_group is tolerated here; the parent must check complete fit-record fields.
    """
    issues = []
    for key in ("status", "selected", "pips", "log_evidence"):
        if key not in result:
            issues.append(f"missing {key}")
    if issues:
        return issues
    status = result["status"]
    if status not in STATUSES:
        return ["unknown status"]
    pips, z = result["pips"], result["log_evidence"]
    if status in {"exact", "completed"} and (pips is None or z is None):
        issues.append("completed method results require PIPs and evidence")
    if status in {"schedule_limit", "numerical_failure", "y_constant", "no_predictors", "invalid_input"}:
        if pips is not None or z is not None:
            issues.append("unavailable PIPs/evidence must be None")
    if status in {"y_constant", "no_predictors"} and tuple(result["selected"] or ()):
        issues.append("early constant/no-predictor result must select empty model")
    if status == "resource_limit" and (pips is not None or z is not None) and not result.get("partial", False):
        issues.append("resource-limit retained estimates must be labelled partial")
    if status == "numerical_failure" and result["selected"] is not None and not result.get("incomplete", False):
        issues.append("numerical-failure selected model must be labelled incomplete")
    if result.get("global_certified", False) and status != "exact":
        issues.append("global_certified requires exact status")
    if status == "exact" and result.get("cut_group") is not None:
        issues.append("exact branch cut_group must be NA/None")
    return issues
