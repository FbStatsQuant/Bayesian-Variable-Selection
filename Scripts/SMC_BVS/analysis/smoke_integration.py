"""Actual development artifacts only: read/hash originals, validate legacy and labelled D copies. No scoring."""
import json
from pathlib import Path
import shutil
from run_pipeline import sha, write

DEFAULT_SMOKE_ROOT=Path("C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/A_build/smoke_records")


def check_actual_smoke(work,snapshot,rscript,execute,check,records,smoke_root=DEFAULT_SMOKE_ROOT):
    out=work/"actual_smoke";out.mkdir();inventory=[];summary=[]
    for p in (500,1000):
        cid=f"dev_p{p:04d}_S1_r001_c100"
        source=smoke_root/f"dev{p}"/"output"/"results"/f"dev_smoke_p{p:04d}_c100"/f"p{p:04d}"/cid
        original={ext:source/("SMCBVS."+ext) for ext in ("csv","rds","sha256","done")}
        before={str(path):sha(path) for path in original.values()}
        legacy=out/f"p{p}"/"legacy";legacy.mkdir(parents=True)
        for path in original.values():
            shutil.copy2(path,legacy/path.name)
            check(f"actual p{p} copied hash {path.suffix}",sha(legacy/path.name)==before[str(path)])
            inventory.append(dict(path=str(path),sha256_before=before[str(path)],copy=str(legacy/path.name)))
        code=snapshot/"benchmark"/"code";adapter=snapshot/"benchmark_adapter.R"
        def validate(bundle,profile,name,error=None):
            dest=out/f"p{p}"/name;log=out/f"p{p}"/(name+".log")
            cmd=[rscript,"--vanilla",adapter,"validate_native",code,dest,bundle/"SMCBVS.rds",bundle/"SMCBVS.csv",profile]
            rc=execute(cmd,log)
            ok=rc==0 if error is None else rc!=0 and error in log.read_text()
            records.append(dict(check=f"actual p{p} {name}",argv=json.dumps(list(map(str,cmd))),exit_status=rc,expected_error=error or "none",passed=ok))
            check(f"actual p{p} {name} outcome",ok)
            check(f"actual p{p} {name} no scoring",not (dest/"scored_rows.csv").exists())
            return dest
        legacy_out=validate(legacy,"legacy","legacy_native_schema")
        legacy_report=json.loads((legacy_out/"native_validation.json").read_text())
        check(f"actual p{p} known legacy mapping mismatch","unresolved or unadopted" in legacy_report["legacy_r1_rejection"])
        validate(legacy,"r1","legacy_R1_expected_rejection","unresolved or unadopted adapter policy")
        adapted=out/f"p{p}"/"D_R1_adapted_copy";shutil.copytree(legacy,adapted)
        cmd=[rscript,"--vanilla",snapshot/"adapt_smoke.R",snapshot/"vendor"/"A_adapter.R",snapshot/"mock_r1_rows.R",
             snapshot/"r1_contract.R",adapted/"SMCBVS"]
        rc=execute(cmd,out/f"p{p}"/"D_adaptation.log")
        records.append(dict(check=f"actual p{p} D reference adaptation",argv=json.dumps(list(map(str,cmd))),exit_status=rc,passed=rc==0))
        check(f"actual p{p} D reference adaptation exit",rc==0)
        validate(adapted,"r1","D_reference_R1_positive")
        adapted_report=json.loads((adapted/"SMCBVS.D_reference.json").read_text())
        check(f"actual p{p} native fit unchanged",adapted_report["native_fit_unchanged"] is True)
        for path,expected in before.items(): check(f"actual original unchanged {path}",sha(path)==expected)
        summary.append(dict(p=p,case_id=cid,legacy_schema="passed",legacy_R1="expected rejection: unresolved policy/NA roles+diagnostics; non-NA folds",
            D_adapted_reference="passed; native fit unchanged; no truth/scoring",stage_rows=legacy_report["stage_rows"],
            original_bound_label=legacy_report["original_bound_label"],D_bound_annotation=adapted_report["bound_annotation"],
            native_fit_sha256=adapted_report["native_fit_sha256"]))
    write(out/"originals_sha256.csv",[dict(r,sha256_after=sha(r["path"])) for r in inventory])
    (out/"smoke_integration.json").write_text(json.dumps(dict(scope="ACTUAL A DEV SMOKE; no production or truth scoring",summary=summary,
        final_A_R1_integration="pending actual updated A adapter; D copy is a reference transformation only"),indent=2),encoding="utf-8")
