// test_merge_mem.cpp -- the merge's memory plan against the merge's measured peak (WP4; the first 1M fit's merge peaked at
// 75.1 GiB RSS against a plan of 43.7 GiB). A scaled probe writes the merge's inputs with the SHAPES of a 10^6 run:
//   data.bin (n x p), setup.bin (blocks of B = 14: logr 2^14 codes per block, three table stores at their caps 40p + 1 /
//   20p / 20p), calib.bin (the calibration's three stores and 2c inherited models, flat), R' island_r.bin with FULL stores
//   (c = 40p + 1 distinct models, mean |S| about 7, as the pilot's 40,000,001 entries at k = 7.25) and an offer floor.
// then runs the real `smcbvs4 merge` as a subprocess and reads the phase records it writes (meta.timings.phases: seconds
// and RSS per phase) and its peak. Values are random, not scores: the probe measures memory and time, not statistics.
//   * TEST wp4_merge_mem_plan_bounds_peak (default suite, p = 4000): the plan bounds the measured peak (>= 1.1x).
//   * TEST wp4_merge_mem_probe (only with V4_MEM_PROBE_P = p [V4_MEM_PROBE_R = R'] [V4_MEM_PROBE_DIR = keep the files]):
//     prints the phases, the plan and the per-component accounting; used to size the 10^6 request.
#include <sys/stat.h>
#include <sys/wait.h>
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <numeric>
#include <random>
#include "tk.h"
#include "tutil.h"
#include "v4/gen.h"
#include "v4/merge.h"
#include "v4/offer_floor.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"
using namespace v4;

