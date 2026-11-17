// island_cmd.cpp -- `smcbvs4 island` (WP3; INTERFACES §1, §5.1, §5.3, §7; WP3_DESIGN §1.13): one FINAL island r of a
// fit. Reads data.bin, setup.bin and calib.bin, runs run_island with calib.bin's frozen grid, N, L, Hm and tier, and
// writes island_r.bin (island_file.h) with meta.inputs = the three content hashes (what WP4's merge checks).
//
//   Driver form:   smcbvs4 island --manifest island_r.json --out island_r.bin [--threads k] [--mem-budget BYTES]
//                  inputs by base name (data.bin, setup.bin, calib.bin) among the manifest's `inputs`; mode = the
//                  manifest's mode; r = params.id (the driver's key) or params.island (INTERFACES §5.3); seed =
//                  params.seed. The manifest is the authority: an explicit argument that disagrees is refused.
//   Explicit form: smcbvs4 island --data D --setup S --calib C --island r --seed s --mode compat|law|V --out island_r.bin
//                  [--Rp R] [--threads k] [--mem-budget BYTES | --mem-budget-gb G] [--G g] [--tile t]
//                  [--ckpt 0|1] [--ckpt-every-s s] [--stop-after-s S (WP7 O4: a soft stop: checkpoint at the first step boundary after S
//                  seconds from the command's start and exit 22 `interrupted_resumable`; a rerun resumes)] [--offer-floor 1|0 (D-29: V final islands drop store offers below calib.bin's
//                  tau_cal; 0 = no floor, the merged science is the same; WP7 O6)]
//   Plan only:     the same with --plan-only 1 (no --out needed): the island's admission plan (memory.h), no run.
//                  Without files: --plan-only 1 --mode M --n n --p p [--N N --threads k --G g --k k --inputs-bytes b]
//                  (ESTIMATE: k given, setup inputs given or 0).
//
// Roles: the command runs final islands only (role `final`). Pilot and diagnostic islands run inside `calibrate`, which
// owns their streams and ledgers (WP3_DESIGN §1.11).
// Kernels (D-21): compat = bit form, particle-major, 1 thread, v3 stream 9 + r; law = bit form, particle-major; V = class A,
// label-major. Memory (INTERFACES §7): --mem-budget is the whole task's memory; the island plan counts X, z, diag(G),
// the stores, ... and, as its caller-supplied term, the setup inputs: the mapped setup.bin sections the flat start law
// reads (StartView, WP3_DESIGN §1.12) + its draw scratch + the neighbour lists.
// k = max(8, q90(pi_0 size) + 1, calib.bin k_store). Over budget: resource_limit before the run, island_r.bin written
// with that status (no estimate section, GUARD-W), exit 11.
// Checkpoints: <out without .bin>.ckpt.{a,b} (INTERFACES §5.1), every --ckpt-every-s seconds (default 600); a restart of
// the same command resumes from the newest valid one; removed once island_r.bin is written as completed.
#include <sys/stat.h>
#include <chrono>
#include <cmath>
#include <cstdio>
#include "v4/calib_run.h"
#include "v4/cmd_args.h"
#include "v4/island/island.h"
#include "v4/island/island_file.h"
#include "v4/island/setup_load.h"
#include "v4/format.h"
#include "v4/offer_floor.h"
#include "v4/prep.h"
#include "v4/provenance.h"
#include "v4/stubs.h"
#include "v4/threads.h"
#include "v4/wp4_io.h"

