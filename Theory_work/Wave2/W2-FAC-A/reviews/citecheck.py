"""citecheck.py -- open every external source cited by W2-FAC-A (STATEMENT.md, lemmas/*.md) and confirm the quoted
text / statement is there (line ranges checked where given). Run from the repo root: py -3.13 Theory_work/Wave2/W2-FAC-A/reviews/citecheck.py
Writes reviews/CITECHECK.txt."""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
T = "Theory_work/"
SOP = T + "State_of_Project/sections/"
CHECKS = [
    # (file, needle, (line_lo, line_hi) or None, cited where)
    (T + "Wave1C/FINAL/sections/s1_setting.tex", "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))", None, "STATEMENT §6, L4 [M5-0]"),
    (SOP + "04_theory.tex", "Composition at every n", (477, 489), "L4 [M5-0] SoP/04_theory.tex:477-489"),
    (T + "Wave1C/FINAL/sections/s3_posterior.tex", "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)", None, "STATEMENT §6, L4 [S-T]"),
    (T + "Wave1C/FINAL/sections/s3_posterior.tex", "Conditional convergence alone would not suffice", None, "L5.1 every-sequence argument"),
    (T + "Wave1/W1-GEN/lemmas/L5_assembly.md", "Operational closure", None, "L4 [OP]"),
    (T + "Wave1/W1-GEN/lemmas/L5_assembly.md", "PROVED (by this seat", None, "L4 [OP] status"),
    (T + "Wave1C/C-GROW/lemmas/L1_descent.md", "Lemma L1.2 (the path and the capped search)", None, "L4 [GROW-L1]"),
    (T + "Wave1C/C-GROW/lemmas/L1_descent.md", "S₀ ⊆ Q ⊆ [p], |Q| ≤ K", None, "L4 [GROW-L1] hypotheses"),
    (T + "Wave1C/C-GROW/lemmas/L1_descent.md", "lemma check R03 (Codex Sol high", None, "L4 [GROW-L1] check record"),
    (T + "Wave1C/C-GROW/lemmas/L3_sandwich.md", "*(a) Every truth is in S̃.*", None, "L2 re-proof source"),
    (T + "Wave1C/C-GROW/STATEMENT.md", "|Q| ≤ C_Q log n", None, "L2 status (G1)"),
    (T + "Wave1C/C-GROW/lemmas/L4_assembly.md", "it does not depend on the cap", None, "L4 [OP] cap-independence"),
    (T + "Wave1/W1-GEN/lemmas/L1_lemmaE.md", "L1.4", None, "L2 [GEN-L1] L1.4(b)"),
    (T + "Wave1/W1-PXN/lemmas/CR_corr_tails.md", "3p² e^{−(n−1)δ²/1024}", None, "L5.1 [CONC']"),
    (T + "Wave1/W1-PXN/lemmas/CR_corr_tails.md", "XF VERIFIED (R19", None, "L5.1 [CONC'] status"),
    (T + "Wave1/W1-GEN/STATEMENT.md", "s₀ = 14 with one of the study's two high-p layouts", None, "STATEMENT (I)(c) layouts"),
    (T + "Wave1/W1-GEN/numerics/study_common.py", "return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I", None, "S5 covariance (port)"),
    ("Scripts/Data_generators/gen_dev_data.R", "0.3*matrix(1,p,p)+0.4*H+0.3*I", None, "S5 covariance (generator)"),
    (T + "Wave1C/C-GROW/STATEMENT.md", "(b) **S5 population covariance, fixed p (illustration).**", None, "STATEMENT (I)(c) diagnostic layout"),
    (T + "Wave1C/FINAL/sections/s6_delivery.tex", "PROVED-CHECKED for the patched calibration law", None, "STATEMENT §6 Prop F status"),
    (T + "Wave1C/FINAL/sections/s6_delivery.tex", "round 3 PASSED (Sol 9.3, Opus 8.6)", None, "STATEMENT §6 A1 council"),
    (T + "Wave1C/FINAL/sections/s6_delivery.tex", "\\st{PROVED (A2), checked by A3}", None, "STATEMENT §6 A2 status"),
    (T + "Wave1C/HQ_AUDIT/A4_postcouncil_check.md", "OK-WITH-FIXES", None, "STATEMENT §6 A4"),
    (T + "Wave1C/HQ_AUDIT/A2_propF_GROW.md", "EXTENDS", (1, 3), "L7 template"),
    (T + "Wave1C/HQ_AUDIT/A2_propF_GROW.md", "Lemma S extends", None, "L7 step 1"),
    (T + "Wave1C/C-DLV/lemmas/L4_delivery.md", "𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_nᶜ", (60, 80), "L7 DLV lemmas/L4_delivery.md:65-77"),
    (T + "Wave1C/FINAL/sections/s1_setting.tex", "complete linkage on $1-|\\hat{r}|$", None, "Lemma P5 partition"),
    ("Scripts/SMC_BVS/core/cpp/v3_blocks.h", "", None, "partition code (R04 checked lines 121-140)"),
]


def main():
    out, miss = [], 0
    for f, needle, rng, where in CHECKS:
        path = os.path.join(ROOT, f)
        if not os.path.exists(path):
            out.append("MISS(file)  %s  [%s]" % (f, where)); miss += 1; continue
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
        if not needle:
            out.append("OK(file)    %s  [%s]" % (f, where)); continue
        hits = [i + 1 for i, l in enumerate(lines) if needle in l]
        if not hits:
            whole = "\n".join(lines)
            hits = [whole[:whole.find(needle)].count("\n") + 1] if needle in whole else []
        if not hits:
            out.append("MISS(text)  %s : %r  [%s]" % (f, needle, where)); miss += 1; continue
        if rng and not any(rng[0] <= h <= rng[1] for h in hits):
            out.append("MISS(line)  %s : %r at %s, cited %d-%d  [%s]" % (f, needle, hits, rng[0], rng[1], where)); miss += 1; continue
        out.append("OK          %s:%s  [%s]" % (f, hits[0], where))
    out.append("TOTAL %d citations, %d misses" % (len(CHECKS), miss))
    txt = "\n".join(out)
    print(txt)
    open(os.path.join(os.path.dirname(__file__), "CITECHECK.txt"), "w", encoding="utf-8").write(txt + "\n")


if __name__ == "__main__":
    main()
