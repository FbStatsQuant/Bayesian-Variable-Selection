VERDICT: BIT-IDENTITY CLAIM NOT ESTABLISHED — no numerical output mismatch was found, but the comparison gate accepts invalid evidence and the claimed unreachable floating-point branch is reachable.

1. **MAJOR — comparison is not fail-closed.** `Theory_work/Wave3/W3-SCALE/scripts/bitid_compare.R:8,15,16,27,39`.
   Three independent scratch reproductions printed `COMPARE PASSED` and exited 0 (including expected count = 1):
   - Start with one otherwise valid paired record and set both `fingerprint <- NULL`. `identical(NULL, NULL)` accepts both the version and whole-fit hash; the result is `IDENTICAL`, `n_fields = 0`.
   - Keep equal valid fingerprints but change B's `fingerprint$delivery$preflight$exceeds` from FALSE to TRUE. Output says `admission decisions equal 0`, yet passes. The equal-admission precondition is only reported, not enforced.
   - Add `unpaired__v32.rec.rds` beside a valid pair. Only A's filenames are enumerated; the extra B record is invisible even with the expected count supplied.
   Fix: require version 2 explicitly, a nonmissing scalar SHA-256 and valid top/delivery schemas; compare both unit inventories and record unit identities; reject or separately classify unequal admission before declaring a successful identity comparison. Expected count alone is insufficient.

2. **MAJOR — the unrestricted raw NaN guarantee relies on an invalid sort comparator.** `Scripts/SMC_BVS/core_v32dev/cpp/v3_blocks.h:178,180,220`; `README.md:70` (raw-export guarantee).
   This is inherited from v3.1, not an observed new mismatch. With NaN correlations, the fallback comparator is not a strict weak ordering: NaN compares equivalent to two distinct numeric correlations that compare unequal to each other. `std::stable_sort` therefore has no defined-result guarantee for that input. Calling an unchanged inline routine does not establish universal bit identity across separately optimized binaries on an undefined-behavior domain. All tested raw cases matched, including late NaNs; that is narrower evidence than the stated guarantee.
   Fix: qualify the raw guarantee to defined inputs/empirically checked cases, or define a NaN ordering through a separately reviewed compatibility decision. Add mixed finite/NaN correlation cases with explicit fallback/ordering assertions; all-NaN payload matrices alone do not exercise the comparator violation above.

3. **MINOR — “A fails after H passes” is reachable under the pinned floating-point flags.** `Scripts/SMC_BVS/core_v32dev/README.md:104`; `cpp/v3_start.h:164`.
   Finite reproducer: n=4, p=2, both columns equal to
   ```cpp
   {0x1.680d09f9e187p+24, 0x1.b18d40112a9edp+25,
    0x1.598da0c86678ap+25, -0x1.19b4edbf0903p+26}
   ```
   Every Gram entry is `0x1.40e843981b6e4p+53`. `chol_inplace(5*G + I, 2)` returns true; `chol_inplace(G + I, 2)` returns false. Direct DFS calls give `append_row(0,0)=true`, then `append_row(1,1)=false`. Exact positive-definite ordering does not constrain independently rounded Cholesky pivots in this way.
   With y={1,2,3,4}, both complete table builds still match: routes 3/0/1, no failures or Q recomputations. This disproves the coverage rationale, not output identity. Fix the wording and add this case with an assertion specifically for the A-pivot failure (aggregate QR counts cannot establish it).

4. **MINOR — mutation counts overstate field coverage; some mutations do nothing.** `Theory_work/Wave3/W3-SCALE/scripts/fingerprint_selftest.R:21,23,24,33`.
   `log_Z * (1 + eps)` leaves zero and infinities unchanged; demonstrated zero yielding `FAIL (not detected): log_Z_one_ulp` although the fingerprint correctly saw no mutation. Missing semantic fields frequently mutate `seed` instead, and timing loops over absent fields perform no mutation. Thus 14/14 and 6/6 on early-return fits do not mean all named fields were exercised. No arguments also yields a vacuous pass.
   Fix: require input fits; assert that each mutated field actually changed; report inapplicable fields as skipped; flip an explicit finite-double bit or use a guaranteed distinct value. Keep separate coverage totals for each real target field.

Numerical attacks and code reasoning

