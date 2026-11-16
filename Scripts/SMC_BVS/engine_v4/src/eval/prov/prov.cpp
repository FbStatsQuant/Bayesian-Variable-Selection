// prov.cpp -- PROVISIONAL WP5-local SHA-256, Philox4x32-10 and .bin container (see include/v4/wp5prov/prov.h).
#include "v4/wp5prov/prov.h"

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#include <cstdio>

namespace v4::wp5prov {

// ---------------------------------------------------------------- SHA-256
static const uint32_t K256[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01,
    0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08,
    0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};
static inline uint32_t rotr(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }
static void sha_block(uint32_t h[8], const uint8_t* p) {
  uint32_t w[64];
  for (int i = 0; i < 16; ++i) w[i] = (uint32_t)p[4 * i] << 24 | (uint32_t)p[4 * i + 1] << 16 | (uint32_t)p[4 * i + 2] << 8 | p[4 * i + 3];
  for (int i = 16; i < 64; ++i) {
    uint32_t s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >> 3);
    uint32_t s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >> 10);
    w[i] = w[i - 16] + s0 + w[i - 7] + s1;
  }
  uint32_t a = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], hh = h[7];
  for (int i = 0; i < 64; ++i) {
    uint32_t S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25), ch = (e & f) ^ (~e & g);
    uint32_t t1 = hh + S1 + ch + K256[i] + w[i];
    uint32_t S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22), mj = (a & b) ^ (a & c) ^ (b & c);
    uint32_t t2 = S0 + mj;
    hh = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
  }
  h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += hh;
}
Sha256::Sha256() {
  static const uint32_t h0[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19};
  std::memcpy(h, h0, sizeof h);
}
void Sha256::update(const void* pv, size_t n) {
  const uint8_t* p = static_cast<const uint8_t*>(pv);
  len += n;
  if (nb) {
    size_t t = std::min(n, 64 - nb);
    std::memcpy(buf + nb, p, t); nb += t; p += t; n -= t;
    if (nb == 64) { sha_block(h, buf); nb = 0; }
  }
  while (n >= 64) { sha_block(h, p); p += 64; n -= 64; }
  if (n) { std::memcpy(buf, p, n); nb = n; }
}
void Sha256::final(uint8_t out[32]) {
  uint64_t bits = len * 8;
  uint8_t pad = 0x80; update(&pad, 1);
  uint8_t z = 0; while (nb != 56) update(&z, 1);
  uint8_t L[8]; for (int i = 0; i < 8; ++i) L[i] = (uint8_t)(bits >> (56 - 8 * i));
  update(L, 8);
  for (int i = 0; i < 8; ++i) { out[4 * i] = h[i] >> 24; out[4 * i + 1] = h[i] >> 16; out[4 * i + 2] = h[i] >> 8; out[4 * i + 3] = h[i]; }
}
std::string hex(const uint8_t* d, size_t n) {
  static const char* x = "0123456789abcdef";
  std::string s(2 * n, '0');
  for (size_t i = 0; i < n; ++i) { s[2 * i] = x[d[i] >> 4]; s[2 * i + 1] = x[d[i] & 15]; }
  return s;
}
std::string sha256_hex(const void* p, size_t n) { Sha256 s; s.update(p, n); uint8_t o[32]; s.final(o); return hex(o, 32); }

