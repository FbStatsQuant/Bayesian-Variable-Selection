// format.cpp -- container writer / reader (INTERFACES §5.1).
#include "v4/format.h"
#include <cstdio>
#include <cstring>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include "v4/sha256.h"

namespace v4::fmt {

size_t dtype_size(uint32_t dt) {
  switch (dt) {
    case D_F64: case D_I64: case D_U64: return 8;
    case D_I32: case D_U32: case D_F32: return 4;
    case D_U16: return 2;
    case D_U8: case D_JSON: return 1;
    default: throw Error(Status::invalid_input, "unknown dtype " + std::to_string(dt));
  }
}
static uint64_t align64(uint64_t x) { return (x + 63) & ~uint64_t(63); }
// content_sha256 = SHA-256(header with table_sha256 and content_sha256 zeroed || table)
static std::array<uint8_t, 32> content_digest(const FileHeader& h, const SectionEntry* t, size_t n) {
  FileHeader z = h;
  std::memset(z.table_sha256, 0, 32); std::memset(z.content_sha256, 0, 32);
  Sha256 s; s.update(&z, sizeof z); s.update(t, n * sizeof(SectionEntry));
  return s.final();
}

void Writer::add_raw(const std::string& name, uint32_t dtype, const void* p, uint64_t bytes, uint64_t d0, uint64_t d1) {
  if (name.empty() || name.size() >= 48) throw Error(Status::internal_error, "section name length: " + name);
  for (auto& s : secs_) if (s.name == name) throw Error(Status::internal_error, "duplicate section " + name);
  if (bytes && !p) throw Error(Status::internal_error, "null section data: " + name);
  secs_.push_back(Sec{name, dtype, d0, d1, (const uint8_t*)p, bytes, nullptr});
}
void Writer::add_copy(const std::string& name, uint32_t dtype, const void* p, uint64_t bytes, uint64_t d0, uint64_t d1) {
  auto own = std::make_shared<std::vector<uint8_t>>((const uint8_t*)p, (const uint8_t*)p + bytes);
  add_raw(name, dtype, own->data(), bytes, d0, d1);
  secs_.back().own = own;
}
void Writer::add_json(const std::string& name, const Json& j) {
  std::string t = j.dump();
  add_copy(name, D_JSON, t.data(), t.size(), t.size(), 0);
}

static void write_all(int fd, const void* p, size_t n, const std::string& path) {
  const uint8_t* b = (const uint8_t*)p;
  while (n) {
    ssize_t w = ::write(fd, b, n);
    if (w <= 0) throw Error(Status::io_error, "write failed: " + path);
    b += w; n -= (size_t)w;
  }
}

std::string Writer::write(const std::string& path) const {
  std::vector<SectionEntry> table(secs_.size());
  uint64_t off = align64(sizeof(FileHeader) + sizeof(SectionEntry) * secs_.size());
  for (size_t i = 0; i < secs_.size(); ++i) {
    SectionEntry& e = table[i];
    std::memset(&e, 0, sizeof e);
    std::memcpy(e.name, secs_[i].name.data(), secs_[i].name.size());
    e.dtype = secs_[i].dtype; e.ndim = secs_[i].d1 ? 2 : 1; e.dims[0] = secs_[i].d0; e.dims[1] = secs_[i].d1;
    e.offset = off; e.length = secs_[i].n;
    auto h = sha256(secs_[i].ptr, secs_[i].n);
    std::memcpy(e.sha256, h.data(), 32);
    off = align64(off + e.length);
  }
  FileHeader hd; std::memset(&hd, 0, sizeof hd);
  std::memcpy(hd.magic, MAGIC, 8);
  hd.format_version = FORMAT_VERSION; hd.kind = kind_; hd.mode = mode_; hd.n_sections = (uint32_t)secs_.size();
  hd.file_bytes = off;
  auto th = sha256(table.data(), table.size() * sizeof(SectionEntry));
  std::memcpy(hd.table_sha256, th.data(), 32);
  std::array<uint8_t, 32> ch = content_digest(hd, table.data(), table.size());
  std::memcpy(hd.content_sha256, ch.data(), 32);
  std::string tmp = path + ".tmp." + std::to_string(::getpid());
  int fd = ::open(tmp.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
  if (fd < 0) throw Error(Status::io_error, "cannot create " + tmp);
  try {
    write_all(fd, &hd, sizeof hd, tmp);
    write_all(fd, table.data(), table.size() * sizeof(SectionEntry), tmp);
    uint64_t pos = sizeof hd + table.size() * sizeof(SectionEntry);
    static const uint8_t zeros[64] = {0};
    for (size_t i = 0; i < secs_.size(); ++i) {
      write_all(fd, zeros, table[i].offset - pos, tmp); pos = table[i].offset;
      write_all(fd, secs_[i].ptr, secs_[i].n, tmp); pos += secs_[i].n;
    }
    write_all(fd, zeros, off - pos, tmp);
    if (::fsync(fd) != 0) throw Error(Status::io_error, "fsync failed: " + tmp);
  } catch (...) { ::close(fd); ::unlink(tmp.c_str()); throw; }
  ::close(fd);
  if (std::rename(tmp.c_str(), path.c_str()) != 0) { ::unlink(tmp.c_str()); throw Error(Status::io_error, "rename failed: " + path); }
  // make the rename durable: fsync the parent directory
  std::string dir = path.find('/') == std::string::npos ? "." : path.substr(0, path.rfind('/'));
  if (dir.empty()) dir = "/";
  int dfd = ::open(dir.c_str(), O_RDONLY | O_DIRECTORY);
  if (dfd >= 0) { if (::fsync(dfd) != 0) { ::close(dfd); throw Error(Status::io_error, "directory fsync failed: " + dir); } ::close(dfd); }
  return hex(ch);
}

Reader::Reader(const std::string& path, bool verify) : path_(path) {
  int fd = ::open(path.c_str(), O_RDONLY);
  if (fd < 0) throw Error(Status::invalid_input, "cannot open " + path);
  struct stat st;
  if (::fstat(fd, &st) != 0) { ::close(fd); throw Error(Status::io_error, "fstat " + path); }
  size_ = (size_t)st.st_size;
  if (size_ < sizeof(FileHeader)) { ::close(fd); throw Error(Status::invalid_input, "file too short: " + path); }
  void* m = ::mmap(nullptr, size_, PROT_READ, MAP_SHARED, fd, 0);
  ::close(fd);
  if (m == MAP_FAILED) throw Error(Status::io_error, "mmap " + path);
  size_t sz = size_;
  map_ = std::shared_ptr<void>(m, [sz](void* q) { ::munmap(q, sz); });
  base_ = (const uint8_t*)m;
  std::memcpy(&hdr_, base_, sizeof hdr_);
  if (std::memcmp(hdr_.magic, MAGIC, 8) != 0) throw Error(Status::invalid_input, "bad magic: " + path);
  if (hdr_.format_version != FORMAT_VERSION) throw Error(Status::invalid_input, "unsupported format version: " + path);
  if (hdr_.file_bytes != size_) throw Error(Status::invalid_input, "file size mismatch (truncated?): " + path);
  uint64_t tb = (uint64_t)hdr_.n_sections * sizeof(SectionEntry);
  if (hdr_.n_sections > (size_ - sizeof(FileHeader)) / sizeof(SectionEntry)) throw Error(Status::invalid_input, "section table out of range: " + path);
  table_.resize(hdr_.n_sections);
  std::memcpy(table_.data(), base_ + sizeof(FileHeader), tb);
  auto th = sha256(table_.data(), tb);
  if (std::memcmp(th.data(), hdr_.table_sha256, 32) != 0) throw Error(Status::invalid_input, "section table hash mismatch: " + path);
  auto ch = content_digest(hdr_, table_.data(), table_.size());
  if (std::memcmp(ch.data(), hdr_.content_sha256, 32) != 0) throw Error(Status::invalid_input, "header hash mismatch (header altered): " + path);
  hash_ = hex(ch);
  const uint64_t data_start = sizeof(FileHeader) + tb;
  for (auto& e : table_) {
    // overflow-safe: length <= size, offset <= size - length; sections start after the header and table
    if (e.offset % 64 != 0 || e.length > size_ || e.offset > size_ - e.length || e.offset < data_start)
      throw Error(Status::invalid_input, "section out of range: " + path);
    dtype_size(e.dtype);
    if (e.length % dtype_size(e.dtype) != 0) throw Error(Status::invalid_input, "section length not a multiple of its dtype: " + path);
  }
  if (verify) verify_all();
}
Reader::~Reader() = default;
void Reader::verify_all() const {
  for (auto& e : table_) {
    auto h = sha256(base_ + e.offset, e.length);
    if (std::memcmp(h.data(), e.sha256, 32) != 0)
      throw Error(Status::invalid_input, std::string("section hash mismatch: ") + e.name + " in " + path_);
  }
}
bool Reader::has(const std::string& name) const {
  for (auto& e : table_) if (name == e.name) return true;
  return false;
}
const SectionEntry& Reader::entry(const std::string& name) const {
  for (auto& e : table_) if (name == e.name) return e;
  throw Error(Status::invalid_input, "missing section " + name + " in " + path_);
}
Json Reader::json(const std::string& name) const {
  const SectionEntry& e = entry(name);
  if (e.dtype != D_JSON) throw Error(Status::invalid_input, "section " + name + " is not json");
  return Json::parse(std::string((const char*)base_ + e.offset, e.length));
}
std::shared_ptr<const void> Reader::keep_alive() const { return map_; }

std::string kind_name(uint32_t k) {
  static const char* nm[] = {"?", "raw", "data", "setup", "calib", "island", "fit", "law", "ckpt", "eval"};
  return k < 10 ? nm[k] : "?";
}
std::string mode_name(uint32_t m) { return m == M_COMPAT ? "compat" : m == M_LAW ? "law" : m == M_V ? "V" : "none"; }
uint32_t mode_from_name(const std::string& s) {
  if (s == "compat") return M_COMPAT;
  if (s == "law") return M_LAW;
  if (s == "V") return M_V;
  if (s == "none") return M_NONE;
  throw Error(Status::invalid_input, "unknown mode " + s);
}
}  // namespace v4::fmt
