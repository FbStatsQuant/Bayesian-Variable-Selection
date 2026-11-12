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
  C12 checkpoint [ERROR] a status source that is a CHECKPOINT_<k>.md changed after ingest (`status_sha256`, the
                          digest recorded at ingest / status change, no longer matches the file) (INFRA R05)
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
Legacy boundary (R03-N1)
  L1 legacy      [ERROR] INFRA/LEGACY_ACCEPTED.tsv differs from what `bvsreg.py legacy-boundary` derives from its tag
                          (hand edit, moved tag, unreadable tag): the boundary is then empty; [WARN] no boundary file
Tombstones (LIFECYCLE §3): a RETRACTED / DEPRECATED claim with `archive:<tag or commit>` in its evidence is hashed,
  status-checked and evidence-checked AS COMMITTED AT THAT REF (its ticket files may have been reverted); a missing
  or mismatching archive is an ERROR (C2-tombstone).
Acceptance mode (HQ, CP3):  check.py --acceptance ID [ID ...]   runs every check above plus, for each named claim:
  A0 accept      [ERROR] unknown id; claim not ACTIVE
  A0 inputs      [ERROR] a consumed claim is not ACTIVE: every claim reached through stmt / proof / bound-bridge
                          edges (transitively), whatever its status text or acks; a direct `@hyp` input that is not
                          ACTIVE unless the status is `conditional on` it (F1)
  A1 gates       [ERROR] headline (headline=yes) without correct:PASS(ev), lit:PASS(ev), necessity:PASS(ev), and
                          better:PASS(ev) or every better-theorem proposal disposed
  A1 evidence    [ERROR] any claim: a gate entry `name:RESULT(ev)` (any result: PASS, FAIL, PENDING, ...; every
                          better-proposal and better-disposition included) whose evidence does not resolve to an
                          existing repository file (first token of ev, plus every later path-like token;
                          `path[:a-b][@commit]`, relative to the repo root, the ticket folder, or the statement /
                          status-source folder; a pinned commit must contain it) (F2, R03-N3)
  A1 correct     [ERROR] checked status (PROVED-CHECKED class) with neither correct:PASS(resolving ev) nor a valid
                          council record (F2: every checked claim, not only headlines)
  A2 better      [ERROR] `better-proposal:<label>(ev)` without its review file, or without
                          `better-disposition:<label>=<declined|adopted|ticket|remark>(ev)`; better:PASS whose evidence
                          mentions a proposal not recorded that way
  A3 assurance   [ERROR] a checked status whose direct input (depends_on or bound bridge) is below that assurance
                          (author-only / unchecked, PARTIAL / SKETCH / CONDITIONAL, OPEN / GAP, or unclassified), unless
                          the input is a DECLARED hypothesis: every edge to it is `ID@hyp`, its id / alias / name occurs
                          (as a whole token) in the hashed statement / premise text, AND the status says
                          `conditional on <its id or name>`. Acks do not waive it.
  A3 condition   [ERROR] a checked claim consuming (stmt / proof, transitively) a conditional result does not carry
                          its condition (`conditional on <W>`) in its status; on accepting the conditional result, each
                          existing checked descendant without it (R06 / Sol-2)
  A4 council     [ERROR] a checked claim without a CP3-PASS council record: `council` =
                          `R<k>; MANIFEST <64-hex>; <seat>=<score> PASS(<review>); <seat>=<score> PASS(<review>)`,
                          two distinct seats and review files, each score >= 8.0 with all gates PASS (R10); the digest
                          is the header of the ticket's reviews/MANIFEST_*.txt and `manifest.py verify` of it passes on
                          the current tree; each review file has exactly one line `COUNCIL-VERDICT round=R<k>
                          manifest=<digest> seat=<seat> score=<x.y> gates=PASS` matching the cell, and no other
                          (malformed or contradictory) COUNCIL-VERDICT line (the `manifest.py bind` rule) (R03-N2);
                          the manifest covers the statement, premise and status-source files, except that a status
                          source that is the ticket's OWN CHECKPOINT_<k>.md is exempt from coverage only if its
                          recorded status_sha256 still matches, its claim ids (REGISTRY blocks + rows sourced there)
                          equal each seat's accepted ids (per-claim table `| id | decision |`), and every review round
                          cited in the status line (`<ROUND>:` / `<ROUND> (<note>):`) resolves to exactly one
                          reviews/<ROUND>_* file quoting a frozen MANIFEST_*.txt digest (INFRA R05)
  A5 accepted    [ERROR] the claim consumes (stmt / proof / bound-bridge edges, transitively; an @hyp edge unless the
                          consumer is `conditional on` it) a checked claim that has neither an `accept` event for its
                          current acceptance identity (`v<version> fp2:<hex>`: row fields, provenance, effective
                          inputs, cited artifact contents; LIFECYCLE §4.1; written by `--record`) nor a row in the
                          verified legacy boundary, or whose record matches but which fails its own acceptance
                          checks on the current tree (revalidation); claims accepted in the same run count as
                          accepted (R03-N1, R04-N1/N2)
  --record       on a PASS (0 ERROR in the whole run) append one `accept` event per named claim to events.log;
                          `--only` (a display filter) is refused together with --acceptance
  Gates are parsed per entry (`name:RESULT(evidence)`, ';'-separated outside parentheses); a gate counts as passed
  only if all its entries are PASS with evidence; unparsable or contradictory entries are A1 ERRORs.
