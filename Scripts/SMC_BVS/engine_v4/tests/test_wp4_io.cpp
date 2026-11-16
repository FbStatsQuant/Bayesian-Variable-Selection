// test_wp4_io.cpp -- WP4 files: calib.bin / island_r.bin / fit.bin round trips, input validation by content hash and
// binary block (T10 through real files), and the merge command end to end (thread invariance of fit.bin).
#include <cstdio>
#include <dirent.h>
#include <fstream>
#include <cmath>
#include <functional>
#include <limits>
#include <random>
#include "tk.h"
#include "tutil.h"
#include "v4/merge.h"
#include "v4/provenance.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"

using namespace v4;

namespace {
struct Fx {   // a small dataset with pair blocks, its setup view, calibration and islands, all as files
  Data D; prep::Result pr; wp4io::SetupView S;
  std::string dpath, spath, cpath, dhash, shash, chash;
  std::vector<std::string> ipath;
  std::vector<merge::IslandIn> isl;
  std::vector<merge::InheritedModel> inh; Model calib_hpm; EventCtx calib_ev;
  std::vector<double> grid{0, 0.3, 0.7, 1};   // the frozen grid; T = 3 stages
  // calib.bin's writer inputs (kept so tests can write variants: review PR37 N-4)
  uint32_t mode = fmt::M_COMPAT; int Nfx = 50; Ledger cl; calib::CalibOut co; calib::Settings cset;
};
// The fixture's CalibWrite (pointers into f: valid while f lives).
wp4io::CalibWrite calib_write(const Fx& f) {
  wp4io::CalibWrite cw; cw.mode = f.mode; cw.co = &f.co; cw.led = &f.cl; cw.inherited = f.inh; cw.N = f.Nfx; cw.L = 4; cw.Hm = 4;
  cw.settings = &f.cset; cw.k_store = 2.0;
  cw.inputs["data.bin"] = f.dhash; cw.inputs["setup.bin"] = f.shash;
  return cw;
}
struct Ev {   // compat evaluator: Bit scorer + comp (as merge::run's)
  const Data* D; const wp4io::SetupView* S; BitScorer sc; std::vector<std::pair<int32_t, int32_t>> scr;
  Ev(const Data* d, const wp4io::SetupView* s) : D(d), S(s), sc(d) {}
  void operator()(const Model& M, double& lm, double& lg0, double& dd, double& F) {
    lm = sc.score(M).logm; double c = S->comp(M, scr); size_t k = M.size();
    lg0 = D->logprior[k] + c; dd = (lm - D->logm0) - c; F = D->logprior[k] + lm;
  }
};
// A binary block with a clean, known git commit: theory/compat merges refuse "-dirty" builds (INTERFACES §5.1), and
// test builds are usually dirty. Islands of the fixtures carry this block.
const Json& clean_block() {
  static Json b = [] { Json x = binary_block(); x["git_commit"] = "0123456789abcdef0123456789abcdef01234567"; return x; }();
  return b;
}
Model random_model(std::mt19937_64& g, int p, int kmax) {
  Model S; int k = 1 + (int)(g() % (uint64_t)kmax); for (int a = 0; a < k; ++a) S.push_back((int32_t)(g() % (uint64_t)p));
  std::sort(S.begin(), S.end()); S.erase(std::unique(S.begin(), S.end()), S.end()); return S;
}

Fx make_fx(const std::string& tag, int R, uint32_t mode = fmt::M_COMPAT) {
  Fx f;
  const int n = 60, p_raw = 24;
  gen::Spec sp; sp.design = gen::Design::AR; sp.n = n; sp.p = p_raw; sp.seed = 5; sp.s0 = 3; sp.a = 1.5;
  std::vector<double> X, y; gen::generate(sp, X, y);
  f.pr = prep::preprocess(X.data(), y.data(), n, p_raw);
  f.D = make_data(f.pr.own, n, f.pr.p);
  const int p = f.D.p;
  f.dpath = tmp_path(tag + "_data.bin");
  f.dhash = prep::write_data(f.dpath, f.D, f.pr, "B", Json::object());
  // setup: blocks {2b, 2b+1}; logr = log m(U) - log m0 (direct scores); table stores over every table model
  wp4io::SetupView& S = f.S;
  BitScorer sc(&f.D);
  S.blk.resize(p); S.pos.resize(p);
  S.blk_ptr.push_back(0);
  for (int j = 0; j < p; ++j) { S.blk[j] = j / 2; S.pos[j] = j % 2; S.blk_members.push_back(j); if (j % 2 == 1 || j == p - 1) S.blk_ptr.push_back(j + 1); }
  S.ttop.init(40ull * p + 1, Order::HPM); S.tlead0.init(20ull * p, Order::LEX); S.tlead1.init(20ull * p, Order::LEX);
  for (size_t b = 0; b + 1 < S.blk_ptr.size(); ++b) {
    int m = (int)(S.blk_ptr[b + 1] - S.blk_ptr[b]);
    S.code_ptr.push_back((int64_t)S.logr.size());
    for (uint32_t c = 0; c < (1u << m); ++c) {
      Model U; for (int i = 0; i < m; ++i) if (c & (1u << i)) U.push_back((int32_t)(S.blk_ptr[b] + i));
      double lm = sc.score(U).logm, lr = lm - f.D.logm0;
      S.logr.push_back(lr);
      double F = f.D.logprior[U.size()] + lm, lg0 = f.D.logprior[U.size()] + lr;
      S.ttop.offer(F, U, f.D.zob.hash(U)); S.tlead0.offer(lg0, U, f.D.zob.hash(U)); S.tlead1.offer(F, U, f.D.zob.hash(U));
    }
  }
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  S.mode_S = Model(S.ttop.model(0).begin(), S.ttop.model(0).end());
  // pi_0 size law (setup.bin size_logmass; calibrate's plan k, review PR37 N-2): P(0) .5, P(1) .3, P(12) .15, P(13) .05
  // -> q90 = 12, plan k = 13
  S.size_logmass.assign((size_t)f.D.K + 1, -std::numeric_limits<double>::infinity());
  S.size_logmass[0] = std::log(0.5); S.size_logmass[1] = std::log(0.3); S.size_logmass[12] = std::log(0.15); S.size_logmass[13] = std::log(0.05);
  f.spath = tmp_path(tag + "_setup.bin");
  Json sin = Json::object(); sin["data.bin"] = f.dhash;
  f.shash = wp4io::write_setup_min(f.spath, S, sin);
  // calibration: a ledger with some scored models; inherited = its top store models
  std::mt19937_64 g(11);
  Ev ev(&f.D, &S);
  LedgerConfig cfg; cfg.p = p; cfg.islands = 4; cfg.leaders = mode == fmt::M_COMPAT; cfg.fresh_counters = false;
  f.cl.init(cfg); Ledger& cl = f.cl;
  for (int t = 0; t < 300; ++t) {
    Model M = random_model(g, p, 4); double lm, lg0, dd, F; ev(M, lm, lg0, dd, F);
    EventCtx e; e.phase = PH_PILOT; e.mech = ME_GIBBS_FLIP; e.phi = 0.25; e.key.seg = SG_CALIB; e.key.iter = 0; e.key.unit = 0;
    e.key.xph = X_BRIDGE; e.key.stage = 1 + t / 100; e.key.round = e.key.stage; e.key.particle = 1 + t % 100; e.key.position = 3;
    cl.event(M, f.D.zob.hash(M), F, lg0, lm, e, true);
  }
  cl.compact();
  for (size_t i = 0; i < cl.top.size(); ++i) {
    Model M(cl.top.model(i).begin(), cl.top.model(i).end()); merge::InheritedModel im; im.S = M; double dd; ev(M, im.logm, im.lg0, dd, im.F); f.inh.push_back(im);
  }
  std::sort(f.inh.begin(), f.inh.end(), [](const merge::InheritedModel& a, const merge::InheritedModel& b) { return lex_less(a.S, b.S); });
  f.calib_hpm = cl.hpmS; f.calib_ev = cl.hpm_ev;
  f.mode = mode; calib::CalibOut& co = f.co; co.status = calib::CalStatus::ok; co.tier_final = 0; co.has_frozen = true;
  co.rule = mode == fmt::M_V ? calib::Rule::bounded : calib::Rule::coded;   // V: bounded rule, N = 2,500 (D-1, D-26)
  const int Nfx = f.Nfx = mode == fmt::M_V ? calib::V_N : 50;
  calib::Settings& cset = f.cset; cset.rule = co.rule; cset.I_max = 1; cset.tiers[0].ell = 3; cset.tiers[0].H = 64; cset.tiers[0].Te = 40;
  co.frozen.grid = f.grid; co.frozen.grid_unrefined = co.frozen.grid; co.frozen.grid_label = "rebuild_1"; co.I_used = 1;
  calib::TierOut t0; t0.tier = 0; t0.has_triggers = true; calib::GridRecord gr; gr.label = "preliminary"; gr.grid = f.grid; t0.grids.push_back(gr);
  co.tiers.push_back(t0);
  const wp4io::CalibWrite cw = calib_write(f);
  f.cpath = tmp_path(tag + "_calib.bin");
  f.chash = wp4io::write_calib(f.cpath, cw);
  // islands
  for (int r = 1; r <= R; ++r) {
    merge::IslandIn I; I.r = r; I.N = Nfx; I.T = 3; I.L = 4; I.Hm = 4; I.logZ = -30 + 0.07 * r; I.ess = {40, 45, 48};
    I.pip.resize(p); I.rb_acc.resize(p);
    for (int j = 0; j < p; ++j) { I.pip[j] = std::fmod(0.017 * (j + 1) * (r + 3), 1.0); I.rb_acc[j] = I.pip[j] * 200; }
    I.rb_round.assign(4, std::vector<double>(p, 1.0));
    LedgerConfig ic = cfg; ic.leaders = false; ic.islands = std::max(4, R); I.led.init(ic);
    for (int t = 0; t < 400; ++t) {
      Model M = random_model(g, p, 5); double lm, lg0, dd, F; ev(M, lm, lg0, dd, F);
      EventCtx e; e.phase = PH_MEASURED; e.mech = ME_GIBBS_FLIP; e.phi = 1; e.key.seg = SG_FINAL; e.key.unit = (uint32_t)r; e.key.xph = X_MEASURED;
      e.key.stage = 3; e.key.round = 1 + t / 100; e.key.particle = 1 + t % 100; e.key.position = 1 + (uint32_t)(g() % 30); e.key.sub = 1;
      I.led.event(M, f.D.zob.hash(M), F, lg0, lm, e, true);
      if (t >= 350) I.terminal.push_back(M);
      if (t == 399) while ((int)I.terminal.size() < Nfx) I.terminal.push_back(I.terminal[I.terminal.size() % 50]);   // N supports
    }
    I.led.compact();
    f.isl.push_back(I);
    std::string ip = tmp_path(tag + "_island_" + std::to_string(r) + ".bin");
    Json in = Json::object(); in["data.bin"] = f.dhash; in["setup.bin"] = f.shash; in["calib.bin"] = f.chash;
    wp4io::write_island(ip, mode, I, in, &clean_block(), &f.grid);
    f.ipath.push_back(ip);
  }
  return f;
}
Json merge_args(const Fx& f, const std::string& out, int threads) {
  Json a = Json::object();
  a["data"] = f.dpath; a["setup"] = f.spath; a["calib"] = f.cpath; a["out"] = out; a["mode"] = "compat";
  a["threads"] = threads; a["chunk"] = 7; a["ell"] = 3; a["Rp"] = (int)f.ipath.size();
  Json il = Json::array(); for (auto& p : f.ipath) il.push(p); a["islands"] = il;
  return a;
}
std::map<std::string, std::string> section_hashes(const std::string& path) {
  fmt::Reader R(path); std::map<std::string, std::string> m;
  for (auto& e : R.sections()) { std::string h; char b[3]; for (int i = 0; i < 32; ++i) { std::snprintf(b, 3, "%02x", e.sha256[i]); h += b; } m[e.name] = h; }
  return m;
}
void flip_byte(const std::string& path, const std::string& section) {   // one byte inside a named section
  uint64_t at;
  { fmt::Reader R(path, false); at = R.entry(section).offset + R.entry(section).length / 2; }
  std::fstream fs(path, std::ios::in | std::ios::out | std::ios::binary);
  fs.seekg((long)at); char c; fs.read(&c, 1); c ^= 0x5A; fs.seekp((long)at); fs.write(&c, 1);
}
// Removes every file this process created for a test tag (tmp_path prefix), at scope exit -- also when a test throws.
struct TmpGuard {
  std::string prefix;
  explicit TmpGuard(const std::string& tag) : prefix(tmp_path(tag + "_")) {}
  ~TmpGuard() {
    std::string dir = prefix.substr(0, prefix.find_last_of('/')), base = prefix.substr(prefix.find_last_of('/') + 1);
    if (DIR* d = opendir(dir.c_str())) {
      while (dirent* e = readdir(d)) {
        std::string n = e->d_name;
        if (n.rfind(base, 0) == 0) std::remove((dir + "/" + n).c_str());
      }
      closedir(d);
    }
  }
};
void cleanup(const Fx& f) {
  std::remove(f.dpath.c_str()); std::remove(f.spath.c_str()); std::remove(f.cpath.c_str());
  for (auto& p : f.ipath) std::remove(p.c_str());
}
}  // namespace

