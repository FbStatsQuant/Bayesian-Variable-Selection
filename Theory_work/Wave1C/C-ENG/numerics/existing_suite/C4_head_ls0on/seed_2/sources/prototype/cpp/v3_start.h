// v3_start.h -- block tables, composite start pi_0, exact normaliser, exact iid sampler, start mode, discrepancy.
// CORE_SPEC v2 §3; M §6.3. Ruling R2 (tables scored, not cached).
#pragma once
#include "v3_blocks.h"

namespace v3 {

// Variate source interface (CORE_SPEC §4.1). Every uniform the algorithm consumes is requested through it with a
// purpose string, so a trace can record it and a prescribed list can replace it.
struct VariateSource {
  virtual double u(const char* purpose) = 0;
  virtual ~VariateSource() {}
};

// Categorical draw used by the pi_0 sampler: smallest index k with cumulative C_k > u (u in [0,1)).
// The cumulative vector is normalised and set to exactly 1 from the last positive-mass category on, so a
// zero-mass category is never returned (documented convention; resampling uses the spec's ">=" rule instead).
inline int cat_draw_gt(const std::vector<double>& cum, double u) {
  return (int)(std::upper_bound(cum.begin(), cum.end(), u) - cum.begin());
}
inline std::vector<double> cumulative_from_logs(const std::vector<double>& lp) {
  // probabilities proportional to exp(lp); computed relative to the maximum (log-sum-exp normalisation)
  double m = NEG_INF; for (double v : lp) m = std::max(m, v);
  std::vector<double> c(lp.size(), 0.0);
  if (m == NEG_INF) return c;
  long double s = 0; std::vector<long double> e(lp.size());
  for (size_t i = 0; i < lp.size(); ++i) { e[i] = (lp[i] == NEG_INF) ? 0.0L : std::exp((long double)(lp[i] - m)); s += e[i]; }
  long double acc = 0; int last = -1;
  for (size_t i = 0; i < lp.size(); ++i) { acc += e[i]; c[i] = (double)(acc / s); if (e[i] > 0) last = (int)i; }
  for (size_t i = (size_t)last; i < lp.size(); ++i) c[i] = 1.0;
  return c;
}

struct Start {
  const Data* D = nullptr;
  int J = 0, B = 0;
  std::vector<std::vector<int>> blocks;      // internal indices, sorted, packing order
  std::vector<int> blk, pos;                 // block and position of each internal column
  std::vector<std::vector<double>> logr;     // logr[b][code] = log m(U) - log m(empty); NaN if |U| > K (not scored)
  std::vector<std::vector<double>> logm_tab; // log m(U) of each table entry (for HPM ingestion)
  std::vector<std::vector<int>> route_tab;
  std::vector<std::vector<double>> logprof;  // log e_b(j), j = 0..min(|C_b|, K)
  std::vector<std::vector<double>> logF;     // log F_b(k), b = 0..J, k = 0..K (partial convolutions)
  double logZbar0 = 0;
  std::vector<double> size_logmass;          // log pi_0(|S| = k)
  // sampler tables
  std::vector<double> size_cum;                               // over k = 0..K
  std::vector<std::vector<std::vector<double>>> cond_cum;     // cond_cum[b][r] over j = 0..min(m_b, r)
  std::vector<std::vector<std::vector<int>>> codes_by_size;   // codes_by_size[b][j] (increasing code order)
  std::vector<std::vector<std::vector<double>>> sub_cum;      // sub_cum[b][j] over codes_by_size[b][j]

