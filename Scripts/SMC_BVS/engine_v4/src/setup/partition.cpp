// partition.cpp -- complete linkage (exact: copy of core/cpp/v3_blocks.h:46-108; truncated: D-4 / THEORY-1 rule on
// the sparse edge set), the top-down cut and next-fit packing (core/cpp/v3_blocks.h:110-144).
#include <algorithm>
#include <iterator>
#include <set>
#include "v4/setup.h"
#include "tiles.h"

namespace v4::setup {

namespace {
// core/cpp/v3_blocks.h:19-30 (R13 tie rule): lexicographic comparison of the sorted unions (a u b) vs (c u d).
bool union_lex_less(const std::vector<int32_t>& a, const std::vector<int32_t>& b, const std::vector<int32_t>& c, const std::vector<int32_t>& d) {
  size_t ia = 0, ib = 0, ic = 0, id = 0;
  while (true) {
    bool e1 = (ia == a.size() && ib == b.size()), e2 = (ic == c.size() && id == d.size());
    if (e1 || e2) return e1 && !e2;  // proper prefix precedes
    int x, y;
    if (ib == b.size() || (ia < a.size() && a[ia] < b[ib])) x = a[ia++]; else x = b[ib++];
    if (id == d.size() || (ic < c.size() && c[ic] < d[id])) y = c[ic++]; else y = d[id++];
    if (x != y) return x < y;
  }
}
void forest_init(Forest& T, int p) {
  T.p = p;
  T.left.assign(p, -1); T.right.assign(p, -1); T.size.assign(p, 1); T.minidx.resize(p); T.height.assign(p, 0.0);
  for (int j = 0; j < p; ++j) T.minidx[j] = j;
}
// New node; left child = child with the smaller minimum index (R13; core/cpp/v3_blocks.h:84-89).
int forest_merge(Forest& T, int na, int nb, double h) {
  int L = (T.minidx[na] < T.minidx[nb]) ? na : nb, R = (L == na) ? nb : na;
  T.left.push_back(L); T.right.push_back(R); T.size.push_back(T.size[na] + T.size[nb]);
  T.minidx.push_back(std::min(T.minidx[na], T.minidx[nb])); T.height.push_back(h);
  return (int)T.left.size() - 1;
}
// core/cpp/v3_blocks.h:110-119 (iterative; left child first).
void subtree_leaves(const Forest& T, int nd, std::vector<int32_t>& out) {
  std::vector<int32_t> st{nd};
  while (!st.empty()) {
    int x = st.back(); st.pop_back();
    if (x < T.p) { out.push_back(x); continue; }
    st.push_back(T.right[x]); st.push_back(T.left[x]);
  }
}
}  // namespace

// ---------------------------------------------------------------- exact (theory mode)
// core/cpp/v3_blocks.h:39-108, unchanged except that the dense distance matrix d_jl = 1 - |r_jl| is filled from the
// streamed tiles (the same bits as core/cpp/v3_blocks.h:10-17 + :53-55) and r is not kept: 8 p^2 bytes instead of 24 p^2.
Forest complete_linkage_exact(const Data& D, int threads) {
  const int p = D.p;
  Forest T; forest_init(T, p);
  if (p == 1) { T.roots = {0}; return T; }
  std::vector<double> dist((size_t)p * p, 0.0);
  {
    std::vector<double> s(p);
    for (int j = 0; j < p; ++j) s[j] = std::sqrt(D.diagG[j]);
    for (int j = 0; j < p; ++j) dist[(size_t)j * p + j] = 1.0 - std::fabs(D.diagG[j] / (s[j] * s[j]));
    detail::tile_pass(D, 256, std::max(1, threads), [&](int, int j, int l0, int cnt, const double* G) {
      for (int t = 0; t < cnt; ++t) {
        int l = l0 + t;
        double v = 1.0 - std::fabs(G[t] / (s[j] * s[l]));
        dist[(size_t)l * p + j] = v; dist[(size_t)j * p + l] = v;
      }
    });
  }
  std::vector<std::vector<int32_t>> mem(p);
  std::vector<int> node(p);
  std::vector<char> active(p, 1);
  for (int j = 0; j < p; ++j) { mem[j] = {j}; node[j] = j; }
  std::vector<int> best(p, -1);
  std::vector<double> bestd(p, POS_INF);
  auto pair_less = [&](int i, int j, int c, int d2) {
    double dij = dist[(size_t)j * p + i], dcd = dist[(size_t)d2 * p + c];
    if (dij != dcd) return dij < dcd;
    return union_lex_less(mem[i], mem[j], mem[c], mem[d2]);
  };
  auto recompute_row = [&](int i) {
    best[i] = -1; bestd[i] = POS_INF;
    for (int j = 0; j < p; ++j) {
      if (j == i || !active[j]) continue;
      if (best[i] < 0 || pair_less(i, j, i, best[i])) { best[i] = j; bestd[i] = dist[(size_t)j * p + i]; }
    }
  };
  for (int i = 0; i < p; ++i) recompute_row(i);
  for (int step = 0; step < p - 1; ++step) {
    int bi = -1;
    for (int i = 0; i < p; ++i) {
      if (!active[i] || best[i] < 0) continue;
      if (bi < 0 || pair_less(i, best[i], bi, best[bi])) bi = i;
    }
    int a = bi, b = best[bi];
    double h = dist[(size_t)b * p + a];
    int nn = forest_merge(T, node[a], node[b], h);
    std::vector<int32_t> u; u.reserve(mem[a].size() + mem[b].size());
    std::merge(mem[a].begin(), mem[a].end(), mem[b].begin(), mem[b].end(), std::back_inserter(u));
    mem[a].swap(u); mem[b].clear(); mem[b].shrink_to_fit(); active[b] = 0; node[a] = nn;
    for (int x = 0; x < p; ++x) {
      if (!active[x] || x == a) continue;
      double v = std::max(dist[(size_t)x * p + a], dist[(size_t)x * p + b]);
      dist[(size_t)x * p + a] = v; dist[(size_t)a * p + x] = v;
    }
    recompute_row(a);
    for (int x = 0; x < p; ++x) {
      if (!active[x] || x == a) continue;
      if (best[x] == a || best[x] == b) recompute_row(x);
      else if (pair_less(x, a, x, best[x])) { best[x] = a; bestd[x] = dist[(size_t)a * p + x]; }
    }
  }
  T.roots = {(int32_t)T.left.size() - 1};
  return T;
}

// ---------------------------------------------------------------- truncated (V-1M; D-4)
// Complete linkage restricted to merges at height <= hcut (strict: < hcut). A pair of clusters is a candidate iff every
// cross pair is an edge (d_jl passes the predicate); its distance is the max over the cross pairs (exact: max does not
// round). Candidates of a merged cluster C = A u B are the clusters adjacent to both A and B, with distance
// max(d(A,X), d(B,X)) (Lance-Williams for complete linkage). The next merge is the candidate pair smallest under
// (distance, union-lex) (R13), the left child the one with the smaller minimum index. Because complete linkage merges
// in non-decreasing height, the result equals the exact dendrogram's merges of height <= hcut, with the same node
// ids, children and heights (gate T11).
Forest complete_linkage_truncated(int p, const std::vector<Edge>& edges, double hcut, bool strict) {
  Forest T; forest_init(T, p);
  auto ok = [&](double d) { return strict ? d < hcut : d <= hcut; };
  std::vector<std::vector<int32_t>> mem(p);
  for (int j = 0; j < p; ++j) mem[j] = {j};
  // adjacency of live clusters: (neighbour node id, complete-linkage distance), ascending id
  std::vector<std::vector<std::pair<int32_t, double>>> adj(p);
  for (const Edge& e : edges) {
    double d = 1.0 - e.absr;  // core/cpp/v3_blocks.h:55
    if (!ok(d) || e.j == e.l) continue;
    adj[e.j].push_back({e.l, d}); adj[e.l].push_back({e.j, d});
  }
  for (auto& a : adj) std::sort(a.begin(), a.end(), [](const auto& x, const auto& y) { return x.first < y.first; });
  struct Key { double d; int32_t a, b; };
  auto cmp = [&](const Key& x, const Key& y) {
    if (x.d != y.d) return x.d < y.d;
    return union_lex_less(mem[x.a], mem[x.b], mem[y.a], mem[y.b]);
  };
  std::set<Key, decltype(cmp)> Q(cmp);
  for (int j = 0; j < p; ++j) for (auto& [l, d] : adj[j]) if (j < l) Q.insert(Key{d, j, l});
  std::vector<std::pair<int32_t, double>> nc;
  while (!Q.empty()) {
    Key k = *Q.begin();
    const int a = k.a, b = k.b;
    for (auto& [x, d] : adj[a]) Q.erase(Key{d, std::min(a, x), std::max(a, x)});
    for (auto& [x, d] : adj[b]) if (x != a) Q.erase(Key{d, std::min(b, x), std::max(b, x)});
    // neighbours of the merged cluster: intersection by id (both lists ascending)
    nc.clear();
    {
      const auto &A = adj[a], &Bv = adj[b];
      size_t i = 0, j = 0;
      while (i < A.size() && j < Bv.size()) {
        if (A[i].first < Bv[j].first) ++i;
        else if (Bv[j].first < A[i].first) ++j;
        else { int x = A[i].first; if (x != a && x != b) nc.push_back({x, std::max(A[i].second, Bv[j].second)}); ++i; ++j; }
      }
    }
    const int nn = forest_merge(T, a, b, k.d);
    adj.emplace_back(); mem.emplace_back();
    // remove a and b from every neighbour list; append nn (the largest id: lists stay ascending)
    auto drop = [&](int x) {
      auto& L = adj[x];
      L.erase(std::remove_if(L.begin(), L.end(), [&](const auto& e) { return e.first == a || e.first == b; }), L.end());
    };
    for (auto& [x, d] : adj[a]) if (x != b) drop(x);
    for (auto& [x, d] : adj[b]) if (x != a) drop(x);
    for (auto& [x, d] : nc) adj[x].push_back({nn, d});
    adj[nn] = nc;
    std::vector<int32_t> u; u.reserve(mem[a].size() + mem[b].size());
    std::merge(mem[a].begin(), mem[a].end(), mem[b].begin(), mem[b].end(), std::back_inserter(u));
    mem[nn].swap(u);
    std::vector<int32_t>().swap(mem[a]); std::vector<int32_t>().swap(mem[b]);
    std::vector<std::pair<int32_t, double>>().swap(adj[a]); std::vector<std::pair<int32_t, double>>().swap(adj[b]);
    for (auto& [x, d] : nc) Q.insert(Key{d, std::min(nn, x), std::max(nn, x)});
  }
  // roots: nodes that are nobody's child, ascending id
  std::vector<char> child(T.left.size(), 0);
  for (size_t x = p; x < T.left.size(); ++x) { child[T.left[x]] = 1; child[T.right[x]] = 1; }
  for (size_t x = 0; x < T.left.size(); ++x) if (!child[x]) T.roots.push_back((int32_t)x);
  return T;
}

// ---------------------------------------------------------------- cut and packing
// core/cpp/v3_blocks.h:121-144: from each root, a node with more than B members is split into its children (left
// first) until every retained cluster has <= B members; next-fit packing of whole clusters into blocks of <= B members;
// members sorted within each block. LeafOrder (exact, one root) = the v3 order; MinIndex (truncated) = clusters
// ordered by their minimum member index (D-4 / THEORY-1 item 4).
Partition cut_and_pack(const Forest& T, int B, PackOrder order) {
  const int p = T.p;
  if (order == PackOrder::LeafOrder && T.roots.size() != 1) throw Error(Status::internal_error, "cut_and_pack: leaf order needs one root");
  std::vector<int32_t> pieces;  // retained cluster nodes
  for (int32_t r : T.roots) {
    std::vector<int32_t> st{r};
    while (!st.empty()) {
      int x = st.back(); st.pop_back();
      if (T.size[x] <= B) { pieces.push_back(x); continue; }
      st.push_back(T.right[x]); st.push_back(T.left[x]);
    }
  }
  if (order == PackOrder::MinIndex)
    std::sort(pieces.begin(), pieces.end(), [&](int32_t a, int32_t b) { return T.minidx[a] < T.minidx[b]; });
  Partition P; P.B = B;
  std::vector<int32_t> cur, leaves;
  auto flush = [&]() { std::sort(cur.begin(), cur.end()); P.members.insert(P.members.end(), cur.begin(), cur.end()); P.bptr.push_back((int64_t)P.members.size()); cur.clear(); };
  for (int32_t x : pieces) {
    leaves.clear(); subtree_leaves(T, x, leaves);
    if (cur.size() + leaves.size() > (size_t)B) flush();
    cur.insert(cur.end(), leaves.begin(), leaves.end());
  }
  if (!cur.empty()) flush();
  P.J = (int32_t)P.bptr.size() - 1;
  P.blk.assign(p, -1); P.pos.assign(p, -1);
  for (int b = 0; b < P.J; ++b) for (int i = 0; i < P.size(b); ++i) { P.blk[P.block(b)[i]] = b; P.pos[P.block(b)[i]] = i; }
  for (int j = 0; j < p; ++j) if (P.blk[j] < 0) throw Error(Status::internal_error, "cut_and_pack: blocks do not cover every column");
  return P;
}

int block_cap(const PartitionOptions& o) { return o.mode == PartMode::Exact ? o.B : std::min(o.B, o.bv_cap); }

Partition make_partition(const Data& D, const CorrResult& C, const PartitionOptions& o, Forest* out) {
  if (o.B < 1 || o.B > 16) throw Error(Status::invalid_input, "partition: B outside 1..16 (core/cpp/v3_core.cpp:180)");
  if (o.bv_cap < 1 || o.bv_cap > 16) throw Error(Status::invalid_input, "partition: bv_cap outside 1..16");
  Forest T;
  Partition P;
  if (o.mode == PartMode::Exact) {
    T = complete_linkage_exact(D, o.threads);
    P = cut_and_pack(T, o.B, PackOrder::LeafOrder);
  } else {
    double tau = o.tau < 0 ? C.rn : o.tau;
    if (tau != C.tau) throw Error(Status::internal_error, "partition: tau differs from the correlation pass's tau");
    T = complete_linkage_truncated(D.p, C.edges, 1.0 - tau, o.strict);
    P = cut_and_pack(T, block_cap(o), o.pack);   // D-19: blocks of at most min(B, bv_cap) members
  }
  if (out) *out = std::move(T);
  return P;
}

}  // namespace v4::setup
