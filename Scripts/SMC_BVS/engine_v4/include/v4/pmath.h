// pmath.h -- the pinned transcendental functions (INTERFACES §6; ENGINEERING_SPEC §3; review §4.9).
// All engine code calls v4::pm::*, never std:: directly, so the binding can be changed in one place.
// Binding v0.1 (WP1 decision, see tests/PMATH_REPORT.md): glibc libm (2.34 on Owls and NOTS), called through the
// same std:: overloads core/ uses, compiled with the bit flags. pm::binding() reports it; pmath_info gives the libm
// path and hash for the manifest.
#pragma once
#include <cmath>
#include <string>

namespace v4::pm {
inline double log(double x) { return std::log(x); }
inline double exp(double x) { return std::exp(x); }
inline double log1p(double x) { return std::log1p(x); }
inline double expm1(double x) { return std::expm1(x); }
inline double lgamma(double x) { return std::lgamma(x); }
inline double sqrt(double x) { return std::sqrt(x); }   // IEEE correctly rounded: not a pinning issue
inline long double logl(long double x) { return std::log(x); }
inline long double expl(long double x) { return std::exp(x); }
inline const char* binding() { return "glibc-libm"; }
struct LibmInfo { std::string path, sha256, gnu_libc_version; };
LibmInfo libm_info();   // path of the loaded libm.so.6, its SHA-256, gnu_get_libc_version()
}  // namespace v4::pm
