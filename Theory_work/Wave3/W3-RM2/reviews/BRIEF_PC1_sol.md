# BRIEF — post-council diff check PC1 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your whole brief. Work
only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state**
(read-only git commands are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/PC1_postcouncil_diff_sol.md`; edit nothing else. Do not start subagents. Use no
effort setting above high.

## Frozen content
`Theory_work/Wave3/W3-RM2/reviews/MANIFEST_PC1.txt`, first line `MANIFEST d2b379495d8b9408c20aad7417a723390a128e187f4d408e2e2186e4d91b5de0`. **Quote this digest line verbatim
at the top of your review.**

## Files you may read
* Current texts (in the manifest), under `Theory_work/Wave3/W3-RM2/`: `STATEMENT.md`, `REPORT.md`, `SHARPNESS.md`,
  `ASSUMPTION_MAP.md`, `lemmas/L2_width.md`, `lemmas/L3_assemblyF.md`, `numerics/RESULTS.md`;
* `Theory_work/Wave3/W3-RM2/reviews/as_reviewed_by_R1/` — the exact seven texts the council read (their sha256 are
  the corresponding rows of `reviews/MANIFEST_R1.txt`: check them);
* the two council reviews `reviews/C_R1_council_astra.md`, `reviews/C_R1_council_opus.md`, the disposition
  `reviews/C1_disposition.md`, and `reviews/MANIFEST_R1.txt`, `reviews/MANIFEST_PC1.txt`;
* `lemmas/L5_formR.md` (only to check the reworded sentences about where b < ½ is used and about Lemma P9's proof),
  `numerics/summary.csv` (only to check the counts in the new opening note of RESULTS).
Do not read any `LOG.md`, any `CHECKPOINT*.md`, or other review files.

## Task (PROTOCOL rule 15: check of a post-council change)
The council round R1 passed (both seats, all gates, no REQUIRED finding). The lead then applied nine non-required
record corrections (markers [C1-F#], [C1-A2]; listed in `C1_disposition.md`), wrote the council result into REPORT
(§1, §4 and the registry block: `correct` gate, `council` line), and left three NITs (F8, F9, F11) unapplied.
1. Run `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2 Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt`
   from the worktree root: it must report exactly the seven files above as CHANGED and nothing else. Report its
   output. Also check that every file of the manifest R1 that is not among the seven is unchanged (same command).
2. Diff each of the seven pairs (`diff --strip-trailing-cr`); list every changed hunk and classify it: (a) required
   by a council finding and applied faithfully; (b) record/editorial (including the council result); (c) a
   substantive change (to a hypothesis, claim, lemma statement, proof step, constant or code pin).
3. Check the registry block of REPORT: every `status_source: REPORT.md:<line>` must point to that claim's own row in
   REPORT §3; the `council:` line must equal the cell printed by
   `python Theory_work/Wave3/tools/manifest.py bind Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt Theory_work/Wave3/W3-RM2/reviews/C_R1_council_astra.md Theory_work/Wave3/W3-RM2/reviews/C_R1_council_opus.md`
   (run it and report); every `PASS(...)` and `PENDING(...)` names an existing file; the scores and gate verdicts
   written in REPORT §1 and §4 equal those in the two council files.
4. Check the new opening note of `numerics/RESULTS.md` against `numerics/summary.csv` (208 runs, 204 at S₀, the cell
   B4 / η = 1 / n = 1600 with 4 failures of 6).
5. One attestation: `ATTESTATION: editorial/record only — the package stands as passed by council round R1` or
   `ATTESTATION: substantive change — needs a fresh review`, with any remaining required change stated exactly.

## Output format (in your one file)
```
MANIFEST <digest>
verify / bind outputs.
Hunks: per file, classified (a)/(b)/(c).
Registry-block checks.
ATTESTATION: …
Checks performed / not checked.
```
End your reply with the attestation line and the path of your file.
