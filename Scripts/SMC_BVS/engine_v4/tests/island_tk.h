// island_tk.h -- minimal test harness for the WP3 island tests (WP1's tests/tk.h replaces it when it lands).
#pragma once
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <string>
#include <vector>

namespace tk {
struct Case { std::string name; std::function<void()> fn; };
inline std::vector<Case>& cases() { static std::vector<Case> c; return c; }
inline int& failures() { static int f = 0; return f; }
inline int& checks() { static int c = 0; return c; }
struct Reg { Reg(const char* n, std::function<void()> f) { cases().push_back({n, f}); } };
inline int run_all(int argc, char** argv) {
  std::string filter = argc > 1 ? argv[1] : "";
  int ran = 0, failed_cases = 0;
  for (auto& c : cases()) {
    if (!filter.empty() && c.name.find(filter) == std::string::npos) continue;
    int f0 = failures();
    std::printf("[ RUN  ] %s\n", c.name.c_str()); std::fflush(stdout);
    c.fn();
    bool ok = failures() == f0;
    std::printf("[ %s ] %s\n", ok ? " OK " : "FAIL", c.name.c_str()); std::fflush(stdout);
    ++ran; if (!ok) ++failed_cases;
  }
  std::printf("%d cases, %d failed, %d checks, %d failed checks\n", ran, failed_cases, checks(), failures());
  return failed_cases ? 1 : 0;
}
}  // namespace tk
#define TK_CAT2(a, b) a##b
#define TK_CAT(a, b) TK_CAT2(a, b)
#define TEST(name) static void name(); static tk::Reg TK_CAT(reg_, name)(#name, name); static void name()
#define CHECK(cond) do { ++tk::checks(); if (!(cond)) { ++tk::failures(); std::printf("  CHECK failed %s:%d: %s\n", __FILE__, __LINE__, #cond); } } while (0)
#define CHECK_MSG(cond, ...) do { ++tk::checks(); if (!(cond)) { ++tk::failures(); std::printf("  CHECK failed %s:%d: %s -- ", __FILE__, __LINE__, #cond); std::printf(__VA_ARGS__); std::printf("\n"); } } while (0)
