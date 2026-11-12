# BT2 — disposition of the better-theorem review on the final statement (lead, 2026-11-11)

Review: `reviews/BT2_better_theorem_astra.md` (Codex gpt-6-astra, reasoningEffort high; blind first read; frozen
content `reviews/MANIFEST_R2.txt`, digest `5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885`, quoted by
the reviewer). Purpose: PROTOCOL rule 10, headline strength — the statement changed materially after CP1 (v1.2 →
v1.3.4), so the better-theorem review is repeated on the final statement.

**Outcome.** Four proposals, each rated ADOPT NOW by the reviewer. None changes a hypothesis, the rate or the scope
of the main clause (Q = S₀ at p ≫ n: (T1)(b) to leading order, (T3)(b) no-leakage clause) or of Theorem FLOOR. For the
exponent ½, (GF-16), (E), the necessity of (AL), the visibility gap, the factor exp(C_R√log n), the fixed-constant
C_L = 0 bound, growing s₀ and non-Gaussian laws the reviewer records "no credible improvement", with the obstruction.

The lead checked each sketch against the proof files (read-only; the frozen content is not edited). "Credible" below
is the lead's reading after that check; it is not a line check and proves nothing.

| label | proposal | claims it would change | lead's check | proposed disposition |
|---|---|---|---|---|
| BT2-P1 | Leading functional: for s₀ ≥ 1 replace the term 15√(2/π)z_n/p of 𝔏⁰_n(h) by 1/p in the O_P bound (T1)(b), in the uniform form (T1)(d), in (T3)(a) and IF-START; hence F2 without the hypothesis p/√log n → ∞ | START-F, F2, TRANSFER, IF-START (statement §2: definition of the leading functional) | **credible.** The term comes from the truncated expectation J_{h_l}(0, σ) = √(2/π)h_l of at most 15 columns that share a block with all of S₀ (`STATEMENT.md:112-116`, `lemmas/L3_LEAK.md:39`). For a bounded number of columns with δ = 0, τ = σ an O_P bound needs tightness only, so a fixed cutoff H_ε replaces z_n; the prior factor is O(1/p). The (T1)(d) constants then depend on ε through H_ε (they already depend on ε). Gain: bounded and slowly growing p (p ≲ √log n) | `ticket` |
| BT2-P2 | Proposition OVL under (V-m) as well as (V-c) | OVL (and the exclusion in statement §6) | **credible.** (V-c) enters the proof only through the factor (1 + e_n)^{s₀} of (10.1) (`lemmas/L10_INTERFACES.md:33-35`, step (ii) at `:44`). The identity 1/π₀(S₀) = [Z_𝓛/γ₀(S₀)]/π₀(𝓛(Q)) is exact; Z_𝓛/γ₀(S₀) ≤ ∏_{l∈Q∖S₀}(1 + \|Q\|m_l/p) is the part of (AGG-c) with no deleted truth ((P3), (CH): `lemmas/L1_AGG_FLOOR.md:19-29`, `:91-96`); π₀(𝓛(Q)) → 1 is (T1)(a), which holds under (V-m). Steps (iii)–(iv) of L10.2 are unchanged | `ticket` |
| BT2-P3 | A non-vacuous partition-free leaking-null limit for 1 ≤ s₀ ≤ 15: 17 − s₀ designated nulls, each leaking above 1 + 2Ā given every proper subset of S₀ of size ≤ 15 | NEC (clause (N2)) | **credible.** Counting: a block has at most 16 columns, so at most 16 − s₀ nulls share a block with all truths; one of 17 − s₀ designated nulls has U*_{b(l)} ⊊ S₀ and is a witness for (C2)(i) (`lemmas/L7_NEC.md` L7.1). The witness is a function of X, so no selection penalty. For s₀ ≥ 16 it is the present (N2) | `ticket` |
| BT2-P4 | (T3)(b) with \|Q\| ≤ n^{1/2−ε_Q} (and \|Q\| ≤ K) in place of \|Q\| ≤ (log n)^{κ_Q}; \|H_l\| stays polylogarithmic | BR ((L-R)), START-R | **credible.** \|Q\| ≤ (log n)^{κ_Q} is used once, for ϱ̄_n → 0 (`lemmas/L9_BR.md:161`); N_ref counts subsets of H_l (`:95`) and P(Eᶜ) does not depend on \|Q\| (`:130`). With the new bound ϱ̄_n = n^{−ε_Q+o(1)}, which is below the threshold c₀ of the uniform theorem. The no-leakage clause is unchanged | `ticket` |

**Why `ticket` and not `adopted` in this ticket.** Each proposal changes a hypothesis or a conclusion of a claim, so
by PROTOCOL rule 15 it needs a fresh review of the change and of what depends on it, and a new council round on a new
manifest. Version 1.3.4 has just been reviewed as a whole on a frozen manifest; adopting now would discard that round
and use the third and last council round of this ticket on five changed claims. The four changes are cheap and
independent of the main clause, so they fit one short follow-up (statement v1.4: statement lock → two line checks →
council), whose claims supersede START-F, F2, TRANSFER, IF-START, OVL, NEC, BR and START-R by implication
(LIFECYCLE supersession). **This is HQ's decision** (CP3): HQ may instead order adoption inside this ticket with a
round R3.

**Named open items** (added to the ticket's list): W3-START-O4 = BT2-P1, W3-START-O5 = BT2-P2, W3-START-O6 = BT2-P3,
W3-START-O7 = BT2-P4.

**Headline gate.** With these dispositions recorded, every credible better-theorem proposal on the final statement
has a disposition. The `lit:` gate is still open, so the claims stay `headline-strength pending`. The lead's reading
for the paper: (T0), (T1) at Q = S₀ and the no-leakage clause of (T3)(b) can be stated as they are; F2 for bounded p,
OVL, (N2) and the lattice clause of (T3)(b) should be stated in their improved forms once the follow-up is checked.
