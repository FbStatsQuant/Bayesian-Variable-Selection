VERDICT: BIT-IDENTITY CLAIM BROKEN — concrete Gram-bit and neighbour-list counterexamples exist through the requested header/export interfaces; identity of completed fits on valid preprocessed data is not disproved by these cases.

## Findings

1. **CRITICAL — NaN payloads change in the Gram.** `core_v32dev/cpp/v3_score.h:64,90` (the originally requested eight-accumulator version: `:57`). Compile the same small program separately against each core with the pinned flags. Set n=3, p=33, y=(1,1,1), and make every observation of column j the quiet NaN whose uint64 bits are `0x7ff8000000000001 + j` (j zero based; construct with memcpy). Call data_init and inspect G[1]. Actual output: v3.1 `7ff8000000000001`; original eight-lane dev `7ff8000000000002`; newer tiled dev `7ff8000000000002`. Whole-Gram SHA256s differ (below). The per-entry reduction order does not constrain which NaN operand's payload a compiler selects for multiplication. Finite multiplication commutativity does not prove NaN-bit commutativity. cpp_context(..., return_gram=TRUE), `v3_core.cpp:91–105`, exposes G without validating finite inputs. **Fix/test:** add this cross-binary case; either explicitly restrict the promise to validated finite standardized inputs and enforce/document export contracts, or use the v3.1 computation for exceptional inputs. v3_fit itself rejects raw NaNs at preprocessing, so this is an export/header counterexample, not a demonstrated fit estimate difference.

2. **CRITICAL — neighbour lists differ with NaN correlations.** `core_v32dev/cpp/v3_blocks.h:204–210`; export `v3_core.cpp:264–267`. Reproducer: n=20, p=4, B=2; column 0 all zero, columns 1–3 all one; arbitrary finite y. Zero-based returned lists:

   ```text
   v3.1:  0:{1,2,3}  1:{0}      2:{0}    3:{0}
   dev:   0:{1,2,3}  1:{0,2,3}  2:{0,1}  3:{0,1}
   ```

   For j>0, the leading NaN can stop v3.1's above-threshold prefix at zero; the new whole-list count sees two correlations equal to one and keeps two. Moreover the comparator is not a strict weak order: NaN compares equivalent to unequal finite keys, violating equivalence transitivity. Changing stable_sort to partial_sort has no general equivalence guarantee on this domain; neither sorting call has a valid comparator contract there. A finite, nonconstant raw-context case also fails: column 0 alternates -1e-200,+1e-200; each other column repeats +1,+1,-1,-1. G00 underflows to zero, its cross-products are zero, and the graphs differ. cpp_context permits both cases. **Fix/test:** retain v3.1 handling when any correlation is NaN if preserving deployed behavior is required; alternatively reject such contexts and narrow the claim. Add both cases. Constant removal and scaling protect the ordinary v3_fit path; do not present these as valid-fit failures.

3. **MAJOR — the fingerprint suppresses non-timing output, and equality is conditional on delivery.** `scripts/ws_common.R:79–88`; `core/cpp/v3_core.cpp:778–789`; `core/cpp/v3_runtime.h:20–25`. ws_strip removes whole runtime_guard objects, including exceeded, checkpoint identities, event coordinates and checkpoint counts; allocation is removed despite not being a wall-clock measurement. It also discards all list attributes except names/class, so attribute changes can hash identically. Synthetic probes confirm identical stripped objects after changing allocation$hours, runtime_guard$exceeded or a custom list attribute. A blanket name filter can hide a substantive value under any excluded name. **Fix/test:** use path-specific exclusions for numeric timing/memory/preflight fields, retain guard structure and decisions and allocation, preserve attributes, and mutation-test the comparator. Timings inside data frames are *retained*, since ws_strip returns them unchanged: that causes false differences, not hidden differences. No random numerical field was identified in the normal completed-fit fingerprint after stripping; however preflight benchmarking and RuntimeGuard can change status, partial-operation archives and available estimates with actual execution speed. Those non-timing consequences survive stripping elsewhere. Restrict identity to equal delivery/guard decisions, or disable guards in a controlled numerical-identity harness. This is a limitation of the unconditional claim, not a newly demonstrated valid-fit counterexample.

