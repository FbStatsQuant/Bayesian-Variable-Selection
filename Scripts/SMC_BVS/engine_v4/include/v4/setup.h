// v4/setup.h -- WP2 `setup`: correlation pass, neighbour graph, duplicate components, partition (exact / truncated),
// cut-group record, block tables, start law pi_0, start mode, table top stores, setup.bin (INTERFACES v0.1 §2, §5.1;
// ENGINEERING_SPEC §0-v2.2 #5, §1 `setup`, §2, §5 T11; DECISIONS D-4; REVIEW_fable R3, R6).
// Every function claimed bit-identical to core/ cites the copied block. All code here lives in v4_bit
// (-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2).
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "v4/data.h"
#include "v4/json.h"
#include "v4/model.h"
#include "v4/rng.h"
#include "v4/status.h"
#include "v4/store.h"

namespace v4::setup {

// ---------------------------------------------------------------- types (INTERFACES §2)
struct Csr {
  std::vector<int64_t> ptr{0};
  std::vector<int32_t> idx;
  int64_t rows() const { return (int64_t)ptr.size() - 1; }
  void push_row(const int32_t* b, const int32_t* e) { idx.insert(idx.end(), b, e); ptr.push_back((int64_t)idx.size()); }
};
using Neighbours = Csr;  // ptr.size() = p + 1; each row sorted ascending; content = core/cpp/v3_blocks.h:149-170

struct Partition {
  int32_t J = 0, B = 0;
  std::vector<int64_t> bptr{0};
  std::vector<int32_t> members;   // block b = members[bptr[b]..bptr[b+1]), sorted, packing order
  std::vector<int32_t> blk, pos;  // as core/cpp/v3_start.h:79-80
  int32_t size(int b) const { return (int32_t)(bptr[b + 1] - bptr[b]); }
  const int32_t* block(int b) const { return members.data() + bptr[b]; }
};

// Edge of the thresholded correlation graph: j < l, absr = |G_jl| / (s_j s_l) (bits of core/cpp/v3_blocks.h:15).
struct Edge { int32_t j, l; double absr; };

struct CorrOptions {
  int B = 0;                 // neighbour cap (= the partition's B)
  int threads = 1;
  int tile = 256;            // columns per tile (not part of the result)
  bool keep_edges = true;    // collect E = {d <= 1 - tau} u {|r| >= rho} u {|r| >= 1 - 1e-10}
  double tau = -1;           // truncation threshold; < 0 => r_n = sqrt(2 log p / n)
  int64_t max_edges = 0;     // 0 => 64 p; exceeding it is a resource_limit (hub designs)
};
struct CorrResult {
  Neighbours nb;
  Csr dup;                   // components of {|r| >= 1 - 1e-10} of size >= 2, sorted, ordered by smallest member
  std::vector<Edge> edges;   // sorted by (j, l)
  double rn = 0, tau = 0;
  double seconds = 0;
  uint64_t pairs = 0;
};
CorrResult correlation_pass(const Data& D, const CorrOptions& o);

// Duplicate components from an edge list (needs keep_edges; same rule as core/cpp/v3_core.cpp:746-760).
Csr dup_components(int p, const std::vector<Edge>& edges);

// ---------------------------------------------------------------- partition
// Dendrogram / forest: node ids 0..p-1 leaves, p.. internal in merge order (core/cpp/v3_blocks.h:32-37).
struct Forest {
  int p = 0;
  std::vector<int32_t> left, right, size, minidx;
  std::vector<double> height;
  std::vector<int32_t> roots;  // forest roots (one root for the exact dendrogram), ascending node id
  int32_t merges() const { return (int32_t)left.size() - p; }
};
enum class PartMode : uint8_t { Exact = 0, Truncated = 1 };
enum class PackOrder : uint8_t { LeafOrder = 0, MinIndex = 1 };
struct PartitionOptions {
  PartMode mode = PartMode::Truncated;
  int B = 0;
  double tau = -1;        // < 0 => r_n
  bool strict = false;    // false: merge iff height <= 1 - tau (">=" sub-choice of THEORY-1); true: height < 1 - tau
  PackOrder pack = PackOrder::MinIndex;   // Truncated mode; Exact mode always uses the v3 leaf order
  int bv_cap = 14;        // D-19: truncated (V-1M) blocks have at most min(B, bv_cap) members at every n; exact keeps B
  int threads = 1;
};
int block_cap(const PartitionOptions& o);   // the block cap actually used: Exact B, Truncated min(B, bv_cap)
// Exact mode: dense p x p distances (8 p^2 bytes), complete linkage copied from core/cpp/v3_blocks.h:46-108.
Forest complete_linkage_exact(const Data& D, int threads);
// Truncated mode: complete linkage restricted to merges at height <= hcut (or < hcut) on the sparse edge set.
Forest complete_linkage_truncated(int p, const std::vector<Edge>& edges, double hcut, bool strict);
// Top-down cut (left first) + next-fit packing; members sorted in each block (core/cpp/v3_blocks.h:121-144).
Partition cut_and_pack(const Forest& T, int B, PackOrder order);
Partition make_partition(const Data& D, const CorrResult& C, const PartitionOptions& o, Forest* out = nullptr);
// Cut-group record (core/cpp/v3_core.cpp:792-818): components of the uncapped {|r| >= rho} graph spanning >= 2 blocks.
Csr cut_groups(int p, const std::vector<Edge>& edges, double rho, const Partition& P);

// ---------------------------------------------------------------- tables, start law (INTERFACES §2)
struct Tables {
  int32_t J = 0, K = 0;
  std::vector<int64_t> code_ptr{0};
  std::vector<double> logr;                // logr[code_ptr[b] + code]; NaN if |U| > K
  std::vector<int64_t> logprof_ptr{0};     // row base of block b; block b has top_b + 1 rows (sizes 0..top_b)
  std::vector<double> logprof;             // log e_b(j) at logprof_ptr[b] + j
  std::vector<double> logF;                // (J + 1) x (K + 1), row-major
  double logZbar0 = 0;
  std::vector<double> size_logmass, size_cum;   // K + 1
  // D-31: cond_cum is NOT stored in setup.bin. cond0[b*(K+1)+r] = the first entry of row (b, r), i.e. P(k_b = 0 | r)
  // as a cumulative: the scan every pi_0 draw needs (j = 0 iff u < cond0). A full row is recomputed by cond_row(T, b, r)
  // from logprof and logF (same bits). build_start(..., store_sampler = true) also fills cond_ptr/cond_cum (tests only).
  std::vector<double> cond0;               // J x (K + 1), row-major
  std::vector<int64_t> cond_ptr{0};        // row b*(K+1)+r (tests only)
  std::vector<double> cond_cum;            // (tests only)
  int cond_len(int b, int r) const { return std::min((int)(logprof_ptr[b + 1] - logprof_ptr[b]) - 1, r) + 1; }
  // D-18: codes_by_size and sub_cum are NOT stored in setup.bin; draw_pi0 recomputes them for the blocks a draw selects
  // (codes_of_size + sub_cum_of, same bits). build_start(..., store_sampler = true) fills these for tests only.
  std::vector<int64_t> cbs_ptr{0};         // row logprof_ptr[b] + j: codes of size j in increasing code order
  std::vector<uint32_t> codes_by_size;
  std::vector<int64_t> sub_ptr{0};         // = cbs_ptr (same row layout)
  std::vector<double> sub_cum;
  double logF_at(int b, int k) const { return logF[(size_t)b * (K + 1) + k]; }
};
// Table top stores: top-c of all table models under each of the three store orders (core/cpp/v3_ledger.h:72-94;
// fed as core/cpp/v3_core.cpp:372-386 ingest_tables): top (HPM, F, 40p+1), lead0 (LEX, lg0, 20p), lead1 (LEX, F, 20p).
struct TableStores { Store top, lead0, lead1; Model hpmS; double hpmF = NEG_INF; int32_t hpm_block = -1; uint32_t hpm_code = 0; };
struct TableStats { uint64_t scored = 0, prefix_scored = 0, fallback_scored = 0, routes[3] = {0, 0, 0}; double seconds = 0, seconds_stores = 0; };
// Tables by depth-first enumeration with sorted-prefix reuse, threaded over blocks. Bits = core/cpp/v3_start.h:76-98.
// If `stores` is given, the table top stores are built (then the per-code log m is dropped).
Tables build_tables(const Data& D, const Partition& P, int threads, TableStores* stores = nullptr, TableStats* st = nullptr);
// Size profiles, convolutions, log Zbar0, size law, cond0 (D-31): bits = core/cpp/v3_start.h:101-151. codes_by_size,
// sub_cum, cond_ptr and cond_cum are stored only if store_sampler (tests; D-18, D-31).
void build_start(const Data& D, const Partition& P, Tables& T, bool store_sampler = false);
// D-18 helpers. Codes 0..2^m-1 of popcount j in increasing code order (core/cpp/v3_start.h:108-112); m <= 16.
const uint32_t* codes_of_size(int m, int j, uint32_t* count);
// Within-size law of block b (size m) at size j: cumulative_from_logs over the codes' logr (core/cpp/v3_start.h:116-118).
void sub_cum_of(const Tables& T, int b, int m, int j, std::vector<double>& out);
// D-31: row (b, r) of the conditional block-size law, cumulative over j = 0..min(top_b, r) (core/cpp/v3_start.h:140-150,
// the same bits as the stored cond_cum row). out.size() == T.cond_len(b, r). Thread-safe.
void cond_row(const Tables& T, int b, int r, std::vector<double>& out);
// D-31: the pi_0 size of block b given r remaining (core/cpp/v3_start.h:163-166): j = 0 by the cond0 scan when u < cond0,
// else upper_bound on cond_row(b, r). Same j as the stored row for every u. Used by Start::draw_pi0.
int pi0_block_size(const Tables& T, int b, int r, double u);
// core/cpp/v3_start.h:21-32
void cumulative_from_logs(const double* lp, size_t n, double* c);

struct ModeResult { Model S; double lg0 = NEG_INF; long ties = 0; bool truncated = false; bool tie_dp_used = false; };
enum class ModeAlgo : uint8_t { Auto = 0, Enumerate = 1, CountThenTieDP = 2 };
// Start mode argmax pi_0 (core/cpp/v3_start.h:178-305), iterative. Enumerate: the v3 enumeration (explicit stack,
// same visiting order) with the v3 tie-DP fallback; CountThenTieDP: count |E| by DP (saturating at cap), then the
// incremental tie-aware DP when needed; both return v3's (S, lg0, ties, truncated, tie_dp_used). Auto picks by size.
ModeResult start_mode(const Data& D, const Partition& P, const Tables& T, long cap = 1000000, bool tie_dp = true,
                      ModeAlgo algo = ModeAlgo::Auto);

struct Start {
  const Data* D = nullptr; const Partition* P = nullptr; const Tables* T = nullptr;
  double logZbar0 = 0;
  ModeResult mode;
  double comp(ModelView S) const;            // core/cpp/v3_start.h:54-66 (same bits)
  double log_gamma0(ModelView S) const { return D->logprior[S.k] + comp(S); }
  // core/cpp/v3_start.h:158-176; uniform t of the draw is read at address `a` with slot = t.
  void draw_pi0(UniformSource& us, Address a, Model& S) const;
};

// ---------------------------------------------------------------- memory accounting and admission (Sol review F1)
// Exact byte accounting of every setup array from the partition alone (no table is allocated). Items marked bound are
// upper bounds that become exact only after the tables exist (store pools: <= B_blocks int32 per entry; std::set /
// allocator overheads of the truncated linkage: per-node estimate). Stage peaks = the arrays live in each stage.
struct MemItem { std::string name, stage; uint64_t bytes = 0; bool exact = true; bool stored = false; uint64_t est = 0; };
struct MemAccount {
  int64_t n = 0, p = 0, K = 0, B = 0, B_blocks = 0, J = 0, threads = 1, edges = 0, nb_nnz = -1;
  std::vector<int64_t> hist;            // hist[m] = number of blocks with m members, m = 0..16
  int64_t C = 0;                        // sum_b 2^{|C_b|} (table codes, logr entries)
  int64_t C_feasible = 0;               // codes with popcount <= K (= C when every block has <= K members)
  int64_t NR = 0, cond_vals = 0, table_models = 0;
  std::vector<MemItem> items;
  std::vector<std::pair<std::string, uint64_t>> stage_peak, stage_peak_est;   // bound / estimate per stage
  uint64_t peak = 0, peak_est = 0, setup_bin = 0, setup_bin_est = 0, not_stored_d18 = 0, not_stored_d31 = 0;
  Json to_json() const;
};
MemAccount account(const Data& D, int coded_B, const Partition& P, int64_t edges, int64_t nb_nnz, int threads, PartMode mode);

// count-only (Sol review F1 item 1): correlation edges -> production partition -> histogram, C, accounting; no tables.
// With AVX-512 the edge set comes from a float32 candidate filter with a proven error margin, every candidate
// re-checked in double with the production predicate (so the edge set, hence the partition, is exactly production's);
// otherwise from the exact correlation pass.
struct CountResult { CorrResult corr; Partition part; MemAccount acc; bool filter_used = false; uint64_t candidates = 0; double seconds_edges = 0, seconds_partition = 0; };
CountResult count_only(const Data& D, const PartitionOptions& po, int coded_B, int threads, bool allow_filter = true);
// float32 AVX-512 candidate filter + exact double re-check (exposed for tests). Throws if AVX-512F is unavailable.
std::vector<Edge> edges_by_filter(const Data& D, double tau, int threads, uint64_t* candidates = nullptr);
bool filter_available();

// ---------------------------------------------------------------- the setup command
struct SetupOptions {
  int B = 0;                  // 0 => min(isqrt(n), isqrt(p), 16) (core/v3_preprocess.R:22)
  PartitionOptions part;      // part.B is set from B
  int threads = 1;
  long mode_cap = 1000000;
  bool tie_dp = true;
  bool table_stores = true;
  uint32_t file_mode = 2;     // 1 compat, 2 law, 3 V
  double mem_budget_gb = 0;   // > 0: admission rule, refuse (resource_limit, reason "admission:") if the accounted peak exceeds it
  int64_t max_edges = 0;      // edge guard for the uncapped threshold graph (0 => 64 p)
};
struct StageTiming { std::string name; double seconds; double peak_rss_mb; };
struct SetupResult {
  Status status = Status::completed;
  std::string reason;
  int B = 0;
  CorrResult corr;
  Partition part;
  Csr cut;
  Tables tab;
  TableStores stores;
  ModeResult mode;
  TableStats tstats;
  MemAccount acc;
  std::vector<StageTiming> timings;
};
int default_B(int n, int p);
// All stages on an in-memory Data (library entry; statuses in SetupResult, never thrown).
SetupResult run_setup(const Data& D, const SetupOptions& o);
// The `setup` command (include/v4/stubs.h): args data (data.bin), out (setup.bin), optional threads, B, partition
// ("truncated" | "exact"), tau, strict (0/1), mode_cap, tie_dp (0/1), file_mode ("law" | "compat" | "V").
Json run(const Json& args);
// setup.bin (INTERFACES §5.1 kind 3). Returns the content hash. `data_hash` = content hash of data.bin.
std::string write_setup_bin(const std::string& path, const Data& D, const SetupResult& r, const SetupOptions& o, const std::string& data_hash);
SetupResult read_setup_bin(const std::string& path, std::string* content_hash = nullptr);
double peak_rss_mb();
namespace testing { void set_force_fallback(int every); }  // tests only: score every k-th table entry by the full scorer

}  // namespace v4::setup
