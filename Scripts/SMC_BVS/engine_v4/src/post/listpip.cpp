// listpip.cpp -- `smcbvs4 listpip FIT.bin [--full 1] [--record out.json]`: the list-renormalised PIP fields of an existing fit.bin
// (SPEC_LIST_PIP.md; include/v4/list_pip.h). It calls the SAME function the merge calls, on the fit's stored `top` store (the
// merged top store, written by every completed merge since WP4), so for a fit.bin that carries the fields the result equals
// the stored values bit for bit (`matches_stored`). p = the length of the fit's `pip_eq` section (a completed fit's);
// a fit that is not completed has no estimate sections: the fields are absent (GUARD-W). Indices are internal, 0-based
// (as `mpm`). The record prints pip_list sparsely (`pip_list_nonzero`: index and value of every nonzero entry; every other
// column is exactly 0) unless --full 1 asks for the dense array.
#include <cstring>
#include <limits>
#include "../eval/io.h"
#include "v4/list_pip.h"
#include "v4/provenance.h"

namespace v4::listpip {

namespace {
bool same_bits(double a, double b) { return std::memcmp(&a, &b, sizeof(double)) == 0; }
}  // namespace

Json run(const Json& args) {
  Json rec = Json::object();
  rec["schema"] = "smcbvs4.listpip/1";
  std::string path = eval::io::arg_str(args, "in", "");
  if (path.empty()) path = eval::io::arg_str(args, "fit", "");
  if (path.empty()) throw Error(Status::invalid_input, "listpip: the fit.bin is required (listpip FIT.bin, or --fit FIT.bin)");
  const bool full = eval::io::arg_num(args, "full", 0) != 0;
  {  // GUARD-W first, from the header and the meta section only: a fit that is not completed has no store and no estimate sections
    fmt::Reader hd(path, false);
    if (hd.kind() != fmt::K_FIT) throw Error(Status::invalid_input, path + ": not a fit.bin (kind != 6)");
    const Json m = hd.has("meta") ? hd.json("meta") : Json::object();
    if (!eval::jfind(m, "status") || m.at("status").type() != Json::STR) throw Error(Status::invalid_input, "fit.bin: meta.status missing");
    rec["fit_status"] = m.at("status").str();
    if (m.at("status").str() != "completed" || !hd.has("pip_eq") || !hd.has("top_v")) {
      rec["reason"] = "fit not completed: the list fields are absent"; rec["status"] = "completed";
      return rec;
    }
  }
  eval::io::FitFile ff; eval::io::load_fit(path, ff);   // verifies every section hash, the store's order and one entry per model
  const fmt::Reader& B = *ff.bin;
  rec["inputs"] = Json::object(); rec["inputs"]["fit.bin"] = B.content_hash();
  uint64_t p = 0; B.get<double>("pip_eq", &p);
  uint64_t cap = 0;
  if (ff.meta.contains("stores") && ff.meta.at("stores").contains("top")) cap = (uint64_t)eval::jnum_or(ff.meta.at("stores").at("top"), "cap", 0);
  ListPipSrc src; src.n = ff.top.size; src.v = ff.top.v; src.off = ff.top.off; src.len = ff.top.len; src.hash = ff.top.hash; src.pool = ff.top.pool;
  const ListPip L = compute_list_pip(src, (int32_t)p, cap);
  rec["p"] = (int64_t)p;
  rec["log_Z_list"] = L.log_Z_list; rec["list_size"] = (int64_t)L.list_size; rec["list_full"] = L.list_full;
  rec["pip_list_source"] = L.source; rec["pip_list_flag"] = L.flag.empty() ? Json() : Json(L.flag);
  rec["store_capacity"] = (int64_t)cap;
  Json mpm = Json::array(); for (int32_t j : L.mpm_list) mpm.push(Json((int)j)); rec["mpm_list"] = mpm;
  if (full) rec["pip_list"] = Json::array_of(L.pip_list);
  else {
    Json idx = Json::array(), val = Json::array(); size_t nz = 0;
    for (size_t j = 0; j < L.pip_list.size(); ++j) if (!(L.pip_list[j] == 0.0)) { idx.push(Json((int64_t)j)); val.push(Json(L.pip_list[j])); ++nz; }
    Json nzj = Json::object(); nzj["index"] = idx; nzj["value"] = val; rec["pip_list_nonzero"] = nzj; rec["n_nonzero"] = (int64_t)nz;
  }
  // a fit.bin written with the fields: the stored values must equal the recomputation bit for bit
  if (B.has("pip_list") && B.has("mpm_list")) {
    uint64_t c = 0, cm = 0; const double* sp = B.get<double>("pip_list", &c); const int32_t* sm = B.get<int32_t>("mpm_list", &cm);
    bool ok = c == L.pip_list.size() && cm == L.mpm_list.size();
    for (uint64_t j = 0; ok && j < c; ++j) ok = same_bits(sp[j], L.pip_list[j]);
    for (uint64_t j = 0; ok && j < cm; ++j) ok = sm[j] == L.mpm_list[j];
    if (ok && ff.meta.contains("logZ_list")) { const Json& z = ff.meta.at("logZ_list"); ok = z.type() == Json::NUM ? same_bits(z.num(), L.log_Z_list) : std::isnan(L.log_Z_list); }
    rec["stored_in_fit"] = true; rec["matches_stored"] = ok;
  } else rec["stored_in_fit"] = false;
  rec["status"] = "completed";
  return rec;
}

}  // namespace v4::listpip
