r"""build_summary.py -- writes SUMMARY_SHARPNESS.md PROGRAMMATICALLY from the four raw CSVs (v1_results.csv, l1_results.csv,
l2_results.csv, n1_results.csv).  No number in the summary is typed by hand; the fixed text blocks contain only definitions and
design deviations.  Run:  py -3.13 build_summary.py
`conclusion held` (for V, L, N-chi, L-gain rows) := LS0 started from the coded start mode, with the SHIPPED cap ell_cap(n,p)+|start|
and complete scans, ends exactly at S0 AND its last scan found no strict improvement ("certified")  [event K_n of RM-0(a)].
Counts are runs, k/N.  No interpretation beyond the counts; no asymptotic claim."""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rm_common import load_csv, cnt, HERE


def P(path):
    return os.path.join(HERE, path)


def held(r):
    return r["ls_final_eq_S0"] and r["ls_certified"]


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def comp(r, key):
    return json.loads(r[key])


L = []
A = L.append
A("# SUMMARY_SHARPNESS -- W3-RM boundary-violation numerics (V1, L1, L2, N1)")
A("")
A("**Generated programmatically by `build_summary.py` from the raw CSVs listed with each table; every number below comes from a CSV "
  "written by the named script.  Falsification / sharpness probes: observations only, never proofs; all theorems are asymptotic; "
  "no claim about asymptotics is made.**  Python: `py -3.13` (numpy 2.3.0, scipy 1.15.3; the `python` on PATH is 3.15 without numpy).")
A("")
A("Common pipeline (`rm_common.py`, importing the port `Theory_work/Wave1C/C-GROW/numerics/bvs_core.py`): sigma = 1, columns centred/"
  "standardised, y via `make_y_std`; start mode `bc.start_mode` (tie tolerance 1e-12, enumeration cap 20000); LS0 = `bc.local_search` "
  "with COMPLETE scans, shipped cap ell_cap(n,p)+|start| (the 'old cap' ell_cap(n,p) result is derived exactly from the same "
  "deterministic path). Definitions (move types, endpoint, certified, S0 scored, S0_is_max): `rm_common.py` docstring; design and "
  "per-column definitions: docstring of each script.")
A("`conclusion held` := LS0 from the start mode (shipped cap) ends at S0 and the last complete scan finds no strict improvement.")
A("")

# ----------------------------------------------------------------- start-mode truncation
trunc_all = []
for nm in ("v1_results.csv", "l1_results.csv", "l2_results.csv", "n1_results.csv"):
    if os.path.exists(P(nm)):
        rr = load_csv(P(nm))
        trunc_all.append((nm, cnt(rr, lambda r: r["start_trunc"]), max(r["start_nopt"] for r in rr)))
A("## 0. Start-mode tie enumeration (port `start_mode`: tie tolerance 1e-12, `enum_cap` = 20000)")
A("")
A(table(["CSV", "runs with start_mode truncated (info.truncated)", "max info.n_optimal over runs"], trunc_all))
A("")

