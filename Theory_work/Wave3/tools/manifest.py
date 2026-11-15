"""manifest.py: freeze and verify the content a review round covers, and bind the council's OUTCOME to it
(Wave 3 resume rule 15; findings R01, R02-reconciliation R01, R03-reconciliation N2).

  python manifest.py freeze TICKET_DIR OUT.txt [--extra LIST.txt]   # sha256 of every reviewed input
  python manifest.py verify TICKET_DIR OUT.txt                      # exit 1 on any change or a corrupted header
  python manifest.py bind   OUT.txt REVIEW.md [REVIEW.md ...] [--council "<council cell>"]
                                                                    # exit 1 unless every review gives ONE PASS
                                                                    # verdict line for OUT's digest

Covered: every file in TICKET_DIR except reviews/, LOG.md, CHECKPOINT_*.md and __pycache__/, plus every
repo-relative path listed in LIST.txt (one per line; '#' comments allowed): the external inputs the proof relies on
(premise sources, inherited proof files, code pinned by the claims). An extra entry may be a file or a directory.
The first line of OUT is `MANIFEST <digest>`, where digest = sha256 of the sorted per-file lines. `verify` recomputes it
from the stored rows (a corrupted or hand-edited header fails) and from the current files. Name the round's manifest
`TICKET_DIR/reviews/MANIFEST_<round>.txt`: CP3 acceptance looks for the council digest there and verifies it.

Line endings (INFRA R06). A text file is the same input on an LF and on a CRLF checkout. A file is EOL-normalisable
iff it contains no NUL byte and every CR in it is the first half of a CRLF pair. For such a file `freeze` records the
sha256 of its LF-normalised content (every CRLF -> LF) and `verify` accepts a recorded hash equal to the sha256 of its
raw bytes, of its LF-normalised content or of its CRLF-ised content (LF-normalised, then every LF -> CRLF), so manifests
frozen before R06 (raw bytes of a mixed LF/CRLF tree) verify on any uniform checkout. Any other file (a NUL byte:
binary; a lone CR, e.g. CR CR LF) is hashed raw only, on freeze and on verify, so no variant of it can match another
content (Sol R06FIX F1). Any byte change beyond a CRLF <-> LF conversion still fails.

Council verdict line (LIFECYCLE §4.1). Every council review file contains, on a line of its own (optionally wrapped
in backticks), exactly once:
    COUNCIL-VERDICT round=R<k> manifest=<64-hex digest> seat=<seat> score=<x.y> gates=PASS|FAIL
A mention of the digest anywhere else in the review is NOT a verdict. `bind` requires, for each review: exactly one
verdict line for OUT's digest, with gates=PASS and 8.0 <= score <= 10; no other COUNCIL-VERDICT line (a verdict for
another digest or round in the same file is a contradiction; a malformed one is an error); across the reviews one
round and distinct seats. It prints the council cell those verdicts make (paste it into the registry `council`
field); with --council it also requires that cell to match them (round, digest, and per seat: score, PASS, file).
"""
import hashlib, os, re, subprocess, sys
sys.dont_write_bytecode = True
SKIP_DIRS = {"reviews", "__pycache__", ".git"}
COUNCIL_MIN = 8.0
VERDICT = re.compile(r"COUNCIL-VERDICT round=R(\d+) manifest=([0-9a-f]{64}) seat=([A-Za-z][\w.-]*) "
                     r"score=(\d+(?:\.\d+)?) gates=(PASS|FAIL)")


class ManifestError(Exception):
    """A manifest that cannot be read or verified (library use: bvsreg / check.py --acceptance)."""


