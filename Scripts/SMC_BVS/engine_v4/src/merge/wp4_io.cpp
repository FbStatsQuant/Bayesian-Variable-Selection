// wp4_io.cpp -- WP4 file I/O and the merge command (see include/v4/wp4_io.h).
#include "v4/wp4_io.h"

#include <sys/stat.h>
#include <algorithm>
#include <chrono>
#include <cmath>
#include "v4/pmath.h"
#include "v4/prep.h"
#include "v4/provenance.h"
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

// ---------------------------------------------------------------------------------------------------- generic sections
void add_store(fmt::Writer& W, Json& meta, const std::string& prefix, const Store& s) {
  if (s.staging() != 0) throw Error(Status::internal_error, "add_store: store " + prefix + " is not compacted");
  W.add(prefix + "_v", s.v); W.add(prefix + "_off", s.off); W.add(prefix + "_len", s.len);
  W.add(prefix + "_hash", s.hash); W.add(prefix + "_pool", s.pool);
  Json d = Json::object(); d["cap"] = u64_json(s.cap); d["order"] = s.ord == Order::HPM ? "HPM" : "LEX"; d["size"] = u64_json(s.size());
  meta["stores"][prefix] = d;
}
void read_store(const fmt::Reader& R, const Json& meta, const std::string& prefix, Store& s) {
  const Json& d = meta.at("stores").at(prefix);
  s.init(u64_of(d.at("cap")), d.at("order").str() == "HPM" ? Order::HPM : Order::LEX);
  uint64_t n = 0, no = 0, nl = 0, nh = 0, np = 0;
  const double* v = R.get<double>(prefix + "_v", &n);
  const uint64_t* off = R.get<uint64_t>(prefix + "_off", &no);
  const uint16_t* len = R.get<uint16_t>(prefix + "_len", &nl);
  const uint64_t* h = R.get<uint64_t>(prefix + "_hash", &nh);
  const int32_t* pool = R.get<int32_t>(prefix + "_pool", &np);
  if (no != n || nl != n || nh != n || n > s.cap) throw Error(Status::invalid_input, "store " + prefix + ": inconsistent sections");
  for (uint64_t i = 0; i < n; ++i) {
    if (off[i] + len[i] > np) throw Error(Status::invalid_input, "store " + prefix + ": pool out of range");
    s.offer(v[i], ModelView(pool + off[i], len[i]), h[i]);
  }
  s.compact();
  if (s.size() != n || !s.check_invariants()) throw Error(Status::invalid_input, "store " + prefix + ": not a valid sorted store (I1)");
}
void add_models(fmt::Writer& W, const std::string& prefix, const std::vector<Model>& ms) {
  std::vector<int64_t> ptr{0}; std::vector<int32_t> idx;
  for (auto& m : ms) { idx.insert(idx.end(), m.begin(), m.end()); ptr.push_back((int64_t)idx.size()); }
  add_vec_copy(W, prefix + "_ptr", ptr); add_vec_copy(W, prefix + "_idx", idx);
}
std::vector<Model> read_models(const fmt::Reader& R, const std::string& prefix) {
  uint64_t np = 0, ni = 0;
  const int64_t* ptr = R.get<int64_t>(prefix + "_ptr", &np);
  const int32_t* idx = R.get<int32_t>(prefix + "_idx", &ni);
  std::vector<Model> out;
  for (uint64_t i = 0; i + 1 < np; ++i) {
    if (ptr[i] < 0 || ptr[i + 1] < ptr[i] || (uint64_t)ptr[i + 1] > ni) throw Error(Status::invalid_input, prefix + ": bad ptr");
    out.emplace_back(idx + ptr[i], idx + ptr[i + 1]);
  }
  return out;
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
  e.phase = index_of(phase_name, N_PHASE, j.at("phase").str()); e.mech = index_of(mech_name, N_MECH, j.at("mechanism").str());
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
  if (co.has_frozen) {
    meta["refine_m"] = co.frozen.refine_m; meta["grid_label"] = co.frozen.grid_label;
    add_vec_copy(W, "grid", co.frozen.grid); add_vec_copy(W, "grid_unrefined", co.frozen.grid_unrefined);
    if (co.frozen.has_rho) add_vec_copy(W, "rho_V", co.frozen.rho_V);
  }
  std::vector<int64_t> gptr{0}; std::vector<double> gall;
  for (auto& g : grids_all) { gall.insert(gall.end(), g.begin(), g.end()); gptr.push_back((int64_t)gall.size()); }
  add_vec_copy(W, "grids_all_ptr", gptr); add_vec_copy(W, "grids_all", gall);
  if (c.led) {
    add_store(W, meta, "cstore_top", c.led->top);
    if (c.led->lead0.cap) add_store(W, meta, "cstore_lead0", c.led->lead0);
    if (c.led->lead1.cap) add_store(W, meta, "cstore_lead1", c.led->lead1);
    add_ledger_tally(W, meta, *c.led);
  } else meta["has_hpm"] = false;
  std::vector<Model> im; std::vector<double> iF, ilg0, ilogm;
  for (auto& m : c.inherited) { im.push_back(m.S); iF.push_back(m.F); ilg0.push_back(m.lg0); ilogm.push_back(m.logm); }
  add_models(W, "inh", im); add_vec_copy(W, "inh_F", iF); add_vec_copy(W, "inh_lg0", ilg0); add_vec_copy(W, "inh_logm", ilogm);
  meta["inputs"] = c.inputs; meta["binary"] = binary_block(); meta["mode"] = fmt::mode_name(c.mode);
  W.add_json("meta", meta);
  return W.write(path);
}
CalibIn read_calib(const std::string& path) {
  fmt::Reader R(path);
  if (R.kind() != fmt::K_CALIB) throw Error(Status::invalid_input, path + ": not a calib file");
  CalibIn c; c.content_hash = R.content_hash(); c.mode = R.mode(); c.meta = R.json("meta");
  c.status = c.meta.at("status").str();
  c.tier = (int32_t)c.meta.at("tier").num(); c.N = (int32_t)c.meta.at("N").num(); c.L = (int32_t)c.meta.at("L").num();
  c.Hm = (int32_t)c.meta.at("Hm").num();
  if (R.has("grid")) c.grid = R.vec<double>("grid");
  c.has_hpm = c.meta.at("has_hpm").boolean();
  if (c.has_hpm) { c.hpm = R.vec<int32_t>("hpm_S"); c.hpm_ev = event_from_json(c.meta.at("hpm_ev")); c.hpm_ev.key.seg = SG_CALIB; }
  std::vector<Model> im = read_models(R, "inh");
  std::vector<double> iF = R.vec<double>("inh_F"), ilg0 = R.vec<double>("inh_lg0"), ilogm = R.vec<double>("inh_logm");
  if (iF.size() != im.size() || ilg0.size() != im.size() || ilogm.size() != im.size()) throw Error(Status::invalid_input, "calib: inherited arrays differ in length");
  for (size_t i = 0; i < im.size(); ++i) c.inherited.push_back({im[i], iF[i], ilg0[i], ilogm[i]});
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
    std::vector<int64_t> tptr{0}; std::vector<int32_t> tS;   // WP3 names: terminal_S_ptr i64 [N+1], terminal_S i32
    for (auto& S : isl.terminal) { tS.insert(tS.end(), S.begin(), S.end()); tptr.push_back((int64_t)tS.size()); }
    add_vec_copy(W, "terminal_S_ptr", tptr); add_vec_copy(W, "terminal_S", tS);
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
    h.status = status_from_name(meta.at("status").str());
    h.logZ = h.status == Status::completed ? R.vec<double>("logZ").at(0) : 0.0;
    if (binary_out) *binary_out = meta.at("binary");
    h.load = merge::Load::ok;
  } catch (const std::exception& e) {
    h = merge::IslandHead(); h.load = merge::Load::corrupt; h.detail = path + ": " + e.what();
  }
  return h;
}

