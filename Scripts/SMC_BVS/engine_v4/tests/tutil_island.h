// tutil_island.h -- printf-style message helper for the WP3 tests on WP1's harness (tests/tk.h).
#pragma once
#include <cstdarg>
#include <cstdio>
#include <string>
inline std::string tk_fmt(const char* f, ...) {
  char b[1024]; va_list ap; va_start(ap, f); std::vsnprintf(b, sizeof b, f, ap); va_end(ap); return b;
}
#define CHECKF(c, ...) CHECK_MSG(c, tk_fmt(__VA_ARGS__))