- Gram: each lane starts at +0 and accumulates observations in increasing i, with separate multiplication/addition. `memcpy` avoids alignment/aliasing assumptions; no lane reduction occurs. The scalar tail uses the original expression. The selected triangle uses the same `(xa,xb)` indices, and mirroring copies the original single sum into both locations. Under these flags there is no reassociation or FMA permission. Signed zeros, subnormal products, and overflow-generated Inf/NaN did not break it. Non-finite X takes the original loop before tiling.
- Neighbours: for numeric absolute correlations, including Inf, index tie-breaking makes the order total; partial-sort prefixes and the one-pass threshold count match the original. A late NaN discards all local chosen lists and recomputes from scratch without changing Data counters. A NaN confined to a diagonal correlation is unused by the ranking. Linkage checks all distances, including diagonals, before the original two-step replay.
- DFS: row entries, diagonal subtraction order, forward substitution, log-diagonal sums and quadratic sums reproduce the original prefix operations. Small-Q cases use the original scorer. Failure replay restores all five counters, clears the block and executes numeric code order, reproducing partial tables and the first exception. Non-finite y/z attacks did not break this path.
- Fingerprint v2 preserved the inspected non-timing fit fields and list attributes; no hidden real fit difference or pure-timing false positive was found in the four actual fit pairs. Name-based stripping is still schema-dependent. The demonstrated false passes are in evidence validation, not a discovered hash collision.
- Original suites do not explicitly assert the A-pivot branch, n=1..3, signed-zero inputs, non-finite y/z with finite X, an Inf-only off-diagonal ranking, or a diagonal-only NaN correlation. The first four were attacked here; remaining special Gram cases were inspected but not separately instrumented. Branch flags only enforce their listed aggregate route conditions.

Execution evidence

Reviewed branch `theory/W3-SCALE`, HEAD `f2ed8ac1d47f789d4744fa2066cf143bf58b503f`. Both core trees have no changes between bbdfea0 and HEAD. No prior review file was opened. Only this report was written in the checkout; builds, core copies, caches and records stayed under the temporary directory.

Toolchain: Rtools GCC 14.3.0, its bin directory first on PATH; `-std=gnu++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`. Windows R 4.6.1. No Linux/cluster execution.

- Supplied `bitid_units.cpp`, both cores, `big`: 49 cases, both exit 0, reference mismatches 0, required branches not reached 0; FNV `c176cf6dc605895f`; identical dump SHA-256 `2451EEBF8D6FBE4BAEAB7D94B92154034C49E623A7A53D1CB5E14324A2CF2D70`.
- Private harness: 116 cases covering n={1,2,3,4,9}, p={1,2,15,16,17,63,64,65,255,256,257}, integer designs, signed zeros/subnormals, late zero/NaN/Inf columns, finite overflow/cancellation, NaN/Inf y. Both exit 0; reference mismatches 0; identical dump SHA-256 `8D0E007049957D884F072311A8973BF66AC9BBF1F355E65B0936A084CCDAC3B9`.
- Pivot counterexample full tables/start: identical SHA-256 `8469256CE4837C18C7F8CF5EDE3785369A0ACA58983BFD3E92BF6E5167A78797`. Additional 20,000 finite extreme-value Gram cases, p=17, n=1..6: zero byte mismatches against gram_fill_v31.
- `export_units.R` on scratch copies of both cores, then `--compare`: `EXPORTS IDENTICAL (11 cases)`; both runs exit 0.
- `bitid_fit.R`: exact_p10, smc_p40_dup, y_constant, no_predictors. Exact/completed/early-return statuses as expected; all four fingerprints identical and admissions equal. Completed SMC: tier 0, 15 stages, numerical counters `7555639/0/0/0/0` in both.
- `fingerprint_selftest.R` on all four v32 fits: each 14/14 mutations detected, 6/6 timing-invariant; `SELFTEST PASSED`, subject to finding 4. Separate zero-logZ synthetic probe confirmed the ineffective mutation; that synthetic probe subsequently errored on an empty named-list subfingerprint, so it was not counted as a passing fit test.
- `refingerprint.R` on all eight scratch fits: `REFINGERPRINTED 8`; subsequent four-pair comparison still passed.
- Three malformed/incomplete comparison probes in finding 1: all exit 0. Ordinary fit comparisons were separately checked to contain actual valid hashes and expected statuses.

Scratch evidence: `C:/Users/felip/AppData/Local/Temp/w3-r02-bb61e0ab6e39445a98228be14eaba7fa` (sources, binaries, dumps, logs, R records and comparison probes).
