#include <fstream>
#include "tk.h"
#include "tutil.h"
#include "v4/format.h"
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
TEST(format_duplicate_section_rejected) {
  fmt::Writer w(fmt::K_RAW, fmt::M_NONE); std::vector<double> a = {1};
  w.add("x", a); CHECK_THROWS(w.add("x", a));
  CHECK_THROWS(w.add(std::string(60, 'n'), a));
}
