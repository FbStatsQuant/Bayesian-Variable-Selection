"""CITECHECK: open every path:line cited in STATEMENT.md / lemmas/*.md and confirm the quoted content is there.
Run from the repo root: py -3.13 Theory_work/Wave1C/C-MIS/numerics/citecheck.py > Theory_work/Wave1C/C-MIS/reviews/CITECHECK.txt
"""
import io, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SOP = "Theory_work/State_of_Project/sections/"
NBH = "Theory_work/Old_Projects/New_BVS_Headquarters/"
T03R = NBH + "branch_snapshots/A-REV5/sources/W1-T03R/PROOF.md"
T38 = NBH + "branch_snapshots/A-REV5/sources/W4-T38FULL/T38_PROOF.md"
GEN = "Theory_work/Wave1/W1-GEN/"
COMMON = "Docs/Theory/theorems/00_COMMON.md"

CHECKS = [
    # (path, first line, last line, list of substrings that must all occur in that range)
    (COMMON, 9, 9, ["non-constant y^r", "Standardised X"]),
    (COMMON, 14, 14, ["μ = CX^rβ*", "S₀ = supp β*"]),
    (COMMON, 35, 35, ["| G |", "ε ~ N_n(0, σ*²I)"]),
    (SOP + "02_method.tex", 84, 106, ["a_0=b_0=0.01", "H_S=(n+1)G_S+I_k", "nu=a_0+n/2"]),
    (SOP + "04_theory.tex", 466, 466, ["T38-(0) \"PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))\""]),
    (SOP + "04_theory.tex", 774, 782, ["fixed \\(s_0\\ge1\\)", "Tail cutoff", "Anchored eigenvalues", "Final statement"]),
    (SOP + "04_theory.tex", 775, 775, ["fixed \\(s_0\\ge1\\)"]),
    (SOP + "04_theory.tex", 776, 779, ["Tail cutoff", "BM-∞"]),
    (SOP + "04_theory.tex", 776, 782, ["Final statement"]),
    (SOP + "04_theory.tex", 811, 811, ["2\\cdot10^{6}"]),
    (T03R, 15, 17, ["R_m:="]),
    (T03R, 44, 47, ["m^\\sharp_n(\\omega):=\\min"]),
    (T03R, 52, 52, ["s_0\\le m^\\sharp_n(\\omega)\\le\\min\\{K,\\ m_n(\\omega)\\}"]),
    (T03R, 74, 99, ["Theorem T02(i♯)", "Lemma den′"]),
    (T03R, 89, 91, ["Lemma den′", "c_{\\rm IG}"]),
    (T03R, 129, 134, ["SE$_\\lambda(j_0)$", "SE$_w(m;g_0)$"]),
    (T03R, 136, 136, ["Lemma I (interlacing"]),
    (T03R, 160, 207, ["Theorem T03♯", "(C10)", "Changed steps"]),
    (T03R, 168, 168, ["**Conclusions.**", "(iv) [no beta-min]"]),
    (T03R, 172, 172, ["(C1) Setting", "m_n:=m^\\sharp_n"]),
    (T38, 16, 30, ["Output-available event", "Lemma RO"]),
    (T38, 34, 46, ["Part (0): the composition", "Markov's inequality"]),
    (GEN + "REPORT.md", 20, 20, ["PROVED-CHECKED"]),
    (GEN + "REPORT.md", 24, 41, ["Theorem GEN", "D_n ≤ P(S̃₀ ≠ S*)"]),
    (GEN + "STATEMENT.md", 115, 115, ["(C4) Random designs", "X-measurable"]),
    (GEN + "lemmas/L5_assembly.md", 57, 64, ["Lemma L5.3 (de-randomisation)"]),
    (GEN + "lemmas/L5_assembly.md", 66, 80, ["Theorem L5.4"]),
    ("Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex", 52, 56, ["IG(v;0.51,b)", "nv(G_S+I)^{-1}"]),
    ("Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex", 340, 342, ["Integral representation", "IG(v;0.51"]),
    (SOP + "02_method.tex", 127, 130, ["IG}(0.51,0.01s_y^2)"]),
    (T03R, 162, 164, ["BM-∞", "BM($c$)", "proof artefact"]),
    (T03R, 164, 164, ["proof artefact, not sharp"]),
    (T03R, 170, 170, ["thresholds $n_0$ now depend on"]),
    (GEN + "lemmas/L6_instances.md", 86, 110, ["## (c) W", "BM-∞", "VIS", "Leakage"]),
]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ok = True
    for path, a, b, subs in CHECKS:
        full = os.path.join(ROOT, path)
        try:
            lines = io.open(full, encoding="utf8").read().split("\n")
        except OSError as ex:
            print(f"MISS  {path}:{a}-{b}  (cannot open: {ex})"); ok = False; continue
        chunk = "\n".join(lines[a - 1:b])
        missing = [s for s in subs if s not in chunk]
        status = "OK  " if not missing else "MISS"
        ok &= not missing
        print(f"{status}  {path}:{a}-{b}" + ("" if not missing else f"  missing: {missing}"))
    print("ALL OK" if ok else "SOME MISSES")


if __name__ == "__main__":
    main()
