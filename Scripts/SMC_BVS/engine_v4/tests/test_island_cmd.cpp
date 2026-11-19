// test_island_cmd.cpp -- `smcbvs4 island` (WP3; src/island/island_cmd.cpp, WP3_DESIGN §1.13) and the plans of
// `--plan-only` (island and calibrate; review PR39 MAJOR-2), through the built binary and in process:
//   * island_command_end_to_end: data.bin + setup.bin -> `calibrate` -> `island` r = 1..4 -> `merge`, per mode (compat,
//     law, V); the island file equals run_island with calib.bin's settings (output hash); V: the file's non-meta section
//     hashes are the same for 1 and 3 threads and G 7 (T3 through the CLI); the merge accepts the islands.
//   * island_command_driver_manifest: the WP5 driver's dry run -> island.json template -> p1m_manifest.py fill
//     --set params.id=R -> `island --manifest ... --threads --mem-budget --out` (the driver's command line); equal to the
//     explicit form; manifest authority (a disagreeing argument is refused).
//   * island_command_refusals_and_budget: invalid_input (exit 13) cases; --mem-budget below the plan: exit 11 and an
//     island file with status resource_limit and no estimates; --plan-only (files and sizes) admits at the plan and
//     refuses one byte below; calibrate --plan-only reports the calibration island's plan and the run refuses one
//     byte below it (N-1, MINOR-1).
//   * island_command_resume: a checkpoint written by an interrupted island is resumed by the command (same output hash),
//     and the checkpoint files are removed after the completed write.
//   * plan_from_sizes_equals_plan_island: plan_sizes + plan_with_budget = plan_island.
//   * v_mode_N_parameter (V-N mini-leg, exp/P1M-VN): V's final-island N is a calibrate parameter (manifest params.N / --N, default
//     2,500): plumbing (calib.bin, record, island, merge), default = 2,500 bit-identical, N = 10^4 accepted and run end to end,
//     invalid N refused as T's island N is, T mode untouched, the memory plans scale with N. With V4_F_SMCBVS4 = the frozen F
//     binary, the default-N calib.bin and island files of the fixture are also compared section by section with F's.
#include <omp.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <cstdio>
#include <filesystem>
#include <fstream>
#include <functional>
#include <random>
#include <set>
#include "tk.h"
#include "tutil.h"
#include "tutil_island.h"
#include "v4/calib_run.h"
#include "v4/island/island.h"
#include "v4/island/island_file.h"
#include "v4/island/setup_load.h"
#include "v4/merge.h"
#include "v4/offer_floor.h"
#include "v4/format.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/score.h"
#include "v4/sha256.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"

using namespace v4::island;
using v4::Json;

