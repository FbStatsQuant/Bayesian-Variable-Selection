// island_pm.h -- the steps shared by both kernels and the particle-major reference (member functions of IslandEngine,
// declared in island_run.h): U, N_b, I steps (core/cpp/v3_engine.h:146-192), the round order (Fisher-Yates,
// core/cpp/v3_engine.h:195-200), and core's serial round for one particle (core/cpp/v3_engine.h:202-214).
#pragma once
#include "island_run.h"

namespace v4::island {

// --- U, N_b, I steps at round position `pos` (core/cpp/v3_engine.h:146-192). Returns true if the state changed;
//     the new state is written to `out`. ----------------------------------------------------------------------
// The I step's proposal at round position `pos`: a pi_0 draw from the step's own addresses, scored. It does not depend
// on the particle's state, so the label-major order phase draws it ahead (K2, WP3_ARCH_REVIEW §2.3); same bits.
template <Arith A>
void IslandEngine<A>::draw_indep(int i, uint32_t pos, const RoundCtx& rc, BitScorer& sc, Particle& out) {
  const uint32_t i1 = (uint32_t)i + 1;
  auto U = [&](uint32_t slot) { return this->U(addr(rc.xph, rc.ustage, i1, pos, slot)); };
  Model T;
  if (csrc) draw_pi0(st, [&](uint32_t slot) { return U(slot); }, T);   // compat: core's serial consumption
  else {
    const Address a0 = addr(rc.xph, rc.ustage, i1, pos, 0);
    const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
    draw_pi0_fast(st, [&](uint32_t slot) { return U(slot); },
                  [&](const uint32_t* sl, double* o8) { philox8_word(ctr.data(), kk.data(), 0, sl, o8); }, T);
  }
  if (cfg.test_fail_indep == i && rc.xph == X_BRIDGE && rc.ustage == (uint32_t)cfg.test_fail_indep_stage)   // test hook
    throw v4::NumericalFailure("score failed (test hook: I proposal)");
  fill(out, T, sc.score(T).logm);
}

template <Arith A>
bool IslandEngine<A>::step_nongibbs(int lab, const Particle& Pc, int i, uint32_t pos, const RoundCtx& rc, ThreadLedger& L, BitScorer& sc, Particle& out,
                                    const Particle* pre) {
  const uint32_t i1 = (uint32_t)i + 1;
  auto U = [&](uint32_t slot) { return this->U(addr(rc.xph, rc.ustage, i1, pos, slot)); };
  int k = (int)Pc.S.size();
  if (lab == p) {   // U: uniform swap
    if (k == 0 || k == p) { L.ms.us_self++; return false; }
    L.ms.us_exec++;
    int j = Pc.S[(int)std::floor(U(SLOT_MOVE_J) * k)];
    int mth = (int)std::floor(U(SLOT_MOVE_L) * (p - k));
    int l = mth; for (int s : Pc.S) { if (s <= l) ++l; else break; }   // mth non-member in increasing order
    Model T = Pc.S; sorted_erase(T, j); sorted_insert(T, l);
    fill(out, T, sc.score(T).logm);
    offer_particle(L, out, rc.phase, ME_USWAP, key(rc, i1, pos));
    double la = lgphi(out, rc.phi) - lgphi(Pc, rc.phi);
    double alpha = (la >= 0) ? 1.0 : pm::exp(la);
    if (U(SLOT_ACCEPT) < alpha) { L.ms.us_acc++; return true; }
    return false;
  }
  if (lab <= p + cfg.B) {   // N_b: neighbour swap
    if (k == 0) { L.ms.ns_self++; return false; }
    L.ms.ns_exec++;
    int j = Pc.S[(int)std::floor(U(SLOT_MOVE_J) * k)];
    std::vector<int> cand;
    for (int64_t e = nb.ptr[j]; e < nb.ptr[j + 1]; ++e) if (!contains(Pc.S, nb.idx[e])) cand.push_back(nb.idx[e]);
    if (cand.empty()) { L.ms.ns_noscore++; return false; }
    int l = cand[(int)std::floor(U(SLOT_MOVE_L) * cand.size())];
    Model T = Pc.S; sorted_erase(T, j); sorted_insert(T, l);
    int back = 0; for (int64_t e = nb.ptr[l]; e < nb.ptr[l + 1]; ++e) if (!contains(T, nb.idx[e])) ++back;
    fill(out, T, sc.score(T).logm);
    offer_particle(L, out, rc.phase, ME_NSWAP, key(rc, i1, pos));
    double la = lgphi(out, rc.phi) - lgphi(Pc, rc.phi) + pm::log((double)cand.size()) - pm::log((double)back);
    double alpha = (la >= 0) ? 1.0 : pm::exp(la);
    if (U(SLOT_ACCEPT) < alpha) { L.ms.ns_acc++; return true; }
    return false;
  }
  // I: independence proposal from pi_0 (drawn here, or ahead by the label-major order phase: `pre`)
  L.ms.in_exec++;
  if (pre) out = *pre; else draw_indep(i, pos, rc, sc, out);
  offer_particle(L, out, rc.phase, ME_INDEP, key(rc, i1, pos));
  double la = rc.phi * (out.d - Pc.d);
  double alpha = (la >= 0) ? 1.0 : pm::exp(la);
  if (U(SLOT_ACCEPT) < alpha) { L.ms.in_acc++; return true; }
  return false;
}

// Round order (core/cpp/v3_engine.h:195-200): Fisher-Yates, uniform of step i at slot m-1-i.
template <Arith A>
void IslandEngine<A>::draw_order(const RoundCtx& rc, int i, uint32_t* ord) {
  for (int t = 0; t < m; ++t) ord[t] = (uint32_t)t;
  if (csrc) {   // compat: one uniform at a time from the serial stream
    uint32_t slot = 0;
    for (int t = m - 1; t >= 1; --t) {
      int jj = (int)std::floor(U(addr(rc.xph, rc.ustage, (uint32_t)i + 1, 0, slot_of(v4::SK_ORDER, slot++))) * (t + 1));
      std::swap(ord[t], ord[jj]);
    }
    return;
  }
  // L5: the same Fisher-Yates swaps with the uniforms of slots d = 0..m-2 computed 8 at a time and the swap targets of
  // the next block prefetched (the addresses are fixed, so the targets are known ahead)
  const Address a0 = addr(rc.xph, rc.ustage, (uint32_t)i + 1, 0, slot_of(v4::SK_ORDER, 0));
  const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
  const int nd = m - 1;
  int jcur[8], jnext[8]; uint32_t sl[8]; double u8[8];
  auto block = [&](int d0, int* jj) {
    for (int l = 0; l < 8; ++l) sl[l] = slot_of(v4::SK_ORDER, (uint32_t)std::min(d0 + l, std::max(0, nd - 1)));
    philox8_word(ctr.data(), kk.data(), 0, sl, u8);
    for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); jj[l] = (int)std::floor(u8[l] * (t + 1)); __builtin_prefetch(&ord[jj[l]], 1); }
  };
  if (nd > 0) block(0, jcur);
  for (int d0 = 0; d0 < nd; d0 += 8) {
    if (d0 + 8 < nd) block(d0 + 8, jnext);
    for (int l = 0; l < 8 && d0 + l < nd; ++l) { const int t = m - 1 - (d0 + l); std::swap(ord[t], ord[jcur[l]]); }
    std::memcpy(jcur, jnext, sizeof jcur);
  }
}

