# BRIEF — diff check RC3 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your whole brief. Work
only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state**
(read-only git commands are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/RC3_diffcheck_sol.md`. Do not edit any other file. Do not start subagents. Use no
effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_LC1.txt`; its first line is
`MANIFEST 0caea883fcf38765f1ebe5b264e8300622f80f6e444a49855ad91725e06f1558`. **Quote this digest line verbatim at the top of your review.** You may run
`python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2 Theory_work/Wave3/W3-RM2/reviews/MANIFEST_LC1.txt`
from the worktree root and report its result.

## Files you may read
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` and `Theory_work/Wave3/W3-RM2/ASSUMPTION_MAP.md` (current, in the manifest);
* `Theory_work/Wave3/W3-RM2/reviews/STATEMENT_v1.3_as_reviewed_by_SC1.md` and
  `reviews/ASSUMPTION_MAP_as_reviewed_by_SC1.md` — the exact texts the statement-change review SC1 read (their
  sha256 are the corresponding rows of `reviews/MANIFEST_SC1.txt`; check them);
* `Theory_work/Wave3/W3-RM2/reviews/SC1_statement_change_sol.md` and `reviews/SC1_disposition.md`;
* `Theory_work/Wave3/W3-RM2/numerics/RESULTS.md` and `reviews/post_BT1_addendum/README.md` (sources of the numbers
  in the limits remark).
Do not read the `lemmas/` folder, any `LOG.md`, any `CHECKPOINT*.md`, or other review files.

## Task (PROTOCOL rule 15: check of a post-review change)
SC1 returned ACCEPT WITH CHANGES with four required record corrections (2 MAJOR, 2 MINOR). The lead says the
current files = the reviewed files + exactly those four corrections (in the files' typography) + one header sentence.
1. Diff both pairs of files; list **every** changed hunk.
2. For each hunk: (a) required by SC1 and applied faithfully (compare with SC1's exact text; typographic rendering
   of η, ℓ_n, S₀, 𝔴⁰_n etc. is allowed), (b) record/editorial, or (c) a substantive change (any change to a
   hypothesis, claim, bridge statement, constant or code pin).
3. Check the numbers of the new limits remark against `numerics/RESULTS.md` (B4 table, §4 addendum) and the
   addendum README.
4. Give SC1's four items a final verdict (RESOLVED / NOT RESOLVED) and one attestation:
   `ATTESTATION: editorial/record only — v1.3 stands as checked by SC1` or
   `ATTESTATION: substantive change — needs a fresh review`, with any remaining required change stated exactly.

## Output format (in your one file)
```
MANIFEST <digest>
Hunks: numbered, classified (a)/(b)/(c).
Verdicts: SC1-1 …, SC1-2 …, SC1-3 …, SC1-4 ….
ATTESTATION: …
Checks performed / not checked.
```
End your reply with the attestation line and the path of your file.
