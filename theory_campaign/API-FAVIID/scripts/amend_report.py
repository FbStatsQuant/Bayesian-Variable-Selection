import sys
f = sys.argv[1]; s = open(f).read()
T = "[API-FAVIID]"
subs = [
("# W5-FAVIID — REPORT:", "<!-- Amended copy made by API-FAVIID (synthesis task 9, Part 1) from W5-FAVIID commit 31695b1. Every change is marked "
 "[API-FAVIID] and backed by `results/audit_out.txt` / `results/audit_tails.txt` (scripts in `scripts/`). Mathematical content and status words "
 "are unchanged. -->\n# W5-FAVIID — REPORT:"),
("factor is an artefact (the realised context changes the bound by ≤ 5%).",
 "factor is an artefact (the realised context changes the bound by ≤ 5% in cell medians; " + T + " single designs: Q₀/Q_real outside [0.9, 1.1) in 197/1,200 rows, range 0.31–5.1)."),
("is valid in 1,600/1,600 designs but vacuous at every n ≤ 3,200 in S3/S4/S6.",
 "is valid in 1,600/1,600 designs but vacuous in the median of every S3/S4/S6 cell at n ≤ 3,200 (" + T + " 5/80 S3 designs at n = 3,200 are non-vacuous)."),
("(T_n + 1)Δ_n < 1 holds in 0/56 runs at n ≤ 3,200 and in 3/16 at n = 6,400, and its median is ≈ 1.5 at 12,800.",
 "(T_n + 1)Δ_n < 1 holds in 1/56 runs at n ≤ 3,200 (" + T + " was \"0/56\"; the one run is S3, p = 500, n = 3,200, value 0.997) and in 3/16 at n = 6,400; its median is 1.5 at 6,400 and 1.6 at 12,800 (2 runs)."),
("CONJECTURE (numerics §4.1: realised truth context changes Q̄ by ≤ 4%) |",
 "CONJECTURE (numerics §4.1: realised truth context changes Q̄ by ≤ 5% in cell medians; " + T + " Q₀/Q_real outside [0.9, 1.1) in 16% of single designs) |"),
("**vacuous (> 1) in\n  every S3/S4/S6 cell up to n = 3,200** (medians 10²–10⁵)",
 "**vacuous (> 1) in\n  every S3/S4/S6 cell up to n = 3,200** (cell medians 2.1–7.2·10⁵; " + T + " at n = 3,200 the S3 cell medians are 2.1–149 and 5/80 S3 designs have bound ≤ 1)"),
("is 0.60–0.82 in every cell\n  (Theorem A: E q ≤ 3.83(1+o(1))ξ_n) — the bound holds with a factor ≈ 5 to spare, and q falls like √(log n/n).",
 "has cell medians 0.60–0.82 in every cell with n ≥ 800\n  (Theorem A: E q ≤ 3.83(1+o(1))ξ_n) — the bound holds with a factor ≈ 5 to spare at the median, and q falls like √(log n/n). "
 + T + " q is heavy-tailed: cell *means* of q/ξ_n are 0.65–2.23 (spare factor ≥ 1.7 against 3.83), and 20/1,600 single designs exceed 3.83 "
 "(max 30, S6 p = 1000 n = 1,600). This does not contradict (A1), which bounds E[q 1_𝒢] asymptotically; the sweep does not record 𝒢."),
("δ̂₁ ≈ 0.99·(1 − π₀(S₀)) at n ≥ 3200, so Δ_n is driven by both endpoints equally.",
 "δ̂₁ ≈ 0.99·(1 − π₀(S₀)) at n ≥ 3200 (" + T + " median 0.985, range 0.26–2.19; δ̂₁ sets Δ_n in 24/74 runs), so Δ_n is driven by both endpoints equally. "
 + T + " With the rigorous lower bound δ₁ ≥ u₁/(1+u₁) in place of δ̂₁, the counts in the last column become 0/16, 0/20, 3/20, 4/16, 1/2."),
("is ≈ 6,400 for the best cells (S3, p = 500) and, in median, beyond 12,800.**",
 "is ≈ 6,400 for the best cells (S3, p = 500) and, in median, beyond 12,800.** (" + T + " one S3 p = 500 run already crosses at n = 3,200, value 0.997; both S3 p = 500 runs cross at 6,400.)"),
("Numerically the context changes Q̄ by ≤ 4% (§4.1), so I believe the factor is an artefact.",
 "Numerically the context changes Q̄ by ≤ 5% in cell medians (§4.1), so I believe the factor is an artefact. (" + T + " Single designs vary more: |log(Q₀/Q_real)| has 90th percentile 0.10–0.22 per n and max 1.63.)"),
]
for a, b in subs:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(f, "w").write(s)
print("ok", len(subs))
