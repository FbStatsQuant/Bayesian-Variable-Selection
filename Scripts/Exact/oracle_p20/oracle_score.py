"""Independent SMC-BVS v3 scoring oracle. No production/prototype source used.

Authority: MASTER_Methodology_and_Plan.md Part I, especially I.1 (preparation),
I.2 (target/numerics), I.3 (enumeration), I.6 (strict HPM order/evidence).
Supporting method: METHODOLOGY_v3.md sections 3--5, 6.2, 6.10, 6.12--6.13.
Master SHA256: 7d77dddb968135d86a6b6431a7a3e04e122eb0c09f5ec9a6a8329e9a20757b6e
M SHA256: 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c

PUBLIC INDEX CONVENTION: every S uses ZERO-based ORIGINAL input columns.
Convert a specification/R index j to j-1. Prepared X/G/z use retained order;
``original_indices`` maps that order back to the public indices. Dropped
columns are rejected in models. Never pass retained positions as original IDs.
Construction prepares data only; it runs no enumeration or tests.
"""

from __future__ import annotations

import itertools
import math
import numbers
from fractions import Fraction
from typing import Iterable

import mpmath as mp
import numpy as np
from scipy import linalg, special


A0 = B0 = 0.01
SOURCE_HASHES = {
    "master": "7d77dddb968135d86a6b6431a7a3e04e122eb0c09f5ec9a6a8329e9a20757b6e",
    "method_v3": "93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c",
}


class NumericalFailure(RuntimeError):
    """Master I.2: failure is explicit, never an artificial minus-infinity."""


def _numeric_inputs(X, y):
    """I.1: preserve sequence scalars BEFORE NumPy infers a common dtype.

    Existing typed i/u/f arrays retain their dtype and routes. For sequences,
    object storage is deliberate: [2**53, 2**53+1, float(2**53)] must not
    become three equal doubles. Only integer/floating scalars are accepted;
    this is not permission for strings, complex, bool or arbitrary objects.
    """
    try:
        def preserve(value):
            if isinstance(value, np.ndarray):
                if value.dtype.kind not in "iuf":
                    raise ValueError("real numeric arrays required")
                return np.array(value, copy=True)
            result = np.array(value, dtype=object)
            for v in result.flat:
                if (isinstance(v, (bool, np.bool_))
                        or not isinstance(v, (numbers.Integral, float, np.floating))):
                    raise ValueError("integer or floating numeric scalars required")
                if not isinstance(v, numbers.Integral) and not np.isfinite(v):
                    raise ValueError("all input entries must be finite")
            return result

        a, b = preserve(X), preserve(y)
        if a.ndim != 2 or b.ndim != 1 or a.shape[0] != b.size:
            raise ValueError("X must be n by p and y length n")
        if a.shape[0] < 3 or a.shape[1] < 1:
            raise ValueError("n >= 3 and at least one input predictor required")
        for array in (a, b):
            if array.dtype.kind != "O" and not np.all(np.isfinite(array)):
                raise ValueError("all input entries must be finite")
        return a, b
    except (TypeError, OverflowError) as exc:
        raise ValueError("invalid real numeric input") from exc


def _number_ratio(value):
    """Exact equality/conversion key, including mixed NumPy scalar types."""
    if isinstance(value, numbers.Integral):
        return int(value), 1
    numerator, denominator = value.as_integer_ratio()
    return int(numerator), int(denominator)


def _constant(values):
    # Homogeneous typed arrays keep their previous exact equality route.
    if values.dtype.kind != "O":
        return bool(np.all(values == values[0]))
    first = _number_ratio(values[0])
    return all(_number_ratio(v) == first for v in values[1:])


def _retained_columns(raw):
    if raw.dtype.kind != "O":
        return np.any(raw != raw[0, :], axis=0)
    return np.array([not _constant(raw[:, j]) for j in range(raw.shape[1])])


def _mp_number(value):
    """Exact numeric ingestion for I.1, with no integer -> float detour.

    Integer scalars enter as Python ints; floating scalars enter through their
    exact binary rational. The active MP precision controls later arithmetic.
    """
    numerator, denominator = _number_ratio(value)
    return mp.mpf(numerator) / denominator


