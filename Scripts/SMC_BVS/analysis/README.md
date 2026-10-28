# D assessment pipeline

Binding sources: deployment BRIEF including Amendments 1/2 and RULINGS_LEAD.md R-1/R-2/R-3. Local mock testing is authorized. No SSH/NOTS/Slurm or child agents are used. All writes belong to pipeline/. Historical benchmark reproduction belongs to the separate reproduction task. Results remain provisional until NEW independent final-source review and later production recount/review.

## One command: regenerate and validate all mock artifacts

From the workspace in PowerShell:

    python 02_Experiments/H_2026-10-22_smcbvs_v3_deploy/D_analysis/pipeline/run_local.py

R defaults to C:/Program Files/R/R-4.4.1/bin/Rscript.exe. Optional --rscript PATH and --benchmark-scoring PATH permit relocation. Every invocation creates fresh validation/local_*/ evidence and preserves failures. launch.json records argument arrays, PIDs, timestamps, environment, executable hash and actual exit. Inspect launcher.log, suite/verification_manifest.json and suite/verification_checks.csv. Exit zero and every check passed are required. The same command then verifies saved hashes and regenerates FREEZE.json, SOURCE_SHA256.csv, ledger/run candidates, STATUS.md and HANDOFF.md.

Sources, unchanged benchmark code/derived_rules, copied A adapter and binding ruling are frozen. The positive fixture is a D-OWNED SCHEMA-LEVEL MOCK, not execution/certification of A's updated adapter. Immutable pre-R1 A helpers supply native output extraction/layout; D mock rows and gzip record publisher implement binding R-1 fixture semantics. No sampler is fitted. Final A integration is PENDING an R-1-compliant handoff; the current published v1 is pre-R1 and is preserved as vendor/HANDOFF_v1.preR1.md. Rerun an actual frozen-A mock after the updated handoff. Earlier old-A debug evidence remains separate. R-1 schema branch tests precede fixture generation. The fixture is explicitly SYNTHETIC_NOT_PRODUCTION; the mapping itself comes from binding R-1 and A's adopted policy. Production mode rejects synthetic rows and obsolete/unadopted A output.

Baseline outputs include 120 datasets, 240 cases, 480 expected SMC rule rows (474 observed deliberate gaps), all benchmark/derived summaries, paired comparisons, T4 case-level uncertainty, T5 runtimes, diagnostics/failures and 28 SVG figures. Mock benchmark table equality includes types; it is not historical reproduction evidence. Source/input/output SHA-256 files, commands, R environments and logs are retained.

## Assessment preparation

prepare_assessment_config.py reads all18 reproduction/runs.tsv entries. --scored-root points to reproduction/local_outputs: c100 resolves to combined_v3_v7/runs/<run_id>; c050 to combined_c050_v7/runs/<run_id>. --source-map permits explicit per-run overrides. No reproduction files are edited. --canonical-root is the published scoring/out archive. All eleven canonical CSV claims are explicit; unavailable originals are disclosed, never counted as matched. Full-design tables regenerate before selection; the separate reproduction report owns full historical reproduction.

Required arguments: python prepare_assessment_config.py --help. --mapping-ruling defaults to the frozen vendor/RULINGS_LEAD.md, whose full-file SHA-256 is pinned. No invented policy JSON or exhaustive native-flag lookup is needed. --mapping-csv is optional fixture audit only. C's inspected output manifest and raw bundles are required.

    python run_pipeline.py --config assessment.json

Outputs remain under the owned pipeline folder. Actual assessment requires the lead G1/destination decision. run_owls.sh is an optional, unexecuted wrapper: nice19, one numerical thread, shared load/memory gates. R-3 allows D4 during build and D2 during C batch; the wrapper uses one. No Owls-only rule applies to local development.

HANDOFF.md describes the completed freeze when available. No production RESULTS claim is made. New independent code review, inspected C outputs, independent >=30-cell raw-support/truth recount and lead review remain gates. A cancelled reviewer is never counted.


For debugging only, verify_fixture.py --reuse-fixture PATH first verifies prior baseline input hashes and copies the existing fixture. freeze_evidence.py refuses recovery runs: the final run_local.py command always generates a clean fixture. Memory/job-limit observations and subprocess command/PID/timestamp/exit/log hashes are saved. Audit-finalization failures retain the original failure and remain failures.

The same command now includes actual A development smoke schema tests at the user-specified smoke_records/dev500 and dev1000 paths. Originals remain untouched. It records legacy expected R-1 rejection and clearly labelled D-owned R-1-adapted positives without production or truth scoring. FINDINGS_CLOSURE.md maps review F1-F4 to rejecting native-consistency mutations. Final actual updated-A integration and fresh independent review remain gates.
