// sm_harness.cpp -- drives the FROZEN start_mode (v2.2.1 tree, read-only include) on batches of instances.
// Build (see build.sh): g++ -O2 -std=c++17 -msse2 -mfpmath=sse -ffp-contract=off -I<frozen cpp dir> sm_harness.cpp
//
// Input (stdin), a sequence of instances. Each instance starts with a line "T" (TABLE mode) or "D" (DATA mode).
// TABLE:  T id p K J cap
//         K+1 doubles: logprior[0..K]
//         for each block b = 0..J-1:  m  idx_0 .. idx_{m-1}      (increasing internal indices)
//                                     2^m doubles: logr[b][code], code = 0..2^m-1 (entries with popcount > K ignored, write nan)
// DATA:   D id n p B cap
//         n*p doubles X (column-major, already standardised), n doubles y (standardised)
// Output, one line per instance:
//   R id lg0(%a hex) ties truncated |S| S...
// In DATA mode, before the R line, the code's own tables are printed:
//   K K ; P logprior(hex)... ; per block: B m idx... ; L logr(hex) per code (nan if not scored)
// Doubles are read with strtod (accepts hex-float), printed with %a so Python reads them exactly.
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include "v3_start.h"

using namespace v3;

static double rd(std::istream& in) { std::string s; in >> s; return std::strtod(s.c_str(), nullptr); }

static void print_result(const std::string& id, const ModeResult& m) {
  std::printf("R %s %a %ld %d %d", id.c_str(), m.lg0, m.ties, m.truncated ? 1 : 0, (int)m.S.size());
  for (int j : m.S) std::printf(" %d", j);
  std::printf("\n");
}

int main() {
  std::ios::sync_with_stdio(false);
  std::string tag;
  while (std::cin >> tag) {
    if (tag == "T") {
      std::string id; int p, K, J; long cap;
      std::cin >> id >> p >> K >> J >> cap;
      Data D; D.n = 2 * K + 2; D.p = p; D.K = K;
      D.logprior.assign(K + 1, 0.0);
      for (int k = 0; k <= K; ++k) D.logprior[k] = rd(std::cin);
      Start st; st.D = &D;
      st.blocks.assign(J, {});
      st.logr.assign(J, {});
      for (int b = 0; b < J; ++b) {
        int m; std::cin >> m;
        st.blocks[b].resize(m);
        for (int i = 0; i < m; ++i) std::cin >> st.blocks[b][i];
        st.logr[b].assign(1u << m, 0.0);
        for (uint32_t c = 0; c < (1u << m); ++c) st.logr[b][c] = rd(std::cin);
        st.logr[b][0] = 0.0;
      }
      st.J = J;
      st.blk.assign(p, -1); st.pos.assign(p, -1);
      for (int b = 0; b < J; ++b) for (size_t i = 0; i < st.blocks[b].size(); ++i) { st.blk[st.blocks[b][i]] = b; st.pos[st.blocks[b][i]] = (int)i; }
      build_start(st);  // codes_by_size, logprof (as in the method; start_mode reads codes_by_size and logprof sizes)
      ModeResult m = start_mode(st, cap);
      print_result(id, m);
    } else if (tag == "D") {
      std::string id; int n, p, B; long cap;
      std::cin >> id >> n >> p >> B >> cap;
      std::vector<double> X((size_t)n * p), y(n);
      for (auto& v : X) v = rd(std::cin);
      for (auto& v : y) v = rd(std::cin);
      std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
      Data D; data_init(D, X.data(), y.data(), n, p, orig);
      Scorer sc(&D);
      Start st; st.D = &D;
      st.blocks = make_blocks(D, B);
      build_tables(st, sc);
      build_start(st);
      ModeResult m = start_mode(st, cap);
      std::printf("K %d\nP", D.K);
      for (double v : D.logprior) std::printf(" %a", v);
      std::printf("\n");
      for (int b = 0; b < st.J; ++b) {
        std::printf("B %d", (int)st.blocks[b].size());
        for (int j : st.blocks[b]) std::printf(" %d", j);
        std::printf("\nL");
        for (double v : st.logr[b]) { if (std::isnan(v)) std::printf(" nan"); else std::printf(" %a", v); }
        std::printf("\n");
      }
      print_result(id, m);
    } else {
      std::fprintf(stderr, "bad tag %s\n", tag.c_str()); return 1;
    }
  }
  return 0;
}
