# LC1r reply — Claude Opus 5.5 (high), new general-purpose agent aa56538fa702baa3e, 2026-11-16 ~16:52 CST (verbatim)

LC1r review of the repaired lemmas T1 GW v2 and T2 BLK v2. I wrote no files and changed no git state. The core is unchanged from 4676af6 to HEAD (`git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` succeeds). I checked every claim below against the code myself. Paths are relative to `Theory_work/Wave3/W3-AUDIT/track_A/` for lemma files and to `Scripts/SMC_BVS/core/` for code.

## 1. LC1 findings: resolved or not

**T1 (GW)**
| LC1 # | Status | Notes |
|---|---|---|
| 1 | RESOLVED | `peak_memory_kb` and the environment readings are now in 𝒱_op. I confirmed they reach only `v3_fit.R:80` and `56-57`. |
| 2 | RESOLVED for the named variables | The new 𝒱_op definition has its own defect (finding 2 below). |
| 3 | RESOLVED | P° now executes the check bodies. The termination argument is correct: k is clamped at `cpp/v3_core.cpp:126`, the benchmark uses a separate `Data` built by `v3_context`, no code anywhere holds global mutable state, and `NumericalFailure` is caught at `:134`. |
| 4 | PARTLY RESOLVED | (GW-iv) was added, but its wording is wrong (finding 1), and W3-SAMP's "𝒜 ∈ σ(𝓒)" is not dealt with (finding 3). |
| 5 | RESOLVED | |
| 6 | RESOLVED | I grepped every `Clock`, `chrono`, `proc.time`, `Sys.time` and `Sys.getenv` call. Step 1's list is now complete for fit time. |
| 7 | RESOLVED | The line list is slightly incomplete (finding 7). |
| 8 | RESOLVED | |
| 9 | RESOLVED | Step 5 leaves out one exit (finding 5). |

**T2 (BLK)**
| LC1 # | Status | Notes |
|---|---|---|
| 1 | RESOLVED | |
| 2 | RESOLVED, with a premise fix | See finding 9. |
| 3 | RESOLVED | The binary64 argument for (BLK-a) and (BLK-b) is correct (details in section 3). (BLK-c)'s binary64 remark is not argued (finding 10). |
| 4 | RESOLVED | |
| 5 | RESOLVED | `:283, 300, 410, 469, 611, 714` all read the same `st`. |
| 6 | RESOLVED | Recorded as a code note. |

## 2. Findings

1. **C — T1_GW/STATEMENT.md:64 (GW-iv).** The statement says "𝒜 = 𝒜° ∩ {no check fires during calibration}". PROOF.md:103-104 defines "calibration checks" more widely: every check evaluated until `v3_calibrate` returns, which includes the first preflight (C1, `v3_fit.R:117`). Read literally, the statement's version is false.
   - Counterexample: SMC branch with a tiny `mem_gb`, for example 1e-9. (C1) fires on memory alone, so `v3_calibrate` never runs and 𝒜 is false.
   - P° does not stop at (C1), so it can calibrate with status "ok", making 𝒜° true. And {no check fires during calibration} is vacuously true.
   - Under the PROOF's definition the equality holds, and I checked both inclusions. 𝒜 ⊆ 𝒜° holds under either reading.
   - **Fix:** in the STATEMENT, write {no check evaluated before `v3_calibrate` returns fires, (C1) included}, or define "calibration check" there.

