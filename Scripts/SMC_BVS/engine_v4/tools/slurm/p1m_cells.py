#!/usr/bin/env python3
"""p1m_cells.py -- the executable cell/seed manifest (Sol F7; REVIEW_disposition_sol F3/F7) for the P1M experiment.

One table of CELLS (below) is the single source. This tool expands it into one row per fit (run id, seeds, mode, N,
islands, planning cost) and into Slurm-driver plans (p1m_driver.py) grouped into batches of <= 150 tasks with one
resource shape each. Docs/Experiments/P1M/MANIFEST_CELLS.md documents the same table and the totals this tool prints.

  p1m_cells.py --tsv fits.tsv [--plans DIR] [--only RUNG] [--code-commit REV]
                                                               (writes files; never submits; RUNG = 4|5|6 = log10 p,
                                                               or 1e4|1e5|1e6, or p itself)
  p1m_cells.py --summary                                       (cost per rung / block, PLANNING VALUES)

Campaign freeze (CAMPAIGN_FREEZE.md): every plan written by --plans carries
  code_commit  the engine commit the binary is built from (--code-commit REV, default HEAD; `git archive` of it is what
               is deployed), resolved to 40 hex;
  method_tag   the frozen METHOD tag, and core_tree the git tree hash of the method's source (Scripts/SMC_BVS/core).
--plans first verifies the pin (verify_freeze): the tag resolves to the pinned method commit, and the code commit's core
tree AND the tag's core tree equal the pinned core_tree, so a change to the method after the freeze refuses to generate.
(Ancestry of the tag is not required: the engine branch carries the same core tree, not the same commit.)
--no-freeze-check writes the old placeholder code_commit "UNSET-fill-at-freeze" (development and tests only).

Seed rule (deterministic, all < 2^31 - 1; collision-free because every field has its own decimal digits):
  data_seed = R * 10^8 + D * 10^6 + (n / 100) * 10^4 + rep        R = log10 p (1 = the p <= 25 exact block T8)
                                                                  D: 1 IND, 2 AR-strong, 3 AR-weak, 4 BLK, 5 ADJ-OPP, 6 NULL
  any engine-side seed = data_seed + 100 * k (same data), with the role k:
    k = 0        engine seed 1 (= data_seed; role GEN is its own Philox address domain, INTERFACES §3)
    k = 1        engine seed 2
    k = 10 + a   precision-study arm a (a = 0..7): final SMC seed (independent per arm, Sol F6)
    k = 20 + a   precision-study arm a: calibration seed (independent per arm)
  Fields: rep in 1..99, k in 0..99, n / 100 in 1..99 (n a multiple of 100), D in 1..9, R in 1..9; expand() asserts them,
  so (R, D, n, k, rep) <-> seed is one-to-one. Intended sharing only: the T, V and A3 arms of one dataset use the same
  (data seed, engine seed) on purpose (paired comparisons); expand() asserts that no other value is shared.
Costs are PLANNING VALUES (ENGINEERING_SPEC §0-v2.5 and the owner sheet; n-scaling c(n) = 3 c_s + 30 ns,
c_s = 30 + 60 n/200 ns), replaced after the SPR sweep and gate T5 by measured core-h per fit.
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import OrderedDict

# The campaign freeze pin (HQ order 11-18; H-14). The METHOD is the tag below; the engine commit is a plan input (code_commit).
FREEZE = OrderedDict([
    ("method_tag", "method-v3.1.1-listpip"),
    ("method_commit", "7100bb3b5a341aed5cbcd3b03fa5851a6345f0dd"),   # main 7100bb3b; the tag is annotated (tag object 15a6d841)
    ("core_path", "Scripts/SMC_BVS/core"),
    ("core_tree", "61b0a5822019b2737fe415ff15625e410f3227b2"),       # same tree on main, the tag and exp/P1M-engine
])
UNSET_COMMIT = "UNSET-fill-at-freeze"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HERE = os.path.dirname(os.path.abspath(__file__))

DESIGN_CODE = {"IND": 1, "AR": 2, "AR-weak": 3, "BLK": 4, "ADJ-OPP": 5, "NULL": 6}
# planning core-h per fit at n = 200 (V = V-1M class A, precise; T = theory mode in the new engine, law mode, bit form)
# 10⁶: H-9 (HQ 11-16) re-size from job 2748756, G = 256 socket-local: 1.44 × the 963 plan (≈ 288 ns·CPU per pair)
RESIZE_6 = 1.234   # H-10 (11-16): MEASURED after L5, job 2749328 (≈ 247 ns·CPU per pair); H-9 used 1.44 (job 2748756)
COST_V = {4: 10.0, 5: 96.0, 6: 963.0 * RESIZE_6}
COST_T = {4: 115.0, 5: 6100.0}          # 10⁴: upper end of 52–115 (escalating coded calibration), the WHOLE fit (N0, R' = 4)
COST_V_N5000 = {6: 1800.0 * RESIZE_6}     # the 1M self-check, reduced to N = 5,000 (H-9; was N = 10⁴ at 3,600)
COST_6_BY_N = {k: v * RESIZE_6 for k, v in {200: 963.0, 500: 1800.0, 1000: 3300.0}.items()}   # owner sheet option D, H-9 re-size
# Per (block, mode) resource shapes and the task-hour limit, from OVERLAP_1e4_SUBMISSION_PLAN §2 (PLANNING VALUES, re-sized after the
# pilot wave W0 is read back). Only the 10⁴ overlap rung has them; every other block keeps the driver's defaults. The T calibrate
# limit of 3:00 exceeds the driver's 2-h task rule (§0-v2.5), so the T overlap plans set max_task_hours = 3.0: a one-off exception
# that needs HQ's acceptance before submission.
# The driver requests the T islands' limit for the escalated N (tier 1 = 4 x N0): 0:45 x 4 = 3:00, so the planned worst case of a T fit
# is 224.7 + 216 = 440.7 core-h (an island that finishes early is billed what it used); see p1m_driver.law_islands_time.
PLAN_RESOURCES = {
    ("overlap 1e4", "V"): {"max_task_hours": 2.0, "resources": {
        "setup": {"cpus": 8, "mem": "8G", "time": "00:15:00"}, "calibrate": {"cpus": 16, "mem": "8G", "time": "00:30:00"},
        "islands": {"cpus": 4, "mem": "4G", "time": "00:30:00"}, "merge": {"cpus": 8, "mem": "4G", "time": "00:15:00"},
        "eval": {"cpus": 8, "mem": "8G", "time": "00:20:00"}}},
    ("overlap 1e4", "law"): {"max_task_hours": 3.0, "resources": {
        "setup": {"cpus": 8, "mem": "8G", "time": "00:15:00"}, "calibrate": {"cpus": 48, "mem": "16G", "time": "03:00:00"},
        "islands": {"cpus": 24, "mem": "16G", "time": "00:45:00"}, "merge": {"cpus": 8, "mem": "8G", "time": "00:20:00"},
        "eval": {"cpus": 8, "mem": "8G", "time": "00:30:00"}}},
}
MAX_REP = 99            # seed-rule field widths (see the module docstring)
K_SEED2, K_PREC_FINAL, K_PREC_CALIB = 1, 10, 20


def _git(repo, *args):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise ValueError("git %s failed: %s" % (" ".join(args), (r.stderr or r.stdout).strip()))
    return r.stdout.strip()


def verify_freeze(code_commit="HEAD", repo=HERE, freeze=FREEZE):
    """Check the freeze pin and return the 40-hex engine commit. Raises ValueError (one line) if
      - the method tag is missing or does not resolve to the pinned method commit (a moved tag), or
      - the core tree of the tag's commit, or of the code commit, differs from the pinned core_tree
        (the method changed after the freeze), or the pin itself is not 40 hex."""
    for k in ("method_commit", "core_tree"):
        if not HEX40.match(freeze[k]):
            raise ValueError("freeze pin %s is not 40 hex: %r" % (k, freeze[k]))
    tag = freeze["method_tag"]
    try:
        tagged = _git(repo, "rev-parse", "--verify", "refs/tags/%s^{commit}" % tag)
    except ValueError:
        raise ValueError("method tag %s not found here (git fetch --tags)" % tag)
    if tagged != freeze["method_commit"]:
        raise ValueError("method tag %s resolves to %s, the pin says %s (tag moved)" % (tag, tagged, freeze["method_commit"]))
    commit = _git(repo, "rev-parse", "--verify", "%s^{commit}" % code_commit)
    for what, rev in (("method tag", tagged), ("code commit", commit)):
        tree = _git(repo, "rev-parse", "--verify", "%s:%s" % (rev, freeze["core_path"]))
        if tree != freeze["core_tree"]:
            raise ValueError("%s %s: %s tree is %s, the freeze pins %s (the method changed)" % (what, rev[:8], freeze["core_path"], tree[:12], freeze["core_tree"][:12]))
    return commit


def plan_set_digest(paths, mask_commit=False):
    """sha256 over the sorted (file name, bytes) of the plan files. mask_commit blanks code_commit first, so the digest of
    the plan set is comparable before the engine freeze commit exists (everything else in a plan is commit-independent)."""
    h = hashlib.sha256()
    for p in sorted(paths, key=os.path.basename):
        b = open(p, "rb").read()
        if mask_commit:
            q = json.loads(b); q["code_commit"] = "MASKED"; b = (json.dumps(q, indent=1)).encode()
        h.update(os.path.basename(p).encode() + b"\0" + b + b"\0")
    return h.hexdigest()


def n0(n, p):
    """The engine's tier-0 particle count in theory mode (calib_run.h budgets()): N0 = max(2500, n, p)."""
    return max(2500, n, p)


