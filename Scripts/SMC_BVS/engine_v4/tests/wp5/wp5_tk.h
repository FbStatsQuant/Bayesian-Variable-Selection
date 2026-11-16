// wp5_tk.h -- minimal test harness for the WP5 tests (WP1's tests/tk.h replaces it when the skeleton lands).
#pragma once
#include <cmath>
#include <cstdio>
#include <functional>
#include <string>
#include <vector>

namespace tk {
struct Case { const char* name; std::function<void()> fn; bool slow; };
inline std::vector<Case>& registry() { static std::vector<Case> r; return r; }
struct Reg { Reg(const char* n, std::function<void()> f, bool slow = false) { registry().push_back({n, f, slow}); } };
inline int& failures() { static int f = 0; return f; }
inline bool& quick() { static bool q = false; return q; }
inline void fail(const char* file, int line, const std::string& msg) { ++failures(); std::printf("    FAIL %s:%d %s\n", file, line, msg.c_str()); }
}  // namespace tk
#define TK_CAT2(a, b) a##b
#define TK_CAT(a, b) TK_CAT2(a, b)
#define TEST(name) static void name(); static tk::Reg TK_CAT(reg_, name)(#name, name); static void name()
#define TEST_SLOW(name) static void name(); static tk::Reg TK_CAT(reg_, name)(#name, name, true); static void name()
#define CHECK(c) do { if (!(c)) tk::fail(__FILE__, __LINE__, #c); } while (0)
#define CHECK_MSG(c, m) do { if (!(c)) tk::fail(__FILE__, __LINE__, std::string(#c) + " : " + (m)); } while (0)
#define CHECK_NEAR(a, b, tol) do { double _a = (a), _b = (b); if (!(std::fabs(_a - _b) <= (tol))) { char _m[256]; std::snprintf(_m, sizeof _m, "%s=%.17g %s=%.17g tol=%.3g", #a, _a, #b, _b, (double)(tol)); tk::fail(__FILE__, __LINE__, _m); } } while (0)
#define CHECK_THROWS(stmt) do { bool _t = false; try { stmt; } catch (...) { _t = true; } if (!_t) tk::fail(__FILE__, __LINE__, "expected throw: " #stmt); } while (0)
