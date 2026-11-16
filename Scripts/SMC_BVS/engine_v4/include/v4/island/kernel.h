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
#pragma once
#include "v4/island/amath.h"
#include "v4/island/dep.h"

namespace v4::island {
using namespace v4::island::dep;
inline namespace V4_ISLAND_ISA_NS {

enum class Arith { Bit, ClassA };
constexpr int KM = 24;  // largest support handled by the vector paths; larger supports take the scalar path

struct SupportCache {
  Model S; int k = 0; uint64_t h = 0;
  double logm = 0, lg0 = 0, d = 0, phi = 0, lgphi = 0;  // the particle's path values at this state
  bool fast = false;    // vector path usable (k <= KM and both Cholesky factors of S exist)
  bool add_ok = false;  // k < K (core/cpp/v3_engine.h:116)
  alignas(64) double MH[KM][KM], MA[KM][KM], LH[KM][KM], LA[KM][KM];
  double zS[KM], wH[KM], rLH[KM], rLA[KM], preH[KM + 1], preA[KM + 1], preQ[KM + 1];
  // composite sum of S by blocks in increasing block order (core/cpp/v3_start.h:54-66)
  std::vector<int> bb; std::vector<uint32_t> bcode; std::vector<double> bterm, bpre;
  // deletions S \ S[a]
  std::vector<double> del_logm, del_odds;
  std::vector<int> arow;  // row of each member in the pass's active-column product matrix (label-major only)
};

// Composite sum of S ∪ {j} (j ∉ S) and S \ {j} (j ∈ S), same additions in the same order as Start::comp.
inline double comp_add(const Start& st, const SupportCache& s, int j) {
  int b = st.blk[j]; uint32_t bit = 1u << st.pos[j];
  size_t m = std::lower_bound(s.bb.begin(), s.bb.end(), b) - s.bb.begin();
  double c = s.bpre[m];
  if (m < s.bb.size() && s.bb[m] == b) { c += st.logr[b][s.bcode[m] | bit]; ++m; }
  else c += st.logr[b][bit];
  for (; m < s.bb.size(); ++m) c += s.bterm[m];
  return c;
}
inline double comp_del(const Start& st, const SupportCache& s, int j) {
  int b = st.blk[j]; uint32_t bit = 1u << st.pos[j];
  size_t m = std::lower_bound(s.bb.begin(), s.bb.end(), b) - s.bb.begin();
  double c = s.bpre[m];
  uint32_t nc = s.bcode[m] & ~bit;
  if (nc) c += st.logr[b][nc];
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
  if (k <= KM) {
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
    double lm = sc.score(Sd).logm;   // WP1's Gram-free Bit scorer: the bits of core's score(S \ S[a])
    double c = comp_del(st, s, S[a]);
    double lg0d = D.logprior[k - 1] + c, dd = (lm - D.logm0) - c;
    s.del_logm[a] = lm;
    s.del_odds[a] = plogis_log(s.lgphi - (lg0d + phi * dd));
  }
}

// --- Bit form: 8 labels sharing the sorted insertion position q. Returns the mask of lanes with a valid result. ---
inline unsigned flip8_bit(const Data& D, const SupportCache& s, int q, const v8d* u, v8d gjj, v8d zj, v8d& logm) {
  const int k = s.k, kk = k + 1; const double n1 = D.n + 1.0;
  v8d L[KM + 1][KM + 1]; v8d ld[2]; v8d w[KM + 1]; v8d quad = bc(0.0);
  unsigned ok = 0xFFu;
  for (int which = 0; which < 2; ++which) {
    const double (*Ls)[KM] = which == 0 ? s.LH : s.LA;
    const double (*Ms)[KM] = which == 0 ? s.MH : s.MA;
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
  for (int l = 0; l < 8; ++l)
    if (!(Q[l] >= 1e-8 * D.yty) || !(arg[l] > 0) || !std::isfinite(logm[l])) ok &= ~(1u << l);
  return ok;
}

// --- Class A: bordered update, label appended last. ---
inline unsigned flip8_A(const Data& D, const SupportCache& s, const v8d* u, v8d gjj, v8d zj, v8d& logm) {
  const int k = s.k; const double n1 = D.n + 1.0;
  v8d vH[KM], vA[KM];
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
  for (int l = 0; l < 8; ++l)
    if (!(Q[l] >= 1e-8 * D.yty) || !std::isfinite(logm[l])) ok &= ~(1u << l);
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
  unsigned bad = lanes & ~ok;
  if (bad) {
    Model T;
    for (int l = 0; l < 8; ++l) if (bad & (1u << l)) { T = s.S; sorted_insert(T, j8[l]); lm[l] = sc.score(T).logm; }
  }
  v8d o = odds_add8<A>(D, st, s, j8, lm);
  for (int l = 0; l < 8; ++l) if (lanes & (1u << l)) { logm_out[l] = lm[l]; o_out[l] = o[l]; }
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
    v8d u[KM];
    const double* xj = D.col(j);
    for (int a = 0; a < s.k; ++a) { const double* xa = D.col(s.S[a]); double g = 0; for (int i = 0; i < D.n; ++i) g += xa[i] * xj[i]; u[a] = bc(g); }
    eval8_add<A>(D, st, sc, s, q, u, j8, 1u, lm8, o8);
  } else {
    Model T = s.S; sorted_insert(T, j);
    v8d lm = bc(sc.score(T).logm);
    v8d o = odds_add8<A>(D, st, s, j8, lm);
    lm8[0] = lm[0]; o8[0] = o[0];
  }
  logm_out = lm8[0]; o_out = o8[0];
}

}  // namespace V4_ISLAND_ISA_NS
}  // namespace v4::island
