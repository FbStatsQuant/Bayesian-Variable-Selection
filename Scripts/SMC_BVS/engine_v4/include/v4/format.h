// format.h -- the binary container of every engine file (INTERFACES §5.1; ENGINEERING_SPEC §1).
// FileHeader (128 B) | SectionEntry[n] (128 B each) | sections at 64-byte aligned offsets. Little-endian.
#pragma once
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <type_traits>
#include <vector>
#include "v4/json.h"
#include "v4/status.h"

namespace v4::fmt {

enum Kind : uint32_t { K_RAW = 1, K_DATA = 2, K_SETUP = 3, K_CALIB = 4, K_ISLAND = 5, K_FIT = 6, K_LAW = 7, K_CKPT = 8, K_EVAL = 9 };
enum Mode : uint32_t { M_NONE = 0 /* gen / prep outputs */, M_COMPAT = 1, M_LAW = 2, M_V = 3 };
enum DType : uint32_t { D_F64 = 1, D_I32 = 2, D_U32 = 3, D_I64 = 4, D_U64 = 5, D_U8 = 6, D_U16 = 7, D_F32 = 8, D_JSON = 9 };
constexpr uint32_t FORMAT_VERSION = 1;
constexpr char MAGIC[8] = {'S', 'M', 'C', 'B', 'V', 'S', '4', '\0'};

#pragma pack(push, 1)
struct FileHeader {
  char magic[8]; uint32_t format_version, kind, mode, n_sections; uint64_t file_bytes;
  uint8_t table_sha256[32];     // SHA-256 of the section table
  uint8_t content_sha256[32];   // SHA-256 of (this header with both hash fields zeroed || section table) = file content hash
  uint8_t reserved[32];
};
struct SectionEntry {
  char name[48]; uint32_t dtype, ndim; uint64_t dims[2]; uint64_t offset, length; uint8_t sha256[32]; uint8_t reserved[8];
};
#pragma pack(pop)
static_assert(sizeof(FileHeader) == 128 && sizeof(SectionEntry) == 128, "container layout");

size_t dtype_size(uint32_t dt);
template <class T> constexpr uint32_t dtype_of() {
  if constexpr (std::is_same_v<T, double>) return D_F64;
  else if constexpr (std::is_same_v<T, int32_t>) return D_I32;
  else if constexpr (std::is_same_v<T, uint32_t>) return D_U32;
  else if constexpr (std::is_same_v<T, int64_t>) return D_I64;
  else if constexpr (std::is_same_v<T, uint64_t>) return D_U64;
  else if constexpr (std::is_same_v<T, uint8_t>) return D_U8;
  else if constexpr (std::is_same_v<T, uint16_t>) return D_U16;
  else if constexpr (std::is_same_v<T, float>) return D_F32;
  else static_assert(sizeof(T) == 0, "unsupported section type");
}

// Writer: collect sections, then write(path) = temporary name, fsync, rename. Returns the file's content hash.
// add()/add_raw() keep a POINTER to the caller's data (no copy: X is 1.6 GB at p = 10^6); it must stay alive and
// unchanged until write() returns. add_json() and add_copy() own their bytes.
class Writer {
 public:
  Writer(uint32_t kind, uint32_t mode) : kind_(kind), mode_(mode) {}
  template <class T> void add(const std::string& name, const T* p, uint64_t count, uint64_t d0 = 0, uint64_t d1 = 0) {
    add_raw(name, dtype_of<T>(), p, count * sizeof(T), d0 ? d0 : count, d1);
  }
  template <class T> void add(const std::string& name, const std::vector<T>& v, uint64_t d0 = 0, uint64_t d1 = 0) {
    add(name, v.data(), v.size(), d0, d1);
  }
  void add_json(const std::string& name, const Json& j);
  void add_raw(const std::string& name, uint32_t dtype, const void* p, uint64_t bytes, uint64_t d0, uint64_t d1);
  void add_copy(const std::string& name, uint32_t dtype, const void* p, uint64_t bytes, uint64_t d0, uint64_t d1);
  std::string write(const std::string& path) const;   // hex content hash (content_sha256: header + table)
 private:
  struct Sec { std::string name; uint32_t dtype; uint64_t d0, d1; const uint8_t* ptr; uint64_t n; std::shared_ptr<std::vector<uint8_t>> own; };
  uint32_t kind_, mode_;
  std::vector<Sec> secs_;
};

// Reader: maps the file read-only, validates the header, the table hash and (by default) every section hash.
class Reader {
 public:
  explicit Reader(const std::string& path, bool verify = true);
  ~Reader();
  Reader(const Reader&) = delete; Reader& operator=(const Reader&) = delete;
  uint32_t kind() const { return hdr_.kind; }
  uint32_t mode() const { return hdr_.mode; }
  const std::string& content_hash() const { return hash_; }   // hex content_sha256 (header + table)
  const std::vector<SectionEntry>& sections() const { return table_; }
  bool has(const std::string& name) const;
  const SectionEntry& entry(const std::string& name) const;   // throws invalid_input
  template <class T> const T* get(const std::string& name, uint64_t* count = nullptr) const {
    const SectionEntry& e = entry(name);
    if (e.dtype != dtype_of<T>()) throw Error(Status::invalid_input, "section " + name + ": wrong dtype");
    if (count) *count = e.length / sizeof(T);
    return reinterpret_cast<const T*>(base_ + e.offset);
  }
  template <class T> std::vector<T> vec(const std::string& name) const { uint64_t c; const T* p = get<T>(name, &c); return std::vector<T>(p, p + c); }
  Json json(const std::string& name) const;
  std::shared_ptr<const void> keep_alive() const;   // keeps the mapping alive (for Data views)
  void verify_all() const;
  void verify_section(const std::string& name) const;   // one section's SHA-256 against the table (throws invalid_input)
 private:
  std::string path_, hash_;
  FileHeader hdr_{};
  std::vector<SectionEntry> table_;
  const uint8_t* base_ = nullptr; size_t size_ = 0;
  std::shared_ptr<void> map_;
};

std::string kind_name(uint32_t k);
std::string mode_name(uint32_t m);
uint32_t mode_from_name(const std::string& s);
}  // namespace v4::fmt
