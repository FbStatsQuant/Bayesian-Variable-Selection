"""W3-READER DEPS.tsv builder (standard library). Hashes each reader-version row block (between ROW markers), each
lemma, the PoolZ section and NOTATION.md, in the working tree and in a checked snapshot directory; state OK if equal."""
import hashlib, re, sys, pathlib
T = pathlib.Path(__file__).resolve().parents[1]
SNAP = T / "reviews" / (sys.argv[1] if len(sys.argv) > 1 else "S2_frozen")
CHECKED_BY = sys.argv[2] if len(sys.argv) > 2 else "reviews/S2_linecheck_sol.md (pending)"
def h(s): return hashlib.sha256(s.encode()).hexdigest()[:16]
def rows(text):
    return {m.group(1): m.group(0) for m in re.finditer(r"<!-- ROW (thm\d+) BEGIN -->.*?<!-- ROW \1 END -->", text, re.S)}
def section(text, start, end):
    i = text.find(start); j = text.find(end, i + 1)
    return text[i:j] if i >= 0 else ""
uses = {
 "thm1": "W3-POST:Thm-1@1.0.0; SOP:TH09@1.0.0; W3-POST2:C@1.0.0; W3-POST2:E@1.0.0; W3-POST2:A0@1.0.0; W3-POST2:A1@1.0.0; W3-READER:R1",
 "thm2": "W3-POST:Thm-1@1.0.0 item 6; W2-APP:POST@1.0.1; W3-READER:R1",
 "thm3": "W3-PSHARP:A@1.0.0; W3-PSHARP:B@1.0.0; W3-READER:R1 (B3.2)",
 "thm4": "W3-MISR:MIS(i)@1.0.0; MIS(i')@1.0.0; MIS(ii)@1.0.0; Cor-G(b)@1.0.0; W3-READER:R1 (B4.1)",
 "thm5": "W3-START2:START-R@1.0.0; W3-START2:BR@1.0.0; W3-START:FLOOR@1.0.0",
 "thm6": "W3-RM2:RM2-R@1.0.0; W3-RM:RM-0@1.0.0; W3-RM:E4@1.0.0; W2-UNI:F-UNI@1.1.0; W3-RM2:D-to-W@1.0.0; W3-RM2:POST-R@1.0.0; W3-READER:R1, R2, R3",
 "thm7": "W3-RM2:RM2-F@1.0.0; W3-RM2:W-suff@1.0.0; W3-RM:RM-0@1.0.0; W2-UNI:F-UNI@1.1.0; W3-READER:R1, R2, R3",
 "thm8": "W3-SCR:A1@1.0.0",
 "thm9": "(placeholder; W3-DIST)",
 "thm10": "W3-SAMP:C@1.1.1; W3-START2:IF-START@1.0.0; W3-POST:Thm-1@1.0.0; W2-APP:POST@1.0.1; W3-READER:R4, PoolZ",
}
cur_rv, snap_rv = (T / "READER_VERSIONS.md").read_text(), (SNAP / "READER_VERSIONS.md").read_text()
cr, sr = rows(cur_rv), rows(snap_rv)
out = ["id\tfile[:lines]\tuses\tsha (sha256, first 16 hex)\tchecked_sha\tchecked_by\tstate"]
def add(i, f, u, cur, snap):
    a = h(cur); b = h(snap) if snap else ""
    st = "PENDING-CHECK" if (b and a == b and "pending" in CHECKED_BY) else ("OK" if b and a == b else ("STALE" if b else "UNCHECKED"))
    out.append("\t".join([i, f, u, a, b, CHECKED_BY if b else "", st]))
# stand-alone objects first
st = lambda p: (T / p).read_text()
ss = lambda p: (SNAP / p).read_text() if (SNAP / p).exists() else ""
pz = ("## Claim PoolZ", "## Bridge lemmas")
add("W3-READER:PoolZ", "STATEMENT.md §Claim PoolZ", "W1-N1:Thm-N1@1.0.0", section(st("STATEMENT.md"), *pz), section(ss("STATEMENT.md"), *pz))
for r, f in [("R1", "lemmas/R1_set_sizes.md"), ("R2", "lemmas/R2_local_regression.md"), ("R3", "lemmas/R3_delivery_assembly.md"), ("R4", "lemmas/R4_printed_outputs.md")]:
    add("W3-READER:" + r, f, {"R1": "SOP:TH09 ([T03R] E2(ii))", "R2": "-", "R3": "W2-UNI:F-UNI@1.1.0; W3-RM2:RM2-R/F@1.0.0", "R4": "W3-SAMP:C@1.1.1; W3-START2:IF-START@1.0.0; W2-APP:POST@1.0.1"}[r], st(f), ss(f))
add("NOTATION", "NOTATION.md", "code pins (Scripts/SMC_BVS/core)", st("NOTATION.md"), ss("NOTATION.md"))
for k in sorted(cr, key=lambda x: int(x[3:])):
    add("RV/" + k, "READER_VERSIONS.md ROW " + k, uses.get(k, ""), cr[k], sr.get(k, ""))
add("CARD", "CLAIMS_CARD.md", "RV/thm1-thm10", st("CLAIMS_CARD.md"), ss("CLAIMS_CARD.md"))
(T / "DEPS.tsv").write_text("\n".join(out) + "\n")
print("\n".join(l.split("\t")[0] + "  " + l.split("\t")[-1] for l in out[1:]))
