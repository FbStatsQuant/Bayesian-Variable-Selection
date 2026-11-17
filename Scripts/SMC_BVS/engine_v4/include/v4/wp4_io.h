// wp4_io.h -- WP4 files: calib.bin (writer + reader), island_r.bin (reader; a reference writer for tests and for WP3),
// fit.bin + record (writer; section names read by WP5's eval), input validation by CONTENT hash and binary block
// (INTERFACES §5.1 "three identities", v0.1.3+), the setup view the merge needs (tables' top stores, comp(S), mode_S),
// and the `merge` command. Spec §1 rows 3-5, §6.
#pragma once
#include <string>
#include <vector>
#include "v4/calib.h"
#include "v4/calib_backend.h"
#include "v4/calib_run.h"
#include "v4/format.h"
#include "v4/json.h"
#include "v4/merge.h"
#include "v4/score.h"

namespace v4::wp4io {

// ---- generic sections ----------------------------------------------------------------------------------------------
// A store as <prefix>_v f64, _off u64, _len u16, _hash u64, _pool i32 (INTERFACES §4.1 flat layout; entries sorted).
// The store must be compacted and stay alive until Writer::write returns. Its cap and order go to meta["stores"].
void add_store(fmt::Writer& W, Json& meta, const std::string& prefix, const Store& s);
void add_store_sections(fmt::Writer& W, const std::string& prefix, const Store& s);   // the five sections only (setup.bin: no meta.stores)
// Rebuilds a Store from the sections (offer + compact; checks I1). Throws Error(invalid_input) on a malformed store.
void read_store(const fmt::Reader& R, const Json& meta, const std::string& prefix, Store& s, int32_t p, int32_t K,
                const Zobrist* zob = nullptr /* hashes checked against the models when given */);
// The same with the store's cap and order given (setup.bin: from INTERFACES §4.1, no meta.stores).
void read_store_sections(const fmt::Reader& R, const std::string& prefix, uint64_t cap, Order order, Store& s, int32_t p, int32_t K,
                         const Zobrist* zob = nullptr);
// Content checks (review PR20 M-2): a model is strictly increasing, in [0, p), of size <= K; else Error(invalid_input).
void check_model(ModelView S, int32_t p, int32_t K, const std::string& what);
// A list of models as <prefix>_ptr i64 (n + 1) and <prefix>_idx i32 (copied).
void add_models(fmt::Writer& W, const std::string& prefix, const std::vector<Model>& ms);
std::vector<Model> read_models(const fmt::Reader& R, const std::string& prefix, int32_t p, int32_t K);   // offsets + models checked
Json event_json(const EventCtx& e);                 // phase/mech names, phi, every key field
EventCtx event_from_json(const Json& j);
void add_ledger_tally(fmt::Writer& W, Json& meta, const Ledger& L);   // hpm_S, meta.hpm_ev/hpm_F/hpm_logm, logical, island_best
void read_ledger_tally(const fmt::Reader& R, const Json& meta, Ledger& L);

// ---- calib.bin -----------------------------------------------------------------------------------------------------
struct CalibWrite {
  uint32_t mode = fmt::M_COMPAT;
  const calib::CalibOut* co = nullptr;
  const Ledger* led = nullptr;                      // the calibration ledger (stores, HPM, counters)
  std::vector<merge::InheritedModel> inherited;     // models of the three calibration stores with F, lg0, logm (or:)
  const calib::InheritedFlat* inherited_flat = nullptr;   // the same, flat (calibrate_with's export; preferred; has d)
  const calib::Settings* settings = nullptr;        // rule parameters recorded in meta (I_max, refine_m, ell, sum mode)
  double k_store = 0;                               // calibration's mean stored |S| (INTERFACES v0.1.12 §7)
  int32_t N = 0, L = 0, Hm = 4;                     // final-run settings frozen with the grid
  Json inputs = Json::object();                     // {data.bin: hash, setup.bin: hash}
  std::vector<calib::StageRecord> stages;           // pilot and diagnostic islands' stage tables (calib.bin `stage_*`)
  Json extra = Json::object();                      // merged into meta (budgets, seed); reserved keys are refused
};
std::string write_calib(const std::string& path, const CalibWrite& c);   // returns the content hash
struct CalibIn {
  std::string content_hash; uint32_t mode = 0; Json meta;
  std::string status;                               // calibration status name (ok, schedule_limit, ...)
  std::vector<double> grid; int32_t tier = 0, N = 0, L = 0, Hm = 4;
  bool has_hpm = false; Model hpm; EventCtx hpm_ev;
  std::vector<merge::InheritedModel> inherited;
  std::string rule; int32_t I_used = 0, I_max = -1, ell = -1; double k_store = 0;
};
// Every model, value, grid and meta range checked. V mode: the bounded rule, tier 0, N = 2,500 (D-1, D-26) and
// I_used <= I_max <= ell. A completed calibration must carry k_store (finite, > 0). When data_hash / setup_hash are
// given, calib.bin's meta.inputs must name them (review PR37 m-3). A non-ok calib.bin exposes no inherited models.
CalibIn read_calib(const std::string& path, int32_t p, int32_t K, const std::string& data_hash = "", const std::string& setup_hash = "");

// ---- island_r.bin (INTERFACES v0.1.8 §5.1 = WP3's include/v4/island/island_file.h) ---------------------------------
// meta {schema, kind, mode, r, N, T, L, Hm, p, status, reason, inputs, binary, timings, logZ_hex, init_hash};
// grid [T+1]; st_phi st_ess st_inc st_cum f64 [T], st_distinct_res st_distinct_moved i32 [T], st_moves u64 [T x 12],
// term_moves u64 [(L+Hm) x 12], term_distinct i32 [L+Hm]; top_{v,hash,off,len,pool}; hpm_S i32, hpm_val f64 [F, log m],
// hpm_ev i64 [12] (seg, tier, iter, unit, xph, stage, round, particle, position, sub, phase, mech); island_best f64
// [r+1]; logical u64; completed only: logZ f64 [1], rb_acc, pip_r f64 [p], rb_round f64 [Hm x p], terminal_S_ptr i64
// [N+1] + terminal_S i32 (N supports after the last measured round). No leader stores (v0.1.7).
// hpm_ev has no phi: it is reconstructed from `grid` and the phase (INIT 0, BRIDGE grid[stage], BURN / MEASURED 1),
// v3's values (core/cpp/v3_engine.h:274-372).
// write_island: a reference writer of that layout (tests and the golden harness, until WP3's writer is merged).
std::string write_island(const std::string& path, uint32_t mode, const merge::IslandIn& isl, const Json& inputs,
                         const Json* binary_override = nullptr /* tests only */, const std::vector<double>* grid = nullptr);
// Expected identities of the merge's inputs (manifest).
struct Expect {
  uint32_t mode = fmt::M_COMPAT;
  std::string data_hash, setup_hash, calib_hash;   // content hashes of the inputs actually opened by the merge
  std::vector<std::string> island_hash;            // per island r = 1..R': manifest content hash ("" = not given)
  std::vector<double> grid;                        // calib.bin's frozen grid: every final island ran it (bitwise)
  int32_t L = -1, Hm = -1, K = 0;                  // calib.bin's L, Hm; the model cap K (data)
  int32_t tier = -1;                               // calib.bin's frozen tier (hpm_ev tier must equal it)
  const Zobrist* zob = nullptr;                    // data's Zobrist keys: every store hash is checked against its model
};
// Pass-1 head of island r (1-based): header, every section hash, kind/mode, content hash vs the manifest, meta.inputs
// vs the merge's data/setup/calib content hashes, and the meta scalars. Classification (spec §6, T10): no file ->
// missing; unreadable / bad hash / wrong kind or mode -> corrupt; content or inputs hash -> hash_mismatch. Never throws.
merge::IslandHead head_island(const std::string& path, int r, const Expect& ex, Json* binary_out);
// Full load (pass 2) of a file whose head was ok: the IslandIn the streaming merge needs (store, HPM + provenance,
// counters, island_best sized for R', estimates, terminal supports). Throws Error(invalid_input) on a malformed file.
merge::IslandIn load_island_full(const std::string& path, int Rp, int p, const Expect& ex);
// Slot form (head + load in one), used by tests.
merge::IslandSlot load_island(const std::string& path, int r, const Expect& ex, int p, Json* binary_out);
// Every island ran a compatible binary/libm block (INTERFACES §5.1 binary consistency; provenance.h): islands whose
// block is not compatible with the first ok island's are marked binary_mismatch. use = MergeV (mode V) or MergeTheory.
void check_binaries(std::vector<merge::IslandSlot>& slots, const std::vector<Json>& blocks, uint32_t mode);
void check_binaries(std::vector<merge::IslandHead>& heads, const std::vector<Json>& blocks, uint32_t mode);
// The streaming merge's source over island files: pass 1 (heads + binary check) at construction, one island loaded
// per load(r) call (the merge frees it after merging).
class FileIslandSource : public merge::IslandSource {
 public:
  FileIslandSource(std::vector<std::string> paths, const Expect& ex, int Rp, int p);
  int count() const override { return (int)paths_.size(); }
  merge::IslandHead head(int r) override { return heads_[(size_t)r - 1]; }
  merge::IslandIn load(int r) override;
  const std::vector<merge::IslandHead>& heads() const { return heads_; }
  void check_calib_isa(const Json& calib_block);   // D-32: an island of another FMA family than calib.bin -> binary_mismatch
 private:
  std::vector<std::string> paths_; std::vector<merge::IslandHead> heads_; std::vector<Json> blocks_; Expect ex_; int Rp_, p_;
};

// ---- setup view (until WP2's reader lands): the sections the merge needs --------------------------------------------
struct SetupView {
  std::string content_hash, data_hash;   // data_hash: setup.bin's meta.inputs["data.bin"] ("" if absent)
  std::vector<int32_t> blk, pos; std::vector<int64_t> code_ptr; std::vector<double> logr;
  std::vector<int64_t> blk_ptr; std::vector<int32_t> blk_members;
  Model mode_S;
  std::vector<double> size_logmass;                 // log P_pi0(|S| = k), k = 0..K (INTERFACES §5; empty if the file has none)
  Store ttop, tlead0, tlead1;                       // table top stores
  // core/cpp/v3_start.h:54-66 (copied): ordered block sum of log r_b(S n C_b).
  double comp(const Model& S, std::vector<std::pair<int32_t, int32_t>>& scratch) const;
  uint64_t table_event_count(int32_t K) const;      // codes with |U| <= K (one logical TABLE event each)
  EventCtx table_event_of(const Model& S) const;    // block b + 1, code of S in that block
};
SetupView read_setup(const std::string& path, int32_t p, int32_t K, const Zobrist* zob = nullptr);   // shapes, ranges and finite values checked
// The pi_0 size law of setup.bin (K + 1 log probabilities summing to 1); Error(invalid_input) otherwise. read_setup runs it;
// calibrate runs it on the dimensions reader's copy before it plans.
void check_size_logmass(const std::vector<double>& v, int32_t K, const std::string& what);
// ---- bounded plan reader (review PR46 MAJOR-2; INTERFACES §7: admission refuses "before any allocation") -------------
// data.bin: the header, the section table and `meta` (against its SHA-256 in the header-authenticated table); no column
// is read. Allocation is O(sections + meta). setup.bin's dimensions come from WP3's island::read_setup_dims (setup_load.h).
// The full readers run only after admission.
struct DataPlanHead { std::string content_hash; int64_t n = 0, p = 0; int32_t K = 0; uint64_t file_bytes = 0; };
DataPlanHead read_data_plan(const std::string& path);            // data.bin meta: n, p, K
std::string write_setup_min(const std::string& path, const SetupView& s, const Json& inputs);   // tests / harness
// Table step of the merge ledger: the table top stores offered (top -> HPM + top, lead0, lead1) with their table event
// keys, plus the logical TABLE count. Equal to ingesting every table code (core/cpp/v3_core.cpp:372-387) for the
// stores (top-c of a superset) and the HPM (the best table model with its own event).
void offer_tables(Ledger& led, const SetupView& s, int32_t K, const Zobrist& zob);

// ---- fit.bin -------------------------------------------------------------------------------------------------------
struct FitWrite {
  uint32_t mode = fmt::M_COMPAT;
  const merge::FitOut* fo = nullptr; const merge::MergeSettings* ms = nullptr;
  Json inputs = Json::object(); Json timings = Json::object();
  double occ_alpha = 0.001;                        // island-homogeneity flag: chi-square p-value < alpha (manager, 11-15)
};
std::string write_fit(const std::string& path, const FitWrite& f, Json* record = nullptr);
double chi2_upper(double x, int df);              // P(chi2_df > x), regularised upper incomplete gamma

}  // namespace v4::wp4io
