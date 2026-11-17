// wp4_io.cpp -- WP4 file I/O and the merge command (see include/v4/wp4_io.h).
#include "v4/wp4_io.h"

#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <map>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <limits>
#include "v4/pmath.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/sha256.h"
#include "v4/stubs.h"
#include "v4/wp4_terminal.h"
#include <cstring>

namespace v4::wp4io {

namespace {
bool file_exists(const std::string& p) { struct stat st; return ::stat(p.c_str(), &st) == 0; }
template <class T> void add_vec_copy(fmt::Writer& W, const std::string& name, const std::vector<T>& v, uint64_t d0 = 0, uint64_t d1 = 0) {
  W.add_copy(name, fmt::dtype_of<T>(), v.data(), v.size() * sizeof(T), d0 ? d0 : v.size(), d1);
}
std::string str_or(const Json& j, const std::string& k, const std::string& d) { return j.contains(k) && j.at(k).type() == Json::STR ? j.at(k).str() : d; }
Json u64_json(uint64_t x) { return x < (1ull << 53) ? Json((double)x) : Json(hex64(x)); }
uint64_t u64_of(const Json& j) {
  if (j.type() == Json::STR) { const std::string& s = j.str(); return std::stoull(s, nullptr, s.rfind("0x", 0) == 0 ? 16 : 10); }
  return (uint64_t)j.num();
}
}  // namespace

// ---------------------------------------------------------------------------------------- content validation (review PR20 M-2)
// Every model read from a file: strictly increasing, in [0, p), size <= K. Every offset: off <= pool and len <= pool - off
// (no u64 wrap). Every value: finite. Checked BEFORE the data is used, so a hash-consistent bad file is refused with
// invalid_input, never a crash or an out-of-bounds read.
void check_model(ModelView S, int32_t p, int32_t K, const std::string& what) {
  if ((int64_t)S.k > (int64_t)K) throw Error(Status::invalid_input, what + ": model larger than K");
  for (uint32_t a = 0; a < S.k; ++a) {
    const int32_t j = S.idx[a];
    if (j < 0 || j >= p) throw Error(Status::invalid_input, what + ": index out of range [0, p)");
    if (a && j <= S.idx[a - 1]) throw Error(Status::invalid_input, what + ": model not strictly increasing");
  }
}
namespace {
inline bool off_ok(uint64_t off, uint64_t len, uint64_t np) { return off <= np && len <= np - off; }
inline void need_finite(double v, const std::string& what) { if (!std::isfinite(v)) throw Error(Status::invalid_input, what + ": not finite"); }
// Validated ptr/idx pair (ptr[0] = 0, non-decreasing, ptr[n] = |idx|), checked before any read.
std::vector<Model> models_checked(const int64_t* ptr, uint64_t np, const int32_t* idx, uint64_t ni, int32_t p, int32_t K, const std::string& what) {
  std::vector<Model> out;
  if (np == 0) return out;
  if (ptr[0] != 0 || (uint64_t)ptr[np - 1] != ni) throw Error(Status::invalid_input, what + ": offsets do not cover the pool");
  for (uint64_t i = 0; i + 1 < np; ++i)
    if (ptr[i + 1] < ptr[i] || (uint64_t)ptr[i + 1] > ni) throw Error(Status::invalid_input, what + ": offsets not monotone or past the pool");
  out.reserve(np - 1);
  for (uint64_t i = 0; i + 1 < np; ++i) {
    ModelView v(idx + ptr[i], (uint32_t)(ptr[i + 1] - ptr[i]));
    check_model(v, p, K, what);
    out.emplace_back(v.begin(), v.end());
  }
  return out;
}
}  // namespace

// ---------------------------------------------------------------------------------------------------- generic sections
void add_store_sections(fmt::Writer& W, const std::string& prefix, const Store& s) {
  if (s.staging() != 0) throw Error(Status::internal_error, "add_store: store " + prefix + " is not compacted");
  W.add(prefix + "_v", s.v); W.add(prefix + "_off", s.off); W.add(prefix + "_len", s.len);
  W.add(prefix + "_hash", s.hash); W.add(prefix + "_pool", s.pool);
}
void add_store(fmt::Writer& W, Json& meta, const std::string& prefix, const Store& s) {
  add_store_sections(W, prefix, s);
  Json d = Json::object(); d["cap"] = u64_json(s.cap); d["order"] = s.ord == Order::HPM ? "HPM" : "LEX"; d["size"] = u64_json(s.size());
  meta["stores"][prefix] = d;
}
void read_store(const fmt::Reader& R, const Json& meta, const std::string& prefix, Store& s, int32_t p, int32_t K, const Zobrist* zob) {
  const Json& d = meta.at("stores").at(prefix);
  read_store_sections(R, prefix, u64_of(d.at("cap")), d.at("order").str() == "HPM" ? Order::HPM : Order::LEX, s, p, K, zob);
}
void read_store_sections(const fmt::Reader& R, const std::string& prefix, uint64_t cap, Order order, Store& s, int32_t p, int32_t K, const Zobrist* zob) {
  s.init(cap, order);
  uint64_t n = 0, no = 0, nl = 0, nh = 0, np = 0;
  const double* v = R.get<double>(prefix + "_v", &n);
  const uint64_t* off = R.get<uint64_t>(prefix + "_off", &no);
  const uint16_t* len = R.get<uint16_t>(prefix + "_len", &nl);
  const uint64_t* h = R.get<uint64_t>(prefix + "_hash", &nh);
  const int32_t* pool = R.get<int32_t>(prefix + "_pool", &np);
  if (no != n || nl != n || nh != n || n > s.cap) throw Error(Status::invalid_input, "store " + prefix + ": inconsistent sections");
  for (uint64_t i = 0; i < n; ++i) {
    if (!off_ok(off[i], len[i], np)) throw Error(Status::invalid_input, "store " + prefix + ": pool out of range");
    need_finite(v[i], "store " + prefix + " value");
    check_model(ModelView(pool + off[i], len[i]), p, K, "store " + prefix);
    if (zob && h[i] != zob->hash(ModelView(pool + off[i], len[i]))) throw Error(Status::invalid_input, "store " + prefix + ": hash differs from the model's");
  }
  for (uint64_t i = 0; i < n; ++i) s.offer(v[i], ModelView(pool + off[i], len[i]), h[i]);
  s.compact();
  if (s.size() != n || !s.check_invariants()) throw Error(Status::invalid_input, "store " + prefix + ": not a valid sorted store (I1)");
}
void add_models(fmt::Writer& W, const std::string& prefix, const std::vector<Model>& ms) {
  std::vector<int64_t> ptr{0}; std::vector<int32_t> idx;
  for (auto& m : ms) { idx.insert(idx.end(), m.begin(), m.end()); ptr.push_back((int64_t)idx.size()); }
  add_vec_copy(W, prefix + "_ptr", ptr); add_vec_copy(W, prefix + "_idx", idx);
}
std::vector<Model> read_models(const fmt::Reader& R, const std::string& prefix, int32_t p, int32_t K) {
  uint64_t np = 0, ni = 0;
  const int64_t* ptr = R.get<int64_t>(prefix + "_ptr", &np);
  const int32_t* idx = R.get<int32_t>(prefix + "_idx", &ni);
  return models_checked(ptr, np, idx, ni, p, K, prefix);
}
Json event_json(const EventCtx& e) {
  Json j = Json::object();
  j["phase"] = phase_name(e.phase); j["mechanism"] = mech_name(e.mech); j["phi"] = e.phi;
  j["seg"] = (int)e.key.seg; j["tier"] = (int)e.key.tier; j["iter"] = (int)e.key.iter; j["unit"] = u64_json(e.key.unit);
  j["island"] = e.island(); j["xph"] = (int)e.key.xph; j["stage"] = u64_json(e.key.stage); j["round"] = u64_json(e.key.round);
  j["particle"] = u64_json(e.key.particle); j["position"] = u64_json(e.key.position); j["sub"] = (int)e.key.sub;
  return j;
}
static int index_of(const char* (*name)(int), int n, const std::string& s) {
  for (int a = 0; a < n; ++a) if (s == name(a)) return a;
  throw Error(Status::invalid_input, "unknown phase/mechanism name " + s);
}
EventCtx event_from_json(const Json& j) {
  EventCtx e;
  e.phase = index_of(phase_name, N_PHASE, j.at("phase").str()); e.mech = index_of(mech_name, N_MECH, j.at("mechanism").str());   // range-checked
  e.phi = j.at("phi").num();
  e.key.seg = (uint8_t)j.at("seg").num(); e.key.tier = (uint8_t)j.at("tier").num(); e.key.iter = (int8_t)j.at("iter").num();
  e.key.unit = (uint32_t)u64_of(j.at("unit")); e.key.xph = (uint8_t)j.at("xph").num(); e.key.stage = (uint32_t)u64_of(j.at("stage"));
  e.key.round = (uint32_t)u64_of(j.at("round")); e.key.particle = (uint32_t)u64_of(j.at("particle"));
  e.key.position = (uint32_t)u64_of(j.at("position")); e.key.sub = (uint8_t)j.at("sub").num();
  return e;
}
void add_ledger_tally(fmt::Writer& W, Json& meta, const Ledger& L) {
  meta["has_hpm"] = L.has_hpm;
  if (L.has_hpm) { add_vec_copy(W, "hpm_S", L.hpmS); meta["hpm_F"] = L.hpmF; meta["hpm_logm"] = L.hpm_logm; meta["hpm_ev"] = event_json(L.hpm_ev); }
  std::vector<uint64_t> lg((size_t)N_PHASE * N_MECH);
  for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) lg[(size_t)a * N_MECH + b] = L.logical[a][b];
  add_vec_copy(W, "logical", lg, N_PHASE, N_MECH);
  add_vec_copy(W, "island_best", L.island_best);
}
void read_ledger_tally(const fmt::Reader& R, const Json& meta, Ledger& L) {
  L.has_hpm = meta.at("has_hpm").boolean();
  if (L.has_hpm) { L.hpmS = R.vec<int32_t>("hpm_S"); L.hpmF = meta.at("hpm_F").num(); L.hpm_logm = meta.at("hpm_logm").num(); L.hpm_ev = event_from_json(meta.at("hpm_ev")); }
  uint64_t n = 0; const uint64_t* lg = R.get<uint64_t>("logical", &n);
  if (n != (uint64_t)N_PHASE * N_MECH) throw Error(Status::invalid_input, "logical: wrong size");
  for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) L.logical[a][b] = lg[(size_t)a * N_MECH + b];
  L.island_best = R.vec<double>("island_best");
}

