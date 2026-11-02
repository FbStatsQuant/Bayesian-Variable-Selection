"""Fabricate a result/attempt tree for the PROD-H dry-run tests (Python 3.9 standard library only).

Usage: python fabricate.py RUN_DIR SPEC.json
RUN_DIR holds config.env (OUTROOT, LOGROOT, RUN_ID) and units.tsv (the real 2,400-unit table). SPEC.json:
  {"default": "ok" | "none", "modes": {"<case_id>": "<mode>", ...}, "t0": "2026-10-29T12:00:00", "step": 2, "limit": N}
Modes (what the tree looks like after the unit's task has run):
  ok            attempt 1 ends, valid .done, v3_status completed
  escalated     as ok, diag_codes "escalated"
  resource_limit  valid .done, native v3_status resource_limit (rules failed)
  method_failed valid .done, native numerical_failure
  none          no attempt, no output (never started)
  infra         attempt 1 ended exit 1, no .done                 (-> class infra)
  infra_repeat  attempts 1 and 2 ended exit 1, no .done          (-> infra_repeat)
  orphan_then_ok first attempt ran in the rerun job (spec rerun_job), done
  infra_then_ok attempt 1 failed (exit 1), attempt 2 (rerun job) done  (-> done, ever_infra)
  hardtimeout   attempt 1 ended exit 124, timed_out true         (-> timeout)
  running       attempt 1 started, no end record                 (-> running when its task is in the queue)
  stalelock     as infra plus a SMCBVS.lock directory
Jobs: units with p = 1000 belong to array job 7002, p = 500 to 7003 (rerun attempts use job 7010).
Event times: t0 + step * (index of the unit in units.tsv) seconds, so the C3 window order is controlled by the table order.
"""
import csv
import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

JOB = {"1000": "7002", "500": "7003"}
RERUN_JOB = "7010"      # spec["rerun_job"] overrides


def write_result(prefix: Path, native: str, status: str, codes: str = ""):
    prefix.parent.mkdir(parents=True, exist_ok=True)
    rds, csvf = prefix.with_suffix(".rds"), prefix.with_suffix(".csv")
    rds.write_bytes(b"fabricated-" + prefix.name.encode())
    csvf.write_text("rule_id,status,v3_status,runtime_s,diag_codes\nhpm,%s,%s,10,%s\npip05,%s,%s,10,%s\n"
                    % (status, native, codes, status, native, codes))
    prefix.with_suffix(".sha256").write_text("".join(
        "%s  %s\n" % (hashlib.sha256(p.read_bytes()).hexdigest(), p.name) for p in (rds, csvf)))
    prefix.with_suffix(".done").write_text("done\n")


def attempt(logroot: Path, case, k, job, task, scale, t_start, t_end, exit_code, done, timed_out, with_end=True):
    d = logroot / "attempts" / case
    d.mkdir(parents=True, exist_ok=True)
    fmt = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
    (d / ("attempt_%d.start.json" % k)).write_text(json.dumps(dict(
        case_id=case, attempt=k, job=job, array_job=job, task=str(task), scale=scale, host="fab", started_utc=fmt(t_start))) + "\n")
    if with_end:
        (d / ("attempt_%d.end.json" % k)).write_text(
            '{"case_id":"%s","attempt":%d,"finished_utc":"%s","exit":%d,"wall_s":%d,"timed_out":%s,"done":%s,"lock_preexisted":false,"stale_lock_removed":false}\n'
            % (case, k, fmt(t_end), exit_code, int((t_end - t_start).total_seconds()), str(timed_out).lower(), str(done).lower()))
        (d / ("attempt_%d.log" % k)).write_text("fabricated\n")


def main(run_dir, spec):
    run_dir = Path(run_dir)
    cfg = dict(l.split("=", 1) for l in (run_dir / "config.env").read_text().split())
    out, logroot = Path(cfg["OUTROOT"]), Path(cfg["LOGROOT"])
    t0 = datetime.fromisoformat(spec.get("t0", "2026-10-29T12:00:00"))
    step = spec.get("step", 2)
    default = spec.get("default", "ok")
    modes = spec.get("modes", {})
    limit = spec.get("limit")
    rj = spec.get("rerun_job", RERUN_JOB)
    n = 0
    for i, u in enumerate(csv.DictReader(open(run_dir / "units.tsv", newline=""), delimiter="\t")):
        if limit is not None and i >= limit:
            break
        case, p, task, scale = u["case_id"], u["p"], u["task"], u["scale"]
        mode = modes.get(case, default)
        if mode == "none":
            continue
        ts = t0 + timedelta(seconds=step * i)
        te = ts + timedelta(seconds=1)
        job = JOB[p]
        prefix = out / "results" / cfg["RUN_ID"] / ("p%04d" % int(p)) / case / "SMCBVS"
        if mode in ("ok", "escalated"):
            write_result(prefix, "completed", "ok", "escalated" if mode == "escalated" else "")
            attempt(logroot, case, 1, job, task, scale, ts, te, 0, True, False)
        elif mode == "resource_limit":
            write_result(prefix, "resource_limit", "failed")
            attempt(logroot, case, 1, job, task, scale, ts, te, 2, True, False)
        elif mode == "method_failed":
            write_result(prefix, "numerical_failure", "failed")
            attempt(logroot, case, 1, job, task, scale, ts, te, 2, True, False)
        elif mode in ("infra", "stalelock"):
            attempt(logroot, case, 1, job, task, scale, ts, te, 1, False, False)
            if mode == "stalelock":
                lock = prefix.with_suffix(".lock")
                lock.mkdir(parents=True)
                (lock / "owner.txt").write_text("pid 1\nhost fab\nutc x\n")
        elif mode == "infra_repeat":
            attempt(logroot, case, 1, job, task, scale, ts, te, 1, False, False)
            attempt(logroot, case, 2, rj, task, scale, ts + timedelta(hours=1), te + timedelta(hours=1), 1, False, False)
        elif mode == "infra_then_ok":
            attempt(logroot, case, 1, job, task, scale, ts, te, 1, False, False)
            write_result(prefix, "completed", "ok")
            attempt(logroot, case, 2, rj, task, scale, ts + timedelta(hours=1), te + timedelta(hours=1), 0, True, False)
        elif mode == "orphan_then_ok":     # never attempted by its own task; first attempt ran in the rerun job
            write_result(prefix, "completed", "ok")
            attempt(logroot, case, 1, rj, task, scale, ts + timedelta(hours=1), te + timedelta(hours=1), 0, True, False)
        elif mode == "hardtimeout":
            attempt(logroot, case, 1, job, task, scale, ts, te, 124, False, True)
        elif mode == "running":
            attempt(logroot, case, 1, job, task, scale, ts, te, 0, False, False, with_end=False)
        else:
            raise SystemExit("unknown mode " + mode)
        n += 1
    return n


if __name__ == "__main__":
    print(main(sys.argv[1], json.loads(Path(sys.argv[2]).read_text())), "units fabricated")
