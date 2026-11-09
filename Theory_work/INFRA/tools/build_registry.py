"""build_registry.py — ONE-OFF seeding of claims.tsv from the transcription fragments.

After seeding, claims.tsv is the source of truth and is edited only with registry.py / propagate.py.
Refuses to overwrite an existing claims.tsv unless --force.

Inputs (Theory_work/INFRA/registry/):
  fragments/*.jsonl (not *_routes.jsonl, not strength*.jsonl)  helper transcriptions, one claim per line
  fragments/strength/strength.jsonl optional strength seed: {id, headline, assumptions, consumes, conclusion, rate, scope, implies, gates, method_commit}
  aliases.tsv                alias -> id; aliases whose target is "SOP:<row>" create external-anchor rows
  tickets.tsv                ticket order (wave order)
External anchors: row looked up in State_of_Project/registry/{theory_main,theory_supp,theory_loop,history,open,
method}.tsv; statement span = that row's line; status = status_exact verbatim.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

SOP_FILES = ["theory_main", "theory_supp", "theory_loop", "history", "open", "method", "empirics"]


def sop_rows():
    out = {}
    for f in SOP_FILES:
        rel = f"Theory_work/State_of_Project/registry/{f}.tsv"
        lines = R.read_lines(rel) or []
        hdr = lines[0].split("\t") if lines else []
        for i, ln in enumerate(lines[1:], 2):
            d = dict(zip(hdr, ln.split("\t")))
            if d.get("id"):
                out.setdefault(d["id"], (rel, i, d))
    return out


def external_row(eid, rel, i, d):
    r = {c: "" for c in R.COLUMNS}
    r.update(id=eid, ticket="SOP", local_id=eid[4:], kind="external", name=d.get("native", ""),
             short=d.get("short", "")[:300], file=rel, lines=f"{i}-{i}", sha256=R.statement_hash(rel, (i, i)),
             version="1.0.0", status=d.get("status_exact", ""), state="ACTIVE", status_source=f"{rel}:{i}",
             evidence=d.get("checked_by", ""), commit=R.git_last_commit(rel),
             notes=f"external anchor (State-of-Project row {eid[4:]}); depends_on there: {d.get('depends_on', '')}")
    return r


STRENGTH_FIELDS = ("headline", "assumptions", "consumes", "conclusion", "rate", "scope", "implies", "gates",
                   "method_commit", "method_components", "tex")


def seed_strength(actor="INFRA"):
    """Apply fragments/strength/* to the LIVE registry: copy assumptions/sharpness/binding TSVs if the registry has
    none yet; fill strength fields that are still empty (never overwrite); log every change."""
    import shutil
    src = os.path.join(R.REG, "fragments", "strength")
    for f in ("assumptions.tsv", "sharpness.tsv", "binding.tsv"):
        dst = os.path.join(R.REG, f)
        if os.path.exists(os.path.join(src, f)) and not os.path.exists(dst):
            shutil.copyfile(os.path.join(src, f), dst)
            print(f"copied {f}")
    rows = R.load_claims()
    idx = R.index(rows)
    n = 0
    for ln in open(os.path.join(src, "strength.jsonl"), encoding="utf-8"):
        if not ln.strip():
            continue
        j = json.loads(ln)
        r = idx.get(j["id"])
        if r is None:
            print(f"WARN strength seed for unknown id {j['id']}")
            continue
        for k in STRENGTH_FIELDS:
            v = j.get(k)
            v = R.join_list(v) if isinstance(v, list) else (v or "")
            if v and not r.get(k):
                r[k] = v
                n += 1
                R.log_event("seed-strength", r["id"], "", f"{k}={v[:80]}", "strength layer seed (helper draft, "
                            "verified by INFRA lead)", actor)
    sharp = R.load_sharpness()
    for r in rows:
        r["improvable"] = R.improvable(r, sharp)
    R.save_claims(rows)
    print(f"strength seed: {n} field(s) filled")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--strength-only", action="store_true",
                    help="apply fragments/strength/* to the live registry (fills empty fields only)")
    a = ap.parse_args()
    if a.strength_only:
        seed_strength()
        return
    if os.path.exists(R.CLAIMS) and not a.force:
        sys.exit("claims.tsv exists; registry is live. Use registry.py/propagate.py (or --force to reseed).")
    order = {t["ticket"]: i for i, t in enumerate(R.load_tickets())}
    rows, seen = [], set()
    for fp in sorted(glob.glob(os.path.join(R.REG, "fragments", "*.jsonl"))):
        base = os.path.basename(fp)
        if base.endswith("_routes.jsonl") or base.startswith("strength"):
            continue
        for n, ln in enumerate(open(fp, encoding="utf-8"), 1):
            if not ln.strip():
                continue
            j = json.loads(ln)
            cid = f"{j['ticket']}:{j['local_id']}"
            if cid in seen:
                print(f"WARN duplicate {cid} ({base}:{n}) skipped")
                continue
            seen.add(cid)
            span = j.get("lines") or [0, 0]
            span = (int(span[0]), int(span[1]))
            h = R.statement_hash(j["file"], span) if span[0] >= 1 else None
            if h is None:
                print(f"WARN cannot hash {cid}: {j['file']}:{span}")
            r = {c: "" for c in R.COLUMNS}
            r.update(id=cid, ticket=j["ticket"], local_id=j["local_id"], kind=j.get("kind", ""),
                     name=j.get("name", ""), short=j.get("short", ""), file=j["file"],
                     lines=f"{span[0]}-{span[1]}", sha256=h or "", version="1.0.0", status=j.get("status", ""),
                     state="ACTIVE", status_source=j.get("status_source", ""), evidence=j.get("evidence", []),
                     council=j.get("council", ""), commit=R.git_last_commit(j["file"]),
                     depends_on=j.get("depends_on", []), method=j.get("method", ""),
                     falsification=j.get("falsification", []), notes=j.get("notes", ""))
            rows.append(r)
    rows.sort(key=lambda r: order.get(r["ticket"], 999))  # stable: fragment order within a ticket
    # external anchors
    sop = sop_rows()
    ext_ids = sorted({v for v in R.load_aliases().values() if v.startswith("SOP:")})
    ext = []
    for eid in ext_ids:
        key = eid[4:]
        if key not in sop:
            print(f"WARN alias target {eid} not found in State_of_Project registry")
            continue
        r = external_row(eid, *sop[key])
        ext.append(r)
    rows = ext + rows
    # strength seed
    sp = os.path.join(R.REG, "fragments", "strength", "strength.jsonl")
    if os.path.exists(sp):
        idx = R.index(rows)
        for ln in open(sp, encoding="utf-8"):
            if not ln.strip():
                continue
            j = json.loads(ln)
            r = idx.get(j["id"])
            if r is None:
                print(f"WARN strength seed for unknown id {j['id']}")
                continue
            for k in ("headline", "assumptions", "consumes", "conclusion", "rate", "scope", "implies", "gates",
                      "method_commit", "method_components", "tex"):
                if j.get(k):
                    r[k] = R.join_list(j[k]) if isinstance(j[k], list) else j[k]
    sharp = R.load_sharpness()
    for r in rows:
        r["improvable"] = R.improvable(r, sharp)
    R.save_claims(rows)
    print(f"seeded {len(rows)} claims ({len(ext)} external anchors) -> {os.path.relpath(R.CLAIMS, R.ROOT)}")


if __name__ == "__main__":
    main()
