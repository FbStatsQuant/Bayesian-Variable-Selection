#!/usr/bin/env python3
"""gc_fence.py -- the ISLANDS ALLOW-LIST FENCE and the NOTS-side deleter for the 1M block's Tier-1 cleanup (HQ H-56, approved (b); GC_PLAN §5 class C + the A / A+ duplicates). Stdlib only.
FENCE: only these paths, relative to /home/fb31/SMC_Engineering_Department/scratch/runs (fb31's department run dirs), batches GC_* only, exactly <GC_batch>/<run_id>/<name> with
  island_1..16.bin (class C), fit.bin / law.bin / eval.bin (class A), setup.bin ONLY for the A+ runs (the pilot, option D, ADJ-OPP r01). No other file name, no deeper path, no '..', no absolute path, no symlink, no other batch family
  (PL_ OV_ VN_ GB_ RG_ T5_ ...), nothing outside that root (no SMC_BVS_v3 deploy folder, /projects/ml75, $WORK, BNP, home).
NOTS deleter (`python3 -I gc_fence.py --plan plan.json [--apply]`): per row re-checks the fence, the realpath under the root, regular file and not a symlink, the size, (islands) the mtime_ns recorded by the V4 check, (A / A+) the sha256 of the file == the sha256 of the sha-verified desktop copy; a row that fails ANY check is REFUSED and kept. Default = dry run."""
import hashlib, json, os, re, sys
ROOT = "/home/fb31/SMC_Engineering_Department/scratch/runs"
A_PLUS = {("GC_P", "6-AR-n200-r01-V-s1"), ("GC_D", "6-AR-n1000-r01-V-s1"), ("GC_W1", "6-ADJOPP-n200-r01-V-s1")}   # setup.bin kept on the desktop (A+): the NOTS copies may go
_BATCH = r"GC_[A-Za-z0-9]+"; _RUN = r"6-[A-Za-z0-9-]+"
RE_ISL = re.compile(r"^(%s)/(%s)/(island_(?:[1-9]|1[0-6])\.bin)$" % (_BATCH, _RUN))
RE_A = re.compile(r"^(%s)/(%s)/((?:fit|law|eval|setup)\.bin)$" % (_BATCH, _RUN))

def fence_kind(rel):
    """rel = path relative to ROOT. Returns 'island' / 'A' / 'A+' or None (REFUSED)."""
    if not isinstance(rel, str) or not rel or rel.startswith("/") or "\\" in rel or "\0" in rel or ".." in rel.split("/") or "//" in rel or rel != os.path.normpath(rel): return None
    m = RE_ISL.match(rel)
    if m: return "island"
    m = RE_A.match(rel)
    if m:
        if m.group(3) == "setup.bin": return "A+" if (m.group(1), m.group(2)) in A_PLUS else None
        return "A"
    return None

def fence_abs(path):
    """absolute path -> kind or None (must lie under ROOT)"""
    if not isinstance(path, str) or not path.startswith(ROOT + "/"): return None
    return fence_kind(path[len(ROOT) + 1:])

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()

def delete_rows(rows, root=ROOT, apply=False):
    """rows: [{rel, kind, size, mtime_ns (islands), sha256 (A / A+ and T2THR island), why}] -> list of result dicts {rel, status: DELETED | WOULD_DELETE | REFUSED, reason}"""
    res = []
    for r in rows:
        rel = r.get("rel"); kind = fence_kind(rel); out = {"rel": rel, "size": r.get("size"), "kind": kind}
        def refuse(why): out.update(status="REFUSED", reason=why); res.append(out)
        if kind is None: refuse("outside the fence"); continue
        if r.get("kind") not in (None, kind): refuse("kind mismatch %s != %s" % (r.get("kind"), kind)); continue
        p = os.path.join(root, rel)
        if os.path.islink(p): refuse("symlink"); continue
        if os.path.realpath(p) != os.path.join(os.path.realpath(root), rel): refuse("realpath leaves the fence"); continue
        if not os.path.isfile(p): refuse("not a regular file / missing"); continue
        st = os.stat(p)
        if st.st_size != r.get("size"): refuse("size %d != %s" % (st.st_size, r.get("size"))); continue
        if kind == "island" and r.get("mtime_ns") is not None and st.st_mtime_ns != r["mtime_ns"]: refuse("mtime changed since the V4 check"); continue
        if kind == "island" and r.get("mtime_ns") is None and not r.get("sha256"): refuse("island row without V4 mtime or sha"); continue
        if kind in ("A", "A+") and not r.get("sha256"): refuse("no desktop sha256 for an A / A+ file"); continue
        if r.get("sha256"):
            g = sha256(p)
            if g != r["sha256"]: refuse("sha256 %s != desktop %s" % (g[:12], r["sha256"][:12])); continue
        if apply:
            os.remove(p); out.update(status="DELETED", reason=r.get("why", ""))
        else: out.update(status="WOULD_DELETE", reason=r.get("why", ""))
        res.append(out)
    return res

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--plan" not in a: sys.exit("usage: gc_fence.py --plan plan.json [--apply]")
    rows = json.load(open(a[a.index("--plan") + 1])); apply = "--apply" in a
    res = delete_rows(rows, ROOT, apply)
    json.dump(res, sys.stdout)
