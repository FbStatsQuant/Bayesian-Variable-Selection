// memory.h -- peak-live memory plan of one island and the --mem-budget admission (manager Q3, Q4; Sol F2; review PR24 P2).
//
// island_memory() is an UPPER BOUND of the island process's memory, given k = the mean size of the stored models (an
// entry costs e = 26 + 4k bytes). Every allocation that grows with p, c, N, G, K or threads is counted:
//   inputs       X (n p 8) + z + diag(G) (16 p), owned by the island process; plus MemSizes::inputs_bytes, which the CLI
//                sets to the mapped setup / calib sections (tables, neighbours). --mem-budget is the TASK's memory: the
//                plan includes the data, and the caller adds the setup inputs through inputs_bytes (INTERFACES §7 note,
//                requested from WP1).
//   x_tiles      label-major: the tiled row-major copy of X                      ntile * tile * n * 8
//   store        store_peak_bytes(): deferred (label-major): old + new kept run 2 c e, staging reserved at c/2: (c/2) e,
//                sort refs + the sort scratch of psort_noalloc (c/2) 64, flags, alive list 5 c, two indexes 2 * 4 pow2(2c + 2);
//                serial (particle-major): staging c/4, refs 32, pool over-reservation (c/4) 4k, + one stale generation
//   k            the plan's mean stored |S|: max(8, q90(pi_0 size) + 1, k_store) -- round 1 stores pi_0-sized models
//   leaders      (calibration islands, option `leaders`) two stores of cap 20p, the same terms as the top store (deferred:
//                parallel compaction at pass boundaries, WP7 O3; serial for particle-major and with leaders_deferred = false)
//   worker_bufs  T offer buffers per store, capacity pow2(65,536) x 1.5          T * 98,304 * e * (1 or 3)
//   rb           u128 accumulators 32 p (+ particle-major 16 p T) (+ compat 8 p) + rb_round Hm p 8 + rb_acc, pip 16 p
//   orders       label-major group: orders + inverse orders + U/N/I lists        2 G m 4 + G (B + 2) 8
//   rows         label-major group: log m and odds rows per support              2 G p 8
//   gram_rows    label-major with bounded scoring (K3): Gram rows of active columns kept across passes   slots p 8
//   supports     support caches (4 k_q^2 doubles each), gathered columns, per-thread product tiles
//                with k_q = min(K, 3k): G (32 k_q^2) + G k_q n 8 + T G k_q tile 8
//   lm_scratch   label-major per-thread scratch (sized before the parallel regions)  T (18 tile + 64 k_q + 64)
//   particles    two populations + pending + terminal supports                   (2N + G) (4k + 64) + N 4k
//   ckpt         streamed checkpoint buffers                                     2 MiB
//   headroom     12 % of every term except the inputs (allocator slack, run-to-run variation of the peak)
//   calib_snapshot  calibration islands: the round-start kept runs (top, leaders) + a copy of the population
// Allocator: for particle-major islands with threads > 1 (their serial store compacts on worker threads) run_island fixes
// glibc's mmap threshold (4 MiB), so every large array (kept runs, staging, indexes) is mmapped and returned to the
// system when freed, whichever thread's arena freed it (re-check m1: with the dynamic threshold, freed kept runs stayed
// resident in per-thread arenas: +9-21 % over the plan at 3 threads).
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
  bool leaders_serial = false;   // the leader stores compact serially although the island is deferred (IslandConfig::leaders_deferred = false: bench / tests)
  int gram_slots = 0;        // K3: Gram-row slots (gram_slots_of)
  double inputs_bytes = 0;   // setup / calib sections mapped by the caller (tables, neighbours)
  bool calib = false;        // calibration island: the round-start snapshot (one kept run per store + the particles)
};

inline uint64_t pow2_at_least(uint64_t x) { uint64_t n = 16; while (n < x) n <<= 1; return n; }

