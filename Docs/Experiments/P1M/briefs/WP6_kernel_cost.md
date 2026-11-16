# Brief — Builder 6: island kernel cost, same bits (Opus 5.5, high; Claude Third; H-11, starts Tue 11-17)

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

## Packages, in order (one PR each into `exp/P1M-engine`, from your own `exp/P1M-wp6-*` branches)
- **K1** bounded scoring, bounded uniform scan, one-particle phase B (port from the prototype). Include the NaN-row test of
  §2.1.
- **K2** the Philox 32×32 multiply, inverse-only round orders, I-step proposals in the order phase.
- **K3** Gram rows of active columns kept across passes: slot allocator, memory-plan term, G following the support size.
- **K4** large supports (lever 7): full 8-label groups across tiles, several groups per flip call.
- **K5** rolling admission (lever 5).

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
