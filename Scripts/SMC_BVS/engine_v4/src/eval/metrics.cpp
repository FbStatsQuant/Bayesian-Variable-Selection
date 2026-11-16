// metrics.cpp -- selection (plan §3.1), PIP (§3.2), evidence/merge diagnostics (§3.4), store mass (§3.3 item 5).
#include <algorithm>
#include <cmath>

#include "v4/eval.h"

namespace v4::eval {

// Copied from core/cpp/v3_util.h:37-42 (splitmix64) and :99-108 (Zobrist keys from 0x5EEDB175C0DE2026).
static uint64_t splitmix64(uint64_t& x) {
  uint64_t z = (x += 0x9E3779B97F4A7C15ULL);
  z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
  z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
  return z ^ (z >> 31);
}
uint64_t zobrist_hash(const Model& S, int32_t p) {
  // keys are generated sequentially, so the key of j needs j + 1 splitmix steps; cache the key table per p
  static thread_local std::vector<uint64_t> key; static thread_local int32_t kp = -1;
  if (kp != p) { key.resize(p); uint64_t x = 0x5EEDB175C0DE2026ULL; for (int32_t j = 0; j < p; ++j) key[j] = splitmix64(x); kp = p; }
  uint64_t h = 0;
  for (int32_t j : S) { if (j < 0 || j >= p) throw Error(Status::invalid_input, "zobrist_hash: index out of range"); h ^= key[j]; }
  return h;
}

StoreMass store_mass(const StoreView& s, double rel_cut) {
  StoreMass m;
  if (s.size == 0) { m.vmax = m.logZ_T = -INFINITY; return m; }
  double vmax = -INFINITY;
  for (size_t i = 0; i < s.size; ++i) vmax = std::max(vmax, s.v[i]);
  const double lcut = std::log(rel_cut);
  // fixed chunks of 65,536 entries, long-double partials combined serially (order independent of threads)
  const size_t CH = 65536;
  long double tot = 0, drop = 0;   // the dropped mass is summed directly (tot − kept would cancel)
  for (size_t c0 = 0; c0 < s.size; c0 += CH) {
    long double pt = 0, pd = 0;
    const size_t c1 = std::min(s.size, c0 + CH);
    for (size_t i = c0; i < c1; ++i) {
      const double r = s.v[i] - vmax;
      const long double e = std::exp((long double)r);
      pt += e;
      if (r >= lcut) ++m.n_kept; else pd += e;
    }
    tot += pt; drop += pd;
  }
  m.vmax = vmax;
  m.logZ_T = vmax + (double)std::log(tot);
  m.dropped_mass = (double)(drop / tot);
  return m;
}

long store_find(const StoreView& s, const Model& S, uint64_t h) {
  for (size_t i = 0; i < s.size; ++i) {
    if (s.hash[i] != h || s.len[i] != S.size()) continue;
    if (std::equal(S.begin(), S.end(), s.pool + s.off[i])) return (long)i;
  }
  return -1;
}

static Json to_orig(const Model& S, const EvalData& D) {
  Json a = Json::array(); for (int32_t j : S) a.push(Json(D.orig[j])); return a;
}
static void set_cmp(const Model& S, const Model& S0, int& tp, int& fp, int& fn) {
  tp = 0; size_t i = 0, j = 0;
  while (i < S.size() && j < S0.size()) { if (S[i] == S0[j]) { ++tp; ++i; ++j; } else if (S[i] < S0[j]) ++i; else ++j; }
  fp = (int)S.size() - tp; fn = (int)S0.size() - tp;
}

Json selection_metrics(const Model& S0, const Model& hpm, double F_hpm, const Model& mpm, double F_S0, const EvalData& D) {
  Json J = Json::object();
  int tp, fp, fn;
  set_cmp(hpm, S0, tp, fp, fn);
  J.set("hpm", to_orig(hpm, D)); J.set("hpm_size", (int64_t)hpm.size());
  J.set("hpm_eq_S0", hpm == S0); J.set("hpm_hamming", fp + fn); J.set("hpm_tp", tp); J.set("hpm_fp", fp); J.set("hpm_fn", fn);
  set_cmp(mpm, S0, tp, fp, fn);
  J.set("mpm", to_orig(mpm, D)); J.set("mpm_size", (int64_t)mpm.size());
  J.set("mpm_eq_S0", mpm == S0); J.set("mpm_hamming", fp + fn); J.set("mpm_tp", tp); J.set("mpm_fp", fp); J.set("mpm_fn", fn);
  J.set("F_hpm", F_hpm); J.set("F_S0", F_S0); J.set("F_hpm_minus_F_S0", F_hpm - F_S0);
  // outcome class (P6): correct; posterior (F(HPM) > F(S0): the posterior prefers another model); search (F(S0) > F(HPM):
  // the sampler did not report the better S0); tie (equal F, different sets: resolved by the |S|/lex order)
  std::string oc = hpm == S0 ? "correct" : (F_hpm > F_S0 ? "posterior" : (F_S0 > F_hpm ? "search" : "tie"));
  J.set("outcome_class", oc);
  return J;
}

Json pip_metrics(const std::vector<double>& pip, const Model& S0, int32_t p) {
  Json J = Json::object();
  if ((int32_t)pip.size() != p) throw Error(Status::invalid_input, "pip_metrics: length != p");
  std::vector<char> tru(p, 0); for (int32_t j : S0) tru[j] = 1;
  double sup_null = -INFINITY, min_true = INFINITY, brier = 0; int32_t arg_sup = -1, arg_min = -1;
  int64_t n01 = 0, n05 = 0;
  const int NB = 20;
  std::vector<int64_t> bn(NB, 0), bt(NB, 0); std::vector<double> bs(NB, 0.0);
  long double br = 0;
  for (int32_t j = 0; j < p; ++j) {
    const double q = pip[j];
    if (!(q >= 0 && q <= 1)) throw Error(Status::invalid_input, "pip_metrics: PIP outside [0,1]");
    const double t = tru[j] ? 1.0 : 0.0;
    br += (long double)((q - t) * (q - t));
    if (tru[j]) { if (q < min_true) { min_true = q; arg_min = j; } }
    else { if (q > sup_null) { sup_null = q; arg_sup = j; } if (q > 0.1) ++n01; if (q > 0.5) ++n05; }
    int b = std::min(NB - 1, (int)std::floor(q * NB));
    bn[b]++; bt[b] += tru[j]; bs[b] += q;
  }
  brier = (double)(br / p);
  J.set("sup_null", S0.size() < (size_t)p ? sup_null : NAN); J.set("argsup_null", arg_sup);
  J.set("min_true", S0.empty() ? NAN : min_true); J.set("argmin_true", arg_min);
  J.set("brier", brier); J.set("n_null_gt_0.1", n01); J.set("n_null_gt_0.5", n05);
  Json rel = Json::array();   // reliability bins of width 0.05 (pooled across fits downstream)
  for (int b = 0; b < NB; ++b) {
    Json r = Json::object();
    r.set("lo", b * 0.05); r.set("hi", (b + 1) * 0.05); r.set("n", bn[b]); r.set("n_true", bt[b]);
    r.set("mean_pip", bn[b] ? bs[b] / bn[b] : NAN);
    rel.push(r);
  }
  J.set("reliability", rel);
  return J;
}

Json pip_island_spread(const double* pr, int32_t Rp, int32_t p, double sd_target) {
  Json J = Json::object();
  double max_sd = 0, max_rng = 0; int32_t arg = -1; int64_t n_over = 0;
  for (int32_t j = 0; j < p; ++j) {
    double m = 0, lo = INFINITY, hi = -INFINITY;
    for (int32_t r = 0; r < Rp; ++r) { double v = pr[(size_t)r * p + j]; m += v; lo = std::min(lo, v); hi = std::max(hi, v); }
    m /= Rp;
    double ss = 0; for (int32_t r = 0; r < Rp; ++r) { double d = pr[(size_t)r * p + j] - m; ss += d * d; }
    const double sd = Rp > 1 ? std::sqrt(ss / (Rp - 1)) : 0.0;
    if (sd > max_sd) { max_sd = sd; arg = j; }
    if (sd > sd_target) ++n_over;
    max_rng = std::max(max_rng, hi - lo);
  }
  J.set("Rp", Rp); J.set("max_sd", max_sd); J.set("argmax_sd", arg); J.set("max_range", max_rng);
  J.set("sd_target", sd_target); J.set("n_sd_over_target", n_over); J.set("target_met", n_over == 0);
  return J;
}

Json evidence_metrics(double logZ, const std::vector<double>& lr, double logZ_T) {
  Json J = Json::object();
  const size_t R = lr.size();
  J.set("logZ", logZ);
  J.set("logZ_r", Json::array_of(lr));
  J.set("logZ_lower95", std::log(0.05) + logZ);   // Markov bound, core/v3_run.R:155
  if (R) {
    double m = 0; for (double v : lr) m += v; m /= R;
    double ss = 0; for (double v : lr) ss += (v - m) * (v - m);
    std::vector<double> s = lr; std::sort(s.begin(), s.end());
    const double med = (R % 2) ? s[R / 2] : 0.5 * (s[R / 2 - 1] + s[R / 2]);
    std::vector<double> ad(R); for (size_t i = 0; i < R; ++i) ad[i] = std::fabs(lr[i] - med);
    std::sort(ad.begin(), ad.end());
    const double mad = (R % 2) ? ad[R / 2] : 0.5 * (ad[R / 2 - 1] + ad[R / 2]);
    const double mx = s.back();
    double w2 = 0, wmax = 0, sw = 0;
    for (double v : lr) sw += std::exp(v - mx);
    for (double v : lr) { double w = std::exp(v - mx) / sw; w2 += w * w; wmax = std::max(wmax, w); }
    J.set("sigma_hat", R > 1 ? std::sqrt(ss / (R - 1)) : NAN);
    J.set("sigma_hat_robust", 1.4826 * mad);
    J.set("max_minus_median", mx - med);
    J.set("R_eff", 1.0 / w2); J.set("R_eff_over_Rp", 1.0 / w2 / R); J.set("max_W", wmax);
    J.set("logZ_pooled_check", mx + std::log(sw) - std::log((double)R));   // = logZ if the merge pooled as v3_run.R:154
  }
  J.set("logZ_T", logZ_T);
  J.set("logZ_minus_logZ_T", logZ - logZ_T);
  return J;
}

double logZ_occ(const double* F, size_t M, uint64_t occ, uint64_t total) {
  if (M == 0 || occ == 0 || total == 0) return NAN;
  double mx = -INFINITY; for (size_t i = 0; i < M; ++i) mx = std::max(mx, F[i]);
  long double s = 0; for (size_t i = 0; i < M; ++i) s += std::exp((long double)(F[i] - mx));
  return mx + (double)std::log(s) - std::log((double)occ / (double)total);
}

}  // namespace v4::eval
