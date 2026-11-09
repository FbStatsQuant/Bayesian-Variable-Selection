"""make_tasks.py -- W2-SIM family PK: write the Slurm task tables (task_id <TAB> command) of the production batches.
usage: python make_tasks.py CONFIG_DIR"""
import os
import sys

LAYS = ("aligned", "mixed")
REPS = range(10)


def write(path, cmds):
    with open(path, "w", newline="\n") as f:
        for i, c in enumerate(cmds, 1):
            f.write(f"{i}\t{c}\n")
    print(path, len(cmds))


def r3_cells():
    req = [(200, 500), (500, 1000), (1000, 2000), (2000, 1500)]                       # SIM_REQUEST R3
    item1 = [(n, int(r * n)) for n in (200, 400, 800) for r in (2.5, 5, 10)]          # p/n in {2.5,5,10}, n=200,400 (+800)
    trend = [(2000, 4000), (4000, 3000)]                                               # n-trend at p/n = 2 and 0.75
    cells = []
    for c in req + item1 + trend:
        if c not in cells:
            cells.append(c)
    return cells


def s5iid_cells():
    cells = [(n, int(r * n)) for n in (200, 400, 800) for r in (1, 2.5, 5, 10)]
    cells += [(1600, 1600), (1600, 4000)]
    return cells


def main():
    d = sys.argv[1]
    os.makedirs(d, exist_ok=True)
    # R3: iid-row CS rho = 0.5
    cmds = []
    for n, p in r3_cells():
        for lay in LAYS:
            for rep in REPS:
                cmds.append(f"python3 r3_iid.py $OUT/raw/R3_cs0.5_{n}_{p}_{lay}_{rep}.jsonl R3 cs0.5 {n} {p} {lay} {rep}")
    write(os.path.join(d, "pk_r3_tasks.tsv"), cmds)
    # R1: exact-Gram CS closed form
    cmds = []
    for n in (20000, 60000, 200000):
        for rho in (0.2, 0.5, 0.8):
            for frac in (0.6, 0.8, 0.99):
                for lay in LAYS:
                    for rep in REPS:
                        cmds.append(f"python3 r1_cs.py $OUT/raw/R1_{rho}_{n}_{frac}_{lay}_{rep}.jsonl {rho} {n} {frac} {lay} {rep}")
    write(os.path.join(d, "pk_r1_tasks.tsv"), cmds)
    # S5PK iid rows
    cmds = []
    for n, p in s5iid_cells():
        for lay in LAYS:
            for rep in REPS:
                cmds.append(f"python3 r3_iid.py $OUT/raw/S5iid_{n}_{p}_{lay}_{rep}.jsonl S5PK_iid s5 {n} {p} {lay} {rep}")
    write(os.path.join(d, "pk_s5iid_tasks.tsv"), cmds)
    # S5PK exact Gram
    cmds = []
    for n in (600, 2000, 4000):
        for frac in (0.6, 0.8, 0.99):
            for lay in LAYS:
                for rep in REPS:
                    cmds.append(f"python3 s5_exact.py $OUT/raw/S5ex_{n}_{frac}_{lay}_{rep}.jsonl {n} {frac} {lay} {rep}")
    write(os.path.join(d, "pk_s5ex_tasks.tsv"), cmds)


if __name__ == "__main__":
    main()
