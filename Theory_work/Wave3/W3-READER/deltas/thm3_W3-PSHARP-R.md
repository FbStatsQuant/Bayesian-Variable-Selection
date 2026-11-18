# Staged READER_DELTA for row thm3 — from W3-PSHARP-R (NOT IN FORCE)

**Status: pending W3-PSHARP-R CP3 (target Tue 11-17, latest Wed 11-18).** Source (read only):
`/home/fb31/BVS-wt/W3-PSHARP-R/Theory_work/Wave3/W3-PSHARP-R/READER_DELTA.md` **v0.3** (copied verbatim below, staged
2026-11-16; replaces v0.2; rebased on row thm3 section 0.2 @88f5dec). The checked text of row thm3 in `READER_VERSIONS.md` stays in force until that CP3 passes; then this text
replaces §3's reader statement (b), its consequences, the (b) "why" line and the honest-limits line, the bridges
B3.3–B3.7 are added, and the row's update log gets one line (tag STRONGER: expectation display for every p).

**W3-READER notes for the swap (card 6 scope rule: √log claimed only on the witness designs):**
*(v0.3 check, 2026-11-16: notes 1 and 2 are already met in v0.3 — "on these designs" for the growing-$s_0$ remark, and
the two witness sequences named; note 3 remains for the swap.)*
1. The remark "If $s_0$ is allowed to grow, a posterior mean error of order $\sqrt{\log n/n}$ forces $s_0$ to stay bounded,
   for every p" must read "… on these (witness) designs, for every p" (it comes from Cor A2-E(ii), which is stated under
   (N-orth)/(N-gauss)).
2. The phrase "on these designs, which satisfy the assumptions of Theorems 1–2" must follow S1-F6: name the two witness
   sequences that also satisfy the upper-bound assumptions (fully orthogonal, and i.i.d. $N(0,1)$ raw designs, fixed
   nonzero coefficients), as the current row does.
3. Statuses of `W3-PSHARP-R:AE`, `W3-PSHARP-R:A2C` quoted verbatim from the registry at the swap; B3.5, B3.7 become
   EXISTS-CHECKED only if those claims are PROVED-CHECKED.

---

# READER_DELTA.md — W3-PSHARP-R (draft v0.3, 2026-11-15, after CP1 conditions; rebased on W3-READER section 0.2 @88f5dec; RIDER_RULES §5, PROTOCOL_v4 H6)

