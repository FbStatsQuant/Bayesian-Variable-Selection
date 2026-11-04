# W5-B2ENV — working notes

Branch `theory/W5-B2ENV` (from `theory/campaign` @ 9db8748). Task: `theory_campaign/tasks/W5-B2ENV.md`.

Inputs read: W4-SHARE (PROOF §§0–7, scripts), W1-T38E (PROOF §§1–8), W3-VT38E (REPORT), W3-PXN (PROOF §§0,10,12–14),
W4-T38FULL (T38_PROOF §§3.4, 4.2), W2-PREM (PROOF §§0,1,5,8,9), W1-T24G (PROOF §0, Cor P1), W1-EXP (PROOF §§1–4),
F-REFINE (ARCHITECTURE, CARDS card 6), METHODOLOGY_v3 §§6.5–6.8.

Plan:
1. Referee W4-SHARE (D4, D5, G, SH, X, M(a), PD, B2-W4).
2. NB′ for D2 on LH exact Gram, c = 1: exact orthogonal factorisation of d on states that do not touch both groups of
   the linked pair (Lemma OF) + peeling bounds on the bad draw sets.
3. Route (b2) on LH: choose the delivery region 𝒩 = {S ⊇ S°, at most k_ν neutral extras, any subset of the masked
   groups}; junk is non-persistent, so confinement holds for every grid (Prop X form); D5 then has Γ = 0; one-round
   repair at φ = 1 from every state of 𝒩 with a fixed probability c₀ > 0.
4. Prop M(b) on LH (lattice gains).
5. Numerics with exact scores at p = 16 (LH config A).
