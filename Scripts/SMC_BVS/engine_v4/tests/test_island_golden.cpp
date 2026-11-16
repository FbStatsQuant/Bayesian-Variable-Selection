// test_island_golden.cpp -- WP3 golden tests against core/ (revision D) compiled UNCHANGED with the v3 flags.
//
// 1. Tables and logZbar0 of the stand-in start law equal core's build_tables / build_start bits.
// 2. Flip scores (bit form, both entry points) equal v3::Scorer::score bits, every label, k = 0..12.
// 3. A whole island: core's Engine::run_island (particle-serial, v3 Ledger without cache) fed with the SAME addressed
//    uniforms (an adapter maps core's serial variate requests to INTERFACES §3 addresses through Engine::ev) against
//    run_island<Bit> with the particle-major and the label-major kernel. Every output is compared: log Z, stage table,
//    move statistics, distinct counts, init hash, HPM + provenance, island_best, logical counters and the top store in
//    bits; RB arrays and PIPs to 1e-12 relative (class A: the island sums them exactly in fixed point, core in double).
#include <cstring>
#include <random>
#include <set>
// core/cpp/v3_runtime.h uses three R symbols in one helper the tests never call; shim them (core/ stays untouched).
typedef void* SEXP;
inline bool Rf_isNull(SEXP x) { return x == nullptr; }
namespace Rcpp { template <class T> struct XPtr { T* p; explicit XPtr(SEXP x) : p((T*)x) {} T* get() { return p; } }; }
#include "v3_engine.h"
#include "tk.h"
#include "tutil_island.h"
#include "v4/island/island.h"

using namespace v4::island;

struct Twin {
  Data D; Start st; Neighbours nb;
  v3::Data D3; v3::Start st3; std::vector<std::vector<int>> Nb3;
  Twin(int n, int p, uint64_t seed, int bsz) {
    make_ar_data(D, n, p, 0.6, seed);
    auto blocks = contiguous_blocks(p, bsz);
    build_start(st, D, blocks);
    nb = window_neighbours(D, 14, 8);
    std::vector<int> orig(p); for (int j = 0; j < p; ++j) orig[j] = j + 1;
    v3::data_init(D3, D.Xs, D.ys, n, p, orig);
    st3.D = &D3; st3.blocks = blocks;
    v3::Scorer sc3(&D3); v3::build_tables(st3, sc3); v3::build_start(st3);
    Nb3.assign(p, {}); for (int j = 0; j < p; ++j) for (int64_t e = nb.ptr[j]; e < nb.ptr[j + 1]; ++e) Nb3[j].push_back(nb.idx[e]);
  }
};

TEST(golden_data_and_tables) {
  Twin W(100, 240, 31, 4);
  CHECK(same_bits(W.D.logm0, W.D3.logm0) && same_bits(W.D.logCn, W.D3.logCn) && same_bits(W.D.logWK, W.D3.logWK) && same_bits(W.D.yty, W.D3.yty));
  bool ok = true;
  for (int j = 0; j < W.D.p; ++j) ok = ok && same_bits(W.D.z[j], W.D3.z[j]) && same_bits(W.D.diagG[j], W.D3.Gat(j, j)) && W.D.zob.key[j] == W.D3.zob.key[j];
  for (int k = 0; k <= W.D.K; ++k) ok = ok && same_bits(W.D.logprior[k], W.D3.logprior[k]);
  CHECK(ok);
  bool tok = W.st.J == W.st3.J && same_bits(W.st.logZbar0, W.st3.logZbar0);
  for (int b = 0; b < W.st.J && tok; ++b)
    for (size_t c = 0; c < W.st.logr[b].size(); ++c) tok = tok && same_bits(W.st.logr[b][c], W.st3.logr[b][c]);
  for (size_t k = 0; k < W.st.size_cum.size() && tok; ++k) tok = same_bits(W.st.size_cum[k], W.st3.size_cum[k]);
  CHECK(tok);
}

