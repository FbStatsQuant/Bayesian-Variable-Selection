"""Generate PKA task tables (task_id<TAB>command).  Usage: python make_tasks.py BATCH OUT_TSV
Each task writes its own files under $OUT/raw/ (no shared appends)."""
import sys, math

batch, out = sys.argv[1], sys.argv[2]
PY = "TICKETS=/home/fb31/projects/BVS/theory_w2/code/tickets_20261109T1105_pka python3 -B"
rows = []


def p1(n, c, rho, lo, hi):
    tag = f"p1_n{n}_c{int(round(c * 100))}_r{int(round(rho * 10))}_{lo:03d}-{hi:03d}"
    rows.append(f"{PY} p1_run.py {n} {c} {rho} {lo} {hi} $OUT/raw/{tag}.jsonl $OUT/raw/{tag}.raw.jsonl.gz")


def p2(v, n, c, lo, hi, mode):
    tag = f"p2_{v}_n{n}_c{int(round(c * 100))}_{mode}_{lo:03d}-{hi:03d}"
    rows.append(f"{PY} p2_run.py {v} {n} {c} {lo} {hi} {mode} $OUT/raw/{tag}.jsonl $OUT/raw/{tag}.raw.jsonl.gz")


def chunks(lo, hi, size):
    return [(a, min(a + size, hi)) for a in range(lo, hi, size)]


C = (.6, .85, .98)
if batch == "val":
    for part in ("v1", "v2", "v4"):
        rows.append(f"{PY} validate.py $OUT/raw/validation_{part}.json {part}")
    for part in ("v3b", "v5", "v6"):
        rows.append(f"{PY} validate_path.py $OUT/raw/validation_{part}.json {part}")
elif batch == "pilot":          # P1 rho=.5 20 seeds n<=6400, 5 seeds at 12800/25600; P2 small
    for n in (800, 1600, 3200, 6400):
        for c in C:
            p1(n, c, .5, 0, 20)
    for n in (12800, 25600):
        for c in C:
            p1(n, c, .5, 0, 5)
    for v in ("v1", "v2", "v3"):
        for c in C:
            p2(v, 1000, c, 0, 20, "full")
            p2(v, 10000, c, 0, 20, "full")
            p2(v, 100000, c, 0, 2, "early")
elif batch == "main_a":         # n-growth first: P1 rho=.5 reps 20..99 for n<=25600 (+ 5..19 at 12800/25600)
    for n in (800, 1600, 3200):
        for c in C:
            p1(n, c, .5, 20, 100)
    for c in C:
        for a, b in chunks(20, 100, 40):
            p1(6400, c, .5, a, b)
        for a, b in chunks(5, 100, 10):
            p1(12800, c, .5, a, b)
        for a, b in chunks(5, 100, 3):
            p1(25600, c, .5, a, b)
elif batch == "main_b":         # P1 n=51200, 20 seeds, one seed per task
    for c in C:
        for r in range(20):
            p1(51200, c, .5, r, r + 1)
elif batch == "sens":           # P1 rho=.2,.8 20 seeds, n<=25600
    for rho in (.2, .8):
        for n in (800, 1600, 3200, 6400):
            for c in C:
                p1(n, c, rho, 0, 20)
        for c in C:
            for a, b in chunks(0, 20, 5):
                p1(12800, c, rho, a, b)
            for a, b in chunks(0, 20, 2):
                p1(25600, c, rho, a, b)
elif batch == "p2main":         # P2 20 seeds: full n in {3162, 31623, 100000}, early n in {316228, 1000000}
    for v in ("v1", "v3", "v2"):
        for c in C:
            p2(v, 3162, c, 0, 20, "full")
            for a, b in chunks(0, 20, 5):
                p2(v, 31623, c, a, b, "full")
            for r in range(20):
                p2(v, 100000, c, r, r + 1, "full")
            for a, b in chunks(0, 20, 4):
                p2(v, 316228, c, a, b, "early")
            for r in range(20):
                p2(v, 1000000, c, r, r + 1, "early")
else:
    raise SystemExit("unknown batch")
with open(out, "w", newline="\n") as f:
    for i, r in enumerate(rows, 1):
        f.write(f"{i}\t{r}\n")
print(batch, len(rows), "tasks ->", out)
