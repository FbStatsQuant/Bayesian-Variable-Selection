// rng.h -- uniforms: position addresses + Philox4x32-10 (production), v3 xoshiro256** streams (compat).
// INTERFACES §3. Philox4x32-10: Salmon, Moraes, Dror, Shaw (2011), "Parallel random numbers: as easy as 1, 2, 3"
// (Random123); constants and round structure as the Random123 reference, checked against its known-answer vectors.
#pragma once
#include <array>
#include <cstdint>
#include <stdexcept>
#include <tuple>
#include <unordered_set>
#include "v4/model.h"

namespace v4 {

// ---------------------------------------------------------------------------------------------------------------
// Philox4x32-10
// ---------------------------------------------------------------------------------------------------------------
using Ctr4 = std::array<uint32_t, 4>;
using Key2 = std::array<uint32_t, 2>;
inline Ctr4 philox4x32_10(Ctr4 c, Key2 k) {
  constexpr uint32_t M0 = 0xD2511F53u, M1 = 0xCD9E8D57u, W0 = 0x9E3779B9u, W1 = 0xBB67AE85u;
  for (int r = 0; r < 10; ++r) {
    if (r > 0) { k[0] += W0; k[1] += W1; }
    const uint64_t p0 = (uint64_t)M0 * c[0], p1 = (uint64_t)M1 * c[2];
    const uint32_t hi0 = (uint32_t)(p0 >> 32), lo0 = (uint32_t)p0, hi1 = (uint32_t)(p1 >> 32), lo1 = (uint32_t)p1;
    c = Ctr4{hi1 ^ c[1] ^ k[0], lo1, hi0 ^ c[3] ^ k[1], lo0};
  }
  return c;
}
// 53-bit uniform in [0, 1) from two 32-bit words (hi, lo), same convention as core/cpp/v3_util.h:60.
inline double u53(uint32_t hi, uint32_t lo) { return (double)((((uint64_t)hi << 32) | lo) >> 11) * 0x1.0p-53; }

// ---------------------------------------------------------------------------------------------------------------
// Addresses (INTERFACES §3)
// ---------------------------------------------------------------------------------------------------------------
enum Role : uint8_t { R_FINAL = 0, R_PILOT = 1, R_DIAG = 2, R_POST = 3, R_GEN = 4, R_TEST = 5 };
enum XPh : uint8_t {
  X_INIT = 0, X_RESAMPLE = 1, X_BRIDGE = 2, X_BURN = 3, X_MEASURED = 4, X_POST = 5,
  X_GEN_X = 8, X_GEN_NOISE = 9, X_GEN_FACTOR = 10, X_TEST_X = 11, X_TEST_NOISE = 12, X_TEST_FACTOR = 13
};
struct Address {
  uint32_t seed = 0; uint8_t role = 0, tier = 0, iter = 0; uint32_t island = 0;   // key
  uint8_t xph = 0; uint32_t stage = 0; uint32_t particle = 0, position = 0, slot = 0;  // counter
};
// Independence step: the pi_0 draw uses slots 0..u-1 (u = uniforms it consumes), the accept test this fixed slot.
constexpr uint32_t SLOT_ACCEPT = 0xFFFFFFFFu;
inline Key2 address_key(const Address& a) {
  if (a.island >= (1u << 20) || a.iter >= 64 || a.tier >= 4 || a.role >= 16) throw std::out_of_range("address key field out of range");
  return Key2{a.seed, ((uint32_t)a.role << 28) | ((uint32_t)a.tier << 26) | ((uint32_t)a.iter << 20) | a.island};
}
inline Ctr4 address_ctr(const Address& a) {
  if (a.stage >= (1u << 24)) throw std::out_of_range("address counter field out of range");
  return Ctr4{a.slot, a.position, a.particle, ((uint32_t)a.xph << 24) | a.stage};
}
// The production uniform of an address.
inline double uniform_at(const Address& a) {
  Ctr4 x = philox4x32_10(address_ctr(a), address_key(a));
  return u53(x[1], x[0]);
}
// Both variates of one Philox block (gen only): u from words (1,0), u2 from words (3,2).
inline void uniform2_at(const Address& a, double& u, double& u2) {
  Ctr4 x = philox4x32_10(address_ctr(a), address_key(a));
  u = u53(x[1], x[0]); u2 = u53(x[3], x[2]);
}

// ---------------------------------------------------------------------------------------------------------------
// v3 serial streams (compat). core/cpp/v3_util.h:43-61, copied.
// ---------------------------------------------------------------------------------------------------------------
struct Xoshiro256ss {
  uint64_t s[4];
  uint64_t count = 0;  // 64-bit draws consumed since seeding
  static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
  void seed_stream(uint64_t seed, uint64_t stream) {
    uint64_t x = (seed << 32) + stream;
    for (int i = 0; i < 4; ++i) s[i] = splitmix64(x);
    count = 0;
  }
  inline uint64_t next() {
    ++count;
    const uint64_t result = rotl(s[1] * 5, 7) * 9;
    const uint64_t t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3];
    s[2] ^= t; s[3] = rotl(s[3], 45);
    return result;
  }
  inline double uniform() { return (double)(next() >> 11) * 0x1.0p-53; }
};
// v3 stream map (core/v3_run.R:8-11, core/cpp/v3_core.cpp:444): pilot 5e, diag 5e + r (r = 1..4), final 9 + r.
inline uint64_t compat_stream(uint8_t role, uint8_t tier, uint32_t island) {
  switch (role) {
    case R_PILOT: if (tier > 1) throw std::out_of_range("compat pilot tier (v3 has tiers 0, 1)"); return 5ull * tier;
    case R_DIAG:
      if (tier > 1) throw std::out_of_range("compat diag tier (v3 has tiers 0, 1)");
      if (island < 1 || island > 4) throw std::out_of_range("compat diag island");
      return 5ull * tier + island;
    case R_FINAL: if (island < 1 || island > 4) throw std::out_of_range("compat final island"); return 9ull + island;
    case R_TEST: return 200;
    default: throw std::out_of_range("role has no compat stream");
  }
}

