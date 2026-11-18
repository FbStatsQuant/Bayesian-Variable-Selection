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
fails, A2 steps 1–2 verbatim; no relevance-set property is used), with 𝒦_n as in L5.2: (a) for every admissible n ≥ 3 with (n, p_raw) ∈ 𝔇 := {ℓ_raw ≤ 10⁶ and ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1}, ℓ_raw := ⌈log₂(n + p_raw + 1)⌉, P(no output) = 0; (b) with A:IDEAL-W⁺ in place of IDEAL-W (IDEAL-W, and the two shipped rejection predicates `le > 10⁶` (Scripts/SMC_BVS/core/v3_run.R:96) and `ℓ + |S̃₀| > INT_MAX` (Scripts/SMC_BVS/core/cpp/v3_core.cpp:474) are false, in the imported premises below; definition at the end of this file): for every admissible n ≥ 3,
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

**IDEAL-W⁺ narrowing note (2026-11-16; HQ D78 correctness event; outside every registered statement span).** Claim (C4-R) (`:39-43`; registered also at `STATEMENT.md:123-124`) now states delivery in two clauses, in the form of W2-UNI's Proposition F-UNI v2 (`Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md`): (a) under IDEAL-W, P(no output) = 0 only on the bounded domain 𝔇; (b) for every admissible n, and the bound on P(Ŝ⁺ ≠ S₀), under A:IDEAL-W⁺. Reason (Sol review TR1, `Theory_work/Dept/research/FUNI_transfer/TR1_sol.md` §1–§2): two shipped LS0 cap validators lie outside Theorem D's exit walk and can end an SMC-branch fit without output, independently of resources: `le > 1e6` (`Scripts/SMC_BVS/core/v3_run.R:96-97`; le = ℓ_n in the stated configuration) and `cap_ll > numeric_limits<int>::max()` with cap_ll = ℓ_n + |S̃₀| (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`). IDEAL-W (C-DLV `STATEMENT.md:24-25`, unchanged) excludes overflow, not these application-level rejection predicates. On 𝔇 neither predicate fires: ℓ_n ≤ ℓ_raw ≤ 10⁶ (p ≤ p_raw) and ℓ_n + |S̃₀| ≤ ℓ_raw + K_n ≤ ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1; the exact-enumeration branch reaches neither check. 𝔇 is sufficient, not necessary, and bounded, so clause (a) carries no asymptotic conclusion. Under A:IDEAL-W⁺ both predicates are false. In both clauses the no-output step of the proof (Theorem D's exit walk with the total tier-1 fallback and the stated allocation, which already contains A4's LS0 preflight terms P_e + A and P̄_LS0 (FIN `s6_delivery.tex:37-44`)) is otherwise unchanged (TR1 §1 table). Definition (verbatim; registered assumption A:IDEAL-W⁺):

**A:IDEAL-W⁺ (IDEAL-W with the two LS0 cap ceilings lifted).** IDEAL-W, exactly as defined in C-DLV `STATEMENT.md:24-25`, and the two shipped rejection predicates `le > 10⁶` (`Scripts/SMC_BVS/core/v3_run.R:96`, the LS0 base-cap validator; le = ℓ_n = ⌈log₂(n + p + 1)⌉ in the shipped configuration) and `ℓ + |S̃₀| > INT_MAX` (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`, the disjunct `cap_ll > numeric_limits<int>::max()` of the LS0 cap-range guard, `int` read as unbounded) are false. Nothing else is lifted: the other conditions of those two validators (numeric type, length, finiteness, integrality, `le < 0`, `o.ls0_ell < 0`), every other validator, the 10⁶-maximiser start-mode enumeration cap with its tie-aware DP fallback, and every fallback and method cap are kept as coded. Like IDEAL-W and EX-A, A:IDEAL-W⁺ is an idealisation of the machine and code; a larger allocation does not imply it.
