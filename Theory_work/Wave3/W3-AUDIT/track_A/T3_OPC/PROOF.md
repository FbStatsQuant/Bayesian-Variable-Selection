# T3 · Lemma OPC — PROOF v1 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Fix a valid input on the sampler branch and assume EX-A. The argument applies verbatim to the actual fit and to P°
(T1 GW: P° differs only in that every check's Boolean is FALSE).

## Step 0 — the configuration reaches the C++ run
`v3_fit` has `ls0 = getOption("v3.ls0", TRUE)` (`v3_fit.R:73`) and passes it to `v3_final_run` (`v3_fit.R:162`), which
builds `ro <- v3_run_settings(setup, frozen, ls0)` (`v3_run.R:226`). With `ls0 = TRUE` and the options unset,
`v3_run_settings` sets `ro$ls0 <- TRUE`, `ro$ls0_ell <- b$ell` (the validation at `v3_run.R:96-97` passes for an integer
in [0, 10⁶]), `ro$ls0_tie_dp <- TRUE` and `ro$ls0_cap <- "ell_n_plus_mode"` (`v3_run.R:93-102`); `b$ell` =
`v3_ceil_log2(n + p + 1)` = ℓ_n (`v3_preprocess.R:15, 23`). In `cpp_final_run` these give `o.ls0 = true`,
`o.ls0_tie_dp = true`, `o.ls0_ell = ℓ_n`, `o.ls0_cap_plus_mode = true` (`cpp/v3_core.cpp:400-404`).

## Step 1 — (OPC-a) LS0 runs on every completed run
The only assignments to `status` in `cpp_final_run` are the initialisation to `"completed"` and the changes to
`"resource_limit"` or `"numerical_failure"` (`cpp/v3_core.cpp:413, 451, 459, 480, 484`); none sets it back. So if the
final status is `"completed"`, none of `:451, 459, 480, 484` executed, and `status == "completed"` held at the gates
`cpp/v3_core.cpp:453` and `cpp/v3_core.cpp:465`. Hence the final local search ran (`cpp/v3_core.cpp:456`) and then the
LS0 block ran (`cpp/v3_core.cpp:465-481`): `m = start_mode(st, 1000000, o.ls0_tie_dp)` (`cpp/v3_core.cpp:469`), so the
centre is `m.S` = S̃₀; the cap is `o.ls0_ell + m.S.size()` = ℓ_n + |S̃₀| (`cpp/v3_core.cpp:473-475`; the range check at
`cpp/v3_core.cpp:474` passes since ℓ_n + |S̃₀| ≤ ℓ_n + K < 2³¹ − 1); and
`E.local_search(m.S, ls0_cap, o.tier, true, -1, PH_LS0)` is called once (`cpp/v3_core.cpp:476`) with
`emit_centre = true`. No other call with phase `PH_LS0` exists.

## Step 2 — (OPC-b) it is the abstract search, run to its end
*No uniforms.* `local_search` (`cpp/v3_engine.h:379-419`), `eval` (`cpp/v3_engine.h:89-101`), `start_mode`
(`cpp/v3_start.h:271`), `Start::comp`, `Scorer::score`, the cache and the ledger contain no `VariateSource::u` call (the
complete list of uniform reads is in T1 GW, PROOF Step 1).

*Not interrupted.* By T1 (GW-v), no check is evaluated inside a search; the LS0 check (`cpp/v3_core.cpp:480`) runs after
the call returns, and on {status = "completed"} it did not fire. A `NumericalFailure` inside would have set
`"numerical_failure"` (`cpp/v3_core.cpp:483-484`), and any other exception ends the R call without a fit; neither
happened. So the call returned through one of its own exits (`cpp/v3_engine.h:410`, `cpp/v3_engine.h:414`).

*Same models, same order.* Under EX-A, `eval` sets F = log ϖ(|S|) + log m(S) whether log m comes from the scorer or the
cache: the cache returns a stored value only for the same model (`find` compares the hash and the full set,
`cpp/v3_score.h:274-282`), and that value was computed by the same scorer (`cpp/v3_engine.h:91-94`). The code's scan
(`cpp/v3_engine.h:394-406`): flips j = 0..p − 1 — deletion if j ∈ C, addition only if |C| < K (`cpp/v3_engine.h:396-397`)
— then swaps (j ∈ C ascending) × (l ∉ C ascending); every scanned model is evaluated (`consider`,
`cpp/v3_engine.h:389-393`). The best neighbour maximises F with exact ties to the lexicographically smaller list
(`cpp/v3_engine.h:392`; `lex_less`, `cpp/v3_util.h:117-119`; the scan order does not matter for the arg-max). A move
happens iff `best.F > C.F` (`cpp/v3_engine.h:408`); if a strict improvement is found when `moves ≥ ell` the search stops
after that scan (`cpp/v3_engine.h:409-410`), else it moves (`cpp/v3_engine.h:412`); with no strict improvement it stops
(`cpp/v3_engine.h:413-414`). So at most ℓ moves are made, a further scan follows the ℓ-th move, and the search stops at
the first scan without strict improvement: these are the rules of LS(c, ℓ) (C-GROW STATEMENT §0 "Method",
`Theory_work/Wave1C/C-GROW/STATEMENT.md:68-71`). The centre is evaluated first (`cpp/v3_engine.h:382`). By induction
over scans, the code's centres, scans and evaluated models coincide with LS(S̃₀, ℓ_n + |S̃₀|)'s, and the evaluated set is
Scored(S̃₀, ℓ_n + |S̃₀|). Since F, K, p and S̃₀ (built from `st`, i.e. from C(X) and the tables scored on (X, y)) are
functions of (X, y), so is this set.

## Step 3 — (OPC-c) its models enter the final comparison
Every evaluation in the LS0 call has `emit = true` (the centre by `emit_centre = true`, `cpp/v3_engine.h:382`; the scan
by the default, `cpp/v3_engine.h:391`), so `eval` calls `led->event(…, fresh || !cache, …)` (`cpp/v3_engine.h:98-99`) on
the final run's ledger (`E.led = &led`, `cpp/v3_core.cpp:411`). A fresh event offers the model to the HPM and the stores
(`cpp/v3_ledger.h:104-113`, `cpp/v3_ledger.h:84-94`). A non-fresh event is a cache hit, i.e. the model was evaluated
earlier in this final run (the cache is created empty at `cpp/v3_core.cpp:409`), and was offered then: this is
`W3-SAMP:CC` CC2 ("CODE-CHECKED"; `Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md:40-62`, which treats the one
`emit = false` call, the final local search's centre, and cache clears). So Scored(S̃₀, ℓ_n + |S̃₀|) ⊆ 𝓜. The ledger is
reported after LS0 (`ledger_to_list`, `cpp/v3_core.cpp:510`), and on a completed run `out$hpm <- led$hpm$model`
(`v3_run.R:142`), the running `hpm_better`-maximum (`cpp/v3_ledger.h:84-88`; order `cpp/v3_util.h:121-126`). Hence
Ŝ⁺ = the `hpm_better`-maximum of 𝓜 (CC2).

## Step 4 — (OPC-d) operational closure
On {status = "completed"}, Steps 2–3 give {S₀ ∈ Scored(S̃₀, ℓ_n + |S̃₀|)} ⊆ {S₀ ∈ 𝓜}. If π(S₀) > ½ then S₀ ∈ Ω and,
since e^F ∝ π on Ω (CC2: F = log ϖ + log m, `cpp/v3_engine.h:97`), F(S₀) > F(S) for every S ∈ Ω ∖ {S₀}; with 𝓜 ⊆ Ω
(CC5) and S₀ ∈ 𝓜, the `hpm_better`-maximum of 𝓜 is S₀. So on the sampler branch
𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ, and 𝒦_n is a function of (X, y) by Step 2. The same holds for P° on 𝒪°, which
gives [OP] of `W1-GEN:L5` in its potential-run form: 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ 𝒦_nᶜ on the sampler branch. ∎

## Re-check of `W1-GEN:L5` [OP] (the item's "re-check" part)
[OP]'s direct argument (`Theory_work/Wave1/W1-GEN/lemmas/L5_assembly.md:11-16`) has four steps; against the code of
record: "GUARD-W excludes an interrupted LS0" — now T1 (GW-iii), (GW-v); "OP-LS0 gives execution of LS0 with the
prescribed emitted centre (e4) and completed scans" — Steps 1–2 here, with e4 replaced by `W3-RM:E4` (maximiser, no lex
claim) as row 3.1 already does; "every model LS0 scores joins the all-scored set" — Step 3; "LS0 reads no uniforms, so
the models it scores are a deterministic function of the data" — Step 2. [OP]'s statement is correct for the code of
record on the sampler branch. One correction to its text: L5 Note (0) says "LS0 is not in production code"
(`Theory_work/Wave1/W1-GEN/lemmas/L5_assembly.md:44-45`); at the pin it is (`cpp/v3_core.cpp:465-481`, shipped default
`ls0 = TRUE`). This does not affect the inclusion.
