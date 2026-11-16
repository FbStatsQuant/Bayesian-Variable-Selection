# T5 · Lemma CAL-C — PROOF v2 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Fix a valid input; assume EX-A. Work with P° (T1 GW); Step 4 transfers to the actual fit.

## Step 1 — (CAL-a) which streams exist before calibration ends
Uniforms are read only through `VariateSource::u` (`RngSource`, `cpp/v3_engine.h:20-23`; the complete list of call sites
is in T1 GW PROOF Step 1), always through the engine's `vs` pointer or the argument of `draw_pi0`. An `RngSource` is
created and seeded at exactly three places: `cpp_start_draw` (`cpp/v3_core.cpp:239-241`; inspection helper
`v3_start_draw`, not called by `v3_fit`), the final run (`cpp/v3_core.cpp:444`) and `CalState::stream`
(`cpp/v3_core.cpp:594-597`), which seeds stream k on first use and reuses it after (diagnostic streams continue across
rebuild iterations, `cpp/v3_core.cpp:669`).

Before `v3_calibrate` returns, `v3_fit` runs preprocessing, the preflight, `v3_context`, `cpp_dup_components`, `v3_setup`
(`cpp_setup`: blocks, tables, start object, neighbour graph — `cpp/v3_core.cpp:272-305`, no `vs`), `cpp_cut_group`, and
`v3_calibrate` (`v3_fit.R:97-151`); none of these but `v3_calibrate` touches a `VariateSource`. Inside it, the engine's
`vs` is set only at `cpp/v3_core.cpp:627` (pilot: `sid = tier == 0 ? 0 : 5`, `cpp/v3_core.cpp:626`) and
`cpp/v3_core.cpp:668` (diagnostics: `sid = (tier == 0 ? 0 : 5) + r`, r = 1..4, `cpp/v3_core.cpp:666-667`), always before
`run_island_s` (`cpp/v3_core.cpp:632, 670`); the local searches, `cpp_cal_V`, `cpp_build_grid` and `cpp_cal_export` read
no uniform. `v3_calibrate` calls `v3_cal_tier` with tier e ∈ {0, 1} only (`v3_calib.R:149-158`: start at `tier = 0`,
at most one escalation to `e <- 1`). So the streams used are k ∈ {0, 5} ∪ {1, …, 4} ∪ {6, …, 9} ⊆ {0, …, 9}. The final
streams are created inside `cpp_final_run` at `cpp/v3_core.cpp:444`, as `seed_stream(seed, 9 + r)`, r = 1..`o.islands`.

## Step 2 — (CAL-b) 𝓒° is a function of (X, y) and U^{(0)}, …, U^{(9)}
In P° every check's Boolean is FALSE, so by T1 (GW-i), (GW-iv) every statistical field is computed from the input, the
options and earlier statistical fields; the only random inputs reaching statistical fields are uniforms (Step 1), and
the allocation reaches only `fit$allocation` and the normalised local `allocation`, which `v3_calibrate` does not
receive (`v3_fit.R:150-151` passes `setup`, `seed`, `preflight`, `runtime`, `grid_fallback`; `preflight` and `runtime`
are check bodies and the guard). The seed enters `v3_calibrate` only through `cpp_cal_new(setup$ptr, cseed, …)` →
`c->seed` (`v3_calib.R:146-148`; `cpp/v3_core.cpp:606`), i.e. only as the seed of the streams, and through
`calibration_seed` (`v3_calib.R:171`), a copy of the input. The `setup` object is a function of (X, y) (`v3_setup.R:67-77`;
no stream). Hence 𝓒° — every statistical field of `v3_calibrate`'s return value (`v3_calib.R:171-190`) — is
Ψ(X, y, seed, U^{(0)}, …, U^{(9)}) (the seed entering only as the label `calibration_seed`, and ⊥ when `v3_calibrate` is not
called, a decision that depends on (X, y) only: `v3_fit.R:99-138`).

