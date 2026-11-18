#!/usr/bin/env python3
"""verify_accepted.py -- `manifest.py verify` over EVERY accepted manifest (theory-ci step `manifests`, prepush gate).

The set is the one check.py counts for acceptance: the council digest (`MANIFEST <64-hex>`) of every ACTIVE claim that
has an accept record, resolved to the ticket's reviews/MANIFEST_*.txt by bvsreg.ticket_dir (the path council_problems /
manifest_problems use), and verified with the library call of Wave3/tools/manifest.py (`verify_problems`, i.e.
exactly `manifest.py verify <ticket> <manifest>`). A manifest that no longer verifies on the current tree fails the run
(exit 1) and is named with every file whose hash differs (CHANGED / REMOVED / ADDED), the rows citing it, and the
command to reproduce. Read-only; no override.

  python verify_accepted.py [--list]      (--list: also print the manifests that verify)
Exit: 0 every accepted manifest verifies; 1 at least one fails or is missing; 2 tool error.
"""
from __future__ import annotations

import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402


def main() -> int:
    show_ok = "--list" in sys.argv[1:]
    try:
        M = R.manifest_tool()
        rows = R.load_claims()
        rec = R.accept_records()
        folder = R.ticket_folders()
    except Exception as e:  # pragma: no cover
        print(f"verify_accepted: cannot load the registry / manifest tool: {e!r}")
        return 2
    groups: dict[tuple[str, str], list[str]] = {}
    n_rows = 0
    for r in rows:
        if r.get("state") != "ACTIVE" or not rec.get(r["id"]):
            continue
        digs = re.findall(r"MANIFEST ([0-9a-f]{64})", r.get("council") or "")
        if not digs:
            continue
        n_rows += 1
        groups.setdefault((R.ticket_dir(r, folder.get(r.get("ticket", ""), "")), digs[0]), []).append(r["id"])
    bad: list[str] = []
    nver = 0
    for (d, dg), ids in sorted(groups.items()):
        found = []
        mdir = os.path.join(R.ROOT, d, "reviews")
        for fn in sorted(os.listdir(mdir)) if os.path.isdir(mdir) else []:
            if fn.startswith("MANIFEST_") and fn.endswith(".txt"):
                mp = os.path.join(mdir, fn)
                try:
                    with open(mp, encoding="utf-8") as fh:
                        head = fh.readline().strip()
                except OSError:
                    continue
                if head == f"MANIFEST {dg}":
                    found.append(mp)
        cited = f"cited by {len(ids)} accepted row(s): {', '.join(ids[:4])}{' ...' if len(ids) > 4 else ''}"
        if not found:
            bad.append(f"FAIL {d}/reviews: no MANIFEST_*.txt has the header `MANIFEST {dg[:12]}...` ({cited})")
            continue
        for mp in found:
            rel = os.path.relpath(mp, R.ROOT).replace(os.sep, "/")
            try:
                _, diffs = M.verify_problems(os.path.join(R.ROOT, d), mp, R.ROOT)
            except M.ManifestError as e:
                diffs = [str(e)]
            if diffs:
                bad.append(f"FAIL {rel} (MANIFEST {dg[:12]}..., {cited}):\n    " + "\n    ".join(diffs)
                           + f"\n    reproduce: python Theory_work/Wave3/tools/manifest.py verify {d} {rel}")
            else:
                nver += 1
                if show_ok:
                    print(f"ok   {rel} ({cited})")
    print(f"verify_accepted: {len(groups)} accepted manifest digest(s) from {n_rows} accepted row(s); "
          f"{nver} verify, {len(bad)} FAIL")
    for b in bad:
        print(b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
