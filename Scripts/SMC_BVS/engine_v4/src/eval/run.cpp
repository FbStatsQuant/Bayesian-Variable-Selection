// run.cpp -- the `eval` command (ENGINEERING_SPEC §1 row 6): fit.bin + data.bin + truth.json → record + eval.bin;
// and the competitor path (same metrics for a competitor record, EXPERIMENT_PLAN §4).
#include <algorithm>
#include <chrono>
#include <cmath>
#include <map>

#include "io.h"
#include "v4/post.h"
#include "v4/prep.h"
#include "v4/sha256.h"

namespace v4::eval {

namespace {

Model read_model_section(const fmt::Reader& B, const std::string& name) {
  uint64_t c = 0; const int32_t* p = B.get<int32_t>(name, &c);
  Model S(p, p + c);
  if (!is_sorted_unique(S)) throw Error(Status::invalid_input, "fit.bin: " + name + " not sorted/unique");
  return S;
}
std::vector<double> read_f64(const fmt::Reader& B, const std::string& name, uint64_t expect) {
  uint64_t c = 0; const double* p = B.get<double>(name, &c);
  if (expect && c != expect) throw Error(Status::invalid_input, "fit.bin: section " + name + " has wrong length");
  return std::vector<double>(p, p + c);
}
Model internal_model(const std::vector<int32_t>& orig1, const Data& D, int64_t* n_dropped) {
  Model S; if (n_dropped) *n_dropped = 0;
  for (int32_t o : orig1) { int32_t j = internal_of(D, o); if (j < 0) { if (n_dropped) ++*n_dropped; } else S.push_back(j); }
  std::sort(S.begin(), S.end());
  S.erase(std::unique(S.begin(), S.end()), S.end());
  return S;
}
Json ratio(const Json& a, const Json& o, const char* sec, const char* key) {
  const Json* x = jfind(a, sec); const Json* y = jfind(o, sec);
  if (!x || !y) return Json();
  return Json(jnum_or(*x, key, NAN) / jnum_or(*y, key, NAN));
}
DistOpts dist_opts(const Json& a, const Truth& T) {
  DistOpts o;
  o.seed = (uint32_t)io::arg_num(a, "seed", (double)(uint32_t)(T.seed & 0xffffffffu));
  o.n_draws = (int)io::arg_num(a, "n_draws", 10000);
  o.n_x = (int)io::arg_num(a, "n_x", 4000);
  o.n_gh = (int)io::arg_num(a, "n_gh", 64);
  o.n_test = (int)io::arg_num(a, "n_test", 10000);
  o.threads = (int)io::arg_num(a, "threads", 1);
  if (o.n_draws < 1 || o.n_x < 2 || o.n_gh < 8 || o.n_test < 2 || o.threads < 1) throw Error(Status::invalid_input, "eval: bad Monte Carlo sizes");
  return o;
}
Json params_json(const DistOpts& o, double rel_cut, const std::string& rows) {
  Json p = Json::object();
  p["seed"] = (int64_t)o.seed; p["n_draws"] = o.n_draws; p["n_x"] = o.n_x; p["n_gh"] = o.n_gh; p["n_test"] = o.n_test;
  p["threads"] = o.threads; p["rel_cut"] = rel_cut; p["test_rows"] = rows;
  return p;
}
// Distribution block for a list of objects (null entries are recorded as null) + the oracle Π(·|S0) and ratios.
Json dist_block(const std::vector<std::pair<std::string, const Law*>>& objs, const Law& oracle, const Truth& T, int32_t n,
                const DistOpts& o, std::map<std::string, std::vector<double>>* draws, std::string* rows) {
  std::vector<int32_t> cols;
  for (auto& ob : objs) if (ob.second) for (auto& c : ob.second->comps) cols.insert(cols.end(), c.orig.begin(), c.orig.end());
  for (auto& c : oracle.comps) cols.insert(cols.end(), c.orig.begin(), c.orig.end());
  const DistShared sh = make_shared_draws(T, cols, o);
  if (rows) *rows = sh.source;
  Json dist = Json::object(), rat = Json::object();
  std::vector<double> dO;
  Json jO = dist_metrics(oracle, T, n, o, sh, 3, &dO);
  if (draws) (*draws)["oracle"] = dO;
  uint32_t oid = 0;
  for (auto& ob : objs) {
    const uint32_t id = (ob.first == "H") ? 0 : (ob.first == "M" ? 1 : (ob.first == "T" ? 2 : 4 + oid++));
    if (!ob.second) { dist[ob.first] = Json(); rat[ob.first] = Json(); continue; }
    std::vector<double> dh;
    Json j = dist_metrics(*ob.second, T, n, o, sh, id, &dh);
    if (draws) (*draws)[ob.first] = dh;
    Json r = Json::object();
    r["plugin_h2"] = ratio(j, jO, "plugin", "h2");
    r["pred_error"] = ratio(j, jO, "plugin", "pred_error");
    r["predictive_h2"] = ratio(j, jO, "predictive", "h2");
    r["kl"] = ratio(j, jO, "predictive", "kl");
    r["test_mse"] = ratio(j, jO, "test", "mse");
    dist[ob.first] = j; rat[ob.first] = r;
  }
  dist["oracle"] = jO;
  dist["ratio_to_oracle"] = rat;
  return dist;
}

}  // namespace

Json run(const Json& a) {
  if (jfind(a, "competitor")) return run_competitor(a);
  auto t0 = std::chrono::steady_clock::now();
  Json rec = Json::object();
  rec["schema"] = "smcbvs4.eval/1";
  const std::string fitp = io::arg_str(a, "fit", ""), datap = io::arg_str(a, "data", ""), truthp = io::arg_str(a, "truth", "");
  const std::string out = io::out_bin(a, "");
  if (fitp.empty() || datap.empty() || truthp.empty() || out.empty()) throw Error(Status::invalid_input, "eval: --fit, --data, --truth and --out are required");
  std::string data_hash;
  const Data D = prep::load_data(datap, &data_hash);
  io::FitFile ff; io::load_fit(fitp, ff);
  const Truth T = truth_from_json(read_json_file(truthp));
  const fmt::Reader& FB = *ff.bin;
  const DistOpts o = dist_opts(a, T);
  const double rel_cut = io::arg_num(a, "rel_cut", 1e-12);

  Json inp = Json::object();
  inp["fit.bin"] = FB.content_hash(); inp["data.bin"] = data_hash; inp["truth.json"] = sha256_file(truthp);
  Json fit = Json::object();
  fit["mode"] = fmt::mode_name(FB.mode());
  fit["meta"] = ff.meta;
  rec["fit"] = fit;
  const std::string fst = jstr_or(ff.meta, "status", "completed");
  rec["fit_status"] = fst;
  if (fst != "completed") {   // GUARD-W: no estimate fields for an incomplete fit; the fit stays in the denominator
    rec["inputs"] = inp;
    rec["reason"] = "fit not completed: no metrics";
    rec["status"] = "completed";
    return rec;
  }
  Json data = Json::object(); data["n"] = D.n; data["p"] = D.p; data["p_raw"] = D.p_raw; data["K"] = D.K;
  rec["data"] = data;

  // ---------------- selection
  int64_t s0_dropped = 0;
  const Model S0 = internal_model(T.S0, D, &s0_dropped);
  const ModelPost mp0 = model_post(D, S0);                       // F(S0) scored directly
  Model hpm; double F_hpm;
  if (FB.has("hpm_S")) { hpm = read_model_section(FB, "hpm_S"); F_hpm = jnum_or(ff.meta, "hpm_F", NAN); }
  else { hpm = ff.top.model(0); F_hpm = ff.top.v[0]; }
  const ModelPost mph = model_post(D, hpm);
  if (!std::isfinite(F_hpm)) F_hpm = mph.F;
  const std::vector<double> pip_eq = read_f64(FB, "pip_eq", (uint64_t)D.p);
  Model mpm; for (int32_t j = 0; j < D.p; ++j) if (pip_eq[j] > 0.5) mpm.push_back(j);   // core/v3_run.R:163
  Json sel = selection_metrics(S0, hpm, F_hpm, mpm, mp0.F, D);
  sel["S0_dropped_columns"] = s0_dropped;
  sel["F_hpm_recomputed_abs_diff"] = std::fabs(mph.F - F_hpm);
  const long i0 = store_find(ff.top, S0, D.zob.hash(S0));
  sel["S0_in_store"] = i0 >= 0; sel["S0_store_rank"] = (int64_t)i0;
  sel["F_S0_ledger_abs_diff"] = i0 >= 0 ? Json(std::fabs(ff.top.v[i0] - mp0.F)) : Json();
  for (const char* k : {"hpm_ev", "hpm_phase", "hpm_mech", "hpm_phi", "local_certified", "ls0_moves", "ls0_first_scan",
                        "mode_size", "start_mode_size", "certified_screening_coverage", "hpm_before_local_F"})
    if (const Json* v = jfind(ff.meta, k)) sel[std::string("prov_") + k] = *v;
  rec["selection"] = sel;

  // ---------------- store mass and the law Π̂^𝒯
  const StoreMass sm = store_mass(ff.top, rel_cut);
  post::LawFile LF;
  const std::string lawp = io::arg_str(a, "law", "");
  if (!lawp.empty()) { std::string h; LF = post::read_law(lawp, &h); inp["law.bin"] = h; }
  else LF = post::build_law(D, ff.top, rel_cut);
  const double logZ = jnum_or(ff.meta, "logZ", NAN);
  Json st = Json::object();
  st["size"] = (uint64_t)ff.top.size; st["logZ_T"] = sm.logZ_T;
  st["pi_T_hat"] = std::exp(sm.logZ_T - logZ);                 // π̂(𝒯) = Σ_𝒯 e^F / Ẑ (ratio of estimates)
  st["law_models"] = (uint64_t)LF.models.size(); st["dropped_mass"] = LF.dropped_mass;
  st["max_abs_dF_law"] = LF.max_abs_dF;
  rec["store"] = st;

  // ---------------- PIPs
  Json pip = Json::object();
  pip["eq"] = pip_metrics(pip_eq, S0, D.p);
  std::vector<double> pip_Z, pip_T;
  if (FB.has("pip_Z")) { pip_Z = read_f64(FB, "pip_Z", D.p); pip["Z"] = pip_metrics(pip_Z, S0, D.p); }
  if (FB.has("pip_T")) { pip_T = read_f64(FB, "pip_T", D.p); pip["T"] = pip_metrics(pip_T, S0, D.p); }
  if (!pip_Z.empty()) { double m = 0; for (int32_t j = 0; j < D.p; ++j) m = std::max(m, std::fabs(pip_Z[j] - pip_eq[j])); pip["max_abs_Z_minus_eq"] = m; }
  if (!pip_T.empty()) {
    double m = 0; for (int32_t j = 0; j < D.p; ++j) m = std::max(m, std::fabs(pip_T[j] - pip_eq[j]));
    const double tgt = 0.01 + (1.0 - std::min(1.0, std::exp(sm.logZ_T - logZ)));   // §0-v2.3
    pip["max_abs_eq_minus_T"] = m; pip["eq_T_target"] = tgt; pip["eq_T_target_met"] = m <= tgt;
  }
  if (FB.has("pip_r")) {
    const fmt::SectionEntry& e = FB.entry("pip_r");
    if (e.ndim != 2 || e.dims[1] != (uint64_t)D.p) throw Error(Status::invalid_input, "fit.bin: pip_r must be Rp × p");
    pip["island_spread"] = pip_island_spread(FB.get<double>("pip_r"), (int32_t)e.dims[0], D.p, 0.005);
  }
  rec["pip"] = pip;

  // ---------------- evidence
  std::vector<double> lr;
  if (FB.has("logZ_r")) lr = read_f64(FB, "logZ_r", 0);
  Json ev = evidence_metrics(logZ, lr, sm.logZ_T);
  Json occ = Json::object();
  if (FB.has("occ_top")) {   // terminal occupancy of the top-1000 store models (D-13), pooled and per island
    uint64_t c = 0; const uint64_t* oc = FB.get<uint64_t>("occ_top", &c);
    const uint64_t tot = (uint64_t)jnum_or(ff.meta, "occ_total", 0);
    for (size_t M : {1, 10, 100, 1000}) {
      if (M > c || M > ff.top.size) continue;
      uint64_t s = 0; for (size_t i = 0; i < M; ++i) s += oc[i];
      occ["M" + std::to_string(M)] = logZ_occ(ff.top.v, M, s, tot);
    }
    if (FB.has("occ_top_r")) {
      const fmt::SectionEntry& e = FB.entry("occ_top_r");
      const uint64_t* ocr = FB.get<uint64_t>("occ_top_r");
      const size_t R = e.dims[0], W = e.dims[1];
      const uint64_t tr = (uint64_t)jnum_or(ff.meta, "occ_total_r", 0);
      Json sdj = Json::object();
      for (size_t M : {1, 10, 100, 1000}) {
        if (M > W || M > ff.top.size) continue;
        std::vector<double> v;
        for (size_t r = 0; r < R; ++r) { uint64_t s = 0; for (size_t i = 0; i < M; ++i) s += ocr[r * W + i]; v.push_back(logZ_occ(ff.top.v, M, s, tr)); }
        double m = 0; for (double x : v) m += x; m /= v.size();
        double ss = 0; for (double x : v) ss += (x - m) * (x - m);
        sdj["M" + std::to_string(M)] = v.size() > 1 ? std::sqrt(ss / (v.size() - 1)) : NAN;
      }
      occ["sd_over_islands"] = sdj;
    }
  } else if (const Json* z = jfind(ff.meta, "logZ_occ")) {
    occ = *z;   // computed by merge (pass-through)
  }
  ev["logZ_occ"] = occ;
  rec["evidence"] = ev;

  // ---------------- distribution objects: Π̂^H, Π̂^M, Π̂^𝒯, oracle Π(·|S0)
  Law LH; LH.name = "H"; LH.comps.push_back(component_from_post(D, mph, 1.0));
  Law LO; LO.name = "oracle"; LO.comps.push_back(component_from_post(D, mp0, 1.0));
  Law LT = post::to_eval_law(LF, "T");
  Law LM; const bool have_M = mpm.size() <= (size_t)D.K;
  if (have_M) { LM.name = "M"; LM.comps.push_back(component_from_post(D, model_post(D, mpm), 1.0)); }
  std::map<std::string, std::vector<double>> dr;
  std::string rows;
  rec["dist"] = dist_block({{"H", &LH}, {"M", have_M ? &LM : nullptr}, {"T", &LT}}, LO, T, D.n, o, &dr, &rows);
  rec["params"] = params_json(o, rel_cut, rows);

  // ---------------- cost (the driver's sacct summary, tools/slurm/p1m_cost.py, + fit timings)
  Json cost = Json::object();
  if (const Json* t = jfind(ff.meta, "timings")) cost["fit_timings"] = *t;
  const std::string costp = io::arg_str(a, "cost", "");
  if (!costp.empty()) { cost["sacct"] = read_json_file(costp); inp["cost.json"] = sha256_file(costp); }
  cost["eval_wall_s"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  rec["cost"] = cost;
  rec["inputs"] = inp;

  // ---------------- eval.bin (arrays)
  fmt::Writer W(fmt::K_EVAL, FB.mode());
  for (auto& kv : dr) W.add("dH_draws_" + kv.first, kv.second);
  W.add_json("meta", rec);
  Json outs = Json::object(); outs[out.substr(out.find_last_of('/') + 1)] = W.write(out);
  rec["outputs"] = outs;
  rec["status"] = "completed";
  return rec;
}

// ------------------------------------------------------------------------------------------------ competitors
Json run_competitor(const Json& a) {
  auto t0 = std::chrono::steady_clock::now();
  Json rec = Json::object();
  rec["schema"] = "smcbvs4.eval_competitor/1";
  const std::string cp = io::arg_str(a, "competitor", ""), datap = io::arg_str(a, "data", ""), truthp = io::arg_str(a, "truth", "");
  if (cp.empty() || datap.empty() || truthp.empty()) throw Error(Status::invalid_input, "eval --competitor: --competitor, --data and --truth are required");
  const Json C = read_json_file(cp);
  if (jstr_or(C, "schema", "") != "smcbvs4.competitor/1") throw Error(Status::invalid_input, cp + ": not a smcbvs4.competitor/1 record");
  std::string data_hash;
  const Data D = prep::load_data(datap, &data_hash);
  const Truth T = truth_from_json(read_json_file(truthp));
  const DistOpts o = dist_opts(a, T);
  Json inp = Json::object(); inp["competitor"] = sha256_file(cp); inp["data.bin"] = data_hash; inp["truth.json"] = sha256_file(truthp);
  rec["inputs"] = inp;
  rec["method"] = jstr_or(C, "method", "?"); rec["package"] = jstr_or(C, "package", ""); rec["version"] = jstr_or(C, "version", "");
  rec["competitor_wall_s"] = jnum_or(C, "wall_s", NAN);
  const std::string cst = jstr_or(C, "status", "failed");
  rec["competitor_status"] = cst;
  if (cst != "completed") { rec["reason"] = jstr_or(C, "reason", "competitor did not complete"); rec["status"] = "completed"; return rec; }

  auto orig_list = [](const Json& j) { std::vector<int32_t> v; for (auto& e : j.elems()) v.push_back((int32_t)e.i64()); return v; };
  int64_t s0_dropped = 0, sel_dropped = 0;
  const Model S0 = internal_model(T.S0, D, &s0_dropped);
  const Model Ssel = internal_model(orig_list(C.at("selected")), D, &sel_dropped);
  const ModelPost mp0 = model_post(D, S0);
  const double F_sel = Ssel.size() <= (size_t)D.K ? model_post(D, Ssel).F : NAN;
  // PIPs (sparse: idx/val on original columns, default elsewhere)
  std::vector<double> pip;
  if (const Json* P = jfind(C, "pip")) if (!P->is_null()) {
    pip.assign(D.p, jnum_or(*P, "default", 0.0));
    const Json& idx = P->at("idx"); const Json& val = P->at("val");
    if (idx.size() != val.size()) throw Error(Status::invalid_input, "competitor pip: idx and val lengths differ");
    for (size_t i = 0; i < idx.size(); ++i) { int32_t j = internal_of(D, (int32_t)idx.at(i).i64()); if (j >= 0) pip[j] = val.at(i).num(); }
  }
  Model mpm = Ssel;
  if (!pip.empty()) { mpm.clear(); for (int32_t j = 0; j < D.p; ++j) if (pip[j] > 0.5) mpm.push_back(j); }
  Json sel = selection_metrics(S0, Ssel, F_sel, mpm, mp0.F, D);
  sel["selected_dropped_columns"] = sel_dropped;
  rec["selection"] = sel;
  if (!pip.empty()) { Json pj = Json::object(); pj["C"] = pip_metrics(pip, S0, D.p); rec["pip"] = pj; }
  // predictive object
  Law LC; LC.name = "C"; bool have = false;
  if (const Json* Pd = jfind(C, "predictive")) if (!Pd->is_null()) {
    const std::string ty = jstr_or(*Pd, "type", "");
    if (ty == "gaussian") {
      std::vector<std::pair<int32_t, double>> bc;
      const Json& idx = Pd->at("idx"); const Json& cf = Pd->at("coef");
      if (idx.size() != cf.size()) throw Error(Status::invalid_input, "competitor predictive: idx and coef lengths differ");
      for (size_t i = 0; i < idx.size(); ++i) if (cf.at(i).num() != 0) bc.emplace_back((int32_t)idx.at(i).i64(), cf.at(i).num());
      std::sort(bc.begin(), bc.end());
      std::vector<int32_t> oi; std::vector<double> ov;
      for (auto& x : bc) { if (!oi.empty() && oi.back() == x.first) throw Error(Status::invalid_input, "competitor predictive: duplicate idx"); oi.push_back(x.first); ov.push_back(x.second); }
      LC.comps.push_back(component_gaussian(oi, ov, Pd->at("intercept").num(), Pd->at("sigma2").num(), 1.0));
      have = true;
    } else if (ty == "model_law") {   // Q(S) with our conjugate kernels: QΠ = Σ Q(S) Π(·|S, D_n) (STATEMENT §2)
      const Json& ms = Pd->at("models"); const Json& ws = Pd->at("weights");
      if (ms.size() != ws.size() || ms.size() == 0) throw Error(Status::invalid_input, "competitor model_law: bad sizes");
      double wsum = 0; for (auto& w : ws.elems()) wsum += w.num();
      for (size_t m = 0; m < ms.size(); ++m) {
        Model S = internal_model(orig_list(ms.at(m)), D, nullptr);
        if (S.size() > (size_t)D.K) continue;
        LC.comps.push_back(component_from_post(D, model_post(D, S), ws.at(m).num() / wsum));
      }
      double w2 = 0; for (auto& c : LC.comps) w2 += c.w;
      for (auto& c : LC.comps) c.w /= w2;
      LC.dropped_mass = 1.0 - w2;
      have = !LC.comps.empty();
    } else throw Error(Status::invalid_input, "competitor predictive: unknown type " + ty);
  }
  Law LO; LO.name = "oracle"; LO.comps.push_back(component_from_post(D, mp0, 1.0));
  std::string rows;
  rec["dist"] = dist_block({{"C", have ? &LC : nullptr}}, LO, T, D.n, o, nullptr, &rows);
  rec["params"] = params_json(o, 0, rows);
  Json cost = Json::object(); cost["eval_wall_s"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  rec["cost"] = cost;
  rec["status"] = "completed";
  return rec;
}

}  // namespace v4::eval
