// test_offer_floor.cpp -- WP7 O6: the D-29 offer floor (INTERFACES v0.1.15 §4.1, §5.1, §7; v0.1.17).
//  * the island's top store under a floor f = the unfloored store restricted to v >= f (ties kept);
//  * run_island refuses a floor outside V-mode final islands, NaN / +inf floors, a floor without its calib.bin, and a
//    resume under another floor; the science outputs of a floored island equal the unfloored island's;
//  * calib.bin tau_cal = the c-th best F of the inherited models (written, read back, checked);
//  * end to end: calibrate (V) -> islands with and without the floor -> merge: every fit.bin section (HPM, log Z_r,
//    PIPs, the merged top store, the tail) identical; the merge refuses floors from another calib.bin, off tau_cal,
//    NaN, outside V mode, and above the pre-island cut-off.
#include <omp.h>
#include <cmath>
#include <cstdio>
#include <filesystem>
#include <map>
#include <random>
#include "tk.h"
#include "tutil.h"
#include "tutil_island.h"
#include "v4/calib_run.h"
#include "v4/format.h"
#include "v4/island/island.h"
#include "v4/island/island_file.h"
#include "v4/island/setup_load.h"
#include "v4/merge.h"
#include "v4/offer_floor.h"
#include "v4/prep.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"

using namespace v4::island;
static const double NINF = -__builtin_huge_val();

namespace {
struct Tmp {   // temporary files under $TMPDIR, removed at the end (also on failure)
  std::vector<std::string> paths;
  std::string add(const std::string& n) { paths.push_back(tmp_path("o6_" + n)); return paths.back(); }
  ~Tmp() { std::error_code ec; for (auto& p : paths) { std::filesystem::remove(p, ec); std::filesystem::remove(p + ".json", ec); } }
};
struct Fx {
  Data D; Start st; Neighbours nb;
  Fx(int n, int p, uint64_t seed) { make_ar_data(D, n, p, 0.6, seed); build_start(st, D, contiguous_blocks(p, 4)); nb = window_neighbours(D, 14, 8); }
};
IslandConfig small_v() {
  IslandConfig c; c.seed = 42; c.island = 3; c.N = 48; c.L = 2; c.Hm = 2; c.B = 14;
  c.grid = {0.0, 0.05, 0.15, 0.35, 0.65, 1.0}; c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  return c;
}
std::vector<std::pair<double, Model>> entries(const IslandRun& r) {
  std::vector<std::pair<double, Model>> e;
  for (size_t i = 0; i < r.top_v.size(); ++i) e.push_back({r.top_v[i], Model(r.top_pool.begin() + r.top_off[i], r.top_pool.begin() + r.top_off[i] + r.top_len[i])});
  return e;
}
std::string bits(double x) { return v4::f64_hex(x); }
}  // namespace

