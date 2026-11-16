// setup_run.cpp -- the `setup` command body: stages, timings, statuses, and setup.bin (INTERFACES v0.1 §5.1, kind 3).
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include "v4/setup.h"
#include "v4/format.h"
#include "v4/prep.h"
#include "v4/threads.h"

namespace v4::setup {

double peak_rss_mb() {
  FILE* f = std::fopen("/proc/self/status", "r");
  if (!f) return -1;
  char line[256]; double kb = -1;
  while (std::fgets(line, sizeof line, f)) if (std::strncmp(line, "VmHWM:", 6) == 0) { kb = std::atof(line + 6); break; }
  std::fclose(f);
  return kb / 1024.0;
}

// core/v3_preprocess.R:22: B = min(isqrt(n), isqrt(p), 16)
int default_B(int n, int p) {
  auto isqrt = [](long x) { long r = (long)std::floor(std::sqrt((double)x)); while ((r + 1) * (r + 1) <= x) ++r; while (r * r > x) --r; return r; };
  return (int)std::min<long>(std::min(isqrt(n), isqrt(p)), 16);
}

SetupResult run_setup(const Data& D, const SetupOptions& o) {
  SetupResult R;
  auto t0 = std::chrono::steady_clock::now();
  auto lap = [&](const char* name) {
    auto t1 = std::chrono::steady_clock::now();
    R.timings.push_back({name, std::chrono::duration<double>(t1 - t0).count(), peak_rss_mb()});
    t0 = t1;
  };
  try {
    R.B = o.B > 0 ? o.B : default_B(D.n, D.p);
    CorrOptions co; co.B = R.B; co.threads = o.threads; co.tau = o.part.tau; co.keep_edges = true;
    R.corr = correlation_pass(D, co);
    lap("correlation");
    PartitionOptions po = o.part; po.B = R.B; po.threads = o.threads;
    R.part = make_partition(D, R.corr, po);
    lap(po.mode == PartMode::Exact ? "partition_exact" : "partition_truncated");
    R.cut = cut_groups(D.p, R.corr.edges, R.corr.rn, R.part);
    std::vector<Edge>().swap(R.corr.edges);  // edges are not needed after the partition and the cut-group record
    lap("cut_groups");
    R.tab = build_tables(D, R.part, o.threads, o.table_stores ? &R.stores : nullptr, &R.tstats);
    lap("tables");
    build_start(D, R.part, R.tab);
    lap("start_law");
    R.mode = start_mode(D, R.part, R.tab, o.mode_cap, o.tie_dp);
    lap("start_mode");
  } catch (const Error& e) {
    R.status = e.st; R.reason = e.what();
  } catch (const std::bad_alloc&) {
    R.status = Status::resource_limit; R.reason = "out of memory";
  } catch (const std::exception& e) {
    R.status = Status::internal_error; R.reason = e.what();
  }
  return R;
}

namespace {
void put_store(fmt::Writer& W, const std::string& nm, const Store& s) {
  W.add("tstore_" + nm + "_v", s.v); W.add("tstore_" + nm + "_off", s.off); W.add("tstore_" + nm + "_len", s.len);
  W.add("tstore_" + nm + "_hash", s.hash); W.add("tstore_" + nm + "_pool", s.pool);
}
// Reads a stored table top store back through the public Store API (offer + compact: the stored content is already
// the sorted top-c, so it is reproduced exactly).
void get_store(const fmt::Reader& Rd, const std::string& nm, Store& s, uint64_t cap, Order ord) {
  s.init(cap, ord);
  auto v = Rd.vec<double>("tstore_" + nm + "_v"); auto off = Rd.vec<uint64_t>("tstore_" + nm + "_off");
  auto len = Rd.vec<uint16_t>("tstore_" + nm + "_len"); auto h = Rd.vec<uint64_t>("tstore_" + nm + "_hash");
  auto pool = Rd.vec<int32_t>("tstore_" + nm + "_pool");
  for (size_t i = 0; i < v.size(); ++i) s.offer(v[i], ModelView(pool.data() + off[i], len[i]), h[i]);
  s.compact();
}
const char* modename(PartMode m) { return m == PartMode::Exact ? "exact" : "truncated"; }
}  // namespace

std::string write_setup_bin(const std::string& path, const Data& D, const SetupResult& r, const SetupOptions& o, const std::string& data_hash) {
  if (r.status != Status::completed) throw Error(Status::internal_error, "write_setup_bin: setup did not complete (GUARD-W)");
  fmt::Writer W(fmt::K_SETUP, o.file_mode);
  W.add("nb_ptr", r.corr.nb.ptr); W.add("nb_idx", r.corr.nb.idx);
  W.add("dup_ptr", r.corr.dup.ptr); W.add("dup_idx", r.corr.dup.idx);
  W.add("cut_ptr", r.cut.ptr); W.add("cut_idx", r.cut.idx);
  W.add("blk_ptr", r.part.bptr); W.add("blk_members", r.part.members);
  W.add("blk", r.part.blk); W.add("pos", r.part.pos);
  const Tables& T = r.tab;
  W.add("code_ptr", T.code_ptr); W.add("logr", T.logr);
  W.add("logprof_ptr", T.logprof_ptr); W.add("logprof", T.logprof);
  W.add("logF", T.logF, (uint64_t)T.J + 1, (uint64_t)T.K + 1);
  W.add("size_logmass", T.size_logmass); W.add("size_cum", T.size_cum);
  W.add("cond_ptr", T.cond_ptr); W.add("cond_cum", T.cond_cum);
  W.add("cbs_ptr", T.cbs_ptr); W.add("codes_by_size", T.codes_by_size);
  W.add("sub_ptr", T.sub_ptr); W.add("sub_cum", T.sub_cum);
  W.add("mode_S", r.mode.S);
  put_store(W, "top", r.stores.top); put_store(W, "lead0", r.stores.lead0); put_store(W, "lead1", r.stores.lead1);
  // WP2-added sections (INTERFACES §5.1 allows additions): binary scalars, so the exact bits survive without JSON
  std::vector<double> sc = {T.logZbar0, r.mode.lg0, r.corr.rn, r.corr.tau, r.stores.hpmF};
  std::vector<int64_t> isc = {D.n, D.p, D.K, r.B, T.J, r.mode.ties, r.mode.truncated, r.mode.tie_dp_used,
                              r.stores.hpm_block, (int64_t)r.stores.hpm_code, (int64_t)o.part.mode, (int64_t)o.part.pack, o.part.strict};
  W.add("scalars_f64", sc); W.add("scalars_i64", isc);
  Json m = Json::object();
  m["kind"] = "setup"; m["index_base"] = "internal0"; m["mode"] = fmt::mode_name(o.file_mode);
  m["n"] = D.n; m["p"] = D.p; m["K"] = D.K; m["B"] = r.B; m["J"] = T.J;
  m["partition"] = modename(o.part.mode); m["pack"] = o.part.pack == PackOrder::MinIndex ? "min_index" : "leaf_order";
  m["strict"] = o.part.strict; m["r_n"] = r.corr.rn; m["tau"] = r.corr.tau; m["logZbar0"] = T.logZbar0;
  Json mo = Json::object(); mo["lg0"] = r.mode.lg0; mo["ties"] = (int64_t)r.mode.ties; mo["truncated"] = r.mode.truncated;
  mo["tie_dp_used"] = r.mode.tie_dp_used; mo["size"] = (int64_t)r.mode.S.size(); m["start_mode"] = mo;
  m["cut_group"] = r.cut.rows() > 0; m["cut_group_count"] = r.cut.rows(); m["dup_components"] = r.corr.dup.rows();
  m["table_codes"] = T.code_ptr.back();
  auto hx = [](uint64_t x) { char b[24]; std::snprintf(b, sizeof b, "0x%llx", (unsigned long long)x); return std::string(b); };  // u64 -> hex (§5.1)
  Json ts = Json::object(); ts["scored"] = hx(r.tstats.scored); ts["prefix"] = hx(r.tstats.prefix_scored); ts["fallback"] = hx(r.tstats.fallback_scored);
  Json rt = Json::array(); for (int q = 0; q < 3; ++q) rt.push(Json(hx(r.tstats.routes[q])));
  ts["routes"] = rt; m["table_stats"] = ts;
  Json in = Json::object(); in["data.bin"] = data_hash; m["inputs"] = in;
  Json tm = Json::array();
  for (auto& t : r.timings) { Json e = Json::object(); e["stage"] = t.name; e["seconds"] = t.seconds; e["peak_rss_mb"] = t.peak_rss_mb; tm.push(e); }
  m["timings"] = tm;
  W.add_json("meta", m);
  return W.write(path);
}

SetupResult read_setup_bin(const std::string& path, std::string* content_hash) {
  fmt::Reader Rd(path);
  if (Rd.kind() != fmt::K_SETUP) throw Error(Status::invalid_input, path + " is not a setup file");
  SetupResult r;
  r.corr.nb.ptr = Rd.vec<int64_t>("nb_ptr"); r.corr.nb.idx = Rd.vec<int32_t>("nb_idx");
  r.corr.dup.ptr = Rd.vec<int64_t>("dup_ptr"); r.corr.dup.idx = Rd.vec<int32_t>("dup_idx");
  r.cut.ptr = Rd.vec<int64_t>("cut_ptr"); r.cut.idx = Rd.vec<int32_t>("cut_idx");
  r.part.bptr = Rd.vec<int64_t>("blk_ptr"); r.part.members = Rd.vec<int32_t>("blk_members");
  r.part.blk = Rd.vec<int32_t>("blk"); r.part.pos = Rd.vec<int32_t>("pos");
  auto sc = Rd.vec<double>("scalars_f64"); auto isc = Rd.vec<int64_t>("scalars_i64");
  if (sc.size() < 5 || isc.size() < 13) throw Error(Status::invalid_input, "setup.bin: scalars missing");
  Tables& T = r.tab;
  T.J = (int32_t)isc[4]; T.K = (int32_t)isc[2]; r.B = (int)isc[3];
  r.part.J = T.J; r.part.B = r.B;
  T.code_ptr = Rd.vec<int64_t>("code_ptr"); T.logr = Rd.vec<double>("logr");
  T.logprof_ptr = Rd.vec<int64_t>("logprof_ptr"); T.logprof = Rd.vec<double>("logprof");
  T.logF = Rd.vec<double>("logF"); T.size_logmass = Rd.vec<double>("size_logmass"); T.size_cum = Rd.vec<double>("size_cum");
  T.cond_ptr = Rd.vec<int64_t>("cond_ptr"); T.cond_cum = Rd.vec<double>("cond_cum");
  T.cbs_ptr = Rd.vec<int64_t>("cbs_ptr"); T.codes_by_size = Rd.vec<uint32_t>("codes_by_size");
  T.sub_ptr = Rd.vec<int64_t>("sub_ptr"); T.sub_cum = Rd.vec<double>("sub_cum");
  T.logZbar0 = sc[0];
  r.mode.S = Rd.vec<int32_t>("mode_S"); r.mode.lg0 = sc[1]; r.mode.ties = (long)isc[5]; r.mode.truncated = isc[6]; r.mode.tie_dp_used = isc[7];
  r.corr.rn = sc[2]; r.corr.tau = sc[3];
  const uint64_t p = (uint64_t)isc[1];
  get_store(Rd, "top", r.stores.top, 40 * p + 1, Order::HPM);
  get_store(Rd, "lead0", r.stores.lead0, 20 * p, Order::LEX);
  get_store(Rd, "lead1", r.stores.lead1, 20 * p, Order::LEX);
  r.stores.hpmF = sc[4]; r.stores.hpm_block = (int32_t)isc[8]; r.stores.hpm_code = (uint32_t)isc[9];
  if (r.stores.top.size()) { ModelView h = r.stores.top.model(0); r.stores.hpmS.assign(h.begin(), h.end()); }
  if (content_hash) *content_hash = Rd.content_hash();
  return r;
}

// The `setup` command (include/v4/stubs.h): data.bin -> setup.bin + record.
Json run(const Json& args) {
  // tables are bit-form: refuse where glibc would not select the FMA variants the v3 records assume (WP1 guard)
  if (!pm::fma_variant_expected() && !(args.contains("allow_non_fma_libm") && args.at("allow_non_fma_libm").i64() != 0))
    throw Error(Status::invalid_input, "setup: libm FMA variant not expected on this CPU (bit form; see tests/PMATH_REPORT.md)");
  std::string data_hash;
  Data D = prep::load_data(args.at("data").str(), &data_hash);
  SetupOptions o;
  o.threads = args.contains("threads") ? (int)args.at("threads").i64() : threads_available();
  if (args.contains("B")) o.B = (int)args.at("B").i64();
  if (args.contains("partition")) {
    const std::string& m = args.at("partition").str();
    if (m == "exact") { o.part.mode = PartMode::Exact; o.part.pack = PackOrder::LeafOrder; }
    else if (m != "truncated") throw Error(Status::invalid_input, "setup: partition must be truncated or exact");
  }
  if (args.contains("tau")) o.part.tau = args.at("tau").num();
  if (args.contains("strict")) o.part.strict = args.at("strict").i64() != 0;
  if (args.contains("mode_cap")) o.mode_cap = (long)args.at("mode_cap").i64();
  if (args.contains("tie_dp")) o.tie_dp = args.at("tie_dp").i64() != 0;
  o.file_mode = args.contains("file_mode") ? fmt::mode_from_name(args.at("file_mode").str()) : (uint32_t)fmt::M_LAW;
  if (o.part.mode == PartMode::Truncated && o.file_mode == fmt::M_COMPAT)
    throw Error(Status::invalid_input, "setup: compat mode uses the exact partition (v3 rule)");
  SetupResult r = run_setup(D, o);
  Json rec = Json::object();
  rec["status"] = status_name(r.status);
  if (r.status != Status::completed) { rec["reason"] = r.reason; return rec; }   // GUARD-W: no setup.bin
  std::string out = args.at("out").str();
  std::string h = write_setup_bin(out, D, r, o, data_hash);
  Json outs = Json::object(); outs[out] = h; rec["outputs"] = outs;
  Json in = Json::object(); in["data.bin"] = data_hash; rec["inputs"] = in;
  rec["p"] = D.p; rec["n"] = D.n; rec["B"] = r.B; rec["J"] = r.part.J; rec["mode_size"] = (int64_t)r.mode.S.size();
  Json tm = Json::object(); for (auto& t : r.timings) tm[t.name] = t.seconds;
  rec["seconds"] = tm; rec["peak_rss_mb"] = peak_rss_mb();
  return rec;
}

}  // namespace v4::setup
