# BT1 disposition (lead) — "better theorem" review by Codex gpt-6-astra (high), blind

Review: `BT1_better_theorem_astra.md`, manifest 65ee6108be26dc13108a18e0b4a9032f25d3092c50bcc17044beb84730e6bec7
(STATEMENT v1.2 LOCKED, ASSUMPTION_MAP, numerics with 207 runs). Three proposals (P1, P2 ADOPT NOW; P3 WORTH A
TICKET) and eight directions with "no credible improvement". The statement is locked: **nothing below has been
applied**; each item is a recommendation for HQ's CP1 decision (PROTOCOL item 3). Lead's own items are G1–G4.

## Proposals

| id | proposal | lead's disposition | evidence |
|---|---|---|---|
| **P1** | Replace **(BM-Q)** by **(BM-width)**: with 𝒟_n := {u_{A,i} : T ∈ 𝓛, i ∈ S₀, A = T ∖ {i} or (T ∖ {i}) ∪ {l}} (truth-removal directions, deletions *and* swaps) and d_n := E sup_{v∈𝒟_n} \|vᵀg\|, require θ*²_min(n − 1)φ₀²/(σ²(d_n² + log n)) → ∞. Since d_n² = O(\|Q\| + log n) always, (BM-Q) ⇒ (BM-width); when d_n² = O(log n), BM-∞ suffices | **ADOPT (recommended).** Weaker hypothesis, same conclusion, cheap: the truth-removal step uses the exact two-square identity RSS_A − RSS_T = (θ_i‖(I − P_A)x_i‖ + σZ_{A,i})² − σ²Z²_{T,l} instead of the toolkit's contrast bound; the toolkit is still needed for score regularity only. It is the item the lead had flagged in ASSUMPTION_MAP (A:BM-Q: single-use union bound, "WEAKENABLE") | identity checked numerically, 400 comparisons with correlated columns and signed coefficients, max relative error 1.2e-14 (`reviews/post_BT1_addendum/check_identity.R`, `check_identity_out.txt`); containment (BM-Q) ⇒ (BM-width) is a cardinality bound; risk named by the reviewer (swap directions must be in 𝒟_n) is met by the definition |
| **P2** | Replace the fixed-δ form of **(W)** by a diverging additive gap: E max_𝔓(\|u_{T,l}ᵀg\| − √c_n(\|T\|)) ≤ −t_n, t_n → ∞ (**W-gap**); and add the conclusion P(NA(𝓛)ᶜ) ≤ n^{−c*} + O(1/n), c* = δ₀²/(32(2A + 2)), under the locked (W) | **ADOPT (recommended), in a slightly different form — lead's G1 below.** The level √c_n(k) contains the proof constant κ_E; the same statement holds with the constant-free level a⁰_n(k) := √(log(n + 1) + 2 log(p/(k + 1))), because √c_n(k) and a⁰_n(k) differ by O(1/√log n). The NA rate is adopted as stated | the reviewer's proof is three lines of Gaussian concentration; the locked (W) implies W-gap with t_n ≍ √log n; nothing is lost |
| **P3** | Form R: leak scale a_n = o(√(log n/n)) instead of C_L n^{−1/2}, and localisation rate r_n = o((n/log n)^{−1/4}) instead of o((n log n)^{−1/4}); same budget 15ρ + b < ½ | **DEFER as named open item O3, with an option:** (P7) SAND-R^b re-proves the spherical tail anyway, so the non-central version can be attempted inside (P7) with a one-attempt kill budget; if it does not close, the locked rates stay. HQ to choose between "defer" and "attempt inside P7". It matches W3-RM's recorded open items (R02 P3b, R04 F6/F8) | the reviewer rates it WORTH A TICKET and names the risk: uniformity of the non-central spherical tail when the mean shift grows like o(√log n) |

## Lead's own items

