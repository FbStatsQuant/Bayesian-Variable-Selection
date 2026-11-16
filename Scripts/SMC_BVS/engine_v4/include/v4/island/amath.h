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
#include <cstring>
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

typedef double v8d __attribute__((vector_size(64), aligned(64)));
typedef int64_t v8l __attribute__((vector_size(64), aligned(64)));
typedef uint64_t v8u __attribute__((vector_size(64), aligned(64)));

inline v8d bc(double x) { return v8d{x, x, x, x, x, x, x, x}; }
inline v8d load8(const double* p) { v8d v; std::memcpy(&v, p, 64); return v; }
inline void store8(double* p, v8d v) { std::memcpy(p, &v, 64); }
inline v8d sqrt8(v8d x) { v8d r; for (int l = 0; l < 8; ++l) r[l] = std::sqrt(x[l]); return r; }
// bitmask of lanes with x > 0 and finite (the pivot test of core/cpp/v3_score.h:80)
inline unsigned pos_finite_mask(v8d x) {
  unsigned m = 0; for (int l = 0; l < 8; ++l) m |= (unsigned)((x[l] > 0) && std::isfinite(x[l])) << l; return m;
}

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
  for (int l = 0; l < 8; ++l) {
    uint64_t ex = ((uint64_t)bits[l] >> 52) & 0x7FF;
    if (bits[l] <= 0 || ex == 0 || ex == 0x7FF) r[l] = std::log(x[l]);
  }
  return r;
}
// exp(x) (fdlibm e_exp.c reduction and polynomial); x > 709.7 -> +inf, x < -745.2 -> 0, NaN -> NaN (scalar lanes).
inline v8d aexp8(v8d x) {
  const double ln2_hi = 6.93147180369123816490e-01, ln2_lo = 1.90821492927058770002e-10, inv_ln2 = 1.44269504088896338700e+00;
  const double P1 = 1.66666666666666019037e-01, P2 = -2.77777777770155933842e-03, P3 = 6.61375632143793436117e-05,
               P4 = -1.65339022054652515390e-06, P5 = 4.13813679705723846039e-08;
  v8d xc = x;
  for (int l = 0; l < 8; ++l) { if (!(xc[l] > -745.0)) xc[l] = -745.0; if (xc[l] > 709.0) xc[l] = 709.0; }
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
  for (int l = 0; l < 8; ++l) {
    if (!(x[l] > -745.0) || x[l] > 709.0) res[l] = std::exp(x[l]);
  }
  return res;
}

}  // namespace V4_ISLAND_ISA_NS
}  // namespace v4::island