TEST(wp4_io_calib_island_roundtrip) {
  TmpGuard tmp_guard("rt"); Fx f = make_fx("rt", 2);
  wp4io::CalibIn c = wp4io::read_calib(f.cpath, f.D.p, f.D.K);
  CHECK(c.status == "ok" && c.grid == f.grid && c.N == 50 && c.L == 4 && c.tier == 0 && c.content_hash == f.chash);
  CHECK(c.has_hpm && c.hpm == f.calib_hpm && c.hpm_ev.key.seg == SG_CALIB && c.hpm_ev.key.stage == f.calib_ev.key.stage &&
        c.hpm_ev.key.particle == f.calib_ev.key.particle && c.hpm_ev.phase == PH_PILOT);
  CHECK(c.inherited.size() == f.inh.size());
  bool same = true;
  for (size_t i = 0; i < f.inh.size(); ++i) same = same && c.inherited[i].S == f.inh[i].S && same_bits(c.inherited[i].F, f.inh[i].F) &&
                                                  same_bits(c.inherited[i].lg0, f.inh[i].lg0) && same_bits(c.inherited[i].logm, f.inh[i].logm);
  CHECK(same);
  wp4io::Expect ex; ex.mode = fmt::M_COMPAT; ex.data_hash = f.dhash; ex.setup_hash = f.shash; ex.calib_hash = f.chash;
  Json blk;
  merge::IslandSlot s = wp4io::load_island(f.ipath[0], 1, ex, f.D.p, &blk);
  CHECK(s.load == merge::Load::ok);
  const merge::IslandIn& a = s.isl; const merge::IslandIn& b = f.isl[0];
  CHECK(a.r == 1 && a.N == 50 && same_bits(a.logZ, b.logZ) && a.pip == b.pip && a.ess == b.ess && a.terminal == b.terminal);
  CHECK(a.led.top.size() == b.led.top.size() && a.led.top.content_hash() == b.led.top.content_hash());
  CHECK(a.led.hpmS == b.led.hpmS && a.led.hpm_ev.key == b.led.hpm_ev.key && same_bits(a.led.island_best[1], b.led.island_best[1]) &&
        a.rb_round.empty() && a.led.lead0.cap == 0);   // rb_* are not loaded by the merge (review PR20 m-2)
  bool lg = true; for (int x = 0; x < N_PHASE; ++x) for (int y = 0; y < N_MECH; ++y) lg = lg && a.led.logical[x][y] == b.led.logical[x][y];
  CHECK(lg && blk.contains("git_commit"));
  wp4io::SetupView S2 = wp4io::read_setup(f.spath, f.D.p, f.D.K);
  CHECK(S2.ttop.content_hash() == f.S.ttop.content_hash() && S2.logr == f.S.logr && S2.mode_S == f.S.mode_S);
  CHECK(S2.table_event_count(f.D.K) == (uint64_t)(4 * (f.D.p / 2) + (f.D.p % 2 ? 2 : 0)));
  cleanup(f);
}

