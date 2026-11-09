# L4 — Assembly: Theorem FAC-L (fixed design), claim (L4)

Status: **PROVED (by this seat, unchecked)** — v1, 2026-11-09; lemma check R03 (Sol high): VERIFIED; given the cited inputs with their recorded statuses.

Inputs (statuses verbatim):
* [M5-0] T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" (FINAL s1, `SoP/04_theory.tex:477-489`):
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n at every n, any X, under the named premises.
* [S-T] T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (FINAL s3): under (H0), 1 − π(S₀) = O_P(√(log n/n)).
* [OP] operational closure 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 from the emitted centre does not score S₀}
  (`Theory_work/Wave1/W1-GEN/lemmas/L5_assembly.md`, "PROVED (by this seat, unchecked)", inside Theorem GEN
  "PROVED-CHECKED"); its argument uses only GUARD-W, OP-LS0, the emitted-centre premise and determinism of LS0 given the
  data, not the cap value (GROW L4 "Inputs"), so it holds for the merged cap ℓ_n + |S̃₀|.
* [GROW-L1] C-GROW `lemmas/L1_descent.md` Lemma L1.2 ("PROVED (by this seat, unchecked)"; lemma check R03 (Codex Sol high): VERIFIED; inside
  C-GROW "PROVED-CHECKED"): for any S₀ ⊆ Q ⊆ [p] with |Q| ≤ K and 𝓛_Q := [S₀, Q], on NA(𝓛_Q) ∩ TL(𝓛_Q), from every
  centre C ∈ 𝓛_Q the §6.10 path deletes one element of C ∖ S₀ per move, reaches S₀ after exactly |C ∖ S₀| moves, and
  the capped search scores S₀ if the cap is ≥ |C ∖ S₀| − 1. Its hypotheses are only S₀ ⊆ Q, |Q| ≤ K (no bound on |Q|).
* L2 (Sandwich), L3 (NA, TL) of this folder.

**Theorem L4.1 (FAC-L, fixed design).** Assume model G, (H0), (AG), (P), (TV), and the method premises of STATEMENT
§1. Then for n ≥ n₀,

  D_n ≤ P(Sand_nᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0,  𝓛 = [S₀, [p]],

hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U_n). On Sand_n ∩ NA(𝓛) ∩ TL(𝓛), LS0
(the prescribed deterministic search, viewed as uninterrupted on these data) reaches S₀ after exactly
τ := |S̃₀ ∖ S₀| moves (all deletions of extras) and scores it by the scan after max(τ − 1, 0) moves (the centre is scored
when τ = 0); a delivered SMC run executes this search, and enumeration scores S₀ directly (R06 item 4).

*Proof.* Under (P), p = o(n), so K = min(p, ⌊n/2⌋) = p for n ≥ n₀; take Q := [p] in [GROW-L1] (|Q| = p ≤ K). By [OP],
D_n ≤ P(LS0 from the emitted centre does not score S₀). The emitted centre is a maximiser of γ₀ (premise); on Sand_n it
contains S₀, hence lies in 𝓛 (every subset of [p] is in Ω since p ≤ K). On Sand_n ∩ NA(𝓛) ∩ TL(𝓛), [GROW-L1] with
C := S̃₀ shows LS0 scores S₀ as soon as its cap is ≥ |S̃₀ ∖ S₀| − 1; the merged cap is ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀|.
This proves the display. P(Sand_nᶜ) → 0 by L2 (its hypotheses: G, energy bound in (H0), (AG) ⇒ (G3a), (P) ⇒ p ≤ n^A and
K = p, (TV)); P(NA(𝓛)ᶜ), P(TL(𝓛)ᶜ) → 0 by L3 (G, (H0) (energy, BM-∞), (AG), (P)). By [S-T], δ₁ := 1 − π(S₀) → 0 in
probability and δ₁ ∈ [0, 1], so E₀δ₁ → 0; [M5-0] gives P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and
P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}). ∎

**Notes.** (1) The exact-enumeration branch only helps (S₀ is scored there once s₀ ≤ K), as in GEN L5 and GROW L4.
(2) For R′ > 4 the extra search from c₄ only adds scored models. (3) Nothing is conditioned on 𝒪. (4) Unlike GROW, the
number of LS0 moves here is typically of order p (the start mode tends to [p], numerics D2), which is why the merged
cap ℓ_n + |S̃₀| (and not ℓ_n) is needed; no new method requirement arises. (5) (H0) is needed only for [S-T] and for
the energy bound/BM-∞ in L2, L3; its anchored eigenvalue parts follow from (AG) (λ_min(R̂) ≥ 3ψ₀/4 on all subsets).
