# L2 — Per-block per-size maxima and their argmax lists

Status: PROVED; cross-family check: R02 CORRECT (Sol).
Code: `CODE/cpp/v3_start.h:186-197` (quoted):
```
186  std::vector<std::vector<double>> mb(J);
187  std::vector<std::vector<std::vector<uint32_t>>> arg(J);
188  for (int b = 0; b < J; ++b) {
189    int top = (int)st.logprof[b].size() - 1;
190    mb[b].assign(top + 1, NEG_INF); arg[b].assign(top + 1, {});
191    for (int j = 0; j <= top; ++j)
192      for (uint32_t c : st.codes_by_size[b][j]) {
193        double v = st.logr[b][c];
194        if (v > mb[b][j]) { mb[b][j] = v; arg[b][j].assign(1, c); }
195        else if (v == mb[b][j]) arg[b][j].push_back(c);
196      }
197  }
```

## Statement
Under (H1), (H2) (and (H4) for executing the C++): for every block b, with t_b := min(|C_b|, K), for every j ∈ {0,…,t_b}:
μ_b(j) := max{ρ_b(U) : U ⊆ C_b, |U| = j} is a real number, `mb[b][j]` = μ_b(j), and `arg[b][j]` is the list of all codes
c with popcount(c) = j and ρ_b(c) = μ_b(j), in increasing numeric order, each once. In particular `arg[b][j]` ≠ ∅,
`mb[b][0]` = 0 and `arg[b][0]` = (0). (Here and below ρ_b(c) means ρ_b of the subset with code c.)

## Proof
By (H1), `logprof[b].size()` = t_b + 1, so `top` = t_b, and `codes_by_size[b][j]` (j ≤ t_b) lists every code
c ∈ {0,…,2^{|C_b|}−1} with popcount(c) = j exactly once, in increasing order (`CODE/cpp/v3_start.h:107-112`: codes are
scanned in increasing order and pushed into the list of their popcount); the list is nonempty since C(|C_b|, j) ≥ 1.
The code ↔ subset map U ↦ code(U) is a bijection between {U ⊆ C_b, |U| = j} and that list, and `logr[b][c]` = ρ_b(U)
∈ ℝ for these entries (H1).

Fix (b, j); let c_1 < c_2 < … < c_L be the list. Claim: after processing c_1,…,c_ℓ (ℓ ≥ 1), `mb[b][j]` =
max_{i≤ℓ} ρ_b(c_i) =: m_ℓ and `arg[b][j]` = (c_i : i ≤ ℓ, ρ_b(c_i) = m_ℓ) in increasing order.
ℓ = 1: initially `mb` = −∞ < ρ_b(c_1) (real), so line 194 sets mb = ρ_b(c_1), arg = (c_1). ✓
ℓ−1 → ℓ: v = ρ_b(c_ℓ). If v > m_{ℓ−1}: m_ℓ = v and c_ℓ is the only maximiser among c_1..c_ℓ; line 194 resets arg to (c_ℓ). ✓
If v = m_{ℓ−1}: m_ℓ = m_{ℓ−1}, the maximisers are the old ones plus c_ℓ; line 195 appends c_ℓ, which is larger than all
earlier codes, so the order stays increasing. ✓ If v < m_{ℓ−1}: nothing changes and m_ℓ = m_{ℓ−1}, c_ℓ is not a
maximiser. ✓ (Comparisons are exact by EX-A.)
At ℓ = L this is the statement. For j = 0 the list is (0) and ρ_b(∅) = `logr[b][0]` = 0 (`CODE/cpp/v3_start.h:95`), so
`mb[b][0]` = 0, `arg[b][0]` = (0). ∎

## Falsification
`numerics/lemma_probes.py` L2 probe: 1,500 single-block instances (|C| ≤ 6, K random, λ isolating one size j): the
frozen code's `res.lg0` = μ(j), `res.ties` = #maximisers, `res.S` = lex-min maximiser in all 1,500 (seed 11).
