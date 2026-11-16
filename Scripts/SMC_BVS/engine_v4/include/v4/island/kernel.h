// kernel.h -- support cache and the 8-lane flip-score / odds primitives shared by the label-major kernel and the
// particle-major reference (ENGINEERING_SPEC §0-v2.4; INTERFACES §6).
//
// A "support" is the state S of one or more particles at the start of a sweep, together with the particle's path
// values (log m, log gamma_0, d) and the temperature phi. For every label j it gives
//   logm(S △ j)  and the Gibbs inclusion odds o_j = plogis(lgphi(S ∪ j) − lgphi(S \ j))  (core/cpp/v3_engine.h:113-132)
// Additions (j ∉ S) are computed 8 labels at a time from the Gram entries u_a = Σ_i x_{i,S_a} x_{i,j} (sequential in i:
// core/cpp/v3_score.h:45-53), gjj = diag(G)_j and z_j:
//   Arith::Bit     sorted-prefix reuse: the Cholesky rows before the sorted insertion position q are the cached rows of
//                  S, later rows are recomputed in chol_inplace's operation order (core/cpp/v3_score.h:76-90, :204-224).
//                  Equal in bits to BitScorer::score(S ∪ j) (golden-tested). Lanes failing the pivot test, the
//                  Q < 1e-8 y'y test or finiteness fall back to the full scalar scorer (same routes as core/).
//   Arith::ClassA  bordered update with the label appended last, fma8, vector log/exp (amath.h). Same exact-arithmetic
//                  value; ≤ 1e-9 relative to Bit (tested). Failing lanes fall back to the Bit scorer (INTERFACES §6).
// Deletions (j ∈ S) are k full scores by WP1's Bit scorer (both forms), done once per support.
// Numerical failures (review PR21 M1): a score that fails after every fallback never throws out of these primitives;
// it is flagged as log m = NaN and odds = ODDS_FAILED (< 0). The island turns a flagged value into numerical_failure
// only if the particle CONSUMES that label (spec §3 rule 2: scores of unconsumed labels are discarded).
#pragma once
#include "v4/island/amath.h"
#include "v4/island/dep.h"

