# W3-POST — ASSUMPTION MAP (sharpness gate, PROTOCOL Wave 3 §3) — v1.2 (council amendments C1–C3 [C1A-, C1B-, C2A-, C2B-, C3A-, C3B-#])

Theorem 1 / Lemma 1a / 1a′ of `STATEMENT.md`. "Enters at" names the proof step ([T03R] = `ARC/W1-T03R/PROOF.md`,
[P1]/[P3] the locked proofs, [POST] = W2-APP L1_POST). Numerics: `numerics/post_exact.py` → `numerics/post_exact_out.txt`
(E0–E5, L1a); exact enumeration of the **coded** posterior, p = 10 (Wave1 PROTOCOL cap p ≤ 10 [C1A-F6]), 20 seeds,
n ∈ {100, 400, 1600, 6400} (E5 also 25600); the signal is generated on the standardised scale (μ = Xθ*, σ* = 1), so
θ labels are literal [C1A-F5]. All numbers quoted are **medians (or frequencies) over the 20 seeds** at the listed n —
empirical trends, not proved limits [C1A-F5]. With p fixed these runs probe the regime A → 0; they say nothing about
p ≫ n. Verdicts: **necessary** (a violation breaks the conclusion), **improvable** (conclusion survives just outside),
**open**.

| Id | Assumption | Enters at | Necessary? | Evidence |
|---|---|---|---|---|
| POST-G | Gaussian noise ε ~ N(0, σ*²I), σ*² fixed | [P1] `lem:num` (the numerator identity needs the true density f₀), `thm:T01iii`, all χ² laws ([P3] `lem:chi`, `lem:Gprob`) | open | Every Bayesian selection theorem cited below also assumes Gaussian errors. Not probed. |
| POST-E | ‖μ‖² ≤ nM | [P1] `thm:T01iii` (scale event 𝓑_n, the constants b±, κ, c_IG); [P3] `lem:ongood` | improvable to sub-linear growth? open | Only analogous to Song–Liang Condition 2 (a predictor-moment condition), under bounded coefficients [C2B-N3]. |
| POST-C | ∃ T, θ: X_Tθ = μ, ‖θ‖² ≤ nM′ (L1a′ only) | L1a′ changed step (ridge bias of the reference model) | open (some coefficient control is needed for the proof; no counterexample found) | L1a′(e): outside the hypothesis (θ = (n, −n), near-collinear pair) max over seeds of max_{t≤m<K} Θ ≤ 1.5·10⁻⁵ at every n, i.e. the conclusion survived. |
| POST-F0 | λ_min(R_{S₀}) ≥ φ₀² | Lemma 1a: only [P1] `lem:den` (ridge bias); Theorem 1: also [P3] `lem:ongood`(c), `lem:onesup` (via (B3)), beta-min scale 1/φ₀² | **improvable for Lemma 1a** (removed: L1a′); for Theorem 1 implied by F_λ | L1a(b),(c): duplicated/near-singular S₀ with bounded θ — max over seeds of max_{t≤m<K} Θ ≤ 1.1·10⁻³ (n = 100), decreasing in n. |
| POST-Fλ | SE_λ(j₀): λ_min(R_{S₀∪J}) ≥ φ₀², \|J\| ≤ j₀ = ⌈(2A+1)s₀⌉+1 (⇒ by interlacing the same floor on every \|S\| ≤ j₀, R02-F2) | [T03R] Lemma B(B2): underfitting S with \|J′(S)\| ≤ j₀ — `cor:diff`, `lem:signal` (beta-min scale), (G4) χ² law; (C6)(b), (C10) | **improvable** on null-only directions (E3); the *anchored* part is necessary *at the beta-min scale* (E4): what matters is θ²_min nφ₀²/log n | E3: exact + near-duplicate null pairs: HPM = S₀ in ≥ 95% of seeds, median δ/r_n 0.81–1.12. E4 (null with 1 − corr² = n^{−γ} to the truth, θ = 1): γ = 0.5 consistent (median δ/r_n 1.08 → 0.64); γ = 0.8 slow (median δ 0.40 → 0.06, HPM wrong in 10–20%); γ = 1 no convergence visible (median δ 0.37–0.50, HPM wrong in 25–30% at every n). Consistent with BM in product form θ²nφ_n²/log n → ∞ with φ_n → 0, which the proof does not allow (n₀ depends on φ₀). |
| POST-Fw | SE_w(m♯_n; g₀): λ_min(G_{S₀∪J}) ≥ g₀ (unnormalised), \|J\| ≤ m♯_n (⇒ λ_min(G_S) ≥ g₀ for every \|S\| ≤ m♯_n) | [T03R] Lemma B(B1): exact χ²_{\|J\|} law of the superset statistics and the determinant bound (D_{S₀∪J}/D_{S₀} ≥ [(n+1)/(1+1/g₀)]^{\|J\|}) in (C4)–(C5), (C8) | **improvable** (exact singularity beyond j₀ is harmless numerically) | E2: s₀ = 1, null x₁₀ = x₃+x₄+x₅+x₆ exactly (S₀∪J singular at \|J\| = 5 > j₀ = 4): median δ/r_n 0.94 → 0.67, HPM = S₀ in 100% of seeds. Heuristic: a rank-deficient superset gets the Occam factor of its rank, but the prior factor of its size, so it is dominated by a full-rank sub-superset. Not proved. |
| POST-BM | θ*²_min ≥ cσ*² log n/(nφ₀²), c > c₀ = max{4C_*, 32[s₀(A+1)+2]} (≥ 128 at s₀ = 1, A = 1) | [P3] `lem:signalgain` via (C10): the underfitting mass | **order: necessary by numerics (fixed p) and a leading-order heuristic (R03 §1A), not proved; constant improvable** [C1B-F2] | E1 (s₀ = 1, iid design, φ₀ ≈ 1; medians): c = 0.5 and c = 1 fail (δ 0.93–0.99), θ² = log log n/n fails (δ ≥ 0.98); c = 2 slow (δ 0.66 → 0.13, δ/r_n not decreasing: 3.1–6.7); c = 4 at rate r_n (δ/r_n 1.54 → 0.70); c = 8 likewise (1.02 → 0.64). Benchmark (R03 §1A; orthogonal true coordinate): deletion log-odds = (√λ + Z)²/2 − log(2p/s₀) − ½ log n + O_P(1), λ = nθ²/σ*², so the deletion mass is n^{a+½−c/2+o_P(1)} when log p = (a + o(1)) log n. Hence, with a **fixed positive margin η**, c ≤ 2a + 1 − η precludes consistency and c ≤ 2a + 2 − η precludes the rate r_n [C1A-F8]; boundary cases depend on the actual log p sequence (a subleading term such as (log n)^{3/4} dominates the √log n fluctuations) and are not claimed. These are *deletion obstructions*, not a sufficiency theorem for general replacement geometry. At fixed p (a = 0) the obstructions sit at c = 1 (consistency) and c = 2 (rate), matching E1. The theorem's c₀ (= 128 at s₀ = A = 1) is 32–64× the rate obstruction 2a + 2 ∈ [2, 4] for a ∈ [0, 1] [C1B-N7]. |
| POST-BM′ | *no* beta-min: specificity max_{j∉S₀} PIP_j → 0 | not claimed (Theorem 1 item 5) | **COUNTEREXAMPLE (numerical, E5; leading-order analytic sketch, unchecked)** [C1B-F4] | **Mechanism**: R03 §5A analytic p = 3 construction (S₀ = {1, 2}, θ² = b² log n/n, proxy x₃ = r(x₁+x₂)/√2 + √(1−r²)u, r² = 0.9, b² = 0.75: the proxy singleton has log-weight coefficient 0.175 (×log n) against ≤ 0 for every other model, gaps of order log n against O_P(√log n) fluctuations; Gram floor 1 − √0.9 > 0), re-derived independently by council seat A (`reviews/C1_council_astra.md`). C1 seat B (`reviews/C1_council_opus.md` §1, own exact runs in `reviews/C1_scratch_opus/`) found this p = 3 margin (0.175 log n) too small to be visible at n ≤ 10⁶ (median PIP₃ ≤ 0.50), so it is cited as **mechanism** only [C1B-F4]. **Leading-order sketch for E5's own design (unchecked as a lemma; C1 seat B's computation, re-done by the lead and re-derived by C2 seat B [C2B-N5]):** with relative log weight (vs ∅) = ‖P_Sμ‖²/(2σ*²) − ½\|S\| log n + O_P(√log n) + O(1) in this fixed-p experiment — the coefficients below are the deterministic leading coefficients [C2A-F3] — and ‖μ‖² = 4c log n (four orthogonal truths, θ² = c log n/n), the proxy captures 16a²θ²n = 3.2c log n (a² = 0.2), so at c = 0.8 the scores in units of log n are {5}: 0.78, ∅: 0, {i}: −0.1, S₀: −0.4, {5, i}: ≈ 0.3, any ≥ 3 variables ≤ 0.1: the proxy wins by ≥ 0.48 log n against O_P(√log n) fluctuations. **Illustration** E5 (`numerics/post_exact_out.txt`, medians): s₀ = 4 weak truths, θ² = 0.8 log n/n each, null proxy x₅ = a(x₁ + … + x₄) + √0.2 z, population λ_min(Σ_{S₀∪{5}}) ≈ 0.106: max_{j∉S₀} PIP_j = 0.26, 0.49, 0.82, 0.92, 0.988 at n = 100 … 25600 (an empirical trend, not a limit). With θ² = 0.5 log n/n: 0.10 → 0.57. Theorem 1 item 5(a) (supersets only) and 5(b) (strong signals) are the right no-beta-min statements. |
| POST-DIM | p ≤ n^A, fixed A | j₀ = ⌈(2A+1)s₀⌉+1 and (C8) rate ((2p)^{s₀}n^{s₀/2}Υ^{>j₀}); m♯_n = O(log n) for the χ² union levels τ_j = C_A j log n ([P1] §T02ii, [P3] (G3)); Lemma 1a does **not** use it | open (technique) | [T03R] E3: the Markov/first-moment size-tail route needs m♯_n − s₀ ≳ (s₀A + (s₀+2)/2) log₂ n (p ≍ n^A; [T03R] E3/Prop D, not re-checked here [C3B-N6]); Prop D: some growth ≥ ½ log₂ n is necessary in general. Exponential p: CJ18 (`Theory_work/State_of_Project/sections/04_theory.tex:816`). See R03. |
| POST-S | s₀ fixed | n₀, j₀, combinatorial constants K_{s₀,j}, 2^{s₀} in (C8) | open for Theorem 1; **not needed** for Lemma 1a′ | — |
| POST-LSF | random design: population floors (i) φ² at size s₀ + j₀, (ii) ψ_n ≫ (log n)^{3/2}/√n at size k̄_n = O(log n) | [POST] step (3) (Weyl transfer: ‖R̂_S − Σ_S‖ ≤ \|S\|·max-entry error = O((log n)^{3/2}/√n)) | (i) anchored version necessary for the sample floors ([POST] Remark 2); (ii) improvable (the Weyl/entrywise step is crude; sparse-eigenvalue concentration gives O(√(k log p/n))) | Not probed numerically. |
| POST-GR | Gaussian rows (random design) | [POST] step (2) only (entrywise event) | improvable (sub-Gaussian rows: Bernstein; [POST] Remark 3, not claimed) | — |

