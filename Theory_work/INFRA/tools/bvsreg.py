"""Shared library for the SMC-BVS claims registry (Theory_work/INFRA/registry).

Plain-text data, standard library only. Every tool in INFRA/tools imports this module.
Data model and rules: Theory_work/INFRA/LIFECYCLE.md. Files (UTF-8, tab-separated, header row):

  claims.tsv           one row per claim (theorem/lemma/.../external anchor); COLUMNS below
  tickets.tsv          one row per ticket (folder, verbatim result, headline claims, SoP row, kill budget)
  aliases.tsv          alias -> claim id (resolves "EXT:T03♯" style references)
  assumptions.tsv      first-class assumptions (A:*) and interface properties (P:*), with their own implication
                       lattice (`implies`), bridge lemma (A ⇒ P) and version
  sharpness.tsv        necessity evidence per (headline claim, assumption); several rows per pair allowed
  binding.tsv          binding map: for each headline assumption, the claim whose proof forces it (+ signals)
  repoints.tsv         proposed / confirmed re-pointings of dependency edges after a supersession
  method_components.tsv component -> code paths (for method pinning)
  config.tsv           key/value: freeze, max_assumption_sets, ...
  events.log           append-only audit trail of every state/status/version change

List cells use "; " as separator (";" inside an item is replaced by ",").
Dependency items are USE-LEVEL edges: "<id>" or "<id>@<use>" with use = "stmt" (default: the statement),
"stmt:<clause>" (one clause of it) or "proof:<fact>" (an event / rate / constant / lemma internal to its proof).
Assumption items: "<A or P id>" (hypothesis polarity) or "<id>~nec" (used in a necessity result / counterexample)
or "<id>~iff" (both directions). Weakening an assumption is only safe where it has hypothesis polarity.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import os
import re
import subprocess
import sys
from collections import defaultdict, deque

for _s in ("stdout", "stderr"):  # Windows consoles default to cp1252; statuses contain ♯, ⊂, 𝔉 ...
    try:
        getattr(sys, _s).reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TOOLS = os.path.dirname(os.path.abspath(__file__))
INFRA = os.path.dirname(TOOLS)
ROOT = os.path.abspath(os.path.join(INFRA, "..", ".."))  # repository root
# STAGED mode (ingest.py --staged, propagate.py rollback-ticket): BVS_STAGE_INFRA names a disposable copy of the
# INFRA state (registry/, DECISIONS.md, FAILED_ROUTES.md, issues/). Every registry read and write goes there;
# statement files are still read from ROOT (the repository). Writes stay confined to that copy (safe_dest).
STAGE_MARK = ".bvs-stage"  # written by make_stage(); a stage must carry it


def _valid_stage(d: str) -> bool:
    """Only a tool-created disposable stage may replace INFRA: an existing directory named bvs-stage-* directly in
    the system temp directory, carrying the STAGE_MARK file, and outside the repository."""
    import tempfile
    rd, tmp, root = (os.path.normcase(os.path.realpath(x)) for x in (d, tempfile.gettempdir(), ROOT))
    return (os.path.isdir(rd) and os.path.basename(rd).startswith("bvs-stage-") and os.path.dirname(rd) == tmp
            and os.path.isfile(os.path.join(rd, STAGE_MARK))
            and os.path.commonpath([rd, root]) != root)


if os.environ.get("BVS_STAGE_INFRA"):
    if not _valid_stage(os.environ["BVS_STAGE_INFRA"]):
        raise SystemExit(f"refusing BVS_STAGE_INFRA={os.environ['BVS_STAGE_INFRA']!r}: not a disposable stage made "
                         "by make_stage() (temp dir bvs-stage-* with its marker, outside the repository)")
    INFRA = os.path.realpath(os.environ["BVS_STAGE_INFRA"])
REG = os.path.join(INFRA, "registry")
P = lambda f: os.path.join(REG, f)  # noqa: E731
# Sol-1: a multi-file transaction whose own restore failed leaves this lock (backup locations + recovery steps).
# R03-N4: every multi-file transaction first writes (and fsyncs) the journal TXN_JOURNAL with its backup locations and
# removes it only after every replacement succeeded, so a process killed between replacements leaves it behind.
# Every tool refuses to run while either exists (import-time guard below, and safe_dest), until `bvsreg.py recover`.
TXN_LOCK = P(".TXN_FAILED")
TXN_JOURNAL = P(".TXN_INPROGRESS")


def txn_guard() -> None:
    if os.path.exists(TXN_JOURNAL):
        raise SystemExit(f"REGISTRY LOCKED: {TXN_JOURNAL} exists (a multi-file transaction did not finish: the process "
                         "was killed or its restore failed, so the registry may be a mix of old and new files)"
                         + (f" and {TXN_LOCK} exists" if os.path.exists(TXN_LOCK) else "") + ". Run `python "
                         "Theory_work/INFRA/tools/bvsreg.py recover` (rolls every journalled file back to its backup; "
                         "safe to re-run), then check.py, then re-run the interrupted command.")
    if os.path.exists(TXN_LOCK):
        raise SystemExit(f"REGISTRY LOCKED: {TXN_LOCK} exists (a multi-file write failed AND its restore failed, so "
                         "the registry may be inconsistent). Read it, then run `python Theory_work/INFRA/tools/"
                         "bvsreg.py recover` (restores every listed file from its backup), then check.py.")


if __name__ != "__main__":  # `python bvsreg.py recover` is the one entry point that runs while locked
    txn_guard()

# F6 (rollback-ticket): in a STAGE only, `.post_revert.tsv` in the stage root lists repository files as they will be
# after the documented `git revert` of a ticket: "<path>\t-" (removed) or "<path>\t<ref>" (content as at <ref>).
# read_lines honours it, so check.py on the stage validates the proposed post-revert tree.
POST_REVERT_FILE = ".post_revert.tsv"
POST_REVERT = {}


def _pkey(relpath: str) -> str:
    return os.path.normpath(relpath or "").replace("\\", "/")


def _pcase(relpath: str) -> str:
    """Lookup key into POST_REVERT: normalised, case-folded on case-insensitive (Windows) file systems."""
    k = _pkey(relpath)
    return k.lower() if os.name == "nt" else k


if INFRA != os.path.dirname(TOOLS) and os.path.isfile(os.path.join(INFRA, POST_REVERT_FILE)):
    with open(os.path.join(INFRA, POST_REVERT_FILE), encoding="utf-8") as _fh:
        for _ln in _fh.read().splitlines():
            if "\t" in _ln:
                _p, _r = _ln.split("\t", 1)
                POST_REVERT[_pcase(_p)] = _r.strip() or "-"
CLAIMS, TICKETS, ALIASES, EVENTS = P("claims.tsv"), P("tickets.tsv"), P("aliases.tsv"), P("events.log")
ASSUMPTIONS, SHARPNESS, BINDING = P("assumptions.tsv"), P("sharpness.tsv"), P("binding.tsv")
REPOINTS, COMPONENTS, CONFIG = P("repoints.tsv"), P("method_components.tsv"), P("config.tsv")

COLUMNS = [
    "id",            # "<TICKET>:<local_id>" or "SOP:<row id>" for State-of-Project anchors
    "ticket",        # ticket folder name, "SOP" for external anchors
    "local_id",
    "kind",          # see KINDS
    "name",          # label verbatim
    "short",         # plain-language summary incl. scope
    "file",          # repo-relative path of the authoritative statement text
    "lines",         # "a-b", 1-based inclusive
    "premises",      # extra spans "path:a-b" (setting, hypotheses, event definitions) hashed WITH the statement
    "sha256",        # of the normalised statement text + premise spans (see claim_hash)
    "version",       # semver: major = claim changes, minor = proof/status changes, patch = editorial
    "status",        # VERBATIM status words from the ticket (tools change it only on an explicit downgrade)
    "state",         # lifecycle, see STATES
    "state_reason",  # why the state is what it is (latest change first)
    "status_source", # path:line where the status is written
    "evidence",      # review files + verdicts (list)
    "council",       # council scores verbatim
    "commit",        # last commit touching the statement file when the row was (re)hashed
    "depends_on",    # USE-LEVEL edges (list of "id[@use]")
    "acks",          # dependency ids whose non-ACTIVE state was reviewed and accepted (list)
    "method",        # method version the claim is about, verbatim
    "method_commit", # pinned commit of the method/code the claim is about ("" = not about code)
    "method_components",  # components (method_components.tsv) whose change is a rollback trigger (list)
    "falsification", # saved falsification scripts (list of "path" or "path | cmd")
    # ---- strength layer (headline theorems + shared assumptions only) ----
    "headline",      # "yes" for paper-headline results: strength gate, sharpness and binding map apply
    "assumptions",   # hypotheses as A:/P: ids with optional polarity suffix (~nec, ~iff)
    "consumes",      # interface properties P:* the proof consumes (never a shared A directly)
    "conclusion",    # "<level>: <conclusion>"; level in CONCLUSION_LEVELS
    "rate",          # rate verbatim, "" if qualitative
    "scope",         # p range; design class; law (fixed design / iid rows / joint)
    "implies",       # claim ids X such that THIS statement implies X's statement (list)
    "superseded_by", # set iff state SUPERSEDED-VALID
    "coexists_with", # incomparable alternatives kept side by side (COEXIST; list)
    "improvable",    # derived (registry.py refresh): "yes(A:..)" / "no" / "" (not a headline)
    "gates",         # e.g. "correct:PASS(R07/R08); lit:PENDING; necessity:PARTIAL; better:PENDING"
    "tex",           # LaTeX statement block for the paper, "path:a-b"
    "tex_sha256",    # hash of the tex span when its transcription was last reviewed against the statement
    "notes",
    "status_sha256", # INFRA R05: content digest (line-wise) of the status source when it is a CHECKPOINT_<k>.md,
                     # recorded at ingest / status change (empty otherwise); check.py C12 flags a later edit
]
STATES = ["ACTIVE", "CANDIDATE", "SUSPECT", "REBASE-NEEDED", "NARROWED", "RETRACTED", "DEPRECATED",
          "SUPERSEDED-VALID"]
VALID = {"ACTIVE", "SUPERSEDED-VALID"}           # true statements one may depend on
DEAD = {"RETRACTED", "DEPRECATED"}
KINDS = ["theorem", "lemma", "proposition", "corollary", "counterexample", "obstruction", "frontier", "audit",
         "implementation", "external"]  # frontier = an open boundary / numerical observation, NOT a proved obstruction
TICKET_COLUMNS = ["ticket", "wave", "folder", "result", "result_source", "headline", "sop_row", "branch",
                  "kill_budget", "notes"]
CONCLUSION_LEVELS = ["identity", "target", "posterior", "reported-model", "delivery"]  # + "negative" (unordered)
NECESSITY = ["NECESSARY", "NECESSARY-FOR-ROUTE", "FAILED-REMOVAL", "ARTEFACT", "WEAKENABLE", "NONE"]
ASSUMPTION_COLUMNS = ["id", "kind", "shared", "name", "statement", "source", "implies", "bridge", "version", "notes"]
SHARPNESS_COLUMNS = ["claim", "assumption", "verdict", "evidence", "notes"]
BINDING_COLUMNS = ["headline", "assumption", "binding_claim", "mechanism", "signals", "notes"]
REPOINT_COLUMNS = ["dependent", "from", "to", "use", "from_version", "to_version", "state", "before", "after",
                   "preexisting", "checked_by", "date", "notes"]
SIGNALS = ["boundary-numerics", "artefact-threshold", "single-use-union-bound", "family-named",
           "literature-dominance", "prover-divergence", "unharvested-conclusion"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


# ---------------------------------------------------------------- TSV I/O
def _clean(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return join_list(v)
    return str(v).replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def split_list(s: str) -> list[str]:
    return [x.strip() for x in (s or "").split(";") if x.strip()]


def join_list(items) -> str:
    return "; ".join(_clean(str(x)).replace(";", ",") for x in items if str(x).strip())


def read_tsv(path: str) -> tuple[list[str], list[dict]]:
    if not os.path.exists(path):
        return [], []
    with open(path, encoding="utf-8", newline="") as fh:
        lines = fh.read().splitlines()
    if not lines:
        return [], []
    header = lines[0].split("\t")
    rows = []
    for ln in lines[1:]:
        if not ln.strip() or ln.startswith("#"):
            continue
        cells = ln.split("\t")
        cells += [""] * (len(header) - len(cells))
        rows.append(dict(zip(header, cells)))
    return header, rows


def safe_dest(path: str, guard: bool = True) -> str:
    """Refuse a write destination unless it resolves strictly inside Theory_work/INFRA and no component from INFRA
    down to the file is a symlink or junction (so a planted link cannot redirect a write outside). No write at all
    while the transaction lock exists (Sol-1)."""
    if guard:
        txn_guard()
    infra = os.path.realpath(INFRA)
    if os.path.realpath(INFRA) != os.path.abspath(INFRA) and os.path.islink(INFRA):
        raise SystemExit(f"refusing to write: {INFRA} is a link")
    p = os.path.abspath(path)
    rp = os.path.realpath(p)
    if os.path.commonpath([os.path.normcase(rp), os.path.normcase(infra)]) != os.path.normcase(infra) or \
            os.path.normcase(rp) == os.path.normcase(infra):
        raise SystemExit(f"refusing to write outside Theory_work/INFRA: {path}")
    cur = p
    while os.path.normcase(cur) != os.path.normcase(os.path.abspath(INFRA)):
        if os.path.islink(cur) or (hasattr(os.path, "isjunction") and os.path.isjunction(cur)):
            raise SystemExit(f"refusing to write through a link: {cur}")
        nxt = os.path.dirname(cur)
        if nxt == cur:
            raise SystemExit(f"refusing to write outside Theory_work/INFRA: {path}")
        cur = nxt
    return p


def write_tsv(path: str, header: list[str], rows: list[dict]) -> None:
    path = safe_dest(path)
    tmp = safe_dest(path + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(_clean(r.get(c, "")) for c in header) + "\n")
    os.replace(tmp, path)


def _fsync_file(path: str) -> None:
    with open(path, "r+b") as fh:  # write access: FlushFileBuffers on Windows needs it
        os.fsync(fh.fileno())


def _fsync_dir(d: str) -> None:
    """Make a rename / removal in directory d durable (POSIX). Windows cannot open a directory for fsync; NTFS
    journals its metadata."""
    if os.name == "nt":
        return
    try:
        fd = os.open(d, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass


def _restore(dest: str, backup: str) -> None:
    """Put `backup` back over `dest` (copy to dest.rst, fsync, atomic replace), or remove a dest that did not exist
    before (backup ''). The backup itself is kept, so an interrupted restore can simply be repeated."""
    import shutil
    if backup:
        shutil.copyfile(backup, dest + ".rst")
        _fsync_file(dest + ".rst")
        os.replace(dest + ".rst", dest)
    elif os.path.exists(dest):
        os.remove(dest)


_RECOVERY = ["python Theory_work/INFRA/tools/bvsreg.py recover   # puts every 'backup' back over its 'dest' (removes a "
             "'remove-new-file' dest), then deletes the journal / lock; safe to re-run if it is interrupted",
             "by hand, if recover fails: copy each backup over its dest, delete each remove-new-file dest, delete "
             "registry/.TXN_INPROGRESS and registry/.TXN_FAILED",
             "python Theory_work/INFRA/tools/check.py   # then re-run the interrupted command"]


def _write_journal(items) -> None:
    """R03-N4: the durable in-progress journal, written (tmp + fsync + atomic rename) BEFORE the first replacement."""
    import json
    info = {"utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "argv": sys.argv,
            "state": "in-progress: no replacement is committed until this file is removed", "restore": items,
            "recovery": _RECOVERY}
    tmp = TXN_JOURNAL + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(info, fh, indent=1)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, TXN_JOURNAL)
    _fsync_dir(os.path.dirname(TXN_JOURNAL))


def _cleanup(items) -> None:
    for it in items:
        for f in (it.get("tmp", ""), it.get("backup", ""), it.get("dest", "") + ".rst"):
            if f and f != it.get("dest") and os.path.exists(f):
                try:
                    os.remove(f)
                except OSError:
                    pass


def replace_all(pairs) -> None:
    """Crash-safe transaction over prepared files: [(tmp, dest)] (R03-N4, Sol-1).
    1. every tmp is fsynced; every existing dest is copied to dest.bak (fsynced);
    2. the journal registry/.TXN_INPROGRESS (each dest, its backup, the action that undoes it) is written and fsynced;
    3. every tmp replaces its dest (atomic rename);
    4. only then the journal is removed (= commit), then the backups.
    On an exception every completed replacement is restored from its backup (or removed if the dest was new) and the
    journal removed; if a restore itself fails, the journal stays and the lock TXN_LOCK is added. A process killed at
    any point after step 2 leaves the journal. While the journal or the lock exists every tool refuses to run;
    `bvsreg.py recover` rolls every journalled file back (restartable: backups are copied, never moved)."""
    import shutil
    txn_guard()
    items = []
    try:
        for tmp, dest in pairs:
            _fsync_file(tmp)
            if os.path.exists(dest):
                bak = safe_dest(dest + ".bak", guard=False)
                shutil.copyfile(dest, bak)
                _fsync_file(bak)
                items.append({"dest": dest, "backup": bak, "action": "restore-from-backup", "tmp": tmp})
            else:
                items.append({"dest": dest, "backup": "", "action": "remove-new-file", "tmp": tmp})
        for d in sorted({os.path.dirname(it["dest"]) for it in items}):
            _fsync_dir(d)  # the backups' directory entries are durable before the journal names them
        _write_journal(items)
    except BaseException:
        if os.path.exists(TXN_JOURNAL):  # nothing was replaced yet
            os.remove(TXN_JOURNAL)
        _cleanup(items + [{"tmp": t} for t, _ in pairs])
        raise
    done = []
    try:
        for it in items:
            os.replace(it["tmp"], it["dest"])
            done.append(it)
        for d in sorted({os.path.dirname(it["dest"]) for it in items}):
            _fsync_dir(d)
    except BaseException as exc:
        todo = []
        for it in reversed(done):
            try:
                _restore(it["dest"], it["backup"])
            except OSError:
                todo.append(it)
                print(f"ROLLBACK FAILED for {it['dest']} (backup {it['backup'] or '-'} kept)", file=sys.stderr)
        if todo:
            write_txn_lock(todo, exc)  # the journal stays too: `recover` rolls the whole transaction back
        else:
            os.remove(TXN_JOURNAL)
            _cleanup(items)
        raise
    os.remove(TXN_JOURNAL)  # commit point
    _fsync_dir(os.path.dirname(TXN_JOURNAL))
    _cleanup(items)


def write_txn_lock(todo, exc) -> None:
    """Record a failed restore (Sol-1): what to put back, from where, and how. Written directly (no guard)."""
    import json
    info = {"utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "argv": sys.argv,
            "error": repr(exc), "restore": todo, "recovery": _RECOVERY}
    try:
        with open(TXN_LOCK, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(info, fh, indent=1)
            fh.flush()
            os.fsync(fh.fileno())
    except OSError as e:  # pragma: no cover - last resort: tell the operator
        print(f"COULD NOT WRITE THE LOCK {TXN_LOCK} ({e}); restore by hand: {todo}", file=sys.stderr)
    print(f"REGISTRY LOCKED: {TXN_LOCK} (run bvsreg.py recover)", file=sys.stderr)


def recover(dry_run: bool = False) -> int:
    """`bvsreg.py recover`: roll an unfinished transaction back from its journal (registry/.TXN_INPROGRESS: killed
    process or failed restore), or, without a journal, undo a failed restore listed in the lock TXN_LOCK; then remove
    the journal and the lock. Restartable: backups are copied over their destinations (never moved) and the journal
    is removed only after every file is back, so a recover killed half-way is simply run again."""
    import json
    src = TXN_JOURNAL if os.path.exists(TXN_JOURNAL) else TXN_LOCK if os.path.exists(TXN_LOCK) else ""
    if not src:
        print(f"no journal or lock ({TXN_JOURNAL}, {TXN_LOCK}): nothing to recover")
        return 0
    try:
        info = json.load(open(src, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"PROBLEM cannot read {src} ({e}); restore by hand (see LIFECYCLE §5.5) and delete it")
        return 1
    items = info.get("restore", [])
    problems = []
    for it in items:
        dest, bak = it.get("dest", ""), it.get("backup", "")
        print(f"{'would ' if dry_run else ''}{it.get('action')}: {dest}" + (f" <- {bak}" if bak else ""))
        if dry_run:
            continue
        try:
            dest = safe_dest(dest, guard=False)
            if it.get("action") == "restore-from-backup":
                bak = safe_dest(bak, guard=False)
                if not os.path.isfile(bak):
                    raise OSError(f"backup {bak} is missing")
                _restore(dest, bak)
            elif it.get("action") == "remove-new-file":
                _restore(dest, "")
            else:
                raise OSError(f"unknown action {it.get('action')!r}")
        except (OSError, SystemExit) as e:
            problems.append(f"{dest}: {e}")
    if problems or dry_run:
        print("\n".join(f"PROBLEM {p}" for p in problems) or "(dry run: nothing changed)")
        return 1 if problems else 0
    for f in (TXN_JOURNAL, TXN_LOCK):  # every file is back: now (and only now) end the transaction
        if os.path.exists(f):
            os.remove(f)
    _fsync_dir(os.path.dirname(TXN_JOURNAL))
    _cleanup(items)
    print(f"recovered {len(items)} file(s) from {os.path.basename(src)}; journal / lock removed. Next: python "
          "Theory_work/INFRA/tools/check.py, then re-run the interrupted command")
    return 0


def write_many(items) -> None:
    """All-or-nothing, crash-safe write of several files: [(path, header, rows)] for TSVs or [(path, text)] for raw
    text (e.g. the events log with its new lines). All are written to .tmp siblings first, then replaced as one
    journalled transaction (replace_all): an exception leaves every file as it was; a killed process leaves the
    journal, which blocks every tool until `bvsreg.py recover` rolls the files back."""
    staged = []
    try:
        for it in items:
            path = safe_dest(it[0])
            tmp = safe_dest(path + ".tmp")
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                if len(it) == 2:
                    fh.write(it[1])
                else:
                    fh.write("\t".join(it[1]) + "\n")
                    for r in it[2]:
                        fh.write("\t".join(_clean(r.get(c, "")) for c in it[1]) + "\n")
            staged.append((tmp, path))
    except BaseException:
        for tmp, _ in staged:
            if os.path.exists(tmp):
                os.remove(tmp)
        raise
    replace_all(staged)


def events_text(new_events) -> str:
    """The events log with these (action, id, before, after, reason, actor) entries appended (for write_many)."""
    old = open(EVENTS, encoding="utf-8", newline="").read() if os.path.exists(EVENTS) else \
        "utc\tactor\taction\tid\tbefore\tafter\treason\n"
    if old and not old.endswith("\n"):
        old += "\n"
    return old + "".join(event_line(*e) for e in new_events)


def event_line(action, cid, before, after, reason, actor="HQ") -> str:
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return "\t".join(_clean(x) for x in (ts, actor, action, cid, before, after, reason)) + "\n"


def load_claims() -> list[dict]:
    return read_tsv(CLAIMS)[1]


def save_claims(rows: list[dict]) -> None:
    write_tsv(CLAIMS, COLUMNS, rows)


def load_tickets() -> list[dict]:
    return read_tsv(TICKETS)[1]


def load_aliases() -> dict[str, str]:
    return {r["alias"]: r["id"] for r in read_tsv(ALIASES)[1] if r.get("alias")}


def load_assumptions() -> dict[str, dict]:
    return {r["id"]: r for r in read_tsv(ASSUMPTIONS)[1]}


def load_sharpness() -> list[dict]:
    return read_tsv(SHARPNESS)[1]


def load_binding() -> list[dict]:
    return read_tsv(BINDING)[1]


def load_repoints() -> list[dict]:
    return read_tsv(REPOINTS)[1]


def save_repoints(rows) -> None:
    write_tsv(REPOINTS, REPOINT_COLUMNS, rows)


def load_components() -> dict[str, list[str]]:
    return {r["component"]: split_list(r.get("paths", "")) for r in read_tsv(COMPONENTS)[1]}


def config() -> dict[str, str]:
    return {r["key"]: r.get("value", "") for r in read_tsv(CONFIG)[1]}


def log_event(action: str, cid: str, before: str, after: str, reason: str, actor: str = "HQ") -> None:
    new = not os.path.exists(EVENTS)
    with open(safe_dest(EVENTS), "a", encoding="utf-8", newline="\n") as fh:
        if new:
            fh.write("utc\tactor\taction\tid\tbefore\tafter\treason\n")
        ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        fh.write("\t".join(_clean(x) for x in (ts, actor, action, cid, before, after, reason)) + "\n")


# ---------------------------------------------------------------- statement hashing
_READ_REF = None  # set by at_ref(): read files from this git commit-ish instead of the working tree (tombstones)


def read_lines(relpath: str) -> list[str] | None:
    if _READ_REF:
        return read_lines_at(relpath, _READ_REF)
    if POST_REVERT and _pcase(relpath) in POST_REVERT:  # staged post-revert tree (rollback-ticket)
        ref = POST_REVERT[_pcase(relpath)]
        return None if ref == "-" else read_lines_at(relpath, ref)
    fp = os.path.join(ROOT, relpath)
    if not relpath or not os.path.isfile(fp):
        return None
    with open(fp, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def read_lines_at(relpath: str, ref: str) -> list[str] | None:
    """The lines of `relpath` as committed at `ref` (a tag / commit), or None."""
    if not relpath or not ref:
        return None
    try:
        p = subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{relpath}"], capture_output=True, timeout=60)
    except Exception:  # pragma: no cover
        return None
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8", errors="replace").splitlines()


class at_ref:
    """`with at_ref(ref):` every read_lines (hashes, status lookups, spans) reads the files as committed at ref."""

    def __init__(self, ref):
        self.ref = ref

    def __enter__(self):
        global _READ_REF
        self.old, _READ_REF = _READ_REF, self.ref
        return self

    def __exit__(self, *exc):
        global _READ_REF
        _READ_REF = self.old
        return False


ARCHIVE_PREFIX = "archive:"


def archive_ref(row: dict) -> str:
    """TOMBSTONES (LIFECYCLE §3): a RETRACTED / DEPRECATED claim whose ticket files were reverted keeps its registry
    row; `archive:<tag or commit>` in its evidence says where its statement and evidence stay readable."""
    if row.get("state") not in DEAD:
        return ""
    for it in split_list(row.get("evidence", "")):
        if it.startswith(ARCHIVE_PREFIX):
            return it[len(ARCHIVE_PREFIX):].strip()
    return ""


def parse_span(s: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", s or "")
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    return (a, b) if 1 <= a <= b else None


_NEGATION = re.compile(r"\b(not|no|never|un|pending|without)\b(\s+\w+){0,2}\s*$")


def _norm_status_text(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*`_|;,]", " ", t or "")).strip().lower()


def status_at(status: str, source: str) -> str:
    """Locate a verbatim status at `path:line`: 'ok' | 'negated' | 'elsewhere' (later lines / other place in the
    file) | 'missing' | 'unreadable'. The match must START on the stated line (it may continue on the next 3), and
    must not be preceded by a negation ("not", "not yet", "no", "pending", ...)."""
    path, _, ln = (source or "").rpartition(":")
    lines = read_lines(path) if path else None
    sp = parse_span(ln.split(",")[0]) if lines else None
    if lines is None or sp is None or sp[0] > len(lines):
        return "unreadable"
    st = _norm_status_text(status)
    if not st:
        return "missing"
    first = _norm_status_text(lines[sp[0] - 1])
    window = _norm_status_text(" ".join(lines[sp[0] - 1: sp[1] + 3]))
    tok = re.compile(r"(?<![\w-])" + re.escape(st) + r"(?![\w-])")  # whole token: not NOT-X, not X-NESS
    m = tok.search(window)
    pos = m.start() if m and m.start() <= len(first) else -1  # must start on the stated line
    if pos < 0:
        return "elsewhere" if tok.search(_norm_status_text(" ".join(lines))) else "missing"
    return "negated" if _NEGATION.search(window[:pos]) else "ok"


def span_key(spec: str):
    """Canonical (path, a, b) for a 'path:a-b' span (path normalised, numbers as ints), or None."""
    path, _, sp = (spec or "").strip().split()[0].rpartition(":") if (spec or "").strip() else ("", "", "")
    s = parse_span(sp)
    if not path or s is None or span_lines(f"{path}:{sp}") is None:
        return None
    return (os.path.normcase(os.path.normpath(path)).replace("\\", "/"), s[0], s[1])


def text_hash(lines: list[str]) -> str:
    """sha256 of the span with trailing whitespace stripped per line and LF joins (CRLF/editor-proof)."""
    return hashlib.sha256("\n".join(l.rstrip() for l in lines).encode("utf-8")).hexdigest()


def statement_hash(relpath: str, span: tuple[int, int]) -> str | None:
    lines = read_lines(relpath)
    if lines is None or span[1] > len(lines):
        return None
    return text_hash(lines[span[0] - 1: span[1]])


def span_lines(spec: str):
    """'path:a-b' -> list of lines, or None."""
    path, _, sp = (spec or "").rpartition(":")
    span = parse_span(sp)
    lines = read_lines(path) if path else None
    if lines is None or span is None or span[1] > len(lines):
        return None
    return lines[span[0] - 1: span[1]]


def split_premise(spec: str) -> tuple[str, str]:
    """A premise item is `path:a-b`, or `path:a-b@archive:<ref>` when its file was reverted with a rolled-back ticket
    (F6): the span is then read as committed at <ref>. -> (path:a-b, ref or '')."""
    s, sep, ref = (spec or "").partition("@" + ARCHIVE_PREFIX)
    return (s.strip(), ref.strip()) if sep else ((spec or "").strip(), "")


def premise_lines(spec: str):
    s, ref = split_premise(spec)
    if ref:
        with at_ref(ref):
            return span_lines(s)
    return span_lines(s)


def claim_hash(row: dict, span=None) -> str | None:
    """sha256 over the statement span plus every premise span (in order). None if any span is unreadable. An
    archive-backed premise (`@archive:<ref>`) hashes exactly as the plain span did."""
    span = span or parse_span(row.get("lines", ""))
    lines = read_lines(row.get("file", ""))
    if lines is None or span is None or span[1] > len(lines):
        return None
    parts = [lines[span[0] - 1: span[1]]]
    for spec in split_list(row.get("premises", "")):
        pl = premise_lines(spec)
        if pl is None:
            return None
        parts.append(["--premise " + split_premise(spec)[0].rpartition(":")[0] + "--"] + pl)
    return text_hash([l for part in parts for l in part])


def repo_file_exists(relpath: str) -> bool:
    """A repository file exists (in the staged post-revert tree, when one is set)."""
    k, kc = _pkey(relpath), _pcase(relpath)
    if POST_REVERT and kc in POST_REVERT:
        return POST_REVERT[kc] != "-" and git("cat-file", "-t", f"{POST_REVERT[kc]}:{k}") == (0, "blob")
    return bool(relpath) and os.path.isfile(os.path.join(ROOT, relpath))


def relocate(relpath: str, sha: str, length: int) -> tuple[int, int] | None:
    """The unique window of `length` lines whose hash is `sha` (statement moved, text unchanged)."""
    lines = read_lines(relpath)
    if lines is None:
        return None
    hits = [i for i in range(0, len(lines) - length + 1) if text_hash(lines[i:i + length]) == sha]
    return (hits[0] + 1, hits[0] + length) if len(hits) == 1 else None


def git(*args: str) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, timeout=60,
                           encoding="utf-8", errors="replace")
        return p.returncode, p.stdout.strip()
    except Exception as e:  # pragma: no cover
        return 1, str(e)


def git_last_commit(relpath: str) -> str:
    return git("log", "-1", "--format=%h", "--", relpath)[1]


# ---------------------------------------------------------------- status vocabulary
# Leading-token classification of verbatim statuses. Strength: 3 checked, 2 proved but unchecked/author-only,
# 1 partial/sketch/candidate, 0 open/stuck/gap/error, None unknown/empty, "NEG" negative results.
_NEG = re.compile(r"^(COUNTEREXAMPLE|REFUTED|OBSTRUCTION|FALSE|NO-GO|NEGATIVE)")
_RULES = [
    (re.compile(r"^(PROVED|VERIFIED|HOLDS)[^;,.]*?(UNCHECKED|BY THIS SEAT|AUTHOR-ONLY)"), 2),
    (re.compile(r"^PROVED[- ]?(CHECKED|LOCKED)"), 3),
    (re.compile(r"^(VERIFIED|HOLDS|EXTENDS|CONFIRMED|ACCEPT|DONE|OK|CORRECT|TRUE-AS-WRITTEN|FAITHFUL)"), 3),
    (re.compile(r"^(PARTIAL|PROOF SKETCH|SKETCH|CANDIDATE|PLAUSIBLE|CONDITIONAL|IN PROGRESS|DRAFT|NOT PROVED)"), 1),
    (re.compile(r"^PROVED[- ]?CONDITIONAL"), 1),
    (re.compile(r"^PROVED"), 2),
    (re.compile(r"^(OPEN(?! ITEMS)|STUCK|CONJECTURE|GAP|ERROR|FAILED|UNPROVED|NOT PROVED|RETRACTED)"), 0),
]


def _norm_status(status: str) -> str:
    s = (status or "").strip()
    if s.upper().startswith("UNSPLIT-STATUS:"):  # a split part inherits its parent's status, never more
        s = s.split(":", 1)[1]
    return s.strip().lstrip("*_`\"'([ ").upper()


def status_token(status: str) -> str:
    m = re.match(r"[A-Z][A-Z*\-]*(?: (?:SKETCH|PROGRESS|PROVED|CHECKED))?", _norm_status(status))
    return m.group(0) if m else ""


def status_strength(status: str):
    s = _norm_status(status)
    if not s:
        return None
    if _NEG.match(s):
        return "NEG"
    for rx, v in _RULES:
        if rx.match(s):
            return v
    return None


# ---------------------------------------------------------------- use-level dependency graph
def parse_dep(item: str) -> tuple[str, str]:
    ref, _, use = item.partition("@")
    return ref.strip(), (use.strip() or "stmt")


def index(rows: list[dict]) -> dict[str, dict]:
    return {r["id"]: r for r in rows}


def resolve(ref: str, ids: set[str], aliases: dict[str, str], ticket: str = "") -> str | None:
    """Resolve a reference to a registry id (exact id, ticket-local id, or alias)."""
    ref = parse_dep(ref)[0]
    if ref in ids:
        return ref
    if ticket and f"{ticket}:{ref}" in ids:
        return f"{ticket}:{ref}"
    for key in (ref, ref[4:] if ref.startswith("EXT:") else None):
        if key and key in aliases and aliases[key] in ids:
            return aliases[key]
    return None


class Graph:
    """deps[u] = [v...]; uses[(u, v)] = {use labels}; rdeps[v] = [u...]; dangling = [(u, raw)]."""

    def __init__(self, rows: list[dict], aliases: dict[str, str] | None = None):
        aliases = load_aliases() if aliases is None else aliases
        ids = {r["id"] for r in rows}
        self.deps, self.rdeps, self.uses, self.dangling = defaultdict(list), defaultdict(list), defaultdict(set), []
        self.unregistered = []  # references aliased to "-": literature, named premises, archive lemmas
        self.self_edges = []    # a claim listing itself (an error; recorded, not silently dropped)
        asm = load_assumptions()
        for r in rows:
            for item in split_list(r.get("depends_on", "")):
                ref, use = parse_dep(item)
                key = ref[4:] if ref.startswith("EXT:") else ref
                if aliases.get(ref) == "-" or aliases.get(key) == "-":
                    self.unregistered.append((r["id"], item))
                    continue
                t = resolve(ref, ids, aliases, r.get("ticket", ""))
                if t is None:
                    self.dangling.append((r["id"], item))
                    continue
                if t == r["id"]:
                    self.self_edges.append((r["id"], item))
                    continue
                self._add(r["id"], t, use)
            # interface rule: a consumer that binds the bridge it uses ("P:X@<claim id>") gets a proof-use edge to
            # that bridge (family/clause-specific; a plain "P:X" is informational and creates no edge)
            for item in split_list(r.get("consumes", "")):
                p, _, b = item.partition("@")
                if not b:
                    continue
                t = resolve(b, ids, aliases, r.get("ticket", ""))
                if t is None:
                    self.dangling.append((r["id"], item))
                elif t == r["id"]:
                    self.self_edges.append((r["id"], item))  # a claim cannot be its own bridge
                else:
                    self._add(r["id"], t, f"proof:{p.strip()}")

    def _add(self, u, t, use):
        if t not in self.deps[u]:
            self.deps[u].append(t)
            self.rdeps[t].append(u)
        self.uses[(u, t)].add(use)

    def dependents(self, cid: str, first_hop=lambda uses: True) -> dict[str, list[str]]:
        """Transitive dependents -> shortest path. `first_hop(uses)` filters the direct edges by what they use
        (e.g. a NARROW that still covers the use, or a PATCH that only affects proof-internal facts); every
        later hop propagates (a dependent in doubt puts its own dependents in doubt)."""
        paths = {cid: [cid]}
        q = deque([cid])
        while q:
            u = q.popleft()
            for v in sorted(self.rdeps.get(u, [])):
                if v in paths:
                    continue
                if u == cid and not first_hop(self.uses[(v, u)]):
                    continue
                paths[v] = paths[u] + [v]
                q.append(v)
        paths.pop(cid)
        return paths

    def cycles(self) -> list[list[str]]:
        color, stack, out = {}, [], []
        sys.setrecursionlimit(10000)

        def dfs(u):
            color[u] = 1
            stack.append(u)
            for v in self.deps.get(u, []):
                if color.get(v) == 1:
                    out.append(stack[stack.index(v):] + [v])
                elif color.get(v) is None:
                    dfs(v)
            stack.pop()
            color[u] = 2

        for u in list(self.deps):
            if color.get(u) is None:
                dfs(u)
        return out


# ---------------------------------------------------------------- strength: assumptions, partial order
def parse_asm(item: str) -> tuple[str, str]:
    """'A:X~nec' -> ('A:X', 'necessity'); default polarity 'hypothesis'."""
    ident, _, pol = item.partition("~")
    return ident.strip(), {"nec": "necessity", "iff": "iff"}.get(pol.strip(), "hypothesis")


def hypotheses(row: dict) -> list[str]:
    pol_default = "necessity" if row.get("kind") in ("counterexample", "obstruction") else None
    out = []
    for it in split_list(row.get("assumptions", "")):
        a, pol = parse_asm(it)
        if (pol_default or pol) == "hypothesis":
            out.append(a)
    return out


def asm_closure(ids, asm: dict[str, dict]) -> set[str]:
    """Everything implied by a set of assumptions through the assumption lattice (`implies` in assumptions.tsv)."""
    seen, stack = set(), list(ids)
    while stack:
        a = stack.pop()
        if a in seen:
            continue
        seen.add(a)
        stack += split_list(asm.get(a, {}).get("implies", ""))
    return seen


def necessity(claim: str, a: str, sharp: list[dict]) -> tuple[str, int]:
    """Aggregate verdict for (claim, assumption): best verdict and the number of DISTINCT failed removal routes
    (distinct by evidence text; duplicate rows do not count twice)."""
    rows = [s for s in sharp if s["claim"] == claim and s["assumption"] == a]
    fails = len({s.get("evidence", "").strip().lower() for s in rows
                 if s["verdict"] == "FAILED-REMOVAL" and s.get("evidence", "").strip()})
    for v in NECESSITY:
        if any(s["verdict"] == v for s in rows):
            return v, fails
    return "NONE", 0


def settled(claim: str, a: str, sharp) -> bool:
    v, fails = necessity(claim, a, sharp)
    return v == "NECESSARY" or fails >= 2


def improvable(row: dict, sharp) -> str:
    """Headline claims only: list the hypotheses with neither necessity evidence nor ≥ 2 failed removal routes."""
    if row.get("headline") != "yes":
        return ""
    if conclusion_level(row) == "negative" or row.get("kind") in ("counterexample", "obstruction"):
        return "n/a(negative result)"
    hyp = hypotheses(row)
    if not hyp:
        return "unknown(no assumptions recorded)"
    weak = [a for a in hyp if not settled(row["id"], a, sharp)]
    return f"yes({','.join(weak)})" if weak else "no"


def conclusion_level(row: dict) -> str:
    return row.get("conclusion", "").split(":", 1)[0].strip().lower() if row.get("conclusion") else ""


def implies_closure(rows: list[dict], src: str, aliases=None) -> set[str]:
    aliases = load_aliases() if aliases is None else aliases
    ids = {r["id"] for r in rows}
    imp = {r["id"]: [resolve(x, ids, aliases, r["ticket"]) for x in split_list(r.get("implies", ""))]
           for r in rows}
    seen, stack = set(), [src]
    while stack:
        for v in imp.get(stack.pop(), []):
            if v and v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def compare(x: dict, y: dict, asm: dict, declared: dict[str, str] | None = None) -> dict[str, str]:
    """Partial order Y vs X per axis: 'better' | 'equal' | 'worse' | 'incomparable' | 'unknown'.
    assumptions: Y's hypotheses must all follow from X's (via the lattice) to be no stronger.
    conclusion: level order. rate/scope: free text -> 'equal' if identical, else taken from `declared`
    (e.g. {"scope": "better"}) or 'unknown'."""
    declared = declared or {}
    out = {}
    hx, hy = set(hypotheses(x)), set(hypotheses(y))
    if not (hx or hy):
        out["assumptions"] = declared.get("assumptions", "unknown")
    else:
        y_le = hy <= asm_closure(hx, asm)   # Y assumes no more than X
        x_le = hx <= asm_closure(hy, asm)
        out["assumptions"] = declared.get("assumptions", "equal" if (y_le and x_le) else "better" if y_le else
                                          "worse" if x_le else "incomparable")
    lx, ly = conclusion_level(x), conclusion_level(y)
    if lx in CONCLUSION_LEVELS and ly in CONCLUSION_LEVELS:
        d = CONCLUSION_LEVELS.index(ly) - CONCLUSION_LEVELS.index(lx)
        c = "better" if d > 0 else "worse" if d < 0 else "equal"
        out["conclusion"] = declared.get("conclusion", c)
    else:
        out["conclusion"] = declared.get("conclusion", "equal" if x.get("conclusion") == y.get("conclusion")
                                         else "unknown")
    for f in ("rate", "scope"):
        out[f] = declared.get(f, "equal" if x.get(f, "") == y.get(f, "") else "unknown")
    return out


def verdict(axes: dict[str, str]) -> str:
    """'dominates' (≥ on every axis, > on one), 'equal', 'dominated', 'incomparable', or 'undetermined'."""
    v = set(axes.values())
    if "unknown" in v:
        return "undetermined"
    if "incomparable" in v or ({"better", "worse"} <= v):
        return "incomparable"
    if "better" in v:
        return "dominates"
    if "worse" in v:
        return "dominated"
    return "equal"


# ---------------------------------------------------------------- misc
def bump(version: str, level: str) -> str:
    if not SEMVER.match(version or ""):
        version = "1.0.0"
    a, b, c = (int(x) for x in version.split("."))
    return {"major": f"{a + 1}.0.0", "minor": f"{a}.{b + 1}.0"}.get(level, f"{a}.{b}.{c + 1}")


def today() -> str:
    return _dt.date.today().isoformat()


def safe(cid: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", cid)


# ---------------------------------------------------------------- staged copies (validate before writing)
STAGE_FILES = ("registry", "DECISIONS.md", "FAILED_ROUTES.md")


def make_stage() -> str:
    """A disposable copy of the INFRA state (registry/ without the seed fragments, DECISIONS.md, FAILED_ROUTES.md)
    in a fresh temporary directory. Tools run on it with BVS_STAGE_INFRA=<dir> (see run_staged)."""
    import shutil
    import tempfile
    d = tempfile.mkdtemp(prefix="bvs-stage-")
    for f in STAGE_FILES:
        s = os.path.join(INFRA, f)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(d, f), ignore=shutil.ignore_patterns("fragments", "*.tmp", "*.bak",
                                                                               "*.rst", ".TXN_*"))
        elif os.path.isfile(s):
            shutil.copy2(s, os.path.join(d, f))
    os.makedirs(os.path.join(d, "registry"), exist_ok=True)
    open(os.path.join(d, STAGE_MARK), "w").write("disposable registry stage (bvsreg.make_stage)\n")
    return d


def run_staged(stage: str, script: str, *args: str):
    """Run tools/<script> with every registry read/write redirected to the staged copy. -> (returncode, output)."""
    env = dict(os.environ, BVS_STAGE_INFRA=stage, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, os.path.join(TOOLS, script), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, cwd=ROOT)
    return p.returncode, p.stdout + p.stderr


def check_findings(stage: str | None = None, acceptance=None):
    """Run check.py (on the live registry, or on a staged copy; with `--acceptance <ids>` if given) ->
    (returncode, {(severity, check, id, message)}, printed summary line)."""
    import json
    import tempfile
    fd, out = tempfile.mkstemp(suffix=".json", prefix="bvs-check-")
    os.close(fd)
    try:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        env.pop("BVS_STAGE_INFRA", None)
        if stage:
            env["BVS_STAGE_INFRA"] = stage
        p = subprocess.run([sys.executable, os.path.join(TOOLS, "check.py"), "--quiet", "--json", out,
                            *(["--acceptance", *acceptance] if acceptance else [])],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=ROOT)
        try:
            with open(out, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            raise SystemExit(f"check.py did not run: {(p.stdout + p.stderr)[-800:]}")
    finally:
        os.remove(out)
    summary = next((l for l in p.stdout.splitlines() if l.startswith("check.py:")), "")
    return p.returncode, {(o["severity"], o["check"], o["id"], o["message"]) for o in data["findings"]}, summary


def commit_stage(stage: str) -> list[str]:
    """Copy a validated staged state back into the live INFRA: every top-level registry file, DECISIONS.md,
    FAILED_ROUTES.md and new issues/ folders that differ, as ONE transaction (replace_all): a failure restores
    every file already replaced and removes the new ones."""
    import filecmp
    import shutil
    pairs = []
    sreg = os.path.join(stage, "registry")
    for f in sorted(os.listdir(sreg)):
        if os.path.isfile(os.path.join(sreg, f)) and not f.endswith((".tmp", ".bak", ".rst")) \
                and not f.startswith(".TXN_"):
            pairs.append((os.path.join(sreg, f), os.path.join(REG, f)))
    for f in ("DECISIONS.md", "FAILED_ROUTES.md"):
        if os.path.isfile(os.path.join(stage, f)):
            pairs.append((os.path.join(stage, f), os.path.join(INFRA, f)))
    sis = os.path.join(stage, "issues")
    if os.path.isdir(sis):
        for dp, _, fs in os.walk(sis):
            for f in fs:
                s = os.path.join(dp, f)
                pairs.append((s, os.path.join(INFRA, "issues", os.path.relpath(s, sis))))
    pairs = [(s, d) for s, d in pairs if not (os.path.isfile(d) and filecmp.cmp(s, d, shallow=False))]
    prepared, made = [], []
    try:
        for s, d in pairs:
            d = safe_dest(d)
            dd = os.path.dirname(d)
            if not os.path.isdir(dd):
                os.makedirs(dd)
                made.append(dd)
            shutil.copyfile(s, safe_dest(d + ".tmp"))
            prepared.append((d + ".tmp", d))
        replace_all(prepared)
    except BaseException:
        for tmp, _ in prepared:
            if os.path.exists(tmp):
                os.remove(tmp)
        for dd in reversed(made):
            shutil.rmtree(dd, ignore_errors=True)
        raise
    return [os.path.relpath(d, ROOT) for _, d in prepared]


# ---------------------------------------------------------------- gates
_GATE = re.compile(r"^([A-Za-z][\w-]*):([^\s()]+)(?:\s*\((.*)\))?$", re.S)


def split_gates(gts: str) -> list[str]:
    """Split a `gates` cell at ';' outside parentheses (evidence may contain ';')."""
    out, depth, cur = [], 0, ""
    for c in gts or "":
        depth += (c == "(") - (c == ")" and depth > 0)
        if c == ";" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def parse_gates(gts: str):
    """`gates` -> ([(name, result, evidence)], [unparsable entries]). Each entry is anchored: `name:RESULT(evidence)`
    with the name the WHOLE token before ':' (so `not-lit:PASS(x)` is gate `not-lit`, never `lit`)."""
    ok, bad = [], []
    for e in split_gates(gts):
        m = _GATE.match(e)
        if m:
            ok.append((m.group(1), m.group(2), (m.group(3) or "").strip()))
        else:
            bad.append(e)
    return ok, bad


def passed_gates(gts: str) -> set:
    """Gate names whose ONLY recorded result is PASS with evidence (a contradictory FAIL/PENDING entry for the same
    gate, or an evidence-less PASS, does not count)."""
    res = {}
    for n, r, ev in parse_gates(gts)[0]:
        res.setdefault(n, []).append((r, ev))
    return {n for n, rs in res.items() if all(r == "PASS" and ev for r, ev in rs)}


# ---------------------------------------------------------------- evidence references (F2 / R05)
def _pathlike(t: str) -> bool:
    """A later evidence token is a file reference if it has a path separator, a commit pin, or a file extension
    (any length), and contains a letter or digit."""
    if not re.search(r"[A-Za-z0-9]", t):
        return False
    return bool(re.search(r"[/\\@]", t) or re.search(r"\.[A-Za-z][A-Za-z0-9_]*(?::\d+(?:-\d+)?)?$", t))


def evidence_refs(ev: str) -> list[str]:
    """The file references in an evidence text: its first token (always a reference), plus every later token that
    looks like a file path (`x.md`, `dir/x`, `x.longext`, `dir/x.md:12-30`, `x.md@<commit>`, `C:\\x`). Tokens are
    separated by ',' or blanks."""
    toks = [t.strip("`'\"") for t in re.split(r"[\s,]+", ev or "") if t.strip("`'\"")]
    return toks[:1] + [t for t in toks[1:] if _pathlike(t)]


def evidence_bases(row: dict, folder: str = "") -> list[str]:
    """Directories an evidence path may be relative to: the repo root, the ticket folder (and its parent), the
    folder of the statement file and of the status source."""
    out = [""]
    for d in (folder, os.path.dirname(folder) if folder else "", os.path.dirname(row.get("file", "")),
              os.path.dirname((row.get("status_source", "") or "").rpartition(":")[0])):
        if d and d not in out:
            out.append(d)
    return out


def resolve_evidence(tok: str, row: dict, folder: str = ""):
    """`path[:a-b][@commit]` -> (repo path, commit or '', None) or (None, '', problem). The file must exist in the
    repository (and, when pinned, at that commit); a line span must be readable."""
    path, pin = tok, ""
    if "@" in tok:
        path, _, pin = tok.rpartition("@")
        if git("rev-parse", "--verify", "--quiet", pin + "^{commit}")[0] != 0:
            return None, "", f"evidence {tok!r}: pinned commit {pin!r} is not a commit in this repository"
    m = re.match(r"^(.*?):(\d+(?:-\d+)?)$", path)
    span = m.group(2) if m else ""
    path = m.group(1) if m else path
    tried = []
    for b in evidence_bases(row, folder):
        c = _pkey(os.path.join(b, path) if b else path)
        if c.startswith("../") or c == ".." or os.path.isabs(c) or c in tried:
            continue
        tried.append(c)
        ok = git("cat-file", "-t", f"{pin}:{c}") == (0, "blob") if pin else repo_file_exists(c)
        if not ok:
            continue
        if span:
            lines = read_lines_at(c, pin) if pin else read_lines(c)
            sp = parse_span(span)
            if lines is None or sp is None or sp[1] > len(lines):
                return None, "", f"evidence {tok!r}: span {span} not readable in {c}"
        return c, pin, None
    where = f" at commit {pin}" if pin else ""
    return None, "", f"evidence {tok!r} resolves to no file{where} (tried: {', '.join(tried) or '-'})"


def evidence_text(path: str, pin: str = "") -> str:
    lines = read_lines_at(path, pin) if pin else read_lines(path)
    return "\n".join(lines or [])


# ---------------------------------------------------------------- checkpoint status sources (INFRA R05)
# Wave 3 tickets write their per-claim status lines in their own CHECKPOINT_<k>.md, which manifest.py never covers (a
# status line written after the council cannot be inside the manifest the council reviewed). Such a status source is
# exempt from manifest coverage (statement and premise files are NOT), and only under checkpoint_problems:
#   (a) the row records the checkpoint's content digest (`status_sha256`, written at ingest) and the file still has it;
#   (b) the claim ids of the checkpoint (its REGISTRY blocks, plus every registry row whose status source is that
#       file) equal, for EACH council seat, the ids that seat accepted in its per-claim table;
#   (c) every review round cited in the claim's status line resolves to exactly one existing review file of the
#       ticket, and that file quotes the digest of an existing frozen manifest of the ticket (an earlier round binds
#       to its own manifest; the acceptance round R<k> of the council cell resolves to the council seats' review
#       files, which A4 binds to the acceptance manifest with a PASS verdict).
_CKPT_NAME = re.compile(r"^CHECKPOINT_(\d+)\.md$")
# a cited review round: `<ROUND>:` or `<ROUND> (<note>):` followed by a blank or the line end, where ROUND is upper-case
# letters / digits with optional `-` parts and contains a digit (LC1-A, BR1, SW1, R2, RC-R2); `W3-START:AGG` is not one
_ROUND_CITE = re.compile(r"(?<![\w:./-])([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)(?:\s*\([^()]*\))?:(?=\s|$)")
_HEX64 = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])")
_ID_HEAD = ("id", "claim", "claim id")
_DECISION_HEAD = ("decision", "disposition")


def status_sha(source: str) -> str:
    """What `status_sha256` records for a status source: the content digest (line-wise, CRLF / LF stable) of its file
    when that file is a CHECKPOINT_<k>.md; '' for any other source or an unreadable file."""
    path = _pkey((source or "").rpartition(":")[0]) if (source or "").rpartition(":")[0] else ""
    if not path or not _CKPT_NAME.match(os.path.basename(path)):
        return ""
    lines = read_lines(path)
    return _digest(lines) if lines is not None else ""


def own_checkpoint(row: dict, folder: str = "") -> str:
    """The repository path of the claim's status source if it is its OWN ticket's CHECKPOINT_<k>.md (directly in the
    ticket folder: tickets.tsv `folder`, else the statement file's folder) and exists; else ''."""
    raw = (row.get("status_source", "") or "").rpartition(":")[0]
    path = _pkey(raw) if raw else ""
    d = ticket_dir(row, folder)
    if not path or not d or d == "." or not _CKPT_NAME.match(os.path.basename(path)):
        return ""
    if _pcase(os.path.dirname(path)) != _pcase(d) or not repo_file_exists(path):
        return ""
    return path


_INGEST_MOD = None


def _ingest_tool():
    """ingest.py as a library: one REGISTRY-block grammar for ingest and for the checkpoint's claim ids."""
    global _INGEST_MOD
    if _INGEST_MOD is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("bvs_ingest_tool", os.path.join(TOOLS, "ingest.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _INGEST_MOD = mod
    return _INGEST_MOD


def checkpoint_claim_ids(path: str, rows: list[dict]) -> set:
    """The claim ids a checkpoint carries: the ids of its REGISTRY blocks (ingest.py's grammar) and of every registry
    row whose status source is that file."""
    try:
        objs = _ingest_tool().convert_report(os.path.join(ROOT, path))[0]
    except Exception:  # pragma: no cover - an unreadable checkpoint fails (a) anyway
        objs = []
    ids = {f"{o.get('ticket', '')}:{o.get('local_id', '')}" for o in objs if o.get("ticket") and o.get("local_id")}
    for r in rows:
        raw = (r.get("status_source", "") or "").rpartition(":")[0]
        if raw and _pcase(raw) == _pcase(path):
            ids.add(r["id"])
    return ids


def _cells(line: str) -> list[str]:
    t = line.strip()
    return [c.strip() for c in t.strip("|").split("|")] if t.startswith("|") else []


def _plain(c: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*`]", "", c)).strip()


def seat_decisions(text: str, ticket: str):
    """A council review's per-claim table(s) -> ({full claim id: accepted?}, [problems]). A per-claim table is a
    Markdown table whose header's first cell is `id` (or `claim`, `claim id`) and second `decision` (or
    `disposition`), case-insensitive; a row is accepted iff its decision starts with `accepted` (`accepted with
    non-blocking remarks` counts, `not accepted` does not). A local id gets the ticket prefix. An id listed twice with
    different decisions is not accepted."""
    dec, probs, tables, in_t = {}, [], 0, False
    for ln in text.splitlines():
        cs = _cells(ln)
        if not cs:
            in_t = False
            continue
        if len(cs) >= 2 and _plain(cs[0]).lower() in _ID_HEAD and _plain(cs[1]).lower() in _DECISION_HEAD:
            in_t, tables = True, tables + 1
            continue
        if not in_t or len(cs) < 2 or re.fullmatch(r"[\s:|-]*", ln.strip()):
            continue
        cid = _plain(cs[0])
        if not cid:
            continue
        cid = cid if ":" in cid else f"{ticket}:{cid}"
        ok = _plain(cs[1]).lower().startswith("accepted")
        if cid in dec and dec[cid] != ok:
            probs.append(f"{cid} is listed with contradictory decisions")
        dec[cid] = ok and dec.get(cid, True)
    if not tables:
        probs.append("no per-claim table (`| id | decision |`) found")
    return dec, probs


def cited_rounds(text: str) -> list[str]:
    """The review rounds cited in a status line (see _ROUND_CITE), in order, without repeats."""
    return list(dict.fromkeys(m.group(1) for m in _ROUND_CITE.finditer(text or "")
                              if any(ch.isdigit() for ch in m.group(1))))


def round_files(rid: str, d: str) -> list[str]:
    """Review files of round `rid` in `<d>/reviews/`: names starting with `<rid>_` (`-` also read as `_`);
    dispositions, briefs and manifests excluded."""
    import glob
    pre = (rid + "_", rid.replace("-", "_") + "_")
    out = []
    for fp in sorted(glob.glob(os.path.join(ROOT, d, "reviews", "*"))):
        b = os.path.basename(fp)
        if not os.path.isfile(fp) or "disposition" in b.lower() or b.upper().startswith(("BRIEF", "MANIFEST")):
            continue
        if b.startswith(pre):
            out.append(os.path.relpath(fp, ROOT).replace(os.sep, "/"))
    return out


def manifest_digests(d: str) -> dict[str, str]:
    """{digest: manifest path} of every `<d>/reviews/MANIFEST_*.txt` (its header line)."""
    import glob
    out = {}
    for mp in sorted(glob.glob(os.path.join(ROOT, d, "reviews", "MANIFEST_*.txt"))):
        rel = os.path.relpath(mp, ROOT).replace(os.sep, "/")
        lines = read_lines(rel)
        m = re.fullmatch(r"MANIFEST ([0-9a-f]{64})", lines[0].strip()) if lines else None
        if m:
            out[m.group(1)] = rel
    return out


def checkpoint_problems(row: dict, folder: str, ck: str, rnd, seat_files, rows: list[dict] | None = None) -> list[str]:
    """[] iff the claim's own CHECKPOINT_<k>.md `ck` may stand as its (uncovered) status source: (a), (b), (c) above.
    `seat_files`: [(seat, review path, pin)] of the council cell; `rnd`: its round number."""
    probs = []
    # (a) the checkpoint is frozen at ingest
    rec, cur = (row.get("status_sha256") or "").strip(), status_sha(row.get("status_source", ""))
    if not rec:
        probs.append(f"status source {ck} is the ticket's checkpoint, but the row records no status_sha256 (written "
                     "at ingest): re-ingest, or put the status line in a file the frozen manifest covers")
    elif rec != cur:
        probs.append(f"checkpoint {ck} changed after ingest (status_sha256 {rec[:12]}... != current "
                     f"{(cur or 'UNREADABLE')[:12]}...): an ingested checkpoint is frozen")
    # (b) the checkpoint's claim ids == the ids EACH council seat accepted
    rows = load_claims() if rows is None else rows
    ck_ids = checkpoint_claim_ids(ck, rows)
    ticket = row.get("ticket", "") or row.get("id", "").partition(":")[0]
    if not seat_files:
        probs.append(f"checkpoint {ck}: no council review file to compare its claim ids with")
    for name, path, pin in seat_files:
        dec, dp = seat_decisions(evidence_text(path, pin), ticket)
        probs += [f"seat {name}: review {path}: {p}" for p in dp]
        acc = {k for k, v in dec.items() if v}
        for lab, ids_ in (("carries claim id(s) this seat did not accept", ck_ids - acc),
                          ("lacks claim id(s) this seat accepted", acc - ck_ids)):
            if ids_:
                ids_ = sorted(ids_)
                probs.append(f"seat {name}: checkpoint {ck} {lab} in {path}: {', '.join(ids_[:8])}"
                             f"{' ...' if len(ids_) > 8 else ''} (the checkpoint's ids must equal each seat's accepted ids)")
    # (c) each review round cited in the status line -> exactly one review file, quoting a frozen manifest's digest
    d = ticket_dir(row, folder)
    sp = parse_span(((row.get("status_source", "") or "").rpartition(":")[2]).split(",")[0])
    lines = read_lines(ck) or []
    text = " ".join(lines[sp[0] - 1: sp[1]]) if sp and sp[1] <= len(lines) else ""
    if not text:
        probs.append(f"status line {row.get('status_source')} unreadable")
    mans = None
    for rid in cited_rounds(text):
        if rnd is not None and rid == f"R{rnd}":
            continue  # the acceptance round: the council seats' files, bound to the acceptance manifest (A4)
        fs = round_files(rid, d)
        if len(fs) != 1:
            probs.append(f"the status line cites review round {rid}, which resolves to "
                         + (f"{len(fs)} review files ({', '.join(fs[:4])})" if fs else f"no file {d}/reviews/{rid}_*")
                         + ": a cited round must resolve to exactly one review file")
            continue
        mans = manifest_digests(d) if mans is None else mans
        if not set(_HEX64.findall(evidence_text(fs[0]))) & set(mans):
            probs.append(f"review {fs[0]} (round {rid}, cited in the status line) quotes no digest of a frozen "
                         f"{d}/reviews/MANIFEST_*.txt")
    return probs


# ---------------------------------------------------------------- council record (R10)
# `council` cell, one machine-readable format (LIFECYCLE §4.1):
#   R<k>; MANIFEST <64-hex>; <seat>=<score> PASS(<review file>); <seat>=<score> PASS(<review file>)
# one passing round: its number, the frozen manifest digest both seats reviewed, and per seat the score and whether
# ALL that seat's gates passed (PASS | FAIL), with the seat's review file (which must quote the digest).
_C_ROUND = re.compile(r"^R(\d+)$")
_C_MAN = re.compile(r"^MANIFEST ([0-9a-f]{64})$")
_C_SEAT = re.compile(r"^([A-Za-z][\w.-]*)=(\d+(?:\.\d+)?) (PASS|FAIL)\((.+)\)$")
COUNCIL_MIN = 8.0


MANIFEST_TOOL = os.path.join(ROOT, "Theory_work", "Wave3", "tools", "manifest.py")
_MANIFEST_MOD = None


def manifest_tool():
    """The Wave 3 manifest tool (freeze / verify / verdict-line grammar), loaded as a library: ONE grammar for
    `manifest.py bind` and CP3 acceptance (R03-N2)."""
    global _MANIFEST_MOD
    if _MANIFEST_MOD is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("bvs_manifest_tool", MANIFEST_TOOL)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MANIFEST_MOD = mod
    return _MANIFEST_MOD


def ticket_dir(row: dict, folder: str = "") -> str:
    """The ticket folder whose reviews/MANIFEST_*.txt holds a claim's council manifest: tickets.tsv `folder`, else the
    folder of the claim's statement file."""
    return _pkey(folder or os.path.dirname(row.get("file", "")) or "")


def manifest_problems(row: dict, folder: str, dg: str) -> list[str]:
    """R03-N2: the council digest must be the header of an existing `<ticket>/reviews/MANIFEST_*.txt`, and
    `manifest.py verify` of that manifest must pass on the CURRENT tree (content changed after the round -> refused)."""
    import glob
    d = ticket_dir(row, folder)
    if not d or d == ".":
        return [f"no ticket folder for {row.get('id')} (tickets.tsv folder / statement file): cannot find the frozen "
                "manifest of the round"]
    try:
        M = manifest_tool()
    except Exception as e:  # pragma: no cover - the tool is part of the repository
        return [f"cannot load {MANIFEST_TOOL}: {e}"]
    found = []
    for mp in sorted(glob.glob(os.path.join(ROOT, d, "reviews", "MANIFEST_*.txt"))):
        try:
            with open(mp, encoding="utf-8") as fh:
                head = fh.readline().strip()
        except OSError:
            continue
        if head == f"MANIFEST {dg}":
            found.append(mp)
    if not found:
        return [f"no {d}/reviews/MANIFEST_*.txt has the header `MANIFEST {dg[:12]}...`: the council digest must be the "
                "round's frozen manifest of this ticket (manifest.py freeze), still present"]
    probs = []
    for mp in found:
        rel = os.path.relpath(mp, ROOT).replace(os.sep, "/")
        try:
            _, diffs = M.verify_problems(os.path.join(ROOT, d), mp, ROOT)
        except M.ManifestError as e:
            diffs = [str(e)]
        if diffs:
            probs.append(f"`manifest.py verify {d} {rel}` fails on the current tree ({len(diffs)} difference(s): "
                         f"{'; '.join(diffs[:3])}{' ...' if len(diffs) > 3 else ''}): the reviewed content changed after "
                         "the round (rule 15: a fresh review of the change is needed)")
            continue
        # the manifest must cover what the claim IS: its statement file, premise files and status source (a file
        # outside the ticket folder must be listed in reviews/INPUTS.txt), else a verified digest proves nothing
        covered = set()
        for ln in M.read_manifest(mp)[2]:
            p_ = ln[66:]
            covered.add(_pcase(p_[4:] if p_.startswith("EXT:") else f"{d}/{p_}"))
        # INFRA R05: a status source that is the ticket's OWN CHECKPOINT_<k>.md (excluded from every manifest by
        # design) is exempt from coverage, as status source only; council_problems then runs checkpoint_problems
        ck = own_checkpoint(row, folder)
        need = [row.get("file", "")] + ([] if ck else [(row.get("status_source", "") or "").rpartition(":")[0]])
        need += [split_premise(x)[0].rpartition(":")[0] for x in split_list(row.get("premises", ""))
                 if not split_premise(x)[1]]  # an archived premise span is frozen in git
        for f_ in dict.fromkeys(x for x in need if x):
            if _pcase(f_) not in covered:
                probs.append(f"the frozen manifest {rel} does not cover {f_} (statement / premise / status source of "
                             f"{row.get('id')}): list it in reviews/INPUTS.txt before the freeze")
    return probs


def council_problems(row: dict, folder: str = "", rows: list[dict] | None = None) -> list[str]:
    """[] iff the claim's council record is a CP3-PASS: two seats (distinct names, distinct review files), each
    >= 8.0 with all gates PASS, in one round, on one MANIFEST digest; that digest is the header of the ticket's
    reviews/MANIFEST_*.txt, which still verifies on the current tree; and every seat's review file contains exactly one
    `COUNCIL-VERDICT` line for that digest matching the cell (round, seat, score, gates=PASS) and no contradictory
    verdict line (R03-N2: an outcome bound to the digest, not a mention of it). When the status source is the
    ticket's own CHECKPOINT_<k>.md (exempt from manifest coverage), checkpoint_problems must also be empty (INFRA R05);
    `rows`: the registry rows (default: claims.tsv), for the checkpoint's claim ids."""
    cell = (row.get("council") or "").strip()
    if not cell:
        return ["no council record (format: R<k>; MANIFEST <64-hex>; <seat>=<score> PASS(<review>); "
                "<seat>=<score> PASS(<review>))"]
    rounds, mans, seats, probs = [], [], [], []
    for e in split_gates(cell):
        if _C_ROUND.match(e):
            rounds.append(e)
        elif _C_MAN.match(e):
            mans.append(_C_MAN.match(e).group(1))
        elif _C_SEAT.match(e):
            seats.append(_C_SEAT.match(e).groups())
        else:
            probs.append(f"unparsable council entry {e[:60]!r}")
    if len(rounds) != 1:
        probs.append(f"needs exactly one round entry R<k> (found {len(rounds)})")
    if len(mans) != 1:
        probs.append(f"needs exactly one `MANIFEST <64-hex>` digest (found {len(mans)})")
    names = {s[0].lower() for s in seats}
    if len(seats) < 2 or len(names) != len(seats):
        probs.append(f"needs two (or more) distinct seats (found {[s[0] for s in seats]})")
    if len(mans) == 1:
        probs += manifest_problems(row, folder, mans[0])
    rnd = int(_C_ROUND.match(rounds[0]).group(1)) if len(rounds) == 1 else None
    files, seat_files = [], []
    for name, score, res, ev in seats:
        if float(score) < COUNCIL_MIN or float(score) > 10:
            probs.append(f"seat {name}: score {score} not in [{COUNCIL_MIN}, 10]")
        if res != "PASS":
            probs.append(f"seat {name}: not all gates PASS ({res})")
        refs = evidence_refs(ev)
        if len(refs) != 1:
            probs.append(f"seat {name}: give exactly one review file (got {ev[:60]!r})")
            continue
        path, pin, prob = resolve_evidence(refs[0], row, folder)
        if prob:
            probs.append(f"seat {name}: {prob}")
            continue
        if _pcase(path) in files:  # same repository file, whatever its case or commit pin (two seats = two reviews)
            probs.append(f"seat {name}: review file {path} is also another seat's (two seats = two reviews)")
        files.append(_pcase(path))
        seat_files.append((name, path, pin))
        if len(mans) == 1:
            try:
                _, vp = manifest_tool().verdict_problems(evidence_text(path, pin), mans[0], rnd, name, score)
            except Exception as e:  # pragma: no cover
                vp = [f"cannot check the verdict line ({e})"]
            probs += [f"seat {name}: review {path}: {p}" for p in vp]
    ck = own_checkpoint(row, folder)
    if ck:
        probs += checkpoint_problems(row, folder, ck, rnd, seat_files, rows)
    return probs


# ---------------------------------------------------------------- durable acceptance records (R03-N1, R04-N1/N2)
# A checked (PROVED-CHECKED-class) claim consumed by an accepted claim must itself have been accepted: an `accept`
# event written by `check.py --acceptance ... --record` (or `ingest.py ... --staged --record`) for its CURRENT
# acceptance identity, or membership in the frozen legacy boundary (claims PROVED-CHECKED on main at tag LEGACY_TAG).
# The identity (R04-N1/N2) is the fingerprint of everything acceptance read: the row fields below (statement source
# and span, provenance, status, edges, gates, council), the ticket folder that locates the frozen manifest, the
# EFFECTIVE dependency graph (resolved inputs with their uses, version, statement hash and status: alias edits count),
# the names the claim answers to, and the CONTENT of every referenced artifact (gate evidence files, council review
# files, the round's frozen MANIFEST_*.txt); a missing artifact is part of the identity as MISSING. In addition, an
# accepted input whose identity still matches is re-checked on the current tree (A5 revalidation, check.py).
ACCEPT_FIELDS = ("id", "ticket", "kind", "name", "file", "lines", "premises", "sha256", "version", "status",
                 "status_source", "status_sha256", "depends_on", "consumes", "assumptions", "gates", "council",
                 "headline")
ACCEPT_FORMAT = "fp2"  # stamp format: `v<version> fp2:<24 hex>`; older `fp:` records are stale (re-accept)
LEGACY_TAG = "theory-v2.0-pre"
LEGACY_FILE = os.path.join(os.path.dirname(TOOLS), "LEGACY_ACCEPTED.tsv")  # the repository file, never a stage copy


def ticket_folders() -> dict[str, str]:
    """{ticket: tickets.tsv folder}."""
    return {t["ticket"]: t.get("folder", "") for t in load_tickets()}


def _digest(lines) -> str:
    """Content digest of a file read line-wise (CRLF and LF checkouts give the same digest)."""
    return hashlib.sha256("\n".join(lines).encode("utf-8", errors="replace")).hexdigest()


def accept_artifacts(row: dict, folder: str = "") -> list[str]:
    """The artifacts a claim's acceptance rests on, each as `<reference> -> <repo path>[@pin] <content digest>` (or
    `<reference> MISSING`): every gate evidence reference (whatever the result), every council seat's review file and
    each `<ticket>/reviews/MANIFEST_*.txt` whose header is the council digest."""
    import glob
    out = set()
    refs = [ev for _, _, ev in parse_gates(row.get("gates", ""))[0] if ev.strip()]
    mans = []
    for e in split_gates(row.get("council", "")):
        m = _C_SEAT.match(e)
        if m:
            refs.append(m.group(4))
        m = _C_MAN.match(e)
        if m:
            mans.append(m.group(1))
    for ev in refs:
        for tok in evidence_refs(ev):
            path, pin, prob = resolve_evidence(tok, row, folder)
            if prob:
                out.add(f"{tok} MISSING")
                continue
            lines = read_lines_at(path, pin) if pin else read_lines(path)
            out.add(f"{tok} -> {_pcase(path)}{'@' + pin if pin else ''} "
                    + (_digest(lines) if lines is not None else "UNREADABLE"))
    d = ticket_dir(row, folder)
    for dg in mans:
        hit = False
        if d and d != ".":
            for mp in sorted(glob.glob(os.path.join(ROOT, d, "reviews", "MANIFEST_*.txt"))):
                rel = os.path.relpath(mp, ROOT).replace(os.sep, "/")
                lines = read_lines(rel)
                if lines and lines[0].strip() == f"MANIFEST {dg}":
                    out.add(f"MANIFEST {dg} -> {_pcase(rel)} {_digest(lines)}")
                    hit = True
        if not hit:
            out.add(f"MANIFEST {dg} MISSING")
    return sorted(out)


def accept_identity(cid: str, by: dict, g, aliases: dict, folders: dict | None = None) -> list[str]:
    """The acceptance identity of a claim (see above) as a list of lines; accept_stamp fingerprints it."""
    row = by[cid]
    folders = ticket_folders() if folders is None else folders
    folder = folders.get(row.get("ticket", ""), "")
    ident = [f"{k}={row.get(k) or ''}" for k in ACCEPT_FIELDS]
    ident.append(f"ticket-folder={ticket_dir(row, folder)}")
    ident.append("names=" + "|".join(sorted(claim_names(cid, by, aliases))))
    for t in sorted(g.deps.get(cid, [])):
        tr = by.get(t, {})
        ident.append(f"input={t}@{','.join(sorted(g.uses[(cid, t)]))} v{tr.get('version', '')} "
                     f"{tr.get('sha256', '')} {tr.get('status', '')}")
    ident += [f"artifact={a}" for a in accept_artifacts(row, folder)]
    return ident


def accept_stamp(cid: str, by: dict, g, aliases: dict, folders: dict | None = None) -> str:
    """`v<version> fp2:<24 hex>`: what an accept event records. The fingerprint covers the whole acceptance identity
    (row fields, ticket folder, effective inputs, names, artifact contents), so ANY later change makes it stale."""
    fp = hashlib.sha256("\x1f".join(accept_identity(cid, by, g, aliases, folders)).encode()).hexdigest()[:24]
    return f"v{by[cid].get('version', '')} {ACCEPT_FORMAT}:{fp}"


def accept_records() -> dict[str, set]:
    """{claim id: {accept stamps}} from the events log."""
    out = defaultdict(set)
    for e in read_tsv(EVENTS)[1]:
        if e.get("action") == "accept":
            out[e.get("id", "")].add(e.get("after", ""))
    return out


def legacy_rows_at(tag: str):
    """{(id, version, sha256)} of the claims with a PROVED-CHECKED-class status in a VALID state in the registry
    committed at `tag` -> (set, commit) or (None, problem)."""
    rc, commit = git("rev-parse", "--verify", "--quiet", tag + "^{commit}")
    if rc != 0:
        return None, f"tag {tag!r} is not a commit in this repository"
    rc, txt = git("show", f"{commit}:Theory_work/INFRA/registry/claims.tsv")
    if rc != 0:
        return None, f"cannot read the registry at {tag}"
    return {(r["id"], r.get("version", ""), r.get("sha256", "")) for r in read_tsv_text(txt)
            if status_strength(r.get("status", "")) == 3 and r.get("state") in VALID}, commit


def load_legacy():
    """The legacy boundary file -> (tag, commit, {(id, version, sha256)}, [format problems]); empty if absent."""
    if not os.path.isfile(LEGACY_FILE):
        return "", "", set(), []
    tag, commit, rows, probs = "", "", set(), []
    for n, ln in enumerate(open(LEGACY_FILE, encoding="utf-8").read().splitlines(), 1):
        if not ln.strip() or ln.startswith("#") or ln == "id\tversion\tsha256":
            continue
        c = ln.split("\t")
        if c[0] == "tag" and len(c) == 3 and not tag:
            tag, commit = c[1], c[2]
        elif len(c) == 3 and c[0] != "tag":
            rows.add(tuple(c))
        else:
            probs.append(f"line {n}: unparsable {ln[:80]!r}")
    if not tag:
        probs.append("no `tag<TAB><name><TAB><commit>` line")
    return tag, commit, rows, probs


_LEGACY = None


def legacy_boundary():
    """-> ({(id, version, sha256)} that may be trusted as accepted, [problems]). The file is trusted only if it is
    exactly what `bvsreg.py legacy-boundary` derives from its tag, and the tag still names the recorded commit; any
    hand edit empties the boundary (fail closed) and is reported (L1-legacy)."""
    global _LEGACY
    if _LEGACY is None:
        tag, commit, rows, probs = load_legacy()
        if not tag and not rows and not probs:
            _LEGACY = (set(), [])
        elif probs:
            _LEGACY = (set(), [f"{os.path.basename(LEGACY_FILE)}: {p}" for p in probs])
        elif tag != LEGACY_TAG:  # Sol toolfix3 N1.b: the file may not choose its own (later) source
            _LEGACY = (set(), [f"{os.path.basename(LEGACY_FILE)}: names tag {tag!r}; the legacy boundary is the "
                               f"registry at {LEGACY_TAG} only"])
        else:
            want, got = legacy_rows_at(tag)
            if want is None:
                _LEGACY = (set(), [f"{os.path.basename(LEGACY_FILE)}: {got}: the boundary cannot be verified"])
            elif got != commit:
                _LEGACY = (set(), [f"{os.path.basename(LEGACY_FILE)}: tag {tag} now names {got[:12]}, not the recorded "
                                   f"{commit[:12]}"])
            elif rows != want:
                extra, miss = sorted(rows - want), sorted(want - rows)
                _LEGACY = (set(), [f"{os.path.basename(LEGACY_FILE)} differs from the registry at {tag}: "
                                   f"{len(extra)} row(s) not there (e.g. {', '.join(r[0] for r in extra[:3]) or '-'}), "
                                   f"{len(miss)} missing (e.g. {', '.join(r[0] for r in miss[:3]) or '-'}); the "
                                   "boundary is frozen: regenerate nothing, revert the edit"])
            else:
                _LEGACY = (rows, [])
    return _LEGACY


def write_legacy_boundary() -> int:
    """`bvsreg.py legacy-boundary`: write LEGACY_ACCEPTED.tsv ONCE, from tag LEGACY_TAG (refuses if it exists)."""
    tag = LEGACY_TAG
    if os.path.exists(LEGACY_FILE):
        print(f"refused: {LEGACY_FILE} exists (the legacy boundary is generated once and frozen)")
        return 1
    rows, commit = legacy_rows_at(tag)
    if rows is None:
        print(f"refused: {commit}")
        return 1
    with open(safe_dest(LEGACY_FILE), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# LEGACY_ACCEPTED.tsv: the frozen legacy acceptance boundary (LIFECYCLE §4 A5; R03 finding N1).\n"
                 f"# Claims with a PROVED-CHECKED-class status in a valid state in the registry at tag {tag}, which\n"
                 "# predate CP3 acceptance records. Generated ONCE by `python Theory_work/INFRA/tools/bvsreg.py\n"
                 "# legacy-boundary`; never edit it: check.py recomputes it from the tag (L1-legacy ERROR on any\n"
                 "# difference) and a row counts only while the claim's id, version and statement hash are unchanged.\n"
                 f"tag\t{tag}\t{commit}\nid\tversion\tsha256\n"
                 + "".join(f"{i}\t{v}\t{h}\n" for i, v, h in sorted(rows)))
    print(f"wrote {LEGACY_FILE}: {len(rows)} claim(s) at {tag} ({commit[:12]})")
    return 0


def unaccepted_inputs(cid: str, by: dict, g, aliases: dict, now: set, records=None, legacy=None, revalidate=None,
                      folders=None):
    """R03-N1 / R04-N1: checked claims cid consumes (stmt / proof / bound-bridge edges, transitively; an @hyp edge too
    unless the consuming claim's status is `conditional on` it) that have neither an accept event for their CURRENT
    acceptance identity (accept_stamp) nor a legacy-boundary row for their current id + version + statement hash, or
    whose identity matches but which no longer pass acceptance on the current tree (`revalidate(id)` -> [problems];
    memoised by the caller) -> [(id, path, why)]. Claims accepted in this same run (`now`) count as accepted (the run
    refuses as a whole on any ERROR); legacy-boundary claims are not revalidated (they predate CP3 records)."""
    records = accept_records() if records is None else records
    legacy = legacy_boundary()[0] if legacy is None else legacy
    folders = ticket_folders() if folders is None else folders
    out, seen, q = [], {cid}, deque([(cid, [cid])])
    while q:
        u, path = q.popleft()
        for d in g.deps.get(u, []):
            if d in seen or d not in by:
                continue
            if g.uses[(u, d)] == {"hyp"} and conditional_on(by[u].get("status", ""), claim_names(d, by, aliases)):
                continue  # a declared condition is assumed, not consumed
            seen.add(d)
            q.append((d, path + [d]))
            dr = by[d]
            if dr.get("state") not in VALID or status_strength(dr.get("status", "")) != 3 or d in now:
                continue
            if (d, dr.get("version", ""), dr.get("sha256", "")) in legacy:
                continue
            have = records.get(d, set())
            if accept_stamp(d, by, g, aliases, folders) in have:
                probs = revalidate(d) if revalidate else []
                if probs:
                    out.append((d, path + [d], "its accept record matches, but it no longer passes acceptance on the "
                                f"current tree ({'; '.join(probs[:2])}{' ...' if len(probs) > 2 else ''})"))
                continue
            if not have:
                why = "it has no accept event and is not in the legacy boundary"
            elif not any(f" {ACCEPT_FORMAT}:" in h for h in have):
                why = (f"its accept record predates the {ACCEPT_FORMAT} acceptance identity (R04): re-accept it on the "
                       "current tree")
            else:
                why = ("its accept record is stale: the claim, its provenance, inputs or cited artifacts (evidence, "
                       "council reviews, frozen manifest) changed after acceptance")
            out.append((d, path + [d], why))
    return out


# ---------------------------------------------------------------- consumed claims: validity and conditions
def claim_names(cid: str, by: dict, aliases: dict) -> list[str]:
    """Ways a claim can be named in text: its id, its aliases, its name (if >= 4 characters)."""
    nm = (by.get(cid) or {}).get("name", "")
    return [cid] + [a for a, t in aliases.items() if t == cid] + ([nm] if len(nm) >= 4 else [])


def name_hit(text: str, names) -> str | None:
    """The first name occurring in text as a whole token (whitespace-normalised), or None."""
    t = re.sub(r"\s+", " ", text or "")
    return next((n for n in names if n and re.search(
        r"(?<![\w-])" + re.escape(re.sub(r"\s+", " ", n)) + r"(?![\w-])", t)), None)


def conditional_on(status: str, names) -> str | None:
    """R06: the status text says `conditional on <one of names>` (the name inside the clause that follows
    'conditional on', up to ';' or the end)."""
    s = status or ""
    want = {re.sub(r"\s+", " ", n).strip().lower(): n for n in names if n}
    for m in re.finditer(r"(?<![\w-])conditional on\b", s, re.I):
        if re.search(r"\b(not|no longer|never|without)\s*$", s[:m.start()], re.I):
            continue  # "not conditional on X" is the opposite claim
        # the clause: up to the end of the sentence ('. ' / end), ';' or a closing ')'; a list of condition names
        clause = re.split(r"\.(?:\s|$)|;|\)", s[m.end():], maxsplit=1)[0]
        for item in re.split(r",|\band\b|&", clause):
            item = re.sub(r"\s*\(.*$", "", item)  # "Lemma W (see §3" -> "Lemma W"
            item = re.sub(r"\s+", " ", item).strip(" \t:`*_\"'").lower()
            if item in want:  # the COMPLETE name: "Lemma Weak Extra" is not "Lemma Weak"
                return want[item]
    return None


def weak_or_invalid(dr: dict) -> bool:
    """An @hyp input needs the conditional-result treatment if it is below checked assurance or not ACTIVE."""
    s = status_strength(dr.get("status", ""))
    return (s != 3 and s != "NEG") or dr.get("state") != "ACTIVE"


def invalid_inputs(cid: str, by: dict, g, aliases: dict) -> list[tuple[str, list[str], str]]:
    """F1: consumed claims that are not ACTIVE -> [(id, path, why)]. Every claim reached from cid through edges that
    are not @hyp-only (stmt / proof / bound bridges, transitively), plus each DIRECT @hyp input that is not ACTIVE
    unless cid's status is `conditional on` it. Status text and acks never waive this."""
    out, seen, q = [], {cid}, deque([(cid, [cid])])
    st = by[cid].get("status", "")
    while q:
        u, path = q.popleft()
        for d in g.deps.get(u, []):
            if g.uses[(u, d)] == {"hyp"}:
                if u == cid and by[d]["state"] != "ACTIVE" and not conditional_on(st, claim_names(d, by, aliases)):
                    out.append((d, path + [d], f"{by[d]['state']} (@hyp, but the status is not 'conditional on' it)"))
                continue
            if d in seen:
                continue
            seen.add(d)
            if by[d]["state"] != "ACTIVE":
                out.append((d, path + [d], by[d]["state"]))
            q.append((d, path + [d]))
    return out


def conditions(cid: str, by: dict, g, _memo=None, _stack=None) -> dict[str, list[str]]:
    """R06: the conditions a claim's truth rests on -> {condition id: path}. A direct @hyp input that is weak or not
    ACTIVE is a condition; conditions of inputs used through stmt / proof edges are inherited (transitively). A claim
    used @hyp is assumed wholesale, so its own conditions are not inherited."""
    memo = {} if _memo is None else _memo
    stack = set() if _stack is None else _stack
    if cid in memo:
        return memo[cid]
    stack.add(cid)
    res = {}
    for d in g.deps.get(cid, []):
        if g.uses[(cid, d)] == {"hyp"}:
            if weak_or_invalid(by[d]):
                res.setdefault(d, [cid, d])
        elif d not in stack:
            for w, p in conditions(d, by, g, memo, stack).items():
                res.setdefault(w, [cid] + p)
    stack.discard(cid)
    memo[cid] = res
    return res


def consumers(cid: str, g) -> dict[str, list[str]]:
    """Transitive dependents of cid through edges that are not @hyp-only -> {id: path} (they inherit its
    conditions)."""
    paths, q = {cid: [cid]}, deque([cid])
    while q:
        u = q.popleft()
        for v in sorted(g.rdeps.get(u, [])):
            if v not in paths and g.uses[(v, u)] != {"hyp"}:
                paths[v] = paths[u] + [v]
                q.append(v)
    paths.pop(cid)
    return paths


def read_tsv_text(text: str) -> list[dict]:
    lines = (text or "").splitlines()
    if not lines:
        return []
    header = lines[0].split("\t")
    out = []
    for ln in lines[1:]:
        if not ln.strip() or ln.startswith("#"):
            continue
        cells = ln.split("\t")
        cells += [""] * (len(header) - len(cells))
        out.append(dict(zip(header, cells)))
    return out


if __name__ == "__main__":
    import argparse
    _ap = argparse.ArgumentParser(description="bvsreg.py recover [--dry-run]: roll back an unfinished transaction "
                                  "(journal registry/.TXN_INPROGRESS, or lock registry/.TXN_FAILED), then remove the "
                                  "journal / lock (restartable). bvsreg.py legacy-boundary [--tag T]: write the frozen "
                                  "legacy acceptance boundary INFRA/LEGACY_ACCEPTED.tsv once, from tag theory-v2.0-pre (R03-N1)")
    _ap.add_argument("cmd", choices=["recover", "legacy-boundary"])
    _ap.add_argument("--dry-run", action="store_true")
    _a = _ap.parse_args()
    if _a.cmd == "legacy-boundary":
        txn_guard()
        sys.exit(write_legacy_boundary())
    sys.exit(recover(_a.dry_run))
