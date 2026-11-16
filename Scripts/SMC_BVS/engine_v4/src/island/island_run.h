// island_run.h -- the island engine: configuration checks, run loop (initial draws, stages, terminal rounds), stage
// barrier (reweight, resample), ledger sync and store compaction at step boundaries, memory re-check, checkpoints,
// the ledger so far of calibration islands, outputs; plan_island and run_island. The two kernels are member
// functions defined out of class: island_pm.h (the shared U / N / I steps, the round order, the particle-major
// reference) and island_lm.h (the label-major round); their group state is island_lm_state.h. island_impl.h
// includes all of them (the file split of WP3_ARCH_REVIEW §4: mechanical, no logic change).
#pragma once
#include <malloc.h>
#include <mutex>
#include <omp.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstdio>
#include <filesystem>
#include <memory>
#include "v4/island/island.h"
#include "v4/provenance.h"
#include "island_lm_state.h"

namespace v4::island {

using u128 = unsigned __int128;
inline uint64_t fix63(double o) { return (uint64_t)(o * 0x1.0p63); }   // o in [0, 1]
inline double unfix63(u128 a) { return (double)a * 0x1.0p-63; }

// INTERFACES v0.1.5 §3 slot kinds (rng.h): SK_ORDER, SK_RESAMPLE, SK_PI0_*, SK_MOVE_J, SK_MOVE_L, SK_ACCEPT
using v4::slot_of; using v4::SLOT_ACCEPT;
static const uint32_t SLOT_MOVE_J = v4::slot_of(v4::SK_MOVE_J, 0), SLOT_MOVE_L = v4::slot_of(v4::SK_MOVE_L, 0),
                      SLOT_RESAMPLE = v4::slot_of(v4::SK_RESAMPLE, 0);

// core/cpp/v3_calib.h:11-46 (lse_cal, population_ess, pilot_next_phi), copied; used only by the adaptive schedule
// option (benchmarks and pilot-like grids; the calibration itself is WP4's).
inline double lse_cal(const std::vector<double>& x) {
  double m = NEG_INF; for (double v : x) if (v > m) m = v;
  if (!std::isfinite(m)) return m;
  long double s = 0.0L; for (double v : x) s += pm::exp(v - m);
  return m + pm::log((double)s);
}
inline double population_ess(const std::vector<double>& d, double delta) {
  std::vector<double> x(d.size()), x2(d.size());
  for (size_t i = 0; i < d.size(); ++i) { x[i] = delta * d[i]; x2[i] = 2 * x[i]; }
  return pm::exp(2 * lse_cal(x) - lse_cal(x2));
}
struct NextPhi { double phi; bool forced; };
inline NextPhi pilot_next_phi(const std::vector<double>& d, double phi, double H, int Te) {
  const double thr = 0.90 * H;
  if (population_ess(d, 1.0 - phi) >= thr) return {1.0, false};
  double lo = phi, hi = 1.0;
  for (int i = 0; i < 60; ++i) {
    double mid = 0.5 * (lo + hi);
    if (population_ess(d, mid - phi) >= thr) lo = mid; else hi = mid;
  }
  if (lo - phi < 1.0 / Te) {
    double f = std::min(1.0, phi + 1.0 / Te);
    if (f >= 1.0 - 1e-12) f = 1.0;
    return {f, true};
  }
  return {lo, false};
}   // INTERFACES v0.1.2 §3 (I step accept)

struct Fnv { uint64_t h = 0xcbf29ce484222325ULL;
  void bytes(const void* p, size_t n) { const unsigned char* c = (const unsigned char*)p; for (size_t i = 0; i < n; ++i) { h ^= c[i]; h *= 0x100000001b3ULL; } }
  template <class T> void pod(const T& x) { bytes(&x, sizeof(T)); }
  template <class T> void vec(const std::vector<T>& v) { uint64_t n = v.size(); pod(n); if (n) bytes(v.data(), n * sizeof(T)); }
};

#ifdef V4_ISLAND_DEFINE_COMMON
uint64_t IslandRun::hash() const {
  Fnv f;
  f.pod(status); f.pod(r); f.pod(N); f.pod(T); f.pod(L); f.pod(Hm); f.pod(p); f.pod(logZ); f.pod(init_hash);
  for (auto& s : stages) { f.pod(s.phi); f.pod(s.inc); f.pod(s.ess); f.pod(s.cum); f.pod(s.distinct_res); f.pod(s.distinct_moved); f.pod(s.moves); }
  for (auto& m : terminal_moves) f.pod(m);
  f.vec(terminal_distinct); f.vec(rb_acc); f.vec(pip);
  for (auto& v : rb_round) f.vec(v);
  f.bytes(logical, sizeof(logical)); f.pod(island_best);
  f.pod(hpm.has); f.vec(hpm.S); f.pod(hpm.F); f.pod(hpm.logm); f.pod(hpm.key.seg); f.pod(hpm.key.tier); f.pod(hpm.key.iter); f.pod(hpm.key.unit); f.pod(hpm.key.xph); f.pod(hpm.key.stage); f.pod(hpm.key.round); f.pod(hpm.key.particle); f.pod(hpm.key.position); f.pod(hpm.key.sub); f.pod(hpm.phase); f.pod(hpm.mech);
  f.vec(top_v); f.vec(top_hash); f.vec(top_len); f.vec(top_pool);
  for (auto& m : terminal) f.vec(m);
  if (compat) f.pod(stream_count);
  if (leaders) { f.vec(lead0_v); f.vec(lead0_len); f.vec(lead0_pool); f.vec(lead1_v); f.vec(lead1_len); f.vec(lead1_pool); }
  return f.h;
}

v4::IslandResult to_record(const IslandRun& r) {
  v4::IslandResult o;
  if (r.status == 1) throw v4::Error(v4::Status::internal_error, "to_record: an interrupted island (stop_after_step) has no record");
  o.status = r.status == 0 ? v4::Status::completed : (r.status == 2 ? v4::Status::numerical_failure : v4::Status::resource_limit);
  o.r = r.r; o.N = r.N; o.T = r.T; o.L = r.L; o.Hm = r.Hm; o.logZ = r.logZ; o.init_hash = r.init_hash;
  o.stages = r.stages; o.terminal_moves = r.terminal_moves; o.terminal_distinct = r.terminal_distinct;
  o.rb_acc = r.rb_acc; o.pip = r.pip; o.rb_round = r.rb_round;
  // calibration islands (WP3_DESIGN §1.11): the calibration ledger's configuration (islands 4, leaders on, caps 40p + 1,
  // 20p, 20p; Ledger::merge refuses a mismatch); the pilot (unit 0) has no island_best of its own (core v3_ledger.h:106)
  const bool calib = r.role != IslandRole::Final;
  v4::LedgerConfig lc; lc.p = r.p; lc.islands = calib ? 4 : std::max(1, r.r); lc.leaders = calib; lc.fresh_counters = false;
  o.led.init(lc);
  o.led.has_hpm = r.hpm.has; o.led.hpmS = r.hpm.S; o.led.hpmF = r.hpm.F; o.led.hpm_logm = r.hpm.logm;
  o.led.hpm_ev.phase = r.hpm.phase; o.led.hpm_ev.mech = r.hpm.mech; o.led.hpm_ev.key = r.hpm.key;
  // phi of the HPM event (core's EventCtx::phi): 0 at the initial draw, phi_t in bridge stage t, 1 in the terminal rounds
  if (r.hpm.has) {
    const EventKey& k = r.hpm.key;
    o.led.hpm_ev.phi = k.xph == X_INIT ? 0.0 : k.xph == X_BRIDGE ? (k.stage < r.grid.size() ? r.grid[k.stage] : 0.0) : 1.0;
  }
  std::memcpy(o.led.logical, r.logical, sizeof(r.logical));
  if (r.r >= 1 && (size_t)r.r < o.led.island_best.size()) o.led.island_best[r.r] = r.island_best;
  for (size_t i = 0; i < r.top_v.size(); ++i) o.led.top.offer(r.top_v[i], v4::ModelView(r.top_pool.data() + r.top_off[i], r.top_len[i]), r.top_hash[i]);
  if (calib) {
    for (size_t i = 0; i < r.lead0_v.size(); ++i) o.led.lead0.offer(r.lead0_v[i], v4::ModelView(r.lead0_pool.data() + r.lead0_off[i], r.lead0_len[i]), r.lead0_hash[i]);
    for (size_t i = 0; i < r.lead1_v.size(); ++i) o.led.lead1.offer(r.lead1_v[i], v4::ModelView(r.lead1_pool.data() + r.lead1_off[i], r.lead1_len[i]), r.lead1_hash[i]);
  }
  o.led.compact();
  o.t.total = r.ks.t_total;
  return o;
}
#endif

// ---------------------------------------------------------------------------------------------------------------
// Checkpoint container (provisional: magic, generation, length, FNV-1a checksum, streamed payload; WP1's kind-8 file
// with SHA-256 sections may replace it). Streaming I/O: IslandEngine::save_ckpt / load_ckpt.
// ---------------------------------------------------------------------------------------------------------------
static const char kCkptMagic[8] = {'S', 'M', 'C', 'V', '4', 'C', 'K', 'P'};

// ---------------------------------------------------------------------------------------------------------------
template <Arith A>
class IslandEngine {
 public:
  const Data& D; const Start& st; const Neighbours& nb; IslandConfig cfg;
  int p, m, NT;
  std::vector<Particle> P;
  TopStore top;
  std::vector<std::unique_ptr<ThreadLedger>> tl;   // one per thread
  ThreadLedger master;                             // merged at every step boundary
  std::vector<std::unique_ptr<BitScorer>> scorers;
  std::vector<u128> rb_cur, rb_tot;
  std::vector<std::vector<u128>> rb_thread;        // particle-major reference with threads
  IslandRun res;
  // tiled row-major copy of X for the label-major products: tile t holds columns [t*Bk, t*Bk + Bk) as n rows of Bk
  std::vector<avec<double>> scratch_P;              // per-thread product buffers, grown on demand, kept across passes
  avec<double> Xt; int Bk = 128, ntile = 0;
  // compat (manager Q2): every uniform is the next draw of the island's v3 stream, in core's serial call order. The
  // stream is the caller's (calibration roles: WP4 keeps streams 0-9 across rebuilds) or the island's own (final 9 + r).
  std::unique_ptr<v4::CompatSource> csrc_own;
  v4::CompatSource* csrc = nullptr;
  TopStore lead0, lead1;
  std::vector<double> rb_d;   // compat: core's cumulative double RB accumulator (core/cpp/v3_engine.h:128, :350-364)
  inline double U(const Address& a) { return csrc ? csrc->u(a) : uniform_at(a); }
  double logZ = 0; double k_est = 8; MemSizes msz;
  KernelStats ks_prev;   // verbose per-round deltas
  uint64_t merges_prev = 0; double sort_prev = 0;
  uint64_t ckpt_writes = 0;
  std::chrono::steady_clock::time_point last_ckpt;

