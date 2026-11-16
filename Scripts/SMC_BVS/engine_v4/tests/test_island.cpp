// test_island.cpp -- WP3 unit tests: Philox KAT, flip kernels (bit form = scorer bits; class A <= 1e-9), class-A
// log/exp, the concurrent store (order-free, multi-thread), T3 execution invariance, T6 restart.
#include <omp.h>
#include <cstdio>
#include <map>
#include <random>
#include <set>
#include <unistd.h>
#include "tk.h"
#include "tutil_island.h"
#include "v4/island/island.h"
#include "v4/island/island_file.h"
#include "v4/format.h"

using namespace v4::island;

static std::string tmpdir() { const char* t = std::getenv("TMPDIR"); return t ? t : "."; }

// ---------------------------------------------------------------------------------------------------------------
TEST(philox_known_answers) {
  // Random123 kat_vectors, philox4x32_10
  struct KAT { uint32_t c[4], k[2], o[4]; } kat[] = {
      {{0, 0, 0, 0}, {0, 0}, {0x6627e8d5, 0xe169c58d, 0xbc57ac4c, 0x9b00dbd8}},
      {{0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff}, {0xffffffff, 0xffffffff}, {0x408f276d, 0x41c83b0e, 0xa20bc7c6, 0x6d5451fd}},
      {{0x243f6a88, 0x85a308d3, 0x13198a2e, 0x03707344}, {0xa4093822, 0x299f31d0}, {0xd16cfe09, 0x94fdcceb, 0x5001e420, 0x24126ea1}},
  };
  for (auto& t : kat) {
    v4::Ctr4 o = v4::philox4x32_10(v4::Ctr4{t.c[0], t.c[1], t.c[2], t.c[3]}, v4::Key2{t.k[0], t.k[1]});
    for (int i = 0; i < 4; ++i) CHECKF(o[i] == t.o[i], "word %d: %08x vs %08x", i, o[i], t.o[i]);
  }
  // address packing (INTERFACES §3) and uniform range
  Address a; a.seed = 7; a.role = R_FINAL; a.island = 3; a.xph = X_BRIDGE; a.stage = 5; a.particle = 11; a.position = 13; a.slot = 2;
  v4::Key2 k = v4::address_key(a); v4::Ctr4 c = v4::address_ctr(a);
  CHECK(k[0] == 7 && k[1] == 3 && c[0] == 2 && c[1] == 13 && c[2] == 11 && c[3] == ((2u << 24) | 5u));
  double u = uniform_at(a); CHECK(u >= 0 && u < 1);
  // the 8-lane Philox of the label-major kernel equals uniform_at lane by lane
  std::mt19937_64 g(1); bool ok = true;
  for (int rep = 0; rep < 2000; ++rep) {
    Address b; b.seed = (uint32_t)g(); b.island = (uint32_t)(g() % 1000); b.xph = (uint8_t)(g() % 5); b.stage = (uint32_t)(g() % 5000);
    b.particle = (uint32_t)g(); b.slot = rep % 3 ? 0 : (uint32_t)g();
    uint32_t pos[8]; for (auto& x : pos) x = (uint32_t)g();
    v4::Ctr4 c = v4::address_ctr(b); v4::Key2 kk = v4::address_key(b); double u8[8];
    philox8_positions(c.data(), kk.data(), pos, u8);
    for (int l = 0; l < 8; ++l) { Address e = b; e.position = pos[l]; ok = ok && same_bits(u8[l], uniform_at(e)); }
  }
  CHECK(ok);
}

// ---------------------------------------------------------------------------------------------------------------
struct Fixture {
  Data D; Start st; Neighbours nb;
  Fixture(int n, int p, uint64_t seed, int bsz = 4, double rho = 0.6) {
    make_ar_data(D, n, p, rho, seed);
    build_start(st, D, contiguous_blocks(p, bsz));
    nb = window_neighbours(D, 14, 8);
  }
};

