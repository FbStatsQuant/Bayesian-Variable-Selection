"""W3-PSHARP-R citation check (adapted from Theory_work/Wave3/W3-PSHARP/citecheck.py).
(1) every cited line range of an external file must contain the quoted tokens; (2) every parent line reference written
as `PARENT :a-b`, `P-ST :a-b`, `P-A :a-b` in this ticket's files must lie inside the parent file; (3) numbers quoted from
the numerics output must occur in it.
Run from anywhere:  python3 Theory_work/Wave3/W3-PSHARP-R/citecheck.py > Theory_work/Wave3/W3-PSHARP-R/reviews/CITECHECK.txt
"""
import os, re, subprocess, sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
W = "Theory_work/Wave3/"
PST, PA, PS = W + "W3-PSHARP/STATEMENT.md", W + "W3-PSHARP/lemmas/A_log_factor.md", W + "W3-PSHARP/lemmas/S_one_step.md"
RV = "/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md"
CHECKS = [  # (file, first, last, tokens, cited in)
    (PST, 16, 30, ["δ_n := 1 − π(S₀)", "γ_j := (Q_{S₀} − Q_{S₀∪{j}})/(2b₀ + Q_{S₀})"], "STATEMENT §1"),
    (PST, 21, 21, ["w(k) = ½/C(2p − 1, k)"], "A2C §2"),
    (PST, 29, 29, ["γ_j :="], "A2C §2"),
    (PST, 32, 44, ["Lemma S", "(sum)"], "STATEMENT §1, §6"),
    (PST, 36, 40, ["(determinant)", "equality iff x_j ⟂ col X_S", "(fit)", "(one model)", "γ_j ∈ [0, 1)"], "A2C header"),
    (PST, 48, 50, ["N_n := |𝒩_n| → ∞", "**(E)** ‖μ‖² ≤ nM", "**(C)** ‖θ*‖² ≤ nM′"], "STATEMENT §1, §2"),
    (PST, 54, 55, ["(W-orth)", "N_n ≤ n − 1 − rank X_{S₀}"], "STATEMENT §1; AE §7"),
    (PST, 56, 60, ["(W-sph)", "(log N_n)² = o(n)", "(r₀ + 1) log N_n = o(n)", "Example"], "STATEMENT §1, §2"),
    (PST, 62, 69, ["Proposition A.", "P( δ_n/(1 − δ_n) ≥ (1 − ϵ)Λ_n ) → 1"], "STATEMENT §0"),
    (PST, 63, 63, ["Λ_n := (s₀ + 1) · [2N_n/(2p − 1 − s₀)] · √(log N_n/(πn))"], "STATEMENT §1"),
    (PST, 71, 73, ["Corollary A1", "liminf E δ_n / [(s₀ + 1)√(log p/(πn))] ≥ 1"], "STATEMENT §0, §6"),
    (PST, 75, 77, ["Corollary A2", "(1 − o_P(1))(s₀ + 1)√(log p/(πn))"], "STATEMENT §0, §6"),
    (PST, 79, 88, ["Remark A3", "Not settled"], "STATEMENT §4.1"),
    (PST, 81, 83, ["orthogonal design", "raw designs with iid N(0, 1) entries"], "STATEMENT §4.1"),
    (PST, 84, 88, ["exact whenever log p ≍ log n", "W3-POST2:C"], "STATEMENT §0, §4.1"),
    (PST, 99, 99, ["(B1)", "π(S₀) ≤ [1 + (s₀ + 1)/(3√n)]⁻¹ surely"], "AE §8; STATEMENT §6"),
    (PST, 101, 102, ["Critical scale", "e^{−λ/2}"], "A2C Remark 1; TARGET"),
    (PST, 103, 111, ["(B2)", "(B3) Target correction"], "STATEMENT §0"),
    (PST, 109, 109, ["does not apply when log p = o(log n); no claim is made there"], "STATEMENT §0, §4.2"),
    (PA, 8, 10, ["Λ_n = P_n n^{−1/2} · N √(2τ/π)"], "A2C §5"),
    (PA, 12, 17, ["Lemma W", "E W₁ ≥ (1 − η)√(2τ/π)", "P( T_N < (1 − ϵ′)(1 − η) N √(2τ/π) )"], "A2C §5"),
    (PA, 22, 24, ["(i) χ²₁", "**exactly**"], "AE §2; A2C §5"),
    (PA, 26, 37, ["(ii) Sphere", "h_d(t) = c_d (1 − t²/d)^{(d−3)/2}", "∈ [(d−1)/d, √((d−1)/d)]",
                  "≤ 3τ/(2d)", "≥ −τ²/(2d)"], "AE §2"),
    (PA, 45, 46, ["*Proof.*", "e^{−ϵ/2}W_j"], "A2C §3"),
    (PA, 53, 63, ["u_j := x_j/√(n−1)", "κ_n := 2ν(n−1)σ*²/(nV)", "V ≤ σ*²E(1 + 0.04/(n−1)) + 1.06M + M′"], "AE §4; A2C §3"),
    (PA, 64, 68, ["P(κ_n < 1 − ϵ/(2 log N))", "N ≤ n − 1 under (W-orth)"], "A2C §3"),
    (PA, 79, 81, ["ζ_j := (n−1)⟨ω_j, ρ̃/‖ρ̃‖⟩²", "νγ_j ≥ κ′_nζ_j/2"], "AE §5"),
    (PA, 82, 85, ["Law of the ζ_j", "unconditionally"], "AE §5"),
    (PA, 95, 99, ["E₂ ≥ m/2", "C₀ := 4(1.02(3M + 4σ*²) + 2M′)/σ*²", "1 − κ′_n ≤ (C₀ + 2x(r₀+1))/n"], "AE §5"),
    (PA, 109, 112, ["P(𝒜_nᶜ)"], "AE §6"),
    (PA, 121, 121, ["Λ_n = (1+o(1))(s₀+1)√(log p/(πn))"], "STATEMENT §3.4; A2C §1"),
    (PA, 141, 142, ["(probability → 1)"], "STATEMENT §4.1"),
    (W + "W3-PSHARP/ASSUMPTION_MAP.md", 15, 15, ["N_n → ∞", "bounded N"], "STATEMENT §5; AE Remark 1"),
    (W + "W3-PSHARP/ASSUMPTION_MAP.md", 33, 36, ["No published lower bound for this target is known to us"], "TARGET §2"),
    (W + "API_AUDIT/sharp2/TRIAGE.md", 21, 22, ["T = ε/c_n"], "BRIEF/STATEMENT header"),
    (W + "API_AUDIT/sharp2/TRIAGE.md", 43, 43, ["| W3-PSHARP:A | EASY | **A1**", "√((a+½)/π)"], "STATEMENT header"),
    (W + "API_AUDIT/sharp2/TRIAGE.md", 80, 80, ["T12 PSHARP-E"], "STATEMENT header"),
    (W + "API_AUDIT/sharp2/TRIAGE.md", 111, 111, ["PSHARP Prop. A / Cor. A1"], "STATEMENT header"),
    (W + "API_AUDIT/sharp2/results/f02.md", 31, 31, ["no published statement"], "TARGET §2"),
    (RV, 246, 248, ["## 3. Theorem 3", "Section version** 0.2"], "READER_DELTA §1 (@88f5dec)"),
    (RV, 257, 266, ["(b) *(Orthogonal or Gaussian null columns.)*", "p\\to\\infty"], "READER_DELTA §1"),
    (RV, 268, 275, ["[S1-F5]", "[S1-F6]", "POST2-R1"], "READER_DELTA §1, §3"),
    (RV, 277, 281, ["Why each assumption", "These are witnesses, not claimed necessary"], "READER_DELTA §3"),
    (RV, 294, 295, ["expectation form of (b)"], "READER_DELTA §1, §4"),
]
miss = 0
for f, a, b, toks, where in CHECKS:
    path = f if f.startswith("/") else os.path.join(ROOT, f)
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError:
        print(f"MISS  {f}: file not found  [{where}]"); miss += 1; continue
    seg = "\n".join(lines[a - 1:b])
    for t in toks:
        ok = t in seg
        miss += not ok
        print(f"{'OK  ' if ok else 'MISS'}  {f}:{a}-{b}  {t!r}  [{where}]")
