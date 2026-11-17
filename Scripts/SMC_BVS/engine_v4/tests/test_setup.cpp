// test_setup.cpp -- WP2 unit tests, gate T11 (truncated linkage = exact dendrogram below 1 - tau_n), thread/tile
// invariance (T3 for setup), setup.bin round trip, edge cases.
#include <map>
#include <sys/stat.h>
#include <unistd.h>
#include "setup_tk.h"
#include "v4/format.h"
#include "v4/store.h"
#include "v4/wp4_io.h"

using namespace v4::setup;
using stk::Fixture;

namespace {
std::string tmpdir() { const char* t = std::getenv("TMPDIR"); return t ? t : "."; }

// Dense transcription of core/cpp/v3_core.cpp:746-760 (duplicate components) and :796-818 (cut group) on v4::gram;
// the R golden (tools/golden_setup_ref.R) checks the Rcpp originals.
void dense_components(const v4::Data& D, double thr, std::vector<std::vector<int>>& out) {
  int p = D.p; std::vector<int> parent(p); for (int j = 0; j < p; ++j) parent[j] = j;
  auto find = [&](int i) { while (parent[i] != i) { parent[i] = parent[parent[i]]; i = parent[i]; } return i; };
  std::vector<double> s(p); for (int j = 0; j < p; ++j) s[j] = std::sqrt(v4::gram(D, j, j));
  for (int a = 0; a < p; ++a) for (int b = a + 1; b < p; ++b)
    if (std::fabs(v4::gram(D, a, b)) / (s[a] * s[b]) >= thr) { int x = find(a), y = find(b); if (x != y) parent[std::max(x, y)] = std::min(x, y); }
  std::map<int, std::vector<int>> comp;
  for (int j = 0; j < p; ++j) comp[find(j)].push_back(j);
  out.clear(); for (auto& kv : comp) if (kv.second.size() >= 2) out.push_back(kv.second);
}
std::vector<std::vector<int>> rows(const Csr& c) {
  std::vector<std::vector<int>> r;
  for (int64_t i = 0; i < c.rows(); ++i) r.emplace_back(c.idx.begin() + c.ptr[i], c.idx.begin() + c.ptr[i + 1]);
  return r;
}
}  // namespace

TEST(unit_dup_components_and_cut_group) {
  for (auto d : {stk::TIE, stk::AR, stk::BLK, stk::IND})
    for (int p : {50, 700}) {
      Fixture F(d, 80, p, 3);
      CorrOptions o; o.B = default_B(80, p); o.threads = stk::threads();
      CorrResult C = correlation_pass(F.D(), o);
      std::vector<std::vector<int>> ref; dense_components(F.D(), 1 - 1e-10, ref);
      SCHECK(rows(C.dup) == ref, "dup components differ (%s p=%d)", stk::design_name(d), p);
      if (d == stk::TIE) SCHECK(C.dup.rows() > 0, "TIE fixture has no duplicates");
      PartitionOptions po; po.B = o.B;
      Partition P = make_partition(F.D(), C, po);
      Csr cut = cut_groups(p, C.edges, C.rn, P);
      std::vector<std::vector<int>> comps, flagged; dense_components(F.D(), C.rn, comps);
      for (auto& c : comps) { bool span = false; for (int j : c) if (P.blk[j] != P.blk[c[0]]) span = true; if (span) flagged.push_back(c); }
      SCHECK(rows(cut) == flagged, "cut groups differ (%s p=%d)", stk::design_name(d), p);
    }
}

// ---- T11: the truncated forest equals the exact dendrogram's merges of height <= 1 - tau_n (and < for strict)
namespace {
void t11(stk::Design d, int n, int p, uint64_t seed, bool strict, double tau = -1) {
  Fixture F(d, n, p, seed);
  int B = default_B(n, p);
  CorrOptions o; o.B = B; o.threads = stk::threads(); o.tau = tau;
  CorrResult C = correlation_pass(F.D(), o);
  const double hcut = 1.0 - C.tau;
  Forest Tt = complete_linkage_truncated(p, C.edges, hcut, strict);
  Forest Te = complete_linkage_exact(F.D(), stk::threads());
  int m = Tt.merges();
  bool ok = m <= Te.merges();
  for (int x = p; ok && x < p + m; ++x)
    ok = Tt.left[x] == Te.left[x] && Tt.right[x] == Te.right[x] && stk::same_bits(Tt.height[x], Te.height[x]);
  // the next exact merge (if any) is above the cut, and every truncated merge is within it
  if (ok && m < Te.merges()) ok = strict ? !(Te.height[p + m] < hcut) : !(Te.height[p + m] <= hcut);
  for (int x = p; ok && x < p + m; ++x) ok = strict ? Tt.height[x] < hcut : Tt.height[x] <= hcut;
  SCHECK(ok, "T11 fails: %s n=%d p=%d strict=%d (truncated merges %d, exact %d)", stk::design_name(d), n, p, (int)strict, m, Te.merges());
  // the clusters at the cut: identical member sets (T11 "identical clusters")
  auto clusters = [&](const Forest& T, int upto) {
    std::vector<int> parent(p + upto); for (int x = 0; x < p + upto; ++x) parent[x] = x;
    std::vector<int> lab(p);
    std::vector<int> owner(T.left.size(), -1);
    for (int x = p; x < p + upto; ++x) { owner[T.left[x]] = x; owner[T.right[x]] = x; }
    for (int j = 0; j < p; ++j) { int x = j; while (owner[x] >= 0 && owner[x] < p + upto) x = owner[x]; lab[j] = x; }
    return lab;
  };
  if (ok) SCHECK(clusters(Tt, m) == clusters(Te, m), "T11 clusters differ: %s p=%d", stk::design_name(d), p);
  std::printf("    T11 %s n=%d p=%d strict=%d: %d merges <= 1 - tau = %.6f, %zu edges, J(trunc) = %d\n", stk::design_name(d), n, p, (int)strict, m,
              hcut, C.edges.size(), cut_and_pack(Tt, B, PackOrder::MinIndex).J);
}
}  // namespace
TEST(T11_truncated_equals_exact_below_cut) {
  for (auto d : {stk::AR, stk::BLK, stk::IND, stk::TIE}) for (bool s : {false, true}) t11(d, 200, 1500, 21, s);
  t11(stk::AR, 60, 800, 22, false, 0.2);  // a lower tau: deep forests
}
TEST_TAGGED(T11_truncated_equals_exact_below_cut_full, "full") {
  for (auto d : {stk::AR, stk::BLK, stk::IND, stk::TIE}) t11(d, 200, 20000, 31, false);
  t11(stk::AR, 200, 20000, 32, true);
  t11(stk::AR, 400, 10000, 33, false);
}

