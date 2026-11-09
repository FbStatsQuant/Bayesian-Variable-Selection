# C-MIS — council round 1, seat Claude Opus 5.5 (R08)

Scope read: STATEMENT.md (v1.1 + logged edits), lemmas/00_MAIN.md, L1–L6, numerics/SUMMARY.md, reviews/CITECHECK.txt.
I checked these against: SoP `04_theory.tex` TH09 card (761–822) and M5 status line (466); `02_method.tex:84-135`; T03R
`PROOF.md` §§3–6 (E2, Lemma B, (C1)–(C10)); [P3] `PROOF_v2.tex` (lem:smoother, cor:diff, lem:det, (G1)–(G4), δ_n, δ''_n,
η_n, lem:ongood, lem:onesup, prop:sup, lem:SvsSp, lem:signalgain); `00_COMMON.md:9-14,35`; T38 `T38_PROOF.md:10-46`; GEN
STATEMENT §§1–3, REPORT:15-45, L5.3–L5.4, L6(c); Song–Liang (2015) p. 957. LOG.md and other reviews were not read.
Brief: try to break the package. I re-derived every changed inequality. I did not just check that a cited line exists.

## What I verified line by line

**Reduction and de-randomisation (L1).**
- Lemma R is exact: ε + ξ ~ N(0, (σ² + τ²)I) given X^r_𝒞, and the run depends only on (X^r_𝒞, y^r, uniforms). π depends
  on y^r only through Cy^r, so α + a is irrelevant (00_COMMON:9).
- MIS (i) is T03♯ applied to (X^r_𝒞, β^𝒞, σ_𝒞²). T03♯ conclusions (i)–(iv) are statements about the law of π or are
  pathwise, so the transfer is legitimate. Proxy and cancellation consequences follow from (ii).
- Corollary N holds: the sample-projection slopes are β^𝒞 + (AᵀCA)⁻¹AᵀCξ. These are a.s. dense when τ² > 0. The
  unconditional bound 1{T_n ≠ S₀^𝒞}π(T_n) ≤ 1 − π(S₀^𝒞) is correct.
- Lemma DR is correct. Monotonicity in L gives f^{L₀}_{n_L} ≥ f^{L}_{n_L} for L ≥ L₀, and the diagonal sequence
  contradicts the hypothesis. No measurability of the sup is needed, because the bound
  P(Y_n > Lr_n) ≤ sup f + P(𝒜ᶜ) is an outer bound.
- MIS (ii)'s f_n^L is a valid version of the conditional probability, because ε′ ⊥ X^r_𝒞 with a fixed law.
- MPM, S† and E Y_n → 0 follow correctly.

**Gaussian conditioning (L2).**
- P(a): the conditional law of x_𝓜 | x_𝒞 and ζ ⊥ X^r_𝒞 are standard. ξ_i = ζ_iᵀβ_𝓜 is iid N(0, τ²), and a matches.
- P(b): cov(x_𝒞, y) = Σ_𝒞𝒞β_𝒞 + Σ_𝒞𝓜β_𝓜. The R06 example (slope 0 vs ½) is correct.
- P(c): from ΣΘ = I, Θ_𝒞𝓜 = −Σ_𝒞𝒞⁻¹Σ_𝒞𝓜Θ_𝓜𝓜 and Σ_{𝓜·𝒞}Θ_𝓜𝓜 = I. ✓
- P(d) and its S₀^𝒞 formula ✓. The partial-correlation sign identity ✓.
- E1: Θ_𝒞k = −Σ_𝒞kΘ_kk = (1, −1, 0), Θ_kk = 1/(3 − 2) = 1, γ = (−1, 1, 0), β^𝒞 = (0, 1, 0). ✓ The dense model is
  feasible once n ≥ 6 (K = 3). ✓
- GD(a): every defining inequality has slack. SLLN gives P(𝒜_n) → 1; only the marginal law at each n matters, so the
  triangular-array coupling is harmless. Interlacing gives SE_λ and SE_w (g₀ = 1 once Nφ₀² ≥ 1). BM-∞ via
  θ_j² = σ̂_j²β_j² ≥ κ. ✓
- GD(b):
  - UᵀX^r_𝒞 has iid N(0, Σ_𝒞𝒞) rows.
  - The χ² union bound uses x = (A + 2)log n, giving 2n⁻².
  - (DS) with t_k² = 2(k log p + 2 log n) gives 2n⁻² per size and 2k_n n⁻² in total.
  - √k_n + t_{k_n} = O(log n) = o(√N).
  - λ_min(R̂_T) ≥ (c₀/2)/(2C₀) ≥ c₀/(8C₀).
  - ‖Wβ‖² ~ (βᵀΣβ)χ²_N ≤ 2NM₀.
  - The BM envelope algebra ✓.

