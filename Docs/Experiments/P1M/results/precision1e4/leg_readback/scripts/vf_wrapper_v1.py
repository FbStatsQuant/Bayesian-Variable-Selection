#!/usr/bin/env python3
"""vf_wrapper.py -- thin input builder for ADDENDUM_2_VF (precision1e4 leg read-back).

compare_overlap_v2.py (sha256 4f402e51...) accepts only run ids ...-(T|V)-sN and takes the id from run_manifest.json.  The 14 VF fits are
named ...-VF-sN.  This wrapper builds scratch input trees in which every VF run dir is presented under the overlap's V name: a real dir whose
entries are symlinks to the collected files, except run_manifest.json, which is a copy with run_id rewritten (VF -> V).  Nothing else is
changed; the scorer is run UNCHANGED on the trees.  Records are never written to.

Trees (all under --out):
  vf_pairs/   20 overlap T fits + the 14 VF fits (as V)               -> wave-check: the 14 VF pairs (the other T fits find no V and are skipped)
  v3_pairs/   20 overlap T fits + the 20 overlap V fits (I_max = 3)    -> wave-check / full mode on the overlap's own V (the I_max = 3 result beside VF)
  mixed40/    20 overlap T fits + 14 VF (as V) + the 6 overlap V fits that have no VF twin (stay as the I_max = 3 record, ADDENDUM_2_VF)  -> full mode
T and overlap-V dirs are symlinked as they are (find_runs resolves duplicates .T2/.V2 by the eval mtime, as in the overlap verdict).
"""
import argparse, json, os, re, sys

OV = os.path.expanduser("~/SMC_Engineering_Department/records/overlap1e4")
PR = os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4")
RUN = re.compile(r"^4-(?P<d>[A-Za-z]+)-n200-r(?P<r>\d+)-(?P<arm>T|V)-s(?P<s>\d+)$")
VF = re.compile(r"^4-(?P<d>[A-Za-z]+)-n200-r(?P<r>\d+)-VF-s(?P<s>\d+)$")


def jload(p):
    with open(p) as fh:
        return json.load(fh)


def rid_of(dp):
    mp = os.path.join(dp, "run_manifest.json")
    if os.path.isfile(mp):
        try:
            r = jload(mp).get("run_id")
            if r:
                return r
        except Exception:
            pass
    return os.path.basename(dp)


def overlap_dirs():
    out = []   # (dirpath, run_id)
    for w in ("W0", "W1", "W2", "W3"):
        base = os.path.join(OV, w)
        for n in sorted(os.listdir(base)):
            dp = os.path.join(base, n)
            if n.startswith("_batch") or not os.path.isdir(dp):
                continue
            out.append((dp, rid_of(dp), w, n))
    return out


def link_dir(src, dst):
    os.symlink(src, dst)


def present_as_V(src, dst, new_id):
    os.makedirs(dst)
    for n in sorted(os.listdir(src)):
        if n == "run_manifest.json":
            m = jload(os.path.join(src, n))
            assert m.get("run_id") and "-VF-" in m["run_id"], (src, m.get("run_id"))
            m["run_id"] = new_id
            with open(os.path.join(dst, n), "w") as fh:
                json.dump(m, fh, indent=1)
        else:
            os.symlink(os.path.join(src, n), os.path.join(dst, n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ovl = overlap_dirs()
    T = [(dp, rid, w, n) for dp, rid, w, n in ovl if RUN.match(rid) and RUN.match(rid).group("arm") == "T"]
    V = [(dp, rid, w, n) for dp, rid, w, n in ovl if RUN.match(rid) and RUN.match(rid).group("arm") == "V"]
    # VF fits of the leg
    vf = {}
    for w in ("S1", "S2"):
        for n in sorted(os.listdir(os.path.join(PR, w))):
            m = VF.match(n)
            if m:
                vf[n] = os.path.join(PR, w, n)
    assert len(vf) == 14, len(vf)
    vf_as_v = {n.replace("-VF-", "-V-"): dp for n, dp in vf.items()}
    twin_ids = set(vf_as_v)
    v_ids = {rid for _, rid, _, _ in V}
    assert twin_ids <= v_ids, sorted(twin_ids - v_ids)
    notwin = [(dp, rid, w, n) for dp, rid, w, n in V if rid not in twin_ids]
    assert len({rid for _, rid, _, _ in notwin}) == 6, len(notwin)
    for tree, parts in (("vf_pairs", "T+VF"), ("v3_pairs", "T+V"), ("mixed40", "T+VF+Vnotwin")):
        root = os.path.join(a.out, tree)
        os.makedirs(root, exist_ok=False)
        for dp, rid, w, n in T:
            link_dir(dp, os.path.join(root, "%s__%s" % (w, n)))
        if parts == "T+V":
            for dp, rid, w, n in V:
                link_dir(dp, os.path.join(root, "%s__%s" % (w, n)))
        else:
            for vid, dp in sorted(vf_as_v.items()):
                present_as_V(dp, os.path.join(root, "VF__" + vid), vid)
            if parts == "T+VF+Vnotwin":
                for dp, rid, w, n in notwin:
                    link_dir(dp, os.path.join(root, "%s__%s" % (w, n)))
        print(tree, len(os.listdir(root)), "entries")


if __name__ == "__main__":
    sys.exit(main())
