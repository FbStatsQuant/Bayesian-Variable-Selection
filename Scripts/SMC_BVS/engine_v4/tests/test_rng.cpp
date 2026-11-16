#include <set>
#include "tk.h"
#include "v4/rng.h"
#include "v3_util.h"   // core/cpp, unchanged
using namespace v4;

// Random123 known-answer vectors for philox4x32_10 (kat_vectors).
TEST(philox_kat) {
  Ctr4 r = philox4x32_10(Ctr4{0, 0, 0, 0}, Key2{0, 0});
  CHECK(r == (Ctr4{0x6627e8d5u, 0xe169c58du, 0xbc57ac4cu, 0x9b00dbd8u}));
  r = philox4x32_10(Ctr4{0xffffffffu, 0xffffffffu, 0xffffffffu, 0xffffffffu}, Key2{0xffffffffu, 0xffffffffu});
  CHECK(r == (Ctr4{0x408f276du, 0x41c83b0eu, 0xa20bc7c6u, 0x6d5451fdu}));
  r = philox4x32_10(Ctr4{0x243f6a88u, 0x85a308d3u, 0x13198a2eu, 0x03707344u}, Key2{0xa4093822u, 0x299f31d0u});
  CHECK(r == (Ctr4{0xd16cfe09u, 0x94fdccebu, 0x5001e420u, 0x24126ea1u}));
}
TEST(address_packing_and_uniqueness) {
  Address a; a.seed = 7; a.role = R_FINAL; a.island = 3; a.xph = X_BRIDGE; a.stage = 5; a.particle = 11; a.position = 13; a.slot = 2;
  Key2 k = address_key(a); Ctr4 c = address_ctr(a);
  CHECK(k[0] == 7 && k[1] == 3u); CHECK(c == (Ctr4{2, 13, 11, (2u << 24) | 5u}));
  a.role = R_DIAG; a.tier = 1; a.iter = 2; k = address_key(a);
  CHECK(k[1] == ((2u << 28) | (1u << 26) | (2u << 20) | 3u));
  // every field changes the value; values in [0, 1)
  std::set<double> seen; Address b;
  b.seed = 1;
  for (uint32_t f = 0; f < 9; ++f) for (uint32_t v = 0; v < 4; ++v) {
    Address x = b;
    switch (f) { case 0: x.seed += v; break; case 1: x.role = (uint8_t)v; break; case 2: x.tier = (uint8_t)v; break; case 3: x.iter = (uint8_t)v; break;
      case 4: x.island = v; break; case 5: x.xph = (uint8_t)v; break; case 6: x.stage = v; break; case 7: x.particle = v; break; default: x.position = v; }
    double u = uniform_at(x); CHECK(u >= 0 && u < 1); seen.insert(u);
  }
  CHECK(seen.size() == 1 + 9 * 3);   // base address shared by v = 0 of every field
  Address bad; bad.island = 1u << 20; CHECK_THROWS(uniform_at(bad));
  bad = Address(); bad.stage = 1u << 24; CHECK_THROWS(uniform_at(bad));
}
TEST(philox_uniform_moments) {
  // crude sanity (not a quality test): mean and variance of 2^20 consecutive-slot uniforms
  Address a; a.seed = 12345; double s = 0, s2 = 0; const int M = 1 << 20;
  for (int i = 0; i < M; ++i) { a.slot = (uint32_t)i; double u = uniform_at(a); s += u; s2 += u * u; }
  double m = s / M, v = s2 / M - m * m;
  CHECK(std::fabs(m - 0.5) < 0.002); CHECK(std::fabs(v - 1.0 / 12) < 0.001);
}
TEST(compat_streams_equal_v3) {
  for (uint64_t stream : {0ull, 1ull, 5ull, 10ull, 13ull, 200ull}) {
    v3::Xoshiro256ss r; r.seed_stream(424242, stream);
    CompatSource c(424242, stream); Address any;
    bool ok = true;
    for (int i = 0; i < 10000; ++i) { double a = r.uniform(), b = c.u(any); if (!same_bits(a, b)) ok = false; }
    CHECK(ok); CHECK(c.g.count == r.count);
  }
  CHECK(compat_stream(R_PILOT, 0, 0) == 0); CHECK(compat_stream(R_DIAG, 0, 4) == 4); CHECK(compat_stream(R_PILOT, 1, 0) == 5);
  CHECK(compat_stream(R_DIAG, 1, 1) == 6); CHECK(compat_stream(R_FINAL, 0, 1) == 10); CHECK(compat_stream(R_FINAL, 0, 4) == 13);
  CHECK_THROWS(compat_stream(R_FINAL, 0, 5));
}
