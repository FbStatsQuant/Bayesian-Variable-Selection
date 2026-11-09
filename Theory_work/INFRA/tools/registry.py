"""registry.py — everyday registry operations (read, edit one field, rehash, derived fields, strength queries).

  show ID                          one claim (all fields) + necessity verdicts of its hypotheses
  deps ID | rdeps ID               transitive dependencies / dependents, with the use of each edge
  add ID --file F --lines a-b --kind K --name N --status S [--state CANDIDATE] [--field k=v ...] --reason R
                                   register a claim (new results from improvement tickets enter as CANDIDATE)
  set ID k=v [k=v ...] --reason R  edit fields (not state/sha/version: propagate.py / rehash); logged
  rehash ID [--lines a-b] --bump none|patch|minor|major --reason R
                                   accept the current statement text: new sha256 (+ span) and version bump
                                   (patch = editorial, minor = proof/status, major = the claim changed)
  refresh                          recompute derived fields (`improvable`)
  compare X Y [--axes k=v,...]     strength partial order of Y vs X (assumptions, conclusion, rate, scope)
  sets                             distinct versioned assumption sets of the headline claims (cap: config.tsv)
  assumption-impact A              every use of A with its polarity; whether weakening A globally is safe
  add-external SOP:<row> --reason R  register a State-of-Project row as an external anchor (statement = the row)
  stats                            counts by ticket, kind, state, conclusion level, improvable
  dot [--headline]                 dependency graph (Graphviz); dashed = `implies`
"""
from __future__ import annotations

import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

PROTECTED = {"id", "state", "superseded_by", "sha256", "version", "improvable"}


