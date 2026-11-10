# R07 — independent exhaustive final sweep

Reviewed: STATEMENT v3.2; L1–L7; CODE_CHECK; ASSUMPTION_MAP; PROGRAM item 5 and PROTOCOL; all nine requested production source files. Reviewer: GPT-6 Astra, high. No subagents, state-changing git commands, production edits, or simulation workloads were used. All paths below are relative to the repository root; abbreviated theory paths are relative to `Theory_work/Wave3/W3-SCR/`.

## Overall assessment

The principal theorem package survives this sweep: I found no counterexample or missing probabilistic step in SCR-A, SCR-A°, SCR-M, their stated asymptotic corollaries, the bridge lemmas, EC′, SCR-C, SCR-R, or SCR-N. The important constants and the code-to-certificate/ledger implications check out. Nevertheless, the full package is not yet clean enough for an unqualified final sign-off: the assumption map contains false mathematical assertions and incorrectly labels sufficient conditions as necessary, including an explicit counterexample to its identifiability claim. There are also residual overstatements, one matrix/scalar notation collision, and documentation/interface defects. These require document repairs, not a redesign of the main proofs. Findings were formed independently before consulting prior-review dispositions; those dispositions were consulted only afterward. In particular, finding 5 identifies a remaining ridge issue in the already revised R06 wording, rather than reopening the previously fixed missing-strong-truth issue.

## Counts

| Severity | Count |
|---|---:|
| BLOCKER | 0 |
| MAJOR | 3 |
| MINOR | 9 |
| NOTE | 0 |
| Total | 12 |

Severity refers to the full requested package. The three major findings concern false assertions in ASSUMPTION_MAP, not failures of the named screening theorems.

## All findings

### 1. MAJOR — ordinary span containment does not make ridge visibility zero

**Location/quote:** `ASSUMPTION_MAP.md:19`, size row: “Γ_n(q) is 0 once q columns can span the missing mean”.

**Problem:** This replaces the positive-definite ridge residual operator by an orthogonal residual projector. The asserted implication is false at finite n. In particular, Δ_n(q)=0 does not imply Γ_n(q)=0.

**Counterexample/derivation:** Take n≥4, p=2, q=1, x_1=x_2=x with g=‖x‖²=n−1, S₀={1}, θ*_1=b≠0, and λ=1/(n+1). The missing models are ∅ and {2}. At S={2}, Δ(S)=0, but R_S x=λx/(g+λ), and

`γ(1|{2}) = b² g² λ / ((g+λ)(2g+λ)) > 0`.

The empty-model gain is also positive, so Γ_n(1)>0. This example lies in the permitted q≤K−1 range and explicitly uses an allowed duplicate column.

**Concrete fix:** Replace the assertion by “ordinary span containment makes Δ_n(q)=0 and invalidates a positive directional-floor bridge; ridge visibility need not be zero.” Do not infer an exact zero ridge gain from zero projection residual.

### 2. MAJOR — identifiability/directional floors are not necessary for the package's pointwise screening conclusion

**Location/quote:** `ASSUMPTION_MAP.md:15`, ID row: “**Yes**: Δ(S) = 0 … makes S₀ non-identified”, flag “necessary”; `:17`, AF/DF row: “DF = 0 … non-identified”, flag “necessary up to constants”; outcome item 2, “Necessary / sharp: … an identifiability margin”.

**Problem:** Nonidentifiability prevents a uniform support-identification guarantee over observationally equivalent parameterisations. It does not establish necessity for a fixed-parameter, possibly vacuous, statement that every LO model of size ≤q contains S₀. The distinction matters here because the package explicitly allows s₀>q and redundant true columns.

**Counterexample/derivation:** Let p=s₀=2, q=1, n→∞, x_1=x_2=x, θ*=(B/2,B/2), with fixed B>σ>0. Then μ=Bx, Δ_n(1)=φ^a_n(1)=φ^d_n(1)=0. Nevertheless every missing model of size ≤1 has an improving addition with probability tending to one. The empty model gains order n by adding either column. At either singleton, the prior ratio for adding the other column is exactly one. With g=n−1 and λ=1/(n+1),

`D = (2n²−1)/(n(2n−1)),  n log D → 1/2`,

`g_{y_c}(2|{1}) = (B²/(2n))(1+o_P(1))`,

