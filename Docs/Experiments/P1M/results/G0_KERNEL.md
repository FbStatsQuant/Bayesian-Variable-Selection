# G0 kernel benchmark on NOTS — results (MEASURED, job 2747371, 2026-11-15 20:53 CST)

Node bb2u25c1: Xeon Platinum 8468 (Sapphire Rapids), 96 allocated CPUs = 48 cores × 2 hyperthreads, spanning both
sockets. GCC 14.3.0, `-O3 -march=sapphirerapids -ffp-contract=off -fno-math-errno -fopenmp`, glibc 2.34.
p = 10⁶, n = 200, AR(0.6). Raw log: `results/g0_kernel_2747371.log`. Billed: 3,168 CPU-s = **0.88 core-h** (33 s).

## Kernel cost per (support, label), thread-time (ns)
| kernel | supports | T = 1 | T = 24 | T = 48 (1 per core) | T = 96 (2 per core) | Owls, T = 8 (FEASIBILITY §1.1) |
|---|---|---|---|---|---|---|
| label-major, **class A** | 256 distinct (\|A\| = 1,279) | 65.5 | 71.9 | **87.5** | 155.1 | 121–128 |
| label-major, class A | S₀ alone | 19.7 | 20.7 | 22.6 | 31.6 | 42 |
| label-major, **bit form** | 256 distinct | 135.4 | 138.0 | 155.9 | 262.8 | 223 |
| label-major, bit form | S₀ alone | 80.7 | 83.8 | 91.5 | 135.8 | 163 |
| direct Gram-free step | — | 1,337 | 1,792 | 1,711 | 2,433 | 2,086–2,705 |

- **Per billed CPU.** At T = 96 the throughput is 96 / 161.6 ns = 0.59 scores per ns per node-half; at T = 48 it is
  48 / 89.0 = 0.54. Hyperthreads add ≈ 10%. Billed cost per (support, label): **≈ 162 ns·CPU (class A)** and
  ≈ 270 ns·CPU (bit form), on 256 distinct supports.
- **Bit checks.** Bit form vs `v3::Scorer`: **0 mismatches of 4,096**. Class A: 0 of 4,096 beyond 1e-9 relative. Direct:
  0 of 2,000.
- **Memory bandwidth** (4 GB read): 10.3 GB/s (T = 1), 135 (T = 24), 209 (T = 48), 236 (T = 96).
- **Round order** (Fisher–Yates + inverse) per label: 8.0 ns (T = 1), 7.6 (T = 24), 12.1 (T = 48), 40.3 (T = 96).
- **Store offers**, capacity 4·10⁷, T = 1: REJECT 5.5 ns; MIX 7.7–19.3 ns; FILL 102; DUP-RANDOM 72.5; NEW 978.
- **Pass fractions** (share of scores within Δ of F(S)): Δ = 14 → 0.10–0.12; Δ = 16 → 1.0.
- **Not measured:** the multi-threaded `offer` mode **crashed** (segfault after the T = 1 offer test: a bug in the
  benchmark's per-thread store, not in a kernel). Fixed in WP3's store, which gets its own test. M (sweeps per round) is
  measured by the stage job and WP3.

## Against the plan (G0 gate, ENGINEERING_SPEC §0-v2.6)
Planning value: c = M·c_s + c_f = 3 × 90 + 30 = 300 ns thread-time (one thread per core), i.e. 600 ns·CPU billed.
- **Measured at T = 48:** c_s = 87.5 → c ≈ 3 × 87.5 + (12 order + ≈ 15 offers) ≈ **290 ns thread-time ≈ 580 ns·CPU**.
- **Measured at T = 96:** ≈ 3 × 155 + 40 + 15 ≈ 520 ns per thread ≈ **520 ns·CPU**.
- **G0 threshold (c ≤ 700 ns per step per thread): PASS.** The precise-plan cost model stands (≈ 963 core-h per precise
  1M fit at M = 3). Use 2 threads per core (T = 96 on 96 CPUs): ≈ 10% cheaper per billed CPU.
- **Label-major vs direct on SPR:** 1,711 / 290 ≈ **5.9×** at M = 3 (per core).