namespace v4::island {

namespace {
const char* W = "island: ";
std::string hex64(uint64_t x) { char b[19]; std::snprintf(b, sizeof b, "0x%016llx", (unsigned long long)x); return b; }
Json u64j(uint64_t x) { return Json((double)x); }   // byte counts < 2^53

// a whole number in [lo, hi] (no unchecked casts)
int64_t whole(const Json& v, const std::string& what, int64_t lo, int64_t hi) {
  if (v.type() != Json::NUM) throw Error(Status::invalid_input, W + what + " must be a number");
  const double x = v.num();
  if (!std::isfinite(x) || x != std::floor(x) || x < (double)lo || x > (double)hi)
    throw Error(Status::invalid_input, W + what + " must be a whole number in [" + std::to_string(lo) + ", " + std::to_string(hi) + "]");
  return (int64_t)x;
}
int64_t whole_arg(const Json& a, const char* k, int64_t dflt, int64_t lo, int64_t hi) {
  return a.contains(k) ? whole(a.at(k), std::string("--") + k, lo, hi) : dflt;
}
std::string str_arg(const Json& a, const char* k) {
  if (!a.contains(k)) return "";
  if (a.at(k).type() != Json::STR) throw Error(Status::invalid_input, std::string(W) + "--" + k + " must be a string");
  return a.at(k).str();
}
// --mem-budget (bytes) / --mem-budget-gb (GiB alias): a whole number of bytes in [0, 2^50], 0 = off (INTERFACES §1, §7)
uint64_t mem_budget_arg(const Json& a) {
  if (a.contains("mem_budget") && a.contains("mem_budget_gb")) throw Error(Status::invalid_input, std::string(W) + "give --mem-budget or --mem-budget-gb, not both");
  if (a.contains("mem_budget")) return (uint64_t)whole(a.at("mem_budget"), "--mem-budget", 0, (int64_t)1 << 50);
  if (a.contains("mem_budget_gb")) {
    if (a.at("mem_budget_gb").type() != Json::NUM) throw Error(Status::invalid_input, std::string(W) + "--mem-budget-gb must be a number");
    return (uint64_t)whole(Json(std::floor(a.at("mem_budget_gb").num() * 1073741824.0)), "--mem-budget-gb", 0, (int64_t)1 << 50);
  }
  return 0;
}

struct Inputs {
  Json manifest = Json::object();
  std::string data, setup, calib, out, mode;
  int64_t r = -1, seed = -1, Rp = -1;
};

// Resolves the inputs: the manifest (authority) and the explicit arguments; a disagreement is refused (as WP4's merge).
Inputs parse_inputs(const Json& args, bool plan_only) {
  Inputs in;
  in.manifest = cmd::manifest_of(args, "island");
  const Json mpar = cmd::manifest_params(in.manifest);
  in.data = cmd::input_path(args, in.manifest, "data", "data.bin", "island", !plan_only);
  in.setup = cmd::input_path(args, in.manifest, "setup", "setup.bin", "island", !plan_only);
  in.calib = cmd::input_path(args, in.manifest, "calib", "calib.bin", "island", !plan_only);
  in.out = str_arg(args, "out");
  // mode: the manifest's, else --mode
  std::string mm;
  if (in.manifest.contains("mode")) {
    if (in.manifest.at("mode").type() != Json::STR) throw Error(Status::invalid_input, std::string(W) + "the manifest's mode must be a string");
    mm = in.manifest.at("mode").str();
  }
  const std::string ma = str_arg(args, "mode");
  if (!mm.empty() && !ma.empty() && mm != ma) throw Error(Status::invalid_input, std::string(W) + "--mode differs from the manifest's mode");
  in.mode = mm.empty() ? ma : mm;
  if (in.mode != "compat" && in.mode != "law" && in.mode != "V") throw Error(Status::invalid_input, std::string(W) + "--mode must be compat, law or V");
  // a whole-number parameter: the manifest's params (authority) or the explicit argument; any disagreement is refused, in
  // either argument order (review PR52 MAJOR-4). `args` holds the manifest's params too (main copies them over an earlier
  // explicit value), so the explicit values are cmd::explicit_args(), not `args`.
  const Json& ex = cmd::explicit_args(args);
  auto param = [&](std::initializer_list<const char*> keys, int64_t lo, int64_t hi) -> int64_t {
    int64_t v = -1; std::string src;
    for (const char* k : keys) {
      for (int pass = 0; pass < 2; ++pass) {
        const Json& o = pass == 0 ? mpar : ex;
        if (!o.contains(k)) continue;
        const std::string nm = (pass == 0 ? "manifest params." : "--") + std::string(k);
        const int64_t x = whole(o.at(k), nm, lo, hi);
        if (v >= 0 && x != v) throw Error(Status::invalid_input, W + nm + " = " + std::to_string(x) + " differs from " + src + " = " + std::to_string(v));
        if (v < 0) { v = x; src = nm; }
      }
    }
    return v;
  };
  in.r = param({"id", "island"}, 1, (1 << 20) - 1);       // INTERFACES §3: final island r = 1..R' < 2^20
  in.seed = param({"seed"}, 1, 2147483647);
  in.Rp = param({"Rp"}, 1, (1 << 20) - 1);
  if (in.Rp > 0 && in.r > in.Rp) throw Error(Status::invalid_input, std::string(W) + "island r = " + std::to_string(in.r) + " > R' = " + std::to_string(in.Rp));
  if (args.contains("role")) {   // calibration roles run inside `calibrate` (WP3_DESIGN §1.11)
    if (args.at("role").type() != Json::STR || args.at("role").str() != "final")
      throw Error(Status::invalid_input, std::string(W) + "--role must be final (pilot and diagnostic islands run inside calibrate)");
  }
  return in;
}

// the calib.bin fields a final island needs (meta + grid; the stores are not loaded: at 10^6 they are GBs)
struct CalibHead { std::string hash, status, data_hash, setup_hash; uint32_t mode = 0; int32_t tier = 0, N = 0, L = 0, Hm = 4; double k_store = 0; int64_t seed = -1; std::vector<double> grid;
                   OfferFloor floor;   // D-29: a V final island's offer floor = calib.bin's tau_cal (else -inf; WP7 O6)
                   Json binary; };     // calib.bin's binary block (D-32: the island refuses another class-A FMA family)
CalibHead read_calib_head(const std::string& path) {
  fmt::Reader R(path);   // every section hash verified (INTERFACES §5.1)
  if (R.kind() != fmt::K_CALIB) throw Error(Status::invalid_input, path + ": not a calib file");
  CalibHead c; c.hash = R.content_hash(); c.mode = R.mode();
  const Json m = R.json("meta");
  c.status = m.at("status").str();
  if (c.status != "ok") throw Error(Status::invalid_input, path + ": calibration status " + c.status + " (no frozen grid)");
  c.tier = (int32_t)whole(m.at("tier"), "calib meta tier", 0, 1); c.N = (int32_t)whole(m.at("N"), "calib meta N", 1, 1 << 24);
  c.L = (int32_t)whole(m.at("L"), "calib meta L", 0, 1 << 16); c.Hm = (int32_t)whole(m.at("Hm"), "calib meta Hm", 1, 1 << 16);
  if (!m.contains("k_store") || m.at("k_store").type() != Json::NUM || !std::isfinite(m.at("k_store").num()) || !(m.at("k_store").num() > 0))
    throw Error(Status::invalid_input, path + ": k_store missing, or not finite and > 0");
  c.k_store = m.at("k_store").num();
  if (m.contains("seed")) c.seed = whole(m.at("seed"), "calib meta seed", 1, 2147483647);
  const Json& in = m.at("inputs");
  if (in.contains("data.bin")) c.data_hash = in.at("data.bin").str();
  if (in.contains("setup.bin")) c.setup_hash = in.at("setup.bin").str();
  c.floor = offer_floor_from_calib(m, c.mode == fmt::M_V, c.hash);   // INTERFACES v0.1.17 §4.1 (MINOR-1); the merge checks it again
  if (m.contains("binary")) c.binary = m.at("binary");
  c.grid = R.vec<double>("grid");
  if (c.grid.size() < 2 || c.grid.front() != 0.0 || c.grid.back() != 1.0) throw Error(Status::invalid_input, path + ": frozen grid does not run from 0 to 1");
  for (size_t i = 1; i < c.grid.size(); ++i) if (!(c.grid[i] > c.grid[i - 1])) throw Error(Status::invalid_input, path + ": frozen grid not strictly increasing");
  return c;
}

Json plan_json(const MemPlan& mp, uint64_t budget, double inputs_bytes, const char* label) {
  Json j = Json::object();
  j["label"] = label;
  Json items = Json::object(); for (const auto& it : mp.items) items[it.name] = u64j(it.bytes);
  j["items"] = items; j["total"] = u64j(mp.total); j["G"] = mp.G; j["k"] = mp.k; j["budget"] = u64j(budget);
  j["setup_inputs"] = inputs_bytes; j["admitted"] = budget == 0 || mp.total <= budget;
  j["text"] = mem_plan_text(mp);
  return j;
}

KernelKind kernel_of(uint32_t mode) { return mode == fmt::M_V ? KernelKind::LabelMajor : KernelKind::ParticleMajor; }
}  // namespace

Json run(const Json& args) {
  const bool plan_only = whole_arg(args, "plan_only", 0, 0, 1) == 1;
  const Inputs in = parse_inputs(args, plan_only);
  const uint32_t mode = fmt::mode_from_name(in.mode);
  const bool compat = mode == fmt::M_COMPAT;
  int threads = (int)whole_arg(args, "threads", threads_available(), 1, 4096);
  if (compat) threads = 1;   // serial v3 streams (D-21)
  const uint64_t budget = mem_budget_arg(args);
  const int G = (int)whole_arg(args, "G", 0, 0, 256), tile = (int)whole_arg(args, "tile", 128, 64, 4096);
  Json rec = Json::object();
  rec["mode"] = in.mode; rec["threads"] = threads; rec["kernel"] = kernel_of(mode) == KernelKind::LabelMajor ? "label_major" : "particle_major";

  // ---- plan without files (ESTIMATE): sizes from the arguments ----------------------------------------------------
  if (plan_only && in.data.empty()) {
    if (!in.setup.empty() || !in.calib.empty()) throw Error(Status::invalid_input, std::string(W) + "--plan-only with files needs --data, --setup and --calib");
    IslandConfig c; c.N = (int)whole_arg(args, "N", 2500, 1, 1 << 24); c.Hm = (int)whole_arg(args, "Hm", 4, 1, 1 << 16);
    c.kernel = kernel_of(mode); c.threads = threads; c.G = G; c.tile = tile; c.compat = compat; c.mem_budget = budget;
    c.inputs_bytes = (double)whole_arg(args, "inputs_bytes", 0, 0, (int64_t)1 << 50);
    const int64_t n = whole_arg(args, "n", 0, 3, (int64_t)1 << 31), p = whole_arg(args, "p", 0, 1, (int64_t)1 << 31);
    if (n < 3 || p < 1) throw Error(Status::invalid_input, std::string(W) + "--plan-only needs --data/--setup/--calib, or --n and --p");
    const double k = (double)whole_arg(args, "k", 8, 1, 1 << 16);
    const calib::Budgets bud = calib::budgets(n, p);   // K = min(p, n / 2) and B = min(isqrt n, isqrt p, 16): the engine's budgets
    if (args.contains("B") && whole(args.at("B"), "--B", 1, 1 << 16) != bud.B)
      throw Error(Status::invalid_input, std::string(W) + "--B differs from the engine's N-swap budget B = " + std::to_string(bud.B));
    c.B = bud.B;
    MemSizes z = plan_sizes((int)n, (int)p, bud.K, c);
    MemPlan mp = plan_with_budget(z, k, c);
    rec["n"] = (double)n; rec["p"] = (double)p; rec["N"] = c.N;
    rec["mem_plan"] = plan_json(mp, budget, c.inputs_bytes, "ESTIMATE (final island plan from sizes: k given, setup inputs = --inputs-bytes)");
    rec["plan_only"] = true;
    rec["status"] = budget && mp.total > budget ? "resource_limit" : "completed";
    if (budget && mp.total > budget) rec["reason"] = "island not admitted: plan " + std::to_string(mp.total) + " B > --mem-budget";
    return rec;
  }

  // ---- inputs: the small things first (calib.bin's settings, the data and setup dimensions): nothing that grows with the
  //      setup is allocated before the admission below (review PR52 MAJOR-2) ----------------------------------------------
  if (in.r < 1) throw Error(Status::invalid_input, std::string(W) + "the island index is required (--island r, or manifest params.id / params.island)");
  if (!plan_only && in.out.empty()) throw Error(Status::invalid_input, std::string(W) + "--out is required");
  if (!plan_only && in.seed < 1) throw Error(Status::invalid_input, std::string(W) + "--seed is required (a whole number in [1, 2^31 - 1])");
  auto t0 = std::chrono::steady_clock::now();
  const CalibHead C = read_calib_head(in.calib);
  if (C.mode != mode) throw Error(Status::invalid_input, std::string(W) + "calib.bin's mode is " + fmt::mode_name(C.mode) + ", not " + in.mode);
  if (mode == fmt::M_V && C.binary.type() == Json::OBJ) {   // D-32 (2), review PR55 m3: one fit = one class-A FMA family
    const BinaryCheck bc = isa_family_compatible(C.binary, binary_block_no_self_test());
    if (!bc.ok) throw Error(Status::invalid_input, std::string(W) + "calib.bin vs this binary: " + bc.reason);
  }
  if (in.seed > 0 && C.seed > 0 && C.seed != in.seed)
    throw Error(Status::invalid_input, std::string(W) + "--seed " + std::to_string(in.seed) + " differs from the calibration's seed " + std::to_string(C.seed));
  if (args.contains("N") && whole(args.at("N"), "N", 1, 1 << 24) != C.N)
    throw Error(Status::invalid_input, std::string(W) + "N differs from calib.bin's frozen N = " + std::to_string(C.N));
  // data.bin: n, p, K from the metadata (mapped; the arrays are read after admission, where the file is verified in full)
  std::string dhash; int64_t n = 0, p = 0, K = 0;
  { fmt::Reader R(in.data, false);
    if (R.kind() != fmt::K_DATA) throw Error(Status::invalid_input, in.data + " is not a data file");
    dhash = R.content_hash(); const Json m = R.json("meta");
    n = whole(m.at("n"), "data.bin n", 3, (int64_t)1 << 31); p = whole(m.at("p"), "data.bin p", 1, (int64_t)1 << 31); K = whole(m.at("K"), "data.bin K", 0, (int64_t)1 << 31); }
  const calib::Budgets bud = calib::budgets(n, p);   // B, K: the budgets the calibration ran with (calibrate uses the same helper)
  // D-29 (review PR54 MAJOR-1/2): tau_cal is checked HERE, before any island work, by the check read_calib uses: distinct
  // inherited models and tau_cal = the c-th best F, bit for bit. The mapped file was verified by read_calib_head already.
  if (mode == fmt::M_V) {
    fmt::Reader RC(in.calib, false); const Json cm = RC.json("meta");
    wp4io::check_calib_tau_cal(RC, cm, C.mode, (int32_t)p, (int32_t)K, in.calib);
  }
  if (bud.K != K) throw Error(Status::invalid_input, std::string(W) + "data.bin K = " + std::to_string(K) + " differs from min(p, n / 2) = " + std::to_string(bud.K));
  // B is part of the law (the N-swap labels per round: shuffled order, addresses, compat stream use). The calibration used
  // budgets(n, p).B, so the final islands must; a conflicting --B is refused (review PR52 MAJOR-3)
  if (args.contains("B") && whole(args.at("B"), "--B", 1, 1 << 16) != bud.B)
    throw Error(Status::invalid_input, std::string(W) + "--B differs from the engine's N-swap budget B = min(isqrt n, isqrt p, 16) = " + std::to_string(bud.B) + " (n = " + std::to_string(n) + ", p = " + std::to_string(p) + ")");
  const SetupDims sd = read_setup_dims(in.setup, p, (int)K, false);
  if (!sd.data_hash.empty() && sd.data_hash != dhash) throw Error(Status::invalid_input, std::string(W) + "setup.bin was built from another data.bin");
  if ((!C.data_hash.empty() && C.data_hash != dhash) || (!C.setup_hash.empty() && C.setup_hash != sd.content_hash))
    throw Error(Status::invalid_input, std::string(W) + "calib.bin's meta.inputs differ from the data.bin / setup.bin in use");

  IslandConfig c;
  c.seed = (uint32_t)std::max<int64_t>(1, in.seed); c.island = (uint32_t)in.r; c.role = IslandRole::Final; c.iter = 0; c.tier = (uint32_t)C.tier;
  c.N = C.N; c.grid = C.grid; c.L = C.L; c.Hm = C.Hm; c.B = bud.B;
  c.kernel = kernel_of(mode); c.threads = threads; c.G = G; c.tile = tile; c.compat = compat;
  // the setup inputs, the same number before the load and in the run: the mapped section bytes of the flat start law
  // (StartView) + its per-thread draw scratch + the neighbour lists (WP2's setup.bin); the expanded-Start model for a
  // minimal file the island must rebuild
  c.k_store = C.k_store; c.inputs_bytes = start_inputs_bytes(sd, threads);
  c.mem_budget = budget; c.leaders = false; c.keep_terminal = true;
  // the checkpoint's identity includes the three verified input hashes (review PR52 MAJOR-1): a restart on other inputs is refused
  c.input_id = input_identity(dhash, sd.content_hash, C.hash);
  // D-29 offer floor (V final islands; --offer-floor 0 runs without it: an execution switch, the merged science is the same)
  if (whole_arg(args, "offer_floor", 1, 0, 1) == 1) { c.offer_floor = C.floor.f; c.offer_floor_calib = C.floor.calib; }
  const bool ckpt = whole_arg(args, "ckpt", 1, 0, 1) == 1;
  if (ckpt && !plan_only) {
    std::string b = in.out; if (b.size() > 4 && b.substr(b.size() - 4) == ".bin") b.resize(b.size() - 4);
    c.ckpt_path = b + ".ckpt";
    c.ckpt_every_s = (double)whole_arg(args, "ckpt_every_s", 600, 1, 1 << 30);
  }
  rec["r"] = (double)in.r; rec["N"] = C.N; rec["T"] = (double)C.grid.size() - 1; rec["L"] = C.L; rec["Hm"] = C.Hm; rec["tier"] = C.tier; rec["B"] = bud.B;
  rec["n"] = (double)n; rec["p"] = (double)p; rec["seed"] = (double)c.seed;
  Json inputs = Json::object(); inputs["data.bin"] = dhash; inputs["setup.bin"] = sd.content_hash; inputs["calib.bin"] = C.hash;
  rec["inputs"] = inputs;

  // ---- admission (INTERFACES §7): the plan from the dimensions, before the data, the Start or the neighbour lists are
  //      read into memory. Same rule as plan_island (k = max(8, q90(pi_0 size) + 1, k_store)); the run's own admission
  //      sees the same numbers (test island_command_refusals_and_budget) ---------------------------------------------------
  MemSizes z = plan_sizes((int)n, (int)p, (int)K, c);
  const double kplan = plan_k(sd.size_logmass, C.k_store);
  const MemPlan mp = plan_with_budget(z, kplan, c);
  const bool admitted = budget == 0 || mp.total <= budget;
  rec["mem_plan"] = plan_json(mp, budget, c.inputs_bytes, sd.mappable ? "ESTIMATE (final island peak-live plan, memory.h; k = max(8, q90(pi_0) + 1, k_store); setup inputs = the mapped setup.bin sections + draw scratch + neighbours)"
                                             : "ESTIMATE (final island peak-live plan, memory.h; k = max(8, q90(pi_0) + 1, k_store); setup inputs = model of the rebuilt Start: the file lacks WP2's sections)");
  const std::string refusal = "mem_budget: predicted peak " + std::to_string(mp.total >> 20) + " MiB > budget " + std::to_string(budget >> 20) + " MiB [" + mem_plan_text(mp) + "]";
  if (plan_only) {
    rec["plan_only"] = true; rec["status"] = admitted ? "completed" : "resource_limit";
    if (!admitted) rec["reason"] = "island not admitted: " + refusal;
    return rec;
  }
  const Arith arith = mode == fmt::M_V ? Arith::ClassA : Arith::Bit;
  if (!admitted) {   // refuse before any allocation: the file carries the request's identity (mode, schedule) and no estimates (GUARD-W)
    IslandRun r; r.status = 3; r.reason = refusal; r.r = (int)in.r; r.N = C.N; r.p = (int)p; r.L = C.L; r.Hm = C.Hm; r.G_used = mp.G; r.mem_plan = mem_plan_text(mp);
    r.role = IslandRole::Final; r.tier = (uint32_t)C.tier; r.compat = compat; r.grid = C.grid; r.T = (int)C.grid.size() - 1;
    rec["island_bin"] = write_island_file(in.out, r, arith, inputs);
    rec["status"] = "resource_limit"; rec["reason"] = refusal; rec["G_used"] = mp.G;
    return rec;
  }

  // ---- read the arrays (the files are verified in full here), then run ------------------------------------------------
  Data D = prep::load_data(in.data, nullptr);
  if (D.n != n || D.p != p || D.K != K) throw Error(Status::invalid_input, std::string(W) + "data.bin changed between the metadata and the load");
  const StartView st = load_start_view(in.setup, D, sd.mappable, sd.content_hash);   // mapped: nothing of the start law is expanded
  if (sd.mappable && st.bytes() != sd.view_bytes) throw Error(Status::internal_error, std::string(W) + "the mapped start law differs from the planned sections");
  const Neighbours nb = load_neighbours(in.setup, D.p, !sd.mappable, sd.content_hash);   // the mapped loader verified every section; same file as the plan
  const double t_load = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  // WP7 O4: --stop-after-s S is a SOFT time stop measured from the start of this command (the load counts): at the first
  // step boundary after S seconds the island checkpoints and exits with the resumable outcome (exit 22, below)
  if (args.contains("stop_after_s")) {
    if (args.at("stop_after_s").type() != Json::NUM || !(args.at("stop_after_s").num() > 0)) throw Error(Status::invalid_input, std::string(W) + "--stop-after-s must be a number > 0");
    c.stop_after_s = std::max(0.001, args.at("stop_after_s").num() - t_load);   // the engine counts from the start of run()
  }
  const IslandRun r = mode == fmt::M_V ? run_island<Arith::ClassA>(D, st, nb, c) : run_island<Arith::Bit>(D, st, nb, c);
  if (r.status == 1 && r.time_stopped) {   // not a failure and not finished: no island file; the checkpoint is the result
    rec["status"] = "completed"; rec["island_status"] = "interrupted_resumable"; rec["reason"] = r.reason;
    rec["stopped_after_step"] = r.stopped_after_step; rec["resumed_from_step"] = r.resumed_from_step; rec["T"] = (double)C.grid.size() - 1;
    Json t = Json::object(); t["load"] = t_load; t["island"] = r.ks.t_total; t["ckpt"] = r.ks.t_ckpt;
    t["total"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count(); rec["seconds"] = t;
    return rec;
  }
  if (r.status == 1) throw Error(Status::internal_error, std::string(W) + "island interrupted without a stop request");
  const std::string fhash = write_island_file(in.out, r, arith, inputs);
  const Status s = r.status == 0 ? Status::completed : r.status == 2 ? Status::numerical_failure : Status::resource_limit;
  if (s == Status::completed && !c.ckpt_path.empty()) { std::remove((c.ckpt_path + ".a").c_str()); std::remove((c.ckpt_path + ".b").c_str()); }
  rec["status"] = status_name(s);
  if (!r.reason.empty()) rec["reason"] = r.reason;
  rec["island_bin"] = fhash; rec["output_hash"] = hex64(r.hash()); rec["init_hash"] = hex64(r.init_hash);
  if (s == Status::completed) rec["logZ"] = r.logZ;
  rec["G_used"] = r.G_used; rec["resumed_from_step"] = r.resumed_from_step;
  rec["start_source"] = st.source; rec["start_view_bytes"] = (double)st.bytes();
  Json t = Json::object(); t["load"] = t_load; t["island"] = r.ks.t_total; t["ckpt"] = r.ks.t_ckpt; t["store_check"] = r.ks.t_check;
  t["total"] = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  rec["seconds"] = t;
  return rec;
}

}  // namespace v4::island
