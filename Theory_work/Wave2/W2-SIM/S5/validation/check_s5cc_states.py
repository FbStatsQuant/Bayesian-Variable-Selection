"""Independent per-state check of the fields added in s5cc.py (R01 item 1): re-runs the deletion-only path with its own
loop, stores per-state arrays (m, r, rT, I, delta, add-del), computes every phase maximum with numpy masks, and compares
with the s5cc.py JSON (run as a subprocess).  usage: py -3.13 check_s5cc_states.py "p n seed [q rb rw]" ..."""
import os, sys, math, json, subprocess
sys.path.insert(0, os.environ["BCS_CORE_DIR"])
import numpy as np
import bcs_core as B


def states(p, n, seed, q=5, rb=.3, rw=.7):
    rng = np.random.default_rng(10007 * seed + p)
    P = B.BCS(n, np.arange(p) // q, rb, rw, B.layout(p, q, s0=4), rng)
    isnull = np.ones(p, bool); isnull[P.S0] = False
    path = B.Path(P, np.ones(p, bool))
    k0 = 1 / math.sqrt(1 - rb); H = math.sqrt(2 * math.log(2 * p))
    Hq = math.sqrt(2 * math.log(2 ** q * p) + 2 * math.log(math.log(n)))
    rows = []
    while True:
        G = path.gains(swaps=False); nt = path.noise_tau()
        T = np.flatnonzero(path.inT); R = T[isnull[T]]
        eR = np.abs(nt["eR"][R]); e = abs(nt["e_T"])
        mxv = max([e] + ([eR.max()] if len(R) else []))
        k = path.k; Lam = math.log(n) + 2 * math.log((2 * p - k) / (k + 1))
        tau = nt["tau"][R]
        gd = G["gdel"]; ga = G["gadd"]
        rows.append(dict(m=len(R), r=k0 * mxv / H, rT=k0 * e / H, I=int((tau > 0).sum() - (tau < 0).sum()),
                         delta=1 - (Hq + k0 * mxv) ** 2 / Lam, d0=1 - Hq ** 2 / Lam,
                         ad=(ga.max() - gd.max()) / math.log(n) if len(ga) and len(gd) else -np.inf))
        if not len(R): return rows, True
        j = int(T[int(np.argmax(gd))])
        if not isnull[j] or gd.max() <= 0: return rows, False
        path.apply("del", j=j)


def mxm(v, mask):
    return float(np.max(v[mask])) if mask.any() else None


bad = 0
for case in sys.argv[1:]:
    a = case.split()
    out = json.loads(subprocess.run([sys.executable, "../scripts/s5cc.py"] + a, capture_output=True, text=True, check=True).stdout)
    kw = {}
    if len(a) > 3: kw = dict(q=int(a[3]), rb=float(a[4]), rw=float(a[5]))
    rows, ok = states(int(a[0]), int(float(a[1])), int(a[2]), **kw)
    m = np.array([r["m"] for r in rows]); rr = np.array([r["r"] for r in rows]); rT = np.array([r["rT"] for r in rows])
    I = np.array([r["I"] for r in rows]); de = np.array([r["delta"] for r in rows]); ad = np.array([r["ad"] for r in rows])
    p = int(a[0])
    exp = dict(r_bulk=mxm(rr, m >= 30), r_mid=mxm(rr, (m < 30) & (m >= 5)), r_end=mxm(rr, m < 5),
               rT_bulk=mxm(rT, m >= 30), rT_mid=mxm(rT, (m < 30) & (m >= 5)), rT_end=mxm(rT, m < 5),
               r_m_ge_p10=mxm(rr, m >= p / 10), r_m_ge_sqrtp=mxm(rr, m >= math.sqrt(p)),
               maxabsI_m_le5=(int(np.max(np.abs(I[m <= 5]))) if (m <= 5).any() else None),
               maxabsI_5_lt_m_le30=(int(np.max(np.abs(I[(m > 5) & (m <= 30)]))) if ((m > 5) & (m <= 30)).any() else None),
               delta_adm_min=float(de.min()), delta_baseline_e0=float(min(r["d0"] for r in rows)),
               deletion_path_complete=ok)
    exp_ad = dict(bulk=mxm(ad, (m >= 30)), mid=mxm(ad, (m < 30) & (m >= 5) ), end=mxm(ad, (m < 5) & (m > 0)))
    for mm in (30, 10, 5):
        exp["I%d" % mm] = int(I[m == mm][0]) if (m == mm).any() else None
    res = {}
    for k_, v in exp.items():
        w = out[k_]
        res[k_] = (v is None and w is None) or (v is not None and w is not None and abs(float(v) - float(w)) <= 1e-12)
    for k_, v in exp_ad.items():
        w = out["add_minus_del_max"][k_]
        res["add_md_" + k_] = (v is None and w is None) or (v is not None and w is not None and abs(v - w) <= 1e-12)
    allok = all(res.values()); bad += not allok
    print(case, "| complete:", ok, "| visited", out["visited_states"], "| all added fields agree:", allok,
          "" if allok else {k_: (exp.get(k_), out.get(k_)) for k_, v in res.items() if not v})
print("ALL AGREE:", bad == 0)