// ---- truncated partition: blocks cover, sizes <= B, packing by minimum index, members sorted
TEST(unit_truncated_partition_shape) {
  for (auto d : {stk::AR, stk::BLK, stk::IND, stk::TIE}) {
    Fixture F(d, 200, 3000, 41);
    int B = default_B(200, 3000);
    CorrOptions o; o.B = B; o.threads = stk::threads();
    CorrResult C = correlation_pass(F.D(), o);
    PartitionOptions po; po.B = B;
    Forest T; Partition P = make_partition(F.D(), C, po, &T);
    std::vector<int> seen(3000, 0); bool ok = true;
    for (int b = 0; b < P.J; ++b) {
      ok &= P.size(b) >= 1 && P.size(b) <= P.B;
      ok &= std::is_sorted(P.block(b), P.block(b) + P.size(b));
      for (int i = 0; i < P.size(b); ++i) { seen[P.block(b)[i]]++; ok &= P.blk[P.block(b)[i]] == b && P.pos[P.block(b)[i]] == i; }
    }
    for (int j = 0; j < 3000; ++j) ok &= seen[j] == 1;
    // PR13 review m6: recompute the packing from the forest (retained clusters cut at > B_blocks, left first; ordered by
    // minimum member index; next-fit into blocks of <= B_blocks; members sorted) and compare with P
    {
      std::vector<std::pair<int, std::vector<int32_t>>> cl;
      for (int32_t r0 : T.roots) {
        std::vector<int32_t> st{r0};
        while (!st.empty()) {
          int x = st.back(); st.pop_back();
          if (T.size[x] <= P.B) {
            std::vector<int32_t> lv, s2{x};
            while (!s2.empty()) { int y = s2.back(); s2.pop_back(); if (y < 3000) lv.push_back(y); else { s2.push_back(T.right[y]); s2.push_back(T.left[y]); } }
            cl.push_back({*std::min_element(lv.begin(), lv.end()), lv});
            continue;
          }
          st.push_back(T.right[x]); st.push_back(T.left[x]);
        }
      }
      std::sort(cl.begin(), cl.end(), [](const auto& a, const auto& b) { return a.first < b.first; });
      std::vector<int64_t> bptr{0}; std::vector<int32_t> mem, cur;
      auto flush = [&]() { std::sort(cur.begin(), cur.end()); mem.insert(mem.end(), cur.begin(), cur.end()); bptr.push_back((int64_t)mem.size()); cur.clear(); };
      for (auto& c : cl) { if (cur.size() + c.second.size() > (size_t)P.B) flush(); cur.insert(cur.end(), c.second.begin(), c.second.end()); }
      if (!cur.empty()) flush();
      SCHECK(bptr == P.bptr && mem == P.members, "packing by minimum index differs from the recomputation (%s)", stk::design_name(d));
    }
    // every forest cluster of size <= B lies inside one block
    for (int32_t r : T.roots) if (T.size[r] <= P.B) {
      std::vector<int32_t> st{r}; int b0 = -1;
      while (!st.empty()) { int x = st.back(); st.pop_back(); if (x < 3000) { if (b0 < 0) b0 = P.blk[x]; ok &= P.blk[x] == b0; } else { st.push_back(T.left[x]); st.push_back(T.right[x]); } }
    }
    SCHECK(ok, "truncated partition shape (%s)", stk::design_name(d));
  }
}

