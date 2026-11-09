# W2-FAC-X — STATEMENT, Target 2 (general one-factor loadings)

Status: **v2 — LOCKED** (2026-11-09; R10 LOCK-WITH-CHANGES, required changes 1–4 applied, reviews/R10_disposition.md;
Corollary FAC-NCS narrowed to Δ_nH̄_n ≤ n^{−1/3} — R10 item 3; **v2.1 (flagged narrowing, R12 item 1): FAC-NCS restricted
to iid rows (R)** — its exact-Gram transfer imported an iid multiplier bound that is false for (G); exact-Gram general
loadings are covered by Theorem FAC-GL(G), exact CS by FAC-B). Separate from STATEMENT.md (Target 1, Theorem FAC-CS-iid,
v3 locked). Abbreviations as in STATEMENT.md; T2 = `Theory_work/Wave2/W2-FAC-X/T2/` (parallel prover's files).
All results asymptotic (scope rule). Written at the population level and as generally as the arguments allow (HQ
framing note, 09:45): the loadings are arbitrary in a compact subset of (0, 1) and may depend on n.

## 0. Diagnosis and scope

numerics/N2X_summary.md (64 paths) and T2/numerics/N_T2_summary.md (366 exact-Gram paths, r = 1–3 loading classes, λ from
0.1 to 0.98, log p/log n up to 0.87): every path from the full model is a pure null deletion ending at S₀. For general
loadings the whitened deletion statistic is |ξ_j − ℓ_jX_T| (ℓ_j = λ_j/√(1 − λ_j²)) with **one scalar centre X_T** but
loading-specific centres ℓ_jX_T, so FAC-B's single-centre gap invariant is unavailable. This statement locks what is
provable by (i) a uniform-over-all-sets argument (T2/L4r_path.md) and (ii) the Target-1 perturbation machinery for
nearly equal loadings (lemmas/X7). The full FAC-B-type range for fixed loading dispersion is **not** claimed (§4).

## 1. Setting

Score, prior, start mode, method and implementation premises exactly as STATEMENT.md §1 (method as merged, MR1 cap).
Two design models:
* **(G) exact Gram:** model G of FACB STATEMENT §1 (fixed design, θ* := D_xβ fixed), XᵀX = (n − 1)Σ_n.
* **(R) iid rows:** model R of STATEMENT.md §1 (rows iid N_p(m_n, Σ_n), fixed raw coefficients β, θ* = D_xβ random).
**One-factor population covariance (1F):** Σ_n = Υ_n(λλᵀ + diag(1 − λ_j²))Υ_n, Υ_n deterministic diagonal ±1,
λ = λ^{(n)} ∈ [λ_lo, λ_hi]^p with fixed 0 < λ_lo ≤ λ_hi < 1 (otherwise arbitrary, may depend on n).
ℓ_j := λ_j/√(1 − λ_j²), R := ℓ_hi/ℓ_lo, γ̄ := ℓ_hi²/(1 + s₀ℓ_lo²),
  **A_S := min{1/(2 max(1, γ̄)), 1/(2((1 + R)² − 1))}**   (A_S = 1/6 for compound symmetry).
Since s₀ ≥ 1, γ̄ < R² and max(1, γ̄) < (1 + R)² − 1, so in fact A_S = 1/(2(R² + 2R)) (R10 suggestion 1); both terms are kept
because they are the deletion and addition margins of the proof.

## 2. Hypotheses

* **(θ)** s₀ ≥ 1 fixed; sign-corrected truth coefficients (θ* for (G), β for (R)) equal a fixed vector ϑ ∈ (ℝ ∖ {0})^{s₀}
  on the support (zero-extended embedding as in STATEMENT.md (θ)); σ² > 0 fixed.
* **(FS-G) population non-masking (block-local; sign-corrected coordinates, R10 item 1):** with Σ⁰_n := Υ_nΣ_nΥ_n
  = λλᵀ + diag(1 − λ_j²) and the zero-extended sign-corrected coefficient vector ϑ⁽ⁿ⁾ (STATEMENT.md (θ)), put
  c⁰_n(U, l) := (Σ⁰_nϑ⁽ⁿ⁾)_l − Σ⁰_{n,lU}(Σ⁰_{n,UU})⁻¹(Σ⁰_nϑ⁽ⁿ⁾)_U — the population regression functional of the linear
  signal on a single population row (raw coefficients β for (R), θ* for (G)); the partial covariance in the original
  coordinates is Υ_{n,ll}c⁰_n(U, l). Assume: there is c_FS > 0 such that for all n ≥ n₀, every U ⊆ [p] with |U| ≤ 15 and
  every l ∉ U with (U, l) not a zero pair (zero pair: U ⊇ S₀ and l null), |c⁰_n(U, l)| ≥ c_FS (one constant, uniform in
  n, U, l). (For compound symmetry this is implied by STATEMENT.md (FS).)
* **(P-S)** limsup_n log p_n/log n < A_S. Fix A₁ with limsup_n log p_n/log n < A₁ < A_S, so p_n ≤ n^{A₁} eventually
  (R10 item 4).

## 3. Claims

**Theorem FAC-GL.** Under (G) or (R), (1F), (θ), (FS-G), (P-S) and the implementation premises — for a given
deterministic triangular array (loadings λ^{(n)}, supports, positions) within these hypotheses; n₀ may depend on ϑ, σ,
s₀, λ_lo, λ_hi, A₁, c_FS and the onsets of the hypotheses for the given array (R15 item 2); no simultaneity over
different loading arrays is asserted (R10 item 4); the path margin c of (G2) does not depend on c_FS:
* **(G1) start mode:** S* = [p] ∖ N₀ is the unique maximiser of γ₀ with probability → 1 (N₀ as in STATEMENT.md §1).
* **(G2) path (uniform form):** on events of probability → 1, simultaneously for every T with S₀ ⊆ T ⊆ [p]: if T ≠ S₀
  the best move is a null deletion with gain ≥ c log n; every addition at T has gain ≤ −c log n; every null-out swap is
  below the best deletion; every truth deletion and truth-out swap has negative gain; S₀ is a strict local maximum
  (the logarithmic margin c = c(λ_lo, λ_hi, s₀, A₁) > 0 is distinct from the truth-move constant, which also depends on
  ϑ, σ). Hence from every start between S₀ and [p] (in particular S*) the uncapped search makes
  exactly |T₀ ∖ S₀| null deletions and ends at S₀, and LS0 with the MR1 cap ends at S₀ certified. For (G) every chosen
  deletion is, among nulls of the same loading value, the argmin of |ξ_j − ℓ_jX_T|.
* **(G3)** D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n) (joint law for (R)).
* **(G4)** delivery: with Proposition F's premises/allocation (CAL-free), P(no output) = 0 and P(Ŝ⁺ = S₀) → 1.

