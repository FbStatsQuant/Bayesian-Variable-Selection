# L4 — Assembly: the main theorem (claim (C4))

Status: **PROVED (by this seat, unchecked)**; lemma check R04 (Codex Sol high, reviews/R04_L4L5_check_sol.md): VERIFIED-WITH-AMENDMENTS (1),
applied (reviews/R04_disposition.md);
given the cited inputs with their recorded statuses.

Inputs (statuses verbatim):
* [M5-0] T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" (SoP `04_theory.tex:489`):
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n at every n, any X, under the named premises.
* [S-T] T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (SoP TH09): under (H0), 1 − π(S₀) = O_P(√(log n/n)).
* [OP] operational closure 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 from S̃₀ does not score S₀}: GEN/lemmas/L5_assembly.md (status
  there "PROVED (by this seat, unchecked)" from the named premises, inside Theorem GEN "PROVED-CHECKED"). Its argument
  uses only GUARD-W, OP-LS0, e4 and the fact that LS0 is deterministic given the data; it does not depend on the cap
  value, so it holds verbatim for LS0 with the cap of MR1.
* L1 (descent), L2 (NA, TL), L3 (sandwich) of this folder.

**Theorem L4.1 (Theorem GROW).** Assume G, (H0), (G1)–(G3) and (G4-χ) or (G4-dir), the implementation premises of
STATEMENT §1, and MR1 (LS0 cap ℓ^{LS0} = ℓ_n + |S̃₀|). Then

  D_n ≤ P(Sand_nᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0,  Sand_n := {S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀},

hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U_n). (b) Under (G4-χ) the same holds
with the production cap ℓ_n = ⌈log₂(n + p + 1)⌉ in place of MR1. No delivery claim.

*Proof.* By [OP], D_n ≤ P(LS0 from the emitted centre does not score S₀). Under premise e4 the emitted centre is a
maximiser of γ₀ (the prescribed one); on Sand_n it lies in 𝓛 (G1 gives |Q| ≤ K, so 𝓛 ⊆ Ω). On
Sand_n ∩ NA(𝓛) ∩ TL(𝓛), L1.2(ii) with C := S̃₀ shows that LS0 scores S₀ as soon as its cap is ≥ |S̃₀ ∖ S₀| − 1;
MR1 gives ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀|. This proves the display. P(Sand_nᶜ) → 0 by L3; P(TL(𝓛)ᶜ) → 0 by L2.1;
P(NA(𝓛)ᶜ) → 0 by L2.2–L2.3. By [S-T], δ₁ := 1 − π(S₀) → 0 in probability and δ₁ ∈ [0, 1], so E₀δ₁ → 0; [M5-0] gives
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) = 1 − P(U_n) − o(1).
(b) Under (G4-χ), on Sand_n: |S̃₀ ∖ S₀| ≤ |𝒫_n| ≤ (1 − δ₀) ln n < log₂ n ≤ ℓ_n, so the production cap is ≥ the
number of moves and the same argument applies. ∎

**Notes.** (1) The exact-enumeration branch only helps (S₀ is scored there once s₀ ≤ K), as in GEN L5.
(2) For R′ > 4 the extra search from c₄ only adds scored models (premise listed). (3) Nothing is conditioned on 𝒪.
(4) **Cost of MR1.** On Sand_n ∩ NA(𝓛) ∩ TL(𝓛) LS0 makes |S̃₀ ∖ S₀| ≤ |𝒫_n| moves (+1 scan); in the worst case (any data)
ℓ^{LS0} ≤ ℓ_n + K moves, each scan scoring ≤ p + k*(p − k*) models (SoP `02_method.tex:413`) — polynomial.
(5) On Sand_n ∩ NA(𝓛) ∩ TL(𝓛) the move count is exactly |S̃₀ ∖ S₀|; GEN used the sufficient upper bound
2^{v̄} − 1 (v̄ the bounded size of its containing set) — R08 item 13.
