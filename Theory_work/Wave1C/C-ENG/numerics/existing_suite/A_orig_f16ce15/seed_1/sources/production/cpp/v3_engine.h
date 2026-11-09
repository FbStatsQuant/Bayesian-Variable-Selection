// v3_engine.h -- particles, variate sources, the four elementary steps, the random-order round,
// one final island (bridge + burn-in + measured rounds), local search.
// CORE_SPEC v2 §§4, 4.1, 5, 6, 7; M §§6.5, 6.6 (resampling), 6.8, 6.10, 6.11, 6.12; rulings R1, R4, R7, R8.
#pragma once
#include "v3_ledger.h"
#include "v3_runtime.h"
#include "v3_calib.h"

namespace v3 {

struct Particle {
  std::vector<int> S; std::vector<uint64_t> bits; uint64_t h = 0;
  double logm = 0, lg0 = 0, d = 0, F = 0;
  inline double lgphi(double phi) const { return lg0 + phi * d; }  // log gamma_phi(S) = log gamma_0(S) + phi d(S)
};

// ---------------------------------------------------------------------------------------------
// Variate sources (CORE_SPEC §4.1, §5)
// ---------------------------------------------------------------------------------------------
struct RngSource : public VariateSource {
  Xoshiro256ss g;
  double u(const char*) override { return g.uniform(); }
};
// Per-stage move statistics (acceptance per mechanism; CORE_SPEC §6 per-stage table).
struct MoveStats {
  uint64_t gibbs = 0, gibbs_change = 0, us_exec = 0, us_acc = 0, us_self = 0, ns_exec = 0, ns_acc = 0, ns_noscore = 0, ns_self = 0,
           in_exec = 0, in_acc = 0;
};

struct IslandResult {
  int phase = PH_FINAL_BRIDGE, tier = 0, iter = -1, island = 0;
  bool partial = false;
  double logZ = NEG_INF;
  std::vector<double> phi, inc, ess, cum;
  std::vector<int> distinct_resampled, distinct_moved;
  std::vector<MoveStats> stage_moves;        // bridge stages 1..T
  std::vector<MoveStats> terminal_moves;     // burn-in rounds then measured rounds
  std::vector<int> terminal_distinct;
  std::vector<double> pip, rb_acc;
  std::vector<std::vector<double>> rb_round; // per measured round accumulator (sum of o_j)
  int forced = 0;                            // pilot: forced (floor) steps
  uint64_t init_hash = 0;                    // hash of the initial draws (particle order; R6 instrumentation)
  double seconds_init = 0, seconds_bridge = 0, seconds_burn = 0, seconds_measured = 0;
};

struct LocalArchive {
  std::vector<int> centre; double centre_F = 0;
  std::vector<std::vector<int>> path; std::vector<double> path_F;
  std::vector<std::vector<int>> scanned; std::vector<double> scanned_F; std::vector<int> scan_complete, scan_size;
  std::string termination; bool local_limit = false, local_certified = false;
  std::vector<int> returned; double returned_F = 0;
  int moves = 0; long n_eval = 0;
};

using Clock = std::chrono::steady_clock;
inline double secs_since(Clock::time_point t0) { return std::chrono::duration<double>(Clock::now() - t0).count(); }

class Engine {
 public:
  const Data& D; const Start& st; const std::vector<std::vector<int>>& Nb; int B;
  Scorer sc;
  ScoreCache* cache = nullptr; Ledger* led = nullptr; RuntimeGuard* guard = nullptr;
  VariateSource* vs = nullptr;
  EventCtx ev;
  MoveStats ms;
  bool rb_on = false; std::vector<double> rb_acc;
  std::vector<std::pair<int,int>> scratch;
  Particle tmpQ;

  Engine(const Data& d, const Start& s, const std::vector<std::vector<int>>& nb, int B_) : D(d), st(s), Nb(nb), B(B_), sc(&d) {}

  int nlabels() const { return D.p + B + 2; }
  std::string label_name(int lab) const {
    if (lab < D.p) return "G" + std::to_string(D.orig[lab]);
    if (lab == D.p) return "U";
    if (lab <= D.p + B) return "N" + std::to_string(lab - D.p);
    return "I";
  }

