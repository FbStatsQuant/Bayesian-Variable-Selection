# R06 disposition (exhaustive sweep, Codex gpt-6.1-sol high): 0 fatal, 3 major, 7 minor, 5 editorial — all fixed

| # | Sev. | Item | Fix |
|---|---|---|---|
| 1 | major | SL's β₀ is a no-intercept minimiser; equals our slope-with-intercept only after centring | STATEMENT §0, §2(iii) and L2 P(b), GD(a) qualified ("for centred rows"; the reviewer's x, z ~ N(1,1) example quoted in L2) |
| 2 | major | SL scope statements lacked Condition 4 / prior setting / full-model qualifications | STATEMENT §0 summary and §5 "Outside GR" replaced by the reviewer's wording |
| 3 | major | Onset 2·10⁶ wrongly exported to all results | STATEMENT §6 and L1.2 remark (b) replaced: thresholds depend on the stated constants; the illustration is not transferred |
| 4 | minor | E1 coordinate mixing | already fixed via R05 (raw and standardised forms) |
| 5 | minor | null-projection parenthesis | already fixed via R05; wording aligned to the sweep's ("aggregate slope vanishes; may result from cancellation") |
| 6 | minor | GD(b) starting index depends on s | n₀(s, A, c₀, C₀, M₀) |
| 7 | minor | "detection needs" upgraded sufficiency to necessity | L4.7: "the sufficient beta-min condition established here uses …"; no lower bound claimed |
| 8 | minor | N5 "slower" unsupported | L5 §4 replaced by the reviewer's wording |
| 9 | minor | one-factor example: dense γ ≠ dense support | L2 remark qualified (null loading candidates → ∞) |
| 10 | minor | §1 heading overclaims | renamed "A nonzero residual outside the unrestricted candidate span requires rank X_𝒞 < N" |
| 11 | editorial | stale status headers | per-claim status headers in L1–L6 (the rewrite briefly dropped L3's inputs/notation, L4's references, L1's and L6's one-line notes; restored) |
| 12 | editorial | Theorem F cited "(ii)–(iii) of MIS (i)" | conclusions listed explicitly (T03R (ii)–(iii)) |
| 13 | editorial | unescaped bars in 00_MAIN table | escaped / rewritten |
| 14 | editorial | 𝒪 used for omitted set and output event | omitted set renamed 𝓜 in STATEMENT §§1–2 and L2; 𝒪 kept for the output event |
| 15 | editorial | "bounded convergence" in L3 | replaced by E Y_n ≤ η + P(Y_n > η) |
