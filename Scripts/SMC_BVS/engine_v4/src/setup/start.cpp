// start.cpp -- composite sum, the exact pi_0 sampler, and the start mode argmax pi_0 (core/cpp/v3_start.h:52-305),
// with an iterative enumeration (no recursion of depth J; REVIEW_fable R6) and an incremental tie-aware DP.
#include <algorithm>
#include "v4/setup.h"

namespace v4::setup {

// core/cpp/v3_start.h:54-66: sum over the blocks met by S in increasing block order.
double Start::comp(ModelView S) const {
  thread_local std::vector<std::pair<int, int>> scratch;
  scratch.clear();
  for (uint32_t i = 0; i < S.k; ++i) scratch.push_back({P->blk[S.idx[i]], P->pos[S.idx[i]]});
  std::sort(scratch.begin(), scratch.end());
  double s = 0;
  size_t i = 0;
  while (i < scratch.size()) {
    int b = scratch[i].first; uint32_t code = 0;
    while (i < scratch.size() && scratch[i].first == b) { code |= (1u << scratch[i].second); ++i; }
    s += T->logr[T->code_ptr[b] + code];
  }
  return s;
}

// core/cpp/v3_start.h:18-20
static inline int cat_draw_gt(const double* b, const double* e, double u) { return (int)(std::upper_bound(b, e, u) - b); }

// core/cpp/v3_start.h:158-176. Variate order: the total size; block sizes for b = J..1 while r > 0; sub-models for
// b = 1..J with k_b > 0. Slots (INTERFACES v0.1.5 §3): PI0_SIZE 0; PI0_BLOCKSIZE b; PI0_SUBMODEL b. A compat
// source ignores the address and returns the serial stream in this same order.
void Start::draw_pi0(UniformSource& us, Address a, Model& S) const {
  const int K = T->K;
  auto U = [&](SlotKind kind, uint32_t index) { Address x = a; x.slot = slot_of(kind, index); return us.u(x); };
  int k = cat_draw_gt(T->size_cum.data(), T->size_cum.data() + K + 1, U(SK_PI0_SIZE, 0));
  thread_local std::vector<std::pair<int, int>> kb;  // (block, size) with size > 0, in decreasing block order
  kb.clear();
  int r = k;
  for (int b = T->J - 1; b >= 0 && r > 0; --b) {
    size_t row = (size_t)b * (K + 1) + r;
    const double* c = &T->cond_cum[T->cond_ptr[row]];
    int j = cat_draw_gt(c, &T->cond_cum[0] + T->cond_ptr[row + 1], U(SK_PI0_BLOCKSIZE, (uint32_t)b));
    if (j > 0) kb.push_back({b, j});
    r -= j;
  }
  S.clear();
  thread_local std::vector<double> sc;
  const bool stored = !T->sub_cum.empty();  // tests only; production setup.bin has no sampler tables (D-18)
  for (auto it = kb.rbegin(); it != kb.rend(); ++it) {
    int b = it->first, j = it->second;
    int64_t row = T->logprof_ptr[b] + j;
    uint32_t code;
    if (stored) {
      const double* c = &T->sub_cum[T->sub_ptr[row]];
      int i = cat_draw_gt(c, &T->sub_cum[0] + T->sub_ptr[row + 1], U(SK_PI0_SUBMODEL, (uint32_t)b));
      code = T->codes_by_size[T->cbs_ptr[row] + i];
    } else {  // D-18: the within-size law of this block and size, recomputed from logr (same bits as the stored arrays)
      sub_cum_of(*T, b, P->size(b), j, sc);
      int i = cat_draw_gt(sc.data(), sc.data() + sc.size(), U(SK_PI0_SUBMODEL, (uint32_t)b));
      uint32_t n; code = codes_of_size(P->size(b), j, &n)[i];
    }
    for (int t = 0; t < P->size(b); ++t) if (code & (1u << t)) S.push_back(P->block(b)[t]);
  }
  std::sort(S.begin(), S.end());
}

// ---------------------------------------------------------------- start mode
namespace {
// core/cpp/v3_start.h:189-226 in flat arrays: mb at the logprof row layout; arg as CSR over the same rows; M (J+1)x(K+1).
struct ModeDP {
  int J = 0, K = 0;
  const Tables* T = nullptr;
  std::vector<double> mb;
  std::vector<int64_t> arg_ptr; std::vector<uint32_t> arg;
  std::vector<double> M;
  int kbest = -1; double vbest = NEG_INF;
  int nj(int b) const { return (int)(T->logprof_ptr[b + 1] - T->logprof_ptr[b]); }        // block b (0-based)
  double mbv(int b, int j) const { return mb[T->logprof_ptr[b] + j]; }
  double Mv(int b, int k) const { return M[(size_t)b * (K + 1) + k]; }
  const uint32_t* arg_b(int b, int j) const { return &arg[arg_ptr[T->logprof_ptr[b] + j]]; }
  const uint32_t* arg_e(int b, int j) const { return &arg[0] + arg_ptr[T->logprof_ptr[b] + j + 1]; }
  // core/cpp/v3_start.h:229-233: level b (1-based) takes size j from remaining r
  bool tight(int b, int r, int j) const {
    if (j >= nj(b - 1) || j > r || Mv(b - 1, r - j) == NEG_INF) return false;
    double v = (j == 0) ? Mv(b - 1, r - j) : Mv(b - 1, r - j) + mbv(b - 1, j);
    return v == Mv(b, r);
  }
};
ModeDP mode_dp(const Data& D, const Tables& T) {
  ModeDP dp; dp.J = T.J; dp.K = D.K; dp.T = &T;
  auto P_size = [&](int b) { return __builtin_ctzll((unsigned long long)(T.code_ptr[b + 1] - T.code_ptr[b])); };  // 2^m codes
  const int J = T.J, K = D.K;
  const int64_t NR = T.logprof_ptr[J];
  dp.mb.assign(NR, NEG_INF);
  dp.arg_ptr.assign(NR + 1, 0);
  std::vector<std::vector<uint32_t>> tmp(NR);
  for (int b = 0; b < J; ++b) {
    const double* lr = &T.logr[T.code_ptr[b]];
    for (int j = 0; j < dp.nj(b); ++j) {
      int64_t row = T.logprof_ptr[b] + j;
      uint32_t nc; const uint32_t* cs = codes_of_size(P_size(b), j, &nc);  // increasing code order (D-18)
      for (uint32_t q = 0; q < nc; ++q) {  // core/cpp/v3_start.h:204-209
        uint32_t c = cs[q]; double v = lr[c];
        if (v > dp.mb[row]) { dp.mb[row] = v; tmp[row].assign(1, c); }
        else if (v == dp.mb[row]) tmp[row].push_back(c);
      }
    }
  }
  for (int64_t r = 0; r < NR; ++r) dp.arg_ptr[r + 1] = dp.arg_ptr[r] + (int64_t)tmp[r].size();
  dp.arg.reserve(dp.arg_ptr[NR]);
  for (auto& v : tmp) dp.arg.insert(dp.arg.end(), v.begin(), v.end());
  dp.M.assign((size_t)(J + 1) * (K + 1), NEG_INF);
  dp.M[0] = 0.0;
  for (int b = 1; b <= J; ++b)  // core/cpp/v3_start.h:213-219
    for (int k = 0; k <= K; ++k) {
      double& Mbk = dp.M[(size_t)b * (K + 1) + k];
      for (int j = 0; j < dp.nj(b - 1) && j <= k; ++j) {
        double Mp = dp.Mv(b - 1, k - j);
        if (Mp == NEG_INF) continue;
        double v = (j == 0) ? Mp : Mp + dp.mbv(b - 1, j);
        if (v > Mbk) Mbk = v;
      }
    }
  for (int k = 0; k <= K; ++k) {  // core/cpp/v3_start.h:220-224
    if (dp.Mv(J, k) == NEG_INF) continue;
    double v = D.logprior[k] + dp.Mv(J, k);
    if (v > dp.vbest) { dp.vbest = v; dp.kbest = k; }
  }
  return dp;
}

// The v3 enumeration (core/cpp/v3_start.h:278-301) with an explicit stack: frames for levels b = J..1, each iterating
// the sizes j in increasing order and, for a tight j, the codes of arg[b-1][j] in increasing order; a leaf at b = 0.
// The visiting order, the count, the truncation point and the kept lex-min set are those of the recursion. Leaves
// build S from the non-empty block choices only (O(K log K) instead of O(p)).
void enumerate(const Partition& P, const ModeDP& dp, long cap, ModeResult& res) {
  const int J = dp.J;
  struct Fr { int b, r, j; const uint32_t* c; const uint32_t* ce; bool pushed; };
  std::vector<Fr> st; st.reserve(J + 1);
  std::vector<std::pair<int, uint32_t>> nz;  // non-empty choices on the current path
  Model S, best; bool have = false; long count = 0; bool trunc = false;
  st.push_back(Fr{J, dp.kbest, -1, nullptr, nullptr, false});
  while (!st.empty() && !trunc) {
    Fr& f = st.back();
    if (f.b == 0) {  // leaf (r == 0 here: M[0][r] = -inf for r != 0, so no tight edge leads elsewhere)
      if (f.r == 0) {
        S.clear();
        for (auto& [b, code] : nz) for (int t = 0; t < P.size(b); ++t) if (code & (1u << t)) S.push_back(P.block(b)[t]);
        std::sort(S.begin(), S.end());
        ++count;
        if (!have || lex_less(S, best)) { best = S; have = true; }
        if (count >= cap) trunc = true;
      }
      st.pop_back();
      continue;
    }
    if (f.pushed) { nz.pop_back(); f.pushed = false; }
    if (f.c != nullptr && f.c < f.ce) {  // next code of the current tight j
      uint32_t code = *f.c++;
      if (code != 0) { nz.push_back({f.b - 1, code}); f.pushed = true; }
      int b = f.b, r = f.r - f.j;
      st.push_back(Fr{b - 1, r, -1, nullptr, nullptr, false});
      continue;
    }
    // advance to the next tight j
    bool found = false;
    while (++f.j < dp.nj(f.b - 1) && f.j <= f.r) {
      if (dp.Mv(f.b - 1, f.r - f.j) == NEG_INF) continue;
      double v = (f.j == 0) ? dp.Mv(f.b - 1, f.r - f.j) : dp.Mv(f.b - 1, f.r - f.j) + dp.mbv(f.b - 1, f.j);
      if (v != dp.Mv(f.b, f.r)) continue;
      f.c = dp.arg_b(f.b - 1, f.j); f.ce = dp.arg_e(f.b - 1, f.j); found = true; break;
    }
    if (!found) st.pop_back();
  }
  res.S = best; res.ties = count; res.truncated = trunc;
}

// |E| = number of leaves of the enumeration, by DP over (level, remaining size), saturating at cap.
long count_leaves(const ModeDP& dp, long cap) {
  const int J = dp.J, K = dp.K;
  std::vector<long> prev(K + 1, 0), cur(K + 1, 0);
  prev[0] = 1;
  for (int b = 1; b <= J; ++b) {
    for (int r = 0; r <= K; ++r) {
      long s = 0;
      for (int j = 0; j < dp.nj(b - 1) && j <= r; ++j) {
        if (!dp.tight(b, r, j) || prev[r - j] == 0) continue;
        long na = (long)(dp.arg_e(b - 1, j) - dp.arg_b(b - 1, j));
        __int128 add = (__int128)na * prev[r - j];
        s = (long)std::min<__int128>((__int128)s + add, (__int128)cap);
      }
      cur[r] = s;
    }
    std::swap(prev, cur);
  }
  return prev[dp.kbest];
}

// core/cpp/v3_start.h:234-270 (TDP-E): lex-min of E. Index by index, include i iff some set of E contains IN u {i}
// and avoids OUT. Same decisions as v3; the feasibility test is incremental: fwd[b][r] (reach (b, r) from (0, 0)) and
// bwd[b][r] (reach (J, kbest) from (b, r)) over tight edges with an allowed size, kept valid for levels <= F and >= Bk;
// a test at block bb uses fwd[bb] and bwd[bb + 1], which do not depend on block bb. A tentative change that leaves
// block bb's allowed sizes unchanged keeps the (feasible) state feasible; one that allows no size is infeasible.
Model tie_dp(const Data& D, const Partition& P, const ModeDP& dp) {
  const int J = dp.J, K = dp.K, p = D.p;
  std::vector<uint32_t> inm(J, 0), outm(J, 0);
  std::vector<int64_t> aptr(J + 1, 0);
  for (int b = 0; b < J; ++b) aptr[b + 1] = aptr[b] + dp.nj(b);
  std::vector<char> allowed(aptr[J], 0);
  auto compute = [&](int b, uint32_t in, uint32_t out, char* a) {
    for (int j = 0; j < dp.nj(b); ++j) {
      a[j] = 0;
      for (const uint32_t* c = dp.arg_b(b, j); c != dp.arg_e(b, j); ++c) if ((*c & in) == in && (*c & out) == 0) { a[j] = 1; break; }
    }
  };
  for (int b = 0; b < J; ++b) compute(b, 0, 0, &allowed[aptr[b]]);
  const size_t W = K + 1;
  std::vector<char> fwd((size_t)(J + 1) * W, 0), bwd((size_t)(J + 1) * W, 0);
  int F = 0, Bk = J;
  for (int r = 0; r <= K; ++r) { fwd[r] = (r == 0); bwd[(size_t)J * W + r] = (r == dp.kbest); }
  auto fwd_level = [&](int b) {  // fwd[b] from fwd[b-1] (core/cpp/v3_start.h:251-256)
    const char* a = &allowed[aptr[b - 1]];
    for (int r = 0; r <= K; ++r) {
      char ok = 0;
      for (int j = 0; j < dp.nj(b - 1) && j <= r && !ok; ++j)
        if (a[j] && fwd[(size_t)(b - 1) * W + r - j] && dp.tight(b, r, j)) ok = 1;
      fwd[(size_t)b * W + r] = ok;
    }
  };
  auto bwd_level = [&](int b) {  // bwd[b-1] from bwd[b]
    const char* a = &allowed[aptr[b - 1]];
    for (int r = 0; r <= K; ++r) {
      char ok = 0;
      for (int j = 0; j < dp.nj(b - 1) && r + j <= K && !ok; ++j)
        if (a[j] && bwd[(size_t)b * W + r + j] && dp.tight(b, r + j, j)) ok = 1;
      bwd[(size_t)(b - 1) * W + r] = ok;
    }
  };
  auto test = [&](int bb, const char* a) {  // feasibility with block bb's allowed sizes replaced by a
    while (F < bb) fwd_level(++F);
    while (Bk > bb + 1) bwd_level(Bk--);
    for (int r = 0; r <= K; ++r) {
      if (!bwd[(size_t)(bb + 1) * W + r]) continue;
      for (int j = 0; j < dp.nj(bb) && j <= r; ++j)
        if (a[j] && fwd[(size_t)bb * W + r - j] && dp.tight(bb + 1, r, j)) return true;
    }
    return false;
  };
  auto invalidate = [&](int bb) { F = std::min(F, bb); Bk = std::max(Bk, bb + 1); };
  // root check (core/cpp/v3_start.h:261): the full forward pass
  {
    bool ok = dp.kbest >= 0;
    if (ok) { while (F < J) fwd_level(++F); ok = fwd[(size_t)J * W + dp.kbest] != 0; }
    if (!ok) throw Error(Status::internal_error, "start_mode tie DP: no tight path from (J, kbest) (invalid tables)");
  }
  Model S;
  std::vector<char> a2(17);
  for (int i = 0; i < p; ++i) {
    const int b = P.blk[i]; const uint32_t bit = 1u << P.pos[i];
    char* cur = &allowed[aptr[b]];
    const int nb = dp.nj(b);
    compute(b, inm[b] | bit, outm[b], a2.data());
    bool same = std::equal(a2.begin(), a2.begin() + nb, cur), any = false;
    for (int j = 0; j < nb; ++j) any |= a2[j] != 0;
    bool feas = same ? true : (any ? test(b, a2.data()) : false);
    if (feas) {
      inm[b] |= bit; S.push_back(i);
      if (!same) { std::copy(a2.begin(), a2.begin() + nb, cur); invalidate(b); }
      continue;
    }
    outm[b] |= bit;
    compute(b, inm[b], outm[b], a2.data());
    if (!std::equal(a2.begin(), a2.begin() + nb, cur)) { std::copy(a2.begin(), a2.begin() + nb, cur); invalidate(b); }
  }
  return S;
}
}  // namespace

// core/cpp/v3_start.h:271-305.
ModeResult start_mode(const Data& D, const Partition& P, const Tables& T, long cap, bool tie, ModeAlgo algo) {
  if (tie && cap < 2) throw Error(Status::invalid_input, "start_mode: the e4 tie-aware fallback requires cap >= 2 (C-PACK MR2)");
  ModeDP dp = mode_dp(D, T);
  ModeResult res; res.lg0 = dp.vbest;
  if (dp.kbest < 0) throw Error(Status::internal_error, "start_mode: no feasible size (invalid tables)");
  if (algo == ModeAlgo::Auto) {
    long total = count_leaves(dp, cap);
    // the enumeration costs about (leaves x levels); the tie DP about p tests. Results are identical (TDP_E lemma;
    // gate: tests/test_setup.cpp start-mode cases), so the choice is cost-only.
    bool need_enum = (total >= cap && !tie);
    algo = (need_enum || (double)std::min(total, cap) * (double)(T.J + 1) <= 5e7) ? ModeAlgo::Enumerate : ModeAlgo::CountThenTieDP;
  }
  if (algo == ModeAlgo::Enumerate) {
    enumerate(P, dp, cap, res);
    if (res.truncated && tie) { res.S = tie_dp(D, P, dp); res.tie_dp_used = true; }
    return res;
  }
  long total = count_leaves(dp, cap);
  res.ties = std::min(total, cap);
  res.truncated = total >= cap;
  if (res.truncated && !tie) throw Error(Status::internal_error, "start_mode: truncated enumeration without tie DP needs ModeAlgo::Enumerate");
  res.S = tie_dp(D, P, dp);
  res.tie_dp_used = res.truncated;
  return res;
}

}  // namespace v4::setup
