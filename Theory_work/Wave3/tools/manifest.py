"""manifest.py: freeze and verify the content a review round covers (Wave 3 resume rule 15; findings R01, R02-reconciliation R01).

  python manifest.py freeze TICKET_DIR OUT.txt [--extra LIST.txt]   # sha256 of every reviewed input
  python manifest.py verify TICKET_DIR OUT.txt                      # exit 1 on any change or a corrupted header
  python manifest.py bind   OUT.txt REVIEW.md [REVIEW.md ...]       # exit 1 unless every review quotes the digest

Covered: every file in TICKET_DIR except reviews/, LOG.md, CHECKPOINT_*.md and __pycache__/, plus every
repo-relative path listed in LIST.txt (one per line; '#' comments allowed): the external inputs the proof relies on
(premise sources, inherited proof files, code pinned by the claims). An extra entry may be a file or a directory.
The first line of OUT is `MANIFEST <digest>`, where digest = sha256 of the sorted per-file lines. `verify` recomputes it
from the stored rows (a corrupted or hand-edited header fails) and from the current files.
"""
import hashlib, os, re, subprocess, sys
sys.dont_write_bytecode = True
SKIP_DIRS = {"reviews", "__pycache__", ".git"}


def repo_root(start):
    out = subprocess.run(["git", "-C", start, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("manifest: not inside a git repository")
    return out.stdout.strip()


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def ticket_entries(root):
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
            out.append(f"{sha(p)}  {os.path.relpath(p, root).replace(os.sep, '/')}")
    return out


def extra_paths(listfile):
    paths = []
    for line in open(listfile, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if line:
            paths.append(line.replace("\\", "/"))
    return paths


def extra_entries(repo, paths):
    out = []
    for rel in paths:
        p = os.path.join(repo, rel)
        if os.path.isdir(p):
            for d, dirs, files in os.walk(p):
                dirs[:] = sorted(x for x in dirs if x not in {"__pycache__", ".git"})
                for f in sorted(files):
                    q = os.path.join(d, f)
                    out.append(f"{sha(q)}  EXT:{os.path.relpath(q, repo).replace(os.sep, '/')}")
        elif os.path.isfile(p):
            out.append(f"{sha(p)}  EXT:{rel}")
        else:
            sys.exit(f"manifest: extra input not found: {rel}")
    return out


def digest(lines):
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def read_manifest(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    if not lines or not re.fullmatch(r"MANIFEST [0-9a-f]{64}", lines[0]):
        sys.exit(f"manifest: {path}: missing or malformed header")
    extras = [l[len("#EXTRA "):] for l in lines[1:] if l.startswith("#EXTRA ")]
    rows = [l for l in lines[1:] if l and not l.startswith("#")]
    return lines[0].split()[1], extras, rows


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("freeze", "verify", "bind"):
        print(__doc__); sys.exit(2)
    cmd = a[0]
    if cmd == "bind":
        if len(a) < 3:
            print(__doc__); sys.exit(2)
        dg, _, rows = read_manifest(a[1])
        if digest(rows) != dg:
            sys.exit(f"bind: header digest does not match the stored rows of {a[1]} (corrupted manifest)")
        bad = [r for r in a[2:] if dg not in open(r, encoding="utf-8", errors="replace").read()]
        if bad:
            print("\n".join(f"NOT BOUND {r}" for r in bad)); print(f"bind: {len(bad)} review(s) do not quote {dg}"); sys.exit(1)
        print(f"bind: OK, {len(a) - 2} review(s) quote MANIFEST {dg}"); return
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
    dg, extras, rows = read_manifest(out)
    if digest(rows) != dg:
        print(f"verify: header digest does not match the stored rows (corrupted or hand-edited manifest)"); sys.exit(1)
    cur = ticket_entries(root) + extra_entries(repo, extras)
    old_files = {l[66:]: l[:64] for l in rows}
    new_files = {l[66:]: l[:64] for l in cur}
    diffs = sorted([f"CHANGED {k}" for k in old_files if k in new_files and old_files[k] != new_files[k]]
                   + [f"REMOVED {k}" for k in old_files if k not in new_files]
                   + [f"ADDED {k}" for k in new_files if k not in old_files])
    if diffs:
        print("\n".join(diffs)); print(f"verify: {len(diffs)} difference(s) vs MANIFEST {dg}"); sys.exit(1)
    print(f"verify: OK MANIFEST {dg}")


if __name__ == "__main__":
    main()
