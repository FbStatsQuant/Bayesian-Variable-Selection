# Council XR1 — sol — blind first read

Verdict: **ACCEPT X1, X3, X5 and T14**, within their stated scope. X3 is VERIFIED. X5 is accepted specifically as **VERIFIED WITH AMENDMENTS** for the uninterrupted pair and potential evidence, with MEAS-J and joint independence for its joint-law form; this does not verify the original unqualified actual-success wording. No C, S or F finding is held. Two E findings below do not block.

Reviewed manifest: `0ebcb2dafa56732bb7b70f920ba3234a7ed62c6a514428162f8e4d973f907d3c`. The prescribed verifier returned OK before review; the core working files also match pin `4676af6` by a read-only diff. Sibling T1/T5/T6/T7/T9 statements were treated as supplied, already checked inputs, not newly reviewed claims.

## Gates

| gate | result | basis |
|---|---|---|
| G1 correctness of steps and code citations | PASS | Re-derived the frozen-run induction, prefix and RB identities, size-tail inequalities and pooling argument; checked the relevant code at the pin and all permitted recorded citation blocks. |
| G2 hypotheses used = stated | PASS | X1 explicitly assumes exact arithmetic, ideal uniforms, START and KERNEL; X3 uses G and both representation bounds; X5 names its required amendments; T14 is restricted to shipped defaults and sites reached. |
| G3 no hidden assumptions | PASS | No stationarity or mixing is required for X1; no eigenvalue bound is needed for X3; no independence between final islands is required for pooling; actual clock selection is expressly excluded without its additional premise. |
| G4 imports and statuses verbatim | PASS | The inspected source statements, bridge status, T12 status and copied PoolZ claim support their reported imports. Historical/registry-only status assertions were not independently audited outside the allowed inputs. No conflicting status was found. |
| G5 scope and constants | PASS | Checked prefix scope, four measured rounds, exact prior ratio, zero-tail case, deterministic cutoff, constants and the dimension/cap boundary arithmetic. The two E notes concern exposition only. |
| G6 fidelity to pinned code and re-checked sources | PASS | The final island control flow and evidence/RB readout agree with T12; the R pooling code computes the stated mean; default LS0 settings and the cap guard agree with REP. |

## Per-claim decisions

| id | decision |
|---|---|
| X1 | ACCEPT |
| X3 | ACCEPT |
| X5 | ACCEPT |
| T14 | ACCEPT |

## Numbered findings

1. **E — make the amended PoolZ notation consistent inside the statement paragraph.** `Theory_work/Wave3/W3-AUDIT/track_A_X/X5_POOLZ/STATEMENT.md:26` displays the joint-law identity with unadorned 𝒜 and Ẑ, although lines 21–25 explicitly restrict the verified result to (𝒜°, 𝓒°, Ẑ°), and lines 31–38 expressly withhold the actual-event identity without clock independence. The surrounding qualification resolves the meaning, so this is not an additional substantive finding. **Repair:** write `E[1_𝒜°Ẑ°] = E[1_𝒜°Z]` at line 26 and use the same superscripts in PROOF steps 1–4, reserving actual 𝒜 for the final precision.

2. **E — include the source domain in the informal X3 summary.** `Theory_work/Wave3/W3-AUDIT/track_A_X/X3_L1A/STATEMENT.md:15` summarises the lemma without mentioning p ≥ 2, which is explicit in `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md:10`; the source also quantifies the tail index over integers. Lines 12–14 say that the source claim is referenced rather than restated, so its domain remains controlling and there is no change to the verified claim. **Repair:** add “p ≥ 2” and “integer m” to the informal summary.

## Substantive checks

- **X1.** Traced stream 9+r and the `nullptr` starts through `cpp/v3_core.cpp:443` and `cpp/v3_engine.h:269`. The fixed schedule has one increment/resampling/round per stage, no stage-0 round, L terminal burn-in rounds and four measured rounds. Scores and the full-set cache check make the statistical transition independent of cache history; ledger/RB bookkeeping does not feed transitions. Fresh iid stream continuations at finite consumption stopping times give R1 and R2. Conditioning sequentially on each particle's round start gives the product law of the order/path pairs in R3, despite variable uniform consumption. Re-derived detailed balance for all four kernel types, invariance of every order-dependent fixed prefix, the resampling conditional mean, the stage induction and the terminal-round induction. For RB, κ_j(σ) = σ⁻¹(g_j)−1 and K_gj 1_{J_j} = o_j give the stated identity; the code records before the draw and divides by N·Hm. These are ideal-arithmetic/ideal-uniform identities for the uninterrupted statistical record.