// ---- invariance: setup.bin content hash identical for threads 1, 2, 3 and tile widths (T3 for setup)
TEST(invariance_threads_and_tiles) {
  // PR13 review m3: file identity is this run's content hash (meta holds timings and the binary block); the result is
  // compared through the hashes of every named section except meta, at threads 1, 2, 3.
  auto section_hashes = [](const std::string& path) {
    std::map<std::string, std::string> h;
    v4::fmt::Reader rd(path);
    for (const auto& e : rd.sections()) if (std::string(e.name) != "meta") h[e.name] = std::string((const char*)e.sha256, 32);
    return h;
  };
  for (auto d : {stk::AR, stk::TIE}) {
    Fixture F(d, 150, 2000, 51);
    for (PartMode pm : {PartMode::Truncated, PartMode::Exact}) {
      std::map<std::string, std::string> ref;
      for (int th : {1, 2, 3}) {
        SetupOptions o; o.threads = th; o.part.mode = pm;
        SetupResult r = run_setup(F.D(), o);
        SCHECK(r.status == v4::Status::completed, "setup failed: %s", r.reason.c_str());
        std::string path = tmpdir() + "/inv_" + std::to_string(getpid()) + ".bin";
        write_setup_bin(path, F.D(), r, o, "test");
        auto h = section_hashes(path);
        std::remove(path.c_str());
        if (ref.empty()) ref = h;
        SCHECK(h == ref && h.size() > 30, "setup.bin sections depend on threads (%s, threads %d, mode %d)", stk::design_name(d), th, (int)pm);
      }
    }
    for (int tile : {32, 100, 512}) {  // correlation pass alone
      CorrOptions a; a.B = 12; a.threads = 3; a.tile = tile;
      CorrOptions b = a; b.threads = 1; b.tile = 256;
      CorrResult ca = correlation_pass(F.D(), a), cb = correlation_pass(F.D(), b);
      bool ok = ca.nb.ptr == cb.nb.ptr && ca.nb.idx == cb.nb.idx && ca.edges.size() == cb.edges.size() && ca.dup.idx == cb.dup.idx;
      for (size_t i = 0; ok && i < ca.edges.size(); ++i) ok = ca.edges[i].j == cb.edges[i].j && ca.edges[i].l == cb.edges[i].l && stk::same_bits(ca.edges[i].absr, cb.edges[i].absr);
      SCHECK(ok, "correlation pass depends on tile/threads (tile %d)", tile);
    }
  }
}

// ---- setup.bin round trip and hash verification
TEST(unit_setup_bin_roundtrip) {
  Fixture F(stk::AR, 100, 500, 61);
  SetupOptions o; o.threads = stk::threads();
  SetupResult r = run_setup(F.D(), o);
  SCHECK(r.status == v4::Status::completed, "setup failed: %s", r.reason.c_str());
  std::string path = tmpdir() + "/rt_" + std::to_string(getpid()) + ".bin";
  std::string h = write_setup_bin(path, F.D(), r, o, "datahash");
  std::string h2; SetupResult q = read_setup_bin(path, &h2);
  SCHECK(h == h2, "content hash differs on read");
  SCHECK(q.corr.nb.idx == r.corr.nb.idx && q.corr.nb.ptr == r.corr.nb.ptr && q.part.members == r.part.members && q.part.blk == r.part.blk &&
        q.tab.logr.size() == r.tab.logr.size() && q.tab.cond_cum.size() == r.tab.cond_cum.size() && q.mode.S == r.mode.S &&
        stk::same_bits(q.tab.logZbar0, r.tab.logZbar0) && q.stores.top.pool == r.stores.top.pool && q.stores.hpmS == r.stores.hpmS,
        "round trip differs");
  bool ok = true;
  for (size_t i = 0; i < r.tab.logr.size(); ++i) ok &= stk::same_bits(q.tab.logr[i], r.tab.logr[i]);
  SCHECK(ok, "logr round trip");
  // a flipped byte must be detected
  {
    long at; { v4::fmt::Reader rd(path); at = (long)rd.entry("logr").offset + 3; }   // a byte inside a hashed section
    FILE* f = std::fopen(path.c_str(), "r+b"); std::fseek(f, at, SEEK_SET); int c = std::fgetc(f); std::fseek(f, at, SEEK_SET); std::fputc(c ^ 1, f); std::fclose(f);
    bool threw = false;
    try { read_setup_bin(path); } catch (const v4::Error& e) { threw = e.st == v4::Status::invalid_input; }
    SCHECK(threw, "corrupted setup.bin not detected");
  }
  std::remove(path.c_str());
}

// ---- edge cases
TEST(unit_edge_cases) {
  for (int p : {1, 2, 3}) {
    Fixture F(stk::IND, 12, p, 71);
    for (PartMode pm : {PartMode::Truncated, PartMode::Exact}) {
      SetupOptions o; o.part.mode = pm;
      SetupResult r = run_setup(F.D(), o);
      SCHECK(r.status == v4::Status::completed && r.part.J >= 1 && (int)r.corr.nb.ptr.size() == p + 1, "p=%d mode=%d: %s", p, (int)pm, r.reason.c_str());
    }
  }
  // tau above 1 (tiny n): no edges, every column its own cluster, still a valid partition
  Fixture F(stk::AR, 6, 400, 72);
  SetupOptions o; SetupResult r = run_setup(F.D(), o);
  SCHECK(r.status == v4::Status::completed && r.corr.rn > 1, "tiny n: %s rn=%g", r.reason.c_str(), r.corr.rn);
  // the edge cap is a resource_limit status, not a crash
  CorrOptions co; co.B = 4; co.max_edges = 10; co.tau = 0.0;
  bool threw = false;
  try { correlation_pass(F.D(), co); } catch (const v4::Error& e) { threw = e.st == v4::Status::resource_limit; }
  SCHECK(threw, "edge cap not enforced");
}

