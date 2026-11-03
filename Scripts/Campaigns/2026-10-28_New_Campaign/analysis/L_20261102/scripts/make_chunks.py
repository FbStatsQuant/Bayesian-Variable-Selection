"""make_chunks.py MANIFEST OUTDIR CHUNK_SIZE : case ids = manifest dataset_id x (c100, c050), sorted; writes OUTDIR/chunk_XX.txt (one case id per line)."""
import csv, os, sys

man, out, size = sys.argv[1], sys.argv[2], int(sys.argv[3])
ds = sorted({r["dataset_id"] for r in csv.DictReader(open(man, encoding="utf-8"))})
cases = [f"{d}_{s}" for d in ds for s in ("c100", "c050")]
os.makedirs(out, exist_ok=True)
n = 0
for i in range(0, len(cases), size):
    with open(os.path.join(out, f"chunk_{i // size:02d}.txt"), "w", newline="\n") as f:
        f.write("\n".join(cases[i:i + size]) + "\n")
    n += 1
print(f"{len(ds)} datasets, {len(cases)} cases, {n} chunks")