namespace {
std::string q(const std::string& s) { return "'" + s + "'"; }
int sh(const std::string& c, const std::string& log = "/dev/null") {
  const int rc = std::system((c + " > " + q(log) + " 2>&1").c_str());
  return WIFEXITED(rc) ? WEXITSTATUS(rc) : -1;
}
struct Dir {   // a fresh directory under $TMPDIR, removed at the end
  std::string d;
  explicit Dir(const std::string& tag) {
    const char* t = std::getenv("TMPDIR");
    if (!t || !*t) throw std::runtime_error("TMPDIR is not set: the island command tests write only under $TMPDIR");
    d = tmp_path("wp3cmd_" + tag); std::error_code ec; std::filesystem::remove_all(d, ec); std::filesystem::create_directories(d);
  }
  std::string operator()(const std::string& n) const { return d + "/" + n; }
  ~Dir() { std::error_code ec; std::filesystem::remove_all(d, ec); }
};
// non-meta section hashes of an engine file (T2 / T3: content hashes include meta, which holds timings)
std::string body_hash(const std::string& path) {
  v4::fmt::Reader R(path); std::string s;
  for (auto& e : R.sections()) if (std::string(e.name) != "meta") s += std::string(e.name) + ":" + v4::hex(e.sha256, 32) + ";";
  return s;
}
Json rec_of(const std::string& p) { return v4::read_json_file(p); }

// data.bin (prep of an AR(0.6) design, n 60, p 30) and setup.bin (blocks of 3, the island's own tables, table stores over
// every table model, neighbour lists, size_cum): the fixture of calibrate_command_end_to_end
struct Fx { v4::Data D; std::string dpath, spath, dhash, shash; };
// copies every section of R into W except `skip` (json sections as json; the rest as raw bytes of their dtype)
void copy_sections(const v4::fmt::Reader& R, v4::fmt::Writer& W, const std::set<std::string>& skip = {}) {
  for (const auto& e : R.sections()) {
    const std::string nm(e.name);
    if (skip.count(nm)) continue;
    if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
    const void* qq = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                   : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                   : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                   : (const void*)R.get<uint8_t>(nm);
    W.add_copy(nm, e.dtype, qq, e.length, e.dims[0], e.dims[1]);
  }
}
// a setup.bin like `src` with other sections (the replaced names are dropped from the copy); returns the new content hash
std::string rewrite_setup(const std::string& src, const std::string& dst, const std::set<std::string>& drop, const std::function<void(v4::fmt::Writer&)>& add) {
  v4::fmt::Reader R(src); v4::fmt::Writer W(v4::fmt::K_SETUP, R.mode());
  copy_sections(R, W, drop); add(W);
  return W.write(dst);
}
// a calib.bin like `src` whose meta.inputs["setup.bin"] names `shash` (every normal input check of the island passes)
std::string rewrite_calib_inputs(const std::string& src, const std::string& dst, const std::string& shash) {
  v4::fmt::Reader R(src); v4::fmt::Writer W(R.kind(), R.mode());
  Json m = R.json("meta"); m["inputs"]["setup.bin"] = shash;
  W.add_json("meta", m); copy_sections(R, W, {"meta"});
  return W.write(dst);
}
void make_fx(Fx& f, const Dir& dir, int bsz = 3) {
  const int n = 60, p_raw = 30;
  std::vector<double> X((size_t)n * p_raw), y(n);
  { std::mt19937_64 g(41); std::normal_distribution<double> nd;
    for (int i = 0; i < n; ++i) { double prev = 0; for (int j = 0; j < p_raw; ++j) { double x = 0.6 * prev + 0.8 * nd(g); X[(size_t)j * n + i] = x; prev = x; } }
    for (int i = 0; i < n; ++i) y[i] = 1.2 * X[(size_t)2 * n + i] - 0.9 * X[(size_t)11 * n + i] + nd(g); }
  v4::prep::Result pr = v4::prep::preprocess(X.data(), y.data(), n, p_raw);
  f.D = v4::make_data(pr.own, n, pr.p);
  const v4::Data& D = f.D; const int p = D.p;
  f.dpath = dir("data.bin"); f.spath = dir("setup.bin");
  f.dhash = v4::prep::write_data(f.dpath, D, pr, "B", Json::object());
  Start st; build_start(st, D, contiguous_blocks(p, bsz));
  Neighbours nb = window_neighbours(D, 6, 4);
  v4::wp4io::SetupView S; S.blk = st.blk; S.pos = st.pos; S.blk_ptr.push_back(0);
  S.ttop.init(40ull * p + 1, v4::Order::HPM); S.tlead0.init(20ull * p, v4::Order::LEX); S.tlead1.init(20ull * p, v4::Order::LEX);
  v4::BitScorer sc(&D);
  for (int b = 0; b < st.J; ++b) {
    for (int j : st.blocks[b]) S.blk_members.push_back(j);
    S.blk_ptr.push_back((int64_t)S.blk_members.size()); S.code_ptr.push_back((int64_t)S.logr.size());
    for (uint32_t c = 0; c < st.logr[b].size(); ++c) {
      S.logr.push_back(st.logr[b][c]);
      v4::Model U; for (size_t i = 0; i < st.blocks[b].size(); ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
      if ((int)U.size() > D.K) continue;
      double F = D.logprior[U.size()] + sc.score(U).logm, lg0 = D.logprior[U.size()] + st.logr[b][c];
      S.ttop.offer(F, U, D.zob.hash(U)); S.tlead0.offer(lg0, U, D.zob.hash(U)); S.tlead1.offer(F, U, D.zob.hash(U));
    }
  }
  S.code_ptr.push_back((int64_t)S.logr.size());   // J + 1 entries; code_ptr[J] = |logr| (INTERFACES v0.1.19 §2/§5)
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  S.mode_S = v4::Model(S.ttop.model(0).begin(), S.ttop.model(0).end());
  Json sin = Json::object(); sin["data.bin"] = f.dhash;
  const std::string s0 = dir("setup0.bin");
  v4::wp4io::write_setup_min(s0, S, sin);
  { v4::fmt::Reader R(s0); v4::fmt::Writer W(v4::fmt::K_SETUP, v4::fmt::M_COMPAT);   // + the neighbour lists (WP2's sections)
    copy_sections(R, W);
    // + size_logmass (WP4 #46: calibrate's plan k = max(8, q90(pi_0 size) + 1) from setup.bin requires it)
    W.add("nb_ptr", nb.ptr); W.add("nb_idx", nb.idx); W.add("size_cum", st.size_cum); W.add("size_logmass", st.size_logmass); f.shash = W.write(f.spath); }
  std::remove(s0.c_str());
  // the producers' records (the driver's fill requires "completed")
  Json ok = Json::object(); ok["status"] = "completed";
  v4::write_json_file(f.dpath + ".json", ok); v4::write_json_file(f.spath + ".json", ok);
}
}  // namespace

TEST(island_command_end_to_end) {
  Dir dir("e2e"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4;
  for (const std::string mode : {"V", "law", "compat"}) {
    const int Rp = mode == "V" ? 4 : 2;
    const std::string cal = dir("calib_" + mode + ".bin");
    const int th = mode == "compat" ? 1 : 3;
    const int rc_cal = sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode " + mode + " --seed 77 --threads " + std::to_string(th) + " --out " + q(cal));
    CHECKF(rc_cal == 0, "%s: calibrate exit %d (record status %s)", mode.c_str(), rc_cal, rec_of(cal + ".json").at("status").str().c_str());
    if (rc_cal != 0) continue;
    CHECK(rec_of(cal + ".json").at("status").str() == "completed" && rec_of(cal + ".json").at("cal_status").str() == "ok");
    const v4::wp4io::CalibIn ci = v4::wp4io::read_calib(cal, f.D.p, f.D.K, f.dhash, f.shash);
    std::string isl;
    for (int r = 1; r <= Rp; ++r) {
      const std::string out = dir("island_" + mode + "_" + std::to_string(r) + ".bin");
      const double t0 = omp_get_wtime();
      const int rc = sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode " + mode + " --seed 77 --island " +
                        std::to_string(r) + " --Rp " + std::to_string(Rp) + " --threads " + std::to_string(th) + " --out " + q(out));
      const Json rec = rec_of(out + ".json");
      CHECKF(rc == 0 && rec.at("status").str() == "completed", "%s island %d: exit %d status %s", mode.c_str(), r, rc, rec.at("status").str().c_str());
      isl += (r > 1 ? "," : "") + out;
      if (r > 2) continue;
      // the file: meta.inputs = the three content hashes; calib's grid, N, L, Hm; GUARD-W estimates present
      const IslandFile F = read_island_file(out);
      CHECK(F.meta.at("inputs").at("data.bin").str() == f.dhash && F.meta.at("inputs").at("setup.bin").str() == f.shash &&
            F.meta.at("inputs").at("calib.bin").str() == ci.content_hash);
      CHECK(F.grid == ci.grid && F.rec.N == ci.N && F.rec.L == ci.L && F.rec.Hm == ci.Hm && F.rec.r == r && (int)F.terminal.size() == ci.N);
      // = run_island with calib.bin's settings (the command adds nothing to the law)
      Start st = load_start(f.spath, f.D); Neighbours nb = load_neighbours(f.spath, f.D.p);
      IslandConfig c; c.seed = 77; c.island = (uint32_t)r; c.tier = (uint32_t)ci.tier; c.N = ci.N; c.grid = ci.grid; c.L = ci.L; c.Hm = ci.Hm;
      c.compat = mode == "compat"; c.threads = th; c.kernel = mode == "V" ? KernelKind::LabelMajor : KernelKind::ParticleMajor;
      // B is part of the law: min(isqrt n, isqrt p, 16) = min(7, 5, 16) = 5 for this n = 60, p = 30 fixture (review PR52 MAJOR-3);
      // the reference sets it by value, not from the CLI default (14, which is right only for n = 200)
      CHECK(f.D.n == 60 && f.D.p == 30 && v4::calib::budgets(f.D.n, f.D.p).B == 5);
      c.B = 5;
      // D-29 (WP7 O6): the command gives a V final island calib.bin's tau_cal as its offer floor (-inf in other modes)
      { const v4::OfferFloor of = v4::offer_floor_from_calib(ci.meta, mode == "V", ci.content_hash); c.offer_floor = of.f; c.offer_floor_calib = of.calib; }
      const IslandRun ref = mode == "V" ? run_island<Arith::ClassA>(f.D, st, nb, c) : run_island<Arith::Bit>(f.D, st, nb, c);
      char hx[19]; std::snprintf(hx, sizeof hx, "0x%016llx", (unsigned long long)ref.hash());
      CHECKF(rec.at("output_hash").str() == hx, "%s island %d: CLI output hash %s, run_island (B 5) %s", mode.c_str(), r, rec.at("output_hash").str().c_str(), hx);
      CHECK((int)rec.at("B").num() == 5);
      if (mode == "V" && r == 1) {   // the wrong B gives other output: the test above would fail on a hard-coded 14
        IslandConfig c14 = c; c14.B = 14;
        const IslandRun w = run_island<Arith::ClassA>(f.D, st, nb, c14);
        CHECK(w.hash() != ref.hash());
      }
      std::printf("  %-6s island %d: %.2f s, T = %zu, N = %d, logZ = %.6f, G %d\n", mode.c_str(), r, omp_get_wtime() - t0, ci.grid.size() - 1, ci.N,
                  rec.at("logZ").num(), (int)rec.at("G_used").num());
      if (mode == "V" && r == 2) {   // T3 through the CLI: 1 thread, G 7, tile 64 -> the same sections
        const std::string o1 = dir("island_V_2_t1.bin");
        CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode V --seed 77 --island 2 --threads 1 --G 7 --tile 64 --out " + q(o1)), 0);
        CHECK(body_hash(o1) == body_hash(out));
      }
    }
    // a refused island carries the request's identity (review PR52 m6): mode, schedule, no estimates; and --B is checked
    { const std::string ro = dir("island_" + mode + "_refused.bin");
      CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode " + mode + " --seed 77 --island 1 --threads " +
                  std::to_string(th) + " --mem-budget 1 --out " + q(ro)), 11);
      v4::fmt::Reader R(ro); const Json m = R.json("meta");
      CHECKF(m.at("status").str() == "resource_limit" && m.at("mode").str() == mode && R.mode() == v4::fmt::mode_from_name(mode) &&
             R.vec<double>("grid") == ci.grid && (size_t)m.at("T").num() + 1 == ci.grid.size() && !R.has("logZ") && !R.has("pip_r") && !R.has("terminal_S"),
             "%s refusal file: status %s mode %s header mode %s", mode.c_str(), m.at("status").str().c_str(), m.at("mode").str().c_str(), v4::fmt::mode_name(R.mode()).c_str());
      const std::string base = bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode " + mode + " --seed 77 --island 1 --plan-only 1";
      CHECK_EQ(sh(base + " --B 14"), 13);   // conflicts with min(isqrt n, isqrt p, 16) = 5
      CHECK_EQ(sh(base + " --B 5"), 0); }
    // WP4's merge takes the islands
    const std::string fit = dir("fit_" + mode + ".bin");
    const int rcm = sh(bin + " merge --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --islands " + q(isl) + " --Rp " +
                       std::to_string(Rp) + " --mode " + mode + " --threads 2 --out " + q(fit));
    // theory-mode merges need equal, clean, known git commits (provenance.h MergeTheory): a -dirty build is refused
    const std::string commit = v4::binary_block_no_self_test().at("git_commit").str();
    const bool clean = mode == "V" || (commit.size() == 40 && commit.find("dirty") == std::string::npos);
    if (!clean) {
      CHECKF(rcm == 13, "%s: merge of a -dirty build: exit %d (expected the clean-commit refusal, 13)", mode.c_str(), rcm);
      std::printf("  %-6s merge: refused as expected (binary %s is not a clean commit); rerun from a clean tree to merge\n", mode.c_str(), commit.c_str());
      continue;
    }
    CHECKF(rcm == 0, "%s: merge exit %d", mode.c_str(), rcm);
    if (rcm == 0) { v4::fmt::Reader R(fit); Json m = R.json("meta");
      CHECK(m.at("status").str() == "completed" && (int)m.at("Rp").num() == Rp && std::isfinite(m.at("logZ").num()));
      std::printf("  %-6s merge: logZ = %.6f\n", mode.c_str(), m.at("logZ").num()); }
  }
}