// ---- prefix scorer: the full-scorer fallback gives the same bits as the prefix path (goldens: prefix path = core/)
TEST(unit_tables_fallback_paths) {
  for (auto d : {stk::TIE, stk::AR}) {
    Fixture F(d, 60, 400, 81);
    CorrOptions co; co.B = default_B(60, 400); CorrResult C = correlation_pass(F.D(), co);
    PartitionOptions po; po.B = co.B; Partition P = make_partition(F.D(), C, po);
    TableStats t0, t1;
    Tables A = build_tables(F.D(), P, 2, nullptr, &t0);
    testing::set_force_fallback(3);
    Tables Bt = build_tables(F.D(), P, 2, nullptr, &t1);
    testing::set_force_fallback(0);
    bool ok = A.logr.size() == Bt.logr.size();
    for (size_t i = 0; ok && i < A.logr.size(); ++i) ok = stk::same_bits(A.logr[i], Bt.logr[i]);
    SCHECK(ok && t1.fallback_scored > 0, "forced fallback changes table bits (%s)", stk::design_name(d));
    std::printf("    tables %s: scored %llu, prefix %llu, fallback %llu (forced run: %llu)\n", stk::design_name(d), (unsigned long long)t0.scored,
                (unsigned long long)t0.prefix_scored, (unsigned long long)t0.fallback_scored, (unsigned long long)t1.fallback_scored);
  }
}

// ---- golden against core/'s R/Rcpp entry points (tools/golden_setup_ref.R): v3_preprocess'd X, cpp_setup
// (exact blocks, neighbours, tables, log Zbar0), cpp_dup_components and cpp_cut_group (core/cpp/v3_core.cpp:746-818).
// Fixtures: tests/fixtures/setup_wp2 (written by the script; regenerate with tests/run_tests.sh --fixtures). A missing
// fixture is a FAIL (INTERFACES v0.1.2 §1). V4_R_GOLDEN_DIR overrides the directory.
namespace {
std::vector<std::vector<int>> read_rows(const std::string& f) {
  std::vector<std::vector<int>> r; FILE* fp = std::fopen(f.c_str(), "r"); if (!fp) return r;
  char buf[1 << 16];
  while (std::fgets(buf, sizeof buf, fp)) {
    std::vector<int> row; char* s = buf;
    while (*s && *s != '\n') { row.push_back((int)std::strtol(s, &s, 10) - 1); if (*s == ',') ++s; }
    r.push_back(row);
  }
  std::fclose(fp); return r;
}
std::vector<double> read_f64(const std::string& f) {
  std::vector<double> v; FILE* fp = std::fopen(f.c_str(), "rb"); if (!fp) return v;
  std::fseek(fp, 0, SEEK_END); long n = std::ftell(fp); std::fseek(fp, 0, SEEK_SET);
  v.resize(n / 8); size_t got = std::fread(v.data(), 8, v.size(), fp); (void)got; std::fclose(fp); return v;
}
}  // namespace
TEST(golden_R_reference) {
  const char* env = std::getenv("V4_R_GOLDEN_DIR");
#ifdef V4_FIXTURE_DIR
  const std::string dflt = std::string(V4_FIXTURE_DIR) + "/setup_wp2";
#else
  const std::string dflt = "tests/fixtures/setup_wp2";
#endif
  const char* dir = env ? env : dflt.c_str();
  FILE* fi = std::fopen((std::string(dir) + "/INDEX").c_str(), "r");
  SCHECK(fi != nullptr, "no INDEX in %s", dir);
  if (!fi) return;
  char tagc[256]; int ncase = 0;
  while (std::fscanf(fi, "%255s", tagc) == 1) {
    std::string d = std::string(dir) + "/" + tagc + "/";
    int n, p, B; FILE* fd = std::fopen((d + "dims.txt").c_str(), "r"); int got = std::fscanf(fd, "%d %d %d", &n, &p, &B); (void)got; std::fclose(fd);
    auto X = read_f64(d + "Xs.f64"), y = read_f64(d + "ys.f64");
    auto ow = std::make_shared<v4::DataOwned>(); ow->X = X; ow->y = y;
    v4::Data own = v4::make_data(ow, n, p);
    SetupOptions o; o.B = B; o.threads = stk::threads(); o.part.mode = PartMode::Exact;
    SetupResult r = run_setup(own, o);
    SCHECK(r.status == v4::Status::completed, "%s: %s", tagc, r.reason.c_str());
    SCHECK(rows(r.corr.nb) == read_rows(d + "neighbours.txt"), "%s: neighbours differ from cpp_setup", tagc);
    std::vector<std::vector<int>> bl; for (int b = 0; b < r.part.J; ++b) bl.emplace_back(r.part.block(b), r.part.block(b) + r.part.size(b));
    SCHECK(bl == read_rows(d + "blocks.txt"), "%s: exact blocks differ from cpp_setup", tagc);
    SCHECK(rows(r.corr.dup) == read_rows(d + "dup.txt"), "%s: duplicate components differ from cpp_dup_components", tagc);
    SCHECK(rows(r.cut) == read_rows(d + "cut.txt"), "%s: cut groups differ from cpp_cut_group", tagc);
    auto lr = read_f64(d + "logr.f64"); bool ok = lr.size() == r.tab.logr.size();
    for (size_t i = 0; ok && i < lr.size(); ++i) ok = stk::same_bits(lr[i], r.tab.logr[i]);
    SCHECK(ok, "%s: tables differ from cpp_setup", tagc);
    SCHECK(stk::same_bits(read_f64(d + "logZbar0.f64")[0], r.tab.logZbar0), "%s: log Zbar0 differs", tagc);
    std::printf("    R golden %s: dup components %lld, cut groups %lld\n", tagc, (long long)r.corr.dup.rows(), (long long)r.cut.rows());
    ++ncase;
  }
  std::fclose(fi);
  SCHECK(ncase >= 4, "R reference has %d cases", ncase);
}

