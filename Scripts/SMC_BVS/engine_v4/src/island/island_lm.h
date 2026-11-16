// island_lm.h -- the label-major round for a group of particles (member function of IslandEngine, declared in
// island_run.h; its group state is island_lm_state.h). Same outputs as the particle-major reference (T3).
#pragma once
#include "island_run.h"

namespace v4::island {

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
    for (int s = 0; s < nsup; ++s) { auto& c = gb.sup[s]; if (c.fast && c.add_ok) gb.act.insert(gb.act.end(), c.S.begin(), c.S.end()); else if (!c.fast) KS.slow_supports++;
                                     if (c.add_ok) KS.flip_evals += (uint64_t)(p - c.k); }   // D-30 counter (WP7 O2)
    std::sort(gb.act.begin(), gb.act.end()); gb.act.erase(std::unique(gb.act.begin(), gb.act.end()), gb.act.end());
    const int nA = (int)gb.act.size();
    KS.act_cols += (uint64_t)nA;   // D-30 counter (WP7 O2)
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
    lap(KS.t_build);

    // ---- phase A: scores, odds, first change per particle -------------------------------------------------
    #pragma omp parallel num_threads(NT)
    {
      BitScorer& sc = *scorers[omp_get_thread_num()];
      avec<double>& Pp = scratch_P[omp_get_thread_num()];   // persistent per thread (no allocation per pass)
      if (Pp.size() < (size_t)std::max(1, nA) * Bk + 8) Pp.resize((size_t)std::max(1, nA) * Bk + 8);
      std::vector<uint8_t> inm(Bk); double tprod = 0;
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
          } else {
            thread_local std::vector<v8d> ub; if (ub.size() < (size_t)std::max(1, c.k)) ub.resize((size_t)std::max(1, c.k));
            v8d* u = ub.data();
            for (int v = 0; v < nbv; v += 8) {
              int32_t j8[8]; unsigned valid = 0;
              for (int l = 0; l < 8; ++l) { int j = j0 + v + l; if (v + l < nbv && !inm[v + l]) valid |= 1u << l; j8[l] = std::min(j, p - 1); }
              if (!valid) continue;
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
          int j = (int)gb.ord[(size_t)gi * m + f - 1];
          if (gb.obuf[(size_t)gb.sup_of[gi] * p + j] < 0) { fail.record(i1 - 1, fail_msg(rc, i1, f, gibbs_fail(j))); gb.etype[gi] = 3; }
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
      std::vector<uint32_t> ncons_v(Bk), fpos_v(Bk); std::vector<int> first_v(Bk);
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
          // consumption counts per label: particles in ascending order, each reading its own inverse order row
          std::fill(ncons_v.begin(), ncons_v.begin() + nbv, 0u); std::fill(first_v.begin(), first_v.begin() + nbv, -1);
          for (int gi : parts) {
            const uint32_t* inv = &gb.inv[(size_t)gi * m + j0]; const uint32_t qi = gb.q[gi], ei = gb.e[gi];
            for (int jj = 0; jj < nbv; ++jj) {
              uint32_t pos = inv[jj];
              if (pos > qi && pos <= ei) { if (first_v[jj] < 0) { first_v[jj] = gi; fpos_v[jj] = pos; } ++ncons_v[jj]; }
            }
          }
          for (int jj = 0; jj < nbv; ++jj) {
            const int j = j0 + jj;
            const uint32_t ncons = ncons_v[jj]; const int first = first_v[jj]; const uint32_t fpos = fpos_v[jj];
            if (!ncons) continue;
            const uint64_t fx = rc.measured ? fix63(ob[j]) : 0;
            if (rc.measured) rb_cur[j] += (u128)fx * ncons;
            L.logical[rc.phase][ME_GIBBS_HELD] += ncons; L.ms.gibbs += ncons;
            const double lm = lb[j];
            if (std::isnan(lm)) { L.ms.gibbs_cap += ncons; continue; }   // infeasible addition: no flip event (core/cpp/v3_engine.h:119)
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
