// test_main.cpp -- runs the registered tests. Usage: v4_tests [--full | --identity] [filter]. Tests tagged "full" run with --full; tests tagged "identity" (the default-N
// identity gate against the frozen binary F: V4_F_SMCBVS4, V4_F_SMCBVS4_SHA256) run ONLY with --identity, which runs only them.
#include <chrono>
#include <cstdlib>
#include "tk.h"

int main(int argc, char** argv) {
  bool full = false, identity = false; std::string filter;
  for (int i = 1; i < argc; ++i) {
    std::string a = argv[i];
    if (a == "--full") full = true;
    else if (a == "--identity") identity = true;
    else if (a == "--allow-missing-fixtures") tk::allow_missing_fixtures() = true;
    else filter = a;
  }
  int ran = 0, failed_cases = 0;
  for (auto& c : tk::registry()) {
    if (!filter.empty() && std::string(c.name).find(filter) == std::string::npos) continue;
    if (!full && std::strcmp(c.tags, "full") == 0) continue;
    if ((std::strcmp(c.tags, "identity") == 0) != identity) continue;   // identity tests: only with --identity, and then only them
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
