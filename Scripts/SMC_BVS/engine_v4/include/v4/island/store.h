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
#include <limits>
#include <memory>
#include <omp.h>
#include <parallel/algorithm>
#include <chrono>
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
struct StoreRef { double v; uint64_t h; const int32_t* S; uint16_t k; };
inline bool same_model_ref(const StoreRef& a, const StoreRef& b) { return a.h == b.h && a.k == b.k && std::equal(a.S, a.S + a.k, b.S); }

// The kept run of an island store: immutable once published (workers read it without the lock).
struct Kept {
  std::vector<double> v; std::vector<uint64_t> hash, off; std::vector<uint16_t> len; std::vector<int32_t> pool;
  std::vector<uint32_t> index; uint64_t imask = 0;   // open addressing over the entries (slot value = entry + 1)
  size_t size() const { return v.size(); }
  StoreRef ref(size_t i) const { return StoreRef{v[i], hash[i], pool.data() + off[i], len[i]}; }
  int64_t find(const StoreRef& e) const {
    if (index.empty()) return -1;
    for (uint64_t s = e.h & imask;; s = (s + 1) & imask) {
      uint32_t x = index[s]; if (!x) return -1;
      if (same_model_ref(ref(x - 1), e)) return (int64_t)x - 1;
    }
  }
  void rebuild_index() {
    uint64_t n = 16; while (n < 2 * v.size() + 2) n <<= 1;
    index.assign(n, 0); imask = n - 1;
    for (size_t i = 0; i < v.size(); ++i) { uint64_t s = hash[i] & imask; while (index[s]) s = (s + 1) & imask; index[s] = (uint32_t)i + 1; }
  }
  size_t bytes() const { return v.capacity() * 8 + hash.capacity() * 8 + off.capacity() * 8 + len.capacity() * 2 + pool.capacity() * 4 + index.capacity() * 4; }
};

struct StoreBuffer {
  std::vector<double> v; std::vector<uint64_t> h, off; std::vector<uint16_t> len; std::vector<int32_t> pool;
  std::shared_ptr<const Kept> snap; uint64_t snap_gen = ~0ull;   // the worker's snapshot of the kept run
  uint64_t n_dup_dropped = 0;
  size_t size() const { return v.size(); }
  void clear() { v.clear(); h.clear(); off.clear(); len.clear(); pool.clear(); }
  void push(double val, const int32_t* S, uint32_t k, uint64_t hash) {
    v.push_back(val); h.push_back(hash); off.push_back(pool.size()); len.push_back((uint16_t)k); pool.insert(pool.end(), S, S + k);
  }
};

// One top store per island (INTERFACES v0.1.2 design: bounded per-thread buffers, one island store, a shared
// monotone cut-off). Memory: per thread O(buf_limit) (default 65,536 entries); per island O(cap) for the kept run, its
// hash index and a staging area of at most stage_limit entries (default max(cap/4, 4096)).
//   offer():   v < tau -> dropped (tau = worst kept value once the store is full, -inf before; atomic, monotone);
//              model already kept with a value >= v in the worker's snapshot -> dropped (exact duplicate filter);
//              else appended to the worker's buffer; a full buffer is flushed.
//   flush():   appends a buffer to the island staging area under the mutex; a full staging area is compacted.
//   compact(): staged entries sorted and de-duplicated by model (largest value kept), matched against the kept run by
//              its hash index (a kept copy with a smaller value is replaced), sorted under ord and merged linearly with
//              the kept run, truncated to cap, into a NEW kept run (index built) that is then published; O(cap + s log s).
// The content after compact() is the top-c of the set of offers (largest value per model), whatever the thread
// count, flush timing, snapshot staleness or merge order (proof: WP3_DESIGN.md §1.3; the duplicate filter only drops
// an offer whose model was already offered with a value at least as large).
class TopStore {
 public:
  uint64_t cap = 0; Order ord = Order::HPM;
  std::shared_ptr<Kept> k = std::make_shared<Kept>();   // current kept run (replaced, never modified, once published)
  std::atomic<double> tau{NEG_INF};
  std::atomic<uint64_t> gen{0};
  std::mutex mu, snap_mu;
  uint64_t n_merges = 0, n_buffered = 0, n_flushes = 0, n_serial_merges = 0;
  size_t buf_limit = 1 << 14, stage_limit = 1 << 16, stage_hard = 1 << 17;
  bool defer = false;          // true: flush() never compacts below stage_hard; the owner calls compact_parallel()
  double t_compact = 0;        // wall seconds spent compacting (any path)
  bool dup_filter = true;
  StoreBuffer stage;                                     // island staging area (guarded by mu)

