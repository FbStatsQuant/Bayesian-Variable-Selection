// tail.h -- WP4: local search with threaded scans (final local search from the merged HPM, and LS0 from the start mode),
// spec §1 row 5, §3 "merge and tail"; = core/cpp/v3_engine.h:370-420 (Engine::local_search) and
// core/cpp/v3_core.cpp:453-481 (final run tail).
//
// Serial semantics kept exactly:
//  * centre scored (emitted as an event only for LS0); scan order flips j = 0..p-1 (additions beyond K skipped, no
//    position used), then swaps (j in S ascending) x (l outside S ascending); position = 1-based index in that order;
//  * best neighbour: largest F, exact ties -> plain lexicographic order; a move only on a strict F increase;
//    at most `ell` moves, then one further scan; local_limit iff that scan still finds a strict improvement;
//  * every scanned model is a score event (phase local or ls0, mechanism local_scan) offered to the ledger.
// Threads: the scan's label space is cut into fixed chunks (chunk size is a parameter, not part of the result),
// processed in WAVES of 4 x threads chunks. Each chunk keeps its best neighbour and the offers that can still enter a
// store (filter: value >= the store's monotone cut-off, INTERFACES §4.1 -- exact, entries below it never enter); after
// each wave the chunk results are applied serially in chunk order and the buffers are freed, so at most one wave of
// chunk buffers (<= 4 x threads x chunk offers) exists at any time (bounded buffers, INTERFACES §7(4); review PR16 F3).
// The best-neighbour reduction is a max under a strict total order, so it keeps the tie rule
// (core/cpp/v3_engine.h:392). Offers are applied with their serial event keys, so stores and HPM provenance equal the
// serial run (INTERFACES §4.2).
// Numerical failure (a scorer exception, or a NaN score): offers before the first failing position are applied, as in
// the serial run, so the HPM-so-far equals v3's exactly; then NumericalFailure is rethrown and the caller returns no
// estimate (GUARD-W). (A ThreadLedger with eager flushes could not keep this: a flushed buffer may hold positions after
// the failure. Hence explicit wave buffers here.)
#pragma once
#include <algorithm>
#include <cmath>
#include <string>
#include <vector>
#include "v4/ledger.h"
#include "v4/records.h"
#include "v4/rng.h"
#include "v4/status.h"
#include "v4/wp4_par.h"