TEST(golden_flip_scores_vs_core_scorer) {
  Twin W(150, 500, 32, 4);
  v3::Scorer sc3(&W.D3); BitScorer sc(&W.D);
  std::mt19937_64 g(77);
  long checked = 0, mism = 0;
  for (int rep = 0; rep < 26; ++rep) {
    int k = rep % 13;
    Model S;
    while ((int)S.size() < k) { int j = (int)(g() % W.D.p); if (!contains(S, j)) sorted_insert(S, j); }
    std::vector<int> S3(S.begin(), S.end());
    double lm = sc3.score(S3).logm, c = W.st3.comp(S3);
    CHECK(same_bits(lm, sc.score(S).logm));
    SupportCache s; build_support(W.D, W.st, sc, s, S, zobrist(W.D, S), lm, W.D.logprior[k] + c, (lm - W.D.logm0) - c, 0.5);
    for (int j = 0; j < W.D.p; ++j) {
      std::vector<int> T3 = S3; if (contains(S, j)) v3::sorted_erase(T3, j); else v3::sorted_insert(T3, j);
      double ref = sc3.score(T3).logm, l1, o1;
      eval1<Arith::Bit>(W.D, W.st, sc, s, j, l1, o1);
      ++checked; if (!same_bits(ref, l1)) ++mism;
    }
  }
  std::printf("  %ld flip scores vs v3::Scorer: %ld mismatches\n", checked, mism);
  CHECK(mism == 0);
}

// core's serial variate requests -> INTERFACES v0.1.5 §3 addresses (reads the engine's event context). The pi_0
// block indices are recovered by replaying core's own size draws (core/cpp/v3_start.h:158-176) on core's tables.
struct AddrSource : public v3::VariateSource {
  v3::Engine* E = nullptr; const v3::Start* st3 = nullptr; uint32_t seed = 0, island = 0;
  std::tuple<int, int, int, int, int> last{-1, -1, -1, -1, -1}; uint32_t order_d = 0;
  int res_stage = -1; uint32_t res_i = 0; uint64_t n = 0;
  int pi_r = 0, pi_b = 0; std::vector<int> kb; size_t sub_next = 0;   // pi_0 replay state
  double u(const char* purpose) override {
    ++n;
    const auto& ev = E->ev;
    Address a; a.seed = seed; a.role = R_FINAL; a.island = island;
    if (std::strcmp(purpose, "resample") == 0) {
      if (ev.stage != res_stage) { res_stage = ev.stage; res_i = 0; }
      a.xph = X_RESAMPLE; a.stage = (uint32_t)ev.stage; a.particle = ++res_i; a.position = 0; a.slot = v4::slot_of(v4::SK_RESAMPLE, 0);
      return uniform_at(a);
    }
    switch (ev.phase) {
      case v3::PH_FINAL_INIT: a.xph = X_INIT; a.stage = 0; break;
      case v3::PH_FINAL_BRIDGE: a.xph = X_BRIDGE; a.stage = (uint32_t)ev.stage; break;
      case v3::PH_BURN_IN: a.xph = X_BURN; a.stage = (uint32_t)ev.round; break;
      case v3::PH_MEASURED: a.xph = X_MEASURED; a.stage = (uint32_t)ev.round; break;
      default: throw std::runtime_error("unexpected phase");
    }
    auto cur = std::make_tuple(ev.phase, ev.stage, ev.round, ev.particle, ev.position);
    if (cur != last) { last = cur; order_d = 0; }
    a.particle = (uint32_t)ev.particle; a.position = (uint32_t)ev.position;
    std::string pu = purpose; double val;
    if (pu == "order") { a.slot = v4::slot_of(v4::SK_ORDER, order_d++); return uniform_at(a); }
    if (pu == "gibbs" || pu == "uswap_accept" || pu == "nswap_accept" || pu == "indep_accept") { a.slot = v4::SLOT_ACCEPT; return uniform_at(a); }
    if (pu == "uswap_j" || pu == "nswap_j") { a.slot = v4::slot_of(v4::SK_MOVE_J, 0); return uniform_at(a); }
    if (pu == "uswap_l" || pu == "nswap_l") { a.slot = v4::slot_of(v4::SK_MOVE_L, 0); return uniform_at(a); }
    if (pu == "pi0_size") {
      a.slot = v4::slot_of(v4::SK_PI0_SIZE, 0); val = uniform_at(a);
      pi_r = v3::cat_draw_gt(st3->size_cum, val); pi_b = st3->J - 1; kb.assign(st3->J, 0); sub_next = 0;
      return val;
    }
    if (pu == "pi0_block_size") {
      int b = pi_b--; a.slot = v4::slot_of(v4::SK_PI0_BLOCKSIZE, (uint32_t)b); val = uniform_at(a);
      int j = v3::cat_draw_gt(st3->cond_cum[b][pi_r], val); kb[b] = j; pi_r -= j;
      return val;
    }
    if (pu == "pi0_submodel") {
      while (sub_next < kb.size() && kb[sub_next] == 0) ++sub_next;
      a.slot = v4::slot_of(v4::SK_PI0_SUBMODEL, (uint32_t)sub_next++); return uniform_at(a);
    }
    throw std::runtime_error("unknown purpose " + pu);
  }
};

