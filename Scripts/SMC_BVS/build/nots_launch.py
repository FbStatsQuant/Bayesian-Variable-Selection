"""Windows, stdlib-only NOTS validation launcher. No production entry point.

Every invocation checks the managing-lead gate BEFORE its sole network call.
Use observe to obtain remote instructions; submit requires their reviewed digest.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
import tarfile
from datetime import datetime, timezone


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def frozen_archive(path, tag, archive_hash, manifest_hash, inventory_hash):
    data = path.read_bytes()
    if len(data) > 100 * 1024**2 or sha(data) != archive_hash:
        raise ValueError("Archive size/hash mismatch")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        expanded = 0
        for item in archive.getmembers():
            name = PurePosixPath(item.name)
            if name.is_absolute() or ".." in name.parts or not name.parts or name.parts[0] != tag:
                raise ValueError("Unsafe archive path")
            if item.isdir():
                continue
            if not item.isfile() or "AGENTS.md" in name.parts:
                raise ValueError("Links/special files/new AGENTS forbidden in archive")
            expanded += item.size
            if expanded > 200 * 1024**2:
                raise ValueError("Expanded archive size exceeds 200 MiB")
            rel = PurePosixPath(*name.parts[1:]).as_posix()
            if rel in files:
                raise ValueError("Duplicate archive member")
            files[rel] = archive.extractfile(item).read()
    if sha(files["manifest.json"]) != manifest_hash or sha(files["SHA256SUMS"]) != inventory_hash:
        raise ValueError("Manifest/inventory hash mismatch")
    manifest = json.loads(files["manifest.json"])
    if manifest["snapshot"] != tag:
        raise ValueError("Snapshot tag mismatch")
    expected = {x["path"]: x["sha256"] for x in manifest["files"]}
    if len(expected) != len(manifest["files"]) or set(files) != set(expected) | {"manifest.json", "SHA256SUMS"}:
        raise ValueError("Manifest coverage mismatch")
    for name, digest in expected.items():
        if sha(files[name]) != digest:
            raise ValueError(f"Frozen source mismatch: {name}")
    sums = {}
    for line in files["SHA256SUMS"].decode("utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if name in sums:
            raise ValueError("Duplicate inventory row")
        sums[name] = digest
    if sums != {**expected, "manifest.json": manifest_hash}:
        raise ValueError("Inventory does not cover manifest exactly")
    for name in ("nots_remote.py", "nots_job.sh", "nots_build.R", "nots_regression.sh"):
        if f"build/{name}" not in expected:
            raise ValueError(f"Missing NOTS wrapper: {name}")
    return data, files


def main():
    # Both live build/ and immutable snapshots/TAG/build/ must read the same lead gate.
    base = next((p for p in Path(__file__).resolve().parents if p.name == "A_build"), None)
    if base is None:
        raise SystemExit("A_build ownership root not found; no network attempted")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("observe", "submit"))
    parser.add_argument("--evidence", type=Path, required=True, help="New local directory; never overwritten")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--ack-instructions-sha256")
    parser.add_argument("--tag", default="v2")
    parser.add_argument("--run", required=True)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--archive-sha256")
    parser.add_argument("--manifest-sha256")
    parser.add_argument("--inventory-sha256")
    parser.add_argument("--module-init", required=True, help="Previously confirmed absolute module initialization script")
    parser.add_argument("--r-library", required=True, help="Explicit preprovisioned NOTS R 4.5.2 package library")
    parser.add_argument("--deps", type=Path, required=True, help='JSON exact versions: Rcpp, digest, jsonlite')
    parser.add_argument("--account", required=True)
    parser.add_argument("--partition", required=True)
    parser.add_argument("--cluster", required=True, help="Previously confirmed SLURM_CLUSTER_NAME")
    parser.add_argument("--time", required=True, help="Slurm HH:MM:SS wall limit")
    parser.add_argument("--mem-mb", type=int, required=True)
    a = parser.parse_args()
    # Fixed location, no CLI override, exact whole line: no substring/quoted/negated gate.
    status = base.parent / "STATUS.md"
    status_bytes = status.read_bytes()
    if "NOTS: open for runs" not in status_bytes.decode("utf-8-sig").splitlines():
        raise SystemExit("CLOSED: deployment STATUS.md lacks exact line NOTS: open for runs; no network attempted")
    if not re.fullmatch(r"(?:v1_r[1-9][0-9]*|v[2-9][0-9]*(?:_r[1-9][0-9]*)?)", a.tag) or not re.fullmatch(r"[A-Za-z0-9_-]+", a.run):
        raise ValueError("Only new revision snapshots and safe run IDs accepted; frozen v1 is immutable")
    for value in (a.account, a.partition, a.cluster):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
            raise ValueError("Unsafe Slurm account/partition")
    if not re.fullmatch(r"[0-9]{1,3}:[0-5][0-9]:[0-5][0-9]", a.time) or not 1024 <= a.mem_mb <= 16384:
        raise ValueError("Explicit wall limit and 1024..16384 MiB required")
    for value in (a.module_init, a.r_library):
        if not value.startswith("/") or any(c.isspace() for c in value) or ".." in PurePosixPath(value).parts:
            raise ValueError("Module/library paths must be absolute, without whitespace or traversal")
    deps = json.loads(a.deps.read_text(encoding="utf-8-sig"))
    if set(deps) != {"Rcpp", "digest", "jsonlite"} or not all(isinstance(v, str) and re.fullmatch(r"[0-9]+(?:[.-][0-9]+)+", v) for v in deps.values()):
        raise ValueError("Specify all three exact installed dependency versions")
    config = dict(action=a.action, tag=a.tag, run=a.run, module_init=a.module_init,
                  r_library=a.r_library, deps=deps, account=a.account, partition=a.partition, cluster=a.cluster,
                  time=a.time, mem_mb=a.mem_mb, status_sha256=sha(status_bytes),
                  local_utc=datetime.now(timezone.utc).isoformat(), local_command=sys.argv)
    payload = b""
    remote_source = Path(__file__).with_name("nots_remote.py").read_bytes()
    if a.action == "submit":
        if not all((a.archive, a.archive_sha256, a.manifest_sha256, a.inventory_sha256, a.receipt, a.ack_instructions_sha256)):
            raise ValueError("Submit needs archive plus three independent expected hashes, receipt and reviewed acknowledgment")
        receipt = json.loads(a.receipt.read_text(encoding="utf-8"))
        if sha(canonical(receipt["instructions"])) != a.ack_instructions_sha256 or receipt["instructions_sha256"] != a.ack_instructions_sha256:
            raise ValueError("Remote instructions acknowledgment mismatch")
        payload, frozen = frozen_archive(a.archive, a.tag, a.archive_sha256, a.manifest_sha256, a.inventory_sha256)
        remote_source = frozen["build/nots_remote.py"]
        config.update(archive_sha256=a.archive_sha256, manifest_sha256=a.manifest_sha256,
                      inventory_sha256=a.inventory_sha256, instructions=receipt["instructions"],
                      instructions_sha256=a.ack_instructions_sha256)
    if a.evidence.exists():
        raise ValueError("Refusing to overwrite local evidence")
    a.evidence.mkdir(parents=True)
    (a.evidence / "request.json").write_bytes(canonical(config) + b"\n")
    (a.evidence / "remote_source.sha256").write_text(sha(remote_source) + "\n")
    command = ["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30", "-o", "ConnectionAttempts=1",
               "nots", "python3 -B -c " + shlex.quote(remote_source.decode("utf-8"))]
    (a.evidence / "ssh_command.json").write_bytes(canonical(command) + b"\n")
    # Re-read immediately before the only network operation (gate may close during preparation).
    if "NOTS: open for runs" not in status.read_text(encoding="utf-8-sig").splitlines():
        raise SystemExit("Gate closed during preparation; no network attempted")
    with (a.evidence / "ssh.stdout.log").open("wb") as out, (a.evidence / "ssh.stderr.log").open("wb") as err:
        # One framed stdin stream avoids Windows command-line limits for full
        # AGENTS receipts. Python reads its JSON line, then the exact tar bytes.
        result = subprocess.run(command, input=canonical(config) + b"\n" + payload, stdout=out, stderr=err, check=False)
    (a.evidence / "ssh_exit_status.txt").write_text(str(result.returncode) + "\n")
    (a.evidence / "finished_utc.txt").write_text(datetime.now(timezone.utc).isoformat() + "\n")
    if result.returncode:
        raise SystemExit("SSH/bootstrap failed; inspect saved logs. After any timeout wait >=15 min; inspect remote state before retry; never duplicate a live job.")
    print((a.evidence / "ssh.stdout.log").read_text(encoding="utf-8"))
    if a.action == "submit":
        print("SUBMITTED ONLY: inspect Slurm status and saved outputs later (poll >=10 min). No NOTS validation pass claimed.")


if __name__ == "__main__":
    main()
