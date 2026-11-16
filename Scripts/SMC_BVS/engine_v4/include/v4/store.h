// store.h -- top-c store of distinct models under a strict total order, flat arrays + integer pool (INTERFACES §4.1).
// Content after compact() = the top-c of everything ever offered, independent of offer order (core/cpp/v3_ledger.h:35-66
// semantics: TopCmp order, distinct models, capacity c; but no std::set and no per-model heap allocation).
#pragma once
#include <cstdint>
#include <vector>
#include "v4/model.h"

namespace v4 {

enum class Order : uint8_t { HPM = 0, LEX = 1 };   // HPM: v desc, |S| asc, lex asc. LEX: v desc, lex asc.

class Store {
 public:
  uint64_t cap = 0; Order ord = Order::HPM;
  std::vector<double> v; std::vector<uint64_t> off, hash; std::vector<uint16_t> len; std::vector<int32_t> pool;

  Store() = default;
  Store(uint64_t c, Order o) { init(c, o); }
  void init(uint64_t c, Order o);
  void offer(double value, ModelView S, uint64_t h);    // may trigger compact(); quick reject when provably out
  void compact();                                       // sort, dedupe, truncate to cap; pool rebuilt in sorted order
  void merge(const Store& o);                           // offer every entry of o, then compact()
  bool would_enter(double value, ModelView S) const;    // valid after compact()
  size_t size() const { return v.size(); }              // valid as "number kept" after compact()
  ModelView model(size_t i) const { return ModelView(pool.data() + off[i], len[i]); }
  bool better(double v1, ModelView S1, double v2, ModelView S2) const;   // strict order of this store
  bool check_invariants() const;                         // I1 (after compact): sorted strictly, no duplicates, size <= cap
  uint64_t content_hash() const;                          // order-sensitive digest of (v bits, S) for tests

 private:
  bool compacted_ = true;   // v[] is sorted/deduped/truncated
  bool full_ = false;       // compacted and size == cap
  size_t since_compact_ = 0;
};

}  // namespace v4