## Implications between assumptions (for the INFRA registry)
- POST-Fλ ⇒ POST-F0 (J = ∅). POST-F0 ∧ POST-E ⇒ POST-C with T = S₀, M′ = 1.5M/φ₀² (n ≥ 3; L1a′ Remark 1).
  Hence Lemma 1a′ ⇒ Lemma 1a (with a different constant).
- Locked SE of T03 (all T, \|T\| ≤ m_n + s₀, constant φ₀²) ⇒ POST-Fλ ∧ POST-Fw with g₀ = φ₀² ([T03R] §4, line 134).
- POST-LSF ∧ POST-GR ∧ fixed coefficient bounds ⇒ (POST-E ∧ POST-Fλ ∧ POST-Fw with φ₀² = φ²/2, g₀ = 1) on events of
  probability → 1 ([POST] Lemma POST(a)). λ_min(Σ_n) ≥ c > 0 ⇒ POST-LSF.
- BM-∞ ⇒ BM(c) eventually for every c. Orthogonal designs (G = (n−1)I) ⇒ POST-F0, Fλ, Fw with φ₀ = 1.
- Theorem 1 items 2–4 ⇐ item 1 by SL0/SL1 (deterministic). Item 5(a) ⇐ G, E, F0, Fw only (T02(ii♯)).

