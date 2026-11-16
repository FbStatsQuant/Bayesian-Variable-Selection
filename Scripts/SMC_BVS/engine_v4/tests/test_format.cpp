#include <fstream>
#include "tk.h"
#include "tutil.h"
#include <cstring>
#include "v4/format.h"
#include "v4/sha256.h"
using namespace v4;

TEST(format_roundtrip_and_alignment) {
  std::string f = tmp_path("fmt.bin");
  std::vector<double> a = {1.5, -2.25, 3.0}; std::vector<int32_t> b = {7, 8, 9, 10, 11};
  std::vector<uint64_t> c(1000); for (size_t i = 0; i < c.size(); ++i) c[i] = i * i;
  fmt::Writer w(fmt::K_SETUP, fmt::M_V);
  w.add("a", a); w.add("b", b, 5); w.add("c_cm", c, 10, 100);
  Json m = Json::object(); m["x"] = 3; w.add_json("meta", m);
  std::vector<double> empty; w.add("empty", empty);
  std::string h = w.write(f);
  fmt::Reader r(f);
  CHECK(r.kind() == fmt::K_SETUP && r.mode() == fmt::M_V && r.content_hash() == h);
  CHECK(r.vec<double>("a") == a); CHECK(r.vec<int32_t>("b") == b); CHECK(r.vec<uint64_t>("c_cm") == c);
  CHECK(r.entry("c_cm").ndim == 2 && r.entry("c_cm").dims[1] == 100);
  CHECK(r.json("meta").at("x").i64() == 3);
  CHECK(r.vec<double>("empty").empty());
  for (auto& e : r.sections()) CHECK(e.offset % 64 == 0);
  CHECK_THROWS(r.get<int32_t>("a"));          // wrong dtype
  CHECK_THROWS(r.entry("nope"));
  // same content -> same content hash
  CHECK(w.write(f + "2") == h);
  std::remove((f + "2").c_str());
  // the header (kind / mode) is covered by the content hash: a changed mode byte is detected
  { std::fstream io(f, std::ios::in | std::ios::out | std::ios::binary); io.seekp(16); uint32_t m = fmt::M_COMPAT; io.write((char*)&m, 4); }
  CHECK_THROWS(fmt::Reader tampered(f));
  CHECK(w.write(f) == h);
  // a flipped byte in a section is detected
  { std::fstream io(f, std::ios::in | std::ios::out | std::ios::binary); io.seekp((std::streamoff)r.entry("c_cm").offset + 17); char z = 0x5A; io.write(&z, 1); }
  CHECK_THROWS(fmt::Reader bad(f));
  // a truncated file is detected
  { std::ofstream t(f, std::ios::binary | std::ios::trunc); t << "SMCBVS4"; }
  CHECK_THROWS(fmt::Reader bad2(f));
  std::remove(f.c_str());
  CHECK_THROWS(fmt::Reader missing(f));
}
// A crafted section entry whose offset + length wraps around, with every hash recomputed so that only the range check
// can catch it (review PR11 #11 / R3); and an entry pointing into the header.
TEST(format_malformed_entries_rejected) {
  std::string f = tmp_path("mal.bin");
  std::vector<double> a(16, 1.0);
  fmt::Writer w(fmt::K_DATA, fmt::M_NONE); w.add("a", a); w.write(f);
  auto craft = [&](uint64_t off, uint64_t len) {
    std::fstream io(f, std::ios::in | std::ios::out | std::ios::binary);
    fmt::FileHeader h; io.read((char*)&h, sizeof h);
    fmt::SectionEntry e; io.read((char*)&e, sizeof e);
    e.offset = off; e.length = len;
    auto th = sha256(&e, sizeof e); std::memcpy(h.table_sha256, th.data(), 32);
    fmt::FileHeader z = h; std::memset(z.table_sha256, 0, 32); std::memset(z.content_sha256, 0, 32);
    Sha256 s; s.update(&z, sizeof z); s.update(&e, sizeof e); auto ch = s.final(); std::memcpy(h.content_sha256, ch.data(), 32);
    io.seekp(0); io.write((char*)&h, sizeof h); io.write((char*)&e, sizeof e);
  };
  craft(64, 0xFFFFFFFFFFFFFFC0ULL);          // offset + length wraps to a small number
  bool range = false;
  try { fmt::Reader r(f); } catch (const Error& e) { range = std::string(e.what()).find("out of range") != std::string::npos; }
  CHECK(range);
  craft(0, 128);                              // inside the header and table
  range = false;
  try { fmt::Reader r(f); } catch (const Error& e) { range = std::string(e.what()).find("out of range") != std::string::npos; }
  CHECK(range);
  std::remove(f.c_str());
}
TEST(format_duplicate_section_rejected) {
  fmt::Writer w(fmt::K_RAW, fmt::M_NONE); std::vector<double> a = {1};
  w.add("x", a); CHECK_THROWS(w.add("x", a));
  CHECK_THROWS(w.add(std::string(60, 'n'), a));
}

// Tests write only under $TMPDIR: tmp_path() refuses when it is unset or empty (no fallback into the working tree).
TEST(tmp_path_requires_tmpdir) {
  const char* old = std::getenv("TMPDIR");
  std::string saved = old ? old : "";
  ::unsetenv("TMPDIR");
  CHECK_THROWS(tmp_path("x"));
  ::setenv("TMPDIR", "", 1);
  CHECK_THROWS(tmp_path("x"));
  if (old) ::setenv("TMPDIR", saved.c_str(), 1); else ::unsetenv("TMPDIR");
  if (old) CHECK(tmp_path("x").rfind(saved + "/v4test_", 0) == 0);
}
