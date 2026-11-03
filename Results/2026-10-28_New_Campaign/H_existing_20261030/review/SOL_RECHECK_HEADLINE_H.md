FIXES INCOMPLETE

| Finding | Resolved | Note |
|---|---|---|
| 1 | No | Companion rows now have equal prominence, remain adjacent to their primary rows, and match the CSVs. Primary-rule comparisons remain explicit. However, the c=1 SuSiE-refine label still omits the expressly requested `fit selection by ELBO`; the renderer drops this supplied registry qualification at both scales. See remaining fix 1 below. |
| 2 | Yes | Flag 3 distinguishes the two CV rules, gives the correct mixed-error counts and FP ranges, and no longer claims all truth variables are retained. The headline explicitly says CV-min. The counts and ranges reproduce from the CSVs. |
| 3 | Yes | SSL-RS pooled results are separated from scenario 1: pooled strict-subset/mixed counts are 499/69 and 497/71; scenario 1 is 10/100 recovered, 90 strict subsets, FP=0 and FN=2.61/3.55. The strong-signal totals are 593/592. All match the CSV. |
| 4 | Yes | F3's all-case arithmetic and sampled support coverage are acknowledged, with additional probes framed accordingly. Both caveat summaries disclose that weak-signal MCP's K37 primary lacks saved-vector coefficient certification. The permitted G5 reports support these qualifications. |
| 5 | Yes | Unsupported literature, project-memory and causal assertions identified by the review have been removed. The audit motivation is observational; the SSL explanation is a hypothesis; the horseshoe statement has an exact PREREG R7 attribution consistent with that source. SuSiE's L statement and the ABESS lower-RSS limitation are corrected. |
| 6 | Yes | Sources now describe existing fits, approval of a future rerun, agreement still to be checked, and separate D11 retries. No completed reproduction is asserted there. |
| 7 | Yes | The statement now concerns equal exact-recovery counts only and warns that selections/error breakdowns can differ. All 168 F1-F3 capped/uncapped EBIC recovery pairs agree. F3 ebic05 at p1000, c=1 has the stated differing FP/FN summaries under K37. The individual k=40 example was not freshly checked against raw joined rows, which are outside this re-check's permitted inputs. |
| 8 | Yes | The verdict now states targeted/seeded stratification, two fixed reconciliation checks, 14/17/3 exact-count coverage, the unsampled K37 cells and the limited scoring PASS. The script's classification comment is corrected. Read-only regeneration of the sampling logic reproduces cell 32 as registered-primary F4 K37 and all five canary keys. No additional raw tie-out certification is claimed by this re-check. |
| 9 | Yes | The AI-written/G5/ABESS disclosure is immediately above the main tables. Every displayed ABESS row uses `ABESS (splicing heuristic)` and states its applicable rule, including K37 where primary. Detailed caveats remain. |
| 10 | No | Assertions now enforce the selected-column comparison, wrong-pass missingness, aggregate uniqueness and denominators; paired merges request one-to-one validation. But equality still excludes seven saved columns, expected supplementary-key coverage is not enforced, and the first CSV is written before several assertions. In-memory negative checks demonstrate two missed failures. See remaining fix 10 below. |
| 11 | Yes | The gain sentence explicitly identifies the best benchmark separately in each cell. The six weak-signal S3/S4/S6 gains are 11, 16, 20, 20, 14 and 23, matching the stated range. |

Remaining fix 1 — **should-fix**

Locations: `scripts/render_tables.py:18`, `HEADLINE_H.md:29`, and the strong-signal SuSiE-refine row in `tables/headline_tables.md`.

The c=1 CSV registry label and PREREG R4 both say `arm added after the c = 1 results were seen; fit selection by ELBO`. The displayed row stops before the ELBO clause. This is an explicit part of the original requested fix, not a new presentation preference.

