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


def safe_dest(path: str) -> str:
    """Refuse a write destination unless it resolves strictly inside Theory_work/INFRA and no component from INFRA
    down to the file is a symlink or junction (so a planted link cannot redirect a write outside)."""
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


def replace_all(pairs) -> None:
    """Transaction over prepared files: [(tmp, dest)]. Each existing dest is first copied to dest.bak; then every tmp
    replaces its dest. On ANY failure every completed replacement is undone (from .bak, or removed if dest was new)
    and the exception re-raised; .tmp / .bak files are removed in every case."""
    import shutil
    done, baks, failed = [], [], []
    try:
        for tmp, dest in pairs:
            if os.path.exists(dest):
                bak = safe_dest(dest + ".bak")
                shutil.copyfile(dest, bak)
                baks.append(bak)
        for tmp, dest in pairs:
            existed = os.path.exists(dest)
            os.replace(tmp, dest)
            done.append((dest, existed))
    except BaseException:
        for dest, existed in reversed(done):
            try:
                if existed:
                    os.replace(dest + ".bak", dest)
                else:
                    os.remove(dest)
            except OSError:
                failed.append(dest + ".bak")
                print(f"ROLLBACK FAILED for {dest} (backup {dest}.bak kept)", file=sys.stderr)
        raise
    finally:
        for tmp, _ in pairs:
            if os.path.exists(tmp):
                os.remove(tmp)
        for bak in baks:
            if os.path.exists(bak) and bak not in failed:
                os.remove(bak)


def write_many(items) -> None:
    """All-or-nothing write of several files: [(path, header, rows)] for TSVs or [(path, text)] for raw text (e.g. the
    events log with its new lines). All are written to .tmp siblings first, then replaced as one transaction
    (replace_all): a failure at any point leaves every file as it was."""
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


def claim_hash(row: dict, span=None) -> str | None:
    """sha256 over the statement span plus every premise span (in order). None if any span is unreadable."""
    span = span or parse_span(row.get("lines", ""))
    lines = read_lines(row.get("file", ""))
    if lines is None or span is None or span[1] > len(lines):
        return None
    parts = [lines[span[0] - 1: span[1]]]
    for spec in split_list(row.get("premises", "")):
        pl = span_lines(spec)
        if pl is None:
            return None
        parts.append(["--premise " + spec.rpartition(":")[0] + "--"] + pl)
    return text_hash([l for part in parts for l in part])


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
            shutil.copytree(s, os.path.join(d, f), ignore=shutil.ignore_patterns("fragments", "*.tmp"))
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


def check_findings(stage: str | None = None):
    """Run check.py (on the live registry, or on a staged copy) -> (returncode, {(severity, check, id, message)},
    printed summary line)."""
    import json
    import tempfile
    fd, out = tempfile.mkstemp(suffix=".json", prefix="bvs-check-")
    os.close(fd)
    try:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        env.pop("BVS_STAGE_INFRA", None)
        if stage:
            env["BVS_STAGE_INFRA"] = stage
        p = subprocess.run([sys.executable, os.path.join(TOOLS, "check.py"), "--quiet", "--json", out],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=ROOT)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
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
        if os.path.isfile(os.path.join(sreg, f)) and not f.endswith(".tmp"):
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
