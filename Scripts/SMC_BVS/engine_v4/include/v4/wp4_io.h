// wp4_io.h -- WP4 files: calib.bin (writer + reader), island_r.bin (reader; a reference writer for tests and for WP3),
// fit.bin + record (writer; section names read by WP5's eval), input validation by CONTENT hash and binary block
// (INTERFACES §5.1 "three identities", v0.1.3+), the setup view the merge needs (tables' top stores, comp(S), mode_S),
// and the `merge` command. Spec §1 rows 3-5, §6.
#pragma once
#include <string>
#include <vector>
#include "v4/calib.h"
#include "v4/format.h"
#include "v4/json.h"
#include "v4/merge.h"
#include "v4/score.h"

namespace v4::wp4io {

// ---- generic sections ----------------------------------------------------------------------------------------------
// A store as <prefix>_v f64, _off u64, _len u16, _hash u64, _pool i32 (INTERFACES §4.1 flat layout; entries sorted).
// The store must be compacted and stay alive until Writer::write returns. Its cap and order go to meta["stores"].
void add_store(fmt::Writer& W, Json& meta, const std::string& prefix, const Store& s);
// Rebuilds a Store from the sections (offer + compact; checks I1). Throws Error(invalid_input) on a malformed store.
void read_store(const fmt::Reader& R, const Json& meta, const std::string& prefix, Store& s);
// A list of models as <prefix>_ptr i64 (n + 1) and <prefix>_idx i32 (copied).
void add_models(fmt::Writer& W, const std::string& prefix, const std::vector<Model>& ms);
std::vector<Model> read_models(const fmt::Reader& R, const std::string& prefix);
Json event_json(const EventCtx& e);                 // phase/mech names, phi, every key field
EventCtx event_from_json(const Json& j);
void add_ledger_tally(fmt::Writer& W, Json& meta, const Ledger& L);   // hpm_S, meta.hpm_ev/hpm_F/hpm_logm, logical, island_best
void read_ledger_tally(const fmt::Reader& R, const Json& meta, Ledger& L);

// ---- calib.bin -----------------------------------------------------------------------------------------------------
struct CalibWrite {
  uint32_t mode = fmt::M_COMPAT;
  const calib::CalibOut* co = nullptr;
  const Ledger* led = nullptr;                      // the calibration ledger (stores, HPM, counters)
  std::vector<merge::InheritedModel> inherited;     // models of the three calibration stores with F, lg0, logm
  int32_t N = 0, L = 0, Hm = 4;                     // final-run settings frozen with the grid
  Json inputs = Json::object();                     // {data.bin: hash, setup.bin: hash}
};
std::string write_calib(const std::string& path, const CalibWrite& c);   // returns the content hash
struct CalibIn {
  std::string content_hash; uint32_t mode = 0; Json meta;
  std::string status;                               // calibration status name (ok, schedule_limit, ...)
  std::vector<double> grid; int32_t tier = 0, N = 0, L = 0, Hm = 4;
  bool has_hpm = false; Model hpm; EventCtx hpm_ev;
  std::vector<merge::InheritedModel> inherited;
};
CalibIn read_calib(const std::string& path);

// ---- island_r.bin --------------------------------------------------------------------------------------------------
// Sections (INTERFACES §5.1): st_phi, st_inc, st_ess, st_cum, rb_acc, rb_round (Hm x p), pip_r, top_* store, hpm_S,
// island_best, logical, optional terminal_S_ptr/terminal_S; meta {r, N, T, L, Hm, logZ, status, message, inputs, binary}.
// write_island is the reference layout (tests; WP3 may adopt it). The merge reads only what merge::IslandIn needs.
std::string write_island(const std::string& path, uint32_t mode, const merge::IslandIn& isl, const Json& inputs,
                         const Json* binary_override = nullptr /* tests only */);
// Expected identities of the merge's inputs (manifest).
struct Expect {
  uint32_t mode = fmt::M_COMPAT;
  std::string data_hash, setup_hash, calib_hash;   // content hashes of the inputs actually opened by the merge
  std::vector<std::string> island_hash;            // per island r = 1..R': manifest content hash ("" = not given)
};
// Loads island r (1-based). Classification (spec §6, T10): no file -> missing; unreadable / bad header / bad section
// hash / wrong kind or mode -> corrupt; content hash != manifest, or meta.inputs != the merge's data/setup/calib
// content hashes -> hash_mismatch. Never throws for these.
merge::IslandSlot load_island(const std::string& path, int r, const Expect& ex, int p, Json* binary_out);
// Every island ran a compatible binary/libm block (INTERFACES §5.1 binary consistency; provenance.h): islands whose
// block is not compatible with island 1's are marked binary_mismatch. use = MergeV (mode V) or MergeTheory.
void check_binaries(std::vector<merge::IslandSlot>& slots, const std::vector<Json>& blocks, uint32_t mode);

// ---- setup view (until WP2's reader lands): the sections the merge needs --------------------------------------------
struct SetupView {
  std::string content_hash;
  std::vector<int32_t> blk, pos; std::vector<int64_t> code_ptr; std::vector<double> logr;
  std::vector<int64_t> blk_ptr; std::vector<int32_t> blk_members;
  Model mode_S;
  Store ttop, tlead0, tlead1;                       // table top stores
  // core/cpp/v3_start.h:54-66 (copied): ordered block sum of log r_b(S n C_b).
  double comp(const Model& S, std::vector<std::pair<int32_t, int32_t>>& scratch) const;
  uint64_t table_event_count(int32_t K) const;      // codes with |U| <= K (one logical TABLE event each)
  EventCtx table_event_of(const Model& S) const;    // block b + 1, code of S in that block
};
SetupView read_setup(const std::string& path);
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