and `(0.02 τ̂² + q_{ {1} }(y_c))/n → σ²` in probability. L1.4 therefore gives

`n [F({1,2})−F({1})] → (B²/σ²−1)/4 > 0`.

The same holds for {2}. Thus there is no LO model of size ≤1 with probability tending to one, and the precise screening conclusion holds despite zero ID/AF/DF. This is an admissible, intentionally vacuous screening conclusion of the kind §3 allows. It refutes the unconditional “necessary” labels, not the bridge lemmas.

**Concrete fix:** Label ID/AF/DF as sufficient bridge properties. State separately that identifiability is required for uniform exact support identification over an explicitly specified parameter class. Retain the valid statement about observational equivalence without converting it into necessity for this certificate theorem.

### 3. MAJOR — the claimed quantitative necessity “nΔ must dominate log p” is unsupported and not scale invariant

**Location/quote:** `ASSUMPTION_MAP.md:15`: “quantitatively nΔ must dominate log p”.

**Problem:** Δ is already defined as squared mean energy, not energy per observation; the map provides no result establishing this necessity. More decisively, the displayed condition omits σ although Model G permits σ=σ_n.

**Counterexample/derivation:** Start with any fixed-p≥2, orthogonal, fixed nonzero coefficient sequence satisfying A1, and multiply θ* and σ by a_n=n^−2. The law of the standardised response, every score, every certificate comparison, and the screening probability are unchanged. Both sides of MC scale by a_n, so SCR-A still applies. But originally Δ_n(q) is of order n for q≥s₀ in an identifiable fixed-p example, whereas after scaling it is of order n^−3. Consequently nΔ_n(q)/log p→0 while screening holds. This also works directly using (A∞), whose ratio is unchanged by the scaling.

**Concrete fix:** Delete the necessity sentence. If a quantitative information-theoretic claim is desired, state a separate result with Δ/σ², its parameter class and entropy, and a proof. B1 gives a sufficient visibility bound involving Δ and coefficient norms, not the asserted necessary rate.

### 4. MINOR — the opening proof sketch omits the positive part and the event qualifier

**Location/quote:** `ASSUMPTION_MAP.md:3-5`: “observed one-step gain is ≥ (√γ(t|S) − σ b)²”.

**Problem/derivation:** A lower bound on an absolute value by a negative number cannot be squared. For γ=0, the printed right side is σ²b²>0, while the observed gain can be arbitrarily close to zero, including on the noise-control event. True-column cancellation with μ=0 is expressly permitted by Model G. Moreover the gain bound is probabilistic, not unconditional.

**Concrete fix:** Write “on the stated noise event, the unstandardised gain g_{y_c}(t|S) is at least (√γ(t|S)−σb)_+².” L7 already proves exactly this correct form. Under MC the bracket is positive, but SCR-M itself does not assume MC or gap positivity.

### 5. MINOR — included true coefficients still contribute through ridge shrinkage

**Location/quote:** `STATEMENT.md:95-96`: “truths already in S do not raise the bar for the missing ones”; `ASSUMPTION_MAP.md:14`: “truths already in S do not raise the bar”.

**Problem:** R_S is not I−P_S, so even included signal contributes to μᵀR_Sμ and can affect the gain. The R06 repair correctly distinguished missing strong truths, but left this separate ridge issue unresolved.

**Counterexample/derivation:** Take orthogonal standardised x_1,x_2, S={1}, μ=A x_1+b x_2. Exactly,

`σ_S² = σ² + b² + A²/n²`,

because R_Sx_1=x_1/n² and R_Sx_2=x_2. Increasing the coefficient of the included truth increases the residual scale. There is no bound on A in the nonasymptotic theorem; A=n already contributes one unit. The term involving τ̄_n² in ϑ° also retains total-signal dependence.

**Concrete fix:** Say that included signal is substantially attenuated, rather than removed, and identify the remaining ridge contribution. No change to SCR-A° or its proof is required.

### 6. MINOR — equality Q_S=n−1 is not exclusive to the empty model

**Location/quote:** `ASSUMPTION_MAP.md:14`: “only at S = ∅ is Q_S = n−1”.

**Problem/derivation:** Since H_S is positive definite, Q_S=n−1 iff z_S=0. A nonempty S with X_Sᵀy=0 also has equality; centred orthogonal vectors provide an immediate deterministic example. For any fixed nonempty S this is a null event under nondegenerate Gaussian noise, but the printed sentence is an algebraic exclusivity claim with no almost-sure qualifier.

