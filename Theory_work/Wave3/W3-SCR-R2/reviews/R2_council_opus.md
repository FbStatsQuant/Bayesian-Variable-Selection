# W3-SCR council round R2, seat `opus` (Claude Opus 5.5, effort high, fresh)

Date: 2026-11-16 01:34 CST (`date`). Worktree `/home/fb31/BVS-wt/W3-SCR-R2`, branch `theory/W3-SCR-R2`. Read-only
review: I wrote only this file and scratch files under `/home/fb31/SMC_Theory_Department/tmp/20261116-W3-SCR-R2-opus/`.
I changed no git state and started no subagents. Of `W3-SCR/reviews/` I read nothing. I read the seat-allowed
`W3-SCR-R2/reviews/PC_SCR_sol.md` and did not take its conclusions on trust.

## 1. Manifest verify

```
$ python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-SCR Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R2.txt
verify: OK MANIFEST 96488f34902506d5cecf92b85aa257627ca396cdd7d3e60b86db32f688300b93
EXIT=0
```

Production code: the eight files in `Scripts/SMC_BVS/core/` match `git show 2252d57:` and `numerics/core_copy/`
byte for byte once line endings are normalised. `SHA256SUMS_source.txt` records the hashes of the CRLF bytes; a
CRLF-converted copy reproduces them (scratch `hashcheck.txt`). The core was last changed at 72785fe8, which is an
ancestor of 2252d57. So CODE_CHECK's line references describe the current code (see E2).

## 2. Seat task 1: the SUBSTANTIVE hunks of PC_SCR_sol.md

| Hunk | (a) current text correct, proof complete with the hypotheses as stated | (b) consumers state the same hypotheses | Decision |
|---|---|---|---|
| **A1** (STATEMENT:158–163; L3:65–76; chain L4.0/B2/B2d/B3, L1, L2, L3:6–35) | yes | STATEMENT/L3/L7 yes; **REPORT:27–29 no** (Finding 1) | **CONFIRM** (proof); derived text F |
| **SCR-G** (STATEMENT:132–145; L7 M2, M4, M5) | yes | STATEMENT/L7 yes; **REPORT:36–37 drops the size condition** (Finding 3) | **CONFIRM** (proof); derived text F |
| **M4** (L7:97–109) | yes; the "for large n" steps use exactly κ, b, M, σ fixed | yes | **CONFIRM** |
| **M6 prose** (STATEMENT:120–129, L7:112–117) | yes, true as written | yes (ASSUMPTION_MAP:16 matches) | **CONFIRM** |
| **ASSUMPTION_MAP:20 construction** | the construction is feasible and Γ_n(0) is computed correctly | not consumed by any claim | **CONFIRM** (E3 on an unproved side remark) |

**A1, re-derived.**
- ‖θ*‖₂ ≤ ‖θ*‖₁ ≤ M, and ‖μ‖ ≤ ‖θ*‖₁√(n−1), so τ_n² ≤ M² + σ² = τ_*².
- The large-n step is the only one that is not exact: n₀(κ, b, M) with √(κ(n−1))b ≥ 2M/√(n+1). It uses κ, b, M fixed, which A1 now states.
- With c_θ ≤ M/√(n+1) ≤ ½√(κ(n−1))b, B2d gives Γ_n(q_n) ≥ (κ(n−1)/n)(√(κ(n−1))b − c_θ)².
  - This step needs B2's bound to be monotone in the floor (κ ≤ φ^d) and in θ_min (≥ b). Both hold because the bracket is ≥ 0.
  - With (n−1)² ≥ n²/4 it follows that Γ_n ≥ κ²b²n/16.
- Denominator: [τ_n√(2log p + log n) + σ√(2q log p)]² ≤ 2τ_*²(2(q+1)log p + log n) ≤ 4τ_*²c₁n.
- So ρ² ≥ κ²b²/(64τ_*²c₁) = 200/64 > 2.
- The (A∞) reduction (L3:26–35) checks out:
  - N_q ≤ (p+1)^q and q log(p+1) ≤ q log p + 1;
  - x_n = √log n gives r_n ≤ √(2q log p) + o(√log n);
  - σ ≤ τ_n absorbs the o(√log n) term into (1+o(1))τ_n√(2log p + log n).
