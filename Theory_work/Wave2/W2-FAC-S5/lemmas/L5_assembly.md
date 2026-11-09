# L5 — Assembly: Theorem FAC-BCS-R ((C3-R), (C4-R)) and the Tier-2 corollary

Status: **PROVED-CHECKED** (Tier 1: lemma checks, mid-point CONTINUE, sweep fixed, council round 2 passed — R09 Sol 8.8, R10 Opus 8.8, all gates PASS), given the cited inputs with their recorded statuses; lemma check R04 (Codex Sol
high, reviews/R04_L5_check_sol.md): VERIFIED-WITH-AMENDMENTS (measurability wording, provenance), applied. It follows FACB
`lemmas/L5_assembly.md` (Theorem FAC-CS "PROVED-CHECKED", FACB REPORT §1) step by step; only the class-specific inputs
change (L1–L4 of this folder replace FACB's L1–L4).

Inputs (statuses verbatim, as FACB L5): [M5-0] T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"
(SoP `04_theory.tex:492`, card TH05.0): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺})
(SoP `04_theory.tex:84`); [S-T] T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (FINAL `s3_posterior.tex`);
[OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED" (`Theory_work/Wave1/W1-GEN/STATEMENT.md:169`);
Lemma CAP (FINAL `s7_impl.tex`) "PROVED (by this seat)", council-checked; Proposition F (A1 corrected statement) and
A2 step 3 (`Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md:55-67`), A2 "PROVED (A2), checked by A3".

## L5.1 (H0) holds on the class
(After L1.0's sign correction; principal eigenvalues are unchanged by Υ_n.) ‖μ‖² = (n − 1)θ*ᵀΣθ* = (n − 1)ϑᵀΣ_{S₀S₀}ϑ ≤ Mn for any fixed M > (1 + s₀)‖ϑ‖² (entries of Σ are ≤ 1). Every
principal submatrix of R̂ = Σ has λ_min ≥ d (L1.2(a)); so λ_min(R̂_{S₀}) ≥ φ₀² := d, SE_λ holds for every j₀ (in particular the required j₀ = ⌈(2A + 1)s₀⌉ + 1 = 3s₀ + 1 at A = 1), and SE_w
holds with the fixed g₀ := d (λ_min(X_AᵀX_A) ≥ (n − 1)d for every nonempty A); p ≤ n/2 (A = 1); s₀ ≤ K = p
eventually; BM-∞: ϑ²_min n d/(σ² log n) → ∞. Hence [S-T]: E₀[1 − π(S₀)] → 0. (Exactly FACB L5.1 with 1 − ρ → d.)

## L5.2 LS0 scores S₀ on E_n ∩ CC_n(δ)
𝒦_n := {deterministic LS0 from the emitted centre with cap a_n = ℓ_n + |S̃₀| scores S₀}. For n ≥ n₀, on
E_n ∩ CC_n(δ): the emitted centre is S* (L2, unique maximiser); the uncapped path from S* makes m₀ null deletions and
ends certified at S₀ (L4); a_n ≥ |S*| ≥ m₀, so by CAP(a) the capped search follows the same path and S₀ is scanned.
𝒦_n is data-measurable (finite deterministic computations with a deterministic tie rule; defined on every admissible data
set, with the exact-branch convention of CAP), so its original-law probability P₀(𝒦_nᶜ) equals its probability P̃(𝒦_nᶜ)
on L1's enlarged space. **E_n and CC_n(δ) are defined on the enlarged space and are not assumed to be data-measurable**; in general CC_n is not
(it involves the latent common factor h through e_R, Var(h | g_{[p]}) > 0; R04 item 1 gives a p = 1 example where
P₀(CC_n | data) ∈ (0, 1); R06 item 18);
probabilities of CC_n refer to that space (STATEMENT §3). Hence, by a union bound,
  P₀(𝒦_nᶜ) = P̃(𝒦_nᶜ) ≤ P̃(E_nᶜ) + P̃(CC_n(δ)ᶜ) = P̃(CC_n(δ)ᶜ) + o(1)  (L3.1).

## L5.3 (C3-R)
**Theorem FAC-BCS-R (consistency part).** Under G, (BCS), (P_α) with α < 1/2, (θ), (FS-BCS), the implementation
premises (with CAL) and MR1, for every δ ∈ (0, 1): D_n ≤ P̃(CC_n(δ)ᶜ) + o(1) and
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P̃(CC_n(δ)ᶜ) + o(1).
*Proof.* [OP]: D_n ≤ P(𝒦_nᶜ); L5.2; [M5-0] with L5.1. ∎

## L5.4 (C4-R) Delivery
Exactly FACB L5.4 steps (1)–(3) (Lemma S inputs: fixed standardised design with nonconstant raw columns, scorer never
fails, A2 steps 1–2 verbatim; no relevance-set property is used), with 𝒦_n as in L5.2: for every admissible n ≥ 3,
P(no output) = 0, and by D′'s pathwise inclusion 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ, so
P(Ŝ⁺ ≠ S₀) ≤ 2E₀[1 − π(S₀)] + P₀(𝒦_nᶜ) ≤ P̃(CC_n(δ)ᶜ) + o(1). CAL is not used. All reused results keep their recorded
qualifications (A3 finding 4): [OP] "PROVED (by this seat, unchecked)"; e4/e4′ (N3 OPEN; only uniqueness of the start
maximiser is used, L2); S.3 audited by code reading; corrected Proposition F / F-GROW council approval applies to their
d315c1e statements, the later preflight addition is A4 "OK-WITH-FIXES" (fixes applied). This is a **new class extension**
of Proposition F's delivery machinery to fixed exact-Gram BCS designs under model G; it inherits no council approval.
Imported premises (all of FACB (C4)): F's method, total tier-1 fallback, MR1 cap a_n, EX-A with its unit-cost
interpretation, IDEAL-W, EX-S, SR, e4, GUARD-W, TDP-IMPL, MACH, CONFIG, OP-LS0 with cap a_n, fixed worker count and
declared R′, valid declared seed/allocation, envelopes W_G, M_G and the current-head LS0 preflight time/archive terms
(FINAL `s6_delivery.tex:37-44`). Random-row S5 is outside this claim. ∎

## L5.5 Tier-2 corollary (conditional on Lemma KL)
If P̃(CC_n(δ)) → 1 (enlarged space) for some fixed δ > 0 along every sequence with limsup log p/log n < α₀ (α₀ ≤ (1 − δ)/2), then for
such sequences, under the hypotheses of L5.3/L5.4, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(Ŝ⁺ = S₀) → 1 (Theorem FAC-BCS).
This corollary is claimed only together with a checked proof of KL.