TEST(wp4_io_load_island_t10) {
  TmpGuard tmp_guard("t10"); Fx f = make_fx("t10", 4);
  wp4io::Expect ex; ex.mode = fmt::M_COMPAT; ex.data_hash = f.dhash; ex.setup_hash = f.shash; ex.calib_hash = f.chash;
  auto load = [&](int r, const wp4io::Expect& e) { Json b; return wp4io::load_island(f.ipath[r - 1], r, e, f.D.p, &b).load; };
  CHECK(load(1, ex) == merge::Load::ok);
  CHECK(wp4io::load_island(tmp_path("t10_nonexistent.bin"), 1, ex, f.D.p, nullptr).load == merge::Load::missing);
  { wp4io::Expect e2 = ex; e2.island_hash = {"", "deadbeef"}; CHECK(load(2, e2) == merge::Load::hash_mismatch); }   // manifest hash
  { wp4io::Expect e2 = ex; e2.calib_hash = "0000"; CHECK(load(2, e2) == merge::Load::hash_mismatch); }             // meta.inputs
  { wp4io::Expect e2 = ex; e2.mode = fmt::M_V; CHECK(load(2, e2) == merge::Load::corrupt); }                        // wrong mode
  flip_byte(f.ipath[2], "pip_r");   // its SHA-256 no longer matches
  { Json b; auto sl = wp4io::load_island(f.ipath[2], 3, ex, f.D.p, &b); CHECK_MSG(sl.load == merge::Load::corrupt, sl.detail); }
  // a different binary block (flags) on island 4 -> binary_mismatch
  Json other = clean_block(); other["flags"] = "-O3 -ffast-math";
  Json in = Json::object(); in["data.bin"] = f.dhash; in["setup.bin"] = f.shash; in["calib.bin"] = f.chash;
  wp4io::write_island(f.ipath[3], fmt::M_COMPAT, f.isl[3], in, &other, &f.grid);
  std::vector<merge::IslandSlot> slots; std::vector<Json> blocks(4);
  for (int r = 1; r <= 4; ++r) slots.push_back(wp4io::load_island(f.ipath[r - 1], r, ex, f.D.p, &blocks[r - 1]));
  wp4io::check_binaries(slots, blocks, fmt::M_COMPAT);
  { // V mode accepts a dirty build (flags and libm must still agree)
    std::vector<merge::IslandSlot> s2(2); s2[0].load = s2[1].load = merge::Load::ok;
    Json d1 = clean_block(); d1["git_commit"] = std::string(40, 'b') + "-dirty"; Json d2 = d1; d2["git_commit"] = std::string(40, 'c');
    wp4io::check_binaries(s2, {d1, d2}, fmt::M_V); CHECK(s2[1].load == merge::Load::ok);
    wp4io::check_binaries(s2, {d1, d2}, fmt::M_COMPAT); CHECK(s2[1].load == merge::Load::binary_mismatch);
  }
  CHECK_MSG(slots[0].load == merge::Load::ok && slots[1].load == merge::Load::ok && slots[3].load == merge::Load::binary_mismatch,
            slots[0].detail + " | " + slots[1].detail + " | " + slots[3].detail + " | " + std::to_string((int)slots[3].load));
  cleanup(f);
}

TEST(wp4_io_merge_command_e2e) {
  TmpGuard tmp_guard("e2e"); Fx f = make_fx("e2e", 4);
  std::string o1 = tmp_path("e2e_fit1.bin"), o3 = tmp_path("e2e_fit3.bin");
  Json r1 = merge::run(merge_args(f, o1, 1));
  Json r3 = merge::run(merge_args(f, o3, 3));
  CHECK_MSG(r1.at("status").str() == "completed" && r1.at("estimates_available").boolean(), r1.dump());
  auto h1 = section_hashes(o1), h3 = section_hashes(o3);
  bool inv = h1.size() == h3.size();
  for (auto& kv : h1) if (kv.first != "meta") inv = inv && h3.count(kv.first) && h3[kv.first] == kv.second;
  CHECK(inv);   // thread invariance: every section but meta (timings) identical
  {
    fmt::Reader R(o1); Json meta = R.json("meta");
    for (const char* s : {"hpm_S", "logZ_r", "pip_eq", "pip_Z", "pip_T", "pip_r", "occ_top", "occ_top_r", "top_v", "top_off", "top_len",
                          "top_hash", "top_pool", "mpm", "mode_S", "near_ptr", "ls_scanned_ptr", "ls0_scanned_ptr"})
      CHECK_MSG(R.has(s), std::string("fit.bin section ") + s);
    CHECK(R.entry("pip_r").dims[0] == 4 && R.entry("pip_r").dims[1] == (uint64_t)f.D.p);
    CHECK(R.entry("occ_top_r").dims[0] == 4 && meta.at("occ_total").num() == 200 && meta.at("occ_total_r").num() == 50);
    CHECK(meta.contains("logZ") && meta.contains("hpm_F") && meta.at("status").str() == "completed" && meta.contains("hpm_ev"));
    CHECK(meta.at("flags").contains("occ_inhomogeneous") && meta.at("occ").size() == 4);
    // the pre-island ledger: table step (top stores + logical count) and the inherited step
    std::vector<uint64_t> lg = R.vec<uint64_t>("logical");
    CHECK(lg[(size_t)PH_TABLE * N_MECH + ME_TABLE] == f.S.table_event_count(f.D.K));
    // pip_eq = long-double mean over islands (rowMeans)
    std::vector<double> pe = R.vec<double>("pip_eq");
    long double a = 0; for (int r = 0; r < 4; ++r) a += f.isl[r].pip[5]; CHECK(same_bits(pe[5], (double)(a / 4.0L)));
  }
  // T10 through the command: missing island, corrupt island, binary mismatch -> declared status, no estimate sections
  auto refused = [&](const std::string& out, Status want) {
    Json r = merge::run(merge_args(f, out, 3));
    fmt::Reader R(out); Json meta = R.json("meta");
    bool none = !R.has("pip_eq") && !R.has("logZ_r") && !R.has("pip_r") && !meta.contains("logZ") && !meta.at("estimates_available").boolean();
    CHECK_MSG(r.at("status").str() == status_name(want) && none, out + ": " + r.at("status").str() + " / " + r.at("reason").str());
    std::remove(out.c_str());
  };
  std::rename(f.ipath[1].c_str(), (f.ipath[1] + ".away").c_str());
  refused(tmp_path("e2e_fit_missing.bin"), Status::io_error);
  std::rename((f.ipath[1] + ".away").c_str(), f.ipath[1].c_str());
  flip_byte(f.ipath[2], "pip_r");
  refused(tmp_path("e2e_fit_corrupt.bin"), Status::invalid_input);
  Json in = Json::object(); in["data.bin"] = f.dhash; in["setup.bin"] = f.shash; in["calib.bin"] = f.chash;
  wp4io::write_island(f.ipath[2], fmt::M_COMPAT, f.isl[2], in, &clean_block(), &f.grid);   // repaired
  { merge::IslandIn bad = f.isl[0]; bad.status = Status::numerical_failure;
    wp4io::write_island(f.ipath[0], fmt::M_COMPAT, bad, in, &clean_block(), &f.grid); refused(tmp_path("e2e_fit_numfail.bin"), Status::numerical_failure);
    wp4io::write_island(f.ipath[0], fmt::M_COMPAT, f.isl[0], in, &clean_block(), &f.grid); }
  { Json dirty = clean_block(); dirty["git_commit"] = std::string(40, 'a') + "-dirty";   // theory mode refuses a dirty build
    wp4io::write_island(f.ipath[1], fmt::M_COMPAT, f.isl[1], in, &dirty, &f.grid); refused(tmp_path("e2e_fit_dirty.bin"), Status::invalid_input);
    wp4io::write_island(f.ipath[1], fmt::M_COMPAT, f.isl[1], in, &clean_block(), &f.grid); }
  { // --mem-budget admission through the command: refused before any island store is loaded
    Json a2 = merge_args(f, tmp_path("e2e_fit_mem.bin"), 1); a2["mem_budget_gb"] = 1e-6;
    Json r = merge::run(a2);
    fmt::Reader R(tmp_path("e2e_fit_mem.bin")); Json meta = R.json("meta");
    CHECK(r.at("status").str() == "resource_limit" && meta.at("fit_state").str() == "not_admitted" && !R.has("pip_eq") && meta.contains("mem_estimate"));
    std::remove(tmp_path("e2e_fit_mem.bin").c_str());
  }
  { // v0.1.8: a non-completed island file carries no estimate section
    merge::IslandIn bad = f.isl[0]; bad.status = Status::numerical_failure;
    std::string bp = tmp_path("e2e_bad_island.bin"); wp4io::write_island(bp, fmt::M_COMPAT, bad, in, &clean_block(), &f.grid);
    fmt::Reader R(bp);
    CHECK(!R.has("logZ") && !R.has("pip_r") && !R.has("rb_acc") && !R.has("rb_round") && !R.has("terminal_S") && !R.has("st_inc") && R.has("st_ess") && R.has("hpm_ev"));
    std::remove(bp.c_str());
  }
  // the merge's own inputs: a manifest hash mismatch for calib.bin refuses the whole job (invalid_input thrown)
  Json man = Json::object(); man["inputs"][f.cpath] = "00ff"; std::string mp = tmp_path("e2e_manifest.json"); write_json_file(mp, man);
  Json a = merge_args(f, tmp_path("e2e_fit_bad.bin"), 1); a["manifest"] = mp;
  CHECK_THROWS(merge::run(a));
  std::remove(mp.c_str()); std::remove(o1.c_str()); std::remove(o3.c_str());
  cleanup(f);
}