## Comparison with the literature

**Song & Liang (2015), JRSSB 77(5), 947–972 (read from the PDF, printed pp. 949–957; PROTOCOL Wave1C path).** Setting:
random design with x ~ ν_x, Gaussian errors, P_n ≻ n^θ. Prior: independent inclusion λ_n = r_n/P_n with size cap r̄_n
(6), β_ξ ~ N(0, σ²V_ξ), σ² ~ IG(a₀, b₀) (§2.1.1). The two consistency theorems have **different settings** [C1A-F3]:
Theorem 1 (p. 952) assumes bounded predictors (|x_i| ≤ 1), approximate sparsity (3) and conditions (8)–(14) (incl.
r̄_n ln P_n ≺ nε_n² (10)); Theorem 2 (p. 953) assumes Condition 1, strict sparsity (4), conditions (9)–(14) and r_n ≻ 1;
both give posterior consistency in Hellinger distance at rate ε_n; Corollary 1 (P_n < exp(Cn^α), ε_n =
O(n^{−(1−α)/2}log^{k/2} n) for r̄_n ≺ log^k n); Theorem 3 (sure screening only — "the specificity is not controlled",
p. 956); Theorem S (MAP consistency) is in the online supplement, **which is not available to this ticket; it was not
read**.
- *Condition 1* (p. 953): sup over sub-vectors of size r ≤ r̄_n and |a_i| ≤ δ of E exp{(Σa_i x_{j_i}/r)²} ≤ e^M — an
  exponential-moment condition on the predictors. Ours (fixed design) has no distributional condition on X; the random
  version assumes Gaussian rows (POST-GR). Their remark (p. 953) verifies Condition 1 for a zero-mean, unit-variance
  Gaussian process; our rows may have arbitrary means (removed by sample centring), so the comparison is for centred
  predictors [C1A-F3].
