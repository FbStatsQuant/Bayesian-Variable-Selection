// bench_setup.cpp -- WP2 stage timings and peak memory (ENGINEERING brief WP2 item 6). Labels: MEASURED on the machine
// it runs on. Usage:
//   v4_setup_bench full  <p> [n=200] [threads=3] [exact=0]    all stages of setup::run on AR(0.6)
//   v4_setup_bench corr  <p> [n=200] [threads=3] [ntiles=0]   correlation pass; ntiles > 0: only that many column
//                                                             tiles J (spread over the range), projected to the full pass
#include <chrono>
#include <cstdlib>
#include <unistd.h>
#include "setup_tk.h"
#include "tiles.h"

using namespace v4::setup;

int main(int argc, char** argv) {
  if (argc < 3) { std::fprintf(stderr, "usage: see header\n"); return 2; }
  std::string what = argv[1];
  int p = std::atoi(argv[2]), n = argc > 3 ? std::atoi(argv[3]) : 200, th = argc > 4 ? std::atoi(argv[4]) : 3;
  int extra = argc > 5 ? std::atoi(argv[5]) : 0;
  char host[256] = {}; gethostname(host, sizeof host - 1);
  auto t0 = std::chrono::steady_clock::now();
  stk::Fixture F(stk::AR, n, p, 2026);
  double tgen = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  std::printf("# host=%s design=AR(0.6) n=%d p=%d threads=%d gen_seconds=%.2f rss_after_gen_mb=%.0f\n", host, n, p, th, tgen, peak_rss_mb());
  if (what == "full") {
    SetupOptions o; o.threads = th; o.part.mode = extra ? PartMode::Exact : PartMode::Truncated;
    SetupResult r = run_setup(F.D(), o);
    std::printf("status=%s %s B=%d J=%d edges_kept=? nb_entries=%zu dup=%lld cut_groups=%lld table_codes=%lld mode_|S|=%zu ties=%ld\n",
                v4::status_name(r.status), r.reason.c_str(), r.B, r.part.J, r.corr.nb.idx.size(), (long long)r.corr.dup.rows(),
                (long long)r.cut.rows(), (long long)(r.tab.code_ptr.empty() ? 0 : r.tab.code_ptr.back()), r.mode.S.size(), r.mode.ties);
    std::printf("stage\tp\tn\tthreads\tseconds\tpeak_rss_mb\n");
    for (auto& t : r.timings) std::printf("%s\t%d\t%d\t%d\t%.3f\t%.0f\n", t.name.c_str(), p, n, th, t.seconds, t.peak_rss_mb);
    std::printf("tables: scored %llu prefix %llu fallback %llu; stores %.3f s\n", (unsigned long long)r.tstats.scored,
                (unsigned long long)r.tstats.prefix_scored, (unsigned long long)r.tstats.fallback_scored, r.tstats.seconds_stores);
    std::string path = std::string(std::getenv("TMPDIR") ? std::getenv("TMPDIR") : ".") + "/bench_setup.bin";
    auto t1 = std::chrono::steady_clock::now();
    if (r.status == v4::Status::completed) {
      std::string h = write_setup_bin(path, F.D(), r, o, "bench");
      FILE* f = std::fopen(path.c_str(), "rb"); std::fseek(f, 0, SEEK_END); long sz = std::ftell(f); std::fclose(f);
      std::printf("setup.bin\t%d\t%d\t%d\t%.3f\t%.0f\tbytes=%ld\n", p, n, th, std::chrono::duration<double>(std::chrono::steady_clock::now() - t1).count(), peak_rss_mb(), sz);
      std::remove(path.c_str());
    }
    return r.status == v4::Status::completed ? 0 : 1;
  }
  // correlation pass
  const int tile = 256, nt = (p + tile - 1) / tile;
  if (extra <= 0) {
    CorrOptions o; o.B = default_B(n, p); o.threads = th;
    CorrResult C = correlation_pass(F.D(), o);
    std::printf("corr_full\t%d\t%d\t%d\t%.3f\t%.0f\tpairs=%llu edges=%zu ns_per_pair_thread=%.3f\n", p, n, th, C.seconds, peak_rss_mb(),
                (unsigned long long)C.pairs, C.edges.size(), C.seconds * th * 1e9 / (double)C.pairs);
    return 0;
  }
  // sampled tiles: the kernel and the top-B/edge sink of the real pass, on `extra` tiles spread over [0, nt)
  std::vector<int> jt;
  for (int i = 0; i < extra; ++i) jt.push_back((int)((long)(nt - 1) * (extra - i) / extra));
  std::vector<double> s(p); for (int j = 0; j < p; ++j) s[j] = std::sqrt(F.D().diagG[j]);
  std::vector<uint64_t> pairs(th, 0); std::vector<double> sink(th, 0);
  auto t1 = std::chrono::steady_clock::now();
  detail::tile_pass(F.D(), tile, th, [&](int tid, int j, int l0, int cnt, const double* G) {
    double a = 0; for (int t = 0; t < cnt; ++t) a += std::fabs(G[t] / (s[j] * s[l0 + t]));
    sink[tid] += a; pairs[tid] += cnt;
  }, &jt);
  double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - t1).count();
  uint64_t P = 0; for (auto c : pairs) P += c;
  double total = (double)p * (p - 1) / 2;
  std::printf("corr_sampled\t%d\t%d\t%d\t%.3f\t%.0f\ttiles=%d pairs=%llu ns_per_pair_thread=%.3f projected_full_seconds=%.0f (ESTIMATE)\n", p, n, th, sec,
              peak_rss_mb(), extra, (unsigned long long)P, sec * th * 1e9 / (double)P, sec / (double)P * total);
  return 0;
}
