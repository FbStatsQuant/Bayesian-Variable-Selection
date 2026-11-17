// test_island.cpp -- WP3 unit tests: Philox KAT, flip kernels (bit form = scorer bits; class A <= 1e-9), class-A
// log/exp, the concurrent store (order-free, multi-thread), T3 execution invariance, T6 restart.
#include <omp.h>
#include <execinfo.h>
#include <atomic>
#include <cstdlib>
#include <cstdio>
#include <filesystem>
#include <map>
#include <random>
#include <set>
#include <unistd.h>
#include "tk.h"
#include "tutil.h"
#include "tutil_island.h"
#include "v4/island/island.h"
#include "v4/island/ckpt_sum.h"
#include "v4/island/island_file.h"
#include "v4/format.h"

using namespace v4::island;

// (the predicates below use omp_get_level() > 0, not omp_in_parallel(): inside a num_threads(1) team the region is inactive and
// omp_in_parallel() is false, so a 1-thread run would never count -- review PR53/61 MINOR A-1)
// Allocation-failure injection (review PR48 finding 1): while g_par_new_countdown > 0, the countdown-th operator new
// called inside an active OpenMP parallel region throws std::bad_alloc. Off (0) for every other test. A real failure at
// an unguarded site inside a region escapes the structured block and aborts the whole test binary (std::terminate).
static std::atomic<long> g_par_new_countdown{0};
// Allocation probe (review PR46 MAJOR-2): while g_new_track is set, every operator new is counted (calls, bytes, largest).
static std::atomic<bool> g_new_track{false};
static std::atomic<uint64_t> g_new_calls{0}, g_new_bytes{0}, g_new_max{0};
// Allocation counter for tests of allocation-free paths (PR50 MAJOR-1, tests/test_setup.cpp): while g_count_allocs is set,
// every operator new on any thread increments g_allocs. Off for every other test.
std::atomic<bool> g_count_allocs{false};
std::atomic<uint64_t> g_allocs{0};
static std::atomic<bool> g_order_phase{false};      // set by the island around the label-major order phase's parallel region
static std::atomic<long> g_order_allocs{0};         // operator-new calls inside that region
void* operator new(std::size_t n) {
  if (g_order_phase.load(std::memory_order_relaxed) && omp_get_level() > 0) g_order_allocs.fetch_add(1, std::memory_order_relaxed);
  if (g_new_track.load(std::memory_order_relaxed)) {
    g_new_calls.fetch_add(1); g_new_bytes.fetch_add(n);
    uint64_t m = g_new_max.load(); while (n > m && !g_new_max.compare_exchange_weak(m, n)) {}
  }
  if (g_count_allocs.load(std::memory_order_relaxed)) g_allocs.fetch_add(1, std::memory_order_relaxed);
  if (g_par_new_countdown.load(std::memory_order_relaxed) > 0 && omp_get_level() > 0 && g_par_new_countdown.fetch_sub(1) == 1) {
    if (std::getenv("V4_DEBUG_INJECT")) { void* bt[32]; int nb = backtrace(bt, 32); std::fprintf(stderr, "== injected\n"); backtrace_symbols_fd(bt, nb, 2); }
    throw std::bad_alloc(); }
  if (void* q = std::malloc(n ? n : 1)) return q;
  throw std::bad_alloc();
}
void operator delete(void* q) noexcept { std::free(q); }
void operator delete(void* q, std::size_t) noexcept { std::free(q); }

// Temporary files (manager 11-16): pid-suffixed names under $TMPDIR through tests/tutil.h tmp_path(), never "." -- the
// island tests refuse to run without TMPDIR -- and every file is removed when the test ends (TmpGuard), even on failure.
static std::string wp3_tmp(const std::string& name) {
  const char* t = std::getenv("TMPDIR");
  if (!t || !*t) throw std::runtime_error("TMPDIR is not set: the island tests write temporary files only under $TMPDIR");
  return tmp_path("wp3_" + name);
}
// removes a file, or a checkpoint base's generations <base>.a/.b and any leftover <base>.{a,b}.tmp.<pid>
static void wp3_rm(const std::string& base) {
  std::error_code ec;
  for (const char* sfx : {"", ".a", ".b"}) std::filesystem::remove(base + sfx, ec);
  std::filesystem::path bp(base);
  const std::string stem = bp.filename().string();
  for (auto& de : std::filesystem::directory_iterator(bp.parent_path(), ec)) {
    const std::string fn = de.path().filename().string();
    if (fn.rfind(stem + ".a.tmp.", 0) == 0 || fn.rfind(stem + ".b.tmp.", 0) == 0 || fn.rfind(stem + ".tmp.", 0) == 0) std::filesystem::remove(de.path(), ec);
  }
}
struct TmpGuard {
  std::vector<std::string> paths;
  const std::string& add(const std::string& p) { paths.push_back(p); return paths.back(); }
  ~TmpGuard() { for (auto& p : paths) wp3_rm(p); }
};

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
    // K2: the slot word (philox8_word word 0), with extreme 32-bit lane values included
    uint32_t sl[8]; for (int l = 0; l < 8; ++l) sl[l] = l < 2 ? (l ? 0xFFFFFFFFu : 0u) : (uint32_t)g();
    b.position = (uint32_t)g(); c = v4::address_ctr(b); kk = v4::address_key(b);
    philox8_word(c.data(), kk.data(), 0, sl, u8);
    for (int l = 0; l < 8; ++l) { Address e = b; e.slot = sl[l]; ok = ok && same_bits(u8[l], uniform_at(e)); }
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

// K1 (WP6, WP3_ARCH_REVIEW §2.1): bounded scoring, bounded scan and one-particle phase B give the dense label-major
// output bits, both arithmetic forms, any threads / G / tile; with the NaN-row test on (score rows poisoned before every
// pass: a read of a value not computed in the pass is an internal_error) and fewer flip evaluations than dense.
template <Arith A>
static void bounded_same_bits(const char* tag) {
  Fixture F(100, 300, 41);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 48; c.bounded_scoring = false;
  IslandRun dense = run_island<A>(F.D, F.st, F.nb, c);
  CHECK(dense.status == 0);
  const uint64_t h0 = dense.hash();
  struct Conf { int threads, G, tile; };
  for (const Conf& cf : std::vector<Conf>{{1, 48, 128}, {3, 48, 64}, {2, 7, 128}, {3, 1, 64}, {3, 16, 256}}) {
    IslandConfig d = c; d.bounded_scoring = true; d.test_nan_rows = true; d.threads = cf.threads; d.G = cf.G; d.tile = cf.tile;
    IslandRun r = run_island<A>(F.D, F.st, F.nb, d);
    CHECKF(r.status == 0 && r.hash() == h0, "[%s] threads %d G %d tile %d: status %d hash %016llx vs dense %016llx", tag, cf.threads, cf.G, cf.tile,
           r.status, (unsigned long long)r.hash(), (unsigned long long)h0);
    CHECKF(r.ks.flip_evals < dense.ks.flip_evals, "[%s] flip evaluations %llu (bounded) vs %llu (dense)", tag, (unsigned long long)r.ks.flip_evals,
           (unsigned long long)dense.ks.flip_evals);
    std::printf("  [%s] threads %d G %3d tile %3d: hash %016llx = dense; flip evaluations %llu vs dense %llu\n", tag, cf.threads, cf.G, cf.tile,
                (unsigned long long)r.hash(), (unsigned long long)r.ks.flip_evals, (unsigned long long)dense.ks.flip_evals);
  }
  // the dense path also passes the NaN-row test (it writes every entry it reads)
  IslandConfig d = c; d.test_nan_rows = true;
  CHECK(run_island<A>(F.D, F.st, F.nb, d).hash() == h0);
}
TEST(bounded_scoring_same_bits_bit) { bounded_same_bits<Arith::Bit>("bit"); }
TEST(bounded_scoring_same_bits_classA) { bounded_same_bits<Arith::ClassA>("A"); }

// K3 (WP3_ARCH_REVIEW §2.2): Gram rows kept across passes give the dense output bits with any number of slots
// (auto, a few: columns without a slot fall back to per-pass products, off), both forms, threads 1 / 3, G 1 / 16 / 48
template <Arith A>
static void gram_rows_same_bits(const char* tag) {
  Fixture F(100, 300, 42);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 48; c.bounded_scoring = false;
  const uint64_t h0 = run_island<A>(F.D, F.st, F.nb, c).hash();
  struct Conf { int slots, threads, G; };
  for (const Conf& cf : std::vector<Conf>{{-1, 3, 48}, {-1, 1, 16}, {3, 3, 48}, {3, 1, 1}, {0, 3, 48}, {400, 3, 16}}) {
    IslandConfig d = c; d.bounded_scoring = true; d.test_nan_rows = true; d.gram_slots = cf.slots; d.threads = cf.threads; d.G = cf.G;
    IslandRun r = run_island<A>(F.D, F.st, F.nb, d);
    const auto& k = r.ks;
    CHECKF(r.status == 0 && r.hash() == h0, "[%s] slots %d threads %d G %d: hash %016llx vs dense %016llx", tag, cf.slots, cf.threads, cf.G,
           (unsigned long long)r.hash(), (unsigned long long)h0);
    if (cf.slots != 0) CHECKF(k.gram_rows_reused > 0 && k.gram_rows_new > 0, "[%s] slots %d: no Gram row reused", tag, cf.slots);
    if (cf.slots == 3) CHECKF(k.gram_rows_noslot > 0, "[%s] 3 slots: the no-slot fallback was not exercised", tag);
    if (cf.slots == 0) CHECK(k.gram_rows_new + k.gram_rows_reused + k.gram_rows_noslot == 0);
    std::printf("  [%s] slots %3d (used %d) threads %d G %2d: hash %016llx = dense; Gram rows computed %llu reused %llu no slot %llu\n", tag, cf.slots,
                gram_slots_of(d, cf.G, F.D.p), cf.threads, cf.G, (unsigned long long)r.hash(), (unsigned long long)k.gram_rows_new,
                (unsigned long long)k.gram_rows_reused, (unsigned long long)k.gram_rows_noslot);
  }
  // the memory plan carries the term, and only when the slots are in use
  auto plan_has = [&](const IslandConfig& x) { for (auto& it : plan_island(F.D, F.st, x).items) if (it.name == "gram_rows") return it.bytes; return (uint64_t)0; };
  IslandConfig d = c; d.bounded_scoring = true; d.G = 48;
  CHECK(plan_has(d) == (uint64_t)gram_slots_of(d, 48, F.D.p) * F.D.p * 8 && gram_slots_of(d, 48, F.D.p) == 120);
  d.gram_slots = 0; CHECK(plan_has(d) == 0);
  d.gram_slots = -1; d.bounded_scoring = false; CHECK(plan_has(d) == 0);
}
TEST(gram_rows_same_bits_bit) { gram_rows_same_bits<Arith::Bit>("bit"); }
TEST(gram_rows_same_bits_classA) { gram_rows_same_bits<Arith::ClassA>("A"); }

// review PR48 finding 1: an allocation failure anywhere inside the label-major parallel regions (the k-th allocation in a
// region, for k over the run) ends the island with resource_limit, never std::terminate; bounded and dense paths
TEST(lm_alloc_failure_in_parallel_is_resource_limit) {
  Fixture F(100, 300, 43);
  int hit = 0, runs = 0;
  for (bool bounded : {true, false}) for (long k = 1; k <= 400000; k = k * 2 + 1) {
    IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16; c.bounded_scoring = bounded;
    g_par_new_countdown.store(k);
    IslandRun r; bool threw = false; std::string what;
    try { r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c); } catch (const std::exception& e) { threw = true; what = e.what(); }
    const bool injected = g_par_new_countdown.exchange(0) <= 0;
    ++runs;
    if (!injected) { CHECKF(!threw && r.status == 0, "k %ld: no injection, status %d", k, r.status); continue; }
    ++hit;
    CHECKF(!threw && r.status == 3 && r.reason.find("out of memory") != std::string::npos, "bounded %d k %ld: threw %d ('%s') status %d '%s'",
           (int)bounded, k, (int)threw, what.c_str(), r.status, r.reason.c_str());
  }
  CHECKF(hit >= 10, "only %d of %d runs reached the injected allocation", hit, runs);
  std::printf("  %d runs, %d with an injected in-region allocation failure: all resource_limit\n", runs, hit);
}

// review PR61 MINOR B-1: the phase-B consumer tie K5 depends on (the first consumer of a shared support is the smallest
// PARTICLE, not the smallest slot) is observable. The log records, per (round, flip model), the smallest first consumer
// (particle, position): what an event key's provenance is made of, and invariant under how the particles are grouped into
// passes. It is equal between rolling admission and groups, and the deliberate bug (consumers in slot order) changes it. The
// final hash alone does not see the tie (event keys reach it only through the HPM provenance).
template <Arith A>
static void rolling_consumer_digest(const char* tag) {
  Fixture F(100, 300, 47);
  auto run = [&](bool rolling, int G, int th, bool bug) {
    ConsumerLog log;
    IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = th; c.G = G; c.rolling_admission = rolling;
    c.test_consumers = &log; c.test_consumers_by_slot = bug;
    IslandRun r = run_island<A>(F.D, F.st, F.nb, c);
    CHECK(r.status == 0);
    uint64_t dg = 0; for (auto& [k, v] : log.first) { uint64_t x = k ^ (v * 0xD6E8FEB86659FD93ull); dg += v4::splitmix64(x); }
    return std::make_tuple(dg, r.hash(), log.first.size());
  };
  int caught = 0;
  for (int G : {5, 7, 16}) for (int th : {1, 3}) {
    const auto g = run(false, G, th, false), r = run(true, G, th, false), bug = run(true, G, th, true);
    const bool same = std::get<0>(r) == std::get<0>(g) && std::get<1>(r) == std::get<1>(g) && std::get<2>(r) == std::get<2>(g);
    CHECKF(same, "[%s] G %d threads %d: consumer log rolling %016llx (%zu models) vs groups %016llx (%zu)", tag, G, th, (unsigned long long)std::get<0>(r),
           std::get<2>(r), (unsigned long long)std::get<0>(g), std::get<2>(g));
    CHECKF(std::get<1>(bug) == std::get<1>(g), "[%s] G %d: the slot-order bug changed the output hash (it should only change the log)", tag, G);
    if (std::get<0>(bug) != std::get<0>(g)) ++caught;
    std::printf("  [%s] G %2d threads %d: %zu (round, model) entries, log %016llx rolling %s groups; consumers-by-slot bug: %016llx%s\n", tag, G, th,
                std::get<2>(g), (unsigned long long)std::get<0>(r), same ? "=" : "!=", (unsigned long long)std::get<0>(bug), std::get<0>(bug) != std::get<0>(g) ? " (differs)" : " (same)");
  }
  CHECKF(caught == 6, "[%s] the slot-order bug was caught in only %d of 6 legs", tag, caught);
}
TEST(rolling_consumer_order_observable_bit) { rolling_consumer_digest<Arith::Bit>("bit"); }
TEST(rolling_consumer_order_observable_classA) { rolling_consumer_digest<Arith::ClassA>("A"); }

