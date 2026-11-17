// test_start_view.cpp -- StartView (include/v4/island/start_view.h; WP3_DESIGN §1.12, gate P5): the flat start law equals
// the expanded dep::Start in every table row, every pi_0 draw (result AND uniform consumption order) and every island hash.
//   * start_view_owned_equals_dep: StartView::from(dep::Start) on stand-in partitions (blocks of 4, 7 and 17: the last
//     enumerates its codes, beyond WP2's static tables).
//   * start_view_mapped_wp2_setup: setup.bin made by WP2's `setup` through the binary (gen -> prep -> setup), mapped. WP2's
//     sections (logprof, logF, size law, cond0, log Zbar0) equal the island's own rebuild from logr bit for bit; the mapped
//     view's rows and draws equal dep's; islands (V label-major 3 threads, law particle-major 3 threads, compat) give the
//     same hash with the mapped view as with the rebuilt dep::Start; the view holds no copy (its arrays lie in the mapping).
//   * start_view_cli_mapped: `calibrate` and `island` through the binary on that setup.bin: the island reads the mapped
//     view (record start_source), its output equals run_island on the rebuilt Start, and the plan's setup inputs are the
//     mapped section bytes + the draw scratch + the neighbour lists.
#include "v4/island/setup_load.h"   // first: the header must stand alone (review PR57 m5)
#include <omp.h>
#include <sys/wait.h>
#include <cstring>
#include <algorithm>
#include <filesystem>
#include <functional>
#include "tk.h"
#include "tutil.h"
#include "tutil_island.h"
#include "v4/calib_run.h"
#include "v4/island/island.h"
#include "v4/prep.h"
#include "v4/wp4_io.h"

using namespace v4::island;
using v4::Json;

