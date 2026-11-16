// metrics.cpp -- selection (plan §3.1), PIP (§3.2), evidence/merge diagnostics (§3.4), store mass (§3.3 item 5).
#include <algorithm>
#include <cmath>

#include "v4/eval.h"

namespace v4::eval {

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

static Json to_orig(const Model& S, const Data& D) {
  Json a = Json::array(); for (int32_t j : S) a.push(Json(D.orig[j])); return a;
}
static void set_cmp(const Model& S, const Model& S0, int& tp, int& fp, int& fn) {
  tp = 0; size_t i = 0, j = 0;
  while (i < S.size() && j < S0.size()) { if (S[i] == S0[j]) { ++tp; ++i; ++j; } else if (S[i] < S0[j]) ++i; else ++j; }
  fp = (int)S.size() - tp; fn = (int)S0.size() - tp;
}

Json selection_metrics(const Model& S0, const Model& hpm, double F_hpm, const Model& mpm, double F_S0, const Data& D) {
  Json J = Json::object();
  int tp, fp, fn;
  set_cmp(hpm, S0, tp, fp, fn);
  J["hpm"] = (to_orig(hpm, D)); J["hpm_size"] = ((int64_t)hpm.size());
  J["hpm_eq_S0"] = (hpm == S0); J["hpm_hamming"] = (fp + fn); J["hpm_tp"] = (tp); J["hpm_fp"] = (fp); J["hpm_fn"] = (fn);
  set_cmp(mpm, S0, tp, fp, fn);
  J["mpm"] = (to_orig(mpm, D)); J["mpm_size"] = ((int64_t)mpm.size());
  J["mpm_eq_S0"] = (mpm == S0); J["mpm_hamming"] = (fp + fn); J["mpm_tp"] = (tp); J["mpm_fp"] = (fp); J["mpm_fn"] = (fn);
  J["F_hpm"] = (F_hpm); J["F_S0"] = (F_S0); J["F_hpm_minus_F_S0"] = (F_hpm - F_S0);
  // outcome class (P6): correct; posterior (F(HPM) > F(S0): the posterior prefers another model); search (F(S0) > F(HPM):
  // the sampler did not report the better S0); tie (equal F, different sets: resolved by the |S|/lex order)
  std::string oc = hpm == S0 ? "correct" : (F_hpm > F_S0 ? "posterior" : (F_S0 > F_hpm ? "search" : "tie"));
  J["outcome_class"] = (oc);
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
    const double q0 = pip[j];   // rounding margin 1e-12 (sums of normalised weights), clamped; beyond it: invalid
    if (!(q0 >= -1e-12 && q0 <= 1 + 1e-12)) throw Error(Status::invalid_input, "pip_metrics: PIP outside [0,1]");
    const double q = std::min(1.0, std::max(0.0, q0));
    const double t = tru[j] ? 1.0 : 0.0;
    br += (long double)((q - t) * (q - t));
    if (tru[j]) { if (q < min_true) { min_true = q; arg_min = j; } }
    else { if (q > sup_null) { sup_null = q; arg_sup = j; } if (q > 0.1) ++n01; if (q > 0.5) ++n05; }
    int b = std::min(NB - 1, (int)std::floor(q * NB));
    bn[b]++; bt[b] += tru[j]; bs[b] += q;
  }
  brier = (double)(br / p);
  J["sup_null"] = S0.size() < (size_t)p ? Json(sup_null) : Json(); J["argsup_null"] = (arg_sup);   // null: no null column
  J["min_true"] = S0.empty() ? Json() : Json(min_true); J["argmin_true"] = (arg_min);   // null: S0 empty
  J["brier"] = (brier); J["n_null_gt_0.1"] = (n01); J["n_null_gt_0.5"] = (n05);
  Json rel = Json::array();   // reliability bins of width 0.05 (pooled across fits downstream)
  for (int b = 0; b < NB; ++b) {
    Json r = Json::object();
    r["lo"] = (b * 0.05); r["hi"] = ((b + 1) * 0.05); r["n"] = (bn[b]); r["n_true"] = (bt[b]);
    r["mean_pip"] = (bn[b] ? bs[b] / bn[b] : NAN);
    rel.push(r);
  }
  J["reliability"] = (rel);
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
  J["Rp"] = (Rp); J["max_sd"] = (max_sd); J["argmax_sd"] = (arg); J["max_range"] = (max_rng);
  J["sd_target"] = (sd_target); J["n_sd_over_target"] = (n_over); J["target_met"] = (n_over == 0);
  return J;
}

Json evidence_metrics(double logZ, const std::vector<double>& lr, double logZ_T) {
  Json J = Json::object();
  const size_t R = lr.size();
  J["logZ"] = (logZ);
  J["logZ_r"] = (Json::array_of(lr));
  J["logZ_lower95"] = (std::log(0.05) + logZ);   // Markov bound, core/v3_run.R:155
  J["logZ_lower95_note"] = "Markov lower confidence bound log(0.05 Zhat); gives no upper bound on Z (Sol F9)";
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
    J["sigma_hat"] = (R > 1 ? std::sqrt(ss / (R - 1)) : NAN);
    J["sigma_hat_robust"] = (1.4826 * mad);
    J["max_minus_median"] = (mx - med);
    J["R_eff"] = (1.0 / w2); J["R_eff_over_Rp"] = (1.0 / w2 / R); J["max_W"] = (wmax);
    J["logZ_pooled_check"] = (mx + std::log(sw) - std::log((double)R));   // = logZ if the merge pooled as v3_run.R:154
  }
  J["logZ_T"] = (logZ_T);
  J["logZ_minus_logZ_T"] = (logZ - logZ_T);
  J["logZ_T_note"] = "log Z_T = log sum_store e^F is a deterministic lower bound on log Z (the only one); logZ_minus_logZ_T compares it with the noisy estimate";
  return J;
}

double logZ_occ(const double* F, size_t M, uint64_t occ, uint64_t total) {
  if (M == 0 || occ == 0 || total == 0) return NAN;
  double mx = -INFINITY; for (size_t i = 0; i < M; ++i) mx = std::max(mx, F[i]);
  long double s = 0; for (size_t i = 0; i < M; ++i) s += std::exp((long double)(F[i] - mx));
  return mx + (double)std::log(s) - std::log((double)occ / (double)total);
}

}  // namespace v4::eval
