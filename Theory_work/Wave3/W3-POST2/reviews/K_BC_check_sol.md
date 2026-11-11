# W3-POST2: adversarial check of Claims B and C

Reviewer: Codex / GPT-6.1 Sol, high effort. Date: 2026-11-09.
Scope: `STATEMENT.md` v1.1; the two requested proof files and their cited proof dependencies. No proof files or git state were changed. Line numbers below refer to the files as read for this review; paths are relative to the repository unless shortened explicitly.

## Verdicts

| File | Verdict | Assessment |
| --- | --- | --- |
| `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md` | **VERIFIED-WITH-AMENDMENTS** | Lemma 1a″ and its exact determinant normalization check out. Remark 1 contains a false equality of constants; the sharper exact-reference constant is recoverable from the proof. |
| `Theory_work/Wave3/W3-POST2/lemmas/C_expectation.md` | **VERIFIED-WITH-AMENDMENTS** | Proposition ER checks out in cases (i), (ii), and (iii), including its single-n uniform formulation. Amend the zero-tail edge case, one notation typo, and an overly broad methodological claim in Remark 3. |

**No FATAL or MAJOR finding.** Findings below are local repairs and do not require weakening either main theorem.

## Numbered findings

1. **MINOR — false equality in the recovery of L1a′.**
   Location: `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md:46` (context: lines 45–48).

   The displayed definition at line 13 gives

   `C″_Λ(M+M′) = C′_Λ + sqrt(2(M+M′)/π)/σ*`,

   rather than `C″_Λ(M+M′) = C′_Λ`, unless `M+M′=0`. Setting the actual residual `r` to zero does not change the definition of the function `C″_Λ(B)`. Thus the stated general probability bound specializes to a bound with a larger constant; it does not, by substitution alone, recover L1a′ with its exact constant.

   **Proposed fix:** replace the equality by: “The general statement implies the L1a′ conclusion with a larger constant. In the exact-reference case, Step 3 improves to `EΛ″ ≤ 1/sqrt(2)+1/2+B/(2σ*²)`, because `r=0`; repeating Step 4 with this improved constant recovers L1a′ with its stated `C′_Λ`.” Then explicitly use `Θ^T = sqrt(D_T)/(n+1)^(t/2) · Θ″ ≤ Θ″` to transfer the tail bound to L1a′'s normalization. The parenthetical already contains the needed improved calculation, so this is a correction of the claim's wording, not a missing substantive argument. The cutoff comparison at lines 47–48 is correct.

2. **MINOR — the zero-tail case is not carried through the cited numerator construction.**
   Location: `Theory_work/Wave3/W3-POST2/lemmas/C_expectation.md:25` (context: lines 24–26).

   The cited proof constructs `Θ^(1)=N_m/v_m` only when `R_m>0`; see L1a′ lines 39–42 and [T03R] lines 93–97. It need not be positive at the selected cutoff: `m♯_n=K` occurs, for example, for fixed `p` and sufficiently large `n`. Then `v_m=0` and this ratio is undefined. The tail is identically zero, so the theorem is unaffected, but the unconditional assertion that the cited construction gives `EΘ^(1)=1` needs a case convention.

   **Proposed fix:** begin the tail paragraph with “If `m♯_n=K`, then `T₀=0` and there is nothing to prove. Otherwise `R_{m♯}>0`, and define `Θ^(1)` as in L1a′.” Alternatively define an arbitrary mean-one nonnegative variable in the zero-tail case and say so explicitly.

3. **NIT — undefined `d` in the chi-square threshold comparison.**
   Location: `Theory_work/Wave3/W3-POST2/lemmas/C_expectation.md:28`.

   The proof writes `d+2sqrt(dx)+2x ≤ N+4sqrt(Nx)` without assigning `d`. It is correct for the intended `d=N`, since `x≤N` implies `2x≤2sqrt(Nx)`.

   **Proposed fix:** replace that expression by `N+2sqrt(Nx)+2x ≤ N+4sqrt(Nx)`. The citation to [P3] `lem:chi`(a) is otherwise exact, and both tails are supplied by that label.

