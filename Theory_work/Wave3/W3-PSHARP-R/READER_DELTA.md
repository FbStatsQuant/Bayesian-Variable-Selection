# READER_DELTA.md — W3-PSHARP-R (draft v0.1, 2026-11-15; RIDER_RULES §5, PROTOCOL_v4 H6)

For HQ → W3-READER. Read-only source: `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
(draft v0.1, W3-READER CP1), §3 "Theorem 3 — The rate cannot be improved", lines 158-200. Nothing here is written in
W3-READER's folder. Master claims: `W3-PSHARP-R:AE`, `W3-PSHARP-R:A2C` (`STATEMENT.md` v1.0 of this ticket; **not yet
proved or checked** — statuses at CP3), on top of `W3-PSHARP:A`@1.0.0 and `W3-PSHARP:B`@1.0.0.

## 1. Current reader text (W3-READER `READER_VERSIONS.md:166-180`, abridged)
(b) *(Orthogonal or Gaussian null columns.)* Assume (S1), s₀ fixed, **p → ∞**, ‖Xθ*‖² ≤ nM and ‖θ*‖² ≤ nM′ with fixed
M, M′, and either (N-orth) … or (N-gauss) … and p ≤ n^A. Then
  1 − π(S₀ | y) ≥ (1 − o_P(1)) (s₀ + 1) √(log p/(πn)).
Remark: "… the rate √(log n/n) is exact whenever log p ≍ log n". Honest limits (`:200`): "the expectation form of (b)
for every p (sharp2 rider T12) is not yet proved".

## 2. What changes
1. (b) gains an **expectation** display valid for **every p** (bounded p allowed), with a larger constant.
2. The assumption "p → ∞" moves from (b) as a whole to the in-probability display only.
3. The remark "exact whenever log p ≍ log n" is split: in probability as before; in expectation for every p.
4. A remark on the critical sparsity scale (orthogonal null columns only) is added.
5. The honest-limits note at `:200` is replaced (see §4).

## 3. New reader text (proposed)

(b) *(Orthogonal or Gaussian null columns.)* Assume (S1), s₀ fixed, ‖Xθ*‖² ≤ nM and ‖θ*‖² ≤ nM′ with fixed M, M′, and
either (N-orth) or (N-gauss) (as now). Then, for every p with s₀ < p (bounded or growing),
$$
\mathbb E\big[1-\pi(S_0\mid y)\big]\ \ge\ (1-o(1))\,(s_0+1)\,\frac{2(p-s_0)}{2p-1-s_0}\,\sqrt{\frac{\log\!\big(p\sqrt n/(s_0+1)\big)}{\pi n}},
$$
and, if moreover p → ∞,
$$
1-\pi(S_0\mid y)\ \ge\ (1-o_P(1))\,(s_0+1)\sqrt{\frac{\log p}{\pi n}}.
$$

*Consequences (remarks).* (As now for (a).) By (b) with p = n^a, E[1 − π(S₀ | y)] ≥ (1 − o(1))(s₀+1)√((a+½)/π)·√(log n/n),
and for fixed p, E[1 − π(S₀ | y)] ≥ c_p (s₀+1)√(log n/n) with c_p = 2(p − s₀)/((2p − 1 − s₀)√(2π)). So the factor √(log n)
is attained **in expectation for every p**, and **in probability whenever log p ≍ log n**; on these designs, which
satisfy the assumptions of Theorems 1–2, the rate √(log n/n) is exact in both senses there (conditional on Theorems 1
and 2). The extra √(log n) in expectation at bounded p comes from rare large gains of a single extra variable, not
from the number of competitors. If s₀ is allowed to grow, a posterior mean error of order √(log n/n) forces s₀ to stay
bounded, for every p. *(Critical scale, (N-orth) only.)* If (s₀ + 1)√(log p/(πn)) → λ ∈ (0, ∞) and s₀/p → 0, then
π(S₀ | y) ≤ e^{−λ} + o_P(1).

*Why each assumption* (one line each, replaces the (b) sentence at `:184-186`): the witness conditions make the
one-variable supersets behave as independent χ²₁ competitors; for the expectation display a single such competitor
already suffices (its heavy upper tail gives the √(log n)), for the in-probability display p → ∞ competitors are
needed (their maximum gives the √(log p)); energy and coefficient bounds keep the variance posterior on scale. These
are witnesses, not claimed necessary.

## 4. Honest limits (replaces `:200`)
"None for the statement. The expectation display holds for every p; whether its constant is attained is a numerical
observation only (ratio 0.99–1.03 at n = 10⁶ for p ∈ {2, 3, 5})." Until CP3: "the expectation display is proved by
rider T12, not yet checked".

## 5. Bridges needed

| # | bridge | mark | detail |
|---|---|---|---|
| B3.3 | (N-orth), s₀ fixed ⇒ (W-orth-E) with 𝒩 = [p]∖S₀ | NEW one line | (N-orth) gives N = p − s₀ ≤ n − 1 − r₀, so p ≤ 2n and (log p)² = o(n) (`STATEMENT.md` §2) |
| B3.4 | (N-gauss), (S2) p ≤ n^A, s₀ fixed ⇒ (W-sph-E) | NEW one line (extends B3.2) | (log p)² ≤ A²(log n)² = o(n); (r₀ + 1) log(pn) ≤ (s₀ + 1)(A + 1) log n = o(n); any number of null columns ≥ 1 |
| B3.5 | expectation display ⇐ Cor A1-E (`STATEMENT.md` §3.2) | EXISTS (at CP3) | display = A1-E main line; under (N-gauss) via the random-(X_{S₀}, θ*) clause of §3.1 with P(𝒜_n) → 1 (or = 1 if the energy and coefficient bounds are assumed surely) |
| B3.6 | in-probability display needs p → ∞ | EXISTS-CHECKED | `W3-PSHARP:A`@1.0.0, Cor A1 (PARENT STATEMENT :71-73), unchanged |
| B3.7 | "s₀ bounded" remark ⇐ Cor A2-E(ii); critical-scale remark ⇐ A2C | EXISTS (at CP3) | (N-orth)/(N-gauss) with 𝒩 = [p]∖S₀ and s₀ ≤ p/2; A2C: (N-orth), p → ∞ |

No internal ids appear in §3's reader text; (N-orth), (N-gauss), (S1), (S2) are W3-READER's own labels.
