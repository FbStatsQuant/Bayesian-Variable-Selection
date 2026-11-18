# W3-FAMC — R1 disposition (lead, Claude Opus 5.5 high; 2026-11-17)

Inputs: `reviews/R1_linecheck_sol.md` (gpt-6.2-sol, codex, high; round=R1; commit 4bb2b603; ACCEPT WITH CHANGES, 1 MAJOR +
10 MINOR) and `reviews/E2_check_opus_R1.md` (claude-opus-5-5, high; OVERALL: PASS). Sol's verdicts were treated as input.
Each point was triaged against the acceptance filter (genuine flaws only, no nitpicks, probability-zero caveats do not
block). Result: **11/11 ACCEPT**, no false positive, and no point relied on a null-set caveat.

| id | sev | triage | why genuine | fix (STATEMENT v1.2 / A_assembly v1.1) |
|---|---|---|---|---|
| S1 | MAJOR | ACCEPT | §1R overclaimed: "aligned signs" in words is false for ρ < 0 (θ = (1, 2) adjacent at ρ = −½: 1 + 2(−½) = 0); delivery stated without (S4); setting omitted; X undefined in §0 | §0 defines X ([NOT] :31-35); §1R rewritten: §0 setting, sign alignment per design, separation by reference, B by reference, (S4) split |
| S2 | MINOR | ACCEPT | owner rule (readable from the statement): B was only cited; "null" is false without finitely many patterns (Sol's dense-correlation example); "excluded: vectors on B" overstated (sign routes can cover vectors on B) | B defined in (BLK-g); nullity scoped to finitely many patterns (VIS-c,d); §1b(i), §5 restricted to the generic routes; §2 wording |
| S3 | MINOR | ACCEPT | brief asks a class per assumption; inherited premises and (S4) had none | §2 rows for (S1)–(S4), with pointers to ASSUMPTION_COMPLIANCE.md (theory/W3-AUDIT @0211dca4, lines 20, 38, 42–44) |
| S4 | MINOR | ACCEPT | signed lower bound false for θ*_j < 0 (proof file was right) | §3 B.V1: identity, then bound on |·| |
| S5 | MINOR | ACCEPT | (P4)'s "0 ≤" holds for the flipped vector, not W at ρ < 0 | magnitude bound; σ-field remark; ρ = 0 case (both files) |
| S6 | MINOR | ACCEPT | TB B9 has the route, not the cross-group computation | cite A_assembly B.0; B9 for the route |
| S7 | MINOR | ACCEPT | pointer missed the N_l definition and (0.1) | [L6] :75-84, :97-100, :233-236 |
| S8 | MINOR | ACCEPT | the block cap also enters the floor sets and the method's partition | §1b(ii) reworded |
| S9 | MINOR | ACCEPT | "covered through E2's class" false for ρ_n → ±1 (2×2 floor 1 − |ρ_n| → 0) | clause dropped |
| S10 | MINOR | ACCEPT | failure of no-leakage overstated (ρ = 0; truth–truth block-mates) | qualified: null–truth covariance bounded away from 0 |
| S11 | MINOR | ACCEPT | "no finite-n statements" contradicts the every-n ≥ 3 delivery clause | limited to finite-n recovery guarantees |

**E2 check (DP1).** PASS: no gap. Three wording notes on RM2/LOC2 files (`L6_poly.md:106`, `L6_examples.md:76-84`,
`L6_examples.md:164-166`) are reported to the manager for W3-RM2, not edited here. STATEMENT §4 records the AR half as
unconditional (HQ DP1).

Citecheck after the fixes: 93 checks, 0 failures. Next: diff round R2 (Sol, gpt-6.2-sol, high) on the v1.1 → v1.2 diff.