  // composite sum  sum_b log r_b(S n C_b), summed over blocks met by S in increasing block order (blocks with an
  // empty intersection contribute log r_b(empty) = 0 exactly and are skipped; identical bits to the full sum).
  double comp(const std::vector<int>& S, std::vector<std::pair<int,int>>& scratch) const {
    scratch.clear();
    for (int j : S) scratch.push_back({blk[j], pos[j]});
    std::sort(scratch.begin(), scratch.end());
    double s = 0;
    size_t i = 0;
    while (i < scratch.size()) {
      int b = scratch[i].first; uint32_t code = 0;
      while (i < scratch.size() && scratch[i].first == b) { code |= (1u << scratch[i].second); ++i; }
      s += logr[b][code];
    }
    return s;
  }
  double comp(const std::vector<int>& S) const { std::vector<std::pair<int,int>> sc; return comp(S, sc); }
  // log gamma_0(S) = log varpi(|S|) + sum_b log r_b(S n C_b)  (M §6.3)
  double log_gamma0(const std::vector<int>& S) const { return D->logprior[S.size()] + comp(S); }
  double log_pi0(const std::vector<int>& S) const { return log_gamma0(S) - logZbar0; }
};

// Tables (M §6.3): every sub-model U of every block scored against the full y; log r_b(U) = log m(U) - log m(empty).
// Sub-models with |U| > K exist only under a B_override larger than K; they never enter pi_0 (the size prior is
// capped) and are not scored (entry NaN).
inline void build_tables(Start& st, Scorer& sc) {
  const Data& D = *st.D;
  st.J = (int)st.blocks.size();
  st.blk.assign(D.p, -1); st.pos.assign(D.p, -1);
  for (int b = 0; b < st.J; ++b) for (size_t i = 0; i < st.blocks[b].size(); ++i) { st.blk[st.blocks[b][i]] = b; st.pos[st.blocks[b][i]] = (int)i; }
  st.logr.assign(st.J, {}); st.logm_tab.assign(st.J, {}); st.route_tab.assign(st.J, {});
  std::vector<int> U;
  for (int b = 0; b < st.J; ++b) {
    int m = (int)st.blocks[b].size();
    uint32_t ncode = 1u << m;
    st.logr[b].assign(ncode, std::numeric_limits<double>::quiet_NaN());
    st.logm_tab[b].assign(ncode, std::numeric_limits<double>::quiet_NaN());
    st.route_tab[b].assign(ncode, -1);
    for (uint32_t code = 0; code < ncode; ++code) {
      U.clear();
      for (int i = 0; i < m; ++i) if (code & (1u << i)) U.push_back(st.blocks[b][i]);
      if ((int)U.size() > D.K) continue;
      ScoreOut o = sc.score(U);
      st.logm_tab[b][code] = o.logm; st.route_tab[b][code] = o.route;
      st.logr[b][code] = (code == 0) ? 0.0 : o.logm - D.logm0;
    }
  }
}

// Size profiles, partial convolutions up to K, exact normaliser and sampler tables (M §6.3).
inline void build_start(Start& st) {
  const Data& D = *st.D;
  int K = D.K, J = st.J;
  st.logprof.assign(J, {});
  st.codes_by_size.assign(J, {}); st.sub_cum.assign(J, {});
  for (int b = 0; b < J; ++b) {
    int m = (int)st.blocks[b].size(), top = std::min(m, K);
    st.codes_by_size[b].assign(top + 1, {});
    for (uint32_t code = 0; code < (1u << m); ++code) {
      int j = __builtin_popcount(code);
      if (j <= top) st.codes_by_size[b][j].push_back(code);
    }
    st.logprof[b].assign(top + 1, NEG_INF);
    st.sub_cum[b].assign(top + 1, {});
    for (int j = 0; j <= top; ++j) {
      std::vector<double> lv; for (uint32_t c : st.codes_by_size[b][j]) lv.push_back(st.logr[b][c]);
      st.logprof[b][j] = log_sum_exp(lv);          // log e_b(j) = log sum_{|U|=j} r_b(U)
      st.sub_cum[b][j] = cumulative_from_logs(lv);  // within-size law r_b(U)/e_b(j), increasing code order
    }
  }
  // log F_b(k) = log sum_j e_b(j) F_{b-1}(k-j), truncated at K (log-space convolution)
  st.logF.assign(J + 1, std::vector<double>(K + 1, NEG_INF));
  st.logF[0][0] = 0.0;
  for (int b = 1; b <= J; ++b) {
    const auto& pr = st.logprof[b - 1];
    for (int k = 0; k <= K; ++k) {
      std::vector<double> t;
      for (int j = 0; j < (int)pr.size() && j <= k; ++j) if (st.logF[b - 1][k - j] != NEG_INF) t.push_back(pr[j] + st.logF[b - 1][k - j]);
      st.logF[b][k] = t.empty() ? NEG_INF : log_sum_exp(t);
    }
  }
  // log Zbar_0 = log sum_k varpi(k) F_J(k)
  std::vector<double> lk(K + 1);
  for (int k = 0; k <= K; ++k) lk[k] = (st.logF[J][k] == NEG_INF) ? NEG_INF : D.logprior[k] + st.logF[J][k];
  st.logZbar0 = log_sum_exp(lk);
  st.size_logmass.assign(K + 1, NEG_INF);
  for (int k = 0; k <= K; ++k) st.size_logmass[k] = lk[k] - st.logZbar0;
  st.size_cum = cumulative_from_logs(lk);
  // backward conditional of block b's size given the remaining total r: P(k_b = j | r) = e_b(j) F_{b-1}(r-j)/F_b(r)
  st.cond_cum.assign(J, {});
  for (int b = 0; b < J; ++b) {
    st.cond_cum[b].assign(K + 1, {});
    const auto& pr = st.logprof[b];
    for (int r = 0; r <= K; ++r) {
      std::vector<double> lj;
      for (int j = 0; j < (int)pr.size() && j <= r; ++j)
        lj.push_back(st.logF[b][r - j] == NEG_INF ? NEG_INF : pr[j] + st.logF[b][r - j]);  // logF index b == block b-1 prefix
      st.cond_cum[b][r] = cumulative_from_logs(lj);
    }
  }
}

// Exact iid draw from pi_0 (M §6.3; CORE_SPEC §4.1). Variate order (documented):
//   1 uniform for the total size k (categorical over 0..K);
//   then for b = J..1 while the remaining size r > 0: 1 uniform for k_b (categorical over j = 0..min(|C_b|, r));
//   then for b = 1..J with k_b > 0: 1 uniform for the sub-model (categorical over size-k_b subsets, increasing code).
// Categoricals use the "smallest k with cumulative > u" rule (cat_draw_gt).
inline void draw_pi0(const Start& st, VariateSource& vs, std::vector<int>& S, std::vector<int>* sizes_out = nullptr) {
  int J = st.J;
  int k = cat_draw_gt(st.size_cum, vs.u("pi0_size"));
  std::vector<int> kb(J, 0);
  int r = k;
  for (int b = J - 1; b >= 0 && r > 0; --b) {
    int j = cat_draw_gt(st.cond_cum[b][r], vs.u("pi0_block_size"));
    kb[b] = j; r -= j;
  }
  S.clear();
  for (int b = 0; b < J; ++b) {
    if (kb[b] == 0) continue;
    int i = cat_draw_gt(st.sub_cum[b][kb[b]], vs.u("pi0_submodel"));
    uint32_t code = st.codes_by_size[b][kb[b]][i];
    for (size_t t = 0; t < st.blocks[b].size(); ++t) if (code & (1u << t)) S.push_back(st.blocks[b][t]);
  }
  std::sort(S.begin(), S.end());
  if (sizes_out) *sizes_out = kb;
}

// Start mode S~_0 = argmax pi_0 (M §6.3; CORE_SPEC §3): max-plus convolution of per-block per-size maxima, summed
// in block order exactly as Start::comp sums, so DP values equal the direct log gamma_0 bits. Ties: smallest size,
// then the lexicographically smallest index set among all sets whose per-block choices attain the DP maxima
// exactly (enumerated; capped at `cap` sets, flag returned).
struct ModeResult { std::vector<int> S; double lg0 = NEG_INF; long ties = 0; bool truncated = false; };
inline ModeResult start_mode(const Start& st, long cap = 1000000) {
  const Data& D = *st.D;
  int J = st.J, K = D.K;
  std::vector<std::vector<double>> mb(J);
  std::vector<std::vector<std::vector<uint32_t>>> arg(J);
  for (int b = 0; b < J; ++b) {
    int top = (int)st.logprof[b].size() - 1;
    mb[b].assign(top + 1, NEG_INF); arg[b].assign(top + 1, {});
    for (int j = 0; j <= top; ++j)
      for (uint32_t c : st.codes_by_size[b][j]) {
        double v = st.logr[b][c];
        if (v > mb[b][j]) { mb[b][j] = v; arg[b][j].assign(1, c); }
        else if (v == mb[b][j]) arg[b][j].push_back(c);
      }
  }
  std::vector<std::vector<double>> M(J + 1, std::vector<double>(K + 1, NEG_INF));
  M[0][0] = 0.0;
  for (int b = 1; b <= J; ++b)
    for (int k = 0; k <= K; ++k)
      for (int j = 0; j < (int)mb[b - 1].size() && j <= k; ++j) {
        if (M[b - 1][k - j] == NEG_INF) continue;
        double v = (j == 0) ? M[b - 1][k - j] : M[b - 1][k - j] + mb[b - 1][j];  // empty block adds exact 0
        if (v > M[b][k]) M[b][k] = v;
      }
  int kbest = -1; double vbest = NEG_INF;
  for (int k = 0; k <= K; ++k) {
    if (M[J][k] == NEG_INF) continue;
    double v = D.logprior[k] + M[J][k];
    if (v > vbest) { vbest = v; kbest = k; }  // strict: ties keep the smaller size
  }
  ModeResult res; res.lg0 = vbest;
  // enumerate all optimal choices backward; keep lexicographically smallest set
  std::vector<uint32_t> choice(J, 0);
  bool have = false; std::vector<int> bestS; long count = 0; bool trunc = false;
  std::function<void(int, int)> rec = [&](int b, int r) {
    if (trunc) return;
    if (b == 0) {
      if (r != 0) return;
      std::vector<int> S;
      for (int bb = 0; bb < J; ++bb) for (size_t t = 0; t < st.blocks[bb].size(); ++t) if (choice[bb] & (1u << t)) S.push_back(st.blocks[bb][t]);
      std::sort(S.begin(), S.end());
      ++count;
      if (!have || lex_less(S, bestS)) { bestS = S; have = true; }
      if (count >= cap) trunc = true;
      return;
    }
    for (int j = 0; j < (int)mb[b - 1].size() && j <= r; ++j) {
      if (M[b - 1][r - j] == NEG_INF) continue;
      double v = (j == 0) ? M[b - 1][r - j] : M[b - 1][r - j] + mb[b - 1][j];
      if (v != M[b][r]) continue;
      for (uint32_t c : arg[b - 1][j]) { choice[b - 1] = c; rec(b - 1, r - j); if (trunc) return; }
      choice[b - 1] = 0;
    }
  };
  rec(J, kbest);
  res.S = bestS; res.ties = count; res.truncated = trunc;
  return res;
}

}  // namespace v3