namespace {
std::string q(const std::string& s) { return "'" + s + "'"; }
int sh(const std::string& c, const std::string& log = "/dev/null") {
  const int rc = std::system((c + " > " + q(log) + " 2>&1").c_str());
  return WIFEXITED(rc) ? WEXITSTATUS(rc) : -1;
}
struct Dir {
  std::string d;
  explicit Dir(const std::string& tag) {
    const char* t = std::getenv("TMPDIR");
    if (!t || !*t) throw std::runtime_error("TMPDIR is not set");
    d = tmp_path("wp3sv_" + tag); std::error_code ec; std::filesystem::remove_all(d, ec); std::filesystem::create_directories(d);
  }
  std::string operator()(const std::string& n) const { return d + "/" + n; }
  ~Dir() { std::error_code ec; std::filesystem::remove_all(d, ec); }
};
bool bits_eq(const double* a, const double* b, size_t n) { return n == 0 || std::memcmp(a, b, n * 8) == 0; }
bool bits_eq(const std::vector<double>& a, const double* b, size_t n) { return a.size() == n && bits_eq(a.data(), b, n); }

// every table row of the view equals the expanded dep::Start's (cond rows on demand, sub rows on demand, scan entries)
int compare_tables(const StartView& v, const dep::Start& st, const char* tag) {
  int bad = 0; const int K = v.K;
  StartView::Scratch& s = v.scr();
  if (v.J != st.J || !bits_eq(st.size_cum, v.size_cum.data(), v.size_cum.size()) || !bits_eq(st.size_logmass, v.size_logmass.data(), v.size_logmass.size()) ||
      std::memcmp(&v.logZbar0, &st.logZbar0, 8) != 0) ++bad;
  for (int b = 0; b < st.J; ++b) {
    if (!bits_eq(st.logprof[b], &v.logprof[(size_t)v.logprof_ptr[b]], (size_t)(v.top(b) + 1))) ++bad;
    for (int r = 0; r <= K; ++r) {
      if (std::memcmp(&st.cond_cum[b][r][0], &v.cond0[(size_t)b * (K + 1) + r], 8) != 0) ++bad;
      const int len = v.cond_row(b, r, s);
      if (!bits_eq(st.cond_cum[b][r], s.row, (size_t)len)) ++bad;
    }
    for (int j = 0; j <= v.top(b); ++j) {
      const uint32_t* cs; const uint32_t nc = v.sub_row(b, j, s, cs);
      if (!bits_eq(st.sub_cum[b][j], s.sc.data(), nc)) ++bad;
      for (uint32_t i = 0; i < nc; ++i) if (cs[i] != (uint32_t)st.codes_by_size[b][j][i]) { ++bad; break; }
    }
  }
  for (int b = 0; b <= st.J; ++b) if (!bits_eq(st.logF[b], &v.logF[(size_t)b * (K + 1)], (size_t)K + 1)) ++bad;
  CHECKF(bad == 0, "%s: %d table rows differ", tag, bad);
  return bad;
}
// draws: the same model and (serial path) the same uniforms in the same order; comp() of each model the same bits
int compare_draws(const StartView& v, const dep::Start& st, int n, const char* tag) {
  int bad = 0;
  for (uint32_t i = 1; i <= (uint32_t)n; ++i) {
    Address a0; a0.seed = 9; a0.island = 3; a0.xph = X_BRIDGE; a0.stage = 2; a0.particle = i; a0.position = 11;
    std::vector<uint32_t> sl1, sl2;
    auto nu1 = [&](uint32_t slot) { sl1.push_back(slot); Address a = a0; a.slot = slot; return uniform_at(a); };
    auto nu2 = [&](uint32_t slot) { sl2.push_back(slot); Address a = a0; a.slot = slot; return uniform_at(a); };
    v4::Model S1, S2, F1, F2;
    dep::draw_pi0(st, nu1, S1); draw_pi0(v, nu2, S2);
    if (S1 != S2 || sl1 != sl2) ++bad;
    const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
    auto nu = [&](uint32_t slot) { Address a = a0; a.slot = slot; return uniform_at(a); };
    auto nu8 = [&](const uint32_t* s, double* out) { philox8_word(ctr.data(), kk.data(), 0, s, out); };
    dep::draw_pi0_fast(st, nu, nu8, F1); draw_pi0_fast(v, nu, nu8, F2);
    if (F1 != F2 || F1 != S1) ++bad;
    const double c1 = st.comp(S1), c2 = v.comp(S1);
    if (std::memcmp(&c1, &c2, 8) != 0) ++bad;
  }
  CHECKF(bad == 0, "%s: %d of %d draws differ", tag, bad, n);
  return bad;
}
uint64_t island_hash(const v4::Data& D, const StartView& v, const Neighbours& nb, const char* mode, int threads) {
  IslandConfig c; c.seed = 21; c.island = 2; c.N = 300; c.grid = {0.0, 0.2, 0.6, 1.0}; c.L = 2; c.Hm = 2; c.B = v4::calib::budgets(D.n, D.p).B;
  c.threads = threads; c.G = 16; c.tile = 64;
  const std::string m = mode;
  if (m == "compat") { c.compat = true; c.kernel = KernelKind::ParticleMajor; c.threads = 1; return run_island<Arith::Bit>(D, v, nb, c).hash(); }
  if (m == "law") { c.kernel = KernelKind::ParticleMajor; return run_island<Arith::Bit>(D, v, nb, c).hash(); }
  c.kernel = KernelKind::LabelMajor; return run_island<Arith::ClassA>(D, v, nb, c).hash();
}
// a copy of setup.bin `src` at `dst` with the named sections replaced (every hash recomputed by the Writer: the file is valid as
// a file, malformed in its values)
std::string rewrite_setup(const std::string& src, const std::string& dst, const std::vector<std::string>& drop, const std::function<void(v4::fmt::Writer&)>& add) {
  v4::fmt::Reader R(src); v4::fmt::Writer W(R.kind(), R.mode());
  for (const auto& e : R.sections()) {
    const std::string nm(e.name);
    if (std::find(drop.begin(), drop.end(), nm) != drop.end()) continue;
    if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
    const void* qq = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                   : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                   : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                   : (const void*)R.get<uint8_t>(nm);
    W.add_copy(nm, e.dtype, qq, e.length, e.dims[0], e.dims[1]);
  }
  add(W);
  return W.write(dst);
}
// true iff the mapped loader refuses the file with invalid_input
bool refused(const std::string& path, const v4::Data& D, const char* why) {
  try { const StartView v = map_start_view(path, D); (void)v; }
  catch (const v4::Error& e) { if (e.st == v4::Status::invalid_input) return true; std::printf("    %s: wrong status %s\n", why, v4::status_name(e.st)); return false; }
  std::printf("    %s: ACCEPTED\n", why); return false;
}
// data.bin + setup.bin made by the binary: gen -> prep -> setup (WP2)
bool wp2_files(const Dir& dir, const std::string& design, int n, int p, int seed, std::string& dpath, std::string& spath) {
  const std::string bin = V4_SMCBVS4, raw = dir("raw.bin");
  dpath = dir("data.bin"); spath = dir("setup.bin");
  return sh(bin + " gen --design " + design + " --n " + std::to_string(n) + " --p " + std::to_string(p) + " --seed " + std::to_string(seed) + " --out " + q(raw)) == 0 &&
         sh(bin + " prep --in " + q(raw) + " --out " + q(dpath)) == 0 &&
         sh(bin + " setup --data " + q(dpath) + " --threads 3 --out " + q(spath)) == 0;
}
}  // namespace

