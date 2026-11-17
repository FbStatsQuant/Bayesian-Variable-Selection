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
#include <omp.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <cstdio>
#include <filesystem>
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
