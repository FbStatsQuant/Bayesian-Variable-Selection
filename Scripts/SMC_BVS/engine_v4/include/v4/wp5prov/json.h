// wp5prov/json.h -- minimal JSON value, parser and writer used by WP5 (eval/post records, truth.json, manifests).
// PROVISIONAL location: if WP1 delivers a JSON helper with records.h, WP5 switches to it.
// Objects keep insertion order (stable record layout). Numbers are doubles, written with %.17g; NaN/Inf are written as null.
#pragma once
#include <cstdint>
#include <memory>
#include <string>
#include <utility>
#include <vector>

namespace v4::wp5prov {

class Json {
 public:
  enum Type { Null, Bool, Num, Str, Arr, Obj };
  Json() = default;
  Json(std::nullptr_t) {}
  Json(bool b) : t_(Bool), b_(b) {}
  Json(double d) : t_(Num), d_(d) {}
  Json(int v) : t_(Num), d_(v) {}
  Json(int64_t v) : t_(Num), d_((double)v) {}
  Json(uint64_t v) : t_(Num), d_((double)v) {}
  Json(uint32_t v) : t_(Num), d_(v) {}
  Json(const char* s) : t_(Str), s_(s) {}
  Json(std::string s) : t_(Str), s_(std::move(s)) {}
  static Json array() { Json j; j.t_ = Arr; return j; }
  static Json object() { Json j; j.t_ = Obj; return j; }
  template <class T> static Json array_of(const std::vector<T>& v) { Json j = array(); for (auto& x : v) j.push(Json(x)); return j; }

  Type type() const { return t_; }
  bool is_null() const { return t_ == Null; }
  bool is_num() const { return t_ == Num; }
  bool is_str() const { return t_ == Str; }
  bool is_arr() const { return t_ == Arr; }
  bool is_obj() const { return t_ == Obj; }
  double num() const;
  bool boolean() const;
  const std::string& str() const;
  size_t size() const { return t_ == Arr ? a_.size() : (t_ == Obj ? o_.size() : 0); }
  const Json& operator[](size_t i) const;
  Json& push(Json v);
  // object access
  bool has(const std::string& k) const;
  const Json& at(const std::string& k) const;            // throws if missing
  const Json* find(const std::string& k) const;          // nullptr if missing
  Json& set(const std::string& k, Json v);               // insert or replace (keeps first position)
  const std::vector<std::pair<std::string, Json>>& items() const { return o_; }
  double num_or(const std::string& k, double dflt) const { const Json* p = find(k); return (p && p->is_num()) ? p->d_ : dflt; }
  std::string str_or(const std::string& k, const std::string& dflt) const { const Json* p = find(k); return (p && p->is_str()) ? p->s_ : dflt; }
  std::vector<double> num_array() const;

  std::string dump(int indent = -1) const;
  static Json parse(const std::string& text);            // throws Error(invalid_input)
  static Json parse_file(const std::string& path);

 private:
  Type t_ = Null; bool b_ = false; double d_ = 0; std::string s_;
  std::vector<Json> a_; std::vector<std::pair<std::string, Json>> o_;
  void dump_to(std::string& out, int indent, int level) const;
  friend struct JsonParser;
};

void write_text_atomic(const std::string& path, const std::string& text);   // tmp + fsync + rename

}  // namespace v4::wp5prov
