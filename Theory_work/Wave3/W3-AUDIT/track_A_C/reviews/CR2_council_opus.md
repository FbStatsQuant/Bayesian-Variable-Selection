# C-R2 · council diff round · seat `opus` (Claude Opus 5.5, high) · W3-AUDIT track A_C item C1

Content reviewed: `reviews/DIFF_CR1_to_CR2.patch` (every hunk), the changed files at this manifest
(`C1_AUDITS/STATEMENT.md` v2.1, `C1_AUDITS/PROOF.md` v2.2, `C1_AUDITS/CHECK.md`, `C1_AUDITS/CITECHECK.txt`),
`reviews/CR1_council_{sol,opus}.md`, `reviews/CR1_disposition.md`, `reviews/BRIEF_CR1_opus.md`, and the C-R1 inputs that
the changed text cites: FIN `s6_delivery.tex:30-48`; DLV-0 at e78a1055 (`lemmas/Q5_dlv0.md:20-30, 55-68`;
`STATEMENT.md:22-28`); `v3_fit.R:25-70, 104-118, 140-150`; `v3_calib.R:150-160`; `INVENTORY.md:28-32`; and the
headers, settings and version tables of the T2/T4/T9/T10/T14 statements.

Manifest: `verify: OK MANIFEST c27fb00ef1630f39b5ca8a38972c2c97df3fabc95d2d2741daedb4df3a3c492e`. The #EXTRA lines and
their hashes are identical to MANIFEST_CR1, so the external inputs are unchanged. `git diff 4676af6 -- Scripts/SMC_BVS/core`
is empty. **The patch is complete.** I copied `C1_AUDITS/` to a scratch directory and applied the patch in reverse. All
four files then hash exactly to MANIFEST_CR1's values (`8180a515…`, `e7cd94a9…`, `3d2d820f…`, `e4ec4113…`). So
the patch is the whole change between the two manifests.

## 1. C-R1 findings

| # | tag | verdict | resolving line(s) |
|---|---|---|---|
| F1 | F | **RESOLVED** in the claim text | `STATEMENT.md` (C1-c), lines 56-58: "excludes the LS0 time term by P̄_LS0 and the `ls0_archive` bytes by mem_n ≥ P_e + A, e = 0, 1 (FIN A4, `…s6_delivery.tex:37-44`)". `PROOF.md` §3, lines 95-97: "excluded there by FIN A4's two terms: the LS0 seconds by time_n ≥ P̄_LS0 and the `ls0_archive` bytes by mem_n ≥ P_e + A, e = 0, 1", which quotes DLV-0. One stale copy of the old wording remains in `CHECK.md:6`; it is not claim text (R2-E1 below). |
| E1 | E | **RESOLVED** | `STATEMENT.md` A-7, lines 75-78: "**Row B1′** (the tier-0 site `v3_fit.R:117`) … The escalation re-preflight … stays row B3". `PROOF.md:18, 22, 32` give the same reading. (C1-c) lists "B1, B1′ (A-7), B2, B3". |
| E2 | E | **RESOLVED** | `STATEMENT.md` A-7, line 73 ("if the bytes fit, also returns …") and 78-80 ("its LS0 seconds term cannot newly fire there (ŝ_K is cached, the seconds do not depend on the tier; PROOF §1.1)"). I re-checked this against the code. `pf_fun` (`v3_fit.R:144-148`) calls `v3_preflight` with the same `time_fun` and the same `allocation`, and `hours` is the allocation's total, not what remains. Tier 0 passed, so its bytes fit and the seconds test ran and passed. At tier 1 the test is evaluated only if the tier-1 bytes fit, and then it gives the same result. |
| E3 | E | **RESOLVED** | `STATEMENT.md` (C1-b), lines 48-50, and `PROOF.md` §2, lines 83-85. The listed contents ("`int` ranges, \|C_b\| ≤ 31, allocations, recursion") match T9's (H4) (`track_A/T9_TDP/STATEMENT.md:24-27`). The discharge is sound: IDEAL-W covers `int` and `long` ranges, MACH covers allocation, stack and recursion, T2 gives \|C_b\| ≤ 16 ≤ 31, and cap = 10⁶ is representable. |
| E4 | E | **RESOLVED** (one residual note, R2-E2) | `STATEMENT.md` new section "Inputs consumed (status as recorded)", lines 82-89. |
| E5 | E | **RESOLVED** | `CHECK.md:20-23`, recorded as a note for the L1-R / Cor-R / M_G owners, "not C1's claim". This is the right place: the claim is not extended. |
| E6 | E | **RESOLVED** | `PROOF.md:18`: `v3_preprocess.R:99-107`. CITECHECK confirms it (`sha=39b58e4bbe`, line 99 = the `is.matrix` check). |

