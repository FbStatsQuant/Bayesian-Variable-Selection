// setup_load.h -- the island's start law and neighbour lists from setup.bin (INTERFACES §5.1: WP2's sections).
//
// Start: the partition (blk_ptr / blk_members) and the block tables (code_ptr / logr) are read; the sampler tables
// (profiles, logF, size and conditional cumulative masses, codes by size, sub-model masses) are rebuilt by the island's
// copy of core's arithmetic (dep.h build_sampler, core/cpp/v3_start.h:101-176). When setup.bin carries WP2's own
// size_cum, it must equal the rebuild bit for bit (else invalid_input): one law, two writers.
// Neighbours: nb_ptr (i64, p + 1) / nb_idx (i32), N(j) = idx[ptr[j] .. ptr[j+1]).
#pragma once
#include <sys/stat.h>
#include <cmath>
#include <string>
#include "v4/format.h"
#include "v4/island/dep.h"

namespace v4::island {

inline Start load_start(const std::string& path, const Data& D) {
  fmt::Reader R(path);
  auto blk_ptr = R.vec<int64_t>("blk_ptr"); auto members = R.vec<int32_t>("blk_members");
  auto code_ptr = R.vec<int64_t>("code_ptr"); auto logr = R.vec<double>("logr");
  const std::string w = path + ": ";
  // J blocks: blk_ptr has J + 1 entries; code_ptr has J (offsets) or J + 1 (CSR with the end marker = |logr|, as WP2's
  // setup.bin writes it; INTERFACES §5.1 does not fix the length)
  const size_t J = blk_ptr.empty() ? 0 : blk_ptr.size() - 1;
  if (code_ptr.size() == J + 1) {
    if (code_ptr[J] != (int64_t)logr.size()) throw Error(Status::invalid_input, path + ": code_ptr end marker != |logr|");
    code_ptr.pop_back();
  }
  if (J == 0 || code_ptr.size() != J || members.size() != (size_t)D.p || blk_ptr[0] != 0 || blk_ptr[J] != D.p) throw Error(Status::invalid_input, w + "partition shape");   // review PR39 m2: blk_ptr[0] = 0
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

// ---------------------------------------------------------------------------------------------------------------
// The setup's dimensions WITHOUT expanding it (review PR52 MAJOR-2; INTERFACES §7: admission before any allocation that
// grows with the setup). The file is mapped (every section hash verified, no heap copy of a section); what is read into
// memory is the block-size histogram (blk_ptr, J + 1 entries) and size_logmass (K + 1 entries). From them:
//  * k of the admission plan: q90 of the pi_0 size distribution (the rule of plan_island, from the persisted size_logmass)
//  * start_bytes_model(): the memory of the expanded dep::Start and neighbour lists, from the section sizes alone.
// StartView (WP3_DESIGN §1.12) replaces the model by the mapped section lengths. The reader split is shared with
// `calibrate`'s up-front admission (WP4, PR46 MAJOR-2): the dimensions are cheap, the arrays are read after admission.
struct SetupDims {
  std::string content_hash, data_hash; uint64_t file_bytes = 0;   // data_hash: setup.bin's meta.inputs["data.bin"] ("" if absent)
  int J = 0; int64_t p = 0; int K = 0;
  uint64_t nb_ptr_len = 0, nb_idx_len = 0;
  std::vector<uint64_t> m_hist = std::vector<uint64_t>(21, 0);   // number of blocks of m members, m = 1..20
  std::vector<double> size_logmass;                              // K + 1 entries
};

// verify = false: header and section-table hashes only (the admission needs the sizes; the sections are verified in full
// when load_start opens the file after admission)
inline SetupDims read_setup_dims(const std::string& path, int64_t p, int K, bool verify = true) {
  fmt::Reader R(path, verify);
  if (R.kind() != fmt::K_SETUP) throw Error(Status::invalid_input, path + ": not a setup file");
  const std::string w = path + ": ";
  SetupDims d; d.content_hash = R.content_hash(); d.p = p; d.K = K;
  { struct stat sb{}; d.file_bytes = ::stat(path.c_str(), &sb) == 0 ? (uint64_t)sb.st_size : 0; }
  { const Json m = R.json("meta");
    if (m.contains("inputs") && m.at("inputs").type() == Json::OBJ && m.at("inputs").contains("data.bin") && m.at("inputs").at("data.bin").type() == Json::STR)
      d.data_hash = m.at("inputs").at("data.bin").str(); }
  for (const char* nm : {"blk_ptr", "nb_ptr", "nb_idx", "logr", "size_logmass"})
    if (!R.has(nm)) throw Error(Status::invalid_input, w + "no section " + nm + " (the admission plan needs it; INTERFACES §5.1)");
  const auto blk_ptr = R.vec<int64_t>("blk_ptr");
  if (blk_ptr.size() < 2 || blk_ptr[0] != 0 || blk_ptr.back() != p) throw Error(Status::invalid_input, w + "partition shape");
  d.J = (int)(blk_ptr.size() - 1);
  for (size_t b = 0; b + 1 < blk_ptr.size(); ++b) {
    const int64_t m = blk_ptr[b + 1] - blk_ptr[b];
    if (m < 1 || m > 20) throw Error(Status::invalid_input, w + "block size outside 1..20");
    ++d.m_hist[(size_t)m];
  }
  uint64_t c = 0; R.get<int64_t>("nb_ptr", &c); d.nb_ptr_len = c; R.get<int32_t>("nb_idx", &c); d.nb_idx_len = c;
  if (d.nb_ptr_len != (uint64_t)p + 1) throw Error(Status::invalid_input, w + "nb_ptr has " + std::to_string(d.nb_ptr_len) + " entries, expected p + 1 = " + std::to_string(p + 1));
  d.size_logmass = R.vec<double>("size_logmass");
  if (d.size_logmass.size() != (size_t)K + 1) throw Error(Status::invalid_input, w + "size_logmass has " + std::to_string(d.size_logmass.size()) + " entries, expected K + 1 = " + std::to_string(K + 1));
  return d;
}

// q90 of the pi_0 size distribution + 1, with the floor 8 and the calibration's measured k_store: the plan's k
// (INTERFACES §7; the same rule as plan_island, which computes it from the rebuilt Start's size_logmass)
inline double pi0_size_q90(const std::vector<double>& size_logmass) {
  double k_pi0 = 0, acc = 0;
  for (size_t k = 0; k < size_logmass.size(); ++k) { acc += std::exp(size_logmass[k]); if (acc >= 0.90) { k_pi0 = (double)k; break; } }
  return k_pi0;
}
inline double plan_k(const std::vector<double>& size_logmass, double k_store) { return std::max({8.0, pi0_size_q90(size_logmass) + 1.0, k_store}); }

// An UPPER-BOUND model of the expanded dep::Start + neighbour lists (what start_bytes() measures after the fact, plus the
// per-row vector headers it leaves out): payloads, 24 B per std::vector, 16 B malloc header per allocation, x 2 for
// vectors grown by push_back / insert. It is the plan's caller-supplied term both before the load (admission) and in the
// run, so the pre-load refusal and the island's own admission are one number. Test `start_bytes_model_bounds_start_bytes`
// pins start_bytes() <= model <= 3 start_bytes() on the fixtures.
inline double start_bytes_model(const SetupDims& d) {
  const double K = d.K, J = d.J, p = (double)d.p, hdr = 40.0;
  double b = 0, flat = 0;
  for (int m = 1; m <= 20; ++m) {
    const double cnt = (double)d.m_hist[(size_t)m]; if (!cnt) continue;
    const int top = std::min(m, d.K);
    double nle = 0, c = 1;   // codes with popcount <= top: sum_j C(m, j)
    for (int j = 0; j <= top; ++j) { nle += c; c = c * (m - j) / (j + 1); }
    double cond = 0; for (int r = 0; r <= d.K; ++r) cond += std::min(top, r) + 1;
    const double ncode = std::ldexp(1.0, m);
    b += cnt * (hdr + m * 4.0 * 2                                   // blocks[b]
                + hdr + ncode * 8                                   // logr[b]
                + hdr + (top + 1) * 8.0                             // logprof[b]
                + hdr + (top + 1) * hdr + nle * 4.0 * 2             // codes_by_size[b]
                + hdr + (top + 1) * hdr + nle * 8.0                 // sub_cum[b]
                + hdr + (K + 1) * hdr + cond * 8.0);                // cond_cum[b]
    flat += cnt * ncode * 8.0;
  }
  b += hdr + flat * 2;                                              // logr_flat
  b += 6 * J * 24.0;                                                // the outer vectors (one row per block)
  b += 2 * (hdr + p * 4.0) + 2 * (hdr + (K + 1) * 8.0);             // blk, pos; size_logmass, size_cum
  b += hdr + (J + 1) * 8.0;                                         // code_ptr
  b += hdr + (J + 1) * ((K + 1) * 8.0 + hdr);                       // logF rows
  b += hdr + (K + 1) * J * 8.0;                                     // c0r
  b += 2 * hdr + (double)d.nb_ptr_len * 8.0 + (double)d.nb_idx_len * 4.0;   // neighbour lists
  return b;
}

inline Neighbours load_neighbours(const std::string& path, int p) {
  fmt::Reader R(path);
  if (!R.has("nb_ptr") || !R.has("nb_idx")) throw Error(Status::invalid_input, path + ": no neighbour lists (nb_ptr / nb_idx)");
  Neighbours nb; nb.ptr = R.vec<int64_t>("nb_ptr"); nb.idx = R.vec<int32_t>("nb_idx");
  if (nb.ptr.size() != (size_t)p + 1 || nb.ptr[0] != 0 || nb.ptr[(size_t)p] != (int64_t)nb.idx.size()) throw Error(Status::invalid_input, path + ": nb_ptr shape (" + std::to_string(nb.ptr.size()) + " entries for p = " + std::to_string(p) + ", ptr[0] = " + std::to_string(nb.ptr.empty() ? -1 : nb.ptr[0]) + ", ptr[p] = " + std::to_string(nb.ptr.size() > (size_t)p ? nb.ptr[(size_t)p] : -1) + ", |idx| = " + std::to_string(nb.idx.size()) + ")");
  for (int j = 0; j < p; ++j) {
    if (nb.ptr[j + 1] < nb.ptr[j]) throw Error(Status::invalid_input, path + ": nb_ptr not increasing");
    for (int64_t e = nb.ptr[j]; e < nb.ptr[j + 1]; ++e) if (nb.idx[e] < 0 || nb.idx[e] >= p || nb.idx[e] == j) throw Error(Status::invalid_input, path + ": nb_idx out of range");
  }
  return nb;
}

}  // namespace v4::island
