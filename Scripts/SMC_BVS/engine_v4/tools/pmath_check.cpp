// pmath_check.cpp -- measures the libm functions the engine pins (log, exp, log1p, expm1, lgamma):
//  (1) a SHA-256 of all results on fixed argument sets (compare across machines / glibc tunables);
//  (2) how many results are not correctly rounded, against libquadmath (113-bit) rounded to double;
//  (3) ns per call. Build: target v4_pmath_check (bit flags). Run under GLIBC_TUNABLES to force the non-FMA variants.
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <random>
#include <vector>
extern "C" {
#include <quadmath.h>
}
#include "v4/pmath.h"
#include "v4/sha256.h"

using namespace v4;

static uint64_t bits(double x) { uint64_t b; std::memcpy(&b, &x, 8); return b; }
static double ulps(double a, double b) {   // distance in units in the last place (same sign, finite)
  if (a == b) return 0;
  int64_t ia = (int64_t)bits(a), ib = (int64_t)bits(b);
  if (ia < 0) ia = INT64_MIN - ia;
  if (ib < 0) ib = INT64_MIN - ib;
  return (double)(ia > ib ? ia - ib : ib - ia);
}
struct Fn { const char* name; double (*f)(double); __float128 (*q)(__float128); double lo, hi; bool logscale; };
static double f_log(double x) { return pm::log(x); }
static double f_exp(double x) { return pm::exp(x); }
static double f_log1p(double x) { return pm::machine::log1p(x); }
static double f_expm1(double x) { return pm::machine::expm1(x); }
static double f_lgamma(double x) { return pm::lgamma(x); }

int main(int argc, char** argv) {
  const size_t N = argc > 1 ? (size_t)std::atol(argv[1]) : 2000000;
  Fn fns[] = {
    {"log", f_log, logq, 1e-300, 1e12, true}, {"log_near1", f_log, logq, 0.5, 2.0, false},
    {"exp", f_exp, expq, -745, 0, false}, {"exp_pos", f_exp, expq, 0, 700, false},
    {"log1p", f_log1p, log1pq, -0.999, 1e3, false}, {"log1p_small", f_log1p, log1pq, 1e-300, 1e-3, true},
    {"expm1", f_expm1, expm1q, -40, 1, false},
    {"lgamma", f_lgamma, lgammaq, 1e-3, 3e6, true}, {"lgamma_int", f_lgamma, lgammaq, 1, 3e6, false},
  };
  auto li = pm::libm_info();
  std::printf("{\"libm\":\"%s\",\"libm_sha256\":\"%s\",\"glibc\":\"%s\",\"N\":%zu,\"functions\":[\n", li.path.c_str(), li.sha256.c_str(), li.gnu_libc_version.c_str(), N);
  bool first = true;
  for (auto& F : fns) {
    std::vector<double> x = pm::check_arguments(F.name, N), y(N);
    auto t0 = std::chrono::steady_clock::now();
    for (size_t i = 0; i < N; ++i) y[i] = F.f(x[i]);
    double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count() / (double)N;
    size_t notcr = 0; double maxu = 0;
    for (size_t i = 0; i < N; ++i) {
      double r = (double)F.q((__float128)x[i]);
      if (bits(r) != bits(y[i])) { ++notcr; maxu = std::max(maxu, ulps(r, y[i])); }
    }
    auto h = sha256(y.data(), N * 8);
    std::printf("%s {\"fn\":\"%s\",\"range\":[%g,%g],\"sha256\":\"%s\",\"not_correctly_rounded\":%zu,\"max_ulp_vs_quad\":%g,\"ns_per_call\":%.2f}\n",
                first ? " " : ",", F.name, F.lo, F.hi, hex(h).c_str(), notcr, maxu, ns);
    first = false;
  }
  // x87 long double rows (INTERFACES v0.1.4): reference = libquadmath rounded to long double; 10 significant bytes compared
  struct FnL { const char* name; long double (*f)(long double); __float128 (*q)(__float128); };
  FnL fl[] = {{"expl", [](long double x) { return pm::expl(x); }, expq}, {"logl", [](long double x) { return pm::logl(x); }, logq}};
  for (auto& F : fl) {
    std::vector<long double> x = pm::check_arguments_l(F.name, N), y(N);
    auto t0 = std::chrono::steady_clock::now();
    for (size_t i = 0; i < N; ++i) y[i] = F.f(x[i]);
    double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count() / (double)N;
    size_t notcr = 0;
    for (size_t i = 0; i < N; ++i) { long double r = (long double)F.q((__float128)x[i]); if (std::memcmp(&r, &y[i], 10) != 0) ++notcr; }
    std::printf(", {\"fn\":\"%s\",\"sha256\":\"%s\",\"not_correctly_rounded\":%zu,\"ns_per_call\":%.2f}\n", F.name, pm::sha256_ld(y).c_str(), notcr, ns);
  }
  std::printf("]}\n");
  return 0;
}
