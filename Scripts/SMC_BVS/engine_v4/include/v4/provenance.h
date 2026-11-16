// provenance.h -- the binary block written into every record and every file's meta (INTERFACES §5.3, §6), the libm
// guard, and the manifest input check.
#pragma once
#include <string>
#include "v4/json.h"

namespace v4 {
// {sha256 of /proc/self/exe, git_commit (at configure time), compiler, flags, libm {path, sha256, glibc, fma_variant}}.
// Computed once per process.
const Json& binary_block();
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
