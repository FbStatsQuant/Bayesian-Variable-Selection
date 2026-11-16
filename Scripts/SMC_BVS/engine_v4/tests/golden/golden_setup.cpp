// golden_setup.cpp -- golden bit tests of WP2 setup against core/ (revision D), PROTOCOL §2 / spec gate T1.
// The reference is core/cpp/v3_ledger.h (which includes v3_start.h, v3_blocks.h, v3_score.h, v3_util.h) compiled
// unchanged in this translation unit with the v3 flags (-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2).
// Every comparison is of bits (same_bits), on fixed seeds.
#include "v3_ledger.h"
#include "setup_tk.h"

using namespace v4::setup;
using stk::Fixture;

namespace {
struct V3 {  // the v3 reference objects for one fixture
  v3::Data D;
  explicit V3(const v4::Data& d) {
    std::vector<int> orig(d.p); for (int j = 0; j < d.p; ++j) orig[j] = j + 1;
    v3::data_init(D, d.Xs, d.ys, d.n, d.p, orig);
  }
};
std::vector<std::vector<int>> to_v3_blocks(const Partition& P) {
  std::vector<std::vector<int>> out(P.J);
  for (int b = 0; b < P.J; ++b) out[b].assign(P.block(b), P.block(b) + P.size(b));
  return out;
}
struct XsSource : v3::VariateSource {  // the v3 stream, read serially (CompatSource semantics, INTERFACES §3)
  v3::Xoshiro256ss g; double u(const char*) override { return g.uniform(); }
};
struct XsSource4 : v4::UniformSource {
  v3::Xoshiro256ss g; double u(const v4::Address&) override { return g.uniform(); }
};
struct Case { stk::Design d; int n, p; uint64_t seed; };
std::vector<Case> cases(bool full) {
  std::vector<Case> c;
  for (auto d : {stk::IND, stk::AR, stk::BLK, stk::TIE}) {
    c.push_back({d, 60, 40, 11}); c.push_back({d, 200, 300, 12}); c.push_back({d, 100, 1200, 13});
    if (full) { c.push_back({d, 200, 2500, 14}); c.push_back({d, 30, 500, 15}); }
  }
  c.push_back({stk::AR, 20, 2, 16}); c.push_back({stk::IND, 20, 3, 17}); c.push_back({stk::AR, 8, 9, 18});
  return c;
}
std::string tag(const Case& c) { return std::string(stk::design_name(c.d)) + " n=" + std::to_string(c.n) + " p=" + std::to_string(c.p); }

// ---- G1 neighbour graph: core/cpp/v3_blocks.h:149-173, threads 1..3, two tile widths
void check_neighbours(const Fixture& F, V3& R, int B, const std::string& t) {
  auto ref = v3::neighbour_graph(R.D, B);
  for (int th : {1, stk::threads()})
    for (int tile : {64, 256}) {
      CorrOptions o; o.B = B; o.threads = th; o.tile = tile;
      CorrResult C = correlation_pass(F.D(), o);
      bool ok = C.nb.rows() == F.p;
      for (int j = 0; ok && j < F.p; ++j) {
        std::vector<int> row(C.nb.idx.begin() + C.nb.ptr[j], C.nb.idx.begin() + C.nb.ptr[j + 1]);
        if (row != ref[j]) ok = false;
      }
      CHECK(ok, "neighbours differ: %s threads=%d tile=%d", t.c_str(), th, tile);
    }
}
}  // namespace

TEST(golden_G1_neighbour_graph, 0) {
  for (auto& c : cases(false)) { Fixture F(c.d, c.n, c.p, c.seed); V3 R(F.D()); check_neighbours(F, R, default_B(c.n, c.p), tag(c)); }
}
TEST(golden_G1_neighbour_graph_full, 1) {
  for (auto& c : cases(true)) { Fixture F(c.d, c.n, c.p, c.seed); V3 R(F.D()); for (int B : {1, 5, default_B(c.n, c.p)}) check_neighbours(F, R, B, tag(c)); }
}

