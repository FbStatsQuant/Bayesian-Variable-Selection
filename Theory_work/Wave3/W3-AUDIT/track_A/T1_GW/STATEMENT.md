# T1 · Lemma GW (GUARD-W: the run-time guard only stops) — STATEMENT v4 (draft, not locked)

Track A item T1 (`AUDIT.md` §6; CHECKPOINT_1 annex order 1). Tier B (code reading, no key lemma). **Lean target: no**
(a code fact). Blocks rows 3.1, 3.5, 3.6.

## Source of the premise
- GUARD-W as named: "**GUARD-W** stop-only guard (operational interruption ⇒ no output)"; same line: "**complete
  scans** no operational interruption of any search"; "D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) in potential-run notation"
  (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:86`).
- Used as: "delivered records are identified with potential ones on 𝒪 by GUARD-W (TLF:86; audit open, not discharged
  here)" (`Theory_work/Wave1/W1-N1/STATEMENT.md:86-88`); "The full GUARD-W delivery audit (only Lemma PC's comparison)"
  not claimed (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:182`); implementation premise of RM-0
  (`Theory_work/Wave3/W3-RM/STATEMENT.md:55`) and of RM2-R (`Theory_work/Wave3/W3-RM2/STATEMENT.md:57`); 𝒜 in code
  terms (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:39-41`) and CAL (`Theory_work/Wave1/W1-N1/STATEMENT.md:79`).
- Partial discharge already checked: `W3-SAMP:PC` (final islands and reported fields only;
  `Theory_work/Wave3/W3-SAMP/lemmas/PC_completed.md:10-20`).

## Code of record
`Scripts/SMC_BVS/core/` at the registry method pin **4676af6** (`method_commit` of `W3-SAMP:CC`, `:PC`, …); the core is
unchanged from the pin to this branch's HEAD (`git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`, checked
2026-11-16). Paths below are relative to `Scripts/SMC_BVS/core/`. Configuration: the shipped `v3_fit(X, y, seed,
allocation)` with `ls0 = TRUE` and the default options (`v3_fit.R:73`).

## Definitions
- **Operational checks** (the complete list at the pin):
  (C1) memory/time preflight before any fit work, `if (pf$exceeds)` (`v3_fit.R:115-117`);
  (C2) preflight before the calibration escalation, `preflight(1)` = `pf_fun(1)` (`v3_calib.R:157`; `v3_fit.R:144-148`);
  (C3) run-time guard `RuntimeGuard::check` (`cpp/v3_runtime.h:21-27`) at: every bridge stage of every island
  (`cpp/v3_engine.h:335-338`; islands of the pilot `cpp/v3_core.cpp:632`, the diagnostics `:670`, the final run `:446`);
  the pilot and diagnostic local searches (`cpp/v3_core.cpp:645`, `:692`); grid construction (`v3_calib.R:75-76` via
  `cpp_runtime_check`, `cpp/v3_core.cpp:770-775`); the final local search (`cpp/v3_core.cpp:459`); LS0
  (`cpp/v3_core.cpp:480`).
  A check's **body** is the computation of its Boolean (for (C1), (C2): `v3_preflight`, including its timing benchmark;
  for (C3): `check`); the check **fires** if the Boolean is TRUE. All (C3) sites share one `RuntimeGuard` object for the
  whole fit (`v3_fit.R:96, 150, 162`).
- **Fields.** A *field* is a leaf: an R list element, a C++ struct member or a local variable.
- **Booleans.** A check's Boolean is the value of the **whole** check expression at its call site, null test of the
  guard included: `pf$exceeds` (`v3_fit.R:117`); `!is.null(preflight) && isTRUE(preflight(1))` (`v3_calib.R:157`);
  `guard && guard->check(…)`, `E.guard && E.guard->check(…)`, `c->guard && c->guard->check(…)`
  (`cpp/v3_engine.h:335`; `cpp/v3_core.cpp:459, 480, 645, 692`); `!is.null(runtime) && cpp_runtime_check(…)`
  (`v3_calib.R:75-76`). The guard handle is non-null on every path after `v3_fit.R:96`.
- **Internal values** of the checks: every value a check body computes or writes, and the guard itself: the handle
  `runtime` and its C++ pointers (`guard`, `E.guard`, `c->guard`), every `RuntimeGuard` member (`start`,
  `elapsed_before`, `allocation`, `exceeded`, `records`; `cpp/v3_runtime.h:14-17`), the preflight record `pf` and its
  fields, `tcache` and the benchmark output. (Values a body only *reads*, such as n, p or `ev`, are not internal values.)
- **Operational fields** 𝒱_op: the closure under assignment of the fields assigned from a clock reading, a
  machine-environment reading (`Sys.getenv`, `R.version`, `/proc/self/status`) or an internal value — where the value of
  a Boolean at its call site is a **cut**: it, and what is computed from it alone (e.g. a status set to
  `"resource_limit"`, `g$resource_limit`, `res.partial`), are not counted as assigned from the internal values.
  **Statistical state** = the fields not in 𝒱_op. (So the `seconds` fields of an island record are operational; its
  `logZ`, populations and `pip` are statistical.)
- **Output event** 𝒪 := {the fit returns `estimates_available = TRUE`}: {`status == "completed"`} on the sampler branch
  (`v3_run.R:143-149, 218`; `v3_fit.R:171`), {`status == "exact"`} on the enumeration branch (`v3_fit.R:125-129`). A run
  that ends in an R error returns no fit object and is not in 𝒪.
- **Potential fit** P°(X, y, seed, allocation): the same program, in which every check body is executed as written and
  its Boolean is then replaced by FALSE. 𝒪° is its output event. 𝓒° := the statistical fields of P°'s `v3_calibrate`
  output (status, tiers, frozen object, inherited models, ledger), and 𝓒° := ⊥ ("not called") on runs where P° does not
  call `v3_calibrate` (exact branch, preprocessing exits, setup failure, invalid seed). 𝒜° := {𝓒° ≠ ⊥ and its status is
  "ok"}; 𝒜 := the same event for the actual fit. G := {no check evaluated before `v3_calibrate` returns — or in the whole
  run if it is not called — fires}; (C1) is included.

## Lemma GW
Assume EX-A (exact arithmetic; `Theory_work/Wave1/W1-N1/STATEMENT.md:70`). For every valid input (X, y, seed,
allocation) of the shipped `v3_fit` and every sequence of clock and environment readings:

**(GW-i) Stop-only.** Every check body terminates normally and draws no uniform from any stream. From the statistical
state it reads only n, p, the budgets, the branch, the tier, `ls0_worst_case`, the normalised allocation, the
preprocessed (X, y) columns (timing benchmark, read only) and the event context passed to `check` (the engine's `ev` at
bridge stages; otherwise one built from the tier and the iteration or grid index); it writes only internal values.
Every statistical field is computed from the input (X, y, seed, allocation, options), earlier statistical fields and
Booleans only.

**(GW-ii) A fired check gives no output.** If some check fires, the run is not in 𝒪: its status is
`"resource_limit"`, every estimate field (`log_Z`, `log_Z_r`, `log_Z_lower95`, `log_Z_rel_m0`, `log_Z_r_rel_m0`,
`pip_primary`, `pip_r`, `mpm`) is NA (`v3_run.R:109-114`, `v3_fit.R:85`), and any HPM it reports is labelled
`hpm_incomplete = TRUE` or is absent.

**(GW-iii) Completed runs are potential runs.** 𝒪 = 𝒪° ∩ {no check fires}, and on 𝒪 the statistical state at every
point of the execution equals P°'s on the same input: in particular the statistical fields of 𝓒 (status included), of
the frozen object, of every final island record, of the final local-search and LS0 archives, of the final ledger, and
every reported statistical field.

**(GW-iv) Interface.** P°'s statistical state is a function of the input (X, y, seed, allocation, options). The
allocation enters statistical state only as `fit$allocation` and the normalised local `allocation` (`v3_fit.R:92-95`),
which is read only by check bodies, by `cpp_runtime_new` (whose output, the guard, is operational) and by `v3_fit.R:95`;
so every other statistical field of P° is a function of (X, y, seed) and the options. 𝒜° ∈ σ(𝓒°). Moreover
𝒜 = 𝒜° ∩ G ⊆ 𝒜°, 𝒪 ⊆ 𝒪°, and for every event A defined by statistical state, with A° the same event for P°:
𝒪 ∩ A ⊆ 𝒪° ∩ A° (pathwise). The "potential uninterrupted record" of `W1-N1` §2 and the potential run 𝒪̄ of TLF:86 are
P°'s. `W3-SAMP`'s "𝒜 ∈ σ(𝓒)" (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:39-41`) holds for the potential pair (𝒜°, 𝓒°);
for the actual 𝒜 it is replaced by 𝒜 ⊆ 𝒜°. That 𝓒° depends on the data and streams 0–9 only (CAL) is T5 (CAL-C), not
this lemma.