def check_theory_arms(rows):
    """Overlap defect (OVERLAP_1e4_SUBMISSION_PLAN §1): every theory-mode (law) fit is N = N0 = max(2500, n, p) with R' = 4
    (EXPERIMENT_PLAN A1); a law fit with V's N = 2,500 / R' = 16 would be sized and timed as the wrong method."""
    bad = [r["run_id"] for r in rows if r["mode"] == "law" and (r["N"] != n0(r["n"], r["p"]) or r["Rp"] != 4)]
    assert not bad, "law-mode fits must have N = max(2500, n, p) and R' = 4: %s" % bad[:5]
    return True


def n_factor(n):
    c = lambda m: 3 * (30 + 60 * m / 200.0) + 30
    return c(n) / c(200)


def fit_cost(rung, n, mode, N=2500, islands=16):
    if rung == 6 and mode == "V" and N == 5000:
        return COST_V_N5000[6]
    if rung == 6:
        return COST_6_BY_N.get(n, COST_V[6] * n_factor(n))
    if mode == "law":   # T: COST_T is the whole fit (coded calibration + R' = 4 islands at N0); N and R' do not rescale it
        return COST_T[rung] * n_factor(n)
    base = COST_V[rung] * n_factor(n)
    # a fit = R′ islands + ≈ 3 island-equivalents of bounded calibration (19 for R′ = 16; OD-2); both scale with N
    return base * (N / 2500.0) * ((islands + 3) / 19.0)