4. **MINOR — an unproved general obstruction is stated as fact in a remark.**
   Location: `Theory_work/Wave3/W3-POST2/lemmas/C_expectation.md:56` (context: lines 53–57).

   “Hölder or a change of measure does not remove it” is broader than anything established by this proof or its citations. Heavy variance tails do explain why particular direct estimates fail; they do not prove that every use of either technique cannot improve the rate. There is a precise narrower obstruction available: for the fixed-rate prior-predictive ratio `Θ^(1)=h(y_c)/f₀(y_c)`, with `h` a nonempty normalized finite mixture, `E₀[(Θ^(1))^(1+η)] = ∫h^(1+η) f₀^(−η) = ∞` for every `η>0`, because `h` has polynomial tails and `f₀` Gaussian tails. Also the direct untruncated integral `E₀[Θ^(1)e^{Λ′}]` diverges. Neither fact rules out truncations or other arguments exploiting the bounded posterior mass.

   **Proposed fix:** say “The direct Hölder estimate requiring a moment of `Θ^(1)` above order one, and the direct untruncated change-of-measure estimate for `Θ^(1)e^{Λ′}`, fail because the corresponding integrals diverge. Whether a different argument removes the factor remains open.” Supply the short integrability calculation if retaining this discussion. This remark is not used to prove ER.

## B: line-by-line checks and attempted breaks

### Statement and Step 1 (lines 6–21)

- The required mean is centered: `μ=Cf`. It need not be in `col X`. The contrast law is exactly `y_c=Uᵀμ+ε_c` with `ε_c~N_N(0,σ*²I)` and strictly positive density `f₀`. The posterior is defined almost surely, since this Gaussian law on `1^⊥` is nondegenerate.
- [P1] `thm:T01iii`, lines 234–250: its theorem is written under G, but the proof of the scale-event bound uses only centering, Gaussian noise, and `||μ||²≤nM`. In particular, the cross covariance in line 248 vanishes by sign symmetry for every deterministic centered `μ`. Thus the extension claimed in B is justified by the source proof, with exactly `(8+24M/σ*²)/(n−1)`.
- [P1] `lem:num`, lines 317–321: the numerator predictive is a proper density at the **fixed** rate `b₋`. The identity `∫(m_b/f₀)f₀=1` requires only a positive true density. It does not require that the mean lie in the working model. This remains valid for the approximate-reference and misspecified-mean cases.
- [P1] `thm:T01i`, lines 173–208, and `thm:Ta`, lines 255–264: the identities and the first transfer inequality are deterministic. The denominator can be bounded by the contribution of any `T∈Ω`; `S₀` in the source's final inequality is not essential. The underlying rate comparison, [P1] lines 213–221, is pointwise in both the data and the rate. No conditioning-on-scale Gaussian assertion is introduced.
- [P1] `lem:slab`, lines 68–80, and `lem:spec`, lines 90–110, are deterministic and include rank-deficient and empty models. Retaining `D_T` is legitimate; there is no eigenvalue-floor assumption hidden in this step.

### Step 2 (lines 23–28)

The variational upper bound has the right penalty: `ϑᵀ(G_T+I)ϑ/n = (||X_Tϑ||²+||ϑ||²)/n`. Since `Cr=r`,

`ε_cᵀUᵀr = εᵀUUᵀr = εᵀCr = εᵀr`.

Therefore the reference cost and the signed cross term bound `Q^c_T` as written. Replacing the signed term by its absolute value is conservative, and `ρ″=B+2|εᵀr|≥0` because the nonnegative cost is bounded by `B`. The variance `σ*²||r||²` and the absolute-normal first moment are correct. For `t=0`, the penalty is zero and `r=μ`; direct expansion of `||μ+Cε||²` gives exactly the same bound. No full-rank assumption is needed.

### Step 3 (lines 30–35)

I re-derived rather than assumed the cited “verbatim” extension. In [P1] `lem:den`, lines 340–357, set `v=σ*²u`, `1≤u≤1+n^(−1/2)`. The exponent is bounded below, pointwise for each observation, by

