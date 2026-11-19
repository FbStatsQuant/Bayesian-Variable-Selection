#!/usr/bin/env python3
"""compare_overlap_v2.py -- 10^4 T-vs-V overlap rung: pre-registered comparison (OVERLAP_1e4_PREREG.md).

  v2 = compare_overlap.py (registered sha 311bbad8...) + ONE change, PREREG_ADDENDUM_1.md (pending HQ approval): a T fit's N check
  accepts the fit's own calibration N_final = N_plan * 4^tier_final (coded calibration escalates by tier, D-26; the registered check
  assumed tier 0).  tier_final / N_final are reported per fit (per_fit.csv, per_dataset.csv, verdict.json).  Nothing else differs.

Python 3 standard library only (numpy is NOT used).  READ-ONLY on the run directories.

  compare_overlap.py --records DIR [DIR ...] --out OUTDIR [--cost-dir DIR ...] [--cross-file F]
                     [--fitbin-dir DIR] [--expect-commit SHA] [--no-verify]
  compare_overlap.py --smoke --records DIR [...] [--fitbin-dir DIR] --out OUTDIR     (single-arm field check)

Reads every run dir  records/<batch>/<run_id>/  (a dir with run_manifest.json and/or eval.bin.json) for both arms,
checks the X/y sha pairing, computes every metric of the pre-registration and writes
OUTDIR/per_fit.csv, per_dataset.csv, verdict.json, verdict.md.   Every threshold lives in PREREG below.

Field map (INTERFACES v0.1.27 / README_WP5; verified on the 10^5 T5 and 10^6 F1M examples):
  eval.bin.json : selection.{hpm,mpm,F_hpm,hpm_size}, evidence.{logZ,logZ_T,logZ_r,R_eff,sigma_hat},
                  pip.eq.{n_null_gt_0.5,...}, dist.{H,M,T,oracle}.{plugin.h2, predictive.{h2,h2_se_x,h2_se_tail,kl}, test.{mlpd,mse}},
                  fit.meta.{N,Rp,mode,tier,flags,binary.{sha256,island_isa}}, status, fit_status, binary.sha256
  fit.bin       : sections pip_eq (= pip_primary), pip_T, pip_list (v0.1.27+), pip_r (Rp x p, row-major)   [p-wide: NOT in any JSON]
  truth.json    : X_sha256, y_sha256, S0, spec
  cost          : cost_<run_id>.json of p1m_cost.py (billed_core_h = sacct CPUTimeRAW/3600)
"""
import argparse
import array
import csv
import hashlib
import json
import math
import os
import re
import struct
import sys

# ----------------------------------------------------------------------------------------------------------------
# PRE-REGISTERED CONSTANTS (OVERLAP_1e4_PREREG.md).  A change after W0 is a logged deviation.
# ----------------------------------------------------------------------------------------------------------------
PREREG = {
    "schema": "overlap1e4.prereg/1",
    "grid": [["AR", 4], ["ARweak", 2], ["ADJOPP", 2], ["IND", 1], ["NULL", 1]],   # design token, reps (n = 200, p = 10^4)
    "seeds": [1, 2],
    "run_id_prefix": "4",
    "n_fits": 40,
    "arms": {
        "V": {"N": 2500, "Rp": 16, "mode": ["V"], "island_isa": "sapphirerapids", "cost_model_core_h": 10.0},
        "T": {"N": 10000, "Rp": 4, "mode": ["law", "T", "theory"], "cost_model_core_h": 115.0},
    },
    "cost_factor": 1.5,                 # per-fit limit = 1.5 x the arm's manifest cost model (V 15.0, T 172.5 core-h)
    "hpm_datasets_min": 9,              # HPM(V) = HPM(T) as sets in >= 9 of 10 datasets
    "F_tol": 1e-6,                      # T "higher F than V" only if F_T > F_V + F_tol (float noise guard)
    "pip_floor": 0.01,                  # max_j |PIP_V - PIP_T| <= max(0.01, 3 se)
    "z_mult": 3.0,                      # 3 combined s.e.
    "hell_frac": 0.10,                  # d_H(V,T) <= 10% of d_H(T, f*)
    "notclean_hpm_misses": 2,           # >= 2 HPM misses -> not clean
    "notclean_pred_misses": 2,          # predictive > 10% on >= 2 datasets -> not clean
    "pooled_seed_sd": True,             # s.e. yardstick pooled over datasets (2 seeds are unstable per dataset)
}

RUN_RE = re.compile(r"^(?P<pre>\d+)-(?P<design>[A-Za-z]+)-n(?P<n>\d+)-r(?P<rep>\d+)-(?P<arm>[TV])-s(?P<seed>\d+)$")
EVAL_NAMES = ("eval.bin.json", "eval.json")
FIT_JSON_NAMES = ("fit.bin.json", "fit.json")


# ----------------------------------------------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------------------------------------------
def jload(path):
    with open(path) as fh:
        return json.load(fh)


def first_json(d, names):
    for n in names:
        p = os.path.join(d, n)
        if os.path.isfile(p):
            return jload(p), p
    return None, None