4. **MAJOR — route counts do not establish full changed-branch coverage.** `tests/bitid_units.cpp:run_case/main`; `core_v32dev/cpp/v3_start.h:160–210`. All 27 author cases report refactor successes=0. Three cases named smallQ_z... report qrec=0; only smallQ_exact_1p003 and smallQ_exact_1p02_dup establish Cholesky small-Q coverage (16 and 32 recomputations). Tests do cover QR and numerical failure, but do not assert each intended route was reached. Counters cannot distinguish failure of the H pivot from failure of A, or all reasons a log marginal is non-finite. **Fix/test:** assert route counts and add branch instrumentation, the targeted refactor case below, NaN/Inf/signed-zero cases, and a failure after earlier DFS descendants with nonzero incoming counters. Directly exercise cpp_setup's incomplete HPM conversion and exported cpp_tables/cpp_neighbours/cpp_blocks, not just header dumps. Partial table equality is strong indirect evidence for cpp_setup, but its R conversion is not executed by the C++ unit.

5. **MINOR — delivery change also applies after work has started; profiling is not a full-fit equivalence test.** `core_v32dev/v3_fit.R:152–158`; `scripts/profile_fit.R:preflight_record/full`. The changed preflight is called again before tier escalation after tier-0 calibration. It can permit escalation and thereby change status, tier, estimates, ledgers and archives relative to a refused v3.1 run; it is not confined to refusal “before any work.” The formula does not feed the scorer/kernel/RNG. profile_fit intentionally bypasses LS0 time gating (including escalation), starts its clock before generation, and synthesizes a subset of the fit fields; it cannot certify every v3_fit field. **Fix/test:** state the equal-admission qualification and test initial refusal and escalation refusal separately with a deterministic time_fun. Use bitid_fit for public-fit claims. bitid_compare also exits successfully on DIFFERENT/MISSING_B and can report zero tested units: make those fail and require an expected unit manifest.

## Arithmetic and scan-bound checks

For finite correlations, ties are broken by index, so the ordering is total; the leading above-threshold prefix equals the global count, and partial_sort selects the same first keep elements. With p>1 and B>=1, 1<=keep<=p-1 even if B>p-1. Complete-linkage distances use the same sqrt/product/divide/fabs/subtract expressions as before; removing their temporary does not by itself change finite values.

I tried to break TableDFS by row/column traversal, signed zeros, stale sibling factors, small-Q fallback, NaN Q, non-finite logm, K<B, K=0, refactor recovery and numerical-failure replay. No difference found. Each lower-triangle element depends only on earlier elements of its row and the completed preceding rows: the new scheduling preserves each scalar dependency chain. The explicit +0.0 matches try_chol, including negative-zero off-diagonals. Log-diagonal sums and quadratic sums start with +0.0, advance in index order and multiply determinants by two only at the finish. DFS preserves its own w and sums independently of Scorer's scratch, including q_nonneg. The negated small-Q test lets NaN Q reach the same invalid-arg/nonfinite-logm fallback; it does not accept NaN. Only a finite successful direct score increments ROUTE_CHOL; fallback increments are owned by sc.score. On NumericalFailure, all five persistent counters are restored, the current block is reinitialized, and increasing-code replay recreates the v3.1 failure prefix; prior blocks are already identical and later blocks remain unallocated. No ledger/cache events occur in either table builder. The production sorted-block invariant holds at exported cpp_tables because to_internal sorts members.

Under the pinned flags there is no permitted reduction reassociation or FMA contraction; packed independent finite operations can preserve the individual recurrence. x86-64-v2 uses SSE double arithmetic here, so an x87 extended-precision explanation is not applicable to these builds. The actual NaN payload experiment shows why these observations are insufficient for a promise over *all bits of all doubles*.

`core/cpp/v3_engine.h:394–405`: a centre of size k<K makes p flips and k(p-k) swaps; at k=K it makes k flips and k(p-k) swaps. Thus each scan is at most p+k(p-k), maximized over integer 0<=k<=K at k*=min(K,floor(p/2)). **The proposed scan bound is valid**, including p=1,2 and K=0. The initial eval(C) at :382 is outside the scan and A.n_eval; the expression is not a bound including that separate request. The whole-search charge does not explicitly add that initial request; its conservative scan count may absorb it. This does not invalidate the requested per-scan bound, and I did not establish a whole-search undercharge. Source changes in v3_fit.R are confined to preflight arithmetic/record; altered admission can affect later outputs.

## Coverage table

Coverage below distinguishes observed counters/results from source inference; no instrumented branch-coverage run was performed. A named case alone does not prove an obscure branch executes.

