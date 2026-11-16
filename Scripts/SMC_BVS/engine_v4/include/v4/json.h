// json.h -- a minimal JSON value, parser and writer for manifests, `meta` sections and records (INTERFACES §5).
// Objects keep keys sorted (std::map), so the serialised text of a value is canonical (stable hashes).
#pragma once
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

namespace v4 {
class Json {
 public:
  enum Type { NUL, BOOL, NUM, STR, ARR, OBJ };
  Json() : t_(NUL) {}
  Json(std::nullptr_t) : t_(NUL) {}
  Json(bool b) : t_(BOOL), b_(b) {}
  Json(double d) : t_(NUM), d_(d) {}
  Json(int v) : t_(NUM), d_(v) {}
  Json(int64_t v) : t_(NUM), d_((double)v) {}
  Json(uint64_t v);   // throws internal_error above 2^53: write such values with hex64() (INTERFACES §5.1)
  Json(uint32_t v) : t_(NUM), d_(v) {}
  Json(const char* s) : t_(STR), s_(s) {}
  Json(std::string s) : t_(STR), s_(std::move(s)) {}
  static Json array() { Json j; j.t_ = ARR; return j; }
  static Json object() { Json j; j.t_ = OBJ; return j; }
  template <class T> static Json array_of(const std::vector<T>& v) { Json j = array(); for (auto& x : v) j.push(Json(x)); return j; }
  Type type() const { return t_; }
  bool is_null() const { return t_ == NUL; }
  bool contains(const std::string& k) const { return t_ == OBJ && o_.count(k); }
  Json& operator[](const std::string& k);               // creates (object)
  const Json& at(const std::string& k) const;            // throws invalid_input if missing
  const Json& at(size_t i) const;
  void push(Json v);
  size_t size() const { return t_ == ARR ? a_.size() : (t_ == OBJ ? o_.size() : 0); }
  double num() const; int64_t i64() const; bool boolean() const; const std::string& str() const;
  const std::map<std::string, Json>& items() const { return o_; }
  const std::vector<Json>& elems() const { return a_; }
  std::string dump(int indent = -1) const;                // -1: compact
  static Json parse(const std::string& text);             // throws Error(invalid_input)
 private:
  Type t_; bool b_ = false; double d_ = 0; std::string s_;
  std::vector<Json> a_; std::map<std::string, Json> o_;
  void dump_to(std::string& out, int indent, int depth) const;
};
Json read_json_file(const std::string& path);
void write_json_file(const std::string& path, const Json& j);   // temporary name + rename
}  // namespace v4
