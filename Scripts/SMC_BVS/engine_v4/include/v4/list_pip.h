// list_pip.h -- list-renormalised PIP fields (SPEC_LIST_PIP.md, HQ order 2026-11-17; owner-approved, additive output only).
// The MERGED top store T (compacted; models in internal 0-based column indices; scores F(S) = log varpi(S) + log m(S)) read as
// a list: pip_list[j] = sum_{S in T, j in S} u_S / sum_{S in T} u_S with u_S = exp(F(S) - max F); mpm_list = {j : pip_list[j]
// > 1/2} (strict, increasing index); log_Z_list = max F + log sum u_S. Computed LAST (merge assembly, or `smcbvs4 listpip`
// from a stored fit.bin: the same function), reads no random number, changes no state. pip_T / log_Z_T of the fit are a
// different computation (long double, forward order) and are NOT touched.
// Numerics (spec §3): subtract max F before exp (F itself is never exponentiated); both sums run from the LAST store entry to
// the first, in plain double with no compensation (a column's numerator adds a subsequence of the denominator's terms in the
// same order, so 0 <= pip_list <= 1 holds exactly in floating point; nothing is clamped); exp = pm::exp (bit form).
// Cases (spec §4): m = 0 -> NA fields, flag "empty_list"; a NaN or +Inf score (or a list whose scores are all -Inf) -> NA fields,
// flag "nonfinite_score"; -Inf scores get weight 0; duplicate models -> Error(internal_error) (a store is a set; never merged).
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "v4/json.h"
#include "v4/store.h"

namespace v4 {

struct ListPipSrc {   // a flat read-only store (Store / eval::StoreView layout), sorted in HPM order
  size_t n = 0;
  const double* v = nullptr; const uint64_t* off = nullptr; const uint16_t* len = nullptr; const uint64_t* hash = nullptr; const int32_t* pool = nullptr;
};
struct ListPip {
  std::vector<double> pip_list;      // p values (NaN when flagged)
  std::vector<int32_t> mpm_list;     // internal 0-based indices, increasing (empty when flagged)
  double log_Z_list = 0;             // NaN when flagged
  uint64_t list_size = 0;            // m = |T|
  bool list_full = false;            // |T| >= the store's capacity
  std::string source = "store";      // "store" (the merge); the exact branch of core v3 has "exact" (v4 has no exact branch)
  std::string flag;                  // "" when clean; "empty_list" | "nonfinite_score"
};

ListPip compute_list_pip(const ListPipSrc& s, int32_t p, uint64_t capacity);
ListPip compute_list_pip(const Store& top, int32_t p);   // top must be compacted; capacity = top.cap
ListPipSrc list_pip_src(const Store& top);

namespace listpip {
// `smcbvs4 listpip FIT.bin [--full 1] [--out file.json]`: the fields of an existing fit.bin, from its stored `top` store.
Json run(const Json& args);
}  // namespace listpip

}  // namespace v4
