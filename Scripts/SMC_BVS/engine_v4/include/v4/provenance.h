// provenance.h -- the binary block written into every record and every file's meta (INTERFACES §5.3, §6), the libm
// guard, and the manifest input check.
#pragma once
#include <string>
#include "v4/json.h"

namespace v4 {
// {sha256 of /proc/self/exe, git_commit (40-hex HEAD + "-dirty" when tracked files changed; refreshed at every build), compiler,
// flags, libm {path, sha256, glibc, fma_variant, binding, self_test}}. Computed once per process.
const Json& binary_block();
const Json& binary_block_no_self_test();   // the same with self_test = "not run" (info only)

// INTERFACES §5.1 binary consistency (v0.1.4), one rule for every caller:
//   MergeV      (merge, V mode)        both self-tests passed; flags and libm binding equal;
//   MergeTheory (merge, compat / law)  the same, plus git commits equal, clean (no "-dirty") and known;
//   Restart     (checkpoint restart)   the same as MergeV, plus the same executable (sha256) and git commit.
enum class BinaryUse { MergeV, MergeTheory, Restart };
struct BinaryCheck { bool ok; std::string reason; };
BinaryCheck binary_compatible(const Json& a, const Json& b, BinaryUse use);
void require_binary_compatible(const Json& a, const Json& b, BinaryUse use);   // throws Error(invalid_input)
// INTERFACES §6 (v0.1.3): throws Error(invalid_input) unless pm::self_test() passes, i.e. log / exp / lgamma return the
// measured reference bits (Owls = NOTS). Keys on function results, not on the libm file hash. Called by every command
// except info / version.
void require_bit_libm();
inline void require_fma_variant() { require_bit_libm(); }   // v0.1.2 name, kept as an alias
// INTERFACES §5.3: manifest "inputs" = {path: content sha256}. Throws Error(invalid_input) on any mismatch.
void verify_inputs(const Json& manifest);
// u64 values go into JSON as hex strings "0x..." (JSON numbers are doubles).
std::string hex64(uint64_t x);
}  // namespace v4
