# W3-D3 — L1 disposition (lead, 2026-11-17)

Reply: `reviews/L1_statement_lock_sol.md` (Sol, gpt-6.1-sol high, fresh, blind): **LOCK-WITH-AMENDMENTS**; findings
L1-1 [C], L1-2 [S], L1-3 [E], L1-4 [E], L1-5 [E], L1-6 [E]. All accepted; STATEMENT v1.1 applies them as specified.

| finding | disposition | where |
|---|---|---|
| L1-1 [C] K = tail constant and cap; B3w(i) "s₀ ≤ K" false under the collision | ACCEPTED. Tail constant renamed **L** (the symbol of the reader version of Theorem 9, [RV] `:1097-1099`; the lock suggested K_SG — same fix, a symbol already used in the paper), L > 0; cap K_cap := min(p_ret, ⌊n/2⌋); n₁ ≥ max(3, 2s₀). The mixing matrix of ExSG renamed B to avoid a new clash. | STATEMENT "Symbols", §0–§3; `lemmas/B3w.md` statement, Steps 0–6; `lemmas/ASSEMBLY.md` |
| L1-2 [S] raw bridge events vs (X, θ*)-measurable interface events; fixed-dimension completion | ACCEPTED. B3w split into (a) on 𝒜_n, (b) probability, (c) interface: completed pair (X°, θ°) (deterministic centred standardised n × p matrix and fixed s₀-supported truth off {p_ret = p}), (X°, θ°)-measurable 𝒜′_n ⊇ 𝒜_n; ASSEMBLY Steps 2–4 transfer with error ≤ P(𝒜_nᶜ). | STATEMENT §2 (c); B3w Step 6 [R-11]; ASSEMBLY Steps 1–4 |
| L1-3 [E] convention when every column is removed | ACCEPTED: p_ret = 0 ⇒ π := δ_∅, HPM = MPM := ∅; stated as a convention, not a code property. | STATEMENT §0 |
| L1-4 [E] unit variances as a reduction rescales β* | ACCEPTED as remark (e). | STATEMENT §4 (e) |
| L1-5 [E] centring qualifier for the Song–Liang implication | ACCEPTED: "for z = x − m_n, unit marginal variances here". | STATEMENT §5 |
| L1-6 [E] provenance outside the span; reader copy; why-lines | ACCEPTED: provenance moved to §7/B3w header; registry-id lines are metadata; READER_DELTA carries the why-line and expands nothing beyond (S1), (S2) references, which the shared setup provides. | STATEMENT §2; READER_DELTA |

Also used from the reply (no change needed): the verification of both verbatim quotations (NH14 v1 p. 16; Song–Liang
p. 953) and the counterexample to the converse of "(A4) ⇒ Condition 1" (cited in STATEMENT §5 and remark (b)).

Lead edits in the same version (not from the lock): Q1, Q2 of `reviews/PENDING_LEAD_EDITS.md` (HQ's anchoring wording;
2b sentence replaced; **ExSG (b) added — STRONGER on the companion claim**, sent to the statement-change check).

**Lock.** With L1-1, L1-2 applied as the lock reviewer specified, STATEMENT v1.1 §§1–2 are locked. §3 (b) is a new
companion clause after the lock; its statement-change check and line check go with the K1 line check batch.