# CELLS: (block, rung, design, n, reps, arms, note). arms: list of dicts {mode, seeds, N, islands, params, tag}.
V1 = [{"mode": "V", "seeds": 1, "tag": "V"}]
V2 = [{"mode": "V", "seeds": 2, "tag": "V"}]                        # seed 1 + seed 2 on the same data
# The T arm (theory mode, law, bit form; EXPERIMENT_PLAN A1, D-26): N0 = max(2500, n, p) and R' = 4 islands, coded calibration.
# The ENGINE sets N itself (calibrate: Budgets::N0, tier 1 = 4 N0 on escalation; island and merge read N from calib.bin; an explicit
# different --N is refused), so the plan's N is the tier-0 record and expand() asserts it equals N0. "N": "N0" resolves to it.
T_ARM = {"mode": "law", "seeds": 2, "tag": "T", "N": "N0", "islands": 4}
TV2 = [T_ARM, {"mode": "V", "seeds": 2, "tag": "V"}]
# Precision study (Sol F6): 8 arms, each with its OWN final seed (k = 10 + a) and calibration seed (k = 20 + a), so no
# two fits share a Philox key and none shares one with the overlap T / V or A3 fits of the same dataset. c = replicate.
# Open (WP4 open item 1, MANIFEST_CELLS §6): I_max in {0, 3} and systematic resampling (D-2, D-14) have NO arms here and
# are not costed; each extra N = 2,500 arm costs ≈ 35 core-h per dataset (≈ 106 over the 3 datasets), ESTIMATE.
PREC = [{"mode": "V", "seeds": 1, "N": N, "islands": 64, "params": {"grid_refine_m": m}, "prec_arm": a,
         "tag": "P-N%d-m%d-c%d" % (N, m, c)}
        for a, (N, m, c) in enumerate((N, m, c) for N in (2500, 10000) for m in (1, 4) for c in (1, 2))]
