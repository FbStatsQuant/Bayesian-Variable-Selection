# MEET-THM · Round 3 brief (identical for Seats A, B, C, D)

Chair (non-voting), 2026-11-04. The agenda is frozen at dispatch. This is the last round.

You are **Seat {SEAT}** of MEET-THM (paper 1's theorem list). You are **read-only**: do not edit, commit or push. Your **final message is your full answer**, filed verbatim as `R3_{SEAT}.md`. Small local checks only (Python, < 1 min, ≤ 20 seeds, outside the repository).

Working directory: `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-THM`. Run `git fetch origin`.

## Read
1. `theory_campaign/MEET-THM/SYNTH_R2.md` (and its audit `SYNTH_R2_AUDIT.md` if present; the audit's corrections bind). This is the chair's reconciled-list **proposal** (§2), the required repairs (§3), the open items R3-1…R3-6 (§4) and this agenda (§5).
2. HQ rulings: `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`, `evidence/2026-11-04_HQ_RULING_Q5.md`.
3. The check verdicts:
   - `evidence/W2_PC1/VERDICTS.md`, `evidence/W2_PC2/VERDICTS.md`;
   - wave 1 `evidence/W1_PC*/VERDICTS.md`;
   - `evidence/CHK_INHERITED/REPORT.md`.
4. All Round 2 answers `R2_A.md`–`R2_D.md`. Your own Round 1 and Round 2 answers.
5. `DOSSIER.md` §4 (IC1–IC7), §5 (the card), §9 (deliverables).

## Rules (unchanged)
- The method is fixed; growth rates only (the R′ edit in SYNTH_R2 §2.6). Depth is claimed at the island level only.
- Binding goals escalate; they are never dropped. Hypotheses are model/design conditions; implementation premises are named as such.
- Statuses are verbatim, with qualifiers, never upgraded. A checker's COUNTEREXAMPLE stands. An OPEN conjecture is not a list theorem.
- No open questions at close. Every item is one of:
  - on the list (with a fallback);
  - FUTURE_WORK (with a reason);
  - a cited lemma;
  - dropped (with a reason).

## Answer in these sections. Tables; ≤ 60 words per row; ≤ 300 words of free text per card; whole answer ≤ 10,000 words

**§S1 Confirm or object.**
- For each row of SYNTH_R2 §2.1, §2.2, §2.4, §2.5, §2.6 and §3: `item | confirm / object | reason (only if object) | what would change it`.
- Then R3-1 to R3-6: your choice and its reason.
- For R3-1, the 8th main slot, choose one: (i) Proposition D in main; (ii) standalone V+ (M1 split); or (iii) 7 main theorems. Weigh IC5: with (i) in the supplement, no main theorem serves objective (2), parallel scalability.

**§S2 Final cards for your assigned theorems** (below). One card per theorem, with the dossier §5 fields:
- ID (K-IDs) and final statement with every hypothesis named; implementation premises listed separately;
- guarantee in one sentence;
- objective, proposal goal and Song–Liang item served;
- status verbatim with qualifiers, and fidelity to v3.1 as shipped;
- self-checked flag;
- novelty, with the citations you checked;
- proof route and key lemma; difficulty;
- Lean core;
- dependencies on other list items (by card ID);
- risk;
- fallback statement + stop rule (a fallback may not silently drop a binding goal);
- IC3 design, exhibited, with where it was checked;
- numerical companion (≤ 20 seeds).

Use only clauses that the checks found TRUE-AS-WRITTEN, or that are repaired exactly as SYNTH_R2 §3 requires. Cite the verdict row for each clause.

**§S3 Agenda 12, the HQ plan.**
- (a) **Dependency graph.** Main and supplement items plus the key lemmas, as an edge list `X → Y` (Y uses X).
- (b) **Launch waves** of 3–4 theorems each, foundations first, with a one-line reason per wave.
- (c) **One charter per assigned main theorem** (≤ 200 words each):
  - goal;
  - the statement to prove (pointer to your §S2 card);
  - first lemma to attack;
  - Lean target;
  - independent-check plan (cross-family);
  - fallback and stop rule;
  - the evidence that would trigger escalation to HQ.

**§S4 Nothing missing.**
- Confirm that every proposal goal (§5.1–5.4, §13.1), every Song–Liang item, every THM-INV §1 cell and every obligation N1–N17 has one of: a list item, a FUTURE_WORK entry with a reason, or a cited lemma.
- Otherwise name what is missing, as `item | where it should go | why`.

**§S5 Questions for HQ** (only outside the meeting's authority; "None" is valid).

## Assignments for §S2/§S3(c) (main theorems, SYNTH_R2 §2.1)

| Seat | Draft final cards and charters for |
|---|---|
| A | M1 (Theorem V/H; also draft the split version V+ / H if you choose R3-1 (ii)) and M7 (STG) |
| B | M2 (§5.3 package WS, with HQ Q1 + Q5 conditions) and M4 (Z𝒯 + certificate card + masked statement) |
| C | M3 (START) and M6 (SEP + Lemma KL), plus the run-card reporting corollary S-REP (Ĵ, ε̂_×) |
| D | M5 (HPM) and Proposition D (work/depth), drafted as a card whatever R3-1 decides |
