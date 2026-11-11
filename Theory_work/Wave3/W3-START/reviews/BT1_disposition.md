# BT1 disposition (lead, 2026-11-11) — review `reviews/BT1_better_theorem_astra.md` (Codex gpt-6-astra high, blind)

Manifest `b3fafa79685f4562886d5e268432b95eba30fc75075cc50eaa30591e3546b7b2` quoted by the reviewer; `manifest.py bind` OK.
Dispositions below are the lead's **recommendations**; HQ decides at CP1 (PROTOCOL rule 10). Nothing is changed in the
locked STATEMENT v1.2 until HQ replies; an adopted change is substantive and gets a fresh Sol check of the change
(rule 15) before proof work uses it.

| label | proposal | recommended disposition | evidence |
|---|---|---|---|
| P1 | Replace (FL-16) (λ_min(R̂_T) ≥ φ₀²) by a constant **unnormalised** Gram floor (GF-16): λ_min(X_TᵀX_T) ≥ g_* > 0 for 1 ≤ \|T\| ≤ 16; same rates. | **ADOPT** | Lead re-derived both scalar bounds from the pinned scorer: D_T/(n+1)^k = ∏(g_i + 1/(n+1))/(g_i + 1) ∈ [(g_*/(g_*+1))^k, 1]; 0 ≤ Q_T − RSS^y_T ≤ (1 + 1/g_*)‖P_Ty‖²/(n+1) ≤ 1 + 1/g_*. So the table expansion keeps an O(1) remainder; the Gaussian events and the RSS bounds never used the floor. Numerics (e): near-twin nulls have λ_min(X_TᵀX_T) ≈ 1 and the conclusion holds. Cost: the toolkit lemma is re-proved locally under (GF-16) (C-GROW:L0.1/L0.2 are stated with the normalised floor and can then no longer be consumed for [TK]); F2 keeps its own floor on R̂_{S₀}. |
| P2 | Column-specific truncation levels h_l ≤ z_n with Σ_l 2¹⁶e^{−h_l²/2} → 0 in J_n, 𝔏_n(Q), 𝔏⁰_n; (AL) in that form. Recovers the present condition at h_l ≡ z_n. | **ADOPT as the general form of (AL)** (default h ≡ z_n in the headline; (T3)(b) keeps h ≡ z_n) | It removes the flag found in numerics (c): with h_l = √(4 log log n) on an isolated leaker, its contribution to n^{−1/2}𝔏_h is n^{c/2−1/2−A+o(1)}, which → 0 exactly when c < 1 + 2A — the threshold of (N2) — whereas the present 𝔏_n rejects c ∈ (≈1.3, 3.2). The proof of bridge (B-L) is unchanged apart from the union bound (at most 2¹⁵ block sets per column, budget b_n). Extra work: carry b_n through (T1)(d) and (T3)(a). The reviewer rates it WORTH A TICKET; the lead judges it small enough to do inside this ticket, and it supersedes the lead's own fallback (isolated leakers through the lattice set Q). |
| P3 | Transfer (T3)(a), and the random-candidate clause of (T6), to design-measurable θ*(X), S₀(X), Q(X) of fixed cardinality. | **ADOPT** | Immediate from the uniform clause (T1)(d): conditional on X the objects are fixed and the constants depend only on the displayed bounds. Removes an exclusion in (T6)/§6. Scope note kept: response-selected supports are not covered. |

"No credible improvement" (reviewer's list, recorded as evidence for the necessity readings): removing the Gram floor
altogether (needs a rank-sensitive aggregation); replacing 𝔏_n(S₀) by the leading functional (joint null
configurations); a cleaner (V-m); deleting the energy bound; removing localisation or the factor e^{C_R√log n};
growing s₀ and non-Gaussian noise (not cheap); a universal √(log p/n) lower bound.

## Lead's own sharpness-gate items
| label | item | disposition | evidence |
|---|---|---|---|
| G1 | truth-block functional Ξ and margin visibility (V-m) instead of e_n and (V-c) over all 15-sets | **ADOPTED** in v1.1 and lock-reviewed (SL2, RC2) | numerics (b) |
| G2 | Gaussian rows: population leakage level η (\|partial covariance\|² ≤ η log n/n) with an explicit exponent, instead of the scale C_L n^{−1/2} | **DEFER** — named open item W3-START-O1; decide at CP3, once bridge (B-R) exists for bounded shifts (the extension is then a change of one parameter in the same Gaussian integral) | numerics (h): graded in η, no cliff at C_L n^{−1/2}; heuristic exponent ½ − √(2Aη′) + η′/2 |
| G3 | isolated strong leakers through the lattice set Q (Proposition OVL extended to give π₀(S₀) → 1) | **REJECT** in favour of P2 (same threshold 1 + 2A, without enlarging Q) | numerics (c); P2's computation |
| G4 | drop the Gram floor among nulls entirely | **DEFER** — open item W3-START-O2 (low priority) | P1 reaches the eigenvalue scale 1/n of the numerics; beyond it the reviewer's obstruction stands |
| G5 | weaken ‖μ‖² ≤ Mn | **REJECT for now** (route constant; reviewer's obstruction: the scorer's fixed 0.02 and ridge remainders are O(1) only when RSS^y ≥ cn) | numerics (f) covers only θ ∝ n^{1/4} |
| G6 | growing s₀ | **DEFER** — open item W3-START-O3 | numerics (g): what binds is the τ²-normalised visibility; reviewer: not a cheap consequence |
