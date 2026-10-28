"""Linux-only SSH helper. No shell interpolation, extraction, or recursive deletion."""
import datetime
import hashlib
import json
import os
from pathlib import PurePosixPath
import platform
import stat
import struct
import sys

AREA = "/scratch/fb31/smcbvs_v3_deploy_20261022"
ROOT = AREA
DISK_CAP_BYTES = 20_000_000_000  # Conservative decimal 20 GB across all threads.
BLOCKED = {"code", "core", "source", "sources", "source_snapshots", "study",
           "inputs", "truth", "holdout", "bench20261019", "benchmarks",
           ".transfer_receipts", ".transfer_audit", "transfer", "runner", "verify",
           "a_build", "b_verify", "d_analysis", "data_audit", "review",
           "pilot_snapshots", "evidence", "config", "configs"}
DELETE_SUFFIXES = {".csv", ".tsv", ".rds", ".rdata", ".json", ".jsonl",
                   ".ndjson", ".log", ".out", ".err", ".png", ".pdf",
                   ".parquet", ".feather", ".arrow", ".fst", ".qs",
                   ".h5", ".hdf5", ".npy", ".npz"}
SOURCE_SUFFIXES = {".r", ".py", ".cpp", ".cc", ".c", ".h", ".hpp", ".sh",
                   ".ps1", ".bat", ".cmd", ".rmd", ".ipynb", ".so", ".o"}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def parts(path):
    if not isinstance(path, str) or not path or "\\" in path:
        raise ValueError("Expected nonempty POSIX relative path")
    p = PurePosixPath(path)
    raw = path.split("/")
    if p.is_absolute() or any(x in ("", ".", "..") for x in raw):
        raise ValueError("Absolute/ambiguous/traversal path rejected")
    for x in raw:
        tokens = x.lower().replace("-", "_").replace(".", "_").split("_")
        if (x.lower() in BLOCKED or {"truth", "holdout"}.intersection(tokens)
                or any(ord(c) < 32 for c in x)
                or ":" in x or x.endswith((".", " "))):
            raise ValueError("Protected/unsafe component: " + repr(x))
        stem = x.split(".")[0].rstrip(" .").upper()
        if stem in {"CON", "PRN", "AUX", "NUL"} or stem in {
                a + str(i) for a in ("COM", "LPT") for i in range(1, 10)}:
            raise ValueError("Windows reserved component")
        if any(c in x for c in '<>"|?*'):
            raise ValueError("Not a portable Windows path")
    return raw


def open_absolute_dir(path):
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for name in filter(None, path.strip("/").split("/")):
            nxt = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                          dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd
    except BaseException:
        os.close(fd)
        raise


def descend(fd, names):
    result = os.dup(fd)
    try:
        for name in names:
            nxt = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                          dir_fd=result)
            os.close(result)
            result = nxt
        return result
    except BaseException:
        os.close(result)
        raise


def identity(s):
    return {"size": s.st_size, "mtime_ns": s.st_mtime_ns,
            "ctime_ns": s.st_ctime_ns, "dev": s.st_dev, "ino": s.st_ino,
            "mode": stat.S_IMODE(s.st_mode), "nlink": s.st_nlink}