TEST(start_view_owned_equals_dep) {
  for (int bsz : {4, 7, 17}) {
    v4::Data D; dep::make_ar_data(D, 60, bsz == 17 ? 34 : 600, 0.6, 51 + bsz);
    dep::Start st; dep::build_start(st, D, dep::contiguous_blocks(D.p, bsz));
    const StartView v = StartView::from(st); v.prepare(1);
    char tag[32]; std::snprintf(tag, sizeof tag, "owned, blocks of %d", bsz);
    CHECK(v.source == "owned" && v.J == st.J && v.max_m == bsz);
    compare_tables(v, st, tag);
    compare_draws(v, st, bsz == 17 ? 300 : 3000, tag);
  }
}

TEST(start_view_mapped_wp2_setup) {
  for (auto [design, n, p, seed] : std::vector<std::tuple<std::string, int, int, int>>{{"AR", 100, 400, 3}, {"BLK", 80, 300, 4}}) {
    Dir dir("map_" + design); std::string dpath, spath;
    CHECKF(wp2_files(dir, design, n, p, seed, dpath, spath), "%s: gen / prep / setup failed", design.c_str());
    if (!std::filesystem::exists(spath)) continue;
    const v4::Data D = v4::prep::load_data(dpath);
    const SetupDims sd = read_setup_dims(spath, D.p, D.K);
    CHECKF(sd.mappable, "%s: WP2's setup.bin should carry every section the view maps", design.c_str());
    const StartView v = map_start_view(spath, D); v.prepare(3);
    const dep::Start st = load_start(spath, D);   // the island's own rebuild from the partition and logr (core's arithmetic)
    const Neighbours nb = load_neighbours(spath, D.p);
    // the view is the mapping: no array is copied, and it costs exactly the planned section bytes
    { const auto* R = static_cast<const v4::fmt::Reader*>(v.keep.get());
      CHECK(v.source == "mapped" && R != nullptr && v.bytes() == sd.view_bytes); }
    std::printf("  %s n %d p %d: J = %d, largest block %d, K = %d, mapped start law %.1f KiB (sections)\n", design.c_str(), D.n, D.p, v.J, v.max_m, v.K, v.bytes() / 1024.0);
    // the sizes-only formula (WP2's count-only accounting -> the 10^6 plans) = the file's own section lengths
    { const SetupDims fd = dims_from_sizes(D.p, D.K, sd.m_hist, sd.nb_idx_len);
      CHECKF(fd.view_bytes == sd.view_bytes && fd.J == sd.J && fd.max_m == sd.max_m, "dims_from_sizes %llu B vs the file's %llu B",
             (unsigned long long)fd.view_bytes, (unsigned long long)sd.view_bytes); }
    char tag[48]; std::snprintf(tag, sizeof tag, "mapped WP2 %s", design.c_str());
    compare_tables(v, st, tag);      // = WP2's sections equal the island's rebuild bit for bit (and the on-demand rows)
    compare_draws(v, st, 3000, tag);
    for (const char* mode : {"V", "law", "compat"}) {
      const StartView vd = StartView::from(st);
      const uint64_t hv = island_hash(D, v, nb, mode, 3), hd = island_hash(D, vd, nb, mode, 3);
      CHECKF(hv == hd, "%s %s: island hash mapped %016llx vs rebuilt %016llx", design.c_str(), mode, (unsigned long long)hv, (unsigned long long)hd);
      std::printf("    %-6s island hash %016llx (mapped = rebuilt)\n", mode, (unsigned long long)hv);
      // pinned: the hashes of the engine before StartView (merge base 04d8d2b5, dep::Start loaded by load_start), measured
      // independently by the PR57 review on the same files. The bit forms are ISA-independent; class A depends on the build.
      const bool ar = design == "AR";
      const uint64_t pin = std::string(mode) == "law" ? (ar ? 0x5298f6a5216f12dcull : 0xeb1d5b4e7f10b76cull)
                         : std::string(mode) == "compat" ? (ar ? 0xc75513efe4d23803ull : 0xee17af9cce39896full) : 0ull;
      if (pin) CHECKF(hv == pin, "%s %s: hash %016llx differs from the pre-StartView engine's %016llx", design.c_str(), mode, (unsigned long long)hv, (unsigned long long)pin);
    }
  }
}