// D-29 (WP7 O6) through the CLI: V islands take calib.bin's tau_cal as their offer floor (island_r.bin meta), --offer-floor 0
// runs without it; every science section of the island files except the store (top_*) is identical, the floored store
// is the unfloored store's prefix v >= floor, and the merged fit.bin is identical section by section.
TEST(island_command_offer_floor_on_off) {
  Dir dir("floor"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4, cal = dir("calib.bin");
  CHECK_EQ(sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --threads 3 --out " + q(cal)), 0);
  const v4::wp4io::CalibIn ci = v4::wp4io::read_calib(cal, f.D.p, f.D.K, f.dhash, f.shash);
  CHECKF(std::isfinite(ci.tau_cal), "tau_cal %g (the fixture needs a finite floor)", ci.tau_cal);
  const int Rp = 3;
  std::string isl[2];
  for (int on = 0; on < 2; ++on) for (int r = 1; r <= Rp; ++r) {
    const std::string out = dir("isl_" + std::to_string(on) + "_" + std::to_string(r) + ".bin");
    CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode V --seed 77 --island " + std::to_string(r) +
                " --threads 3 --offer-floor " + std::to_string(on) + " --out " + q(out)), 0);
    isl[on] += (r > 1 ? "," : "") + out;
    const IslandFile F = read_island_file(out);
    if (on) CHECK(v4::f64_hex(F.offer_floor) == v4::f64_hex(ci.tau_cal) && F.offer_floor_calib == ci.content_hash);
    else CHECK(std::isinf(F.offer_floor) && F.offer_floor < 0 && F.meta.at("offer_floor_calib").is_null());
  }
  for (int r = 1; r <= Rp; ++r) {   // science sections equal; the store = the unfloored prefix v >= floor
    const std::string a = dir("isl_0_" + std::to_string(r) + ".bin"), b = dir("isl_1_" + std::to_string(r) + ".bin");
    v4::fmt::Reader Ra(a), Rb(b); bool same = true;
    for (auto& e : Ra.sections()) {
      const std::string nm(e.name);
      if (nm == "meta" || nm.rfind("top_", 0) == 0) continue;
      bool found = false; for (auto& g : Rb.sections()) if (std::string(g.name) == nm) { found = true; same = same && std::memcmp(e.sha256, g.sha256, 32) == 0; }
      same = same && found;
    }
    const IslandFile Fa = read_island_file(a), Fb = read_island_file(b);
    const v4::Store &sa = Fa.rec.led.top, &sb = Fb.rec.led.top;
    size_t want = 0; while (want < sa.size() && sa.v[want] >= ci.tau_cal) ++want;
    bool sto = sb.size() == want;
    for (size_t i = 0; sto && i < want; ++i) sto = v4::f64_hex(sb.v[i]) == v4::f64_hex(sa.v[i]) && v4::same_model(sb.model(i), sa.model(i));
    CHECKF(same && sto, "island %d: science sections equal %d, store %zu vs %zu above the floor", r, (int)same, sb.size(), want);
  }
  std::string fit[2];
  for (int on = 0; on < 2; ++on) {
    fit[on] = dir("fit_" + std::to_string(on) + ".bin");
    CHECK_EQ(sh(bin + " merge --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --islands " + q(isl[on]) + " --Rp " +
                std::to_string(Rp) + " --mode V --threads 2 --out " + q(fit[on])), 0);
  }
  CHECK(body_hash(fit[0]) == body_hash(fit[1]) && !body_hash(fit[0]).empty());
  std::printf("  tau_cal %.6f: islands floored through the CLI; fit.bin identical with and without the floor\n", ci.tau_cal);
}

