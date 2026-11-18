# PRE-LEAN PASS, Sol-3: PACKET for the Sol final-text confirmation (W3-D2 + W3-D3)

Target: the two tickets whose last real council round was **Opus-only** (diff-only, D91, Codex level 1): **W3-D2** (`Thm2X`, `Cor2X`: Theorem 2 on random Gaussian designs, with a floor) and **W3-D3** (`B3w`, `ExSG`, `Thm2SG`: the sub-Gaussian-rows Theorem 2, the presented Theorem 2 of the card). Sol saw only each ticket's round R1 (blind first read); both R1 verdicts were FAIL; everything after was Opus-only or an HQ carrier (CITATION-ONLY / FORM-ONLY re-freezes).
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`). Paths repo-relative. Two tickets, **two review sections, two verdict lines** (see "Required output format").

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`)
W3-D2 (`Theory_work/Wave3/W3-D2/`):
| id | line | version | status (verbatim) |
|---|---|---|---|
| `W3-D2:Thm2X` | 545 | 1.0.2 | PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R2, MANIFEST d408b7dc2c23f82fca1ebd927b120f8a1788e5da422d61826785b061379c5561, sol=9.2 PASS, opus=9.6 PASS |
| `W3-D2:Cor2X` | 546 | 1.0.0 | same status string as Thm2X |
Registry council cell (recorded manifest): `R2; MANIFEST f76e9decfe21a0f3a402ec61d01f663f97877fb4325777f5ad1a9f6798308522; sol=9.2 PASS(reviews/R2f5_record_sol.md); opus=9.6 PASS(reviews/R2f5_record_opus.md)`. `manifest.py verify` of `reviews/MANIFEST_R2f5.txt`: OK.
W3-D3 (`Theory_work/Wave3/W3-D3/`):
| id | line | version | status (verbatim) |
|---|---|---|---|
| `W3-D3:B3w` | 547 | 1.0.0 | PROVED-CHECKED; council R2, MANIFEST 1c14a298ee1cea87f3ffcfbdd37b34985b9adc31c4d040a1c6a7b088fe2b406d, sol=8.5 PASS, opus=9.3 PASS |
| `W3-D3:ExSG` | 548 | 1.0.0 | same status string |
| `W3-D3:Thm2SG` | 549 | 1.0.0 | same status string |
Registry council cell (recorded manifest): `R2; MANIFEST dff18ca977905816cc08b004936a617e1151f600a43938ad9e1e73b16f6ad9b4; sol=8.5 PASS(reviews/R2g4_record_sol.md); opus=9.3 PASS(reviews/R2g4_record_opus.md)`. `manifest.py verify` of `reviews/MANIFEST_R2g4.txt`: OK.
**Bind your D2 verdict line to `f76e9decfe21a0f3a402ec61d01f663f97877fb4325777f5ad1a9f6798308522` and your D3 verdict line to `dff18ca977905816cc08b004936a617e1151f600a43938ad9e1e73b16f6ad9b4`.** The `R2*_record_*` files are HQ carriers of earlier verdicts (their `COUNCIL-VERDICT` lines belong to older manifests or to the Opus seat), not reviews of the final text; do not rely on them. The `ingest.py convert` step is not applicable (these REPORTs are already registered).

