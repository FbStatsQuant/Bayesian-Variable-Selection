# PRE-LEAN PASS, Sol-1: PACKET for the Sol final-text confirmation (C1 code audit)

Target: the **C1 code audit**, i.e. the two registered code-reading audits `C-DLV:P1-Inventory` and `C-DLV:L2-S3` checked **at pin 4676af6**
(track A_C item C1, council C-R1 + diff round C-R2). Lean target: no (code facts). Blocks row 3.1 (DLV-0 consumes both).
Why this call: the last round (C-R2, MANIFEST c27fb00e) was an Opus-only diff round (D91); Sol saw only C-R1 (MANIFEST 221ca4e1, 9.3, no findings), not the final text.
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`). All paths repo-relative.

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`)
| id | line | version | status (verbatim) |
|---|---|---|---|
| `C-DLV:P1-Inventory` | 116 | 1.1.1 | CODE-CHECKED (second seat, code reading; holds at pin 4676af6 after amendments A-1–A-7); council R2, MANIFEST 12802ac713050c6baf2f8f5717228e0c4cc11607f1602969fa59ee5bfb162eca, sol=9.3 PASS, opus=9.4 PASS (= track A_C C1, MANIFEST_CR2 c27fb00e) |
| `C-DLV:L2-S3` | 121 | 1.0.1 | CODE-CHECKED (second seat, code reading; holds at pin 4676af6 after amendments A-1–A-7); council R2, MANIFEST 12802ac713050c6baf2f8f5717228e0c4cc11607f1602969fa59ee5bfb162eca, sol=9.3 PASS, opus=9.4 PASS (= track A_C C1, MANIFEST_CR2 c27fb00e) |

**Recorded manifest digests** (both are in the cells):
- `12802ac713050c6baf2f8f5717228e0c4cc11607f1602969fa59ee5bfb162eca` = the registry council cell (C-DLV record manifest `Theory_work/Wave1C/C-DLV/reviews/MANIFEST_C1c.txt`; `manifest.py verify` OK locally). **Bind your verdict line to this digest.**
- `c27fb00ef1630f39b5ca8a38972c2c97df3fabc95d2d2741daedb4df3a3c492e` = MANIFEST_CR2, the manifest of the audit text itself (STATEMENT v2.1, PROOF v2.2, CHECK; the Opus-only round). `manifest.py verify` of it now reports 3 differences, all in the core AFTER the pin (see "Core drift" below); the audit files themselves are unchanged.
The existing seat record `Theory_work/Wave1C/C-DLV/reviews/C1c_record_sol.md` is an HQ carrier of the C-R1 verdict, not a review of the final text. Do not rely on it.

## Spans (read these, nothing else; long files in chunks of 120 lines)
Audit text (the thing to confirm), `Theory_work/Wave3/W3-AUDIT/track_A_C/`:
1. `C1_AUDITS/STATEMENT.md:1-102` (v2.1: Lemma C1 (C1-a), (C1-b), (C1-c); amendments A-1–A-7; inputs consumed; not claimed).
2. `C1_AUDITS/PROOF.md:1-100` (v2.2: §1 row → pin-line map, §1.1–§1.3 added call-graph nodes, §2 X2 / S.3 instances, §3 DLV-0 (E2)).
3. `C1_AUDITS/CHECK.md:1-27`; `CHECKPOINT_C1_CLOSE.md`.
4. **The part Sol never saw:** `reviews/DIFF_CR1_to_CR2.patch:1-190` (whole change C-R1 → C-R2) and `reviews/CR2_council_opus.md:1-91` (the Opus diff round; it says the patch is complete).
The two registered audits, as amended:
5. `Theory_work/Wave1C/C-DLV/STATEMENT.md:52-53` (claim P1), `Theory_work/Wave1C/C-DLV/INVENTORY.md:1-93` (rows A1–A7, B1–B3, C1–C5, D1–D5, E1–E5, X1–X8, G1–G4).
6. `Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md:1-72` (Lemma S.3 (i)–(ix)).
Code of record: `Scripts/SMC_BVS/core/` **at pin 4676af6** (`v3_fit.R`, `v3_run.R`, `v3_calib.R`, `v3_exact.R`, `v3_preprocess.R`, `v3_setup.R`, `cpp/*`). The working tree is main, which differs from the pin in exactly three files (`README.md`, `v3_fit.R`, `v3_run.R`; the patch is `Theory_work/Wave3/PRE_LEAN_PASS/Sol1/CORE_DRIFT_4676af6_to_main.patch`). For those three, read the pin with `git show 4676af6:Scripts/SMC_BVS/core/<file>` (read-only); all other core files are identical to the pin. Read only the code lines the audit cites, plus whatever you need to check an exit site; do not read the whole core.

## Core drift (context; OBSERVATION only, not part of the ACCEPT/REJECT)
After the pin, commits 4b08bb88, 99aa0998, 8bd779be ("core v3.1 list-PIP, additive output only") touched the three files above. The patch adds, at the end of `v3_fit`, `v3_add_list_fields(...)` and `stop("list PIP: ...")` calls in `v3_run.R`. The audit's claim is "at pin 4676af6". Please state, as an OBSERVATION and in at most 5 lines, whether any added code is a NEW exit of `v3_fit` without estimates (error or `estimates_available = FALSE`) that the amended P1 inventory (e.g. class row X2) or S.3 would not already cover. Do not use this to REJECT the claims at the pin.

## The question (per claim)
For each of `C-DLV:P1-Inventory@1.1.1` and `C-DLV:L2-S3@1.0.1`, on the recorded final text (STATEMENT v2.1 / PROOF v2.2 / the registered files as amended): **is the claim, as amended (A-1–A-7), true at pin 4676af6 in the shipped default configuration?** Confirm or reject, with the exact line for each reason.
Check in particular what the Opus-only round changed (the patch): the wording of (C1-c) (A4's two terms: LS0 seconds by P̄_LS0 and `ls0_archive` bytes by mem_n ≥ P_e + A), the A-7 scope (row B1′ at the tier-0 site `v3_fit.R:117`; escalation re-preflight stays row B3 with no new LS0 seconds term), (C1-b), the added call-graph nodes, and the "Inputs consumed" statuses (are they quoted as recorded?). Spot-check the row → pin-line map of PROOF §1 against the pin (sample at least the rows whose trigger changed: B1, B1′, B3, E5/G2, X2 instances).
Role: final-text confirmation. Findings only; important points only. Do NOT rewrite the audit, restate what holds, or report nitpicks (typos, line-number drift inside the same statement, notation). Report only a genuine wrong claim, a missed exit site, a step that does not follow, or a recorded status quoted incorrectly.

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then one line per claim: `CLAIM C-DLV:P1-Inventory@1.1.1: ACCEPT | REJECT` and `CLAIM C-DLV:L2-S3@1.0.1: ACCEPT | REJECT`.
Then numbered points, each: id (S1-1, ...), class (FLAW / MISSED-SITE / STATUS-MISQUOTE / OBSERVATION), file:line, what and why, minimal fix, severity (blocking / local / cosmetic).
Then the "Core drift" observation (<= 5 lines).
Then, on a line of its own and exactly once, the verdict line (fill score in 0.0-10.0; gates=PASS only if both claims are ACCEPT, else FAIL):
`COUNCIL-VERDICT round=R2 manifest=12802ac713050c6baf2f8f5717228e0c4cc11607f1602969fa59ee5bfb162eca seat=sol score=<x.y> gates=<PASS|FAIL>`
Finish with `COUNT: <number of numbered points>`.
