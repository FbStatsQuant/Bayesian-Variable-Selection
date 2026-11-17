// calib_runner.h -- WP3's calibration-island runner for WP4's calibration backend (WP3_DESIGN §1.11; the interface is
// WP4's v4::calib::IslandRunner, include/v4/calib_backend.h).
//
// One runner per calibration. run(IslandSpec) runs one pilot (role PILOT, island 0, iteration 0, core's adaptive pilot
// rule) or one diagnostic island (role DIAG, island 1..4, iteration k, the candidate grid) with run_island<A> and
// returns WP4's IslandOut: status, message, partial, logZ, schedule phi_1..phi_T, forced, stages, pip, the island's own
// Ledger (CALIB keys, leaders on, islands = 4; the ledger so far on resource_limit and numerical_failure) and, in compat,
// the stream positions. Compat: the runner owns the v3 streams 0-9 (core/cpp/v3_core.cpp:593-596) and continues them
// across rebuilds and tiers, as core's CalState does; a stream is created (seed_stream(seed, s)) at its first use.
// Header-only template: the R golden harness links only the bit-form library and instantiates <Arith::Bit>.
#pragma once
#include <map>
#include <memory>
#include "v4/calib_backend.h"
#include "v4/island/island.h"

namespace v4::island {

struct CalibRunnerConfig {
  uint32_t seed = 1;
  bool compat = false;                         // theory compat: Bit, particle-major, 1 thread, v3 streams
  KernelKind kernel = KernelKind::ParticleMajor;
  int threads = 1, G = 0, tile = 128, B = 14;  // B: number of N-swap labels (budgets B)
  double k_store = 0, inputs_bytes = 0; uint64_t mem_budget = 0;
  bool allow_test_kernels = false;             // tests: the bit-form label-major kernel (LM = PM checks)
  std::string cost_dir;                        // D-30 (WP7 O5): per-island cost records <dir>/cost_<pilot|diag>_t<e>_k<k>_r<r>.jsonl
  bool verbose = false;                        // per-step progress lines on stderr (IslandConfig::verbose)
};
// the cost-record file of one calibration island (WP7 O5; IslandConfig::cost_path)
inline std::string calib_cost_path(const std::string& dir, bool pilot, int tier, int iter, int island) {
  return dir + "/cost_" + (pilot ? "pilot" : "diag") + "_t" + std::to_string(tier) + "_k" + std::to_string(iter) + "_r" + std::to_string(island) + ".jsonl";
}

template <Arith A>
class CalibIslandRunner final : public v4::calib::IslandRunner {
 public:
  CalibIslandRunner(const Data& D, const Start& st, const Neighbours& nb, const CalibRunnerConfig& c) : D_(D), st_(st), nb_(nb), c_(c) {}

  v4::calib::IslandOut run(const v4::calib::IslandSpec& sp) override {
    const bool pilot = sp.role == v4::calib::IslandRole::Pilot;
    IslandConfig c;
    c.seed = c_.seed; c.role = pilot ? IslandRole::Pilot : IslandRole::Diag; c.tier = (uint32_t)sp.tier; c.iter = (uint32_t)sp.iter;
    c.island = (uint32_t)sp.island; c.N = sp.H; c.L = sp.L; c.Hm = sp.Hm; c.B = c_.B;
    c.kernel = c_.kernel; c.threads = c_.threads; c.G = c_.G; c.tile = c_.tile; c.allow_test_kernels = c_.allow_test_kernels;
    // memory (INTERFACES §7, WP4's N-1 rule in IslandSpec): spec.mem_budget is the WHOLE calibration task's budget (0 = no
    // admission); spec.resident_bytes is the calibration process's own state (calibration ledger at its staging peak +
    // inherited export) WITHOUT X / z / diag(G) and the setup inputs, which the island's plan counts itself (its inputs
    // term: X, z, diag(G) + inputs_bytes = the setup inputs). Admitted iff resident_bytes + plan <= mem_budget: the
    // resident bytes join the plan's caller-supplied term, so no byte is counted twice.
    c.k_store = c_.k_store; c.inputs_bytes = c_.inputs_bytes + (double)sp.resident_bytes;
    c.mem_budget = sp.mem_budget ? sp.mem_budget : c_.mem_budget;
    c.keep_terminal = false; c.leaders = true;
    if (!c_.cost_dir.empty()) c.cost_path = calib_cost_path(c_.cost_dir, pilot, sp.tier, sp.iter, sp.island);
    c.verbose = c_.verbose;
    if (pilot) { c.adaptive = true; c.adaptive_H = sp.H; c.adaptive_Te = sp.Te; } else c.grid = sp.grid;
    if (c_.compat) {
      c.compat = true;
      c.compat_src = &stream(v4::compat_stream(pilot ? R_PILOT : R_DIAG, (uint8_t)sp.tier, (uint32_t)sp.island));
    }
    IslandRun r = run_island<A>(D_, st_, nb_, c);   // invalid configurations throw (invalid_input): not an island outcome
    v4::calib::IslandOut o;
    o.status = r.status == 0 ? v4::Status::completed : r.status == 2 ? v4::Status::numerical_failure : v4::Status::resource_limit;
    o.message = r.reason; o.partial = r.partial; o.logZ = r.logZ; o.forced = r.forced;
    // schedule phi_1..phi_T of the completed stages (a stop between stages leaves no phi without its stage)
    const size_t ns = r.status == 0 ? (r.grid.size() ? r.grid.size() - 1 : 0) : std::min(r.stages.size(), r.grid.size() ? r.grid.size() - 1 : 0);
    o.schedule.assign(r.grid.begin() + (r.grid.empty() ? 0 : 1), r.grid.begin() + (r.grid.empty() ? 0 : 1) + ns);
    o.stages = r.stages; o.pip = r.pip;
    o.led = std::move(to_record(r).led);
    o.init_hash = r.init_hash;
    if (r.compat) { o.position_start = r.stream_start; o.position_end = r.stream_count; }
    return o;
  }

  // compat streams, by v3 stream number (tests: positions after a calibration)
  v4::CompatSource& stream(uint64_t s) {
    auto it = streams_.find(s);
    if (it == streams_.end()) it = streams_.emplace(s, std::make_unique<v4::CompatSource>(c_.seed, s)).first;
    return *it->second;
  }

 private:
  const Data& D_; const Start& st_; const Neighbours& nb_; CalibRunnerConfig c_;
  std::map<uint64_t, std::unique_ptr<v4::CompatSource>> streams_;
};

}  // namespace v4::island
