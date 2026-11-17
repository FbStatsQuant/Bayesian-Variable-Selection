// cmd_args.h -- input paths of a command from the driver's manifest or the explicit arguments (INTERFACES §1, §5.3; the
// rule of WP4's merge, review PR20 re-check n-3). The CLI copies the manifest's `params` into the arguments and keeps the
// parsed manifest under args["manifest"]. An input is found by base name among the manifest's `inputs` (their keys are
// paths); with a manifest, the manifest is the authority: an explicit argument that names another path is refused
// (invalid_input), in either argument order. Used by `calibrate` and `island` (v4_cmd).
#pragma once
#include <string>
#include "v4/json.h"
#include "v4/status.h"

namespace v4::cmd {

inline std::string base_name(const std::string& p) { size_t k = p.find_last_of('/'); return k == std::string::npos ? p : p.substr(k + 1); }

// the parsed manifest (an object; empty when none was given)
inline Json manifest_of(const Json& args, const std::string& cmd) {
  if (!args.contains("manifest")) return Json::object();
  const Json& m = args.at("manifest");
  Json M = m.type() == Json::STR ? read_json_file(m.str()) : m;
  if (M.type() != Json::OBJ) throw Error(Status::invalid_input, cmd + ": --manifest is not a JSON object");
  if (M.contains("command") && (M.at("command").type() != Json::STR || M.at("command").str() != cmd))
    throw Error(Status::invalid_input, cmd + ": the manifest is not a " + cmd + " manifest (command)");
  return M;
}

// the path of input `name` (e.g. "data.bin"): --key, or the manifest input with that base name; "" if neither and not
// required
inline std::string input_path(const Json& args, const Json& manifest, const char* key, const std::string& name, const std::string& cmd, bool required) {
  std::string f;
  if (manifest.contains("inputs"))
    for (auto& [k, v] : manifest.at("inputs").items()) if (base_name(k) == name) {
      if (!f.empty()) throw Error(Status::invalid_input, cmd + ": the manifest's inputs name " + name + " twice");
      f = k;
    }
  std::string a;
  if (args.contains(key)) {
    if (args.at(key).type() != Json::STR) throw Error(Status::invalid_input, cmd + ": --" + key + " must be a path");
    a = args.at(key).str();
  }
  if (!a.empty() && !f.empty() && a != f) throw Error(Status::invalid_input, cmd + ": --" + key + " differs from the manifest's " + name);
  if (required && a.empty() && f.empty()) throw Error(Status::invalid_input, cmd + ": no " + name + " (give --" + key + " or a manifest input)");
  return a.empty() ? f : a;
}

}  // namespace v4::cmd
