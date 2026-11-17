# T14 · Lemma REP — PROOF v0 (DRAFT; code at pin 4676af6, paths relative to `Scripts/SMC_BVS/core/`)

Fix an R-representable input that reaches the LS0 settings, i.e. a sampler-branch fit that has passed preprocessing,
the preflight, setup and calibration (otherwise neither site is evaluated).

## Step 1 — the dimensions
`v3_preprocess` sets n <- `nrow(X)`, p_raw <- `ncol(X)`, kept ⊆ {1..p_raw}, p = `length(kept)` (`v3_preprocess.R:103,
111-113`), with n ≥ 3 and p ≥ 1 on a fit that continues (`v3_preprocess.R:106-107, 114`). R matrix dimensions are R
integers, so n, p_raw ≤ 2³¹ − 1, hence p ≤ 2³¹ − 1. The context is built from the kept columns (`v3_fit.R:118`), and
`cpp_context` reads n and p as `int` (`cpp/v3_core.cpp:92`) and returns them (`ctx$n`, `ctx$p`, `cpp/v3_core.cpp:103`).

## Step 2 — (REP-a), the base-cap validator
`v3_setup` computes `b <- v3_budgets(ctx$n, ctx$p)` (`v3_setup.R:68`); `v3_budgets` converts both to double
(`v3_preprocess.R:20`) and sets `ell <- v3_ceil_log2(n + p + 1)` (`v3_preprocess.R:23`), the smallest c with 2^c ≥ x
(`v3_preprocess.R:15`; exact in double for integers below 2⁵³). Since 5 ≤ n + p + 1 ≤ 2³² − 1, ℓ_n ∈ [3, 32]. In
`v3_run_settings` with the option unset, `le <- b$ell` (`v3_run.R:95`); the validator (`v3_run.R:96-97`) stops only if
`le` is non-numeric, not of length 1, non-finite, negative, non-integral or > 10⁶; `le` is a finite integral double in
[3, 32], so none holds. `ro$ls0_ell <- as.integer(le)` (`v3_run.R:98`). ∎(REP-a)

## Step 3 — (REP-b), the cap-range guard
`o.ls0_ell = as<int>(ro["ls0_ell"])` = ℓ_n (`cpp/v3_core.cpp:402`); `o.ls0_cap_plus_mode` is true because
`ro$ls0_cap` = "ell_n_plus_mode" (`v3_run.R:101`; `cpp/v3_core.cpp:404`). `m = start_mode(st, 1000000, true)`
(`cpp/v3_core.cpp:469`) returns a set of size k̂ ≤ K: every candidate of the enumeration and of the tie-aware fallback has
size k̂, and k̂ ranges over 0..K (`cpp/v3_start.h:220-224`; T9 (TDP-a), (TDP-b)). K = `D.K` = min(p, n/2) in `int`
(`cpp/v3_score.h:40`) ≤ ⌊(2³¹ − 1)/2⌋ = 2³⁰ − 1. So `cap_ll` = ℓ_n + |m.S| ≤ 32 + 2³⁰ − 1 = 2³⁰ + 31 < 2³¹ − 1 = INT_MAX,
computed in `long long` (`cpp/v3_core.cpp:473`), and `o.ls0_ell < 0` is false (ℓ_n ≥ 3); the guard at
`cpp/v3_core.cpp:474` does not fire. ∎(REP-b)

## Conclusion
On every R-representable input both predicates lifted by A:IDEAL-W⁺ are false; so IDEAL-W⁺ costs nothing on any input the software can receive (n, p ≤ 2³¹ − 1). The
bounds use only R's integer `dim` limit and the shipped option values; no memory or time assumption is used.
