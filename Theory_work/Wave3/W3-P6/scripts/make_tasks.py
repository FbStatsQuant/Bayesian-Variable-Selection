"""W3-P6 task tables. Usage: python make_tasks.py GRID OUT_TSV  (GRID in GRIDS below).
Each line: task_id<TAB>command (run from the frozen scripts dir; $CODE, $OUT set by run_table.sh)."""
import sys

def cmd(design, n, p, s0, rep, arm="wide", rho=None, hours=22.5, mem_gb=12, savefull=0, tag=""):
    kv = [f"design={design}", f"n={n}", f"p={p}", f"s0={s0}", f"rep={rep}", f"arm={arm}", f"hours={hours}",
          f"mem_gb={mem_gb}", f"savefull={savefull}"]
    if rho is not None: kv.append(f"rho={rho}")
    if tag: kv.append(f"tag={tag}")
    return "Rscript --vanilla p6_fit.R $CODE/Scripts/SMC_BVS/core $OUT/raw/fits.jsonl $OUT/rds " + " ".join(kv)

def probe01():
    t = [cmd("cs", 40, 40, 4, 900, "wide", 0.5, savefull=1), cmd("cs", 40, 40, 4, 900, "mr1", 0.5, savefull=1)]
    for n in (50, 100, 150, 200):
        for r in (1, 2.5, 5, 10):
            t.append(cmd("cs", n, int(round(r * n)), 4, 901, "wide", 0.5))
    t += [cmd("cs", 50, 2500, 4, 901, "wide", 0.5), cmd("cs", 100, 5000, 4, 901, "wide", 0.5),
          cmd("fac2", 100, 250, 4, 901), cmd("s5", 100, 250, 4, 901), cmd("cs", 100, 250, 8, 901, "wide", 0.5),
          cmd("cs", 50, 50, 4, 901, "mr1", 0.5), cmd("cs", 50, 125, 4, 901, "mr1", 0.5)]
    return t

VARIANTS = [("cs", 0.3, 4), ("cs", 0.7, 4), ("fac2", None, 4), ("s5", None, 4), ("cs", 0.5, 8)]

def cells_A1(ns, ratios):
    return [("cs", 0.5, 4, n, int(round(r * n))) for n in ns for r in ratios]

def cells_A2(ns, ratios):
    return [(d, rho, s0, n, int(round(r * n))) for n in ns for r in ratios for (d, rho, s0) in VARIANTS]

def expand(cells, reps, arm="wide"):
    return [cmd(d, n, p, s0, rep, arm, rho) for (d, rho, s0, n, p) in cells for rep in reps]

def b1():
    reps = range(1, 21)
    t = expand(cells_A1([50], (1, 2.5, 5, 10)), reps) + expand(cells_A2([50], (1, 5)), reps)
    t += expand([("cs", 0.5, 4, 50, 50), ("cs", 0.5, 4, 50, 125)], reps, "mr1")
    return t

def b2():
    reps = range(1, 21)
    long_first = [("cs", 0.5, 4, 100, 1000), ("cs", 0.5, 4, 150, 150), ("cs", 0.5, 4, 75, 750), ("cs", 0.5, 4, 100, 250)]
    long_first += [(d, rho, s0, 100, 250) for (d, rho, s0) in VARIANTS]
    short = [("cs", 0.5, 4, 100, 100), ("cs", 0.5, 4, 75, 188), ("cs", 0.5, 4, 75, 75)]
    return expand(long_first + short, reps)

GRIDS = {"probe01": probe01, "b1": b1, "b2": b2}

def data_seed(design, n, p, s0, rep, rho):
    dcode = ["cs", "fac2", "s5"].index(design) + 1
    rho = rho if rho is not None else 0.0
    return int((7919 * rep + 13 * n + p + 1000003 * dcode + 50021 * s0 + 7 * round(1000 * rho)) % (2**31 - 4 * 10**6 - 2))

if __name__ == "__main__":
    rows = GRIDS[sys.argv[1]]()
    seen = {}
    for c in rows:
        kv = dict(x.split("=", 1) for x in c.split() if "=" in x and not x.startswith("$"))
        rho = float(kv["rho"]) if "rho" in kv else None
        k = (kv["design"], int(kv["n"]), int(kv["p"]), int(kv["s0"]), int(kv["rep"]), rho)
        sd = data_seed(*k)
        if sd in seen and seen[sd] != k: raise SystemExit(f"seed collision {k} {seen[sd]}")
        seen[sd] = k
    with open(sys.argv[2], "w", newline="\n") as f:
        for i, c in enumerate(rows, 1):
            f.write(f"{i}\t{c}\n")
    print(len(rows), "tasks")
