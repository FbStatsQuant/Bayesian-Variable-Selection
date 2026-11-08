"""n3lib.py -- definitions for the N3 checks: instances, exact brute force of the prescribed start mode,
DFS order of the coded enumeration, the floating replica of the code's log_gamma0, and the harness driver.

Everything here is a direct transcription of STATEMENT.md section 1 (definitions), NOT of the code under test,
except `ghat` (clause (e)), which replicates Start::comp / log_gamma0 (v3_start.h:54-69) operation by operation.
"""
from fractions import Fraction
from itertools import combinations
import math
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.join(HERE, "sm_harness.exe")


class Inst:
    """p, K, blocks (list of increasing lists), lam (list len K+1), rho (list per block: dict code->value),
    values are Python ints, Fractions or floats. `cap` is the start_mode cap."""

    def __init__(self, p, K, blocks, lam, rho, cap=1000000, iid="x"):
        self.p, self.K, self.blocks, self.lam, self.rho, self.cap, self.iid = p, K, blocks, lam, rho, cap, iid
        self.blk = {}
        self.pos = {}
        for b, C in enumerate(blocks):
            for i, x in enumerate(C):
                self.blk[x] = b
                self.pos[x] = i

    def parts(self, S):
        """choice vector: list of codes per block"""
        codes = [0] * len(self.blocks)
        for x in S:
            codes[self.blk[x]] |= 1 << self.pos[x]
        return codes


def exact(v):
    return v if isinstance(v, (int, Fraction)) else Fraction(v)


def f_exact(I, S):
    codes = I.parts(S)
    return exact(I.lam[len(S)]) + sum(exact(I.rho[b][c]) for b, c in enumerate(codes) if c)


def ghat(I, S):
    """float replica of Start::log_gamma0 (blocks met by S in increasing block order, starting from s = 0.0)."""
    codes = I.parts(S)
    s = 0.0
    for b, c in enumerate(codes):
        if c:
            s += float(I.rho[b][c])
    return float(I.lam[len(S)]) + s


def all_sets(I):
    for k in range(0, I.K + 1):
        for S in combinations(range(I.p), k):
            yield list(S)


def prescribed(I, value=f_exact):
    """returns (maxval, kstar, Astar sorted lexicographically, Sstar)"""
    best = None
    A = []
    for S in all_sets(I):
        v = value(I, S)
        if best is None or v > best:
            best, A = v, [S]
        elif v == best:
            A.append(S)
    kstar = min(len(S) for S in A)
    Astar = sorted(S for S in A if len(S) == kstar)  # Python list order == lex_less on sorted int lists
    return best, kstar, Astar, Astar[0]


def dfs_key(I, S):
    codes = I.parts(S)
    key = []
    for b in range(len(I.blocks) - 1, -1, -1):
        key += [bin(codes[b]).count("1"), codes[b]]
    return tuple(key)


def predict(I):
    """Predicted start_mode output per STATEMENT (a)-(d)."""
    best, kstar, Astar, Sstar = prescribed(I)
    order = sorted(Astar, key=lambda S: dfs_key(I, S))
    visited = order[: I.cap]
    S_ret = min(visited)
    return dict(lg0=best, kstar=kstar, nA=len(Astar), Sstar=Sstar, ties=min(len(Astar), I.cap),
                truncated=int(len(Astar) >= I.cap), S=S_ret)


def fmt(v):
    if isinstance(v, int):
        fv = float(v)
        assert math.isfinite(fv) and int(fv) == v, "integer table value not representable as a double"
        return float.hex(fv)
    if isinstance(v, Fraction):
        fv = float(v)
        assert Fraction(fv) == v, "table value not representable as a double"
        return float.hex(fv)
    if isinstance(v, float) and math.isnan(v):
        return "nan"
    return float.hex(float(v))


def encode_table(I):
    J = len(I.blocks)
    out = [f"T {I.iid} {I.p} {I.K} {J} {I.cap}", " ".join(fmt(v) for v in I.lam)]
    for b, C in enumerate(I.blocks):
        m = len(C)
        out.append(f"{m} " + " ".join(map(str, C)))
        vals = []
        for c in range(1 << m):
            if c == 0:
                vals.append("0")
            elif bin(c).count("1") > min(m, I.K):
                vals.append("nan")
            else:
                vals.append(fmt(I.rho[b][c]))
        out.append(" ".join(vals))
    return "\n".join(out) + "\n"


def parse_R(line):
    t = line.split()
    assert t[0] == "R"
    k = int(t[5])
    return dict(id=t[1], lg0=float.fromhex(t[2]) if "0x" in t[2] or "inf" in t[2] else float(t[2]),
                ties=int(t[3]), truncated=int(t[4]), S=[int(x) for x in t[6:6 + k]])


def run_harness(text):
    r = subprocess.run([HARNESS], input=text, capture_output=True, text=True, check=True)
    return r.stdout.splitlines()


def run_tables(insts):
    lines = run_harness("".join(encode_table(I) for I in insts))
    res = [parse_R(l) for l in lines]
    assert len(res) == len(insts)
    return res


def run_data(cases):
    """cases: list of (iid, n, p, B, cap, Xcolmajor, y). Returns list of (Inst built from the code's own tables, R)."""
    text = []
    for iid, n, p, B, cap, X, y in cases:
        text.append(f"D {iid} {n} {p} {B} {cap}\n" + " ".join(float.hex(v) for v in X) + "\n" +
                    " ".join(float.hex(v) for v in y) + "\n")
    lines = run_harness("".join(text))
    out = []
    i = 0
    for iid, n, p, B, cap, X, y in cases:
        K = int(lines[i].split()[1]); i += 1
        lam = [float.fromhex(v) for v in lines[i].split()[1:]]; i += 1
        blocks, rho = [], []
        while lines[i].startswith("B"):
            t = lines[i].split(); m = int(t[1]); blocks.append([int(x) for x in t[2:2 + m]]); i += 1
            vals = lines[i].split()[1:]; i += 1
            rho.append({c: (float("nan") if v == "nan" else float.fromhex(v)) for c, v in enumerate(vals)})
        R = parse_R(lines[i]); i += 1
        out.append((Inst(p, K, blocks, lam, rho, cap, iid), R))
    return out
