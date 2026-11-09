Verdict: **VERIFIED-WITH-AMENDMENTS**.

I checked `lemmas/L3_static.md` against STATEMENT (P3), the listed PK/FACB imports, and FINAL s7's loop rule and prefix property. I found no fatal or major mathematical defect. The static argument and the budget prove P3 after the minor amendments below. Line numbers refer to the reviewed files; I have not edited the proof or changed git state.

1. **MINOR — Unfinished event/dependency declaration for STATIC(e).** Location: `L3_static.md:36–42`, propagated to `82–89` and `108–110`. The formal lemma assumes E1–E4, but (e) still says to add the N1 event used by its cited proof. Complete this dependency before locking the text. Either intersect with N1 and state its probability tends to one under PK′ alone, or, preferably, remove this unnecessary dependency: for every size-K set, E1 already gives |s_T| ≤ KH̄. The formula in L2.2(ii) therefore gives

   |t_j| ≤ O(n/K) + κ₁(H̄ + KH̄/(K + κ)) + O(n/K) = O(√n H̄)

   for every retained null j, uniformly over T. For a missing truth l, |t_l − t_j| ≥ cn, so V ≥ c′n² − O(n^(3/2)H̄) ≥ c″n². Together with α ≤ n² and ψ_T ≤ n, this proves the required swap gain ≥ c₃n using E1–E2 alone. Thus this is a repair of the stated dependency, not a counterexample to (e), and it does not require PK or PB.

2. **MINOR — Restore dropped error terms in the small-m displays.** Location: `L3_static.md:51–52` and `60–63`. At 61 the upper bound for (1 + γ_{k−1})d_T² includes O(L_nH̄), but the first gain inequality at 62 drops that error while retaining only O(log log n). That intermediate inequality is not established as written. With t := s₀ + κ, write instead

   G_del ≥ ½log n + ½h − ½(1 + C/log n)[t/(t + 1)]h − O(L_nH̄ + log log n).

   It implies the final bound already stated at 62–63, since L_nH̄ = o(log n). Also restore the harmless +log 2 + o(1) when substituting log p = ½h − L_n − log 2 into the addition bound at 51. Both corrections are absorbed by the final remainder; neither changes STATIC or P3.

3. **MINOR — Handle zero nearest distance before dividing by d.** Location: `L3_static.md:54–68`. The deterministic lemma is stated on E1–E4 without a nondegeneracy event. Those events do not exclude ξ_j = x_T, whereas the strict two-side/one-side split omits equality and Step 1 divides by d before Step 2 treats small d. Add an initial case d_T = 0: its deletion gain is exactly Δ_k ≥ ½log n − o(1), which satisfies both required bounds. Alternatively handle all d_T ≤ 1 first, using M1 and 1 + γ_{k−1} ≤ 2. Then perform the splits only when d > 1. No additional probability-zero event is necessary.

4. **EDITORIAL — Update stale status and import descriptions.** Location: `L3_static.md:3–5`, `28–29`, `108–110`, and `L0_imports.md:41–43`. The static numerics have been run; remove “to be run.” Cite the multiplier estimate in the proof of L2.2(iii), rather than suggesting that its statement is a multiplier lemma. L1(a) already uses a truth-free block, so the proposed replacement of “some regular block” is obsolete. Finally, L0's assertion that the only multiplier bound used in this ticket is a lower bound is stale: L3 explicitly needs upper bounds M1 and M2. Retain the exclusion of FACB's p ≤ n/2 residual-based upper bound, but distinguish it from the valid small-energy upper bound reused here.

The substantive checks are as follows.

**E4 and uniformity.** The projection identity is valid for every fixed T containing S₀: P_X − P_T is an orthogonal projector of rank p − |T|, even for the nonorthogonal CS columns. Thus its Gaussian quadratic form is χ²_{p−|T|}. The split at 24 holds for all sufficiently large n: if n − 1 − p < n/5, then p − K > 3n/10 − 1 ≥ n/4. In the other case the common residual r alone supplies the floor. With c = 2^(−9)/e, the union bound in the second case is at most

2^n(ce)^(n/8) = 2^(−n/8).

This overcomes the exponential number of sets. Independence between different T is unnecessary, and p = n − 1, where r = 0, is covered by the second branch. The stated c_M = c/4 and C_M = 2/c_M are conservative and valid. There is no hidden use of p ≤ n/2 here.

E3 is also valid. Its grid union costs O(n√log n) times n^(−3/2), which tends to zero; doubling for U₋ is harmless. Interpolation costs at most 2p/n ≤ 2, absorbed by the extra log n. E1 supplies the cutoff beyond H̄. Once these simultaneous events hold, the remaining inequalities are deterministic and require no further union over adaptively selected sets.

**Centring and small m.** The identity ∑_{R_T}(ξ_j − x) = x(s₀ + κ) − s_{S₀} + ϱ is exact. Its bound e_n = O(√log n) is uniform because s₀ and ρ are fixed, |ϱ| = O(L_n), and L_n = o(H̄). M2 applies throughout m ≤ m_e, including S₀.

For two occupied sides, d_T ≤ H̄ and m ≥ 2. Consequently γ_{k−1} ≤ 1/(s₀ + 1 + κ_∞), giving precisely c_D log n − O(log log n). For one occupied side, the essential coefficient is

(1 + γ_{k−1})[tH̄/(m + t)]² = t²h/[(m + t − 1)(m + t)] ≤ [t/(t + 1)]h,

where t = s₀ + κ. The maximum occurs at m = 1. This handles the delicate singleton case with its correct γ_{k−1}; applying the two-sided gamma bound to m = 1 would be invalid, but the proof does not do that. After amendment 2, the one-sided error is o(log n), and the claimed (c_D − ε)log n bound follows uniformly.