`(u−1)/2 · (E′/u−N) − ρ″/(2σ*²)`

`≥ −|E′−N|/(2sqrt(n)) − E′/(2n) − ρ″/(2σ*²)`.

Here `−ρ″/(2σ*²u)≥−ρ″/(2σ*²)` uses only nonnegativity and `u≥1`. No distributional manipulation involving `ρ″` occurs inside this comparison. Its correlation with `E′` is harmless. The integration interval has length `σ*²/sqrt(n)` and the IG minimum is the same fixed `c_IG`; hence the exact `D_T^(−1/2)` factor and all constants in line 33 are correct.

Linearity of expectation suffices for line 35. In particular,

`E[ρ″/(2σ*²)] ≤ B/(2σ*²) + sqrt(2B/π)/σ*`.

This verifies the stated `C″_Λ(B)` without independence.

### Step 4 and remarks (lines 37–62)

For `R_m>0`, `v_m=R_m ϖ(T)` is exact; the cap normalization cancels. The source assembly [T03R] lines 93–97 therefore gives `Θ″≤c♯e^{Λ″}Θ^(1)` on the scale event, with `EΘ^(1)=1`. The union bound followed by two Markov inequalities yields the stated bound for every `L>c♯²`. This is `sup_m P(...)`, not the stronger and unproved `P(sup_m ... )`. For `R_m=0`, the tail is zero by positivity of all model weights.

The `O_P(e^(−ω_n))` consequence follows for common fixed `(M,B,σ*²)` from this uniform tail bound. Dropping weak coefficients (lines 50–52) uses the triangle inequality with `||x_j||=sqrt(N)` and is correct. For the empty reference (lines 53–54), `R_m=2Σq_k≤2^(1−m)` follows directly from the unnormalized sum in [P1] `lem:prior` proof, line 128; it does not require replacing `W_K` by one. The determinant product in lines 56–57 is the exact [P1] formula. Small eigenvalues help to the extent that their actual factors `((n+1)λ+1)/(λ+1)` are small; no uniform quantitative claim beyond that formula is supplied. The growing-cost remark follows by scaling the Markov bound; it is not a bounded-cost tightness assertion when `B_n` diverges. The numerical summary at lines 60–62 agrees with the saved N6 output (lines 74–93).

### Independent falsification attempt

Scratch reproduction: `Theory_work/Wave3/W3-POST2/reviews/K_BC_scratch/check_b.py`.

Command from repository root:

`py -3.13 -B -I Theory_work/Wave3/W3-POST2/reviews/K_BC_scratch/check_b.py`

I used the supplied exact enumerator, independently computing the contrast marginal likelihood and its Gaussian density ratio. The 2,160 draws covered `n∈{8,30,100,1000}`, `p=4`, iid/duplicate/nearly-collinear columns, references of sizes zero/one/two, and residual norms zero/one/three in a centered direction orthogonal to the entire design span. All integer cutoffs `−1≤m<K` were tested, including cutoffs below `t` absent from the original N6 scan.

Results:

- Maximum `Q^c_T−(E′+ρ″)`: `5.04485342e−13`, consistent with rounding at equality.
- Minimum log ratio of the exact denominator to its proposed lower bound: `2.77253855` (required nonnegative).
- Maximum log ratio of posterior tail to the mixed-endpoint transfer bound, on the scale event: `−0.957345868` (required nonpositive).
- Maximum observed `Θ″`: `0.994231163`.

No counterexample was found. These are checks of the pointwise ingredients and a finite sample search, not an empirical proof of the probability tail bound.

## C: line-by-line checks and expectation accounting

### Decomposition and tail (lines 17–32)

The decomposition covers every feasible model other than `S₀`, and `T_sup+T_U≤1`, so removing the good event costs its probability only once. In (i)–(ii), using the selection event, including G4, is necessary for the cited signal-gain lemma. In (iii), the replacement event is exactly the one used by E1.

Under F₀, `||θ*||²≤nM/(Nφ₀²)`. Consequently

`ρ=(||μ||²+||θ*||²)/n ≤ M+M/(Nφ₀²) ≤ M+M/(2φ₀²)`.

