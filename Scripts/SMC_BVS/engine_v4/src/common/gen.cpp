// gen.cpp -- synthetic data generator (see gen.h for the definition).
#include "v4/gen.h"
#include <algorithm>
#include <cmath>
#include "v4/format.h"
#include "v4/pmath.h"
#include "v4/provenance.h"
#include "v4/rng.h"
#include "v4/sha256.h"
#include "v4/status.h"

namespace v4::gen {

static constexpr const char* GEN_VERSION = "smcbvs4.gen/1";

Design design_from_name(const std::string& s) {
  if (s == "IND") return Design::IND;
  if (s == "AR") return Design::AR;
  if (s == "BLK") return Design::BLK;
  if (s == "ADJ-OPP" || s == "ADJOPP") return Design::ADJOPP;
  throw Error(Status::invalid_input, "unknown design " + s);
}
std::string design_name(Design d) {
  switch (d) { case Design::IND: return "IND"; case Design::AR: return "AR"; case Design::BLK: return "BLK"; case Design::ADJOPP: return "ADJ-OPP"; }
  return "?";
}
Spec spec_from_json(const Json& j) {
  Spec s;
  s.design = design_from_name(j.at("design").str());
  s.n = (int32_t)j.at("n").i64(); s.p = (int32_t)j.at("p").i64(); s.seed = (uint32_t)j.at("seed").i64();
  if (j.contains("rho")) s.rho = j.at("rho").num(); else if (s.design == Design::BLK) s.rho = 0.5;
  if (j.contains("b")) s.b = (int32_t)j.at("b").i64();
  if (j.contains("a")) s.a = j.at("a").num();
  if (j.contains("s0")) s.s0 = (int32_t)j.at("s0").i64();
  if (j.contains("sigma")) s.sigma = j.at("sigma").num();
  if (s.n < 3 || s.p < 1 || s.seed < 1 || s.seed > 2147483647u) throw Error(Status::invalid_input, "gen: need n >= 3, p >= 1, seed in [1, 2^31-1]");
  if (!(s.rho >= 0 && s.rho < 1)) throw Error(Status::invalid_input, "gen: rho must be in [0, 1)");
  if (s.design == Design::BLK && s.b < 1) throw Error(Status::invalid_input, "gen: b >= 1");
  if (s.s0 < 0 || s.s0 > 5 || s.s0 > s.p) throw Error(Status::invalid_input, "gen: s0 in 0..min(5, p)");
  if (s.design == Design::ADJOPP && (s.s0 < 2 || s.p < 10)) throw Error(Status::invalid_input, "gen: ADJ-OPP needs s0 >= 2 and p >= 10");
  return s;
}
Json spec_to_json(const Spec& s) {
  Json j = Json::object();
  j["design"] = design_name(s.design); j["n"] = s.n; j["p"] = s.p; j["seed"] = s.seed; j["rho"] = s.rho;
  j["b"] = s.b; j["a"] = s.a; j["s0"] = s.s0; j["sigma"] = s.sigma;
  return j;
}

Truth truth(const Spec& s) {
  static const double base[5] = {1.0, -0.8, 0.9, -0.7, 0.6};
  Truth t;
  if (s.a == 0.0 || s.s0 == 0) return t;
  std::vector<int64_t> pos;
  for (int k = 1; k <= s.s0; ++k) pos.push_back(std::max<int64_t>(k, (int64_t)(2 * k - 1) * s.p / 10));
  if (s.design == Design::ADJOPP) pos[1] = pos[0] + 1;
  for (size_t k = 1; k < pos.size(); ++k) if (pos[k] <= pos[k - 1]) pos[k] = pos[k - 1] + 1;   // strictly increasing
  if (s.design == Design::BLK)
    for (size_t k = 1; k < pos.size(); ++k)
      while ((pos[k] - 1) / s.b <= (pos[k - 1] - 1) / s.b) pos[k] = ((pos[k] - 1) / s.b + 1) * s.b + 1;
  for (size_t k = 0; k < pos.size(); ++k) {
    if (pos[k] > s.p) throw Error(Status::invalid_input, "gen: truths do not fit in p columns");
    t.S0.push_back((int32_t)pos[k]); t.beta.push_back(s.a * base[k]);
  }
  return t;
}

double normal_at(uint32_t seed, uint8_t xph, uint32_t row, uint32_t col) {
  Address a; a.seed = seed; a.role = R_GEN; a.xph = xph; a.particle = row; a.position = col;
  for (uint32_t t = 0;; ++t) {
    a.slot = t;
    double u, u2; uniform2_at(a, u, u2);
    double v1 = 2.0 * u - 1.0, v2 = 2.0 * u2 - 1.0;
    double r = v1 * v1 + v2 * v2;
    if (r > 0.0 && r < 1.0) return v1 * pm::sqrt(-2.0 * pm::log(r) / r);
    if (t == 0xFFFFFFFFu) throw Error(Status::internal_error, "gen: polar method did not accept");
  }
}

static double powi(double x, int64_t d) {   // exponentiation by squaring (no libm; deterministic)
  double r = 1.0, b = x;
  while (d > 0) { if (d & 1) r *= b; b *= b; d >>= 1; }
  return r;
}

void generate(const Spec& s, std::vector<double>& X, std::vector<double>& y) {
  const int32_t n = s.n, p = s.p;
  X.assign((size_t)n * p, 0.0);
  y.assign((size_t)n, 0.0);
  if (s.design == Design::AR || s.design == Design::ADJOPP) {
    const double rho = s.rho, c = pm::sqrt(1.0 - rho * rho);
#pragma omp parallel for schedule(static)
    for (int32_t i = 0; i < n; ++i) {
      double prev = normal_at(s.seed, X_GEN_X, (uint32_t)i, 0);
      X[(size_t)i] = prev;
      for (int32_t j = 1; j < p; ++j) {
        double x = rho * prev + c * normal_at(s.seed, X_GEN_X, (uint32_t)i, (uint32_t)j);
        X[(size_t)j * n + i] = x; prev = x;
      }
    }
  } else if (s.design == Design::BLK) {
    const double sf = pm::sqrt(s.rho), se = pm::sqrt(1.0 - s.rho);
#pragma omp parallel for schedule(static)
    for (int32_t j = 0; j < p; ++j)
      for (int32_t i = 0; i < n; ++i)
        X[(size_t)j * n + i] = sf * normal_at(s.seed, X_GEN_FACTOR, (uint32_t)i, (uint32_t)(j / s.b)) +
                               se * normal_at(s.seed, X_GEN_X, (uint32_t)i, (uint32_t)j);
  } else {
#pragma omp parallel for schedule(static)
    for (int32_t j = 0; j < p; ++j)
      for (int32_t i = 0; i < n; ++i) X[(size_t)j * n + i] = normal_at(s.seed, X_GEN_X, (uint32_t)i, (uint32_t)j);
  }
  Truth t = truth(s);
  for (int32_t i = 0; i < n; ++i) {
    double m = 0;
    for (size_t k = 0; k < t.S0.size(); ++k) m += t.beta[k] * X[(size_t)(t.S0[k] - 1) * n + i];
    y[(size_t)i] = m + s.sigma * normal_at(s.seed, X_GEN_NOISE, (uint32_t)i, 0);
  }
}

void generate_test(const Spec& s, int32_t nt, const std::vector<int32_t>& cols, std::vector<int32_t>& oc,
                   std::vector<double>& Xt, std::vector<double>& yt) {
  Truth t = truth(s);
  oc = cols; oc.insert(oc.end(), t.S0.begin(), t.S0.end());
  std::sort(oc.begin(), oc.end()); oc.erase(std::unique(oc.begin(), oc.end()), oc.end());
  for (int32_t j : oc) if (j < 1 || j > s.p) throw Error(Status::invalid_input, "gen test: column out of range");
  const size_t m = oc.size();
  Xt.assign((size_t)nt * m, 0.0); yt.assign((size_t)nt, 0.0);
#pragma omp parallel for schedule(static)
  for (int32_t i = 0; i < nt; ++i) {
    double prev = 0; int64_t jprev = -1;
    for (size_t c = 0; c < m; ++c) {
      uint32_t j0 = (uint32_t)(oc[c] - 1);   // 0-based column
      double x;
      if (s.design == Design::AR || s.design == Design::ADJOPP) {
        double e = normal_at(s.seed, X_TEST_X, (uint32_t)i, j0);
        if (jprev < 0) x = e;
        else { double rd = powi(s.rho, (int64_t)j0 - jprev); x = rd * prev + pm::sqrt(1.0 - rd * rd) * e; }
        prev = x; jprev = j0;
      } else if (s.design == Design::BLK) {
        x = pm::sqrt(s.rho) * normal_at(s.seed, X_TEST_FACTOR, (uint32_t)i, j0 / (uint32_t)s.b) +
            pm::sqrt(1.0 - s.rho) * normal_at(s.seed, X_TEST_X, (uint32_t)i, j0);
      } else {
        x = normal_at(s.seed, X_TEST_X, (uint32_t)i, j0);
      }
      Xt[c * nt + i] = x;
    }
    double mu = 0;
    for (size_t k = 0; k < t.S0.size(); ++k) {
      size_t c = (size_t)(std::lower_bound(oc.begin(), oc.end(), t.S0[k]) - oc.begin());
      mu += t.beta[k] * Xt[c * nt + i];
    }
    yt[(size_t)i] = mu + s.sigma * normal_at(s.seed, X_TEST_NOISE, (uint32_t)i, 0);
  }
}

static Json truth_json(const Spec& s, const Truth& t) {
  Json j = Json::object();
  j["generator"] = GEN_VERSION; j["spec"] = spec_to_json(s);
  j["S0"] = Json::array_of(t.S0); j["beta"] = Json::array_of(t.beta); j["sigma"] = s.sigma;
  return j;
}
static Json file_meta(const Spec& s, const Truth& t) {
  Json j = truth_json(s, t);
  j["kind"] = "raw"; j["mode"] = "none"; j["inputs"] = Json::object(); j["binary"] = binary_block();
  return j;
}

Json run(const Json& args) {
  Spec s = spec_from_json(args.at("spec"));
  std::string out = args.at("out").str();
  std::vector<double> X, y;
  generate(s, X, y);
  Truth t = truth(s);
  fmt::Writer w(fmt::K_RAW, fmt::M_NONE);
  w.add("X_cm", X, (uint64_t)s.n, (uint64_t)s.p);
  w.add("y", y);
  w.add_json("meta", file_meta(s, t));
  std::string h = w.write(out);
  // data identity (independent of the binary block in meta): the section hashes of X_cm and y
  std::string hx = hex(sha256(X.data(), X.size() * 8)), hy = hex(sha256(y.data(), y.size() * 8));
  Json tj = truth_json(s, t); tj["raw_content_sha256"] = h; tj["X_sha256"] = hx; tj["y_sha256"] = hy;
  if (args.contains("truth")) write_json_file(args.at("truth").str(), tj);
  Json rec = Json::object();
  rec["status"] = "completed"; rec["raw"] = out; rec["raw_content_sha256"] = h; rec["X_sha256"] = hx; rec["y_sha256"] = hy;
  rec["truth"] = tj;
  return rec;
}

Json run_test(const Json& args) {
  Spec s = spec_from_json(args.at("spec"));
  int32_t nt = (int32_t)args.at("ntest").i64();
  std::vector<int32_t> cols;
  for (auto& c : args.at("cols").elems()) cols.push_back((int32_t)c.i64());
  std::vector<int32_t> oc; std::vector<double> Xt, yt;
  generate_test(s, nt, cols, oc, Xt, yt);
  fmt::Writer w(fmt::K_RAW, fmt::M_NONE);
  w.add("Xt_cm", Xt, (uint64_t)nt, (uint64_t)oc.size());
  w.add("yt", yt); w.add("cols", oc);
  Json meta = file_meta(s, truth(s)); meta["ntest"] = nt; meta["kind"] = "test_rows";
  w.add_json("meta", meta);
  std::string h = w.write(args.at("out").str());
  Json rec = Json::object(); rec["status"] = "completed"; rec["content_sha256"] = h; rec["ncols"] = (int64_t)oc.size();
  return rec;
}

}  // namespace v4::gen