// ---- count-only (Sol review F1 item 1): the filter's edge set and partition equal production's; the accounting of
// the per-code and start-law arrays equals the arrays run_setup actually builds; the stores fit their bound.
TEST(count_only_equals_production_and_accounting_exact) {
  for (auto d : {stk::AR, stk::IND, stk::BLK, stk::TIE})
    for (int n : {60, 200}) {
      Fixture F(d, n, 3000, 91);
      const int B = default_B(n, 3000);
      PartitionOptions po;
      CountResult c = count_only(F.D(), po, B, stk::threads(), /*allow_filter=*/true);
      SetupOptions o; o.threads = stk::threads();
      SetupResult r = run_setup(F.D(), o);
      SCHECK(r.status == v4::Status::completed, "%s", r.reason.c_str());
      CorrOptions co; co.B = B; co.threads = stk::threads();
      CorrResult full = correlation_pass(F.D(), co);
      bool ok = c.corr.edges.size() == full.edges.size();
      for (size_t i = 0; ok && i < full.edges.size(); ++i)
        ok = c.corr.edges[i].j == full.edges[i].j && c.corr.edges[i].l == full.edges[i].l && stk::same_bits(c.corr.edges[i].absr, full.edges[i].absr);
      SCHECK(ok, "count-only edges differ from production (%s n=%d, filter=%d, %zu vs %zu)", stk::design_name(d), n, (int)c.filter_used,
             c.corr.edges.size(), full.edges.size());
      SCHECK(c.part.bptr == r.part.bptr && c.part.members == r.part.members, "count-only partition differs (%s n=%d)", stk::design_name(d), n);
      const MemAccount& A = c.acc;
      SCHECK(A.C == (int64_t)r.tab.logr.size() && A.NR == (int64_t)r.tab.logprof.size() && A.cond_vals == (int64_t)r.tab.cond_cum.size() &&
             A.J == r.part.J, "accounting differs from the built arrays (%s n=%d)", stk::design_name(d), n);
      uint64_t sb = 0;
      for (const v4::Store* st : {&r.stores.top, &r.stores.lead0, &r.stores.lead1})
        sb += st->v.size() * 26 + st->pool.size() * 4;
      uint64_t bound = 0; for (auto& it : A.items) if (it.name.rfind("table top stores kept", 0) == 0) bound = it.bytes;
      SCHECK(sb <= bound, "table stores exceed their accounted bound (%s n=%d)", stk::design_name(d), n);
      if (n == 200 && d == stk::AR) std::printf("    count-only AR n=200 p=3000: filter %d, candidates %llu, edges %zu, J %lld, C %lld, peak %.1f MB\n",
                                               (int)c.filter_used, (unsigned long long)c.candidates, c.corr.edges.size(), (long long)A.J, (long long)A.C, A.peak / 1e6);
    }
}

// ---- admission (Sol review F1 item 2) and the exact-mode guard (PR13 review m7)
TEST(admission_rule_refuses_with_reason) {
  Fixture F(stk::AR, 100, 1500, 92);
  SetupOptions o; o.threads = stk::threads(); o.mem_budget_gb = 1e-6;
  SetupResult r = run_setup(F.D(), o);
  SCHECK(r.status == v4::Status::resource_limit && r.reason.find("admission:") != std::string::npos, "%s", r.reason.c_str());
  o.mem_budget_gb = 64; r = run_setup(F.D(), o);
  SCHECK(r.status == v4::Status::completed, "%s", r.reason.c_str());
  SetupOptions e; e.part.mode = PartMode::Exact; e.mem_budget_gb = 8.0 * 1500 * 1500 / 1e9 / 2;   // below 8 p^2
  r = run_setup(F.D(), e);
  SCHECK(r.status == v4::Status::resource_limit && r.reason.find("exact partition needs") != std::string::npos, "%s", r.reason.c_str());
}

// ---- D-19: truncated blocks capped at min(B, bv_cap) at every n; exact keeps the coded B
TEST(d19_block_cap) {
  Fixture F(stk::IND, 400, 3000, 93);   // coded B = min(20, 54, 16) = 16
  SetupOptions o; o.threads = stk::threads();
  SetupResult r = run_setup(F.D(), o);
  int mx = 0; for (int b = 0; b < r.part.J; ++b) mx = std::max(mx, r.part.size(b));
  SCHECK(r.B == 16 && r.part.B == 14 && mx == 14, "D-19 cap: B=%d B_blocks=%d max block %d", r.B, r.part.B, mx);
  o.part.bv_cap = 9; r = run_setup(F.D(), o);
  mx = 0; for (int b = 0; b < r.part.J; ++b) mx = std::max(mx, r.part.size(b));
  SCHECK(r.part.B == 9 && mx <= 9, "bv_cap=9: max block %d", mx);
}