merge::IslandIn load_island_full(const std::string& path, int Rp, int p) {
  fmt::Reader R(path);
  Json meta = R.json("meta");
  merge::IslandIn I;
  I.r = (int32_t)meta.at("r").num(); I.N = (int32_t)meta.at("N").num(); I.T = (int32_t)meta.at("T").num();
  I.L = (int32_t)meta.at("L").num(); I.Hm = (int32_t)meta.at("Hm").num();
  I.status = status_from_name(meta.at("status").str()); I.message = str_or(meta, "reason", "");
  if ((int)meta.at("p").num() != p) throw Error(Status::invalid_input, path + ": p differs from data.bin");
  std::vector<double> grid = R.vec<double>("grid");
  I.ess = R.vec<double>("st_ess");
  LedgerConfig cfg; cfg.p = p; cfg.islands = Rp; cfg.leaders = false; cfg.fresh_counters = false;   // v0.1.7: no leaders
  I.led.init(cfg);
  { uint64_t n = 0, no = 0, nl = 0, nh = 0, np = 0;
    const double* v = R.get<double>("top_v", &n); const uint64_t* off = R.get<uint64_t>("top_off", &no);
    const uint16_t* len = R.get<uint16_t>("top_len", &nl); const uint64_t* hh = R.get<uint64_t>("top_hash", &nh);
    const int32_t* pool = R.get<int32_t>("top_pool", &np);
    if (no != n || nl != n || nh != n || n > I.led.top.cap) throw Error(Status::invalid_input, path + ": inconsistent top store");
    for (uint64_t i = 0; i < n; ++i) {
      if (off[i] + len[i] > np) throw Error(Status::invalid_input, path + ": top pool out of range");
      I.led.top.offer(v[i], ModelView(pool + off[i], len[i]), hh[i]);
    }
    I.led.top.compact();
    if (I.led.top.size() != n || !I.led.top.check_invariants()) throw Error(Status::invalid_input, path + ": top store not sorted / unique (I1)");
  }
  { std::vector<int32_t> hs = R.vec<int32_t>("hpm_S"); std::vector<double> hv = R.vec<double>("hpm_val"); std::vector<int64_t> ev = R.vec<int64_t>("hpm_ev");
    if (hv.size() != 2 || ev.size() != 12) throw Error(Status::invalid_input, path + ": hpm_val / hpm_ev size");
    I.led.has_hpm = I.led.top.size() > 0; I.led.hpmS = Model(hs.begin(), hs.end()); I.led.hpmF = hv[0]; I.led.hpm_logm = hv[1];
    EventKey& k = I.led.hpm_ev.key;
    k.seg = (uint8_t)ev[0]; k.tier = (uint8_t)ev[1]; k.iter = (int8_t)ev[2]; k.unit = (uint32_t)ev[3]; k.xph = (uint8_t)ev[4];
    k.stage = (uint32_t)ev[5]; k.round = (uint32_t)ev[6]; k.particle = (uint32_t)ev[7]; k.position = (uint32_t)ev[8]; k.sub = (uint8_t)ev[9];
    I.led.hpm_ev.phase = (int)ev[10]; I.led.hpm_ev.mech = (int)ev[11];
    // phi is not in hpm_ev: v3's values by phase (INIT 0, BRIDGE grid[stage], BURN / MEASURED 1)
    I.led.hpm_ev.phi = k.xph == X_BRIDGE && k.stage < grid.size() ? grid[k.stage] : (k.xph == X_BURN || k.xph == X_MEASURED) ? 1.0 : 0.0;
  }
  { std::vector<double> ib = R.vec<double>("island_best");
    for (size_t i = 0; i < ib.size() && i < I.led.island_best.size(); ++i) I.led.island_best[i] = ib[i]; }
  { uint64_t n = 0; const uint64_t* lg = R.get<uint64_t>("logical", &n);
    if (n != (uint64_t)N_PHASE * N_MECH) throw Error(Status::invalid_input, path + ": logical size");
    for (int a = 0; a < N_PHASE; ++a) for (int b = 0; b < N_MECH; ++b) I.led.logical[a][b] = lg[(size_t)a * N_MECH + b]; }
  if (I.status == Status::completed) {
    I.logZ = R.vec<double>("logZ").at(0);
    I.rb_acc = R.vec<double>("rb_acc"); I.pip = R.vec<double>("pip_r");
    if ((int)I.pip.size() != p) throw Error(Status::invalid_input, path + ": pip_r has the wrong length");
    std::vector<double> rr = R.vec<double>("rb_round");
    if (p > 0 && rr.size() != (size_t)I.Hm * (size_t)p) throw Error(Status::invalid_input, path + ": rb_round is not Hm x p");
    for (int h = 0; h < I.Hm; ++h) I.rb_round.emplace_back(rr.begin() + (size_t)h * p, rr.begin() + (size_t)(h + 1) * p);
    I.terminal = merge::read_terminal_supports(R, I.N, p);
  }
  return I;
}

