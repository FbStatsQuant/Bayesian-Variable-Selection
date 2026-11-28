#include "tk.h"
#include "v4/sha256.h"
#include "v4/json.h"
#include "v4/status.h"
using namespace v4;

TEST(sha256_nist_vectors) {
  CHECK(hex(sha256("", 0)) == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
  CHECK(hex(sha256("abc", 3)) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
  const char* m = "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq";
  CHECK(hex(sha256(m, std::strlen(m))) == "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1");
  std::string a(1000000, 'a');
  CHECK(hex(sha256(a.data(), a.size())) == "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0");
  Sha256 s; for (int i = 0; i < 1000; ++i) s.update(a.data(), 1000);   // streaming = one shot
  CHECK(hex(s.final()) == "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0");
}
TEST(json_roundtrip) {
  Json j = Json::object(); j["b"] = 1.5; j["a"] = "x\"y\n"; j["c"] = Json::array_of(std::vector<int>{1, 2, 3}); j["d"] = true; j["e"] = nullptr;
  j["big"] = (int64_t)123456789012345LL; j["f"] = 0.1;
  std::string t = j.dump();
  Json k = Json::parse(t);
  CHECK(k.dump() == t);
  CHECK(k.at("f").num() == 0.1);
  CHECK(k.at("big").i64() == 123456789012345LL);
  CHECK(t.find("\"a\"") < t.find("\"b\""));   // canonical key order
  CHECK_THROWS(Json::parse("{\"a\":}"));
  CHECK_THROWS(Json::parse("[1,2] x"));
}
TEST(status_precedence) {
  CHECK(fit_status({}) == Status::completed);
  CHECK(fit_status({Status::io_error, Status::resource_limit}) == Status::resource_limit);
  CHECK(fit_status({Status::completed, Status::numerical_failure, Status::internal_error}) == Status::internal_error);
  CHECK(fit_status({Status::internal_error, Status::invalid_input}) == Status::invalid_input);
  CHECK(exit_code(Status::completed) == 0 && exit_code(Status::io_error) == 14 && exit_code(Status::schedule_limit) == 16);
  CHECK(fit_status({Status::io_error, Status::schedule_limit}) == Status::schedule_limit);
  CHECK(fit_status({Status::schedule_limit, Status::resource_limit}) == Status::resource_limit);
  for (int i = 0; i <= 6; ++i) CHECK(status_from_name(status_name((Status)i)) == (Status)i);
}