static uint64_t D_hash(const std::vector<uint64_t>& key, const Model& S) { uint64_t h = 0; for (int j : S) h ^= key[j]; return h; }
static Model random_support(std::mt19937_64& g, int p, int k, const Model& base = {}) {
  Model S = base;
  while ((int)S.size() < k) { int j = (int)(g() % p); if (!contains(S, j)) sorted_insert(S, j); }
  return S;
}

// Bit form: every flip score equals the full scorer's bits, at every insertion position, k = 0..12; both kernels'
// entry points (8-lane batch with shared q, and the one-label path).
TEST(flip_bit_equals_scorer) {
  Fixture F(120, 400, 11);
  BitScorer sc(&F.D);
  std::mt19937_64 g(5);
  long checked = 0, mism = 0, fallback_lanes = 0;
  for (int rep = 0; rep < 40; ++rep) {
    int k = rep % 13;
    Model S = random_support(g, F.D.p, k);
    double lm = sc.score(S).logm; double c = F.st.comp(S);
    SupportCache s; build_support(F.D, F.st, sc, s, S, zobrist(F.D, S), lm, F.D.logprior[k] + c, (lm - F.D.logm0) - c, 0.37);
    CHECK(s.fast);
    for (int j0 = 0; j0 < F.D.p; j0 += 8) {
      int32_t j8[8]; unsigned valid = 0;
      for (int l = 0; l < 8; ++l) { j8[l] = j0 + l; if (!contains(S, j0 + l)) valid |= 1u << l; }
      std::vector<v8d> ub(64); v8d* u = ub.data();
      for (int a = 0; a < k; ++a) for (int l = 0; l < 8; ++l) u[a][l] = gram(F.D, S[a], j8[l]);
      double lm8[8] = {0}, o8[8] = {0};
      unsigned rest = valid;
      while (rest) {
        int l0 = __builtin_ctz(rest);
        int q = (int)(std::lower_bound(S.begin(), S.end(), j8[l0]) - S.begin());
        unsigned lanes = 0;
        for (int l = l0; l < 8; ++l) if (((rest >> l) & 1u) && (int)(std::lower_bound(S.begin(), S.end(), j8[l]) - S.begin()) == q) lanes |= 1u << l;
        eval8_add<Arith::Bit>(F.D, F.st, sc, s, q, u, j8, lanes, lm8, o8);
        rest &= ~lanes;
      }
      for (int l = 0; l < 8; ++l) {
        Model T = S; double ref, o1, l1;
        if (contains(S, j8[l])) { sorted_erase(T, j8[l]); } else sorted_insert(T, j8[l]);
        ref = sc.score(T).logm;
        eval1<Arith::Bit>(F.D, F.st, sc, s, j8[l], l1, o1);
        ++checked;
        if (!same_bits(ref, l1)) ++mism;
        if ((valid >> l) & 1u) { if (!same_bits(ref, lm8[l]) || !same_bits(o1, o8[l])) ++mism; }
        // odds against core/cpp/v3_engine.h:124-126 written out
        int kT = (int)T.size(); double cT = F.st.comp(T);
        double lgT = (F.D.logprior[kT] + cT) + 0.37 * ((ref - F.D.logm0) - cT), lgS = s.lgphi;
        double oref = contains(S, j8[l]) ? plogis_log(lgS - lgT) : plogis_log(lgT - lgS);
        if (!same_bits(oref, o1)) ++mism;
      }
    }
  }
  std::printf("  bit flips checked %ld, mismatches %ld, fallback lanes %ld\n", checked, mism, fallback_lanes);
  CHECK(mism == 0);
}

