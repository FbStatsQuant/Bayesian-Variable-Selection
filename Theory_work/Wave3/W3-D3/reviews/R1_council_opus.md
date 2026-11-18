# W3-D3 — council R1, seat `opus` (Claude Opus 5.5, high; blind first read)

Manifest reviewed: `MANIFEST de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768`. I re-ran
`Theory_work/Wave3/tools/manifest.py verify` on the worktree before reading and got "verify: OK" for that digest. The only
working-tree change is `LOG.md`, which the manifest excludes and which I did not read. Files read: the brief,
`reviews/MANIFEST_R1.txt`, `reviews/INPUTS_R1.txt`, `reviews/CITECHECK.txt`, STATEMENT.md (v1.2), lemmas/B3w.md,
lemmas/ASSEMBLY.md, REPORT.md, TARGET.md, READER_DELTA.md, PLAN.md, DEPS.tsv, deps_hand.py, citecheck.py (header),
API_CARD.md, api_request_build.py (skim), numerics/N1_*.py/out and N2_*.py/out. I also read every INPUTS_R1 source that
the proofs cite: W3-POST STATEMENT :1-127; W3-DIST STATEMENT :14-34, :158-165, :380-417; [EB] B0, B1, B2core, B2, B3 in
full; R1_set_sizes; READER_VERSIONS :20-40, :255-292, :1090-1102; NOTATION :1-40; CLAIMS_CARD :50-58; L1_POST in full.
I opened no other file in reviews/. With git, read-only, I checked that all 12 external inputs are byte-identical at
029bb748, at 968f19d1 and in the worktree (STATEMENT :17's claim holds).

## (a) Per-claim decisions

| id | decision |
|---|---|
| W3-D3:Thm2SG | ACCEPT |
| W3-D3:B3w | ACCEPT |
| W3-D3:ExSG | ACCEPT |

All three proofs are correct as written. My one non-editorial finding (S1) is in REPORT §3's card text, not in a
registered span or a proof. It does not affect the claim decisions, but under the brief it makes `gates=FAIL`.

## (b) Findings

**S1 (REPORT card text claims more than STATEMENT): `REPORT.md:34`, also `:35-36`.**
(i) The parenthetical "(… correlated mixtures of independent features, each sub-Gaussian or bounded by a fixed multiple
of its standard deviation, also qualify)" drops the uniformity that ExSG (a) needs. ExSG (a) asks for
E exp(λξ_k) ≤ exp(L²λ²/2) with one fixed L for unit-variance ξ_k (STATEMENT.md:85). The phrase "each sub-Gaussian" has
no common constant and no "at the scale of its standard deviation".
*Counterexample to the sentence as written:* take standardised Bernoulli(p_n) features with p_n → 0, mixed by B = I.
At every n each feature is bounded, hence sub-Gaussian, so the features are "each sub-Gaussian". Yet (A4) fails for every
fixed L. STATEMENT §4 (b) (`STATEMENT.md:98`) and READER_DELTA :55 say exactly this, and STATEMENT §5 :141 rejected HQ's
first wording for the same reason. The bounded clause in the same sentence correctly says "a fixed multiple"; the
sub-Gaussian clause does not.
(ii) ":35-36 This contains the isotropic sub-Gaussian rows of Narisetty and He … and implies Song and Liang's Condition 1"
drops the qualifiers that STATEMENT §5 :116-117 attaches: "[for centred rows, with L a fixed multiple of their
sub-Gaussian constant]" and "[for z = x − m_n]". The centring matters mathematically. A non-centred row with E xxᵀ = I and
mean m ≠ 0 has covariance I − mmᵀ, which is not a correlation matrix, so it is not in the class of Theorem 2SG.
*Fix (one line each):* "each sub-Gaussian with a common constant L at the scale of its standard deviation, or confined to
K standard deviations of its mean"; "the centred isotropic sub-Gaussian rows of Narisetty and He (2014, Lemma 6.1) …
implies Song and Liang's Condition 1 for x − m_n".

**E1 (changelog check cell stale): `STATEMENT.md:188`.** The 1.1 ExSG (b) row says check = "statement-change check
(pending; Opus diff round)". REPORT.md:44 says the statement-change check v1.0 → v1.1 was part of K1. I could not open K1
under the brief, so I did not verify the K1 side. Update the cell to name the review file, or keep "pending" and say why.

**E2: `TARGET.md:9`.** The class column says "1 (proposed; …)". STATEMENT §5 :111 records HQ's ruling (class 1, with a 2b
backup). Make the two agree.

