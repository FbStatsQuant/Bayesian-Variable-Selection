#!/usr/bin/env python3
"""Generate and execute the full deterministic mock suite locally (Amendment 2)."""
import argparse
import csv
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import traceback

from run_pipeline import ROOT, OWNER, PINNED, TABLES, sha, read, write, utc, stats, stratified, build_tables
from smoke_integration import check_actual_smoke

KEYS = {
    "rules_long": ["method_id", "rule_id", "p", "scenario"],
    "T1": ["method_id", "rule_id", "p", "scenario"],
    "T2": ["method_id", "rule_id", "p", "scenario"],
    "T3": ["method_id", "rule_id", "p", "scenario"],
    "T4_by_variable": ["method_id", "rule_id", "p", "scenario", "signal"],
    "T4_by_group": ["method_id", "rule_id", "p", "scenario", "abs_beta", "rho_S6"],
    "T5": ["method_id", "p"],
    "T6": ["method_id", "rule_id", "p", "scenario"],
    "S_tables": ["method_id", "rule_id", "p", "scenario"],
    "caps": ["method_id", "rule_id", "p", "scenario"],
    "codes_by_rule": ["method_id", "rule_id", "p", "scenario", "code"],
}


def execute(argv, log):
    record=dict(argv=list(map(str,argv)),started_utc=utc(),log=str(log))
    with log.open("w", encoding="utf-8") as f:
        p = subprocess.Popen(record["argv"], stdout=f, stderr=subprocess.STDOUT)
        record["pid"]=p.pid
        log.with_suffix(".command.json").write_text(json.dumps(record,indent=2),encoding="utf-8")
        rc=p.wait()
    record.update(exit_status=rc,finished_utc=utc(),log_sha256=sha(log))
    log.with_suffix(".command.json").write_text(json.dumps(record,indent=2),encoding="utf-8")
    return rc


