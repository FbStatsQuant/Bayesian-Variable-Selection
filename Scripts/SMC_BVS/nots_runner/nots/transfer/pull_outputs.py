"""Pull frozen NOTS C_ops outputs with per-file SHA-256 and separate opt-in deletion.

Python standard library only; run on the laptop, using its existing SSH setup.
"""
import argparse
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import struct
import subprocess
import sys
import threading
import uuid
import time

import remote

DEST = Path(r"C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022")
HERE = Path(__file__).absolute().parent
REMOTE_HELPER = "/home/fb31/projects/BVS/SMC_BVS_v3/deploy/claude/transfer/remote.py"


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                return h.hexdigest()
            h.update(b)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def safe_local(path, create=False):
    """Reject junctions/reparse points as well as symbolic links on Windows."""
    path = Path(os.path.abspath(path))
    for component in [*reversed(path.parents), path]:
        try:
            s = os.lstat(component)
        except FileNotFoundError:
            if create:
                component.mkdir()
                s = os.lstat(component)
            else:
                continue
        if stat.S_ISLNK(s.st_mode) or getattr(s, "st_file_attributes", 0) & 0x400:
            raise ValueError("Local symlink/reparse point rejected: " + str(component))
    return path


def write_json(path, value):
    safe_local(path.parent)
    temp = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    with open(temp, "x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    safe_local(path)
    os.replace(temp, path)


def event(folder, value):
    path = folder / "events.jsonl"
    safe_local(path)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(dict(utc=now(), **value), sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def destination(subtree, relative=None):
    names = remote.parts(subtree)
    if relative is not None:
        names += remote.parts(relative)
    path = DEST.joinpath(*names)
    if os.path.commonpath([str(DEST), str(path)]) != str(DEST):
        raise ValueError("Destination escaped fixed root")
    safe_local(path)
    return path


def check_entries(entries):
    seen = set()
    for e in entries:
        remote.parts(e["path"])
        key = e["path"].casefold()
        if key in seen:
            raise ValueError("Case-insensitive path collision")
        seen.add(key)
        if (not isinstance(e["size"], int) or isinstance(e["size"], bool)
                or e["size"] < 0 or len(e["sha256"]) != 64
                or any(c not in "0123456789abcdef" for c in e["sha256"])):
            raise ValueError("Malformed file size/hash")
    # A Windows file cannot simultaneously be another file's parent directory.
    for key in seen:
        components = key.split("/")
        if any("/".join(components[:i]) in seen for i in range(1, len(components))):
            raise ValueError("File/directory collision")


def require_run_gate():
    status = HERE.parents[2] / "STATUS.md"
    # Claude E_ops (AUDIT_C_OPS finding 10): accept the managing lead's line in any letter case,
    # with trailing remarks, as C's r3 backend does (root STATUS.md says "NOTS: OPEN FOR RUNS (...)").
    import re
    if not any(re.match(r"NOTS: open for runs\b", line.strip(), re.IGNORECASE)
               for line in status.read_text(encoding="utf-8-sig").splitlines()):
        raise RuntimeError("NOTS closed: managing-lead STATUS.md lacks exact open-for-runs line")
    backoff = DEST / ".transfer_audit" / ".nots-backoff.json"
    if backoff.exists() and time.time() < load(backoff)["retry_after_epoch"]:
        raise RuntimeError("NOTS connection backoff active; wait 15 minutes after failed operation")


def mark_backoff():
    write_json(DEST / ".transfer_audit" / ".nots-backoff.json",
               {"utc": now(), "retry_after_epoch": time.time() + 900})


def ssh_prefix():
    require_run_gate()
    # Amendment 2 / R-4: direct configured NOTS host only, gated; no fallback.
    return ["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
            "-o", "ConnectionAttempts=1", "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=2", "-o", "StrictHostKeyChecking=yes", "nots"]


class LocalLock:
    """Hold a kernel lock for the complete invocation; crashes release the lock."""
    def __enter__(self):
        path = safe_local(DEST / ".transfer_audit", create=True) / ".nots-transfer.lock"
        safe_local(path)
        self.stream = open(path, "a+b")
        try:
            if os.fstat(self.stream.fileno()).st_size == 0:
                self.stream.write(b"0")
                self.stream.flush()
            self.stream.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BaseException:
            self.stream.close()
            raise RuntimeError("Another NOTS transfer invocation owns the lock; serialize calls")
        return self

    def __exit__(self, *exc):
        if os.name == "nt":
            import msvcrt
            self.stream.seek(0)
            msvcrt.locking(self.stream.fileno(), msvcrt.LK_UNLCK, 1)
        self.stream.close()


class Session:
    def __init__(self, args, folder):
        self.args, self.folder, self.counter = args, folder, 0
        self.source = (HERE / "remote.py").read_bytes()

    def start(self, request):
        self.counter += 1
        stem = "ssh-%02d-%s" % (self.counter, request["action"])
        # A single constant, base64-only shell argument; no paths enter shell text.
        encoded = base64.b64encode(self.source).decode("ascii")
        # Claude E_ops: from Windows the inline base64 command failed (double quotes mangled by argv
        # quoting; then the 25 KB payload truncated: "Incorrect padding"). The identical helper is
        # staged once at REMOTE_HELPER and every call verifies its SHA-256 before running it.
        digest = hashlib.sha256(self.source).hexdigest()
        command = ("echo '" + digest + "  " + REMOTE_HELPER + "' | sha256sum --quiet --strict -c - && "
                   "nice -n 19 python3 -B " + REMOTE_HELPER)
        argv = ssh_prefix() + [command]
        write_json(self.folder / (stem + "-request.json"), request)
        write_json(self.folder / (stem + "-launch.json"),
                   {"argv": argv, "utc": now(), "helper_sha256": hashlib.sha256(self.source).hexdigest()})
        err = open(self.folder / (stem + "-stderr.log"), "xb")
        p = None
        try:
            p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err)
            p.transfer_timer = threading.Timer(self.args.ssh_timeout, p.kill)
            p.transfer_timer.daemon = True
            p.transfer_timer.start()
            event(self.folder, {"state": "ssh_started", "action": request["action"], "pid": p.pid})
            p.stdin.write(json.dumps(request).encode("utf-8"))
            p.stdin.close()
        except BaseException:
            if p is not None:
                self.abort(p, err, stem)
            err.close()
            raise
        return p, err, stem

    def finish(self, p, err, stem):
        code = p.wait(timeout=45)
        p.transfer_timer.cancel()
        err.close()
        event(self.folder, {"state": "ssh_finished", "launch": stem, "exit_status": code})
        if code:
            mark_backoff()
            raise RuntimeError("SSH/helper failed (%s); see %s-stderr.log" % (code, stem))

    def abort(self, p, err, stem):
        mark_backoff()
        p.transfer_timer.cancel()
        if p.poll() is None:
            p.terminate()
        try:
            code = p.wait(timeout=10)
        except subprocess.TimeoutExpired:
            p.kill()
            code = p.wait()
        err.close()
        event(self.folder, {"state": "ssh_aborted", "launch": stem, "exit_status": code})

    def json(self, request):
        p, err, stem = self.start(request)
        try:
            raw = p.stdout.read()
            (self.folder / (stem + "-stdout.json")).write_bytes(raw)
            self.finish(p, err, stem)
            return json.loads(raw)
        except BaseException:
            self.abort(p, err, stem)
            raise


def exact(stream, n):
    chunks = []
    remaining = n
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError("Incomplete remote stream")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_frame(stream):
    n = struct.unpack(">Q", exact(stream, 8))[0]
    if n > 8 * 1024 * 1024:
        raise ValueError("Oversized protocol header (possible unexpected SSH output)")
    return json.loads(exact(stream, n))


def verify_local(subtree, entry):
    path = destination(subtree, entry["path"])
    s = os.lstat(path)
    if not stat.S_ISREG(s.st_mode) or s.st_size != entry["size"] or sha(path) != entry["sha256"]:
        raise ValueError("Local file missing/changed: " + str(path))
    after = os.lstat(path)
    if (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns) != (
            after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise ValueError("Local file changed during verification")
    return {"path": str(path), "size": s.st_size, "sha256": entry["sha256"],
            "mtime_ns": s.st_mtime_ns, "verified_utc": now()}


def pull(session, args, base, folder):
    manifest = session.json(dict(base, action="manifest"))
    if manifest["root"] != remote.ROOT or manifest["subtree"] != args.subtree:
        raise ValueError("Unexpected remote source root")
    check_entries(manifest["files"])
    write_json(folder / "manifest.json", manifest)
    safe_local(destination(args.subtree), create=True)
    # Never overwrite an existing destination. Identical files can be reverified on retry.
    pending, verified = [], []
    for entry in manifest["files"]:
        path = destination(args.subtree, entry["path"])
        if path.exists():
            verified.append(verify_local(args.subtree, entry))
        else:
            pending.append(entry)
    receipt = {"schema": 1, "status": "in_progress", "root": remote.ROOT,
               "subtree": args.subtree, "destination_root": str(DEST),
               "manifest_sha256": sha(folder / "manifest.json"),
               "files": manifest["files"], "verified_local": verified,
               "started_utc": now(), "deletion_performed": False}
    write_json(folder / "receipt.json", receipt)
    if pending:
        p, err, stem = session.start(dict(base, action="stream", files=pending))
        try:
            header = read_frame(p.stdout)
            if set(header) != {"runtime"} or header["runtime"].get("nice") != 19:
                raise ValueError("Remote runtime context missing/nice 19 not confirmed")
            write_json(folder / (stem + "-runtime.json"), header["runtime"])
            for entry in pending:
                if read_frame(p.stdout) != {"entry": entry}:
                    raise ValueError("Unexpected streamed entry")
                path = destination(args.subtree, entry["path"])
                safe_local(path.parent, create=True)
                temp = path.with_name(".transfer-" + uuid.uuid4().hex + ".partial")
                h = hashlib.sha256()
                try:
                    with open(temp, "xb") as f:
                        remaining = entry["size"]
                        while remaining:
                            b = exact(p.stdout, min(1024 * 1024, remaining))
                            f.write(b)
                            h.update(b)
                            remaining -= len(b)
                        f.flush()
                        os.fsync(f.fileno())
                    if read_frame(p.stdout) != {"verified": entry["path"]}:
                        raise ValueError("Missing remote post-copy verification")
                    if h.hexdigest() != entry["sha256"] or sha(temp) != entry["sha256"]:
                        raise ValueError("Local copy SHA-256 mismatch")
                    os.utime(temp, ns=(entry["mtime_ns"], entry["mtime_ns"]))
                    safe_local(path)
                    # Windows rename refuses overwrite. Link provides no-clobber on POSIX.
                    if os.name == "nt":
                        os.rename(temp, path)
                    else:
                        os.link(temp, path, follow_symlinks=False)
                        os.unlink(temp)
                    verified.append(verify_local(args.subtree, entry))
                    write_json(folder / "receipt.json", receipt)
                    event(folder, {"state": "file_verified", "entry": entry})
                finally:
                    if temp.exists():
                        safe_local(temp)
                        temp.unlink()
            if read_frame(p.stdout) != {"complete": True} or p.stdout.read(1):
                raise ValueError("Unexpected stream trailer")
            session.finish(p, err, stem)
        except BaseException:
            session.abort(p, err, stem)
            raise
    # A receipt becomes deletion-eligible only after a fresh hash of every local file.
    receipt["verified_local"] = [verify_local(args.subtree, e) for e in manifest["files"]]
    receipt.update(status="verified", completed_utc=now())
    write_json(folder / "receipt.json", receipt)
    return folder / "receipt.json"


def delete(session, args, base, folder):
    receipt_path = safe_local(Path(args.receipt).absolute())
    receipt = load(receipt_path)
    if (receipt.get("status") != "verified" or receipt.get("root") != remote.ROOT
            or receipt.get("subtree") != args.subtree or receipt.get("destination_root") != str(DEST)):
        raise ValueError("Receipt is unverified or for a different fixed root/subtree")
    manifest_path = safe_local(receipt_path.parent / "manifest.json")
    if sha(manifest_path) != receipt["manifest_sha256"] or load(manifest_path)["files"] != receipt["files"]:
        raise ValueError("Receipt/manifest integrity mismatch")
    check_entries(receipt["files"])
    allow = load(safe_local(Path(args.allowlist).absolute()))
    if (not isinstance(allow, list) or not allow or not all(isinstance(x, str) for x in allow)
            or len({x.casefold() for x in allow}) != len(allow)):
        raise ValueError("Allowlist must be a nonempty JSON array of unique exact relative file paths")
    indexed = {e["path"]: e for e in receipt["files"]}
    entries = []
    for path in allow:
        remote.deletion_allowed(args.subtree + "/" + path)
        if path not in indexed:
            raise ValueError("Allowlisted path absent from verified receipt: " + path)
        verify_local(args.subtree, indexed[path])
        entries.append(indexed[path])
    request = dict(base, action="delete", files=entries,
                   confirmation=args.confirm, source_quiescent=args.source_quiescent,
                   transaction=str(uuid.uuid4()), receipt_sha256=sha(receipt_path))
    write_json(folder / "deletion-plan.json", request)
    p, err, stem = session.start(request)
    complete = False
    try:
        with open(folder / "deletion-receipt.jsonl", "x", encoding="utf-8") as journal:
            for raw in p.stdout:
                value = json.loads(raw)
                journal.write(json.dumps(value, sort_keys=True) + "\n")
                journal.flush()
                os.fsync(journal.fileno())
                if value.get("state") == "complete":
                    complete = True
        session.finish(p, err, stem)
        if not complete:
            raise ValueError("Remote deletion completion record missing; inspect remote journal")
    except BaseException:
        session.abort(p, err, stem)
        raise
    return folder / "deletion-receipt.jsonl"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "pull", "delete"])
    parser.add_argument("--subtree", required=True, help="Nonempty output subtree relative to fixed NOTS C_ops root")
    parser.add_argument("--ssh-timeout", type=int, default=3600,
                        help="Hard wall-clock seconds per SSH operation (default 3600)")
    parser.add_argument("--reviewed-inspection", help="inspect.json whose remote instructions the operator has read")
    parser.add_argument("--receipt")
    parser.add_argument("--allowlist", help="JSON array of exact relative file paths; never glob/directory")
    parser.add_argument("--source-quiescent", action="store_true", help="Assert no producer can write/rename the output subtree")
    parser.add_argument("--confirm", choices=["DELETE_VERIFIED_OUTPUTS"])
    args = parser.parse_args()
    if args.ssh_timeout <= 0:
        parser.error("--ssh-timeout must be positive")
    remote.parts(args.subtree)
    if args.action != "inspect" and not args.reviewed_inspection:
        parser.error("inspect first, read all returned remote AGENTS.md instructions, then pass --reviewed-inspection")
    if args.action == "delete" and not (args.receipt and args.allowlist and args.source_quiescent and args.confirm):
        parser.error("delete requires --receipt, --allowlist, --source-quiescent, --confirm DELETE_VERIFIED_OUTPUTS")
    safe_local(DEST, create=True)
    with LocalLock():
        run(args)