// ------------------------------------------------------------------------------------------------------------ calib.bin
std::string write_calib(const std::string& path, const CalibWrite& c) {
  const calib::CalibOut& co = *c.co;
  fmt::Writer W(fmt::K_CALIB, c.mode);
  Json meta = Json::object();
  meta["status"] = calib::cal_status_name(co.status); meta["task_status"] = status_name(calib::task_status(co.status));
  meta["rule"] = co.rule == calib::Rule::coded ? "coded" : "bounded";
  meta["tier"] = co.tier_final; meta["N"] = c.N; meta["L"] = c.L; meta["Hm"] = c.Hm; meta["I_used"] = co.I_used;
  meta["escalated"] = co.escalated; meta["escalation_blocked"] = co.escalation_blocked;
  Json fl = Json::object();
  fl["escalated"] = co.flags.escalated; fl["grid_unconverged"] = co.flags.grid_unconverged;
  fl["grid_fallback"] = co.flags.grid_fallback; fl["forced_pilot_steps"] = co.flags.forced_pilot_steps;
  fl["checks_passed_calibration"] = co.flags.checks_passed_calibration < 0 ? Json() : Json(co.flags.checks_passed_calibration == 1);
  fl["triggers_fired"] = Json::array_of(co.flags.triggers_fired);
  meta["flags"] = fl;
  Json tiers = Json::array();
  std::vector<std::vector<double>> grids_all; std::vector<std::string> labels;
  for (auto& t : co.tiers) {
    Json tj = Json::object(); tj["tier"] = t.tier; tj["status"] = calib::cal_status_name(t.status);
    tj["triggers"] = Json::array_of(t.triggers.fired()); tj["converged"] = t.converged; tj["rebuilds"] = t.rebuilds;
    tj["grid_source"] = t.grid_source; tj["V_sizes"] = Json::array();
    for (auto& g : t.grids) { grids_all.push_back(g.grid); labels.push_back("t" + std::to_string(t.tier) + ":" + g.label + (g.ok ? "" : ":" + g.reason)); tj["V_sizes"].push(u64_json(g.V_size)); }
    tiers.push(tj);
  }
  meta["tiers"] = tiers; meta["grids_all_labels"] = Json::array_of(labels);
  // per-iteration diagnostics (review PR37 m-2): log Z_r, island_best, overall best, E1-E3 of every rebuild
  { Json its = Json::array();
    for (auto& t : co.tiers) for (auto& it : t.iterations) {
      Json j = Json::object(); j["tier"] = t.tier; j["iteration"] = it.iter; j["grid_label"] = it.grid_label; j["complete"] = it.complete;
      j["logZ_r"] = Json::array_of(it.logZ_r); Json ib = Json::array(); for (double x : it.island_best) ib.push(std::isfinite(x) ? Json(x) : Json()); j["island_best"] = ib;
      if (it.complete) { j["overall_best"] = it.overall_best; j["E1"] = it.E1; j["E2"] = it.E2; j["E3"] = it.E3; }
      its.push(j);
    }
    meta["iterations"] = its; }
  if (c.settings) {
    meta["I_max"] = c.settings->I_max; meta["ell"] = c.settings->tiers[(size_t)co.tier_final].ell;
    meta["sum_mode"] = c.settings->sum_mode == calib::SumMode::Serial ? "serial" : "blocked";
    meta["H"] = c.settings->tiers[(size_t)co.tier_final].H; meta["T_e"] = c.settings->tiers[(size_t)co.tier_final].Te;
  }
  if (co.status == calib::CalStatus::ok) meta["k_store"] = c.k_store;
  if (co.has_frozen) {
    meta["refine_m"] = co.frozen.refine_m; meta["grid_label"] = co.frozen.grid_label;
    add_vec_copy(W, "grid", co.frozen.grid); add_vec_copy(W, "grid_unrefined", co.frozen.grid_unrefined);
    if (co.frozen.has_rho) add_vec_copy(W, "rho_V", co.frozen.rho_V);
  }
  std::vector<int64_t> gptr{0}; std::vector<double> gall;
  for (auto& g : grids_all) { gall.insert(gall.end(), g.begin(), g.end()); gptr.push_back((int64_t)gall.size()); }
  add_vec_copy(W, "grids_all_ptr", gptr); add_vec_copy(W, "grids_all", gall);
  // stores, HPM and inherited models only for a completed calibration (review PR37 m-3); otherwise the HPM so far is
  // recorded in meta, labelled incomplete
  const bool ok = co.status == calib::CalStatus::ok;
  if (c.led && ok) {
    add_store(W, meta, "cstore_top", c.led->top);
    if (c.led->lead0.cap) add_store(W, meta, "cstore_lead0", c.led->lead0);
    if (c.led->lead1.cap) add_store(W, meta, "cstore_lead1", c.led->lead1);
    add_ledger_tally(W, meta, *c.led);
  } else if (c.led) {
    meta["has_hpm"] = false;
    if (c.led->has_hpm) { meta["hpm_incomplete"] = true; meta["hpm_so_far_F"] = c.led->hpmF; meta["hpm_so_far_ev"] = event_json(c.led->hpm_ev); }
  } else meta["has_hpm"] = false;
  if (ok && c.inherited_flat) {
    const calib::InheritedFlat& f = *c.inherited_flat;
    add_vec_copy(W, "inh_ptr", f.ptr); add_vec_copy(W, "inh_idx", f.idx);
    add_vec_copy(W, "inh_F", f.F); add_vec_copy(W, "inh_lg0", f.lg0); add_vec_copy(W, "inh_logm", f.logm); add_vec_copy(W, "inh_d", f.d);
  } else if (ok) {
    std::vector<Model> im; std::vector<double> iF, ilg0, ilogm;
    for (auto& m : c.inherited) { im.push_back(m.S); iF.push_back(m.F); ilg0.push_back(m.lg0); ilogm.push_back(m.logm); }
    add_models(W, "inh", im); add_vec_copy(W, "inh_F", iF); add_vec_copy(W, "inh_lg0", ilg0); add_vec_copy(W, "inh_logm", ilogm);
  }
  // stage records (spec §1 row 3): one row block per calibration island, in run order
  if (!c.stages.empty()) {
    std::vector<int32_t> sm; std::vector<int64_t> sp{0}; std::vector<double> lz, phi, inc, ess, cum; std::vector<int32_t> dr, dm; std::vector<uint64_t> mv, sx;
    for (auto& st : c.stages) {
      sm.insert(sm.end(), {st.tier, st.iter, st.island, st.partial ? 1 : 0}); lz.push_back(st.logZ);
      sx.insert(sx.end(), {st.init_hash, st.position_start, st.position_end});
      for (auto& row : st.stages) {
        phi.push_back(row.phi); inc.push_back(row.inc); ess.push_back(row.ess); cum.push_back(row.cum);
        dr.push_back(row.distinct_res); dm.push_back(row.distinct_moved);
        const MoveStats& m = row.moves;
        mv.insert(mv.end(), {m.gibbs, m.gibbs_change, m.us_exec, m.us_acc, m.us_self, m.ns_exec, m.ns_acc, m.ns_noscore, m.ns_self, m.in_exec, m.in_acc, m.gibbs_cap});
      }
      sp.push_back((int64_t)phi.size());
    }
    add_vec_copy(W, "stage_meta", sm, c.stages.size(), 4); add_vec_copy(W, "stage_logZ", lz); add_vec_copy(W, "stage_ptr", sp);
    add_vec_copy(W, "stage_stream", sx, c.stages.size(), 3);   // init_hash, stream position start, end (compat)
    add_vec_copy(W, "stage_phi", phi); add_vec_copy(W, "stage_inc", inc); add_vec_copy(W, "stage_ess", ess); add_vec_copy(W, "stage_cum", cum);
    add_vec_copy(W, "stage_distinct_res", dr); add_vec_copy(W, "stage_distinct_moved", dm); add_vec_copy(W, "stage_moves", mv, phi.size(), 12);
    meta["stage_meta_columns"] = Json::array_of(std::vector<std::string>{"tier", "iter", "island", "partial"});
  }
  for (auto& [k, v] : c.extra.items()) {   // reserved keys are never overwritten (review PR37 m-2)
    if (meta.contains(k) || k == "inputs" || k == "binary" || k == "mode") throw Error(Status::internal_error, "write_calib: extra meta key " + k + " is reserved");
    meta[k] = v;
  }
  meta["inputs"] = c.inputs; meta["binary"] = binary_block(); meta["mode"] = fmt::mode_name(c.mode);
  W.add_json("meta", meta);
  return W.write(path);
}
CalibIn read_calib(const std::string& path, int32_t p, int32_t K, const std::string& data_hash, const std::string& setup_hash) {
  fmt::Reader R(path);
  if (R.kind() != fmt::K_CALIB) throw Error(Status::invalid_input, path + ": not a calib file");
  CalibIn c; c.content_hash = R.content_hash(); c.mode = R.mode(); c.meta = R.json("meta");
  c.status = c.meta.at("status").str();
  c.tier = (int32_t)c.meta.at("tier").num(); c.N = (int32_t)c.meta.at("N").num(); c.L = (int32_t)c.meta.at("L").num();
  c.Hm = (int32_t)c.meta.at("Hm").num();
  if (c.N < 1 || c.L < 0 || c.Hm < 1 || c.tier < 0 || c.tier > 1) throw Error(Status::invalid_input, path + ": calib meta N / L / Hm / tier out of range");
  if (R.has("grid")) c.grid = R.vec<double>("grid");
  if (c.status == "ok" && !calib::check_grid(c.grid)) throw Error(Status::invalid_input, path + ": frozen grid is not a valid grid");
  c.rule = c.meta.contains("rule") ? c.meta.at("rule").str() : "";
  c.I_used = c.meta.contains("I_used") ? (int32_t)c.meta.at("I_used").num() : 0;
  c.I_max = c.meta.contains("I_max") ? (int32_t)c.meta.at("I_max").num() : -1;
  c.ell = c.meta.contains("ell") ? (int32_t)c.meta.at("ell").num() : -1;
  if (c.mode == fmt::M_V) {   // V-1M (D-1, D-26): bounded rule, tier 0, N = 2,500, I_used <= I_max <= ell
    if (c.rule != "bounded" || c.tier != 0 || c.N != calib::V_N) throw Error(Status::invalid_input, path + ": a V calib.bin must have the bounded rule, tier 0 and N = 2500 (D-1, D-26)");
    if (c.I_max < 0 || c.ell < 0 || c.I_used > c.I_max || c.I_max > c.ell) throw Error(Status::invalid_input, path + ": I_used <= I_max <= ell violated");
  } else if (c.rule != "coded") throw Error(Status::invalid_input, path + ": a theory-mode calib.bin must have the coded rule");
  if (!data_hash.empty() || !setup_hash.empty()) {
    const Json& in = c.meta.at("inputs");
    if ((!data_hash.empty() && str_or(in, "data.bin", "") != data_hash) || (!setup_hash.empty() && str_or(in, "setup.bin", "") != setup_hash))
      throw Error(Status::invalid_input, path + ": meta.inputs differ from the data / setup in use");
  }
  if (c.status == "ok") {
    if (!c.meta.contains("k_store") || c.meta.at("k_store").type() != Json::NUM ||   // a NaN is written as the string "NaN"
        !std::isfinite(c.meta.at("k_store").num()) || !(c.meta.at("k_store").num() > 0))
      throw Error(Status::invalid_input, path + ": k_store (calibration mean stored |S|) missing or not finite and > 0");
    c.k_store = c.meta.at("k_store").num();
  } else return c;   // a non-ok calib.bin exposes no inherited models
  c.has_hpm = c.meta.at("has_hpm").boolean();
  if (c.has_hpm) {
    c.hpm = R.vec<int32_t>("hpm_S"); check_model(c.hpm, p, K, path + ": hpm_S");
    c.hpm_ev = event_from_json(c.meta.at("hpm_ev")); c.hpm_ev.key.seg = SG_CALIB;
  }
  std::vector<Model> im = read_models(R, "inh", p, K);
  std::vector<double> iF = R.vec<double>("inh_F"), ilg0 = R.vec<double>("inh_lg0"), ilogm = R.vec<double>("inh_logm");
  if (iF.size() != im.size() || ilg0.size() != im.size() || ilogm.size() != im.size()) throw Error(Status::invalid_input, "calib: inherited arrays differ in length");
  for (size_t i = 0; i < im.size(); ++i) {
    need_finite(iF[i], path + ": inh_F"); need_finite(ilg0[i], path + ": inh_lg0"); need_finite(ilogm[i], path + ": inh_logm");
    c.inherited.push_back({im[i], iF[i], ilg0[i], ilogm[i]});
  }
  return c;
}

