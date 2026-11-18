# R3 council review — seat `opus` — W3-READER (diff-only confirmation)

**Manifest.** `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-READER Theory_work/Wave3/W3-READER/reviews/MANIFEST_R3.txt`
prints `verify: OK MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263`.

**Diff integrity.** I regenerated `git diff ae8acc8e 68443dcc` on the ticket folder (reviews/ and LOG.md excluded). It equals
`reviews/R3_diff_R2_to_R3.diff` line for line, apart from `index` lines. `git diff --stat 68443dcc HEAD` on the same paths is
empty, so the bound tree is the reviewed diff. Seven files change: CLAIMS_CARD, DEPS.tsv, METHOD_INTUITION, READER_VERSIONS,
REPORT, STATEMENT and lemmas/R4. Every hunk maps to one of the 14 tagged items or to bookkeeping (update-log lines, card
v1.12 header, DEPS.tsv). I found no change outside them.

## Per-item decisions

| tag | decision | note |
|---|---|---|
| R2-O1 / R2-E2(sol) part 1 | ACCEPT | `CLAIMS_CARD.md:73`: the leading "Given the frozen calibration," is removed. One conditioning remains, the same one as PoolZ / N1. The rest of the row is unchanged. |
| R2-O2 | ACCEPT | `READER_VERSIONS.md:148`: "$s_0\le K-1$ suffices, by Corollary B with $c(p,s_0)\ge1$ or by Prop. LB". Checked against `W3-PSHARP/STATEMENT.md:93-96`: Corollary B holds for every design ($p\ge2$), every data set and $0\le s_0\le K-1$, with $\pi(S_0)\le\sqrt n/(\sqrt n+c(p,s_0))$ and $c(p,s_0)\ge1$ for $s_0\ge1$. Theorem 1 (A2) has $s_0\ge1$ (`:102`), so the miss is $\ge 1/(\sqrt n+1)$, surely. `W3-PSHARP:B@1.0.0` is "PROVED-CHECKED" (claims.tsv:410). The domain is correct and the pointer no longer relies only on the unchecked Prop. LB. |
| R2-O3 | ACCEPT | `METHOD_INTUITION.md:71-72`: "at least $1-n^{-c}$" (both places) matches Theorem 5 (`READER_VERSIONS.md:590, 604`). |
| R2-O4 | ACCEPT | `READER_VERSIONS.md:833`: I re-derived the example. With $\theta^{*2}_{\min}\ge C_Q\sigma_*^2(\lvert Q\rvert+\log n)/(n\varphi_0^2)$, the left side of (BM-Q♭) is $\ge(1-\tfrac1n)C_Q(\lvert Q\rvert+\log n)$. The right side is $\le32\lvert Q\rvert+(64A+c)\log n+32+64\log2$, because $p\le n^A$ (S2). With $C_Q>\max\{32,64A+c\}$ the inequality holds for large $n$. (BM-Q♭) ⇒ (BM-W⁺) is `W3-RM2-R/STATEMENT.md:107-112`. The text says "e.g.", so it gives one sufficient choice and claims no threshold. |
| R2-O5 | ACCEPT | `STATEMENT.md:43` now reads "Thms 1, 2, 3, 4, 6, 10", the same as `REPORT.md:19`. R4 uses B2.1 and B6.1 (`lemmas/R4_printed_outputs.md:34, 37`). |
| R2-O6 | ACCEPT | `READER_VERSIONS.md:704-706`: the `W3-RM2:Ex-PolyR@1.0.3` status is quoted verbatim from claims.tsv:463 up to "Lemma-IR;" and then truncated with "…". The version matches. The example stays under "never hypotheses". |
| R2-O7 | ACCEPT | `lemmas/R4_printed_outputs.md:49`: the citation is now `W3-RM2-R:DLV-0`, and F-UNI Step 2 is kept as history. DLV-0 (`W3-RM2-R/STATEMENT.md:144-148`) gives `estimates_available = TRUE` "for every valid non-degenerate input, every seed and every realisation", with the 𝔇 variant. That implies completion with probability one. The remark is still not used. See E2. |
| R2-O8 | ACCEPT | `METHOD_INTUITION.md:81`: the scope is now the same as card row 3.5 and the intuition table at `:128`. |
| R2-O9 | ACCEPT | `REPORT.md:13`: the annotation agrees with `W3-SAMP/STATEMENT.md:33, 51` (potential, uninterrupted records) and with card row 3.5. The identity is unchanged. |
| R2-O10 | ACCEPT | `CLAIMS_CARD.md:7`: I hashed the `v1.8 = ` line across the card's history. The restored line is byte-identical to the original (sha1 `bb8582ea…`, as at 54785728 and the three commits before it). The R1-F6 correction stays in v1.11 (`:4`) and in row 3.1. |
| R2-E1(sol) | ACCEPT | Card row 3.1 (`CLAIMS_CARD.md:69`)'s last column now reads "NEW bridge R2; delivery identity B6.6′; R3 historical". No "bridges R2, R3" remains outside reviews/. B7.2 and B7.3 (`READER_VERSIONS.md:887-888`) keep the W-χ / W-loc width implications as current. The BM-∞ / BM-Q commentary is labelled "historical, under the former hypotheses", with pointers to B7.2′ and B7.3′, which exist at `:883-884`. |
| R2-E2(sol) part 2 | ACCEPT | `READER_VERSIONS.md:1350`: $\rho_n=n^{-1/2}e^{C\sqrt{\log n}}$ (`:1298`), so $\rho_n/\sqrt{\log n/n}=e^{C\sqrt{\log n}}/\sqrt{\log n}$, exactly. See E1 for the comma splice. |
| R2-L1 (lead) | ACCEPT | `READER_VERSIONS.md:1348-1349`: the scope is the same as card row 3.6 after R1-F5: row 3.5 needs no design condition, and row 3.1 covers only AR or block designs that meet Theorem 6's conditions. Nothing is claimed for printed PIPs or $\hat Z$ outside (A5). |
| GUARD-W (Thm 7, card row 3.2) | ACCEPT | `READER_VERSIONS.md:846` and `CLAIMS_CARD.md:70` use the same sentence as rows 3.1, 3.5 and 3.6 and Theorem 6 (R2-reviewed). Code fidelity: `Scripts/SMC_BVS/core/README.md:19` ("Stops return `resource_limit` … final estimates unavailable"); `v3_run.R:143-144` (`estimates_available <- FALSE`, `hpm_incomplete`); `cpp/v3_core.cpp:451, 459, 480, 637, 678`; `v3_calib.R:81, 113, 157`. The parenthetical "as in Theorem 6" points to `:696`, which gives the incomplete-HPM detail. EQUAL: no guarantee changes. |
| bookkeeping | ACCEPT | Update-log lines (`READER_VERSIONS.md:253, 807, 922, 1378`) and card v1.12 header. The DEPS.tsv shas changed only for R4, thm1, thm6, thm7, thm10 and CARD, which are the files and sections touched. I recomputed R4 (`7dfd819c977f3b84`) and CARD (`0552cb7b58f43ff3`) and both match. The checked_by column moves to R3 (pending). STATEMENT.md changed only in the bridge table, outside §Claim PoolZ, so the PoolZ sha is correctly unchanged. |