  void set_model(Particle& q, const std::vector<int>& S) {
    q.S = S; q.bits.assign(D.W, 0); q.h = 0;
    for (int j : S) { bit_set(q.bits, j); q.h ^= D.zob.key[j]; }
  }
  inline void add_var(Particle& q, int j) { sorted_insert(q.S, j); bit_flip(q.bits, j); q.h ^= D.zob.key[j]; }
  inline void del_var(Particle& q, int j) { sorted_erase(q.S, j); bit_flip(q.bits, j); q.h ^= D.zob.key[j]; }

  // Score a model (cache, then the scorer) and fill log m, log gamma_0, d, F. Emits one logical score event.
  // d(S) = log BF(S) - sum_b log r_b(S n C_b) (M §6.3); F = log varpi(|S|) + log m(S).
  void eval(Particle& q, int mech, bool emit = true) {
    double lm; bool fresh = false;
    if (!(cache && cache->find(q.S, q.h, lm))) {
      ScoreOut o = sc.score(q.S); lm = o.logm; fresh = true;
      if (cache) cache->insert(q.S, q.h, lm);
    }
    double c = st.comp(q.S, scratch);
    int k = (int)q.S.size();
    q.logm = lm; q.lg0 = D.logprior[k] + c; q.d = (lm - D.logm0) - c; q.F = D.logprior[k] + lm;
    if (emit) {
      if (led) led->event(q.S, q.F, q.lg0, q.logm, fresh || !cache, false, ev, mech);
    }
  }
  // The current state counted as scored without re-evaluation (SR: both Gibbs configurations count as scored).
  void held(const Particle& q, int mech) {
    if (led) led->event(q.S, q.F, q.lg0, q.logm, false, true, ev, mech);
  }

  // Exact pi_0 draw
  void draw_start(std::vector<int>& S) { draw_pi0(st, *vs, S); }