**Corollary FAC-NCS (nearly equal loadings; standalone specification, R10 item 2).** Assume the design model (R) (iid rows; v2.1),
(1F) with Δ_n := max_j|λ_j − λ̄| for a fixed λ̄ ∈ (0, 1) and **(NCS) Δ_nH̄_n ≤ n^{−1/3}** (R10 item 3: slower dispersion
decay breaks the transfer's spacing event), (θ) on β, (P-½) of STATEMENT.md, (FS) of STATEMENT.md
for ρ := λ̄², and the implementation/delivery premises — **in place of** (P-S) and (FS-G). Then claims (C1)–(C4) of
STATEMENT.md hold with the CS reference centre x_T built from ℓ̄ := λ̄/√(1 − λ̄²) (κ, ϱ as in lemmas/X7 for (R)),
and with every occurrence of ϖ_n replaced by ϖ′_n := (1 + C₇)ϖ_n (constant C₇ = C₇(λ̄)) — in particular deleted nulls lie in (a_T − 4.3ϖ′_n, b_T + 4.3ϖ′_n) (lemmas/X7).

## 4. Not claimed / frontier

Fixed loading dispersion beyond A_S: the present estimates of the uniform-over-sets route yield A_S, and finite-n
numerical examples suggest a limitation of that route (no asymptotic necessity or sharpness is claimed; R15 item 3): T2 adversarial non-path sets with positive addition gains, e.g. CS at log p/log n = 0.33: +0.083 log n; a
two-class heuristic suggests sharpness of the addition threshold for worst-case configurations, not established); FAC-B's path route fails per loading class at (B2) (cross-class
drift accumulates hole asymmetry), (B1) (classes become one-sided) and (E-side) (minority-side deletions) — T2/NOTES.md
§2 with numerics. These are obstructions of the proof techniques, supported by finite numerical evidence; the method's paths behave in
all simulated data sets (N2X: 32 iid + 32 reference-mode paths; N_T2: 366 exact-Gram paths) — evidence, not a proof about
the asymptotic frontier. Loading dispersion between n^{−1/3}/H̄_n and fixed (beyond A_S) is not covered. k ≥ 2 factors: ticket W2-FAC-K2. Block-local Ψ: not covered (breaks the rank-one structure).

## 5. Proof map

(G2)(G): T2/L4r_path.md §L4r.0–L4r.3 (Lemma L4r-S). (G2)(R): lemmas/X9_iid_general.md (uniform perturbation transfer).
(G1): lemmas/X8_start_general.md. (G3), (G4): lemmas/X10_assembly_T2.md. Corollary FAC-NCS: lemmas/X7_near_cs_loadings.md.
