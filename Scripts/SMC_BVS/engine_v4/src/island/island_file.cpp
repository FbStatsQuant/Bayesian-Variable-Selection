// island_file.cpp -- island_r.bin writer and reader (see include/v4/island/island_file.h).
#include "v4/island/island_file.h"
#include <cstdio>
#include <cstring>
#include "v4/format.h"
#include "v4/provenance.h"

namespace v4::island {

static std::string hex64(uint64_t x) { char b[19]; std::snprintf(b, sizeof b, "0x%016llx", (unsigned long long)x); return b; }
static void moves_row(const MoveStats& m, std::vector<uint64_t>& out) {
  uint64_t f[MOVE_FIELDS] = {m.gibbs, m.gibbs_change, m.us_exec, m.us_acc, m.us_self, m.ns_exec, m.ns_acc, m.ns_noscore, m.ns_self, m.in_exec, m.in_acc, m.gibbs_cap};
  out.insert(out.end(), f, f + MOVE_FIELDS);
}
static MoveStats moves_from(const uint64_t* f) {
  MoveStats m; m.gibbs = f[0]; m.gibbs_change = f[1]; m.us_exec = f[2]; m.us_acc = f[3]; m.us_self = f[4]; m.ns_exec = f[5];
  m.ns_acc = f[6]; m.ns_noscore = f[7]; m.ns_self = f[8]; m.in_exec = f[9]; m.in_acc = f[10]; m.gibbs_cap = f[11]; return m;
}
static const char* status_str(int s) { return s == 0 ? "completed" : (s == 2 ? "numerical_failure" : "resource_limit"); }

std::string write_island_file(const std::string& path, const IslandRun& r, Arith arith, const Json& inputs) {
  if (r.status == 1)   // `interrupted` (stop_after_step) is a test outcome, never a file (review m3)
    throw Error(Status::internal_error, "write_island_file: an interrupted island (stop_after_step) has no island file");
  fmt::Writer w(fmt::K_ISLAND, r.compat ? fmt::M_COMPAT : (arith == Arith::ClassA ? fmt::M_V : fmt::M_LAW));
  const bool done = r.status == 0;
  uint64_t lz; std::memcpy(&lz, &r.logZ, 8);
  Json m = Json::object();
  m["schema"] = "smcbvs4.island/1"; m["kind"] = "island"; m["mode"] = r.compat ? "compat" : (arith == Arith::ClassA ? "V" : "law");
  if (r.compat) m["stream_count"] = hex64(r.stream_count);
  m["r"] = r.r; m["N"] = r.N; m["T"] = r.T; m["L"] = r.L; m["Hm"] = r.Hm; m["p"] = r.p;
  m["status"] = status_str(r.status); m["reason"] = r.reason; m["inputs"] = inputs; m["binary"] = binary_block();
  m["init_hash"] = hex64(r.init_hash); m["output_hash"] = hex64(r.hash());
  if (done) { m["logZ"] = r.logZ; m["logZ_hex"] = hex64(lz); }
  Json t = Json::object(); t["total"] = r.ks.t_total; t["init"] = r.ks.t_init; m["timings"] = t;
  w.add_json("meta", m);
  // stage table and terminal rounds (no estimate content; written in every status)
  const size_t T = r.stages.size();
  std::vector<double> phi(T), inc(T), ess(T), cum(T); std::vector<int32_t> dr(T), dm(T); std::vector<uint64_t> mv, tmv;
  for (size_t i = 0; i < T; ++i) { auto& s = r.stages[i]; phi[i] = s.phi; inc[i] = s.inc; ess[i] = s.ess; cum[i] = s.cum; dr[i] = s.distinct_res; dm[i] = s.distinct_moved; moves_row(s.moves, mv); }
  for (auto& x : r.terminal_moves) moves_row(x, tmv);
  w.add_copy("grid", fmt::D_F64, r.grid.data(), r.grid.size() * 8, r.grid.size(), 0);
  w.add_copy("st_phi", fmt::D_F64, phi.data(), T * 8, T, 0); w.add_copy("st_ess", fmt::D_F64, ess.data(), T * 8, T, 0);
  if (done) { w.add_copy("st_inc", fmt::D_F64, inc.data(), T * 8, T, 0); w.add_copy("st_cum", fmt::D_F64, cum.data(), T * 8, T, 0); }   // estimates: GUARD-W (m2)
  w.add_copy("st_distinct_res", fmt::D_I32, dr.data(), T * 4, T, 0); w.add_copy("st_distinct_moved", fmt::D_I32, dm.data(), T * 4, T, 0);
  w.add_copy("st_moves", fmt::D_U64, mv.data(), mv.size() * 8, T, MOVE_FIELDS);
  w.add_copy("term_moves", fmt::D_U64, tmv.data(), tmv.size() * 8, r.terminal_moves.size(), MOVE_FIELDS);
  w.add("term_distinct", r.terminal_distinct);
  // ledger
  w.add("top_v", r.top_v); w.add("top_hash", r.top_hash); w.add("top_off", r.top_off); w.add("top_len", r.top_len); w.add("top_pool", r.top_pool);
  // no leader stores in island_r.bin, in any mode (INTERFACES v0.1.7 §4.1/§5.1; D-7)
  w.add("hpm_S", r.hpm.S);
  double hv[2] = {r.hpm.F, r.hpm.logm}; w.add_copy("hpm_val", fmt::D_F64, hv, 16, 2, 0);
  const EventKey& k = r.hpm.key;
  int64_t ev[12] = {k.seg, k.tier, k.iter, (int64_t)k.unit, k.xph, (int64_t)k.stage, (int64_t)k.round, (int64_t)k.particle, (int64_t)k.position, k.sub, r.hpm.phase, r.hpm.mech};
  w.add_copy("hpm_ev", fmt::D_I64, ev, sizeof ev, 12, 0);
  std::vector<double> ib((size_t)std::max(0, r.r) + 1, NEG_INF); if (r.r >= 0) ib[(size_t)r.r] = r.island_best;
  w.add_copy("island_best", fmt::D_F64, ib.data(), ib.size() * 8, ib.size(), 0);
  w.add_copy("logical", fmt::D_U64, &r.logical[0][0], sizeof(r.logical), N_PHASE, N_MECH);
  // estimates (GUARD-W)
  std::vector<double> rbr; std::vector<int64_t> tptr; std::vector<int32_t> tS;
  if (done) {
    w.add_copy("logZ", fmt::D_F64, &r.logZ, 8, 1, 0);
    w.add("rb_acc", r.rb_acc); w.add("pip_r", r.pip);
    for (auto& v : r.rb_round) rbr.insert(rbr.end(), v.begin(), v.end());
    w.add_copy("rb_round", fmt::D_F64, rbr.data(), rbr.size() * 8, r.rb_round.size(), (uint64_t)r.p);
    tptr.push_back(0); for (auto& S : r.terminal) { tS.insert(tS.end(), S.begin(), S.end()); tptr.push_back((int64_t)tS.size()); }
    w.add_copy("terminal_S_ptr", fmt::D_I64, tptr.data(), tptr.size() * 8, tptr.size(), 0);
    w.add_copy("terminal_S", fmt::D_I32, tS.data(), tS.size() * 4, tS.size(), 0);
  }
  return w.write(path);
}

IslandFile read_island_file(const std::string& path, bool verify) {
  fmt::Reader rd(path, verify);
  if (rd.kind() != fmt::K_ISLAND) throw Error(Status::invalid_input, path + ": not an island file");
  IslandFile f; f.content_hash = rd.content_hash(); f.meta = rd.json("meta");
  auto& o = f.rec;
  const std::string st = f.meta.at("status").str();
  o.status = st == "completed" ? Status::completed : (st == "numerical_failure" ? Status::numerical_failure : Status::resource_limit);
  o.r = (int32_t)f.meta.at("r").i64(); o.N = (int32_t)f.meta.at("N").i64(); o.T = (int32_t)f.meta.at("T").i64();
  o.L = (int32_t)f.meta.at("L").i64(); o.Hm = (int32_t)f.meta.at("Hm").i64();
  const int p = (int)f.meta.at("p").i64();
  f.grid = rd.vec<double>("grid");
  auto phi = rd.vec<double>("st_phi"), ess = rd.vec<double>("st_ess");
  std::vector<double> inc(phi.size(), 0.0), cum(phi.size(), 0.0);
  if (rd.has("st_inc")) { inc = rd.vec<double>("st_inc"); cum = rd.vec<double>("st_cum"); }
  auto dr = rd.vec<int32_t>("st_distinct_res"), dm = rd.vec<int32_t>("st_distinct_moved");
  auto mv = rd.vec<uint64_t>("st_moves"), tmv = rd.vec<uint64_t>("term_moves");
  for (size_t i = 0; i < phi.size(); ++i) { StageRow s; s.phi = phi[i]; s.inc = inc[i]; s.ess = ess[i]; s.cum = cum[i]; s.distinct_res = dr[i]; s.distinct_moved = dm[i]; s.moves = moves_from(&mv[i * MOVE_FIELDS]); o.stages.push_back(s); }
  for (size_t i = 0; i * MOVE_FIELDS < tmv.size(); ++i) o.terminal_moves.push_back(moves_from(&tmv[i * MOVE_FIELDS]));
  o.terminal_distinct = rd.vec<int32_t>("term_distinct");
  LedgerConfig lc; lc.p = p; lc.islands = std::max(1, o.r); lc.leaders = false; lc.fresh_counters = false;
  o.led.init(lc);
  auto v = rd.vec<double>("top_v"); auto h = rd.vec<uint64_t>("top_hash"); auto off = rd.vec<uint64_t>("top_off");
  auto len = rd.vec<uint16_t>("top_len"); auto pool = rd.vec<int32_t>("top_pool");
  if (h.size() != v.size() || off.size() != v.size() || len.size() != v.size()) throw Error(Status::invalid_input, path + ": inconsistent top store sections");
  o.led.top.load_unique_sorted(v.size(), v.data(), h.data(), off.data(), len.data(), pool.data(), pool.size());   // verified bulk load
  auto hs = rd.vec<int32_t>("hpm_S"); auto hv = rd.vec<double>("hpm_val"); auto ev = rd.vec<int64_t>("hpm_ev");
  o.led.has_hpm = !v.empty() || !hs.empty(); o.led.hpmS = Model(hs.begin(), hs.end()); o.led.hpmF = hv[0]; o.led.hpm_logm = hv[1];
  EventKey& k = o.led.hpm_ev.key;
  k.seg = (uint8_t)ev[0]; k.tier = (uint8_t)ev[1]; k.iter = (int8_t)ev[2]; k.unit = (uint32_t)ev[3]; k.xph = (uint8_t)ev[4]; k.stage = (uint32_t)ev[5];
  k.round = (uint32_t)ev[6]; k.particle = (uint32_t)ev[7]; k.position = (uint32_t)ev[8]; k.sub = (uint8_t)ev[9];
  o.led.hpm_ev.phase = (int)ev[10]; o.led.hpm_ev.mech = (int)ev[11];
  auto ib = rd.vec<double>("island_best");
  for (size_t i = 0; i < ib.size() && i < o.led.island_best.size(); ++i) o.led.island_best[i] = ib[i];
  auto lg = rd.vec<uint64_t>("logical"); std::memcpy(o.led.logical, lg.data(), std::min(lg.size() * 8, sizeof(o.led.logical)));
  if (o.status == Status::completed) {
    o.logZ = rd.vec<double>("logZ").at(0);
    o.rb_acc = rd.vec<double>("rb_acc"); o.pip = rd.vec<double>("pip_r");
    auto rbr = rd.vec<double>("rb_round");
    for (size_t hh = 0; p > 0 && (hh + 1) * (size_t)p <= rbr.size(); ++hh) o.rb_round.emplace_back(rbr.begin() + hh * p, rbr.begin() + (hh + 1) * p);
    auto tp = rd.vec<int64_t>("terminal_S_ptr"); auto ts = rd.vec<int32_t>("terminal_S");
    for (size_t i = 0; i + 1 < tp.size(); ++i) f.terminal.emplace_back(ts.begin() + tp[i], ts.begin() + tp[i + 1]);
  }
  return f;
}

}  // namespace v4::island
