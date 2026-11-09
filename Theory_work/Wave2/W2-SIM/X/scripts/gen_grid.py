"""gen_grid.py (v2, after X_R01) -- W2-SIM family X task tables.
Writes configs/<name>.tsv (task_id <TAB> command; one output file per task) and configs/<name>_cells.csv.
Usage: python gen_grid.py ITEM NAME [pmin pmax] [secs_per_path_at_p1000]
  ITEM = A  : iid CS frontier batch 1 (A_target grid, 20 seeds, start=both) for pmin <= p <= pmax
         A2 : iid CS batch 2, p in (pmin, pmax]: 10 seeds, both_seeds 0-2 (start mode + [p]), others [p] only
         B  : fixed-dispersion one-factor loadings (20 seeds; start=both for p <= 2000, else [p])
         BS : sensitivity set for B (X_R01 item 10): coef=rev for two-class designs, lseed 1, 2 for unif; p = 2000,
              n in {1e5, 1e6}, 10 seeds, start=full
         K  : k = 2, 3 factor designs (x_paths_k.py), REAL: real-data-like covariances (x_paths_k.py)"""
import sys, math, csv, os

here = os.path.dirname(os.path.abspath(__file__))
item, name = sys.argv[1], sys.argv[2]
pmin = int(sys.argv[3]) if len(sys.argv) > 3 else 10
pmax = int(sys.argv[4]) if len(sys.argv) > 4 else 4500
c1000 = float(sys.argv[5]) if len(sys.argv) > 5 else 16.6     # measured ~13-17 s per [p]-path at p = 1000 (x_pilot02)
TASK_BUDGET = 3 * 3600.0
DATADIR = "/scratch/fb31/theory_w2/fam_X/scripts/data"


def cost(p, start):
    path = c1000 * (p / 1000.0) ** 3 * 1.15 + 2.0          # +15% for the validation recomputations
    if start == "both":
        return 2.0 * path + 6.0 * (p / 1000.0) ** 3
    return path


cells = []
A_list = [0.3, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9]
n_list = [10 ** 3, 3 * 10 ** 3, 10 ** 4, 3 * 10 ** 4, 10 ** 5, 3 * 10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8]
if item in ("A", "A2"):
    for A in A_list:
        for n in n_list:
            p = min(int(round(n ** A)), n // 2)
            if p < pmin or p > pmax or (item == "A2" and p <= pmin):
                continue
            for rho in (0.3, 0.7):
                if item == "A":
                    cells.append(dict(script="x_paths.py", item="A", rho=rho, n=n, p=p, A=A, load="cs", seeds=list(range(20)),
                                      start="both", extra=f"A_target={A}"))
                else:
                    cells.append(dict(script="x_paths.py", item="A", rho=rho, n=n, p=p, A=A, load="cs", seeds=list(range(10)),
                                      start="full", extra=f"A_target={A} both_seeds=0-2"))
elif item == "B":
    for load in ("two03_09", "two05_095", "unif02_09"):
        for n in (10 ** 5, 10 ** 6):
            for p in (500, 2000, 5000):
                if pmin <= p <= pmax:
                    cells.append(dict(script="x_paths.py", item="B", rho=0.5, n=n, p=p, A=round(math.log(p) / math.log(n), 3),
                                      load=load, seeds=list(range(20)), start="both" if p <= 2000 else "full", extra=""))
elif item == "BS":
    for n in (10 ** 5, 10 ** 6):
        for load, ex in (("two03_09", "coef=rev"), ("two05_095", "coef=rev"), ("unif02_09", "lseed=1"), ("unif02_09", "lseed=2")):
            cells.append(dict(script="x_paths.py", item="B", rho=0.5, n=n, p=2000, A=round(math.log(2000) / math.log(n), 3),
                              load=load, seeds=list(range(10)), start="full", extra=ex))
elif item == "K":
    for load in ("k2blk", "k2glob", "k3glob", "k2gen", "k3gen"):
        for n, p in ((10 ** 4, 100), (10 ** 4, 1000), (10 ** 5, 300), (10 ** 5, 2000), (10 ** 6, 1000), (10 ** 6, 4000),
                     (10 ** 8, 300)):
            if pmin <= p <= pmax:
                cells.append(dict(script="x_paths_k.py", item="K", rho=None, n=n, p=p, A=round(math.log(p) / math.log(n), 3),
                                  load=load, seeds=list(range(20)), start="both", extra=""))
elif item == "REAL":
    for load, pd in (("real:riboflavin", 4088), ("real:fred_md", 99), ("real:fred_qd", 170)):
        for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8):
            for p in sorted({min(pd, 200), min(pd, 1000), pd}):
                if p > n // 2 or not (pmin <= p <= pmax):
                    continue
                cells.append(dict(script="x_paths_k.py", item="REAL", rho=None, n=n, p=p, A=round(math.log(p) / math.log(n), 3),
                                  load=load, seeds=list(range(20)), start="both", extra=f"datadir={DATADIR}"))
else:
    raise SystemExit("item")

tasks = []
for c in cells:
    st = "both" if c["start"] == "both" or "both_seeds" in c["extra"] else c["start"]
    per = cost(c["p"], c["start"]) if "both_seeds" not in c["extra"] else cost(c["p"], "full") * 1.6
    chunk = max(1, min(len(c["seeds"]), int(TASK_BUDGET // per)))
    for i in range(0, len(c["seeds"]), chunk):
        ss = c["seeds"][i:i + chunk]
        rng = f"{ss[0]}-{ss[-1]}" if len(ss) > 1 else f"{ss[0]}"
        tagx = c["extra"].replace("A_target=", "").replace(" both_seeds=0-2", "b").replace("datadir=" + DATADIR, "")
        tagx = tagx.replace("=", "").replace(" ", "")
        lname = c["load"].replace(":", "_")
        rho = f"_r{c['rho']}" if c["rho"] is not None else ""
        outn = f"$OUT/raw/{c['item']}_{lname}{rho}_n{c['n']}_p{c['p']}_{tagx}_s{rng}.jsonl"
        args = f"item={c['item']} rho={c['rho']} " if c["script"] == "x_paths.py" else ""
        cmd = (f"python3 -B {c['script']} {outn} {args}n={c['n']} p={c['p']} load={c['load']} seeds={rng} "
               f"start={c['start']} {c['extra']}").strip()
        tasks.append((per * len(ss), cmd))
tasks.sort(key=lambda t: -t[0])
outs = [t[1].split()[3] for t in tasks]
assert len(outs) == len(set(outs)), "duplicate output files"
os.makedirs(os.path.join(here, "..", "configs"), exist_ok=True)
with open(os.path.join(here, "..", "configs", name + ".tsv"), "w", newline="\n") as f:
    for i, (cst, cmd) in enumerate(tasks, 1):
        f.write(f"{i}\t{cmd}\n")
with open(os.path.join(here, "..", "configs", name + "_cells.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["script", "item", "rho", "n", "p", "A", "load", "start", "extra", "nseeds",
                                      "pred_cost_s_per_seed"])
    w.writeheader()
    for c in cells:
        w.writerow(dict(script=c["script"], item=c["item"], rho=c["rho"], n=c["n"], p=c["p"], A=c["A"], load=c["load"],
                        start=c["start"], extra=c["extra"], nseeds=len(c["seeds"]),
                        pred_cost_s_per_seed=round(cost(c["p"], c["start"]), 1)))
tot = sum(t[0] for t in tasks)
print(f"{name}: {len(cells)} cells, {len(tasks)} tasks, predicted {tot/3600:.1f} CPU-h, max task {tasks[0][0]/3600:.2f} h")
