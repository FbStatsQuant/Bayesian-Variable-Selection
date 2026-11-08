# L5 — The capped enumeration visits exactly the ≺_DFS-first min(N, cap) elements of 𝒜* (key lemma)

Status: PROVED; cross-family check: R03 CORRECT (Sol). Attempt 2 (2026-11-08): (A) repaired after R02 (attempt 1 WRONG: the first
form of (A) omitted the final-prefix condition; counterexample in `reviews/R02_batch1_check_raw.md` §L5.1); re-checked R03: CORRECT.
Code: `CODE/cpp/v3_start.h:214-238` (quoted):
```
214  // enumerate all optimal choices backward; keep lexicographically smallest set
215  std::vector<uint32_t> choice(J, 0);
216  bool have = false; std::vector<int> bestS; long count = 0; bool trunc = false;
217  std::function<void(int, int)> rec = [&](int b, int r) {
218    if (trunc) return;
219    if (b == 0) {
220      if (r != 0) return;
221      std::vector<int> S;
222      for (int bb = 0; bb < J; ++bb) for (size_t t = 0; t < st.blocks[bb].size(); ++t) if (choice[bb] & (1u << t)) S.push_back(st.blocks[bb][t]);
223      std::sort(S.begin(), S.end());
224      ++count;
225      if (!have || lex_less(S, bestS)) { bestS = S; have = true; }
226      if (count >= cap) trunc = true;
227      return;
228    }
229    for (int j = 0; j < (int)mb[b - 1].size() && j <= r; ++j) {
230      if (M[b - 1][r - j] == NEG_INF) continue;
231      double v = (j == 0) ? M[b - 1][r - j] : M[b - 1][r - j] + mb[b - 1][j];
232      if (v != M[b][r]) continue;
233      for (uint32_t c : arg[b - 1][j]) { choice[b - 1] = c; rec(b - 1, r - j); if (trunc) return; }
234      choice[b - 1] = 0;
235    }
236  };
237  rec(J, kbest);
238  res.S = bestS; res.ties = count; res.truncated = trunc;
```

Notation: STATEMENT v1.3 §1 (𝒜*, N = |𝒜*|, S*, κ, ≺_DFS); L2 (μ_b, `arg`), L3 (V_b = M[b][·]), L4 (kbest = k*).
For S ⊆ {0,…,p−1}: s_b := code(S_b), R_b(S) := Σ_{c<b} |S_c| (so R_J(S) = |S|), P_b(S) := Σ_{c<b} ρ_c(S_c).

## Statement
Under (H1), (H2), (H3), and (H4) for the execution of the C++ (STATEMENT v1.2):
(A) Tightness characterisation. S ∈ 𝒜* ⇔ |S| = k* and P_b(S) = M[b][R_b(S)] for **every** b ∈ {0,1,…,J}
    (including b = J) and ρ_c(S_c) = μ_c(|S_c|) for every c ∈ {0,…,J−1}.
    (The b = J condition is essential: without it the conditions only say that each block choice is optimal for the
    allocation S happens to use; e.g. p = 2, K = 1, C_0 = {0}, C_1 = {1}, λ = (−10, 0), ρ_0({0}) = 1, ρ_1({1}) = 2:
    S = {0} satisfies the conditions for b ≤ 1 and all c, but P_2(S) = 1 < M[2][1] = 2 and S ∉ 𝒜* = {{1}}.)
(B) Call tree. Ignoring the truncation exits, the calls of `rec` form an ordered tree T whose leaves (calls with b = 0)
    are in bijection with 𝒜*: the leaf reached through choices (c_{J−1}, …, c_0) builds the set S with s_b = c_b, and
    every S ∈ 𝒜* is built by exactly one leaf. Line 220's `return` is never taken.
(C) Order. T's leaves are visited (in the untruncated traversal) in increasing ≺_DFS order of the sets they build.
(D) Truncation. With the truncation exits, exactly the first min(N, cap) leaves of T in traversal order are visited and
    processed by lines 221–226; afterwards no further leaf is processed. Consequently `res.ties` = min(N, cap),
    `res.truncated` = [N ≥ cap], and `res.S` = the lex_less-minimum of the ≺_DFS-first min(N, cap) elements of 𝒜*.

