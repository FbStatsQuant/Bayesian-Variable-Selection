// io.cpp -- WP5 readers (see io.h).
#include "io.h"

#include <cmath>
#include <cstdio>
#include <fstream>

namespace v4::eval::io {

using wp5prov::BinReader;

void load_data(const std::string& path, DataFile& o, bool verify) {
  o.bin = std::make_unique<BinReader>(path, verify);
  const BinReader& B = *o.bin;
  if (B.header().kind != wp5prov::K_DATA) throw Error(Status::invalid_input, path + ": not a data.bin (kind != 2)");
  o.meta = Json::parse(B.json("meta"));
  EvalData& D = o.D;
  D.n = (int32_t)o.meta.at("n").num();
  D.p = (int32_t)o.meta.at("p").num();
  D.p_raw = (int32_t)o.meta.num_or("p_raw", D.p);
  uint64_t c = 0;
  D.Xs = B.ptr<double>("Xs_cm", wp5prov::DT_F64, &c);
  if (c != (uint64_t)D.n * (uint64_t)D.p) throw Error(Status::invalid_input, "data.bin: Xs_cm size != n p");
  D.ys = B.ptr<double>("ys", wp5prov::DT_F64, &c); if (c != (uint64_t)D.n) throw Error(Status::invalid_input, "data.bin: ys size");
  D.z = B.has("z") ? B.ptr<double>("z", wp5prov::DT_F64) : nullptr;
  D.col_max = B.ptr<double>("col_max", wp5prov::DT_F64);
  D.col_mean = B.ptr<double>("col_mean", wp5prov::DT_F64);
  D.col_sd = B.ptr<double>("col_sd", wp5prov::DT_F64);
  const int32_t* kept = B.ptr<int32_t>("kept", wp5prov::DT_I32, &c);
  if (c != (uint64_t)D.p) throw Error(Status::invalid_input, "data.bin: kept size != p");
  o.orig_owned.assign(kept, kept + D.p);
  for (int32_t j = 1; j < D.p; ++j) if (!(o.orig_owned[j - 1] < o.orig_owned[j])) throw Error(Status::invalid_input, "data.bin: kept not increasing");
  D.orig = o.orig_owned.data();
  double yty = 0; for (int32_t i = 0; i < D.n; ++i) yty += D.ys[i] * D.ys[i];
  D.yty = o.meta.num_or("yty", yty);
  D.y_max = o.meta.at("y_max").num(); D.y_mean = o.meta.at("y_mean").num(); D.y_sd_scaled = o.meta.at("y_sd_scaled").num();
  data_constants(D);
  if (B.has("logprior")) {   // WP1's bits win; ours must agree (else the inputs disagree on the prior)
    const double* lp = B.ptr<double>("logprior", wp5prov::DT_F64, &c);
    if (c != (uint64_t)D.K + 1) throw Error(Status::invalid_input, "data.bin: logprior length != K + 1");
    for (uint64_t k = 0; k < c; ++k) {
      if (std::fabs(lp[k] - D.logprior[k]) > 1e-9 * std::max(1.0, std::fabs(lp[k])))
        throw Error(Status::invalid_input, "data.bin: logprior disagrees with the eval recomputation");
      D.logprior[k] = lp[k];
    }
  }
}

void load_fit(const std::string& path, FitFile& o, bool verify) {
  o.bin = std::make_unique<BinReader>(path, verify);
  const BinReader& B = *o.bin;
  if (B.header().kind != wp5prov::K_FIT) throw Error(Status::invalid_input, path + ": not a fit.bin (kind != 6)");
  o.meta = B.has("meta") ? Json::parse(B.json("meta")) : Json::object();
  uint64_t n = 0, c = 0;
  StoreView& s = o.top;
  s.v = B.ptr<double>("top_v", wp5prov::DT_F64, &n); s.size = n;
  s.off = B.ptr<uint64_t>("top_off", wp5prov::DT_U64, &c); if (c != n) throw Error(Status::invalid_input, "fit.bin: top_off size");
  s.len = B.ptr<uint16_t>("top_len", wp5prov::DT_U16, &c); if (c != n) throw Error(Status::invalid_input, "fit.bin: top_len size");
  s.hash = B.ptr<uint64_t>("top_hash", wp5prov::DT_U64, &c); if (c != n) throw Error(Status::invalid_input, "fit.bin: top_hash size");
  s.pool = B.ptr<int32_t>("top_pool", wp5prov::DT_I32, &c);
  for (size_t i = 0; i < n; ++i) if (s.off[i] + s.len[i] > c) throw Error(Status::invalid_input, "fit.bin: store entry beyond pool");
  for (size_t i = 1; i < n; ++i) if (s.v[i] > s.v[i - 1]) throw Error(Status::invalid_input, "fit.bin: top store not sorted (I1)");
}

std::map<std::string, std::string> parse_args(int argc, char** argv, int first) {
  std::map<std::string, std::string> a;
  for (int i = first; i < argc; ++i) {
    std::string k = argv[i];
    if (k.rfind("--", 0) != 0) throw Error(Status::invalid_input, "unexpected argument " + k);
    k = k.substr(2);
    if (i + 1 < argc && std::string(argv[i + 1]).rfind("--", 0) != 0) a[k] = argv[++i];
    else a[k] = "1";
  }
  return a;
}
std::string arg_or(const std::map<std::string, std::string>& a, const std::string& k, const std::string& d) {
  auto it = a.find(k); return it == a.end() ? d : it->second;
}
std::string file_sha256(const std::string& path) {
  std::ifstream f(path, std::ios::binary);
  if (!f) throw Error(Status::invalid_input, "cannot open " + path);
  wp5prov::Sha256 h; char buf[1 << 16];
  while (f) { f.read(buf, sizeof buf); h.update(buf, (size_t)f.gcount()); }
  uint8_t d[32]; h.final(d); return wp5prov::hex(d, 32);
}
int finish(const std::string& out_json, Json rec, Status st, const std::string& reason) {
  rec.set("status", wp5prov::Json(status_name(st)));
  rec.set("reason", reason);
  try { wp5prov::write_text_atomic(out_json, rec.dump(1) + "\n"); }
  catch (const std::exception& e) { std::fprintf(stderr, "io_error: %s\n", e.what()); return 10 + (int)Status::io_error; }
  return st == Status::completed ? 0 : 10 + (int)st;
}

}  // namespace v4::eval::io
