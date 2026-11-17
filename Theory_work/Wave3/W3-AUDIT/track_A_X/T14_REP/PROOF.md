# T14 · Lemma REP — PROOF v1 (DRAFT; code at pin 4676af6, paths relative to `Scripts/SMC_BVS/core/`)

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
(`cpp/v3_core.cpp:469`) returns a set of size at most max(k̂, 0) ≤ K, by a structural argument valid in any arithmetic
(council XR1 Opus F1; it does not use T9, whose (TDP-a), (TDP-b) assume EX-A or (H2-FP)):
(1) `mode_dp` sets k̂ = `kbest` only to some k ∈ {0, …, K} (the scan `for (int k = 0; k <= K; ++k)`,
`cpp/v3_start.h:220-224`), or leaves k̂ = −1.
(2) Each leaf of `rec(J, k̂)` (`cpp/v3_start.h:281-301`) is reached along edges that subtract the block size j from the
remaining size and accepts only r = 0, with codes c ∈ `arg[b][j]` ⊆ `codes_by_size[b][j]` (each of popcount j,
`cpp/v3_start.h:111, 201-209`); so its set has exactly k̂ elements. If no leaf is reached, `bestS` stays empty.
(3) `mode_tie_dp` returns only after the root check `feasible()` passes (`cpp/v3_start.h:261`), and keeps i in IN only
when `feasible()` holds with i added (`cpp/v3_start.h:263-268`); an i that fails is moved to OUT, and feasibility is
preserved because a witness path for (IN, OUT) cannot contain i. At the end IN ∪ OUT = {0, …, p − 1} and `feasible()`
holds, so some reachable tight path with block sizes summing to k̂ has, block by block, a code whose set contains IN's
members of that block and avoids OUT's; hence IN equals that path's set and |IN| = k̂.
The tests in (2), (3) are integer bookkeeping on whatever doubles `mode_dp` computed; no property of those doubles is used. K = `D.K` = min(p, n/2) in `int`
(`cpp/v3_score.h:40`) ≤ ⌊(2³¹ − 1)/2⌋ = 2³⁰ − 1. So `cap_ll` = ℓ_n + |m.S| ≤ 32 + 2³⁰ − 1 = 2³⁰ + 31 < 2³¹ − 1 = INT_MAX,
computed in `long long` (`cpp/v3_core.cpp:473`), and `o.ls0_ell < 0` is false (ℓ_n ≥ 3); the guard at
`cpp/v3_core.cpp:474` does not fire. ∎(REP-b)

## Conclusion
On every R-representable input both predicates lifted by A:IDEAL-W⁺ are false; so IDEAL-W⁺ costs nothing on any input the software can receive (n, p ≤ 2³¹ − 1). The
bounds use only R's integer `dim` limit, the shipped option values and the integer structure of `start_mode` (Step 3);
no arithmetic idealisation, memory or time assumption is used.