// WP7 O4: `island --stop-after-s S` is a soft stop: exit 22, record island_status = interrupted_resumable, no island file,
// the checkpoint left; the rerun resumes. A chain of stops ends with the uninterrupted island's sections; invalid
// values (S <= 0, S without checkpoints) are refused (13).
TEST(island_command_time_stop_chain) {
  Dir dir("tstop"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4, cal = dir("calib.bin");
  CHECK_EQ(sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --threads 3 --out " + q(cal)), 0);
  const std::string base = bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode V --seed 77 --island 1 --threads 3 ";
  const std::string ref = dir("ref.bin"), out = dir("island_1.bin");
  CHECK_EQ(sh(base + "--out " + q(ref)), 0);
  struct stat sb{};
  int attempts = 0, stops = 0, rc = -1; int last = -1;
  while (attempts < 30) {
    rc = sh(base + "--stop-after-s 0.4 --out " + q(out)); ++attempts;
    if (rc == 0) break;
    CHECKF(rc == 22, "attempt %d: exit %d", attempts, rc);
    const Json rec = rec_of(out + ".json");
    CHECK(rec.at("status").str() == "completed" && rec.at("island_status").str() == "interrupted_resumable" && !rec.contains("island_bin"));
    CHECK(::stat(out.c_str(), &sb) != 0);   // no island file yet
    CHECK(::stat((dir("island_1.ckpt.a")).c_str(), &sb) == 0 || ::stat((dir("island_1.ckpt.b")).c_str(), &sb) == 0);
    const int after = (int)rec.at("stopped_after_step").num(); CHECKF(after > last, "attempt %d stopped after step %d (last %d)", attempts, after, last); last = after;
    ++stops;
  }
  CHECKF(rc == 0 && stops >= 2, "exit %d after %d attempts (%d stops)", rc, attempts, stops);
  CHECK(body_hash(out) == body_hash(ref));
  CHECK(rec_of(out + ".json").at("resumed_from_step").num() == last);
  CHECK(::stat(dir("island_1.ckpt.a").c_str(), &sb) != 0 && ::stat(dir("island_1.ckpt.b").c_str(), &sb) != 0);   // removed after the completed write
  CHECK_EQ(sh(base + "--stop-after-s 0 --out " + q(dir("bad0.bin"))), 13);
  CHECK_EQ(sh(base + "--stop-after-s 5 --ckpt 0 --out " + q(dir("bad1.bin"))), 13);
  std::printf("  island command: %d attempts (%d soft stops, exit 22) -> the uninterrupted island's sections\n", attempts, stops);
}

// D-29 (review PR54 MAJOR-1/2): the island command validates tau_cal itself, before any island work, with the check
// read_calib uses: a tampered finite tau_cal (next ulp, or far above every value) and inherited models that are not
// distinct (one model repeated; two models alternating) are refused (13, no island file); the valid calib.bin runs.
TEST(island_command_refuses_tampered_tau_cal) {
  Dir dir("tau"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4, cal = dir("calib.bin");
  CHECK_EQ(sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --threads 3 --out " + q(cal)), 0);
  const v4::wp4io::CalibIn ci = v4::wp4io::read_calib(cal, f.D.p, f.D.K, f.dhash, f.shash);
  CHECK(std::isfinite(ci.tau_cal) && ci.inherited.size() > (size_t)(40 * f.D.p + 1));
  auto island = [&](const std::string& calf, const std::string& out) {
    return sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(calf) + " --mode V --seed 77 --island 1 --threads 3 --out " + q(out));
  };
  struct stat sb{};
  { const std::string out = dir("ok.bin"); CHECK_EQ(island(cal, out), 0); }   // the control: the valid calib.bin runs
  auto with_tau = [&](const std::string& dst, double tau) {   // the same calib.bin with another finite tau_cal
    v4::fmt::Reader R(cal); v4::fmt::Writer W(R.kind(), R.mode());
    Json m = R.json("meta"); v4::tau_cal_to_meta(m, tau); W.add_json("meta", m); copy_sections(R, W, {"meta"}); W.write(dst);
  };
  const std::string t1 = dir("calib_ulp.bin"), t2 = dir("calib_big.bin");
  with_tau(t1, std::nextafter(ci.tau_cal, 0.0)); with_tau(t2, 1e6);
  for (const std::string& c : {t1, t2}) {
    const std::string out = dir("bad_" + c.substr(c.rfind('/') + 1));
    CHECK_EQ(island(c, out), 13); CHECK(::stat(out.c_str(), &sb) != 0);
  }
  // inherited models that are not distinct, with matching repeated values and the tau_cal the row count would give
  auto with_models = [&](const std::string& dst, const std::vector<size_t>& pick) {
    std::vector<int64_t> ptr{0}; std::vector<int32_t> idx; std::vector<double> F, lg0, logm, d;
    for (size_t i : pick) { const auto& m = ci.inherited[i]; idx.insert(idx.end(), m.S.begin(), m.S.end()); ptr.push_back((int64_t)idx.size());
      F.push_back(m.F); lg0.push_back(m.lg0); logm.push_back(m.logm); d.push_back(0.0); }
    v4::fmt::Reader R(cal); v4::fmt::Writer W(R.kind(), R.mode());
    Json m = R.json("meta"); v4::tau_cal_to_meta(m, v4::tau_cal_of(F, 40ull * (uint64_t)f.D.p + 1)); W.add_json("meta", m);
    copy_sections(R, W, {"meta", "inh_ptr", "inh_idx", "inh_F", "inh_lg0", "inh_logm", "inh_d"});
    W.add("inh_ptr", ptr); W.add("inh_idx", idx); W.add("inh_F", F); W.add("inh_lg0", lg0); W.add("inh_logm", logm); if (R.has("inh_d")) W.add("inh_d", d);
    W.write(dst);
  };
  const size_t n = ci.inherited.size();
  std::vector<size_t> one(n, 0), alt; for (size_t i = 0; i < n; ++i) alt.push_back(i % 2);
  const std::string d1 = dir("calib_one.bin"), d2 = dir("calib_alt.bin");
  with_models(d1, one); with_models(d2, alt);
  for (const std::string& c : {d1, d2}) {
    const std::string out = dir("bad_" + c.substr(c.rfind('/') + 1));
    CHECK_EQ(island(c, out), 13); CHECK(::stat(out.c_str(), &sb) != 0);
    bool refused = false; try { v4::wp4io::read_calib(c, f.D.p, f.D.K); } catch (const v4::Error& e) { refused = e.st == v4::Status::invalid_input; }
    CHECK(refused);   // read_calib and the command agree
  }
}

// D-32 (review PR55 m3): a V island refuses a calib.bin written by a binary of the other class-A FMA family
TEST(island_command_refuses_other_fma_family_calib) {
  Dir dir("isa"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4, cal = dir("calib.bin"), cal2 = dir("calib_other.bin");
  CHECK_EQ(sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --threads 3 --out " + q(cal)), 0);
  { v4::fmt::Reader R(cal); v4::fmt::Writer W(R.kind(), R.mode());
    Json m = R.json("meta"); const bool fma = m.at("binary").contains("island_fma") && m.at("binary").at("island_fma").boolean();
    m["binary"]["island_fma"] = !fma; m["binary"]["island_isa"] = fma ? "portable" : "x86-64-v3";
    W.add_json("meta", m); copy_sections(R, W, {"meta"}); W.write(cal2); }
  const std::string base = bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --island 1 --threads 3 --plan-only 1 --calib ";
  CHECK_EQ(sh(base + q(cal)), 0);
  CHECK_EQ(sh(base + q(cal2)), 13);
}

TEST(island_command_driver_manifest) {
  Dir dir("drv"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4, tools = std::string(V4_FIXTURE_DIR) + "/../../tools/slurm";
  if (sh("command -v python3") != 0) { std::printf("    python3 not found: NOT RUN\n"); return; }
  // the driver's dry run of the example plan (mode V, R' 16, seed 1 for its first fit)
  const std::string drv = dir("drv"), dept = dir("dept");
  CHECK_EQ(sh("python3 " + q(tools + "/p1m_driver.py") + " --plan " + q(tools + "/examples/plan_A2_pilot_1e4.json") + " --out " + q(drv) +
              " --dept " + q(dept) + " --now 2026-11-16T00:00:00Z"), 0);
  const std::string mdir = drv + "/manifests/A2_ARs_n200_r1";
  Json T = v4::read_json_file(mdir + "/island.json");
  CHECK(T.at("command").str() == "island" && T.at("mode").str() == "V" && T.at("inputs").size() == 3 && (int)T.at("params").at("seed").num() == 1);
  std::string rundir;
  for (auto& [k, v] : T.at("inputs").items()) {
    const std::string b = k.substr(k.find_last_of('/') + 1); rundir = k.substr(0, k.find_last_of('/'));
    if (b == "calib.bin") continue;   // produced below by the calibrate stage
    const std::string src = b == "data.bin" ? f.dpath : f.spath;
    sh("mkdir -p " + q(rundir) + " && cp " + q(src) + " " + q(k) + " && cp " + q(src + ".json") + " " + q(k + ".json"));
  }
  // the driver's calibrate stage: fill, then `calibrate --manifest ... --threads --mem-budget --out` (inputs from the manifest)
  const std::string cman = dir("calibrate.json"), cal = rundir + "/calib.bin";
  CHECK_EQ(sh("BIN=" + q(bin) + " python3 " + q(tools + "/p1m_manifest.py") + " fill --template " + q(mdir + "/calibrate.json") + " --out " + q(cman) + " --bin " + q(bin)), 0);
  CHECK_EQ(sh(bin + " calibrate --manifest " + q(cman) + " --threads 3 --mem-budget " + std::to_string(8ull << 30) + " --out " + q(cal), dir("drv_cal.log")), 0);
  CHECK(rec_of(cal + ".json").at("status").str() == "completed");
  CHECK_EQ(sh(bin + " calibrate --manifest " + q(cman) + " --data " + q(f.spath) + " --out " + q(dir("c_a.bin"))), 13);   // disagreeing input
  CHECK_EQ(sh(bin + " calibrate --manifest " + q(cman) + " --mode law --out " + q(dir("c_b.bin"))), 13);                 // disagreeing mode
  { const std::string cal2 = dir("calib_explicit.bin");   // = the explicit form
    CHECK_EQ(sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 1 --threads 3 --out " + q(cal2)), 0);
    CHECK(body_hash(cal2) == body_hash(cal)); }
  const std::string tmpl = mdir + "/island.json";
  // the driver's islands stage: fill with params.id = R, then the command line of stage_body("islands")
  const std::string man = dir("island_3.json"), out = rundir + "/island_3.bin";
  CHECK_EQ(sh("BIN=" + q(bin) + " python3 " + q(tools + "/p1m_manifest.py") + " fill --template " + q(tmpl) + " --out " + q(man) + " --bin " + q(bin) +
              " --set params.id=3"), 0);
  const uint64_t memb = 8ull << 30;
  const int rc = sh(bin + " island --manifest " + q(man) + " --threads 2 --mem-budget " + std::to_string(memb) + " --out " + q(out), dir("drv_island.log"));
  CHECKF(rc == 0, "driver form: exit %d", rc);
  const Json rec = rec_of(out + ".json");
  CHECK(rec.at("status").str() == "completed" && (int)rec.at("r").num() == 3 && rec.at("mem_plan").at("admitted").boolean());
  // = the explicit form (r 3, seed 1, 3 threads)
  const std::string ex = dir("island_3_explicit.bin");
  CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode V --seed 1 --island 3 --threads 3 --out " + q(ex)), 0);
  CHECK(body_hash(ex) == body_hash(out));
  // manifest authority: a disagreeing island index, mode, seed or input path is refused; agreeing ones are accepted
  CHECK_EQ(sh(bin + " island --manifest " + q(man) + " --island 4 --out " + q(dir("m_a.bin"))), 13);
  CHECK_EQ(sh(bin + " island --island 4 --manifest " + q(man) + " --out " + q(dir("m_b.bin"))), 13);
  CHECK_EQ(sh(bin + " island --manifest " + q(man) + " --mode law --out " + q(dir("m_c.bin"))), 13);
  CHECK_EQ(sh(bin + " island --manifest " + q(man) + " --seed 2 --out " + q(dir("m_d.bin"))), 13);
  CHECK_EQ(sh(bin + " island --manifest " + q(man) + " --data " + q(f.dpath) + " --out " + q(dir("m_e.bin"))), 13);
  CHECK_EQ(sh(bin + " island --manifest " + q(man) + " --id 3 --threads 2 --out " + q(dir("m_f.bin"))), 0);
  // the same keys BEFORE --manifest (review PR52 MAJOR-4: main copies the manifest's params over an earlier explicit value):
  // the manifest has id 3, seed 1, Rp 16
  for (const char* conflict : {"--seed 2", "--id 4", "--Rp 8", "--island 4"})
    CHECK_MSG(sh(bin + " island " + conflict + " --manifest " + q(man) + " --plan-only 1") == 13, std::string("before the manifest: ") + conflict);
  for (const char* conflict : {"--seed 2", "--id 4", "--Rp 8", "--island 4"})
    CHECK_MSG(sh(bin + " island --manifest " + q(man) + " " + conflict + " --plan-only 1") == 13, std::string("after the manifest: ") + conflict);
  CHECK_EQ(sh(bin + " island --id 3 --seed 1 --manifest " + q(man) + " --plan-only 1"), 0);   // agreeing values, before the manifest
  // calibrate: the manifest freezes the seed (and I_max / refine_m); a conflicting explicit seed is refused on either side
  CHECK_EQ(sh(bin + " calibrate --seed 2 --manifest " + q(cman) + " --plan-only 1"), 13);
  CHECK_EQ(sh(bin + " calibrate --manifest " + q(cman) + " --seed 2 --plan-only 1"), 13);
  CHECK_EQ(sh(bin + " calibrate --seed 1 --manifest " + q(cman) + " --plan-only 1"), 0);
  // a manifest of another command is refused
  { Json M = v4::read_json_file(man); M["command"] = "merge"; v4::write_json_file(dir("m_merge.json"), M); }
  CHECK_EQ(sh(bin + " island --manifest " + q(dir("m_merge.json")) + " --out " + q(dir("m_g.bin"))), 13);
}

TEST(island_command_refusals_and_budget) {
  Dir dir("ref"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4;
  const std::string cal = dir("calib.bin");
  CHECK_EQ(sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --threads 3 --out " + q(cal)), 0);
  const std::string base = bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --threads 2";
  const std::string ok = base + " --mode V --seed 77 --island 1";
  auto o = [&](const std::string& n) { return " --out " + q(dir(n)); };
  // invalid_input (exit 13)
  CHECK_EQ(sh(base + " --mode law --seed 77 --island 1" + o("r1.bin")), 13);          // calib.bin is V
  CHECK_EQ(sh(base + " --mode V --seed 5 --island 1" + o("r2.bin")), 13);             // another seed than the calibration's
  CHECK_EQ(sh(base + " --mode V --island 1" + o("r3.bin")), 13);                      // no seed
  CHECK_EQ(sh(base + " --mode V --seed 77" + o("r4.bin")), 13);                       // no island index
  CHECK_EQ(sh(base + " --mode V --seed 77 --island 0" + o("r5.bin")), 13);            // r >= 1
  CHECK_EQ(sh(base + " --mode V --seed 77 --island 5 --Rp 4" + o("r6.bin")), 13);     // r <= R'
  CHECK_EQ(sh(base + " --mode V --seed 77 --island 1.5" + o("r7.bin")), 13);
  CHECK_EQ(sh(ok), 13);                                                               // no --out
  CHECK_EQ(sh(ok + " --role pilot" + o("r8.bin")), 13);                               // calibration roles run inside calibrate
  CHECK_EQ(sh(ok + " --N 100" + o("r9.bin")), 13);                                    // N differs from calib.bin's
  CHECK_EQ(sh(ok + " --G 300" + o("r10.bin")), 13);
  for (const char* b : {"-5", "1e30", "1.5", "nan"}) CHECK_MSG(sh(ok + " --mem-budget " + b + o("r11.bin")) == 13, std::string("--mem-budget ") + b);
  CHECK_EQ(sh(ok + " --mem-budget 1000 --mem-budget-gb 1" + o("r12.bin")), 13);
  CHECK(sh(base + " --mode V --seed 77 --island 1 --data " + q(dir("missing.bin")) + o("r13.bin")) != 0);   // no data.bin
  CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(f.spath) + " --mode V --seed 77 --island 1" + o("r14.bin")), 13);   // not a calib file
  // --plan-only with the files: admitted at the plan, refused one byte below (fixed G: the plan does not shrink)
  const std::string pr = dir("plan.json");
  CHECK_EQ(sh(ok + " --G 16 --plan-only 1 --record " + q(pr)), 0);
  const Json P = rec_of(pr);
  const uint64_t plan = (uint64_t)P.at("mem_plan").at("total").num();
  CHECK(plan > 0 && P.at("mem_plan").at("setup_inputs").num() > 0 && P.at("mem_plan").at("items").contains("x_tiles") && P.at("mem_plan").at("k").num() >= 8);
  CHECK_EQ(sh(ok + " --G 16 --plan-only 1 --mem-budget " + std::to_string(plan)), 0);
  CHECK_EQ(sh(ok + " --G 16 --plan-only 1 --mem-budget " + std::to_string(plan - 1)), 11);
  // the run: refused below the plan (exit 11, island file with status resource_limit, no estimates), admitted at it
  CHECK_EQ(sh(ok + " --G 16 --mem-budget " + std::to_string(plan - 1) + o("lim.bin")), 11);
  { v4::fmt::Reader R(dir("lim.bin")); Json m = R.json("meta");
    CHECK(m.at("status").str() == "resource_limit" && !R.has("logZ") && !R.has("pip_r") && !R.has("terminal_S"));
    CHECK(rec_of(dir("lim.bin") + ".json").at("status").str() == "resource_limit"); }
  { const int rc = sh(ok + " --G 16 --mem-budget " + std::to_string(plan) + o("adm.bin"));
    const Json r = rec_of(dir("adm.bin") + ".json");
    CHECKF(rc == 0 || r.at("reason").str().find("after step") != std::string::npos, "budget = plan: exit %d '%s'", rc, r.contains("reason") ? r.at("reason").str().c_str() : ""); }
  // G = 0 with a budget: the largest G that fits
  { const std::string pr2 = dir("plan2.json");
    CHECK_EQ(sh(ok + " --plan-only 1 --mem-budget " + std::to_string(plan) + " --record " + q(pr2)), 0);
    CHECK(rec_of(pr2).at("mem_plan").at("G").num() >= 16 && rec_of(pr2).at("mem_plan").at("total").num() <= (double)plan); }
  // the pre-load plan IS the plan run_island admits with (the Start is rebuilt from the same setup): same total, same G
  { const v4::wp4io::CalibIn ci = v4::wp4io::read_calib(cal, f.D.p, f.D.K, f.dhash, f.shash);
    Start st = load_start(f.spath, f.D); Neighbours nb = load_neighbours(f.spath, f.D.p);
    const SetupDims sd = read_setup_dims(f.spath, f.D.p, f.D.K);
    IslandConfig c; c.seed = 77; c.island = 1; c.N = ci.N; c.grid = ci.grid; c.L = ci.L; c.Hm = ci.Hm; c.B = 5; c.kernel = KernelKind::LabelMajor; c.threads = 2; c.G = 16;
    c.k_store = ci.k_store; c.inputs_bytes = start_bytes_model(sd);
    CHECK(plan_island(f.D, st, c).total == plan);
    c.G = 0; c.mem_budget = plan;   // G chosen by the budget: the same G as the plan-only record
    CHECK(plan_island(f.D, st, c).G == (int)rec_of(dir("plan2.json")).at("mem_plan").at("G").num());
    (void)nb; }
  // admission comes BEFORE the arrays are read (review PR52 MAJOR-2): a setup whose arrays load_start rejects (blk_members
  // not a partition; header, hashes and dimensions intact, calib.bin's inputs updated) is refused by the budget (11) without
  // ever being expanded, rejected by the load (13) when admitted, and planned (0) without any load
  { std::vector<int32_t> bm; { v4::fmt::Reader R(f.spath); bm = R.vec<int32_t>("blk_members"); }
    bm[0] = bm[1];
    const std::string bad = dir("setup_bad.bin"), calb = dir("calib_bad.bin");
    const std::string bh = rewrite_setup(f.spath, bad, {"blk_members"}, [&](v4::fmt::Writer& W) { W.add("blk_members", bm); });
    rewrite_calib_inputs(cal, calb, bh);
    const std::string b2 = bin + " island --data " + q(f.dpath) + " --setup " + q(bad) + " --calib " + q(calb) + " --mode V --seed 77 --island 1 --threads 2 --G 16";
    CHECK_EQ(sh(b2 + " --mem-budget 1" + o("bad_refused.bin")), 11);
    CHECK_EQ(sh(b2 + o("bad_loaded.bin")), 13);
    CHECK_EQ(sh(b2 + " --plan-only 1"), 0);
    CHECK_EQ(sh(b2 + " --plan-only 1 --mem-budget 1"), 11); }
  // --plan-only from sizes (10^6, V, 96 threads, G 64, k 7): the plan of memory.h
  { const std::string pr3 = dir("plan3.json");
    CHECK_EQ(sh(bin + " island --plan-only 1 --mode V --n 200 --p 1000000 --threads 96 --G 64 --k 7 --record " + q(pr3)), 0);
    MemSizes big; big.n = 200; big.p = 1000000; big.K = 100; big.N = 2500; big.B = v4::calib::budgets(200, 1000000).B; big.threads = 96; big.G = 64; big.cap = 40000001ULL; big.deferred = true;
    { IslandConfig gc; gc.kernel = KernelKind::LabelMajor; big.gram_slots = gram_slots_of(gc, 64, 1000000); }   // K3's Gram-row slots (default config: bounded scoring)
    const double t = rec_of(pr3).at("mem_plan").at("total").num();
    CHECKF(t == (double)island_memory(big, 7).total, "sizes plan %.0f vs memory.h %.0f", t, (double)island_memory(big, 7).total);
    std::printf("  1M final island plan (sizes, G 64, 96 threads, k 7): %.2f GiB\n", t / 1073741824.0);
    CHECK_EQ(sh(bin + " island --plan-only 1 --mode V --n 200 --p 1000000 --threads 96 --G 64 --k 7 --mem-budget 1000"), 11); }
  // calibrate --plan-only: the calibration island's plan (N-1: resident inside), and the run refuses one byte below it
  { const std::string cp = dir("cal_plan.json");
    CHECK_EQ(sh(bin + " calibrate --plan-only 1 --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --threads 3 --record " + q(cp)), 0);
    const Json C = rec_of(cp);
    CHECK(C.contains("island_plan") && !C.at("mem_plan").contains("island_budget"));
    // with a budget the island takes the largest G that fits: admitted iff the G = 1 plan (floor) fits
    const uint64_t ip = (uint64_t)C.at("island_plan").at("floor").num(), res = (uint64_t)C.at("island_plan").at("resident").num();
    CHECK(ip > res && ip <= (uint64_t)C.at("island_plan").at("total").num() && C.at("island_plan").at("setup_inputs").num() > 0);
    CHECK(res == (uint64_t)(C.at("mem_plan").at("ledger").num() + C.at("mem_plan").at("export").num()));
    CHECK_EQ(sh(bin + " calibrate --plan-only 1 --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --threads 3 --mem-budget " + std::to_string(ip)), 0);
    CHECK_EQ(sh(bin + " calibrate --plan-only 1 --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --threads 3 --mem-budget " + std::to_string(ip - 1)), 11);
    // a refused plan-only still prints the plan and its floor (review PR52 m5): that is when the requester resizes
    { const std::string cp2 = dir("cal_plan_refused.json");
      CHECK_EQ(sh(bin + " calibrate --plan-only 1 --mode V --n 200 --p 1000000 --threads 3 --mem-budget 1000 --record " + q(cp2)), 11);
      const Json R2 = rec_of(cp2);
      CHECK(R2.contains("plan_only") && R2.contains("island_plan") && R2.at("island_plan").at("floor").num() > 1e10 && R2.at("island_plan").at("admitted").boolean() == false); }
    // the run with the budget one byte below the island plan: the pilot is refused at admission (exit 11, no calib.bin)
    const std::string c2 = dir("calib_lim.bin");
    CHECK_EQ(sh(bin + " calibrate --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --threads 3 --mem-budget " + std::to_string(ip - 1) + " --out " + q(c2)), 11);
    struct stat sb{}; CHECK(::stat(c2.c_str(), &sb) != 0);
    // sizes only (no setup): the plan without the setup inputs
    CHECK_EQ(sh(bin + " calibrate --plan-only 1 --mode V --n 200 --p 1000000 --threads 96 --record " + q(cp)), 0);
    const Json C3 = rec_of(cp);
    std::printf("  1M calibration island plan (sizes, 96 threads, no setup inputs; resident included): %.2f GiB at G %d, floor %.2f GiB (G 1); calibration resident %.2f GiB\n",
                C3.at("island_plan").at("total").num() / 1073741824.0, (int)C3.at("island_plan").at("G").num(), C3.at("island_plan").at("floor").num() / 1073741824.0,
                C3.at("island_plan").at("resident").num() / 1073741824.0); }
}

TEST(island_command_resume) {
  Dir dir("res"); Fx f; make_fx(f, dir);
  const std::string cal = dir("calib.bin");
  { Json a = Json::object(); a["data"] = f.dpath; a["setup"] = f.spath; a["out"] = cal; a["mode"] = "V"; a["seed"] = 77.0; a["threads"] = 3.0;
    CHECK(v4::calib::run(a).at("status").str() == "completed"); }
  const v4::wp4io::CalibIn ci = v4::wp4io::read_calib(cal, f.D.p, f.D.K);
  auto args = [&](const std::string& out, const std::string& setup, const std::string& calibf) {
    Json a = Json::object(); a["data"] = f.dpath; a["setup"] = setup; a["calib"] = calibf; a["mode"] = "V"; a["seed"] = 77.0; a["island"] = 2.0;
    a["threads"] = 3.0; a["out"] = out; return a;
  };
  const Json full = v4::island::run(args(dir("full.bin"), f.spath, cal));
  CHECK(full.at("status").str() == "completed" && (int)full.at("resumed_from_step").num() == -1);
  // an island of the same configuration interrupted after step 2 leaves <out>.ckpt.{a,b}; the command resumes from it.
  // Same configuration = the CLI's: B = 5 for n = 60, p = 30, and the identity of the three verified inputs
  const std::string out = dir("island_2.bin"), ck = dir("island_2.ckpt");
  CHECK(v4::calib::budgets(f.D.n, f.D.p).B == 5);
  auto interrupted = [&](const std::string& ckbase, const std::string& setup_hash, const std::string& calib_hash, const std::string& setup_path) {
    Start st = load_start(setup_path, f.D); Neighbours nb = load_neighbours(setup_path, f.D.p);
    IslandConfig c; c.seed = 77; c.island = 2; c.tier = (uint32_t)ci.tier; c.N = ci.N; c.grid = ci.grid; c.L = ci.L; c.Hm = ci.Hm; c.B = 5; c.threads = 3;
    c.kernel = KernelKind::LabelMajor; c.ckpt_path = ckbase; c.ckpt_every_s = 1e9; c.stop_after_step = 2;
    c.input_id = input_identity(f.dhash, setup_hash, calib_hash);
    { const v4::OfferFloor of = v4::offer_floor_from_calib(ci.meta, true, ci.content_hash); c.offer_floor = of.f; c.offer_floor_calib = of.calib; }   // = the command (D-29)
    return run_island<Arith::ClassA>(f.D, st, nb, c).status;
  };
  CHECK(interrupted(ck, f.shash, ci.content_hash, f.spath) == 1);
  struct stat sb{}; CHECK(::stat((ck + ".a").c_str(), &sb) == 0 || ::stat((ck + ".b").c_str(), &sb) == 0);
  // other inputs, every normal check passing (review PR52 MAJOR-1): setup' = the same setup with another (valid, empty)
  // neighbour graph; calib' = calib.bin with meta.inputs updated to setup'. The frozen grid, N, L, Hm are the same, so only
  // the checkpoint's input identity tells the two apart. The checkpoint of the original inputs must be refused (13), and
  // stay on disk; the changed inputs themselves run fine from scratch
  const std::string setup_b = dir("setup_b.bin"), calib_b = dir("calib_b.bin");
  const std::vector<int64_t> empty_ptr((size_t)f.D.p + 1, 0); const std::vector<int32_t> empty_idx;   // Writer::add keeps a reference until write()
  const std::string shash_b = rewrite_setup(f.spath, setup_b, {"nb_ptr", "nb_idx"}, [&](v4::fmt::Writer& W) {
    W.add("nb_ptr", empty_ptr); W.add("nb_idx", empty_idx); });
  const std::string chash_b = rewrite_calib_inputs(cal, calib_b, shash_b);
  CHECK(shash_b != f.shash && chash_b != ci.content_hash);
  { bool refused = false;
    try { v4::island::run(args(out, setup_b, calib_b)); } catch (const v4::Error& e) { refused = e.st == v4::Status::invalid_input; }
    CHECK_MSG(refused, "a checkpoint of other inputs must be refused (invalid_input)");
    CHECK(::stat((ck + ".a").c_str(), &sb) == 0 || ::stat((ck + ".b").c_str(), &sb) == 0);   // not deleted
    CHECK(::stat(out.c_str(), &sb) != 0);                                                     // no island file
    const Json fresh = v4::island::run(args(dir("island_2_b.bin"), setup_b, calib_b));          // the changed inputs are themselves valid
    CHECK(fresh.at("status").str() == "completed" && (int)fresh.at("resumed_from_step").num() == -1);
    CHECK(fresh.at("output_hash").str() != full.at("output_hash").str()); }
  const Json res = v4::island::run(args(out, f.spath, cal));
  CHECKF(res.at("status").str() == "completed" && (int)res.at("resumed_from_step").num() == 2, "resume: status %s from step %d",
         res.at("status").str().c_str(), (int)res.at("resumed_from_step").num());
  CHECK(res.at("output_hash").str() == full.at("output_hash").str() && body_hash(out) == body_hash(dir("full.bin")));
  CHECK(::stat((ck + ".a").c_str(), &sb) != 0 && ::stat((ck + ".b").c_str(), &sb) != 0);   // removed after the completed write
}

// the Start model that admission uses before anything is expanded bounds what dep::Start + neighbours really take
// (start_bytes measures the expanded structures after the fact), without being far above it
TEST(start_bytes_model_bounds_start_bytes) {
  for (int bsz : {3, 5, 8}) {
    Dir dir("sbm" + std::to_string(bsz)); Fx f; make_fx(f, dir, bsz);
    const SetupDims sd = read_setup_dims(f.spath, f.D.p, f.D.K);
    const Start st = load_start(f.spath, f.D); const Neighbours nb = load_neighbours(f.spath, f.D.p);
    const double meas = start_bytes(st, nb), model = start_bytes_model(sd);
    CHECKF(sd.J == st.J && model >= meas && model <= 3.0 * meas, "blocks of %d: model %.0f B vs measured %.0f B (J %d)", bsz, model, meas, sd.J);
    std::printf("  blocks of %d: J = %d, Start + neighbours %.0f B measured, model %.0f B (x %.2f)\n", bsz, sd.J, meas, model, model / meas);
  }
}

TEST(plan_from_sizes_equals_plan_island) {
  v4::Data D; make_ar_data(D, 80, 600, 0.6, 7);
  Start st; build_start(st, D, contiguous_blocks(600, 4));
  int checked = 0;
  for (auto kern : {KernelKind::LabelMajor, KernelKind::ParticleMajor}) for (int th : {1, 3}) for (int G : {0, 1, 64}) for (auto role : {IslandRole::Final, IslandRole::Pilot})
    for (uint64_t budget : {0ull, 60ull << 20}) {
      IslandConfig c; c.kernel = kern; c.threads = th; c.G = G; c.role = role; c.N = 300; c.Hm = 3; c.mem_budget = budget; c.inputs_bytes = 12345;
      c.k_store = role == IslandRole::Final ? 9.5 : 0; c.island = role == IslandRole::Final ? 1 : 0;
      MemSizes za; double k = 0; int Ga = 0;
      const MemPlan a = plan_island(D, st, c, &za, &k, &Ga);
      MemSizes zb = plan_sizes(D.n, D.p, D.K, c);
      const MemPlan b = plan_with_budget(zb, k, c);
      bool same = a.total == b.total && a.G == b.G && Ga == b.G && a.items.size() == b.items.size();
      for (size_t i = 0; same && i < a.items.size(); ++i) same = a.items[i].name == b.items[i].name && a.items[i].bytes == b.items[i].bytes;
      CHECKF(same, "kernel %d threads %d G %d role %d budget %llu: %llu vs %llu", (int)kern, th, G, (int)role, (unsigned long long)budget,
             (unsigned long long)a.total, (unsigned long long)b.total);
      ++checked;
    }
  std::printf("  %d configurations: plan from sizes = plan_island\n", checked);
}

// ---- V-N mini-leg (exp/P1M-VN): V's final-island N is a parameter of `calibrate` (default V_N = 2,500) ------------------------
TEST(v_mode_N_parameter) {
  Dir dir("vn"); Fx f; make_fx(f, dir);
  const std::string bin = V4_SMCBVS4;
  const char* fenv = std::getenv("V4_F_SMCBVS4");   // optional: the frozen F binary (method-v3.1.1-listpip); then default-N outputs are compared with F's
  const std::string fbin = fenv ? fenv : "";
  const std::string common = " --data " + q(f.dpath) + " --setup " + q(f.spath) + " --mode V --seed 77 --threads 3";
  auto calibrate = [&](const std::string& exe, const std::string& tag, const std::string& extra) {
    const std::string out = dir("calib_" + tag + ".bin");
    const int rc = sh(exe + " calibrate" + common + extra + " --out " + q(out), dir("calib_" + tag + ".log"));
    return std::make_pair(rc, out);
  };
  // the frozen constants (calib_run.h): the default and the range of the V parameter
  CHECK(v4::calib::V_N == 2500 && v4::calib::V_N_MIN == 1 && v4::calib::V_N_MAX == (1 << 24));
  { const v4::calib::Budgets b = v4::calib::budgets(f.D.n, f.D.p);   // plumbing: frozen_N reads the parameter in V, never in T
    CHECK(v4::calib::frozen_N(b, v4::calib::Rule::bounded, 0) == 2500 && v4::calib::frozen_N(b, v4::calib::Rule::bounded, 0, 10000) == 10000);
    CHECK(v4::calib::frozen_N(b, v4::calib::Rule::coded, 0, 10000) == b.N[0] && v4::calib::frozen_N(b, v4::calib::Rule::coded, 1, 10000) == b.N[1]); }
  // default (no N), explicit N = 2500 and N = 10000
  const auto cd = calibrate(bin, "default", ""), c25 = calibrate(bin, "n2500", " --N 2500"), c1e4 = calibrate(bin, "n10000", " --N 10000");
  CHECK_EQ(cd.first, 0); CHECK_EQ(c25.first, 0); CHECK_EQ(c1e4.first, 0);
  if (cd.first || c25.first || c1e4.first) return;
  const v4::wp4io::CalibIn Id = v4::wp4io::read_calib(cd.second, f.D.p, f.D.K, f.dhash, f.shash), I25 = v4::wp4io::read_calib(c25.second, f.D.p, f.D.K, f.dhash, f.shash),
                           I4 = v4::wp4io::read_calib(c1e4.second, f.D.p, f.D.K, f.dhash, f.shash);
  CHECK(Id.N == 2500 && I25.N == 2500 && I4.N == 10000 && I4.tier == 0 && I4.rule == "bounded");
  CHECK(rec_of(cd.second + ".json").at("settings").at("tiers").at(0).at("N_final").num() == 2500 &&
        rec_of(c1e4.second + ".json").at("settings").at("tiers").at(0).at("N_final").num() == 10000);
  // default N = 2,500 is bit-identical: an omitted N, an explicit 2500 and the pre-change binary (F) give the same sections, meta included but for the timings
  CHECK(body_hash(cd.second) == body_hash(c25.second) && Id.grid == I25.grid && Id.hpm == I25.hpm);
  { const Json a = v4::fmt::Reader(cd.second).json("meta"), b = v4::fmt::Reader(c25.second).json("meta");
    for (const char* k : {"N", "L", "Hm", "tier", "I_used", "I_max", "k_store", "rule", "tau_cal_hex", "seed"}) CHECKF(a.dump().size() && (a.contains(k) == b.contains(k)) && (!a.contains(k) || a.at(k).dump() == b.at(k).dump()), "meta.%s", k); }
  // the calibration itself does not depend on N (its islands have H = 512): only meta.N and the records differ
  CHECK(body_hash(cd.second) == body_hash(c1e4.second) && Id.grid == I4.grid && Id.inherited.size() == I4.inherited.size());
  if (!fbin.empty()) {
    const auto cf = calibrate(fbin, "F", "");
    CHECK_EQ(cf.first, 0);
    if (cf.first == 0) { CHECKF(body_hash(cf.second) == body_hash(cd.second), "default-N calib.bin sections differ from F's"); const Json a = v4::fmt::Reader(cf.second).json("meta"), b = v4::fmt::Reader(cd.second).json("meta");
      CHECK(a.at("N").dump() == b.at("N").dump() && a.at("L").dump() == b.at("L").dump() && a.at("I_used").dump() == b.at("I_used").dump() && a.at("k_store").dump() == b.at("k_store").dump()); }
    std::printf("  default-N calib.bin vs F (%s): sections %s\n", fbin.c_str(), cf.first == 0 && body_hash(cf.second) == body_hash(cd.second) ? "identical" : "DIFFER");
  } else std::printf("  (V4_F_SMCBVS4 unset: no comparison with the F binary)\n");
  // invalid N is refused exactly as the island refuses T's N (a whole number in [1, 2^24]): exit 13, no calib.bin
  for (const char* bad : {"0", "-5", "2.5", "16777217", "abc"}) {
    const auto r = calibrate(bin, std::string("bad") + bad, std::string(" --N ") + bad);
    struct stat sb{};
    CHECKF(r.first == 13 && ::stat(r.second.c_str(), &sb) != 0, "calibrate --N %s: exit %d (expected 13, no calib.bin)", bad, r.first);
    CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cd.second) + " --mode V --seed 77 --island 1 --plan-only 1 --N " + bad), 13);   // T's check
  }
  { const auto r = calibrate(bin, "edgeN1", " --N 1"); CHECK_EQ(r.first, 0);   // the bounds themselves are accepted, as the island accepts them
    if (r.first == 0) CHECK(v4::wp4io::read_calib(r.second, f.D.p, f.D.K).N == 1); }
  // manifest path (the driver's): params.N is the authority; a different explicit --N is refused; an invalid manifest N is refused
  { const std::string rec = dir("plan.json");
    auto man = [&](const std::string& nm, const std::string& n) { const std::string m = dir(nm);
      std::ofstream(m) << "{\"schema\":\"smcbvs4.manifest/1\",\"command\":\"calibrate\",\"mode\":\"V\",\"params\":{\"N\":" + n + "}}\n"; return m; };
    const std::string plan = bin + " calibrate --plan-only 1 --n 200 --p 1000 --record " + q(rec);
    CHECK_EQ(sh(plan + " --manifest " + q(man("m1e4.json", "10000"))), 0);
    CHECK(rec_of(rec).at("settings").at("tiers").at(0).at("N_final").num() == 10000);
    CHECK_EQ(sh(plan + " --manifest " + q(man("m1e4b.json", "10000")) + " --N 2500"), 13);   // conflicting explicit N
    CHECK_EQ(sh(plan + " --N 2500 --manifest " + q(man("m1e4c.json", "10000"))), 13);        // either argument order
    CHECK_EQ(sh(plan + " --manifest " + q(man("m1e4d.json", "10000")) + " --N 10000"), 0);
    CHECK_EQ(sh(plan + " --manifest " + q(man("mbad.json", "0"))), 13);
    CHECK_EQ(sh(plan + " --manifest " + q(man("mbad2.json", "10000.5"))), 13); }
  // T mode is unchanged: calibrate (law, compat) takes no V parameter, its N is v3's N_e; --N is ignored as before
  for (const char* mode : {"law", "compat"}) {
    const std::string rec = dir(std::string("plan_") + mode + ".json");
    CHECK_EQ(sh(bin + " calibrate --plan-only 1 --mode " + mode + " --n 200 --p 1000 --record " + q(rec)), 0);
    const double n0 = rec_of(rec).at("settings").at("tiers").at(0).at("N_final").num();
    CHECK_EQ(sh(bin + " calibrate --plan-only 1 --mode " + mode + " --n 200 --p 1000 --N 10000 --record " + q(rec)), 0);
    CHECK(n0 == 2500 && rec_of(rec).at("settings").at("tiers").at(0).at("N_final").num() == n0 && rec_of(rec).at("settings").at("tiers").size() == 2); }
  // end to end at N = 10^4 on the fixture: islands take calib.bin's N, a conflicting --N is refused, the merge takes them; the reference run_island agrees
  { const std::string cal = c1e4.second; std::string isl; const int Rp = 2;
    Start st = load_start(f.spath, f.D); Neighbours nb = load_neighbours(f.spath, f.D.p);
    for (int r = 1; r <= Rp; ++r) {
      const std::string out = dir("island_n1e4_" + std::to_string(r) + ".bin");
      const double t0 = omp_get_wtime();
      CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode V --seed 77 --island " + std::to_string(r) + " --Rp " + std::to_string(Rp) +
                  " --threads 3 --out " + q(out)), 0);
      const Json rec = rec_of(out + ".json");
      CHECKF(rec.at("status").str() == "completed" && (int)rec.at("N").num() == 10000, "island %d: %s", r, rec.at("status").str().c_str());
      const IslandFile F = read_island_file(out);
      CHECK(F.rec.N == 10000 && (int)F.terminal.size() == 10000 && F.grid == I4.grid);
      IslandConfig c; c.seed = 77; c.island = (uint32_t)r; c.tier = 0; c.N = I4.N; c.grid = I4.grid; c.L = I4.L; c.Hm = I4.Hm; c.B = 5; c.threads = 3; c.kernel = KernelKind::LabelMajor;
      { const v4::OfferFloor of = v4::offer_floor_from_calib(I4.meta, true, I4.content_hash); c.offer_floor = of.f; c.offer_floor_calib = of.calib; }
      const IslandRun ref = run_island<Arith::ClassA>(f.D, st, nb, c);
      char hx[19]; std::snprintf(hx, sizeof hx, "0x%016llx", (unsigned long long)ref.hash());
      CHECKF(rec.at("output_hash").str() == hx, "N = 10^4 island %d: CLI output hash %s, run_island %s", r, rec.at("output_hash").str().c_str(), hx);
      std::printf("  N = 10^4 smoke, island %d: %.2f s, T = %zu, logZ = %.6f\n", r, omp_get_wtime() - t0, I4.grid.size() - 1, rec.at("logZ").num());
      isl += (r > 1 ? "," : "") + out;
    }
    CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --mode V --seed 77 --island 1 --threads 3 --N 2500 --out " + q(dir("island_conflict.bin"))), 13);
    const std::string fit = dir("fit_n1e4.bin");
    CHECK_EQ(sh(bin + " merge --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cal) + " --islands " + q(isl) + " --Rp " + std::to_string(Rp) + " --mode V --threads 2 --out " + q(fit)), 0);
    { v4::fmt::Reader R(fit); const Json m = R.json("meta");
      CHECK(m.at("status").str() == "completed" && (int)m.at("Rp").num() == Rp && (int)m.at("N").num() == 10000 && std::isfinite(m.at("logZ").num()));
      std::printf("  N = 10^4 smoke, merge: logZ = %.6f, N = %d\n", m.at("logZ").num(), (int)m.at("N").num()); }
    // an island file of N = 2,500 cannot be merged under an N = 10^4 calib.bin (and vice versa): the merge checks N against calib.bin's
    const std::string i25 = dir("island_n2500_1.bin");
    CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cd.second) + " --mode V --seed 77 --island 1 --Rp 2 --threads 3 --out " + q(i25)), 0);
    { // the merge refuses mixed N, both ways (exit 13: the island's meta.inputs name the other calib.bin; N itself is also checked at merge.h:274,323)
      const std::string i1e4 = dir("island_n1e4_1.bin"), i1e4b = dir("island_n1e4_2.bin");
      auto merge = [&](const std::string& calf, const std::string& islands, const std::string& out) {
        return sh(bin + " merge --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(calf) + " --islands " + q(islands) + " --Rp 2 --mode V --threads 2 --out " + q(out)); };
      // island 2 at N = 2,500 (calib `cd`), island 1 at N = 10^4 (calib `cal`)
      const std::string i25b = dir("island_n2500_2.bin");
      CHECK_EQ(sh(bin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cd.second) + " --mode V --seed 77 --island 2 --Rp 2 --threads 3 --out " + q(i25b)), 0);
      CHECK_EQ(merge(cal, i1e4 + "," + i25b, dir("fit_mix_a.bin")), 13);     // N = 10^4 calib.bin, one N = 2,500 island
      CHECK_EQ(merge(cd.second, i25 + "," + i1e4b, dir("fit_mix_b.bin")), 13); // N = 2,500 calib.bin, one N = 10^4 island
      CHECK_EQ(merge(cd.second, i25 + "," + i25b, dir("fit_n2500.bin")), 0);   // the matching N = 2,500 pair merges
    }
    if (!fbin.empty()) {   // default N: the island of the branch and of F: identical sections
      const std::string iF = dir("island_F_1.bin"), cF = dir("calib_F.bin");
      CHECK_EQ(sh(fbin + " island --data " + q(f.dpath) + " --setup " + q(f.spath) + " --calib " + q(cF) + " --mode V --seed 77 --island 1 --Rp 2 --threads 3 --out " + q(iF)), 0);
      CHECKF(body_hash(iF) == body_hash(i25), "default-N island file sections differ from F's");
      std::printf("  default-N island vs F: sections %s\n", body_hash(iF) == body_hash(i25) ? "identical" : "DIFFER");
    }
  }
  // the memory plans scale with N: island --plan-only (sizes) and the merge estimate; the admission edge sits between the two plans
  { const std::string r1 = dir("ip_2500.json"), r2 = dir("ip_10000.json");
    const std::string ip = bin + " island --plan-only 1 --mode V --n 200 --p 10000 --threads 4 --k 8 --G 1 --record ";   // G = 1: the plan is the admission floor
    CHECK_EQ(sh(ip + q(r1) + " --N 2500"), 0); CHECK_EQ(sh(ip + q(r2) + " --N 10000"), 0);
    const double t1 = rec_of(r1).at("mem_plan").at("total").num(), t2 = rec_of(r2).at("mem_plan").at("total").num();
    CHECKF(t2 > t1 && (int)rec_of(r2).at("N").num() == 10000, "island plan: N 2500 %.0f B, N 10^4 %.0f B", t1, t2);
    const uint64_t mid = (uint64_t)((t1 + t2) / 2);
    CHECK_EQ(sh(ip + q(r1) + " --N 2500 --mem-budget " + std::to_string(mid)), 0);
    CHECK_EQ(sh(ip + q(r2) + " --N 10000 --mem-budget " + std::to_string(mid)), 11);
    v4::merge::MergeSettings a, b; a.Rp = b.Rp = 16; a.p = b.p = 10000; a.kbar = b.kbar = 8; a.N = 2500; b.N = 10000;
    const v4::merge::MemEstimate ea = v4::merge::estimate_merge_memory(a), eb = v4::merge::estimate_merge_memory(b);
    CHECK(eb.small > ea.small && eb.total >= ea.total && eb.small - ea.small == (uint64_t)(16.0 * 7500 * (24 + 4 * 8.0)));
    std::printf("  memory plans, p = 10^4, 4 threads: final island %.2f -> %.2f GiB (N 2500 -> 10^4), merge terminal supports %.1f -> %.1f MiB\n",
                t1 / 1073741824.0, t2 / 1073741824.0, ea.small / 1048576.0, eb.small / 1048576.0); }
}