TEST(wp4_io_chi2_and_inherited_provenance) {
  // chi-square upper tail: known values (R: pchisq(x, df, lower.tail = FALSE))
  CHECK(std::fabs(wp4io::chi2_upper(3.841458820694124, 1) - 0.05) < 1e-12);
  CHECK(std::fabs(wp4io::chi2_upper(30.57791416689249, 15) - 0.01) < 1e-12);
  CHECK(std::fabs(wp4io::chi2_upper(0.5, 3) - 0.9188914117) < 1e-9);
  // inherited step (v0.1.6): (i) table model -> table key; (ii) inherited only -> calibration key; (iii) neither -> no offer
  LedgerConfig cfg; cfg.p = 10; cfg.islands = 4; cfg.leaders = false; cfg.fresh_counters = false;
  Zobrist z; z.init(10);
  EventCtx cal; cal.phase = PH_DIAG; cal.mech = ME_USWAP; cal.key.seg = SG_CALIB; cal.key.iter = 2; cal.key.unit = 3; cal.key.stage = 4;
  Model T{2, 3}, A{1, 5};
  auto run = [&](bool table_has, const std::vector<merge::InheritedModel>& inh, const Model& chpm) {
    Ledger L(cfg);
    if (table_has) L.event(T, z.hash(T), 5.0, 1.0, 4.0, merge::table_event(1, 3), true);
    merge::offer_inherited(L, inh, true, chpm, cal, z);
    return L;
  };
  merge::InheritedModel iT{T, 5.0, 1.0, 4.0}, iA{A, 4.0, 1.0, 3.0};
  Ledger L1 = run(true, {iA, iT}, T);    // (i)
  CHECK(L1.hpmS == T && L1.hpm_ev.phase == PH_TABLE && L1.hpm_ev.key.seg == SG_TABLE && L1.hpm_ev.key.position == 3);
  Ledger L2 = run(false, {iA, iT}, T);   // (ii)
  CHECK(L2.hpmS == T && L2.hpm_ev.key == cal.key && L2.hpm_ev.phase == PH_DIAG);
  Ledger L3 = run(false, {iA}, T);       // (iii): the calibration HPM is never offered; the HPM is A with an INHERITED key
  CHECK(L3.hpmS == A && L3.hpm_ev.phase == PH_INHERITED && L3.hpm_ev.key.particle == 0);
  Ledger L4 = run(false, {iT, iA}, A);   // another inherited model keeps its INHERITED key (input index 0)
  CHECK(L4.hpmS == T && L4.hpm_ev.phase == PH_INHERITED && L4.hpm_ev.key.particle == 0);
}

// review PR37 N-4: every calib.bin refusal added in PR #37 (read_calib's V rule / tier / N, I_used <= I_max <= ell,
// k_store, meta.inputs; write_calib's reserved extra keys), each against a variant of the fixture's own calib.bin.
#define EXPECT_STR(a, b) do { const std::string a_ = (a), b_ = (b); CHECK_MSG(a_ == b_, "got " + a_ + ", want " + b_); } while (0)
TEST(wp4_io_calib_refusals) {
  TmpGuard tmp_guard("cref");
  Fx fv = make_fx("cref", 1, fmt::M_V), ft = make_fx("cref_t", 1, fmt::M_COMPAT);   // "cref_" prefix: removed by tmp_guard
  // outcome of writing + reading one variant: "ok", "w:<status>" (writer refused) or "r:<status>" (reader refused)
  auto outcome = [&](const Fx& f, const std::function<void(wp4io::CalibWrite&, calib::CalibOut&, calib::Settings&)>& mod,
                     const std::string& dh = "", const std::string& sh = "") -> std::string {
    calib::CalibOut co = f.co; calib::Settings cs = f.cset;
    wp4io::CalibWrite cw = calib_write(f); cw.co = &co; cw.settings = &cs;
    mod(cw, co, cs);
    const std::string path = tmp_path("cref_variant.bin");
    try { wp4io::write_calib(path, cw); } catch (const Error& e) { return std::string("w:") + status_name(e.st); }
    try { wp4io::read_calib(path, f.D.p, f.D.K, dh, sh); } catch (const Error& e) { return std::string("r:") + status_name(e.st); }
    return "ok";
  };
  using CW = wp4io::CalibWrite; using CO = calib::CalibOut; using CS = calib::Settings;
  const std::string bad = "r:invalid_input";
  // baselines: the fixture's V and compat calib.bin read back, also with the right data / setup hashes
  EXPECT_STR(outcome(fv, [](CW&, CO&, CS&) {}), "ok");
  EXPECT_STR(outcome(fv, [](CW&, CO&, CS&) {}, fv.dhash, fv.shash), "ok");
  EXPECT_STR(outcome(ft, [](CW&, CO&, CS&) {}, ft.dhash, ft.shash), "ok");
  // V: N = 2,500, tier 0 and the bounded rule only (D-1, D-26)
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.N = 50; }), bad);
  EXPECT_STR(outcome(fv, [](CW&, CO& c, CS& s) { c.tier_final = 1; s.tiers[1].ell = 3; }), bad);
  EXPECT_STR(outcome(fv, [](CW&, CO& c, CS& s) { c.rule = calib::Rule::coded; s.rule = calib::Rule::coded; }), bad);
  // theory mode: the coded rule only
  EXPECT_STR(outcome(ft, [](CW&, CO& c, CS& s) { c.rule = calib::Rule::bounded; s.rule = calib::Rule::bounded; }), bad);
  // V: I_used <= I_max <= ell (fixture: I_used 1, I_max 1, ell 3)
  EXPECT_STR(outcome(fv, [](CW&, CO&, CS& s) { s.I_max = 3; }), "ok");                  // I_max = ell: allowed
  EXPECT_STR(outcome(fv, [](CW&, CO&, CS& s) { s.I_max = 4; }), bad);                   // I_max > ell
  EXPECT_STR(outcome(fv, [](CW&, CO& c, CS&) { c.I_used = 2; }), bad);                  // I_used > I_max
  // k_store: finite and > 0 when the calibration completed; not needed otherwise
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.k_store = 0; }), bad);
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.k_store = -1; }), bad);
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.k_store = std::nan(""); }), bad);
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.k_store = std::numeric_limits<double>::infinity(); }), bad);
  EXPECT_STR(outcome(ft, [](CW& w, CO&, CS&) { w.k_store = 0; }), bad);
  EXPECT_STR(outcome(fv, [](CW& w, CO& c, CS&) { w.k_store = 0; c.status = calib::CalStatus::resource_limit; }), "ok");
  {  // a non-ok calib.bin exposes no inherited models and no HPM
    calib::CalibOut co = fv.co; co.status = calib::CalStatus::resource_limit; CW cw = calib_write(fv); cw.co = &co;
    const std::string path = tmp_path("cref_nonok.bin"); wp4io::write_calib(path, cw);
    wp4io::CalibIn c = wp4io::read_calib(path, fv.D.p, fv.D.K, fv.dhash, fv.shash);
    CHECK(c.status == "resource_limit" && c.inherited.empty() && !c.has_hpm && c.k_store == 0);
  }
  // meta.inputs must name the data / setup in use (review PR37 m-3)
  const std::string other(64, 'a');
  EXPECT_STR(outcome(fv, [](CW&, CO&, CS&) {}, other, fv.shash), bad);
  EXPECT_STR(outcome(fv, [](CW&, CO&, CS&) {}, fv.dhash, other), bad);
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.inputs = Json::object(); }, fv.dhash, ""), bad);   // no inputs recorded
  // write_calib: reserved meta keys are refused (internal_error), other extra keys are written
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.extra["N"] = 50; }), "w:internal_error");
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.extra["k_store"] = 9; }), "w:internal_error");
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.extra["inputs"] = Json::object(); }), "w:internal_error");
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.extra["mode"] = "compat"; }), "w:internal_error");
  EXPECT_STR(outcome(fv, [](CW& w, CO&, CS&) { w.extra["seed"] = 7; }), "ok");
}