  struct RoundCtx { uint8_t xph; uint32_t ustage; uint32_t ev_stage, ev_round; int phase; double phi; bool measured; };
  // calibration roles (WP3_DESIGN §1.11)
  bool calib = false; uint8_t role_addr = R_FINAL;
  int phase_of(int ph) const { return cfg.role == IslandRole::Pilot ? PH_PILOT : cfg.role == IslandRole::Diag ? PH_DIAG : ph; }
  // round-start state for the ledger so far on a numerical failure (calibration, law mode): the published kept runs
  // (immutable), the particles; the master tally is only changed at step boundaries
  struct RoundSnap { bool valid = false; bool init = false; RoundCtx rc{}; std::vector<Particle> P;
                     std::shared_ptr<Kept> top, lead0, lead1; } snap;
  uint32_t last_fail_particle = UINT32_MAX;
  // ---- numerical failures (review PR21 M1) -------------------------------------------------------------------
  // An island fails at the first CONSUMED event whose score fails. Inside an OpenMP region nothing throws: failures are
  // recorded here (the smallest particle index wins, so the choice does not depend on the schedule) and rethrown after
  // the region. Particle-major rounds record every particle's first failure; label-major groups run in particle order
  // and stop after the first group with a failure: both report the round's smallest failing particle, same text.
  enum FailKind { FK_NUMERICAL = 0, FK_INTERNAL = 1, FK_RESOURCE = 2 };
  struct FailSlot {
    std::mutex mu; bool has = false; int kind = 0; uint32_t particle = 0; std::string msg;
    void record(uint32_t i, const std::string& m, int k = FK_NUMERICAL) {
      std::lock_guard<std::mutex> lk(mu);
      if (!has || i < particle) { has = true; particle = i; msg = m; kind = k; }
    }
  } fail;
  // out of memory inside a parallel region (review #21 re-check n1): recorded, never std::terminate; rank UINT32_MAX so
  // that a deterministic numerical failure of the same round, if any, is reported instead
  template <class Fn> void oom_guard(Fn&& f) {
    try { f(); } catch (const std::bad_alloc&) { fail.record(UINT32_MAX, "out of memory inside a parallel region", FK_RESOURCE); }
  }
  bool fail_fatal() { std::lock_guard<std::mutex> lk(fail.mu); return fail.has && fail.kind != FK_NUMERICAL; }
  static const char* xph_name(uint8_t x) { return x == X_INIT ? "init" : x == X_BRIDGE ? "bridge stage" : x == X_BURN ? "burn-in round" : x == X_MEASURED ? "measured round" : "?"; }
  std::string fail_msg(const RoundCtx& rc, uint32_t i1, uint32_t pos, const std::string& what) const {
    return std::string(xph_name(rc.xph)) + " " + std::to_string(rc.ustage) + ", particle " + std::to_string(i1) + ", position " +
           std::to_string(pos) + ": " + what;
  }
  static std::string gibbs_fail(int j) { return "Gibbs label " + std::to_string(j) + ": score failed after Cholesky, refactor and augmented QR"; }
  void throw_if_failed() {
    std::lock_guard<std::mutex> lk(fail.mu);
    if (!fail.has) return;
    std::string m = fail.msg; int kd = fail.kind; fail.has = false; last_fail_particle = fail.particle;
    if (kd == FK_INTERNAL) throw v4::Error(v4::Status::internal_error, m);
    if (kd == FK_RESOURCE) throw v4::Error(v4::Status::resource_limit, m);
    throw v4::NumericalFailure(m);
  }

  IslandEngine(const Data& d, const Start& s, const Neighbours& n, const IslandConfig& c) : D(d), st(s), nb(n), cfg(c) {
    p = D.p; m = p + cfg.B + 2; NT = std::max(1, cfg.threads);
    top.init(cfg.store_cap ? cfg.store_cap : 40ULL * (uint64_t)p + 1, Order::HPM);
    for (int t = 0; t < NT; ++t) { tl.emplace_back(new ThreadLedger()); tl.back()->top = &top; scorers.emplace_back(new BitScorer(&D)); }
    master.top = &top;
    if (cfg.compat) {
      if (cfg.compat_src) csrc = cfg.compat_src;
      else { csrc_own.reset(new v4::CompatSource(cfg.seed, v4::compat_stream(R_FINAL, (uint8_t)cfg.tier, cfg.island))); csrc = csrc_own.get(); }
    }
    calib = cfg.role != IslandRole::Final;
    role_addr = cfg.role == IslandRole::Pilot ? R_PILOT : cfg.role == IslandRole::Diag ? R_DIAG : R_FINAL;
    if (cfg.leaders) {   // calibration islands / golden tests only (INTERFACES v0.1.7: no final-run leader stores)
      lead0.init(20ULL * (uint64_t)p, Order::LEX); lead1.init(20ULL * (uint64_t)p, Order::LEX);   // core/cpp/v3_ledger.h:78
      for (auto& t : tl) { t->lead0 = &lead0; t->lead1 = &lead1; }
    }
    top.dup_filter = cfg.store_dup_filter;
    top.test_oom_merge = cfg.test_oom_merge;
    top.defer = cfg.store_parallel_compact && NT > 1 && cfg.kernel == KernelKind::LabelMajor;   // PM has no boundaries (review m3)   // compaction at pass/step boundaries, all threads
    scratch_P.resize(NT);
    Bk = std::max(64, (cfg.tile + 63) / 64 * 64);
  }

