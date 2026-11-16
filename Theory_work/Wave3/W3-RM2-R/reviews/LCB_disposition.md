# LC-B disposition (lead) — Q4 VERIFIED, Q5 VERIFIED-WITH-AMENDMENTS (3 F), Q6 VERIFIED

| # | tag | finding | disposition |
|---|---|---|---|
| Q5-1 | F | MACH exits (interrupt `v3_core.cpp:552`, `digest` `v3_run.R:73`, allocation failures) not assigned in the walk | ACCEPTED; new paragraph "MACH exits [LCB-1]" in (E7), conclusion sentence updated |
| Q5-2 | F | scorer k > K throw is `cpp/v3_score.h:230`, not `v3_core.cpp:112`; name `nth_nonmember` (`v3_engine.h:143`, S.3(v)) | ACCEPTED [LCB-2] |
| Q5-3 | F | W2-UNI L5 Step 2 is at `:27`, not `:23-24` | ACCEPTED [LCB-3] |
Q5's statement (§1) is unchanged; dependents Q4, Q6 consume only the statement, so their checks stand. Diff of the repair:
`reviews/LCB_repair_Q5.diff` (Q5 as checked: `reviews/Q5_dlv0_as_checked_LCB.md`). Re-check of the repair by a new Sol
agent: `reviews/BRIEF_RC1_sol.md` → `reviews/RC1_recheck_sol.md`.
