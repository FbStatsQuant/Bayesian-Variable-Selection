# I8 — Lean-readiness assessment (FR01 sixth item; assessment only, no formalisation done)

Status: assessment by this seat (unchecked), 2026-11-08. Source of the existing library: `NBH/branch_snapshots/L-LEAN/STATUS.md:1-15`
("lake build is green: 0 errors, 0 warnings, 0 sorry"; 101 declarations).

| core | finite/deterministic? | existing Lean coverage | gap to formalise |
|---|---|---|---|
| Composition (C) deterministic step + Markov | yes | `T21HPM.lean`: `hpm_eq_truth`, `markov_half`, `t21_C1` (2E₀δ₁ form) — "Ŝ is a maximiser of F over 𝒮 on Uᶜ (any tie rule)" | instantiate 𝒮 := 𝒮⁺ (LS0 union) and the strict output event 𝒪; the closure 𝒪 ∩ {S₀ ∉ 𝒮⁺} ⊆ {LS0 of R̄⁺ misses S₀} is a premise-level set inclusion (GUARD, OP-LS0) — formalisable as a hypothesis, not provable in Lean |
| Lemma LS (lattice descent of the production search) | yes | `T37Greedy.lean`, `T37Lattice.lean`: `theoremA1..A4`, `theoremA3_hpm`, `lemma0c` (abstract best-improvement search on a lattice) | a wrapper stating (D_S) with progress ties allowed, the move cap ℓ and the final scan (the "capped-scan interface" already named in the M5 card as "To add") |
| Tr-J(a) (truncated Beta moment) | finite inequality, but needs Beta/Gamma integrals and Wendel | none | Mathlib has Gamma and Beta integrals; Wendel's inequality is not in Mathlib (would need a log-convexity proof) — moderate |
| (E1), (E2) (determinant and quadratic-form algebra) | finite linear algebra | none | commuting-matrix identity and eigenvalue bounds for symmetric PD matrices: available in Mathlib (spectral theorem); moderate |
| Lattice margin case list (§8.3) | finite Gaussian conditional-variance algebra | none | closed forms for 4×4-type covariance blocks; feasible but tedious |
| Probabilistic steps (Tr-J(c), Lemma E (E3)–(E5), Lemma B/Λ Haar laws, Theorem R tails, T03♯, de-randomisation) | no (measure-theoretic, asymptotic) | none | out of reach at reasonable cost; stay prose (as for all main cards) |

**Assessment.** The finite deterministic skeleton of the theorem — (C) and Lemma LS — is already covered in abstract form
by sorry-free declarations; the missing pieces are two thin wrappers (output event / 𝒮⁺ instantiation; capped-scan
interface). Tr-J(a), (E1), (E2) are finite inequalities that are formalisable with moderate Mathlib work. The
probability layer is not Lean-ready. No new Lean obligation blocks this ticket's "done" definition.
