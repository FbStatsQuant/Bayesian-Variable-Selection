// law.cpp -- build / write / read law.bin (see include/v4/post.h) and the `post` command.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <map>

#include "../eval/io.h"
#include "v4/post.h"

namespace v4::post {

using eval::Json;
using wp5prov::BinReader;
using wp5prov::BinWriter;

LawFile build_law(const eval::EvalData& D, const eval::StoreView& s, double rel_cut, size_t max_models) {
  LawFile L;
  L.n = D.n; L.p = D.p; L.rel_cut = rel_cut; L.n_store = s.size;
  L.ybar = D.ybar(); L.sy = D.sy(); L.a0 = D.a0; L.b0 = D.b0;
  eval::StoreMass sm = eval::store_mass(s, rel_cut);
  L.vmax = sm.vmax; L.logZ_T = sm.logZ_T;
  if (s.size == 0) throw Error(Status::invalid_input, "build_law: empty store");
  const double lcut = std::log(rel_cut);
  // the store is sorted by F descending (I1), so the kept models are a prefix
  std::vector<size_t> keep;
  for (size_t i = 0; i < s.size && keep.size() < max_models; ++i) { if (s.v[i] - sm.vmax < lcut) break; keep.push_back(i); }
  long double tot = 0, kept = 0, drop = 0;
  for (size_t i = 0; i < s.size; ++i) { long double e = std::exp((long double)(s.v[i] - sm.vmax)); tot += e; if (i >= keep.size()) drop += e; }
  for (size_t i : keep) kept += std::exp((long double)(s.v[i] - sm.vmax));
  L.dropped_mass = (double)(drop / tot);   // includes models cut by max_models
  std::map<int32_t, int> colset;
  for (size_t i : keep) {
    eval::Model S = s.model(i);
    eval::ModelPost mp = eval::model_post(D, S);
    L.max_abs_dF = std::max(L.max_abs_dF, std::fabs(mp.F - s.v[i]));
    mp.F = s.v[i];
    for (int32_t j : S) colset[j] = 1;
    L.models.push_back(std::move(mp));
    L.w.push_back((double)(std::exp((long double)(s.v[i] - sm.vmax)) / kept));
  }
  for (auto& kv : colset) {
    L.cols.push_back(kv.first); L.cols_orig.push_back(D.orig[kv.first]);
    L.cols_xbar.push_back(D.xbar(kv.first)); L.cols_xsd.push_back(D.xsd(kv.first));
  }
  return L;
}

eval::Law to_eval_law(const LawFile& L, const std::string& name) {
  eval::Law out; out.name = name; out.dropped_mass = L.dropped_mass;
  for (size_t m = 0; m < L.models.size(); ++m) {
    const eval::ModelPost& mp = L.models[m];
    eval::Component c; c.w = L.w[m]; c.gaussian = false; c.n = L.n; c.alpha_n = mp.alpha_n; c.beta_n = mp.beta_n;
    c.theta_bar = mp.theta_bar; c.LH = mp.LH; c.F = mp.F; c.ybar = L.ybar; c.sy = L.sy;
    for (int32_t j : mp.S) {
      size_t q = (size_t)(std::lower_bound(L.cols.begin(), L.cols.end(), j) - L.cols.begin());
      c.orig.push_back(L.cols_orig[q]); c.xbar.push_back(L.cols_xbar[q]); c.xsd.push_back(L.cols_xsd[q]);
    }
    out.comps.push_back(std::move(c));
  }
  return out;
}

std::string write_law(const LawFile& L, const std::string& path, int n_draws, uint32_t draw_seed) {
  const size_t M = L.models.size(), C = L.cols.size();
  std::vector<int64_t> mptr(M + 1, 0), lptr(M + 1, 0);
  std::vector<int32_t> midx; std::vector<double> F(M), w = L.w, logm(M), Q(M), an(M), bn(M), th, LH;
  std::vector<uint8_t> route(M);
  for (size_t m = 0; m < M; ++m) {
    const eval::ModelPost& mp = L.models[m];
    const size_t k = mp.S.size();
    midx.insert(midx.end(), mp.S.begin(), mp.S.end());
    th.insert(th.end(), mp.theta_bar.begin(), mp.theta_bar.end());
    for (size_t i = 0; i < k; ++i) for (size_t j = 0; j <= i; ++j) LH.push_back(mp.LH[i * k + j]);
    mptr[m + 1] = (int64_t)midx.size(); lptr[m + 1] = (int64_t)LH.size();
    F[m] = mp.F; logm[m] = mp.logm; Q[m] = mp.Q; an[m] = mp.alpha_n; bn[m] = mp.beta_n; route[m] = (uint8_t)mp.route;
  }
  Json meta = Json::object();
  meta.set("schema", "smcbvs4.law/1");
  meta.set("n", L.n); meta.set("p", L.p); meta.set("M", (int64_t)M); meta.set("C", (int64_t)C);
  meta.set("rel_cut", L.rel_cut); meta.set("vmax", L.vmax); meta.set("logZ_T", L.logZ_T);
  meta.set("dropped_mass", L.dropped_mass); meta.set("n_store", L.n_store);
  meta.set("ybar", L.ybar); meta.set("sy", L.sy); meta.set("a0", L.a0); meta.set("b0", L.b0); meta.set("max_abs_dF", L.max_abs_dF);
  for (auto& kv : L.meta_extra.items()) meta.set(kv.first, kv.second);
  BinWriter W(wp5prov::K_LAW, wp5prov::M_V);
  W.add_vec("model_ptr", wp5prov::DT_I64, mptr); W.add_vec("model_idx", wp5prov::DT_I32, midx);
  W.add_vec("F", wp5prov::DT_F64, F); W.add_vec("w", wp5prov::DT_F64, w);
  W.add_vec("logm", wp5prov::DT_F64, logm); W.add_vec("Q", wp5prov::DT_F64, Q);
  W.add_vec("alpha_n", wp5prov::DT_F64, an); W.add_vec("beta_n", wp5prov::DT_F64, bn);
  W.add_vec("route", wp5prov::DT_U8, route);
  W.add_vec("theta_bar", wp5prov::DT_F64, th);
  W.add_vec("LH_ptr", wp5prov::DT_I64, lptr); W.add_vec("LH", wp5prov::DT_F64, LH);
  W.add_vec("cols", wp5prov::DT_I32, L.cols); W.add_vec("cols_orig", wp5prov::DT_I32, L.cols_orig);
  W.add_vec("cols_xbar", wp5prov::DT_F64, L.cols_xbar); W.add_vec("cols_xsd", wp5prov::DT_F64, L.cols_xsd);
  if (n_draws > 0) {
    eval::Law el = to_eval_law(L);
    std::vector<int32_t> dm(n_draws); std::vector<double> da(n_draws), dv(n_draws), db((size_t)n_draws * C, 0.0);
    for (int d = 0; d < n_draws; ++d) {
      eval::ParamDraw pd = eval::draw_params(el, draw_seed, 0, (uint32_t)d);
      dm[d] = pd.comp; da[d] = pd.a; dv[d] = pd.v;
      const eval::ModelPost& mp = L.models[pd.comp];
      for (size_t i = 0; i < mp.S.size(); ++i) {
        size_t q = (size_t)(std::lower_bound(L.cols.begin(), L.cols.end(), mp.S[i]) - L.cols.begin());
        db[(size_t)d * C + q] = pd.b[i];
      }
    }
    W.add_vec("draw_model", wp5prov::DT_I32, dm); W.add_vec("draw_a", wp5prov::DT_F64, da); W.add_vec("draw_v", wp5prov::DT_F64, dv);
    W.add("draw_b", wp5prov::DT_F64, db.data(), db.size() * sizeof(double), 2, (uint64_t)n_draws, C);
    Json dj = Json::object(); dj.set("n", n_draws); dj.set("seed", (int64_t)draw_seed); dj.set("role", "POST");
    meta.set("draws", dj);
  } else {
    meta.set("draws", Json());
  }
  W.add_json("meta", meta.dump());
  return W.write(path);
}

LawFile read_law(const std::string& path) {
  BinReader B(path, true);
  if (B.header().kind != wp5prov::K_LAW) throw Error(Status::invalid_input, path + ": not a law.bin (kind != 7)");
  Json meta = Json::parse(B.json("meta"));
  if (meta.str_or("schema", "") != "smcbvs4.law/1") throw Error(Status::invalid_input, path + ": unknown law schema");
  LawFile L;
  L.n = (int32_t)meta.at("n").num(); L.p = (int32_t)meta.at("p").num();
  L.rel_cut = meta.at("rel_cut").num(); L.vmax = meta.at("vmax").num(); L.logZ_T = meta.at("logZ_T").num();
  L.dropped_mass = meta.at("dropped_mass").num(); L.n_store = (uint64_t)meta.at("n_store").num();
  L.ybar = meta.at("ybar").num(); L.sy = meta.at("sy").num(); L.a0 = meta.at("a0").num(); L.b0 = meta.at("b0").num();
  L.max_abs_dF = meta.num_or("max_abs_dF", NAN);
  const size_t M = (size_t)meta.at("M").num();
  uint64_t c;
  const int64_t* mptr = B.ptr<int64_t>("model_ptr", wp5prov::DT_I64, &c); if (c != M + 1) throw Error(Status::invalid_input, "law.bin: model_ptr");
  const int32_t* midx = B.ptr<int32_t>("model_idx", wp5prov::DT_I32, &c);
  if ((uint64_t)mptr[M] != c) throw Error(Status::invalid_input, "law.bin: model_idx size");
  const double *F = B.ptr<double>("F", wp5prov::DT_F64), *w = B.ptr<double>("w", wp5prov::DT_F64), *logm = B.ptr<double>("logm", wp5prov::DT_F64),
               *Q = B.ptr<double>("Q", wp5prov::DT_F64), *an = B.ptr<double>("alpha_n", wp5prov::DT_F64), *bn = B.ptr<double>("beta_n", wp5prov::DT_F64),
               *th = B.ptr<double>("theta_bar", wp5prov::DT_F64), *LH = B.ptr<double>("LH", wp5prov::DT_F64);
  const uint8_t* route = B.ptr<uint8_t>("route", wp5prov::DT_U8);
  const int64_t* lptr = B.ptr<int64_t>("LH_ptr", wp5prov::DT_I64);
  for (size_t m = 0; m < M; ++m) {
    eval::ModelPost mp;
    const size_t k = (size_t)(mptr[m + 1] - mptr[m]);
    mp.S.assign(midx + mptr[m], midx + mptr[m + 1]);
    mp.theta_bar.assign(th + mptr[m], th + mptr[m + 1]);
    if ((size_t)(lptr[m + 1] - lptr[m]) != k * (k + 1) / 2) throw Error(Status::invalid_input, "law.bin: LH block size");
    mp.LH.assign(k * k, 0.0);
    size_t q = (size_t)lptr[m];
    for (size_t i = 0; i < k; ++i) for (size_t j = 0; j <= i; ++j) mp.LH[i * k + j] = LH[q++];
    mp.F = F[m]; mp.logm = logm[m]; mp.Q = Q[m]; mp.alpha_n = an[m]; mp.beta_n = bn[m]; mp.route = route[m];
    L.models.push_back(std::move(mp)); L.w.push_back(w[m]);
  }
  const int32_t* cols = B.ptr<int32_t>("cols", wp5prov::DT_I32, &c);
  L.cols.assign(cols, cols + c);
  const int32_t* co = B.ptr<int32_t>("cols_orig", wp5prov::DT_I32); L.cols_orig.assign(co, co + c);
  const double* cx = B.ptr<double>("cols_xbar", wp5prov::DT_F64); L.cols_xbar.assign(cx, cx + c);
  const double* cs = B.ptr<double>("cols_xsd", wp5prov::DT_F64); L.cols_xsd.assign(cs, cs + c);
  return L;
}

int run(int argc, char** argv) {
  std::string out = "law";
  Json rec = Json::object();
  rec.set("schema", "smcbvs4.post/1"); rec.set("command", "post");
  try {
    auto a = eval::io::parse_args(argc, argv, 1);
    out = eval::io::arg_or(a, "out", "law");
    const std::string fitp = eval::io::arg_or(a, "fit", ""), datap = eval::io::arg_or(a, "data", "");
    if (fitp.empty() || datap.empty()) throw Error(Status::invalid_input, "post: --fit and --data are required");
    const double rel = std::stod(eval::io::arg_or(a, "rel-cut", "1e-12"));
    const size_t maxm = (size_t)std::stoull(eval::io::arg_or(a, "max-models", "1000000"));
    const int nd = std::stoi(eval::io::arg_or(a, "draws", "0"));
    const uint32_t seed = (uint32_t)std::stoul(eval::io::arg_or(a, "seed", "1"));
    auto t0 = std::chrono::steady_clock::now();
    eval::io::DataFile df; eval::io::load_data(datap, df);
    eval::io::FitFile ff; eval::io::load_fit(fitp, ff);
    LawFile L = build_law(df.D, ff.top, rel, maxm);
    Json inp = Json::object(); inp.set("fit.bin", ff.bin->content_hash()); inp.set("data.bin", df.bin->content_hash());
    L.meta_extra.set("inputs", inp);
    const std::string h = write_law(L, out + ".bin", nd, seed);
    rec.set("inputs", inp);
    Json o = Json::object(); o.set("law.bin", h); rec.set("outputs", o);
    rec.set("M", (int64_t)L.models.size()); rec.set("dropped_mass", L.dropped_mass); rec.set("logZ_T", L.logZ_T);
    rec.set("max_abs_dF", L.max_abs_dF);
    rec.set("wall_s", std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count());
    return eval::io::finish(out + ".json", rec, Status::completed, "");
  } catch (const Error& e) {
    return eval::io::finish(out + ".json", rec, e.st, e.what());
  } catch (const std::exception& e) {
    return eval::io::finish(out + ".json", rec, Status::internal_error, e.what());
  }
}

}  // namespace v4::post
