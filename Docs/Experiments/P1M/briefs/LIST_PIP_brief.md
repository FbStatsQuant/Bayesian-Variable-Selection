# Brief: list-renormalised PIP fields in core v3 and engine v4 (HQ order 11-17; owner-approved; additive output only)

Spec (binding): briefs/SPEC_LIST_PIP.md (copy of theory/W3-AUDIT 523dda23, SPEC_LIST_PIP.md, 80 lines). Read it in full.

## What to build
Fields: pip_list, mpm_list, log_Z_list, list_size, list_full, pip_list_source, pip_list_flag (spec §5).
They are computed LAST, read no random numbers and change no state. Log-sum-exp, and both sums run from the last store entry to the first in plain double.
- **Core v3** (`Scripts/SMC_BVS/core/`, the theory's pinned method: additive output only, no other edit):
  - SMC branch: compute from `out$top_store` after everything else in `v3_run.R`.
  - Exact branch (`v3_fit.R:120-127`): follow spec §4.
  - Other statuses: the fields are absent.
  - Doc line in `core/README.md`.
- **Engine v4:** compute from the MERGED top store in the merge, after everything else, and write the fields to fit.bin and fit.json. Keep the existing PIP_T exactly as it is (it is not this quantity's numerics). Add an INTERFACES line (next free version: #64 and #65 both claim v0.1.25, so take the next one after whichever lands) and a doc line in the engine README.
- **Post-hoc tool** (v4): `smcbvs4 listpip FIT.bin` (or a tools/ script that calls the SAME function) prints the fields for an existing fit.bin.

## Acceptance (spec §7, all 12)
- **A1–A3 (bit identity):**
  - v3: the 24 + 10 production-hash cases plus one fit per status path; every existing field `identical()`.
  - v3: removing the new fields gives the old serialised hash.
  - v4: WP4 golden (540,419 checks / 0) and T3 hashes unchanged; every existing fit.bin section's hash unchanged on a test merge.
  - Same seed run twice → the new fields are identical.
- **B4–B11:** hand cases as unit tests in BOTH implementations; v4 tests through the same function the merge calls.
- **B12:** v3 vs v4 on the golden set: pip_list and log_Z_list within 1e-12, mpm_list identical (report any case within 1e-9 of 0.5).

## Confirm in the PR description (spec flags these as unverified)
- (a) Does v3's exact branch return `top_store`? If not, which path does spec §4's alternative apply to?
- (b) What is v4's equivalent of `top_store`: which store, its capacity, its order, and does it hold distinct models?
- (c) Post-hoc: can the fields be computed from the stored fit.bin of the 1M pilot (replicate 1, 6-AR-n200-r01-V-s1) and T5? Show the tool on a local 10⁴/10⁵ fit.bin and state whether those runs' fit.bin carry the full merged store. Do not touch NOTS.

## Rules
- Branch `exp/P1M-list-pip` from exp/P1M-engine (stacked on #65 if #65 is still open, since both touch merge/wp4_io), one PR.
- Owls only, ≤ 3 threads, one suite at a time, TMPDIR in your own folder.
- core/ files are hashed in theory manifests. Change only what the spec needs. HQ tags the merge commit and Theory bumps method_commit.
- Report: the PR URL, the head, the test counts, (a)/(b)/(c), and any spec ambiguity you hit (ask rather than guess).
