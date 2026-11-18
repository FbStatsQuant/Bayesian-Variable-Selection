# CLC1 brief — blind line check of track-A_C item C1 (check of the audits C-DLV:P1-Inventory and C-DLV:L2-S3 at pin 4676af6)
(Claude Opus 5.5, high; fresh agent)

You are an independent line checker and have never seen this work. Read only the files below; do not open any LOG,
CHECKPOINT, INDEX, CHECK or `reviews/` file. Write no files; change no git state. Your job is to **break** this item.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT`.
- The item: `Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS/{STATEMENT,PROOF}.md`.
- The claims it checks (registered text): `Theory_work/Wave1C/C-DLV/STATEMENT.md` (around lines 20-60),
  `Theory_work/Wave1C/C-DLV/INVENTORY.md` (whole), `Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md` (whole).
- Inputs it cites (read to see what is assumed; do not review them): `Theory_work/Wave3/W3-AUDIT/track_A/T10_P1S3/{STATEMENT,PROOF}.md`,
  `.../track_A/T2_BLK/STATEMENT.md`, `.../track_A/T4_ENC/STATEMENT.md`, `.../track_A/T9_TDP/STATEMENT.md`,
  `.../track_A_X/T14_REP/STATEMENT.md`.
- The downstream consumer (Lemma DLV-0): `git -C /home/fb31/BVS-wt/W3-AUDIT show e78a1055:Theory_work/Wave3/W3-RM2-R/STATEMENT.md`
  lines 140-165 and 225-235.
- The code of record `Scripts/SMC_BVS/core/` (registry method pin 4676af6; `git diff --quiet 4676af6 HEAD --
  Scripts/SMC_BVS/core` confirms). Read the code yourself; do not trust the line quotes or the reused T10 map.

Check:
1. **Completeness (the main question):** find any site on the shipped `v3_fit` call graph (default options) at which
   `v3_fit` returns with `estimates_available = FALSE`, or which ends `v3_fit` by an R error or C++ exception, that is
   not covered by an INVENTORY row (A1–A7, B1–B3, C1–C5, D1–D2, E1–E5, X1–X8) as the item maps it. Include R-level
   calls (e.g. `match.arg`, `%||%`, option parsing, `v3_budgets`, `v3_preflight`, `v3_randomness`, `v3_calibrate`,
   `v3_run_settings`), and any status value that could reach `v3_fit` other than those listed.
2. **Unreachability:** every "unreachable"/"holds" verdict of PROOF §2 (D2, (i)–(vii), `get_holder`, `start_mode`
   throws, implicit errors), and the X7/X8 representability bound.
3. **Correctness of each citation** (says what the proof claims) and of the 1.1 table (the only places
   `estimates_available` becomes TRUE).
4. **Strength / faithfulness:** no clause claims more than is proved; (C1-c) gives DLV-0 what DLV-0 takes from the two
   audits. If you find a real failure of P1 or S.3 at the pin (a reachable exit without estimates that no row covers,
   or a wrong "unreachable"), say so first and tag it **C**.

Reply (plain markdown, as your final message): verdict `VERIFIED` / `VERIFIED WITH AMENDMENTS` / `NOT VERIFIED`, then
numbered findings tagged **C**, **S**, **F** or **E** with file:line, what fails, and the fix.
Last line: `CLC1-VERDICT: C1=<…>`.
