// bench_wp4_fv.cpp -- WP4 micro-benchmark: one F_V evaluation over |V| members (calibration grid construction),
// serial (class B) vs blocked (class C), 1..k threads; and evaluations per grid on a synthetic V.
//   bench_wp4_fv <n_members> <threads> <reps>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <v4/calib_rules.h>
using namespace v4::calib;
int main(int argc, char** argv) {
  size_t n = argc > 1 ? std::strtoull(argv[1], 0, 10) : 4000000; int th = argc > 2 ? atoi(argv[2]) : 3; int reps = argc > 3 ? atoi(argv[3]) : 10;
  std::mt19937_64 g(1); std::normal_distribution<double> nd;
  std::vector<double> a(n), b(n); for (size_t i = 0; i < n; ++i) { a[i] = 5 * nd(g); b[i] = 30 * nd(g); }
  for (SumMode m : {SumMode::Serial, SumMode::Blocked}) for (int t : {1, th}) {
    FV fv(a, b, m, t); volatile double sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int r = 0; r < reps; ++r) sink = sink + fv(0.001 + 0.1 * r);
    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count() / reps;
    std::printf("F_V |V|=%zu mode=%s threads=%d: %.4f s per evaluation (%.2f ns per member)\n", n, sum_mode_name(m), t, s, 1e9 * s / n);
  }
  std::vector<double> tg; for (int k = 0; k <= 40; ++k) tg.push_back(k / 40.0 * k / 40.0);
  size_t ns = std::min<size_t>(n, 200000);
  std::vector<double> a2(a.begin(), a.begin() + ns), b2(b.begin(), b.begin() + ns);
  auto t0 = std::chrono::steady_clock::now();
  auto gr = build_grid(a2, b2, tg, 4000, SumMode::Serial, 1);
  double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  std::printf("build_grid |V|=%zu: ok=%d intervals=%zu F_V evaluations=%ld in %.2f s (1 thread)\n", ns, (int)gr.ok, gr.grid.size() - 1, gr.evals, s);
}