**Theorem F (L4).** I re-derived:
- Lemma S, including rᵀỹ = rᵀe and the exact rate shift b_y − b̃ = b₀c_n/N.
- (G5) consequences: c_n ≥ −2σ² log n and c_n ≤ NΔ_n + Nσ²_{𝒞,n}√(2 log n/N), using 2σ√Δ ≤ σ² + Δ.
- L4.4(b): the cross term rᵀP_Se = 0.
- L4.4(c): ‖(I − P_{S′})y_c‖² ≤ ‖r + e‖². Both bounds on E_n^𝒞 hold: (3 + √2) ≤ 5 in δ''^𝒞_n, and NΔ_n + Nσ² = Nσ²_{𝒞,n}.
- (C4): (P_S − P_{S₀^𝒞})r = 0 and the lower denominator bound from L4.4(b).
- (C6)(b): [P3] lem:SvsSp uses lem:ongood(d) with B = E_n, so B = E_n^𝒞 ≥ Nσ²(1 − δ_n^𝒞) is exactly the right
  replacement. The n²/(n² − 1) algebra gives V/(8σ²_{𝒞,n}).
- (C7): P_{S′}μ^𝒞 = μ^𝒞 and N_S ≤ σ²C_* log n ≤ σ²_{𝒞,n}C_* log n.
- (C10): c₀ = L_* is unchanged, and BM^𝒞 is stated with σ²_{𝒞,n}.
- Step 0 → TAIL^𝒞. The assembly partition is exhaustive.
- δ_n^𝒞 log n → 0, so ε_n^𝒞 → 0.

**Corollary F(a) and Lemma T.**
- F(a): R_m depends only on (p_𝒞, s₀^𝒞, m) once K = p_𝒞. The family is finite, so r_min > 0 and m♯_n = K eventually. ✓
- Lemma T:
  - Uniform denominator: ‖e‖² − ‖P_Ve‖² ≥ σ²(N − d) − 5σ²√(N log n) − 2σ² log n.
  - νn/((n+1)N) = ½υ⁰_n.
  - t_n ≤ t̄ gives 1 − 2t̄ = ¼ + 3κ/8 and ρ ∈ (0.63, 1).
  - The exact χ²_{r_J} mgf holds without full rank (P_{S′} − P_{S₀} is a projection).
  - lem:prior(b) and the 2^s multiplicity ✓.
  - (C6)(a) needs no eigenvalue condition. D_{S′}/D_{S₀} ≥ 1 because f ≥ 1.
  - n^{sA}n^{s/2}·n^{−(s(A+½)+1)} = n⁻¹.
  - ρ̃_n → 0 since nη_n = O(1/n).
  - The only eigenvalue hypothesis used is R on S₀^𝒞, as claimed. This lemma is genuinely new and correct.

**Lemma Z, O1, O2, E2, E3.**
- Lemma Z: D_S ≥ f(g₀)^k, t_S ≤ ‖P_𝒞e‖², and the lower bound ‖r‖² + 2rᵀe ≥ −σ_*²Z². C(p,k)/C(2p−1,k) ≤ 2·2^{−k}. The
  geometric sum is ≤ 2e^{Λ_n}a_n, and Λ_n = O_P(1). ✓
- O2: the mixture is bounded by the sup of the Gaussian likelihood, and v̂_S ≥ ‖(I − P_V)y_c‖²/N. ✓ The consequence
  paragraph is now correctly limited to the technique.
- E2: conditioning on Z, then T03♯ for each z ≠ 0, then dominated convergence. ✓
- E3 ✓.

**Corollary H and Corollary D.**
- H: each of the five T38-(0) steps uses S₀ only through "π(T) > ½ ⇒ T is the strict maximiser". ✓
- D: Lemma R transfers the whole run law to GEN's model G with σ_𝒞².
- D′: σ² enters GEN L6(c) only in BM, VIS (factor-3 margin: ¾√n vs √n/4·(1 + o(1))) and NL/E_{T,l}, with
  δ² = O(n^{−7/6}) independent of σ². ✓ The remark that the proxy correlation θ_n/τ → 0 is honest.

**Fidelity to the method.**
- Shipped g = n ridge score, ν = a₀ + n/2, and in the contrast experiment IG(0.51, b) with b = b₀‖y_c‖²/N
  (`02_method.tex`, Reduction statement).