  void init(uint64_t c, Order o) {
    cap = c; ord = o; k = std::make_shared<Kept>(); tau.store(NEG_INF); gen.store(0);
    stage.clear();
    n_merges = n_buffered = n_flushes = n_serial_merges = 0; t_compact = 0;
    buf_limit = 65536;                                             // INTERFACES v0.1.2 §4.2 OfferBuffer default
    stage_limit = (size_t)std::max<uint64_t>(4096, c / 4);          // §4.1: staging compacted at max(cap/4, 4096)
    stage_hard = (size_t)std::max<uint64_t>(8192, c / 2);           // deferred mode: in-pass serial fallback (peak ~2.5c)
  }
  size_t size() const { return k->size(); }
  double cutoff() const { return tau.load(std::memory_order_acquire); }   // INTERFACES §4.1: monotone, atomic
  std::shared_ptr<const Kept> snapshot() { std::lock_guard<std::mutex> lk(snap_mu); return k; }
  void refresh(StoreBuffer& b) {
    uint64_t g = gen.load(std::memory_order_acquire);
    if (b.snap_gen != g) { b.snap = snapshot(); b.snap_gen = g; }
  }
  // hot path, any thread, its own buffer
  inline void offer(StoreBuffer& b, double val, const int32_t* S, uint32_t kk, uint64_t hsh) {
    if (cap == 0 || val < tau.load(std::memory_order_relaxed)) return;
    if (dup_filter) {
      refresh(b);
      int64_t at = b.snap->find(StoreRef{val, hsh, S, (uint16_t)kk});
      if (at >= 0 && b.snap->v[at] >= val) { ++b.n_dup_dropped; return; }
    }
    b.push(val, S, kk, hsh);
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
    if (stage.size() >= (defer ? stage_hard : stage_limit)) { ++n_serial_merges; compact_locked(); }
  }
  size_t staged() { std::lock_guard<std::mutex> lk(mu); return stage.size(); }
  void merge_buffer(StoreBuffer& b) { flush(b); }
  void compact() { std::lock_guard<std::mutex> lk(mu); compact_locked(); }

