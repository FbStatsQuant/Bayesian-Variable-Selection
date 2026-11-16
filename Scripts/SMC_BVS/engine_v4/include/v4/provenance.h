// provenance.h -- the binary block written into every record and every file's meta (INTERFACES §5.3, §6), the libm
// guard, and the manifest input check.
#pragma once
#include <string>
#include "v4/json.h"

namespace v4 {
// {sha256 of /proc/self/exe, git_commit (at configure time), compiler, flags, libm {path, sha256, glibc, fma_variant}}.
// Computed once per process.
const Json& binary_block();
// Throws Error(invalid_input) unless the FMA/AVX2 libm variant is in use (INTERFACES §6). Called by every command
// except info / version.
void require_fma_variant();
// INTERFACES §5.3: manifest "inputs" = {path: content sha256}. Throws Error(invalid_input) on any mismatch.
void verify_inputs(const Json& manifest);
// u64 values go into JSON as hex strings "0x..." (JSON numbers are doubles).
std::string hex64(uint64_t x);
}  // namespace v4
