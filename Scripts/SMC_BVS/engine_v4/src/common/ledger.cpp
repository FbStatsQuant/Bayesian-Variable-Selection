// ledger.cpp -- Ledger, ThreadLedger (INTERFACES §4.2).
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

void Tally::init_tally(const LedgerConfig& c) {
  cfg = c;
  has_hpm = false; hpmS.clear(); hpmF = LEDGER_NEG_INF; hpm_logm = 0; hpm_ev = EventCtx();
  for (auto& r : logical) for (auto& x : r) x = 0;
  for (auto& r : fresh) for (auto& x : r) x = 0;
  island_best.assign((size_t)c.islands + 1, LEDGER_NEG_INF);
}
// core/cpp/v3_ledger.h:84-88 (offer_hpm): strict order hpm_better. For the same model, the smaller event key keeps the
// provenance, so out-of-order (threaded / label-major) arrival gives the serial "first score" provenance.
void Tally::offer_hpm(ModelView S, double F, double logm, const EventCtx& ev) {
  if (!has_hpm || hpm_better(F, S, hpmF, hpmS)) {
    has_hpm = true; hpmS.assign(S.begin(), S.end()); hpmF = F; hpm_logm = logm; hpm_ev = ev;
  } else if (F == hpmF && same_model(S, hpmS) && ev.key < hpm_ev.key) {
    hpm_ev = ev;
  }
}
void Tally::merge_tally(const Tally& o) {
  if (o.cfg.p != cfg.p || o.cfg.islands != cfg.islands) throw Error(Status::internal_error, "ledger merge: config mismatch");
  if (o.has_hpm) offer_hpm(o.hpmS, o.hpmF, o.hpm_logm, o.hpm_ev);
  for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) { logical[a][b] += o.logical[a][b]; fresh[a][b] += o.fresh[a][b]; }
  for (size_t r = 0; r < island_best.size(); ++r) if (o.island_best[r] > island_best[r]) island_best[r] = o.island_best[r];
}
// core/cpp/v3_ledger.h:104-111 (event: counters and island_best), copied with the island taken from the event key.
void Tally::count(double F, const EventCtx& ev, bool is_fresh) {
  if (ev.phase < 0 || ev.phase >= N_PHASE || ev.mech < 0 || ev.mech >= N_MECH) throw Error(Status::internal_error, "ledger: bad phase/mech");
  logical[ev.phase][ev.mech]++;
  if (is_fresh && cfg.fresh_counters) fresh[ev.phase][ev.mech]++;
  int r = ev.island();
  bool own = r >= 1 && r <= cfg.islands &&
             (ev.phase == PH_FINAL_INIT || ev.phase == PH_FINAL_BRIDGE || ev.phase == PH_BURN_IN || ev.phase == PH_MEASURED ||
              ev.phase == PH_PILOT || ev.phase == PH_DIAG);
  if (own && F > island_best[(size_t)r]) island_best[(size_t)r] = F;
}

void Ledger::init(const LedgerConfig& c) {
  init_tally(c);
  // core/cpp/v3_ledger.h:76-78: top 40p + 1 (HPM order), leaders 20p (lexicographic ties).
  top.init(40ull * (uint64_t)c.p + 1, Order::HPM);
  lead0.init(c.leaders ? 20ull * (uint64_t)c.p : 0, Order::LEX);
  lead1.init(c.leaders ? 20ull * (uint64_t)c.p : 0, Order::LEX);
}
// core/cpp/v3_ledger.h:89-94 (offer_stores), copied: lead1 is ordered by F (= log gamma_1 order).
void Ledger::offer_stores(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev) {
  offer_hpm(S, F, logm, ev);
  top.offer(F, S, h);
  lead0.offer(lg0, S, h);
  lead1.offer(F, S, h);
}
// core/cpp/v3_ledger.h:104-113 (event), copied.
void Ledger::event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev, bool is_fresh) {
  count(F, ev, is_fresh);
  if (is_fresh) offer_stores(S, h, F, lg0, logm, ev);
}
void Ledger::absorb(ThreadLedger& t) {
  if (t.isl_ != this) throw Error(Status::internal_error, "absorb: thread ledger belongs to another island");
  std::lock_guard<std::mutex> g(*mu_);
  t.flush_all_locked();
  merge_tally(t);
  t.init_tally(t.cfg);
}
void Ledger::merge(const Ledger& o) {
  merge_tally(o);
  top.merge(o.top); lead0.merge(o.lead0); lead1.merge(o.lead1);
}

void OfferBuffer::push(double value, ModelView S, uint64_t h) {
  v.push_back(value); hash.push_back(h); off.push_back((uint32_t)pool.size()); len.push_back((uint16_t)S.k);
  pool.insert(pool.end(), S.begin(), S.end());
}
void OfferBuffer::flush_into(Store& s) {
  for (size_t i = 0; i < v.size(); ++i) s.offer(v[i], ModelView(pool.data() + off[i], len[i]), hash[i]);
  clear();
}

ThreadLedger::ThreadLedger(Ledger& island, size_t buf_cap) : isl_(&island), cap_(buf_cap ? buf_cap : 1) {
  init_tally(island.cfg);
}
void ThreadLedger::offer(int which, Store& s, double value, ModelView S, uint64_t h) {
  if (s.cap == 0) return;
  if (value != value) throw Error(Status::internal_error, "store: NaN value (breaks the strict order)");
  if (value < s.cutoff()) { ++dropped_by_cutoff; return; }   // strictly worse than c entries already offered
  if (S.k > 65535) throw Error(Status::internal_error, "store: model too large");
  buf_[which].push(value, S, h);
  if (buf_[which].size() >= cap_) {
    std::lock_guard<std::mutex> g(isl_->mutex());
    buf_[which].flush_into(s);
    ++flushes;
  }
}
void ThreadLedger::flush_all_locked() {
  buf_[0].flush_into(isl_->top); buf_[1].flush_into(isl_->lead0); buf_[2].flush_into(isl_->lead1);
}
void ThreadLedger::event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev, bool is_fresh) {
  count(F, ev, is_fresh);
  if (!is_fresh) return;
  offer_hpm(S, F, logm, ev);
  offer(0, isl_->top, F, S, h);
  offer(1, isl_->lead0, lg0, S, h);
  offer(2, isl_->lead1, F, S, h);
}

}  // namespace v4
