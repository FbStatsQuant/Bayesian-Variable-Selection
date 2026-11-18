// sha256.h -- bundled SHA-256 (FIPS 180-4), for section and file hashes (INTERFACES §5.1). No external dependency.
#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <string>

namespace v4 {
struct Sha256 {
  uint32_t h[8]; uint64_t len = 0; uint8_t buf[64]; size_t nbuf = 0;
  Sha256();
  void update(const void* data, size_t n);
  std::array<uint8_t, 32> final();
};
std::array<uint8_t, 32> sha256(const void* data, size_t n);
std::string hex(const uint8_t* d, size_t n);
inline std::string hex(const std::array<uint8_t, 32>& d) { return hex(d.data(), 32); }
std::string sha256_file(const std::string& path);   // hex digest of a whole file (manifest: binary, libm)
}  // namespace v4