- w(k) = ½/C(2p_𝒞 − 1, k), K = min(p_𝒞, ⌊n/2⌋), candidate-only standardisation and partition.
- Reported HPM = ≻-maximum of the scored set.
- No full-p conditioning anywhere. No raw-likelihood substitution: the actual response-dependent rate is kept and
  bounded through the full mean.

**Statuses.** These are verbatim and not upgraded: T03♯ (card 765/798); T01–T03; T38-(0) (SoP 466); GEN "PROVED-CHECKED"
with e4 / N3 OPEN. The TH09 onset (≈2·10⁶) is explicitly not transferred. TH09's "no random-design extension" is
respected: MIS (ii) is new content proved here via Lemma DR, not attributed to TH09.

**Song–Liang comparison.** Theorem 4 (density consistency, a.s.) and Corollary 2 (π(s̃ ⊂ ξ) → 1 in probability, under no
exact multicollinearity) are described accurately (p. 957). The package claims a stronger conclusion under stronger
hypotheses (GR / jointly Gaussian rows, fixed σ_𝒞², fixed s₀^𝒞, T03♯ eigenvalue and BM conditions). It flags that
β^𝒞 = SL's β₀ only for centred rows. It claims no density-contraction analog. No overclaim found, apart from minor m5.

**Frontier.** Stated honestly:
- The (TL) window for growing p_𝒞.
- Nothing outside GR; N5 is labelled exploratory.
- Full-rank designs reduce to representability.
- O2 is an obstruction to one technique only.
- Growing s₀^𝒞 (one-factor example) and n-dependent τ_n² are excluded.

**Numerics.** Used only as falsification. Consistent with every claim (N3 Δ = 4 shows the σ²_𝒞 dilution; N7
reproduces E1). The check_L4 pathwise inequalities show no violation.

## Findings

No fatal or major findings.

**Minor**

m1. `STATEMENT.md:42-43` (D0, "Valid inputs … under every model below this holds almost surely"). This is overstated:
for fixed designs (MIS (i), Theorem F, Lemma Z, E2/E3), non-constant candidate columns are a hypothesis. For a general
random design in MIS (ii) it holds only if 𝒜_n enforces it. The SE_λ(j₀) inequalities on every S₀ ∪ {j} implicitly
require standardisable columns, so nothing breaks.
*Fix:* "Valid inputs: … ; y^r is non-constant a.s. under every model below; non-constant candidate columns are assumed
for fixed designs, hold a.s. under jointly Gaussian rows, and are part of 𝒜_n in MIS (ii)."

m2. Internal status inconsistency.
- `lemmas/L5_frontier.md:78` heads §6 "PROVED (by this seat, unchecked)", but the status line `L5_frontier.md:3-4` says
  "§6 Examples E2, E3 — … R05 VERIFIED".
- `lemmas/00_MAIN.md:7,12,18,19`, column "Checks", says only "added after R04" for Corollary N, E1, Lemma Z and E2/E3.
  The lemma files record R05 VERIFIED / VERIFIED-WITH-AMENDMENTS.

*Fix:* make the §6 heading read "(from R04; R05 VERIFIED)" and add the R05 verdicts to the four 00_MAIN rows.

m3. `lemmas/00_MAIN.md:10` writes "precision of the marginal (x_𝒞, x_𝒪)". 𝒪 is reserved for the output-available event
(`STATEMENT.md:44`). *Fix:* replace it with x_𝓜.

m4. Notation clash in `lemmas/L2_gaussian.md:75-78`. GD(b) names the population restricted-eigenvalue floor c₀
("λ_min(Σ_TT) ≥ c₀", "φ₀² := c₀/(8C₀)", "n₀(s, A, c₀, C₀, M₀)"). c₀ is the beta-min threshold c₀(s, A) used throughout
(MIS (ii) "fixed c > c₀"; brief: "c₀ unchanged"). *Fix:* rename the floor to λ₀ (or c_Σ) in lines 75–81 and the proof
step (2) at lines 95–99.

m5. Statement-level precision on Song–Liang, `STATEMENT.md:88-89` (GD(a): "the inclusion clause recovers SL's full
Corollary 2 conclusion (π(S₀^𝒞 ⊆ S) → 1)"). SL's conclusion concerns s̃, which equals S₀^𝒞 only for centred rows. The
sentence also sits inside the jointly Gaussian special case of SL's setting. (`L2_gaussian.md:62-63` carries the
qualifier; the STATEMENT sentence does not.)
*Fix:* "… recovers, in the jointly Gaussian special case, SL's Corollary 2 conclusion (π(S₀^𝒞 ⊆ S) → 1; S₀^𝒞 = s̃ for
m = 0, its intercept-adjusted analogue otherwise)".

