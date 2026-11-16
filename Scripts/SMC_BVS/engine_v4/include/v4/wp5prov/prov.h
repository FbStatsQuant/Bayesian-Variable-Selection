// wp5prov/prov.h -- PROVISIONAL WP5-local infrastructure (WP5 builder, 2026-11-15).
//
// INTERFACES v0.1 §8 assigns sha256, format.h (the .bin container), rng.h (Philox) and status.h to WP1. They were not yet
// on origin/exp/P1M-engine when WP5 started, so WP5 carries minimal implementations of exactly the v0.1 contract here,
// in namespace v4::wp5prov. When the WP1 skeleton lands, every use is switched to the WP1 header and this directory is
// deleted (one commit; the tests in tests/wp5/test_prov.cpp then run against the WP1 versions unchanged).
#pragma once
#include <cstdint>
#include <cstring>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace v4 {

// ---- INTERFACES §7 statuses (provisional copy) ------------------------------------------------------------------
#ifndef V4_HAVE_STATUS_H
enum class Status : uint8_t { completed = 0, resource_limit = 1, numerical_failure = 2, invalid_input = 3, io_error = 4, internal_error = 5 };
inline const char* status_name(Status s) {
  switch (s) {
    case Status::completed: return "completed";
    case Status::resource_limit: return "resource_limit";
    case Status::numerical_failure: return "numerical_failure";
    case Status::invalid_input: return "invalid_input";
    case Status::io_error: return "io_error";
    default: return "internal_error";
  }
}
struct Error : std::runtime_error {
  Status st;
  Error(Status s, const std::string& m) : std::runtime_error(m), st(s) {}
};
struct NumericalFailure : Error {
  explicit NumericalFailure(const std::string& m) : Error(Status::numerical_failure, m) {}
};
#endif

namespace wp5prov {

// ---- SHA-256 (FIPS 180-4) ----------------------------------------------------------------------------------------
struct Sha256 {
  uint32_t h[8]; uint64_t len = 0; uint8_t buf[64]; size_t nb = 0;
  Sha256();
  void update(const void* p, size_t n);
  void final(uint8_t out[32]);
};
std::string hex(const uint8_t* d, size_t n);
std::string sha256_hex(const void* p, size_t n);

// ---- Philox4x32-10 and the INTERFACES §3 address map -------------------------------------------------------------
enum Role : uint8_t { R_FINAL = 0, R_PILOT = 1, R_DIAG = 2, R_POST = 3, R_GEN = 4, R_TEST = 5 };
enum XPh : uint8_t { X_INIT = 0, X_RESAMPLE = 1, X_BRIDGE = 2, X_BURN = 3, X_MEASURED = 4, X_POST = 5,
                     X_GEN_X = 8, X_GEN_NOISE = 9, X_GEN_FACTOR = 10, X_TEST_X = 11, X_TEST_NOISE = 12, X_TEST_FACTOR = 13 };
struct Address {
  uint32_t seed = 0; uint8_t role = 0, tier = 0, iter = 0; uint32_t island = 0;
  uint8_t xph = 0; uint32_t stage = 0; uint32_t particle = 0, position = 0, slot = 0;
};
void philox4x32_10(const uint32_t ctr_in[4], const uint32_t key_in[2], uint32_t out[4]);
void philox_at(const Address& a, uint32_t out[4]);
double uniform_at(const Address& a);    // u  (first variate)
double uniform2_at(const Address& a);   // u2 (second variate)

// ---- the §5.1 .bin container ---------------------------------------------------------------------------------------
enum DType : uint32_t { DT_F64 = 1, DT_I32 = 2, DT_U32 = 3, DT_I64 = 4, DT_U64 = 5, DT_U8 = 6, DT_U16 = 7, DT_F32 = 8, DT_JSON = 9 };
enum Kind : uint32_t { K_RAW = 1, K_DATA = 2, K_SETUP = 3, K_CALIB = 4, K_ISLAND = 5, K_FIT = 6, K_LAW = 7, K_CKPT = 8, K_EVAL = 9 };
enum Mode : uint32_t { M_COMPAT = 1, M_LAW = 2, M_V = 3 };
#pragma pack(push, 1)
struct FileHeader {
  char magic[8]; uint32_t format_version, kind, mode, n_sections; uint64_t file_bytes;
  uint8_t table_sha256[32]; uint8_t reserved[64];
};
struct SectionEntry {
  char name[48]; uint32_t dtype, ndim; uint64_t dims[2]; uint64_t offset, length; uint8_t sha256[32];
  uint8_t reserved[8];   // INTERFACES v0.1 lists 120 B of fields for a 128 B entry; WP5 pads at the end (change request to WP1)
};
#pragma pack(pop)
static_assert(sizeof(FileHeader) == 128, "FileHeader must be 128 bytes");
static_assert(sizeof(SectionEntry) == 128, "SectionEntry must be 128 bytes");
size_t dtype_size(uint32_t dt);

class BinWriter {
 public:
  BinWriter(uint32_t kind, uint32_t mode) : kind_(kind), mode_(mode) {}
  void add(const std::string& name, uint32_t dtype, const void* data, uint64_t bytes, uint32_t ndim, uint64_t d0, uint64_t d1 = 0);
  template <class T> void add_vec(const std::string& name, uint32_t dtype, const std::vector<T>& v) {
    add(name, dtype, v.data(), v.size() * sizeof(T), 1, v.size());
  }
  void add_json(const std::string& name, const std::string& text) { add(name, DT_JSON, text.data(), text.size(), 1, text.size()); }
  // Writes <path>.tmp.<pid>, fsyncs, renames. Returns the content hash (SHA-256 of the section table, hex). Throws Error(io_error).
  std::string write(const std::string& path) const;
 private:
  struct Sec { std::string name; uint32_t dtype, ndim; uint64_t d0, d1; std::vector<uint8_t> bytes; };
  uint32_t kind_, mode_;
  std::vector<Sec> secs_;
};

class BinReader {
 public:
  // mmap read-only; verifies magic, version, table hash and (verify_sections) every section hash. Throws Error(invalid_input).
  explicit BinReader(const std::string& path, bool verify_sections = true);
  ~BinReader();
  BinReader(const BinReader&) = delete; BinReader& operator=(const BinReader&) = delete;
  const FileHeader& header() const { return *hdr_; }
  bool has(const std::string& name) const { return idx_.count(name) > 0; }
  const SectionEntry& entry(const std::string& name) const;
  const void* raw(const std::string& name) const;
  template <class T> const T* ptr(const std::string& name, uint32_t dtype, uint64_t* count = nullptr) const {
    const SectionEntry& e = entry(name);
    if (e.dtype != dtype) throw Error(Status::invalid_input, "section " + name + ": dtype mismatch");
    if (count) *count = e.length / sizeof(T);
    return reinterpret_cast<const T*>(raw(name));
  }
  std::string json(const std::string& name) const;
  std::string content_hash() const { return hex(hdr_->table_sha256, 32); }
  std::vector<std::string> names() const;
 private:
  const uint8_t* base_ = nullptr; size_t size_ = 0;
  const FileHeader* hdr_ = nullptr; const SectionEntry* tab_ = nullptr;
  std::map<std::string, size_t> idx_;
};

}  // namespace wp5prov
}  // namespace v4
