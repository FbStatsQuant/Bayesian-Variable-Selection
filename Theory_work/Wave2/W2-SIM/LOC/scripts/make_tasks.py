r"""make_tasks.py -- writes W2-SIM/LOC task tables (TSV: task_id <TAB> command) into ../configs/ (v2, after R01).
Usage: python make_tasks.py pilot | pilot2 | main | prod
main -> main_light.tsv (grouped: 10 seeds per task, commons 12 h, per-run LS0 guard 3000 s),
        main_heavy.tsv (one run per task, commons 24 h, per-run LS0 guard 70000 s),
        main_scheduled.txt (every scheduled spec = the denominator of every rate; R01-9).
prod -> prod_tasks.tsv (Q3; one fit per task) + prod_scheduled.txt.
Asserts: unique seed keys across all scheduled runs; expected counts."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(HERE, "..", "configs")
sys.path.insert(0, HERE)

TOEP = [("PT", a) for a in ("0.5", "0.8", "1.5", "2.5", "4", "6", "8.5", "10")] + [("AF", d) for d in ("0.1", "0.25", "0.4")]
LONG = {("PT", "0.5"), ("PT", "0.8"), ("AF", "0.1"), ("AF", "0.25"), ("AF", "0.4")}
CSG_ARMS = ("one", "one4", "two", "twoM")
SEEDS = range(1, 11)
NQ = (500, 1000, 2000, 4000, 8000, 16000)
NS = (500, 1000, 2000, 4000, 8000, 16000, 32000, 64000)
NC = (500, 1000, 2000, 4000, 8000, 16000, 32000)


def port(specs, tmax):
    return f"python3 loc_batch.py $OUT/raw/port {tmax} " + " ".join(specs)


def p_of(fam, par, n, prule):
    p = n // 4 if prule == "q" else int(round(n ** 0.6))
    if fam == "CSG":
        g = math.ceil(n ** float(par.split(",")[0])); p = g * (p // g)
    return p


def seed_key(spec):
    import loc_run
    fam, par, place, n, prule, seed = spec.split(":")
    pp = loc_run.parse_par(fam, par)
    pv = [int(round(1000 * x)) for x in (pp if isinstance(pp, tuple) else (pp,))]
    return tuple([loc_run.FAMC[fam]] + pv + [loc_run.PLC[place], int(n), p_of(fam, par, int(n), prule), int(seed)])


def prod_cmd(cid, fam, par, place, n, prule, seed, mem_gb, hours=1e7):
    p = p_of(fam, par, n, prule)
    ident = f"{cid}_n{n}_s{seed}"
    seedoff = 100003 * int(cid[1:])
    return (f"mkdir -p $OUT/data $OUT/raw/prodport && LOC_EXPORT=$OUT/data/{ident} python3 loc_run.py $OUT/raw/prodport/{ident}.json "
            f"{fam} {par} {place} {n} {prule} {seed} && Rscript --vanilla loc_prod_fit.R $CODE/Scripts/SMC_BVS/core "
            f"$OUT/raw/prod_{ident}.jsonl $OUT/rds design=file dfile=$OUT/data/{ident} n={n} p={p} rep={seed} seedoff={seedoff} "
            f"hours={hours:g} mem_gb={mem_gb} tag=_{ident}; rc=$?; "
            f"Rscript --vanilla loc_prod_extract.R $OUT/rds/file_n{n}_p{p}_r{seed:03d}_mr1_{ident}.rds $OUT/raw/prodx_{ident}.json; rx=$?; "
            f"rm -f $OUT/data/{ident}.X.bin $OUT/data/{ident}.y.bin; exit $(( rc != 0 ? rc : rx ))")


def write(name, cmds):
    fp = os.path.join(CFG, name)
    with open(fp, "w", newline="\n") as f:
        for i, c in enumerate(cmds, 1):
            f.write(f"{i}\t{c}\n")
    print(fp, len(cmds))


def write_list(name, items):
    with open(os.path.join(CFG, name), "w", newline="\n") as f:
        f.write("\n".join(items) + "\n")


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "main":
        heavy, light, sched = [], [], []
        for (fam, par) in TOEP:
            for place in ("spread", "adj"):
                for n in NQ:
                    sp = [f"{fam}:{par}:{place}:{n}:q:{s}" for s in SEEDS]
                    sched += sp
                    if ((fam, par) in LONG and n >= 8000) or n >= 16000:
                        heavy += [port([x], 70000) for x in sp]
                    else:
                        light.append(port(sp, 3000))
                for n in NS:
                    sp = [f"{fam}:{par}:{place}:{n}:s:{s}" for s in SEEDS]
                    sched += sp
                    light.append(port(sp, 3000))
        for b in ("0.2", "0.35", "0.5"):
            for rho in ("0.5", "0.8"):
                for place in CSG_ARMS:
                    for n in NC:
                        sp = [f"CSG:{b},{rho}:{place}:{n}:q:{s}" for s in SEEDS]
                        sched += sp
                        if n >= 16000:
                            heavy += [port([x], 70000) for x in sp]
                        else:
                            light.append(port(sp, 3000))
        keys = [seed_key(s) for s in sched]
        assert len(set(keys)) == len(keys), "seed keys not unique"
        assert len(sched) == 10 * (len(TOEP) * 2 * (len(NQ) + len(NS)) + 3 * 2 * len(CSG_ARMS) * len(NC))
        write("main_light.tsv", light); write("main_heavy.tsv", heavy); write_list("main_scheduled.txt", sched)
        print("scheduled runs", len(sched), "light tasks", len(light), "heavy tasks", len(heavy))
    elif which == "prod":
        cells = [("C1", "PT", "1.5", "spread"), ("C2", "AF", "0.25", "spread"), ("C3", "CSG", "0.5,0.8", "one"),
                 ("C4", "CSG", "0.5,0.8", "two"), ("C5", "PT", "0.5", "adj"), ("C6", "CSG", "0.5,0.8", "twoM")]
        cmds, sched = [], []
        for n in (8000, 2000, 500):                    # longest first
            for (cid, fam, par, place) in cells:
                for s in SEEDS:
                    cmds.append(prod_cmd(cid, fam, par, place, n, "q", 100 + s, 24 if n == 8000 else 12))
                    sched.append(f"{cid}:{fam}:{par}:{place}:{n}:q:{100 + s}")
        write("prod_tasks.tsv", cmds); write_list("prod_scheduled.txt", sched)
    else:
        raise SystemExit(f"unknown mode {which!r} (pilot tables were written by v1 of this script; see LOG.md)")
