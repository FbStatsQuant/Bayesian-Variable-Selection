// wp4_terminal.h -- WP4 reader of the terminal supports of island_r.bin, in WP3's layout (PR #21,
// include/v4/island/island_file.h): terminal_S_ptr i64 [N + 1], terminal_S i32 [ptr[N]] -- the N particles' supports
// after the LAST measured round, in particle order (manager, 2026-11-15); absent unless the island completed.
// Validated here, before any read: N + 1 entries, ptr[0] = 0, non-decreasing, each <= the pool size, ptr[N] = pool size;
// then each support sorted, unique, < p.
#pragma once
#include <string>
#include <vector>
#include "v4/format.h"
#include "v4/model.h"
#include "v4/status.h"

namespace v4::merge {
inline std::vector<Model> read_terminal_supports(const fmt::Reader& R, int32_t N, int32_t p) {
  std::vector<Model> out;
  if (!R.has("terminal_S_ptr")) return out;
  uint64_t np = 0, ni = 0;
  const int64_t* ptr = R.get<int64_t>("terminal_S_ptr", &np);
  const int32_t* idx = R.get<int32_t>("terminal_S", &ni);
  if (np != (uint64_t)N + 1 || ptr[0] != 0 || (uint64_t)ptr[np - 1] != ni)
    throw Error(Status::invalid_input, "terminal_S: expected N + 1 = " + std::to_string(N + 1) + " offsets covering the pool");
  out.reserve((size_t)N);
  for (uint64_t i = 0; i < (uint64_t)N; ++i)   // validate every offset before any read (review PR16 re-check m-1)
    if (ptr[i + 1] < ptr[i] || (uint64_t)ptr[i + 1] > ni) throw Error(Status::invalid_input, "terminal_S: offsets not monotone or past the pool");
  for (uint64_t i = 0; i < (uint64_t)N; ++i) {
    Model S(idx + ptr[i], idx + ptr[i + 1]);
    for (size_t a = 0; a < S.size(); ++a)
      if (S[a] < 0 || S[a] >= p || (a && S[a] <= S[a - 1])) throw Error(Status::invalid_input, "terminal_S: support not sorted / unique / in range");
    out.push_back(std::move(S));
  }
  return out;
}
}  // namespace v4::merge