TEST(flip_classA_agrees_with_bit) {
  Fixture F(200, 600, 12);
  BitScorer sc(&F.D);
  std::mt19937_64 g(9);
  double worst = 0, worst_o = 0; long n = 0;
  for (int rep = 0; rep < 30; ++rep) {
    int k = 1 + rep % 12;
    Model S = random_support(g, F.D.p, k);
    double lm = sc.score(S).logm, c = F.st.comp(S);
    SupportCache s; build_support(F.D, F.st, sc, s, S, zobrist(F.D, S), lm, F.D.logprior[k] + c, (lm - F.D.logm0) - c, 1.0);
    for (int j = 0; j < F.D.p; ++j) {
      if (contains(S, j)) continue;
      double lb, ob, la, oa;
      eval1<Arith::Bit>(F.D, F.st, sc, s, j, lb, ob);
      eval1<Arith::ClassA>(F.D, F.st, sc, s, j, la, oa);
      worst = std::max(worst, std::fabs(la - lb) / std::fabs(lb));
      worst_o = std::max(worst_o, std::fabs(oa - ob));
      ++n;
    }
  }
  std::printf("  class A vs bit: %ld scores, max relative |dlogm| %.3e, max |do| %.3e (FMA: %d)\n", n, worst, worst_o, (int)kHasFMA());
  CHECK(worst <= 1e-9);
  CHECK(worst_o <= 1e-8);
}

TEST(classA_vector_log_exp) {
  std::mt19937_64 g(3); std::uniform_real_distribution<double> U(-30, 30);
  double wl = 0, we = 0;
  for (int rep = 0; rep < 20000; ++rep) {
    v8d x, y;
    for (int l = 0; l < 8; ++l) { x[l] = std::exp(U(g)); y[l] = U(g) * 20; }
    v8d a = alog8(x), e = aexp8(y);
    for (int l = 0; l < 8; ++l) {
      double rl = std::log(x[l]), re = std::exp(y[l]);
      wl = std::max(wl, std::fabs(a[l] - rl) / std::max(1e-300, std::fabs(rl)));
      if (re > 1e-300) we = std::max(we, std::fabs(e[l] - re) / re);
    }
  }
  v8d z = bc(-800); v8d ez = aexp8(z); CHECK(ez[0] == 0.0);
  v8d one = bc(1.0); v8d l1 = alog8(one); CHECK(l1[0] == 0.0);
  std::printf("  max relative error: log %.3e, exp %.3e\n", wl, we);
  CHECK(wl < 4e-16 * 4); CHECK(we < 4e-16 * 4);
}

// ---------------------------------------------------------------------------------------------------------------
// Store: content = top-c of the offered set (max value per model), independent of order, buffer sizes and threads.
static std::vector<std::tuple<double, Model>> reference_top(const std::vector<std::pair<double, Model>>& offers, size_t cap) {
  std::map<Model, double> best;
  for (auto& o : offers) { auto it = best.find(o.second); if (it == best.end() || o.first > it->second) best[o.second] = o.first; }
  std::vector<std::tuple<double, Model>> v;
  for (auto& e : best) v.push_back({e.second, e.first});
  std::sort(v.begin(), v.end(), [](auto& a, auto& b) {
    if (std::get<0>(a) != std::get<0>(b)) return std::get<0>(a) > std::get<0>(b);
    if (std::get<1>(a).size() != std::get<1>(b).size()) return std::get<1>(a).size() < std::get<1>(b).size();
    return lex_less(std::get<1>(a), std::get<1>(b));
  });
  if (v.size() > cap) v.resize(cap);
  return v;
}
TEST(store_order_free_multithread) {
  std::mt19937_64 g(17);
  const int p = 500;
  std::vector<uint64_t> key(p); uint64_t x = 99; for (auto& k : key) k = splitmix64(x);
  std::vector<std::pair<double, Model>> offers;
  for (int i = 0; i < 200000; ++i) {
    Model S = random_support(g, 60, 1 + (int)(g() % 4));   // few distinct models: many duplicates
    double v = -std::floor((double)(g() % 1000) / 10.0);     // many exact value ties
    if (g() % 50 == 0) v += 1e-13;                           // class-A-like second value of a model
    offers.push_back({v, S});
  }
  for (size_t cap : {1ul, 7ul, 1000ul, 5000ul, 100000ul}) {
    auto ref = reference_top(offers, cap);
    for (int threads : {1, 3}) for (size_t lim : {(size_t)1, (size_t)37, (size_t)100000}) {
      if ((double)offers.size() / lim * (double)cap > 3e8) continue;   // keep the merge count affordable
      TopStore st; st.init(cap, Order::HPM); st.buf_limit = lim; st.stage_limit = std::max<size_t>(1, lim * 3);
      std::vector<StoreBuffer> bufs(threads);
      #pragma omp parallel for num_threads(threads) schedule(dynamic, 97)
      for (size_t i = 0; i < offers.size(); ++i) {
        auto& o = offers[(i * 7919) % offers.size()];   // a permuted order
        uint64_t h = 0; for (int j : o.second) h ^= key[j];
        st.offer(bufs[omp_get_thread_num()], o.first, o.second.data(), (uint32_t)o.second.size(), h);
      }
      for (auto& b : bufs) st.flush(b);
      st.compact();
      bool ok = st.check_invariant() && st.size() == ref.size();
      for (size_t i = 0; ok && i < ref.size(); ++i) ok = same_bits(st.value(i), std::get<0>(ref[i])) && st.model(i) == std::get<1>(ref[i]);
      CHECKF(ok, "cap %zu threads %d buf %zu: size %zu vs %zu", cap, threads, lim, st.size(), ref.size());
    }
  }
}

