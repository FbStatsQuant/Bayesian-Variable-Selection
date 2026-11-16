// tk.h -- minimal test harness (no external dependency). TEST(name) registers; CHECK / CHECK_EQ count failures.
#pragma once
#include <cstdio>
#include <cstring>
#include <functional>
#include <string>
#include <vector>

namespace tk {
struct Case { const char* name; std::function<void()> fn; const char* tags; };
inline std::vector<Case>& registry() { static std::vector<Case> r; return r; }
inline int& failures() { static int f = 0; return f; }
inline std::string& current() { static std::string c; return c; }
inline bool& allow_missing_fixtures() { static bool a = false; return a; }   // --allow-missing-fixtures
struct Reg { Reg(const char* n, const char* tags, std::function<void()> f) { registry().push_back({n, std::move(f), tags}); } };
inline void fail(const char* file, int line, const std::string& msg) {
  ++failures();
  std::fprintf(stderr, "  FAIL %s (%s:%d): %s\n", current().c_str(), file, line, msg.c_str());
}
}  // namespace tk

#define TK_CAT2(a, b) a##b
#define TK_CAT(a, b) TK_CAT2(a, b)
#define TEST_TAGGED(name, tags) static void name(); static tk::Reg TK_CAT(reg_, name)(#name, tags, name); static void name()
#define TEST(name) TEST_TAGGED(name, "quick")
#define CHECK(c) do { if (!(c)) tk::fail(__FILE__, __LINE__, "CHECK(" #c ")"); } while (0)
#define CHECK_MSG(c, m) do { if (!(c)) tk::fail(__FILE__, __LINE__, std::string("CHECK(" #c "): ") + (m)); } while (0)
#define CHECK_EQ(a, b) do { auto _a = (a); auto _b = (b); if (!(_a == _b)) tk::fail(__FILE__, __LINE__, std::string(#a " == " #b " : ") + std::to_string(_a) + " vs " + std::to_string(_b)); } while (0)
#define CHECK_THROWS(stmt) do { bool _t = false; try { stmt; } catch (...) { _t = true; } if (!_t) tk::fail(__FILE__, __LINE__, "expected throw: " #stmt); } while (0)
// bitwise double equality (NaN == NaN with the same payload)
inline bool same_bits(double a, double b) { uint64_t x, y; std::memcpy(&x, &a, 8); std::memcpy(&y, &b, 8); return x == y; }