# ----------------------------------------------------------------- V1
if os.path.exists(P("v1_results.csv")):
    R = load_csv(P("v1_results.csv"))
    A("## 1. V1 -- visibility violated (truth j masked inside its block)")
    A("")
    A("Script `v1_masked.py`, CSV `v1_results.csv` (runs: %d).  Cells: V1a (15 decoys per truth; p=200 has B=14 < 16 so groups cannot fit "
      "one block), V1a13 (variant: 13 decoys per truth, p=200 only: group size 14 = B), V1b (no decoys).  Column definitions in the script "
      "docstring.  `j,k same block` = realised blocks of j and k coincide; `block(j) holds k or k-decoys` = number of runs in which j's "
      "realised block contains k or a decoy of k; `min|cov_j| noK` = maximum over runs of the min over U subset block(j)\\{j,k} of "
      "|Cov(W_j, m | W_U)| (all-U minimum is exactly 0 at U = empty in every run, so (V) and (V_b) fail in every run by construction; "
      "see the script docstring); `masked U frac` = mean over runs of the fraction of U subset block(j)\\{j} with |Cov| < 1e-9." % len(R))
    A("")
    keys = sorted({(r["cell"], int(r["p"]), int(r["n"])) for r in R})
    rows = []
    for k in keys:
        rr = [r for r in R if (r["cell"], int(r["p"]), int(r["n"])) == k]
        kdec = sum(1 for r in rr if (comp(r, "blk_j_composition").get("k", 0) + comp(r, "blk_j_composition").get("dK", 0)) > 0)
        ent = {e: sum(1 for r in rr if r["j_entry"] == e) for e in ("in_start", "add", "swap", "never")}
        rows.append([k[0], k[1], k[2], len(rr), cnt(rr, lambda r: r["same_block_jk"]), kdec,
                     "%d-%d" % (min(r["blk_j_size"] for r in rr), max(r["blk_j_size"] for r in rr)),
                     cnt(rr, lambda r: r["j_in_start"]), cnt(rr, lambda r: r["k_in_start"]), cnt(rr, lambda r: r["S0_in_start"]),
                     "%d/%d/%d/%d" % (ent["in_start"], ent["add"], ent["swap"], ent["never"]),
                     cnt(rr, held), cnt(rr, lambda r: r["ls_final_eq_S0"] and r["j_entry"] == "add"),
                     cnt(rr, lambda r: r["ls_old_final_eq_S0"]), cnt(rr, lambda r: r["ls_S0_is_max"]),
                     "%.2g" % max(r["minabs_cov_j_noK"] for r in rr), "%.3f" % (sum(r["frac_masked_noK"] for r in rr) / len(rr)),
                     "%d" % max(r["n_extra"] for r in rr)])
    A(table(["cell", "p", "n", "runs", "j,k same block", "block(j) holds k or k-decoys", "block(j) size", "j in start", "k in start",
             "S0 in start", "j enters: in_start/add/swap/never", "conclusion held", "held AND j added by addition move",
             "old cap -> S0", "F(S0) max of scored", "max min|cov_j| noK", "masked U frac (noK)", "max |extras|"], rows))
    A("")
    for cell in ("V1a", "V1a13", "V1b"):
        rr = [r for r in R if r["cell"] == cell]
        A("- V1 / (V) cell %s: conclusion held in %s runs outside the assumption (all runs have min_U |Cov(W_j, m | W_U)| = 0 at U = empty)." % (cell, cnt(rr, held)))
    rr = R
    A("- V1 / (V), all cells pooled: conclusion held in %s runs outside the assumption." % cnt(rr, held))
    A("- V1a with intent achieved (j,k in different blocks AND block(j) holds neither k nor k-decoys): conclusion held in %s runs." % cnt(
        [r for r in R if r["cell"] in ("V1a", "V1a13") and (not r["same_block_jk"]) and
         (comp(r, "blk_j_composition").get("k", 0) + comp(r, "blk_j_composition").get("dK", 0)) == 0], held))
    A("")