- *Condition 2* (p. 954): second moments E(Σa_ix_{j_i}/r)² ≤ M, a predictor-moment condition; gives only convergence in
  probability (16). Only *analogous* to our POST-E (‖μ‖² ≤ nM), and only under bounded coefficients [C1A-F3].
- *Condition 3* (p. 955, identifiability): E exp{−(x_k + Σ_{i≤r̄_n} b_ix_{j_i})²} ≤ 1 − δ_n, δ_n ≻ ε_n², for all r̄_n-sets
  of other predictors. On p. 955 they show it is implied by smallest eigenvalue of every (r̄_n + 1)-sub-covariance
  ≻ r̄_nε_n² **for centred bounded predictors** (|x_i| ≤ 1), and separately (variance ≻ ε_n²) for standard Gaussian
  predictors; covariance control alone does not give it for arbitrary laws [C1A-F3]. Theirs is over
  **all** sets of size r̄_n + 1 but allows a **vanishing** floor; ours (POST-Fλ/Fw) is stated on sets S₀ ∪ J, but by
  interlacing it implies the same floor on **every** set of size ≤ j₀ (resp. ≤ m♯_n) [R02-F2] — so ours is a fixed
  floor on all sets of bounded size j₀ (plus anchored sets of size s₀ + j₀) and an essentially free floor (g₀/(n−1)) on
  all sets of size O(log n); theirs is a vanishing floor on all sets of size r̄_n + 1. E4
  suggests the fixed floor can be traded against beta-min (product form), which would bring ours closer to theirs.
- *Prior conditions*: their cap condition (10) fails for the coded cap K = min(p, ⌊n/2⌋) when p ≥ n/2 (then K = ⌊n/2⌋)
  [C1A-F3], and BB(1,p) has prior mean size ≈ 1, not r_n → ∞; Lemma 1a/1a′ replaces (10) (size tail from the exact
  prior tail **and** the reference-model marginal-likelihood bound). Our ridge prior n(G + I)⁻¹ is their
  "ridge prior" example V_ξ⁻¹ = E(x_ξx_ξᵀ) + c_nI with c_n ∝ 1/n (p. 953), on the sample scale.
- *Conclusions*: ours are stronger on the selection side (π(S₀) → 1 at rate √(log n/n), exact HPM and MPM, specificity
  of PIPs) and narrower in dimension (n^A vs exp(Cn^α)); Hellinger/predictive contraction (their Thms 1–2) is PROGRAM
  item 1b, not done here.

