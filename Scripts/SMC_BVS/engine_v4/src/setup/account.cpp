// account.cpp -- exact byte accounting of every setup array from the partition alone, the admission rule's input, and
// `setup --count-only` (Sol review EXP_CP1 §F1; PR13 review m2). Also the float32 AVX-512 candidate filter used by
// count-only to find the production edge set at p = 10^6 quickly; every candidate is re-checked in double with the
// production predicate, so the edge set (hence the partition, histogram and C) is exactly production's.
#include <immintrin.h>
#include <omp.h>
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include "v4/setup.h"

namespace v4::setup {

namespace {
uint64_t al64(uint64_t b) { return (b + 63) & ~uint64_t(63); }
int64_t binom(int m, int j) { int64_t c = 1; for (int i = 1; i <= j; ++i) c = c * (m - j + i) / i; return c; }
}  // namespace

MemAccount account(const Data& D, int coded_B, const Partition& P, int64_t edges, int64_t nb_nnz, int threads, PartMode mode) {
  MemAccount A;
  const int64_t n = D.n, p = D.p, K = D.K, J = P.J, TH = std::max(1, threads);
  A.n = n; A.p = p; A.K = K; A.B = coded_B; A.B_blocks = P.B; A.J = J; A.threads = TH; A.edges = edges; A.nb_nnz = nb_nnz;
  A.hist.assign(17, 0);
  int maxm = 0;
  for (int b = 0; b < J; ++b) {
    const int m = P.size(b), top = (int)std::min<int64_t>(m, K);
    A.hist[m]++; maxm = std::max(maxm, m);
    A.C += (int64_t)1 << m;
    for (int j = 0; j <= top; ++j) A.C_feasible += binom(m, j);
    A.NR += top + 1;
    for (int64_t r = 0; r <= K; ++r) A.cond_vals += std::min<int64_t>(top, r) + 1;
  }
  A.table_models = A.C_feasible - (J - 1);  // the empty model counted once
  const int64_t Bn = std::min<int64_t>(coded_B, std::max<int64_t>(p - 1, 1));
  const int64_t nb = nb_nnz >= 0 ? nb_nnz : 2 * p * Bn;  // the symmetric union has at most 2 p B entries in total
  // est: the estimate used beside a bound (measured factors, labelled in the name); = bytes for exact items
  auto add = [&](const char* name, const char* stage, uint64_t bytes, bool exact = true, bool stored = false, int64_t est = -1) {
    MemItem it{name, stage, bytes, exact, stored}; it.est = est < 0 ? bytes : (uint64_t)est; A.items.push_back(it);
  };
  // ---- data (data.bin, mapped): X and the per-column arrays
  add("X (n x p f64)", "data", 8ull * n * p, true, false);
  add("ys, z, diagG, col_max, col_mean, col_sd, orig", "data", 8ull * n + 5 * 8ull * p + 4ull * p);
  // ---- correlation pass (transient)
  add("corr: global top-B lists (f64 + i32 per slot, 2 u8 per column)", "corr", (uint64_t)p * Bn * 12 + 2ull * p);
  add("corr: per-thread tile copy + accumulators + block-local top-B", "corr", (uint64_t)TH * (8ull * n * 256 + 8ull * 4 * 256 + 2ull * 256 * Bn * 12));
  add("corr: chosen + counts", "corr", 4ull * p * Bn + p);
  add("corr: neighbour pair list before unique (bound 2 p B)", "corr", 16ull * p * Bn, false);
  add("edges (j, l, |r|), x2 while merging per-thread lists", "corr", 2 * 16ull * edges);
  // ---- persistent setup objects
  add("neighbours CSR (nb_ptr, nb_idx)", "persistent", 8ull * (p + 1) + 4ull * nb, nb_nnz >= 0, true);
  add("partition (blk_ptr, blk_members, blk, pos)", "persistent", 8ull * (J + 1) + 12ull * p, true, true);
  // ---- partition transient
  if (mode == PartMode::Exact) add("exact linkage: dense distances 8 p^2 + members", "partition", 8ull * p * p + 32ull * p, false);
  else add("truncated linkage: adjacency, members, std::set (per-node estimate)", "partition", 2 * 24ull * edges + 2 * 64ull * edges + 2ull * p * (24 + 24 + 8 + 24), false);
  // ---- tables
  add("logr (C f64)", "persistent", 8ull * A.C, true, true);
  add("code_ptr", "persistent", 8ull * (J + 1), true, true);
  add("tables: per-batch log m buffers (threads x 16 blocks x 2^maxm f64)", "tables", (uint64_t)TH * 16 * 8ull * ((uint64_t)1 << maxm));
  // stores: entry = v f64 + off u64 + hash u64 + len u16 = 26 B, pool <= B_blocks int32 per entry (bound)
  const uint64_t ct = std::min<uint64_t>(40ull * p + 1, (uint64_t)A.table_models), cl = std::min<uint64_t>(20ull * p, (uint64_t)A.table_models);
  // entry = 26 B exact (v, off, hash, len) + pool: bound B_blocks int32; estimate 3.1 int32 (MEASURED mean |S| of the
  // table stores: 3.03 top / 2.59 leads at p = 1e5 and 3e4, AR n = 200)
  const uint64_t ent = 26 + 4ull * P.B, ent_est = 26 + 12;
  add("table top stores kept (top 40p+1, lead0 20p, lead1 20p; pool bound B_blocks x i32, estimate 3.1 x i32)", "persistent",
      (ct + 2 * cl) * ent, false, true, (int64_t)((ct + 2 * cl) * ent_est));
  // fill transient (two-pass build, serial offers): the three staging runs (<= c_i / 4 each, WP1 Store trigger) plus one
  // merge run (<= the top store's c) at a time
  add("table top stores fill transient (staging c_i/4 x 3 + one merge run <= c_top)", "tables", (ct / 4 + cl / 2 + ct) * ent, false, false,
      (int64_t)((ct / 4 + cl / 2 + ct) * ent_est));
  // ---- start law (persistent) and D-18
  add("logprof_ptr, logprof", "persistent", 8ull * (J + 1) + 8ull * A.NR, true, true);
  add("logF ((J+1) x (K+1) f64)", "persistent", 8ull * (J + 1) * (K + 1), true, true);
  add("size_logmass, size_cum", "persistent", 16ull * (K + 1), true, true);
  add("cond0 (D-31 scan table P(k_b = 0 | r), J x (K+1) f64)", "persistent", 8ull * J * (K + 1), true, true);
  add("static code tables (all m <= 16)", "persistent", 4ull * ((1u << 17) - 1));
  A.not_stored_d18 = 4ull * A.C_feasible + 8ull * A.C_feasible + 16ull * (A.NR + 1);
  A.not_stored_d31 = 8ull * (J * (K + 1) + 1) + 8ull * A.cond_vals;   // cond_ptr + cond_cum, recomputed by cond_row
  // ---- start mode (transient)
  // arg: codes attaining each per-size maximum; bound C_feasible, estimate NR (one per row without exact ties)
  const uint64_t mode_fixed = 8ull * A.NR + 8ull * (A.NR + 1) + 24ull * A.NR + 8ull * (J + 1) * (K + 1) + 2ull * (J + 1) * (K + 1) + 16ull * J + A.NR;
  add("start mode: mb, arg (bound C_feasible u32, estimate NR u32), M, count DP, tie DP", "mode", mode_fixed + 4ull * A.C_feasible, false, false,
      (int64_t)(mode_fixed + 4ull * A.NR));
  // ---- stage peaks (bound and estimate): the arrays live in each stage
  auto stage_sum = [&](bool est, std::initializer_list<const char*> stages, std::initializer_list<const char*> names) {
    uint64_t t = 0;
    for (auto& it : A.items) {
      bool in = false;
      for (const char* st : stages) if (it.stage == st) in = true;
      for (const char* nm : names) if (it.name.rfind(nm, 0) == 0) in = true;
      if (in) t += est ? it.est : it.bytes;
    }
    return t;
  };
  for (int est = 0; est < 2; ++est) {
    auto& sp = est ? A.stage_peak_est : A.stage_peak;
    sp.clear();
    sp.push_back({"correlation", stage_sum(est, {"corr"}, {"X (", "ys, z"})});
    sp.push_back({"partition", stage_sum(est, {"partition"}, {"X (", "ys, z", "neighbours", "edges"})});
    sp.push_back({"tables", stage_sum(est, {"tables"}, {"X (", "ys, z", "neighbours", "partition (", "logr", "code_ptr", "table top stores kept"})});
    // PR50 MAJOR-2: selected by stage, not by display name, so a renamed or new persistent item (cond0 in D-31) cannot drop
    // out of the live set: start law = every data item + every persistent item; start mode = those + the mode transient.
    sp.push_back({"start_law", stage_sum(est, {"data", "persistent"}, {})});
    sp.push_back({"start_mode", stage_sum(est, {"data", "persistent", "mode"}, {})});
    uint64_t pk = 0; for (auto& x : sp) pk = std::max(pk, x.second);
    (est ? A.peak_est : A.peak) = pk;
  }
  // ---- setup.bin bytes (64-aligned sections + header and table; dup/cut sections excluded: small, known after corr)
  uint64_t f = 128;
  int nsec = 0;
  uint64_t fe = 128;
  for (auto& it : A.items) if (it.stored && it.name.rfind("static", 0) != 0) { f += al64(it.bytes); fe += al64(it.est); ++nsec; }
  f += 128ull * (nsec + 20) + 8 * 64; fe += 128ull * (nsec + 20) + 8 * 64;
  A.setup_bin = f; A.setup_bin_est = fe;
  return A;
}

Json MemAccount::to_json() const {
  Json j = Json::object();
  j["n"] = n; j["p"] = p; j["K"] = K; j["B_coded"] = B; j["B_blocks"] = B_blocks; j["J"] = J; j["threads"] = threads;
  j["edges"] = edges; j["nb_nnz"] = nb_nnz;
  Json h = Json::object(); for (int m = 0; m < (int)hist.size(); ++m) if (hist[m]) h[std::to_string(m)] = hist[m];
  j["block_histogram"] = h;
  j["C"] = C; j["C_feasible"] = C_feasible; j["codes_per_column"] = p ? (double)C / (double)p : 0.0;
  j["mean_block"] = J ? (double)p / (double)J : 0.0; j["table_models"] = table_models; j["NR"] = NR; j["cond_vals"] = cond_vals;
  Json it = Json::array();
  for (auto& x : items) { Json e = Json::object(); e["name"] = x.name; e["stage"] = x.stage; e["bytes"] = (int64_t)x.bytes; e["estimate_bytes"] = (int64_t)x.est; e["exact"] = x.exact; e["in_setup_bin"] = x.stored; it.push(e); }
  j["items"] = it;
  Json sp = Json::object(); for (auto& s : stage_peak) sp[s.first] = (int64_t)s.second;
  Json se = Json::object(); for (auto& s : stage_peak_est) se[s.first] = (int64_t)s.second;
  j["stage_peak_bytes"] = sp; j["peak_bytes"] = (int64_t)peak; j["setup_bin_bytes"] = (int64_t)setup_bin;
  j["stage_peak_estimate_bytes"] = se; j["peak_estimate_bytes"] = (int64_t)peak_est; j["setup_bin_estimate_bytes"] = (int64_t)setup_bin_est;
  j["peak_note"] = "peak_bytes: exact arrays + upper bounds (store pools at B_blocks per entry, start-mode ties at C_feasible); "
                   "peak_estimate_bytes: the same with measured factors (mean |S| 3.1 in the table stores, no exact ties). X is file-backed (data.bin mapping).";
  j["d18_not_stored_bytes"] = (int64_t)not_stored_d18; j["d31_not_stored_bytes"] = (int64_t)not_stored_d31;
  return j;
}

// ---------------------------------------------------------------- float32 candidate filter (count-only)
// Columns are normalised in double and rounded to float: a_j = fl32(x_j / s_j). The float32 dot product of length n
// (FMA, any order) satisfies |r~ - r| <= (n + 4) u (1 + O(nu)) with u = 2^-24, since sum |a_i b_i| <= ||a|| ||b|| ~ 1.
// Candidates: |r~| >= thr - margin, margin = 2 (n + 8) u, thr = min(rho, tau, 1 - 1e-10). Every candidate is
// re-checked with the production arithmetic (v4::gram, sequential in double) and the production predicate of
// correlation_pass, so a pair is kept iff the exact pass would keep it.
bool filter_available() { return __builtin_cpu_supports("avx512f"); }

namespace {
// 4 rows j (columns of the j-tile) x 64 columns l of the row-major tile R (n x 64 floats). Writes hit pairs.
__attribute__((target("avx512f,fma")))
int micro_4x64(const float* const* xj, const float* R, int n, float thr, int jbase, int l0, int lmin_off[4], int32_t* hits) {
  // 16 named accumulators (an indexed array is not kept in registers at -O2)
  __m512 c00 = _mm512_setzero_ps(), c01 = c00, c02 = c00, c03 = c00, c10 = c00, c11 = c00, c12 = c00, c13 = c00;
  __m512 c20 = c00, c21 = c00, c22 = c00, c23 = c00, c30 = c00, c31 = c00, c32 = c00, c33 = c00;
  const float *x0 = xj[0], *x1 = xj[1], *x2 = xj[2], *x3 = xj[3];
  for (int i = 0; i < n; ++i) {
    const float* r = R + (size_t)i * 64;
    const __m512 r0 = _mm512_loadu_ps(r), r1 = _mm512_loadu_ps(r + 16), r2 = _mm512_loadu_ps(r + 32), r3 = _mm512_loadu_ps(r + 48);
    __m512 b = _mm512_set1_ps(x0[i]);
    c00 = _mm512_fmadd_ps(b, r0, c00); c01 = _mm512_fmadd_ps(b, r1, c01); c02 = _mm512_fmadd_ps(b, r2, c02); c03 = _mm512_fmadd_ps(b, r3, c03);
    b = _mm512_set1_ps(x1[i]);
    c10 = _mm512_fmadd_ps(b, r0, c10); c11 = _mm512_fmadd_ps(b, r1, c11); c12 = _mm512_fmadd_ps(b, r2, c12); c13 = _mm512_fmadd_ps(b, r3, c13);
    b = _mm512_set1_ps(x2[i]);
    c20 = _mm512_fmadd_ps(b, r0, c20); c21 = _mm512_fmadd_ps(b, r1, c21); c22 = _mm512_fmadd_ps(b, r2, c22); c23 = _mm512_fmadd_ps(b, r3, c23);
    b = _mm512_set1_ps(x3[i]);
    c30 = _mm512_fmadd_ps(b, r0, c30); c31 = _mm512_fmadd_ps(b, r1, c31); c32 = _mm512_fmadd_ps(b, r2, c32); c33 = _mm512_fmadd_ps(b, r3, c33);
  }
  const __m512 c[4][4] = {{c00, c01, c02, c03}, {c10, c11, c12, c13}, {c20, c21, c22, c23}, {c30, c31, c32, c33}};
  const __m512 th = _mm512_set1_ps(thr);
  int nh = 0;
  for (int q = 0; q < 4; ++q)
    for (int t = 0; t < 4; ++t) {
      __mmask16 mk = _mm512_cmp_ps_mask(_mm512_abs_ps(c[q][t]), th, _CMP_GE_OQ);
      while (mk) {
        int bit = __builtin_ctz(mk); mk &= mk - 1;
        int off = t * 16 + bit;
        if (off < lmin_off[q]) continue;  // only l > j
        hits[2 * nh] = jbase + q; hits[2 * nh + 1] = l0 + off; ++nh;
      }
    }
  return nh;
}
}  // namespace

std::vector<Edge> edges_by_filter(const Data& D, double tau, int threads, uint64_t* candidates) {
  if (!filter_available()) throw Error(Status::internal_error, "edges_by_filter: AVX-512F not available");
  const int n = D.n, p = D.p, TH = std::max(1, threads);
  const double rn = std::sqrt(2.0 * pm::log((double)p) / D.n), hcut = 1.0 - tau;
  const double u = std::ldexp(1.0, -24), margin = 2.0 * (n + 8) * u;
  const double thr = std::min({rn, tau, 1 - 1e-10}) - margin - 1e-12;
  std::vector<double> s(p);
  for (int j = 0; j < p; ++j) s[j] = std::sqrt(D.diagG[j]);
  // normalised float copy, column-major, padded to a multiple of 64 columns with zero columns
  const int nt = (p + 63) / 64, pp = nt * 64;
  std::vector<float> A((size_t)pp * n, 0.0f);
#pragma omp parallel for num_threads(TH) schedule(static, 1024)
  for (int j = 0; j < p; ++j) { const double* x = D.col(j); for (int i = 0; i < n; ++i) A[(size_t)j * n + i] = (float)(x[i] / s[j]); }
  std::vector<std::vector<Edge>> out(TH);
  std::vector<uint64_t> cand(TH, 0);
  std::atomic<int> next{0};
  std::atomic<bool> failed{false};
  const float thrf = (float)thr;  // rounding thr to float moves it by <= u |thr|, inside the margin's slack (margin >= 16u)
#pragma omp parallel num_threads(TH)
  {
    try {
      const int tid = omp_get_thread_num();
      std::vector<float> R((size_t)n * 64);
      std::vector<int32_t> hits(2 * 4 * 64);
      for (;;) {
        int uu = next.fetch_add(1);
        if (uu >= nt || failed) break;
        const int Jt = nt - 1 - uu, l0 = Jt * 64;
        for (int t = 0; t < 64; ++t) { const float* a = &A[(size_t)(l0 + t) * n]; for (int i = 0; i < n; ++i) R[(size_t)i * 64 + t] = a[i]; }
        for (int j = 0; j < std::min(p, l0 + 64); j += 4) {
          const float* xj[4]; int lmin[4];
          for (int q = 0; q < 4; ++q) { xj[q] = &A[(size_t)(j + q) * n]; lmin[q] = std::max(0, j + q - l0 + 1); }
          int nh = micro_4x64(xj, R.data(), n, thrf, j, l0, lmin, hits.data());
          for (int h = 0; h < nh; ++h) {
            const int a = hits[2 * h], b = hits[2 * h + 1];
            if (a >= p || b >= p) continue;  // padding columns
            ++cand[tid];
            const double ar = std::fabs(gram(D, a, b) / (s[a] * s[b]));  // production arithmetic (corr.cpp)
            if (ar >= rn || (1.0 - ar) <= hcut || ar >= 1 - 1e-10) out[tid].push_back(Edge{a, b, ar});
          }
        }
      }
    } catch (...) { failed = true; }
  }
  if (failed) throw Error(Status::resource_limit, "edges_by_filter: allocation failed");
  std::vector<Edge> E;
  for (auto& v : out) { E.insert(E.end(), v.begin(), v.end()); std::vector<Edge>().swap(v); }
  std::sort(E.begin(), E.end(), [](const Edge& x, const Edge& y) { return x.j != y.j ? x.j < y.j : x.l < y.l; });
  if (candidates) { *candidates = 0; for (auto c : cand) *candidates += c; }
  return E;
}

CountResult count_only(const Data& D, const PartitionOptions& po0, int coded_B, int threads, bool allow_filter) {
  CountResult R;
  PartitionOptions po = po0; po.B = coded_B; po.threads = threads;
  auto t0 = std::chrono::steady_clock::now();
  const double rn = std::sqrt(2.0 * pm::log((double)D.p) / D.n);
  const double tau = po.tau < 0 ? rn : po.tau;
  if (allow_filter && filter_available() && po.mode == PartMode::Truncated) {
    R.corr.edges = edges_by_filter(D, tau, threads, &R.candidates);
    R.corr.rn = rn; R.corr.tau = tau; R.filter_used = true;
    R.corr.dup = dup_components(D.p, R.corr.edges);
  } else {
    CorrOptions co; co.B = coded_B; co.threads = threads; co.tau = po.tau;
    R.corr = correlation_pass(D, co);
  }
  R.seconds_edges = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  t0 = std::chrono::steady_clock::now();
  R.part = make_partition(D, R.corr, po);
  R.seconds_partition = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  R.acc = account(D, coded_B, R.part, (int64_t)R.corr.edges.size(), R.filter_used ? -1 : (int64_t)R.corr.nb.idx.size(), threads, po.mode);
  return R;
}

}  // namespace v4::setup
