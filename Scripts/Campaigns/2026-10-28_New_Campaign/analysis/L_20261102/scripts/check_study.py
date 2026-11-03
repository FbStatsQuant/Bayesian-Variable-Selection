"""check_study.py STAGED_SHA256 LOCAL_STUDY OUT
Compares every staged file under runs/<RID>/study/ (excluding dev/) with the local sealed study. Writes OUT and prints the verdict."""
import hashlib, os, sys

staged, study, out = sys.argv[1], sys.argv[2], sys.argv[3]
rows, n_ok, bad = [], 0, []
for line in open(staged, encoding="utf-8"):
    h, p = line.strip().split(" ", 1)
    p = p.lstrip("*")
    key = "/study/"
    if key not in p or "/code/" in p:
        continue
    rel = p.split(key, 1)[1]
    if rel.startswith("dev/"):
        continue
    loc = os.path.join(study, rel)
    if not os.path.exists(loc):
        bad.append(("missing", rel)); continue
    d = hashlib.sha256(open(loc, "rb").read()).hexdigest()
    if d == h:
        n_ok += 1
    else:
        bad.append(("mismatch", rel))
with open(out, "w", encoding="utf-8") as f:
    f.write(f"staged study files compared: {n_ok + len(bad)}; equal: {n_ok}; bad: {len(bad)}\n")
    for b in bad:
        f.write(f"{b[0]} {b[1]}\n")
    f.write("VERDICT " + ("STUDY_EQUAL" if not bad and n_ok > 0 else "STUDY_DIFFERS") + "\n")
print(open(out, encoding="utf-8").read())
