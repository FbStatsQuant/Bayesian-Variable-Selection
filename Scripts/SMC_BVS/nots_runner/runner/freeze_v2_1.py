"""Freeze the v2.1 snapshot: SHA256SUMS + manifest.json + tarball (standard library only).

Usage: python -I freeze_v2_1.py SNAPSHOT_DIR V2_SNAPSHOT_DIR ARCHIVE_PATH
Checks that every code/core file is byte-identical to v2 and lists every file that changed.
"""
import hashlib
import json
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

snap, v2, archive = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
skip = {"SHA256SUMS", "manifest.json"}
files = sorted(p.relative_to(snap).as_posix() for p in snap.rglob("*")
               if p.is_file() and p.relative_to(snap).as_posix() not in skip and ".cpp_cache" not in p.parts)
v2_files = {line.split("  ", 1)[1]: line.split("  ", 1)[0]
            for line in (v2 / "SHA256SUMS").read_text().splitlines()}
for f in files:   # an edit must not change a file's line-ending convention (v2 bytes are the reference)
    if sha(snap / f) != v2_files.get(f) and (b"\r\n" in (snap / f).read_bytes()) != (b"\r\n" in (v2 / f).read_bytes()):
        raise SystemExit("line-ending convention changed in " + f)
core = [f for f in files if f.startswith("code/core/")]
assert core and all(f in v2_files and sha(snap / f) == v2_files[f] for f in core), "core differs from v2"
assert set(files) | {"manifest.json"} == set(v2_files), ("file set differs", (set(files) | {"manifest.json"}) ^ set(v2_files))
changed = [dict(path=f, v2_sha256=v2_files[f], v2_1_sha256=sha(snap / f)) for f in files if sha(snap / f) != v2_files[f]]
manifest = dict(snapshot="v2.1", created_utc=datetime.now(timezone.utc).isoformat(),
                base="A v2 (archive 17bdd21a...e1ff; SHA256SUMS b56100b3...5a)",
                base_SHA256SUMS_sha256=sha(v2 / "SHA256SUMS"), core_identical_to_v2=True,
                changed_files=changed, files=[dict(path=f, sha256=sha(snap / f), bytes=(snap / f).stat().st_size) for f in files])
(snap / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", newline="\n")
listed = sorted(files + ["manifest.json"])
(snap / "SHA256SUMS").write_text("".join("%s  %s\n" % (sha(snap / f), f) for f in listed), newline="\n")
archive.parent.mkdir(parents=True, exist_ok=True)
with tarfile.open(archive, "w:gz", format=tarfile.PAX_FORMAT) as tar:
    for f in ["SHA256SUMS", "manifest.json"] + files:
        info = tar.gettarinfo(str(snap / f), arcname="v2_1/" + f)
        info.uid = info.gid = 0; info.uname = info.gname = ""
        info.mode = 0o755 if f.endswith(".sh") else 0o644
        with open(snap / f, "rb") as fh:
            tar.addfile(info, fh)
print("files", len(files), "changed", [c["path"] for c in changed])
print("SHA256SUMS", sha(snap / "SHA256SUMS"), "manifest", sha(snap / "manifest.json"), "archive", sha(archive))
