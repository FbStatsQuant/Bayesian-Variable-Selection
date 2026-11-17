// island_file.h -- island_r.bin (INTERFACES §5.1, kind 5; WP3 owns it, manager Q8).
//
// Sections (names fixed; WPs may add, never rename):
//   meta                 json: schema, kind, mode, r, N, T, L, Hm, p, status, reason, tier, inputs, binary, timings,
//                        logZ_hex (the bits of log Z), init_hash (hex); cost: the D-30 per-step execution record
//                        (schema smcbvs4.cost/1, header + one column per StepCost field; not hashed; WP7 O2)
//   logZ                 f64 [1]            log Ẑ_r (bits)
//   grid                 f64 [T+1]          the schedule used
//   st_phi st_inc st_ess st_cum             f64 [T]
//   st_distinct_res st_distinct_moved       i32 [T]
//   st_moves             u64 [T x 12]       MoveStats per bridge stage (records.h field order)
//   term_moves           u64 [(L+Hm) x 12]  burn-in rounds then measured rounds
//   term_distinct        i32 [L+Hm]
//   rb_acc pip_r         f64 [p]
//   rb_round             f64 [Hm x p]
//   top_v top_hash top_off top_len top_pool f64 / u64 / u64 / u16 / i32: the island store, compacted, sorted (HPM order)
//   hpm_S                i32 [k]
//   hpm_val              f64 [2]            F, log m
//   hpm_ev               i64 [12]           seg, tier, iter, unit, xph, stage, round, particle, position, sub, phase, mech
//   island_best          f64 [r + 1]        entry r = this island's maximum (others -inf), as Ledger::island_best
//   logical              u64 [N_PHASE x N_MECH]
//   terminal_S_ptr       i64 [N + 1]        terminal supports: the N particles' supports after the LAST measured
//   terminal_S           i32 [ptr[N]]        round, in particle order (manager 11-15; WP4 merge: Ẑ_occ, D-13, occupancy)
// No estimate section (logZ, rb_*, pip_r, terminal_S*) is written unless status = completed (GUARD-W).
#pragma once
#include <string>
#include "v4/island/island.h"
#include "v4/json.h"
#include "v4/records.h"

namespace v4::island {

constexpr int MOVE_FIELDS = 12;   // records.h MoveStats

// Writes island_r.bin (temporary name, fsync, rename; WP1 fmt::Writer). `inputs` = content hashes of data/setup/calib.
// Returns the file's content hash (hex).
std::string write_island_file(const std::string& path, const IslandRun& r, Arith arith, const Json& inputs);

struct IslandFile {
  v4::IslandResult rec;            // INTERFACES §5.2 record (Ledger with the store, HPM + provenance, counters)
  std::vector<Model> terminal;     // N supports after the last measured round (empty unless completed)
  std::vector<double> grid;
  Json meta;
  std::string content_hash;
};
IslandFile read_island_file(const std::string& path, bool verify = true);

}  // namespace v4::island
