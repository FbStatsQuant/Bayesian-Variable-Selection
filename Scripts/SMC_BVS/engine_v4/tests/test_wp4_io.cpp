// test_wp4_io.cpp -- WP4 files: calib.bin / island_r.bin / fit.bin round trips, input validation by content hash and
// binary block (T10 through real files), and the merge command end to end (thread invariance of fit.bin).
#include <cstdio>
#include <fstream>
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
};
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
  f.spath = tmp_path(tag + "_setup.bin");
  Json sin = Json::object(); sin["data.bin"] = f.dhash;
  f.shash = wp4io::write_setup_min(f.spath, S, sin);
  // calibration: a ledger with some scored models; inherited = its top store models
  std::mt19937_64 g(11);
  Ev ev(&f.D, &S);
  LedgerConfig cfg; cfg.p = p; cfg.islands = 4; cfg.leaders = mode == fmt::M_COMPAT; cfg.fresh_counters = false;
  Ledger cl(cfg);
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
  calib::CalibOut co; co.status = calib::CalStatus::ok; co.tier_final = 0; co.has_frozen = true;
  co.frozen.grid = {0, 0.3, 1}; co.frozen.grid_unrefined = co.frozen.grid; co.frozen.grid_label = "rebuild_1"; co.I_used = 1;
  calib::TierOut t0; t0.tier = 0; t0.has_triggers = true; calib::GridRecord gr; gr.label = "preliminary"; gr.grid = {0, 0.3, 1}; t0.grids.push_back(gr);
  co.tiers.push_back(t0);
  wp4io::CalibWrite cw; cw.mode = mode; cw.co = &co; cw.led = &cl; cw.inherited = f.inh; cw.N = 50; cw.L = 4; cw.Hm = 4;
  cw.inputs["data.bin"] = f.dhash; cw.inputs["setup.bin"] = f.shash;
  f.cpath = tmp_path(tag + "_calib.bin");
  f.chash = wp4io::write_calib(f.cpath, cw);
  // islands
  for (int r = 1; r <= R; ++r) {
    merge::IslandIn I; I.r = r; I.N = 50; I.T = 3; I.L = 4; I.Hm = 4; I.logZ = -30 + 0.07 * r; I.ess = {40, 45, 48};
    I.pip.resize(p); I.rb_acc.resize(p);
    for (int j = 0; j < p; ++j) { I.pip[j] = std::fmod(0.017 * (j + 1) * (r + 3), 1.0); I.rb_acc[j] = I.pip[j] * 200; }
    I.rb_round.assign(4, std::vector<double>(p, 1.0));
    LedgerConfig ic = cfg; ic.leaders = false; I.led.init(ic);
    for (int t = 0; t < 400; ++t) {
      Model M = random_model(g, p, 5); double lm, lg0, dd, F; ev(M, lm, lg0, dd, F);
      EventCtx e; e.phase = PH_MEASURED; e.mech = ME_GIBBS_FLIP; e.phi = 1; e.key.seg = SG_FINAL; e.key.unit = (uint32_t)r; e.key.xph = X_MEASURED;
      e.key.stage = 3; e.key.round = 1 + t / 100; e.key.particle = 1 + t % 100; e.key.position = 1 + (uint32_t)(g() % 30); e.key.sub = 1;
      I.led.event(M, f.D.zob.hash(M), F, lg0, lm, e, true);
      if (t >= 350) I.terminal.push_back(M);
    }
    I.led.compact();
    f.isl.push_back(I);
    std::string ip = tmp_path(tag + "_island_" + std::to_string(r) + ".bin");
    Json in = Json::object(); in["data.bin"] = f.dhash; in["setup.bin"] = f.shash; in["calib.bin"] = f.chash;
    wp4io::write_island(ip, mode, I, in, &clean_block());
    f.ipath.push_back(ip);
  }
  return f;
}
Json merge_args(const Fx& f, const std::string& out, int threads) {
  Json a = Json::object();
  a["data"] = f.dpath; a["setup"] = f.spath; a["calib"] = f.cpath; a["out"] = out; a["mode"] = "compat";
  a["threads"] = threads; a["chunk"] = 7; a["ell"] = 3;
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
void cleanup(const Fx& f) {
  std::remove(f.dpath.c_str()); std::remove(f.spath.c_str()); std::remove(f.cpath.c_str());
  for (auto& p : f.ipath) std::remove(p.c_str());
}
}  // namespace

