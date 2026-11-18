# LC1r2 reply — Claude Opus 5.5 (high), new general-purpose agent acef7c9e47939c4d5, 2026-11-16 ~17:03 CST (verbatim)

# LC1r2: second re-check of T1 GW v3 and T2 BLK v3 (Claude Opus 5.5, high)

I wrote no files and changed no git state. The core is the same at the pin and at HEAD: `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` succeeds. Lemma paths below are relative to `Theory_work/Wave3/W3-AUDIT/track_A/`, and code paths to `Scripts/SMC_BVS/core/`. I checked every code claim against the source myself.

## 1. LC1r findings

| LC1r # | Lemma | Status | Notes |
|---|---|---|---|
| 1 | T1 | RESOLVED | STATEMENT:76 now includes (C1). I checked both inclusions in Step 4 (section 3). |
| 2 | T1 | RESOLVED in substance | Fields are now leaves. 𝒱_op is now seeded from the readings and the check bodies' internal values. Booleans and the status chain are statistical (PROOF:54-56). (GW-i) and (GW-iii) are restated. The STATEMENT's wording of the definition still has literal defects (finding 1). |
| 3 | T1 | RESOLVED | 𝒜° ∈ σ(𝓒°) is stated. W3-SAMP's clause is now read for the potential pair (𝒜°, 𝓒°), with 𝒜 ⊆ 𝒜° for the actual 𝒜. CAL is assigned to T5. |
| 4 | T1 | RESOLVED | One leaf-level gap remains (finding 2). |
| 5 | T1 | RESOLVED | Minor precision point in finding 7. |
| 6 | T1 | RESOLVED | The other checks' event contexts are not covered (finding 4). |
| 7 | T1 | RESOLVED | `v3_calib.R:50, 94` and `Sys.getenv` at `v3.R:17, 29` are now listed. |
| 8 | T1 | RESOLVED | The no-error-path argument is written out but skips two stretches of code (finding 6). TLF:74 is cited, and I confirmed the quote. |
| 9 | T2 | RESOLVED | The atomless-coordinate premise and its proof line are correct. Small gaps in findings 9 and 10. |
| 10 | T2 | RESOLVED | |
| 11 | T2 | RESOLVED | `cpp/v3_core.cpp:811` reads `st.blk`; the output reaches the fit at `v3_fit.R:141-142, 172`. |
| 12 | T1, T2 | RESOLVED | Both rows were retagged STRONGER (T1 STATEMENT:102; T2 STATEMENT:64). |

## 2. Findings

1. **S — T1_GW/STATEMENT.md:38-43. The 𝒱_op definition has three literal defects.** The proof's intended reading (PROOF:54-63) is sound, but the definition as written does not say it.
   - **(a) The exception for Booleans never applies.** Every Boolean is computed from an internal value of its body: `check` returns `exceeded` (`cpp/v3_runtime.h:25-26`), and `pf$exceeds` is a field of `pf`, which STATEMENT:39 lists as internal. So the first sentence of the definition puts every Boolean in 𝒱_op. The exception ("unless they also depend on such a reading") never applies, because every Boolean does depend on one. Read literally, that is LC1r #2 again.
     - **Fix:** define 𝒱_op as the closure, under assignment, of the fields assigned from a reading or an internal value. Treat each Boolean's value at its call site as a cut: it is not counted as computed from the body's internal values. Then delete "unless they also depend on such a reading".
   - **(b) "Computes or touches" also covers reads.** The bridge check reads the engine's `ev` (`cpp/v3_engine.h:335`). `v3_preflight` reads n, p, `b` and `pre$X`. Under "touches", those become internal values, so 𝒱_op would take in the ledger provenance (`led->event(…, ev, mech)`, `cpp/v3_engine.h:99, 104`) and the whole setup. That contradicts (GW-i)'s list of statistical reads.
     - If instead the list after the colon is meant to be complete, it leaves out the guard members `start` (a clock reading) and `allocation` (`cpp/v3_runtime.h:14-15`, set at `cpp/v3_core.cpp:766`).
     - **Fix:** write "computes or writes", and list every `RuntimeGuard` member (`start`, `elapsed_before`, `allocation`, `exceeded`, `records`) as internal.
   - **(c) The guard handle is not classified.** `runtime` is produced by `cpp_runtime_new(…, proc.time()[["elapsed"]] - t_start)` (`v3_fit.R:96`), so by STATEMENT:40-41 it is in 𝒱_op. The call-site expressions read it outside the Boolean:
     - `!is.null(runtime) && …` (`v3_calib.R:75`)
     - `c->guard && …` (`cpp/v3_core.cpp:645, 692`)
     - `E.guard && …` (`:459, 480`)
     - `guard && …` (`cpp/v3_engine.h:335`)

     So `g$resource_limit`, which PROOF:55 lists as statistical, reads an operational field. Separately, `if (!is.null(runtime))` at `v3_fit.R:82` is a decision outside any check body, which contradicts PROOF:32 as worded. That branch writes only `fit$runtime_guard`, which is operational, so nothing downstream breaks.
     - **Fix:** define the Boolean as the whole call-site expression, including the null test. Note that the handle is non-null on every path after `v3_fit.R:96`, so in P° the expression is FALSE. At PROOF:32, write "reaches a decision that assigns a statistical field only through a Boolean".