def dig(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return default
    return d


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def sd(xs):
    xs = list(xs)
    if len(xs) < 2:
        return float("nan")
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def isnum(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def fmt(x, nd=4):
    if x is None:
        return "NA"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, float):
        if math.isnan(x):
            return "NA"
        return ("%." + str(nd) + "g") % x
    return str(x)


# ----------------------------------------------------------------------------------------------------------------
# engine container reader (INTERFACES 5.1): header 128 B | section table 128 B each | sections
# ----------------------------------------------------------------------------------------------------------------
def read_sections(path, names, verify=True):
    """Return {name: array/list/dict} for the requested sections that exist; raises ValueError on a corrupt file."""
    out = {}
    with open(path, "rb") as fh:
        h = fh.read(128)
        if len(h) < 128 or h[:8] != b"SMCBVS4\x00":
            raise ValueError("bad magic: %s" % path)
        kind, mode, ns = struct.unpack_from("<3I", h, 12)
        size = struct.unpack_from("<Q", h, 24)[0]
        if os.path.getsize(path) != size:
            raise ValueError("file size mismatch (truncated transfer?): %s" % path)
        tbl = fh.read(128 * ns)
        ent = {}
        for i in range(ns):
            o = 128 * i
            nm = tbl[o:o + 48].split(b"\0")[0].decode()
            dt, nd = struct.unpack_from("<II", tbl, o + 48)
            d0, d1, off, ln = struct.unpack_from("<4Q", tbl, o + 56)
            ent[nm] = (dt, nd, d0, d1, off, ln, tbl[o + 88:o + 120])
        for nm in names:
            if nm not in ent:
                continue
            dt, nd, d0, d1, off, ln, sha = ent[nm]
            fh.seek(off)
            b = fh.read(ln)
            if verify and hashlib.sha256(b).digest() != sha:
                raise ValueError("section hash mismatch: %s in %s" % (nm, path))
            if dt == 1:
                a = array.array("d")
                a.frombytes(b)
            elif dt == 2:
                a = array.array("i")
                a.frombytes(b)
            elif dt == 9:
                out[nm] = json.loads(b.decode())
                continue
            else:
                raise ValueError("dtype %d not supported (%s)" % (dt, nm))
            if sys.byteorder == "big":
                a.byteswap()
            out[nm] = (a, (d0, d1) if nd == 2 else (d0,))
    return out


# ----------------------------------------------------------------------------------------------------------------
# one run directory -> a parsed record
# ----------------------------------------------------------------------------------------------------------------
def find_runs(roots):
    runs = {}
    dups = []
    for root in roots:
        for dp, dns, fns in os.walk(root):
            if "run_manifest.json" in fns or any(n in fns for n in EVAL_NAMES):
                rid = None
                if "run_manifest.json" in fns:
                    try:
                        rid = jload(os.path.join(dp, "run_manifest.json")).get("run_id")
                    except Exception:
                        rid = None
                if not rid:
                    rid = os.path.basename(dp)
                if RUN_RE.match(rid or ""):
                    if rid in runs:
                        dups.append((rid, runs[rid], dp))
                        # the most recently written eval record wins (one infrastructure rerun is allowed)
                        def stamp(d):
                            ps = [os.path.join(d, n) for n in EVAL_NAMES if os.path.isfile(os.path.join(d, n))]
                            return max([os.path.getmtime(p) for p in ps] or [0])
                        if stamp(dp) > stamp(runs[rid]):
                            runs[rid] = dp
                    else:
                        runs[rid] = dp
                    dns[:] = []     # never descend into a run dir
    return runs, dups


def batch_name(rundir, rid):
    return os.path.basename(os.path.dirname(rundir)) if os.path.basename(rundir) == rid else os.path.basename(rundir)


def billed_core_h(obj):
    """Search a cost structure for billed_core_h (p1m_cost.py: cost_<run_id>.json, or eval.cost.<...>)."""
    if isinstance(obj, dict):
        if isnum(obj.get("billed_core_h")) and "stages" in obj:
            return float(obj["billed_core_h"])
        for k, v in obj.items():
            if k in ("sacct", "billed"):
                r = billed_core_h(v)
                if r is not None:
                    return r
        if isnum(obj.get("billed_core_h")):
            return float(obj["billed_core_h"])
    return None


def load_cost(rundir, rid, cost_dirs, ev):
    cands = [os.path.join(rundir, "cost_%s.json" % rid), os.path.join(rundir, "cost", "cost_%s.json" % rid),
             os.path.join(rundir, "cost.json")]
    cands += [os.path.join(cd, "cost_%s.json" % rid) for cd in cost_dirs]
    for c in cands:
        if os.path.isfile(c):
            try:
                v = billed_core_h(jload(c))
            except Exception:
                v = None
            if v is not None:
                return v, c
    v = billed_core_h(dig(ev or {}, "cost", default={}))
    return (v, "eval.cost") if v is not None else (None, None)


def parse_run(rid, rundir, opts):
    m = RUN_RE.match(rid)
    rec = {"run_id": rid, "dir": rundir, "arm": m["arm"], "seed": int(m["seed"]), "design": m["design"], "rep": int(m["rep"]),
           "n": int(m["n"]), "delivered": False, "reasons": [], "warnings": []}
    ev, evp = first_json(rundir, EVAL_NAMES)
    man = jload(os.path.join(rundir, "run_manifest.json")) if os.path.isfile(os.path.join(rundir, "run_manifest.json")) else {}
    tr = jload(os.path.join(rundir, "truth.json")) if os.path.isfile(os.path.join(rundir, "truth.json")) else {}
    rec["X_sha"], rec["y_sha"] = tr.get("X_sha256"), tr.get("y_sha256")
    rec["S0"] = tr.get("S0")
    rec["code_commit"] = man.get("code_commit")
    rec["p_nominal"] = dig(man, "params", "p") or dig(tr, "spec", "p")
    if ev is None:
        rec["reasons"].append("no eval.bin.json / eval.json")
        return rec
    fitjson, _ = first_json(rundir, FIT_JSON_NAMES)
    meta = dig(ev, "fit", "meta") or fitjson or {}
    rec["eval_status"], rec["fit_status"] = ev.get("status"), ev.get("fit_status")
    if ev.get("status") != "completed" or ev.get("fit_status") not in (None, "completed"):
        rec["reasons"].append("eval/fit status %r/%r" % (ev.get("status"), ev.get("fit_status")))
    if meta.get("status") not in (None, "completed") or meta.get("fit_state") not in (None, "completed"):
        rec["reasons"].append("fit meta status %r/%r" % (meta.get("status"), meta.get("fit_state")))
    # --- arm settings (README: V = N 2500, R' 16, class A; T = law, N 10^4, R' 4)
    spec = PREREG["arms"][rec["arm"]]
    N = meta.get("N", dig(man, "params", "N"))
    Rp = meta.get("Rp", dig(man, "params", "Rp"))
    mode = meta.get("mode", ev.get("mode"))
    isa = dig(meta, "binary", "island_isa") or meta.get("island_isa")
    rec.update({"N": N, "Rp": Rp, "mode": mode, "island_isa": isa, "tier": meta.get("tier"),
                "flags": {k: v for k, v in (meta.get("flags") or {}).items() if v is True},
                "binary_sha": dig(ev, "binary", "sha256"), "fit_binary_sha": dig(meta, "binary", "sha256")})
    tier_final = meta.get("tier")
    # ADDENDUM_1: a T fit is delivered at its own calibration N_final = N_plan * 4^tier_final (D-26); the tier must be recorded.
    # V fits (bounded plan, no tier) and a T fit with no recorded tier keep the registered N.
    n_want = spec["N"]
    if rec["arm"] == "T" and isinstance(tier_final, int) and not isinstance(tier_final, bool) and tier_final >= 0:
        n_want = spec["N"] * 4 ** tier_final
    rec["tier_final"] = tier_final
    rec["N_final"] = N
    rec["N_expected_at_tier"] = n_want
    for lab, got, want in (("N", N, n_want), ("Rp", Rp, spec["Rp"])):
        if got is None:
            rec["warnings"].append("%s not found in eval/fit/manifest (unverified)" % lab)
        elif got != want:
            rec["reasons"].append("arm settings: %s = %r, pre-registered %r" % (lab, got, want))
    if mode is None:
        rec["warnings"].append("mode not found (unverified)")
    elif mode not in spec["mode"]:
        rec["reasons"].append("arm settings: mode = %r, pre-registered one of %r" % (mode, spec["mode"]))
    if rec["arm"] == "V" and isa is not None and isa != spec["island_isa"]:
        rec["reasons"].append("arm settings: island_isa = %r, pre-registered %r" % (isa, spec["island_isa"]))
    if rec["arm"] == "V" and isa is None:
        rec["warnings"].append("island_isa not found (unverified)")
    # --- selection
    sel = ev.get("selection") or {}
    rec["hpm"] = frozenset(sel["hpm"]) if isinstance(sel.get("hpm"), list) else None
    rec["mpm"] = frozenset(sel["mpm"]) if isinstance(sel.get("mpm"), list) else None
    rec["F_hpm"] = sel.get("F_hpm", meta.get("hpm_F"))
    rec["hpm_size"] = sel.get("hpm_size")
    for k in ("hpm_fp", "hpm_fn", "hpm_eq_S0", "mpm_eq_S0", "outcome_class"):
        rec[k] = sel.get(k)
    if rec["hpm"] is None or not isnum(rec["F_hpm"]):
        rec["reasons"].append("selection.hpm / F_hpm missing")
    # --- evidence
    evd = ev.get("evidence") or {}
    rec["logZ"], rec["logZ_T"] = evd.get("logZ"), evd.get("logZ_T")
    rec["R_eff"], rec["sigma_hat"] = evd.get("R_eff"), evd.get("sigma_hat")
    lzr = evd.get("logZ_r")
    rec["logZ_r"] = lzr if isinstance(lzr, list) else None
    if not isnum(rec["logZ"]) or not isnum(rec["logZ_T"]):
        rec["reasons"].append("evidence.logZ / logZ_T missing")
    rec["se_logZ_isl"] = se_logZ_islands(rec["logZ_r"], rec["sigma_hat"], Rp)
    # --- PIP summaries of the eval record
    rec["n_null_gt_0.5"] = dig(ev, "pip", "eq", "n_null_gt_0.5")
    rec["sup_null_eq"] = dig(ev, "pip", "eq", "sup_null")
    rec["min_true_eq"] = dig(ev, "pip", "eq", "min_true")
    rec["pip_max_sd_isl"] = dig(ev, "pip", "island_spread", "max_sd")
    # --- predictive / distribution
    T = dig(ev, "dist", "T") or {}
    pr = T.get("predictive") or {}
    rec["pred_h2"], rec["pred_h2_se_x"], rec["pred_h2_se_tail"] = pr.get("h2"), pr.get("h2_se_x"), pr.get("h2_se_tail")
    rec["pred_exact"], rec["pred_kl"] = pr.get("exact"), pr.get("kl")
    rec["test_mlpd"], rec["test_mse"] = dig(T, "test", "mlpd"), dig(T, "test", "mse")
    rec["dropped_mass"] = T.get("dropped_mass")
    rec["plugin_h2_H"] = dig(ev, "dist", "H", "plugin", "h2")
    rec["plugin_h2_M"] = dig(ev, "dist", "M", "plugin", "h2")
    rec["plugin_h2_T"] = dig(T, "plugin", "h2")
    rec["weighted_plugin_h2_T"] = dig(T, "weighted_plugin", "h2")
    rec["oracle_pred_h2"] = dig(ev, "dist", "oracle", "predictive", "h2")
    rec["ratio_to_oracle_T"] = dig(ev, "dist", "ratio_to_oracle", "T")
    rec["post_dH_q50_T"] = dig(T, "post_dH", "q50")
    if not isnum(rec["pred_h2"]):
        rec["reasons"].append("dist.T.predictive.h2 missing")
    # --- cost
    rec["core_h"], rec["cost_src"] = load_cost(rundir, rid, opts["cost_dirs"], ev)
    # --- fit.bin: p-wide PIPs and the island matrix
    fb = os.path.join(rundir, "fit.bin")
    if not os.path.isfile(fb) and opts["fitbin_dir"]:
        alt = os.path.join(opts["fitbin_dir"], "%s_%s.fit.bin" % (batch_name(rundir, rid), rid))
        fb = alt if os.path.isfile(alt) else fb
    rec["fit_bin"] = fb if os.path.isfile(fb) else None
    rec["pip_eq"] = rec["pip_T"] = rec["pip_list"] = rec["se_pip"] = None
    if rec["fit_bin"] is None:
        rec["reasons"].append("fit.bin not found")
    else:
        try:
            s = read_sections(fb, ["pip_eq", "pip_T", "pip_list", "pip_r", "logZ_r", "orig"], verify=opts["verify"])
            if "pip_eq" in s:
                rec["pip_eq"] = s["pip_eq"][0]
                rec["p_kept"] = len(rec["pip_eq"])
            else:
                rec["reasons"].append("fit.bin has no pip_eq")
            if "pip_T" in s:
                rec["pip_T"] = s["pip_T"][0]
            if "pip_list" in s:
                rec["pip_list"] = s["pip_list"][0]
            if "orig" in s:
                rec["orig_hash"] = hashlib.sha256(s["orig"][0].tobytes()).hexdigest()
            if "pip_r" in s and rec["pip_eq"] is not None:
                a, (R, p) = s["pip_r"]
                rec["se_pip"] = pip_island_se(a, R, p)
                rec["R_pipr"] = R
            elif rec["pip_eq"] is not None:
                rec["warnings"].append("fit.bin has no pip_r: PIP s.e. unavailable")
            if rec["logZ_r"] is None and "logZ_r" in s:
                rec["logZ_r"] = list(s["logZ_r"][0])
                rec["se_logZ_isl"] = se_logZ_islands(rec["logZ_r"], rec["sigma_hat"], Rp)
        except (ValueError, OSError, struct.error) as e:
            rec["reasons"].append("fit.bin unreadable: %s" % e)
    rec["delivered"] = not rec["reasons"]
    return rec


def se_logZ_islands(lzr, sigma_hat, Rp):
    """Delta-method s.e. of log Zhat = log mean_r exp(logZ_r):  sd_r(Z_r / Zhat) / sqrt(R)   (Zhat = plain mean, v3_run.R:155)."""
    if lzr and len(lzr) >= 2 and all(isnum(x) for x in lzr):
        mx = max(lzr)
        w = [math.exp(x - mx) for x in lzr]
        m = mean(w)
        return sd([x / m for x in w]) / math.sqrt(len(w))
    if isnum(sigma_hat) and isnum(Rp) and Rp > 0:
        return sigma_hat / math.sqrt(Rp)
    return None


def pip_island_se(a, R, p):
    """Per-column s.e. of the equal-weight PIP = sd over the R islands / sqrt(R).  a is the row-major R x p matrix."""
    se = []
    sq = math.sqrt(R)
    for j in range(p):
        col = a[j::p]
        se.append(sd(col) / sq if R > 1 else float("nan"))
    return se


# ----------------------------------------------------------------------------------------------------------------
# the pre-registered comparison
# ----------------------------------------------------------------------------------------------------------------
def expected_datasets():
    return [(d, r) for d, reps in PREREG["grid"] for r in range(1, reps + 1)]


def ds_id(design, rep):
    return "%s-%s-n200-r%02d" % (PREREG["run_id_prefix"], design, rep)


def crit(cid, name, status, detail, **kw):
    d = {"id": cid, "name": name, "status": status, "detail": detail}
    d.update(kw)
    return d


def compare(recs, opts):
    """recs: run_id -> parsed record.  Returns (per_dataset rows, criteria list, summary dict, outcome dict)."""
    P = PREREG
    dsets = expected_datasets()
    seeds = P["seeds"]
    warn = []
    byds = {}
    for rid, r in recs.items():
        if r["rep"] is not None and r["run_id"].startswith(P["run_id_prefix"] + "-"):
            byds.setdefault((r["design"], r["rep"]), {})[(r["arm"], r["seed"])] = r

    def get(ds, arm, s):
        r = byds.get(ds, {}).get((arm, s))
        return r if (r is not None and r["delivered"]) else None

    # ---------------- D: delivered 40/40
    expected_ids = ["%s-%s-n200-r%02d-%s-s%d" % (P["run_id_prefix"], d, rp, a, s) for d, rp in dsets for a in ("V", "T") for s in seeds]
    missing = [i for i in expected_ids if i not in recs]
    bad = [(i, recs[i]["reasons"]) for i in expected_ids if i in recs and not recs[i]["delivered"]]
    unexpected = [i for i in recs if i.startswith(P["run_id_prefix"] + "-") and i not in expected_ids]
    n_deliv = len(expected_ids) - len(missing) - len(bad)
    C = []
    C.append(crit("D", "delivered 40/40 (complete, valid arm settings, fit.bin readable)", "PASS" if n_deliv == P["n_fits"] else "FAIL",
                  "%d/%d delivered; missing %d; failed/invalid %d; unexpected %d" % (n_deliv, P["n_fits"], len(missing), len(bad), len(unexpected)),
                  missing=missing, failed=[{"run_id": i, "reasons": r} for i, r in bad], unexpected=unexpected))

    # ---------------- pairing: X, y sha equal across the 4 fits of a dataset
    pairing_bad = []
    for ds in dsets:
        shas = {(r["X_sha"], r["y_sha"]) for r in byds.get(ds, {}).values()}
        if any(x is None or y is None for x, y in shas):
            pairing_bad.append({"dataset": ds_id(*ds), "problem": "truth.json X_sha256 / y_sha256 missing in a fit"})
        elif len(shas) > 1:
            pairing_bad.append({"dataset": ds_id(*ds), "problem": "X/y sha differ across fits", "shas": sorted(map(list, shas))})
    # same X/y must not be reused across datasets
    seen = {}
    for ds in dsets:
        for r in byds.get(ds, {}).values():
            if r["X_sha"]:
                seen.setdefault(r["X_sha"], set()).add(ds)
    for x, s in seen.items():
        if len(s) > 1:
            pairing_bad.append({"dataset": "|".join(ds_id(*d) for d in sorted(s)), "problem": "identical X_sha256 in different datasets"})
    C.append(crit("PAIR", "X/y sha256 equal across the 4 fits of each dataset", "PASS" if not pairing_bad else "FAIL",
                  "%d problems" % len(pairing_bad), problems=pairing_bad))

    # binaries / commit consistency (info only; stop rule at HQ level)
    info = {"binary_sha_by_arm": {}, "code_commits": sorted({r["code_commit"] for r in recs.values() if r["code_commit"]})}
    for a in ("V", "T"):
        info["binary_sha_by_arm"][a] = sorted({(r["binary_sha"], r["fit_binary_sha"]) for r in recs.values()
                                                if r["arm"] == a and r["run_id"].startswith(P["run_id_prefix"] + "-") and r["binary_sha"]})
    if len(info["code_commits"]) > 1:
        warn.append("several code_commit values across run manifests: %s" % info["code_commits"])
    if opts.get("expect_commit") and info["code_commits"] != [opts["expect_commit"]]:
        warn.append("code_commit %s differs from --expect-commit %s" % (info["code_commits"], opts["expect_commit"]))
    for a, v in info["binary_sha_by_arm"].items():
        if len(v) > 1:
            warn.append("arm %s: %d different binary sha256 pairs (plan 2: one build per arm)" % (a, len(v)))

    # ---------------- evidence yardstick: pooled seed-to-seed sd per arm
    def pooled_seed_var(arm, key="logZ"):
        ss = []
        for ds in dsets:
            a, b = get(ds, arm, seeds[0]), get(ds, arm, seeds[1])
            if a and b and isnum(a[key]) and isnum(b[key]):
                ss.append((a[key] - b[key]) ** 2 / 2.0)
        return (mean(ss), len(ss)) if ss else (float("nan"), 0)

    sV2, dfV = pooled_seed_var("V")
    sT2, dfT = pooled_seed_var("T")

    rows = []
    n_hpm_ok = n_hpm_real_miss = n_hpm_evaluable = 0
    t_higher = []
    mpm_bad = []
    pip_fail, ev_fail, lb_fail, pred_fail, pred_pending, null_fail = [], [], [], [], [], []
    ev_eval = pip_eval = pred_eval = 0
    for ds in dsets:
        row = {"dataset": ds_id(*ds), "design": ds[0], "rep": ds[1]}
        did = ds_id(*ds)
        # ---- selection (per engine-seed pair)
        pair_ok = []
        for s in seeds:
            v, t = get(ds, "V", s), get(ds, "T", s)
            row["delivered_V_s%d" % s], row["delivered_T_s%d" % s] = v is not None, t is not None
            if v and t:
                eq = v["hpm"] == t["hpm"]
                row["hpm_equal_s%d" % s] = eq
                row["hpm_V_s%d" % s] = ";".join(map(str, sorted(v["hpm"])))
                row["hpm_T_s%d" % s] = ";".join(map(str, sorted(t["hpm"])))
                row["F_V_s%d" % s], row["F_T_s%d" % s] = v["F_hpm"], t["F_hpm"]
                hi = t["F_hpm"] > v["F_hpm"] + P["F_tol"]
                row["T_higher_F_s%d" % s] = hi
                if hi:
                    t_higher.append("%s s%d (F_T - F_V = %.3g)" % (did, s, t["F_hpm"] - v["F_hpm"]))
                row["mpm_equal_s%d" % s] = v["mpm"] == t["mpm"]
                if v["mpm"] != t["mpm"]:
                    mpm_bad.append("%s s%d" % (did, s))
                pair_ok.append(eq)
        if len(pair_ok) == len(seeds):
            n_hpm_evaluable += 1
            ok = all(pair_ok)
            row["hpm_dataset_ok"] = ok
            n_hpm_ok += ok
            n_hpm_real_miss += (not ok)
        else:
            row["hpm_dataset_ok"] = None
            if pair_ok and not all(pair_ok):       # a real mismatch in the one pair we do have
                n_hpm_real_miss += 1
        # ---- NULL check
        if ds[0] == "NULL":
            for a in ("V", "T"):
                for s in seeds:
                    r = get(ds, a, s)
                    if r is not None:
                        n = r["n_null_gt_0.5"]
                        row["null_pip_gt_half_%s_s%d" % (a, s)] = n
                        if n is None or n > 0:
                            null_fail.append("%s %s s%d (n_null_gt_0.5 = %s)" % (did, a, s, n))
        # ---- evidence
        zs = {(a, s): get(ds, a, s) for a in ("V", "T") for s in seeds}
        full = all(zs.values())
        for (a, s), r in zs.items():
            if r:
                row["logZ_%s_s%d" % (a, s)] = r["logZ"]
                row["logZ_T_%s_s%d" % (a, s)] = r["logZ_T"]
                row["se_isl_%s_s%d" % (a, s)] = r["se_logZ_isl"]
                row["tier_final_%s_s%d" % (a, s)], row["N_final_%s_s%d" % (a, s)] = r.get("tier_final"), r.get("N_final")
        if full and dfV > 0 and dfT > 0:
            def arm_var(a, s2):
                isl = [zs[(a, s)]["se_logZ_isl"] for s in seeds]
                isl_var = sum(x * x for x in isl) / 4.0 if all(isnum(x) for x in isl) else 0.0
                return max(s2 / 2.0, isl_var)
            vV, vT = arm_var("V", sV2), arm_var("T", sT2)
            se = math.sqrt(vV + vT)
            dz = mean([zs[("V", s)]["logZ"] for s in seeds]) - mean([zs[("T", s)]["logZ"] for s in seeds])
            row["logZ_diff_VminusT"], row["se_comb_logZ"] = dz, se
            row["logZ_ratio"] = abs(dz) / se if se > 0 else (0.0 if dz == 0 else float("inf"))
            row["logZ_ok"] = abs(dz) <= P["z_mult"] * se
            ev_eval += 1
            if not row["logZ_ok"]:
                ev_fail.append("%s (|d| = %.4g, 3se = %.4g)" % (did, abs(dz), P["z_mult"] * se))
            # deterministic lower bound consistency: log Z_T(arm A) <= log Zhat(arm B) + 3 se_comb (both directions)
            zT_V, zT_T = mean([zs[("V", s)]["logZ_T"] for s in seeds]), mean([zs[("T", s)]["logZ_T"] for s in seeds])
            zh_V, zh_T = mean([zs[("V", s)]["logZ"] for s in seeds]), mean([zs[("T", s)]["logZ"] for s in seeds])
            row["logZ_T_arm_V"], row["logZ_T_arm_T"] = zT_V, zT_T
            row["logZ_T_diff_TminusV"] = zT_T - zT_V
            lb_ok = (zT_V <= zh_T + P["z_mult"] * se) and (zT_T <= zh_V + P["z_mult"] * se)
            # own-arm consistency: log Z_T <= log Zhat within 3 island s.e. (a deterministic lower bound cannot exceed the truth)
            for a in ("V", "T"):
                for s in seeds:
                    r = zs[(a, s)]
                    if isnum(r["se_logZ_isl"]) and r["logZ_T"] > r["logZ"] + P["z_mult"] * r["se_logZ_isl"] + 1e-9:
                        lb_ok = False
            row["logZ_T_lowerbound_ok"] = lb_ok
            if not lb_ok:
                lb_fail.append(did)
        else:
            row["logZ_ok"] = None
            row["logZ_T_lowerbound_ok"] = None
        # ---- PIP
        if full:
            pe = {k: mean_vec([zs[(k, s)]["pip_eq"] for s in seeds]) for k in ("V", "T")}
            n_cols = {len(zs[(a, s)]["pip_eq"]) for a in ("V", "T") for s in seeds}
            if len(n_cols) != 1:
                row["pip_ok"] = None
                row["pip_note"] = "PIP vectors of different length %s" % sorted(n_cols)
                pip_fail.append("%s: PIP vectors of different length" % did)
            else:
                orig = {zs[(a, s)].get("orig_hash") for a in ("V", "T") for s in seeds}
                if len(orig) > 1:
                    pip_fail.append("%s: kept->original column maps differ" % did)
                se_ok = all(zs[(a, s)]["se_pip"] is not None for a in ("V", "T") for s in seeds)
                p = n_cols.pop()
                worst, worst_j, worst_thr, maxabs, maxabs_j = 0.0, -1, None, 0.0, -1
                for j in range(p):
                    d = abs(pe["V"][j] - pe["T"][j])
                    if se_ok:
                        vv = {a: sum(zs[(a, s)]["se_pip"][j] ** 2 for s in seeds) / 4.0 for a in ("V", "T")}
                        sej = math.sqrt(vv["V"] + vv["T"])
                    else:
                        sej = 0.0
                    thr = max(P["pip_floor"], P["z_mult"] * sej)
                    if d > maxabs:
                        maxabs, maxabs_j = d, j
                    if d / thr > worst:
                        worst, worst_j, worst_thr = d / thr, j, thr
                row["pip_max_abs_diff"] = maxabs
                row["pip_argmax_kept_index0"] = maxabs_j
                row["pip_worst_ratio"] = worst
                row["pip_thr_at_worst"] = worst_thr
                row["pip_ok"] = (worst <= 1.0) if se_ok else None
                if se_ok:
                    pip_eval += 1
                else:
                    row["pip_note"] = "pip_r missing: s.e. unavailable (floor 0.01 only) -> not evaluated"
                    if worst > 1.0:
                        pip_fail.append("%s: exceeds the 0.01 floor even without s.e. (max|d| = %.4g)" % (did, maxabs))
                if row["pip_ok"] is False:
                    pip_fail.append("%s (worst |d|/thr = %.3g at kept col %d, max|d| = %.4g)" % (did, worst, worst_j, maxabs))
                # reported, not criteria: PIP_T, list-PIP, T's own seed spread, V's own seed spread
                for lab, key in (("pipT", "pip_T"), ("pipList", "pip_list")):
                    if all(zs[(a, s)][key] is not None for a in ("V", "T") for s in seeds):
                        m2 = {a: mean_vec([zs[(a, s)][key] for s in seeds]) for a in ("V", "T")}
                        row["%s_max_abs_diff" % lab] = max(abs(x - y) for x, y in zip(m2["V"], m2["T"]))
                for a in ("V", "T"):
                    row["pip_seed_range_%s" % a] = max(abs(x - y) for x, y in zip(zs[(a, seeds[0])]["pip_eq"], zs[(a, seeds[1])]["pip_eq"]))
        else:
            row["pip_ok"] = None
        # ---- predictive
        for a in ("V", "T"):
            for s in seeds:
                r = zs[(a, s)]
                if r:
                    row["pred_h2_%s_s%d" % (a, s)] = r["pred_h2"]
                    row["plugin_h2_HPM_%s_s%d" % (a, s)] = r["plugin_h2_H"]
                    row["plugin_h2_MPM_%s_s%d" % (a, s)] = r["plugin_h2_M"]
        if full:
            dT = mean([math.sqrt(max(zs[("T", s)]["pred_h2"], 0.0)) for s in seeds])
            dV = mean([math.sqrt(max(zs[("V", s)]["pred_h2"], 0.0)) for s in seeds])
            row["dH_T_to_fstar"], row["dH_V_to_fstar"] = dT, dV
            screen = abs(dT - dV)       # triangle inequality: d_H(V,T) >= |d_H(V,f*) - d_H(T,f*)|
            row["dH_VT_lower_bound_triangle"] = screen
            row["pred_threshold"] = P["hell_frac"] * dT
            cross = opts["cross"].get(did)
            if cross is not None:
                dvt = mean([math.sqrt(max(cross[s]["h2"], 0.0)) for s in seeds if s in cross]) if all(s in cross for s in seeds) else None
            else:
                dvt = None
            if dvt is not None:
                row["dH_VT"] = dvt
                row["pred_ratio"] = dvt / dT if dT > 0 else float("inf")
                row["pred_status"] = "PASS" if dvt <= P["hell_frac"] * dT else "FAIL"
                pred_eval += 1
                if row["pred_status"] == "FAIL":
                    pred_fail.append("%s (d_VT = %.4g > %.4g)" % (did, dvt, P["hell_frac"] * dT))
            elif screen > P["hell_frac"] * dT:
                row["pred_status"] = "FAIL"
                row["pred_note"] = "cross value absent; FAIL certain from the triangle screen |dV - dT| > 10% dT"
                pred_fail.append("%s (screen: |dV - dT| = %.4g > %.4g; cross value absent)" % (did, screen, P["hell_frac"] * dT))
                pred_eval += 1
            else:
                row["pred_status"] = "NOT_EVALUATED"
                row["pred_note"] = "no V-vs-T cross Hellinger supplied (--cross-file); triangle screen only"
                pred_pending.append(did)
        else:
            row["pred_status"] = None
        # ---- cost
        for a in ("V", "T"):
            for s in seeds:
                r = byds.get(ds, {}).get((a, s))
                if r:
                    row["core_h_%s_s%d" % (a, s)] = r["core_h"]
        rows.append(row)

    # ---------------- criteria
    C.append(crit("S1", "HPM(V) = HPM(T) as sets, both engine-seed pairs, in >= %d of %d datasets" % (P["hpm_datasets_min"], len(dsets)),
                  "PASS" if n_hpm_ok >= P["hpm_datasets_min"] else "FAIL",
                  "%d/%d datasets equal (%d evaluable, %d real mismatching datasets)" % (n_hpm_ok, len(dsets), n_hpm_evaluable, n_hpm_real_miss),
                  n_ok=n_hpm_ok, n_real_miss=n_hpm_real_miss))
    C.append(crit("S2", "T never reports a higher-F HPM than V (per seed pair)", "PASS" if not t_higher else "FAIL",
                  "%d pairs with F_T > F_V + %g" % (len(t_higher), P["F_tol"]), pairs=t_higher))
    n_mpm_eval = sum(1 for ds in dsets for s in seeds if get(ds, "V", s) and get(ds, "T", s))
    C.append(crit("S3", "MPM(V) = MPM(T) in every evaluable dataset-seed pair", "PASS" if not mpm_bad and n_mpm_eval == len(dsets) * len(seeds) else
                  ("FAIL" if mpm_bad else "NOT_EVALUATED"), "%d mismatching pairs of %d evaluable" % (len(mpm_bad), n_mpm_eval), pairs=mpm_bad))
    n_null_eval = sum(1 for ds in dsets if ds[0] == "NULL" for a in ("V", "T") for s in seeds if get(ds, a, s))
    C.append(crit("S4", "NULL dataset: no column with PIP > 0.5 (either arm, either seed)", "FAIL" if null_fail else ("PASS" if n_null_eval == 4 else "NOT_EVALUATED"),
                  "%d fits checked, %d violations" % (n_null_eval, len(null_fail)), violations=null_fail))
    pip_status = "FAIL" if pip_fail else ("PASS" if pip_eval == len(dsets) else "NOT_EVALUATED")
    C.append(crit("P", "max_j |PIP_V - PIP_T| <= max(0.01, 3 combined s.e.) for pip_primary (= pip_eq), every dataset",
                  pip_status, "%d/%d datasets evaluated, %d fail" % (pip_eval, len(dsets), len(pip_fail)), datasets=pip_fail))
    if dfV and dfT:
        yard = "pooled seed-to-seed sd (df V %d, T %d): s_V = %.4g, s_T = %.4g" % (dfV, dfT, math.sqrt(sV2), math.sqrt(sT2))
    else:
        yard = "pooled seed-to-seed sd unavailable (needs a dataset with both seeds in an arm)"
    C.append(crit("E1", "|log Zhat_V - log Zhat_T| <= 3 combined s.e. (seed-pooled / island, per dataset)",
                  "FAIL" if ev_fail else ("PASS" if ev_eval == len(dsets) else "NOT_EVALUATED"),
                  "%d/%d datasets evaluated, %d fail; %s" % (ev_eval, len(dsets), len(ev_fail), yard), datasets=ev_fail))
    C.append(crit("E2", "log Z_T deterministic lower bound: consistent with the other arm's log Zhat (3 combined s.e.) and its own",
                  "FAIL" if lb_fail else ("PASS" if ev_eval == len(dsets) else "NOT_EVALUATED"),
                  "%d datasets inconsistent (log Z_T reported per arm in per_dataset.csv; log Zhat_occ deferred, D-21 / H-18)" % len(lb_fail), datasets=lb_fail))
    ps = ("FAIL" if pred_fail and (len(pred_fail) >= 1) else ("PASS" if pred_eval == len(dsets) and not pred_pending else "NOT_EVALUATED"))
    C.append(crit("H", "Hellinger d_H(V,T) between the store-BMA predictives <= 10% of d_H(T,f*), every dataset",
                  ps, "%d datasets evaluated (%d with a V-vs-T cross value), %d fail, %d pending%s" %
                  (pred_eval, len([r for r in rows if "dH_VT" in r]), len(pred_fail), len(pred_pending),
                   " (no cross value supplied via --cross-file; the engine eval has NO V-vs-T field, only the triangle screen ran)" if pred_pending else ""),
                  datasets=pred_fail, pending=pred_pending))
    # cost
    over = []
    nocost = []
    for rid in expected_ids:
        r = recs.get(rid)
        if not r:
            continue
        lim = PREREG["cost_factor"] * PREREG["arms"][r["arm"]]["cost_model_core_h"]
        if r["core_h"] is None:
            nocost.append(rid)
        elif r["core_h"] > lim:
            over.append("%s: %.1f > %.1f" % (rid, r["core_h"], lim))
    C.append(crit("C", "cost <= 1.5 x model per fit (V 15.0, T 172.5 core-h, sacct billed)", "FAIL" if over else ("PASS" if not nocost and len(recs) else "NOT_EVALUATED"),
                  "%d fits over limit, %d without a cost record" % (len(over), len(nocost)), over=over, no_cost=nocost))

    # ---------------- outcome
    by_id = {c["id"]: c for c in C}
    notclean = []
    if n_hpm_real_miss >= P["notclean_hpm_misses"]:
        notclean.append(">= %d datasets with an HPM mismatch" % P["notclean_hpm_misses"])
    if t_higher:
        notclean.append("T reports a higher-F model than V")
    if len(pred_fail) >= P["notclean_pred_misses"]:
        notclean.append("predictive Hellinger > 10%% on >= %d datasets" % P["notclean_pred_misses"])
    incomplete = by_id["D"]["status"] != "PASS" or by_id["PAIR"]["status"] != "PASS" or any(c["status"] == "NOT_EVALUATED" for c in C)
    other_fail = [c["id"] for c in C if c["status"] == "FAIL" and c["id"] not in ("D", "PAIR")]
    if by_id["PAIR"]["status"] == "FAIL":
        outcome, why = "INVALID", ["dataset pairing broken (X/y sha): the comparison is not valid; stop and tell HQ"]
    elif notclean:
        outcome, why = "NOT CLEAN", notclean
    elif other_fail:
        outcome, why = "MARGINAL", ["criteria failed: %s (not in the not-clean list)" % ", ".join(other_fail)]
    elif incomplete:
        outcome, why = "INCOMPLETE", ["criteria not PASS: %s" % ", ".join(c["id"] for c in C if c["status"] != "PASS")]
    else:
        outcome, why = "CLEAN", ["all pre-registered criteria PASS (release still needs the independent review ACCEPT)"]
    summary = {"n_fits_expected": P["n_fits"], "n_delivered": n_deliv, "pooled_seed_sd": {"V": math.sqrt(sV2) if dfV else None, "T": math.sqrt(sT2) if dfT else None,
                                                                                               "df_V": dfV, "df_T": dfT},
               "info": info, "warnings": warn, "duplicates_resolved": opts.get("dups", [])}
    # cost totals
    tot = {a: [recs[i]["core_h"] for i in expected_ids if i in recs and recs[i]["arm"] == a and recs[i]["core_h"] is not None] for a in ("V", "T")}
    summary["cost_core_h"] = {a: {"n": len(v), "sum": sum(v), "max": max(v) if v else None} for a, v in tot.items()}
    summary["cost_core_h"]["total"] = sum(sum(v) for v in tot.values())
    return rows, C, summary, {"outcome": outcome, "reasons": why, "incomplete": incomplete, "other_fail": other_fail}


def wave_check(recs, opts):
    """Per-(dataset, seed) V-vs-T pair table for partial data (W0 / W1 / W2).  NO verdict: island-only s.e., single seed.
    Use it to debug field parsing and to read a wave before all 40 fits exist."""
    P = PREREG
    rows = []
    pairs = {}
    for rid, r in recs.items():
        pairs.setdefault((r["design"], r["rep"], r["seed"]), {})[r["arm"]] = r
    for (design, rep, seed), d in sorted(pairs.items()):
        row = {"dataset": ds_id(design, rep), "seed": seed, "V_delivered": bool(d.get("V") and d["V"]["delivered"]),
               "T_delivered": bool(d.get("T") and d["T"]["delivered"])}
        v, t = d.get("V"), d.get("T")
        for a, r in (("V", v), ("T", t)):
            if r:
                row["reasons_" + a] = " | ".join(r["reasons"])
                row["core_h_" + a] = r["core_h"]
                row["tier_" + a] = r.get("tier")
                row["tier_final_" + a], row["N_final_" + a] = r.get("tier_final"), r.get("N_final")
                row["flags_" + a] = ",".join(sorted(r.get("flags", {})))
        if v and t and v["delivered"] and t["delivered"]:
            row["X_y_sha_equal"] = (v["X_sha"], v["y_sha"]) == (t["X_sha"], t["y_sha"])
            row["hpm_equal"] = v["hpm"] == t["hpm"]
            row["mpm_equal"] = v["mpm"] == t["mpm"]
            row["F_V"], row["F_T"] = v["F_hpm"], t["F_hpm"]
            row["T_higher_F"] = t["F_hpm"] > v["F_hpm"] + P["F_tol"]
            row["logZ_V"], row["logZ_T"] = v["logZ"], t["logZ"]
            row["logZ_T_lb_V"], row["logZ_T_lb_T"] = v["logZ_T"], t["logZ_T"]
            if isnum(v["se_logZ_isl"]) and isnum(t["se_logZ_isl"]):
                se = math.sqrt(v["se_logZ_isl"] ** 2 + t["se_logZ_isl"] ** 2)
                row["logZ_diff_VminusT"], row["se_isl_comb"] = v["logZ"] - t["logZ"], se
                row["logZ_diff_in_se"] = abs(v["logZ"] - t["logZ"]) / se if se > 0 else None
            if v["pip_eq"] is not None and t["pip_eq"] is not None and len(v["pip_eq"]) == len(t["pip_eq"]):
                dd = [abs(x - y) for x, y in zip(v["pip_eq"], t["pip_eq"])]
                row["pip_max_abs_diff"] = max(dd)
                if v["se_pip"] and t["se_pip"]:
                    row["pip_worst_ratio_isl"] = max(x / max(P["pip_floor"], P["z_mult"] * math.sqrt(a * a + b * b))
                                                     for x, a, b in zip(dd, v["se_pip"], t["se_pip"]))
            if isnum(v["pred_h2"]) and isnum(t["pred_h2"]):
                dT, dV = math.sqrt(max(t["pred_h2"], 0.0)), math.sqrt(max(v["pred_h2"], 0.0))
                row["dH_T_to_fstar"], row["dH_V_to_fstar"] = dT, dV
                row["dH_VT_lower_bound_triangle"] = abs(dT - dV)
                row["triangle_screen_exceeds_10pct"] = abs(dT - dV) > P["hell_frac"] * dT
                cr = opts["cross"].get(ds_id(design, rep), {}).get(seed)
                if cr is not None:
                    row["dH_VT"] = math.sqrt(max(cr["h2"], 0.0))
                    row["dH_VT_over_dH_T"] = row["dH_VT"] / dT if dT > 0 else None
        rows.append(row)
    return rows


def mean_vec(vs):
    n = len(vs)
    return [sum(x) / n for x in zip(*vs)]


# ----------------------------------------------------------------------------------------------------------------
# output
# ----------------------------------------------------------------------------------------------------------------
def write_csv(path, rows):
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})


