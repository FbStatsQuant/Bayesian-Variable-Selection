// merge.h -- WP4: merge of R' island results and the tail (spec §1 row 5, §0-v2.2 #2/#8, §4.2 rows "R' != 4, merge"
// and "table and inherited models offered at the merge", §6; DECISIONS D-6, D-11, D-13).
//
// Order of work = the serial order of core/cpp/v3_core.cpp:407-481 + core/v3_run.R:119-220:
//   1. the pre-island ledger: table events, inherited models (offered at the merge, not per island), the inherited
//      HPM's calibration provenance (core/cpp/v3_core.cpp:419-441) -- built by the caller with the helpers below;
//   2. GUARD-W: every manifest island present, valid and completed, or the merge refuses (no subset is ever pooled);
//   3. Ledger.merge of the islands (stores = top-c of the union; HPM by hpm_better, provenance = smallest EventKey;
//      island_best by maximum; logical counters by sum);
//   4. the tail: final local search from the merged HPM (cap ell), the start mode, LS0 (cap ell + |S~0|);
//   5. assembly: log Z^ (LSE - log R'), PIP_eq (primary, equal weight), PIP_Z + R_eff + max W_r, log Z_T + PIP_T
//      (store-renormalised), log Z^_occ for top-M sets, MPM, near ties, flags.
// No estimate field is filled unless every island and the tail completed (GUARD-W, spec §4.3).
#pragma once
#include <cmath>
#include <functional>
#include <string>
#include <unordered_map>
#include <vector>
#include "calib_rules.h"
#include "tail.h"
#include "wp4_standin.h"

