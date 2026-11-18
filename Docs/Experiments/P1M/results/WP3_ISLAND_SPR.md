# WP3 class-A island on NOTS SPR — first measurement (MEASURED, job 2747881, commit 820bd30, 2026-11-15 22:16–22:28 CST)

Node bb3u15c1 (Xeon 8468, 96 allocated CPUs). Label-major class-A kernel, N = 2,500, G = 256, tile 128, AR(0.6), n = 200,
**p = 10⁴** (stand-in partition: blocks of 4). The p = 10⁵ runs did **not** finish inside my 12-min limit (TIMEOUT; no output).
Billed 70,080 CPU-s = 19.5 core-h. Raw log: `results/wp3_bench_2747881.log`.

| grid | threads | wall (s) | thread-time ns/step | wall ns/step | **billed ns·CPU/step if CPUs = threads** | M | products ns/pair |
|---|---|---|---|---|---|---|---|
| adaptive (T = 17) | 24 | 23.95 | 791 | 33.0 | 791 | 3.63 | 17.7 |
| adaptive | 48 | 19.64 | 1,298 | 27.0 | 1,298 | 3.63 | 21.8 |
| adaptive | 96 | 19.04 | 2,517 | 26.2 | 2,517 | 3.63 | 43.8 |
| geo:30 | 24 | 31.43 | 717 | 29.9 | 717 | 4.19 | 16.8 |
| geo:30 | 48 | 25.63 | 1,170 | 24.4 | 1,170 | 4.19 | 20.6 |
| geo:30 | 96 | 23.66 | 2,160 | 22.5 | 2,160 | 4.19 | 41.5 |

- **T3 on SPR: PASS.** The output hash is identical at 24/48/96 threads for each grid.
- **Thread scaling at p = 10⁴ is poor.** Wall time barely falls from 24 to 96 threads. Per-step thread-time at 24 threads splits
  into phase A 222 ns (products + odds) and phase B 285 ns, plus orders 20, build 39 and walk 30. At 10⁴ each of the 3,633
  passes carries only ≈ 51 supports × 10⁴ labels, so synchronisation and per-pass overheads dominate. At 10⁶ a pass carries
  100× more work. Whether scaling recovers there is **the** open question; it was not measured (10⁵ timed out).
- **Against the plan** (300 ns thread-time = 600 ns·CPU billed at 1 thread/core): at 10⁴ the best billed figure is ≈ 717–791
  ns·CPU/step (24 threads on 24 CPUs) = **+20–30%**. At 48–96 threads it is 2–4× worse. M = 3.63 on the calibrated-like grid
  (plan 3).
- **Not yet known:** the cost per step at 10⁵–10⁶, the thread count at which a 1M island saturates, and the setup + calibration
  timing (T5).
