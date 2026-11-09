# R03 — fresh statement-lock review of SINGLETON_TARGET.md (T1b-S / T2-S)

Reviewer: Claude Opus 5.5, independent; did not read LOG, REPORT, CHECKPOINT or R02. Date 2026-11-09.
Read: Wave2/Wave1C/Wave1 PROTOCOL.md, PKA STATEMENT.md, SINGLETON_TARGET.md, numerics/n3_singletons.py (+ n1_exact_grid.py adapter),
N3_singletons.jsonl, W2-FAC-B lemmas/L1_cs_reduction.md (L1.1–L1.3), production core `Scripts/SMC_BVS/core/cpp/v3_core.cpp`,
`v3_engine.h`, `v3_ledger.h`. Scratch: reviews/R03_scratch/s0two.py → s0two_out.jsonl (s0 = 2 variant, 8 runs).
This is a statement-lock verdict, not a proof certification.

## VERDICT: LOCK-WITH-CHANGES

S1 and S2 are well-posed after small repairs, plausible, and the size-only cap-miss argument is valid. But for s0 = 1 the
result has no bearing on D_n or on any consistency claim, because the production run scores every block subset, so
S0 = {0} is always scored. The scope text must say so. R1 below is required; an s0 ≥ 2 variant is recommended.

## Required fixes

**R1 (scope; blocking). For s0 = 1, S0 is in the all-scored set deterministically, under every partition.**
`cpp_final_run` calls `ingest_tables(led, *h)` (v3_core.cpp:408; also the calibration ledger at :613). `ingest_tables`
(:372–386) offers every block subset U with a non-NaN table entry to the ledger via `led.event(..., ME_TABLE)`, with
F = logprior[|U|] + log m(U). That is the full-model score of U. `Ledger::event` → `offer_stores` → `offer_hpm`
(v3_ledger.h:84–112). Every singleton {j} is a block subset, so S0 = {0} ∈ 𝒮⁺ for every partition. Then
D_n := P(potential output, S0 not scored) = 0 identically. More generally D_n = 0 whenever S0 ⊆ one block.
So S2's "merged LS0 misses S0" is only a statement about LS0's own scanned set. It refutes the literal T2 formula
"uniformly over partitions, P(LS0(a) scans S0) → 1" for s0 = 1. It does not obstruct D_n → 0, T3, or reported-HPM
consistency, for any partition. Required text changes:
- Define the event exactly. Let 𝒩_LS0 be the union of the closed flip/swap neighbourhoods N[C_t] over
  t ≤ min(a, m*). The claim is S0 ∉ 𝒩_LS0. Do not call it a scoring failure of the method.
- State that S0 ∈ 𝒮⁺ by table ingestion (cite the lines above), so D_n ≡ 0 in this model.
- Change "identifies whether a uniform-partition proof of the original cap can be true" to: "shows that a
  uniform-partition proof that **LS0 alone** scores S0 under cap ell+|S̃0| cannot hold; it does not bear on D_n".
- **Recommended:** add or substitute a variant S2′ with s0 = 2, θ = (1,1) (θ̄ ≠ 0), singleton blocks. Each truth then
  sits in its own block, so S0 = {0,1} is not a table model. This targets the LS0 route that a uniform-partition D_n
  proof would actually use. It still says nothing about D_n itself, since SMC or the final search may score S0.
  Scratch (s0two_out.jsonl): start size K, both truths in the start, all moves swaps then deletions, final = S0, and
  15, 14, 33, 33, 32, 25, 86, 54 initial swaps against the needed ell + 4 = 15/16. The same behaviour as s0 = 1. The
  size-only threshold becomes ell + s0 + 2 (see R3).

**R2 (well-posedness of S2).** "The first ⌈C log n⌉ uncapped moves" is undefined when m* < ⌈C log n⌉. The log base is
also unstated. Restate the claim as: E_n = {every move t ≤ min(m*, L_n) is a size-preserving swap}, with
L_n := ell + 3 (general s0: ell + s0 + 2). Optionally add the stronger m* ≥ L_n, or "every fixed C > 0, natural log".
The miss consequence needs only E_n. With natural logs, ⌈C log n⌉ ≥ ell + 3 eventually iff C > 1/ln 2, because
ell = ⌈log₂(n+p+1)⌉. "For every C" is stronger than needed. If kept, record that it is not what the consequence uses.

**R3 (the size-only argument, which is valid; state it in this form).** Code facts: centres C_0 … C_a are all scanned,
since the cap check `A.moves >= ell` comes after the scan (v3_engine.h local_search, ~l.407–410). Additions are skipped
at |C| = K (~l.397). LS0's cap is ell + |S̃0| (v3_core.cpp:472–475). Let k0 = |S̃0|. On E_n, for t ≤ min(a, m*):
|C_t| ≥ k0 − max(0, t − L_n) ≥ L_n − ell. This holds because each move lowers the size by at most one, the first L_n
moves keep the size, and t ≤ ell + k0. With L_n = ell + s0 + 2 this gives |C_t| ≥ s0 + 2. Every member of N[C_t] then
has size ≥ s0 + 1, so S0 ∉ N[C_t]. If m* < L_n, the size stays k0 throughout. No later deletion-only premise is used.
So the argument is valid for complete scans under EX-A, with no further premise. Two refinements:
- It needs only k0 ≥ s0 + 2 and E_n. "Truth retained", "null-null" and "size K" are not needed for the miss. They are
  proof devices for E_n, so do not list them as conditions of the consequence.