2. **S — T1_GW/STATEMENT.md:72-74; PROOF.md:114-117.** "The allocation reaches only the field `fit$allocation`" is false at leaf level, and so is "every statistical field other than `fit$allocation` is a function of (X, y, seed) and the options".
   - The normalised local `allocation` (`v3_fit.R:92`) is statistical by the definition: it is computed from the input with no reading.
   - Depending on how finding 1(b) and 1(c) are fixed, the guard's `allocation` member and the handle `runtime` (`v3_fit.R:96`) are statistical too.
   - All of these are read only by check bodies (`v3_fit.R:115, 145`, `cpp_runtime_new`, `check`) or copied into `fit$allocation`, so the substance holds.
   - PROOF:115 calls `cpp_runtime_new` a check body. By STATEMENT:33-34 it is not one.
   - **Fix:** classify the guard (its handle and members) as operational. Then say that the allocation reaches statistical state only through `fit$allocation` and the normalised local `allocation`, which is read only by check bodies and by `v3_fit.R:95`.

3. **E — T1_GW/STATEMENT.md:49-50, 74-76; PROOF.md:120.** 𝓒°, 𝒜° and G are not defined when `v3_calibrate` is never called. That happens on the exact branch, the preprocessing exits, setup failure, an invalid seed, and when (C1) fires.
   - **Fix:** give 𝓒° a "not called" value; then 𝒜° = {status = "ok"} ∈ σ(𝓒°) still holds. Read G as "up to the return of `v3_calibrate`, or the whole run if it is not called".
   - The proof's parenthetical "(C1) and every check inside `v3_calibrate`" needs one more fact to equal G: no check site lies in `v3_fit.R:118-149` (`v3_setup`, `cpp_cut_group`). I confirmed this with grep: `cpp_runtime_check` is called only at `v3_calib.R:75`. Add that line to the proof.