## Proof
(A) "⇐": by the b = J condition and |S| = k*, P_J(S) = M[J][R_J(S)] = M[J][k*] = V_J(k*) = max_{|S'|=k*} Σ_b ρ_b(S'_b) (L3), so f(S) = λ(k*) + V_J(k*) = max f (L4), and
|S| = k*: S ∈ 𝒜*. "⇒": let S ∈ 𝒜*. Then f(S) = max f = λ(k*) + M[J][k*] (L4), so P_J(S) = M[J][k*] = M[J][R_J(S)].
Backward induction: assume P_b(S) = M[b][R_b(S)] for some b ≥ 1 (true at b = J). Write j := |S_{b−1}|, so
R_{b−1}(S) = R_b(S) − j. Since (S_0,…,S_{b−2}) ∈ Ch_{b−1}(R_{b−1}(S)), P_{b−1}(S) ≤ V_{b−1}(R_{b−1}(S)) = M[b−1][R_{b−1}(S)]
(L3); in particular the right side is > −∞. Also ρ_{b−1}(S_{b−1}) ≤ μ_{b−1}(j) (L2). By the L3 recurrence (the term j
of the max), M[b−1][R_{b−1}(S)] + μ_{b−1}(j) ≤ M[b][R_b(S)]. Chaining,
P_b(S) = P_{b−1}(S) + ρ_{b−1}(S_{b−1}) ≤ M[b−1][R_{b−1}(S)] + μ_{b−1}(j) ≤ M[b][R_b(S)] = P_b(S).
All terms are real, so equality holds throughout; since P_{b−1}(S) ≤ M[b−1][R_{b−1}(S)] and ρ_{b−1}(S_{b−1}) ≤ μ_{b−1}(j)
and their sums are equal, both inequalities are equalities. This gives ρ_{b−1}(S_{b−1}) = μ_{b−1}(j) and P_{b−1}(S) =
M[b−1][R_{b−1}(S)], which continues the induction down to b = 1; at b = 0, P_0(S) = 0 = M[0][0] = M[0][R_0(S)] holds
trivially. Together with |S| = k* this is the right side of (A).

(B) Invariant (I) for a call rec(b, r) made with choice[b..J−1] = (c_b,…,c_{J−1}):
  M[b][r] ∈ ℝ,  r + Σ_{c≥b} popcount(c_c) = k*,  M[b][r] + Σ_{c≥b} ρ_c(c_c) = M[J][k*].
