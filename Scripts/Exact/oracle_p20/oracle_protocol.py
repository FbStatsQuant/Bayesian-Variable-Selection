"""Independent protocol checks from master Part I, never prototype source.

This deliberately small oracle is for comparison, not a production sampler.
Arrays and integer choices use zero-based indices. Fit output uses original
one-based indices through the scorer's preprocessing map.
"""

import math
import numpy as np
from scipy.special import logsumexp


class Stream:
    """Part I.4: exact unsigned SplitMix64 -> xoshiro256** convention."""

    MASK = (1 << 64) - 1

    def __init__(self, seed, stream):
        self.state = []
        x = ((int(seed) << 32) + int(stream)) & self.MASK
        for _ in range(4):
            x = (x + 0x9E3779B97F4A7C15) & self.MASK
            z = x
            z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & self.MASK
            z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & self.MASK
            self.state.append(z ^ (z >> 31))
        self.draw_count = 0

    @classmethod
    def rotate(cls, value, shift):
        value &= cls.MASK
        return ((value << shift) | (value >> (64 - shift))) & cls.MASK

    def next_uint64(self):
        a = self.state
        result = (self.rotate(a[1] * 5, 7) * 9) & self.MASK
        t = (a[1] << 17) & self.MASK
        a[2] ^= a[0]
        a[3] ^= a[1]
        a[1] ^= a[2]
        a[0] ^= a[3]
        a[2] ^= t
        a[3] = self.rotate(a[3], 45)
        self.draw_count += 1
        return result

    def uniform(self):
        return (self.next_uint64() >> 11) * (2.0 ** -53)

    def permutation(self, labels):
        values = list(labels)
        for length in range(len(values), 1, -1):
            position = int(self.uniform() * length)
            values[length - 1], values[position] = values[position], values[length - 1]
        return values


def cumulative_weights(logweights):
    """I.4: serial, unnormalized cumulative sum then divide once by total."""
    lw = list(map(float, logweights))
    maximum = max(lw)
    if not math.isfinite(maximum):
        raise ValueError("at least one finite log weight required")
    cumulative = []
    total = 0.0
    for value in lw:
        total += math.exp(value - maximum)
        cumulative.append(total)
    cumulative = [value / total for value in cumulative]
    cumulative[-1] = 1.0
    return cumulative


def resample_index(cumulative, uniform):
    """I.4: naive first-index oracle, independent of A's required guide table."""
    if not 0.0 <= uniform < 1.0:
        raise ValueError("uniform outside [0,1)")
    effective = math.nextafter(0.0, 1.0) if uniform == 0.0 else uniform
    for index, value in enumerate(cumulative):
        if value >= effective:
            return index
    raise ValueError("CDF must end at 1")


def start_category(probabilities, uniform):
    """I.3: start categorical strict >, distinct from resampling >=."""
    if not 0.0 <= uniform < 1.0:
        raise ValueError("uniform outside [0,1)")
    cumulative = 0.0
    for index, value in enumerate(probabilities):
        cumulative += value
        if index == len(probabilities) - 1:
            cumulative = 1.0
        if cumulative > uniform:
            return index
    raise ValueError("invalid categorical probabilities")


def empirical_ess(logweights):
    """I.4: (sum w)^2/sum w^2, with shift to avoid overflow."""
    values = np.asarray(logweights, dtype=float)
    values = values - np.max(values)
    return float(np.exp(2 * logsumexp(values) - logsumexp(2 * values)))


def pilot_endpoint(phi, discrepancies, ceiling):
    """I.5: exact endpoint/floor/snap decision, independent of particles."""
    d = np.asarray(discrepancies, dtype=float)
    threshold = 0.9 * len(d)
    if empirical_ess((1 - phi) * d) >= threshold:
        return 1.0, False
    lo, hi = phi, 1.0
    for _ in range(60):
        middle = (lo + hi) / 2
        if empirical_ess((middle - phi) * d) >= threshold:
            lo = middle
        else:
            hi = middle
    forced = lo - phi < 1 / ceiling
    if forced:
        lo = min(1.0, phi + 1 / ceiling)
        if lo >= 1 - 1e-12:
            lo = 1.0
    return lo, forced


