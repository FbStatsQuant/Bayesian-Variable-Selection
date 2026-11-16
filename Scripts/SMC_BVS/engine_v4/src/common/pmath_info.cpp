// pmath_info.cpp -- which libm the pinned functions resolve to (path + SHA-256 for the manifest).
#include <dlfcn.h>
#include <gnu/libc-version.h>
#include <link.h>
#include <cmath>
#include <cstdlib>
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
  // the loaded shared object whose name contains "libm.so" (the one log() resolves to in a dynamic build)
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
}  // namespace v4::pm