It is deterministic at fixed `(X,θ*)`. L1a′ lines 27–42 apply directly, with no need to use the approximate-reference result B. At `m=m♯_n`, the cutoff definition in [W3P] lines 36–39 gives exactly the prefactor `(1+1/n)^(s₀/2)n^(−1/2)`. Finding 2 handles the empty tail.

The potentially suspicious inequality in line 27 is valid: write `E′=N+(E′−N)`, bound the difference by its absolute value, and use `1/n≤1/sqrt(n)`. Thus `Λ′≤λ₀+|E′−N|/sqrt(n)`. [P3] `lem:chi`(a), lines 154–163, really supplies both claimed exponential tails. After the typo in finding 3 is repaired, for `0<x≤N`,

`P(|E′−N|>4sqrt(Nx))≤2e^(−x)`.

The event `Λ′>λ₀+4sqrt(x)` is contained in this deviation event because `sqrt(N)≤sqrt(n)`. The choice `x=(log n)/2` lies in `(0,N]` for every `n≥3`, and `4sqrt(x)=2sqrt(2log n)` exactly.

The expectation step is valid without independence:

`E[e^{Λ′}Θ^(1) 1{Λ′≤λ}] ≤ e^λ EΘ^(1) = e^λ`.

The event indicator for the scale event may also be discarded since all quantities are nonnegative. On the remaining deviation event, use `T₀≤1`. This proves the displayed tail expectation with the stated exponent and `2n^(−1/2)` remainder.

### Superset and underfit terms (lines 34–42)

All expectation claims here use **first-moment bounds** from the cited proofs, not an invalid conversion of an `O_P` statement into an expectation statement.

Let `H_n=(2p)^(s₀)(n+1)^(s₀/2)` and `h=(j₀+1)/2`. Uniformly beyond a constant-dependent threshold, `e^{ρ_n}≤2`.

| Case | Good event | Available unconditional moments | Consequence on that event |
| --- | --- | --- | --- |
| (i) | `𝒢^sel_n` | [T03R] C5(b): `EΥ_n≤2K_{s₀,0}q_n≤Cr_n`; C8 proof: `H_n EΥ_n^{>j₀}≤C(log n)^h/n` | Superset expectation `≤Cr_n`; underfit expectation `≤C[n^(−2)(1+r_n)+(log n)^h/n]`. |
| (ii) | `𝒢^sel_n` | A C5′(b): `EΥ′_n≤𝒪_n^{>0}` and `H_n EΥ′_n^{>j₀}≤H_n𝒪_n^{>j₀}`; OS bounds both by `C_OS r_n` | Superset expectation `≤2C_OS r_n`; underfit expectation `≤C(n^(−2)+r_n)`. |
| (iii) | `𝒢^sup_n∩𝒢⁵_n` | Same moments as (ii), and E1 gives `κ_n≤n^(−2)` | The same expectation bounds as (ii). |

For (i)–(ii), C10's `κ_n≤e^{ρ_n}n^(−2)` uses F_λ only on bounded-excess unions, BM(c), and G4; the required threshold includes `n≥c/(c−c₀)`. For (iii), E1 lines 24–43 use the floor on S₀ only, ID(c), and the cross-term event. I checked its Gaussian union bound (lines 19–23), the lower bound on the score difference (lines 32–36), and its exponent calculation (lines 37–43). Its strict margin `c>c₁` yields the asserted deterministic `n^(−2)` comparison after a uniform threshold.

The second underfit coefficient `e^{2ρ_n}` in C line 39 is conservative: [T03R] C8 actually needs only `e^{ρ_n}` after its improved crude comparison. Since `ρ_n≥0`, the looser coefficient is valid. In particular C does not accidentally need an eigenvalue bound for large-excess underfits. The intermediate comparison unions may leave Ω: [P3] lines 39–43 and 227 define their scores there, and A's moment sums extend to `j≤min(m♯_n,p−s₀)`. Thus the OS hypothesis is controlling the required range.

