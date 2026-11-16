// ledger.cpp -- Ledger (INTERFACES §4.2).
#include "v4/ledger.h"
#include "v4/status.h"

namespace v4 {

const char* phase_name(int ph) {
  static const char* nm[] = {"table", "pilot", "diag", "final_init", "final_bridge", "burn_in", "measured", "local", "inherited", "test", "ls0"};
  return (ph >= 0 && ph < N_PHASE) ? nm[ph] : "?";
}
const char* mech_name(int me) {
  static const char* nm[] = {"table", "init_draw", "gibbs_held", "gibbs_flip", "uswap", "nswap", "indep", "local_scan", "inherited"};
  return (me >= 0 && me < N_MECH) ? nm[me] : "?";
}

void Ledger::init(const LedgerConfig& c) {
  cfg = c;
  has_hpm = false; hpmS.clear(); hpmF = NEG_INF_L(); hpm_logm = 0; hpm_ev = EventCtx();
  // core/cpp/v3_ledger.h:76-78: top 40p + 1 (HPM order), leaders 20p (lexicographic ties).
  top.init(40ull * (uint64_t)c.p + 1, Order::HPM);
  lead0.init(c.leaders ? 20ull * (uint64_t)c.p : 0, Order::LEX);
  lead1.init(c.leaders ? 20ull * (uint64_t)c.p : 0, Order::LEX);
  for (auto& r : logical) for (auto& x : r) x = 0;
  for (auto& r : fresh) for (auto& x : r) x = 0;
  island_best.assign((size_t)c.islands + 1, NEG_INF_L());
}

// core/cpp/v3_ledger.h:84-88 (offer_hpm): strict order hpm_better. For the same model, the smaller event key keeps the
// provenance, so out-of-order (threaded / label-major) arrival gives the serial "first score" provenance.
void Ledger::offer_hpm(ModelView S, double F, double logm, const EventCtx& ev) {
  if (!has_hpm || hpm_better(F, S, hpmF, hpmS)) {
    has_hpm = true; hpmS.assign(S.begin(), S.end()); hpmF = F; hpm_logm = logm; hpm_ev = ev;
  } else if (F == hpmF && same_model(S, hpmS) && ev.key < hpm_ev.key) {
    hpm_ev = ev;
  }
}
// core/cpp/v3_ledger.h:89-94 (offer_stores), copied: lead1 is ordered by F (= log gamma_1 order).
void Ledger::offer_stores(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev) {
  offer_hpm(S, F, logm, ev);
  top.offer(F, S, h);
  lead0.offer(lg0, S, h);
  lead1.offer(F, S, h);
}
// core/cpp/v3_ledger.h:104-113 (event), copied with the island taken from the event key.
void Ledger::event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev, bool is_fresh) {
  if (ev.phase < 0 || ev.phase >= N_PHASE || ev.mech < 0 || ev.mech >= N_MECH) throw Error(Status::internal_error, "ledger: bad phase/mech");
  logical[ev.phase][ev.mech]++;
  if (is_fresh && cfg.fresh_counters) fresh[ev.phase][ev.mech]++;
  int r = ev.island();
  bool own = r >= 1 && r <= cfg.islands &&
             (ev.phase == PH_FINAL_INIT || ev.phase == PH_FINAL_BRIDGE || ev.phase == PH_BURN_IN || ev.phase == PH_MEASURED ||
              ev.phase == PH_PILOT || ev.phase == PH_DIAG);
  if (own && F > island_best[(size_t)r]) island_best[(size_t)r] = F;
  if (is_fresh) offer_stores(S, h, F, lg0, logm, ev);
}

void Ledger::merge(const Ledger& o) {
  if (o.cfg.p != cfg.p || o.cfg.islands != cfg.islands) throw Error(Status::internal_error, "ledger merge: config mismatch");
  if (o.has_hpm) offer_hpm(o.hpmS, o.hpmF, o.hpm_logm, o.hpm_ev);
  top.merge(o.top); lead0.merge(o.lead0); lead1.merge(o.lead1);
  for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) { logical[a][b] += o.logical[a][b]; fresh[a][b] += o.fresh[a][b]; }
  for (size_t r = 0; r < island_best.size(); ++r) if (o.island_best[r] > island_best[r]) island_best[r] = o.island_best[r];
}

}  // namespace v4