// ---------------------------------------------------------------------------------------------------------------
// Sources
// ---------------------------------------------------------------------------------------------------------------
struct UniformSource {
  virtual double u(const Address& a) = 0;
  virtual ~UniformSource() = default;
};
struct AddressedSource final : public UniformSource {
  double u(const Address& a) override { return uniform_at(a); }
};
// Compat: the address is a label only; values come from the unit's serial stream in v3's order.
struct CompatSource final : public UniformSource {
  Xoshiro256ss g;
  CompatSource(uint64_t seed, uint64_t stream) { g.seed_stream(seed, stream); }
  double u(const Address&) override { return g.uniform(); }
};

// ---------------------------------------------------------------------------------------------------------------
// Invariant I5 (INTERFACES §3): CheckedSource wraps any source and checks every address it is asked for.
//   UNIQUE     (production): no address is used twice;
//   INCREASING (compat, one per stream): addresses arrive strictly increasing in serial_less, the v3 serial order
//              within one unit: calibration iteration, then INIT < (stage t: RESAMPLE < BRIDGE round) < BURN < MEASURED
//              < POST, then particle, position, slot.
// A violation throws std::logic_error (callers map it to internal_error).
// ---------------------------------------------------------------------------------------------------------------
inline auto serial_key(const Address& a) {
  int rank = a.xph == X_INIT ? 0 : (a.xph == X_RESAMPLE || a.xph == X_BRIDGE) ? 1 : a.xph == X_BURN ? 2 : a.xph == X_MEASURED ? 3 : 4 + a.xph;
  int sub = a.xph == X_BRIDGE ? 1 : 0;
  return std::make_tuple(a.seed, a.role, a.tier, a.iter, a.island, rank, a.stage, sub, a.particle, a.position, a.slot);
}
inline bool serial_less(const Address& a, const Address& b) { return serial_key(a) < serial_key(b); }

struct CheckedSource final : public UniformSource {
  enum Mode { UNIQUE, INCREASING };
  UniformSource& inner; Mode mode; uint64_t checked = 0;
  CheckedSource(UniformSource& in, Mode m) : inner(in), mode(m) {}
  double u(const Address& a) override {
    if (mode == INCREASING) {
      if (checked > 0 && !serial_less(last_, a)) throw std::logic_error("I5: address not increasing in the serial order");
      last_ = a;
    } else {
      Key2 k = address_key(a); Ctr4 c = address_ctr(a);
      if (!seen_.insert(Packed{k, c}).second) throw std::logic_error("I5: address used twice");
    }
    ++checked;
    return inner.u(a);
  }
 private:
  struct Packed { Key2 k; Ctr4 c; bool operator==(const Packed& o) const { return k == o.k && c == o.c; } };
  struct PackedHash { size_t operator()(const Packed& p) const {
    uint64_t x = ((uint64_t)p.k[0] << 32 | p.k[1]) ^ 0x9E3779B97F4A7C15ULL;
    for (uint32_t w : p.c) { x ^= w; x = splitmix64(x); }
    return (size_t)x; } };
  std::unordered_set<Packed, PackedHash> seen_;
  Address last_;
};

}  // namespace v4
