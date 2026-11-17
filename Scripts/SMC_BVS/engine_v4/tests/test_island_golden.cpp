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
#include "v4/island/calib_runner.h"

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
  // calibration islands (phase_override: every event is PH_PILOT / PH_DIAG, so the phase is tracked here): a round
  // starts at particle 1's first order draw; a round preceded by resampling is bridge stage ev.stage, the following ones
  // are burn-in rounds 1..L, then measured rounds 1..Hm (addresses: MEASURED stage h, INTERFACES §3)
  bool calib = false; uint8_t role = R_FINAL, tier = 0, iter = 0; int L = 0;
  int kind = 0; uint32_t ustage = 0; int post = 0; bool resampled = false;
  double u(const char* purpose) override {
    ++n;
    const auto& ev = E->ev;
    Address a; a.seed = seed; a.role = role; a.tier = tier; a.iter = iter; a.island = island;
    if (std::strcmp(purpose, "resample") == 0) {
      if (ev.stage != res_stage) { res_stage = ev.stage; res_i = 0; }
      resampled = true;
      a.xph = X_RESAMPLE; a.stage = (uint32_t)ev.stage; a.particle = ++res_i; a.position = 0; a.slot = v4::slot_of(v4::SK_RESAMPLE, 0);
      return uniform_at(a);
    }
    auto cur = std::make_tuple(ev.phase, ev.stage, ev.round, ev.particle, ev.position);
    if (cur != last) { last = cur; order_d = 0; }
    if (calib) {
      if (std::strcmp(purpose, "order") == 0 && order_d == 0 && ev.particle == 1) {   // a new round
        if (resampled) { kind = 1; ustage = (uint32_t)ev.stage; resampled = false; }
        else { ++post; if (post <= L) { kind = 2; ustage = (uint32_t)post; } else { kind = 3; ustage = (uint32_t)(post - L); } }
      }
      static const uint8_t xk[4] = {X_INIT, X_BRIDGE, X_BURN, X_MEASURED};
      a.xph = xk[kind]; a.stage = kind == 0 ? 0 : ustage;
    } else switch (ev.phase) {
      case v3::PH_FINAL_INIT: a.xph = X_INIT; a.stage = 0; break;
      case v3::PH_FINAL_BRIDGE: a.xph = X_BRIDGE; a.stage = (uint32_t)ev.stage; break;
      case v3::PH_BURN_IN: a.xph = X_BURN; a.stage = (uint32_t)ev.round; break;
      case v3::PH_MEASURED: a.xph = X_MEASURED; a.stage = (uint32_t)ev.round; break;
      default: throw std::runtime_error("unexpected phase");
    }
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
  for (int variant = 0; variant < 3; ++variant) {   // variant 2: n = 12 (K = 6), the Gibbs cap is reached (review m6)
    int n = variant == 2 ? 12 : (variant ? 80 : 100), p = variant == 2 ? 60 : (variant ? 150 : 220), N = variant ? 40 : 30;
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
    uint64_t cap = 0; for (auto& sr : R.stages) cap += sr.moves.gibbs_cap; for (auto& tm : R.terminal_moves) cap += tm.gibbs_cap;
    if (variant == 2) CHECKF(cap > 0, "compat %d: the cap was never reached", variant);
    std::printf("  compat %d: logZ %.12f, %llu draws, store %zu, lead0 %zu, lead1 %zu, cap steps %llu\n", variant, R.logZ, (unsigned long long)R.stream_count,
                R.top_v.size(), R.lead0_v.size(), R.lead1_v.size(), (unsigned long long)cap);
  }
}

