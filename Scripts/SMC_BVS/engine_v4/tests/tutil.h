// tutil.h -- test helpers: temp paths under $TMPDIR, small deterministic datasets.
#pragma once
#include <cstdlib>
#include <string>
#include <unistd.h>
#include <vector>
#include "v4/gen.h"
#include "v4/prep.h"

inline std::string tmp_path(const std::string& name) {
  const char* t = std::getenv("TMPDIR");
  std::string d = t ? t : ".";
  return d + "/v4test_" + std::to_string(::getpid()) + "_" + name;
}
// Standardised dataset from the generator (design, n, p, seed) through prep.
inline v4::Data make_test_data(v4::gen::Design d, int n, int p, uint32_t seed, double a = 1.0) {
  v4::gen::Spec s; s.design = d; s.n = n; s.p = p; s.seed = seed; s.a = a; if (d == v4::gen::Design::BLK) s.rho = 0.5;
  std::vector<double> X, y; v4::gen::generate(s, X, y);
  v4::prep::Result r = v4::prep::preprocess(X.data(), y.data(), n, p);
  return v4::make_data(r.own, n, r.p);
}
