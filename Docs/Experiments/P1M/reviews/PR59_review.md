# PR #59 review — WP7 τ_cal by radix select (builder 7, head 89c75320 → exp/P1M-engine)

Reviewer: Opus-class independent review, read-only. Checkout: `git checkout --detach 89c75320` in my worktree; diff base `7c2c6a75` (= merge-base with origin/exp/P1M-engine; 3 files, +49/−6, all under `engine_v4/`).

## Verdict: **ACCEPT-WITH-FIXES** — 0 CRITICAL, 1 MAJOR, 4 MINOR

The select is exact: 1.92 × 10⁶ randomized/adversarial/exhaustive cases agree with the old `nth_element` value in every case except the sign of a zero in ±0 ties (which the old code leaves unspecified), and agree bit-for-bit with a total-order oracle in all cases. Real `calib.bin` τ_cal bits are unchanged. Quick suite is 175/175 green. The one MAJOR is that the calib.bin **writer still makes the 0.64 GB F copy** this PR is meant to remove.

## Findings

### 1. MAJOR — the writer still copies F (`src/merge/wp4_io.cpp:213-214`)
```cpp
std::vector<double> F;
if (c.inherited_flat) F = c.inherited_flat->F; else for (auto& m : c.inherited) F.push_back(m.F);
tau_cal_to_meta(meta, tau_cal_of(F, c.led ? c.led->top.cap : 0));
```
Only the reader (`check_calib_tau_cal`, line 288) was converted. At p = 10⁶ (≈ 8·10⁷ inherited models) the writer makes a full 0.64 GB `std::vector<double>` copy of `inherited_flat->F` at export time, on top of the flat arrays it already holds. The PR description ("shared by the calib.bin writer and reader") and the new header comment ("no copy of the values") do not hold for the writer.
**Fix:** for the flat case call `tau_cal_of(c.inherited_flat->F.data(), c.inherited_flat->F.size(), cap)`; keep the vector only for the legacy `c.inherited` (struct-per-model) path, or build it once there. Bits are unchanged (same function).

### 2. MINOR — ±0 is ordered by the select, equal under the old comparator (`include/v4/offer_floor.h:36,50-51`)
The key map puts −0 (key 0x7FFF…F) strictly below +0 (key 0x8000…0). The old comparator `a > b` treats them as equal, so `nth_element` returned *whichever* zero ended up at index c−1 (an arbitrary, library-dependent choice). Measured: 354,501 test cases had a zero at the c-th position; in 93,067 the old and new values differ in the sign bit (equal as numbers; 0 value mismatches). So "bits exactly those of the old value" cannot hold for ±0 ties — and cannot be *defined* for the old code. The new value is deterministic (it is the c-th largest in total order), the writer and the reader use the same function, so the merge condition "island floor bits = τ_cal bits" is self-consistent for all new files.
Reachability: F = logprior + lm; under round-to-nearest an exact cancellation gives **+0**, never −0 (needs both operands −0), and an exact 0 is itself measure-zero. So I judge this practically unreachable. The only exposure is a *legacy* calib.bin (old writer) with τ = −0, which the new reader would refuse (`tau_cal is not the c-th best F`).
**Fix (cheap, makes the answer independent of any sign convention):** map −0 to +0 in `key` (`if (x == 0) x = 0.0;`) and return +0 for that tie group, and say so in the comment. Or leave as is and document that ±0 ties are by total order. Either way, add the ±0 case to the unit test with bit equality against the total-order oracle (the current test accepts any zero, `test_offer_floor.cpp` “zero” shortcut).

### 3. MINOR — "allocation-free" is not literally true: one 512 KiB heap block per call (`offer_floor.h:37`)
`std::vector<uint64_t> cnt(65536)` allocates 524,288 B on the heap on every call (measured with an overriding `operator new`: exactly one allocation of 524,288 B per call, none other). It is O(1) in n and tiny against 0.64 GB, so the memory goal is met, and it is not an n-dependent allocation before admission; but the brief asks for fixed-size histograms on the stack / preallocated, the header comment says "O(1) memory", and a `std::bad_alloc` here would escape as a non-`Status` exception before admission.
**Fix:** `static thread_local std::array<uint64_t,65536>` or a caller-supplied scratch, or 8 passes × 256 counters (stack, 2 KiB; the cost is 4 more scans of n, about +0.15 s at 8·10⁷). Not blocking.

