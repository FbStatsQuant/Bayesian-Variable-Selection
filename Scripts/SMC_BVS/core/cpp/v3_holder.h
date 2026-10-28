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
};