- The numerics follow this: in N3 every run misses iff initial swaps ≥ ell + 3. Example: n = 200, p = 170, ell = 9:
  11 swaps scores at t = 109 = a, while 12 swaps misses.

**R4 (S1 well-posedness).** ξ exists only on the enlarged probability space of FAC-B L1.1, where g = √ρ η1 + √(1−ρ) ξ.
State this. The selected set is coupling-free: the top K−1 nulls by g equal the top K−1 by z, given all null z_j > 0,
which holds w.p. → 1 since θ̄ > 0. The common level of ξ is determined only up to the conditional spread of η given g.
That spread is O_P(p^{-1/2}), so the limit φ(t)/q is coupling-independent. Say "in probability", and define
q_n = (K−1)/(p−1) → 1/(2c). Alternatively, state the claim coupling-free as a mean of (g_j − ḡ)/√(1−ρ). The values
match N3 (c = .6/.85/.98 → .30/.66/.78; observed .22–.37/.51–.69/.63–.80).

**R5 (dependency honesty).** "No other-ticket theorem is needed" is true for start selection only. S2's route uses the
exact CS closed forms: F depends on (|U|, A_U, B_U), plus the neighbour formulas with t_j = z_j − γ_k B_T. These are
FAC-B L1.2–L1.3, status "PROVED (by this seat, unchecked)" with R03 Sol VERIFIED-WITH-AMENDMENTS. Either cite that
status verbatim or re-derive the formulas in PKA. They are a few lines of Sherman–Morrison. L1 is not on STATEMENT's
"Not inherited" list, so citing it is allowed.

**R6 (tie/genericity premise).** Lexicographic ties have probability 0, because F is a non-constant real-analytic
function of ε on each comparison. Say so, or carry EX-A plus an a.s.-no-ties remark. The numerics only report float
ties.

## Hidden or false assumptions checked

- **Start (S1): sound.** With singleton blocks, γ0(S) = w(|S|) ∏ m({j})/m(∅) on |S| ≤ K. The start is therefore
  top-k by z_j² for the best k. Every null's marginal log BF is about 0.067n − ½ log n (ρ = .5, θ̄ = 1, σ = 1). The prior
  step costs log((2p−k)/k) = O(1). So the start saturates at K. The truth leads by λ₁ ≍ n against κ₁ max|ξ| ≍ √(n log n).
- **e4′/tie DP:** trivial for singletons (no ties a.s.).
- **Production partition:** the singleton partition must be injected. The production linkage on exact CS does not
  produce it, which is already acknowledged as NONPRODUCTION. Uniform-partition claims include it, since its block
  size 1 ≤ B.
- **Not false, but not needed:** "truth retained, no deletion" (see R3).

## Viability of S2 (heuristic, not a proof; to guide the proof)

From L1.3, at |T| = K with c_T ≈ the in-model mean (shrunk), write t = κ₁(ξ − m). Then:
- ΔF_swap(j→l) ≈ λ[(ξ_l−m)² − (ξ_j−m)²];
- ΔF_del(j) ≈ ½ log(n+1) + log((2p−K)/K) − λ(ξ_j−m)²;
- λ := n/(2R), where R = residual noise SS/σ² ≈ n − K·Var(ξ | ξ > t). Since R ≤ (n−1)(1+o(1)), λ ≥ ½ − o(1).

The swap beats every deletion iff λ max_out(ξ_l−m)² ≳ ½ log n + O(1). The out set is the bottom tail, with
max (ξ−m)² ≈ 2 log n, so the swap wins with margin, because 2λ ≥ 1 > ½. Truth-out moves cost about −n. The γ_k(t_l−t_j)²
cross term is O(log n / n) relative. Over O(log n) swaps, m and R drift by O(√log n / n) and O(log n), which is
negligible. The predicted swap count is ≈ p·Φ(m − √(log n/(2λ))) = n^{1−1/(4λ)+o(1)}, which is polynomial. For
n = 2000 this gives about 27 (c = .6) and about 85 (c = .98), against 24–31 and 110–127 observed. So "every fixed C"
is very likely true, and ell + 2|S̃0| has a large margin. The proof must:
- control the adaptive Q, including the .02 offset and ν = .01 + n/2;
- give an explicit uniform bound on min_in(ξ_j − m)² (nulls near the centre exist w.p. → 1);
- handle the bottom-tail maximum over a set of size (c−½)n, using order-statistic tails.

The fixed values ρ = ½, σ = 1, θ0 = 1 look unnecessary, since λ ≥ ½ holds generally. That is optional.

## Exact scope after fixes

Established if proved: for explicitly nonproduction singleton partitions, exact CS, p = ⌊cn⌋ with c ∈ (½, 1), and fixed
s0 (1 or 2 as stated), P(S0 ∉ 𝒩_LS0) → 1 with cap ell + |S̃0|. This refutes only the uniform-over-partitions version
of "LS0 alone scores S0".

Not established:
- failure on the production partition (OPEN);
- D_n > 0, which is false for s0 = 1, where D_n ≡ 0, and unaddressed for s0 = 2;
- failure of the full scored set, SMC, the final search, or HPM consistency;
- sufficiency or minimality of any doubled cap.

Finite N3 misses are diagnostics, not asymptotic counterexamples (2 seeds per cell).