// The island's concurrent store against WP1's reference v4::Store (INTERFACES §4.1) when every model has one value
// (the bit form): identical content, order and bits, in both orders.
TEST(store_equals_wp1_reference_store) {
  std::mt19937_64 g(23);
  std::vector<uint64_t> key(300); uint64_t x = 5; for (auto& k : key) k = splitmix64(x);
  std::map<Model, double> val;
  std::vector<Model> offers;
  for (int i = 0; i < 100000; ++i) {
    Model S = random_support(g, 300, 1 + (int)(g() % 5));
    if (!val.count(S)) val[S] = -std::floor((double)(g() % 5000) / 7.0);
    offers.push_back(S);
  }
  for (auto ord : {Order::HPM, Order::LEX}) for (uint64_t cap : {1ull, 13ull, 2000ull, 30000ull}) {
    v4::Store ref(cap, ord); TopStore st; st.init(cap, ord); st.buf_limit = 512; st.stage_limit = 3000;
    std::vector<StoreBuffer> bufs(3);
    for (auto& S : offers) ref.offer(val[S], S, D_hash(key, S));
    ref.compact();
    #pragma omp parallel for num_threads(3) schedule(dynamic, 64)
    for (size_t i = 0; i < offers.size(); ++i) {
      const Model& S = offers[offers.size() - 1 - i];
      st.offer(bufs[omp_get_thread_num()], val.at(S), S.data(), (uint32_t)S.size(), D_hash(key, S));
    }
    for (auto& b : bufs) st.flush(b);
    st.compact();
    bool ok = ref.size() == st.size() && st.check_invariant() && ref.check_invariants();
    for (size_t i = 0; ok && i < ref.size(); ++i) ok = same_bits(ref.v[i], st.value(i)) && Model(ref.model(i).begin(), ref.model(i).end()) == st.model(i);
    CHECKF(ok, "order %d cap %llu: sizes %zu vs %zu", (int)ord, (unsigned long long)cap, ref.size(), st.size());
  }
}

