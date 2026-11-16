# W3-T03ACC — source pins (copied 2026-11-15 23:33 CST from worktree HEAD bcea2483)

Every file below is a byte copy. `sha256` = sha256 of the copy (verified equal to the origin blob where shown).
Worktree HEAD at copy time: `bcea24835054912626f10fa55229c7f4b9857a6a` (origin/main lineage).

## A. The proof under review (W1-T03R, branch `origin/theory/W1-T03R`, commit `7e14d6f090bef91861455f45c69017e2a5774198`)
Copied with `git show 7e14d6f:theory_campaign/W1-T03R/<file>`. Also identical to the snapshot
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/` (SNAPSHOT_MANIFEST sha256 match).

| copy | origin | sha256 |
|---|---|---|
| `sources/W1-T03R/PROOF.md` | `theory_campaign/W1-T03R/PROOF.md` @7e14d6f | 1497376391655759bb8d0479b4f344c10f3c9e1a476182cd1881ee28868e9bd4 |
| `sources/W1-T03R/REPORT.md` | same @7e14d6f | 7828c9e60c1e9f25ea74b58410a68795f647b96d2a7cdeae9cc6f15d74b08d6d |
| `sources/W1-T03R/NOTES.md` | same @7e14d6f | a833128d10f7262c2bb30ea8515b5f8e4705c4e9996a7ab7af1a713734c64b6c |
| `sources/W1-T03R/BRIEF.md` | same @7e14d6f | 2a6316ab7f745f4f70017b10ff0f4d63494afe9eecb8fd93b5c5f2b7a9240a31 |
| `sources/W1-T03R/scripts/{bm_constants,duplicate_counterexample,proof_n0,se_n200,tail_bound}.py` and `*_output.txt` | same @7e14d6f | see `sha256sum sources/W1-T03R/**` |

## B. Locked proofs it builds on (repo `Docs/`, blob unchanged between 7e14d6f and bcea248; last commit eb757378, 2026-10-28)
| copy | origin (git blob) | sha256 |
|---|---|---|
| `sources/P1/PROOF_v3.tex` = **[P1]** | `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex` (blob 37c74bec) | 626137f4bdc98a3642faaa7fa9f7779ca28e170cc42215e625141bda4db33250 |
| `sources/P1/STATEMENT.md`, `FINAL_REPORT.md`, `STATUS.md` | same folder | 3aa33d44…, 1edad810…, e43a1690… |
| `sources/P3/PROOF_v2.tex` = **[P3]** | `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` (blob a6cde5a9) | bbc0bc0a346a51477065b96e4546a82b3ec4b886e4707134a083eccface885d0 |
| `sources/P3/STATEMENT.md`, `FINAL_REPORT.md`, `STATUS.md` | same folder (STATEMENT blob 221db84d) | 67e92149…, 578a29c4…, 0f9ec594… |
| `sources/common/00_COMMON.md` | `Docs/Theory/theorems/00_COMMON.md` (blob 64371e15) | a7d05134350823efd62add9d66a8ec1e8ff78185f2efc78415a504cc819e023d |

The locked proofs' own review files (`Docs/.../review/`) are copied to `reviews/context/P1_review/` and
`reviews/context/P3_review/` (outside every manifest: they are earlier reviews and blind seats do not get them).

## C. Statement sources
| copy | origin | sha256 |
|---|---|---|
| `sources/statement/W6-FIXREV2_STATEMENTS.md` | `branch_snapshots/W6-FIXREV2/STATEMENTS.md` = `theory/W6-FIXREV2@be2d456:theory_campaign/W6-FIXREV2/STATEMENTS.md` (statement of record per NBH `ID_REGISTRY.md` TH128) | 6ea1ecb09d9652121d8c040b441d409c59f96b4650ee445544bc7c6d7a1f553b |
| `sources/statement/TLF_434-499.md` | lines 434–499 of `branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md` = `theory/MEET-THM@37b4d2b` (full file sha256 f292d3f1…); copy line k = TLF line 433+k | 1338be945117c6a31edc8c77d21dc30fe5859823c03605834a5b559b5a6e67d2 |
| `sources/statement/SoP_04_theory_767-812.tex` | lines 767–812 of `Theory_work/State_of_Project/sections/04_theory.tex` @bcea248 (TH09 card); copy line k = file line 766+k | 06917267d3ddcd57550c62671b09b5e2a5da91e068498d1082915c2d1ddf582e |
| `sources/statement/registry_theory_main_L68.tsv` | line 68 of `Theory_work/State_of_Project/registry/theory_main.tsv` @bcea248 (SOP:TH09 row) | 5c3cedf9cb496f2927ffb96d90a3a36ea356c388a24e15c10210bdc96c2c0288 |

## D. Prior verifications — pinned, NOT copied (lead context only; never given to blind seats)
| item | pin |
|---|---|
| SF: W2-VT03R `REPORT.md` | `origin/theory/W2-VT03R` @ `b9f6d9b8f6507dd1053d6b916d7a68e1f7b4aa5e` (REPORT last changed 9ba0d7ec); snapshot `branch_snapshots/W2-VT03R/REPORT.md`, sha256 c33ad5d2d9c9a20176f347ce788ad9bd6f25524296dcb9c350035df5fc7787bc |
| XF: A-REV2 `REVIEW.md` | `origin/theory/A-REV2` @ `09dc2307b3b4a133765877239d5cd2149c25cd89`; snapshot `branch_snapshots/A-REV2/REVIEW.md`, sha256 9aa3280304df9b5244cc2f47a39a7ede8ef2e44fd4a440c0454897330d437bc8 |
| A-REV5 (onset gloss check) | snapshot `branch_snapshots/A-REV5/` (theory/A-REV5@189770c) |
| Consumer restatement | `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100` @bcea248 (W3-POST Theorem 1) |
