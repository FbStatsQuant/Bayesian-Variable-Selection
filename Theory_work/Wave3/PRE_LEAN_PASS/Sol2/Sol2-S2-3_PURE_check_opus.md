PURE check of `Sol2/Sol2-S2-2_correction.patch` and `Sol2/Sol2-S2-3_correction.patch` (both patch CLAIMS_CARD.md; one fresh Opus subagent run covered both, with a separate verdict line for each; claudeAgent_personal, high; scratch in `.rc_tmp/pure_s2_2_s2_3/`). Verbatim report (harness indent removed):

PURE-VERDICT-S2-2: PURE
PURE-VERDICT-S2-3: PURE

- **Apply check.** `git apply --check` passes for each patch on the tracked file (blob 2d21cda7, which matches both patches' index line). On scratch copies under `.rc_tmp/pure_s2_2_s2_3/{A,B,AB}`, A alone, B alone, and A then B together all apply. A reverse check of both patches on the combined copy also passes. The file stays at 181 lines in every case, and the tracked file is unmodified.
- **Character diff, A.** The only change is the insertion of `, on calibration success,` after "has" on line 97. Nothing else in the file changes.
- **Character diff, B.** The only changes are on line 166: "C/E/A0/A1/D (@1.0.6: C" becomes "C/E/A0/A1 (@1.0.6) and D (@1.1.6) (C". Nothing else changes.
- **Matches the card.** Both new phrases equal FABLE_CARD.md rows S2-2 and S2-3 column (c) exactly. `grep -F` finds each full new phrase once in the combined copy.
- **A is true.** STATEMENT.md:21-23 (PoolZ) states $E[\hat Z\mid\mathcal C]=Z$ "almost surely on $\mathcal A$", and the proof at :25-30 is also on $\mathcal A$. Card row 3.5 (line 76) already opens "On calibration success". The rest of row 4.1 is byte-identical, including "(equal to the printed evidence on completed runs; no unbiasedness conditional on completion)" and the `PoolZ@1.0.2` citation, and it is consistent with row 3.5.
- **B is true.** `git show 2676e71f:…/claims.tsv` gives W3-POST2:D at version 1.1.6, and A0, A1, C and E all at 1.0.6. C there is "conditional on W3-POST:Prop-LB, W2-APP:POST"; E, A1 and D are "conditional on W2-APP:POST"; A0 has no condition. This matches the bullet's parenthetical. At HEAD and origin/main, D is now 1.1.7 and C/E/A0/A1 are 1.0.7. The bullet is labelled as history, so this is fine.
- **No registry span.** No row in claims.tsv has CLAIMS_CARD.md as its file; the only W3-READER rows point to STATEMENT.md:12-39 and lemmas/R1-R4. Two other registry files, events.log and HEADLINE_CANDIDATES.md, mention CLAIMS_CARD in prose only; neither defines claim spans.

One thing to know about the check itself: running `git apply` inside `.rc_tmp`, which is under the worktree, silently applied nothing. I used `patch -p1` for the scratch applies instead.