// The floor on the store: content = the unfloored store restricted to v >= f, ties kept; leaders untouched.
TEST(offer_floor_store_is_unfloored_above_f) {
  std::mt19937_64 g(5);
  std::vector<std::pair<double, Model>> offers;
  for (int i = 0; i < 60000; ++i) {
    Model S; int k = 1 + (int)(g() % 4); while ((int)S.size() < k) { int j = (int)(g() % 80); if (!contains(S, j)) sorted_insert(S, j); }
    offers.push_back({-std::floor((double)(g() % 3000) / 7.0), S});   // many ties
  }
  std::vector<uint64_t> key(80); uint64_t x = 3; for (auto& k : key) k = splitmix64(x);
  auto H = [&](const Model& S) { uint64_t h = 0; for (int j : S) h ^= key[j]; return h; };
  for (uint64_t cap : {50ull, 5000ull, 100000ull}) {
    TopStore ref; ref.init(cap, Order::HPM);
    std::vector<StoreBuffer> b0(3);
    #pragma omp parallel for num_threads(3) schedule(dynamic, 64)
    for (size_t i = 0; i < offers.size(); ++i) ref.offer(b0[omp_get_thread_num()], offers[i].first, offers[i].second.data(), (uint32_t)offers[i].second.size(), H(offers[i].second));
    for (auto& b : b0) ref.flush(b);
    ref.compact();
    for (double f : {NINF, -200.0, -100.0, ref.size() ? ref.value(ref.size() / 2) : 0.0, 1e9}) {
      TopStore st; st.init(cap, Order::HPM); st.floor = f;
      std::vector<StoreBuffer> b1(3);
      #pragma omp parallel for num_threads(3) schedule(dynamic, 64)
      for (size_t i = 0; i < offers.size(); ++i) st.offer(b1[omp_get_thread_num()], offers[i].first, offers[i].second.data(), (uint32_t)offers[i].second.size(), H(offers[i].second));
      uint64_t dropped = 0; for (auto& b : b1) { st.flush(b); dropped += b.n_floor_dropped; }
      st.compact();
      size_t want = 0; while (want < ref.size() && ref.value(want) >= f) ++want;   // ref is sorted: the prefix v >= f
      bool ok = st.size() == want && st.check_invariant() && st.cutoff() == (st.size() >= cap ? st.value(st.size() - 1) : NINF);
      for (size_t i = 0; ok && i < want; ++i) ok = bits(st.value(i)) == bits(ref.value(i)) && st.model(i) == ref.model(i);
      uint64_t below = 0; for (auto& o : offers) below += o.first < f;
      CHECKF(ok && dropped == below, "cap %llu floor %g: %zu vs %zu entries, dropped %llu of %llu", (unsigned long long)cap, f, st.size(), want,
             (unsigned long long)dropped, (unsigned long long)below);
    }
  }
}

