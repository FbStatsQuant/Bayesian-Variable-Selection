# R06 (exhaustive sweep, fresh Codex gpt-6.1-sol high) — disposition, 2026-11-08 22:47
Counts: FATAL 0, MAJOR 4, MINOR 9, EDITORIAL 2. Verbatim: R06_sweep_codex.md. All 15 fixed; no objection recorded.
1. MAJOR P2 scope (general-h, certificate budgets) — FIXED: premise CONFIG (STATEMENT §1); L1 R.3′ adds default-𝓗 work
   and storage and Cert/Cert_M (declared polynomial certificate budget); P2 stated "within CONFIG".
2. MAJOR concurrency — FIXED: CONFIG declares a fixed number w of workers/scorers; scorer workspace term × w in M̄.
3. MAJOR allocation success — FIXED: MACH now explicitly assumes heap/stack/worker allocations succeed within the
   declared memory (operational premise, not derived from counting).
4. MAJOR finite-constant overstatement — FIXED: METHOD_REQUIREMENTS C separates the word-size limit (IDEAL-W) from the
   60-halving issue ("bound no longer excludes", attainability open).
5. MINOR constants — FIXED: "explicit polynomial shapes, implementation-dependent constants" in STATEMENT and L1.
6. MINOR allocation units/names — FIXED: named fields mem_gb, hours; mem_gb ≥ mem_n/2³⁰, hours ≥ time_n/3600.
7. MINOR N3 pair selection — FIXED: L5 Remark 5.4(0) says "selected pair", notes 7/51 coincident modes, other pairs not
   searched.
8. MINOR asymptotic regime presented as established — FIXED: labelled CONJECTURAL / heuristic.
9. MINOR Ψ asymptotic impossibility — FIXED: STATEMENT says N1 does not support Ψ at the tested configurations.
10. MINOR sampled maximum — FIXED (L3 Remark 3.6: ≈ 22.98–57,135, lower bound on the supremum).
11. MINOR rounding — FIXED (≥ 0.129).
12. MINOR LS0 centre count — FIXED (1 + (ℓ+1)(p + p²/4)).
13. MINOR v3_context assertions — FIXED (L2 S.3 (vi′)).
14. EDITORIAL D′ label — FIXED ("joint consistency with the delivery term"; delivery-free only for Prop. F).
15. EDITORIAL s₀ clash — FIXED (L5 constant renamed s_θ; STATEMENT updated).
