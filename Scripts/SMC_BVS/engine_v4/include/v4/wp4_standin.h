// wp4_standin.h -- TEMPORARY stand-ins for the WP1-owned headers that WP4 codes against (INTERFACES v0.1 §2, §4, §7):
// Model/ModelView, lex_less/hpm_better, Phase/Mech/Segment/EventKey/EventCtx, Store, Ledger, Status/Error.
// When WP1's headers are on the include path (detected by __has_include(<v4/ledger.h>)), they are used instead and
// this file defines nothing but the adapters WP4 needs. Delete the stand-in block once WP1 is merged.
// The stand-in semantics follow INTERFACES §4 exactly (order-free stores, smaller-EventKey provenance, sums, maxima);
// its storage layout is NOT WP1's flat layout (no pool), which is irrelevant to WP4's logic.
#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <limits>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_set>
#include <vector>

#if __has_include(<v4/ledger.h>) && !defined(V4_WP4_FORCE_STANDIN)
#include <v4/types.h>
#include <v4/model.h>
#include <v4/store.h>
#include <v4/ledger.h>
#include <v4/status.h>
#define V4_WP4_USING_WP1 1
#else
#define V4_WP4_USING_WP1 0

namespace v4 {

const double NEG_INF = -std::numeric_limits<double>::infinity();

// ---- §2 models -------------------------------------------------------------------------------------------------
using Model = std::vector<int32_t>;
struct ModelView { const int32_t* idx; uint32_t k; };
inline ModelView view(const Model& S) { return ModelView{S.data(), (uint32_t)S.size()}; }

// core/cpp/v3_util.h:111-126 (copied): strict lexicographic order; HPM order (F desc, |S| asc, lex asc).
inline bool lex_less(const Model& a, const Model& b) {
  return std::lexicographical_compare(a.begin(), a.end(), b.begin(), b.end());
}
inline bool hpm_better(double F1, const Model& S1, double F2, const Model& S2) {
  if (F1 > F2) return true;
  if (F1 < F2) return false;
  if (S1.size() != S2.size()) return S1.size() < S2.size();
  return lex_less(S1, S2);
}

// ---- §7 statuses ------------------------------------------------------------------------------------------------
enum class Status : uint8_t { completed = 0, resource_limit = 1, numerical_failure = 2, invalid_input = 3, io_error = 4, internal_error = 5 };
inline const char* status_name(Status s) {
  static const char* nm[] = {"completed", "resource_limit", "numerical_failure", "invalid_input", "io_error", "internal_error"};
  return nm[(int)s];
}
struct Error : std::runtime_error {
  Status st;
  Error(Status s, const std::string& m) : std::runtime_error(m), st(s) {}
};
struct NumericalFailure : Error {
  explicit NumericalFailure(const std::string& m) : Error(Status::numerical_failure, "numerical_failure: " + m) {}
};
// fit level: the first that applies in the order invalid_input, internal_error, numerical_failure, resource_limit,
// io_error, completed (spec §6).
inline Status fit_status(const std::vector<Status>& v) {
  const Status order[] = {Status::invalid_input, Status::internal_error, Status::numerical_failure, Status::resource_limit, Status::io_error};
  for (Status s : order) for (Status x : v) if (x == s) return s;
  return Status::completed;
}

// ---- §4.2 phases, mechanisms, event keys -------------------------------------------------------------------------
// = core/cpp/v3_ledger.h:11-22 (names identical)
enum Phase { PH_TABLE = 0, PH_PILOT, PH_DIAG, PH_FINAL_INIT, PH_FINAL_BRIDGE, PH_BURN_IN, PH_MEASURED, PH_LOCAL, PH_INHERITED, PH_TEST, PH_LS0, N_PHASE };
enum Mech { ME_TABLE = 0, ME_INIT, ME_GIBBS_HELD, ME_GIBBS_FLIP, ME_USWAP, ME_NSWAP, ME_INDEP, ME_LOCAL, ME_INHERITED, N_MECH };
inline const char* phase_name(int ph) {
  static const char* nm[] = {"table", "pilot", "diag", "final_init", "final_bridge", "burn_in", "measured", "local", "inherited", "test", "ls0"};
  return nm[ph];
}
inline const char* mech_name(int me) {
  static const char* nm[] = {"table", "init_draw", "gibbs_held", "gibbs_flip", "uswap", "nswap", "indep", "local_scan", "inherited"};
  return nm[me];
}
enum Segment : uint8_t { SG_TABLE = 0, SG_INHERITED = 1, SG_CALIB = 2, SG_FINAL = 3, SG_LOCAL = 4, SG_LS0 = 5 };
enum XphKey : uint8_t { XK_NONE = 0, XK_INIT = 0, XK_BRIDGE = 2, XK_BURN = 3, XK_MEASURED = 4 };
const uint32_t UNIT_LOCAL = 0xFFFFFFFFu;
struct EventKey {
  uint8_t seg = 0, tier = 0; int8_t iter = -1; uint32_t unit = 0;
  uint8_t xph = 0; uint32_t stage = 0, round = 0, particle = 0, position = 0; uint8_t sub = 0;
  auto tie() const { return std::tie(seg, tier, iter, unit, xph, stage, round, particle, position, sub); }
  bool operator<(const EventKey& o) const { return tie() < o.tie(); }
  bool operator==(const EventKey& o) const { return tie() == o.tie(); }
};
struct EventCtx { int phase = 0, mech = 0; EventKey key; double phi = 0; };

// ---- §4.1 store -------------------------------------------------------------------------------------------------
enum class Order : uint8_t { HPM, LEX };
struct StoreEntry { double v; Model S; };
struct Store {
  uint64_t cap = 0; Order ord = Order::HPM;
  std::vector<StoreEntry> e;      // sorted, unique, <= cap after compact()
  std::vector<StoreEntry> buf;    // offers since the last compact()
  Store() = default;
  Store(uint64_t c, Order o) : cap(c), ord(o) {}
  bool less(const StoreEntry& a, const StoreEntry& b) const {   // "a ranks before b"; core/cpp/v3_ledger.h:35-42
    if (a.v != b.v) return a.v > b.v;
    if (ord == Order::HPM && a.S.size() != b.S.size()) return a.S.size() < b.S.size();
    return lex_less(a.S, b.S);
  }
  void offer(double v, const Model& S) {
    if (cap == 0) return;
    buf.push_back({v, S});
    if (buf.size() >= std::max<uint64_t>(cap, 1024)) compact();
  }
  void compact() {
    if (buf.empty()) return;
    for (auto& x : buf) e.push_back(std::move(x));
    buf.clear();
    std::sort(e.begin(), e.end(), [&](const StoreEntry& a, const StoreEntry& b) { return less(a, b); });
    e.erase(std::unique(e.begin(), e.end(), [](const StoreEntry& a, const StoreEntry& b) { return a.v == b.v && a.S == b.S; }), e.end());
    if (e.size() > cap) e.resize(cap);
  }
  void merge(const Store& o) { for (auto& x : o.e) offer(x.v, x.S); for (auto& x : o.buf) offer(x.v, x.S); compact(); }
  // after compact(): cap not reached or strictly better than the worst kept entry
  bool would_enter(double v, const Model& S) const {
    if (cap == 0) return false;
    if (e.size() < cap) return true;
    return less(StoreEntry{v, S}, e.back());
  }
  size_t size() const { return e.size(); }
  bool full() const { return e.size() >= cap; }
};

// ---- §4.2 ledger ------------------------------------------------------------------------------------------------
struct Ledger {
  bool has_hpm = false; Model hpmS; double hpmF = NEG_INF, hpm_logm = 0; EventCtx hpm_ev;
  Store top, lead0, lead1;
  uint64_t logical[N_PHASE][N_MECH] = {};
  std::vector<double> island_best;   // index r = 0..R'
  Ledger() = default;
  Ledger(uint64_t p, int Rp, bool leaders) : top(40 * p + 1, Order::HPM), lead0(leaders ? 20 * p : 0, Order::LEX),
                                             lead1(leaders ? 20 * p : 0, Order::LEX), island_best(Rp + 1, NEG_INF) {}
  // HPM: hpm_better; for the same model the smaller EventKey wins provenance (serial "first score" rule).
  void offer_hpm(const Model& S, double F, double logm, const EventCtx& ev) {
    if (!has_hpm || hpm_better(F, S, hpmF, hpmS)) { has_hpm = true; hpmS = S; hpmF = F; hpm_logm = logm; hpm_ev = ev; }
    else if (S == hpmS && ev.key < hpm_ev.key) hpm_ev = ev;
  }
  void offer_stores(const Model& S, double F, double lg0, double logm, const EventCtx& ev) {
    offer_hpm(S, F, logm, ev);
    top.offer(F, S); lead0.offer(lg0, S); lead1.offer(F, S);
  }
  // core/cpp/v3_ledger.h:104-112: counts; island_best for the island's own events; offers when `offer`.
  void event(const Model& S, double F, double lg0, double logm, const EventCtx& ev, bool offer) {
    logical[ev.phase][ev.mech]++;
    bool own = (ev.phase == PH_FINAL_INIT || ev.phase == PH_FINAL_BRIDGE || ev.phase == PH_BURN_IN || ev.phase == PH_MEASURED ||
                ev.phase == PH_PILOT || ev.phase == PH_DIAG);
    uint32_t r = ev.key.unit;
    if (own && r >= 1 && r < island_best.size() && F > island_best[r]) island_best[r] = F;
    if (offer) offer_stores(S, F, lg0, logm, ev);
  }
  void compact() { top.compact(); lead0.compact(); lead1.compact(); }
  void merge(const Ledger& o) {
    if (o.has_hpm) offer_hpm(o.hpmS, o.hpmF, o.hpm_logm, o.hpm_ev);
    top.merge(o.top); lead0.merge(o.lead0); lead1.merge(o.lead1);
    for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) logical[a][b] += o.logical[a][b];
    if (island_best.size() < o.island_best.size()) island_best.resize(o.island_best.size(), NEG_INF);
    for (size_t r = 0; r < o.island_best.size(); ++r) island_best[r] = std::max(island_best[r], o.island_best[r]);
  }
};

}  // namespace v4
#endif