// --- particle-major reference: core/cpp/v3_engine.h:202-214 for particle i ---------------------------------
template <Arith A>
void IslandEngine<A>::pm_round(int i, const RoundCtx& rc, ThreadLedger& L, BitScorer& sc, std::vector<u128>* rb) {
  // a worker drops a stale snapshot at every particle boundary (review m3; the PM analogue of the tile-start release)
  if (L.buf.snap && L.buf.snap_gen != top.gen.load(std::memory_order_relaxed)) { L.buf.snap.reset(); L.buf.snap_gen = ~0ull; }
  std::vector<uint32_t> ord(m); draw_order(rc, i, ord.data());
  Particle& Pi = P[i]; const uint32_t i1 = (uint32_t)i + 1;
  SupportCache s; bool cache_ok = false; Particle tmp;
  uint32_t pos_cur = 0;
  try {
  if (cfg.test_oom_pass >= 0 && (int)rc.ev_round == cfg.test_oom_pass && i == 0) throw std::bad_alloc();   // test hook
  for (int pos0 = 0; pos0 < m; ++pos0) {
    const uint32_t pos = (uint32_t)pos0 + 1; int lab = (int)ord[pos0];
    pos_cur = pos;
    if (lab < p) {
      // Gibbs (core/cpp/v3_engine.h:113-132): held state counted, other configuration scored and offered
      L.ms.gibbs++; L.logical[rc.phase][ME_GIBBS_HELD]++;
      if (!cache_ok) { build_support(D, st, sc, s, Pi.S, Pi.h, Pi.logm, Pi.lg0, Pi.d, rc.phi); cache_ok = true; }
      bool in = contains(Pi.S, lab);
      double lm = 0, o = 0;
      eval1<A>(D, st, sc, s, lab, lm, o);
      if (o < 0) { fail.record((uint32_t)i, fail_msg(rc, i1, pos, gibbs_fail(lab))); return; }   // consumed failed score
      bool has_other = in || s.add_ok;
      if (!has_other) L.ms.gibbs_cap++;   // addition refused at |S| = K: one event (held), INTERFACES v0.1.5 §4.2
      Model T;
      if (has_other) {
        T = Pi.S; if (in) sorted_erase(T, lab); else sorted_insert(T, lab);
        double F = D.logprior[T.size()] + lm;
        const double lg0T = cfg.leaders ? D.logprior[T.size()] + st.comp(T) : std::numeric_limits<double>::quiet_NaN();
        L.scored(T.data(), (uint32_t)T.size(), Pi.h ^ D.zob.key[lab], F, lm, rc.phase, ME_GIBBS_FLIP, key(rc, i1, pos, 1), lg0T);
      }
      if (rb) { if (csrc) rb_d[lab] += o; else (*rb)[lab] += fix63(o); }   // compat: core's double sum, serial order
      double u = U(addr(rc.xph, rc.ustage, i1, pos, SLOT_ACCEPT));
      bool include = u < o;
      if (include != in) { fill(Pi, T, canonical(sc, T, lm)); L.ms.gibbs_change++; cache_ok = false; }
    } else {
      if (step_nongibbs(lab, Pi, i, pos, rc, L, sc, tmp)) { Pi = tmp; cache_ok = false; }
    }
  }
  } catch (const v4::NumericalFailure& e) { fail.record((uint32_t)i, fail_msg(rc, i1, pos_cur, e.what())); }
  catch (const std::bad_alloc&) { fail.record(UINT32_MAX, "out of memory inside a parallel region", FK_RESOURCE); }
}

}  // namespace v4::island