// review PR61 MINOR B-2, PR66 MINOR 1 / 2: after a numerical failure rolling admission admits no more particles (the groups
// kernel stops after the failing group). A failed island reports the same status, reason and law outputs as groups (hash() with
// the default keep_terminal: the in-memory partial population is cleared on failure); the work counters (particle-rounds) are
// execution diagnostics and differ, in either direction, from groups. What holds in general: rolling with the stop admits a
// prefix of what rolling without it admits (test_no_stop_admitting), so it never runs more; and in the first window (the failing
// particle is index 0) it runs at most G.
TEST(rolling_stops_admitting_after_failure) {
  Fixture F(100, 300, 32);
  auto compare = [&](const char* tag, const v4::Data& D, const Start& st, IslandConfig c, int victim, bool first_window) {
    c.kernel = KernelKind::LabelMajor;
    const int G = c.G, th = c.threads;
    c.rolling_admission = false; IslandRun g = run_island<Arith::ClassA>(D, st, F.nb, c);
    c.rolling_admission = true; c.test_no_stop_admitting = true; IslandRun r0 = run_island<Arith::ClassA>(D, st, F.nb, c);
    c.test_no_stop_admitting = false; IslandRun r = run_island<Arith::ClassA>(D, st, F.nb, c);
    CHECKF(g.status == 2 && r.status == 2 && r0.status == 2 && r.reason == g.reason && r0.reason == g.reason,
           "[%s] victim %d G %d threads %d: status %d / %d / %d, rolling '%s' vs groups '%s'", tag, victim, G, th, r.status, r0.status, g.status, r.reason.c_str(), g.reason.c_str());
    CHECKF(r.hash() == g.hash() && r0.hash() == g.hash() && r.terminal.empty(), "[%s] victim %d G %d threads %d: failed-run hash %016llx (no stop %016llx) vs groups %016llx",
           tag, victim, G, th, (unsigned long long)r.hash(), (unsigned long long)r0.hash(), (unsigned long long)g.hash());
    CHECKF(r.ks.particle_rounds <= r0.ks.particle_rounds, "[%s] victim %d G %d threads %d: %llu particle-rounds with the stop vs %llu without it", tag, victim, G, th,
           (unsigned long long)r.ks.particle_rounds, (unsigned long long)r0.ks.particle_rounds);
    if (first_window) CHECKF(r.ks.particle_rounds <= (uint64_t)G, "[%s] G %d threads %d: rolling ran %llu particle-rounds after a failure in its first window", tag, G, th,
                             (unsigned long long)r.ks.particle_rounds);
    else if (victim + 2 * G < c.N) CHECKF(r.ks.particle_rounds < r0.ks.particle_rounds, "[%s] victim %d G %d threads %d: the stop saved nothing (%llu = %llu)", tag, victim, G, th,
                                          (unsigned long long)r.ks.particle_rounds, (unsigned long long)r0.ks.particle_rounds);
    std::printf("  [%s] victim %2d G %2d threads %d: particle-rounds rolling %llu (no stop %llu), groups %llu; same status, reason, hash\n", tag, victim, G, th,
                (unsigned long long)r.ks.particle_rounds, (unsigned long long)r0.ks.particle_rounds, (unsigned long long)g.ks.particle_rounds);
  };
  // (1) poisoned labels: the failing particle is index 0, in the first window
  const std::vector<int> bad = {37, 151, 222};
  auto own = std::make_shared<v4::DataOwned>();
  own->X.assign(F.D.Xs, F.D.Xs + (size_t)F.D.n * F.D.p); own->y.assign(F.D.ys, F.D.ys + F.D.n);
  for (int j : bad) for (int i = 0; i < F.D.n; ++i) own->X[(size_t)j * F.D.n + i] *= 1e200;
  v4::Data D2 = v4::make_data(own, F.D.n, F.D.p);
  Start st2 = F.st;
  for (int j : bad) { int b = st2.blk[j]; for (size_t code = 0; code < st2.logr[b].size(); ++code) if (code & (1u << st2.pos[j])) st2.logr[b][code] = NEG_INF; }
  build_sampler(st2, F.D);
  for (int G : {5, 16}) for (int th : {1, 3}) {
    IslandConfig c = small_cfg(); c.threads = th; c.G = G;
    compare("poisoned", D2, st2, c, 0, true);
  }
  // (2) a late victim (the I proposal of particle `victim` fails in bridge stage s): the failure is recorded after later
  // particles were admitted, some of the particles already running finish, and the work counters differ from groups
  for (int stage : {1, 2}) for (int victim : {5, 20, 37}) for (int G : {5, 16}) for (int th : {1, 3}) {
    IslandConfig c = small_cfg(); c.threads = th; c.G = G; c.test_fail_indep = victim; c.test_fail_indep_stage = stage;
    compare(stage == 1 ? "late s1" : "late s2", F.D, F.st, c, victim, false);
  }
}

// K2: label-major draws and scores the I proposal in the order phase; a failed score must surface where core's serial
// round fails (the walk reaching the I position), with the same reason as particle-major, any threads / G
TEST(indep_proposal_failure_deferred_to_its_position) {
  Fixture F(100, 300, 44);
  for (int arith = 0; arith < 2; ++arith) for (int victim : {0, 5, 37}) {
    std::string reason0;
    struct Conf { KernelKind k; int threads, G; };
    for (const Conf& cf : std::vector<Conf>{{KernelKind::ParticleMajor, 1, 1}, {KernelKind::LabelMajor, 1, 48}, {KernelKind::LabelMajor, 3, 16},
                                            {KernelKind::LabelMajor, 3, 7}}) {
      IslandConfig c = small_cfg(); c.kernel = cf.k; c.threads = cf.threads; c.G = cf.G; c.test_fail_indep = victim; c.test_fail_indep_stage = 2;
      IslandRun r = arith ? run_island<Arith::ClassA>(F.D, F.st, F.nb, c) : run_island<Arith::Bit>(F.D, F.st, F.nb, c);
      if (reason0.empty()) { reason0 = r.reason; std::printf("  [%s] victim %d: %s\n", arith ? "A" : "bit", victim, r.reason.c_str()); }
      CHECKF(r.status == 2 && r.reason.find("test hook: I proposal") != std::string::npos && r.reason == reason0,
             "arith %d victim %d kernel %d threads %d G %d: status %d '%s' vs '%s'", arith, victim, (int)cf.k, cf.threads, cf.G, r.status,
             r.reason.c_str(), reason0.c_str());
    }
  }
}

// K5 (WP3_ARCH_REVIEW §2 lever 5): rolling admission (a finished particle's slot takes the next particle) gives the
// output bits of groups run one after the other, both forms, threads 1 / 3, G < N, dense and bounded, with fewer passes
template <Arith A>
static void rolling_same_bits(const char* tag) {
  Fixture F(100, 300, 45);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16; c.rolling_admission = false;
  IslandRun g = run_island<A>(F.D, F.st, F.nb, c);
  CHECK(g.status == 0);
  struct Conf { int threads, G; bool bounded; };
  for (const Conf& cf : std::vector<Conf>{{3, 16, true}, {1, 7, true}, {3, 5, false}, {2, 48, true}, {3, 1, true}}) {
    IslandConfig d = c; d.rolling_admission = true; d.threads = cf.threads; d.G = cf.G; d.bounded_scoring = cf.bounded; d.test_nan_rows = true;
    IslandRun r = run_island<A>(F.D, F.st, F.nb, d);
    d.rolling_admission = false; d.test_nan_rows = false; IslandRun r0 = run_island<A>(F.D, F.st, F.nb, d);
    CHECKF(r.status == 0 && r.hash() == g.hash(), "[%s] threads %d G %d bounded %d: hash %016llx vs groups %016llx", tag, cf.threads, cf.G, (int)cf.bounded,
           (unsigned long long)r.hash(), (unsigned long long)g.hash());
    CHECKF(r.ks.particle_rounds == r0.ks.particle_rounds && r.ks.particle_sweeps == r0.ks.particle_sweeps, "[%s] G %d: rounds / sweeps differ", tag, cf.G);
    if (cf.G < c.N && cf.G > 1) CHECKF(r.ks.passes < r0.ks.passes, "[%s] G %d: passes %llu (rolling) vs %llu (groups)", tag, cf.G,
                                       (unsigned long long)r.ks.passes, (unsigned long long)r0.ks.passes);
    std::printf("  [%s] threads %d G %2d bounded %d: hash %016llx = groups; passes %llu (groups %llu), supports per pass %.1f (groups %.1f)\n", tag,
                cf.threads, cf.G, (int)cf.bounded, (unsigned long long)r.hash(), (unsigned long long)r.ks.passes, (unsigned long long)r0.ks.passes,
                (double)r.ks.supports / std::max<uint64_t>(1, r.ks.passes), (double)r0.ks.supports / std::max<uint64_t>(1, r0.ks.passes));
  }
}
TEST(rolling_admission_same_bits_bit) { rolling_same_bits<Arith::Bit>("bit"); }
TEST(rolling_admission_same_bits_classA) { rolling_same_bits<Arith::ClassA>("A"); }

// review PR53 MAJOR: the label-major order phase (inverse orders, nongibbs lists, the I proposals' pi_0 draws and scores)
// allocates nothing inside its parallel region: everything is sized serially before it, cold and warm, both forms,
// threads 1 / 3, G < N. Counted by the replaced operator new while the island's test flag is set.
template <Arith A>
static void order_phase_no_alloc(const char* tag) {
  Fixture F(100, 300, 46);
  // control: the counter sees an allocation made in a region while the flag is set (and not otherwise)
  g_order_allocs = 0; g_order_phase = true;
  #pragma omp parallel num_threads(3)
  { int* q = new int[100]; asm volatile("" : : "r"(q) : "memory"); delete[] q; }
  g_order_phase = false;
  CHECKF(g_order_allocs.load() >= 3, "[%s] control: the counting hook did not see %ld in-region allocations", tag, g_order_allocs.load());
  // the same at one thread (omp_in_parallel() is false inside a num_threads(1) team: the hook uses omp_get_level())
  g_order_allocs = 0; g_order_phase = true;
  #pragma omp parallel num_threads(1)
  { int* q = new int[100]; asm volatile("" : : "r"(q) : "memory"); delete[] q; }
  g_order_phase = false;
  CHECKF(g_order_allocs.load() >= 1, "[%s] control: the counting hook did not see the allocation of a 1-thread region (%ld)", tag, g_order_allocs.load());
  for (int th : {1, 3}) for (int G : {16, 48}) {
    IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = th; c.G = G; c.test_order_phase = &g_order_phase;
    g_order_allocs = 0;
    IslandRun r = run_island<A>(F.D, F.st, F.nb, c);
    const long n = g_order_allocs.exchange(0);
    CHECKF(r.status == 0 && n == 0, "[%s] threads %d G %d: %ld allocations inside the order phase's parallel region (status %d)", tag, th, G, n, r.status);
    std::printf("  [%s] threads %d G %2d: %llu particle-rounds, %ld allocations in the order phase's region\n", tag, th, G, (unsigned long long)r.ks.particle_rounds, n);
  }
}
TEST(order_phase_allocates_nothing_in_parallel_bit) { order_phase_no_alloc<Arith::Bit>("bit"); }
TEST(order_phase_allocates_nothing_in_parallel_classA) { order_phase_no_alloc<Arith::ClassA>("A"); }