namespace v4 {
namespace merge {

// LocalArchive = v4::LocalArchive (records.h; core/cpp/v3_engine.h:46-53).
inline std::string strip_status_prefix(const std::string& m) {   // Error::what() = "<status>: <message>"
  const std::string pre = "numerical_failure: ";
  return m.rfind(pre, 0) == 0 ? m.substr(pre.size()) : m;
}

struct TailSettings {
  int threads = 1;
  size_t chunk = 2048;     // labels per chunk (not part of the result)
  int K = 0;               // model size cap
  int p = 0;
  int tier = 0;
  const Zobrist* zob = nullptr;   // model hashes for the stores (Data::zob)
  // Event keys (INTERFACES v0.1.5 §4.2): the final search uses (LOCAL, frozen tier, -1, UNIT_LOCAL), LS0 (LS0, ...). A
  // calibration search (core/cpp/v3_core.cpp:642, 689: after the pilot / the diagnostic islands of rebuild k) uses
  // (CALIB, tier e, iter k, UNIT_LOCAL): set calib = true and iter = k.
  bool calib = false;
  int iter = -1;
};

namespace detail {
struct Offer { Model S; double F, lg0, logm; uint32_t position; };
struct ChunkOut {
  bool have = false; Model bestS; double bestF = 0;
  std::vector<Offer> offers;
  long n_eval = 0;
  bool failed = false; uint32_t fail_pos = 0; std::string fail_msg;
};
}  // namespace detail

// One local search. phase = PH_LOCAL (seg SG_LOCAL) or PH_LS0 (seg SG_LS0). Factory as in calib::rescore_V.
template <class Factory>
LocalArchive local_search(const Model& centre, int ell, bool emit_centre, int phase, Ledger& led, Factory& fac,
                          const TailSettings& ts) {
  LocalArchive A;
  const uint8_t seg = ts.calib ? SG_CALIB : phase == PH_LS0 ? SG_LS0 : SG_LOCAL;
  auto make_ev = [&](uint32_t stage, uint32_t round, uint32_t position) {
    EventCtx ev; ev.phase = phase; ev.mech = ME_LOCAL; ev.phi = 1.0;
    ev.key.seg = seg; ev.key.tier = (uint8_t)ts.tier; ev.key.iter = (int8_t)(ts.calib ? ts.iter : -1); ev.key.unit = UNIT_LOCAL; ev.key.xph = X_INIT;
    ev.key.stage = stage; ev.key.round = round; ev.key.position = position;
    return ev;
  };
  Model C = centre; double CF;
  {
    auto ev = fac.make(); double lm, lg0, d;
    ev(C, lm, lg0, d, CF);
    if (emit_centre) led.event(C, ts.zob->hash(C), CF, lg0, lm, make_ev(0, 0, 0), true);
  }
  A.centre = C; A.centre_F = CF;
  const int p = ts.p, K = ts.K;
  while (true) {
    const uint32_t stage = (uint32_t)A.scanned.size() + 1, round = (uint32_t)A.moves;
    const int k = (int)C.size();
    const bool add_ok = k < K;
    // label space: t in [0, p) flips; t in [p, p + k*p) swaps (a = (t-p)/p member index, l = (t-p)%p)
    const size_t n_lab = (size_t)p + (size_t)k * (size_t)p;
    const uint32_t n_flip_eval = add_ok ? (uint32_t)p : (uint32_t)k;
    auto in_C = [&](int j) { return std::binary_search(C.begin(), C.end(), j); };
    auto below = [&](int j) { return (uint32_t)(std::lower_bound(C.begin(), C.end(), j) - C.begin()); };  // members < j
    const size_t nc = n_chunks(n_lab, ts.chunk);
    const size_t wave = 4 * (size_t)std::max(1, ts.threads);
    auto passes = [](const Store& st, double v) { return st.cap > 0 && v >= st.cutoff(); };
    bool failed = false; std::string fmsg;
    bool have = false; Model bestS; double bestF = 0; long n_eval = 0;
    std::vector<detail::ChunkOut> co(std::min(wave, nc));
    for (size_t w0 = 0; w0 < nc && !failed; w0 += wave) {
      const size_t w1 = std::min(nc, w0 + wave);
      for (auto& o : co) o = detail::ChunkOut();
      for_chunks(w1 - w0, 1, ts.threads, [&](size_t i, size_t, size_t) {
        const size_t c = w0 + i, b = c * ts.chunk, e = std::min(n_lab, b + ts.chunk);
        detail::ChunkOut& o = co[i];
        auto ev = fac.make();
        Model Q; double lm, lg0, d, F;
        for (size_t t = b; t < e; ++t) {
          uint32_t pos;
          if (t < (size_t)p) {
            int j = (int)t;
            bool in = in_C(j);
            if (!in && !add_ok) continue;
            Q = C;
            if (in) Q.erase(std::lower_bound(Q.begin(), Q.end(), j));
            else Q.insert(std::lower_bound(Q.begin(), Q.end(), j), j);
            pos = add_ok ? (uint32_t)j + 1 : below(j) + 1;
          } else {
            size_t u = t - (size_t)p; int a = (int)(u / (size_t)p); int l = (int)(u % (size_t)p);
            if (in_C(l)) continue;
            int j = C[a];
            Q = C;
            Q.erase(std::lower_bound(Q.begin(), Q.end(), j));
            Q.insert(std::lower_bound(Q.begin(), Q.end(), l), l);
            pos = n_flip_eval + (uint32_t)a * (uint32_t)(p - k) + ((uint32_t)l - below(l)) + 1;
          }
          try {
            ev(Q, lm, lg0, d, F);
            if (std::isnan(F) || std::isnan(lg0)) throw NumericalFailure("NaN score in the local search");   // review PR16 F11
          } catch (const NumericalFailure& ex) { o.failed = true; o.fail_pos = pos; o.fail_msg = ex.what(); return; }
          o.n_eval++;
          if (!o.have || F > o.bestF || (F == o.bestF && lex_less(Q, o.bestS))) { o.bestS = Q; o.bestF = F; o.have = true; }
          if (passes(led.top, F) || passes(led.lead0, lg0) || passes(led.lead1, F)) o.offers.push_back({Q, F, lg0, lm, pos});
        }
      });
      // serial combination of this wave in chunk order; buffers freed before the next wave
      for (size_t i = 0; i < w1 - w0 && !failed; ++i) {
        detail::ChunkOut& o = co[i];
        for (auto& x : o.offers) led.offer_stores(x.S, ts.zob->hash(x.S), x.F, x.lg0, x.logm, make_ev(stage, round, x.position));
        n_eval += o.n_eval;
        if (o.failed) { failed = true; fmsg = o.fail_msg; break; }
        if (o.have && (!have || o.bestF > bestF || (o.bestF == bestF && lex_less(o.bestS, bestS)))) { bestS = o.bestS; bestF = o.bestF; have = true; }
      }
    }
    led.logical[phase][ME_LOCAL] += (uint64_t)n_eval;
    A.n_eval += n_eval;
    if (failed) throw NumericalFailure(strip_status_prefix(fmsg));
    A.scanned.push_back(C); A.scanned_F.push_back(CF); A.scan_complete.push_back(1);
    A.scan_size.push_back((int)(n_flip_eval + (uint32_t)k * (uint32_t)(p - k)));
    if (have && bestF > CF) {   // strict F improvement only (R14)
      if (A.moves >= ell) { A.local_limit = true; A.termination = "move_limit"; A.returned = bestS; A.returned_F = bestF; break; }
      C = bestS; CF = bestF; A.moves++; A.path.push_back(C); A.path_F.push_back(CF);
    } else {
      A.termination = "no_improvement"; A.local_certified = true; A.returned = C; A.returned_F = CF; break;
    }
  }
  led.compact();
  return A;
}

}  // namespace merge
}  // namespace v4
