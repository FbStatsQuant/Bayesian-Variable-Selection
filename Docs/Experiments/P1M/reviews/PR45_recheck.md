# PR #45 re-check — `bf7daa23` → `f6567dc0` (PR45 review fixes + INTERFACES v0.1.15, D-29 offer floor)

Reviewer: Sonnet 5.5 sub-agent, independent of the author. 2026-11-16. Read only: no push, no GitHub comment, no branch
change. Checkout: detached `origin/exp/P1M-wp1-store-perf` = `f6567dc0`, in my own worktree.
Inputs: `reviews/PR45_review.md`, `reviews/D29_WP4_answer.md`, `briefs/REVIEW_PR_template.md`.

## Verdict: **MERGE** (0 CRITICAL, 0 MAJOR, 4 MINOR, 4 INFO)

All four MINORs and INFO-1 of the first review are fixed as claimed, and the new tests pass. The v0.1.15 text matches
WP4's note point by point. The MINORs below are contract gaps that builder 7 would have to guess at. They are wording
changes, no code is affected. Fold them into the builder-7 PR (O6) or a v0.1.16 line. None of them needs to hold the
merge back.

## 1. Are the first review's findings fixed?

| finding | where | result |
|---|---|---|
| MINOR-2, `compact()` comment | `INTERFACES.md:164` | Fixed: "one entry per model, its best value". |
| MINOR-2, `load_unique_sorted` preconditions | `INTERFACES.md:166, 174-181`; `store.h:35-42` | Fixed: empty target (else `internal_error`), n ≤ cap refused and never truncated, store left empty after a refusal, "same bits" for valid input only. This agrees with the first review's code reading (§(a)). |
| MINOR-2, §5.1 conditional fields | `INTERFACES.md:336-358` | Fixed, and I checked each against `write_calib` (`src/merge/wp4_io.cpp:165-215`): `iterations` rows (`tier`, `iteration`, `grid_label`, `complete`, `logZ_r`, `island_best`; `overall_best` and E1–E3 only when `complete`) ✓; `k_store`, the stores, HPM, `logical` and the inherited models only when ok ✓; `inh_d` only on the flat path ✓; `grid` only when frozen ✓; `stage_stream` ✓. |
| MINOR-1, §7 memory rule ahead of the code | `INTERFACES.md:477` and the changelog | Fixed by the first review's option 1: the rule is marked "effective with WP4 PR #46". See INFO-4 for the merge order. |
| MINOR-3, test of the eval refusal | `tests/wp5/test_eval.cpp:208-237` | Added: ok / duplicate not adjacent / wrapping offset. **PASS** (`wp5_load_fit_refuses_duplicate_model`). The `ok` file accepted proves the duplicate and wrap files fail for their own reason. |
| INFO-1, overflow-safe pool bound | `src/eval/io.cpp:24-25` | `len > c \|\| off > c − len`: correct, no wrap. The wrap test (`UINT64_MAX − 1`, len 2) would have passed the old `off + len > c` and then read out of bounds. |
| MINOR-4, verify in `read_island_file` | `src/island/island_file.cpp:98-107` | Correct: under `verify` the labels are checked in [0, p) before `zob.hash` reads `key[j]` (no out-of-range read), and the stored hash must equal `zob.hash(S)` (`Zobrist::init(p)` is the same table the engine uses; the round-trip test reads real islands with `verify = true` and passes). `p ≤ 0` is refused. Tests at `tests/test_island.cpp:383-397`: a wrong hash → `invalid_input` with `verify`, accepted without it; a label `p` → `invalid_input`. **PASS** (`island_file_roundtrip_and_terminal_supports`). See INFO-1. |

## 2. INTERFACES v0.1.15 against WP4's offer-floor note

