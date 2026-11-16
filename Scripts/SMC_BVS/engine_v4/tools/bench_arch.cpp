// bench_arch.cpp -- WP3 architect measurements (branch exp/P1M-wp3-arch; prototypes, not production code).
// Every number is thread-time on the machine it runs on unless labelled wall. Modes:
//   check <cap> <k> <threads>
//        cost of the I1 store invariant (TopStore::check_invariant, serial, run after every step when
//        IslandConfig::check_store is true) on a full store of `cap` models of size k; and of a parallel variant.
//   products <nA> <ntile> <threads> [n] [tile]
//        ns per multiply-add of the tile products: block 1, block 4 (the engine's bits) and block 4 with FMA (class A only).
//   fy <m> <threads> <reps>
//        Fisher-Yates round order + inverse: the L5 code against deeper look-ahead (identical permutations).
//   comp <p> <bsz> <nsup> <threads> <scatter:0|1> [small_pages:0|1]
//        the composite-table read of comp_add with production-sized tables (blocks of bsz), and with a singleton array.
#include <omp.h>
#include <sys/mman.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <string>
#include <vector>
#include "v4/island/island.h"

using namespace v4::island;
static double now() { return omp_get_wtime(); }

// the same predicate as TopStore::check_invariant, over disjoint index ranges (each entry: one order compare with its
// predecessor, one index lookup); the conjunction does not depend on the split
static bool check_invariant_parallel(const TopStore& st, int threads) {
  const Kept& K = *st.k;
  if (K.size() > st.cap) return false;
  bool ok = true;
  #pragma omp parallel for num_threads(threads) schedule(static) reduction(&& : ok)
  for (size_t i = 0; i < K.size(); ++i) {
    if (i > 0 && !st.ord_less(K.ref(i - 1), K.ref(i))) ok = false;
    if (K.find(K.ref(i)) != (int64_t)i) ok = false;
  }
  return ok;
}

static void bench_check(uint64_t cap, int k, int T) {
  TopStore st; st.init(cap, Order::HPM); st.dup_filter = false;
  std::vector<StoreBuffer> bufs(T);
  double t0 = now();
  #pragma omp parallel num_threads(T)
  {
    std::mt19937_64 g(omp_get_thread_num() + 1); std::normal_distribution<double> nd;
    std::vector<int32_t> S(k);
    #pragma omp for
    for (long i = 0; i < (long)cap; ++i) {
      // distinct models: the first two members encode i, the rest are fixed large labels
      S[0] = (int32_t)(i % 1000000); if (k > 1) S[1] = (int32_t)(1000000 + i / 1000000);
      for (int a = 2; a < k; ++a) S[a] = 2100000 + a;
      uint64_t hx = (uint64_t)i;
      st.offer(bufs[omp_get_thread_num()], nd(g), S.data(), (uint32_t)k, splitmix64(hx));
    }
  }
  for (auto& b : bufs) st.flush(b);
  st.compact();
  double tfill = now() - t0;
  t0 = now(); bool ok1 = st.check_invariant(); double tser = now() - t0;
  t0 = now(); bool ok2 = check_invariant_parallel(st, T); double tpar = now() - t0;
  std::printf("check cap=%llu k=%d: store built in %.1f s wall (%d threads); check_invariant serial %.2f s (%.1f ns per entry, ok %d); "
              "parallel %d threads %.2f s wall (ok %d)\n", (unsigned long long)cap, k, tfill, T, tser, 1e9 * tser / (double)st.size(), (int)ok1, T, tpar, (int)ok2);
}

