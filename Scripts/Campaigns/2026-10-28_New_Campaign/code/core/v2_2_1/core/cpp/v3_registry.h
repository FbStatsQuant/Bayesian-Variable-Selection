// Distinct scored models; this observer never affects sampling.
#pragma once
struct RegFirst { int8_t phase, mech, tier; int16_t iter, island; int32_t stage; };
struct Registry {
  int p; bool exact; std::vector<uint64_t> zob;
  std::unordered_map<uint64_t, RegFirst> seen;
  double mx = NEG_INF; long double total = 0;
  std::vector<uint8_t> hll;
  uint64_t first_by[N_PHASE][N_MECH] = {};
  double n_cal = NA_REAL, lse_cal = NA_REAL, hll_cal = NA_REAL;
  explicit Registry(const Data& d) : p(d.p), exact(d.p <= 64), zob(d.zob.key), hll(1 << 14, 0) {}
  void insert(const std::vector<int>& S, double F, const EventCtx& ev, int mech) {
    uint64_t key = 0, x = 0;
    for (int j : S) { if (exact) key |= (1ULL << j); x ^= zob[j]; }
    uint64_t h = splitmix64(x); unsigned idx = h >> 50; uint64_t tail = h << 14;
    int rank = tail ? __builtin_clzll(tail) + 1 : 51;
    hll[idx] = std::max(hll[idx], (uint8_t)rank);
    if (!exact) return;
    RegFirst first{(int8_t)ev.phase, (int8_t)mech, (int8_t)ev.tier, (int16_t)ev.iter, (int16_t)ev.island, (int32_t)ev.stage};
    if (!seen.emplace(key, first).second) return;
    first_by[ev.phase][mech]++;
    if (F > mx) { total = total * std::exp((long double)mx - F) + 1; mx = F; }
    else total += std::exp((long double)F - mx);
  }
  double lse() const { return seen.empty() ? NEG_INF : mx + std::log(total); }
  double estimate() const {
    const double m = (double)hll.size(); double sum = 0; int zero = 0;
    for (uint8_t r : hll) { sum += std::ldexp(1.0, -(int)r); if (!r) ++zero; }
    double e = (0.7213 / (1 + 1.079 / m)) * m * m / sum;
    return e <= 2.5 * m && zero ? m * std::log(m / zero) : e;
  }
  void snapshot() { n_cal = exact ? (double)seen.size() : NA_REAL; lse_cal = exact ? lse() : NA_REAL; hll_cal = estimate(); }
};