def file_open(root, path):
    names = parts(path)
    parent = descend(root, names[:-1])
    try:
        fd = os.open(names[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                     dir_fd=parent)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            os.close(fd)
            raise ValueError("Nonregular file rejected: " + path)
        return fd
    finally:
        os.close(parent)


def digest_fd(fd):
    os.lseek(fd, 0, os.SEEK_SET)
    h = hashlib.sha256()
    while True:
        b = os.read(fd, 1024 * 1024)
        if not b:
            return h.hexdigest()
        h.update(b)


def file_info(root, path):
    fd = file_open(root, path)
    try:
        before = identity(os.fstat(fd))
        sha = digest_fd(fd)
        if before != identity(os.fstat(fd)):
            raise ValueError("File changed while hashing: " + path)
        return dict(path=path, sha256=sha, **before)
    finally:
        os.close(fd)


def require_same(root, entry):
    current = file_info(root, entry["path"])
    if current != entry:
        raise ValueError("Remote file changed: " + entry["path"])


def instructions(subtree):
    # Read ONLY applicable instruction files, never enumerate protected datasets.
    ancestors = ["/", "/scratch", "/scratch/fb31", ROOT]
    path = ROOT
    for component in parts(subtree):
        path += "/" + component
        ancestors.append(path)
    result = []
    for parent in ancestors:
        fd = open_absolute_dir(parent)
        try:
            try:
                f = os.open("AGENTS.md", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
            except FileNotFoundError:
                continue
            try:
                s = os.fstat(f)
                if not stat.S_ISREG(s.st_mode) or s.st_size > 1024 * 1024:
                    raise ValueError("Unsafe or oversized AGENTS.md")
                with os.fdopen(f, "rb", closefd=False) as stream:
                    data = stream.read(1024 * 1024 + 1)
                result.append({"path": parent.rstrip("/") + "/AGENTS.md",
                               "sha256": hashlib.sha256(data).hexdigest(),
                               "text": data.decode("utf-8")})
            finally:
                os.close(f)
        finally:
            os.close(fd)
    # Nested instructions also govern files that the recursive pull may visit.
    target = open_absolute_dir(ROOT + "/" + subtree)
    def nested(fd, prefix):
        for name in sorted(os.listdir(fd)):
            parts(name)
            s = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISLNK(s.st_mode):
                raise ValueError("Symlink rejected while discovering instructions")
            if not stat.S_ISDIR(s.st_mode):
                continue
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=fd)
            try:
                try:
                    instruction = os.open("AGENTS.md", os.O_RDONLY | os.O_NOFOLLOW,
                                          dir_fd=child)
                except FileNotFoundError:
                    instruction = None
                if instruction is not None:
                    try:
                        s = os.fstat(instruction)
                        if not stat.S_ISREG(s.st_mode) or s.st_size > 1024 * 1024:
                            raise ValueError("Unsafe/oversized nested instruction file")
                        with os.fdopen(instruction, "rb", closefd=False) as stream:
                            data = stream.read(1024 * 1024 + 1)
                        result.append({"path": prefix + "/" + name + "/AGENTS.md",
                                       "sha256": hashlib.sha256(data).hexdigest(),
                                       "text": data.decode("utf-8")})
                    finally:
                        os.close(instruction)
                nested(child, prefix + "/" + name)
            finally:
                os.close(child)
    try:
        nested(target, ROOT + "/" + subtree)
    finally:
        os.close(target)
    return result


def inventory(fd, prefix=""):
    result = []
    for name in sorted(os.listdir(fd)):
        path = prefix + name
        parts(path)  # Reject the entire inventory if any unsafe/protected entry exists.
        s = os.stat(name, dir_fd=fd, follow_symlinks=False)
        if stat.S_ISDIR(s.st_mode):
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=fd)
            try:
                for entry in inventory(child):
                    entry["path"] = path + "/" + entry["path"]
                    result.append(entry)
            finally:
                os.close(child)
        elif stat.S_ISREG(s.st_mode):
            result.append(file_info(fd, name))
        else:
            raise ValueError("Symlink/special file rejected: " + path)
    return result


def frame(value):
    b = json.dumps(value, sort_keys=True).encode("utf-8")
    sys.stdout.buffer.write(struct.pack(">Q", len(b)))
    sys.stdout.buffer.write(b)
    sys.stdout.buffer.flush()


def emit(value):
    print(json.dumps(value, sort_keys=True), flush=True)


