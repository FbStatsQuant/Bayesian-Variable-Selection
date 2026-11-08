# L5 — Assembly: claims (C3), (C3-fav), (C4)

Status: **PROVED (by this seat, unchecked)**, given the cited inputs with their recorded statuses; lemma check R06
(Codex Sol): VERIFIED-WITH-AMENDMENTS, amendments applied (v2, reviews/R06_disposition.md).

Inputs and statuses (verbatim):
* [M5-0] T38-(0): "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" (SoP `04_theory.tex:489`):
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n at every n, any X, under the named premises, with
  D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) in potential-run notation.
* [S-T] T03♯: "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (TH09): under (H0), 1 − π(S₀) = O_P(√(log n/n)).
* [OP] Operational closure: 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 from S̃₀ does not score S₀}. Status: PROVED (by this seat,
  unchecked) from the named premises; corroborated by [W6] (candidate). Direct pathwise argument: on a potential output run, GUARD-W excludes an interrupted LS0; OP-LS0 gives execution of LS0 with
  the prescribed emitted centre (e4) and completed scans; every model LS0 scores joins the all-scored set
  (SoP `02_method.tex:494`); LS0 reads no uniforms, so the models it scores are a deterministic function of the data.
  Hence if that prescribed search scores S₀, no potential output omits S₀ from 𝒮̄⁺. (If the run takes the exact
  branch, S₀ is scored anyway once s₀ ≤ K.) Corroborated by BS/API-PXNGAP/PROOF.md:443-446 (candidate).
* L2 (C1), L3 + L4 (C2) of this folder.

## (C3)

**Theorem L5.1.** Under (H0), (H1), (H2) and the premises of STATEMENT §1, for every n ≥ n₀ (the L3 onset, which
includes ⌊n/2⌋ ≥ v̄ + 1, so every member of L3's family is feasible) with ℓ_n ≥ 2^{v̄} − 1:

  D_n ≤ P(S̃₀ ≠ S*) + P(Ω_nᶜ) + 1{n < n₀},

with Ω_n, n₀ from L3. (Scoring needs only ℓ_n ≥ τ − 1, i.e. ℓ_n ≥ 2^{v̄} − 2 suffices.) Rate: P(Ω_nᶜ) ≤
2e^{−n^{1/3}} + O(n^{−2}) + O(n^{−1}) + 2v̄2^{v̄}e^{−(log log n)²/2} + 2/log n = O(1/log n) (L1.1, L3.0), so
D_n ≤ P(S̃₀ ≠ S*) + O(1/log n) for n ≥ n₀. Consequently D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and
P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1), so liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U_n).

*Proof.* By [OP], D_n ≤ P(LS0 from S̃₀ does not score S₀). On {S̃₀ = S*} ∩ Ω_n with n ≥ n₀: S* ⊆ 𝒱, Corollary L3.4
holds, and L4.1(iii) with τ(S*) ≤ 2^{v̄} − 1 ≤ ℓ_n + 1 gives that LS0 scores S₀. This proves the display.
P(S̃₀ ≠ S*) → 0 by L2; P(Ω_nᶜ) → 0 by L3; ℓ_n = ⌈log₂(n + p + 1)⌉ → ∞, so the cap condition holds eventually.
(Feasibility: L3's family has sets of size ≤ min(p, |𝒱_n| + 1); if 𝒱_n = [p] there is no outside variable and all
sets have size ≤ p = K once ⌊n/2⌋ ≥ p; otherwise p ≥ |𝒱_n| + 1 and ⌊n/2⌋ ≥ v̄ + 1 suffices. Indices at which the
production run happens to take the exact-enumeration branch only help: S₀ is scored there once s₀ ≤ K, SoP
`02_method.tex:167-170`; this is not needed.) By [S-T], δ₁ := 1 − π(S₀) → 0 in probability and
δ₁ ∈ [0, 1], so for every ε > 0, E₀δ₁ ≤ ε + P(δ₁ > ε) → ε; hence E₀δ₁ → 0. [M5-0] gives P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0. Finally
P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) = 1 − P(U_n) − o(1). ∎

