// wp1_format_shim.h -- TEMPORARY stand-in for WP1's format.h + src/common/sha256.cpp (INTERFACES v0.1 §5.1).
// Container: FileHeader (128 B) | SectionEntry[n] (128 B each) | sections at 64-byte aligned offsets; little-endian;
// written to <name>.tmp.<pid>, fsync'd, renamed; the reader verifies every hash. Replaced by WP1's header when it lands.
#pragma once
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <fcntl.h>
#include <unistd.h>
#include "wp1_shim.h"

namespace v4::fmt {

// ---- SHA-256 (FIPS 180-4), small portable implementation ----
struct Sha256 {
  uint32_t h[8]; uint64_t bits = 0; uint8_t buf[64]; size_t nb = 0;
  Sha256() { static const uint32_t h0[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19}; std::memcpy(h, h0, sizeof h); }
  static uint32_t rotr(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }
  void block(const uint8_t* p) {
    static const uint32_t k[64] = {
      0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
      0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
      0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
      0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
      0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
      0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};
    uint32_t w[64];
    for (int i = 0; i < 16; ++i) w[i] = (uint32_t)p[4 * i] << 24 | (uint32_t)p[4 * i + 1] << 16 | (uint32_t)p[4 * i + 2] << 8 | p[4 * i + 3];
    for (int i = 16; i < 64; ++i) {
      uint32_t s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >> 3), s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >> 10);
      w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }
    uint32_t a = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], hh = h[7];
    for (int i = 0; i < 64; ++i) {
      uint32_t t1 = hh + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) + ((e & f) ^ (~e & g)) + k[i] + w[i];
      uint32_t t2 = (rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c));
      hh = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
    }
    h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += hh;
  }
  void update(const void* data, size_t len) {
    const uint8_t* p = (const uint8_t*)data; bits += (uint64_t)len * 8;
    while (len) { size_t t = std::min(len, 64 - nb); std::memcpy(buf + nb, p, t); nb += t; p += t; len -= t; if (nb == 64) { block(buf); nb = 0; } }
  }
  void final(uint8_t out[32]) {
    uint64_t b = bits; uint8_t pad = 0x80; update(&pad, 1); uint8_t z = 0; while (nb != 56) update(&z, 1);
    uint8_t L[8]; for (int i = 0; i < 8; ++i) L[i] = (uint8_t)(b >> (56 - 8 * i)); update(L, 8);
    for (int i = 0; i < 8; ++i) { out[4 * i] = h[i] >> 24; out[4 * i + 1] = h[i] >> 16; out[4 * i + 2] = h[i] >> 8; out[4 * i + 3] = h[i]; }
  }
};
inline void sha256(const void* d, size_t n, uint8_t out[32]) { Sha256 s; s.update(d, n); s.final(out); }
inline std::string hex(const uint8_t* d, size_t n) { static const char* x = "0123456789abcdef"; std::string s; for (size_t i = 0; i < n; ++i) { s += x[d[i] >> 4]; s += x[d[i] & 15]; } return s; }

enum DType : uint32_t { F64 = 1, I32 = 2, U32 = 3, I64 = 4, U64 = 5, U8 = 6, U16 = 7, F32 = 8, JSON = 9 };
struct FileHeader { char magic[8]; uint32_t format_version, kind, mode, n_sections; uint64_t file_bytes; uint8_t table_sha256[32]; uint8_t reserved[64]; };
// NOTE: the fields of INTERFACES v0.1 §5.1 sum to 120 bytes; padded with reserved[8] to the stated 128 (raised with WP1).
struct SectionEntry { char name[48]; uint32_t dtype, ndim; uint64_t dims[2]; uint64_t offset, length; uint8_t sha256[32]; uint8_t reserved[8]; };
static_assert(sizeof(FileHeader) == 128, "FileHeader is 128 bytes");
static_assert(sizeof(SectionEntry) == 128, "SectionEntry is 128 bytes");

