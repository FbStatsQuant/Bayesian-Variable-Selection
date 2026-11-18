# Brief — Builder 6: island kernel cost, same bits (Opus 5.5, high; Claude Personal; H-11, starts Tue 11-17)

You are **builder 6** of SMC - Engineering. You own the label-major round, `island_lm.h`, after WP3's file split.
WP3's builder still owns the island as a whole (run loop, calibration roles, I/O). The WP3 architect's prototypes are your
starting point, on branch `exp/P1M-wp3-arch`.

## Read first
- `Docs/Experiments/P1M/WP3_ARCH_REVIEW.md`: §1 the cost model, §2 the levers, §2.1 bounded scoring, §2.2 Gram rows,
  §4 the work split, §7 the addendum. This is your design.
- `Docs/Experiments/P1M/results/WP3_L5_SPR.md` and `WP3_LEVERS_SPR.md` (measured basis), and `INTERFACES.md` (binding).
- `Docs/Experiments/P1M/DECISIONS.md`: D-18…D-30, H-9…H-11. **D-28: no FMA, no class-A deletion scores. Bit identity
  first.**
- `Docs/Experiments/P1M/briefs/BUILD_COMMON.md` (binding discipline).

## Fast-track order (manager, 11-16 16:00 CT; 1M pilot plan, results/PILOT_1M_FASTTRACK.md)
- **K1 then K3 first** (levers 2 and 3; the H-11 gate measures them in the 10⁶ calibration pilot). K2 and K5 come after
  K3 is merged. Base: `exp/P1M-engine` at or after 8b7f89be (WP3's split #42 and m3 #43 are merged).
- When you reach K2: it also edits `draw_order` / `step_nongibbs` in `island_pm.h` (PR42 review minor); that file is
  yours for those two functions only.
- Department cap: 4 concurrent Claude agents. Don't start helpers or sub-agents.

## Packages, in order (one PR each into `exp/P1M-engine`, from your own `exp/P1M-wp6-*` branches)
- **K1** bounded scoring, bounded uniform scan, one-particle phase B (port from the prototype). Include the NaN-row test of
  §2.1.
- **K2** the Philox 32×32 multiply, inverse-only round orders, I-step proposals in the order phase.
- **K3** Gram rows of active columns kept across passes: slot allocator and memory-plan term. With the production start
  law (E|S| ≈ 3.6–3.9 at 10⁶, n = 200; review §9), a fixed 640 slots at G = 256 should cover every stage, so no
  G-following-support logic is needed unless the pilot shows otherwise.
- **K4** large supports (lever 7): **dropped for now** (review §9: production supports are small). It returns only if
  WP2's n = 400 / 1,000 start-law sizes are large.
- **K5** rolling admission (lever 5).

## Benches
From now on, measure with the production setup (WP2's setup.bin), not the stand-in partition: the stand-in overstates
supports 15× and understates the late M (review §9). Until WP2's PR #13 and WP3's StartView land, say which you used.

## Gates, for every package
- **Bits:** output hashes unchanged in both arithmetic forms (Bit and class A), both kernels, 1 and 3 threads, G = 64 and
  256. T3 hashes and every golden unchanged.
- **Measured gain:** on Owls with the `[round]`/`[arch]` counters, before/after, plus the memory-plan delta. After K1 and
  after K3, write the exact SPR bench command and its cost; the manager submits.
- An independent review per PR (the manager starts it).

## Rules
Owls only, `nice -n 19`, ≤ 3 cores, never two test suites at once. Temp under
`/home/fb31/SMC_Engineering_Department/tmp/<YYYYMMDD>-wp6-*`, removed after. No NOTS. Never `pkill -f`. Push only your own
branches. Report per PR in ≤ 8 lines: head, measured gain, hashes, tests.
