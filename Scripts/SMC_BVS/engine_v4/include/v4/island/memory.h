// memory.h -- peak-live memory accounting of one island and the --mem-budget admission (manager Q3, Q4; Sol F2).
//
// island_memory() is a deterministic function of the configuration, the sizes (n, p, K), the thread count, the group
// size G and an estimate k of the mean support size of the stored models. It counts every allocation of the island
// that grows with p, c, N, G or threads (ESTIMATE where it depends on k; exact otherwise):
//   x_tiles      label-major: the tiled row-major copy of X               ntile * tile * n * 8
//   store_peak   kept run (old) + new kept run during a compaction        2 c (26 + 4k)
//                staging (deferred mode: hard limit c/2; serial: c/4)     s (26 + 4k)  + s * 33 (sort refs, flags)
//                dead flags + alive list                                  5 c
//                hash indexes (old + new)                                 2 * 4 * pow2(2c + 2)
//                (worker snapshots are released before every pass-boundary compaction, so at most two kept runs live)
//   worker_bufs  T offer buffers                                          T * 65,536 * (26 + 4k)
//   rb           measured-round and total accumulators (16 B)             32 p   (particle-major: + T * 16 p)
//   orders       label-major group: orders + inverse orders               2 G m * 4
//   rows         label-major group: log m and odds rows per support       2 G p * 8   (distinct supports <= G)
//   products     gathered active columns + per-thread product tiles       G k n * 8 + T G k tile * 8
//   particles    two populations                                          2 N (4k + 64)
//   ckpt         streamed checkpoint buffers                              2 MiB
// Not counted (inputs shared by every island of a node, budgeted by WP1/WP2): X itself (n p 8), z, diag(G), setup tables.
#pragma once
#include <cstdint>
#include <string>
#include <vector>

namespace v4::island {

struct MemItem { std::string name; uint64_t bytes; };
struct MemPlan { std::vector<MemItem> items; uint64_t total = 0; int G = 0; double k = 0; };

inline uint64_t pow2_at_least(uint64_t x) { uint64_t n = 16; while (n < x) n <<= 1; return n; }

inline MemPlan island_memory(int n, int p, int N, int B, uint64_t cap, int threads, int G, int tile, bool label_major, bool deferred,
                             double k) {
  MemPlan m; m.G = G; m.k = k;
  const double e = 26.0 + 4.0 * k;
  const uint64_t c = cap, m_lab = (uint64_t)p + (uint64_t)B + 2;
  const uint64_t s = deferred ? std::max<uint64_t>(8192, c / 2) : std::max<uint64_t>(4096, c / 4);
  const uint64_t T = (uint64_t)std::max(1, threads), ntile = ((uint64_t)p + tile - 1) / tile;
  auto add = [&](const char* nm, double b) { m.items.push_back({nm, (uint64_t)b}); m.total += (uint64_t)b; };
  if (label_major) add("x_tiles", (double)ntile * tile * n * 8);
  add("store_peak", 2.0 * c * e + s * e + s * 33.0 + 5.0 * c + 2.0 * 4.0 * pow2_at_least(2 * c + 2));
  add("worker_bufs", (double)T * 65536.0 * e);
  add("rb", 32.0 * p + (label_major ? 0.0 : 16.0 * T * p));
  if (label_major) {
    add("orders", 2.0 * G * m_lab * 4);
    add("rows", 2.0 * G * (double)p * 8);
    add("products", (double)G * k * n * 8 + (double)T * G * k * tile * 8);
  }
  add("particles", 2.0 * N * (4.0 * k + 64));
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