// review PR37 N-1 / N-2: the calibration plan's k comes from setup.bin's pi_0 size law (q90 + 1, floor 8, as WP3's
// plan_island); resident excludes the inputs; the command refuses up front iff resident + inputs + one island ledger >
// --mem-budget. setup.bin's size_logmass is validated.
TEST(wp4_io_calib_plan_from_setup) {
  TmpGuard tmp_guard("cplan");
  Fx f = make_fx("cplan", 1, fmt::M_V);
  wp4io::SetupView S = wp4io::read_setup(f.spath, f.D.p, f.D.K, &f.D.zob);
  CHECK(S.size_logmass == f.S.size_logmass);
  CHECK_EQ(calib::calib_k_plan(S.size_logmass), 13.0);                           // q90 = 12
  { std::vector<double> lm(31, -INFINITY); lm[2] = std::log(0.95); lm[3] = std::log(0.05); CHECK_EQ(calib::calib_k_plan(lm), 8.0); }   // floor
  { std::vector<double> lm(31, -INFINITY); lm[0] = std::log(0.9); lm[20] = std::log(0.1); CHECK_EQ(calib::calib_k_plan(lm), 8.0); }    // q90 = 0
  { std::vector<double> lm(31, -INFINITY); lm[0] = std::log(0.89); lm[20] = std::log(0.11); CHECK_EQ(calib::calib_k_plan(lm), 21.0); }
  // the plan: resident = ledger + export (no inputs); total = resident + inputs + one island ledger
  const calib::CalibMemPlan m = calib::calib_memory_plan(1000000, 8, 123456);
  CHECK(m.resident == m.ledger + m.export_ && m.total == m.resident + m.inputs + m.island_ledger && m.inputs == 123456);
  // the command (plan only) on the fixture's data / setup
  Json a = Json::object(); a["data"] = f.dpath; a["setup"] = f.spath; a["mode"] = "V"; a["plan_only"] = 1;
  Json r = calib::run(a);
  const Json& mp = r.at("mem_plan");
  CHECK(r.at("status").str() == "completed" && mp.at("kbar").num() == 13.0);
  const double total = mp.at("total").num(), resident = mp.at("resident").num();
  CHECK(resident == mp.at("ledger").num() + mp.at("export").num() && total == resident + mp.at("inputs").num() + mp.at("island_ledger").num());
  auto with_budget = [&](double bytes) { Json b = a; b["mem_budget"] = bytes; return calib::run(b).at("status").str(); };
  CHECK(with_budget(total) == "completed");                                       // total <= budget: admitted
  CHECK(with_budget(total - 1) == "resource_limit");                              // N-2: refused up front
  CHECK(with_budget(resident + 1) == "resource_limit");                           // resident fits, no island would
  // setup.bin without a size law, or with a malformed one
  auto setup_variant = [&](const std::vector<double>& lm) {
    wp4io::SetupView v = f.S; v.size_logmass = lm;
    Json sin = Json::object(); sin["data.bin"] = f.dhash;
    const std::string sp = tmp_path("cplan_setup_v.bin"); wp4io::write_setup_min(sp, v, sin);
    Status st = Status::completed;
    try { wp4io::read_setup(sp, f.D.p, f.D.K, &f.D.zob); Json b = a; b["setup"] = sp; calib::run(b); } catch (const Error& e) { st = e.st; }
    return st;
  };
  CHECK(setup_variant({}) == Status::invalid_input);                                // read_setup accepts, calibrate refuses
  std::vector<double> lm = f.S.size_logmass; lm.pop_back();
  CHECK(setup_variant(lm) == Status::invalid_input);                                // length != K + 1
  lm = f.S.size_logmass; lm[13] = std::log(0.01);
  CHECK(setup_variant(lm) == Status::invalid_input);                                // sums to 0.96
  lm = f.S.size_logmass; lm[5] = std::nan("");
  CHECK(setup_variant(lm) == Status::invalid_input);
  lm = f.S.size_logmass; lm[5] = INFINITY;
  CHECK(setup_variant(lm) == Status::invalid_input);
}

