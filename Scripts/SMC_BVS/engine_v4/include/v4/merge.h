// merge.h -- WP4: merge of R' island results and the tail (spec §1 row 5, §0-v2.2 #2/#8, §4.2 rows "R' != 4, merge"
// and "table and inherited models offered at the merge", §6; DECISIONS D-6, D-11, D-13).
//
// Order of work = the serial order of core/cpp/v3_core.cpp:407-481 + core/v3_run.R:119-220:
//   1. the pre-island ledger: table events, inherited models (offered at the merge, not per island), the calibration
//      HPM offered with its CALIBRATION EventCtx (INTERFACES v0.1.6) -- built by the caller with the helpers below;
//   2. GUARD-W, pass 1 over the islands' heads only: every manifest island present, valid, completed and with a finite
//      log Z_r, or the merge refuses (no subset is ever pooled); then the memory admission (--mem-budget);
//   3. pass 2, STREAMING (review PR16 F1): one island at a time is loaded, Ledger.merge'd into the one merged ledger
//      (stores = top-c of the union; HPM by hpm_better, provenance = smallest EventKey; island_best by maximum; logical
//      counters by sum -- all order-free) and freed; only its small fields (log Z_r, ess, pip_r, terminal supports)
//      are kept. Peak = merged ledger + one island + small fields + bounded tail buffers;
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
#include <algorithm>
#include <chrono>
#include <limits>
#include "v4/calib_rules.h"
#include "v4/ledger.h"
#include "v4/records.h"
#include "v4/status.h"
#include "v4/tail.h"