TEST(wp4_io_calib_island_roundtrip) {
  Fx f = make_fx("rt", 2);
  wp4io::CalibIn c = wp4io::read_calib(f.cpath);
  CHECK(c.status == "ok" && c.grid == std::vector<double>({0, 0.3, 1}) && c.N == 50 && c.L == 4 && c.tier == 0 && c.content_hash == f.chash);
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
        a.rb_round.size() == 4 && a.rb_round[0].size() == (size_t)f.D.p && a.led.lead0.cap == 0);
  bool lg = true; for (int x = 0; x < N_PHASE; ++x) for (int y = 0; y < N_MECH; ++y) lg = lg && a.led.logical[x][y] == b.led.logical[x][y];
  CHECK(lg && blk.contains("git_commit"));
  wp4io::SetupView S2 = wp4io::read_setup(f.spath);
  CHECK(S2.ttop.content_hash() == f.S.ttop.content_hash() && S2.logr == f.S.logr && S2.mode_S == f.S.mode_S);
  CHECK(S2.table_event_count(f.D.K) == (uint64_t)(4 * (f.D.p / 2) + (f.D.p % 2 ? 2 : 0)));
  cleanup(f);
}

TEST(wp4_io_load_island_t10) {
  Fx f = make_fx("t10", 4);
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
  wp4io::write_island(f.ipath[3], fmt::M_COMPAT, f.isl[3], in, &other);
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
  Fx f = make_fx("e2e", 4);
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
  wp4io::write_island(f.ipath[2], fmt::M_COMPAT, f.isl[2], in, &clean_block());   // repaired
  { merge::IslandIn bad = f.isl[0]; bad.status = Status::numerical_failure;
    wp4io::write_island(f.ipath[0], fmt::M_COMPAT, bad, in, &clean_block()); refused(tmp_path("e2e_fit_numfail.bin"), Status::numerical_failure);
    wp4io::write_island(f.ipath[0], fmt::M_COMPAT, f.isl[0], in, &clean_block()); }
  { Json dirty = clean_block(); dirty["git_commit"] = std::string(40, 'a') + "-dirty";   // theory mode refuses a dirty build
    wp4io::write_island(f.ipath[1], fmt::M_COMPAT, f.isl[1], in, &dirty); refused(tmp_path("e2e_fit_dirty.bin"), Status::invalid_input);
    wp4io::write_island(f.ipath[1], fmt::M_COMPAT, f.isl[1], in, &clean_block()); }
  { // --mem-budget admission through the command: refused before any island store is loaded
    Json a2 = merge_args(f, tmp_path("e2e_fit_mem.bin"), 1); a2["mem_budget_gb"] = 1e-6;
    Json r = merge::run(a2);
    fmt::Reader R(tmp_path("e2e_fit_mem.bin")); Json meta = R.json("meta");
    CHECK(r.at("status").str() == "resource_limit" && meta.at("fit_state").str() == "not_admitted" && !R.has("pip_eq") && meta.contains("mem_estimate"));
    std::remove(tmp_path("e2e_fit_mem.bin").c_str());
  }
  { // v0.1.8: a non-completed island file carries no estimate section
    merge::IslandIn bad = f.isl[0]; bad.status = Status::numerical_failure;
    std::string bp = tmp_path("e2e_bad_island.bin"); wp4io::write_island(bp, fmt::M_COMPAT, bad, in, &clean_block());
    fmt::Reader R(bp);
    CHECK(!R.has("logZ") && !R.has("pip_r") && !R.has("rb_acc") && !R.has("rb_round") && !R.has("terminal_S") && !R.has("st_inc") && R.has("st_ess") && R.has("hpm_ev"));
    std::remove(bp.c_str());
  }
  // the merge's own inputs: a manifest hash mismatch for calib.bin refuses the whole job (invalid_input thrown)
  Json man = Json::object(); man["inputs"]["calib.bin"] = "00ff"; std::string mp = tmp_path("e2e_manifest.json"); write_json_file(mp, man);
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
