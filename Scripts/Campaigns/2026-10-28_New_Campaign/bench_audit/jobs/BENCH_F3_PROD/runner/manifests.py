#!/usr/bin/env python3
"""Create or revalidate manifests; never delete data."""
import hashlib
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import tempfile
import csv
import re
import shlex
import subprocess
from units import units
from retry import select
from terminal import assert_absent


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    args = sys.argv[1:]
    verify = "--verify" in args
    args = [x for x in args if x != "--verify"]
    run_log = None
    if "--run-log" in args:
        pos = args.index("--run-log")
        if pos + 1 >= len(args): raise ValueError("--run-log needs a path")
        run_log = Path(args[pos + 1])
        del args[pos:pos + 2]
    if not args:
        sys.exit("usage: manifests.py absolute_folder [absolute_folder ...] [--verify]")
    folders = [Path(x) for x in args]
    if not verify and any(str(x).startswith("/scratch/fb31/New_Campaign/") for x in folders):
        if run_log is None or not run_log.is_absolute():
            raise ValueError("production manifests require --run-log")
        run_id = run_log.name
        if not re.fullmatch(r"[0-9]{8}T[0-9]{4,6}Z_bench_f3v2_(dev|prod)", run_id):
            raise ValueError("invalid run id")
        root = Path("/scratch/fb31/New_Campaign")
        if run_log != root / "logs" / run_id or set(folders) != {root / "results" / run_id / "p0500", root / "results" / run_id / "p1000", run_log}:
            raise ValueError("must preflight exactly both result folders and this run's logs")
        kind = "dev" if run_id.endswith("_bench_f3v2_dev") else "prod"
        mapping = units(kind)
        with (run_log / "jobs.tsv").open(newline="") as f:
            jobs = list(csv.DictReader(f, delimiter="\t"))
        if len(jobs) != (1 if kind == "dev" else 4):
            raise ValueError("incomplete primary job journal")
        expected_jobs = [(j["job_id"], {r[0] for r in mapping if j["cell"] == "dev" or f"p{r[1]:04d}_{r[4]}" == j["cell"]}) for j in jobs]
        for marker in run_log.glob("retry_*.intent"):
            text = marker.read_text(encoding="utf-8")
            match = re.search(r"^job_id=(\d+)$", text, re.MULTILINE)
            if not match: raise ValueError("retry acceptance unresolved")
            command = shlex.split(text.splitlines()[0])
            arg = next(x for x in command if x.startswith("--array="))
            expected_jobs.append((match[1], {int(x) for x in arg.split("=", 1)[1].split("%", 1)[0].split(",")}))
        for job, expected in expected_jobs:
            assert_absent(job)
            data = subprocess.run(["sacct", "-n", "-P", "-j", job, "--format=JobID%40,State%30"], capture_output=True, text=True, check=True).stdout
            select("JobID|State\n" + data, job, expected)
        if not (run_log / "accounting.tsv").is_file() or "TOTAL" not in (run_log / "accounting.tsv").read_text():
            raise ValueError("final accounting report required")
    if len(set(folders)) != len(folders):
        raise ValueError("duplicate folder")
    plans = []
    for folder in folders:
        if not folder.is_absolute() or not folder.is_dir():
            raise ValueError("absolute existing folder required")
        if any(x.is_symlink() for x in folder.rglob("*")):
            raise ValueError("symlinks refused")
        if any(x.name.endswith(".lock") or x.name.endswith(".tmp") or ".tmp." in x.name for x in folder.rglob("*")):
            raise ValueError("unfinished lock or temporary artifact; inspect and archive after terminal-state proof")
        files = sorted(x for x in folder.rglob("*") if x.is_file() and x != folder / "MANIFEST.sha256")
        if any("\n" in x.relative_to(folder).as_posix() or "\\" in x.name for x in files):
            raise ValueError("unsafe filename")
        text = "".join(f"{sha(x)}  {x.relative_to(folder).as_posix()}\n" for x in files)
        man = folder / "MANIFEST.sha256"
        if man.exists() and man.read_text(encoding="utf-8") != text:
            raise ValueError("existing manifest differs")
        if verify and not man.exists():
            raise ValueError("manifest missing")
        plans.append((folder, files, text, man))
    for folder, files, text, man in plans:
        if not man.exists():
            fd, name = tempfile.mkstemp(prefix=".manifest.", dir=folder)
            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text); f.flush(); os.fsync(f.fileno())
                os.replace(name, man)
            finally:
                if os.path.exists(name):
                    os.unlink(name)
        if man.read_text(encoding="utf-8") != text:
            raise ValueError("manifest changed during commit")
        print(f"{folder} files={len(files)} manifest_sha256={sha(man)}" + (" EMPTY" if not files else ""))


if __name__ == "__main__":
    main()
