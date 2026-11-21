import sys, os, json, struct, hashlib, array, glob
def sec(path, names):
    out = {}
    with open(path, "rb") as fh:
        h = fh.read(128); assert h[:8] == b"SMCBVS4\x00"
        ns = struct.unpack_from("<3I", h, 12)[2]; size = struct.unpack_from("<Q", h, 24)[0]
        assert os.path.getsize(path) == size
        tbl = fh.read(128 * ns)
        for i in range(ns):
            o = 128 * i; nm = tbl[o:o+48].split(b"\0")[0].decode()
            if nm not in names: continue
            dt, nd = struct.unpack_from("<II", tbl, o + 48); d0, d1, off, ln = struct.unpack_from("<4Q", tbl, o + 56)
            fh.seek(off); b = fh.read(ln); assert hashlib.sha256(b).digest() == tbl[o+88:o+120]
            a = array.array("d"); a.frombytes(b); out[nm] = list(a)
    return out
res = {}
for d in sys.argv[1:]:
    fs = sorted(glob.glob(os.path.join(d, "island_*.bin")), key=lambda s: int(os.path.basename(s)[7:-4]))
    r = {}
    for f in fs:
        s = sec(f, {"st_ess", "st_phi"}); r[os.path.basename(f)] = s
    res[d] = r
json.dump(res, sys.stdout)