// ---------------------------------------------------------------------------------------------------------------
static IslandConfig small_cfg() {
  IslandConfig c; c.seed = 42; c.island = 3; c.N = 48; c.L = 2; c.Hm = 2; c.B = 14;
  c.grid = {0.0, 0.05, 0.15, 0.35, 0.65, 1.0};
  c.store_cap = 0; c.threads = 1; c.allow_test_kernels = true;
  return c;
}
template <Arith A>
static void t3_invariance(const char* tag) {
  Fixture F(100, 300, 21);
  IslandConfig c = small_cfg();
  c.kernel = KernelKind::ParticleMajor; c.threads = 1;
  IslandRun ref = run_island<A>(F.D, F.st, F.nb, c);
  CHECK(ref.status == 0);
  uint64_t h0 = ref.hash();
  std::printf("  [%s] reference hash %016llx logZ %.12f hpm |S|=%zu F=%.6f store %zu sweeps/round %.3f\n", tag, (unsigned long long)h0,
              ref.logZ, ref.hpm.S.size(), ref.hpm.F, ref.top_v.size(), 0.0);
  struct Conf { KernelKind k; int threads, G, tile; };
  std::vector<Conf> confs = {{KernelKind::ParticleMajor, 3, 1, 64},
                             {KernelKind::LabelMajor, 1, 48, 128}, {KernelKind::LabelMajor, 2, 48, 128}, {KernelKind::LabelMajor, 3, 48, 64},
                             {KernelKind::LabelMajor, 3, 1, 128}, {KernelKind::LabelMajor, 2, 7, 64}, {KernelKind::LabelMajor, 3, 16, 256}};
  for (auto& cf : confs) {
    IslandConfig d = c; d.kernel = cf.k; d.threads = cf.threads; d.G = cf.G; d.tile = cf.tile;
    IslandRun r = run_island<A>(F.D, F.st, F.nb, d);
    double M = r.ks.particle_rounds ? (double)r.ks.particle_sweeps / r.ks.particle_rounds : 0;
    CHECKF(r.hash() == h0, "[%s] kernel %d threads %d G %d tile %d: hash %016llx logZ %.17g vs %.17g", tag, (int)cf.k, cf.threads, cf.G,
              cf.tile, (unsigned long long)r.hash(), r.logZ, ref.logZ);
    std::printf("  [%s] kernel %s threads %d G %3d tile %3d: hash %016llx  M %.3f  pairs/(N p round) %.3f\n", tag,
                cf.k == KernelKind::LabelMajor ? "LM" : "PM", cf.threads, cf.G, cf.tile, (unsigned long long)r.hash(), M,
                r.ks.particle_rounds ? (double)r.ks.support_label_pairs / ((double)r.ks.particle_rounds * F.D.p) : 0.0);
  }
}
TEST(t3_invariance_bit) { t3_invariance<Arith::Bit>("bit"); }
TEST(t3_invariance_classA) { t3_invariance<Arith::ClassA>("A"); }

// I4-type check: logical counts equal the executed steps
TEST(logical_counts_and_invariants) {
  Fixture F(100, 300, 22);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  IslandRun r = run_island<Arith::Bit>(F.D, F.st, F.nb, c);
  int T = (int)c.grid.size() - 1;
  uint64_t held = r.logical[PH_FINAL_BRIDGE][ME_GIBBS_HELD];
  CHECK(held == (uint64_t)c.N * F.D.p * T);
  CHECK(r.logical[PH_BURN_IN][ME_GIBBS_HELD] == (uint64_t)c.N * F.D.p * c.L);
  CHECK(r.logical[PH_MEASURED][ME_GIBBS_HELD] == (uint64_t)c.N * F.D.p * c.Hm);
  CHECK(r.logical[PH_FINAL_INIT][ME_INIT] == (uint64_t)c.N);
  uint64_t g = 0; for (auto& s : r.stages) g += s.moves.gibbs; CHECK(g == held);
  // I4 (INTERFACES v0.1.5 §4.2, records.h i4_holds): logical events by mechanism = i4_expected(moves), per phase
  { MoveStats mb; for (auto& s : r.stages) add_moves(mb, s.moves);
    MoveStats mt, mm; for (int t2 = 0; t2 < (int)r.terminal_moves.size(); ++t2) add_moves(t2 < c.L ? mt : mm, r.terminal_moves[t2]);
    CHECK(v4::i4_holds(mb, r.logical[PH_FINAL_BRIDGE])); CHECK(v4::i4_holds(mt, r.logical[PH_BURN_IN])); CHECK(v4::i4_holds(mm, r.logical[PH_MEASURED]));
    CHECK(r.logical[PH_FINAL_BRIDGE][ME_GIBBS_FLIP] > r.logical[PH_FINAL_BRIDGE][ME_GIBBS_HELD] / 2); }   // ~2 events per Gibbs step
  // every bridge stage: one U, B N-swaps and one I per particle
  for (auto& s : r.stages) { CHECK(s.moves.us_exec + s.moves.us_self == (uint64_t)c.N); CHECK(s.moves.in_exec == (uint64_t)c.N);
                             CHECK(s.moves.ns_exec + s.moves.ns_self == (uint64_t)c.N * c.B); }
  // HPM: F(HPM) >= every store F; recomputed score equals the stored value (I2)
  CHECK(r.hpm.has && r.top_v.size() > 0 && r.hpm.F >= r.top_v[0]);
  BitScorer sc(&F.D); CHECK(same_bits(sc.score(r.hpm.S).logm, r.hpm.logm));
  CHECK(r.island_best == r.hpm.F);
  for (auto& s : r.stages) CHECK(s.ess >= 1 - 1e-9 && s.ess <= c.N + 1e-9);
  double sum = 0; for (double v : r.pip) { CHECK(v >= 0 && v <= 1 + 1e-12); sum += v; }
  std::printf("  sum of PIPs %.4f, HPM size %zu\n", sum, r.hpm.S.size());
}

