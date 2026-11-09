# L1 — Theorem MIS (i)–(ii): reduction to T03♯ and de-randomisation

Status (per claim; lead's label "PROVED (by this seat)" + checks): Lemma R, MIS (i), Lemma DR — R02 VERIFIED; MIS (ii)/(ii′) —
R02 VERIFIED-WITH-AMENDMENTS (applied, reviews/R02_R03_disposition.md); Corollary N — added after R04, R05
VERIFIED-WITH-AMENDMENTS (applied, reviews/R05_disposition.md). Sweep R06 fixes applied. Council pending.
Notation of STATEMENT.md §§1–2.

## L1.0 What T03♯ assumes (read from its sources)

T03♯ (TH09; SoP `04_theory.tex:776-782`; proof T03R §6, `PROOF.md:160-207`) is a statement about the exact posterior π
of the shipped target computed from raw data (X^r, y^r) with p columns, under:
* **G** (`Docs/Theory/theorems/00_COMMON.md:35`): fixed design; ε ~ N_n(0, σ*²I), σ*² > 0 fixed; intercept removed by
  contrasts. The statistical model is y^r = α*1 + X^rβ* + ε, μ = CX^rβ* = Xθ*, θ* = D_xβ*, S₀ = supp β*
  (`00_COMMON.md:14`).
* R1, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞ or BM(c > c₀): conditions on (X, θ*, σ*², s₀, p) only
  (SoP `04_theory.tex:776-779`; T03R `PROOF.md:129-134,162-164`).
* Its conclusions (T03R `PROOF.md:168`) are statements about the law of y ↦ π(· | X, y) (and functions of it: PIP, MPM,
  S†) under that model.

Nothing else about how y was generated enters: the proof uses only the Gaussian law of e = Uᵀε (with variance σ*²), the
mean μ_c = X_cθ* ([P3] lem:red(b)), and the design. In particular the value α* is irrelevant: π depends on y^r only
through Cy^r (standardisation centres y^r; `00_COMMON.md:9`), and C1 = 0.

## L1.1 Lemma R (exact reduction). Fixed candidate design.

**Statement.** Let X^r_𝒞 be fixed (non-constant columns) and assume GR: ω = a1 + X^r_𝒞γ + ξ with ξ ~ N_n(0, τ²I)
independent of ε ~ N_n(0, σ²I). Then
  y^r = (α + a)1 + X^r_𝒞β^𝒞 + ε′,  ε′ := ε + ξ ~ N_n(0, σ_𝒞²I),  σ_𝒞² = σ² + τ²,
so the law of (X^r_𝒞, y^r) — and hence, jointly with the independent uniforms, the law of every output of the method run
on (X^r_𝒞, y^r), in particular of π_𝒞(· | y) — is **identical** to its law under the G-model with design X^r_𝒞,
intercept α + a, coefficient β^𝒞 and noise variance σ_𝒞².

*Proof.* The display is algebra: y^r = α1 + X^r_𝒞β_𝒞 + a1 + X^r_𝒞γ + ξ + ε. ε and ξ are independent centred
Gaussian vectors with covariances σ²I and τ²I, so ε + ξ ~ N_n(0, (σ² + τ²)I). The method and π_𝒞 are measurable
functions of (X^r_𝒞, y^r) and of the uniforms (STATEMENT §1: the method is run on (X^r_𝒞, y^r) only), and the uniforms
are independent of (ε, ξ). ∎

**Remark (τ² = 0).** τ² = 0 is allowed (then ξ = 0 a.s. and ω is an exact linear function of the candidates); then
σ_𝒞² = σ² and the problem is the well-specified one with truth β^𝒞.

## L1.2 Theorem MIS (i)

Assume GR with fixed X^r_𝒞 and (H-MIS): the T03♯ hypotheses with (p, S₀, s₀, θ*, μ, σ*²) := (p_𝒞, S₀^𝒞, s₀^𝒞,
θ^𝒞, μ^𝒞, σ_𝒞²), where S₀^𝒞 = supp β^𝒞 = supp θ^𝒞 (D_x is diagonal with positive entries) and s₀^𝒞 ≥ 1 fixed
(TH09's R1 requires s₀ ≥ 1, SoP `04_theory.tex:775`).

*Proof.* By Lemma R the posterior π_𝒞(· | y) has the law it has under the G-model (X^r_𝒞, β^𝒞, σ_𝒞²); in that model
the truth is S₀^𝒞 and the T03♯ hypotheses hold by assumption. Each conclusion of T03♯ (T03R `PROOF.md:168`, (i)–(iv)) is
a statement about the law of a function of π_𝒞 (or a deterministic inequality valid for every data set), so it holds
verbatim with S₀ := S₀^𝒞, θ* := θ^𝒞, σ*² := σ_𝒞²:
1. 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n);
2. max_j |PIP_j − 1{j ∈ S₀^𝒞}| ≤ 1 − π_𝒞(S₀^𝒞 | y) for every data set (with s₀^𝒞 ≤ K), and P(MPM_𝒞 = S₀^𝒞) → 1;
3. P(S†_𝒞 ≠ S₀^𝒞) ≤ 2E[1 − π_𝒞(S₀^𝒞 | y)] → 0;
4. without BM, for fixed c > c₀(s₀^𝒞, A) and J_n^𝒞(c) := {j ∈ S₀^𝒞 : θ^𝒞_j² ≥ cσ_𝒞² log n/(nφ₀²)}:
   π_𝒞(S ⊉ J_n^𝒞(c) | y) = O_P(r_n).
**Proxies and cancellations.** If j ∈ S₀^𝒞 ∖ S₀ then 1 − PIP_j ≤ 1 − π_𝒞(S₀^𝒞 | y) → 0 in probability; if
j ∈ (S₀ ∩ 𝒞) ∖ S₀^𝒞 then PIP_j ≤ 1 − π_𝒞(S₀^𝒞 | y) → 0 (item 2). ∎

**Remarks.** (a) The beta-min threshold is on the *projected* coefficients and scales with σ_𝒞² = σ² + τ²: omitted
signal raises the detection threshold (dilution). Since σ_𝒞² is a fixed constant, BM-∞ for σ_𝒞² is equivalent to BM-∞
for σ²; the difference matters for BM(c) and for J_n^𝒞(c). (b) All convergence claims are asymptotic, with thresholds depending on the stated constants and envelope/onset
sequences; TH09's ≈ 2·10⁶ illustration (SoP `04_theory.tex:811`) is not a universal threshold and is not transferred. (c) If s₀^𝒞 = 0 (β^𝒞 = 0) the target is the empty model; TH09 as carded
requires s₀ ≥ 1, so this case is not claimed here.

**Corollary N (the naive targets are wrong whenever a proxy or a cancellation exists).** Under the hypotheses of (i):
for every model T ∈ Ω_𝒞 with T ≠ S₀^𝒞, π_𝒞(T | y) ≤ 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n). In particular, if
S₀ ∩ 𝒞 ≠ S₀^𝒞 (some candidate null in the full model has γ_j ≠ 0, or some true candidate is cancelled), then
π_𝒞(S₀ ∩ 𝒞 | y) → 0 in probability (convention: π_𝒞(T | y) := 0 for T ∉ Ω_𝒞, so the bound covers every wrong subset).
Sample projection: let T_n be the support of the candidate slopes of the least-squares projection of the realised
y-mean on [1, X^r_𝒞] (unique when the centred candidate matrix has full column rank). Under fixed-design GR these slopes
are β^𝒞 + (AᵀCA)⁻¹AᵀCξ (A := X^r_𝒞), with covariance τ²(AᵀCA)⁻¹; so **if τ² > 0** and A has full centred column rank,
T_n = 𝒞 almost surely (numerics N1: 10/10 nonzero in every run); if τ² = 0, T_n = S₀^𝒞 can be sparse. In general the
justified unconditional statement is 1{T_n ≠ S₀^𝒞}π_𝒞(T_n | y) ≤ 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n); in particular
π_𝒞(T_n | y) → 0 in probability whenever P(T_n ≠ S₀^𝒞) → 1. *Proof.* π_𝒞 is a probability on Ω_𝒞. ∎ (Numerics N1, N4: π(S₀ ∩ 𝒞) → 0 while π(S₀^𝒞) → 1.)

