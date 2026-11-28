# WP3 — the island: label-major kernel, addressed uniforms, threads, stores, checkpoints (Opus 5.5 builder)
Read BUILD_COMMON.md first. Branch: `exp/P1M-wp3-island`. This is the performance-critical heart of V-1M.

Inputs:
- ENGINEERING_SPEC §0-v2.4 (kernels), §0-v2.2, §3 (rules for the label-major round), §4.2, §6;
- `FEASIBILITY_fable.md` §1 (measured kernel; cost model c = M·c_s + c_f);
- the expert's working prototype `feas_bench.cpp`, at `/home/fb31/p1m_feas_bench/` or, after the move,
  `/home/fb31/SMC_Engineering_Department/bench/20261115-P1M-feas-bench/`. Read it; copy what you use into your branch
  with attribution;
- `core/cpp/v3_engine.h` (the four elementary steps, round order, resampling, bridge, terminal rounds, RB accumulation),
  `v3_ledger.h`, `v3_util.h`;
- `INTERFACES.md` as soon as WP1 writes it (hours). Start with the kernel prototype work, which does not depend on it.

Scope:
1. The island algorithm of `core/cpp/v3_engine.h` (init draws from π₀, T bridge stages with reweight + multinomial
   resampling + one round, L burn-in and Hm measured rounds with RB accumulation). Driven by **position-addressed
   uniforms** (INTERFACES), so that every execution order gives identical bytes.
2. **Label-major round** (spec §3 rules 1–4): tiles of X; products X_Aᵀx_j for the group's active set; per (support,
   label): score, odds, uniform, accept. Particles that move take a new sweep (factor M). Two arithmetic forms behind one
   interface: **bit form** (equals `v3::Scorer` bits; sorted-prefix reuse) and **class A** (bordered update, FMA, vector
   log/exp).
3. A **particle-major one-thread reference** of the same production algorithm (T3 reference).
4. Per-thread ledgers and stores, merged deterministically at stage ends; flat top store; no global score cache; logical
   counters; `island_best`.
5. RB accumulators with a declared chunked reduction order.
6. **Checkpoint/restart** at stage boundaries (spec §6), with a bit-identical resume (T6).
7. Tests: T3 (identical output hash for threads 1/2/3, group sizes, tile sizes; label-major vs particle-major); bit form
   vs `core/` on single steps; class A vs bit form agreement (≤ 1e-9 relative on scores).
8. **Measure** on Owls (≤ 3 threads; label each number): ns per (support, label) for both forms; M (sweeps per
   particle-round) on real islands at p = 10⁴; the cost of store offers; one island at p = 10⁴ and 10⁵ end to end.
   Compare with the planning values (90 ns, M = 3, c_f = 30 ns) and report the deviation.
