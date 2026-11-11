# K-D (line check of D_hellinger.md, gpt-6.1-sol high) — disposition

Verdict VERIFIED-WITH-AMENDMENTS; 0 FATAL / 1 MAJOR / 2 MINOR / 1 NIT. All applied.

| # | finding | action |
|---|---|---|
| 1 MAJOR | D(b) used the per-size bound ‖P_Te‖² ≤ σ*²C_A|T| log n, but (G2) as defined is the uniform O((m+s₀) log n) bound | Event (G2*) (per-size, proved by [P3] line 190, implies (G2), exceptional probability ≤ 1/n unchanged) now part of 𝒢^sup_n in STATEMENT v1.1, A_occam (G3′) paragraph and D(b); all probability accounting unchanged. |
| 2 MINOR | "[T03R] (C8′)" does not exist; need max ∅ := 0 | Cites `A_occam.md` (C8′) replacing [T03R] (C8); max ∅ := 0 added. |
| 3 MINOR | Song–Liang Cor 1 rate needs its branch/hypotheses; d² = 2H² | D4 Remark 1 and ASSUMPTION_MAP qualified (printed p. 954, logarithmic model-size branch, strict sparsity, P_n < exp(Cn^ξ)); normalisation noted. |
| 4 NIT | spurious "+ 2 log n" | Deleted. Also D1 now states (E) explicitly (reviewer's side remark). |