## L1.3 Lemma DR (uniform tightness by a diagonal argument)

**Statement.** For each n let 𝒜_n be a nonempty (for n ≥ n₂) measurable set of candidate designs, and for L > 0 let
f_n^L : 𝒜_n → [0, 1] be measurable and nonincreasing in L. Suppose that for **every** sequence x_n ∈ 𝒜_n (n ≥ n₂),
lim_{L→∞} limsup_n f_n^L(x_n) = 0. Then lim_{L→∞} limsup_n sup_{x∈𝒜_n} f_n^L(x) = 0.

*Proof.* Put g(L) := limsup_n sup_{𝒜_n} f_n^L, nonincreasing in L, so lim_L g(L) =: η exists. Suppose η > 0. For every
integer L ≥ 1, g(L) ≥ η > η/2, so sup_{𝒜_n} f_n^L > η/2 for infinitely many n. Choose recursively n_1 < n_2 < … with
n_L ≥ n₂ and points x_{n_L} ∈ 𝒜_{n_L} with f_{n_L}^L(x_{n_L}) > η/2. For n ∉ {n_L} (n ≥ n₂) pick any x_n ∈ 𝒜_n. For
fixed L₀ and every L ≥ L₀, monotonicity gives f_{n_L}^{L₀}(x_{n_L}) ≥ f_{n_L}^{L}(x_{n_L}) > η/2, so
limsup_n f_n^{L₀}(x_n) ≥ η/2 for every L₀, contradicting the hypothesis on the sequence (x_n). ∎

(This extends GEN L5.3, `Theory_work/Wave1/W1-GEN/lemmas/L5_assembly.md:57-64`, from "→ 0" to tightness.)

