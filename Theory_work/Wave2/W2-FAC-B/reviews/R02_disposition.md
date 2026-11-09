# R02 disposition (statement lock v2, Codex gpt-6.1-sol high: LOCK-WITH-CHANGES)

1. **Extended endpoints a_T, b_T for every retained set.** APPLIED (STATEMENT §3 now defines a_T, b_T with {∓∞} for all T,
   one-sided and empty configurations; (C2)(iii) asserted before each move including T_0). L4.1 already used the ±∞
   convention for all sets.
2. **Signed energy constant.** APPLIED: M > ϑᵀΣ̄_{S₀S₀}ϑ = ‖μ‖²/(n − 1) with Σ̄ = (1 − ρ)I + ρ11ᵀ (STATEMENT §2, L5.1).
3. **Bounded p; relevance-set wording.** APPLIED: STATEMENT "Uniformity in p_n" paragraph; L4.2 (crude regime
   p ≤ n^{1/200}, which contains bounded p, uses no balance argument; regimes are per-n with a common n₀, so no
   subsequence argument is needed). Relevance-set sentence replaced by "not automatic on this class and do not cover
   p ≫ log n (for bounded p the trivial relevance set [p] satisfies their size requirement)". The reviewer's fixed-p
   imbalance example is consistent with this: the balance argument is used only for p > n^{1/200}.
4. **Direct invariant test.** APPLIED: numerics/n6_gap.py asserts, at every pre-move set including T_0 and the one/two-extra
   states, a_T < x_T < b_T and deleted = {a_T < ξ < b_T} (extended endpoints), the move is a null deletion at a gap edge,
   and runs truth-complete-block layouts started at S* with N₀ ≠ ∅ (N₀ stays eligible for additions/swaps in the scan).
   R01 disposition item 2 is hereby completed (it previously overstated what N3/N5 tested).
Optional: max_swap_gain now recorded before the stopping test (cs_gain.py); it is positive (O(1)) on some runs, as R01
predicted, while best-swap-minus-best-deletion stays negative. PLAN: checkpoint trigger "after L4 or ~3 h" and
citation check before council restored.

Statement **v3 LOCKED** on these changes (R02's verdict was LOCK-WITH-CHANGES; the changes are wording/definitions and a
diagnostic, no claim was strengthened).
