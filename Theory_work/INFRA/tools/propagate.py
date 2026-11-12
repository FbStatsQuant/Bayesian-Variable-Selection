"""propagate.py — lifecycle operations on claims, with use-level propagation, decision log and repair issues.

Rules and who may run what: Theory_work/INFRA/LIFECYCLE.md. DRY RUN IS THE DEFAULT: without --apply an operation only
prints its impact report and writes nothing. Every applied operation is written to registry/events.log; decisions also to DECISIONS.md.

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
  clear     ID --reason R                      repaired: SUSPECT / REBASE-NEEDED / NARROWED -> ACTIVE (minor bump);
                                               refused while any consumed claim (stmt / proof edges, transitively)
                                               is not ACTIVE, or a direct @hyp input is not ACTIVE and the status is
                                               not `conditional on` it; acks never suffice (F1)
  retract|deprecate ID ... --archive REF       also mark the row a TOMBSTONE: `archive:REF` in its evidence (REF =
                                               tag / commit where its statement + evidence stay readable after its
                                               ticket's files are reverted; the statement hash must match at REF)
  rollback-ticket TICKET --archive REF --reason R [--as retract|deprecate]
                                               the registry part of rolling back a MERGED ticket, atomically: every
                                               live claim of TICKET is retracted (or deprecated) as a tombstone on
                                               REF, on the CURRENT graph (later dependents become SUSPECT), in a
                                               staged copy; the full check.py runs on that copy; only if it adds no
                                               ERROR is the staged state written (--apply). Dry run: the priced report.
                                               F6: a surviving claim whose premise span lies in the ticket's files reads
                                               it at REF (`path:a-b@archive:REF`), and check.py also runs on the
                                               proposed POST-REVERT tree (the ticket's files removed; exact set with
                                               --merge M: the files M changed, as at M^1); a new ERROR there refuses
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
  coexist   X --with Y --reason R             incomparable: both kept as parallel theorems (needs proved
                                               incomparability on the declared axes and gate parity)
  decline   X --by Y --reason R               decision not to adopt Y (logged)
  remark    X --by Y --reason R               internal-only improvement, not free: logged as a remark, no rebuild
  confirm-repoint D --from X --to Y --checked-by WHO   apply a PROPOSED re-point after the cheap check
  reject-repoint  D --from X --to Y --checked-by WHO   the used fact does not survive: keep D on X
  fail-route X --assumption A --route TEXT --reason R   a failed attempt to remove/weaken A (weak necessity
                                               evidence): sharpness row FAILED-REMOVAL + DECISIONS.md + FAILED_ROUTES.md
Flags: --dry-run, --issues-dir D, --gh (create the issues), --actor A (default HQ),
       --status S --status-source path:line (downgrade / retract / deprecate only: the new verbatim status must
       occur at that source, and it can never be stronger than the current one)
Version policy: retract / narrow = major; patch / downgrade / supersede (of X) / deprecate / clear = minor;
coverage corrections (spans, premises) = patch (registry.py).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.dont_write_bytecode = True  # never write __pycache__ (tools must not write outside their outputs)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

DECISIONS = os.path.join(R.INFRA, "DECISIONS.md")
ROUTES = os.path.join(R.INFRA, "FAILED_ROUTES.md")
INERT = R.DEAD  # SUPERSEDED-VALID claims are still TRUE claims: a correctness change upstream must reach them
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
    with open(R.safe_dest(DECISIONS), "a", encoding="utf-8", newline="\n") as fh:
        if new:
            fh.write("# Decision log\n\n")
        ax = ", ".join(f"{k}={v}" for k, v in (axes or {}).items())
        fh.write(f"\n## {R.today()} — {kind.upper()} {x}" + (f" / {y}" if y else "") + "\n\n"
                 f"- decided by: {actor}\n- reason: {reason}\n" + (f"- axes (Y vs X): {ax}\n" if ax else "")
                 + (f"- {extra}\n" if extra else ""))


def gh_issue(title, body_file, labels):
    from ghapi import issue  # gh CLI if installed, else the REST API with git's stored credential
    return issue(title, body_file, labels)


def passed_gates(row: dict) -> set:
    """Gate names recorded as PASS WITH evidence: `name:PASS(evidence)` (anchored parser, shared with check.py)."""
    return R.passed_gates(row.get("gates", ""))


def status_ok_at(status: str, source: str) -> bool:
    return R.status_at(status, source) == "ok"  # same negation-aware locator as check.py C10


def plan_reverts(cid, rows, ids, aliases, by):
    """For a retraction of cid: which confirmed re-points to cid are undone, and onto what. A re-point is undone
    only if the dependent STILL uses cid through it (a later re-point may have moved it on). The restore target is
    the latest VALID source in that dependent's re-point chain; if none is valid, the dependent keeps its edge to
    cid (and is invalidated with it). Returns [(rp, restore_item or None)] and the set of skipped (moved-on) rps."""
    rps = R.load_repoints()
    plan, moved = [], []
    for rp in rps:
        if rp["to"] != cid or rp["state"] != "CONFIRMED":
            continue
        d = by[rp["dependent"]]
        after = rp.get("after") or f"{cid}@{rp['use']}"
        if after not in R.split_list(d["depends_on"]) + R.split_list(d.get("consumes", "")):
            moved.append(rp)
            continue
        src, use, seen = rp["from"], rp["use"], set()
        while src and by.get(src, {}).get("state") not in R.VALID and src not in seen:
            seen.add(src)
            prev = [q for q in rps if q["dependent"] == d["id"] and q["use"] == use and q["to"] == src
                    and q["state"] in ("CONFIRMED", "REVERTED", "MOVED-ON")]
            src = prev[-1]["from"] if prev else None
        restore = f"{src}@{use}" if src and by.get(src, {}).get("state") in R.VALID else None
        plan.append((rp, restore))
    return plan, moved


def apply_revert(d: dict, rp: dict, restore) -> None:
    """Undo one confirmed re-point onto `restore` (an `id@use` item) or, if None, leave the edge to the retracted
    claim in place. An independent pre-existing edge to the retracted claim is always kept."""
    if restore is None:
        return
    if "consumes" in rp.get("notes", ""):  # a bound bridge in `consumes`
        prop = (rp.get("before") or "").partition("@")[0].strip()
        restore_item = f"{prop}@{restore.partition('@')[0]}"
        cons = R.split_list(d.get("consumes", ""))
        if rp.get("preexisting") != "yes":  # the binding to the retracted claim came only from this re-point
            cons = [c for c in cons if c != rp.get("after")]
        if restore_item not in cons:
            cons.append(restore_item)
        d["consumes"] = R.join_list(cons)
        return
    items = R.split_list(d["depends_on"])
    after = rp.get("after") or f"{rp['to']}@{rp['use']}"
    if rp.get("preexisting") != "yes":
        items = [it for it in items if it != after]
    if restore not in items:
        items.append(restore)
    d["depends_on"] = R.join_list(items)


def revert_edge(d: dict, rp: dict) -> None:
    """Undo one confirmed re-point exactly: put back the recorded `before` item; remove the `after` item only if
    it did not exist before the confirmation (an independent use of the target is an obligation of its own)."""
    items = R.split_list(d["depends_on"])
    after, before = rp.get("after") or f"{rp['to']}@{rp['use']}", rp.get("before") or f"{rp['from']}@{rp['use']}"
    if rp.get("preexisting") != "yes":
        items = [it for it in items if it != after]
    if before not in items:
        items.append(before)
    d["depends_on"] = R.join_list(items)


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


def archive_problems(row: dict, ref: str) -> list[str]:
    """A tombstone's archive must be a commit/tag at which the claim's statement (+ premises) still hashes to its
    registered sha256."""
    if R.git("rev-parse", "--verify", "--quiet", ref + "^{commit}")[0] != 0:
        return [f"archive {ref!r} is not a commit or tag in this repository"]
    with R.at_ref(ref):
        h = R.claim_hash(row)
    if h != row.get("sha256"):
        return [f"{row['id']}: statement {row['file']}:{row['lines']} " + ("unreadable" if h is None else
                "does not match its sha256") + f" at {ref} (tag the commit that holds the current text)"]
    return []


def topo_dependents_first(ids_, g):
    """Order claims so that a claim comes before the claims (in the same set) it depends on."""
    seen, order = set(), []

    def visit(c):
        if c in seen:
            return
        seen.add(c)
        for d in g.deps.get(c, []):
            if d in ids_:
                visit(d)
        order.append(c)

    for c in sorted(ids_):
        visit(c)
    return order[::-1]


KEPT_BY_REVERT = ("Theory_work/INFRA/registry/", "Theory_work/INFRA/DECISIONS.md", "Theory_work/INFRA/FAILED_ROUTES.md",
                  "Theory_work/INFRA/issues/")  # LIFECYCLE §3 step 3 checks these out again after the revert


def ticket_files(a, by, mine) -> dict[str, str]:
    """F6: the repository files the documented revert changes -> {path: '-' (removed) | ref (content as at ref)}.
    With --merge M: exactly the files M changed (as at M^1 after the revert, or removed if M added them).
    Without it: every file under the ticket's folder (tickets.tsv) and the statement files of its claims, removed."""
    out = {}
    if a.merge:
        rc, txt = R.git("diff", "--name-only", f"{a.merge}^1", a.merge)
        if rc != 0:
            sys.exit(f"--merge {a.merge!r}: not a merge commit of this repository ({txt[:200]})")
        for p in txt.splitlines():
            if p and not p.startswith(KEPT_BY_REVERT):
                ok = R.git("cat-file", "-e", f"{a.merge}^1:{p}")[0] == 0
                out[R._pkey(p)] = f"{a.merge}^1" if ok else "-"
        return out
    folder = next((t.get("folder", "") for t in R.load_tickets() if t["ticket"] == a.id), "")
    if folder and os.path.isdir(os.path.join(R.ROOT, folder)):
        for dp, dn, fs in os.walk(os.path.join(R.ROOT, folder)):
            dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
            out.update({R._pkey(os.path.relpath(os.path.join(dp, f), R.ROOT)): "-" for f in fs})
    out.update({R._pkey(by[c]["file"]): "-" for c in mine if by[c].get("file")})
    return out