Merge / continuation audit:  check.py --consumed-vs GIT_REF --tickets T [T ...]   (rule 11, R07)
  R7 consumed    [ERROR] a claim consumed by T is not ACTIVE here, absent from / not ACTIVE in the registry at GIT_REF
                          (read with `git show GIT_REF:Theory_work/INFRA/registry/claims.tsv`), or at a higher major
                          version there; [WARN] other version / text difference
Refuses to run while registry/.TXN_INPROGRESS (an unfinished transaction: killed process) or registry/.TXN_FAILED
(a failed restore) exists: run `bvsreg.py recover` (R03-N4, Sol-1).
Exit code 1 if any ERROR (or any WARN with --strict).
"""
from __future__ import annotations

import argparse
import contextlib
import glob
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # never write __pycache__ (tools must not write outside their outputs)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

BLOCKING = {"SUSPECT", "NARROWED", "RETRACTED", "DEPRECATED", "CANDIDATE"}  # REBASE-NEEDED is still true
DISPOSITIONS = ("declined", "adopted", "ticket", "remark")  # recorded outcomes of a better-theorem proposal
ASSURANCE = {2: "proved but unchecked / author-only", 1: "partial / sketch / conditional", 0: "open / gap",
             None: "unclassified status"}


def ref_ok(ref: str) -> bool:
    return R.git("rev-parse", "--verify", "--quiet", ref + "^{commit}")[0] == 0


def run(acceptance=None, consumed=None):
    R.txn_guard()
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
        ref = R.archive_ref(r)
        if ref:  # tombstone: the statement as committed at the archive ref
            if not ref_ok(ref):
                add("ERROR", "C2-tombstone", cid, f"archive ref {ref!r} is not a commit/tag in this repository")
            else:
                with R.at_ref(ref):
                    h = R.claim_hash(r)
                if h != r.get("sha256"):
                    add("ERROR", "C2-tombstone", cid, f"statement {f}:{r.get('lines')} (+ premises) "
                        f"{'unreadable' if h is None else 'does not match its sha256'} at archive {ref}")
            continue
        if R.read_lines(f) is None:
            add("ERROR", "C2-hash", cid, f"statement file missing: {f!r}" + (
                " (a retracted / deprecated claim whose files were reverted needs `archive:<tag>` in its evidence: "
                "propagate.py retract|deprecate --archive, or rollback-ticket)" if r.get("state") in R.DEAD else ""))
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
            ref = R.archive_ref(r)
            if ref:  # tombstone: evidence must stay reachable through the archive ref
                if not any(R.git("cat-file", "-e", f"{ref}:{c.replace(os.sep, '/')}")[0] == 0 for c in cands):
                    add("WARN", "C9-evidence", r["id"], f"evidence file not found at archive {ref}: {p}")
            elif not any(R.repo_file_exists(c) for c in cands):
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
        ref = R.archive_ref(r)  # tombstone: read the status source at the archive when it is there
        ctx = R.at_ref(ref) if ref and path and R.read_lines_at(path, ref) is not None else contextlib.nullcontext()
        with ctx:
            lines = R.read_lines(path) if path else None
            sp = R.parse_span(ln.split(",")[0]) if lines else None
            if lines is None or sp is None:
                add("ERROR", "C10-verbatim", r["id"], f"status_source {src!r} is not a readable path:line (no "
                    "provenance)")
                continue
            stx = r.get("status", "")
            if stx.startswith("UNSPLIT-STATUS: "):
                add("WARN", "C10-unsplit", r["id"], "split part without its own status: inherits the parent's "
                    "verbatim status (the ticket should state per-clause statuses)")
                stx = stx[len("UNSPLIT-STATUS: "):]
            res = R.status_at(stx, src)
        if res == "ok":
            continue
        msg = {"negated": "status is NEGATED at its source (e.g. 'not', 'not yet', 'pending' precedes it)",
               "elsewhere": f"status does not start on {src} (it occurs elsewhere in {path}): fix status_source",
               "missing": f"status {r['status'][:80]!r} not found verbatim in {path}",
               "unreadable": f"status_source {src!r} unreadable"}[res]
        add("ERROR", "C10-verbatim", r["id"], msg)
    # C12 (INFRA R05): a status source that is a CHECKPOINT_<k>.md is frozen at ingest: the digest recorded in
    # status_sha256 must still match the file (any later edit of the checkpoint is flagged)
    for r in rows:
        rec = (r.get("status_sha256") or "").strip()
        if not rec or r["state"] in R.DEAD:
            continue
        cur = R.status_sha(r.get("status_source", ""))
        if cur != rec:
            add("ERROR", "C12-checkpoint", r["id"], f"status source {r.get('status_source', '')!r} "
                + ("is not a readable CHECKPOINT_<k>.md" if not cur else "changed after ingest")
                + f" (status_sha256 {rec[:12]}..., now {(cur or '-')[:12]}...): an ingested checkpoint is frozen; "
                "restore it, or record a status change with registry.py correct-status / propagate.py")
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
        for p in [c.partition("@")[0].strip() for c in R.split_list(r.get("consumes", ""))]:
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
            ref = R.archive_ref(r)  # tombstone: its LaTeX transcription may live only at the archive
            tpath = r["tex"].rpartition(":")[0]
            with (R.at_ref(ref) if ref and R.read_lines_at(tpath, ref) is not None else contextlib.nullcontext()):
                tl = R.span_lines(r["tex"])
            if tl is None:
                add("ERROR", "C11-tex", cid, f"tex span {r['tex']!r} unreadable")
            elif r.get("tex_sha256") and R.text_hash(tl) != r["tex_sha256"]:
                add("ERROR", "C11-tex", cid, "LaTeX transcription changed since its last review against the statement "
                    "(re-check it, then registry.py rehash ID --tex)")
            elif not r.get("tex_sha256"):
                add("WARN" if r.get("headline") == "yes" else "INFO", "C11-tex", cid,
                    "LaTeX transcription never reviewed against the Markdown statement (paper block is flagged)")
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
    # L1 (R03-N1): the frozen legacy acceptance boundary must be exactly what its tag gives
    if not os.path.isfile(R.LEGACY_FILE):
        add("WARN", "L1-legacy", "-", f"no {os.path.basename(R.LEGACY_FILE)}: every checked input of an accepted "
            "claim needs an accept event")
    for p_ in R.legacy_boundary()[1]:
        add("ERROR", "L1-legacy", "-", p_)
    for rp in R.load_repoints():
        if rp.get("state") == "PROPOSED":
            add("INFO", "S9-repoints", rp["dependent"], f"PROPOSED re-point {rp['from']} -> {rp['to']} "
                f"(use {rp.get('use')}) awaiting a check")
    if acceptance:
        acceptance_checks(acceptance, rows, by, ids, aliases, g, add)
    if consumed:
        consumed_vs(consumed[0], consumed[1], rows, by, g, add)
    e = sum(o["severity"] == "ERROR" for o in out)
    w = sum(o["severity"] == "WARN" for o in out)
    return out, e, w, len(rows)


STAMPS = {}  # claim id -> accept stamp of the content this acceptance run examined (for --record)


def statement_text(r) -> str:
    """The hashed text of a claim (statement span + premise spans), whitespace-normalised."""
    parts = [R.span_lines(f"{r.get('file', '')}:{r.get('lines', '')}") or []]
    parts += [R.premise_lines(s) or [] for s in R.split_list(r.get("premises", ""))]
    return re.sub(r"\s+", " ", " ".join(l for p in parts for l in p))


def claim_checks(cid, r, fold, by, aliases, g, memo, add):
    """The per-claim acceptance checks (all but A0-accept and A5): every consumed claim ACTIVE (F1); gate evidence
    resolvable (F2); every checked claim with correctness evidence and a CP3-PASS council record (F2, R10); strength
    gates block headline admission (R05); a checked status may not rest on a less-assured input unless that input is
    an explicit, status-carried hypothesis, inherited by every consumer (R06). Used for the named claims and, by A5
    revalidation (R04-N1), for every accepted input they consume."""
    for d, path, why in R.invalid_inputs(cid, by, g, aliases):
        add("ERROR", "A0-inputs", cid, f"consumes {d}, which is {why} (via {' -> '.join(path)}); repair it, or "
            "remove / re-point the edge; acks and status text do not waive this")
    gts = r.get("gates", "")
    entries, unparsable = R.parse_gates(gts)
    passed = R.passed_gates(gts)
    bad_ev = set()
    for n, res, ev in entries:  # R03-N3: every reference resolves, whatever the result (proposals included)
        if not ev.strip():
            continue
        for tok in R.evidence_refs(ev):
            prob = R.resolve_evidence(tok, r, fold)[2]
            if prob:
                bad_ev.add(n)
                add("ERROR", "A1-evidence", cid, f"gate {n}:{res}: {prob}")
    props = [(res, ev) for n, res, ev in entries if n == "better-proposal"]
    disp = {}
    for n, res, ev in entries:
        if n == "better-disposition":
            lab, _, d = res.partition("=")
            disp[lab] = (d, ev)
    for e_ in unparsable:  # Sol toolfix3 N3.a: never let malformed syntax hide an evidence reference
        add("ERROR", "A1-gates", cid, f"unparsable gate entry {e_[:80]!r} (expected name:RESULT(evidence))")
    if r.get("headline") == "yes":
        seen = {}
        for n, res, ev in entries:
            seen.setdefault(n, set()).add(res)
        for n, rs in sorted(seen.items()):
            if n not in ("better-proposal", "better-disposition") and len(rs) > 1:
                add("ERROR", "A1-gates", cid, f"gate {n} has contradictory results {sorted(rs)}")
        for k in ("correct", "lit", "necessity"):
            if k not in passed:
                add("ERROR", "A1-gates", cid, f"headline without {k}:PASS(<evidence>) (gates: {gts[:120]!r})")
        if "better" not in passed and not props:
            add("ERROR", "A1-gates", cid, "headline without better:PASS(<evidence>) and without a disposed "
                "better-theorem proposal")
        for lab, ev in props:
            if not ev.strip():
                add("ERROR", "A2-better", cid, f"better-theorem proposal {lab} without its review file "
                    f"(better-proposal:{lab}(<review file>))")
            d = disp.get(lab)
            if d is None:
                add("ERROR", "A2-better", cid, f"better-theorem proposal {lab} ({ev}) has no recorded disposition "
                    f"(better-disposition:{lab}=<{'|'.join(DISPOSITIONS)}>(<evidence>))")
            elif d[0] not in DISPOSITIONS or not d[1].strip():
                add("ERROR", "A2-better", cid, f"proposal {lab}: disposition {d[0]!r} must be one of "
                    f"{'|'.join(DISPOSITIONS)} with evidence (a deferral is not a disposition)")
        for lab in sorted(set(disp) - {lab for lab, _ in props}):
            add("WARN", "A2-better", cid, f"disposition for an unrecorded proposal {lab!r}")
        if not props and any(n == "better" and re.search(r"propos", ev, re.I) for n, _, ev in entries):
            add("ERROR", "A2-better", cid, "better:PASS evidence mentions a proposal: record each credible "
                "proposal as better-proposal:<label>(<review>) with better-disposition:<label>=...(<evidence>)")
    else:
        add("INFO", "A1-gates", cid, "not a headline (headline != yes): strength gates not required")
    if R.status_strength(r.get("status", "")) != 3:
        return
    # F2 / R10: correctness evidence and a CP3-PASS council record for EVERY checked claim
    cprobs = R.council_problems(r, fold, list(by.values()))
    for p_ in cprobs:
        add("ERROR", "A4-council", cid, f"council: {p_}")
    if cprobs and ("correct" not in passed or "correct" in bad_ev):
        add("ERROR", "A1-correct", cid, f"checked status {R.status_token(r['status'])!r} without correctness "
            "evidence: neither correct:PASS(<existing review file>) nor a valid council record")
    # R06: assurance of direct inputs; declared hypotheses must be carried by the status, and inherited
    text = None
    st = r.get("status", "")
    for d in g.deps.get(cid, []):
        dr = by[d]
        uses = g.uses[(cid, d)]
        s_d = R.status_strength(dr.get("status", ""))
        if uses == {"hyp"}:
            if not R.weak_or_invalid(dr):
                continue
            text = statement_text(r) if text is None else text
            names_d = R.claim_names(d, by, aliases)
            hit, cond = R.name_hit(text, names_d), R.conditional_on(st, names_d)
            if hit and cond:
                add("INFO", "A3-assurance", cid, f"uses {d}@hyp ({ASSURANCE.get(s_d, s_d)}, {dr['state']}) as a "
                    f"declared hypothesis named in its statement ({hit!r}) and its status is conditional on it "
                    f"({cond!r}); HQ attests it is stated as a hypothesis")
                continue
            add("ERROR", "A3-assurance", cid, f"uses {d}@hyp ({ASSURANCE.get(s_d, s_d)}, {dr['state']}) but "
                + ("" if hit else "does not name it in the hashed statement / premise text")
                + (" and " if not hit and not cond else "")
                + ("" if cond else f"its status {st[:60]!r} is not 'conditional on <{d} or its name>'")
                + "; a conditional result must say so in its status")
            continue
        if s_d == 3 or s_d == "NEG":
            continue
        add("ERROR", "A3-assurance", cid, f"status {R.status_token(st)!r} but uses {d}@"
            f"{','.join(sorted(uses))}, whose assurance is below it ({ASSURANCE.get(s_d, s_d)}: "
            f"{dr.get('status', '')[:80]!r}); check that input, or make it an explicit hypothesis: depend on it "
            "ONLY as `" + d + "@hyp`, name it in the hashed statement / premise text, and write 'conditional on "
            "<it>' in the status; acks do not waive this")
    own = R.conditions(cid, by, g, memo)
    for w, path in sorted(own.items()):
        if len(path) == 2:
            continue  # a direct @hyp condition: checked above
        if not R.conditional_on(st, R.claim_names(w, by, aliases)):
            add("ERROR", "A3-condition", cid, f"consumes the conditional result {path[1]}, which rests on {w} "
                f"(via {' -> '.join(path)}); its status {st[:60]!r} must carry the condition: 'conditional on "
                f"<{w} or its name>'")
    for e_, path in sorted(R.consumers(cid, g).items()):
        er = by[e_]
        if er["state"] in R.DEAD or R.status_strength(er.get("status", "")) != 3:
            continue
        for w in sorted(own):
            if not R.conditional_on(er.get("status", ""), R.claim_names(w, by, aliases)):
                add("ERROR", "A3-condition", cid, f"descendant {e_} (via {' -> '.join(path)}) has the "
                    f"unconditional status {er.get('status', '')[:50]!r} but rests on {cid}'s condition {w}; it "
                    f"must carry 'conditional on <{w} or its name>'")


def acceptance_checks(names, rows, by, ids, aliases, g, add):
    """CP3 acceptance (LIFECYCLE §4, §5.5): A0-accept, the per-claim checks (claim_checks) and A5: every checked claim
    consumed, transitively, carries an accept record for its CURRENT acceptance identity (or is legacy), and still
    passes the per-claim checks on the current tree (R03-N1, R04-N1/N2)."""
    folder = R.ticket_folders()
    memo = {}
    now = {R.resolve(x, ids, aliases) for x in names} - {None}
    records, legacy = R.accept_records(), R.legacy_boundary()[0]
    reval = {}

    def revalidate(d):  # R04-N1: an accepted input must still pass its acceptance checks (memoised)
        if d not in reval:
            errs = []
            claim_checks(d, by[d], folder.get(by[d]["ticket"], ""), by, aliases, g, memo,
                         lambda sev, chk, _i, msg: errs.append(f"{chk}: {msg[:160]}") if sev == "ERROR" else None)
            reval[d] = errs
        return reval[d]
    for ref in names:
        cid = R.resolve(ref, ids, aliases)
        if cid is None:
            add("ERROR", "A0-accept", ref, "unknown claim id")
            continue
        r = by[cid]
        if r["state"] != "ACTIVE":
            add("ERROR", "A0-accept", cid, f"state {r['state']}: only an ACTIVE claim can be accepted")
        claim_checks(cid, r, folder.get(r["ticket"], ""), by, aliases, g, memo, add)
        # R03-N1 / R04-N1: every checked claim it consumes, transitively, carries a durable acceptance of its current
        # identity (or is legacy) and still passes its acceptance checks
        for d, path, why in R.unaccepted_inputs(cid, by, g, aliases, now, records, legacy, revalidate, folder):
            add("ERROR", "A5-accepted", cid, f"consumes the checked claim {d} (via {' -> '.join(path)}), but {why}; "
                f"accept it first (`check.py --acceptance {d} --record`), or use it only as {d}@hyp with a "
                "'conditional on' status")
        STAMPS[cid] = R.accept_stamp(cid, by, g, aliases, folder)


def consumed_vs(ref, tickets, rows, by, g, add):
    """R07 / rule 11: each claim the given ticket(s) consume, compared with the registry committed at `ref`
    (e.g. origin/main): ERROR if it is absent there, not ACTIVE there, or at a higher major version there."""
    rc, txt = R.git("show", f"{ref}:Theory_work/INFRA/registry/claims.tsv")
    if rc != 0:
        add("ERROR", "R7-consumed", "-", f"cannot read the registry at {ref!r}: {txt[:120]}")
        return
    there = R.index(R.read_tsv_text(txt))
    mine = [r["id"] for r in rows if r["ticket"] in tickets]
    if not mine:
        add("ERROR", "R7-consumed", "-", f"no claims of ticket(s) {', '.join(tickets)} here")
    major = lambda v: int(v.split(".")[0]) if R.SEMVER.match(v or "") else -1  # noqa: E731
    seen = set()
    for c in mine:
        for d in g.deps.get(c, []):
            if by[d]["ticket"] in tickets or (c, d) in seen:
                continue
            seen.add((c, d))
            here, t = by[d], there.get(d)
            pre = f"{c} consumes {d} (here {here['state']} v{here['version']})"
            if here["state"] != "ACTIVE":
                add("ERROR", "R7-consumed", c, f"{pre}: not ACTIVE here")
            if t is None:
                add("ERROR", "R7-consumed", c, f"{pre}: absent from the registry at {ref}")
                continue
            if t.get("state") != "ACTIVE":
                add("ERROR", "R7-consumed", c, f"{pre}: {t.get('state')} at {ref} ({t.get('state_reason', '')[:80]})")
            if major(t.get("version", "")) > major(here["version"]):
                add("ERROR", "R7-consumed", c, f"{pre}: v{t.get('version')} at {ref} (the claim changed: re-check "
                    "the use, then rebase onto it)")
            elif t.get("version") != here["version"] or t.get("sha256") != here.get("sha256"):
                add("WARN", "R7-consumed", c, f"{pre}: v{t.get('version')} at {ref} (proof / status / text "
                    "changed: re-check a proof-level use)")


def freeze_violations(rows, sharp, cfg):
    """Freeze criterion (LIFECYCLE §5.3): every hypothesis of every valid headline settled (NECESSARY or >= 2
    distinct failed removal routes), and the latest strategy review and adversarial round are recorded files."""
    out = []
    for r in rows:
        if r.get("headline") == "yes" and r["state"] in R.VALID:
            for a in R.hypotheses(r):
                if not R.settled(r["id"], a, sharp):
                    out.append(f"{r['id']} hypothesis {a} is not settled")
    # failed removal routes must be documented: evidence = readable path:line, distinct by path:line
    for r in rows:
        if r.get("headline") == "yes" and r["state"] in R.VALID:
            for a in R.hypotheses(r):
                if R.necessity(r["id"], a, sharp)[0] == "NECESSARY":
                    continue
                docs = set()
                for s in sharp:
                    if s["claim"] == r["id"] and s["assumption"] == a and s["verdict"] == "FAILED-REMOVAL":
                        k = R.span_key(s.get("evidence", ""))  # first token = path:line, canonicalised
                        if k is not None:
                            docs.add(k)
                if len(docs) < 2:
                    out.append(f"{r['id']} {a}: fewer than 2 failed removal routes with readable path:line evidence")
    # the two reviews must exist and carry an explicit (human-attested) outcome line
    for k in ("last_strategy_review", "last_adversarial_round"):
        v = cfg.get(k, "")
        lines = R.read_lines(v) if v else None
        if lines is None:
            out.append(f"config {k} does not name an existing review file")
        elif not any(l.strip().startswith("FREEZE-OUTCOME: no headline-changing candidate") for l in lines):
            out.append(f"{v} has no line 'FREEZE-OUTCOME: no headline-changing candidate' (attested outcome)")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json")
    ap.add_argument("--quiet", action="store_true", help="summary + ERRORs only")
    ap.add_argument("--strict", action="store_true", help="exit 1 on WARN too")
    ap.add_argument("--only", help="comma-separated check prefixes, e.g. C2,C4,S")
    ap.add_argument("--acceptance", nargs="+", metavar="CLAIM",
                    help="CP3 acceptance: also run A0-A4 for these claims (inputs ACTIVE, evidence, council, "
                    "strength gates, assurance)")
    ap.add_argument("--consumed-vs", metavar="GIT_REF",
                    help="rule 11 / R07: compare each claim consumed by --tickets with the registry at GIT_REF")
    ap.add_argument("--tickets", nargs="+", metavar="TICKET", help="the ticket(s) for --consumed-vs")
    ap.add_argument("--record", action="store_true",
                    help="with --acceptance: on a PASS (0 ERROR), append an `accept` event per claim to events.log "
                    "(the durable acceptance record A5 requires of checked inputs; R03-N1)")
    ap.add_argument("--actor", default="HQ")
    a = ap.parse_args()
    if bool(a.consumed_vs) != bool(a.tickets):
        ap.error("--consumed-vs and --tickets go together")
    if a.record and not a.acceptance:
        ap.error("--record needs --acceptance")
    if a.only and a.acceptance:  # Sol toolfix3 N1.a: a filtered run must never print (or record) an acceptance PASS
        ap.error("--only cannot be combined with --acceptance: the acceptance verdict and --record cover every finding")
    out, e, w, n = run(a.acceptance, (a.consumed_vs, a.tickets) if a.consumed_vs else None)
    if a.only:
        keep = tuple(a.only.split(","))
        out = [o for o in out if o["check"].startswith(keep)]
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for o in sorted(out, key=lambda o: (order[o["severity"]], o["check"], o["id"])):
        if a.quiet and o["severity"] != "ERROR" and not o["check"].startswith("A"):
            continue
        print(f"{o['severity']:5} {o['check']:17} {o['id']:30} {o['message']}")
    counts = {s: sum(o["severity"] == s for o in out) for s in order}
    by_check = {}
    for o in out:
        by_check.setdefault(f"{o['severity']}:{o['check']}", 0)
        by_check[f"{o['severity']}:{o['check']}"] += 1
    print(f"\ncheck.py: {n} claims; {counts['ERROR']} ERROR, {counts['WARN']} WARN, {counts['INFO']} INFO")
    if a.acceptance:
        acc = sum(o["severity"] == "ERROR" and o["check"].startswith("A") for o in out)
        print(f"acceptance ({', '.join(a.acceptance)}): {'REFUSED' if counts['ERROR'] else 'PASS'}; {acc} "
              f"acceptance ERROR, {counts['ERROR'] - acc} other ERROR")
    if a.consumed_vs:
        r7 = [o for o in out if o["check"] == "R7-consumed"]
        print(f"consumed-vs {a.consumed_vs} ({', '.join(a.tickets)}): "
              f"{sum(o['severity'] == 'ERROR' for o in r7)} ERROR, {sum(o['severity'] == 'WARN' for o in r7)} WARN")
    print("by check: " + ", ".join(f"{k}={v}" for k, v in sorted(by_check.items())))
    if a.record:
        if counts["ERROR"]:
            print("record: nothing recorded (acceptance REFUSED)")
        else:
            why = f"check.py --acceptance {' '.join(a.acceptance)}: PASS (0 ERROR)"
            R.write_many([(R.EVENTS, R.events_text(("accept", cid, "", stamp, why, a.actor)
                                                   for cid, stamp in sorted(STAMPS.items())))])
            print("record: accept event written for " + ", ".join(f"{c} ({s_})" for c, s_ in sorted(STAMPS.items())))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"claims": n, "counts": counts, "by_check": by_check, "findings": out}, fh,
                      ensure_ascii=False, indent=1)
    sys.exit(1 if counts["ERROR"] or (a.strict and counts["WARN"]) else 0)


if __name__ == "__main__":
    main()