**Concrete fix:** Write “at S=∅, Q_S=n−1 identically; other models can have smaller residuals.” Alternatively state the almost-sure version explicitly.

### 7. MINOR — G_S is simultaneously a Gram matrix and a scalar lower gain

**Location/quote:** `STATEMENT.md` §0: “G_S = X_SᵀX_S”; `STATEMENT.md:106` and `lemmas/L7_master.md:23`: “G_S := (√γ(t|S) − σ b_𝓗(x))₊²”.

**Problem:** The second definition silently reuses a foundational matrix symbol for a scalar. L7 also invokes earlier identities expressed using the Gram matrix. Dimensions let a reader reconstruct the intended meaning, but the package does not have a consistent symbol dictionary.

**Concrete fix:** Rename the scalar to `g_S^−` or another unused symbol throughout SCR-M and L7, including u_S and M3/M4. Preserve G_S for the Gram matrix everywhere.

### 8. MINOR — assumption ID SV(q) has incompatible finite-sample and asymptotic meanings

**Location/quote:** `STATEMENT.md:233`: “SV(q) sparse visibility with margin MC”; `ASSUMPTION_MAP.md:12`: “SV(q) … √Γ_n(q) ≥ (1+δ)(τ_n√(2 log p + log n) + σ√(2q log p))”, with entry point “L3 Claim”.

**Problem:** The table uses an undefined δ and no “eventually” quantifier. It states an asymptotic surrogate using log p/log n rather than the finite-sample MC(q,x) involving T_n, N_q and x. L3's claim consumes MC, not the displayed surrogate at arbitrary n and x. This undermines the shared assumption-ID interface required by PROTOCOL item 5.

**Concrete fix:** Use MC(q,x) as SV(q,x), matching §4. Add a separately named asymptotic condition with “some fixed δ>0, for all sufficiently large n”, and cite the (A∞) proof for its implication with x_n=√log n. Include SV° in the map as a distinct interface condition rather than only mentioning it in other rows.

### 9. MINOR — the sharpness summary promotes a sufficient near-orthogonality condition to necessity

**Location/quote:** `ASSUMPTION_MAP.md`, outcome item 2: “Necessary / sharp: … some near-orthogonality for exact recovery”.

**Problem:** The NF row itself correctly says “The floor is sufficient, not shown necessary”. The counterexamples establish that arbitrary correlated designs cannot all be covered without further conditions; they do not establish necessity of near-orthogonality. EC′ explicitly uses conditional lengths and dual-direction dependence, which need not be described by a near-orthogonality floor. If q≤s₀, screening alone already yields the exactness conclusion, without any exclusion of strict supersets to prove.

**Concrete fix:** Replace the summary by “exact recovery in general requires additional control of possible LO strict supersets; NF is one sufficient condition, and its constant is not shown necessary.” Do not place near-orthogonality itself under “Necessary / sharp”.

### 10. MINOR — the tie-change explanation overstates when the top-level flag is false

**Location/quote:** `CODE_CHECK.md:41-42`: “an exact-F tie that moves the HPM away from the scanned centre leaves the flag FALSE”.

**Problem/derivation:** The per-search certification contribution is false when the HPM differs from that search's endpoint. The top-level flag is the OR of final-search and LS0 contributions. Thus `hpm != final$returned`, `hpm == ls0$returned`, and `ls0$local_certified == TRUE` gives TRUE even though the final centre was displaced. The explanation fails to specify which flag/centre it means. The actual CC2 implication and the code are correct.

**Concrete fix:** Say “a displaced centre's certificate does not transfer to the HPM; the top-level flag requires one of the certified archives to return the HPM itself.” This also matches the careful caveat already in SCR-G(ii).

### 11. MINOR — the “same setting except” citation omits a real change in the noise hypothesis

**Location/quote:** `STATEMENT.md:17-18`: “This is the setting of … s1_setting.tex:7-24, except that s₀ and p are not restricted”.

**Problem:** The cited source's Model G at line 7 explicitly has σ²>0 **fixed**; this ticket permits σ depending on n. That extension is legitimate and is handled correctly by the scale-relative proofs, but the exception list is inaccurate.