// ---- products: per multiply-add cost of the tile products, mul + add (the engine's bits) against FMA (class A only) ----
// block 4 with fma8: s = fma(x_a[i], x_j[i], s), sequential in i per lane. Not the bits of core's Gram entry (one rounding
// per term instead of two); usable only in class A, and only if the particle-major reference (eval1) does the same.
// products <nA> <ntile> <threads> [n] [tile]: ntile distinct tiles (ntile * tile * n * 8 bytes: choose it larger than the
// caches to include the DRAM stream of X, as in a pass), T threads each sweeping all of them
static void bench_products(int nA, int ntile, int T, int n, int Bk) {
  avec<double> XA((size_t)nA * n), Xt((size_t)ntile * Bk * n);
  std::mt19937_64 g(7); std::normal_distribution<double> nd;
  for (auto& x : XA) x = nd(g);
  for (auto& x : Xt) x = nd(g);
  double tt[3] = {0, 0, 0}; double maxrel = 0;
  for (int var = 0; var < 3; ++var) {
    double t0 = now();
    #pragma omp parallel num_threads(T)
    {
      avec<double> P((size_t)nA * Bk);
      #pragma omp for schedule(dynamic, 1)
      for (int ti = 0; ti < ntile; ++ti) {
        const double* X = &Xt[(size_t)ti * Bk * n];
        if (var == 0) tile_products(XA.data(), nA, n, X, Bk, P.data(), 1);
        else if (var == 1) tile_products(XA.data(), nA, n, X, Bk, P.data(), 4);
        else tile_products_fma4(XA.data(), nA, n, X, Bk, P.data());
      }
    }
    tt[var] = now() - t0;
  }
  {   // accuracy of the FMA products against the mul + add bits (class-A sized difference expected)
    avec<double> P1((size_t)nA * Bk), P2((size_t)nA * Bk);
    tile_products(XA.data(), nA, n, Xt.data(), Bk, P1.data(), 4); tile_products_fma4(XA.data(), nA, n, Xt.data(), Bk, P2.data());
    for (size_t i = 0; i < P1.size(); ++i) maxrel = std::max(maxrel, std::fabs(P1[i] - P2[i]) / std::max(1.0, std::fabs(P1[i])));
  }
  const double ops = (double)ntile * nA * Bk * n;
  std::printf("products nA=%d tiles=%d (%.0f MB of X) n=%d tile=%d threads=%d: ns per multiply-add (thread-time): block1 %.4f, block4 %.4f, "
              "block4-FMA %.4f (max |diff| vs mul+add %.2e, scaled by max(1,|g|))\n", nA, ntile, (double)ntile * Bk * n * 8 / 1e6, n, Bk, T,
              1e9 * tt[0] * T / ops, 1e9 * tt[1] * T / ops, 1e9 * tt[2] * T / ops, maxrel);
}

// ---- Fisher-Yates round order: L5 (uniforms 8 at a time, targets prefetched one block ahead) against a deeper
// look-ahead (W uniforms ahead, W a multiple of 8). The same swaps in the same order: identical permutations. ----
static void fy_l5(const v4::Ctr4& ctr, const v4::Key2& kk, int m, uint32_t* ord) {
  for (int t = 0; t < m; ++t) ord[t] = (uint32_t)t;
  const int nd = m - 1; int jcur[8], jnext[8]; uint32_t sl[8]; double u8[8];
  auto block = [&](int d0, int* jj) {
    for (int l = 0; l < 8; ++l) sl[l] = v4::slot_of(v4::SK_ORDER, (uint32_t)std::min(d0 + l, std::max(0, nd - 1)));
    philox8_word(ctr.data(), kk.data(), 0, sl, u8);
    for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); jj[l] = (int)std::floor(u8[l] * (t + 1)); __builtin_prefetch(&ord[jj[l]], 1); }
  };
  if (nd > 0) block(0, jcur);
  for (int d0 = 0; d0 < nd; d0 += 8) {
    if (d0 + 8 < nd) block(d0 + 8, jnext);
    for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); std::swap(ord[t], ord[jcur[l]]); }
    std::memcpy(jcur, jnext, sizeof jcur);
  }
}
static void fy_deep(const v4::Ctr4& ctr, const v4::Key2& kk, int m, uint32_t* ord, int W) {
  for (int t = 0; t < m; ++t) ord[t] = (uint32_t)t;
  const int nd = m - 1;
  std::vector<int> ring(2 * W);   // targets of draws [base, base + 2W)
  auto fill = [&](int d0, int* jj) {   // W targets from draw d0, prefetched
    uint32_t sl[8]; double u8[8];
    for (int b = 0; b < W; b += 8) {
      for (int l = 0; l < 8; ++l) sl[l] = v4::slot_of(v4::SK_ORDER, (uint32_t)std::min(d0 + b + l, std::max(0, nd - 1)));
      philox8_word(ctr.data(), kk.data(), 0, sl, u8);
      for (int l = 0; l < 8; ++l) { const int d = d0 + b + l; if (d >= nd) break; const int t = m - 1 - d; jj[b + l] = (int)std::floor(u8[l] * (t + 1)); __builtin_prefetch(&ord[jj[b + l]], 1); }
    }
  };
  int* cur = ring.data(); int* nxt = ring.data() + W;
  if (nd > 0) fill(0, cur);
  for (int d0 = 0; d0 < nd; d0 += W) {
    if (d0 + W < nd) fill(d0 + W, nxt);
    const int lim = std::min(W, nd - d0);
    for (int l = 0; l < lim; ++l) { const int t = m - 1 - (d0 + l); std::swap(ord[t], ord[cur[l]]); }
    std::swap(cur, nxt);
  }
}
// fy <m> <threads> <reps>: every thread draws `reps` orders of m labels and their inverses (its own arrays, as a group does)
static void bench_fy(int m, int T, int reps) {
  const int Ws[] = {0, 16, 32, 64, 128};   // 0 = the L5 code
  for (int W : Ws) {
    double tfy = 0, tinv = 0; bool same = true;
    #pragma omp parallel num_threads(T) reduction(+ : tfy, tinv) reduction(&& : same)
    {
      std::vector<uint32_t> ord(m), inv(m), ref;
      for (int r = 0; r < reps; ++r) {
        Address a0; a0.seed = 2026; a0.island = 1; a0.xph = X_MEASURED; a0.stage = 1; a0.particle = (uint32_t)(omp_get_thread_num() * 1000 + r + 1);
        a0.slot = v4::slot_of(v4::SK_ORDER, 0);
        const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
        double t0 = now();
        if (W == 0) fy_l5(ctr, kk, m, ord.data()); else fy_deep(ctr, kk, m, ord.data(), W);
        double t1 = now();
        for (int t = 0; t < m; ++t) { if (t + 16 < m) __builtin_prefetch(&inv[ord[t + 16]], 1); inv[ord[t]] = (uint32_t)t + 1; }
        double t2 = now();
        tfy += t1 - t0; tinv += t2 - t1;
        if (W != 0 && r == 0) { ref.resize(m); fy_l5(ctr, kk, m, ref.data()); same = same && ref == ord; }
      }
    }
    std::printf("fy m=%d threads=%d look-ahead %s: Fisher-Yates %.1f ns per label, inverse %.1f ns per label (thread-time)%s\n", m, T,
                W == 0 ? "8 (L5)" : std::to_string(W).c_str(), 1e9 * tfy / ((double)T * reps * m), 1e9 * tinv / ((double)T * reps * m),
                W == 0 ? "" : (same ? "; identical to L5" : "; DIFFERENT"));
  }
}