def get(rows, ref):
    cid = R.resolve(ref, {r["id"] for r in rows}, R.load_aliases())
    if cid is None:
        sys.exit(f"unknown id {ref!r}")
    return R.index(rows)[cid]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["show", "deps", "rdeps", "add", "set", "rehash", "refresh", "compare", "sets",
                                    "assumption-impact", "stats", "dot", "add-external"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--reason", default="")
    ap.add_argument("--lines")
    ap.add_argument("--bump", choices=["none", "patch", "minor", "major"])
    ap.add_argument("--file")
    ap.add_argument("--kind")
    ap.add_argument("--name")
    ap.add_argument("--status")
    ap.add_argument("--state", default="ACTIVE", choices=["ACTIVE", "CANDIDATE"])
    ap.add_argument("--field", action="append", default=[])
    ap.add_argument("--axes", default="")
    ap.add_argument("--headline", action="store_true")
    ap.add_argument("--actor", default="HQ")
    a = ap.parse_args()
    rows = R.load_claims()
    sharp = R.load_sharpness()

    if a.cmd == "show":
        r = get(rows, a.args[0])
        for c in R.COLUMNS:
            if r.get(c):
                print(f"{c:18} {r[c]}")
        for h in R.hypotheses(r):
            v, n = R.necessity(r["id"], h, sharp)
            print(f"  necessity {h:24} {v:20} failed-removals={n}")
    elif a.cmd in ("deps", "rdeps"):
        r = get(rows, a.args[0])
        g = R.Graph(rows)
        if a.cmd == "rdeps":
            for d, p in sorted(g.dependents(r["id"]).items(), key=lambda kv: (len(kv[1]), kv[0])):
                print(f"{'  ' * (len(p) - 2)}{d} [{R.index(rows)[d]['state']}] uses "
                      f"{','.join(sorted(g.uses[(p[-1], p[-2])]))} of {p[-2]}")
        else:
            seen, stack = set(), [(r["id"], 0)]
            while stack:
                u, dpt = stack.pop()
                for v in g.deps.get(u, []):
                    if v not in seen:
                        seen.add(v)
                        print(f"{'  ' * dpt}{v} [{R.index(rows)[v]['state']}] @{','.join(sorted(g.uses[(u, v)]))}")
                        stack.append((v, dpt + 1))
    elif a.cmd == "add":
        cid = a.args[0]
        if cid in {r["id"] for r in rows}:
            sys.exit(f"{cid} exists")
        if not (a.file and a.lines and a.kind and a.name and a.status is not None and a.reason):
            sys.exit("add needs --file --lines --kind --name --status --reason")
        span = R.parse_span(a.lines)
        h = R.statement_hash(a.file, span) if span else None
        if h is None:
            sys.exit("cannot hash the span (file/lines)")
        t, _, loc = cid.partition(":")
        r = {c: "" for c in R.COLUMNS}
        r.update(id=cid, ticket=t, local_id=loc, kind=a.kind, name=a.name, file=a.file, lines=a.lines, sha256=h,
                 version="1.0.0", status=a.status, state=a.state, commit=R.git_last_commit(a.file),
                 state_reason=f"{a.state} {R.today()}: {a.reason}" if a.state != "ACTIVE" else "")
        for kv in a.field:
            k, _, v = kv.partition("=")
            if k not in R.COLUMNS or k in PROTECTED:
                sys.exit(f"field {k!r} not settable")
            r[k] = v
        r["improvable"] = R.improvable(r, sharp)
        rows.append(r)
        R.save_claims(rows)
        R.log_event("add", cid, "", f"{a.state} v1.0.0 {a.status}", a.reason, a.actor)
        print(f"added {cid} ({a.state})")
    elif a.cmd == "set":
        r = get(rows, a.args[0])
        if not a.reason:
            sys.exit("set needs --reason")
        for kv in a.args[1:]:
            k, _, v = kv.partition("=")
            if k not in R.COLUMNS or k in PROTECTED:
                sys.exit(f"field {k!r} not settable here (state: propagate.py; sha/version: rehash)")
            R.log_event("set", r["id"], f"{k}={r.get(k, '')[:80]}", f"{k}={v[:80]}", a.reason, a.actor)
            r[k] = v
        r["improvable"] = R.improvable(r, sharp)
        R.save_claims(rows)
    elif a.cmd == "rehash":
        r = get(rows, a.args[0])
        if not a.bump or not a.reason:
            sys.exit("rehash needs --bump and --reason")
        span = R.parse_span(a.lines or r["lines"])
        h = R.statement_hash(r["file"], span) if span else None
        if h is None:
            sys.exit("cannot hash the span")
        before = f"{r['lines']} {r['sha256'][:12]} v{r['version']}"
        r["lines"], r["sha256"], r["commit"] = f"{span[0]}-{span[1]}", h, R.git_last_commit(r["file"])
        if a.bump != "none":
            r["version"] = R.bump(r["version"], a.bump)
        R.save_claims(rows)
        R.log_event("rehash", r["id"], before, f"{r['lines']} {h[:12]} v{r['version']}", a.reason, a.actor)
        print(f"{r['id']}: {r['lines']} {h[:12]} v{r['version']}")
    elif a.cmd == "refresh":
        n = 0
        for r in rows:
            v = R.improvable(r, sharp)
            if v != r.get("improvable", ""):
                r["improvable"], n = v, n + 1
        R.save_claims(rows)
        print(f"refresh: {n} row(s) updated")
    elif a.cmd == "compare":
        x, y = get(rows, a.args[0]), get(rows, a.args[1])
        axes = R.compare(x, y, R.load_assumptions(), dict(kv.split("=") for kv in a.axes.split(",") if "=" in kv))
        for k, v in axes.items():
            print(f"{k:12} {v}")
        free = x["id"] in R.implies_closure(rows, y["id"])
        print(f"verdict: {y['id']} {R.verdict(axes)} {x['id']}; implication recorded: {free}")
    elif a.cmd == "sets":
        asm = R.load_assumptions()
        sets = collections.defaultdict(list)
        for r in rows:
            if r.get("headline") == "yes" and r["state"] in R.VALID and R.hypotheses(r):
                sets[tuple(sorted(f"{h}@{asm.get(h, {}).get('version', '?')}" for h in R.hypotheses(r)))].append(r["id"])
        cap = R.config().get("max_assumption_sets", "10")
        print(f"{len(sets)} distinct headline assumption sets (cap {cap})")
        for i, (k, v) in enumerate(sorted(sets.items(), key=lambda kv: -len(kv[1])), 1):
            print(f"AS{i}: {', '.join(v)}\n     {'; '.join(k)}")
    elif a.cmd == "assumption-impact":
        aid = a.args[0]
        uses = collections.defaultdict(list)
        for r in rows:
            for it in R.split_list(r.get("assumptions", "")):
                x, pol = R.parse_asm(it)
                if x == aid:
                    if r["kind"] in ("counterexample", "obstruction"):
                        pol = "necessity"
                    uses[pol].append(r["id"])
            if aid in R.split_list(r.get("consumes", "")):
                uses["consumed"].append(r["id"])
        for pol, ids in uses.items():
            print(f"{pol:10} {len(ids):3}  {', '.join(ids)}")
        unsafe = uses.get("necessity") or uses.get("iff")
        print("weakening globally: " + ("UNSAFE — used in necessity/iff results; SPLIT it (keep the old A for those, "
                                        "add a weaker A' for the hypotheses)" if unsafe else "safe (hypothesis uses only)"))
    elif a.cmd == "add-external":
        from build_registry import sop_rows, external_row
        eid = a.args[0]
        if eid in {r["id"] for r in rows} or not eid.startswith("SOP:"):
            sys.exit(f"{eid} exists or is not SOP:<row>")
        sop = sop_rows()
        if eid[4:] not in sop:
            sys.exit(f"{eid[4:]} not found in the State-of-Project registry")
        rows.insert(0, external_row(eid, *sop[eid[4:]]))
        R.save_claims(rows)
        R.log_event("add-external", eid, "", "ACTIVE", a.reason or "external anchor", a.actor)
        print(f"added {eid}")
    elif a.cmd == "stats":
        for f in ("ticket", "kind", "state"):
            c = collections.Counter(r[f] for r in rows)
            print(f"{f}: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
        c = collections.Counter(R.conclusion_level(r) or "-" for r in rows if r.get("headline") == "yes")
        print("headline conclusion levels: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
        c = collections.Counter((r.get("improvable") or "-").split("(")[0] for r in rows if r.get("headline") == "yes")
        print("headline improvable: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
        print(f"headlines: {sum(r.get('headline') == 'yes' for r in rows)}; total claims: {len(rows)}")
    elif a.cmd == "dot":
        g = R.Graph(rows)
        keep = {r["id"] for r in rows if not a.headline or r.get("headline") == "yes"}
        print("digraph claims {\n  rankdir=BT; node [shape=box,fontsize=9];")
        for r in rows:
            if r["id"] in keep:
                col = {"ACTIVE": "black", "CANDIDATE": "blue", "SUPERSEDED-VALID": "gray",
                       "REBASE-NEEDED": "orange", "SUSPECT": "orange"}.get(r["state"], "red")
                print(f'  "{r["id"]}" [color={col}];')
        for u, vs in g.deps.items():
            for v in vs:
                if u in keep and v in keep:
                    print(f'  "{u}" -> "{v}" [label="{",".join(sorted(g.uses[(u, v)]))}"];')
        ids, al = {r["id"] for r in rows}, R.load_aliases()
        for r in rows:
            for x in R.split_list(r.get("implies", "")):
                t = R.resolve(x, ids, al, r["ticket"])
                if t and r["id"] in keep and t in keep:
                    print(f'  "{r["id"]}" -> "{t}" [style=dashed,label="implies"];')
        print("}")


if __name__ == "__main__":
    main()
