// ledger.h -- score events: HPM + provenance, stores, logical counters, island_best; per-thread instances and an
// order-free merge (INTERFACES §4.2; core/cpp/v3_ledger.h).
#pragma once
#include <cstdint>
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

class Ledger {
 public:
  LedgerConfig cfg;
  bool has_hpm = false; Model hpmS; double hpmF = NEG_INF_L(), hpm_logm = 0; EventCtx hpm_ev;
  Store top, lead0, lead1;   // top-(40p+1) by F (HPM order); top 20p by lg0 (LEX); top 20p by F (LEX)
  uint64_t logical[N_PHASE][N_MECH] = {}, fresh[N_PHASE][N_MECH] = {};
  std::vector<double> island_best;   // r = 0..islands

  Ledger() = default;
  explicit Ledger(const LedgerConfig& c) { init(c); }
  void init(const LedgerConfig& c);
  // One logical score event (core/cpp/v3_ledger.h:104-113). fresh = freshly evaluated: compat counts it and offers to
  // the HPM and stores only then; production passes fresh = true for every consumed score (no cache, OD-3).
  void event(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev, bool fresh);
  void offer_hpm(ModelView S, double F, double logm, const EventCtx& ev);
  void offer_stores(ModelView S, uint64_t h, double F, double lg0, double logm, const EventCtx& ev);
  void merge(const Ledger& o);   // order-free: stores by top-c of the union, HPM by hpm_better then smaller key, max, sum
  void compact() { top.compact(); lead0.compact(); lead1.compact(); }
  static constexpr double NEG_INF_L() { return -__builtin_huge_val(); }
};

}  // namespace v4
