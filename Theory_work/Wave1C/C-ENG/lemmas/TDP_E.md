# Lemma TDP-E — the coded e4 fallback returns the lex-minimum of the enumeration's tie set

Status: PROVED (by this seat, unchecked) — submitted to the plan reviewer and the code reviewer.
Notation as in `Theory_work/Wave1/W1-N3/STATEMENT.md` §1 and `lemmas/L7_tie_aware_dp.md`.

## Objects computed by `start_mode` (CORE/cpp/v3_start.h, refactored into `mode_dp`)
* t_b = min(|C_b|, K). For j ≤ t_b: `mb[b][j]` = max over size-j codes of `logr[b][c]` (binary64 comparisons; NaN
  entries |U| > K never read since j ≤ K); `arg[b][j]` = the codes attaining it exactly (in increasing code order).
* `M[0][0] = 0`, `M[0][k] = −inf` (k > 0), `M[b][k] = max_{j ≤ min(t_{b−1}, k), M[b−1][k−j] ≠ −inf} v(b,k,j)` with
  v(b,k,j) := `M[b−1][k−j]` if j = 0 and `M[b−1][k−j] + mb[b−1][j]` otherwise (binary64 sum).
* k̂ := the smallest k with `logprior[k] + M[J][k]` maximal (strict `>` scan), V̂ that maximum.
* Tight edge (b, r, j), 1 ≤ b ≤ J: j ≤ min(t_{b−1}, r), `M[b−1][r−j] ≠ −inf`, v(b,r,j) == `M[b][r]` (exact equality of
  doubles; the same expression as in the enumeration).

## The enumeration's visited set
A tight path is (j_0, …, j_{J−1}) with r_J := k̂, r_{b−1} := r_b − j_{b−1}, every (b, r_b, j_{b−1}) tight, r_0 = 0.
E := {S : S ∩ C_b = U_b, code(U_b) ∈ arg[b][j_b], (j_b) a tight path}. By the code of `rec` (v3_start.h:217-237): it
visits exactly the elements of E (each once, since S determines (U_b) and hence (j_b)), and `res.S` = lex-min of the
visited ones. So with no truncation `res.S` = lex_min E; the uncapped enumeration (cap = ∞) always returns lex_min E.
All elements of E have size k̂ (Σ j_b = k̂).

## Algorithm TDP-E (`mode_tie_dp`)
For disjoint IN, OUT ⊆ {0..p−1}: allowed_b(j) := ∃ c ∈ arg[b][j] with (IN ∩ C_b) ⊆ U(c) and U(c) ∩ OUT = ∅.
reach[0][0] = true, reach[0][r] = false (r > 0); reach[b][r] = ∃ j: (b, r, j) tight ∧ allowed_{b−1}(j) ∧ reach[b−1][r−j].
feasible(IN, OUT) := reach[J][k̂].
IN = OUT = ∅; for i = 0..p−1: if feasible(IN ∪ {i}, OUT) then IN ∪= {i} else OUT ∪= {i}. Return IN.

## Hypotheses (carried over from W1-N3 STATEMENT §2, R01 #6)
(H1) encoding as W1-N3 (H1): `st.blocks` a partition of {0..p−1} into increasing lists (any block order), |C_b| ≤ 31,
`st.blk`/`st.pos` inverse of `st.blocks`, `st.logr[b][code(U)]` finite for |U| ≤ min(|C_b|, K) with `logr[b][0] = 0`
(entries with |U| > K may be NaN and are never read), `codes_by_size`/`logprof` as built by `build_start`,
`D->logprior` of length K+1 finite. (H2-FP) IEEE binary64, round-to-nearest-even, operations executed as written
(Makevars.v3: `-ffp-contract=off`), every intermediate sum of `mode_dp` finite. (H4) integer counters fit, allocations
succeed. The claim is about the doubles the code computes; it makes **no** claim of lexicographic optimality over all
rounded ĝ = `log_gamma0` maximisers (R01 #2: block {0,1}, K = 1, λ(1) = 2⁵⁴, ρ({0}) = 1, ρ({1}) = 2 gives ĝ({0}) = ĝ({1})
= 2⁵⁴ but E = {{1}}; both the old fast path and TDP-E return {1}). Under EX-A the claim specialises to S*.

## Claim
TDP-E returns lex_min E, in binary64, for every input on which `start_mode` runs (no assumption on block order, K, ties).
Under EX-A (exact arithmetic) E = 𝒜* (W1-N3 Theorem N3-code (b)), so TDP-E returns S*.

## Proof
(1) feasible(IN, OUT) ⟺ ∃ S ∈ E with IN ⊆ S and S ∩ OUT = ∅. (⇐) S ∈ E gives a tight path (j_b) and codes c_b ∈
arg[b][j_b]; IN ⊆ S and S ∩ OUT = ∅ restrict per block to IN ∩ C_b ⊆ U(c_b), U(c_b) ∩ OUT = ∅ (blocks partition the
index set), so allowed_b(j_b) for all b, and induction on b along the path gives reach[b][r_b] = true, in particular
reach[J][k̂]. (⇒) reach[J][k̂] = true unrolls (choose, at each level, a witness j) into a tight path with allowed_b(j_b)
for all b; choose witnesses c_b; S := ∪ U(c_b) ∈ E and satisfies the per-block constraints, hence IN ⊆ S, S ∩ OUT = ∅.
(2) E ≠ ∅: the enumeration's first branch always exists (M[J][k̂] finite, every finite M[b][r] is attained by some tight j,
and arg[b][j] ≠ ∅ whenever mb[b][j] is finite). (Also: `M[J][0] = 0` so k̂ exists.)
(3) Greedy invariant (as L7): Inv(i): IN ∪ OUT = {0..i−1}, IN = S_E ∩ {0..i−1}, S_E := lex_min E. If i ∈ S_E, S_E
witnesses feasible(IN ∪ {i}, OUT), so i joins IN. If i ∉ S_E and some S ∈ E were consistent with (IN ∪ {i}, OUT), then
S and S_E agree below i and i ∈ S ∖ S_E; both have size k̂, so lex_less(S, S_E) (W1-N3 L1(iii): for equal-size sorted
vectors, the one containing min(S Δ S') is lex-smaller), contradicting minimality. So i joins OUT. Inv(p): IN = S_E. ∎

(4) Consequence for the new `start_mode`: the enumeration fast path is unchanged; if it ends with count < cap
(`truncated` false) the result is lex_min E as before; if count ≥ cap, the result is replaced by TDP-E = lex_min E. So
the new `start_mode` returns lex_min E = the uncapped enumeration's result for every cap ≥ 1, and is byte-identical to the
old one whenever the old one was not truncated (and also when N = cap exactly).

## Cost
Each feasible() call: O(Σ_b (K+1)(t_b+1)) boolean work; each IN/OUT change re-evaluates allowed for one block: O(2^{|C_b|}).
Total O(p · J (K+1)(B+1) + p · 2^B). No element of E is listed.

## Falsification
`tests/test_tdp.R` (TDP-E vs uncapped enumeration on all random instances; vs brute force with the code's own ĝ on
integer-valued tables; W1-N3's p = 44 counterexample at cap 10⁶; the family of L6 at all caps ≤ 2^{m+1}+1).