// negative control of the NaN-row test: bounded scoring that skips the position just below the running first change
// (test_bound_shrink = 1) consumes unscored values; the test must catch it as an internal_error
TEST(nan_rows_catch_an_unscored_read) {
  Fixture F(100, 300, 41);
  for (int th : {1, 3}) {
    IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = th; c.G = 48; c.test_nan_rows = true; c.test_bound_shrink = 1;
    bool caught = false; std::string what;
    try { (void)run_island<Arith::ClassA>(F.D, F.st, F.nb, c); }
    catch (const v4::Error& e) { caught = e.st == v4::Status::internal_error && std::string(e.what()).find("NaN-row test") != std::string::npos; what = e.what(); }
    CHECKF(caught, "threads %d: the deliberate unscored read was not caught ('%s')", th, what.c_str());
    std::printf("  threads %d: caught: %s\n", th, what.c_str());
  }
}

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
  TmpGuard tg;
  Fixture F(100, 300, 23);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 2; c.G = 16;
  uint64_t h0 = run_island<Arith::Bit>(F.D, F.st, F.nb, c).hash();
  int Tsteps = (int)c.grid.size() - 1 + c.L + c.Hm;
  for (int stop : {0, 2, 5, 6, Tsteps - 1}) {
    IslandConfig a = c; a.ckpt_path = tg.add(wp3_tmp("t6_" + std::to_string(stop))); a.ckpt_every_s = 1e9; a.stop_after_step = stop;
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
    IslandConfig a = c; a.ckpt_path = tg.add(wp3_tmp("t6_gen")); a.ckpt_every_s = 0; a.stop_after_step = 4;
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
  TmpGuard tg;
  Fixture F(100, 300, 24);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  for (int arith = 0; arith < 2; ++arith) {
    IslandRun r = arith ? run_island<Arith::ClassA>(F.D, F.st, F.nb, c) : run_island<Arith::Bit>(F.D, F.st, F.nb, c);
    CHECK(r.status == 0 && (int)r.terminal.size() == c.N);
    std::string path = tg.add(wp3_tmp("island_rt.bin"));
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
    // PR45 review MINOR-4: the verifying reader checks every top-store hash against its model (Zobrist keys of meta.p)
    // and every label against [0, p): a wrong hash or an out-of-range label is invalid_input; verify = false skips it.
    if (arith == 0 && !r.top_v.empty() && r.top_len[0] > 0) {
      auto status_of = [&](const std::string& pth, bool verify) {
        try { read_island_file(pth, verify); } catch (const v4::Error& e) { return e.st; }
        return v4::Status::completed;
      };
      IslandRun bh = r; bh.top_hash[0] ^= 1;
      std::string ph = tg.add(wp3_tmp("island_rt_badhash.bin")); write_island_file(ph, bh, Arith::Bit, inputs);
      CHECK(status_of(ph, true) == v4::Status::invalid_input);
      CHECK(status_of(ph, false) == v4::Status::completed);
      IslandRun bl = r; bl.top_pool[bl.top_off[0] + bl.top_len[0] - 1] = r.p;   // still sorted; label p is out of range
      std::string pl = tg.add(wp3_tmp("island_rt_badlabel.bin")); write_island_file(pl, bl, Arith::Bit, inputs);
      CHECK(status_of(pl, true) == v4::Status::invalid_input);
      std::remove(ph.c_str()); std::remove(pl.c_str());
    }
  }
  // interrupted run (stop after a checkpoint): no logZ / rb / pip / terminal sections
  IslandConfig a = c; a.ckpt_path = tg.add(wp3_tmp("island_rt_ck")); a.ckpt_every_s = 1e9; a.stop_after_step = 2;
  std::remove((a.ckpt_path + ".a").c_str()); std::remove((a.ckpt_path + ".b").c_str());
  IslandRun ri = run_island<Arith::Bit>(F.D, F.st, F.nb, a);
  std::string path = tg.add(wp3_tmp("island_rt_int.bin"));
  bool refused = false; try { write_island_file(path, ri, Arith::Bit, v4::Json::object()); } catch (const v4::Error&) { refused = true; }
  CHECK(refused);   // an interrupted island is a test outcome, never a file (review m3)
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
  TmpGuard tg; const std::string base = tg.add(wp3_tmp("t6k"));
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
  { FILE* lf = std::fopen((base + ".b.tmp.12345").c_str(), "rb"); CHECK(lf == nullptr); if (lf) std::fclose(lf); }   // m4b: leftover removed
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

// Parallel compaction (pass/step boundaries) = serial compaction, for every thread count and every flush order:
// offers cut into buffers that are flushed in permuted orders, several compaction cycles (deferred mode), value ties,
// and models offered with two values (largest kept). Compared entry by entry with the serial store and, where every
// model has one value, with WP1's reference v4::Store.
TEST(store_parallel_compaction_any_flush_order) {
  std::mt19937_64 g(41);
  std::vector<uint64_t> key(500); uint64_t x = 3; for (auto& k : key) k = splitmix64(x);
  struct Off { double v; Model S; };
  std::vector<Off> offers;
  std::map<Model, double> one;   // the single value per model (for the WP1 comparison)
  for (int i = 0; i < 120000; ++i) {
    Model S = random_support(g, 500, 1 + (int)(g() % 4));
    if (!one.count(S)) one[S] = -std::floor((double)(g() % 20000) / 3.0);
    offers.push_back({one[S], S});
  }
  for (bool two_values : {false, true}) {
    std::vector<Off> of = offers;
    if (two_values) for (size_t i = 0; i < of.size(); i += 13) of[i].v += 1e-12;   // class-A-like second value
    for (uint64_t cap : {1000ull, 25000ull}) {
      // serial reference
      TopStore ref; ref.init(cap, Order::HPM); ref.buf_limit = 1 << 30; ref.stage_limit = 1 << 30; ref.dup_filter = false;
      { StoreBuffer b; for (auto& o : of) ref.offer(b, o.v, o.S.data(), (uint32_t)o.S.size(), D_hash(key, o.S)); ref.flush(b); ref.compact(); }
      bool all_ok = ref.check_invariant();
      if (!two_values) {
        v4::Store w(cap, Order::HPM); for (auto& o : of) w.offer(o.v, o.S, D_hash(key, o.S)); w.compact();
        bool ok = w.size() == ref.size();
        for (size_t i = 0; ok && i < w.size(); ++i) ok = same_bits(w.v[i], ref.value(i)) && Model(w.model(i).begin(), w.model(i).end()) == ref.model(i);
        CHECKF(ok, "serial store vs WP1 Store, cap %llu", (unsigned long long)cap);
      }
      for (int threads : {1, 2, 3, 4}) for (int perm = 0; perm < 3; ++perm) {
        TopStore st; st.init(cap, Order::HPM); st.defer = true; st.buf_limit = 1 << 30; st.stage_hard = 1 << 30; st.dup_filter = (perm != 1);
        // cut into 40 buffers, flush them in a permuted order, compact (parallel) after every 7 flushes
        std::vector<StoreBuffer> bufs(40);
        for (size_t i = 0; i < of.size(); ++i) { auto& o = of[i]; bufs[i % 40].push(o.v, o.S.data(), (uint32_t)o.S.size(), D_hash(key, o.S)); }
        std::vector<int> order(40); for (int i = 0; i < 40; ++i) order[i] = i;
        std::mt19937_64 gp(100 + perm); std::shuffle(order.begin(), order.end(), gp);
        int nflush = 0;
        for (int b : order) { st.flush(bufs[b]); if (++nflush % 7 == 0) st.compact_parallel(threads); }
        st.compact_parallel(threads);
        bool ok = st.check_invariant() && st.size() == ref.size();
        for (size_t i = 0; ok && i < ref.size(); ++i) ok = same_bits(st.value(i), ref.value(i)) && st.model(i) == ref.model(i);
        // the index finds every kept model
        for (size_t i = 0; ok && i < st.size(); ++i) ok = st.k->find(st.k->ref(i)) == (int64_t)i;
        CHECKF(ok, "two_values %d cap %llu threads %d perm %d: size %zu vs %zu", (int)two_values, (unsigned long long)cap, threads, perm, st.size(), ref.size());
        all_ok = all_ok && ok;
      }
      CHECK(all_ok);
    }
  }
}

// --mem-budget admission (manager Q3/Q4): deterministic refusal before any allocation with a named reason; G = 0
// chooses the largest G <= 256 that fits, and the output does not depend on it.
static MemSizes sizes_of(const Fixture& F, const IslandConfig& c, int G) {
  MemSizes z; z.n = F.D.n; z.p = F.D.p; z.K = F.D.K; z.N = c.N; z.B = c.B; z.Hm = c.Hm; z.threads = c.threads; z.G = G; z.tile = 128;
  z.cap = c.store_cap ? c.store_cap : 40ULL * F.D.p + 1; z.label_major = c.kernel == KernelKind::LabelMajor;
  z.deferred = c.store_parallel_compact && c.threads > 1 && z.label_major; z.leaders = c.leaders; z.compat = c.compat; z.inputs_bytes = c.inputs_bytes;
  return z;
}
TEST(mem_budget_admission) {
  Fixture F(100, 300, 26);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3;
  const uint64_t h0 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c).hash();
  auto plan = [&](int G) { IslandConfig cg = c; cg.G = G; return plan_island(F.D, F.st, cg).total; };
  // (1) refusal before any allocation: budget below the G = 1 plan; deterministic reason
  IslandConfig a = c; a.G = 0; a.mem_budget = plan(1) - 1;
  IslandRun r1 = run_island<Arith::ClassA>(F.D, F.st, F.nb, a);
  CHECKF(r1.status == 3 && r1.reason.rfind("mem_budget:", 0) == 0 && r1.top_v.empty(), "refusal: status %d reason %s", r1.status, r1.reason.c_str());
  CHECK(run_island<Arith::ClassA>(F.D, F.st, F.nb, a).reason == r1.reason);
  // (2) G chosen by the budget: between plan(17) and plan(18) -> G = 17; same output as any G (T3)
  a.mem_budget = (plan(17) + plan(18)) / 2;
  IslandRun r2 = run_island<Arith::ClassA>(F.D, F.st, F.nb, a);
  CHECKF(r2.status == 0 && r2.G_used == 17 && r2.hash() == h0, "auto G: status %d G %d", r2.status, r2.G_used);
  // (3) a fixed G whose plan exceeds the budget is refused
  IslandConfig b = c; b.G = 48; b.mem_budget = plan(17);
  CHECK(run_island<Arith::ClassA>(F.D, F.st, F.nb, b).status == 3);
  // (4) step-boundary refusal (review PR24 m1): the admission's k (forced to 0.5) is far below the stored models' real
  //     size, so the admission passes and the first step-boundary check (actual pool) refuses; no store is reported
  IslandConfig d = c; d.test_admission_k = 0.5;
  d.mem_budget = plan_island(F.D, F.st, d).total + 1024;
  IslandRun r4 = run_island<Arith::ClassA>(F.D, F.st, F.nb, d);
  CHECKF(r4.status == 3 && r4.reason.find("after step") != std::string::npos && r4.top_v.empty() && r4.rb_acc.empty(), "step refusal: status %d '%s'", r4.status, r4.reason.c_str());
  TmpGuard tg; std::string path = tg.add(wp3_tmp("refused.bin"));
  write_island_file(path, r4, Arith::ClassA, v4::Json::object());
  { v4::fmt::Reader rd(path); uint64_t n = 0; rd.get<double>("top_v", &n);
    CHECK(rd.json("meta").at("status").str() == "resource_limit" && n == 0 && !rd.has("logZ") && !rd.has("terminal_S")); }
  std::remove(path.c_str());
  // (5) the plan grows with G, threads, k and leaders
  MemSizes z = sizes_of(F, c, 64); CHECK(island_memory(z, 8).total > island_memory(sizes_of(F, c, 1), 8).total);
  MemSizes zl = z; zl.leaders = true; CHECK(island_memory(zl, 8).total > island_memory(z, 8).total);
  MemSizes big; big.n = 200; big.p = 1000000; big.K = 100; big.N = 2500; big.B = 14; big.threads = 96; big.G = 64; big.cap = 40000001ULL;
  std::printf("  1M plan (G 64, 96 threads, k 7): %s\n", mem_plan_text(island_memory(big, 7)).c_str());
}

// out of memory inside a parallel region (review #21 re-check n1): status resource_limit, never an abort
TEST(oom_in_region_is_resource_limit) {
  Fixture F(100, 300, 34);
  for (int kern = 0; kern < 2; ++kern) for (int th : {1, 3}) {
    IslandConfig c = small_cfg(); c.kernel = kern ? KernelKind::LabelMajor : KernelKind::ParticleMajor; c.threads = th; c.G = 16; c.test_oom_pass = 2;
    IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
    CHECKF(r.status == 3 && r.reason.find("out of memory") != std::string::npos && r.top_v.empty(), "threads %d: status %d '%s'", th, r.status, r.reason.c_str());
  }
}

// out of memory in the parallel compaction (review PR26 r2): the sort scratch is allocated outside every parallel
// region (psort_noalloc), so the failure is a catchable std::bad_alloc -> resource_limit, never an abort
TEST(oom_in_parallel_compaction_is_resource_limit) {
  Fixture F(100, 300, 34);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16; c.test_oom_merge = 1;
  IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
  CHECKF(r.status == 3 && r.reason.find("out of memory") != std::string::npos && r.top_v.empty(), "status %d '%s' (merges %llu)", r.status, r.reason.c_str(),
         (unsigned long long)r.ks.store_merges);
  // psort_noalloc = std::sort for every thread count (chunks + pairwise merges)
  // (review m3: every merge round is cut into merge-path segments; uneven chunk and segment counts included)
  std::mt19937_64 g(7);
  for (size_t n : {(size_t)4100, (size_t)20011}) {
    std::vector<uint64_t> a(n); for (auto& x : a) x = g() % 5000;
    std::vector<uint64_t> ref = a; std::sort(ref.begin(), ref.end());
    for (int th : {1, 2, 3, 4, 5, 7, 8}) { std::vector<uint64_t> b = a, tmp; psort_noalloc(b, tmp, std::less<uint64_t>(), th); CHECKF(b == ref, "n %zu threads %d", n, th); }
  }
}

// leader stores (review PR24 P1): label-major = particle-major (= core through the compat golden), both arithmetic forms
TEST(leaders_label_major_equal_particle_major) {
  Fixture F(100, 300, 35);
  for (int arith = 0; arith < 2; ++arith) {
    IslandConfig c = small_cfg(); c.leaders = true; c.kernel = KernelKind::ParticleMajor; c.threads = 1;
    IslandRun r0 = arith ? run_island<Arith::ClassA>(F.D, F.st, F.nb, c) : run_island<Arith::Bit>(F.D, F.st, F.nb, c);
    c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
    IslandRun r1 = arith ? run_island<Arith::ClassA>(F.D, F.st, F.nb, c) : run_island<Arith::Bit>(F.D, F.st, F.nb, c);
    bool ok = r0.leaders && r1.leaders && !r0.lead0_v.empty() && r0.lead0_v.size() == r1.lead0_v.size() && r0.lead1_v.size() == r1.lead1_v.size() &&
              r0.lead0_pool == r1.lead0_pool && r0.lead1_pool == r1.lead1_pool && r0.hash() == r1.hash();
    for (size_t i = 0; ok && i < r0.lead0_v.size(); ++i) ok = same_bits(r0.lead0_v[i], r1.lead0_v[i]);
    for (size_t i = 0; ok && i < r0.lead1_v.size(); ++i) ok = same_bits(r0.lead1_v[i], r1.lead1_v[i]);
    CHECKF(ok, "arith %d: leaders PM %zu/%zu vs LM %zu/%zu", arith, r0.lead0_v.size(), r0.lead1_v.size(), r1.lead0_v.size(), r1.lead1_v.size());
    std::printf("  [%s] lead0 %zu, lead1 %zu entries: label-major = particle-major\n", arith ? "A" : "bit", r1.lead0_v.size(), r1.lead1_v.size());
  }
}

// Compat (serial v3 stream): checkpoint/resume restores the xoshiro state and the double RB accumulator (identical
// bytes); island_r.bin is mode compat with NO leader stores (INTERFACES v0.1.7); production configurations
// that cannot be serial are refused.
TEST(compat_restart_file_and_refusals) {
  Fixture F(100, 300, 27);
  IslandConfig c = small_cfg(); c.compat = true; c.kernel = KernelKind::ParticleMajor; c.threads = 1; c.island = 2;
  IslandRun r0 = run_island<Arith::Bit>(F.D, F.st, F.nb, c);
  CHECK(r0.status == 0 && r0.compat && r0.stream_count > 0 && !r0.leaders && r0.lead0_v.empty() && r0.lead1_v.empty());   // v0.1.7
  TmpGuard tg; const std::string base = tg.add(wp3_tmp("compat_ck"));
  for (int stop : {0, 3, 6}) {
    std::remove((base + ".a").c_str()); std::remove((base + ".b").c_str());
    IslandConfig a = c; a.ckpt_path = base; a.ckpt_every_s = 1e9; a.stop_after_step = stop;
    CHECK(run_island<Arith::Bit>(F.D, F.st, F.nb, a).status == 1);
    IslandConfig b = a; b.stop_after_step = -1;
    IslandRun r = run_island<Arith::Bit>(F.D, F.st, F.nb, b);
    CHECKF(r.status == 0 && r.resumed_from_step == stop && r.hash() == r0.hash() && r.stream_count == r0.stream_count, "compat resume after %d", stop);
  }
  std::remove((base + ".a").c_str()); std::remove((base + ".b").c_str());
  std::string path = tg.add(wp3_tmp("compat_island.bin"));
  write_island_file(path, r0, Arith::Bit, v4::Json::object());
  { v4::fmt::Reader rd(path); CHECK(rd.mode() == v4::fmt::M_COMPAT && !rd.has("lead0_v") && !rd.has("lead1_v") && rd.json("meta").at("mode").str() == "compat"); }
  // even an island run with the test-only leaders option writes no leader store (v0.1.7)
  { IslandConfig cl = c; cl.leaders = true; IslandRun rl = run_island<Arith::Bit>(F.D, F.st, F.nb, cl);
    CHECK(rl.leaders && !rl.lead0_v.empty());
    write_island_file(path, rl, Arith::Bit, v4::Json::object());
    v4::fmt::Reader rd(path); CHECK(!rd.has("lead0_v") && !rd.has("lead1_v")); }
  std::remove(path.c_str());
  for (int bad = 0; bad < 3; ++bad) {
    IslandConfig x = c; if (bad == 0) x.threads = 2; if (bad == 1) { x.kernel = KernelKind::LabelMajor; x.allow_test_kernels = true; } if (bad == 2) x.island = 5;
    bool refused = false; try { run_island<Arith::Bit>(F.D, F.st, F.nb, x); } catch (const std::exception&) { refused = true; }
    CHECKF(refused, "compat refusal case %d", bad);
  }
  bool refusedA = false; try { run_island<Arith::ClassA>(F.D, F.st, F.nb, c); } catch (const std::exception&) { refusedA = true; }
  CHECK(refusedA);
}

// M1 (review PR21): a numerical failure inside the kernels returns status numerical_failure (no abort), deterministically:
// the same reason for the particle-major and the label-major kernel at 1 and 3 threads; no estimate and no store in the
// result or the island file. Columns scaled by 1e200 make Cholesky, refactor and QR fail for every model containing them.
TEST(numerical_failure_status_deterministic) {
  Fixture F(100, 300, 28);
  auto own = std::make_shared<v4::DataOwned>();
  own->X.assign(F.D.Xs, F.D.Xs + (size_t)F.D.n * F.D.p); own->y.assign(F.D.ys, F.D.ys + F.D.n);
  for (int j : {37, 151, 222}) for (int i = 0; i < F.D.n; ++i) own->X[(size_t)j * F.D.n + i] *= 1e200;
  v4::Data D2 = v4::make_data(own, F.D.n, F.D.p);
  for (int arith = 0; arith < 2; ++arith) {
    std::string reason0;
    for (int kern = 0; kern < 2; ++kern) for (int th : {1, 3}) {
      IslandConfig c = small_cfg(); c.kernel = kern ? KernelKind::LabelMajor : KernelKind::ParticleMajor; c.threads = th; c.G = 16;
      IslandRun r = arith ? run_island<Arith::ClassA>(D2, F.st, F.nb, c) : run_island<Arith::Bit>(D2, F.st, F.nb, c);
      bool ok = r.status == 2 && r.reason.find("numerical_failure") != std::string::npos && r.top_v.empty() && r.rb_acc.empty() && r.pip.empty();
      if (reason0.empty()) { reason0 = r.reason; std::printf("  [%s] %s\n", arith ? "A" : "bit", r.reason.c_str()); }
      CHECKF(ok && r.reason == reason0, "arith %d kernel %d threads %d: status %d reason '%s' vs '%s'", arith, kern, th, r.status, r.reason.c_str(), reason0.c_str());
      if (kern == 1 && th == 3) {
        TmpGuard tg; std::string path = tg.add(wp3_tmp("nf.bin"));
        write_island_file(path, r, arith ? Arith::ClassA : Arith::Bit, v4::Json::object());
        v4::fmt::Reader rd(path);
        CHECK(rd.json("meta").at("status").str() == "numerical_failure" && !rd.has("logZ") && !rd.has("rb_acc") && !rd.has("pip_r") &&
              !rd.has("terminal_S") && !rd.has("st_cum") && rd.has("st_phi"));
        std::remove(path.c_str());
      }
    }
  }
}

