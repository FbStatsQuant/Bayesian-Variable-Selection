# ERRATA — editorial findings for one later batch (PROTOCOL_v4 §5.3: E findings never block; applied together later)

From council R1 (`reviews/R1_council_opus.md`, `reviews/R1_council_sol.md`). Items in files that changed for the diff
round (T2, T8, T9) were applied there; the rest wait here, so the accepted items T1, T3, T10 stay byte-identical.

| # | source | file | item |
|---|---|---|---|
| ER-1 | Opus E1 | T10 STATEMENT, claim header | Open the claim with "Under the inventory's (d)-premises EX-A, IDEAL-W, MACH (for X9 alternatively TDP_E's (H2-FP)), on valid declared inputs: …"; optionally note that X9 is unreachable in binary64 as well (`mb` never NaN, M[J][0] = 0). |
| ER-2 | Opus E4 | T1 PROOF header | Add "v4 → v5: SL1LC2 #1 applied". |
| ER-3 | Opus E4 | T3 STATEMENT header | Bump to v2.1 (changelog row v2.1 exists). |
| ER-4 | Opus E4 | T10 PROOF header | "v2.1" → "v2.2" to match STATEMENT v2.2 (exact X7/X8 bound). |
| ER-5 | Opus E5 | T1 STATEMENT, Not claimed | Add: signals and user interrupts, incl. `Rcpp::checkUserInterrupt()` in exact enumeration (`cpp/v3_core.cpp:552`): MACH / INVENTORY X4; outside 𝒪, no clause affected. |
| ER-6 | Opus E6, Sol #4 | T3 STATEMENT (W3-RM:E4 status) | Point the quoted status to `STATUS_EXTRACT.md` (added in R1d). |
| (done) | Opus E4 | T2 STATEMENT changelog order | applied in v6 (rows reordered). |
| (done) | Opus E2, E3 | T8 | applied in v4 (with Sol #2). |
| (done) | Opus E4 | T9 header | applied in v3. |
| (done) | Opus E6, Sol #4 | T8 status quotes | `STATUS_EXTRACT.md` added; T8 points to it. |
