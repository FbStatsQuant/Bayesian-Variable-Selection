// v3_observer.h -- observer instrumentation (CORE_SPEC v2 §8, items 2-4) behind the R11 firewall.
// The observer only READS particle states and score events; it owns no random stream, never writes to the ledger,
// the cache, the particles or the search, and scores (start quantities, o_j(S0,1)) only with its own Scorer instance.
#pragma once
#include "v3_ledger.h"
#include <Rcpp.h>

namespace v3 {

inline int symdiff_count(const std::vector<uint64_t>& a, const std::vector<uint64_t>& b) {
  int c = 0; for (size_t i = 0; i < a.size(); ++i) c += __builtin_popcountll(a[i] ^ b[i]); return c;
}

struct WModel {
  std::string name;
  std::vector<int> S; std::vector<uint64_t> bits; uint64_t h = 0; double logpi0 = NEG_INF;
  bool found = false; EventCtx first; int first_mech = -1;
  std::vector<uint32_t> cnt;  // [phase][mech][island 0..R]
  bool final_iid_hit = false; uint64_t final_iid_count = 0;
  double opp_n[N_PHASE][N_MECH] = {}, opp_h[N_PHASE][N_MECH] = {};
};
struct WSet {
  std::string name;
  std::unordered_multimap<uint64_t, std::vector<uint64_t>> mem;
  bool contains(const std::vector<uint64_t>& bits, uint64_t h) const {
    auto r = mem.equal_range(h);
    for (auto it = r.first; it != r.second; ++it) if (it->second == bits) return true;
    return false;
  }
};

class Observer {
 public:
  const Data* D; const Start* st; const std::vector<std::vector<int>>* Nb;
  int R = 4;
  std::vector<WModel> wm;    // index 0 = truth if supplied; start mode always present
  int truth_idx = -1, mode_idx = -1;
  std::vector<WSet> ws;
  // per-particle round state
  int N = 0;
  std::vector<std::vector<char>> in_start;   // [target][particle] membership at round start (targets = models then sets)
  std::vector<std::vector<char>> in_now;     // current membership of sets (models are recomputed)
  std::vector<std::vector<char>> exited;     // [set][particle] first exit already counted in this round
  std::vector<std::vector<uint64_t>> exit_cnt;  // [set][mech] for the current round
  std::vector<char> prefix_bit;              // T23 bit per particle for the current measured round
  // records (rows)
  std::vector<int> so_island, so_stage, so_when, so_target, so_count;           // stage occupancy
  std::vector<int> so_phase, so_tier, so_iter, ro_tier, ro_iter, se_tier, se_iter;
  std::vector<int> ro_island, ro_phase, ro_stage, ro_round, ro_target, ro_occ_start, ro_occ_end, ro_ii, ro_io, ro_oi, ro_oo;
  std::vector<int> se_island, se_phase, se_stage, se_round, se_set; std::vector<std::vector<uint64_t>> se_cnt;
  std::vector<int> pf_island, pf_round; std::vector<double> pf_Bbar;
  std::vector<std::vector<double>> rb_bad, rb_tot;  // [island][j]
  int T_last = 0;  // number of bridge stages (for "up to the last evidence weight")
  int cur_tier = 0, cur_iter = -1;  // context of the current round (set by the engine before round_end_all)
  double max_oj_dev = NA_REAL;

  Observer(const Data* d, const Start* s, const std::vector<std::vector<int>>* nb, int R_) : D(d), st(s), Nb(nb), R(R_) {
    rb_bad.assign(R + 1, std::vector<double>(d->p, 0.0)); rb_tot.assign(R + 1, std::vector<double>(d->p, 0.0));
  }
  std::vector<std::string> infeasible;   // watched models / truth with |S| > K: skipped and reported (review R-3)
  bool add_model(const std::string& name, const std::vector<int>& S) {
    if ((int)S.size() > D->K) { infeasible.push_back(name); return false; }
    WModel w; w.name = name; w.S = S; w.bits.assign(D->W, 0); w.h = 0;
    for (int j : S) { bit_set(w.bits, j); w.h ^= D->zob.key[j]; }
    w.logpi0 = st->log_pi0(S);
    w.cnt.assign((size_t)N_PHASE * N_MECH * (R + 1), 0);
    wm.push_back(w);
    return true;
  }
  void add_set(const std::string& name, const std::vector<std::vector<int>>& models) {
    WSet s; s.name = name;
    for (auto& S : models) {
      std::vector<uint64_t> b(D->W, 0); uint64_t h = 0;
      for (int j : S) { bit_set(b, j); h ^= D->zob.key[j]; }
      if (!s.contains(b, h)) s.mem.insert({h, b});
    }
    ws.push_back(s);
  }
  int ntargets() const { return (int)(wm.size() + ws.size()); }
  bool member(int t, const std::vector<uint64_t>& bits, uint64_t h) const {
    if (t < (int)wm.size()) return wm[t].h == h && wm[t].bits == bits;
    return ws[t - wm.size()].contains(bits, h);
  }

