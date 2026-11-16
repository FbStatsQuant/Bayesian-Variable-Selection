// bench_setup.cpp -- WP2 stage timings and peak memory (ENGINEERING brief WP2 item 6). Labels: MEASURED on the machine
// it runs on. Usage:
//   v4_setup_bench full  <p> [n=200] [threads=3] [exact=0]    all stages of setup::run on AR(0.6)
//   v4_setup_bench corr  <p> [n=200] [threads=3] [ntiles=0]   correlation pass; ntiles > 0: only that many column
//                                                             tiles J (spread over the range), projected to the full pass
//   v4_setup_bench count <design> <p> <n> [threads=3] [seed=1] [bv_cap=14]   setup --count-only on WP1's generator
//                                                             (AR | IND | BLK | ADJOPP), X standardised in place
#include <chrono>
#include <cstdlib>
#include <unistd.h>
#include "setup_tk.h"
#include "tiles.h"
#include "v4/gen.h"
#include "v4/prep.h"

using namespace v4::setup;

static int count_main(int argc, char** argv) {
  v4::gen::Spec sp; sp.design = v4::gen::design_from_name(argv[2]); sp.p = std::atoi(argv[3]); sp.n = std::atoi(argv[4]);
  int th = argc > 5 ? std::atoi(argv[5]) : 3; sp.seed = argc > 6 ? (uint32_t)std::atoi(argv[6]) : 1u;
  int bv = argc > 7 ? std::atoi(argv[7]) : 14;
  if (sp.design == v4::gen::Design::BLK) sp.rho = 0.5;
  auto t0 = std::chrono::steady_clock::now();
  auto own = std::make_shared<v4::DataOwned>();
  v4::gen::generate(sp, own->X, own->y);
  double tg = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  // standardise in place, column by column (the arithmetic of prep: v3_standardise, core/v3_preprocess.R:24-51)
  std::vector<double> z(sp.n);
  for (int j = 0; j < sp.p; ++j) { double* x = &own->X[(size_t)j * sp.n]; v4::prep::standardise(x, sp.n, z.data()); std::copy(z.begin(), z.end(), x); }
  v4::prep::standardise(own->y.data(), sp.n, z.data()); std::copy(z.begin(), z.end(), own->y.begin());
  v4::Data D = v4::make_data(own, sp.n, sp.p);
  double ts = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count() - tg;
  PartitionOptions po; po.bv_cap = bv;
  CountResult c = count_only(D, po, default_B(sp.n, sp.p), th);
  v4::Json rec = v4::Json::object();
  rec["design"] = v4::gen::design_name(sp.design); rec["n"] = sp.n; rec["p"] = sp.p; rec["seed"] = (int64_t)sp.seed; rec["threads"] = th;
  char host[256] = {}; gethostname(host, sizeof host - 1); rec["host"] = host;
  rec["accounting"] = c.acc.to_json(); rec["filter_used"] = c.filter_used; rec["filter_candidates"] = (int64_t)c.candidates;
  rec["r_n"] = c.corr.rn; rec["dup_components"] = c.corr.dup.rows();
  v4::Json s = v4::Json::object(); s["generate"] = tg; s["standardise"] = ts; s["edges"] = c.seconds_edges; s["partition"] = c.seconds_partition;
  rec["seconds"] = s; rec["peak_rss_mb"] = peak_rss_mb();
  std::printf("%s\n", rec.dump(1).c_str());
  return 0;
}

int main(int argc, char** argv) {
  if (argc < 3) { std::fprintf(stderr, "usage: see header\n"); return 2; }
  std::string what = argv[1];
  if (what == "count") return count_main(argc, argv);
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
    std::printf("accounting: C=%lld J=%lld B_blocks=%lld peak=%.0f MB setup_bin=%.0f MB (stage peaks:", (long long)r.acc.C, (long long)r.acc.J,
                (long long)r.acc.B_blocks, r.acc.peak / 1e6, r.acc.setup_bin / 1e6);
    for (auto& sp : r.acc.stage_peak) std::printf(" %s %.0f", sp.first.c_str(), sp.second / 1e6);
    std::printf(")\n");
    for (const auto* st : {&r.stores.top, &r.stores.lead0, &r.stores.lead1})
      std::printf("store: entries %zu pool %zu ints (mean |S| %.2f) bytes %.0f MB\n", st->v.size(), st->pool.size(),
                  st->v.size() ? (double)st->pool.size() / st->v.size() : 0.0, (st->v.size() * 26.0 + st->pool.size() * 4.0) / 1e6);
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
