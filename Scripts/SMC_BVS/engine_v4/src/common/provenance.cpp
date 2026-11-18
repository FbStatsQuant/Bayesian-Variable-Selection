// provenance.cpp -- binary block, libm guard, manifest input check.
#include "v4/provenance.h"
#include <cstdio>
#include "v4/format.h"
#include "v4/pmath.h"
#include "v4/sha256.h"
#include "v4/status.h"

#include "v4_git.h"   // generated at build time: V4_GIT_COMMIT = git rev-parse HEAD + "-dirty" if tracked files changed

#ifndef V4_ISLAND_ISA_STR
#define V4_ISLAND_ISA_STR ""
#endif
extern "C" int v4_class_a_fma() __attribute__((weak));   // island_a.cpp (D-32)

namespace v4 {

static Json make_block(bool with_self_test) {
  {
    Json j = Json::object();
    try { j["sha256"] = sha256_file("/proc/self/exe"); } catch (...) { j["sha256"] = "unreadable"; }
    j["git_commit"] = V4_GIT_COMMIT;
    j["compiler"] = std::string("g++ ") + __VERSION__;
    j["flags"] = V4_BIT_FLAGS_STR;
    // D-32 (WP7 O5; review PR55 m4): island_fma = whether class A uses a true FMA in this binary (from the class-A
    // translation unit itself; the family of every class-A bit), island_isa = the -march of the island sources (cmake
    // -DV4_ISLAND_ISA), or "x86-64-v3" for a V4_WIDE_ISA class-A build without one, else "portable"
    const bool has_fma = v4_class_a_fma && v4_class_a_fma() != 0;
    if (v4_class_a_fma) j["island_fma"] = has_fma;
    j["island_isa"] = !std::string(V4_ISLAND_ISA_STR).empty() ? std::string(V4_ISLAND_ISA_STR) : (has_fma ? std::string("x86-64-v3") : std::string("portable"));
    auto li = pm::libm_info();
    Json l = Json::object();
    l["path"] = li.path; l["sha256"] = li.sha256; l["glibc"] = li.gnu_libc_version; l["fma_variant"] = li.fma_variant;
    l["binding"] = pm::binding();
    if (with_self_test) {
      const pm::SelfTest st = pm::self_test();
      Json t = Json::object(); t["pass"] = st.ok;
      for (auto& r : st.rows) t[r.fn] = r.ok;
      l["self_test"] = t;
    } else {
      l["self_test"] = "not run";
    }
    j["libm"] = l;
    return j;
  }
}
const Json& binary_block() { static const Json b = make_block(true); return b; }
const Json& binary_block_no_self_test() { static const Json b = make_block(false); return b; }

static std::string field(const Json& b, const char* k) {
  return b.contains(k) && b.at(k).type() == Json::STR ? b.at(k).str() : std::string();
}
static bool self_test_pass(const Json& b) {
  if (!b.contains("libm")) return false;
  const Json& l = b.at("libm");
  return l.contains("self_test") && l.at("self_test").type() == Json::OBJ && l.at("self_test").contains("pass") &&
         l.at("self_test").at("pass").type() == Json::BOOL && l.at("self_test").at("pass").boolean();
}
// D-32 (2): one fit = one FMA family. Class A uses a true FMA in every FMA build and a*b + c without one
// (island/amath.h fma8), so blocks of the two families carry different class-A bits. The family is island_fma when
// the block has it (the class-A unit's own answer), else known island_isa names; an unknown family is not refused.
static int fma_family(const Json& blk) {   // 1 FMA, 0 no FMA, -1 unknown
  if (blk.contains("island_fma") && blk.at("island_fma").type() == Json::BOOL) return blk.at("island_fma").boolean() ? 1 : 0;
  const std::string isa = field(blk, "island_isa");
  if (isa == "portable" || isa == "x86-64" || isa == "x86-64-v2") return 0;
  static const char* fma_names[] = {"x86-64-v3", "x86-64-v4", "sapphirerapids", "icelake-server", "cascadelake", "skylake-avx512",
                                    "haswell", "broadwell", "skylake", "znver2", "znver3", "znver4"};
  for (const char* n : fma_names) if (isa == n) return 1;
  return -1;
}
BinaryCheck isa_family_compatible(const Json& a, const Json& b) {
  const int fa = fma_family(a), fb = fma_family(b);
  if (fa >= 0 && fb >= 0 && fa != fb)
    return {false, "island ISA families differ (" + field(a, "island_isa") + " vs " + field(b, "island_isa") + "): class-A bits differ (D-32)"};
  return {true, "ok"};
}
BinaryCheck binary_compatible(const Json& a, const Json& b, BinaryUse use) {
  auto no = [](const std::string& why) { return BinaryCheck{false, why}; };
  if (!self_test_pass(a) || !self_test_pass(b)) return no("libm self-test not passed in both binary blocks");
  if (field(a, "flags") != field(b, "flags")) return no("compiler flags differ");
  if (!a.contains("libm") || !b.contains("libm") || a.at("libm").at("binding").str() != b.at("libm").at("binding").str())
    return no("libm binding differs");
  const std::string ga = field(a, "git_commit"), gb = field(b, "git_commit");
  auto unusable = [](const std::string& g) { return g.empty() || g == "unknown" || g.find("-dirty") != std::string::npos; };
  switch (use) {
    case BinaryUse::MergeV:
      return isa_family_compatible(a, b);
    case BinaryUse::MergeTheory:
      if (unusable(ga) || unusable(gb)) return no("theory mode needs a clean, known git commit (got '" + ga + "', '" + gb + "')");
      if (ga != gb) return no("git commits differ ('" + ga + "' vs '" + gb + "')");
      return {true, "ok"};
    case BinaryUse::Restart:
      if (field(a, "sha256").empty() || field(a, "sha256") != field(b, "sha256")) return no("executable differs from the one that wrote the checkpoint");
      if (ga != gb) return no("git commits differ ('" + ga + "' vs '" + gb + "')");
      return {true, "ok"};
  }
  return no("unknown use");
}
void require_binary_compatible(const Json& a, const Json& b, BinaryUse use) {
  BinaryCheck c = binary_compatible(a, b, use);
  if (!c.ok) throw Error(Status::invalid_input, "binary blocks incompatible: " + c.reason);
}

void require_bit_libm() {
  const pm::SelfTest& st = pm::self_test();
  if (!st.ok) {
    std::string bad;
    for (auto& r : st.rows) if (!r.ok) bad += std::string(bad.empty() ? "" : ", ") + r.fn;
    throw Error(Status::invalid_input, "libm self-test failed for " + bad + ": bit-form results would differ from the reference "
                                       "(Owls = NOTS) bits (INTERFACES §6)");
  }
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