# (2) range check of parent line references written in this ticket's files
LEN = {k: len(open(os.path.join(ROOT, v), encoding="utf-8").read().splitlines()) for k, v in
       {"PARENT": PST, "P-ST": PST, "P-A": PA}.items()}
OWN = ["STATEMENT.md", "PLAN.md", "TARGET.md", "READER_DELTA.md", "lemmas/AE_expectation.md", "lemmas/A2C_critical.md"]
pat = re.compile(r"\b(PARENT|P-ST|P-A) :(\d+)(?:-(\d+))?((?:, ?:\d+(?:-\d+)?)*)")
nref = 0
for fn in OWN:
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        continue
    for ln, line in enumerate(open(p, encoding="utf-8").read().splitlines(), 1):
        for m in pat.finditer(line):
            nums = [int(m.group(2))] + ([int(m.group(3))] if m.group(3) else []) + [int(x) for x in re.findall(r"\d+", m.group(4))]
            nref += 1
            bad = [x for x in nums if not 1 <= x <= LEN[m.group(1)]]
            miss += bool(bad)
            if bad:
                print(f"MISS  {fn}:{ln}  {m.group(0)!r} out of range (len {LEN[m.group(1)]})")
print(f"range check: {nref} parent references scanned")
# (3) numbers quoted from numerics
OUT = [("numerics/ae_fixed_p_out.txt", "1000000 2 1  2.9348e-03 (2.1e-06)  2.9657e-03  0.990"),
       ("numerics/ae_fixed_p_out.txt", "1000000 3 1  3.0864e-03 (2.3e-06)  3.0515e-03  1.011"),
       ("numerics/ae_fixed_p_out.txt", "1000000 5 1  3.2242e-03 (5.1e-06)  3.1562e-03  1.022"),
       ("numerics/ae_fixed_p_out.txt", "1000000 5 2  4.0051e-03 (4.5e-06)  3.9515e-03  1.014"),
       ("numerics/ae_fixed_p_out.txt", "100 2 1  1.6004e-01 (1.0e-04)  1.7122e-01  0.935")]
for f, t in OUT:
    ok = t in open(os.path.join(HERE, f), encoding="utf-8").read()
    miss += not ok
    print(f"{'OK  ' if ok else 'MISS'}  {f}  {t!r}")
print(f"{len([t for c in CHECKS for t in c[3]]) + len(OUT)} token checks + {nref} range checks, {miss} MISS")
sys.exit(1 if miss else 0)
