"""BENCH-FIX freeze: write code/bench_v2/MANIFEST_SHA256.txt over the three method trees and
print the manifest digest and the F3 runner source tree digest (same formula as run_case.R
source_hashes() and bench_audit/jobs/BENCH_F3_PROD/runner/frozen.py). Refuses to overwrite."""
import hashlib
from pathlib import Path
import sys

ROOT = Path("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/"
            "I_2026-10-28_New_Campaign/code/bench_v2")
TREES = ("F1_Lasso", "F2_ElasticNet", "F3_AdaptiveLasso")
F3_CODE = ("config.R", "common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R", "run_case.R")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out = ROOT / "MANIFEST_SHA256.txt"
    if out.exists():
        sys.exit("MANIFEST_SHA256.txt already exists; refusing to overwrite")
    files = sorted(p for t in TREES for p in (ROOT / t).rglob("*") if p.is_file())
    if any(p.is_symlink() for t in TREES for p in (ROOT / t).rglob("*")):
        sys.exit("symlink in tree")
    lines = [f"{sha(p)}  {p.relative_to(ROOT).as_posix()}" for p in files]
    out.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    f3 = ROOT / "F3_AdaptiveLasso"
    text = "\n".join(f"{name}  {sha(f3 / name)}" for name in F3_CODE)
    print("files", len(lines))
    print("manifest_sha256", sha(out))
    print("f3_source_sha256", hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