// ---- G2 exact partition: core/cpp/v3_blocks.h:46-145 (blocks, merges, heights)
namespace {
void golden_exact(bool full) {
  for (auto& c : cases(full)) {
    Fixture F(c.d, c.n, c.p, c.seed); V3 R(F.D());
    int B = default_B(c.n, c.p);
    v3::Dendrogram T3;
    auto blocks3 = v3::make_blocks(R.D, B, &T3);
    Forest T4 = complete_linkage_exact(F.D(), stk::threads());
    bool ok = (int)T4.left.size() == (int)T3.left.size();
    for (size_t x = 0; ok && x < T4.left.size(); ++x)
      ok = T4.left[x] == T3.left[x] && T4.right[x] == T3.right[x] && T4.size[x] == T3.size[x] && T4.minidx[x] == T3.minidx[x] && stk::same_bits(T4.height[x], T3.height[x]);
    CHECK(ok, "dendrogram differs: %s", tag(c).c_str());
    Partition P = cut_and_pack(T4, B, PackOrder::LeafOrder);
    CHECK(to_v3_blocks(P) == blocks3, "exact blocks differ: %s", tag(c).c_str());
    PartitionOptions po; po.mode = PartMode::Exact; po.B = B; po.threads = 1;
    CorrOptions co; co.B = B;
    Partition P2 = make_partition(F.D(), correlation_pass(F.D(), co), po);
    CHECK(to_v3_blocks(P2) == blocks3, "make_partition(Exact) differs: %s", tag(c).c_str());
  }
}
}  // namespace
TEST(golden_G2_exact_partition, 0) { golden_exact(false); }
TEST(golden_G2_exact_partition_full, 1) { golden_exact(true); }

