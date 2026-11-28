# Audit audit1-core1-s2: Theory_work/Wave3/API_AUDIT/audit1/REQ_core1.md
claims: core1:B1.SL, core1:B1.IO, core1:B2.SL, core1:B2.IO, core1:B3.SL, core1:B3.IO, core1:B4-UP.SL, core1:B4.IO, core1:B4-LO.SL, core1:B5.SL, core1:B5.IO, core1:B6.SL, core1:B6.IO, core1:B7.SL, core1:B7.IO, core1:DR.SL, core1:SUM.SL, core1:PRIOR.SL, core1:ROW13.SL, core1:SCOPE.IO
stop_reason: max_tokens

## core1:B5.SL

**Problem.** The clause "on smaller sets" is wrong for Thm 2 (A3), and it misses a difference in which sets are quantified. The other clauses stand: fixed against vanishing level, a stronger conclusion, and (for (A4)/(A4′) only) bounded sizes that are eventually below r̄_n + 1.

1. **Sizes and sequences.** Thm 2 (A3) asks a fixed floor on every S with |S| ≤ 5(A+1)(s₀+1) log n (`READER_VERSIONS.md:274–275`). Condition 3 (SL p. 955) quantifies over r̄_n other predictors, so its sets have size r̄_n + 1.
   - SL only require r̄_n ≥ r_n with r_n ≻ 1 (display (12), p. 952; Theorem 2, p. 953).
   - Corollary 1 (p. 954) explicitly admits r̄_n ≺ log^k(n) "for some k > 0".
   - Counterexample: r̄_n = √(log n) is admissible, and then SL's sets are of size √(log n) + 1 = o(log n). Our (A3) sets are then the larger ones.
   - The same holds for the master LSF(ii) sets of size k̄_n = O(log n) (`W3-POST/STATEMENT.md:108–109`).

2. **Which sets.** In Theorem 3 (p. 956) Condition 3 is required only of a true predictor x_t against r̄_n others. Our (A4) and (A3) are "for every S" (`READER_VERSIONS.md:107–108, 274–275`), and the master says its floor "excludes e.g