// ======================================================================================================================
// Calibration islands (WP3_DESIGN §1.11, agreed with WP4): the production runner (CalibIslandRunner, WP4's IslandRunner
// interface) against core's Engine::run_island_s with phase_override PH_PILOT / PH_DIAG -- one fresh v3 ledger per
// island, as WP4's CoreRunner (tests/golden/wp4_harness.cpp) -- over a calibration-like sequence: tier-0 pilot, two
// rebuilds of 4 diagnostic islands, tier-1 pilot.
//  * compat: core's v3 streams 0 / 1-4 / 5, continued across rebuilds (core/cpp/v3_core.cpp:593-596): every output and
//    the island's ledger (HPM + provenance incl. phi, logical counters, island_best, top / lead0 / lead1) in bits, and
//    the stream positions;
//  * law: core fed with the addressed uniforms (role PILOT / DIAG, tier e, iteration k, island r) through AddrSource,
//    against the particle-major kernel (1 thread) and the label-major kernel (3 threads, bit form);
//  * a numerical failure (scaled columns, consumed Gibbs flip): the ledger so far equals core's ledger after its throw
//    (the serial prefix), in compat and in law (label-major replays the prefix particle-major).
struct CoreCal {
  std::unique_ptr<v3::Ledger> L3; v3::IslandResult R3; bool failed = false; std::string msg; uint64_t pos0 = 0, pos1 = 0;
};
static CoreCal core_cal(const v3::Data& D3, const v3::Start& st3, const std::vector<std::vector<int>>& Nb3, int B, v3::VariateSource& src,
                        AddrSource* asrc, const v4::calib::IslandSpec& sp) {
  CoreCal c; c.L3.reset(new v3::Ledger(&D3, 4));
  v3::Engine E(D3, st3, Nb3, B); E.led = c.L3.get(); E.vs = &src; E.cache = nullptr;
  if (asrc) asrc->E = &E;
  const bool pilot = sp.role == v4::calib::IslandRole::Pilot;
  v3::Engine::Schedule sch; std::vector<double> g = sp.grid;
  if (pilot) { sch.adaptive = true; sch.H = sp.H; sch.Te = sp.Te; } else sch.grid = &g;
  try { c.R3 = E.run_island_s(pilot ? 0 : sp.island, sp.H, sch, sp.L, sp.Hm, sp.tier, nullptr, pilot ? v3::PH_PILOT : v3::PH_DIAG, sp.iter); }
  catch (const v3::NumericalFailure& e) { c.failed = true; c.msg = e.what(); }
  return c;
}
static bool same_store3(const std::set<v3::TopEntry, v3::TopCmp>& s3, const v4::Store& s) {
  if (s3.size() != s.size()) return false;
  size_t i = 0;
  for (auto it = s3.begin(); it != s3.end(); ++it, ++i) {
    v4::ModelView m = s.model(i);
    if (!same_bits(it->v, s.v[i]) || Model(it->S.begin(), it->S.end()) != Model(m.begin(), m.end())) return false;
  }
  return true;
}
static void compare_cal_ledger(const v3::Ledger& L3, const v4::Ledger& L, int r, const char* tag) {
  const v4::EventKey& k = L.hpm_ev.key; const v3::EventCtx& e = L3.hpm_ev;
  bool hok = L3.has_hpm == L.has_hpm && Model(L3.hpmS.begin(), L3.hpmS.end()) == L.hpmS && same_bits(L3.hpmF, L.hpmF) &&
             same_bits(L3.hpm_logm, L.hpm_logm) && L.hpm_ev.phase == e.phase && L.hpm_ev.mech == L3.hpm_mech && same_bits(L.hpm_ev.phi, e.phi) &&
             k.seg == v4::SG_CALIB && k.tier == e.tier && k.iter == e.iter && (int)k.unit == e.island && (int)k.stage == e.stage &&
             (int)k.round == e.round && (int)k.particle == e.particle && (int)k.position == e.position && k.sub == (L3.hpm_mech == v3::ME_GIBBS_FLIP ? 1 : 0);
  CHECKF(hok, "[%s] HPM: F %.17g vs %.17g, phase %d/%d, (tier %d iter %d unit %d stage %d round %d particle %d position %d phi %.17g) vs "
              "(%d %d %u %u %u %u %u %.17g)", tag, L3.hpmF, L.hpmF, e.phase, L.hpm_ev.phase, e.tier, e.iter, e.island, e.stage, e.round, e.particle,
              e.position, e.phi, k.tier, k.iter, k.unit, k.stage, k.round, k.particle, k.position, L.hpm_ev.phi);
  bool lok = true;
  for (int ph = 0; ph < N_PHASE; ++ph) for (int me = 0; me < N_MECH; ++me) if (L3.logical[ph][me] != L.logical[ph][me]) {
    lok = false; std::printf("  [%s] logical[%d][%d] %llu vs %llu\n", tag, ph, me, (unsigned long long)L3.logical[ph][me], (unsigned long long)L.logical[ph][me]); }
  CHECKF(lok, "[%s] logical counters", tag);
  bool ib = L.island_best.size() == 5;
  for (int u = 0; ib && u <= 4; ++u) ib = same_bits(u == r && r >= 1 ? L3.island_best[u] : -__builtin_huge_val(), L.island_best[u]);
  CHECKF(ib, "[%s] island_best (unit %d): %.17g vs %.17g", tag, r, r >= 1 ? L3.island_best[r] : 0.0, r >= 1 && L.island_best.size() > (size_t)r ? L.island_best[r] : 0.0);
  CHECKF(L.cfg.islands == 4 && L.cfg.leaders && L.cfg.p == (int)L3.D->p, "[%s] ledger configuration", tag);
  CHECKF(same_store3(L3.top.s, L.top), "[%s] top store (%zu vs %zu)", tag, L3.top.s.size(), L.top.size());
  CHECKF(same_store3(L3.lead0.s, L.lead0), "[%s] lead0 (%zu vs %zu)", tag, L3.lead0.s.size(), L.lead0.size());
  CHECKF(same_store3(L3.lead1.s, L.lead1), "[%s] lead1 (%zu vs %zu)", tag, L3.lead1.s.size(), L.lead1.size());
}
static void compare_cal(const CoreCal& c, const v4::calib::IslandOut& o, int r, bool rb_bits, const char* tag) {
  CHECKF(!c.failed && o.status == v4::Status::completed && !o.partial, "[%s] status: core failed %d, island %s '%s'", tag, (int)c.failed, v4::status_name(o.status), o.message.c_str());
  if (c.failed || o.status != v4::Status::completed) return;
  const v3::IslandResult& R3 = c.R3;
  bool ok = same_bits(R3.logZ, o.logZ) && R3.forced == o.forced && R3.phi.size() == o.schedule.size() && R3.phi.size() == o.stages.size();
  for (size_t t = 0; ok && t < R3.phi.size(); ++t) {
    const auto& s = o.stages[t]; const auto& m3 = R3.stage_moves[t];
    ok = same_bits(R3.phi[t], o.schedule[t]) && same_bits(R3.phi[t], s.phi) && same_bits(R3.inc[t], s.inc) && same_bits(R3.ess[t], s.ess) &&
         same_bits(R3.cum[t], s.cum) && R3.distinct_resampled[t] == s.distinct_res && R3.distinct_moved[t] == s.distinct_moved &&
         m3.gibbs == s.moves.gibbs && m3.gibbs_change == s.moves.gibbs_change && m3.us_acc == s.moves.us_acc && m3.ns_acc == s.moves.ns_acc && m3.in_acc == s.moves.in_acc;
  }
  CHECKF(ok, "[%s] logZ %.17g vs %.17g, forced %d vs %d, T %zu vs %zu / %zu", tag, R3.logZ, o.logZ, R3.forced, o.forced, R3.phi.size(), o.schedule.size(), o.stages.size());
  double w = 0; bool bits = o.pip.size() == R3.pip.size();
  for (size_t j = 0; bits && j < o.pip.size(); ++j) { w = std::max(w, std::fabs(o.pip[j] - R3.pip[j])); if (rb_bits && !same_bits(o.pip[j], R3.pip[j])) bits = false; }
  CHECKF(bits && w <= 1e-12, "[%s] PIP: %s, max deviation %.3e", tag, bits ? "sizes ok" : "not bit-identical", w);
  compare_cal_ledger(*c.L3, o.led, r, tag);
}
// the calibration sequence: tier-0 pilot, rebuilds 1 and 2 (4 diagnostic islands each), tier-1 pilot, tier-1 rebuild 1
// (review PR39 m5: tier-1 diagnostic streams 6-9 / addresses tier 1)
static std::vector<v4::calib::IslandSpec> cal_sequence(int H, int Te, int L, int Hm) {
  std::vector<v4::calib::IslandSpec> v;
  auto pilot = [&](int e) { v4::calib::IslandSpec s; s.role = v4::calib::IslandRole::Pilot; s.tier = e; s.iter = 0; s.island = 0; s.H = H; s.adaptive = true; s.Te = Te; s.L = L; s.Hm = Hm; return s; };
  v.push_back(pilot(0));
  const std::vector<std::vector<double>> grids = {{0.0, 0.05, 0.3, 1.0}, {0.0, 0.02, 0.1, 0.4, 1.0}};
  for (int k = 1; k <= 2; ++k) for (int r = 1; r <= 4; ++r) {
    v4::calib::IslandSpec s; s.role = v4::calib::IslandRole::Diag; s.tier = 0; s.iter = k; s.island = r; s.H = H; s.grid = grids[k - 1]; s.L = L; s.Hm = Hm;
    v.push_back(s);
  }
  v.push_back(pilot(1));
  for (int r = 1; r <= 4; ++r) {
    v4::calib::IslandSpec s; s.role = v4::calib::IslandRole::Diag; s.tier = 1; s.iter = 1; s.island = r; s.H = H; s.grid = grids[1]; s.L = L; s.Hm = Hm;
    v.push_back(s);
  }
  return v;
}