def verify(work, scoring, rscript, local_mock=False, reuse_fixture=None, preflight_only=False, reproduction=None):
    if platform.system() == "Linux" and platform.node().lower().startswith("owls"):
        if os.getpriority(os.PRIO_PROCESS, 0) < 19:
            raise RuntimeError("nice19 required")
        available = next(int(x.split()[1]) for x in Path("/proc/meminfo").read_text().splitlines() if x.startswith("MemAvailable:"))
        if os.getloadavg()[0] > 40 or available < 30*1024*1024:
            raise RuntimeError("Owls batch gate failed; parent must wait 15min")
    work = work.resolve()
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[name]="1"
    work.mkdir(parents=True, exist_ok=False)
    records = []; status = {"started_utc": utc(), "pid": os.getpid(), "host": platform.node(),
        "argv": sys.argv, "status": "running", "seed": "none; deterministic synthetic fixture",
        "source_sha256": {str(p): sha(p) for p in ROOT.iterdir() if p.is_file()}}
    def check(name, condition):
        records.append({"check": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)
    try:
        for name, expected in PINNED.items():
            check("immutable source "+name, sha(scoring/"code"/name) == expected)
        snapshot = work/"source_snapshot"; snapshot.mkdir()
        for p in ROOT.iterdir():
            if p.is_file(): shutil.copy2(p, snapshot/p.name)
        shutil.copytree(ROOT/"vendor", snapshot/"vendor")
        check("frozen pre-R1 A layout helper", sha(snapshot/"vendor"/"A_adapter.R") == "e543af87a1b0bdc92fd32f01858c5d8bbb7d2d273ef1c265edcd91a26b07b3b4")
        shutil.copytree(scoring/"code", snapshot/"benchmark"/"code")
        shutil.copytree(scoring/"derived_rules", snapshot/"benchmark"/"derived_rules")
        cmd=[rscript,"--vanilla",snapshot/"test_r1_adapter.R",snapshot/"vendor"/"A_adapter.R",
             snapshot/"mock_r1_rows.R",snapshot/"r1_contract.R",work/"r1_branches"]
        rc=execute(cmd,work/"r1_branches.log")
        records.append(dict(check="D R-1 schema branches",argv=json.dumps(list(map(str,cmd))),exit_status=rc,passed=rc==0))
        check("all D R-1 schema branches exit",rc==0)
        check("all R-1 branch checks",all(r["passed"]=="TRUE" for r in read(work/"r1_branches"/"r1_checks.csv")))
        cmd=[rscript,"--vanilla",snapshot/"test_native_controls.R",snapshot/"vendor"/"A_adapter.R",
             snapshot/"mock_r1_rows.R",snapshot/"r1_contract.R",work/"native_controls"]
        rc=execute(cmd,work/"native_controls.log")
        records.append(dict(check="F1-F4 branch controls",argv=json.dumps(list(map(str,cmd))),exit_status=rc,passed=rc==0))
        check("native controls exit",rc==0)
        check("all native controls",all(r["passed"]=="TRUE" for r in read(work/"native_controls"/"native_control_checks.csv")))
        check_actual_smoke(work,snapshot,rscript,execute,check,records)
        if preflight_only:
            status.update(status="passed_preflight_only",exit_status=0)
            return
        # All subprocesses inherit nice19 and single-core numerical-library limits.
        fixture = work/"fixture"
        if reuse_fixture is None:
            command = [rscript, "--vanilla", snapshot/"make_fixture.R", snapshot/"benchmark"/"code", fixture, snapshot/"vendor"/"A_adapter.R",snapshot/"mock_r1_rows.R"]
            rc = execute(command, work/"fixture_generation.log")
            records.append({"check": "fixture generation", "argv": json.dumps(list(map(str, command))), "exit_status": rc, "passed": rc==0})
            check("fixture generator exit", rc == 0)
        else:
            reuse_fixture=reuse_fixture.resolve()
            prior=json.loads((reuse_fixture.parent/"baseline"/"manifest.json").read_text())
            check("recovery prior baseline completed",prior["status"]=="completed_provisional" and prior["exit_status"]==0)
            covered=[]
            for path,meta in prior["files"].items():
                p=Path(path)
                if p.is_relative_to(reuse_fixture):
                    check("recovery input "+str(p.relative_to(reuse_fixture)),sha(p)==meta["sha256"])
                    covered.append(dict(path=str(p),sha256=meta["sha256"]))
            check("recovery generator unchanged",sha(ROOT/"make_fixture.R")==sha(reuse_fixture.parent/"source_snapshot"/"make_fixture.R") and
                  sha(ROOT/"mock_r1_rows.R")==sha(reuse_fixture.parent/"source_snapshot"/"mock_r1_rows.R"))
            check("recovery has input hashes",len(covered)>1000)
            shutil.copytree(reuse_fixture,fixture)
            write(work/"recovered_inputs.csv",covered)
            status["fixture_reused"]=str(reuse_fixture)
        config = {"mode": "synthetic", "out": str(work/"baseline"), "output_root": str(work), "rscript": str(rscript),
            "benchmark_scoring": str(snapshot/"benchmark"), "inputs_manifest": str(fixture/"inputs_manifest.csv"),
            "truth_manifest": str(fixture/"truth_manifest.csv"), "truth_dir": str(fixture/"truth"),
            "mapping_csv": str(fixture/"mock_mapping.csv"),
            "mapping_ruling": str(snapshot/"vendor"/"RULINGS_LEAD.md"),
            "assessment_selector": {"p": [500,1000], "scenario": list(range(1,7)), "replicate": list(range(1,11)), "scale_key": ["c100","c050"]},
            "benchmark_sources": [], "smc_sources": []}
        for sk in ("c100", "c050"):
            source = fixture/("benchmark_"+sk)
            config["benchmark_sources"].append({"scored_dir": str(source), "version": "SYNTHETIC full 11-replicate source",
                "tables": {tb: {"path": str(source/(tb+".csv")), "keys": KEYS[tb]} for tb in TABLES}})
            config["smc_sources"].append({"scale_key": sk, "results_dir": str(fixture/("SYNTHETIC_SMC_"+sk))})
        def pipeline(cfg, name, expected_error=None):
            cfg = json.loads(json.dumps(cfg)); cfg["out"] = str(work/name)
            path = work/(name+".json"); path.write_text(json.dumps(cfg,indent=2), encoding="utf-8")
            cmd = [sys.executable, snapshot/"run_pipeline.py", "--config", path]
            rc = execute(cmd, work/(name+".log"))
            log = (work/(name+".log")).read_text()
            expected = rc == 0 if expected_error is None else rc != 0 and expected_error in log
            records.append({"check": name, "argv": json.dumps(list(map(str,cmd))), "exit_status": rc,
                            "expected_error": expected_error or "none", "passed": expected})
            check(name+" expected outcome", expected)
            return work/name
        baseline = pipeline(config, "baseline")
        metrics = read(baseline/"study_metrics_mcse.csv")
        hpm = next(r for r in metrics if r["method_id"]=="SMCBVS" and r["rule_id"]=="hpm" and
                   r["scale_key"]=="c100" and r["p"]=="500" and r["scenario"]=="1")
        check("assessment n10", all(r["n_expected"] == ("60" if r["scenario"]=="pooled" else "10") for r in metrics))
        check("hand exact count", float(hpm["exact_all_sum"]) == 3)
        check("hand passing count", float(hpm["exact_passing_sum"]) == 2)
        check("hand failure count", float(hpm["n_fail_total"]) == 3)
        check("hand FP mean", math.isclose(float(hpm["fp_mean"]), 2/7, rel_tol=1e-14))
        check("hand FN mean", math.isclose(float(hpm["fn_mean"]), 16/7, rel_tol=1e-14))
        check("hand binary sample MCSE", math.isclose(float(hpm["exact_all_mcse"]), math.sqrt(.3*.7/9), rel_tol=1e-14))
        joined = read(baseline/"joined_scored_rows.csv")
        smc = [r for r in joined if r["method_id"]=="SMCBVS"]
        check("actual A native fields preserved", all(r.get("v3_status") and r.get("v3_flags_json") for r in smc))
        check("no invented native CSV fields", all("native_status" not in r and "native_flags" not in r for r in smc))
        check("R-1 failed diagnostics and audit retained", all(r["diag_flag"] in {"TRUE","FALSE"} and r["support"]=="NA" and r["fp"]=="NA"
             for r in smc if r["status"] in {"failed","timeout","not_run"}) and any(r["support_audit"]=="1;2" for r in smc))
        check("successful null model distinct", any(r["status"]=="ok" and r["support"]=="" and r["k"]=="0" and r["fn"]=="14" for r in smc))
        check("degenerate unavailable PIPs preserved", any(r["v3_status"]=="y_constant" and r["rule_id"]=="hpm" and
              r["status"]=="failed" and r["support_audit"]=="" and r["pip_a01"]=="NA" for r in smc))
        check("R-1 fold fields unavailable", all(r["fold_seed"]=="NA" and r["fold_sha256"]=="NA" for r in smc))
        check("R-1 converged unavailable", all(r["converged"]=="NA" for r in smc))
        check("selected rows only", all(int(r["replicate"])<=10 for r in joined))
        check("SMC rows expected gaps", sum(r["method_id"]=="SMCBVS" for r in joined)==474)
        check("complete selector", len(read(baseline/"selected_cases.csv")) == 240)
        check("all scenario figures", len(list(baseline.glob("exact_*.svg"))) == 28)
        check("immutable benchmark reproduction", all(r["cell_and_type_equal"]=="TRUE" for r in read(baseline/"published_reproduction.csv")))
        paired = read(baseline/"paired_comparisons.csv")
        pr = next(r for r in paired if r["method_id"]=="F1" and r["rule_id"]=="cv_min" and r["smc_rule"]=="hpm"
                  and r["scale_key"]=="c100" and r["p"]=="500" and r["scenario"]=="1")
        check("paired common-case mean", math.isclose(float(pr["exact_difference_mean"]),.1))
        check("paired common-case MCSE", math.isclose(float(pr["exact_difference_mcse"]),.1))
        check("paired conditional FP denominator", pr["fp_difference_n"]=="6" and float(pr["fp_difference_mcse"])==0)
        check("n1 and n0 MCSE unavailable", stats([1])["mcse"] is None and stats([])["mcse"] is None and stratified([(1,0)]) is None)
        check("all registered and derived rules", len(metrics)==(50+2)*28)
        filters=read(baseline/"assessment_filter_checks.csv")
        check("pre and post selection hashes", all(r["hash_assertions_before"]=="True" and r["hash_assertions_after"]=="True" and int(r["rows_excluded"])>0 for r in filters))
        # Independent arithmetic from saved rows for fixed-stratum and grouped T4 checks.
        groups = {}
        for sc in range(1,7):
            selected = [r for r in joined if r["method_id"]=="SMCBVS" and r["rule_id"]=="hpm"
                        and r["scale_key"]=="c100" and r["p"]=="500" and int(r["scenario"])==sc]
            vals = [int(r["exact"]=="TRUE") for r in selected]
            vals += [0]*(10-len(vals))
            mean = sum(vals)/10
            sample_var = sum((x-mean)**2 for x in vals)/9
            groups[sc] = sample_var
        expected_se = math.sqrt(sum((1/6)**2 * v/10 for v in groups.values()))
        pooled = next(r for r in metrics if r["method_id"]=="SMCBVS" and r["rule_id"]=="hpm" and
                      r["scale_key"]=="c100" and r["p"]=="500" and r["scenario"]=="pooled")
        check("independent fixed-stratum pooled MCSE", math.isclose(float(pooled["exact_all_mcse"]), expected_se, rel_tol=1e-14))
        group = next(r for r in read(baseline/"T4_mcse.csv") if r["method_id"]=="SMCBVS" and r["rule_id"]=="hpm"
                     and r["scale_key"]=="c100" and r["p"]=="500" and r["scenario"]=="1"
                     and r["group_type"]=="abs_beta" and r["group"]=="0.8")
        # abs_beta .8 at active positions 1,7,8,14; case proportions preserve their dependence.
        values = [1,1,.75,.75,0,1,0,0,0,1]
        mean = sum(values)/10; expected_var = sum((x-mean)**2 for x in values)/9
        check("within-case T4 group variance", math.isclose(float(group["selection_sample_variance"]), expected_var, rel_tol=1e-14))
        check("within-case T4 group MCSE", math.isclose(float(group["selection_mcse"]), math.sqrt(expected_var/10), rel_tol=1e-14))
        # Entirely absent rule group: the registered denominator survives without a single row.
        absent_dir=work/"absent_group"; absent_dir.mkdir()
        cases={r["case_id"]:dict(r,p="500",scenario="1") for r in read(baseline/"selected_cases.csv")
               if r["case_id"].startswith("p0500_S1_") and r["scale_key"]=="c100"}
        summary,_=build_tables([],cases,[dict(method_id="SMCBVS",rule_id="hpm",scale_key="c100",role="primary",label="mock absent")],absent_dir,{})
        check("entire missing rule group preserves n10 and n60 selection denominator", all(r["n_missing"]==10 and r["exact_all_sum"]==0 for r in summary))
        # Config preparation consumes the current all-18 reproduction interface, without scoring it.
        inventory=reproduction/"runs.tsv"
        cmd=[sys.executable,snapshot/"prepare_assessment_config.py","--out",work/"assessment_prepared.json",
             "--analysis-out",work/"future_assessment","--runs-tsv",inventory,"--scored-root",reproduction/"local_outputs",
             "--canonical-root",scoring/"out","--benchmark-scoring",scoring,"--inputs-manifest",fixture/"inputs_manifest.csv",
             "--truth-manifest",fixture/"truth_manifest.csv","--truth-dir",fixture/"truth","--mapping-csv",fixture/"mock_mapping.csv",
             "--mapping-ruling",snapshot/"vendor"/"RULINGS_LEAD.md","--ops-outputs",fixture/"FIXTURE.txt",
             "--smc-c100",fixture/"SYNTHETIC_SMC_c100","--smc-c050",fixture/"SYNTHETIC_SMC_c050","--rscript",rscript]
        rc=execute(cmd,work/"prepare_assessment.log")
        records.append(dict(check="prepare all18 config",argv=json.dumps(list(map(str,cmd))),exit_status=rc,passed=rc==0))
        check("prepare assessment config exit",rc==0)
        prepared=json.loads((work/"assessment_prepared.json").read_text())
        check("all18 current reproduction paths",len(prepared["benchmark_sources"])==18 and all(
            ("combined_v3_v7" if s["scale_key"]=="c100" else "combined_c050_v7")+"/runs/" in s["scored_dir"].replace("\\","/")
            for s in prepared["benchmark_sources"]))
        # Adversarial mutations affect fixture copies only. Originals and source code remain read-only.
        for name, error in [("duplicate", "duplicate row key"), ("bad_hash", "input hash mismatch"),
                            ("outside_bad_hash", "input hash mismatch"),
                            ("mixed_source", "within-fit source_sha256 differs"),
                            ("mixed_status", "inconsistent fit-wide scheduler status")]:
            changed = work/("fixture_"+name)
            shutil.copytree(fixture/"benchmark_c100",changed)
            data = read(changed/"scored_rows.csv")
            if name=="duplicate": data.append(dict(data[0]))
            elif name=="bad_hash": data[0]["x_sha256"]="0"*64
            elif name=="outside_bad_hash": next(r for r in data if r["replicate"]=="11")["y_sha256"]="0"*64
            elif name=="mixed_source": data[0]["source_sha256"]="0"*64
            else:
                data[0].update(status="timeout",exact="FALSE",error_type="failed",tp="NA",fp="NA",fn="NA")
            write(changed/"scored_rows.csv",data)
            cfg=json.loads(json.dumps(config)); cfg["benchmark_sources"][0]["scored_dir"]=str(changed)
            pipeline(cfg,name,error)
        # Explicit selector corruption must not silently fabricate 90 missing replicates.
        cfg=json.loads(json.dumps(config)); cfg["assessment_selector"]["replicate"]=[1,2]
        pipeline(cfg,"bad_selector","exact Amendment 1 assessment_selector")
        path=work/"bad_ruling.md"; path.write_text("unadopted placeholder")
        cfg=json.loads(json.dumps(config)); cfg["mapping_ruling"]=str(path)
        pipeline(cfg,"bad_ruling_hash","binding R-1 ruling hash mismatch")
        cfg=json.loads(json.dumps(config)); cfg["mode"]="assessment";cfg["ops_outputs"]=str(fixture/"FIXTURE.txt")
        pipeline(cfg,"mock_in_assessment","assessment refuses synthetic study rows")
        # Target the actual raw-bundle adapter directly: one bundle per test, same immutable scorer.
        for name,error in [("bad_pip","native primary PIP/export mismatch"),("unavailable_pip","native primary PIP/export mismatch"),
                           ("stale_truth","prefilled truth column"),("failed_as_null","failed row with support/k"),
                           ("successful_as_NA","invalid support/k"),("unresolved_policy","unresolved or unadopted"),
                           ("unmapped_native","native flags JSON differs"),("duplicate_smc","empty/duplicate/unregistered"),
                           ("csv_rds_disagree","RDS/CSV rows differ"),("corrupt_sidecar","hash mismatch"),
                           ("missing_bundle","incomplete SMC bundle"),
                           ("hpm_disagrees","native hpm/exported support mismatch"),
                           ("pip_disagrees","native primary PIP/export mismatch"),
                           ("native_status_disagrees","native fit/status/export mismatch"),
                           ("reverse_failure_status","native fit/status/export mismatch"),
                           ("degenerate_status_disagrees","native fit/status/export mismatch"),
                           ("missing_native_payload","native timings payload missing"),
                           ("missing_native_pip","native primary PIP missing/invalid"),
                           ("bad_preprocessing_map","native preprocessing map invalid"),
                           ("wrong_native_pip_names","native primary PIP missing/invalid"),
                           ("missing_native_stage","native SMC stage payload missing"),
                           ("missing_island_evidence","native island evidence/streams payload missing"),
                           ("missing_native_streams","native island evidence/streams payload missing"),
                           ("missing_bound_label_certified","native heuristic bound label missing"),
                           # D-F1: uncertified fits need no label; they pass every native/R-1 check and
                           # stop only at the deliberately unopenable truth path.
                           ("missing_bound_label_uncertified","MUST_NOT_OPEN_TRUTH_FOR_INVALID_NATIVE/p0500/p0500_S1_r001.rds"),
                           ("native_json_disagrees","native flags JSON differs"),
                           *[("json_"+nm,"native flags JSON differs") for nm in
                             ("cut_group_count","cut_group_components","local_limit","local_certified","global_certified","near_tie_truncated")],
                           ("missing_failure_audit","native failed support_audit mismatch"),
                           ("changed_failure_audit","native failed support_audit mismatch"),
                           ("null_failure_as_NA","native failed support_audit mismatch"),
                           ("unavailable_failure_as_empty","native failed support_audit mismatch")]:
            raw=work/("raw_"+name); dest=work/("adapter_"+name)
            failed=name in {"failed_as_null","reverse_failure_status","missing_failure_audit","changed_failure_audit","unavailable_failure_as_empty"}
            rep=7 if failed else 9 if name=="null_failure_as_NA" else 1
            scenario=2 if name=="null_failure_as_NA" else 1
            cid=f"p0500_S{scenario}_r{rep:03d}_c100"
            original=fixture/"SYNTHETIC_SMC_c100"/"p0500"/cid
            bundle=raw/"p0500"/cid
            shutil.copytree(original,bundle)
            # Preserve the original run identity in the explicit fixture copy.
            raw_final=raw/"SYNTHETIC_SMC_c100"
            raw_final.mkdir(); shutil.move(str(raw/"p0500"),str(raw_final/"p0500"))
            prefix=raw_final/"p0500"/cid/"SMCBVS"
            if name=="corrupt_sidecar":
                with prefix.with_suffix(".csv").open("a") as f: f.write("\n")
            elif name=="missing_bundle": prefix.with_suffix(".rds").unlink()
            else:
                cmd=[rscript,"--vanilla",snapshot/"mutate_fixture.R",prefix,name]
                rc=execute(cmd,work/(name+"_mutation.log"))
                records.append(dict(check=name+" mutation",argv=json.dumps(list(map(str,cmd))),exit_status=rc,passed=rc==0))
                check(name+" mutation exit",rc==0)
            cmd=[rscript,"--vanilla",snapshot/"benchmark_adapter.R","smc",snapshot/"benchmark"/"code",dest,
                 raw_final,baseline/"selected_inputs_manifest.csv",work/"MUST_NOT_OPEN_TRUTH_FOR_INVALID_NATIVE",fixture/"truth_manifest.csv","c100",
                 ]
            log=work/(name+"_adapter.log"); rc=execute(cmd,log)
            records.append(dict(check=name+" adapter",argv=json.dumps(list(map(str,cmd))),exit_status=rc,
                                expected_error=error,passed=rc!=0 and error in log.read_text()))
            check(name+" rejected correctly",rc!=0 and error in log.read_text())
        status.update(status="passed", exit_status=0)
    except BaseException:
        status.update(status="failed", exit_status=1, error=traceback.format_exc())
        raise
    finally:
        status["finished_utc"]=utc()
        (work/"verification_manifest.json").write_text(json.dumps(status,indent=2),encoding="utf-8")
        write(work/"verification_checks.csv",records)
        active_error=sys.exc_info()[0] is not None
        try:
            write(work/"verification_outputs_sha256.csv",[{"path":str(p.relative_to(work)),"sha256":sha(p)}
                  for p in sorted(work.rglob("*")) if p.is_file() and p.name!="verification_outputs_sha256.csv"])
        except Exception:
            status.update(status="failed_output_audit",exit_status=1,output_audit_error=traceback.format_exc())
            (work/"verification_manifest.json").write_text(json.dumps(status,indent=2),encoding="utf-8")
            if not active_error: raise


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work",type=Path,required=True)
    parser.add_argument("--benchmark-scoring",type=Path,required=True)
    parser.add_argument("--rscript",default="/usr/bin/Rscript")
    parser.add_argument("--local-mock",action="store_true",help="Amendment2 authorized local synthetic tests only")
    parser.add_argument("--reuse-fixture",type=Path,help="DEBUG ONLY: verify prior audited inputs and copy them; final freeze forbids reuse")
    parser.add_argument("--reproduction-root",type=Path,required=True,help="D_analysis/reproduction (runs.tsv and local_outputs)")
    parser.add_argument("--preflight-only",action="store_true",help="Bounded native controls and actual dev smoke; not a full-suite pass")
    args=parser.parse_args()
    verify(args.work,args.benchmark_scoring,args.rscript,args.local_mock,args.reuse_fixture,args.preflight_only,args.reproduction_root.resolve())
