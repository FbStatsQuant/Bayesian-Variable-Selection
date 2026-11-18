// wp5_tk.h -- WP5 additions to WP1's tests/tk.h (tolerance check; slow tests run with `v4_tests --full`).
#pragma once
#include <cmath>
#include <cstdio>

#include "tk.h"
#define TEST_SLOW(name) TEST_TAGGED(name, "full")
#define CHECK_NEAR(a, b, tol) do { double _a = (a), _b = (b); if (!(std::fabs(_a - _b) <= (tol))) { char _m[256]; std::snprintf(_m, sizeof _m, "%s=%.17g %s=%.17g tol=%.3g", #a, _a, #b, _b, (double)(tol)); tk::fail(__FILE__, __LINE__, _m); } } while (0)
