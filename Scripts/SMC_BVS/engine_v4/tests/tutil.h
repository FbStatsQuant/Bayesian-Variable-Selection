// tutil.h -- test helpers: temp paths under $TMPDIR, small deterministic datasets.
#pragma once
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <system_error>
#include <thread>
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
// Remove temp files / directories without failing the test: cleanup is not what tests check. On NFS a file that is
// still open or mapped leaves a ".nfs*" placeholder until the handle closes, so callers release their handles first
// (inner scope) and this retries a few times with a short back-off, then only prints a note.
inline void remove_quietly(const std::vector<std::string>& paths) {
  for (int attempt = 0; attempt < 5; ++attempt) {
    bool left = false;
    for (auto& p : paths) {
      std::error_code ec;
      std::filesystem::remove_all(p, ec);
      if (std::filesystem::exists(p, ec)) left = true;
    }
    if (!left) return;
    std::this_thread::sleep_for(std::chrono::milliseconds(200 * (attempt + 1)));
  }
  std::printf("    note: some temp files could not be removed yet (NFS placeholder?), first: %s\n", paths.empty() ? "" : paths[0].c_str());
}

// Standardised dataset from the generator (design, n, p, seed) through prep.
inline v4::Data make_test_data(v4::gen::Design d, int n, int p, uint32_t seed, double a = 1.0) {
  v4::gen::Spec s; s.design = d; s.n = n; s.p = p; s.seed = seed; s.a = a; if (d == v4::gen::Design::BLK) s.rho = 0.5;
  std::vector<double> X, y; v4::gen::generate(s, X, y);
  v4::prep::Result r = v4::prep::preprocess(X.data(), y.data(), n, p);
  return v4::make_data(r.own, n, r.p);
}
