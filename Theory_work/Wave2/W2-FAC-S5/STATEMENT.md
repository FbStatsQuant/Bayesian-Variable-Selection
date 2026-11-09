# W2-FAC-S5 — STATEMENT (target statement)

Ticket W2-FAC-S5, Theory Wave 2 (follow-up of W2-FAC-B §5(b)/§6 item 1). Lead: Claude Opus 5.5 (Claude Personal).
Status of this file: **v2.3 — LOCKED** (v2.1–v2.3 = post-lock wording/notation fixes: R03 item 3, R05 item 1, R06 items 10, 13, 14, 15; no hypothesis or claim changed) (2026-11-09; R01 (Codex Sol high, reviews/R01_statement_lock_sol.md)
LOCK-WITH-CHANGES; all five required changes applied, disposition reviews/R01_disposition.md; v2 also contains the lead's
pre-verdict correction of the centre condition to the size-dependent CC_n(δ), see LOG 09:36).

Abbreviations: SoP = `Theory_work/State_of_Project/sections/`; FINAL = `Theory_work/Wave1C/FINAL/sections/`;
FACB = `Theory_work/Wave2/W2-FAC-B/`; FACA = `Theory_work/Wave2/W2-FAC-A/`. All results are asymptotic (Wave-2 scope rule).

## 0. Target, diagnosis, and the two tiers