  bool ord_less(const StoreRef& a, const StoreRef& b) const {   // strict order of the store
    if (a.v != b.v) return a.v > b.v;
    if (ord == Order::HPM && a.k != b.k) return a.k < b.k;
    return lex_less(a.S, a.k, b.S, b.k);
  }
  void compact_locked() {
    if (stage.size() == 0) return;
    ++n_merges;
    auto t0 = std::chrono::steady_clock::now();
    struct Tm { std::chrono::steady_clock::time_point t0; double& acc; ~Tm() { acc += std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count(); } } tm{t0, t_compact};
    const Kept& K = *k;
    std::vector<StoreRef> r; r.reserve(stage.size());
    for (size_t i = 0; i < stage.size(); ++i) r.push_back({stage.v[i], stage.h[i], stage.pool.data() + stage.off[i], stage.len[i]});
    std::sort(r.begin(), r.end(), [](const StoreRef& a, const StoreRef& b) {   // by model, then value desc
      if (a.h != b.h) return a.h < b.h;
      if (a.k != b.k) return a.k < b.k;
      int c = std::memcmp(a.S, b.S, sizeof(int32_t) * a.k);
      if (c != 0) return lex_less(a.S, a.k, b.S, b.k);
      return a.v > b.v;
    });
    size_t w = 0;
    std::vector<uint8_t> dead(K.size(), 0);
    for (size_t i = 0; i < r.size(); ++i) {
      if (w > 0 && same_model_ref(r[w - 1], r[i])) continue;       // same model staged twice: keep the largest
      int64_t at = K.find(r[i]);
      if (at >= 0) { if (K.v[at] >= r[i].v) continue; dead[at] = 1; } // kept copy at least as large: drop the staged one
      r[w++] = r[i];
    }
    r.resize(w);
    std::sort(r.begin(), r.end(), [this](const StoreRef& a, const StoreRef& b) { return ord_less(a, b); });
    auto nk = std::make_shared<Kept>();
    size_t keep = std::min<size_t>(cap, K.size() + r.size());
    nk->v.reserve(keep); nk->hash.reserve(keep); nk->off.reserve(keep); nk->len.reserve(keep); nk->pool.reserve(K.pool.size() + stage.pool.size());
    size_t i = 0, j = 0;
    auto put = [&](const StoreRef& e) { nk->v.push_back(e.v); nk->hash.push_back(e.h); nk->len.push_back(e.k); nk->off.push_back(nk->pool.size()); nk->pool.insert(nk->pool.end(), e.S, e.S + e.k); };
    while (nk->v.size() < cap) {
      while (i < K.size() && dead[i]) ++i;
      bool hs = i < K.size(), hr = j < r.size();
      if (!hs && !hr) break;
      if (hs && (!hr || ord_less(K.ref(i), r[j]))) { put(K.ref(i)); ++i; } else { put(r[j]); ++j; }
    }
    nk->rebuild_index();
    stage.clear();
    { std::lock_guard<std::mutex> lk(snap_mu); k = nk; }
    gen.fetch_add(1, std::memory_order_acq_rel);
    tau.store(k->size() >= cap ? k->v.back() : NEG_INF);
  }
  // Parallel compaction (pass boundaries and step boundaries; all `threads` workers are free). Same content as
  // compact_locked() -- a function of the set of offers -- for every thread count and flush order:
  //   1. staged refs sorted by (hash, |S|, S, v desc) with __gnu_parallel::sort (the order is total on content, so the
  //      sorted sequence is unique); 2. first entry per model kept (sequential scan); 3. each survivor matched against
  //      the kept index in parallel (a kept copy >= drops it, a smaller kept copy is marked dead); 4. survivors sorted
  //      under the store order (parallel); 5. merge-path parallel merge of the alive kept run and the survivors, both
  //      strictly ordered with distinct models, truncated at cap; pool offsets by a prefix sum; parallel copy;
  //   6. hash index built in parallel by CAS insertion (slot layout may differ, lookups do not).
  void compact_parallel(int threads) {
    std::lock_guard<std::mutex> lk(mu);
    if (stage.size() == 0) return;
    if (threads <= 1) { compact_locked(); return; }
    ++n_merges;
    auto t0 = std::chrono::steady_clock::now();
    const Kept& K = *k;
    const size_t s = stage.size();
    std::vector<StoreRef> r(s);
    #pragma omp parallel for num_threads(threads) schedule(static)
    for (size_t i = 0; i < s; ++i) r[i] = StoreRef{stage.v[i], stage.h[i], stage.pool.data() + stage.off[i], stage.len[i]};
    auto by_model = [](const StoreRef& a, const StoreRef& b) {
      if (a.h != b.h) return a.h < b.h;
      if (a.k != b.k) return a.k < b.k;
      int c = std::memcmp(a.S, b.S, sizeof(int32_t) * a.k);
      if (c != 0) return lex_less(a.S, a.k, b.S, b.k);
      return a.v > b.v;
    };
    __gnu_parallel::sort(r.begin(), r.end(), by_model, __gnu_parallel::default_parallel_tag(threads));
    size_t w = 0;
    for (size_t i = 0; i < s; ++i) if (w == 0 || !same_model_ref(r[w - 1], r[i])) r[w++] = r[i];
    r.resize(w);
    std::vector<uint8_t> dead(K.size(), 0), drop(w, 0);
    #pragma omp parallel for num_threads(threads) schedule(static)
    for (size_t i = 0; i < w; ++i) {
      int64_t at = K.find(r[i]);
      if (at >= 0) { if (K.v[at] >= r[i].v) drop[i] = 1; else dead[at] = 1; }   // distinct staged models: distinct `at`
    }
    size_t w2 = 0; for (size_t i = 0; i < w; ++i) if (!drop[i]) r[w2++] = r[i];
    r.resize(w2);
    auto ordl = [this](const StoreRef& a, const StoreRef& b) { return ord_less(a, b); };
    __gnu_parallel::sort(r.begin(), r.end(), ordl, __gnu_parallel::default_parallel_tag(threads));
    std::vector<uint32_t> alive; alive.reserve(K.size());
    for (size_t i = 0; i < K.size(); ++i) if (!dead[i]) alive.push_back((uint32_t)i);
    const size_t na = alive.size(), nb = r.size(), keep = std::min<size_t>(cap, na + nb);
    auto A = [&](size_t i) { return K.ref(alive[i]); };
    // merge path: for output diagonal d, the number i of A-entries among the first d outputs
    auto split = [&](size_t d) {
      size_t lo = d > nb ? d - nb : 0, hi = std::min(d, na);
      while (lo < hi) { size_t i = (lo + hi) / 2; if (ord_less(A(i), r[d - i - 1])) lo = i + 1; else hi = i; }
      return lo;
    };
    const int T = threads;
    std::vector<size_t> dpos(T + 1), ipos(T + 1);
    for (int t = 0; t <= T; ++t) { dpos[t] = keep * (size_t)t / (size_t)T; ipos[t] = split(dpos[t]); }
    auto nk = std::make_shared<Kept>();
    nk->v.resize(keep); nk->hash.resize(keep); nk->off.resize(keep); nk->len.resize(keep);
    std::vector<uint64_t> segpool(T + 1, 0);
    #pragma omp parallel for num_threads(T) schedule(static, 1)
    for (int t = 0; t < T; ++t) {   // pass 1: values, hashes, lengths of segment t
      size_t i = ipos[t], j = dpos[t] - ipos[t]; uint64_t pl = 0;
      for (size_t d = dpos[t]; d < dpos[t + 1]; ++d) {
        bool fromA = i < na && (j >= nb || ord_less(A(i), r[j]));
        StoreRef e = fromA ? A(i++) : r[j++];
        nk->v[d] = e.v; nk->hash[d] = e.h; nk->len[d] = e.k; pl += e.k;
      }
      segpool[t + 1] = pl;
    }
    for (int u = 0; u < T; ++u) segpool[u + 1] += segpool[u];
    nk->pool.resize(segpool[T]);
    #pragma omp parallel for num_threads(T) schedule(static, 1)
    for (int t = 0; t < T; ++t) {   // pass 2: pool offsets and copies of segment t
      size_t i = ipos[t], j = dpos[t] - ipos[t]; uint64_t o = segpool[t];
      for (size_t d = dpos[t]; d < dpos[t + 1]; ++d) {
        bool fromA = i < na && (j >= nb || ord_less(A(i), r[j]));
        StoreRef e = fromA ? A(i++) : r[j++];
        nk->off[d] = o; std::memcpy(nk->pool.data() + o, e.S, sizeof(int32_t) * e.k); o += e.k;
      }
    }
    // parallel index (CAS insertion)
    uint64_t n = 16; while (n < 2 * keep + 2) n <<= 1;
    nk->index.assign(n, 0); nk->imask = n - 1;
    uint32_t* idx = nk->index.data(); const uint64_t mask = nk->imask;
    #pragma omp parallel for num_threads(threads) schedule(static)
    for (size_t i = 0; i < keep; ++i) {
      uint64_t sl = nk->hash[i] & mask;
      while (true) {
        uint32_t expect = 0;
        if (__atomic_compare_exchange_n(&idx[sl], &expect, (uint32_t)i + 1, false, __ATOMIC_RELAXED, __ATOMIC_RELAXED)) break;
        sl = (sl + 1) & mask;
      }
    }
    stage.clear();
    { std::lock_guard<std::mutex> lk2(snap_mu); k = nk; }
    gen.fetch_add(1, std::memory_order_acq_rel);
    tau.store(k->size() >= cap ? k->v.back() : NEG_INF);
    t_compact += std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  }
  // after loading a kept run (checkpoint): index, tau, generation
  void publish_loaded() { k->rebuild_index(); gen.fetch_add(1); tau.store(k->size() >= cap ? k->v.back() : NEG_INF); }
  // I1 check: strictly sorted, no duplicates, size <= cap (valid after compact())
  bool check_invariant() const {
    const Kept& K = *k;
    if (K.size() > cap) return false;
    for (size_t i = 1; i < K.size(); ++i) if (!ord_less(K.ref(i - 1), K.ref(i))) return false;
    std::vector<std::pair<uint64_t, size_t>> hs; for (size_t i = 0; i < K.size(); ++i) hs.push_back({K.hash[i], i});
    std::sort(hs.begin(), hs.end());
    for (size_t i = 1; i < hs.size(); ++i)
      if (hs[i].first == hs[i - 1].first && same_model_ref(K.ref(hs[i].second), K.ref(hs[i - 1].second))) return false;
    return true;
  }
  Model model(size_t i) const { const Kept& K = *k; return Model(K.pool.data() + K.off[i], K.pool.data() + K.off[i] + K.len[i]); }
  double value(size_t i) const { return k->v[i]; }
  size_t bytes() const { return k->bytes() + stage.v.capacity() * 26 + stage.pool.capacity() * 4; }
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
  // compat mode (v3 serial streams): the two leader stores of core/cpp/v3_ledger.h:72-94 (lead0: log gamma_0, lead1: F)
  TopStore* lead0 = nullptr; TopStore* lead1 = nullptr; StoreBuffer buf0, buf1;
  inline void scored(const int32_t* S, uint32_t k, uint64_t h, double F, double logm, int phase, int mech, const EventKey& key,
                     double lg0 = std::numeric_limits<double>::quiet_NaN()) {
    logical[phase][mech]++;
    if (F > island_best) island_best = F;
    if (F >= hpm.F && hpm_cand_better(F, S, k, key, hpm)) {
      hpm.has = true; hpm.S.assign(S, S + k); hpm.F = F; hpm.logm = logm; hpm.key = key; hpm.phase = phase; hpm.mech = mech;
    }
    top->offer(buf, F, S, k, h);
    if (lead0) { lead0->offer(buf0, lg0, S, k, h); lead1->offer(buf1, F, S, k, h); }
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