  // ---- §8.2 scoring ledger of watched models (logical counts, first-score event, final-iid hit) ----
  void on_score(const std::vector<uint64_t>& bits, uint64_t h, const EventCtx& ev, int mech, bool is_held) {
    for (auto& w : wm) {
      if (w.h != h || w.bits != bits) continue;
      int isl = std::min(std::max(ev.island, 0), R);
      w.cnt[((size_t)ev.phase * N_MECH + mech) * (R + 1) + isl]++;
      if (!w.found && !is_held) { w.found = true; w.first = ev; w.first_mech = mech; }
      bool final_phase = ev.phase == PH_FINAL_INIT || ev.phase == PH_FINAL_BRIDGE || ev.phase == PH_BURN_IN || ev.phase == PH_MEASURED;
      if (final_phase && (mech == ME_INIT || mech == ME_INDEP)) { w.final_iid_hit = true; w.final_iid_count++; }
    }
  }

  // ---- §8.2 opportunities before the first score (inclusive of the successful one) ----
  // kind: ME_GIBBS_FLIP (a Gibbs execution at j; recorded under gibbs_flip), ME_USWAP, ME_NSWAP, ME_INDEP, ME_INIT, executed from pre-state (S, bits).
  void opportunity(const std::vector<int>& S, const std::vector<uint64_t>& bits, int kind, int j, const EventCtx& ev) {
    int p = D->p, k = (int)S.size();
    for (auto& w : wm) {
      if (w.found) continue;
      double haz = 0; bool opp = false;
      if (kind == ME_GIBBS_FLIP) {
        int dd = symdiff_count(bits, w.bits);
        opp = (dd == 0) || (dd == 1 && bit_get(bits, j) != bit_get(w.bits, j));
        haz = 1.0;  // under SR both configurations are scored
      } else if (kind == ME_USWAP) {
        if (k > 0 && k < p && (int)w.S.size() == k && symdiff_count(bits, w.bits) == 2) { opp = true; haz = 1.0 / ((double)k * (p - k)); }
      } else if (kind == ME_NSWAP) {
        if (k > 0 && (int)w.S.size() == k && symdiff_count(bits, w.bits) == 2) {
          int jo = -1, li = -1;
          for (int a : S) if (!bit_get(w.bits, a)) jo = a;
          for (int a : w.S) if (!bit_get(bits, a)) li = a;
          const auto& nj = (*Nb)[jo];
          if (std::binary_search(nj.begin(), nj.end(), li)) {
            int cnt = 0; for (int l : nj) if (!bit_get(bits, l)) ++cnt;
            opp = true; haz = 1.0 / ((double)k * cnt);
          }
        }
      } else if (kind == ME_INDEP || kind == ME_INIT) {
        opp = true; haz = std::exp(w.logpi0);
      } else if (kind == ME_LOCAL) {
        int dd = symdiff_count(bits, w.bits);
        opp = (dd == 1) || (dd == 2 && (int)w.S.size() == k);
        haz = 1.0;
      }
      if (opp) { w.opp_n[ev.phase][kind] += 1; w.opp_h[ev.phase][kind] += haz; }
    }
  }