// ---------------------------------------------------------------- Philox4x32-10 (Salmon et al. 2011; Random123)
void philox4x32_10(const uint32_t ci[4], const uint32_t ki[2], uint32_t out[4]) {
  const uint32_t M0 = 0xD2511F53u, M1 = 0xCD9E8D57u, W0 = 0x9E3779B9u, W1 = 0xBB67AE85u;
  uint32_t c0 = ci[0], c1 = ci[1], c2 = ci[2], c3 = ci[3], k0 = ki[0], k1 = ki[1];
  for (int r = 0; r < 10; ++r) {
    if (r) { k0 += W0; k1 += W1; }
    uint64_t p0 = (uint64_t)M0 * c0, p1 = (uint64_t)M1 * c2;
    uint32_t hi0 = (uint32_t)(p0 >> 32), lo0 = (uint32_t)p0, hi1 = (uint32_t)(p1 >> 32), lo1 = (uint32_t)p1;
    uint32_t n0 = hi1 ^ c1 ^ k0, n1 = lo1, n2 = hi0 ^ c3 ^ k1, n3 = lo0;
    c0 = n0; c1 = n1; c2 = n2; c3 = n3;
  }
  out[0] = c0; out[1] = c1; out[2] = c2; out[3] = c3;
}
void philox_at(const Address& a, uint32_t out[4]) {
  // INTERFACES §3: key = { seed, (role<<28)|(tier<<26)|(iter<<20)|island }; ctr = { slot, position, particle, (xph<<24)|stage }
  if (a.island >= (1u << 20) || a.iter >= 64 || a.tier >= 4 || a.stage >= (1u << 24) || a.role >= 16)
    throw Error(Status::internal_error, "philox address field out of range");
  uint32_t key[2] = {a.seed, ((uint32_t)a.role << 28) | ((uint32_t)a.tier << 26) | ((uint32_t)a.iter << 20) | a.island};
  uint32_t ctr[4] = {a.slot, a.position, a.particle, ((uint32_t)a.xph << 24) | a.stage};
  philox4x32_10(ctr, key, out);
}
double uniform_at(const Address& a) {
  uint32_t x[4]; philox_at(a, x);
  return (double)((((uint64_t)x[1] << 32) | x[0]) >> 11) * 0x1.0p-53;
}
double uniform2_at(const Address& a) {
  uint32_t x[4]; philox_at(a, x);
  return (double)((((uint64_t)x[3] << 32) | x[2]) >> 11) * 0x1.0p-53;
}

