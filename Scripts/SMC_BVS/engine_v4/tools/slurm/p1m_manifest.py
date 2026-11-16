#!/usr/bin/env python3
"""p1m_manifest.py -- fill a job-manifest template at run time (INTERFACES §5.3). Stdlib only; Python >= 3.6.

  p1m_manifest.py fill --template T.json --out M.json [--bin PATH] [--set a.b=v ...]

Placeholders in the template:
  inputs {"<path>": "@hash"} -> the content hash of the .bin at <path> = SHA-256 of its section table (INTERFACES §5.1;
                            what smcbvs4 checks), after checking the table against the header; the producer's record
                            <path>.json must exist with "status": "completed", else exit (refuse to start)
  "@binary"              -> binary.sha256 = SHA-256 of --bin (default $BIN); compiler/flags/libm = "see <bin> info"
  "@slurm"               -> machine.host / slurm_job_id / params.threads from the Slurm environment
"""
import argparse
import hashlib
import json
import os
import socket
import struct
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def content_hash(path):
    """Content hash of an engine container (INTERFACES §5.1).
    v0.1.2: FileHeader.content_sha256 (bytes 64..96) = SHA-256(header with table_sha256 and content_sha256 zeroed || table).
    v0.1.1 files (content field all zero): the SHA-256 of the section table. The table hash (bytes 32..64) is checked in
    both cases."""
    with open(path, "rb") as fh:
        hdr = fh.read(128)
        if len(hdr) < 128 or hdr[:8] != b"SMCBVS4\0":
            raise SystemExit("p1m_manifest: %s is not an engine container: refusing to start" % path)
        ns = struct.unpack_from("<I", hdr, 20)[0]
        table = fh.read(128 * ns)
    th = hashlib.sha256(table).digest()
    if th != hdr[32:64]:   # FileHeader: magic 8, 4 x u32, u64 file_bytes, table_sha256, content_sha256, reserved
        raise SystemExit("p1m_manifest: %s: section table hash mismatch: refusing to start" % path)
    stored = hdr[64:96]
    if stored == b"\0" * 32:
        return th.hex()
    zeroed = hdr[:32] + b"\0" * 64 + hdr[96:128]
    ch = hashlib.sha256(zeroed + table).digest()
    if ch != stored:
        raise SystemExit("p1m_manifest: %s: content hash mismatch: refusing to start" % path)
    return ch.hex()


def check_record(path):
    rp = path + ".json"
    try:
        with open(rp) as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as e:
        raise SystemExit("p1m_manifest: cannot read the producer record %s (%s): refusing to start" % (rp, e))
    if rec.get("status") != "completed":
        raise SystemExit("p1m_manifest: %s has status %r: refusing to start" % (rp, rec.get("status")))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fill"])
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bin", default=os.environ.get("BIN", ""))
    ap.add_argument("--set", action="append", default=[])
    a = ap.parse_args(argv)
    with open(a.template) as fh:
        m = json.load(fh)
    for k, v in list(m.get("inputs", {}).items()):
        if v == "@hash":
            check_record(k)
            m["inputs"][k] = content_hash(k)
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
