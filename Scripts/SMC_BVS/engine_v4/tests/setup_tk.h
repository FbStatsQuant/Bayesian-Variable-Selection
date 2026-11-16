// setup_tk.h -- minimal test harness and synthetic designs for the WP2 setup tests (WP1 owns tests/tk.h; this file
// is folded into it at integration). No external dependencies.
#pragma once
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <functional>
#include <string>
#include <vector>
#include "v4/setup.h"

namespace stk {

struct Test { const char* name; int level; std::function<void()> fn; };  // level 0 quick, 1 full
inline std::vector<Test>& registry() { static std::vector<Test> r; return r; }
struct Reg { Reg(const char* n, int lvl, std::function<void()> f) { registry().push_back({n, lvl, f}); } };
inline long& fails() { static long f = 0; return f; }
inline long& checks() { static long c = 0; return c; }
inline int& threads() { static int t = 3; return t; }
#define STK_CAT2(a, b) a##b
#define STK_CAT(a, b) STK_CAT2(a, b)
#define TEST(name, level) static void STK_CAT(t_, name)(); static stk::Reg STK_CAT(r_, name)(#name, level, STK_CAT(t_, name)); static void STK_CAT(t_, name)()
#define CHECK(cond, ...) do { ++stk::checks(); if (!(cond)) { ++stk::fails(); std::printf("  FAIL %s:%d: %s ", __FILE__, __LINE__, #cond); std::printf(__VA_ARGS__); std::printf("\n"); } } while (0)

inline bool same_bits(double a, double b) { uint64_t x, y; std::memcpy(&x, &a, 8); std::memcpy(&y, &b, 8); return x == y || (std::isnan(a) && std::isnan(b)); }

// deterministic normal generator (splitmix64 + Box-Muller); the designs need not match any other generator
struct Rng {
  uint64_t s;
  explicit Rng(uint64_t seed) : s(seed * 0x9E3779B97F4A7C15ULL + 12345) {}
  double u() { return ((v4::splitmix64(s) >> 11) + 0.5) * 0x1.0p-53; }
  double norm() { double a = u(), b = u(); return std::sqrt(-2 * std::log(a)) * std::cos(2 * M_PI * b); }
};

enum Design { IND, AR, BLK, TIE };
inline const char* design_name(Design d) { static const char* n[] = {"IND", "AR", "BLK", "TIE"}; return n[d]; }

// Standardised fixture: X n x p column-major (centred, sum x^2 = n - 1), y standardised. TIE = AR(0.6) with exact
// duplicates and sign-flipped duplicates of some columns (bit-identical |columns|) to exercise every tie rule.
struct Fixture {
  v4::DataOwner own;
  const v4::Data& D() const { return own.D; }
  Design design; int n, p;
  Fixture(Design d, int n_, int p_, uint64_t seed, double rho = 0.6, int blk = 20) : design(d), n(n_), p(p_) {
    Rng g(seed + 1000003ULL * (int)d);
    std::vector<double> X((size_t)n * p), y(n, 0.0);
    std::vector<double> f(n);
    for (int j = 0; j < p; ++j) {
      double* x = &X[(size_t)j * n];
      if (d == BLK && j % blk == 0) for (int i = 0; i < n; ++i) f[i] = g.norm();
      for (int i = 0; i < n; ++i) {
        double e = g.norm();
        if (d == IND) x[i] = e;
        else if (d == AR || d == TIE) x[i] = (j == 0) ? e : rho * X[(size_t)(j - 1) * n + i] + std::sqrt(1 - rho * rho) * e;
        else x[i] = std::sqrt(rho) * f[i] + std::sqrt(1 - rho) * e;
      }
    }
    for (int j = 0; j < p; ++j) {  // standardise
      double* x = &X[(size_t)j * n]; double m = 0, s = 0;
      for (int i = 0; i < n; ++i) m += x[i];
      m /= n;
      for (int i = 0; i < n; ++i) { x[i] -= m; s += x[i] * x[i]; }
      s = std::sqrt(s / (n - 1));
      for (int i = 0; i < n; ++i) x[i] /= s;
    }
    if (d == TIE) {  // columns 3k+1 copy 3k (every 3rd group), some negated
      for (int j = 1; j < p; j += 7) {
        double sg = (j % 2) ? 1.0 : -1.0;
        for (int i = 0; i < n; ++i) X[(size_t)j * n + i] = sg * X[(size_t)(j - 1) * n + i];
      }
    }
    // y: five signals spread over the columns
    int sig[5] = {p / 7, 2 * p / 7 + 1, 3 * p / 7 + 2, 4 * p / 7 + 3, 6 * p / 7 + 1};
    double beta[5] = {1, -0.8, 0.9, -0.7, 0.6};
    for (int i = 0; i < n; ++i) { double s = 0; for (int q = 0; q < 5; ++q) if (sig[q] < p) s += beta[q] * X[(size_t)sig[q] * n + i]; y[i] = s + g.norm(); }
    double m = 0, s = 0; for (int i = 0; i < n; ++i) m += y[i];
    m /= n; for (int i = 0; i < n; ++i) { y[i] -= m; s += y[i] * y[i]; }
    s = std::sqrt(s / (n - 1)); for (int i = 0; i < n; ++i) y[i] /= s;
    own.init(X.data(), y.data(), n, p);
  }
};

}  // namespace stk