// M1, kernel path: pi_0 never draws the scaled columns (their table entries set to -inf), so the failure is a consumed
// Gibbs flip (label-major: phase-A flag, walk; particle-major: eval1 flag) -- same reason for every kernel and thread count.
TEST(numerical_failure_in_flip_deterministic) {
  Fixture F(100, 300, 32);
  const std::vector<int> bad = {37, 151, 222};
  auto own = std::make_shared<v4::DataOwned>();
  own->X.assign(F.D.Xs, F.D.Xs + (size_t)F.D.n * F.D.p); own->y.assign(F.D.ys, F.D.ys + F.D.n);
  for (int j : bad) for (int i = 0; i < F.D.n; ++i) own->X[(size_t)j * F.D.n + i] *= 1e200;
  v4::Data D2 = v4::make_data(own, F.D.n, F.D.p);
  Start st2 = F.st;
  for (int j : bad) { int b = st2.blk[j]; for (size_t code = 0; code < st2.logr[b].size(); ++code) if (code & (1u << st2.pos[j])) st2.logr[b][code] = NEG_INF; }
  build_sampler(st2, F.D);
  for (int arith = 0; arith < 2; ++arith) {
    std::string reason0;
    for (int kern = 0; kern < 2; ++kern) for (int th : {1, 3}) {
      IslandConfig c = small_cfg(); c.kernel = kern ? KernelKind::LabelMajor : KernelKind::ParticleMajor; c.threads = th; c.G = 16;
      IslandRun r = arith ? run_island<Arith::ClassA>(D2, st2, F.nb, c) : run_island<Arith::Bit>(D2, st2, F.nb, c);
      if (reason0.empty()) { reason0 = r.reason; std::printf("  [%s] %s\n", arith ? "A" : "bit", r.reason.c_str()); }
      CHECKF(r.status == 2 && r.reason == reason0 && r.reason.find("Gibbs label") != std::string::npos && r.top_v.empty(),
             "arith %d kernel %d threads %d: status %d reason '%s' vs '%s'", arith, kern, th, r.status, r.reason.c_str(), reason0.c_str());
    }
  }
}

// M2 (review PR21): kept runs held by worker snapshots are released at step boundaries and on flush: after an island
// none is alive, and at most a few were alive at once (current + new during a compaction + snapshots in a tile).
TEST(store_snapshots_released) {
  Fixture F(100, 300, 29);
  kept_live_max().store(kept_live().load());
  const int before = kept_live().load();
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16; c.store_cap = 2000;   // many compactions
  IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
  CHECK(r.status == 0);
  std::printf("  kept runs alive: before %d, max during the island %d, after %d (merges %llu)\n", before, r.ks.kept_live_max, kept_live().load(),
              (unsigned long long)r.ks.store_merges);
  CHECK(kept_live().load() == before);
  CHECK(r.ks.kept_live_max - before <= 3);   // current + new during a compaction + one stale snapshot mid-tile
}

// m6a: flips at supports k > 24 (the uncapped vector path), k = 25, 40, 99 at K = 100: bit form = scorer bits (both entry
// points), class A <= 1e-9 relative.
TEST(flip_large_supports) {
  Fixture F(200, 400, 30);
  BitScorer sc(&F.D);
  std::mt19937_64 g(8);
  long checked = 0, mism = 0; double worstA = 0;
  for (int k : {25, 40, 99}) {
    Model S = random_support(g, F.D.p, k);
    double lm = sc.score(S).logm, cc = F.st.comp(S);
    SupportCache s; build_support(F.D, F.st, sc, s, S, zobrist(F.D, S), lm, F.D.logprior[k] + cc, (lm - F.D.logm0) - cc, 1.0);
    CHECK(s.fast);
    for (int j = 0; j < F.D.p; ++j) {
      Model T = S; if (contains(S, j)) sorted_erase(T, j); else sorted_insert(T, j);
      double ref = sc.score(T).logm, l1, o1, la, oa;
      eval1<Arith::Bit>(F.D, F.st, sc, s, j, l1, o1);
      eval1<Arith::ClassA>(F.D, F.st, sc, s, j, la, oa);
      ++checked; if (!same_bits(ref, l1)) ++mism;
      if (!contains(S, j)) worstA = std::max(worstA, std::fabs(la - ref) / std::fabs(ref));
    }
  }
  std::printf("  k = 25/40/99: %ld flips, %ld bit mismatches, class A max relative %.2e\n", checked, mism, worstA);
  CHECK(mism == 0); CHECK(worstA <= 1e-9);
}

// m6c: the Gibbs cap |S| = K is reached (n = 12 -> K = 6): I4 by mechanism holds, PM = LM in both forms.
TEST(gibbs_cap_island) {
  Fixture F(12, 80, 31);
  for (int arith = 0; arith < 2; ++arith) {
    IslandConfig c = small_cfg(); c.kernel = KernelKind::ParticleMajor;
    IslandRun r0 = arith ? run_island<Arith::ClassA>(F.D, F.st, F.nb, c) : run_island<Arith::Bit>(F.D, F.st, F.nb, c);
    c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
    IslandRun r1 = arith ? run_island<Arith::ClassA>(F.D, F.st, F.nb, c) : run_island<Arith::Bit>(F.D, F.st, F.nb, c);
    uint64_t cap = 0; MoveStats mb; for (auto& s : r1.stages) { cap += s.moves.gibbs_cap; add_moves(mb, s.moves); }
    for (auto& s : r1.terminal_moves) cap += s.gibbs_cap;
    CHECKF(r0.status == 0 && r1.status == 0 && r0.hash() == r1.hash(), "arith %d: PM vs LM", arith);
    CHECKF(cap > 0, "arith %d: the cap was never reached", arith);
    CHECK(v4::i4_holds(mb, r1.logical[PH_FINAL_BRIDGE]));
    std::printf("  [%s] K = %d: %llu Gibbs steps at the cap\n", arith ? "A" : "bit", F.D.K, (unsigned long long)cap);
  }
}

// m5 (review PR24): compaction through offer() with the duplicate filter active and stale snapshots, serial in-pass
// fallbacks (small stage_hard) interleaved with parallel compactions between cycles: equals the serial reference
TEST(store_offer_path_fallbacks_and_parallel) {
  std::mt19937_64 g(43);
  std::vector<uint64_t> key(400); uint64_t x = 9; for (auto& k : key) k = splitmix64(x);
  std::vector<std::pair<double, Model>> offers;
  std::map<Model, double> val;
  for (int i = 0; i < 90000; ++i) { Model S = random_support(g, 400, 1 + (int)(g() % 4)); if (!val.count(S)) val[S] = -std::floor((double)(g() % 9000) / 3.0); offers.push_back({val[S], S}); }
  for (uint64_t cap : {2000ull, 20000ull}) {
    v4::Store ref(cap, Order::HPM); for (auto& o : offers) ref.offer(o.first, o.second, D_hash(key, o.second)); ref.compact();
    TopStore st; st.init(cap, Order::HPM); st.defer = true; st.buf_limit = 97; st.stage_hard = 3000; st.stage_limit = 1500;
    std::vector<StoreBuffer> bufs(3);
    for (int cycle = 0; cycle < 3; ++cycle) {
      #pragma omp parallel for num_threads(3) schedule(dynamic, 64)
      for (size_t i = cycle; i < offers.size(); i += 3) {
        auto& o = offers[(i * 7919) % offers.size()];
        st.offer(bufs[omp_get_thread_num()], o.first, o.second.data(), (uint32_t)o.second.size(), D_hash(key, o.second));
      }
      for (auto& b : bufs) st.flush(b);
      for (auto& b : bufs) { b.snap.reset(); b.snap_gen = ~0ull; }
      st.compact_parallel(3);
    }
    bool ok = st.check_invariant() && st.size() == ref.size();
    for (size_t i = 0; ok && i < ref.size(); ++i) ok = same_bits(st.value(i), ref.v[i]) && st.model(i) == Model(ref.model(i).begin(), ref.model(i).end());
    uint64_t dropped = 0; for (auto& b : bufs) dropped += b.n_dup_dropped;
    CHECKF(ok, "cap %llu: size %zu vs %zu", (unsigned long long)cap, st.size(), ref.size());
    std::printf("  cap %llu: %llu serial fallbacks, %llu compactions, %llu duplicate offers dropped, content = reference: %d\n", (unsigned long long)cap,
                (unsigned long long)st.n_serial_merges, (unsigned long long)st.n_merges, (unsigned long long)dropped, (int)ok);
  }
}

// P2 (review PR24): the plan is an upper bound of the island's memory. VmHWM is reset after the data are built
// (/proc/self/clear_refs 5); the island's increment must not exceed the plan (without the inputs term, already
// resident) evaluated at the stored models' true mean size. Quick case p = 2e4 here; p = 1e5 under --full.
static long status_kb(const char* key) {
  FILE* f = std::fopen("/proc/self/status", "r"); if (!f) return -1;
  char line[256]; long kb = -1; size_t n = std::strlen(key);
  while (std::fgets(line, sizeof line, f)) if (std::strncmp(line, key, n) == 0) { kb = std::atol(line + n); break; }
  std::fclose(f); return kb;
}
static void plan_bounds_peak(int p, int N, std::initializer_list<int> Gs) {
  Fixture F(200, p, 36);
  // rows: label-major for each G (leaders off / on); particle-major, 3 threads (re-check m1; leaders off / on); a
  // calibration diagnostic island, label-major (leaders and the round-start snapshot)
  std::vector<std::tuple<int, int, bool, bool>> rows;   // kernel (0 PM, 1 LM), G, leaders, calibration
  for (int G : Gs) for (bool lead : {false, true}) rows.emplace_back(1, G, lead, false);
  for (bool lead : {false, true}) rows.emplace_back(0, 1, lead, false);
  rows.emplace_back(1, *Gs.begin(), true, true);
  for (auto [kern, G, lead, cal] : rows) {
    IslandConfig c = small_cfg(); c.N = kern || !lead ? N : N / 2;   // PM with leaders: N / 2 (time)
    c.kernel = kern ? KernelKind::LabelMajor : KernelKind::ParticleMajor; c.threads = 3; c.G = G; c.leaders = lead;
    c.grid = {0.0, 0.3, 0.7, 1.0}; c.L = 0; c.Hm = 1; c.k_store = 8.0;   // as calib.bin would give (r1)
    if (cal) { c.role = IslandRole::Diag; c.island = 1; c.iter = 1; }
    { FILE* cr = std::fopen("/proc/self/clear_refs", "w"); if (cr) { std::fputs("5", cr); std::fclose(cr); } }
    const long rss0 = status_kb("VmRSS:");
    IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
    const long hwm = status_kb("VmHWM:");
    double k = r.top_v.empty() ? 8.0 : (double)r.top_pool.size() / (double)r.top_v.size();
    if (lead && !r.lead0_v.empty()) k = std::max({k, (double)r.lead0_pool.size() / r.lead0_v.size(), (double)r.lead1_pool.size() / r.lead1_v.size()});
    double k_plan = 0; MemPlan mp = plan_island(F.D, F.st, c, nullptr, &k_plan, nullptr);   // the admission's own plan
    uint64_t inputs = 0; for (auto& it : mp.items) if (it.name == "inputs") inputs = it.bytes;
    const double plan_mb = (double)(mp.total - inputs) / 1048576.0, meas_mb = (double)(hwm - rss0) / 1024.0;
    std::printf("  (stored mean |S| at the end %.2f; the plan's k %.2f)\n", k, k_plan);
    std::printf("  p %d N %d %s G %3d leaders %d%s: island peak increment %.0f MiB, plan %.0f MiB (k %.2f) -> %s\n", p, c.N, kern ? "LM" : "PM", G, (int)lead,
                cal ? " calibration" : "", meas_mb, plan_mb, k, plan_mb >= 1.10 * meas_mb ? "bound + 10 % holds" : "BOUND (+10 %) FAILS");
    // the plan is an upper bound with headroom (manager 11-16): >= 10 % over the measured peak in every row
    CHECKF(r.status == 0 && rss0 > 0 && hwm > 0 && plan_mb >= 1.10 * meas_mb, "p %d %s G %d leaders %d cal %d: measured %.0f MiB, plan %.0f MiB < 1.10 x measured", p,
           kern ? "LM" : "PM", G, (int)lead, (int)cal, meas_mb, plan_mb);
  }
}
TEST(mem_plan_bounds_measured_peak_2e4) { plan_bounds_peak(20000, 500, {64, 256}); }
TEST_TAGGED(mem_plan_bounds_measured_peak_1e5, "full") { plan_bounds_peak(100000, 500, {64, 256}); }

// review PR24 r1 / PR26 B1: at p >= 1e5 an island without the calibration-measured k_store is invalid_input (no real
// run plans from the pi_0 fallback); with k_store (or the test/bench override) it is admitted
TEST(k_store_required_at_1e5) {
  Fixture F(20, 100000, 37);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::ParticleMajor; c.threads = 1; c.N = 4; c.grid = {0.0, 1.0}; c.L = 0; c.Hm = 1;
  c.mem_budget = 1ull << 40;   // the requirement is the admission's (final island with a budget; re-check m2)
  bool refused = false;
  try { (void)run_island<Arith::ClassA>(F.D, F.st, F.nb, c); } catch (const v4::Error& e) { refused = e.st == v4::Status::invalid_input && std::string(e.what()).find("k_store") != std::string::npos; }
  CHECKF(refused, "p 1e5 without k_store was not refused");
  c.k_store = 8.0; IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c); CHECKF(r.status == 0, "with k_store: status %d", r.status);
  c.k_store = 0; c.k_store_optional = true; IslandRun r2 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c); CHECKF(r2.status == 0 && r2.hash() == r.hash(), "override");
  // re-check m2: without a budget there is no admission, and calibration islands plan from the setup (no calib.bin)
  c.k_store_optional = false; c.mem_budget = 0; IslandRun r3 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c); CHECKF(r3.status == 0, "no budget: status %d", r3.status);
  c.mem_budget = 1ull << 40; c.role = IslandRole::Pilot; c.island = 0; c.adaptive = true; c.adaptive_H = c.N; c.adaptive_Te = 4; c.grid.clear();
  IslandRun r4 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c); CHECKF(r4.status == 0, "pilot at 1e5 without k_store: status %d '%s'", r4.status, r4.reason.c_str());
}