**(GW-v) Complete scans.** No check is evaluated inside a local search (`cpp/v3_engine.h:379-419`); checks run only
after a search returns. So no search of any run is interrupted operationally, and on 𝒪 every search that P° runs was
run to its own termination rule.

## Not claimed
- Anything about binary64 (EX-A is an idealisation); machine failures (out-of-memory kill, signal) — premise MACH.
- A probability model for clock readings. (GW-i)–(GW-v) are pathwise, for every clock sequence. If the clock is
  jointly measurable with the streams, 𝒪 is an event and P(𝒪 ∩ A) ≤ P(𝒪° ∩ A°); otherwise the transfer holds as an
  outer-probability bound. The core statements use only this upper-bound direction (TLF Output contract: "Bounds
  transfer by intersection with 𝒪", `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md:74`).
- `ls0 = FALSE` (v3 mode): (GW-ii)'s NA clause is coded for v3.1 only (`v3_run.R:106-108`).
- That 𝒪 has high probability (delivery).
- Concurrency (the core at the pin is serial: `cpp/v3_core.cpp:443-452`).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM | track A T1 | `AUDIT.md` §6 T1 | — |
| v2 | defs, (GW-i)–(GW-iii) | EQUAL in substance (definitions repaired: 𝒱_op, P° executes check bodies, `peak_memory_kb` and environment readings) | LC1 #1–3, #8 | `reviews/LC1_reply_opus.md` | pending (gate) |
| v2 | (GW-iv), (GW-v) | STRONGER (new clauses, proved from Steps 1–3) | LC1 #4, #9 | `reviews/LC1_reply_opus.md` | pending (gate) |
| v2 | (GW-i) "check bodies terminate normally" | STRONGER (retagged from EQUAL) | LC1r #12 | `reviews/LC1r_reply_opus.md` | pending (gate) |
| v3 | fields, 𝒱_op, statistical state, (GW-i) | EQUAL in substance (leaf-field granularity; Booleans not operational; (GW-i) reads/writes stated exactly) | LC1r #2, #6 | `reviews/LC1r_reply_opus.md` | pending (gate) |
| v3 | (GW-iv) | WEAKER as to the input (allocation now named, reaching only `fit$allocation`); STRONGER (𝒜° ∈ σ(𝓒°)); 𝒜-equality corrected to include (C1) | LC1r #1, #3, #4 | `reviews/LC1r_reply_opus.md` | pending (gate) |
| v4 | defs (Booleans = whole call-site expression; internal values incl. the guard handle and all members; cut rule), (GW-i), (GW-iii) wording | EQUAL in substance | LC1r2 #1, #4, #5 | `reviews/LC1r2_reply_opus.md` | pending (gate) |
| v4 | (GW-iv) allocation clause; 𝓒° = ⊥ when not called; G defined | EQUAL in substance (wording repaired) | LC1r2 #2, #3 | `reviews/LC1r2_reply_opus.md` | pending (gate) |

Note on tags: (GW-iv) and (GW-v) are not CP1 target clauses (this is a Tier B code lemma with no CP1); the WEAKER tag of
the v3 (GW-iv) row (input now names the allocation) needs only the statement-change check at the gate.