def deletion_allowed(path):
    names = parts(path)
    if any(name.lower() in {"manifest", "manifests", "log", "logs", "audit",
                            "receipts", "metadata", "provenance", "seeds"}
           for name in names):
        raise ValueError("Manifest/log/audit directories must be retained")
    basename = names[-1].lower()
    tokens = basename.replace("-", "_").replace(".", "_").split("_")
    if any(token.startswith(("manifest", "receipt", "provenance", "environment",
                             "config", "instruction", "seed", "agents", "status",
                             "metadata", "launch", "command"))
           for token in tokens):
        raise ValueError("Audit/configuration/seed metadata must be retained")
    suffixes = [x.lower() for x in PurePosixPath(names[-1]).suffixes]
    if any(x in {".log", ".out", ".err", ".jsonl", ".ndjson"} for x in suffixes):
        raise ValueError("Logs and event journals must be retained")
    if any(x in SOURCE_SUFFIXES for x in suffixes):
        raise ValueError("Source file deletion forbidden")
    if suffixes and suffixes[-1] in (".gz", ".bz2", ".xz", ".zst"):
        suffixes.pop()
    if not suffixes or suffixes[-1] not in DELETE_SUFFIXES:
        raise ValueError("Deletion extension is not an approved output format")


def disk_usage():
    """Metadata only: account for ALL deployment threads, never read file contents.

    Count both apparent and allocated bytes conservatively (including hardlinks).
    Count symlink inode bytes without following; refuse other special files.
    Truth/holdout trees are forbidden even for this inventory.
    """
    fd = open_absolute_dir(AREA)
    def visit(directory):
        apparent, allocated = 0, 0
        for name in os.listdir(directory):
            tokens = name.lower().replace("-", "_").replace(".", "_").split("_")
            if {"truth", "holdout"}.intersection(tokens):
                raise ValueError("Truth/holdout found in deployment area; refusing traversal")
            info = os.stat(name, dir_fd=directory, follow_symlinks=False)
            apparent += info.st_size
            allocated += info.st_blocks * 512
            if stat.S_ISDIR(info.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=directory)
                try:
                    a, b = visit(child)
                    apparent += a
                    allocated += b
                finally:
                    os.close(child)
            elif not (stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)):
                raise ValueError("Symlink/special file found in deployment disk inventory")
        return apparent, allocated
    try:
        apparent, allocated = visit(fd)
        top = os.fstat(fd)
        apparent += top.st_size
        allocated += top.st_blocks * 512
    finally:
        os.close(fd)
    return {"area": AREA, "cap_bytes": DISK_CAP_BYTES,
            "apparent_bytes": apparent, "allocated_bytes": allocated,
            "within_cap": max(apparent, allocated) <= DISK_CAP_BYTES,
            "utc": now()}


def runtime_context():
    priority = os.getpriority(os.PRIO_PROCESS, 0)
    if priority != 19:
        raise ValueError("Remote helper must run at nice 19")
    return {"nice": priority, "pid": os.getpid(),
            "utc": now(), "host": platform.node(), "python": sys.version,
            "platform": platform.platform()}


def main(request):
    import fcntl  # Linux only; the laptop imports this module for path-policy functions.
    # The local lock prevents parallel SSH from this laptop. This NOTS advisory
    # lock also rejects another cooperating laptop/helper, without waiting.
    root = open_absolute_dir(ROOT)
    try:
        lock = os.open(".transfer.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW,
                       0o600, dir_fd=root)
        try:
            if not stat.S_ISREG(os.fstat(lock).st_mode) or os.fstat(lock).st_nlink != 1:
                raise ValueError("Unsafe transfer lock")
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            context = runtime_context()
            operation(request, context)
        finally:
            os.close(lock)
    finally:
        os.close(root)


