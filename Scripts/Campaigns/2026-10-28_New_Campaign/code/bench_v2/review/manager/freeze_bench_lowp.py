"""BENCH-FIX freeze record for code/bench_lowp after the port: writes
code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256.txt (every file, relative paths). Refuses to overwrite."""
import hashlib
from pathlib import Path
import sys

CAMP = Path("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign")
TREE = CAMP / "code" / "bench_lowp"
SUFFIX = sys.argv[1] if len(sys.argv) > 1 else ""   # e.g. "_r2" for a documented revision
OUT = CAMP / "code" / "bench_v2" / "lowp_port" / f"BENCH_LOWP_MANIFEST_SHA256{SUFFIX}.txt"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


if OUT.exists():
    sys.exit("manifest exists; refusing to overwrite")
files = sorted(p for p in TREE.rglob("*") if p.is_file())
OUT.write_bytes(("\n".join(f"{sha(p)}  {p.relative_to(TREE).as_posix()}" for p in files) + "\n").encode("utf-8"))
print("files", len(files))
print("manifest_sha256", sha(OUT))
