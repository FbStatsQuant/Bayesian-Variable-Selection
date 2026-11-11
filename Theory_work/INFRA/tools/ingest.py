"""ingest.py — add new tickets' claims, or split bundled claims, into the LIVE registry (validated, logged).

  ingest.py claims FRAGMENT.jsonl|REPORT.md [--apply | --staged]
      one claim per JSONL line in the transcription schema (registry/fragments/BRIEF.md) plus the registry schema
      keys `premises`, `consumes` (bound bridges `P:X@<claim>` create proof-use edges), `method_commit`,
      `method_components`, `headline`, `binding` (binding-map rows) and `strength` (BRIEF_STRENGTH.md: assumptions,
      consumes, conclusion, rate, scope, implies, sharpness, binding, gates, method_commit, notes). A `.md` path is
      read as a Wave 3 REPORT: every REGISTRY block in it (templates/ASSUMPTION_MAP.md format) is converted first.
      New ids only; each status must start verbatim (un-negated) on its status_source; a missing status is allowed
      (WARN in check). Adds a tickets.tsv row for unknown tickets.
  ingest.py splits SPLITS.tsv [--apply | --staged]
      split spec (registry/fragments/BRIEF_SPLIT.md): `part` rows create child claims; a child without its own
      status gets `UNSPLIT-STATUS: <parent status verbatim>` (checked against the parent's source; never stronger);
      the parent then depends on every part (@stmt) and `implies` it; `repoint` rows move a dependent's edge from
      the parent to the part it uses.
  ingest.py convert REPORT.md
      print the REPORT's REGISTRY blocks as ingest JSONL (paths made repo-relative from the REPORT's folder);
      exit 1 if a block cannot be converted exactly (unknown field, unparsable item).

ALL OR NOTHING: any problem (unknown field, unresolvable reference, unreadable span, non-verbatim status, duplicate
id, ...) is printed, NOTHING is written and the exit code is 1 — with or without --apply.
  (default)   dry run: validate and print what would change.
  --apply     validate, then write every registry file through .tmp siblings (all or none).
  --staged    validate, apply to a disposable COPY of the registry (BVS_STAGE_INFRA), run the full check.py on that
              copy and print its result (ERROR findings the fragment introduces are listed separately); the live
              registry is never touched. Exit code = check.py's on the staged copy (1 on any ERROR).
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True  # never write __pycache__ (tools must not write outside their outputs)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bvsreg as R  # noqa: E402

UNSPLIT = "UNSPLIT-STATUS: "
# the supported schema; anything else is REJECTED (never silently dropped)
TOP_KEYS = {"ticket", "local_id", "kind", "name", "short", "file", "lines", "premises", "status", "status_source",
            "evidence", "council", "depends_on", "method", "method_commit", "method_components", "falsification",
            "notes", "headline", "consumes", "binding", "strength"}
STRENGTH_KEYS = {"id", "headline", "assumptions", "consumes", "conclusion", "rate", "scope", "implies", "sharpness",
                 "binding", "gates", "method_commit", "notes"}
SHARP_KEYS = {"assumption", "verdict", "evidence", "notes"}
BIND_KEYS = {"assumption", "binding_claim", "mechanism", "signals", "notes"}
ASM_KEYS = {"id", "kind", "shared", "name", "statement", "source", "implies", "bridge", "notes"}
PART_FIELDS = {"local_id", "kind", "name", "file", "lines", "premises", "status", "status_source", "depends_on",
               "notes"}


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


def as_list(v):
    if v is None or v == "":
        return []
    return [str(x) for x in v] if isinstance(v, list) else R.split_list(str(v))


# ---------------------------------------------------------------- REPORT.md REGISTRY block -> JSONL
BLOCK_KEYS = {"claim", "kind", "statement", "premises", "status", "status_source", "assumptions", "consumes",
              "conclusion", "rate", "scope", "depends_on", "implies", "sharpness", "binding", "gates", "name",
              "short", "evidence", "council", "method", "method_commit", "method_components", "falsification",
              "notes", "headline"}
EMPTY = re.compile(r"^\s*(none\b.*|—.*|-|n/a)?\s*$", re.I)
SPAN = re.compile(r"^(\S+):(\d+(?:-\d+)?)$")


def split_top(s: str, sep: str) -> list[str]:
    """Split at occurrences of `sep` outside (), [], {}."""
    out, depth, cur, i = [], 0, "", 0
    while i < len(s):
        c = s[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth = max(0, depth - 1)
        if depth == 0 and s.startswith(sep, i):
            out.append(cur)
            cur, i = "", i + len(sep)
            continue
        cur += c
        i += 1
    out.append(cur)
    return [x.strip() for x in out]


def convert_report(path: str):
    """REGISTRY blocks of a REPORT.md -> ([json objects], [problems]). Paths are relative to the REPORT's folder
    unless they start with Theory_work/."""
    base = os.path.dirname(os.path.relpath(os.path.abspath(path), R.ROOT)).replace("\\", "/")

    def rel(p):
        p = p.strip().strip("`")
        return p if p.startswith("Theory_work/") or not base else f"{base}/{p}"

    def span(v, what, probs):
        m = SPAN.match(v.strip().strip("`"))
        if not m:
            probs.append(f"{what} {v!r} is not path:a-b")
            return None, None
        return rel(m.group(1)), m.group(2)

    lines = open(path, encoding="utf-8").read().splitlines()
    blocks, i = [], 0
    while i < len(lines):
        if lines[i].strip() == "REGISTRY":
            # the block runs to a closing fence, a heading or the next REGISTRY; blank lines inside it are skipped,
            # and after a blank line the block continues while lines look like `field:` (an unknown field is then
            # reported, never dropped); other prose after a blank line ends it
            body, j, gap = [], i + 1, False
            while j < len(lines):
                t_ = lines[j].strip()
                if t_.startswith(("```", "#")) or t_ == "REGISTRY":
                    break
                if not t_:
                    gap = True
                elif gap and not re.match(r"^[a-z_]+:\s", t_):
                    break
                else:
                    body.append((j + 1, t_))
                j += 1
            blocks.append((i + 1, body))
            i = j
        else:
            i += 1
    out, problems = [], []
    for start, body in blocks:
        f, probs = {}, []
        for ln, text in body:
            for seg in split_top(text, " | "):
                m = re.match(r"([a-z_]+):\s*(.*)$", seg, re.S)
                if not m or m.group(1) not in BLOCK_KEYS:
                    probs.append(f"line {ln}: unknown field in {seg[:60]!r} (fields: {', '.join(sorted(BLOCK_KEYS))})")
                    continue
                if m.group(1) in f:
                    probs.append(f"line {ln}: field {m.group(1)} given twice")
                f[m.group(1)] = m.group(2).strip()
        cid = f.get("claim", "")
        t, _, loc = cid.partition(":")
        if not (t and loc):
            probs.append(f"claim {cid!r} is not <TICKET>:<local_id>")
        j = {"ticket": t, "local_id": loc, "kind": f.get("kind", "")}
        for k in ("name", "short", "council", "method", "method_commit", "notes"):
            if k in f:
                j[k] = f[k]
        if "headline" in f:
            j["headline"] = f["headline"].lower()
        j["file"], sp = span(f.get("statement", ""), "statement", probs)
        if sp:
            a, _, b = sp.partition("-")
            j["lines"] = [int(a), int(b or a)]
        prem = []
        if not EMPTY.match(f.get("premises", "")):
            for it in split_top(f["premises"], ";"):
                pf, ps = span(it, "premise", probs)
                if pf:
                    prem.append(f"{pf}:{ps}")
        j["premises"] = prem
        j["status"] = f.get("status", "")
        if f.get("status_source"):
            m = SPAN.match(f["status_source"])
            j["status_source"] = f"{rel(m.group(1))}:{m.group(2)}" if m else f["status_source"]
            if not m:
                probs.append(f"status_source {f['status_source']!r} is not path:line")
        for k in ("evidence", "method_components", "falsification"):
            if k in f:
                j[k] = split_top(f[k], ";")
        for k in ("depends_on", "consumes"):
            items = [] if EMPTY.match(f.get(k, "")) else split_top(f[k], ";")
            for it in items:
                if re.search(r"\s", it):
                    probs.append(f"{k} item {it!r} contains spaces (one id[@use] per item, '; '-separated)")
            j[k] = items
        notes = [j["notes"]] if j.get("notes") else []
        sgt = {}
        if "assumptions" in f:
            items = []
            for it in ([] if EMPTY.match(f["assumptions"]) else split_top(f["assumptions"], ";")):
                m = re.match(r"^([AP]:[^\s(]+)\s*(?:\((.*)\))?\s*$", it, re.S)
                if not m:
                    probs.append(f"assumption item {it!r}: expected `A:ID` or `A:ID (new | name | statement | "
                                 "source | shared yes|no | bridge ID)`")
                    continue
                aid, paren = m.group(1), (m.group(2) or "").strip()
                if paren.lower().startswith("new"):
                    d = {"id": aid}
                    free = []
                    for p_ in split_top(paren, "|")[1:]:
                        if re.match(r"^shared\s+(yes|no)$", p_, re.I):
                            d["shared"] = p_.split()[1].lower()
                        elif p_.lower().startswith("bridge "):
                            d["bridge"] = p_.split(None, 1)[1].strip()
                        elif SPAN.match(p_) or re.match(r"^\S+:\d+$", p_):
                            pth, _, sp_ = p_.rpartition(":")
                            d["source"] = f"{rel(pth)}:{sp_}"
                        elif p_:
                            free.append(p_)
                    if len(free) > 2:
                        probs.append(f"new assumption {aid}: unparsable parts {free[2:]!r}")
                    d["name"] = free[0] if free else ""
                    d["statement"] = free[1] if len(free) > 1 else d["name"]
                    items.append(d)
                else:
                    items.append(aid)
                    if paren:
                        notes.append(f"{aid}: {paren}")
            sgt["assumptions"] = items
        for k in ("conclusion", "rate", "scope", "gates"):
            if k in f:
                sgt[k] = f[k]
        if "implies" in f and not EMPTY.match(f["implies"]):
            imp = []
            for it in split_top(f["implies"], ";"):
                tok, _, why = it.partition(" ")
                imp.append(tok)
                if why.strip():
                    notes.append(f"implies {tok}: {why.strip()}")
            sgt["implies"] = imp
        if "sharpness" in f and not EMPTY.match(f["sharpness"]):
            sh = []
            for it in split_top(f["sharpness"], ";"):
                m = re.match(r"^([AP]:\S+)\s*=\s*([A-Z][A-Z-]*)\s*(?:\((.*)\))?\s*$", it, re.S)
                if not m:
                    probs.append(f"sharpness item {it!r}: expected `A:ID = VERDICT (evidence: path:line)`")
                    continue
                ev = re.sub(r"^evidence:?\s*", "", (m.group(3) or "").strip())
                tok = ev.split()[0] if ev.split() else ""
                pth, _, ln_ = tok.rpartition(":")
                if pth and R.parse_span(ln_) and not pth.startswith("Theory_work/"):
                    ev = f"{rel(pth)}:{ln_}" + ev[len(tok):]
                sh.append({"assumption": m.group(1), "verdict": m.group(2), "evidence": ev})
            sgt["sharpness"] = sh
        if "binding" in f and not EMPTY.match(f["binding"]):
            bd = []
            for it in split_top(f["binding"], ";"):
                m = re.match(r"^([AP]:\S+)\s+forced by\s+(\S+)\s+via\s+(.*?)\s*(?:\[([^\]]*)\])?\s*$", it, re.S)
                if not m:
                    probs.append(f"binding item {it!r}: expected `A:ID forced by <claim id> via <mechanism> "
                                 "[signals]`")
                    continue
                bd.append({"assumption": m.group(1), "binding_claim": m.group(2), "mechanism": m.group(3),
                           "signals": [s.strip() for s in re.split(r"[;,]", m.group(4) or "") if s.strip()]})
            j["binding"] = bd
        if sgt:
            j["strength"] = sgt
        if notes:
            j["notes"] = "; ".join(notes)
        j.setdefault("headline", "")  # headline=yes is Felipe's decision: only when the block says so
        problems += [f"REGISTRY block at {path}:{start} ({cid or '?'}): {p}" for p in probs]
        out.append(j)
    if not blocks:
        problems.append(f"{path}: no REGISTRY block found")
    return out, problems


def read_fragment(path):
    """-> ([(label, obj)], problems). JSONL, or a REPORT.md whose REGISTRY blocks are converted."""
    if path.lower().endswith(".md"):
        objs, problems = convert_report(path)
        return [(f"block {n}", o) for n, o in enumerate(objs, 1)], problems
    out, problems = [], []
    for n, ln in enumerate(open(path, encoding="utf-8"), 1):
        if not ln.strip():
            continue
        try:
            j = json.loads(ln)
        except ValueError as e:
            problems.append(f"line {n}: not JSON ({e})")
            continue
        if not isinstance(j, dict):
            problems.append(f"line {n}: not a JSON object")
            continue
        out.append((f"line {n}", j))
    return out, problems


# ---------------------------------------------------------------- claims
def ingest_claims(path, apply):
    rows = R.load_claims()
    ids = {r["id"] for r in rows}
    aliases = R.load_aliases()
    asm = R.load_assumptions()
    sharp = R.load_sharpness()
    h_bind, binding = R.read_tsv(R.BINDING)
    tickets = R.load_tickets()
    comps = R.load_components()
    tk = {t["ticket"] for t in tickets}
    objs, problems = read_fragment(path)
    # pass 1: ids and new assumptions of the whole fragment (so rows may reference each other)
    frag_ids, new_asm = [], []
    for lab, j in objs:
        if j.get("ticket") and j.get("local_id"):
            frag_ids.append(f"{j['ticket']}:{j['local_id']}")
        sgt = j.get("strength") if isinstance(j.get("strength"), dict) else {}
        for a_ in sgt.get("assumptions", []) or []:
            if isinstance(a_, str) and " = " in a_:  # "A:ID = definition" -> a new assumption row
                i_, _, d_ = a_.partition(" = ")
                a_ = {"id": i_.strip(), "statement": d_.strip(), "name": i_.strip()[2:]}
            if isinstance(a_, dict):
                bad = sorted(set(a_) - ASM_KEYS)
                if bad:
                    problems.append(f"{lab}: new assumption {a_.get('id')!r}: unknown field(s) {bad}")
                aid = str(a_.get("id", "")).split("~")[0]
                if aid in asm:
                    continue  # already registered: only the id is used
                if aid in {x["id"] for x in new_asm}:
                    continue
                kind = a_.get("kind") or ("property" if aid.startswith("P:") else "assumption")
                new_asm.append(dict(id=aid, kind=kind, shared=a_.get("shared", "no") or "no",
                                    name=a_.get("name", ""), statement=a_.get("statement", ""),
                                    source=a_.get("source", ""), implies=R.join_list(as_list(a_.get("implies"))),
                                    bridge=a_.get("bridge", ""), version="1.0.0",
                                    notes=(a_.get("notes", "") + f" added by ingest from {os.path.basename(path)}")
                                    .strip()))
    dup = [c for c, n in collections.Counter(frag_ids).items() if n > 1]
    for c in dup:
        problems.append(f"{c}: appears {frag_ids.count(c)} times in the fragment")
    all_ids = ids | set(frag_ids)
    all_asm = dict(asm, **{x["id"]: x for x in new_asm})
    for x in new_asm:
        if x["kind"] not in ("assumption", "property") or not re.match(r"^[AP]:\S+$", x["id"]):
            problems.append(f"new assumption {x['id']!r}: bad id or kind {x['kind']!r}")
        if x["shared"] not in ("yes", "no"):
            problems.append(f"new assumption {x['id']}: shared must be yes|no")
        if x["bridge"]:
            tkt = next((j["ticket"] for _, j in objs if any(
                (isinstance(a_, dict) and str(a_.get("id", "")).split("~")[0] == x["id"])
                for a_ in ((j.get("strength") or {}).get("assumptions") or []))), "")
            b = R.resolve(x["bridge"], all_ids, aliases, tkt)
            if b is None:
                problems.append(f"new assumption {x['id']}: bridge {x['bridge']!r} resolves to no claim")
            else:
                x["bridge"] = b
        for y in R.split_list(x["implies"]):
            if y not in all_asm:
                problems.append(f"new assumption {x['id']}: implies unknown {y!r}")

    def ref_ok(ref, ticket):
        key = ref[4:] if ref.startswith("EXT:") else ref
        return aliases.get(ref) == "-" or aliases.get(key) == "-" or R.resolve(ref, all_ids, aliases, ticket)

    added, new_sharp, new_bind = [], [], []
    for lab, j in objs:
        bad = sorted(set(j) - TOP_KEYS)
        sgt = j.get("strength") or {}
        if not isinstance(sgt, dict):
            problems.append(f"{lab}: `strength` must be an object")
            sgt = {}
        bad += [f"strength.{k}" for k in sorted(set(sgt) - STRENGTH_KEYS)]
        miss = [k for k in ("ticket", "local_id", "file", "lines") if not j.get(k)]
        cid = f"{j.get('ticket')}:{j.get('local_id')}"
        if bad:
            problems.append(f"{lab} {cid}: unknown field(s) {bad} (supported: {', '.join(sorted(TOP_KEYS))}; "
                            f"strength: {', '.join(sorted(STRENGTH_KEYS))})")
        if miss:
            problems.append(f"{lab} {cid}: missing required field(s) {miss}")
            continue
        if sgt.get("id") and sgt["id"] != cid:
            problems.append(f"{cid}: strength.id {sgt['id']!r} differs")
        if cid in ids:
            problems.append(f"{cid}: already registered (use registry.py rehash / correct-status)")
            continue
        span = j["lines"]
        if isinstance(span, str):
            span = R.parse_span(span) or [0, 0]
        if not (isinstance(span, (list, tuple)) and len(span) == 2):
            problems.append(f"{cid}: lines must be [a, b] or 'a-b'")
            continue
        st, src = j.get("status", ""), j.get("status_source", "")
        headline = j.get("headline", sgt.get("headline", "yes" if sgt else ""))
        consumes = list(dict.fromkeys(as_list(j.get("consumes")) + as_list(sgt.get("consumes"))))
        mcommit = j.get("method_commit") or sgt.get("method_commit", "")
        notes = "; ".join(x for x in (j.get("notes", ""), sgt.get("notes", "")) if x)
        r = new_row(cid, kind=j.get("kind", ""), name=j.get("name", ""), short=j.get("short", ""), file=j["file"],
                    lines=f"{span[0]}-{span[1]}", premises=as_list(j.get("premises")), status=st, status_source=src,
                    evidence=as_list(j.get("evidence")), council=j.get("council", ""),
                    depends_on=as_list(j.get("depends_on")), method=j.get("method", ""), method_commit=mcommit,
                    method_components=as_list(j.get("method_components")),
                    falsification=as_list(j.get("falsification")), notes=notes, consumes=consumes,
                    headline=headline)
        t = r["ticket"]
        if r["kind"] not in R.KINDS:
            problems.append(f"{cid}: kind {r['kind']!r} not in {R.KINDS}")
        if headline not in ("yes", "no", ""):
            problems.append(f"{cid}: headline must be yes|no")
        if not r["sha256"]:
            problems.append(f"{cid}: statement/premise span unreadable ({j['file']}:{span} / {r['premises']})")
        if not status_ok(st, src):
            problems.append(f"{cid}: status {st[:60]!r} does not start verbatim on {src} ({R.status_at(st, src)})")
        for it in R.split_list(r["depends_on"]):
            if not ref_ok(R.parse_dep(it)[0], t):
                problems.append(f"{cid}: depends_on {it!r} resolves to no registry id (nor an alias)")
            elif R.resolve(it, all_ids, aliases, t) == cid:
                problems.append(f"{cid}: depends_on lists the claim itself")
        for it in consumes:
            p, _, b = it.partition("@")
            if all_asm.get(p.strip(), {}).get("kind") != "property":
                problems.append(f"{cid}: consumes {p.strip()!r}, which is not a registered property P:*")
            if b:
                tb = R.resolve(b, all_ids, aliases, t)
                if tb is None:
                    problems.append(f"{cid}: consumes {it!r}: bridge {b!r} resolves to no registry id")
                elif tb == cid:
                    problems.append(f"{cid}: consumes {it!r}: a claim cannot be its own bridge")
        if mcommit and R.git("cat-file", "-e", mcommit + "^{commit}")[0] != 0:
            problems.append(f"{cid}: method_commit {mcommit!r} is not a commit in this repository")
        for c in R.split_list(r["method_components"]):
            if c not in comps:
                problems.append(f"{cid}: unknown method component {c!r} (method_components.tsv)")
        if sgt:
            for k in ("conclusion", "rate", "scope"):
                r[k] = sgt.get(k, "")
            lvl = R.conclusion_level(r)
            if r["conclusion"] and lvl not in R.CONCLUSION_LEVELS + ["negative"]:
                problems.append(f"{cid}: conclusion level {lvl!r} not in {R.CONCLUSION_LEVELS + ['negative']}")
            r["implies"] = R.join_list(as_list(sgt.get("implies")))
            for x_ in R.split_list(r["implies"]):
                if R.resolve(x_, all_ids, aliases, t) is None:
                    problems.append(f"{cid}: implies {x_!r} resolves to no registry id")
            items = []
            for a_ in sgt.get("assumptions", []) or []:
                if isinstance(a_, str) and " = " in a_:
                    a_ = a_.partition(" = ")[0].strip()
                aid = (a_.get("id", "") if isinstance(a_, dict) else str(a_)).strip()
                base, _, pol = aid.partition("~")
                if base not in all_asm:
                    problems.append(f"{cid}: unknown assumption {base!r} (define it as a new assumption)")
                if pol and pol not in ("nec", "iff"):
                    problems.append(f"{cid}: bad polarity in {aid!r}")
                items.append(aid)
            r["assumptions"] = R.join_list(items)
            for s in sgt.get("sharpness", []) or []:
                if not isinstance(s, dict) or set(s) - SHARP_KEYS:
                    problems.append(f"{cid}: sharpness row {s!r}: unknown field(s)")
                    continue
                if s.get("assumption") not in all_asm or s.get("verdict") not in R.NECESSITY:
                    problems.append(f"{cid}: sharpness ({s.get('assumption')!r}, {s.get('verdict')!r}): unknown "
                                    f"assumption or verdict not in {R.NECESSITY}")
                    continue
                new_sharp.append(dict(claim=cid, assumption=s["assumption"], verdict=s["verdict"],
                                      evidence=s.get("evidence", ""), notes=s.get("notes", "") or "ingested"))
            r["gates"] = sgt.get("gates", "")
        for b in (j.get("binding") or []) + (sgt.get("binding") or []):
            if not isinstance(b, dict) or set(b) - BIND_KEYS:
                problems.append(f"{cid}: binding row {b!r}: unknown field(s) (supported: {sorted(BIND_KEYS)})")
                continue
            bc = R.resolve(b.get("binding_claim", ""), all_ids, aliases, t) if b.get("binding_claim") else ""
            sig = as_list(b.get("signals"))
            if b.get("assumption") not in all_asm:
                problems.append(f"{cid}: binding for unknown assumption {b.get('assumption')!r}")
            elif bc is None:
                problems.append(f"{cid}: binding claim {b.get('binding_claim')!r} resolves to no registry id")
            elif [s_ for s_ in sig if s_ not in R.SIGNALS]:
                problems.append(f"{cid}: unknown binding signal(s) {[s_ for s_ in sig if s_ not in R.SIGNALS]}")
            else:
                new_bind.append(dict(headline=cid, assumption=b["assumption"], binding_claim=bc,
                                     mechanism=b.get("mechanism", ""), signals=R.join_list(sig),
                                     notes=b.get("notes", "") or "ingested"))
        added.append(r)
    newt = sorted({r["ticket"] for r in added} - tk)
    print(f"{len(added)} claim(s) to add; {len(problems)} problem(s); new tickets {newt}; "
          f"{len(new_asm)} new assumption(s); {len(new_sharp)} sharpness row(s); {len(new_bind)} binding row(s); "
          f"{sum(1 for r in added if any('@' in c for c in R.split_list(r['consumes'])))} claim(s) with bound "
          f"bridges; {sum(1 for r in added if r['method_commit'])} method pin(s)")
    for p in problems:
        print("  PROBLEM", p)
    if problems:
        sys.exit("refused: nothing written (all-or-nothing; fix every problem first)")
    if not apply:
        print("(dry run: nothing written; add --apply, or --staged to check the result on a copy)")
        return
    sharp_all = sharp + new_sharp
    for r in added:
        r["improvable"] = R.improvable(r, sharp_all)
    writes = [(R.CLAIMS, R.COLUMNS, rows + added)]
    if new_asm:
        h, A = R.read_tsv(R.ASSUMPTIONS)
        writes.append((R.ASSUMPTIONS, h or R.ASSUMPTION_COLUMNS, A + new_asm))
    if new_sharp:
        writes.append((R.SHARPNESS, R.SHARPNESS_COLUMNS, sharp_all))
    if new_bind:
        writes.append((R.BINDING, h_bind or R.BINDING_COLUMNS, binding + new_bind))
    if newt:
        h, T = R.read_tsv(R.TICKETS)
        for t in newt:
            T.append(dict(ticket=t, wave="Wave" + t[1] if t.startswith("W") else "", folder="", result="",
                          result_source="", headline="", sop_row="", branch=f"theory/{t}", kill_budget="",
                          notes="added by ingest; fill folder/result"))
        writes.append((R.TICKETS, h or R.TICKET_COLUMNS, T))
    writes.append((R.EVENTS, R.events_text(("ingest", r["id"], "", f"v1.0.0 {r['status'][:60]}",
                                            f"ingested from {os.path.basename(path)}", "INFRA") for r in added)))
    R.write_many(writes)  # one transaction, events included
    print("written")


# ---------------------------------------------------------------- splits
def ingest_splits(path, apply):
    rows = R.load_claims()
    by = R.index(rows)
    aliases = R.load_aliases()
    parts = collections.OrderedDict()
    repoints, problems = [], []
    header, spec = R.read_tsv(path)
    miss = {"kind_of_row", "parent", "id", "field", "value"} - set(header)
    if miss:
        sys.exit(f"refused: split spec lacks column(s) {sorted(miss)}")
    for n, c in enumerate(spec, 2):
        if c["kind_of_row"] == "part":
            if c["field"] not in PART_FIELDS:
                problems.append(f"row {n} ({c['id']}): unknown part field {c['field']!r} (supported: "
                                f"{', '.join(sorted(PART_FIELDS))})")
                continue
            parts.setdefault((c["parent"], c["id"]), {})[c["field"]] = c.get("value", "")
        elif c["kind_of_row"] == "repoint":
            if c["field"] != "edge":
                problems.append(f"row {n} ({c['id']}): repoint field must be `edge`, not {c['field']!r}")
                continue
            repoints.append(c)
        else:
            problems.append(f"row {n}: unknown kind_of_row {c['kind_of_row']!r} (part | repoint)")
    created = []
    new_ids = {cid for _, cid in parts}
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
        for it in R.split_list(r["depends_on"]):
            if R.resolve(it, set(by) | new_ids, aliases, r["ticket"]) is None:
                problems.append(f"{cid}: depends_on {it!r} resolves to no registry id")
        so, sn = R.status_strength(p["status"]), R.status_strength(st)
        if isinstance(so, int) and isinstance(sn, int) and sn > so:
            problems.append(f"{cid}: part status stronger than the parent's ({sn} > {so}) — check the source")
        created.append((parent, r))
    for rp in repoints:
        d = by.get(rp["id"])
        old, _, new = rp.get("value", "").partition("=>")
        old, new = old.strip(), new.strip()
        if d is None or old not in R.split_list(d["depends_on"]):
            problems.append(f"re-point {rp['id']}: {old!r} is not one of its depends_on items")
        elif R.resolve(new, set(by) | new_ids, aliases, d["ticket"]) is None:
            problems.append(f"re-point {rp['id']}: new item {new!r} resolves to no registry id")
    print(f"{len(created)} part(s) to create from {len({p for p, _ in created})} parent(s); "
          f"{len(repoints)} re-point(s); {len(problems)} problem(s)")
    for x in problems:
        print("  PROBLEM", x)
    if problems:
        sys.exit("refused: nothing written (all-or-nothing; fix the spec first)")
    if not apply:
        print("(dry run: nothing written; add --apply, or --staged to check the result on a copy)")
        return
    rows += [r for _, r in created]
    by = R.index(rows)
    events = []
    for parent, r in created:
        p = by[parent]
        p["depends_on"] = R.join_list(dict.fromkeys(R.split_list(p["depends_on"]) + [f"{r['id']}@stmt"]))
        p["implies"] = R.join_list(dict.fromkeys(R.split_list(p.get("implies", "")) + [r["id"]]))
        events.append(("split", r["id"], parent, f"{r['status'][:60]}", f"split from {parent} "
                       f"({os.path.basename(path)})"))
    for rp in repoints:
        d = by[rp["id"]]
        old, _, new = rp.get("value", "").partition("=>")
        old, new = old.strip(), new.strip()
        d["depends_on"] = R.join_list(new if it == old else it for it in R.split_list(d["depends_on"]))
        events.append(("split-repoint", d["id"], old, new, rp.get("evidence", "")))
    R.write_many([(R.CLAIMS, R.COLUMNS, rows), (R.EVENTS, R.events_text(e + ("INFRA",) for e in events))])
    print("written")


# ---------------------------------------------------------------- staged
def staged(what, path):
    """Apply to a disposable copy of the registry, run the full check.py on it, print the result."""
    stage = R.make_stage()
    try:
        rc, out = R.run_staged(stage, "ingest.py", what, os.path.abspath(path), "--apply")
        print(out.rstrip())
        if rc != 0:
            print("\nSTAGED: ingest refused; nothing written anywhere")
            return 1
        rc_live, live, _ = R.check_findings()
        rc_st, st, summary = R.check_findings(stage)
        new = sorted(f for f in st - live if f[0] == "ERROR")
        print(f"\nSTAGED check.py on the proposed registry: {summary.replace('check.py: ', '')}")
        print(f"  ERROR introduced by this {what} fragment: {len(new)}; ERROR already in the live registry: "
              f"{sum(1 for f in st if f[0] == 'ERROR') - len(new)}")
        for f in new:
            print(f"  NEW {f[0]:5} {f[1]:17} {f[2]:30} {f[3]}")
        print("(staged copy discarded; the live registry was not touched. Apply with --apply, then run check.py.)")
        return rc_st
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=["claims", "splits", "convert"])
    ap.add_argument("path")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true")
    g.add_argument("--staged", action="store_true")
    a = ap.parse_args()
    if a.what == "convert":
        objs, problems = convert_report(a.path)
        for o in objs:
            print(json.dumps(o, ensure_ascii=False))
        for p in problems:
            print("PROBLEM", p, file=sys.stderr)
        sys.exit(1 if problems else 0)
    if a.staged:
        sys.exit(staged(a.what, a.path))
    (ingest_claims if a.what == "claims" else ingest_splits)(a.path, a.apply)


if __name__ == "__main__":
    main()