// T6: interrupt after a checkpoint at several steps, resume (with other threads / G / kernel): identical bytes.
TEST(t6_restart_bit_identical) {
  Fixture F(100, 300, 23);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 2; c.G = 16;
  uint64_t h0 = run_island<Arith::Bit>(F.D, F.st, F.nb, c).hash();
  int Tsteps = (int)c.grid.size() - 1 + c.L + c.Hm;
  for (int stop : {0, 2, 5, 6, Tsteps - 1}) {
    IslandConfig a = c; a.ckpt_path = tmpdir() + "/wp3_t6_" + std::to_string(stop); a.ckpt_every_s = 1e9; a.stop_after_step = stop;
    std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
    IslandRun r1 = run_island<Arith::Bit>(F.D, F.st, F.nb, a);
    CHECK(r1.status == 1);
    IslandConfig b = a; b.stop_after_step = -1; b.threads = 3; b.G = 5; b.kernel = (stop % 2) ? KernelKind::ParticleMajor : KernelKind::LabelMajor;
    IslandRun r2 = run_island<Arith::Bit>(F.D, F.st, F.nb, b);
    CHECKF(r2.status == 0 && r2.resumed_from_step == stop && r2.hash() == h0, "stop %d: resumed %d hash %016llx vs %016llx", stop,
              r2.resumed_from_step, (unsigned long long)r2.hash(), (unsigned long long)h0);
    std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
  }
  // two generations: checkpoint every step; corrupt the newest; resume from the older one
  {
    IslandConfig a = c; a.ckpt_path = tmpdir() + "/wp3_t6_gen"; a.ckpt_every_s = 0; a.stop_after_step = 4;
    std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
    run_island<Arith::Bit>(F.D, F.st, F.nb, a);
    // step 4 was the 5th write (steps 0..4) -> file .a; corrupt one byte in its payload
    std::string newest = a.ckpt_path + ".a";
    FILE* f = std::fopen(newest.c_str(), "r+b"); CHECK(f != nullptr);
    if (f) { std::fseek(f, 100, SEEK_SET); int ch = std::fgetc(f); std::fseek(f, 100, SEEK_SET); std::fputc(ch ^ 0x5A, f); std::fclose(f); }
    IslandConfig b = a; b.stop_after_step = -1;
    IslandRun r2 = run_island<Arith::Bit>(F.D, F.st, F.nb, b);
    CHECKF(r2.resumed_from_step == 3 && r2.hash() == h0, "corrupt newest: resumed %d", r2.resumed_from_step);
    std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
  }
}