- The transfer to 𝒞 and to `local_certified` goes through CC2–CC3 and L3:20–24, with no conditioning on certification.
- L3:76 (p ≤ n^A, q_n = o(n/log n)) follows because c₁ > 0 is fixed.
- σ fixed is stated in A1 but is not used in the proof: the large-n step does not involve σ. That is not a defect (better-theorem note BT1).

**SCR-G / M4, re-derived.**
- √g⁻_S ≥ √Γ − σ r_n ≥ κb√n/4 − o(√n) ≥ κb√n/5. This uses b_𝓗 ≤ r_n, the maximising witness, r_n² ≤ 2q log p + 2log2 + 2 + 2x_n = o(n), and κ, b, σ fixed.
- Ū_S ≤ (n−0.98)τ̄² ≤ 1.01nτ_*² for large n. Then u_S ≥ (n/(n+1))κ²b²/(25.25τ_*²) ≥ u* = κ²b²/(26τ_*²) once n/(n+1) ≥ 25.25/26, that is n ≥ 34. This step is correct.
- κb ≤ M holds. Take S = ∅ in φ^d; then ‖Xθ*‖ ≤ ‖θ*‖₁√(n−1) and ‖θ*‖₂² ≥ b‖θ*‖₁.
- −νlog(1−u_S) ≥ nu*/2, and B_S ≤ log(2p−1) + ½log(n+1) = o(n) uniformly in S. So δ_S > nu*/4 = c₂n for large n, and c₂ = κ²b²/(104τ_*²) is correct.
- SCR-G (i): from M2, every C ∈ 𝓗⁻ has `hpm_F` − F(C) ≥ δ_C > c₂n.
  - `hpm_F` is `led$hpm$F` (v3_run.R:142), on the same F = logprior + logm scale as `scanned_F` (v3_engine.h:97).
- SCR-G (ii): M2, then M5.
  - In M5 a swap N = C∖{t}∪{l} has l ∉ S₀ because C ⊇ S₀.
  - Also |C| = |N| ≤ K−1, so C∪{l} ∈ 𝒩(C) was scanned, and F(C∪{l}) ≤ F(N).
  - In the deletion case N∪t = C with F(C) < F(N).
- SCR-G (iii) is M5(i). It needs moves to the best scanned neighbour, which v3_engine.h:390–413 confirms (strict improvement, lexicographic ties).
- M4 does not use the c₁ growth bound, only 𝐋_n = o(n). SCR-G assumes both, which is harmless.

**M6.**
- The bound b_𝓗 ≤ √dim span{d_S} + √(2x) holds: w(𝓓) ≤ E‖Πg‖ ≤ √r, because dᵀg = dᵀΠg ≤ ‖Πg‖ for ‖d‖ ≤ 1.
- Illustration: if x_1 ⊥ X_S then R_Sx_1 = x_1 and a = n²/(n+1).
  - γ = θ₁²(n−1)²(n+1)/n² and τ_n² = σ² + θ₁².
  - All d_S coincide, so b_𝓗 ≤ 1 + √(2x).
  - Hence u_S → θ₁²/(σ²+θ₁²) ∈ (0,1) uniformly, −νlog(1−u_S) is of order n, and B_S = o(n) when log p = o(n). So δ_S > 0 for every S ∌ 1 of size ≤ K−1, for large n, with θ₁, σ, x fixed as stated.
- "b_𝓗 itself is the smaller of this kind of geometric bound and the counting bound" is accurate; the counting branch is kept in the definition.

**ASSUMPTION_MAP:20.**
- For 0 < κ ≤ 1 and n ≥ 3 the correlation −(1−κ) is realisable in the centred subspace (dimension n−1 ≥ 2).
- The pair Gram is (n−1)[[1, −(1−κ)], [−(1−κ), 1]], with λ_min = κ(n−1). So φ^a_n(0) = φ^d_n(0) = κ; for φ^d, ‖b(x₁+x₂)‖² = 2b²κ(n−1).
- x_tᵀμ = b(n−1)κ and a(t|∅) = n²/(n+1), so Γ_n(0) = γ(t|∅) = b²κ²(n−1)²(n+1)/n², which is of order κ²nb² and matches the B2 bound up to constants.
- The second half, "absent for card(T) = 1", is asserted without a computation (E3).