def per_fit_rows(recs):
    out = []
    for rid in sorted(recs):
        r = recs[rid]
        out.append({"run_id": rid, "arm": r["arm"], "seed": r["seed"], "delivered": r["delivered"], "reasons": " | ".join(r["reasons"]),
                    "warnings": " | ".join(r["warnings"]), "N": r.get("N"), "Rp": r.get("Rp"), "mode": r.get("mode"), "tier": r.get("tier"),
                    "tier_final": r.get("tier_final"), "N_final": r.get("N_final"),
                    "flags_true": ",".join(sorted(r.get("flags", {}))), "island_isa": r.get("island_isa"), "p_kept": r.get("p_kept"),
                    "hpm": ";".join(map(str, sorted(r["hpm"]))) if r.get("hpm") is not None else "", "F_hpm": r.get("F_hpm"),
                    "mpm": ";".join(map(str, sorted(r["mpm"]))) if r.get("mpm") is not None else "",
                    "logZ": r.get("logZ"), "se_logZ_islands": r.get("se_logZ_isl"), "logZ_T_lower_bound": r.get("logZ_T"),
                    "pred_h2": r.get("pred_h2"), "pred_h2_se_x": r.get("pred_h2_se_x"), "pred_h2_se_tail": r.get("pred_h2_se_tail"), "pred_kl": r.get("pred_kl"),
                    "plugin_h2_HPM": r.get("plugin_h2_H"), "plugin_h2_MPM": r.get("plugin_h2_M"), "weighted_plugin_h2_T": r.get("weighted_plugin_h2_T"),
                    "oracle_pred_h2": r.get("oracle_pred_h2"), "test_mse": r.get("test_mse"), "test_mlpd": r.get("test_mlpd"),
                    "n_null_gt_0.5": r.get("n_null_gt_0.5"), "pip_max_sd_islands": r.get("pip_max_sd_isl"), "core_h": r.get("core_h"),
                    "binary_sha": r.get("binary_sha"), "code_commit": r.get("code_commit"), "dir": r["dir"]})
    return out