# ----------------------------------------------------------------- L1
if os.path.exists(P("l1_results.csv")):
    R = load_csv(P("l1_results.csv"))
    A("## 2. L1 -- leakage far beyond log n (count of visible nulls = g - 1)")
    A("")
    A("Script `l1_groupsize.py`, CSV `l1_results.csv` (runs: %d).  `outside (N-chi)` := g-1 > log n (the number of visible nulls exceeds "
      "log n).  `all del` = LS0 shipped-cap path consists only of deletions of non-truths (and the run has >= 1 move or none needed)." % len(R))
    A("")
    rows = []
    for g in (8, 32, 128):
        for n in (400, 1600, 6400):
            rr = [r for r in R if int(r["g"]) == g and int(r["n"]) == n]
            if not rr:
                continue
            ex = sorted(r["n_extra"] for r in rr)
            rows.append([g, n, "%.2f" % math.log(n), "yes" if g - 1 > math.log(n) else "no", len(rr),
                         "%d-%d (median %d)" % (ex[0], ex[-1], ex[len(ex) // 2]), cnt(rr, lambda r: r["n_extra_le_logn"]),
                         cnt(rr, lambda r: r["n_extra_le_ell"]), cnt(rr, lambda r: r["S0_in_start"]),
                         cnt(rr, held), cnt(rr, lambda r: r["ls_old_final_eq_S0"] and r["ls_old_certified"]),
                         cnt(rr, lambda r: r["ls_all_del_extra"]), cnt(rr, lambda r: r["ls_S0_is_max"]),
                         max(r["ls_moves"] for r in rr)])
    A(table(["g", "n", "log n", "outside (N-chi)", "runs", "|S~\\S0| range", "|S~\\S0| <= log n", "|S~\\S0| <= ell_cap", "S0 in start",
             "held (shipped cap)", "held (old cap)", "all moves = del of extra", "F(S0) max of scored", "max moves"], rows))
    A("")
    out = [r for r in R if int(r["g"]) - 1 > math.log(int(r["n"]))]
    A("- L1 / (N-chi), runs with g-1 > log n: conclusion held in %s runs outside the assumption (shipped cap); with the OLD cap in %s." % (
        cnt(out, held), cnt(out, lambda r: r["ls_old_final_eq_S0"] and r["ls_old_certified"])))
    A("- L1, all runs: conclusion held in %s runs (shipped cap)." % cnt(R, held))
    A("")

# ----------------------------------------------------------------- L2
if os.path.exists(P("l2_results.csv")):
    R = load_csv(P("l2_results.csv"))
    A("## 3. L2 -- population proxy strength n r^2 = eta log n (exploratory; NOT a certified violation of (L-gain))")
    A("")
    A("Script `l2_eta.py`, CSV `l2_results.csv` (runs: %d).  EVERY non-truth column is a proxy with n r^2 = eta log n.  `proxies in start` = "
      "|S~ \\ {j}| (the sandwich S0 <= S~ <= Q with Q = S0 fails iff > 0).  **What eta is and is not (council C1, seat A, finding 1):** eta is the "
      "NOMINAL POPULATION proxy strength (rows are Gaussian; r is the population correlation of every non-truth column with the truth).  "
      "The column `eta_A` is the nominal cellwise value (sqrt(2A+1) - sqrt(2A))^2 with A := log p / log n of that cell (often below 1, "
      "whereas the theorems fix A >= 1, for which eta_A <= 0.1010).  The runs do NOT measure the fixed-design condition (L-gain) of "
      "STATEMENT v1.2 (realised delta^2_{U,l} <= eta tau_U^2 log n uniformly over l and |U| <= 15): the sample quantity was not stored, it "
      "fluctuates over the p columns, and with theta = sigma = 1 the residual-variance normalisation gives tau^2 = 2 at U = empty, so the "
      "nominal tau-normalised strength is eta/2.  Hence no run is certified to be inside or outside (L-gain); `eta > eta_A` below is a label "
      "of the nominal population strength only.  In Form R terms every eta > 0 sequence has n r^2 -> infinity and is outside the leak rate "
      "of (L-gain-R) asymptotically.  **Seeds: 20 per cell; 10 for eta = 2.0 with p = 200 and n >= 1600; the cells eta = 2.0, p = 400, "
      "n in {1600, 6400} were not run (see `nseeds_cell` in the script).**" % len(R))
    A("")
    rows = []
    keys = sorted({(r["eta_label"], int(r["p"]), int(r["n"])) for r in R},
                  key=lambda k: (["0", "0.5etaA", "2etaA", "0.5", "1.0", "2.0"].index(
                      {0.0: "0", 0.5: "0.5", 1.0: "1.0", 2.0: "2.0"}.get(k[0], k[0]) if not isinstance(k[0], str) else k[0]), k[1], k[2]))
    # (lead's fix: load_csv turns the numeric labels "0", "0.5", "1.0", "2.0" into floats)
    for k in keys:
        rr = [r for r in R if (r["eta_label"], int(r["p"]), int(r["n"])) == k]
        ex = sorted(r["n_extra"] for r in rr)
        rows.append([k[0], "%.4f" % rr[0]["eta"], "%.4f" % rr[0]["eta_A"], k[1], k[2], len(rr), "%.2f" % rr[0]["n_r2"],
                     cnt(rr, lambda r: r["n_proxy_in_start"] > 0), "%d-%d (median %d)" % (ex[0], ex[-1], ex[len(ex) // 2]),
                     cnt(rr, lambda r: r["j_in_start"]), cnt(rr, held), cnt(rr, lambda r: r["ls_old_final_eq_S0"] and r["ls_old_certified"]),
                     cnt(rr, lambda r: r["ls_all_del_extra"]), cnt(rr, lambda r: r["ls_S0_is_max"]),
                     "%d-%d" % (min(r["ls_moves"] for r in rr), max(r["ls_moves"] for r in rr))])
    A(table(["eta label", "eta", "eta_A", "p", "n", "runs", "n r^2", "start has a proxy (sandwich fails)", "proxies in start",
             "j in start", "held (shipped cap)", "held (old cap)", "all moves = del of extra", "F(S0) max of scored", "moves"], rows))
    A("")
    outL = [r for r in R if r["eta"] > r["eta_A"]]
    inL = [r for r in R if r["eta"] <= r["eta_A"]]
    A("- L2, runs with nominal eta > nominal eta_A (population strength; not a certified violation of (L-gain)): conclusion held in %s runs (shipped cap); old cap: %s." % (
        cnt(outL, held), cnt(outL, lambda r: r["ls_old_final_eq_S0"] and r["ls_old_certified"])))
    A("- L2, runs with nominal eta <= nominal eta_A (eta = 0, 0.5 eta_A): conclusion held in %s runs." % cnt(inL, held))
    A("- L2, runs with nominal eta > nominal eta_A and a proxy in the start mode (sandwich with Q = S0 fails): conclusion held in %s." % cnt(
        [r for r in outL if r["n_proxy_in_start"] > 0], held))
    A("")

# ----------------------------------------------------------------- N1
if os.path.exists(P("n1_results.csv")):
    R = load_csv(P("n1_results.csv"))
    A("## 4. N1 -- the lattice condition (N): whole-lattice NA versus the greedy path")
    A("")
    A("Script `n1_lattice.py`, CSV `n1_results.csv` (runs: %d).  Exact-Gram design (`gram_err` max over runs: %.2e; min over runs of "
      "lam_min(Sigma): %.4g -- Sigma = V V' is positive definite in every run, so no sin(a) adjustment was needed).  "
      "`maxZ2 > c_n'` = lattice proxy of NA fails; `NA(F) fails` = some searched (T, l), l not in Q, has F(T u l) > F(T) by the port's F; "
      "`outside (N-chi)` := |Q \\ S0| = m > log n.  LS0 columns: from Q, from the 3 adversarial centres T_tau (A1-A3), and from the "
      "coded start mode; `->S0` = shipped-cap endpoint == S0; `del-only` = endpoint == S0 AND every move a deletion of a non-truth." % (
          len(R), max(r["gram_err"] for r in R), min(r["lam_min"] for r in R)))
    A("")
    rows = []
    keys = sorted({(float(r["C"]), int(r["n"])) for r in R})
    for k in keys:
        rr = [r for r in R if (float(r["C"]), int(r["n"])) == k]
        m = rr[0]["m"]

        def cs(pre, f):
            sub = [r for r in rr if (pre + "final_eq_S0") in r and r[pre + "final_eq_S0"] != ""]
            return cnt(sub, f(pre))

        rows.append([k[0], k[1], int(m), "yes" if m > math.log(k[1]) else "no", len(rr),
                     "%.1f" % max(r["maxZ2_adv"] for r in rr), "%.1f" % max(r["maxZ2_rand"] for r in rr), "%.1f" % rr[0]["cn"],
                     cnt(rr, lambda r: r["lat_fail"]), cnt(rr, lambda r: r["lat_fail_2logp"]),
                     "%.2f" % max(r["na_F_maxgain"] for r in rr), cnt(rr, lambda r: r["na_F_fail"]),
                     cs("Q_", lambda p_: (lambda r: r[p_ + "final_eq_S0"] and r[p_ + "certified"])),
                     cs("Q_", lambda p_: (lambda r: r[p_ + "reach_all_del"])),
                     cs("Q_", lambda p_: (lambda r: r[p_ + "old_final_eq_S0"])),
                     cs("A1_", lambda p_: (lambda r: r[p_ + "final_eq_S0"])), cs("A2_", lambda p_: (lambda r: r[p_ + "final_eq_S0"])),
                     cs("A3_", lambda p_: (lambda r: r[p_ + "final_eq_S0"])),
                     cs("A1_", lambda p_: (lambda r: r[p_ + "reach_all_del"])),
                     cs("st_", lambda p_: (lambda r: r[p_ + "final_eq_S0"] and r[p_ + "certified"])),
                     cnt(rr, lambda r: r["start_eq_S0"])])
    A(table(["C", "n", "m", "outside (N-chi)", "runs", "max Z2 adv", "max Z2 rand", "c_n'", "lattice proxy fails (Z2>c_n')", "Z2 > 2 log p",
             "max F-gain over searched (T,l)", "NA(F) fails", "Q->S0 (cert.)", "Q del-only", "Q->S0 (old cap)", "A1->S0", "A2->S0", "A3->S0",
             "A1 del-only", "start->S0 (cert.)", "start == S0"], rows))
    A("")
    out = [r for r in R if r["m"] > math.log(int(r["n"]))]
    A("- N1 / (N-chi), runs with m > log n: whole-lattice NA (F) conclusion held (NO searched (T,l) with F(T u l) > F(T)) in %s runs outside the assumption." % cnt(
        out, lambda r: not r["na_F_fail"]))
    A("- N1 / (N-chi), runs with m > log n: LS0 from centre Q ends at S0 in %s runs; with deletions only in %s; from the best adversarial centre A1 in %s." % (
        cnt(out, lambda r: r["Q_final_eq_S0"] and r["Q_certified"]), cnt(out, lambda r: r["Q_reach_all_del"]),
        cnt(out, lambda r: r["A1_final_eq_S0"] and r["A1_certified"])))
    A("- N1, runs with m > log n: conclusion held (LS0 from the start mode, shipped cap) in %s runs." % cnt(out, lambda r: r["st_final_eq_S0"] and r["st_certified"]))
    A("- N1 / (N-chi), runs with m <= log n (inside the assumption): NA(F) held in %s; Q->S0 in %s." % (
        cnt([r for r in R if r["m"] <= math.log(int(r["n"]))], lambda r: not r["na_F_fail"]),
        cnt([r for r in R if r["m"] <= math.log(int(r["n"]))], lambda r: r["Q_final_eq_S0"] and r["Q_certified"])))
    A("")

with open(P("SUMMARY_SHARPNESS_body.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("wrote SUMMARY_SHARPNESS_body.md")