TEST(golden_calibration_islands_compat_vs_core) {
  Twin W(80, 150, 71, 5);
  const uint32_t seed = 23; const int B = 14;
  CalibRunnerConfig rc; rc.seed = seed; rc.compat = true; rc.kernel = KernelKind::ParticleMajor; rc.threads = 1; rc.B = B;
  CalibIslandRunner<Arith::Bit> run(W.D, W.st, W.nb, rc);
  std::map<int, v3::RngSource> streams;   // core's CalState streams (created at first use, continued)
  auto stream = [&](int k) -> v3::RngSource& { auto it = streams.find(k); if (it == streams.end()) { v3::RngSource g; g.g.seed_stream(seed, (uint64_t)k); it = streams.emplace(k, g).first; } return it->second; };
  int n = 0;
  for (const auto& sp : cal_sequence(40, 8, 2, 2)) {
    const bool pilot = sp.role == v4::calib::IslandRole::Pilot;
    const int sid = (sp.tier == 0 ? 0 : 5) + (pilot ? 0 : sp.island);   // core v3_core.cpp:626, 667
    v3::RngSource& rs = stream(sid);
    const uint64_t p0 = rs.g.count;
    CoreCal c = core_cal(W.D3, W.st3, W.Nb3, B, rs, nullptr, sp);
    v4::calib::IslandOut o = run.run(sp);
    char tag[64]; std::snprintf(tag, sizeof tag, "compat %s e%d k%d r%d", pilot ? "pilot" : "diag", sp.tier, sp.iter, sp.island);
    compare_cal(c, o, sp.island, true, tag);
    CHECKF(o.position_start == p0 && o.position_end == rs.g.count && o.init_hash == c.R3.init_hash, "[%s] stream positions %llu..%llu vs %llu..%llu, init hash", tag,
           (unsigned long long)o.position_start, (unsigned long long)o.position_end, (unsigned long long)p0, (unsigned long long)rs.g.count);
    ++n;
  }
  std::printf("  %d calibration islands (compat, streams 0-9 continued) = core, ledgers included\n", n);
}

