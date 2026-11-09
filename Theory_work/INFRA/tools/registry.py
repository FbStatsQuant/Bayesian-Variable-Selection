"""registry.py — everyday registry operations (read, edit one field, rehash, derived fields, strength queries).

  show ID                          one claim (all fields) + necessity verdicts of its hypotheses
  deps ID | rdeps ID               transitive dependencies / dependents, with the use of each edge
  add ID --file F --lines a-b --kind K --name N --status S --source path:line [--state CANDIDATE]
      [--field k=v ...] --reason R    (the status must occur verbatim at --source)
                                   register a claim (new results from improvement tickets enter as CANDIDATE)
  set ID k=v [k=v ...] --reason R  edit fields (not state/sha/version: propagate.py / rehash); logged
  rehash ID [--lines a-b] --bump none|patch|minor|major --reason R
                                   accept the current statement text: new sha256 (+ span) and version bump
                                   (patch = editorial, minor = proof/status, major = the claim changed)
  rehash ID --tex --reason R       record that the LaTeX transcription (`tex`) was reviewed against the statement
  correct-status ID --status S --source path:line --reason R
                                   fix a TRANSCRIPTION error: S must occur verbatim at path:line (± 3 lines)
                                   (real status changes: propagate.py downgrade / a new ticket result)
  freeze --set|--unset --reason R  set config freeze; --set refuses unless the freeze criterion holds
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

PROTECTED = {"id", "state", "superseded_by", "sha256", "version", "improvable", "status", "status_source",
             "tex_sha256"}


def get(rows, ref):
    cid = R.resolve(ref, {r["id"] for r in rows}, R.load_aliases())
    if cid is None:
        sys.exit(f"unknown id {ref!r}")
    return R.index(rows)[cid]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["show", "deps", "rdeps", "add", "set", "rehash", "refresh", "compare", "sets",
                                    "assumption-impact", "stats", "dot", "add-external", "correct-status", "freeze"])
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
    ap.add_argument("--tex", action="store_true")
    ap.add_argument("--source")
    ap.add_argument("--set", dest="do_set", action="store_true")
    ap.add_argument("--unset", action="store_true")
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
        if span is None:
            sys.exit("bad --lines")
        t, _, loc = cid.partition(":")
        r = {c: "" for c in R.COLUMNS}
        r.update(id=cid, ticket=t, local_id=loc, kind=a.kind, name=a.name, file=a.file, lines=a.lines, sha256="",
                 version="1.0.0", status=a.status, state=a.state, commit=R.git_last_commit(a.file),
                 state_reason=f"{a.state} {R.today()}: {a.reason}" if a.state != "ACTIVE" else "")
        for kv in a.field:
            k, _, v = kv.partition("=")
            if k not in R.COLUMNS or k in PROTECTED:
                sys.exit(f"field {k!r} not settable")
            r[k] = v
        if a.status:
            import re as _re
            norm = lambda t: _re.sub(r"\s+", " ", _re.sub(r"[*`]", "", t)).strip().lower()  # noqa: E731
            path, _, ln = (a.source or "").rpartition(":")
            lines, n = (R.read_lines(path) if path else None), (int(ln) if ln.isdigit() else 0)
            if not lines or n < 1 or norm(a.status) not in norm(" ".join(lines[n - 1: n + 3])):
                sys.exit("add: --status must occur verbatim at --source path:line (± 3 lines)")
            r["status_source"] = a.source
        r["sha256"] = R.claim_hash(r) or sys.exit("cannot hash the statement/premise spans")
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
            if k == "premises":  # coverage correction: re-hash, PATCH bump (the claim itself did not change)
                h = R.claim_hash(r)
                if h is None:
                    sys.exit("premise span unreadable; nothing saved")
                if h != r["sha256"]:
                    r["sha256"], r["version"] = h, R.bump(r["version"], "patch")
        r["improvable"] = R.improvable(r, sharp)
        R.save_claims(rows)
    elif a.cmd == "rehash" and a.tex:
        r = get(rows, a.args[0])
        tl = R.span_lines(r.get("tex", ""))
        if tl is None or not a.reason:
            sys.exit("rehash --tex needs a readable tex span and --reason (who compared it with the statement)")
        r["tex_sha256"] = R.text_hash(tl)
        R.save_claims(rows)
        R.log_event("rehash-tex", r["id"], "", r["tex_sha256"][:12], a.reason, a.actor)
        print(f"{r['id']}: tex transcription recorded as reviewed")
    elif a.cmd == "rehash":
        r = get(rows, a.args[0])
        if not a.bump or not a.reason:
            sys.exit("rehash needs --bump and --reason")
        span = R.parse_span(a.lines or r["lines"])
        h = R.claim_hash(r, span) if span else None
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
    elif a.cmd == "correct-status":
        r = get(rows, a.args[0])
        if not (a.status and a.source and a.reason):
            sys.exit("correct-status needs --status, --source path:line and --reason")
        import re as _re
        norm = lambda t: _re.sub(r"\s+", " ", _re.sub(r"[*`]", "", t)).strip()  # noqa: E731
        path, _, ln = a.source.rpartition(":")
        lines, n = R.read_lines(path), int(ln) if ln.isdigit() else 0
        if not lines or n < 1 or norm(a.status) not in norm(" ".join(lines[n - 1: n + 3])):
            sys.exit("the status is not found verbatim at --source (± 3 lines); nothing changed")
        R.log_event("correct-status", r["id"], f"{r['status'][:80]} @ {r['status_source']}",
                    f"{a.status[:80]} @ {a.source}", a.reason, a.actor)
        r["status"], r["status_source"] = a.status, a.source
        r["version"] = R.bump(r["version"], "patch")
        R.save_claims(rows)
        print(f"{r['id']}: status corrected (transcription), v{r['version']}")
    elif a.cmd == "freeze":
        import check
        cfg_h, cfg = R.read_tsv(R.CONFIG)
        if a.do_set == a.unset or not a.reason:
            sys.exit("freeze needs exactly one of --set / --unset, and --reason (Felipe's decision)")
        if a.do_set:
            bad = check.freeze_violations(rows, sharp, R.config())
            if bad:
                sys.exit("freeze criterion not met:\n  " + "\n  ".join(bad))
        for c in cfg:
            if c["key"] == "freeze":
                c["value"] = "yes" if a.do_set else "no"
        R.write_tsv(R.CONFIG, cfg_h, cfg)
        R.log_event("freeze", "-", "", "yes" if a.do_set else "no", a.reason, a.actor)
        print("freeze =", "yes" if a.do_set else "no")
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
