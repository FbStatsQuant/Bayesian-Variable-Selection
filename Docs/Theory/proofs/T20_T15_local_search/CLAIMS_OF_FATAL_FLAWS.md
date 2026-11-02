# CLAIMS_OF_FATAL_FLAWS.md — T20 (T15) (i)–(ii)

Every fatal or gap finding, verbatim, with the lead's answer.

## Stage A — Astra #1 (session 01a1641e-caed-7313-8c23-8d32e3a413f3), round 1, on PROOF_v1 + STATEMENT v1

### A1-1 (fatal, per the reviewer: "it does not invalidate the formal conclusions in §§3–4")

> 1. **Location:** STATEMENT.md §5, item 1, beginning “If one instead reads it as the last centre…”.
>
>    **Severity:** fatal — this explanatory claim is false; it does not invalidate the formal conclusions in §§3–4.
>
>    **Claim:** The running HPM \(R\) and the last centre \(c_m\) do not differ only in the presence of score ties. Unique attainment of the largest scored value does not ensure that they coincide.
>
>    **Evidence:** Take \(p=1\), \(n=3\), hence \(K=1\), with
>    \[
>    \mathcal S^-=\{\varnothing\},\qquad \ell=0,\qquad
>    F(\varnothing)=0,\quad F(\{1\})=1.
>    \]
>    Scan \(0\) scores \(\{1\}\) and stops with LIMIT. The last centre is \(c_m=\varnothing\), whereas \(R=\{1\}\). There are no score ties, and the scored maximum is unique. More generally, (i-d) itself establishes \(F(R)>F(c_m)\) on every LIMIT outcome. Thus the explanatory sentence contradicts a formal claim that the proof correctly establishes.

**Lead's answer: accepted and fixed.** The sentence in the readings section was wrong: on LIMIT, R ≠ c_m always. It was an explanatory remark, not one of the claims of §§3–4, and the proof never used it. STATEMENT.md §5 item 1 now reads: on LIMIT, R ≠ c_m but the flag is 0 under both readings (c_m has a strictly improving neighbour); on NOIMP, R = c_m unless another scored model has exactly the score F(c_m) and precedes c_m in the HPM order; so the two readings give different flag values only on NOIMP with such an exact tie. (Check: under the "last centre" reading the flag is 1 iff NOIMP; under the adopted reading it is 1 iff NOIMP and R = c_m, by (i-a).)

### A1-2 (gap)

> 2. **Location:** PROOF_v1.tex, “Clause (ii), margin and statistical parts,” lemma labelled `lem:finite`, proof for nonempty \(S\).
>
>    **Severity:** gap.
>
>    **Claim:** The asserted lower bound on \(Q_S\) is not justified by definitions supplied in the permitted files.
>
>    **Evidence:** The proof establishes
>    \[
>    n z_S^\top H_S^{-1}z_S\le \frac{n}{n+1}y^\top y
>    \]
>    and immediately concludes
>    \[
>    Q_S\ge \frac{y^\top y}{n+1}\ge0.
>    \]
>    However, neither supplied text defines \(Q_S\) for nonempty \(S\), or states an identity connecting it to the preceding quadratic form. Only \(Q_\varnothing\) is defined. Consequently this implication, and therefore this particular derivation of positivity of the displayed marginal likelihood, cannot be verified from the permitted files. The identification of those detailed formulas with the method’s marginal likelihood also relies on an external source whose contents are not supplied.
>
>    This is an auxiliary derivational gap: the stated setting already assumes a real-valued score, and the subsequent posterior-odds calculation is correct.

**Lead's answer: accepted and fixed.** The packet lacked the definition. STATEMENT.md §1 now writes out the method's score in full, copied from 00_COMMON §1 and METHODOLOGY_v3 §5: G_S, z_S, H_S, D_S, Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, ν, m(S), w, W_K, ϖ. It also says the proof uses only these displayed formulas. PROOF_v2's Lemma (finite) now cites that definition explicitly at the step Q_S ≥ yᵀy/(n+1). The identification with a Bayesian marginal likelihood is not used anywhere in the proof; the formulas are the definition of the score.

Astra #1 round 2 (same session, on PROOF_v2 + STATEMENT v2 + this log): agrees with both answers ("I agree with the answer and confirm that the fix works" for A1-1 and A1-2); no new findings; verdict **verified** (review/astra1_r2.md). End of Stage A; proof candidate = PROOF_v2.

## Stage B — Astra #2 (fresh session 01a16424-4661-7c72-9494-a9613c43944d) and Opus 5.5 xhigh reviewer, round 1, on PROOF_v2 + STATEMENT v2 (change log removed from the packet copy)

**No fatal or gap findings.** Astra #2: verdict verified; one remark (the inner-probability parenthetical in (ii-C)3 is unnecessary; kept, harmless). Opus: verdict verified; findings F1–F10, all exposition or scope (review/astra2_r1.md, review/opus_r1.md).

Lead's handling of the exposition/scope findings (unified revision PROOF_v3 + STATEMENT v3; no hypothesis or claim content changed):
- F1 accepted: (ii-C)3 and proof step 3 now name EX-A and EXEC.
- F2 accepted: (i-b) now says the F′-run uses ≻ and the move order computed from F′ with the same fixed tie-break rule (the proof already did this via τ).
- F3 accepted: (i-b) "does not certify global maximality" now qualified by Ω ∖ 𝒮_end ≠ ∅, with the trivial 𝒮_end = Ω case noted (statement and proof).
- F4 accepted: (i-a) now states that every equal-score neighbour N of a certified R satisfies R ≻ N.
- F5 accepted: proof §1 shows 𝒩(c) ≠ ∅.
- F6 accepted: proof (ii-C) takes C ≥ 1 (so log(2C) > 0).
- F7 accepted: "from the moment scan k scores S₀" (statement and proof).
- F8 noted (scope): (i-c) holds by construction of the formal model; the link to the method is now quoted verbatim in STATEMENT §0 (METHODOLOGY_v3 §6.10 and §6.1).
- F9 partly addressed: the source's E_n definition and the method's §6.10 text are now quoted verbatim in STATEMENT §0; H03 remains an explicit hypothesis (T03 is a conjecture being proved in a sibling thread), as the statement says.
- F10 accepted: §5 item 5 now mentions the tie-only route (NOIMP with an equal-score neighbour preceding c_m), covered by (i-a).

### Stage B ruling round (on PROOF_v3 + STATEMENT v3 + this log)

- **Opus reviewer (r2): verified.** Agrees with every answer in the log; each change works. New findings N1–N3, exposition only (review/opus_r2.md).
- **Astra #2 (r2, same session): verified.** Agrees with every answer (table of rulings); one exposition finding, the same point as Opus N1 (review/astra2_r2.md).
- Lead: N1 (= Astra #2's point) and N2 accepted, fixed in STATEMENT v3.1 (§5 item 5 and §1 text only; proof unchanged). N3 (measurability of E_n via a.s. continuity of standardisation) noted; harmless, both reviewers agree; not applied, to keep the reviewed proof text final.
- No fatal or gap finding is outstanding. No dispute; Astra judge not used.