**Derived texts** (asked in the brief).
- STATEMENT:3–8 is faithful. It says κ, b, M fixed was "made explicit" and that no conclusion or constant changed; both are true of the current text. Its silence on the hypothesis change is a record matter (E1).
- ASSUMPTION_MAP rows 13, 16, 20, 21 and 23 match the current statements; row 26 is loose (E4).
- REPORT §2 does **not** state A1, A1°, SCR-G(ii), SCR-C or SCR-R faithfully (Findings 1–3).

## 3. Per-claim table (21 rows)

| id | decision | lines checked / reason |
|---|---|---|
| CC | ACCEPT | CODE_CHECK CC1–CC6 against v3_engine.h:87–100, 379–419; v3_ledger.h:84–112 (offer only on fresh events; the only non-emitting eval is the final search's initial centre = current HPM); v3_core.cpp:395–481; v3_run.R:136–200; v3_exact.R:15; v3_score.h:14, 57–72, 175–235; v3_preprocess.R:21 (K) |
| L1 | ACCEPT | L1.1–L1.7 re-derived (variational form, Schur/rank-one, prior ratio, D-bounds, L1.5/L1.5° penalty domination, augmented representation) |
| L2 | ACCEPT | E1 (one Gaussian per S via deterministic witness), E4, E2⁺/E2⁻ (Laurent–Massart, AM–GM), E2ᶜʰⁱ, E3a (T3), E3b |
| SCR-A | ACCEPT | L3:6–24 |
| A-inf | ACCEPT | L3:26–35 |
| SCR-Ao | ACCEPT | L3:37–56 (Step 1 AM–GM, Step 2 with ρ̄(n−1) ≤ T_n, σ ≤ σ_S) |
| Ao-inf | ACCEPT | L3:58–63 (ϑ° → 0 iff the ‖μ‖ = o(nσ) term vanishes) |
| SCR-M | ACCEPT | L7:31–58 (both branches of b_𝓗, c_𝓗; numerator/denominator; gap), M1, M2, M3, M5, M6 |
| SCR-G | ACCEPT | STATEMENT:132–145, L7 M2/M4/M5 and 107–110; REPORT summary F (Finding 3) does not affect the claim text |
| B1 | ACCEPT | L4.0, L4:105–108 |
| B2 | ACCEPT | L4:110–119 |
| B2o | ACCEPT | L4:121–133 (u ≥ u₀ ≥ 2c_θ, monotonicity in u and V) |
| B2d | ACCEPT | L4:135–143 (only the first inequality uses the floor) |
| B3 | ACCEPT | L4:145–150 (Schur complement eigenvalue bound) |
| A1 | ACCEPT | STATEMENT:158–163, L3:65–76 (re-derived above); REPORT summary F (Finding 1) does not affect the claim text |
| A1o | ACCEPT | L3:78–86 (B2° with κ ≤ φ^d, the min-split, 8𝐋_n vs 4𝐋_n); REPORT summary F (Finding 2) |
| SCR-C | ACCEPT | L5:81–103 (x = 2log n, x′ = (ε/8)log n, Λ_k lower bound, comparison ≥ (ε/2)𝐋 − O(√𝐋)) |
| L5.1 | ACCEPT | L5:7–58 (facts (a)–(c); Steps 1–3; probability 1 − (1+2q)e^{-x} − e^{-x′}/(1−e^{-x′})); STATEMENT:177–192 incl. the m = 1 α-bound |
| L5.2 | ACCEPT | L5:71–79 ((EC) violated ⇒ (EC′) violated via α ≥ φ, ω ≤ 1/φ, Λ increasing; φ_n ≤ 1) |
| SCR-R | ACCEPT | L5:111–119 (P_CC = P_C for centred columns; E3a second part; XG⁻²Xᵀ ⪯ λ_min⁻¹P_C) |
| SCR-N | ACCEPT | L6:5–52 (★ at ∅, B_n bounds, union bounds 2e^{-x}, E2⁻; Consequence 1 and 2 sequences re-computed) |

## 4. Findings

**Finding 1 — F — REPORT.md:27–29 (A1 summary omits two stated hypotheses).**
- Quoted text: "Sparse eigenvalue floor κ … fixed coefficients (θ_min ≥ b, ‖θ*‖₁ ≤ M), (q_n + 1) log p + log n ≤ c₁n with c₁ = κ²b²/(200(M² + σ²)): the probability → 0."
- What fails: STATEMENT:159–160 assumes "κ, b, M, σ fixed (not depending on n)". The REPORT fixes only the coefficient bounds b and M. The package's convention (STATEMENT:19–21: σ may vary with n, and "where a result needs … σ fixed it says so") therefore reads the REPORT as claiming A1 with κ_n and σ_n free to vary. That is more than STATEMENT proves.
- Mitigation: the claim is true. σ is unused, and κ ≤ M/b (L7:103–104) together with the growth condition gives the large-n step (BT1). So nothing false is asserted, but the derived text does not match the authoritative statement.
- Fix required: write "with κ, b, M, σ fixed (not depending on n)" in REPORT:28. Alternatively, adopt BT1 in STATEMENT/L3 first and then summarise that version.

**Finding 2 — F — REPORT.md:30–31 (A1° summary states a false sufficiency).**
- Quoted text: "Each missing truth competes against the residual scale of the model at hand, not the total signal: beta-min θ_min ≥ 16σκ^{-1}√(((q_n+1) log p + log n)/n) suffices (no fixed coefficients)."
- What fails: STATEMENT:165–169 also needs 𝐋_n = o(n), s₀𝐋_n ≤ κn/576, ‖θ*‖₂ ≤ ½√(κ(n²−1))θ_min and ‖μ‖ = o(nσ). Its own parenthetical says "The total signal is still restricted by ‖μ‖ = o(nσ)".
- The REPORT sentence is false as stated. Counterexample, analytic and checked numerically in scratch `a1o_counter.py` / `.out`:
  - orthogonal design (κ = 1), n = 20000, p = 10, s₀ = 2, q = 1, σ = 1;
  - θ₂ = 1.01 × the beta-min level (0.431), with s₀𝐋_n = 29.0 ≤ n/576 = 34.7;
  - θ₁ = 10⁵, which violates ‖μ‖ = o(nσ) (‖μ‖/(nσ) ≈ 707);
  - {1} is LO and misses truth 2: F({1,2}) − F({1}) = −7.1 and no neighbour improves.
- Mechanism: the ridge-shrunk huge truth sets σ_S² ≈ σ² + θ₁²/n², which is exactly the "total signal" the sentence says does not matter.
- Fix required: state A1°'s full hypothesis list in REPORT, at least "and ‖μ‖ = o(nσ), s₀𝐋_n ≤ κn/576", and delete "not the total signal". REPORT:50 ("fixed coefficients → beta-min at rate σ√(𝐋_n/n)") should carry the same qualifier.

**Finding 3 — F — REPORT.md:36–37 and 42–45 (SCR-G(ii), SCR-C, SCR-R summaries drop hypotheses).**
- SCR-G(ii), quoted: "if a search stops on its move cap, its returned model contains S₀ whenever its last scanned centre is within c₂n of the best score".
  - STATEMENT:138–139 requires C and N "both of size ≤ q_n". M2 needs C ∈ 𝓗 and M5 needs N ∈ 𝓗. For larger sizes the package says the question is open (ASSUMPTION_MAP:22).
- SCR-C, quoted: "with s₀ bounded and a floor φ ≥ … a sparse certified model equals S₀ with probability → 1".
  - It omits the screening hypothesis ((A∞) or (A°∞)), ‖θ*‖₂ = O(σ√n) and q_n log p = o(n) (STATEMENT:172–173).
  - Without screening the claim is false; REPORT's own weak-signal numerics (line 92) show this.
- SCR-R (REPORT:44–45) omits "under the hypothesis of (A∞) or (A°∞)" (STATEMENT:196).
- Fix required: add "(C, N of size ≤ q_n)" to (ii), "under the screening hypothesis of (A∞)/(A°∞), ‖θ*‖₂ = O(σ√n), q_n log p = o(n)" to SCR-C, and "under (A∞)/(A°∞)" to SCR-R.

**Finding E1 — E — STATEMENT.md:3–5, REPORT.md:7–9 (record).**
- STATEMENT calls the A1/SCR-G change "made explicit", and REPORT calls all six post-pass applications "wording edits".
- Adding "κ, b, M fixed" to A1/SCR-G restricts the stated hypotheses (as PC_SCR_sol says), even though the current proof needs and uses exactly that restriction.
- The current statement is not affected. Suggest: "A1/SCR-G: κ, b, M, σ fixed now stated (scope restriction; re-scored in R2)."

**Finding E2 — E — numerics/core_copy/SHA256SUMS_source.txt.**
- `sha256sum -c` fails on 18 of 18 files in this checkout. The recorded hashes are of CRLF bytes while the checkout is LF.
- The content is identical to production and to 2252d57 after line-ending normalisation (scratch `hashcheck.txt`).
- Suggest recording LF-normalised hashes or noting the byte convention.

**Finding E3 — E — ASSUMPTION_MAP.md:1, 20.**
- The header says "for STATEMENT v3.3", but row 20 was edited for v3.4.
- Row 20's "absent for card(T) = 1" has no computation behind it. Heuristically γ ≈ θ_t²‖(I−P_S)x_t‖² is linear in κ, up to ridge terms.
- Row 20 writes γ(t, ∅) where the package notation is γ(t|∅).

**Finding E4 — E — ASSUMPTION_MAP.md:26.**
- "a scanned centre within δ of the best score, or the returned model of a capped search whose last centre is, suffices" leaves out "C (and N) in 𝓗".
- δ is defined only on 𝓗, so the row is not wrong, but adding "in 𝓗 (size ≤ q_n for SCR-G)" would match STATEMENT:137–139.

**Better-theorem notes (not findings).**
- **BT1 (A1).** σ fixed is unused, and κ need not be fixed. If b and M are fixed (or more generally M/b ≤ 50(n²−1)log n/n), the growth condition gives the large-n step:
  - κ²b² ≥ 200M² log n/n, and κ ≤ M/b,
  - so κb²(n²−1) ≥ κ²b²(n²−1)b/M ≥ 200Mb(n²−1)log n/n ≥ 4M².
  - The rest of the A1 proof is exact for each n.
- **BT2 (A1°).** The hypothesis ‖θ*‖₂ ≤ ½√(κ(n²−1))θ_min is implied by ‖μ‖ ≤ nσ and the beta-min condition, for n ≥ 3:
  - ‖μ‖² ≥ φ^d(n−1)‖θ*‖₂² (take S = ∅), so ‖θ*‖₂ ≤ nσ/√(κ(n−1));
  - and nσ/√(κ(n−1)) ≤ 8σκ^{-1/2}√((n²−1)𝐋_n/n) ≤ ½√(κ(n²−1))θ_min whenever n³ ≤ 64(n−1)²(n+1)𝐋_n.
  - So the hypothesis is redundant under ‖μ‖ = o(nσ).

## 5. Gates

- G1 (every step correct): **PASS**. Every proof step I re-derived for the 21 claims is correct.
- G2 (hypotheses used = hypotheses stated): **FAIL**. STATEMENT and the lemmas are consistent (A1, SCR-G and M4 now state κ, b, M, σ fixed and use them). The derived REPORT §2, however, states A1, A1°, SCR-G(ii), SCR-C and SCR-R with fewer hypotheses than STATEMENT (Findings 1–3, F).
- G3 (no hidden assumptions): **PASS** for STATEMENT and the lemmas. EX-A and Model G are named, and nothing about the start mode, leakage or blocks is used.
- G4 (cited results have adequate status): **PASS**. Laurent–Massart Lemma 1, Gaussian concentration (Boucheron–Lugosi–Massart Thm 5.6) and Schur-complement facts are standard.
- G5 (constants and rates tracked): **PASS**. Checked: c₁ (ρ² ≥ 200/64), c₂ (u*/4, n ≥ 34), M3 thresholds L′/(n−0.98) and L′/(n−1), SCR-C (ε/2)𝐋 and the B_n bounds.
- G6 (fidelity to the code): **PASS**. CC1–CC6 hold on the current core, which is identical in content to 2252d57.

## 6. Score

**8.6.** The mathematics of all 21 claims is correct and complete on the current text. The v3.4 fixed-parameter edits to A1, SCR-G and M4 are confirmed, and so are the M6 correction and the two-truth construction. The deductions are only for the derived-text infidelities in REPORT §2 (Findings 1–3). The A1° sentence is the most serious, because it is false as stated. Each is fixed by restoring the STATEMENT hypotheses in REPORT.

`COUNCIL-VERDICT round=R2 manifest=96488f34902506d5cecf92b85aa257627ca396cdd7d3e60b86db32f688300b93 seat=opus score=8.6 gates=FAIL`
