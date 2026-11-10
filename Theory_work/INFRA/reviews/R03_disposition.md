# R03 disposition (review: R03_review_astra.md, REJECT 6.5/6/7.5)

All items accepted. Regression suite `tools/test_lifecycle.py`: 21/21 PASS (10 R01 + 6 R02 + 5 R03 scenarios), in a disposable worktree copy.

| item | disposition |
|---|---|
| N1 MAJOR: a status change keeps stale provenance | Fixed. downgrade, retract and deprecate save the validated `--status-source` with the status. Scenario R03-N1. |
| N2 MAJOR: a self-bound `consumes` vanishes | Fixed. `P:X@<self>` is recorded as a self-edge (ERROR C3-self). Binding refs resolve ticket-locally like depends_on. Scenario R03-N2. |
| F2 (partly): exited intermediate parent hides grandchildren; snapshot errors; removal unchecked | Fixed with a Windows Job Object. Every process a script spawns joins the job by inheritance, so orphans whose parent exited are still members. The job has KILL_ON_JOB_CLOSE, is terminated in `finally`, and is polled until zero processes are active (bounded at 20 s, then raises). Verified: a 5-process tree whose parent stays alive is fully killed. Parent-pid kill is kept as a second line of defence with bounded retries; this also fixes the calibration abort caused by a 0.5 s kill window. A failed snapshot now raises (fail closed). A failed sandbox removal prints a warning. |
| F5/F6 (partly): "Not yet PROVED-CHECKED"; a status borrowed from the next line | Fixed. One shared locator, `bvsreg.status_at`, is used by C10, propagate `--status` and registry add/correct-status. The match must START on the stated line and must not be preceded (within two words) by not / no / never / un / pending / without. Eight real rows pointed one or two lines early; their sources were corrected through `correct-status`. Scenarios R03-F6. |
| F8 (partly): confirm/revert ignore bound `consumes` | Fixed. Confirmation and revert recognise `proof:P:X` uses that come from `consumes` bindings and swap the binding (`P:X@src` → `P:X@dst`, and back on revert). |
| F10 (partly): `README.md:1` and `README.md:01` count twice | Fixed. Routes are deduplicated by canonical `(path, a, b)` from the first token (`bvsreg.span_key`), which is also the format `fail-route` validates. Scenario R03-F10. |
| F7 (partly): POST line 33; PLR unsplit | Documented limitation. Registry spans are line-granular, and POST's line 33 both ends the SL1 clause and opens the inclusion clause; the scope note records the exclusion. Splitting PLR (C-i/C-ii), F-LOC2 classes and the other split-needed rows is a curation task for HQ (list in R01 disposition #12, plus S5:L1 L1.3 and XA:L1 L1b/c). Their strength fields carry explicit notes and are not used by the optimizer. |
| F9 (partly): coverage | Per-id fixes below. Complete coverage is ongoing curation; the check makes drift visible. Never-reviewed LaTeX stays a WARN with a visible flag in the generated block, since publication is a human act. A CHANGED transcription is an ERROR. |
| §5.3 vs planner | LIFECYCLE §5.3 now describes restoration onto the latest valid source in the re-point chain. |

Per-id: `W2-LOC2:Lemma-BC` now uses the CT block-inverse/Rayleigh argument instead of CD. `W2-FAC-S5:L1` hashes L1.1–L1.3 (44–67) as premises and is marked split-needed. `W1-GEN:L8` hashes the H2a–H2c definitions (STATEMENT 64–75). `W2-FAC-XA:L1` hashes L1b and L1c (35–42, 56–77) and is marked split-needed.