// L5: the vectorised pi_0 draw = the original draw (same uniforms per slot, same model), and philox8_word over slots
// = uniform_at; checked for many particles, two partitions, and sizes up to K (n = 60 -> K = 30).
TEST(pi0_fast_draw_equals_draw) {
  for (int bsz : {4, 7}) {
    Data D; make_ar_data(D, 60, 3000, 0.6, 51);
    Start st; build_start(st, D, contiguous_blocks(3000, bsz));
    long same = 0, total = 0; size_t maxk = 0;
    for (uint32_t i = 1; i <= 3000; ++i) {
      Address a0; a0.seed = 5; a0.island = 2; a0.xph = X_BRIDGE; a0.stage = 3; a0.particle = i; a0.position = 77;
      auto nu = [&](uint32_t slot) { Address a = a0; a.slot = slot; return uniform_at(a); };
      const v4::Ctr4 ctr = v4::address_ctr(a0); const v4::Key2 kk = v4::address_key(a0);
      Model S1, S2;
      draw_pi0(st, nu, S1);
      draw_pi0_fast(st, nu, [&](const uint32_t* sl, double* out) { philox8_word(ctr.data(), kk.data(), 0, sl, out); }, S2);
      ++total; if (S1 == S2) ++same; maxk = std::max(maxk, S1.size());
    }
    std::printf("  blocks of %d: %ld / %ld draws identical (largest |S| %zu)\n", bsz, same, total, maxk);
    CHECK(same == total);
  }
}

// calibration admission (WP4's N-1 rule, IslandSpec): mem_budget = the whole task's budget, resident_bytes = the
// calibration's own state without the inputs; admitted iff resident_bytes + the island's plan <= mem_budget (to the byte)
#include "v4/island/calib_runner.h"
TEST(calibration_admission_n1_rule) {
  Fixture F(100, 300, 38);
  // a fixed G on both sides (G = 0 lets the admission shrink G until the plan fits)
  CalibRunnerConfig rc; rc.seed = 3; rc.kernel = KernelKind::ParticleMajor; rc.threads = 1; rc.B = 14; rc.G = 1;
  CalibIslandRunner<Arith::Bit> run(F.D, F.st, F.nb, rc);
  v4::calib::IslandSpec sp; sp.role = v4::calib::IslandRole::Diag; sp.tier = 0; sp.iter = 1; sp.island = 1; sp.H = 30;
  sp.grid = {0.0, 0.3, 1.0}; sp.L = 1; sp.Hm = 1; sp.resident_bytes = 123456789;
  IslandConfig c; c.role = IslandRole::Diag; c.island = 1; c.iter = 1; c.N = sp.H; c.grid = sp.grid; c.L = 1; c.Hm = 1; c.B = 14;
  c.kernel = KernelKind::ParticleMajor; c.threads = 1; c.G = 1; c.leaders = true; c.inputs_bytes = (double)sp.resident_bytes;
  const uint64_t plan = plan_island(F.D, F.st, c).total;   // includes the resident bytes through the inputs term
  sp.mem_budget = plan - 1;
  v4::calib::IslandOut o1 = run.run(sp);
  CHECKF(o1.status == v4::Status::resource_limit && !o1.partial, "budget = plan - 1: status %s partial %d", v4::status_name(o1.status), (int)o1.partial);
  sp.mem_budget = plan;
  v4::calib::IslandOut o2 = run.run(sp);
  CHECKF(o2.status == v4::Status::completed, "budget = plan: status %s '%s'", v4::status_name(o2.status), o2.message.c_str());
  sp.resident_bytes = 0; sp.mem_budget = plan - 123456789;   // the same island without the resident state fits exactly
  v4::calib::IslandOut o3 = run.run(sp);
  CHECKF(o3.status == v4::Status::completed, "no resident, budget = plan - resident: status %s", v4::status_name(o3.status));
  std::printf("  plan with resident %llu B: refused at budget plan - 1, admitted at plan\n", (unsigned long long)plan);
}

// review PR39 m1: a step-boundary refusal through CalibIslandRunner (the admission's k forced below the real model size:
// admitted, then refused at the first step boundary): resource_limit with partial = true, the schedule / stages so far
// and the ledger so far (WP3_DESIGN §1.11), never an estimate of a completed island
TEST(calibration_runner_step_boundary_partial) {
  Fixture F(100, 300, 38);
  CalibRunnerConfig rc; rc.seed = 3; rc.kernel = KernelKind::ParticleMajor; rc.threads = 1; rc.B = 14; rc.G = 1; rc.test_admission_k = 0.5;
  CalibIslandRunner<Arith::Bit> run(F.D, F.st, F.nb, rc);
  v4::calib::IslandSpec sp; sp.role = v4::calib::IslandRole::Diag; sp.tier = 0; sp.iter = 1; sp.island = 1; sp.H = 30;
  sp.grid = {0.0, 0.3, 0.6, 1.0}; sp.L = 1; sp.Hm = 1; sp.resident_bytes = 1000000;
  IslandConfig c; c.role = IslandRole::Diag; c.island = 1; c.iter = 1; c.N = sp.H; c.grid = sp.grid; c.L = 1; c.Hm = 1; c.B = 14;
  c.kernel = KernelKind::ParticleMajor; c.threads = 1; c.G = 1; c.leaders = true; c.inputs_bytes = (double)sp.resident_bytes; c.test_admission_k = 0.5;
  sp.mem_budget = plan_island(F.D, F.st, c).total + 1024;
  v4::calib::IslandOut o = run.run(sp);
  CHECKF(o.status == v4::Status::resource_limit && o.partial && o.message.find("after step") != std::string::npos,
         "step boundary: status %s partial %d '%s'", v4::status_name(o.status), (int)o.partial, o.message.c_str());
  CHECKF(!o.stages.empty() && o.schedule.size() == o.stages.size() && o.led.top.size() > 0 && o.led.logical[v4::PH_DIAG][ME_INIT] == (uint64_t)sp.H,
         "ledger so far: %zu stages, %zu schedule points, %zu stored, INIT events %llu", o.stages.size(), o.schedule.size(), o.led.top.size(),
         (unsigned long long)o.led.logical[v4::PH_DIAG][ME_INIT]);
  std::printf("  refused %s; %zu stage(s) and %zu stored models so far\n", o.message.substr(0, o.message.find(" [")).c_str(), o.stages.size(), o.led.top.size());
}

// `smcbvs4 calibrate` end to end (WP4's calib::run with WP3's island runner plugged in; WP3_DESIGN §1.11): data.bin from
// prep, a setup.bin with the partition, block tables, table stores and neighbour lists (WP4's write_setup_min sections
// + nb_ptr / nb_idx), then the command in each mode. compat runs the bit form particle-major on the v3 streams, law the
// bit form particle-major, V class A label-major. Checks: status ok, calib.bin readable (grid from 0 to 1, inherited
// models), the island's start law equals the setup's (load_start), V the same for 1 and 3 threads.
#include "v4/calib_run.h"
#include "v4/island/setup_load.h"
#include "v4/prep.h"
#include "v4/stubs.h"
#include "v4/wp4_io.h"
#include "v4/island/pilot_only.h"
// calibration inputs at small p (data.bin + setup.bin with the neighbour lists): shared by the calibrate end-to-end
// test and the pilot-only test (WP7 O5)
struct CalInputs { v4::Data D; std::string dpath, spath; int p = 0; };
static CalInputs make_cal_inputs(TmpGuard& tg, const std::string& tag) {
  const int n = 60, p_raw = 30;
  std::vector<double> X((size_t)n * p_raw), y(n);
  { std::mt19937_64 g(41); std::normal_distribution<double> nd;
    for (int i = 0; i < n; ++i) { double prev = 0; for (int j = 0; j < p_raw; ++j) { double x = 0.6 * prev + 0.8 * nd(g); X[(size_t)j * n + i] = x; prev = x; } }
    for (int i = 0; i < n; ++i) y[i] = 1.2 * X[(size_t)2 * n + i] - 0.9 * X[(size_t)11 * n + i] + nd(g); }
  v4::prep::Result pr = v4::prep::preprocess(X.data(), y.data(), n, p_raw);
  CHECK(pr.status == "ok");
  v4::Data D = v4::make_data(pr.own, n, pr.p);
  const int p = D.p;
  const std::string dpath = tg.add(wp3_tmp(tag + "_data.bin")), s0 = tg.add(wp3_tmp(tag + "_setup0.bin")), spath = tg.add(wp3_tmp(tag + "_setup.bin"));
  const std::string dhash = v4::prep::write_data(dpath, D, pr, "B", v4::Json::object());
  // setup: blocks of 3, the island's own tables (core's arithmetic), table stores over every table model
  Start st; build_start(st, D, contiguous_blocks(p, 3));
  Neighbours nb = window_neighbours(D, 6, 4);
  v4::wp4io::SetupView S; S.blk = st.blk; S.pos = st.pos; S.blk_ptr.push_back(0);
  S.ttop.init(40ull * p + 1, Order::HPM); S.tlead0.init(20ull * p, Order::LEX); S.tlead1.init(20ull * p, Order::LEX);
  BitScorer sc(&D);
  for (int b = 0; b < st.J; ++b) {
    for (int j : st.blocks[b]) S.blk_members.push_back(j);
    S.blk_ptr.push_back((int64_t)S.blk_members.size()); S.code_ptr.push_back((int64_t)S.logr.size());
    for (uint32_t c = 0; c < st.logr[b].size(); ++c) {
      S.logr.push_back(st.logr[b][c]);
      Model U; for (size_t i = 0; i < st.blocks[b].size(); ++i) if (c & (1u << i)) U.push_back(st.blocks[b][i]);
      if ((int)U.size() > D.K) continue;
      double F = D.logprior[U.size()] + sc.score(U).logm, lg0 = D.logprior[U.size()] + st.logr[b][c];
      S.ttop.offer(F, U, D.zob.hash(U)); S.tlead0.offer(lg0, U, D.zob.hash(U)); S.tlead1.offer(F, U, D.zob.hash(U));
    }
  }
  S.code_ptr.push_back((int64_t)S.logr.size());   // J + 1 entries; code_ptr[J] = |logr| (INTERFACES v0.1.19 §2/§5)
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  S.mode_S = Model(S.ttop.model(0).begin(), S.ttop.model(0).end());
  v4::Json sin = v4::Json::object(); sin["data.bin"] = dhash;
  v4::wp4io::write_setup_min(s0, S, sin);
  { v4::fmt::Reader R(s0); v4::fmt::Writer W(v4::fmt::K_SETUP, v4::fmt::M_COMPAT);   // + the neighbour lists (WP2's sections)
    for (const auto& e : R.sections()) {
      const std::string nm(e.name);
      if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
      const void* q = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                    : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                    : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                    : (const void*)R.get<uint8_t>(nm);
      W.add_copy(nm, e.dtype, q, e.length, e.dims[0], e.dims[1]);
    }
    W.add("nb_ptr", nb.ptr); W.add("nb_idx", nb.idx); W.add("size_cum", st.size_cum); W.add("size_logmass", st.size_logmass); W.write(spath); }
  { Start st2 = load_start(spath, D); Neighbours nb2 = load_neighbours(spath, p);
    CHECK(st2.size_cum == st.size_cum && st2.logZbar0 == st.logZbar0 && st2.blocks == st.blocks && nb2.ptr == nb.ptr && nb2.idx == nb.idx); }
  CalInputs ci; ci.D = std::move(D); ci.dpath = dpath; ci.spath = spath; ci.p = p;
  return ci;
}
TEST(calibrate_command_end_to_end) {
  TmpGuard tg;
  CalInputs CI = make_cal_inputs(tg, "cal");
  const v4::Data& D = CI.D; const std::string& dpath = CI.dpath; const std::string& spath = CI.spath; const int p = CI.p;
  auto calibrate = [&](const std::string& mode, int threads, const std::string& out) {
    v4::Json a = v4::Json::object(); a["data"] = dpath; a["setup"] = spath; a["out"] = out; a["mode"] = mode; a["seed"] = 77.0; a["threads"] = (double)threads;
    return v4::calib::run(a);
  };
  std::map<std::string, v4::wp4io::CalibIn> got;
  for (auto [mode, th] : std::vector<std::pair<std::string, int>>{{"compat", 1}, {"law", 3}, {"V", 1}, {"V", 3}}) {
    const std::string out = tg.add(wp3_tmp("cal_" + mode + std::to_string(th) + ".bin"));
    double t0 = omp_get_wtime();
    v4::Json rec = calibrate(mode, th, out);
    CHECKF(rec.at("status").str() == "completed" && rec.at("cal_status").str() == "ok", "%s threads %d: status %s", mode.c_str(), th, rec.at("status").str().c_str());
    if (rec.at("status").str() != "completed") continue;
    v4::wp4io::CalibIn ci = v4::wp4io::read_calib(out, p, D.K);
    CHECKF(ci.grid.size() >= 2 && ci.grid.front() == 0.0 && ci.grid.back() == 1.0 && !ci.inherited.empty() && ci.has_hpm, "%s: calib.bin", mode.c_str());
    std::printf("  calibrate %-6s threads %d: %.1f s, tier %d, T = %zu, %zu inherited models, HPM |S| = %zu\n", mode.c_str(), th, omp_get_wtime() - t0,
                ci.tier, ci.grid.size() - 1, ci.inherited.size(), ci.hpm.size());
    const std::string key = mode + (mode == "V" ? "" : std::to_string(th));
    if (got.count(key)) {   // V with 1 and 3 threads: the same calibration
      const auto& o = got[key];
      bool same = o.grid == ci.grid && o.tier == ci.tier && o.inherited.size() == ci.inherited.size() && o.hpm == ci.hpm;
      for (size_t i = 0; same && i < ci.inherited.size(); ++i) same = o.inherited[i].S == ci.inherited[i].S && same_bits(o.inherited[i].F, ci.inherited[i].F);
      CHECKF(same, "%s: calibration differs between runs / thread counts", mode.c_str());
    } else got[key] = ci;
  }
}

