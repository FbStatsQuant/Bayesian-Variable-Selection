# X8 — Start mode for one-factor designs with general loadings (claim (G1) of STATEMENT_T2)

Status: **PROVED (by this seat, unchecked)**; lemma check R12 (Codex Sol high, reviews/R12_X7X8X10_check_sol.md): **VERIFIED**. Falsification numerics: T2/numerics (paths only) and numerics/N5X_out.txt
(CS); the start-mode argument is the general-Σ form of X5 (iid) and FACB L2 (exact Gram).

Setting: STATEMENT_T2 §1–2 (models (G) and (R), (1F), (θ), (FS-G)); Υ_n = I (FACB L1.0; legitimate because (FS-G) is
stated in sign-corrected coordinates, R10 item 1). ψ_lo := 1 − λ_hi².
Population: λ_min(Σ_n) ≥ ψ_lo (Σ_n = λλᵀ + Ψ ⪰ Ψ ⪰ ψ_lo I), entries |Σ_jk| ≤ 1.

**The argument of X5 uses about Σ only:** (a) a uniform lower bound on λ_min of sample correlation submatrices
(here c₀ := ψ_lo/5); (b) uniform closeness of the sample partial covariance c_n^{sample}(U, l) (a Lipschitz function of
the ≤ (16 + s₀)² entries of R̂_V and of θ*_{S₀}) to its population value c_n(U, l), uniformly over |U| ≤ 15; (c) the
dichotomy "zero pair ⇒ r_lᵀμ = 0 exactly; otherwise |c_n(U, l)| ≥ c_FS" — which is now **hypothesis (FS-G)** instead of
FACB's compound-symmetry computation; (d) Gaussian noise conditionally on the design. Compound symmetry is not used
elsewhere in X5.

**Lemma X8.** Under (G) or (R), (1F), (θ), (FS-G), p ≤ n^{A₁} eventually with A₁ < ½ (R10 suggestion 3: the global
sample eigenvalue floor below uses r_n → 0): P(S* = [p] ∖ N₀ is the unique maximiser of γ₀)
→ 1.

*Proof.* (R): X5 verbatim with Σ_n in place of the CS matrix: the design event 𝒜_n uses Lemma CR (entrywise
|R̂_jk − Σ_jk| ≤ δ′_n; CR is distribution-free in Σ for Gaussian rows), sd concentration (unit population variances by
(1F)), and λ_min(R̂) ≥ c₀ (as X2.1: G^r ⪰ Ψ^{1/2}WΨ^{1/2} ⪰ ψ_lo N(1 − r_n)I with W ~ W_p(N, I) from the general-loading
rotation representation of X7; sd² ≤ 2). On 𝒜_n, for V = U ∪ {l} ∪ S₀, ‖R̂_V − Σ_V‖ ≤ (16 + s₀)δ′_n and
λ_min(R̂_V), λ_min(Σ_V) ≥ min(c₀, ψ_lo); the functional c(M, θ) = M_{l,S₀}θ − M_{lU}M_UU⁻¹M_{U,S₀}θ is Lipschitz on this
set (B⁻¹ − A⁻¹ = B⁻¹(A − B)A⁻¹, entries ≤ 1), so |c_n^{sample}(U, l) − c_n(U, l)| ≤ C(c₀, s₀, ‖ϑ‖)δ′_n uniformly; by (FS-G)
|c_n^{sample}| ≥ c_FS/2 on non-zero pairs for n ≥ n₀, and zero pairs are exactly zero. The noise events E^Z_1–E^Z_3 and
X5.3–X5.4 are unchanged (they use only λ_min ≥ c₀, the s² bounds and Gaussian noise given the raw design).
(G): the design is fixed; define the (G) design event as {R̂ = Σ_n, λ_min(R̂) ≥ ψ_lo ≥ c₀, θ* = ϑ⁽ⁿ⁾} — it holds
deterministically; X5.1's raw-sd condition is **omitted** (raw scales are irrelevant once θ* = D_xβ is the fixed
coefficient of model G; R15 item 1: raw design 2X with coefficients θ*/2 is admissible but has sd_j = 2). Then
c_n^{sample} = c_n, and the noise events E^Z_1–E^Z_3 (with Z the fixed design; s² bounds from ‖μ‖² = (n − 1)ϑᵀΣ_{S₀S₀}ϑ)
and X5.3–X5.4 apply unchanged. ∎

**Remark.** (FS-G) is the population "non-masking" condition of the general framework (W2-UNI (A3)) restricted to
block-local conditioning sets (|U| ≤ 15). It is a uniform-in-n population assumption; no genericity claim is made
here beyond the CS case (where it follows from STATEMENT.md (FS), FACB L2.1).
