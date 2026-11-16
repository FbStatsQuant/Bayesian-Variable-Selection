// provenance.cpp -- binary block, libm guard, manifest input check.
#include "v4/provenance.h"
#include <cstdio>
#include "v4/format.h"
#include "v4/pmath.h"
#include "v4/sha256.h"
#include "v4/status.h"

#ifndef V4_GIT_COMMIT
#define V4_GIT_COMMIT "unknown"
#endif

namespace v4 {

const Json& binary_block() {
  static const Json b = [] {
    Json j = Json::object();
    try { j["sha256"] = sha256_file("/proc/self/exe"); } catch (...) { j["sha256"] = "unreadable"; }
    j["git_commit"] = V4_GIT_COMMIT;
    j["compiler"] = std::string("g++ ") + __VERSION__;
    j["flags"] = V4_BIT_FLAGS_STR;
    auto li = pm::libm_info();
    Json l = Json::object();
    l["path"] = li.path; l["sha256"] = li.sha256; l["glibc"] = li.gnu_libc_version; l["fma_variant"] = li.fma_variant;
    l["binding"] = pm::binding();
    j["libm"] = l;
    return j;
  }();
  return b;
}

void require_fma_variant() {
  if (!pm::fma_variant_expected())
    throw Error(Status::invalid_input, "libm FMA/AVX2 variant not available or masked (GLIBC_TUNABLES): bit-form results "
                                       "would differ from the v3.1 records (INTERFACES §6)");
}

void verify_inputs(const Json& manifest) {
  if (!manifest.contains("inputs")) return;
  for (auto& [path, h] : manifest.at("inputs").items()) {
    fmt::Reader rd(path);
    if (rd.content_hash() != h.str()) throw Error(Status::invalid_input, "input hash mismatch: " + path);
  }
}

std::string hex64(uint64_t x) { char b[24]; std::snprintf(b, sizeof b, "0x%016llx", (unsigned long long)x); return b; }

}  // namespace v4
