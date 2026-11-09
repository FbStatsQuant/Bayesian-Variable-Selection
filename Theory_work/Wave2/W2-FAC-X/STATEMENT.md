# W2-FAC-X — STATEMENT (target statement)

Ticket W2-FAC-X, Theory Wave 2 (extension of W2-FAC-B's Theorem FAC-CS to random designs and beyond). Lead: Claude
Opus 5.5 (Claude Personal). Status of this file: **v3 — LOCKED** (2026-11-09). v1 REJECTED by R01 (six changes applied → v2, disposition
reviews/R01_disposition.md); v2 LOCK-WITH-CHANGES by a fresh reviewer R02 (reviews/R02_statement_lock_sol.md; five
changes applied → v3, disposition reviews/R02_disposition.md). No conclusion was strengthened by v3.

Abbreviations: FACB = `Theory_work/Wave2/W2-FAC-B/` (Theorem FAC-CS, STATEMENT v3.1, lemmas L1–L5, PROVED-CHECKED);
FACA = `Theory_work/Wave2/W2-FAC-A/` (Theorem FAC-L, PROVED-CHECKED); FINAL = `Theory_work/Wave1C/FINAL/sections/`;
SoP = `Theory_work/State_of_Project/sections/`. All results are asymptotic (Wave-2 scope rule). Lemma files are
named X1–X6 (lemmas/); the claims below are named (C1)–(C4) to avoid confusion (R01 suggestion 3). The symbol ϖ_n
denotes the perturbation scale; β denotes the raw regression coefficients.

## 0. Targets, diagnosis and scope

HQ brief, in priority order: (1) iid Gaussian rows with compound-symmetric covariance, p ≤ n^A with the largest A
reachable beyond 1/6; (2) general one-factor loadings; (3) k ≥ 2 factors — **moved by HQ to ticket W2-FAC-K2 (2026-11-09); out of scope here**. **This statement locks Target 1** (Theorem
FAC-CS-iid). Target 2 is recorded in §6, to be locked separately; nothing is claimed for them here.

**Diagnosis (numerics/, not proofs).** numerics/iid_core.py simulates the exact sufficient statistics of iid-row data at
any n (Bartlett; self-test iid_selftest_out.txt). N1X (numerics/N1X_summary.md): 121/121 uncapped LS0 paths from [p]
(n ≤ 10⁶, p ≤ 1000, log p/log n up to 0.75) are pure null deletions ending at S₀; the deletion order is an interval of
the sorted noise coordinates only up to a band (defect up to 520 points), of width ≈ 1.3–1.5 × the empirical
perturbation, which scales like √(k log p/n). Mechanism (lemmas/X1): the noise coordinates ξ_j are iid N(0, 1) and
independent of the idiosyncratic Wishart matrix W ~ W_p(n − 3, I); the iid-row deletion statistic is FACB's
one-dimensional statistic ξ_j − x_T plus a perturbation whose first-order part is −(B₀⁻¹Rc⁰)_j with
R = W_T/(n − 3) − I and c⁰_l = ξ_l − x_T, i.e. (Rc⁰)_j = (n − 3)⁻¹Σ_{l∈T}(W − (n − 3)I)_{jl}(ξ_l − x_T) = O(√(k/n)) per
coordinate (R01 item 3) — but path dependent, so it must be controlled on the band-structured sets the path visits.

## 1. Setting

* **Score and method** exactly as FACB STATEMENT §1 (D0, BB(1, p) prior with cap K = min(p, ⌊n/2⌋), block tables, start
  γ₀, method v3.1 as merged on main 4676af6: LS0 = one §6.10 local search from the emitted start-mode centre S̃₀ with move
  cap a_n := ℓ_n + |S̃₀| (MR1), production move rule, single-search prefix property; implementation premises EX-A, EX-S,
  SR, GUARD-W, OP-LS0 (cap a_n), e4 read as e4′, complete scans; CAL only for the [M5-0] route). Nothing is changed.
* **Model R (random design).** Rows of the raw design X^r are iid N_p(m_n, Σ_n) (any mean m_n); ε ~ N_n(0, σ²I)
  independent of X^r; y^r = α1 + X^rβ + ε. The method centres and standardises: X := CX^rD_x⁻¹ (D_x = diag of sample
  sds), θ* := D_xβ (random), μ := Xθ*, Y := Cy^r = μ + Cε, y := Y/s, s² := ‖Y‖²/(n − 1). S₀ := supp β,
  **s₀ := |S₀| ≥ 1** (R01 item 5). Probabilities are under the **joint law** of (X^r, ε).
* **Partition and N₀.** The method's partition is a function of X (blocks of size ≤ 16), hence random. N₀ := the set of
  nulls lying in a realised block that contains all of S₀ (empty if no block contains S₀; |N₀| ≤ 15 since s₀ ≥ 1).
  N₀ is X-measurable and in general dependent on the noise coordinates (R01 item 4); the path claim (C2) is therefore
  proved **simultaneously for every 𝔫 ⊆ [p] ∖ S₀ with |𝔫| ≤ 15** in place of N₀, on events defined over the
  deterministic null set [p] ∖ S₀; zero-pair bounds for (C1) are proved conditionally on the raw design X^r (R05).

## 2. Hypotheses (class CS-iid)

* **(CS-R)** Σ_n = Υ_n[(1 − ρ)I_p + ρ11ᵀ]Υ_n, ρ ∈ (0, 1) fixed, Υ_n deterministic diagonal ±1.
* **(P-½)** limsup_n log p_n / log n < 1/2 (p_n ≥ 1 arbitrary otherwise, bounded allowed).
* **(θ)** s₀ ≥ 1 fixed; with S₀ = {i₁(n) < … < i_{s₀}(n)} (positions arbitrary), ((Υ_nβ)_{i_r(n)})_{r≤s₀} = ϑ, a fixed vector
  in (ℝ ∖ {0})^{s₀}; σ² > 0 fixed. Support-indexed uses ϑ_i (i ∈ S₀), ϑ(V) mean the zero-extended embedding
  ϑ⁽ⁿ⁾_{i_r(n)} := ϑ_r, ϑ⁽ⁿ⁾_j := 0 off S₀ (R07 item 3; notation only).
* **(FS)** (population, R01 item 5): with ϑ(V) := Σ_{i∈V}ϑ_i, (a) ϑ(V) ≠ 0 for every nonempty V ⊆ S₀; (b)
  ϑ_l + ρϑ(V)/(1 + (u − 1)ρ) ≠ 0 for every V ⊆ S₀, l ∈ V, u ∈ {0, …, 15}. (FACB's (FS′) involves the realised block of a
  masked truth; with a random partition it would be an additional hypothesis on the method's partition. It is **not**
  part of this statement; see §5.)

## 3. Definitions (precise forms in lemmas/X1)

Υ_n = I w.l.o.g. (lemmas/X1 header). N := n − 3, ℓ := √(ρ/(1 − ρ)). There are random variables η ~ N(0, 1), ξ = (ξ_j)
iid N(0, 1), a = (a_j) iid N(0, 1), φ² ~ χ²_{n−2} and W ~ W_p(N, I), mutually independent and independent of ‖Cε‖, such
that every score evaluated by the method is a fixed function of (‖Cε‖, η, φ, ξ, a, W, column scales) (lemmas/X1, Lemma
X1.1; checked in R01). κ := N/(ℓ²φ²), ϱ := Nη/(ℓφ²) (T-independent), and for S₀ ⊆ T ⊆ [p], k := |T|, the **reference
centre** x_T := (Σ_{j∈T}ξ_j − ϱ)/(k + κ), with the exact drift identity x_{T∖j} = x_T − (ξ_j − x_T)/(k − 1 + κ). This is
an RSS-reference analogue of FACB's centre (κ, ϱ differ from FACB L1.4's by factors 1 + O_P(n^{−1/2})); FACB's ridge
score reduction is not used literally — the ridge, determinant and Q-versus-RSS corrections are bounded in absolute
terms in lemmas/X1 §X1.4 (R01 item 3). For 𝔫 ⊆ [p] ∖ S₀ with |𝔫| ≤ 15 (R02 item 3): S*(𝔫) := [p] ∖ 𝔫, 𝒩*(𝔫) := ([p] ∖ S₀) ∖ 𝔫, m₀(𝔫) := p − s₀ − |𝔫|;
S* := S*(N₀), 𝒩* := 𝒩*(N₀), m₀ := m₀(N₀). For T with S₀ ⊆ T ⊆ S*(𝔫):
a_T := max{ξ_j : j ∈ T ∖ S₀, ξ_j < x_T} (−∞ if none), b_T := min{ξ_j : j ∈ T ∖ S₀, ξ_j > x_T} (+∞ if none).
ϖ_n := C₀H̄_n√(p_n log n/n) + n^{−1/3} with H̄_n² := 2 log(2(p_n − s₀) + 2) + 2 log log n (the single definition
used in X2–X4) and C₀ := 6C_X, C_X = C_X(ρ) the constant of Proposition X2 (lemmas/X2; X4.0 uses ϖ = 6C_XH̄√(p log n/n)
+ n^{−1/3}; R09 recommendation 2); then ϖ_n ≤ n^{−c} for some c > 0 under (P-½).

