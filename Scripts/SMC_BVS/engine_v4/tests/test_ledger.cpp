#include <random>
#include "tk.h"
#include "v4/ledger.h"
using namespace v4;

namespace {
struct Ev { Model S; double F, lg0; EventCtx ctx; };
std::vector<Ev> events(uint32_t seed, int n, int p) {
  std::mt19937_64 g(seed); std::vector<Ev> out;
  for (int i = 0; i < n; ++i) {
    Model S; int k = (int)(g() % 4);
    while ((int)S.size() < k) { int j = (int)(g() % p); if (!std::binary_search(S.begin(), S.end(), j)) sorted_insert(S, j); }
    uint64_t h = 77; for (int j : S) { h ^= (uint64_t)(j + 1) * 0x9E3779B97F4A7C15ULL; h = splitmix64(h); }
    Ev e; e.S = S; e.F = (double)(h % 13); e.lg0 = (double)(h % 7);
    e.ctx.phase = PH_FINAL_BRIDGE; e.ctx.mech = ME_GIBBS_FLIP;
    e.ctx.key.seg = SG_FINAL; e.ctx.key.unit = 1 + (uint32_t)(i % 4); e.ctx.key.xph = 2; e.ctx.key.stage = (uint32_t)(i / 100);
    e.ctx.key.particle = (uint32_t)(i % 100); e.ctx.key.position = (uint32_t)i;
    out.push_back(e);
  }
  return out;
}
bool same_ledger(const Ledger& a, const Ledger& b) {
  if (a.has_hpm != b.has_hpm || a.hpmS != b.hpmS || !same_bits(a.hpmF, b.hpmF) || !(a.hpm_ev.key == b.hpm_ev.key)) return false;
  if (a.top.content_hash() != b.top.content_hash() || a.lead0.content_hash() != b.lead0.content_hash() || a.lead1.content_hash() != b.lead1.content_hash()) return false;
  for (int x = 0; x < N_PHASE; ++x) for (int y = 0; y < N_MECH; ++y) if (a.logical[x][y] != b.logical[x][y]) return false;
  return a.island_best == b.island_best;
}
}  // namespace

TEST(ledger_merge_order_free_equals_serial) {
  const int p = 30; auto ev = events(5, 4000, p);
  Zobrist z; z.init(p);
  LedgerConfig cfg; cfg.p = p; cfg.islands = 4;
  Ledger serial(cfg);
  for (auto& e : ev) serial.event(e.S, z.hash(e.S), e.F, e.lg0, e.F, e.ctx, true);
  serial.compact();
  for (int nthreads : {2, 3, 7}) {
    std::vector<Ledger> part(nthreads, Ledger(cfg));
    // out-of-order arrival: reversed within each thread
    for (int i = (int)ev.size() - 1; i >= 0; --i) { auto& e = ev[i]; part[(size_t)(i * 31 % nthreads)].event(e.S, z.hash(e.S), e.F, e.lg0, e.F, e.ctx, true); }
    Ledger m1(cfg); for (auto& q : part) m1.merge(q);
    Ledger m2(cfg); for (int t = nthreads - 1; t >= 0; --t) m2.merge(part[(size_t)t]);
    m1.compact(); m2.compact();
    CHECK(same_ledger(serial, m1)); CHECK(same_ledger(serial, m2));
  }
  // the HPM provenance is the smallest event key among the HPM model's events
  EventKey first; bool found = false;
  for (auto& e : ev) if (e.S == serial.hpmS && (!found || e.ctx.key < first)) { first = e.ctx.key; found = true; }
  CHECK(found && first == serial.hpm_ev.key);
}
TEST(ledger_island_best_and_counters) {
  LedgerConfig cfg; cfg.p = 5; cfg.islands = 2; cfg.leaders = false;
  Ledger L(cfg); Zobrist z; z.init(5);
  EventCtx c; c.phase = PH_LOCAL; c.mech = ME_LOCAL; c.key.unit = UNIT_LOCAL;
  Model S{1}; L.event(S, z.hash(S), 3.0, 0, 3.0, c, true);
  CHECK(L.island_best[0] == Ledger::NEG_INF_L() && L.island_best[1] == Ledger::NEG_INF_L());   // local events are not island events
  c.phase = PH_MEASURED; c.mech = ME_GIBBS_HELD; c.key.unit = 2; L.event(S, z.hash(S), 3.0, 0, 3.0, c, false);
  CHECK(L.island_best[2] == 3.0); CHECK(L.logical[PH_MEASURED][ME_GIBBS_HELD] == 1); CHECK(L.fresh[PH_MEASURED][ME_GIBBS_HELD] == 0);
  CHECK(L.lead0.cap == 0 && L.top.cap == 201);
}
