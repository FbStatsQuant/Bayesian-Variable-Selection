// xeval.h -- cross predictive Hellinger between two store-BMA laws on the same dataset (EVAL-ONLY tool; PREREG criterion H of
// the 10^4 overlap, results/overlap1e4/OVERLAP_1e4_PREREG.md §3.6). Built as the library v4_xeval and the executable
// smcbvs4_xeval; the fit binary smcbvs4 and every fit-side source are untouched.
//
// d_H²(f̄_A, f̄_B) = 1 − ∫∫ √(f̄_A f̄_B) dy ν_x(dx), with f̄_A, f̄_B the mixture predictive densities of two laws (law.bin).
// The numerics are those of the engine's per-fit d_H(·, f*) (src/eval/dist.cpp, dist_metrics, "predictive"): the same x rows
// (eval::make_rows, rows x_row0 … x_row0 + n_x − 1 of the truth's design, eval seed), the same Gauss–Hermite grid
// (eval::gauss_hermite, 64 nodes), the same exact-top-K + stratified-tail estimator of each mixture density. The code of
// dist.cpp's static helpers is COPIED here (comp_at, log_comp, MixAt, Split, tail_sample) so that dist.cpp stays unchanged;
// a law equal to the truth (truth_law) reproduces the engine's own predictive h2 (test xeval_equals_engine_dH_to_truth).
#pragma once
#include <cstdint>
#include <string>

#include "v4/eval.h"

namespace v4::xeval {

struct CrossOpts {
  uint32_t seed = 1;        // tail samples (role POST) and non-gen rows (role TEST): the eval's seed rule (default: truth seed, low 32 bits)
  int n_x = 4000, n_gh = 64, threads = 1;
  int top_k = 1000, tail_r = 1000, tail_groups = 8, block_rows = 500;
  int x_row0 = 0;
};
struct CrossResult {
  double h2 = 0;            // 1 − mean_x affinity (pooled estimate)
  double se_x = 0;          // x-Monte-Carlo SE
  double se_tail = 0;       // between-group tail SE (0 when both laws are exact)
  double h2_topK = 0;       // top-K-only value (tail dropped, renormalised)
  double tail_mass_a = 0, tail_mass_b = 0;
  bool exact_a = true, exact_b = true;
  uint64_t top_a = 0, top_b = 0, tail_a = 0, tail_b = 0;
  int n_x = 0, n_gh = 0, groups = 0;
};

// The single-component law of the truth f* (Gaussian N(α* + xᵀβ*, σ²_eff)): B = truth_law(T) gives the engine's d_H(A, f*).
eval::Law truth_law(const eval::Truth& T);
// oid_a / oid_b select the tail-sample streams (Philox stage 1000 + 4·oid); the engine's store object T has oid 2. Use
// DIFFERENT ids for two store laws; assign them by a symmetric rule (the CLI orders the two laws by content hash) so that
// the result does not depend on which law is called A.
CrossResult cross_h2(const eval::Law& A, const eval::Law& B, const eval::Truth& T, const CrossOpts& o, uint32_t oid_a = 2, uint32_t oid_b = 6);

// The command (JSON args): --a law.bin --b law.bin | --b_truth 1, --truth truth.json, --out cross.json, optional --data data.bin
// (+ --data-b law B's own data.bin): each file's whole-file hash must equal its law's recorded inputs.data.bin hash and the two
// files must have the same DATA identity (section hashes of Xs_cm and ys, n, p, p_raw; not the whole-file hash, which embeds the
// writing binary's meta block). Without --data the two recorded hashes must be equal. --dataset ID --seed_id 1|2 (then `pairs` is filled),
// --seed, --threads, --n_x, --n_gh, --top_k, --tail_r, --tail_groups, --block_rows. Returns the record (schema
// overlap1e4.cross_vt/1 + an `xeval` block).
Json run(const Json& args);

}  // namespace v4::xeval