// Review PR46 MAJOR-2 (INTERFACES §7: admission refuses "before any allocation"): at p ~ 20,000 every full reader
// allocates p-sized arrays (Zobrist keys, blk / pos / members, logr: >= 80 KB each), while the bounded plan readers
// (read_data_plan, WP3's read_setup_dims) allocate the section table, meta, blk_ptr (J + 1 entries; blocks of 4 here)
// and the size law. Every operator new during an over-budget `calib::run` is counted: none may reach 64 KiB, and the
// total stays below 1 MiB (the old order, load_data + read_setup first, allocates 160,000 B at once).
TEST(calibrate_admission_before_allocation) {
  const int n = 8, p_raw = 20000;
  std::vector<double> X((size_t)n * p_raw), y(n);
  { std::mt19937_64 g(47); std::normal_distribution<double> nd;
    for (auto& x : X) x = nd(g); for (auto& v : y) v = nd(g); }
  v4::prep::Result pr = v4::prep::preprocess(X.data(), y.data(), n, p_raw);
  CHECK(pr.status == "ok");
  if (pr.status != "ok") return;
  v4::Data D = v4::make_data(pr.own, n, pr.p);
  const int p = D.p;
  CHECK(p > 10000);
  TmpGuard tg;
  const std::string dpath = tg.add(wp3_tmp("adm_data.bin")), spath = tg.add(wp3_tmp("adm_setup.bin"));
  const std::string dhash = v4::prep::write_data(dpath, D, pr, "B", v4::Json::object());
  v4::wp4io::SetupView S;   // blocks of 4 columns (the last 1..4); logr = 0; the tables' empty model and {0}; size law P(0) = P(1) = 1/2
  S.blk_ptr.push_back(0); S.code_ptr.push_back(0);
  for (int j0 = 0; j0 < p; j0 += 4) {
    const int m = std::min(4, p - j0), b = j0 / 4;
    for (int i = 0; i < m; ++i) { S.blk.push_back(b); S.pos.push_back(i); S.blk_members.push_back(j0 + i); }
    S.blk_ptr.push_back(j0 + m);
    for (int c = 0; c < (1 << m); ++c) S.logr.push_back(0.0);
    S.code_ptr.push_back((int64_t)S.logr.size());
  }
  S.ttop.init(40ull * p + 1, Order::HPM); S.tlead0.init(20ull * p, Order::LEX); S.tlead1.init(20ull * p, Order::LEX);
  for (const Model& U : {Model{}, Model{0}}) {
    const double F = D.logprior[U.size()] + (U.empty() ? 0.0 : -1.0);
    S.ttop.offer(F, U, D.zob.hash(U)); S.tlead0.offer(F, U, D.zob.hash(U)); S.tlead1.offer(F, U, D.zob.hash(U));
  }
  S.ttop.compact(); S.tlead0.compact(); S.tlead1.compact();
  S.mode_S = Model{0};
  S.size_logmass.assign((size_t)D.K + 1, -std::numeric_limits<double>::infinity()); S.size_logmass[0] = S.size_logmass[1] = std::log(0.5);
  v4::Json sin = v4::Json::object(); sin["data.bin"] = dhash;
  const std::string s0 = tg.add(wp3_tmp("adm_setup0.bin"));
  v4::wp4io::write_setup_min(s0, S, sin);
  { v4::fmt::Reader R(s0); v4::fmt::Writer W(v4::fmt::K_SETUP, v4::fmt::M_COMPAT);   // + empty neighbour lists (the dimensions reader needs them)
    for (const auto& e : R.sections()) {
      const std::string nm(e.name);
      if (e.dtype == v4::fmt::D_JSON) { W.add_json(nm, R.json(nm)); continue; }
      const void* q = e.dtype == v4::fmt::D_F64 ? (const void*)R.get<double>(nm) : e.dtype == v4::fmt::D_I32 ? (const void*)R.get<int32_t>(nm)
                    : e.dtype == v4::fmt::D_U32 ? (const void*)R.get<uint32_t>(nm) : e.dtype == v4::fmt::D_I64 ? (const void*)R.get<int64_t>(nm)
                    : e.dtype == v4::fmt::D_U64 ? (const void*)R.get<uint64_t>(nm) : e.dtype == v4::fmt::D_U16 ? (const void*)R.get<uint16_t>(nm)
                    : (const void*)R.get<uint8_t>(nm);
      W.add_copy(nm, e.dtype, q, e.length, e.dims[0], e.dims[1]);
    }
    const std::vector<int64_t> nbp((size_t)p + 1, 0); const std::vector<int32_t> nbi;
    W.add("nb_ptr", nbp); W.add("nb_idx", nbi); W.write(spath); }
  for (int plan_only : {0, 1}) {
    v4::Json a = v4::Json::object(); a["data"] = dpath; a["setup"] = spath; a["mode"] = "V"; a["mem_budget"] = 1.0;
    a["plan_only"] = (double)plan_only; a["seed"] = 5.0; a["out"] = tg.add(wp3_tmp("adm_calib.bin"));
    g_new_calls = 0; g_new_bytes = 0; g_new_max = 0;
    g_new_track = true;
    v4::Json r = v4::calib::run(a);
    g_new_track = false;
    const uint64_t calls = g_new_calls, bytes = g_new_bytes, mx = g_new_max;
    std::printf("  plan_only %d: %llu allocations, %llu B, largest %llu B before the refusal\n", plan_only, (unsigned long long)calls,
                (unsigned long long)bytes, (unsigned long long)mx);
    CHECKF(r.at("status").str() == "resource_limit", "plan_only %d: status %s", plan_only, r.at("status").str().c_str());
    CHECKF(mx < (64u << 10) && bytes < (1u << 20), "plan_only %d: largest %llu B, total %llu B", plan_only, (unsigned long long)mx, (unsigned long long)bytes);
  }
}

// ---------------------------------------------------------------------------------------------------------------
// O1 (WP3_ARCH_REVIEW R4): the parallel I1 check is the serial predicate for every thread count, on valid stores and on
// each kind of violation (order, a model twice, size > cap, a broken index), including violations at the boundaries of
// the static thread ranges.
static bool i1_all_agree(const TopStore& st, bool expect, const char* what) {
  const bool ser = st.check_invariant();
  bool ok = ser == expect;
  for (int t : {1, 2, 3, 5, 8}) { const bool par = st.check_invariant_parallel(t); if (par != ser) ok = false; }
  CHECKF(ok, "%s: serial %d, expected %d", what, (int)ser, (int)expect);
  return ok;
}
TEST(store_check_parallel_equals_serial) {
  std::mt19937_64 g(41);
  std::vector<uint64_t> key(2000); uint64_t x = 13; for (auto& k : key) k = splitmix64(x);
  for (auto ord : {Order::HPM, Order::LEX}) for (uint64_t cap : {1ull, 2ull, 9ull, 5000ull, 60000ull}) {
    TopStore st; st.init(cap, ord);
    std::vector<StoreBuffer> bufs(3);
    #pragma omp parallel for num_threads(3) schedule(dynamic, 64)
    for (int i = 0; i < 150000; ++i) {
      std::mt19937_64 gi((uint64_t)i * 7 + 1);
      Model S = random_support(gi, 2000, 1 + (int)(gi() % 6));
      const double v = -std::floor((double)(gi() % 20000) / 3.0);   // value ties: the |S| / lex tie-breaks are checked
      st.offer(bufs[omp_get_thread_num()], v, S.data(), (uint32_t)S.size(), D_hash(key, S));
    }
    for (auto& b : bufs) st.flush(b);
    st.compact();
    const size_t n = st.size();
    char tag[96]; std::snprintf(tag, sizeof tag, "ord %d cap %llu valid", (int)ord, (unsigned long long)cap);
    i1_all_agree(st, true, tag);
    if (n < 3) continue;
    Kept& K = *st.k;
    for (size_t at : {(size_t)1, n / 2, n / 3, n - 1}) {   // n/2, n/3: static range boundaries at 2 and 3 threads
      // (a) order: entry `at` better than its predecessor
      { const double keep = K.v[at]; K.v[at] = K.v[at - 1] + 1.0;
        std::snprintf(tag, sizeof tag, "ord %d cap %llu order at %zu", (int)ord, (unsigned long long)cap, at); i1_all_agree(st, false, tag);
        K.v[at] = keep; }
      // (b) a model twice: entry `at` gets the model of an earlier entry of the same size (order by value unchanged)
      { size_t j = SIZE_MAX; for (size_t q = 0; q < at; ++q) if (K.len[q] == K.len[at] && K.v[q] > K.v[at]) { j = q; break; }
        if (j != SIZE_MAX) {
          std::vector<int32_t> saved(K.pool.begin() + K.off[at], K.pool.begin() + K.off[at] + K.len[at]); const uint64_t hs = K.hash[at];
          std::copy(K.pool.begin() + K.off[j], K.pool.begin() + K.off[j] + K.len[j], K.pool.begin() + K.off[at]); K.hash[at] = K.hash[j];
          K.rebuild_index();
          std::snprintf(tag, sizeof tag, "ord %d cap %llu duplicate %zu=%zu", (int)ord, (unsigned long long)cap, at, j); i1_all_agree(st, false, tag);
          std::copy(saved.begin(), saved.end(), K.pool.begin() + K.off[at]); K.hash[at] = hs; K.rebuild_index();
        } }
      // (d) a broken index: the slot of entry `at` cleared
      { uint64_t s = K.hash[at] & K.imask; while (K.index[s] != (uint32_t)at + 1) s = (s + 1) & K.imask;
        K.index[s] = 0;
        std::snprintf(tag, sizeof tag, "ord %d cap %llu index at %zu", (int)ord, (unsigned long long)cap, at); i1_all_agree(st, false, tag);
        K.rebuild_index(); }
    }
    // (c) size > cap
    { const uint64_t c0 = st.cap; st.cap = n - 1; std::snprintf(tag, sizeof tag, "ord %d cap %llu size > cap", (int)ord, (unsigned long long)c0);
      i1_all_agree(st, false, tag); st.cap = c0; }
    i1_all_agree(st, true, "restored");
  }
}

// O1 wiring: the check runs before every checkpoint and before the final write, once per store generation; the
// output is the same bits with the check off, at checkpoints only (default) and after every step; a broken store is
// refused (internal_error) before a checkpoint and before the final write, with and without leader stores.
TEST(store_check_at_checkpoints_and_final_write) {
  TmpGuard tg;
  Fixture F(100, 300, 43);
  for (bool leaders : {false, true}) {
    IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16; c.leaders = leaders;
    IslandRun r0 = run_island<Arith::Bit>(F.D, F.st, F.nb, c);
    const uint64_t h0 = r0.hash();
    CHECKF(r0.status == 0 && r0.ks.store_checks == 1, "leaders %d: default, no checkpoints: %llu checks", (int)leaders, (unsigned long long)r0.ks.store_checks);
    IslandConfig off = c; off.check_store = false;
    IslandRun r1 = run_island<Arith::Bit>(F.D, F.st, F.nb, off);
    CHECK(r1.hash() == h0 && r1.ks.store_checks == 0);
    IslandConfig each = c; each.check_store_each_step = true;
    IslandRun r2 = run_island<Arith::Bit>(F.D, F.st, F.nb, each);
    const int Tsteps = (int)c.grid.size() - 1 + c.L + c.Hm;
    CHECKF(r2.hash() == h0 && r2.ks.store_checks >= 1 && r2.ks.store_checks <= (uint64_t)Tsteps + 1, "leaders %d: each step: %llu checks",
           (int)leaders, (unsigned long long)r2.ks.store_checks);
    if (!leaders) {   // checkpoints at every step (leaders: final-role tests only, no checkpoint path needed)
      IslandConfig ck = c; ck.ckpt_path = tg.add(wp3_tmp("o1_ck")); ck.ckpt_every_s = 0;
      wp3_rm(ck.ckpt_path);
      IslandRun r3 = run_island<Arith::Bit>(F.D, F.st, F.nb, ck);
      // one check per checkpoint with a new store generation (steps 0..Tsteps); the final write then finds the last
      // generation checked and does not check again
      CHECKF(r3.hash() == h0 && r3.ks.store_checks >= 2 && r3.ks.store_checks <= (uint64_t)Tsteps + 1, "checkpoints: %llu checks", (unsigned long long)r3.ks.store_checks);
      std::printf("  checkpoint every step: %llu checks (%.4f s), each-step mode %llu, default %llu, off %llu: hash %016llx in all\n",
                  (unsigned long long)r3.ks.store_checks, r3.ks.t_check, (unsigned long long)r2.ks.store_checks, (unsigned long long)r0.ks.store_checks,
                  (unsigned long long)r1.ks.store_checks, (unsigned long long)h0);
      wp3_rm(ck.ckpt_path);
      // a broken store: refused before the next checkpoint
      IslandConfig bad = ck; bad.test_corrupt_store_step = 3;
      bool threw = false;
      try { run_island<Arith::Bit>(F.D, F.st, F.nb, bad); } catch (const v4::Error& e) { threw = e.st == v4::Status::internal_error && std::string(e.what()).find("I1") != std::string::npos; }
      CHECK(threw);
      wp3_rm(ck.ckpt_path);
    }
    // a broken store: refused before the final write (no checkpoints; corrupted after the last step)
    IslandConfig bad = c; bad.test_corrupt_store_step = Tsteps;
    bool threw = false;
    try { run_island<Arith::Bit>(F.D, F.st, F.nb, bad); } catch (const v4::Error& e) { threw = e.st == v4::Status::internal_error && std::string(e.what()).find("I1") != std::string::npos; }
    CHECK(threw);
    // and with the check off it is not seen (the hook really breaks the store)
    IslandConfig bad_off = bad; bad_off.check_store = false;
    IslandRun rb = run_island<Arith::Bit>(F.D, F.st, F.nb, bad_off);
    CHECK(rb.status == 0 && rb.hash() != h0);
  }
}