def operation(request, context):
    subtree = request["subtree"]
    names = parts(subtree)
    root = open_absolute_dir(ROOT)
    target = descend(root, names)
    try:
        applicable = instructions(subtree)
        action = request["action"]
        if action == "inspect":
            emit({"root": ROOT, "subtree": subtree, "instructions": applicable,
                  "utc": now(), "host": platform.node(), "python": sys.version,
                  "platform": platform.platform(), "runtime": context})
            return
        if applicable != request["instructions"]:
            raise ValueError("Applicable remote instructions changed; inspect and review again")
        context["disk_usage"] = disk_usage()
        if not context["disk_usage"]["within_cap"]:
            # Allow verified evacuation/cleanup to recover from an existing breach.
            # This helper never uploads bulk data; only small audit journals grow.
            print("NOTS area exceeds 20 GB: stop producers and evacuate verified outputs",
                  file=sys.stderr, flush=True)
        if action == "manifest":
            emit({"root": ROOT, "subtree": subtree, "files": inventory(target),
                  "utc": now(), "host": platform.node(), "python": sys.version,
                  "platform": platform.platform(), "instructions": applicable, "runtime": context})
        elif action == "stream":
            frame({"runtime": context})
            for entry in request["files"]:
                require_same(target, entry)
                fd = file_open(target, entry["path"])
                try:
                    if identity(os.fstat(fd)) != {k: entry[k] for k in identity(os.fstat(fd))}:
                        raise ValueError("File replaced before streaming")
                    frame({"entry": entry})
                    remaining = entry["size"]
                    while remaining:
                        b = os.read(fd, min(1024 * 1024, remaining))
                        if not b:
                            raise ValueError("File truncated during streaming")
                        sys.stdout.buffer.write(b)
                        remaining -= len(b)
                    sys.stdout.buffer.flush()
                    require_same(target, entry)
                    frame({"verified": entry["path"]})
                finally:
                    os.close(fd)
            frame({"complete": True})
        elif action == "delete":
            if request.get("confirmation") != "DELETE_VERIFIED_OUTPUTS" or request.get("source_quiescent") is not True:
                raise ValueError("Explicit deletion confirmation and quiescence assertion required")
            entries = request["files"]
            if len({e["path"].casefold() for e in entries}) != len(entries) or not entries:
                raise ValueError("Empty/duplicate deletion allowlist")
            for entry in entries:
                # Retention rules apply from the fixed root, including --subtree.
                deletion_allowed(subtree + "/" + entry["path"])
                require_same(target, entry)
                if entry["nlink"] != 1:
                    raise ValueError("Hardlinked file deletion refused")
            transaction = request["transaction"]
            if not transaction or any(c not in "0123456789abcdef-" for c in transaction):
                raise ValueError("Unsafe transaction ID")
            try:
                os.mkdir(".transfer_receipts", mode=0o700, dir_fd=root)
                os.fsync(root)
            except FileExistsError:
                pass
            audit = descend(root, [".transfer_receipts"])
            try:
                journal = os.open(transaction + ".jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                  0o600, dir_fd=audit)
                os.fsync(audit)
                def record(value):
                    value["utc"] = now()
                    raw = (json.dumps(value, sort_keys=True) + "\n").encode()
                    with os.fdopen(os.dup(journal), "ab") as j:
                        j.write(raw)
                        j.flush()
                        os.fsync(j.fileno())
                    emit(value)
                try:
                    record({"state": "started", "subtree": subtree,
                            "receipt_sha256": request["receipt_sha256"],
                            "allowlist": entries, "host": platform.node(), "runtime": context})
                    for entry in entries:
                        require_same(target, entry)
                        parent = descend(target, parts(entry["path"])[:-1])
                        try:
                            # Resolve the same file through the held parent descriptor.
                            actual = file_info(parent, parts(entry["path"])[-1])
                            actual["path"] = entry["path"]
                            if actual != entry:
                                raise ValueError("File changed immediately before unlink")
                            if entry["nlink"] != 1:
                                raise ValueError("Hardlinked file deletion refused")
                            record({"state": "intent", "entry": entry})
                            os.unlink(parts(entry["path"])[-1], dir_fd=parent)
                            os.fsync(parent)
                            record({"state": "deleted", "entry": entry})
                        finally:
                            os.close(parent)
                    record({"state": "complete"})
                except BaseException as error:
                    record({"state": "failed", "error": repr(error)})
                    raise
                finally:
                    os.close(journal)
            finally:
                os.close(audit)
        else:
            raise ValueError("Unknown action")
    finally:
        os.close(target)
        os.close(root)


if __name__ == "__main__":
    try:
        main(json.load(sys.stdin))
    except BaseException as exc:
        print(repr(exc), file=sys.stderr, flush=True)
        sys.exit(1)
