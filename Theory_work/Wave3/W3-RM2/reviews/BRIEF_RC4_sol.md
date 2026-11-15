# BRIEF — diff check RC4 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your whole brief. Work
only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state**
(read-only git commands are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/RC4_diffcheck_sol.md`. Do not edit any other file. Do not start subagents. Use no
effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_RC4.txt`; its first line is
`MANIFEST b9c2675af243ac0945b09a015de87d0e4cdf42d790965312e49e84d5569dcec8`. **Quote this digest line verbatim at the top of your review.** You may run
`python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2 Theory_work/Wave3/W3-RM2/reviews/MANIFEST_RC4.txt`
from the worktree root and report its result.

## Files you may read
* Current texts (in the manifest), under `Theory_work/Wave3/W3-RM2/`: `ASSUMPTION_MAP.md`, `PLAN.md`,
  `lemmas/L0_toolkit_b.md`, `lemmas/L1_sandF_b.md`, `lemmas/L2_width.md`, `lemmas/L3_assemblyF.md`;
* `Theory_work/Wave3/W3-RM2/reviews/as_reviewed_by_MP1/` — the exact six texts the independent mid-point review MP1
  read (their sha256 are the corresponding rows of `reviews/MANIFEST_MP1.txt`: check them);
* `Theory_work/Wave3/W3-RM2/reviews/MP1_midpoint_astra.md` and `reviews/MP1_disposition.md`;
* `Theory_work/Wave3/W3-RM2/reviews/LC1A_L0L1_check_sol.md`, `reviews/LC1B_L2L3_check_sol.md` — only to check the
  verdict words quoted in the new status headers of L0–L3;
* `Theory_work/Wave3/W3-RM2/numerics/RESULTS.md` (source of the numbers in ASSUMPTION_MAP: B-tables and the §4
  addendum) and `Theory_work/Wave3/W3-RM2/STATEMENT.md` (only where a changed sentence refers to it).
Do not read any `LOG.md`, any `CHECKPOINT*.md`, or other review files.

## Task (PROTOCOL rule 15: check of a post-review change)
MP1 returned CONTINUE WITH CHANGES with three MINOR findings on supporting records and one NIT on a proof sentence.
The lead says: current files = the reviewed files + exactly those four corrections (markers [MP1-1]…[MP1-4]) + the
record-only hunks listed in `MP1_disposition.md` (v1.3 name of the signal floor in one table row; review-status
headers in L0–L3; nothing else).
1. Diff each of the six pairs (`diff` of the two files; the files use different line-ending conventions in places —
   compare content, e.g. `diff --strip-trailing-cr`); list **every** changed hunk.
2. For each hunk: (a) required by MP1 and applied faithfully (compare with MP1's exact correction; typographic
   rendering of η, β, 𝔴⁰_n, S₀ etc. is allowed), (b) record/editorial, or (c) a substantive change (any change to a
   hypothesis, claim, lemma statement, proof step, constant or code pin). For the hunk in `L3_assemblyF.md` marked
   [MP1-4]: it rewords one proof sentence; decide whether the new sentence is a correct proof of the same step from
   the same input (convergence in probability of a [0, 1]-valued variable ⇒ convergence of its mean) and uses no
   stronger input.
3. Check every number in the changed ASSUMPTION_MAP hunks against `numerics/RESULTS.md` (run counts 208 / 204; the
   B4, η = 1, n = 1600 cell: failures 4 of 6, swaps 19, 24, 35, 73, the range of outside columns in the start mode;
   completed sizes; B1/B2/B3 counts if touched).
4. Check that the status headers of L0–L3 quote the lemma-check and mid-point verdicts accurately and still say
   "PROVED (by this seat, unchecked)" (no upgraded status label).
5. Give MP1's four items a final verdict each (RESOLVED / NOT RESOLVED) and one attestation:
   `ATTESTATION: editorial/record only — L0–L3 stand as reviewed by MP1` or
   `ATTESTATION: substantive change — needs a fresh review`, with any remaining required change stated exactly.

## Output format (in your one file)
```
MANIFEST <digest>
Hunks: numbered, per file, classified (a)/(b)/(c).
Verdicts: MP1-1 …, MP1-2 …, MP1-3 …, MP1-4 ….
ATTESTATION: …
Checks performed / not checked.
```
End your reply with the attestation line and the path of your file.