**Exact fix:** retain the complete registry qualification in the renderer's c=1 refine label: `companion (R4); arm added after the c = 1 results were seen; fit selection by ELBO`. Preserve the c=0.5 registry's ELBO qualification as well, for example `companion (R4), pre-registered; fit selection by ELBO`. Regenerate `headline_tables.md` and synchronize the two corresponding rows in `HEADLINE_H.md`. Recovery counts need no change.

Remaining fix 10 — **minor**

Locations: `scripts/build_headline.py:38-55`, with the paired merge correctly hardened at line 115.

- The equality test omits `exact_all_mcse`, `exact_passing_sum`, `label`, `n_flagged`, `role`, `tp_mcse` and `tp_n`, although these columns are copied into `all_rules_recovery_long.csv`. A read-only, in-memory check changing only one pass's F1 `exact_all_mcse` to 0.123456 still passes the current aggregate assertions.
- Uniqueness and valid denominators do not establish expected key coverage. Removing the same F4_SCAD / bic_K37 / c100 / p500 / scenario 1 key from both synthetic pass frames still passes those assertions, leaving 1,455 combined rows. The later 14-row checks concern headline rules only and do not cover this supplementary rule.
- Line 44 writes `all_rules_recovery_long.csv` before the wrong-pass assertion at line 52 and uniqueness/denominator assertions at lines 54-55. A failing build can therefore publish a table before reporting failure.

**Exact fix:** compare the complete normalized benchmark frames, including all saved columns, after asserting identical schemas and per-pass unique keys. Assert equality with an explicit expected method/rule/scale/p/scenario key set for all primary and supplementary cells, not merely agreement between passes or the presence of 14 headline rows. Assert the expected wrong-pass key set as well as its all-missing values. Perform these checks, including 100/600 denominators, before the first CSV write. Retain the checks JSON and the existing one-to-one paired merge. Update the resolution's claim of full equality/coverage after implementing this.

New issue N1 — **minor: file description no longer matches the expanded tables**

Location: `HEADLINE_H.md:164`.

The Files entry describes `headline_tables.md`, `headline_recovery_long.csv` and `headline_recovery_wide.csv` collectively as “the tables above.” The expanded display has 38 rule rows / 532 numeric counts. The long CSV still has 280 primary/secondary entries and the wide CSV has 20 rows; neither includes the new SuSiE-refine or F1-F3 companion rows. The data are consistent, but the navigation now promises expanded content in files that contain only the original primary/secondary tables.

**Exact fix:** split that entry into: `headline_tables.md`: the expanded tables above, rendered from `all_rules_recovery_long.csv` by `scripts/render_tables.py`; and `headline_recovery_long.csv` / `headline_recovery_wide.csv`: the primary/secondary-rule tables used for the headline comparison. Keep the all-rules CSV as the source for companions. No CSV changes are needed.

Verification scope and evidence: this was a narrow re-check of the listed fixes and their immediate effects, using only the authorized files and read-only `py -3 -I` (Python 3.13.1). All 532 displayed recovery counts agree with `all_rules_recovery_long.csv` and the renderer's row descriptors in both markdown files; all 280 primary error-table rows agree with the corresponding all-rules fields. Current all-rules keys are unique and complete, denominators are 100/600, and pooled recovery counts equal scenario sums. The in-memory checks executed selected check/sampling logic only; no file-writing script main, fit, simulation, network call or SSH command ran. `build2.log` reports passing checks and `build2.exit` is 0; those two files do not themselves establish the resolution's historical byte-identity claim. Raw tie-out results, historical outputs and PROGRESS.md were not reopened. The binding p >> n restriction remains satisfied in the changed reporting: selection against truth only, with no Z-accuracy or PIP-error-versus-exact claim. Only this requested review report was written.

Resolved: 9 of 11 findings; findings 1 and 10 remain incomplete.
New issue: 1 minor file-description mismatch; no numerical discrepancy found in the checked tables.
Disposition: apply the exact fixes above, then re-check only those changes.
