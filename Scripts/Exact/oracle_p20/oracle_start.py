"""Independent composite-start oracle; no production/prototype imports.

Authority: MASTER_Methodology_and_Plan.md Part I (2026-10-22), I.1
(budgets/index ordering), I.2 (capped prior), I.3 (blocks, cut_group,
tables, convolution, exact draw), I.4 (start draw consumption). Supporting
source: METHODOLOGY_v3.md sections 3, 5, 6.3. Part I governs differences.

All public model indices are 0-based ORIGINAL column indices. Convert a
Part-I index by subtracting 1, and add 1 when comparing its textual output.
Noncontiguous labels after dropping columns are allowed. Callback/scorer
adapters must use the same labels; no silent retained-position conversion.
This is a small-problem reference, not production fitting code.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import heapq
import math
from numbers import Integral
from typing import Callable, Iterable, Protocol

import numpy as np
from scipy.special import gammaln, logsumexp

Model = tuple[int, ...]


class ScorerLike(Protocol):
    """Planned oracle_score.Scorer interface (I.2); arrays already standardized."""
    n: int
    p: int
    K: int
    X: np.ndarray
    y: np.ndarray
    G: np.ndarray
    z: np.ndarray
    yty: float

    def log_m(self, S: Model) -> float: ...
    def log_bf(self, S: Model) -> float: ...
    def log_prior(self, S: Model) -> float: ...
    def score(self, S: Model) -> float: ...


def canonical_model(S: Iterable[int]) -> Model:
    values = tuple(S)
    if any(isinstance(j, bool) or not isinstance(j, Integral) or j < 0 for j in values):
        raise ValueError("model indices must be nonnegative integers (0-based)")
    if len(set(values)) != len(values):
        raise ValueError("duplicate model index")
    return tuple(sorted(int(j) for j in values))


def budgets(n: int, p: int) -> dict[str, int]:
    """Part I I.1; integer arithmetic for floor/ceiling operations."""
    if n < 3 or p < 1:
        raise ValueError("require n >= 3 and retained p >= 1")
    ell = (n + p).bit_length()  # ceil(log2(n+p+1))
    N = max(2500, n, p)
    return dict(K=min(p, n // 2), B=min(math.isqrt(n), math.isqrt(p), 16),
                ell=ell, L=max(4, n.bit_length()), N0=N,
                H0=(512 * N + 2499) // 2500, T0=max(1000, ell * ell))


def exact_branch(n: int, p: int) -> dict[str, int | bool]:
    """I.3 saturating decision: E is capped at threshold+1, never an estimate."""
    b = budgets(n, p)
    threshold = (5 * b['H0'] + 4 * b['N0']) * p
    total, term = 1, 1
    for k in range(1, b['K'] + 1):
        term = term * (p - k + 1) // k
        total += term
        if total > threshold:
            return dict(use_exact=False, E=threshold + 1, saturated=True, threshold=threshold)
    return dict(use_exact=True, E=total, saturated=False, threshold=threshold)


def _correlation(r, original_indices=None):
    r = np.asarray(r, dtype=float)
    if r.ndim != 2 or r.shape[0] != r.shape[1] or not len(r):
        raise ValueError("correlation must be a nonempty square matrix")
    if not np.isfinite(r).all() or not np.allclose(r, r.T, rtol=0, atol=1e-14):
        raise ValueError("finite symmetric correlation required")
    ids = tuple(range(len(r))) if original_indices is None else tuple(original_indices)
    if len(ids) != len(r) or len(canonical_model(ids)) != len(r):
        raise ValueError("one distinct original index per correlation row required")
    return r, ids


@dataclass(frozen=True)
class ClusterNode:
    members: Model
    left: ClusterNode | None = None
    right: ClusterNode | None = None
    height: float = 0.0

    @property
    def leaves(self) -> Model:
        return self.members if self.left is None else self.left.leaves + self.right.leaves


@dataclass(frozen=True)
class BlockConstruction:
    root: ClusterNode
    clusters: tuple[Model, ...]  # top-down cut, left first; members sorted
    blocks: tuple[Model, ...]    # next-fit; members sorted for binary table order
    leaf_order: Model
    merges: tuple[tuple[float, Model], ...]
    B: int


def build_blocks(correlation, n: int, original_indices=None) -> BlockConstruction:
    """Full I.3 complete linkage, lexicographic UNION ties, cut, next-fit pack.

    No scipy linkage tie convention is inherited. Exact distance equality
    alone is a tie. Distances update by max, and left child has smaller min.
    All p-1 merges finish before the size cut; there is no correlation-height
    stopping threshold. B is the I.1 rule, with no production override.
    """
    r, ids = _correlation(correlation, original_indices)
    p = len(ids)
    B = budgets(n, p)['B']
    active = {j: ClusterNode((ids[j],)) for j in range(p)}
    distances, heap, merges = {}, [], []
    for a in range(p):
        for b in range(a + 1, p):
            d = float(1.0 - abs(r[a, b]))
            distances[a, b] = d
            heapq.heappush(heap, (d, tuple(sorted((ids[a], ids[b]))), a, b))
    nxt = p
    while len(active) > 1:
        d, union, a, b = heapq.heappop(heap)
        if a not in active or b not in active:
            continue
        left, right = sorted((active[a], active[b]), key=lambda node: node.members[0])
        node = ClusterNode(union, left, right, d)
        del active[a], active[b]
        for c, other in active.items():
            da = distances[min(a, c), max(a, c)]
            db = distances[min(b, c), max(b, c)]
            dc = max(da, db)
            distances[min(c, nxt), max(c, nxt)] = dc
            merged = tuple(sorted(union + other.members))
            heapq.heappush(heap, (dc, merged, min(c, nxt), max(c, nxt)))
        active[nxt] = node
        nxt += 1
        merges.append((d, union))
    root = next(iter(active.values()))
    clusters = []
    def cut(node):
        if len(node.members) <= B:
            clusters.append(node.members)
        else:
            cut(node.left)
            cut(node.right)
    cut(root)
    blocks, current = [], ()
    for cluster in clusters:
        if current and len(current) + len(cluster) > B:
            blocks.append(tuple(sorted(current)))
            current = ()
        current += cluster
    if current:
        blocks.append(tuple(sorted(current)))
    return BlockConstruction(root, tuple(clusters), tuple(blocks), root.leaves,
                             tuple(merges), B)


def cut_group(correlation, n: int, blocks=None, original_indices=None) -> dict:
    """I.3 D4: uncapped >= threshold graph; blocks=None is exact-branch NA."""
    r, ids = _correlation(correlation, original_indices)
    if n < 3:
        raise ValueError("n >= 3 required")
    rho = math.sqrt(2 * math.log(len(ids)) / n)
    if blocks is None:
        return dict(cut_group=None, flagged_component_count=None, components=None,
                    threshold=rho)
    normalized = tuple(canonical_model(b) for b in blocks)
    flat = tuple(j for b in normalized for j in b)
    if any(not b for b in normalized) or len(flat) != len(ids) or set(flat) != set(ids):
        raise ValueError("blocks must partition retained original indices")
    owner = {j: b for b, C in enumerate(normalized) for j in C}
    unseen, flagged = set(range(len(ids))), []
    while unseen:
        seed = min(unseen, key=lambda j: ids[j])
        unseen.remove(seed)
        todo, component = [seed], []
        while todo:
            a = todo.pop()
            component.append(ids[a])
            adjacent = [b for b in unseen if abs(r[a, b]) >= rho]
            unseen.difference_update(adjacent)
            todo.extend(adjacent)
        members = tuple(sorted(component))
        spans = tuple(sorted({owner[j] for j in members}))
        if len(spans) >= 2:
            flagged.append(dict(size=len(members), block_count=len(spans),
                                members=members, block_indices=spans))
    flagged.sort(key=lambda c: c['members'])
    return dict(cut_group=bool(flagged), flagged_component_count=len(flagged),
                components=flagged, threshold=rho)


def log_size_prior(p: int, K: int):
    """I.2: per-MODEL log w(k)/W_K; binomial multiplicity only in W_K."""
    if p < 1 or not 0 <= K <= p:
        raise ValueError("require 0 <= K <= p and p >= 1")
    k = np.arange(K + 1, dtype=float)
    logw = -math.log(2) - (gammaln(2*p) - gammaln(k+1) - gammaln(2*p-k))
    logchoose = gammaln(p+1) - gammaln(k+1) - gammaln(p-k+1)
    logWK = float(logsumexp(logchoose + logw))
    return logw - logWK, logWK


def enumerate_models(variables, K):
    ids = canonical_model(variables)
    for k in range(min(K, len(ids)) + 1):
        yield from combinations(ids, k)


@dataclass(frozen=True)
class BlockTable:
    members: Model
    models: tuple[Model, ...]  # increasing binary code; first member is LSB
    log_r: np.ndarray
    by_size: tuple[tuple[int, ...], ...]  # binary codes within each size
    log_profile: np.ndarray


def build_tables(blocks, log_bf: Callable[[Model], float], on_score=None):
    """I.3: exponent-one full-response tables. on_score(S,logBF) sees EVERY row.

    No score cache is created. Parent owns HPM/leader integration through the
    optional callback; it can call scorer.score(S) there if needed.
    """
    tables = []
    for raw in blocks:
        members = canonical_model(raw)
        if not members:
            raise ValueError("empty block")
        models, weights = [], []
        classes = [[] for _ in range(len(members) + 1)]
        for code in range(1 << len(members)):
            S = tuple(j for bit, j in enumerate(members) if code & (1 << bit))
            value = float(log_bf(S))
            if not math.isfinite(value):
                raise ValueError("table logBF must be finite; numerical failure cannot be hidden")
            if not S and value != 0.0:
                raise ValueError("logBF(empty) must be exactly zero")
            models.append(S)
            weights.append(value)
            classes[len(S)].append(code)
            if on_score is not None:
                on_score(S, value)
        weights = np.asarray(weights)
        profile = np.asarray([logsumexp(weights[c]) for c in classes])
        tables.append(BlockTable(members, tuple(models), weights,
                                 tuple(tuple(c) for c in classes), profile))
    return tuple(tables)


def log_convolution(profiles, K: int) -> np.ndarray:
    """I.3 A_b(k); rows 0..J, columns 0..K. Impossible mass is -inf."""
    if K < 0:
        raise ValueError("negative K")
    A = np.full((len(profiles) + 1, K + 1), -np.inf)
    A[0, 0] = 0.0
    for b, profile in enumerate(profiles, 1):
        for k in range(K + 1):
            A[b, k] = logsumexp([profile[j] + A[b-1, k-j]
                                 for j in range(min(k, len(profile)-1) + 1)])
    return A


def categorical_log(logweights, u: float) -> int:
    """I.3: ascending candidates; first cumulative STRICTLY > u, final 1."""
    lw = np.asarray(logweights, dtype=float)
    if lw.ndim != 1 or not len(lw) or np.isnan(lw).any() or np.isposinf(lw).any():
        raise ValueError("invalid log categorical weights")
    if not 0 <= u < 1 or not np.isfinite(lw).any():
        raise ValueError("require 0 <= u < 1 and positive categorical mass")
    weights = np.exp(lw - np.max(lw))
    cdf = np.cumsum(weights)
    cdf /= cdf[-1]
    cdf[-1] = 1.0
    return int(np.searchsorted(cdf, u, side='right'))


class CompositeStart:
    """I.3 log tables, exact probability and reference sampler on supplied blocks.

    Fixture blocks may be supplied for mathematical unit checks; production
    construction is build_blocks(). uniform is a zero-argument callable.
    No PRNG is prescribed here: parent supplies its stream. No bit identity
    with production arithmetic is claimed, only the specified law/order.
    """
    def __init__(self, blocks, K: int, log_bf, *, on_score=None):
        blocks = tuple(canonical_model(b) for b in blocks)
        self.variables = canonical_model(j for b in blocks for j in b)
        self.p, self.K = len(self.variables), K
        if not self.p or not 0 <= K <= self.p or any(len(b) > K for b in blocks):
            raise ValueError("require nonempty partition and max block size <= K <= p")
        self.blocks = blocks
        self._log_bf = log_bf
        self.tables = build_tables(blocks, log_bf, on_score)
        self.log_prior_by_size, self.log_WK = log_size_prior(self.p, K)
        self.log_A = log_convolution([t.log_profile for t in self.tables], K)
        self.log_Z0 = float(logsumexp(self.log_prior_by_size + self.log_A[-1]))
        self.log_size_prob = self.log_prior_by_size + self.log_A[-1] - self.log_Z0
        self._lookups = [{S: i for i, S in enumerate(t.models)} for t in self.tables]

    @classmethod
    def from_scorer(cls, scorer: ScorerLike, blocks, *, on_score=None):
        """No import of oracle_score is needed; uses its planned log_bf(S)."""
        result = cls(blocks, scorer.K, scorer.log_bf, on_score=on_score)
        if result.p != scorer.p:
            raise ValueError("scorer.p and block partition size differ")
        return result

    def _model(self, S):
        S = canonical_model(S)
        if len(S) > self.K or not set(S).issubset(self.variables):
            raise ValueError("infeasible model")
        return S

    def log_block_product(self, S) -> float:
        S = set(self._model(S))
        return float(sum(t.log_r[lookup[tuple(j for j in t.members if j in S)]]
                         for t, lookup in zip(self.tables, self._lookups)))

    def log_gamma0(self, S) -> float:
        S = self._model(S)
        return float(self.log_prior_by_size[len(S)] + self.log_block_product(S))

    def log_pi0(self, S) -> float:
        return self.log_gamma0(S) - self.log_Z0

    def probability(self, S) -> float:
        return math.exp(self.log_pi0(S))

    def discrepancy(self, S) -> float:
        S = self._model(S)
        return float(self._log_bf(S) - self.log_block_product(S))

    def log_gamma(self, S, phi: float) -> float:
        if not 0 <= phi <= 1:
            raise ValueError("temperature outside [0,1]")
        return self.log_gamma0(S) + phi * self.discrepancy(S)

    def sample(self, uniform: Callable[[], float], *, trace=None) -> Model:
        """I.3/I.4 draw order; trace(label, block, choice) is optional oracle QA."""
        def choose(lw, label, block=None):
            choice = categorical_log(lw, float(uniform()))
            if trace is not None:
                trace(label, block, choice)
            return choice
        remaining = choose(self.log_size_prob, 'pi0_size')
        sizes = [0] * len(self.tables)
        for b in range(len(self.tables)-1, -1, -1):
            if remaining == 0:
                break
            t = self.tables[b]
            lw = [t.log_profile[j] + self.log_A[b, remaining-j]
                  for j in range(min(len(t.members), remaining) + 1)]
            sizes[b] = choose(lw, 'pi0_block_size', b)
            remaining -= sizes[b]
        if remaining != 0:
            raise ArithmeticError("backward sampler failed to exhaust total size")
        model = []
        for b, (t, size) in enumerate(zip(self.tables, sizes)):
            if size:
                codes = t.by_size[size]
                selected = choose(t.log_r[list(codes)], 'pi0_submodel', b)
                model.extend(t.models[codes[selected]])
        return tuple(sorted(model))

    def sampler_path_log_probability(self, S) -> float:
        """Independent conditional-product identity for every model's unique path."""
        S = set(self._model(S))
        sizes = [len(S.intersection(t.members)) for t in self.tables]
        remaining = sum(sizes)
        out = float(self.log_size_prob[remaining])
        for b in range(len(self.tables)-1, -1, -1):
            if remaining == 0:
                break
            t, j = self.tables[b], sizes[b]
            normalizer = logsumexp([t.log_profile[a] + self.log_A[b, remaining-a]
                                   for a in range(min(len(t.members), remaining)+1)])
            out += t.log_profile[j] + self.log_A[b, remaining-j] - normalizer
            remaining -= j
        for t, lookup, j in zip(self.tables, self._lookups, sizes):
            if j:
                U = tuple(a for a in t.members if a in S)
                out += t.log_r[lookup[U]] - t.log_profile[j]
        return float(out)


def brute_force_pi0(start: CompositeStart, dps=80):
    """Independent mpmath full enumeration, I.2/I.3; no convolution/table reads.

    Promotes callback logBF double values to high precision, so this validates
    start arithmetic, not accuracy of an external scorer. Returns mp numbers.
    """
    import mpmath as mp
    with mp.workdps(dps):
        W = mp.fsum(mp.binomial(start.p, k) / (2 * mp.binomial(2*start.p-1, k))
                    for k in range(start.K + 1))
        masses = {}
        for S in enumerate_models(start.variables, start.K):
            members = set(S)
            bf = mp.fsum(mp.mpf(float(start._log_bf(tuple(j for j in C if j in members))))
                         for C in start.blocks)
            masses[S] = mp.exp(bf) / (2 * mp.binomial(2*start.p-1, len(S)) * W)
        Z = mp.fsum(masses.values())
        probabilities = {S: mass / Z for S, mass in masses.items()}
        return dict(log_Z0=+mp.log(Z), log_WK=+mp.log(W), probabilities=probabilities)
