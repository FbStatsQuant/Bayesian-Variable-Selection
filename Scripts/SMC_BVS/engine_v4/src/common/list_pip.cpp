// list_pip.cpp -- see list_pip.h (SPEC_LIST_PIP.md).
#include "v4/list_pip.h"
#include <algorithm>
#include <cmath>
#include <limits>
#include <utility>
#include "v4/pmath.h"
#include "v4/status.h"

namespace v4 {

ListPipSrc list_pip_src(const Store& t) {
  ListPipSrc s; s.n = t.size(); s.v = t.v.data(); s.off = t.off.data(); s.len = t.len.data(); s.hash = t.hash.data(); s.pool = t.pool.data();
  return s;
}

namespace {
// The store is a set: no model twice. Entries are grouped by their stored hash (a model's hash is a function of the model),
// then compared model by model inside a group. 16 bytes per entry transient.
void require_distinct(const ListPipSrc& s) {
  const size_t m = s.n;
  if (m < 2) return;
  if (m > std::numeric_limits<uint32_t>::max()) throw Error(Status::internal_error, "list PIP: store larger than 2^32 entries");
  std::vector<std::pair<uint64_t, uint32_t>> kp(m);
  for (size_t i = 0; i < m; ++i) kp[i] = {s.hash[i], (uint32_t)i};
  std::sort(kp.begin(), kp.end(), [](const std::pair<uint64_t, uint32_t>& a, const std::pair<uint64_t, uint32_t>& b) { return a.first != b.first ? a.first < b.first : a.second < b.second; });
  auto same = [&](uint32_t a, uint32_t b) { return s.len[a] == s.len[b] && std::equal(s.pool + s.off[a], s.pool + s.off[a] + s.len[a], s.pool + s.off[b]); };
  for (size_t i = 0; i < m;) {
    size_t j = i + 1;
    while (j < m && kp[j].first == kp[i].first) ++j;
    for (size_t a = i; a < j; ++a) for (size_t b = a + 1; b < j; ++b)
      if (same(kp[a].second, kp[b].second)) throw Error(Status::internal_error, "list PIP: the top store holds a duplicate model");
    i = j;
  }
}
}  // namespace

ListPip compute_list_pip(const ListPipSrc& s, int32_t p, uint64_t capacity) {
  const double NaN = std::numeric_limits<double>::quiet_NaN();
  ListPip r; r.list_size = s.n; r.list_full = capacity > 0 && s.n >= capacity; r.source = "store";
  auto flagged = [&](const char* f) { r.flag = f; r.pip_list.assign((size_t)p, NaN); r.mpm_list.clear(); r.log_Z_list = NaN; return r; };
  if (s.n == 0) return flagged("empty_list");
  require_distinct(s);   // error precedence: a duplicate model is an error BEFORE any flag is set (a store is a set, whatever its scores are)
  double Fmax = -std::numeric_limits<double>::infinity();
  for (size_t i = 0; i < s.n; ++i) {
    if (std::isnan(s.v[i]) || s.v[i] == std::numeric_limits<double>::infinity()) return flagged("nonfinite_score");
    Fmax = std::max(Fmax, s.v[i]);
  }
  if (Fmax == -std::numeric_limits<double>::infinity()) return flagged("nonfinite_score");   // all -Inf: normaliser 0 (Theory-confirmed via HQ 11-17)
  std::vector<double> num((size_t)p, 0.0);
  double den = 0.0;
  for (size_t i = s.n; i-- > 0;) {   // last entry first (smallest weights first)
    const double u = pm::exp(s.v[i] - Fmax);
    den += u;
    const int32_t* q = s.pool + s.off[i];
    for (uint16_t k = 0; k < s.len[i]; ++k) {
      if (q[k] < 0 || q[k] >= p) throw Error(Status::internal_error, "list PIP: a stored model has a column outside [0, p)");
      num[(size_t)q[k]] += u;
    }
  }
  r.pip_list.resize((size_t)p);
  for (int32_t j = 0; j < p; ++j) { r.pip_list[(size_t)j] = num[(size_t)j] / den; if (r.pip_list[(size_t)j] > 0.5) r.mpm_list.push_back(j); }
  r.log_Z_list = Fmax + pm::log(den);
  return r;
}

ListPip compute_list_pip(const Store& top, int32_t p) {
  if (top.staging() != 0) throw Error(Status::internal_error, "list PIP: the store is not compacted");
  return compute_list_pip(list_pip_src(top), p, top.cap);
}

}  // namespace v4