def archive_premises(a, removed, steps_rows) -> tuple[list, list]:
    """F6: surviving claims (not of the ticket, not dead) whose premise spans lie in the reverted files keep reading
    them as committed at the archive (`path:a-b@archive:<ref>`), provided the text there equals the current text.
    -> (registry.py set steps, blocking problems)."""
    steps, probs = [], []
    for r in steps_rows:
        if r["ticket"] == a.id or r["state"] in R.DEAD:
            continue
        items, changed = [], False
        for it in R.split_list(r.get("premises", "")):
            s, ref = R.split_premise(it)
            if not ref and R._pcase(s.rpartition(":")[0]) in {R._pcase(k) for k in removed}:
                it, changed = f"{s}@{R.ARCHIVE_PREFIX}{a.archive}", True
            items.append(it)
        if not changed:
            continue
        now = R.claim_hash(r)
        if now is None or now != r.get("sha256") or R.claim_hash(dict(r, premises=R.join_list(items))) != now:
            probs.append(f"{r['id']}: its premise spans lie in the reverted files but the statement + premises "
                         f"{'do not hash to its sha256 now' if now != r.get('sha256') else 'read differently at ' + a.archive}"
                         "; fix its provenance before the rollback")
            continue
        steps.append(("registry.py", "set", r["id"], "premises=" + R.join_list(items), "--reason",
                      f"rollback of ticket {a.id}: premise span(s) in its reverted files kept at archive {a.archive}"))
    return steps, probs