The root rec(J, kbest) satisfies (I): kbest = k* (L4), M[J][k*] ∈ ℝ (L3), empty suffix. If rec(b, r), b ≥ 1, satisfies
(I) and calls rec(b−1, r−j) at line 233 with choice[b−1] = c, then M[b−1][r−j] ≠ −∞ (line 230), so it is real;
M[b−1][r−j] + mb[b−1][j] = M[b][r] (line 232; for j = 0 the addition is omitted and mb[b−1][0] = 0); c ∈ arg[b−1][j], so
popcount(c) = j and ρ_{b−1}(c) = μ_{b−1}(j) = mb[b−1][j] (L2). Hence M[b−1][r−j] + ρ_{b−1}(c) + Σ_{c'≥b} ρ_{c'}(c_{c'}) =
M[J][k*] and (r−j) + j + Σ popcount = k*: the child satisfies (I).
No dead ends: every call rec(b, r) with b ≥ 1 satisfying (I) has at least one child. Indeed M[b][r] ∈ ℝ is, by the L3
recurrence, the maximum of finitely many terms M[b−1][r−j] + μ_{b−1}(j), j ≤ min(t_{b−1}, r), with M[b−1][r−j] ≠ −∞;
some j attains it, so that j passes lines 230 and 232, and arg[b−1][j] ≠ ∅ (L2), so line 233 makes a call.
Leaves: a call rec(0, r) satisfies (I), so M[0][r] ∈ ℝ, i.e. r = 0 (L3, b = 0); line 220 never returns. All entries
choice[0..J−1] were assigned on the path from the root (level b assigns choice[b−1] immediately before its recursive
call; the reset `choice[b−1] = 0` at line 234 runs after each j's inner loop, and every later recursive call from this
level is preceded by a fresh assignment `choice[b−1] = c` at line 233, so no leaf ever reads a reset entry). The set S built at lines 221–223
therefore has S_b = the subset with code c_b, |S| = Σ popcount(c_b) = k*, and Σ_b ρ_b(S_b) = M[J][k*] − M[0][0] = M[J][k*],
so f(S) = λ(k*) + M[J][k*] = max f: S ∈ 𝒜*.
Every S ∈ 𝒜* is reached: by (A), consider the path that at level b (b = J, J−1, …, 1) is at the call rec(b, R_b(S))
with suffix choices s_b..s_{J−1}. At level b, the loop reaches j = |S_{b−1}| ≤ min(t_{b−1}, R_b(S)); M[b−1][R_{b−1}(S)] =
P_{b−1}(S) ∈ ℝ, so line 230 does not skip; v = M[b−1][R_{b−1}(S)] + μ_{b−1}(j) = P_{b−1}(S) + ρ_{b−1}(S_{b−1}) =
P_b(S) = M[b][R_b(S)] by (A), so line 232 does not skip (exact comparison, EX-A); s_{b−1} ∈ arg[b−1][j] because S_{b−1}
is a maximiser of size j (A, L2). So rec(b−1, R_{b−1}(S)) is called with choice[b−1] = s_{b−1}. At b = 0 the leaf builds S.
Exactly one leaf: a leaf is identified by its sequence of (j, c) choices; j = popcount(c), so by (c_{J−1},…,c_0); this
sequence equals (s_{J−1},…,s_0) of the set it builds, and distinct sequences build distinct sets (blocks are disjoint and
U ↦ code(U) is injective). Within one level the pairs (j, c) are distinct (j ascending, and `arg[b−1][j]` has no
repetitions, L2), so distinct children carry distinct choice[b−1].

(C) T is an ordered tree: the children of a call are visited in the order in which the loops at lines 229 and 233
generate them — j increasing, and within j the codes of `arg[b−1][j]` in increasing order (L2) — i.e. in increasing
order of (popcount(c), c). A depth-first traversal of an ordered tree visits leaves in the lexicographic order of their
root-to-leaf child-label sequences. The label sequence of the leaf building S is
((|S_{J−1}|, s_{J−1}), (|S_{J−2}|, s_{J−2}), …, (|S_0|, s_0)), whose flattening is κ(S). Hence leaves are visited in
increasing ≺_DFS order of the sets built.

(D) `count` starts at 0 and is incremented exactly once per processed leaf (line 224) before the test at line 226. Let the
untruncated traversal visit leaves L_1, L_2, …, L_N (by (B), N leaves) in this order. Claim: in the actual run, L_i is
processed iff i ≤ min(N, cap). While `trunc` is false the code behaves exactly as the untruncated traversal (the checks
at lines 218 and 233 are inactive), so L_1, …, L_m are processed in order where m is the first index with count = m ≥ cap,
if such m ≤ N exists, i.e. m = cap when cap ≤ N; otherwise all N leaves are processed and trunc stays false. When trunc
becomes true at L_cap, the leaf returns (227); every ancestor frame returns immediately after its recursive call
(line 233 `if (trunc) return;`), and no new call is processed (line 218), so no leaf after L_cap is processed. Thus the
processed leaves are L_1..L_{min(N,cap)}, `count` = min(N, cap), `trunc` = [cap ≤ N].
Selection: line 225 replaces bestS iff it is unset or S is lex_less-smaller; the processed sets are distinct and of
common size k* (B), so lex_less is a strict total order on them (L1(iii)) and after the last processed leaf bestS is
their lex_less-minimum; `have` becomes true at L_1, which exists since N ≥ 1 (𝒜 ≠ ∅) and cap ≥ 1. Line 238 copies bestS,
count and trunc into res. With (C), the processed sets are the ≺_DFS-first min(N, cap) elements of 𝒜*. ∎

## Falsification
`numerics/lemma_probes.py` L5 probe: 400 random instances with heavy ties; for each, cap = 1, …, min(N, 60): the frozen
code's (res.S, ties, truncated) equals the prediction "lex-min of the ≺_DFS-first cap elements" in 1,551/1,551 runs.
(These are output/count/flag checks of the predicted prefixes; they do not observe the non-record visits, so they do not
by themselves recover the full visiting order — (C) is proved, not inferred from them.)
`run_checks.py` clauses (b), (d-prediction) on the integer-table families (exact in binary64) incl. `cap_edge(N−1,N,N+1)` (35,551 + 35,585 instances, two seeds), 0 failures.
