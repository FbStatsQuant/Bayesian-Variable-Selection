"""Single-SSH bootstrap: read/verify reviewed remote AGENTS before any mutation.

Executed using python3 -B -c; not a numerical program. Never calls production.
"""
import hashlib
import io
import json
import os
import re
from pathlib import Path, PurePosixPath
import shutil
import socket
import subprocess
import sys
import tarfile
from datetime import datetime, timezone

D = Path("/projects/ml75/fb31/BVS/smcbvs_v3_deploy_20261022")
CODE = D / "code"
SCRATCH = Path("/scratch/fb31/smcbvs_v3_deploy_20261022/A_build")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def instructions(config):
    # Include existing ancestors, future destination, home/cwd and resolved symlink paths.
    paths = set()
    for target in (Path.home(), Path.cwd(), CODE / "snapshots" / config["tag"],
                   CODE / "validation" / config["run"], SCRATCH / config["run"]):
        for root in (target, target.resolve()):
            paths.update([root, *root.parents])
    rows = []
    for root in sorted(paths):
        path = root / "AGENTS.md"
        if path.exists():
            data = path.read_bytes()
            rows.append(dict(path=str(path), sha256=sha(data), text=data.decode("utf-8-sig")))
        else:
            rows.append(dict(path=str(path), absent=True))
    return rows


