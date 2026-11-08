# L7 — The e4 tie-aware DP (reference algorithm TDP), clause (f)

Status: PROVED; cross-family check: R05 CORRECT (Sol). Reference algorithm only: **not** in any code path of
the method (`STATEMENT.md` §0, §4). Exact arithmetic throughout (the e4 sentence asks for the "prescribed" maximiser, which
is defined by exact comparisons). Uses L1(iii) and the L3 argument.

## Algorithm TDP(I)
For IN, OUT ⊆ {0,…,p−1} disjoint, per block b and j ≤ t_b = min(|C_b|,K):
  μ_b^{IN,OUT}(j) := max{ρ_b(U) : U ⊆ C_b, |U| = j, IN ∩ C_b ⊆ U, U ∩ OUT = ∅}  (−∞ if the set is empty);
  M^{IN,OUT}[0][0] := 0, M^{IN,OUT}[0][k] := −∞ (k > 0),
  M^{IN,OUT}[b][k] := max_{0 ≤ j ≤ min(t_{b−1},k)} ( M^{IN,OUT}[b−1][k−j] + μ_{b−1}^{IN,OUT}(j) )  (b = 1..J, k ≤ K);
  Φ(IN, OUT; k) := λ(k) + M^{IN,OUT}[J][k].
1. V* := max_{k≤K} Φ(∅,∅;k); k* := min{k : Φ(∅,∅;k) = V*}.
2. IN := ∅, OUT := ∅. For i = 0, 1, …, p−1: if Φ(IN ∪ {i}, OUT; k*) = V* then IN := IN ∪ {i} else OUT := OUT ∪ {i}.
3. Return IN.
(Python transcription: `numerics/tdp.py`.)

## Statement
For every instance I (STATEMENT §1), TDP returns S*, and uses at most (p+1) evaluations of M^{IN,OUT}, each costing
O(Σ_b 2^{|C_b|} + J (K+1)²) = O(Σ_b (2^{|C_b|} + (K+1)²)) operations; in total O(p · Σ_b (2^{|C_b|} + (K+1)²)). It never
enumerates the elements of 𝒜*.

## Proof
*Constrained DP.* Let 𝒮(IN,OUT;k) := {S : |S| = k, IN ⊆ S, S ∩ OUT = ∅}. Claim: Φ(IN,OUT;k) = max_{S∈𝒮(IN,OUT;k)} f(S)
(−∞ if empty). The constraints are per element, and the blocks partition {0,…,p−1}, so S ∈ 𝒮(IN,OUT;k) iff every S_b
satisfies IN ∩ C_b ⊆ S_b, S_b ∩ OUT = ∅, and Σ_b |S_b| = k. The proof of L3 (split off the last block; the maximum of a sum
of independently chosen terms is the sum of the maxima; −∞ absorbs) applies verbatim with the restricted per-block
families, giving M^{IN,OUT}[J][k] = max{Σ_b ρ_b(S_b) : S ∈ 𝒮(IN,OUT;k)}; add λ(k). With IN = OUT = ∅, step 1 yields
V* = max_{Ω_K} f and k* as in L4.

*Invariant.* Let S* be the prescribed start mode. Inv(i): IN ∪ OUT = {0,…,i−1}, IN = S* ∩ {0,…,i−1} (hence OUT ∩ S* = ∅).
Inv(0) holds. Assume Inv(i) and process i. Always Φ(IN∪{i}, OUT; k*) ≤ V*, since it is a maximum of f over a subset of
Ω_K (k* ≤ K).
- If i ∈ S*: S* ∈ 𝒮(IN∪{i}, OUT; k*) (|S*| = k*, IN ∪ {i} ⊆ S*, S* ∩ OUT = ∅ by Inv(i)), and f(S*) = V*; so
  Φ = V*, i joins IN, and Inv(i+1) holds.
- If i ∉ S*: suppose some S ∈ 𝒮(IN∪{i}, OUT; k*) had f(S) = V*. Then S ∈ 𝒜* (size k*, maximiser). S ∩ {0..i−1} = IN =
  S* ∩ {0..i−1} (S ⊇ IN, S misses OUT = {0..i−1} \ IN), and i ∈ S \ S*, so min(S Δ S*) = i ∈ S. By L1(iii),
  lex_less(S, S*) with S ∈ 𝒜*, contradicting the minimality of S*. Hence Φ(IN∪{i}, OUT; k*) < V*, i joins OUT, and
  Inv(i+1) holds.
Inv(p) gives IN = S* ∩ {0,…,p−1} = S*. ∎

*Cost.* Each evaluation of M^{IN,OUT}: per block, one pass over the 2^{|C_b|} codes (membership tests by bitmasks) gives
all μ_b^{IN,OUT}(j); the convolution costs Σ_{b} Σ_{k≤K} (min(t_b,k)+1) ≤ J (K+1)². There is one evaluation in step 1
and one per i in step 2. No step lists more than one element of 𝒜*. (An incremental version recomputing only the block
containing i and a suffix/prefix split is possible; not needed.)

## Relation to the specification and to D9
This is the "greedy index-by-index route with a feasibility max-plus DP" that seats A and B sketched
(`NBH/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md:183`, "seat-derived, unchecked") and the W1PC2 D9 row ("take the
smallest maximising size, then include the smallest index whenever an optimal consistent completion exists",
`NBH/branch_snapshots/MEET-THM/evidence/W1_PC2/VERDICTS.md:198`, script `d9_tiedp.py` not in the repo). Floating point is
not covered: an implementation must compare Φ with V* using the same evaluation order as the code's ĝ, or the
lexicographic guarantee holds only under EX-A (cf. L-FP (v)).

## Falsification
`numerics/tdp.py` against brute force in every `run_checks.py` instance (integer-table families, 35,551 + 35,585 instances over two seeds, incl. exhaustive p ≤ 3,
truncation and K-binding families; 0 failures), in `cex_default_cap.py` (p = 44) and `cex_family.py` (m = 0..12).