// ---------------------------------------------------------------------------------------------------------------
// O2 (D-30, review PR49): the per-step cost record. Rows are contiguous and final when they close; an exit row closes
// the run; the rows sum exactly to the island's lifetime totals (counts) and to t_total (wall), uninterrupted, after a
// resume and on a failure exit; checkpointed rows are bit-identical after the resume; meta.cost round-trips; the
// sidecar is a progress log rebuilt from the rows the run continues from (no duplicate, missing or torn rows after a
// repeated resume, a lost line or a torn tail; a short write disables it without failing the island); the
// particle-major rows publish NaN for what that kernel does not measure; the output bits never change.
static std::vector<v4::Json> read_jsonl(const std::string& path) {
  std::vector<v4::Json> out; FILE* f = std::fopen(path.c_str(), "r"); if (!f) return out;
  std::string ln; int ch;
  while ((ch = std::fgetc(f)) != EOF) { if (ch == '\n') { if (!ln.empty()) out.push_back(v4::Json::parse(ln)); ln.clear(); } else ln.push_back((char)ch); }
  std::fclose(f);
  if (!ln.empty()) out.push_back(v4::Json::parse(ln));   // a torn last line throws (invalid_input): the caller fails
  return out;
}
static std::string slurp(const std::string& path) { std::string s; FILE* f = std::fopen(path.c_str(), "rb"); if (!f) return s; int c; while ((c = std::fgetc(f)) != EOF) s.push_back((char)c); std::fclose(f); return s; }
// rows sum to the run's lifetime totals
static bool cost_sums_match(const IslandRun& r, const char* what) {
  uint64_t rounds = 0, sweeps = 0, pairs = 0, passes = 0, flips = 0, act = 0, offers = 0, merges = 0, dup = 0; double wall = 0, comp = 0, chk = 0, ck = 0;
  for (const StepCost& q : r.cost) {
    rounds += q.particle_rounds; sweeps += q.sweeps; pairs += q.pairs; passes += q.passes; flips += q.flips; act += q.act_cols;
    offers += q.offers; merges += q.merges; dup += q.dup_dropped; wall += q.wall; comp += q.t_compact; chk += q.t_check; ck += q.t_ckpt;
  }
  const KernelStats& k = r.ks;
  const bool ok = rounds == k.particle_rounds && sweeps == k.particle_sweeps && pairs == k.support_label_pairs && passes == k.passes &&
                  flips == k.flip_evals && act == k.act_cols && offers == k.store_buffered && merges == k.store_merges && dup == k.store_dup_dropped &&
                  std::abs(wall - k.t_total) <= 1e-9 * std::max(1.0, k.t_total) && std::abs(comp - k.t_store_compact) <= 1e-9 &&
                  std::abs(chk - k.t_check) <= 1e-9 && std::abs(ck - k.t_ckpt) <= 1e-9 && !r.cost.empty() && r.cost.back().kind == 4;
  CHECKF(ok, "%s: rows vs totals: rounds %llu/%llu sweeps %llu/%llu flips %llu/%llu offers %llu/%llu merges %llu/%llu wall %.9f/%.9f check %.9f/%.9f", what,
         (unsigned long long)rounds, (unsigned long long)k.particle_rounds, (unsigned long long)sweeps, (unsigned long long)k.particle_sweeps,
         (unsigned long long)flips, (unsigned long long)k.flip_evals, (unsigned long long)offers, (unsigned long long)k.store_buffered,
         (unsigned long long)merges, (unsigned long long)k.store_merges, wall, k.t_total, chk, k.t_check);
  return ok;
}
// the sidecar holds exactly a header and the run's rows (as JSON)
static bool sidecar_equals(const std::string& path, const IslandRun& r, int m, const char* what) {
  auto ln = read_jsonl(path);
  bool ok = ln.size() == r.cost.size() + 1 && ln[0].contains("cost_header");
  for (size_t i = 0; ok && i < r.cost.size(); ++i) ok = ln[i + 1].dump() == cost_row_json(r.cost[i], m).dump();
  CHECKF(ok, "%s: sidecar %zu lines for %zu rows", what, ln.size(), r.cost.size());
  return ok;
}
TEST(cost_record_per_step) {
  TmpGuard tg;
  Fixture F(100, 300, 47);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  const int T = (int)c.grid.size() - 1, Tsteps = T + c.L + c.Hm, m = F.D.p + c.B + 2;
  IslandRun r0 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
  const uint64_t h0 = r0.hash();
  // (a) uninterrupted, with the sidecar: 1 + T + L + Hm step rows + the exit row; sums = totals; sidecar = rows
  IslandConfig cs = c; cs.cost_path = tg.add(wp3_tmp("o2_cost.jsonl")); wp3_rm(cs.cost_path);
  IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, cs);
  CHECK(r.status == 0 && r.hash() == h0 && r.cost_log_error.empty());
  CHECKF(r.cost.size() == (size_t)Tsteps + 2, "%zu rows", r.cost.size());
  bool ok = true;
  for (size_t i = 0; i < r.cost.size(); ++i) {
    const StepCost& q = r.cost[i];
    const int kind = i == 0 ? 0 : ((int)i <= T ? 1 : ((int)i <= T + c.L ? 2 : ((int)i <= Tsteps ? 3 : 4)));
    ok = ok && q.step == (int64_t)i && q.kind == kind && q.segment == 0 && q.kernel == 0 && q.wall >= 0 && q.mean_S > 0 && q.hwm_kb >= q.rss_kb && q.rss_kb > 0;
    if (kind == 1) ok = ok && q.phi == c.grid[i];
    if (kind >= 1 && kind <= 3) ok = ok && q.particle_rounds == (uint64_t)c.N && q.sweeps >= q.particle_rounds && q.flips > 0 && q.act_cols > 0 && q.pairs >= q.flips;
    if (kind == 4) ok = ok && std::isnan(q.phi) && q.particle_rounds == 0 && q.t_check > 0;   // the I1 check on exit is in the exit row
  }
  CHECK(ok);
  cost_sums_match(r, "uninterrupted");
  CHECK(r.cost[Tsteps].store_size == r.top_v.size());
  sidecar_equals(cs.cost_path, r, m, "uninterrupted");
  // (b) island_r.bin meta.cost: header and every column round-trip; NaN stays NaN
  {
    std::string path = tg.add(wp3_tmp("o2_island.bin"));
    write_island_file(path, r, Arith::ClassA, v4::Json::object());
    IslandFile f = read_island_file(path);
    const v4::Json& mc = f.meta.at("cost");
    bool okf = mc.at("schema").str() == "smcbvs4.cost/1" && mc.at("m").i64() == m && mc.at("N").i64() == c.N && mc.at("threads").i64() == 3 &&
               mc.at("rows").i64() == (int64_t)r.cost.size();
    for (size_t i = 0; okf && i < r.cost.size(); ++i) {
      const v4::Json row = cost_row_json(r.cost[i], m);   // a named Json: items() refers into it
      for (auto& kv : row.items()) okf = okf && mc.at("columns").at(kv.first).at(i).dump() == kv.second.dump();
    }
    CHECK(okf);
    // `smcbvs4 info --meta 1` exposes meta.cost (the T5 report reads island files this way) and the binary block's
    // island ISA (D-32; WP7 O5)
    const std::string rec = tg.add(wp3_tmp("o2_info"));
    const std::string cmd = std::string(V4_SMCBVS4) + " info --in " + path + " --meta 1 --out " + rec + " > /dev/null 2>&1";
    CHECK(std::system(cmd.c_str()) == 0);
    v4::Json ij = v4::read_json_file(rec + ".json");
    CHECK(ij.at("meta").at("cost").at("rows").i64() == (int64_t)r.cost.size());
    CHECK(ij.at("meta").at("binary").at("island_isa").type() == v4::Json::STR && !ij.at("meta").at("binary").at("island_isa").str().empty());
    std::remove((rec + ".json").c_str());
  }
  // (c) checkpoint and resume at steps 0 and 3: checkpointed rows bit-identical, segments 0 then 1, lifetime totals,
  //     law-determined totals equal to the uninterrupted run's; the sidecar equals the final rows after: an orderly
  //     resume, a lost last line (crash between the checkpoint and the append), a torn tail, and a second resume from the
  //     same checkpoint (the first resume's rows beyond it discarded)
  for (int s : {0, 3}) {
    IslandConfig a = cs; a.ckpt_path = tg.add(wp3_tmp("o2_ck" + std::to_string(s))); a.ckpt_every_s = 1e9; a.stop_after_step = s;
    a.cost_path = tg.add(wp3_tmp("o2_cost_ck" + std::to_string(s) + ".jsonl"));
    wp3_rm(a.ckpt_path); wp3_rm(a.cost_path);
    IslandRun r1 = run_island<Arith::ClassA>(F.D, F.st, F.nb, a);
    CHECK(r1.status == 1 && r1.cost.size() == (size_t)s + 2 && r1.cost.back().kind == 4);
    cost_sums_match(r1, "interrupted");
    IslandConfig b = a; b.stop_after_step = -1;
    for (int variant = 0; variant < 4; ++variant) {
      if (variant == 1) {   // drop the sidecar's last line
        std::string t = slurp(a.cost_path); t.pop_back(); t = t.substr(0, t.rfind('\n') + 1);
        FILE* f = std::fopen(a.cost_path.c_str(), "wb"); std::fwrite(t.data(), 1, t.size(), f); std::fclose(f);
      } else if (variant == 2) {   // a torn tail
        FILE* f = std::fopen(a.cost_path.c_str(), "ab"); std::fputs("{\"step\":99,\"wa", f); std::fclose(f);
      }
      IslandRun r2 = run_island<Arith::ClassA>(F.D, F.st, F.nb, b);   // variant 3: the same checkpoint again
      bool okr = r2.status == 0 && r2.hash() == h0 && r2.resumed_from_step == s && r2.cost.size() == (size_t)Tsteps + 2;
      for (size_t i = 0; okr && i < r2.cost.size(); ++i) okr = r2.cost[i].step == (int64_t)i && r2.cost[i].segment == ((int)i <= s ? 0 : 1);
      for (int i = 0; okr && i <= s; ++i) okr = std::memcmp(&r2.cost[i], &r1.cost[i], sizeof(StepCost)) == 0;   // every raw field
      CHECKF(okr, "resume at %d (variant %d): rows %zu", s, variant, r2.cost.size());
      cost_sums_match(r2, "resumed");
      CHECKF(r2.ks.particle_rounds == r.ks.particle_rounds && r2.ks.particle_sweeps == r.ks.particle_sweeps &&
             r2.ks.support_label_pairs == r.ks.support_label_pairs, "resume %d: rounds %llu/%llu sweeps %llu/%llu pairs %llu/%llu flips %llu/%llu", s,
             (unsigned long long)r2.ks.particle_rounds, (unsigned long long)r.ks.particle_rounds, (unsigned long long)r2.ks.particle_sweeps,
             (unsigned long long)r.ks.particle_sweeps, (unsigned long long)r2.ks.support_label_pairs, (unsigned long long)r.ks.support_label_pairs,
             (unsigned long long)r2.ks.flip_evals, (unsigned long long)r.ks.flip_evals);
      sidecar_equals(a.cost_path, r2, m, "resumed");
    }
    wp3_rm(a.ckpt_path); wp3_rm(a.cost_path);
  }
  // (d) a short sidecar write: the log is cut back to whole lines and disabled; the island and meta.cost are unaffected
  {
    IslandConfig a = cs; a.cost_path = tg.add(wp3_tmp("o2_cost_short.jsonl")); a.test_cost_log_short = 3; wp3_rm(a.cost_path);
    IslandRun rs = run_island<Arith::ClassA>(F.D, F.st, F.nb, a);
    CHECK(rs.status == 0 && rs.hash() == h0 && !rs.cost_log_error.empty() && rs.cost.size() == (size_t)Tsteps + 2);
    auto ln = read_jsonl(a.cost_path);   // throws on a torn line
    CHECKF(ln.size() == 1 + 3, "short write: %zu whole lines", ln.size());
    const std::string t = slurp(a.cost_path); CHECK(!t.empty() && t.back() == '\n');
    cost_sums_match(rs, "short write");
  }
  // (e) a failure exit (memory budget after step 1): the exit row carries the rest; sums = totals
  {
    IslandConfig a = c; a.test_admission_k = .5; a.mem_budget = plan_island(F.D, F.st, a).total + 1024;
    IslandRun rf = run_island<Arith::ClassA>(F.D, F.st, F.nb, a);
    CHECK(rf.status == 3 && rf.cost.size() == 3 && rf.cost.back().kind == 4);
    cost_sums_match(rf, "budget exit");
  }
  // (f) particle-major: label-major-only fields are NaN in the JSON (never 0); measured ones are numbers; sums hold
  {
    IslandConfig a = c; a.kernel = KernelKind::ParticleMajor; a.threads = 1;
    IslandRun rp = run_island<Arith::Bit>(F.D, F.st, F.nb, a);
    CHECK(rp.status == 0 && rp.cost.size() == (size_t)Tsteps + 2 && rp.cost[1].kernel == 1);
    cost_sums_match(rp, "particle-major");
    v4::Json j = cost_row_json(rp.cost[1], m);
    bool okp = j.at("particle_rounds").num() == c.N && j.at("t_pm").type() == v4::Json::NUM && j.at("kernel").str() == "pm";
    for (const char* k : {"sweeps", "passes", "pairs", "flips", "act_cols", "M", "flips_per_step", "act_cols_per_pass", "t_phaseA", "t_phaseB"})
      okp = okp && j.at(k).type() == v4::Json::NUM && std::isnan(j.at(k).num());
    CHECKF(okp, "particle-major row %s", j.dump().c_str());
    CHECK(std::isnan(cost_row_json(r.cost[1], m).at("t_pm").num()));   // and the label-major row's t_pm
  }
  std::printf("  %zu rows; bridge stage 1: wall %.3f s, M %.3f, mean |S| %.2f, flips/step %.3f, active columns/pass %.1f, offers %llu; exit row %.4f s\n",
              r.cost.size(), r.cost[1].wall, (double)r.cost[1].sweeps / r.cost[1].particle_rounds, r.cost[1].mean_S,
              (double)r.cost[1].flips / ((double)r.cost[1].particle_rounds * m), (double)r.cost[1].act_cols / std::max<uint64_t>(1, r.cost[1].passes),
              (unsigned long long)r.cost[1].offers, r.cost.back().wall);
}

// Review PR47 finding 1: I1 runs on every exit, whatever the status. The reviewer's case (a final island stopped by the
// step-boundary memory budget after step 1) and a caught out-of-memory in the parallel compaction: a valid store is
// checked once and the island returns resource_limit; a corrupted store raises internal_error, so no IslandRun and no
// island file exist (INTERFACES §7: internal_error before resource_limit).
TEST(store_check_on_failure_exits) {
  TmpGuard tg;
  Fixture F(100, 300, 43);
  IslandConfig base = small_cfg(); base.kernel = KernelKind::LabelMajor; base.threads = 3; base.G = 16;
  auto expect_i1_error = [&](const IslandConfig& c, const char* what) {
    bool threw = false; std::string msg;
    try { IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
          msg = "returned status " + std::to_string(r.status) + " (" + r.reason + "), checks " + std::to_string(r.ks.store_checks); }
    catch (const v4::Error& e) { threw = e.st == v4::Status::internal_error && std::string(e.what()).find("I1") != std::string::npos; msg = e.what(); }
    CHECKF(threw, "%s: %s", what, msg.c_str());
  };
  // (a) step-boundary budget exit (the reviewer's reproducer)
  IslandConfig b = base; b.test_admission_k = .5; b.mem_budget = plan_island(F.D, F.st, b).total + 1024;
  {
    IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, b);
    CHECKF(r.status == 3 && r.reason.find("mem_budget") != std::string::npos && r.ks.store_checks == 1, "budget exit, valid store: status %d checks %llu",
           r.status, (unsigned long long)r.ks.store_checks);
    std::string path = tg.add(wp3_tmp("pr47_budget.bin"));   // the failure file of a checked store is still written (no estimates)
    write_island_file(path, r, Arith::ClassA, v4::Json::object());
    CHECK(read_island_file(path).meta.at("status").str() == "resource_limit");
  }
  IslandConfig bc = b; bc.test_corrupt_store_step = 1;
  expect_i1_error(bc, "budget exit, corrupted store");
  // (b) a caught out-of-memory (inside phase A, the first pass of step 2: no compaction between the corruption after
  //     step 1 and the failure)
  uint64_t passes1 = 0;
  {
    IslandConfig a = base; a.ckpt_path = tg.add(wp3_tmp("pr47_ck")); a.ckpt_every_s = 1e9; a.stop_after_step = 1; wp3_rm(a.ckpt_path);
    passes1 = run_island<Arith::ClassA>(F.D, F.st, F.nb, a).ks.passes;   // passes up to the end of step 1
    wp3_rm(a.ckpt_path);
  }
  IslandConfig o = base; o.test_oom_pass = (int)passes1;   // throws in pass passes1 + 1
  {
    IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, o);
    CHECKF(r.status == 3 && r.reason.find("out of memory") != std::string::npos && r.ks.store_checks == 1 && r.ks.passes == passes1 + 1,
           "oom exit, valid store: status %d '%s' checks %llu passes %llu", r.status, r.reason.c_str(), (unsigned long long)r.ks.store_checks,
           (unsigned long long)r.ks.passes);
  }
  IslandConfig oc = o; oc.test_corrupt_store_step = 1;
  expect_i1_error(oc, "oom exit, corrupted store");
  // (c) numerical-failure exits are covered by the same call (it precedes every status branch); interrupted runs by the
  //     checkpoint guard (store_check_at_checkpoints_and_final_write)
}