// ----------------------------------------------------------------------------------------------------------- island
std::string write_island(const std::string& path, uint32_t mode, const merge::IslandIn& isl, const Json& inputs, const Json* binary_override,
                         const std::vector<double>* grid) {
  fmt::Writer W(fmt::K_ISLAND, mode);
  const bool done = isl.status == Status::completed;
  const size_t T = isl.ess.size();
  Json meta = Json::object();
  meta["schema"] = "smcbvs4.island/1"; meta["kind"] = "island"; meta["mode"] = fmt::mode_name(mode);
  meta["r"] = isl.r; meta["N"] = isl.N; meta["T"] = (int)T; meta["L"] = isl.L; meta["Hm"] = isl.Hm; meta["p"] = (int)isl.pip.size();
  meta["status"] = status_name(isl.status); meta["reason"] = isl.message; meta["inputs"] = inputs;
  meta["binary"] = binary_override ? *binary_override : binary_block();
  { uint64_t b; std::memcpy(&b, &isl.logZ, 8); if (done) { meta["logZ"] = isl.logZ; meta["logZ_hex"] = hex64(b); } }
  W.add_json("meta", meta);
  std::vector<double> g = grid ? *grid : std::vector<double>(T + 1, 0.0), zf(T, 0.0);
  std::vector<int32_t> zi(T, 0); std::vector<uint64_t> mv(T * 12, 0), tmv((size_t)(isl.L + isl.Hm) * 12, 0);
  std::vector<int32_t> td((size_t)(isl.L + isl.Hm), 0);
  add_vec_copy(W, "grid", g); add_vec_copy(W, "st_phi", zf); add_vec_copy(W, "st_ess", isl.ess);
  add_vec_copy(W, "st_distinct_res", zi); add_vec_copy(W, "st_distinct_moved", zi);
  add_vec_copy(W, "st_moves", mv, T, 12); add_vec_copy(W, "term_moves", tmv, (uint64_t)(isl.L + isl.Hm), 12); add_vec_copy(W, "term_distinct", td);
  const Store& top = isl.led.top;
  if (top.staging() != 0) throw Error(Status::internal_error, "write_island: store not compacted");
  W.add("top_v", top.v); W.add("top_hash", top.hash); W.add("top_off", top.off); W.add("top_len", top.len); W.add("top_pool", top.pool);
  add_vec_copy(W, "hpm_S", isl.led.hpmS);
  std::vector<double> hv{isl.led.hpmF, isl.led.hpm_logm}; add_vec_copy(W, "hpm_val", hv);
  const EventKey& k = isl.led.hpm_ev.key;
  std::vector<int64_t> ev{k.seg, k.tier, k.iter, (int64_t)k.unit, k.xph, (int64_t)k.stage, (int64_t)k.round, (int64_t)k.particle,
                          (int64_t)k.position, k.sub, isl.led.hpm_ev.phase, isl.led.hpm_ev.mech};
  add_vec_copy(W, "hpm_ev", ev);
  std::vector<double> ib((size_t)std::max(0, isl.r) + 1, NEG_INF); if (isl.r >= 0 && (size_t)isl.r < isl.led.island_best.size()) ib[(size_t)isl.r] = isl.led.island_best[(size_t)isl.r];
  add_vec_copy(W, "island_best", ib);
  std::vector<uint64_t> lg((size_t)N_PHASE * N_MECH);
  for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) lg[(size_t)a * N_MECH + b] = isl.led.logical[a][b];
  add_vec_copy(W, "logical", lg, N_PHASE, N_MECH);
  if (done) {   // GUARD-W: estimates only for a completed island
    std::vector<double> lz{isl.logZ}; add_vec_copy(W, "logZ", lz);
    add_vec_copy(W, "st_inc", zf); add_vec_copy(W, "st_cum", zf);
    add_vec_copy(W, "rb_acc", isl.rb_acc); add_vec_copy(W, "pip_r", isl.pip);
    std::vector<double> rr; for (auto& x : isl.rb_round) rr.insert(rr.end(), x.begin(), x.end());
    add_vec_copy(W, "rb_round", rr, isl.rb_round.size(), isl.rb_round.empty() ? 0 : isl.rb_round[0].size());
    if (!isl.terminal.empty()) {   // WP3 names: terminal_S_ptr i64 [N+1], terminal_S i32 (omitted when the source has none,
                                   // e.g. core's islands in the golden harness; the merge then reports no occupancy)
      std::vector<int64_t> tptr{0}; std::vector<int32_t> tS;
      for (auto& S : isl.terminal) { tS.insert(tS.end(), S.begin(), S.end()); tptr.push_back((int64_t)tS.size()); }
      add_vec_copy(W, "terminal_S_ptr", tptr); add_vec_copy(W, "terminal_S", tS);
    }
  }
  return W.write(path);
}

merge::IslandHead head_island(const std::string& path, int r, const Expect& ex, Json* binary_out) {
  merge::IslandHead h; h.r = 0;
  if (!file_exists(path)) { h.load = merge::Load::missing; h.detail = path + ": missing"; return h; }
  try {
    fmt::Reader R(path);   // header hashes and every section hash
    if (R.kind() != fmt::K_ISLAND || R.mode() != ex.mode) { h.load = merge::Load::corrupt; h.detail = path + ": wrong kind or mode"; return h; }
    if ((size_t)r <= ex.island_hash.size() && !ex.island_hash[(size_t)r - 1].empty() && ex.island_hash[(size_t)r - 1] != R.content_hash()) {
      h.load = merge::Load::hash_mismatch; h.detail = path + ": content hash differs from the manifest"; return h;
    }
    Json meta = R.json("meta");
    const Json& in = meta.at("inputs");
    if (str_or(in, "data.bin", "") != ex.data_hash || str_or(in, "setup.bin", "") != ex.setup_hash || str_or(in, "calib.bin", "") != ex.calib_hash) {
      h.load = merge::Load::hash_mismatch; h.detail = path + ": meta.inputs differ from the merge's data/setup/calib"; return h;
    }
    h.r = (int32_t)meta.at("r").num(); h.N = (int32_t)meta.at("N").num(); h.p = (int32_t)meta.at("p").num();
    h.T = (int32_t)meta.at("T").num(); h.L = (int32_t)meta.at("L").num(); h.Hm = (int32_t)meta.at("Hm").num();
    h.status = status_from_name(meta.at("status").str());
    h.logZ = h.status == Status::completed ? R.vec<double>("logZ").at(0) : 0.0;
    h.content_hash = R.content_hash();
    { uint64_t ne = 0, npool = 0; R.get<uint16_t>("top_len", &ne); R.get<int32_t>("top_pool", &npool); h.store_entries = ne; h.store_pool = npool; }
    if (binary_out) *binary_out = meta.at("binary");
    h.load = merge::Load::ok;
  } catch (const std::exception& e) {
    h = merge::IslandHead(); h.load = merge::Load::corrupt; h.detail = path + ": " + e.what();
  }
  return h;
}