TEST(start_view_cli_mapped) {
  Dir dir("cli"); std::string dpath, spath;
  CHECK(wp2_files(dir, "AR", 100, 400, 7, dpath, spath));
  const std::string bin = V4_SMCBVS4, out = dir("island_1.bin");
  const std::string cal = dir("calib.bin");   // WP4's calibrate reads WP2's setup.bin directly (#46)
  CHECK_EQ(sh(bin + " calibrate --data " + q(dpath) + " --setup " + q(spath) + " --mode V --seed 5 --threads 3 --out " + q(cal)), 0);
  const std::string base = bin + " island --data " + q(dpath) + " --setup " + q(spath) + " --calib " + q(cal) + " --mode V --seed 5 --island 1 --threads 3";
  CHECK_EQ(sh(base + " --out " + q(out)), 0);
  const Json rec = v4::read_json_file(out + ".json");
  CHECK(rec.at("status").str() == "completed" && rec.at("start_source").str() == "mapped");
  const v4::Data D = v4::prep::load_data(dpath);
  const SetupDims sd = read_setup_dims(spath, D.p, D.K);
  const v4::wp4io::CalibIn ci = v4::wp4io::read_calib(cal, D.p, D.K);
  // = run_island on the rebuilt Start with calib.bin's settings
  { const dep::Start st = load_start(spath, D); const Neighbours nb = load_neighbours(spath, D.p);
    IslandConfig c; c.seed = 5; c.island = 1; c.tier = (uint32_t)ci.tier; c.N = ci.N; c.grid = ci.grid; c.L = ci.L; c.Hm = ci.Hm;
    c.B = v4::calib::budgets(D.n, D.p).B; c.threads = 3; c.kernel = KernelKind::LabelMajor;
    char hx[19]; std::snprintf(hx, sizeof hx, "0x%016llx", (unsigned long long)run_island<Arith::ClassA>(D, st, nb, c).hash());
    CHECKF(rec.at("output_hash").str() == hx, "CLI (mapped) %s vs rebuilt %s", rec.at("output_hash").str().c_str(), hx); }
  // the plan's setup inputs = mapped sections + draw scratch (3 threads) + neighbour lists
  { const std::string pr = dir("plan.json");
    CHECK_EQ(sh(base + " --plan-only 1 --record " + q(pr)), 0);
    const double si = v4::read_json_file(pr).at("mem_plan").at("setup_inputs").num();
    const double want = (double)sd.view_bytes + start_scratch_bytes(sd.max_m, D.K, 3) + 80.0 + (double)sd.nb_ptr_len * 8 + (double)sd.nb_idx_len * 4 + kStartFixedHeapBytes;
    CHECKF(si == want && si == start_inputs_bytes(sd, 3), "setup inputs %.0f vs mapped sections + scratch + neighbours %.0f", si, want);
    std::printf("  island plan setup inputs: %.1f KiB = mapped sections %.1f KiB + scratch + neighbours\n", si / 1024, sd.view_bytes / 1024.0); }
}