// ---------------------------------------------------------------- container
size_t dtype_size(uint32_t dt) {
  switch (dt) {
    case DT_F64: case DT_I64: case DT_U64: return 8;
    case DT_I32: case DT_U32: case DT_F32: return 4;
    case DT_U16: return 2;
    case DT_U8: case DT_JSON: return 1;
  }
  throw Error(Status::invalid_input, "unknown dtype");
}
void BinWriter::add(const std::string& name, uint32_t dtype, const void* data, uint64_t bytes, uint32_t ndim, uint64_t d0, uint64_t d1) {
  if (name.size() >= 48) throw Error(Status::internal_error, "section name too long: " + name);
  for (auto& s : secs_) if (s.name == name) throw Error(Status::internal_error, "duplicate section " + name);
  uint64_t elems = ndim == 2 ? d0 * d1 : d0;
  if (elems * dtype_size(dtype) != bytes) throw Error(Status::internal_error, "section " + name + ": dims do not match bytes");
  Sec s{name, dtype, ndim, d0, d1, {}};
  s.bytes.assign((const uint8_t*)data, (const uint8_t*)data + bytes);
  secs_.push_back(std::move(s));
}
static uint64_t align64(uint64_t x) { return (x + 63) & ~uint64_t(63); }
std::string BinWriter::write(const std::string& path) const {
  std::vector<SectionEntry> tab(secs_.size());
  uint64_t off = align64(128 + 128 * secs_.size());
  for (size_t i = 0; i < secs_.size(); ++i) {
    SectionEntry& e = tab[i]; std::memset(&e, 0, sizeof e);
    std::memcpy(e.name, secs_[i].name.data(), secs_[i].name.size());
    e.dtype = secs_[i].dtype; e.ndim = secs_[i].ndim; e.dims[0] = secs_[i].d0; e.dims[1] = secs_[i].d1;
    e.offset = off; e.length = secs_[i].bytes.size();
    Sha256 h; h.update(secs_[i].bytes.data(), secs_[i].bytes.size()); h.final(e.sha256);
    off = align64(off + e.length);
  }
  FileHeader H; std::memset(&H, 0, sizeof H);
  std::memcpy(H.magic, "SMCBVS4\0", 8);
  H.format_version = 1; H.kind = kind_; H.mode = mode_; H.n_sections = (uint32_t)secs_.size(); H.file_bytes = off;
  { Sha256 h; h.update(tab.data(), tab.size() * sizeof(SectionEntry)); h.final(H.table_sha256); }
  std::string tmp = path + ".tmp." + std::to_string(getpid());
  int fd = ::open(tmp.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
  if (fd < 0) throw Error(Status::io_error, "cannot create " + tmp);
  auto put = [&](const void* p, size_t n) {
    const uint8_t* c = (const uint8_t*)p;
    while (n) { ssize_t w = ::write(fd, c, n); if (w <= 0) { ::close(fd); throw Error(Status::io_error, "write failed: " + tmp); } c += w; n -= (size_t)w; }
  };
  uint64_t pos = 0; static const uint8_t zeros[64] = {0};
  put(&H, sizeof H); pos += sizeof H;
  put(tab.data(), tab.size() * sizeof(SectionEntry)); pos += tab.size() * sizeof(SectionEntry);
  for (size_t i = 0; i < secs_.size(); ++i) {
    while (pos < tab[i].offset) { size_t t = (size_t)std::min<uint64_t>(64, tab[i].offset - pos); put(zeros, t); pos += t; }
    put(secs_[i].bytes.data(), secs_[i].bytes.size()); pos += secs_[i].bytes.size();
  }
  while (pos < off) { size_t t = (size_t)std::min<uint64_t>(64, off - pos); put(zeros, t); pos += t; }
  if (::fsync(fd) != 0 || ::close(fd) != 0) throw Error(Status::io_error, "fsync/close failed: " + tmp);
  if (std::rename(tmp.c_str(), path.c_str()) != 0) throw Error(Status::io_error, "rename failed: " + path);
  return hex(H.table_sha256, 32);
}

BinReader::BinReader(const std::string& path, bool verify) {
  int fd = ::open(path.c_str(), O_RDONLY);
  if (fd < 0) throw Error(Status::invalid_input, "cannot open " + path);
  struct stat st; if (fstat(fd, &st) != 0) { ::close(fd); throw Error(Status::invalid_input, "cannot stat " + path); }
  size_ = (size_t)st.st_size;
  if (size_ < 128) { ::close(fd); throw Error(Status::invalid_input, path + ": too short for a header"); }
  void* m = mmap(nullptr, size_, PROT_READ, MAP_PRIVATE, fd, 0);
  ::close(fd);
  if (m == MAP_FAILED) throw Error(Status::invalid_input, "mmap failed: " + path);
  base_ = (const uint8_t*)m; hdr_ = (const FileHeader*)base_;
  if (std::memcmp(hdr_->magic, "SMCBVS4\0", 8) != 0) throw Error(Status::invalid_input, path + ": bad magic");
  if (hdr_->format_version != 1) throw Error(Status::invalid_input, path + ": unsupported format version");
  if (hdr_->file_bytes != size_) throw Error(Status::invalid_input, path + ": file_bytes mismatch (truncated?)");
  uint64_t tb = 128ull * hdr_->n_sections;
  if (128 + tb > size_) throw Error(Status::invalid_input, path + ": section table beyond end");
  tab_ = (const SectionEntry*)(base_ + 128);
  { uint8_t d[32]; Sha256 h; h.update(tab_, tb); h.final(d);
    if (std::memcmp(d, hdr_->table_sha256, 32) != 0) throw Error(Status::invalid_input, path + ": section table hash mismatch"); }
  for (size_t i = 0; i < hdr_->n_sections; ++i) {
    const SectionEntry& e = tab_[i];
    std::string nm(e.name, strnlen(e.name, 48));
    if (e.offset % 64 || e.offset + e.length > size_) throw Error(Status::invalid_input, path + ": bad section " + nm);
    if (verify) {
      uint8_t d[32]; Sha256 h; h.update(base_ + e.offset, e.length); h.final(d);
      if (std::memcmp(d, e.sha256, 32) != 0) throw Error(Status::invalid_input, path + ": hash mismatch in section " + nm);
    }
    if (!idx_.emplace(nm, i).second) throw Error(Status::invalid_input, path + ": duplicate section " + nm);
  }
}
BinReader::~BinReader() { if (base_) munmap((void*)base_, size_); }
const SectionEntry& BinReader::entry(const std::string& name) const {
  auto it = idx_.find(name);
  if (it == idx_.end()) throw Error(Status::invalid_input, "missing section " + name);
  return tab_[it->second];
}
const void* BinReader::raw(const std::string& name) const { return base_ + entry(name).offset; }
std::string BinReader::json(const std::string& name) const {
  const SectionEntry& e = entry(name);
  if (e.dtype != DT_JSON) throw Error(Status::invalid_input, "section " + name + " is not json");
  return std::string((const char*)base_ + e.offset, e.length);
}
std::vector<std::string> BinReader::names() const { std::vector<std::string> v; for (auto& kv : idx_) v.push_back(kv.first); return v; }

}  // namespace v4::wp5prov
