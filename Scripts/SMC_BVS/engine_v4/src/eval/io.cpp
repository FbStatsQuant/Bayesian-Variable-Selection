// io.cpp -- WP5 readers (see io.h).
#include "io.h"

#include <cmath>
#include <cstdio>

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
  for (size_t i = 0; i < n; ++i) if (s.off[i] + s.len[i] > c) throw Error(Status::invalid_input, "fit.bin: store entry beyond pool");
  for (size_t i = 1; i < n; ++i) if (s.v[i] > s.v[i - 1]) throw Error(Status::invalid_input, "fit.bin: top store not sorted (I1)");
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