**Concrete fix:** Add varying σ_n>0 to the list of departures from the chapter setting. This is a citation/description correction, not a missing theorem assumption.

### 12. MINOR — unescaped vertical bars break the assumption-map table

**Location/quote:** `ASSUMPTION_MAP.md:17` contains “|T| ≥ 2” and “|T| = 1” inside a table cell; `:19` begins “| **size |Ŝ| ≤ q_n** |”.

**Problem:** In GitHub-flavoured Markdown these literal pipes are table-cell delimiters. The AF/DF and size rows therefore acquire extra cells, shifting or dropping the entry-point, necessity and flag text. This is especially undesirable in the document meant to distinguish sufficient from necessary assumptions.

**Concrete fix:** Escape all within-cell vertical bars (`\|T\|`, `\|Ŝ\|`, etc.), or use `card(T)` notation. Check the full table for every within-cell pipe, including later occurrences in the size row.

## Results completely checked and found mathematically correct

The following is a positive verification ledger, not a claim that the separate prose defects above are harmless. All results are read under Model G and EX-A, with the explicitly stated size/family restrictions and common retained-column coordinates.

1. **L1.1–L1.7, including L1.5°.** Re-derived the ridge variational identity, Schur complement, rank-one update, augmented representation, prior ratio and determinant bounds. The sufficient addition threshold is exactly `T_n=(n+1)/n [2 log(2p−1)+log(n+1)]`; the strict improvement follows despite a weak ≥ threshold. The deletion inequality uses `log(1+u)≤u` in the correct direction. The identities hold for singular/duplicate columns because λ₀>0. The empty model uses the usual zero-dimensional determinant/inverse convention.

2. **L2 E1, E4, E2±, E2chi, E3a, E3b.** Checked Gaussian variances, deterministic witnesses, centring, rank domination and every union count. E1 costs e^−x, E2+ costs 2e^−x, E4 costs at most e^−x; E2chi plus E3a costs `(1+2q)e^−x`. E3b costs `Σ_{m≥1}e^(−mx′)=e^−x′/(1−e^−x′)`. Empty indexing families and μ=0 are handled. Large x can make lower bounds vacuous but does not invalidate them.

3. **SCR-A, (A∞), SCR-A°, (A°∞).** Verified the common-event conclusion for all LO models and all seeds, then the certified-model inclusions. The 3e^−x/4e^−x probabilities are correct. In the residual bound, `0.02+(n−1)/(n+1)≤1.02`; the extra `(n+1)/n` in ϑ° is correct. With x_n=√log n, the count bound `log N_q≤q log p+1` is valid also at q=0. All error terms are controlled relative to the displayed denominator, including varying σ_n. For A°∞, `‖μ‖=o(nσ)` gives `τ̄²=o(nσ²)` as needed.

4. **B1, B2, B2°, B2d, B3.** Checked the monotonicity domains before squaring, missing-coefficient ℓ1/ℓ2 comparisons, augmented bias c_θ, and the Schur-complement eigenvalue bound. The 4 and 9 in B2° follow from u−c_θ≥u/2 and u+c_θ≤3u/2. The directional extension uses only the asserted directional energy bound; it does not require φ^d≤1. B2°'s statement specialises the more general valid κ≤φ formulation in L4.

5. **A1 and A1°.** The conservative Γ bound κ²b²n/16 and the squared denominator bound give `200/64>2`, validating c₁. In A1°, the constants 16 and 576 give Ψ≥8L while the squared threshold is ≤4L; the coefficient-ratio condition is exactly what is needed for `sqrt(κ(n−1)) θ_min≥2c_θ`. No unmentioned fixed-σ assumption enters A1°.

6. **SCR-M and M1–M6.** Re-derived the signed-witness numerator, both denominator bounds, the exact log gap, and its comparison direction. Taking the minimum of two deterministic tail thresholds costs only one e^−x, because the smaller threshold is selected deterministically; no mistaken union-bound penalty is needed. The event costs 4e^−x, or 3e^−x for the total-scale-only denominator. Empty H-minus and u_S≥1 conventions are consistent. M3 needs the maximising witness, now stated. In M4, κb≤M (not κ≤1) is sufficient; `u*=κ²b²/[26(M²+σ²)]` yields the strict c₂n gap with denominator 104. Uniformity follows from the common bounds on Γ, τ, r and B_S. M6's illustration is valid with fixed nonzero coefficient, fixed σ,x, and log p=o(n); it is an example, not an added design-family theorem hypothesis.

