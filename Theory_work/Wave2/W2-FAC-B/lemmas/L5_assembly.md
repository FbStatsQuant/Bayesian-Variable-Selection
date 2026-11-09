# L5 — Assembly: Theorem FAC-CS (claims (C2) consequences, (C3), (C4))

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses; lemma check R05 (Codex
Sol high, reviews/R05_L5_check_sol.md): VERIFIED-WITH-AMENDMENTS (4 minor), applied.

Inputs (statuses verbatim):
* [M5-0] T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" (SoP `04_theory.tex:492`, card TH05.0; R05 item 4):
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) (potential-run notation, SoP `04_theory.tex:84`).
* [S-T] T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (FINAL `s3_posterior.tex`, Theorem S-T).
* [OP] operational closure 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 from S̃₀ does not score S₀}: "PROVED (by this seat, unchecked)" inside
  Theorem GEN "PROVED-CHECKED" (`Theory_work/Wave1/W1-GEN/STATEMENT.md:169`); its argument uses only GUARD-W, OP-LS0,
  e4 and that LS0 is deterministic given the data, not the cap value (`Theory_work/Wave1C/C-GROW/lemmas/L4_assembly.md:12-14`).
* Lemma CAP (FINAL `s7_impl.tex`, §"Integration lemma"), part (a) (prefix property), "PROVED (by this seat)", council-checked.
* Proposition F with A1's corrected statement and its GROW extension A2 (FINAL `s6_delivery.tex`; A2 "PROVED (A2), checked
  by A3"), in particular A2 step 3 (`Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md:55-67`).
* L1–L4 of this folder.

## L5.1 (H0) holds on the class

Under (CS), (P), (θ), with Σ̄ := (1 − ρ)I + ρ11ᵀ: ‖μ‖² = (n − 1)θ*ᵀΣ_nθ* = (n − 1)ϑᵀΣ̄_{S₀S₀}ϑ ≤ Mn for any fixed
M > ϑᵀΣ̄_{S₀S₀}ϑ (sign-corrected coordinates, L1.0; Σ̄_{S₀S₀} does not depend on n or positions; R02 item 2);
every principal submatrix of R̂ = Σ has λ_min = 1 − ρ (or 1 for singletons), so λ_min(R̂_{S₀}) ≥ φ₀² := 1 − ρ, SE_λ(j₀)
holds with j₀ = ⌈(2A + 1)s₀⌉ + 1 = 3s₀ + 1 (and for every j₀); SE_w(m♯_n; g₀) holds with the fixed g₀ := 1 − ρ, because
λ_min(X_AᵀX_A) ≥ (n − 1)(1 − ρ) ≥ g₀ for every nonempty A ⊆ [p], in particular for every anchored S₀ ∪ J with
|J| ≤ m♯_n (R_K = 0 gives s₀ ≤ m♯_n ≤ K eventually; no bound on m♯_n is needed) [R05 item 1]; p ≤ n/2 ≤ n¹ (A = 1); s₀ ≤ K = p eventually; BM-∞: θ*²_min nφ₀²/(σ² log n) = |ϑ|²_min n(1 − ρ)/(σ² log n) → ∞.
Hence [S-T]: 1 − π(S₀) = O_P(√(log n/n)), and E₀[1 − π(S₀)] → 0 (bounded by 1).

## L5.2 LS0 scores S₀ (the event 𝒦_n)

Let 𝒦_n := {deterministic LS0 from the emitted centre, with the method's cap a_n = ℓ_n + |S̃₀| (MR1), scores S₀}.
For n beyond the onsets n₀ of L2 and L4, on G_n := E_n ∩ E_n^S ∩ 𝒩𝒟_n (L3, L2, and L4's probability-one
nondegeneracy event; R05 item 2): the emitted centre is S̃₀ = S* (L2; unique maximiser, so e4/e4′ and TDP return it);
the uncapped path from S* makes m₀ = |S* ∖ S₀| moves, all null deletions, and ends certified at S₀ (L4). Since
a_n = ℓ_n + |S*| ≥ m₀, Lemma CAP(a) shows the capped search follows the same path, makes m₀ moves and terminates
certified at S₀ (S₀ is scanned, hence scored). So G_n ⊆ 𝒦_n and P(𝒦_nᶜ) ≤ P(E_nᶜ) + P((E_n^S)ᶜ) → 0 (P(𝒩𝒟_n) = 1). 𝒦_n is data-measurable, so its probability under
the original law equals that on L1's enlarged probability space.

**Necessity of a large cap (on the LS0 route).** On G_n, if m₀ ≥ ℓ_n + 2, LS0 with the legacy cap ℓ_n scans only
C_0, …, C_{min(ℓ_n, m₀)} = C_0, …, C_{ℓ_n} (CAP(a)), and every model it scores has ≥ |S*| − ℓ_n − 1 > s₀ elements, so S₀ is not scored by
LS0(ℓ_n). (This is a statement about the LS0 route, not about the full method.)

## L5.3 Theorem FAC-CS ((C3))

**Theorem.** Under G, (CS), (P), (θ), (FS), the implementation premises of STATEMENT §1 and MR1:
D_n ≤ P(𝒦_nᶜ) → 0; P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U_n).

*Proof.* [OP] gives D_n ≤ P(𝒦_nᶜ) (exact-enumeration branches only add scored models, as in GROW L4 note 1). L5.2 gives
P(𝒦_nᶜ) → 0. [M5-0] with L5.1: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n → 0; and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). ∎

## L5.4 Delivery ((C4))

Proposition F's classes (LH, LH-iid, GEN; GROW via A2) are hereby extended to fixed exact-Gram CS designs under model
G and the hypotheses of STATEMENT §2, exactly as A2 extends them to GROW (R09 suggestion 5).

Take exactly the method, total tier-1 fallback, premises and allocation of Proposition F (FINAL `s6_delivery.tex`,
A1's corrected statement, cap a_n = ℓ_n + |S̃₀|, envelopes W_G, M_G and the current-head preflight additions).
(1) **Lemma S inputs.** A fixed CS design is a fixed standardised design with nonconstant raw columns (model G), so no
column is dropped and p_raw = p; the centred response is nonconstant with probability one (ε Gaussian); Q_S ≥ yᵀy/(n + 1)
> 0 for every S, so the scorer never fails (A2 step 1, `A2_propF_GROW.md:37-47`, applies verbatim: it uses no
relevance-set property). (2) **No output has probability 0.** Proposition F's conclusion "for every admissible n ≥ 3,
P(no output) = 0" uses only the method/allocation/premises and Lemma S inputs, not the statistical class (A2 step 2).
(3) **Consistency.** With 𝒦_n as in L5.2, D′'s pathwise inclusion (FINAL s6, Corollary D′; reused with cap a_n in A2
step 3) gives 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ; with P(𝒪) = 1, Markov and L5.1–L5.2:
P(Ŝ⁺ ≠ S₀) ≤ 2E₀[1 − π(S₀)] + P(𝒦_nᶜ) → 0. CAL, restricted-ESS success and any bound on the fallback probability are not
used. All reused results keep their recorded qualifications (A3 finding 4: [OP] unchecked-by-seat; e4/N3; S.3 audited by
code reading). Implementation fact: the fallback, the MR1 cap and the LS0 preflight charge are on main through merge
4676af6 (merge of w1c/ls0-merge; FINAL s6/s7 and the C-ENG report describe the earlier unmerged state). The FAC-CS
extension does not inherit council approval from the reused inputs (R05 item 4). ∎