## 4. Claims (Theorem FAC-CS-iid)

Under model R, (CS-R), (P-½), (θ), (FS), there are events of probability → 1 on which:

* **(C1) Start mode.** S* is the unique maximiser of γ₀ on Ω; hence S̃₀ = S* ⊇ S₀ and m₀ ≥ p − s₀ − 15.
* **(C2) Path lemma (key lemma).** On one event of probability → 1, simultaneously for every 𝔫 ⊆ [p] ∖ S₀ with |𝔫| ≤ 15
  (in particular 𝔫 = N₀), the uncapped §6.10 search from S*(𝔫) visits T_0 = S*(𝔫), T_1, … and at every visited T ≠ S₀
  (with a_T, b_T as in §3 for this 𝔫):
  (i) the best move is the deletion of a null j with |ξ_j − x_T| ≤ min_{l∈T∖S₀}|ξ_l − x_T| + 2ϖ_n, with positive gain;
  (ii) every addition **at T** has gain ≤ −c log n (c = c(ρ, s₀, limsup log p/log n) > 0); every truth deletion and every
  truth-out swap has negative gain; every null-out swap has gain strictly below the best deletion's gain (no claim is
  made for sets the path does not visit — no-addition is false on general interval-hole sets, R01 item 2, FACB L4.5(3));
  (iii) **band-controlled gap:** no kept null lies in (a_T, b_T), and every deleted null j ∈ 𝒩*(𝔫) ∖ T satisfies
  a_T − 4.3ϖ_n < ξ_j < b_T + 4.3ϖ_n;
  (iv) after exactly m₀(𝔫) moves the search is at S₀, where every feasible neighbour has strictly smaller F.
  Consequently (𝔫 = N₀, on the event of (C1)) LS0 with cap a_n = ℓ_n + |S̃₀| ≥ m₀ ends at S₀ as a certified search endpoint (FACB (C2) wording), and the
  legacy cap ℓ_n misses S₀ whenever m₀ ≥ ℓ_n + 2.
