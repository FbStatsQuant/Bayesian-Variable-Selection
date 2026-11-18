D3 diff check — STATEMENT.md 1662ba905918bb90; work/D_output/P6_DISTC.md 0b0b1556cfba806b; lemmas/NEC.md 48cb55be4d967f3e; work/D_output/COR_C.md 55d8b14f968de040

Independent mathematical amendment check, reasoning effort high. The brief was read first and in full. All four launch hashes match. Scope: the supplied exact patch, D1-01–D1-04 and D2-01, the requested changelog comparisons, and the additional reported-HPM conclusion of Corollary C, checked against its proofs and the current code. No agents, git commands, cluster jobs or temporary files were used. The small in-memory patch computation ran with nice -n 10. Only this review file was written.

## Findings

None. No CRITICAL, MAJOR, MINOR or NIT finding in the requested scope.

## 1. P6_DISTC.md A-10: D1-01

RESOLVED. The locked [P1] thm:T01i and its change-of-variables proof identify the coded, standardized-response, n-dimensional marginal likelihood as

    m(S) = c_n(s_y) m^c_b(S),
    b = 0.01 s_y²,
    c_n(s_y) = s_y^(n−1) Γ(0.51) / [sqrt(2π·0.01) Γ(0.01)].

This factor is independent of S and strictly positive and finite on a completed run. The contrast likelihood has dimension N = n−1 and variance prior IG(0.51, b). The half-power v^(−1/2) from the n-dimensional working likelihood changes the shape from 0.01 to 0.51 when that likelihood is replaced by the contrast likelihood; it does not disappear.

For every v > 0, the contrast Gaussian likelihood is at most (2πv)^(−N/2). The conditional coefficient prior integrates to one for each v, including the empty-model point-mass convention. With a = 0.51 and b > 0, substitution u = b/v gives

    E_IG(a,b)[v^(−N/2)] = b^(−N/2) Γ(a+N/2)/Γ(a).

Consequently the amended upper bound

    m^c_b(S) ≤ (2π)^(−N/2) b^(−N/2) Γ(0.51+N/2)/Γ(0.51) < ∞

is correct, and multiplication by c_n(s_y) proves m(S) < ∞. Strict positivity follows from a strictly positive likelihood and proper priors. Since Ω is finite and its prior weights are positive, the score normalizer is positive and finite too.

No remaining argument uses the discarded shape-0.01/N-dimensional bound. The shape 0.01 still mentioned in §0 belongs to the working-model prior on the response scale, not the contrast-model prior; its propriety is sufficient for that paragraph's positivity argument. A-10 supplies the finiteness argument there. Lemma U, Lemma W and the subsequent transfers consume positivity/finiteness, not the old numerical bound. No additional hypothesis is introduced.

## 2. STATEMENT.md (C-i): D1-02 and the TC8 tag

RESOLVED. The event at lines 293–295 is now exactly the event in P6_DISTC.md §6 (C-i)(a):

    {completed} ∩ {π(𝒯) ≥ exp(−λt)}
                ∩ {Π̂^𝒯(B_n) ≤ exp(−(c−λ)t)}.

On it, P6(c) with Q = Π̂^𝒯, A = B_n and ε² = C²t/n gives the displayed predictive inequality directly. Neither a stopped run nor a completed run failing the store-mass premise is included. The preceding probability display is unchanged and follows by containment in the DIST-1 bad-data event. The arbitrary-threshold pathwise sentence also remains the proved C-i° statement. The opening “(or (1.2), with its rate)” is read with the rate substitution specified in P6 Remark 6.6: the predictive squared-radius term for that version is C²tℓ_n/n.

EQUAL on TC8: CONFIRMED. TARGET.md §5 explicitly protects the deterministic transfers and requires every delivery statement jointly with {completed} and under its named premise. With this scope, the completion and store-mass qualifications are already required; the new text states the good side of the same conditional transfer. It leaves C-0, the failure bound, its exponent and the rate unchanged. The edit is a literal restriction of the formerly unqualified complement sentence, but that literal complement asserted something outside TC8's stipulated completion/premise scope. I do not classify this as WEAKER on TC8. This confirmation is not a claim of literal equality of the two prose sentences on all outcomes.

## 3. Three split tags and Corollary C

All three split tags are CONFIRMED.