For HQ → W3-READER. Read-only source: `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
(at commit 88f5dec), §3 "Theorem 3 — The rate cannot be improved" (commit 88f5dec, lines 246-295; W3-READER staged v0.2 of this file as
`deltas/thm3_W3-PSHARP-R.md`, pending CP3). Nothing here is written in
W3-READER's folder. Master claims: `W3-PSHARP-R:AE`, `W3-PSHARP-R:A2C` (`STATEMENT.md` v1.1, locked, of this ticket; proofs written in `lemmas/`, **not yet
proved or checked** — statuses at CP3), on top of `W3-PSHARP:A`@1.0.0 and `W3-PSHARP:B`@1.0.0.

## 1. Current reader text (W3-READER `READER_VERSIONS.md` at commit 88f5dec, §3 "Theorem 3", section version 0.2, lines 246-295)
(b) (`:257-266`) *(Orthogonal or Gaussian null columns.)* Assume (S1), s₀ fixed, **p → ∞**, ‖Xθ*‖² ≤ nM and
‖θ*‖² ≤ nM′ with fixed M, M′, and either (N-orth) … or (N-gauss) … and p ≤ n^A. Then
  1 − π(S₀ | y) ≥ (1 − o_P(1)) (s₀ + 1) √(log p/(πn)).
Consequences (`:268-275`, for sequences with s₀ ≤ min(K − 1, p/2) [S1-F5]): "… By (b) with p = n^a, the factor √(log n)
is attained. On the two witness sequences … the rate √(log n/n) is exact (conditional on Theorems 1 and 2) [S1-F6]. On a
general design only the order n^{−1/2} of part (a) is proved as a lower bound; a matching √(log n/n) lower bound on every
design is open (post-freeze rider POST2-R1) [H5-6]." Why each assumption (`:277-281`). Honest limits (`:294-295`): "the
expectation form of (b) for every p (sharp2 rider T12) is not yet proved".

## 2. What changes
1. (b) gains an **expectation** display valid for **every p** (bounded p allowed), with a larger constant.
2. The assumption "p → ∞" moves from (b) as a whole to the in-probability display only.
3. The remark "exact whenever log p ≍ log n" is split: in probability as before; in expectation for every p.
4. A remark on the critical sparsity scale (orthogonal null columns only) is added.
5. The honest-limits note at `:295` is replaced (see §4).

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

*Consequences (remarks), all for sequences with s₀ ≤ min(K − 1, p/2).* (Part (a) text unchanged, `:268-270`.) The
bounds in (b) are lower bounds **on the two witness designs only**. By (b) with p = n^a,
E[1 − π(S₀ | y)] ≥ (1 − o(1))(s₀+1)√((a+½)/π)·√(log n/n), and for fixed p, E[1 − π(S₀ | y)] ≥ c (s₀+1)√(log n/n) with a
constant c > 0 depending only on p and s₀. So on these designs the factor √(log n) is present **in expectation for every
p**, bounded p included, and **in probability whenever log p ≍ log n**. When log p = o(log n), nothing is claimed **in
probability**: the in-probability display then gives only order √(log p/n), and whether the √(log n) is present in
probability there is open. On the two witness sequences that also satisfy the upper-bound assumptions (as now, `:271-274`)
the rate √(log n/n) is exact in probability (conditional on Theorems 1 and 2), and in expectation wherever a matching
upper bound for the posterior mean error is available. The extra √(log n) in expectation at bounded p comes from rare
large gains of a single extra variable, not from the number of competitors. If s₀ is allowed to grow, then on these
designs a posterior mean error of order √(log n/n) forces s₀ to stay bounded, for every p. *(Critical scale, (N-orth)
only.)* If (s₀ + 1)√(log p/(πn)) → λ ∈ (0, ∞) and s₀/p → 0, then π(S₀ | y) ≤ e^{−λ} + o_P(1). On a general design only the
order n^{−1/2} of part (a) is proved as a lower bound; a matching √(log n/n) lower bound on every design is open
(post-freeze rider POST2-R1) (as now, `:274-275`).

*Why each assumption* (one line each, replaces the (b) sentence at `:279-281`): the witness conditions make the
one-variable supersets behave as independent χ²₁ competitors; for the expectation display a single such competitor
already suffices (its heavy upper tail gives the √(log n)), for the in-probability display p → ∞ competitors are
needed (their maximum gives the √(log p)); energy and coefficient bounds keep the variance posterior on scale. These
are witnesses, not claimed necessary.

## 4. Honest limits (replaces `:295`)
"The √(log n) lower bounds hold on the two witness designs only; on every design only order n^{−1/2} is proved
(part (a)). Whether the constant of the expectation display is attained is not proved." Until CP3: "the expectation
display is proved, not yet independently checked". (Note for HQ, not reader text: numerically the expectation constant
looks attained at fixed p, `numerics/ae_fixed_p_out.txt`.)

## 5. Bridges needed

| # | bridge | mark | detail |
|---|---|---|---|
| B3.3 | (N-orth), s₀ fixed ⇒ (W-orth-E) with 𝒩 = [p]∖S₀ | NEW one line | (N-orth) gives N = p − s₀ ≤ n − 1 − r₀, so p ≤ 2n and (log p)² = o(n) (`STATEMENT.md` §2) |
| B3.4 | (N-gauss), (S2) p ≤ n^A, s₀ fixed ⇒ (W-sph-E) | NEW one line (extends B3.2) | (log p)² ≤ A²(log n)² = o(n); (r₀ + 1) log(pn) ≤ (s₀ + 1)(A + 1) log n = o(n); any number of null columns ≥ 1 |
| B3.5 | expectation display ⇐ Cor A1-E (`STATEMENT.md` §3.2) | EXISTS (at CP3) | display = A1-E main line; under (N-gauss) via the random-(X_{S₀}, θ*) clause of §3.1 with P(𝒜_n) → 1 (or = 1 if the energy and coefficient bounds are assumed surely) |
| B3.6 | in-probability display needs p → ∞ | EXISTS-CHECKED | `W3-PSHARP:A`@1.0.0, Cor A1 (PARENT STATEMENT :71-73), unchanged |
| B3.7 | "s₀ bounded" remark ⇐ Cor A2-E(ii); critical-scale remark ⇐ A2C | EXISTS (at CP3) | (N-orth)/(N-gauss) with 𝒩 = [p]∖S₀ and s₀ ≤ p/2; A2C: (N-orth), p → ∞ |

No internal ids appear in §3's reader text; (N-orth), (N-gauss), (S1), (S2) are W3-READER's own labels.
