# PRE-LEAN PASS, Sol-2: PACKET for the Sol final-text confirmation (READER R4/R5)

Target: the **W3-READER ticket as frozen after council rounds R4 and R5** (both Opus-only, diff-only, Codex level 1 / HQ D101): the five registered bridge claims `W3-READER:PoolZ`, `:R1`, `:R2`, `:R3`, `:R4`, and the reader text / card edits made after Sol's last round (R3: sol 9.5, opus 9.4, MANIFEST 7aebdf2e…).
Why this call: Sol saw R3 only. R4 (7.9, FAIL, wording / status quotes) and R5 (9.6, PASS) and the later carriers (R5r..R5r7: CITATION-ONLY re-freezes and the READER editorial round ED1-ED3) were Opus-only or HQ carriers. This is the final-text check.
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`; the READER ticket folder is identical to main). Paths repo-relative.

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`; look up each id there to confirm)
| id | line | version | status (verbatim) |
|---|---|---|---|
| `W3-READER:PoolZ` | 526 | 1.0.2 | PROVED-CHECKED; council R3, MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS |
| `W3-READER:R1` | 527 | 1.0.4 | same status string |
| `W3-READER:R2` | 528 | 1.0.2 | same status string |
| `W3-READER:R3` | 529 | 1.0.2 | same status string |
| `W3-READER:R4` | 530 | 1.0.3 | same status string |
Registry council cell of all five (the recorded manifest): `R5; MANIFEST c867c42e869bacf0458cdcef98d697bd780793a7b0bb464ca1e4e9b7e8d85567; opus=9.6 PASS(reviews/R5r7_record_opus.md); sol=9.5 PASS(reviews/R5r7_record_sol.md)`.
**Bind your verdict line to `c867c42e869bacf0458cdcef98d697bd780793a7b0bb464ca1e4e9b7e8d85567`.** The two `R5r7_record_*` files are HQ carriers of earlier verdicts, not reviews of the final text; do not rely on them.
Local manifest check: `manifest.py verify` of MANIFEST_R5r7 reports 3 differences, all in `Scripts/SMC_BVS/core/{README.md,v3_fit.R,v3_run.R}` (the v3.1 list-PIP commits after the C-DLV pin); the READER files themselves verify unchanged.

## Spans (read these; long files in chunks of 120 lines)
The claims, `Theory_work/Wave3/W3-READER/`:
1. `STATEMENT.md:1-46` (PoolZ, :12-39), `lemmas/R1_set_sizes.md:1-59`, `lemmas/R2_local_regression.md:1-43`, `lemmas/R3_delivery_assembly.md:1-63`, `lemmas/R4_printed_outputs.md:1-48` (claim paragraph :25-29).
What changed since Sol's last round (the part Sol never saw):
2. `Theory_work/Wave3/PRE_LEAN_PASS/Sol2/READER_DELTA_R3r3_to_main.diff:1-790` = `git diff fe05ccec origin/main` over the ticket folder (CLAIMS_CARD, READER_VERSIONS, REPORT, the three lemma files, READER_ED_RECORDER_ITEMS), with reviews/, LOG.md, DEPS.tsv, CHECKPOINT_4.md and tools/ excluded. fe05ccec is the recorded R3r3 text.
3. The two Opus rounds: `reviews/BRIEF_R4_opus.md:1-41` (the edit table: T14-REP, B2, AUD-S4, R3-O1/O2, REQUOTE), `reviews/R4_council_opus.md:1-111`, `reviews/R5_council_opus.md:1-84`; and `READER_ED_RECORDER_ITEMS.md:1-79`.
Only as needed to judge a hunk in context: `READER_VERSIONS.md` (1458 lines; read the hunk's neighbourhood, never the whole file), `CLAIMS_CARD.md:1-181`, the registry rows for any status quoted in a hunk, and `Scripts/SMC_BVS/core/v3_fit.R:84`, `v3_run.R:110-113, 142-146` (GUARD-W wording), at origin/main.

## The question
1. **Per claim** (`PoolZ`, `R1`, `R2`, `R3`, `R4`): on the recorded final text, is the claim as stated and proved correct, and unchanged in substance from what Sol accepted at R3 (the three lemma hunks in the delta are the only changes to claim files)? ACCEPT or REJECT.
2. **READER-TEXT** (one overall ACCEPT / REJECT): do the post-R3 edits in the delta do what their tags say and nothing else? Check in particular: (a) every version and status quoted in a hunk matches `claims.tsv` verbatim (G4); (b) the T14-REP integer-limit sentence claims no more than its master `W3-AUDIT-AX:REP@1.0.0` proves; (c) the B2 GUARD-W wording ("a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered") matches the cited code lines; (d) the AUD-S4 Song–Liang sentences make no claim beyond what the Opus brief says (they concern the other paper's limits); (e) the H5 card 17 swap in row 1.2 (Thm2SG presented as the Theorem 2) is faithful to `W3-D3:Thm2SG`'s registry status and scope; (f) no hunk smuggles in a finite-n claim, a scope widening, or a status upgrade.
Role: final-text confirmation. Findings only, important points only. Do NOT rewrite, restate what holds, or report nitpicks (typos, formatting, line-number drift). Report only a genuine wrong claim, an unfaithful reader sentence, a status misquote, or a step that does not follow.

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then one line per claim: `CLAIM W3-READER:PoolZ@1.0.2: ACCEPT | REJECT` (same for R1@1.0.4, R2@1.0.2, R3@1.0.2, R4@1.0.3) and `READER-TEXT: ACCEPT | REJECT` (with `FIDELITY: FAITHFUL | NOT-FAITHFUL` on its own line).
Then numbered points, each: id (S2-1, ...), class (FLAW / STATUS-MISQUOTE / UNFAITHFUL / OBSERVATION), file:line (or diff line), what and why, minimal fix, severity (blocking / local / cosmetic).
Then, on a line of its own and exactly once (score 0.0-10.0; gates=PASS only if every line above is ACCEPT):
`COUNCIL-VERDICT round=R5 manifest=c867c42e869bacf0458cdcef98d697bd780793a7b0bb464ca1e4e9b7e8d85567 seat=sol score=<x.y> gates=<PASS|FAIL>`
Finish with `COUNT: <number of numbered points>`.
