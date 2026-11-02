// t33_harness.cpp -- W7-SEC. Compiles the PRODUCTION scorer (Scripts/SMC_BVS/core/cpp/v3_score.h, unmodified)
// and scores a list of models on stored data, printing every intermediate the T33 bound talks about.
// Input (binary, little endian): int32 n, int32 p, double X[n*p] (column-major), double y[n],
//   int32 nmodels, then per model: int32 k, int32 idx[k] (0-based, sorted).
// Output (text): header line with the data constants, then one line per model.
#include <cstdio>
#include <cstdint>
#include <vector>
#include "v3_score.h"

int main(int argc, char** argv) {
  if (argc < 2) { std::fprintf(stderr, "usage: t33_harness input.bin\n"); return 1; }
  FILE* f = std::fopen(argv[1], "rb");
  int32_t n, p; std::fread(&n, 4, 1, f); std::fread(&p, 4, 1, f);
  std::vector<double> X((size_t)n * p), y(n);
  std::fread(X.data(), 8, X.size(), f); std::fread(y.data(), 8, n, f);
  int32_t nm; std::fread(&nm, 4, 1, f);
  std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
  v3::Data D; v3::data_init(D, X.data(), y.data(), n, p, orig);
  std::printf("HEADER n=%d p=%d K=%d yty=%.17g logCn=%.17g logm0=%.17g logWK=%.17g\n", n, p, D.K, D.yty, D.logCn, D.logm0, D.logWK);
  std::printf("LOGPRIOR");
  for (int k = 0; k <= D.K; ++k) std::printf(" %.17g", D.logprior[k]);
  std::printf("\n");
  v3::Scorer sc(&D);
  for (int m = 0; m < nm; ++m) {
    int32_t k; std::fread(&k, 4, 1, f);
    std::vector<int> S(k); for (int a = 0; a < k; ++a) { int32_t t; std::fread(&t, 4, 1, f); S[a] = t; }
    try {
      v3::ScoreOut o = sc.score(S);
      double F = D.logprior[k] + o.logm;
      std::printf("M %d %d %.17g %.17g %.17g %.17g %.17g %.17g %d %d %.17g %.17g\n", m, k, o.logm, F, o.Q, o.logdetH, o.logdetA,
                  o.cond_H, o.route, (int)o.q_recomputed, sc.error_bound(o, k), o.cond_A);
    } catch (std::exception& e) {
      std::printf("M %d %d FAIL %s\n", m, k, e.what());
    }
  }
  std::fclose(f);
  return 0;
}