// run_island: the floor's roles and values (review PR45 MINOR-2/3), science outputs unchanged, store = unfloored >= f,
// island_r.bin meta round trip, and no resume under another floor.
TEST(offer_floor_island_roles_and_science) {
  Tmp tmp;
  Fx F(100, 300, 61);
  IslandConfig c = small_v();
  IslandRun r0 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
  CHECK(r0.status == 0 && r0.top_v.size() > 100 && std::isinf(r0.offer_floor));
  const double f = r0.top_v[r0.top_v.size() / 3];
  IslandConfig cf = c; cf.offer_floor = f; cf.offer_floor_calib = "0xcalibhash";
  IslandRun r1 = run_island<Arith::ClassA>(F.D, F.st, F.nb, cf);
  // science: everything but the store is identical (V counts every consumed score; the floor only drops store offers)
  bool same = r1.status == 0 && bits(r1.logZ) == bits(r0.logZ) && r1.init_hash == r0.init_hash && r1.pip == r0.pip && r1.rb_acc == r0.rb_acc &&
              r1.rb_round == r0.rb_round && r1.terminal == r0.terminal && r1.terminal_distinct == r0.terminal_distinct &&
              std::memcmp(r1.logical, r0.logical, sizeof r0.logical) == 0 && bits(r1.island_best) == bits(r0.island_best) &&
              r1.hpm.S == r0.hpm.S && bits(r1.hpm.F) == bits(r0.hpm.F) && r1.hpm.key == r0.hpm.key && r1.stages.size() == r0.stages.size();
  for (size_t i = 0; same && i < r0.stages.size(); ++i) same = bits(r1.stages[i].ess) == bits(r0.stages[i].ess) && bits(r1.stages[i].inc) == bits(r0.stages[i].inc);
  CHECK(same);
  auto e0 = entries(r0), e1 = entries(r1);
  size_t want = 0; while (want < e0.size() && e0[want].first >= f) ++want;
  bool sto = e1.size() == want && r1.ks.store_floor_dropped > 0;
  for (size_t i = 0; sto && i < want; ++i) sto = bits(e1[i].first) == bits(e0[i].first) && e1[i].second == e0[i].second;
  CHECKF(sto, "store %zu entries vs %zu above the floor (dropped %llu)", e1.size(), want, (unsigned long long)r1.ks.store_floor_dropped);
  // island_r.bin: the floor round-trips; the unfloored file reads -inf
  {
    const std::string a = tmp.add("isl_floor.bin"), b = tmp.add("isl_nofloor.bin");
    write_island_file(a, r1, Arith::ClassA, v4::Json::object()); write_island_file(b, r0, Arith::ClassA, v4::Json::object());
    IslandFile fa = read_island_file(a), fb = read_island_file(b);
    CHECK(bits(fa.offer_floor) == bits(f) && fa.offer_floor_calib == "0xcalibhash" && fa.meta.at("offer_floor_hex").str() == v4::f64_hex(f));
    CHECK(std::isinf(fb.offer_floor) && fb.offer_floor < 0 && fb.offer_floor_calib.empty() && fb.meta.at("offer_floor_calib").is_null());
  }
  // refusals (invalid_input): law (bit form), compat, leaders, a calibration role, NaN, +inf, no calib hash
  auto refused = [&](const char* what, auto&& fn) {
    bool r = false; try { fn(); } catch (const v4::Error& e) { r = e.st == v4::Status::invalid_input; }
    CHECKF(r, "%s: not refused", what);
  };
  refused("law (bit form)", [&] { IslandConfig x = cf; x.allow_test_kernels = true; run_island<Arith::Bit>(F.D, F.st, F.nb, x); });
  refused("compat", [&] { IslandConfig x = cf; x.compat = true; x.kernel = KernelKind::ParticleMajor; x.threads = 1; run_island<Arith::ClassA>(F.D, F.st, F.nb, x); });
  refused("leaders", [&] { IslandConfig x = cf; x.leaders = true; run_island<Arith::ClassA>(F.D, F.st, F.nb, x); });
  refused("pilot role", [&] { IslandConfig x = cf; x.role = IslandRole::Pilot; x.island = 0; x.iter = 0; run_island<Arith::ClassA>(F.D, F.st, F.nb, x); });
  refused("NaN", [&] { IslandConfig x = cf; x.offer_floor = std::nan(""); run_island<Arith::ClassA>(F.D, F.st, F.nb, x); });
  refused("+inf", [&] { IslandConfig x = cf; x.offer_floor = __builtin_huge_val(); run_island<Arith::ClassA>(F.D, F.st, F.nb, x); });
  refused("no calib hash", [&] { IslandConfig x = cf; x.offer_floor_calib.clear(); run_island<Arith::ClassA>(F.D, F.st, F.nb, x); });
  // a checkpoint written under one floor is not resumed under another (fingerprint)
  {
    IslandConfig a = cf; a.ckpt_path = tmp.add("ckpt"); a.ckpt_every_s = 1e9; a.stop_after_step = 2;
    for (const char* s : {".a", ".b"}) tmp.paths.push_back(a.ckpt_path + s);
    CHECK(run_island<Arith::ClassA>(F.D, F.st, F.nb, a).status == 1);
    refused("resume under another floor", [&] { IslandConfig b = a; b.stop_after_step = -1; b.offer_floor = std::nextafter(f, 0.0); run_island<Arith::ClassA>(F.D, F.st, F.nb, b); });
    IslandConfig b = a; b.stop_after_step = -1;
    IslandRun rr = run_island<Arith::ClassA>(F.D, F.st, F.nb, b);
    CHECK(rr.status == 0 && rr.resumed_from_step == 2 && rr.hash() == r1.hash());
  }
}

