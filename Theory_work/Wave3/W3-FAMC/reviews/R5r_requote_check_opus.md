# W3-FAMC STATEMENT §4 requote check (Opus one-shot, recorder-requested; NOT a council seat)

Reviewer: Claude Opus 5.5 (one-shot subagent, read-only), task RM2FAMC, 2026-11-17, two rounds on the same agent. Subject: STATEMENT.md §4 (heading line 162, the table rows of W3-RM2:Ex-PolyR, W2-LOC2:Lemma-BC and Lemma-IR, and one Consequence sentence)
and the DEPS.tsv S:inputs row, after the three rows were upgraded to PROVED-CHECKED in the same landing (the ticket's citecheck.py needs the current registry statuses and pins verbatim). Round 1 found two stale phrases (the heading's
"main a779c1df" and the second column "condition of Ex-PolyR"), which the recorder fixed. Final verdict, quoted verbatim:

REQUOTE-VERDICT: PURE
- (1) All three §4 quotes match claims.tsv exactly. The pins match the registry: Ex-PolyR@1.0.5, BC@1.0.1, IR@1.0.1.
- (2) Both files are 209 lines. Only lines 162, 178-180 and 190 differ; lines 1-161 (claim span 49-81 and premises 25-32), 163-177, 181-189 and 191-209 are identical.
- (3) DEPS.tsv: only the S:inputs row changed. The sha of lines 162-190 recomputes to d5a650600f7994c8, which matches.
- Anything else changed: no. The diff touches only the heading, the three rows and the one Consequence sentence. Line 177 stays as it was.