TEST(golden_calibration_islands_law_vs_core) {
  Twin W(80, 150, 72, 5);
  const uint32_t seed = 29; const int B = 14;
  for (int kern = 0; kern < 2; ++kern) for (int th : {1, 3}) {   // review PR39 m5: both kernels at 1 and 3 threads
    CalibRunnerConfig rc; rc.seed = seed; rc.B = B; rc.kernel = kern ? KernelKind::LabelMajor : KernelKind::ParticleMajor;
    rc.threads = th; rc.G = 8; rc.tile = 64; rc.allow_test_kernels = true;
    CalibIslandRunner<Arith::Bit> run(W.D, W.st, W.nb, rc);
    int n = 0;
    for (const auto& sp : cal_sequence(40, 8, 2, 2)) {
      const bool pilot = sp.role == v4::calib::IslandRole::Pilot;
      AddrSource src; src.st3 = &W.st3; src.seed = seed; src.island = (uint32_t)sp.island; src.calib = true;
      src.role = pilot ? v4::R_PILOT : v4::R_DIAG; src.tier = (uint8_t)sp.tier; src.iter = (uint8_t)sp.iter; src.L = sp.L;
      CoreCal c = core_cal(W.D3, W.st3, W.Nb3, B, src, &src, sp);
      v4::calib::IslandOut o = run.run(sp);
      char tag[80]; std::snprintf(tag, sizeof tag, "law %s %dt %s e%d k%d r%d", kern ? "LM" : "PM", th, pilot ? "pilot" : "diag", sp.tier, sp.iter, sp.island);
      compare_cal(c, o, sp.island, false, tag);
      ++n;
    }
    std::printf("  [%s, %d thread%s] %d calibration islands (addressed: role, tier, iteration, island) = core\n", kern ? "label-major" : "particle-major", th, th > 1 ? "s" : "", n);
  }
}

