# W3-START2-R — CHECKPOINT 1 (target fixed) — 2026-11-15

Lead: Claude Opus 5.5, effort high (Claude Third). Tier B rider, NORMAL mode. No git state changed. No holds on
`origin/main:Theory_work/Wave3/HOLDS.md`. **Nothing is proved or checked yet** (no lemma file written).

## Locked statement
`STATEMENT.md` **v1.5**, a delta over W3-START2 v1.4.1. Lock review **SL1**: Sol (codex gpt-6.1-sol, high, NORMAL
mode, fresh blind first read), verdict **LOCK WITH CHANGES**: 2 F, 3 E and 1 optional proposal, all applied
(`reviews/SL1_statement_lock_sol.md`, `reviews/SL1_disposition.md`). The one non-EQUAL changelog row (F #1: the bridges
take [TK] again, as their parents do) gets its statement-change check inside the LC1 Sol review, before any freeze.

## What changes, in plain words (for the H5 card)
1. **Start rate with Gaussian rows (headline: START2 (T3⁺)(b), IF-START⁺).** With no leakage, and null columns
   uncorrelated with the true columns (or correlated at most C/√(n log n) given proper subsets of the truth), the start
   puts mass **1 − O_P(√(log n/n))** on the true model. Before: (log n)^{15κ+1/2}/√n under exact zero leakage, and
   otherwise n^{−1/2}e^{C√log n}. The floor is ⅓(n + 1)^{−1/2}, so the new rate is optimal up to √log n. The locality
   sets H_l may now have size e^{κ√log n} instead of polylog. The sampler interface rate (IF-START) becomes √(log n/n).
2. **Fixed-design visibility (headline: START2 (T1⁺)).** Each truth's gain is asked at τ²(c·log n + 2 log p), c > 1, with
   the actual p. Before: (1 + 2A) log n, with A the exponent of the bound p ≤ n^A. The margin form keeps the negative
   prior price of adding nulls. The necessity side now uses the same level, so the threshold is **exactly 1 for every
   sequence p_n**, with drifting constants allowed (window of width 1/√log n). The conclusions are unchanged; the
   premise is weaker.
3. **Transfer** in conditional, random-rate form. Restatements of MIS (with an exact Gaussian instance of (GR)), EX
   (new rates), F1–F4 and OVL. The LEAK-0 remark is corrected; P1 of v1.4 is not sold as a p ≫ n gain.
None of these weakens a conclusion. Each new claim implies its parent (STATEMENT §5).

## Target clauses (16 claims, ids W3-START2-R:*)
| clause | kind | headline effect |
|---|---|---|
| START-R (T3⁺⁺)(b)(iii) o₀ = O_P(√(log n/n)); (b)(i) with \|H_l\| ≤ e^{κ_H√log n}; (b)(ii) C_L = 0 rate (\|Q\| + 1)N̄_n√(log n/n) | STRONGER | **yes** (START2 (T3⁺)(b)) |
| IF-START⁺⁺ rate √(log n/n) under (b)(iii) | STRONGER | **yes** (IF-START⁺) |
| START-F (T1⁺⁺) under (V-cp)/(V-mp) | STRONGER (weaker premise) | **yes** (START2 (T1⁺)) |
| BR⁺⁺ (incl. new (iii): 𝔏^♯_n = O_P(√log n)); TRANSFER⁺⁺; VIS-c⁺⁺, VIS-m⁺⁺; NEC-b⁺⁺, NEC⁺⁺; F1⁺⁺–F4⁺⁺; OVL⁺⁺; MIS⁺⁺; EX⁺⁺ | STRONGER | no |
Hypotheses of the main clauses: (T3⁺⁺)(b) Setting R, p > s₀, (FL-R16), (V-R), (L-R⁺⁺), and (L-gain-0) for (iii);
(T1⁺⁺) Setting F, (E), (GF-16), (V-cp) or (V-mp), (AL).

## Files
`TARGET.md` (assumption map, parity, boundary numerics plan); `READER_DELTA.md` (new Theorem 5 text: e^{κ√log n}
locality, a new assumption (A6) "nulls uncorrelated with truths" ⇒ 1 − π₀(S₀) = O_P(√(log n/n)); a proposed
fixed-design reader Theorem 5F showing that the visibility constant 1 is sharp for every p); `PLAN.md`; `DEPS.tsv`
(statement rows, UNCHECKED); `LOG.md`.

## Plan with hours (~11–13 Opus h; CP3 by Wed 11-18 18:00 CT)
R1_VIS + R2_NEC (T8, Opus helper A, ~3.5 h) ∥ R3_RATE (T10, lead, ~3 h); R4_TRANSFER_COR (~1.5 h); R5_EX (~1.5 h);
numerics (Sonnet helper B, ~1.5 h); LC1 (R1+R2+changelog check), LC2 (R3+R4+R5) by Sol; citecheck, REPORT, council R1
(Sol + Opus) Tue night; diff round Wed AM. Expected OpenAI reviews: 4. Kill budget: 2 attempts on the R3 step that
removes N_ref.

## Decisions asked of the manager
1. Approve the target. Two places go beyond the brief's wording, and each implies the brief's clause: (iii) assumes
   (L-gain-0) rather than C_L = 0; F2⁺⁺ and OVL⁺⁺ are restated as well.
2. T9/T11 (optional): I recommend **not** adopting them. They stay named open items, which leaves time for the two
   line checks and the council before the cut-off.
3. Go to launch helper A (Opus 5.5, high, Claude Third) for T8 and helper B (Sonnet 5.5, high) for the numerics.