- **X3.** Evaluating the slab variational problem at the deterministic representing θ gives Q_T^c ≤ σ*²E′ + ρ, with 0 ≤ ρ ≤ M+M′, including T empty. The denominator exponent inequalities retain their direction after replacing R_n by ρ. Restricting the inverse-gamma integral gives the exact factor c_IG σ*²/√n; D_T ≤ (n+1)^t requires no rank or eigenvalue assumption. The chi-square first absolute moment gives C′_Λ = 1/√2 + 1/2 + (M+M′)/(2σ*²). The numerator has mean v_m for a data-free rate. The exact identity v_m/ϖ(T) = R_m^T, the R_m^T=0 case, the two Markov bounds and the scale-event probability produce the displayed uniform-in-m tail bound. The deterministic cutoff exists because T ∈ Ω and R_K^T=0; substitution gives precisely (1+1/n)^{t/2}e^{−ω}. The constants depend only on the stated bounds and σ*². No interchange of supremum and probability is used.

- **X5.** Checked the verbatim copied source and N1's localised conditional identity. On 𝒜°, four per-island identities and linearity give E[Ẑ°/Z | 𝓒°]=1 without between-island independence. Z is positive and constant for fixed data. For the joint law, the stated joint stream independence and MEAS-J permit freezing conditional on (data,𝓒°); the bounded-function freezing lemma extends to nonnegative evidence by monotone truncation, so the final equality can hold in [0,∞] without an integrability assumption. Joint measurability follows on each fixed-dimension/count cell from finite Borel computations and measurable branches, with countably many cells. Actual 𝒜=𝒜°∩G is not generally measurable with respect to 𝓒°, and equality cannot be transferred by the upper-bound/intersection argument. The amendment correctly identifies this limitation and states the additional joint independence sufficient for the actual-event equality.

- **T14.** Checked retained p ≤ p_raw and the double conversion before n+p+1. At any evaluated default base-cap validator, 5 ≤ n+p+1 ≤ 2³²−1, hence 3 ≤ ℓ_n ≤ 32; the helper uses exact power-of-two/integer comparisons in this range. The stored integer base cap is therefore nonnegative. Any start-mode set returned on the shipped path has size at most K (enumeration paths allocate the selected total size ≤K; the tie-aware fallback returns a member of the same set family). The second site's execution already entails that the preceding mode call returned; no completion/allocation claim is needed. Consequently cap_ll ≤ 32+⌊n/2⌋ ≤ 1,073,741,855 < 2,147,483,647, and its addition is performed in long long. Both lifted predicates are false at their evaluated sites. This discharges only the two extra clauses relative to IDEAL-W, exactly as the statement's exclusions specify; it does not establish general native integer safety or successful delivery.

## Score

**9.4 / 10**, assessing C/S/F issues only. No blocking finding or repair is required for the four qualified claims; the E notes do not reduce the score.

## Checks performed

- Ran the exact prescribed `python3 -B Theory_work/Wave3/tools/manifest.py verify ...` command: OK for the named manifest.
- Ran read-only `git -c core.fsmonitor=false diff --no-ext-diff --exit-code 4676af6 -- Scripts/SMC_BVS/core`: exit 0, no differences.
- Recomputed the stored citation-block SHA prefixes without invoking the writing citation-checker: X1 54/54, X3 29/29 permitted blocks, X5 11/11 and T14 31/31 matched; no missing or out-of-range permitted block. The one X3 registry block was deliberately skipped because the registry is outside the permitted inputs.
- Read the four items' statements, proofs and citation reports, the copied PoolZ source, the relevant whitelisted external inputs and the five permitted sibling statements. Independently checked the algebra and cited execution paths described above.
- Used no subagents and changed no git state. The only authored file is this report.

## Not checked

- No content review of INDEX, CHECK files, card drafts, logs or other review reports; manifest verification hashed frozen files as prescribed without using their contents as review evidence.
- No independent registry audit, status promotion or verification of historical-review/remote-worktree provenance. In particular, the original W3-READER worktree was not accessed; the frozen verbatim copy was the reviewed source.
- No re-proof of the already checked sibling lemmas, the full P1/T03R results or N1's full theorem. Their relevant imported statements and used steps were checked within the allowed packet.
- No new comparison against the old v2.2.1 tree, which is outside the permitted inputs; its relationship to the pin was read from the permitted CC input, and the relevant current code was inspected directly.
- No floating-point accuracy, actual PRNG independence, mixing, clock probability model, general overflow/allocation safety, delivery guarantee, interrupted-run unbiasedness, T12 (i.d)/(iv), or excluded X3 remarks. No runtime statistical experiments or formal proof assistant checks were performed.

COUNCIL-VERDICT round=R1 manifest=0ebcb2dafa56732bb7b70f920ba3234a7ed62c6a514428162f8e4d973f907d3c seat=sol score=9.4 gates=PASS