def rollback_ticket(a):
    """R02: the registry part of rolling back a merged ticket, done on a staged copy and written all at once.
    F6: dependents' premise spans in the ticket's files move to the archive, and the staged registry is checked
    twice: as written (before the revert) and on the proposed post-revert tree (the ticket's files removed)."""
    rows = R.load_claims()
    by = R.index(rows)
    g = R.Graph(rows)
    mine = [r["id"] for r in rows if r["ticket"] == a.id]
    if not mine:
        sys.exit(f"no registry claims of ticket {a.id!r}")
    op = a.as_
    todo = topo_dependents_first({c for c in mine if by[c]["state"] not in R.DEAD}, g)
    already = [c for c in mine if by[c]["state"] in R.DEAD and not R.archive_ref(by[c])]
    blocking = []
    if not a.archive:
        blocking.append("--archive <tag or commit> is required: where the ticket's statements and evidence stay "
                        "readable after the revert (e.g. git tag -a retracted/<ticket> <current main>)")
    else:
        for c in mine:
            blocking += archive_problems(by[c], a.archive)
    outside = sorted({d for c in mine for d in g.dependents(c) if by[d]["ticket"] != a.id
                      and by[d]["state"] not in R.DEAD})
    print(f"# rollback-ticket {a.id} ({op}, archive {a.archive or '—'})\n\n- reason: {a.reason}\n"
          f"- claims of {a.id}: {len(mine)} ({len(todo)} to {op}; {len(mine) - len(todo)} already dead, "
          f"{len(already)} of them to be marked as tombstones)\n- dependents outside the ticket on the CURRENT graph: "
          f"{len(outside)} ({', '.join(outside[:12])}{' …' if len(outside) > 12 else ''})")
    stage = R.make_stage()
    try:
        steps = [("propagate.py", op, c, "--reason", f"rollback of ticket {a.id}: {a.reason}", "--apply",
                  "--actor", a.actor, *(["--archive", a.archive] if a.archive and not blocking else []))
                 for c in todo]
        steps += [("registry.py", "set", c, "evidence=" + R.join_list(R.split_list(by[c].get("evidence", ""))
                                                                       + [R.ARCHIVE_PREFIX + a.archive]),
                   "--reason", f"tombstone of ticket {a.id} rollback") for c in already if a.archive and not blocking]
        for st_ in steps:
            rc, out = R.run_staged(stage, *st_)
            if rc != 0:
                sys.exit(f"rollback-ticket refused: step {' '.join(st_[:3])} failed (nothing written):\n"
                         f"{out[-1500:]}")
        removed = ticket_files(a, by, mine)
        if a.archive and not blocking:
            psteps, pprobs = archive_premises(a, removed,
                                              R.read_tsv(os.path.join(stage, "registry", "claims.tsv"))[1])
            blocking += pprobs
            for st_ in psteps:
                rc, out = R.run_staged(stage, *st_, "--actor", a.actor)
                if rc != 0:
                    sys.exit(f"rollback-ticket refused: step {' '.join(st_[:3])} failed (nothing written):\n"
                             f"{out[-1500:]}")
        new_rows = R.index(R.read_tsv(os.path.join(stage, "registry", "claims.tsv"))[1])
        changed = [(c, by[c]["state"], new_rows[c]["state"]) for c in sorted(by)
                   if c in new_rows and new_rows[c]["state"] != by[c]["state"]]
        moved_p = [c for c in sorted(by) if c in new_rows and new_rows[c].get("premises") != by[c].get("premises")]
        lost = sorted(set(by) - set(new_rows))
        _, live, _ = R.check_findings()
        rc_st, staged_f, summary = R.check_findings(stage)
        new_err = sorted(f for f in staged_f - live if f[0] == "ERROR")
        with open(os.path.join(stage, R.POST_REVERT_FILE), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("".join(f"{p}\t{ref}\n" for p, ref in sorted(removed.items())))
        _, post_f, summary_pr = R.check_findings(stage)  # the proposed post-revert tree
        new_post = sorted(f for f in post_f - live - staged_f if f[0] == "ERROR")
        print("\n## State changes (staged)\n\n| claim | before | after |\n|---|---|---|")
        print("\n".join(f"| {c} | {b} | {n} |" for c, b, n in changed) or "| — | | |")
        if moved_p:
            print("\n## Premise spans kept at the archive (F6)\n\n" + "\n".join(
                f"- {c}: `{new_rows[c]['premises']}`" for c in moved_p))
        print(f"\n## Staged check.py\n\n- {summary.replace('check.py: ', '')}\n- ERROR introduced by the rollback: "
              f"{len(new_err)}" + "".join(f"\n  - {f[1]} {f[2]}: {f[3]}" for f in new_err))
        print(f"\n## Post-revert check.py (staged registry; {len(removed)} file(s) of {a.id} "
              f"{'as at ' + a.merge + '^1 or removed' if a.merge else 'removed'})\n\n"
              f"- {summary_pr.replace('check.py: ', '')}\n- further ERROR after the revert: {len(new_post)}"
              + "".join(f"\n  - {f[1]} {f[2]}: {f[3]}" for f in new_post)
              + ("" if a.merge else "\n- (file set guessed from the ticket folder and statement files: pass "
                 "--merge <merge commit> for the exact set)"))
        if new_post:
            blocking.append(f"{len(new_post)} new check ERROR(s) on the post-revert tree (a surviving claim reads a "
                            "file the revert removes: move its statement / status source, or fix it first)")
        if lost:
            blocking.append(f"rows lost: {lost}")
        if new_err:
            blocking.append(f"{len(new_err)} new check ERROR(s) on the staged registry")
        if blocking:
            print("\n## Blocking\n\n" + "\n".join(f"- {b}" for b in blocking))
        if a.dry_run:
            print("\n(dry run: nothing written; add --apply. Then revert the ticket's non-registry files, keeping "
                  "these rows: LIFECYCLE §3)")
            return
        if blocking:
            sys.exit("rollback-ticket refused (see Blocking); nothing written")
        with open(os.path.join(stage, "registry", "events.log"), "a", encoding="utf-8", newline="\n") as fh:
            fh.write(R.event_line("rollback-ticket", a.id, "", f"{len(todo)} {op}", f"archive {a.archive}: "
                                  f"{a.reason}", a.actor))  # the summary event is part of the same transaction
        moved = R.commit_stage(stage)
        print(f"\nwritten: {len(moved)} file(s) ({', '.join(os.path.basename(m) for m in moved[:8])}"
              f"{' …' if len(moved) > 8 else ''})\nnext (LIFECYCLE §3): git revert -m 1 --no-commit <merge>; "
              "git checkout HEAD -- Theory_work/INFRA/registry Theory_work/INFRA/DECISIONS.md "
              "Theory_work/INFRA/FAILED_ROUTES.md Theory_work/INFRA/issues; python Theory_work/INFRA/tools/check.py")
    finally:
        import shutil
        shutil.rmtree(stage, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("op", choices=["patch", "downgrade", "narrow", "retract", "deprecate", "suspect", "clear",
                                   "promote", "supersede", "coexist", "decline", "remark", "confirm-repoint",
                                   "reject-repoint", "fail-route", "rollback-ticket"])
    ap.add_argument("id")
    ap.add_argument("--reason", default="")
    ap.add_argument("--status")
    ap.add_argument("--status-source", default="")
    ap.add_argument("--still-covers", default="")
    ap.add_argument("--by")
    ap.add_argument("--with", dest="with_")
    ap.add_argument("--axes", default="")
    ap.add_argument("--key-step-checked", default="")
    ap.add_argument("--parity-with")
    ap.add_argument("--no-reference", default="", help="promote without a predecessor: the reason")
    ap.add_argument("--from", dest="from_")
    ap.add_argument("--to")
    ap.add_argument("--checked-by", default="")
    ap.add_argument("--assumption")
    ap.add_argument("--route", default="")
    ap.add_argument("--dry-run", action="store_true", help="(default) print the impact report, write nothing")
    ap.add_argument("--apply", action="store_true",
                    help="actually write: registry/, DECISIONS.md, FAILED_ROUTES.md, issues/ (all under Theory_work/INFRA)")
    ap.add_argument("--issues-dir")
    ap.add_argument("--gh", action="store_true")
    ap.add_argument("--actor", default="HQ")
    ap.add_argument("--archive", default="", help="retract / deprecate / rollback-ticket: tombstone archive ref")
    ap.add_argument("--as", dest="as_", default="retract", choices=["retract", "deprecate"],
                    help="rollback-ticket: retract (default) or deprecate the ticket's claims")
    ap.add_argument("--merge", default="", help="rollback-ticket: the ticket's merge commit (exact set of files the "
                    "revert changes, for the post-revert check)")
    a = ap.parse_args()
    a.dry_run = a.dry_run or not a.apply  # nothing is ever written without --apply
    if a.issues_dir:  # issue files may only go under Theory_work/INFRA/issues
        root = os.path.realpath(os.path.join(R.INFRA, "issues"))
        if os.path.commonpath([os.path.realpath(a.issues_dir), root]) != root:
            sys.exit("--issues-dir must be inside Theory_work/INFRA/issues")
    if a.gh and not a.apply:
        sys.exit("--gh needs --apply")
    if not a.reason and a.op not in ("confirm-repoint", "reject-repoint"):
        sys.exit("--reason is required")
    if a.archive and a.op not in ("retract", "deprecate", "rollback-ticket"):
        sys.exit(f"--archive is not accepted for {a.op}")
    if a.merge and a.op != "rollback-ticket":
        sys.exit(f"--merge is not accepted for {a.op}")
    if a.op == "rollback-ticket":
        return rollback_ticket(a)

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
        problems = []
        if a.op == "confirm-repoint":
            if by[dst]["state"] != "ACTIVE":
                problems.append(f"destination {dst} is {by[dst]['state']}, not ACTIVE")
            for rp in hit:
                if rp.get("from_version") and rp["from_version"] != by[src]["version"] or \
                        rp.get("to_version") and rp["to_version"] != by[dst]["version"]:
                    problems.append(f"stale proposal ({rp['use']}): versions changed since it was proposed "
                                    f"({rp.get('from_version')}->{by[src]['version']}, "
                                    f"{rp.get('to_version')}->{by[dst]['version']}); re-run supersede --dry-run")
            uses_now = {R.parse_dep(it)[1] for it in R.split_list(x["depends_on"])
                        if R.resolve(it, ids, aliases, x["ticket"]) == src}
            uses_now |= {"proof:" + it.partition("@")[0].strip() for it in R.split_list(x.get("consumes", ""))
                         if "@" in it and R.resolve(it.partition("@")[2], ids, aliases, x["ticket"]) == src}
            for rp in hit:
                if rp["use"] not in uses_now:
                    problems.append(f"{cid} no longer uses {src}@{rp['use']}")
            if dst in g.dependents(cid) or cid == dst:
                problems.append(f"{dst} depends on {cid}: re-pointing would create a cycle")
        print("\n".join(report + [f"- {a.op}: {cid} uses {src} -> {dst}, checked by {a.checked_by}"]
                              + [f"- BLOCKING: {p_}" for p_ in problems]))
        if problems:
            sys.exit(f"{a.op} refused")
        if a.dry_run:
            return
        for rp in hit:
            rp.update(state="CONFIRMED" if a.op == "confirm-repoint" else "REJECTED", checked_by=a.checked_by,
                      date=stamp)
        if a.op == "confirm-repoint":
            items = R.split_list(x["depends_on"])
            cons = R.split_list(x.get("consumes", ""))
            for rp in hit:
                if rp["use"].startswith("proof:") and any(
                        "@" in c and R.resolve(c.partition("@")[2], ids, aliases, x["ticket"]) == src and
                        "proof:" + c.partition("@")[0].strip() == rp["use"] for c in cons):
                    p_ = rp["use"][len("proof:"):]
                    before = next(c for c in cons if c.partition("@")[0].strip() == p_ and
                                  R.resolve(c.partition("@")[2], ids, aliases, x["ticket"]) == src)
                    after = f"{p_}@{dst}"
                    kept = next((c for c in cons if c.partition("@")[0].strip() == p_ and
                                 R.resolve(c.partition("@")[2], ids, aliases, x["ticket"]) == dst), None)
                    pre = kept is not None
                    if pre:
                        after = kept  # the exact item that stays, whatever alias / local spelling it uses
                    cons = [c for c in cons if c != before] + ([] if pre else [after])
                    rp.update(before=before, after=after, preexisting="yes" if pre else "no",
                              notes=(rp.get("notes", "") + " consumes"))
                    continue
                before = next(it for it in items if R.resolve(it, ids, aliases, x["ticket"]) == src
                              and R.parse_dep(it)[1] == rp["use"])
                after = f"{dst}@{rp['use']}"
                pre = any(R.resolve(it, ids, aliases, x["ticket"]) == dst and R.parse_dep(it)[1] == rp["use"]
                          for it in items)
                items = [it for it in items if it != before] + ([] if pre else [after])
                rp.update(before=before, after=after, preexisting="yes" if pre else "no")
            x["depends_on"] = R.join_list(items)
            x["consumes"] = R.join_list(cons)
        open_left = [rp for rp in rps if rp["dependent"] == cid and rp["state"] == "PROPOSED"]
        if x["state"] == "REBASE-NEEDED" and not open_left:
            x["state"], x["state_reason"] = "ACTIVE", f"rebase obligations resolved {stamp} (last: {src} -> {dst}, " \
                                                      f"{a.op}, checked by {a.checked_by})"
        R.save_repoints(rps)
        R.save_claims(rows)
        R.log_event(a.op, cid, src, dst, f"checked by {a.checked_by} {a.reason}", a.actor)
        return
    if a.op == "fail-route":
        if not (a.assumption and a.route):
            sys.exit("fail-route needs --assumption and --route")
        if R.span_lines(a.route.split()[0]) is None:
            sys.exit("--route must start with a readable path:line documenting the failed attempt")
        print("\n".join(report + [f"- failed removal of {a.assumption}: {a.route}"]))
        if a.dry_run:
            return
        sh = R.load_sharpness()
        sh.append({"claim": cid, "assumption": a.assumption, "verdict": "FAILED-REMOVAL", "evidence": a.route,
                   "notes": f"{stamp}: {a.reason}"})
        R.write_tsv(R.SHARPNESS, R.SHARPNESS_COLUMNS, sh)
        decision("failed sharpening", cid, a.assumption, None, f"{a.route} — {a.reason}", a.actor,
                 f"failed removal routes for this pair now: {R.necessity(cid, a.assumption, sh)[1]}")
        with open(R.safe_dest(ROUTES), "a", encoding="utf-8", newline="\n") as fh:
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
        problems = []
        if a.op == "coexist":
            if x["state"] != "ACTIVE" or y["state"] != "ACTIVE":
                problems.append(f"both must be ACTIVE ({cid} {x['state']}, {yid} {y['state']})")
            if R.verdict(axes) != "incomparable":
                problems.append(f"verdict is {R.verdict(axes)}, not incomparable: declare every axis with --axes "
                                "(coexist needs a proved trade-off), or use supersede / decline")
            gap = sorted(passed_gates(x) - passed_gates(y))
            if gap:
                problems.append(f"assurance parity: {yid} lacks gates {gap} that {cid} passed")
            if R.config().get("freeze") == "yes" and "yes" in (x.get("headline"), y.get("headline")):
                problems.append("FROZEN: coexist changes the headline set")
        if yid == cid:
            problems.append("X and Y are the same claim")
        print("\n".join(report + [f"- axes (Y vs X): {axes} -> {R.verdict(axes)}"]
                              + [f"- BLOCKING: {p_}" for p_ in problems]))
        if problems:
            sys.exit(f"{a.op} refused")
        if a.dry_run:
            return
        if a.op == "coexist":
            for u, v in ((x, y), (y, x)):
                u["coexists_with"] = R.join_list(dict.fromkeys(R.split_list(u.get("coexists_with", "")) + [v["id"]]))
            x["notes"] = (x.get("notes", "") + f" [{stamp}: parallel theorem to {yid} (COEXIST: incomparable)]").strip()
            R.save_claims(rows)
        decision(a.op, cid, yid, axes, a.reason, a.actor)
        R.log_event(a.op, cid, "", yid, a.reason, a.actor)
        return
    if a.op == "promote":
        if x["state"] != "CANDIDATE":
            sys.exit(f"{cid} is {x['state']}, not CANDIDATE")
        need_gates = ["correct"]
        if not a.parity_with and not a.no_reference:
            sys.exit("promote needs --parity-with <the claim it would replace> (or --no-reference REASON for a "
                     "genuinely new result)")
        have = passed_gates(x)
        if a.parity_with:
            need_gates += sorted(passed_gates(by[need(a.parity_with, "--parity-with")]))
        missing = sorted({k for k in need_gates if k not in have})
        if R.config().get("freeze") == "yes" and x.get("headline") == "yes" and not (
                a.parity_with and need(a.parity_with, "--parity-with") in R.implies_closure(rows, cid, aliases)):
            sys.exit("FROZEN: a new headline may only enter as a free replacement (it must imply --parity-with)")
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
        if yid == cid:
            problems.append("X and Y are the same claim")
        if x["state"] != "ACTIVE":
            problems.append(f"X is {x['state']}: only an ACTIVE claim can be superseded")
        if y["state"] != "ACTIVE":
            problems.append(f"Y is {y['state']}: it must pass the same gates as X first (promote); keep working on X")
        missing = sorted(passed_gates(x) - passed_gates(y))
        if missing:
            problems.append(f"assurance parity: Y lacks {missing}")
        if free:
            pass  # a verified implication Y ⇒ X settles dominance; the axes are informational
        elif v in ("incomparable", "dominated"):
            problems.append(f"Y does not dominate X ({v}): use `coexist` (or `decline`)")
        elif v == "undetermined":
            problems.append("some axes unknown: declare them with --axes rate=better,scope=equal,...")
        elif v == "equal":
            problems.append("not strictly better on any axis: use `decline` or `remark`")
        if mode == "internal-only":
            problems.append("internal-only and not free: log it with `remark`, no rebuild")
        if mode == "headline-changing" and not a.key_step_checked:
            problems.append("headline-changing: needs --key-step-checked <evidence that Y's key new step was "
                            "independently checked>")
        if R.config().get("freeze") == "yes" and mode != "free":
            problems.append("FROZEN: only free supersessions (Y ⇒ X) allowed")
        if yid in g.dependents(cid):
            problems.append(f"{yid} itself depends on {cid}: superseding would orphan the replacement's own proof")
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
            print("\n(dry run: nothing written; add --apply to write)")
            return
        x["state"], x["superseded_by"], x["version"] = "SUPERSEDED-VALID", yid, R.bump(x["version"], "minor")
        x["state_reason"] = f"SUPERSEDED-VALID {stamp} by {yid} ({mode}): {a.reason}"
        R.log_event("supersede", cid, "ACTIVE", f"SUPERSEDED-VALID by {yid}", a.reason, a.actor)
        decision("supersede", cid, yid, axes, a.reason, a.actor,
                 f"class {mode}; key step check: {a.key_step_checked or '—'}; dependents: {len(direct)} direct")
        rps = R.load_repoints()
        for d in direct:
            for use in sorted(g.uses[(d, cid)]):
                rps.append({"dependent": d, "from": cid, "to": yid, "use": use, "from_version": x["version"],
                            "to_version": y["version"], "state": "PROPOSED", "date": stamp, "notes": mode})
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
        if a.status:
            if a.op not in ("downgrade", "retract", "deprecate"):
                sys.exit(f"--status is not accepted for {a.op}")
            if not status_ok_at(a.status, a.status_source):
                sys.exit("--status must occur verbatim at --status-source path:line (± 3 lines)")
            so, sn = R.status_strength(x["status"]), R.status_strength(a.status)
            if isinstance(so, int) and isinstance(sn, int) and sn > so:
                sys.exit(f"refused: the new status is stronger ({sn} > {so}); upgrades need a ticket result")
        if a.archive:  # tombstone: the statement must stay readable (and unchanged) at the archive ref
            probs = archive_problems(x, a.archive)
            if probs:
                sys.exit("refused: " + "; ".join(probs))
            report.append(f"- tombstone: row kept, statement + evidence archived at `{a.archive}`")
        if a.op == "clear":
            if x["state"] not in ("SUSPECT", "REBASE-NEEDED", "NARROWED"):
                sys.exit(f"{cid} is {x['state']}; clear lifts SUSPECT / REBASE-NEEDED / NARROWED only")
            # F1: every consumed claim (transitively through stmt / proof edges) must be ACTIVE; a non-ACTIVE @hyp
            # input only if the status is `conditional on` it (R06). Acks never suffice.
            bad_in = R.invalid_inputs(cid, by, g, aliases)
            if bad_in:
                sys.exit("clear refused: consumed claims not ACTIVE: " + "; ".join(
                    f"{d} {why} via {' -> '.join(p_)}" for d, p_, why in bad_in) + " (repair them first, or remove / "
                    "re-point the edge, or declare it `@hyp` with a 'conditional on' status; an ack is not enough)")
            open_rp = [rp for rp in R.load_repoints() if rp["dependent"] == cid and rp["state"] == "PROPOSED"]
            if open_rp:
                sys.exit(f"clear refused: {len(open_rp)} re-point proposal(s) still open for {cid}")
        covered = set(R.split_list(a.still_covers))
        hop = {"patch": lambda uses: any(u.startswith("proof:") for u in uses),
               "narrow": lambda uses: not uses <= covered}.get(a.op, lambda uses: True)
        restored, reverted = [], []
        if a.op == "retract":  # reversibility: restore what this claim superseded, revert confirmed re-points
            restored = [r for r in rows if r.get("superseded_by") == cid]
            reverted, moved = plan_reverts(cid, rows, ids, aliases, by)
        if a.op == "clear":
            paths = {}
        else:
            if reverted:  # the impact is computed on the graph AS IT WILL BE after the reverts (transitive)
                tmp = {r["id"]: dict(r) for r in rows}
                for rp, restore in reverted:
                    apply_revert(tmp[rp["dependent"]], rp, restore)
                g = R.Graph(list(tmp.values()), aliases)
            paths = {d: p for d, p in g.dependents(cid, hop).items() if by[d]["state"] not in INERT}
        direct = sorted(d for d, p in paths.items() if len(p) == 2)
        report += [f"- restored (were superseded by {cid}): {', '.join(r['id'] for r in restored)}" if restored else "",
                   (f"- re-points reverted: " + ", ".join(f"{rp['dependent']} -> {rs or 'kept on ' + cid}"
                                                           for rp, rs in reverted)) if reverted else "",
                   "", "## Impact", ""] + cost(paths, direct, by, False)
        if paths:
            report += ["", "| dependent | uses | becomes | path |", "|---|---|---|---|"]
            report += [f"| {d} | {', '.join(sorted(g.uses.get((d, p[-2]), {'?'})))} | SUSPECT | {' → '.join(p)} |"
                       for d, p in sorted(paths.items())]
        print("\n".join(l for l in report if l is not None))
        if a.dry_run:
            print("\n(dry run: nothing written; add --apply to write)")
            return
        before = f"{x['state']} v{x['version']}"
        if a.op == "clear":
            sb = x.get("superseded_by", "")
            back = "SUPERSEDED-VALID" if sb and by.get(sb, {}).get("state") in R.VALID else "ACTIVE"
            if back == "ACTIVE":
                x["superseded_by"] = ""
            x["state"], x["version"] = back, R.bump(x["version"], "minor")
            x["state_reason"] = f"cleared {stamp}: {a.reason}"
        elif a.op == "patch":
            x["version"] = R.bump(x["version"], "minor")
            x["state_reason"] = (f"patched {stamp}: {a.reason}. " + x.get("state_reason", "")).strip()
        elif a.op == "downgrade":
            x["state_reason"] = f"downgraded {stamp} from `{x['status'][:100]}`: {a.reason}"
            x["status"], x["status_source"], x["version"] = a.status, a.status_source, R.bump(x["version"], "minor")
            x["status_sha256"] = R.status_sha(a.status_source)  # INFRA R05
        else:
            st = {"retract": "RETRACTED", "narrow": "NARROWED", "deprecate": "DEPRECATED", "suspect": "SUSPECT"}[a.op]
            x["state"], x["state_reason"] = st, f"{st} {stamp}: {a.reason}"
            if a.op in ("retract", "narrow"):
                x["version"] = R.bump(x["version"], "major")
            elif a.op == "deprecate":
                x["version"] = R.bump(x["version"], "minor")
            if a.status:
                x["status"], x["status_source"] = a.status, a.status_source
                x["status_sha256"] = R.status_sha(a.status_source)  # INFRA R05
            if a.archive:
                x["evidence"] = R.join_list(dict.fromkeys(R.split_list(x.get("evidence", ""))
                                                          + [R.ARCHIVE_PREFIX + a.archive]))
        R.log_event(a.op, cid, before, f"{x['state']} v{x['version']}", a.reason, a.actor)
        for r in restored:
            old = r["state"]
            r["superseded_by"] = ""
            if old == "SUPERSEDED-VALID":  # still valid: back in service
                r["state"] = "ACTIVE"
                r["state_reason"] = f"restored {stamp}: its replacement {cid} was retracted ({a.reason})"
            else:  # invalidated meanwhile: stays as it is, history kept in the reason
                r["state_reason"] = (r.get("state_reason", "") + f" || replacement {cid} retracted {stamp}; "
                                     "not restored (own state not valid)")
            R.log_event("restore", r["id"], old, r["state"], f"{cid} retracted", a.actor)
        if a.op == "retract":
            rps = R.load_repoints()
            for rp in rps:
                if rp["to"] == cid and rp["state"] == "PROPOSED":
                    rp["state"], rp["notes"] = "OBSOLETE", f"{stamp}: {cid} retracted before the check"
            R.save_repoints(rps)
        if a.op == "retract" and (reverted or moved):
            rps = R.load_repoints()
            key = lambda q: (q["dependent"], q["from"], q["to"], q["use"], q.get("date", ""))  # noqa: E731
            plan = {key(rp): rs for rp, rs in reverted}
            moved_keys = {key(rp) for rp in moved}
            for rp in rps:
                k = key(rp)
                if k in plan:
                    d = by[rp["dependent"]]
                    apply_revert(d, rp, plan[k])
                    rp["state"] = "REVERTED" if plan[k] else "CONFIRMED-DEAD"
                    rp["notes"] = f"{stamp}: {cid} retracted; " + (f"restored onto {plan[k]}" if plan[k] else
                                                                     "no valid predecessor, edge kept")
                    R.log_event("revert-repoint", d["id"], cid, plan[k] or "-", f"{cid} retracted", a.actor)
                elif k in moved_keys:
                    rp["state"], rp["notes"] = "MOVED-ON", f"{stamp}: {cid} retracted after a later re-point"
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
            with open(R.safe_dest(ROUTES), "a", encoding="utf-8", newline="\n") as fh:
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
    os.makedirs(R.safe_dest(idir), exist_ok=True)
    with open(R.safe_dest(os.path.join(idir, "00_impact.md")), "w", encoding="utf-8") as fh:
        fh.write("\n".join(l for l in report if l is not None) + "\n")
    issues.insert(0, (f"[{a.op}] {cid}: {a.reason[:70]}", "00_impact.md", None, LABELS.get(a.op, ["theory"])))
    for title, fn, body, labels in issues:
        if body is not None:
            with open(R.safe_dest(os.path.join(idir, fn)), "w", encoding="utf-8") as fh:
                fh.write(body)
    print(f"\nwrote {len(issues)} issue file(s) to {os.path.relpath(idir, R.ROOT)}")
    if a.gh:
        for title, fn, _, labels in issues:
            print(gh_issue(title, os.path.join(idir, fn), labels))
    print("next: python Theory_work/INFRA/tools/check.py ; python Theory_work/INFRA/tools/assemble.py")


if __name__ == "__main__":
    main()
