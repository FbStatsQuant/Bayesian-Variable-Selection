// stubs.h -- entry points of the other work packages. WP1 ships stubs that throw internal_error("not implemented"),
// so every WP links from day one; each WP replaces its stub (and deletes it from src/stubs/stubs.cpp).
#pragma once
#include "v4/json.h"

namespace v4 {
namespace setup { Json run(const Json& args); }    // WP2: data.bin -> setup.bin
namespace island { Json run(const Json& args); }   // WP3: data, setup, calib -> island_r.bin
namespace calib { Json run(const Json& args); }    // WP4: data, setup -> calib.bin
namespace merge { Json run(const Json& args); }    // WP4: islands -> fit.bin + fit.json
namespace eval { Json run(const Json& args); }     // WP5: fit, truth -> eval record
namespace post { Json run(const Json& args); }     // WP5: fit -> law.bin
}  // namespace v4
