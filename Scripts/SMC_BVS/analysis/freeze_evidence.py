"""Inspect a completed mock suite and freeze source/evidence handoff inside pipeline only."""
import argparse
import json
from pathlib import Path
import sys
from run_pipeline import ROOT, OWNER, sha, read, write, utc, PINNED, RULING_SHA256


def freeze(evidence):
    evidence=evidence.resolve()
    if not evidence.is_relative_to(OWNER): raise ValueError("evidence outside owned pipeline")
    launch=json.loads((evidence/"launch.json").read_text())
    suite=evidence/"suite"; state=json.loads((suite/"verification_manifest.json").read_text())
    checks=read(suite/"verification_checks.csv")
    r1_checks=read(suite/"r1_branches"/"r1_checks.csv")
    if len(r1_checks)!=26 or any(r["passed"]!="TRUE" for r in r1_checks): raise ValueError("R-1 branch evidence incomplete")
    if state.get("fixture_reused"): raise ValueError("debug recovery is not a clean final run")
    smoke=json.loads((suite/"actual_smoke"/"smoke_integration.json").read_text())
    original_files=read(suite/"actual_smoke"/"originals_sha256.csv")
    if len(original_files)!=8 or any(sha(r["path"])!=r["sha256_before"] or r["sha256_after"]!=r["sha256_before"] for r in original_files):
        raise ValueError("actual A smoke originals changed")
    controls=read(suite/"native_controls"/"native_control_checks.csv")
    if not controls or any(r["passed"]!="TRUE" for r in controls): raise ValueError("native branch controls incomplete")
    closure={
      "F1":["hpm_disagrees","pip_disagrees","bad_preprocessing_map","wrong_native_pip_names"],
      "F2":["native_status_disagrees","reverse_failure_status","degenerate_status_disagrees"],
      "F3":["missing_native_payload","missing_native_pip","missing_native_stage","missing_island_evidence","missing_native_streams","missing_bound_label_certified","missing_bound_label_uncertified","native_json_disagrees",
            *["json_"+nm for nm in ("cut_group_count","cut_group_components","local_limit","local_certified","global_certified","near_tie_truncated")]],
      "F4":["missing_failure_audit","changed_failure_audit","null_failure_as_NA","unavailable_failure_as_empty"]}
    passed={r["check"] for r in checks if r["passed"] in {"TRUE","True"}}
    for finding,names in closure.items():
        if any(name+" adapter" not in passed for name in names): raise ValueError("finding regression incomplete: "+finding)
    if launch["exit_status"]!=0 or state["status"]!="passed" or not checks or any(r["passed"] not in {"True","TRUE"} for r in checks):
        raise ValueError("cannot freeze failing or incomplete suite")
    verified=0
    for manifest in (suite/"verification_outputs_sha256.csv",suite/"baseline"/"outputs_sha256.csv"):
        for row in read(manifest):
            if sha(manifest.parent/row["path"])!=row["sha256"]: raise ValueError("saved output hash mismatch: "+row["path"])
            verified+=1
    source=[]
    for path in sorted(ROOT.iterdir()):
        if path.suffix in {".py",".R",".sh"}:
            snapshot=suite/"source_snapshot"/path.name
            if not snapshot.exists() or sha(path)!=sha(snapshot): raise ValueError("code changed after run: "+path.name)
            source.append(dict(path=path.name,sha256=sha(path),bytes=path.stat().st_size))
    for path in sorted((ROOT/"vendor").rglob("*")):
        if path.is_file():
            frozen=suite/"source_snapshot"/path.relative_to(ROOT)
            if not frozen.exists() or sha(path)!=sha(frozen): raise ValueError("vendor changed after run")
            source.append(dict(path=str(path.relative_to(ROOT)),sha256=sha(path),bytes=path.stat().st_size))
    write(ROOT/"SOURCE_SHA256.csv",source)
    baseline=suite/"baseline"; metrics=read(baseline/"study_metrics_mcse.csv")
    freeze=dict(frozen_utc=utc(),evidence=str(evidence),checks_passed=len(checks),r1_branch_checks_passed=len(r1_checks),output_hashes_verified=verified,
        source_manifest_sha256=sha(ROOT/"SOURCE_SHA256.csv"),verification_manifest_sha256=sha(suite/"verification_manifest.json"),
        verification_checks_sha256=sha(suite/"verification_checks.csv"),launch_sha256=sha(evidence/"launch.json"),
        ruling_sha256=RULING_SHA256,benchmark_pins=PINNED,independent_review="pending NEW final-source review",
        final_A_integration="PENDING formal R-1 A handoff and rerun; current passing fixture is D-owned schema-level mock",
        review_r2_sha256=sha(ROOT/"vendor"/"REVIEW_r2_REQUEST_CHANGES.md"),finding_regressions=closure,
        actual_smoke_report_sha256=sha(suite/"actual_smoke"/"smoke_integration.json"),actual_smoke_originals_unchanged=8,
        native_control_checks_passed=len(controls),
        historical_reproduction="owned by separate task; mock equality is not historical reproduction")
    (ROOT/"FREEZE.json").write_text(json.dumps(freeze,indent=2)+"\n",encoding="utf-8")
    ledger=["# Append-only candidates for managing lead (R-2)","", "No root files were edited. All code remains unverified pending NEW independent review.","",
        "| File | SHA-256 | Evidence | Status |","|---|---|---|---|"]
    ledger += [f'| D_analysis/pipeline/{r["path"]} | {r["sha256"]} | {evidence.name}/suite | mock suite passed; review pending |' for r in source]
    (ROOT/"LEDGER_CANDIDATES.md").write_text("\n".join(ledger)+"\n",encoding="utf-8")
    (ROOT/"RUNS_CANDIDATES.md").write_text(
        "# Append-only run candidate for managing lead (R-2)\n\n"
        f"Local synthetic validation only; no fit, SSH or scheduler job.\n\nEvidence: {evidence}\n\n"
        f"Actual command: {json.dumps(launch['argv'])}\n\nPID {launch['child_pid']}; started {launch['started_utc']}; "
        f"finished {launch['finished_utc']}; exit 0. Checks passed: {len(checks)}. Rscript hash {launch['rscript_sha256']}. "
        f"Source inventory: SOURCE_SHA256.csv ({freeze['source_manifest_sha256']}). Deterministic fixture, no RNG seed.\n",encoding="utf-8")
    descriptions={
      "F1":"Reconstruct original-index primary PIPs through a strict kept/dropped partition; compare native HPM/MPM and retained/exported copies before truth access.",
      "F2":"Require fit$status = record native_status = CSV v3_status. Sole documented exception is before-core adapter_error with fit=NULL, nonempty error, unavailable estimates; retained-fit adapter errors fail closed.",
      "F3":"Require actual branch payload (SMC stages, log_Z/log_Z_r, four streams, PIPs, timings and bound annotation; exact payload without fabricated SMC data); compare all eight represented native JSON fields.",
      "F4":"Compare failed HPM and actually returned PIP-derived MPM audits to native sources; distinguish unavailable NA from returned empty support. Positive and negative partial-MPM controls pass."}
    lines=["# Review round 2 finding closure (R4 implementation)","", "All four findings addressed by code and passing regressions; NEW independent review of these hashes is pending. This is not approval from the prior REQUEST CHANGES report.","",
           f"Clean evidence: {evidence}","", "| Finding | Change | Saved rejecting adapter cases |","|---|---|---|"]
    lines += [f"| {f} | {descriptions[f]} | {', '.join(names)} |" for f,names in closure.items()]
    lines += ["",f"Additional native controls: {len(controls)}; see suite/native_controls/native_control_checks.csv.",
      "Each mutation refreshes CSV/RDS sidecars and fails with the specified native-integrity error. Invalid-native calls use a nonexistent truth directory, so reaching truth would fail the expected-error assertion.","",
      "Actual A dev p500/p1000: raw schema/native integrity PASS; legacy R-1 rejection EXPECTED; labelled D-owned adapted copies PASS with numeric-byte/attribute-identical native fit. Stage rows 587/769. No truth or production scoring. Eight original output files unchanged before/after and rechecked at freeze.",
      "Legacy native log_Z_lower95 has no explicit heuristic label; only the D reference copy carries a clearly labelled separate R-1 annotation. No native evidence value is changed.",
      "Actual updated A R-1 adapter integration and fresh independent review remain pending."]
    (ROOT/"FINDINGS_CLOSURE.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    handoff=(
        "# Final pipeline implementation handoff\n\n"
        f"Completed and locally executed: {utc()}. Full positive/adversarial mock suite exit 0; {len(checks)} saved passing check rows. "
        f"Inspected and SHA-256 verified {verified} saved output entries. This is implementer validation; a NEW independent final-source review is pending. "
        "No cancelled reviewer is counted.\n\n"
        "Scope: D-OWNED SCHEMA-LEVEL MOCK matching current A CSV/RDS fields plus binding R-1 semantics. "
        "This does NOT execute or certify A's updated adapter. The frozen A file is pre-R1; immutable old helpers supply native PIP extraction/layout only. "
        "D mock rows/record publisher supplies labelled R-1 fixture semantics and gzip RDS encoding. Earlier old-A compatibility/debug attempts remain separate. "
        "A's published HANDOFF_v1.md is snapshotted as vendor/HANDOFF_v1.preR1.md: v1 is still pre-R1 and is not R-1 compliant. "
        "Final-A adapter integration is an explicit pending gate: rerun an actual frozen-A mock after an R-1-compliant handoff arrives.\n\n"
        f"Review F1-F4 are addressed with saved mutation regressions and {len(controls)} branch/audit controls; see FINDINGS_CLOSURE.md and FREEZE.json. "
        "Actual A dev p500/p1000 are included in the same command: native/schema integrity passes, legacy R-1 output is explicitly rejected, "
        "and D-owned R-1-adapted copies pass without changing any native value or attribute (numeric-byte equality). "
        "The copied fit retains 587/769 stage rows; all eight original files are hash-unchanged. No truth or production scoring occurs in smoke validation. "
        "The absent native heuristic-bound label is disclosed; a separate D annotation labels the reference copy only.\n\n"
        f"Evidence: [{evidence.name}]({evidence.as_posix()}); launch.json, launcher.log, suite/verification_manifest.json and "
        "suite/verification_checks.csv hold actual commands/PIDs/timestamps/exit statuses/logs. Failed earlier attempts remain in validation/. "
        "FREEZE.json and SOURCE_SHA256.csv freeze checked code, copied A adapter, binding ruling and saved results.\n\n"
        "Re-run every mock artifact from the workspace with:\n\n"
        "    python 02_Experiments/H_2026-10-22_smcbvs_v3_deploy/D_analysis/pipeline/run_local.py\n\n"
        "R defaults to C:/Program Files/R/R-4.4.1/bin/Rscript.exe. No SSH/NOTS/Slurm or child agents were used. All writes stayed in pipeline/. "
        "R-2 ledger/run candidates are staged here for lead integration; no root file was edited. R-3 Owls shares remain D4 build/D2 during C batch; "
        "current local numerical libraries are capped to one thread.\n\n"
        "Binding R-1 is applied: hpm primary, pip05 S0, converged/fold_seed/fold_sha256 NA; exact/completed are ok or warning only for captured R warning/message; "
        "all other native statuses failed with returned supports audited. Diagnostic flags do not change status or selection, apply identically to both rules, "
        "and use only final checks E1-E3/low ESS/grid/local limit. Informational flags stay informational. Native v3_status/v3_flags_json and full RDS fit records survive. "
        "Obsolete or inconsistent A output fails closed. No production mapping was invented.\n\n"
        f"Assessment fixture: 120 datasets, 240 fits, 480 expected SMC rows, 474 observed deliberate gaps. Metrics rows: {len(metrics)}; "
        "denominators 10/cell and 60 pooled; 28 figures. All registered/derived benchmark rules remain visible. Pre/post-filter hashes and duplicate/adversarial cases pass. "
        "The separate reproduction task owns full historical reproduction; prepared config consumes all18 runs via combined_v3_v7/runs and combined_c050_v7/runs.\n\n"
        "Pooled FP/FN and complete-success-pair MCSEs condition on observed successful stratum counts. They exclude randomness of failure-driven mixture weights. "
        "Paired and within-case grouped uncertainty is preserved. Parent's 15-case mathematical check in ../review_metrics/20261022T194630Z/report.json is hash-specific "
        "and is not full final-source verification.\n\n"
        "Remaining production gates: formal R-1 A handoff and actual frozen-A integration rerun, inspected C outputs, lead destination/G1 decision, NEW independent review, independent >=30-cell raw-support/truth recount "
        "after assessment, and lead final review. No production RESULTS claim.\n")
    (ROOT/"HANDOFF.md").write_text(handoff,encoding="utf-8")
    (ROOT/"STATUS.md").write_text("# Pipeline status\n\nPhase: implementation completed; full local mock suite PASSED, exit0. "
        f"{len(checks)} saved passing check rows; {verified} output hash entries independently read back by freeze tool. "
        f"Evidence: {evidence}.\n\nSee HANDOFF.md, FREEZE.json and SOURCE_SHA256.csv. New final-source independent review remains pending. "
        "No production results claimed; no cancelled reviewer counted. R-1 adopted and snapshotted; R-2 candidates staged locally; R-3 D4/D2 acknowledged. "
        "No SSH/NOTS/Slurm or child agents; all writes pipeline only. Earlier failed attempts preserved.\n",encoding="utf-8")
    print(json.dumps(freeze,indent=2))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--evidence",type=Path,required=True)
    freeze(p.parse_args().evidence)