#include "v4/island/island_file.h"
TEST(wp4_io_island_layout_vs_wp3) {
  // INTERFACES v0.1.8: island_r.bin as WP3 writes it. (a) WP3's write_island_file -> WP4's head_island + load_island_full;
  // (b) WP4's reference write_island -> WP3's read_island_file. Every field the merge reads must agree.
  TmpGuard tmp_guard("x3"); Fx f = make_fx("x3", 2, fmt::M_LAW);
  const merge::IslandIn& I = f.isl[1];
  island::IslandRun run;
  run.status = 0; run.r = I.r; run.N = I.N; run.T = (int)I.ess.size(); run.L = I.L; run.Hm = I.Hm; run.p = f.D.p; run.logZ = I.logZ;
  run.grid = {0, 0.3, 0.7, 1};
  for (double e : I.ess) { StageRow sr; sr.ess = e; run.stages.push_back(sr); }
  run.terminal_moves.resize((size_t)(I.L + I.Hm)); run.terminal_distinct.assign((size_t)(I.L + I.Hm), 0);
  run.rb_acc = I.rb_acc; run.pip = I.pip; run.rb_round = I.rb_round;
  for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) run.logical[a][b] = I.led.logical[a][b];
  run.island_best = I.led.island_best[(size_t)I.r];
  run.hpm.has = true; run.hpm.S = I.led.hpmS; run.hpm.F = I.led.hpmF; run.hpm.logm = I.led.hpm_logm; run.hpm.key = I.led.hpm_ev.key;
  run.hpm.phase = I.led.hpm_ev.phase; run.hpm.mech = I.led.hpm_ev.mech;
  run.top_v = I.led.top.v; run.top_hash = I.led.top.hash; run.top_off = I.led.top.off; run.top_len = I.led.top.len; run.top_pool = I.led.top.pool;
  run.terminal = I.terminal;
  Json in = Json::object(); in["data.bin"] = f.dhash; in["setup.bin"] = f.shash; in["calib.bin"] = f.chash;
  std::string pa = tmp_path("x3_wp3_island.bin");
  island::write_island_file(pa, run, island::Arith::Bit, in);
  wp4io::Expect ex; ex.mode = fmt::M_LAW; ex.data_hash = f.dhash; ex.setup_hash = f.shash; ex.calib_hash = f.chash;
  merge::IslandHead h = wp4io::head_island(pa, 2, ex, nullptr);
  CHECK_MSG(h.load == merge::Load::ok && h.r == 2 && h.N == I.N && h.p == f.D.p && same_bits(h.logZ, I.logZ), h.detail);
  merge::IslandIn A = wp4io::load_island_full(pa, 4, f.D.p, ex);
  CHECK(A.r == 2 && same_bits(A.logZ, I.logZ) && A.pip == I.pip && A.ess == I.ess && A.terminal == I.terminal && A.rb_round.empty());
  CHECK(A.led.top.content_hash() == I.led.top.content_hash() && A.led.hpmS == I.led.hpmS && A.led.hpm_ev.key == I.led.hpm_ev.key &&
        same_bits(A.led.hpmF, I.led.hpmF) && same_bits(A.led.island_best[2], I.led.island_best[2]) && A.led.island_best.size() == 5);
  // phi from the grid: the HPM event is MEASURED in this fixture -> 1
  CHECK(A.led.hpm_ev.phi == 1.0);
  // (b) WP4's writer read by WP3's reader
  std::string pb = tmp_path("x3_wp4_island.bin");
  std::vector<double> grid{0, 0.3, 0.7, 1};
  wp4io::write_island(pb, fmt::M_LAW, I, in, nullptr, &grid);
  island::IslandFile F = island::read_island_file(pb);
  CHECK(F.rec.r == 2 && F.rec.N == I.N && F.rec.Hm == I.Hm && same_bits(F.rec.logZ, I.logZ) && F.rec.pip == I.pip && F.terminal == I.terminal);
  CHECK(F.rec.rb_round == I.rb_round && F.rec.led.top.content_hash() == I.led.top.content_hash() && F.rec.led.hpmS == I.led.hpmS &&
        F.rec.led.hpm_ev.key == I.led.hpm_ev.key && F.grid == grid);
  std::remove(pa.c_str()); std::remove(pb.c_str());
  cleanup(f);
}

#include <sys/wait.h>
namespace {
// runs a command; on an exit code other than `expect` (when given) its output is printed for the diagnosis
int run_cmd(const std::string& cmd, int expect = -1) {
  const std::string log = tmp_path("cli_cmd.log");
  int rc = std::system((cmd + " > '" + log + "' 2>&1").c_str());
  int code = WIFEXITED(rc) ? WEXITSTATUS(rc) : -1;
  if (expect >= 0 && code != expect) { std::ifstream f(log); std::string l; while (std::getline(f, l)) std::printf("    | %s\n", l.c_str()); }
  std::remove(log.c_str());
  return code;
}
std::string q(const std::string& s) { return "'" + s + "'"; }
struct DirGuard { std::string d; ~DirGuard() { if (!d.empty()) run_cmd("rm -rf " + q(d)); } };
}
TEST(wp4_io_merge_cli_and_driver_manifest) {
  // Review PR20 C-1 / M-1: the built smcbvs4 binary, called the way the CLI and the WP5 driver call it.
  const std::string bin = V4_SMCBVS4, tools = std::string(V4_FIXTURE_DIR) + "/../../tools/slurm";
  TmpGuard tmp_guard("cli"); Fx f = make_fx("cli", 16, fmt::M_V);   // the example plan's fits have R' = 16, mode V
  DirGuard dg{tmp_path("cli_dir")}; run_cmd("mkdir -p " + q(dg.d));
  std::string isl; for (size_t i = 0; i < f.ipath.size(); ++i) isl += (i ? "," : "") + f.ipath[i];
  const std::string base = bin + " merge --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(f.cpath) + " --mode V --threads 2";
  auto out = [&](const std::string& n) { return dg.d + "/" + n; };
  // explicit arguments: --islands as the CLI passes it (one comma-separated string), R' from --Rp
  CHECK_EQ(run_cmd(base + " --islands " + q(isl) + " --Rp 16 --out " + q(out("fit_ok.bin")), 0), 0);
  { fmt::Reader R(out("fit_ok.bin")); Json m = R.json("meta");
    CHECK(m.at("status").str() == "completed" && (int)m.at("Rp").num() == 16 && std::isfinite(m.at("logZ").num()) && R.has("pip_eq"));
    CHECK(m.at("inputs").at("island_1.bin").str() == wp4io::head_island(f.ipath[0], 1, wp4io::Expect{fmt::M_V, f.dhash, f.shash, f.chash}, nullptr).content_hash); }
  CHECK_EQ(run_cmd(base + " --islands " + q(isl) + " --out " + q(out("fit_noRp.bin"))), 13);                // no R'
  std::string isl15 = isl.substr(0, isl.rfind(','));
  CHECK_EQ(run_cmd(base + " --islands " + q(isl15) + " --Rp 16 --out " + q(out("fit_15.bin"))), 13);        // a subset
  CHECK_EQ(run_cmd(base + " --islands " + q(isl15 + "," + f.ipath[0]) + " --Rp 16 --out " + q(out("fit_dup.bin"))), 13);   // duplicate
  CHECK_EQ(run_cmd(base + " --islands '' --Rp 16 --out " + q(out("fit_empty.bin"))), 13);                    // empty list
  CHECK_EQ(run_cmd(base + " --islands " + q(isl) + " --Rp 0 --out " + q(out("fit_rp0.bin"))), 13);           // R' = 0
  CHECK_EQ(run_cmd(base + " --islands " + q(isl) + " --Rp 16"), 13);                                         // no --out
  CHECK_EQ(run_cmd(base + " --islands " + q(isl) + " --Rp 16 --mem-budget 1000 --out " + q(out("fit_mem.bin"))), 11);   // bytes
  { fmt::Reader R(out("fit_mem.bin")); Json m = R.json("meta");
    CHECK(m.at("fit_state").str() == "not_admitted" && !R.has("pip_eq") && m.at("mem_estimate").at("budget").num() == 1000); }
  CHECK_EQ(run_cmd(base + " --islands " + q(isl) + " --Rp 16 --mem-budget-gb 0.000001 --out " + q(out("fit_memgb.bin"))), 11);   // alias
  // the WP5 driver: dry run of the example plan -> the merge manifest template -> p1m_manifest.py fill -> smcbvs4 merge --manifest
  if (run_cmd("command -v python3") != 0) { std::printf("    python3 not found: driver-manifest part NOT RUN\n"); cleanup(f); return; }
  const std::string drv = dg.d + "/drv", dept = dg.d + "/dept";
  CHECK_EQ(run_cmd("python3 " + q(tools + "/p1m_driver.py") + " --plan " + q(tools + "/examples/plan_A2_pilot_1e4.json") + " --out " + q(drv) +
                   " --dept " + q(dept) + " --now 2026-11-16T00:00:00Z"), 0);
  const std::string tmpl = drv + "/manifests/A2_ARs_n200_r1/merge.json";
  Json T = read_json_file(tmpl);
  CHECK(T.at("mode").str() == "V" && (int)T.at("params").at("Rp").num() == 16 && T.at("inputs").size() == 19);
  // place the run's files where the template names them, with the producers' records
  std::string rundir;
  for (auto& [k, v] : T.at("inputs").items()) {
    std::string b = k.substr(k.find_last_of('/') + 1); rundir = k.substr(0, k.find_last_of('/'));
    std::string src = b == "data.bin" ? f.dpath : b == "setup.bin" ? f.spath : b == "calib.bin" ? f.cpath
                    : f.ipath[(size_t)std::stoi(b.substr(7, b.size() - 11)) - 1];
    run_cmd("mkdir -p " + q(rundir) + " && cp " + q(src) + " " + q(k));
    write_json_file(k + ".json", [] { Json j = Json::object(); j["status"] = "completed"; return j; }());
  }
  const std::string man = dg.d + "/merge_filled.json";
  CHECK_EQ(run_cmd("BIN=" + q(bin) + " python3 " + q(tools + "/p1m_manifest.py") + " fill --template " + q(tmpl) + " --out " + q(man) + " --bin " + q(bin)), 0);
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --threads 2 --out " + q(rundir + "/fit.bin")), 0);
  { fmt::Reader R(rundir + "/fit.bin"); Json m = R.json("meta");
    CHECK(m.at("status").str() == "completed" && (int)m.at("Rp").num() == 16 && R.has("pip_r") && R.entry("pip_r").dims[0] == 16); }
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --threads 2 --mem-budget 1000 --out " + q(rundir + "/fit_mem.bin")), 11);
  // an island input removed from the filled manifest: the merge is refused, never pooled as a subset
  Json M = read_json_file(man); Json in2 = Json::object();
  for (auto& [k, v] : M.at("inputs").items()) if (k.find("island_16.bin") == std::string::npos) in2[k] = v;
  M["inputs"] = in2; write_json_file(dg.d + "/merge_15.json", M);
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(dg.d + "/merge_15.json") + " --threads 2 --out " + q(rundir + "/fit_15.bin")), 13);
  // re-check n-3: with a manifest, an explicit argument that disagrees is refused, whatever the argument order
  std::string isl_m; for (int r = 1; r <= 15; ++r) isl_m += (r > 1 ? "," : "") + rundir + "/island_" + std::to_string(r) + ".bin";
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --Rp 15 --islands " + q(isl_m) + " --out " + q(rundir + "/fit_n3a.bin")), 13);
  CHECK_EQ(run_cmd(bin + " merge --Rp 15 --islands " + q(isl_m) + " --manifest " + q(man) + " --out " + q(rundir + "/fit_n3b.bin")), 13);
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --islands " + q(isl_m) + " --out " + q(rundir + "/fit_n3c.bin")), 13);
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --data " + q(f.dpath) + " --out " + q(rundir + "/fit_n3d.bin")), 13);
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --mode law --out " + q(rundir + "/fit_n3e.bin")), 13);
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --Rp 16 --out " + q(rundir + "/fit_n3f.bin"), 0), 0);   // agreeing: fine
  // re-check n-4: an oversized island index and bad budgets -> invalid_input (13); 0 = off
  { Json M2 = read_json_file(man); Json in3 = M2.at("inputs"); in3[rundir + "/island_99999999999.bin"] = in3.at(rundir + "/island_1.bin").str();
    M2["inputs"] = in3; write_json_file(dg.d + "/merge_big.json", M2); }
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(dg.d + "/merge_big.json") + " --out " + q(rundir + "/fit_n4a.bin")), 13);
  for (const char* b : {"-5", "1e30", "1.5", "nan"})
    CHECK_MSG(run_cmd(bin + " merge --manifest " + q(man) + " --mem-budget " + b + " --out " + q(rundir + "/fit_n4b.bin")) == 13, std::string("--mem-budget ") + b);
  CHECK_EQ(run_cmd(bin + " merge --manifest " + q(man) + " --mem-budget 0 --out " + q(rundir + "/fit_n4c.bin"), 0), 0);
  cleanup(f);
}

