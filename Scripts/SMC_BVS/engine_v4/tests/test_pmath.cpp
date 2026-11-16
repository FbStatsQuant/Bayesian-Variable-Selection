#include <cmath>
#include "tk.h"
#include "v4/pmath.h"
using namespace v4;

TEST(pmath_binding_is_libm) {
  auto li = pm::libm_info();
  std::printf("    libm: %s sha256 %s glibc %s binding %s\n", li.path.c_str(), li.sha256.c_str(), li.gnu_libc_version.c_str(), pm::binding());
  CHECK(!li.path.empty());
  double xs[] = {1e-300, 0.1, 0.5, 1, 2, 3.5, 100, 1e10};
  bool ok = true;
  for (double x : xs) ok = ok && same_bits(pm::log(x), std::log(x)) && same_bits(pm::exp(-x), std::exp(-x)) && same_bits(pm::lgamma(x), std::lgamma(x)) &&
                      same_bits(pm::log1p(x), std::log1p(x)) && same_bits(pm::expm1(-x), std::expm1(-x));
  CHECK(ok);
}