  // ---- §8.3 per stage: occupancy after resampling (when = 0) and after the move round (when = 1) ----
  template <class PVec> void stage_occupancy(int island, int stage, int when, const PVec& P, const EventCtx& ev) {
    for (int t = 0; t < ntargets(); ++t) {
      int c = 0; for (auto& q : P) if (member(t, q.bits, q.h)) ++c;
      so_island.push_back(island); so_stage.push_back(stage); so_when.push_back(when); so_target.push_back(t); so_count.push_back(c);
      so_phase.push_back(ev.phase); so_tier.push_back(ev.tier); so_iter.push_back(ev.iter);
    }
  }
  // ---- §8.3 / §8.4 round hooks ----
  template <class PVec> void round_begin_all(const PVec& P) {
    N = (int)P.size(); int nt = ntargets();
    in_start.assign(nt, std::vector<char>(N, 0)); in_now.assign(ws.size(), std::vector<char>(N, 0));
    exited.assign(ws.size(), std::vector<char>(N, 0)); exit_cnt.assign(ws.size(), std::vector<uint64_t>(N_MECH, 0));
    prefix_bit.assign(N, 0);
    for (int t = 0; t < nt; ++t) for (int i = 0; i < N; ++i) in_start[t][i] = member(t, P[i].bits, P[i].h);
    for (size_t s = 0; s < ws.size(); ++s) for (int i = 0; i < N; ++i) in_now[s][i] = in_start[wm.size() + s][i];
    if (truth_idx >= 0) for (int i = 0; i < N; ++i) prefix_bit[i] = !in_start[truth_idx][i];
  }
  // after every elementary step of particle i (0-based), mechanism `mech` (state may or may not have changed)
  void post_step(int i, const std::vector<uint64_t>& bits, uint64_t h, int mech) {
    for (size_t s = 0; s < ws.size(); ++s) {
      bool now = ws[s].contains(bits, h);
      if (in_now[s][i] && !now && !exited[s][i]) { exited[s][i] = 1; exit_cnt[s][mech]++; }
      in_now[s][i] = now;
    }
    if (truth_idx >= 0 && !prefix_bit[i]) {
      const WModel& w = wm[truth_idx];
      if (!(w.h == h && w.bits == bits)) prefix_bit[i] = 1;
    }
  }
  // RB recording at a Gibbs step j in a measured round, pre-state bits: is X_pre-j \ {j} != S0 \ {j}?
  void rb_record(int island, int j, const std::vector<uint64_t>& bits) {
    if (truth_idx < 0) return;
    const WModel& w = wm[truth_idx];
    int dd = symdiff_count(bits, w.bits);
    bool same = (dd == 0) || (dd == 1 && bit_get(bits, j) != bit_get(w.bits, j));
    rb_tot[island][j] += 1; if (!same) rb_bad[island][j] += 1;
  }
  template <class PVec> void round_end_all(int island, int phase, int stage, int round, const PVec& P) {
    int nt = ntargets();
    for (int t = 0; t < nt; ++t) {
      int os = 0, oe = 0, ii = 0, io = 0, oi = 0, oo = 0;
      for (int i = 0; i < N; ++i) {
        bool a = in_start[t][i], b = member(t, P[i].bits, P[i].h);
        os += a; oe += b; if (a && b) ++ii; else if (a) ++io; else if (b) ++oi; else ++oo;
      }
      ro_island.push_back(island); ro_phase.push_back(phase); ro_stage.push_back(stage); ro_round.push_back(round);
      ro_tier.push_back(cur_tier); ro_iter.push_back(cur_iter);
      ro_target.push_back(t); ro_occ_start.push_back(os); ro_occ_end.push_back(oe);
      ro_ii.push_back(ii); ro_io.push_back(io); ro_oi.push_back(oi); ro_oo.push_back(oo);
    }
    for (size_t s = 0; s < ws.size(); ++s) {
      se_island.push_back(island); se_phase.push_back(phase); se_stage.push_back(stage); se_round.push_back(round);
      se_tier.push_back(cur_tier); se_iter.push_back(cur_iter);
      se_set.push_back((int)s); se_cnt.push_back(exit_cnt[s]);
    }
    if (phase == PH_MEASURED && truth_idx >= 0) {
      double b = 0; for (int i = 0; i < N; ++i) b += prefix_bit[i];
      pf_island.push_back(island); pf_round.push_back(round); pf_Bbar.push_back(b / N);
    }
  }

  Rcpp::List to_list() const;
};

// Ledger::event (declared in v3_ledger.h).
inline void Ledger::event(const std::vector<int>& S, double F, double lg0, double logm, bool is_fresh, bool is_held,
                          const EventCtx& ev, int mech) {
  logical[ev.phase][mech]++;
  if (is_fresh) fresh[ev.phase][mech]++;
  bool own = ev.island >= 1 && ev.island <= islands &&
             (ev.phase == PH_FINAL_INIT || ev.phase == PH_FINAL_BRIDGE || ev.phase == PH_BURN_IN || ev.phase == PH_MEASURED ||
              ev.phase == PH_PILOT || ev.phase == PH_DIAG);
  if (own && F > island_best[ev.island]) island_best[ev.island] = F;
  if (is_fresh) offer_stores(S, F, lg0, logm, ev, mech);
  if (dump) {
    auto it = dumpmap.find(S);
    if (it == dumpmap.end()) {
      DumpRec r; r.F = F; r.logm = logm; r.lg0 = lg0; r.first = ev; r.first_mech = mech;
      it = dumpmap.emplace(S, r).first;
    }
    it->second.cnt[ev.phase][mech]++;
  }
}

}  // namespace v3
