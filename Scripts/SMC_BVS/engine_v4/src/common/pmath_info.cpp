// pmath_info.cpp -- which libm the pinned functions resolve to (path + SHA-256), and the bit-form self-test.
#include <dlfcn.h>
#include <gnu/libc-version.h>
#include <link.h>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <random>
#include <string>
#include "v4/pmath.h"
#include "v4/sha256.h"

namespace v4::pm {
bool fma_variant_expected() {
  if (!__builtin_cpu_supports("fma") || !__builtin_cpu_supports("avx2")) return false;
  const char* t = std::getenv("GLIBC_TUNABLES");
  if (t) { std::string s(t); if (s.find("-FMA") != std::string::npos || s.find("-AVX2") != std::string::npos) return false; }
  return true;
}
LibmInfo libm_info() {
  LibmInfo r;
  r.gnu_libc_version = gnu_get_libc_version();
  dl_iterate_phdr([](struct dl_phdr_info* info, size_t, void* data) -> int {
    std::string nm = info->dlpi_name ? info->dlpi_name : "";
    if (nm.find("/libm.so") != std::string::npos || nm.rfind("libm.so", 0) == 0) { *(std::string*)data = nm; return 1; }
    return 0;
  }, &r.path);
  if (!r.path.empty()) { try { r.sha256 = sha256_file(r.path); } catch (...) { r.sha256 = "unreadable"; } }
  else r.path = "static-or-unknown";
  r.fma_variant = fma_variant_expected();
  return r;
}

// Argument rows of tools/pmath_check.cpp (generator mt19937_64(12345), one fresh generator per row).
struct Row { const char* name; double lo, hi; bool logscale, integer; };
static const Row ROWS[] = {
  {"log", 1e-300, 1e12, true, false}, {"log_near1", 0.5, 2.0, false, false}, {"exp", -745, 0, false, false},
  {"exp_pos", 0, 700, false, false}, {"log1p", -0.999, 1e3, false, false}, {"log1p_small", 1e-300, 1e-3, true, false},
  {"expm1", -40, 1, false, false}, {"lgamma", 1e-3, 3e6, true, false}, {"lgamma_int", 1, 3e6, false, true}};
std::vector<double> check_arguments(const std::string& name, size_t n) {
  for (const Row& r : ROWS) {
    if (name != r.name) continue;
    std::mt19937_64 g(12345); std::vector<double> x(n);
    for (size_t i = 0; i < n; ++i) {
      double u = (double)(g() >> 11) * 0x1.0p-53;
      x[i] = r.logscale ? pm::exp(pm::log(r.lo) + u * (pm::log(r.hi) - pm::log(r.lo))) : r.lo + u * (r.hi - r.lo);
      if (r.integer) x[i] = std::floor(x[i]);
    }
    return x;
  }
  return {};
}

std::vector<long double> check_arguments_l(const std::string& name, size_t n) {
  std::mt19937_64 g(12345); std::vector<long double> x(n);
  if (name == "expl") {
    for (size_t i = 0; i < n; ++i) { double u = (double)(g() >> 11) * 0x1.0p-53; x[i] = (long double)(-11000.0 + u * 11000.0); }
  } else if (name == "logl") {
    for (size_t i = 0; i < n; ++i) x[i] = 1.0L + (long double)g() * 0x1.0p-64L * 1000.0L;
  } else return {};
  return x;
}
std::string sha256_ld(const std::vector<long double>& y) {
  Sha256 s;
  for (long double v : y) { unsigned char b[sizeof(long double)]; std::memcpy(b, &v, sizeof v); s.update(b, 10); }
  return hex(s.final());
}

// SHA-256 of the 2·10^6 results per row: the values measured on Owls (tests/fixtures/pmath_owls_glibc234_fma.json) and
// measured equal on NOTS (results/PMATH_NOTS.md, job 2747666). log1p / expm1 rows are not part of the guard (class A).
// expl / logl (x87, v0.1.4): Owls values; the NOTS comparison is pending (fails closed on a difference).
static const struct { const char* fn; const char* sha; } REF[] = {
  {"log", "164995feb48757a32cd1743916481ea7aad73c777c0b516cf5342b7a8399f10c"}, {"log_near1", "be4025e3d956faace7d3bbd5dda696268d53fd0b9ae2ce04992a5f52065d9c98"}, {"exp", "9c68e5b42ddc2763d0f039b7675098fb4c2e95ead26cb30ef2ee647cb375b673"}, {"exp_pos", "f24a4667ec96665b03b36aa0d5ff1a620f3802945603bed0943a573b792ed51f"},
  {"lgamma", "2e128c4aca69a2d64762dd560db3fd3bbfcebdc57a4e2ed295ce527a74a02c2c"}, {"lgamma_int", "3eff706a7b26e8e59c4f8ac0cbdaf21d462c24a1cad0f1081a275ec970f7cf85"},
  {"expl", "90880997dcef54b6acc1a111130e48b3b675aea3ab01b106aabe0de40bff888b"}, {"logl", "475c11284bfe560a27d9a71af19691da7d616bad52ac13afa30efb3d1bcd4f38"}};

static constexpr size_t SELF_TEST_N = 2000000;
SelfTest self_test() {
  static const SelfTest st = [] {
    SelfTest s;
    for (auto& r : REF) {
      std::string h;
      if (std::strcmp(r.fn, "expl") == 0 || std::strcmp(r.fn, "logl") == 0) {
        std::vector<long double> x = check_arguments_l(r.fn, SELF_TEST_N), y(x.size());
        bool is_log = r.fn[0] == 'l';
        for (size_t i = 0; i < x.size(); ++i) y[i] = is_log ? pm::logl(x[i]) : pm::expl(x[i]);
        h = sha256_ld(y);
      } else {
        std::vector<double> x = check_arguments(r.fn, SELF_TEST_N), y(x.size());
        bool is_log = std::strncmp(r.fn, "log", 3) == 0, is_exp = std::strncmp(r.fn, "exp", 3) == 0;
        for (size_t i = 0; i < x.size(); ++i) y[i] = is_log ? pm::log(x[i]) : is_exp ? pm::exp(x[i]) : pm::lgamma(x[i]);
        h = hex(sha256(y.data(), y.size() * 8));
      }
      bool ok = h == r.sha;
      s.rows.push_back({r.fn, h, ok});
      s.ok = s.ok && ok;
    }
    return s;
  }();
  return st;
}
}  // namespace v4::pm