* **(C3) Consistency.** (H0) holds with probability → 1 in the design (conditionally on the raw design X^r, with common constants; R05);
  D_n → 0; P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n), under the joint law.
* **(C4) Delivery.** With all premises, method changes and the amended allocation of Proposition F as stated in FINAL
  `s6_delivery.tex` (as in FACB (C4); CAL not assumed): P(no output) = 0 for every admissible n ≥ 3 and
  **P(Ŝ⁺ = S₀) → 1** under the joint law.

## 5. Not claimed / frontier (evidence only)

* limsup log p/log n ≥ 1/2. In the proof the band term of the perturbation is ≤ C·H̄·#Band·√(log n/n) with
  #Band ≤ C(p·ϖ_n + log n), so its ratio to the error budget ϖ_n is at most C·p·H̄·√(log n/n) + C·H̄(log n)^{3/2}/(√n ϖ_n);
  the second term → 0 by the n^{−1/3} floor and the first → 0 under (P-½). This is a sufficient absorption criterion
  (it also holds e.g. for p = ⌊√n/log²n⌋), not an equivalence (R01 item 6, R02 item 5). This is an obstruction of the proof technique (worst-case control of band
  membership against the Wishart row); N1X shows the method's path unchanged at log p/log n up to 0.75. A leave-one-out
  decoupling of band membership from W_{j·} is a possible approach (not attempted, no claim).
* (FS′) (masked truths) for random partitions; non-Gaussian rows; general loadings (§6); k ≥ 2 (ticket W2-FAC-K2); S5; p > n/2.

## 6. Target 2 (to be locked separately; not part of Theorem FAC-CS-iid)

* **T2** general one-factor loadings Σ = λλᵀ + diag(1 − λ_j²): whitened noise coordinates ṽ1_j = ξ_j + ℓ_jη,
  ℓ_j = λ_j/√(1 − λ_j²); reference statistic ξ_j − ℓ_jX_T with one scalar X_T. First case: finitely many loading values.

## 7. Dependencies (statuses verbatim)

FACB Theorem FAC-CS and lemmas L1–L5: "PROVED-CHECKED" (council R08 9.3 / R09 9.0) — used as an argument template
(L4's constants and case analysis) and for L2/L5; FACA Proposition L5.1 (random-design de-randomisation) and F-FAC:
inside Theorem FAC-L "PROVED-CHECKED"; M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))";
S-T/T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem
GEN "PROVED-CHECKED"; Lemma CAP "PROVED (by this seat)", council-checked; Proposition F (A1 corrected statement) and
F-GROW (A2 "PROVED (A2), checked by A3").
