# L3 — The max-plus DP table; L4 — size selection

Status: PROVED; cross-family check: R02 CORRECT-WITH-MINOR-FIXES (Sol; evidence wording only, fixed).
Code: `CODE/cpp/v3_start.h:198-213` (quoted):
```
198  std::vector<std::vector<double>> M(J + 1, std::vector<double>(K + 1, NEG_INF));
199  M[0][0] = 0.0;
200  for (int b = 1; b <= J; ++b)
201    for (int k = 0; k <= K; ++k)
202      for (int j = 0; j < (int)mb[b - 1].size() && j <= k; ++j) {
203        if (M[b - 1][k - j] == NEG_INF) continue;
204        double v = (j == 0) ? M[b - 1][k - j] : M[b - 1][k - j] + mb[b - 1][j];  // empty block adds exact 0
205        if (v > M[b][k]) M[b][k] = v;
206      }
207  int kbest = -1; double vbest = NEG_INF;
208  for (int k = 0; k <= K; ++k) {
209    if (M[J][k] == NEG_INF) continue;
210    double v = D.logprior[k] + M[J][k];
211    if (v > vbest) { vbest = v; kbest = k; }  // strict: ties keep the smaller size
212  }
213  ModeResult res; res.lg0 = vbest;
```

## Definitions
For b ∈ {0,…,J} and k ∈ {0,…,K}, Ch_b(k) := the set of tuples (U_0,…,U_{b−1}) with U_c ⊆ C_c and Σ_c |U_c| = k
(then |U_c| ≤ k ≤ K, so |U_c| ≤ t_c = min(|C_c|,K) automatically and every ρ_c(U_c) is defined).
V_b(k) := max_{Ch_b(k)} Σ_{c<b} ρ_c(U_c), with V_b(k) := −∞ if Ch_b(k) = ∅. (Ch_0(0) = {()} with empty sum 0, Ch_0(k) = ∅ for k > 0.)

## L3 statement
Under (H1), (H2) (and (H4) for executing the C++): after line 206, `M[b][k]` = V_b(k) for all b ≤ J, k ≤ K. Moreover V_J(k) is finite for every k ≤ K,
and V_J(k) = max{Σ_b ρ_b(S_b) : |S| = k}.

## L3 proof
Induction on b. b = 0: line 198–199 give M[0][0] = 0 = V_0(0), M[0][k] = −∞ = V_0(k) for k > 0. ✓
Step b−1 → b (b ≥ 1). Row M[b][·] is written only in iteration b of line 200 and reads only row b−1, which is final.
Splitting a tuple in Ch_b(k) into (its first b−1 components, U_{b−1}) with j := |U_{b−1}| ∈ {0,…,min(t_{b−1}, k)} gives a
bijection Ch_b(k) ≅ ⊔_j Ch_{b−1}(k−j) × {U ⊆ C_{b−1} : |U| = j}, and the sum splits additively. Hence
V_b(k) = max_j [ V_{b−1}(k−j) + μ_{b−1}(j) ] over j ∈ {0,…,min(t_{b−1},k)} (−∞ + real = −∞; max of an empty set or of
only −∞ terms is −∞), using that the maximum of a sum of two independently chosen terms is the sum of their maxima.
The loop (202–206) ranges over exactly j ∈ {0,…,min(t_{b−1},k)} (`mb[b−1].size()` = t_{b−1}+1 by L2), skips the j with
M[b−1][k−j] = −∞ (these terms equal −∞ and do not change a max that starts at −∞), and otherwise forms
v = M[b−1][k−j] + mb[b−1][j] (for j = 0 the code omits the addition; mb[b−1][0] = 0 by L2, so v is the same value), and
keeps the running maximum starting from −∞ (line 198). By the induction hypothesis and L2 (mb = μ), M[b][k] equals the
displayed maximum, i.e. V_b(k). ✓
Finiteness and set form: the map S ↦ (S_0,…,S_{J−1}) is a bijection from {S ⊆ {0..p−1} : |S| = k} onto Ch_J(k), because
the C_b partition {0,…,p−1}. For k ≤ K ≤ p this set is nonempty, so V_J(k) = max_{|S|=k} Σ_b ρ_b(S_b) ∈ ℝ. ∎

## L4 statement
Under (H1), (H2) (and (H4) for executing the C++): `vbest` = `res.lg0` = max_{Ω_K} f, and `kbest` = k* = min{|S| : f(S) = max f}.

## L4 proof
By L3, M[J][k] ∈ ℝ for every k ≤ K, so line 209 never skips, and v_k := λ(k) + M[J][k] = max_{|S|=k} f(S). Lines 208–212
scan k = 0,1,…,K and replace (vbest, kbest) only on a strict increase, starting from vbest = −∞ < v_0. By induction on the
scan, after step k: vbest = max_{k'≤k} v_{k'} and kbest = the smallest k' ≤ k attaining it. At k = K: vbest =
max_k max_{|S|=k} f(S) = max_{Ω_K} f, and kbest = the smallest size k with v_k = max f, which is the smallest size of a
maximiser of f, i.e. k*. Line 213 sets res.lg0 = vbest. ∎

## Falsification
`numerics/lemma_probes.py` L3 probe: 300 random instances; for every prefix b = 1..J (blocks 0..b−1, indices relabelled
order-preservingly) and every feasible prefix size k ≤ min(K, |C_0 ∪ … ∪ C_{b−1}|), λ isolating size k makes `res.lg0` = M[b][k];
compared with V_b(k) by direct enumeration: 2,521 probes, 0 failures (seed 11). (Black-box output checks; row b = 0 and
infeasible cells are not probed.) L4: clause (a) checks in `run_checks.py` (`res.lg0` = max f and
|res.S| = k*) on the integer-table families (35,551 + 35,585 instances, seeds 20261108 and 7), 0 failures.
