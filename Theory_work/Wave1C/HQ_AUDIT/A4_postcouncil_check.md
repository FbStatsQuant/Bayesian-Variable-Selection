# OK-WITH-FIXES

Targeted review of `d315c1e..c32b67f` in `FINAL/sections/` and `FINAL/consistency.tex`, against engineering head `493579a`. No chapter/code edits or tests run; repository inspection used only `git show` and `git diff`.

## 1. Current-head preflight: correct; allocation is sufficient under MACH

`493579a:Scripts/SMC_BVS/core/v3_fit.R:43–65` implements exactly the stated extra checks. Put s = ℓ_n + K + 1, q = p + p²/4, W = ceil(p/64). The additional memory component is

    A = (2s + 4)(12K + 256) + 96s + 4(8W + 4K + 96) + 4096 bytes.

For each SMC tier e = 0,1, `mem_n >= P_e + A` bounds the preflight sum; memory is checked before benchmarking. The time estimate is **2sq ŝ_K**, compared with the whole `3600 * allocation$hours`, not added to another SMC time estimate. The size-K measurement is cached across the initial/escalation calls (`v3_fit.R:107–115,144–146`). The switches and the historical/current-head distinction in s6 Remark (5), s7 and s8 agree with the code. `REPORT.md:63–81,107–112` agrees; the production diff `8a27652..493579a` changes only this preflight machinery. `git diff 72785fe 493579a -- Scripts/SMC_BVS/core` is empty; the cited ef33f91 → 98fac03 → 72785fe fixes/review trail are accurate.

**Why measured time is covered:** `cpp/v3_core.cpp:124–137` returns the elapsed time of the 200-iteration timing loop divided by 200. With U_K bounding that entire timed interval's operations, MACH gives

    ŝ_K <= (τ U_K + τ₀)/200,
    2sq ŝ_K <= sq(τ U_K + τ₀)/100 = P̄_LS0
               <= time_n <= 3600 * allocation$hours.

The rejection tests use strict `>`, so equality passes. This is a bound on the guard's measured estimate, not an inference that benchmarking predicts actual LS0 runtime. Actual runtime/peak memory remain covered separately by W_G/M_G and MACH. Benchmark context construction, scoring and fixed overhead are polynomial and fit those envelopes with sufficiently large implementation constants. Consequently the new preflight adds no no-output event under the amended allocation; the existing ideal-machine delivery argument still yields P(no output) = 0, including F-GROW. No empirical timing assumption is needed beyond MACH.

**MINOR precision fix — `FINAL/sections/s6_delivery.tex:37`:** replace “U_K the operation count of the 200 timed size-K scores” with:

> “U_K(n,p_raw) a deterministic polynomial upper bound on all operations between the timing start and elapsed-time read in cpp_time_scores(ctx,K,200), including model construction, sorting and scoring; MACH bounds this measured elapsed time by τU_K+τ₀.”

The timer includes construction/sorting (`cpp/v3_core.cpp:128–136`); counting only scorer calls would not justify the displayed inequality. Insert the two-line inequality above after the allocation, and define the archive bytes explicitly as A above. Use a uniform operation bound so the declared allocation remains a function of dimensions, as claimed in the F-GROW outline.

## 2. Council statuses: supported, with a scope qualification

`FINAL/reviews/COUNCIL_BRIEF_R3.md` explicitly requires full independent mathematical checks of CAP, corrected F and F-GROW. `C3_council_sol.md` contains separate full checks and G3 PASS (9.3); `C3_council_opus.md` likewise has “The three items checked in full” and G3 PASS (8.6). Both pass all six gates. The relabelling is justified for the d315c1e forms, with original audit verdicts and inherited qualifications preserved.

**MINOR scope fix — s6 Proposition F/F-GROW status boxes and the front-matter status summary:** append:

> “The full round-3 check applies to the d315c1e statements. The current-head preflight allocation addition was made after that council and is checked separately in HQ audit A4.”

`C3_disposition.md` already states this distinction, but “the corrected form above … checked in full” otherwise appears to include the newly added allocation. This is provenance clarification, not a failed G3 or a request to repeat council.

## 3. Remaining diff: no further substantive theorem change

No changes occur in s3–s5. Apart from the explicit stronger allocation (also inherited by F-GROW), theorem conclusions are unchanged. The random-GEN parenthesis spells out the inherited independent Gaussian-noise model and removes the contradictory “every realisation … almost surely”; it does not introduce a new statistical class. The s1 HPM wording excludes post-hoc certificate evaluations consistently with the existing output convention; s7's C6 equality merely expands a_n. Other changes are implementation history, statuses and provenance. No additional hypothesis weakening or conclusion enlargement found.
