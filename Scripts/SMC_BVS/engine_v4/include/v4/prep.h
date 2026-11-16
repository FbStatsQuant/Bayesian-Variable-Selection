// prep.h -- preprocessing (ENGINEERING_SPEC §1 row 1): drop exactly-constant columns, standardise X and y with the
// arithmetic of core/v3_preprocess.R:24-51 (v3_standardise; R's long-double two-pass mean and long-double sum),
// build data.bin. Class B against R by test (tests/test_prep.cpp on fixtures written by tools/make_fixtures.R). If a platform ever
// fails that test, `prep --from-r <dir>` takes the R-standardised X instead and the C++ path is declared class A.
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "v4/data.h"
#include "v4/json.h"

namespace v4::prep {

struct ColStd { double max = 0, mean = 0, sd = 0; bool anchored = false; };
// R's mean(x) for a double vector (src/main/summary.c real_mean, R 4.x): long double sum / n, then one long-double
// correction pass  s += sum(x_i - s) / n.
double r_mean(const double* x, size_t n);
// R's sum(x) for doubles (summary.c rsum): long double accumulation, rounded once.
double r_sum(const double* x, size_t n);
// v3_standardise (core/v3_preprocess.R:24-51) of x (length n) into z.
ColStd standardise(const double* x, size_t n, double* z);

struct Result {
  std::string status = "ok";               // ok | invalid_input | no_predictors | y_constant
  std::string reason;
  int32_t n = 0, p_raw = 0, p = 0;
  std::vector<int32_t> kept, dropped;      // 1-based
  std::shared_ptr<DataOwned> own;          // Xs, ys, col stats (filled when ok)
  ColStd ystd;
};
// core/v3_preprocess.R:94-131 (v3_preprocess without the duplicate check; WP2 computes duplicates in setup).
Result preprocess(const double* X, const double* y, int32_t n, int32_t p_raw);
// Write data.bin (sections per INTERFACES §5.1); returns the content hash.
std::string write_data(const std::string& path, const Data& D, const Result& r, const std::string& prep_class,
                       const Json& inputs);
// Load data.bin as a Data view over the mapped file.
Data load_data(const std::string& path, std::string* content_hash = nullptr);
// prep command (args: in = raw.bin | from_r = dir, out = data.bin).
Json run(const Json& args);

}  // namespace v4::prep