def restricted_rho(log_gamma0, discrepancies, u, v):
    """I.5: restricted finite-sum moment ratio, including 2v-u>1."""
    lg = np.asarray(log_gamma0, dtype=float)
    d = np.asarray(discrepancies, dtype=float)
    # Subtract a common constant only; same finite-sum definition.
    lg = lg - np.max(lg)
    f_u = logsumexp(lg + u * d)
    f_v = logsumexp(lg + v * d)
    f_extrapolated = logsumexp(lg + (2 * v - u) * d)
    return float(np.exp(2 * f_v - f_u - f_extrapolated))


def restricted_grid(log_gamma0, discrepancies, targets, ceiling):
    """I.5: post-snap validation; no rescue floor or hidden tolerance."""
    grid = [0.0]
    for target in targets:
        if not 0 < target <= 1:
            raise ValueError("pilot targets must be in (0,1]")
        while grid[-1] < target:
            u = grid[-1]
            if restricted_rho(log_gamma0, discrepancies, u, target) >= 0.9:
                v = float(target)
            else:
                lo, hi = u, float(target)
                for _ in range(60):
                    middle = (lo + hi) / 2
                    if restricted_rho(log_gamma0, discrepancies, u, middle) >= 0.9:
                        lo = middle
                    else:
                        hi = middle
                v = lo
            if v >= 1 - 1e-12:
                v = 1.0
            if v <= u or restricted_rho(log_gamma0, discrepancies, u, v) < 0.9:
                return {"ok": False, "reason": "post_snap_validation", "grid": grid}
            grid.append(v)
            if len(grid) - 1 > ceiling:
                return {"ok": False, "reason": "too_many_intervals", "grid": grid}
    return {"ok": grid[-1] == 1.0, "reason": None, "grid": grid}


def evidence(log_m_empty, log_zbar0, island_increments):
    """I.6: full-scale and BF-scale evidence; linear arithmetic pooling."""
    if len(island_increments) != 4:
        raise ValueError("exactly four final islands required")
    relative = [log_zbar0 + math.fsum(x) for x in island_increments]
    full = [log_m_empty + x for x in relative]
    pooled = float(logsumexp(full) - math.log(4))
    return {"island_log_z": full, "island_log_z_bf": relative,
            "log_z": pooled, "log_z_bf": pooled - log_m_empty,
            "log_lower95": pooled + math.log(0.05)}


def budgets(n, p):
    """I.1 fixed formulas, with integer operations where exact."""
    ell = (n + p).bit_length()
    N0 = max(2500, n, p)
    return {"K": min(p, n // 2), "B": min(math.isqrt(n), math.isqrt(p), 16),
            "ell": ell, "L": max(4, n.bit_length()), "N0": N0,
            "H0": (512 * N0 + 2499) // 2500, "T0": max(1000, ell * ell)}


def exact_branch(n, p):
    """I.3: arbitrary-precision integer oracle for saturated decision."""
    b = budgets(n, p)
    count = sum(math.comb(p, k) for k in range(b["K"] + 1))
    threshold = (5 * b["H0"] + 4 * b["N0"]) * p
    return count <= threshold, count, threshold


def memory_bytes(n, p, tier=0, exact=False):
    """I.1: prescribed estimate (not a rigorous upper bound)."""
    b = budgets(n, p)
    K, B = b["K"], b["B"]
    if exact:
        return 8 * (3 * n * p + p * p) + 8 * (40 * p + 1) * (min(K, (p + 1) // 2) + 8) + 32 * p
    cache = 500 * p
    blocks = (p + B - 1) // B
    N = (4 ** tier) * b["N0"]
    return (8 * (3 * n * p + 3 * p * p)
            + 16 * blocks * (2 ** B) + 8 * blocks * (K + 1) * (B + 1)
            + 29 * (1 << (2 * cache - 1).bit_length()) + 4 * cache * K
            + (80 * p + 1) * (4 * K + 64)
            + 2 * N * (8 * ((p + 63) // 64) + 4 * K + 96))


def time_guard(elapsed, operation_duration, hours):
    """I.1: strictly >, evaluated at the specified completed checkpoints."""
    return elapsed + operation_duration > hours * 3600