// ---- G3-G7: tables, table top stores, start law, draws, start mode; on the exact and the truncated partition
namespace {
void golden_tables_start(const Fixture& F, V3& R, const Partition& P, const std::string& t, bool full) {
  const v4::Data& D = F.D();
  // v3 reference
  v3::Start st; st.D = &R.D; st.blocks = to_v3_blocks(P);
  v3::Scorer sc(&R.D);
  v3::build_tables(st, sc);
  v3::build_start(st);
  // v4
  TableStores S4; TableStats ts;
  Tables T = build_tables(D, P, stk::threads(), &S4, &ts);
  build_start(D, P, T);
  // G3 tables (logr bits, NaN pattern)
  bool ok = T.J == st.J;
  for (int b = 0; ok && b < T.J; ++b)
    for (uint32_t c = 0; ok && c < st.logr[b].size(); ++c) ok = stk::same_bits(T.logr[T.code_ptr[b] + c], st.logr[b][c]);
  CHECK(ok, "tables logr differ: %s", t.c_str());
  CHECK(ts.scored == ts.prefix_scored + ts.fallback_scored + (uint64_t)P.J, "table counts: %s", t.c_str());
  // G4 table top stores vs the v3 ledger fed as core/cpp/v3_core.cpp:372-386 (ingest_tables)
  {
    v3::Ledger led(&R.D, 4);
    v3::EventCtx ev; ev.phase = v3::PH_TABLE; ev.island = 0;
    std::vector<int> U;
    for (int b = 0; b < st.J; ++b) {
      int m = (int)st.blocks[b].size();
      for (uint32_t c = 0; c < (1u << m); ++c) {
        if (std::isnan(st.logm_tab[b][c])) continue;
        U.clear(); for (int i = 0; i < m; ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
        double lm = st.logm_tab[b][c], Fv = R.D.logprior[U.size()] + lm, lg0 = R.D.logprior[U.size()] + st.logr[b][c];
        ev.stage = b + 1; ev.position = (int)c;
        led.event(U, Fv, lg0, lm, true, false, ev, v3::ME_TABLE);
      }
    }
    auto cmp_store = [&](const v3::TopStore& a, const v4::Store& s, const char* nm) {
      bool o = a.s.size() == s.size(); size_t i = 0;
      for (auto it = a.s.begin(); o && it != a.s.end(); ++it, ++i) {
        std::vector<int> m(s.pool.begin() + s.off[i], s.pool.begin() + s.off[i] + s.len[i]);
        o = stk::same_bits(it->v, s.v[i]) && it->S == m && s.hash[i] == D.zob.hash(s.S(i));
      }
      CHECK(o, "table store %s differs: %s (sizes %zu vs %zu)", nm, t.c_str(), a.s.size(), s.size());
    };
    cmp_store(led.top, S4.top, "top"); cmp_store(led.lead0, S4.lead0, "lead0"); cmp_store(led.lead1, S4.lead1, "lead1");
    std::vector<int> h(S4.hpmS.begin(), S4.hpmS.end());
    CHECK(led.has_hpm && h == led.hpmS && stk::same_bits(S4.hpmF, led.hpmF), "table HPM differs: %s", t.c_str());
    CHECK(S4.hpm_block + 1 == led.hpm_ev.stage && (int)S4.hpm_code == led.hpm_ev.position, "table HPM provenance differs: %s", t.c_str());
  }
  // G5 start law (core/cpp/v3_start.h:101-151)
  ok = stk::same_bits(T.logZbar0, st.logZbar0);
  for (int b = 0; ok && b < T.J; ++b) {
    int npr = (int)(T.logprof_ptr[b + 1] - T.logprof_ptr[b]);
    ok = npr == (int)st.logprof[b].size();
    for (int j = 0; ok && j < npr; ++j) {
      int64_t row = T.logprof_ptr[b] + j;
      ok = stk::same_bits(T.logprof[row], st.logprof[b][j]) && (size_t)(T.cbs_ptr[row + 1] - T.cbs_ptr[row]) == st.codes_by_size[b][j].size();
      for (size_t q = 0; ok && q < st.codes_by_size[b][j].size(); ++q)
        ok = T.codes_by_size[T.cbs_ptr[row] + q] == st.codes_by_size[b][j][q] && stk::same_bits(T.sub_cum[T.sub_ptr[row] + q], st.sub_cum[b][j][q]);
    }
    for (int r = 0; ok && r <= D.K; ++r) {
      size_t row = (size_t)b * (D.K + 1) + r;
      ok = (size_t)(T.cond_ptr[row + 1] - T.cond_ptr[row]) == st.cond_cum[b][r].size();
      for (size_t q = 0; ok && q < st.cond_cum[b][r].size(); ++q) ok = stk::same_bits(T.cond_cum[T.cond_ptr[row] + q], st.cond_cum[b][r][q]);
    }
  }
  for (int b = 0; ok && b <= T.J; ++b) for (int k = 0; ok && k <= D.K; ++k) ok = stk::same_bits(T.logF_at(b, k), st.logF[b][k]);
  for (int k = 0; ok && k <= D.K; ++k) ok = stk::same_bits(T.size_logmass[k], st.size_logmass[k]) && stk::same_bits(T.size_cum[k], st.size_cum[k]);
  CHECK(ok, "start law differs: %s", t.c_str());
  // comp and log gamma_0 on the table models and random models
  Start S; S.D = &D; S.P = &P; S.T = &T; S.logZbar0 = T.logZbar0;
  // G6 draws from pi_0 (core/cpp/v3_start.h:158-176), same serial stream
  {
    XsSource a; a.g.seed_stream(7, 200);
    XsSource4 b4; b4.g.seed_stream(7, 200);
    std::vector<int> S3; v4::Model S4m; bool o = true; int nd = full ? 20000 : 3000;
    for (int i = 0; o && i < nd; ++i) {
      v3::draw_pi0(st, a, S3);
      v4::Address ad; ad.particle = i + 1;
      S.draw_pi0(b4, ad, S4m);
      o = std::vector<int>(S4m.begin(), S4m.end()) == S3 && stk::same_bits(S.comp(v4::view(S4m)), st.comp(S3)) &&
          stk::same_bits(S.log_gamma0(v4::view(S4m)), st.log_gamma0(S3));
    }
    CHECK(o && a.g.count == b4.g.count, "pi_0 draws / comp differ: %s", t.c_str());
  }
  // G7 start mode (core/cpp/v3_start.h:178-305), every cap regime, every algorithm
  for (long cap : {1000000L, 2L, 3L, 5L, 17L, 1L})
    for (bool tie : {true, false}) {
      if (tie && cap < 2) continue;
      v3::ModeResult m3 = v3::start_mode(st, cap, tie);
      for (ModeAlgo al : {ModeAlgo::Auto, ModeAlgo::Enumerate, ModeAlgo::CountThenTieDP}) {
        if (al == ModeAlgo::CountThenTieDP && !tie && m3.truncated) continue;  // needs the enumeration (documented)
        ModeResult m4 = start_mode(D, P, T, cap, tie, al);
        bool o = std::vector<int>(m4.S.begin(), m4.S.end()) == m3.S && stk::same_bits(m4.lg0, m3.lg0) && m4.ties == m3.ties &&
                 m4.truncated == m3.truncated && m4.tie_dp_used == m3.tie_dp_used;
        CHECK(o, "start mode differs: %s cap=%ld tie=%d algo=%d (v3 ties=%ld trunc=%d)", t.c_str(), cap, (int)tie, (int)al, m3.ties, (int)m3.truncated);
      }
    }
}
void golden_ts(bool full) {
  for (auto& c : cases(full)) {
    Fixture F(c.d, c.n, c.p, c.seed); V3 R(F.D());
    int B = default_B(c.n, c.p);
    CorrOptions co; co.B = B; co.threads = stk::threads();
    CorrResult C = correlation_pass(F.D(), co);
    for (PartMode pm : {PartMode::Exact, PartMode::Truncated}) {
      if (pm == PartMode::Exact && c.p > 1500) continue;
      PartitionOptions po; po.mode = pm; po.B = B; po.threads = stk::threads();
      Partition P = make_partition(F.D(), C, po);
      golden_tables_start(F, R, P, tag(c) + (pm == PartMode::Exact ? " exact" : " truncated"), full);
    }
  }
}
}  // namespace
TEST(golden_G3to7_tables_stores_start_draws_mode, 0) { golden_ts(false); }
TEST(golden_G3to7_tables_stores_start_draws_mode_full, 1) { golden_ts(true); }

// ---- tie-heavy start-mode fixture: many duplicate signal columns, so |E| is large and the tie DP path is taken
TEST(golden_G7_start_mode_tie_heavy, 0) {
  for (int p : {60, 400}) {
    Fixture F(stk::TIE, 120, p, 77);
    // overwrite y with a sum of many duplicated columns (each duplicate pair is one tied choice in the mode)
    std::vector<double> X(F.own.X), y(F.n, 0.0);
    stk::Rng g(5);
    for (int j = 1, q = 0; j < p && q < 8; j += 7 * (p / 60), ++q) for (int i = 0; i < F.n; ++i) y[i] += ((j % 2) ? 1.5 : -1.5) * X[(size_t)j * F.n + i];
    for (int i = 0; i < F.n; ++i) y[i] += 0.5 * g.norm();
    double m = 0, s = 0; for (double v : y) m += v;
    m /= F.n; for (double& v : y) { v -= m; s += v * v; }
    s = std::sqrt(s / (F.n - 1)); for (double& v : y) v /= s;
    v4::DataOwner own; own.init(X.data(), y.data(), F.n, p);
    V3 R(own.D);
    int B = default_B(F.n, p);
    CorrOptions co; co.B = B; CorrResult C = correlation_pass(own.D, co);
    for (PartMode pm : {PartMode::Exact, PartMode::Truncated}) {
      PartitionOptions po; po.mode = pm; po.B = B;
      Partition P = make_partition(own.D, C, po);
      v3::Start st; st.D = &R.D; st.blocks = to_v3_blocks(P);
      v3::Scorer sc(&R.D); v3::build_tables(st, sc); v3::build_start(st);
      Tables T = build_tables(own.D, P, 2); build_start(own.D, P, T);
      for (long cap : {1000000L, 2L, 4L, 64L, 1000L})
        for (bool tie : {true, false}) {
          v3::ModeResult m3 = v3::start_mode(st, cap, tie);
          for (ModeAlgo al : {ModeAlgo::Auto, ModeAlgo::Enumerate, ModeAlgo::CountThenTieDP}) {
            if (al == ModeAlgo::CountThenTieDP && !tie && m3.truncated) continue;
            ModeResult m4 = start_mode(own.D, P, T, cap, tie, al);
            bool o = std::vector<int>(m4.S.begin(), m4.S.end()) == m3.S && stk::same_bits(m4.lg0, m3.lg0) && m4.ties == m3.ties &&
                     m4.truncated == m3.truncated && m4.tie_dp_used == m3.tie_dp_used;
            CHECK(o, "tie-heavy start mode differs: p=%d part=%d cap=%ld tie=%d algo=%d (v3 ties=%ld)", p, (int)pm, cap, (int)tie, (int)al, m3.ties);
          }
        }
      // the fixture must actually exercise ties
      long nt = v3::start_mode(st, 1000000, true).ties;
      std::printf("    tie-heavy p=%d part=%d: |E| = %ld\n", p, (int)pm, nt);
      CHECK(nt >= 16, "tie-heavy fixture has too few ties (p=%d)", p);
    }
  }
}
