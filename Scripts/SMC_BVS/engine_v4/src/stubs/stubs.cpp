// stubs.cpp -- placeholders for WP2-WP5 entry points (see include/v4/stubs.h). Each returns nothing and throws.
#include "v4/stubs.h"
#include "v4/status.h"

namespace v4 {
#define V4_STUB(ns, wp) namespace ns { Json run(const Json&) { throw Error(Status::internal_error, #ns ": not implemented (" wp ")"); } }
V4_STUB(setup, "WP2")
V4_STUB(island, "WP3")
V4_STUB(calib, "WP4")
V4_STUB(eval, "WP5")
V4_STUB(post, "WP5")
#undef V4_STUB
}  // namespace v4