  // ---- Elementary steps (M §6.5, R1, CORE_SPEC §4.1) ----
  // Gibbs coordinate j: o_j = a/(1+a), a = gamma_phi(S u j)/gamma_phi(S \ j); o_j = 0 if |S \ j| = K (R1).
  // Both feasible configurations count as scored (SR). One uniform: include iff u < o_j.
  void step_gibbs(Particle& P, int j, double phi) {
    MoveStats& m = ms; m.gibbs++;
    bool in = bit_get(P.bits, j);
    bool add_ok = in || (int)P.S.size() < D.K;
    double oj = 0; bool has_other = false;
    held(P, ME_GIBBS_HELD);
    if (in || add_ok) {
      tmpQ = P;
      if (in) del_var(tmpQ, j); else add_var(tmpQ, j);
      eval(tmpQ, ME_GIBBS_FLIP);
      has_other = true;
      double lw = in ? P.lgphi(phi) : tmpQ.lgphi(phi);
      double lo = in ? tmpQ.lgphi(phi) : P.lgphi(phi);
      oj = plogis_log(lw - lo);
    }
    if (rb_on) rb_acc[j] += oj;  // R8: recorded before the draw
    double u = vs->u("gibbs");
    bool include = u < oj;
    if (include != in) { P = tmpQ; m.gibbs_change++; }
  }
  // m-th (0-based) non-member in increasing index order (word-level popcount skip).
  int nth_nonmember(const std::vector<uint64_t>& bits, int m) const {
    for (int w = 0; w < D.W; ++w) {
      uint64_t word = ~bits[w];
      int valid = std::min(64, D.p - 64 * w);
      if (valid < 64) word &= ((1ULL << valid) - 1);
      int c = __builtin_popcountll(word);
      if (m < c) { for (int t = 0; t < m; ++t) word &= word - 1; return 64 * w + __builtin_ctzll(word); }
      m -= c;
    }
    throw std::runtime_error("nth_nonmember out of range");
  }
  // Uniform swap: self-loop if |S| in {0, p}; j uniform in S, l uniform outside S; accept w.p. 1 ^ gamma_phi(S')/gamma_phi(S).
  void step_uswap(Particle& P, double phi) {
    int k = (int)P.S.size(), p = D.p;
    if (k == 0 || k == p) { ms.us_self++; return; }
    ms.us_exec++;
    int j = P.S[(int)std::floor(vs->u("uswap_j") * k)];
    int l = nth_nonmember(P.bits, (int)std::floor(vs->u("uswap_l") * (p - k)));
    tmpQ = P; del_var(tmpQ, j); add_var(tmpQ, l);
    eval(tmpQ, ME_USWAP);
    double la = tmpQ.lgphi(phi) - P.lgphi(phi);
    double alpha = (la >= 0) ? 1.0 : std::exp(la);
    double u = vs->u("uswap_accept");
    bool acc = u < alpha;
    if (acc) { P = tmpQ; ms.us_acc++; }
  }
  // Neighbour swap (label N<b>): self-loop at empty S; j uniform in S; reject without score if N(j)\S is empty;
  // l uniform in N(j)\S; accept w.p. 1 ^ [gamma_phi(S')/gamma_phi(S)] |N(j)\S| / |N(l)\S'|.
  void step_nswap(Particle& P, double phi, int b) {
    int k = (int)P.S.size();
    std::string lab = "N" + std::to_string(b);
    if (k == 0) { ms.ns_self++; return; }
    ms.ns_exec++;
    int j = P.S[(int)std::floor(vs->u("nswap_j") * k)];
    std::vector<int> cand;
    for (int l : Nb[j]) if (!bit_get(P.bits, l)) cand.push_back(l);
    if (cand.empty()) { ms.ns_noscore++; return; }
    int l = cand[(int)std::floor(vs->u("nswap_l") * cand.size())];
    tmpQ = P; del_var(tmpQ, j); add_var(tmpQ, l);
    int back = 0; for (int x : Nb[l]) if (!bit_get(tmpQ.bits, x)) ++back;  // |N(l) \ S'| >= 1 (j is in it)
    eval(tmpQ, ME_NSWAP);
    double la = tmpQ.lgphi(phi) - P.lgphi(phi) + std::log((double)cand.size()) - std::log((double)back);
    double alpha = (la >= 0) ? 1.0 : std::exp(la);
    double u = vs->u("nswap_accept");
    bool acc = u < alpha;
    if (acc) { P = tmpQ; ms.ns_acc++; }
  }
  // Independence proposal S' ~ pi_0 (exact draw), accepted w.p. 1 ^ exp{phi [d(S') - d(S)]}.
  void step_indep(Particle& P, double phi) {
    ms.in_exec++;
    std::vector<int> S; draw_start(S);
    set_model(tmpQ, S);
    eval(tmpQ, ME_INDEP);
    double la = phi * (tmpQ.d - P.d);
    double alpha = (la >= 0) ? 1.0 : std::exp(la);
    double u = vs->u("indep_accept");
    bool acc = u < alpha;
    if (acc) { P = tmpQ; ms.in_acc++; }
  }
  // Round order: uniformly random permutation of the m labels (canonical list G1..Gp, U, N1..NB, I) by Fisher-Yates:
  // for i = m down to 2 (1-based): j = floor(u i) + 1, swap positions i and j  (m - 1 uniforms, purpose "order").
  void draw_order(std::vector<int>& ord) {
    int m = nlabels();
    ord.resize(m);
    for (int i = 0; i < m; ++i) ord[i] = i;
    for (int i = m - 1; i >= 1; --i) { int jj = (int)std::floor(vs->u("order") * (i + 1)); std::swap(ord[i], ord[jj]); }
  }
  // One round of the m = p + B + 2 labelled steps in a fresh random order (M §6.5).
  void one_round(Particle& P, int i, double phi) {
    std::vector<int> ord; draw_order(ord);
    int p = D.p;
    for (size_t pos = 0; pos < ord.size(); ++pos) {
      ev.position = (int)pos + 1;
      int lab = ord[pos], mech;
      if (lab < p) { step_gibbs(P, lab, phi); mech = ME_GIBBS_FLIP; }
      else if (lab == p) { step_uswap(P, phi); mech = ME_USWAP; }
      else if (lab <= p + B) { step_nswap(P, phi, lab - p); mech = ME_NSWAP; }
      else { step_indep(P, phi); mech = ME_INDEP; }
    }
    ev.position = 0;
  }
  void population_round(std::vector<Particle>& P, double phi) {
    for (size_t i = 0; i < P.size(); ++i) { ev.particle = (int)i + 1; one_round(P[i], (int)i, phi); }
    ev.particle = 0;
  }
  static int distinct(const std::vector<Particle>& P) {
    std::unordered_map<uint64_t, std::vector<const std::vector<uint64_t>*>> seen;
    int c = 0;
    for (auto& q : P) {
      auto& v = seen[q.h]; bool f = false;
      for (auto* b : v) if (*b == q.bits) { f = true; break; }
      if (!f) { v.push_back(&q.bits); ++c; }
    }
    return c;
  }