namespace {
struct Probe {
  std::string dir, dpath, spath, cpath, dhash, shash, chash;
  std::vector<std::string> ipath;
  int p = 0, n = 0, R = 0, K = 0; uint64_t c = 0;
  uint64_t bytes_data = 0, bytes_setup = 0, bytes_calib = 0, bytes_island = 0;
  size_t n_inherited = 0; double kbar_island = 0;
};
const Json& clean_block() {
  static Json b = [] { Json x = binary_block(); x["git_commit"] = "0123456789abcdef0123456789abcdef01234567"; return x; }();
  return b;
}
uint64_t file_size(const std::string& f) { struct stat st{}; return ::stat(f.c_str(), &st) == 0 ? (uint64_t)st.st_size : 0; }
// a random model of size 3..11 (mean 7) over [0, p)
Model rnd_model(std::mt19937_64& g, int p) {
  Model S; const int k = 3 + (int)(g() % 9);
  while ((int)S.size() < k) S.push_back((int32_t)(g() % (uint64_t)p));
  std::sort(S.begin(), S.end()); S.erase(std::unique(S.begin(), S.end()), S.end()); return S;
}

Probe make_probe(const std::string& dir, int p_raw, int R, int n) {
  Probe P; P.dir = dir; P.R = R; P.n = n;
  std::mt19937_64 g(20261118);
  gen::Spec sp; sp.design = gen::Design::AR; sp.n = n; sp.p = p_raw; sp.seed = 5; sp.s0 = 5; sp.a = 1.5;
  std::vector<double> X, y; gen::generate(sp, X, y);
  prep::Result pr = prep::preprocess(X.data(), y.data(), n, p_raw);
  X.clear(); X.shrink_to_fit();
  Data D = make_data(pr.own, n, pr.p);
  const int p = P.p = D.p; P.K = D.K; P.c = 40ull * (uint64_t)p + 1;
  P.dpath = dir + "/data.bin"; P.dhash = prep::write_data(P.dpath, D, pr, "B", Json::object());
  // ---- setup.bin: blocks of 14 (the last 1..14), logr = finite values, table stores at their caps
  wp4io::SetupView S;
  S.blk_ptr.push_back(0); S.code_ptr.push_back(0);
  std::vector<std::pair<int, int>> blocks;   // (first column, size)
  for (int j0 = 0; j0 < p; j0 += 14) blocks.push_back({j0, std::min(14, p - j0)});
  for (size_t b = 0; b < blocks.size(); ++b) {
    const int j0 = blocks[b].first, m = blocks[b].second;
    for (int i = 0; i < m; ++i) { S.blk.push_back((int32_t)b); S.pos.push_back(i); S.blk_members.push_back(j0 + i); }
    S.blk_ptr.push_back(j0 + m);
    S.logr.push_back(0.0);
    for (uint32_t cd = 1; cd < (1u << m); ++cd) S.logr.push_back(-0.5 - 1e-3 * (double)__builtin_popcount(cd) - 1e-9 * (double)(cd + 17 * b % 1000));
    S.code_ptr.push_back((int64_t)S.logr.size());
  }
  S.ttop.init(P.c, Order::HPM); S.tlead0.init(20ull * p, Order::LEX); S.tlead1.init(20ull * p, Order::LEX);
  {  // table models: per block the codes of popcount <= 3 first (the small subsets the tables rank highest), then 4, 5, ...
    uint64_t idx = 0;
    for (int pc = 0; pc <= 14 && idx < P.c; ++pc)
      for (size_t b = 0; b < blocks.size() && idx < P.c; ++b) {
        const int j0 = blocks[b].first, m = blocks[b].second;
        if (pc > m) continue;
        for (uint32_t cd = 0; cd < (1u << m) && idx < P.c; ++cd) {
          if (__builtin_popcount(cd) != pc) continue;
          Model U; for (int i = 0; i < m; ++i) if (cd & (1u << i)) U.push_back(j0 + i);
          const double F = -300.0 - 1e-6 * (double)idx, lg0 = -400.0 - 1e-6 * (double)idx;
          const uint64_t h = D.zob.hash(U);
          S.ttop.offer(F, U, h); if (idx < 20ull * p) { S.tlead0.offer(lg0, U, h); S.tlead1.offer(F, U, h); }
          ++idx;
        }
      }
  }
  S.code_ptr.size();
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  S.mode_S = Model(S.ttop.model(0).begin(), S.ttop.model(0).end());
  S.size_logmass.assign((size_t)D.K + 1, -std::numeric_limits<double>::infinity());
  { double tot = 0; for (int k = 0; k <= 12; ++k) { S.size_logmass[(size_t)k] = std::log(std::pow(0.5, k + 1)); tot += std::pow(0.5, k + 1); }
    for (int k = 0; k <= 12; ++k) S.size_logmass[(size_t)k] -= std::log(tot); }
  { Json sin = Json::object(); sin["data.bin"] = P.dhash; P.spath = dir + "/setup.bin"; P.shash = wp4io::write_setup_min(P.spath, S, sin); }
  // ---- calib.bin: 2c inherited models (flat, lexicographic), the calibration's three stores, HPM
  const size_t m_inh = (size_t)(2 * P.c); P.n_inherited = m_inh;
  calib::InheritedFlat flat;
  {
    std::vector<int32_t> pool; std::vector<int64_t> ptr; pool.reserve(m_inh * 8); ptr.reserve(m_inh + 1); ptr.push_back(0);
    for (size_t i = 0; i < m_inh; ++i) { Model M = rnd_model(g, p); pool.insert(pool.end(), M.begin(), M.end()); ptr.push_back((int64_t)pool.size()); }
    std::vector<uint32_t> ord(m_inh); std::iota(ord.begin(), ord.end(), 0u);
    auto view = [&](uint32_t i) { return ModelView(pool.data() + ptr[i], (uint32_t)(ptr[i + 1] - ptr[i])); };
    std::sort(ord.begin(), ord.end(), [&](uint32_t a, uint32_t b) { return lex_less(view(a), view(b)); });
    ord.erase(std::unique(ord.begin(), ord.end(), [&](uint32_t a, uint32_t b) { return same_model(view(a), view(b)); }), ord.end());
    flat.ptr.assign(1, 0); flat.idx.reserve(pool.size());
    std::uniform_real_distribution<double> U(0.0, 1.0);
    for (uint32_t i : ord) {
      ModelView v = view(i); flat.idx.insert(flat.idx.end(), v.begin(), v.end()); flat.ptr.push_back((int64_t)flat.idx.size());
      const double F = -2000.0 + 1750.0 * U(g);   // [-2000, -250]
      flat.F.push_back(F); flat.lg0.push_back(F - 100.0 * U(g)); flat.logm.push_back(F + 5.0); flat.d.push_back(U(g));
    }
    P.n_inherited = flat.size();
  }
  LedgerConfig cfg; cfg.p = p; cfg.islands = 4; cfg.leaders = true; cfg.fresh_counters = false;
  Ledger cl(cfg);
  {
    EventCtx e; e.phase = PH_PILOT; e.mech = ME_GIBBS_FLIP; e.phi = 0.25; e.key.seg = SG_CALIB; e.key.iter = 0; e.key.unit = 0; e.key.xph = X_BRIDGE;
    e.key.stage = 1; e.key.round = 1; e.key.particle = 1; e.key.position = 3;
    for (size_t i = 0; i < flat.size(); ++i) {
      ModelView v = flat.model(i); const uint64_t h = D.zob.hash(v);
      cl.top.offer(flat.F[i], v, h); cl.lead1.offer(flat.F[i], v, h); cl.lead0.offer(flat.lg0[i], v, h);
    }
    size_t ib = 0; for (size_t i = 1; i < flat.size(); ++i) if (flat.F[i] > flat.F[ib]) ib = i;
    cl.offer_hpm(flat.model(ib), flat.F[ib], flat.logm[ib], e);
    cl.compact();
  }
  // tau_cal = the c-th best F of the inherited models (D-29)
  double tau = -std::numeric_limits<double>::infinity();
  if (flat.size() >= P.c) { std::vector<double> Fs = flat.F; std::nth_element(Fs.begin(), Fs.begin() + (long)(P.c - 1), Fs.end(), std::greater<double>()); tau = Fs[(size_t)P.c - 1]; }
  calib::CalibOut co; co.status = calib::CalStatus::ok; co.tier_final = 0; co.has_frozen = true; co.rule = calib::Rule::bounded;
  calib::Settings cset; cset.rule = co.rule; cset.I_max = 1; cset.tiers[0].ell = 3; cset.tiers[0].H = 64; cset.tiers[0].Te = 40;
  const std::vector<double> grid{0, 0.3, 0.7, 1};
  co.frozen.grid = grid; co.frozen.grid_unrefined = grid; co.frozen.grid_label = "rebuild_1"; co.I_used = 1;
  calib::TierOut t0; t0.tier = 0; t0.has_triggers = true; calib::GridRecord gr; gr.label = "preliminary"; gr.grid = grid; t0.grids.push_back(gr);
  co.tiers.push_back(t0);
  const int Nfx = calib::V_N;
  {
    wp4io::CalibWrite cw; cw.mode = fmt::M_V; cw.co = &co; cw.led = &cl; cw.inherited_flat = &flat; cw.N = Nfx; cw.L = 4; cw.Hm = 4;
    cw.settings = &cset; cw.k_store = 7.25;
    cw.inputs["data.bin"] = P.dhash; cw.inputs["setup.bin"] = P.shash;
    P.cpath = dir + "/calib.bin"; P.chash = wp4io::write_calib(P.cpath, cw);
  }
  flat = calib::InheritedFlat(); cl = Ledger();
  // ---- islands: full stores of c distinct models above the floor tau_cal
  double ksum = 0;
  for (int r = 1; r <= R; ++r) {
    merge::IslandIn I; I.r = r; I.N = Nfx; I.T = 3; I.L = 4; I.Hm = 4; I.logZ = -30 + 0.07 * r; I.ess = {400, 450, 480};
    I.pip.resize((size_t)p); I.rb_acc.resize((size_t)p);
    for (int j = 0; j < p; ++j) { I.pip[(size_t)j] = std::fmod(0.017 * (j + 1) * (r + 3), 1.0); I.rb_acc[(size_t)j] = I.pip[(size_t)j] * 200; }
    I.rb_round.assign(4, std::vector<double>((size_t)p, 1.0));
    LedgerConfig ic = cfg; ic.leaders = false; ic.islands = std::max(4, R); I.led.init(ic);
    std::uniform_real_distribution<double> U(0.0, 1.0);
    const double lo = std::isfinite(tau) ? tau : -2000.0;
    for (uint64_t t = 0; t < P.c; ++t) {
      Model M = rnd_model(g, p); const double F = lo + (-245.0 - lo) * U(g);
      EventCtx e; e.phase = PH_MEASURED; e.mech = ME_GIBBS_FLIP; e.phi = 1; e.key.seg = SG_FINAL; e.key.unit = (uint32_t)r; e.key.xph = X_MEASURED;
      e.key.stage = 3; e.key.round = 1 + (uint32_t)(t / 100000); e.key.particle = 1 + (uint32_t)(t % 100000); e.key.position = 1 + (uint32_t)(g() % 30); e.key.sub = 1;
      I.led.event(M, D.zob.hash(M), F, F - 50.0, F + 3.0, e, true);
    }
    I.led.compact();
    for (int t = 0; t < Nfx; ++t) { ModelView v = I.led.top.model((size_t)(t * 7919ull % I.led.top.size())); I.terminal.emplace_back(v.begin(), v.end()); }
    ksum += (double)I.led.top.pool.size() / (double)std::max<size_t>(1, I.led.top.size());
    Json in = Json::object(); in["data.bin"] = P.dhash; in["setup.bin"] = P.shash; in["calib.bin"] = P.chash;
    const std::string ip = dir + "/island_" + std::to_string(r) + ".bin";
    if (std::isfinite(tau)) {   // the reference writer has no floor: copy the file with meta.offer_floor* (D-29)
      const std::string raw = ip + ".raw";
      wp4io::write_island(raw, fmt::M_V, I, in, &clean_block(), &grid);
      { fmt::Reader Rr(raw, false); fmt::Writer W(fmt::K_ISLAND, Rr.mode());
        for (const auto& e : Rr.sections()) {
          const std::string nm(e.name);
          if (e.dtype == fmt::D_JSON) { Json m = Rr.json(nm); if (nm == "meta") { OfferFloor of; of.f = tau; of.calib = P.chash; offer_floor_to_meta(m, of); } W.add_json(nm, m); continue; }
          const void* q = e.dtype == fmt::D_F64 ? (const void*)Rr.get<double>(nm) : e.dtype == fmt::D_I32 ? (const void*)Rr.get<int32_t>(nm)
                        : e.dtype == fmt::D_U32 ? (const void*)Rr.get<uint32_t>(nm) : e.dtype == fmt::D_I64 ? (const void*)Rr.get<int64_t>(nm)
                        : e.dtype == fmt::D_U64 ? (const void*)Rr.get<uint64_t>(nm) : e.dtype == fmt::D_U16 ? (const void*)Rr.get<uint16_t>(nm)
                        : (const void*)Rr.get<uint8_t>(nm);
          W.add_copy(nm, e.dtype, q, e.length, e.dims[0], e.dims[1]);
        }
        W.write(ip); }
      std::remove(raw.c_str());
    } else wp4io::write_island(ip, fmt::M_V, I, in, &clean_block(), &grid);
    P.ipath.push_back(ip);
  }
  P.kbar_island = ksum / R;
  P.bytes_data = file_size(P.dpath); P.bytes_setup = file_size(P.spath); P.bytes_calib = file_size(P.cpath); P.bytes_island = file_size(P.ipath[0]);
  return P;
}

// The merge as the CLI runs it; returns the exit code. The record (<out>.json) carries peak_rss_kb and meta.timings.phases.
int run_merge(const Probe& P, const std::string& out, int threads, uint64_t mem_budget = 0) {
  std::string isl; for (size_t i = 0; i < P.ipath.size(); ++i) isl += (i ? "," : "") + P.ipath[i];
  std::string cmd = std::string("'") + V4_SMCBVS4 + "' merge --data '" + P.dpath + "' --setup '" + P.spath + "' --calib '" + P.cpath + "' --mode V --threads " +
                    std::to_string(threads) + " --islands '" + isl + "' --Rp " + std::to_string(P.R) + " --out '" + out + "'";
  if (mem_budget) cmd += " --mem-budget " + std::to_string(mem_budget);
  cmd += " > '" + out + ".log' 2>&1";
  int rc = std::system(cmd.c_str());
  return WIFEXITED(rc) ? WEXITSTATUS(rc) : -1;
}
}  // namespace