  // --- addresses ---------------------------------------------------------------------------------------------
  inline Address addr(uint8_t xph, uint32_t ustage, uint32_t particle1, uint32_t position, uint32_t slot) const {
    Address a; a.seed = cfg.seed; a.role = role_addr; a.tier = calib ? (uint8_t)cfg.tier : 0; a.iter = calib ? (uint8_t)cfg.iter : 0; a.island = cfg.island;
    a.xph = xph; a.stage = ustage; a.particle = particle1; a.position = position; a.slot = slot; return a;
  }
  // INTERFACES v0.1.5 §4.2: final island r: (FINAL, frozen tier, iter -1, r, xph, stage, round, particle, q, sub);
  // sub = within-step ordinal: Gibbs held 0 (never offered), flip 1; U / N / I proposals and the initial draw 0.
  // calibration island: (CALIB, e, k, r, ...) with MEASURED round L + h (RoundCtx::ev_round).
  inline EventKey key(const RoundCtx& rc, uint32_t particle1, uint32_t position, uint8_t sub = 0) const {
    EventKey k = base_key(); k.xph = rc.xph;
    k.stage = rc.ev_stage; k.round = rc.ev_round; k.particle = particle1; k.position = position; k.sub = sub; return k;
  }
  inline EventKey base_key() const {
    EventKey k; k.seg = calib ? v4::SG_CALIB : SG_FINAL; k.tier = (uint8_t)cfg.tier; k.iter = calib ? (int8_t)cfg.iter : (int8_t)-1; k.unit = cfg.island;
    return k;
  }
  // Manager decision Q2b: every accepted state carries the full Bit score of its model (one value per model state;
  // removes class-A path dependence of particle states). Bit form: the flip score already has these bits.
  double canonical(BitScorer& sc, const Model& T, double lm) const {
    if constexpr (A == Arith::Bit) return lm; else return sc.score(T).logm;
  }
  // core/cpp/v3_engine.h:89-101: log m, log gamma_0, d, F of a model
  void fill(Particle& q, const Model& S, double logm) {
    q.S = S; q.h = zobrist(D, S); double c = st.comp(S); int k = (int)S.size();
    q.logm = logm; q.lg0 = D.logprior[k] + c; q.d = (logm - D.logm0) - c; q.F = D.logprior[k] + logm;
  }
  static inline double lgphi(const Particle& q, double phi) { return q.lg0 + phi * q.d; }
  void offer_particle(ThreadLedger& L, const Particle& q, int phase, int mech, const EventKey& k) {
    L.scored(q.S.data(), (uint32_t)q.S.size(), q.h, q.F, q.logm, phase, mech, k, q.lg0);
  }

  // --- U, N_b, I steps at round position `pos` (core/cpp/v3_engine.h:146-192). Returns true if the state changed;
  //     the new state is written to `out`. ----------------------------------------------------------------------
  bool step_nongibbs(int lab, const Particle& Pc, int i, uint32_t pos, const RoundCtx& rc, ThreadLedger& L, BitScorer& sc, Particle& out);   // island_pm.h

  // Round order (core/cpp/v3_engine.h:195-200): Fisher-Yates, uniform of step i at slot m-1-i.
  void draw_order(const RoundCtx& rc, int i, uint32_t* ord);   // island_pm.h

  // --- particle-major reference: core/cpp/v3_engine.h:202-214 for particle i ---------------------------------
  void pm_round(int i, const RoundCtx& rc, ThreadLedger& L, BitScorer& sc, std::vector<u128>* rb);   // island_pm.h

  // label-major group state: island_lm_state.h (owned with island_lm.h)
  using GroupBuf = LmGroupBuf;
  GroupBuf gb;

  void lm_group(int g0, int gN, const RoundCtx& rc);   // island_lm.h

  void round(const RoundCtx& rc) {
    if (calib) { snap.valid = true; snap.init = false; snap.rc = rc; snap.P = P; snap.top = top.k; snap.lead0 = lead0.k; snap.lead1 = lead1.k; }
    if (rc.measured) std::fill(rb_cur.begin(), rb_cur.end(), (u128)0);
    if (cfg.kernel == KernelKind::LabelMajor) {
      int G = std::max(1, cfg.G);
      for (int g0 = 0; g0 < cfg.N; g0 += G) { lm_group(g0, std::min(G, cfg.N - g0), rc); throw_if_failed(); }
    } else {
      auto t0 = std::chrono::steady_clock::now();
      if (rc.measured) for (auto& v : rb_thread) std::fill(v.begin(), v.end(), (u128)0);
      #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
      for (int i = 0; i < cfg.N; ++i) {
        if (csrc && fail.has) continue;   // compat (serial): stop at the first failure, as core
        int th = omp_get_thread_num();
        pm_round(i, rc, *tl[th], *scorers[th], rc.measured ? &rb_thread[th] : nullptr);
      }
      throw_if_failed();
      if (rc.measured) for (auto& v : rb_thread) for (int j = 0; j < p; ++j) rb_cur[j] += v[j];
      res.ks.particle_rounds += cfg.N;
      res.ks.t_pm += std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    }
  }