struct Writer {
  struct Sec { SectionEntry e; std::vector<uint8_t> bytes; };
  uint32_t kind, mode; std::vector<Sec> secs;
  Writer(uint32_t k, uint32_t m) : kind(k), mode(m) {}
  void add(const std::string& name, uint32_t dt, const void* d, size_t bytes, uint64_t d0, uint64_t d1 = 0) {
    if (name.size() >= 48) throw Error(Status::internal_error, "section name too long: " + name);
    Sec s; std::memset(&s.e, 0, sizeof s.e); std::memcpy(s.e.name, name.data(), name.size());
    s.e.dtype = dt; s.e.ndim = d1 ? 2 : 1; s.e.dims[0] = d0; s.e.dims[1] = d1; s.e.length = bytes;
    s.bytes.assign((const uint8_t*)d, (const uint8_t*)d + bytes);
    sha256(s.bytes.data(), bytes, s.e.sha256);
    secs.push_back(std::move(s));
  }
  template <class T> void vec(const std::string& name, uint32_t dt, const std::vector<T>& v) { add(name, dt, v.data(), v.size() * sizeof(T), v.size()); }
  void json(const std::string& name, const std::string& s) { add(name, JSON, s.data(), s.size(), s.size()); }
  // returns the content hash (SHA-256 of the section table)
  std::string write(const std::string& path) {
    uint64_t off = 128 + 128 * (uint64_t)secs.size();
    for (auto& s : secs) { off = (off + 63) & ~uint64_t(63); s.e.offset = off; off += s.e.length; }
    std::vector<SectionEntry> tab; for (auto& s : secs) tab.push_back(s.e);
    FileHeader h; std::memset(&h, 0, sizeof h); std::memcpy(h.magic, "SMCBVS4", 8);
    h.format_version = 1; h.kind = kind; h.mode = mode; h.n_sections = (uint32_t)secs.size(); h.file_bytes = off;
    sha256(tab.data(), tab.size() * sizeof(SectionEntry), h.table_sha256);
    std::string tmp = path + ".tmp." + std::to_string(getpid());
    int fd = ::open(tmp.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) throw Error(Status::io_error, "cannot open " + tmp);
    auto put = [&](const void* d, size_t n) { const uint8_t* p = (const uint8_t*)d; while (n) { ssize_t w = ::write(fd, p, n); if (w <= 0) { ::close(fd); throw Error(Status::io_error, "write failed: " + tmp); } p += w; n -= w; } };
    uint64_t pos = 0; static const uint8_t zeros[64] = {};
    put(&h, sizeof h); put(tab.data(), tab.size() * sizeof(SectionEntry)); pos = 128 + 128 * tab.size();
    for (auto& s : secs) { while (pos < s.e.offset) { size_t t = std::min<uint64_t>(64, s.e.offset - pos); put(zeros, t); pos += t; } put(s.bytes.data(), s.bytes.size()); pos += s.bytes.size(); }
    if (::fsync(fd) != 0 || ::close(fd) != 0) throw Error(Status::io_error, "fsync/close failed: " + tmp);
    if (std::rename(tmp.c_str(), path.c_str()) != 0) throw Error(Status::io_error, "rename failed: " + path);
    return hex(h.table_sha256, 32);
  }
};

struct Reader {
  FileHeader h; std::vector<SectionEntry> tab; std::vector<uint8_t> file;
  explicit Reader(const std::string& path, uint32_t want_kind) {
    FILE* f = std::fopen(path.c_str(), "rb");
    if (!f) throw Error(Status::io_error, "cannot open " + path);
    std::fseek(f, 0, SEEK_END); long n = std::ftell(f); std::fseek(f, 0, SEEK_SET);
    file.resize(n); size_t got = std::fread(file.data(), 1, n, f); std::fclose(f);
    if ((long)got != n || n < 128) throw Error(Status::invalid_input, "short file " + path);
    std::memcpy(&h, file.data(), 128);
    if (std::memcmp(h.magic, "SMCBVS4", 8) != 0 || h.format_version != 1 || h.kind != want_kind || h.file_bytes != (uint64_t)n)
      throw Error(Status::invalid_input, "bad header in " + path);
    tab.resize(h.n_sections); std::memcpy(tab.data(), file.data() + 128, 128 * (size_t)h.n_sections);
    uint8_t d[32]; sha256(tab.data(), tab.size() * sizeof(SectionEntry), d);
    if (std::memcmp(d, h.table_sha256, 32)) throw Error(Status::invalid_input, "section table hash mismatch in " + path);
    for (auto& e : tab) {
      if (e.offset + e.length > (uint64_t)n) throw Error(Status::invalid_input, "section out of range");
      sha256(file.data() + e.offset, e.length, d);
      if (std::memcmp(d, e.sha256, 32)) throw Error(Status::invalid_input, std::string("section hash mismatch: ") + e.name);
    }
  }
  const SectionEntry& sec(const std::string& name) const {
    for (auto& e : tab) if (name == e.name) return e;
    throw Error(Status::invalid_input, "missing section " + name);
  }
  template <class T> std::vector<T> vec(const std::string& name) const {
    const auto& e = sec(name); std::vector<T> v(e.length / sizeof(T));
    if (e.length) std::memcpy(v.data(), file.data() + e.offset, e.length);
    return v;
  }
  std::string json(const std::string& name) const { const auto& e = sec(name); return std::string((const char*)file.data() + e.offset, e.length); }
  std::string content_hash() const { return hex(h.table_sha256, 32); }
};

}  // namespace v4::fmt
