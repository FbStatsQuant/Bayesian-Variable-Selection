"""manifest.py: freeze and verify the content a review round covers (Wave 3 resume rule 15, review finding R01).

  python manifest.py freeze  TICKET_DIR OUT.txt    # write sha256 of every reviewed file
  python manifest.py verify  TICKET_DIR OUT.txt    # exit 1 and list changes if anything differs

Covered: every file in TICKET_DIR except reviews/, LOG.md, CHECKPOINT_*.md and __pycache__/. The first line of OUT is
the manifest digest (sha256 of the sorted per-file lines); each reviewer quotes it in their reply.
"""
import hashlib, os, sys
sys.dont_write_bytecode = True
SKIP_DIRS = {"reviews", "__pycache__", ".git"}
def entries(root):
    out = []
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and os.path.relpath(os.path.join(d, x), root) not in SKIP_DIRS)
        for f in sorted(files):
            if f == "LOG.md" or (f.startswith("CHECKPOINT_") and f.endswith(".md")):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if rel.split("/")[0] in SKIP_DIRS:
                continue
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            out.append(f"{h}  {rel}")
    return out
def digest(lines):
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()
def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("freeze", "verify"):
        print(__doc__); sys.exit(2)
    cmd, root, out = sys.argv[1:]
    cur = entries(root)
    if cmd == "freeze":
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(f"MANIFEST {digest(cur)}\n" + "\n".join(cur) + "\n")
        print(f"MANIFEST {digest(cur)} ({len(cur)} files)"); return
    old = open(out, encoding="utf-8").read().splitlines()
    old_files = {l[66:]: l[:64] for l in old[1:] if l}
    new_files = {l[66:]: l[:64] for l in cur}
    diffs = sorted([f"CHANGED {k}" for k in old_files if k in new_files and old_files[k] != new_files[k]]
                   + [f"REMOVED {k}" for k in old_files if k not in new_files]
                   + [f"ADDED {k}" for k in new_files if k not in old_files])
    if diffs:
        print("\n".join(diffs)); print(f"verify: {len(diffs)} difference(s) vs {old[0]}"); sys.exit(1)
    print(f"verify: OK {old[0]}")
if __name__ == "__main__":
    main()