def _standardize(a):
    """Master I.1.4 / M4: double route plus recorded MP target fallback.

    This independent mathematical oracle is not a production bit-identity
    clone. Keep ordinary maxabs/mean/sample-SD double arithmetic, but reject
    its route if conversion is lossy or the conservative roundoff/SD estimate
    exceeds 1e-13. This is a precision guard, NEVER a constant/drop threshold.
    Fallback repeats the specified maxabs sequence at 80 decimal digits and
    rounds only the final working vector/map to double. A separate map-only
    fallback preserves the working route. Unusable raw mean/SD doubles become
    None; availability flags, decimal strings and factors explain the map.

    ``*_float64_available`` checks finite range and, on the MP map route,
    relative rounding error <= 8*eps (zero mean is valid only if truly zero).
    ``raw_map_float64_available`` also checks mean rounding relative to SD
    against 1e-13. These are numerical heuristics, not exact reconstruction
    guarantees. ``high_precision`` stores 80-digit decimal maps by retained
    position; ``factored`` gives raw=max_abs*(working*sd_scaled+mean_scaled).
    Use MP arithmetic on decimal factors, not float() on a raw SD string.
    """
    vector = a.ndim == 1
    raw = a[:, None] if vector else a
    n, p = raw.shape
    prepared = np.empty((n, p), dtype=float)
    fields = ("max_abs", "mean_scaled", "sd_scaled", "mean", "sd", "log_sd")
    record = {key: np.empty(p, dtype=float) for key in fields}
    routes, reasons, precisions, high_precision = [], [], [], []
    map_routes, map_reasons, factored = [], [], []
    availability = {key: [] for key in ("mean_float64_available", "sd_float64_available",
                                       "raw_map_float64_available")}
    map_issues = []
    for j in range(p):
        values = raw[:, j]
        why = []
        with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
            double = np.asarray(values, dtype=np.float64)
            # Compare exact rational keys, since mixed NumPy scalar comparisons
            # can themselves coerce large integers to floating point.
            for v, d in zip(values, double):
                if math.isfinite(float(d)) and _number_ratio(v) != _number_ratio(d):
                    reason = ("integer_float64_conversion" if isinstance(v, numbers.Integral)
                              else "floating_float64_conversion")
                    if reason not in why:
                        why.append(reason)
            if not np.all(np.isfinite(double)):
                why.append("nonfinite_float64_conversion")
            maximum = np.max(np.abs(double))
            scaled = double / maximum
            mean_scaled = np.mean(scaled)
            centered = scaled - mean_scaled
            sd_scaled = np.sqrt(np.sum(centered * centered) / (n - 1))
            if not math.isfinite(float(sd_scaled)) or sd_scaled <= 0:
                why.append("degenerate_float64_centering")
            elif 8 * np.finfo(float).eps / sd_scaled > 1e-13:
                why.append("centering_relative_accuracy")
            stats = (maximum, mean_scaled, sd_scaled, maximum * mean_scaled,
                     maximum * sd_scaled, np.log(maximum) + np.log(sd_scaled))
        # Multiplying factors can overflow or underflow even when preparation
        # is well-conditioned. Inspect subnormals too: nonzero is not enough
        # to promise a useful relative-accuracy raw scale (e.g. 3*t/2 -> 2*t).
        map_why = []
        for key, product, factor in (("mean", stats[3], mean_scaled),
                                     ("sd", stats[4], sd_scaled)):
            if (not math.isfinite(float(product))
                    or (product == 0 and factor != 0)
                    or 0 < abs(product) < np.finfo(float).tiny):
                map_why.append(key + "_product_range")
        # A double zero mean can also hide a nonzero exact sum through
        # cancellation before the product (e.g. [t, 0, 1, -1], t=2**-1074).
        exact_sum = sum((Fraction(*_number_ratio(v)) for v in values), Fraction())
        if mean_scaled == 0 and exact_sum != 0:
            map_why.append("mean_cancellation_to_zero")
        precise = None
        issues = []
        if why or map_why:
            # I.1.4's exact target, evaluated at higher precision; no dropping,
            # recentering shortcut, target change or score tolerance relaxation.
            with mp.workdps(80):
                v = [_mp_number(t) for t in values]
                maximum_mp = max(abs(t) for t in v)
                scaled_mp = [t / maximum_mp for t in v]
                mean_mp = mp.fsum(scaled_mp) / n
                centered_mp = [t - mean_mp for t in scaled_mp]
                sd_mp = mp.sqrt(mp.fsum(t*t for t in centered_mp) / (n - 1))
                if not mp.isfinite(sd_mp) or sd_mp <= 0:
                    raise NumericalFailure("nonconstant MP preparation failed")
                if why:
                    prepared[:, j] = [float(t / sd_mp) for t in centered_mp]
                # Report the raw map from raw MP moments, avoiding another
                # loss of significant digits through nearly equal scaled
                # values. MP has no binary64 raw-square range restriction.
                # This does not change the maxabs working preparation above.
                # Finite-precision fsum can lose a tiny residual even when
                # large positive/negative terms cancel. Sum supplied binary
                # rationals exactly, then round the final mean to MP once.
                exact_mean = exact_sum / n
                raw_mean_mp = mp.mpf(exact_mean.numerator) / exact_mean.denominator
                raw_sd_mp = mp.sqrt(mp.fsum((t-raw_mean_mp)**2 for t in v) / (n-1))
                if not mp.isfinite(raw_sd_mp) or raw_sd_mp <= 0:
                    raise NumericalFailure("nonconstant MP raw map failed")
                stats_mp = (maximum_mp, raw_mean_mp/maximum_mp, raw_sd_mp/maximum_mp,
                            raw_mean_mp, raw_sd_mp, mp.log(raw_sd_mp))
                stats = tuple(float(t) for t in stats_mp)
                precise = {"retained_position": j, "dps": 80,
                           "scope": "preparation_and_map" if why else "map_only",
                           **{key: mp.nstr(t, 80) for key, t in zip(fields, stats_mp)}}
                high_precision.append(precise)
                usable = {}
                for key, value, rounded in (("mean", stats_mp[3], stats[3]),
                                             ("sd", stats_mp[4], stats[4])):
                    if not math.isfinite(rounded):
                        usable[key] = False
                        issues.append(key + "_overflow")
                    elif value != 0 and rounded == 0:
                        usable[key] = False
                        issues.append(key + "_underflow_to_zero")
                    elif value != 0 and abs((_mp_number(rounded)-value)/value) > mp.mpf(8)*mp.mpf(2)**-52:
                        usable[key] = False
                        issues.append(key + "_float64_relative_accuracy")
                    else:
                        usable[key] = True
                raw_usable = usable["mean"] and usable["sd"]
                if raw_usable and abs(_mp_number(stats[3])-stats_mp[3])/stats_mp[4] > mp.mpf("1e-13"):
                    raw_usable = False
                    issues.append("mean_rounding_relative_to_sd")
            map_routes.append("mpmath_80dps")
        else:
            usable = {"mean": True, "sd": True}
            raw_usable = True
            map_routes.append("float64")
        if why:
            routes.append("mpmath_80dps")
            precisions.append(80)
        else:
            prepared[:, j] = centered / sd_scaled
            routes.append("float64")
            precisions.append(0)
        for key in ("mean", "sd"):
            availability[key + "_float64_available"].append(usable[key])
        availability["raw_map_float64_available"].append(raw_usable)
        map_reasons.append(map_why)
        map_issues.append(issues)
        factored.append({"representation": "decimal_80dps" if precise else "float64",
                         **{key: precise[key] if precise else float(stats[i])
                            for key, i in (("max_abs", 0), ("mean_scaled", 1),
                                           ("sd_scaled", 2), ("log_sd", 5))}})
        reasons.append(why)
        for key, value in zip(fields, stats):
            record[key][j] = value
    # Preserve numeric array dtypes on ordinary inputs. Only unavailable map
    # entries need object storage; None cannot be silently used as zero/inf.
    for key in ("mean", "sd"):
        flags = availability[key + "_float64_available"]
        if not all(flags):
            record[key] = np.array([v if ok else None for v, ok in zip(record[key], flags)], dtype=object)
    record.update(route=routes, fallback_reasons=reasons, fallback_dps=precisions,
                  high_precision=high_precision, map_route=map_routes,
                  map_fallback_reasons=map_reasons, map_limitations=map_issues,
                  factored=factored, **availability)
    if vector:
        for key in (*fields, "route", "fallback_reasons", "fallback_dps", "map_route",
                    "map_fallback_reasons", "map_limitations", "factored", *availability):
            record[key] = record[key][0]
        prepared = prepared[:, 0]
    return prepared, record


