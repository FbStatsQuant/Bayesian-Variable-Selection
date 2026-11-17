# W3-D5P — TARGET (one page; v0.1 with STATEMENT v0.1)

## Target clauses (for CP1)
- **T1 (LIST-R (i)).** Theorem 6's data event 𝒢⁺_n carries, for every admissible output run, S₀ ∈ returned list,
  `hpm` = S₀, and the list fields within ε_n = 1 − π(S₀ | y) of the truth and of the exact posterior; `mpm_list` = S₀
  when ε_n < ½. No hypothesis beyond Theorem 6 (+ IMPL-LIST, a code fact).
- **T2 (LIST-R (ii)–(iii)).** Errors O_P(√(log n/n)) on output (p ≥ 2); without "on output" under (D).
- **T3 (LIST-CODE (i)–(ii)).** The two DIST links: completed = output (sampler branch); `hpm` = Ŝ⁺.

## Assumption map (only what this ticket adds; Theorem 6's own map: READER §6 "Why each assumption")
| hypothesis | where it enters | how | necessity reading |
|---|---|---|---|
| Theorem 6 (A1)–(A6) = RM2-R-plus's | LIST-R (i) | only through P(𝒢⁺_n) → 1 | as for Theorem 6; S₀ must be scored for (i), which is Theorem 6's search clause |
| (T1-R) = LSF | LIST-R (ii) | E ε_n → 0 and the rate √(log n/n) (POST (b)) | rate sharp up to √log n for 1 − π(S₀) (W3-POST Thm-1 item 7: 1 − π(S₀) ≥ 1/(1 + √(n+1))) |
| EX-A | all | the fields are computed from exact F | idealisation, as Theorem 6 |
| IMPL-LIST | LIST-R | identifies the printed fields with pip_𝒯, mpm_𝒯, logZ_𝒯 | code fact; open until the method commit |
| (D) | LIST-R (iii) only | delivery (DLV-0) | as Theorem 6's delivery clause |

## Parity table
| clause | (a) PROGRAM goals (design-agnostic within the theorem, p ≫ n, method as coded) | (b) closest published | (c) our best registered result | verdict |
|---|---|---|---|---|
| PIPs from the output on AR / block designs | method as coded, p ≫ n, at the coded budget: **matches** | Song–Liang (2015): sampler statements are limits in the iteration count at fixed data (supplement pp. 9–10, 12–13, 16–17), none at a coded budget | row 3.6: printed sampler PIPs, rate n^{−1/2}e^{C√log n}, **only without leakage (Thm 5's (A5)); AR/BLK not covered** | **beats** 3.6 in scope (AR/BLK) and rate, for a different (list-based) output |
| median model from the output | as above: **matches** | as above | row 3.6: P(MPM wrong ∩ calibration success) → 0, no-leak designs only | **beats** in scope |
| evidence from the output | as above | Del Moral unbiasedness (row 3.5) is not a consistency statement | row 3.5: E Ẑ = Z, any design (unbiased, no consistency); 3.6: |Ẑ/Z − 1| → 0 no-leak only | **new** (deterministic sandwich log Z + log π(S₀) ≤ log_Z_list ≤ log Z) |
| reported model | — | — | row 3.1 | **equal** (re-derived on the same event, jointly) |
| hypotheses | no new hypothesis beyond Theorem 6 | — | row 3.1 | **equal** |
| short rows | the printed sampler averages on AR/BLK: not reached (TRACK_D §5a NO-GO, HQ D86); not a target here | | | named limit, not an item |

## Boundary numerics
None needed for weakened hypotheses (no hypothesis is weakened). Numerics planned (PLAN step 4): brute-force check of
LIST-K on random small Ω, and one end-to-end small case through the real core (sampler branch vs exact enumeration).

## §4 Better-theorem candidates and dispositions
| candidate | disposition |
|---|---|
| Bounds in 1 − π(𝒯 \| y) (sharper than 1 − π(S₀ \| y); numerics show it far smaller at moderate n) | already proved for the PIP-vs-posterior error (LIST-K (b)); not a target for the "vs truth" error, whose scale 1 − π(S₀ \| y) is the posterior's own and is sharp up to √log n (W3-POST Thm-1 item 7); 1 − π(𝒯) is not certified by the output (DIST (C-ii)(β)) |
| The printed sampler averages (`pip_primary`, `mpm`, `log_Z`) on AR/BLK | NO-GO by HQ (D86; TRACK_D §5a): needs a new non-collapse lemma; out of this ticket's scope |
| Corollary 9C's list premise discharged on designs inside both Theorem 9 and Theorem 6 | one-line consequence of LIST-R (i) (π(𝒯) ≥ π(S₀) > ½); proposed to HQ at CP3 (STATEMENT §5 remark 3), not claimed: needs a bridge between the two theorems' hypotheses (no new scope, D106) |
| The rate for p = 1 | omitted (POST covers p ≥ 2); the fixed-t clause holds for every p |
| A binary64 version | out of scope (EX-A, as every theorem of the programme); SPEC §7 acceptance tests cover the numerics |