  // ---- stage barrier helpers (serial, particle order) -------------------------------------------------------
  int distinct() const {
    std::vector<int> idx(P.size()); for (size_t i = 0; i < P.size(); ++i) idx[i] = (int)i;
    std::sort(idx.begin(), idx.end(), [&](int a, int b) { if (P[a].h != P[b].h) return P[a].h < P[b].h; return lex_less(P[a].S, P[b].S); });
    int c = 0; for (size_t t = 0; t < idx.size(); ++t) if (t == 0 || P[idx[t]].h != P[idx[t - 1]].h || P[idx[t]].S != P[idx[t - 1]].S) ++c;
    return c;
  }
  // core/cpp/v3_engine.h:234-259 with addressed uniforms (RESAMPLE, stage t, particle i, position 0, slot 0)
  std::vector<int> resample(const std::vector<double>& lw, uint32_t t) {
    int N = (int)lw.size();
    double mx = NEG_INF; for (double v : lw) mx = std::max(mx, v);
    std::vector<double> W(N); double c = 0;
    for (int i = 0; i < N; ++i) { c += pm::exp(lw[i] - mx); W[i] = c; }
    for (int i = 0; i < N; ++i) W[i] /= c;
    W[N - 1] = 1.0;
    std::vector<int> guide(N); int k = 0;
    for (int b = 0; b < N; ++b) { double boundary = (double)b / (double)N; while (k < N - 1 && W[k] < boundary) ++k; guide[b] = k; }
    std::vector<int> a(N);
    for (int i = 0; i < N; ++i) {
      double u = U(addr(X_RESAMPLE, t, (uint32_t)i + 1, 0, SLOT_RESAMPLE));
      double ue = (u > 0) ? u : std::numeric_limits<double>::denorm_min();
      int bucket = std::min(N - 1, (int)std::floor(ue * (double)N));
      int kk = guide[bucket];
      while (kk < N - 1 && W[kk] < ue) ++kk;
      while (kk > 0 && W[kk - 1] >= ue) --kk;
      a[i] = kk;
    }
    return a;
  }
  // merge thread ledgers and flush store buffers (step boundary; order-free)
  void sync_ledgers() {
    for (auto& t : tl) { top.flush(t->buf); if (cfg.leaders) { lead0.flush(t->buf0); lead1.flush(t->buf1); } master.merge_from(*t); t->reset_counters(); }
    if (cfg.leaders) {
      lead0.compact(); lead1.compact();
      for (auto& t : tl) { t->buf0.snap.reset(); t->buf0.snap_gen = ~0ull; t->buf1.snap.reset(); t->buf1.snap_gen = ~0ull; }
      if (lead0.nan_offered.load() || lead1.nan_offered.load()) throw v4::Error(v4::Status::internal_error, "leader store: a NaN value was offered");
    }
    release_snapshots();
    if (top.defer) top.compact_parallel(NT); else top.compact();   // one island store, compacted at every step boundary
    if (top.nan_offered.load()) throw v4::Error(v4::Status::internal_error, "store: a NaN value was offered (INTERFACES v0.1.3)");
  }
  // workers drop their kept-run snapshots before a boundary compaction: at most two kept runs are ever alive
  void release_snapshots() { for (auto& t : tl) { t->buf.snap.reset(); t->buf.snap_gen = ~0ull; } }
  // --mem-budget at a step boundary (deterministic: the kept run's content is a function of the offers)
  bool over_budget(int step) {
    if (!cfg.mem_budget) return false;
    // the stored models' actual mean size (exact pool) once the store is full; before that the larger of it and the
    // admission's k (the not-yet-stored entries are unknown)
    const double kk = top.size() ? (double)top.k->pool.size() / (double)top.size() : k_est;
    const double k = top.size() >= top.cap ? kk : std::max(kk, k_est);
    MemPlan mp = island_memory(msz, k);
    if (mp.total <= cfg.mem_budget) return false;
    res.status = 3; res.reason = "mem_budget: predicted peak " + std::to_string(mp.total >> 20) + " MiB > budget " + std::to_string(cfg.mem_budget >> 20) +
                 " MiB after step " + std::to_string(step) + " [" + mem_plan_text(mp) + "]";
    return true;
  }
  MoveStats take_moves() { MoveStats ms = master.ms; master.ms = MoveStats(); return ms; }

