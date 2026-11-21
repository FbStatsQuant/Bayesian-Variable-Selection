#!/usr/bin/env python3
# descriptive, unregistered: reads st_phi / st_ess (+grid) sections of island.bin files (same container as compare_overlap_v2.read_sections; seeks only)
import sys, os, struct, hashlib, array, json
def sections(path, names):
    out = {}
    with open(path, "rb") as fh:
        h = fh.read(128)
        assert h[:8] == b"SMCBVS4\x00", "bad magic"
        ns = struct.unpack_from("<3I", h, 12)[2]; size = struct.unpack_from("<Q", h, 24)[0]
        assert os.path.getsize(path) == size, "size mismatch"
        tbl = fh.read(128 * ns)
        for i in range(ns):
            o = 128 * i; nm = tbl[o:o+48].split(b"\0")[0].decode()
            if nm not in names: continue
            dt, nd = struct.unpack_from("<II", tbl, o + 48); d0, d1, off, ln = struct.unpack_from("<4Q", tbl, o + 56)
            fh.seek(off); b = fh.read(ln)
            assert hashlib.sha256(b).digest() == tbl[o+88:o+120], "hash " + nm
            assert dt == 1, "dtype"
            a = array.array("d"); a.frombytes(b); out[nm] = list(a)
    return out
if __name__ == "__main__":
    res = {}
    for f in sys.argv[1:]:
        s = sections(f, {"grid", "st_phi", "st_ess", "st_inc"})
        res[f] = s
    json.dump(res, sys.stdout)