def run(args):
    folder = DEST / ".transfer_audit" / (datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex)
    safe_local(folder, create=True)
    for filename in ("pull_outputs.py", "remote.py"):
        shutil.copyfile(HERE / filename, folder / filename)
    write_json(folder / "environment.json", {"utc": now(), "argv": sys.argv,
               "python": sys.version, "platform": platform.platform(), "host": platform.node(),
               "cwd": os.getcwd(), "source_sha256": {f: sha(HERE / f) for f in ("pull_outputs.py", "remote.py")}})
    session = Session(args, folder)
    base = {"subtree": args.subtree}
    print("Audit directory:", folder, flush=True)
    try:
        if args.action == "inspect":
            result = session.json(dict(base, action="inspect"))
            write_json(folder / "inspect.json", result)
            print(json.dumps(result, indent=2))
            output = folder / "inspect.json"
        else:
            inspection = load(safe_local(Path(args.reviewed_inspection).absolute()))
            if inspection["root"] != remote.ROOT or inspection["subtree"] != args.subtree:
                raise ValueError("Inspection applies to a different source")
            base["instructions"] = inspection["instructions"]
            write_json(folder / "reviewed-inspection.json", inspection)
            output = pull(session, args, base, folder) if args.action == "pull" else delete(session, args, base, folder)
        write_json(folder / "status.json", {"status": "success", "utc": now(), "output": str(output)})
        print("Saved:", output)
    except BaseException as exc:
        write_json(folder / "status.json", {"status": "failed", "utc": now(), "error": repr(exc)})
        print("FAILED:", exc, file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
