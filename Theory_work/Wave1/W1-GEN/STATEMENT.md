# W1-GEN — STATEMENT (target statement)

Ticket W1-GEN, Theory Wave 1. Lead: Claude Opus 5.5.
Status of this file: **v2.3** (v2 LOCKED 2026-11-08; v2.1 (C6) design, v2.2 (C1′) added, v2.3 (C5)(d) layout and (C1′) energy — all logged in LOG.md) after statement-lock review R01 (Codex gpt-6.1-sol high,
LOCK-WITH-CHANGES; all nine required changes applied, see `reviews/R01_statement_lock_sol.md` and its disposition
`reviews/R01_disposition.md`). Later changes are logged in LOG.md and flagged in REPORT.md.

SoP = `Theory_work/State_of_Project/sections/`; NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`;
BS = `NBH/branch_snapshots/`; T22iii = `Docs/Theory/proofs/T22iii_T16_start_aggregation/`.

## 0. Target and how this statement answers it

Goal (HQ brief): consistency of the method's **reported** HPM Ŝ⁺ on a general, checkable class of correlated designs,
p ≤ n^A (A > 1 allowed), masking allowed, of the form "on 𝒟(...), P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0", with LH, W, LH-iid as
instances. Starting point, M5(0) (SoP `04_theory.tex:464-539`, T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF:
VERIFIED* (A-REV5))"), at every n and any X:

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n,   D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺})  (potential-run notation).     (M5-0)

S-T (TH09, T03♯) gives 1 − π(S₀) → 0 in probability, hence E₀[1 − π(S₀)] → 0 (bounded convergence). **The new
content: a general design class on which D_n → 0.** This is a sufficient class, substantially narrower than "any
correlated design" (CE169; non-identifiable designs; see §4).

## 1. Setting

* **D0** as in SoP `04_theory.tex:69-74`: shipped g = n score, a₀ = b₀ = 0.01, normalized capped BB(1,p) prior,
  K = min(p, ⌊n/2⌋), Ω = {S : |S| ≤ K}, tables r_b(U) = m(U)/m(∅), start γ₀ ∝ w(|S|)∏_b r_b(S ∩ C_b) on Ω, π₀,
  start mode S̃₀ = argmax_Ω γ₀ with the size-then-lex tie rule.
* **G**: fixed raw design X^r (n × p, nonconstant columns), y^r = α1 + X^rβ + ε, ε ~ N_n(0, σ²I), σ² > 0 fixed;
  X = CX^rD_x⁻¹ (‖x_j‖² = n − 1), μ := CX^rβ = Xθ*, θ* := D_xβ, S₀ := supp β, s₀ := |S₀| ≥ 1 fixed, p = p_n ≤ n^A
  (A ≥ 1 fixed; p ≫ n allowed).
* **Notation.** P_T: projection on span X_T; Λ_T := ‖(I − P_T)μ‖²; Δ_T := Λ_T/(n − 1); v_T := σ² + Δ_T;
  R̂_T := X_TᵀX_T/(n − 1); θ*_min := min_{j∈S₀}|θ*_j|. For a pair (T, l), l ∉ T, **only on the families named below,
  where the relevant SE guarantees (I − P_T)x_l ≠ 0**: u_{T,l} := (I − P_T)x_l/‖(I − P_T)x_l‖, δ_{T,l} := u_{T,l}ᵀμ,
  so that Λ_T − Λ_{T∪{l}} = δ²_{T,l}. For T with λ_min(R̂_{T∪{l}}) = 0 we use the projection form
  Λ_T − Λ_{T∪{l}} (always defined).
* **Blocks** C₁, …, C_J: the method's actual partition (complete linkage on 1 − |r̂|, top-down cut at B, next-fit
  packing; B = min(⌊√n⌋, ⌊√p⌋, 16)), SoP `02_method.tex:187-211`; under G a deterministic function of X.
* **Method:** v3.1 with LS0 as specified (SoP `02_method.tex:490-506`); local search M §6.10 (SoP `02_method.tex:463-467`);
  cap ℓ_n = ⌈log₂(n + p + 1)⌉. A *move* is a strict improvement to the best scanned neighbour (lexicographic ties);
  every scanned neighbour is scored; after ℓ moves one further scan; the LS0 centre is emitted (scored).
* **Implementation premises** (named, not proved here; M5's list, SoP `04_theory.tex:86`): EX-A, EX-S, CAL, SR,
  GUARD-W, OP-LS0, **e4** (emitted LS0 centre = the prescribed start-mode maximiser; DP invariant N3 OPEN, owned by
  W1-N3), complete scans; for R′ > 4 also IND-T and the extra search from c₄ (nested scored set).

## 2. Hypotheses

**(H0) = the hypotheses of S-T/T03♯** (SoP `04_theory.tex` TH09 card, from NBH TLF:448-451), written out:
* R1: fixed s₀ ≥ 1, p ≤ n^A, s₀ ≤ K eventually; G;
* R: ‖μ‖² ≤ Mn for a fixed M; λ_min(R̂_{S₀}) ≥ φ₀² for a fixed φ₀ > 0;
* SE_λ(j₀), j₀ := ⌈(2A + 1)s₀⌉ + 1: λ_min(R̂_{S₀∪J}) ≥ φ₀² for every J with |J| ≤ j₀ (normalized);
* SE_w(m♯_n; g₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for every |J| ≤ m♯_n (unnormalized; fixed g₀ > 0), where
  m♯_n := min{m ≥ s₀ : R_m ≤ n^{−(s₀+2)/2}}, R_m := Σ_{k=max(m+1,0)}^{K} C(p,k) w(k)/w(s₀) (deterministic, data-free);
* BM-∞: θ*²_min n φ₀²/(σ² log n) → ∞. (BM(c > c₀) is not used.)

**(H1) Bounded, separated relevance set (descent).** Deterministic sets 𝒱_n ⊇ S₀ with |𝒱_n| ≤ v̄ (fixed) such that
* (H1a) SE on 𝒱: λ_min(R̂_{𝒱∪{l}}) ≥ φ₀² for every l ∈ [p];
* (H1b) SEP(c_S): ζ_n := max{Λ_S − Λ_{S∪{l}} : S ⊆ 𝒱, l ∉ 𝒱} ≤ c_S (n − 1) φ₀⁴ θ*²_min eventually, for a fixed
  c_S ∈ [0, 1). Convention: ζ_n := 0 if 𝒱 = [p].
  Variables outside 𝒱 may be correlated among themselves (subject only to (H0)'s anchored sparse-eigenvalue
  conditions and (H2a)); they only must not carry, given any subset of
  𝒱, more partial signal than the fixed fraction c_S of the guaranteed best-truth decrement (n − 1)φ₀⁴θ*²_min.

**(H2) Centre (on the actual blocks).** A deterministic reference S* ⊆ 𝒱 (S* ∈ Ω, s* := |S*| ≤ v̄,
U*_b := S* ∩ C_b) such that
* (H2a) within-block SE: λ_min(R̂_T) ≥ φ₀² for every nonempty T ⊆ C_b, every b;
* (H2b) VIS(S*): for a deterministic M_n → ∞, g_{b,U} := ‖(P_{U∪U*_b} − P_U)μ‖² ≥ M_n v_U log n for every b and every
  U ⊆ C_b with U*_b ⊄ U;
* (H2c) NL(S*): with the leakage family 𝓛(S*) := {(b, T, l) : l ∈ C_b ∖ U*_b, U*_b ⊆ T ⊆ C_b ∖ {l}},
  (i) δ²_{T,l} ≤ C_L σ² log n on 𝓛(S*) for a fixed C_L < ∞, and
  (ii) NL_avg(κ) for a fixed κ > 0: if p > s*, eventually
  (p − s*)⁻¹ Σ_{l∉S*} max_{T:(b(l),T,l)∈𝓛(S*)} exp(E_{T,l}) ≤ n^{1/2−κ}, where, for a fixed ε₀ > 0 and
  h_n := √(2(A + ε₀) log n), E_{T,l} := min{δ²_{T,l}/(2Δ_T), δ²_{T,l}/(2v_T) + |δ_{T,l}|σh_n/v_T}, with E_{T,l} := 0
  when δ_{T,l} = 0 (in particular when Δ_T = 0); the average is omitted when p = s*.
  (NL_η(S*): δ²_{T,l} ≤ ησ² log n on 𝓛(S*) with 0 ≤ η < (√(2A+1) − √(2A))², implies (i) and (ii), as in T22iii §2.)

S* is an **existential certificate** depending on (X, β, σ², partition): it is not required to be the exact minimiser
of Λ in each block (exact minimisers can contain nulls with negligible gain and violate VIS; R01 item 2). Masking is
allowed: true variables with no block-level signal given U*_b are omitted from S* (they lie in 𝓛(S*)), and S* may
contain nulls (block-level proxies).

## 3. Claims

**(C1) Centre law (generalized T22(iii)).** [G, R (bounded energy only), p ≤ n^A, (H2), s* ≤ v̄]: 1 − π₀(S*) → 0 in
probability; on {π₀(S*) > ½} the maximiser of γ₀ is unique, so S̃₀ = S*; hence P(S̃₀ = S*) → 1. The proof re-runs
the locked T22(iii) argument (reference S₀) with reference S*, with (H2c) in place of NL_η, and with EXP′ **proved**
(uniform score expansion, L1) instead of assumed.

**(C1′) Canonical certificate (added after R05, v2.2; sufficient condition for (H2b)–(H2c), no hypothesis changed).**
Under (H2a), let γ_b be the coefficients of the projection of μ on span X_{C_b} (the regression of μ on the block's own
columns). Assume also ‖μ‖² ≤ Mn. If every γ_b = γ^L_b + γ^S_b (disjoint supports) with, for a fixed
η ∈ [0, (√(2A+1) − √(2A))²) and some M_n → ∞, (i) ‖X_{C_b}γ^S_b‖² ≤ ησ² log n and (ii)
√((n − 1)φ₀²)·min_{j∈supp γ^L_b}|γ^L_{b,j}| ≥ √(ησ² log n) + √(M_n(σ² + 2M) log n) whenever supp γ^L_b ≠ ∅,
then S* := ∪_b supp γ^L_b
satisfies (H2b) and NL_η(S*) (lemmas/L8_certificate.md). Masked truths = truths with zero (or negligible) block
coefficient. Checkability: the hypotheses are explicit inequalities in (X, β, σ², partition) — oracle quantities —
not an observable test from X alone; (H1)–(H2) are polynomial-size checks for given bounded certificates.

**(C2) Descent.** For C ⊆ 𝒱, C ∈ Ω, let τ(C) ∈ ℕ ∪ {∞} be the number of moves of the **uncapped** greedy path
(M §6.10 without the cap) from C before it first reaches S₀. [G, R, s₀ fixed, p ≤ n^A, BM-∞, (H1)]: there are events
Ω_n with P(Ω_n) → 1 such that on Ω_n, simultaneously for every such C: every **centre** of the uncapped path lies in
2^𝒱 (scanned neighbours may lie outside 𝒱), τ(C) ≤ 2^{v̄} − 1, and S₀ has no strictly improving feasible neighbour.
Consequently the capped production search from C scores S₀ whenever ℓ ≥ τ(C) − 1 (S₀ is the emitted centre if
C = S₀) and, whenever ℓ ≥ τ(C), its search endpoint is S₀, reached with a completed scan that finds no strict
improvement and without `local_limit` (wording clarified after R04: the public flag `local_certified` is evaluated on
the finally reported HPM, SoP `02_method.tex:505-506`).

**(C3) Main theorem.** [(H0), (H1), (H2), premises of §1]. For all n ≥ n₀ (the onset of L3, which includes
⌊n/2⌋ ≥ v̄ + 1, the BM-∞ and SEP onsets) with ℓ_n ≥ 2^{v̄} − 2: D_n ≤ P(S̃₀ ≠ S*) + P(Ω_nᶜ), where
P(Ω_nᶜ) = O(1/log n) (wording aligned with L5.1 after council R12). Hence D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and
liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup_n P(U_n). No delivery claim.
**(C3-fav)** If S* = S₀: under (H0), (H2) and the premises (no (H1)), D_n ≤ P(S̃₀ ≠ S₀) → 0 and the same conclusions
hold (BM-∞ enters only through (H0)).

**(C4) Random designs.** Let X^r be random, independent of ε; β may be X-measurable (as when a generator scales
signal on sample-standardized columns). Let 𝒜_n be X-measurable events with P(𝒜_n) → 1, and let 𝒱_n, S*_n be
X-measurable. Suppose that every deterministic sequence x_n ∈ 𝒜_n satisfies (H0)–(H2) (resp. (H0), (H2) with
S* = S₀) with the **same** fixed constants (A, M, φ₀, g₀, v̄, c_S, C_L, κ, ε₀) and the **same** deterministic
envelope sequences (a sequence b_n → ∞ lower-bounding θ*²_min n φ₀²/(σ² log n), and M_n → ∞ in VIS). Then the
conclusions of (C3) (resp. (C3-fav)) hold under the joint law of (X, ε).

**(C5) Instances** (each an explicit proof obligation).
(a) *LH, exact Gram* (BS/W4-T38FULL/T38_PROOF.md:217-235): X'X = (n − 1)Σ_LH, p ≤ n − 1; groups of size g, within
equicorrelation ρ_h ∈ [ρ₋, ρ₊] ⊂ (0, 1); c linked pairs (a_i, b_i, ψ_i), 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i}), cross-group
correlation only inside pair units via the hubs (rank-one), as in T38_PROOF.md:224-235; θ_{a_i} = β_i ≠ 0,
θ_{b_i} = −ψ_iβ_i, visible hubs θ_h ≠ 0, fixed c, number of visible groups and coefficients; SIZE g ≤ B_n < 2g. Claim:
(H0)–(H2) hold with S* = S₀ ∖ M, 𝒱 = union of the signal units (pair unions and visible groups), c_S = 0, η = 0.
Input used: blocks = groups under SIZE (W1-EXP Lemma 4.2, cited with its status).
(b) *LH-iid* (BS/API-PXNGAP/PROOF.md:36-60) with SIZE, p ≤ n^A: (C4) applies with 𝒜_n built from partition recovery
(W7-PART Theorem B, candidate) and [CONC]; (H1), (H2) to be **verified directly** on 𝒜_n (deterministic envelopes),
not inferred from API-PXNGAP's start result. Conditional on the candidate inputs; labelled so.
(c) *W* (exact Gram, groups of 9 at ¼, cross ε_n = 1/(np), two n^{−1/4} signals in different groups, σ² = 1; BS/MEET-THM
TLF:71,178, R1_C.md:362-363): (H0) verified directly (no S-T row exists for W, SoP `04_theory.tex:846`), and
(C3-fav) with S* = S₀.
(d) *Study generator* (Scripts/Data_generators/gen_dev_data.R:18-42). Asymptotic sequence: groups of 5; p_n = 5G_n → ∞,
p_n ≤ n^A; (v2.3, after sweep R10 item 6) s₀ = 14 with one of the study's two high-p layouts at fixed indices (step 7
or step 13, the R code's positions), extended as a theoretical sequence (the R function defines truth only for
p ∈ {30, 500, 1000}); the 14-entry β pattern (1.4, −1.0, 1.8, −1.2, 0.8, −1.6 cycled) and fixed signal scale c; iid N(0, Σ_s) rows,
σ² = 1; signal formed on sample-standardized columns (β X-measurable, (C4)). Claim to be proved or refuted per
scenario: S1, S3, S4, S6 covered by (C3-fav) via (C4); S2 (AR(1)) and S5 (between-group 0.3) not covered (to be
explained, with the failing hypothesis). The partition is checked as it is (unions of whole groups for S3/S4/S6 on a
margin event), not assumed to equal groups. At n = 200 nothing quantitative is claimed; M5(0) remains the every-n
statement.

**(C6) Boundedness of the relevance set cannot be dropped from the LS0 route.** (v2.1 after R06, see LOG.) An
explicit exact-Gram design (s₀ ≥ 17 mutually orthogonal truths, so no block table scores S₀; one truth x₀ carries
d_n ≍ log n weak, nearly orthogonal proxies x_i = (a/√d_n)x₀ + √(1 − a²/d_n) z_i; other nulls orthogonal) satisfies
(H0), (H1a), (H1b) with 𝒱 = S₀ ∪ proxies, (H2a), and VIS/NL for the growing reference S* = S₀ ∪ (proxies outside
x₀'s block) — every hypothesis except the two size bounds |𝒱_n| ≤ v̄ and s* ≤ v̄ — and with probability → 1,
|S̃₀ Δ S₀| ≥ ⌈d_n/B⌉ − 1 > 2(ℓ_n + 1). Since each move changes at most two memberships, LS0 (ℓ_n moves plus a final
scan) scores only models within symmetric-difference distance 2(ℓ_n + 1) of S̃₀, so P(LS0 from S̃₀ misses S₀) → 1.
Conclusion: no universal LS0-discovery guarantee survives removal of both size bounds (the inclusion
D_n ≤ P(LS0 misses S₀) stays true; its right side tends to one). Not claimed: that the full method's D_n fails to
vanish (the SMC or the final local search may score S₀). Growth slower than the cap is not excluded.

## 4. Not claimed

P(U_n) → 0 (delivery); anything about v3 without LS0; posterior consistency beyond T03♯ (cited); growing s₀;
exponential p; any finite-n bound (all asymptotic; at n = 200 the margins are not expected to bite); masked PIP/evidence
accuracy; necessity of the class beyond (C6); designs with unbounded relevance sets (e.g. fixed-ρ AR(1), common-factor
designs) — frontier.

## 5. Dependencies (status as recorded; never upgraded)

* M5(0): T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))".
* S-T: T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; T01–T03 PROVED-LOCKED, SAME-FAMILY-ONLY.
* T22(i): "PROVED-LOCKED" (deterministic; any partition with |C_b| ≤ K, positive tables, any feasible reference).
* T22(iii): "PROVED-LOCKED CONDITIONAL" (reference S₀, EXP′ assumed): re-run here with reference S*, EXP′ proved.
* Operational closure [OP] 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆ {LS0 from S̃₀ does not score S₀}: PROVED (by this seat, unchecked)
  from the named premises (L5); corroborated by [W6] (BS/W6-FIXREV1) as used in BS/API-PXNGAP/PROOF.md:443-446
  (candidate).
* Instances only: blocks = groups on LH (W1-EXP Lemma 4.2), W partition (TLF:71), W7-PART Theorem B (candidate),
  [CONC] (classical).
