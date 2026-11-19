#!/usr/bin/env python3
"""vf_merge_units.py -- add law.bin + data.bin to the 14 VF units of records/precision1e4 (manager 11-19): verify each file's CONTENT hash against what the fit recorded
(law.bin.json outputs['law.bin'] for the law; law.bin.json inputs['data.bin'] and data.bin.json / eval inputs for the data), move it into the unit, keep the old SHA256SUMS as
SHA256SUMS.prev (not deleted), write the new SHA256SUMS (old entries + the two new files), `sha256sum -c`. No recomputation of any fit. Stdlib only."""
import hashlib, json, os, shutil, struct, subprocess, sys
REC = "/home/fb31/SMC_Engineering_Department/records/precision1e4"; FETCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetch")
def content_hash(path):   # INTERFACES §5.1 as p1m_manifest.py: header content_sha256 (verified against table + header) or the table hash for v0.1.1 files
    with open(path, "rb") as fh:
        hdr = fh.read(128)
        if hdr[:8] != b"SMCBVS4\0": raise SystemExit("%s: not an engine container" % path)
        ns = struct.unpack_from("<I", hdr, 20)[0]; table = fh.read(128 * ns)
    th = hashlib.sha256(table).digest()
    if th != hdr[32:64]: raise SystemExit("%s: section table hash mismatch" % path)
    stored = hdr[64:96]
    if stored == b"\0" * 32: return th.hex()
    ch = hashlib.sha256(hdr[:32] + b"\0" * 64 + hdr[96:128] + table).digest()
    if ch != stored: raise SystemExit("%s: content hash mismatch" % path)
    return ch.hex()
def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""): h.update(c)
    return h.hexdigest()
log = []; bad = 0
for line in open(os.path.join(os.path.dirname(FETCH), "vf_list.tsv")):
    wave, batch, rid = line.rstrip("\n").split("\t"); u = "%s/%s/%s" % (REC, wave, rid)
    lj = json.load(open(u + "/law.bin.json")); want_law = lj["outputs"]["law.bin"]; want_data = lj["inputs"]["data.bin"]
    try:
        f_law, f_data = "%s/%s/%s/law.bin" % (FETCH, batch, rid), "%s/%s/%s/data.bin" % (FETCH, batch, rid)
        got_law, got_data = content_hash(f_law), content_hash(f_data)
    except (OSError, SystemExit) as e:
        print("MISSING/INVALID %s: %s" % (rid, e)); bad += 1; continue
    ok = got_law == want_law and got_data == want_data
    print("%-28s law content %s.. == recorded %s.. : %s | data content %s.. == recorded %s.. : %s" % (rid, got_law[:12], want_law[:12], got_law == want_law, got_data[:12], want_data[:12], got_data == want_data))
    if not ok: bad += 1; continue
    if os.path.exists(u + "/law.bin") or os.path.exists(u + "/SHA256SUMS.prev"):
        print("   already merged: skipped"); continue
    shutil.copy2(u + "/SHA256SUMS", u + "/SHA256SUMS.prev")     # the old sums are kept, not deleted
    shutil.move(f_law, u + "/law.bin"); shutil.move(f_data, u + "/data.bin")
    ent = [l.rstrip("\n") for l in open(u + "/SHA256SUMS.prev") if l.strip()] + ["%s  law.bin" % sha(u + "/law.bin"), "%s  data.bin" % sha(u + "/data.bin")]
    ent.sort(key=lambda l: l.split("  ", 1)[1]); open(u + "/SHA256SUMS", "w").write("\n".join(ent) + "\n")
    r = subprocess.run(["sha256sum", "--quiet", "-c", "SHA256SUMS"], cwd=u); 
    names = sorted(f for f in os.listdir(u) if f.startswith("SHA256SUMS"))
    print("   merged; sha256sum -c rc=%d; sums files %s; entries %d" % (r.returncode, names, len(ent)))
    if r.returncode: bad += 1
print("DONE; problems: %d" % bad); sys.exit(1 if bad else 0)
