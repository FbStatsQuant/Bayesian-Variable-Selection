# T1 · Lemma GW — PROOF v4 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

v1 → v2: LC1 findings #1–#9 applied (`reviews/LC1_reply_opus.md`, disposition `reviews/LC1_disposition.md`).
v2 → v3: LC1r findings #1–#8 applied (`reviews/LC1r_reply_opus.md`, disposition `reviews/LC1r_disposition.md`).
v3 → v4: LC1r2 findings #1–#7 applied (`reviews/LC1r2_reply_opus.md`, disposition `reviews/LC1r2_disposition.md`).

Fix a valid input (X, y, seed, allocation) and assume EX-A. Then every computation of `v3_fit` is a deterministic
function of the input, the option values, the clock readings and the machine-environment readings: the only randomness
is the counter-based uniform streams `Xoshiro256ss::seed_stream(seed, k)` (`cpp/v3_util.h:43-61`), and no thread,
`random_device`, `rand`, R RNG call (`runif`, `sample`, `rnorm`, `set.seed`) or wall-clock seed occurs in the core (grep
over `cpp/` and `*.R`, 2026-11-16; the clock hits are those listed in Step 1, plus `Sys.time` in the build helper
`v3_compile`, `v3.R:37, 54-55`, and `Sys.getenv` at `v3.R:17, 29` (core directory and build flags), which run once at
load time, before any fit; they choose which code is loaded, and the lemma is about the code of record). Environment readings: `Sys.getenv` and
`R.version` inside `v3_preflight` (`v3_fit.R:56-57`, into the preflight's returned record only) and
`/proc/self/status` in `v3_peak_memory_kb` (`v3_fit.R:2-7`, into `fit$peak_memory_kb` only, `v3_fit.R:80`). Everything
below is a statement about which variables these readings can reach.

## Step 1 — where clock and environment readings go (GW-i)
C++ (`Clock = std::chrono::steady_clock`, `cpp/v3_engine.h:55-56`; guard clock `cpp/v3_runtime.h:14, 19`):
- `cpp/v3_engine.h:284, 298, 341, 348, 361` → `res.seconds_init/bridge/burn/measured` (IslandResult timing fields);
  `cpp/v3_engine.h:304, 335` → the operation time passed to `guard->check`; `cpp/v3_engine.h:336` → `res.seconds_bridge`
  on a stop.
- `cpp/v3_core.cpp:278-303` → `g->block/table/start/graph_seconds`; `cpp/v3_core.cpp:406, 514` → `seconds_total`;
  `cpp/v3_core.cpp:455-459` → `sec_local` (output field and `check` argument); `cpp/v3_core.cpp:468, 477, 480, 516` →
  `sec_ls0` (same); `cpp/v3_core.cpp:630-645` and `cpp/v3_core.cpp:664-692` → `sec_isl`, `sec_ls` (output fields and
  `check` arguments); `cpp/v3_core.cpp:579, 582` → `seconds` of `cpp_build_grid`; `cpp/v3_core.cpp:128-137` →
  `seconds_per_score` of the timing benchmark; `cpp/v3_core.cpp:789` → the guard report.
- R (`proc.time`): `v3_calib.R:30, 41, 65, 76, 135, 145, 191`; `v3_fit.R:74, 81, 96, 121-122, 133, 139, 149, 152, 162,
  164`. Each goes to a timing variable or field (`t_start`, `t0`, `t_all`, `t_build`, `t_grid`, `*seconds*`,
  `fit$timings`), to `elapsed_before` of the guard (`v3_fit.R:96`), or to the operation time of `cpp_runtime_check`
  (`v3_calib.R:75-76`). The grid's `g$seconds` goes to `grids[[·]]$seconds` and `t_grid` (`v3_calib.R:73-74`).

All of these are in 𝒱_op. A value in 𝒱_op reaches a decision that assigns a statistical field only through a Boolean.
The one decision on the guard outside a check expression, `if (!is.null(runtime))` (`v3_fit.R:82`), writes only
`fit$runtime_guard`, which is operational. Time is compared only inside check bodies: the comparisons involving a time
quantity at the pin are `cpp/v3_runtime.h:23` (in `check`) and `v3_fit.R:60, 65` (in `v3_preflight`'s `exceeds`); the
call sites that use a check's Boolean are exactly the (C1)–(C3) sites (`cpp/v3_core.cpp:459, 480`, the `?:` at
`cpp/v3_core.cpp:645, 692`, the `&&` at `v3_calib.R:75-76`, `cpp/v3_engine.h:335`, `v3_fit.R:117`, `v3_calib.R:157`).
In R, timing variables are read only to compute other timing fields (`v3_calib.R:40, 50, 74, 94, 132-135`; `v3_fit.R:81, 139,
152, 164`; `v3_run.R:214-216`); no statement of `v3_calibrate`, `v3_cal_tier`, `v3_final_run` or `v3_assemble_final`
reads one in a condition or in a statistical assignment.

The check bodies and what they touch.
- `RuntimeGuard::check` (`cpp/v3_runtime.h:21-27`) reads `elapsed()` (clock + `elapsed_before`), its argument and
  `allocation`, appends one `GuardRecord` (a copy of the `EventCtx` argument) and updates `exceeded` (sticky:
  `exceeded = exceeded || stop`); it returns `exceeded`. Its struct holds only the fields at `cpp/v3_runtime.h:14-17`:
  no pointer to an engine, ledger, cache, stream or start object. `cpp_runtime_check` (`cpp/v3_core.cpp:770-775`)
  builds a fresh `EventCtx` and calls `check`.
- `v3_preflight` (`v3_fit.R:26-68`) reads n, p, the budgets `b` (K, B, tier sizes, `ell`, for the exact branch
  `b$exact_count`), `branch`, `tier`, the allocation, `ls0_worst_case` (from option `v3.ls0_cap`, `v3_fit.R:114`) and the
  environment; through `time_fun` it runs the benchmark `v3_time_scores` (`v3_fit.R:10-14`), which builds a **new**
  context from columns of the preprocessed (X, y) (`v3_context`, `v3_setup.R:7-13`) and scores 200 fixed models with a
  local `Scorer` (`cpp/v3_core.cpp:124-138`); only `seconds_per_score` leaves it (`sink` is discarded). It uses no stream
  and no shared cache, ledger or setup object. Its writes are its return value (the local `pf`), `tcache` (read only by
  `time_fun`), and `fit$preflight` / `fit$preflight_escalation` (`v3_fit.R:116, 146`); `fit` is not passed to
  `v3_setup`, `v3_calibrate` or `v3_final_run` (`v3_fit.R:133, 150-151, 162`).
- The Boolean at the call site, and what is computed from it (`_["status"] = … ? "resource_limit" : "ok"`, the local
  `status`, `g$resource_limit`, `res.partial`, `fit$status`), are statistical by definition; they are the only channel
  from a check to the statistical state, and on the no-fire path every Boolean is FALSE.
- The bridge check reads the engine's event context `ev` (`cpp/v3_engine.h:335`) and copies it into the guard record
  (`cpp/v3_runtime.h:24`); it reads no other engine member.

So every statistical field is computed from the input, earlier statistical fields and Booleans: the only other sources
(clock, environment, check-body internal values) are in 𝒱_op by definition, and the paragraphs above show that no
statistical assignment reads a field of 𝒱_op. (Granularity: e.g. `island_to_list` puts `seconds` next to `logZ` in one
list (`cpp/v3_core.cpp:347`); the `seconds` element is operational, the others are not.)

Termination of the bodies (needed because P° executes them): `check` and `cpp_runtime_check` contain no throw;
`v3_preflight` is arithmetic plus `time_fun`; in `v3_time_scores`, `v3_context`'s `stopifnot` conditions hold for a
column subset of the preprocessed design (`v3_setup.R:8`), `cpp_time_scores` clamps k to [0, K] (`cpp/v3_core.cpp:126`)
so `Scorer::score` never sees |S| > K (`cpp/v3_score.h:230`), and it catches `NumericalFailure` (`cpp/v3_core.cpp:134`).
(Allocation failure is MACH.)

No check draws a uniform: uniforms are read only through `VariateSource::u` (`RngSource`, `cpp/v3_engine.h:20-23`) at
`cpp/v3_engine.h:108, 129, 150-151, 156, 167, 171, 177, 189, 199, 250` and `cpp/v3_start.h:160, 164, 170`, never in
`v3_runtime.h`, `v3_preflight` or `cpp_time_scores`. This proves (GW-i).

## Step 2 — every fired check ends the run without output (GW-ii)
- (C1) `v3_fit.R:117`: status `"resource_limit"`, immediate `return(finish(fit))`; no HPM field is set.
- (C2) `v3_calib.R:157`: `status <- "resource_limit"`, loop exits; `v3_calibrate` returns that status
  (`v3_calib.R:171`), and `v3_fit.R:154-159` sets `fit$status` to it, labels the HPM `hpm_incomplete = TRUE` and returns.
- (C3) bridge stage: `cpp/v3_engine.h:335-337` sets `res.partial = true` and returns. Pilot: `cpp/v3_core.cpp:637` returns
  status `"resource_limit"` → `v3_calib.R:57` `fail(pil)`. Diagnostics: `cpp/v3_core.cpp:673-680` → `v3_calib.R:100`
  `fail(dg)`. Final run: `cpp/v3_core.cpp:451` sets `status = "resource_limit"` and breaks the island loop; the final
  local search and LS0 are skipped (`cpp/v3_core.cpp:453, 465`).
- (C3) local searches: pilot `cpp/v3_core.cpp:645` and diagnostics `cpp/v3_core.cpp:692` return status
  `"resource_limit"` → `v3_calib.R:57, 100`. Final local search `cpp/v3_core.cpp:459` and LS0 `cpp/v3_core.cpp:480` set
  `status = "resource_limit"`; LS0 is then not started (`cpp/v3_core.cpp:465`). Nothing in `cpp_final_run` assigns
  `"completed"` after its initialisation (grep: the only assignments to `status` are `cpp/v3_core.cpp:413, 451, 459,
  480, 484`).
- (C3) grid construction: `v3_calib.R:75-76` → `v3_calib.R:81` or `v3_calib.R:113`
  `fail(...status = "resource_limit")`.
- In calibration every `fail` makes `a$status != "ok"`, so `v3_calibrate` breaks with that status (`v3_calib.R:153`) and
  `v3_fit.R:154-159` returns as in (C2). In the final run `v3_assemble_final` takes the branch
  `raw$status != "completed"` (`v3_run.R:143-148`): `hpm_incomplete = TRUE`, `estimates_available = FALSE`, estimate
  fields NA (`v3_run.R:147`, v3.1). `finish` then sets every estimate field to NA again whenever
  `estimates_available` is not TRUE (`v3_fit.R:85`, `v3_run.R:109-114`). `estimates_available = TRUE` is set only at
  `v3_fit.R:129` (exact branch, status `"exact"`) and `v3_run.R:218` (reached only when `raw$status == "completed"`).
  The code run after a firing has no error path: `fail` (`v3_calib.R:33-43`) only builds a list from fields that
  exist (`exists(...)` guards at `v3_calib.R:37-40`); `cpp_cal_export` (`cpp/v3_core.cpp:728-740`) only reads the
  calibration state; `v3_stage_table` skips NULL or empty island slots (`v3_run.R:52`); the incomplete branch of
  `v3_assemble_final` (`v3_run.R:143-148`) only assigns fields. The rest of `v3_calibrate` after a stop (`v3_calib.R:161-191`) is safe: a NULL `tr` gives `isTRUE(NULL)` = FALSE and
  `names(NULL)[NULL]` = NULL, `vapply(…, 0)` accepts the integer `forced_pilot_steps`, and `v3_calib.R:163` short-circuits
  on `status`; `v3_fit.R:163-173` after a final-run stop only creates list fields and copies them. So the fit returns
  with status `"resource_limit"`. Hence a fired check gives a run outside 𝒪. This proves (GW-ii).

## Step 3 — completed runs are potential runs (GW-iii)
Run the actual fit and P° side by side on the same input, with the same clock and environment readings. Both programs
execute the same statements in the same order (P° also executes every check body) until the first check that fires in
the actual run: at each earlier check both take the "no stop" branch, and by Step 1 everything the check bodies and the
timing code assigned lies in 𝒱_op, from which no statistical variable is assigned except through a Boolean that was
FALSE in both. So, by induction over the executed statements, the statistical states agree up to the first firing check.

If no check fires in the whole actual run, the two executions agree to the end, so their statistical states agree at
every point and the run is in 𝒪 iff P°'s run is in 𝒪°. If some check fires, the run is outside 𝒪 by Step 2. Hence
𝒪 = 𝒪° ∩ {no check fires}, and on 𝒪 every statistical quantity equals P°'s. ∎ (GW-iii)

## Step 4 — the interface (GW-iv)
In P° every Boolean is FALSE, so by (GW-i) every statistical field of P° is computed from the input and earlier
statistical fields only, hence is a function of the input. The allocation enters statistical state only as
`fit$allocation` and the normalised local `allocation` (`v3_fit.R:76, 92-95`); the latter is read only by `v3_fit.R:95`,
by the check bodies (`v3_preflight` at `v3_fit.R:115, 145`) and by `cpp_runtime_new` (`v3_fit.R:96`), whose output, the
guard, is an internal value. So every other statistical field of P° is a function of (X, y, seed) and the options.
𝒜° = {𝓒° ≠ ⊥, status of 𝓒° = "ok"} ∈ σ(𝓒°), with ⊥ a value of 𝓒°.

𝒜 = 𝒜° ∩ G (G as defined in the STATEMENT). The checks evaluated before `v3_calibrate` returns are (C1) and those inside
`v3_calibrate`: no check site lies in `v3_fit.R:118-149` (`v3_setup`, `cpp_cut_group`; `cpp_runtime_check` is called only
at `v3_calib.R:75`). If P° does not call `v3_calibrate`, neither does the actual run (that decision is statistical and
precedes any check except (C1), which can only stop the actual run), so 𝒜 = 𝒜° = ∅ there. (⊇) On G, Step 3's induction runs to the return of `v3_calibrate` with no firing, so the actual
calibration output's statistical fields equal P°'s, in particular its status; so 𝒜° ∩ G ⊆ 𝒜. (⊆) If (C1) fires,
`v3_calibrate` is never called (`v3_fit.R:117`) and 𝒜 fails; if a check inside `v3_calibrate` fires, its status is
`"resource_limit"` (Step 2) and 𝒜 fails; so 𝒜 ⊆ G, and on G the statuses agree, so 𝒜 ⊆ 𝒜°. From (GW-iii), 𝒪 ⊆ 𝒪°,
and for an event A of the statistical state, on 𝒪 the indicator of A equals that of A° (same statistical state), so
𝒪 ∩ A ⊆ 𝒪° ∩ A°. The identifications with W1-N1's potential record and TLF's 𝒪̄ are these definitions. ∎

## Step 5 — complete scans (GW-v)
`Engine::local_search` (`cpp/v3_engine.h:379-419`) contains no check (the only uses of `guard` in the engine are
`cpp/v3_engine.h:62, 335`, and `run_island_s` is not called from it); its exits are its own termination rules, the move
cap (`cpp/v3_engine.h:410`) and no strict improvement (`cpp/v3_engine.h:414`), and a `NumericalFailure` thrown by the
scorer inside `eval` (`cpp/v3_engine.h:92`, `cpp/v3_score.h:237`). The throw is not operational; every catch sets status
`"numerical_failure"` (`cpp/v3_core.cpp:483-484, 649-650, 695-696`), so a throw in a calibration search ends the run outside 𝒜
(`v3_calib.R:57, 100` → `v3_calib.R:153`) and a throw in the final local search or LS0 ends it outside 𝒪
(`v3_run.R:143`). (The |S| > K `runtime_error`, `cpp/v3_score.h:230`, is unreachable in a search: additions are skipped at
size K, `cpp/v3_engine.h:397`, swaps keep the size, and centres have size ≤ K.) Every check on a search sits after the call returns (`cpp/v3_core.cpp:456-459,
476-480, 642-645, 689-692`). So no search is interrupted operationally in any run; on 𝒪 it is also P°'s search by
(GW-iii). ∎

## Relation to existing claims
- `W3-SAMP:PC` (i) is the special case "final islands, (C3) bridge checks of the final run" of (GW-iii); GW adds the
  calibration-phase checks, the preflights, the final local search and LS0, and the reported fields.
- (GW-iv) gives `W3-SAMP`'s convention a precise reading: its 𝒜 (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:39-41`) is the
  actual event, 𝒜 ⊆ 𝒜°, and every claim of the form P(completed ∩ ·) ≤ (bound on 𝒜° for potential quantities) holds
  with CAL applied to 𝓒° (T5 CAL-C). The guard's clock dependence enters only through {no check fires}.
