// setup_run.cpp -- the `setup` command body: stages, timings, statuses, and setup.bin (INTERFACES v0.1 §5.1, kind 3).
#include <chrono>
#include <cstdio>
#include <sstream>
#include "v4/setup.h"
#include "wp1_format_shim.h"

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

SetupResult run(const Data& D, const SetupOptions& o) {
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
  W.vec("tstore_" + nm + "_v", fmt::F64, s.v);
  W.vec("tstore_" + nm + "_off", fmt::U64, s.off);
  W.vec("tstore_" + nm + "_len", fmt::U16, s.len);
  W.vec("tstore_" + nm + "_hash", fmt::U64, s.hash);
  W.vec("tstore_" + nm + "_pool", fmt::I32, s.pool);
}
void get_store(const fmt::Reader& Rd, const std::string& nm, Store& s, uint64_t cap, Order ord) {
  s.init(cap, ord);
  s.v = Rd.vec<double>("tstore_" + nm + "_v"); s.off = Rd.vec<uint64_t>("tstore_" + nm + "_off");
  s.len = Rd.vec<uint16_t>("tstore_" + nm + "_len"); s.hash = Rd.vec<uint64_t>("tstore_" + nm + "_hash");
  s.pool = Rd.vec<int32_t>("tstore_" + nm + "_pool"); s.nsorted = s.v.size();
}
const char* modename(PartMode m) { return m == PartMode::Exact ? "exact" : "truncated"; }
}  // namespace

std::string write_setup_bin(const std::string& path, const Data& D, const SetupResult& r, const SetupOptions& o, const std::string& data_hash) {
  if (r.status != Status::completed) throw Error(Status::internal_error, "write_setup_bin: setup did not complete (GUARD-W)");
  fmt::Writer W(3, o.file_mode);
  W.vec("nb_ptr", fmt::I64, r.corr.nb.ptr); W.vec("nb_idx", fmt::I32, r.corr.nb.idx);
  W.vec("dup_ptr", fmt::I64, r.corr.dup.ptr); W.vec("dup_idx", fmt::I32, r.corr.dup.idx);
  W.vec("cut_ptr", fmt::I64, r.cut.ptr); W.vec("cut_idx", fmt::I32, r.cut.idx);
  W.vec("blk_ptr", fmt::I64, r.part.bptr); W.vec("blk_members", fmt::I32, r.part.members);
  W.vec("blk", fmt::I32, r.part.blk); W.vec("pos", fmt::I32, r.part.pos);
  const Tables& T = r.tab;
  W.vec("code_ptr", fmt::I64, T.code_ptr); W.vec("logr", fmt::F64, T.logr);
  W.vec("logprof_ptr", fmt::I64, T.logprof_ptr); W.vec("logprof", fmt::F64, T.logprof);
  W.add("logF", fmt::F64, T.logF.data(), T.logF.size() * 8, (uint64_t)T.J + 1, (uint64_t)T.K + 1);
  W.vec("size_logmass", fmt::F64, T.size_logmass); W.vec("size_cum", fmt::F64, T.size_cum);
  W.vec("cond_ptr", fmt::I64, T.cond_ptr); W.vec("cond_cum", fmt::F64, T.cond_cum);
  W.vec("cbs_ptr", fmt::I64, T.cbs_ptr); W.vec("codes_by_size", fmt::U32, T.codes_by_size);
  W.vec("sub_ptr", fmt::I64, T.sub_ptr); W.vec("sub_cum", fmt::F64, T.sub_cum);
  W.vec("mode_S", fmt::I32, r.mode.S);
  put_store(W, "top", r.stores.top); put_store(W, "lead0", r.stores.lead0); put_store(W, "lead1", r.stores.lead1);
  // WP2-added sections (INTERFACES §5.1 allows additions): binary scalars, so readers need no JSON parser
  std::vector<double> sc = {T.logZbar0, r.mode.lg0, r.corr.rn, r.corr.tau, r.stores.hpmF};
  std::vector<int64_t> isc = {D.n, D.p, D.K, r.B, T.J, r.mode.ties, r.mode.truncated, r.mode.tie_dp_used,
                              r.stores.hpm_block, (int64_t)r.stores.hpm_code, (int64_t)o.part.mode, (int64_t)o.part.pack, o.part.strict};
  W.vec("scalars_f64", fmt::F64, sc); W.vec("scalars_i64", fmt::I64, isc);
  std::ostringstream m; m.precision(17);
  m << "{\"kind\":\"setup\",\"index_base\":\"internal0\",\"n\":" << D.n << ",\"p\":" << D.p << ",\"K\":" << D.K << ",\"B\":" << r.B
    << ",\"J\":" << T.J << ",\"partition\":\"" << modename(o.part.mode) << "\",\"pack\":\"" << (o.part.pack == PackOrder::MinIndex ? "min_index" : "leaf_order")
    << "\",\"strict\":" << (o.part.strict ? "true" : "false") << ",\"r_n\":" << r.corr.rn << ",\"tau\":" << r.corr.tau
    << ",\"logZbar0\":" << T.logZbar0 << ",\"mode\":{\"lg0\":" << r.mode.lg0 << ",\"ties\":" << r.mode.ties << ",\"truncated\":"
    << (r.mode.truncated ? "true" : "false") << ",\"tie_dp_used\":" << (r.mode.tie_dp_used ? "true" : "false") << "}"
    << ",\"cut_group\":" << (r.cut.rows() > 0 ? "true" : "false") << ",\"cut_group_count\":" << r.cut.rows()
    << ",\"dup_components\":" << r.corr.dup.rows() << ",\"table_codes\":" << T.code_ptr.back()
    << ",\"table_stats\":{\"scored\":" << r.tstats.scored << ",\"prefix\":" << r.tstats.prefix_scored << ",\"fallback\":" << r.tstats.fallback_scored
    << ",\"routes\":[" << r.tstats.routes[0] << "," << r.tstats.routes[1] << "," << r.tstats.routes[2] << "]}"
    << ",\"inputs\":{\"data.bin\":\"" << data_hash << "\"},\"timings\":[";
  for (size_t i = 0; i < r.timings.size(); ++i)
    m << (i ? "," : "") << "{\"stage\":\"" << r.timings[i].name << "\",\"seconds\":" << r.timings[i].seconds << ",\"peak_rss_mb\":" << r.timings[i].peak_rss_mb << "}";
  m << "]}";
  W.json("meta", m.str());
  return W.write(path);
}

SetupResult read_setup_bin(const std::string& path, std::string* content_hash) {
  fmt::Reader Rd(path, 3);
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
  if (r.stores.top.size()) r.stores.hpmS.assign(r.stores.top.pool.begin() + r.stores.top.off[0], r.stores.top.pool.begin() + r.stores.top.off[0] + r.stores.top.len[0]);
  if (content_hash) *content_hash = Rd.content_hash();
  return r;
}

}  // namespace v4::setup