merge::IslandSlot load_island(const std::string& path, int r, const Expect& ex, int p, Json* binary_out) {
  merge::IslandSlot s;
  merge::IslandHead h = head_island(path, r, ex, binary_out);
  s.load = h.load; s.detail = h.detail;
  if (h.load != merge::Load::ok) return s;
  try { s.isl = load_island_full(path, std::max(1, h.r), p); }
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
FileIslandSource::FileIslandSource(std::vector<std::string> paths, const Expect& ex, int Rp, int p) : paths_(std::move(paths)), Rp_(Rp), p_(p) {
  std::vector<Json> blocks(paths_.size());
  for (size_t r = 1; r <= paths_.size(); ++r) heads_.push_back(head_island(paths_[r - 1], (int)r, ex, &blocks[r - 1]));
  check_binaries(heads_, blocks, ex.mode);
}
merge::IslandIn FileIslandSource::load(int r) {
  try { return load_island_full(paths_[(size_t)r - 1], Rp_, p_); }
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
SetupView read_setup(const std::string& path) {
  fmt::Reader R(path);
  if (R.kind() != fmt::K_SETUP) throw Error(Status::invalid_input, path + ": not a setup file");
  SetupView s; s.content_hash = R.content_hash();
  Json meta = R.json("meta");
  s.blk = R.vec<int32_t>("blk"); s.pos = R.vec<int32_t>("pos"); s.code_ptr = R.vec<int64_t>("code_ptr"); s.logr = R.vec<double>("logr");
  s.blk_ptr = R.vec<int64_t>("blk_ptr"); s.blk_members = R.vec<int32_t>("blk_members"); s.mode_S = R.vec<int32_t>("mode_S");
  read_store(R, meta, "tstore_top", s.ttop);
  if (R.has("tstore_lead0_v")) read_store(R, meta, "tstore_lead0", s.tlead0);
  if (R.has("tstore_lead1_v")) read_store(R, meta, "tstore_lead1", s.tlead1);
  return s;
}
std::string write_setup_min(const std::string& path, const SetupView& s, const Json& inputs) {
  fmt::Writer W(fmt::K_SETUP, fmt::M_COMPAT);
  Json meta = Json::object();
  W.add("blk", s.blk); W.add("pos", s.pos); W.add("code_ptr", s.code_ptr); W.add("logr", s.logr);
  W.add("blk_ptr", s.blk_ptr); W.add("blk_members", s.blk_members); W.add("mode_S", s.mode_S);
  add_store(W, meta, "tstore_top", s.ttop);
  if (s.tlead0.cap) add_store(W, meta, "tstore_lead0", s.tlead0);
  if (s.tlead1.cap) add_store(W, meta, "tstore_lead1", s.tlead1);
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
std::string sget(const Json& a, const std::string& k, const std::string& d = "") { return a.contains(k) ? a.at(k).str() : d; }
double nget(const Json& a, const std::string& k, double d) { return a.contains(k) ? a.at(k).num() : d; }
}  // namespace

// args: data, setup, calib, islands [paths, r = 1..R'], out (fit.bin), mode (compat | law | V), threads, chunk,
// manifest (optional: inputs {name: content hash} for data/setup/calib/islands), ell (test override).
Json run(const Json& args) {
  auto t0 = std::chrono::steady_clock::now();
  const uint32_t mode = fmt::mode_from_name(sget(args, "mode", "compat"));
  Json man = args.contains("manifest") ? read_json_file(args.at("manifest").str()) : Json::object();
  const Json& minp = man.contains("inputs") ? man.at("inputs") : Json::object();
  auto want = [&](const std::string& path, const std::string& name) {
    std::string base = path.substr(path.find_last_of('/') + 1);
    return minp.contains(path) ? minp.at(path).str() : minp.contains(base) ? minp.at(base).str() : minp.contains(name) ? minp.at(name).str() : std::string();
  };
  const std::string dpath = sget(args, "data"), spath = sget(args, "setup"), cpath = sget(args, "calib"), out = sget(args, "out", "fit.bin");
  std::string dhash;
  Data D = prep::load_data(dpath, &dhash);
  wp4io::SetupView S = wp4io::read_setup(spath);
  wp4io::CalibIn C = wp4io::read_calib(cpath);
  for (auto pr : {std::make_pair(dpath, dhash), std::make_pair(spath, S.content_hash), std::make_pair(cpath, C.content_hash)}) {
    std::string w = want(pr.first, pr.first == dpath ? "data.bin" : pr.first == spath ? "setup.bin" : "calib.bin");
    if (!w.empty() && w != pr.second) throw Error(Status::invalid_input, pr.first + ": content hash differs from the manifest");
  }
  if (C.status != "ok") throw Error(Status::invalid_input, "calib.bin status " + C.status + ": no frozen grid");
  if (C.mode != mode) throw Error(Status::invalid_input, "calib.bin mode differs from the merge mode");
  const Json& il = args.at("islands");
  const int R = (int)il.size();
  wp4io::Expect ex; ex.mode = mode; ex.data_hash = dhash; ex.setup_hash = S.content_hash; ex.calib_hash = C.content_hash;
  for (int r = 0; r < R; ++r) ex.island_hash.push_back(want(il.at((size_t)r).str(), "island_" + std::to_string(r + 1) + ".bin"));
  std::vector<std::string> paths; for (int r = 0; r < R; ++r) paths.push_back(il.at((size_t)r).str());
  wp4io::FileIslandSource src(paths, ex, R, D.p);   // pass 1: heads + binary check
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
  ms.mem_budget_bytes = (uint64_t)(nget(args, "mem_budget_gb", 0) * 1073741824.0);   // --mem-budget (GiB); 0 = off
  BitFactory fac{&D, &S};
  FitOut fo = merge_stream(src, std::move(pre), S.mode_S, fac, ms);
  std::string why;
  for (auto& h : src.heads()) if (h.load != Load::ok) why += (why.empty() ? "" : "; ") + h.detail;
  if (!why.empty()) fo.reason += " [" + why + "]";
  wp4io::FitWrite fw; fw.mode = mode; fw.fo = &fo; fw.ms = &ms;
  fw.inputs["data.bin"] = dhash; fw.inputs["setup.bin"] = S.content_hash; fw.inputs["calib.bin"] = C.content_hash;
  for (int r = 0; r < R; ++r) fw.inputs["island_" + std::to_string(r + 1) + ".bin"] = ex.island_hash[(size_t)r];
  fw.timings["merge_tail_seconds"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  Json rec = Json::object();
  wp4io::write_fit(out, fw, &rec);
  rec["command"] = "merge";
  if (fo.status != Status::completed) rec["exit_status"] = status_name(fo.status);
  return rec;
}
}  // namespace v4::merge