  // Multinomial resampling (M §6.6; CORE_SPEC §4.1): N uniforms u_1..u_N (purpose "resample"); ancestor i is the
  // smallest k with cumulative normalised weight W_k >= u_i; W_k = c_k / c_N with c_k = sum_{i<=k} exp(lw_i - max lw),
  // and W_N set to 1 exactly. Guard (code review R-7): u_i = 0 is replaced by the smallest positive double, so a
  // particle whose normalised weight is 0 (W_k = W_{k-1}) is never selected; for u_i > 0 the rule is unchanged.
  std::vector<int> resample(const std::vector<double>& lw) {
    int N = (int)lw.size();
    double mx = NEG_INF; for (double v : lw) mx = std::max(mx, v);
    std::vector<double> W(N); double c = 0;
    for (int i = 0; i < N; ++i) { c += std::exp(lw[i] - mx); W[i] = c; }
    for (int i = 0; i < N; ++i) W[i] /= c;
    W[N - 1] = 1.0;
    // Chen-Asau guide table: monotone O(N) construction, O(1) expected lookup.
    std::vector<int> guide(N); int k = 0;
    for (int b = 0; b < N; ++b) {
      double boundary = (double)b / (double)N;
      while (k < N - 1 && W[k] < boundary) ++k;
      guide[b] = k;
    }
    std::vector<int> a(N);
    for (int i = 0; i < N; ++i) {
      double u = vs->u("resample");
      double ue = (u > 0) ? u : std::numeric_limits<double>::denorm_min();
      int bucket = std::min(N - 1, (int)std::floor(ue * (double)N));
      int k = guide[bucket];
      while (k < N - 1 && W[k] < ue) ++k;
      while (k > 0 && W[k - 1] >= ue) --k;  // repeated backward adjustment, including zero-weight runs
      a[i] = k;
    }
    return a;
  }

