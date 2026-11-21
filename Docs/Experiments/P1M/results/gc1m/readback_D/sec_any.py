import sys, os, json, struct, hashlib, array
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
            if dt == 9: out[nm] = b.decode()[:2000]; continue
            a = array.array({1:"d",2:"i"}.get(dt, "q") if dt in (1,2) else "q"); 
            if dt not in (1,2): out[nm] = ("dtype",dt,nd,d0,d1); continue
            a.frombytes(b); out[nm] = (list(a), d0, d1)
    return out
names = set(sys.argv[1].split(","))
res = {}
for f in sys.argv[2:]:
    res[f] = sec(f, names)
json.dump(res, sys.stdout)
