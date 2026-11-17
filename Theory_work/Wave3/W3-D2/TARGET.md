# W3-D2 — TARGET (one page; 2026-11-17)

## Assumption map (Theorem 2X; reader form)
| hypothesis | where it enters | how | necessity reading |
|---|---|---|---|
| Gaussian rows N_p(m, Σ), Σ_jj > 0 | CorGb-plus proof steps 1–3 (`W3-MISR-R/lemmas/G2_corr.md`) | sample SDs, sparse eigenvalues, energy χ² | not known to be necessary (sub-Gaussian rows: audit candidate #3) |
| Gaussian noise ⫫ design, σ² > 0 | (N) → (GR^c | σ(X)) | exact contrast law | as Theorem 1 (open) |
| (A1) p ≤ n^A, s₀ fixed | size cutoff m♯_n, union bounds | as Theorem 1 | as Theorem 1 (`W3-PSHARP:B` for s₀) |
| (A2) floor on R, \|T\| ≤ 3(A+1)(s₀+1) log n | CorGb-plus floor on \|T\| ≤ k_n | (F₀), (F_λ), (F_w) ⇒ (OS) | floor on S₀-anchored small sets needed (row 1.1 why-lines); size 3(…) is an upper bound for k_n (N1 (i): ≤ 0.40 of it) |
| (A3) βᵀΣβ ≤ M₀σ² | energy (E^σ) | posterior of the variance on scale | some control necessary (row 1.1 counterexample) |
| (A3) ρ_n → ∞ | (BM^σ) | beta-min branch | order √(log n/n) believed necessary (numerics); a fixed liminf level suffices (CorGb-plus) |

## Parity (each main clause)
| clause | (a) PROGRAM goals | (b) closest published (Song–Liang 2015, Thm 2/3) | (c) best registered (row 1.2 masters) |
|---|---|---|---|
| E δ_n = O(r_n) | matches (p ≫ n, method as coded) | beats: they give screening in probability, no expectation rate | beats: row 1.2 is O_P |
| P(HPM/MPM ≠ S₀) = O(r_n) | matches | beats (exact selection with a rate) | beats (row 1.2: → 0, no rate) |
| floor size | matches | short in kind: they need no sparse floor of this form but assume Condition 1 (stronger moment form) — as row 1.2 | beats: 3(A+1)(s₀+1) log n vs 5(A+1)(s₀+1) log n |
| scope (Σ, β, σ² vary with n) | matches | beats (theirs fixed-order) | beats (row 1.2 fixes σ², bounded β) |
| vanishing floor allowed | — | — | **incomparable** [L1-2]: W2-APP:POST keeps a fixed floor on \|S\| ≤ min(p, s₀ + j₀) and allows ψ_n → 0 (ψ_n√n/(log n)^{3/2} → ∞) on \|S\| ≤ k̄_n; Theorem 2X needs a fixed c on \|T\| ≤ k_n (CorGb-plus's transfer uses one fixed floor); keep the old master as coexisting |
| status | — | — | **short**: conditional (CorGb-plus's conditions; W3-POST2:C ← W3-POST:Prop-LB unchecked) vs "clean" |

## Boundary numerics
`numerics/N1_floor_and_e2e.py` → `N1_out.txt`: (i) exact k_n vs 3(…) and 5(…) log n on 150 grid cases: max ratio 0.394;
(ii) end-to-end exact enumeration (p = 6) with Σ_n, σ_n² varying with n and Σ not a correlation matrix (outside the recorded
Theorem 2, inside Theorem 2X): E δ_n / r_n = 2.14, 1.58, 1.12, 1.15, 1.08, 1.07 at n = 50…1600; P(HPM ≠ S₀) = 0 at n = 1600.
A floor-size boundary cannot be simulated at small p (3(A+1)(s₀+1) log n > p); the floor's size is a proof device.
