"""Independent finite-state move oracle; never imports production/prototype code.

Authority: MASTER_Methodology_and_Plan.md Part I §§I.1, I.3, I.4;
METHODOLOGY_v3.md §§6.3--6.5, with Part I governing all differences.
Public original column IDs are ZERO-based: subtract 1 from Part I IDs on input,
add 1 on export to the method's reporting format. IDs can be noncontiguous.
Matrices are row-stochastic, states are sorted by size then lexicographically.
These are exhaustive finite-state probabilities, evaluated in double precision,
not stochastic simulation and not a bit-level PRNG oracle. No work on import.
"""
from dataclasses import dataclass
from itertools import combinations
import math
import numpy as np
from scipy.special import logsumexp, expit


@dataclass(frozen=True)
class ModelSpace:
    """Part I I.1/I.2: all subsets of original_indices with size <= K."""
    original_indices: tuple
    K: int

    def __post_init__(self):
        ids = tuple(self.original_indices)
        if (not ids or any(not isinstance(j, (int, np.integer)) or j < 0 for j in ids)
                or tuple(sorted(set(ids))) != ids
                or not isinstance(self.K, (int, np.integer)) or not 0 <= self.K <= len(ids)):
            raise ValueError("sorted distinct nonnegative original IDs and 0 <= K <= p required")
        object.__setattr__(self, "original_indices", ids)

    @property
    def states(self):
        return tuple(s for k in range(self.K + 1)
                     for s in combinations(self.original_indices, k))


def _vector(values, n, positive=False):
    a = np.asarray(values, dtype=float)
    if a.shape != (n,) or not np.all(np.isfinite(a)) or (positive and np.any(a <= 0)):
        raise ValueError("finite aligned vector required (strictly positive for probabilities)")
    return a


def bridge(space, pi0, F, phi):
    """I.3: log q_phi = const+(1-phi)log pi0+phi F.

    pi0 must contain positive normalized probabilities in space.states order.
    d differs from F-log pi0 only by a constant, irrelevant to all MH ratios.
    Absolute gamma normalizers/evidence cannot be recovered from pi0 and F alone.
    """
    n = len(space.states)
    pi0 = _vector(pi0, n, positive=True)
    F = _vector(F, n)
    if not math.isfinite(phi) or not 0 <= phi <= 1:
        raise ValueError("phi must be in [0,1]")
    if not np.isclose(pi0.sum(), 1.0, rtol=0, atol=2e-14):
        raise ValueError("pi0 must be normalized")
    log0 = np.log(pi0)
    logw = (1 - phi) * log0 + phi * F
    return {"log_target": logw, "q": np.exp(logw - logsumexp(logw)),
            "d_up_to_constant": F - log0}


def gibbs_kernel(space, log_target, j):
    """I.4 G_j; returns (matrix, o_j at each incoming state)."""
    states = space.states
    logw = _vector(log_target, len(states))
    if j not in space.original_indices:
        raise ValueError("unknown coordinate")
    ix = {s: i for i, s in enumerate(states)}
    P = np.zeros((len(states), len(states)))
    recording = np.zeros(len(states))
    for i, s in enumerate(states):
        a = tuple(k for k in s if k != j)
        ia = ix[a]
        if len(a) == space.K:
            P[i, ia] = 1.0
            continue
        b = tuple(sorted((*a, j)))
        ib = ix[b]
        o = float(expit(logw[ib] - logw[ia]))
        recording[i] = o
        P[i, ia], P[i, ib] = 1 - o, o
    return P, recording


def _accept(logratio):
    return math.exp(min(0.0, float(logratio)))


def uniform_swap_kernel(space, log_target):
    """I.4 U: included/excluded choices uniform, no cap-changing proposal."""
    states = space.states
    logw = _vector(log_target, len(states))
    ix = {s: i for i, s in enumerate(states)}
    P = np.eye(len(states))
    for i, s in enumerate(states):
        outside = set(space.original_indices) - set(s)
        if not s or not outside:
            continue
        proposal = 1.0 / (len(s) * len(outside))
        for j in s:
            for l in sorted(outside):
                t = tuple(sorted((set(s) - {j}) | {l}))
                it = ix[t]
                flow = proposal * _accept(logw[it] - logw[i])
                P[i, it] += flow
                P[i, i] -= flow
    return P


def validate_graph(space, graph):
    """I.4: graph is the symmetric union; degrees need not be <= B."""
    ids = set(space.original_indices)
    if set(graph) != ids:
        raise ValueError("one neighbour list per retained original ID required")
    g = {j: frozenset(graph[j]) for j in ids}
    for j in ids:
        if j in g[j] or not g[j] <= ids:
            raise ValueError("invalid edge")
        if any(j not in g[l] for l in g[j]):
            raise ValueError("neighbour graph must be symmetric")
    return g