## L1.4 Theorem MIS (ii) (random candidate design)

**Hypotheses.** X^r_𝒞 random; conditionally on X^r_𝒞 = x, ω = a(x)1 + x γ(x) + ξ with ξ ~ N_n(0, τ²I), and
(ε, ξ) independent given X^r_𝒞 with ε ~ N_n(0, σ²I) independent of X^r_𝒞 (so ε′ = ε + ξ is N_n(0, σ_𝒞²I) and
independent of X^r_𝒞); a, γ measurable; uniforms independent of everything. Fixed constants (A, s, M, φ₀, g₀, σ_𝒞²)
and either a fixed c > c₀(s, A) or a deterministic M_n → ∞; measurable sets 𝒜_n of designs with P(X^r_𝒞 ∈ 𝒜_n) → 1
such that, for every n beyond a deterministic starting index n₁, every x ∈ 𝒜_n satisfies **at that n** the finite-n
inequalities: s₀^𝒞(x) = s; p_𝒞 ≤ n^A; ‖μ^𝒞(x)‖² ≤ Mn; λ_min(R̂_{S₀^𝒞(x)}) ≥ φ₀²; the SE_λ(j₀) and SE_w(m♯_n; g₀)
inequalities anchored at S₀^𝒞(x); and BM(c): θ^𝒞_min(x)² ≥ cσ_𝒞² log n/(nφ₀²) (resp. the envelope
θ^𝒞_min(x)²nφ₀²/(σ_𝒞² log n) ≥ M_n). (An individual design cannot "satisfy BM-∞"; the deterministic envelope M_n is
what makes every selection x_n ∈ 𝒜_n a BM-∞ array. Proof thresholds n₀ of T03♯ are not design hypotheses: they depend
only on the fixed constants and on (M_n) (T03R `PROOF.md:170`). s ≤ K holds for n ≥ 2s since p_𝒞 ≥ s.)
**(ii′) without beta-min.** The same with the beta-min requirement dropped (all other finite-n inequalities kept):
then π_𝒞(S ⊉ J_n^𝒞(c)(X) | y) = O_P(r_n) under the joint law, for fixed c > c₀(s, A).

**Conclusion.** Under the joint law: 1 − π_𝒞(S₀^𝒞 | y) = O_P(r_n); P(MPM_𝒞 ≠ S₀^𝒞) → 0; P(S†_𝒞 ≠ S₀^𝒞) → 0
and E[1 − π_𝒞(S₀^𝒞 | y)] → 0; the inclusion statement for J_n^𝒞(c).

*Proof.* Let Y_n := 1 − π_𝒞(S₀^𝒞(X^r_𝒞) | X^r_𝒞, y) ∈ [0, 1]. Define f_n^L(x) := ∫ 1{Y_n(x, y(x, e′)) > L r_n}
N(0, σ_𝒞²I_n)(de′), where y(x, e′) := (α + a(x))1 + xβ^𝒞(x) + e′ (the value of α + a(x) does not affect Y_n,
L1.0). Since ε′ is independent of X^r_𝒞 with law N(0, σ_𝒞²I), f_n^L is a measurable version of
P(Y_n > L r_n | X^r_𝒞 = ·), and f_n^L(x) is the fixed-design probability at design x (Lemma R). It is nonincreasing in L.
For any sequence x_n ∈ 𝒜_n the deterministic array (x_n) satisfies the T03♯ hypotheses with fixed constants and truth
S₀^𝒞(x_n) of fixed size s (BM-∞ holds because M_n → ∞); T03♯ gives Y_n = O_P(r_n) along it, i.e.
lim_L limsup_n f_n^L(x_n) = 0. Lemma DR gives lim_L limsup_n sup_{𝒜_n} f_n^L = 0, and
P(Y_n > L r_n) ≤ sup_{𝒜_n} f_n^L + P(X^r_𝒞 ∉ 𝒜_n). Hence lim_L limsup_n P(Y_n > L r_n) = 0, which is O_P(r_n)
in the convention of [P3] §1 (finitely many n are tight automatically since Y_n/r_n ≤ 1/r_n). For MPM and S†:
{MPM_𝒞 ≠ S₀^𝒞} ∪ {S†_𝒞 ≠ S₀^𝒞} ⊆ {Y_n ≥ ½} (T03R `PROOF.md:168` (ii)–(iii), deterministic parts), and
P(Y_n ≥ ½) → 0 since Y_n → 0 in probability; E Y_n ≤ η + P(Y_n > η) for every η ∈ (0, 1), so E Y_n → 0.
(ii′): the same argument with Y′_n := π_𝒞(S ⊉ J_n^𝒞(c)(X) | y) and T03R (iv) (`PROOF.md:168`), which needs no beta-min.
On 𝒜_nᶜ nothing is assumed (posterior mass of an infeasible support is 0 by convention, [P3] (ii)). ∎

**Note on measurability.** As in GEN L5.4, 𝒜_n, a, γ, β^𝒞 and S₀^𝒞 must be measurable functions of the candidate
design; nothing may depend on (ε, ξ).
