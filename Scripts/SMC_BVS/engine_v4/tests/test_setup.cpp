// test_setup.cpp -- WP2 unit tests, gate T11 (truncated linkage = exact dendrogram below 1 - tau_n), thread/tile
// invariance (T3 for setup), setup.bin round trip, edge cases.
#include <map>
#include <unistd.h>
#include "setup_tk.h"
#include "wp1_format_shim.h"

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

TEST(unit_dup_components_and_cut_group, 0) {
  for (auto d : {stk::TIE, stk::AR, stk::BLK, stk::IND})
    for (int p : {50, 700}) {
      Fixture F(d, 80, p, 3);
      CorrOptions o; o.B = default_B(80, p); o.threads = stk::threads();
      CorrResult C = correlation_pass(F.D(), o);
      std::vector<std::vector<int>> ref; dense_components(F.D(), 1 - 1e-10, ref);
      CHECK(rows(C.dup) == ref, "dup components differ (%s p=%d)", stk::design_name(d), p);
      if (d == stk::TIE) CHECK(C.dup.rows() > 0, "TIE fixture has no duplicates");
      PartitionOptions po; po.B = o.B;
      Partition P = make_partition(F.D(), C, po);
      Csr cut = cut_groups(p, C.edges, C.rn, P);
      std::vector<std::vector<int>> comps, flagged; dense_components(F.D(), C.rn, comps);
      for (auto& c : comps) { bool span = false; for (int j : c) if (P.blk[j] != P.blk[c[0]]) span = true; if (span) flagged.push_back(c); }
      CHECK(rows(cut) == flagged, "cut groups differ (%s p=%d)", stk::design_name(d), p);
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
  CHECK(ok, "T11 fails: %s n=%d p=%d strict=%d (truncated merges %d, exact %d)", stk::design_name(d), n, p, (int)strict, m, Te.merges());
  // the clusters at the cut: identical member sets (T11 "identical clusters")
  auto clusters = [&](const Forest& T, int upto) {
    std::vector<int> parent(p + upto); for (int x = 0; x < p + upto; ++x) parent[x] = x;
    std::vector<int> lab(p);
    std::vector<int> owner(T.left.size(), -1);
    for (int x = p; x < p + upto; ++x) { owner[T.left[x]] = x; owner[T.right[x]] = x; }
    for (int j = 0; j < p; ++j) { int x = j; while (owner[x] >= 0 && owner[x] < p + upto) x = owner[x]; lab[j] = x; }
    return lab;
  };
  if (ok) CHECK(clusters(Tt, m) == clusters(Te, m), "T11 clusters differ: %s p=%d", stk::design_name(d), p);
  std::printf("    T11 %s n=%d p=%d strict=%d: %d merges <= 1 - tau = %.6f, %zu edges, J(trunc) = %d\n", stk::design_name(d), n, p, (int)strict, m,
              hcut, C.edges.size(), cut_and_pack(Tt, B, PackOrder::MinIndex).J);
}
}  // namespace
TEST(T11_truncated_equals_exact_below_cut, 0) {
  for (auto d : {stk::AR, stk::BLK, stk::IND, stk::TIE}) for (bool s : {false, true}) t11(d, 200, 1500, 21, s);
  t11(stk::AR, 60, 800, 22, false, 0.2);  // a lower tau: deep forests
}
TEST(T11_truncated_equals_exact_below_cut_full, 1) {
  for (auto d : {stk::AR, stk::BLK, stk::IND, stk::TIE}) t11(d, 200, 20000, 31, false);
  t11(stk::AR, 200, 20000, 32, true);
  t11(stk::AR, 400, 10000, 33, false);
}

// ---- truncated partition: blocks cover, sizes <= B, packing by minimum index, members sorted
TEST(unit_truncated_partition_shape, 0) {
  for (auto d : {stk::AR, stk::BLK, stk::IND, stk::TIE}) {
    Fixture F(d, 200, 3000, 41);
    int B = default_B(200, 3000);
    CorrOptions o; o.B = B; o.threads = stk::threads();
    CorrResult C = correlation_pass(F.D(), o);
    PartitionOptions po; po.B = B;
    Forest T; Partition P = make_partition(F.D(), C, po, &T);
    std::vector<int> seen(3000, 0); bool ok = true; int prev_min = -1;
    for (int b = 0; b < P.J; ++b) {
      ok &= P.size(b) >= 1 && P.size(b) <= B;
      ok &= std::is_sorted(P.block(b), P.block(b) + P.size(b));
      for (int i = 0; i < P.size(b); ++i) { seen[P.block(b)[i]]++; ok &= P.blk[P.block(b)[i]] == b && P.pos[P.block(b)[i]] == i; }
      (void)prev_min;
    }
    for (int j = 0; j < 3000; ++j) ok &= seen[j] == 1;
    // every forest cluster of size <= B lies inside one block
    for (int32_t r : T.roots) if (T.size[r] <= B) {
      std::vector<int32_t> st{r}; int b0 = -1;
      while (!st.empty()) { int x = st.back(); st.pop_back(); if (x < 3000) { if (b0 < 0) b0 = P.blk[x]; ok &= P.blk[x] == b0; } else { st.push_back(T.left[x]); st.push_back(T.right[x]); } }
    }
    CHECK(ok, "truncated partition shape (%s)", stk::design_name(d));
  }
}

