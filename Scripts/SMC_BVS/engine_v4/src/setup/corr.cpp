// corr.cpp -- the correlation pass: neighbour graph (bit-equal to core/cpp/v3_blocks.h:149-173), duplicate
// components (core/cpp/v3_core.cpp:746-760) and the thresholded edge set, from streamed tiles. Memory
// O(threads * p * B + edges); nothing p x p.
#include <omp.h>
#include <algorithm>
#include <chrono>
#include "v4/setup.h"
#include "tiles.h"

namespace v4::setup {

namespace {
// Candidate order of core/cpp/v3_blocks.h:160-164: |r| descending, ties by smaller index.
inline bool cand_better(double ra, int a, double rb, int b) { return ra != rb ? ra > rb : a < b; }

// Per-thread bounded candidate lists: B slots per column, unsorted, with the position of the worst kept.
struct TopB {
  int B = 0; std::vector<double> v; std::vector<int32_t> id; std::vector<uint8_t> cnt, worst;
  void init(int p, int b) { B = b; v.assign((size_t)p * b, 0.0); id.assign((size_t)p * b, -1); cnt.assign(p, 0); worst.assign(p, 0); }
  inline void offer(int j, double r, int l) {
    double* vv = &v[(size_t)j * B]; int32_t* ii = &id[(size_t)j * B];
    int c = cnt[j];
    if (c < B) {
      vv[c] = r; ii[c] = l; cnt[j] = (uint8_t)(c + 1);
      if (c == 0 || cand_better(vv[worst[j]], ii[worst[j]], r, l)) worst[j] = (uint8_t)c;
      return;
    }
    int w = worst[j];
    if (!cand_better(r, l, vv[w], ii[w])) return;
    vv[w] = r; ii[w] = l;
    int nw = 0;
    for (int t = 1; t < B; ++t) if (cand_better(vv[nw], ii[nw], vv[t], ii[t])) nw = t;
    worst[j] = (uint8_t)nw;
  }
};

struct UF {
  std::vector<int32_t> parent;
  explicit UF(int p) : parent(p) { for (int j = 0; j < p; ++j) parent[j] = j; }
  int find(int i) { while (parent[i] != i) { parent[i] = parent[parent[i]]; i = parent[i]; } return i; }
  void unite(int a, int b) { int x = find(a), y = find(b); if (x != y) parent[std::max(x, y)] = std::min(x, y); }
};
// Components of size >= 2, members ascending, ordered by smallest member (= the union-find root, since the smaller
// root always wins): the order of core/cpp/v3_core.cpp:756-759 (std::map keyed by root).
Csr components(UF& uf, int p) {
  std::vector<int32_t> root(p), cnt(p, 0);
  for (int j = 0; j < p; ++j) { root[j] = uf.find(j); cnt[root[j]]++; }
  std::vector<int64_t> start(p, -1); int64_t tot = 0;
  Csr c;
  std::vector<int32_t> rows;
  for (int j = 0; j < p; ++j) if (root[j] == j && cnt[j] >= 2) { start[j] = tot; tot += cnt[j]; rows.push_back(j); }
  c.idx.assign(tot, 0);
  std::vector<int64_t> fill = start;
  for (int j = 0; j < p; ++j) { int r = root[j]; if (start[r] >= 0) c.idx[fill[r]++] = j; }
  for (int r : rows) c.ptr.push_back(start[r] + cnt[r]);
  return c;
}
}  // namespace

Csr dup_components(int p, const std::vector<Edge>& edges) {
  UF uf(p);
  for (const Edge& e : edges) if (e.absr >= 1 - 1e-10) uf.unite(e.j, e.l);  // core/cpp/v3_core.cpp:754
  return components(uf, p);
}

CorrResult correlation_pass(const Data& D, const CorrOptions& o) {
  auto t0 = std::chrono::steady_clock::now();
  const int p = D.p, B = o.B;
  if (B < 1 || B > 255) throw Error(Status::invalid_input, "correlation_pass: B out of range");
  CorrResult R;
  // core/cpp/v3_blocks.h:154 (and :14 for s_j = sqrt(G_jj), core/cpp/v3_core.cpp:808 for rho)
  R.rn = std::sqrt(2.0 * pm::log((double)p) / D.n);
  R.tau = o.tau < 0 ? R.rn : o.tau;
  const double hcut = 1.0 - R.tau, rho = R.rn;
  const int64_t max_edges = o.max_edges > 0 ? o.max_edges : 64 * (int64_t)p;
  std::vector<double> s(p);
  for (int j = 0; j < p; ++j) s[j] = std::sqrt(D.diagG[j]);
  const int T = std::max(1, o.threads);
  std::vector<TopB> heaps(T);
  std::vector<std::vector<Edge>> edges(T);
  std::vector<uint64_t> pairs(T, 0);
  std::atomic<bool> overflow{false};
#pragma omp parallel for num_threads(T) schedule(static, 1)
  for (int t = 0; t < T; ++t) heaps[t].init(p, std::min(B, std::max(p - 1, 1)));
  detail::tile_pass(D, o.tile, T, [&](int tid, int j, int l0, int cnt, const double* G) {
    TopB& H = heaps[tid];
    std::vector<Edge>& E = edges[tid];
    const double sj = s[j];
    for (int t = 0; t < cnt; ++t) {
      const int l = l0 + t;
      const double ar = std::fabs(G[t] / (sj * s[l]));  // core/cpp/v3_blocks.h:15, :161
      H.offer(j, ar, l);
      H.offer(l, ar, j);
      if (o.keep_edges && (ar >= rho || (1.0 - ar) <= hcut || ar >= 1 - 1e-10)) E.push_back(Edge{j, l, ar});
    }
    pairs[tid] += cnt;
    if ((int64_t)E.size() > max_edges) overflow = true;
  });
  if (overflow) throw Error(Status::resource_limit, "correlation_pass: more than max_edges edges (hub design); raise max_edges");
  for (uint64_t c : pairs) R.pairs += c;
  // Merge the per-thread lists (top-B of a union under a strict total order: independent of the split), then the
  // selection of core/cpp/v3_blocks.h:165-168 and the symmetric union of :170-171.
  std::vector<int32_t> chosen((size_t)p * B, -1);
  std::vector<uint8_t> nchosen(p, 0);
#pragma omp parallel num_threads(T)
  {
    std::vector<std::pair<double, int32_t>> c;
#pragma omp for schedule(static, 1024)
    for (int j = 0; j < p; ++j) {
      c.clear();
      for (int t = 0; t < T; ++t) {
        const TopB& H = heaps[t];
        for (int q = 0; q < H.cnt[j]; ++q) c.push_back({H.v[(size_t)j * H.B + q], H.id[(size_t)j * H.B + q]});
      }
      std::sort(c.begin(), c.end(), [](const auto& a, const auto& b) { return cand_better(a.first, a.second, b.first, b.second); });
      int above = 0;
      for (size_t q = 0; q < c.size() && (int)q < B; ++q) { if (c[q].first > R.rn) ++above; else break; }
      int keep = std::min(B, std::max(1, above));
      keep = std::min<int>(keep, (int)c.size());
      for (int q = 0; q < keep; ++q) chosen[(size_t)j * B + q] = c[q].second;
      nchosen[j] = (uint8_t)keep;
    }
  }
  heaps.clear(); heaps.shrink_to_fit();
  {
    std::vector<uint64_t> pr;
    size_t tot = 0; for (int j = 0; j < p; ++j) tot += nchosen[j];
    pr.reserve(2 * tot);
    for (int j = 0; j < p; ++j)
      for (int q = 0; q < nchosen[j]; ++q) {
        uint64_t l = (uint32_t)chosen[(size_t)j * B + q];
        pr.push_back(((uint64_t)j << 32) | l); pr.push_back((l << 32) | (uint64_t)j);
      }
    std::sort(pr.begin(), pr.end());
    pr.erase(std::unique(pr.begin(), pr.end()), pr.end());
    R.nb.ptr.assign(p + 1, 0); R.nb.idx.resize(pr.size());
    for (size_t q = 0; q < pr.size(); ++q) { R.nb.ptr[(pr[q] >> 32) + 1]++; R.nb.idx[q] = (int32_t)(pr[q] & 0xffffffffu); }
    for (int j = 0; j < p; ++j) R.nb.ptr[j + 1] += R.nb.ptr[j];
  }
  if (o.keep_edges) {
    size_t tot = 0; for (auto& e : edges) tot += e.size();
    if ((int64_t)tot > max_edges) throw Error(Status::resource_limit, "correlation_pass: more than max_edges edges (hub design); raise max_edges");
    R.edges.reserve(tot);
    for (auto& e : edges) { R.edges.insert(R.edges.end(), e.begin(), e.end()); std::vector<Edge>().swap(e); }
    std::sort(R.edges.begin(), R.edges.end(), [](const Edge& a, const Edge& b) { return a.j != b.j ? a.j < b.j : a.l < b.l; });
    R.dup = dup_components(p, R.edges);
  }
  R.seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  return R;
}

Csr cut_groups(int p, const std::vector<Edge>& edges, double rho, const Partition& P) {
  // core/cpp/v3_core.cpp:792-818: union-find over {|r| >= rho} (uncapped, no forced partner); flag components whose
  // members lie in >= 2 blocks; components in order of their smallest member; members ascending.
  UF uf(p);
  for (const Edge& e : edges) if (e.absr >= rho) uf.unite(e.j, e.l);
  Csr all = components(uf, p), out;
  for (int64_t c = 0; c < all.rows(); ++c) {
    const int32_t* b = all.idx.data() + all.ptr[c]; const int32_t* e = all.idx.data() + all.ptr[c + 1];
    int first = P.blk[*b]; bool span = false;
    for (const int32_t* q = b; q != e; ++q) if (P.blk[*q] != first) { span = true; break; }
    if (span) out.push_row(b, e);
  }
  return out;
}

}  // namespace v4::setup