def main():
    config_line = sys.stdin.buffer.readline(4 * 1024**2 + 1)
    if len(config_line) > 4 * 1024**2 or not config_line.endswith(b"\n"):
        raise SystemExit("Missing/oversize framed launch configuration")
    config = json.loads(config_line)
    observed = instructions(config)
    digest = sha(canonical(observed))
    # Reading instructions is the first filesystem operation other than Python loading.
    # Observation prints their FULL contents and absence inventory, without writing remotely.
    if config["action"] == "observe":
        print(json.dumps(dict(instructions=observed, instructions_sha256=digest,
                             hostname=socket.getfqdn(), observed_utc=datetime.now(timezone.utc).isoformat()), indent=2))
        return
    if config["action"] != "submit" or observed != config["instructions"] or digest != config["instructions_sha256"]:
        raise SystemExit("Remote AGENTS changed or not reviewed; NO remote writes/submission")
    if os.getuid() != __import__("pwd").getpwnam("fb31").pw_uid:
        raise SystemExit("Wrong remote user")
    for root in (CODE, SCRATCH):
        if root.resolve() != root:
            raise SystemExit("Ownership root traverses a symlink; request reviewed path update")
    if not CODE.is_dir():
        raise SystemExit("Managing lead must provision A-owned $D/code before submission")
    if not re.fullmatch(r"(?:v1_r[1-9][0-9]*|v[2-9][0-9]*(?:_r[1-9][0-9]*)?)", config["tag"]) or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in config["run"]):
        raise SystemExit("Unsafe snapshot/run")
    snapshot = CODE / "snapshots" / config["tag"]
    receipt = CODE / "validation" / config["run"]
    out = SCRATCH / config["run"]
    if any(p.exists() for p in (snapshot, receipt, out)):
        raise SystemExit("Snapshot or run exists: never overwrite or automatically resubmit")
    for path in (snapshot, receipt, out):
        if path.resolve() != path:
            raise SystemExit("Destination traverses symlink")
    archive_data = sys.stdin.buffer.read(100 * 1024**2 + 1)
    if len(archive_data) > 100 * 1024**2 or sha(archive_data) != config["archive_sha256"]:
        raise SystemExit("Transferred archive hash/size mismatch")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive_data), mode="r:gz") as archive:
        total = 0
        for item in archive.getmembers():
            name = PurePosixPath(item.name)
            if name.is_absolute() or ".." in name.parts or not name.parts or name.parts[0] != config["tag"]:
                raise SystemExit("Unsafe archive member")
            if item.isdir():
                continue
            total += item.size
            if total > 200 * 1024**2 or not item.isfile() or "AGENTS.md" in name.parts:
                raise SystemExit("Oversize/new instruction/link/special member")
            rel = PurePosixPath(*name.parts[1:]).as_posix()
            if rel in files:
                raise SystemExit("Duplicate archive path")
            files[rel] = archive.extractfile(item).read()
    manifest = json.loads(files["manifest.json"])
    expected = {x["path"]: x["sha256"] for x in manifest["files"]}
    if manifest["snapshot"] != config["tag"] or len(expected) != len(manifest["files"]):
        raise SystemExit("Invalid source manifest")
    if set(files) != set(expected) | {"manifest.json", "SHA256SUMS"}:
        raise SystemExit("Unmanifested files")
    for path, digest in expected.items():
        if sha(files[path]) != digest:
            raise SystemExit("Source hash mismatch: " + path)
    if sha(files["manifest.json"]) != config["manifest_sha256"] or sha(files["SHA256SUMS"]) != config["inventory_sha256"]:
        raise SystemExit("Pinned source manifest/inventory mismatch")
    # All validation above is read-only. Frozen source/project receipt are small;
    # all compilation caches, generated data, raw RDS and logs go to scratch.
    os.umask(0o077)
    snapshot.mkdir(parents=True, exist_ok=False)
    receipt.mkdir(parents=True, exist_ok=False)
    out.mkdir(parents=True, exist_ok=False)
    for rel, data in files.items():
        path = snapshot / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    with (receipt / "source_validation.log").open("wb") as log:
        subprocess.run(["sha256sum", "--strict", "-c", "SHA256SUMS"], cwd=snapshot, stdout=log, stderr=subprocess.STDOUT, check=True)
    (receipt / "launch.json").write_bytes(canonical(config) + b"\n")
    (receipt / "remote_agents.json").write_bytes(canonical(observed) + b"\n")
    (receipt / "snapshot_archive.sha256").write_text(config["archive_sha256"] + "\n")
    shutil.copyfile(receipt / "launch.json", out / "launch.json")
    shutil.copyfile(receipt / "remote_agents.json", out / "remote_agents.json")
    # Snapshot bytes stay frozen; v3.R compilation runs only on a scratch copy.
    for path in snapshot.rglob("*"):
        path.chmod(0o500 if path.is_dir() else 0o400)
    snapshot.chmod(0o500)
    command = ["sbatch", "--parsable", "--account=" + config["account"], "--partition=" + config["partition"],
               "--job-name=A-nots-regression", "--nodes=1", "--ntasks=1", "--cpus-per-task=1",
               "--mem=" + str(config["mem_mb"]) + "M", "--time=" + config["time"],
               "--export=NONE", "--chdir=" + str(out), "--output=" + str(out / "slurm-%j.out"),
               "--error=" + str(out / "slurm-%j.err"), str(snapshot / "build/nots_job.sh"),
               str(snapshot), str(out), str(receipt)]
    (receipt / "sbatch_command.json").write_bytes(canonical(command) + b"\n")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    (receipt / "sbatch.stdout").write_bytes(result.stdout)
    (receipt / "sbatch.stderr").write_bytes(result.stderr)
    (receipt / "submission_exit_status.txt").write_text(str(result.returncode) + "\n")
    (receipt / "submitted_utc.txt").write_text(datetime.now(timezone.utc).isoformat() + "\n")
    if result.returncode:
        raise SystemExit("sbatch failed; retained source and receipt; inspect, do not blindly retry")
    job = result.stdout.decode().strip().split(";")[0]
    if not job.isdigit():
        raise SystemExit("Unrecognized sbatch response; inspect before any retry")
    (receipt / "job_id.txt").write_text(job + "\n")
    print(json.dumps(dict(submitted=True, job_id=job, snapshot=str(snapshot), receipt=str(receipt), scratch=str(out),
                          production_launched=False), indent=2))


if __name__ == "__main__":
    main()
