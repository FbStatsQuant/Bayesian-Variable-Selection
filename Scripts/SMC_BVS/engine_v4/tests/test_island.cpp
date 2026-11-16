// test_island.cpp -- WP3 unit tests: Philox KAT, flip kernels (bit form = scorer bits; class A <= 1e-9), class-A
// log/exp, the concurrent store (order-free, multi-thread), T3 execution invariance, T6 restart.
#include <omp.h>
#include <cstdio>
#include <map>
#include <random>
#include <set>
#include "island_tk.h"
#include "v4/island/island.h"

using namespace v4::island;

static bool same_bits(double a, double b) { return std::memcmp(&a, &b, 8) == 0; }
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
    uint32_t o[4]; Philox4x32::gen(t.c, t.k, o);
    for (int i = 0; i < 4; ++i) CHECK_MSG(o[i] == t.o[i], "word %d: %08x vs %08x", i, o[i], t.o[i]);
  }
  // address packing (INTERFACES §3) and uniform range
  Address a; a.seed = 7; a.role = R_FINAL; a.island = 3; a.xph = X_BRIDGE; a.stage = 5; a.particle = 11; a.position = 13; a.slot = 2;
  uint32_t c[4], k[2]; address_words(a, c, k);
  CHECK(k[0] == 7 && k[1] == 3 && c[0] == 2 && c[1] == 13 && c[2] == 11 && c[3] == ((2u << 24) | 5u));
  double u = uniform_at(a); CHECK(u >= 0 && u < 1);
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
      v8d u[KM];
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
      TopStore st; st.init(cap, Order::HPM); st.buf_limit = lim;
      std::vector<StoreBuffer> bufs(threads);
      #pragma omp parallel for num_threads(threads) schedule(dynamic, 97)
      for (size_t i = 0; i < offers.size(); ++i) {
        auto& o = offers[(i * 7919) % offers.size()];   // a permuted order
        uint64_t h = 0; for (int j : o.second) h ^= key[j];
        st.offer(bufs[omp_get_thread_num()], o.first, o.second.data(), (uint32_t)o.second.size(), h);
      }
      for (auto& b : bufs) st.merge_buffer(b);
      bool ok = st.check_invariant() && st.size() == ref.size();
      for (size_t i = 0; ok && i < ref.size(); ++i) ok = same_bits(st.v[i], std::get<0>(ref[i])) && st.model(i) == std::get<1>(ref[i]);
      CHECK_MSG(ok, "cap %zu threads %d buf %zu: size %zu vs %zu", cap, threads, lim, st.size(), ref.size());
    }
  }
}

// ---------------------------------------------------------------------------------------------------------------
static IslandConfig small_cfg() {
  IslandConfig c; c.seed = 42; c.island = 3; c.N = 48; c.L = 2; c.Hm = 2; c.B = 14;
  c.grid = {0.0, 0.05, 0.15, 0.35, 0.65, 1.0};
  c.store_cap = 0; c.threads = 1;
  return c;
}
template <Arith A>
static void t3_invariance(const char* tag) {
  Fixture F(100, 300, 21);
  IslandConfig c = small_cfg();
  c.kernel = KernelKind::ParticleMajor; c.threads = 1;
  IslandResult ref = run_island<A>(F.D, F.st, F.nb, c);
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
    IslandResult r = run_island<A>(F.D, F.st, F.nb, d);
    double M = r.ks.particle_rounds ? (double)r.ks.particle_sweeps / r.ks.particle_rounds : 0;
    CHECK_MSG(r.hash() == h0, "[%s] kernel %d threads %d G %d tile %d: hash %016llx logZ %.17g vs %.17g", tag, (int)cf.k, cf.threads, cf.G,
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
  IslandResult r = run_island<Arith::Bit>(F.D, F.st, F.nb, c);
  int T = (int)c.grid.size() - 1;
  uint64_t held = r.logical[PH_FINAL_BRIDGE][ME_GIBBS_HELD];
  CHECK(held == (uint64_t)c.N * F.D.p * T);
  CHECK(r.logical[PH_BURN_IN][ME_GIBBS_HELD] == (uint64_t)c.N * F.D.p * c.L);
  CHECK(r.logical[PH_MEASURED][ME_GIBBS_HELD] == (uint64_t)c.N * F.D.p * c.Hm);
  CHECK(r.logical[PH_FINAL_INIT][ME_INIT] == (uint64_t)c.N);
  uint64_t g = 0; for (auto& s : r.stages) g += s.moves.gibbs; CHECK(g == held);
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
    IslandResult r1 = run_island<Arith::Bit>(F.D, F.st, F.nb, a);
    CHECK(r1.status == 1);
    IslandConfig b = a; b.stop_after_step = -1; b.threads = 3; b.G = 5; b.kernel = (stop % 2) ? KernelKind::ParticleMajor : KernelKind::LabelMajor;
    IslandResult r2 = run_island<Arith::Bit>(F.D, F.st, F.nb, b);
    CHECK_MSG(r2.status == 0 && r2.resumed_from_step == stop && r2.hash() == h0, "stop %d: resumed %d hash %016llx vs %016llx", stop,
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
    IslandResult r2 = run_island<Arith::Bit>(F.D, F.st, F.nb, b);
    CHECK_MSG(r2.resumed_from_step == 3 && r2.hash() == h0, "corrupt newest: resumed %d", r2.resumed_from_step);
    std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
  }
}

int main(int argc, char** argv) { return tk::run_all(argc, argv); }
