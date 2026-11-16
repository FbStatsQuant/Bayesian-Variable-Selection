// store.h -- the island's concurrent top store and per-thread ledgers (INTERFACES §4; ENGINEERING_SPEC §1, §3).
//
// TopStore: top-c of every (model, value) offered, under Order HPM (v desc, |S| asc, lex asc) or LEX (v desc, lex asc)
// (core/cpp/v3_ledger.h:35-42). The content is a function of the SET of offers only:
//   * a model offered with several values keeps its largest value (Bit: all values of a model are equal; Class A:
//     a model reached by different paths can carry values that differ in the last bits);
//   * threads append offers to private buffers; a full buffer is merged under the store mutex;
//   * an offer with v < tau is dropped, where tau = the value of the c-th entry once the store holds c distinct
//     models (−inf before). tau only increases, and every model the final store keeps has a value >= any tau seen,
//     so the drop never changes the final content (proof in src/island/README.md). Equal values are never dropped.
// So the result is independent of thread count, schedule, group size, tile size and pass structure (T3).
//
// ThreadLedger: logical counters, island_best, the HPM candidate with its event key, move statistics. merge() is
// order-free: counters by sum, island_best by max, HPM by (F desc, |S| asc, lex asc, event key asc); for one model
// the smallest key wins provenance (= core's "first score" rule, core/cpp/v3_ledger.h:84-88).
#pragma once
#include <atomic>
#include <mutex>
#include <tuple>
#include "v4/island/dep.h"

namespace v4::island {
using namespace v4::island::dep;

using v4::Phase; using v4::Mech; using v4::Segment; using v4::Order; using v4::EventKey; using v4::MoveStats;
using v4::PH_FINAL_INIT; using v4::PH_FINAL_BRIDGE; using v4::PH_BURN_IN; using v4::PH_MEASURED; using v4::N_PHASE; using v4::N_MECH;
using v4::ME_INIT; using v4::ME_GIBBS_HELD; using v4::ME_GIBBS_FLIP; using v4::ME_USWAP; using v4::ME_NSWAP; using v4::ME_INDEP; using v4::SG_FINAL;
inline void add_moves(MoveStats& a, const MoveStats& o) {
  a.gibbs += o.gibbs; a.gibbs_change += o.gibbs_change; a.us_exec += o.us_exec; a.us_acc += o.us_acc; a.us_self += o.us_self;
  a.ns_exec += o.ns_exec; a.ns_acc += o.ns_acc; a.ns_noscore += o.ns_noscore; a.ns_self += o.ns_self; a.in_exec += o.in_exec; a.in_acc += o.in_acc; a.gibbs_cap += o.gibbs_cap;
}

// ---------------------------------------------------------------------------------------------------------------
struct StoreBuffer {
  std::vector<double> v; std::vector<uint64_t> h, off; std::vector<uint16_t> len; std::vector<int32_t> pool;
  size_t size() const { return v.size(); }
  void clear() { v.clear(); h.clear(); off.clear(); len.clear(); pool.clear(); }
  void push(double val, const int32_t* S, uint32_t k, uint64_t hash) {
    v.push_back(val); h.push_back(hash); off.push_back(pool.size()); len.push_back((uint16_t)k); pool.insert(pool.end(), S, S + k);
  }
};

// One top store per island (INTERFACES v0.1.2 design: bounded per-thread buffers, one island store, a shared
// monotone cut-off). Memory: per thread O(buf_limit) (default 65,536 entries); per island O(cap) for the store, its
// hash index and a staging area of at most stage_limit entries (default max(cap/4, 4096)).
//   offer():   v < tau -> dropped (tau = worst kept value once the store is full, -inf before; atomic, monotone);
//              else appended to the thread's buffer; a full buffer is flushed.
//   flush():   appends a buffer to the island staging area under the mutex; a full staging area is compacted.
//   compact(): staged entries sorted and de-duplicated by model (largest value kept), matched against the store by a
//              hash index (a store copy with a smaller value is replaced), sorted under ord and merged linearly with
//              the store, truncated to cap; pool, index and tau rebuilt. O(cap + s log s).
// The content after compact() is the top-c of the set of offers (largest value per model), whatever the thread
// count, flush timing or merge order (proof: src/island/README.md, "Store").
class TopStore {
 public:
  uint64_t cap = 0; Order ord = Order::HPM;
  // compacted content, strictly sorted under ord, no duplicates (I1)
  std::vector<double> v; std::vector<uint64_t> hash, off; std::vector<uint16_t> len; std::vector<int32_t> pool;
  std::atomic<double> tau{NEG_INF};
  std::mutex mu;
  uint64_t n_merges = 0, n_buffered = 0, n_flushes = 0;
  size_t buf_limit = 1 << 14, stage_limit = 1 << 16;
  StoreBuffer stage;                         // island staging area (guarded by mu)
  std::vector<uint32_t> index; uint64_t imask = 0;   // open-addressing hash index over the compacted entries (idx + 1)