def neighbour_swap_kernel(space, log_target, graph):
    """I.4 N: alpha=min(1,target_ratio * forward_count/reverse_count)."""
    states = space.states
    logw = _vector(log_target, len(states))
    ix = {s: i for i, s in enumerate(states)}
    graph = validate_graph(space, graph)
    P = np.eye(len(states))
    for i, s in enumerate(states):
        if not s:
            continue
        ss = set(s)
        for j in s:
            candidates = graph[j] - ss
            if not candidates:  # chosen j rejects without proposing/scoring
                continue
            proposal = 1.0 / (len(s) * len(candidates))
            for l in sorted(candidates):
                ts = (ss - {j}) | {l}
                t = tuple(sorted(ts))
                it = ix[t]
                reverse_count = len(graph[l] - ts)
                ratio = logw[it] - logw[i] + math.log(len(candidates) / reverse_count)
                flow = proposal * _accept(ratio)
                P[i, it] += flow
                P[i, i] -= flow
    return P


def independence_kernel(space, pi0, F, phi):
    """I.4 I: pi0 proposal, acceptance exp(phi*Delta d), includes self."""
    b = bridge(space, pi0, F, phi)
    d = b["d_up_to_constant"]
    n = len(space.states)
    P = np.eye(n)
    for i in range(n):
        for t in range(n):
            if t != i:
                flow = float(pi0[t]) * _accept(phi * (d[t] - d[i]))
                P[i, t] += flow
                P[i, i] -= flow
    return P


def round_kernels(space, pi0, F, phi, B, graph):
    """I.4 canonical labels; N labels are distinct despite identical matrices."""
    if not isinstance(B, (int, np.integer)) or B < 1:
        raise ValueError("B must be positive")
    b = bridge(space, pi0, F, phi)
    out = {f"G{j}": gibbs_kernel(space, b["log_target"], j)[0]
           for j in space.original_indices}
    out["U"] = uniform_swap_kernel(space, b["log_target"])
    N = neighbour_swap_kernel(space, b["log_target"], graph)
    out.update({f"N{k}": N.copy() for k in range(B)})
    out["I"] = independence_kernel(space, pi0, F, phi)
    return out


def ordered_round(kernels, labels):
    """I.4: realised order preserves q, need not be reversible."""
    if len(labels) != len(kernels) or set(labels) != set(kernels):
        raise ValueError("labels must be a permutation of every elementary label")
    P = np.eye(next(iter(kernels.values())).shape[0])
    for label in labels:
        P = P @ kernels[label]
    return P


def random_order_round(kernels):
    """I.4 exact uniform-permutation average, subset dynamic programming.

    D[A] = sum_{i in A} D[A minus {i}] K_i / |A|. Each labelled ordering occurs
    once with weight 1/m!, including repeated neighbour kernels. Tiny-p only.
    """
    mats = list(kernels.values())
    if not mats or len(mats) > 10:
        raise ValueError("this exhaustive oracle supports 1..10 labels")
    dp = {0: np.eye(mats[0].shape[0])}
    for mask in range(1, 1 << len(mats)):
        bits = [i for i in range(len(mats)) if mask & (1 << i)]
        dp[mask] = sum((dp[mask ^ (1 << i)] @ mats[i] for i in bits)) / len(bits)
    return dp[(1 << len(mats)) - 1]


def ordered_gibbs_recordings(space, log_target, kernels, labels, incoming):
    """I.4/I.6 expected o_j at its current within-round state, given an order.

    incoming is a distribution or a one-hot incoming particle state. Expectations
    propagate through every preceding step, including swaps/independence moves.
    Parent can compare these to a supplied transition/recording adapter remotely.
    """
    if len(labels) != len(kernels) or set(labels) != set(kernels):
        raise ValueError("labels must be a full elementary permutation")
    distribution = _vector(incoming, len(space.states))
    if np.any(distribution < 0) or not np.isclose(distribution.sum(), 1, rtol=0, atol=2e-14):
        raise ValueError("incoming must be a probability distribution")
    expectations = {}
    for label in labels:
        if label.startswith("G"):
            j = int(label[1:])
            _, conditional = gibbs_kernel(space, log_target, j)
            expectations[j] = float(distribution @ conditional)
        distribution = distribution @ kernels[label]
    return {"expected_recordings": expectations, "outgoing": distribution}


def matrix_residuals(P, q):
    """Inspectable invariant/detailed-balance evidence, no pass threshold here."""
    P, q = np.asarray(P, float), np.asarray(q, float)
    flow = q[:, None] * P
    return {"row_sum": float(np.max(np.abs(P.sum(axis=1) - 1))),
            "minimum_entry": float(P.min()),
            "stationarity": float(np.max(np.abs(q @ P - q))),
            "detailed_balance": float(np.max(np.abs(flow - flow.T)))}
