# W2-UNI — CHECKPOINT 1 (after statement lock), 2026-11-09 ~10:10 CST

**Locked target:** STATEMENT.md v1.1 (R01 Codex Sol high LOCK-WITH-CHANGES, 8/8 changes applied; reviews/R01_*).
* (A1) Gaussian rows, p ≤ n^A, exact LSF for the posterior; (A2) Σ = ΛΛᵀ + Ψ, Ψ metric-local (exponential decay along an
  arbitrary pseudometric of polynomial growth, spectrum in [c, C]); for k = 1 a bounded subset-exposure ratio κ ≤ κ̄;
  (A3) fixed s₀, beta-min, non-masking (PTV / TV-pop).
* Theorems: UNI-P (posterior, any k) = APP POST; PLR as the abstract engine; **UNI-0** (k = 0, any p ≤ n^A) via PLR;
  **UNI-1** (k = 1 with local Ψ, limsup log p/log n < α₀(κ̄) = 1/(2κ̄(κ̄ + 2))) — new, strictly contains FAC-A's class.
* k ≥ 2: Lemma OBS-k (naive route obstructed by pigeonhole) + absorption plan; FAC-B (CS, p ≤ n/2) as partial version.

**Done:** falsification numerics for LOCL (numerics/n1_out.txt: ℓ¹ localisation error decays exponentially in r in 4
geometries) and for the U-LOC identity/inequality on non-block Ψ (numerics/n3_out.txt: identity error ≤ 1.3e-14, 0
inequality violations in ~27k pairs).
**In progress:** L1_metric + L2_k0 (parallel Opus prover); L3_ULOC (key lemma, lead).
**Next:** lemma checks (Sol high; L3 Sol xhigh), CHECKPOINT 2 at the key lemma, mid-point, sweep, council.
**Estimate:** UNI-0 and UNI-1 both look closable; the exponent for heterogeneous loadings can be small (κ ≈ 3–6 in the
probes ⇒ α₀ ≈ 1/30–1/80); k ≥ 2 and k = 1 beyond α₀ stay open here (parallel tickets).

# CHECKPOINT 2 (key lemma), 2026-11-09 ~10:35 CST
* **Key lemma U-LOC proved and cross-family checked** (L3_ULOC v1.1; R03 Sol xhigh V-W-A, 1 MAJOR fixed: empty conditioning
  set for TL). Theorem UNI-1 reduction (L4_k1), delivery reduction F-UNI (L5), OBS-k (L6) checked in the same round.
* Pending: L1_metric (LOCL etc.) + L2_k0 from the parallel prover → R02 check; then mid-point (fresh Sol xhigh), sweep,
  CITECHECK, council. UNI-1 depends on LOCL/RB_M/CD_M exactly as stated in STATEMENT R1 (R03 confirmed nothing more is used).