  void init(uint64_t c, Order o) {
    cap = c; ord = o; v.clear(); hash.clear(); off.clear(); len.clear(); pool.clear(); tau.store(NEG_INF);
    stage.clear(); index.clear(); imask = 0;
    n_merges = n_buffered = n_flushes = 0;
    buf_limit = 65536;                                             // INTERFACES v0.1.2 §4.2 OfferBuffer default
    stage_limit = (size_t)std::max<uint64_t>(4096, c / 4);          // §4.1: staging compacted at max(cap/4, 4096)
  }
  size_t size() const { return v.size(); }
  double cutoff() const { return tau.load(std::memory_order_acquire); }   // INTERFACES §4.1: monotone, atomic
  // hot path, any thread, its own buffer
  inline void offer(StoreBuffer& b, double val, const int32_t* S, uint32_t k, uint64_t hsh) {
    if (cap == 0 || val < tau.load(std::memory_order_relaxed)) return;
    b.push(val, S, k, hsh);
    if (b.size() >= buf_limit) flush(b);
  }
  void flush(StoreBuffer& b) {
    if (b.size() == 0) return;
    std::lock_guard<std::mutex> lk(mu);
    const uint64_t base = stage.pool.size();
    for (size_t i = 0; i < b.size(); ++i) { stage.v.push_back(b.v[i]); stage.h.push_back(b.h[i]); stage.off.push_back(base + b.off[i]); stage.len.push_back(b.len[i]); }
    stage.pool.insert(stage.pool.end(), b.pool.begin(), b.pool.end());
    n_buffered += b.size(); ++n_flushes;
    b.clear();
    if (stage.size() >= stage_limit) compact_locked();
  }
  void merge_buffer(StoreBuffer& b) { flush(b); }     // (name kept for callers)
  void compact() { std::lock_guard<std::mutex> lk(mu); compact_locked(); }