#include <functional>
#include <unistd.h>
namespace {
// Rewrites one section of an engine file hash-consistently (the WP1 Writer recomputes every hash): the review PR20 probe.
using Bytes = std::vector<uint8_t>;
void rewrite(const std::string& src, const std::string& dst, const std::string& name, const std::function<void(Bytes&, uint64_t&, uint64_t&)>& mut) {
  std::vector<std::pair<std::string, Bytes>> secs; std::vector<std::array<uint64_t, 3>> meta_d; std::vector<uint32_t> dt; Json meta;
  uint32_t kind, mode;
  { fmt::Reader R(src); kind = R.kind(); mode = R.mode();
    for (auto& e : R.sections()) {
      std::string n(e.name);
      if (e.dtype == fmt::D_JSON) { meta = R.json(n); continue; }
      const uint8_t* p = nullptr;
      switch (e.dtype) {
        case fmt::D_F64: p = (const uint8_t*)R.get<double>(n); break;   case fmt::D_I32: p = (const uint8_t*)R.get<int32_t>(n); break;
        case fmt::D_U32: p = (const uint8_t*)R.get<uint32_t>(n); break; case fmt::D_I64: p = (const uint8_t*)R.get<int64_t>(n); break;
        case fmt::D_U64: p = (const uint8_t*)R.get<uint64_t>(n); break; case fmt::D_U8: p = (const uint8_t*)R.get<uint8_t>(n); break;
        case fmt::D_U16: p = (const uint8_t*)R.get<uint16_t>(n); break; default: p = (const uint8_t*)R.get<float>(n);
      }
      secs.push_back({n, Bytes(p, p + e.length)}); meta_d.push_back({e.dims[0], e.dims[1], 0}); dt.push_back(e.dtype);
    } }
  fmt::Writer W(kind, mode);
  W.add_json("meta", meta);
  for (size_t i = 0; i < secs.size(); ++i) {
    uint64_t d0 = meta_d[i][0], d1 = meta_d[i][1];
    if (secs[i].first == name) mut(secs[i].second, d0, d1);
    W.add_copy(secs[i].first, dt[i], secs[i].second.data(), secs[i].second.size(), d0, d1);
  }
  W.write(dst);
}
template <class T> std::function<void(Bytes&, uint64_t&, uint64_t&)> set_at(size_t i, T v) {
  return [i, v](Bytes& b, uint64_t&, uint64_t&) { std::memcpy(b.data() + i * sizeof(T), &v, sizeof(T)); };
}
template <class T> std::function<void(Bytes&, uint64_t&, uint64_t&)> set_all(std::vector<T> v) {
  return [v](Bytes& b, uint64_t& d0, uint64_t&) { b.assign((const uint8_t*)v.data(), (const uint8_t*)(v.data() + v.size())); d0 = v.size(); };
}
// 0 = refused (invalid_input, record or exception), 1 = accepted as completed, 2 = other status, 3 = other exception;
// a crash is a signal. The merge runs in a forked child (one thread), so a crash cannot kill the test binary.
int merge_in_child(const Json& args, Json* rec_out_file = nullptr) {
  (void)rec_out_file;
  std::fflush(stdout);
  pid_t pid = fork();
  if (pid == 0) {
    int code = 3;
    try { Json r = merge::run(args); const std::string st = r.at("status").str(); code = st == "invalid_input" ? 0 : st == "completed" ? 1 : 2; }
    catch (const Error& e) { code = e.st == Status::invalid_input ? 0 : 3; }
    catch (...) { code = 3; }
    _exit(code);
  }
  int ws = 0; waitpid(pid, &ws, 0);
  return WIFEXITED(ws) ? WEXITSTATUS(ws) : 100 + (WIFSIGNALED(ws) ? WTERMSIG(ws) : 0);
}
}  // namespace