merge::IslandIn load_island_full(const std::string& path, int Rp, int p, const Expect& ex) {
  fmt::Reader R(path);
  Json meta = R.json("meta");
  merge::IslandIn I;
  I.r = (int32_t)meta.at("r").num(); I.N = (int32_t)meta.at("N").num(); I.T = (int32_t)meta.at("T").num();
  I.L = (int32_t)meta.at("L").num(); I.Hm = (int32_t)meta.at("Hm").num();
  I.status = status_from_name(meta.at("status").str()); I.message = str_or(meta, "reason", "");
  const int32_t K = ex.K > 0 ? ex.K : p;
  if ((int)meta.at("p").num() != p) throw Error(Status::invalid_input, "p differs from data.bin");
  if (I.r < 1 || I.r > Rp || I.N < 1 || I.T < 0 || I.L < 0 || I.Hm < 1) throw Error(Status::invalid_input, "meta r / N / T / L / Hm out of range");
  // schedule and stage table: T + 1 grid points, T stages; the final islands run the calibration's frozen grid, L, Hm
  std::vector<double> grid = R.vec<double>("grid");
  I.ess = R.vec<double>("st_ess");
  if (grid.size() != (size_t)I.T + 1 || I.ess.size() != (size_t)I.T) throw Error(Status::invalid_input, "grid / st_ess length differs from T");
  for (double e : I.ess) if (!(e >= 0.0 && e <= (double)I.N)) throw Error(Status::invalid_input, "st_ess: not in [0, N]");   // re-check n-2
  for (double x : grid) need_finite(x, "grid");
  if (!ex.grid.empty() && grid != ex.grid) throw Error(Status::invalid_input, "grid differs from calib.bin's frozen grid");
  if ((ex.L >= 0 && I.L != ex.L) || (ex.Hm >= 1 && I.Hm != ex.Hm)) throw Error(Status::invalid_input, "L / Hm differ from calib.bin");
  LedgerConfig cfg; cfg.p = p; cfg.islands = Rp; cfg.leaders = false; cfg.fresh_counters = false;   // v0.1.7: no leaders
  I.led.init(cfg);
  { uint64_t n = 0, no = 0, nl = 0, nh = 0, np = 0;
    const double* v = R.get<double>("top_v", &n); const uint64_t* off = R.get<uint64_t>("top_off", &no);
    const uint16_t* len = R.get<uint16_t>("top_len", &nl); const uint64_t* hh = R.get<uint64_t>("top_hash", &nh);
    const int32_t* pool = R.get<int32_t>("top_pool", &np);
    if (no != n || nl != n || nh != n || n > I.led.top.cap) throw Error(Status::invalid_input, "inconsistent top store sections");
    for (uint64_t i = 0; i < n; ++i) {   // every entry validated before any is used
      if (!off_ok(off[i], len[i], np)) throw Error(Status::invalid_input, "top store: pool offset out of range");
      need_finite(v[i], "top store value");
      check_model(ModelView(pool + off[i], len[i]), p, K, "top store");
      // review PR20 re-check n-1: a wrong hash would let duplicates of one model into the merged store
      if (ex.zob && hh[i] != ex.zob->hash(ModelView(pool + off[i], len[i]))) throw Error(Status::invalid_input, "top store: hash differs from the model's");
    }
    for (uint64_t i = 0; i < n; ++i) I.led.top.offer(v[i], ModelView(pool + off[i], len[i]), hh[i]);
    I.led.top.compact();
    if (I.led.top.size() != n || !I.led.top.check_invariants()) throw Error(Status::invalid_input, "top store not sorted / unique (I1)");
  }
  { std::vector<int32_t> hs = R.vec<int32_t>("hpm_S"); std::vector<double> hv = R.vec<double>("hpm_val"); std::vector<int64_t> ev = R.vec<int64_t>("hpm_ev");
    if (hv.size() != 2 || ev.size() != 12) throw Error(Status::invalid_input, "hpm_val / hpm_ev size");
    I.led.has_hpm = I.led.top.size() > 0;
    if (I.led.has_hpm) {
      Model S(hs.begin(), hs.end());
      check_model(S, p, K, "hpm_S");
      need_finite(hv[0], "hpm_val F");
      need_finite(hv[1], "hpm_val log m");   // re-check n-2
      // the island's HPM is the best entry of its own store (same order), with the same value
      ModelView t0 = I.led.top.model(0);
      if (!same_model(S, t0) || hv[0] != I.led.top.v[0]) throw Error(Status::invalid_input, "hpm_S / hpm_val differ from the store's best entry");
      // hpm_ev: field ranges (INTERFACES v0.1.8 §5.1 order), a final event of this island, stage <= T
      if (ev[10] < 0 || ev[10] >= N_PHASE || ev[11] < 0 || ev[11] >= N_MECH) throw Error(Status::invalid_input, "hpm_ev phase / mech out of range");
      if (ev[0] != SG_FINAL || ev[3] != I.r) throw Error(Status::invalid_input, "hpm_ev is not a final event of this island");
      if (!(ev[4] == X_INIT || ev[4] == X_BRIDGE || ev[4] == X_BURN || ev[4] == X_MEASURED)) throw Error(Status::invalid_input, "hpm_ev xph out of range");
      for (int q : {1, 5, 6, 7, 8, 9}) if (ev[q] < 0 || ev[q] > (int64_t)UINT32_MAX) throw Error(Status::invalid_input, "hpm_ev field out of range");
      if (ev[2] < -1 || ev[2] > 63) throw Error(Status::invalid_input, "hpm_ev iter out of range");
      if (ev[1] < 0 || ev[1] > 1 || (ex.tier >= 0 && ev[1] != ex.tier)) throw Error(Status::invalid_input, "hpm_ev tier is not the frozen tier");   // re-check n-2
      if (ev[9] < 0 || ev[9] > 255) throw Error(Status::invalid_input, "hpm_ev sub out of range");
      if (ev[5] > I.T || (ev[4] == X_BRIDGE && ev[5] < 1)) throw Error(Status::invalid_input, "hpm_ev stage out of range [0, T]");
      I.led.hpmS = S; I.led.hpmF = hv[0]; I.led.hpm_logm = hv[1];
      EventKey& k = I.led.hpm_ev.key;
      k.seg = (uint8_t)ev[0]; k.tier = (uint8_t)ev[1]; k.iter = (int8_t)ev[2]; k.unit = (uint32_t)ev[3]; k.xph = (uint8_t)ev[4];
      k.stage = (uint32_t)ev[5]; k.round = (uint32_t)ev[6]; k.particle = (uint32_t)ev[7]; k.position = (uint32_t)ev[8]; k.sub = (uint8_t)ev[9];
      I.led.hpm_ev.phase = (int)ev[10]; I.led.hpm_ev.mech = (int)ev[11];
      // phi is not in hpm_ev: v3's values by phase (INIT 0, BRIDGE grid[stage], BURN / MEASURED 1); stage <= T checked
      I.led.hpm_ev.phi = k.xph == X_BRIDGE ? grid[k.stage] : (k.xph == X_BURN || k.xph == X_MEASURED) ? 1.0 : 0.0;
    } else if (I.status == Status::completed) throw Error(Status::invalid_input, "a completed island with an empty store");
  }
  { std::vector<double> ib = R.vec<double>("island_best");
    if (ib.size() != (size_t)I.r + 1) throw Error(Status::invalid_input, "island_best length is not r + 1");
    if (std::isnan(ib[(size_t)I.r]) || ib[(size_t)I.r] == POS_INF) throw Error(Status::invalid_input, "island_best: not finite");
    // re-check n-2: the island's own maximum is its HPM's F (WP3 and v3 write it so)
    if (I.led.has_hpm && ib[(size_t)I.r] != I.led.hpmF) throw Error(Status::invalid_input, "island_best[r] differs from the island HPM's F");
    // only entry r belongs to this island; the others stay -inf (review PR20 M-2, H19)
    I.led.island_best[(size_t)I.r] = ib[(size_t)I.r]; }
  { uint64_t n = 0; const uint64_t* lg = R.get<uint64_t>("logical", &n);
    if (n != (uint64_t)N_PHASE * N_MECH) throw Error(Status::invalid_input, "logical size");
    for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) I.led.logical[a][b] = lg[(size_t)a * N_MECH + b]; }
  if (I.status == Status::completed) {
    std::vector<double> lz = R.vec<double>("logZ");
    if (lz.size() != 1) throw Error(Status::invalid_input, "logZ size");
    I.logZ = lz[0]; need_finite(I.logZ, "logZ");
    I.pip = R.vec<double>("pip_r");
    if ((int)I.pip.size() != p) throw Error(Status::invalid_input, "pip_r has the wrong length");
    for (double x : I.pip) if (!(x >= 0.0 && x <= 1.0)) throw Error(Status::invalid_input, "pip_r: not in [0, 1]");
    // rb_acc / rb_round are not used by the merge: not loaded (review PR20 m-2); their shape is still checked
    if (R.entry("rb_round").length != (uint64_t)I.Hm * (uint64_t)p * 8) throw Error(Status::invalid_input, "rb_round is not Hm x p");
    I.terminal = merge::read_terminal_supports(R, I.N, p);
    for (auto& S : I.terminal) check_model(S, p, K, "terminal_S");
  }
  return I;
}

