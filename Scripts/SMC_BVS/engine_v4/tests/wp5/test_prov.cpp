// test_prov.cpp -- SHA-256, Philox KAT, the §5.1 container, JSON (provisional WP5 infrastructure).
#include <unistd.h>

#include <cstdio>
#include <fstream>

#include "v4/wp5prov/json.h"
#include "v4/wp5prov/prov.h"
#include "wp5_tk.h"

using namespace v4::wp5prov;

static std::string tmpdir() { const char* t = std::getenv("TMPDIR"); return t ? t : "."; }

TEST(sha256_vectors) {
  CHECK(sha256_hex("", 0) == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
  CHECK(sha256_hex("abc", 3) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
  std::string m = "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq";
  CHECK(sha256_hex(m.data(), m.size()) == "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1");
  std::string mil(1000000, 'a');
  Sha256 h; for (size_t i = 0; i < mil.size(); i += 777) h.update(mil.data() + i, std::min<size_t>(777, mil.size() - i));
  uint8_t d[32]; h.final(d);
  CHECK(hex(d, 32) == "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0");
}

TEST(philox_kat) {
  // Random123 kat_vectors, philox4x32_10
  uint32_t o[4];
  { uint32_t c[4] = {0, 0, 0, 0}, k[2] = {0, 0}; philox4x32_10(c, k, o);
    CHECK(o[0] == 0x6627e8d5u && o[1] == 0xe169c58du && o[2] == 0xbc57ac4cu && o[3] == 0x9b00dbd8u); }
  { uint32_t c[4] = {0xffffffffu, 0xffffffffu, 0xffffffffu, 0xffffffffu}, k[2] = {0xffffffffu, 0xffffffffu}; philox4x32_10(c, k, o);
    CHECK(o[0] == 0x408f276du && o[1] == 0x41c83b0eu && o[2] == 0xa20bc7c6u && o[3] == 0x6d5451fdu); }
  { uint32_t c[4] = {0x243f6a88u, 0x85a308d3u, 0x13198a2eu, 0x03707344u}, k[2] = {0xa4093822u, 0x299f31d0u}; philox4x32_10(c, k, o);
    CHECK(o[0] == 0xd16cfe09u && o[1] == 0x94fdccebu && o[2] == 0x5001e420u && o[3] == 0x24126ea1u); }
  // address map: distinct fields give distinct values; u in [0,1)
  Address a; a.seed = 7; a.role = R_POST; a.xph = X_POST; a.stage = 3; a.particle = 11; a.slot = 2;
  double u = uniform_at(a); CHECK(u >= 0 && u < 1);
  Address b = a; b.slot = 3; CHECK(uniform_at(b) != u);
  Address c2 = a; c2.role = R_TEST; CHECK(uniform_at(c2) != u);
  Address bad = a; bad.island = 1u << 20; CHECK_THROWS(uniform_at(bad));
}

TEST(container_roundtrip_and_corruption) {
  std::string p = tmpdir() + "/wp5_container_" + std::to_string(getpid()) + ".bin";
  std::vector<double> x = {1.5, -2.25, 3e300};
  std::vector<int32_t> ix = {3, 1, 4, 1, 5, 9};
  BinWriter W(K_LAW, M_V);
  W.add_vec("x", DT_F64, x);
  W.add("ix2", DT_I32, ix.data(), ix.size() * 4, 2, 2, 3);
  W.add_json("meta", "{\"a\":1}");
  CHECK_THROWS(W.add_vec("x", DT_F64, x));
  std::string h = W.write(p);
  {
    BinReader R(p);
    CHECK(R.content_hash() == h);
    CHECK(R.header().kind == K_LAW && R.header().mode == M_V && R.header().n_sections == 3);
    uint64_t c; const double* px = R.ptr<double>("x", DT_F64, &c);
    CHECK(c == 3 && px[2] == 3e300);
    CHECK(R.entry("ix2").ndim == 2 && R.entry("ix2").dims[1] == 3);
    CHECK(R.entry("x").offset % 64 == 0 && R.entry("ix2").offset % 64 == 0);
    CHECK(R.json("meta") == "{\"a\":1}");
    CHECK_THROWS(R.ptr<int32_t>("x", DT_I32));
    CHECK_THROWS(R.entry("nope"));
  }
  // flip one byte inside section x → hash mismatch
  {
    BinReader R(p); uint64_t off = R.entry("x").offset;
    std::fstream f(p, std::ios::in | std::ios::out | std::ios::binary);
    f.seekp((std::streamoff)off + 1); char ch = 0x55; f.write(&ch, 1);
  }
  CHECK_THROWS(BinReader R(p));
  BinReader R2(p, false);   // without section verification the table still checks out
  CHECK(R2.has("x"));
  std::remove(p.c_str());
}

TEST(json_roundtrip) {
  Json j = Json::parse(R"({"a": [1, 2.5, -3e-7, null], "b": {"c": "x\"y\n", "d": true}, "e": 12345678901})");
  CHECK(j.at("a").size() == 4 && j.at("a")[1].num() == 2.5 && j.at("a")[3].is_null());
  CHECK(j.at("b").at("c").str() == "x\"y\n" && j.at("b").at("d").boolean());
  CHECK(j.at("e").num() == 12345678901.0);
  Json k = Json::parse(j.dump(2));
  CHECK(k.dump() == j.dump());
  Json n = Json::object(); n.set("nan", NAN); n.set("v", 0.1);
  CHECK(Json::parse(n.dump()).at("nan").is_null());
  CHECK(Json::parse(n.dump()).at("v").num() == 0.1);
  CHECK_THROWS(Json::parse("{\"a\":1,}x"));
}