| Changed branch / condition | Author suite or added probe; remaining gap |
|---|---|
| Eight-entry Gram loop entered/skipped; scalar tail entered/skipped | Generic cases and tiny p1/7/8/9/17; all dumps equal |
| New tiled Gram full/partial tile, SIMD/scalar remainder, diagonal/off-diagonal mirror blocks | Recompiled author suite on newer snapshot: p203/600/333 and tiny cases; all dumps equal; add exact p255/256/257 and p63/64/65 boundary cases |
| Gram n=0/p=0 empty loops | Not tested; outside public valid-fit domain; explicit raw-header tests needed if promised |
| Gram NaN payload / Inf / signed zero / subnormal products | Payload added: FAIL; signed-zero table probe does not test Gram negative-zero X; overflow author cases exercise Inf Gram; add raw +/-0, denorm_min and mixed +/-Inf inputs |
| Linkage p=1 return / p>1 distance construction | tiny_p1 / all larger cases |
| Linkage finite ties | duplicates and integer cases |
| Linkage NaN distances | overflow cases exercise them; add zero-column tree dump directly; no internal distance dump |
| Graph p=1 return / candidate self-skip | tiny_p1 / larger cases |
| Graph ar>rn true/false; above=0/positive; B cap active/inactive | Independent/correlated/duplicate cases (source inference, no branch counts); add identity Gram, all-duplicate Gram and exact ar==rn fixtures |
| Graph comparator unequal / finite equal index tie | Generic / duplicate and integer cases |
| Graph NaN keys and count versus prefix | Added p4 zero column and orthogonal underflow cases: FAIL |
| Graph keep=p-1 and B>p-1 | tiny_p2 reaches keep=p-1; author's explicit overlarge-B tiny export case absent |
| Table layout/alloc; empty score; put code=0/nonzero | All author cases |
| DFS depth>=K return / false | B_above_K cases / ordinary cases; added K0 also passes |
| DFS empty child range / sibling backtracking / r=0 versus r>0 | Ordinary multi-member blocks; exact dumps test resulting state |
| H pivot positive versus nonpositive/nonfinite | Ordinary / huge-duplicate and overflow cases; exact distinction of zero, negative, NaN, +Inf not instrumented |
| A pivot rejection after H success | Not established; construct a rounding-sensitive Gram where A fails while H succeeds, assert append_row=false specifically there |
| prefix_ok false skips append and uses scorer | Expected in huge-duplicate subtrees; not independently instrumented; added tampered G00=-1 guarantees it and passes |
| Q small versus not small | smallQ_exact_1p003 / ordinary; first three smallQ_z cases do NOT establish small-Q table coverage |
| Q NaN, arg<=0/NaN, nonfinite logm | Added NaN_z/NaN_yty pass with numerical failure; Inf_z also passes; add separately asserted arg<=0 and +Inf-logm cases |
| Direct finite logm / done=false fallback | Ordinary / QR, small-Q and overflow cases |
| sc.score fallback successful refactor | Not reached by author's suite; added G00=-1 with identity design: 4 refactors, passes |
| sc.score fallback successful QR | huge_dup_qr: 444; mixed: 248; 1e120: 126 |
| Catch NumericalFailure / normal completion | overflow_fail and overflow_fail_late / ordinary; both failures have fail=1 and byte-equal partial tables |
| Counter restore with nonzero incoming counters / later blocks unallocated | Later-block overflow cases cover prior route counts; incoming qrec/refactor/QR/failure counts not explicitly seeded; add that fixture |
| Exported cpp_setup failure HPM and R table/tree/graph conversion | Not run here; supplementary fit definitions do not themselves prove execution of every export/failure conversion |
| Preflight exact / SMC LS0-off / LS0-on | R supplementary exact/SMC definitions; added deterministic LS0-on probes; explicit LS0-off/option tests should be asserted |
| Preflight method/v31 option; K below/above half, odd p | Added method/v31 and scan bound enumeration p1..100,K0..p,k0..K; both sides of half and odd p covered algebraically |
| Preflight memory skip/timing, time admit/refuse, escalation admit/refuse | Added time admit/refuse, memory sufficient; memory skip and actual escalation not run |

## What I ran

Checkout branch `theory/W3-SCALE`, HEAD `a6413127d0101074a26f58c393db0c050997e5a9`. Initial dirty file: LOG.md. During review another process changed v3_score.h; I neither changed nor reverted it. The original reviewed Gram Git blob is `0a124c0`; the newer snapshot blob is `0353f4bc3a931fd1128770385ec28b5c7b363f84`. The other three changed files were read against originals with `git diff --no-index --ignore-space-at-eol`; scorer, engine, exports, runtime, preprocessing, README and all requested scripts were inspected.

