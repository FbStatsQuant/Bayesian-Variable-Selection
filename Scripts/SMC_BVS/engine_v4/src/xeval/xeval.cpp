// xeval.cpp -- see xeval.h. Copies (not edits) the predictive-density helpers of src/eval/dist.cpp.
#include "xeval/xeval.h"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <numeric>

#include "eval/io.h"
#include "v4/format.h"
#include "v4/post.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/sha256.h"

namespace v4::xeval {
using namespace v4::eval;

namespace {

// ---- COPY of dist.cpp (predictive densities): one component at one x, the hoisted log-density constants ----
struct CompAt { double loc, scale2, lc, hnu, inv; bool gauss; double w; };
double t_const(double nu) {
  thread_local double last_nu = -1, last_c = 0;
  if (nu != last_nu) { last_nu = nu; last_c = std::lgamma(0.5 * (nu + 1)) - std::lgamma(0.5 * nu) - 0.5 * std::log(nu * M_PI); }
  return last_c;
}
void comp_at(const Component& C, const XSample& xs, size_t row, double w, CompAt& o) {
  const size_t K = xs.cols.size();
  const double* x = &xs.X[row * K];
  const size_t k = C.orig.size();
  o.w = w;
  if (C.gaussian) {
    double s = C.a;
    for (size_t i = 0; i < k; ++i) { int p = xs.pos(C.orig[i]); if (p < 0) throw Error(Status::internal_error, "comp_at: column missing"); s += x[p] * C.b[i]; }
    o.loc = s; o.scale2 = C.sigma2; o.gauss = true;
    o.lc = -0.5 * std::log(2.0 * M_PI * C.sigma2); o.inv = 0.5 / C.sigma2; o.hnu = 0;
    return;
  }
  double xt[64], wv[64];
  std::vector<double> xtv, wvv;
  double* xtp = xt; double* wp = wv;
  if (k > 64) { xtv.resize(k); wvv.resize(k); xtp = xtv.data(); wp = wvv.data(); }
  double lin = 0;
  for (size_t i = 0; i < k; ++i) {
    int p = xs.pos(C.orig[i]); if (p < 0) throw Error(Status::internal_error, "comp_at: column missing");
    xtp[i] = (x[p] - C.xbar[i]) / C.xsd[i];
    lin += C.theta_bar[i] * xtp[i];
  }
  double q = 0;
  for (size_t i = 0; i < k; ++i) { double s = xtp[i]; for (size_t t = 0; t < i; ++t) s -= C.LH[i * k + t] * wp[t]; wp[i] = s / C.LH[i * k + i]; q += wp[i] * wp[i]; }
  const double nu = 2.0 * C.alpha_n;
  o.loc = C.ybar + C.sy * lin;
  o.scale2 = C.sy * C.sy * (C.beta_n / C.alpha_n) * (1.0 + C.n * q);
  o.gauss = false;
  o.lc = t_const(nu) - 0.5 * std::log(o.scale2);
  o.hnu = 0.5 * (nu + 1); o.inv = 1.0 / (nu * o.scale2);
}
inline double log_comp(const CompAt& c, double y) {
  const double r = y - c.loc;
  return c.gauss ? c.lc - r * r * c.inv : c.lc - c.hnu * std::log1p(r * r * c.inv);
}
double comp_var(const CompAt& c) { return c.gauss ? c.scale2 : c.scale2 * (2 * c.hnu - 1) / (2 * c.hnu - 3); }

// ---- COPY of dist.cpp MixAt: density estimate at y from the exact part + tail groups ----
struct MixAt {
  std::vector<CompAt> ex;
  std::vector<std::vector<CompAt>> tail;
  double tau = 0;
  void eval(double y, double* out) const {   // out: G + 2 log densities: [0] pooled, [1..G] per group, [G+1] top-K only
    const size_t G = tail.size();
    double m = -INFINITY;
    thread_local std::vector<double> le, lt;
    le.resize(ex.size());
    for (size_t i = 0; i < ex.size(); ++i) { le[i] = log_comp(ex[i], y); m = std::max(m, le[i]); }
    size_t nt = 0; for (auto& g : tail) nt += g.size();
    lt.resize(nt);
    size_t q = 0;
    for (auto& g : tail) for (auto& c : g) { lt[q] = log_comp(c, y); m = std::max(m, lt[q]); ++q; }
    double se = 0; for (size_t i = 0; i < ex.size(); ++i) se += ex[i].w * std::exp(le[i] - m);
    double pooled_tail = 0; q = 0;
    for (size_t g = 0; g < G; ++g) {
      double sg = 0; for (size_t i = 0; i < tail[g].size(); ++i, ++q) sg += std::exp(lt[q] - m);
      sg /= (double)tail[g].size();
      out[1 + g] = m + std::log(se + tau * sg);
      pooled_tail += sg / G;
    }
    out[0] = m + std::log(se + tau * pooled_tail);
    out[G + 1] = m + std::log(se / (1.0 - tau));
  }
  void moments(double& m1, double& var) const {
    double s1 = 0, s2 = 0, wsum = 0;
    for (auto& c : ex) { s1 += c.w * c.loc; s2 += c.w * (comp_var(c) + c.loc * c.loc); wsum += c.w; }
    for (auto& g : tail) for (auto& c : g) { const double w = tau / (g.size() * tail.size()); s1 += w * c.loc; s2 += w * (comp_var(c) + c.loc * c.loc); wsum += w; }
    m1 = s1 / wsum; var = std::max(s2 / wsum - m1 * m1, 1e-300);
  }
};

// ---- COPY of dist.cpp Split / make_split / tail_sample ----
struct Split {
  std::vector<int> top, tail;
  std::vector<double> tail_cum;
  double tau = 0;
  bool exact = false;
  int G = 0, Rg = 0;
};
Split make_split(const Law& L, const CrossOpts& o) {
  Split s;
  const size_t M = L.comps.size();
  std::vector<int> ord(M); std::iota(ord.begin(), ord.end(), 0);
  const size_t K = std::min<size_t>(M, (size_t)std::max(1, o.top_k));
  std::partial_sort(ord.begin(), ord.begin() + K, ord.end(), [&](int a, int b) {
    return L.comps[a].w > L.comps[b].w || (L.comps[a].w == L.comps[b].w && a < b); });
  if (M - K <= (size_t)o.tail_r) { s.top = ord; s.exact = true; return s; }
  s.top.assign(ord.begin(), ord.begin() + K);
  s.tail.assign(ord.begin() + K, ord.end());
  std::sort(s.tail.begin(), s.tail.end());
  s.tail_cum.resize(s.tail.size());
  long double c = 0; for (size_t i = 0; i < s.tail.size(); ++i) { c += L.comps[s.tail[i]].w; s.tail_cum[i] = (double)c; }
  s.tau = (double)c;
  s.G = std::max(2, o.tail_groups); s.Rg = std::max(1, o.tail_r / s.G);
  return s;
}
std::vector<int> tail_sample(const Split& s, uint32_t seed, uint32_t oid, uint32_t stream, uint32_t block, int g) {
  Address a; a.seed = seed; a.role = R_POST; a.xph = X_POST; a.stage = 1000 + oid * 4 + stream; a.particle = block; a.position = (uint32_t)g;
  const double u0 = uniform_at(a);
  std::vector<int> out(s.Rg);
  const double tot = s.tail_cum.back();
  for (int r = 0; r < s.Rg; ++r) {
    const double u = (r + u0) / s.Rg * tot;
    size_t i = (size_t)(std::upper_bound(s.tail_cum.begin(), s.tail_cum.end(), u) - s.tail_cum.begin());
    out[r] = s.tail[std::min(i, s.tail.size() - 1)];
  }
  return out;
}
double mean_se_of(const std::vector<double>& v, double& se) {
  double s = 0; for (double x : v) s += x; const double m = s / v.size();
  double ss = 0; for (double x : v) ss += (x - m) * (x - m);
  se = v.size() > 1 ? std::sqrt(ss / (v.size() - 1) / v.size()) : NAN;
  return m;
}
double sd_of(const std::vector<double>& v) {
  if (v.size() < 2) return 0;
  double m = 0; for (double x : v) m += x; m /= v.size();
  double ss = 0; for (double x : v) ss += (x - m) * (x - m);
  return std::sqrt(ss / (v.size() - 1));
}
// version v of a law with GX groups: 0 pooled, 1..G group g (an exact law: its single value), G + 1 top-K only
inline double pick(const double* o, size_t GX, size_t G, size_t v) {
  if (v == 0) return o[0];
  if (v == G + 1) return o[GX + 1];
  return GX ? o[v] : o[0];
}

}  // namespace

Law truth_law(const Truth& T) {
  Law L; L.name = "truth";
  L.comps.push_back(component_gaussian(T.S0, T.beta, T.alpha, T.sigma2_eff(), 1.0));
  return L;
}

CrossResult cross_h2(const Law& A, const Law& B, const Truth& T, const CrossOpts& o, uint32_t oid_a, uint32_t oid_b) {
  if (A.comps.empty() || B.comps.empty()) throw Error(Status::internal_error, "xeval: empty law");
  if (o.n_x < 2 || o.n_gh < 8 || o.threads < 1 || o.top_k < 1 || o.tail_r < 2 || o.tail_groups < 2 || o.block_rows < 1)
    throw Error(Status::invalid_input, "xeval: bad sizes");
  for (const Law* L : {&A, &B}) {
    double s = 0; for (auto& c : L->comps) s += c.w;
    if (std::fabs(s - 1.0) > 1e-9) throw Error(Status::internal_error, "xeval: weights do not sum to 1");
  }
  CrossOpts oo = o;
  const Split sa = make_split(A, oo), sb = make_split(B, oo);
  const size_t GA = sa.exact ? 0 : (size_t)sa.G, GB = sb.exact ? 0 : (size_t)sb.G, G = std::max(GA, GB), NV = G + 2;
  std::vector<double> ght, ghw; gauss_hermite(o.n_gh, ght, ghw);
  auto top_cols_of = [](const Law& L, const Split& s) {
    std::vector<int32_t> c;
    for (int i : s.top) c.insert(c.end(), L.comps[i].orig.begin(), L.comps[i].orig.end());
    return c;
  };
  const std::vector<int32_t> top_a = top_cols_of(A, sa), top_b = top_cols_of(B, sb);
  const uint32_t Bk = (uint32_t)o.block_rows;
  std::vector<double> aff((size_t)o.n_x * NV);
  for (uint32_t r0 = 0, blk = 0; r0 < (uint32_t)o.n_x; r0 += Bk, ++blk) {
    const uint32_t nr = std::min<uint32_t>(Bk, (uint32_t)o.n_x - r0);
    std::vector<std::vector<int>> ga(GA), gb(GB);
    std::vector<int32_t> cols = top_a; cols.insert(cols.end(), top_b.begin(), top_b.end());
    for (size_t g = 0; g < GA; ++g) { ga[g] = tail_sample(sa, o.seed, oid_a, 0, blk, (int)g); for (int c : ga[g]) cols.insert(cols.end(), A.comps[c].orig.begin(), A.comps[c].orig.end()); }
    for (size_t g = 0; g < GB; ++g) { gb[g] = tail_sample(sb, o.seed, oid_b, 0, blk, (int)g); for (int c : gb[g]) cols.insert(cols.end(), B.comps[c].orig.begin(), B.comps[c].orig.end()); }
    const XSample xs = make_rows(T, cols, (uint32_t)o.x_row0 + r0, nr, o.seed, false);
    auto fill = [&](MixAt& Mx, const Law& L, const Split& s, const std::vector<std::vector<int>>& groups, size_t r) {
      Mx.ex.resize(s.top.size()); Mx.tau = s.tau;
      for (size_t i = 0; i < s.top.size(); ++i) comp_at(L.comps[s.top[i]], xs, r, L.comps[s.top[i]].w, Mx.ex[i]);
      Mx.tail.assign(groups.size(), {});
      for (size_t g = 0; g < groups.size(); ++g) { Mx.tail[g].resize(groups[g].size()); for (size_t i = 0; i < groups[g].size(); ++i) comp_at(L.comps[groups[g][i]], xs, r, 0, Mx.tail[g][i]); }
    };
#pragma omp parallel for schedule(static) num_threads(o.threads)
    for (long r = 0; r < (long)nr; ++r) {
      MixAt MA, MB; fill(MA, A, sa, ga, (size_t)r); fill(MB, B, sb, gb, (size_t)r);
      double m1a, va, m1b, vb; MA.moments(m1a, va); MB.moments(m1b, vb);
      // importance Gaussian of the GH rule: the moment-matched product of the two predictive densities (symmetric in A, B)
      const double prec = 0.5 * (1.0 / va + 1.0 / vb), sc2 = 1.0 / prec, cen = sc2 * 0.5 * (m1a / va + m1b / vb), sc = std::sqrt(sc2);
      std::vector<double> la(GA + 2), lb(GB + 2);
      double* out = &aff[(size_t)(r0 + r) * NV];
      for (size_t v = 0; v < NV; ++v) out[v] = 0;
      for (size_t i = 0; i < ght.size(); ++i) {
        const double y = cen + M_SQRT2 * sc * ght[i];
        MA.eval(y, la.data()); MB.eval(y, lb.data());
        const double base = std::log(ghw[i]) + ght[i] * ght[i];
        for (size_t v = 0; v < NV; ++v) out[v] += std::exp(base + 0.5 * (pick(la.data(), GA, G, v) + pick(lb.data(), GB, G, v))) * M_SQRT2 * sc;
      }
    }
  }
  auto column = [&](size_t v) { std::vector<double> c((size_t)o.n_x); for (int i = 0; i < o.n_x; ++i) c[i] = aff[(size_t)i * NV + v]; return c; };
  CrossResult R;
  double ase; const double am = mean_se_of(column(0), ase);
  R.h2 = 1.0 - am; R.se_x = ase;
  std::vector<double> hg; for (size_t g = 0; g < G; ++g) { double s_; hg.push_back(1.0 - mean_se_of(column(1 + g), s_)); }
  R.se_tail = G ? sd_of(hg) / std::sqrt((double)G) : 0.0;
  double sK; R.h2_topK = 1.0 - mean_se_of(column(NV - 1), sK);
  R.tail_mass_a = sa.tau; R.tail_mass_b = sb.tau; R.exact_a = sa.exact; R.exact_b = sb.exact;
  R.top_a = sa.top.size(); R.top_b = sb.top.size(); R.tail_a = sa.tail.size(); R.tail_b = sb.tail.size();
  R.n_x = o.n_x; R.n_gh = o.n_gh; R.groups = (int)G;
  return R;
}

// ------------------------------------------------------------------------------------------------ the command
namespace {
struct LawIn { post::LawFile F; std::string hash, data_hash; };
LawIn load_law_in(const std::string& path) {
  LawIn L; L.F = post::read_law(path, &L.hash);
  fmt::Reader B(path, false);
  const Json meta = B.json("meta");
  if (const Json* inp = jfind(meta, "inputs")) L.data_hash = jstr_or(*inp, "data.bin", "");
  return L;
}

// The DATA identity of a data.bin: the section hashes of the standardised X (Xs_cm) and y (ys) plus n, p, p_raw. The whole-file
// content hash is NOT an identity of the data: it covers the meta block, which embeds the writing binary's provenance, so the
// same X/y written by two binaries (the T and V builds of the 10^4 overlap) hash differently. `whole` is kept for provenance only
// (a law's recorded inputs.data.bin is the whole-file hash).
struct DataId { std::string whole, X, y; int32_t n = 0, p = 0, p_raw = 0; };
DataId data_identity(const std::string& path) {
  DataId d; const Data D = prep::load_data(path, &d.whole);   // validates the file (section hashes, stored constants)
  fmt::Reader R(path);
  d.X = hex(R.entry("Xs_cm").sha256, 32); d.y = hex(R.entry("ys").sha256, 32);
  d.n = D.n; d.p = D.p; d.p_raw = D.p_raw;
  return d;
}
}  // namespace

Json run(const Json& a) {
  const auto t0 = std::chrono::steady_clock::now();
  Json rec = Json::object();
  rec["schema"] = "overlap1e4.cross_vt/1";
  const std::string pa = io::arg_str(a, "a", ""), pb = io::arg_str(a, "b", ""), truthp = io::arg_str(a, "truth", ""), datap = io::arg_str(a, "data", "");
  const std::string datapb = io::arg_str(a, "data_b", "");   // law B's own data.bin (when it differs from --data in meta only)
  const std::string dataset = io::arg_str(a, "dataset", ""), seed_id = io::arg_str(a, "seed_id", "");
  const bool b_truth = io::arg_num(a, "b_truth", 0) != 0;
  if (pa.empty() || truthp.empty() || (pb.empty() && !b_truth) || (!pb.empty() && b_truth))
    throw Error(Status::invalid_input, "xeval: --a law.bin, --truth truth.json and exactly one of --b law.bin / --b_truth 1 are required");
  if (!datapb.empty() && (datap.empty() || b_truth)) throw Error(Status::invalid_input, "xeval: --data-b needs --data and a --b law.bin");
  if (dataset.empty() != seed_id.empty()) throw Error(Status::invalid_input, "xeval: --dataset and --seed_id go together");
  if (!seed_id.empty() && seed_id != "1" && seed_id != "2") throw Error(Status::invalid_input, "xeval: --seed_id must be 1 or 2");
  const std::string truth_hash = sha256_file(truthp);
  const Truth T = truth_from_json(read_json_file(truthp));
  CrossOpts o;
  o.seed = (uint32_t)io::arg_num(a, "seed", (double)(uint32_t)(T.seed & 0xffffffffu));   // the eval's default seed rule
  o.n_x = (int)io::arg_num(a, "n_x", 4000); o.n_gh = (int)io::arg_num(a, "n_gh", 64); o.threads = (int)io::arg_num(a, "threads", 1);
  o.top_k = (int)io::arg_num(a, "top_k", 1000); o.tail_r = (int)io::arg_num(a, "tail_r", 1000);
  o.tail_groups = (int)io::arg_num(a, "tail_groups", 8); o.block_rows = (int)io::arg_num(a, "block_rows", 500);

  Json inp = Json::object();
  inp["truth.json"] = truth_hash;
  LawIn LA = load_law_in(pa);
  inp["law_a.bin"] = LA.hash;
  Json x = Json::object();
  x["a"] = pa;
  Law la = post::to_eval_law(LA.F, "A");
  Law lb; LawIn LB;
  if (b_truth) { lb = truth_law(T); x["b"] = "truth f*"; }
  else {
    LB = load_law_in(pb);
    inp["law_b.bin"] = LB.hash; x["b"] = pb;
    lb = post::to_eval_law(LB.F, "B");
    // the two laws must come from the SAME dataset (pairing check): n, p here; the data identity (X / y section hashes) below
    if (LA.F.n != LB.F.n || LA.F.p != LB.F.p) throw Error(Status::invalid_input, "xeval: the two laws have different n or p");
    // equal recorded whole-file hashes = the same data.bin. Different ones may be a meta-only difference (the binary block of
    // two builds), which cannot be told from a data difference by the hashes alone: then both data.bin files are required.
    if (datap.empty() && !LA.data_hash.empty() && !LB.data_hash.empty() && LA.data_hash != LB.data_hash)
      throw Error(Status::invalid_input, "xeval: the two laws recorded different data.bin whole-file hashes; pass --data (law A's data.bin) and "
                                         "--data-b (law B's) so that the data identity (X / y section hashes) can be compared");
  }
  if (!datap.empty()) {
    const DataId dA = data_identity(datap);
    const DataId dB = datapb.empty() ? dA : data_identity(datapb);
    inp["data.bin"] = dA.whole;
    if (!datapb.empty()) inp["data_b.bin"] = dB.whole;
    if (dA.n != LA.F.n) throw Error(Status::invalid_input, "xeval: data.bin n differs from the law's n");
    // provenance: each file must be the data.bin its law recorded (whole-file hash)
    if (!LA.data_hash.empty() && LA.data_hash != dA.whole)
      throw Error(Status::invalid_input, "xeval: --data hash differs from law A's recorded data.bin hash");
    if (!b_truth && !LB.data_hash.empty() && LB.data_hash != dB.whole)
      throw Error(Status::invalid_input, std::string("xeval: ") + (datapb.empty() ? "--data" : "--data-b") + " hash differs from law B's recorded data.bin hash");
    // identity: the same X and y (section hashes), n, p, p_raw; a real data mismatch is refused
    if (dA.X != dB.X || dA.y != dB.y || dA.n != dB.n || dA.p != dB.p || dA.p_raw != dB.p_raw)
      throw Error(Status::invalid_input, "xeval: the two laws were built on different data (X / y section hashes of data.bin differ)");
    Json id = Json::object(); id["X_section_sha256"] = dA.X; id["y_section_sha256"] = dA.y; id["n"] = dA.n; id["p"] = dA.p; id["p_raw"] = dA.p_raw;
    inp["data_identity"] = id;
  }
  // symmetric tail-stream rule for two store laws: the law with the smaller content hash gets stream 2 (the engine's T id)
  uint32_t oa = 2, ob = 6;
  if (!b_truth && LB.hash < LA.hash) { oa = 6; ob = 2; }
  const CrossResult R = cross_h2(la, lb, T, o, oa, ob);

  Json d = Json::object();
  d["h2"] = R.h2; d["dH"] = std::sqrt(std::max(R.h2, 0.0));
  d["se_x"] = R.se_x; d["se_tail"] = R.se_tail; d["se"] = std::sqrt(R.se_x * R.se_x + R.se_tail * R.se_tail);
  d["h2_topK"] = R.h2_topK;
  d["exact_a"] = R.exact_a; d["exact_b"] = R.exact_b; d["top_a"] = R.top_a; d["top_b"] = R.top_b;
  d["tail_components_a"] = R.tail_a; d["tail_components_b"] = R.tail_b; d["tail_mass_a"] = R.tail_mass_a; d["tail_mass_b"] = R.tail_mass_b;
  d["dropped_mass_a"] = LA.F.dropped_mass; d["dropped_mass_b"] = b_truth ? 0.0 : LB.F.dropped_mass;
  // laws are truncated approximations of the store BMA (README_WP5 law_truncation): d_H(f̄_store, f̄_law) <= sqrt(delta) each
  d["dH_bound_truncation"] = std::sqrt(LA.F.dropped_mass) + (b_truth ? 0.0 : std::sqrt(LB.F.dropped_mass));
  d["n_x"] = o.n_x; d["n_gh"] = o.n_gh; d["seed"] = (int64_t)o.seed; d["top_k"] = o.top_k; d["tail_r"] = o.tail_r;
  d["tail_groups"] = o.tail_groups; d["block_rows"] = o.block_rows; d["threads"] = o.threads;
  d["oid_a"] = (int64_t)oa; d["oid_b"] = (int64_t)ob;
  d["rows"] = T.gen_spec.is_null() ? "eval_philox" : "gen_test";
  d["definition"] = "h2 = 1 - mean_x int sqrt(fbar_A fbar_B) dy, same x rows / 64-node Gauss-Hermite / top-K + stratified tail as the engine eval predictive";
  d["wall_s"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  rec["xeval"] = d; rec["inputs"] = inp;
  Json pairs = Json::object();
  if (!dataset.empty()) {
    Json cell = Json::object(); cell["h2"] = R.h2; cell["se"] = d.at("se"); cell["se_x"] = R.se_x; cell["se_tail"] = R.se_tail;
    Json bys = Json::object(); bys[seed_id] = cell; pairs[dataset] = bys;
  }
  rec["pairs"] = pairs;
  rec["status"] = "completed";
  return rec;
}

}  // namespace v4::xeval