// ---- composite sum of an addition (comp_add): cost of the table read with production-sized tables ----
// The benches use a stand-in partition (blocks of 4: 16 codes per block, a 32 MB table at 1e6). WP2's partition packs
// blocks to a mean of 13.2 of B_V = 14 (D-18/D-19: ~850 codes per column, ~7 GB at 1e6), and comp_add reads the
// singleton code logr[code_ptr[b] + (1 << pos)] of every scored label: one random read into that table per flip.
// comp <p> <bsz> <nsup> <threads> <scatter:0|1>: synthetic tables (random values; timing only) for blocks of bsz,
// contiguous (scatter 0: AR-like clusters) or with labels assigned to blocks at random (scatter 1); nsup supports of 6
// random members; ns per (support, label) of comp_add as coded, and with a p-indexed array of the singleton terms
// lr1[j] = logr[blk[j]][1 << pos[j]] (same doubles, same additions in the same order: identical results, checked).
static void bench_comp(int p, int bsz, int nsup, int T, int scatter, int small_pages) {
  Start st; st.J = (p + bsz - 1) / bsz;
  st.blk.assign(p, 0); st.pos.assign(p, 0);
  std::vector<int> perm(p); for (int j = 0; j < p; ++j) perm[j] = j;
  std::mt19937_64 g(99);
  if (scatter) std::shuffle(perm.begin(), perm.end(), g);
  std::vector<int> bsize(st.J, 0);
  for (int t = 0; t < p; ++t) { const int j = perm[t], b = t / bsz; st.blk[j] = b; st.pos[j] = bsize[b]++; }
  st.code_ptr.assign(st.J + 1, 0);
  for (int b = 0; b < st.J; ++b) st.code_ptr[b + 1] = st.code_ptr[b] + ((int64_t)1 << bsize[b]);
  double t0 = now();
  // small_pages = 1: the table on 4 KB pages (as a mapped setup.bin section is: file pages are not huge pages); the
  // default heap allocation is on transparent 2 MB pages where the machine enables them
  st.logr_flat.reserve((size_t)st.code_ptr[st.J]);
  if (small_pages) {
    const uintptr_t a = ((uintptr_t)st.logr_flat.data() + 4095) & ~(uintptr_t)4095; const size_t len = ((size_t)st.code_ptr[st.J] * 8) & ~(size_t)4095;
    if (len > 4096 && madvise((void*)a, len - 4096, MADV_NOHUGEPAGE) != 0) std::printf("# madvise(MADV_NOHUGEPAGE) failed\n");
  }
  st.logr_flat.resize((size_t)st.code_ptr[st.J]);
  #pragma omp parallel for num_threads(T) schedule(static)
  for (int64_t i = 0; i < st.code_ptr[st.J]; ++i) { uint64_t x = (uint64_t)i; st.logr_flat[i] = -1e-3 * (double)(splitmix64(x) >> 44); }
  std::vector<double> lr1(p);
  for (int j = 0; j < p; ++j) lr1[j] = st.lr(st.blk[j], 1u << st.pos[j]);
  std::printf("# comp tables p=%d blocks of %d (%s; %s pages): %.2f GB of logr, built in %.1f s\n", p, bsz, scatter ? "labels scattered over blocks" : "contiguous blocks",
              small_pages ? "4 KB" : "default (huge where enabled)", (double)st.logr_flat.size() * 8 / 1073741824.0, now() - t0);
  {   // the table pages a phase-A sweep touches: the singleton codes of every label
    std::vector<uint64_t> pg; pg.reserve(p);
    for (int j = 0; j < p; ++j) pg.push_back((uint64_t)(st.code_ptr[st.blk[j]] + ((int64_t)1 << st.pos[j])) * 8 / 4096);
    std::sort(pg.begin(), pg.end()); const size_t np = std::unique(pg.begin(), pg.end()) - pg.begin();
    std::printf("# singleton codes touch %zu of %zu 4 KB pages of logr (%.1f%%, %.2f GB); %.2f pages per label\n", np, st.logr_flat.size() * 8 / 4096,
                100.0 * np / (st.logr_flat.size() * 8 / 4096.0), np * 4096.0 / 1073741824.0, (double)np / p);
  }
  std::vector<SupportCache> sup(nsup);
  for (auto& c : sup) {   // the composite-block part of build_support (kernel.h), on random supports of 6 members
    Model S; while ((int)S.size() < 6) { int j = (int)(g() % p); if (!contains(S, j)) sorted_insert(S, j); }
    c.S = S; c.k = 6;
    std::vector<std::pair<int, int>> pr; for (int j : S) pr.push_back({st.blk[j], st.pos[j]});
    std::sort(pr.begin(), pr.end());
    c.bb.clear(); c.bcode.clear(); c.bterm.clear(); c.bpre.assign(1, 0.0);
    for (size_t i = 0; i < pr.size();) {
      int b = pr[i].first; uint32_t code = 0;
      while (i < pr.size() && pr[i].first == b) { code |= 1u << pr[i].second; ++i; }
      c.bb.push_back(b); c.bcode.push_back(code); c.bterm.push_back(st.lr(b, code)); c.bpre.push_back(c.bpre.back() + c.bterm.back());
    }
  }
  const int Bk = 128, ntile = p / Bk; double tt[2]; uint64_t chk[2] = {0, 0};
  for (int var = 0; var < 2; ++var) {
    uint64_t acc = 0; t0 = now();   // order-free check: the sum of the results' bit patterns
    #pragma omp parallel for num_threads(T) schedule(dynamic, 4) reduction(+ : acc)
    for (int ti = 0; ti < ntile; ++ti) {
      const int j0 = ti * Bk;
      for (const auto& c : sup) {
        for (int jj = 0; jj < Bk; ++jj) {
          const int j = j0 + jj;
          if (std::binary_search(c.S.begin(), c.S.end(), j)) continue;
          double v;
          if (var == 0) v = comp_add(st, c, j);
          else {   // the same sum with the singleton term from the p-indexed array when the label's block does not meet S
            const int b = st.blk[j];
            size_t mm = std::lower_bound(c.bb.begin(), c.bb.end(), b) - c.bb.begin();
            if (mm < c.bb.size() && c.bb[mm] == b) v = comp_add(st, c, j);
            else { v = c.bpre[mm] + lr1[j]; for (; mm < c.bb.size(); ++mm) v += c.bterm[mm]; }
          }
          uint64_t bits; std::memcpy(&bits, &v, 8); acc += bits;
        }
      }
    }
    tt[var] = now() - t0; chk[var] = acc;
  }
  const double pairs = (double)ntile * Bk * nsup;
  std::printf("comp p=%d bsz=%d scatter=%d supports=%d threads=%d: comp_add %.1f ns per (support,label) (thread-time); with the singleton array %.1f ns; "
              "sums %s\n", p, bsz, scatter, nsup, T, 1e9 * tt[0] * T / pairs, 1e9 * tt[1] * T / pairs, chk[0] == chk[1] ? "identical" : "DIFFERENT");
}

int main(int argc, char** argv) {
  if (argc < 2) { std::fprintf(stderr, "see header\n"); return 1; }
  std::string mode = argv[1];
  if (mode == "check" && argc >= 5) bench_check(strtoull(argv[2], 0, 10), atoi(argv[3]), atoi(argv[4]));
  else if (mode == "products" && argc >= 5) bench_products(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), argc > 5 ? atoi(argv[5]) : 200, argc > 6 ? atoi(argv[6]) : 128);
  else if (mode == "fy" && argc >= 5) bench_fy(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]));
  else if (mode == "comp" && argc >= 7) bench_comp(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), atoi(argv[6]), argc > 7 ? atoi(argv[7]) : 0);
  else { std::fprintf(stderr, "unknown mode or missing arguments (see header)\n"); return 1; }
  return 0;
}
