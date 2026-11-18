// amath.h -- 8-lane double vectors (GCC vector extensions) and the class-A vector log / exp.
//
// One lane type for every kernel path: the batched label-major kernel and the one-label particle-major reference both
// call the same 8-lane functions (the reference fills all lanes with its label), so the two kernels produce the same
// bits in both arithmetic forms (T3) by construction, whatever the ISA of the build.
//  - Bit form uses only IEEE +, -, *, /, sqrt (exact per lane at any vector width, no contraction under
//    -ffp-contract=off) and scalar pm::log / pm::exp per lane: the bits of core/cpp/v3_score.h.
//  - Class A additionally uses fma8 (a true fused multiply-add when the build has FMA, else a*b + c) and the vector
//    log / exp below (fdlibm e_log.c / e_exp.c algorithms, < 1 ulp; rounding differs from glibc: class A).
#pragma once
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <new>
#include <vector>
#if defined(__AVX512F__) || defined(__FMA__)
#include <immintrin.h>
#endif

#if defined(__AVX512F__)
#define V4_ISLAND_ISA_NS isa_avx512
#elif defined(__FMA__)
#define V4_ISLAND_ISA_NS isa_fma
#else
#define V4_ISLAND_ISA_NS isa_base
#endif
namespace v4::island {
inline namespace V4_ISLAND_ISA_NS {

typedef double v8d __attribute__((vector_size(64)));   // natural alignment 64
typedef int64_t v8l __attribute__((vector_size(64)));   // natural alignment 64
typedef uint64_t v8u __attribute__((vector_size(64)));   // natural alignment 64

// 64-byte aligned allocator: the tile, product and gathered-column buffers are read with 64-byte vector loads, which
// cost about twice as much when they straddle cache lines (measured: 0.166 vs 0.085 ns per product multiply-add).
template <class T> struct Aligned64 {
  using value_type = T;
  Aligned64() = default;
  template <class U> Aligned64(const Aligned64<U>&) {}
  T* allocate(size_t n) { void* p = std::aligned_alloc(64, ((n * sizeof(T) + 63) / 64) * 64); if (!p) throw std::bad_alloc(); return (T*)p; }
  void deallocate(T* p, size_t) { std::free(p); }
  template <class U> bool operator==(const Aligned64<U>&) const { return true; }
  template <class U> bool operator!=(const Aligned64<U>&) const { return false; }
};
template <class T> using avec = std::vector<T, Aligned64<T>>;

inline v8d bc(double x) { return v8d{x, x, x, x, x, x, x, x}; }
inline v8d load8(const double* p) { v8d v; std::memcpy(&v, p, 64); return v; }
inline void store8(double* p, v8d v) { std::memcpy(p, &v, 64); }
inline v8d sqrt8(v8d x) { v8d r; for (int l = 0; l < 8; ++l) r[l] = std::sqrt(x[l]); return r; }
inline unsigned lanemask(v8l m) { unsigned r = 0; for (int l = 0; l < 8; ++l) r |= (unsigned)(m[l] != 0) << l; return r; }
inline bool any8(v8l m) { int64_t a = 0; for (int l = 0; l < 8; ++l) a |= m[l]; return a != 0; }
// bitmask of lanes with x > 0 and finite (the pivot test of core/cpp/v3_score.h:80); NaN fails both compares
inline unsigned pos_finite_mask(v8d x) { return lanemask((x > bc(0.0)) & (x < bc(__builtin_inf()))); }

inline v8d fma8(v8d a, v8d b, v8d c) {
#if defined(__AVX512F__)
  return (v8d)_mm512_fmadd_pd((__m512d)a, (__m512d)b, (__m512d)c);
#elif defined(__FMA__)
  __m256d lo = _mm256_fmadd_pd(_mm256_set_pd(a[3], a[2], a[1], a[0]), _mm256_set_pd(b[3], b[2], b[1], b[0]), _mm256_set_pd(c[3], c[2], c[1], c[0]));
  __m256d hi = _mm256_fmadd_pd(_mm256_set_pd(a[7], a[6], a[5], a[4]), _mm256_set_pd(b[7], b[6], b[5], b[4]), _mm256_set_pd(c[7], c[6], c[5], c[4]));
  v8d r; std::memcpy(&r, &lo, 32); std::memcpy((char*)&r + 32, &hi, 32); return r;
#else
  return a * b + c;
#endif
}
inline v8d fnma8(v8d a, v8d b, v8d c) { return fma8(-a, b, c); }   // c - a*b
inline constexpr bool kHasFMA() {
#if defined(__AVX512F__) || defined(__FMA__)
  return true;
#else
  return false;
#endif
}

// Philox4x32-10 (v4::philox4x32_10, rng.h) for 8 counters that differ only in word 1 (the position): the uniforms of
// one particle at 8 positions. Same words, same bits as uniform_at (tested lane by lane).
// Philox4x32-10 (v4::philox4x32_10, rng.h) for 8 counters that differ only in one word (`word`: 0 = slot, 1 = position):
// e.g. one particle's uniforms at 8 positions, or 8 slots of one step. Same words, same bits as uniform_at (tested).
inline void philox8_word(const uint32_t ctr[4], const uint32_t key[2], int word, const uint32_t vals[8], double out[8]) {
  const v8u M = {0xFFFFFFFFull, 0xFFFFFFFFull, 0xFFFFFFFFull, 0xFFFFFFFFull, 0xFFFFFFFFull, 0xFFFFFFFFull, 0xFFFFFFFFull, 0xFFFFFFFFull};
  v8u c0, c1, c2, c3;
  for (int l = 0; l < 8; ++l) { c0[l] = ctr[0]; c1[l] = ctr[1]; c2[l] = ctr[2]; c3[l] = ctr[3]; }
  if (word == 0) for (int l = 0; l < 8; ++l) c0[l] = vals[l]; else for (int l = 0; l < 8; ++l) c1[l] = vals[l];
  uint32_t k0 = key[0], k1 = key[1];
  for (int r = 0; r < 10; ++r) {
    if (r) { k0 += 0x9E3779B9u; k1 += 0xBB67AE85u; }
#if defined(__AVX512F__)
    // K2 (WP3_ARCH_REVIEW §2 lever 4): the lanes hold 32-bit values, so the 32 x 32 -> 64 unsigned multiply of the low
    // halves (vpmuludq: 1 uop, latency 5) gives the products of the 64-bit lane multiply the generic expression compiles
    // to with AVX-512DQ (vpmullq: 3 uops, latency 15). Same bits (philox_known_answers / uniform_at lane tests).
    v8u p0 = (v8u)_mm512_mul_epu32((__m512i)c0, _mm512_set1_epi64(0xD2511F53ll)), p1 = (v8u)_mm512_mul_epu32((__m512i)c2, _mm512_set1_epi64(0xCD9E8D57ll));
#else
    v8u p0 = c0 * 0xD2511F53ull, p1 = c2 * 0xCD9E8D57ull;     // 32 x 32 -> 64 (lanes hold 32-bit values)
#endif
    v8u n0 = (p1 >> 32) ^ c1 ^ (uint64_t)k0, n2 = (p0 >> 32) ^ c3 ^ (uint64_t)k1;
    c1 = p1 & M; c3 = p0 & M; c0 = n0; c2 = n2;
  }
  v8u w = ((c1 << 32) | c0) >> 11;
  v8d u = __builtin_convertvector(w, v8d) * 0x1.0p-53;
  store8(out, u);
}
inline void philox8_positions(const uint32_t ctr[4], const uint32_t key[2], const uint32_t pos[8], double out[8]) {
  philox8_word(ctr, key, 1, pos, out);
}

inline v8d select8(v8l mask, v8d a, v8d b) { return (v8d)(((v8l)a & mask) | ((v8l)b & ~mask)); }

// log(x) for normal positive finite x (fdlibm e_log.c). Other lanes: scalar std::log (rare; class A).
inline v8d alog8(v8d x) {
  const double ln2_hi = 6.93147180369123816490e-01, ln2_lo = 1.90821492927058770002e-10;
  const double Lg1 = 6.666666666666735130e-01, Lg2 = 3.999999999940941908e-01, Lg3 = 2.857142874366239149e-01,
               Lg4 = 2.222219843214978396e-01, Lg5 = 1.818357216161805012e-01, Lg6 = 1.531383769920937332e-01,
               Lg7 = 1.479819860511658591e-01;
  v8l bits = (v8l)x;
  v8l e = ((bits >> 52) & 0x7FF) - 1023;
  v8l mb = (bits & 0x000FFFFFFFFFFFFFLL) | 0x3FF0000000000000LL;   // m in [1, 2)
  v8d m = (v8d)mb;
  v8l big = m > bc(1.4142135623730950488);
  m = select8(big, m * bc(0.5), m);
  e = e + (big & 1);
  v8d f = m - bc(1.0);
  v8d s = f / (bc(2.0) + f);
  v8d z = s * s, w = z * z;
  v8d t1 = w * fma8(w, fma8(w, bc(Lg6), bc(Lg4)), bc(Lg2));
  v8d t2 = z * fma8(w, fma8(w, fma8(w, bc(Lg7), bc(Lg5)), bc(Lg3)), bc(Lg1));
  v8d R = t2 + t1;
  v8d hfsq = bc(0.5) * f * f;
  v8d dk = __builtin_convertvector(e, v8d);
  v8d r = dk * bc(ln2_hi) - ((hfsq - (s * (hfsq + R) + dk * bc(ln2_lo))) - f);
  v8l ex = (bits >> 52) & 0x7FF;
  v8l special = (bits <= 0) | (ex == 0) | (ex == 0x7FF);   // zero, negative, subnormal, inf, NaN: scalar (rare)
  if (any8(special)) for (int l = 0; l < 8; ++l) if (special[l]) r[l] = std::log(x[l]);
  return r;
}
// exp(x) (fdlibm e_exp.c reduction and polynomial); x > 709.7 -> +inf, x < -745.2 -> 0, NaN -> NaN (scalar lanes).
inline v8d aexp8(v8d x) {
  const double ln2_hi = 6.93147180369123816490e-01, ln2_lo = 1.90821492927058770002e-10, inv_ln2 = 1.44269504088896338700e+00;
  const double P1 = 1.66666666666666019037e-01, P2 = -2.77777777770155933842e-03, P3 = 6.61375632143793436117e-05,
               P4 = -1.65339022054652515390e-06, P5 = 4.13813679705723846039e-08;
  v8l special = ~(x > bc(-745.0)) | (x > bc(709.0));          // underflow, overflow, NaN: scalar (rare)
  v8d xc = select8(special, bc(0.0), x);
  const double shifter = 0x1.8p52;
  v8d kd = (xc * bc(inv_ln2) + bc(shifter)) - bc(shifter);           // round to nearest
  v8d hi = xc - kd * bc(ln2_hi);
  v8d lo = kd * bc(ln2_lo);
  v8d r = hi - lo;
  v8d t = r * r;
  v8d c = r - t * fma8(t, fma8(t, fma8(t, fma8(t, bc(P5), bc(P4)), bc(P3)), bc(P2)), bc(P1));
  v8d y = bc(1.0) - ((lo - (r * c) / (bc(2.0) - c)) - hi);
  v8l k = __builtin_convertvector(kd, v8l);
  v8l k1 = k >> 1, k2 = k - k1;                                      // two factors keep 2^k normal down to -1074
  v8d s1 = (v8d)((k1 + 1023) << 52), s2 = (v8d)((k2 + 1023) << 52);
  v8d res = (y * s1) * s2;
  if (any8(special)) for (int l = 0; l < 8; ++l) if (special[l]) res[l] = std::exp(x[l]);
  return res;
}

}  // namespace V4_ISLAND_ISA_NS
}  // namespace v4::island
