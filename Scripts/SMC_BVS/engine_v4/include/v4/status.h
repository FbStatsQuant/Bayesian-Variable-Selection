// status.h -- task / fit statuses and the engine's exception types (INTERFACES §7; ENGINEERING_SPEC §6).
#pragma once
#include <cstdint>
#include <stdexcept>
#include <string>
#include <vector>

namespace v4 {

// schedule_limit (v0.1.7): theory / compat calibration only -- tier-1 grid construction failed and no fallback grid
// exists (core/v3_calib.R:170). It cannot arise in V-1M (D-26).
enum class Status : uint8_t { completed = 0, resource_limit = 1, numerical_failure = 2, invalid_input = 3, io_error = 4, internal_error = 5,
                              schedule_limit = 6 };

const char* status_name(Status s);
Status status_from_name(const std::string& s);   // throws Error(invalid_input) on an unknown name
inline int exit_code(Status s) { return s == Status::completed ? 0 : 10 + (int)s; }

struct Error : public std::runtime_error {
  Status st;
  Error(Status s, const std::string& m) : std::runtime_error(std::string(status_name(s)) + ": " + m), st(s) {}
};
// Thrown when a score fails after every fallback (core/cpp/v3_util.h:26-28 semantics; M §6.13).
struct NumericalFailure : public Error {
  explicit NumericalFailure(const std::string& m) : Error(Status::numerical_failure, m) {}
};

// Fit level: the first that applies in the order invalid_input, internal_error, numerical_failure, resource_limit,
// schedule_limit, io_error, completed (ENGINEERING_SPEC §6; schedule_limit added in v0.1.7). Empty input -> completed.
Status fit_status(const std::vector<Status>& tasks);

}  // namespace v4