merge::IslandSlot load_island(const std::string& path, int r, const Expect& ex, int p, Json* binary_out) {
  merge::IslandSlot s;
  merge::IslandHead h = head_island(path, r, ex, binary_out);
  s.load = h.load; s.detail = h.detail;
  if (h.load != merge::Load::ok) return s;
  try { s.isl = load_island_full(path, std::max(1, h.r), p, ex); }
  catch (const std::exception& e) { s = merge::IslandSlot(); s.load = merge::Load::corrupt; s.detail = path + ": " + e.what(); }
  return s;
}
void check_binaries(std::vector<merge::IslandHead>& heads, const std::vector<Json>& blocks, uint32_t mode) {
  const BinaryUse use = mode == fmt::M_V ? BinaryUse::MergeV : BinaryUse::MergeTheory;
  int ref = -1;
  for (size_t i = 0; i < heads.size(); ++i) if (heads[i].load == merge::Load::ok) { ref = (int)i; break; }
  if (ref < 0) return;
  for (size_t i = 0; i < heads.size(); ++i) {
    if (heads[i].load != merge::Load::ok) continue;
    BinaryCheck bc = binary_compatible(blocks[(size_t)ref], blocks[i], use);
    if (!bc.ok) { heads[i].load = merge::Load::binary_mismatch; heads[i].detail = "island " + std::to_string(i + 1) + ": " + bc.reason; }
  }
}
void check_binaries(std::vector<merge::IslandSlot>& slots, const std::vector<Json>& blocks, uint32_t mode) {
  std::vector<merge::IslandHead> h(slots.size());
  for (size_t i = 0; i < slots.size(); ++i) h[i].load = slots[i].load;
  check_binaries(h, blocks, mode);
  for (size_t i = 0; i < slots.size(); ++i) if (h[i].load == merge::Load::binary_mismatch) { slots[i].load = h[i].load; slots[i].detail = h[i].detail; }
}
FileIslandSource::FileIslandSource(std::vector<std::string> paths, const Expect& ex, int Rp, int p) : paths_(std::move(paths)), ex_(ex), Rp_(Rp), p_(p) {
  std::vector<Json> blocks(paths_.size());
  for (size_t r = 1; r <= paths_.size(); ++r) heads_.push_back(head_island(paths_[r - 1], (int)r, ex, &blocks[r - 1]));
  check_binaries(heads_, blocks, ex.mode);
}
merge::IslandIn FileIslandSource::load(int r) {
  try { return load_island_full(paths_[(size_t)r - 1], Rp_, p_, ex_); }
  catch (const std::exception& e) { merge::IslandIn bad; bad.r = -1; bad.message = e.what(); return bad; }   // refused by the merge
}

// ------------------------------------------------------------------------------------------------------------ setup
double SetupView::comp(const Model& S, std::vector<std::pair<int32_t, int32_t>>& scratch) const {
  // core/cpp/v3_start.h:54-66, copied: (block, position) pairs sorted; one code per block met; sum in block order.
  scratch.clear();
  for (int32_t j : S) scratch.push_back({blk[(size_t)j], pos[(size_t)j]});
  std::sort(scratch.begin(), scratch.end());
  double s = 0; size_t i = 0;
  while (i < scratch.size()) {
    int32_t b = scratch[i].first; uint32_t code = 0;
    while (i < scratch.size() && scratch[i].first == b) { code |= (1u << scratch[i].second); ++i; }
    s += logr[(size_t)code_ptr[(size_t)b] + code];
  }
  return s;
}
uint64_t SetupView::table_event_count(int32_t K) const {
  uint64_t n = 0;
  for (size_t b = 0; b + 1 < blk_ptr.size(); ++b) {
    int64_t m = blk_ptr[b + 1] - blk_ptr[b];
    for (uint32_t c = 0; c < (1u << m); ++c) if (__builtin_popcount(c) <= K) ++n;
  }
  return n;
}
EventCtx SetupView::table_event_of(const Model& S) const {
  if (S.empty()) return merge::table_event(0, 0);   // the empty model: block 1, code 0 is its first table event
  int32_t b = blk[(size_t)S[0]]; uint32_t code = 0;
  for (int32_t j : S) { if (blk[(size_t)j] != b) throw Error(Status::invalid_input, "table store model spans blocks"); code |= 1u << pos[(size_t)j]; }
  return merge::table_event(b, code);
}
namespace {
std::string setup_data_hash(const Json& meta) {
  if (meta.contains("inputs") && meta.at("inputs").contains("data.bin") && meta.at("inputs").at("data.bin").type() == Json::STR) return meta.at("inputs").at("data.bin").str();
  return "";
}
// the pi_0 size law (calibrate's memory plan, INTERFACES §7): K + 1 log masses summing to 1
std::vector<double> checked_size_logmass(const double* q, uint64_t c, int32_t K, const std::string& w) {
  if (c != (uint64_t)K + 1) throw Error(Status::invalid_input, w + "size_logmass length != K + 1");
  std::vector<double> v(q, q + c);
  long double tot = 0;
  for (double x : v) {
    if (std::isnan(x) || x == std::numeric_limits<double>::infinity() || x > 1e-9) throw Error(Status::invalid_input, w + "size_logmass not a log probability");
    tot += std::exp((long double)x);
  }
  if (std::fabs((double)tot - 1.0) > 1e-6) throw Error(Status::invalid_input, w + "size_logmass does not sum to 1");
  return v;
}
// One small section, checked against its table hash (the Reader was opened without verify_all). Refuses a section
// longer than `max_bytes`, so a plan read stays bounded whatever the file claims.
void check_small_section(const fmt::Reader& R, const std::string& name, const void* q, uint64_t max_bytes, const std::string& w) {
  const fmt::SectionEntry& e = R.entry(name);
  if (e.length > max_bytes) throw Error(Status::invalid_input, w + "section " + name + " too long for a plan read");
  auto h = sha256(q, (size_t)e.length);
  if (std::memcmp(h.data(), e.sha256, 32) != 0) throw Error(Status::invalid_input, w + "section " + name + " hash mismatch");
}
// a JSON section read with pread (Reader::json has no raw view), checked against its hash, then parsed
Json small_json(const fmt::Reader& R, const std::string& path, const std::string& name, const std::string& w) {
  const fmt::SectionEntry& e = R.entry(name);
  if (e.dtype != fmt::D_JSON) throw Error(Status::invalid_input, w + "section " + name + " is not json");
  constexpr uint64_t MAXJ = 16ull << 20;
  if (e.length > MAXJ) throw Error(Status::invalid_input, w + "section " + name + " too long for a plan read");
  std::string txt((size_t)e.length, '\0');
  int fd = ::open(path.c_str(), O_RDONLY);
  if (fd < 0) throw Error(Status::invalid_input, "cannot open " + path);
  ssize_t got = ::pread(fd, txt.data(), (size_t)e.length, (off_t)e.offset);
  ::close(fd);
  if (got != (ssize_t)e.length) throw Error(Status::io_error, w + "short read of section " + name);
  check_small_section(R, name, txt.data(), MAXJ, w);
  return Json::parse(txt);
}
uint64_t stat_bytes(const std::string& p) { struct stat st{}; return ::stat(p.c_str(), &st) == 0 ? (uint64_t)st.st_size : 0; }
}  // namespace

DataPlanHead read_data_plan(const std::string& path) {
  fmt::Reader R(path, /*verify=*/false);   // header + table (hash-checked), no section read
  const std::string w = path + ": ";
  if (R.kind() != fmt::K_DATA) throw Error(Status::invalid_input, path + " is not a data file");
  Json m = small_json(R, path, "meta", w);
  DataPlanHead h; h.content_hash = R.content_hash(); h.file_bytes = stat_bytes(path);
  if (!m.contains("n") || !m.contains("p") || !m.contains("K")) throw Error(Status::invalid_input, w + "meta has no n / p / K");
  h.n = m.at("n").i64(); h.p = m.at("p").i64(); const int64_t K = m.at("K").i64();
  if (h.n < 3 || h.p < 1 || h.p > ((int64_t)1 << 31) - 1 || K < 0 || K > h.p) throw Error(Status::invalid_input, w + "bad n / p / K");
  h.K = (int32_t)K;
  return h;
}
SetupPlanHead read_setup_plan(const std::string& path, int32_t K) {
  fmt::Reader R(path, /*verify=*/false);
  const std::string w = path + ": ";
  if (R.kind() != fmt::K_SETUP) throw Error(Status::invalid_input, path + ": not a setup file");
  SetupPlanHead h; h.content_hash = R.content_hash(); h.file_bytes = stat_bytes(path);
  h.data_hash = setup_data_hash(small_json(R, path, "meta", w));
  if (R.has("size_logmass")) {
    uint64_t c = 0; const double* q = R.get<double>("size_logmass", &c);
    check_small_section(R, "size_logmass", q, 8ull * ((uint64_t)K + 1), w);   // a length != K + 1 is refused here, unread
    h.size_logmass = checked_size_logmass(q, c, K, w);
  }
  return h;
}

