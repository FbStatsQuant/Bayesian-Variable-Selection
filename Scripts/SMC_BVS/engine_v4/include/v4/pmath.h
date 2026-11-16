// pmath.h -- the pinned transcendental functions (INTERFACES §6; ENGINEERING_SPEC §3; review §4.9).
// All engine code calls v4::pm::*, never std:: directly, so the binding can be changed in one place.
// Binding (WP1, tests/PMATH_REPORT.md): glibc 2.34 libm, called through the same std:: overloads core/ uses, compiled
// with the bit flags.
//   pm::log, pm::exp, pm::lgamma, pm::sqrt -- BIT FORM. Their bits equal on Owls and NOTS (MEASURED, 2·10^6 arguments
//       each, results/PMATH_NOTS.md) although the libm files differ; checked at start by pm::self_test().
//   pm::logl, pm::expl -- BIT FORM (x87 long double; log_sum_exp -> log W_K -> log varpi -> every F, and WP2's
//       cumulative_from_logs). Self-test rows "expl" / "logl" (80-bit results hashed); Owls reference, NOTS re-run pending.
//   pm::machine::log1p, pm::machine::expm1 -- CLASS A ONLY. Their bits differ between Owls and NOTS (NOTS's libm takes
//       the SSE2 code for them). Bit-form code must not call them (core/ never does: log_add and log1mexp_v3 in
//       core/cpp/v3_util.h:67-86 are unused); their results never enter a fixture or a bit test.
#pragma once
#include <cmath>
#include <string>
#include <vector>

namespace v4::pm {
inline double log(double x) { return std::log(x); }
inline double exp(double x) { return std::exp(x); }
inline double lgamma(double x) { return std::lgamma(x); }
inline double sqrt(double x) { return std::sqrt(x); }   // IEEE correctly rounded: not a pinning issue
inline long double logl(long double x) { return std::log(x); }   // x87 long double log/exp (log_sum_exp); see report
inline long double expl(long double x) { return std::exp(x); }
namespace machine {   // class A only: machine-dependent bits
inline double log1p(double x) { return std::log1p(x); }
inline double expm1(double x) { return std::expm1(x); }
}  // namespace machine
inline const char* binding() { return "glibc-libm"; }

struct LibmInfo { std::string path, sha256, gnu_libc_version; bool fma_variant = false; };
LibmInfo libm_info();   // path of the loaded libm.so.6, its SHA-256, gnu_get_libc_version(), FMA/AVX2 present & unmasked
bool fma_variant_expected();

// Self-test of the bit-form functions (log, exp, lgamma): SHA-256 of f(x) over the six fixed v4_pmath_check rows
// (2·10^6 arguments each) compared with the hashes measured on Owls and equal on NOTS (PMATH_NOTS.md). This is the
// guard: it keys on function results, not on the libm file hash (the files differ between Owls and NOTS).
struct SelfTestRow { const char* fn; std::string sha256; bool ok; };
struct SelfTest { bool ok = true; std::vector<SelfTestRow> rows; };   // log, log_near1, exp, exp_pos, lgamma, lgamma_int, expl, logl
SelfTest self_test();                                   // once per process; MEASURED 1.0–1.4 s wall with binary_block()
// v4_pmath_check rows (shared with the tool): arguments of row `name`, first n.
std::vector<double> check_arguments(const std::string& name, size_t n);
// Long double rows: "expl" (double-valued arguments in [-11000, 0], as log_sum_exp passes them) and "logl" (genuine
// 64-bit-mantissa arguments in [1, 1001), as the long double sums of log_sum_exp). Generator mt19937_64(12345).
std::vector<long double> check_arguments_l(const std::string& name, size_t n);
// SHA-256 over the 10 significant bytes of each x87 value (the 6 padding bytes are not hashed).
std::string sha256_ld(const std::vector<long double>& y);
}  // namespace v4::pm