- Corollary C, line 477: EQUAL for the computational-description corrections under the existing exact-arithmetic convention; STRONGER for adding the reported-most-probable-model conclusion to the reader corollary. Derivability from an existing master result does not make an added conclusion EQUAL. The row accurately records both parts. Its HQ go is treated solely as a recorded decision, as instructed.
- Reader Remarks, line 478: EQUAL for the constant bookkeeping and explanatory edits; WEAKER for requiring (A3), (A4) on the window of each selected level M = nε_n²/log n. The current Remark (1), lines 261–263, contains exactly that qualification. The tag correctly distinguishes reduced applicability of the remark from the protected reader displays.
- Bridges, line 483: STRONGER for the B2 implication on all m with min{p,s₀+m} ≤ q, since s₀ ≤ s and m ≤ q−s implies this condition. At q = p the condition is automatic, so the extension includes levels excluded by the old uncapped range. WEAKER for the posterior-defined domain restriction in B0, the positive envelope in B3 and withdrawal of the false uncapped window assertions. The further change from M ≤ sqrt(n) to M ≤ sqrt(n)/log n in the last bridge bullet is explicitly recorded as WEAKER, resolving D1-03. The body at lines 413–414 has the recorded smaller range. These bridge/remark changes do not reduce Theorem A's stated range.

Corollary C's added conclusion: VERIFIED, line by line as follows.

1. Fix a completed final SMC run. If it scored the raw true model, that model has an internal-index representative in Ω: its columns were retained and its size is within the cap. If either condition fails, the antecedent cannot hold. P6 Lemma M, with A-2 and A-8, puts every model scored by this run in the offered set 𝓜. Cache hits and held states were offered when first scored; the final-local-search centre with emit=false was already the running best. The final-run cache starts empty (v3_core.cpp:409).
2. If π(S_true) > 1/2, then for every other S,

       π(S) ≤ 1−π(S_true) < 1/2 < π(S_true).

   Under H-ID, F(S) = log Z + log π(S). Thus S_true has a strict score maximum over Ω. This is exactly P6 Lemma U, and it is the strict inequality needed in COR_C.md C2 and P6 Corollary R1(ii).
3. Under EX-A, scores and comparisons are exact. TopCmp (v3_ledger.h:35–41) and hpm_better (v3_util.h:121–125) use the same order: decreasing F, then smaller size, then lexicographic order. The strict majority prevents a score tie involving S_true; ties among other models do not affect it. Replacing “exceeds 1/2” by “at least 1/2” would require separate tie handling and is not asserted.
4. The top store has positive capacity 40p_ret+1 (v3_ledger.h:78). Its quick rejection, duplicate check, insertion and deletion of the worst entry at lines 49–55 preserve the best offered models. A unique offered global maximum enters and cannot subsequently be evicted. This checks the invariant used by P6 Lemma R and R1(ii).
5. offer_stores sends the same model and score to offer_hpm and top.offer (v3_ledger.h:89–93). offer_hpm retains the first model in the same strict order (lines 84–86). The separate failure-recovery offer_hpm call is inside the NumericalFailure catch (v3_core.cpp:483–502), which sets a non-completed status. It cannot change this argument for a completed run.
6. ledger_to_list serializes hpmS through to_orig into led$hpm$model and serializes the ordered top store (v3_core.cpp:358–366). v3_run.R:142 assigns that model to out$hpm; line 210 returns the top store on the completed path. Thus “reports as most probable” refers to the returned HPM field, not the MPM obtained from marginal inclusion probabilities, nor an exact numerical certificate of the HPM's posterior probability. The raw/internal index map is the same for both returned objects.
7. Hence S_true belongs to 𝒯, is its first entry, and equals the reported HPM. Finally π(𝒯) ≥ π(S_true) > 1/2. This is precisely the conclusion at STATEMENT.md:233–234 and COR_C.md C2.

This verification assumes EX-A and H-ID as the proof does. It does not establish an exact-posterior ordering guarantee for rounded floating-point scores, or assert discovery of the true model.

## 4. Five check-column spot checks

The following five rows reproduce D1's actual verdicts, with their qualifications:

| Current row | Comparison with D1 |
|---|---|
| 1.4 Setup, line 473 | CONFIRMED scoped to TC9, as in D1 Part C and its verdict lines. |
| 1.4 Corollary C, line 477 | Correctly reports that the old EQUAL tag was CONTESTED, the added conclusion is STRONGER, and its proof was valid; it sends the corrected tag to D3. |
| 1.4 DIST-C, line 481 | CONFIRMED scoped to TC8, with the explicit caveat that D1-02 still required SCR-4; the new row accurately records its subsequent application. |
| 1.4 bridges, line 483 | Correctly reports CONTESTED for mixed directions (D1-04) and the unrecorded final-bullet range change (D1-03). |
| 1.4.7 DIST-1(c), line 490 | CONFIRMED EQUAL on TC3; D1 Part A items 1–7 verified the repair. This quotes D1's result, not a new constants review here. |

