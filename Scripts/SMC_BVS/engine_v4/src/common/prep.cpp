// prep.cpp -- preprocessing with R's arithmetic (see prep.h).
#include "v4/prep.h"
#include <cfloat>
#include <cmath>
#include <fstream>
#include "v4/format.h"
#include "v4/sha256.h"
#include "v4/status.h"

namespace v4::prep {

// R 4.x src/main/summary.c, real_mean (REALSXP branch), re-implemented: LDOUBLE s = sum x; s /= n; if finite:
// t = sum (x_i - s) in long double; s += t / n; return (double) s. (The overflow branch "s = sum x_i / n" is kept.)
double r_mean(const double* x, size_t n) {
  long double s = 0.0L;
  for (size_t i = 0; i < n; ++i) s += x[i];
  if (std::isfinite((double)s)) s /= (long double)n;
  else { long double t = 0.0L; for (size_t i = 0; i < n; ++i) t += x[i] / (long double)n; s = t; }
  if (std::isfinite((double)s)) {
    long double t = 0.0L;
    for (size_t i = 0; i < n; ++i) t += (x[i] - s);
    s += t / (long double)n;
  }
  return (double)s;
}
// R 4.x src/main/summary.c, rsum, re-implemented: LDOUBLE accumulation; +-Inf beyond DBL_MAX.
double r_sum(const double* x, size_t n) {
  long double s = 0.0L;
  for (size_t i = 0; i < n; ++i) s += x[i];
  if (s > DBL_MAX) return HUGE_VAL;
  if (s < -DBL_MAX) return -HUGE_VAL;
  return (double)s;
}

// core/v3_preprocess.R:24-51 (v3_standardise), translated statement by statement. R's x^2 is x*x (arithmetic.c R_POW
// special case), max(abs(x)) is exact, vector ops are elementwise double operations.
ColStd standardise(const double* x, size_t n, double* z) {
  ColStd c;
  double mx = 0; for (size_t i = 0; i < n; ++i) mx = std::max(mx, std::fabs(x[i]));   // mx <- max(abs(x))
  std::vector<double> x1(n), x2(n), sq(n);
  for (size_t i = 0; i < n; ++i) x1[i] = x[i] / mx;                                   // x1 <- x / mx
  double mu = r_mean(x1.data(), n);                                                   // mu <- mean(x1)
  double m2 = 0;
  for (size_t i = 0; i < n; ++i) { x2[i] = x1[i] - mu; m2 = std::max(m2, std::fabs(x2[i])); }   // x2 <- x1 - mu
  if (m2 <= std::sqrt(DBL_EPSILON)) {                                                 // anchored two-pass branch
    std::vector<double> d(n), u(n), uc(n);
    double dm = 0;
    for (size_t i = 0; i < n; ++i) { d[i] = x[i] - x[0]; dm = std::max(dm, std::fabs(d[i])); }
    for (size_t i = 0; i < n; ++i) u[i] = d[i] / dm;
    double um = r_mean(u.data(), n);
    for (size_t i = 0; i < n; ++i) uc[i] = u[i] - um;
    double correction = r_mean(uc.data(), n);
    for (size_t i = 0; i < n; ++i) uc[i] = uc[i] - correction;
    for (size_t i = 0; i < n; ++i) sq[i] = uc[i] * uc[i];
    double us = std::sqrt(r_sum(sq.data(), n) / (double)(n - 1));
    double ratio = dm / mx;
    for (size_t i = 0; i < n; ++i) z[i] = uc[i] / us;
    c.max = mx; c.mean = (x[0] / mx + ratio * um) + ratio * correction; c.sd = ratio * us; c.anchored = true;
    return c;
  }
  for (size_t i = 0; i < n; ++i) sq[i] = x2[i] * x2[i];
  double s = std::sqrt(r_sum(sq.data(), n) / (double)(n - 1));                       // s <- sqrt(sum(x2^2) / (n - 1))
  for (size_t i = 0; i < n; ++i) z[i] = x2[i] / s;                                    // z = x2 / s
  c.max = mx; c.mean = mu; c.sd = s;
  return c;
}

Result preprocess(const double* X, const double* y, int32_t n, int32_t p_raw) {
  Result r; r.n = n; r.p_raw = p_raw;
  auto bad = [&](const char* why) { r.status = "invalid_input"; r.reason = why; return r; };
  for (size_t i = 0; i < (size_t)n * p_raw; ++i) if (!std::isfinite(X[i])) return bad("non-finite entry in X or y");
  for (int32_t i = 0; i < n; ++i) if (!std::isfinite(y[i])) return bad("non-finite entry in X or y");
  if (n < 3) return bad("n < 3");
  if (p_raw < 1) return bad("p < 1");
  for (int32_t j = 0; j < p_raw; ++j) {
    const double* xj = X + (size_t)j * n; bool constant = true;
    for (int32_t i = 1; i < n && constant; ++i) if (!(xj[i] == xj[0])) constant = false;
    (constant ? r.dropped : r.kept).push_back(j + 1);
  }
  r.p = (int32_t)r.kept.size();
  if (r.kept.empty()) { r.status = "no_predictors"; return r; }
  bool yc = true; for (int32_t i = 1; i < n && yc; ++i) if (!(y[i] == y[0])) yc = false;
  if (yc) { r.status = "y_constant"; return r; }
  r.own = std::make_shared<DataOwned>();
  auto& o = *r.own;
  o.X.assign((size_t)n * r.p, 0.0); o.y.assign((size_t)n, 0.0);
  o.col_max.resize(r.p); o.col_mean.resize(r.p); o.col_sd.resize(r.p);
  for (int32_t a = 0; a < r.p; ++a) {
    ColStd c = standardise(X + (size_t)(r.kept[a] - 1) * n, (size_t)n, o.X.data() + (size_t)a * n);
    o.col_max[a] = c.max; o.col_mean[a] = c.mean; o.col_sd[a] = c.sd;
  }
  r.ystd = standardise(y, (size_t)n, o.y.data());
  o.orig = r.kept; o.dropped = r.dropped;
  return r;
}

std::string write_data(const std::string& path, const Data& D, const Result& r, const std::string& prep_class, const Json& inputs) {
  fmt::Writer w(fmt::K_DATA, fmt::M_NONE);
  w.add("Xs_cm", D.Xs, (uint64_t)D.n * D.p, (uint64_t)D.n, (uint64_t)D.p);
  w.add("ys", D.ys, (uint64_t)D.n);
  w.add("z", D.z, (uint64_t)D.p);
  w.add("diagG", D.diagG, (uint64_t)D.p);
  w.add("col_max", D.col_max, (uint64_t)D.p);
  w.add("col_mean", D.col_mean, (uint64_t)D.p);
  w.add("col_sd", D.col_sd, (uint64_t)D.p);
  w.add("kept", D.orig, (uint64_t)D.p);
  w.add("dropped", r.dropped);
  w.add("logw", D.logw);
  w.add("logprior", D.logprior);
  Json m = Json::object();
  m["n"] = D.n; m["p_raw"] = r.p_raw; m["p"] = D.p; m["K"] = D.K; m["yty"] = D.yty; m["logCn"] = D.logCn; m["logm0"] = D.logm0;
  m["logWK"] = D.logWK; m["nu"] = D.nu; m["a0"] = D.a0; m["b0"] = D.b0;
  m["y_max"] = D.y_max; m["y_mean"] = D.y_mean; m["y_sd_scaled"] = D.y_sd_scaled; m["prep_class"] = prep_class;
  m["inputs"] = inputs; m["schema"] = "smcbvs4.data/1";
  w.add_json("meta", m);
  return w.write(path);
}

Data load_data(const std::string& path, std::string* content_hash) {
  auto rd = std::make_shared<fmt::Reader>(path);
  if (rd->kind() != fmt::K_DATA) throw Error(Status::invalid_input, path + " is not a data file");
  Json m = rd->json("meta");
  Data D;
  D.n = (int32_t)m.at("n").i64(); D.p = (int32_t)m.at("p").i64(); D.p_raw = (int32_t)m.at("p_raw").i64();
  uint64_t c;
  D.Xs = rd->get<double>("Xs_cm", &c); if (c != (uint64_t)D.n * D.p) throw Error(Status::invalid_input, "data.bin: Xs size");
  D.ys = rd->get<double>("ys", &c); if (c != (uint64_t)D.n) throw Error(Status::invalid_input, "data.bin: ys size");
  D.z = rd->get<double>("z"); D.diagG = rd->get<double>("diagG");
  D.col_max = rd->get<double>("col_max"); D.col_mean = rd->get<double>("col_mean"); D.col_sd = rd->get<double>("col_sd");
  D.orig = rd->get<int32_t>("kept");
  D.yty = m.at("yty").num(); D.y_max = m.at("y_max").num(); D.y_mean = m.at("y_mean").num(); D.y_sd_scaled = m.at("y_sd_scaled").num();
  data_constants(D);
  // the stored constants must equal the recomputed ones (same binary, same libm): a mismatch means a different libm
  if (D.logCn != m.at("logCn").num() || D.logm0 != m.at("logm0").num() || D.logWK != m.at("logWK").num() || D.K != m.at("K").i64())
    throw Error(Status::invalid_input, "data.bin: stored constants differ from the recomputed ones (libm or binary mismatch)");
  if (content_hash) *content_hash = rd->content_hash();
  D.keep = std::shared_ptr<const void>(rd, rd.get());
  return D;
}

static std::vector<double> read_f64(const std::string& f, size_t n) {
  std::ifstream in(f, std::ios::binary);
  if (!in) throw Error(Status::invalid_input, "cannot open " + f);
  std::vector<double> v(n);
  in.read((char*)v.data(), (std::streamsize)(n * 8));
  if ((size_t)in.gcount() != n * 8) throw Error(Status::invalid_input, "short file " + f);
  return v;
}

Json run(const Json& args) {
  std::string out = args.at("out").str();
  Json inputs = Json::object();
  Result r; std::string cls;
  if (args.contains("from_r")) {
    // R-standardised input (compat gates): dir with meta.json {n, p, p_raw, kept, dropped, y_max, y_mean, y_sd_scaled},
    // Xs.f64 (n*p col-major), ys.f64, col_max.f64, col_mean.f64, col_sd.f64 (little-endian doubles).
    std::string dir = args.at("from_r").str();
    Json m = read_json_file(dir + "/meta.json");
    r.n = (int32_t)m.at("n").i64(); r.p = (int32_t)m.at("p").i64(); r.p_raw = (int32_t)m.at("p_raw").i64();
    for (auto& v : m.at("kept").elems()) r.kept.push_back((int32_t)v.i64());
    for (auto& v : m.at("dropped").elems()) r.dropped.push_back((int32_t)v.i64());
    r.own = std::make_shared<DataOwned>();
    r.own->X = read_f64(dir + "/Xs.f64", (size_t)r.n * r.p); r.own->y = read_f64(dir + "/ys.f64", (size_t)r.n);
    r.own->col_max = read_f64(dir + "/col_max.f64", (size_t)r.p); r.own->col_mean = read_f64(dir + "/col_mean.f64", (size_t)r.p);
    r.own->col_sd = read_f64(dir + "/col_sd.f64", (size_t)r.p);
    r.own->orig = r.kept; r.own->dropped = r.dropped;
    r.ystd.max = m.at("y_max").num(); r.ystd.mean = m.at("y_mean").num(); r.ystd.sd = m.at("y_sd_scaled").num();
    cls = "B(R-standardised input)";
    inputs["from_r_meta.json"] = sha256_file(dir + "/meta.json");
    inputs["from_r_Xs.f64"] = sha256_file(dir + "/Xs.f64");
  } else {
    std::string in = args.at("in").str();
    fmt::Reader rd(in);
    if (rd.kind() != fmt::K_RAW) throw Error(Status::invalid_input, in + " is not a raw file");
    const auto& e = rd.entry("X_cm");
    int32_t n = (int32_t)e.dims[0], p = (int32_t)e.dims[1];
    r = preprocess(rd.get<double>("X_cm"), rd.get<double>("y"), n, p);
    cls = "B";
    inputs["raw.bin"] = rd.content_hash();
  }
  Json rec = Json::object();
  if (r.status != "ok") {
    rec["status"] = r.status == "invalid_input" ? "invalid_input" : "completed";
    rec["prep_status"] = r.status; rec["reason"] = r.reason;
    return rec;
  }
  Data D = make_data(r.own, r.n, r.p);
  D.p_raw = r.p_raw; D.y_max = r.ystd.max; D.y_mean = r.ystd.mean; D.y_sd_scaled = r.ystd.sd;
  std::string h = write_data(out, D, r, cls, inputs);
  rec["status"] = "completed"; rec["prep_status"] = "ok"; rec["data"] = out; rec["content_sha256"] = h;
  rec["n"] = r.n; rec["p"] = r.p; rec["p_raw"] = r.p_raw; rec["dropped"] = Json::array_of(r.dropped); rec["prep_class"] = cls;
  return rec;
}

}  // namespace v4::prep
