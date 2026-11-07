#!/usr/bin/env python3
"""State of Project — consistency and fidelity checks (stdlib only).

Checks
  C1  every \\src{...} path exists (NBH/ prefix expanded) and cited line numbers exist
  C2  every cited file is unchanged since the frozen source commit
  C3  every \\rid{X} resolves to a \\defid / card in the .tex or to a registry row
  C4  every ID is defined at most once in the .tex
  C5  registry status_exact equals the status column of NBH/ID_REGISTRY.md (for archive IDs)
  C6  registry rows are well formed (12 columns, known kind)
  C7  coverage of in-scope archive IDs (Part A all; Part B those cited by NBH/03 and NBH/05)
  C8  LaTeX log: missing glyphs, undefined references/citations (with --log)
  C9  \\todo count
Usage
  python scripts/check.py                      # whole document
  python scripts/check.py --files sections/02_method.tex registry/theory_main.tsv
  python scripts/check.py --log main.log --strict
"""
import argparse, glob, os, re, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(DOC, "..", ".."))
NBH = "Theory_work/Old_Projects/New_BVS_Headquarters/"
FROZEN = "21ebc28"
KINDS = {"main-card", "supp-card", "clause", "remark", "obligation", "future-work", "drop", "limitation",
         "definition", "ruling", "method-decision", "dissent", "cited-lemma", "history-result", "refuted",
         "counterexample", "decision-pending", "engineering", "frontier", "empirical"}
COLS = ["id", "native", "kind", "short", "status_exact", "checked_by", "regime", "depends_on", "used_by",
        "open_items", "tex_label", "sources"]
ARCHIVE_ID = re.compile(r"^(TH|LM|CJ|RF|CE|OB|DR|LIM|DF|RL|MD|DS|CL)\d{2,3}(\.[A-Za-z0-9]+)?$")


def rel(p):
    return os.path.relpath(p, DOC).replace("\\", "/")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def split_md_row(line):
    cells, cur, i = [], "", 0
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "\\|"; i += 2; continue
        if s[i] == "|":
            cells.append(cur.strip()); cur = ""; i += 1; continue
        cur += s[i]; i += 1
    cells.append(cur.strip())
    return cells


def load_id_registry():
    path = os.path.join(REPO, NBH, "ID_REGISTRY.md")
    reg, part = {}, None
    for line in read(path).splitlines():
        if line.startswith("# ID registry A"):
            part = "A"
        elif line.startswith("# ID registry B"):
            part = "B"
        elif line.startswith("## Alias index"):
            part = None
        if part and line.startswith("| "):
            c = split_md_row(line)
            if c and ARCHIVE_ID.match(c[0]) and len(c) >= 5:
                reg[c[0]] = {"part": part, "status": c[4], "native": c[1]}
    return reg


def tex_files(selected):
    if selected:
        return [os.path.join(DOC, f) for f in selected if f.endswith(".tex")]
    return sorted(glob.glob(os.path.join(DOC, "sections", "*.tex")) + glob.glob(os.path.join(DOC, "tables", "*.tex")))


def tsv_files(selected):
    if selected:
        return [os.path.join(DOC, f) for f in selected if f.endswith(".tsv")]
    return sorted(glob.glob(os.path.join(DOC, "registry", "*.tsv")))


SRC_RE = re.compile(r"\\src\{([^{}]*)\}")
STMT_RE = re.compile(r"\\begin\{stmt\}\{([^{}]*)\}")
DEFID_RE = re.compile(r"\\defid\{([^{}]+)\}|\\begin\{card\}\{([^{}]+)\}")
RID_RE = re.compile(r"\\rid\{([^{}]+)\}")


def parse_src(s):
    """'NBH/x.md:12-30' -> (repo-relative path, [(12,30)]) ; 'x.md §3' -> (path, [])"""
    s = s.strip()
    m = re.match(r"^(.*?)(?::([0-9][0-9,\-–\s]*))?(?:\s+(§|sec|lines?).*)?$", s)
    path, lines = m.group(1).strip(), m.group(2)
    path = path.split(" ")[0]
    if path.startswith("NBH/"):
        path = NBH + path[4:]
    spans = []
    if lines:
        for part in re.split(r"[,\s]+", lines.strip()):
            if not part:
                continue
            a = re.split(r"[-–]", part)
            try:
                lo = int(a[0]); hi = int(a[1]) if len(a) > 1 and a[1] else lo
                spans.append((lo, hi))
            except ValueError:
                pass
    return path, spans