2. **S/C — T1_GW/STATEMENT.md:36-38, 59-61; PROOF.md:52-53.** The 𝒱_op definition counts a variable as operational if it is assigned "from a check body". A check's Boolean is the value of its body. So the status chain is operational on every run, fired or not:
   - `_["status"] = check ? "resource_limit" : "ok"` (`cpp/v3_core.cpp:645, 692`) runs on every pilot and diagnostic call.
   - From there it flows to `pil$status`, `out$pilot$partial` (`v3_calib.R:51, 53`), `a$status`/`status` (`v3_calib.R:153`) and `fit$status`.

   Two consequences:
   - (GW-iii)'s "𝓒 and its status", 𝒜° (a status event) and Step 4's "statistical state is a function of (X, y, seed)" all refer to variables the definition calls operational. PROOF.md:52 classifies `fit$status` as the "Boolean acting" but puts `g$resource_limit` in 𝒱_op, which is inconsistent.
   - The definition does not fix granularity. Objects such as `res`/`island_to_list` (`seconds` at `cpp/v3_core.cpp:347`), `pil`, `cal` and `fit` mix timing fields with statistical ones. (GW-iii)'s "every final island record … equals P°'s" is literally false for the island records' `seconds` fields.

   **Fix:**
   - Define 𝒱_op at leaf-field level (list element or struct member).
   - Seed 𝒱_op from clock and environment readings and from the check bodies' internal values (`records`, `exceeded`, `pf`, `tcache`, benchmark output), not from the Boolean's value at the call site.
   - Restate (GW-i) as: every statistical field is a function of earlier statistical fields and the Booleans, and on the no-fire path every Boolean is FALSE.
   - Step 3's induction then goes through unchanged, since in P° the Booleans are the constant FALSE.

3. **F — T1_GW/STATEMENT.md:63-66; PROOF.md:117-122 (Relation).** W3-SAMP:39-41 asserts "𝒜 ∈ σ(𝓒)". GW-iv now reads W3-SAMP's 𝒜 as the actual event. That event depends on the clock through {no calibration check fires}, so in general it is not σ(𝓒)-measurable. GW leaves W3-SAMP's clause standing.
   - What holds is 𝒜° ∈ σ(𝓒°): status is a field of 𝓒°, and the branch depends only on (n, p).
   - "The calibration record of CAL is 𝓒°" is a naming, not a discharge. CAL's "streams 0–9" part is a two-line code fact: `CalState::stream` (`cpp/v3_core.cpp:594-597`) with sid ∈ {0..9} (`:626, :667`).
   - **Fix:** add "𝒜° ∈ σ(𝓒°); W3-SAMP's 𝒜 ∈ σ(𝓒) is to be read for the potential pair (𝒜°, 𝓒°)". Either cite where CAL for 𝓒° is proved or add the stream fact.

4. **S — T1_GW/STATEMENT.md:63; PROOF.md:102-103.** "P°'s statistical state is a function of (X, y, seed) alone" is false for `fit$allocation`. It is set from the input `allocation` (`v3_fit.R:76, 95`) and is not in 𝒱_op. Nothing else statistical depends on `allocation`; the preflight and the guard are in 𝒱_op. **Fix:** write "(X, y, seed, allocation), with allocation reaching only `fit$allocation`", or put that field in 𝒱_op.

5. **C (minor) — T1_GW/PROOF.md:111-113 (Step 5).** "Its exits are its own termination rules: the move cap and no strict improvement" leaves out the exception exit: `eval` calls `Scorer::score`, which can throw `NumericalFailure` (`cpp/v3_engine.h:92`; `cpp/v3_score.h:237`). (GW-v)'s conclusion still holds, because every such throw sets status `numerical_failure` (`cpp/v3_core.cpp:649-650, 695-696, 483-484`), which is outside 𝒜 and 𝒪. **Fix:** add the throw exit and the line about status.
   - On the point the brief asked about, "no check runs inside a search" is correct. The only `guard` uses in the engine are `cpp/v3_engine.h:62` (declaration) and `:335` (inside `run_island_s`, which `local_search` does not call). The R-level checks (C1), (C2) and the grid check run outside any C++ search. Every C++ search check comes after the search returns (`cpp/v3_core.cpp:456-459, 476-480, 642-645, 689-692`).

6. **E — T1_GW/STATEMENT.md:52.** "No check reads … the engine" is literally false. The bridge check receives the engine's member `ev` (`cpp/v3_engine.h:335`) and copies it into `GuardRecord` (`cpp/v3_runtime.h:24`). This is harmless because it is a read whose copy lands in 𝒱_op. **Fix:** "reads only the engine's event context `ev`, copied into the guard record".