| WP4 point | v0.1.15 text | match |
|---|---|---|
| `calib.bin meta.tau_cal` = c-th best F, c = 40p+1, HPM order, distinct inherited models that calib.bin exports; −∞ if fewer; only for a completed V-mode calibration | `:348-351` | ✓. Encoding `tau_cal_hex` (authoritative) + `tau_cal` ("-Inf" for −∞): matches `Json`'s non-finite output (`src/common/json.cpp:63`) and the existing `logZ_hex` convention. |
| `island_r.bin meta.offer_floor` + calib hash | `:357-360`: `offer_floor_hex`, `offer_floor`, `offer_floor_calib` (null at −∞); an absent key means −∞ | ✓ |
| Drop only v < floor, ties kept; store = top c of offers ≥ floor, may hold fewer than c; I1 unchanged; HPM, counters, island_best, Tally see every event | `:198-204` | ✓ |
| Merge, after tables + inherited: floor ≤ `pre.top.cutoff()` (≤), else `invalid_input` under GUARD-W, no estimate | `:467-475` | ✓ |
| Floor > −∞ only for V-mode final-run islands; compat, law and calibration islands must have −∞, merge refuses otherwise | `:469-470`, `:208-209` | ✓ in wording, but see MINOR-2 (cannot be checked for calibration islands) |
| Floor-hash / calib-hash mismatch refused | `:471` | ✓ |
| Floors as exact bits in `_hex` keys | `:350, 357` | ✓ |
| §4/§5 line on floored stores | `:205-209`, `:359-360`, `:373` (fit.bin: the merged `top_*` is the only store with meaning) | ✓ |
| Memory estimate unchanged, kbar still an upper bound | `:474-475` | ✓ |

The safety argument also holds: dropped offers are < f ≤ pre-island cut-off, and the cut-off only rises, so no dropped
offer could be in the merged top c. Duplicates are not affected (the store keeps the best value, and a worse duplicate
below the floor changes nothing). Only the top store is affected.

### Findings

#### MINOR-1 — the contract does not say where the floor is applied or how `island::run` gets it
- **Where:** `INTERFACES.md:198-204` (floor paragraph), `:160-170` (`Store` API), `:236` (§4.2 "dropped if v < island.store.cutoff()"); `include/v4/island/island.h` (`IslandConfig` has no floor field).
- **Evidence:** the text says "the store drops an offer iff v < f, in addition to its own cut-off rule". The `Store` listing has no floor, and §4.2's quick-reject line and §7 rule (4) (thread-invariant quick rejects against the monotone cut-off) do not mention it. Three things are open for builder 7:
  1. the carrier (a `Store` member, a `LedgerConfig` field for the `top` store only, or the offer buffer);
  2. that `cutoff()` is unchanged (still −∞ below cap entries, so the effective threshold is max(cutoff(), f)) and that `would_enter` / `merge(Store)` / `load_unique_sorted` / `compact` do not apply the floor;
  3. the source of f: read automatically from the manifest's `calib.bin meta.tau_cal` for V-mode final runs, or passed by the caller. What happens when `tau_cal` is absent (older calib.bin, compat or theory-mode calibration, or a V calibration with fewer than c inherited models) is also unstated. The natural rule is f = −∞ with `offer_floor_calib` null.
- **Fix:** one sentence each in §4.1 and §4.2: "the floor is a constant of the island's `top` store (a `LedgerConfig` field); the effective reject threshold is max(cutoff(), f); the other `Store` operations are unchanged. `island::run` reads f from its calib.bin `meta.tau_cal_hex` when the mode is V and the run is a final run, else f = −∞. A missing `tau_cal` means f = −∞."