TEST(wp4_io_hostile_files_refused) {
  // Review PR20 M-2: hash-consistent files with bad content (the reviewer's corrupt-file list). Every case is refused with
  // invalid_input -- never a crash, never a completed fit; H19 (other islands' island_best entries) is accepted with
  // those entries ignored.
  TmpGuard tmp_guard("hos"); Fx f = make_fx("hos", 4);
  const int p = f.D.p;
  auto args = [&](const std::string& out) { Json a = merge_args(f, out, 1); return a; };
  CHECK_EQ(merge_in_child(args(tmp_path("hos_fit_base.bin"))), 1);   // the untouched fixture completes
  struct Case { const char* id; int file; const char* sec; std::function<void(Bytes&, uint64_t&, uint64_t&)> mut; int want; };
  // file: 0 island 1, 1 island 2, 10 calib, 20 setup
  Model h0 = f.isl[0].led.hpmS; double hF = f.isl[0].led.hpmF;
  size_t multi = 0;   // a store entry with >= 2 members (for the unsorted-model case)
  { const Store& t = f.isl[0].led.top; for (size_t i = 0; i < t.size(); ++i) if (t.len[i] >= 2) { multi = t.off[i]; break; } }
  std::vector<Case> cases = {
    {"H1 top_pool index p+1e8", 0, "top_pool", set_at<int32_t>(0, p + 100000000), 0},
    {"H2 top_pool index -1", 0, "top_pool", set_at<int32_t>(0, -1), 0},
    {"H3 unsorted store model", 0, "top_pool", [multi](Bytes& b, uint64_t&, uint64_t&) { int32_t* q = (int32_t*)b.data() + multi; std::swap(q[0], q[1]); }, 0},
    {"H4 top_off wraps", 0, "top_off", set_at<uint64_t>(1, UINT64_MAX), 0},
    {"H5 hpm_S index p+1e8", 0, "hpm_S", set_all<int32_t>({p + 100000000}), 0},
    {"H6 hpm_S unsorted", 0, "hpm_S", set_all<int32_t>({5, 2}), 0},
    {"H7 hpm_ev phase 99 mech 77", 0, "hpm_ev", [](Bytes& b, uint64_t&, uint64_t&) { int64_t* e = (int64_t*)b.data(); e[10] = 99; e[11] = 77; }, 0},
    {"H8 hpm_val F NaN", 0, "hpm_val", set_at<double>(0, std::numeric_limits<double>::quiet_NaN()), 0},
    {"H9 top_v NaN", 0, "top_v", set_at<double>(0, std::numeric_limits<double>::quiet_NaN()), 0},
    {"H10 st_ess length 1", 0, "st_ess", set_all<double>({40.0}), 0},
    {"H11 empty grid", 0, "grid", set_all<double>({}), 0},
    {"H11b grid not calib's", 0, "grid", set_all<double>({0, 0.5, 0.75, 1}), 0},
    {"H16 top_len past the pool", 0, "top_len", set_at<uint16_t>(0, 60000), 0},
    {"H17 empty logZ", 0, "logZ", set_all<double>({}), 0},
    {"H18 pip_r NaN", 0, "pip_r", set_at<double>(0, std::numeric_limits<double>::quiet_NaN()), 0},
    {"H18b pip_r > 1", 0, "pip_r", set_at<double>(0, 1.5), 0},
    {"H20 logical size", 0, "logical", set_all<uint64_t>({1, 2, 3}), 0},
    {"H21 hpm_ev stage > T", 0, "hpm_ev", [](Bytes& b, uint64_t&, uint64_t&) { ((int64_t*)b.data())[5] = 99; }, 0},
    {"H22 hpm_ev other island", 0, "hpm_ev", [](Bytes& b, uint64_t&, uint64_t&) { ((int64_t*)b.data())[3] = 3; }, 0},
    {"H23 terminal index p+1e8", 0, "terminal_S", set_at<int32_t>(0, p + 100000000), 0},
    {"C1 calib inh_idx p+1e8", 10, "inh_idx", set_at<int32_t>(0, p + 100000000), 0},
    {"C2 calib hpm_S p+1e8", 10, "hpm_S", set_all<int32_t>({p + 100000000}), 0},
    {"C3 calib inh_F NaN", 10, "inh_F", set_at<double>(0, std::numeric_limits<double>::quiet_NaN()), 0},
    {"C4 calib inh_ptr wraps", 10, "inh_ptr", set_at<int64_t>(1, (int64_t)1 << 40), 0},
    {"S2 setup pos 40", 20, "pos", set_at<int32_t>(0, 40), 0},
    {"S3 setup code_ptr 1e12", 20, "code_ptr", set_at<int64_t>(0, 1000000000000LL), 0},
    {"S4 setup tstore pool p+1e8", 20, "tstore_top_pool", set_at<int32_t>(0, p + 100000000), 0},
    {"S5 setup mode_S p+1e8", 20, "mode_S", set_all<int32_t>({p + 100000000}), 0},
    {"S6 setup blk out of range", 20, "blk", set_at<int32_t>(0, 1000000), 0},
    {"S7 setup logr NaN", 20, "logr", set_at<double>(1, std::numeric_limits<double>::quiet_NaN()), 0},
    // review PR20 re-check n-1 / n-2
    {"N1 top_hash wrong (all XORed)", 0, "top_hash", [](Bytes& b, uint64_t&, uint64_t&) { for (size_t i = 0; i < b.size() / 8; ++i) ((uint64_t*)b.data())[i] ^= 0x5A5A5A5A5A5A5A5AULL; }, 0},
    {"N1b setup tstore hash wrong", 20, "tstore_top_hash", [](Bytes& b, uint64_t&, uint64_t&) { ((uint64_t*)b.data())[0] ^= 1; }, 0},
    {"N2 st_ess NaN", 0, "st_ess", set_at<double>(0, std::numeric_limits<double>::quiet_NaN()), 0},
    {"N2b st_ess -5", 0, "st_ess", set_at<double>(0, -5.0), 0},
    {"N2c st_ess 1e9 > N", 0, "st_ess", set_at<double>(0, 1e9), 0},
    {"N3 own island_best 1e300", 0, "island_best", set_at<double>(1, 1e300), 0},
    {"N3b own island_best -inf", 0, "island_best", set_at<double>(1, -std::numeric_limits<double>::infinity()), 0},
    {"N4 hpm log m +inf", 0, "hpm_val", set_at<double>(1, std::numeric_limits<double>::infinity()), 0},
    {"N5 hpm_ev tier 1 (calib tier 0)", 0, "hpm_ev", [](Bytes& b, uint64_t&, uint64_t&) { ((int64_t*)b.data())[1] = 1; }, 0},
    {"N5b hpm_ev sub 300", 0, "hpm_ev", [](Bytes& b, uint64_t&, uint64_t&) { ((int64_t*)b.data())[9] = 300; }, 0},
  };
  (void)h0; (void)hF;
  for (auto& c : cases) {
    const std::string src = c.file == 10 ? f.cpath : c.file == 20 ? f.spath : f.ipath[(size_t)c.file];
    const std::string keep = src + ".orig";
    run_cmd("cp " + q(src) + " " + q(keep));
    rewrite(keep, src, c.sec, c.mut);
    int got = merge_in_child(args(tmp_path("hos_fit_case.bin")));
    CHECK_MSG(got == c.want, std::string(c.id) + ": got " + std::to_string(got) + (got >= 100 ? " (CRASH, signal " + std::to_string(got - 100) + ")" : ""));
    run_cmd("mv " + q(keep) + " " + q(src));
  }
  // H19: island 2's entries for the other islands (1e300) are ignored: island_best of island 1 is island 1's own
  { const std::string src = f.ipath[1], keep = src + ".orig";
    run_cmd("cp " + q(src) + " " + q(keep));
    rewrite(keep, src, "island_best", set_at<double>(1, 1e300));
    Json r = merge::run(args(tmp_path("hos_fit_h19.bin")));
    fmt::Reader R(tmp_path("hos_fit_h19.bin"));
    std::vector<double> ib = R.vec<double>("island_best");
    CHECK(r.at("status").str() == "completed" && ib.size() == 5 && ib[1] == f.isl[0].led.island_best[1] && ib[1] < 1e300);
    run_cmd("mv " + q(keep) + " " + q(src)); }
  cleanup(f);
}
