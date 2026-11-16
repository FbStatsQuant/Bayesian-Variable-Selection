// bench_arch.cpp -- WP3 architect measurements (branch exp/P1M-wp3-arch; prototypes, not production code).
// Every number is thread-time on the machine it runs on unless labelled wall. Modes:
//   check <cap> <k> <threads>
//        cost of the I1 store invariant (TopStore::check_invariant, serial, run after every step when
//        IslandConfig::check_store is true) on a full store of `cap` models of size k; and of a parallel variant.
//   products <nA> <ntile> <threads> [n] [tile]
//        ns per multiply-add of the tile products: block 1, block 4 (the engine's bits) and block 4 with FMA (class A only).
//   fy <m> <threads> <reps>
//        Fisher-Yates round order + inverse: the L5 code against deeper look-ahead (identical permutations).
#include <omp.h>
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
static void tile_products_fma4(const double* XA, int nA, int n, const double* Xtile, int Bk, double* P) {
  int a = 0;
  for (; a + 4 <= nA; a += 4) {
    const double *x0 = XA + (size_t)a * n, *x1 = x0 + n, *x2 = x1 + n, *x3 = x2 + n;
    for (int c0 = 0; c0 < Bk; c0 += 32) {
      v8d a00 = bc(0), a01 = bc(0), a02 = bc(0), a03 = bc(0), a10 = bc(0), a11 = bc(0), a12 = bc(0), a13 = bc(0);
      v8d a20 = bc(0), a21 = bc(0), a22 = bc(0), a23 = bc(0), a30 = bc(0), a31 = bc(0), a32 = bc(0), a33 = bc(0);
      const double* rp = Xtile + c0;
      for (int i = 0; i < n; ++i, rp += Bk) {
        const v8d r0 = load8(rp), r1 = load8(rp + 8), r2 = load8(rp + 16), r3 = load8(rp + 24);
        const v8d b0 = bc(x0[i]), b1 = bc(x1[i]), b2 = bc(x2[i]), b3 = bc(x3[i]);
        a00 = fma8(b0, r0, a00); a01 = fma8(b0, r1, a01); a02 = fma8(b0, r2, a02); a03 = fma8(b0, r3, a03);
        a10 = fma8(b1, r0, a10); a11 = fma8(b1, r1, a11); a12 = fma8(b1, r2, a12); a13 = fma8(b1, r3, a13);
        a20 = fma8(b2, r0, a20); a21 = fma8(b2, r1, a21); a22 = fma8(b2, r2, a22); a23 = fma8(b2, r3, a23);
        a30 = fma8(b3, r0, a30); a31 = fma8(b3, r1, a31); a32 = fma8(b3, r2, a32); a33 = fma8(b3, r3, a33);
      }
      double* p0 = P + (size_t)a * Bk + c0; double* p1 = p0 + Bk; double* p2 = p1 + Bk; double* p3 = p2 + Bk;
      store8(p0, a00); store8(p0 + 8, a01); store8(p0 + 16, a02); store8(p0 + 24, a03);
      store8(p1, a10); store8(p1 + 8, a11); store8(p1 + 16, a12); store8(p1 + 24, a13);
      store8(p2, a20); store8(p2 + 8, a21); store8(p2 + 16, a22); store8(p2 + 24, a23);
      store8(p3, a30); store8(p3 + 8, a31); store8(p3 + 16, a32); store8(p3 + 24, a33);
    }
  }
  for (; a < nA; ++a) {
    const double* xa = XA + (size_t)a * n; double* Pa = P + (size_t)a * Bk;
    for (int c0 = 0; c0 < Bk; c0 += 8) {
      v8d s0 = bc(0); const double* rp = Xtile + c0;
      for (int i = 0; i < n; ++i, rp += Bk) s0 = fma8(bc(xa[i]), load8(rp), s0);
      store8(Pa + c0, s0);
    }
  }
}
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

int main(int argc, char** argv) {
  if (argc < 2) { std::fprintf(stderr, "see header\n"); return 1; }
  std::string mode = argv[1];
  if (mode == "check" && argc >= 5) bench_check(strtoull(argv[2], 0, 10), atoi(argv[3]), atoi(argv[4]));
  else if (mode == "products" && argc >= 5) bench_products(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), argc > 5 ? atoi(argv[5]) : 200, argc > 6 ? atoi(argv[6]) : 128);
  else if (mode == "fy" && argc >= 5) bench_fy(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]));
  else { std::fprintf(stderr, "unknown mode or missing arguments (see header)\n"); return 1; }
  return 0;
}
