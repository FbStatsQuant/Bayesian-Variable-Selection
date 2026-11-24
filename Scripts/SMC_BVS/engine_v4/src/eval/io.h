// io.h -- WP5-internal readers for fit.bin (INTERFACES §5.1 section names) and argument helpers.
#pragma once
#include <memory>
#include <string>

#include "v4/eval.h"
#include "v4/format.h"

namespace v4::eval::io {

struct FitFile {
  std::shared_ptr<fmt::Reader> bin;
  Json meta;          // the `meta` section
  StoreView top;
};
// fit.bin: top_v f64, top_off u64, top_len u16, top_hash u64, top_pool i32 (internal), meta, and the optional sections
// read by eval (hpm_S, logZ_r, pip_eq, pip_Z, pip_T, pip_r, occ_top, occ_top_r). Store sorted (I1) and in range.
void load_fit(const std::string& path, FitFile& out);

std::string arg_str(const Json& a, const std::string& k, const std::string& dflt);   // also accepts numbers
double arg_num(const Json& a, const std::string& k, double dflt);
// --out names the .bin output (WP1 convention: the record is <out>.json, written by main)
std::string out_bin(const Json& a, const std::string& dflt);

}  // namespace v4::eval::io
