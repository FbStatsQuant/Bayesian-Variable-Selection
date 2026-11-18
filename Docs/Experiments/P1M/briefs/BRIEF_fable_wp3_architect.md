# Brief — WP3 architect (Fable 5.2, high; owner-approved 11-16, RECOVERY_OPTIONS (b))

You are the **WP3 architect** of SMC - Engineering, a child of the Engineering manager. About **3 working days**.
The owner approved you to give the island kernel (WP3) a second, senior design opinion **and** to attack the largest
remaining cost lever of the 1M run. You advise and prototype; WP3's builder (Opus) owns the production code.

## Why you exist (read first)
- `Docs/Experiments/P1M/RECOVERY_OPTIONS.md` — option (b) and its 11-16 update.
- `Docs/Experiments/P1M/results/WP3_ISLAND_SPR.md`, `WP3_ROUNDS_SPR.md`, `WP3_LEVERS_SPR.md` — the measured costs on NOTS
  Sapphire Rapids (Xeon 8468, 2 sockets × 48 cores × 2 threads). Headline: at p = 10⁶, G = 256, one island per socket,
  the late rounds cost ≈ 288 ns·CPU per (support, label) pair, 1.44× the plan (200). About half of a late round is
  per-pass overhead (walk, build, orders, apply); the products are ≈ 44 ns/pair after WP3's 4-column blocking.
  WP3 has since built L5 (π₀ draw, 8-lane Fisher–Yates, no row zero-fill, parallel apply): ESTIMATE ≈ 215 ns·CPU/pair,
  not yet measured on SPR.
- `Docs/Experiments/P1M/DECISIONS.md` — D-18…D-26 and **H-9** (budget ≈ 28.3k core-h; AR-weak at 1M is the first
  buy-back if per-pass costs fall; an unpriced risk is M = pairs per step 3.9–4.1 vs 3).

## Code and contract
- Engine: `Scripts/SMC_BVS/engine_v4/` on branch `exp/P1M-engine` (WP3 island code under `src/island/`,
  `include/v4/island/`; bench `tools/bench_island.cpp`). Open PR #26 (`exp/P1M-wp3-island4`) is under re-check.
- Contract: `Docs/Experiments/P1M/INTERFACES.md` (binding; v0.1.11). Design: `Docs/Experiments/P1M/WP3_DESIGN.md`.
- Spec: `Docs/Experiments/P1M/ENGINEERING_SPEC.md` §0-v3 (wins), §0-v2. Reviews: `Docs/Experiments/P1M/reviews/PR21*`,
  `PR24*`, `PR26*`.

## Scope (in priority order)
1. **Cost architecture of the island at 10⁶ (the NUMA / memory / per-pass lever).** Model where a late 10⁶ round spends
   its time (products, odds, walk, build, orders, apply, store) on SPR, from the measured per-round counters, and
   propose the design changes that bring the cost per pair to ≤ 200 ns·CPU (or say honestly that it cannot, and why).
   Candidates to judge, not a list to implement: X / score-row layout and blocking for L1/L2 reuse, the tile size,
   G > 256 with an inverse-order-only scheme (WP3's proposal), fusing walk/build, socket-local placement and first
   touch, SMT (hyperthreads) on or off per island, the per-pass synchronisation. Every proposal must keep the output
   **bit-identical** (class A arithmetic, addressed uniforms, T3 thread invariance) unless you say explicitly that it
   needs a contract change.
2. **Second design opinion on what is built**: deterministic stores under threads, addressed sampling, checkpoints and
   restart, the memory plan. Find design-level risks the PR reviews (line-level) would miss.
3. **Work split for builders 6–7.** The owner will add two builders once your design lands (~day 3). Propose how to split
   the remaining WP3/WP4/T5 work so they start on a settled design: packages, interfaces, order.

## Rules
- Measure, don't estimate, where you can: Owls only, `nice -n 19`, **≤ 3 cores**, one job at a time; temp only under
  `/home/fb31/SMC_Engineering_Department/tmp/<YYYYMMDD>-wp3arch/`, removed when done. Never `pkill -f` / `killall`.
- **No NOTS access.** If a measurement needs SPR, write the exact bench command and expected cost; the manager submits.
- Prototypes may go on your own branch `exp/P1M-wp3-arch` (push allowed; no PRs merged by you; never push to other
  branches, never force-push). Work in your own worktree under `/home/fb31/BVS-wt/`.
- Labels: MEASURED / ESTIMATE / PLANNING VALUE on every number.
- Discipline: `briefs/BUILD_COMMON.md` (binding).

## Deliverables and checkpoints
- **Checkpoint 1 (end of day 1):** ≤ 15-line message to the manager: the cost model of a late 10⁶ round, the top 3
  levers with expected gain per pair (ESTIMATE), and any design-level risk found.
- **Final (≈ day 3):** `Docs/Experiments/P1M/WP3_ARCH_REVIEW.md`: the cost model; ranked recommendations with
  expected and (where measured) actual gains; the design-risk findings; the builder 6–7 work split; the exact SPR
  measurement to confirm it (bench commands, cost). Final message ≤ 15 lines.
