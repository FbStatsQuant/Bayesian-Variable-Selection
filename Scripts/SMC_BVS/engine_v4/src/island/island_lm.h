// island_lm.h -- the label-major round for a group of particles (member function of IslandEngine, declared in
// island_run.h; its group state is island_lm_state.h). Same outputs as the particle-major reference (T3).
#pragma once
#include "island_run.h"

namespace v4::island {

// ---- K1 helpers (bounded scoring; WP3_ARCH_REVIEW §2.1, prototype exp/P1M-wp3-arch 88fa644a / 0c98bea3) ---------
// bit l set iff lo < pos[l] < hi, for 16 positions (AVX-512: two unsigned compares)
static inline uint32_t lm_in_open_range16(const uint32_t* pos, uint32_t lo, uint32_t hi) {
#if defined(__AVX512F__)
  const __m512i v = _mm512_loadu_si512((const void*)pos);
  return (uint32_t)(_mm512_cmpgt_epu32_mask(v, _mm512_set1_epi32((int)lo)) & _mm512_cmplt_epu32_mask(v, _mm512_set1_epi32((int)hi)));
#else
  uint32_t r = 0; for (int l = 0; l < 16; ++l) r |= (uint32_t)((pos[l] > lo) & (pos[l] < hi)) << l; return r;
#endif
}
// the labels jj of a tile (nbv of them, positions pos[jj]) with lo < pos[jj] < hi, OR-ed into the bit words w
static inline void lm_or_range_bits(const uint32_t* pos, int nbv, uint32_t lo, uint32_t hi, uint64_t* w) {
  int jj = 0;
  for (; jj + 16 <= nbv; jj += 16) w[jj >> 6] |= (uint64_t)lm_in_open_range16(pos + jj, lo, hi) << (jj & 63);
  for (; jj < nbv; ++jj) w[jj >> 6] |= (uint64_t)((pos[jj] > lo) & (pos[jj] < hi)) << (jj & 63);
}
// clears the members' bits (their values are the cached deletions) and lists the set bits in ascending order
static inline int lm_list_bits(uint64_t* w, int nw, const int32_t* mlo, const int32_t* mhi, int j0, int* out) {
  for (const int32_t* it = mlo; it != mhi; ++it) w[(*it - j0) >> 6] &= ~(1ull << ((*it - j0) & 63));
  int cnt = 0;
  for (int k = 0; k < nw; ++k) for (uint64_t b = w[k]; b; b &= b - 1) out[cnt++] = k * 64 + __builtin_ctzll(b);
  return cnt;
}
// NaN-row test (tests only): a quiet NaN with a payload no computation produces from non-poisoned inputs
static constexpr uint64_t LM_POISON_BITS = 0x7FFBADC0FFEE0BADull;
static inline bool lm_poisoned(double x) { uint64_t b; std::memcpy(&b, &x, 8); return b == LM_POISON_BITS; }

template <Arith A>
void IslandEngine<A>::lm_group(int g0, int gN, const RoundCtx& rc) {
  auto& KS = res.ks;
  auto t0 = std::chrono::steady_clock::now();
  auto lap = [&](double& acc) { auto t1 = std::chrono::steady_clock::now(); acc += std::chrono::duration<double>(t1 - t0).count(); t0 = t1; };
  gb.ord.resize((size_t)gN * m); gb.inv.resize((size_t)gN * m); gb.ng.assign(gN, {});
  #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
  for (int gi = 0; gi < gN; ++gi) oom_guard([&] {
    uint32_t* ord = &gb.ord[(size_t)gi * m]; uint32_t* inv = &gb.inv[(size_t)gi * m];
    draw_order(rc, g0 + gi, ord);
    for (int t = 0; t < m; ++t) { if (t + 16 < m) __builtin_prefetch(&inv[ord[t + 16]], 1); inv[ord[t]] = (uint32_t)t + 1; }   // 1-based positions
    for (int lab = p; lab < m; ++lab) gb.ng[gi].push_back({inv[lab], lab});
    std::sort(gb.ng[gi].begin(), gb.ng[gi].end());
  });
  if (fail_fatal()) return;
  gb.q.assign(gN, 0); gb.e.assign(gN, 0); gb.done.assign(gN, 0); gb.etype.assign(gN, 0); gb.pending.assign(gN, Particle());
  std::vector<std::atomic<uint32_t>> fm(gN); gb.fmin.swap(fm);
  KS.particle_rounds += gN;
  lap(KS.t_orders);
  std::vector<int> active;
  while (true) {
    active.clear(); for (int gi = 0; gi < gN; ++gi) if (!gb.done[gi]) active.push_back(gi);
    if (active.empty()) break;
    KS.passes++; KS.particle_sweeps += active.size();
    // distinct supports: (hash, log m bits, S)  [class A: one model can carry different path values]
    std::vector<int> idx = active;
    auto lmbits = [&](int gi) { uint64_t b; std::memcpy(&b, &P[g0 + gi].logm, 8); return b; };
    std::sort(idx.begin(), idx.end(), [&](int a, int b) {
      const Particle &x = P[g0 + a], &y = P[g0 + b];
      if (x.h != y.h) return x.h < y.h;
      if (lmbits(a) != lmbits(b)) return lmbits(a) < lmbits(b);
      if (x.S != y.S) return lex_less(x.S, y.S);
      return a < b;
    });
    gb.sup_of.assign(gN, -1); gb.sup_parts.clear();
    std::vector<int> rep;
    for (size_t t = 0; t < idx.size(); ++t) {
      int gi = idx[t];
      if (t == 0 || P[g0 + gi].h != P[g0 + idx[t - 1]].h || lmbits(gi) != lmbits(idx[t - 1]) || P[g0 + gi].S != P[g0 + idx[t - 1]].S) {
        rep.push_back(gi); gb.sup_parts.push_back({});
      }
      gb.sup_of[gi] = (int)rep.size() - 1; gb.sup_parts.back().push_back(gi);
    }
    for (auto& v : gb.sup_parts) std::sort(v.begin(), v.end());
    const int nsup = (int)rep.size();
    KS.supports += nsup; KS.support_label_pairs += (uint64_t)nsup * p;
    if ((int)gb.sup.size() < nsup) gb.sup.resize(nsup);
    #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
    for (int s = 0; s < nsup; ++s) oom_guard([&] {
      const Particle& x = P[g0 + rep[s]];
      build_support(D, st, *scorers[omp_get_thread_num()], gb.sup[s], x.S, x.h, x.logm, x.lg0, x.d, rc.phi);
    });
    if (fail_fatal()) return;
    // active columns: members of fast supports that can add
    gb.act.clear();
    for (int s = 0; s < nsup; ++s) { auto& c = gb.sup[s]; if (c.fast && c.add_ok) gb.act.insert(gb.act.end(), c.S.begin(), c.S.end()); else if (!c.fast) KS.slow_supports++; }
    std::sort(gb.act.begin(), gb.act.end()); gb.act.erase(std::unique(gb.act.begin(), gb.act.end()), gb.act.end());
    const int nA = (int)gb.act.size();
    for (int s = 0; s < nsup; ++s) {
      auto& c = gb.sup[s]; c.arow.assign(c.k, 0);
      if (c.fast && c.add_ok) for (int a = 0; a < c.k; ++a) c.arow[a] = (int)(std::lower_bound(gb.act.begin(), gb.act.end(), c.S[a]) - gb.act.begin());
    }
    gb.XA.resize((size_t)nA * D.n);
    for (int a = 0; a < nA; ++a) std::memcpy(&gb.XA[(size_t)a * D.n], D.col(gb.act[a]), sizeof(double) * D.n);
    if (gb.lbuf.size() < (size_t)nsup * p) {   // sized once to G p (review P2 / L5: growing re-zero-fills and reallocates)
      const size_t full = (size_t)std::max(nsup, std::min(cfg.G, cfg.N)) * p;
      gb.lbuf.clear(); gb.lbuf.shrink_to_fit(); gb.obuf.clear(); gb.obuf.shrink_to_fit();
      gb.lbuf.resize(full); gb.obuf.resize(full);
    }
    for (int gi : active) gb.fmin[gi].store(UINT32_MAX, std::memory_order_relaxed);
    const bool poison = cfg.test_nan_rows;
    // tests: a read of a score row entry not written in this pass must fail loudly (bounded scoring writes only the
    // entries some particle can consume; review §2.1)
    auto unscored = [&](int s, int j, const double* lb, const double* ob, uint32_t i1, uint32_t pos) {
      if (!lm_poisoned(lb[j]) && !lm_poisoned(ob[j])) return false;
      fail.record(i1 - 1, fail_msg(rc, i1, pos, "label-major: read of support " + std::to_string(s) + ", label " + std::to_string(j) +
                                   " not scored in this pass (NaN-row test)"), FK_INTERNAL);
      return true;
    };
    if (poison) {
      double pv; std::memcpy(&pv, &LM_POISON_BITS, 8);
      std::fill(gb.lbuf.begin(), gb.lbuf.begin() + (size_t)nsup * p, pv); std::fill(gb.obuf.begin(), gb.obuf.begin() + (size_t)nsup * p, pv);
    }
    const bool bounded = cfg.bounded_scoring;
    if (bounded) {
      // Deletion pre-scan. The deletion odds of the k members are in the support cache, so the first member whose
      // addressed uniform deletes it is known before any tile is scored: it bounds the particle's first change. Same
      // test as the tile scan (member: change iff failed score or !(u < o)), same uniform address (philox8_positions
      // lane = uniform_at).
      for (int gi : active) {
        const SupportCache& c = gb.sup[gb.sup_of[gi]];
        const uint32_t* inv = &gb.inv[(size_t)gi * m]; const uint32_t qi = gb.q[gi]; uint32_t best = UINT32_MAX;
        const uint32_t i1 = (uint32_t)(g0 + gi) + 1;
        for (int a = 0; a < c.k; ++a) {
          const uint32_t pos = inv[c.S[a]];
          if (pos <= qi || pos >= best) continue;
          const double oj = c.del_odds[a];
          const double u = uniform_at(addr(rc.xph, rc.ustage, i1, pos, SLOT_ACCEPT));
          if (oj < 0 || !(u < oj)) best = pos;
        }
        gb.fmin[gi].store(best, std::memory_order_relaxed);
      }
    }
    const uint32_t shrink = (uint32_t)std::max(0, cfg.test_bound_shrink);
    lap(KS.t_build);

    // ---- phase A: scores, odds, first change per particle -------------------------------------------------
    #pragma omp parallel num_threads(NT)
    {
      BitScorer& sc = *scorers[omp_get_thread_num()];
      avec<double>& Pp = scratch_P[omp_get_thread_num()];   // persistent per thread (no allocation per pass)
      if (Pp.size() < (size_t)std::max(1, nA) * Bk + 8) Pp.resize((size_t)std::max(1, nA) * Bk + 8);
      const int nw = Bk / 64;   // Bk is a multiple of 64
      std::vector<uint8_t> inm(Bk); std::vector<uint64_t> needw(nw); std::vector<int> nlist(Bk + 1); double tprod = 0; uint64_t nflip = 0;
      #pragma omp for schedule(dynamic, 1) nowait
      for (int ti = 0; ti < ntile; ++ti) oom_guard([&] {
        if (cfg.test_oom_pass >= 0 && (int)KS.passes == cfg.test_oom_pass + 1 && ti == 0) throw std::bad_alloc();   // test hook
        const int j0 = ti * Bk, nbv = std::min(Bk, p - j0);
        const double* Xtile = &Xt[(size_t)ti * Bk * D.n];
        // products P[a][jj] = sum_i x_{i,a} x_{i,j}, sequential in i (bits of the Gram entry)
        const double tp0 = omp_get_wtime();
        tile_products(gb.XA.data(), nA, D.n, Xtile, Bk, Pp.data(), products_block_of(cfg));
        tprod += omp_get_wtime() - tp0;
        for (int s = 0; s < nsup; ++s) {
          const SupportCache& c = gb.sup[s];
          double* lb = &gb.lbuf[(size_t)s * p]; double* ob = &gb.obuf[(size_t)s * p];
          std::fill(inm.begin(), inm.end(), 0);
          auto mlo = std::lower_bound(c.S.begin(), c.S.end(), j0), mhi = std::lower_bound(c.S.begin(), c.S.end(), j0 + nbv);
          for (auto it = mlo; it != mhi; ++it) { int a = (int)(it - c.S.begin()); inm[*it - j0] = 1; lb[*it] = c.del_logm[a]; ob[*it] = c.del_odds[a]; }
          if (!c.add_ok) {
            for (int jj = 0; jj < nbv; ++jj) if (!inm[jj]) { lb[j0 + jj] = std::numeric_limits<double>::quiet_NaN(); ob[j0 + jj] = 0.0; }
          } else if (!c.fast) {
            for (int jj = 0; jj < nbv; ++jj) if (!inm[jj]) eval1<A>(D, st, sc, c, j0 + jj, lb[j0 + jj], ob[j0 + jj]);
          } else if (bounded) {
            // Bounded scoring (K1). A non-member label j is scored for support s only if some particle i on s can still
            // consume it: q_i < inv_i[j] < fmin_i, where fmin_i, the particle's running first change, only decreases and
            // bounds its final e at any time. Every label a particle consumes (position <= e) passed the test when its tile
            // was scored, so the scan, the walk, phase B and the apply step read only values computed in this pass; the
            // others are never read (spec §3 rule 2; the NaN-row test checks it). The needed labels are packed 8 to a
            // vector; a lane's result does not depend on the other lanes, so the bits are those of the dense path.
            thread_local std::vector<v8d> ub; if (ub.size() < (size_t)std::max(1, c.k)) ub.resize((size_t)std::max(1, c.k));
            v8d* u = ub.data();
            std::fill(needw.begin(), needw.end(), 0ull);
            for (int gi : gb.sup_parts[s]) {
              const uint32_t fm = gb.fmin[gi].load(std::memory_order_relaxed);
              lm_or_range_bits(&gb.inv[(size_t)gi * m + j0], nbv, gb.q[gi], fm > shrink ? fm - shrink : 0u, needw.data());
            }
            const int cnt = lm_list_bits(needw.data(), nw, c.S.data() + (mlo - c.S.begin()), c.S.data() + (mhi - c.S.begin()), j0, nlist.data());
            nflip += (uint64_t)cnt;
            for (int c0 = 0; c0 < cnt; c0 += 8) {
              const int nl = std::min(8, cnt - c0); const unsigned valid = (1u << nl) - 1u;
              int32_t j8[8], jj8[8];
              for (int l = 0; l < 8; ++l) { jj8[l] = nlist[c0 + std::min(l, nl - 1)]; j8[l] = j0 + jj8[l]; }   // idle lanes repeat the last label
              for (int a = 0; a < c.k; ++a) {
                const double* row = &Pp[(size_t)c.arow[a] * Bk];
                v8d g; for (int l = 0; l < 8; ++l) g[l] = row[jj8[l]];
                u[a] = g;
              }
              double lm8[8], o8[8];
              if constexpr (A == Arith::ClassA) {
                eval8_add<A>(D, st, sc, c, 0, u, j8, valid, lm8, o8);
              } else {
                unsigned rest = valid;
                while (rest) {   // lanes sharing the sorted insertion position q
                  int l0 = __builtin_ctz(rest);
                  int q = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l0]) - c.S.begin());
                  unsigned lanes = 0;
                  for (int l = l0; l < 8; ++l) if ((rest >> l) & 1u) { int ql = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l]) - c.S.begin()); if (ql == q) lanes |= 1u << l; }
                  eval8_add<A>(D, st, sc, c, q, u, j8, lanes, lm8, o8);
                  rest &= ~lanes;
                }
              }
              for (int l = 0; l < nl; ++l) { lb[j8[l]] = lm8[l]; ob[j8[l]] = o8[l]; }
            }
          } else {
            thread_local std::vector<v8d> ub; if (ub.size() < (size_t)std::max(1, c.k)) ub.resize((size_t)std::max(1, c.k));
            v8d* u = ub.data();
            for (int v = 0; v < nbv; v += 8) {
              int32_t j8[8]; unsigned valid = 0;
              for (int l = 0; l < 8; ++l) { int j = j0 + v + l; if (v + l < nbv && !inm[v + l]) valid |= 1u << l; j8[l] = std::min(j, p - 1); }
              if (!valid) continue;
              nflip += (uint64_t)__builtin_popcount(valid);
              for (int a = 0; a < c.k; ++a) u[a] = load8(&Pp[(size_t)c.arow[a] * Bk + v]);
              double lm8[8], o8[8];
              if constexpr (A == Arith::ClassA) {
                eval8_add<A>(D, st, sc, c, 0, u, j8, valid, lm8, o8);
              } else {
                unsigned rest = valid;
                while (rest) {   // lanes sharing the sorted insertion position q
                  int l0 = __builtin_ctz(rest);
                  int q = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l0]) - c.S.begin());
                  unsigned lanes = 0;
                  for (int l = l0; l < 8; ++l) if ((rest >> l) & 1u) { int ql = (int)(std::lower_bound(c.S.begin(), c.S.end(), j8[l]) - c.S.begin()); if (ql == q) lanes |= 1u << l; }
                  eval8_add<A>(D, st, sc, c, q, u, j8, lanes, lm8, o8);
                  rest &= ~lanes;
                }
              }
              for (int l = 0; l < 8; ++l) if ((valid >> l) & 1u) { lb[j8[l]] = lm8[l]; ob[j8[l]] = o8[l]; }
            }
          }
          // first change of each particle on this support within the tile
          for (int gi : gb.sup_parts[s]) {
            const uint32_t* inv = &gb.inv[(size_t)gi * m];
            const uint32_t qi = gb.q[gi]; uint32_t best = gb.fmin[gi].load(std::memory_order_relaxed);
            const uint32_t i1 = (uint32_t)(g0 + gi) + 1;
            Address a0 = addr(rc.xph, rc.ustage, i1, 0, SLOT_ACCEPT);   // lanes set the position
            v4::Ctr4 ctr = v4::address_ctr(a0); v4::Key2 key = v4::address_key(a0);
            if (bounded && c.fast && c.add_ok) {
              // bounded scan (K1): the non-member labels of the tile with q < position < best, packed 8 to a Philox call
              // (the members were tested by the deletion pre-scan, with the same uniforms)
              std::fill(needw.begin(), needw.end(), 0ull);
              lm_or_range_bits(inv + j0, nbv, qi, best, needw.data());
              const int cnt = lm_list_bits(needw.data(), nw, c.S.data() + (mlo - c.S.begin()), c.S.data() + (mhi - c.S.begin()), j0, nlist.data());
              for (int c0 = 0; c0 < cnt; c0 += 8) {
                const int nl = std::min(8, cnt - c0); uint32_t pos8[8]; double u8[8];
                for (int l = 0; l < 8; ++l) pos8[l] = inv[j0 + nlist[c0 + std::min(l, nl - 1)]];
                philox8_positions(ctr.data(), key.data(), pos8, u8);
                for (int l = 0; l < nl; ++l) {
                  const int j = j0 + nlist[c0 + l];
                  if (poison && unscored(s, j, lb, ob, i1, pos8[l])) continue;
                  const double oj = ob[j];   // ODDS_FAILED (< 0): a failed score is an event at its position
                  if ((oj < 0 || u8[l] < oj) && pos8[l] < best) best = pos8[l];
                }
              }
            } else
            for (int v = 0; v < nbv; v += 8) {
              uint32_t pos8[8]; unsigned need = 0;
              for (int l = 0; l < 8; ++l) {
                uint32_t pos = (v + l < nbv) ? inv[j0 + v + l] : 0;
                pos8[l] = pos; if (pos > qi && pos < best) need |= 1u << l;
              }
              if (!need) continue;
              double u8[8];
              philox8_positions(ctr.data(), key.data(), pos8, u8);   // = uniform_at(addr(.., pos, slot 0)) per lane
              for (int l = 0; l < 8; ++l) if ((need >> l) & 1u) {
                const int jj = v + l;
                if (poison && unscored(s, j0 + jj, lb, ob, i1, pos8[l])) continue;
                const double oj = ob[j0 + jj];   // ODDS_FAILED (< 0): a failed score is an event at its position
                bool change = oj < 0 || (inm[jj] ? !(u8[l] < oj) : (u8[l] < oj));
                if (change && pos8[l] < best) best = pos8[l];
              }
            }
            uint32_t cur = gb.fmin[gi].load(std::memory_order_relaxed);
            while (best < cur && !gb.fmin[gi].compare_exchange_weak(cur, best, std::memory_order_relaxed)) {}
          }
        }
      });
      #pragma omp atomic
      KS.t_products += tprod;
      #pragma omp atomic
      KS.flip_evals += nflip;
    }
    lap(KS.t_phaseA);
    if (fail_fatal()) return;

    // ---- walk: U/N/I labels in position order up to the first Gibbs change --------------------------------
    #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
    for (size_t t = 0; t < active.size(); ++t) {
      int gi = active[t]; ThreadLedger& L = *tl[omp_get_thread_num()]; BitScorer& sc = *scorers[omp_get_thread_num()];
      uint32_t f = gb.fmin[gi].load(std::memory_order_relaxed);
      gb.etype[gi] = 0; gb.e[gi] = (uint32_t)m;
      if (f != UINT32_MAX) { gb.etype[gi] = 1; gb.e[gi] = f; }
      const uint32_t i1 = (uint32_t)(g0 + gi) + 1; uint32_t pos_cur = 0;
      try {
        for (auto& pl : gb.ng[gi]) {
          if (pl.first <= gb.q[gi]) continue;
          if (pl.first >= f) break;
          pos_cur = pl.first;
          if (step_nongibbs(pl.second, P[g0 + gi], g0 + gi, pl.first, rc, L, sc, gb.pending[gi])) { gb.etype[gi] = 2; gb.e[gi] = pl.first; break; }
        }
        if (gb.etype[gi] == 1) {   // the event at f: a Gibbs change, or a consumed failed score
          int j = (int)gb.ord[(size_t)gi * m + f - 1]; const int s = gb.sup_of[gi];
          if (poison && unscored(s, j, &gb.lbuf[(size_t)s * p], &gb.obuf[(size_t)s * p], i1, f)) gb.etype[gi] = 3;
          else if (gb.obuf[(size_t)s * p + j] < 0) { fail.record(i1 - 1, fail_msg(rc, i1, f, gibbs_fail(j))); gb.etype[gi] = 3; }
        }
      } catch (const v4::NumericalFailure& e) { fail.record(i1 - 1, fail_msg(rc, i1, pos_cur, e.what())); gb.etype[gi] = 3; }
      catch (const std::bad_alloc&) { fail.record(UINT32_MAX, "out of memory inside a parallel region", FK_RESOURCE); gb.etype[gi] = 3; }
      if (gb.etype[gi] == 3) gb.e[gi] = gb.q[gi];   // a failed particle consumes nothing more (the round's events are discarded)
    }
    lap(KS.t_walk);
    if (top.defer && top.staged() >= (top.stage_limit + top.stage_hard) / 2) { release_snapshots(); top.compact_parallel(NT); }   // walk offers

    // ---- phase B: consumption of the Gibbs labels at positions (q, e] -------------------------------------
    // In waves of tiles; between waves (all threads free) the staging area is compacted in parallel once it passes
    // the trigger, so in-pass serial compactions are rare (content: a function of the offers only).
    // wave size bounded by offer volume (review P2): a wave offers at most nsup * tile entries per tile, so <= 0.1 c per
    // wave keeps the staging area below 0.375 c + 0.1 c < c/2 = stage_hard: the in-pass serial compaction (stale
    // snapshots, pool over-reservation) is unreachable in label-major
    const uint64_t per_tile = (uint64_t)std::max(1, nsup) * (uint64_t)Bk;
    const int wave = top.defer ? (int)std::max<uint64_t>(1, std::min<uint64_t>((uint64_t)std::max(64, 16 * NT), (top.cap / 10) / per_tile)) : ntile;
    for (int w0 = 0; w0 < ntile; w0 += wave) {
    const int w1 = std::min(ntile, w0 + wave);
    #pragma omp parallel num_threads(NT)
    {
      ThreadLedger& L = *tl[omp_get_thread_num()];
      Model T;
      std::vector<uint32_t> ncons_v(Bk), fpos_v(Bk); std::vector<int> first_v(Bk); std::vector<uint64_t> consw((size_t)Bk / 64);
      #pragma omp for schedule(dynamic, 1)
      for (int ti = w0; ti < w1; ++ti) oom_guard([&] {
        if (L.buf.snap && L.buf.snap_gen != top.gen.load(std::memory_order_relaxed)) { L.buf.snap.reset(); L.buf.snap_gen = ~0ull; }   // M2
        if (cfg.leaders) {
          if (L.buf0.snap && L.buf0.snap_gen != lead0.gen.load(std::memory_order_relaxed)) { L.buf0.snap.reset(); L.buf0.snap_gen = ~0ull; }
          if (L.buf1.snap && L.buf1.snap_gen != lead1.gen.load(std::memory_order_relaxed)) { L.buf1.snap.reset(); L.buf1.snap_gen = ~0ull; }
        }
        const int j0 = ti * Bk, nbv = std::min(Bk, p - j0);
        for (int s = 0; s < nsup; ++s) {
          const SupportCache& c = gb.sup[s];
          const double* lb = &gb.lbuf[(size_t)s * p]; const double* ob = &gb.obuf[(size_t)s * p];
          const auto& parts = gb.sup_parts[s];
          const double prior_add = c.add_ok ? D.logprior[c.k + 1] : 0.0, prior_del = c.k > 0 ? D.logprior[c.k - 1] : 0.0;
          // one consumed label: ncons particles of this support consumed it; `first` = the smallest of them, at fpos
          auto consume = [&](const int jj, const uint32_t ncons, const int first, const uint32_t fpos) {
            const int j = j0 + jj;
            if (poison && unscored(s, j, lb, ob, (uint32_t)(g0 + first) + 1, fpos)) return;
            const uint64_t fx = rc.measured ? fix63(ob[j]) : 0;
            if (rc.measured) rb_cur[j] += (u128)fx * ncons;
            L.logical[rc.phase][ME_GIBBS_HELD] += ncons; L.ms.gibbs += ncons;
            const double lm = lb[j];
            if (std::isnan(lm)) { L.ms.gibbs_cap += ncons; return; }   // infeasible addition: no flip event (core/cpp/v3_engine.h:119)
            const bool in = std::binary_search(c.S.begin(), c.S.end(), j);
            const double F = (in ? prior_del : prior_add) + lm;
            L.logical[rc.phase][ME_GIBBS_FLIP] += ncons - 1;   // + 1 inside scored()
            // leaders (review PR24 P1): log gamma_0 of the flip (same block sum as Start::comp) and each leader's own cut-off
            const double lg0 = cfg.leaders ? (in ? prior_del + comp_del(st, c, j) : prior_add + comp_add(st, c, j)) : 0.0;
            const bool lead_pass = cfg.leaders && (lg0 >= lead0.tau.load(std::memory_order_relaxed) || F >= lead1.tau.load(std::memory_order_relaxed));
            if (lead_pass || F >= top.tau.load(std::memory_order_relaxed) || F > L.island_best || F >= L.hpm.F) {
              T = c.S; if (in) sorted_erase(T, j); else sorted_insert(T, j);
              L.scored(T.data(), (uint32_t)T.size(), c.h ^ D.zob.key[j], F, lm, rc.phase, ME_GIBBS_FLIP, key(rc, (uint32_t)(g0 + first) + 1, fpos, 1),
                       cfg.leaders ? lg0 : std::numeric_limits<double>::quiet_NaN());
            } else {
              L.logical[rc.phase][ME_GIBBS_FLIP] += 1;
            }
          };
          if (bounded && parts.size() == 1) {
            // one particle on the support (K1; the usual case once the particles have separated): its consumed labels of
            // the tile are the bits q < position < e + 1, in ascending label order as below; no per-label counting pass
            const int gi = parts[0]; const uint32_t qi = gb.q[gi], ei = gb.e[gi];
            if (ei > qi) {
              const uint32_t* inv = &gb.inv[(size_t)gi * m + j0];
              std::fill(consw.begin(), consw.end(), 0ull);
              lm_or_range_bits(inv, nbv, qi, ei + 1, consw.data());
              for (size_t w = 0; w < consw.size(); ++w)
                for (uint64_t b = consw[w]; b; b &= b - 1) { const int jj = (int)(w * 64) + __builtin_ctzll(b); consume(jj, 1u, gi, inv[jj]); }
            }
          } else {
            // consumption counts per label: particles in ascending order, each reading its own inverse order row
            std::fill(ncons_v.begin(), ncons_v.begin() + nbv, 0u); std::fill(first_v.begin(), first_v.begin() + nbv, -1);
            for (int gi : parts) {
              const uint32_t* inv = &gb.inv[(size_t)gi * m + j0]; const uint32_t qi = gb.q[gi], ei = gb.e[gi];
              for (int jj = 0; jj < nbv; ++jj) {
                uint32_t pos = inv[jj];
                if (pos > qi && pos <= ei) { if (first_v[jj] < 0) { first_v[jj] = gi; fpos_v[jj] = pos; } ++ncons_v[jj]; }
              }
            }
            for (int jj = 0; jj < nbv; ++jj) if (ncons_v[jj]) consume(jj, ncons_v[jj], first_v[jj], fpos_v[jj]);
          }
        }
      });
    }
    if (top.defer && w1 < ntile && top.staged() >= (top.stage_limit + top.stage_hard) / 2) { release_snapshots(); top.compact_parallel(NT); }
    }   // waves
    lap(KS.t_phaseB);
    if (fail_fatal()) return;
    if (top.defer && top.staged() >= top.stage_limit) {   // pass boundary: all threads free
      release_snapshots();
      top.compact_parallel(NT);
    }
    lap(KS.t_compact_pass);

    // ---- apply the state changes ---------------------------------------------------------------------------
    // particles are independent: in parallel (L5; class A pays one canonical Bit score per accepted Gibbs change)
    #pragma omp parallel for schedule(dynamic, 1) num_threads(NT)
    for (size_t t = 0; t < active.size(); ++t) oom_guard([&] {
      const int gi = active[t]; const int th = omp_get_thread_num();
      Particle& x = P[g0 + gi];
      if (gb.etype[gi] == 1) {
        int j = (int)gb.ord[(size_t)gi * m + gb.e[gi] - 1];
        const SupportCache& c = gb.sup[gb.sup_of[gi]];
        if (poison && unscored(gb.sup_of[gi], j, &gb.lbuf[(size_t)gb.sup_of[gi] * p], &gb.obuf[(size_t)gb.sup_of[gi] * p], (uint32_t)(g0 + gi) + 1, gb.e[gi])) return;
        double lm = gb.lbuf[(size_t)gb.sup_of[gi] * p + j];
        Model T = c.S; if (std::binary_search(T.begin(), T.end(), j)) sorted_erase(T, j); else sorted_insert(T, j);
        try { fill(x, T, canonical(*scorers[th], T, lm)); tl[th]->ms.gibbs_change++; }
        catch (const v4::NumericalFailure& e) { fail.record((uint32_t)(g0 + gi), fail_msg(rc, (uint32_t)(g0 + gi) + 1, gb.e[gi], e.what())); gb.etype[gi] = 3; }
      } else if (gb.etype[gi] == 2) {
        x = gb.pending[gi];
      }
      gb.q[gi] = gb.e[gi];
      if (gb.e[gi] == (uint32_t)m || gb.etype[gi] == 3) gb.done[gi] = 1;
    });
    if (fail_fatal()) return;
    lap(KS.t_apply);
  }
}

}  // namespace v4::island
