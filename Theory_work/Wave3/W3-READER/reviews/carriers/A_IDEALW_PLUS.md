# A:IDEAL-W⁺ — definition text (for `Theory_work/INFRA/registry/assumptions.tsv` and the 17-claim batch, verbatim)

Prepared 2026-11-16 05:47 CST by the Theory Dept implementation sub-agent (Claude Opus 5.5), per HQ's form decision.
Sources: HQ's definition; TR1 §2 (`Theory_work/Dept/research/FUNI_transfer/TR1_sol.md`); code as on origin/main
(`Scripts/SMC_BVS/core/v3_run.R:95-97`, `Scripts/SMC_BVS/core/cpp/v3_core.cpp:473-474`). IDEAL-W itself
(`Theory_work/Wave1C/C-DLV/STATEMENT.md:24-25`) is **not** changed; A:IDEAL-W⁺ is a separate, stronger assumption.

## Definition (cite this paragraph verbatim)

**A:IDEAL-W⁺ (IDEAL-W with the two LS0 cap ceilings lifted).** IDEAL-W, exactly as defined in C-DLV `STATEMENT.md:24-25`, and the two shipped rejection predicates `le > 10⁶` (`Scripts/SMC_BVS/core/v3_run.R:96`, the LS0 base-cap validator; le = ℓ_n = ⌈log₂(n + p + 1)⌉ in the shipped configuration) and `ℓ + |S̃₀| > INT_MAX` (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`, the disjunct `cap_ll > numeric_limits<int>::max()` of the LS0 cap-range guard, `int` read as unbounded) are false. Nothing else is lifted: the other conditions of those two validators (numeric type, length, finiteness, integrality, `le < 0`, `o.ls0_ell < 0`), every other validator, the 10⁶-maximiser start-mode enumeration cap with its tie-aware DP fallback, and every fallback and method cap are kept as coded. Like IDEAL-W and EX-A, A:IDEAL-W⁺ is an idealisation of the machine and code; a larger allocation does not imply it.

## Proposed assumptions.tsv row (columns: id, kind, shared, name, statement, source, implies, bridge, version, notes)

| column | value |
|---|---|
| id | `A:IDEAL-W+` (display A:IDEAL-W⁺) |
| kind | assumption |
| shared | yes |
| name | IDEAL-W with the two LS0 cap ceilings lifted |
| statement | the paragraph above, verbatim |
| source | `Theory_work/Dept/research/FUNI_transfer/TR1_sol.md` §2 (and this file) |
| implies | — (it contains IDEAL-W, which has no separate row; IDEAL-W sits inside A:DELIVERY-ALLOC) |
| bridge | — |
| version | 1.0.0 |
| notes | Without it, statements that use it hold on the sufficient bounded domain 𝔇 := {(n, p_raw): ⌈log₂(n + p_raw + 1)⌉ ≤ 10⁶ and ⌈log₂(n + p_raw + 1)⌉ + ⌊n/2⌋ ≤ 2³¹ − 1}. Both predicates are false there, because p ≤ p_raw and \|S̃₀\| ≤ K ≤ ⌊n/2⌋, and the exact-enumeration branch reaches neither check (TR1 §2). 𝔇 is sufficient, not necessary. This is the same assumption as W3-RM2-R's IDEAL-W⁺ (`Theory_work/Wave3/W3-RM2-R/STATEMENT.md:80-85`); that file says the two bounds are treated as satisfied (the rejection predicates `le > 1e6`, `cap_ll > INT_MAX` never fire), the reading of TR1 §2. First users: W2-UNI:F-UNI@2.0.0 clause (b), W3-RM2-R:DLV-0. |

**Wording note for the batch:** the code ceiling is `numeric_limits<int>::max()` = 2³¹ − 1 on the shipped platform. "INT_MAX" in
the paragraph means that value. The predicate fires on cap_ll = `ls0_ell` + |S̃₀|; under the shipped configuration (`ls0_cap`
= "ell_n_plus_mode", `ls0_ell` = ℓ_n), that is ℓ_n + |S̃₀|.