// Peak of one store during a compaction. Deferred (label-major, review P2): the staging area is reserved at its hard
// limit and never reaches it (bounded waves), the parallel path allocates the new pool exactly and runs after all workers
// released their snapshots: old + new kept run + staging + sort refs and the sort scratch + flags + two indexes.
// Serial (particle-major, or a store without deferral): staging at its limit, std::sort refs, the new pool over-reserved
// by the staged pool, and one stale snapshot generation held by another worker.
inline double store_peak_bytes(uint64_t c, bool deferred, double k) {
  const double e = 26.0 + 4.0 * k, idx = 4.0 * (double)pow2_at_least(2 * c + 2);
  if (deferred) {
    const uint64_t s = std::max<uint64_t>(8192, c / 2);
    return 2.0 * c * e + (double)s * e + s * 64.0 + (double)s + 5.0 * c + 2.0 * idx;
  }
  const uint64_t s = std::max<uint64_t>(4096, c / 4) + 65536;   // staging reserved at limit + one buffer (re-check m1)
  return 2.0 * c * e + (double)s * e + s * 32.0 + s * 4.0 * k + (double)s + 5.0 * c + 2.0 * idx + c * e + idx;
}

inline MemPlan island_memory(const MemSizes& z, double k) {
  MemPlan m; m.G = z.G; m.k = k;
  const double e = 26.0 + 4.0 * k, kq = std::min<double>(z.K, 3.0 * k);
  const uint64_t c = z.cap, m_lab = (uint64_t)z.p + (uint64_t)z.B + 2;
  const double T = std::max(1, z.threads), G = z.G, p = z.p, n = z.n;
  const uint64_t ntile = ((uint64_t)z.p + z.tile - 1) / z.tile;
  auto add = [&](const char* nm, double b) { m.items.push_back({nm, (uint64_t)b}); m.total += (uint64_t)b; };
  add("inputs", n * p * 8 + 16 * p + z.inputs_bytes);
  if (z.label_major) add("x_tiles", (double)ntile * z.tile * n * 8);
  add("store", store_peak_bytes(c, z.deferred, k));
  if (z.leaders) { const uint64_t cl = 20ULL * (uint64_t)z.p; add("leaders", 2.0 * store_peak_bytes(cl, z.deferred && !z.leaders_serial, k)); }   // WP7 O3: deferred parallel compaction like the top store, unless leaders_deferred = false
  add("worker_bufs", T * 1.5 * (double)pow2_at_least(65536) * e * (z.leaders ? 3 : 1));
  add("rb", 32 * p + (z.label_major ? 0.0 : 16 * p * T) + (z.compat ? 8 * p : 0.0) + (double)z.Hm * p * 8 + 16 * p);
  if (z.label_major) {
    add("orders", 2.0 * G * m_lab * 4 + G * (z.B + 2) * 8);
    add("rows", 2.0 * G * p * 8);
    if (z.gram_slots > 0) add("gram_rows", (double)z.gram_slots * p * 8);
    add("supports", G * 32.0 * kq * kq + G * kq * n * 8 + T * G * kq * z.tile * 8);
    add("lm_scratch", T * (18.0 * z.tile + 64.0 * kq + 64.0));
  } else {
    add("supports", T * (32.0 * kq * kq + kq * n * 8));
  }
  add("particles", (2.0 * z.N + G) * (4 * k + 64) + z.N * 4 * k);
  if (z.calib) {   // round-start snapshot for the ledger so far (WP3_DESIGN §1.11): a kept run held per store + a population copy
    const double cl = z.leaders ? 2.0 * 20.0 * z.p : 0.0, idxl = z.leaders ? 2.0 * 4.0 * (double)pow2_at_least(2 * 20ULL * (uint64_t)z.p + 2) : 0.0;
    add("calib_snapshot", ((double)c + cl) * e + 4.0 * (double)pow2_at_least(2 * c + 2) + idxl + z.N * (4 * k + 64));
  }
  add("ckpt", 2.0 * 1048576);
  // headroom (manager 11-16, after the PR #26 re-check): 12 % of every term except the inputs. The terms above are
  // upper bounds of the arrays, but the measured peak also carries allocator slack (free lists, arena tails, page
  // rounding) and varies between runs of the same configuration (VmHWM 220 vs 237 MiB in one label-major row at
  // p = 2e4, against a 243 MiB plan): the headroom keeps the plan >= 10 % over every measured row.
  { uint64_t rest = 0; for (const auto& it : m.items) if (it.name != "inputs") rest += it.bytes; add("headroom", 0.12 * (double)rest); }
  return m;
}
inline std::string mem_plan_text(const MemPlan& m) {
  std::string s;
  for (auto& it : m.items) { s += it.name + "=" + std::to_string(it.bytes >> 20) + "MiB "; }
  s += "total=" + std::to_string(m.total >> 20) + "MiB (G=" + std::to_string(m.G) + ", k=" + std::to_string(m.k) + ")";
  return s;
}

}  // namespace v4::island