## 2. Diff-hunk verdicts

| hunk | change | verdict |
|---|---|---|
| CHECK.md @16 | row 7 filled with the C-R1 result; row "diff round C-R2" added; E5 note | **OK.** The scores and finding counts match the two C-R1 files. The E5 note restates my C-R1 E5 faithfully (m = min(p, max(64, K)), `cpp/v3_score.h:41-52`, X5 instance, owners' question). However, the unchanged status block at `CHECK.md:3-8` is now stale (R2-E1). |
| CITECHECK.txt @14, @21, @37, @222, footer | new rows for `s6_delivery.tex:37-44` (×3), `v3_fit.R:117`, `:144-148`, `v3_calib.R:157` (reordered); `v3_preprocess.R:98-107` → `:99-107`; 225 → 229 | **OK.** These are mechanical changes. The four added rows match the four new backticked citations in STATEMENT and PROOF. The shown excerpt of `s6_delivery.tex:37` matches the file. |
| PROOF.md @1 | header v2.1 → v2.2 | OK. |
| PROOF.md @15 (table) | E6 fix; row 117 "the tier-0 site"; escalation row "B3 (its unspecified tier-1 memory estimate includes `ls0_archive`)" | **OK.** "Unspecified" is accurate: B3's registered trigger is "tier-1 memory estimate > mem (escalation blocked)" with no formula (`INVENTORY.md:31`). B1 does carry a formula (`:29`), which is why the tier-0 site needs B1′. No new claim. |
| PROOF.md @29 (§1.1) | "same site as B1 (tier 0, row B1′) or B3 (escalation), but its tier-0 trigger is new" | **OK.** It is consistent with the following sentence (at escalation only the byte term can fire) and with the code (`v3_fit.R:43-47, 65`). |
| PROOF.md @81 (§2) | (H4) discharge clause | **OK** (see E3). This is not stronger than proved: it names premises C1 already holds. |
| PROOF.md @90 (§3) | row list "B1, B1′, B2, B3"; A4's two terms; DLV-0 quote | **OK.** **The DLV-0 quotation is verbatim.** `Q5_dlv0.md` at e78a1055, line 64, reads: "A4: the LS0 preflight time 2(ℓ_n + K + 1)q(p)ŝ_K ≤ P̄_LS0 and memory P_e + A, with the strict ">"". Line 65 closes the parenthesis, and line 59 opens (E2), so lines 59-65 is the right span. **The FIN content is accurate.** `s6_delivery.tex:37` states "time_n ≥ P̄_LS0 := (ℓ_n+K+1)q(p)(τU_K+τ₀)/100" and "mem_n ≥ P_e + A (e = 0, 1)". Lines 38-44 give 2sqŝ_K ≤ P̄_LS0 ≤ time_n and the strict-">" remark. So the span 37-44 is right. The paraphrase "the LS0 seconds by time_n ≥ P̄_LS0" is correct: the code's seconds are 2·`ls0_requests`·ŝ_K = 2sqŝ_K (`v3_fit.R:44, 47`). The byte formula A in FIN equals the code's `ls0_archive` (`v3_fit.R:45`). e = 0, 1 covers both the tier-0 site and the escalation site, so it also matches the B1′/B3 split. |
| STATEMENT.md @1 | header v2 → v2.1, "Sol LOCK on v2" | OK. Version-table row v2.1 is "EQUAL (claim unchanged; attribution and wording)". I agree: no clause is strengthened or weakened. |
| STATEMENT.md @45 (C1-b) | (H4) clause | OK (E3). |
| STATEMENT.md @50 (C1-c) | row list; A4's two terms; span 59-64 → 59-65 | **OK.** The quotation and attribution are correct (see the PROOF @90 row). "excludes the LS0 time term by P̄_LS0" is shorthand for time_n ≥ P̄_LS0, and PROOF says this in full. Acceptable. |
| STATEMENT.md @67 (A-7) | rewritten: tier-0 scope, "if the bytes fit", B3 for escalation, no LS0 seconds at escalation | **OK.** Checked against `v3_fit.R:42-48, 61-66, 114-117, 144-148` and `v3_calib.R:157`. The time disjunct is reached only inside `if (sum(comp) <= mem_gb * 2^30)`, which includes `ls0_archive` (`v3_fit.R:45-47`). The OR into `exceeds` uses `isTRUE` (`:65`). The gate is `ls0_wc` (`:114`). The A-7 claim is narrower than v2's wording, and the narrowing is correct; the coverage (C1-a) is unchanged. |
| STATEMENT.md new "Inputs consumed" | statuses of T10, T2, T4, T9, T14, Prop-F, FIN A4 | **OK, with a note.** The versions agree with the files' own version tables (T2 v6, T4 v3, T9 v3, T10 v2.2 / PROOF v2.1, T14 v1). The Prop-F status matches the same words as quoted at `T10_P1S3/STATEMENT.md:38` and FIN `s6_delivery.tex:49`. FIN A4's "OK-WITH-FIXES" matches DLV-0 (`Q5_dlv0.md:25-26`, "A4 preflight addition, … OK-WITH-FIXES)"). The council scores and the "lead's label" strings point to files I am not allowed to read, so I did not verify them (R2-E2). |
| STATEMENT.md version table | row v2.1 | OK. |

There is no new error, no claim stronger than proved, and no misquote, in the FIN A4 quotation, in DLV-0's words, or elsewhere in the changed text.

## 3. New findings (this round)

**R2-E1 (E) — the CHECK.md status block still carries the F1 wording and stale data.**
`CHECK.md:6` reads "DLV-0's (E2) excludes the B1′ exit by 𝒜_n's P̄_LS0; Sol CSL1 confirmed". This is the attribution that
F1 corrected, and it now contradicts STATEMENT v2.1 (C1-c). Three other parts of the same block are stale:
- `CHECK.md:3-4` still says "council pending" (line 4);
- `CHECK.md:9` gives "Frozen text … for council C-R1: STATEMENT `e4ec41131924`, PROOF `3d2d820fb467`", but the hashes are now `ba8c56a382af` and `e15ff519b740`;
- row 6 (`CHECK.md:18`) says "225 citations", but `CITECHECK.txt` now has 229.

The diff did not touch these lines, and C-R1 never read CHECK.md (the C-R1 brief forbade it), so neither C-R1 seat
accepted this text. It is a process record, not C1's claim, so it does not block. My C-R1 F1 repair asked that the corrected
wording replace the shorthand "wherever C1 text is copied into the log or index". Repair: in `CHECK.md:6`, write
"excludes the B1′ exit by FIN A4's time_n ≥ P̄_LS0 (LS0 seconds) and mem_n ≥ P_e + A (`ls0_archive` bytes)". Update
lines 4, 9 and 18 at bind. Apply the same wording in INDEX/LOG and in `P1_CONSUMERS.md` if they copy the old
sentence (I was not allowed to read them).

**R2-E2 (E) — where the recorded statuses come from.**
"Inputs consumed (status as recorded)" (`STATEMENT.md:82-89`) does not say where the labels are recorded. The sibling
files' own headers still read "draft, not locked" (T2, T4, T9, T10) and "DRAFT, post-freeze item; not locked" (T14).
The section is honest as worded ("lead's label", "council … bound"), but a reader cannot check it from the cited
files. Optional repair: add the record (for example `INDEX.md:<line>`) for each label, and one clause saying that the files'
headers are not updated after binding.

## 4. Gates (changed content)

| gate | result | basis |
|---|---|---|
| G1 correctness of every step and code citation | PASS | The new A-7 wording, the B1′/B3 split and the escalation argument were checked against `v3_fit.R` / `v3_calib.R` at the pin. The new citations resolve (CITECHECK 229/229, and I spot-checked them). |
| G2 hypotheses used = stated | PASS | (H4) is now named and discharged (E3). No new premise. |
| G3 no hidden assumptions | PASS | The B3 reading ("unspecified estimate includes `ls0_archive`") is stated explicitly. |
| G4 imports and statuses verbatim | PASS | The FIN A4 terms and DLV-0's words are verbatim. Statuses are recorded (provenance note R2-E2). |
| G5 scope | PASS | Tier 0 and the escalation are both handled. The default configuration is unchanged. |
| G6 fidelity to the code and to the registered texts | PASS | `INVENTORY.md:29-31`, `s6_delivery.tex:37-44`, `Q5_dlv0.md:59-65` and T9 (H4) were checked. The stale record in `CHECK.md:6` is outside the claim text (R2-E1). |

## 5. Claim table

| id | decision |
|---|---|
| C1 | **ACCEPT** |

## Score
**9.4 / 10** (C, S and F findings only). There are no C, S or F findings. F1 and E1–E6 are resolved. The two new E findings are about records.

COUNCIL-VERDICT round=R2 manifest=c27fb00ef1630f39b5ca8a38972c2c97df3fabc95d2d2741daedb4df3a3c492e seat=opus score=9.4 gates=PASS