  // One island (M §6.8 final and diagnostic islands; M §6.6 pilot; R7, R8): N iid pi_0 draws (or supplied states,
  // stages t = 1..T with weights exp{(phi_t - phi_{t-1}) d(S^{(t-1)})}, log increment before resampling,
  // multinomial resampling after every reweighting, one round at phi_t; then L burn-in and Hm measured rounds at
  // phi = 1 with RB recording. log Zhat_r = log m(empty) + log Zbar_0 + sum_t log increment_t (M §6.12).
  // Schedule: a fixed grid, or the adaptive pilot rule (pilot_next_phi on the current population's d, threshold 0.9 H,
  // floor 1/T_e, ends exactly at 1). phase_override >= 0 labels every event of the island with that phase
  // (calibration: pilot or diag); measured rounds are then numbered L+1..L+Hm so that they stay distinguishable.
  struct Schedule { const std::vector<double>* grid = nullptr; bool adaptive = false; double H = 0; int Te = 1; };
  IslandResult run_island(int r, int N, const std::vector<double>& grid, int L, int Hm, int tier,
                          const std::vector<std::vector<int>>* init_states) {
    Schedule sch; sch.grid = &grid;
    return run_island_s(r, N, sch, L, Hm, tier, init_states, -1, -1);
  }
  IslandResult run_island_s(int r, int N, const Schedule& sch, int L, int Hm, int tier,
                            const std::vector<std::vector<int>>* init_states, int phase_override, int iter) {
    IslandResult res;
    res.phase = phase_override >= 0 ? phase_override : PH_FINAL_BRIDGE;
    res.tier = tier; res.iter = iter; res.island = r;
    int p = D.p;
    int T = sch.adaptive ? 0 : (int)sch.grid->size() - 1;
    auto PH = [&](int ph) { return phase_override >= 0 ? phase_override : ph; };
    ev = EventCtx(); ev.island = r; ev.tier = tier; ev.iter = iter;
    std::vector<Particle> P(N);
    auto t0 = Clock::now();
    ev.phase = PH(PH_FINAL_INIT); ev.stage = 0; ev.round = 0; ev.phi = 0;
    for (int i = 0; i < N; ++i) {
      ev.particle = i + 1; ev.position = 0;
      std::vector<int> S;
      if (init_states) S = (*init_states)[i]; else draw_start(S);
      set_model(P[i], S);
      eval(P[i], ME_INIT);
    }
    ev.particle = 0;
    // hash of the initial population: h <- SplitMix64(h xor Zobrist(S_i) xor i), i = 1..N (instrumentation only)
    { uint64_t hh = 0x243F6A8885A308D3ULL;
      for (int i = 0; i < N; ++i) { uint64_t x = hh ^ P[i].h ^ (uint64_t)(i + 1); hh = splitmix64(x); }
      res.init_hash = hh; }
    res.seconds_init = secs_since(t0); t0 = Clock::now();
    double logZ = D.logm0 + st.logZbar0;
    std::vector<double> lw(N), dvec(N);
    double phi_prev = 0.0;
    int t = 0;
    while (true) {
      auto stage_start = Clock::now();
      double phi_new;
      if (!sch.adaptive) {
        if (t >= T) break;
        phi_prev = (*sch.grid)[t]; phi_new = (*sch.grid)[t + 1];
      } else {
        if (phi_prev == 1.0) break;
        for (int i = 0; i < N; ++i) dvec[i] = P[i].d;
        NextPhi np = pilot_next_phi(dvec, phi_prev, sch.H, sch.Te);
        phi_new = np.phi; if (np.forced) res.forced++;
      }
      ++t;
      double dphi = phi_new - phi_prev;
      for (int i = 0; i < N; ++i) lw[i] = dphi * P[i].d;
      double lse = log_sum_exp(lw);
      double inc = lse - std::log((double)N);
      std::vector<double> lw2(N); for (int i = 0; i < N; ++i) lw2[i] = 2 * lw[i];
      double ess = std::exp(2 * lse - log_sum_exp(lw2));   // (sum w)^2 / sum w^2
      logZ += inc;
      ev.phase = PH(PH_FINAL_BRIDGE); ev.stage = t; ev.round = t; ev.phi = phi_new;
      std::vector<int> a = resample(lw);
      std::vector<Particle> Pn(N);
      for (int i = 0; i < N; ++i) Pn[i] = P[a[i]];
      P.swap(Pn);
      res.phi.push_back(phi_new); res.inc.push_back(inc); res.ess.push_back(ess); res.cum.push_back(logZ);
      res.distinct_resampled.push_back(distinct(P));
      ms = MoveStats();
      population_round(P, phi_new);
      res.stage_moves.push_back(ms);
      res.distinct_moved.push_back(distinct(P));
      phi_prev = phi_new;
      if (guard && guard->check(secs_since(stage_start), "bridge_stage", ev)) {
        res.partial = true; res.logZ = logZ; res.seconds_bridge = secs_since(t0);
        ev = EventCtx(); return res;
      }
    }
    T = t;
    res.seconds_bridge = secs_since(t0); t0 = Clock::now();
    ev.phase = PH(PH_BURN_IN); ev.stage = T; ev.phi = 1.0;
    for (int l = 1; l <= L; ++l) {
      ev.round = l; ms = MoveStats();
      population_round(P, 1.0);
      res.terminal_moves.push_back(ms); res.terminal_distinct.push_back(distinct(P));
    }
    res.seconds_burn = secs_since(t0); t0 = Clock::now();
    ev.phase = PH(PH_MEASURED);
    rb_acc.assign(p, 0.0);
    for (int h = 1; h <= Hm; ++h) {
      ev.round = phase_override >= 0 ? L + h : h; ms = MoveStats();
      std::vector<double> before = rb_acc;
      rb_on = true;
      population_round(P, 1.0);
      rb_on = false;
      std::vector<double> diff(p); for (int j = 0; j < p; ++j) diff[j] = rb_acc[j] - before[j];
      res.rb_round.push_back(diff);
      res.terminal_moves.push_back(ms); res.terminal_distinct.push_back(distinct(P));
    }
    res.seconds_measured = secs_since(t0);
    res.rb_acc = rb_acc;
    res.pip.assign(p, 0.0);
    for (int j = 0; j < p; ++j) res.pip[j] = rb_acc[j] / ((double)N * Hm);  // PIP_rj = mean over particles and rounds
    res.logZ = logZ;
    ev = EventCtx();
    return res;
  }

