#!/usr/bin/env python3
"""gc_v4_check.py <runs_root> <smcbvs4> <batch/run>... -- V4 of the H-41 "verified merge" (GC_PLAN §5), runs ON NOTS (stdlib; detached, nice 19; env.sh sourced by the caller; READ-ONLY): for every fit run dir
  (a) fit.bin.json says status completed and lists island_1.bin .. island_16.bin in `inputs` (exactly the files the merge consumed, with their content hashes);
  (b) for each island_k.bin: `smcbvs4 info island_k.bin --verify 1` (the F2 binary) returns rc 0 with `verified` true, its `content_sha256` equals the island sidecar's `island_bin` AND the fit's `inputs[island_k.bin]`,
      the sidecar status is completed, and the on-disk size equals the container header's file_bytes;
  (c) records (size, mtime_ns) of every island file so that the deleter can refuse a file that changed after this check.
Prints one JSON {run: {ok, n_ok, n, problems, files: {island_k.bin: [size, mtime_ns]}}}. Nothing is written or deleted."""
import json, os, struct, subprocess, sys
root, binf = sys.argv[1], sys.argv[2]; out = {}
for br in sys.argv[3:]:
    d = os.path.join(root, br); prob = []; files = {}; n_ok = 0
    try: fj = json.load(open(os.path.join(d, "fit.bin.json")))
    except Exception as e: out[br] = {"ok": False, "n_ok": 0, "n": 0, "problems": ["fit.bin.json unreadable: %s" % e], "files": {}}; continue
    if fj.get("status") != "completed": prob.append("fit.bin.json status %r" % fj.get("status"))
    inp = fj.get("inputs") or {}; want = ["island_%d.bin" % k for k in range(1, 17)]
    missing = [w for w in want if w not in inp]
    if missing: prob.append("fit inputs lack %s" % missing)
    for w in want:
        p = os.path.join(d, w)
        if not os.path.isfile(p) or os.path.islink(p): prob.append("%s missing / not a regular file" % w); continue
        st = os.stat(p); files[w] = [st.st_size, st.st_mtime_ns]
        with open(p, "rb") as fh: hb = fh.read(32); fb = struct.unpack_from("<Q", hb, 24)[0]
        sc = json.load(open(p + ".json")) if os.path.exists(p + ".json") else {}
        r = subprocess.run([binf, "info", p, "--verify", "1"], capture_output=True, text=True)
        try: j = json.loads(r.stdout)
        except Exception: j = {}
        ok = r.returncode == 0 and j.get("verified") is True and j.get("content_sha256") == sc.get("island_bin") == inp.get(w) and sc.get("status") == "completed" and st.st_size == fb
        if ok: n_ok += 1
        else: prob.append("%s: rc %d verified %r content %s sidecar %s fit %s status %r size %d header %d" % (w, r.returncode, j.get("verified"), str(j.get("content_sha256"))[:12], str(sc.get("island_bin"))[:12], str(inp.get(w))[:12], sc.get("status"), st.st_size, fb))
    out[br] = {"ok": not prob and n_ok == 16, "n_ok": n_ok, "n": 16, "problems": prob, "files": files}
json.dump(out, sys.stdout)