SetupView read_setup(const std::string& path, int32_t p, int32_t K, const Zobrist* zob) {
  fmt::Reader R(path);
  if (R.kind() != fmt::K_SETUP) throw Error(Status::invalid_input, path + ": not a setup file");
  SetupView s; s.content_hash = R.content_hash();
  Json meta = R.json("meta");
  s.data_hash = setup_data_hash(meta);
  s.blk = R.vec<int32_t>("blk"); s.pos = R.vec<int32_t>("pos"); s.code_ptr = R.vec<int64_t>("code_ptr"); s.logr = R.vec<double>("logr");
  s.blk_ptr = R.vec<int64_t>("blk_ptr"); s.blk_members = R.vec<int32_t>("blk_members"); s.mode_S = R.vec<int32_t>("mode_S");
  // shapes (review PR20 M-2): blk / pos / members over p columns; blocks of 1..20 members (B <= 16, table codes < 2^20);
  // members[blk_ptr[b] + pos[j]] = j; each block's table fits in logr; logr finite for every code with |U| <= K
  const std::string w = path + ": ";
  if (s.blk.size() != (size_t)p || s.pos.size() != (size_t)p || s.blk_members.size() != (size_t)p) throw Error(Status::invalid_input, w + "blk / pos / blk_members length != p");
  // INTERFACES v0.1.18 §2/§5: J blocks; blk_ptr and code_ptr both have J + 1 entries (CSR); code_ptr[0] = 0, block b's
  // table is logr[code_ptr[b] .. code_ptr[b + 1]) = 2^m codes, code_ptr[J] = |logr|
  if (s.blk_ptr.empty() || s.code_ptr.size() != s.blk_ptr.size()) throw Error(Status::invalid_input, w + "code_ptr must have J + 1 entries like blk_ptr");
  const size_t J = s.blk_ptr.size() - 1;
  if (J == 0 || s.blk_ptr[0] != 0 || s.blk_ptr[J] != p) throw Error(Status::invalid_input, w + "blk_ptr shape");
  if (s.code_ptr[0] != 0 || s.code_ptr[J] != (int64_t)s.logr.size()) throw Error(Status::invalid_input, w + "code_ptr[0] != 0 or code_ptr[J] != |logr|");
  for (size_t b = 0; b < J; ++b) {
    const int64_t m = s.blk_ptr[b + 1] - s.blk_ptr[b];
    if (m < 1 || m > 20) throw Error(Status::invalid_input, w + "block size outside 1..20");
    const int64_t c0 = s.code_ptr[b];
    if (c0 < 0 || (uint64_t)c0 > s.logr.size() || (uint64_t)(1ull << m) > s.logr.size() - (uint64_t)c0) throw Error(Status::invalid_input, w + "code_ptr / logr out of range");
    if (s.code_ptr[b + 1] - c0 != (int64_t)(1ull << m)) throw Error(Status::invalid_input, w + "code_ptr: block table length != 2^m");
    for (uint32_t c = 0; c < (1u << m); ++c) if (__builtin_popcount(c) <= K && !std::isfinite(s.logr[(size_t)c0 + c])) throw Error(Status::invalid_input, w + "logr not finite for a code with |U| <= K");
  }
  for (int32_t j = 0; j < p; ++j) {
    const int32_t b = s.blk[(size_t)j], q = s.pos[(size_t)j];
    if (b < 0 || (size_t)b >= J) throw Error(Status::invalid_input, w + "blk out of range");
    if (q < 0 || q >= s.blk_ptr[(size_t)b + 1] - s.blk_ptr[(size_t)b]) throw Error(Status::invalid_input, w + "pos out of range of its block");
    if (s.blk_members[(size_t)(s.blk_ptr[(size_t)b] + q)] != j) throw Error(Status::invalid_input, w + "blk / pos / blk_members inconsistent");
  }
  check_model(s.mode_S, p, K, w + "mode_S");
  if (R.has("size_logmass")) { uint64_t c = 0; const double* q = R.get<double>("size_logmass", &c); s.size_logmass = checked_size_logmass(q, c, K, w); }
  // table stores: caps and orders from INTERFACES §4.1 (top 40p + 1 HPM, lead0 / lead1 20p LEX); setup.bin carries no
  // meta.stores (v0.1.18), the tstore_* sections are all there is. A stray meta.stores is ignored.
  read_store_sections(R, "tstore_top", 40ull * (uint64_t)p + 1, Order::HPM, s.ttop, p, K, zob);
  if (R.has("tstore_lead0_v")) read_store_sections(R, "tstore_lead0", 20ull * (uint64_t)p, Order::LEX, s.tlead0, p, K, zob);
  if (R.has("tstore_lead1_v")) read_store_sections(R, "tstore_lead1", 20ull * (uint64_t)p, Order::LEX, s.tlead1, p, K, zob);
  for (const Store* st : {&s.ttop, &s.tlead0, &s.tlead1})   // table models lie within one block
    for (size_t i = 0; i < st->size(); ++i) { ModelView v = st->model(i); s.table_event_of(Model(v.begin(), v.end())); }
  return s;
}
std::string write_setup_min(const std::string& path, const SetupView& s, const Json& inputs) {
  if (s.code_ptr.empty() || s.code_ptr.size() != s.blk_ptr.size() || s.code_ptr.back() != (int64_t)s.logr.size())
    throw Error(Status::internal_error, "write_setup_min: code_ptr must have J + 1 entries with code_ptr[J] = |logr| (INTERFACES v0.1.18)");
  fmt::Writer W(fmt::K_SETUP, fmt::M_COMPAT);
  Json meta = Json::object();
  W.add("blk", s.blk); W.add("pos", s.pos); W.add("code_ptr", s.code_ptr); W.add("logr", s.logr);
  W.add("blk_ptr", s.blk_ptr); W.add("blk_members", s.blk_members); W.add("mode_S", s.mode_S);
  if (!s.size_logmass.empty()) W.add("size_logmass", s.size_logmass);
  add_store_sections(W, "tstore_top", s.ttop);   // no meta.stores in setup.bin (INTERFACES v0.1.18)
  if (s.tlead0.cap) add_store_sections(W, "tstore_lead0", s.tlead0);
  if (s.tlead1.cap) add_store_sections(W, "tstore_lead1", s.tlead1);
  meta["inputs"] = inputs; meta["binary"] = binary_block(); meta["writer"] = "wp4 write_setup_min (test/harness; WP2 owns setup.bin)";
  W.add_json("meta", meta);
  return W.write(path);
}
void offer_tables(Ledger& led, const SetupView& s, int32_t K, const Zobrist& zob) {
  for (size_t i = 0; i < s.ttop.size(); ++i) {
    ModelView v = s.ttop.model(i); Model S(v.begin(), v.end());
    led.offer_hpm(S, s.ttop.v[i], 0.0, s.table_event_of(S));
    led.top.offer(s.ttop.v[i], S, zob.hash(S));
  }
  for (size_t i = 0; i < s.tlead0.size(); ++i) { ModelView v = s.tlead0.model(i); led.lead0.offer(s.tlead0.v[i], v, s.tlead0.hash[i]); }
  for (size_t i = 0; i < s.tlead1.size(); ++i) { ModelView v = s.tlead1.model(i); led.lead1.offer(s.tlead1.v[i], v, s.tlead1.hash[i]); }
  led.logical[PH_TABLE][ME_TABLE] += s.table_event_count(K);
  led.compact();
}

// -------------------------------------------------------------------------------------------------------------- fit
// Regularised upper incomplete gamma Q(a, x) (series for x < a + 1, continued fraction otherwise; Numerical Recipes
// 6.2 algorithm), P(chi2_df > x) = Q(df/2, x/2).
double chi2_upper(double x, int df) {
  if (df <= 0 || !(x >= 0)) return std::numeric_limits<double>::quiet_NaN();
  const double a = 0.5 * df, z = 0.5 * x;
  if (z == 0) return 1.0;
  const double gln = pm::lgamma(a);
  if (z < a + 1) {
    double ap = a, sum = 1.0 / a, del = sum;
    for (int n = 0; n < 1000; ++n) { ap += 1; del *= z / ap; sum += del; if (std::fabs(del) < std::fabs(sum) * 1e-15) break; }
    return 1.0 - sum * pm::exp(-z + a * pm::log(z) - gln);
  }
  double b = z + 1 - a, c = 1e300, d = 1 / b, h = d;
  for (int i = 1; i < 1000; ++i) {
    double an = -i * (i - a); b += 2; d = an * d + b; if (std::fabs(d) < 1e-300) d = 1e-300;
    c = b + an / c; if (std::fabs(c) < 1e-300) c = 1e-300; d = 1 / d; double del = d * c; h *= del;
    if (std::fabs(del - 1) < 1e-15) break;
  }
  return pm::exp(-z + a * pm::log(z) - gln) * h;
}

static void add_archive(fmt::Writer& W, Json& meta, const std::string& pfx, const LocalArchive& A) {
  add_models(W, pfx + "_path", A.path); add_vec_copy(W, pfx + "_path_F", A.path_F);
  add_models(W, pfx + "_scanned", A.scanned); add_vec_copy(W, pfx + "_scanned_F", A.scanned_F);
  add_vec_copy(W, pfx + "_scan_size", A.scan_size);
  add_vec_copy(W, pfx + "_centre", A.centre); add_vec_copy(W, pfx + "_returned", A.returned);
  Json j = Json::object();
  j["centre_F"] = A.centre_F; j["returned_F"] = A.returned_F; j["termination"] = A.termination; j["local_limit"] = A.local_limit;
  j["local_certified"] = A.local_certified; j["moves"] = A.moves; j["n_evaluated"] = (double)A.n_eval;
  meta[pfx] = j;
}

