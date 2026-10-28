"""Pull immutable A evidence through one sequential SSH connection, verify SHA-256.

No computations, fitting, or removal. Remote members must be inside A and finished.
Usage: python pull_evidence.py TAG runs/run1 [dev500 ...]
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone

tag, *members = sys.argv[1:]
if not re.fullmatch(r"[A-Za-z0-9_-]+", tag) or not members:
    raise SystemExit("tag and members required")
for member in members:
    p = PurePosixPath(member)
    if p.is_absolute() or ".." in p.parts or (p.parts[0] not in {"runs", "dev500", "dev1000"} and not re.fullmatch(r"v[0-9]+dev(?:500|1000)",p.parts[0])):
        raise SystemExit("member outside A evidence scope")
root = "/home/fb31/smcbvs_v3_deploy_20261022/A_build"
dest = Path(r"C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\A_build")
dest.mkdir(parents=True, exist_ok=True)
archive = dest / (tag + ".tar.gz")
if archive.exists():
    raise SystemExit("archive exists; choose a new tag")
script = "set -euo pipefail\ncd " + shlex.quote(root) + "\n"
for member in members:
    script += 'test "$(realpath ' + shlex.quote(member) + ')" != "' + root + '"\n'
    script += 'case "$(realpath ' + shlex.quote(member) + ')/" in "' + root + '/"*) ;; *) exit 2;; esac\n'
    if member.startswith("runs/"):
        script += "test -f " + shlex.quote(member + "/exit_status.txt") + " || test -f " + shlex.quote(member + "/cancel_reason.txt") + "\n"
script += "mkdir -p exports\n"
remote = "exports/" + tag + ".tar.gz"
script += "test ! -e " + shlex.quote(remote) + "\n"
script += "tar --exclude=shared_compile_cache --exclude=.cpp_cache -czf " + shlex.quote(remote) + " " + " ".join(map(shlex.quote, members)) + "\n"
script += "sha256sum " + shlex.quote(remote) + "\ncat " + shlex.quote(remote) + "\n"
proc = subprocess.Popen(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "owls", "nice -n 19 bash -s"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
proc.stdin.write(script.encode()); proc.stdin.close()
line = proc.stdout.readline().decode().strip()
expected = line.split()[0] if line else ""
if not re.fullmatch(r"[0-9a-f]{64}", expected):
    proc.wait()
    raise SystemExit("remote archive did not return a SHA-256: " + line)
h = hashlib.sha256()
with archive.open("xb") as target:
    while True:
        chunk = proc.stdout.read(1024 * 1024)
        if not chunk:
            break
        h.update(chunk); target.write(chunk)
rc = proc.wait()
actual = h.hexdigest()
record = {"utc": datetime.now(timezone.utc).isoformat(), "archive": str(archive),
          "remote": root + "/" + remote, "members": members, "expected_sha256": expected,
          "sha256": actual, "ssh_exit_status": rc, "verified": rc == 0 and actual == expected}
(dest / (tag + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
if not record["verified"]:
    raise SystemExit("transfer verification failed; remote files retained")
