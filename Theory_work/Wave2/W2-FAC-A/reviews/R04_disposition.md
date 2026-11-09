# R04 disposition (Codex gpt-6.1-sol high; L5–L7: VERIFIED / VERIFIED-WITH-AMENDMENTS, no FATAL)
1. MAJOR (GC-CS minimum over infeasible configurations for bounded p; absolute values): fixed in L5.2 (realised
   configurations, u ≤ min(15, |V| + p − s₀), minimum of absolute values) — same issue as R05 item 3.
2. λ_min(Ψ) ≥ d (equality iff a group of size ≥ 2): fixed.
3. L3 "p + 1 ≤ K": already fixed (R03 item 1).
4. Exact S5 certificate: done (tv_cert_exact.py, Lemma TVF); R04 independently reproduced 2023/32500 and 7/2080.
5. L6 events/margins: (E1),(E2) reused algebraically only; extra Laurent–Massart event; numerator positivity; margin
   (1+2ε). Fixed. Scope strengthening (no p ≤ K needed) recorded in L6 status and to be flagged in REPORT.
6. L7 allocation wording: replaced by the complete Proposition F inequalities + A3 score count. Fixed.
7. fna_check.py large-df branch labelled approximate; "no witness found" wording. Fixed (docstring; outputs unchanged).
