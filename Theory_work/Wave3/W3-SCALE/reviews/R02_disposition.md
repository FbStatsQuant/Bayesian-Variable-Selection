# R02 (Sol, blind re-read of the final code) — disposition by the lead, 2026-11-11

Review: `R02_code_sol.md` (Codex gpt-6.1-sol, reasoningEffort high; blind first read of `core_v32dev` at bbdfea0 and
of the tests). Verdict received: **NOT ESTABLISHED** — no numerical mismatch found (the author's 49 cases, 116
private cases, 20,000 extreme finite Gram cases, the export test, four fits), but the comparison gate accepted
invalid evidence and one README statement was false. All four findings are accepted. **No C++ or R core file changed
after this review**: the tested code is still bbdfea0; the changes are in the comparison and test scripts and in the
README wording.

| # | severity | finding | disposition | where |
|---|---|---|---|---|
| 1 | MAJOR | `bitid_compare.R` was not fail-closed: two records without fingerprints compared equal; unequal admission decisions only reported; an unpaired B record invisible | **Fixed.** A unit passes only with two records naming the same unit, version-2 fingerprints with a 64-hex hash and a non-empty field table, equal admission decisions and equal hashes. Verdicts IDENTICAL / DIFFERENT / ADMISSION_DIFFERS / INVALID / MISSING_A / MISSING_B; both inventories are enumerated; the expected unit count is a required argument; the two labels must come from two different compiled cores. Negative tests run locally (version-1 records, wrong count, same label twice, unpaired B record, changed admission): all exit 1. | `scripts/bitid_compare.R`; LOG entry |
| 2 | MAJOR | The raw-export guarantee for NaN correlations rests on v3.1's `stable_sort` with a comparator that is not a strict weak order there: undefined by the language, so "calls the same routine" is not a guarantee across separately compiled binaries | **Accepted; claim narrowed.** README: outside finite inputs with numeric correlations the statement is "the v3.1 code itself is run; equal on the tested cases", not a guarantee; v3.1 is itself not reproducible by specification there. No new NaN ordering is defined (that would be a behaviour decision, not leg A's). The unit cases `zero_column_p4` and `underflow_column_p9` now assert that they mix NaN and numeric correlations. | `core_v32dev/README.md`, `tests/bitid_units.cpp` |
| 3 | MINOR | "A pivot fails after the H pivot passes" is reachable by rounding (finite reproducer with two equal huge columns); the README called it unreachable | **Fixed.** README corrected. Sol's reproducer is the unit case `a_pivot_after_h`, which asserts that `chol_inplace` passes on H and fails on A for the model {0, 1} and that the QR route is taken; dumps identical under both cores. | `core_v32dev/README.md`, `tests/bitid_units.cpp` |
| 4 | MINOR | The self-test counted mutations that did nothing (zero or infinite log Z; fields absent on early returns; fallback to mutating `seed`); no input gave a vacuous pass | **Fixed.** A mutation that leaves the fit unchanged is reported "not applicable" and not counted; the summary reports detected / applied; no input file or no applied mutation is a failure. | `scripts/fingerprint_selftest.R` |

Sol's supporting checks recorded here because the checkpoint cites them: signed zeros, subnormals and finite overflow
in the Gram; late NaN and Inf columns; non-finite y and z; n = 1..4; p at every tile boundary; the failure replay.
None produced a difference between v3.1 and v3.2-dev.
