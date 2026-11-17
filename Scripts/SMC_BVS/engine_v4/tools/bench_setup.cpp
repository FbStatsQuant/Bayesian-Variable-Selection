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

// Production start law at (design, p, n): partition (as count-only), tables without stores, start law. Reports the size
// law of pi_0 (mean, quantiles) and the expected number of blocks a pi_0 draw touches, exactly:
//   E #touched = sum_b (1 - P(k_b = 0)),  P(k_b = 0) = sum_k varpi(k) F_{-b}(k) / Zbar_0,
//   F_{-b} = (prefix convolution of blocks < b) * (suffix convolution of blocks > b), in log space.
// mc > 0: also that many pi_0 draws (addressed uniforms) as a Monte Carlo cross-check.
static int startlaw_main(int argc, char** argv) {
  v4::gen::Spec sp; sp.design = v4::gen::design_from_name(argv[2]); sp.p = std::atoi(argv[3]); sp.n = std::atoi(argv[4]);
  int th = argc > 5 ? std::atoi(argv[5]) : 3; sp.seed = argc > 6 ? (uint32_t)std::atoi(argv[6]) : 1u;
  int mc = argc > 7 ? std::atoi(argv[7]) : 0;
  if (sp.design == v4::gen::Design::BLK) sp.rho = 0.5;
  auto t0 = std::chrono::steady_clock::now();
  auto lap = [&]() { double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count(); t0 = std::chrono::steady_clock::now(); return s; };
  auto own = std::make_shared<v4::DataOwned>();
  v4::gen::generate(sp, own->X, own->y);
  std::vector<double> z(sp.n);
  for (int j = 0; j < sp.p; ++j) { double* x = &own->X[(size_t)j * sp.n]; v4::prep::standardise(x, sp.n, z.data()); std::copy(z.begin(), z.end(), x); }
  v4::prep::standardise(own->y.data(), sp.n, z.data()); std::copy(z.begin(), z.end(), own->y.begin());
  v4::Data D = v4::make_data(own, sp.n, sp.p);
  double t_gen = lap();
  PartitionOptions po;
  CountResult c = count_only(D, po, default_B(sp.n, sp.p), th);
  double t_part = lap();
  TableStats ts;
  Tables T = build_tables(D, c.part, th, nullptr, &ts);
  double t_tab = lap();
  build_start(D, c.part, T);
  double t_start = lap();
  const int K = D.K, J = T.J;
  // size law
  std::vector<double> P(K + 1);
  double mean = 0, cum = 0; int q50 = -1, q90 = -1, q99 = -1;
  for (int k = 0; k <= K; ++k) { P[k] = std::exp(T.size_logmass[k]); mean += k * P[k]; }
  for (int k = 0; k <= K; ++k) { cum += P[k]; if (q50 < 0 && cum >= 0.5) q50 = k; if (q90 < 0 && cum >= 0.9) q90 = k; if (q99 < 0 && cum >= 0.99) q99 = k; }
  // suffix convolutions G[b][k] (blocks b..J-1), log space
  std::vector<double> G((size_t)(J + 1) * (K + 1), v4::NEG_INF);
  G[(size_t)J * (K + 1)] = 0.0;
  std::vector<double> t;
  for (int b = J - 1; b >= 0; --b) {
    const double* pr = &T.logprof[T.logprof_ptr[b]]; int npr = (int)(T.logprof_ptr[b + 1] - T.logprof_ptr[b]);
    for (int k = 0; k <= K; ++k) {
      t.clear();
      for (int j = 0; j < npr && j <= k; ++j) { double g = G[(size_t)(b + 1) * (K + 1) + k - j]; if (g != v4::NEG_INF) t.push_back(pr[j] + g); }
      G[(size_t)b * (K + 1) + k] = t.empty() ? v4::NEG_INF : v4::log_sum_exp(t);
    }
  }
  std::vector<double> p0(J);
#pragma omp parallel for num_threads(th) schedule(dynamic, 64)
  for (int b = 0; b < J; ++b) {
    std::vector<double> tt, outer;
    for (int k = 0; k <= K; ++k) {   // log F_{-b}(k) = LSE_i logF[b][i] + G[b+1][k-i]
      tt.clear();
      for (int i = 0; i <= k; ++i) { double a = T.logF_at(b, i), g = G[(size_t)(b + 1) * (K + 1) + k - i]; if (a != v4::NEG_INF && g != v4::NEG_INF) tt.push_back(a + g); }
      if (!tt.empty()) outer.push_back(D.logprior[k] + v4::log_sum_exp(tt));
    }
    p0[b] = outer.empty() ? 0.0 : std::exp(v4::log_sum_exp(outer) - T.logZbar0);
  }
  double touched = 0; for (int b = 0; b < J; ++b) touched += 1.0 - p0[b];
  double t_touch = lap();
  v4::Json rec = v4::Json::object();
  rec["design"] = v4::gen::design_name(sp.design); rec["n"] = sp.n; rec["p"] = sp.p; rec["K"] = K; rec["J"] = J; rec["B_blocks"] = c.part.B;
  rec["C"] = T.code_ptr.back(); rec["logZbar0"] = T.logZbar0;
  rec["E_size"] = mean; rec["q50"] = q50; rec["q90"] = q90; rec["q99"] = q99; rec["P_size0"] = P[0];
  rec["E_blocks_touched"] = touched;
  if (mc > 0) {   // Monte Carlo cross-check with pi_0 draws
    Start S; S.D = &D; S.P = &c.part; S.T = &T; S.logZbar0 = T.logZbar0;
    v4::AddressedSource as; v4::Model M; double ms = 0, mb = 0;
    auto td = std::chrono::steady_clock::now();
    for (int i = 1; i <= mc; ++i) { v4::Address ad; ad.seed = 9; ad.xph = v4::X_INIT; ad.particle = (uint32_t)i; S.draw_pi0(as, ad, M); }
    rec["mc_us_per_draw"] = 1e6 * std::chrono::duration<double>(std::chrono::steady_clock::now() - td).count() / mc;   // D-31 path
    if (argc > 8 && std::string(argv[8]) == "stored") {   // D-31 check: the stored rows (old layout) give the same draws; their cost
      Tables Ts = T; build_start(D, c.part, Ts, /*store_sampler=*/true);
      Ts.cbs_ptr.assign(1, 0); Ts.codes_by_size.clear(); Ts.sub_ptr.assign(1, 0); Ts.sub_cum.clear();   // D-18 as in production
      Start S2 = S; S2.T = &Ts; v4::Model M2; bool same = true;
      td = std::chrono::steady_clock::now();
      for (int i = 1; i <= mc; ++i) { v4::Address ad; ad.seed = 9; ad.xph = v4::X_INIT; ad.particle = (uint32_t)i; S2.draw_pi0(as, ad, M2); }
      rec["mc_us_per_draw_stored_rows"] = 1e6 * std::chrono::duration<double>(std::chrono::steady_clock::now() - td).count() / mc;
      for (int i = 1; same && i <= mc; ++i) { v4::Address ad; ad.seed = 9; ad.xph = v4::X_INIT; ad.particle = (uint32_t)i; S.draw_pi0(as, ad, M); S2.draw_pi0(as, ad, M2); same = M == M2; }
      rec["mc_same_draws_stored_rows"] = same;
      rec["cond_cum_bytes_old"] = (int64_t)(8 * (Ts.cond_ptr.size() + Ts.cond_cum.size()));
    }
    rec["cond0_bytes"] = (int64_t)(8 * T.cond0.size());
    for (int i = 1; i <= mc; ++i) {
      v4::Address ad; ad.seed = 9; ad.xph = v4::X_INIT; ad.particle = (uint32_t)i;
      S.draw_pi0(as, ad, M);
      ms += (double)M.size();
      std::vector<int> bl; for (int32_t j : M) bl.push_back(c.part.blk[j]);
      std::sort(bl.begin(), bl.end()); mb += (double)(std::unique(bl.begin(), bl.end()) - bl.begin());
    }
    rec["mc_draws"] = mc; rec["mc_E_size"] = ms / mc; rec["mc_E_blocks_touched"] = mb / mc;
  }
  v4::Json sec = v4::Json::object(); sec["generate"] = t_gen; sec["partition"] = t_part; sec["tables"] = t_tab; sec["start_law"] = t_start; sec["touched"] = t_touch;
  rec["seconds"] = sec; rec["peak_rss_mb"] = peak_rss_mb(); rec["threads"] = th;
  std::printf("%s\n", rec.dump(1).c_str());
  return 0;
}

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
  if (what == "startlaw") return startlaw_main(argc, argv);
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
