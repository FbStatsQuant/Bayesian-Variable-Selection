"""Citation check for the Wave-1C consistency chapter.

Scans consistency.tex and sections/*.tex for
  \\srcq{path:lines}{token}  -> file exists, lines exist, token occurs (whitespace-normalised) in the cited lines
  \\src{path:lines} / \\src{path} -> file exists, lines exist
  \\path{...} (repo-relative or aliased paths only) -> file or directory exists
Writes CITECHECK.txt next to this script. Usage: python -I citecheck.py
"""
import os
import re
import subprocess
import sys

BRANCH = "8a27652"  # C-ENG head cited by the chapter (origin/w1c/ls0-merge has since advanced)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ALIASES = {
    "W1C/": "Theory_work/Wave1C/",
    "W1/": "Theory_work/Wave1/",
    "SoP/": "Theory_work/State_of_Project/sections/",
    "CORE/": "Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/",
    "PROD/": "Scripts/SMC_BVS/core/",
    "NBH/": "Theory_work/Old_Projects/New_BVS_Headquarters/",
}


def expand(p):
    for k, v in ALIASES.items():
        if p.startswith(k):
            return v + p[len(k):]
    return p


def norm(s):
    s = s.replace("\\$", "$").replace("\\_", "_").replace("\\%", "%").replace("\\&", "&")
    return re.sub(r"\s+", " ", s).strip()


def parse_lines(spec):
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.append((int(a), int(b)))
        else:
            out.append((int(part), int(part)))
    return out


def balanced(text, i):
    """text[i] == '{'; return (content, index after closing brace)."""
    depth = 0
    j = i
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j + 1
        j += 1
    raise ValueError("unbalanced")


def main():
    files = [os.path.join(HERE, "consistency.tex")]
    sd = os.path.join(HERE, "sections")
    files += [os.path.join(sd, f) for f in sorted(os.listdir(sd)) if f.endswith(".tex")]
    rows, bad = [], 0
    for fn in files:
        text = open(fn, encoding="utf-8").read()
        rel = os.path.relpath(fn, HERE)
        for m in re.finditer(r"\\(srcq|src|path)\{", text):
            kind = m.group(1)
            if text[max(0, m.start() - 12):m.start()].endswith("newcommand{"):
                continue
            arg, nxt = balanced(text, m.end() - 1)
            token = None
            if kind == "srcq":
                token, _ = balanced(text, nxt)
            lineno = text.count("\n", 0, m.start()) + 1
            if kind == "srcq" and "#" in arg:
                continue  # macro definition
            ref = arg.strip()
            if kind == "path":
                if not any(ref.startswith(k) for k in ALIASES) and not ref.startswith(("Theory_work/", "Scripts/", "BR/")):
                    continue  # bare file names next to an earlier full path
                path, spec = ref.rstrip("/"), None
            else:
                mm = re.match(r"^(.*?):([0-9,\- ]+)$", ref)
                path, spec = (mm.group(1), mm.group(2)) if mm else (ref, None)
            status, note = "OK", ""
            if path.startswith("BR/"):
                # read-only: the file as committed on branch origin/w1c/ls0-merge
                r = subprocess.run(["git", "-C", ROOT, "show", BRANCH + ":" + path[3:]], capture_output=True)
                exists = r.returncode == 0
                content = r.stdout.decode("utf-8", errors="replace") if exists else ""
            else:
                full = os.path.join(ROOT, expand(path))
                exists = os.path.exists(full)
                content = open(full, encoding="utf-8", errors="replace").read() if exists and os.path.isfile(full) else ""
            if not exists:
                status, note = "MISSING-FILE", expand(path)
            elif spec is not None:
                lines = content.split("\n")
                rngs = parse_lines(spec)
                if any(a < 1 or b > len(lines) or a > b for a, b in rngs):
                    status, note = "BAD-LINES", f"file has {len(lines)} lines"
                elif token is not None:
                    seg = norm(" ".join(" ".join(lines[a - 1:b]) for a, b in rngs))
                    if norm(token) not in seg:
                        status = "TOKEN-MISS"
                        # locate the token elsewhere in the file to help fixing
                        hits = [i + 1 for i, l in enumerate(lines) if norm(token) in norm(l)]
                        note = f"token '{token}' not in {spec}; found at lines {hits[:8]}"
            if status != "OK":
                bad += 1
            rows.append(f"{status:13s} {rel}:{lineno}  \\{kind}{{{ref}}}" + (f"  [{token}]" if token else "") + (f"  -- {note}" if note else ""))
    out = os.path.join(HERE, "CITECHECK.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"citecheck.py: {len(rows)} citations checked, {bad} problems\n")
        f.write("\n".join(rows) + "\n")
    print(f"{len(rows)} citations, {bad} problems -> {out}")
    for r in rows:
        if not r.startswith("OK"):
            print(r)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
