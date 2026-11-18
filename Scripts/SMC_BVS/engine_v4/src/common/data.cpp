// data.cpp -- Data construction: z, diag(G), y'y and the constants of the target (core/cpp/v3_score.h:39-72, Gram-free).
#include "v4/data.h"
#include <cmath>
#include <stdexcept>
#include "v4/status.h"

namespace v4 {

void data_constants(Data& D) {
  // core/cpp/v3_score.h:40, :57-71, copied (K, nu, log C_n, log m0, log w(k), log W_K, log varpi(k), Zobrist).
  const int n = D.n, p = D.p;
  D.K = std::min(p, n / 2);
  D.nu = D.a0 + n / 2.0;
  D.logCn = D.a0 * pm::log(2 * D.b0) + pm::lgamma(D.a0 + n / 2.0) - (n / 2.0) * pm::log(M_PI) - pm::lgamma(D.a0);
  D.logm0 = D.logCn - D.nu * pm::log(2 * D.b0 + D.yty);
  D.logw.assign(D.K + 1, 0.0);
  std::vector<double> terms(D.K + 1);
  for (int k = 0; k <= D.K; ++k) {
    D.logw[k] = -M_LN2 - lchoose_d(2.0 * p - 1.0, k);
    terms[k] = lchoose_d((double)p, k) + D.logw[k];
  }
  D.logWK = log_sum_exp(terms);
  D.logprior.assign(D.K + 1, 0.0);
  for (int k = 0; k <= D.K; ++k) D.logprior[k] = D.logw[k] - D.logWK;
  D.zob.init(p);
}

Data make_data(std::shared_ptr<DataOwned> own, int32_t n, int32_t p) {
  if (n < 1 || p < 1) throw Error(Status::invalid_input, "make_data: n and p must be positive");
  if (own->X.size() != (size_t)n * (size_t)p || own->y.size() != (size_t)n) throw Error(Status::invalid_input, "make_data: X/y size mismatch");
  Data D;
  D.n = n; D.p = p; if (D.p_raw == 0) D.p_raw = p;
  D.Xs = own->X.data(); D.ys = own->y.data();
  // core/cpp/v3_score.h:44-53: diag(G) entries (a = b) of the sequential Gram sum.
  own->diagG.assign((size_t)p, 0.0);
  for (int a = 0; a < p; ++a) own->diagG[a] = gram(D, a, a);
  // core/cpp/v3_score.h:54-56: z = X^T y, y'y (sequential sums).
  own->z.assign((size_t)p, 0.0);
  for (int a = 0; a < p; ++a) { const double* xa = D.col(a); double s = 0; for (int i = 0; i < n; ++i) s += xa[i] * D.ys[i]; own->z[a] = s; }
  D.yty = 0; for (int i = 0; i < n; ++i) D.yty += D.ys[i] * D.ys[i];
  if (own->orig.empty()) { own->orig.resize((size_t)p); for (int j = 0; j < p; ++j) own->orig[j] = j + 1; }
  if (own->orig.size() != (size_t)p) throw Error(Status::invalid_input, "make_data: orig size mismatch");
  D.z = own->z.data(); D.diagG = own->diagG.data(); D.orig = own->orig.data();
  if (own->col_max.size() == (size_t)p) { D.col_max = own->col_max.data(); D.col_mean = own->col_mean.data(); D.col_sd = own->col_sd.data(); }
  data_constants(D);
  D.keep = own;
  return D;
}

}  // namespace v4