**Narisetty & He (2014), Ann. Statist. 42(2), 789–817** — read from arXiv:1405.6545 (printed pp. 5–6, 10–12 of the
arXiv version; condition numbers as printed there) [C1A-F2]. Prior (1): spike-and-slab normal, β_i | Z_i = 0 ~
N(0, σ²τ²_{0,n}), β_i | Z_i = 1 ~ N(0, σ²τ²_{1,n}), P(Z_i = 1) = q_n, σ² ~ IG. Condition 4.1: log p_n = o(n).
Condition 4.2: nτ²_{0n} = o(1), nτ²_{1n} ~ (n ∨ p_n^{2+3δ}), q_n ~ p_n⁻¹. Condition 4.3: \|t\| fixed; inactive
coefficients may be nonzero with ‖X_{tᶜ}β_{tᶜ}‖₂ = O(1). Condition 4.4 (identifiability): for some K > 1 + 8/δ,
Δ_n(K) := inf_{k: \|k\| < K\|t\|, k ⊉ t} ‖(I − P_k)X_tβ_t‖² > 5σ²\|t\|(1 + δ) log(√n ∨ p_n) — a **residual-signal**
condition on underfits, not an eigenvalue condition. Condition 4.5 (regularity): for some ν < δ and κ < (K − 1)δ/2 (with ν > 0 in the definition of m_n(ν), p. 6)
[C2A-F2], λ^n_M ≺ (nτ²_{0n})⁻¹ ∧ nτ²_{1n} and
λ^n_m(ν) ⪰ (n ∨ p_n^{2+2δ})/(nτ²_{1n}) ∨ p_n^{−κ}, where λ^n_m(ν) is the infimum over \|k\| ≤ m_n(ν) =
p_n ∧ n/((2 + ν) log p_n) of the **minimum nonzero eigenvalue** of X_kᵀX_k/n (p. 6) — so exact singularity is
allowed — and λ^n_M is the largest eigenvalue of XᵀX/n. Theorem 4.1 (p. 12): P(Z = t | Y, σ²) → 1 under 4.1–4.5
(known σ²; the IG-prior version, Theorem 4.2, was not re-read). **Comparison.** Their design control is split into
identifiability (4.4) and nonzero-eigenvalue regularity (4.5); ours puts a positive floor on all small sets (F_λ, which
excludes exact singularity at size ≤ j₀) and a positive unnormalised floor up to size m♯_n (F_w, which excludes it
there). E2/E3 suggest our floors are stronger than needed exactly in the directions where theirs are weaker (singular
null directions) — consistent with R03's DG/VIS proposals, which move toward their split. Their signal scale is
log(√n ∨ p_n) through 4.4, not unconditionally log p_n. They allow log p_n = o(n); we require p ≤ n^A.

**Yang, Wainwright & Jordan (2016), Ann. Statist. 44(6), 2497–2532** — read from arXiv:1505.07925 (printed pp. 6–9 of
the arXiv version) [C1A-F1]. Model (5): g-prior β_γ | γ ~ N(0, gφ⁻¹(X_γᵀX_γ)⁻¹), π(φ) ∝ 1/φ, sparsity prior
π(γ) ∝ p^{−κ\|γ\|} 𝕀[\|γ\| ≤ s₀]; regime p ≥ n. Assumption A (‖Xβ*‖²/n ≤ gσ₀² log p/n; off-support residual
≤ L̃σ₀² log p/n); Assumption B with an integer s: RE(s) min_{\|γ\|≤s} λ_min(X_γᵀX_γ/n) ≥ ν and a sparse projection
condition SI(s); Assumption C: g ≍ p^{2α}, κ + α ≥ C₁(L + L̃) + 2; Assumption D in two versions: D(s*) sets s₀ := p
(**no cap**) with s* ≤ (8C₀K)⁻¹{n/log p − 16L̃σ₀²}, and D(s₀) is a sandwich on the cap. **Theorem 1** (posterior
concentration) uses A, B with s = Ks*, C and **D(s*)** — no truncation of the model space — and
C²_β ≥ c₀(L + L̃ + α + κ)σ₀² log p/n, giving π_n(γ* | Y) ≥ 1 − c₁p⁻¹ with probability ≥ 1 − c₂p^{−c₃}. **Theorem 2**
(rapid mixing, not re-read) is the one that uses D(s₀) and the cap. **Comparison** in the shared regime p ≥ n with
p = n^A (A ≥ 1): their per-variable penalty is ≈ (κ + α) log p with κ + α ≥ 2, giving 1 − π(S₀) = O(p⁻¹) = O(n^{−A});
the coded prior's per-variable penalty is ≈ log(2p) + ½ log n, and our proved rate is √(log n/n). That our rate is
attained for the coded prior when p grows is a **conjecture** (sharpness record item 4), not a theorem.