4. **E — T1_GW/STATEMENT.md:57-58 ((GW-i)'s list of statistical reads).** "The engine's event context `ev`" covers only the bridge check. The other checks get a context built at the call site:
   - `local_event(tier, iter)` (`cpp/v3_core.cpp:459, 480, 645, 692`)
   - `cpp_runtime_check`'s `tier` and `length(grids) - 1L` (`v3_calib.R:76`; `cpp/v3_core.cpp:772-773`)

   The list also leaves out `ls0_worst_case` (`v3_fit.R:114-115, 145`). **Fix:** "the event context passed to `check` (the engine's `ev` at bridge stages; otherwise one built from the tier and the iteration or grid index)", and add `ls0_worst_case`.

5. **E — T1_GW/STATEMENT.md:103 (changelog).** The v3 row leaves out (GW-iii), whose wording changed to "statistical fields" (disposition #2). Separately, the (GW-iv) row carries a WEAKER tag. PROTOCOL_v4:162 handles a WEAKER change differently on a target clause, so the row should record whether (GW-iv) is one. It was added in v2 and does not look like a CP1 target.

6. **E — T1_GW/PROOF.md:96-99 (Step 2, no error path).** Two stretches of code that run after a firing are not argued. I checked both, and neither can raise an error.
   - **The rest of `v3_calibrate` after a stop** (`v3_calib.R:161-191`). `tr` may be NULL, but `isTRUE(NULL)` is FALSE and `names(NULL)[NULL]` is NULL. `vapply(…, 0)` accepts the integer `forced_pilot_steps`, because vapply promotes integer to double. Line 163 short-circuits on `status`.
   - **`v3_fit.R:163-173` after a final-run stop.** `fr$flags$… <-` on a NULL `fr$flags` creates a list, and the copy loop cannot fail.

   **Fix:** add one sentence covering both.

7. **E — T1_GW/PROOF.md:131-133 (Step 5).** "Outside 𝒜 or 𝒪" should say which applies where. A throw in a calibration search ends the run outside 𝒜 (`v3_calib.R:57, 100` → `:153`). A throw in the final local search or LS0 ends it outside 𝒪 (`v3_run.R:143`).
   - Optional: the `std::runtime_error` for |S| > K (`cpp/v3_score.h:230`) cannot be reached in `local_search`. Additions are skipped at `cpp/v3_engine.h:397`, swaps keep the size, and the centres have size ≤ K. If it were reached, it would become an R error, which is outside 𝒪.

8. **E — T2_BLK/STATEMENT.md:65 (changelog tag).** The setting-R premise row is tagged EQUAL. Compared with v2's "continuous law" read as absolutely continuous, the clause now also covers singular Σ_n. **Fix:** retag it STRONGER, or state that the pending statement-change check for the v2 STRONGER row on the same clause (:64) covers it.

9. **E — T2_BLK/STATEMENT.md:26-29.** The premise sentence leaves out "ε independent of the raw rows". PROOF:72-73 uses that fact for "independent of ε". It is part of setting R (`W3-RM/STATEMENT.md:42`), but the sentence reads as a complete list of premises. **Fix:** add it.

10. **E — T2_BLK/STATEMENT.md:45 vs PROOF.md:71-72.** The statement claims σ(X)-measurability; the proof composes through the raw design and shows σ(X^r)-measurability, a larger σ-field. **Fix:** either argue directly that C = f(X) a.s. with f Borel by (BLK-c), so C is σ(X)-measurable up to the null set, or state σ(X^r) in the STATEMENT.

## 3. Attempts to break the rewritten parts that held

**Is any statistical field computed from an operational one? No, at code level.** I checked:
- `fail` (`v3_calib.R:33-43`): `seconds_total`, `grid_construction$seconds`, `partial_operation` (a leaf-level mix).
- `out$seconds` and the `grids[[·]]$seconds` records (`v3_calib.R:71-74, 132-135`).
- The pilot and diagnostic `seconds` (`:50, 94`).
- The stage tables, which have no time columns (`v3_run.R:50-64`).
- `island_to_list` `seconds` (`cpp/v3_core.cpp:347`) and the final timings (`v3_run.R:214-216`).
- `cpp_runtime_report`.
- `fit$preflight` and `fit$preflight_escalation`, which are written but never read.
- The numerical-route counters. They live in `Data` (`cpp/v3_score.h:20-21`; `cpp/v3_core.cpp:822-826`), and the benchmark scores on a fresh context, so the counters are separate.

**Does the clock leak outside the Booleans? No.** The only comparisons involving time are `cpp/v3_runtime.h:23` and `v3_fit.R:60, 65, 47`, all inside check bodies. The only paths from the guard into statistical state are the call-site expressions listed in finding 1(c).

**𝒜 = 𝒜° ∩ G, (⊆).** Every check reachable before `v3_calibrate` returns makes the status non-"ok" when it fires:
- pilot bridge: `cpp/v3_core.cpp:637-639`
- pilot local search: `:645`
- diagnostic bridge: `:673-680`
- diagnostic local search: `:692`
- grid construction: `v3_calib.R:81, 113`. Because `cpp_build_grid` returns no `status` element, `c(g, list(status = "resource_limit"))$status` is "resource_limit".
- (C2): `:157`
- (C1): `v3_fit.R:117`, where calibration is never called.

The fallback grid and `schedule_limit` apply only when `status == "ok"` (`:163, 170`). The shared guard is sticky, and no check runs before (C1) or between (C1) and `v3_calibrate`.

**𝒜 = 𝒜° ∩ G, (⊇).** P° runs the same bodies and sees the same clock readings, so up to the first firing the two runs agree in full state, not just statistical state. On G that agreement lasts until `v3_calibrate` returns.

**𝒜° ∈ σ(𝓒°)** holds once the "not called" case is fixed (finding 3).

**Step 5.** `local_search` is called only at `cpp/v3_core.cpp:455, 476, 642, 689`. The catches at `:483-484, 649-650, 695-696` all set "numerical_failure". No other catch surrounds a search, and `local_search` contains no `guard` use.

**T2.** P(x_{1j} = x_{2j}) = 0 holds for independent copies of an atomless law, and the bound for all columns follows by a finite union. The binary64 sentence for (BLK-c) is correct: `data_init` computes G from X only (`cpp/v3_score.h:44-53`).

None of the findings is C or F. T1's two S findings are wording fixes that leave the proof's argument unchanged. T2's three findings are editorial only.

LC1r2-VERDICT: T1=VERIFIED WITH AMENDMENTS; T2=VERIFIED WITH AMENDMENTS
