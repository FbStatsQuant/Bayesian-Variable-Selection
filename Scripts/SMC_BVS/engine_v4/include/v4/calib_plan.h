// calib_plan.h -- the calibration island's memory plan and the live setup copy it counts (WP3; one definition for
// `calibrate`, the pilot tool v4_pilot_island and v4_plan_tables; review PR57 MAJOR-1, MINOR-2).
//
// The calibration island is planned as CalibIslandRunner admits it under WP4's N-1 rule (INTERFACES §7): the caller-supplied
// term of the island plan = the island's own setup inputs (mapped start-law sections + draw scratch + neighbour lists +
// fixed heap: start_inputs_bytes) + the live copy of setup.bin that WP4's reader keeps for the whole calibration (setup_view_bytes:
// logr and the partition, 12 p + 8 C + ...; the table stores are released once they are in the ledger) + the calibration's own
// resident state without the inputs (ledger + export). Admitted iff that plan <= --mem-budget.
#pragma once
#include "v4/calib.h"
#include "v4/calib_run.h"
#include "v4/format.h"
#include "v4/island/island.h"
#include "v4/island/setup_load.h"
#include "v4/wp4_io.h"

namespace v4::calib {

// `ip` at the G the budget allows, `ip1` at G = 1 (the admission floor). With the setup's dimensions (read_setup_dims or
// dims_from_sizes: nothing expanded) k = the q90 rule and both setup terms are counted; without them, sizes only (k = kbar,
// setup terms 0: an ESTIMATE floor).
struct IslandPlans { island::MemPlan ip, ip1; double setup_in = 0, setup_copy = 0; };

inline IslandPlans calib_island_plans(const Settings& s, Rule rule, uint32_t mode, int B, int K, int64_t n, int64_t p, uint64_t budget,
                                      uint64_t resident_own, const island::SetupDims* sd, double kbar, int G = 0) {
  island::IslandConfig ic; ic.role = island::IslandRole::Pilot; ic.island = 0; ic.leaders = true; ic.B = B; ic.G = G; ic.mem_budget = budget;   // G = 0: the largest that fits
  ic.N = 1; ic.Hm = 1;
  for (int e = 0; e < (rule == Rule::coded ? 2 : 1); ++e) { ic.N = std::max(ic.N, s.tiers[e].H); ic.Hm = std::max(ic.Hm, s.tiers[e].Hm); }
  ic.compat = mode == fmt::M_COMPAT; ic.threads = ic.compat ? 1 : s.threads;
  ic.kernel = mode == fmt::M_V ? island::KernelKind::LabelMajor : island::KernelKind::ParticleMajor;
  IslandPlans r;
  r.setup_in = sd ? island::start_inputs_bytes(*sd, ic.threads) : 0.0;   // mapped sections (StartView) or the rebuild model
  r.setup_copy = sd ? island::setup_view_bytes(*sd) : 0.0;               // WP4's SetupView, live beside the island
  ic.inputs_bytes = r.setup_in + r.setup_copy + (double)resident_own;
  const double k = sd ? island::plan_k(sd->size_logmass, 0.0) : kbar;
  island::IslandConfig ic1 = ic; ic1.G = 1; ic1.mem_budget = 0;
  island::MemSizes z = island::plan_sizes((int)n, (int)p, K, ic), z1 = island::plan_sizes((int)n, (int)p, K, ic1);
  r.ip = island::plan_with_budget(z, k, ic); r.ip1 = island::plan_with_budget(z1, k, ic1);
  return r;
}

// The three table top stores of a SetupView are read once, into the calibration ledger (offer_tables copies every entry);
// nothing after that reads them. Releasing them keeps the live copy to what setup_view_bytes counts.
inline void release_table_stores(wp4io::SetupView& S) { S.release_tables(); }

}  // namespace v4::calib
