#!/usr/bin/env python3
"""Prepare a reviewed upload folder; this tool does not connect to NOTS."""
import hashlib
from pathlib import Path
import re
import shutil
import sys
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "runner"))
import frozen


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: prepare.py dev|prod RUN_ID absolute_bench_v2_directory")
    kind, run_id, code_arg = sys.argv[1:]
    if kind not in ("dev", "prod") or not re.fullmatch(r"[0-9]{8}T[0-9]{4,6}Z_bench_f3v2_" + kind, run_id):
        raise ValueError("bad run id")
    code = Path(code_arg)
    if not code.is_absolute():
        raise ValueError("absolute code path required")
    manifest = code / "MANIFEST_SHA256.txt"
    tree = code / "F3_AdaptiveLasso"
    freeze = HERE / "runner" / "freeze.json"
    frozen.check(tree, manifest, freeze)
    target = HERE.parent / "staging" / run_id
    if target.exists():
        raise ValueError("upload folder already exists")
    target.mkdir(parents=True)
    shutil.copytree(tree, target / "F3_AdaptiveLasso")
    shutil.copy2(manifest, target / "MANIFEST_SHA256.txt")
    shutil.copytree(HERE / "runner", target / "runner",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(manifest, target / "runner" / "MANIFEST_SHA256.txt")
    shutil.copy2(HERE.parent / "BENCH_F3_DEV" / "runner" / "sizing.py", target / "runner" / "sizing.py")
    job = HERE.parent / ("BENCH_F3_DEV" if kind == "dev" else "BENCH_F3_PROD") / "JOB.md"
    shutil.copy2(job, target / "JOB.md")
    frozen.check(target / "F3_AdaptiveLasso", target / "MANIFEST_SHA256.txt", target / "runner" / "freeze.json")
    lines = []
    for f in sorted(p for p in target.rglob("*") if p.is_file()):
        lines.append(f"{frozen.sha(f)}  {f.relative_to(target).as_posix()}\n")
    bundle_manifest = target / "UPLOAD_SHA256.txt"
    bundle_manifest.write_text("".join(lines), encoding="utf-8", newline="\n")
    print("upload_folder", target)
    print("upload_manifest_sha256", frozen.sha(bundle_manifest))


if __name__ == "__main__":
    main()