7. **E — T1_GW/PROOF.md:34-35 and 7-10.**
   - The list of places where R timing values are "read only to compute timing fields" leaves out `v3_calib.R:50` (`seconds = pil$seconds`) and `:94` (`seconds = dg$seconds`).
   - The load-time environment readings `Sys.getenv` at `v3.R:17, 29` are not mentioned next to `Sys.time` at `v3.R:37, 54-55`.

   Conclusions are unchanged.

8. **E — T1_GW/PROOF.md:86-88 (Step 2) and STATEMENT.md:75-76.**
   - "No error path … (checked independently by LC1)" uses a reviewer's note as a proof step. Put the short argument into the proof: `fail` builds lists only; `v3_stage_table` handles NULL island slots; the incomplete branch of `v3_assemble_final` is `v3_run.R:143-148`.
   - "The core statements use only this upper-bound direction" has no source. Cite TLF's Output contract row: "Bounds transfer by intersection with 𝒪, never by conditioning on delivery".

9. **F — T2_BLK/STATEMENT.md:26 and PROOF.md:69.** "Continuous rows" / "i.i.d. with a continuous law" is the wrong premise for setting R:
   - W3-RM:41-42 assumes rows N(m_n, Σ_n) with Σ_n unit-diagonal. It does not assume Σ_n nonsingular (its λ_min conditions are on subsets only, `W3-RM/STATEMENT.md:131-134`).
   - If "continuous" means absolutely continuous, it excludes singular Σ_n. If it means atomless, it is too weak: a row law can be atomless while one coordinate is constant.
   - What is needed is that each coordinate's marginal law is atomless. In setting R that holds because (Σ_n)_jj = 1.

   **Fix:** state that premise. The rest of the paragraph is correct: the null-set extension is Borel, and C is independent of ε because ε is independent of the rows.

10. **E — T2_BLK/STATEMENT.md:51-52.** The claim that (BLK-c) holds "with R̂ replaced by the computed correlation matrix" is not argued in the PROOF's Binary64 section (PROOF.md:74-79). It does follow from the code reading at PROOF.md:44-46: `make_blocks` reads only `correlation_matrix(D)` and `D.p`, and the binary64 standardisation is column-wise with no y. **Fix:** add that one sentence there.

11. **E — T2_BLK/STATEMENT.md:32-34.** The list of uses of `st` leaves out `cpp_cut_group`, which reads `st.blk` (`cpp/v3_core.cpp:811`) and feeds `fit$cut_group` and its flag (`v3_fit.R:141-142, 172`). Rows 3.1 and 3.6 don't need it, but the list reads as complete.

12. **E — changelogs (T1_GW/STATEMENT.md:85; T2_BLK/STATEMENT.md:59).** Two v2 changes are tagged "EQUAL in substance" but add new claims, so they should be tagged STRONGER:
    - (GW-i) now also claims "every check body terminates normally".
    - (BLK-c) now also claims σ(X)-measurability and independence from ε under setting R.

## 3. Does the repair break anything LC1 had verified?

No. I re-checked the following and they still hold:
- Step 2's paths and the status assignments in `cpp_final_run` (only `:413, 451, 459, 480, 484`).
- The sticky shared guard.
- `estimates_available = TRUE` is set only at `v3_fit.R:129` and `v3_run.R:218`.
- In calibration, no "resource_limit" can turn back into "ok": `v3_calib.R:153`, and `:163, :170` apply only when status is "ok".
- Step 3's induction. With P° executing the bodies, actual and P° now take identical steps up to the first check that fires, which is cleaner than v1.

For T2, the (BLK-a) and (BLK-b) arguments are unchanged. In the new binary64 section I checked `recompute_row`'s `best[i] < 0 ||` guard (`cpp/v3_blocks.h:71`), the recomputation at `:102` and `bi` selection (`:79-80`): each merge joins two distinct active slots whatever the floating comparisons return, NaN included. `nrow`/`ncol` ≤ 2³¹ − 1, so `v3_isqrt` is exact.

LC1r-VERDICT: T1=VERIFIED WITH AMENDMENTS; T2=VERIFIED WITH AMENDMENTS