namespace v4::island {
using namespace v4::island::dep;
inline namespace V4_ISLAND_ISA_NS {

enum class Arith { Bit, ClassA };
// Matrices and lane buffers are sized by the support (no size cap: supports up to K take the vector paths; the
// earlier fixed cap of 24 sent large pi_0 supports to a per-label full-score path, MEASURED 50 us per label at p = 1e5).
struct Mat {   // k x k row-major
  std::vector<double> a; int ld = 0;
  void resize(int k) { ld = k; a.assign((size_t)k * k, 0.0); }
  double* operator[](int r) { return a.data() + (size_t)r * ld; }
  const double* operator[](int r) const { return a.data() + (size_t)r * ld; }
};
struct VMat {  // rows of 8-lane vectors, ld columns
  v8d* p; int ld;
  v8d* operator[](int r) const { return p + (size_t)r * ld; }
};
inline std::vector<v8d>& lane_scratch(int which, size_t n) {   // per-thread scratch: 0 L, 1 w, 2 vH, 3 vA
  thread_local std::vector<v8d> buf[4];
  if (buf[which].size() < n) buf[which].resize(n);
  return buf[which];
}

constexpr double ODDS_FAILED = -1.0;   // flag: the score of this flip failed (odds are otherwise in [0, 1])

struct SupportCache {
  Model S; int k = 0; uint64_t h = 0;
  double logm = 0, lg0 = 0, d = 0, phi = 0, lgphi = 0;  // the particle's path values at this state
  bool fast = false;    // vector path usable (both Cholesky factors of S exist)
  bool add_ok = false;  // k < K (core/cpp/v3_engine.h:116)
  Mat MH, MA, LH, LA;
  std::vector<double> zS, wH, rLH, rLA, preH, preA, preQ;
  // composite sum of S by blocks in increasing block order (core/cpp/v3_start.h:54-66)
  std::vector<int> bb; std::vector<uint32_t> bcode; std::vector<double> bterm, bpre;
  // deletions S \ S[a]
  std::vector<double> del_logm, del_odds;
  std::vector<int> arow;  // row of each member in the pass's active-column product matrix (label-major only)
};

// Tile products P[a][jj] = sum_i x_{i,a} x_{i,j} for the nA gathered active columns XA (n each, contiguous) and the Bk
// labels of a row-major tile (n rows of Bk). Every lane is the sequential sum s = s + x_a[i] * x_j[i], i = 0..n-1, with
// no contraction: the bits of the Gram entry (core/cpp/v3_score.h:45-53) whatever the blocking.
//   block = 1: one active column x 64 labels per sweep of the tile (8 accumulators; the tile is re-read nA times);
//   (an 8-column x 16-label variant measured slower on Owls: 125 vs 83 ns per pair; not kept)
//   block = 4: four active columns x 32 labels (16 accumulators): 4 multiply-adds per tile load instead of 1, the tile is
//              re-read nA/4 times (L2 traffic / 4). Same per-lane operation sequence, same bits (T3 hashes unchanged).
inline void tile_products(const double* XA, int nA, int n, const double* Xtile, int Bk, double* P, int block) {
  int a = 0;
  if (block >= 4) {
    for (; a + 4 <= nA; a += 4) {
      const double *x0 = XA + (size_t)a * n, *x1 = x0 + n, *x2 = x1 + n, *x3 = x2 + n;
      for (int c0 = 0; c0 < Bk; c0 += 32) {
        v8d a00 = bc(0), a01 = bc(0), a02 = bc(0), a03 = bc(0), a10 = bc(0), a11 = bc(0), a12 = bc(0), a13 = bc(0);
        v8d a20 = bc(0), a21 = bc(0), a22 = bc(0), a23 = bc(0), a30 = bc(0), a31 = bc(0), a32 = bc(0), a33 = bc(0);
        const double* rp = Xtile + c0;
        for (int i = 0; i < n; ++i, rp += Bk) {
          const v8d r0 = load8(rp), r1 = load8(rp + 8), r2 = load8(rp + 16), r3 = load8(rp + 24);
          const v8d b0 = bc(x0[i]), b1 = bc(x1[i]), b2 = bc(x2[i]), b3 = bc(x3[i]);
          a00 = a00 + b0 * r0; a01 = a01 + b0 * r1; a02 = a02 + b0 * r2; a03 = a03 + b0 * r3;
          a10 = a10 + b1 * r0; a11 = a11 + b1 * r1; a12 = a12 + b1 * r2; a13 = a13 + b1 * r3;
          a20 = a20 + b2 * r0; a21 = a21 + b2 * r1; a22 = a22 + b2 * r2; a23 = a23 + b2 * r3;
          a30 = a30 + b3 * r0; a31 = a31 + b3 * r1; a32 = a32 + b3 * r2; a33 = a33 + b3 * r3;
        }
        double* p0 = P + (size_t)a * Bk + c0; double* p1 = p0 + Bk; double* p2 = p1 + Bk; double* p3 = p2 + Bk;
        store8(p0, a00); store8(p0 + 8, a01); store8(p0 + 16, a02); store8(p0 + 24, a03);
        store8(p1, a10); store8(p1 + 8, a11); store8(p1 + 16, a12); store8(p1 + 24, a13);
        store8(p2, a20); store8(p2 + 8, a21); store8(p2 + 16, a22); store8(p2 + 24, a23);
        store8(p3, a30); store8(p3 + 8, a31); store8(p3 + 16, a32); store8(p3 + 24, a33);
      }
    }
  }
  for (; a < nA; ++a) {
    const double* xa = XA + (size_t)a * n; double* Pa = P + (size_t)a * Bk;
    for (int c0 = 0; c0 < Bk; c0 += 64) {
      v8d s0 = bc(0), s1 = bc(0), s2 = bc(0), s3 = bc(0), s4 = bc(0), s5 = bc(0), s6 = bc(0), s7 = bc(0);
      const double* rp = Xtile + c0;
      for (int i = 0; i < n; ++i, rp += Bk) {
        v8d xi = bc(xa[i]);
        s0 = s0 + xi * load8(rp);      s1 = s1 + xi * load8(rp + 8);  s2 = s2 + xi * load8(rp + 16); s3 = s3 + xi * load8(rp + 24);
        s4 = s4 + xi * load8(rp + 32); s5 = s5 + xi * load8(rp + 40); s6 = s6 + xi * load8(rp + 48); s7 = s7 + xi * load8(rp + 56);
      }
      store8(Pa + c0, s0); store8(Pa + c0 + 8, s1); store8(Pa + c0 + 16, s2); store8(Pa + c0 + 24, s3);
      store8(Pa + c0 + 32, s4); store8(Pa + c0 + 40, s5); store8(Pa + c0 + 48, s6); store8(Pa + c0 + 56, s7);
    }
  }
}

// [arch] prototype: class-A products with FMA, s = fma(x_a[i], x_j[i], s), sequential in i per lane. NOT the bits of
// core's Gram entry (one rounding per term instead of two): class A only, and the particle-major reference (eval1)
// must do the same so that T3 holds. Process-wide switch, set by the island from IslandConfig::products_fma.
inline bool& products_fma() { static bool on = false; return on; }
inline void tile_products_fma4(const double* XA, int nA, int n, const double* Xtile, int Bk, double* P) {
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

// Composite sum of S ∪ {j} (j ∉ S) and S \ {j} (j ∈ S), same additions in the same order as Start::comp.
inline double comp_add(const Start& st, const SupportCache& s, int j) {
  int b = st.blk[j]; uint32_t bit = 1u << st.pos[j];
  size_t m = std::lower_bound(s.bb.begin(), s.bb.end(), b) - s.bb.begin();
  double c = s.bpre[m];
  if (m < s.bb.size() && s.bb[m] == b) { c += st.lr(b, s.bcode[m] | bit); ++m; }
  else c += st.lr(b, bit);
  for (; m < s.bb.size(); ++m) c += s.bterm[m];
  return c;
}
inline double comp_del(const Start& st, const SupportCache& s, int j) {
  int b = st.blk[j]; uint32_t bit = 1u << st.pos[j];
  size_t m = std::lower_bound(s.bb.begin(), s.bb.end(), b) - s.bb.begin();
  double c = s.bpre[m];
  uint32_t nc = s.bcode[m] & ~bit;
  if (nc) c += st.lr(b, nc);
  for (++m; m < s.bb.size(); ++m) c += s.bterm[m];
  return c;
}

// Build the cache of support S with the particle's path values. BitScorer is per thread.
inline void build_support(const Data& D, const Start& st, BitScorer& sc, SupportCache& s, const Model& S, uint64_t h,
                          double logm, double lg0, double d, double phi) {
  s.S = S; s.k = (int)S.size(); s.h = h; s.logm = logm; s.lg0 = lg0; s.d = d; s.phi = phi;
  s.lgphi = lg0 + phi * d;  // core/cpp/v3_engine.h:14
  const int k = s.k; const double n1 = D.n + 1.0;
  s.add_ok = k < D.K;
  std::vector<double> G((size_t)k * k);
  for (int a = 0; a < k; ++a) for (int b = 0; b <= a; ++b) { double g = gram(D, S[a], S[b]); G[a * k + b] = g; G[b * k + a] = g; }
  s.fast = false;
  s.MH.resize(k); s.MA.resize(k); s.LH.resize(k); s.LA.resize(k);
  s.zS.assign(k, 0.0); s.wH.assign(k, 0.0); s.rLH.assign(k, 0.0); s.rLA.assign(k, 0.0);
  s.preH.assign(k + 1, 0.0); s.preA.assign(k + 1, 0.0); s.preQ.assign(k + 1, 0.0);
  {
    // core/cpp/v3_score.h:180-184: H = (n+1) G_S + I, A = G_S + I, factors by chol_inplace
    std::vector<double> bH((size_t)k * k), bA((size_t)k * k);
    for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) {
      s.MH[a][b] = bH[a * k + b] = n1 * G[a * k + b] + (a == b ? 1.0 : 0.0);
      s.MA[a][b] = bA[a * k + b] = G[a * k + b] + (a == b ? 1.0 : 0.0);
    }
    if (v4::chol_inplace(bH, k) && v4::chol_inplace(bA, k)) {
      s.fast = true;
      for (int a = 0; a < k; ++a) for (int b = 0; b < k; ++b) { s.LH[a][b] = bH[a * k + b]; s.LA[a][b] = bA[a * k + b]; }
      s.preH[0] = s.preA[0] = s.preQ[0] = 0;
      for (int a = 0; a < k; ++a) {
        s.zS[a] = D.z[S[a]];
        double w = s.zS[a];  // core/cpp/v3_score.h:93 forward solve, row a
        for (int t = 0; t < a; ++t) w -= s.LH[a][t] * s.wH[t];
        s.wH[a] = w / s.LH[a][a];
        s.preH[a + 1] = s.preH[a] + pm::log(s.LH[a][a]);   // prefix of the sequential sum of :209
        s.preA[a + 1] = s.preA[a] + pm::log(s.LA[a][a]);
        s.preQ[a + 1] = s.preQ[a] + s.wH[a] * s.wH[a];     // prefix of :216
        s.rLH[a] = 1.0 / s.LH[a][a]; s.rLA[a] = 1.0 / s.LA[a][a];
      }
    }
  }
  // composite blocks
  std::vector<std::pair<int, int>> pr; pr.reserve(k);
  for (int j : S) pr.push_back({st.blk[j], st.pos[j]});
  std::sort(pr.begin(), pr.end());
  s.bb.clear(); s.bcode.clear(); s.bterm.clear(); s.bpre.assign(1, 0.0);
  for (size_t i = 0; i < pr.size();) {
    int b = pr[i].first; uint32_t code = 0;
    while (i < pr.size() && pr[i].first == b) { code |= 1u << pr[i].second; ++i; }
    s.bb.push_back(b); s.bcode.push_back(code); s.bterm.push_back(st.logr[b][code]);
    s.bpre.push_back(s.bpre.back() + s.bterm.back());
  }
  // deletions: score(S \ S[a]) from the cached Gram (bits of core's scorer), odds as core/cpp/v3_engine.h:124-126
  s.del_logm.assign(k, 0.0); s.del_odds.assign(k, 0.0);
  Model Sd;
  for (int a = 0; a < k; ++a) {
    Sd.clear(); for (int t = 0; t < k; ++t) if (t != a) Sd.push_back(S[t]);
    double lm;
    try { lm = sc.score(Sd).logm; }   // WP1's Gram-free Bit scorer: the bits of core's score(S \ S[a])
    catch (const v4::NumericalFailure&) { s.del_logm[a] = std::numeric_limits<double>::quiet_NaN(); s.del_odds[a] = ODDS_FAILED; continue; }
    double c = comp_del(st, s, S[a]);
    double lg0d = D.logprior[k - 1] + c, dd = (lm - D.logm0) - c;
    s.del_logm[a] = lm;
    s.del_odds[a] = plogis_log(s.lgphi - (lg0d + phi * dd));
  }
}

// --- Bit form: 8 labels sharing the sorted insertion position q. Returns the mask of lanes with a valid result. ---
inline unsigned flip8_bit(const Data& D, const SupportCache& s, int q, const v8d* u, v8d gjj, v8d zj, v8d& logm) {
  const int k = s.k, kk = k + 1; const double n1 = D.n + 1.0;
  VMat L{lane_scratch(0, (size_t)kk * kk).data(), kk}; v8d ld[2]; v8d* w = lane_scratch(1, (size_t)kk).data(); v8d quad = bc(0.0);
  unsigned ok = 0xFFu;
  for (int which = 0; which < 2; ++which) {
    const Mat& Ls = which == 0 ? s.LH : s.LA;
    const Mat& Ms = which == 0 ? s.MH : s.MA;
    auto Mlab = [&](int a) { return which == 0 ? bc(n1) * u[a] + bc(0.0) : u[a] + bc(0.0); };
    for (int c = 0; c < q; ++c) {   // row q (the label), columns before it
      v8d x = Mlab(c);
      for (int t = 0; t < c; ++t) x = x - L[q][t] * bc(Ls[c][t]);
      L[q][c] = x / bc(Ls[c][c]);
    }
    for (int c = q; c < kk; ++c) {  // columns from q on
      v8d d = (c == q) ? (which == 0 ? bc(n1) * gjj + bc(1.0) : gjj + bc(1.0)) : bc(Ms[c - 1][c - 1]);
      for (int t = 0; t < c; ++t) { v8d lct = (t < q && c != q) ? bc(Ls[c - 1][t]) : L[c][t]; d = d - lct * lct; }
      ok &= pos_finite_mask(d);
      v8d l = sqrt8(d); L[c][c] = l;
      for (int i = c + 1; i < kk; ++i) {
        v8d x = (c == q) ? Mlab(i - 1) : bc(Ms[i - 1][c - 1]);
        for (int t = 0; t < c; ++t) {
          v8d lit = (t < q) ? bc(Ls[i - 1][t]) : L[i][t];
          v8d lct = (t < q && c != q) ? bc(Ls[c - 1][t]) : L[c][t];
          x = x - lit * lct;
        }
        L[i][c] = x / l;
      }
    }
    v8d acc = bc(which == 0 ? s.preH[q] : s.preA[q]);
    for (int a = q; a < kk; ++a) { v8d lg; for (int l = 0; l < 8; ++l) lg[l] = pm::log(L[a][a][l]); acc = acc + lg; }
    ld[which] = acc;
    if (which == 0) {   // forward solve L_H w = z_{S ∪ j}, rows from q on (core/cpp/v3_score.h:93, :216)
      quad = bc(s.preQ[q]);
      for (int i = q; i < kk; ++i) {
        v8d x = (i == q) ? zj : bc(s.zS[i - 1]);
        for (int t = 0; t < i; ++t) {
          v8d lit = (i == q) ? L[q][t] : ((t < q) ? bc(Ls[i - 1][t]) : L[i][t]);
          v8d wt = (t < q) ? bc(s.wH[t]) : w[t];
          x = x - lit * wt;
        }
        w[i] = x / L[i][i];
        quad = quad + w[i] * w[i];
      }
    }
  }
  v8d ldH = ld[0] * bc(2.0), ldA = ld[1] * bc(2.0);
  v8d Q = bc(D.yty) - bc((double)D.n) * quad;
  v8d arg = bc(2 * D.b0) + Q;
  v8d la; for (int l = 0; l < 8; ++l) la[l] = pm::log(arg[l]);
  logm = (bc(D.logCn) - bc(0.5) * (ldH - ldA)) - bc(D.nu) * la;
  ok &= lanemask((Q >= bc(1e-8 * D.yty)) & (arg > bc(0.0)) & (logm > bc(-__builtin_inf())) & (logm < bc(__builtin_inf())));
  return ok;
}

// --- Class A: bordered update, label appended last. ---
inline unsigned flip8_A(const Data& D, const SupportCache& s, const v8d* u, v8d gjj, v8d zj, v8d& logm) {
  const int k = s.k; const double n1 = D.n + 1.0;
  v8d* vH = lane_scratch(2, (size_t)std::max(1, k)).data(); v8d* vA = lane_scratch(3, (size_t)std::max(1, k)).data();
  v8d dH = fma8(bc(n1), gjj, bc(1.0)), dA = gjj + bc(1.0), wz = zj;
  for (int c = 0; c < k; ++c) {
    v8d x = bc(n1) * u[c], y = u[c];
    for (int t = 0; t < c; ++t) { x = fnma8(vH[t], bc(s.LH[c][t]), x); y = fnma8(vA[t], bc(s.LA[c][t]), y); }
    vH[c] = x * bc(s.rLH[c]); vA[c] = y * bc(s.rLA[c]);
    dH = fnma8(vH[c], vH[c], dH); dA = fnma8(vA[c], vA[c], dA); wz = fnma8(vH[c], bc(s.wH[c]), wz);
  }
  unsigned ok = pos_finite_mask(dH) & pos_finite_mask(dA);
  v8d quad = bc(s.preQ[k]) + (wz * wz) / dH;
  v8d Q = fnma8(bc((double)D.n), quad, bc(D.yty));
  v8d t1 = alog8(dH / dA), t2 = alog8(bc(2 * D.b0) + Q);
  logm = bc(D.logCn - (s.preH[k] - s.preA[k])) - fma8(bc(D.nu), t2, bc(0.5) * t1);
  ok &= lanemask((Q >= bc(1e-8 * D.yty)) & (logm > bc(-__builtin_inf())) & (logm < bc(__builtin_inf())));
  return ok;
}

// Odds for additions: lane l is label j8[l] ∉ S with logm8[l] = log m(S ∪ j). core/cpp/v3_engine.h:97, :124-126.
template <Arith A>
inline v8d odds_add8(const Data& D, const Start& st, const SupportCache& s, const int32_t* j8, v8d logm8) {
  v8d c;
  for (int l = 0; l < 8; ++l) c[l] = comp_add(st, s, j8[l]);
  v8d lg0 = bc(D.logprior[s.k + 1]) + c;
  v8d d = (logm8 - bc(D.logm0)) - c;
  v8d la = (lg0 + bc(s.phi) * d) - bc(s.lgphi);
  v8d o;
  if constexpr (A == Arith::Bit) {
    for (int l = 0; l < 8; ++l) o[l] = plogis_log(la[l]);
  } else {
    v8l pos = la >= bc(0.0);
    v8d e = aexp8(select8(pos, -la, la));
    o = select8(pos, bc(1.0) / (bc(1.0) + e), e / (bc(1.0) + e));
  }
  return o;
}

// Additions for 8 labels: fills logm_out / o_out for the lanes in `lanes` (all non-members; for Bit they share the
// insertion position q). u: Gram entries of the 8 labels with each member of S (lane-wise). Requires s.fast, s.add_ok.
template <Arith A>
inline void eval8_add(const Data& D, const Start& st, BitScorer& sc, const SupportCache& s, int q, const v8d* u,
                      const int32_t* j8, unsigned lanes, double* logm_out, double* o_out) {
  v8d gjj, zj;
  for (int l = 0; l < 8; ++l) { gjj[l] = D.diagG[j8[l]]; zj[l] = D.z[j8[l]]; }
  v8d lm;
  unsigned ok = (A == Arith::Bit) ? flip8_bit(D, s, q, u, gjj, zj, lm) : flip8_A(D, s, u, gjj, zj, lm);
  unsigned bad = lanes & ~ok, failed = 0;
  if (bad) {
    Model T;
    for (int l = 0; l < 8; ++l) if (bad & (1u << l)) {
      T = s.S; sorted_insert(T, j8[l]);
      try { lm[l] = sc.score(T).logm; } catch (const v4::NumericalFailure&) { lm[l] = std::numeric_limits<double>::quiet_NaN(); failed |= 1u << l; }
    }
  }
  v8d o = odds_add8<A>(D, st, s, j8, lm);
  for (int l = 0; l < 8; ++l) if (lanes & (1u << l)) { logm_out[l] = lm[l]; o_out[l] = (failed >> l) & 1u ? ODDS_FAILED : o[l]; }
}

// One label, any support (the particle-major reference and the slow path of the label-major kernel).
// Writes log m(S △ j) (NaN if the addition is infeasible) and o_j. Members: the cached deletion values.
template <Arith A>
inline void eval1(const Data& D, const Start& st, BitScorer& sc, const SupportCache& s, int j, double& logm_out, double& o_out) {
  auto it = std::lower_bound(s.S.begin(), s.S.end(), j);
  int q = (int)(it - s.S.begin());
  if (it != s.S.end() && *it == j) { logm_out = s.del_logm[q]; o_out = s.del_odds[q]; return; }
  if (!s.add_ok) { logm_out = std::numeric_limits<double>::quiet_NaN(); o_out = 0.0; return; }
  int32_t j8[8]; for (int l = 0; l < 8; ++l) j8[l] = j;
  double lm8[8], o8[8];
  if (s.fast) {
    thread_local std::vector<v8d> ub; if (ub.size() < (size_t)std::max(1, s.k)) ub.resize((size_t)std::max(1, s.k));
    v8d* u = ub.data();
    const double* xj = D.col(j);
    if (A == Arith::ClassA && products_fma()) {   // [arch] the same FMA sum as tile_products_fma4, one lane
      for (int a = 0; a < s.k; ++a) { const double* xa = D.col(s.S[a]); v8d g = bc(0); for (int i = 0; i < D.n; ++i) g = fma8(bc(xa[i]), bc(xj[i]), g); u[a] = g; }
    } else
    for (int a = 0; a < s.k; ++a) { const double* xa = D.col(s.S[a]); double g = 0; for (int i = 0; i < D.n; ++i) g += xa[i] * xj[i]; u[a] = bc(g); }
    eval8_add<A>(D, st, sc, s, q, u, j8, 1u, lm8, o8);
  } else {
    Model T = s.S; sorted_insert(T, j);
    double l1;
    try { l1 = sc.score(T).logm; }
    catch (const v4::NumericalFailure&) { logm_out = std::numeric_limits<double>::quiet_NaN(); o_out = ODDS_FAILED; return; }
    v8d lm = bc(l1);
    v8d o = odds_add8<A>(D, st, s, j8, lm);
    lm8[0] = lm[0]; o8[0] = o[0];
  }
  logm_out = lm8[0]; o_out = o8[0];
}

}  // namespace V4_ISLAND_ISA_NS
}  // namespace v4::island