## Sharpness record (answers to the ticket's three questions)
1. **Beta-min rate.** Order √(log n/n) is necessary — **numerical evidence (E1: c ≤ 1 and log log n fail at fixed p)
   and a leading-order heuristic (R03 §1A), not proved** [C1B-F2]; at p = n^A it coincides with the √(log p/n)
   scale of the information-theoretic support-recovery limits (Wainwright 2009, IEEE Trans. Inf. Theory 55(12),
   5728–5741 — recalled, not re-read) [C2B-N7]. The constant is improvable: the orthogonal deletion obstruction sits at c = 2a + 1 (consistency) and
   c = 2a + 2 (rate r_n), up to a fixed margin (a = lim log p/log n; boundary cases not claimed), against c₀ = max{4C_*, 32[s₀(A+1)+2]}. R03 §1B proposes a bounded-work
   replacement c_new = (√C_* + √(2(A+1)))² (keep the first inequality of [P3] `lem:SvsSp`; risk low–medium; not
   sharp, since C_* ≍ A·j₀). **Improvable (constant only); not done here.**
2. **Floor set size.** F_w (sets of size up to m♯_n) looks removable (E2); F_λ is needed only in the anchored, masking
   direction and only through the product θ²_min φ₀² (E3, E4). **Improvable (assumption strength), not proved.**
   Bounded-work routes (R03 §2): (A) replace F_w by the determinant-ratio interface DG(c_D):
   D_{S₀∪J}/D_{S₀} ≥ [c_D(n+1)]^{|J|} for 1 ≤ |J| ≤ m♯_n (implied by F_w with c_D = g₀/(1+g₀); rank loss absorbed by
   truncating exp(min(χ², τ_j)/2) and rank domination; risk low); (B) replace F_λ off S₀ by signal visibility
   VIS(φ): ‖(I − P_S)μ‖² ≥ Nφ²‖θ*_{S₀∖S}‖² for underfits with |S∖S₀| ≤ j₀ (risk medium). Deleting F_w outright is
   unresolved (R03 §2C: high risk). The size-tail lemma needs no floor at all (L1a′).
3. **p ≤ n^A range.** Lemma 1a′ is free of it. Theorem 1 uses it through j₀ and the polynomial union bounds; the
   barrier E3 concerns the size-tail technique only. R03 §3: a conservative extension to L_n := log(2p) + log n =
   o(n^{1/3}) with rate √(L_n/n) looks bounded-work, but pays a stronger beta-min nθ²_minφ₀² ≥ C(j_nL_n + log n) with
   j_n ≍ [s₀ log(2p) + (s₀+2) log n]/log(n/L_n) (the G4 union bound costs j_n log p); keeping beta-min at √(log p/n)
   needs a new weighted-underfit argument; log p = o(n) is not reachable by this chain cheaply. Exponential p remains
   CJ18. **Open; improvable in range at the cost of beta-min (proposal, risk medium).**
4. **Rate.** **Proved lower bound** (status PROVED (by this seat, unchecked), line-checked by both C2 seats) [C3B-N4] (Proposition LB, `lemmas/LB_rate_lower_bound.md`): for every data set and design,
   1 − π(S₀) ≥ 1/(1 + √(n+1)) when 1 ≤ s₀ < p, s₀ + 1 ≤ K (claimed only in this domain; it can fail at p = s₀, C2 seat A F1) (falsification `numerics/lb_check_out.txt`: min ratio 1.013).
   So the proved rate √(log n/n) is sharp up to √(log n). Empirical, fixed p: median δ√n ≈ 2.1–2.6 across n = 100 … 6400
   (E0), i.e. order n^{−1/2} is attained there. **Conjecture** (not proved; C1A-F1): for p = n^A and well-conditioned designs the superset mass of the coded
   prior is of exact order √(log n/n) (sum over the p null additions of one-variable Bayes factors ≈ (2p)⁻¹n^{−1/2}e^{χ²/2},
   whose truncated mean grows like √log p), so √(log n/n) would be the sharp rate for the coded prior. Proving it needs a
   lower-bound proposition that this ticket does not supply. YWJ16's faster O(p⁻¹) comes with a larger per-variable
   penalty (κ + α ≥ 2 in units of log p), i.e. a different prior.
