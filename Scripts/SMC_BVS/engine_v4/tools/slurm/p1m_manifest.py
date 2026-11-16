#!/usr/bin/env python3
"""p1m_manifest.py -- fill a job-manifest template at run time (INTERFACES §5.3). Stdlib only; Python >= 3.6.

  p1m_manifest.py fill --template T.json --run-dir RUN --out M.json [--bin PATH] [--set a.b=v ...]

Placeholders in the template:
  "@from:<record>.json"  -> the content hash of the input, read from RUN/<record>.json "outputs" (written by the stage
                            that produced it); the record must have "status": "completed", else exit 66 (refuse to start)
  "@binary"              -> binary.sha256 = SHA-256 of --bin (default $BIN); compiler/flags/libm = "see <bin> info"
  "@slurm"               -> machine.host / slurm_job_id / params.threads from the Slurm environment
"""
import argparse
import hashlib
import json
import os
import socket
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_from(run_dir, rec_name, input_name):
    path = os.path.join(run_dir, rec_name)
    try:
        with open(path) as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as e:
        raise SystemExit("p1m_manifest: cannot read %s (%s): refusing to start" % (path, e))
    if rec.get("status") != "completed":
        raise SystemExit("p1m_manifest: %s has status %r: refusing to start" % (path, rec.get("status")))
    outs = rec.get("outputs") or {}
    h = outs.get(input_name)
    if h is None:   # records may key outputs by path; match the basename
        for k, v in outs.items():
            if os.path.basename(k) == input_name:
                h = v
    if not h:
        raise SystemExit("p1m_manifest: %s lists no output %s: refusing to start" % (path, input_name))
    return h


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fill"])
    ap.add_argument("--template", required=True)
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bin", default=os.environ.get("BIN", ""))
    ap.add_argument("--set", action="append", default=[])
    a = ap.parse_args(argv)
    with open(a.template) as fh:
        m = json.load(fh)
    for k, v in list(m.get("inputs", {}).items()):
        if isinstance(v, str) and v.startswith("@from:"):
            m["inputs"][k] = resolve_from(a.run_dir, v[len("@from:"):], k)
    b = m.get("binary", {})
    for k, v in list(b.items()):
        if v == "@binary":
            if k == "sha256":
                b[k] = sha256_file(a.bin) if a.bin and os.path.exists(a.bin) else "UNKNOWN"
            else:
                b[k] = "see %s info" % (a.bin or "binary")
    mach = m.get("machine", {})
    for k, v in list(mach.items()):
        if v == "@slurm":
            mach[k] = socket.gethostname() if k == "host" else os.environ.get("SLURM_JOB_ID", "none")
    prm = m.get("params", {})
    if prm.get("threads") == "@slurm":
        prm["threads"] = int(os.environ.get("SLURM_CPUS_PER_TASK", "1"))
    for s in a.set:
        key, _, val = s.partition("=")
        node = m
        parts = key.split(".")
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = int(val) if val.lstrip("-").isdigit() else val
    tmp = a.out + ".tmp.%d" % os.getpid()
    with open(tmp, "w") as fh:
        json.dump(m, fh, indent=1)
        fh.write("\n")
    os.replace(tmp, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
