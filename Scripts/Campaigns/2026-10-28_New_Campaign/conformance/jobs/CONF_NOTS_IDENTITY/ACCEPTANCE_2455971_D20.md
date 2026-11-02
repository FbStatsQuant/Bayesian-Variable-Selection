# Job 2455971: local acceptance after the D20 comparator amendment (CONF-2b, 2026-10-29)

**Result: ACCEPT (exit 0).** Both units pass every criterion. cmp2 compares 175,927 paths for S3 and 221,287 for S5, with 0 differences and 0 non-allowlisted additions. These are the same path counts that Sol's in-memory replay found.

## Amendment

`cmp2.R`, in `shape_cmp`, changes only this line:

```r
if (length(x) != length(y) && path != "record$environment$command") return(cmp2_diff(e, path, "exempt value: length differs"))
```

This is Sol's minimal remedy (`conformance/review/SOL_IDENTITY_RESULT.md`), as decided in D20. The type, names and attribute checks stay, as do every other shape, addition and computed-content check and the numerical-environment criteria.

| File | sha256 |
|---|---|
| `cmp2.R` before D20 (kept byte-identical at `conformance/work/regression2/cmp2.R`) | 947f6803fe75893f5d6a6ddf7db509940cdf41b0e6132efd4694f46bb0edfa82 |
| `cmp2.R` after D20 (this folder) | f2662113babc300d102957f0d79920a97ba75383fe4ef80b38eeaabaebefa048 |

The original failing log, `ACCEPTANCE_2455971.log`, is preserved unchanged.

## Evidence (all local, on the verified downloads; no NOTS rerun)

| Check | Log | Result |
|---|---|---|
| Acceptance, `compare_identity.R` on `NOTS Data/New_Campaign/results/conf_identity/results/conf_identity` + `logs/conf_identity/run_env_2455971.txt` | `ACCEPTANCE_2455971_D20.log` | **ACCEPT**, exit 0 |
| Comparator self-test (`regression2/cmp2_selftest.R`, unchanged, sourcing the amended `cmp2.R`) | `conformance/work/d20_cmp2/cmp2_selftest_D20.txt` | 101/101 assertions pass |
| In-memory negative controls on both real units | `conformance/work/d20_cmp2/neg_controls_d20.log` | 16/16 as expected |
| Whole-pipeline dry runs | `conformance/work/d20_cmp2/dryrun_D20.log` | both rejected, exit 1 |

**What the in-memory negative controls show:**
- Still accepted: the unmodified records, and a further change to argv's length or value. That field is exempt by design.
- Still rejected:
  - argv changed from character to list;
  - argv gains an attribute;
  - argv renamed;
  - an unrelated environment vector's length changes (`$R`);
  - `fit$log_Z` changes by 1e-12;
  - a non-allowlisted addition.

**The whole-pipeline dry runs:**
1. Historical outputs posing as new, with emptied checksum manifests and an environment record that has no header, end, launch or compile lines: FAIL, 31 criteria.
   - The original control (`DRYRUN_negative_controls.log`) failed 30 criteria. It emptied only one unit's manifest; this run empties both, which accounts for the one extra failure.
2. The real outputs with a conflicting second `final_status`: FAIL, 1 criterion (the job record).

Scripts: `conformance/work/d20_cmp2/neg_controls_d20.R` and `selftest_amended.R`. The dry-run fixtures were built in a scratch folder and then removed.
