// block_stats.cpp -- API-RESID helper. For one block (columns Xb, n x m, standardised as in the engine) and responses
// Y (n x ny), return for every subset U of the block, indexed by code (bit i-1 <-> column i, the engine's table order):
//   ld[code]   = log det H_U - log det(G_U + I),  H_U = (n+1) G_U + I   (so D_U = exp(ld))
//   t[code, r] = n z_U' H_U^{-1} z_U with z = Xb' Y[, r]                 (so Q_U = y'y - t_U)
// These are exactly the quantities of the production scorer (v3_score.h finish_from_factors); the engine's log m(U) is
// logCn - ld/2 - nu log(2 b0 + y'y - t). Subsets are enumerated depth-first, extending both Cholesky factors by one row
// per added column (mathematically identical to the engine's full factorisation; rounding differs at ~1e-13).
#include <Rcpp.h>
#include <cmath>
#include <vector>
using namespace Rcpp;

// [[Rcpp::export]]
List block_stats_cpp(NumericMatrix G, NumericMatrix Z, int n) {
  int m = G.nrow(), ny = Z.ncol();
  uint32_t N = 1u << m;
  NumericVector ld(N, 0.0);
  NumericMatrix t(N, ny);
  std::vector<double> LH(m * m, 0.0), LA(m * m, 0.0), W(m * ny, 0.0);  // rows of the current path (depth-indexed)
  std::vector<int> idx(m, -1);
  std::vector<double> ldH(m + 1, 0.0), ldA(m + 1, 0.0), quad((m + 1) * ny, 0.0);
  double n1 = n + 1.0;
  // iterative DFS: stack of (depth k, next candidate column)
  std::vector<int> nextc(m + 1, 0);
  std::vector<uint32_t> code(m + 1, 0);
  int k = 0; nextc[0] = 0; code[0] = 0;
  while (k >= 0) {
    if (nextc[k] >= m) { --k; continue; }
    int c = nextc[k]++;
    // add column c at depth k (path idx[0..k-1])
    idx[k] = c;
    double sH = n1 * G(c, c) + 1.0, sA = G(c, c) + 1.0;
    for (int j = 0; j < k; ++j) {
      double hH = n1 * G(c, idx[j]), hA = G(c, idx[j]);
      for (int q = 0; q < j; ++q) { hH -= LH[k * m + q] * LH[j * m + q]; hA -= LA[k * m + q] * LA[j * m + q]; }
      LH[k * m + j] = hH / LH[j * m + j]; LA[k * m + j] = hA / LA[j * m + j];
      sH -= LH[k * m + j] * LH[k * m + j]; sA -= LA[k * m + j] * LA[k * m + j];
    }
    if (!(sH > 0) || !(sA > 0)) stop("non-positive pivot");
    LH[k * m + k] = std::sqrt(sH); LA[k * m + k] = std::sqrt(sA);
    ldH[k + 1] = ldH[k] + std::log(sH); ldA[k + 1] = ldA[k] + std::log(sA);
    uint32_t cd = code[k] | (1u << c);
    ld[cd] = ldH[k + 1] - ldA[k + 1];
    for (int r = 0; r < ny; ++r) {
      double w = Z(c, r);
      for (int q = 0; q < k; ++q) w -= LH[k * m + q] * W[q * ny + r];
      w /= LH[k * m + k];
      W[k * ny + r] = w;
      quad[(k + 1) * ny + r] = quad[k * ny + r] + w * w;
      t(cd, r) = n * quad[(k + 1) * ny + r];
    }
    // descend
    code[k + 1] = cd; nextc[k + 1] = c + 1; ++k;
  }
  return List::create(_["ld"] = ld, _["t"] = t);
}