Truth-out negativity and strict local maximality of S₀ also check out. Truth residual coordinates are of order √n, uniformly separated from the O(√log n) null coordinates. At S₀, the null-addition likelihood gain is at most ½h + o(log n), while its size penalty includes ½log n + log p. The resulting negative margin is ½log n − o(log n).

**Large m and the mirror case.** For d > 1, the centring identity bounds the total distance on the less favourable side by the full upper-tail distance plus e_n. The layer-cake identity is correct, including the dU₊(a) boundary contribution. It gives

m ≤ 2U₊(a) + d^(−1)∫_a^H̄ U₊(u)du + e_n/d.

E3's additive term costs O(H̄ log n), not O(m log n). This is o(m) uniformly for m > ⌈log²n⌉, so absorbing it into half of m is legitimate. The Mills inequality used is in the correct direction: ∫_a^∞ Φ̄ ≤ φ(a) ≤ Φ̄(a)(1 + a²)/a. Since a > 1 and a = O(√log n), the polynomial factor loses only O(log log n), yielding a²/2 ≤ log(p/m) + O(log log n).

For m ≤ n^(1−c₀), the small-energy condition follows from n^(−c₀)log²n → 0. With M_T ≤ ½(1 + C/log n), the d² term cancels against a²/2; its multiplier and gamma errors are O(1) and O(1/log n), respectively. For m > n^(1−c₀), a² ≤ 2c₀log n + O(log log n). Substitution of c₀ = ε/(8C_M) gives a penalty at most (ε/2)log n + o(log n). Because ε, c₀, C_M are fixed before n tends to infinity, every stated error is eventually dominated. The possibly enormous onset is admissible in this asymptotic ticket.

The mirror argument is deterministic and remains valid with the offset and truths. Replace all ξ coordinates by their negatives, x by −x, s_{S₀} by −s_{S₀}, and ϱ by −ϱ. The centring error becomes −E_T with the same absolute bound; the relevant count becomes U₋. This does not require the transformed ϱ to be the offset generated by another model realization, nor any symmetry assumption on the truth coefficients. Only the displayed algebra and absolute bounds are used.

**BUDGET, phase A, and endpoint.** The sign in the score budget is correct:

F(S₀) − F(T) = ∑Δ_k + ν log(ψ_T/ψ_{S₀}) ≤ ∑Δ_k

for T containing S₀. Nested-model monotonicity gives quad_T ≥ quad_{S₀}, hence ψ_T ≤ ψ_{S₀}. This bound holds for every such T, not only path sets.

The combinatorial identity is exact: ∑_{k=1}^K log((2p − k)/k) = log binom(2p − 1,K). Since p ≤ 2K + 1, its bound per K is at most 1 + log(4 + 1/K), eventually below 2.39. The 2.4 constant therefore has sufficient slack, including the determinant increment errors. For 0 < ε < c_D/2 < 1/4, the ratio of the bulk budget to (½ − ε)log n is eventually at most (1 + 6ε)K.

Phase A cannot leave size K: additions are infeasible, all deletions gain at most Δ_K = O(log n), and a missing truth supplies a swap gaining c₃n. Finite strict ascent then forces entry into the family containing S₀. Afterwards every truth-out move is negative, and every other centre except S₀ has an improving null deletion. Thus the path stays in that family and ends at S₀. Local maxima of size below K without S₀ may exist elsewhere, but are unreachable by this argument and are not needed to be excluded. The endpoint argument does not use the phase-A move bound, so the later use of F(S₀) − F(C₀) to bound A_n is not circular.

At the first centre with m ≤ m_e, the remaining budget is O(m_e log n), hence the remaining number of moves is O(m_e), even if subsequent additions enlarge m again. Also A_n = O(log n). These overheads are o(K), because K = ⌊n/2⌋. With ε = min(δ/12,c_D/4), the bulk coefficient leaves at least δK/2 of slack to absorb them. FINAL s7 checks for no improvement before applying the cap test, so a cap equal to m* already certifies the terminal centre. Its prefix property therefore proves the certified-endpoint assertion uniformly for every permitted data-dependent cap. The proposed ℓ_n + 2K cap follows by choosing, for example, δ = 1/2.

**Falsification work.** I inspected `l3_static.py`, `pk_core.py`, all 988 saved static rows, and both saved summaries. None of those static rows has a nonpositive best null-deletion gain. Five lie below their nominal limiting coefficient; these finite-n deviations do not refute the asymptotic lemma. I reran `l3_trend.py` with the specified Python 3.13 interpreter; its output matches `L3_trend.txt` exactly.

Additional scratch checks exhaustively maximize d_T over every retained pair for three n = 8,000, p = 7,999 data sets: **95,916,021 pairs** in total, plus every singleton. The cases use (ρ,s₀) = (0.8,1), (0.95,1), and (0.5,4), with mixed truth signs in the last case. At the maximizing pairs, deletion gains divided by log n are approximately 0.7673, 0.3413, and 0.6078; the corresponding c_D values are 0.05556, 0.01282, and 0.33333. These searches found no counterexample, including at m = 1. I also checked the one-sided coefficient over 24 fixed (s₀,ρ) combinations and m = 1,…,1000, and exhaustively checked deletion upper bounds and the containing-truth score budget across 5,148 small size-K sets. The latter are algebra checks only, not tests of asymptotic onset or PK′; a weak-signal phase-A failure at n = 14 in the scratch output is not an objection to the theorem.

Reproducible scratch artifacts: `reviews/R04_scratch/check_l3.py`, `check_l3_results.json`, and `l3_trend_rerun.txt`. Only these scratch artifacts and this requested review file were written. **P3 survives the attempted falsification; apply amendments 1–3 before marking the proof checked.**