  // ---- checkpoint ---------------------------------------------------------------------------------------------
  // Configuration + binary fingerprint (not threads, G, tile or kernel: a resume may change them). INTERFACES v0.1.3:
  // a restart refuses a different binary block.
  uint64_t fingerprint() const {
    Fnv f; f.pod(cfg.seed); f.pod(cfg.island); f.pod(cfg.tier); f.pod(cfg.N); f.vec(cfg.grid); f.pod(cfg.L); f.pod(cfg.Hm); f.pod(cfg.B);
    f.pod(top.cap); f.pod(D.n); f.pod(D.p); f.pod(D.yty); f.pod(st.logZbar0); f.pod(st.J); f.pod((int)A); f.pod(cfg.compat); f.pod(cfg.leaders);
    const std::string bb = v4::binary_block_no_self_test().dump(); f.bytes(bb.data(), bb.size());
    return f.h;
  }
  // Streamed checkpoint I/O (manager Q6): no byte image of the store; the checksum is computed while streaming.
  struct CkptOut {
    FILE* f = nullptr; Fnv ck; uint64_t len = 0; bool bad = false;
    void raw(const void* q, size_t n) { if (n && std::fwrite(q, 1, n, f) != n) bad = true; ck.bytes(q, n); len += n; }
    template <class T> void put(const T& x) { raw(&x, sizeof(T)); }
    template <class T> void putv(const std::vector<T>& v) { uint64_t n = v.size(); put(n); raw(v.data(), n * sizeof(T)); }
  };
  struct CkptIn {
    FILE* f = nullptr; uint64_t left = 0; bool bad = false;
    void raw(void* q, size_t n) { if (bad || n > left || (n && std::fread(q, 1, n, f) != n)) { bad = true; return; } left -= n; }
    template <class T> void get(T& x) { raw(&x, sizeof(T)); }
    template <class T> void getv(std::vector<T>& v) {
      uint64_t n = 0; get(n); if (bad || n > left / std::max<size_t>(1, sizeof(T))) { bad = true; return; }
      v.resize(n); raw(v.data(), n * sizeof(T));
    }
  };
  // the event key field by field (no padding bytes in the checkpoint; review m4d)
  static void key_io(CkptOut& w, const EventKey& k) { w.put(k.seg); w.put(k.tier); w.put(k.iter); w.put(k.unit); w.put(k.xph); w.put(k.stage); w.put(k.round); w.put(k.particle); w.put(k.position); w.put(k.sub); }
  static void key_io(CkptIn& r, EventKey& k) { r.get(k.seg); r.get(k.tier); r.get(k.iter); r.get(k.unit); r.get(k.xph); r.get(k.stage); r.get(k.round); r.get(k.particle); r.get(k.position); r.get(k.sub); }
  template <class W> void ckpt_payload(W& w, int step) {
    w.put(fingerprint()); w.put(step); w.put(logZ); w.put(res.init_hash);
    uint64_t np = P.size(); w.put(np);
    for (auto& x : P) { w.putv(x.S); w.put(x.h); w.put(x.logm); w.put(x.lg0); w.put(x.d); w.put(x.F); }
    w.putv(res.stages); w.putv(res.terminal_moves); w.putv(res.terminal_distinct);
    uint64_t nr = res.rb_round.size(); w.put(nr); for (auto& v : res.rb_round) w.putv(v);
    w.putv(rb_tot);
    w.put(master.logical); w.put(master.island_best);
    w.put(master.hpm.has); w.putv(master.hpm.S); w.put(master.hpm.F); w.put(master.hpm.logm); key_io(w, master.hpm.key); w.put(master.hpm.phase); w.put(master.hpm.mech);
    w.putv(top.k->v); w.putv(top.k->hash); w.putv(top.k->off); w.putv(top.k->len); w.putv(top.k->pool);
    if (csrc) { w.put(csrc->g.s); w.put(csrc->g.count); w.putv(rb_d); }   // compat: xoshiro state + position, double RB
    if (cfg.leaders) for (TopStore* L : {&lead0, &lead1}) { w.putv(L->k->v); w.putv(L->k->hash); w.putv(L->k->off); w.putv(L->k->len); w.putv(L->k->pool); }
  }
  // Two generations <path>.a/.b, alternately: header placeholder, streamed payload, header (generation, length,
  // checksum) rewritten in place, fflush + fsync, rename from <file>.tmp.<pid>. A kill at any point leaves the other
  // generation intact (tests: truncated / leftover temporary / corrupt newest).
  void save_ckpt(int step) {
    auto t0 = std::chrono::steady_clock::now();
    std::string path = cfg.ckpt_path + ((ckpt_writes & 1) ? ".b" : ".a");
    std::string tmp = path + ".tmp." + std::to_string((long)getpid());
    FILE* f = std::fopen(tmp.c_str(), "wb");
    if (!f) throw v4::Error(v4::Status::io_error, "cannot open checkpoint " + tmp);
    std::setvbuf(f, nullptr, _IOFBF, 1 << 20);
    uint64_t zero[3] = {0, 0, 0};
    bool ok = std::fwrite(kCkptMagic, 1, 8, f) == 8 && std::fwrite(zero, 8, 3, f) == 3;
    CkptOut w; w.f = f;
    ckpt_payload(w, step);
    uint64_t gen = (uint64_t)(step + 1) * 1024 + (uint64_t)(ckpt_writes & 1023);
    ok = ok && !w.bad && std::fseek(f, 8, SEEK_SET) == 0 && std::fwrite(&gen, 8, 1, f) == 1 && std::fwrite(&w.len, 8, 1, f) == 1 &&
         std::fwrite(&w.ck.h, 8, 1, f) == 1 && std::fflush(f) == 0 && ::fsync(fileno(f)) == 0;
    ok = (std::fclose(f) == 0) && ok;
    if (!ok || std::rename(tmp.c_str(), path.c_str()) != 0) { std::remove(tmp.c_str()); throw v4::Error(v4::Status::io_error, "checkpoint write failed: " + path); }
    {   // the rename is durable only once the directory entry is (review m4a; INTERFACES §5.1)
      std::string dir = path.substr(0, path.find_last_of('/') == std::string::npos ? 0 : path.find_last_of('/'));
      int dfd = ::open(dir.empty() ? "." : dir.c_str(), O_RDONLY | O_DIRECTORY);
      if (dfd < 0 || ::fsync(dfd) != 0) { if (dfd >= 0) ::close(dfd); throw v4::Error(v4::Status::io_error, "directory fsync failed for " + path); }
      ::close(dfd);
    }
    ++ckpt_writes;
    last_ckpt = std::chrono::steady_clock::now();
    res.ks.t_ckpt += std::chrono::duration<double>(last_ckpt - t0).count();
  }
  // returns the step to continue after, or -1 (no valid checkpoint). A valid checkpoint (checksum ok) of another
  // configuration or binary is refused (invalid_input), never silently ignored.
  int load_ckpt() {
    {   // leftover temporary files of killed writers (review m4b): <path>.{a,b}.tmp.<pid>
      std::filesystem::path base(cfg.ckpt_path); std::error_code ec;
      std::filesystem::path dir = base.has_parent_path() ? base.parent_path() : std::filesystem::path(".");
      const std::string stem = base.filename().string();
      for (auto& de : std::filesystem::directory_iterator(dir, ec)) {
        const std::string fn = de.path().filename().string();
        if (fn.rfind(stem + ".a.tmp.", 0) == 0 || fn.rfind(stem + ".b.tmp.", 0) == 0) std::filesystem::remove(de.path(), ec);
      }
    }
    int best_step = -1; uint64_t best_gen = 0; std::string best; bool foreign = false;
    for (const char* sfx : {".a", ".b"}) {
      std::string path = cfg.ckpt_path + sfx;
      FILE* f = std::fopen(path.c_str(), "rb"); if (!f) continue;
      char mg[8]; uint64_t gen = 0, len = 0, ck = 0;
      bool ok = std::fread(mg, 1, 8, f) == 8 && std::memcmp(mg, kCkptMagic, 8) == 0 && std::fread(&gen, 8, 1, f) == 1 &&
                std::fread(&len, 8, 1, f) == 1 && std::fread(&ck, 8, 1, f) == 1;
      if (ok) { std::fseek(f, 0, SEEK_END); ok = (uint64_t)std::ftell(f) == 32 + len && len >= 12; std::fseek(f, 32, SEEK_SET); }
      uint64_t fp = 0; int s = -1;
      if (ok) {   // pass 1: checksum by streaming
        Fnv c; std::vector<unsigned char> buf(1 << 20); uint64_t left = len, pos = 0;
        while (left && ok) {
          size_t n = (size_t)std::min<uint64_t>(left, buf.size());
          if (std::fread(buf.data(), 1, n, f) != n) { ok = false; break; }
          if (pos == 0 && n >= 12) { std::memcpy(&fp, buf.data(), 8); std::memcpy(&s, buf.data() + 8, 4); }
          c.bytes(buf.data(), n); left -= n; pos += n;
        }
        ok = ok && c.h == ck;
      }
      std::fclose(f);
      if (!ok) continue;
      if (fp != fingerprint()) { foreign = true; continue; }
      if (best_step < 0 || gen > best_gen) { best_gen = gen; best = path; best_step = s; }
    }
    if (best_step < 0) {
      if (foreign) throw v4::Error(v4::Status::invalid_input, "checkpoint " + cfg.ckpt_path + " belongs to another configuration or binary");
      return -1;
    }
    // pass 2. The file passed its checksum: a parse failure now is an internal inconsistency, never a silent fresh start
    // over partially overwritten state (review m4c).
    auto corrupt = [&](FILE* fp) { if (fp) std::fclose(fp); throw v4::Error(v4::Status::internal_error, "checkpoint " + best + ": checksum valid but payload unreadable"); };
    FILE* f = std::fopen(best.c_str(), "rb"); if (!f) corrupt(nullptr);
    uint64_t len = 0; std::fseek(f, 16, SEEK_SET); if (std::fread(&len, 8, 1, f) != 1) corrupt(f);
    std::fseek(f, 32, SEEK_SET);
    CkptIn r; r.f = f; r.left = len;
    uint64_t fp; int step; r.get(fp); r.get(step); r.get(logZ); r.get(res.init_hash);
    uint64_t np; r.get(np); if (r.bad || np != (uint64_t)cfg.N) corrupt(f);
    P.assign(np, Particle());
    for (auto& x : P) { r.getv(x.S); r.get(x.h); r.get(x.logm); r.get(x.lg0); r.get(x.d); r.get(x.F); }
    r.getv(res.stages); r.getv(res.terminal_moves); r.getv(res.terminal_distinct);
    uint64_t nr = 0; r.get(nr); if (r.bad || nr > 1u << 20) corrupt(f);
    res.rb_round.assign(nr, {}); for (auto& v : res.rb_round) r.getv(v);
    r.getv(rb_tot);
    r.get(master.logical); r.get(master.island_best);
    r.get(master.hpm.has); r.getv(master.hpm.S); r.get(master.hpm.F); r.get(master.hpm.logm); key_io(r, master.hpm.key); r.get(master.hpm.phase); r.get(master.hpm.mech);
    { auto nk = std::make_shared<Kept>(); r.getv(nk->v); r.getv(nk->hash); r.getv(nk->off); r.getv(nk->len); r.getv(nk->pool); top.k = nk; }
    if (csrc) { r.get(csrc->g.s); r.get(csrc->g.count); r.getv(rb_d); }
    if (cfg.leaders) for (TopStore* L : {&lead0, &lead1}) { auto nk = std::make_shared<Kept>(); r.getv(nk->v); r.getv(nk->hash); r.getv(nk->off); r.getv(nk->len); r.getv(nk->pool); L->k = nk; L->publish_loaded(); }
    if (r.bad) corrupt(f);
    std::fclose(f);
    top.publish_loaded();
    return step;
  }
  void maybe_ckpt(int step, bool& stop) {
    stop = false;
    if (cfg.ckpt_path.empty()) return;
    double since = std::chrono::duration<double>(std::chrono::steady_clock::now() - last_ckpt).count();
    if (step == cfg.stop_after_step || since >= cfg.ckpt_every_s) save_ckpt(step);
    if (step == cfg.stop_after_step) stop = true;
  }

  // initial draw of particle i (core/cpp/v3_engine.h:285-297): pi_0 draw, score, one INIT event. A failed score is
  // recorded (no event), as core's eval throws before its event.
  void init_particle(int i, ThreadLedger& L, BitScorer& sc) {
    Model S;
    if (csrc) draw_pi0(st, [&](uint32_t slot) { return U(addr(X_INIT, 0, (uint32_t)i + 1, 0, slot)); }, S);
    else {
      const Address a0 = addr(X_INIT, 0, (uint32_t)i + 1, 0, 0);
      const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
      draw_pi0_fast(st, [&](uint32_t slot) { return U(addr(X_INIT, 0, (uint32_t)i + 1, 0, slot)); },
                    [&](const uint32_t* sl, double* out) { philox8_word(ctr.data(), kk.data(), 0, sl, out); }, S);
    }
    try { fill(P[i], S, sc.score(S).logm); }
    catch (const v4::NumericalFailure& e) { fail.record((uint32_t)i, "initial draw, particle " + std::to_string(i + 1) + ": " + e.what()); return; }
    catch (const std::bad_alloc&) { fail.record(UINT32_MAX, "out of memory inside a parallel region", FK_RESOURCE); return; }
    EventKey k = base_key(); k.xph = X_INIT; k.particle = (uint32_t)i + 1;
    offer_particle(L, P[i], phase_of(PH_FINAL_INIT), ME_INIT, k);
  }

