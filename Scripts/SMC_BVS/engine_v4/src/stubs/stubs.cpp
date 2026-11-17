// stubs.cpp -- placeholders for WP2-WP5 entry points (see include/v4/stubs.h). Each returns nothing and throws.
#include "v4/stubs.h"
#include "v4/status.h"

namespace v4 {
#define V4_STUB(ns, wp) namespace ns { Json run(const Json&) { throw Error(Status::internal_error, #ns ": not implemented (" wp ")"); } }
// (no stubs remain: setup is WP2 src/setup, island is WP3 src/island/island_cmd.cpp)
#undef V4_STUB
}  // namespace v4
