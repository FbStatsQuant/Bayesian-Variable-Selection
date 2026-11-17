// setup_load.h -- the island's start law and neighbour lists from setup.bin (INTERFACES §5.1: WP2's sections).
//
// Start: the partition (blk_ptr / blk_members) and the block tables (code_ptr / logr) are read; the sampler tables
// (profiles, logF, size and conditional cumulative masses, codes by size, sub-model masses) are rebuilt by the island's
// copy of core's arithmetic (dep.h build_sampler, core/cpp/v3_start.h:101-176). When setup.bin carries WP2's own
// size_cum, it must equal the rebuild bit for bit (else invalid_input): one law, two writers.
// Neighbours: nb_ptr (i64, p + 1) / nb_idx (i32), N(j) = idx[ptr[j] .. ptr[j+1]).
#pragma once
#include <string>
#include "v4/format.h"
#include "v4/island/dep.h"

namespace v4::island {

inline Start load_start(const std::string& path, const Data& D) {
  fmt::Reader R(path);
  auto blk_ptr = R.vec<int64_t>("blk_ptr"); auto members = R.vec<int32_t>("blk_members");
  auto code_ptr = R.vec<int64_t>("code_ptr"); auto logr = R.vec<double>("logr");
  const std::string w = path + ": ";
  const size_t J = code_ptr.size();
  if (blk_ptr.size() != J + 1 || members.size() != (size_t)D.p || blk_ptr[0] != 0 || blk_ptr[J] != D.p) throw Error(Status::invalid_input, w + "partition shape");   // review PR39 m2: blk_ptr[0] = 0
  Start st; st.D = &D; st.J = (int)J; st.blocks.assign(J, {}); st.logr.assign(J, {});
  st.blk.assign(D.p, -1); st.pos.assign(D.p, -1);
  for (size_t b = 0; b < J; ++b) {
    const int64_t m = blk_ptr[b + 1] - blk_ptr[b];
    if (m < 1 || m > 20 || code_ptr[b] < 0 || (uint64_t)code_ptr[b] + (1ull << m) > logr.size()) throw Error(Status::invalid_input, w + "block tables shape");
    for (int64_t i = 0; i < m; ++i) {
      const int32_t j = members[(size_t)(blk_ptr[b] + i)];
      if (j < 0 || j >= D.p || st.blk[j] >= 0) throw Error(Status::invalid_input, w + "blk_members is not a partition of 0..p-1");
      st.blocks[b].push_back(j); st.blk[j] = (int)b; st.pos[j] = (int)i;
    }
    st.logr[b].assign(logr.begin() + code_ptr[b], logr.begin() + code_ptr[b] + (1ll << m));
  }
  for (int j = 0; j < D.p; ++j) if (st.blk[j] < 0) throw Error(Status::invalid_input, w + "blk_members is not a partition of 0..p-1 (variable " + std::to_string(j) + " in no block)");
  build_sampler(st, D);
  auto same = [](const std::vector<double>& a, const std::vector<double>& b) {
    if (a.size() != b.size()) return false;
    for (size_t i = 0; i < a.size(); ++i) { uint64_t x, y; std::memcpy(&x, &a[i], 8); std::memcpy(&y, &b[i], 8); if (x != y) return false; }
    return true;
  };
  if (R.has("size_cum") && !same(R.vec<double>("size_cum"), st.size_cum))
    throw Error(Status::invalid_input, w + "size_cum differs from the island's rebuild of the start law (core/cpp/v3_start.h)");
  return st;
}

// Resident bytes of a dep::Start and its neighbour lists: payloads + 24 B per std::vector + 16 B malloc header per
// allocation (the plan's caller-supplied inputs term until the island reads WP2's flat arrays as a view; manager 11-16).
inline double start_bytes(const Start& st, const Neighbours& nb) {
  double b = 0;
  auto v = [&](const auto& x) { b += 24.0 + 16.0 + (double)x.capacity() * sizeof(x[0]); };
  for (const auto& x : st.blocks) v(x);
  v(st.blk); v(st.pos); v(st.size_logmass); v(st.size_cum); v(st.code_ptr); v(st.logr_flat); v(st.c0r);
  for (const auto& x : st.logr) v(x);
  for (const auto& x : st.logprof) v(x);
  for (const auto& x : st.logF) v(x);
  for (const auto& b1 : st.cond_cum) { b += 40; for (const auto& x : b1) v(x); }
  for (const auto& b1 : st.sub_cum) { b += 40; for (const auto& x : b1) v(x); }
  for (const auto& b1 : st.codes_by_size) { b += 40; for (const auto& x : b1) v(x); }
  v(nb.ptr); v(nb.idx);
  return b;
}

inline Neighbours load_neighbours(const std::string& path, int p) {
  fmt::Reader R(path);
  if (!R.has("nb_ptr") || !R.has("nb_idx")) throw Error(Status::invalid_input, path + ": no neighbour lists (nb_ptr / nb_idx)");
  Neighbours nb; nb.ptr = R.vec<int64_t>("nb_ptr"); nb.idx = R.vec<int32_t>("nb_idx");
  if (nb.ptr.size() != (size_t)p + 1 || nb.ptr[0] != 0 || nb.ptr[(size_t)p] != (int64_t)nb.idx.size()) throw Error(Status::invalid_input, path + ": nb_ptr shape");
  for (int j = 0; j < p; ++j) {
    if (nb.ptr[j + 1] < nb.ptr[j]) throw Error(Status::invalid_input, path + ": nb_ptr not increasing");
    for (int64_t e = nb.ptr[j]; e < nb.ptr[j + 1]; ++e) if (nb.idx[e] < 0 || nb.idx[e] >= p || nb.idx[e] == j) throw Error(Status::invalid_input, path + ": nb_idx out of range");
  }
  return nb;
}

}  // namespace v4::island
