"""propagate.py — lifecycle operations on claims, with use-level propagation, decision log and repair issues.

Rules and who may run what: Theory_work/INFRA/LIFECYCLE.md. Every operation supports --dry-run (impact report,
nothing changed). Every applied operation is written to registry/events.log; decisions also to DECISIONS.md.

Correctness rollbacks
  patch     ID --reason R                      proof changed, statement stands (minor bump): only dependents that
                                               use a proof-internal fact (@proof:...) become SUSPECT
  downgrade ID --status S --reason R           evidence weaker than recorded: status := S (minor bump);
                                               all dependents SUSPECT
  narrow    ID --still-covers U1;U2 --reason R statement narrowed in place (major bump; then registry.py rehash):
                                               dependents whose use is still covered (listed uses) are untouched,
                                               the others SUSPECT
  retract   ID --reason R [--status S]         statement false: RETRACTED (major bump). Claims it had superseded
                                               are RESTORED (SUPERSEDED-VALID -> ACTIVE) and confirmed re-points
                                               to it are reverted; remaining dependents SUSPECT
  deprecate ID --reason R                      wrong target: DEPRECATED; dependents SUSPECT; FAILED_ROUTES.md entry
  suspect   ID --reason R                      possible gap found: SUSPECT; dependents SUSPECT
  clear     ID --reason R                      repaired: SUSPECT / REBASE-NEEDED / NARROWED -> ACTIVE (minor bump)
Strength (better theorems)
  promote   Y [--parity-with X] --reason R     CANDIDATE -> ACTIVE once Y passed the gates (all `k:PASS` of X)
  supersede X --by Y [--axes scope=better,rate=equal] [--key-step-checked EVIDENCE] --reason R
            decision rule (LIFECYCLE §5): Y must be ACTIVE with gate parity and dominate X on every axis.
            free (Y ⇒ X recorded in `implies`) -> X SUPERSEDED-VALID; re-points of X's dependents to Y are
              PROPOSED (repoints.tsv), applied only by confirm-repoint after a check.
            headline-changing (X headline, not free) -> needs --key-step-checked; X SUPERSEDED-VALID; direct
              dependents REBASE-NEEDED (still true, should be rebuilt on Y), one issue each with the exact diff.
            internal-only and not free -> refused: use `remark`.   incomparable -> refused: use `coexist`.
            After freeze (config freeze=yes) only free supersessions are allowed.
  coexist   X --with Y --reason R             incomparable: both kept (X as corollary / special case)
  decline   X --by Y --reason R               decision not to adopt Y (logged)
  remark    X --by Y --reason R               internal-only improvement, not free: logged as a remark, no rebuild
  confirm-repoint D --from X --to Y --checked-by WHO   apply a PROPOSED re-point after the cheap check
  reject-repoint  D --from X --to Y --checked-by WHO   the used fact does not survive: keep D on X
  fail-route X --assumption A --route TEXT --reason R   a failed attempt to remove/weaken A (weak necessity
                                               evidence): sharpness row FAILED-REMOVAL + DECISIONS.md + FAILED_ROUTES.md
Flags: --dry-run, --issues-dir D, --gh (create the issues with gh), --actor A (default HQ)
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

DECISIONS = os.path.join(R.INFRA, "DECISIONS.md")
ROUTES = os.path.join(R.INFRA, "FAILED_ROUTES.md")
INERT = R.DEAD | {"SUPERSEDED-VALID"}
LABELS = {"retract": ["retraction", "theory"], "narrow": ["retraction", "theory"],
          "downgrade": ["retraction", "theory"], "patch": ["lemma-gap", "theory"], "deprecate": ["strategy", "theory"],
          "suspect": ["suspect", "theory"], "supersede": ["strategy", "theory", "major-claim"],
          "dependent": ["suspect", "lemma-gap", "theory"], "rebase": ["lemma-gap", "theory"],
          "repoint": ["theory"]}
# price of rebuilding, in review units (see LIFECYCLE.md §6); edit here if the protocol changes
PRICE = {"proof": "1 proof session", "check": "1 cross-family lemma check", "sweep": "1 exhaustive sweep",
         "council": "1 council (2 reviewers)", "gate": "1 strength gate (lit + necessity + better-theorem review)"}


def decision(kind, x, y, axes, reason, actor, extra=""):
    new = not os.path.exists(DECISIONS)
    with open(DECISIONS, "a", encoding="utf-8", newline="\n") as fh:
        if new:
            fh.write("# Decision log\n\n")
        ax = ", ".join(f"{k}={v}" for k, v in (axes or {}).items())
        fh.write(f"\n## {R.today()} — {kind.upper()} {x}" + (f" / {y}" if y else "") + "\n\n"
                 f"- decided by: {actor}\n- reason: {reason}\n" + (f"- axes (Y vs X): {ax}\n" if ax else "")
                 + (f"- {extra}\n" if extra else ""))


def gh_issue(title, body_file, labels):
    from ghapi import issue  # gh CLI if installed, else the REST API with git's stored credential
    return issue(title, body_file, labels)


def diff_lines(x, y, asm):
    hx, hy = set(R.hypotheses(x)), set(R.hypotheses(y))
    nm = lambda a: f"{a} ({asm.get(a, {}).get('name', '?')})"  # noqa: E731
    out = []
    if hy - hx:
        out.append("hypotheses ADDED (each dependent must now verify them or the property it consumes): "
                   + ", ".join(nm(a) for a in sorted(hy - hx)))
    if hx - hy:
        out.append("hypotheses DROPPED: " + ", ".join(nm(a) for a in sorted(hx - hy)))
    if not (hx or hy):
        out.append("no assumption lists recorded: compare the STATEMENTs by hand")
    for f in ("consumes", "conclusion", "rate", "scope", "method_commit"):
        if x.get(f, "") != y.get(f, ""):
            out.append(f"{f}: `{x.get(f, '') or '—'}` -> `{y.get(f, '') or '—'}`")
    out.append(f"statements: {x['file']}:{x['lines']} -> {y['file']}:{y['lines']}")
    return out


def cost(paths, direct, by, rebase):
    tickets = sorted({by[d]["ticket"] for d in paths})
    heads = sorted(d for d in paths if by[d].get("headline") == "yes")
    paper = sorted(d for d in paths if by[d].get("tex") or by[d].get("headline") == "yes")
    n = len(direct) if rebase else len(paths)
    lines = [f"- {len(direct)} direct / {len(paths) - len(direct)} indirect dependents; tickets: "
             f"{', '.join(tickets) or '—'}; headlines: {', '.join(heads) or '—'}; paper blocks: {len(paper)} "
             "(regeneration by assemble.py is free)",
             f"- re-proof + re-review: {n} × ({PRICE['proof']} + {PRICE['check']}), {len(tickets)} × {PRICE['sweep']}, "
             f"{len(heads)} × {PRICE['council']} + {len(heads)} × {PRICE['gate']}"]
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("op", choices=["patch", "downgrade", "narrow", "retract", "deprecate", "suspect", "clear",
                                   "promote", "supersede", "coexist", "decline", "remark", "confirm-repoint",
                                   "reject-repoint", "fail-route"])
    ap.add_argument("id")
    ap.add_argument("--reason", default="")
    ap.add_argument("--status")
    ap.add_argument("--still-covers", default="")
    ap.add_argument("--by")
    ap.add_argument("--with", dest="with_")
    ap.add_argument("--axes", default="")
    ap.add_argument("--key-step-checked", default="")
    ap.add_argument("--parity-with")
    ap.add_argument("--from", dest="from_")
    ap.add_argument("--to")
    ap.add_argument("--checked-by", default="")
    ap.add_argument("--assumption")
    ap.add_argument("--route", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--issues-dir")
    ap.add_argument("--gh", action="store_true")
    ap.add_argument("--actor", default="HQ")
    a = ap.parse_args()
    if not a.reason and a.op not in ("confirm-repoint", "reject-repoint"):
        sys.exit("--reason is required")

    rows = R.load_claims()
    aliases = R.load_aliases()
    ids = {r["id"] for r in rows}
    by = R.index(rows)
    asm = R.load_assumptions()

    def need(ref, what):
        c = R.resolve(ref or "", ids, aliases)
        if c is None:
            sys.exit(f"{what}: unknown id {ref!r}")
        return c

    cid = need(a.id, "id")
    x = by[cid]
    g = R.Graph(rows, aliases)
    stamp = R.today()
    report = [f"# {a.op} {cid}" + (f" (by {a.by or a.with_})" if (a.by or a.with_) else ""), "",
              f"- reason: {a.reason}", f"- {x['name']} [{x['ticket']}] v{x['version']} state {x['state']}; status "
              f"`{x['status'][:140]}`"]
    issues = []  # (title, filename, body, labels)

    # ------------------------------------------------ simple record-keeping operations
    if a.op in ("confirm-repoint", "reject-repoint"):
        src, dst = need(a.from_, "--from"), need(a.to, "--to")
        rps = R.load_repoints()
        hit = [rp for rp in rps if rp["dependent"] == cid and rp["from"] == src and rp["to"] == dst
               and rp["state"] == "PROPOSED"]
        if not hit or not a.checked_by:
            sys.exit("no PROPOSED re-point with these ids, or --checked-by missing")
        print("\n".join(report + [f"- {a.op}: {cid} uses {src} -> {dst}, checked by {a.checked_by}"]))
        if a.dry_run:
            return
        for rp in hit:
            rp.update(state="CONFIRMED" if a.op == "confirm-repoint" else "REJECTED", checked_by=a.checked_by,
                      date=stamp)
        if a.op == "confirm-repoint":
            items = []
            for it in R.split_list(x["depends_on"]):
                ref, use = R.parse_dep(it)
                items.append(f"{dst}@{use}" if R.resolve(ref, ids, aliases, x["ticket"]) == src else it)
            x["depends_on"] = R.join_list(dict.fromkeys(items))
            if x["state"] == "REBASE-NEEDED":
                x["state"], x["state_reason"] = "ACTIVE", f"rebased onto {dst} {stamp} (checked by {a.checked_by})"
        R.save_repoints(rps)
        R.save_claims(rows)
        R.log_event(a.op, cid, src, dst, f"checked by {a.checked_by} {a.reason}", a.actor)
        return
    if a.op == "fail-route":
        if not (a.assumption and a.route):
            sys.exit("fail-route needs --assumption and --route")
        print("\n".join(report + [f"- failed removal of {a.assumption}: {a.route}"]))
        if a.dry_run:
            return
        sh = R.load_sharpness()
        sh.append({"claim": cid, "assumption": a.assumption, "verdict": "FAILED-REMOVAL", "evidence": a.route,
                   "notes": f"{stamp}: {a.reason}"})
        R.write_tsv(R.SHARPNESS, R.SHARPNESS_COLUMNS, sh)
        decision("failed sharpening", cid, a.assumption, None, f"{a.route} — {a.reason}", a.actor,
                 f"failed removal routes for this pair now: {R.necessity(cid, a.assumption, sh)[1]}")
        with open(ROUTES, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(f"\n| {stamp} | {cid} | remove/weaken {a.assumption}: {a.route} | {a.reason} | "
                     f"DECISIONS.md {stamp} |\n")
        x["improvable"] = R.improvable(x, sh)
        R.save_claims(rows)
        R.log_event("fail-route", cid, a.assumption, "FAILED-REMOVAL", a.route, a.actor)
        return
    if a.op in ("coexist", "decline", "remark"):
        yid = need(a.with_ if a.op == "coexist" else a.by, "--with/--by")
        y = by[yid]
        axes = R.compare(x, y, asm, dict(kv.split("=") for kv in a.axes.split(",") if "=" in kv))
        print("\n".join(report + [f"- axes (Y vs X): {axes} -> {R.verdict(axes)}"]))
        if a.dry_run:
            return
        if a.op == "coexist":
            for u, v in ((x, y), (y, x)):
                u["coexists_with"] = R.join_list(dict.fromkeys(R.split_list(u.get("coexists_with", "")) + [v["id"]]))
            x["notes"] = (x.get("notes", "") + f" [{stamp}: kept alongside {yid} (COEXIST: incomparable)]").strip()
            R.save_claims(rows)
        decision(a.op, cid, yid, axes, a.reason, a.actor)
        R.log_event(a.op, cid, "", yid, a.reason, a.actor)
        return
    if a.op == "promote":
        if x["state"] != "CANDIDATE":
            sys.exit(f"{cid} is {x['state']}, not CANDIDATE")
        need_gates = ["correct"]
        if a.parity_with:
            xp = by[need(a.parity_with, "--parity-with")]
            need_gates += [s.split(":")[0].strip() for s in R.split_list(xp.get("gates", "")) if ":PASS" in s]
        missing = sorted({k for k in need_gates if f"{k}:PASS" not in x.get("gates", "")})
        print("\n".join(report + [f"- gates required: {sorted(set(need_gates))}; missing: {missing or 'none'}"]))
        if missing:
            sys.exit("assurance parity not reached: Y stays CANDIDATE; keep working on X")
        if a.dry_run:
            return
        x["state"], x["state_reason"] = "ACTIVE", f"promoted {stamp}: {a.reason}"
        R.save_claims(rows)
        R.log_event("promote", cid, "CANDIDATE", "ACTIVE", a.reason, a.actor)
        return

    # ------------------------------------------------ supersede: classify by the decision rule
    mode, y, axes, diff = "", None, {}, []
    if a.op == "supersede":
        yid = need(a.by, "--by")
        y = by[yid]
        axes = R.compare(x, y, asm, dict(kv.split("=") for kv in a.axes.split(",") if "=" in kv))
        v = R.verdict(axes)
        free = cid in R.implies_closure(rows, yid, aliases)
        diff = diff_lines(x, y, asm)
        mode = "free" if free else ("headline-changing" if x.get("headline") == "yes" else "internal-only")
        report += [f"- replacement {yid}: {y['name']} state {y['state']}; status `{y['status'][:120]}`",
                   f"- axes (Y vs X): {axes} -> **{v}**", f"- decision-rule class: **{mode}**"]
        report += ["", "## Statement diff", ""] + [f"- {d}" for d in diff]
        problems = []
        if y["state"] != "ACTIVE":
            problems.append(f"Y is {y['state']}: it must pass the same gates as X first (promote); keep working on X")
        missing = [s.split(":")[0].strip() for s in R.split_list(x.get("gates", "")) if ":PASS" in s
                   and s.split(":")[0].strip() + ":PASS" not in y.get("gates", "")]
        if missing:
            problems.append(f"assurance parity: Y lacks {missing}")
        if free:
            pass  # a verified implication Y ⇒ X settles dominance; the axes are informational
        elif v in ("incomparable", "dominated"):
            problems.append(f"Y does not dominate X ({v}): use `coexist` (or `decline`)")
        elif v == "undetermined":
            problems.append("some axes unknown: declare them with --axes rate=better,scope=equal,...")
        if mode == "internal-only":
            problems.append("internal-only and not free: log it with `remark`, no rebuild")
        if mode == "headline-changing" and not a.key_step_checked:
            problems.append("headline-changing: needs --key-step-checked <evidence that Y's key new step was "
                            "independently checked>")
        if R.config().get("freeze") == "yes" and mode != "free":
            problems.append("FROZEN: only free supersessions (Y ⇒ X) allowed")
        if cid in g.dependents(yid):
            problems.append(f"{yid} itself depends on {cid}")
        paths = {d: p for d, p in g.dependents(cid).items() if by[d]["state"] not in INERT}
        direct = sorted(d for d, p in paths.items() if len(p) == 2)
        report += ["", "## Rebuild cost", ""]
        if mode == "free":
            report += [f"- free: {len(direct)} re-point(s) PROPOSED (one cheap check each), no rebase, no re-review"]
        else:
            report += cost({d: paths[d] for d in direct}, direct, by, True)
        if direct:
            report += ["", "| dependent | uses | action |", "|---|---|---|"]
            report += [f"| {d} | {', '.join(sorted(g.uses[(d, cid)]))} | "
                       f"{'propose re-point' if mode == 'free' else 'REBASE-NEEDED'} |" for d in direct]
        if problems:
            report += ["", "## Blocking", ""] + [f"- {p}" for p in problems]
        print("\n".join(report))
        if a.dry_run or problems:
            if problems and not a.dry_run:
                sys.exit("supersede refused (see Blocking)")
            print("\n(dry run: registry unchanged)")
            return
        x["state"], x["superseded_by"] = "SUPERSEDED-VALID", yid
        x["state_reason"] = f"SUPERSEDED-VALID {stamp} by {yid} ({mode}): {a.reason}"
        R.log_event("supersede", cid, "ACTIVE", f"SUPERSEDED-VALID by {yid}", a.reason, a.actor)
        decision("supersede", cid, yid, axes, a.reason, a.actor,
                 f"class {mode}; key step check: {a.key_step_checked or '—'}; dependents: {len(direct)} direct")
        rps = R.load_repoints()
        for d in direct:
            for use in sorted(g.uses[(d, cid)]):
                rps.append({"dependent": d, "from": cid, "to": yid, "use": use, "state": "PROPOSED", "date": stamp,
                            "notes": mode})
            if mode != "free":
                old = by[d]["state"]
                by[d]["state"] = "REBASE-NEEDED" if old == "ACTIVE" else old
                by[d]["state_reason"] = (f"REBASE-NEEDED {stamp}: uses {cid}, superseded by {yid}; still true on "
                                         f"{cid}, rebuild on {yid}") + ("" if old == "ACTIVE" else
                                                                         " || " + by[d].get("state_reason", ""))
                R.log_event("propagate", d, old, by[d]["state"], f"supersede {cid} -> {yid}", a.actor)
                issues.append((f"[rebase] {d} onto {yid}", f"rebase_{R.safe(d)}.md",
                               f"# Rebase {d} onto {yid}\n\n{d} ({by[d]['name']}) uses {cid}@"
                               f"{','.join(sorted(g.uses[(d, cid)]))}. {cid} is SUPERSEDED-VALID (still true) by "
                               f"{yid}, which does not imply it, so the dependent stays correct but should be rebuilt "
                               f"on {yid}.\n\n## What changed\n\n" + "\n".join(f"- {s}" for s in diff)
                               + f"\n\n## Done when\n\n- the step of {by[d]['file']} that uses {cid} is re-proved "
                               f"from {yid} and lemma-checked\n- `propagate.py confirm-repoint {d} --from {cid} --to "
                               f"{yid} --checked-by <reviewer file>`\n", LABELS["rebase"]))
            else:
                issues.append((f"[repoint] check {d}: {cid} -> {yid}", f"repoint_{R.safe(d)}.md",
                               f"# Cheap check: re-point {d} from {cid} to {yid}\n\n{yid} implies {cid} (registry "
                               f"`implies`). Confirm that what {d} uses (`{','.join(sorted(g.uses[(d, cid)]))}`) "
                               f"survives in {yid} (same event/rate/constants), then run `propagate.py "
                               f"confirm-repoint {d} --from {cid} --to {yid} --checked-by <who/file>`; otherwise "
                               f"`reject-repoint` (the dependent simply stays on {cid}, which remains valid).\n",
                               LABELS["repoint"]))
        R.save_repoints(rps)
        R.save_claims(rows)
    else:
        # ------------------------------------------------ correctness rollbacks
        if a.op == "downgrade" and not a.status:
            sys.exit("downgrade needs --status")
        if a.op == "clear" and x["state"] not in ("SUSPECT", "REBASE-NEEDED", "NARROWED"):
            sys.exit(f"{cid} is {x['state']}; clear lifts SUSPECT / REBASE-NEEDED / NARROWED only")
        covered = set(R.split_list(a.still_covers))
        hop = {"patch": lambda uses: any(u.startswith("proof:") for u in uses),
               "narrow": lambda uses: not uses <= covered}.get(a.op, lambda uses: True)
        restored, reverted = [], []
        if a.op == "retract":  # reversibility: restore what this claim superseded, revert confirmed re-points
            restored = [r for r in rows if r.get("superseded_by") == cid and r["state"] == "SUPERSEDED-VALID"]
            reverted = [rp for rp in R.load_repoints() if rp["to"] == cid and rp["state"] == "CONFIRMED"]
        if a.op == "clear":
            paths = {}
        else:
            if reverted:  # recompute the graph as it will be after the reverts
                tmp = {r["id"]: dict(r) for r in rows}
                for rp in reverted:
                    d = tmp[rp["dependent"]]
                    d["depends_on"] = R.join_list(
                        f"{rp['from']}@{R.parse_dep(it)[1]}" if R.resolve(it, ids, aliases, d["ticket"]) == cid
                        and R.parse_dep(it)[1] == rp["use"] else it for it in R.split_list(d["depends_on"]))
                g = R.Graph(list(tmp.values()), aliases)
            paths = {d: p for d, p in g.dependents(cid, hop).items() if by[d]["state"] not in INERT}
        direct = sorted(d for d, p in paths.items() if len(p) == 2)
        report += [f"- restored (were superseded by {cid}): {', '.join(r['id'] for r in restored)}" if restored else "",
                   f"- re-points reverted: {', '.join(rp['dependent'] for rp in reverted)}" if reverted else "",
                   "", "## Impact", ""] + cost(paths, direct, by, False)
        if paths:
            report += ["", "| dependent | uses | becomes | path |", "|---|---|---|---|"]
            report += [f"| {d} | {', '.join(sorted(g.uses.get((d, p[-2]), {'?'})))} | SUSPECT | {' → '.join(p)} |"
                       for d, p in sorted(paths.items())]
        print("\n".join(l for l in report if l is not None))
        if a.dry_run:
            print("\n(dry run: registry unchanged)")
            return
        before = f"{x['state']} v{x['version']}"
        if a.op == "clear":
            x["state"], x["version"] = "ACTIVE", R.bump(x["version"], "minor")
            x["state_reason"] = f"cleared {stamp}: {a.reason}"
        elif a.op == "patch":
            x["version"] = R.bump(x["version"], "minor")
            x["state_reason"] = (f"patched {stamp}: {a.reason}. " + x.get("state_reason", "")).strip()
        elif a.op == "downgrade":
            x["state_reason"] = f"downgraded {stamp} from `{x['status'][:100]}`: {a.reason}"
            x["status"], x["version"] = a.status, R.bump(x["version"], "minor")
        else:
            st = {"retract": "RETRACTED", "narrow": "NARROWED", "deprecate": "DEPRECATED", "suspect": "SUSPECT"}[a.op]
            x["state"], x["state_reason"] = st, f"{st} {stamp}: {a.reason}"
            if a.op in ("retract", "narrow"):
                x["version"] = R.bump(x["version"], "major")
            if a.status:
                x["status"] = a.status
        R.log_event(a.op, cid, before, f"{x['state']} v{x['version']}", a.reason, a.actor)
        for r in restored:
            r["state"], r["superseded_by"] = "ACTIVE", ""
            r["state_reason"] = f"restored {stamp}: its replacement {cid} was retracted ({a.reason})"
            R.log_event("restore", r["id"], "SUPERSEDED-VALID", "ACTIVE", f"{cid} retracted", a.actor)
        if a.op == "retract":
            rps = R.load_repoints()
            for rp in rps:
                if rp["to"] == cid and rp["state"] == "PROPOSED":
                    rp["state"], rp["notes"] = "OBSOLETE", f"{stamp}: {cid} retracted before the check"
            R.save_repoints(rps)
        if reverted:
            rps = R.load_repoints()
            for rp in rps:
                if rp["to"] == cid and rp["state"] == "CONFIRMED":
                    d = by[rp["dependent"]]
                    d["depends_on"] = R.join_list(
                        f"{rp['from']}@{R.parse_dep(it)[1]}" if R.resolve(it, ids, aliases, d["ticket"]) == cid
                        and R.parse_dep(it)[1] == rp["use"] else it for it in R.split_list(d["depends_on"]))
                    rp["state"], rp["notes"] = "REVERTED", f"{stamp}: {cid} retracted"
                    R.log_event("revert-repoint", d["id"], cid, rp["from"], f"{cid} retracted", a.actor)
            R.save_repoints(rps)
        for d, path in paths.items():
            r = by[d]
            old = r["state"]
            r["state"] = "SUSPECT"
            why = f"SUSPECT {stamp}: uses {path[1] if len(path) > 1 else cid} ← {a.op} {cid} ({a.reason}) via " \
                  f"{' -> '.join(path)}"
            r["state_reason"] = why if old == "ACTIVE" else why + " || " + r.get("state_reason", "")
            R.log_event("propagate", d, old, "SUSPECT", why, a.actor)
        if a.op in ("retract", "deprecate", "narrow"):
            decision(a.op, cid, None, None, a.reason, a.actor, f"{len(paths)} dependents SUSPECT; restored: "
                     f"{', '.join(r['id'] for r in restored) or '—'}")
        if a.op == "deprecate":
            with open(ROUTES, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(f"\n| {stamp} | {cid} | target deprecated | {a.reason} | events.log {stamp} |\n")
        R.save_claims(rows)
        groups = {}
        for d in paths:
            groups.setdefault(by[d]["ticket"], []).append(d)
        for t, ds in sorted(groups.items()):
            issues.append((f"[suspect] {t}: {len(ds)} claim(s) after {a.op} {cid}", f"suspect_{R.safe(t)}.md",
                           f"# {t}: {len(ds)} claim(s) SUSPECT after {a.op} of {cid}\n\nReason: {a.reason}\n\n"
                           + "\n".join(f"- {d} ({by[d]['name']}) via {' → '.join(paths[d])}" for d in sorted(ds))
                           + "\n\nFor each: re-check the step that uses the upstream claim. PATCH if it survives "
                             "(`propagate.py clear <id>`), otherwise narrow / retract and propagate.\n",
                           LABELS["dependent"]))
    # ------------------------------------------------ issues
    idir = a.issues_dir or os.path.join(R.INFRA, "issues", f"{stamp}_{a.op}_{R.safe(cid)}")
    os.makedirs(idir, exist_ok=True)
    with open(os.path.join(idir, "00_impact.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(l for l in report if l is not None) + "\n")
    issues.insert(0, (f"[{a.op}] {cid}: {a.reason[:70]}", "00_impact.md", None, LABELS.get(a.op, ["theory"])))
    for title, fn, body, labels in issues:
        if body is not None:
            with open(os.path.join(idir, fn), "w", encoding="utf-8") as fh:
                fh.write(body)
    print(f"\nwrote {len(issues)} issue file(s) to {os.path.relpath(idir, R.ROOT)}")
    if a.gh:
        for title, fn, _, labels in issues:
            print(gh_issue(title, os.path.join(idir, fn), labels))
    print("next: python Theory_work/INFRA/tools/check.py ; python Theory_work/INFRA/tools/assemble.py")


if __name__ == "__main__":
    main()
