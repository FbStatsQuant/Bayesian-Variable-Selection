# CSL1 reply (Codex gpt-6.1-sol high, blind, delegate 45257664; 2026-11-16) — verbatim

Part 1: **LOCK.** No statement changes required. C1 supplies the amended inventory completeness and unreachable-site facts that DLV-0 consumes, under the stated configuration and premises.

Part 2: **VERIFIED WITH AMENDMENTS.** Two editorial corrections to the proof are required below. No uncovered reachable no-estimates exit was found.

The core pin check passed: `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` returned 0. Review was read-only.

1. **E — The exhaustive grep list omits a rethrow.** C1 PROOF.md:36 says it lists every explicit `throw`, but omits the bare `throw;` at v3_core.cpp:209. **Fix:** add `:209` and classify it as off the fit call graph: it belongs to the auxiliary `cpp_start` constructor. This does not change coverage or reachability.

2. **E — The additional-node paragraph overstates execution frequency.** C1 PROOF.md:47 introduces its nodes as called “on every non-early-exit run.” `cpp_cut_group` runs only on the SMC branch, while `cpp_runtime_report` and `cpp_numerical_routes` have conditional calls in `finish`. **Fix:** say “Additional nodes on the fit call graph, reached under the following conditions.” The individual node analyses remain valid.

The explicitly requested checks passed:

- **A-7 completeness.** v3_preflight (v3_fit.R:26) has exactly the described rejection conditions. Exact preflight checks its three memory components and `exact_count × measured seconds`; SMC preflight checks data/Gram/correlation/distance, tables, convolution, cache, stores, populations and, under the default LS0 configuration, `ls0_archive` plus LS0 seconds. There is no additional default preflight rejection predicate. Escalation repeats the SMC test with tier-1 populations. Its LS0 time cannot newly reject after an initial pass because `time_fun(K)` is cached and the time expression is tier-independent. All five named options cover the method-specific option reads relevant here.

- **DLV-0 (E2) excludes A-7.** Q5_dlv0.md:59 at e78a1055 was inspected using `git show`. Its imported allocation matches FIN s6_delivery.tex:37 (Theory_work/Wave1C/FINAL/sections/s6_delivery.tex): with s = ℓ_n + K + 1, q = p + p²/4, the coded time is 2sqŝ_K, and the archive is A = (2s+4)(12K+256) + 96s + 4(8W+4K+96) + 4096. FIN requires memory at least P_e + A for both tiers. The **MACH wall-time premise**, applied to the deterministic operation bound U_K for the complete measured interval, gives ŝ_K ≤ (τU_K + τ₀)/200; hence 2sqŝ_K ≤ P̄_LS0. The benchmark constructs and sorts 200 models of exactly size K: its column subcontext preserves that capacity. FIN's envelopes are evaluated at (n, p_raw); retained p ≤ p_raw, and the LS0 factors are nondecreasing. SMC checks memory before timing; exact preflight times before its rejection check. Both rejection tests use strict `>`, so equality passes.

- **Return and invariant checks.** The §1.1 success assignments and no-estimates returns match the code. The §1.3 nodes introduce only the already classified pointer, conversion, allocation and environment possibilities. D2's escalation argument holds; S.3 (i)–(vii), including the additional primed steps, hold at the relocated lines. Internally constructed pointers, models, provenance, grids and record shapes exclude `get_holder` and the implicit-error class under the stated premises. The start-mode cap is 10⁶; T4's encoding and T9's root-feasibility result exclude its other throw, with execution failures handled separately by IDEAL-W/MACH.

- **Representability and scope.** For R-representable inputs, ℓ_n ≤ 32 and |S̃₀| ≤ K ≤ 2³⁰ − 1, excluding X7/X8 in the default configuration. This does not assert that other native integer arithmetic is safe without IDEAL-W. C1-c correctly identifies **L1-R's preflight-seconds bound** as exact-branch only; the additional SMC LS0 preflight-seconds bound comes from FIN A4.

CSL1-VERDICT: C1 lock=LOCK, check=VERIFIED WITH AMENDMENTS; A7-complete=yes; DLV0-E2-excludes=yes