def write_md(path, verdict, rows, C, summary, outcome, opts):
    L = []
    L.append("# 10^4 T-vs-V overlap: verdict\n")
    L.append("**Outcome: %s**  \nreasons: %s  \n" % (outcome["outcome"], "; ".join(outcome["reasons"])))
    L.append("script sha256 `%s`; delivered %d/%d; records: %s; generated by compare_overlap.py (pre-registered thresholds, OVERLAP_1e4_PREREG.md)\n" %
             (verdict["script_sha256"], summary["n_delivered"], summary["n_fits_expected"], ", ".join(verdict["records"])))
    L.append("## Criteria\n")
    L.append("| id | criterion | status | detail |\n|---|---|---|---|")
    for c in C:
        L.append("| %s | %s | **%s** | %s |" % (c["id"], c["name"], c["status"], c["detail"]))
    L.append("")
    for c in C:
        for k in ("failed", "missing", "datasets", "pairs", "over", "violations", "problems", "pending"):
            if c.get(k):
                L.append("- %s `%s`: %s" % (c["id"], k, json.dumps(c[k])[:1500]))
    L.append("\n## Per dataset\n")
    L.append("| dataset | HPM eq (s1,s2) | F_T>F_V | dlogZ (V-T) | 3 se | PIP worst ratio | max|dPIP| | d_H(T,f*) | d_H(V,T) | pred |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        L.append("| %s | %s,%s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["dataset"], fmt(r.get("hpm_equal_s1")), fmt(r.get("hpm_equal_s2")),
            fmt(r.get("T_higher_F_s1") or r.get("T_higher_F_s2")), fmt(r.get("logZ_diff_VminusT")),
            fmt(3 * r["se_comb_logZ"] if r.get("se_comb_logZ") is not None else None), fmt(r.get("pip_worst_ratio")), fmt(r.get("pip_max_abs_diff")),
            fmt(r.get("dH_T_to_fstar")), fmt(r.get("dH_VT")), fmt(r.get("pred_status"))))
    L.append("\n## Cost (sacct billed core-h)\n")
    L.append("V: n %d, sum %s, max %s; T: n %d, sum %s, max %s; total %s (plan: expected ~1.0k, ceiling 2.5k)" % (
        summary["cost_core_h"]["V"]["n"], fmt(summary["cost_core_h"]["V"]["sum"]), fmt(summary["cost_core_h"]["V"]["max"]),
        summary["cost_core_h"]["T"]["n"], fmt(summary["cost_core_h"]["T"]["sum"]), fmt(summary["cost_core_h"]["T"]["max"]), fmt(summary["cost_core_h"]["total"])))
    if summary["warnings"]:
        L.append("\n## Warnings\n" + "\n".join("- " + w for w in summary["warnings"]))
    L.append("\nPer-fit table: per_fit.csv; per-dataset table: per_dataset.csv; machine-readable: verdict.json.")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")


