## W3-RM2-R council R2 diff review (seat opus; claude-opus-5-5, effort high, Claude Third; new thread). Reply verbatim below (link targets shortened).

`manifest.py verify` returned `OK MANIFEST e71637e0…190b` both before and after the review. I read only what the brief allows:
- this brief and my R1 review;
- `R2_diff.txt`, covering the six changed files;
- the dependents named in the brief: `STATEMENT.md:105-113` and `:183-240`, checked against the REPORT REGISTRY and READER_DELTA, and all of `numerics/RESULTS.md`, checked against TARGET §3.

I wrote no file and ran no git-changing command.

### (1) My R1 findings

| R1 | status | why |
|---|---|---|
| **F1** (REPORT/REGISTRY conditions vs `STATEMENT.md:234`) | **RESOLVED** | **Ex-Proxy-d:** status (`REPORT.md:34`) and its registry block now carry "conditional on SOP:TH09@1.0.0" and `SOP:TH09@hyp`.<br>**TL-F-c:** now points at `STATEMENT.md:189` (the Q2 row) and Q2 §4 only. TH09 is gone from its status and `depends_on`.<br>**RM2-F-plus:** POST/MODE-F is recorded in its `notes:` with the correct pointer (`STATEMENT.md:190`, Q3 row; Q2 §6). That claim already carries `SOP:TH09@hyp`.<br>The statuses now match STATEMENT:234 ("for (C1⁺) and Ex-Proxy-d"). The `status_source` lines 32/33/34 are still correct: the table hunk keeps its line numbers. |
| **F2** (READER bridge R7.2) | **RESOLVED** | The new row is correct. It uses a fixed D > 2+4A, so d_n² ≤ (2+4A)log n + O(1) ≤ D log n for n ≥ n₀. It uses strict C_β²φ₀² > max{c_TL⁰, 8(1+√(D/2))²} and a choice c_TL⁰ < c_TL with max{c_TL, 8(1+√(D/2))²} < C_β²φ₀²(1−1/n₀). Then λ_n ≥ (1−1/n)C_β²φ₀² log n ≥ max{…}·log n for n ≥ n₀, which is exactly the last sentence of (BM-W⁺) (`STATEMENT.md:111-112`). The one gap is harmless: the choice of c_TL needs n₀ large enough, which is implicit in "for n ≥ n₀". The closing paragraph (former lines 66-68) is now consistent. |
| E1 (STATEMENT:80-81 wording) | NOT RESOLVED in text; deferred | Recorded as ERRATA E2. STATEMENT is locked and byte-identical. Acceptable for an E. |
| E2 (Q5 stale status) | NOT RESOLVED in text; deferred | ERRATA E3. |
| E3 (DLV-0 `depends_on`) | **RESOLVED** | Prop-F@proof, P1-Inventory and L2-S3 are added. The `notes:` record the FIN s6 allocation as a non-registry input and restrict Prop-F to its delivery half, matching `STATEMENT.md:219` and :230-233. |
| E4 (name the hypotheses of Lemma E4) | NOT RESOLVED in text; deferred | ERRATA E4. |
| E5 (interval identity) | NOT RESOLVED in text; deferred | ERRATA E5. |
| E6 (pointers) | **RESOLVED** (mostly) | Row pointers are now `:188` and `:189`. Sharpness evidence is now `Q1:158` and `Q2:113`; Q2 matches my suggestion. Q1 is one line before the range I gave (159-162), probably the remark heading. I did not check it, because that lemma is outside the read scope. Rows 32-33 still use the full path, not the relative form I asked for. This is cosmetic. |
| E7 ("s₀ ≤ K" in (c⁺)) | NOT RESOLVED in text; deferred | ERRATA E6. |
| E8 (TARGET wording) | **RESOLVED** | TARGET now cites v1.0 (locked). The necessity cell now says "HEURISTIC … necessity is not proved here". |
| E9 ((FL_b)/(G3a) name) | NOT RESOLVED in text; deferred | ERRATA E7. Caution on applying it: the planned text "(FL_b) = (G3a) + (FL-Q)" is not the identity I gave in R1 ("same condition", PARENT `STATEMENT.md:169`). Check it against PARENT :169 before applying. |