std::string write_fit(const std::string& path, const FitWrite& f, Json* record) {
  const merge::FitOut& fo = *f.fo; const merge::MergeSettings& ms = *f.ms;
  fmt::Writer W(fmt::K_FIT, f.mode);
  Json meta = Json::object();
  meta["status"] = status_name(fo.status); meta["fit_state"] = fo.fit_state; meta["reason"] = fo.reason;
  meta["estimates_available"] = fo.estimates_available; meta["Rp"] = ms.Rp; meta["N"] = ms.N; meta["tier"] = ms.tier;
  { Json me = Json::object(); me["merged"] = u64_json(fo.mem.merged); me["one_island"] = u64_json(fo.mem.one_island);
    me["small"] = u64_json(fo.mem.small); me["tail"] = u64_json(fo.mem.tail); me["total"] = u64_json(fo.mem.total);
    me["label"] = "ESTIMATE (streaming merge memory model)"; me["budget"] = u64_json(ms.mem_budget_bytes); meta["mem_estimate"] = me; }
  Json ist = Json::array(); for (Status s : fo.island_status) ist.push(status_name(s)); meta["island_status"] = ist;
  meta["missing_islands"] = Json::array_of(fo.missing); meta["invalid_islands"] = Json::array_of(fo.invalid);
  if (fo.has_hpm) {
    add_vec_copy(W, "hpm_S", fo.hpm);
    meta["hpm_F"] = fo.hpm_F; meta["hpm_ev"] = event_json(fo.hpm_ev); meta["hpm_phase"] = phase_name(fo.hpm_ev.phase);
    meta["hpm_mech"] = mech_name(fo.hpm_ev.mech); meta["hpm_phi"] = fo.hpm_ev.phi; meta["hpm_incomplete"] = fo.hpm_incomplete;
  }
  if (fo.estimates_available) {   // GUARD-W: every estimate field only for a completed fit
    meta["logZ"] = fo.log_Z; meta["logZ_lower95"] = fo.log_Z_lower95; meta["logZ_rel_m0"] = fo.log_Z_rel_m0;
    meta["logZ_T"] = fo.log_Z_T; meta["R_eff"] = fo.R_eff; meta["max_W"] = fo.max_W;
    meta["hpm_before_local_F"] = fo.hpm_before_local_F; meta["hpm_before_ls0_F"] = fo.hpm_before_ls0_F;
    meta["local_certified"] = fo.local_certified; meta["local_certified_by"] = fo.local_certified_by;
    meta["mode_size"] = (int)fo.mode_S.size(); meta["ls0_moves"] = fo.ls0.moves; meta["ls0_cap"] = fo.ls0_cap;
    Json fl = Json::object();
    fl["E1"] = fo.E1; fl["E2"] = fo.E2; fl["E3"] = fo.E3; fl["low_empirical_ESS"] = fo.low_ESS; fl["local_limit"] = fo.local_limit;
    fl["near_tie_truncated"] = fo.near_tie_truncated; fl["checks_passed_final"] = fo.checks_passed_final;
    fl["final_local_limit"] = fo.final_local_limit; fl["ls0_local_limit"] = fo.ls0_local_limit;
    fl["ls0_improved"] = fo.ls0_improved; fl["ls0_hpm_changed"] = fo.ls0_hpm_changed;
    bool inhom = false;
    Json occ = Json::array();
    for (auto& row : fo.occ) {
      Json o = Json::object(); double pv = chi2_upper(row.chi2_homogeneity, row.chi2_df);
      o["M"] = row.M; o["M_used"] = row.M_used; o["log_store_mass"] = row.log_store_mass; o["occ"] = row.occ;
      o["log_Z_occ"] = row.log_Z_occ; o["sd_log_Z_occ_r"] = row.sd_log_Z_occ_r; o["chi2"] = row.chi2_homogeneity;
      o["df"] = row.chi2_df; o["p_value"] = pv; o["inhomogeneous"] = pv < f.occ_alpha;
      if (pv < f.occ_alpha) inhom = true;
      o["log_Z_occ_r"] = Json::array_of(row.log_Z_occ_r);
      occ.push(o);
    }
    fl["occ_inhomogeneous"] = inhom;   // flag only (never switches an estimator); chi-square p < 0.001
    meta["flags"] = fl; meta["occ"] = occ; meta["occ_alpha"] = f.occ_alpha;
    if (fo.occ_available) {
      meta["occ_total"] = u64_json(fo.occ_total);
      meta["occ_total_r"] = u64_json(fo.occ_total_r.empty() ? 0 : fo.occ_total_r[0]);   // per island (equal N): WP5 reads one scalar
      meta["occ_total_r_all"] = Json::array(); for (uint64_t t : fo.occ_total_r) meta["occ_total_r_all"].push(u64_json(t));
      add_vec_copy(W, "occ_top", fo.occ_top);
      add_vec_copy(W, "occ_top_r", fo.occ_top_r, (uint64_t)ms.Rp, fo.occ_top.size());
    }
    add_vec_copy(W, "logZ_r", fo.logZ_r); add_vec_copy(W, "pip_eq", fo.pip_eq); add_vec_copy(W, "pip_Z", fo.pip_Z);
    add_vec_copy(W, "pip_T", fo.pip_T); add_vec_copy(W, "W_r", fo.W_r);
    std::vector<double> pr; for (auto& x : fo.pip_r) pr.insert(pr.end(), x.begin(), x.end());
    add_vec_copy(W, "pip_r", pr, (uint64_t)ms.Rp, (uint64_t)ms.p);
    add_vec_copy(W, "mpm", fo.mpm); add_vec_copy(W, "mode_S", fo.mode_S);
    add_vec_copy(W, "hpm_before_local_S", fo.hpm_before_local); add_vec_copy(W, "hpm_before_ls0_S", fo.hpm_before_ls0);
    add_models(W, "near", fo.near_ties); add_vec_copy(W, "near_F", fo.near_tie_F);
    add_archive(W, meta, "ls", fo.local); add_archive(W, meta, "ls0", fo.ls0);
    add_store(W, meta, "top", fo.led.top);
    if (fo.led.lead0.cap) add_store(W, meta, "lead0", fo.led.lead0);
    if (fo.led.lead1.cap) add_store(W, meta, "lead1", fo.led.lead1);
    std::vector<uint64_t> lg((size_t)N_PHASE * N_MECH);
    for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) lg[(size_t)a * N_MECH + b] = fo.led.logical[a][b];
    add_vec_copy(W, "logical", lg, N_PHASE, N_MECH);
    add_vec_copy(W, "island_best", fo.led.island_best);
  }
  meta["inputs"] = f.inputs; meta["timings"] = f.timings; meta["binary"] = binary_block(); meta["mode"] = fmt::mode_name(f.mode);
  W.add_json("meta", meta);
  std::string h = W.write(path);
  if (record) {   // fit.json: scalars and hashes only
    Json& rec = *record;
    rec["status"] = status_name(fo.status); rec["fit_state"] = fo.fit_state; rec["reason"] = fo.reason;
    rec["estimates_available"] = fo.estimates_available; rec["fit_bin"] = h; rec["inputs"] = f.inputs;
    if (fo.has_hpm) rec["hpm_F"] = fo.hpm_F;
    if (fo.estimates_available) { rec["logZ"] = fo.log_Z; rec["logZ_T"] = fo.log_Z_T; rec["R_eff"] = fo.R_eff; }
  }
  return h;
}

}  // namespace v4::wp4io

