// json.cpp -- minimal JSON (RFC 8259 subset: no \u surrogate pairs beyond the BMP needed by our files).
#include "v4/json.h"
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <unistd.h>
#include "v4/status.h"

namespace v4 {

Json::Json(uint64_t v) : t_(NUM), d_((double)v) {
  if (v > 9007199254740992ULL) throw Error(Status::internal_error, "json: u64 above 2^53 must be written as a hex string");
}
Json& Json::operator[](const std::string& k) {
  if (t_ == NUL) t_ = OBJ;
  if (t_ != OBJ) throw Error(Status::internal_error, "json: not an object");
  return o_[k];
}
const Json& Json::at(const std::string& k) const {
  if (t_ != OBJ) throw Error(Status::invalid_input, "json: not an object (key " + k + ")");
  auto it = o_.find(k);
  if (it == o_.end()) throw Error(Status::invalid_input, "json: missing key " + k);
  return it->second;
}
const Json& Json::at(size_t i) const {
  if (t_ != ARR || i >= a_.size()) throw Error(Status::invalid_input, "json: bad array index");
  return a_[i];
}
void Json::push(Json v) {
  if (t_ == NUL) t_ = ARR;
  if (t_ != ARR) throw Error(Status::internal_error, "json: not an array");
  a_.push_back(std::move(v));
}
double Json::num() const { if (t_ != NUM) throw Error(Status::invalid_input, "json: not a number"); return d_; }
int64_t Json::i64() const {
  double d = num();
  if (d != std::floor(d) || std::fabs(d) > 9007199254740992.0) throw Error(Status::invalid_input, "json: not an integer");
  return (int64_t)d;
}
bool Json::boolean() const { if (t_ != BOOL) throw Error(Status::invalid_input, "json: not a bool"); return b_; }
const std::string& Json::str() const { if (t_ != STR) throw Error(Status::invalid_input, "json: not a string"); return s_; }

static void dump_str(std::string& out, const std::string& s) {
  out += '"';
  for (unsigned char c : s) {
    switch (c) {
      case '"': out += "\\\""; break; case '\\': out += "\\\\"; break; case '\n': out += "\\n"; break;
      case '\r': out += "\\r"; break; case '\t': out += "\\t"; break;
      default:
        if (c < 0x20) { char b[8]; std::snprintf(b, sizeof b, "\\u%04x", c); out += b; } else out += (char)c;
    }
  }
  out += '"';
}
void Json::dump_to(std::string& out, int indent, int depth) const {
  auto nl = [&](int d) { if (indent >= 0) { out += '\n'; out.append((size_t)(indent * d), ' '); } };
  switch (t_) {
    case NUL: out += "null"; break;
    case BOOL: out += b_ ? "true" : "false"; break;
    case NUM: {
      if (!std::isfinite(d_)) { out += std::isnan(d_) ? "\"NaN\"" : (d_ > 0 ? "\"Inf\"" : "\"-Inf\""); break; }
      char b[40];
      if (d_ == std::floor(d_) && std::fabs(d_) < 9007199254740992.0) std::snprintf(b, sizeof b, "%lld", (long long)d_);
      else std::snprintf(b, sizeof b, "%.17g", d_);
      out += b; break;
    }
    case STR: dump_str(out, s_); break;
    case ARR: {
      out += '['; bool first = true;
      for (auto& v : a_) {
        if (!first) out += ',';
        first = false; nl(depth + 1); v.dump_to(out, indent, depth + 1);
      }
      if (!a_.empty()) nl(depth);
      out += ']'; break;
    }
    case OBJ: {
      out += '{'; bool first = true;
      for (auto& [k, v] : o_) {
        if (!first) out += ',';
        first = false; nl(depth + 1);
        dump_str(out, k); out += indent >= 0 ? ": " : ":"; v.dump_to(out, indent, depth + 1);
      }
      if (!o_.empty()) nl(depth);
      out += '}'; break;
    }
  }
}
std::string Json::dump(int indent) const { std::string s; dump_to(s, indent, 0); return s; }

namespace {
struct Parser {
  const std::string& s; size_t i = 0;
  [[noreturn]] void fail(const char* m) { throw Error(Status::invalid_input, std::string("json parse: ") + m + " at " + std::to_string(i)); }
  void ws() { while (i < s.size() && (s[i] == ' ' || s[i] == '\n' || s[i] == '\r' || s[i] == '\t')) ++i; }
  Json value() {
    ws(); if (i >= s.size()) fail("unexpected end");
    char c = s[i];
    if (c == '{') {
      ++i; Json o = Json::object(); ws();
      if (i < s.size() && s[i] == '}') { ++i; return o; }
      while (true) {
        ws(); if (i >= s.size() || s[i] != '"') fail("expected key");
        std::string k = string(); ws();
        if (i >= s.size() || s[i] != ':') fail("expected :");
        ++i;
        o[k] = value(); ws();
        if (i < s.size() && s[i] == ',') { ++i; continue; }
        if (i < s.size() && s[i] == '}') { ++i; return o; }
        fail("expected , or }");
      }
    }
    if (c == '[') {
      ++i; Json a = Json::array(); ws();
      if (i < s.size() && s[i] == ']') { ++i; return a; }
      while (true) {
        a.push(value()); ws();
        if (i < s.size() && s[i] == ',') { ++i; continue; }
        if (i < s.size() && s[i] == ']') { ++i; return a; }
        fail("expected , or ]");
      }
    }
    if (c == '"') return Json(string());
    if (s.compare(i, 4, "true") == 0) { i += 4; return Json(true); }
    if (s.compare(i, 5, "false") == 0) { i += 5; return Json(false); }
    if (s.compare(i, 4, "null") == 0) { i += 4; return Json(); }
    const char* b = s.c_str() + i; char* e = nullptr;
    double d = std::strtod(b, &e);
    if (e == b) fail("bad value");
    i += (size_t)(e - b);
    return Json(d);
  }
  std::string string() {
    ++i; std::string out;
    while (i < s.size() && s[i] != '"') {
      char c = s[i++];
      if (c != '\\') { out += c; continue; }
      if (i >= s.size()) fail("bad escape");
      char e = s[i++];
      switch (e) {
        case '"': out += '"'; break; case '\\': out += '\\'; break; case '/': out += '/'; break;
        case 'n': out += '\n'; break; case 'r': out += '\r'; break; case 't': out += '\t'; break;
        case 'b': out += '\b'; break; case 'f': out += '\f'; break;
        case 'u': {
          if (i + 4 > s.size()) fail("bad \\u");
          unsigned cp = (unsigned)std::stoul(s.substr(i, 4), nullptr, 16); i += 4;
          if (cp < 0x80) out += (char)cp;
          else if (cp < 0x800) { out += (char)(0xC0 | (cp >> 6)); out += (char)(0x80 | (cp & 0x3F)); }
          else { out += (char)(0xE0 | (cp >> 12)); out += (char)(0x80 | ((cp >> 6) & 0x3F)); out += (char)(0x80 | (cp & 0x3F)); }
          break;
        }
        default: fail("bad escape");
      }
    }
    if (i >= s.size()) fail("unterminated string");
    ++i; return out;
  }
};
}  // namespace

Json Json::parse(const std::string& text) {
  Parser p{text};
  Json v = p.value(); p.ws();
  if (p.i != text.size()) p.fail("trailing characters");
  return v;
}
Json read_json_file(const std::string& path) {
  std::ifstream f(path);
  if (!f) throw Error(Status::invalid_input, "cannot open " + path);
  std::stringstream b; b << f.rdbuf();
  return Json::parse(b.str());
}
void write_json_file(const std::string& path, const Json& j) {
  std::string tmp = path + ".tmp." + std::to_string(::getpid());
  { std::ofstream f(tmp); if (!f) throw Error(Status::io_error, "cannot write " + tmp); f << j.dump(2) << '\n'; if (!f) throw Error(Status::io_error, "write failed " + tmp); }
  if (std::rename(tmp.c_str(), path.c_str()) != 0) throw Error(Status::io_error, "rename failed " + path);
}
}  // namespace v4
