"""DEPS.tsv by hand (PROTOCOL_v4 §4.1; pattern of W3-D3/deps_hand.py, spans located by section headers so that edits do not
shift them). sha = first 16 hex of sha256 of the span's text.
Usage: python3 deps_hand.py [ID=REVIEWFILE ...]  -> rewrites DEPS.tsv; an ID given takes its current sha as checked_sha.
Existing checked_sha / checked_by are kept; state = OK if sha == checked_sha, STALE if it differs, else UNCHECKED."""
import csv, hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # id, file, start header prefix, end header prefix (exclusive; None = end of file), uses
    ("S:setting", "STATEMENT.md", "## 0.", "## 1R.", ""),
    ("S:reader", "STATEMENT.md", "## 1R.", "## 1.", "S:Cor-FAMC"),
    ("S:Cor-FAMC", "STATEMENT.md", "## 1.", "## 1b.", "S:setting"),
    ("S:class", "STATEMENT.md", "## 2.", "## 3.", "S:Cor-FAMC"),
    ("S:map", "STATEMENT.md", "## 3.", "## 4.", "S:Cor-FAMC"),
    ("S:inputs", "STATEMENT.md", "## 4.", "## 5.", ""),
    ("P:BLK", "lemmas/A_assembly.md", "## A.1", "## A.2", "S:Cor-FAMC,S:inputs"),
    ("P:AR", "lemmas/A_assembly.md", "## A.2", "## A.3", "S:Cor-FAMC,S:inputs"),
    ("R:registry", "REPORT.md", "## 6. Registry blocks", None, "S:Cor-FAMC"),
]
def span(f, h0, h1):
    L = open(os.path.join(HERE, f), encoding="utf-8").read().split("\n")
    a = next(k for k, l in enumerate(L) if l.startswith(h0))
    b = len(L) if h1 is None else next(k for k in range(a + 1, len(L)) if L[k].startswith(h1))
    while b > a and L[b - 1].strip() == "":
        b -= 1
    return "\n".join(L[a:b]), a + 1, b
old = {}
p = os.path.join(HERE, "DEPS.tsv")
if os.path.exists(p):
    old = {r["id"]: r for r in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")}
marks = dict(x.split("=", 1) for x in sys.argv[1:] if "=" in x)
out = ["id\tfile[:lines]\tuses\tsha\tchecked_sha\tchecked_by\tstate"]
for rid, f, h0, h1, uses in ROWS:
    if not os.path.exists(os.path.join(HERE, f)):
        continue
    t, a, b = span(f, h0, h1)
    sha = hashlib.sha256(t.encode()).hexdigest()[:16]
    o = old.get(rid, {})
    csha, cby = o.get("checked_sha", ""), o.get("checked_by", "")
    if rid in marks:
        csha, cby = sha, marks[rid]
    state = "OK" if csha == sha else ("STALE" if csha else "UNCHECKED")
    out.append(f"{rid}\t{f}:{a}-{b}\t{uses}\t{sha}\t{csha}\t{cby}\t{state}")
open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