HQ target: Theorem FAC-BCS — on exact-Gram block compound symmetry (S5 as core instance), fixed s₀, generic
no-cancellation, p ≤ n/2 (or as large a range as possible beyond FAC-A's log p/log n < 1/6): start mode, path lemma,
D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, delivery P(Ŝ⁺ = S₀) → 1.

**Diagnosis (numerics/; not proofs).** (i) Exact-Gram S5, p ∈ {500, 2000}, n from 10³ to 10¹² (log p/log n from 0.22
to 0.92), 27 runs (numerics/s1_out/): the **candidate-restricted** search (all flips; swaps restricted to top-12
deletions × all outside, all retained × top-12 additions, and all same-group pairs; bcs_core.py `Path._swaps`) is a pure
null deletion ending at S₀ in 27/27, with best addition and best candidate swap ≈ ½ log n below the chosen deletion.
Complete-scan certification (every swap pair) on p ≤ 500: numerics/s1_exh/ (S1-EXH), rerun with the lexicographic tie rule in s1_exh2/ (S1X2_summary.txt; 0 exact ties). (ii) Deleted nulls do jump
when group-mates are deleted: the largest outside |τ| reaches ≈ 1.9–2.0 × the current deletion level during
within-group cascades; but within a group (global level known) the group is exactly compound symmetric and greedy
elimination satisfies a re-add invariant exactly in 300/300 trials (S2). (iii) The global error e_T (the only
cross-group coupling) satisfies κ₀|e|/H_q ≤ 0.05 while ≥ 30 nulls are retained and ≤ 0.23 overall, the maximum being
attained with 2–5 retained nulls (numerics/S3_summary.txt, s3b_out/), i.e. near the end κ₀|e| is a non-vanishing
fraction of H_q (heuristically ≈ H/(s₀ + 1 + (1 − ρ_b)/ρ_b) with imbalance ±1, H := √(2 log 2p); not used in any proof),
which is why the centre condition below is size-dependent.

**Theory diagnosis.** Every neighbour score is an exact function of per-group CS statistics and one scalar, the
global error e_T (L1). Outside-null statistics split as τ = (group part) + (κ·e_T) with |group part| ≤ H_q uniformly
over all 2^{q̄}·p (null, mate-set) pairs. Hence **for log p/log n < 1/2 the whole path analysis reduces to one scalar
condition — control of e_T along the path** — and the within-group jumps are irrelevant there. Lattice (all-set)
bounds on e_T are of the same order as the deletion level itself; with them the conditions of
(C2-R) can be verified only below exponent 1/6 (FAC-A's lattice exponent; FAC-A proves sharpness of 1/6 only for the
full-lattice route in exact compound symmetry, not necessity for S5). Path control of e_T is the proposed direction
beyond 1/6; no necessity claim is made.

**Tier 1 (proof target of this ticket, through the full review pipeline): Theorem FAC-BCS-R (reduction).** (C1) start
mode for every p ≤ ⌊n/2⌋; (C2-R) path lemma under the global-centre condition CC_n; (C3-R)/(C4-R) consistency and
delivery up to P̃(CC_nᶜ) (P̃: the enlarged probability space of §3).
**Tier 2 (attempted; claimed only if proved and checked): Lemma KL** — for a chosen α₀ < 1/2, a fixed δ > 0 with
α₀ ≤ (1 − δ)/2 and P̃(CC_n(δ)) → 1 along every sequence with limsup log p/log n < α₀; this turns Tier 1 into the
unconditional Theorem FAC-BCS there (ideal: for every α₀ < 1/2 such a δ exists) [v2.2 wording fix, R05 item 1].
If KL is not proved, the ticket reports PARTIAL with KL as the exact obstruction (with evidence).

## 1. Setting (as FACB STATEMENT §1)

* D0, prior, block tables, start mode, F(S) := log w(|S|) + log m(S): SoP `04_theory.tex:69-74`, FINAL `s1_setting.tex`
  (verbatim as FACB STATEMENT §1).
* **G** (fixed design; FACB §1): X := CX^rD_x⁻¹, θ* := D_xβ, μ = Xθ*, Y = Cy^r = μ + Cε, ε ~ N(0, σ²I), σ² fixed,
  S₀ = supp θ*, s₀ ≥ 1 fixed; the score uses y = Y/s, s² = ‖Y‖²/(n − 1).
* **Method**: v3.1 as merged on main 4676af6; LS0 from the emitted start-mode centre with cap a_n = ℓ_n + |S̃₀|
  (MR1), ℓ_n = ⌈log₂(n + p + 1)⌉; implementation premises named exactly as FACB STATEMENT §1 (EX-A, EX-S, SR,
  GUARD-W, OP-LS0 with cap a_n, e4 read as e4′, complete scans; for R′ > 4, IND-T and the c₄ search; CAL only for the
[M5-0] route). Blocks: the method's
  partition (size ≤ 16); (C1)–(C3) hold for every deterministic partition into blocks of size ≤ 16.

## 2. Hypotheses (class BCS)

* **(BCS) exact-Gram block compound symmetry.** XᵀX = (n − 1)Υ_nΣ_nΥ_n, Υ_n diagonal ±1, with
  Σ_n = ρ_b11ᵀ + ⊕_{g=1}^{J_n}(bJ_{q_g} + dI_{q_g}) (J_n groups), b := ρ_w − ρ_b > 0, d := 1 − ρ_w > 0, 0 < ρ_b < ρ_w < 1 fixed,
  group sizes 1 ≤ q_g ≤ q̄ (q̄ fixed; the groups G_g partition [p]; unrelated to the method's blocks).
  Study S5: ρ_b = 0.3, ρ_w = 0.7, q_g = 5.
* **(P)** p_n ≤ ⌊n/2⌋ for (C1); **(P_α)** limsup log p_n/log n < α for the path claims (C2-R)–(C4-R), with α < 1/2.
* **(θ)** s₀ fixed; the sign-corrected truth coefficients (Υ_nθ*)_{S₀} equal a fixed vector ϑ ∈ (ℝ∖{0})^{s₀}; the
  positions of S₀ (and their group/block incidences) may vary with n.
* **(FS-BCS) generic no-cancellation.** For U ⊆ [p] contained in one method block, |U| ≤ 15, and l ∉ U in the same
  block, let c(U, l) := Cov(x_l, μ | x_U) (population, Σ-scale). Require: c(U, l) ≠ 0 unless U ⊇ S₀ and l is null.
  Σ⁻¹ = D⁻¹ − ρ_b(D⁻¹1)(D⁻¹1)ᵀ/(1 + ρ_b1ᵀD⁻¹1), D := ⊕(dI + bJ), has strictly negative off-diagonal entries (and so
  does the inverse of every principal submatrix, being of the same form); hence Cov(x_l, x_i | x_U) > 0 for distinct
  l, i ∉ U (it is 0 when i ∈ U). So c(U, l) = Σ_{i∈S₀∖U}ϑ_iCov(x_l, x_i | x_U) is a linear form in ϑ with strictly
  positive coefficients on S₀ ∖ U and zero coefficients on the conditioned truths S₀ ∩ U (after sign correction).
  Its coefficients depend only on the incidence pattern of U ∪ {l} ∪ S₀ (which indices share a group), with the truth
  labels retained; over the whole n-sequence there are finitely many such patterns (|U| ≤ 15, s₀ fixed), so (FS-BCS)
  excludes finitely many proper hyperplanes of ϑ, and c_FS := min |c| over all nonzero values arising along the sequence
  is a positive constant (proof: L2.1).

## 3. Definitions used in the claims (precise forms in lemmas/L1)

**Probability space.** After sign correction, g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ) and r := ‖(C − P_X)ε‖²/σ² ~ χ²_{n−1−p}
are independent; every score, block table, start-mode quantity, deterministic LS0 search and data event used here is a
function of (g, r) and the deterministic design/θ* (L1.1); the full method additionally uses its independent algorithmic
uniforms (R06 item 10).
On an enlarged space we realise g_j = h + y_j, h := √ρ_b η, y_j := √b ζ_{g(j)} + √d ξ_j, with η, (ζ_g), (ξ_j), r
independent, η, ζ_g, ξ_j ~ N(0, 1); all events below (E_n, CC_n) live on this space, and events measurable in the data
have their original probabilities.
**Statistics.** For R ⊆ [p] and l ∉ R: v_{l|R} := Σ_ll − Σ_{lR}Σ_RR⁻¹Σ_{Rl}, τ_{l|R} := (g_l − Σ_{lR}Σ_RR⁻¹g_R)/√v_{l|R}
(R = ∅: τ_{l|∅} = g_l). e_R := h − E[h | g_R] (e_∅ := h), V_R := Var(e_R) = [ρ_b⁻¹ + Σ_g|R∩G_g|/(d + b|R∩G_g|)]⁻¹.
With U := R ∩ G_{g(l)}, u := |U|, a_u := d/(d + ub), ψ_u := d[d + (u + 1)b]/(d + ub),
A_l(U) := [y_l − bΣ_{j∈U}y_j/(d + ub)]/√ψ_u ~ N(0, 1), the exact identity (L1.3) is
  τ_{l|R} = (√ψ_u A_l(U) + a_u e_R)/√(ψ_u + a_u²V_R),  hence |τ_{l|R}| ≤ |A_l(U)| + κ₀|e_R|, κ₀ := (1 − ρ_b)^{−1/2}.
For T ∋ j the deletion statistic of j is τ_{j|T∖j} (controlled by e_{T∖j}); for l ∉ T the addition statistic is
τ_{l|T} (controlled by e_T).
**H_q** := (2 log(2^{q̄}p) + 2L_n)^{1/2}, L_n := log log n.

**The path Π (defined through the actual score).** T_0 := S* := [p] ∖ N₀ (N₀ as in L2), and while T_i ≠ S₀:
T_{i+1} := T_i ∖ {j_i}, where j_i is the null j ∈ T_i maximising the exact score gain F(T_i ∖ {j}) − F(T_i) (F the
method's ridge score with the normalised response, signal and residual energy; exact ties broken by taking the
lexicographically smallest resulting set, as the production rule does). Π stops after m₀ steps at T_{m₀} = S₀
(indices i = 0, …, m₀, the terminal index included).
**Global-centre condition CC_n(δ)** (δ ∈ (0, 1) fixed): for every i ∈ {0, …, m₀} (k := |T_i|) and every
T′ ∈ {T_i} ∪ {T_i ∖ {j} : j ∈ T_i ∖ S₀}:
  (H_q + κ₀|e_{T′}|)² ≤ (1 − δ)·Λ_k,  Λ_k := log n + 2 log((2p − k)/(k + 1)).
(Exact requirement κ₀|e_{T′}| ≤ √((1 − δ)Λ_k) − H_q. If log p/log n → a, at k ≍ p a positive leading-order allowance
for e needs a < (1 − δ)/2 (a ≤ (1 − δ)/2 is necessary at leading order) [v2.1 wording fix, R03 item 3, post-lock, no claim changed];
near the end Λ_k ≈ log n + H_q², so κ₀|e| of order H_q is allowed. The earlier form "κ₀|e| ≤ cH_q" is false near the
end of the path, LOG 09:36.)

## 4. Claims

* **(C1) Start mode.** Under G, (BCS), (P), (θ), (FS-BCS): P(S* is the unique maximiser of γ₀ on Ω) → 1, with
  N₀ := ⋃{C_b ∖ S₀ : S₀ ⊆ C_b} (|N₀| ≤ 15). On this event S̃₀ = S* ⊇ S₀, |S̃₀ ∖ S₀| = m₀ := p − s₀ − |N₀|.
* **(C2-R) Path lemma (key lemma of Tier 1).** Under G, (BCS), (P_α) with α < 1/2, (θ), and any fixed δ ∈ (0, 1):
  there are events E_n with P(E_n) → 1 such that on E_n ∩ CC_n(δ), for n ≥ n₀, the uncapped §6.10 search from S*
  follows Π: at every T_i ≠ S₀ the chosen move is a null deletion with gain ≥ (δ/8) log n, every addition and every
  null-out swap has gain smaller than the chosen deletion by ≥ (δ/8) log n, and every move removing a truth (truth
  deletion, truth-out swap) has gain ≤ −c_θ n; after exactly m₀
  moves it is at S₀, where every feasible neighbour has strictly smaller F. Consequently LS0 with cap a_n ≥ m₀ ends at
  S₀ as a certified search endpoint.
* **(C3-R) Consistency up to the centre condition.** Under the hypotheses of (C2-R) and (C1), the implementation
  premises (with CAL) and MR1: (H0) holds; D_n ≤ P̃(CC_n(δ)ᶜ) + o(1); P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P̃(CC_n(δ)ᶜ) + o(1).
* **(C4-R) Delivery up to the centre condition.** Under the hypotheses of (C2-R), (C1) and all premises of Proposition F
  as in FACB (C4) (CAL not assumed): P(no output) = 0 for every admissible n ≥ 3 and P(Ŝ⁺ ≠ S₀) ≤ P̃(CC_n(δ)ᶜ) + o(1).
* **(C5) Tier 2 (KL), claimed only if proved and checked:** P(CC_n(δ)) → 1 for some fixed δ > 0 along every sequence
  with limsup log p/log n < α₀ (some α₀ > 1/6, ideally every α₀ < 1/2), giving the unconditional Theorem FAC-BCS there:
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and, with all premises of (C4-R) including Proposition F's amended allocation, P(Ŝ⁺ = S₀) → 1.
  Without a checked KL the ticket result is PARTIAL.
* **(C6) Frontier (evidence; not proved).** CC numerics; within-group structure (CS per group, re-add invariants) as a
  proposed (conjectural) route beyond 1/2 — no necessity claimed; p > n/2 as FACB §5(a).
* **Proof obligations recorded at lock (R01 item 2):** uniform control of (a) the ridge regularisation H = (n² − 1)Σ + I
  and the resulting signal leakage for T ⊇ S₀; (b) M_T = ½(1 + o(1)) at every base T ⊇ S₀ incl. null one-deletion sets;
  (c) occupancy-dependent determinant increments L(R ∪ l) − L(R) = log(n + 1) + o(1) uniformly; (d) truth deletions and
  truth-out swaps by a separate signal argument (Gram floor d, uniform noise-projection bounds), no CC needed; (e) outside
  nulls include N₀.

## 5. Not claimed

Finite-n bounds; anything about CC_n beyond (C5) unless proved; random rows; general factor loadings; p > n/2 for the
path claims; changes to shipped components.

## 6. Dependencies (statuses verbatim, as FACB STATEMENT §6)

M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; S-T/T03♯ "PROVED; SF VERIFIED (W2-VT03R);
XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma CAP (FINAL s7)
"PROVED (by this seat)", council-checked; Proposition F (A1 corrected statement, council round 3 passed; preflight
addition A4 "OK-WITH-FIXES") and F-GROW (A2 "PROVED (A2), checked by A3"). From FACB (Theorem FAC-CS "PROVED-CHECKED",
REPORT §1): the algebra of L1.5 (Q vs RSS) and the assembly pattern of L5, re-verified here for BCS.