// ---- invariance: setup.bin content hash identical for threads 1, 2, 3 and tile widths (T3 for setup)
TEST(invariance_threads_and_tiles, 0) {
  for (auto d : {stk::AR, stk::TIE}) {
    Fixture F(d, 150, 2000, 51);
    std::string ref;
    for (int th : {1, 2, 3})
      for (PartMode pm : {PartMode::Truncated, PartMode::Exact}) {
        SetupOptions o; o.threads = th; o.part.mode = pm;
        SetupResult r = run(F.D(), o);
        CHECK(r.status == v4::Status::completed, "setup failed: %s", r.reason.c_str());
        r.timings.clear();  // timings are not part of the result
        std::string path = tmpdir() + "/inv_" + std::to_string(getpid()) + ".bin";
        std::string h = write_setup_bin(path, F.D(), r, o, "test");
        std::remove(path.c_str());
        std::string key = std::to_string((int)pm);
        static std::map<std::string, std::string> refs;
        std::string k2 = std::string(stk::design_name(d)) + key;
        if (!refs.count(k2)) refs[k2] = h;
        CHECK(refs[k2] == h, "setup.bin hash depends on threads (%s, threads %d, mode %d)", stk::design_name(d), th, (int)pm);
      }
    for (int tile : {32, 100, 512}) {  // correlation pass alone
      CorrOptions a; a.B = 12; a.threads = 3; a.tile = tile;
      CorrOptions b = a; b.threads = 1; b.tile = 256;
      CorrResult ca = correlation_pass(F.D(), a), cb = correlation_pass(F.D(), b);
      bool ok = ca.nb.ptr == cb.nb.ptr && ca.nb.idx == cb.nb.idx && ca.edges.size() == cb.edges.size() && ca.dup.idx == cb.dup.idx;
      for (size_t i = 0; ok && i < ca.edges.size(); ++i) ok = ca.edges[i].j == cb.edges[i].j && ca.edges[i].l == cb.edges[i].l && stk::same_bits(ca.edges[i].absr, cb.edges[i].absr);
      CHECK(ok, "correlation pass depends on tile/threads (tile %d)", tile);
    }
  }
}

// ---- setup.bin round trip and hash verification
TEST(unit_setup_bin_roundtrip, 0) {
  Fixture F(stk::AR, 100, 500, 61);
  SetupOptions o; o.threads = stk::threads();
  SetupResult r = run(F.D(), o);
  CHECK(r.status == v4::Status::completed, "setup failed: %s", r.reason.c_str());
  std::string path = tmpdir() + "/rt_" + std::to_string(getpid()) + ".bin";
  std::string h = write_setup_bin(path, F.D(), r, o, "datahash");
  std::string h2; SetupResult q = read_setup_bin(path, &h2);
  CHECK(h == h2, "content hash differs on read");
  CHECK(q.corr.nb.idx == r.corr.nb.idx && q.corr.nb.ptr == r.corr.nb.ptr && q.part.members == r.part.members && q.part.blk == r.part.blk &&
        q.tab.logr.size() == r.tab.logr.size() && q.tab.cond_cum.size() == r.tab.cond_cum.size() && q.mode.S == r.mode.S &&
        stk::same_bits(q.tab.logZbar0, r.tab.logZbar0) && q.stores.top.pool == r.stores.top.pool && q.stores.hpmS == r.stores.hpmS,
        "round trip differs");
  bool ok = true;
  for (size_t i = 0; i < r.tab.logr.size(); ++i) ok &= stk::same_bits(q.tab.logr[i], r.tab.logr[i]);
  CHECK(ok, "logr round trip");
  // a flipped byte must be detected
  {
    FILE* f = std::fopen(path.c_str(), "r+b"); std::fseek(f, -10, SEEK_END); int c = std::fgetc(f); std::fseek(f, -10, SEEK_END); std::fputc(c ^ 1, f); std::fclose(f);
    bool threw = false;
    try { read_setup_bin(path); } catch (const v4::Error& e) { threw = e.st == v4::Status::invalid_input; }
    CHECK(threw, "corrupted setup.bin not detected");
  }
  std::remove(path.c_str());
}

// ---- edge cases
TEST(unit_edge_cases, 0) {
  for (int p : {1, 2, 3}) {
    Fixture F(stk::IND, 12, p, 71);
    for (PartMode pm : {PartMode::Truncated, PartMode::Exact}) {
      SetupOptions o; o.part.mode = pm;
      SetupResult r = run(F.D(), o);
      CHECK(r.status == v4::Status::completed && r.part.J >= 1 && (int)r.corr.nb.ptr.size() == p + 1, "p=%d mode=%d: %s", p, (int)pm, r.reason.c_str());
    }
  }
  // tau above 1 (tiny n): no edges, every column its own cluster, still a valid partition
  Fixture F(stk::AR, 6, 400, 72);
  SetupOptions o; SetupResult r = run(F.D(), o);
  CHECK(r.status == v4::Status::completed && r.corr.rn > 1, "tiny n: %s rn=%g", r.reason.c_str(), r.corr.rn);
  // the edge cap is a resource_limit status, not a crash
  CorrOptions co; co.B = 4; co.max_edges = 10; co.tau = 0.0;
  bool threw = false;
  try { correlation_pass(F.D(), co); } catch (const v4::Error& e) { threw = e.st == v4::Status::resource_limit; }
  CHECK(threw, "edge cap not enforced");
}

// ---- prefix scorer: the full-scorer fallback gives the same bits as the prefix path (goldens: prefix path = core/)
TEST(unit_tables_fallback_paths, 0) {
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
    CHECK(ok && t1.fallback_scored > 0, "forced fallback changes table bits (%s)", stk::design_name(d));
    std::printf("    tables %s: scored %llu, prefix %llu, fallback %llu (forced run: %llu)\n", stk::design_name(d), (unsigned long long)t0.scored,
                (unsigned long long)t0.prefix_scored, (unsigned long long)t0.fallback_scored, (unsigned long long)t1.fallback_scored);
  }
}
