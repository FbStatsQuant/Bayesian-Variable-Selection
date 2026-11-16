// io.h -- WP5-internal readers for data.bin / fit.bin (INTERFACES §5.1 section names) and the command-line helper.
#pragma once
#include <map>
#include <memory>
#include <string>

#include "v4/eval.h"

namespace v4::eval::io {

struct DataFile {
  std::unique_ptr<wp5prov::BinReader> bin;
  EvalData D;
  std::vector<int32_t> orig_owned;   // copy of `kept`
  Json meta;
};
// data.bin: Xs_cm, ys, z, col_max, col_mean, col_sd, kept (i32 1-based), meta{n, p_raw, p, K, yty, y_max, y_mean,
// y_sd_scaled, ...}, logprior. Constants are recomputed (data_constants) and compared with meta/logprior when present.
void load_data(const std::string& path, DataFile& out, bool verify = true);

struct FitFile {
  std::unique_ptr<wp5prov::BinReader> bin;
  Json meta;          // the `meta` section (scalars) merged with fit.json if given
  StoreView top;
};
// fit.bin: top_v f64, top_off u64, top_len u16, top_hash u64, top_pool i32 (internal), meta, and the optional sections
// read by eval (hpm_S, logZ_r, pip_eq, pip_Z, pip_T, pip_r, occ_top, occ_top_r).
void load_fit(const std::string& path, FitFile& out, bool verify = true);

// --key value parser; flags without a value get "1".
std::map<std::string, std::string> parse_args(int argc, char** argv, int first);
std::string arg_or(const std::map<std::string, std::string>& a, const std::string& k, const std::string& dflt);
std::string file_sha256(const std::string& path);   // SHA-256 of a whole file (truth.json, cost.json)

// Writes <out>.json with {schema, command, status, reason, ...record} and returns the exit code (0 or 10 + status).
int finish(const std::string& out_json, Json record, Status st, const std::string& reason);

}  // namespace v4::eval::io
