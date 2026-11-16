// island_lm_state.h -- the label-major group state (owned with island_lm.h; WP3_ARCH_REVIEW §4). A namespace-scope type
// so that the engine (island_run.h) can hold it as a member while the label-major code lives in island_lm.h.
#pragma once
#include <atomic>
#include "v4/island/island.h"

namespace v4::island {

// --- label-major round for the particles [g0, g0 + gN) ------------------------------------------------------
struct LmGroupBuf {
  std::vector<uint32_t> ord, inv;             // gN x m
  std::vector<std::vector<std::pair<uint32_t, int>>> ng;   // per particle: (position, label) of U/N/I labels, sorted
  std::vector<uint32_t> q, e; std::vector<uint8_t> done, etype; std::vector<Particle> pending;
  std::vector<std::atomic<uint32_t>> fmin;
  std::vector<SupportCache> sup; std::vector<int> sup_of;
  std::vector<std::vector<int>> sup_parts;     // particles (group-local, ascending) per support
  std::vector<int> act;                        // active columns
  avec<double> XA;                             // |act| x n
  std::vector<double> lbuf, obuf;              // nsup x p
};

}  // namespace v4::island