def hpm_better(model, value, incumbent, incumbent_value):
    """Master I.6: strict score order; ONLY exact == invokes size then lex."""
    candidate = tuple(sorted(model))
    if not math.isfinite(float(value)):
        raise NumericalFailure("nonfinite HPM score")
    if incumbent is None or value > incumbent_value:
        return True
    old = tuple(sorted(incumbent))
    return value == incumbent_value and (len(candidate), candidate) < (len(old), old)


class Scorer:
    """Standalone oracle with original-index models; see module convention.

    ``status`` is ready, invalid_input, no_predictors, or y_constant. Terminal
    inputs retain an empty HPM, but evidence/PIPs are unavailable (None).
    ``log_m``, ``log_bf``, ``log_prior`` and ``score`` require ready status.
    Invalid models (including size > K) raise ValueError BEFORE any scoring.
    There is no seed or allocation argument because this is a deterministic
    external oracle, not the production fit or its resource preflight.
    """

    def __init__(self, X, y):
        self.status, self.message = "invalid_input", None
        self.n = self.p = self.input_p = self.K = 0
        self.X = self.y = self.G = self.z = None
        self.yty = None
        self.original_indices, self.dropped_indices = (), ()
        self.duplicate_components = []
        self.preprocessing = {}
        self._positions = {}
        self.last_details = None
        try:
            raw_x, raw_y = _numeric_inputs(X, y)
        except ValueError as exc:
            self.message = str(exc)
            return
        self.n, self.input_p = raw_x.shape
        keep = _retained_columns(raw_x)
        self.original_indices = tuple(int(j) for j in np.flatnonzero(keep))
        self.dropped_indices = tuple(int(j) for j in np.flatnonzero(~keep))
        self.p = len(self.original_indices)
        self.K = min(self.p, self.n // 2)
        self._positions = {j: i for i, j in enumerate(self.original_indices)}
        if self.p == 0:
            self.status = "no_predictors"
            return
        if _constant(raw_y):
            self.status = "y_constant"
            return
        self.X, xr = _standardize(raw_x[:, keep])
        self.y, yr = _standardize(raw_y)
        self.preprocessing = {"X": xr, "y": yr, "s_y": None if yr["sd"] is None else float(yr["sd"]),
                              "s_y_float64_available": yr["sd_float64_available"],
                              "s_y_decimal": yr["high_precision"][0]["sd"] if yr["high_precision"] else None,
                              "s_y_factored": dict(yr["factored"]), "log_s_y": yr["log_sd"]}
        # Explicit audit trail: X identifiers use PUBLIC original indices.
        self.preprocessing["fallbacks"] = [
            {"target": "X", "original_index": self.original_indices[i],
             "route": xr["route"][i], "reasons": why, "dps": xr["fallback_dps"][i]}
            for i, why in enumerate(xr["fallback_reasons"]) if why
        ]
        if yr["fallback_reasons"]:
            self.preprocessing["fallbacks"].append(
                {"target": "y", "route": yr["route"], "reasons": yr["fallback_reasons"],
                 "dps": yr["fallback_dps"]})
        self.G = self.X.T @ self.X
        self.z = self.X.T @ self.y
        self.yty = float(self.y @ self.y)
        # Master I.1.5 connected components, including sign duplicates; keep all.
        corr = self.G / np.sqrt(np.outer(np.diag(self.G), np.diag(self.G)))
        unseen = set(range(self.p))
        while unseen:
            root = min(unseen)
            unseen.remove(root)
            component, frontier = [root], [root]
            while frontier:
                i = frontier.pop()
                linked = sorted(j for j in unseen if abs(corr[i, j]) >= 1.0 - 1e-10)
                unseen.difference_update(linked)
                component.extend(linked)
                frontier.extend(linked)
            if len(component) > 1:
                self.duplicate_components.append(sorted(self.original_indices[j] for j in component))
        # Master I.2: individual-model log weights and W_K exactly once.
        sizes = np.arange(self.K + 1, dtype=float)
        self.log_w = -math.log(2.0) - (
            special.gammaln(2 * self.p) - special.gammaln(sizes + 1)
            - special.gammaln(2 * self.p - sizes)
        )
        log_counts = (special.gammaln(self.p + 1) - special.gammaln(sizes + 1)
                      - special.gammaln(self.p - sizes + 1))
        self.log_WK = float(special.logsumexp(log_counts + self.log_w))
        self.nu = A0 + self.n / 2.0
        self.log_Cn = float(A0 * math.log(2 * B0) + special.gammaln(self.nu)
                            - self.n / 2.0 * math.log(math.pi) - special.gammaln(A0))
        self.status = "ready"
        self.log_m_empty = self._details(())["log_m"]

    def _model(self, S: Iterable[int]):
        if self.status != "ready":
            raise ValueError("scoring unavailable for status " + self.status)
        try:
            values = tuple(S)
        except TypeError as exc:
            raise ValueError("S must be an iterable of integer original indices") from exc
        if any(isinstance(j, (bool, np.bool_)) or not isinstance(j, numbers.Integral) for j in values):
            raise ValueError("model indices must be integers")
        model = tuple(sorted(int(j) for j in values))
        if len(set(model)) != len(model):
            raise ValueError("duplicate model indices")
        if len(model) > self.K:
            raise ValueError("model exceeds K")
        if any(j not in self._positions for j in model):
            raise ValueError("model contains a dropped or out-of-range original column")
        return model

    def _factor_pair(self, positions):
        """Master I.2: Gram Cholesky -> rebuild Cholesky -> augmented QR."""
        k = len(positions)
        subset = self.X[:, positions]
        gram = self.G[np.ix_(positions, positions)]
        identity = np.eye(k)
        for route in ("gram_cholesky", "rebuilt_cholesky"):
            if route == "rebuilt_cholesky":
                gram = subset.T @ subset
            try:
                LH = linalg.cholesky((self.n + 1) * gram + identity, lower=True)
                LA = linalg.cholesky(gram + identity, lower=True)
                return LH, LA, subset, route
            except (linalg.LinAlgError, ValueError, FloatingPointError):
                pass
        try:
            _, RH = linalg.qr(np.vstack((math.sqrt(self.n + 1) * subset, identity)), mode="economic")
            _, RA = linalg.qr(np.vstack((subset, identity)), mode="economic")
            # Positive diagonals; R.T serves as a lower factor of each SPD matrix.
            RH = np.where(np.diag(RH) < 0, -1.0, 1.0)[:, None] * RH
            RA = np.where(np.diag(RA) < 0, -1.0, 1.0)[:, None] * RA
            if (not np.all(np.isfinite(RH)) or not np.all(np.isfinite(RA))
                    or np.any(np.diag(RH) <= 0) or np.any(np.diag(RA) <= 0)):
                raise linalg.LinAlgError("invalid augmented QR factor")
            return RH.T, RA.T, subset, "augmented_qr"
        except (linalg.LinAlgError, ValueError, FloatingPointError) as exc:
            raise NumericalFailure("numerical_failure after rebuild and QR") from exc

    def _details(self, model):
        k = len(model)
        route, nonnegative = "empty", False
        kH = kA = 1.0
        Q, determinant_log_ratio = self.yty, 0.0
        if k:
            positions = [self._positions[j] for j in model]
            LH, LA, subset, route = self._factor_pair(positions)
            # Recompute z from the data on fallback; do not reuse damaged cache.
            z = self.z[positions] if route == "gram_cholesky" else subset.T @ self.y
            try:
                solved = linalg.cho_solve((LH, True), z)
            except (linalg.LinAlgError, ValueError, FloatingPointError) as exc:
                raise NumericalFailure("factor solve failed") from exc
            determinant_log_ratio = float(2 * (np.log(np.diag(LH)).sum() - np.log(np.diag(LA)).sum()))
            Q = float(self.yty - self.n * (z @ solved))
            if Q < 1e-8 * self.yty:
                beta = self.n * solved
                fitted = subset @ beta
                residual = self.y - fitted
                Q = float(residual @ residual + (fitted @ fitted + beta @ beta) / self.n)
                nonnegative = True
            kH = float((np.max(np.diag(LH)) / np.min(np.diag(LH))) ** 2)
            kA = float((np.max(np.diag(LA)) / np.min(np.diag(LA))) ** 2)
        if not math.isfinite(Q) or Q <= 0:
            raise NumericalFailure("Q must be finite and positive; no clipping allowed")
        log_m = self.log_Cn - 0.5 * determinant_log_ratio - self.nu * math.log(2 * B0 + Q)
        if not math.isfinite(log_m):
            raise NumericalFailure("nonfinite integrated log score")
        # Master I.2 heuristic only; never changes target or HPM ordering.
        eta = 64 * np.finfo(float).eps * (
            self.nu * (self.yty / Q) * (1 + k * kH) + k * (kH + kA)
            + abs(self.log_Cn) + self.nu * abs(math.log(2 * B0 + Q)))
        return {"log_m": float(log_m), "Q": Q, "route": route,
                "nonnegative_recompute": nonnegative, "eta": float(eta)}

    def details(self, S):
        """Extra diagnostics for parent comparisons (no hidden cache)."""
        result = self._details(self._model(S))
        self.last_details = dict(result)
        return result

    def log_m(self, S):
        return self.details(S)["log_m"]

    def log_bf(self, S):
        return self.log_m(S) - self.log_m_empty

    def log_prior(self, S):
        model = self._model(S)
        return float(self.log_w[len(model)] - self.log_WK)

    def score(self, S):
        model = self._model(S)
        return self.log_m(model) + float(self.log_w[len(model)] - self.log_WK)

    def enumerate_exact(self):
        return enumerate_exact(self)


def enumerate_exact(scorer: Scorer):
    """Master I.3/I.6 independent reference, p<=20, streaming all |S|<=K.

    This deliberately does NOT apply the production branch threshold: it is an
    external verifier, never an input to a fit. Original-length PIPs include 0
    for dropped columns. Terminal cases use None, not asserted zero PIPs.
    Both evidence scales are log values; BF scale is log(Z/m(empty)).
    """
    if scorer.status != "ready":
        return {"status": scorer.status, "hpm": [], "pips": None,
                "log_Z_full": None, "log_Z_bf": None, "enumerated": 0}
    if scorer.p > 20:
        raise ValueError("external exact oracle is limited to retained p <= 20")
    log_z = -math.inf
    numerators = np.full(scorer.input_p, -math.inf)
    best, best_value, best_eta = None, -math.inf, None
    competitor_score = competitor_upper = -math.inf
    count = 0
    for k in range(scorer.K + 1):
        for model in itertools.combinations(scorer.original_indices, k):
            d = scorer.details(model)
            value = d["log_m"] + scorer.log_prior(model)
            if hpm_better(model, value, best, best_value):
                if best is not None:
                    competitor_score = max(competitor_score, best_value)
                    competitor_upper = max(competitor_upper, best_value + best_eta)
                best, best_value, best_eta = model, value, d["eta"]
            else:
                competitor_score = max(competitor_score, value)
                competitor_upper = max(competitor_upper, value + d["eta"])
            log_z = float(np.logaddexp(log_z, value))
            for j in model:
                numerators[j] = np.logaddexp(numerators[j], value)
            count += 1
    pips = np.exp(numerators - log_z)
    margin = best_value - competitor_score
    bound = best_value - competitor_upper
    return {"status": "exact", "enumerated": count, "hpm": list(best),
            "hpm_score": float(best_value), "pips": pips.tolist(),
            "mpm": [int(j) for j in np.flatnonzero(pips > 0.5)],
            "log_Z_full": log_z, "log_Z_bf": log_z - scorer.log_m_empty,
            "log_m_empty": scorer.log_m_empty, "log_WK": scorer.log_WK,
            "local_certified": True,
            "global_certified": bool(best_value - best_eta > competitor_upper),
            "hpm_eta": best_eta, "hpm_margin": margin, "certificate_bound": bound,
            "certificate_label": "heuristic (not a validated interval bound)",
            "original_indices": list(scorer.original_indices),
            "dropped_indices": list(scorer.dropped_indices)}


def mp_reference(X, y, S, dps=80):
    """Independent high-precision formula (Master I.1/I.2, M sections 4--5).

    Recenter/rescale original numeric inputs in arbitrary precision, independently
    of Scorer. Integrate via the N-by-N observation covariance
       V = I + n X_S (X_S'X_S + I)^(-1) X_S'
    and Q=y' V^(-1)y, avoiding H, cached Gram/z, and subtractive Q entirely.
    Linear systems are solved; no explicit inverse/determinant is formed.
    Prior uses beta functions and an explicit binomial sum, not log-gamma.
    Returns decimal STRINGS (dps significant digits), JSON serializable.
    """
    if not isinstance(dps, numbers.Integral) or dps < 80:
        raise ValueError("at least 80 decimal digits required")
    raw_x, raw_y = _numeric_inputs(X, y)
    keep = list(np.flatnonzero(_retained_columns(raw_x)))
    values = tuple(S)
    if any(isinstance(j, (bool, np.bool_)) or not isinstance(j, numbers.Integral) for j in values):
        raise ValueError("model indices must be integers")
    model = tuple(sorted(int(j) for j in values))
    n, p = len(raw_y), len(keep)
    K = min(p, n // 2)
    if not p or _constant(raw_y):
        raise ValueError("high-precision score unavailable for terminal input")
    if len(set(model)) != len(model) or len(model) > K or any(j not in keep for j in model):
        raise ValueError("infeasible original-index model")
    with mp.workdps(int(dps)):
        def standardize(values):
            # Original integers remain exact, even above binary64's 2**53.
            # This independent raw-mean route is algebraically equivalent to
            # maxabs scaling; it does not call Scorer's preparation fallback.
            vec = [_mp_number(t) for t in values]
            mean = mp.fsum(vec) / n
            centered = [v - mean for v in vec]
            sd = mp.sqrt(mp.fsum(v*v for v in centered) / (n-1))
            return [v / sd for v in centered]

        response = mp.matrix(standardize(raw_y))
        V = mp.eye(n)
        if model:
            cols = [standardize(raw_x[:, j]) for j in model]
            design = mp.matrix([[cols[j][i] for j in range(len(model))] for i in range(n)])
            A = design.T * design + mp.eye(len(model))
            # Each column of A^{-1} X' is obtained by an independent solve.
            AXt = mp.matrix(len(model), n)
            for i in range(n):
                solution = mp.lu_solve(A, design[i, :].T)
                for j in range(len(model)):
                    AXt[j, i] = solution[j]
            V += n * design * AXt
            # The exact covariance is symmetric. Independent LU solves can
            # differ in their last MP digit; remove only that skew roundoff.
            V = (V + V.T) / 2
        L = mp.cholesky(V)
        logdet = 2 * mp.fsum(mp.log(L[i, i]) for i in range(n))
        Q = (response.T * mp.lu_solve(V, response))[0]
        a, b = mp.mpf("0.01"), mp.mpf("0.01")
        nu = a + mp.mpf(n)/2
        logc = a*mp.log(2*b) + mp.loggamma(nu) - mp.mpf(n)/2*mp.log(mp.pi) - mp.loggamma(a)
        logm = logc - logdet/2 - nu*mp.log(2*b + Q)
        lognull = logc - nu*mp.log(2*b + (response.T*response)[0])
        weights = [mp.beta(1+k, 2*p-k) / mp.beta(1, p) for k in range(K+1)]
        wk = mp.fsum(mp.binomial(p, k)*weights[k] for k in range(K+1))
        lp = mp.log(weights[len(model)] / wk)
        result = {"log_m": logm, "log_bf": logm-lognull, "log_prior": lp,
                  "score": logm+lp, "Q": Q, "log_WK": mp.log(wk)}
        return {key: mp.nstr(value, int(dps)) for key, value in result.items()}
