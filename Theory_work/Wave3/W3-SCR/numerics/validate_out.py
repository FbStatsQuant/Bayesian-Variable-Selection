"""W3-SCR: validate numerics outputs after the interrupted/duplicated batch; remove corrupt N2 files, dedupe N1 files."""
import glob, json, os
for f in sorted(glob.glob("n2_out/*.txt")):
    reps = set(); summ = 0; bad = 0
    for line in open(f, encoding="utf-8", errors="replace"):
        line = line.strip("\x00 \r\n")
        if not line: continue
        try:
            if line.startswith("SUMMARY "): json.loads(line[8:]); summ += 1
            else: reps.add(json.loads(line)["rep"])
        except Exception: bad += 1
    ok = (len(reps) == 10 and summ == 1 and bad == 0 and sum(1 for _ in open(f, encoding="utf-8", errors="replace")) == 11)
    print(f, "reps", len(reps), "summary", summ, "bad", bad, "OK" if ok else "REMOVED")
    if not ok: os.remove(f)
n = 0
for f in sorted(glob.glob("n1_raw/*.jsonl")):
    lines = [l for l in open(f, encoding="utf-8") if l.strip()]
    good = []
    for l in lines:
        try: json.loads(l); good.append(l)
        except Exception: pass
    if not good: os.remove(f); print(f, "REMOVED"); continue
    if len(lines) != 1: open(f, "w", encoding="utf-8").write(good[0]); print(f, "deduped", len(lines), "->1")
    n += 1
print("valid N1 files:", n)
