# PR #54 review: REJECT

**0 CRITICAL, 2 MAJOR, 1 MINOR.** Reviewer: Codex GPT-6.1 Sol, high, independent review sub-agent. Head: `33fd9dd90e7e1e6578d89b9dc66623f85e87f871`.

V-mode science invariance is reproduced. The required refusal contract is incomplete: the island command can run with an invalid finite floor, and `read_calib` ranks duplicate inherited rows as distinct models. P8 should remain closed until findings 1–2 are fixed and rechecked. The tested merge cut-off guard protects final estimates.

## Scope and sandbox

Only O6 was reviewed. The comparison base is local merge `18434f016bcc4cf5d7252a1eabd975de45fc5a2d`, with parents `af2d3f60cd784cb323200ea3d1e51c485efb9821` and `f6567dc0961c8328c80312d7ab64318039578b8f`. It was built from a detached `git merge`. Conflict resolution preserves both INTERFACES changes and relocates PR45's bulk top-store load into the split `island_run.h`. PR45's store/performance changes are excluded from the O6 diff. See [O6.diff](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/O6.diff) and [base_sha](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/base_sha).

All scratch, builds, logs, TMPDIR and P1M_TEST_ROOT are under this worktree's `.rc_tmp`. Tests run on Owls at nice 19, with at most three test threads; active test processes are restricted to three CPUs. The C++ runner was held between phases while the added p = 80 tests ran, so suites did not run concurrently and timed test bodies were not paused. No sub-agents, NOTS, pushes, GitHub comments, implementation edits, permission requests or manual cleanup commands. The stock test helpers perform their normal fixture cleanup; `--keep` preserves the golden work directory.

Inputs: [briefs/REVIEW_PR_template.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/briefs/REVIEW_PR_template.md) (including Sandbox), [DECISIONS.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/DECISIONS.md) D-29, [ENGINEERING_SPEC.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/ENGINEERING_SPEC.md) §0-v2/v3, [reviews/D29_WP4_answer.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/reviews/D29_WP4_answer.md), [reviews/PR45_recheck.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/reviews/PR45_recheck.md), [INTERFACES.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/INTERFACES.md) v0.1.15, the head's [INTERFACES.md:220](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/INTERFACES.md:220) v0.1.17 additions, and [briefs/WP7_island_ops_T5.md](/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/briefs/WP7_island_ops_T5.md) O6.

## Numbered findings

### 1. MAJOR — the island command trusts a finite calibration floor that the full reader refuses

**Where:** [src/island/island_cmd.cpp:150](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:150); the floor is passed into the run at [src/island/island_cmd.cpp:248](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/island/island_cmd.cpp:248). `read_calib_head` reads the floor from metadata without checking its rank among inherited models or its safety against the pre-island cut-off.

**Evidence:** Starting from the retained valid p = 80 calibration (τ_cal = −117.989502, exact bits `0xc05d7f5402337894`), the reviewer rewrote `tau_cal_hex` to (a) its next representable value toward zero and (b) 1,000,000, recomputing the container hashes. `wp4io::read_calib` refused both with `invalid_input`. Calling production `island::run`, the CLI handler, completed both runs. The file under floor 1,000,000 verifies its hashes, records `status = completed`, and has zero `top_v` entries. NaN and +Inf are correctly refused. See [added_tests.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/added_tests.log) and [bad_floor_info.json](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/bad_floor_info.json).

This violates the requested island-side refusal before a 1M fit. The later merge refuses the invalid calibration, after the islands have already done their work. The source of the floor is therefore insufficiently validated at the command boundary.

**Fix:** share the semantic τ_cal validation with `read_calib` before starting the island. Keep the large-p reader light: scan mapped inherited values and validate the count above/equal to τ_cal, together with model uniqueness, without expanding the stores. For a valid c-th value over c distinct exported models, the safety bound follows. Add command-level regressions for a one-ULP-wrong finite τ and a floor above the pre-island cut-off.

