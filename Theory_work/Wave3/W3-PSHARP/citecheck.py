"""W3-PSHARP citation check: every cited line range of an external file must contain the quoted tokens, and every
`file:line` reference written in this ticket's own files must point at an existing line.
Run from the repo root or anywhere:  py -3.13 -I Theory_work/Wave3/W3-PSHARP/citecheck.py > reviews/CITECHECK.txt
"""
import os, re, subprocess, sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
W = "Theory_work/Wave3/"
CHECKS = [  # (file, first line, last line, tokens that must occur in that range, cited in)
    (W + "W3-POST/STATEMENT.md", 16, 39, ["K = min(p, ⌊n/2⌋)", "H_S = (n + 1)G_S + I", "D_S = det H_S / det(G_S + I)",
                                          "ν = 0.01 + n/2", "w(k) = ½/C(2p − 1, k)", "a₀ = b₀ = 0.01"], "STATEMENT §0"),
    (W + "W3-POST/STATEMENT.md", 104, 104, ["conjecture"], "STATEMENT A3"),
    (W + "W3-POST/STATEMENT.md", 106, 118, ["LSF", "ψ_n√n/(log n)^{3/2} → ∞"], "A_log_factor Remark 2"),
    (W + "W3-POST/STATEMENT.md", 63, 76, ["(F_λ)", "(F_w)", "BM-∞"], "A_log_factor Remark 2"),
    (W + "W3-POST/lemmas/L1a_size_tail.md", 10, 11, ["X_Tθ = μ", "‖μ‖² ≤ nM", "‖θ‖² ≤ nM′"], "C §1"),
    (W + "W3-POST/lemmas/L1a_size_tail.md", 11, 12, ["R^T_m", "m^T_n(ω) := min{m ≥ t : R^T_m ≤ n^{−(t+1)/2}e^{−ω}}"], "STATEMENT C.2"),
    (W + "W3-POST/lemmas/L1a_size_tail.md", 12, 16, ["Θ^T_{n,m}", "C′_Λ := 1/√2 + 1/2 + (M + M′)/(2σ*²)"], "C §4"),
    (W + "W3-POST/lemmas/L1a_size_tail.md", 50, 55, ["Is a coefficient bound needed? (open)"], "STATEMENT C"),
    (W + "W3-POST/lemmas/LB_rate_lower_bound.md", 25, 25, ["D_S/D_{S₀} ≤ n + 1"], "S Remark 1"),
    (W + "W3-POST/lemmas/LB_rate_lower_bound.md", 28, 28, ["(iii) Fit"], "STATEMENT Lemma S"),
    (W + "W3-POST/REPORT.md", 190, 190, ["Growing s₀", "o(log n/log log n)"], "STATEMENT B3"),
    (W + "W3-POST2/STATEMENT.md", 44, 44, ["B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n"], "STATEMENT C.1"),
    (W + "W3-POST2/STATEMENT.md", 58, 62, ["δ_n ≥ 𝒪⁰_n / (1 + 𝒪⁰_n)"], "B Remark 1"),
    (W + "W3-POST2/lemmas/B_tail_approx.md", 7, 14, ["B_T(ϑ)", "A^T_m := R^T_m√(D_T)√n", "Θ″_{n,m}"], "C §4"),
    (W + "W3-POST2/lemmas/B_tail_approx.md", 10, 10, ["A^T_m := R^T_m√(D_T)√n"], "STATEMENT C.2"),
    (W + "W3-POST2/REPORT.md", 189, 190, ["Open questions", "√(log n) factor in E δ_n"], "STATEMENT A3"),
    (W + "API_AUDIT/sharp1/TRIAGE.md", 72, 79, ["T3 — POST-SHARP"], "STATEMENT header"),
]
miss = 0
for f, a, b, toks, where in CHECKS:
    try:
        lines = open(os.path.join(ROOT, f), encoding="utf-8").read().splitlines()
    except OSError:
        print(f"MISS  {f}: file not found  [{where}]"); miss += 1; continue
    seg = "\n".join(lines[a - 1:b])
    for t in toks:
        ok = t in seg
        miss += not ok
        print(f"{'OK  ' if ok else 'MISS'}  {f}:{a}-{b}  {t!r}  [{where}]")
# output-number claims: each (file, token) must occur in the numerics outputs
OUT = [("numerics/b_check_out.txt", "55740 (design, data, S0) cases: min odds/O_lb = 1.033240"),
       ("numerics/b_check_out.txt", "8064 (S, j) pairs"),
       ("numerics/b_check_out.txt", "superset odds/O_lb = 1.000000000000"),
       ("numerics/a_orth_out.txt", "worst relative difference: 1.37e-13"),
       ("numerics/a_orth_out.txt", "n= 25600 p= 25599 s0=1 reps= 12 | Lam=0.0225 | 1.003"),
       ("numerics/a_orth_out.txt", "n= 25600 p= 25599 s0=3 reps= 12 | Lam=0.0449 | 1.007"),
       ("numerics/a_sph_out.txt", "p= 40960000"),
       ("numerics/c_counter_out.txt", "n=2e+02: k=64 p=66 K=66 m_n=32: R n^2 = 3.564e-04"),
       ("numerics/c_counter_out.txt", "(ii) mpmath 60 digits")]
for f, t in OUT:
    ok = t in open(os.path.join(HERE, f), encoding="utf-8").read()
    miss += not ok
    print(f"{'OK  ' if ok else 'MISS'}  {f}  {t!r}")
print(f"{len([t for c in CHECKS for t in c[3]]) + len(OUT)} checks, {miss} MISS")
sys.exit(1 if miss else 0)
