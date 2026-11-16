# Pinned transcendental functions: measurement and decision (WP1, 2026-11-15)

**Question (spec §3, review §4.9).** Bundle our own exp/log/log1p/expm1/lgamma, or use glibc? Does glibc on Owls
already give the v3.1 record bits?

## Measurements (MEASURED; Owls `owls.stat.rice.edu`, Xeon Gold 6148 (Skylake-SP: FMA, AVX2, AVX-512), glibc
2.34-284.el9_8.4, `/lib64/libm.so.6` sha256 `840be1bb…3d7e`, GCC 11.5.0, bit flags, 1 thread, nice 19)
Tool: `tools/pmath_check.cpp` (target `v4_pmath_check`), 2·10⁶ arguments per row, fixed seed. Reference: libquadmath
(113-bit) rounded to double. Raw output: `tests/fixtures/pmath_owls_glibc234_fma.json`.

| function, argument range | not correctly rounded (of 2·10⁶) | max error vs quad | ns/call | same bits with `GLIBC_TUNABLES=glibc.cpu.hwcaps=-AVX2,-FMA`? |
|---|---|---|---|---|
| log, [1e-300, 1e12] log-uniform | 3 | 1 ulp | 7.0 | **no** (5 not CR) |
| log, [0.5, 2] | 2,601 | 1 ulp | 10.1 | **no** |
| exp, [-745, 0] | 1,602 | 1 ulp | 14.7 | **no** |
| exp, [0, 700] | 1,578 | 1 ulp | 10.3 | **no** |
| log1p, [-0.999, 1e3] | 39,988 | 1 ulp | 15.2 | **no** |
| expm1, [-40, 1] | 22,746 | 1 ulp | 13.7 | **no** |
| lgamma, [1e-3, 3e6] log-uniform | 412,936 | 2 ulp | 22.0 | **no** |
| lgamma, integers in [1, 3e6] | 640,129 | 2 ulp | 17.2 | **no** |

(The obsolete tunable spelling `-AVX2_Usable,-FMA_Usable` is silently ignored by glibc 2.34: same bits as default.)

Other facts:
- The v3 compat scorer reproduces `core/` bit for bit on Owls (tests: 1,608 R-compiled `cpp_score` values, 773,998
  table entries, 3,000+ random models per design against the core headers, all routes forced).
- G0 on NOTS (manager, results/G0_KERNEL.md): bit form = v3 scorer bits (0 of 4,096) on SPR, glibc 2.34, GCC 14.3.0.

## Conclusions
1. glibc is **not** correctly rounded (≤ 1 ulp for exp/log, ≤ 2 ulp for lgamma), so any bundled correctly rounded
   library (e.g. CORE-MATH) would change v3.1 bits in a measurable fraction of calls: 0.1–2% for log/exp and ~20–30% for
   lgamma. That would require rebuilding the reference and regenerating the 34 units (≈ 20 task-h, review §4.9).
2. glibc results **depend on the CPU features** (ifunc selects FMA/AVX2 variants at load time). Owls (Skylake) and NOTS
   (Sapphire Rapids) both take the FMA variant; a node without FMA/AVX2 would produce different bits.

## Decision (WP1; INTERFACES v0.1.1 §6)
- **Do not bundle.** `v4::pm::*` binds to glibc 2.34 libm (FMA variant), the same routines the v3.1 records used.
- **Guard:** `pm::fma_variant_expected()` (FMA + AVX2 present, not masked by GLIBC_TUNABLES); bit-form (T / compat)
  runs must refuse when it is false. Every manifest records the libm path, its SHA-256 and `libm_fma_variant`
  (`smcbvs4 version`).
- **One cross-machine check, needs the manager (one sequential `ssh nots`):** run `v4_pmath_check` on one SPR node and
  compare its 9 hashes with `tests/fixtures/pmath_owls_glibc234_fma.json`. Expect identical bits if the libm code is the
  same el9 build family. If not, it is the libm package, not the CPU, and this decision is revisited.
- Class-A kernels (V) may use vector log/exp: they are class A by definition, not affected.

## Addendum (2026-11-15, after the NOTS run; INTERFACES v0.1.3)
- NOTS (job 2747666, node bb2u16c1, SPR, glibc 2.34, libm sha256 98677841…; Owls 840be1bb…): 7 of 9 row hashes equal.
  `log1p` and `expm1` differ. NOTS's not-correctly-rounded counts for them (39,981 and 22,831) are exactly Owls' counts
  under the **non-FMA** variant, so NOTS's libm build takes the SSE2 code for these two functions.
  Write-up: `Docs/Experiments/P1M/results/PMATH_NOTS.md`.
- `core/` never calls log1p/expm1 (`log_add` and `log1mexp_v3` are unused), so the Owls fixtures are valid for NOTS.
- **The no-bundling decision stands.** Changes:
  - log1p/expm1 move to `pm::machine::` (class A only);
  - the guard becomes `require_bit_libm()`, which checks that log/exp/lgamma reproduce the six measured row hashes. It
    keys on function results, not on the libm file hash. A CPU-flag check alone could not have seen the per-function
    difference above.