// the pure merge rule (merge::offer_floor_refusal) on every branch
TEST(offer_floor_merge_rule) {
  v4::merge::IslandHead h;
  CHECK(v4::merge::offer_floor_refusal(h, false, "c", 1.0, 0.0).empty());   // no floor: always fine
  h.floor = -5.0; h.floor_calib = "c";
  CHECK(v4::merge::offer_floor_refusal(h, true, "c", -5.0, -5.0).empty());   // floor == cut-off: kept (<=)
  CHECK(v4::merge::offer_floor_refusal(h, true, "c", -5.0, -4.0).empty());
  CHECK(!v4::merge::offer_floor_refusal(h, true, "c", -5.0, std::nextafter(-5.0, -10.0)).empty());   // above the cut-off
  CHECK(!v4::merge::offer_floor_refusal(h, true, "c", -5.0, NINF).empty());   // pre store not full: cut-off -inf
  CHECK(!v4::merge::offer_floor_refusal(h, false, "c", -5.0, 0.0).empty());   // not V
  CHECK(!v4::merge::offer_floor_refusal(h, true, "d", -5.0, 0.0).empty());    // another calib.bin
  CHECK(!v4::merge::offer_floor_refusal(h, true, "c", std::nextafter(-5.0, 0.0), 0.0).empty());   // not tau_cal's bits
  h.floor = std::nan(""); CHECK(!v4::merge::offer_floor_refusal(h, true, "c", -5.0, 0.0).empty());
  h.floor = __builtin_huge_val(); CHECK(!v4::merge::offer_floor_refusal(h, true, "c", -5.0, 1e300).empty());
  // tau_cal: the c-th largest, -inf below c values
  CHECK(v4::tau_cal_of({3, 1, 2, 5, 4}, 2) == 4.0 && v4::tau_cal_of({3, 1, 2}, 3) == 1.0 && std::isinf(v4::tau_cal_of({3, 1}, 3)));
  v4::Json m = v4::Json::object(); v4::tau_cal_to_meta(m, -1.25);
  CHECK(v4::tau_cal_of_meta(m) == -1.25 && std::isinf(v4::tau_cal_of_meta(v4::Json::object())));
  CHECK(std::isinf(v4::offer_floor_from_calib(m, false, "h").f) && v4::offer_floor_from_calib(m, true, "h").f == -1.25 &&
        v4::offer_floor_from_calib(m, true, "h").calib == "h");
}