### 2. MAJOR — τ_cal is recomputed over rows, without checking distinct inherited models

**Where:** [src/merge/wp4_io.cpp:276](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:276) and [src/merge/wp4_io.cpp:289](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:289); the writer likewise passes a values-only list at [src/merge/wp4_io.cpp:201](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:201).

**Evidence:** The reviewer rewrote a valid calibration's 4,801 inherited rows as repetitions of one model, with matching repeated F/logm/lg0 values and a finite declared τ equal to that F (`0xc062f79598cd3298`). The file's hashes are valid. `read_calib` accepted it and returned that finite τ. There is only **one distinct model**, fewer than c = 3,201, so the required τ is −Inf, or the duplicate file must be refused. The current rank check counts all 4,801 rows. See [added_tests.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/added_tests.log) and [tmp/refusal_duplicate_inherited.bin](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/tmp/refusal_duplicate_inherited.bin).

The normal exporter emits unique models; the reader fails to establish the assumption required by its new D-29 validation. In the additional merge probe, correct floor/hash metadata with this calibration was refused by the pre-island cut-off guard and yielded no estimates. That protection passed; it does not make this reader's accepted τ valid.

**Fix:** validate one inherited entry per model before deriving or verifying τ. The existing canonical lexicographic export can be checked for strict uniqueness without constructing another large store. Reject duplicates with `invalid_input`, then calculate the c-th value over the verified distinct set. Make the writer's precondition explicit or enforce it. Add a duplicate-model calibration regression, including duplicates separated in the file.

### 3. MINOR — merge does not enforce the advertised `meta.mode = V` floor rule

**Where:** [src/merge/wp4_io.cpp:365](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:365) and [src/merge/wp4_io.cpp:494](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/merge/wp4_io.cpp:494); [include/v4/merge.h:67](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/include/v4/merge.h:67) uses only the caller's V-mode boolean.

**Evidence:** A valid floored V island was rewritten with `meta.mode = law`, preserving its V container header and recomputing all hashes. The merge completed with estimates. The standalone island reader rejects this metadata mode under a finite floor. [INTERFACES.md:527](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/INTERFACES.md:527) (v0.1.17 §7) explicitly requires `meta.mode = V`. See [added_tests.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/added_tests.log) and [tmp/refusal_island_metamode.bin](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/tmp/refusal_island_metamode.bin).

This is a malformed-file consistency gap; normal writer output agrees between header and metadata.

**Fix:** in `head_island`, check that `meta.mode` matches the container's mode, and require V metadata for a finite floor. Add a header/meta disagreement test.

## Science and floor checks

- **Builder p = 30 reproduced:** 1,697 inherited models, c = 1,201, τ_cal = −75.091292. Across three final islands the floor dropped **1,599,395 offers**; all **41 non-meta fit.bin sections** matched the no-floor control. The independent CLI on/off test also passed.
- **Reviewer p = 80:** n = 100, 80 columns built from 20 repeated predictors, seed 41 data / seed 77 run; 4,801 inherited models, c = 3,201, τ_cal = −117.989502. There are **45 distinct inherited models with F exactly equal to the floor**. The floor dropped **20,462,006 offers** over three final islands. All 41 fit sections and all 21 non-store science sections of each island matched. Every fit metadata key was compared except input hashes, build record, timings and the memory admission estimate: HPM value/provenance, log Z scalars, tail/LS0 results, certification and flags matched. The final island stores in this fixture had cut-offs above the floor and retained no exactly-at-floor entry, so the boundary replay below separately exercises admission of those ties.
- **Boundary replay:** REVIEW p=80 c=3201: 45 exact floor ties kept; 1645 drops (45 near-floor duplicate offers plus 1600 lower models); partial island top 1745 -> 145; cutoff remains -Inf; pre-cutoff equals floor; merged top 3201 entries bit-identical
- **Isolated role/value refusals:** Passed in otherwise-valid compat, law, leader, pilot and diagnostic configurations; also NaN, +Inf and missing-hash refusals.
- **Merge refusals:** missing/mismatched floor hash, non-finite floor and non-τ bits are refused. The added actual-file probe with matching floor/τ/hash but a floor above the pre-island cut-off returned `invalid_input`, `estimates_available = false`. Equality at the cut-off is admitted by the merge-rule test.
- **Checkpoint:** exact floor bytes enter the fingerprint at [src/island/island_run.h:486](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/island/island_run.h:486). The head's tests refuse a changed-floor resume and reproduce the full-run hash under a same-floor resume. Production input identity separately includes the calibration content hash.

