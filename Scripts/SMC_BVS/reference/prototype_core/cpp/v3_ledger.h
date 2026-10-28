// v3_ledger.h -- operational bookkeeping of scored models: HPM running best, near-tie store, score leaders,
// logical/fresh score counters, island bests, dump of scored models.
// CORE_SPEC v2 §7 (HPM, stores), §6 (`dump_scored`), §8.6 (counters); rulings R2, R3, R5, R9; M §6.10.
#pragma once
#include "v3_start.h"

namespace v3 {

// PH_TEST: events of the step/round testing samplers (v3_step_sample, v3_round_sample; code review S-2).
enum Phase { PH_TABLE = 0, PH_PILOT, PH_DIAG, PH_FINAL_INIT, PH_FINAL_BRIDGE, PH_BURN_IN, PH_MEASURED, PH_LOCAL, PH_INHERITED, PH_TEST, N_PHASE };
// Gibbs events are split (lead ruling R15): gibbs_held = the current state counted as scored under SR (not
// re-evaluated); gibbs_flip = the other feasible configuration S u j or S \ j (scored).
enum Mech { ME_TABLE = 0, ME_INIT, ME_GIBBS_HELD, ME_GIBBS_FLIP, ME_USWAP, ME_NSWAP, ME_INDEP, ME_LOCAL, ME_INHERITED, N_MECH };
inline const char* phase_name(int ph) {
  static const char* nm[] = {"table", "pilot", "diag", "final_init", "final_bridge", "burn_in", "measured", "local", "inherited", "test"};
  return nm[ph];
}
inline const char* mech_name(int me) {
  static const char* nm[] = {"table", "init_draw", "gibbs_held", "gibbs_flip", "uswap", "nswap", "indep", "local_scan", "inherited"};
  return nm[me];
}

// Where a score event happened. island: 1..R for final islands, 0 for tables / final local search.
// stage: bridge stage t (0 for initial draws; T for terminal rounds); round: index within the phase
// (bridge: t; burn-in 1..L; measured 1..4; local: move number); particle 1-based; position 1-based in the round order
// (local: index within the scan); phi: temperature of the step.
// iter: calibration rebuild iteration (0 = pilot and its local search; k = diagnostic islands and local search of
// rebuild iteration k); -1 = tables, final run, testing interfaces.
struct EventCtx { int phase = 0, tier = 0, island = 0, stage = 0, round = 0, particle = 0, position = 0, iter = -1; double phi = 0; };

// Top-k store of distinct models by a value, with a strict total tie order (so the std::set also finds a model by
// (value, S): a model's value is a deterministic function of the model).
struct TopEntry { double v; std::vector<int> S; };
struct TopCmp {
  bool hpm_order;  // true: exact ties -> smaller size, then lexicographic (HPM rule); false: lexicographic only (R3)
  bool operator()(const TopEntry& a, const TopEntry& b) const {
    if (a.v != b.v) return a.v > b.v;
    if (hpm_order && a.S.size() != b.S.size()) return a.S.size() < b.S.size();
    return lex_less(a.S, b.S);
  }
};
struct TopStore {
  size_t cap = 0;
  TopCmp cmp{true};
  std::set<TopEntry, TopCmp> s{TopCmp{true}};
  void init(size_t c, bool hpm_order) { cap = c; cmp = TopCmp{hpm_order}; s = std::set<TopEntry, TopCmp>(cmp); }
  // returns true if inserted
  bool offer(double v, const std::vector<int>& S) {
    if (cap == 0) return false;
    TopEntry e{v, S};
    if (s.size() >= cap && !cmp(e, *s.rbegin())) return false;  // quick reject: not better than the worst
    if (s.count(e)) return false;
    s.insert(e);
    if (s.size() > cap) s.erase(std::prev(s.end()));
    return true;
  }
  bool would_enter(double v, const std::vector<int>& S) const {
    if (cap == 0) return false;
    if (s.size() < cap) return true;
    TopEntry e{v, S};
    return cmp(e, *s.rbegin());
  }
};

struct DumpRec {
  double F = 0, logm = 0, lg0 = 0;
  uint32_t cnt[N_PHASE][N_MECH] = {};
  EventCtx first; int first_mech = 0;
};

class Observer;  // defined in v3_observer.h

class Ledger {
 public:
  const Data* D;
  int islands = 4;
  bool has_hpm = false;
  std::vector<int> hpmS; double hpmF = NEG_INF, hpm_logm = 0; EventCtx hpm_ev; int hpm_mech = 0;
  TopStore top, lead0, lead1;  // top-(40p+1) by F (HPM order); top 20p by log gamma_0; top 20p by log gamma_1 (R3)
  uint64_t logical[N_PHASE][N_MECH] = {}, fresh[N_PHASE][N_MECH] = {};
  std::vector<double> island_best;  // R5: max F over models scored by the island's own particles and proposals
  bool dump = false;
  std::map<std::vector<int>, DumpRec> dumpmap;
  Observer* obs = nullptr;

  explicit Ledger(const Data* d, int R) : D(d), islands(R) {
    size_t p = d->p;
    top.init(40 * p + 1, true); lead0.init(20 * p, false); lead1.init(20 * p, false);
    island_best.assign(R + 1, NEG_INF);
  }

  // HPM running best (M §6.10): strict order hpm_better; provenance = the event at which it became the best
  // (that event is necessarily the model's first score: a model that loses once can never win later).
  void offer_hpm(const std::vector<int>& S, double F, double logm, const EventCtx& ev, int mech) {
    if (!has_hpm || hpm_better(F, S, hpmF, hpmS)) {
      has_hpm = true; hpmS = S; hpmF = F; hpm_logm = logm; hpm_ev = ev; hpm_mech = mech;
    }
  }
  void offer_stores(const std::vector<int>& S, double F, double lg0, double logm, const EventCtx& ev, int mech) {
    offer_hpm(S, F, logm, ev, mech);
    top.offer(F, S);
    lead0.offer(lg0, S);
    lead1.offer(F, S);  // log gamma_1 = log varpi + log m (R3); ordering identical to F
  }

  // One logical score event. `fresh` = freshly evaluated (cache miss or uncached source). Stores are idempotent, so
  // they are updated only on fresh evaluations: a cache hit or a held current state was processed when first scored.
  // (The cache is owned by the run, so every cached model was processed by this ledger.)
  inline void event(const std::vector<int>& S, double F, double lg0, double logm, bool is_fresh, bool is_held,
                    const EventCtx& ev, int mech);
};

}  // namespace v3
