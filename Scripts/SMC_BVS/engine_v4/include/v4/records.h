// records.h -- in-memory records serialised into island / calib / fit files (INTERFACES §5.2). Owned by WP1 as a
// contract; WP3 (IslandResult), WP4 (CalibResult, FitResult) fill and serialise them.
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "v4/ledger.h"
#include "v4/status.h"

namespace v4 {
// core/cpp/v3_engine.h:25-29 (MoveStats), copied: per-stage acceptance counters.
struct MoveStats {
  uint64_t gibbs = 0, gibbs_change = 0, us_exec = 0, us_acc = 0, us_self = 0, ns_exec = 0, ns_acc = 0, ns_noscore = 0, ns_self = 0,
           in_exec = 0, in_acc = 0;
};
struct StageRow { double phi = 0, inc = 0, ess = 0, cum = 0; int32_t distinct_res = 0, distinct_moved = 0; MoveStats moves; };
struct Timings { double init = 0, bridge = 0, burn = 0, measured = 0, total = 0; };
struct IslandResult {
  Status status = Status::completed; int32_t r = 0, N = 0, T = 0, L = 0, Hm = 4; double logZ = 0;
  std::vector<StageRow> stages; std::vector<MoveStats> terminal_moves; std::vector<int32_t> terminal_distinct;
  std::vector<double> rb_acc, pip; std::vector<std::vector<double>> rb_round; Ledger led; Timings t;
  uint64_t init_hash = 0;
};
struct LocalArchive {   // core/cpp/v3_engine.h LocalArchive, flat
  Model centre; double centre_F = 0; std::vector<Model> path; std::vector<double> path_F;
  std::vector<Model> scanned; std::vector<double> scanned_F; std::vector<int32_t> scan_complete, scan_size;
  std::string termination; bool local_limit = false, local_certified = false; Model returned; double returned_F = 0;
  int32_t moves = 0; int64_t n_eval = 0;
};
enum CalibFlag : uint32_t { CF_GRID_FALLBACK = 1, CF_GRID_UNCONVERGED = 2, CF_ESCALATED = 4 };
struct CalibResult {
  Status status = Status::completed; int32_t tier = 0, N = 0, L = 0, I_used = 0; std::vector<double> grid;
  std::vector<std::vector<double>> grids_all; uint32_t flags = 0; std::vector<IslandResult> pilot_diag; Ledger led;
};
struct FitResult {
  Status status = Status::completed; int32_t Rp = 0; double logZ = 0; std::vector<double> logZ_r, pip_eq, pip_Z, pip_T;
  Model hpm, hpm_before_local, mpm, mode_S; double hpmF = 0; EventCtx hpm_ev; LocalArchive local, ls0; Store top; uint32_t flags = 0;
};
}  // namespace v4
