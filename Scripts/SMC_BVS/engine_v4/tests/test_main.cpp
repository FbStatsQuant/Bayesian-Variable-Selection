// test_main.cpp -- runs the registered tests. Usage: v4_tests [--full] [filter]. Tests tagged "full" run with --full.
#include <chrono>
#include <cstdlib>
#include "tk.h"

int main(int argc, char** argv) {
  bool full = false; std::string filter;
  for (int i = 1; i < argc; ++i) { std::string a = argv[i]; if (a == "--full") full = true; else filter = a; }
  int ran = 0, failed_cases = 0;
  for (auto& c : tk::registry()) {
    if (!filter.empty() && std::string(c.name).find(filter) == std::string::npos) continue;
    if (!full && std::strcmp(c.tags, "full") == 0) continue;
    tk::current() = c.name;
    int before = tk::failures();
    auto t0 = std::chrono::steady_clock::now();
    try { c.fn(); } catch (const std::exception& e) { tk::fail(__FILE__, __LINE__, std::string("exception: ") + e.what()); }
    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    bool ok = tk::failures() == before;
    std::printf("[%s] %-44s %8.3f s\n", ok ? "PASS" : "FAIL", c.name, s);
    ++ran; if (!ok) ++failed_cases;
  }
  std::printf("%d test cases, %d failed, %d check failures\n", ran, failed_cases, tk::failures());
  return failed_cases ? 1 : 0;
}