def repo_root(start):
    out = subprocess.run(["git", "-C", start, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if out.returncode != 0:
        raise ManifestError("manifest: not inside a git repository")
    return out.stdout.strip()


def _h(data):
    return hashlib.sha256(data).hexdigest()


def eol_text(data):
    """INFRA R06: EOL-normalisable text = no NUL byte and every CR is the first half of a CRLF pair. Only such a file
    is line-ending normalised; a binary file (NUL) or one with a lone CR is hashed raw only (Sol R06FIX F1: CR CR LF
    normalised to CR LF would otherwise match the raw hash of a different file)."""
    return b"\0" not in data and data.count(b"\r") == data.count(b"\r\n")


def lf_normalised(data):
    """Every CRLF pair -> LF for EOL-normalisable text; any other content unchanged."""
    return data.replace(b"\r\n", b"\n") if eol_text(data) else data


def sha(p):
    """What `freeze` records for a file: sha256 of its LF-normalised content (raw bytes unless EOL-normalisable)."""
    return _h(lf_normalised(open(p, "rb").read()))


def accepted_hashes(p):
    """The hashes `verify` accepts for an unchanged file: of its raw bytes, LF-normalised and CRLF-ised content
    (EOL-normalisable text); of its raw bytes only (anything else)."""
    data = open(p, "rb").read()
    if not eol_text(data):
        return {_h(data)}
    lf = data.replace(b"\r\n", b"\n")
    return {_h(data), _h(lf), _h(lf.replace(b"\n", b"\r\n"))}


def ticket_files(root):
    """[(path, manifest name)] of the covered files of the ticket folder."""
    out = []
    for d, dirs, files in os.walk(root):
        rel_d = os.path.relpath(d, root)
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        if rel_d != "." and rel_d.replace(os.sep, "/").split("/")[0] in SKIP_DIRS:
            continue
        for f in sorted(files):
            if f == "LOG.md" or (f.startswith("CHECKPOINT_") and f.endswith(".md")):
                continue
            p = os.path.join(d, f)
            out.append((p, os.path.relpath(p, root).replace(os.sep, "/")))
    return out


def ticket_entries(root):
    return [f"{sha(p)}  {name}" for p, name in ticket_files(root)]


def extra_paths(listfile):
    paths = []
    for line in open(listfile, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if line:
            paths.append(line.replace("\\", "/"))
    return paths


def extra_files(repo, paths):
    """[(path, manifest name `EXT:<repo path>`)] of the listed external inputs (a directory: every file under it)."""
    out = []
    for rel in paths:
        p = os.path.join(repo, rel)
        if os.path.isdir(p):
            for d, dirs, files in os.walk(p):
                dirs[:] = sorted(x for x in dirs if x not in {"__pycache__", ".git"})
                for f in sorted(files):
                    q = os.path.join(d, f)
                    out.append((q, f"EXT:{os.path.relpath(q, repo).replace(os.sep, '/')}"))
        elif os.path.isfile(p):
            out.append((p, f"EXT:{rel}"))
        else:
            raise ManifestError(f"manifest: extra input not found: {rel}")
    return out


def extra_entries(repo, paths):
    return [f"{sha(p)}  {name}" for p, name in extra_files(repo, paths)]


def digest(lines):
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def read_manifest(path):
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as e:
        raise ManifestError(f"manifest: {path}: {e}")
    if not lines or not re.fullmatch(r"MANIFEST [0-9a-f]{64}", lines[0]):
        raise ManifestError(f"manifest: {path}: missing or malformed header")
    extras = [l[len("#EXTRA "):] for l in lines[1:] if l.startswith("#EXTRA ")]
    rows = [l for l in lines[1:] if l and not l.startswith("#")]
    return lines[0].split()[1], extras, rows


def verify_problems(root, out, repo=None):
    """`verify` as a library call -> (digest, [differences]); [] = the manifest matches the current tree.
    Raises ManifestError for an unreadable / malformed manifest."""
    dg, extras, rows = read_manifest(out)
    if digest(rows) != dg:
        return dg, ["header digest does not match the stored rows (corrupted or hand-edited manifest)"]
    try:
        cur = ticket_files(root) + extra_files(repo or repo_root(root), extras)
    except ManifestError as e:
        return dg, [str(e)]
    old_files = {l[66:]: l[:64] for l in rows}
    new_files = {name: p for p, name in cur}
    # INFRA R06: a recorded hash matches if it is the raw, LF-normalised or CRLF-ised hash of the current file
    return dg, sorted([f"CHANGED {k}" for k in old_files if k in new_files
                       and old_files[k] not in accepted_hashes(new_files[k])]
                      + [f"REMOVED {k}" for k in old_files if k not in new_files]
                      + [f"ADDED {k}" for k in new_files if k not in old_files])


# ---------------------------------------------------------------- council verdict lines (R03-N2)
def verdict_lines(text):
    """Every line naming COUNCIL-VERDICT -> ([(round, digest, seat, score, gates)], [malformed lines]). A verdict
    line is the whole line (optionally in backticks); COUNCIL-VERDICT inside prose is malformed, never ignored."""
    ok, bad = [], []
    for ln in (text or "").splitlines():
        if "COUNCIL-VERDICT" not in ln:
            continue
        t = ln.strip()
        if len(t) >= 2 and t[0] == "`" and t[-1] == "`":
            t = t[1:-1].strip()
        m = VERDICT.fullmatch(t)
        if m:
            ok.append((int(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5)))
        else:
            bad.append(ln.strip()[:120])
    return ok, bad


def verdict_problems(text, dg, rnd=None, seat=None, score=None):
    """The ONE verdict a council review gives on manifest `dg` -> (verdict or None, [problems]). rnd (int), seat and
    score are the council cell's values to match (None: not compared). Problems: a malformed verdict line; zero or
    several verdict lines for dg; any verdict line for another digest (contradictory: one review file = one round on
    one manifest); gates=FAIL; a score outside [8.0, 10]; a round / seat / score that differs from the cell."""
    ok, bad = verdict_lines(text)
    probs = [f"malformed COUNCIL-VERDICT line {b!r} (expected exactly: COUNCIL-VERDICT round=R<k> "
             "manifest=<64-hex> seat=<seat> score=<x.y> gates=PASS|FAIL)" for b in bad]
    mine = [v for v in ok if v[1] == dg]
    if not mine:
        probs.append(f"no COUNCIL-VERDICT line for MANIFEST {dg[:12]}... (a mention of the digest is not a verdict)")
    elif len(mine) > 1:
        probs.append(f"{len(mine)} COUNCIL-VERDICT lines for MANIFEST {dg[:12]}... (exactly one)")
    for v in ok:
        if v[1] != dg:
            probs.append(f"contradictory COUNCIL-VERDICT line for another manifest {v[1][:12]}... (R{v[0]}, seat "
                         f"{v[2]}, gates={v[4]}): a council review file gives one verdict, on one manifest")
    v = mine[0] if len(mine) == 1 else None
    if v:
        r_, _, s_, sc_, g_ = v
        if g_ != "PASS":
            probs.append(f"verdict gates={g_} (not all gates PASS)")
        if not COUNCIL_MIN <= float(sc_) <= 10:
            probs.append(f"verdict score {sc_} not in [{COUNCIL_MIN}, 10]")
        if rnd is not None and r_ != int(rnd):
            probs.append(f"verdict round R{r_} differs from the council record's R{rnd}")
        if seat is not None and s_.lower() != str(seat).lower():
            probs.append(f"verdict seat {s_!r} differs from the council record's seat {seat!r}")
        if score is not None and float(sc_) != float(score):
            probs.append(f"verdict score {sc_} differs from the council record's {score}")
    return v, probs


_C_SEAT = re.compile(r"^([A-Za-z][\w.-]*)=(\d+(?:\.\d+)?) (PASS|FAIL)\((.+)\)$")


def parse_cell(cell):
    """A council cell `R<k>; MANIFEST <hex>; seat=score PASS(file); ...` -> (round, digest, [(seat, score, res,
    file)], [unparsable entries])."""
    rnd, dg, seats, bad = None, None, [], []
    for e in [x.strip() for x in (cell or "").split(";") if x.strip()]:
        if re.fullmatch(r"R(\d+)", e):
            rnd = int(e[1:]) if rnd is None else -1
        elif re.fullmatch(r"MANIFEST [0-9a-f]{64}", e):
            dg = e.split()[1] if dg is None else "several"
        elif _C_SEAT.match(e):
            seats.append(_C_SEAT.match(e).groups())
        else:
            bad.append(e)
    return rnd, dg, seats, bad


def _same_file(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def bind(man_path, reviews, cell=None):
    """-> (council cell or None, [problems])."""
    dg, _, rows = read_manifest(man_path)
    if digest(rows) != dg:
        return None, [f"header digest does not match the stored rows of {man_path} (corrupted manifest)"]
    tdir = os.path.dirname(os.path.dirname(os.path.abspath(man_path)))  # <ticket>/reviews/MANIFEST_*.txt
    probs, got = [], []
    for r in reviews:
        try:
            text = open(r, encoding="utf-8", errors="replace").read()
        except OSError as e:
            probs.append(f"{r}: {e}")
            continue
        v, ps = verdict_problems(text, dg)
        probs += [f"{r}: {p}" for p in ps]
        if v:
            got.append((r, v))
    if len({v[0] for _, v in got}) > 1:
        probs.append(f"verdicts from different rounds: {sorted({v[0] for _, v in got})}")
    seats = [v[2].lower() for _, v in got]
    if len(set(seats)) != len(seats):
        probs.append(f"two reviews give the same seat: {seats}")
    files = [os.path.normcase(os.path.realpath(r)) for r, _ in got]
    if len(set(files)) != len(files):
        probs.append("the same review file is given twice")
    if cell is not None:
        c_rnd, c_dg, c_seats, c_bad = parse_cell(cell)
        probs += [f"--council: unparsable entry {b!r}" for b in c_bad]
        if c_dg != dg:
            probs.append(f"--council: MANIFEST {c_dg} is not this manifest's digest {dg}")
        if got and c_rnd != got[0][1][0]:
            probs.append(f"--council: round R{c_rnd} differs from the verdicts' R{got[0][1][0]}")
        by_seat = {s.lower(): (s, sc, res, f) for s, sc, res, f in c_seats}
        if len(by_seat) != len(c_seats):
            probs.append("--council: the same seat twice")
        for r, v in got:
            c = by_seat.get(v[2].lower())
            if c is None:
                probs.append(f"--council: no seat {v[2]} (review {r})")
                continue
            if c[2] != "PASS" or float(c[1]) != float(v[3]):
                probs.append(f"--council: seat {c[0]}={c[1]} {c[2]} differs from the verdict score={v[3]} "
                             f"gates={v[4]} in {r}")
            if not any(_same_file(os.path.join(b, c[3]), r) for b in (tdir, os.getcwd())):
                probs.append(f"--council: seat {c[0]} names review {c[3]}, not {r}")
        for s in set(by_seat) - {v[2].lower() for _, v in got}:
            probs.append(f"--council: seat {by_seat[s][0]} has no review among the arguments")
    if probs or not got:
        return None, probs or ["no review given"]

    def rel(r):
        p = os.path.relpath(os.path.abspath(r), tdir).replace(os.sep, "/")
        return r.replace(os.sep, "/") if p.startswith("../") else p
    return (f"R{got[0][1][0]}; MANIFEST {dg}; "
            + "; ".join(f"{v[2]}={v[3]} PASS({rel(r)})" for r, v in got)), []


def txn_guard():
    """CLI only (R03-N4, Sol toolfix3 N4.a): refuse while a registry transaction is unfinished, like every INFRA tool
    (registry/.TXN_INPROGRESS or .TXN_FAILED; run `bvsreg.py recover`). The library functions stay usable."""
    here = os.path.dirname(os.path.abspath(__file__))
    regs = [os.path.join(here, "..", "..", "INFRA", "registry")]
    if os.environ.get("BVS_STAGE_INFRA"):
        regs.append(os.path.join(os.environ["BVS_STAGE_INFRA"], "registry"))
    for reg in regs:
        for f in (".TXN_INPROGRESS", ".TXN_FAILED"):
            p = os.path.normpath(os.path.join(reg, f))
            if os.path.exists(p):
                sys.exit(f"REGISTRY LOCKED: {p} exists (an unfinished registry transaction). Run `python "
                         "Theory_work/INFRA/tools/bvsreg.py recover`, then check.py, then re-run this command.")


def main():
    txn_guard()
    a = sys.argv[1:]
    if not a or a[0] not in ("freeze", "verify", "bind"):
        print(__doc__); sys.exit(2)
    cmd = a[0]
    try:
        if cmd == "bind":
            args, cell = a[1:], None
            if "--council" in args:
                i = args.index("--council")
                if i + 1 >= len(args):
                    print(__doc__); sys.exit(2)
                cell = args[i + 1]
                del args[i:i + 2]
            if len(args) < 2:
                print(__doc__); sys.exit(2)
            got, probs = bind(args[0], args[1:], cell)
            if probs:
                print("\n".join(f"NOT BOUND {p}" for p in probs))
                print(f"bind: REFUSED ({len(probs)} problem(s)); every council review needs exactly one line "
                      "`COUNCIL-VERDICT round=R<k> manifest=<digest> seat=<seat> score=<x.y> gates=PASS`")
                sys.exit(1)
            print(f"bind: OK, {len(args) - 1} review(s) give a PASS verdict (>= {COUNCIL_MIN}) on "
                  f"MANIFEST {read_manifest(args[0])[0]}\ncouncil cell: {got}")
            return
        if len(a) not in (3, 5) or (len(a) == 5 and a[3] != "--extra"):
            print(__doc__); sys.exit(2)
        root, out = a[1], a[2]
        repo = repo_root(root)
        if cmd == "freeze":
            paths = extra_paths(a[4]) if len(a) == 5 else []
            cur = ticket_entries(root) + extra_entries(repo, paths)
            with open(out, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(f"MANIFEST {digest(cur)}\n" + "".join(f"#EXTRA {p}\n" for p in paths) + "\n".join(cur) + "\n")
            print(f"MANIFEST {digest(cur)} ({len(cur)} files, {len(paths)} extra input(s))"); return
        dg, diffs = verify_problems(root, out, repo)
        if diffs:
            print("\n".join(diffs)); print(f"verify: {len(diffs)} difference(s) vs MANIFEST {dg}"); sys.exit(1)
        print(f"verify: OK MANIFEST {dg}")
    except ManifestError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
