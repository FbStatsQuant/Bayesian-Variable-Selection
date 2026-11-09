# X6 — Assembly: Theorem FAC-CS-iid, claims (C2) consequences, (C3), (C4)

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses; lemma check R05 (Codex
Sol high, reviews/R05_X5X6_check_sol.md): VERIFIED-WITH-AMENDMENTS, applied (reviews/R05_disposition.md).

**Conditioning (R05 item 1).** Throughout, Z := X^r (the raw design). Z determines X, D_x, θ* = D_xβ, the partition
and N₀; given Z = z, e = Cε ~ N(0, σ²C) and the data are a fixed-design instance (X(z), θ*(z)) of model G. Fixed-design
results are applied conditionally on Z and integrated over Z.

Inputs (statuses verbatim):
* [M5-0] T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" (SoP `04_theory.tex:492`):
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) — a fixed-design statement, applied conditionally on Z.
* [S-T] T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (FINAL `s3_posterior.tex`, Theorem S-T), with the
  random-design pattern of FINAL `s3_posterior.tex:20` ("Random designs": T03♯ along every deterministic sequence in the
  X-events with common constants; conditional convergence alone would not suffice) as executed in FACA L5.1.
* [OP] operational closure 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 from S̃₀ does not score S₀}: "PROVED (by this seat, unchecked)" inside
  Theorem GEN "PROVED-CHECKED"; it uses only GUARD-W, OP-LS0, e4 and determinism of LS0 given the data (FACB L5 inputs).
* Lemma CAP (FINAL `s7_impl.tex`), part (a) (prefix property), "PROVED (by this seat)", council-checked.
* Proposition F with A1's corrected statement and its GROW extension A2 (FINAL `s6_delivery.tex`; A2 "PROVED (A2), checked
  by A3"), A2 step 3 (`Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md:55-67`); FACB L5.4 (the CS extension).
* X1–X5 of this folder.

## X6.1 (H0) on a design event with common constants

On 𝒜_n (X5.1), for n ≥ n₀: every principal submatrix of R̂ has λ_min ≥ c₀ =: φ₀² (anchored eigenvalue conditions and
SE_λ(j₀) for every j₀); λ_min(X_AᵀX_A) ≥ c₀(n − 1) ≥ g₀ := c₀ for every nonempty A (SE_w with fixed g₀); energy
‖μ‖² = (n − 1)θ*ᵀR̂θ* ≤ (n − 1)s₀‖θ*‖² ≤ Mn with M := 2s₀‖ϑ‖² (entries of R̂ bounded by 1; ‖θ*‖ ≤ (1 + δ′_n)‖ϑ‖);
BM-∞: θ*²_min nφ₀²/(σ² log n) ≥ (|ϑ|_min/2)²c₀n/(σ² log n) → ∞; p ≤ n^{1/2} (A = ½); s₀ ≤ K = p eventually. These
constants and envelopes do not depend on z ∈ 𝒜_n (a raw-design event, X5.1). Hence (FACA L5.1's every-sequence
argument): if sup_{z∈𝒜_n}E[1 − π(S₀) | Z = z] did not tend to 0, a deterministic raw-design sequence z_n ∈ 𝒜_n with
E[1 − π(S₀) | z_n] ≥ η > 0 along a subsequence (extended arbitrarily in 𝒜_n at the other indices) would induce
deterministic pairs (X(z_n), θ*(z_n)) satisfying T03♯'s hypotheses with common constants (T03♯ allows a deterministic
coefficient sequence), contradicting 1 − π(S₀) = O_P(√(log n/n)) (bounded by 1, so the expectation would tend to 0). So
E[1 − π(S₀)] ≤ P(𝒜_nᶜ) + sup_{z∈𝒜_n}E[1 − π(S₀) | Z = z] → 0 under the joint law.

## X6.2 LS0 scores S₀ (event 𝒦_n)

