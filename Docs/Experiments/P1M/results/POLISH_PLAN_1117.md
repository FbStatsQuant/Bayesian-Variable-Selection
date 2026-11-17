# Engine polish workstream (owner mission 11-17: "a highly polished engine"; Engineering plan, no dates moved)

State today (exp/P1M-engine): README.md is a 32-line WP1-era internal note; INTERFACES.md (704 lines) is the binding
contract but not a user guide; run docs live in tools/slurm/T5_AND_PILOT.md + T6_AND_RESTART.md; 25 test files,
tests/run_tests.sh --quick|--full; driver = tools/slurm/p1m_driver.py + p1m_cells/cost/manifest.py.

## Rule: polish never touches the science path before the 1M block
- Docs, help text, the test harness and the driver's front end: any time, on branch exp/P1M-polish, merged after review.
- Code on the CLI/message path: merged only if T3 hashes + goldens + one 10⁵ island hash are unchanged (the freeze check).
- island/merge/setup source changes: after the 1M block (≈ 12-08), or by a freeze amendment through HQ.
- The campaign keeps running the frozen driver version; polished driver features ship in the release.

## Items (one Sonnet polish builder, continuous, inside the cap of 3; Sonnet reviews; one Codex at the release gate)
| # | item | when |
|---|---|---|
| P-1 | User README: what it is, install (GCC/CMake/OpenMP), 5-minute example at p = 10⁴ on one node, then SLURM; outputs explained (fit.json fields, PIP_eq / PIP_T / list-PIP) | 11-18 – 11-22 |
| P-2 | REPRODUCIBILITY.md: what "same bits" guarantees (thread count, schedule, restart), ISA/libm pin, how to verify hashes, restart/checkpoint guide (from T6 doc) | 11-18 – 11-22 |
| P-3 | Error catalogue: every status / exit code → meaning → what to do; audit that each message names the file, value and limit | 11-22 – 11-26 |
| P-4 | CLI `--help` per subcommand, consistent flag names, `smcbvs4 version` prints build + ISA + libm pin | 11-22 – 11-26 |
| P-5 | Driver ergonomics: `plan validate`, `--dry-run` (task list + cost + memory before submit), `status`, `resume`; one example plan per use | 11-26 – 11-30 |
| P-6 | Test suite: one `ctest`/`run_tests.sh` entry, quick suite time budget, test names by component, golden refresh procedure documented | 11-26 – 11-30 |
| P-7 | Usability check: a fresh Haiku/Sonnet agent with ONLY the README builds and runs the example on Owls; every stumble → fix | ≈ 12-01 |
| P-9 | Data importer: `smcbvs4 import` from CSV / R / numpy into raw.bin (a newcomer can only use `gen` today; needed for the real-data example) | after the freeze, ≈ 11-23 – 11-27 |
| P-10 | Driver site config: NOTS account / partition / qos / modules / folder guard moved to a site file; a generic SLURM template | ≈ 11-27 – 12-01 |
| P-8 | Release v4.0: CHANGELOG (from INTERFACES history), tag, API/file-format doc frozen; Codex release review | after the 1M block (≈ 12-08 – 12-10) |