### 4. MINOR — finiteness is a caller precondition, not enforced; writer does not check (`offer_floor.h:31-33`, `wp4_io.cpp:214`)
NaN/inf behaviour (my probe): +inf and −inf map correctly (they are ordinary keys; covered by my tests). A positive NaN keys above +inf (`tau_cal_of({1,NaN,-2},1)` returns NaN), a negative NaN below −inf — i.e. garbage but no UB (the old comparator on NaN was UB for `nth_element`). The reader is safe (`need_finite(F[i])` at `wp4_io.cpp:275` runs before the select; ±inf and NaN refused). The writer (line 214) feeds F straight in; if upstream ever produced a non-finite F the writer would write a calib.bin that the reader then refuses, rather than failing at write time. Upstream F = finite logprior + finite lm, so this is defensive only.
**Fix:** a one-line finiteness scan in the writer (or an assert in `tau_cal_of`); add a non-finite unit case.

### 5. MINOR — tests and a behaviour change worth stating
(a) The new unit test (`test_offer_floor.cpp:158-176`) is small (n ≤ 700, 60 reps × 4 c) and compares by value, not by total-order bits; adequate as a smoke test, my differential run (below) is the real evidence. It does not exercise n large enough for the four passes to see non-trivial prefixes with ≥ 2³² counts (irrelevant at 8·10⁷ since counters are uint64).
(b) The new refusal `n > 2^24` for a non-canonical inherited list (`wp4_io.cpp:283`, replacing the former 2³²−1 cap) is a deliberate contract narrowing (legacy / hand-made lists only; the exporter's list is canonical, so the scan at 277-278 passes at any size). It is untested and I found no mention in INTERFACES.md; add one sentence there and a test with a stub n (or document it as untested because of its size).

### What I checked and found correct
1. **Key map** (`offer_floor.h:36`, inverse at 51): `u>>63 ? ~u : u|0x8000…` is the standard order-preserving bijection (negatives complemented, positives flipped); strictly monotone on all non-NaN doubles including ±inf and subnormals (subnormal / adjacent-double test classes: 0 mismatches). The inverse `k>>63 ? k&0x7FFF… : ~k` is exact. −0 < +0 (see 2).
2. **Select logic** (38-48): pass p scans keys whose bits above `shift+16` equal `prefix` (the `hi == 64` branch avoids the `>> 64` UB on the first pass); picks the largest bucket `b` with cumulative count ≥ `rem`, subtracts the mass above it; counters are `uint64_t` (n up to 8·10⁷ and beyond); `rem ≥ 1` throughout, so `b` always lands on a non-empty bucket (the `b > 0` loop bound is safe). Ties at the c-th position, c = 1, c = n, c = n−1 and c = n+1 / c = 0 (→ −inf via the `tau_cal_of` guard) all agree. `kth_largest_f64` itself requires 1 ≤ c ≤ n; its only callers go through the guarded `tau_cal_of`.
3. **Integer width:** `40ull * (uint64_t)p + 1` (reader, line 288) is 64-bit; writer c = `top.cap` is `uint64`; no 32-bit counters or indices introduced.
4. **Determinism:** no randomness, no threads, fixed 4 passes, integer arithmetic only; result depends only on the multiset of F bits (no dependence on order) — stronger than `nth_element`, which for ±0 depends on layout.
5. **Allocation / admission:** no n-dependent allocation anywhere in the select; the reader works on the mapped file; the only remaining n-dependent allocation in the check is the legacy-order index sort (4 B/model), now capped at 2^24 models (64 MB) before admission — an improvement.
6. **Scale:** 4 sequential passes over F. Timed at n = 2·10⁷: 0.16 s (select) vs 0.31 s (copy + `nth_element`), so ≈ 0.7 s at 8·10⁷ with no 0.64 GB copy. No 32-bit limit at p = 10⁶, n = 200.
7. **Discipline:** only `engine_v4/` touched (3 files, +49/−6); no paths, no big files.

## Evidence

### (3a) Randomized differential test — `.rc_tmp/diff_test.cpp` (my own, compiled with `-O2 -std=c++20 -ffp-contract=off`)
Compares `v4::tau_cal_of` (pointer and vector overloads) against (i) the old implementation verbatim (copy + `std::nth_element`, comparator `a > b`) and (ii) a total-order oracle (sort by the same key, take c-th; bit-exact).
Value classes: small-integer ties, quarter-steps, subnormals (bit patterns 0…3000 both signs, includes ±0), ±0 mixes, ±DBL_MAX/DBL_MIN, runs of adjacent doubles (`nextafter`), random bit patterns, values sharing the top 16/32/48 bits and differing only below (stresses every pass), ±inf injections; c ∈ {1, n, n−1, three random, n+1, 0}.
Result (`.rc_tmp/diff_run1.log`):
```
cases 1920967  fail_vs_old(value/bits excl +-0) 0  fail_vs_key_oracle 0
zero-tie cases 354501 (bits differ from old: 93067)       # sign of a zero only; values equal
allocations in the pointer overload: one block of 524288 B per call, nothing larger
```
Included: 700k+ small/medium cases × 8 c values with ties, 300 large cases (n = 2·10⁵–2·10⁶, heavy ties, c ∈ {1, n/2, n, random}), and **exhaustive** enumeration of all multisets of length ≤ 6 over {−inf, −1, −0, +0, 5e-324, 1, +inf} with every c. (The ≥ 10⁶ requirement is met 1.9×.) Also a NaN probe (see 4).

### (3b) Real calib.bin
No `calib.bin` is committed in `tests/fixtures` (the suite generates them in-process), so I produced one with the built CLI on the committed fixtures `tests/fixtures/wp2_setup/p14_{data,setup}.bin`: `smcbvs4 calibrate --mode V --seed 77 --threads 2` → `.rc_tmp/real/calib.bin` (p = 14, c = 40p+1 = 561, 706 inherited models → finite τ_cal). `.rc_tmp/real_calib` (reads the file with `fmt::Reader`, old code on the real `inh_F`):
```
meta tau_cal_hex 0xc049c4df8a93457b  inherited n=706
old sort-based tau at c=40p+1=561: 0xc049c4df8a93457b  (file meta: 0xc049c4df8a93457b)
real-F all-c comparison: 707 checks, 0 bit differences      # every c = 1..n+1 on the real F values
```
τ_cal bits unchanged. (This file was written by the new writer; the old-code value is recomputed independently from the file's own `inh_F`.) Reader acceptance of such files is exercised by `island_command_offer_floor_on_off` and `offer_floor_end_to_end_merge` (both PASS).

### (4) Quick suite — `nice -n 19 tests/run_tests.sh --quick --keep` (Owls, g++ 11.5.0, 3 threads, `TMPDIR=<worktree>/.rc_tmp/tmp`, `P1M_TEST_ROOT=$TMPDIR`; `--keep` so the script deletes nothing)
```
175 test cases, 0 failed, 0 check failures
WP5 Slurm-driver tests: OK (Ran 28 tests)   WP5 competitor harness: OK   WP5 install script: OK (9 checks)
WP4 golden: 540419 checks, 0 failures
```
Includes `offer_floor_merge_rule` (the new radix block), `offer_floor_island_roles_and_science`, `offer_floor_store_is_unfloored_above_f`, `island_command_offer_floor_on_off` and `offer_floor_end_to_end_merge`. **T3 (thread/group/tile invariance)** unchanged: the island-command T3 checks (1 thread vs 3 threads, G 7, tile 64: identical section hashes) and the WP4 golden bit tests pass; the diff touches no island/store/RNG/score code, only the deterministic post-calibration τ_cal function and a size guard, so there is no path by which thread count can enter.

Sandbox: all scratch, build and TMPDIR under `<worktree>/.rc_tmp/`; nothing deleted; nothing written outside the worktree; no network; no sub-agents.
(Expected-failure log lines such as `numerical_failure: score failed after Cholesky…` in `quick.log` are the "law failure" tests passing.)
