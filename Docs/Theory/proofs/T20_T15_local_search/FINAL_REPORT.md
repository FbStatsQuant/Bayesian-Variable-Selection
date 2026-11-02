# FINAL_REPORT.md — T20 (T15), clauses (i)–(ii): local-search semantics

**Result: proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted.** Adoption is Felipe's word.

- Final proof: `proof/PROOF_v3.tex` and `proof/PROOF_v3.pdf` (5 pages).
- Final statement: `STATEMENT.md` (v3.1).
- Theorem file: `theorems/T20_T15_local_search.md`.
- Method: METHODOLOGY_v3, SHA-256 93043758…8019c, re-checked 2026-10-22.
- Date: 2026-10-22.

## 1. What was proved, in plain words

The method ends each phase with a **local search**. It starts from the best model found so far (the "centre") and scores every model that differs from it by adding, removing or swapping one variable. It then moves to the best strictly better model, and repeats for at most ℓ moves plus one last scan. It sets a flag, `local_certified`, when the reported model was itself a centre and none of its neighbours scored strictly higher.

**Clause (i): what the flag means.** Proved for any scoring function, assuming exact arithmetic and that every scan runs to completion.
- The flag is 1 exactly when the search stopped because a scan found no improvement *and* the reported model is that last centre (i-a).
- A certified model scores at least as high as each of its neighbours. Neighbours with the same score are allowed, but they must come after it in the HPM tie order.
- The flag depends only on models that were actually scored. It says nothing about unscored models, so it is not a certificate of global optimality unless every model was scored (i-b).
- Every model a scan scores, including ones not moved to, enters the HPM comparison (i-c).
- If the move limit is used up and the last scan still finds a better model:
  - that model becomes the reported HPM;
  - it was first found by that last scan and was never a centre;
  - it is not certified (i-d).
- Without exact score ties at the top: certified ⟺ the search did not hit the move limit (i-e).

**Clause (ii): one step from the truth.** Let E_n be the event that the true model S₀ is the strict global maximiser of the score.
- On E_n, any scan whose centre is one flip or swap away from S₀ scores S₀.
- If a move remains, the search moves to S₀, and the next scan certifies S₀.
- If no move remains, S₀ is still the reported HPM, but without the certificate.
- Two facts link this to the posterior:
  - (ii-B) The score margin of S₀ over every other model is at least its posterior log-odds, log[π(S₀)/(1−π(S₀))]. So π(S₀) > ½ already implies E_n.
  - (ii-C) Assume hypothesis H03, which is the conclusion of T03(i): 1 − π(S₀) = O_P(√(log n / n)). Then P₀(E_n) → 1, and the log-odds are at least ½ log n − ½ log log n − O_P(1). The statements above then hold for every scan of the run with probability tending to 1.

Neither part needed assumption EXP (or EXP′).

## 2. Changes to the statement

No hypothesis was changed or added. The step 1 outcome was (a), correct as stated.

To make the informal clauses precise, STATEMENT.md:
- formalises the method's §6.10 search as a short algorithm (§2), with the source text quoted verbatim in §0;
- uses T03 only through the explicit hypothesis H03;
- names the "scans execute" assumption EXEC;
- records seven readings in §5. Two examples:
  - "returned model" means the running HPM at the end of the search;
  - "can be the reported HPM without a certificate" is proved as a conditional ("on LIMIT, …"). No claim is made that LIMIT actually happens for real data.

Reviewer-driven text corrections (change log in STATEMENT.md §6):
- v1 → v2:
  - an explanatory remark in §5 was wrong and was fixed (A1-1);
  - the score formulas were written out in full (A1-2).
- v2 → v3:
  - (i-b)'s "does not certify global maximality" is now qualified by "when some model is unscored". A reviewer noted it was false if every model had been scored;
  - other edits are clarifications only.
- v3 → v3.1: readings and setting wording only.

## 3. Review history

**Stage A: lead + Astra #1** (GPT-6 Astra, high, session <uuid>).
- Round 1 on v1: *not verified*.
  - One "fatal" finding, in an explanatory reading note rather than a claim. The reviewer said it does not affect §§3–4.
  - One gap: Q_S was not defined in the packet.
  - One exposition finding.
  - All three were accepted and fixed.
- Round 2 on v2: *verified*. Astra agreed with both answers.

**Stage B: two fresh independent reviews of v2, started together.**
- **Astra #2** (new session <uuid>): *verified*. No fatal or gap findings; one cosmetic remark.
- **Opus 5.5 xhigh** (native Agent, read-only Plan type, Claude Work account): *verified*. Ten exposition or scope notes (F1–F10); seven applied in v3.
- **Ruling round on v3 and the claims log:** both *verified*, agreeing with every answer.
  - Both raised the same remaining exposition point, fixed in STATEMENT v3.1.
  - One harmless note (N3, on measurability) was left unapplied so the reviewed proof text stays final.

No disputes; the Astra judge was not used. The full log, with every fatal and gap finding verbatim and the lead's answers, is in `CLAIMS_OF_FATAL_FLAWS.md`. All replies are in `review/`.

**Numerical sanity check.** A Sonnet assistant ran a single-seed local check (`helpers/numcheck/NUMCHECK.md`).
- Scope: 72 small problems (p ≤ 8), where the whole model space can be scored, and 8,640 random search runs.
- Result: 0 failures across all checks of (i)–(ii), including tie canaries.
- This is a sanity check, not part of the proof.

## 4. Limits

- **The statistical part (ii-C) is conditional on H03.** T03 is itself a conjecture, being proved in a sibling thread. Nothing here proves H03.
- **The theorem is about the formalised algorithm**, with exact arithmetic (EX-A) and completed scans (EXEC). Numerical error and resource stops are outside its scope.
- **The link between STATEMENT.md and the method is supported by verbatim quotes** of METHODOLOGY_v3 §6.10 and §6.1. The lead checked them against the hashed file; the reviewers saw only the quotes.

## 5. Agent and call counts

| Model | Role | Calls |
|---|---|---|
| Opus 5.5 (high) | lead (this session) | — |
| GPT-6 Astra (high), #1 | Stage A consultant/reviewer | 2 (1 new session + 1 resume) |
| GPT-6 Astra (high), #2 | Stage B reviewer | 2 (1 new session + 1 resume) |
| Opus 5.5 (xhigh) | Stage B reviewer | 2 (1 spawn + 1 follow-up) |
| GPT-6 Astra (xhigh) | judge | 0 |
| Sonnet 5.5 | assistant: numerical check | 1 |
| Haiku 5.5, Fable, Sol | — | 0 |

The packet folders under `<PC_TEMP_PATH>` were deleted at the end. Nothing outside this project folder was edited.

## Stage C (campaign review, 2026-10-22)

- Final reviewers Fable 5.1 (high) and Astra (xhigh) both hold the proof correct (source: COLLECTED/review/FABLE_STAGE_C_phase2.md). Exposition edits applied: none (no edits; final file unchanged). 
- Result label now: proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted.
