// island_impl.h -- template implementation of v4::island::run_island (included by island_bit.cpp, island_a.cpp).
#pragma once
#include <omp.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstdio>
#include <filesystem>
#include <memory>
#include "v4/island/island.h"
#include "v4/provenance.h"

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

// [arch] bit l set iff lo < pos[l] < hi, for 16 positions (AVX-512: two unsigned compares)
static inline uint32_t in_open_range16(const uint32_t* pos, uint32_t lo, uint32_t hi) {
#if defined(__AVX512F__)
  const __m512i v = _mm512_loadu_si512((const void*)pos);
  return (uint32_t)(_mm512_cmpgt_epu32_mask(v, _mm512_set1_epi32((int)lo)) & _mm512_cmplt_epu32_mask(v, _mm512_set1_epi32((int)hi)));
#else
  uint32_t r = 0; for (int l = 0; l < 16; ++l) r |= (uint32_t)((pos[l] > lo) & (pos[l] < hi)) << l; return r;
#endif
}
// [arch] the labels jj of a tile (nbv of them, positions pos[jj]) with lo < pos[jj] < hi, OR-ed into the bit words w
static inline void or_range_bits(const uint32_t* pos, int nbv, uint32_t lo, uint32_t hi, uint64_t* w) {
  int jj = 0;
  for (; jj + 16 <= nbv; jj += 16) w[jj >> 6] |= (uint64_t)in_open_range16(pos + jj, lo, hi) << (jj & 63);
  for (; jj < nbv; ++jj) w[jj >> 6] |= (uint64_t)((pos[jj] > lo) & (pos[jj] < hi)) << (jj & 63);
}

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
  v4::LedgerConfig lc; lc.p = r.p; lc.islands = std::max(1, r.r); lc.leaders = false; lc.fresh_counters = false;
  o.led.init(lc);
  o.led.has_hpm = r.hpm.has; o.led.hpmS = r.hpm.S; o.led.hpmF = r.hpm.F; o.led.hpm_logm = r.hpm.logm;
  o.led.hpm_ev.phase = r.hpm.phase; o.led.hpm_ev.mech = r.hpm.mech; o.led.hpm_ev.key = r.hpm.key;
  std::memcpy(o.led.logical, r.logical, sizeof(r.logical));
  if (r.r >= 0 && (size_t)r.r < o.led.island_best.size()) o.led.island_best[r.r] = r.island_best;
  for (size_t i = 0; i < r.top_v.size(); ++i) o.led.top.offer(r.top_v[i], v4::ModelView(r.top_pool.data() + r.top_off[i], r.top_len[i]), r.top_hash[i]);
  o.led.top.compact();
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
  // compat (manager Q2): every uniform is the next draw of the island's v3 stream, in core's serial call order
  std::unique_ptr<v4::CompatSource> csrc;
  TopStore lead0, lead1;
  std::vector<double> rb_d;   // compat: core's cumulative double RB accumulator (core/cpp/v3_engine.h:128, :350-364)
  inline double U(const Address& a) { return csrc ? csrc->u(a) : uniform_at(a); }
  double logZ = 0; double k_est = 8; MemSizes msz;
  KernelStats ks_prev;   // verbose per-round deltas
  uint64_t ckpt_writes = 0;
  std::chrono::steady_clock::time_point last_ckpt;

  struct RoundCtx { uint8_t xph; uint32_t ustage; uint32_t ev_stage, ev_round; int phase; double phi; bool measured; };

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
    std::string m = fail.msg; int kd = fail.kind; fail.has = false;
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
      csrc.reset(new v4::CompatSource(cfg.seed, v4::compat_stream(R_FINAL, (uint8_t)cfg.tier, cfg.island)));
    }
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
    Address a; a.seed = cfg.seed; a.role = R_FINAL; a.tier = 0; a.iter = 0; a.island = cfg.island;
    a.xph = xph; a.stage = ustage; a.particle = particle1; a.position = position; a.slot = slot; return a;
  }
  // INTERFACES v0.1.5 §4.2: final island r: (FINAL, frozen tier, iter -1, r, xph, stage, round, particle, q, sub);
  // sub = within-step ordinal: Gibbs held 0 (never offered), flip 1; U / N / I proposals and the initial draw 0.
  inline EventKey key(const RoundCtx& rc, uint32_t particle1, uint32_t position, uint8_t sub = 0) const {
    EventKey k; k.seg = SG_FINAL; k.tier = (uint8_t)cfg.tier; k.iter = -1; k.unit = cfg.island; k.xph = rc.xph;
    k.stage = rc.ev_stage; k.round = rc.ev_round; k.particle = particle1; k.position = position; k.sub = sub; return k;
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
  bool step_nongibbs(int lab, const Particle& Pc, int i, uint32_t pos, const RoundCtx& rc, ThreadLedger& L, BitScorer& sc, Particle& out) {
    const uint32_t i1 = (uint32_t)i + 1;
    auto U = [&](uint32_t slot) { return this->U(addr(rc.xph, rc.ustage, i1, pos, slot)); };
    int k = (int)Pc.S.size();
    if (lab == p) {   // U: uniform swap
      if (k == 0 || k == p) { L.ms.us_self++; return false; }
      L.ms.us_exec++;
      int j = Pc.S[(int)std::floor(U(SLOT_MOVE_J) * k)];
      int mth = (int)std::floor(U(SLOT_MOVE_L) * (p - k));
      int l = mth; for (int s : Pc.S) { if (s <= l) ++l; else break; }   // mth non-member in increasing order
      Model T = Pc.S; sorted_erase(T, j); sorted_insert(T, l);
      fill(out, T, sc.score(T).logm);
      offer_particle(L, out, rc.phase, ME_USWAP, key(rc, i1, pos));
      double la = lgphi(out, rc.phi) - lgphi(Pc, rc.phi);
      double alpha = (la >= 0) ? 1.0 : pm::exp(la);
      if (U(SLOT_ACCEPT) < alpha) { L.ms.us_acc++; return true; }
      return false;
    }
    if (lab <= p + cfg.B) {   // N_b: neighbour swap
      if (k == 0) { L.ms.ns_self++; return false; }
      L.ms.ns_exec++;
      int j = Pc.S[(int)std::floor(U(SLOT_MOVE_J) * k)];
      std::vector<int> cand;
      for (int64_t e = nb.ptr[j]; e < nb.ptr[j + 1]; ++e) if (!contains(Pc.S, nb.idx[e])) cand.push_back(nb.idx[e]);
      if (cand.empty()) { L.ms.ns_noscore++; return false; }
      int l = cand[(int)std::floor(U(SLOT_MOVE_L) * cand.size())];
      Model T = Pc.S; sorted_erase(T, j); sorted_insert(T, l);
      int back = 0; for (int64_t e = nb.ptr[l]; e < nb.ptr[l + 1]; ++e) if (!contains(T, nb.idx[e])) ++back;
      fill(out, T, sc.score(T).logm);
      offer_particle(L, out, rc.phase, ME_NSWAP, key(rc, i1, pos));
      double la = lgphi(out, rc.phi) - lgphi(Pc, rc.phi) + pm::log((double)cand.size()) - pm::log((double)back);
      double alpha = (la >= 0) ? 1.0 : pm::exp(la);
      if (U(SLOT_ACCEPT) < alpha) { L.ms.ns_acc++; return true; }
      return false;
    }
    // I: independence proposal from pi_0
    L.ms.in_exec++;
    Model T;
    if (csrc) draw_pi0(st, [&](uint32_t slot) { return U(slot); }, T);   // compat: core's serial consumption
    else {
      const Address a0 = addr(rc.xph, rc.ustage, i1, pos, 0);
      const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
      draw_pi0_fast(st, [&](uint32_t slot) { return U(slot); },
                    [&](const uint32_t* sl, double* out) { philox8_word(ctr.data(), kk.data(), 0, sl, out); }, T);
    }
    fill(out, T, sc.score(T).logm);
    offer_particle(L, out, rc.phase, ME_INDEP, key(rc, i1, pos));
    double la = rc.phi * (out.d - Pc.d);
    double alpha = (la >= 0) ? 1.0 : pm::exp(la);
    if (U(SLOT_ACCEPT) < alpha) { L.ms.in_acc++; return true; }
    return false;
  }

  // Round order (core/cpp/v3_engine.h:195-200): Fisher-Yates, uniform of step i at slot m-1-i.
  void draw_order(const RoundCtx& rc, int i, uint32_t* ord) {
    for (int t = 0; t < m; ++t) ord[t] = (uint32_t)t;
    if (csrc) {   // compat: one uniform at a time from the serial stream
      uint32_t slot = 0;
      for (int t = m - 1; t >= 1; --t) {
        int jj = (int)std::floor(U(addr(rc.xph, rc.ustage, (uint32_t)i + 1, 0, slot_of(v4::SK_ORDER, slot++))) * (t + 1));
        std::swap(ord[t], ord[jj]);
      }
      return;
    }
    // L5: the same Fisher-Yates swaps with the uniforms of slots d = 0..m-2 computed 8 at a time and the swap targets of
    // the next block prefetched (the addresses are fixed, so the targets are known ahead)
    const Address a0 = addr(rc.xph, rc.ustage, (uint32_t)i + 1, 0, slot_of(v4::SK_ORDER, 0));
    const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
    const int nd = m - 1;
    int jcur[8], jnext[8]; uint32_t sl[8]; double u8[8];
    auto block = [&](int d0, int* jj) {
      for (int l = 0; l < 8; ++l) sl[l] = slot_of(v4::SK_ORDER, (uint32_t)std::min(d0 + l, std::max(0, nd - 1)));
      philox8_word(ctr.data(), kk.data(), 0, sl, u8);
      for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); jj[l] = (int)std::floor(u8[l] * (t + 1)); __builtin_prefetch(&ord[jj[l]], 1); }
    };
    if (nd > 0) block(0, jcur);
    for (int d0 = 0; d0 < nd; d0 += 8) {
      if (d0 + 8 < nd) block(d0 + 8, jnext);
      for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); std::swap(ord[t], ord[jcur[l]]); }
      std::memcpy(jcur, jnext, sizeof jcur);
    }
  }

  // --- particle-major reference: core/cpp/v3_engine.h:202-214 for particle i ---------------------------------
  void pm_round(int i, const RoundCtx& rc, ThreadLedger& L, BitScorer& sc, std::vector<u128>* rb) {
    // a worker drops a stale snapshot at every particle boundary (review m3; the PM analogue of the tile-start release)
    if (L.buf.snap && L.buf.snap_gen != top.gen.load(std::memory_order_relaxed)) { L.buf.snap.reset(); L.buf.snap_gen = ~0ull; }
    std::vector<uint32_t> ord(m); draw_order(rc, i, ord.data());
    Particle& Pi = P[i]; const uint32_t i1 = (uint32_t)i + 1;
    SupportCache s; bool cache_ok = false; Particle tmp;
    uint32_t pos_cur = 0;
    try {
    if (cfg.test_oom_pass >= 0 && (int)rc.ev_round == cfg.test_oom_pass && i == 0) throw std::bad_alloc();   // test hook
    for (int pos0 = 0; pos0 < m; ++pos0) {
      const uint32_t pos = (uint32_t)pos0 + 1; int lab = (int)ord[pos0];
      pos_cur = pos;
      if (lab < p) {
        // Gibbs (core/cpp/v3_engine.h:113-132): held state counted, other configuration scored and offered
        L.ms.gibbs++; L.logical[rc.phase][ME_GIBBS_HELD]++;
        if (!cache_ok) { build_support(D, st, sc, s, Pi.S, Pi.h, Pi.logm, Pi.lg0, Pi.d, rc.phi); cache_ok = true; }
        bool in = contains(Pi.S, lab);
        double lm = 0, o = 0;
        eval1<A>(D, st, sc, s, lab, lm, o);
        if (o < 0) { fail.record((uint32_t)i, fail_msg(rc, i1, pos, gibbs_fail(lab))); return; }   // consumed failed score
        bool has_other = in || s.add_ok;
        if (!has_other) L.ms.gibbs_cap++;   // addition refused at |S| = K: one event (held), INTERFACES v0.1.5 §4.2
        Model T;
        if (has_other) {
          T = Pi.S; if (in) sorted_erase(T, lab); else sorted_insert(T, lab);
          double F = D.logprior[T.size()] + lm;
          const double lg0T = cfg.leaders ? D.logprior[T.size()] + st.comp(T) : std::numeric_limits<double>::quiet_NaN();
          L.scored(T.data(), (uint32_t)T.size(), Pi.h ^ D.zob.key[lab], F, lm, rc.phase, ME_GIBBS_FLIP, key(rc, i1, pos, 1), lg0T);
        }
        if (rb) { if (csrc) rb_d[lab] += o; else (*rb)[lab] += fix63(o); }   // compat: core's double sum, serial order
        double u = U(addr(rc.xph, rc.ustage, i1, pos, SLOT_ACCEPT));
        bool include = u < o;
        if (include != in) { fill(Pi, T, canonical(sc, T, lm)); L.ms.gibbs_change++; cache_ok = false; }
      } else {
        if (step_nongibbs(lab, Pi, i, pos, rc, L, sc, tmp)) { Pi = tmp; cache_ok = false; }
      }
    }
    } catch (const v4::NumericalFailure& e) { fail.record((uint32_t)i, fail_msg(rc, i1, pos_cur, e.what())); }
    catch (const std::bad_alloc&) { fail.record(UINT32_MAX, "out of memory inside a parallel region", FK_RESOURCE); }
  }

  // --- label-major round for the particles [g0, g0 + gN) ------------------------------------------------------
  struct GroupBuf {
    std::vector<uint32_t> ord, inv;             // gN x m
    std::vector<std::vector<std::pair<uint32_t, int>>> ng;   // per particle: (position, label) of U/N/I labels, sorted
    std::vector<uint32_t> q, e; std::vector<uint8_t> done, etype; std::vector<Particle> pending;
    std::vector<std::atomic<uint32_t>> fmin;
    std::vector<SupportCache> sup; std::vector<int> sup_of;
    std::vector<std::vector<int>> sup_parts;     // particles (group-local, ascending) per support
    std::vector<int> act;                        // active columns
    avec<double> XA;                             // |act| x n
    std::vector<double> lbuf, obuf;              // nsup x p
  };
  GroupBuf gb;

  void lm_group(int g0, int gN, const RoundCtx& rc) {
    auto& KS = res.ks;
    auto t0 = std::chrono::steady_clock::now();
    auto lap = [&](double& acc) { auto t1 = std::chrono::steady_clock::now(); acc += std::chrono::duration<double>(t1 - t0).count(); t0 = t1; };
    gb.ord.resize((size_t)gN * m); gb.inv.resize((size_t)gN * m); gb.ng.assign(gN, {});
    #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
    for (int gi = 0; gi < gN; ++gi) oom_guard([&] {
      uint32_t* ord = &gb.ord[(size_t)gi * m]; uint32_t* inv = &gb.inv[(size_t)gi * m];
      draw_order(rc, g0 + gi, ord);
      for (int t = 0; t < m; ++t) { if (t + 16 < m) __builtin_prefetch(&inv[ord[t + 16]], 1); inv[ord[t]] = (uint32_t)t + 1; }   // 1-based positions
      for (int lab = p; lab < m; ++lab) gb.ng[gi].push_back({inv[lab], lab});
      std::sort(gb.ng[gi].begin(), gb.ng[gi].end());
    });
    if (fail_fatal()) return;
    gb.q.assign(gN, 0); gb.e.assign(gN, 0); gb.done.assign(gN, 0); gb.etype.assign(gN, 0); gb.pending.assign(gN, Particle());
    std::vector<std::atomic<uint32_t>> fm(gN); gb.fmin.swap(fm);
    KS.particle_rounds += gN;
    lap(KS.t_orders);
    std::vector<int> active;
    while (true) {
      active.clear(); for (int gi = 0; gi < gN; ++gi) if (!gb.done[gi]) active.push_back(gi);
      if (active.empty()) break;
      KS.passes++; KS.particle_sweeps += active.size();
      // distinct supports: (hash, log m bits, S)  [class A: one model can carry different path values]
      std::vector<int> idx = active;
      auto lmbits = [&](int gi) { uint64_t b; std::memcpy(&b, &P[g0 + gi].logm, 8); return b; };
      std::sort(idx.begin(), idx.end(), [&](int a, int b) {
        const Particle &x = P[g0 + a], &y = P[g0 + b];
        if (x.h != y.h) return x.h < y.h;
        if (lmbits(a) != lmbits(b)) return lmbits(a) < lmbits(b);
        if (x.S != y.S) return lex_less(x.S, y.S);
        return a < b;
      });
      gb.sup_of.assign(gN, -1); gb.sup_parts.clear();
      std::vector<int> rep;
      for (size_t t = 0; t < idx.size(); ++t) {
        int gi = idx[t];
        if (t == 0 || P[g0 + gi].h != P[g0 + idx[t - 1]].h || lmbits(gi) != lmbits(idx[t - 1]) || P[g0 + gi].S != P[g0 + idx[t - 1]].S) {
          rep.push_back(gi); gb.sup_parts.push_back({});
        }
        gb.sup_of[gi] = (int)rep.size() - 1; gb.sup_parts.back().push_back(gi);
      }
      for (auto& v : gb.sup_parts) std::sort(v.begin(), v.end());
      const int nsup = (int)rep.size();
      KS.supports += nsup; KS.support_label_pairs += (uint64_t)nsup * p;
      if ((int)gb.sup.size() < nsup) gb.sup.resize(nsup);
      #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
      for (int s = 0; s < nsup; ++s) oom_guard([&] {
        const Particle& x = P[g0 + rep[s]];
        build_support(D, st, *scorers[omp_get_thread_num()], gb.sup[s], x.S, x.h, x.logm, x.lg0, x.d, rc.phi);
      });
      if (fail_fatal()) return;
      // active columns: members of fast supports that can add
      gb.act.clear();
      for (int s = 0; s < nsup; ++s) { auto& c = gb.sup[s]; if (c.fast && c.add_ok) gb.act.insert(gb.act.end(), c.S.begin(), c.S.end()); else if (!c.fast) KS.slow_supports++; }
      std::sort(gb.act.begin(), gb.act.end()); gb.act.erase(std::unique(gb.act.begin(), gb.act.end()), gb.act.end());
      const int nA = (int)gb.act.size();
      for (int s = 0; s < nsup; ++s) {
        auto& c = gb.sup[s]; c.arow.assign(c.k, 0);
        if (c.fast && c.add_ok) for (int a = 0; a < c.k; ++a) c.arow[a] = (int)(std::lower_bound(gb.act.begin(), gb.act.end(), c.S[a]) - gb.act.begin());
      }
      gb.XA.resize((size_t)nA * D.n);
      for (int a = 0; a < nA; ++a) std::memcpy(&gb.XA[(size_t)a * D.n], D.col(gb.act[a]), sizeof(double) * D.n);
      if (gb.lbuf.size() < (size_t)nsup * p) {   // sized once to G p (review P2 / L5: growing re-zero-fills and reallocates)
        const size_t full = (size_t)std::max(nsup, std::min(cfg.G, cfg.N)) * p;
        gb.lbuf.clear(); gb.lbuf.shrink_to_fit(); gb.obuf.clear(); gb.obuf.shrink_to_fit();
        gb.lbuf.resize(full); gb.obuf.resize(full);
      }
      for (int gi : active) gb.fmin[gi].store(UINT32_MAX, std::memory_order_relaxed);
      if (cfg.bounded_scoring) {
        // [arch] deletion pre-scan. The deletion odds of the k members are in the support cache, so the first member
        // whose addressed uniform deletes it is known before any tile is scored: it bounds the particle's first change.
        // Same test as the tile scan below (member: change iff failed score or !(u < o)), same uniform address.
        for (int gi : active) {
          const SupportCache& c = gb.sup[gb.sup_of[gi]];
          const uint32_t* inv = &gb.inv[(size_t)gi * m]; const uint32_t qi = gb.q[gi]; uint32_t best = UINT32_MAX;
          const uint32_t i1 = (uint32_t)(g0 + gi) + 1;
          for (int a = 0; a < c.k; ++a) {
            const uint32_t pos = inv[c.S[a]];
            if (pos <= qi || pos >= best) continue;
            const double oj = c.del_odds[a];
            const double u = uniform_at(addr(rc.xph, rc.ustage, i1, pos, SLOT_ACCEPT));
            if (oj < 0 || !(u < oj)) best = pos;
          }
          gb.fmin[gi].store(best, std::memory_order_relaxed);
        }
      }
      lap(KS.t_build);

      // ---- phase A: scores, odds, first change per particle -------------------------------------------------
      #pragma omp parallel num_threads(NT)
      {
        BitScorer& sc = *scorers[omp_get_thread_num()];
        avec<double>& Pp = scratch_P[omp_get_thread_num()];   // persistent per thread (no allocation per pass)
        if (Pp.size() < (size_t)std::max(1, nA) * Bk + 8) Pp.resize((size_t)std::max(1, nA) * Bk + 8);
        std::vector<uint8_t> inm(Bk); std::vector<uint64_t> needw((size_t)Bk / 64); std::vector<int> nlist(Bk + 1); double tprod = 0; uint64_t nflip = 0;
        #pragma omp for schedule(dynamic, 1) nowait
        for (int ti = 0; ti < ntile; ++ti) oom_guard([&] {
          if (cfg.test_oom_pass >= 0 && (int)KS.passes == cfg.test_oom_pass + 1 && ti == 0) throw std::bad_alloc();   // test hook
          const int j0 = ti * Bk, nbv = std::min(Bk, p - j0);
          const double* Xtile = &Xt[(size_t)ti * Bk * D.n];
          // products P[a][jj] = sum_i x_{i,a} x_{i,j}, sequential in i (bits of the Gram entry)
          const double tp0 = omp_get_wtime();
          tile_products(gb.XA.data(), nA, D.n, Xtile, Bk, Pp.data(), products_block_of(cfg));
          tprod += omp_get_wtime() - tp0;
          for (int s = 0; s < nsup; ++s) {
            const SupportCache& c = gb.sup[s];
            double* lb = &gb.lbuf[(size_t)s * p]; double* ob = &gb.obuf[(size_t)s * p];
            std::fill(inm.begin(), inm.end(), 0);
            auto mlo = std::lower_bound(c.S.begin(), c.S.end(), j0), mhi = std::lower_bound(c.S.begin(), c.S.end(), j0 + nbv);
            for (auto it = mlo; it != mhi; ++it) { int a = (int)(it - c.S.begin()); inm[*it - j0] = 1; lb[*it] = c.del_logm[a]; ob[*it] = c.del_odds[a]; }
            if (!c.add_ok) {
              for (int jj = 0; jj < nbv; ++jj) if (!inm[jj]) { lb[j0 + jj] = std::numeric_limits<double>::quiet_NaN(); ob[j0 + jj] = 0.0; }
            } else if (!c.fast) {
              for (int jj = 0; jj < nbv; ++jj) if (!inm[jj]) eval1<A>(D, st, sc, c, j0 + jj, lb[j0 + jj], ob[j0 + jj]);
            } else if (cfg.bounded_scoring) {
              // [arch] bounded scoring. A non-member label j is scored for support s only if some particle i on s can
              // still consume it: q_i < inv_i[j] < fmin_i, where fmin_i is the particle's running first change (an upper
              // bound of its final e at any time: it only decreases). Every label a particle consumes (position <= e)
              // satisfied the test when its tile was scored, so phase B, the walk and the apply step read only values
              // computed in this pass; the others are never read (spec §3 rule 2). The needed labels of the tile are
              // packed 8 to a vector: a lane's result does not depend on the other lanes, so the bits are unchanged.
              thread_local std::vector<v8d> ub; if (ub.size() < (size_t)std::max(1, c.k)) ub.resize((size_t)std::max(1, c.k));
              v8d* u = ub.data();
              std::fill(needw.begin(), needw.end(), 0ull);
              for (int gi : gb.sup_parts[s])
                or_range_bits(&gb.inv[(size_t)gi * m + j0], nbv, gb.q[gi], gb.fmin[gi].load(std::memory_order_relaxed), needw.data());
              for (auto it = mlo; it != mhi; ++it) needw[(*it - j0) >> 6] &= ~(1ull << ((*it - j0) & 63));   // members: cached deletions
              int cnt = 0;
              for (size_t w = 0; w < needw.size(); ++w) for (uint64_t b = needw[w]; b; b &= b - 1) nlist[cnt++] = (int)(w * 64) + __builtin_ctzll(b);
              nflip += (uint64_t)cnt;
              for (int c0 = 0; c0 < cnt; c0 += 8) {
                const int nl = std::min(8, cnt - c0); const unsigned valid = (1u << nl) - 1u;
                int32_t j8[8], jj8[8];
                for (int l = 0; l < 8; ++l) { jj8[l] = nlist[c0 + std::min(l, nl - 1)]; j8[l] = j0 + jj8[l]; }
                for (int a = 0; a < c.k; ++a) {
                  const double* row = &Pp[(size_t)c.arow[a] * Bk];
                  v8d g; for (int l = 0; l < 8; ++l) g[l] = row[jj8[l]];
                  u[a] = g;
                }
                double lm8[8], o8[8];
                if constexpr (A == Arith::ClassA) {
                  eval8_add<A>(D, st, sc, c, 0, u, j8, valid, lm8, o8);
                } else {
                  unsigned rest = valid;
                  while (rest) {   // lanes sharing the sorted insertion position q
                    int l0 = __builtin_ctz(rest);
                    int q = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l0]) - c.S.begin());
                    unsigned lanes = 0;
                    for (int l = l0; l < 8; ++l) if ((rest >> l) & 1u) { int ql = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l]) - c.S.begin()); if (ql == q) lanes |= 1u << l; }
                    eval8_add<A>(D, st, sc, c, q, u, j8, lanes, lm8, o8);
                    rest &= ~lanes;
                  }
                }
                for (int l = 0; l < nl; ++l) { lb[j8[l]] = lm8[l]; ob[j8[l]] = o8[l]; }
              }
            } else {
              thread_local std::vector<v8d> ub; if (ub.size() < (size_t)std::max(1, c.k)) ub.resize((size_t)std::max(1, c.k));
              v8d* u = ub.data();
              for (int v = 0; v < nbv; v += 8) {
                int32_t j8[8]; unsigned valid = 0;
                for (int l = 0; l < 8; ++l) { int j = j0 + v + l; if (v + l < nbv && !inm[v + l]) valid |= 1u << l; j8[l] = std::min(j, p - 1); }
                if (!valid) continue;
                nflip += (uint64_t)__builtin_popcount(valid);
                for (int a = 0; a < c.k; ++a) u[a] = load8(&Pp[(size_t)c.arow[a] * Bk + v]);
                double lm8[8], o8[8];
                if constexpr (A == Arith::ClassA) {
                  eval8_add<A>(D, st, sc, c, 0, u, j8, valid, lm8, o8);
                } else {
                  unsigned rest = valid;
                  while (rest) {   // lanes sharing the sorted insertion position q
                    int l0 = __builtin_ctz(rest);
                    int q = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l0]) - c.S.begin());
                    unsigned lanes = 0;
                    for (int l = l0; l < 8; ++l) if ((rest >> l) & 1u) { int ql = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l]) - c.S.begin()); if (ql == q) lanes |= 1u << l; }
                    eval8_add<A>(D, st, sc, c, q, u, j8, lanes, lm8, o8);
                    rest &= ~lanes;
                  }
                }
                for (int l = 0; l < 8; ++l) if ((valid >> l) & 1u) { lb[j8[l]] = lm8[l]; ob[j8[l]] = o8[l]; }
              }
            }
            // first change of each particle on this support within the tile
            for (int gi : gb.sup_parts[s]) {
              const uint32_t* inv = &gb.inv[(size_t)gi * m];
              const uint32_t qi = gb.q[gi]; uint32_t best = gb.fmin[gi].load(std::memory_order_relaxed);
              const uint32_t i1 = (uint32_t)(g0 + gi) + 1;
              Address a0 = addr(rc.xph, rc.ustage, i1, 0, SLOT_ACCEPT);   // lanes set the position
              v4::Ctr4 ctr = v4::address_ctr(a0); v4::Key2 key = v4::address_key(a0);
              for (int v = 0; v < nbv; v += 8) {
                uint32_t pos8[8]; unsigned need = 0;
                for (int l = 0; l < 8; ++l) {
                  uint32_t pos = (v + l < nbv) ? inv[j0 + v + l] : 0;
                  pos8[l] = pos; if (pos > qi && pos < best) need |= 1u << l;
                }
                if (!need) continue;
                double u8[8];
                philox8_positions(ctr.data(), key.data(), pos8, u8);   // = uniform_at(addr(.., pos, slot 0)) per lane
                for (int l = 0; l < 8; ++l) if ((need >> l) & 1u) {
                  const int jj = v + l;
                  const double oj = ob[j0 + jj];   // ODDS_FAILED (< 0): a failed score is an event at its position
                  bool change = oj < 0 || (inm[jj] ? !(u8[l] < oj) : (u8[l] < oj));
                  if (change && pos8[l] < best) best = pos8[l];
                }
              }
              uint32_t cur = gb.fmin[gi].load(std::memory_order_relaxed);
              while (best < cur && !gb.fmin[gi].compare_exchange_weak(cur, best, std::memory_order_relaxed)) {}
            }
          }
        });
        #pragma omp atomic
        KS.t_products += tprod;
        #pragma omp atomic
        KS.flip_evals += nflip;
      }
      lap(KS.t_phaseA);
      if (fail_fatal()) return;

      // ---- walk: U/N/I labels in position order up to the first Gibbs change --------------------------------
      #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
      for (size_t t = 0; t < active.size(); ++t) {
        int gi = active[t]; ThreadLedger& L = *tl[omp_get_thread_num()]; BitScorer& sc = *scorers[omp_get_thread_num()];
        uint32_t f = gb.fmin[gi].load(std::memory_order_relaxed);
        gb.etype[gi] = 0; gb.e[gi] = (uint32_t)m;
        if (f != UINT32_MAX) { gb.etype[gi] = 1; gb.e[gi] = f; }
        const uint32_t i1 = (uint32_t)(g0 + gi) + 1; uint32_t pos_cur = 0;
        try {
          for (auto& pl : gb.ng[gi]) {
            if (pl.first <= gb.q[gi]) continue;
            if (pl.first >= f) break;
            pos_cur = pl.first;
            if (step_nongibbs(pl.second, P[g0 + gi], g0 + gi, pl.first, rc, L, sc, gb.pending[gi])) { gb.etype[gi] = 2; gb.e[gi] = pl.first; break; }
          }
          if (gb.etype[gi] == 1) {   // the event at f: a Gibbs change, or a consumed failed score
            int j = (int)gb.ord[(size_t)gi * m + f - 1];
            if (gb.obuf[(size_t)gb.sup_of[gi] * p + j] < 0) { fail.record(i1 - 1, fail_msg(rc, i1, f, gibbs_fail(j))); gb.etype[gi] = 3; }
          }
        } catch (const v4::NumericalFailure& e) { fail.record(i1 - 1, fail_msg(rc, i1, pos_cur, e.what())); gb.etype[gi] = 3; }
        catch (const std::bad_alloc&) { fail.record(UINT32_MAX, "out of memory inside a parallel region", FK_RESOURCE); gb.etype[gi] = 3; }
        if (gb.etype[gi] == 3) gb.e[gi] = gb.q[gi];   // a failed particle consumes nothing more (the round's events are discarded)
      }
      lap(KS.t_walk);
      if (top.defer && top.staged() >= (top.stage_limit + top.stage_hard) / 2) { release_snapshots(); top.compact_parallel(NT); }   // walk offers

      // ---- phase B: consumption of the Gibbs labels at positions (q, e] -------------------------------------
      // In waves of tiles; between waves (all threads free) the staging area is compacted in parallel once it passes
      // the trigger, so in-pass serial compactions are rare (content: a function of the offers only).
      // wave size bounded by offer volume (review P2): a wave offers at most nsup * tile entries per tile, so <= 0.1 c per
      // wave keeps the staging area below 0.375 c + 0.1 c < c/2 = stage_hard: the in-pass serial compaction (stale
      // snapshots, pool over-reservation) is unreachable in label-major
      const uint64_t per_tile = (uint64_t)std::max(1, nsup) * (uint64_t)Bk;
      const int wave = top.defer ? (int)std::max<uint64_t>(1, std::min<uint64_t>((uint64_t)std::max(64, 16 * NT), (top.cap / 10) / per_tile)) : ntile;
      for (int w0 = 0; w0 < ntile; w0 += wave) {
      const int w1 = std::min(ntile, w0 + wave);
      #pragma omp parallel num_threads(NT)
      {
        ThreadLedger& L = *tl[omp_get_thread_num()];
        Model T;
        std::vector<uint32_t> ncons_v(Bk), fpos_v(Bk); std::vector<int> first_v(Bk); std::vector<uint64_t> consw((size_t)Bk / 64);
        #pragma omp for schedule(dynamic, 1)
        for (int ti = w0; ti < w1; ++ti) oom_guard([&] {
          if (L.buf.snap && L.buf.snap_gen != top.gen.load(std::memory_order_relaxed)) { L.buf.snap.reset(); L.buf.snap_gen = ~0ull; }   // M2
          if (cfg.leaders) {
            if (L.buf0.snap && L.buf0.snap_gen != lead0.gen.load(std::memory_order_relaxed)) { L.buf0.snap.reset(); L.buf0.snap_gen = ~0ull; }
            if (L.buf1.snap && L.buf1.snap_gen != lead1.gen.load(std::memory_order_relaxed)) { L.buf1.snap.reset(); L.buf1.snap_gen = ~0ull; }
          }
          const int j0 = ti * Bk, nbv = std::min(Bk, p - j0);
          for (int s = 0; s < nsup; ++s) {
            const SupportCache& c = gb.sup[s];
            const double* lb = &gb.lbuf[(size_t)s * p]; const double* ob = &gb.obuf[(size_t)s * p];
            const auto& parts = gb.sup_parts[s];
            const double prior_add = c.add_ok ? D.logprior[c.k + 1] : 0.0, prior_del = c.k > 0 ? D.logprior[c.k - 1] : 0.0;
            // one consumed label: ncons particles of this support consumed it; `first` = the smallest of them, at fpos
            auto consume = [&](const int jj, const uint32_t ncons, const int first, const uint32_t fpos) {
              const int j = j0 + jj;
              const uint64_t fx = rc.measured ? fix63(ob[j]) : 0;
              if (rc.measured) rb_cur[j] += (u128)fx * ncons;
              L.logical[rc.phase][ME_GIBBS_HELD] += ncons; L.ms.gibbs += ncons;
              const double lm = lb[j];
              if (std::isnan(lm)) { L.ms.gibbs_cap += ncons; return; }   // infeasible addition: no flip event (core/cpp/v3_engine.h:119)
              const bool in = std::binary_search(c.S.begin(), c.S.end(), j);
              const double F = (in ? prior_del : prior_add) + lm;
              L.logical[rc.phase][ME_GIBBS_FLIP] += ncons - 1;   // + 1 inside scored()
              // leaders (review PR24 P1): log gamma_0 of the flip (same block sum as Start::comp) and each leader's own cut-off
              const double lg0 = cfg.leaders ? (in ? prior_del + comp_del(st, c, j) : prior_add + comp_add(st, c, j)) : 0.0;
              const bool lead_pass = cfg.leaders && (lg0 >= lead0.tau.load(std::memory_order_relaxed) || F >= lead1.tau.load(std::memory_order_relaxed));
              if (lead_pass || F >= top.tau.load(std::memory_order_relaxed) || F > L.island_best || F >= L.hpm.F) {
                T = c.S; if (in) sorted_erase(T, j); else sorted_insert(T, j);
                L.scored(T.data(), (uint32_t)T.size(), c.h ^ D.zob.key[j], F, lm, rc.phase, ME_GIBBS_FLIP, key(rc, (uint32_t)(g0 + first) + 1, fpos, 1),
                         cfg.leaders ? lg0 : std::numeric_limits<double>::quiet_NaN());
              } else {
                L.logical[rc.phase][ME_GIBBS_FLIP] += 1;
              }
            };
            if (cfg.bounded_scoring && parts.size() == 1) {
              // [arch] one particle on the support (the usual case once the particles have separated): its consumed
              // labels of the tile are the bits lo < position < e + 1; no per-label counting pass
              const int gi = parts[0]; const uint32_t qi = gb.q[gi], ei = gb.e[gi];
              if (ei > qi) {
                const uint32_t* inv = &gb.inv[(size_t)gi * m + j0];
                std::fill(consw.begin(), consw.end(), 0ull);
                or_range_bits(inv, nbv, qi, ei + 1, consw.data());
                for (size_t w = 0; w < consw.size(); ++w) for (uint64_t b = consw[w]; b; b &= b - 1) { const int jj = (int)(w * 64) + __builtin_ctzll(b); consume(jj, 1u, gi, inv[jj]); }
              }
            } else {
              // consumption counts per label: particles in ascending order, each reading its own inverse order row
              std::fill(ncons_v.begin(), ncons_v.begin() + nbv, 0u); std::fill(first_v.begin(), first_v.begin() + nbv, -1);
              for (int gi : parts) {
                const uint32_t* inv = &gb.inv[(size_t)gi * m + j0]; const uint32_t qi = gb.q[gi], ei = gb.e[gi];
                for (int jj = 0; jj < nbv; ++jj) {
                  uint32_t pos = inv[jj];
                  if (pos > qi && pos <= ei) { if (first_v[jj] < 0) { first_v[jj] = gi; fpos_v[jj] = pos; } ++ncons_v[jj]; }
                }
              }
              for (int jj = 0; jj < nbv; ++jj) if (ncons_v[jj]) consume(jj, ncons_v[jj], first_v[jj], fpos_v[jj]);
            }
          }
        });
      }
      if (top.defer && w1 < ntile && top.staged() >= (top.stage_limit + top.stage_hard) / 2) { release_snapshots(); top.compact_parallel(NT); }
      }   // waves
      lap(KS.t_phaseB);
      if (fail_fatal()) return;
      if (top.defer && top.staged() >= top.stage_limit) {   // pass boundary: all threads free
        release_snapshots();
        top.compact_parallel(NT);
      }
      lap(KS.t_compact_pass);

      // ---- apply the state changes ---------------------------------------------------------------------------
      // particles are independent: in parallel (L5; class A pays one canonical Bit score per accepted Gibbs change)
      #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
      for (size_t t = 0; t < active.size(); ++t) oom_guard([&] {
        const int gi = active[t]; const int th = omp_get_thread_num();
        Particle& x = P[g0 + gi];
        if (gb.etype[gi] == 1) {
          int j = (int)gb.ord[(size_t)gi * m + gb.e[gi] - 1];
          const SupportCache& c = gb.sup[gb.sup_of[gi]];
          double lm = gb.lbuf[(size_t)gb.sup_of[gi] * p + j];
          Model T = c.S; if (std::binary_search(T.begin(), T.end(), j)) sorted_erase(T, j); else sorted_insert(T, j);
          try { fill(x, T, canonical(*scorers[th], T, lm)); tl[th]->ms.gibbs_change++; }
          catch (const v4::NumericalFailure& e) { fail.record((uint32_t)(g0 + gi), fail_msg(rc, (uint32_t)(g0 + gi) + 1, gb.e[gi], e.what())); gb.etype[gi] = 3; }
        } else if (gb.etype[gi] == 2) {
          x = gb.pending[gi];
        }
        gb.q[gi] = gb.e[gi];
        if (gb.e[gi] == (uint32_t)m || gb.etype[gi] == 3) gb.done[gi] = 1;
      });
      if (fail_fatal()) return;
      lap(KS.t_apply);
    }
  }

  void round(const RoundCtx& rc) {
    if (rc.measured) std::fill(rb_cur.begin(), rb_cur.end(), (u128)0);
    if (cfg.kernel == KernelKind::LabelMajor) {
      int G = std::max(1, cfg.G);
      for (int g0 = 0; g0 < cfg.N; g0 += G) { lm_group(g0, std::min(G, cfg.N - g0), rc); throw_if_failed(); }
    } else {
      auto t0 = std::chrono::steady_clock::now();
      if (rc.measured) for (auto& v : rb_thread) std::fill(v.begin(), v.end(), (u128)0);
      #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
      for (int i = 0; i < cfg.N; ++i) {
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
        #pragma omp parallel for schedule(dynamic, 16) num_threads(NT)
        for (int i = 0; i < N; ++i) {
          int th = omp_get_thread_num(); Model S;
          if (csrc) draw_pi0(st, [&](uint32_t slot) { return U(addr(X_INIT, 0, (uint32_t)i + 1, 0, slot)); }, S);
          else {
            const Address a0 = addr(X_INIT, 0, (uint32_t)i + 1, 0, 0);
            const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
            draw_pi0_fast(st, [&](uint32_t slot) { return U(addr(X_INIT, 0, (uint32_t)i + 1, 0, slot)); },
                          [&](const uint32_t* sl, double* out) { philox8_word(ctr.data(), kk.data(), 0, sl, out); }, S);
          }
          try { fill(P[i], S, scorers[th]->score(S).logm); }
          catch (const v4::NumericalFailure& e) { fail.record((uint32_t)i, "initial draw, particle " + std::to_string(i + 1) + ": " + e.what()); continue; }
          catch (const std::bad_alloc&) { fail.record(UINT32_MAX, "out of memory inside a parallel region", FK_RESOURCE); continue; }
          EventKey k; k.seg = SG_FINAL; k.tier = (uint8_t)cfg.tier; k.iter = -1; k.unit = cfg.island; k.xph = X_INIT; k.particle = (uint32_t)i + 1;
          offer_particle(*tl[th], P[i], PH_FINAL_INIT, ME_INIT, k);
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
            grid.push_back(np.phi);
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
          RoundCtx rc{X_BRIDGE, (uint32_t)t, (uint32_t)t, (uint32_t)t, PH_FINAL_BRIDGE, phi_new, false};
          round(rc);
          sync_ledgers(); row.moves = take_moves(); row.distinct_moved = distinct();
          res.stages.push_back(row);
        } else if (step <= T + L) {   // burn-in round l
          int l = step - T;
          RoundCtx rc{X_BURN, (uint32_t)l, (uint32_t)T, (uint32_t)l, PH_BURN_IN, 1.0, false};
          round(rc);
          sync_ledgers(); res.terminal_moves.push_back(take_moves()); res.terminal_distinct.push_back(distinct());
        } else {   // measured round h with RB
          int h = step - T - L;
          RoundCtx rc{X_MEASURED, (uint32_t)h, (uint32_t)T, (uint32_t)h, PH_MEASURED, 1.0, true};
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
                         "phaseB %.2f s compaction %.2f s\n",
                         step, dt, steps, pairs, steps > 0 ? pairs / steps * m / std::max(1.0, (double)p) : 0.0, sweeps, rounds > 0 ? sweeps / rounds : 0.0,
                         (unsigned long long)(k.passes - ks_prev.passes), steps > 0 ? 1e9 * dt * NT / steps : 0.0, pairs > 0 ? 1e9 * dt * NT / pairs : 0.0,
                         pairs > 0 ? 1e9 * (k.t_products - ks_prev.t_products) / pairs : 0.0,
                         pairs > 0 ? 1e9 * (k.t_phaseA - ks_prev.t_phaseA) * NT / pairs : 0.0, k.t_phaseB - ks_prev.t_phaseB, top.t_compact - ks_prev.t_store_compact);
            std::fprintf(stderr, "  [arch] step %d: orders %.2f build %.2f phaseA %.2f (products %.2f thread-s) walk %.2f phaseB %.2f compact_pass %.2f apply %.2f | prev-step I1 check %.2f s\n",
                         step, k.t_orders - ks_prev.t_orders, k.t_build - ks_prev.t_build, k.t_phaseA - ks_prev.t_phaseA, k.t_products - ks_prev.t_products,
                         k.t_walk - ks_prev.t_walk, k.t_phaseB - ks_prev.t_phaseB, k.t_compact_pass - ks_prev.t_compact_pass, k.t_apply - ks_prev.t_apply,
                         k.t_check - ks_prev.t_check);
            std::fprintf(stderr, "  [arch] step %d: flip evaluations %.4g = %.3f per step (pairs %.3f per step)\n", step, (double)(k.flip_evals - ks_prev.flip_evals),
                         steps > 0 ? (double)(k.flip_evals - ks_prev.flip_evals) / steps : 0.0, steps > 0 ? pairs / steps : 0.0);
            ks_prev = k; ks_prev.t_store_compact = top.t_compact;
          }
          prev_t = now_t;
        }
        if (cfg.check_store) {   // [arch] timed: serial O(c) hash lookups after every step
          const auto tc0 = std::chrono::steady_clock::now();
          const bool ok = top.check_invariant();
          res.ks.t_check += std::chrono::duration<double>(std::chrono::steady_clock::now() - tc0).count();
          if (!ok) throw v4::Error(v4::Status::internal_error, "store invariant I1 violated");
        }
        if (over_budget(step)) { stop = true; break; }
        maybe_ckpt(step, stop);
      }
    } catch (const NumericalFailure& e) {
      res.status = 2; res.reason = e.what();
    } catch (const v4::Error& e) {
      if (e.st != v4::Status::resource_limit) throw;
      res.status = 3; res.reason = e.what();
    } catch (const std::bad_alloc&) {
      res.status = 3; res.reason = "resource_limit: out of memory";
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
    if (res.status == 0 || res.status == 1) {   // only a completed (or test-interrupted) island reports its store: a failed
                                                // or refused island may hold part of an unfinished round (GUARD-W, review m1)
      Kept& K = *top.k;      // moved, not copied (review m8b; the run is over)
      res.top_v = std::move(K.v); res.top_hash = std::move(K.hash); res.top_off = std::move(K.off); res.top_len = std::move(K.len); res.top_pool = std::move(K.pool);
    }
    res.ks.kept_live_max = kept_live_max().load();
    if (cfg.keep_terminal) for (auto& x : P) res.terminal.push_back(x.S);
    if (csrc) { res.compat = true; res.stream_count = csrc->g.count; }
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
  z.deferred = cfg.store_parallel_compact && cfg.threads > 1 && lm; z.leaders = cfg.leaders; z.compat = cfg.compat; z.inputs_bytes = cfg.inputs_bytes;
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

template <Arith A>
IslandRun run_island(const Data& D, const Start& st, const Neighbours& nb, const IslandConfig& cfg) {
  if (!cfg.adaptive && (cfg.grid.size() < 2 || cfg.grid.front() != 0.0 || cfg.grid.back() != 1.0)) throw v4::Error(v4::Status::invalid_input, "run_island: grid must run from 0 to 1");
  for (size_t i = 1; i < cfg.grid.size(); ++i) if (!(cfg.grid[i] > cfg.grid[i - 1])) throw v4::Error(v4::Status::invalid_input, "run_island: grid not strictly increasing (I3)");
  if (cfg.adaptive && !cfg.ckpt_path.empty()) throw v4::Error(v4::Status::invalid_input, "run_island: the adaptive schedule has no checkpoints");
  if (cfg.compat && (A != Arith::Bit || cfg.kernel != KernelKind::ParticleMajor || cfg.threads != 1 || cfg.adaptive))
    throw v4::Error(v4::Status::invalid_input, "run_island: compat mode needs Arith::Bit, the particle-major kernel, 1 thread and a fixed grid (serial v3 streams)");
  if (A == Arith::Bit && cfg.kernel == KernelKind::LabelMajor && !cfg.allow_test_kernels)
    throw v4::Error(v4::Status::invalid_input, "run_island: the bit-form label-major kernel is test-only (D-21, manager Q1); theory mode runs particle-major");
  if (cfg.stop_after_step >= 0 && cfg.ckpt_path.empty()) throw v4::Error(v4::Status::invalid_input, "run_island: stop_after_step needs a checkpoint path");
  if (cfg.G < 0 || cfg.G > 256) throw v4::Error(v4::Status::invalid_input, "run_island: G must be in 0..256 (0 = chosen by mem_budget; manager Q3)");
  if (D.p >= 100000 && !(cfg.k_store > 0) && !cfg.k_store_optional)   // review PR24 r1 / PR26 B1: no real run plans without it
    throw v4::Error(v4::Status::invalid_input, "run_island: p >= 1e5 needs k_store (the calibration-measured mean stored |S|, calib.bin)");
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
  return E.run();
}

}  // namespace v4::island
