# D1 — diagnosis numerics (component port, not production runs)

Script `numerics/d1_diag.py` (imports, does not edit, C-GROW `numerics/bvs_core.py` and W2-APP `numerics/n3b_fastls.py::ls_fast`);
raw output `numerics/d1_out.txt`, table `numerics/d1_results.csv` (74 runs), stdout `numerics/d1_stdout.txt`.
Python 3.13 (numpy 2.3.0, scipy 1.15.3). Seeds: SeedSequence([20261110, design, n, p, seed]).

Designs: G2E (2-D grid, exp(−‖Δ‖₂/1.2)), G2A (2-D separable AR(1), ρ = 0.6), TP15 / TP3 (Toeplitz (1+h)^{−1.5} / (1+h)^{−3}),
EBM (equicorrelated blocks ρ = 0.5, size ⌈3 log n⌉, one truth per block: s₀(g−1) ≈ 9 log n — logarithmic, but above
APP LOC-B's sufficient inequality s₀(g−1) ≤ (1 − δ₀) log n; the middle regime) [R07-5].
s₀ = 3, θ = (1, −0.8, 1.2), σ = 1; p = 400 (grids 20×20) and p = 900 (30×30) at n = 12800.

| design | p | n | #runs | extras in start mode (min–max) | max extra dist (grids: ℓ∞ grid distance, ≤ Euclidean ≤ √2·ℓ∞; TP: |i−j|; EBM: 0 = same group) [R07-16] | S₀ ⊆ start | LS0 final = S₀ | certified | path = extra deletions only | max path h | lattice sup h (est.) | 2 log p | c_n′ | q |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G2E | 400 | 800 | 4 | 4–7 | 2 | 4 | 4 | 4 | 3 | 15.9 | 22.0 | 12.0 | 10.4 | 63 |
| G2E | 400 | 3200 | 4 | 11–17 | 4 | 4 | 4 | 4 | 4 | 15.3 | 19.2 | 12.0 | 11.7 | 64 |
| G2E | 400 | 12800 | 4 | 22–27 | 3 | 4 | 4 | 4 | 4 | 11.5 | 15.9 | 12.0 | 12.9 | 70 |
| G2E | 400 | 51200 | 2 | 36–39 | 4 | 2 | 2 | 2 | 2 | 10.0 | 11.3 | 12.0 | 14.0 | 80 |
| G2E | 900 | 12800 | 2 | 25–27 | 3 | 2 | 2 | 2 | 2 | 12.6 | 13.9 | 13.6 | 14.5 | 70 |
| G2A | 400 | 800 | 4 | 7–17 | 3 | 4 | 4 | 4 | 4 | 13.2 | 20.5 | 12.0 | 10.3 | 65 |
| G2A | 400 | 3200 | 4 | 17–23 | 10 | 4 | 4 | 4 | 4 | 9.3 | 12.6 | 12.0 | 11.4 | 75 |
| G2A | 400 | 12800 | 4 | 26–31 | 5 | 4 | 4 | 4 | 4 | 11.0 | 14.7 | 12.0 | 12.7 | 80 |
| G2A | 400 | 51200 | 2 | 37–52 | 6 | 2 | 2 | 2 | 2 | 15.4 | 18.5 | 12.0 | 13.6 | 100 |
| G2A | 900 | 12800 | 2 | 28–36 | 6 | 2 | 2 | 2 | 2 | 9.4 | 11.5 | 13.6 | 14.1 | 88 |
| TP15 | 400 | 800–51200 | 14 | 0–6 | ≤ 10 | 14 | 14 | 14 | 14 | ≤ 11.4 | ≤ 12.5 | 12.0 | 13.1–15.9 | 15–63 |
| TP3 | 400 | 800–51200 | 14 | 0–3 | ≤ 2 | 14 | 14 | 14 | 14 | ≤ 13.7 | ≤ 13.9 | 12.0 | 13.1–17.3 | 15 |
| EBM | 400 | 800 | 4 | 4–6 | 0 (in truth groups) | 4 | 4 | 4 | 4 | 13.0 | 18.9 | 12.0 | 10.4 | 63 |
| EBM | 400 | 3200 | 4 | 11–13 | 0 | 4 | 4 | 4 | 4 | 13.0 | 17.0 | 12.0 | 11.6 | 66 |
| EBM | 400 | 12800 | 4 | 23–38 | 0 | 4 | 4 | 4 | 4 | 12.2 | 18.6 | 12.0 | 12.9 | 72 |
| EBM | 400 | 51200 | 2 | 59–64 | 0 | 2 | 2 | 2 | 2 | 9.5 | 14.6 | 12.0 | 13.8 | 90 |

h_{T,l} = (n−1)(RSS_T − RSS_{T∪l})/RSS_T (= Z²_{T,l}(1 + o(1)) for T ⊇ S₀); "lattice sup" is a LOWER estimate of
sup over T ∈ [S₀, S₀ ∪ Q̂] (Q̂ = start-mode extras ∪ the ≤ 60 nearest nulls; 200 random T + adversarial coordinate
ascent for 15 worst l). c_n′ = log(n+1) + 2 log p − 2 log(q+1) (GROW L2.2 threshold without its constant −4κ_E − 2).
TL margin (min truth-deletion loss in F along the path) ≥ 62 in every run.

## Readings (observations only; not proof)
1. **Start-mode growth** in d = 2 and in the middle regime: G2E extras/(log n) = 0.8, 1.7, 2.5, 3.4 for
   n = 800 … 51200; EBM extras 5 → 62 while log n = 6.7 → 10.8. These observations motivate relevance sets larger than
   (1 − δ₀) log n (EBM violates APP LOC-B's sufficient size inequality; (G4-χ) does not apply); they do not prove any
   asymptotic growth rate. EBM has g_n ≍ log n, so it is NOT in APP L5_VN (V2)'s rigorous obstruction regime
   g_n/log n → ∞ [R07-5].
2. **LS0 works on all 74 runs**: S₀ ⊆ start mode, the path deletes one extra per move (73/74; the exception at
   G2E n = 800 still ends at S₀ certified), ends certified at S₀ — the GROW L1 mechanism.
3. **Whole-lattice NA vs path**: the estimated lattice supremum (a LOWER estimate of the true lattice sup) exceeds the
   path maximum by at most 9.19 h-units per run (max at G2A, n = 800, seed 3; recomputed from d1_results.csv) [R07-6]; this
   observed gap does not bound the true lattice–path gap. The estimated lattice sup falls below c_n′ at the largest n for
   G2E/G2A(p = 900)/TP; for EBM and G2A(p = 400) at n = 51200 it is within 1–5 units of c_n′ (finite-n; the asymptotic
   slack c_n − 2 log p is ≍ log n). This is consistent with the proved conclusion of Lemma NA-R,
   max_{T,l} Z²_{T,l} ≤ 2 log p + o(log n) w.p. → 1 [R07-7].
4. Polynomial-decay Toeplitz at these n has small start modes (visible region small: the marginal-visibility count is
   10 → 52 for α = 1.5 and 0 → 12 for α = 3), so these runs do not probe the polynomial-|Q| regime; they are
   uninformative about the asymptotic obstruction for (b).