### (2) Does the diff break anything?

**F3 (F): TARGET §3 misreports the numerics (`TARGET.md:36-39`, compared with `numerics/RESULTS.md:171-173, 187-195`).**
- **The problem:** TARGET lists "start-mode inclusion" among the recorded events, then says "Observed: failures only for κ ≤ 4 (n = 400) and κ ≤ 2 (n = 1600)".
- **What RESULTS says:** in design G, the coded start mode misses the weak truth in every run up to κ = 16, at both n (0/10 and 0/6). At κ = 32 it is still missing in half the runs or fewer (5/10 and 5/6). The RESULTS table calls this "not reached in range" (`RESULTS.md:194-195`).
- **Scope:** the TARGET sentence holds only for truth removal at T = S₀ and the LS0 endpoint (both designs), and for inclusion in design P.
- **Why it matters:** this is the evidence row for (V♭) and the necessity reading. It hides the most informative observation for (V♭). In G, the start mode fails, yet LS0 recovers S₀ from κ = 8 (n = 400) and κ = 4 (n = 1600).
- **What it does not affect:** the conclusion "far below κ₀; constants are artefacts; nothing shows the order is necessary" still stands.
- **Fix:** "Observed: truth removal at S₀ and the LS0 endpoint fail only for κ ≤ 4 (n = 400) and κ ≤ 2 (n = 1600), in both designs. Start-mode inclusion follows the same pattern in design P, but in design G the weak truth is not in the coded start mode up to κ = 16 (5/10 and 5/6 at κ = 32), while LS0 still recovers S₀. All of these levels are far below κ₀. The constants are artefacts, and nothing here shows that the order is necessary."
- **Related:** `H5_SUMMARY.md:165-166` says "derived-text findings fixed in the diff round R2" before R2 has concluded. It should read "addressed in R2 (result pending)" until the round closes.

I found no other C, S or F finding in the changed lines:
- REPORT §4 matches my R1 verdict; I did not check the Sol entries, which are out of scope.
- The lit row is narrowed to YWJ only, consistent with H5.
- The RESULTS reading sentence agrees with the table: for κ < 8 the binding competitor is ∅ (`:108-110`).
- The ERRATA rows are records of planned fixes only.

### (3) Per-claim table

| id | decision |
|---|---|
| W3-RM2-R:RM0-plus | ACCEPT |
| W3-RM2-R:DLV-0 | ACCEPT |
| W3-RM2-R:RM2-F-plus | ACCEPT |
| W3-RM2-R:RM2-R-plus | ACCEPT |
| W3-RM2-R:SAND-F-c | ACCEPT |
| W3-RM2-R:TL-F-c | ACCEPT |
| W3-RM2-R:Ex-Proxy-d | ACCEPT |
| W3-RM2-R:Cont-plus | ACCEPT |

STATEMENT and the lemmas are byte-identical to R1, so my R1 mathematical checks carry over unchanged. The conditions are now recorded consistently (F1).

### (4) Gates on manifest R2

| gate | result | why |
|---|---|---|
| correct | PASS | No proof text changed. The new R7.2 derivation is correct. |
| strength | PASS | R7.2 now implies (BM-W⁺) as stated. |
| faithfulness | **FAIL** | F3: TARGET §3 disagrees with RESULTS on start-mode inclusion in design G. The REGISTRY and READER now match STATEMENT. |
| lit | PASS | The unverified Song–Liang and Narisetty–He comparisons are withdrawn. The YWJ verdict is fair. |
| necessity | PASS | TARGET and RESULTS both disclaim necessity. F3 does not change that reading. |
| better | PASS | Unchanged from R1. |

### Verdict

Both of my R1 F findings are resolved, and the addressed E items are resolved or recorded in ERRATA. The diff introduces one minor F, a one-sentence misreport of the numerics in TARGET §3 (F3). Under the binding rule I must therefore give `gates=FAIL`. The fix is the single sentence above.

COUNCIL-VERDICT round=R2 manifest=e71637e0a175535f82cf9a86996974e83b968caa5df9981d97bc59b69a88190b seat=opus score=9.0 gates=FAIL
