// law.cpp -- build / write / read law.bin (see include/v4/post.h) and the `post` command.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <map>

#include "../eval/io.h"
#include "v4/format.h"
#include "v4/post.h"
#include "v4/prep.h"
#include "v4/provenance.h"

namespace v4::post {


LawFile build_law(const Data& D, const eval::StoreView& s, double rel_cut, size_t max_models, int threads) {
  LawFile L;
  L.n = D.n; L.p = D.p; L.rel_cut = rel_cut; L.n_store = s.size;
  L.ybar = eval::ybar(D); L.sy = eval::sy(D); L.a0 = D.a0; L.b0 = D.b0;
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
  // conjugate parameters per kept model: independent, threaded, stored by index (no order dependence)
  L.models.resize(keep.size()); L.w.resize(keep.size());
  std::vector<double> dF(keep.size());
#pragma omp parallel for schedule(dynamic, 256) num_threads(std::max(1, threads))
  for (long q = 0; q < (long)keep.size(); ++q) {
    const size_t i = keep[q];
    eval::ModelPost mp = eval::model_post(D, s.model(i));
    dF[q] = std::fabs(mp.F - s.v[i]);
    mp.F = s.v[i];
    L.models[q] = std::move(mp);
    L.w[q] = (double)(std::exp((long double)(s.v[i] - sm.vmax)) / kept);
  }
  for (double x : dF) L.max_abs_dF = std::max(L.max_abs_dF, x);
  std::vector<int32_t> cs;
  for (auto& mp : L.models) cs.insert(cs.end(), mp.S.begin(), mp.S.end());
  std::sort(cs.begin(), cs.end()); cs.erase(std::unique(cs.begin(), cs.end()), cs.end());
  for (int32_t j : cs) {
    L.cols.push_back(j); L.cols_orig.push_back(D.orig[j]);
    L.cols_xbar.push_back(eval::xbar(D, j)); L.cols_xsd.push_back(eval::xsd(D, j));
  }
  return L;
}

eval::Law to_eval_law(const LawFile& L, const std::string& name) {
  eval::Law out; out.name = name; out.dropped_mass = L.dropped_mass; out.store_law = true;
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

std::string write_law(const LawFile& L, const std::string& path, int n_draws, uint32_t draw_seed, uint32_t mode) {
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
  meta["schema"] = ("smcbvs4.law/1");
  meta["label"] = "truncated approximation of the store BMA";   // Sol F9-b
  meta["truncation"] = "models with relative weight >= rel_cut (at most max_models); dropped_mass = summed omitted relative mass; d_H error <= sqrt(dropped_mass)";
  meta["n"] = (L.n); meta["p"] = (L.p); meta["M"] = ((int64_t)M); meta["C"] = ((int64_t)C);
  meta["rel_cut"] = (L.rel_cut); meta["vmax"] = (L.vmax); meta["logZ_T"] = (L.logZ_T);
  meta["dropped_mass"] = (L.dropped_mass); meta["n_store"] = (eval::hex_u64(L.n_store));
  meta["ybar"] = (L.ybar); meta["sy"] = (L.sy); meta["a0"] = (L.a0); meta["b0"] = (L.b0); meta["max_abs_dF"] = (L.max_abs_dF);
  for (auto& kv : L.meta_extra.items()) meta[kv.first] = kv.second;
  meta["binary"] = binary_block(); meta["kind"] = "law"; meta["mode"] = fmt::mode_name(mode);   // v0.1.2 §5.3; mode of the fit (MINOR-3)
  fmt::Writer W(fmt::K_LAW, mode);
  W.add("model_ptr", mptr); W.add("model_idx", midx);
  W.add("F", F); W.add("w", w);
  W.add("logm", logm); W.add("Q", Q);
  W.add("alpha_n", an); W.add("beta_n", bn);
  W.add("route", route);
  W.add("theta_bar", th);
  W.add("LH_ptr", lptr); W.add("LH", LH);
  W.add("cols", L.cols); W.add("cols_orig", L.cols_orig);
  W.add("cols_xbar", L.cols_xbar); W.add("cols_xsd", L.cols_xsd);
  // draws stored sparsely (D-17 item 3): draw d's coefficients are draw_b[draw_ptr[d] .. draw_ptr[d+1]) on model draw_model[d]
  std::vector<int32_t> dm; std::vector<double> da, dv, db; std::vector<int64_t> dptr;
  if (n_draws > 0) {
    eval::Law el = to_eval_law(L);
    const std::vector<double> cum = eval::cumulative_weights(el);
    dm.resize(n_draws); da.resize(n_draws); dv.resize(n_draws); dptr.assign((size_t)n_draws + 1, 0);
    for (int d = 0; d < n_draws; ++d) {
      eval::ParamDraw pd = eval::draw_params(el, cum, draw_seed, 0, (uint32_t)d);
      dm[d] = pd.comp; da[d] = pd.a; dv[d] = pd.v;
      db.insert(db.end(), pd.b.begin(), pd.b.end());
      dptr[d + 1] = (int64_t)db.size();
    }
    W.add("draw_model", dm); W.add("draw_a", da); W.add("draw_v", dv); W.add("draw_ptr", dptr); W.add("draw_b", db);
    Json dj = Json::object(); dj["n"] = (n_draws); dj["seed"] = ((int64_t)draw_seed); dj["role"] = ("POST"); dj["layout"] = "sparse";
    meta["draws"] = (dj);
  } else {
    meta["draws"] = (Json());
  }
  W.add_json("meta", meta);
  return W.write(path);
}

LawFile read_law(const std::string& path, std::string* content_hash) {
  fmt::Reader B(path);
  if (content_hash) *content_hash = B.content_hash();
  if (B.kind() != fmt::K_LAW) throw Error(Status::invalid_input, path + ": not a law.bin (kind != 7)");
  Json meta = B.json("meta");
  if (eval::jstr_or(meta, "schema", "") != "smcbvs4.law/1") throw Error(Status::invalid_input, path + ": unknown law schema");
  LawFile L;
  L.n = (int32_t)meta.at("n").num(); L.p = (int32_t)meta.at("p").num();
  L.rel_cut = meta.at("rel_cut").num(); L.vmax = meta.at("vmax").num(); L.logZ_T = meta.at("logZ_T").num();
  L.dropped_mass = meta.at("dropped_mass").num(); L.n_store = eval::ju64_or(meta, "n_store", 0);
  L.ybar = meta.at("ybar").num(); L.sy = meta.at("sy").num(); L.a0 = meta.at("a0").num(); L.b0 = meta.at("b0").num();
  L.max_abs_dF = eval::jnum_or(meta, "max_abs_dF", NAN);
  const size_t M = (size_t)meta.at("M").num();
  uint64_t c;
  const int64_t* mptr = B.get<int64_t>("model_ptr", &c); if (c != M + 1) throw Error(Status::invalid_input, "law.bin: model_ptr");
  const int32_t* midx = B.get<int32_t>("model_idx", &c);
  if ((uint64_t)mptr[M] != c) throw Error(Status::invalid_input, "law.bin: model_idx size");
  const double *F = B.get<double>("F"), *w = B.get<double>("w"), *logm = B.get<double>("logm"),
               *Q = B.get<double>("Q"), *an = B.get<double>("alpha_n"), *bn = B.get<double>("beta_n"),
               *th = B.get<double>("theta_bar"), *LH = B.get<double>("LH");
  const uint8_t* route = B.get<uint8_t>("route");
  const int64_t* lptr = B.get<int64_t>("LH_ptr");
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
  const int32_t* cols = B.get<int32_t>("cols", &c);
  L.cols.assign(cols, cols + c);
  const int32_t* co = B.get<int32_t>("cols_orig"); L.cols_orig.assign(co, co + c);
  const double* cx = B.get<double>("cols_xbar"); L.cols_xbar.assign(cx, cx + c);
  const double* cs = B.get<double>("cols_xsd"); L.cols_xsd.assign(cs, cs + c);
  return L;
}

Json run(const Json& a) {
  auto t0 = std::chrono::steady_clock::now();
  Json rec = Json::object();
  rec["schema"] = "smcbvs4.post/1";
  const std::string fitp = eval::io::arg_str(a, "fit", ""), datap = eval::io::arg_str(a, "data", ""), out = eval::io::out_bin(a, "");
  if (fitp.empty() || datap.empty() || out.empty()) throw Error(Status::invalid_input, "post: --fit, --data and --out are required");
  const double rel = eval::io::arg_num(a, "rel_cut", 1e-12);
  const size_t maxm = (size_t)eval::io::arg_num(a, "max_models", 1000000);
  const int nd = (int)eval::io::arg_num(a, "draws", 0);
  const uint32_t seed = (uint32_t)eval::io::arg_num(a, "seed", 1);
  std::string dh;
  const Data D = prep::load_data(datap, &dh);
  eval::io::FitFile ff; eval::io::load_fit(fitp, ff);
  // GUARD-W (PR12 MINOR-4): no law from a fit that is not completed; a missing status is invalid input
  if (!eval::jfind(ff.meta, "status") || ff.meta.at("status").type() != Json::STR) throw Error(Status::invalid_input, "fit.bin: meta.status missing");
  if (ff.meta.at("status").str() != "completed") {
    rec["fit_status"] = ff.meta.at("status").str(); rec["reason"] = "fit not completed: no law"; rec["status"] = "completed";
    return rec;
  }
  LawFile L = build_law(D, ff.top, rel, maxm, (int)eval::io::arg_num(a, "threads", 1));
  Json inp = Json::object(); inp["fit.bin"] = ff.bin->content_hash(); inp["data.bin"] = dh;
  L.meta_extra["inputs"] = inp;
  const std::string h = write_law(L, out, nd, seed, ff.bin->mode());
  rec["inputs"] = inp;
  Json o = Json::object(); o[out.substr(out.find_last_of('/') + 1)] = h; rec["outputs"] = o;
  rec["M"] = (uint64_t)L.models.size(); rec["dropped_mass"] = L.dropped_mass; rec["logZ_T"] = L.logZ_T;
  rec["max_abs_dF"] = L.max_abs_dF;
  rec["wall_s"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  rec["status"] = "completed";
  return rec;
}

}  // namespace v4::post
