"""W3-T03ACC: hand-kept DEPS helper (v4 H4: until deps.py exists). Standard library only.
Recomputes `sha` (sha256 of the cited line block, first 16 hex) for every row of DEPS.tsv and derives `state`:
OK (sha == checked_sha and checked_by names a file that exists), UNCHECKED (no checked_sha), STALE (sha != checked_sha),
REFUTED (state already REFUTED), DOWNSTREAM (a `uses` row is not OK). Usage: python deps_hash.py [--write]"""
import csv, hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(HERE, "DEPS.tsv")
def block(ref):
    f, _, lines = ref.partition(":"); path = os.path.join(HERE, f)
    if not os.path.isfile(path): path = os.path.join(ROOT, f)
    data = open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    if lines:
        a, _, b = lines.partition("-"); a = int(a); b = int(b or a); data = data[a - 1:b]
    return hashlib.sha256("\n".join(data).encode()).hexdigest()[:16]
rows = list(csv.DictReader(open(P, encoding="utf-8"), delimiter="\t"))
for r in rows:
    r["sha"] = block(r["file"])
    if r["state"] == "REFUTED": continue
    ok = r["checked_sha"] and r["checked_sha"] == r["sha"] and r["checked_by"] and \
        os.path.isfile(os.path.join(HERE, r["checked_by"].split("#")[0]))
    r["state"] = "OK" if ok else ("UNCHECKED" if not r["checked_sha"] else "STALE")
byid = {r["id"]: r for r in rows}
for r in rows:
    if r["state"] == "OK" and any(byid[u]["state"] != "OK" for u in r["uses"].split(";") if u in byid):
        r["state"] = "DOWNSTREAM"
w = csv.DictWriter(sys.stdout if "--write" not in sys.argv else open(P, "w", encoding="utf-8", newline=""),
                   fieldnames=["id", "file", "uses", "sha", "checked_sha", "checked_by", "state"], delimiter="\t",
                   lineterminator="\n")
w.writeheader(); w.writerows(rows)