𝒦_n := {deterministic LS0 from the emitted centre, cap a_n = ℓ_n + |S̃₀|, scores S₀}. On 𝒢_n := 𝔊_n (X4.0) ∩ {start
event of X5} ∩ {ξ_l ≠ x_T ∀ l, T} (probability one), n ≥ n₀: S̃₀ = S* = [p] ∖ N₀ (X5); Lemma X4 with 𝔫 := N₀ (it holds
for every |𝔫| ≤ 15 simultaneously, so the data-dependence of N₀ is irrelevant) gives an uncapped path of exactly
m₀ = |S* ∖ S₀| ≤ |S̃₀| ≤ a_n null deletions ending certified at S₀; Lemma CAP(a) (prefix property) shows the capped search
follows it and terminates certified at S₀, which it scans. So 𝒢_n ⊆ 𝒦_n and P(𝒦_nᶜ) ≤ P(𝔊_nᶜ) + P(start failure) → 0
(Lemmas X4.0, X5). **Legacy cap:** on 𝒢_n, if m₀ ≥ ℓ_n + 2, every model scored by LS0 with cap ℓ_n has ≥ |S*| − ℓ_n − 1
> s₀ elements, so S₀ is not scored (FACB L5.2's argument verbatim; a statement about the LS0 route only).

## X6.3 Theorem FAC-CS-iid, (C3)

**Theorem.** Under model R, (CS-R), (P-½), (θ), (FS), the implementation premises of FACB STATEMENT §1 (with CAL) and
MR1: (H0) holds on 𝒜_n with common constants (P(𝒜_n) → 1); D_n ≤ P(𝒦_nᶜ) → 0; P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; and
liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U_n), all under the joint law of (X^r, ε) and the algorithm's randomness.
*Proof.* For every raw design z, [OP] gives D_n(z) ≤ P(𝒦_nᶜ | Z = z), D_n(z) := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} | Z = z) (potential-run
event; the inclusion is pathwise given the data; exact-enumeration branches only add scored models), and [M5-0] gives
P(𝒪 ∩ {Ŝ⁺ ≠ S₀} | z) ≤ 2E[1 − π(S₀) | z] + D_n(z). Integrate over Z (E_Z D_n(Z) = D_n): D_n ≤ P(𝒦_nᶜ) → 0 (X6.2) and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀)] + D_n → 0 (X6.1). Finally
P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}). ∎

## X6.4 Delivery, (C4)

Proposition F's classes (and their extensions GROW (A2), FAC-CS (FACB L5.4), FAC-L incl. iid rows (FACA (D))) are
extended to model R with (CS-R), (P-½), (θ), (FS), with exactly Proposition F's method, total tier-1 fallback, premises
and allocation (FINAL `s6_delivery.tex`, A1's corrected statement, cap a_n = ℓ_n + |S̃₀|, envelopes W_G, M_G and the
current-head LS0 preflight terms), CAL not assumed.
(1) **Lemma S inputs.** With probability one the raw columns of X^r are nonconstant (iid Gaussian rows, n ≥ 3) and the
centred response is nonconstant, so no column is dropped, p_raw = p, and Q_S ≥ yᵀy/(n + 1) > 0 for every S (A2 step 1,
`A2_propF_GROW.md:37-47`, applies verbatim to each realised design). (2) **No output has probability 0.** Proposition F's
conclusion "for every admissible n ≥ 3, P(no output) = 0" holds conditionally on every such raw design z (A2 step 2), hence
under the joint law. (3) **Consistency.** D′'s pathwise inclusion (FINAL s6, Corollary D′, with cap a_n as in A2 step 3)
gives, data set by data set, 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ; with P(𝒪) = 1, Markov and X6.1–X6.2:
P(Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ) → 0. CAL, restricted-ESS success and fallback-probability bounds are not used. All
reused results keep their recorded qualifications ([OP] unchecked-by-seat; e4/N3; S.3 audited by code reading); the
extension does not inherit council approval from the reused inputs. ∎