// the ledger so far on a numerical failure (WP4 11-16): scaled columns (Cholesky, refactor and QR fail for any model
// containing them) that pi_0 never draws, so the failure is a consumed Gibbs flip inside a round
TEST(golden_calibration_failure_ledger_so_far) {
  Twin W(80, 150, 73, 5);
  const uint32_t seed = 31; const int B = 14;
  v4::calib::IslandSpec sp; sp.role = v4::calib::IslandRole::Diag; sp.tier = 0; sp.iter = 1; sp.island = 2; sp.H = 40;
  sp.grid = {0.0, 0.05, 0.3, 1.0}; sp.L = 2; sp.Hm = 2;
  // variant 0: the tables are unchanged, so the initial draw fails at the first particle whose pi_0 draw holds a scaled
  // column (the prefix: the INIT events of particles 1..i-1); variant 1: the tables exclude them, a Gibbs flip fails
  for (int variant = 0; variant < 2; ++variant) {
    const std::vector<int> bad = variant ? std::vector<int>{37, 101} : std::vector<int>{3, 18, 37, 52, 66, 81, 101, 117, 129, 144};
    auto own = std::make_shared<v4::DataOwned>();
    own->X.assign(W.D.Xs, W.D.Xs + (size_t)W.D.n * W.D.p); own->y.assign(W.D.ys, W.D.ys + W.D.n);
    for (int j : bad) for (int i = 0; i < W.D.n; ++i) own->X[(size_t)j * W.D.n + i] *= 1e200;
    v4::Data D2 = v4::make_data(own, W.D.n, W.D.p);
    v3::Data D3b; { std::vector<int> orig(W.D.p); for (int j = 0; j < W.D.p; ++j) orig[j] = j + 1; v3::data_init(D3b, D2.Xs, D2.ys, W.D.n, W.D.p, orig); }
    Start stv = W.st; v3::Start st3v = W.st3;
    if (variant) {
      for (int j : bad) { int b = stv.blk[j]; for (size_t code = 0; code < stv.logr[b].size(); ++code) if (code & (1u << stv.pos[j])) { stv.logr[b][code] = NEG_INF; st3v.logr[b][code] = NEG_INF; } }
      build_sampler(stv, W.D); v3::build_start(st3v);
    }
    std::printf("  variant %d (%s)\n", variant, variant ? "consumed Gibbs flip" : "initial draw");
    {   // compat
      CalibRunnerConfig rc; rc.seed = seed; rc.compat = true; rc.B = B;
      CalibIslandRunner<Arith::Bit> run(D2, stv, W.nb, rc);
      v3::RngSource rs; rs.g.seed_stream(seed, 2);
      CoreCal c = core_cal(D3b, st3v, W.Nb3, B, rs, nullptr, sp);
      v4::calib::IslandOut o = run.run(sp);
      CHECKF(c.failed && o.status == v4::Status::numerical_failure, "compat %d: core failed %d, island %s", variant, (int)c.failed, v4::status_name(o.status));
      std::printf("   compat island: %s\n", o.message.c_str());
      compare_cal_ledger(*c.L3, o.led, sp.island, "compat failure");
      CHECKF(o.position_end == rs.g.count, "compat %d: stream position %llu vs %llu", variant, (unsigned long long)o.position_end, (unsigned long long)rs.g.count);
    }
    // law: particle-major 1 and 3 threads, label-major 3 threads, against core with the addressed uniforms
    for (int kern = 0; kern < 2; ++kern) for (int th : {1, 3}) {
      if (kern == 1 && th == 1) continue;
      CalibRunnerConfig rc; rc.seed = seed; rc.B = B; rc.kernel = kern ? KernelKind::LabelMajor : KernelKind::ParticleMajor; rc.threads = th; rc.G = 8; rc.tile = 64;
      rc.allow_test_kernels = true;
      CalibIslandRunner<Arith::Bit> run(D2, stv, W.nb, rc);
      AddrSource src; src.st3 = &st3v; src.seed = seed; src.island = (uint32_t)sp.island; src.calib = true; src.role = v4::R_DIAG; src.tier = 0; src.iter = 1; src.L = sp.L;
      CoreCal c = core_cal(D3b, st3v, W.Nb3, B, src, &src, sp);
      v4::calib::IslandOut o = run.run(sp);
      char tag[64]; std::snprintf(tag, sizeof tag, "law failure %d %s %d threads", variant, kern ? "LM" : "PM", th);
      CHECKF(c.failed && o.status == v4::Status::numerical_failure, "[%s] core failed %d, island %s", tag, (int)c.failed, v4::status_name(o.status));
      compare_cal_ledger(*c.L3, o.led, sp.island, tag);
      if (kern == 1) std::printf("   [%s] %s; ledger so far: %zu stored, INIT events %llu, flips %llu\n", tag, o.message.c_str(), o.led.top.size(),
                                 (unsigned long long)o.led.logical[v4::PH_DIAG][ME_INIT], (unsigned long long)o.led.logical[v4::PH_DIAG][ME_GIBBS_FLIP]);
    }
  }
}