  // Ledger so far after a numerical failure (calibration roles; WP3_DESIGN §1.11): core's shared ledger holds the SERIAL
  // prefix -- every event before the failing score in core's order (earlier rounds; particles 1..i-1 of the failing
  // round or initial draw; particle i up to the failing score). The label-major (or threaded particle-major) round
  // offered events of other particles too, so the round-start state is restored (published kept runs, tallies, the
  // particles) and the prefix is replayed particle-major, serially, at the same addresses (same events and offers).
  // Compat runs serially and stops at the first failure: its ledger is the prefix already.
  void rebuild_prefix() {
    const uint32_t fi = last_fail_particle;
    for (auto& t : tl) {
      t->buf.clear(); t->buf.snap.reset(); t->buf.snap_gen = ~0ull;
      t->buf0.clear(); t->buf0.snap.reset(); t->buf0.snap_gen = ~0ull; t->buf1.clear(); t->buf1.snap.reset(); t->buf1.snap_gen = ~0ull;
      t->reset_counters();
    }
    top.restore(snap.top);
    if (cfg.leaders) { lead0.restore(snap.lead0); lead1.restore(snap.lead1); }
    ThreadLedger& L = *tl[0]; BitScorer& sc = *scorers[0];
    if (snap.init) {
      for (uint32_t i = 0; i < fi && i < (uint32_t)cfg.N; ++i) init_particle((int)i, L, sc);
    } else {
      P = snap.P;
      for (uint32_t i = 0; i <= fi && i < (uint32_t)cfg.N; ++i) pm_round((int)i, snap.rc, L, sc, nullptr);
    }
    { std::lock_guard<std::mutex> lk(fail.mu); fail.has = false; }   // the replay meets the same failure at particle fi
  }