## Findings

No C, S or F findings.

### Editorial (E) — not counted in the score
- **E1** `READER_VERSIONS.md:1349-1350`: "The rate $\rho_n$ is the start law's rate, its ratio to …" is a comma splice.
  Write "The rate $\rho_n$ is the start law's rate; its ratio to the posterior rate $\sqrt{\log n/n}$ is
  $e^{C\sqrt{\log n}}/\sqrt{\log n}$ [R2-E2]."
- **E2** `lemmas/R4_printed_outputs.md:49`: the parenthesis cites DLV-0 without its registry condition. Add
  "conditional on C-DLV:L2-S3, C-DLV:P1-Inventory", as card rows 3.1 and 3.2 do:
  "(`W3-RM2-R:DLV-0`, deterministic delivery at the pinned code, conditional on the two code-reading audits
  C-DLV:L2-S3, C-DLV:P1-Inventory; history: F-UNI Step 2)". The remark is not used, so nothing depends on it.

## Interpretive sentences in changed text (D71)

| location | sentence | verdict |
|---|---|---|
| RV:148 | posterior miss at least of order $n^{-1/2}$ for $s_0\le K-1$ | SUPPORTED (Corollary B, PROVED-CHECKED; sure bound) |
| MI:71-72 | $\pi_0$ mass at least $1-n^{-c}$ w.p.→1 | SUPPORTED (Theorem 5) |
| MI:81 | unbiasedness of the uninterrupted final run's estimate, given the calibration | SUPPORTED (N1, PoolZ, row 3.5) |
| RV:833 | $C_Q>\max\{32,64A+c\}$ suffices (large $n$) | SUPPORTED (re-derived above) |
| RV:1348-1350 | AR/block scope pointer; exact rate ratio | SUPPORTED (rows 3.1, 3.5, 3.6; arithmetic) |
| RV:846, Card:70 | guarantees as if uninterrupted; guard stop gives `resource_limit` and no output | SUPPORTED (code facts above) |
| REPORT:13 | potential record, data fixed; equals printed field on completed runs | SUPPORTED (SAMP:PC, `:33, :51`) |
| R4:49 | completion with probability one under (S4), via DLV-0 | SUPPORTED (DLV-0 is deterministic, so this is stronger than "almost surely"; condition: see E2) |

## Gates (judged on the diff)

| gate | result | note |
|---|---|---|
| G1 correctness | PASS | All 14 items checked; the R2-O2, R2-O4 and R2-E2 arithmetic re-derived. |
| G2 hypotheses used = stated | PASS | No hypothesis added or removed. R2-O4 is an "e.g." sufficient choice inside the stated (A5)(b). |
| G3 faithfulness to masters | PASS | No item claims more than its master. Each item does what its tag says and nothing else. |
| D71 | PASS | See the table above. |
| G4 statuses verbatim | PASS | `W3-RM2:Ex-PolyR@1.0.3` matches claims.tsv:463. No other status text changed. |
| G5 no hidden finite-n / scope claims | PASS | R2-O4 is stated "for large $n$" through the (BM-Q♭) route. R2-L1 narrows to particular designs. |
| G6 code fidelity | PASS | GUARD-W `resource_limit` and estimates-unavailable facts checked in README:19, v3_run.R:143-144 and v3_core.cpp. |

**Score: 9.4 / 10.0** (C, S, F only; none found). The diff is the corrected text R2 asked for and changes no guarantee.
Only the two editorial items E1 and E2 remain.

COUNCIL-VERDICT round=R3 manifest=7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263 seat=opus score=9.4 gates=PASS