A3 = [{"mode": "V", "seeds": 1, "tag": "A3-exactlink", "params": {"partition": "exact_linkage"}}]
CELLS = [
    # --- exact reference T8 (p <= 25; SMC branch forced; 400 islands per fixture): costed as a block, not per fit
    ("T8 exact", 1, "AR", 200, 20, [{"mode": "V", "seeds": 1, "tag": "T8", "fixed_cost": 2.5}], "20 fixtures x 400 islands (< 50 core-h)"),
    # --- 10⁴ overlap (§0-v2.7): T (law mode) vs V, 2 seeds each, the same 10 datasets
    ("overlap 1e4", 4, "AR", 200, 4, TV2, "AR-strong"),
    ("overlap 1e4", 4, "AR-weak", 200, 2, TV2, "AR-weak (a = 0.6)"),
    ("overlap 1e4", 4, "ADJ-OPP", 200, 2, TV2, "ADJ-OPP (WP1 layout)"),
    ("overlap 1e4", 4, "IND", 200, 1, TV2, ""),
    ("overlap 1e4", 4, "NULL", 200, 1, TV2, "a = 0"),
    # --- precision study (Sol F6, mandatory): 64 islands; N x grid refinement x 2 calibration seeds; 3 overlap datasets
    ("precision", 4, "AR", 200, 1, PREC, "on overlap dataset AR-strong rep 1"),
    ("precision", 4, "AR-weak", 200, 1, PREC, "on overlap dataset AR-weak rep 1"),
    ("precision", 4, "ADJ-OPP", 200, 1, PREC, "on overlap dataset ADJ-OPP rep 1"),
    # --- 10⁴ science (n-trend, designs, null, ablations, second seed, partition)
    ("science 1e4", 4, "AR", 100, 10, V1, ""), ("science 1e4", 4, "AR", 200, 10, V2, "second seed on all 10"),
    ("science 1e4", 4, "AR", 400, 10, V1, ""), ("science 1e4", 4, "AR", 800, 10, V1, ""),
    ("science 1e4", 4, "AR-weak", 100, 20, V1, ""), ("science 1e4", 4, "AR-weak", 200, 20, V1, ""),
    ("science 1e4", 4, "AR-weak", 400, 10, V1, ""), ("science 1e4", 4, "AR-weak", 800, 10, V1, ""),
    ("science 1e4", 4, "IND", 100, 5, V1, ""), ("science 1e4", 4, "IND", 200, 5, V1, ""), ("science 1e4", 4, "IND", 400, 5, V1, ""),
    ("science 1e4", 4, "BLK", 100, 5, V1, ""), ("science 1e4", 4, "BLK", 200, 5, V1, ""), ("science 1e4", 4, "BLK", 400, 5, V1, ""),
    ("science 1e4", 4, "ADJ-OPP", 200, 5, V1, "mandatory (Sol F7)"), ("science 1e4", 4, "ADJ-OPP", 400, 5, V1, "mandatory (Sol F7)"),
    ("science 1e4", 4, "NULL", 200, 5, V1, "null control"),
    # A3: every A3 fit is paired with the default-partition V fit (seed 1) on the same data: AR n = 200 has 10 reps,
    # BLK n = 200 has 5, so A3 is 10 AR + 5 BLK (PR #19 MAJOR-2; expand() asserts the pairing)
    ("science 1e4", 4, "AR", 200, 10, A3, "A3: exact complete linkage vs the 1M rule on the same data (AR)"),
    ("science 1e4", 4, "BLK", 200, 5, A3, "A3: exact complete linkage vs the 1M rule on the same data (BLK)"),
    # --- 10⁵ rung (12 fits)
    ("rung 1e5", 5, "AR", 200, 5, V1, "n-trend; pi(S0) trend gates option D"), ("rung 1e5", 5, "AR", 400, 3, V1, "n-trend"),
    ("rung 1e5", 5, "IND", 200, 2, V1, ""), ("rung 1e5", 5, "ADJ-OPP", 200, 2, V1, "mandatory (Sol F7)"),
    # --- 10⁶ rung (OD-14 / D-10): rep 1 is the pilot (counts only if the frozen configuration is unchanged)
    ("rung 1e6", 6, "AR", 200, 3, V1, "rep 1 = pilot"), ("rung 1e6", 6, "ADJ-OPP", 200, 1, V1, ""),
    ("rung 1e6", 6, "AR", 200, 1, [{"mode": "V", "seeds": 1, "N": 5000, "tag": "N5000"}], "self-check: N = 5,000 on AR rep 1's data (H-9)"),
    # H-10: AR-weak at 1M bought back as the LAST-released cell, gated: runs only after T5 prices M and the re-sized total
    # (including M) stays <= the H-9 envelope (~28.3k); otherwise it drops again automatically.
    ("rung 1e6 gated-H10", 6, "AR-weak", 200, 1, V1, "GATED H-10: last released; only if the post-T5 total incl. M <= 28.3k"),
    ("option D", 6, "AR", 1000, 1, V1, "conditional on the 10⁵ pi(S0) trend (H-1)"),
]
# block-level costs not expanded into fits (PLANNING VALUES; ENGINEERING_SPEC §0-v2.8 and REVIEW_disposition_sol)
FIXED = OrderedDict([
    ("gates + benchmarks (T1–T11 on NOTS, G0)", 400.0),
    ("T5 end-to-end NOTS gate (Sol F3)", 200.0),
    ("5k anchor (revision D unmodified vs new engine compat vs V; 20-seed law test at 2k)", 300.0),
    ("ablations (start mode / + LS0 / pilot + local) once per distinct 10⁴–10⁶ dataset (ESTIMATE 6% of its V fit)", None),   # computed
    ("competitors (all rungs) + acceptance runs (Sol F8)", 400.0),
])
OPTIONAL = [("1M second seed on AR rep 1 (Sol F7: named, NOT in A + D)", 963.0 * RESIZE_6),
]
CONTINGENCY = 0.25