static void compare_island(const v3::IslandResult& R3, const v3::Ledger& L3, const IslandRun& R, int r, const char* tag) {
  bool ok = same_bits(R3.logZ, R.logZ) && R3.init_hash == R.init_hash && R3.phi.size() == R.stages.size();
  CHECKF(ok, "[%s] logZ %.17g vs %.17g, init hash %d, T %zu vs %zu", tag, R3.logZ, R.logZ, (int)(R3.init_hash == R.init_hash), R3.phi.size(), R.stages.size());
  for (size_t t = 0; t < std::min(R3.phi.size(), R.stages.size()); ++t) {
    const auto& s = R.stages[t]; const auto& m3 = R3.stage_moves[t];
    bool st_ok = same_bits(R3.phi[t], s.phi) && same_bits(R3.inc[t], s.inc) && same_bits(R3.ess[t], s.ess) && same_bits(R3.cum[t], s.cum) &&
                 R3.distinct_resampled[t] == s.distinct_res && R3.distinct_moved[t] == s.distinct_moved;
    bool mv_ok = m3.gibbs == s.moves.gibbs && m3.gibbs_change == s.moves.gibbs_change && m3.us_exec == s.moves.us_exec && m3.us_acc == s.moves.us_acc &&
                 m3.us_self == s.moves.us_self && m3.ns_exec == s.moves.ns_exec && m3.ns_acc == s.moves.ns_acc && m3.ns_noscore == s.moves.ns_noscore &&
                 m3.ns_self == s.moves.ns_self && m3.in_exec == s.moves.in_exec && m3.in_acc == s.moves.in_acc;
    CHECKF(st_ok && mv_ok, "[%s] stage %zu: table %d moves %d (gibbs_change %llu vs %llu)", tag, t + 1, (int)st_ok, (int)mv_ok,
              (unsigned long long)m3.gibbs_change, (unsigned long long)s.moves.gibbs_change);
  }
  CHECK(R3.terminal_moves.size() == R.terminal_moves.size());
  for (size_t t = 0; t < std::min(R3.terminal_moves.size(), R.terminal_moves.size()); ++t) {
    CHECK(R3.terminal_moves[t].gibbs_change == R.terminal_moves[t].gibbs_change && R3.terminal_moves[t].us_acc == R.terminal_moves[t].us_acc &&
          R3.terminal_moves[t].ns_acc == R.terminal_moves[t].ns_acc && R3.terminal_moves[t].in_acc == R.terminal_moves[t].in_acc &&
          R3.terminal_distinct[t] == R.terminal_distinct[t]);
  }
  double wrb = 0;
  for (size_t j = 0; j < R.rb_acc.size(); ++j) {
    wrb = std::max(wrb, std::fabs(R3.rb_acc[j] - R.rb_acc[j]) / std::max(1.0, std::fabs(R3.rb_acc[j])));
    wrb = std::max(wrb, std::fabs(R3.pip[j] - R.pip[j]));
    for (size_t h = 0; h < R.rb_round.size(); ++h) wrb = std::max(wrb, std::fabs(R3.rb_round[h][j] - R.rb_round[h][j]) / std::max(1.0, std::fabs(R3.rb_round[h][j])));
  }
  CHECKF(wrb <= 1e-12, "[%s] RB/PIP max deviation %.3e", tag, wrb);
  // ledger
  std::vector<int> h3(L3.hpmS.begin(), L3.hpmS.end());
  bool hok = L3.has_hpm == R.hpm.has && Model(h3.begin(), h3.end()) == R.hpm.S && same_bits(L3.hpmF, R.hpm.F) && same_bits(L3.hpm_logm, R.hpm.logm) &&
             L3.hpm_ev.phase == R.hpm.phase && L3.hpm_mech == R.hpm.mech && (uint32_t)L3.hpm_ev.stage == R.hpm.key.stage &&
             (uint32_t)L3.hpm_ev.round == R.hpm.key.round && (uint32_t)L3.hpm_ev.particle == R.hpm.key.particle && (uint32_t)L3.hpm_ev.position == R.hpm.key.position;
  // m6e: the key's xph (from the phase) and the within-step ordinal sub (flip 1, else 0)
  uint8_t xph_exp = L3.hpm_ev.phase == v3::PH_FINAL_INIT ? X_INIT : L3.hpm_ev.phase == v3::PH_FINAL_BRIDGE ? X_BRIDGE : L3.hpm_ev.phase == v3::PH_BURN_IN ? X_BURN : X_MEASURED;
  hok = hok && R.hpm.key.xph == xph_exp && R.hpm.key.sub == (L3.hpm_mech == v3::ME_GIBBS_FLIP ? 1 : 0) && R.hpm.key.seg == v4::SG_FINAL && R.hpm.key.unit == (uint32_t)r;
  CHECKF(hok, "[%s] HPM F %.17g vs %.17g; ev (%d,%d,%d,%d,%d) vs (%d,%u,%u,%u,%u)", tag, L3.hpmF, R.hpm.F, L3.hpm_ev.phase, L3.hpm_ev.stage,
            L3.hpm_ev.round, L3.hpm_ev.particle, L3.hpm_ev.position, R.hpm.phase, R.hpm.key.stage, R.hpm.key.round, R.hpm.key.particle, R.hpm.key.position);
  CHECK(same_bits(L3.island_best[r], R.island_best));
  bool lok = true;
  for (int ph = 0; ph < N_PHASE; ++ph) for (int me = 0; me < N_MECH; ++me) if (L3.logical[ph][me] != R.logical[ph][me]) {
    lok = false; std::printf("  [%s] logical[%d][%d] %llu vs %llu\n", tag, ph, me, (unsigned long long)L3.logical[ph][me], (unsigned long long)R.logical[ph][me]); }
  CHECK(lok);
  bool sok = L3.top.s.size() == R.top_v.size(); size_t i = 0;
  for (auto it = L3.top.s.begin(); sok && it != L3.top.s.end(); ++it, ++i) {
    Model S(it->S.begin(), it->S.end());
    sok = same_bits(it->v, R.top_v[i]) && S == Model(R.top_pool.begin() + R.top_off[i], R.top_pool.begin() + R.top_off[i] + R.top_len[i]);
  }
  CHECKF(sok, "[%s] top store: sizes %zu vs %zu, first difference at %zu", tag, L3.top.s.size(), R.top_v.size(), i);
}