**E3: `TARGET.md:14`.** "(Rademacher, uniform, and a correlated Rademacher mixture)": N2 runs Gaussian, Rademacher and
uniform ξ, all mixed by the same AR(1) Cholesky factor (`N2_subgauss_rows.py:84-98`). There is no separate "correlated
Rademacher mixture"; the Rademacher run is that mixture. Also, the N2 docstring (:3-4) writes K for the constant L.

**E4: `STATEMENT.md:88`.** ExSG (b): "it holds with L = K whenever ξ_k takes its values in an interval of length 2K".
(a)'s scalar hypothesis quantifies over every k with one L. Write "whenever every ξ_k takes its values in an interval of
length 2K (the same K for all k)". The proof (ASSEMBLY :79-80) is per coordinate, so it already gives this.

**E5: `STATEMENT.md:73-79`, `B3w.md:34-40`.** 𝒜′_n is well defined only for n ≥ n₁: (F_w) uses m♯_n, which needs
s₀ ≤ min(p, ⌊n/2⌋). Item 6 is asymptotic, so this is harmless, but one clause would close it: "for n < n₁ put 𝒜′_n := ∅".

**E6: `citecheck.py:9`.** The docstring says the statuses are "quoted in STATEMENT §5"; they are in §6, and CITECHECK
reports §6. Docstring only.

No C or F findings.

### Step-by-step verification record (what I checked; all OK)
- **Window coverage (B3w Step 0).** (1) R1 B1.2 gives s₀ + j₀ ≤ (2A+2)s₀ + 2. Since 5 log 3 = 5.493 ≥ 5.49, W̄_n ≥ 5.49(As₀
  + A + s₀ + 1) ≥ 2As₀ + 2s₀ + 2, so |S₀∪J| ≤ ⌊W̄_n⌋ = q_n and ≤ p. (2) R1 B1.3 applies (n ≥ 3, A ≥ 1, s₀ ≥ 1, s₀ ≤ K,
  p ≤ n^A for the p in which m♯_n is computed), giving s₀ + m♯_n ≤ 3(A+1)(s₀+1) log n ≤ W̄_n. N1 recomputes m♯_n exactly
  from W3-POST :36-37 (threshold n^{−(s₀+2)/2} = n^{−(s₀+1)/2}e^{−½log n}, correct) with 0 violations. Every set used in
  (F_λ), (F_w), B2-core and B2 (a) lies in the windows of (A3) and (A4).
- **B2-core's size condition.** q′ = min(q_n, p) = w_n ≥ 1, and 0 ≤ log(ep/w_n) ≤ 1 + A log n, so
  q′log(ep/q′) ≤ W̄_n(1 + A log n) ≤ c₂n/L⁴ for n ≥ n₁. n₁(s₀, A, L) is finite (the left side is O(log²n)) and ≥ 3, as
  B1 (a) needs. B2-core's other hypotheses hold: E z = 0, Var z_j = 1, q_n ≥ 1 is an integer, and (SG_{q_n}) is (A4)
  restricted to u with ≤ q_n ≤ W̄_n nonzero entries, with Var(uᵀz) = uᵀΣ_nu. B1's (SG₁) is (A4) at u = e_j, using
  W̄_n ≥ 1 and Σ_{n,jj} = 1.
- **Constants after B0.** B0 (a) and (e) apply: n ≥ 3, p_ret ≥ 1, non-constant y^r, and the rows satisfy (RD) of W3-DIST
  :19-22 (i.i.d. (x_i, y_i), Gaussian noise independent of the design, fixed s₀, p ≤ n^A).
  - M_E: B1 (c) with b̄ = b_hi/σ*, σ* = 1, |supp β̃*| ≤ s₀ gives ‖μ̃‖² ≤ n·2s₀²b_hi²/σ*².
  - (F_λ): with B2's identity G_T = nΛ_TΣ̂^z_TΛ_T (Σ̂^z is n⁻¹-normalised and centred, consistent with B2-core :16), 𝓔₂,
    (A3) and ŝ_j² ≤ 2 give λ_min(G_T/(n−1)) ≥ φ²/4.
  - (F_w): B2 (a) with c_ψ = φ² ≥ φ²/n gives φ²/4 ≥ φ²/8 = g₀.
  - BM: θ̃*_j² = ŝ_j²β*_j²/σ*² ≥ b_lo²/(2σ*²), so θ̃*²_min nφ₀²/log n ≥ b_lo²nφ²/(8σ*² log n) = M_n → ∞.
  - Theorem 1's ranges: φ₀ = φ/2 ∈ (0, ½] ⊂ (0, 1]; g₀ > 0; M_E ≥ 0.
