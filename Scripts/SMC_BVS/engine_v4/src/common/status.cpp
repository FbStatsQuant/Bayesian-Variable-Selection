// status.cpp -- status names and the fit-level precedence (ENGINEERING_SPEC §6).
#include "v4/status.h"

namespace v4 {
const char* status_name(Status s) {
  switch (s) {
    case Status::completed: return "completed";
    case Status::resource_limit: return "resource_limit";
    case Status::numerical_failure: return "numerical_failure";
    case Status::invalid_input: return "invalid_input";
    case Status::io_error: return "io_error";
    case Status::internal_error: return "internal_error";
    case Status::schedule_limit: return "schedule_limit";
  }
  return "internal_error";
}
Status status_from_name(const std::string& s) {
  for (int i = 0; i <= 6; ++i) if (s == status_name((Status)i)) return (Status)i;
  throw Error(Status::invalid_input, "unknown status " + s);
}
Status fit_status(const std::vector<Status>& tasks) {
  static const Status order[] = {Status::invalid_input, Status::internal_error, Status::numerical_failure, Status::resource_limit,
                                 Status::schedule_limit, Status::io_error};
  for (Status o : order) for (Status t : tasks) if (t == o) return o;
  return Status::completed;
}
}  // namespace v4