TEST(golden_island_vs_core_engine) {
  for (int variant = 0; variant < 2; ++variant) {
    int n = variant ? 80 : 100, p = variant ? 150 : 220, N = variant ? 40 : 30;
    Twin W(n, p, 40 + variant, variant ? 5 : 4);
    std::vector<double> grid = variant ? std::vector<double>{0.0, 0.02, 0.1, 0.3, 0.6, 1.0} : std::vector<double>{0.0, 0.1, 0.4, 1.0};
    int L = 2, Hm = 2, B = 14, r = 2; uint32_t seed = 9 + variant;
    // core
    v3::Engine E(W.D3, W.st3, W.Nb3, B);
    v3::Ledger L3(&W.D3, 4);
    AddrSource src; src.E = &E; src.st3 = &W.st3; src.seed = seed; src.island = (uint32_t)r;
    E.led = &L3; E.vs = &src; E.cache = nullptr;
    v3::IslandResult R3 = E.run_island(r, N, grid, L, Hm, 0, nullptr);
    std::printf("  core island: logZ %.12f, %llu uniforms, store %zu, HPM |S| %zu\n", R3.logZ, (unsigned long long)src.n, L3.top.s.size(), L3.hpmS.size());
    // island
    IslandConfig c; c.allow_test_kernels = true; c.seed = seed; c.island = (uint32_t)r; c.N = N; c.grid = grid; c.L = L; c.Hm = Hm; c.B = B;
    for (int kern = 0; kern < 2; ++kern) {
      c.kernel = kern ? KernelKind::LabelMajor : KernelKind::ParticleMajor; c.threads = kern ? 3 : 1; c.G = 8; c.tile = 64;
      IslandRun R = run_island<Arith::Bit>(W.D, W.st, W.nb, c);
      compare_island(R3, L3, R, r, kern ? "label-major" : "particle-major");
    }
  }
}