// The merge's own plan (fit.bin meta.mem_estimate) and its measured peak (the process's VmHWM at the end, the record's
// peak_rss_kb), read from the files the subprocess wrote.
struct PlanAndPeak { double total = 0, sacct_upper = 0, peak = 0; Json est, rec; std::string status; };
static PlanAndPeak read_plan_and_peak(const std::string& out) {
  PlanAndPeak r; r.rec = read_json_file(out + ".json");
  fmt::Reader R(out); Json m = R.json("meta");
  r.est = m.at("mem_estimate"); r.total = r.est.at("total").num(); r.sacct_upper = r.est.at("sacct_upper").num();
  r.status = m.at("status").str();
  r.peak = r.rec.contains("peak_rss_kb") ? r.rec.at("peak_rss_kb").num() * 1024.0 : 0.0;
  return r;
}

// Default suite: the plan bounds the measured peak by at least 1.1 and is not absurd; the load phases are admitted before
// anything is read (--mem-budget below the load peak refuses with resource_limit and writes a refusal record).
TEST(wp4_merge_mem_plan_bounds_peak) {
  const std::string dir = tmp_path("mmplan"); ::mkdir(dir.c_str(), 0755);
  struct Cleanup { std::string d; ~Cleanup() { std::string cmd = "rm -rf '" + d + "'"; (void)std::system(cmd.c_str()); } } cl{dir};
  Probe P = make_probe(dir, 4000, 4, 200);
  const std::string out = dir + "/fit.bin";
  CHECK(run_merge(P, out, 2) == 0);
  const PlanAndPeak pk = read_plan_and_peak(out);
  std::printf("  p = %d: measured peak %.1f MB, plan %.1f MB (x%.2f), sacct upper %.1f MB\n", P.p, pk.peak / 1e6, pk.total / 1e6, pk.total / std::max(1.0, pk.peak), pk.sacct_upper / 1e6);
  CHECK(pk.status == "completed" && pk.peak > 0);
  CHECK(pk.total >= 1.1 * pk.peak);                 // the plan bounds the measured peak
  CHECK(pk.total <= 4.0 * pk.peak);                 // and is not absurd
  CHECK(pk.sacct_upper > pk.total);
  // the phases the record carries: in order, with the process memory at each
  const Json& ph = pk.rec.at("timings").at("phases");
  CHECK(ph.size() >= 10 && ph.at(0).at("phase").str() == "start");
  { bool seen_setup = false, seen_streamed = false;
    for (size_t i = 0; i < ph.size(); ++i) { const std::string nm = ph.at(i).at("phase").str(); seen_setup = seen_setup || nm == "setup_read"; seen_streamed = seen_streamed || nm == "island_4_merged"; }
    CHECK(seen_setup && seen_streamed); }
  // early admission: a budget below the load peak is refused before read_setup (no phases beyond data_loaded)
  const uint64_t need = (uint64_t)pk.est.at("load_setup").num();
  const std::string out2 = dir + "/fit_refused.bin";
  CHECK(run_merge(P, out2, 2, std::max<uint64_t>(1, need / 2)) == 11);   // resource_limit
  { fmt::Reader R(out2); Json m = R.json("meta");
    CHECK(m.at("fit_state").str() == "not_admitted" && m.at("reason").str().find("before the inputs are read") != std::string::npos && !R.has("pip_eq")); }
  // a budget at the plan's total is admitted
  CHECK(run_merge(P, dir + "/fit_ok.bin", 2, (uint64_t)pk.total + 1) == 0);
}

