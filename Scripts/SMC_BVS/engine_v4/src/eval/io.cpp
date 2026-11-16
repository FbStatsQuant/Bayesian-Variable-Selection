// io.cpp -- WP5 readers (see io.h).
#include "io.h"

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <utility>
#include <vector>

namespace v4::eval::io {

void load_fit(const std::string& path, FitFile& o) {
  o.bin = std::make_shared<fmt::Reader>(path);
  const fmt::Reader& B = *o.bin;
  if (B.kind() != fmt::K_FIT) throw Error(Status::invalid_input, path + ": not a fit.bin (kind != 6)");
  o.meta = B.has("meta") ? B.json("meta") : Json::object();
  uint64_t n = 0, c = 0;
  StoreView& s = o.top;
  s.v = B.get<double>("top_v", &n); s.size = n;
  s.off = B.get<uint64_t>("top_off", &c); if (c != n) throw Error(Status::invalid_input, "fit.bin: top_off size");
  s.len = B.get<uint16_t>("top_len", &c); if (c != n) throw Error(Status::invalid_input, "fit.bin: top_len size");
  s.hash = B.get<uint64_t>("top_hash", &c); if (c != n) throw Error(Status::invalid_input, "fit.bin: top_hash size");
  s.pool = B.get<int32_t>("top_pool", &c);
  for (size_t i = 0; i < n; ++i)   // overflow-safe (PR45 review INFO-1): no off + len wrap-around
    if (s.len[i] > c || s.off[i] > c - s.len[i]) throw Error(Status::invalid_input, "fit.bin: store entry beyond pool");
  for (size_t i = 1; i < n; ++i) if (s.v[i] > s.v[i - 1]) throw Error(Status::invalid_input, "fit.bin: top store not sorted (I1)");
  // I1, one entry per model (INTERFACES §4.1 v0.1.13; PR40 review #6): a fit.bin merged before that rule (V mode) may
  // hold a model twice, which double counts it in log Z_T, PIP_T and the occupancy sets. Refuse such files.
  {
    std::vector<std::pair<uint64_t, uint32_t>> kp(n);
    for (size_t i = 0; i < n; ++i) kp[i] = {s.hash[i], (uint32_t)i};
    auto mless = [&](uint32_t a, uint32_t b) {
      return std::lexicographical_compare(s.pool + s.off[a], s.pool + s.off[a] + s.len[a], s.pool + s.off[b], s.pool + s.off[b] + s.len[b]);
    };
    std::sort(kp.begin(), kp.end(), [&](const std::pair<uint64_t, uint32_t>& x, const std::pair<uint64_t, uint32_t>& y) {
      return x.first != y.first ? x.first < y.first : mless(x.second, y.second);
    });
    for (size_t t = 1; t < n; ++t)
      if (kp[t].first == kp[t - 1].first && !mless(kp[t - 1].second, kp[t].second) && !mless(kp[t].second, kp[t - 1].second))
        throw Error(Status::invalid_input, "fit.bin: a model appears twice in the top store (I1; re-merge with the current engine)");
  }
}

std::string arg_str(const Json& a, const std::string& k, const std::string& d) {
  const Json* p = jfind(a, k);
  if (!p) return d;
  if (p->type() == Json::STR) return p->str();
  if (p->type() == Json::NUM) { char b[64]; std::snprintf(b, sizeof b, "%.17g", p->num()); return b; }
  throw Error(Status::invalid_input, "argument " + k + ": expected a string");
}
double arg_num(const Json& a, const std::string& k, double d) {
  const Json* p = jfind(a, k);
  if (!p) return d;
  if (p->type() == Json::NUM) return p->num();
  if (p->type() == Json::STR) { try { return std::stod(p->str()); } catch (...) {} }
  throw Error(Status::invalid_input, "argument " + k + ": expected a number");
}
std::string out_bin(const Json& a, const std::string& d) { return arg_str(a, "out", d); }

}  // namespace v4::eval::io