namespace v4 {
namespace merge {

// In-memory island record (INTERFACES §5.2 IslandResult; fields WP4 reads). `terminal` = the optional terminal
// supports (`terminal_S_ptr/terminal_S`): the supports of the N particles after the LAST measured round (manager
// decision 2026-11-15; WP3 writes them). The merge counts whatever list it is given.
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
// How an island file was found by the loader (WP1 format reader / manifest / binary check).
enum class Load : uint8_t { ok = 0, missing, corrupt, hash_mismatch, binary_mismatch };
// Pass-1 view of an island: what GUARD-W needs, read from headers and meta only (no store is loaded).
struct IslandHead { Load load = Load::missing; Status status = Status::completed; int32_t r = 0, N = 0, p = 0; double logZ = 0; std::string detail; };
// Where the streaming merge reads islands from: files (slice 2), memory (tests, golden harness).
struct IslandSource {
  virtual ~IslandSource() = default;
  virtual int count() const = 0;
  virtual IslandHead head(int r) = 0;    // r = 1..count(); cheap
  virtual IslandIn load(int r) = 0;      // the full island; the merge frees it after merging
};
// In-memory slots (tests, harness). load() copies one island at a time, so the peak still holds one island copy.
struct IslandSlot { Load load = Load::missing; IslandIn isl; std::string detail; };
struct VectorSource : IslandSource {
  const std::vector<IslandSlot>& v;
  explicit VectorSource(const std::vector<IslandSlot>& s) : v(s) {}
  int count() const override { return (int)v.size(); }
  IslandHead head(int r) override {
    const IslandSlot& s = v[(size_t)r - 1]; IslandHead h; h.load = s.load; h.detail = s.detail;
    h.status = s.isl.status; h.r = s.isl.r; h.N = s.isl.N; h.p = (int32_t)s.isl.pip.size(); h.logZ = s.isl.logZ; return h;
  }
  IslandIn load(int r) override { return v[(size_t)r - 1].isl; }
};

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
  const Zobrist* zob = nullptr;   // model hashes (Data::zob)
  // memory admission (review PR16 F1): 0 = off; else refuse with resource_limit before any island store is loaded if
  // estimate_merge_memory(...).total exceeds it
  uint64_t mem_budget_bytes = 0;
  double kbar = 8;             // mean model size used by the estimate
  // INTERFACES v0.1.7: final-run leader stores are not outputs in any mode; final-run ledgers use leaders = false
};

// Memory model of the streaming merge (ESTIMATE; bytes). A store entry costs 26 + 4 k bytes (v, off, hash, len, pool);
// a store peaks at 2.5 cap entries (kept + staging + new kept run, INTERFACES §4.1).
struct MemEstimate { uint64_t merged = 0, one_island = 0, small = 0, tail = 0, total = 0; };
inline MemEstimate estimate_merge_memory(const MergeSettings& ms) {
  const double entry = 26.0 + 4.0 * ms.kbar, c = 40.0 * ms.p + 1, lead = 0.0;   // no final-run leaders (v0.1.7)
  MemEstimate m;
  m.merged = (uint64_t)(2.5 * (c + lead) * entry);
  m.one_island = (uint64_t)(2.5 * c * entry);                                        // one island store while loaded
  m.small = (uint64_t)((double)ms.Rp * ms.p * 8.0 * 2 + (double)ms.Rp * ms.N * (24 + 4 * ms.kbar));   // pip_r (+ pip_eq/Z/T) + terminal supports
  m.tail = (uint64_t)((double)std::max(1, ms.threads) * 4 * (double)ms.chunk * (entry + 48));        // one wave of chunk buffers
  m.total = m.merged + m.one_island + m.small + m.tail;
  return m;
}

struct OccRow {   // log Z^_occ for one M (D-13)
  int M = 0; int M_used = 0;
  bool available = true;               // false if the pooled occupancy of the set is 0 (review PR16 F5)
  double log_store_mass = 0;           // LSE of F over the top-M models of the merged store
  double occ = 0, log_Z_occ = 0;       // pooled terminal occupancy of the set; log_store_mass - log occ
  std::vector<double> occ_r, log_Z_occ_r;   // NaN for an island with zero occupancy
  int n_zero_islands = 0;              // islands with zero occupancy: excluded from the sd and the chi-square
  double sd_log_Z_occ_r = 0;
  double chi2_homogeneity = 0; int chi2_df = 0;   // island homogeneity of the occupancies (flag only)
};

struct FitOut {
  // status (INTERFACES §7) + why; fit_state = "completed" | "incomplete" (merge refused) | "not_admitted" | "failed"
  Status status = Status::completed; std::string fit_state = "completed", reason;
  std::vector<Status> island_status; std::vector<int> missing, invalid;
  bool estimates_available = false;
  MemEstimate mem;
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
  // per-model terminal occupancy of the first M_top = min(max occ_M, |store|) store models (WP5 fit.bin `occ_top`,
  // `occ_top_r` R' x M_top, meta `occ_total`, `occ_total_r`)
  std::vector<uint64_t> occ_top, occ_top_r, occ_total_r; uint64_t occ_total = 0;
  // near ties, certificates, flags (core/v3_run.R:169-207, v3.1 branch)
  std::vector<Model> near_ties; std::vector<double> near_tie_F; bool near_tie_truncated = false;
  bool local_limit = false, local_certified = false; std::string local_certified_by = "none";
  bool final_local_limit = false, ls0_local_limit = false, ls0_improved = false, ls0_hpm_changed = false;
  bool E1 = false, E2 = false, E3 = false, low_ESS = false, checks_passed_final = false;
  Ledger led;   // merged ledger after the tail: top store, leader stores (compat), island_best, logical counters
};

// ---- helpers for the pre-island ledger ----------------------------------------------------------------------------
inline EventCtx table_event(int block, uint32_t code) {   // core/cpp/v3_core.cpp:372-387 (stage = b + 1, position = code)
  EventCtx ev; ev.phase = PH_TABLE; ev.mech = ME_TABLE; ev.key.seg = SG_TABLE; ev.key.iter = -1; ev.key.unit = 0;
  ev.key.stage = (uint32_t)block + 1; ev.key.position = code; return ev;
}
// INTERFACES v0.1.5 key table: inherited model i (input order) = (INHERITED, tier 0, iter -1, unit 0, particle i).
inline EventCtx inherited_event(uint32_t i) {
  EventCtx ev; ev.phase = PH_INHERITED; ev.mech = ME_INHERITED; ev.key.seg = SG_INHERITED; ev.key.iter = -1; ev.key.particle = i;
  return ev;
}
// One inherited model with its stored values (calibration scorer: F, lg0, logm).
struct InheritedModel { Model S; double F = 0, lg0 = 0, logm = 0; };
// The inherited step (core/cpp/v3_core.cpp:419-441; INTERFACES v0.1.6 §4.2): every model is offered to the HPM and the
// stores (no logical count, as v3's offer_stores). The offer of the CALIBRATION HPM model carries that model's
// calibration EventCtx (segment CALIB); all others carry INHERITED keys with their input index. With the smallest-key
// rule this gives v3's provenance in its three cases: (i) the model is also a table model -> its table event (earlier
// key) wins, as in v3 where the HPM then carries the label "table" and is not relabelled; (ii) it is in the inherited
// list only -> its calibration provenance; (iii) it is in neither -> it is never offered, as in v3 (nothing relabelled).
inline void offer_inherited(Ledger& led, const std::vector<InheritedModel>& inh, bool has_calib_hpm, const Model& calib_hpm,
                            const EventCtx& calib_ev, const Zobrist& zob) {
  for (size_t i = 0; i < inh.size(); ++i) {
    const InheritedModel& m = inh[i];
    const bool is_hpm = has_calib_hpm && m.S == calib_hpm;
    led.offer_stores(m.S, zob.hash(m.S), m.F, m.lg0, m.logm, is_hpm ? calib_ev : inherited_event((uint32_t)i));
  }
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
inline Status load_status(Load l) {
  switch (l) {
    case Load::ok: return Status::completed;
    case Load::missing: return Status::io_error;
    default: return Status::invalid_input;   // corrupt, hash_mismatch, binary_mismatch
  }
}
}  // namespace detail

// GUARD-W, pass 1 (spec §6 "missing or invalid island at merge"): heads only. A non-finite log Z_r is a numerical
// failure of that island (review PR16 F8; R's sd would give NA there). Returns true if the merge may proceed.
inline bool guard_heads(IslandSource& src, const MergeSettings& ms, FitOut& out) {
  if (src.count() != ms.Rp) { out.status = Status::invalid_input; out.fit_state = "incomplete"; out.reason = "manifest R' != number of islands"; return false; }
  std::vector<Status> st;
  for (int r = 1; r <= ms.Rp; ++r) {
    IslandHead h = src.head(r);
    Status x = detail::load_status(h.load);
    if (h.load == Load::missing) out.missing.push_back(r);
    else if (h.load != Load::ok) out.invalid.push_back(r);
    else if (h.r != r || h.p != ms.p || h.N != ms.N) { x = Status::invalid_input; out.invalid.push_back(r); }
    else if (h.status != Status::completed) x = h.status;
    else if (!std::isfinite(h.logZ)) x = Status::numerical_failure;
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

// The streaming merge + tail. `pre` = the pre-island ledger (tables, inherited), moved in; mode_S = start mode (setup).
// Factory: per-thread evaluator for the tail (calib::rescore_V contract). guard(seconds, checkpoint) -> true = stop.
template <class Factory>
FitOut merge_stream(IslandSource& src, Ledger&& pre, const Model& mode_S, Factory& fac, const MergeSettings& ms,
                    const std::function<bool(double, const std::string&)>& guard = nullptr) {
  FitOut out;
  out.mem = estimate_merge_memory(ms);
  if (!guard_heads(src, ms, out)) return out;   // no ledger, no estimates
  if (ms.mem_budget_bytes && out.mem.total > ms.mem_budget_bytes) {
    out.status = Status::resource_limit; out.fit_state = "not_admitted";
    out.reason = "merge not admitted: estimated peak " + std::to_string(out.mem.total) + " B > --mem-budget " + std::to_string(ms.mem_budget_bytes) + " B";
    return out;
  }
  if (pre.lead0.cap != 0 || pre.lead1.cap != 0) {   // v0.1.7: no final-run leaders; the admission assumes none (re-check m-2)
    out.status = Status::invalid_input; out.fit_state = "incomplete";
    out.reason = "merge refused: the pre-island ledger has leader stores (final-run ledgers need leaders = false, INTERFACES v0.1.7)";
    return out;
  }
  const int R = ms.Rp, p = ms.p;
  // 3. pass 2: stream the islands into the one merged ledger (order-free), keep the small fields
  Ledger led = std::move(pre);
  std::vector<double> ess_all;
  std::vector<std::vector<Model>> terminal((size_t)R);
  for (int r = 1; r <= R; ++r) {
    IslandIn I = src.load(r);
    if (I.r != r || (int)I.pip.size() != p || I.N != ms.N || I.status != Status::completed || !std::isfinite(I.logZ)) {
      out = FitOut(); out.mem = estimate_merge_memory(ms);
      out.status = Status::invalid_input; out.fit_state = "incomplete";
      out.reason = "merge refused (GUARD-W): island " + std::to_string(r) + " changed between the head check and its load" +
                   (I.message.empty() ? std::string() : " (" + I.message + ")");
      return out;
    }
    if (I.led.lead0.cap != 0 || I.led.lead1.cap != 0) {   // final-run island ledgers carry no leaders (v0.1.7)
      out = FitOut(); out.mem = estimate_merge_memory(ms);
      out.status = Status::invalid_input; out.fit_state = "incomplete";
      out.reason = "merge refused (GUARD-W): island " + std::to_string(r) + " has leader stores (INTERFACES v0.1.7)";
      return out;
    }
    if (!I.terminal.empty() && (int64_t)I.terminal.size() != (int64_t)I.N) {   // N supports (last measured round) or none
      out = FitOut(); out.mem = estimate_merge_memory(ms);
      out.status = Status::invalid_input; out.fit_state = "incomplete";
      out.reason = "merge refused (GUARD-W): island " + std::to_string(r) + " has " + std::to_string(I.terminal.size()) +
                   " terminal supports, expected N = " + std::to_string(I.N) + " (the last measured round)";
      return out;
    }
    led.merge(I.led);
    out.logZ_r.push_back(I.logZ);
    out.pip_r.push_back(std::move(I.pip));
    ess_all.insert(ess_all.end(), I.ess.begin(), I.ess.end());
    terminal[(size_t)r - 1] = std::move(I.terminal);
  }   // each IslandIn (its ledger and stores) is freed at the end of its iteration
  led.compact();
  // 4. tail
  TailSettings ts; ts.threads = ms.threads; ts.chunk = ms.chunk; ts.K = ms.K; ts.p = p; ts.tier = ms.tier; ts.zob = ms.zob;
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
  } catch (const Error& e) {
    out.status = e.st; out.fit_state = "failed"; out.reason = e.what();
  }
  led.compact();
  out.has_hpm = led.has_hpm; out.hpm = led.hpmS; out.hpm_F = led.hpmF; out.hpm_logm = led.hpm_logm; out.hpm_ev = led.hpm_ev;
  if (out.status != Status::completed) {   // GUARD-W: no estimate field
    out.hpm_incomplete = true; out.logZ_r.clear(); out.pip_r.clear(); out.led = std::move(led); return out;
  }

  // 5. assembly (core/v3_run.R:150-216, v3.1 branch)
  out.log_Z = detail::lse(out.logZ_r) - pm::log((double)R);
  out.log_Z_lower95 = pm::log(0.05) + out.log_Z;
  out.log_Z_rel_m0 = out.log_Z - ms.log_m0;
  for (double z : out.logZ_r) out.log_Z_r_rel_m0.push_back(z - ms.log_m0);
  // PIP_eq = rowMeans (R: long double accumulation over islands, divided by R in long double)
  out.pip_eq.assign(p, 0.0);
  for (int j = 0; j < p; ++j) { long double a = 0.0L; for (int r = 0; r < R; ++r) a += out.pip_r[r][j]; a /= (long double)R; out.pip_eq[j] = (double)a; }
  for (int j = 0; j < p; ++j) if (out.pip_eq[j] > 0.5) out.mpm.push_back(j);
  // PIP_Z: evidence weights W_r = Z_r / sum Z_r
  double lz = detail::lse(out.logZ_r);
  double w2 = 0; out.max_W = 0;
  for (double z : out.logZ_r) { double w = pm::exp(z - lz); out.W_r.push_back(w); w2 += w * w; out.max_W = std::max(out.max_W, w); }
  out.R_eff = 1.0 / w2;
  out.pip_Z.assign(p, 0.0);
  for (int j = 0; j < p; ++j) { long double a = 0.0L; for (int r = 0; r < R; ++r) a += (long double)out.W_r[r] * out.pip_r[r][j]; out.pip_Z[j] = (double)a; }
  // log Z_T (deterministic lower bound: LSE of F over the merged top store) and PIP_T (store-renormalised)
  const Store& top = led.top;   // compacted: entries sorted under the HPM order
  out.log_Z_T = detail::lse(top.v);
  { std::vector<long double> acc(p, 0.0L);
    for (size_t i = 0; i < top.size(); ++i) { long double w = pm::expl((long double)(top.v[i] - out.log_Z_T)); for (int32_t j : top.model(i)) acc[j] += w; }
    out.pip_T.assign(p, 0.0); for (int j = 0; j < p; ++j) out.pip_T[j] = (double)acc[j]; }
  // log Z^_occ (D-13): available only if every island supplied terminal supports
  out.occ_available = true;
  for (auto& t : terminal) if (t.empty()) out.occ_available = false;
  if (out.occ_available) {
    {  // per-model counts of the top models
      int Mt = 0; for (int M : ms.occ_M) Mt = std::max(Mt, M);
      Mt = (int)std::min<size_t>((size_t)Mt, top.size());
      std::unordered_map<Model, int, detail::ModelHash> idx;
      for (int i = 0; i < Mt; ++i) { ModelView S = top.model((size_t)i); idx.emplace(Model(S.begin(), S.end()), i); }
      out.occ_top.assign((size_t)Mt, 0); out.occ_top_r.assign((size_t)R * (size_t)Mt, 0);
      for (int r = 0; r < R; ++r) {
        for (auto& S : terminal[(size_t)r]) {
          auto it = idx.find(S);
          if (it != idx.end()) { out.occ_top[(size_t)it->second]++; out.occ_top_r[(size_t)r * (size_t)Mt + (size_t)it->second]++; }
        }
        out.occ_total_r.push_back(terminal[(size_t)r].size()); out.occ_total += terminal[(size_t)r].size();
      }
    }
    for (int M : ms.occ_M) {
      OccRow row; row.M = M; row.M_used = (int)std::min<size_t>((size_t)M, top.size());
      std::unordered_map<Model, int, detail::ModelHash> set;
      std::vector<double> F;
      for (int i = 0; i < row.M_used; ++i) { ModelView S = top.model((size_t)i); set.emplace(Model(S.begin(), S.end()), i); F.push_back(top.v[(size_t)i]); }
      row.log_store_mass = detail::lse(F);
      uint64_t in_all = 0, tot_all = 0; std::vector<uint64_t> in_r, tot_r;
      for (auto& t : terminal) {
        uint64_t in = 0; for (auto& S : t) if (set.count(S)) ++in;
        in_r.push_back(in); tot_r.push_back(t.size()); in_all += in; tot_all += t.size();
      }
      row.occ = (double)in_all / (double)tot_all;
      row.available = in_all > 0;   // review PR16 F5: a zero occupancy gives no estimate (NA), not +Inf
      row.log_Z_occ = row.available ? row.log_store_mass - pm::log(row.occ) : std::numeric_limits<double>::quiet_NaN();
      std::vector<double> finite_r; std::vector<int> used;
      for (int r = 0; r < R; ++r) {
        double o = (double)in_r[r] / (double)tot_r[r];
        row.occ_r.push_back(o);
        if (in_r[r] == 0) { row.n_zero_islands++; row.log_Z_occ_r.push_back(std::numeric_limits<double>::quiet_NaN()); }
        else { double v = row.log_store_mass - pm::log(o); row.log_Z_occ_r.push_back(v); finite_r.push_back(v); used.push_back(r); }
      }
      row.sd_log_Z_occ_r = calib::r_sd(finite_r);   // NaN with fewer than 2 islands
      // Pearson chi-square of the 2 x R'' table (in set / not in set by island) over the islands with nonzero
      // occupancy, df = R'' - 1
      uint64_t in_u = 0, tot_u = 0; for (int r : used) { in_u += in_r[r]; tot_u += tot_r[r]; }
      double pin = tot_u ? (double)in_u / (double)tot_u : 0; double chi = 0;
      if (pin > 0 && pin < 1) for (int r : used) {
        double ein = pin * tot_r[r], eout = (1 - pin) * tot_r[r];
        double oin = (double)in_r[r], oout = (double)(tot_r[r] - in_r[r]);
        chi += (oin - ein) * (oin - ein) / ein + (oout - eout) * (oout - eout) / eout;
      }
      row.chi2_homogeneity = chi; row.chi2_df = std::max(0, (int)used.size() - 1);
      out.occ.push_back(row);
    }
  }
  // near ties (core/v3_run.R:170-173)
  for (size_t i = 0; i < top.size(); ++i) if (top.v[i] >= out.hpm_F - ms.near_tie_eps) { ModelView S = top.model(i); out.near_ties.emplace_back(S.begin(), S.end()); out.near_tie_F.push_back(top.v[i]); }
  out.near_tie_truncated = top.size() >= top.cap && top.size() > 0 && top.v.back() >= out.hpm_F - ms.near_tie_eps;
  // certificates and flags (core/v3_run.R:175-207)
  const LocalArchive& ls = out.local;
  out.local_limit = ls.local_limit;
  bool cert_final = ls.local_certified && out.hpm == ls.returned;
  out.local_certified = cert_final;
  for (int r = 1; r <= R; ++r) if (led.island_best[r] < out.hpm_F - 1) out.E1 = true;
  out.E2 = R >= 2 && calib::r_sd(out.logZ_r) > 1;   // log Z_r finite (pass 1)
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
  for (double e : ess_all) if (e < 0.5 * ms.N) out.low_ESS = true;
  out.checks_passed_final = !(out.E1 || out.E2 || out.E3 || out.low_ESS);
  out.estimates_available = true;
  out.led = std::move(led);
  return out;
}

// In-memory convenience (tests, harness): the same streaming merge over a vector of slots.
template <class Factory>
FitOut merge_and_tail(const std::vector<IslandSlot>& slots, Ledger&& pre, const Model& mode_S, Factory& fac, const MergeSettings& ms,
                      const std::function<bool(double, const std::string&)>& guard = nullptr) {
  VectorSource src(slots);
  return merge_stream(src, std::move(pre), mode_S, fac, ms, guard);
}

}  // namespace merge
}  // namespace v4