def load_cross(path):
    """cross file: {"schema": "overlap1e4.cross_vt/1", "pairs": {"4-AR-n200-r01": {"1": {"h2": ..., "se": ...}, "2": {...}}}}
    h2 = 1 - integral sqrt(fbar_V fbar_T) over (x, y), same 4,000 x draws x 64-node GH as the eval; d_H = sqrt(h2)."""
    if not path:
        return {}
    d = jload(path)
    out = {}
    for k, v in d.get("pairs", {}).items():
        out[k] = {int(s): x for s, x in v.items()}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records", nargs="+", required=True, help="roots searched for run dirs (records/<batch>/<run_id>/)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cost-dir", nargs="*", default=[], help="dirs with cost_<run_id>.json (p1m_cost.py --out-dir)")
    ap.add_argument("--cross-file", default=None, help="V-vs-T cross Hellinger values (see load_cross)")
    ap.add_argument("--fitbin-dir", default=None, help="fallback dir with <batch>_<run_id>.fit.bin (Owls fitbin_1117 layout)")
    ap.add_argument("--expect-commit", default=None)
    ap.add_argument("--no-verify", action="store_true", help="skip section sha256 verification of fit.bin")
    ap.add_argument("--smoke", action="store_true", help="single-arm field-parse check: no pairing, no verdict")
    ap.add_argument("--wave-check", action="store_true", help="partial data: per-(dataset, seed) V-vs-T pair table, island-only s.e., NO verdict")
    a = ap.parse_args(argv)
    opts = {"cost_dirs": a.cost_dir, "fitbin_dir": a.fitbin_dir, "verify": not a.no_verify, "expect_commit": a.expect_commit,
            "cross": load_cross(a.cross_file)}
    runs, dups = find_runs(a.records)
    opts["dups"] = [{"run_id": r, "kept": runs[r], "other": o if o != runs[r] else d} for r, d, o in dups] if dups else []
    os.makedirs(a.out, exist_ok=True)
    recs = {rid: parse_run(rid, d, opts) for rid, d in sorted(runs.items())}
    script_sha = sha256_file(os.path.abspath(__file__))
    if a.smoke:
        out = []
        for rid, r in recs.items():
            out.append({k: (sorted(v) if isinstance(v, frozenset) else v) for k, v in r.items()
                        if k not in ("pip_eq", "pip_T", "pip_list", "se_pip", "logZ_r")})
            out[-1]["pip_eq_len"] = len(r["pip_eq"]) if r.get("pip_eq") is not None else None
            out[-1]["pip_eq_max"] = max(r["pip_eq"]) if r.get("pip_eq") is not None else None
            out[-1]["se_pip_max"] = max(r["se_pip"]) if r.get("se_pip") else None
            print("%s  delivered=%s  hpm=%s F=%s logZ=%s se_isl=%s logZ_T=%s h2_pred=%s p_kept=%s se_pip_max=%s core_h=%s" % (
                rid, r["delivered"], sorted(r["hpm"]) if r.get("hpm") is not None else None, fmt(r.get("F_hpm"), 8), fmt(r.get("logZ"), 8),
                fmt(r.get("se_logZ_isl")), fmt(r.get("logZ_T"), 8), fmt(r.get("pred_h2")), r.get("p_kept"),
                fmt(out[-1]["se_pip_max"]), fmt(r.get("core_h"))))
            for x in r["reasons"]:
                print("   REASON:", x)
            for x in r["warnings"]:
                print("   warn:", x)
        with open(os.path.join(a.out, "smoke.json"), "w") as fh:
            json.dump({"script_sha256": script_sha, "runs": out}, fh, indent=1, default=str)
        return 0
    if a.wave_check:
        rows = wave_check(recs, opts)
        write_csv(os.path.join(a.out, "wave_check.csv"), rows)
        write_csv(os.path.join(a.out, "per_fit.csv"), per_fit_rows(recs))
        for r in rows:
            print("%s s%s  V:%s T:%s  hpm_eq=%s T_higher_F=%s dlogZ=%s (%s se) pip_worst_ratio=%s dH_T=%s screen>10%%=%s" % (
                r["dataset"], r["seed"], r["V_delivered"], r["T_delivered"], fmt(r.get("hpm_equal")), fmt(r.get("T_higher_F")),
                fmt(r.get("logZ_diff_VminusT")), fmt(r.get("logZ_diff_in_se")), fmt(r.get("pip_worst_ratio_isl")), fmt(r.get("dH_T_to_fstar")),
                fmt(r.get("triangle_screen_exceeds_10pct"))))
        return 0
    rows, C, summary, outcome = compare(recs, opts)
    verdict = {"schema": "overlap1e4.verdict/1", "script_sha256": script_sha, "prereg": PREREG, "records": a.records, "outcome": outcome["outcome"],
               "reasons": outcome["reasons"], "incomplete": outcome["incomplete"], "criteria": C, "summary": summary,
               "fits_tier_N": {rid: {"arm": r["arm"], "tier_final": r.get("tier_final"), "N_final": r.get("N_final"),
                                     "N_expected_at_tier": r.get("N_expected_at_tier"), "delivered": r["delivered"]}
                               for rid, r in sorted(recs.items())}}
    write_csv(os.path.join(a.out, "per_dataset.csv"), rows)
    write_csv(os.path.join(a.out, "per_fit.csv"), per_fit_rows(recs))
    with open(os.path.join(a.out, "verdict.json"), "w") as fh:
        json.dump(verdict, fh, indent=1, default=str)
    write_md(os.path.join(a.out, "verdict.md"), verdict, rows, C, summary, outcome, opts)
    print("outcome: %s  (%s)" % (outcome["outcome"], "; ".join(outcome["reasons"])))
    for c in C:
        print("  %-5s %-14s %s" % (c["id"], c["status"], c["detail"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