// End to end at small p: calibrate (V) writes tau_cal; final islands with and without the floor; the merge gives the
// same fit.bin (every section but meta); tampered floors are refused (invalid_input, no estimates: GUARD-W).
TEST(offer_floor_end_to_end_merge) {
  Tmp tg;
  const int n = 60, p_raw = 30;
  std::vector<double> X((size_t)n * p_raw), y(n);
  { std::mt19937_64 g(41); std::normal_distribution<double> nd;
    for (int i = 0; i < n; ++i) { double prev = 0; for (int j = 0; j < p_raw; ++j) { double x = 0.6 * prev + 0.8 * nd(g); X[(size_t)j * n + i] = x; prev = x; } }
    for (int i = 0; i < n; ++i) y[i] = 1.2 * X[(size_t)2 * n + i] - 0.9 * X[(size_t)11 * n + i] + nd(g); }
  v4::prep::Result pr = v4::prep::preprocess(X.data(), y.data(), n, p_raw);
  CHECK(pr.status == "ok");
  v4::Data D = v4::make_data(pr.own, n, pr.p);
  const int p = D.p;
  const std::string dpath = tg.add("of_data.bin"), s0 = tg.add("of_setup0.bin"), spath = tg.add("of_setup.bin");
  const std::string dhash = v4::prep::write_data(dpath, D, pr, "B", v4::Json::object());
  // setup: blocks of 3, the island's own tables (core's arithmetic), table stores over every table model
  Start st; build_start(st, D, contiguous_blocks(p, 3));
  Neighbours nb = window_neighbours(D, 6, 4);
  v4::wp4io::SetupView S; S.blk = st.blk; S.pos = st.pos; S.blk_ptr.push_back(0);
  S.ttop.init(40ull * p + 1, Order::HPM); S.tlead0.init(20ull * p, Order::LEX); S.tlead1.init(20ull * p, Order::LEX);
  BitScorer sc(&D);
  for (int b = 0; b < st.J; ++b) {
    for (int j : st.blocks[b]) S.blk_members.push_back(j);
    S.blk_ptr.push_back((int64_t)S.blk_members.size()); S.code_ptr.push_back((int64_t)S.logr.size());
    for (uint32_t c = 0; c < st.logr[b].size(); ++c) {
      S.logr.push_back(st.logr[b][c]);
      Model U; for (size_t i = 0; i < st.blocks[b].size(); ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
      if ((int)U.size() > D.K) continue;
      double F = D.logprior[U.size()] + sc.score(U).logm, lg0 = D.logprior[U.size()] + st.logr[b][c];
      S.ttop.offer(F, U, D.zob.hash(U)); S.tlead0.offer(lg0, U, D.zob.hash(U)); S.tlead1.offer(F, U, D.zob.hash(U));
    }
  }
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  S.mode_S = Model(S.ttop.model(0).begin(), S.ttop.model(0).end());
  v4::Json sin = v4::Json::object(); sin["data.bin"] = dhash;
  v4::wp4io::write_setup_min(s0, S, sin);
  { v4::fmt::Reader R(s0); v4::fmt::Writer W(v4::fmt::K_SETUP, v4::fmt::M_COMPAT);   // + the neighbour lists (WP2's sections)
    for (const auto& e : R.sections()) {
      const std::string nm(e.name);
      if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
      const void* q = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                    : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                    : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                    : (const void*)R.get<uint8_t>(nm);
      W.add_copy(nm, e.dtype, q, e.length, e.dims[0], e.dims[1]);
    }
    W.add("nb_ptr", nb.ptr); W.add("nb_idx", nb.idx); W.add("size_cum", st.size_cum); W.add("size_logmass", st.size_logmass); W.write(spath); }
  { Start st2 = load_start(spath, D); Neighbours nb2 = load_neighbours(spath, p);
    CHECK(st2.size_cum == st.size_cum && st2.logZbar0 == st.logZbar0 && st2.blocks == st.blocks && nb2.ptr == nb.ptr && nb2.idx == nb.idx); }
  // calibration (V)
  const std::string cpath = tg.add("of_calib.bin");
  { v4::Json a = v4::Json::object(); a["data"] = dpath; a["setup"] = spath; a["out"] = cpath; a["mode"] = "V"; a["seed"] = 77.0; a["threads"] = 3.0;
    v4::Json rec = v4::calib::run(a); CHECKF(rec.at("status").str() == "ok" || rec.at("status").str() == "completed", "calibrate: %s", rec.dump().c_str()); }
  v4::wp4io::SetupView SV = v4::wp4io::read_setup(spath, D.p, D.K, &D.zob);
  v4::wp4io::CalibIn C = v4::wp4io::read_calib(cpath, D.p, D.K);
  CHECK(C.meta.contains("tau_cal_hex"));
  const double tau = C.tau_cal;
  std::printf("  p = %d: %zu inherited models, c = %d, tau_cal = %.6f\n", p, C.inherited.size(), 40 * p + 1, tau);
  CHECKF(tau > NINF, "tau_cal is -inf (%zu inherited models < c = %d): the end-to-end floor test needs a finite floor", C.inherited.size(), 40 * p + 1);
  // a calib.bin whose tau_cal is not the c-th best F is refused by read_calib
  { v4::fmt::Reader R(cpath); v4::Json meta = R.json("meta"); v4::tau_cal_to_meta(meta, std::nextafter(tau, 0.0));
    v4::fmt::Writer W(v4::fmt::K_CALIB, R.mode());
    for (const auto& e : R.sections()) {
      const std::string nm(e.name); if (nm == "meta") continue;
      if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
      const void* q = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                    : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                    : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                    : (const void*)R.get<uint8_t>(nm);
      W.add_copy(nm, e.dtype, q, e.length, e.dims[0], e.dims[1]);
    }
    W.add_json("meta", meta); const std::string bad = tg.add("of_calib_badtau.bin"); W.write(bad);
    bool r = false; try { v4::wp4io::read_calib(bad, D.p, D.K); } catch (const v4::Error& e) { r = e.st == v4::Status::invalid_input; }
    CHECK(r); }
  // final islands (the island command's configuration): R' = 3, with and without the floor
  const Start stF = load_start(spath, D); const Neighbours nbF = load_neighbours(spath, D.p);
  const v4::calib::Budgets b = v4::calib::budgets(D.n, D.p);
  v4::Json inputs = v4::Json::object(); inputs["data.bin"] = dhash; inputs["setup.bin"] = SV.content_hash; inputs["calib.bin"] = C.content_hash;
  const int R = 3;
  std::vector<IslandRun> runs[2];
  std::vector<std::string> files[2];
  for (int fl = 0; fl < 2; ++fl) for (int r = 1; r <= R; ++r) {
    IslandConfig c; c.seed = 77; c.island = (uint32_t)r; c.N = C.N; c.grid = C.grid; c.L = C.L; c.Hm = C.Hm; c.B = b.B; c.tier = (uint32_t)C.tier;
    c.kernel = KernelKind::LabelMajor; c.threads = 3;
    if (fl) { const v4::OfferFloor of = v4::offer_floor_from_calib(C.meta, true, C.content_hash); c.offer_floor = of.f; c.offer_floor_calib = of.calib; }
    runs[fl].push_back(run_island<Arith::ClassA>(D, stF, nbF, c));
    CHECK(runs[fl].back().status == 0);
    files[fl].push_back(tg.add("of_island_" + std::to_string(fl) + "_" + std::to_string(r) + ".bin"));
    write_island_file(files[fl].back(), runs[fl].back(), Arith::ClassA, inputs);
  }
  uint64_t dropped = 0; for (auto& x : runs[1]) dropped += x.ks.store_floor_dropped;
  CHECKF(dropped > 0, "the floor dropped no offer (tau %.6f)", tau);
  auto merge = [&](const std::vector<std::string>& isl, const std::string& out) {
    v4::Json a = v4::Json::object(); a["data"] = dpath; a["setup"] = spath; a["calib"] = cpath; a["out"] = out; a["mode"] = "V";
    a["threads"] = 3.0; a["Rp"] = (double)isl.size(); v4::Json il = v4::Json::array(); for (auto& x : isl) il.push(x); a["islands"] = il;
    return v4::merge::run(a);
  };
  auto sections = [](const std::string& path) {
    v4::fmt::Reader Rd(path); std::map<std::string, std::string> m;
    for (auto& e : Rd.sections()) { if (std::string(e.name) == "meta") continue; std::string h; char x[3]; for (int i = 0; i < 32; ++i) { std::snprintf(x, 3, "%02x", e.sha256[i]); h += x; } m[e.name] = h; }
    return m;
  };
  const std::string o0 = tg.add("of_fit0.bin"), o1 = tg.add("of_fit1.bin");
  v4::Json m0 = merge(files[0], o0), m1 = merge(files[1], o1);
  CHECKF(m0.at("status").str() == "completed" && m1.at("status").str() == "completed", "merges: %s | %s", m0.dump().c_str(), m1.dump().c_str());
  auto h0 = sections(o0), h1 = sections(o1);
  CHECKF(h0 == h1 && !h0.empty(), "fit.bin sections differ with the floor (%zu vs %zu)", h0.size(), h1.size());
  CHECK(m0.at("logZ").dump() == m1.at("logZ").dump() && m0.at("hpm_F").dump() == m1.at("hpm_F").dump());
  std::printf("  floor %.6f dropped %llu offers over %d islands; fit.bin: %zu sections identical (HPM, log Z_r, PIPs, merged store, tail)\n",
              tau, (unsigned long long)dropped, R, h0.size());
  // refusals: each tampered island 2 -> invalid_input, no estimates (GUARD-W)
  auto refused_merge = [&](const char* what, IslandRun x) {
    std::vector<std::string> isl = files[1];
    isl[1] = tg.add(std::string("of_bad_") + what + ".bin");
    write_island_file(isl[1], x, Arith::ClassA, inputs);
    const std::string out = tg.add(std::string("of_fitbad_") + what + ".bin");
    v4::Json rec;
    try { rec = merge(isl, out); } catch (const v4::Error& e) { rec = v4::Json::object(); rec["status"] = v4::status_name(e.st); }
    const bool ok = rec.at("status").str() == "invalid_input" && !(rec.contains("estimates_available") && rec.at("estimates_available").boolean());
    CHECKF(ok, "%s: %s", what, rec.dump().c_str());
  };
  { IslandRun x = runs[1][1]; x.offer_floor_calib = "0xnot_this_calib"; refused_merge("calib", x); }
  { IslandRun x = runs[1][1]; x.offer_floor = std::nextafter(tau, -1e300); refused_merge("not_tau", x); }
  { IslandRun x = runs[1][1]; x.offer_floor = std::nan(""); refused_merge("nan", x); }
  { IslandRun x = runs[1][1]; x.offer_floor = __builtin_huge_val(); refused_merge("inf", x); }
  // review PR54 MINOR: a floored island whose meta.mode disagrees with its V container header is refused by the merge
  // (head_island), as is a finite floor under meta.mode = law
  auto rewrite_island_meta = [&](const std::string& src, const std::string& dst, const char* mode) {
    v4::fmt::Reader R(src); v4::fmt::Writer W(R.kind(), R.mode());
    v4::Json m = R.json("meta"); m["mode"] = mode; W.add_json("meta", m);
    for (const auto& e : R.sections()) {
      const std::string nm(e.name); if (nm == "meta") continue;
      if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
      const void* q = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                    : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                    : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                    : (const void*)R.get<uint8_t>(nm);
      W.add_copy(nm, e.dtype, q, e.length, e.dims[0], e.dims[1]);
    }
    W.write(dst);
  };
  for (const char* md : {"law", "compat"}) {
    std::vector<std::string> isl = files[1];
    isl[1] = tg.add(std::string("of_metamode_") + md + ".bin");
    rewrite_island_meta(files[1][1], isl[1], md);
    const std::string out = tg.add(std::string("of_fitmm_") + md + ".bin");
    v4::Json rec;
    try { rec = merge(isl, out); } catch (const v4::Error& e) { rec = v4::Json::object(); rec["status"] = v4::status_name(e.st); }
    CHECKF(rec.at("status").str() == "invalid_input" && !(rec.contains("estimates_available") && rec.at("estimates_available").boolean()),
           "meta.mode %s under a floor: %s", md, rec.dump().c_str());
  }
  // review PR54 MAJOR-2: read_calib's tau_cal is over DISTINCT inherited models whatever their order: the same models in
  // reverse (non-canonical) order are accepted with the same tau_cal; duplicates separated in the file are refused
  {
    auto with_models = [&](const std::string& dst, const std::vector<size_t>& pick) {
      std::vector<int64_t> ptr{0}; std::vector<int32_t> idx; std::vector<double> F, lg0, logm, d;
      for (size_t i : pick) { const auto& m = C.inherited[i]; idx.insert(idx.end(), m.S.begin(), m.S.end()); ptr.push_back((int64_t)idx.size());
        F.push_back(m.F); lg0.push_back(m.lg0); logm.push_back(m.logm); d.push_back(0.0); }
      v4::fmt::Reader R(cpath); v4::fmt::Writer W(R.kind(), R.mode());
      v4::Json m = R.json("meta"); v4::tau_cal_to_meta(m, v4::tau_cal_of(F, 40ull * (uint64_t)D.p + 1)); W.add_json("meta", m);
      for (const auto& e : R.sections()) {
        const std::string nm(e.name);
        if (nm == "meta" || nm == "inh_ptr" || nm == "inh_idx" || nm == "inh_F" || nm == "inh_lg0" || nm == "inh_logm" || nm == "inh_d") continue;
        if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
        const void* q = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                      : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                      : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                      : (const void*)R.get<uint8_t>(nm);
        W.add_copy(nm, e.dtype, q, e.length, e.dims[0], e.dims[1]);
      }
      W.add("inh_ptr", ptr); W.add("inh_idx", idx); W.add("inh_F", F); W.add("inh_lg0", lg0); W.add("inh_logm", logm);
      if (R.has("inh_d")) W.add("inh_d", d);
      W.write(dst);
    };
    const size_t ni = C.inherited.size();
    std::vector<size_t> rev, sep;
    for (size_t i = 0; i < ni; ++i) rev.push_back(ni - 1 - i);
    sep = rev; sep.push_back(0); sep.push_back(ni / 2); sep.push_back(0);   // models 0 and ni/2 repeated, apart from their first copies
    const std::string rv = tg.add("of_calib_rev.bin"), sp = tg.add("of_calib_sep.bin");
    with_models(rv, rev); with_models(sp, sep);
    v4::wp4io::CalibIn cr = v4::wp4io::read_calib(rv, D.p, D.K);
    CHECKF(v4::f64_hex(cr.tau_cal) == v4::f64_hex(tau), "reordered distinct models: tau_cal %.17g vs %.17g", cr.tau_cal, tau);
    bool refused = false; try { v4::wp4io::read_calib(sp, D.p, D.K); } catch (const v4::Error& e) { refused = e.st == v4::Status::invalid_input; }
    CHECK(refused);
  }
}