#### MINOR-2 — "calibration islands with a floor are refused by the merge" cannot be checked
- **Where:** `INTERFACES.md:208-209`, `:469-470`.
- **Evidence:** calibration islands run in process and never write an `island_r.bin` (`island.h:56`: leaders are "never written to island_r.bin"; calibration stages live in `calib.bin`'s stage records). `island_r.bin meta.mode` is only `compat`, `V` or `law` (`island_file.cpp:28`); there is no role field. So the merge can refuse `compat` or `law` with a floor, but "final-run vs calibration" is not observable in the merge. The real guard for a calibration island is on the island side (`island::run` with `leaders = true` or any calibration role), and the text puts it on the merge.
- **Fix:** split the clause: (a) `island::run` refuses a floor > −∞ with `invalid_input` when `compat`, `Arith::Bit` (law), `leaders` or a calibration role; (b) the merge refuses a floor > −∞ unless `meta.mode` = "V".

#### MINOR-3 — floor value is not tied to the calib.bin's `tau_cal`, and non-finite floors are unspecified
- **Where:** `INTERFACES.md:469-472`.
- **Evidence:** the merge checks only that `offer_floor_calib` equals the island's `meta.inputs` calib hash and floor ≤ cut-off. An island that writes any smaller floor with the right hash passes. This is safe for the merged store (the ≤ rule is the real guard), but it defeats the "f = tau_cal" contract and would hide a builder bug (a floor computed over a different set of models). The merge already reads that calib.bin (`wp4_io.cpp:823`, `read_calib`), so the check costs nothing. Also unstated: NaN or +∞ floors. NaN is refused implicitly by `≤`, +∞ only passes against a +∞ cut-off.
- **Fix:** add "and `offer_floor_hex` is bit-equal to that calib.bin's `tau_cal_hex`; a floor is −∞ or finite (NaN, +∞ → `invalid_input`)". Both for the island reader and the merge.

#### MINOR-4 — "every reader of an untrusted file checks each stored hash" is too strong
- **Where:** `INTERFACES.md:174-176`.
- **Evidence:** it names WP4 `read_store`, `load_island_full` and WP3 `read_island_file(verify)`, which is correct. But the WP5 `load_fit` (`src/eval/io.cpp:26-40`) also does a one-per-model check by (hash, model) and does not verify hashes (it has no Zobrist). A fit.bin with one model under two hashes would pass it. The risk is small (fit.bin is the engine's own output, content-hashed), but the binding text says "every".
- **Fix:** "the readers listed here check the hashes; `load_fit` relies on the fit.bin's own content hash", or drop "every".

#### INFO-1 — the label test of MINOR-4 is not isolated
`tests/test_island.cpp:391-395`: the bad-label file also has a wrong hash (the stored hash is the original model's), and there is no `verify = false` counterpart. A hash-only implementation would also pass. Build the hash with a `Zobrist` over p + 1 labels (so only the label is wrong), assert `verify = false` is accepted, and add a negative label. The code itself is correct (labels are checked first, per entry).

#### INFO-2 — `zob.init(p)` allocates from `meta.p` (`island_file.cpp:99-100`)
A hostile but content-hash-valid file with p ≈ 2³¹ asks for 16 GB. This is not new: `led.init(lc)` on the line above already sizes by p. No action.

#### INFO-3 — WP4's last bullet is not in the contract
WP4's note (a) asks WP3/WP7 to confirm that `island_run` writes nothing derived from its own store besides the store itself (e.g. a per-island log Z_T or PIP_T). v0.1.15 says no consumer may use the store alone but does not state "every `island_r.bin` field except `top_*` is floor-independent" (log Z_r, `pip_r`, ess, terminal supports, HPM, counters, island_best). One sentence at `:359-360` would close it.

#### INFO-4 — merge order with WP4 PR #46 (carried over from review MINOR-1)
`origin/exp/P1M-wp4-calib2` (`12931094`) still has the stale citation `INTERFACES v0.1.12` at `calib_run.h:67` and `26.0 + 4.0 * kbar` at `:80`. This branch has v0.1.13 and `30.0 + 4.0 * kbar` at `:65, :73`. Expect a textual conflict. Whoever merges second keeps 30 + 4k and the v0.1.13/§5.1 citation, as the first review said.

## 3. Test run (Owls, `nice -n 19`, `--threads 3`)

`TMPDIR=/home/fb31/SMC_Engineering_Department/tmp/20261116-recheck-45 tests/run_tests.sh --quick --threads 3`, head
`f6567dc0`, GCC 11.5.0, flags `-O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2`, load average 24–29 from other
jobs.
- **114 PASS, 0 FAIL** (113 before, plus `wp5_load_fit_refuses_duplicate_model`). `island_file_roundtrip_and_terminal_supports` (extended) passes.
- WP5 Slurm driver: 17 tests OK. Competitor harness: OK. Install script: 23 checks OK.
- **WP4 golden: 443,598 checks, 0 failures.** Exit code 0.
- I did not repeat the first review's `adv.cpp` and fit.bin comparisons: the diff touches none of the store, merge or fit-writer code (`store.h` is comment-only), so those results stand.
- Cleanup: the TMPDIR folder is removed after this note is written. No sub-agents, no NOTS. Nothing written outside the
  TMPDIR and this file.