All scratch builds, binaries, dumps, logs and probes are in `C:/Users/felip/AppData/Local/Temp/w3review_5407728832bf4b1a8e3e217de50a94ba`. No SSH/cluster/commit or production cache compilation. GCC was `C:/rtools45/x86_64-w64-mingw32.static.posix/bin/g++.exe`, version 14.3.0, with that directory first on PATH. Every compilation used:

```text
-std=gnu++17 -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2
```

Commands (T denotes the scratch directory):

```text
g++ FLAGS -IScripts/SMC_BVS/core/cpp Theory_work/Wave3/W3-SCALE/tests/bitid_units.cpp -o T/v31.exe
g++ FLAGS -DHAVE_V31_REFS -IScripts/SMC_BVS/core_v32dev/cpp Theory_work/Wave3/W3-SCALE/tests/bitid_units.cpp -o T/v32.exe
T/v31.exe T/v31.bin
T/v32.exe T/v32.bin
```

Both exited 0; 27 cases; FNV `ae2fa6c2cc82672f`; dev in-process reference mismatches 0. SHA256 of both complete dumps: `00918adce068067f30172ed47e01ee83646c26669da1926cfd4284d977419736`. Recompiled the identical author source against the newer private cpp_snapshot; same exit, FNV, zero mismatches and SHA256. Did not run optional `big`.

Compiled and ran private `adversarial.cpp` against dev headers: graph counterexample above; `REFACTOR tables_equal=1 refactor_counts=4/4`. Compiled `edges.cpp` with the same flags: compares all log_r/log_m bytes, route tables, exception messages and five counters against build_tables_v31:

```text
ordinary equal=1 routes=10/0/0 qrec=0 fail=0
K0 equal=1 routes=2/0/0 qrec=0 fail=0
NaN_z equal=1 routes=2/0/0 qrec=0 fail=1
Inf_z equal=1 routes=2/0/0 qrec=0 fail=1
NaN_yty equal=1 routes=1/0/0 qrec=0 fail=1
refactor equal=1 routes=6/4/0 qrec=0 fail=0
signed_zero equal=1 routes=10/0/0 qrec=0 fail=0
nonconstant_underflow_graph_equal=0 G00=0
```

These use an 8x4 identity-column design, y=ones, blocks {{0,1,2},{3}}; modify K=0, z[1]=NaN/Inf, yty=NaN, G00=-1, or off-diagonal Gram/z zeros to -0.0, respectively. The orthogonal underflow graph fixture is as described in finding 2.

Compiled `nan_payload.cpp` against original eight-lane and newer private headers: four placements of column-specific quiet NaNs produced 844 and 524 differing Gram entries respectively versus gram_fill_v31. Then compiled `nan_cross.cpp` separately against the actual v3.1, original eight-lane private snapshot and newer snapshot, calling data_init in each executable. G[1] bits were 1/2/2 in the payload, confirming the discrepancy is not just an in-process-reference artifact. Whole-Gram SHA256:

```text
v31:    f38352e47046531201cdef66af5ec0fe4b0e71e52e5627078cd504b404353f19
eight:  782db203af49c63b0ed378b907724b0da4684d66e26399ff2b7f257c52ee417d
latest: 2942dda6e4d0aefb06c1b60b514af156cef2f11a09d7ef3ef6617e1c8e13b2d9
```

Ran `C:/Users/felip/AppData/Local/Programs/R/R-4.6.1/bin/Rscript.exe --vanilla T/probes.R`, sourcing ws_common.R and each v3_fit.R into separate environments without loading/compiling v3.R. Output:

```text
strip hides allocation and guard change: TRUE
strip hides list attributes: TRUE
data frame times remain different: TRUE
preflight scans/scan/requests/exceeds v31: 19 2600 49400 TRUE
preflight scans/scan/requests/exceeds v32: 19 1000 19000 TRUE
between-charge verdicts: TRUE FALSE
v31 option restores requests: TRUE
scan bound enumeration p=1..100 K=0..p k=0..K: PASS
```

Preflight fixture: n=20,p=100,K=10,B=4,ell=8,N=(100,400),mem_gb=8,time_fun=function(k)1; first hours=0.4, then hours=15. Startup printed four locale-setting warnings; script exited 0. Full Rcpp exports and full v3_fit fingerprints were not run. No empirical claim here extends these Windows builds to another compiler/ABI or to actual production fit delivery near resource limits.

