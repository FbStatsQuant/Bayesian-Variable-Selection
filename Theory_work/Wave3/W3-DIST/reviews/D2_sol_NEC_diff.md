D2 diff check — lemmas/NEC.md sha256 54340e87b89336a1

Scope: the complete D2 brief, L7's three findings, the supplied patch, the current `lemmas/NEC.md`, and the relevant passages of `STATEMENT.md`. This is a check of the amendments, not a new line-by-line proof review. I additionally read the named snapshot's NEC file with `git show` to verify the patch exhaustively. No other numerical review or experiment was consulted. The small inline calculation ran with `nice -n 10`; no temporary files, agents, cluster jobs, or state-changing git commands were used. Only this output file was written.

## Findings

**D2-01 — MINOR — `lemmas/NEC.md` §8(d), lines 180–183; L7-03 amendment.** The new text correctly identifies the calculation as conditional on `|S| ≤ 4`, but still says “the full-posterior masses are slightly smaller” and reports “the event of the Proposition in every draw for k = 1, 2.” The normalization direction is correct for the reported families, but the size of the difference and the full-posterior event do not follow from the restricted calculation. Put `R = {|S| ≤ 4}`. For k = 1, 2, `𝒮_k ⊆ R`, so

`π(𝒮_k | y) = π(R | y) π(𝒮_k | y, R)`.

Without a bound on `π(Rᶜ | y)`, the restricted values do not establish that the decrease is slight. Likewise, verifying the Proposition's posterior threshold under the conditional posterior does not certify it under the full posterior. For any distance event B, the restricted calculation alone supplies only

`Π(B | y) ≥ π(R | y) Π(B | y, R)`,

not the same lower threshold without the factor `π(R | y)`. The paragraph contains no full normalization or certified omitted-mass bound. Its opening conditional-posterior qualification fixes the original “exact posterior” misdescription, but the remaining full-posterior assertions prevent full resolution as written. This concerns the numerical remark only; it does not invalidate the analytic Proposition or Corollary.

**Minimal repair:** replace “so the full-posterior masses are slightly smaller” with “so these conditional family masses are upper bounds on their full-posterior counterparts”; replace “the event of the Proposition in every draw” with “the corresponding posterior-threshold check under the restricted posterior in every draw,” explicitly stating that this does not verify the full-posterior event. Alternatively provide a certified omitted-mass bound and sufficient numerical slack to justify both assertions. I did not authenticate the reported 200-draw experiment or the exact restricted computations, which are outside this short diff check.

## Hunk checks

| Patch hunk | Verdict | Check |
|---|---|---|
| Version line, current lines 3–4 | RESOLVED | Metadata records v0.2 and the three presentation amendments. |
| L7-01, §0, current lines 21–23 | RESOLVED | Lemma X′ has squared in-sample threshold `Cσ*²tℓ_n`; display (1.2) has population Hellinger threshold `C√(tℓ_n/n)`. The amended sentence distinguishes these correctly and correctly declines to infer a random-design population counterexample from this fixed-design in-sample bound. |
| L7-02, §3, current line 100 | RESOLVED | The false decimal equality is replaced by the exact coefficient and a valid upper bound; the eventual `0.08p` bound remains valid, as checked below. |
| L7-03, §8(d), current lines 180–183 | NOT RESOLVED | The conditional normalization is now explicit, but D2-01 remains. |

## Numerical inequality

At `β = 256`,

`2/√(πβ) = 1/(8√π) = 0.070523697943469535… < 0.0706`.

Here `d = 1 + βL`, `L = log p′`, `p = p′ + 1`, and `ε = 8/√n`. For large n, `L > 0` and `d ≥ βL`, so the integral bound on line 100 indeed yields

`E Ã′ ≤ 1 + (2/√(πβ)) p′ e^(εL) ≤ 1 + 0.0706 p′ e^(εL)`.

Since `εL → 0` and `p′ → ∞`, division by p makes the final upper bound tend to `0.0706 < 0.08`. Thus `E Ã′ ≤ 0.08p` eventually. Explicit sufficient conditions are `e^(εL) ≤ 1.06` and `p′ ≥ 214`: then

`1 + 0.0706 p′ e^(εL) ≤ 1 + 0.074836 p′ ≤ 0.08(p′ + 1)`,

because `0.005164 p′ ≥ 0.92`. Both conditions hold eventually. Markov therefore still gives `P(Ã′ > p/2) ≤ 0.16`.

## Exhaustiveness and statement agreement

The current full SHA-256 is `54340e87b89336a127906b467d3dfbf8230c47234a84d91b0fb118a4747c8896`. All four supplied hunks match the current file exactly. Reversing those hunks in memory yields SHA-256 `c88d10a4555cf0d711d79439ab5df2759ee7101b076c0a9dc0574616e0b337c5`, identical byte-for-byte to `lemmas/NEC.md` in snapshot commit `f0e0d58` and to L7's recorded hash prefix. Thus there is no change beyond the version line and the three specified amendments.

Neither the Proposition nor the Corollary is changed. No design constant, theorem constant, probability guarantee, or proof argument is changed. The sole numerical change within the proof is precisely the requested repair of the intermediate decimal coefficient: the erroneous equality with `0.0705` becomes equality with `2/√(πβ)` followed by the valid upper bound `0.0706`. The subsequent `0.08p`, `0.16`, and `0.6` bounds are unchanged.

`STATEMENT.md` §3, lines 370–377, agrees with `lemmas/NEC.md` §0: the standardised design has `p = floor(√n) + 1`, the null truth satisfies both interfaces for all nonnegative M and M′, and the same fixed-k threshold `(k/24)σ*² log n`, posterior lower mass `c₄(k)/(2n)`, and noise probability `0.6` appear. The cap `K = p` is implicit in the global cap for this dimension at large n. Its consequence concerning failure of Lemma X without (ND), and its fixed-design and in-probability qualifications, agree as well. That paragraph assigns no common radius to Lemma X′ and (1.2), so it does not repeat L7-01. The actual radii in §3 lines 366–368 and §1 display (1.2), line 95, match the amended NEC text.

## Verdicts

Version hunk: RESOLVED.
L7-01 hunk: RESOLVED.
L7-02 hunk: RESOLVED.
L7-03 hunk: NOT RESOLVED.
File as it now stands: VERIFIED-WITH-AMENDMENTS (D2-01; diff-check scope).
Proposition NEC and Corollary NEC: their L7 verification is unaffected by this diff.

Overall verdict: VERIFIED-WITH-AMENDMENTS.
