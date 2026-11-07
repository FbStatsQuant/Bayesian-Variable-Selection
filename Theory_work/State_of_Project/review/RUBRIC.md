# Review rubric — SMC-BVS "State of the Project" (approved by F.B., 2026-11-07)

Purpose of the document: the ground truth that seeds a deep agentic theory loop (agents + council). It must be as
concrete as possible and contain all relevant information the project has, so the loop can produce theoretical
results without re-deriving the past or overstating anything. Judge it for that purpose.

Inputs given to reviewers: the PDF `State_of_Project_v1.0.pdf`, its sources `sections/*.tex`, `registry/*.tsv`,
the build (`scripts/build.sh`, `scripts/check.py`, `scripts/make_tables.py`), the frozen sources in the repo
(commit 21ebc28; `NBH/` = `Theory_work/Old_Projects/New_BVS_Headquarters/`), and `review/QUESTION_BANK_questions_only.md`
(then `review/QUESTION_BANK.md` for the key, only after answering).

## 1. Hard gates (any failure caps the overall score at 5.0)

| Gate | Check (seed your random sample with the round number; report the sample) |
|---|---|
| G1 Statement fidelity | 15 formal statements (`stmt` boxes) vs their source span: only LaTeX formatting may differ. Any change of a hypothesis, quantifier, rate, constant or exponent = FAIL. |
| G2 Status fidelity | 20 status entries vs the source (verbatim; no upgrade, e.g. PROOF SKETCH shown as proved, SF shown as XF). |
| G3 Numbers reproduce | Re-run `python scripts/make_tables.py` and `bash scripts/build.sh`; every generated table matches; 10 numbers in prose match a table or a cited source. |
| G4 Nothing invented | 15 claim-bearing paragraphs: each has a resolvable source (`path:line` or `[pos N]`) that supports it. |
| G5 Method = code | 5 method steps vs `METHOD_v3.1_FINAL.md` and the frozen code; every divergence is flagged in a DIVERGENCE box. |

## 2. Scored dimensions (weights sum to 100; report each 0–10, overall = weighted mean)

| Weight | Dimension | What earns it |
|---|---|---|
| 25 | Correctness and fidelity (beyond the gates) | Hypotheses complete; regime of each result explicit (any X / T03♯ fixed design / LH / W / LH-iid / study design); asymptotic vs finite-n stated; plain readings never overreach. |
| 20 | Completeness | `checks/coverage_report.txt` ≥ 98% of in-scope IDs (all Part-A IDs + Part-B IDs cited by NBH/03 and NBH/05), each omission justified; every reversal/refutation, pending decision, headline table, ABL-CONF, N200 present. |
| 20 | Actionability for theory work | Each open target has: exact remaining gap, hypotheses, failed routes + why, dependencies, acceptance criteria ("done" = …), a first attack from the sources; a ranked frontier list. |
| 15 | Agent-readiness | Notation defined before use; stable greppable IDs; registry TSV ≡ PDF (check.py); agent brief gives rules and update protocol; an agent rarely needs to open the archive. |
| 10 | Calibration and honesty | Explicit not-proved lists; gaps stated (n = 200 vs onset, groups of 5 outside LH, polynomial p only); conflicts in UNCERTAIN boxes; novelty claims carry the literature check. |
| 10 | Clarity for a human | Plain reading per theorem; method understandable without code; dependency and regime figures/tables. |

Anchors: 9–10 an agent could start proving from the document alone; 8 usable with minor gaps; 6–7 frequent archive digging needed; ≤ 5 a gate failed or the document misleads.

## 3. Tests every reviewer runs

1. **Question bank.** Answer `review/QUESTION_BANK_questions_only.md` (30 questions) using only the document (PDF + .tex). Then compare with `review/QUESTION_BANK.md`. Report the score x/30 and each miss with the reason (document silent / wrong / ambiguous). Pass: ≥ 27/30.
2. **Next-step test.** From the document alone, propose the loop's first 3 theory tasks, each with acceptance criteria. Report every fact you had to guess or fetch from the archive — each is a completeness issue.
3. **Contradiction scan.** Sections vs each other vs the registry TSVs.

## 4. Automated checks (run before each round by the lead; reviewers may re-run)

`bash scripts/build.sh` → LaTeX builds; `check.py`: 0 errors (sources resolve and unchanged since 21ebc28; IDs resolve and are defined once; registry statuses = NBH/ID_REGISTRY.md; no dropped glyphs; no undefined references); coverage ≥ 98%.

## 5. Pass rule

Same round: both reviewers ≥ 8.0, all gates pass for both, question bank ≥ 27/30 for both, automated checks green. Cap: 5 rounds.

## 6. Reply format

```
SCORE: <0.0-10.0>
GATES: G1 <PASS|FAIL> (sample: …) | G2 … | G3 … | G4 … | G5 …
DIMENSIONS: fidelity x | completeness x | actionability x | agent-readiness x | calibration x | clarity x
QUESTION_BANK: x/30 (misses: Qnn reason; …)
ISSUES:
1. [critical|major|minor] [G#|dimension] <problem, with file:line or page> -> <concrete fix>
STRENGTHS: <one or two lines>
```
A score of 8.0 or more means you would accept this work as is.
