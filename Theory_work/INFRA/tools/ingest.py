"""ingest.py — add new tickets' claims, or split bundled claims, into the LIVE registry (validated, logged).

  ingest.py claims FRAGMENT.jsonl [--apply]
      one claim per line in the transcription schema (registry/fragments/BRIEF.md) plus optional `premises` and
      `strength` keys (Wave 3 REPORT registry block). New ids only; each status must start verbatim (un-negated) on
      its status_source; a missing status is allowed (WARN in check). Adds a tickets.tsv row for unknown tickets.
  ingest.py splits SPLITS.tsv [--apply]
      split spec (registry/fragments/BRIEF_SPLIT.md): `part` rows create child claims; a child without its own
      status gets `UNSPLIT-STATUS: <parent status verbatim>` (checked against the parent's source; never stronger);
      the parent then depends on every part (@stmt) and `implies` it; `repoint` rows move a dependent's edge from
      the parent to the part it uses.
Dry run by default (prints what would change); --apply writes registry files only.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys

sys.dont_write_bytecode = True  # never write __pycache__ (tools must not write outside their outputs)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

UNSPLIT = "UNSPLIT-STATUS: "


def status_ok(status: str, source: str) -> bool:
    if not status:
        return True
    if status.startswith(UNSPLIT):
        status = status[len(UNSPLIT):]
    return R.status_at(status, source) == "ok"


def new_row(cid, **kw):
    r = {c: "" for c in R.COLUMNS}
    t, _, loc = cid.partition(":")
    r.update(id=cid, ticket=t, local_id=loc, version="1.0.0", state="ACTIVE")
    r.update({k: (R.join_list(v) if isinstance(v, list) else (v or "")) for k, v in kw.items()})
    r["sha256"] = R.claim_hash(r) or ""
    r["commit"] = R.git_last_commit(r["file"])
    return r


def ingest_claims(path, apply):
    rows = R.load_claims()
    ids = {r["id"] for r in rows}
    asm = R.load_assumptions()
    sharp = R.load_sharpness()
    tickets = R.load_tickets()
    tk = {t["ticket"] for t in tickets}
    added, problems, new_asm, new_sharp = [], [], [], []
    for n, ln in enumerate(open(path, encoding="utf-8"), 1):
        if not ln.strip():
            continue
        j = json.loads(ln)
        cid = f"{j['ticket']}:{j['local_id']}"
        if cid in ids:
            problems.append(f"{cid}: already registered (use registry.py rehash / correct-status)")
            continue
        span = j.get("lines") or [0, 0]
        st, src = j.get("status", ""), j.get("status_source", "")
        r = new_row(cid, kind=j.get("kind", ""), name=j.get("name", ""), short=j.get("short", ""), file=j["file"],
                    lines=f"{span[0]}-{span[1]}", premises=j.get("premises", []), status=st, status_source=src,
                    evidence=j.get("evidence", []), council=j.get("council", ""), depends_on=j.get("depends_on", []),
                    method=j.get("method", ""), falsification=j.get("falsification", []), notes=j.get("notes", ""))
        if r["kind"] not in R.KINDS:
            problems.append(f"{cid}: kind {r['kind']!r} not in {R.KINDS}")
            continue
        if not r["sha256"]:
            problems.append(f"{cid}: statement/premise span unreadable ({j['file']}:{span})")
            continue
        if not status_ok(st, src):
            problems.append(f"{cid}: status {st[:60]!r} does not start verbatim on {src} ({R.status_at(st, src)})")
            continue
        sgt = j.get("strength") or {}
        if sgt:
            r["headline"] = "yes"
            for k in ("conclusion", "rate", "scope"):
                r[k] = sgt.get(k, "")
            r["implies"] = R.join_list(sgt.get("implies", []))
            items = []
            for a_ in sgt.get("assumptions", []):
                if isinstance(a_, str) and " = " in a_:  # "A:ID = definition" -> a new assumption row
                    i_, _, d_ = a_.partition(" = ")
                    a_ = {"id": i_.strip(), "statement": d_.strip(), "name": i_.strip()[2:],
                          "kind": "property" if i_.strip().startswith("P:") else "assumption"}
                aid = a_["id"] if isinstance(a_, dict) else a_
                items.append(aid)
                if isinstance(a_, dict) and aid.split("~")[0] not in asm and                         aid.split("~")[0] not in {x["id"] for x in new_asm}:
                    new_asm.append(dict(id=aid.split("~")[0], kind=a_.get("kind", "assumption"), shared="no",
                                        name=a_.get("name", ""), statement=a_.get("statement", ""),
                                        source=a_.get("source", ""), implies="", bridge="", version="1.0.0",
                                        notes=f"added by ingest from {os.path.basename(path)}"))
            r["assumptions"] = R.join_list(items)
            known = set(asm) | {x["id"] for x in new_asm}
            for s in sgt.get("sharpness", []):
                if s["assumption"] not in known:
                    problems.append(f"{cid}: sharpness for undefined assumption {s['assumption']!r}")
                    continue
                new_sharp.append(dict(claim=cid, assumption=s["assumption"], verdict=s["verdict"],
                                      evidence=s.get("evidence", ""), notes="ingested"))
            r["gates"] = sgt.get("gates", "")
        added.append(r)
        ids.add(cid)
    newt = sorted({r["ticket"] for r in added} - tk)
    print(f"{len(added)} claim(s) to add; {len(problems)} problem(s); new tickets {newt}; "
          f"{len(new_asm)} new assumption(s); {len(new_sharp)} sharpness row(s)")
    for p in problems:
        print("  PROBLEM", p)
    if not apply:
        print("(dry run: nothing written; add --apply)")
        return
    rows += added
    sharp_all = sharp + new_sharp
    for r in added:
        r["improvable"] = R.improvable(r, sharp_all)
    R.save_claims(rows)
    if new_asm:
        h, A = R.read_tsv(R.ASSUMPTIONS)
        R.write_tsv(R.ASSUMPTIONS, h, A + new_asm)
    if new_sharp:
        R.write_tsv(R.SHARPNESS, R.SHARPNESS_COLUMNS, sharp_all)
    if newt:
        h, T = R.read_tsv(R.TICKETS)
        for t in newt:
            T.append(dict(ticket=t, wave="Wave" + t[1] if t.startswith("W") else "", folder="", result="",
                          result_source="", headline="", sop_row="", branch=f"theory/{t}", kill_budget="",
                          notes="added by ingest; fill folder/result"))
        R.write_tsv(R.TICKETS, h, T)
    for r in added:
        R.log_event("ingest", r["id"], "", f"v1.0.0 {r['status'][:60]}", f"ingested from {os.path.basename(path)}",
                    "INFRA")
    print("written")


def ingest_splits(path, apply):
    rows = R.load_claims()
    by = R.index(rows)
    parts = collections.OrderedDict()
    repoints, problems = [], []
    for c in R.read_tsv(path)[1]:
        if c["kind_of_row"] == "part":
            parts.setdefault((c["parent"], c["id"]), {})[c["field"]] = c.get("value", "")
        elif c["kind_of_row"] == "repoint":
            repoints.append(c)
    created = []
    for (parent, cid), f in parts.items():
        if parent not in by:
            problems.append(f"{cid}: unknown parent {parent}")
            continue
        if cid in by:
            problems.append(f"{cid}: already registered")
            continue
        p = by[parent]
        st = f.get("status", "")
        src = f.get("status_source", "") or p["status_source"]
        if not st or st.startswith(UNSPLIT):
            st, src = UNSPLIT + p["status"], p["status_source"]  # never invent or upgrade
        r = new_row(cid, kind=f.get("kind", p["kind"]), name=f.get("name", ""), file=f.get("file", p["file"]),
                    lines=f.get("lines", ""), premises=f.get("premises", ""), status=st, status_source=src,
                    depends_on=f.get("depends_on", ""), council=p.get("council", ""), method=p.get("method", ""),
                    notes=(f.get("notes", "") + f" [split from {parent}]").strip())
        if r["kind"] not in R.KINDS:
            problems.append(f"{cid}: kind {r['kind']!r} not in {R.KINDS}")
            continue
        if not r["sha256"]:
            problems.append(f"{cid}: span unreadable {r['file']}:{r['lines']} / {r['premises']}")
            continue
        if not status_ok(st, src):
            problems.append(f"{cid}: status not verbatim at {src}: {st[:60]!r}")
            continue
        so, sn = R.status_strength(p["status"]), R.status_strength(st)
        if isinstance(so, int) and isinstance(sn, int) and sn > so:
            problems.append(f"{cid}: part status stronger than the parent's ({sn} > {so}) — check the source")
        created.append((parent, r))
    print(f"{len(created)} part(s) to create from {len({p for p, _ in created})} parent(s); "
          f"{len(repoints)} re-point(s); {len(problems)} problem(s)")
    for x in problems:
        print("  PROBLEM", x)
    if not apply:
        print("(dry run: nothing written; add --apply)")
        return
    if problems:
        sys.exit("refusing to apply with problems; fix the spec first")
    rows += [r for _, r in created]
    by = R.index(rows)
    for parent, r in created:
        p = by[parent]
        p["depends_on"] = R.join_list(dict.fromkeys(R.split_list(p["depends_on"]) + [f"{r['id']}@stmt"]))
        p["implies"] = R.join_list(dict.fromkeys(R.split_list(p.get("implies", "")) + [r["id"]]))
        R.log_event("split", r["id"], parent, f"{r['status'][:60]}", f"split from {parent} ({os.path.basename(path)})",
                    "INFRA")
    for rp in repoints:
        d = by.get(rp["id"])
        old, _, new = rp.get("value", "").partition("=>")
        old, new = old.strip(), new.strip()
        if d is None or old not in R.split_list(d["depends_on"]):
            print(f"  skip re-point {rp['id']}: {old!r} not found")
            continue
        d["depends_on"] = R.join_list(new if it == old else it for it in R.split_list(d["depends_on"]))
        R.log_event("split-repoint", d["id"], old, new, rp.get("evidence", ""), "INFRA")
    R.save_claims(rows)
    print("written")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=["claims", "splits"])
    ap.add_argument("path")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    (ingest_claims if a.what == "claims" else ingest_splits)(a.path, a.apply)


if __name__ == "__main__":
    main()