7. **M2, M5 and SCR-G as coded.** A scanned missing centre has an evaluated improving addition, and CC6 transfers its score to the reported ledger maximum. For M5, removing the unique dropped truth gives either the old centre or an addition-neighbour of that centre; the best-neighbour property supplies the contradiction. The swap argument is legal because N∈H implies |C|=|N|≤K−1. The capped return is precisely that best neighbour. Strict δ>c₂n justifies SCR-G's weak observed-gap comparison ≤c₂n. No certificate inheritance from an arbitrary unscanned near tie is used.

8. **L5 facts (a)–(c), EC′/EC, L5.2 and SCR-C.** Verified the dual Gram/correlation matrix, α lower bound, ω≤1/φ, and the augmented bias in both lower and upper noise bounds. The deletion coefficient is `(n−1)/(n+0.02)≥1−1.02/n`. The positive part of Λ is necessary and correctly used. The single-excess α upper bound is algebraically valid for A>0. For SCR-C, η→0 uniformly, k≤(s₀+1)m uses bounded s₀, and the comparison margin is ε(2 log p+log n), larger than all uniform remainder terms. The chosen x=2 log n and x′=(ε/8)log n make the stated failure sum vanish. Cases q≤s₀ require no superset argument.

9. **SCR-R.** The common E3a event controls adaptive certified models without conditioning on their selection. Prediction needs no eigenvalue floor; coefficient error does. The probability tends to one because q≤n and the screening event holds. No claim that the method itself outputs the refit is made.

10. **SCR-N and both L6 sequences.** At ∅, a=n²/(n+1), D=n and Q=n−1 give the exact B_n threshold with n−0.98 and n+0.02. The coefficient `1−0.98/(n²+0.02n)` gives the displayed bounds; the u_n≥2 lower-bound case is properly separated. The probability count is 4e^−x and 4a_x≤1 justifies the squared lower scale. The orthogonal-signal sequence has a solvable coefficient equation and the required false-column noise slack. The cancelling-pair sequence has Δ~2(log n)², Γ~(log n)²/n and the stated B1 ratio. These establish the specified empty-model sharpness claims, not a necessity result for general q or a claim about which model the code reports.

11. **CC1–CC6, substantive implications.** Read the full requested R/C++ sources, including exact enumeration, preprocessing, start tables/mode, score fallbacks, cache, ledger, final search and LS0 assembly. Every complete scan enumerates the stated neighbourhood; the cap and certificate branches match. Exact enumeration scores all feasible subsets. Cache ownership plus the already-offered initial final-search centre justifies CC6 even on a non-emitting evaluation; cache eviction does not lose the running HPM. The reported flags use endpoint equality and the two-search OR. Indices are mapped to original retained-column labels in output; theorem comparisons require the stated common-coordinate convention. The source manifest's hashes were compared against every listed current core file: no mismatch. N0's output confirms 16,004 comparisons and maximum difference 5.969e−13, consistent with CODE_CHECK's rounded 6.0e−13; its local scan is a numerical check with tolerance, not a replacement for EX-A.

12. **Protocol/target scope.** A1 supplies PROGRAM item 5 with explicit coefficient/noise/growth conditions; the design-family examples do not enter theorem hypotheses. The all-seed statements follow from events involving only the data and simultaneous deterministic-model inequalities. The package correctly avoids claiming output frequency, cap-size screening, PIP/MPM/evidence results or a floating-point theorem. The requested edge cases q=0, S=∅, K=1, |S|=K−1, small p, duplicate columns, μ=0, s₀>q, varying σ and large x introduce no additional failure in the formal results.

## Prior-disposition check and limitations

After forming the findings, I read R02/R03/R04, R05 and R06 disposition files. The deliberate choices to use the log-linear EC′, omit a cap-boundary theorem, and retain the code's certificate semantics are respected; none is reported as a new flaw. Finding 5 concerns a still-false absolute claim about included signal after R06's repair. This review checked the mathematical proofs and production source semantics; it did not rerun the expensive production numerical studies or independently reproduce every numerical frequency quoted in the assumption map. No theorem conclusion above relies on those frequencies. Only this report was written.
