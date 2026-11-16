# L1 — statement lock, W3-MISR-R (brief, saved before launch)

Reviewer: Sol (codex, gpt-6.1-sol, reasoningEffort high), fresh agent, blind first read. Role: statement-lock reviewer
(PROTOCOL_v4 §3.1, §2A step 1).

---

You are the statement-lock reviewer for the rider ticket W3-MISR-R in the repository checkout
`/home/fb31/BVS-wt/W3-MISR-R` (read-only for you, except the one reply file named below). You have never reviewed this
ticket. Read only the files listed here (and files they cite by `file:line` when you need to check a citation).

**Task.** Check the delta statement and plan against the sources: right target, faithfully stated, every hypothesis
explicit, each claim plausibly provable as planned, each "implies" row of §8 true, citations correct. Try to break
each claim: look for counterexamples, missing hypotheses (measurability, null events, non-constant columns, constants
that silently depend on n or on the sequence, quantifier order, uniformity), over-claims, and mismatches between a
clause and what the cited source states. Statement-level only: no lemma files exist yet; judge the proof sketches in
`PLAN.md` §1 for viability.

**Files to review (the frozen inputs).**
1. `Theory_work/Wave3/W3-MISR-R/STATEMENT.md` (v1.0; the delta statement — the object of the lock).
2. `Theory_work/Wave3/W3-MISR-R/PLAN.md` (proof sketches, §1).
3. `Theory_work/Wave3/W3-MISR-R/BRIEF.md` (what the ticket was asked to do).
4. Parent (BASE): `Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.3), `Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md`
   (G.1–G.3), `Theory_work/Wave3/W3-MISR/lemmas/M_misr.md` (§M.3 and the (M0) display near the top),
   `Theory_work/Wave3/W3-MISR/lemmas/R_reduction.md` (Lemma R′).
5. Consumed upstream statements: `Theory_work/Wave3/W3-POST2/STATEMENT.md` (Notation, (OS) at :29-36, implications
   :46-47, Claim D at :99-119), `Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md` (D0, D2, D3),
   `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md` (Lemma A0, :14-27), `Theory_work/Wave3/W3-POST/STATEMENT.md` (§0 :16-40,
   regime R1 and hypotheses :63-78).
6. Motivation: `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md` rows at :40-42, §2 row T13 (:81), §3 (:88-103).

**Specific questions** (answer each):
Q1. CorG-min (§2): is (a) true as stated (arbitrary candidate-design law; α arbitrary random; γ, τ² Borel in the
    design)? Are (c) (necessity under Gaussian noise) and (d) (Cramér partial converse) true and correctly quantified?
    Is (E1) with a singular Σ_𝒞𝒞 and the Moore–Penrose inverse correct?
Q2. CorGb-plus (§3): does BASE G.2 go through with Gaussian candidate rows + (OV) (no joint Gaussianity), a floor on the
    correlation matrix only on |T| ≤ k_n (no global Σ_𝒞𝒞 ≻ 0), and the liminf beta-min condition, with the stated
    constants and explicit bound? Is the column-rescaling invariance of the coded target correctly used?
Q3. CorH-plus (§4): does (a′) follow from [POST2] D(a) under exactly (SZ), (E^σ), (F₀), δ_n → 0 (no (OS))? Is the (KL)
    display correct, and the KL reading (i)–(ii) correctly scoped?
Q4. CorH-U (§5): is the subsequence-with-fillers argument (PLAN H0, (U-b), (U-a)) valid for turning the sequence
    statements of [POST2] D(a)/D(b) into the uniform statements, including the constants it relies on (C_H depends only
    on (s, A); D(a) has no constants in its conclusion; the filler class constants are n-free)? Is (RD) correct as a
    freezing argument (measurability of the posterior functional; Π depends on y^r only through Uᵀy^r)?
Q5. §8: is each "implies" row true? §7: are the inputs and statuses complete for what the claims use?
Q6. Is anything in the statement stronger than the plan can deliver, or anything that should be weakened, dropped or
    made explicit before the lock?

**Output.** Write your full reply to `Theory_work/Wave3/W3-MISR-R/reviews/L1_statement_lock_sol.md` (create it; write
nothing else anywhere). Format: findings numbered L1-1, L1-2, …, each with severity FATAL / MAJOR / MINOR / NIT, the
clause and line, what fails, and a concrete fix; then the answers to Q1–Q6; then one final line
`LOCK-VERDICT: LOCK | LOCK-WITH-AMENDMENTS | NO-LOCK`. Also return the same content as your final message.