// ------------------------------------------------------------------------------------------------- the merge command
namespace v4::merge {
namespace {
struct BitEval {   // per-chunk evaluator: compat Bit scorer + comp(S) of the setup tables
  const Data* D; const wp4io::SetupView* S; BitScorer sc; std::vector<std::pair<int32_t, int32_t>> scratch;
  BitEval(const Data* d, const wp4io::SetupView* s) : D(d), S(s), sc(d) {}
  void operator()(const Model& M, double& lm, double& lg0, double& dd, double& F) {
    lm = sc.score(M).logm;
    double c = S->comp(M, scratch); size_t k = M.size();
    lg0 = D->logprior[k] + c; dd = (lm - D->logm0) - c; F = D->logprior[k] + lm;   // core/cpp/v3_engine.h:84-90
  }
};
struct BitFactory { const Data* D; const wp4io::SetupView* S; BitEval make() const { return BitEval(D, S); } };
int ceil_log2(double x) { int c = 0; while (std::ldexp(1.0, c) < x) ++c; return c; }   // core/v3_preprocess.R:15
double nget(const Json& a, const std::string& k, double d) { return a.contains(k) ? a.at(k).num() : d; }
}  // namespace

// The merge's inputs (review PR20 C-1, M-1). Two forms, which may be combined:
//  * the WP5 driver's manifest (`--manifest m.json`; the CLI passes the parsed object and copies `params` into args):
//    data / setup / calib / island_<r>.bin are the `inputs` paths (by base name), R' = params.Rp, mode = the manifest's mode;
//  * explicit arguments: --data --setup --calib, --islands as a JSON array or a comma-separated list (island r = position r),
//    --Rp, --mode.
// R' must be given (params.Rp or --Rp) and the island list must have exactly R' entries, indices 1..R' each once; else
// invalid_input. --mem-budget is in BYTES (INTERFACES §7; 0 = off); --mem-budget-gb is an alias. --out is required.
struct MergeInputs { std::string data, setup, calib, out; std::vector<std::string> islands; int Rp = 0; uint32_t mode = 0; Json manifest; };
namespace {
std::string base_name(const std::string& p) { size_t k = p.find_last_of('/'); return k == std::string::npos ? p : p.substr(k + 1); }
}
MergeInputs parse_merge_inputs(const Json& args) {
  MergeInputs in;
  if (args.contains("manifest")) {
    const Json& m = args.at("manifest");
    in.manifest = m.type() == Json::STR ? read_json_file(m.str()) : m;
    if (in.manifest.type() != Json::OBJ) throw Error(Status::invalid_input, "merge: --manifest is not a JSON object");
  } else in.manifest = Json::object();
  const Json minp = in.manifest.contains("inputs") ? in.manifest.at("inputs") : Json::object();
  auto from_inputs = [&](const std::string& name) {
    std::string found;
    for (auto& [k, v] : minp.items()) if (base_name(k) == name) {
      if (!found.empty()) throw Error(Status::invalid_input, "merge: manifest inputs name " + name + " twice");
      found = k;
    }
    return found;
  };
  // With a manifest, the manifest is the authority (review PR20 re-check n-3): an explicit argument that disagrees with
  // it is refused, so neither argument order nor an override can pool a subset or swap an input.
  const bool has_man = in.manifest.size() > 0;
  auto path_arg = [&](const char* key, const std::string& name) {
    std::string f = from_inputs(name), a;
    if (args.contains(key)) { if (args.at(key).type() != Json::STR) throw Error(Status::invalid_input, std::string("merge: --") + key + " must be a path"); a = args.at(key).str(); }
    if (!a.empty() && !f.empty() && a != f) throw Error(Status::invalid_input, std::string("merge: --") + key + " differs from the manifest's " + name);
    if (a.empty() && f.empty()) throw Error(Status::invalid_input, std::string("merge: no ") + name + " (give --" + key + " or a manifest input)");
    return a.empty() ? f : a;
  };
  in.data = path_arg("data", "data.bin"); in.setup = path_arg("setup", "setup.bin"); in.calib = path_arg("calib", "calib.bin");
  if (!args.contains("out") || args.at("out").type() != Json::STR || args.at("out").str().empty())
    throw Error(Status::invalid_input, "merge: --out is required");   // review PR20 m-4: no default output path
  in.out = args.at("out").str();
  // R' (never from the list's length): the manifest's params.Rp when a manifest is given, else --Rp
  auto whole = [](const Json& v, const char* what) {
    if (v.type() != Json::NUM) throw Error(Status::invalid_input, std::string("merge: ") + what + " must be a number");
    const double x = v.num();
    if (!(x >= 1) || x != std::floor(x) || x > 1e6) throw Error(Status::invalid_input, std::string("merge: ") + what + " must be a whole number in [1, 10^6]");
    return (int)x;
  };
  const bool man_rp = has_man && in.manifest.contains("params") && in.manifest.at("params").contains("Rp");
  if (man_rp) {
    in.Rp = whole(in.manifest.at("params").at("Rp"), "manifest params.Rp");
    if (args.contains("Rp") && whole(args.at("Rp"), "--Rp") != in.Rp) throw Error(Status::invalid_input, "merge: --Rp differs from the manifest's params.Rp");
  } else {
    if (!args.contains("Rp")) throw Error(Status::invalid_input, "merge: R' must be given (manifest params.Rp or --Rp)");
    in.Rp = whole(args.at("Rp"), "--Rp");
  }
  // the manifest's island_<r>.bin inputs, r = 1..R' each exactly once (index digits bounded: n-4)
  std::vector<std::string> man_islands;
  { std::map<int, std::string> by_r;
    for (auto& [k, v] : minp.items()) {
      const std::string b = base_name(k);
      if (b.rfind("island_", 0) != 0 || b.size() < 12 || b.substr(b.size() - 4) != ".bin") continue;
      const std::string num = b.substr(7, b.size() - 11);
      if (num.empty() || num.size() > 9 || num.find_first_not_of("0123456789") != std::string::npos)
        throw Error(Status::invalid_input, "merge: bad island input name " + b);
      const int r = std::stoi(num);
      if (by_r.count(r)) throw Error(Status::invalid_input, "merge: island " + num + " named twice in the manifest");
      by_r[r] = k;
    }
    if (!by_r.empty()) {
      for (auto& [r, k] : by_r) if (r < 1 || r > in.Rp) throw Error(Status::invalid_input, "merge: island index " + std::to_string(r) + " outside 1..R'");
      for (int r = 1; r <= in.Rp; ++r) {
        if (!by_r.count(r)) throw Error(Status::invalid_input, "merge: island " + std::to_string(r) + " of R' = " + std::to_string(in.Rp) + " is not in the manifest");
        man_islands.push_back(by_r[r]);
      }
    } else if (man_rp) throw Error(Status::invalid_input, "merge: the manifest names no island inputs");
  }
  // explicit islands: a JSON array or the CLI's comma-separated string; island r = position r
  if (args.contains("islands")) {
    const Json& il = args.at("islands");
    if (il.type() == Json::ARR) {
      for (auto& x : il.elems()) { if (x.type() != Json::STR || x.str().empty()) throw Error(Status::invalid_input, "merge: --islands entries must be paths"); in.islands.push_back(x.str()); }
    } else if (il.type() == Json::STR) {
      const std::string t = il.str();
      size_t a = 0;
      while (a <= t.size()) {
        size_t b = t.find(',', a);
        if (b == std::string::npos) b = t.size();
        const std::string x = t.substr(a, b - a);
        if (x.empty()) throw Error(Status::invalid_input, "merge: empty entry in --islands");
        in.islands.push_back(x);
        a = b + 1;
      }
    } else throw Error(Status::invalid_input, "merge: --islands must be a list of paths");
    std::vector<std::string> sorted = in.islands; std::sort(sorted.begin(), sorted.end());
    if (std::adjacent_find(sorted.begin(), sorted.end()) != sorted.end()) throw Error(Status::invalid_input, "merge: an island path appears twice");
    if (!man_islands.empty() && in.islands != man_islands) throw Error(Status::invalid_input, "merge: --islands differs from the manifest's island inputs (r = 1..R')");
  } else in.islands = man_islands;
  if ((int)in.islands.size() != in.Rp)
    throw Error(Status::invalid_input, "merge: " + std::to_string(in.islands.size()) + " island files for R' = " + std::to_string(in.Rp) + " (no subset is ever pooled)");
  // mode: --mode or the manifest's; both given must agree
  const std::string am = args.contains("mode") && args.at("mode").type() == Json::STR ? args.at("mode").str() : "";
  const std::string mm = in.manifest.contains("mode") && in.manifest.at("mode").type() == Json::STR ? in.manifest.at("mode").str() : "";
  if (!am.empty() && !mm.empty() && am != mm) throw Error(Status::invalid_input, "merge: --mode differs from the manifest's mode");
  const std::string mode = am.empty() ? mm : am;
  if (mode.empty()) throw Error(Status::invalid_input, "merge: mode not given (--mode or the manifest's mode)");
  in.mode = fmt::mode_from_name(mode);
  return in;
}

Json run(const Json& args) {
  auto t0 = std::chrono::steady_clock::now();
  MergeInputs in = parse_merge_inputs(args);
  const uint32_t mode = in.mode;
  const Json minp = in.manifest.contains("inputs") ? in.manifest.at("inputs") : Json::object();
  auto want = [&](const std::string& path) {   // the manifest's content hash for this input: exact path, else a unique base name
    if (minp.contains(path)) return minp.at(path).str();
    std::string found; int n = 0;
    for (auto& [k, v] : minp.items()) if (base_name(k) == base_name(path) && v.type() == Json::STR) { found = v.str(); ++n; }
    return n == 1 ? found : std::string();
  };
  std::string dhash;
  Data D = prep::load_data(in.data, &dhash);
  wp4io::SetupView S = wp4io::read_setup(in.setup, D.p, D.K, &D.zob);
  wp4io::CalibIn C = wp4io::read_calib(in.calib, D.p, D.K, dhash, S.content_hash);   // calib.bin tied to this data / setup (PR37 m-3)
  for (auto pr : {std::make_pair(in.data, dhash), std::make_pair(in.setup, S.content_hash), std::make_pair(in.calib, C.content_hash)}) {
    std::string w = want(pr.first);
    if (!w.empty() && w != pr.second) throw Error(Status::invalid_input, pr.first + ": content hash differs from the manifest");
  }
  if (C.status != "ok") throw Error(Status::invalid_input, "calib.bin status " + C.status + ": no frozen grid");
  if (C.mode != mode) throw Error(Status::invalid_input, "calib.bin mode differs from the merge mode");
  const int R = in.Rp;
  wp4io::Expect ex; ex.mode = mode; ex.data_hash = dhash; ex.setup_hash = S.content_hash; ex.calib_hash = C.content_hash;
  ex.grid = C.grid; ex.L = C.L; ex.Hm = C.Hm; ex.K = D.K; ex.tier = C.tier; ex.zob = &D.zob;
  for (int r = 0; r < R; ++r) ex.island_hash.push_back(want(in.islands[(size_t)r]));
  wp4io::FileIslandSource src(in.islands, ex, R, D.p);   // pass 1: heads + binary check
  LedgerConfig cfg; cfg.p = D.p; cfg.islands = R; cfg.leaders = false; cfg.fresh_counters = false;   // v0.1.7: no final-run leaders
  Ledger pre(cfg);
  wp4io::offer_tables(pre, S, D.K, D.zob);
  offer_inherited(pre, C.inherited, C.has_hpm, C.hpm, C.hpm_ev, D.zob);
  pre.compact();
  MergeSettings ms;
  ms.Rp = R; ms.N = C.N; ms.p = D.p; ms.K = D.K; ms.tier = C.tier;
  ms.ell = (int)nget(args, "ell", ceil_log2((double)D.n + D.p + 1));
  ms.ls0 = true; ms.ls0_ell = ms.ell; ms.log_m0 = D.logm0;
  ms.threads = (int)nget(args, "threads", 1); ms.chunk = (size_t)nget(args, "chunk", 2048); ms.zob = &D.zob;
  // --mem-budget: bytes (INTERFACES §7), whole task; --mem-budget-gb: alias in GiB
  // (review PR20 re-check n-4: a finite whole number of bytes in [0, 2^50]; 0 = off as INTERFACES §7 says; negative,
  // fractional, NaN or absurd values are refused before any cast)
  auto budget = [](const Json& v, double scale, const char* what) {
    if (v.type() != Json::NUM) throw Error(Status::invalid_input, std::string("merge: ") + what + " must be a number");
    const double x = v.num() * scale;
    if (!std::isfinite(x) || x < 0 || x > 1125899906842624.0 || x != std::floor(x))
      throw Error(Status::invalid_input, std::string("merge: ") + what + " must be a whole number of bytes in [0, 2^50] (0 = off)");
    return (uint64_t)x;
  };
  if (args.contains("mem_budget") && args.contains("mem_budget_gb")) throw Error(Status::invalid_input, "merge: give --mem-budget or --mem-budget-gb, not both");
  if (args.contains("mem_budget")) ms.mem_budget_bytes = budget(args.at("mem_budget"), 1.0, "--mem-budget");
  else if (args.contains("mem_budget_gb")) ms.mem_budget_bytes = budget(Json(std::floor(args.at("mem_budget_gb").num() * 1073741824.0)), 1.0, "--mem-budget-gb");
  // memory plan (review PR20 m-2): mean model size from the islands' store sections; the rest of the task = data.bin
  // (X mapped) + setup.bin (arrays and table stores, x 2.5 for the stores' staging)
  { double kb = 1;
    for (auto& h : src.heads()) if (h.store_entries) kb = std::max(kb, (double)h.store_pool / (double)h.store_entries);
    ms.kbar = kb;
    struct stat a{}, b{};
    uint64_t dsz = ::stat(in.data.c_str(), &a) == 0 ? (uint64_t)a.st_size : 0, ssz = ::stat(in.setup.c_str(), &b) == 0 ? (uint64_t)b.st_size : 0;
    ms.extra_bytes = dsz + (uint64_t)(2.5 * (double)ssz); }
  BitFactory fac{&D, &S};
  FitOut fo = merge_stream(src, std::move(pre), S.mode_S, fac, ms);
  std::string why;
  for (auto& h : src.heads()) if (h.load != Load::ok) why += (why.empty() ? "" : "; ") + h.detail;
  if (!why.empty()) fo.reason += " [" + why + "]";
  wp4io::FitWrite fw; fw.mode = mode; fw.fo = &fo; fw.ms = &ms;
  fw.inputs["data.bin"] = dhash; fw.inputs["setup.bin"] = S.content_hash; fw.inputs["calib.bin"] = C.content_hash;
  // review PR20 m-1: the content hash actually read ("" only for a file that could not be read)
  for (int r = 0; r < R; ++r) fw.inputs["island_" + std::to_string(r + 1) + ".bin"] = src.heads()[(size_t)r].content_hash;
  fw.timings["merge_tail_seconds"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  Json rec = Json::object();
  wp4io::write_fit(in.out, fw, &rec);
  rec["command"] = "merge"; rec["Rp"] = R;
  if (fo.status != Status::completed) rec["exit_status"] = status_name(fo.status);
  return rec;
}
}  // namespace v4::merge
