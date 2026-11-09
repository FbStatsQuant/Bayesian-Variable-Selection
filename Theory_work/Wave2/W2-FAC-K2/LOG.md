# W2-FAC-K2 — LOG (dated running log)

* 2026-11-09 — Ticket opened (lead: Claude Fable 5.1, Claude Personal). Read Wave2/Wave1C/Wave1 protocols, FAC-B
  STATEMENT/REPORT/L1–L5, fac_core.py, FAC-A statement header, W2-APP §1/§4. Python: Python313 (numpy 2.3.0,
  scipy 1.15.3); the default `python` (3.15) has no numpy.
* Plan: numerics first (multi-class exchangeable designs, k = 2, 3; closed-form k-dimensional scanner validated against
  fac_core.scan), then STATEMENT v1 → lock.
* Pre-numerics analysis (to be tested, not claimed): with k classes the exact reduction has a k-vector centre
  X(T) = (R⁻¹ + Ñ_T)⁻¹(Ñ_T V̄_T + offset) (Bayesian shrinkage of class means; Ñ_T = diag(u_c/ψ_c)); a deletion in class d
  moves X along the d-th column of (R⁻¹ + Ñ)⁻¹ (exact Sherman–Morrison). Two predicted issues: (i) cross-class drift
  breaks FAC-B's exact interval invariant (proof-technique issue); (ii) a truth-free class c with effective
  κ_c = ψ_c/(conditional class correlation) < 1 may leave LS0 stuck at S₀ ∪ {j, l} (opposite extremes) when
  log p/log n > (1 + κ_c)/2 — a METHOD-level trap for the LS0 route. Both go to numerics N1/N2 first.
