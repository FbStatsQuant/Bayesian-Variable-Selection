# L6 — Assembly of Theorem N3-code (a)–(d); the deviation family

Status: PROVED; cross-family check: R05 CORRECT (Sol). Uses L1–L5 (batch 1).

## Statement
Theorem N3-code (a)–(d) of `STATEMENT.md` v1.3 §3, and the deviation family:
for every integer m ≥ 0 the instance D_m below has N = 2^{m+1}, and for every cap with 1 ≤ cap ≤ 2^m the algorithm of
`start_mode` (and the frozen code, whenever (H4) holds for (D_m, cap)) returns `res.S` = E_m ∪ {2m+1, 2m+2} ≠ S* = E_m ∪ {2m, 2m+3}, where E_m := {0, 2, 4, …, 2m−2}.

**Instance D_m.** p = 2m + 4, K = m + 2, λ ≡ 0, blocks in this order: C_i = {2i, 2i+1} for i = 0,…,m−1, then
C_m = {2m, 2m+1, 2m+2, 2m+3} (last). Tables: ρ_i({2i}) = ρ_i({2i+1}) = 1, ρ_i({2i,2i+1}) = −10 (i < m); in C_m, with
positions 0,1,2,3 ↔ a = 2m, b = 2m+1, c = 2m+2, d = 2m+3: ρ_m({a,d}) = ρ_m({b,c}) = 5 (codes 9 and 6), every other
nonempty U ⊆ C_m with |U| ≤ min(4, K) has ρ_m(U) = −3. (Abstract tables; not claimed to be producible by the scorer.)
For cap = 10⁶ take m = 20 (2²⁰ = 1,048,576 ≥ 10⁶): p = 44, K = 22.

## Proof of (a)–(d)
(a) `res.lg0` = vbest = max_{Ω_K} f by L4 (line 213 assigns vbest, and nothing later changes `res.lg0`). By L5(D),
`res.S` is one of the processed sets, all of which lie in 𝒜* (L5(B)); at least one is processed (N ≥ 1, cap ≥ 1).
By L1(i), 𝒜* is the set of smallest-size maximisers of π₀.
(b) L5(C) and L5(D).
(c) If N ≤ cap, L5(D) processes min(N, cap) = N sets, i.e. all of 𝒜* (L5(B): the N leaves are in bijection with 𝒜*), so
`res.S` = lex_less-min of 𝒜* = S*. If `res.truncated` = false then N < cap by (b). Default cap: every element of 𝒜* has
size k*, so N ≤ C(p, k*) ≤ C(p, ⌊p/2⌋), and C(22, 11) = 705,432 ≤ 10⁶ (C(p,⌊p/2⌋) is nondecreasing in p); hence N ≤ cap
for all instances with p ≤ 22. (C(23, 11) = 1,352,078, so p ≤ 22 is the exact range of this sufficient condition.)
(d) If N > cap, L5(D) gives `res.S` = lex_less-min of the ≺_DFS-first cap elements of 𝒜*. That this can differ from S*
for every cap ≥ 1 follows from the family: given cap, pick m ≥ 0 with 2^m ≥ cap and apply the claim below.

## Proof of the claim on D_m
*Maximisers.* For S ∈ Ω_K, f(S) = Σ_{i<m} ρ_i(S_i) + ρ_m(S_m). Each inner term is ≤ 1, with equality iff S_i is a
singleton (ρ_i(∅) = 0, ρ_i(pair) = −10). The last term is ≤ 5, with equality iff S_m ∈ {{a,d},{b,c}} (ρ_m(∅) = 0, other
values −3; sub-models of C_m of size > K are not in Ω_K). So f ≤ m + 5, and f(S) = m + 5 iff every S_i is a singleton
and S_m ∈ {{a,d},{b,c}}; such S have |S| = m + 2 = K, so they lie in Ω_K and the bound is attained. Hence 𝒜 is exactly
this family, k* = m + 2, 𝒜* = 𝒜, N = 2^m · 2 = 2^{m+1}.
*S*.* Let X := E_m ∪ {a, d}. For Y ∈ 𝒜*, Y ≠ X: if Y ∩ {0,…,2m−1} ≠ E_m, let i be the smallest pair index where they
differ; then Y picks 2i+1 and X picks 2i, all smaller elements agree, so min(X Δ Y) = 2i ∈ X. Otherwise Y = E_m ∪ {b,c},
X Δ Y = {a,b,c,d} and min = a ∈ X. By L1(iii), X is the lex_less-minimum: S* = X = E_m ∪ {2m, 2m+3}.
*DFS prefix.* The last block C_m is the first coordinate pair of κ (STATEMENT §1): every S ∈ 𝒜* has |S_m| = 2 and
code(S_m) ∈ {6, 9}. All elements with code(S_m) = 6 (i.e. S_m = {b,c}) precede all with code 9 in ≺_DFS; there are 2^m
of them. Since cap ≤ 2^m, the ≺_DFS-first cap elements all contain b, hence differ from S* (which does not contain b). By (d) `res.S` is one of them, so `res.S` ≠ S*. Among the code-6 elements, the ≺_DFS-first one has every
inner code equal to 1 (position 0 = the smaller index 2i), i.e. it is E_m ∪ {b,c}, which by the argument used for S*
is also the lex_less-minimum of the whole code-6 family; it is the first processed set, so `res.S` = E_m ∪ {2m+1, 2m+2}.
(For m = 0: p = 4, K = 2, one block, N = 2, cap = 1: `res.S` = {1,2}, S* = {0,3}.) ∎

## Note on the specification
The spec (`NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md:150`) prescribes, on truncation, a "deterministic tie-aware
DP that returns the prescribed … maximiser"; `start_mode` (`CODE/cpp/v3_start.h:178-240`) has no such branch: after
truncation it returns `bestS` as in (d) and only sets `res.truncated`. No caller of `start_mode` exists in the production
tree (`SoP/02_method.tex:789`; the Rcpp export was removed, `CODE/README.md:15`).

## What this does and does not close
(a)–(c) prove N3 for the frozen `start_mode` conditionally on N ≤ cap (in particular whenever `res.truncated` is false),
under EX-A for its arithmetic; (d) shows the conditional is necessary on abstract tables and that the specification's
truncation fallback is missing. Premise e4 for the **emitted centre of an integrated LS0** is not discharged: LS0 and the
fallback are not in production code, the integration/replay (N2(c)) is open, D_m is not shown to arise from scorer
tables or on LH (it is not a counterexample to T38-b1-LH), and in native doubles even untruncated runs can miss the
rounded lexicographic choice (L-FP, "Consequence for the e4 fallback").

## Falsification
`numerics/cex_default_cap.py` (m = 20, cap = 10⁶) through the frozen code: `res.S` = {0,2,…,38,41,42}, ties = 10⁶,
truncated = 1; TDP and the closed form give S* = {0,2,…,38,40,43}; f = 25 for both (`out_cex_default_cap.txt`).
`numerics/run_checks.py` family `constructed/codelex-cap1-*` (within-block code ≠ lex ties with cap = 1) and all
truncation families: (d) prediction matched in every instance; 529 + ≈400 truncated instances per seed had
`res.S` ≠ S*. `numerics/cex_family.py`: D_m for m = 0..12, every cap ∈ {1, 2^m, 2^m + 1, 2^{m+1}} (0 failures; see file).
