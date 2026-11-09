# W2-FAC-PK — PLAN (v2, after R01)

## Route
1. **L0 imports.** FACB L1 closed forms re-read for K < p ≤ n − 1 (lemmas/L0_imports.md).
2. **L1 START (P1).** Exchange arguments at any maximiser: (a) saturation; (b) within-block order (gap × positive
   bracket); (c) water-filling from the population concavity gap of the block log-table plus a uniform perturbation
   bound; (d) no full regular block under (PK).
3. **L2 NEG (P2), key negative lemma.** Static scan bounds at every size-K set (deletions ≤ Δ_K; missing truth ⇒ swap
   gain ≥ c₃n; outside null with ξ ≤ −t_n ⇒ some swap gains ≥ ½log n + 2), counting of excluded block minima ⇒ the first
   ⌊n^β⌋ moves are swaps ⇒ no scored S₀ for caps ≤ |S̃₀| − s₀ − 2 + ⌊n^β⌋. No swap-selection rule used.
4. **L3 STATIC (P3), key positive lemma.** Events: tail counts, uniform multiplier floor (χ² union bound). For every T ⊇ S₀:
   truth moves negative; S₀ strict local max; 1 ≤ m ≤ log²n ⇒ best deletion gain ≥ (c_D − ε)log n (one-sided/two-sided
   cases via the centring identity); m > log²n ⇒ ≥ (½ − ε)log n (tail counting). Budget: F(S₀) − F(T) ≤ Σ_{k≤|T|}Δ_k
   for T ⊇ S₀, Σ_{k≤K}Δ_k ≤ K(½log n + 2.4) ⇒ m* ≤ (1 + δ)K; path ends at S₀. Phase A (start missing truths) O(log n).
5. **L4 assembly (P4, P5).** (H0) with A = 1; [OP], [M5-0], Lemma CAP; delivery (Lemma S, Proposition F/A2 with
   re-charged LS0 terms, pathwise inclusion); cost (LS0 worst-case terms only).
6. **P6** numerical, pending (W2-SIM R2). **F1** p ≫ n: W2-SIM R3, heuristic discussion in REPORT.

## Falsification numerics (done / to do)
L0/L1: pk_selftest (p > K cases), l12_check. L2: N1, N3 (lead swaps), l12_check, l2_chain (link-by-link, since t_n is
not reached at simulable n). L3: l3_static (gains on random/adversarial/path sets; budget), l3_trend (n-trend of the
worst large-m set). To do: a direct test of the one-sided/two-sided small-m bounds (L3(c)) on adversarial small sets.

## Review pipeline
R02 re-lock (fresh Sol high). Lemma checks: L0+L1+L2 (Sol xhigh, key negative lemma), L3 (Sol xhigh, key positive lemma),
L4 (Sol high). CHECKPOINT.md after L2/L3 checks. Mid-point (fresh Sol xhigh, statement + proofs only) → sweep (Sol xhigh)
→ council (Sol xhigh + Opus high; both ≥ 8.0, all six gates). Statuses: P6 stays numerical/pending whatever happens;
no clause is upgraded without its own checks.
