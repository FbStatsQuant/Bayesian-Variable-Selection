"""Independent closed-form checks of supplementary uncertainty arithmetic.

Read a frozen copy of the implementation. These checks do not validate scoring,
the input join, or the scientific conclusions of an assessment.
"""
import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = ROOT / "pipeline/run_pipeline.py"
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    work = ROOT / "review_metrics" / stamp
    work.mkdir(parents=True, exist_ok=False)
    snapshot = work / "run_pipeline.py"
    snapshot.write_bytes(source.read_bytes())
    source_hash = sha(snapshot)
    spec = importlib.util.spec_from_file_location("independent_mcse_candidate", snapshot)
    candidate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    checks = []

    def check(label, actual, expected):
        passed = actual is None if expected is None else math.isclose(actual, expected, rel_tol=1e-13, abs_tol=1e-15)
        checks.append({"check": label, "actual": actual, "expected": expected, "passed": passed})

    # Five recoveries among ten: unbiased sample variance = (10*.25)/9.
    result = candidate.metric("rate", [(1, v) for v in [0, 1] * 5])
    check("binary rate mean", result["rate_mean"], 0.5)
    check("binary rate unbiased sample variance", result["rate_sample_variance"], 5 / 18)
    check("binary rate MCSE", result["rate_mcse"], 1 / 6)
    # One discordance in each direction and eight ties: mean zero, sum squares=2.
    paired = candidate.metric("difference", [(1, v) for v in [-1, 1] + [0] * 8])
    check("paired difference mean", paired["difference_mean"], 0)
    check("paired difference MCSE", paired["difference_mcse"], math.sqrt(1 / 45))
    # Scenario labels describe fixed strata, not extra sampling observations.
    check("fixed-stratum constant strata", candidate.stratified([(1, 0)] * 10 + [(2, 1)] * 10), 0)
    check("unequal successful denominators", candidate.stratified([(1, 0), (1, 1)] + [(2, 2)] * 4), 1 / 6)
    check("singleton stratum MCSE unavailable", candidate.stratified([(1, 0), (2, 0), (2, 1)]), None)
    check("empty MCSE unavailable", candidate.stratified([]), None)
    check("single observation MCSE unavailable", candidate.stats([1])["mcse"], None)
    # Two perfectly dependent signals in each case yield the same proportions
    # as one signal, not twice as many independent Bernoulli observations.
    grouped = candidate.metric("group", [(1, v) for v in [1, 1, 0, 0]])
    check("case-level grouped MCSE", grouped["group_mcse"], math.sqrt(1 / 12))
    check("type7 p95", candidate.quantile7([1, 2, 7, 11], 0.95), 10.4)
    check("missing fit is nonrecovery", candidate.exact(None), 0)
    check("failed fit is nonrecovery even with stale exact", candidate.exact({"status": "failed", "exact": "TRUE"}), 0)
    check("unknown diagnostics do not pass", int(candidate.passing({"diag_flag": "NA"})), 0)
    report = {"scope": "closed-form MCSE/order-statistic/eligibility checks only",
              "candidate_sha256": source_hash, "candidate_current_sha256": sha(source),
              "test_source_sha256": sha(Path(__file__)), "checks": checks,
              "passed": all(x["passed"] for x in checks)}
    (work / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(work / "report.json"), "checks": len(checks), "passed": report["passed"]}))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