  // Local search (M §6.10; R4; lead ruling R14): from the centre, scan every feasible flip (additions beyond K
  // excluded) and every swap with the centre frozen; the best neighbour is the one with the largest F, exact F ties
  // broken by the plain lexicographic order (proper prefix first). It is an improvement only if its F is strictly
  // larger than the centre's F (an exact-F tie is not a move). At most `ell` moves, then one further scan;
  // local_limit iff that scan still finds a strict F improvement. Every scanned model still updates the HPM running
  // best through the ledger (HPM tie rule), so an exact-tie neighbour can become the HPM without being a move.
  // Scan order: flips j = 1..p, then swaps (j in S ascending) x (l outside S ascending).
  // The search never alters particles. Every evaluated model is a score event (phase local, mechanism local_scan).
  LocalArchive local_search(const std::vector<int>& centre, int ell, int tier, bool emit_centre, int iter = -1) {
    LocalArchive A;
    ev = EventCtx(); ev.phase = PH_LOCAL; ev.tier = tier; ev.island = 0; ev.phi = 1.0; ev.iter = iter;
    Particle C; set_model(C, centre); eval(C, ME_LOCAL, emit_centre);
    A.centre = C.S; A.centre_F = C.F;
    int p = D.p, K = D.K;
    while (true) {
      ev.round = A.moves; ev.stage = (int)A.scanned.size() + 1;
      bool have = false; Particle best, Q;
      int pos = 0;
      auto consider = [&](Particle& q) {
        ev.position = ++pos;
        eval(q, ME_LOCAL); A.n_eval++;
        if (!have || q.F > best.F || (q.F == best.F && lex_less(q.S, best.S))) { best = q; have = true; }
      };
      for (int j = 0; j < p; ++j) {
        Q = C;
        if (bit_get(C.bits, j)) del_var(Q, j);
        else { if ((int)C.S.size() >= K) continue; add_var(Q, j); }
        consider(Q);
      }
      std::vector<int> CS = C.S;
      for (int j : CS)
        for (int l = 0; l < p; ++l) {
          if (bit_get(C.bits, l)) continue;
          Q = C; del_var(Q, j); add_var(Q, l);
          consider(Q);
        }
      A.scanned.push_back(C.S); A.scanned_F.push_back(C.F); A.scan_complete.push_back(1); A.scan_size.push_back(pos);
      if (have && best.F > C.F) {  // strict F improvement only (R14)
        if (A.moves >= ell) {
          A.local_limit = true; A.termination = "move_limit"; A.returned = best.S; A.returned_F = best.F; break;
        }
        C = best; A.moves++; A.path.push_back(C.S); A.path_F.push_back(C.F);
      } else {
        A.termination = "no_improvement"; A.local_certified = true; A.returned = C.S; A.returned_F = C.F; break;
      }
    }
    ev = EventCtx();
    return A;
  }
};

}  // namespace v3
