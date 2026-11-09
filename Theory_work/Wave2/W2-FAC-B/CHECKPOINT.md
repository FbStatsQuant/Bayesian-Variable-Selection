# W2-FAC-B — CHECKPOINT (key lemma proved and checked) — 2026-11-09 ~07:50 CST

**Target as locked (STATEMENT v3).** Theorem FAC-CS: exact-Gram compound symmetry Σ = (1 − ρ)I + ρ11ᵀ (up to column
signs), fixed ρ ∈ (0,1), p ≤ ⌊n/2⌋ (any sequence), fixed s₀ and coefficients with a generic no-cancellation condition
(FS); method v3.1 with LS0 cap ℓ_n + |S̃₀| (MR1). Claims: (C1) start mode = S* = [p] ∖ N₀ (the whole model minus at most
15 nulls sharing a block with all truths); (C2) the LS0 path from S* is a pure backward elimination of the m₀ nulls,
deleting at each step the null closest to an explicit centre x_T, the deleted nulls always forming an open gap around
x_T, additions failing by ≥ c log n, every swap below the chosen deletion, ending certified at S₀; (C3) D_n → 0 and
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; (C4) delivery P(Ŝ⁺ = S₀) → 1 under Proposition F's method/allocation (CAL-free).

**Why the route works (route B).** On factor designs every null block absorbs the factor signal through the
full-response tables, so the start mode is the whole model (N1, L2); GROW's O(log n) relevance set is impossible and the
LS0 cap must be ≳ |S̃₀| (MR1 is necessary on this route). For compound symmetry every neighbour's score is an exact
function of ξ_j − x_T with one common centre (L1). The path-restricted analysis (L4) uses only the sets the path visits:
gap structure + self-correcting asymmetry (L4.1), a sign-symmetric comparison of retained sums with symmetric top sets
(bulk), and the extreme-tail imbalance dynamics (end phase, margin c_D = ½ − 1/(s₀ + 1 + (1 − ρ)/ρ) > 0).

**Status of the pieces.**
| file | content | check |
|---|---|---|
| lemmas/L1_cs_reduction.md | exact closed forms, gains, centre, Q vs RSS | R03 Sol high VERIFIED-WITH-AMENDMENTS (2), applied |
| lemmas/L2_start.md | (C1) start mode = S* | R03 V-W-A (1), applied |
| lemmas/L3_event.md | event E_n, P → 1 | R03 V-W-A (5), applied |
| lemmas/L4_path.md | **key lemma (C2)** | **R04 Sol xhigh VERIFIED-WITH-AMENDMENTS, no fatal issue** (7), applied |
| lemmas/L5_assembly.md | (H0), (C3), (C4) | check pending (R05) |
Statement lock: R01 REJECT (swap margin false — fixed), R02 LOCK-WITH-CHANGES (applied) → v3 locked.
Numerics: N1–N6, N3b (all summaries in numerics/); finite-n exceptions documented.

**Left.** R05 (L5 check), independent mid-point (fresh Sol xhigh), exhaustive sweep, citation check, council.
Then REPORT with the frontier (S5 / general factors / iid rows / p > n/2: obstructions to the technique, N2 cap
evidence). **Estimate:** the target as locked should close; no narrowing foreseen.