// calibrate's admission counts the live copy of setup.bin that WP4's reader keeps beside the mapped start law (review PR57
// MAJOR-1): a budget between the plan without the copy and the complete plan is refused, by --plan-only and by the run
// (no calib.bin), and the complete plan itself is admitted at its floor.
TEST(start_view_calibrate_admission_counts_setup_copy) {
  Dir dir("adm"); std::string dpath, spath;
  CHECK(wp2_files(dir, "AR", 100, 400, 9, dpath, spath));
  const std::string bin = V4_SMCBVS4, pr = dir("plan.json");
  const v4::Data D = v4::prep::load_data(dpath);
  const SetupDims sd = read_setup_dims(spath, D.p, D.K);
  const std::string base = bin + " calibrate --data " + q(dpath) + " --setup " + q(spath) + " --mode V --threads 3";
  CHECK_EQ(sh(base + " --plan-only 1 --record " + q(pr)), 0);
  const Json P = v4::read_json_file(pr).at("island_plan");
  const double copy = P.at("setup_copy").num();
  CHECKF(copy == setup_view_bytes(sd) && copy > 12.0 * D.p + 8.0 * sd.logr_len, "setup copy %.0f B vs setup_view_bytes %.0f", copy, setup_view_bytes(sd));
  const uint64_t floor_full = (uint64_t)P.at("floor").num(), floor_old = floor_full - (uint64_t)copy;   // the plan the PR admitted before the fix
  CHECK(floor_old < floor_full);
  CHECK_EQ(sh(base + " --plan-only 1 --mem-budget " + std::to_string(floor_full)), 0);
  CHECK_EQ(sh(base + " --plan-only 1 --mem-budget " + std::to_string(floor_full - 1)), 11);
  CHECK_EQ(sh(base + " --plan-only 1 --mem-budget " + std::to_string(floor_old)), 11);   // admitted before: refused now
  const std::string c1 = dir("calib_refused.bin"), c2 = dir("calib_ok.bin");
  CHECK_EQ(sh(base + " --seed 5 --mem-budget " + std::to_string(floor_old) + " --out " + q(c1)), 11);
  CHECK(!std::filesystem::exists(c1));                                                     // refused before any calibration
  CHECK_EQ(sh(base + " --seed 5 --mem-budget " + std::to_string(floor_full) + " --out " + q(c2)), 0);   // the complete plan is admitted (at G = 1)
  CHECK(std::filesystem::exists(c2));
}

