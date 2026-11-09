# BT1 disposition — "better theorem" review (gpt-6-astra high), 2026-11-09

Lead re-derived each adopted item line by line before adoption (derivations in the lemma files named below).

| BT1 item | Disposition | Where |
|---|---|---|
| §1 T-free C: E|W_r − 1| ≤ β ≤ 2max(δ, (1−δ)o₀) ≤ 2δ̄ by telescoping the negative potential loss against MR-a | **ADOPTED** (replaces the T·δ̄ evidence bound; hypothesis of C-v becomes 1_𝒜δ̄ → 0, i.e. P-CONC + π₀(S₀) → 1, no rate) | `lemmas/C_theorem.md` v2 Steps 3–4; STATEMENT v3 C-iii, C-v; P-START loses its T and its rate |
| §1 keep the T-dependent occupation bound C-ii separate | ADOPTED (C-ii kept, labelled as a bridge-occupation statement) | C-ii |
| Candidate 1 (min(T, D⁺)) | superseded; not pursued | ASSUMPTION_MAP |
| §2 terminal repair under global overlap L/M → ∞ (minorization K_I ≥ π/M; Doeblin; stationary coupling) | **ADOPTED** as new Theorem TR — the non-circular, (π, π₀)-only premise alternative to NC_r for item (b) | `lemmas/TR_theorem.md`; STATEMENT v3 |
| §2 three-state example: start mass alone does not control M | ADOPTED as a remark in TR | TR remark |
| §3.1 D with the MAP premise P(S† ≠ S₀) instead of P(δ ≥ ½) | **ADOPTED** (strictly weaker premise, same proof) | `lemmas/D_theorem.md` v2; D-iii, D-iv |
| §3.2 Gibbs-/swap-neighbour scoring bound (11) | NOT ADOPTED in this ticket (global M makes b_G tiny in practice; adds review load). Recorded for HQ as an optional extension | REPORT open items |
| §4.1 E[W E_r] ≤ g and E E_r ≤ g + β/2 (uniform RB error, T-free, no union over islands) | **ADOPTED** (C-iv rewritten; LT-b′ added) | `lemmas/LT_theorem.md` v2 Step 2′; C v2 Step 5 |
| §4.2 bias |E p̂_r(j) − PIP_j| ≤ β/2 | ADOPTED (one line in C-iv) | C v2 Step 5 |
| §4.3 evidence-pooled secondary estimator | NOT ADOPTED (not a reported field on main); noted | REPORT |
| §4.4 log-evidence tail P(|log W̄| > u) ≤ β/(1 − e^{−u}); O_P(r_n) rates | ADOPTED (C-iii, C-v) | C v2 |
| §5 ST constant 18 | NOT ADOPTED (19 kept; immaterial) | — |
| §5 NC with a vanishing threshold η_n (1_𝒜 g/η_n → 0) | ADOPTED as LT-e′ | LT v2 Step 5 |

Statement consequence: STATEMENT v2 → v3 (sharpness-gate amendments; all strengthenings, no claim weakened). The
mid-point reviewer receives v3.