// island_r.bin: write, read back, compare with the run (record fields, store, HPM key, terminal supports); an
// interrupted run writes no estimate section (GUARD-W).
TEST(island_file_roundtrip_and_terminal_supports) {
  Fixture F(100, 300, 24);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  for (int arith = 0; arith < 2; ++arith) {
    IslandRun r = arith ? run_island<Arith::ClassA>(F.D, F.st, F.nb, c) : run_island<Arith::Bit>(F.D, F.st, F.nb, c);
    CHECK(r.status == 0 && (int)r.terminal.size() == c.N);
    std::string path = tmpdir() + "/wp3_island_rt.bin";
    v4::Json inputs = v4::Json::object(); inputs["data.bin"] = "test";
    write_island_file(path, r, arith ? Arith::ClassA : Arith::Bit, inputs);
    IslandFile f = read_island_file(path);
    const v4::IslandResult& o = f.rec;
    bool ok = o.status == v4::Status::completed && o.r == r.r && o.N == r.N && o.T == r.T && same_bits(o.logZ, r.logZ) &&
              o.stages.size() == r.stages.size() && o.rb_acc == r.rb_acc && o.pip == r.pip && o.rb_round == r.rb_round &&
              o.terminal_distinct == r.terminal_distinct && f.grid == r.grid && f.terminal == r.terminal;
    for (size_t i = 0; ok && i < r.stages.size(); ++i) ok = same_bits(o.stages[i].ess, r.stages[i].ess) && std::memcmp(&o.stages[i].moves, &r.stages[i].moves, sizeof(MoveStats)) == 0;
    ok = ok && o.led.top.size() == r.top_v.size() && o.led.hpmS == r.hpm.S && same_bits(o.led.hpmF, r.hpm.F) && o.led.hpm_ev.key == r.hpm.key &&
         same_bits(o.led.island_best[r.r], r.island_best) && std::memcmp(o.led.logical, r.logical, sizeof(r.logical)) == 0;
    for (size_t i = 0; ok && i < r.top_v.size(); ++i) ok = same_bits(o.led.top.v[i], r.top_v[i]);
    CHECKF(ok, "roundtrip arith %d", arith);
    // the terminal supports are the particles after the last measured round, in particle order
    CHECK(f.terminal.size() == (size_t)c.N && f.meta.at("mode").str() == (arith ? "V" : "law"));
    std::remove(path.c_str());
  }
  // interrupted run (stop after a checkpoint): no logZ / rb / pip / terminal sections
  IslandConfig a = c; a.ckpt_path = tmpdir() + "/wp3_island_rt_ck"; a.ckpt_every_s = 1e9; a.stop_after_step = 2;
  std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
  IslandRun ri = run_island<Arith::Bit>(F.D, F.st, F.nb, a);
  std::string path = tmpdir() + "/wp3_island_rt_int.bin";
  write_island_file(path, ri, Arith::Bit, v4::Json::object());
  { v4::fmt::Reader rd(path); CHECK(!rd.has("logZ") && !rd.has("rb_acc") && !rd.has("pip_r") && !rd.has("terminal_S") && rd.has("st_phi")); }
  std::remove(path.c_str()); std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
}

// Sol F2: ONE worker supplies ALL the winners. Thread 0 offers the c best of 3c models, threads 1-2 the 2c others (and
// re-offers), with small buffers and staging so that thread 0 flushes many times; content must equal WP1's reference.
TEST(store_one_worker_all_winners) {
  const uint64_t cap = 100000; const int M = 3 * (int)cap;
  std::vector<uint64_t> key(400); uint64_t x = 11; for (auto& k : key) k = splitmix64(x);
  std::vector<Model> models; models.reserve(M);
  std::mt19937_64 g(31);
  std::set<Model> seen;
  while ((int)models.size() < M) { Model S = random_support(g, 400, 2 + (int)(g() % 3)); if (seen.insert(S).second) models.push_back(S); }
  auto val = [&](int i) { return -(double)i * 0.25; };   // model i has value -i/4: the winners are 0..cap-1
  for (size_t lim : {(size_t)64, (size_t)65536}) {
    TopStore st; st.init(cap, Order::HPM); st.buf_limit = lim; st.stage_limit = std::max<size_t>(4096, lim * 2);
    std::vector<StoreBuffer> bufs(3);
    #pragma omp parallel num_threads(3)
    {
      int t = omp_get_thread_num();
      if (t == 0) { for (int i = (int)cap - 1; i >= 0; --i) st.offer(bufs[0], val(i), models[i].data(), (uint32_t)models[i].size(), D_hash(key, models[i])); }
      else { for (int rep = 0; rep < 2; ++rep) for (int i = (int)cap + t - 1; i < M; i += 2) st.offer(bufs[t], val(i), models[i].data(), (uint32_t)models[i].size(), D_hash(key, models[i])); }
    }
    for (int t = 0; t < 3; ++t) st.flush(bufs[t]);
    st.compact();
    v4::Store ref(cap, Order::HPM);
    for (int i = M - 1; i >= 0; --i) ref.offer(val(i), models[i], D_hash(key, models[i]));
    ref.compact();
    bool ok = st.size() == cap && ref.size() == cap && st.check_invariant();
    for (size_t i = 0; ok && i < cap; ++i) ok = same_bits(st.value(i), ref.v[i]) && st.model(i) == models[i];
    CHECKF(ok, "buffer %zu: size %zu, flushes %llu, merges %llu", lim, st.size(), (unsigned long long)st.n_flushes, (unsigned long long)st.n_merges);
    std::printf("  one worker, all winners: buffer %zu -> %llu flushes, %llu compactions, content = reference: %d\n", lim,
                (unsigned long long)st.n_flushes, (unsigned long long)st.n_merges, (int)ok);
  }
}

