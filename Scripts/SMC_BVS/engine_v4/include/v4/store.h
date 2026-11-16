// store.h -- top-c store of distinct models under a strict total order, flat arrays + integer pool (INTERFACES §4.1).
// Content after compact() = the top-c of everything ever offered, independent of offer order (core/cpp/v3_ledger.h:35-66
// semantics: TopCmp order, distinct models, capacity c; but no std::set and no per-model heap allocation).
// A model may be offered with different values (class A: path-dependent maxima, INTERFACES §4.1): the store holds each
// model ONCE, with the best value it was offered with ("top-c of distinct models by their best value"); still
// independent of offer order.
// Layout: [0, nkept) the kept run (sorted, unique); [nkept, size) the staging run (unsorted offers). compact() sorts the
// staging run and merges it into the kept run (peak about 2.5 c entries with the max(c/4, 4096) staging trigger; an entry
// costs 30 + 4k bytes kept (26 + 4k data, 4 index), plus about 9 B per entry transient during compact()).
// cutoff(): -inf until c entries are kept, then the worst kept value; monotone non-decreasing; atomic (other threads
// may read it while this store is being filled under its owner's lock).
#pragma once
#include <atomic>
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
  Store(const Store& o) { *this = o; }
  Store& operator=(const Store& o);
  void init(uint64_t c, Order o);
  void offer(double value, ModelView S, uint64_t h);    // quick reject if provably out; may trigger compact()
  void compact();                                       // staging sorted + merged into the kept run; truncate to cap
  void merge(const Store& o);                           // offer every entry of o, then compact()
  // Bulk load of an already valid store into this EMPTY store, without compactions: O(n) verification (strict order,
  // models sorted, pool ranges, n <= cap) plus one (hash, index) pair sort for the model index, which also verifies one
  // entry per model, ASSUMING the given hashes are the models' hashes (callers that read untrusted files check them
  // against the Zobrist keys: WP4 read_store / load_island_full, WP3 read_island_file). Preconditions: this store is
  // empty (else Error(internal_error)); n > cap is refused, not truncated. Content = what offering every entry and
  // compacting gives, for valid input. Throws Error(invalid_input) when the input is not a valid store (e.g. a corrupt
  // file) and leaves this store empty. For island records, island files and stored sections.
  void load_unique_sorted(size_t n, const double* v, const uint64_t* hash, const uint64_t* off, const uint16_t* len,
                          const int32_t* pool, size_t pool_n);
  double cutoff() const { return cut_.load(std::memory_order_relaxed); }
  bool would_enter(double value, ModelView S) const;    // valid after compact()
  size_t size() const { return v.size(); }              // = number kept after compact()
  size_t staging() const { return v.size() - nkept_; }
  ModelView model(size_t i) const { return ModelView(pool.data() + off[i], len[i]); }
  bool better(double v1, ModelView S1, double v2, ModelView S2) const;   // strict order of this store
  // I1 (after compact): strictly sorted, size <= cap, cut-off = worst value when full, ONE ENTRY PER MODEL (checked by
  // a fresh (hash, model) sort, independent of the index but assuming correct stored hashes), and the index is a valid
  // permutation in key order.
  bool check_invariants() const;
  uint64_t content_hash() const;                        // order-sensitive digest of (v bits, S), for tests
  size_t bytes_reserved() const;                        // capacity of all arrays, in bytes (memory accounting)

 private:
  size_t nkept_ = 0;                                    // kept run = [0, nkept_)
  std::vector<uint32_t> hidx_;                          // kept run indices sorted by (hash, model): duplicate lookup
  bool key_less(uint32_t a, uint32_t b) const;          // (hash, then lexicographic model)
  std::atomic<double> cut_{-__builtin_huge_val()};
  uint64_t trigger() const { return cap / 4 > 4096 ? cap / 4 : 4096; }
};

}  // namespace v4