// ---- hub (Sol review F1 item 4): one column correlated with every other. The uncapped threshold graph and the
// symmetric neighbour union have a row of degree p - 1 (so "<= 2B per column" is false per column; the total is
// <= 2 p B); the edge guard turns a too-large graph into resource_limit; the partition stays valid.
TEST(hub_column_guard_and_degrees) {
  // tau_n = sqrt(2 log p / n) = 0.084 at (p, n) = (1200, 2000); hub loading 0.19: hub pairs r = 0.19 (about 5 sd above
  // tau_n, so the hub has degree p - 1), other pairs r = 0.036 (about 2 sd below: a few percent are noise edges)
  const int n = 2000, p = 1200;
  stk::Rng g(94);
  auto own = std::make_shared<v4::DataOwned>();
  own->X.resize((size_t)n * p); own->y.resize(n);
  std::vector<double> f(n); for (auto& v : f) v = g.norm();
  for (int j = 0; j < p; ++j)
    for (int i = 0; i < n; ++i) own->X[(size_t)j * n + i] = (j == 0) ? f[i] : 0.19 * f[i] + std::sqrt(1 - 0.19 * 0.19) * g.norm();
  for (int i = 0; i < n; ++i) own->y[i] = f[i] + g.norm();
  for (int j = 0; j <= p; ++j) {  // standardise columns and y
    double* x = j < p ? &own->X[(size_t)j * n] : own->y.data(); double m = 0, s = 0;
    for (int i = 0; i < n; ++i) m += x[i];
    m /= n; for (int i = 0; i < n; ++i) { x[i] -= m; s += x[i] * x[i]; }
    s = std::sqrt(s / (n - 1)); for (int i = 0; i < n; ++i) x[i] /= s;
  }
  v4::Data D = v4::make_data(own, n, p);
  const int B = default_B(n, p);
  CorrOptions co; co.B = B; co.threads = stk::threads();
  CorrResult C = correlation_pass(D, co);
  int64_t hubdeg = 0; for (const Edge& e : C.edges) if (e.j == 0 && e.absr >= C.rn) ++hubdeg;
  const int64_t nbhub = C.nb.ptr[1] - C.nb.ptr[0];
  SCHECK(hubdeg >= p - 1 - 20 && nbhub > 2 * B, "hub degree %lld (threshold graph), %lld (neighbour union)", (long long)hubdeg, (long long)nbhub);
  SCHECK((int64_t)C.nb.idx.size() <= 2LL * p * B, "neighbour total %zu > 2 p B", C.nb.idx.size());
  co.max_edges = p / 2;
  bool threw = false;
  try { correlation_pass(D, co); } catch (const v4::Error& e) { threw = e.st == v4::Status::resource_limit; }
  SCHECK(threw, "edge guard did not fire on the hub");
  SetupOptions o; o.threads = stk::threads(); o.max_edges = p / 2;
  SetupResult r = run_setup(D, o);
  SCHECK(r.status == v4::Status::resource_limit && r.reason.find("max_edges") != std::string::npos, "setup on the hub: %s", r.reason.c_str());
  o.max_edges = 0; r = run_setup(D, o);
  int mx = 0; for (int b = 0; b < r.part.J; ++b) mx = std::max(mx, r.part.size(b));
  SCHECK(r.status == v4::Status::completed && mx <= r.part.B, "setup with a hub: %s", r.reason.c_str());
  std::printf("    hub: threshold-graph degree %lld, neighbour-union degree %lld, edges %zu, J %d\n", (long long)hubdeg, (long long)nbhub, C.edges.size(), r.part.J);
}