| id | item | disposition |
|---|---|---|
| **G1** (refines P2) | State (W) as **𝔴⁰_n := E max_𝔓(\|u_{T,l}ᵀg\| − a⁰_n(\|T\|)) → −∞** and the converse as **𝔴⁰_n → +∞ ⇒ P(NA(𝓛)) → 0**. Both directions are Gaussian concentration of the same 1-Lipschitz functional plus the two-sided score conversion (the factor 2 on p in the locked a⁺ level shifts the level by ≤ log 2/√log n → 0). The locked pair (W)/(W-conv) with fixed δ's is the special case of gaps of order √log n. Result: whole-lattice no-addition holds w.p. → 1 if the width gap → −∞ and fails w.p. → 1 if it → +∞ — an (almost) exact characterisation, constant-free | **ADOPT (recommended)** together with P2; the sufficient forms (W-χ), (W-ref), (W-loc) are unchanged and imply it |
| **G2** | A polynomial rate for the search event in Form F: P(𝒦_nᶜ) = O(n^{−c₀}) (sandwich ladder O(√log n · n^{−ξ}); maxima thresholds with n^{−c} instead of 1/log n; NA rate of P2; TL under (BM-width) with r log n deviations). No rate for the reported model (the posterior input gives only E[1 − π(S₀)] → 0) | **ADOPT IF CHEAP at proof time** (a remark/corollary of (C1); no hypothesis changes) |
| **G3** | b ≥ ½ and leak levels beyond the frontier. Numerics: at b = 0.5–0.75 LS0 still ends at S₀ (48/48) with up to 4 non-deletion moves; at η = 1, n = 1600, it stops at the move cap before S₀ in 4/6 runs (19–73 swaps against a slack of ℓ_n + s₀ = 15). The quantity that decides the conclusion out there is the number of non-deletion moves against the cap slack | **DEFER as named open item O1** (path-level ticket; PROTOCOL rule 14). Input for it: the cap-slack accounting and the observed failure mode. Not this ticket |
| **G4** | Decoupling b from η by a *leak profile* (how many outside columns leak at each level) instead of a uniform level | **DEFER as named open item O2.** The reviewer confirms that under the worst-case hypothesis (L-gain) a counting argument reproduces b < β(η, A); a profile hypothesis is a different (more detailed) assumption |

## Directions where the reviewer found no credible improvement (recorded; no action)
1. removing the b/η coupling under (L-gain), or the n^{15ρ} reference count in Form R — the counting argument gives
   the same threshold; consistent with G4/O2;
2. b ≥ ½ with a deterministic sandwich — outside pure-noise entrants stop vanishing; consistent with B1 and O1;
3. removing (BM-Q) with no geometric replacement — P1 is the replacement; (W) alone does not control swap-removal
   directions;
4. a weaker descent condition tolerating whole-lattice improving additions — would need a path argument (O1);
5. a common-factor primitive certified broader than (W-ref)/(W-loc) — not claimed; the equicorrelated example in
   (C5) stays a candidate (**named open item O4**: verify or drop it at the examples stage);
6. an exact converse threshold from mean-width concentration alone — G1 gives the two one-sided statements
   (gap → −∞ / gap → +∞); the bounded-gap window stays undetermined, and no coded-LS0 failure follows from the
   failure of (W) (B2 observes the opposite);
7. a polynomial rate for the whole reported-model theorem — only for the search event (G2);
8. an unconditional old-cap result at polynomial size — none; (C1) keeps "the old cap is not covered beyond (W-χ)".

## Named open items after this round
O1 path-level control beyond b ≥ ½ / beyond the leak frontier, with cap accounting (separate ticket);
O2 leak-profile (counting) form of (L); O3 Form R leak and localisation scales (P3); O4 the equicorrelated
leak-group example.

## Protocol note
`manifest.py bind` on this review returns REFUSED ("no COUNCIL-VERDICT line"): the tool binds council verdict lines
only, and a better-theorem review has none. The review quotes the manifest digest verbatim on its first line, and
`manifest.py verify` passes on MANIFEST_BT1 for the current tree. The same holds for SL1, RC1, RC2 (each quotes its
digest; none is a council review).