- **Probability (b).** P(𝓔₁ᶜ) + P(𝓔₂(q_n)ᶜ) ≤ 4pe^{−c₁n/L⁴} + e^{−c₂n/L⁴} ≤ 5n^Ae^{−c₂n/L⁴} → 0, using c₂ = 10⁻⁵ ≤ 1/576.
- **Completed pair and measurability (c).**
  - {p_ret = p} is Borel. On it, X and θ̃* = D_xβ̃* are continuous functions of the raw design, so (X°, θ°) is a Borel
    function of X^r and is independent of ε by (S1).
  - supp θ° = S₀ on every outcome: on {p_ret = p} because every ŝ_j > 0, and off it by the choice of θ⁰. With S₀ and m♯_n
    deterministic, 𝒜′_n is a finite intersection of closed conditions on (X°, θ°), hence (X°, θ°)-measurable.
  - 𝒜_n ⊆ 𝒜′_n ∩ {p_ret = p} by Steps 2–5, since m♯_n is computed with p_ret = p on 𝒜_n.
  - Item 6 and R1 are met: s₀ ≥ 1 fixed; 2 ≤ p ≤ n^A for the raw p, which is the completed design's dimension at every
    outcome; s₀ ≤ min(p, ⌊n/2⌋) for n ≥ 2s₀; noise ε/σ* ~ N(0, I) independent of (X°, θ°); X⁰ is centred with column
    norms n − 1, so it is a valid standardised retained design; constants and envelope are common; P(𝒜′_n) → 1.
- **Transfer (ASSEMBLY Steps 3–4).** On {p_ret = p}: X° = X and Y° = X°θ° + Cε/σ* = Cỹ (C idempotent, μ̃ = Xθ̃*). The
  coded posterior depends only on (X, Cy/s_y), so all outputs equal their °-counterparts, and the §0 conventions are not
  invoked. Off {p_ret = p} only P(p_ret ≠ p) ≤ P(𝒜_nᶜ) → 0 enters. Conclusions (1)–(3) follow by the stated union bounds.
  Conclusion (3) uses item 3's pathwise PIP ≤ δ bound.
- **Row 1.2's Gaussian steps (L1_POST).** Each is covered:
  - (2)–(3), the entrywise event 𝒢_n with Weyl: replaced by 𝓔₂(q_n) + B2 (a) + Step 3.
  - The raw-scale event ℋ_n (χ² tails): replaced by 𝓔₁ (B1).
  - p_ret = p a.s. (implicit in L1_POST): replaced by B1 (b) plus the completion (B3 A-2).
  - (1), the window: replaced by R1 B1.2, B1.3.
  - (4), energy: replaced by B1 (c).
  - (5), the diagonal transfer: unchanged, through item 6, and it uses only the Gaussian noise of (S1).
- **ExSG.**
  - (a): mean and covariance are correct; the product of the MGFs gives exp(L²λ²‖Bᵀu‖²/2) with ‖Bᵀu‖² = uᵀΣu.
  - (b), the three examples: Gaussian is exact. Rademacher uses (2k)! ≥ 2^k k!. Uniform has variance 1, and
    (2k+1)!/(2^k k!) = 3·5·…·(2k+1) ≥ 3^k.
  - (b), Hoeffding's lemma proved in place: the chord bound, θ = −a/(b−a) ∈ (0, 1), e^{λa} = e^{−θh}, ψ(0) = ψ′(0) = 0,
    ψ″ = ρ(1−ρ) ≤ ¼, and the Lagrange remainder give exp(λ²(b−a)²/8) = exp(K²λ²/2) for b − a = 2K. The degenerate
    a = 0 or b = 0 case is handled.
  - The eq. (4.16) citation is not checked against the 1963 paper; the in-place proof makes it non-load-bearing.
- **Unstated hypotheses.** None found. β*, α* are deterministic (§0); L > 0 is fixed; σ*² is fixed; s₀ is fixed; the
  row law is the same at each n, with p varying with n. Remark (d)'s "L ≥ 1 automatically" is correct by B1.0 (iii).

### Sweep (Tier B)
- **STATEMENT copies vs lemma statements.**
  - §2 vs B3w Statement: same objects and constants. The lemma is slightly stronger (p ≥ 2, φ₀ ≤ ½, and the 5n^A bound).
  - §3 vs ASSEMBLY's ExSG claim: verbatim.
  - B3w's quotations of B1, B2-core and B2 (a) match [EB] B1 :8-19, B2core :9-17 and B2 :18-24, :45-52.
- **Each lemma's scope vs its use.** B0 is used with n ≥ 3, p_ret ≥ 1 and (RD); B1 with Var ∈ (0, ∞) and n ≥ 3;
  B2-core with E z = 0, unit variances and q integer ≥ 1; B2 with p ≥ 2 and (A4_q) from (A3); R1 with n ≥ 3, A ≥ 1,
  s ≥ 1, s ≤ K and p ≤ n^A. All OK.