For A C5′, the key moment is correct also at rank zero: `χ²_0=0`; at rank `d>0`, [P3] `lem:chi`(b) gives the truncated moment bounded by `(eτ_j/d)^(d/2)`. Eventually `e^{jε_n}≤2^(j/2)`, which is precisely the additional factor in `a_J`. No independence among the different `χ²_J` is used.

### Bad events, uniform threshold, and consequences (lines 7–14, 44–59)

The good-event probabilities are `≤4/n` for G1–G3, `≤5/n` with G4, and `≤1/n` for the extra E1 event. These follow from [P3] `lem:Gprob`, lines 187–194, with rank domination as in A lines 43–50. Therefore each case in C pays at most `5/n` outside its chosen event.

The single-n formulation is justified, not merely inherited from sequence-wise convergence. By [T03R] E2, lines 50–60, `m♯_n≤C_m log n` uniformly under `p≤n^A`. Substitution into [P3] lines 197–203 and 232–253 gives deterministic envelopes for `δ_n`, `δ″_n`, `ρ_n`, and `ε_n`; C5 adds an envelope for `q_n` in case (i). All thresholds can be chosen from the listed constants and the strict BM or ID margin. Neither an onset for OS nor a common onset across arrays is needed when its two inequalities are assumed at the current `n`. Under BM-∞ the envelope must be deterministic and the hypothesis at each applicable `n` must be `θ_min²≥M_nσ*²log n/(nφ₀²)`; the additional threshold is when that envelope exceeds a fixed admissible beta-min constant. This is the stated qualification.

For random designs, conditioning on `(X,θ*)` is legitimate under noise independence. Apply the uniform deterministic bound on `𝒜_n` and use `δ_n≤1` off it to obtain the additive `P(𝒜_n^c)` remainder.

Finally `(log n)^h/n=O(r_n)` for fixed `h`, and `sqrt(log n)≤exp(2sqrt(2log n))` for all sufficiently large `n`. This completes ER. The PIP and model-selection inequalities in lines 49–51 agree with [P3] paragraphs (ii)–(iii), lines 362–364, and [SL] SL0/SL1, lines 20–51. The lower bound in line 52 has exactly LB's additional domain `1≤s₀<p`, `s₀+1≤K`; LB lines 20–32 prove the cited deterministic constant. Combined with ER it yields the claimed exponent `1/2`. N5's saved numerical values support only the qualitative suggestion in Remark 3, not an improvement of the proved rate.

## Source audit index

All requested cited labels were opened and checked locally; no web attribution was substituted for the locked sources.

- **[P1]** `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`: `lem:slab` 68–80; `lem:spec` 90–110; `lem:prior` 113–136; `lem:chi` 139–150; `thm:T01i` 173–208; underlying envelope 213–221; `thm:T01iii` 234–250; `thm:Ta` 255–264; `lem:num` 317–321; `lem:den` 324–359; `thm:T02i` 362–378.
- **[P3]** sibling path `T03_A2_selection_consistency/PROOF_v2.tex`: single-n envelopes 35–49; smoother/comparison/determinant/prior 94–143; signal 146–151; `lem:chi` 154–166; good events and probability 169–194; `lem:ongood` 197–222; superset sums and moments 225–277; underfit comparisons and assembly 280–329; main decomposition 334–359; selection/PIP consequences 362–364.
- **[T03R]** `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`: cutoff location 45–60; exact constants and denominator/assembly 74–99; restricted assumptions and comparisons 129–143; C1–C10 and assembly 170–205.
- **[L1a′]** `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md`: statement and proof 9–42; coefficient bound 45–49. **[W3P]** `Theory_work/Wave3/W3-POST/STATEMENT.md`: target and cutoff 16–39, theorem hypotheses and consequences 63–104.
- **Local dependencies:** `A_occam.md` 43–83, particularly C5′ 61–72 and C8′ 74–76; `E_visibility.md` E1 12–43 and its explicit assembly 45–55; `W3-POST/lemmas/LB_rate_lower_bound.md` 9–32; `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md` 20–51; saved `numerics/post2_checks_out.txt` N5/N6 58–93.
