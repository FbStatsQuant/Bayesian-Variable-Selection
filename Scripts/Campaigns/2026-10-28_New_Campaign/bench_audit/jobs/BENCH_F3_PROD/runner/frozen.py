#!/usr/bin/env python3
"""Verify the manifest's own hash, exact F3 tree membership, and each file hash."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1048576), b""):
            h.update(b)
    return h.hexdigest()


def check(tree, manifest, freeze):
    config = json.loads(freeze.read_text(encoding="utf-8"))
    for name in ("manifest_sha256", "source_sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", config[name]):
            raise ValueError(f"{name}: manager must replace the freeze placeholder")
    if sha(manifest) != config["manifest_sha256"]:
        raise ValueError("manifest digest differs from frozen value")
    wanted = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
        if not m:
            raise ValueError("invalid manifest line")
        path = m[2].removeprefix("./")
        if not path.startswith("F3_AdaptiveLasso/"):
            continue
        rel = path[len("F3_AdaptiveLasso/"):]
        if not rel or rel.startswith("/") or ".." in Path(rel).parts or rel in wanted:
            raise ValueError("unsafe or duplicate F3 manifest entry")
        wanted[rel] = m[1]
    if not wanted or "run_case.R" not in wanted:
        raise ValueError("manifest lacks F3 tree")
    if any(p.is_symlink() for p in tree.rglob("*")):
        raise ValueError("symlinks forbidden")
    got = {p.relative_to(tree).as_posix() for p in tree.rglob("*") if p.is_file()}
    if got != set(wanted):
        raise ValueError(f"tree membership mismatch missing={sorted(set(wanted)-got)} extra={sorted(got-set(wanted))}")
    for rel, expected in wanted.items():
        if sha(tree / rel) != expected:
            raise ValueError("hash mismatch: " + rel)
    files = ("config.R", "common.R", "methods/glmnet_helpers.R",
             "methods/fit_F3_alasso.R", "run_case.R")
    text = "\n".join(f"{name}  {sha(tree / name)}" for name in files)
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != config["source_sha256"]:
        raise ValueError("runner source tree digest mismatch; confirm CODE_FILES at freeze")
    return config


def main(argv):
    if len(argv) not in (4, 5) or argv[0] not in ("check", "stage"):
        sys.exit("usage: frozen.py check TREE MANIFEST FREEZE | stage SOURCE MANIFEST FREEZE DEST")
    action, tree, manifest, freeze = argv[:4]
    tree, manifest, freeze = map(Path, (tree, manifest, freeze))
    if not all(p.is_absolute() for p in (tree, manifest, freeze)):
        raise ValueError("absolute paths required")
    check(tree, manifest, freeze)
    if action == "stage":
        if len(argv) != 5:
            raise ValueError("stage requires destination")
        dest = Path(argv[4])
        if str(dest) != "/home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso":
            raise ValueError("destination is not the authorized F3 code path")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            check(dest, manifest, freeze)
        else:
            shutil.copytree(tree, dest, symlinks=False)
            check(dest, manifest, freeze)
    print("FROZEN_OK")


if __name__ == "__main__":
    main(sys.argv[1:])