m6. Corollary N is listed in the proof map as a claim of "STATEMENT.md v1.1" (`00_MAIN.md:3,7`). The STATEMENT contains
only the proxy/cancellation consequence sentence (line 67) and E1. The sample-projection claim (T_n = 𝒞 a.s. when
τ² > 0, `L1_reduction.md:69-74`) is not in the STATEMENT.
*Fix:* add one sentence after `STATEMENT.md:68`: "Corollary N (L1): every T ≠ S₀^𝒞 has π_𝒞(T | y) ≤ 1 − π_𝒞(S₀^𝒞 | y);
in particular π_𝒞(S₀ ∩ 𝒞 | y) → 0 when S₀ ∩ 𝒞 ≠ S₀^𝒞, and the (a.s. dense, τ² > 0) sample-projection support gets
vanishing mass." Alternatively, mark the row as a remark.

m7. Fidelity caveat not carried into the STATEMENT. Corollary D is about "method v3.1 + LS0" (`STATEMENT.md:111`,
`L3_hpm.md:33-34`), but neither file carries GEN's flag that LS0 is not in production code (GEN REPORT flag 4: "about
v3.1 + LS0 as specified (LS0 is not in production code)"). *Fix:* append "(LS0 as specified; not in production code —
GEN REPORT flag 4)" to both places.

m8. Cosmetic, `L4_theoremF.md:178`. The bound ρ̃_n ≤ 3υ⁰η_n n(M + σ²)/(σ²(1 − ζ_n)) is valid but loose by a factor 2
(½·4·¾ = 3/2). There is no consequence, since only ρ̃_n → 0 is used. *Fix (optional):* write 3/2, or say "≤ (crudely)".

m9. Frontier completeness, `STATEMENT.md:143-160`. Theorem F, Lemma T and Lemma Z are fixed-design only. A random-design
EP version is neither claimed nor listed as open. *Fix:* add a bullet under §5: "Random-design versions of Theorem F /
Lemma T (EP with random full design) are not claimed; the Lemma DR route would need EP and (TL) on design envelopes."

## Gate verdicts

1. Correctness of every step — **PASS**. Reduction, de-randomisation (Lemma DR), Gaussian conditioning, every changed
   T03♯ step ((G5), δ_n^𝒞, E_n^𝒞, (C4)–(C10)), Lemma T, Lemma Z, the corollaries and E1–E3 were re-derived without
   error. m8 is cosmetic.
2. Hypotheses used = hypotheses stated — **PASS**. Candidate-only rerun, fixed σ_𝒞² (made explicit in P(a) and GD(b)),
   s₀^𝒞 ≥ 1 (Lemma Z separate), envelopes with fixed constants, and GEN premises with σ² := σ_𝒞² everywhere. m1 is a
   wording fix.
3. No hidden assumptions — **PASS**. Measurability, independence of uniforms, valid inputs and the τ² > 0 → random-omitted
   requirement are all explicit or harmless. m1 should still be fixed.
4. Cited lemmas have adequate status — **PASS**. Cited statuses are verbatim and none is upgraded; e4 / N3 OPEN and the
   "SAME-FAMILY-ONLY" qualifier are carried. Internal labels are inconsistent (m2) but not upgraded.
5. Constants / rates / thresholds tracked — **PASS**. δ_n^𝒞, δ''^𝒞_n, E_n^𝒞, c₀ = L_* unchanged, m^T_n explicit,
   O_P(r_n) and O_P(n^{−1/2}) rates, no expectation rate, no transferred onset. m4 is a symbol clash.
6. Fidelity to the method as coded — **PASS**. Shipped score, IG(0.01, 0.01) with the response-dependent rate kept,
   BB(1, p_𝒞) weights, cap K, candidate standardisation and partition, reported HPM over the scored set. m7 is a caveat
   to carry.

Also judged: no overclaim relative to Song–Liang (m5 is a wording tightening). The frontier is honestly stated (m9 adds
one line).

This is a clean, well-scoped package. The reduction is exact, the Theorem F rerun is meticulous, and Lemma T is a real,
correct contribution with a sharp, honestly reported window. The deductions are only for bookkeeping and wording.

SCORE: 9.0/10