// ---- PR13 review m9: CLI gen -> prep -> setup (and --count-only) -> info: exit codes, status, sections, meta
#ifdef V4_SMCBVS4
#include <sys/wait.h>
namespace {
int run_cli(const std::string& args) {
  std::string cmd = std::string(V4_SMCBVS4) + " " + args + " > /dev/null 2>&1";
  int st = std::system(cmd.c_str());
  return WIFEXITED(st) ? WEXITSTATUS(st) : -1;
}
}  // namespace
TEST(cli_setup_pipeline) {
  const std::string d = tmpdir() + "/clisetup_" + std::to_string(getpid());
  SCHECK(run_cli("gen --design AR --n 80 --p 400 --seed 5 --out " + d + "_raw.bin") == 0, "gen");
  SCHECK(run_cli("prep --in " + d + "_raw.bin --out " + d + "_data.bin") == 0, "prep");
  SCHECK(run_cli("setup --data " + d + "_data.bin --out " + d + "_setup.bin --threads 2") == 0, "setup");
  v4::Json rec = v4::read_json_file(d + "_setup.bin.json");
  SCHECK(rec.at("status").str() == "completed" && rec.contains("binary") && rec.at("partition").str() == "truncated" &&
         rec.at("file_mode").str() == "law", "setup record");
  {
    v4::fmt::Reader rd(d + "_setup.bin");
    v4::Json m = rd.json("meta");
    SCHECK(rd.kind() == v4::fmt::K_SETUP && m.contains("binary") && m.at("B_blocks").i64() <= 14 && rd.has("logr") && !rd.has("sub_cum") &&
           !rd.has("codes_by_size"), "setup.bin sections / meta");
  }
  SCHECK(run_cli("info --in " + d + "_setup.bin") == 0, "info");
  // driver form (WP3 pipeline, p = 2000): inputs from --manifest (data.bin by base name), as calibrate / island / merge
  {
    const std::string md = d + "_run";   // the driver's layout: <run>/data.bin (inputs are matched by base name)
    SCHECK(run_cli("gen --design AR --n 80 --p 400 --seed 5 --out " + md + "_raw.bin") == 0, "gen 2");
    mkdir(md.c_str(), 0700);
    SCHECK(run_cli("prep --in " + md + "_raw.bin --out " + md + "/data.bin") == 0, "prep into <run>/data.bin");
    const std::string dh = v4::fmt::Reader(md + "/data.bin").content_hash();
    auto manifest = [&](const std::string& path, const std::string& mode, int p) {
      v4::Json m = v4::Json::object(); m["schema"] = "smcbvs4.manifest/1"; m["command"] = "setup"; m["mode"] = mode;
      v4::Json in = v4::Json::object(); in[md + "/data.bin"] = dh; m["inputs"] = in;
      v4::Json pr = v4::Json::object(); pr["n"] = 80; pr["p"] = p; pr["seed"] = 3; pr["Rp"] = 4; pr["N"] = 100; m["params"] = pr;
      FILE* f = std::fopen(path.c_str(), "w"); std::fputs(m.dump(1).c_str(), f); std::fclose(f);
    };
    manifest(d + "_m.json", "law", 400);
    const int rcm = run_cli("setup --manifest " + d + "_m.json --threads 2 --out " + d + "_msetup.bin");
    SCHECK(rcm == 0, "setup --manifest: exit %d, %s", rcm, v4::read_json_file(d + "_msetup.bin.json").at("reason").str().c_str());
    if (rcm != 0) return;
    v4::fmt::Reader a(d + "_setup.bin"), b(d + "_msetup.bin");
    std::map<std::string, std::string> ha, hb;
    for (auto& e : a.sections()) ha[e.name] = std::string((const char*)e.sha256, 32);
    for (auto& e : b.sections()) hb[e.name] = std::string((const char*)e.sha256, 32);
    ha.erase("meta"); hb.erase("meta");
    const bool same = ha == hb && !ha.empty();
    SCHECK(same, "setup --manifest gives other data sections than setup --data");
    v4::Json mm = b.json("meta");
    SCHECK(mm.at("inputs").at("data.bin").str() == dh && mm.at("mode").str() == "law", "manifest-form setup.bin meta.inputs / mode");
    // meta.stores: WP4's store descriptors; read back with WP4's own reader
    for (const char* pf : {"tstore_top", "tstore_lead0", "tstore_lead1"}) {
      v4::Store s; v4::wp4io::read_store(b, mm, pf, s, 400, 80, nullptr);
      SCHECK(s.size() > 0 && s.size() == b.vec<double>(std::string(pf) + "_v").size(), "WP4 read_store on setup.bin %s", pf);
    }
    SCHECK(run_cli("setup --manifest " + d + "_m.json --data " + d + "_raw.bin --out " + d + "_x.bin") == 13, "--data that differs from the manifest: exit 13");
    manifest(d + "_m2.json", "law", 401);
    SCHECK(run_cli("setup --manifest " + d + "_m2.json --out " + d + "_x.bin") == 13, "manifest p differs from data.bin: exit 13");
    manifest(d + "_m3.json", "compat", 400);
    SCHECK(run_cli("setup --manifest " + d + "_m3.json --threads 2 --out " + d + "_csetup.bin") == 0, "compat manifest");
    v4::Json cr2 = v4::read_json_file(d + "_csetup.bin.json");
    SCHECK(cr2.at("partition").str() == "exact" && cr2.at("file_mode").str() == "compat", "compat manifest: exact partition, compat file");
    SCHECK(run_cli("setup --out " + d + "_x.bin") == 13, "no data: exit 13");
    for (const char* sfx : {"_m.json", "_m2.json", "_m3.json", "_msetup.bin", "_msetup.bin.json", "_csetup.bin", "_csetup.bin.json", "_x.bin.json",
                            "_run_raw.bin", "_run_raw.bin.json", "_run/data.bin", "_run/data.bin.json", "_truth.json"})
      std::remove((d + sfx).c_str());
    rmdir(md.c_str());
  }
  SCHECK(run_cli("setup --data " + d + "_data.bin --out " + d + "_count --count-only 1 --threads 2") == 0, "count-only");
  v4::Json cr = v4::read_json_file(d + "_count.json");
  SCHECK(cr.at("count_only").boolean() && cr.at("accounting").at("C").i64() > 0, "count-only record");
  SCHECK(run_cli("setup --data " + d + "_data.bin --out " + d + "_adm.bin --mem-budget 0.000001") == 11, "admission exit code (resource_limit = 11)");
  for (const char* sfx : {"_raw.bin", "_raw.bin.json", "_data.bin", "_data.bin.json", "_setup.bin", "_setup.bin.json", "_count.json", "_adm.bin.json", "_truth.json"})
    std::remove((d + sfx).c_str());
}
#endif