namespace v4 {
namespace merge {

// In-memory island record (INTERFACES §5.2 IslandResult; fields WP4 reads). `terminal` = the optional terminal
// supports (`terminal_S_ptr/terminal_S`): ASSUMED to be the N particle supports after each measured round (Hm x N
// entries) -- to be confirmed by WP3.
struct IslandIn {
  Status status = Status::completed; std::string message;
  int32_t r = 0, N = 0, T = 0, L = 0, Hm = 4;
  double logZ = 0;
  std::vector<double> ess;               // bridge stages 1..T (stage table st_ess)
  std::vector<double> rb_acc, pip;       // p each
  std::vector<std::vector<double>> rb_round;
  Ledger led;
  std::vector<Model> terminal;           // optional
};
// How an island file was found by the loader (WP1 format reader / manifest check).
enum class Load : uint8_t { ok = 0, missing, corrupt, hash_mismatch };
struct IslandSlot { Load load = Load::missing; IslandIn isl; std::string detail; };

struct MergeSettings {
  int Rp = 16;                 // manifest R'
  int N = 0;                   // final N (for the low-ESS flag 0.5 N)
  int p = 0, K = 0, tier = 0;
  int ell = 0;                 // final local search cap
  bool ls0 = true;             // v3.1 LS0
  int ls0_ell = -1;            // LS0 base cap (-1 = ell)
  bool ls0_cap_plus_mode = true;   // C-GROW MR1: cap ell + |S~0|
  double log_m0 = 0;
  std::vector<int> occ_M{1, 10, 100, 1000};
  double near_tie_eps = 1e-9;
  int threads = 1; size_t chunk = 2048;
};

struct OccRow {   // log Z^_occ for one M (D-13)
  int M = 0; int M_used = 0;
  double log_store_mass = 0;           // LSE of F over the top-M models of the merged store
  double occ = 0, log_Z_occ = 0;       // pooled terminal occupancy of the set; log_store_mass - log occ
  std::vector<double> occ_r, log_Z_occ_r;
  double sd_log_Z_occ_r = 0;
  double chi2_homogeneity = 0; int chi2_df = 0;   // island homogeneity of the occupancies (flag only)
};

struct FitOut {
  // status (INTERFACES §7) + why; fit_state = "completed" | "incomplete" (merge refused) | "failed"
  Status status = Status::completed; std::string fit_state = "completed", reason;
  std::vector<Status> island_status; std::vector<int> missing, invalid;
  bool estimates_available = false;
  // HPM (always reported when the ledger exists; labelled incomplete otherwise)
  bool has_hpm = false, hpm_incomplete = false; Model hpm; double hpm_F = 0, hpm_logm = 0; EventCtx hpm_ev;
  Model hpm_before_local; double hpm_before_local_F = 0;
  Model hpm_before_ls0; double hpm_before_ls0_F = 0; EventCtx hpm_before_ls0_ev;
  LocalArchive local, ls0; bool has_local = false, has_ls0 = false; int ls0_cap = 0;
  Model mode_S;
  // estimates (only if estimates_available)
  std::vector<double> logZ_r; double log_Z = 0, log_Z_lower95 = 0, log_Z_rel_m0 = 0;
  std::vector<double> log_Z_r_rel_m0;
  std::vector<std::vector<double>> pip_r;     // R' x p
  std::vector<double> pip_eq, pip_Z, pip_T, W_r; double R_eff = 0, max_W = 0;
  double log_Z_T = 0;
  std::vector<int32_t> mpm;
  std::vector<OccRow> occ; bool occ_available = false;
  // near ties, certificates, flags (core/v3_run.R:169-207, v3.1 branch)
  std::vector<Model> near_ties; std::vector<double> near_tie_F; bool near_tie_truncated = false;
  bool local_limit = false, local_certified = false; std::string local_certified_by = "none";
  bool final_local_limit = false, ls0_local_limit = false, ls0_improved = false, ls0_hpm_changed = false;
  bool E1 = false, E2 = false, E3 = false, low_ESS = false, checks_passed_final = false;
  Ledger led;   // merged ledger after the tail: top store, leader stores (compat), island_best, logical counters
};

// ---- helpers for the pre-island ledger ----------------------------------------------------------------------------
inline EventCtx table_event(int block, uint32_t code) {   // core/cpp/v3_core.cpp:372-387 (stage = b + 1, position = code)
  EventCtx ev; ev.phase = PH_TABLE; ev.mech = ME_TABLE; ev.key.seg = SG_TABLE; ev.key.iter = -1;
  ev.key.stage = (uint32_t)block + 1; ev.key.position = code; return ev;
}
inline EventCtx inherited_event() {
  EventCtx ev; ev.phase = PH_INHERITED; ev.mech = ME_INHERITED; ev.key.seg = SG_INHERITED; ev.key.iter = -1; return ev;
}
// core/cpp/v3_core.cpp:430-441: after the inherited offers, the inherited HPM's label "inherited" is replaced by its
// calibration provenance when the ledger's HPM is the calibration HPM and still carries the label "inherited".
inline void apply_inherited_provenance(Ledger& led, const Model& calib_hpm, const EventCtx& calib_ev) {
  if (led.has_hpm && led.hpm_ev.phase == PH_INHERITED && led.hpmS == calib_hpm) led.hpm_ev = calib_ev;
}

namespace detail {
struct ModelHash {
  size_t operator()(const Model& S) const {
    uint64_t h = 0x9E3779B97F4A7C15ULL;
    for (int32_t j : S) { h ^= (uint64_t)(uint32_t)j + 0x9E3779B97F4A7C15ULL + (h << 6) + (h >> 2); }
    return (size_t)h;
  }
};
// LSE in the arithmetic of core/v3_run.R:4 (R: m + log(sum(exp(x - m))), sum in long double) = calib::lse_cal.
inline double lse(const std::vector<double>& x) { return calib::lse_cal(x); }
}  // namespace detail

// GUARD-W check (spec §6 "missing or invalid island at merge"). Returns true if the merge may proceed.
inline bool guard_islands(const std::vector<IslandSlot>& slots, const MergeSettings& ms, FitOut& out) {
  std::vector<Status> st;
  if ((int)slots.size() != ms.Rp) { out.status = Status::invalid_input; out.fit_state = "incomplete"; out.reason = "manifest R' != number of island slots"; return false; }
  for (int i = 0; i < ms.Rp; ++i) {
    const IslandSlot& s = slots[i];
    Status x = Status::completed;
    switch (s.load) {
      case Load::missing: x = Status::io_error; out.missing.push_back(i + 1); break;
      case Load::corrupt: x = Status::invalid_input; out.invalid.push_back(i + 1); break;
      case Load::hash_mismatch: x = Status::invalid_input; out.invalid.push_back(i + 1); break;
      case Load::ok:
        if (s.isl.r != i + 1 || (int)s.isl.pip.size() != ms.p || s.isl.N != ms.N) { x = Status::invalid_input; out.invalid.push_back(i + 1); }
        else x = s.isl.status;
        break;
    }
    st.push_back(x);
  }
  out.island_status = st;
  Status f = fit_status(st);
  if (f != Status::completed) {
    out.status = f; out.fit_state = "incomplete";
    out.reason = "merge refused (GUARD-W): " + std::to_string(out.missing.size()) + " missing, " + std::to_string(out.invalid.size()) +
                 " invalid, " + std::to_string(std::count_if(st.begin(), st.end(), [](Status s) { return s == Status::numerical_failure || s == Status::resource_limit; })) +
                 " failed island(s)";
    return false;
  }
  return true;
}

// The merge + tail. `pre` = the pre-island ledger (tables, inherited, provenance applied); mode_S = start mode (setup).
// Factory: per-thread evaluator for the tail (calib::rescore_V contract). guard(seconds, checkpoint) -> true = stop.
template <class Factory>
FitOut merge_and_tail(const std::vector<IslandSlot>& slots, Ledger pre, const Model& mode_S, Factory& fac, const MergeSettings& ms,
                      const std::function<bool(double, const std::string&)>& guard = nullptr) {
  FitOut out;
  if (!guard_islands(slots, ms, out)) return out;   // no ledger, no estimates
  const int R = ms.Rp, p = ms.p;
  // 3. ledger merge (order-free)
  Ledger led = std::move(pre);
  if ((int)led.island_best.size() < R + 1) led.island_best.resize(R + 1, NEG_INF);
  for (auto& s : slots) led.merge(s.isl.led);
  led.compact();
  // 4. tail
  TailSettings ts; ts.threads = ms.threads; ts.chunk = ms.chunk; ts.K = ms.K; ts.p = p; ts.tier = ms.tier;
  out.hpm_before_local = led.hpmS; out.hpm_before_local_F = led.hpmF;
  try {
    auto t0 = std::chrono::steady_clock::now();
    out.local = local_search(led.hpmS, ms.ell, false, PH_LOCAL, led, fac, ts); out.has_local = true;
    if (guard && guard(std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count(), "local_search")) {
      out.status = Status::resource_limit; out.fit_state = "failed"; out.reason = "runtime guard after the final local search";
    }
    if (ms.ls0 && out.status == Status::completed) {
      out.hpm_before_ls0 = led.hpmS; out.hpm_before_ls0_F = led.hpmF; out.hpm_before_ls0_ev = led.hpm_ev;
      out.mode_S = mode_S;
      int base = ms.ls0_ell >= 0 ? ms.ls0_ell : ms.ell;
      long long cap = (long long)base + (ms.ls0_cap_plus_mode ? (long long)mode_S.size() : 0LL);
      if (base < 0 || cap > (long long)std::numeric_limits<int>::max()) throw Error(Status::internal_error, "LS0 move cap out of range");
      out.ls0_cap = (int)cap;
      auto t1 = std::chrono::steady_clock::now();
      out.ls0 = local_search(mode_S, out.ls0_cap, true, PH_LS0, led, fac, ts); out.has_ls0 = true;
      if (guard && guard(std::chrono::duration<double>(std::chrono::steady_clock::now() - t1).count(), "ls0")) {
        out.status = Status::resource_limit; out.fit_state = "failed"; out.reason = "runtime guard after LS0";
      }
    }
  } catch (const NumericalFailure& e) {
    out.status = Status::numerical_failure; out.fit_state = "failed"; out.reason = e.what();
  }
  led.compact();
  out.has_hpm = led.has_hpm; out.hpm = led.hpmS; out.hpm_F = led.hpmF; out.hpm_logm = led.hpm_logm; out.hpm_ev = led.hpm_ev;
  if (out.status != Status::completed) { out.hpm_incomplete = true; out.led = std::move(led); return out; }

  // 5. assembly (core/v3_run.R:150-216, v3.1 branch)
  for (auto& s : slots) out.logZ_r.push_back(s.isl.logZ);
  out.log_Z = detail::lse(out.logZ_r) - std::log((double)R);
  out.log_Z_lower95 = std::log(0.05) + out.log_Z;
  out.log_Z_rel_m0 = out.log_Z - ms.log_m0;
  for (double z : out.logZ_r) out.log_Z_r_rel_m0.push_back(z - ms.log_m0);
  for (auto& s : slots) out.pip_r.push_back(s.isl.pip);
  // PIP_eq = rowMeans (R: long double accumulation over islands, divided by R in long double)
  out.pip_eq.assign(p, 0.0);
  for (int j = 0; j < p; ++j) { long double a = 0.0L; for (int r = 0; r < R; ++r) a += out.pip_r[r][j]; a /= (long double)R; out.pip_eq[j] = (double)a; }
  for (int j = 0; j < p; ++j) if (out.pip_eq[j] > 0.5) out.mpm.push_back(j);
  // PIP_Z: evidence weights W_r = Z_r / sum Z_r
  double lz = detail::lse(out.logZ_r);
  double w2 = 0; out.max_W = 0;
  for (double z : out.logZ_r) { double w = std::exp(z - lz); out.W_r.push_back(w); w2 += w * w; out.max_W = std::max(out.max_W, w); }
  out.R_eff = 1.0 / w2;
  out.pip_Z.assign(p, 0.0);
  for (int j = 0; j < p; ++j) { long double a = 0.0L; for (int r = 0; r < R; ++r) a += (long double)out.W_r[r] * out.pip_r[r][j]; out.pip_Z[j] = (double)a; }
  // log Z_T (deterministic lower bound: LSE of F over the merged top store) and PIP_T (store-renormalised)
  const auto& top = led.top.e;
  { std::vector<double> F; F.reserve(top.size()); for (auto& x : top) F.push_back(x.v); out.log_Z_T = detail::lse(F); }
  { std::vector<long double> acc(p, 0.0L);
    for (auto& x : top) { long double w = std::exp((long double)(x.v - out.log_Z_T)); for (int32_t j : x.S) acc[j] += w; }
    out.pip_T.assign(p, 0.0); for (int j = 0; j < p; ++j) out.pip_T[j] = (double)acc[j]; }
  // log Z^_occ (D-13): available only if every island supplied terminal supports
  out.occ_available = true;
  for (auto& s : slots) if (s.isl.terminal.empty()) out.occ_available = false;
  if (out.occ_available) {
    for (int M : ms.occ_M) {
      OccRow row; row.M = M; row.M_used = (int)std::min<size_t>((size_t)M, top.size());
      std::unordered_map<Model, int, detail::ModelHash> set;
      std::vector<double> F;
      for (int i = 0; i < row.M_used; ++i) { set.emplace(top[i].S, i); F.push_back(top[i].v); }
      row.log_store_mass = detail::lse(F);
      uint64_t in_all = 0, tot_all = 0; std::vector<uint64_t> in_r, tot_r;
      for (auto& s : slots) {
        uint64_t in = 0; for (auto& S : s.isl.terminal) if (set.count(S)) ++in;
        in_r.push_back(in); tot_r.push_back(s.isl.terminal.size()); in_all += in; tot_all += s.isl.terminal.size();
      }
      row.occ = (double)in_all / (double)tot_all;
      row.log_Z_occ = row.log_store_mass - std::log(row.occ);
      for (int r = 0; r < R; ++r) {
        double o = (double)in_r[r] / (double)tot_r[r];
        row.occ_r.push_back(o); row.log_Z_occ_r.push_back(row.log_store_mass - std::log(o));
      }
      row.sd_log_Z_occ_r = calib::r_sd(row.log_Z_occ_r);
      // Pearson chi-square of the 2 x R' table (in set / not in set by island), df = R' - 1
      double pin = row.occ; double chi = 0;
      if (pin > 0 && pin < 1) for (int r = 0; r < R; ++r) {
        double ein = pin * tot_r[r], eout = (1 - pin) * tot_r[r];
        double oin = (double)in_r[r], oout = (double)(tot_r[r] - in_r[r]);
        chi += (oin - ein) * (oin - ein) / ein + (oout - eout) * (oout - eout) / eout;
      }
      row.chi2_homogeneity = chi; row.chi2_df = R - 1;
      out.occ.push_back(row);
    }
  }
  // near ties (core/v3_run.R:170-173)
  for (auto& x : top) if (x.v >= out.hpm_F - ms.near_tie_eps) { out.near_ties.push_back(x.S); out.near_tie_F.push_back(x.v); }
  out.near_tie_truncated = led.top.full() && !top.empty() && top.back().v >= out.hpm_F - ms.near_tie_eps;
  // certificates and flags (core/v3_run.R:175-207)
  const LocalArchive& ls = out.local;
  out.local_limit = ls.local_limit;
  bool cert_final = ls.local_certified && out.hpm == ls.returned;
  out.local_certified = cert_final;
  for (int r = 1; r <= R; ++r) if (led.island_best[r] < out.hpm_F - 1) out.E1 = true;
  out.E2 = R >= 2 && calib::r_sd(out.logZ_r) > 1;
  out.E3 = out.hpm_F > out.hpm_before_local_F;
  if (ms.ls0) {
    out.E3 = out.hpm_before_ls0_F > out.hpm_before_local_F;   // LS0 does not fire E3
    bool cert_ls0 = out.ls0.local_certified && out.hpm == out.ls0.returned;
    out.local_certified = cert_final || cert_ls0;
    out.local_certified_by = cert_final && cert_ls0 ? "both" : cert_final ? "final" : cert_ls0 ? "ls0" : "none";
    out.final_local_limit = ls.local_limit; out.ls0_local_limit = out.ls0.local_limit;
    out.local_limit = out.final_local_limit || out.ls0_local_limit;
    out.ls0_improved = out.hpm_F > out.hpm_before_ls0_F;
    out.ls0_hpm_changed = out.hpm != out.hpm_before_ls0;
  }
  for (auto& s : slots) for (double e : s.isl.ess) if (e < 0.5 * ms.N) out.low_ESS = true;
  out.checks_passed_final = !(out.E1 || out.E2 || out.E3 || out.low_ESS);
  out.estimates_available = true;
  out.led = std::move(led);
  return out;
}

}  // namespace merge
}  // namespace v4
