#include <Rcpp.h>
#include <cmath>
#include <algorithm>
#include <vector>
using namespace Rcpp;
static inline double lmin3(double a, double b, double c) {  // min eigenvalue of [[1,a,b],[a,1,c],[b,c,1]]
  double q = a*a + b*b + c*c, t = 2.0*a*b*c;
  if (q <= 0) return 1.0;
  double arg = (3.0*t/(2.0*q))*std::sqrt(3.0/q); if (arg > 1) arg = 1; if (arg < -1) arg = -1;
  double phi = std::acos(arg)/3.0, s = 2.0*std::sqrt(q/3.0), PI = 3.14159265358979323846, m = 1e300;
  for (int k = 0; k < 3; ++k) { double x = s*std::cos(phi - 2.0*PI*k/3.0); if (x < m) m = x; }
  return 1.0 + m;
}
// [[Rcpp::export]]
List triple_scan(NumericMatrix R, double tol) {
  int p = R.nrow(); double best = 1e300;
  for (int i = 0; i < p; ++i) for (int j = i+1; j < p; ++j) { double a = R(i,j);
    for (int k = j+1; k < p; ++k) { double v = lmin3(a, R(i,k), R(j,k)); if (v < best) best = v; } }
  std::vector<int> I, J, K; std::vector<double> V;
  for (int i = 0; i < p; ++i) for (int j = i+1; j < p; ++j) { double a = R(i,j);
    for (int k = j+1; k < p; ++k) { double v = lmin3(a, R(i,k), R(j,k)); if (v <= best + tol && I.size() < 2000) { I.push_back(i+1); J.push_back(j+1); K.push_back(k+1); V.push_back(v); } } }
  return List::create(_["best"] = best, _["i"] = I, _["j"] = J, _["k"] = K, _["v"] = V);
}
// Gershgorin-pruned exact scan: a triple with lambda_min <= ub has some vertex whose two edges satisfy |r1|+|r2| >= 1-ub,
// so it suffices to scan (v,u,w) with |r_vu|+|r_vw| >= thr = 1-ub (rigorous). maxvisit caps the work (returns aborted=TRUE).
// [[Rcpp::export]]
List triple_pruned(NumericMatrix R, double thr, double maxvisit) {
  int p = R.nrow(); double best = 1e300, visited = 0; bool aborted = false;
  std::vector<int> I, J, K; std::vector<double> V;
  std::vector<std::pair<double,int> > nb(p);
  for (int v = 0; v < p && !aborted; ++v) {
    int m = 0; for (int u = 0; u < p; ++u) if (u != v) nb[m++] = std::make_pair(-std::fabs(R(v,u)), u);
    std::sort(nb.begin(), nb.begin() + m);
    for (int a = 0; a < m && !aborted; ++a) { double ra = -nb[a].first; if (2.0*ra < thr) break;
      for (int b = a+1; b < m; ++b) { double rb = -nb[b].first; if (ra + rb < thr) break;
        visited += 1; if (visited > maxvisit) { aborted = true; break; }
        int u = nb[a].second, w = nb[b].second; double val = lmin3(R(v,u), R(v,w), R(u,w));
        if (val < best - 1e-6) { I.clear(); J.clear(); K.clear(); V.clear(); }
        if (val < best) best = val;
        if (val <= best + 1e-6 && I.size() < 2000) { I.push_back(v+1); J.push_back(u+1); K.push_back(w+1); V.push_back(val); } } } }
  return List::create(_["best"] = best, _["i"] = I, _["j"] = J, _["k"] = K, _["v"] = V, _["visited"] = visited, _["aborted"] = aborted);
}