// T6 (Sol F5, manager item 7; D-21: stage boundaries): kills during a checkpoint write leave a temporary file and/or a
// torn newest generation -> the older generation is used; repeated resubmission; a checkpoint of another
// configuration is refused (invalid_input), never silently ignored.
TEST(t6_kill_during_write_resubmit_and_refusal) {
  Fixture F(100, 300, 25);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 2; c.G = 16;
  const uint64_t h0 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c).hash();
  const std::string base = tmpdir() + "/wp3_t6k";
  auto clean = [&]() { for (const char* s : {".a", ".b", ".b.tmp.12345", ".a.tmp.12345"}) std::remove((base + s).c_str()); };
  // (1) checkpoint every step, stop after step 4 (writes 0 a, 1 b, 2 a, 3 b, 4 a); then a "kill" during the next
  //     write: a partial temporary file, and the newest generation torn to half its length
  clean();
  IslandConfig a = c; a.ckpt_path = base; a.ckpt_every_s = 0; a.stop_after_step = 4;
  CHECK(run_island<Arith::ClassA>(F.D, F.st, F.nb, a).status == 1);
  { FILE* f = std::fopen((base + ".b.tmp.12345").c_str(), "wb"); std::fputs("partial", f); std::fclose(f); }
  { FILE* f = std::fopen((base + ".a").c_str(), "rb"); std::fseek(f, 0, SEEK_END); long n = std::ftell(f); std::fclose(f);
    CHECK(::truncate((base + ".a").c_str(), n / 2) == 0); }
  IslandConfig b = a; b.stop_after_step = -1; b.threads = 3; b.G = 7;
  IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, b);
  CHECKF(r.status == 0 && r.resumed_from_step == 3 && r.hash() == h0, "torn newest: resumed %d", r.resumed_from_step);
  // (2) repeated resubmission: stop at 2, resume and stop at 6, resume to the end
  clean();
  a.stop_after_step = 2; a.ckpt_every_s = 1e9;
  CHECK(run_island<Arith::ClassA>(F.D, F.st, F.nb, a).status == 1);
  IslandConfig a2 = a; a2.stop_after_step = 6; a2.kernel = KernelKind::ParticleMajor;
  IslandRun r2 = run_island<Arith::ClassA>(F.D, F.st, F.nb, a2);
  CHECK(r2.status == 1 && r2.resumed_from_step == 2);
  IslandConfig a3 = a; a3.stop_after_step = -1; a3.threads = 1; a3.G = 48;
  IslandRun r3 = run_island<Arith::ClassA>(F.D, F.st, F.nb, a3);
  CHECKF(r3.status == 0 && r3.resumed_from_step == 6 && r3.hash() == h0, "resubmission: resumed %d", r3.resumed_from_step);
  // (3) a checkpoint of another configuration (seed) is refused
  clean();
  a.stop_after_step = 2;
  run_island<Arith::ClassA>(F.D, F.st, F.nb, a);
  IslandConfig other = a; other.seed = a.seed + 1; other.stop_after_step = -1;
  bool refused = false;
  try { run_island<Arith::ClassA>(F.D, F.st, F.nb, other); } catch (const v4::Error& e) { refused = e.st == v4::Status::invalid_input; }
  CHECK(refused);
  clean();
}
