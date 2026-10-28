"""Byte-preserving, source-only deployment snapshot; no numerical workload.

Run locally: python A_build/build/freeze.py TAG
Writes only A_build/snapshots/TAG and A_build/artifacts/TAG.tar.gz.
The fixed prototype source hashes are checked before copying.
"""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tarfile
from datetime import datetime, timezone


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    base = Path(__file__).resolve().parents[1]
    project = base.parents[2]
    packet = project / "01_Methodology_and_Theory/MASTER_Methodology_and_Plan/deployment_20261022_v3"
    master = packet.parent / "MASTER_Methodology_and_Plan.md"
    expected_master = "7d77dddb968135d86a6b6431a7a3e04e122eb0c09f5ec9a6a8329e9a20757b6e"
    if sha(master) != expected_master:
        raise RuntimeError("Master contract hash changed")
    tag = sys.argv[1]
    if not tag or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in tag):
        raise ValueError("Invalid snapshot tag")
    for folder in ("build", "tests", "smoke"):
        for script in (base / folder).rglob("*.sh"):
            if b"\r" in script.read_bytes():
                raise RuntimeError("Shell source must be LF-only: " + str(script))
    dest = base / "snapshots" / tag
    dest.mkdir(parents=True, exist_ok=False)
    for folder in ("code", "tests", "smoke", "build"):
        shutil.copytree(base / folder, dest / folder,
                        ignore=shutil.ignore_patterns(".cpp_cache", "__pycache__", "*.o", "*.so"))
    proto = packet / "source_snapshots/prototype_core"
    provenance = []
    for line in (packet / "source_snapshots/prototype_core.sha256").read_text(encoding="utf-8").splitlines():
        digest, name = line.split(" ", 1)
        name = name.strip().lstrip("*").removeprefix("./")
        if name.startswith(".cpp_cache/"):
            continue
        source = proto / name
        if sha(source) != digest:
            raise RuntimeError(f"Prototype hash mismatch: {name}")
        target = dest / "reference/prototype_core" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        provenance.append({"path": name, "sha256": digest})
    for name in ("CHANGES.md", "RULINGS_OPEN.md", "RULINGS_2.md", "RULINGS_3.md"):
        shutil.copyfile(packet / name, dest / "reference" / name)
    shutil.copyfile(master, dest / "reference/MASTER_Methodology_and_Plan.md")
    shutil.copyfile(base.parent / "BRIEF.md", dest / "reference/BRIEF.md")
    shutil.copyfile(base.parent / "RULINGS_LEAD.md", dest / "reference/RULINGS_LEAD.md")
    generator = project / "02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/code/R/gen_dev_data.R"
    shutil.copyfile(generator, dest / "reference/gen_dev_data.R")
    files = [{"path": f.relative_to(dest).as_posix(), "sha256": sha(f), "bytes": f.stat().st_size}
             for f in sorted(dest.rglob("*")) if f.is_file()]
    manifest = {"snapshot": tag, "created_utc": datetime.now(timezone.utc).isoformat(),
                "master_sha256": expected_master, "files": files, "reference_sources": provenance,
                "environment_required": {"GCC": "11.5.0", "R": "4.6.0", "threads": 1, "nice": 19},
                "remote_root": "/home/fb31/smcbvs_v3_deploy_20261022/A_build/" + tag,
                "validation_targets": {
                    "Owls": {"GCC": "11.5.0", "R": "4.6.0", "purpose": "development validation"},
                    "NOTS": {"GCC": "14.3.0", "R": "4.5.2", "purpose": "required before any NOTS fit",
                             "status": "not_executed_gate_closed", "gate": "NOTS: open for runs",
                             "source_root": "/projects/ml75/fb31/BVS/smcbvs_v3_deploy_20261022/code/snapshots/" + tag}},
                "job_ids": [], "commands": [], "status": "frozen_unrun"}
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    lines = [f"{x['sha256']}  {x['path']}" for x in files]
    lines.append(f"{sha(dest / 'manifest.json')}  manifest.json")
    # sha256sum treats CR as part of the filename; keep the inventory LF-only even on Windows.
    (dest / "SHA256SUMS").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    artifacts = base / "artifacts"
    artifacts.mkdir(exist_ok=True)
    archive = artifacts / (tag + ".tar.gz")
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(dest, arcname=tag)
    record = {"snapshot": str(dest), "manifest_sha256": sha(dest / "manifest.json"),
              "checksums_sha256": sha(dest / "SHA256SUMS"), "archive": str(archive),
              "archive_sha256": sha(archive)}
    (artifacts / (tag + ".json")).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