// WP7 O5: the pilot-only path (include/v4/island/pilot_only.h, tool v4_pilot_island) runs the same island as the first
// island of `calibrate --mode V`: with the same seed, the per-step cost records of the two pilots agree step by step in
// every law-determined field (phi, rounds, sweeps, pairs, passes, active columns, store size, mean |S|), at 1 and 3 threads.
// Also: calibrate --cost-dir writes one record per calibration island (pilot + diagnostic islands).
TEST(pilot_only_equals_calibrate_pilot) {
  TmpGuard tg;
  CalInputs CI = make_cal_inputs(tg, "pil");
  auto rows_of = [](const std::string& path) {
    std::vector<v4::Json> r; for (auto& j : read_jsonl(path)) if (!j.contains("cost_header")) r.push_back(j); return r;
  };
  // law-determined fields only: flips (K1's bounded count) and offers (the snapshot duplicate filter) depend on the schedule
  const char* keys[] = {"step", "kind", "phi", "particle_rounds", "sweeps", "pairs", "store_size", "mean_S", "act_cols", "passes"};
  std::vector<v4::Json> ref;
  auto section_hashes = [](const std::string& path) {   // every section but meta
    v4::fmt::Reader Rd(path); std::map<std::string, std::string> m;
    for (auto& e : Rd.sections()) { if (std::string(e.name) == "meta") continue; std::string h; char x[3]; for (int i = 0; i < 32; ++i) { std::snprintf(x, 3, "%02x", e.sha256[i]); h += x; } m[e.name] = h; }
    return m;
  };
  std::string cal3;   // the 3-thread calibrate run with --cost-dir (compared with a run without it below)
  for (int th : {1, 3}) {
    const std::string cdir = tg.add(wp3_tmp("pil_cal_cost" + std::to_string(th)));
    const std::string out = tg.add(wp3_tmp("pil_cal" + std::to_string(th) + ".bin"));
    v4::Json a = v4::Json::object(); a["data"] = CI.dpath; a["setup"] = CI.spath; a["out"] = out; a["mode"] = "V"; a["seed"] = 77.0;
    a["threads"] = (double)th; a["cost_dir"] = cdir;
    v4::Json rec = v4::calib::run(a);
    CHECK(rec.at("status").str() == "completed" && rec.at("cal_status").str() == "ok");   // #52: task status + cal_status
    if (th == 3) cal3 = out;
    int nfiles = 0, ndiag = 0;
    for (auto& de : std::filesystem::directory_iterator(cdir)) { ++nfiles; ndiag += de.path().filename().string().rfind("cost_diag_", 0) == 0; }
    CHECKF(nfiles >= 2 && ndiag >= 1, "threads %d: %d cost records, %d diagnostic", th, nfiles, ndiag);
    auto cal = rows_of(calib_cost_path(cdir, true, 0, 0, 0));
    const std::string pdir = tg.add(wp3_tmp("pil_only_cost" + std::to_string(th)));
    v4::Json pa = v4::Json::object(); pa["data"] = CI.dpath; pa["setup"] = CI.spath; pa["seed"] = 77.0; pa["threads"] = (double)th; pa["cost_dir"] = pdir;
    int rc = -1;
    v4::Json pr = run_pilot_only(pa, rc);
    CHECKF(rc == 0 && pr.at("status").str() == "completed", "pilot-only threads %d: rc %d %s", th, rc, pr.dump().c_str());
    auto pil = rows_of(pr.at("cost_record").str());
    bool same = !cal.empty() && cal.size() == pil.size() && (int64_t)pil.size() == pr.at("T").i64() + 2 + pr.at("settings").at("L").i64() + pr.at("settings").at("Hm").i64();   // + the exit row
    for (size_t i = 0; same && i < cal.size(); ++i) for (const char* k : keys) if (cal[i].at(k).dump() != pil[i].at(k).dump()) { same = false; std::printf("  step %zu key %s: %s vs %s\n", i, k, cal[i].at(k).dump().c_str(), pil[i].at(k).dump().c_str()); }
    CHECKF(same, "threads %d: calibrate pilot %zu rows, pilot-only %zu rows", th, cal.size(), pil.size());
    if (ref.empty()) ref = pil;
    else {   // and the same island at 1 and 3 threads (T3 through the record)
      bool t3 = ref.size() == pil.size();
      for (size_t i = 0; t3 && i < ref.size(); ++i) for (const char* k : {"phi", "sweeps", "store_size", "mean_S"}) t3 = t3 && ref[i].at(k).dump() == pil[i].at(k).dump();
      CHECK(t3);
    }
    std::printf("  threads %d: pilot T = %lld (%lld forced), %zu rows, %.2f s; calibrate wrote %d cost records (%d diagnostic)\n", th,
                (long long)pr.at("T").i64(), (long long)pr.at("forced").i64(), pil.size(), pr.at("seconds_island").num(), nfiles, ndiag);
    if (th == 3) {   // review PR55 INFO-8: the schedule-dependent counts, two pilot-only runs of one binary
      const std::string pdir2 = tg.add(wp3_tmp("pil_only_cost3b"));
      v4::Json pb = pa; pb["cost_dir"] = pdir2; int rc2 = -1; v4::Json pr2 = run_pilot_only(pb, rc2);
      auto pil2 = rows_of(pr2.at("cost_record").str());
      uint64_t f1 = 0, f2 = 0; for (auto& j : pil) f1 += j.at("flips").type() == v4::Json::NUM ? (uint64_t)j.at("flips").num() : 0;
      for (auto& j : pil2) f2 += j.at("flips").type() == v4::Json::NUM ? (uint64_t)j.at("flips").num() : 0;
      std::printf("  two pilot-only runs at 3 threads: flips %llu vs %llu (%s)\n", (unsigned long long)f1, (unsigned long long)f2,
                  f1 == f2 ? "equal this time" : "run-to-run execution variation in one binary");
    }
  }
  {   // review PR55 m7a: --cost-dir (and --verbose) leave calib.bin's sections unchanged
    const std::string out = tg.add(wp3_tmp("pil_cal_nocost.bin"));
    v4::Json a = v4::Json::object(); a["data"] = CI.dpath; a["setup"] = CI.spath; a["out"] = out; a["mode"] = "V"; a["seed"] = 77.0; a["threads"] = 3.0;
    CHECK(v4::calib::run(a).at("status").str() == "completed");
    CHECK(!cal3.empty() && section_hashes(out) == section_hashes(cal3));
  }
}

// D-32 (2): the merge refuses islands of two FMA families in V mode (class-A bits differ); the same family is accepted;
// theory merges are unaffected by the ISA field
TEST(merge_refuses_mixed_fma_families) {
  v4::Json a = v4::binary_block(), b = v4::binary_block();
  auto with = [](v4::Json j, const char* isa) {   // a block of that ISA: the name and the class-A unit's own FMA flag
    j["island_isa"] = isa; const std::string s(isa); j["island_fma"] = !(s == "portable" || s == "x86-64-v2"); return j;
  };
  CHECK(v4::binary_compatible(with(a, "sapphirerapids"), with(b, "x86-64-v3"), v4::BinaryUse::MergeV).ok);
  CHECK(!v4::binary_compatible(with(a, "sapphirerapids"), with(b, "portable"), v4::BinaryUse::MergeV).ok);
  CHECK(!v4::binary_compatible(with(a, "x86-64-v2"), with(b, "x86-64-v4"), v4::BinaryUse::MergeV).ok);
  CHECK(v4::binary_compatible(with(a, "portable"), with(b, "portable"), v4::BinaryUse::MergeV).ok);
  CHECK(!a.at("island_isa").str().empty());
  // island_fma (the class-A unit's answer) wins over the name: a V4_WIDE_ISA build labelled "x86-64-v3" with FMA
  v4::Json w = a; w["island_isa"] = "portable"; w["island_fma"] = true;
  CHECK(!v4::binary_compatible(w, with(b, "portable"), v4::BinaryUse::MergeV).ok);
  CHECK(v4::binary_compatible(w, with(b, "x86-64-v3"), v4::BinaryUse::MergeV).ok);
}

// ---------------------------------------------------------------------------------------------------------------
// WP7 O4: the checkpoint checksum (ckpt_sum.h) is a function of the byte stream alone: any chunking of the writer's
// calls, any number of threads and the whole-region form give the same value; a changed byte (at block boundaries too),
// a changed length and the empty stream differ. A checkpoint of the older (serial checksum) format is refused, not ignored.
TEST(checkpoint_checksum_is_chunking_and_thread_independent) {
  std::mt19937_64 g(33);
  const size_t B = BlockSum::B;
  for (size_t n : {(size_t)0, (size_t)1, (size_t)8, B - 1, B, B + 1, 2 * B, 3 * B + 17, 5 * B + B / 3}) {
    std::vector<unsigned char> d(n); for (auto& x : d) x = (unsigned char)g();
    const uint64_t ref = BlockSum::of_region(d.data(), n, 1);
    bool ok = true;
    for (int th : {1, 2, 3, 5}) {
      ok = ok && BlockSum::of_region(d.data(), n, th) == ref;
      for (int rep = 0; rep < 3; ++rep) {   // random chunkings, including empty adds and chunks that straddle blocks
        BlockSum s(th); size_t pos = 0;
        while (pos < n) {
          size_t take = rep == 0 ? 1 + (size_t)(g() % 97) : (rep == 1 ? 1 + (size_t)(g() % (3 * B)) : n);
          take = std::min(take, n - pos);
          s.add(d.data() + pos, take); pos += take; if (g() % 5 == 0) s.add(d.data() + pos, 0);
        }
        ok = ok && s.finish() == ref && s.length() == n;
      }
    }
    CHECKF(ok, "n %zu: the checksum depends on the chunking or the thread count", n);
    if (n == 0) continue;
    // one changed byte anywhere (first, block edges, last) changes it
    for (size_t at : {(size_t)0, n / 2, n - 1, std::min(n - 1, B - 1), std::min(n - 1, B)}) {
      d[at] ^= 0x40; const uint64_t h2 = BlockSum::of_region(d.data(), n, 3); d[at] ^= 0x40;
      CHECKF(h2 != ref, "n %zu: a changed byte at %zu is not detected", n, at);
    }
    // the length is part of the value: the stream with one more zero byte differs
    std::vector<unsigned char> e = d; e.push_back(0);
    CHECK(BlockSum::of_region(e.data(), e.size(), 2) != ref);
  }
  CHECK(BlockSum::of_region(nullptr, 0, 1) == BlockSum(1).finish());
}

TEST(checkpoint_of_the_older_format_is_refused) {
  TmpGuard tg;
  Fixture F(100, 300, 61);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  IslandConfig a = c; a.ckpt_path = tg.add(wp3_tmp("o4_oldfmt")); a.ckpt_every_s = 1e9; a.stop_after_step = 2; wp3_rm(a.ckpt_path);
  CHECK(run_island<Arith::ClassA>(F.D, F.st, F.nb, a).status == 1);
  // a checkpoint of the new format written with 3 threads resumes with 1 (the checksum does not depend on threads)
  { IslandConfig b = a; b.stop_after_step = -1; b.threads = 1; b.G = 7;
    IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, b);
    CHECK(r.status == 0 && r.resumed_from_step == 2 && r.hash() == run_island<Arith::ClassA>(F.D, F.st, F.nb, c).hash()); }
  for (const char* sfx : {".a", ".b"}) {   // the files stay after run_island (the command removes them); make them the old magic ...CKP
    FILE* f = std::fopen((a.ckpt_path + sfx).c_str(), "r+b"); if (!f) continue;
    std::fseek(f, 7, SEEK_SET); std::fputc('P', f); std::fclose(f);
  }
  bool refused = false; std::string msg;
  try { IslandConfig b = a; b.stop_after_step = -1; run_island<Arith::ClassA>(F.D, F.st, F.nb, b); }
  catch (const v4::Error& e) { refused = e.st == v4::Status::invalid_input; msg = e.what(); }
  CHECKF(refused && msg.find("older format") != std::string::npos, "old-format refusal: %s", msg.c_str());
}

// WP7 O4: the soft time stop. stop_after_s ends the run at a step boundary with a checkpoint (status 1, time_stopped);
// a chain of such stops, each resuming from the last checkpoint with another thread count / group size, ends with the
// uninterrupted island's hash; each attempt makes progress (at least one step); the last step is never stopped;
// invalid values are refused.
TEST(time_stop_chain_equals_uninterrupted) {
  TmpGuard tg;
  Fixture F(100, 300, 62);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  const uint64_t h0 = run_island<Arith::ClassA>(F.D, F.st, F.nb, c).hash();
  const int Tsteps = (int)c.grid.size() - 1 + c.L + c.Hm;
  IslandConfig a = c; a.ckpt_path = tg.add(wp3_tmp("o4_chain")); a.ckpt_every_s = 1e9; a.stop_after_s = 1e-6; wp3_rm(a.ckpt_path);
  int attempts = 0, last = -1; bool done = false;
  while (attempts < Tsteps + 5 && !done) {
    IslandConfig b = a; b.threads = 1 + attempts % 3; b.G = attempts % 2 ? 7 : 16;
    IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, b);
    ++attempts;
    if (r.status == 0) { done = true; CHECKF(r.hash() == h0 && r.resumed_from_step == last, "chain end: hash %016llx vs %016llx, resumed %d vs %d", (unsigned long long)r.hash(), (unsigned long long)h0, r.resumed_from_step, last); }
    else {
      CHECKF(r.status == 1 && r.time_stopped && r.stopped_after_step > last, "attempt %d: status %d stopped %d after %d", attempts, r.status, r.stopped_after_step, last);
      CHECK(r.stopped_after_step < Tsteps);   // the final step is never stopped
      last = r.stopped_after_step;
    }
  }
  CHECKF(done && attempts >= 3, "the chain ended after %d attempts (done %d)", attempts, (int)done);
  std::printf("  time-stop chain: %d attempts (threads 1/2/3, G 16/7), same hash as the uninterrupted island\n", attempts);
  // refusals
  bool r1 = false, r2 = false;
  try { IslandConfig b = c; b.stop_after_s = 1.0; run_island<Arith::ClassA>(F.D, F.st, F.nb, b); } catch (const v4::Error& e) { r1 = e.st == v4::Status::invalid_input; }   // no checkpoint path
  try { IslandConfig b = a; b.stop_after_s = -1.0; run_island<Arith::ClassA>(F.D, F.st, F.nb, b); } catch (const v4::Error& e) { r2 = e.st == v4::Status::invalid_input; }
  CHECK(r1 && r2);
}

// WP7: `smcbvs4 info FILE --meta 1` reads the header, the table and the meta section only (a 2 GB island file at 10^6 took
// 11-19 s per full verification, and the T5 report called it for every island). The file can be the first argument; the
// meta section's hash is still checked; a damaged OTHER section is not seen by --meta alone and is refused by the
// default (full) read and by --verify 1; a missing file argument is invalid_input.
TEST(info_meta_only_reads_the_meta_section) {
  TmpGuard tg;
  Fixture F(100, 300, 63);
  IslandConfig c = small_cfg(); c.kernel = KernelKind::LabelMajor; c.threads = 3; c.G = 16;
  IslandRun r = run_island<Arith::ClassA>(F.D, F.st, F.nb, c);
  const std::string path = tg.add(wp3_tmp("info_meta.bin")), rec = tg.add(wp3_tmp("info_rec"));
  write_island_file(path, r, Arith::ClassA, v4::Json::object());
  auto info = [&](const std::string& args) {
    const std::string cmd = std::string(V4_SMCBVS4) + " info " + args + " --out " + rec + " > /dev/null 2>&1";
    const int rc = std::system(cmd.c_str()); return WIFEXITED(rc) ? WEXITSTATUS(rc) : -1;
  };
  CHECK(info(path + " --meta 1") == 0);   // the file as the first argument
  { v4::Json j = v4::read_json_file(rec + ".json");
    CHECK(j.at("verified").type() == v4::Json::STR && j.at("verified_sections").str() == "meta" && j.at("meta").at("cost").at("rows").i64() == (int64_t)r.cost.size() &&
          j.at("sections").size() > 10 && j.at("kind").str() == "island"); }
  CHECK(info("--in " + path + " --meta 1") == 0);   // the driver's form
  CHECK(info(path) == 0); CHECK(v4::read_json_file(rec + ".json").at("verified").boolean());   // default: every section
  CHECK(info("--meta 1") == 13);                    // no file
  // damage one byte inside top_v (not the meta section)
  uint64_t top_off = 0, meta_off = 0;
  { v4::fmt::Reader R(path, false); for (const auto& e : R.sections()) { if (std::string(e.name) == "top_v") top_off = e.offset; if (std::string(e.name) == "meta") meta_off = e.offset; } }
  auto flip = [&](uint64_t at) { FILE* f = std::fopen(path.c_str(), "r+b"); std::fseek(f, (long)at + 3, SEEK_SET); int ch = std::fgetc(f); std::fseek(f, (long)at + 3, SEEK_SET); std::fputc(ch ^ 0x5A, f); std::fclose(f); };
  CHECK(top_off > 0 && meta_off > 0);
  flip(top_off);
  CHECK(info(path) == 13);                          // full verification sees it
  CHECK(info(path + " --meta 1 --verify 1") == 13);
  CHECK(info(path + " --meta 1") == 0);             // meta-only does not read top_v (by design: header, table, meta)
  flip(top_off);                                    // restore, then damage the meta section: the meta-only read refuses it
  flip(meta_off);
  CHECK(info(path + " --meta 1") == 13);
}