The safety argument holds for valid inputs: the pre-island ledger already contains c distinct models with F ≥ τ_cal, and its cut-off can only rise. Dropping only F < floor cannot remove a survivor of the merged top-c store. Equality must be kept, including all candidates needed by the HPM size/lexicographic tie order.

The new branch is in `TopStore::offer`, after the NaN guard and before buffer insertion ([include/v4/island/store.h:190](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/include/v4/island/store.h:190)). Only the final V top store receives it ([src/island/island_run.h:215](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/Scripts/SMC_BVS/engine_v4/src/island/island_run.h:215)). Tally/HPM/counters/island_best see the events independently; scoring, addressed uniforms, particle transitions and RB arithmetic are unchanged. The island's other scientific sections are assembled from those tallies or particles. The only store-derived science fields are `top_*`; floor metadata, the top-dependent output hash and execution cost fields are expected metadata differences. Tail, LS0 and near ties use the identical merged store.

INTERFACES v0.1.17 supplies wording for all four PR45 re-check gaps: floor carrier/source/effective threshold and unchanged Store operations; calibration role checks on the island side; finite values and exact τ bits; and the scoped hash-reader claim. Findings 1–3 are implementation/validation gaps under that contract.

At p = 10⁶, the new c calculation uses 64-bit arithmetic (`40ull * p + 1`), as does the island capacity. The floor adds no per-model field or changed arithmetic. The scoped 14-file diff stays inside `engine_v4`, adds no hard-coded external runtime path or large asset, and passes `git diff --check`.

## Test execution

```
export TMPDIR="$PWD/.rc_tmp/tmp" P1M_TEST_ROOT="$PWD/.rc_tmp/tmp" OMP_NUM_THREADS=3
nice -n 19 bash Scripts/SMC_BVS/engine_v4/tests/run_tests.sh --full --threads 3 --keep
```

Owls; GCC 11.5.0; clean head recorded in the binary; `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`.

- **C++ suite: 176 cases, 0 failed, 0 check failures**, including full scale/memory cases, T3 bit/class-A invariance, compat/law CLI paths, core-backed fixtures, O6 floor tests and resume checks.
- **2,510,317 checks, 0 failures**, full seven-case WP4 goldens against core/.
- **WP5 driver: 28 tests OK.** Competitor harness OK on its missing-package path; glmnet, ncvreg, biglasso, L0Learn, susieR, varbvs, BAS and bigmemory are absent. Install script: **9 guard checks OK**; broader package-install routes were not exercised here.
- Reviewer p = 80 science assertions passed. The observational refusal audit deliberately records the accepted invalid inputs described in findings 1–3; its own zero assertion failures are not a claim that those contracts passed.
- Full runner log: [full_suite.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/full_suite.log). Added run and audit: [added_tests.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/added_tests.log). Boundary and isolated roles: [boundary_test.log](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/boundary_test.log). Reproducer sources: [reviewer_p80.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/reviewer_p80.cpp), [reviewer_refusals.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/reviewer_refusals.cpp), [reviewer_boundary.cpp](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/reviewer_boundary.cpp). Retained fixture/fit paths: [tmp/review80_paths.json](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-7e1aad3a-37ce904b15d20298/.rc_tmp/tmp/review80_paths.json).

**Completion:** All requested tests have finished. Verdict remains REJECT for the numbered findings.
