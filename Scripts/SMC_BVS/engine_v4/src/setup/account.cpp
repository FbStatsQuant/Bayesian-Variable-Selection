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
  auto add = [&](const char* name, const char* stage, uint64_t bytes, bool exact = true, bool stored = false) {
    A.items.push_back(MemItem{name, stage, bytes, exact, stored});
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
  const uint64_t ent = 26 + 4ull * P.B;
  add("table top stores kept (top 40p+1, lead0 20p, lead1 20p; pool bound B_blocks x i32)", "persistent", (ct + 2 * cl) * ent, false, true);
  add("table top stores fill peak extra (staging + merge run, about 1.5 x kept; WP1 Store)", "tables", (uint64_t)(1.5 * (double)((ct + 2 * cl) * ent)), false);
  // ---- start law (persistent) and D-18
  add("logprof_ptr, logprof", "persistent", 8ull * (J + 1) + 8ull * A.NR, true, true);
  add("logF ((J+1) x (K+1) f64)", "persistent", 8ull * (J + 1) * (K + 1), true, true);
  add("size_logmass, size_cum", "persistent", 16ull * (K + 1), true, true);
  add("cond_ptr, cond_cum", "persistent", 8ull * (J * (K + 1) + 1) + 8ull * A.cond_vals, true, true);
  add("static code tables (all m <= 16)", "persistent", 4ull * ((1u << 17) - 1));
  A.not_stored_d18 = 4ull * A.C_feasible + 8ull * A.C_feasible + 16ull * (A.NR + 1);
  // ---- start mode (transient)
  add("start mode: mb, arg (bound C_feasible u32), M, count DP, tie DP", "mode",
      8ull * A.NR + 8ull * (A.NR + 1) + 4ull * A.C_feasible + 24ull * A.NR + 8ull * (J + 1) * (K + 1) + 2ull * (J + 1) * (K + 1) + 16ull * J + A.NR, false);
  // ---- stage peaks
  auto sum = [&](std::initializer_list<const char*> stages) {
    uint64_t s = 0;
    for (auto& it : A.items) for (const char* st : stages) if (it.stage == st) s += it.bytes;
    return s;
  };
  const uint64_t data = sum({"data"});
  const uint64_t nbb = 8ull * (p + 1) + 4ull * nb, partb = 8ull * (J + 1) + 12ull * p;
  const uint64_t logr = 8ull * A.C + 8ull * (J + 1);
  uint64_t stores_kept = 0, stores_extra = 0, start = 0;
  for (auto& it : A.items) {
    if (it.name.rfind("table top stores kept", 0) == 0) stores_kept = it.bytes;
    if (it.name.rfind("table top stores fill", 0) == 0) stores_extra = it.bytes;
    if (it.stage == "persistent" && (it.name.rfind("logprof", 0) == 0 || it.name.rfind("logF", 0) == 0 || it.name.rfind("size_", 0) == 0 ||
                                     it.name.rfind("cond_", 0) == 0 || it.name.rfind("static", 0) == 0)) start += it.bytes;
  }
  const uint64_t edgesb = 16ull * edges;
  A.stage_peak.push_back({"correlation", data + sum({"corr"})});
  A.stage_peak.push_back({"partition", data + nbb + edgesb + sum({"partition"})});
  A.stage_peak.push_back({"tables", data + nbb + partb + logr + sum({"tables"}) + stores_kept});
  A.stage_peak.push_back({"start_law", data + nbb + partb + logr + stores_kept + start});
  A.stage_peak.push_back({"start_mode", data + nbb + partb + logr + stores_kept + start + sum({"mode"})});
  for (auto& sp : A.stage_peak) A.peak = std::max(A.peak, sp.second);
  (void)stores_extra;
  // ---- setup.bin bytes (64-aligned sections + header and table; dup/cut sections excluded: small, known after corr)
  uint64_t f = 128;
  int nsec = 0;
  for (auto& it : A.items) if (it.stored && it.name.rfind("static", 0) != 0) { f += al64(it.bytes); ++nsec; }
  f += 128ull * (nsec + 20) + 8 * 64;
  A.setup_bin = f;
  return A;
}

Json MemAccount::to_json() const {
  Json j = Json::object();
  j["n"] = n; j["p"] = p; j["K"] = K; j["B_coded"] = B; j["B_blocks"] = B_blocks; j["J"] = J; j["threads"] = threads;
  j["edges"] = edges; j["nb_nnz"] = nb_nnz;
  Json h = Json::object(); for (int m = 0; m < (int)hist.size(); ++m) if (hist[m]) h[std::to_string(m)] = hist[m];
  j["block_histogram"] = h;
  j["C"] = C; j["C_feasible"] = C_feasible; j["codes_per_column"] = p ? (double)C / (double)p : 0.0;
  j["mean_block"] = J ? (double)p / (double)J : 0.0; j["table_models"] = table_models;
  Json it = Json::array();
  for (auto& x : items) { Json e = Json::object(); e["name"] = x.name; e["stage"] = x.stage; e["bytes"] = (int64_t)x.bytes; e["exact"] = x.exact; e["in_setup_bin"] = x.stored; it.push(e); }
  j["items"] = it;
  Json sp = Json::object(); for (auto& s : stage_peak) sp[s.first] = (int64_t)s.second;
  j["stage_peak_bytes"] = sp; j["peak_bytes"] = (int64_t)peak; j["setup_bin_bytes"] = (int64_t)setup_bin;
  j["d18_not_stored_bytes"] = (int64_t)not_stored_d18;
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
  __m512 c[4][4];
  for (int q = 0; q < 4; ++q) for (int t = 0; t < 4; ++t) c[q][t] = _mm512_setzero_ps();
  for (int i = 0; i < n; ++i) {
    const float* r = R + (size_t)i * 64;
    const __m512 r0 = _mm512_loadu_ps(r), r1 = _mm512_loadu_ps(r + 16), r2 = _mm512_loadu_ps(r + 32), r3 = _mm512_loadu_ps(r + 48);
    for (int q = 0; q < 4; ++q) {
      const __m512 b = _mm512_set1_ps(xj[q][i]);
      c[q][0] = _mm512_fmadd_ps(b, r0, c[q][0]); c[q][1] = _mm512_fmadd_ps(b, r1, c[q][1]);
      c[q][2] = _mm512_fmadd_ps(b, r2, c[q][2]); c[q][3] = _mm512_fmadd_ps(b, r3, c[q][3]);
    }
  }
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
