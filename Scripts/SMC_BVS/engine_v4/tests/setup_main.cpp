// setup_main.cpp -- runner for the WP2 setup tests: v4_setup_tests [--quick|--full] [--threads k] [--filter substr]
#include <chrono>
#include <cstdlib>
#include "setup_tk.h"

int main(int argc, char** argv) {
  int level = 0; std::string filter;
  for (int i = 1; i < argc; ++i) {
    std::string a = argv[i];
    if (a == "--full") level = 1;
    else if (a == "--quick") level = 0;
    else if (a == "--threads" && i + 1 < argc) stk::threads() = std::atoi(argv[++i]);
    else if (a == "--filter" && i + 1 < argc) filter = argv[++i];
  }
  int ran = 0, failed_tests = 0;
  for (auto& t : stk::registry()) {
    if (t.level > level) continue;
    if (!filter.empty() && std::string(t.name).find(filter) == std::string::npos) continue;
    long f0 = stk::fails(), c0 = stk::checks();
    auto t0 = std::chrono::steady_clock::now();
    try { t.fn(); } catch (const std::exception& e) { ++stk::fails(); std::printf("  FAIL exception: %s\n", e.what()); }
    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    bool ok = stk::fails() == f0;
    std::printf("%s %-44s %7ld checks %8.2f s\n", ok ? "PASS" : "FAIL", t.name, stk::checks() - c0, s);
    std::fflush(stdout);
    ++ran; if (!ok) ++failed_tests;
  }
  std::printf("%d tests, %d failed, %ld checks, %ld failed checks (threads %d, level %s)\n", ran, failed_tests, stk::checks(), stk::fails(),
              stk::threads(), level ? "full" : "quick");
  return failed_tests ? 1 : 0;
}
