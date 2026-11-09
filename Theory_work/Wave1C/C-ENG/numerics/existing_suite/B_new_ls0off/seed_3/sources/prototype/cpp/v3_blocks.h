// v3_blocks.h -- blocks (complete linkage, top-down cut, next-fit packing) and neighbour graph.
// CORE_SPEC v2 §3 with ruling R13; M §6.3 (clustering, cut, packing) and M §6.4 (neighbour graph).
#pragma once
#include "v3_score.h"

namespace v3 {

// Correlation r_jl = G_jl / sqrt(G_jj G_ll) from the Gram matrix of the standardised columns (equal to cor(X)
// up to rounding; the explicit normalisation removes the rounding of ||x_j||^2 = n-1).
inline std::vector<double> correlation_matrix(const Data& D) {
  int p = D.p;
  std::vector<double> r((size_t)p * p);
  std::vector<double> s(p);
  for (int j = 0; j < p; ++j) s[j] = std::sqrt(D.Gat(j, j));
  for (int a = 0; a < p; ++a) for (int b = 0; b < p; ++b) r[(size_t)b * p + a] = D.Gat(a, b) / (s[a] * s[b]);
  return r;
}

// Lexicographic comparison of the sorted unions (a u b) vs (c u d) without materialising them (R13 tie rule).
inline bool union_lex_less(const std::vector<int>& a, const std::vector<int>& b, const std::vector<int>& c, const std::vector<int>& d) {
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

struct Dendrogram {
  // node ids: 0..p-1 leaves (internal index j), p..2p-2 internal nodes in merge order
  std::vector<int> left, right, size, minidx;
  std::vector<double> height;
  int root = -1;
};

// Complete linkage on d_jl = 1 - |r_jl| (M §6.3), implemented explicitly with R13:
// (1) the merge taken at each step is the pair of current clusters with the smallest complete-linkage distance;
//     among exactly equal distances, the pair whose union has the lexicographically smallest sorted index list;
// (2) at every internal node the left child is the child containing the smaller minimum index.
// Distances between clusters are updated by the Lance-Williams rule for complete linkage, d(a u b, x) =
// max(d(a,x), d(b,x)), which is exact in floating point (max involves no rounding).
// Each active cluster keeps its best partner under the order (distance, union-lex); O(p^2) typical work.
inline Dendrogram complete_linkage(const Data& D) {
  int p = D.p;
  Dendrogram T;
  T.left.assign(2 * p - 1, -1); T.right.assign(2 * p - 1, -1); T.size.assign(2 * p - 1, 1); T.minidx.assign(2 * p - 1, 0);
  T.height.assign(2 * p - 1, 0.0);
  for (int j = 0; j < p; ++j) T.minidx[j] = j;
  if (p == 1) { T.root = 0; return T; }
  std::vector<double> r = correlation_matrix(D);
  std::vector<double> dist((size_t)p * p);
  for (size_t i = 0; i < dist.size(); ++i) dist[i] = 1.0 - std::fabs(r[i]);
  std::vector<std::vector<int>> mem(p);
  std::vector<int> node(p);
  std::vector<char> active(p, 1);
  for (int j = 0; j < p; ++j) { mem[j] = {j}; node[j] = j; }
  std::vector<int> best(p, -1);
  std::vector<double> bestd(p, POS_INF);
  auto pair_less = [&](int i, int j, int c, int d2) {  // is pair (i,j) before pair (c,d2)?
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
  int next_node = p;
  for (int step = 0; step < p - 1; ++step) {
    int bi = -1;
    for (int i = 0; i < p; ++i) {
      if (!active[i] || best[i] < 0) continue;
      if (bi < 0 || pair_less(i, best[i], bi, best[bi])) bi = i;
    }
    int a = bi, b = best[bi];
    double h = dist[(size_t)b * p + a];
    // new node; left child = child with smaller minimum index (R13)
    int na = node[a], nb = node[b];
    int L = (T.minidx[na] < T.minidx[nb]) ? na : nb, R = (L == na) ? nb : na;
    int nn = next_node++;
    T.left[nn] = L; T.right[nn] = R; T.size[nn] = T.size[na] + T.size[nb];
    T.minidx[nn] = std::min(T.minidx[na], T.minidx[nb]); T.height[nn] = h;
    // merge b into slot a
    std::vector<int> u; u.reserve(mem[a].size() + mem[b].size());
    std::merge(mem[a].begin(), mem[a].end(), mem[b].begin(), mem[b].end(), std::back_inserter(u));
    mem[a].swap(u); mem[b].clear(); active[b] = 0; node[a] = nn;
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
  T.root = next_node - 1;
  return T;
}

// Leaves of a subtree in left-to-right order (iterative; left child first).
inline std::vector<int> subtree_leaves(const Dendrogram& T, int nd, int p) {
  std::vector<int> out, st{nd};
  while (!st.empty()) {
    int x = st.back(); st.pop_back();
    if (x < p) { out.push_back(x); continue; }
    st.push_back(T.right[x]); st.push_back(T.left[x]);
  }
  return out;
}

// Top-down cut (M §6.3): from the root, any node with more than B members is split into its two children
// (left child first) until every retained cluster has at most B members. Then next-fit packing in leaf order,
// whole clusters only, into blocks of at most B members; members sorted within each block.
inline std::vector<std::vector<int>> make_blocks(const Data& D, int B, Dendrogram* out_tree = nullptr) {
  int p = D.p;
  Dendrogram T = complete_linkage(D);
  std::vector<std::vector<int>> clusters;
  std::vector<int> st{T.root};
  while (!st.empty()) {
    int x = st.back(); st.pop_back();
    if (T.size[x] <= B) { clusters.push_back(subtree_leaves(T, x, p)); continue; }
    st.push_back(T.right[x]); st.push_back(T.left[x]);
  }
  std::vector<std::vector<int>> blocks;
  std::vector<int> cur;
  for (auto& c : clusters) {
    if (cur.size() + c.size() > (size_t)B) { blocks.push_back(cur); cur.clear(); }
    cur.insert(cur.end(), c.begin(), c.end());
  }
  if (!cur.empty()) blocks.push_back(cur);
  for (auto& b : blocks) std::sort(b.begin(), b.end());
  if (out_tree) *out_tree = T;
  return blocks;
}

// Neighbour graph (M §6.4): r_n = sqrt(2 log p / n). For each j, candidates l != j ordered by |r_jl| descending
// (ties by smaller index); keep those with |r_jl| > r_n, always at least the first (largest) one, at most B.
// N(j) = symmetric union. No edges when p = 1.
inline std::vector<std::vector<int>> neighbour_graph(const Data& D, int B) {
  int p = D.p;
  std::vector<std::vector<int>> N(p);
  if (p == 1) return N;
  std::vector<double> r = correlation_matrix(D);
  double rn = std::sqrt(2.0 * std::log((double)p) / D.n);
  std::vector<std::vector<int>> chosen(p);
  std::vector<int> cand(p - 1);
  for (int j = 0; j < p; ++j) {
    int c = 0;
    for (int l = 0; l < p; ++l) if (l != j) cand[c++] = l;
    std::stable_sort(cand.begin(), cand.end(), [&](int a, int b) {
      double ra = std::fabs(r[(size_t)a * p + j]), rb = std::fabs(r[(size_t)b * p + j]);
      if (ra != rb) return ra > rb;
      return a < b;
    });
    int above = 0;
    for (int l : cand) { if (std::fabs(r[(size_t)l * p + j]) > rn) ++above; else break; }
    int keep = std::min(B, std::max(1, above));
    chosen[j].assign(cand.begin(), cand.begin() + keep);
  }
  for (int j = 0; j < p; ++j) for (int l : chosen[j]) { N[j].push_back(l); N[l].push_back(j); }
  for (int j = 0; j < p; ++j) { std::sort(N[j].begin(), N[j].end()); N[j].erase(std::unique(N[j].begin(), N[j].end()), N[j].end()); }
  return N;
}

}  // namespace v3