_linecount = {}


def nlines(p):
    if p not in _linecount:
        try:
            with open(p, "rb") as f:
                _linecount[p] = f.read().count(b"\n") + 1
        except OSError:
            _linecount[p] = -1
    return _linecount[p]


def git_changed(paths):
    if not paths:
        return set()
    out = subprocess.run(["git", "-C", REPO, "diff", "--name-only", FROZEN, "--"] + sorted(paths),
                         capture_output=True, text=True)
    return set(x.strip() for x in out.stdout.splitlines() if x.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="*", default=None, help="paths relative to the document folder")
    ap.add_argument("--log", default=None)
    ap.add_argument("--strict", action="store_true", help="exit 1 on any error")
    ap.add_argument("--coverage-out", default=os.path.join(DOC, "checks", "coverage_report.txt"))
    a = ap.parse_args()
    errors, warns = [], []
    texs, tsvs = tex_files(a.files), tsv_files(a.files)
    reg = load_id_registry()

    # ---- read tex
    defined, refs, srcs, alltex = Counter(), defaultdict(list), [], ""
    for f in texs:
        t = read(f)
        alltex += t
        t_nc = re.sub(r"(?<!\\)%.*", "", t)
        t_nc = re.sub(r"\\verb(.).*?\1", "", t_nc)  # ignore \verb|...| examples
        for m in DEFID_RE.finditer(t_nc):
            defined[m.group(1) or m.group(2)] += 1
        for m in RID_RE.finditer(t_nc):
            refs[m.group(1)].append(rel(f))
        for m in list(SRC_RE.finditer(t_nc)) + list(STMT_RE.finditer(t_nc)):
            srcs.append((rel(f), m.group(1)))

    # ---- read registry
    rows = []
    for f in tsv_files(None):  # always load all rows for resolution
        lines = read(f).splitlines()
        if not lines:
            continue
        hdr = lines[0].split("\t")
        if hdr != COLS:
            errors.append(f"C6 {rel(f)}: header must be exactly {COLS}")
            continue
        for k, line in enumerate(lines[1:], start=2):
            if not line.strip():
                continue
            c = line.split("\t")
            if len(c) != len(COLS):
                errors.append(f"C6 {rel(f)}:{k}: {len(c)} columns (need {len(COLS)})")
                continue
            r = dict(zip(COLS, c)); r["_file"] = rel(f); r["_line"] = k
            rows.append(r)
    reg_ids = Counter(r["id"] for r in rows)
    selected_tsv = set(rel(f) for f in tsvs)

    # C1/C2 sources
    cited_paths = set()
    for f, s in srcs:
        for piece in s.split(";"):
            if not piece.strip():
                continue
            path, spans = parse_src(piece)
            full = os.path.join(REPO, path)
            if not os.path.exists(full):
                errors.append(f"C1 {f}: source not found: {piece.strip()}")
                continue
            cited_paths.add(path)
            n = nlines(full)
            for lo, hi in spans:
                if lo < 1 or hi < lo or hi > n:
                    errors.append(f"C1 {f}: line span {lo}-{hi} outside {path} ({n} lines)")
    for r in rows:
        if r["_file"] not in selected_tsv:
            continue
        for piece in r["sources"].split(";"):
            if piece.strip():
                path, spans = parse_src(piece)
                if not os.path.exists(os.path.join(REPO, path)):
                    errors.append(f"C1 {r['_file']}:{r['_line']}: source not found: {piece.strip()}")
                else:
                    cited_paths.add(path)
    changed = git_changed(cited_paths)
    for p in sorted(changed):
        errors.append(f"C2 cited file changed since {FROZEN}: {p}")

    # C3/C4 ids
    for i, n in defined.items():
        if n > 1:
            errors.append(f"C4 ID defined {n} times in .tex: {i}")
    full_defined = set(defined)
    if a.files:  # resolution needs whole document
        for f in tex_files(None):
            for m in DEFID_RE.finditer(re.sub(r"(?<!\\)%.*", "", read(f))):
                full_defined.add(m.group(1) or m.group(2))
    for i, where in refs.items():
        if i not in full_defined and i not in reg_ids and i not in reg:
            errors.append(f"C3 \\rid{{{i}}} resolves nowhere (used in {sorted(set(where))})")
        elif i not in full_defined and i not in reg_ids:
            warns.append(f"C3 \\rid{{{i}}} has no \\defid in the .tex (only registry/archive) — used in {sorted(set(where))[:3]}")

    # C5/C6 registry
    for r in rows:
        if r["_file"] not in selected_tsv:
            continue
        where = f"{r['_file']}:{r['_line']}"
        if r["kind"] not in KINDS:
            errors.append(f"C6 {where}: unknown kind '{r['kind']}'")
        if reg_ids[r["id"]] > 1:
            errors.append(f"C6 {where}: duplicate registry id {r['id']}")
        if r["id"] in reg:
            want = reg[r["id"]]["status"]
            if r["status_exact"].replace("\\|", "|") != want.replace("\\|", "|"):
                errors.append(f"C5 {where}: status_exact of {r['id']} differs from NBH/ID_REGISTRY.md")
        if r["tex_label"] and r["tex_label"] not in full_defined:
            warns.append(f"C6 {where}: tex_label {r['tex_label']} not defined in .tex (yet)")

    # C7 coverage
    if not a.files:
        partA = {i for i, v in reg.items() if v["part"] == "A"}
        cited_B = set()
        for doc in ("03_results_and_conclusions.md", "05_open_questions_and_next_steps.md"):
            for m in re.finditer(r"\b(TH|LM|CJ|RF|CE)(1\d\d|[2-9]\d\d)\b", read(os.path.join(REPO, NBH, doc))):
                cited_B.add(m.group(0))
        cited_B &= set(reg)
        present = set(full_defined) | set(reg_ids) | set(refs)
        text_ids = set(re.findall(r"\b(?:TH|LM|CJ|RF|CE|OB|DR|LIM|DF|RL|MD|DS|CL)\d{2,3}(?:\.[A-Za-z0-9]+)?\b", alltex))
        present |= text_ids
        inscope = partA | cited_B
        miss = sorted(inscope - present)
        cov = 100.0 * (len(inscope) - len(miss)) / max(1, len(inscope))
        os.makedirs(os.path.dirname(a.coverage_out), exist_ok=True)
        with open(a.coverage_out, "w", encoding="utf-8") as f:
            f.write(f"in-scope IDs: {len(inscope)} (Part A {len(partA)}, Part B cited by NBH/03,05: {len(cited_B)})\n")
            f.write(f"present: {len(inscope) - len(miss)}  coverage: {cov:.1f}%\nmissing:\n")
            for m_ in miss:
                f.write(f"  {m_}\t{reg[m_]['native'][:90]}\n")
        print(f"C7 coverage {cov:.1f}% ({len(inscope) - len(miss)}/{len(inscope)}); missing list -> {rel(a.coverage_out)}")
        if cov < 98.0:
            warns.append(f"C7 coverage {cov:.1f}% < 98% target")

    # C8 log
    if a.log:
        log = read(a.log) if os.path.exists(a.log) else ""
        miss = re.findall(r"Missing character: There is no (.+?) in font", log)
        if miss:
            errors.append(f"C8 {len(miss)} dropped glyph(s): {sorted(Counter(miss).items())[:15]}")
        und = re.findall(r"(?:Reference|Citation|Hyper reference) `([^']+)' .*undefined", log)
        und += re.findall(r"pdfTeX warning \(dest\): name\{([^}]+)\} has been referenced but does not exist", log)
        und += re.findall(r"name\{([^}]+)\} has been referenced but does not exist", log)
        if und:
            errors.append(f"C8 {len(set(und))} undefined reference(s): {sorted(set(und))[:15]}")
        ovf = len(re.findall(r"Overfull \\hbox", log))
        if ovf:
            warns.append(f"C8 {ovf} overfull hbox warnings")

    # C9 todo
    todos = len(re.findall(r"\\todo\{", re.sub(r"(?<!\\)%.*", "", alltex)))
    if todos:
        warns.append(f"C9 {todos} \\todo item(s) remain")

    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"checked {len(texs)} tex, {len(tsvs)} tsv; {len(srcs)} \\src/stmt refs; {len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if (errors and a.strict) else 0)


if __name__ == "__main__":
    main()