- **REPORT vs STATEMENT.**
  - The registry blocks' line spans (59-79, 41-57, 81-88, 23-39), conclusions, scope and depends_on match STATEMENT §§1–3
    and §7 and the proofs. B3w uses B0 (f), (e); Thm2SG uses B0 (a), (e).
  - §2 Caveats: n₁ "of order 10⁹–10¹¹" matches N1_out (8.9·10⁸ – 8.7·10¹⁰).
  - §5 is labelled OPEN where it should be.
  - The §3 card text is the exception: finding S1.
- **DEPS.** I recomputed all 10 span hashes with deps_hand.py's span rule, in memory without rewriting DEPS.tsv. Each
  equals both sha and checked_sha, with the stated line ranges. The named review files are off-limits under this brief,
  so I did not compare their contents.
- **Tags.**
  - STRONGER (§8) is correct against the reader statement [RV] :263-275. (A1)–(A3) and the conclusions are verbatim.
    Gaussian rows satisfy (A4) with L = 1 for every u. Reading p as the raw count changes nothing under Gaussian rows,
    because p_ret = p a.s. there.
  - The master comparison (fixed floor vs LSF's vanishing ψ_n; SL1 (a)–(e) not reproduced) is stated openly.
  - §9 tags are consistent with the diffs they describe, apart from the stale check cell in E1.

## (c) Interpretive sentences inside the registered spans (STATEMENT §1–§3)

| line | sentence | verdict |
|---|---|---|
| `STATEMENT.md:75` | "(X°, θ°) is a Borel function of the raw design, hence independent of ε." | checked (B3w Step 6; ε ⟂ X^r by (S1)) |
| `STATEMENT.md:77-79` | "Moreover (with (b): P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) → 0) the hypotheses of [W3P] Theorem 1 item 6 hold for (X°, θ°, ε/σ*) in regime R1 …" | checked (B3w Step 6 "R1 for the completed pair" and (b)) |
| `STATEMENT.md:86` | "In particular (A4) holds with this L." | checked (take m = m_n, Σ = Σ_n; (A4)'s u-set is a subset of all u) |
| `STATEMENT.md:51` | "(for instance, λ_min(Σ_n) ≥ φ²)" (example in (A3), recorded text) | checked (eigenvalue interlacing) |

No sentence needs to move out and none is false.

## (d) Gates

- **correct: PASS.** No C finding. Every step of B3w, ASSEMBLY and ExSG checks against STATEMENT and the cited sources.
- **strength: PASS.** The STRONGER tag is correct. No conclusion exceeds what is proved. B3w (c)'s "WEAKER in form" note
  in §9 is accurate.
- **faithful: PASS.** The quotations of B0, B1, B2-core, B2, B3, R1 and W3-POST item 6 are verbatim, and the external
  inputs are unchanged at the cited commits. The N1 and N2 code matches the descriptions, apart from editorial E3.
- **statuses: PASS.** The registry statuses quoted in §6 match CITECHECK's verbatim checks. The lemma files say "PROVED
  (by this seat, unchecked)", and REPORT carries the same. Nothing is called checked that is not.
- **sweep: FAIL.** S1: REPORT §3's card text claims more than STATEMENT (non-uniform "each sub-Gaussian"; dropped
  centring qualifier).
- **reader: PASS.** READER_DELTA's Theorem 2′ and its remarks are correct and match STATEMENT (L-sub-Gaussian
  coordinates; the K-interval rule; failure for rare binary predictors). The reader-facing card sentence is counted
  under the sweep gate (S1).

## (e) Score

**8.8.** The mathematics is clean and complete. The one S finding is a two-phrase repair in REPORT's card text, outside
the registered spans and the proofs. Under the brief's rule it still forces `gates=FAIL` for this manifest.

### Better-theorem proposals (not findings)
1. The window can be reduced to max{(2A+2)s₀ + 2, 3(A+1)(s₀+1) log n}, using R1 B1.3 and B2-core at that q. This is
   option o1, OFF by HQ.
2. On the logarithmic sets the floor can be of order 1/n through B2 (a): Step 4 actually yields λ_min(G_T) ≥ nφ²/4, far
   above g₀. This is option o2, OFF by HQ.
3. B3w (b) is non-asymptotic. A version of Theorem 2SG with an explicit failure probability added to item 6's
   design-event remainder would cost one line, if item 6 is ever restated in a quantitative form.

COUNCIL-VERDICT round=R1 manifest=de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768 seat=opus score=8.8 gates=FAIL