// ---- setup.bin -> the island's Start / Neighbours (manager request; WP3 island, WP4 calibration)
#include "v4/setup_island.h"
TEST(island_loader_round_trip) {
  namespace dep = v4::island::dep;
  for (auto d : {stk::AR, stk::TIE}) {
    Fixture F(d, 150, 1500, 101);
    SetupOptions o; o.threads = stk::threads();
    SetupResult r = run_setup(F.D(), o);
    SCHECK(r.status == v4::Status::completed, "%s", r.reason.c_str());
    const std::string path = tmpdir() + "/isl_" + std::to_string(getpid()) + ".bin";
    write_setup_bin(path, F.D(), r, o, "data-hash-A");
    dep::Start st; dep::Neighbours nb;
    std::string h = load_for_island(path, F.D(), st, nb, "data-hash-A");
    SCHECK(!h.empty() && st.D == &F.D() && st.J == r.part.J, "loader header (%s)", stk::design_name(d));
    // every array, in bits, against WP2's tables (sampler arrays stored here only for the comparison, D-18)
    Tables T2 = r.tab; build_start(F.D(), r.part, T2, /*store_sampler=*/true);
    bool ok = nb.ptr == r.corr.nb.ptr && nb.idx == r.corr.nb.idx && stk::same_bits(st.logZbar0, T2.logZbar0);
    const int K = F.D().K;
    for (int b = 0; ok && b < st.J; ++b) {
      ok = st.blocks[b] == std::vector<int>(r.part.block(b), r.part.block(b) + r.part.size(b));
      for (size_t c = 0; ok && c < st.logr[b].size(); ++c) ok = stk::same_bits(st.logr[b][c], T2.logr[T2.code_ptr[b] + c]) && stk::same_bits(st.lr(b, (uint32_t)c), st.logr[b][c]);
      for (size_t j = 0; ok && j < st.logprof[b].size(); ++j) {
        const int64_t row = T2.logprof_ptr[b] + (int64_t)j;
        ok = stk::same_bits(st.logprof[b][j], T2.logprof[row]) && st.codes_by_size[b][j].size() == (size_t)(T2.cbs_ptr[row + 1] - T2.cbs_ptr[row]);
        for (size_t q = 0; ok && q < st.codes_by_size[b][j].size(); ++q)
          ok = (uint32_t)st.codes_by_size[b][j][q] == T2.codes_by_size[T2.cbs_ptr[row] + q] && stk::same_bits(st.sub_cum[b][j][q], T2.sub_cum[T2.sub_ptr[row] + q]);
      }
      for (int r0 = 0; ok && r0 <= K; ++r0) {
        const size_t row = (size_t)b * (K + 1) + r0;
        ok = st.cond_cum[b][r0].size() == (size_t)(T2.cond_ptr[row + 1] - T2.cond_ptr[row]);
        for (size_t q = 0; ok && q < st.cond_cum[b][r0].size(); ++q) ok = stk::same_bits(st.cond_cum[b][r0][q], T2.cond_cum[T2.cond_ptr[row] + q]);
      }
    }
    for (int b = 0; ok && b <= st.J; ++b) for (int k = 0; ok && k <= K; ++k) ok = stk::same_bits(st.logF[b][k], T2.logF_at(b, k));
    SCHECK(ok, "island Start / Neighbours differ from setup's arrays (%s)", stk::design_name(d));
    // WP3's own stand-in sampler, run on the loaded logr, reproduces WP2's arrays (same bits)
    dep::Start re = st; dep::build_sampler(re, F.D());
    ok = stk::same_bits(re.logZbar0, st.logZbar0);
    for (int b = 0; ok && b < st.J; ++b) {
      for (size_t j = 0; ok && j < st.sub_cum[b].size(); ++j)
        for (size_t q = 0; ok && q < st.sub_cum[b][j].size(); ++q) ok = stk::same_bits(re.sub_cum[b][j][q], st.sub_cum[b][j][q]);
      for (int r0 = 0; ok && r0 <= K; ++r0)
        for (size_t q = 0; ok && q < st.cond_cum[b][r0].size(); ++q) ok = stk::same_bits(re.cond_cum[b][r0][q], st.cond_cum[b][r0][q]);
    }
    SCHECK(ok, "WP3's build_sampler on the loaded logr differs from WP2's arrays (%s)", stk::design_name(d));
    // pi_0 draws at the same Philox addresses (INTERFACES §3 v0.1.5 slots) and comp: identical
    Start S; S.D = &F.D(); S.P = &r.part; S.T = &r.tab; S.logZbar0 = r.tab.logZbar0;
    v4::AddressedSource as;
    v4::Model a, b2; ok = true;
    for (uint32_t i = 1; ok && i <= 5000; ++i) {
      v4::Address ad; ad.seed = 77; ad.role = v4::R_FINAL; ad.island = 3; ad.xph = v4::X_INIT; ad.particle = i;
      S.draw_pi0(as, ad, a);
      dep::draw_pi0(st, [&](uint32_t slot) { v4::Address x = ad; x.slot = slot; return v4::uniform_at(x); }, b2);
      ok = a == b2 && stk::same_bits(S.comp(a), st.comp(b2));
    }
    SCHECK(ok, "pi_0 draws or comp differ between setup::Start and island::dep::Start (%s)", stk::design_name(d));
    // refusals: other data (p differs) and another data.bin hash
    Fixture G(d, 150, 1400, 102);
    bool t1 = false, t2 = false;
    try { load_for_island(path, G.D(), st, nb); } catch (const v4::Error& e) { t1 = e.st == v4::Status::invalid_input; }
    try { load_for_island(path, F.D(), st, nb, "data-hash-B"); } catch (const v4::Error& e) { t2 = e.st == v4::Status::invalid_input; }
    SCHECK(t1 && t2, "loader refusals (%s): p mismatch %d, data hash %d", stk::design_name(d), (int)t1, (int)t2);
    std::remove(path.c_str());
  }
}
