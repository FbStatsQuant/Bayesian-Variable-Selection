# R08 — Council seat (Claude Opus 5.5, high), W2-FAC-S5 round 1

Scope: Tier 1 only (Theorem FAC-BCS-R = (C1), (C2-R), (C3-R), (C4-R) of STATEMENT v2.3), its framing, and the frontier
report. Read: STATEMENT, REPORT, L1–L5, numerics summaries, CITECHECK, SoP `04_theory.tex:69-74` (score/prior), FINAL
`s7_impl.tex` (L3) loop rule, FAC-A STATEMENT/REPORT (for the "frontier stays at 1/6" claim), KL prover READMEs, R03 (for its
24-path scan). The R01–R06 reports were skimmed only to confirm the trail; the judgement below is my own.

## Independent checks (reviews/R08_scratch/)

* `r08_ident.py`: L1.3 on 300 random BCS instances with variable group sizes (q ≤ 5, random ρ_b < ρ_w), random T, every
  j: residual decomposition r_j = a_j(U) + c_u e_R and v_j = s_u² + c_u²V_R to ≤ 1.0e−15 (e_R computed directly as
  h − ρ_b1ᵀΣ_RR⁻¹g_R, not by L1's normal equation); |τ| ≤ |A| + κ₀|e_R| violated 0 / 2355 times.
* `r08_check.py`: an implementation of F written from scratch in mpmath (60 digits) from SoP `04_theory.tex:70-71`
  (det H, det(G + I), Q, ν, w(k) = [2·C(2p−1, k)]⁻¹), with exact Gram (n − 1)Σ for S5 (p = 20, 4 groups of 5, truths in two groups,
  ϑ = (1, −0.8)), complete scans (all flips and all swaps) from [p] (= S* since N₀ = ∅ here). Results:
  n = 10²⁰ (seed 0) and n = 10³⁰ (seeds 0, 1): pure null-deletion path, 18 steps, ends at S₀ with no improving neighbour;
  min best-deletion gain ≥ 0.48 log n; best addition ≤ best deletion − 0.98 log n; best null-out swap ≤ best deletion − 0.498 log n;
  every truth-removing move ≤ −0.105 n; CC_n(0) margin min over the path +0.42 to +0.65 (normalised by log n), so CC_n(δ) holds
  for δ up to ≈ 0.4 (n = 10³⁰ seed 2: margin +0.58). n = 10¹² (seeds 0, 1, 2): same path behaviour (min deletion gain
  ≥ 0.467 log n, swap gap ≥ 0.498 log n), CC margins +0.07, +0.20, +0.03. All consistent with (a)–(c) of L4 with room to
  spare. Raw lines: `out_n1e12.txt`, `out_n1e30.txt` (7 paths in total, all pure null deletion ending certified at S₀).

## Gate verdicts

**G1 — correctness of every step: PASS.** I re-derived the load-bearing steps:
* L1.3: conditional-on-h argument and the identity τ = (s_uA + c_ue_R)/√v; c_u/s_u decreasing with value
  (1 − ρ_b)^{−1/2} at u = 0, √v ≥ s_u ⇒ (L1.3.1). Numerically confirmed (above).
* L1.4: σ_j = a⁻¹β̃ᵀϑ^R (S₀ ⊆ R ⇒ Σ̃_RR⁻¹Σ̃_{RS₀} is the selection), hence the leakage √k/n^{3/2}; the (β − β̃) and
  ṽ − v terms; the gain identities from F = log w − ½L − ν log ψ (checked against the SoP formula; w(k − 1)/w(k) = (2p − k)/k);
  M_T = ν(n/(n + 1))σ²/(s²ψ_T) → ½ for T ⊇ S₀ when p ≤ n^α, α < 1; the two elementary log bounds.
* L2: inverse-M-matrix sign pattern ⇒ positive conditional covariances ⇒ (FS-BCS) excludes finitely many proper
  hyperplanes; positive-pair increment ≥ (n/2)c₂ − 2 log n; zero-pair increment ≤ −¼ log n via ψ_U ≥ σ²n/(2s²_max) and
  (L1.4.1) on U ∪ {l}; the dichotomy argument (a non-N₀ missing l always forms a positive pair).
* L3: union-bound counts (E1, E_A with ≤ p·2^{q̄−1} statistics, 2Φ̄(x) ≤ e^{−x²/2}) give 1/(2 log n); E2 via LM with p ≤ n/2;
  E_S variance ≤ 1.
* L4: thresholds of L4.1 (Λ_k is ≤ each of the three 2Δ's up to b_n, 2/p); CC is imposed exactly on the sets whose
  e-values control the three families of statistics (deletion of j at T ⇒ e_{T∖j}; addition at T ⇒ e_T; addition in a
  null-out swap ⇒ e_{T∖j}), so (a) and (b) follow; (c) by the bias/noise RSS argument (Gram floor d; Q_{T′} − Q_T ≥ c₃n;
  ψ_T < n ⇒ ratio ≥ 1 + c₃). The path claim is then essentially by definition of Π (best null deletion, production tie
  rule), since every non-null-deletion candidate is strictly worse. Endpoint: CC at the terminal index covers additions to S₀.
* L5: [OP] ⇒ D_n ≤ P(𝒦_nᶜ); 𝒦_n data-measurable so P₀ = P̃; union bound on the enlarged space; [M5-0] with L5.1's (H0).
  Delivery via D′'s pathwise inclusion, as FACB.
* Non-vacuity remark: (H_q + κ₀(G_n + 2L_n))² ≈ 2a(1 + κ₀)² log n ≤ (1 − δ)(log n − 2) ⇔ a < (1 − δ)/(2(1 + κ₀)²);
  S5: κ₀ = 0.7^{−1/2}, bound 0.1038. Correct.
No errors found.

**G2 — hypotheses used = hypotheses stated: PASS.** (C2-R) uses G, (BCS), (P_α) α < 1/2, (θ), δ, and L3's E_n (E_S is
only needed by L2, harmless); (FS-BCS) is used only in (C1) and correctly not listed for (C2-R). (C3-R)/(C4-R) list
(C1)+(C2-R) hypotheses, premises, MR1; (P_α) implies (P) eventually. The bounded-p case is handled (R03 item 1).

**G3 — no hidden assumptions: PASS.** The method partition is a deterministic function of the fixed design (stated);
"positions of S₀ may vary with n" is covered by the finite-pattern argument; p ≥ 1 bounded allowed; non-data-measurability
of CC_n is stated explicitly and the probability statements are placed on the enlarged space (L5.2). Nothing about the
deletion order or within-group dynamics is assumed.

**G4 — cited results' status adequate, verbatim, not upgraded: PASS.** CITECHECK 6/6 OK; I spot-checked SoP
`04_theory.tex:69-74` and FINAL `s7_impl.tex` (L3). Statuses of T38-(0), T03♯, [OP] (incl. "unchecked" inside GEN),
CAP, Proposition F/F-GROW/A4 are reproduced verbatim and qualified in L5.4; FAC-CS is used for pattern/algebra only and
re-verified. Unchecked KL prover output is not used by Tier 1. (One framing slip about the prover output — see fix 1 —
concerns the frontier text, not a cited input.)

**G5 — constants/rates tracked: PASS.** n₀(α, δ, ρ_b, ρ_w, q̄, ϑ, σ, s₀) declared; η_n = 8n^{−min(1−α, 1/3)}, b_n = 2p/((n − 1)d),
|ε| ≤ n^{−1/2}, c₁ = c_FS/(2s_max), c₃ = ϑ²_min d/(4s²_max), c_θ = ¼log(1 + c₃), margins (δ/4)Λ_k − o(1) ≥ (δ/8)log n with
the Λ_k ≥ log n − 2 floor (k = p case included); the x²/ν correction O((log n)²/n). The sign-corrected-scale constants
are uniform over T and over the incidence patterns. Rates are asymptotic, as required by the scope rule.

**G6 — fidelity to v3.1 / main 4676af6 / MR1: PASS.** Score, prior and Ω (K = p) as SoP; LS0 loop as FINAL s7 (L3):
complete flip+swap scan, best scanned neighbour, exact ties lexicographic, cap tested only after selecting a neighbour —
hence "a ≥ m₀ certified, a ≥ m₀ − 1 scores S₀" is correct; MR1 a_n = ℓ_n + |S̃₀| ≥ |S*| ≥ m₀ is used essentially and
correctly (legacy ℓ_n would fail, L4.6.3). Start mode = unique maximiser, so e4/e4′ and lex rule are irrelevant (MR3).

## Score: **8.6 / 10**

The Tier-1 mathematics is correct, short and clean, and the reduction to the single scalar e_T is a genuine structural
insight (L1.3 two-level identity + union bound over (null, mate-set) pairs). The result is honestly labelled PARTIAL and
correctly states that the unconditional S5 frontier remains FAC-A's 1/6 (FAC-A instance (c) indeed covers S5). The score
reflects that the deliverable is a conditional reduction whose condition is unverified above 1/6 (its own crude witness
reaches only a* < 0.104, i.e. Tier 1 alone adds no unconditional range), plus the two framing fixes below.

## Required fixes (minor; framing/status only — no mathematics changes)

1. **REPORT flag 2 misdescribes the lattice-sharpness evidence.** "sharp: two parallel provers proved the matching lattice
   lower bound" — per LOG 10:15/11:25 and the READMEs, the provers were two *sequential* rounds; only round 2
   (`KL_attempt_sol2/02_lattice_obstruction.md`) contains the matching lower bound (round 1 gives an upper bound with
   constant √(23/7)), and it is **unchecked**. Reword, e.g. "sharp for all-set arguments by the round-2 prover's matching
   lattice lower bound (unchecked)". Add "(unchecked)" likewise in §5(i) where "this is sharp for all-set arguments" is stated.
2. **Status labels are inconsistent.** The lemma headers say "PROVED (by this seat, unchecked)" while also recording
   R02–R04 checks, and REPORT flag 1 says "Proved and checked". Harmonise (e.g. lemma headers: "PROVED; lemma check RNN
   V-W-A applied; sweep R06; council pending/passed"; REPORT §1/§4: fill in the council outcome when known).

## Optional suggestions

* STATEMENT (C3-R)/(C4-R) write P(CC_n(δ)ᶜ) while REPORT/L5 write P̃; use P̃ in the STATEMENT too (§3 already explains it).
* REPORT §5 numerics: S3_summary's `CCmargin` column (δ = 0) is negative in 16/18 runs; this is because H_q² exceeds
  Λ_k at those n (e.g. p = 2000, n = 10⁶), not because of e. Worth one sentence that the S3 runs monitor the e-part ratio,
  not CC itself, and that CC is a sufficient condition (paths are pure deletion even where it fails). My large-n runs
  (n = 10²⁰, 10³⁰, p = 20) show CC with margin 0.4–0.65 log n and all L4 margins.
* L4.2: say once that the "o(1)" absorbed in (L4.3) includes b_n, η_nΛ_k, x²/ν and 1/p-type terms, with η_nΛ_k = o(1)
  because η_n is polynomially small (it is, but it is the one place where a relative error multiplies a log n quantity).
* W2-UNI §7 list is useful; item 2 (floor on all principal submatrices) is the real design-agnostic bottleneck and
  deserves to be flagged to HQ as such.
