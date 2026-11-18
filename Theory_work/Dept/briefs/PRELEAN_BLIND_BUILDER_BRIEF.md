# Pre-Lean BLIND API batch: builder brief (HQ, 2026-11-18; owner: use the API credits well)

**Role.** You are the Sonnet builder, explicitly on claudeAgent_personal. You BUILD request packets; you submit nothing. HQ submits from the desktop, as with auditD2, auditD3 and auditD5P1. Work on branch `theory/prelean-blind` from origin/main, in folder `Theory_work/Wave3/API_AUDIT/prelean_blind/`. Never push to main, and never edit registry files.

## Format: copy the auditD3 pattern exactly
- `Theory_work/Wave3/W3-D3/API_CARD.md`, `W3-D3/api_request_build.py`, `W3-D3/reviews/API_CARD_README.md` and `W3-D3/reviews/API_build_MANIFEST.txt`.
- `Theory_work/Wave3/API_AUDIT/audit_batch.py`, and the results README and USAGE for auditD3 (`API_AUDIT/auditD3_results/`).
- Reuse the same brief: "find a genuine error or say none, with file:line evidence". Reuse the same output schema, including FINDINGS=<k>. Keep the same model, Fable 5.2. Use N = 2 independent samples per target.

## Blindness (critical)
Each request must be **self-contained**. It holds only:
- the STATEMENT;
- the **full proof files**;
- the definitions and premises the proof needs, which are notation, cited lemma statements, and the registry statuses of inputs quoted verbatim.

It **must not** contain any review, council file, disposition, CHECKPOINT, LOG, CODEX_* or FABLE_CARD, any PRE_LEAN_PASS or walks file, earlier API audit results, or ERRATA findings beyond what the statement itself carries. The point is fully independent eyes.

## Targets: 6 targets × N = 2 = 12 requests
| id | target | start from |
|---|---|---|
| PB-T1 | Thm 3(a) rate lower bound | `W3-PSHARP:B` |
| PB-T3 | Hellinger reduction (W3-DIST:H), Lemma D0, and the domination transfer (Cor 9C core) | `W3-DIST` |
| PB-T4 | Thm 1, Thm 1′, and the presented Thm 2 = W3-D3:Thm2SG (with B3w and ExSG) | CLAIMS_CARD rows 1.1 and 1.2 |
| PB-T5 | Thm 9, 9B and Cor 9C | CLAIMS_CARD row 2.1 |
| PB-T8 | Thm 7 | CLAIMS_CARD row 3.2 |
| PB-T9 | Thm 10 | CLAIMS_CARD row 3.6 |

For each, follow the master claim id from the card into `claims.tsv`, then take its statement and proof spans and its dependencies. Include the dependencies' **statements** but not their proofs, unless they are short and needed.

## Current texts and pending corrections
The pre-Lean correction batch has NOT landed yet. So build from **origin/main**, and add to each request a short **"Known pending corrections (do not re-report)"** note. List only the items for that target, and take them from `origin/theory/PRE-LEAN:Theory_work/Wave3/PRE_LEAN_PASS/CORRECTIONS.md`. Use one line per item: location, then old → new. Do not explain why they were found. Include the deferred T4 R4 as well. If the batch lands before you finish, tell the manager.

## Size
Keep each request to **≤ ~150k input tokens**, estimated as chars/3.5 plus the brief. If a target is too large, split it into sub-requests along its lemma chain, still with N = 2, and say so.

## Deliverables
- The built `requests/*.jsonl`, or the auditD3-equivalent format.
- `BUILD_MANIFEST.txt`, with each file's sha256 and source commit.
- `README.md`, with a per-request token estimate and the total.
- Commit and push. Report to the manager in ≤ 8 lines: branch head, request count, per-target token estimate, total, and anything you excluded or split.

Put scratch only under `<worktree>/.rc_tmp/`. Start no subagents.