All five checks pass. The separately requested Remarks row also correctly reports D1's contested old tag.

## 5. NEC §8(d): D2-01

RESOLVED. Let R = {|S| ≤ 4}. The reported families 𝒮₁ and 𝒮₂ consist of models of size 2 and 3, respectively, so each lies in R. Therefore

    π(𝒮_k | y) = π(R | y) π(𝒮_k | y,R)
                ≤ π(𝒮_k | y,R),  k = 1,2.

The new upper-bound wording has exactly the correct direction and no longer asserts that the omitted normalization changes the mass only slightly. The displayed numerical values explicitly use the restricted normalization. The threshold checks are explicitly under the restricted posterior, and the paragraph expressly says that these do not verify the full-posterior event. The full event is attributed to the analytic proof. No remaining inference of the full event or an omitted-mass bound is made from the restricted calculation.

I did not rerun or authenticate the stated 200-draw experiment or its approximate numerical values. D3 verifies the amended interpretation, not those measurements. No part of the Proposition, Corollary, constants or proof is changed by this hunk.

## 6. Exhaustiveness

All supplied current-side hunk contents match the current files. Reversing all supplied hunks in memory gives these first-16 SHA-256 values:

| File | Reconstructed predecessor | Prior review hash |
|---|---|---|
| STATEMENT.md | e8503b045fde127a | D1: e8503b045fde127a |
| work/D_output/P6_DISTC.md | 5e3f9116a9ce9d36 | D1: 5e3f9116a9ce9d36 |
| lemmas/NEC.md | 54340e87b89336a1 | D2: 54340e87b89336a1 |

Thus the supplied patch exhausts the changes relative to the reviewed predecessors. Its three STATEMENT hunks are the version line, D1-02's predictive-event repair, and changelog changes recording D1-03/D1-04 and the earlier verdicts. The P6 hunk is exactly D1-01's finiteness repair. The two NEC hunks are metadata and D2-01's numerical-remark repair. COR_C.md has the unchanged launch hash. No unexplained mathematical change occurs. Apart from the described correction of the finiteness argument and explicit qualification of the predictive sentence, no theorem, lemma, constant or proof step is altered.

Limits: this is an amendment review, not a fresh verification of every unchanged proof line or of the proofs/statuses of consumed results. DIST-1/2/3, Theorem A and H-ID retain their stated inherited status. The locked T01(i) identification, the affected finiteness argument and the requested Corollary C reported-HPM conclusion were checked directly. The empirical values, the HQ decision and code commit identities were not independently authenticated. No required amendment or requested conclusion check remains unperformed within this scope.

## Verdict lines

Item 1 — D1-01: RESOLVED.
Item 2 — D1-02: RESOLVED; EQUAL on TC8: CONFIRMED (not WEAKER on TC8).
Item 3 — D1-03/D1-04: RESOLVED; Corollary C tags: CONFIRMED; Remarks tags: CONFIRMED; bridges tags: CONFIRMED; Corollary C reported-HPM conclusion: VERIFIED.
Item 4 — five quoted D1 verdicts: VERIFIED.
Item 5 — D2-01: RESOLVED.
Item 6 — patch coverage and absence of unexplained mathematical changes: VERIFIED.
work/D_output/P6_DISTC.md — Lemma P6: VERIFIED; Theorem DIST-C: VERIFIED (amendment-check scope, under the stated inherited premises).
lemmas/NEC.md: VERIFIED (amendment-check scope; unchanged Proposition and Corollary proofs not re-reviewed).
STATEMENT.md — DIST-C (C-i): VERIFIED (with the stated rate substitution for the (1.2) version).
STATEMENT.md / work/D_output/COR_C.md — Corollary C: VERIFIED (including the added reported-HPM conclusion, under EX-A and H-ID).
Findings: none; no CRITICAL, MAJOR, MINOR or NIT findings.
Overall verdict: VERIFIED — D1-01–D1-04 and D2-01 resolved; requested tags confirmed; added Corollary C conclusion verified.