  struct Ref { double v; uint64_t h; const int32_t* S; uint16_t k; };
  bool ord_less(const Ref& a, const Ref& b) const {   // strict order of the store
    if (a.v != b.v) return a.v > b.v;
    if (ord == Order::HPM && a.k != b.k) return a.k < b.k;
    return lex_less(a.S, a.k, b.S, b.k);
  }
  static bool same_model(const Ref& a, const Ref& b) { return a.h == b.h && a.k == b.k && std::equal(a.S, a.S + a.k, b.S); }
  Ref ref(size_t i) const { return Ref{v[i], hash[i], pool.data() + off[i], len[i]}; }
  int64_t find(const Ref& e) const {
    if (index.empty()) return -1;
    for (uint64_t s = e.h & imask;; s = (s + 1) & imask) {
      uint32_t x = index[s]; if (!x) return -1;
      if (same_model(ref(x - 1), e)) return (int64_t)x - 1;
    }
  }
  void rebuild_index() {
    uint64_t n = 16; while (n < 2 * v.size() + 2) n <<= 1;
    index.assign(n, 0); imask = n - 1;
    for (size_t i = 0; i < v.size(); ++i) { uint64_t s = hash[i] & imask; while (index[s]) s = (s + 1) & imask; index[s] = (uint32_t)i + 1; }
  }
  void compact_locked() {
    if (stage.size() == 0) return;
    ++n_merges;
    std::vector<Ref> r; r.reserve(stage.size());
    for (size_t i = 0; i < stage.size(); ++i) r.push_back({stage.v[i], stage.h[i], stage.pool.data() + stage.off[i], stage.len[i]});
    std::sort(r.begin(), r.end(), [](const Ref& a, const Ref& b) {   // by model, then value desc
      if (a.h != b.h) return a.h < b.h;
      if (a.k != b.k) return a.k < b.k;
      int c = std::memcmp(a.S, b.S, sizeof(int32_t) * a.k);
      if (c != 0) return lex_less(a.S, a.k, b.S, b.k);
      return a.v > b.v;
    });
    size_t w = 0;
    std::vector<uint8_t> dead(v.size(), 0);
    for (size_t i = 0; i < r.size(); ++i) {
      if (w > 0 && same_model(r[w - 1], r[i])) continue;           // same model staged twice: keep the largest
      int64_t at = find(r[i]);
      if (at >= 0) { if (v[at] >= r[i].v) continue; dead[at] = 1; } // store copy at least as large: drop the staged one
      r[w++] = r[i];
    }
    r.resize(w);
    std::sort(r.begin(), r.end(), [this](const Ref& a, const Ref& b) { return ord_less(a, b); });
    std::vector<double> nv; std::vector<uint64_t> nh, no; std::vector<uint16_t> nl; std::vector<int32_t> np;
    size_t keep = std::min<size_t>(cap, v.size() + r.size());
    nv.reserve(keep); nh.reserve(keep); no.reserve(keep); nl.reserve(keep); np.reserve(pool.size() + stage.pool.size());
    size_t i = 0, j = 0;
    auto put = [&](const Ref& e) { nv.push_back(e.v); nh.push_back(e.h); nl.push_back(e.k); no.push_back(np.size()); np.insert(np.end(), e.S, e.S + e.k); };
    while (nv.size() < cap) {
      while (i < v.size() && dead[i]) ++i;
      bool hs = i < v.size(), hr = j < r.size();
      if (!hs && !hr) break;
      if (hs && (!hr || ord_less(ref(i), r[j]))) { put(ref(i)); ++i; } else { put(r[j]); ++j; }
    }
    v.swap(nv); hash.swap(nh); off.swap(no); len.swap(nl); pool.swap(np);
    stage.clear();
    rebuild_index();
    tau.store(v.size() >= cap ? v.back() : NEG_INF);
  }
  // I1 check: strictly sorted, no duplicates, size <= cap (valid after compact())
  bool check_invariant() const {
    if (v.size() > cap) return false;
    for (size_t i = 1; i < v.size(); ++i) if (!ord_less(ref(i - 1), ref(i))) return false;
    std::vector<std::pair<uint64_t, size_t>> hs; for (size_t i = 0; i < v.size(); ++i) hs.push_back({hash[i], i});
    std::sort(hs.begin(), hs.end());
    for (size_t i = 1; i < hs.size(); ++i)
      if (hs[i].first == hs[i - 1].first && same_model(ref(hs[i].second), ref(hs[i - 1].second))) return false;
    return true;
  }
  Model model(size_t i) const { return Model(pool.data() + off[i], pool.data() + off[i] + len[i]); }
  size_t bytes() const { return v.capacity() * 8 + hash.capacity() * 8 + off.capacity() * 8 + len.capacity() * 2 + pool.capacity() * 4 + index.capacity() * 4; }
};

// ---------------------------------------------------------------------------------------------------------------
struct HpmRec {
  bool has = false; Model S; double F = NEG_INF, logm = 0; EventKey key; int phase = 0, mech = 0;
};
// strict order of HPM candidates (event level): F desc, |S| asc, lex asc, key asc
inline bool hpm_cand_better(double F, const int32_t* S, size_t k, const EventKey& key, const HpmRec& r) {
  if (!r.has) return true;
  if (F != r.F) return F > r.F;
  if (k != r.S.size()) return k < r.S.size();
  if (!std::equal(S, S + k, r.S.begin())) return lex_less(S, k, r.S.data(), r.S.size());
  return key < r.key;
}

struct ThreadLedger {
  uint64_t logical[N_PHASE][N_MECH] = {};
  double island_best = NEG_INF;
  HpmRec hpm;
  MoveStats ms;
  StoreBuffer buf;
  TopStore* top = nullptr;
  // One logical score event that is offered (a scored model): counters, island_best, HPM, store.
  inline void scored(const int32_t* S, uint32_t k, uint64_t h, double F, double logm, int phase, int mech, const EventKey& key) {
    logical[phase][mech]++;
    if (F > island_best) island_best = F;
    if (F >= hpm.F && hpm_cand_better(F, S, k, key, hpm)) {
      hpm.has = true; hpm.S.assign(S, S + k); hpm.F = F; hpm.logm = logm; hpm.key = key; hpm.phase = phase; hpm.mech = mech;
    }
    top->offer(buf, F, S, k, h);
  }
  void merge_from(const ThreadLedger& o) {
    for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) logical[a][b] += o.logical[a][b];
    if (o.island_best > island_best) island_best = o.island_best;
    if (o.hpm.has && hpm_cand_better(o.hpm.F, o.hpm.S.data(), o.hpm.S.size(), o.hpm.key, hpm)) hpm = o.hpm;
    add_moves(ms, o.ms);
  }
  void reset_counters() { std::memset(logical, 0, sizeof(logical)); island_best = NEG_INF; hpm = HpmRec(); ms = MoveStats(); }
};

}  // namespace v4::island