def expand():
    """One row per distinct fit. A fit that two blocks name (same data seed, mode, arm and engine seed; e.g. an overlap
    dataset that is also a 10⁴-science replicate) is run once, costed to the first block, and noted in the second."""
    rows = []; seen = {}
    for block, rung, design, n, reps, arms, note in CELLS:
        dcode = DESIGN_CODE[design]
        assert 1 <= reps <= MAX_REP, "seed rule: rep must be in 1..%d (%s %s n=%d)" % (MAX_REP, block, design, n)
        assert n % 100 == 0 and 1 <= n // 100 <= 99 and 1 <= dcode <= 9 and 1 <= rung <= 9, "seed rule field out of range"
        for rep in range(1, reps + 1):
            data_seed = rung * 10**8 + dcode * 10**6 + (n // 100) * 10**4 + rep
            for arm in arms:
                assert arm.get("seeds", 1) <= 2
                for s in range(1, arm.get("seeds", 1) + 1):
                    N = arm.get("N", 2500); isl = arm.get("islands", 16)
                    if N == "N0":
                        N = n0(n, 25 if rung == 1 else 10**rung)
                    cost = arm["fixed_cost"] if "fixed_cost" in arm else fit_cost(rung, n, arm["mode"], N, isl)
                    params = dict(arm.get("params") or {})
                    if "prec_arm" in arm:
                        assert s == 1 and 0 <= arm["prec_arm"] <= 9
                        seed = data_seed + 100 * (K_PREC_FINAL + arm["prec_arm"])
                        params["calib_seed"] = data_seed + 100 * (K_PREC_CALIB + arm["prec_arm"])
                    else:
                        seed = data_seed + (100 * K_SEED2 if s == 2 else 0)
                    p = 25 if rung == 1 else 10**rung   # (the 5k anchor is block-costed, no rung-3 cell)
                    gdesign = "AR" if design == "AR-weak" else design
                    signal = "weak" if design == "AR-weak" else ("null" if design == "NULL" else "strong")
                    rid = "%s-%s-n%d-r%02d-%s-s%d" % ({1: "x", 4: "4", 5: "5", 6: "6"}[rung], design.replace("-", ""), n, rep, arm["tag"], s)
                    if rid in seen:
                        seen[rid]["note"] = (seen[rid]["note"] + "; " if seen[rid]["note"] else "") + "also " + block
                        continue
                    rows.append(OrderedDict([
                        ("block", block), ("run_id", rid), ("p", p), ("design", gdesign), ("signal", signal), ("n", n), ("rep", rep),
                        ("mode", arm["mode"]), ("N", N), ("Rp", isl), ("data_seed", data_seed),
                        ("seed", seed), ("params", json.dumps(params, sort_keys=True)),
                        ("core_h_planning", round(cost, 1)), ("note", note)]))
                    seen[rid] = rows[-1]
    ids = [r["run_id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate run ids"
    for r in rows:
        assert 1 <= r["seed"] <= 2**31 - 1 and 1 <= r["data_seed"] <= 2**31 - 1
    check_seeds(rows)
    check_a3_pairing(rows)
    check_theory_arms(rows)
    return rows


def check_seeds(rows):
    """PR #19 MAJOR-1 / MINOR-5: the only shared seed values are the intended pairings.
    - data seeds, seed-2 values, precision final seeds and calibration seeds are pairwise disjoint sets;
    - every precision fit has its own (seed, calib_seed), shared with no other fit (incl. the overlap T / V and A3 fits);
    - a (data seed, engine seed) pair is shared only by fits of the same dataset whose engine seed is seed 1 or seed 2
      (T vs V, A3 vs the default partition, the 1M N = 5,000 self-check (H-9)): never by a precision arm."""
    data = {r["data_seed"] for r in rows}
    s2 = {r["seed"] for r in rows if r["seed"] == r["data_seed"] + 100 * K_SEED2}
    prec = [r for r in rows if r["block"] == "precision"]
    pf = [r["seed"] for r in prec]
    pc = [json.loads(r["params"])["calib_seed"] for r in prec]
    assert len(set(pf)) == len(pf) and len(set(pc)) == len(pc), "precision seeds repeat across arms"
    sets = {"data": data, "seed2": s2, "prec_final": set(pf), "prec_calib": set(pc)}
    names = list(sets)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            assert not (sets[a] & sets[b]), "seed collision between %s and %s: %s" % (a, b, sorted(sets[a] & sets[b])[:5])
    for r in rows:   # every engine seed is the data seed itself, seed 2, or a precision final seed of this dataset
        k, rest = divmod(r["seed"] - r["data_seed"], 100)
        assert rest == 0 and (k in (0, K_SEED2) or (r["block"] == "precision" and K_PREC_FINAL <= k < K_PREC_CALIB)), r["run_id"]
    pairs = {}
    for r in rows:
        pairs.setdefault((r["data_seed"], r["seed"]), []).append(r)
    for key, rs in pairs.items():
        if len(rs) > 1:
            assert not any(r["block"] == "precision" for r in rs), "precision fit shares a seed: %s" % [r["run_id"] for r in rs]
    return True


def check_a3_pairing(rows):
    """PR #19 MAJOR-2: every A3 (exact-linkage) fit has a default-partition V fit (seed 1, N = 2,500, R' = 16) on the
    same data, so the A3 comparison is paired."""
    default = {r["data_seed"] for r in rows if r["mode"] == "V" and r["N"] == 2500 and r["Rp"] == 16 and r["seed"] == r["data_seed"]
               and "partition" not in json.loads(r["params"]) and r["block"] != "T8 exact"}
    unpaired = [r["run_id"] for r in rows if "A3" in r["run_id"] and r["data_seed"] not in default]
    assert not unpaired, "A3 fits without a default-partition V fit on the same data: %s" % unpaired
    return True


def summary(rows):
    blocks = OrderedDict()
    for r in rows:
        b = blocks.setdefault(r["block"], {"fits": 0, "core_h": 0.0})
        b["fits"] += 1; b["core_h"] += r["core_h_planning"]
    fixed = OrderedDict(FIXED)
    ds = {}
    for r in rows:   # one ablation set per distinct dataset (data seed), costed at 6% of a V fit there (pilot ≈ 1/19, setup shared)
        if r["block"] in ("T8 exact", "option D", "precision") or r["mode"] != "V" or r["Rp"] != 16 or r["N"] != 2500:
            continue
        ds[r["data_seed"]] = r["core_h_planning"]
    fixed["ablations (start mode / + LS0 / pilot + local) once per distinct 10⁴–10⁶ dataset (ESTIMATE 6% of its V fit)"] = round(0.06 * sum(ds.values()), 1)
    planned = sum(v["core_h"] for k, v in blocks.items() if k != "option D") + sum(fixed.values())
    d = blocks.get("option D", {"core_h": 0.0})["core_h"]
    return blocks, fixed, planned, d


def rung_to_p(only):
    """--only RUNG: 4|5|6 (log10 p, as in the run ids), 1e4|1e5|1e6, or p itself (10000, ...)."""
    s = str(only).strip().lower()
    if s.isdigit() and len(s) == 1:
        return 10 ** int(s)
    if s.startswith("1e") and s[2:].isdigit():
        return 10 ** int(s[2:])
    if s.isdigit():
        return int(s)
    raise ValueError("--only: expected a rung 4|5|6, 1e4|1e5|1e6 or p, got %r" % only)


def plans(rows, outdir, only=None, code_commit=None):
    """Driver plans: one per (block, p, n, mode, N, Rp) group, split so that each batch has <= 150 tasks. code_commit is
    the engine commit (40 hex, see verify_freeze); None writes the placeholder UNSET-fill-at-freeze (development, tests).
    Every plan also carries method_tag and core_tree (FREEZE)."""
    assert code_commit is None or HEX40.match(code_commit), "code_commit must be 40 hex, got %r" % (code_commit,)
    os.makedirs(outdir, exist_ok=True)
    groups = OrderedDict()
    only_p = rung_to_p(only) if only else None
    for r in rows:
        if r["block"] == "T8 exact" or (only_p is not None and r["p"] != only_p):
            continue
        key = (r["block"], r["p"], r["n"], r["mode"], r["N"], r["Rp"])
        groups.setdefault(key, []).append(r)
    written = []
    for (block, p, n, mode, N, Rp), rs in groups.items():
        per_fit = 4 + Rp
        cap = max(1, 150 // per_fit)
        for b in range(0, len(rs), cap):
            chunk = rs[b:b + cap]
            name = "%s_p%d_n%d_%s_N%d_R%d_b%d" % (block.replace(" ", "").replace("⁴", "4").replace("⁵", "5").replace("⁶", "6"), p, n, mode, N, Rp, b // cap + 1)
            shape = PLAN_RESOURCES.get((block, mode), {})
            plan = {"batch": name[:64], "mode": mode, "code_commit": code_commit or UNSET_COMMIT,
                    "method_tag": FREEZE["method_tag"], "core_tree": FREEZE["core_tree"], "binary": "bin/smcbvs4",
                    "max_task_hours": shape.get("max_task_hours", 2.0),
                    **({"island_isa": "sapphirerapids"} if mode == "V" else {}),   # D-32: V plans need an FMA island ISA
                    "kind": "gated (needs HQ go)", **({"resources": shape["resources"]} if shape else {}), "fits": []}
            for r in chunk:
                f = {"run_id": r["run_id"], "design": "NULL" if r["signal"] == "null" else r["design"], "p": r["p"], "n": r["n"],
                     "signal": r["signal"], "data_seed": r["data_seed"], "seed": r["seed"], "Rp": r["Rp"], "N": r["N"]}
                pr = json.loads(r["params"])
                if pr:
                    f["params"] = pr
                plan["fits"].append(f)
            # core_h_cap is a required plan key (the driver refuses a plan without it: a missing or misspelt cap must not mean
            # "no cap"): the plan's own worst case, rounded up, so a later change of any limit trips the guard and needs a new cap
            import p1m_driver
            wc = p1m_driver.resolve(dict(plan, core_h_cap=1e12))["worst_case_core_h"]
            plan = {**{k: v for k, v in plan.items() if k != "fits"}, "core_h_cap": math.ceil(wc + 0.05), "fits": plan["fits"]}
            path = os.path.join(outdir, name[:64] + ".json")
            with open(path, "w") as fh:
                json.dump(plan, fh, indent=1)
            written.append(path)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tsv"); ap.add_argument("--plans"); ap.add_argument("--only", metavar="RUNG", help="4|5|6 (log10 p), 1e4|1e5|1e6, or p"); ap.add_argument("--summary", action="store_true")
    ap.add_argument("--code-commit", default="HEAD", metavar="REV", help="engine commit the plans pin (default HEAD); verified against the freeze")
    ap.add_argument("--no-freeze-check", action="store_true", help="development/tests: skip the freeze check, write code_commit %s" % UNSET_COMMIT)
    a = ap.parse_args(argv)
    rows = expand()
    if a.tsv:
        with open(a.tsv, "w") as fh:
            fh.write("\t".join(rows[0].keys()) + "\n")
            for r in rows:
                fh.write("\t".join(str(v) for v in r.values()) + "\n")
    if a.plans:
        commit = None
        if not a.no_freeze_check:
            try:
                commit = verify_freeze(a.code_commit)
            except ValueError as e:
                print("freeze check failed: %s" % e, file=sys.stderr)
                return 65
        w = plans(rows, a.plans, a.only, commit)
        print("wrote %d driver plans to %s; code_commit %s, method_tag %s, core_tree %s"
              % (len(w), a.plans, commit or UNSET_COMMIT, FREEZE["method_tag"], FREEZE["core_tree"][:12]))
        print("plan set sha256 %s (code_commit masked: %s)" % (plan_set_digest(w), plan_set_digest(w, True)))
    if a.summary or not (a.tsv or a.plans):
        blocks, fixed, planned, d = summary(rows)
        print("%-14s %6s %10s" % ("block", "fits", "core-h"))
        for k, v in blocks.items():
            print("%-14s %6d %10.0f" % (k, v["fits"], v["core_h"]))
        for k, v in fixed.items():
            print("  + %-88s %8.0f" % (k, v))
        print("planned (excl. option D): %.0f; with %d%% contingency: %.0f" % (planned, CONTINGENCY * 100, planned * (1 + CONTINGENCY)))
        print("option D: %.0f; with contingency: %.0f" % (d, d * (1 + CONTINGENCY)))
        print("A + D with contingency: %.0f (H-9 envelope ~28.3k; H-1 was ~24.6k)" % ((planned + d) * (1 + CONTINGENCY)))
        for k, v in OPTIONAL:
            print("optional, not in the total: %s %.0f" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
