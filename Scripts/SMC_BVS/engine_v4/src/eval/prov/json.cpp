// json.cpp -- minimal JSON (see include/v4/wp5prov/json.h).
#include "v4/wp5prov/json.h"

#include <fcntl.h>
#include <unistd.h>

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <sstream>

#include "v4/wp5prov/prov.h"

namespace v4::wp5prov {

static Error jerr(const std::string& m) { return Error(Status::invalid_input, "json: " + m); }

double Json::num() const { if (t_ != Num) throw jerr("not a number"); return d_; }
bool Json::boolean() const { if (t_ != Bool) throw jerr("not a boolean"); return b_; }
const std::string& Json::str() const { if (t_ != Str) throw jerr("not a string"); return s_; }
const Json& Json::operator[](size_t i) const { if (t_ != Arr || i >= a_.size()) throw jerr("bad array index"); return a_[i]; }
Json& Json::push(Json v) { if (t_ == Null) t_ = Arr; if (t_ != Arr) throw jerr("push on non-array"); a_.push_back(std::move(v)); return a_.back(); }
bool Json::has(const std::string& k) const { return find(k) != nullptr; }
const Json* Json::find(const std::string& k) const {
  if (t_ != Obj) return nullptr;
  for (auto& kv : o_) if (kv.first == k) return &kv.second;
  return nullptr;
}
const Json& Json::at(const std::string& k) const { const Json* p = find(k); if (!p) throw jerr("missing key '" + k + "'"); return *p; }
Json& Json::set(const std::string& k, Json v) {
  if (t_ == Null) t_ = Obj;
  if (t_ != Obj) throw jerr("set on non-object");
  for (auto& kv : o_) if (kv.first == k) { kv.second = std::move(v); return kv.second; }
  o_.emplace_back(k, std::move(v)); return o_.back().second;
}
std::vector<double> Json::num_array() const {
  if (t_ != Arr) throw jerr("not an array");
  std::vector<double> v; v.reserve(a_.size());
  for (auto& x : a_) v.push_back(x.is_null() ? NAN : x.num());
  return v;
}

static void esc(std::string& out, const std::string& s) {
  out += '"';
  for (unsigned char c : s) {
    switch (c) {
      case '"': out += "\\\""; break;
      case '\\': out += "\\\\"; break;
      case '\n': out += "\\n"; break;
      case '\t': out += "\\t"; break;
      case '\r': out += "\\r"; break;
      default:
        if (c < 0x20) { char b[8]; std::snprintf(b, sizeof b, "\\u%04x", c); out += b; }
        else out += (char)c;
    }
  }
  out += '"';
}
void Json::dump_to(std::string& out, int indent, int level) const {
  auto nl = [&](int l) { if (indent >= 0) { out += '\n'; out.append((size_t)(indent * l), ' '); } };
  switch (t_) {
    case Null: out += "null"; break;
    case Bool: out += b_ ? "true" : "false"; break;
    case Num: {
      if (!std::isfinite(d_)) { out += "null"; break; }
      char b[40];
      if (d_ == std::floor(d_) && std::fabs(d_) < 9.007199254740992e15) std::snprintf(b, sizeof b, "%.0f", d_);
      else std::snprintf(b, sizeof b, "%.17g", d_);
      out += b; break;
    }
    case Str: esc(out, s_); break;
    case Arr: {
      out += '[';
      bool flat = true; for (auto& x : a_) if (x.t_ == Arr || x.t_ == Obj) flat = false;
      for (size_t i = 0; i < a_.size(); ++i) {
        if (i) out += ',';
        if (!flat) nl(level + 1); else if (i && indent >= 0) out += ' ';
        a_[i].dump_to(out, indent, level + 1);
      }
      if (!flat && !a_.empty()) nl(level);
      out += ']'; break;
    }
    case Obj: {
      out += '{';
      for (size_t i = 0; i < o_.size(); ++i) {
        if (i) out += ',';
        nl(level + 1); esc(out, o_[i].first); out += indent >= 0 ? ": " : ":";
        o_[i].second.dump_to(out, indent, level + 1);
      }
      if (!o_.empty()) nl(level);
      out += '}'; break;
    }
  }
}
std::string Json::dump(int indent) const { std::string s; dump_to(s, indent, 0); return s; }

struct JsonParser {
  const std::string& s; size_t i = 0;
  explicit JsonParser(const std::string& t) : s(t) {}
  void ws() { while (i < s.size() && (s[i] == ' ' || s[i] == '\n' || s[i] == '\t' || s[i] == '\r')) ++i; }
  char peek() { ws(); if (i >= s.size()) throw jerr("unexpected end"); return s[i]; }
  void expect(char c) { if (peek() != c) throw jerr(std::string("expected '") + c + "' at " + std::to_string(i)); ++i; }
  std::string str() {
    expect('"'); std::string o;
    while (true) {
      if (i >= s.size()) throw jerr("unterminated string");
      char c = s[i++];
      if (c == '"') break;
      if (c != '\\') { o += c; continue; }
      if (i >= s.size()) throw jerr("bad escape");
      char e = s[i++];
      switch (e) {
        case '"': o += '"'; break; case '\\': o += '\\'; break; case '/': o += '/'; break;
        case 'b': o += '\b'; break; case 'f': o += '\f'; break; case 'n': o += '\n'; break;
        case 'r': o += '\r'; break; case 't': o += '\t'; break;
        case 'u': {
          if (i + 4 > s.size()) throw jerr("bad \\u");
          unsigned cp = (unsigned)std::stoul(s.substr(i, 4), nullptr, 16); i += 4;
          if (cp < 0x80) o += (char)cp;
          else if (cp < 0x800) { o += (char)(0xC0 | (cp >> 6)); o += (char)(0x80 | (cp & 0x3F)); }
          else { o += (char)(0xE0 | (cp >> 12)); o += (char)(0x80 | ((cp >> 6) & 0x3F)); o += (char)(0x80 | (cp & 0x3F)); }
          break;
        }
        default: throw jerr("bad escape");
      }
    }
    return o;
  }
  Json value() {
    char c = peek();
    if (c == '{') {
      ++i; Json o = Json::object();
      if (peek() == '}') { ++i; return o; }
      while (true) { std::string k = str(); expect(':'); o.set(k, value()); char d = peek(); ++i; if (d == '}') break; if (d != ',') throw jerr("expected , or }"); }
      return o;
    }
    if (c == '[') {
      ++i; Json a = Json::array();
      if (peek() == ']') { ++i; return a; }
      while (true) { a.push(value()); char d = peek(); ++i; if (d == ']') break; if (d != ',') throw jerr("expected , or ]"); }
      return a;
    }
    if (c == '"') return Json(str());
    if (s.compare(i, 4, "true") == 0) { i += 4; return Json(true); }
    if (s.compare(i, 5, "false") == 0) { i += 5; return Json(false); }
    if (s.compare(i, 4, "null") == 0) { i += 4; return Json(); }
    const char* b = s.c_str() + i; char* e = nullptr;
    double d = std::strtod(b, &e);
    if (e == b) throw jerr("bad token at " + std::to_string(i));
    i += (size_t)(e - b);
    return Json(d);
  }
};
Json Json::parse(const std::string& text) {
  JsonParser P(text); Json v = P.value(); P.ws();
  if (P.i != text.size()) throw jerr("trailing characters");
  return v;
}
Json Json::parse_file(const std::string& path) {
  std::ifstream f(path, std::ios::binary);
  if (!f) throw Error(Status::invalid_input, "cannot open " + path);
  std::stringstream ss; ss << f.rdbuf();
  return parse(ss.str());
}
void write_text_atomic(const std::string& path, const std::string& text) {
  std::string tmp = path + ".tmp." + std::to_string(getpid());
  int fd = ::open(tmp.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
  if (fd < 0) throw Error(Status::io_error, "cannot create " + tmp);
  const char* p = text.data(); size_t n = text.size();
  while (n) { ssize_t w = ::write(fd, p, n); if (w <= 0) { ::close(fd); throw Error(Status::io_error, "write failed " + tmp); } p += w; n -= (size_t)w; }
  if (::fsync(fd) != 0 || ::close(fd) != 0) throw Error(Status::io_error, "fsync failed " + tmp);
  if (std::rename(tmp.c_str(), path.c_str()) != 0) throw Error(Status::io_error, "rename failed " + path);
}

}  // namespace v4::wp5prov
