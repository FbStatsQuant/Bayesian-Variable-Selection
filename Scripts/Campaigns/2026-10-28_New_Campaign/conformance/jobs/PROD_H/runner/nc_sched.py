"""Scheduler access for reconcile.py and poll.py (Python 3.9 standard library only).

Every squeue/sacct/scontrol call goes through run(), so the local dry-run tests can substitute the scheduler:
tests monkeypatch nc_sched.run, or set NC_STUB_BIN to a folder of stub scripts (run through bash). The shell
entry scripts (submit.sh, rerun.sh, p5_submit.sh, ...) refuse NC_STUB_BIN unless NC_LOCAL_TEST=1.
"""
import os
import subprocess


def run(args, env=None):
    stub = os.environ.get("NC_STUB_BIN")
    if stub:
        args = ["bash", os.path.join(stub, args[0])] + list(args[1:])
    return subprocess.run(args, capture_output=True, text=True, env=env)