## Spans (read these; long files in chunks of 120 lines)
W3-D2 final text:
1. `Theory_work/Wave3/W3-D2/STATEMENT.md:1-126` (Thm2X :29-48, Cor2X :50-58, premises :14-27, :60-64, :81-86), `PROOF.md:1-97`.
What changed since Sol's R1 read (the part Sol never saw): `reviews/D1_diff_since_R1.txt:1-279` (= the diff of the Opus-only round D1/R2), `reviews/D1_council_opus.md:1-145` (that round), `reviews/STATEMENT_v1.1_to_v1.2.diff:1-46`; Sol's own R1 read for reference: `reviews/R1_council_sol.md:1-60`, `reviews/R1_disposition.md:1-23`.
W3-D3 final text:
2. `Theory_work/Wave3/W3-D3/STATEMENT.md:1-200` (Thm2SG :41-57, B3w :59-80, ExSG :82-90, premises :23-39), `lemmas/ASSEMBLY.md:1-83`, `lemmas/B3w.md:1-134`.
What changed since Sol's R1 read: `reviews/R2_diff_since_R1.txt:1-230`, `reviews/R2_council_opus.md:1-138`, `reviews/STATEMENT_v1.0_to_v1.1.diff:1-250`, `reviews/PENDING_LEAD_EDITS.md:1-21`; Sol's own R1 read: `reviews/R1_council_sol.md:1-64`, `reviews/R1_disposition.md:1-22`.
Only as needed to judge a point in context (do not read whole files): `Theory_work/INFRA/registry/claims.tsv` rows of the consumed claims named in the statements; the masters cited in a hunk.

## The question
For each ticket, on the recorded final text:
1. **Per claim:** is the claim as stated and proved correct (including every hypothesis it uses, the constants, the events and the conditionality labels exactly as in the registry status)? ACCEPT or REJECT.
2. **Were Sol's own R1 findings fixed?** (D2 F1: numerical cutoff and reported grid maximum; D3: the R1 findings in `R1_council_sol.md`.) State FIXED / NOT-FIXED per finding, one line each.
3. **Did the Opus-only diff round introduce or leave any wrong step, scope widening, or status misquote?** Check the hunks of the `*_diff_since_R1` files and the statement diffs in context. In particular for D3: the passage that presents Thm2SG as the Theorem 2 (sub-Gaussian rows, Gaussian = the case L = 1) must not claim more than the registry status and its consumed statuses (`W3-POST:Thm-1`, `W3-DIST:B0`, `B3w`, `ExSG`); for D2: Cor2X's quoted recorded hypotheses ("α*, β* non-random") and the conditional labels.
Role: final-text confirmation. Findings only, important points only. Do NOT rewrite, restate what holds, or report nitpicks (typos, formatting, line-number drift). Report only a genuine wrong claim, a step that does not follow, an unstated hypothesis, or a status misquote.

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then two sections, each self-contained, separated by a line consisting of exactly `=====SPLIT=====`:
**Section 1: `REVIEW W3-D2`**: lines `CLAIM W3-D2:Thm2X@1.0.2: ACCEPT | REJECT` and `CLAIM W3-D2:Cor2X@1.0.0: ACCEPT | REJECT`; the R1-finding lines (FIXED / NOT-FIXED); numbered points (id S3a-1, ...; class FLAW / UNSTATED-HYPOTHESIS / STATUS-MISQUOTE / OBSERVATION; file:line; what and why; minimal fix; severity blocking / local / cosmetic); then, on a line of its own and exactly once in this section: `COUNCIL-VERDICT round=R2 manifest=f76e9decfe21a0f3a402ec61d01f663f97877fb4325777f5ad1a9f6798308522 seat=sol score=<x.y> gates=<PASS|FAIL>`; then `COUNT: <n>`.
**Section 2: `REVIEW W3-D3`**: the same, with claims `W3-D3:B3w@1.0.0`, `W3-D3:ExSG@1.0.0`, `W3-D3:Thm2SG@1.0.0`, point ids S3b-1, ..., and the verdict line `COUNCIL-VERDICT round=R2 manifest=dff18ca977905816cc08b004936a617e1151f600a43938ad9e1e73b16f6ad9b4 seat=sol score=<x.y> gates=<PASS|FAIL>`; then `COUNT: <n>`.
(score 0.0-10.0; gates=PASS only if every claim of that section is ACCEPT and every R1 finding is FIXED.) Each section contains exactly one `COUNCIL-VERDICT` line and no other line containing that keyword.