  // ---- the island ---------------------------------------------------------------------------------------------
  IslandRun run() {
    auto tstart = std::chrono::steady_clock::now();
    last_ckpt = tstart;
    const int N = cfg.N, L = cfg.L, Hm = cfg.Hm;
    // adaptive schedule (benchmarks / pilot-like grids): T is known only when phi reaches 1
    int T = cfg.adaptive ? (1 << 23) : (int)cfg.grid.size() - 1;
    std::vector<double> grid = cfg.adaptive ? std::vector<double>{0.0} : cfg.grid;
    res.r = (int)cfg.island; res.N = N; res.T = T; res.L = L; res.Hm = Hm; res.p = p;
    rb_cur.assign(p, 0); rb_tot.assign(p, 0); if (csrc) rb_d.assign(p, 0.0);
    if (csrc) res.stream_start = csrc->g.count;
    if (cfg.kernel == KernelKind::ParticleMajor) rb_thread.assign(NT, std::vector<u128>(p, 0));
    if (cfg.kernel == KernelKind::LabelMajor) {   // tiled row-major X (zero-padded last tile)
      ntile = (p + Bk - 1) / Bk; Xt.assign((size_t)ntile * Bk * D.n, 0.0);
      #pragma omp parallel for schedule(static) num_threads(NT)
      for (int ti = 0; ti < ntile; ++ti)
        for (int jj = 0; jj < Bk && ti * Bk + jj < p; ++jj) { const double* x = D.col(ti * Bk + jj); for (int i = 0; i < D.n; ++i) Xt[(size_t)ti * Bk * D.n + (size_t)i * Bk + jj] = x[i]; }
    }
    int done_step = -1;
    if (!cfg.ckpt_path.empty() && cfg.resume) { done_step = load_ckpt(); res.resumed_from_step = done_step; }
    bool stop = false;
    try {
      if (done_step < 0) {
        // initial draws (core/cpp/v3_engine.h:285-297)
        P.assign(N, Particle());
        if (calib) { snap = RoundSnap(); snap.valid = true; snap.init = true; snap.top = top.k; snap.lead0 = lead0.k; snap.lead1 = lead1.k; }
        #pragma omp parallel for schedule(dynamic, 16) num_threads(NT)
        for (int i = 0; i < N; ++i) {
          if (csrc && fail.has) continue;   // compat (serial): stop at the first failure, as core (no further draws)
          int th = omp_get_thread_num();
          init_particle(i, *tl[th], *scorers[th]);
        }
        throw_if_failed();
        uint64_t hh = 0x243F6A8885A308D3ULL;
        for (int i = 0; i < N; ++i) { uint64_t x = hh ^ P[i].h ^ (uint64_t)(i + 1); hh = splitmix64(x); }
        res.init_hash = hh;
        logZ = D.logm0 + st.logZbar0;
        sync_ledgers();
        res.ks.t_init += std::chrono::duration<double>(std::chrono::steady_clock::now() - tstart).count();
        done_step = 0; maybe_ckpt(0, stop);
      }
      std::vector<double> lw(N), lw2(N);
      for (int step = done_step + 1; step <= T + L + Hm && !stop; ++step) {
        if (step <= T) {   // bridge stage t (core/cpp/v3_engine.h:303-339)
          auto tb = std::chrono::steady_clock::now();
          int t = step; double phi_prev = grid[t - 1];
          if (cfg.adaptive) {   // core/cpp/v3_engine.h:309-313 with the pilot rule of core/cpp/v3_calib.h:30-46
            std::vector<double> dv(N); for (int i = 0; i < N; ++i) dv[i] = P[i].d;
            NextPhi np = pilot_next_phi(dv, phi_prev, cfg.adaptive_H > 0 ? cfg.adaptive_H : (double)N, cfg.adaptive_Te);
            grid.push_back(np.phi); if (np.forced) ++res.forced;
            if (np.phi == 1.0) T = t;   // the last bridge stage
          }
          double phi_new = grid[t], dphi = phi_new - phi_prev;
          for (int i = 0; i < N; ++i) lw[i] = dphi * P[i].d;
          double lse = log_sum_exp(lw);
          double inc = lse - pm::log((double)N);
          for (int i = 0; i < N; ++i) lw2[i] = 2 * lw[i];
          double ess = pm::exp(2 * lse - log_sum_exp(lw2));
          logZ += inc;
          std::vector<int> a = resample(lw, (uint32_t)t);
          std::vector<Particle> Pn(N); for (int i = 0; i < N; ++i) Pn[i] = P[a[i]]; P.swap(Pn);
          StageRow row; row.phi = phi_new; row.inc = inc; row.ess = ess; row.cum = logZ; row.distinct_res = distinct();
          res.ks.t_barrier += std::chrono::duration<double>(std::chrono::steady_clock::now() - tb).count();
          RoundCtx rc{X_BRIDGE, (uint32_t)t, (uint32_t)t, (uint32_t)t, phase_of(PH_FINAL_BRIDGE), phi_new, false};
          round(rc);
          sync_ledgers(); row.moves = take_moves(); row.distinct_moved = distinct();
          res.stages.push_back(row);
        } else if (step <= T + L) {   // burn-in round l
          int l = step - T;
          RoundCtx rc{X_BURN, (uint32_t)l, (uint32_t)T, (uint32_t)l, phase_of(PH_BURN_IN), 1.0, false};
          round(rc);
          sync_ledgers(); res.terminal_moves.push_back(take_moves()); res.terminal_distinct.push_back(distinct());
        } else {   // measured round h with RB
          int h = step - T - L;
          RoundCtx rc{X_MEASURED, (uint32_t)h, (uint32_t)T, (uint32_t)(calib ? L + h : h), phase_of(PH_MEASURED), 1.0, true};
          std::vector<double> before; if (csrc) before = rb_d;
          round(rc);
          std::vector<double> rr(p);
          if (csrc) { for (int j = 0; j < p; ++j) rr[j] = rb_d[j] - before[j]; }   // core/cpp/v3_engine.h:353-358
          else for (int j = 0; j < p; ++j) { rr[j] = unfix63(rb_cur[j]); rb_tot[j] += rb_cur[j]; }
          res.rb_round.push_back(rr);
          sync_ledgers(); res.terminal_moves.push_back(take_moves()); res.terminal_distinct.push_back(distinct());
        }
        if (cfg.verbose) {
          const auto& k = res.ks;
          static thread_local double prev_t = 0; double now_t = std::chrono::duration<double>(std::chrono::steady_clock::now() - tstart).count();
          std::fprintf(stderr, "  [island] step %d (+%.1f s) done %.1f s: passes %llu supports %llu slow %llu | phaseA %.1f B %.1f walk %.1f build %.1f orders %.1f | store %zu merges %llu buffered %llu\n",
                       step, now_t - prev_t, now_t, (unsigned long long)k.passes,
                       (unsigned long long)k.supports, (unsigned long long)k.slow_supports, k.t_phaseA, k.t_phaseB, k.t_walk, k.t_build, k.t_orders,
                       top.size(), (unsigned long long)top.n_merges, (unsigned long long)top.n_buffered);
          {   // memory at the step boundary: resident set, kept run, stored mean |S|
            long rss = -1, hwm = -1;
            if (FILE* fs = std::fopen("/proc/self/status", "r")) { char ln[256];
              while (std::fgets(ln, sizeof ln, fs)) { if (!std::strncmp(ln, "VmRSS:", 6)) rss = std::atol(ln + 6); if (!std::strncmp(ln, "VmHWM:", 6)) hwm = std::atol(ln + 6); }
              std::fclose(fs); }
            const double km = top.size() ? (double)top.k->pool.size() / (double)top.size() : 0.0;
            std::fprintf(stderr, "  [mem] step %d: RSS %.2f GB, peak %.2f GB | store %zu entries, mean |S| %.2f, kept run %.2f GB\n", step, rss / 1048576.0,
                         hwm / 1048576.0, top.size(), km, (26.0 * top.size() + 4.0 * top.k->pool.size()) / 1073741824.0);
          }
          {   // per-round counters (manager 11-16 (a)): the round's own pairs, sweeps and costs
            const double dt = now_t - prev_t, steps = (double)(k.particle_rounds - ks_prev.particle_rounds) * (double)m;
            const double pairs = (double)(k.support_label_pairs - ks_prev.support_label_pairs), sweeps = (double)(k.particle_sweeps - ks_prev.particle_sweeps);
            const double rounds = (double)(k.particle_rounds - ks_prev.particle_rounds);
            std::fprintf(stderr, "  [round] step %d: wall %.2f s | steps %.4g pairs %.4g (%.3f pairs per particle-round / p) sweeps %.4g (M %.3f) passes %llu | "
                         "ns per step (wall x threads) %.1f | ns per pair (wall x threads) %.1f | products ns/pair (thread) %.1f | phaseA ns/pair (wall x threads) %.1f | "
                         "phaseB %.2f s compaction %.2f s (%llu compactions, sorts %.2f s)\n",
                         step, dt, steps, pairs, steps > 0 ? pairs / steps * m / std::max(1.0, (double)p) : 0.0, sweeps, rounds > 0 ? sweeps / rounds : 0.0,
                         (unsigned long long)(k.passes - ks_prev.passes), steps > 0 ? 1e9 * dt * NT / steps : 0.0, pairs > 0 ? 1e9 * dt * NT / pairs : 0.0,
                         pairs > 0 ? 1e9 * (k.t_products - ks_prev.t_products) / pairs : 0.0,
                         pairs > 0 ? 1e9 * (k.t_phaseA - ks_prev.t_phaseA) * NT / pairs : 0.0, k.t_phaseB - ks_prev.t_phaseB, top.t_compact - ks_prev.t_store_compact,
                         (unsigned long long)(top.n_merges - merges_prev), top.t_sort - sort_prev);
            ks_prev = k; ks_prev.t_store_compact = top.t_compact; merges_prev = top.n_merges; sort_prev = top.t_sort;
          }
          prev_t = now_t;
        }
        if (cfg.check_store && !(top.check_invariant())) throw v4::Error(v4::Status::internal_error, "store invariant I1 violated");
        if (over_budget(step)) { stop = true; break; }
        maybe_ckpt(step, stop);
      }
    } catch (const NumericalFailure& e) {
      res.status = 2; res.reason = e.what();
      if (calib && !csrc && snap.valid) rebuild_prefix();   // the ledger so far = core's serial prefix
    } catch (const v4::Error& e) {
      if (e.st != v4::Status::resource_limit) throw;
      res.status = 3; res.reason = e.what();
    } catch (const std::bad_alloc&) {
      res.status = 3; res.reason = "resource_limit: out of memory";
    }
    if (calib && (res.status == 2 || res.status == 3)) {   // the ledger so far (WP4 merges it; core's ledger is shared)
      try { sync_ledgers(); } catch (const std::bad_alloc&) { res.status = 3; res.reason = "resource_limit: out of memory"; }
      res.partial = res.status == 3;
    }
    res.T = T; res.grid = grid;
    if (stop && res.status == 0) { res.status = 1; res.reason = "interrupted after checkpoint (stop_after_step)"; }
    // outputs
    res.logZ = logZ;
    if (res.status == 0) {
      res.rb_acc.assign(p, 0.0); res.pip.assign(p, 0.0);
      for (int j = 0; j < p; ++j) { res.rb_acc[j] = csrc ? rb_d[j] : unfix63(rb_tot[j]); res.pip[j] = res.rb_acc[j] / ((double)N * Hm); }
    }
    std::memcpy(res.logical, master.logical, sizeof(res.logical));
    res.island_best = master.island_best; res.hpm = master.hpm;
    if (res.status == 0 || res.status == 1 || calib) {   // only a completed (or test-interrupted) island reports its store: a failed
                                                // or refused island may hold part of an unfinished round (GUARD-W, review m1)
      Kept& K = *top.k;      // moved, not copied (review m8b; the run is over)
      res.top_v = std::move(K.v); res.top_hash = std::move(K.hash); res.top_off = std::move(K.off); res.top_len = std::move(K.len); res.top_pool = std::move(K.pool);
    }
    res.ks.kept_live_max = kept_live_max().load();
    if (cfg.keep_terminal) for (auto& x : P) res.terminal.push_back(x.S);
    if (csrc) { res.compat = true; res.stream_count = csrc->g.count; }
    res.role = cfg.role; res.tier = cfg.tier; res.iter = cfg.iter;
    if (cfg.leaders) {
      res.leaders = true;
      res.lead0_v = std::move(lead0.k->v); res.lead0_hash = std::move(lead0.k->hash); res.lead0_off = std::move(lead0.k->off); res.lead0_len = std::move(lead0.k->len); res.lead0_pool = std::move(lead0.k->pool);
      res.lead1_v = std::move(lead1.k->v); res.lead1_hash = std::move(lead1.k->hash); res.lead1_off = std::move(lead1.k->off); res.lead1_len = std::move(lead1.k->len); res.lead1_pool = std::move(lead1.k->pool);
    }
    res.ks.store_merges = top.n_merges; res.ks.store_buffered = top.n_buffered;
    res.ks.store_serial_merges = top.n_serial_merges; res.ks.t_store_compact = top.t_compact;
    for (auto& t : tl) res.ks.store_dup_dropped += t->buf.n_dup_dropped;
    res.ks.t_total = std::chrono::duration<double>(std::chrono::steady_clock::now() - tstart).count();
    return std::move(res);
  }
};


#ifdef V4_ISLAND_DEFINE_COMMON
MemPlan plan_island(const Data& D, const Start& st, const IslandConfig& cfg, MemSizes* zout, double* kout, int* Gout) {
  // k for the plan (review P2 at 10^6): round 1 stores pi_0-sized models, so the stored mean size is bounded by the
  // pi_0 size distribution (exact, from setup) -- its 90 % quantile + 1 (flips add one member) -- and, later, by the
  // calibration-measured stored mean k_store
  double k_pi0 = 0, acc = 0;
  for (size_t k = 0; k < st.size_logmass.size(); ++k) { acc += std::exp(st.size_logmass[k]); if (acc >= 0.90) { k_pi0 = (double)k; break; } }
  const double k_est = cfg.test_admission_k > 0 ? cfg.test_admission_k : std::max({8.0, k_pi0 + 1.0, cfg.k_store});
  const uint64_t cap = cfg.store_cap ? cfg.store_cap : 40ULL * (uint64_t)D.p + 1;
  const bool lm = cfg.kernel == KernelKind::LabelMajor;
  MemSizes z; z.n = D.n; z.p = D.p; z.K = D.K; z.N = cfg.N; z.B = cfg.B; z.Hm = cfg.Hm; z.threads = cfg.threads;
  z.tile = std::max(64, (cfg.tile + 63) / 64 * 64); z.cap = cap; z.label_major = lm;
  z.deferred = cfg.store_parallel_compact && cfg.threads > 1 && lm; z.leaders = cfg.leaders || cfg.role != IslandRole::Final; z.compat = cfg.compat; z.inputs_bytes = cfg.inputs_bytes;
  z.calib = cfg.role != IslandRole::Final;
  int G = cfg.G ? cfg.G : 256;
  z.G = G; MemPlan mp = island_memory(z, k_est);
  if (cfg.mem_budget && cfg.G == 0) {
    while (G > 1 && mp.total > cfg.mem_budget) { --G; z.G = G; mp = island_memory(z, k_est); }
  }
  if (zout) *zout = z;
  if (kout) *kout = k_est;
  if (Gout) *Gout = G;
  return mp;
}
#endif

// glibc: a fixed mmap threshold (no dynamic raise), so large arrays are mmapped and given back to the system when freed,
// whichever thread's arena frees them (re-check m1). Process-wide, set once; small allocations are unaffected. Only for
// islands whose store compacts on worker threads (particle-major with threads > 1): label-major compacts on the main
// thread, where freed kept runs are reused in place, and fresh mmaps would add page faults to every compaction.
inline void fix_mmap_threshold() {
  static std::once_flag once;
  std::call_once(once, [] { mallopt(M_MMAP_THRESHOLD, 4 << 20); });
}

template <Arith A>
IslandRun run_island(const Data& D, const Start& st, const Neighbours& nb, const IslandConfig& cfg_in) {
  if (cfg_in.kernel == KernelKind::ParticleMajor && cfg_in.threads > 1) fix_mmap_threshold();
  IslandConfig cfg = cfg_in;
  const bool calib = cfg.role != IslandRole::Final;
  if (calib) {   // WP3_DESIGN §1.11 (agreed with WP4)
    if (cfg.role == IslandRole::Pilot && (cfg.island != 0 || cfg.iter != 0)) throw v4::Error(v4::Status::invalid_input, "run_island: the pilot is island 0, iteration 0");
    if (cfg.role == IslandRole::Diag && (cfg.island < 1 || cfg.island > 4 || cfg.iter < 1)) throw v4::Error(v4::Status::invalid_input, "run_island: a diagnostic island is 1..4 at iteration k >= 1");
    if (cfg.tier > 3 || cfg.iter > 63) throw v4::Error(v4::Status::invalid_input, "run_island: calibration tier < 4 and iteration < 64 (INTERFACES §3)");
    if (!cfg.ckpt_path.empty() || cfg.stop_after_step >= 0) throw v4::Error(v4::Status::invalid_input, "run_island: calibration islands have no checkpoints");
    if (cfg.compat && !cfg.compat_src) throw v4::Error(v4::Status::invalid_input, "run_island: a compat calibration island needs the caller's stream (compat_src)");
    cfg.leaders = true;   // the calibration leader stores feed V (D-7)
  } else if (cfg.island < 1) throw v4::Error(v4::Status::invalid_input, "run_island: a final island is r >= 1");
  if (!cfg.adaptive && (cfg.grid.size() < 2 || cfg.grid.front() != 0.0 || cfg.grid.back() != 1.0)) throw v4::Error(v4::Status::invalid_input, "run_island: grid must run from 0 to 1");
  for (size_t i = 1; i < cfg.grid.size(); ++i) if (!(cfg.grid[i] > cfg.grid[i - 1])) throw v4::Error(v4::Status::invalid_input, "run_island: grid not strictly increasing (I3)");
  if (cfg.adaptive && !cfg.ckpt_path.empty()) throw v4::Error(v4::Status::invalid_input, "run_island: the adaptive schedule has no checkpoints");
  if (cfg.compat && (A != Arith::Bit || cfg.kernel != KernelKind::ParticleMajor || cfg.threads != 1))
    throw v4::Error(v4::Status::invalid_input, "run_island: compat mode needs Arith::Bit, the particle-major kernel and 1 thread (serial v3 streams)");
  if (A == Arith::Bit && cfg.kernel == KernelKind::LabelMajor && !cfg.allow_test_kernels)
    throw v4::Error(v4::Status::invalid_input, "run_island: the bit-form label-major kernel is test-only (D-21, manager Q1); theory mode runs particle-major");
  if (cfg.stop_after_step >= 0 && cfg.ckpt_path.empty()) throw v4::Error(v4::Status::invalid_input, "run_island: stop_after_step needs a checkpoint path");
  if (cfg.G < 0 || cfg.G > 256) throw v4::Error(v4::Status::invalid_input, "run_island: G must be in 0..256 (0 = chosen by mem_budget; manager Q3)");
  // review PR24 r1 / PR26 B1, re-check m2: a final island admitted under a memory budget at p >= 1e5 needs calib.bin's
  // measured k_store; calibration islands (before calib.bin exists) plan from the setup: max(8, q90(pi_0 size) + 1, k_store)
  if (!calib && cfg.mem_budget && D.p >= 100000 && !(cfg.k_store > 0) && !cfg.k_store_optional)
    throw v4::Error(v4::Status::invalid_input, "run_island: a final island at p >= 1e5 needs k_store (the calibration-measured mean stored |S|, calib.bin)");
  // admission (manager Q3/Q4, review PR24 P2): plan_island (k = max(8, q90(pi_0 size) + 1, k_store); G = the largest
  // value <= 256 that fits). The step-boundary re-check uses the store's actual pool.
  MemSizes z; double k_est = 0; int G = 0;
  MemPlan mp = plan_island(D, st, cfg, &z, &k_est, &G);
  IslandConfig c2 = cfg; c2.G = G;
  if (cfg.mem_budget && mp.total > cfg.mem_budget) {   // deterministic refusal before any allocation
    IslandRun r; r.status = 3; r.r = (int)cfg.island; r.N = cfg.N; r.p = D.p; r.L = cfg.L; r.Hm = cfg.Hm; r.G_used = G; r.mem_plan = mem_plan_text(mp);
    r.reason = "mem_budget: predicted peak " + std::to_string(mp.total >> 20) + " MiB > budget " + std::to_string(cfg.mem_budget >> 20) + " MiB [" + r.mem_plan + "]";
    return r;
  }
  IslandEngine<A> E(D, st, nb, c2);
  E.k_est = k_est; E.msz = z; E.res.G_used = G; E.res.mem_plan = mem_plan_text(mp);
  E.top.reserve_staging(k_est);   // no reallocation transients of the staging area (the plan counts its full capacity)
  if (cfg.leaders) { E.lead0.reserve_staging(k_est); E.lead1.reserve_staging(k_est); }
  return E.run();
}

}  // namespace v4::island
