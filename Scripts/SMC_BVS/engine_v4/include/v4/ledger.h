// ledger.h -- score events: HPM + provenance, stores, logical counters, island_best (INTERFACES §4.2; core/cpp/v3_ledger.h).
// One store-owning Ledger per island; one ThreadLedger per worker thread (small Tally + bounded offer buffers, no
// stores), absorbed into the island Ledger at stage ends in thread-index order. Quick rejects use the island store's
// monotone cutoff(). The island store's content equals the serial one (top-c is order-free).
#pragma once
#include <cstdint>
#include <memory>
#include <mutex>
#include <tuple>
#include <vector>
#include "v4/store.h"

namespace v4 {

// core/cpp/v3_ledger.h:11-23 (phase and mechanism enums and names), copied.
enum Phase { PH_TABLE = 0, PH_PILOT, PH_DIAG, PH_FINAL_INIT, PH_FINAL_BRIDGE, PH_BURN_IN, PH_MEASURED, PH_LOCAL, PH_INHERITED, PH_TEST, PH_LS0, N_PHASE };
enum Mech { ME_TABLE = 0, ME_INIT, ME_GIBBS_HELD, ME_GIBBS_FLIP, ME_USWAP, ME_NSWAP, ME_INDEP, ME_LOCAL, ME_INHERITED, N_MECH };
const char* phase_name(int ph);
const char* mech_name(int me);

enum Segment : uint8_t { SG_TABLE = 0, SG_INHERITED = 1, SG_CALIB = 2, SG_FINAL = 3, SG_LOCAL = 4, SG_LS0 = 5 };
constexpr uint32_t UNIT_LOCAL = 0xFFFFFFFFu;   // the local search of a (tier, iter) sorts after its islands

// Total order = lexicographic in field order = v3's serial execution order (INTERFACES §4.2).
struct EventKey {
  uint8_t seg = 0, tier = 0; int8_t iter = -1; uint32_t unit = 0;
  uint8_t xph = 0; uint32_t stage = 0, round = 0, particle = 0, position = 0; uint8_t sub = 0;
  auto tie() const { return std::tie(seg, tier, iter, unit, xph, stage, round, particle, position, sub); }
  bool operator<(const EventKey& o) const { return tie() < o.tie(); }
  bool operator==(const EventKey& o) const { return tie() == o.tie(); }
};
struct EventCtx {
  int phase = 0, mech = 0;   // reported labels (phase may be a calibration override, as v3)
  EventKey key;
  double phi = 0;
  int island() const { return key.unit == UNIT_LOCAL ? 0 : (int)key.unit; }
};

struct LedgerConfig { int32_t p = 0; int32_t islands = 4; bool leaders = true; bool fresh_counters = true; };
constexpr double LEDGER_NEG_INF = -__builtin_huge_val();

// The small part of a ledger: HPM + provenance, counters, island maxima. Merges are order-free.
struct Tally {
  LedgerConfig cfg;
  bool has_hpm = false; Model hpmS; double hpmF = LEDGER_NEG_INF, hpm_logm = 0; EventCtx hpm_ev;
  uint64_t logical[N_PHASE][N_MECH] = {}, fresh[N_PHASE][N_MECH] = {};
  std::vector<double> island_best;   // r = 0..islands

  void init_tally(const LedgerConfig& c);
  void offer_hpm(ModelView S, double F, double logm, const EventCtx& ev);
  void merge_tally(const Tally& o);
  // counters + island_best of one event (core/cpp/v3_ledger.h:104-111)
  void count(double F, const EventCtx& ev, bool is_fresh);
};

class ThreadLedger;

class Ledger : public Tally {
 public:
  Store top, lead0, lead1;   // top-(40p+1) by F (HPM order); top 20p by lg0 (LEX); top 20p by F (LEX)

  Ledger() = default;
  explicit Ledger(const LedgerConfig& c) { init(c); }
  void init(const LedgerConfig& c);
  // Serial use. One logical score event (core/cpp/v3_ledger.h:104-113). fresh = freshly evaluated: compat counts it and
  // offers to the HPM and stores only then; production passes fresh = true for every consumed score (no cache, OD-3).
  void event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev, bool fresh);
  void offer_stores(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev);
  void absorb(ThreadLedger& t);   // flush t's buffers into the stores, merge t's tally, reset t (thread-index order)
  void merge(const Ledger& o);    // whole ledgers: stores by top-c of the union + merge_tally
  void compact() { top.compact(); lead0.compact(); lead1.compact(); }
  std::mutex& mutex() { return *mu_; }

 private:
  std::shared_ptr<std::mutex> mu_ = std::make_shared<std::mutex>();
  friend class ThreadLedger;
};

// A bounded buffer of offers for one store.
struct OfferBuffer {
  std::vector<double> v; std::vector<uint64_t> hash; std::vector<uint32_t> off; std::vector<uint16_t> len; std::vector<int32_t> pool;
  size_t size() const { return v.size(); }
  void push(double value, ModelView S, uint64_t h);
  void flush_into(Store& s);   // offer every entry, then clear (capacity kept)
  void clear() { v.clear(); hash.clear(); off.clear(); len.clear(); pool.clear(); }
};

class ThreadLedger : public Tally {
 public:
  ThreadLedger(Ledger& island, size_t buf_cap = 65536);
  // Same semantics as Ledger::event; offers go to bounded buffers after the cut-off test (value < cutoff -> dropped).
  void event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev, bool fresh);
  size_t buffered() const { return buf_[0].size() + buf_[1].size() + buf_[2].size(); }
  uint64_t dropped_by_cutoff = 0, flushes = 0;   // diagnostics (not part of any output)

 private:
  Ledger* isl_; size_t cap_;
  OfferBuffer buf_[3];   // top, lead0, lead1
  void offer(int which, Store& s, double value, ModelView S, uint64_t h);
  void flush_all_locked();
  friend class Ledger;
};

}  // namespace v4
