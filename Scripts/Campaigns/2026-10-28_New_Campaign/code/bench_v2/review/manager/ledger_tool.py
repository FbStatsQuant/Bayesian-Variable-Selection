"""Verify or write a bundle ledger (sha256sum format, paths relative to the bundle folder).
usage: ledger_tool.py verify LEDGER
       ledger_tool.py write BUNDLE_DIR OUT_NAME [EXTRA_RELATIVE_PATH ...]
write: every file under BUNDLE_DIR except OUT_NAME, __pycache__/*.pyc and the archive_ledgers/ folder,
plus the EXTRA paths (relative to BUNDLE_DIR, e.g. ../BENCH_F3_PROD/runner/x.py). Refuses to overwrite."""
import hashlib
from pathlib import Path
import sys


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(ledger):
    base = ledger.parent
    bad = 0
    n = 0
    for line in ledger.read_text(encoding="utf-8").splitlines():
        h, rel = line.split("  ", 1)
        n += 1
        p = (base / rel)
        if not p.is_file():
            print("MISSING", rel); bad += 1
        elif sha(p) != h:
            print("MISMATCH", rel); bad += 1
    print(f"{ledger}: {n - bad}/{n} OK")
    return bad


def write(bundle, out_name, extras):
    out = bundle / out_name
    if out.exists():
        sys.exit("refusing to overwrite " + str(out))
    files = []
    for p in sorted(bundle.rglob("*")):
        rel = p.relative_to(bundle).as_posix()
        if not p.is_file() or rel == out_name or "__pycache__" in rel or rel.endswith(".pyc") \
                or rel.startswith("archive_ledgers/"):
            continue
        files.append((rel, p))
    for rel in extras:
        files.append((rel, (bundle / rel).resolve()))
    out.write_text("".join(f"{sha(p)}  {rel}\n" for rel, p in files), encoding="utf-8", newline="\n")
    print("entries", len(files))
    print("ledger_sha256", sha(out))


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(1 if verify(Path(sys.argv[2])) else 0)
    write(Path(sys.argv[2]), sys.argv[3], sys.argv[4:])
