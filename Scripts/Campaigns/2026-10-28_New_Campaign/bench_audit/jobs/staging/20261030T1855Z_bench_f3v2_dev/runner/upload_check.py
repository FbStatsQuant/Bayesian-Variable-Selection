#!/usr/bin/env python3
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
from frozen import sha

if len(sys.argv) != 3 or not re.fullmatch(r"[0-9a-f]{64}", sys.argv[2]):
    sys.exit("usage: upload_check.py absolute_folder expected_manifest_sha256")
root = Path(sys.argv[1])
manifest = root / "UPLOAD_SHA256.txt"
if not root.is_absolute() or sha(manifest) != sys.argv[2]:
    raise ValueError("upload manifest digest mismatch")
expected = {}
for line in manifest.read_text(encoding="utf-8").splitlines():
    m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
    if not m or m[2] in expected or ".." in Path(m[2]).parts or Path(m[2]).is_absolute():
        raise ValueError("bad upload manifest entry")
    expected[m[2]] = m[1]
if any(p.is_symlink() for p in root.rglob("*")):
    raise ValueError("upload contains symlink")
found = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p != manifest}
if found != set(expected):
    raise ValueError("upload membership mismatch")
for rel in found:
    if sha(root / rel) != expected[rel]:
        raise ValueError("upload hash mismatch " + rel)
print("UPLOAD_OK", len(found))