// map_start_view refuses a file whose hashes are valid but whose values break the invariants the draws' bounds depend on
// (review PR57 MAJOR-2), and the draw itself stays in bounds if such arrays reach it (the clamps)
TEST(start_view_malformed_values_refused) {
  Dir dir("bad"); std::string dpath, spath;
  CHECK(wp2_files(dir, "AR", 100, 400, 3, dpath, spath));
  const v4::Data D = v4::prep::load_data(dpath);
  const size_t K1 = (size_t)D.K + 1;
  std::vector<double> sc, c0, lf, lp; std::vector<int32_t> blk, pos; std::vector<int64_t> cp;
  { v4::fmt::Reader R(spath); sc = R.vec<double>("size_cum"); c0 = R.vec<double>("cond0"); lf = R.vec<double>("logF"); lp = R.vec<double>("logprof");
    blk = R.vec<int32_t>("blk"); pos = R.vec<int32_t>("pos"); cp = R.vec<int64_t>("code_ptr"); }
  { bool ok = true; try { const StartView v = map_start_view(spath, D); (void)v; } catch (const v4::Error&) { ok = false; }
    CHECK_MSG(ok, "the untouched file must be accepted"); }
  auto mk = [&](const char* name, const std::function<void(v4::fmt::Writer&)>& add, const std::vector<std::string>& drop) {
    const std::string out = dir(std::string("bad_") + name + ".bin");
    rewrite_setup(spath, out, drop, add); return out; };
  // size law
  { std::vector<double> z(K1, 0.0);
    CHECK(refused(mk("size_zeros", [&](v4::fmt::Writer& W) { W.add("size_cum", z); }, {"size_cum"}), D, "size_cum all zeros"));
    std::vector<double> h = sc; h[K1 - 1] = 0.5;
    CHECK(refused(mk("size_end", [&](v4::fmt::Writer& W) { W.add("size_cum", h); }, {"size_cum"}), D, "size_cum ends at 0.5"));
    std::vector<double> m = sc; std::swap(m[0], m[1]); if (m[0] != m[1]) CHECK(refused(mk("size_mono", [&](v4::fmt::Writer& W) { W.add("size_cum", m); }, {"size_cum"}), D, "size_cum not monotone"));
    std::vector<double> t = sc; t[0] = std::nextafter(t[0], 1.0);   // one ulp off the rebuild: valid cumulative, wrong bits
    CHECK(refused(mk("size_ulp", [&](v4::fmt::Writer& W) { W.add("size_cum", t); }, {"size_cum"}), D, "size_cum one ulp off the rebuild")); }
  // scan table and profiles
  { std::vector<double> a = c0; a[3] = 2.0;
    CHECK(refused(mk("cond0_range", [&](v4::fmt::Writer& W) { W.add("cond0", a, (uint64_t)(c0.size() / K1), (uint64_t)K1); }, {"cond0"}), D, "cond0 entry 2.0"));
    std::vector<double> u = c0; u[K1 + 5] = std::nextafter(u[K1 + 5], u[K1 + 5] > 0.5 ? 0.0 : 1.0);   // a valid probability, wrong bits
    CHECK(refused(mk("cond0_ulp", [&](v4::fmt::Writer& W) { W.add("cond0", u, (uint64_t)(c0.size() / K1), (uint64_t)K1); }, {"cond0"}), D, "cond0 one ulp off the rebuilt row"));
    std::vector<double> f = lf; f[7] = std::nan("");
    CHECK(refused(mk("logF_nan", [&](v4::fmt::Writer& W) { W.add("logF", f, (uint64_t)(lf.size() / K1), (uint64_t)K1); }, {"logF"}), D, "logF NaN"));
    std::vector<double> q2 = lp; q2[1] = std::nan("");
    CHECK(refused(mk("logprof_nan", [&](v4::fmt::Writer& W) { W.add("logprof", q2); }, {"logprof"}), D, "logprof NaN")); }
  // partition and offsets
  { std::vector<int32_t> b2 = blk; b2[1] = b2[0] == b2[1] ? b2[1] : b2[0];
    if (b2 != blk) CHECK(refused(mk("blk", [&](v4::fmt::Writer& W) { W.add("blk", b2); }, {"blk"}), D, "blk of a variable moved to another block"));
    std::vector<int32_t> p2 = pos; p2[0] = p2[0] + 1;
    CHECK(refused(mk("pos", [&](v4::fmt::Writer& W) { W.add("pos", p2); }, {"pos"}), D, "pos shifted"));
    std::vector<int64_t> c2 = cp; c2[1] += 1;
    CHECK(refused(mk("code_ptr", [&](v4::fmt::Writer& W) { W.add("code_ptr", c2); }, {"code_ptr"}), D, "code_ptr step not 2^m")); }
  // identity: the second open must be the file the plan read (review PR57 m3)
  { bool r1 = false, r2 = false;
    try { map_start_view(spath, D, true, std::string(64, '0')); } catch (const v4::Error& e) { r1 = e.st == v4::Status::invalid_input; }
    try { load_neighbours(spath, D.p, false, std::string(64, '0')); } catch (const v4::Error& e) { r2 = e.st == v4::Status::invalid_input; }
    CHECK(r1 && r2);
    const SetupDims sd = read_setup_dims(spath, D.p, D.K, false);
    const StartView v = map_start_view(spath, D, true, sd.content_hash); (void)v;
    const Neighbours nb = load_neighbours(spath, D.p, false, sd.content_hash); CHECK(nb.ptr.size() == (size_t)D.p + 1); }
  // the draws stay in bounds on arrays the loader would have refused: a size law that never reaches 1, rows that never reach 1
  { const dep::Start st = load_start(spath, D);   // the island's own rebuild
    StartView v = StartView::from(st); v.prepare(1);
    auto* o = const_cast<sv_detail::Owned*>(static_cast<const sv_detail::Owned*>(v.keep.get()));
    std::fill(o->size_cum.begin(), o->size_cum.end(), 0.0);
    std::fill(o->cond0.begin(), o->cond0.end(), 0.0);
    for (size_t i = 0; i < o->logprof.size(); ++i) o->logprof[i] = v4::NEG_INF;   // every row all -inf: zeros after the cumulative
    int bad = 0;
    for (uint32_t i = 1; i <= 500; ++i) {
      Address a0; a0.seed = 4; a0.island = 1; a0.particle = i;
      auto nu = [&](uint32_t slot) { Address a = a0; a.slot = slot; return uniform_at(a); };
      v4::Model S; draw_pi0(v, nu, S);
      if ((int)S.size() > D.K) ++bad;
      for (int j : S) if (j < 0 || j >= D.p) ++bad;
    }
    CHECKF(bad == 0, "%d malformed draws left the bounds (size <= K, members in [0, p))", bad); }
}
