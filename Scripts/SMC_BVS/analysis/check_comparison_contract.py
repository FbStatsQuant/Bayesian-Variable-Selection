"""Independent fixtures for the reproduction exact-comparison checker.

This tests comparison infrastructure, not benchmark scientific results.
No benchmark inputs or outputs are modified.
"""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
CHECKER = ROOT / "reproduction/code/compare_exact.R"
RSCRIPT = Path("C:/Program Files/R/R-4.4.1/bin/Rscript.exe")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    work = ROOT / "review_reproduction" / stamp
    work.mkdir(parents=True, exist_ok=False)
    source_hash = digest(CHECKER)
    frozen = work / "compare_exact.R"
    frozen.write_bytes(CHECKER.read_bytes())
    header = "method_id,rule_id,p,scenario,mean_fp\n"
    row1 = "F1,cv_min,500,1,0.1\n"
    row2 = "F1,cv_min,500,2,0.2\n"
    tests = [
        ("identical", header + row1 + row2, header + row1 + row2, True),
        ("key_reordering", header + row1 + row2, header + row2 + row1, True),
        ("tiny_numeric_change", header + row1, header + row1.replace("0.1", "0.10000000000000002"), False),
        ("lexical_change", header + row1, header + row1.replace("0.1", "0.10"), False),
        ("duplicate_key", header + row1 + row1, header + row1 + row1, False),
        ("missing_row", header + row1 + row2, header + row1, False),
        ("column_order", header + row1, "rule_id,method_id,p,scenario,mean_fp\ncv_min,F1,500,1,0.1\n", False),
        ("missing_file", header + row1, None, False),
    ]
    records = []
    for name, expected, actual, should_pass in tests:
        case = work / name
        ref, got = case / "reference", case / "actual"
        ref.mkdir(parents=True)
        got.mkdir()
        (ref / "T3.csv").write_text(expected, encoding="utf-8")
        if actual is not None:
            (got / "T3.csv").write_text(actual, encoding="utf-8")
        command = [str(RSCRIPT), "--vanilla", str(frozen), "--reference", str(ref),
                   "--actual", str(got), "--out", str(case / "comparison")]
        with (case / "command.log").open("w", encoding="utf-8") as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        record = {"case": name, "expected_equal": should_pass, "exit_status": result.returncode,
                  "pass": (result.returncode == 0) == should_pass, "command": command,
                  "log_sha256": digest(case / "command.log")}
        records.append(record)
    report = {"source": str(CHECKER), "source_sha256": source_hash,
              "source_unchanged": source_hash == digest(CHECKER),
              "rscript": str(RSCRIPT), "test_source_sha256": digest(Path(__file__)),
              "scope": "comparison infrastructure only; no scientific recomputation",
              "tests": records,
              "passed": all(r["pass"] for r in records) and source_hash == digest(CHECKER)}
    (work / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(work / "report.json"), "passed": report["passed"], "tests": len(records)}))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
