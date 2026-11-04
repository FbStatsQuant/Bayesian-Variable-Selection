// n9_order.cpp -- the round order of the PRODUCTION Engine::draw_order (v3_engine.h:195-200) is a uniform permutation.
// Drives draw_order with every combination of its m-1 categorical choices (u = (c+1/2)/(i+1)) and checks that the
// m! choice vectors map bijectively onto the m! permutations (so, with continuous uniforms, every order has
// probability 1/m!, and the law is invariant under reversal). Also reports the grid-level (2^-53) deviation from
// 1/(i+1) of each categorical floor(u*(i+1)) for i+1 <= 64, computed by bisection on the production RNG grid.
#include <cstdio>
#include <memory>
typedef void* SEXP;
inline bool Rf_isNull(SEXP x) { return x == nullptr; }
namespace Rcpp { template <class T> struct XPtr { T* p; explicit XPtr(SEXP x) : p((T*)x) {} T* get() const { return p; } }; }
#include "v3_engine.h"
using namespace v3;

struct Scripted : public VariateSource {
  std::vector<double> q; size_t pos = 0;
  double u(const char*) override { return pos < q.size() ? q[pos++] : 0.0; }
};

int main() {
  for (int p = 1; p <= 4; ++p) for (int B = 1; B <= 2; ++B) {
    int n = 8;
    std::vector<double> X((size_t)n * p), y(n);
    for (int i = 0; i < n; ++i) { y[i] = (i % 3) - 1.0; for (int j = 0; j < p; ++j) X[(size_t)j * n + i] = std::sin(1.3 * i + 0.7 * j * j + j); }
    std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
    Data D; data_init(D, X.data(), y.data(), n, p, orig);
    Start st; st.D = &D; std::vector<std::vector<int>> Nb(p);
    Engine E(D, st, Nb, B); Scripted src; E.vs = &src;
    int m = E.nlabels();
    // enumerate mixed-radix choice vectors: position for i = m-1..1 has i+1 options
    long total = 1; for (int i = 2; i <= m; ++i) total *= i;
    std::set<std::vector<int>> perms; std::set<std::vector<int>> rev_closed;
    std::vector<int> ch(m, 0);
    for (long t = 0; t < total; ++t) {
      long x = t; src.q.clear();
      for (int i = m - 1; i >= 1; --i) { int c = (int)(x % (i + 1)); x /= (i + 1); src.q.push_back((c + 0.5) / (i + 1)); }
      src.pos = 0;
      std::vector<int> ord; E.draw_order(ord);
      perms.insert(ord);
    }
    bool all_rev = true;
    for (auto& o : perms) { std::vector<int> r(o.rbegin(), o.rend()); if (!perms.count(r)) all_rev = false; }
    printf("p=%d B=%d m=%d: m!=%ld choice vectors -> %zu distinct permutations (%s); reversal-closed: %s\n", p, B, m, total,
           perms.size(), (long)perms.size() == total ? "bijection, uniform" : "NOT A BIJECTION", all_rev ? "yes" : "no");
  }
  // grid-level deviation of floor(u*k) with u = i 2^-53 (production Xoshiro256ss::uniform)
  double worst = 0; int wk = 0;
  for (int k = 2; k <= 64; ++k) {
    uint64_t prev = 0;
    for (int a = 0; a < k; ++a) {
      // first grid integer x with floor(x 2^-53 * k) > a
      uint64_t lo = prev, hi = (uint64_t)1 << 53;
      if (a == k - 1) { lo = hi; }
      else { while (hi - lo > 1) { uint64_t mid = lo + (hi - lo) / 2; if ((int)std::floor((double)mid * 0x1.0p-53 * k) <= a) lo = mid; else hi = mid; } lo = hi; }
      double pr = (double)(lo - prev) * 0x1.0p-53;
      double dev = std::fabs(pr - 1.0 / k) / (1.0 / k);
      if (dev > worst) { worst = dev; wk = k; }
      prev = lo;
    }
  }
  printf("grid-level max relative deviation of P(floor(u k) = a) from 1/k, k <= 64: %.3e (k=%d)\n", worst, wk);
  return 0;
}
