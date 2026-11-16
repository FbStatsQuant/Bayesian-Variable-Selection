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
// Threads: the scan's label space is cut into fixed chunks (chunk size is a parameter, not part of the result); each
// chunk keeps its best neighbour and the offers that can enter a store (filter: would_enter at the scan start, which is
// exact because stores only improve); chunk results are combined serially in chunk order. The best-neighbour reduction
// is a max under a strict total order, so it keeps the tie rule (core/cpp/v3_engine.h:392). Offers are applied with
// their serial event keys, so stores and HPM provenance equal the serial run (INTERFACES §4.2).
// Numerical failure: offers before the first failing position are applied (as in the serial run), then
// NumericalFailure is rethrown; the caller returns no estimate (GUARD-W).
#pragma once
#include <algorithm>
#include <string>
#include <vector>
#include "wp4_par.h"
#include "wp4_standin.h"

namespace v4 {
namespace merge {

// = core/cpp/v3_engine.h:46-53
struct LocalArchive {
  Model centre; double centre_F = 0;
  std::vector<Model> path; std::vector<double> path_F;
  std::vector<Model> scanned; std::vector<double> scanned_F; std::vector<int> scan_complete, scan_size;
  std::string termination; bool local_limit = false, local_certified = false;
  Model returned; double returned_F = 0;
  int moves = 0; long n_eval = 0;
};

struct TailSettings {
  int threads = 1;
  size_t chunk = 2048;     // labels per chunk (not part of the result)
  int K = 0;               // model size cap
  int p = 0;
  int tier = 0;
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
  const uint8_t seg = phase == PH_LS0 ? SG_LS0 : SG_LOCAL;
  auto make_ev = [&](uint32_t stage, uint32_t round, uint32_t position) {
    EventCtx ev; ev.phase = phase; ev.mech = ME_LOCAL; ev.phi = 1.0;
    ev.key.seg = seg; ev.key.tier = (uint8_t)ts.tier; ev.key.iter = -1; ev.key.unit = UNIT_LOCAL;
    ev.key.stage = stage; ev.key.round = round; ev.key.position = position;
    return ev;
  };
  Model C = centre; double CF;
  {
    auto ev = fac.make(); double lm, lg0, d;
    ev(C, lm, lg0, d, CF);
    if (emit_centre) led.event(C, CF, lg0, lm, make_ev(0, 0, 0), true);
  }
  A.centre = C; A.centre_F = CF;
  const int p = ts.p, K = ts.K;
  while (true) {
    const uint32_t stage = (uint32_t)A.scanned.size() + 1, round = (uint32_t)A.moves;
    led.compact();   // the would_enter filter needs compacted stores
    const int k = (int)C.size();
    const bool add_ok = k < K;
    // label space: t in [0, p) flips; t in [p, p + k*p) swaps (a = (t-p)/p member index, l = (t-p)%p)
    const size_t n_lab = (size_t)p + (size_t)k * (size_t)p;
    const uint32_t n_flip_eval = add_ok ? (uint32_t)p : (uint32_t)k;
    auto in_C = [&](int j) { return std::binary_search(C.begin(), C.end(), j); };
    auto below = [&](int j) { return (uint32_t)(std::lower_bound(C.begin(), C.end(), j) - C.begin()); };  // members < j
    const size_t nc = n_chunks(n_lab, ts.chunk);
    std::vector<detail::ChunkOut> co(nc);
    for_chunks(n_lab, ts.chunk, ts.threads, [&](size_t c, size_t b, size_t e) {
      detail::ChunkOut& o = co[c];
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
        try { ev(Q, lm, lg0, d, F); }
        catch (const NumericalFailure& ex) { o.failed = true; o.fail_pos = pos; o.fail_msg = ex.what(); return; }
        o.n_eval++;
        if (!o.have || F > o.bestF || (F == o.bestF && lex_less(Q, o.bestS))) { o.bestS = Q; o.bestF = F; o.have = true; }
        if (led.top.would_enter(F, Q) || led.lead0.would_enter(lg0, Q) || led.lead1.would_enter(F, Q))
          o.offers.push_back({Q, F, lg0, lm, pos});
      }
    });
    // serial combination in chunk order
    bool failed = false; std::string fmsg;
    bool have = false; Model bestS; double bestF = 0; long n_eval = 0;
    for (size_t c = 0; c < nc && !failed; ++c) {
      detail::ChunkOut& o = co[c];
      for (auto& x : o.offers) led.offer_stores(x.S, x.F, x.lg0, x.logm, make_ev(stage, round, x.position));
      n_eval += o.n_eval;
      if (o.failed) { failed = true; fmsg = o.fail_msg; break; }
      if (o.have && (!have || o.bestF > bestF || (o.bestF == bestF && lex_less(o.bestS, bestS)))) { bestS = o.bestS; bestF = o.bestF; have = true; }
    }
    led.logical[phase][ME_LOCAL] += (uint64_t)n_eval;
    A.n_eval += n_eval;
    if (failed) throw NumericalFailure(fmsg.rfind("numerical_failure: ", 0) == 0 ? fmsg.substr(19) : fmsg);
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
