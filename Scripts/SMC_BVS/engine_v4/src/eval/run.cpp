// run.cpp -- the `eval` command (ENGINEERING_SPEC §1 row 6): fit.bin + data.bin + truth.json → <out>.json + <out>.bin.
#include <algorithm>
#include <chrono>
#include <cmath>

#include "io.h"
#include "v4/post.h"

namespace v4::eval {

namespace {

Model read_model_section(const wp5prov::BinReader& B, const std::string& name) {
  uint64_t c = 0; const int32_t* p = B.ptr<int32_t>(name, wp5prov::DT_I32, &c);
  return Model(p, p + c);
}
std::vector<double> read_f64(const wp5prov::BinReader& B, const std::string& name, uint64_t expect) {
  uint64_t c = 0; const double* p = B.ptr<double>(name, wp5prov::DT_F64, &c);
  if (expect && c != expect) throw Error(Status::invalid_input, "fit.bin: section " + name + " has wrong length");
  return std::vector<double>(p, p + c);
}
Model internal_S0(const Truth& T, const EvalData& D, int64_t* n_dropped) {
  Model S; *n_dropped = 0;
  for (int32_t o : T.S0) { int32_t j = D.internal_of(o); if (j < 0) ++*n_dropped; else S.push_back(j); }
  std::sort(S.begin(), S.end());
  return S;
}
Json ratio(const Json& a, const Json& o, const char* sec, const char* key) {
  const Json* x = a.find(sec); const Json* y = o.find(sec);
  if (!x || !y) return Json();
  double u = x->num_or(key, NAN), v = y->num_or(key, NAN);
  return Json(u / v);
}

}  // namespace

int run(int argc, char** argv) {
  std::string out = "eval";
  Json rec = Json::object();
  rec.set("schema", "smcbvs4.eval/1"); rec.set("command", "eval");
  try {
    auto t0 = std::chrono::steady_clock::now();
    auto a = io::parse_args(argc, argv, 1);
    out = io::arg_or(a, "out", "eval");
    const std::string fitp = io::arg_or(a, "fit", ""), datap = io::arg_or(a, "data", ""), truthp = io::arg_or(a, "truth", "");
    if (fitp.empty() || datap.empty() || truthp.empty()) throw Error(Status::invalid_input, "eval: --fit, --data and --truth are required");
    io::DataFile df; io::load_data(datap, df);
    io::FitFile ff; io::load_fit(fitp, ff);
    const Json truthj = Json::parse_file(truthp);
    const Truth T = truth_from_json(truthj);
    const EvalData& D = df.D;
    const wp5prov::BinReader& FB = *ff.bin;

    DistOpts o;
    o.seed = (uint32_t)std::stoul(io::arg_or(a, "seed", std::to_string((uint32_t)(T.seed & 0xffffffffu))));
    o.n_draws = std::stoi(io::arg_or(a, "n-draws", "10000"));
    o.n_x = std::stoi(io::arg_or(a, "n-x", "4000"));
    o.n_gh = std::stoi(io::arg_or(a, "n-gh", "64"));
    o.n_test = std::stoi(io::arg_or(a, "n-test", "10000"));
    o.threads = std::stoi(io::arg_or(a, "threads", "1"));
    const double rel_cut = std::stod(io::arg_or(a, "rel-cut", "1e-12"));

    Json inp = Json::object();
    inp.set("fit.bin", FB.content_hash()); inp.set("data.bin", df.bin->content_hash()); inp.set("truth.json", io::file_sha256(truthp));
    rec.set("inputs", inp);
    Json prm = Json::object();
    prm.set("seed", (int64_t)o.seed); prm.set("n_draws", o.n_draws); prm.set("n_x", o.n_x); prm.set("n_gh", o.n_gh);
    prm.set("n_test", o.n_test); prm.set("threads", o.threads); prm.set("rel_cut", rel_cut);
    rec.set("params", prm);
    Json fit = Json::object();
    fit.set("mode", (int64_t)FB.header().mode);
    fit.set("meta", ff.meta);
    rec.set("fit", fit);
    const std::string fst = ff.meta.str_or("status", "completed");
    if (fst != "completed") {   // GUARD-W: no estimate fields for an incomplete fit; the fit stays in the denominator
      rec.set("fit_status", fst);
      return io::finish(out + ".json", rec, Status::completed, "fit not completed: no metrics");
    }
    rec.set("fit_status", fst);
    Json data = Json::object(); data.set("n", D.n); data.set("p", D.p); data.set("p_raw", D.p_raw); data.set("K", D.K);
    rec.set("data", data);

    // ---------------- selection
    int64_t s0_dropped = 0;
    const Model S0 = internal_S0(T, D, &s0_dropped);
    const ModelPost mp0 = model_post(D, S0);                       // F(S0) scored directly
    Model hpm; double F_hpm;
    if (FB.has("hpm_S")) { hpm = read_model_section(FB, "hpm_S"); F_hpm = ff.meta.num_or("hpm_F", NAN); }
    else { hpm = ff.top.model(0); F_hpm = ff.top.v[0]; }
    const ModelPost mph = model_post(D, hpm);
    if (!std::isfinite(F_hpm)) F_hpm = mph.F;
    const std::vector<double> pip_eq = read_f64(FB, "pip_eq", (uint64_t)D.p);
    Model mpm; for (int32_t j = 0; j < D.p; ++j) if (pip_eq[j] > 0.5) mpm.push_back(j);   // core/v3_run.R:163
    Json sel = selection_metrics(S0, hpm, F_hpm, mpm, mp0.F, D);
    sel.set("S0_dropped_columns", s0_dropped);
    sel.set("F_hpm_recomputed_abs_diff", std::fabs(mph.F - F_hpm));
    const uint64_t h0 = zobrist_hash(S0, D.p);
    const long i0 = store_find(ff.top, S0, h0);
    sel.set("S0_in_store", i0 >= 0); sel.set("S0_store_rank", (int64_t)i0);
    sel.set("F_S0_ledger_abs_diff", i0 >= 0 ? Json(std::fabs(ff.top.v[i0] - mp0.F)) : Json());
    for (const char* k : {"hpm_ev", "hpm_phase", "hpm_mech", "hpm_phi", "local_certified", "ls0_moves", "ls0_first_scan",
                          "mode_size", "start_mode_size", "certified_screening_coverage", "hpm_before_local_F"})
      if (const Json* v = ff.meta.find(k)) sel.set(std::string("prov_") + k, *v);
    rec.set("selection", sel);

    // ---------------- store mass and the law Π̂^𝒯
    StoreMass sm = store_mass(ff.top, rel_cut);
    post::LawFile LF;
    const std::string lawp = io::arg_or(a, "law", "");
    if (!lawp.empty()) { LF = post::read_law(lawp); inp.set("law.bin", wp5prov::BinReader(lawp).content_hash()); rec.set("inputs", inp); }
    else LF = post::build_law(D, ff.top, rel_cut);
    const double logZ = ff.meta.num_or("logZ", NAN);
    Json st = Json::object();
    st.set("size", (int64_t)ff.top.size); st.set("logZ_T", sm.logZ_T);
    st.set("pi_T_hat", std::exp(sm.logZ_T - logZ));                 // π̂(𝒯) = Σ_𝒯 e^F / Ẑ (ratio of estimates)
    st.set("law_models", (int64_t)LF.models.size()); st.set("dropped_mass", LF.dropped_mass);
    st.set("max_abs_dF_law", LF.max_abs_dF);
    rec.set("store", st);

    // ---------------- PIPs
    Json pip = Json::object();
    pip.set("eq", pip_metrics(pip_eq, S0, D.p));
    std::vector<double> pip_Z, pip_T;
    if (FB.has("pip_Z")) { pip_Z = read_f64(FB, "pip_Z", D.p); pip.set("Z", pip_metrics(pip_Z, S0, D.p)); }
    if (FB.has("pip_T")) { pip_T = read_f64(FB, "pip_T", D.p); pip.set("T", pip_metrics(pip_T, S0, D.p)); }
    if (!pip_Z.empty()) { double m = 0; for (int32_t j = 0; j < D.p; ++j) m = std::max(m, std::fabs(pip_Z[j] - pip_eq[j])); pip.set("max_abs_Z_minus_eq", m); }
    if (!pip_T.empty()) {
      double m = 0; for (int32_t j = 0; j < D.p; ++j) m = std::max(m, std::fabs(pip_T[j] - pip_eq[j]));
      const double tgt = 0.01 + (1.0 - std::min(1.0, std::exp(sm.logZ_T - logZ)));   // §0-v2.3
      pip.set("max_abs_eq_minus_T", m); pip.set("eq_T_target", tgt); pip.set("eq_T_target_met", m <= tgt);
    }
    if (FB.has("pip_r")) {
      const wp5prov::SectionEntry& e = FB.entry("pip_r");
      if (e.ndim != 2 || e.dims[1] != (uint64_t)D.p) throw Error(Status::invalid_input, "fit.bin: pip_r must be Rp × p");
      pip.set("island_spread", pip_island_spread(FB.ptr<double>("pip_r", wp5prov::DT_F64), (int32_t)e.dims[0], D.p, 0.005));
    }
    rec.set("pip", pip);

    // ---------------- evidence
    std::vector<double> lr;
    if (FB.has("logZ_r")) lr = read_f64(FB, "logZ_r", 0);
    Json ev = evidence_metrics(logZ, lr, sm.logZ_T);
    Json occ = Json::object();
    if (FB.has("occ_top")) {   // terminal occupancy of the top-1000 store models (D-13), pooled and per island
      uint64_t c = 0; const uint64_t* oc = FB.ptr<uint64_t>("occ_top", wp5prov::DT_U64, &c);
      const uint64_t tot = (uint64_t)ff.meta.num_or("occ_total", 0);
      for (size_t M : {1, 10, 100, 1000}) {
        if (M > c || M > ff.top.size) continue;
        uint64_t s = 0; for (size_t i = 0; i < M; ++i) s += oc[i];
        occ.set("M" + std::to_string(M), logZ_occ(ff.top.v, M, s, tot));
      }
      if (FB.has("occ_top_r")) {
        const wp5prov::SectionEntry& e = FB.entry("occ_top_r");
        const uint64_t* ocr = FB.ptr<uint64_t>("occ_top_r", wp5prov::DT_U64);
        const size_t R = e.dims[0], W = e.dims[1];
        const uint64_t tr = (uint64_t)ff.meta.num_or("occ_total_r", 0);
        Json sdj = Json::object();
        for (size_t M : {1, 10, 100, 1000}) {
          if (M > W || M > ff.top.size) continue;
          std::vector<double> v;
          for (size_t r = 0; r < R; ++r) { uint64_t s = 0; for (size_t i = 0; i < M; ++i) s += ocr[r * W + i]; v.push_back(logZ_occ(ff.top.v, M, s, tr)); }
          double m = 0; for (double x : v) m += x; m /= v.size();
          double ss = 0; for (double x : v) ss += (x - m) * (x - m);
          sdj.set("M" + std::to_string(M), v.size() > 1 ? std::sqrt(ss / (v.size() - 1)) : NAN);
        }
        occ.set("sd_over_islands", sdj);
      }
    } else if (const Json* z = ff.meta.find("logZ_occ")) {
      occ = *z;   // computed by merge (pass-through)
    }
    ev.set("logZ_occ", occ);
    rec.set("evidence", ev);

    // ---------------- distribution objects: Π̂^H, Π̂^M, Π̂^𝒯, oracle Π(·|S0)
    Law LH; LH.name = "H"; LH.comps.push_back(component_from_post(D, mph, 1.0));
    Law LO; LO.name = "oracle"; LO.comps.push_back(component_from_post(D, mp0, 1.0));
    Law LT = post::to_eval_law(LF, "T");
    Law LM; bool have_M = mpm.size() <= (size_t)D.K;
    if (have_M) { LM.name = "M"; LM.comps.push_back(component_from_post(D, model_post(D, mpm), 1.0)); }
    std::vector<int32_t> cols;
    for (const Law* L : {&LH, &LO, &LT, &LM}) for (auto& c : L->comps) cols.insert(cols.end(), c.orig.begin(), c.orig.end());
    const DistShared sh = make_shared_draws(T, cols, o);
    Json dist = Json::object();
    std::vector<double> dH_H, dH_M, dH_T, dH_O;
    Json jH = dist_metrics(LH, T, D.n, o, sh, 0, &dH_H);
    Json jM = have_M ? dist_metrics(LM, T, D.n, o, sh, 1, &dH_M) : Json();
    Json jT = dist_metrics(LT, T, D.n, o, sh, 2, &dH_T);
    Json jO = dist_metrics(LO, T, D.n, o, sh, 3, &dH_O);
    dist.set("H", jH); dist.set("M", jM); dist.set("T", jT); dist.set("oracle", jO);
    Json rat = Json::object();
    for (auto pr : {std::make_pair("H", &jH), std::make_pair("M", &jM), std::make_pair("T", &jT)}) {
      if (pr.second->is_null()) { rat.set(pr.first, Json()); continue; }
      Json r = Json::object();
      r.set("plugin_h2", ratio(*pr.second, jO, "plugin", "h2"));
      r.set("pred_error", ratio(*pr.second, jO, "plugin", "pred_error"));
      r.set("predictive_h2", ratio(*pr.second, jO, "predictive", "h2"));
      r.set("kl", ratio(*pr.second, jO, "predictive", "kl"));
      r.set("test_mse", ratio(*pr.second, jO, "test", "mse"));
      rat.set(pr.first, r);
    }
    dist.set("ratio_to_oracle", rat);
    rec.set("dist", dist);

    // ---------------- cost (pass-through of the driver's sacct summary + fit timings)
    Json cost = Json::object();
    if (const Json* t = ff.meta.find("timings")) cost.set("fit_timings", *t);
    const std::string costp = io::arg_or(a, "cost", "");
    if (!costp.empty()) { cost.set("sacct", Json::parse_file(costp)); inp.set("cost.json", io::file_sha256(costp)); rec.set("inputs", inp); }
    const double wall = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    cost.set("eval_wall_s", wall);
    rec.set("cost", cost);

    // ---------------- eval.bin (arrays)
    wp5prov::BinWriter W(wp5prov::K_EVAL, FB.header().mode);
    W.add_vec("dH_draws_H", wp5prov::DT_F64, dH_H); W.add_vec("dH_draws_T", wp5prov::DT_F64, dH_T); W.add_vec("dH_draws_oracle", wp5prov::DT_F64, dH_O);
    if (have_M) W.add_vec("dH_draws_M", wp5prov::DT_F64, dH_M);
    W.add_json("meta", rec.dump());
    const std::string h = W.write(out + ".bin");
    Json outs = Json::object(); outs.set(out + ".bin", h); rec.set("outputs", outs);
    return io::finish(out + ".json", rec, Status::completed, "");
  } catch (const Error& e) {
    return io::finish(out + ".json", rec, e.st, e.what());
  } catch (const std::exception& e) {
    return io::finish(out + ".json", rec, Status::internal_error, e.what());
  }
}

}  // namespace v4::eval
