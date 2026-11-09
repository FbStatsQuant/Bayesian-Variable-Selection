# R02 disposition (re-lock, Codex Sol high: LOCK-WITH-CHANGES)

Reviewer reply verbatim: reviews/R02_relock_sol.md. All three required changes applied → STATEMENT v3, LOCKED.

1. **(P4) quantifier/allocation mismatch.** Applied: (i)–(ii) for every lower-bounded cap rule; (iii) delivery only for
   rules with the deterministic bound a(data) ≤ ℓ_n + 2K on every admissible input; examples restricted accordingly
   (ℓ_n + ⌈(1 + δ)|S̃₀|⌉ with 0 < δ ≤ 1). Same change in lemmas/L4_assembly.md §L4.2 and METHOD_REQUIREMENTS.md.
2. **Realised-work identity.** Applied: stated only for rules with a ≥ ℓ_n + |S̃₀| (all three named rules); the
   reviewer's counterexample (N1 row n = 600, p = 360, seed 0, rule ⌈1.001|S̃₀|⌉) recorded in (P5). L4.4 and
   METHOD_REQUIREMENTS "Transfer" also distinguish caps ≥ MR1 (scored-set containment) from caps ≥ ℓ_n (legacy transfer).
3. **Positive-theorem frontier K < p < K + 16s₀ + 1.** Applied: added to §0 and §5 (F2′) with the reviewer's example
   (one truth with 15 block-mates, p = K + 1: unsaturated start).
Optional suggestions applied: §6 now names FACB review files and verdicts and states that only FACB L4.0(d)'s small-energy
refinement is imported; stale L1 Remark 4 (TK) replaced.