## Step 3 — measurability (bounded computation)
The calibration consumes a number of uniforms bounded by a deterministic function of (n, p): at most 2 tiers; per tier
one pilot island and at most ℓ_n rebuild iterations (`v3_calib.R:85`) of 4 diagnostic islands; each island has
H_e particles (`v3_calib.R:11`), at most T_e stages (pilot: every non-terminal stage
advances φ by ≥ 1/T_e, `cpp/v3_calib.h:38-42`; diagnostics: a grid of ≤ T_e intervals, `cpp/v3_calib.h:94`, W3-SAMP CC6),
L + Hm rounds at φ = 1; each round has p + B + 2 steps (`cpp/v3_engine.h:72`) each using a bounded number of uniforms
(`cpp/v3_engine.h:129, 150-151, 156, 167, 171, 177, 189`), the order shuffle uses p + B + 1 uniforms
(`cpp/v3_engine.h:199`), resampling N (`cpp/v3_engine.h:250`), and each π₀ draw at most 1 + 2J (`cpp/v3_start.h:158-176`).
So Ψ depends on finitely many coordinates of each U^{(k)}, and is obtained from them and (X, y) by a computation whose
length is bounded by a function of (n, p); each step is a Borel operation (arithmetic, exp, log, floor) or a branch on a
comparison of Borel functions. A finite composition of such steps is Borel, so Ψ is measurable (this is the argument of
W1-N1 Lemma B (MEAS) for one island, `Theory_work/Wave1/W1-N1/STATEMENT.md:83-85`, applied to the finitely many islands
and searches of the calibration). 𝒜° = {𝓒° ≠ ⊥ and status "ok"} ∈ σ(𝓒°) since status is a field of 𝓒°.

## Step 4 — (CAL-c) the final run's settings and randomness
`v3_final_run(setup, frozen, seed, runtime, ls0)` (`v3_fit.R:162`; `v3_run.R:223-228`) computes
`ro <- v3_run_settings(setup, frozen, ls0)`: N = `b$tiers$N[tier + 1]`, L = `b$L`, `measured_rounds = 4L`,
`islands = 4L`, `ell = b$ell`, `cache_capacity = 500 p`, and the LS0 options (`v3_run.R:88-104`), with
`b = setup$budgets = v3_budgets(n, p)` (`v3_setup.R:68`) and `tier = frozen$tier`. `cpp_final_run` receives
`frozen$grid`, `ro`, `seed`, `frozen$inherited`, `runtime` (`v3_run.R:227`). `frozen` is `out$frozen` of
`v3_calibrate` (`v3_fit.R:161`; built at `v3_calib.R:184-190` from the last tier's grid, tier e, its N and L, and
`ex$inherited`), a field of 𝓒°. Inside `cpp_final_run` the islands draw only from `RngSource` seeded
`(seed, 9 + r)` (`cpp/v3_core.cpp:443-446`); the final local search and LS0 read no uniform (T3 OPC Step 2). So every
setting is a function of 𝓒° and (n, p, options), the final run's randomness is U^{(10)}, …, U^{(13)}, and `setup`
depends on (X, y) only.

## Step 5 — (CAL-d) the actual fit
T1 (GW-iv): 𝒜 = 𝒜° ∩ G ⊆ 𝒜°. On G no check evaluated before `v3_calibrate` returns fires, so T1's induction (PROOF
Steps 3–4, the (⊇) part of Step 4) runs to that return with every Boolean FALSE, and the actual output's statistical
fields equal P°'s. So on 𝒜 ⊆ G the actual record is 𝓒°. ∎

## Where the flag bites
See STATEMENT, "Where the T1 flag bites": the conditional arguments of W3-SAMP are valid for (𝒜°, 𝓒°) by (CAL-b), and
P-START's source states its bound for every event (`Theory_work/Wave3/W3-START2-R/STATEMENT.md:241-244`), so it holds on
𝒜°. P-OVL is T8.
