// memory.h -- peak-live memory plan of one island and the --mem-budget admission (manager Q3, Q4; Sol F2; review PR24 P2).
//
// island_memory() is an UPPER BOUND of the island process's memory, given k = the mean size of the stored models (an
// entry costs e = 26 + 4k bytes). Every allocation that grows with p, c, N, G, K or threads is counted:
//   inputs       X (n p 8) + z + diag(G) (16 p), owned by the island process; plus MemSizes::inputs_bytes, which the CLI
//                sets to the mapped setup / calib sections (tables, neighbours). --mem-budget is the TASK's memory: the
//                plan includes the data, and the caller adds the setup inputs through inputs_bytes (INTERFACES §7 note,
//                requested from WP1).
//   x_tiles      label-major: the tiled row-major copy of X                      ntile * tile * n * 8
//   store        kept run (old, while a compaction runs) + new kept run         2 c e + s 4k (pool over-reservation)
//                staging, vector capacity at the next power of two x 1.5         1.5 pow2(s) e        (s = c/2 deferred, c/4 serial)
//                sort refs + the parallel mergesort's temporary copy             s 64,  flags s + c, alive list 4 c
//                hash indexes, old + new                                         2 * 4 pow2(2c + 2)
//                one stale snapshot generation held by a worker mid-tile        c e + 4 pow2(2c + 2)
//   leaders      (calibration islands, option `leaders`) two stores of cap 20p, serial compaction at cap/4, same terms
//   worker_bufs  T offer buffers per store, capacity pow2(65,536) x 1.5          T * 98,304 * e * (1 or 3)
//   rb           u128 accumulators 32 p (+ particle-major 16 p T) (+ compat 8 p) + rb_round Hm p 8 + rb_acc, pip 16 p
//   orders       label-major group: orders + inverse orders + U/N/I lists        2 G m 4 + G (B + 2) 8
//   rows         label-major group: log m and odds rows per support              2 G p 8
//   supports     support caches (4 k_q^2 doubles each), gathered columns, per-thread product tiles
//                with k_q = min(K, 3k): G (32 k_q^2) + G k_q n 8 + T G k_q tile 8
//   particles    two populations + pending + terminal supports                   (2N + G) (4k + 64) + N 4k
//   ckpt         streamed checkpoint buffers                                     2 MiB
// The plan depends on the thread count (worker buffers, product tiles, staging limit): a refusal is reproducible for the
// same thread count (review m2). G does not change outputs.
#pragma once
#include <algorithm>
#include <cstdint>
#include <string>
#include <vector>

namespace v4::island {

struct MemItem { std::string name; uint64_t bytes; };
struct MemPlan { std::vector<MemItem> items; uint64_t total = 0; int G = 0; double k = 0; };
struct MemSizes {
  int n = 0, p = 0, K = 0, N = 0, B = 0, Hm = 4, threads = 1, G = 1, tile = 128;
  uint64_t cap = 0; bool label_major = true, deferred = true, leaders = false, compat = false;
  double inputs_bytes = 0;   // setup / calib sections mapped by the caller (tables, neighbours)
};

inline uint64_t pow2_at_least(uint64_t x) { uint64_t n = 16; while (n < x) n <<= 1; return n; }

inline double store_peak_bytes(uint64_t c, uint64_t s, double k) {
  const double e = 26.0 + 4.0 * k, idx = 4.0 * (double)pow2_at_least(2 * c + 2);
  return 2.0 * c * e + s * 4.0 * k            // old + new kept runs, pool over-reservation
         + 1.5 * (double)pow2_at_least(s) * e   // staging capacity incl. reallocation
         + s * 64.0 + (double)s + (double)c + 4.0 * c   // sort refs + temporary copy, flags, alive list
         + 2.0 * idx                            // old + new index
         + c * e + idx;                         // one stale snapshot generation
}

inline MemPlan island_memory(const MemSizes& z, double k) {
  MemPlan m; m.G = z.G; m.k = k;
  const double e = 26.0 + 4.0 * k, kq = std::min<double>(z.K, 3.0 * k);
  const uint64_t c = z.cap, m_lab = (uint64_t)z.p + (uint64_t)z.B + 2;
  const uint64_t s = z.deferred ? std::max<uint64_t>(8192, c / 2) : std::max<uint64_t>(4096, c / 4);
  const double T = std::max(1, z.threads), G = z.G, p = z.p, n = z.n;
  const uint64_t ntile = ((uint64_t)z.p + z.tile - 1) / z.tile;
  auto add = [&](const char* nm, double b) { m.items.push_back({nm, (uint64_t)b}); m.total += (uint64_t)b; };
  add("inputs", n * p * 8 + 16 * p + z.inputs_bytes);
  if (z.label_major) add("x_tiles", (double)ntile * z.tile * n * 8);
  add("store", store_peak_bytes(c, s, k));
  if (z.leaders) { const uint64_t cl = 20ULL * (uint64_t)z.p; add("leaders", 2.0 * store_peak_bytes(cl, std::max<uint64_t>(4096, cl / 4), k)); }
  add("worker_bufs", T * 1.5 * (double)pow2_at_least(65536) * e * (z.leaders ? 3 : 1));
  add("rb", 32 * p + (z.label_major ? 0.0 : 16 * p * T) + (z.compat ? 8 * p : 0.0) + (double)z.Hm * p * 8 + 16 * p);
  if (z.label_major) {
    add("orders", 2.0 * G * m_lab * 4 + G * (z.B + 2) * 8);
    add("rows", 2.0 * G * p * 8);
    add("supports", G * 32.0 * kq * kq + G * kq * n * 8 + T * G * kq * z.tile * 8);
  } else {
    add("supports", T * (32.0 * kq * kq + kq * n * 8));
  }
  add("particles", (2.0 * z.N + G) * (4 * k + 64) + z.N * 4 * k);
  add("ckpt", 2.0 * 1048576);
  return m;
}
inline std::string mem_plan_text(const MemPlan& m) {
  std::string s;
  for (auto& it : m.items) { s += it.name + "=" + std::to_string(it.bytes >> 20) + "MiB "; }
  s += "total=" + std::to_string(m.total >> 20) + "MiB (G=" + std::to_string(m.G) + ", k=" + std::to_string(m.k) + ")";
  return s;
}

}  // namespace v4::island
