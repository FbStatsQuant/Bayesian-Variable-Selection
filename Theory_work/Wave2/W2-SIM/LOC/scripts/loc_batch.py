r"""loc_batch.py -- run several loc_run.run() specs sequentially in one Slurm task (restartable: skips existing outputs).
Usage: python3 loc_batch.py OUTDIR TMAX_LS SPEC [SPEC ...], SPEC = fam:par:place:n:prule:seed (CSG par = b,rho).
Writes OUTDIR/<fam>_<par>_<place>_n<n>_<prule>_s<seed>.json; on exception writes the same name with .err."""
import sys, os, json, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loc_run

out, tmax = sys.argv[1], float(sys.argv[2])
os.makedirs(out, exist_ok=True)
for spec in sys.argv[3:]:
    fam, par, place, n, prule, seed = spec.split(":")
    name = f"{fam}_{par}_{place}_n{n}_{prule}_s{seed}"
    fp = os.path.join(out, name + ".json")
    if os.path.exists(fp):
        print("skip", name, flush=True); continue
    try:
        r = loc_run.run(fam, loc_run.parse_par(fam, par), place, int(n), prule, int(seed), tmax_ls=tmax)
        r["spec"] = spec
        tmp = fp + ".tmp"
        with open(tmp, "w") as f:
            json.dump(r, f, default=float); f.write("\n")
        os.replace(tmp, fp)
        print("done", name, r["mode_size"], r["n_extra"], r["ls_moves"], r["final_eq_S0"], r["t_total"], flush=True)
    except Exception:
        with open(os.path.join(out, name + ".err"), "w") as f:
            f.write(traceback.format_exc())
        print("ERR", name, flush=True)