TEST(wp4_merge_mem_probe) {
  const char* ps = std::getenv("V4_MEM_PROBE_P");
  if (!ps) { std::printf("  wp4_merge_mem_probe: set V4_MEM_PROBE_P to run (not part of the default checks)\n"); return; }
  const int p = std::atoi(ps), R = std::getenv("V4_MEM_PROBE_R") ? std::atoi(std::getenv("V4_MEM_PROBE_R")) : 16;
  const char* keep = std::getenv("V4_MEM_PROBE_DIR");
  const std::string dir = keep ? std::string(keep) : tmp_path("mmprobe");
  ::mkdir(dir.c_str(), 0755);
  Probe P;
  const std::string marker = dir + "/probe.json";
  if (keep && file_size(marker) > 0) {   // reuse the files of an earlier run with the same p and R'
    Json m = read_json_file(marker);
    P.dir = dir; P.dpath = m.at("dpath").str(); P.spath = m.at("spath").str(); P.cpath = m.at("cpath").str(); P.R = (int)m.at("R").num(); P.p = (int)m.at("p").num();
    P.K = (int)m.at("K").num(); P.c = (uint64_t)m.at("c").num(); P.n = (int)m.at("n").num(); P.n_inherited = (size_t)m.at("n_inherited").num(); P.kbar_island = m.at("kbar_island").num();
    for (size_t i = 0; i < m.at("ipath").size(); ++i) P.ipath.push_back(m.at("ipath").at(i).str());
    P.bytes_data = file_size(P.dpath); P.bytes_setup = file_size(P.spath); P.bytes_calib = file_size(P.cpath); P.bytes_island = file_size(P.ipath[0]);
  } else {
    P = make_probe(dir, p, R, 200);
    if (keep) {
      Json m = Json::object(); m["dpath"] = P.dpath; m["spath"] = P.spath; m["cpath"] = P.cpath; m["R"] = P.R; m["p"] = P.p; m["K"] = P.K; m["c"] = (double)P.c; m["n"] = P.n;
      m["n_inherited"] = (double)P.n_inherited; m["kbar_island"] = P.kbar_island;
      Json ip = Json::array(); for (auto& x : P.ipath) ip.push(x); m["ipath"] = ip;
      write_json_file(marker, m);
    }
  }
  std::printf("  probe p = %d, c = %llu, R' = %d: data %.1f MB, setup %.1f MB, calib %.1f MB (%zu inherited), island %.1f MB (k = %.2f)\n", P.p,
              (unsigned long long)P.c, R, P.bytes_data / 1e6, P.bytes_setup / 1e6, P.bytes_calib / 1e6, P.n_inherited, P.bytes_island / 1e6, P.kbar_island);
  const int threads = std::getenv("V4_MEM_PROBE_THREADS") ? std::atoi(std::getenv("V4_MEM_PROBE_THREADS")) : 3;
  const std::string out = dir + "/fit.bin";
  const int rc = run_merge(P, out, threads);
  CHECK(rc == 0);
  Json rec = read_json_file(out + ".json");
  std::printf("  merge exit %d, peak RSS %.1f MB\n", rc, rec.at("peak_rss_kb").num() / 1024.0);
  const Json& ph = rec.at("timings").at("phases");
  for (size_t i = 0; i < ph.size(); ++i) {
    const Json& x = ph.at(i); const std::string nm = x.at("phase").str();
    if (nm.rfind("island_", 0) == 0 && nm != "island_1_loaded" && nm != "island_1_merged" && nm != "island_2_loaded" && nm != "island_2_merged" &&
        nm.find("island_" + std::to_string(R) + "_") != 0) continue;
    std::printf("    %-22s t %8.2f s  rss %9.1f MB  anon %9.1f MB  file %9.1f MB  hwm %9.1f MB\n", nm.c_str(), x.at("t").num(), x.at("rss_kb").num() / 1024,
                x.at("anon_kb").num() / 1024, x.at("file_kb").num() / 1024, x.at("hwm_kb").num() / 1024);
  }
  const PlanAndPeak pk = read_plan_and_peak(out);
  std::printf("  plan (MB): load_setup %.1f load_calib %.1f offers %.1f streaming %.1f tail %.1f | merged %.1f one_island %.1f small %.1f extra %.1f | total %.1f (x%.2f of the peak) "
              "sacct_upper %.1f\n", pk.est.at("load_setup").num() / 1e6, pk.est.at("load_calib").num() / 1e6, pk.est.at("offers").num() / 1e6, pk.est.at("streaming").num() / 1e6,
              pk.est.at("tail_phase").num() / 1e6, pk.est.at("merged").num() / 1e6, pk.est.at("one_island").num() / 1e6, pk.est.at("small").num() / 1e6, pk.est.at("extra").num() / 1e6,
              pk.total / 1e6, pk.total / std::max(1.0, pk.peak), pk.sacct_upper / 1e6);
  std::printf("  write_fit %.1f s; end RSS %.1f MB (file %.1f MB)\n", pk.rec.at("write_fit_seconds").num(), pk.rec.at("end_rss_kb").num() / 1024.0, pk.rec.at("end_file_kb").num() / 1024.0);
  if (!keep) { std::string cmd = "rm -rf '" + dir + "'"; std::system(cmd.c_str()); }
}
