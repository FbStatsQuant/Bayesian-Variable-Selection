// bench_score.cpp -- ns per score of Scorer<Arith::Bit> (compat, Gram-free, one thread) on a data.bin.
// Usage: v4_bench_score data.bin [k=5] [reps=20000]. Random sorted models of size k (fixed seed).
#include <chrono>
#include <cstdio>
#include <random>
#include "v4/prep.h"
#include "v4/score.h"
using namespace v4;
int main(int argc, char** argv) {
  if (argc < 2) { std::fprintf(stderr, "usage: v4_bench_score data.bin [k] [reps]\n"); return 2; }
  Data D = prep::load_data(argv[1]);
  int k = argc > 2 ? std::atoi(argv[2]) : 5, reps = argc > 3 ? std::atoi(argv[3]) : 20000;
  std::mt19937_64 g(1); std::vector<Model> ms(reps);
  for (auto& S : ms) { while ((int)S.size() < k) { int j = (int)(g() % D.p); if (!std::binary_search(S.begin(), S.end(), j)) sorted_insert(S, j); } }
  BitScorer sc(&D); double sink = 0;
  auto t0 = std::chrono::steady_clock::now();
  for (auto& S : ms) sink += sc.score(S).logm;
  double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count() / reps;
  std::printf("{\"n\":%d,\"p\":%d,\"k\":%d,\"reps\":%d,\"ns_per_score\":%.0f,\"sink\":%.6g}\n", D.n, D.p, k, reps, ns, sink);
}