// COMPAT (manager Q2; the <= 5k bit anchor): the island with core's serial v3 stream 9 + r (WP1 CompatSource), the
// particle-major bit path and core's double RB sum, against core's Engine::run_island with its own RngSource on the same
// stream: every output in bits (RB, rb_round and PIPs included) and the stream position at the end. The leader stores
// (not outputs: INTERFACES v0.1.7) are compared too, with the test-only option `leaders`.
TEST(golden_compat_island_vs_core_serial_stream) {
  for (int variant = 0; variant < 2; ++variant) {
    int n = variant ? 80 : 100, p = variant ? 150 : 220, N = variant ? 40 : 30;
    Twin W(n, p, 60 + variant, variant ? 5 : 4);
    std::vector<double> grid = variant ? std::vector<double>{0.0, 0.02, 0.1, 0.3, 0.6, 1.0} : std::vector<double>{0.0, 0.1, 0.4, 1.0};
    int L = 2, Hm = 3, B = 14, r = 3; uint32_t seed = 17 + variant;
    v3::Engine E(W.D3, W.st3, W.Nb3, B);
    v3::Ledger L3(&W.D3, 4);
    v3::RngSource src; src.g.seed_stream(seed, 9 + r);
    E.led = &L3; E.vs = &src; E.cache = nullptr;
    v3::IslandResult R3 = E.run_island(r, N, grid, L, Hm, 0, nullptr);
    IslandConfig c; c.compat = true; c.leaders = true; /* test-only: compares core's leader stores */ c.kernel = KernelKind::ParticleMajor; c.threads = 1; c.seed = seed; c.island = (uint32_t)r;
    c.N = N; c.grid = grid; c.L = L; c.Hm = Hm; c.B = B;
    IslandRun R = run_island<Arith::Bit>(W.D, W.st, W.nb, c);
    compare_island(R3, L3, R, r, "compat");
    bool rb_bits = R.rb_acc.size() == R3.rb_acc.size();
    for (size_t j = 0; rb_bits && j < R.rb_acc.size(); ++j) {
      rb_bits = same_bits(R.rb_acc[j], R3.rb_acc[j]) && same_bits(R.pip[j], R3.pip[j]);
      for (size_t h = 0; rb_bits && h < R.rb_round.size(); ++h) rb_bits = same_bits(R.rb_round[h][j], R3.rb_round[h][j]);
    }
    CHECKF(rb_bits, "compat %d: RB / rb_round / PIP not bit-identical", variant);
    auto same_store = [](const std::set<v3::TopEntry, v3::TopCmp>& s3, const std::vector<double>& v, const std::vector<uint64_t>& off,
                         const std::vector<uint16_t>& len, const std::vector<int32_t>& pool) {
      if (s3.size() != v.size()) return false;
      size_t i = 0;
      for (auto it = s3.begin(); it != s3.end(); ++it, ++i) {
        Model S(it->S.begin(), it->S.end());
        if (!same_bits(it->v, v[i]) || S != Model(pool.begin() + off[i], pool.begin() + off[i] + len[i])) return false;
      }
      return true;
    };
    CHECKF(same_store(L3.lead0.s, R.lead0_v, R.lead0_off, R.lead0_len, R.lead0_pool), "compat %d: lead0 (%zu vs %zu)", variant, L3.lead0.s.size(), R.lead0_v.size());
    CHECKF(same_store(L3.lead1.s, R.lead1_v, R.lead1_off, R.lead1_len, R.lead1_pool), "compat %d: lead1 (%zu vs %zu)", variant, L3.lead1.s.size(), R.lead1_v.size());
    CHECKF(src.g.count == R.stream_count, "compat %d: stream position %llu vs %llu", variant, (unsigned long long)src.g.count, (unsigned long long)R.stream_count);
    std::printf("  compat %d: logZ %.12f, %llu draws, store %zu, lead0 %zu, lead1 %zu\n", variant, R.logZ, (unsigned long long)R.stream_count,
                R.top_v.size(), R.lead0_v.size(), R.lead1_v.size());
  }
}
