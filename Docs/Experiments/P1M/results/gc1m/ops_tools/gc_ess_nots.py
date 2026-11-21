#!/usr/bin/env python3
"""gc_ess_nots.py <run_dir>... -- runs ON NOTS (stdlib only, read-only; shipped and run detached with nice 19): for every island_<k>.bin of each run dir read the sections st_phi, st_ess, grid by SEEKS ONLY (hash-verified per section,
same container reader as readback_D/ess_read.py) and print one JSON {run_dir: {island_k.bin: {grid, st_phi, st_ess}}}. Nothing is written to the runs. Used by gc_wave_check.py (HQ H-48 wave check): the islands stay on NOTS."""
import array, glob, hashlib, json, os, struct, sys
def sections(path, names):
    out = {}
    with open(path, "rb") as fh:
        h = fh.read(128)
        assert h[:8] == b"SMCBVS4\x00", "bad magic"
        ns = struct.unpack_from("<3I", h, 12)[2]; size = struct.unpack_from("<Q", h, 24)[0]
        assert os.path.getsize(path) == size, "size mismatch"
        tbl = fh.read(128 * ns)
        for i in range(ns):
            o = 128 * i; nm = tbl[o:o + 48].split(b"\0")[0].decode()
            if nm not in names: continue
            dt, nd = struct.unpack_from("<II", tbl, o + 48); d0, d1, off, ln = struct.unpack_from("<4Q", tbl, o + 56)
            fh.seek(off); b = fh.read(ln)
            assert hashlib.sha256(b).digest() == tbl[o + 88:o + 120], "hash " + nm
            assert dt == 1, "dtype " + nm
            a = array.array("d"); a.frombytes(b); out[nm] = list(a)
    return out
if __name__ == "__main__":
    res = {}
    for d in sys.argv[1:]:
        r = {}
        for f in sorted(glob.glob(os.path.join(d, "island_*.bin")), key=lambda s: int(os.path.basename(s)[7:-4])):
            r[os.path.basename(f)] = sections(f, {"grid", "st_phi", "st_ess"})
        res[d] = r
    json.dump(res, sys.stdout)
