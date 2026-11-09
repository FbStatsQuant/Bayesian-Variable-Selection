"""C-DLV CITECHECK: open every path:line cited in STATEMENT.md, INVENTORY.md, lemmas/*.md, REPORT.md and print the
cited lines (first and last of each range) so each claim can be compared with the text. Usage: python citecheck.py"""
import re, os, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
HERE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORE = os.path.join(ROOT, "Scripts", "SMC_BVS", "core")
SOP = os.path.join(ROOT, "Theory_work", "State_of_Project", "sections")
files = [os.path.join(HERE, f) for f in ("STATEMENT.md", "INVENTORY.md", "REPORT.md", "METHOD_REQUIREMENTS.md")] + \
    sorted(glob.glob(os.path.join(HERE, "lemmas", "*.md")))
pat = re.compile(r"((?:core/)?(?:cpp/)?v3_[a-z_]+\.(?:R|h|cpp)|(?:SoP/)?[0-9A-Za-z_]+\.tex)((?::[0-9]+(?:-[0-9]+)?)(?:,\s*:?[0-9]+(?:-[0-9]+)?)*)")


def resolve(name):
    base = name.replace("core/", "").replace("SoP/", "")
    if base.endswith(".tex"):
        return os.path.join(SOP, base)
    c = os.path.join(CORE, base)
    return c if os.path.exists(c) else os.path.join(CORE, "cpp", base)


out = []; seen = set(); missing = 0
for f in files:
    if not os.path.exists(f):
        continue
    txt = open(f, encoding="utf-8").read()
    for m in pat.finditer(txt):
        name, ranges = m.group(1), m.group(2)
        path = resolve(name)
        for r in re.findall(r"([0-9]+)(?:-([0-9]+))?", ranges):
            a = int(r[0]); b = int(r[1]) if r[1] else a
            key = (path, a, b)
            if key in seen:
                continue
            seen.add(key)
            if not os.path.exists(path):
                out.append(f"MISSING FILE  {name}:{a}-{b}  (cited in {os.path.basename(f)})"); missing += 1; continue
            lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
            if b > len(lines) or a < 1:
                out.append(f"OUT OF RANGE  {name}:{a}-{b} (file has {len(lines)} lines; cited in {os.path.basename(f)})"); missing += 1; continue
            first = lines[a - 1].strip()[:150]; last = lines[b - 1].strip()[:150]
            out.append(f"{name}:{a}-{b}  [{os.path.basename(f)}]\n    L{a}: {first}" + (f"\n    L{b}: {last}" if b != a else ""))
print(f"citations checked: {len(seen)}; missing/out of range: {missing}\n")
print("\n".join(out))
