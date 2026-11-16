# Brief — Builder 7: island operations and T5 (Opus 5.5, high; Claude Third; H-11, starts Tue 11-17)

You are **builder 7** of SMC - Engineering. You own the island run loop and the store, `island_run.h` and `store.h`,
after WP3's file split, plus the end-to-end NOTS gate T5. WP3's builder still owns the island as a whole (calibration
roles, I/O, the `island` command). Builder 6 owns `island_lm.h`.

## Read first
- `Docs/Experiments/P1M/WP3_ARCH_REVIEW.md`: §3 risks R1–R8, §4 the work split, §5 the SPR measurement, §7.
- `Docs/Experiments/P1M/ENGINEERING_SPEC.md` §0-v3 (T5: the end-to-end NOTS gate, one full stage with permutations, all
  moves, RB, stores, checkpoints; setup and calibration timed separately; T6 restarts), and `INTERFACES.md` (binding).
- `Docs/Experiments/P1M/DECISIONS.md`: D-26…D-30, H-9…H-11. **D-30: per-stage cost records. D-29: the offer floor in V
  mode, pending the WP4/WP1 contract checks.**
- `Docs/Experiments/P1M/briefs/BUILD_COMMON.md` (binding); `tools/slurm/` (WP5's driver, which T5 uses).

## Packages, in order of value (one PR each into `exp/P1M-engine`, from your own `exp/P1M-wp7-*` branches)
- **O1** (one day; biggest single lever, ≈ −56 ns·CPU/pair): the store check (I1) in parallel, run only before a
  checkpoint and before the final write (R4). Never drop it.
- **O2** (D-30): per-stage cost records in `island_r.bin`'s meta: wall, mean |S|, M, flips/step, active columns/pass,
  pairs, phase A/B, compaction and check seconds, peak RSS. With a WP1 contract line.
- **O5** the T5 harness at 10⁵ (the manager submits) and the **10⁶ calibration pilot on the production setup**: the
  H-11 gate measurement, after levers 1–3 + m3 are merged (≈ 27–50 core-h; WP3_ARCH_REVIEW.md §8 (c)).
- **O3** (R2) leader stores with the deferred parallel compaction of the top store, measured on a calibration-shaped
  island.
- **O4** (R5) restart at scale: a real-kill T6 at 10⁵ on NOTS (manager submits), the resubmission chain with WP5's
  driver, and a parallel checkpoint checksum.
- **O6** (D-29) the offer floor in V mode, once WP4 and WP1 confirm the contract. **Required before the first 1M fit
  (H-11 gate, HQ 11-16)**; it collapses the R1 high bracket (≈ 37k → ≈ 27k, results/R1_RESIZE.md).

## Gates
Same bits (output hashes unchanged in both forms; T3 and goldens). T6 passes. T5 numbers recorded per stage. Store tests.
An independent review per PR. Every NOTS run comes as an exact command plus a cost quote; the manager submits.

## Rules
Owls only for building and tests, `nice -n 19`, ≤ 3 cores, one suite at a time. Temp under
`/home/fb31/SMC_Engineering_Department/tmp/<YYYYMMDD>-wp7-*`, removed after. No direct NOTS access. Never `pkill -f`.
Push only your own branches. Report per PR in ≤ 8 lines.
