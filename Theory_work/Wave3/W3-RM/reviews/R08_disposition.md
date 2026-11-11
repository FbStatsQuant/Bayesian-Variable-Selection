# R08 disposition (exhaustive sweep, Codex gpt-6-astra high)

Reviewer reply verbatim: `reviews/R08_sweep_astra.md`. Counts: 0 FATAL, 6 MAJOR, 11 MINOR, 4 EDITORIAL. Reviewer's
conclusion: "None of the FATAL/MAJOR findings refutes or currently breaks (C1) or (C2) as stated under their full
hypotheses and implementation premises"; findings 1-5 concern necessity/sharpness claims around the theorems, finding 6
the citation checker. All 21 findings fixed; none is contested.

| # | sev. | finding (short) | disposition |
|---|---|---|---|
| 1 | MAJOR | ASSUMPTION_MAP called posterior concentration "essentially necessary" | map rewritten (v2): T1 is a sufficient input; necessity not claimed; also SHARPNESS section 5 |
| 2 | MAJOR | "Necessary: \|Q\| < K" / saturation promoted to necessity | removed; FAC-PK now stated as a failing class (existential obstruction for LS0) with its full hypotheses |
| 3 | MAJOR | "not class-sharp" inferred from successful designs | SHARPNESS rewritten (v2) with four separate categories: proved / successful designs outside / failing designs outside / open |
| 4 | MAJOR | nonimplication "(V)+(L) do not imply (N-D)(i)" had no proof | L2_NAF and SHARPNESS section 4 now say "not established from"; the N1 computation is labelled heuristic, with the angle calculation behind 0.40 and 2.5 written out |
| 5 | MAJOR | claimed necessity of path-NA was false | paragraph replaced by the correct statement (NA on deletion children is sufficient, stronger than necessary; path condition in terms of best deletion vs best swap/addition) |
| 6 | MAJOR | citecheck resolver could accept a wrong file | citecheck.py v2: explicit paths preserved, table lookups only for bare/lemmas/cpp names, same-line ticket conflict = failure, ../ relative to the citing file, resolver self-tests, exit code 1 on failure |
| 7 | MINOR | "15": B1/B1' do not prove necessity | SHARPNESS section 1 reworded |
| 8 | MINOR | (V) "route-necessary" overstated | SHARPNESS section 2 reworded |
| 9 | MINOR | Cauchy-Schwarz "route-sharp" overstated | SHARPNESS section 4 and map reworded |
| 10 | MINOR | VN paraphrase dropped (F16) | hypotheses added |
| 11 | MINOR | GEN (C6) application: BM-Q, exact design data, status wording | SHARPNESS section 3.2 rewritten with GEN L7_counterexample:14-36, the floor 1 - a, fixed theta, p = n - 1, K, BM-Q; status states the actual review |
| 12 | MINOR | heuristic converse: range/scaling assumptions | positive part and the assumptions log p/log n -> A, tau/sigma -> 1 stated |
| 13 | MINOR | "l then enters the start mode" unconditional | reworded in L1_fixed |
| 14 | MINOR | c_n undefined in B4 | defined |
| 15 | MINOR | citecheck coverage/exit code | ASSUMPTION_MAP included; backticked continuations parsed, orphans reported UNSUPPORTED; exit code; header says "extracted ranges"; limits stated in the docstring |
| 16 | EDIT. | five citation ranges semantically off | corrected (GROW L1_descent 9-11, 57-61; STATEMENT 40-42, 33-36; APP L5_VN 74-106; FAC-PK REPORT 24-33) and added as token assertions |
| 17 | EDIT. | historical wording | fixed in L1_fixed, L3_SANDR, L3b_rate |
| 18 | EDIT. | informal (D-R) narrower than source | reworded (variance at most one; L_n) |
| 19 | MINOR | `ls0_cap_plus_mode` is an internal field | STATEMENT now names the public option `ls0_cap = "ell_n_plus_mode"` |
| 20 | MINOR | registry map incomplete; IND-T/c4 unused | map v2: all ids, `implies` relations, IND-T/c4 marked as execution conventions |
| 21 | EDIT. | dangling "section REPORT" | pointer fixed |

After the fixes: `reviews/CITECHECK.txt` (v2 checker): 274 extracted citation ranges, 0 failures; 32 token assertions,
0 failures; 8 quoted statuses found verbatim.
