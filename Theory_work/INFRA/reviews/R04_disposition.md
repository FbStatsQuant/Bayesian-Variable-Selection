# R04 disposition (review: R04_review_sol.md, REJECT 6.5)

All four reproduced findings and both PARTLY per-id items accepted and fixed. Regression suite: 26/26 PASS (10 R01 + 6 R02 + 5 R03 + 5 R04 scenarios).

| finding | disposition |
|---|---|
| MAJOR: a child spawned before `Job.add(parent)` escapes the job | Fixed. Scripts start with CREATE_SUSPENDED, are assigned to the Job Object, and are only then resumed (`NtResumeProcess`), so no code runs, and no child is spawned, outside the job. Verified with a script that spawns a grandchild immediately: the job held 3 processes and closed with 0 active. |
| MAJOR: confirming then reverting `P:X@X; P:X@Y` loses the independent Y binding | Fixed. Confirmation detects an existing binding of the same property to the destination (`preexisting=yes`) and only removes the source binding, without creating a duplicate. Revert restores the source binding and keeps a pre-existing destination binding, so the dependent is still invalidated by the retraction. Scenarios R04-F8 (2). |
| MAJOR: `status_at` accepts `NOT-PROVED-CHECKED` and `PROVED-CHECKEDNESS` | Fixed. Matching is whole-token: no word character or hyphen glued on either side, on top of the negation and start-of-line rules. Scenarios R04 (3). |
| MINOR: failed process enumeration returns an empty table | Fixed. An empty table or a failed `ps` raises on both platforms (fail closed). |
| W2-FAC-S5:L1 partly | L1.1–L1.2 (22–42) added to premises. |
| W1-GEN:L8 partly | STATEMENT notation 32–36 added to premises. |
