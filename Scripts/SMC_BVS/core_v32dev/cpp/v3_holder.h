#pragma once
#include <memory>
#include "v3_engine.h"
// One holder type for contexts, starts and setups; pieces not yet built are empty.
struct Holder {
  std::shared_ptr<v3::Data> D;
  std::shared_ptr<v3::Start> st;
  std::vector<std::vector<int>> Nb;
  int B = 0;
  bool has_start = false, has_graph = false;
  double table_seconds = 0, block_seconds = 0, start_seconds = 0, graph_seconds = 0;
  // v3.2-dev (B4): the start mode start_mode(st, 1e6, tie_dp) is a deterministic function of the setup; it is computed
  // once per tie rule and reused by the post-setup LS0 preflight and by LS0 itself (same call, same result).
  std::shared_ptr<v3::ModeResult> mode[2];
  const v3::ModeResult& start_mode_cached(bool tie_dp) {
    int i = tie_dp ? 1 : 0;
    if (!mode[i]) mode[i] = std::make_shared<v3::ModeResult>(v3::start_mode(*st, 1000000, tie_dp));
    return *mode[i];
  }
};
