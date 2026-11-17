"""DEPS.tsv by hand (PROTOCOL_v4 §4.1; deps.py not yet written). sha = first 16 hex of sha256 of the span's text.
Usage: python3 deps_hand.py [--check ID=REVIEWFILE ...]  -> rewrites DEPS.tsv; an ID marked checked takes its current sha
as checked_sha. Existing checked_sha / checked_by are kept; state = OK if sha == checked_sha, STALE if differs, else UNCHECKED."""
import csv, hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # id, file, a, b, uses
    ("S:setting", "STATEMENT.md", 14, 27, ""),
    ("S:Thm2X", "STATEMENT.md", 29, 48, "S:setting,S:det"),
    ("S:Cor2X", "STATEMENT.md", 50, 58, "S:Thm2X"),
    ("S:det", "STATEMENT.md", 60, 63, "S:setting"),
    ("S:inputs", "STATEMENT.md", 76, 84, ""),
    ("P:P0", "PROOF.md", 7, 17, "S:det"),
    ("P:P1", "PROOF.md", 18, 53, "S:setting,S:Thm2X,S:inputs"),
    ("P:P2", "PROOF.md", 54, 59, "P:P0,P:P1"),
    ("P:P3", "PROOF.md", 60, 80, "S:Cor2X,P:P2"),
    ("R:registry", "REPORT.md", None, None, "S:Thm2X,S:Cor2X"),
]
def span(f, a, b):
    L = open(os.path.join(HERE, f), encoding="utf-8").read().split("\n")
    if a is None:
        i = next(k for k, l in enumerate(L) if l.startswith("## 6. Registry blocks")); a, b = i + 1, len(L)
    return "\n".join(L[a - 1:b]), a, b
old = {}
p = os.path.join(HERE, "DEPS.tsv")
if os.path.exists(p):
    old = {r["id"]: r for r in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")}
marks = dict(x.split("=", 1) for x in sys.argv[1:] if "=" in x)
out = ["id\tfile[:lines]\tuses\tsha\tchecked_sha\tchecked_by\tstate"]
for rid, f, a, b, uses in ROWS:
    t, a, b = span(f, a, b)
    sha = hashlib.sha256(t.encode()).hexdigest()[:16]
    o = old.get(rid, {})
    csha, cby = o.get("checked_sha", ""), o.get("checked_by", "")
    if rid in marks:
        csha, cby = sha, marks[rid]
    state = "OK" if csha == sha else ("STALE" if csha else "UNCHECKED")
    out.append(f"{rid}\t{f}:{a}-{b}\t{uses}\t{sha}\t{csha}\t{cby}\t{state}")
open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
