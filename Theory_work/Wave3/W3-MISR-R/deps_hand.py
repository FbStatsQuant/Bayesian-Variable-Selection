#!/usr/bin/env python3
"""Hand-kept DEPS.tsv for W3-MISR-R (PROTOCOL_v4 §4.1 and H4: kept by hand with sha256 until deps.py exists).

ROWS below is edited by hand; `checked_sha`/`checked_by` are filled from review dispositions.
sha = first 16 hex of sha256 of the cited line range (bytes of those lines incl. newlines) or of the whole file.
state: OK (sha == checked_sha), UNCHECKED, STALE (edited since check), DOWNSTREAM (uses a row that is not OK).
Usage (from this folder): python3 deps_hand.py  -> writes DEPS.tsv and prints it.
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# id, file (relative to this folder), lines "a-b" or "", uses, checked_sha, checked_by
ROWS = [
    ("S:notation", "STATEMENT.md", "25-46", "", "3a025174ce55c22e", "reviews/K1_linecheck_sol.md"),
    ("S:CorG-min", "STATEMENT.md", "48-92", "S:notation", "97b1ed2602f41b3b", "reviews/K1_linecheck_sol.md"),
    ("S:CorGb-plus", "STATEMENT.md", "94-108", "S:CorG-min", "3b27ea0d061b648c", "reviews/K1_linecheck_sol.md"),
    ("S:CorH-plus", "STATEMENT.md", "110-132", "S:notation,S:CorG-min", "55e295180dcc9662", "reviews/K1_linecheck_sol.md"),
    ("S:CorH-U", "STATEMENT.md", "134-155", "S:CorH-plus,S:CorGb-plus", "533cc312b9632e27", "reviews/K1_linecheck_sol.md"),
    ("S:inputs-deps", "STATEMENT.md", "164-205", "", "2b1ceff43dd69cd8", "reviews/K1_linecheck_sol.md"),
    ("L:G1_min", "lemmas/G1_min.md", "", "S:CorG-min", "4915f1f44e6d09a8", "reviews/K1_linecheck_sol.md"),
    ("L:G2_corr", "lemmas/G2_corr.md", "", "S:CorGb-plus,L:G1_min", "3fea96051b137a2e", "reviews/K1_linecheck_sol.md"),
    ("L:H1_plus", "lemmas/H1_plus.md", "", "S:CorH-plus,L:G1_min", "697ee1475af3f701", "reviews/K1_linecheck_sol.md + reviews/K2_recheck_sol.md"),
    ("L:H2_uniform", "lemmas/H2_uniform.md", "", "S:CorH-U,L:H1_plus,L:G2_corr", "7757a8986d5306c9", "reviews/K1_linecheck_sol.md + reviews/K2_recheck_sol.md"),
]


def sha(path, lines):
    with open(os.path.join(HERE, path), "rb") as f:
        data = f.read()
    if lines:
        a, b = (int(t) for t in lines.split("-"))
        data = b"".join(data.splitlines(keepends=True)[a - 1:b])
    return hashlib.sha256(data).hexdigest()[:16]


def main():
    out = ["id\tfile[:lines]\tuses\tsha\tchecked_sha\tchecked_by\tstate"]
    state = {}
    rows = []
    for rid, path, lines, uses, csha, cby in ROWS:
        s = sha(path, lines)
        st = "UNCHECKED" if not csha else ("OK" if csha == s else "STALE")
        state[rid] = st
        rows.append([rid, path + (":" + lines if lines else ""), uses, s, csha, cby, st])
    for r in rows:
        if r[6] == "OK" and any(state.get(u) != "OK" for u in r[2].split(",") if u):
            r[6] = "DOWNSTREAM"
        out.append("\t".join(r))
    with open(os.path.join(HERE, "DEPS.tsv"), "w") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
