# libm bind check on NOTS vs Owls (MEASURED, job 2747666, node bb2u16c1, 2026-11-15 22:01 CST)

WP1's `v4_pmath_check` (PR #11 at 8ff9775), GCC 14.3.0, glibc 2.34 on both machines. The libm files themselves differ
(NOTS libm sha256 98677841…, Owls 840be1bb…). 2·10⁶ arguments per function. Raw: `results/pmath_nots_2747666.log`.

| function | range | bits NOTS = Owls |
|---|---|---|
| log | [1e-300, 1e12] | **yes** |
| log near 1 | [0.5, 2] | **yes** |
| exp | [−745, 0] | **yes** |
| exp | [0, 700] | **yes** |
| log1p | [−0.999, 1000] | **NO** (39,981 vs 39,988 not correctly rounded) |
| log1p small | [1e-300, 1e-3] | **yes** |
| expm1 | [−40, 1] | **NO** (22,831 vs 22,746) |
| lgamma | [1e-3, 3e6] | **yes** |
| lgamma at integers | [1, 3e6] | **yes** |

**Impact on the v3 bit contract: none.**
- `core/` calls log1p/expm1 only inside `log_add` and `log1mexp_v3` (`cpp/v3_util.h:71, 86`), and neither is called
  anywhere in `core/` (grep of `cpp/*.h`, `cpp/*.cpp`, `*.R`).
- Every function `core/` uses (log, exp, lgamma) gives identical bits on both machines, so Owls fixtures are valid
  references for NOTS runs.

**Rule for engine_v4.** Bit-form code paths must not call `log1p` or `expm1`. Where class-A code uses them, its outputs
are machine-dependent at the 1-ulp level and must never enter a bit test or fixture. The guard (`v4_pmath_check`) records
the libm hash in every manifest.
