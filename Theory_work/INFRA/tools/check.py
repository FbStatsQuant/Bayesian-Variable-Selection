"""check.py — consistency audit of the claims registry against the repository (rules: INFRA/LIFECYCLE.md).

Run from anywhere:  python Theory_work/INFRA/tools/check.py [--json OUT] [--quiet] [--strict] [--only C2,C4]

Correctness layer
  C1 schema      [ERROR] duplicate id, unknown kind/state, bad semver, non-ACTIVE without state_reason
  C2 hash        [ERROR] statement text changed (sha256 mismatch); [WARN] unchanged but MOVED (new span given)
  C3 dangling    [ERROR] depends_on reference that resolves to no registry id (after aliases.tsv)
  C4 lifecycle   [ERROR] ACTIVE claim depends on a SUSPECT / NARROWED / RETRACTED / DEPRECATED / CANDIDATE id
                          without an ack; [INFO] depends on SUPERSEDED-VALID (re-point pending)
  C5 strength    [WARN]  checked status resting on a PARTIAL/SKETCH/OPEN input (negative results excluded)
  C6 cycles      [ERROR] dependency cycle
  C7 SoP         [WARN]  ticket result vs State_of_Project/registry/theory_loop.tsv; [INFO] no row (lag)
  C8 FINAL       [WARN]  ticket statuses quoted in Wave1C/FINAL/sections/*.tex vs ticket result
  C9 evidence    [WARN]  evidence file named in the registry does not exist
  M1 method pin  [WARN]  method component changed since the commit the claim is pinned to (rollback trigger);
                          [WARN] pin not a known commit
Strength layer (headline theorems + shared assumptions)
  S1 schema      [ERROR] unknown assumption/property id, bad polarity, bad sharpness/binding row, implies /
                          superseded_by / coexists_with target missing, SUPERSEDED-VALID <-> superseded_by mismatch
  S2 implies     [WARN]  Y implies X although X's conclusion level is stronger
  S3 improvable  [WARN]  stored `improvable` differs from the derived value (registry.py refresh)
  S4 gates       [WARN]  headline without correct:PASS; [INFO] strength gates not passed; no assumptions recorded
  S5 interface   [WARN]  a non-headline claim lists a SHARED assumption directly (consume its property P via the
                          bridge); `consumes` holds a non-property; shared assumption without a bridge
  S6 sets        [WARN]  more distinct headline assumption sets than config max_assumption_sets
  S7 binding     [WARN]  headline hypothesis without a binding-map row
  S8 freeze      [INFO]  freeze criterion per headline (every hypothesis NECESSARY or ≥ 2 failed removals)
  S9 repoints    [INFO]  PROPOSED re-pointings awaiting a check
Exit code 1 if any ERROR (or any WARN with --strict).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

BLOCKING = {"SUSPECT", "NARROWED", "RETRACTED", "DEPRECATED", "CANDIDATE"}  # REBASE-NEEDED is still true


def run():
    out = []

    def add(sev, chk, cid, msg):
        out.append({"severity": sev, "check": chk, "id": cid, "message": msg})

    rows = R.load_claims()
    tickets = R.load_tickets()
    aliases = R.load_aliases()
    by = {}
    # C1
    for r in rows:
        cid = r["id"]
        if cid in by:
            add("ERROR", "C1-schema", cid, "duplicate id")
        by[cid] = r
        if r.get("kind") not in R.KINDS:
            add("ERROR", "C1-schema", cid, f"unknown kind {r.get('kind')!r}")
        if r.get("state") not in R.STATES:
            add("ERROR", "C1-schema", cid, f"unknown state {r.get('state')!r}")
        if not R.SEMVER.match(r.get("version", "")):
            add("ERROR", "C1-schema", cid, f"bad version {r.get('version')!r}")
        if r.get("state") not in ("ACTIVE",) and not r.get("state_reason"):
            add("ERROR", "C1-schema", cid, "non-ACTIVE state without state_reason")
    ids = set(by)
    # C2
    for r in rows:
        cid, f, span = r["id"], r.get("file", ""), R.parse_span(r.get("lines", ""))
        if R.read_lines(f) is None:
            add("ERROR", "C2-hash", cid, f"statement file missing: {f!r}")
            continue
        if span is None:
            add("ERROR", "C2-hash", cid, f"bad line span {r.get('lines')!r}")
            continue
        h = R.claim_hash(r)
        if h is None:
            add("ERROR", "C2-hash", cid, f"a premise span is unreadable: {r.get('premises')!r}")
            continue
        if h == r.get("sha256"):
            continue
        new = None if r.get("premises") else R.relocate(f, r.get("sha256", ""), span[1] - span[0] + 1)
        if new:
            add("WARN", "C2-moved", cid, f"statement unchanged but moved {f}:{span[0]}-{span[1]} -> {new[0]}-{new[1]} "
                f"(registry.py rehash {cid} --lines {new[0]}-{new[1]} --bump none --reason moved)")
        else:
            add("ERROR", "C2-changed", cid, f"statement at {f}:{span[0]}-{span[1]} no longer matches its sha256 "
                f"(edited, or span shifted); review the change, then registry.py rehash {cid} --bump patch|minor|major")
    # C3, C6
    g = R.Graph(rows, aliases)
    for cid, ref in g.dangling:
        add("ERROR", "C3-dangling", cid, f"depends_on {ref!r} resolves to no registry id")
    for cid, ref in g.self_edges:
        add("ERROR", "C3-self", cid, f"depends_on lists the claim itself ({ref!r})")
    for cid, ref in g.unregistered:
        add("INFO", "C3-unregistered", cid, f"uses {ref!r}: literature / named premise / archive lemma with no "
            "registry row (aliases.tsv '-')")
    for cyc in g.cycles():
        add("ERROR", "C6-cycle", cyc[0], " -> ".join(cyc))
    # C4, C5
    for r in rows:
        cid = r["id"]
        acks = set(R.split_list(r.get("acks", "")))
        s_me = R.status_strength(r.get("status", ""))
        for d in g.deps.get(cid, []):
            dr = by[d]
            if r["state"] in R.VALID and dr["state"] in BLOCKING and d not in acks:
                add("ERROR", "C4-lifecycle", cid, f"{r['state']} but uses {d}@{','.join(sorted(g.uses[(cid, d)]))} "
                    f"which is {dr['state']} ({dr.get('state_reason', '')[:100]}); propagate.py or ack")
            elif dr["state"] == "SUPERSEDED-VALID":
                add("INFO", "C4-lifecycle", cid, f"uses {d}, SUPERSEDED-VALID by {dr.get('superseded_by')} "
                    "(still true; re-point after a check: propagate.py confirm-repoint)")
            s_d = R.status_strength(dr.get("status", ""))
            if isinstance(s_me, int) and isinstance(s_d, int) and s_me == 3 and s_d <= 1 and d not in acks:
                add("WARN", "C5-strength", cid, f"status {R.status_token(r['status'])!r} rests on {d} "
                    f"({dr.get('status', '')[:90]!r})")
            elif isinstance(s_me, int) and s_me == 3 and s_d == 2 and dr["ticket"] != r["ticket"] and d not in acks:
                add("INFO", "C5-strength", cid, f"checked result uses {d} from another ticket whose own status is "
                    f"author-level ({dr.get('status', '')[:60]!r}); a ticket council does not certify inputs")
    # C7
    loop_path = os.path.join(R.ROOT, "Theory_work/State_of_Project/registry/theory_loop.tsv")
    loop = {x["id"]: x for x in R.read_tsv(loop_path)[1]}
    for t in tickets:
        row = loop.get(t.get("sop_row") or t["ticket"])
        if row is None:
            if t.get("result"):
                add("INFO", "C7-sop-missing", t["ticket"], f"no theory_loop.tsv row (result {t['result'][:70]!r})")
            continue
        a, b = R.status_token(t.get("result", "")), R.status_token(row.get("status_exact", ""))
        if a and b and a != b:
            add("WARN", "C7-sop", t["ticket"], f"ticket result {a!r} vs theory_loop.tsv {b!r}")
    # C8
    tick = {t["ticket"]: t for t in tickets}
    pat_st = re.compile(r"([A-Z0-9][A-Za-z0-9\-]+(?:, [A-Z0-9][A-Za-z0-9\-]+)*):? \\st\{([^}]*)\}")
    pat_src = re.compile(r"\\srcq\{W1C?/([A-Za-z0-9\-]+)/REPORT\.md:[0-9\-]+\}\{([^}]*)\}")
    for tex in sorted(glob.glob(os.path.join(R.ROOT, "Theory_work/Wave1C/FINAL/sections/*.tex"))):
        rel = os.path.relpath(tex, R.ROOT).replace("\\", "/")
        with open(tex, encoding="utf-8", errors="replace") as fh:
            for ln, line in enumerate(fh, 1):
                hits = [(n.strip(), s) for grp, s in pat_st.findall(line) for n in grp.split(",")]
                for name, st in hits + pat_src.findall(line):
                    t = tick.get(name)
                    sa, sb = R.status_strength((t or {}).get("result", "")), R.status_strength(st)
                    if not t or not isinstance(sa, int) or not isinstance(sb, int) or sa == sb:
                        continue  # citation tokens that are not statuses ("Review trail") are citecheck's job
                    if sb > sa:
                        add("WARN", "C8-final", name, f"{rel}:{ln} quotes {st[:70]!r}, STRONGER than the ticket "
                            f"result {t['result'][:70]!r} (overclaim unless it is a sub-claim)")
                    else:
                        add("INFO", "C8-final", name, f"{rel}:{ln} quotes {st[:70]!r}, weaker than the ticket "
                            f"result {t['result'][:50]!r}")
    # C9
    folder = {t["ticket"]: t["folder"] for t in tickets}
    for r in rows:
        for ev in R.split_list(r.get("evidence", "")):
            p = ev.split(":")[0].strip()
            if not re.search(r"\.(md|txt|py|tex)$", p):
                continue
            base = folder.get(r["ticket"], "")
            cands = [p] + ([os.path.join(base, p), os.path.join(os.path.dirname(base), p)] if base else [])
            if not any(os.path.exists(os.path.join(R.ROOT, c)) for c in cands):
                add("WARN", "C9-evidence", r["id"], f"evidence file not found: {p}")
    # C10 verbatim status: the status string must occur at status_source (± 3 lines), else anywhere in that file
    def norm(s):
        # markdown emphasis and table/list punctuation are not part of a status ("| A | B |" == "A; B")
        return re.sub(r"\s+", " ", re.sub(r"[*`_|;,]", " ", s or "")).strip().lower()
    for r in rows:
        src, st = r.get("status_source", ""), norm(r.get("status", ""))
        if r["kind"] == "external":
            continue
        if not st:
            add("WARN", "C10-verbatim", r["id"], "empty status (no own status written in the ticket files)")
            continue
        path, _, ln = src.rpartition(":")
        lines = R.read_lines(path) if path else None
        sp = R.parse_span(ln.split(",")[0]) if lines else None
        if lines is None or sp is None:
            add("ERROR", "C10-verbatim", r["id"], f"status_source {src!r} is not a readable path:line (no provenance)")
            continue
        window = norm(" ".join(lines[max(0, sp[0] - 4): sp[1] + 3]))
        if st in window:
            continue
        if st in norm(" ".join(lines)):
            add("WARN", "C10-verbatim", r["id"], f"status found in {path} but not at line {ln} (± 3): fix status_source")
        else:
            add("WARN", "C10-verbatim", r["id"], f"status {r['status'][:80]!r} not found verbatim in {path}")
    # M1 method pinning
    comps, cache = R.load_components(), {}
    for r in rows:
        pin = r.get("method_commit", "")
        if not pin or r["state"] in R.DEAD:
            continue
        if R.git("cat-file", "-e", pin + "^{commit}")[0] != 0:
            add("WARN", "M1-pin", r["id"], f"method_commit {pin!r} is not a commit in this repository")
            continue
        for c in R.split_list(r.get("method_components", "")) or ["core"]:
            key = (pin, c)
            if key not in cache:
                paths = comps.get(c)
                cache[key] = None if paths is None else R.git("diff", "--name-only", pin, "HEAD", "--", *paths)[1]
            if cache[key] is None:
                add("WARN", "M1-pin", r["id"], f"unknown method component {c!r} (method_components.tsv)")
            elif cache[key]:
                files = cache[key].splitlines()
                add("WARN", "M1-method-changed", r["id"], f"component {c} changed since pin {pin} "
                    f"({len(files)} file(s), e.g. {files[0]}): rollback trigger — re-check, then re-pin")
    # ---- strength layer
    asm, sharp, binding = R.load_assumptions(), R.load_sharpness(), R.load_binding()
    for a, ar in asm.items():
        if ar.get("kind") not in ("assumption", "property"):
            add("ERROR", "S1-schema", a, f"assumption kind {ar.get('kind')!r}")
        for x in R.split_list(ar.get("implies", "")):
            if x not in asm:
                add("ERROR", "S1-schema", a, f"implies unknown assumption {x!r}")
        brs = [b for b in R.split_list(ar.get("bridge", "")) if b != "MISSING"]
        if ar.get("kind") == "assumption" and ar.get("shared") == "yes" and not brs:
            add("WARN", "S5-interface", a, "shared assumption without a bridge lemma A ⇒ P")
        if len(brs) > 1 and ar.get("kind") == "assumption":
            add("WARN", "S5-interface", a, f"{len(brs)} bridges ({', '.join(brs)}); interface rule: exactly one A ⇒ P")
        for b in brs:
            if R.resolve(b, ids, aliases) is None:
                add("ERROR", "S1-schema", a, f"bridge {b!r} resolves to no claim")
    shared = {a for a, ar in asm.items() if ar.get("kind") == "assumption" and ar.get("shared") == "yes"}
    bridges = {R.resolve(b, ids, aliases) for ar in asm.values() for b in R.split_list(ar.get("bridge", ""))}
    sets = {}
    for r in rows:
        cid = r["id"]
        for it in R.split_list(r.get("assumptions", "")):
            a, _ = R.parse_asm(it)
            if a not in asm:
                add("ERROR", "S1-schema", cid, f"unknown assumption {a!r} (add to assumptions.tsv)")
            if "~" in it and it.split("~", 1)[1] not in ("nec", "iff"):
                add("ERROR", "S1-schema", cid, f"bad polarity in {it!r}")
            if a in shared and r.get("headline") != "yes" and cid not in bridges and \
                    R.parse_asm(it)[1] == "hypothesis":
                add("WARN", "S5-interface", cid, f"lists shared assumption {a} directly; consume its property via "
                    f"the bridge {asm[a].get('bridge')}")
        for p in R.split_list(r.get("consumes", "")):
            if asm.get(p, {}).get("kind") != "property":
                add("WARN", "S5-interface", cid, f"consumes {p!r}, which is not a registered property P:*")
        lvl = R.conclusion_level(r)
        if r.get("conclusion") and lvl not in R.CONCLUSION_LEVELS + ["negative"]:
            add("WARN", "S1-schema", cid, f"conclusion level {lvl!r} unknown")
        for x in R.split_list(r.get("implies", "")):
            t = R.resolve(x, ids, aliases, r["ticket"])
            if t is None:
                add("ERROR", "S1-schema", cid, f"implies {x!r} resolves to no id")
            elif lvl in R.CONCLUSION_LEVELS and R.conclusion_level(by[t]) in R.CONCLUSION_LEVELS and \
                    R.CONCLUSION_LEVELS.index(R.conclusion_level(by[t])) > R.CONCLUSION_LEVELS.index(lvl):
                add("WARN", "S2-implies", cid, f"implies {t} whose conclusion level is stronger")
        for x in R.split_list(r.get("coexists_with", "")):
            if R.resolve(x, ids, aliases, r["ticket"]) is None:
                add("ERROR", "S1-schema", cid, f"coexists_with {x!r} resolves to no id")
        sb = r.get("superseded_by", "")
        if sb and R.resolve(sb, ids, aliases, r["ticket"]) is None:
            add("ERROR", "S1-schema", cid, f"superseded_by {sb!r} resolves to no id")
        if r.get("state") == "SUPERSEDED-VALID" and not sb:
            add("ERROR", "S1-schema", cid, "SUPERSEDED-VALID without superseded_by")
        if sb and r.get("state") in ("ACTIVE", "CANDIDATE", "REBASE-NEEDED"):
            add("ERROR", "S1-schema", cid, f"superseded_by set but state {r['state']}")
        if r.get("tex"):
            tl = R.span_lines(r["tex"])
            if tl is None:
                add("ERROR", "C11-tex", cid, f"tex span {r['tex']!r} unreadable")
            elif r.get("tex_sha256") and R.text_hash(tl) != r["tex_sha256"]:
                add("WARN", "C11-tex", cid, "LaTeX transcription changed since its last review against the statement "
                    "(re-check, then registry.py set ... tex_sha256 via rehash --tex)")
            elif not r.get("tex_sha256"):
                add("INFO", "C11-tex", cid, "LaTeX transcription never reviewed against the Markdown statement")
        if r.get("headline") == "yes":
            derived = R.improvable(r, sharp)
            if r.get("improvable", "") != derived:
                add("WARN", "S3-improvable", cid, f"stored {r.get('improvable')!r} != derived {derived!r} "
                    "(registry.py refresh)")
            gts = r.get("gates", "")
            for gname, ev in re.findall(r"(\w+):PASS(?:\(([^)]*)\))?", gts):
                if not (ev or "").strip():
                    add("WARN", "S4-gates", cid, f"gate {gname}:PASS without evidence in parentheses")
            if "correct:PASS" not in gts:
                add("WARN", "S4-gates", cid, "headline has not passed the correctness gate (correct:PASS)")
            miss = [k for k in ("lit", "necessity", "better") if f"{k}:PASS" not in gts]
            if miss:
                add("INFO", "S4-gates", cid, f"strength gates not passed: {','.join(miss)}")
            hyp = R.hypotheses(r)
            if not hyp and r["kind"] not in ("counterexample", "obstruction") and \
                    R.conclusion_level(r) != "negative":
                add("INFO", "S4-gates", cid, "headline without an assumption list (strength fields not seeded)")
            if hyp and r["state"] in R.VALID:
                key = tuple(sorted(f"{a}@{asm.get(a, {}).get('version', '?')}" for a in hyp))
                sets.setdefault(key, []).append(cid)
                bound = {b["assumption"] for b in binding if b["headline"] == cid}
                for a in hyp:
                    if a not in bound:
                        add("WARN", "S7-binding", cid, f"hypothesis {a} has no binding-map row (which claim forces it?)")
                unsettled = [a for a in hyp if not R.settled(cid, a, sharp)]
                add("INFO", "S8-freeze", cid, "freeze criterion MET" if not unsettled else
                    f"freeze criterion not met: {len(unsettled)} hypothesis(es) without necessity evidence or "
                    f"2 failed removals ({','.join(unsettled[:6])})")
    cfg = R.config()
    if cfg.get("freeze") == "yes":
        for msg in freeze_violations(rows, sharp, cfg):
            add("ERROR", "S8-freeze", "-", f"freeze=yes but {msg}")
    cap = int(cfg.get("max_assumption_sets", "10") or 10)
    if len(sets) > cap:
        add("WARN", "S6-sets", "-", f"{len(sets)} distinct headline assumption sets > cap {cap}; prefer splitting "
            "assumptions into shared interface properties")
    for s in sharp:
        if s["claim"] not in ids or s["assumption"] not in asm or s.get("verdict") not in R.NECESSITY:
            add("ERROR", "S1-schema", s["claim"], f"sharpness row ({s['claim']}, {s['assumption']}, "
                f"{s.get('verdict')!r}) has an unknown claim/assumption/verdict")
    for b in binding:
        if b["headline"] not in ids or b["assumption"] not in asm or \
                (b.get("binding_claim") and R.resolve(b["binding_claim"], ids, aliases) is None):
            add("ERROR", "S1-schema", b["headline"], f"binding row ({b['headline']}, {b['assumption']}, "
                f"{b.get('binding_claim')}) references an unknown id")
        for sg in R.split_list(b.get("signals", "")):
            if sg not in R.SIGNALS:
                add("WARN", "S1-schema", b["headline"], f"unknown signal {sg!r}")
    for rp in R.load_repoints():
        if rp.get("state") == "PROPOSED":
            add("INFO", "S9-repoints", rp["dependent"], f"PROPOSED re-point {rp['from']} -> {rp['to']} "
                f"(use {rp.get('use')}) awaiting a check")
    e = sum(o["severity"] == "ERROR" for o in out)
    w = sum(o["severity"] == "WARN" for o in out)
    return out, e, w, len(rows)


def freeze_violations(rows, sharp, cfg):
    """Freeze criterion (LIFECYCLE §5.3): every hypothesis of every valid headline settled (NECESSARY or >= 2
    distinct failed removal routes), and the latest strategy review and adversarial round are recorded files."""
    out = []
    for r in rows:
        if r.get("headline") == "yes" and r["state"] in R.VALID:
            for a in R.hypotheses(r):
                if not R.settled(r["id"], a, sharp):
                    out.append(f"{r['id']} hypothesis {a} is not settled")
    for k in ("last_strategy_review", "last_adversarial_round"):
        v = cfg.get(k, "")
        if not v or not os.path.exists(os.path.join(R.ROOT, v)):
            out.append(f"config {k} does not name an existing review file")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json")
    ap.add_argument("--quiet", action="store_true", help="summary + ERRORs only")
    ap.add_argument("--strict", action="store_true", help="exit 1 on WARN too")
    ap.add_argument("--only", help="comma-separated check prefixes, e.g. C2,C4,S")
    a = ap.parse_args()
    out, e, w, n = run()
    if a.only:
        keep = tuple(a.only.split(","))
        out = [o for o in out if o["check"].startswith(keep)]
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for o in sorted(out, key=lambda o: (order[o["severity"]], o["check"], o["id"])):
        if a.quiet and o["severity"] != "ERROR":
            continue
        print(f"{o['severity']:5} {o['check']:17} {o['id']:30} {o['message']}")
    counts = {s: sum(o["severity"] == s for o in out) for s in order}
    by_check = {}
    for o in out:
        by_check.setdefault(f"{o['severity']}:{o['check']}", 0)
        by_check[f"{o['severity']}:{o['check']}"] += 1
    print(f"\ncheck.py: {n} claims; {counts['ERROR']} ERROR, {counts['WARN']} WARN, {counts['INFO']} INFO")
    print("by check: " + ", ".join(f"{k}={v}" for k, v in sorted(by_check.items())))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"claims": n, "counts": counts, "by_check": by_check, "findings": out}, fh,
                      ensure_ascii=False, indent=1)
    sys.exit(1 if counts["ERROR"] or (a.strict and counts["WARN"]) else 0)


if __name__ == "__main__":
    main()
