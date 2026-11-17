// island_lm_state.h -- the label-major group state (owned with island_lm.h; WP3_ARCH_REVIEW §4). A namespace-scope type
// so that the engine (island_run.h) can hold it as a member while the label-major code lives in island_lm.h.
#pragma once
#include <atomic>
#include <exception>
#include <memory>
#include "v4/island/island.h"

namespace v4::island {

// Per-thread label-major scratch (review PR48 finding 1): sized serially before the parallel regions, so no allocation
// happens inside an OpenMP region outside the oom_guard (an escaping std::bad_alloc would std::terminate). Grows only.
struct LmScratch {
  std::vector<uint8_t> inm;                    // Bk: member flags of a tile
  std::vector<uint64_t> needw, consw;          // Bk / 64: needed (phase A) / consumed (phase B) label bits of a tile
  std::vector<int> nlist, first;               // Bk + 1: listed bits; Bk: first consuming particle per label
  std::vector<uint32_t> ord;                   // m: one round order (K2: only the inverse is kept per particle)
  std::vector<uint32_t> ncons, fpos;           // Bk: consumption counts and positions per label
  std::vector<v8d> ub;                         // max k: one 8-lane Gram vector per member
};

// --- label-major round for the particles [g0, g0 + gN) ------------------------------------------------------
struct LmGroupBuf {
  std::vector<int> pid;                        // particle of each slot (K5: slots are reused within a round)
  std::vector<uint32_t> inv;                  // gN x m: 1-based position of each label (K2: the order itself is not kept)
  std::vector<std::vector<std::pair<uint32_t, int>>> ng;   // per particle: (position, label) of U/N/I labels, sorted
  std::vector<uint32_t> q, e; std::vector<uint8_t> done, etype; std::vector<Particle> pending;
  std::vector<int32_t> elab;                  // the label at e of a Gibbs event (etype 1)
  // running first change per particle, packed (position << 32) | label (K2: positions are distinct, so the minimum by
  // position carries its label and the order is not needed to find it); UINT64_MAX = none
  std::vector<std::atomic<uint64_t>> fmin;
  // the I step's proposal per particle, drawn and scored in the order phase (K2); a failed score is kept and raised
  // only when the walk reaches the I position (the event that core would fail at)
  std::vector<Particle> iprop; std::vector<std::exception_ptr> ierr;
  std::vector<SupportCache> sup; std::vector<int> sup_of;
  std::vector<std::vector<int>> sup_parts;     // particles (group-local, ascending) per support
  std::vector<int> act;                        // active columns
  avec<double> XA;                             // |loc| x n: the columns whose products this pass computes
  // K3 (WP3_ARCH_REVIEW §2.2): Gram rows of active columns kept across the passes of a group, and across groups and
  // rounds while the column stays active. Row r = X^T x_col, p entries with the bits of tile_products. A column gets a
  // slot the first pass it is active (that pass's tile sweep writes the row) and loses it at the first pass in which no
  // fast support that can add holds it. Values depend on the column only, so nothing here is checkpointed.
  std::unique_ptr<double[]> GR; int gr_slots = 0;   // gr_slots x p, uninitialised until a row's first pass writes it
  std::vector<int> slot_col;                   // column of each slot, -1 = free
  std::vector<const double*> act_gr;           // per active column: its row, computed in an earlier pass, or nullptr
  std::vector<int> act_local, act_newslot;     // per active column: product row in this pass (-1: cached); slot it fills (-1: none)
  std::vector<int> loc;                        // the active columns computed in this pass: new (with a slot) first, then no slot
  std::vector<double> lbuf, obuf;              // nsup x p
  std::vector<LmScratch> scr;                  // one per thread
};

}  // namespace v4::island
