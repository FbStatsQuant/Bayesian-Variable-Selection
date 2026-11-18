// listpip.cpp -- `smcbvs4 listpip FIT.bin [--data data.bin] [--full 1] [--record out.json]`: the list-renormalised PIP fields of an existing
// fit.bin (SPEC_LIST_PIP.md; include/v4/list_pip.h). It calls the SAME function the merge calls, on the fit's stored `top` store (the
// merged top store, written by every completed merge since WP4), so for a fit.bin that carries the fields the result equals the stored
// values bit for bit (`matches_stored`). p = the length of the fit's `pip_eq` section (a completed fit's); a fit that is not completed has
// no estimate sections: the fields are absent (GUARD-W).
// INDEX SPACE (review PR68 MAJOR-1): the spec's mpm_list holds ORIGINAL column indices (1-based, v3's and `mpm`'s space). The kept -> original
// map is the fit.bin section `orig` (written by every merge since this change) or, for an older fit.bin (the pilot's, T5's), the `orig` of the
// data.bin given with --data (the fit's own input; its hash is in the fit's meta.inputs and is checked). Without either, the record says
// `index_space` = "internal_0based" and carries no original index. pip_list is dense by KEPT column j; `columns_orig` (with --full 1) labels it,
// and the default sparse form lists the nonzero entries by ORIGINAL index (`index`) and kept index (`kept`).
// A flagged result (empty_list / nonfinite_score) carries the flag and the scalars only: no pip_list, mpm_list or log_Z_list.
#include <cstring>
#include <limits>
#include "../eval/io.h"
#include "v4/list_pip.h"
#include "v4/prep.h"
#include "v4/provenance.h"

namespace v4::listpip {

namespace {
bool same_bits(double a, double b) { return std::memcmp(&a, &b, sizeof(double)) == 0; }
}  // namespace

Json run(const Json& args) {
  Json rec = Json::object();
  rec["schema"] = "smcbvs4.listpip/2";
  std::string path = eval::io::arg_str(args, "in", "");
  if (path.empty()) path = eval::io::arg_str(args, "fit", "");
  if (path.empty()) throw Error(Status::invalid_input, "listpip: the fit.bin is required (listpip FIT.bin, or --fit FIT.bin)");
  const std::string datap = eval::io::arg_str(args, "data", "");
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
  // the kept -> original map
  std::vector<int32_t> orig; std::string space = "internal_0based", orig_from = "none";
  if (B.has("orig")) {
    uint64_t c = 0; const int32_t* o = B.get<int32_t>("orig", &c);
    if (c != p) throw Error(Status::invalid_input, "fit.bin: the orig section has " + std::to_string(c) + " entries, expected p = " + std::to_string(p));
    orig.assign(o, o + c); orig_from = "fit.bin";
  } else if (!datap.empty()) {
    std::string dh; const Data D = prep::load_data(datap, &dh);
    if ((uint64_t)D.p != p) throw Error(Status::invalid_input, "listpip: data.bin has p = " + std::to_string(D.p) + " retained columns, the fit has " + std::to_string(p));
    if (ff.meta.contains("inputs") && ff.meta.at("inputs").contains("data.bin") && ff.meta.at("inputs").at("data.bin").type() == Json::STR &&
        ff.meta.at("inputs").at("data.bin").str() != dh)
      throw Error(Status::invalid_input, "listpip: data.bin is not the fit's input (content hash differs from the fit's meta.inputs)");
    orig.assign(D.orig, D.orig + D.p); orig_from = "data.bin";
  }
  if (!orig.empty()) {
    for (size_t j = 1; j < orig.size(); ++j) if (!(orig[j] > orig[j - 1])) throw Error(Status::invalid_input, "listpip: the kept -> original map is not strictly increasing");
    space = "original_1based";
  }
  rec["index_space"] = space; rec["orig_from"] = orig_from;
  ListPipSrc src; src.n = ff.top.size; src.v = ff.top.v; src.off = ff.top.off; src.len = ff.top.len; src.hash = ff.top.hash; src.pool = ff.top.pool;
  const ListPip L = compute_list_pip(src, (int32_t)p, cap);
  rec["p"] = (int64_t)p;
  rec["list_size"] = (int64_t)L.list_size; rec["list_full"] = L.list_full; rec["pip_list_source"] = L.source; rec["store_capacity"] = (int64_t)cap;
  rec["pip_list_flag"] = L.flag.empty() ? Json() : Json(L.flag);
  if (L.flag.empty()) {
    rec["log_Z_list"] = L.log_Z_list;
    Json mpm = Json::array(); for (int32_t j : L.mpm_list) mpm.push(Json((int)(orig.empty() ? j : orig[(size_t)j]))); rec["mpm_list"] = mpm;
    if (full) {
      rec["pip_list"] = Json::array_of(L.pip_list);   // dense, by kept column j = 0 .. p-1
      if (!orig.empty()) rec["columns_orig"] = Json::array_of(orig);   // the label of entry j
    } else {
      Json idx = Json::array(), kept = Json::array(), val = Json::array(); size_t nz = 0;
      for (size_t j = 0; j < L.pip_list.size(); ++j) if (!(L.pip_list[j] == 0.0)) {
        if (!orig.empty()) idx.push(Json((int64_t)orig[j]));
        kept.push(Json((int64_t)j)); val.push(Json(L.pip_list[j])); ++nz;
      }
      Json nzj = Json::object(); if (!orig.empty()) nzj["index"] = idx; nzj["kept"] = kept; nzj["value"] = val;
      rec["pip_list_nonzero"] = nzj; rec["n_nonzero"] = (int64_t)nz;
    }
  }
  // a fit.bin written with the fields: the stored values must equal the recomputation bit for bit (flagged: neither list section is stored)
  const bool stored = L.flag.empty() ? (B.has("pip_list") && B.has("mpm_list")) : (ff.meta.contains("pip_list_flag"));
  if (stored) {
    bool ok = true;
    if (L.flag.empty()) {
      uint64_t c = 0, cm = 0; const double* sp = B.get<double>("pip_list", &c); const int32_t* sm = B.get<int32_t>("mpm_list", &cm);
      ok = c == L.pip_list.size() && cm == L.mpm_list.size();
      for (uint64_t j = 0; ok && j < c; ++j) ok = same_bits(sp[j], L.pip_list[j]);
      const bool stored_orig = ff.meta.contains("mpm_list_index_space") && ff.meta.at("mpm_list_index_space").type() == Json::STR && ff.meta.at("mpm_list_index_space").str() == "original_1based";
      for (uint64_t j = 0; ok && j < cm; ++j) ok = sm[j] == (stored_orig && !orig.empty() ? orig[(size_t)L.mpm_list[j]] : L.mpm_list[j]);
      if (ok && ff.meta.contains("log_Z_list")) { const Json& z = ff.meta.at("log_Z_list"); ok = z.type() == Json::NUM && same_bits(z.num(), L.log_Z_list); }
    } else ok = ff.meta.at("pip_list_flag").type() == Json::STR && ff.meta.at("pip_list_flag").str() == L.flag;
    rec["stored_in_fit"] = true; rec["matches_stored"] = ok;
  } else rec["stored_in_fit"] = false;
  rec["status"] = "completed";
  return rec;
}

}  // namespace v4::listpip