*Notes.* (0) Premise e4 is used only on {π₀(S*) > ½}, where the start-mode maximiser is unique (L2 step 9). For the
coded `start_mode` with a unique maximiser (N = 1 ≤ cap) the sibling ticket W1-N3 proves the coded DP returns the
prescribed maximiser (its clause (c); status as recorded in Theory_work/Wave1/W1-N3/REPORT.md: "PROVED-CHECKED",
Wave-1 sibling result, not adopted by HQ). The remaining content of e4 here is the integration of LS0 itself (LS0 is
not in production code); e4/N3 stays a named premise. (1) For R′ > 4 the scored set contains the extra search from c₄ (nested), so the inclusion of [OP] is
unchanged (premise listed). (2) The exact branch: whenever the production run enumerates, S₀ ∈ 𝒮̄⁺ once s₀ ≤ K, so
those n contribute nothing to D_n. (3) Nothing is conditioned on 𝒪; bounds are intersections with 𝒪.

## (C3-fav)

**Corollary L5.2.** If S* = S₀, under (H0), (H2) and the premises (no (H1)): D_n ≤ P(S̃₀ ≠ S₀) → 0, and the
conclusions of L5.1 hold. *Proof.* On {S̃₀ = S₀} the emitted LS0 centre is S₀, which is scored (OP-LS0). L2 gives
P(S̃₀ ≠ S₀) → 0; then [S-T] and [M5-0] as above. ∎

## (C4) Random designs

**Lemma L5.3 (de-randomisation).** Let X_n be a random element of a standard Borel space and let f_n be **any fixed
measurable function** with values in [0, 1] such that P(E_n) = E f_n(X_n) (a measurable version of the conditional
probability of an event E_n given X_n). Let 𝒜_n be
measurable sets with P(X_n ∈ 𝒜_n) → 1 and 𝒜_n ≠ ∅ for n ≥ n₂. If f_n(x_n) → 0 for **every** deterministic sequence
with x_n ∈ 𝒜_n (n ≥ n₂), then sup_{x∈𝒜_n} f_n(x) → 0 and P(E_n) → 0.
*Proof.* If sup_{𝒜_n} f_n ↛ 0, there are η > 0 and n_k ↑ ∞ with sup_{𝒜_{n_k}} f_{n_k} > η, hence x_{n_k} ∈ 𝒜_{n_k}
with f_{n_k}(x_{n_k}) > η. Complete to a sequence by choosing any x_n ∈ 𝒜_n for n ∉ {n_k}. Then f_n(x_n) ↛ 0,
contradicting the hypothesis. Finally P(E_n) ≤ sup_{𝒜_n} f_n + P(X_n ∉ 𝒜_n). ∎

**Theorem L5.4.** Under the hypotheses of (C4) (STATEMENT §3), under the joint law of (X, ε, uniforms):
D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and the liminf statement holds.
*Proof.* **Canonical version.** The method's run is a measurable function of (raw design x, noise e, uniforms u) and
of the X-measurable objects β(x), 𝒱_n(x), S*_n(x), the actual partition and the deterministic tie rules (all chosen
as measurable versions on the admissible set of designs with nonconstant columns). Let H_n(x, e, u) be the indicator
of the event of interest — E_n := 𝒪 ∩ {Ŝ⁺ ≠ S₀}, or the potential-run event E′_n := 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} — and define
f_n(x) := ∫∫ H_n(x, e, u) N(0, σ²I_n)(de) P_U(du) at **every** x. Since ε and the uniforms are independent of X
(the method's randomisation does not depend on X; G), f_n is a measurable version of P(E_n | X_n = x) and f_n(x) is
exactly the fixed-design probability at design x. For a deterministic sequence x_n ∈ 𝒜_n the model given X_n = x_n
is the fixed-design model G with design x_n and coefficients β(x_n), satisfying (H0)–(H2) (resp. (H0), (H2) with
S* = S₀) by assumption; L5.1 (resp. L5.2) gives f_n(x_n) → 0 for both events. Lemma L5.3 gives P(E_n) → 0 and
D_n = P(E′_n) → 0. The liminf statement follows from P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − P(E_n). ∎

*Remark.* Common constants across sequences are stronger than needed: L5.1/L5.2 must apply to each sequence (SEP
onsets may depend on the sequence); the
diagonal argument of L5.3 then needs no explicit uniform rate. The partition is the actual X-measurable one; 𝒱 and S*
may be X-measurable; nothing may depend on ε.
