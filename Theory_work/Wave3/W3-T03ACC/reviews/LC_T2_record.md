# LC_T2 record — two line checks added to W3-T03ACC's LC record (HQ carrier; PROTOCOL_v4 §7; NOT a new review)

Written by the HQ recorder (HQ GO real run (task T2, 2026-11-16); HQ standing GO "If VERIFIED: an HQ carrier adding them to the LC record, then re-discharge", task T2). The two Sol line checks below (codex gpt-6.1-sol, effort high, one fresh call each, read-only) were commissioned by the Theory Department after task T's edge table kept two items outside LC-A/B/C. They are copied verbatim into this folder from `dept/theory` @ d8bcc970 (`Theory_work/Dept/research/T2_linechecks/`). They are outside the voted manifest (MANIFEST_R1 9714aea4), which is unchanged.

| item | added to the LC record | review (verbatim copy; sha256) | brief (dept/theory; sha256) | verdict |
|---|---|---|---|---|
| [P1] `lem:prior`(e) (PROOF_v3.tex:113-136), consumed by W3-DIST X and V | T2(i) | `reviews/T2i_sol.md` (93bcc83da940ddf1) | `Theory_work/Dept/research/T2_linechecks/BRIEF_T2i_sol.md`@d8bcc970 (418f2b975d6aa5fb) | "LEMMA-PRIOR(e): VERIFIED" |
| T02(ii♯) item 5(a) ([T03R] PROOF.md:149 and the reused [P1] T02(ii) steps lem:good/onG/one, thm:T02ii), consumed by W3-POST:Thm-1 item 5(a) | T2(ii) | `reviews/T2ii_sol.md` (6fbd19a171337771) | `Theory_work/Dept/research/T2_linechecks/BRIEF_T2ii_sol.md`@d8bcc970 (d15797f7ef1a0960) | "T02ii-5a: VERIFIED"; Findings C=0, S=0, F=0, E=0 |

Source files at review time (sha256, verified equal to this folder's copies now):
- P1 PROOF_v3.tex: `Theory_work/Wave3/W3-T03ACC/sources/P1/PROOF_v3.tex` 626137f4bdc98a3642faaa7fa9f7779ca28e170cc42215e625141bda4db33250
- W6-FIXREV2_STATEMENTS.md: `Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md` 6ea1ecb09d9652121d8c040b441d409c59f96b4650ee445544bc7c6d7a1f553b
- W1-T03R PROOF.md: `Theory_work/Wave3/W3-T03ACC/sources/W1-T03R/PROOF.md` 1497376391655759bb8d0479b4f344c10f3c9e1a476182cd1881ee28868e9bd4
- inputs.sha (dept/theory @d8bcc970): 195a10d6b0f4f5fe

Scope: these checks add the two items to the line-check record of W3-T03ACC (LC-A/B/C + T2). They do not upgrade the T01–T03 or T02(i♯)/(ii♯) rows themselves (card 12 condition 2): SOP:TH09-T02 and SOP:TH09-T01T03 keep their statuses; edges to the verified steps are discharged (task T edge rule, card 12 condition 1).

