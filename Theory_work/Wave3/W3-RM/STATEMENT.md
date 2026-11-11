# W3-RM — STATEMENT (Theorem 3: the reported model under visibility (V) and bounded leakage (L))

Ticket W3-RM, Theory Wave 3 (PROGRAM item 3). Lead: Claude Fable 5.2 (Claude Personal, effort high).
Status of this file: **v1.2.1** (2026-11-09; v1.2.1 = council round-1 wording/record fixes [C1-A#], [C1-B#], no hypothesis
or conclusion changed) = v1.1 LOCKED + three post-lock **weakenings of hypotheses** adopted from the
"better theorem" review R02 (`reviews/R02_disposition.md`; markers [P1], [P2], [P3a]) and one corollary [P7]; every v1.1
hypothesis implies its v1.2 replacement, so the locked v1.1 theorem is a special case. v1.1 was LOCKED after statement-lock review R01 (Codex gpt-6.1-sol high,
LOCK-WITH-CHANGES; all five required changes and the four optional suggestions applied, `reviews/R01_disposition.md`;
change markers [R01-#]). Protocol: `Theory_work/Wave3/PROTOCOL.md`.
All results are asymptotic (n → ∞). Method = production core as on main (LS0 from the start mode, move cap
ℓ_n + |S̃₀|; tie-aware start-mode DP; `Scripts/SMC_BVS/core/`). **No method change is requested.**

Abbreviations. GROW = `Theory_work/Wave1C/C-GROW/`; GEN = `Theory_work/Wave1/W1-GEN/`; APP = `Theory_work/Wave2/W2-APP/`;
LOC2 = `Theory_work/Wave2/W2-LOC2/`; UNI = `Theory_work/Wave2/W2-UNI/`; N3 = `Theory_work/Wave1/W1-N3/`;
PACK = `Theory_work/Wave1C/C-PACK/`; DLV = `Theory_work/Wave1C/C-DLV/`; ENG = `Theory_work/Wave1C/C-ENG/`;
FIN = `Theory_work/Wave1C/FINAL/sections/`; CORE = `Scripts/SMC_BVS/core/`.

## 0. What is claimed, in one paragraph

Theorem 3 has one deterministic core and two primitive forms. **Core (RM-0):** for any design and any deterministic
Q ⊇ S₀, on the data event Sand(Q) ∩ NA(Q) ∩ TL(Q) the coded LS0 deletes the start mode's extras one per move and scores
S₀; with posterior concentration, every run that returns output — whatever its seed, N_e, R′ and calibration outcome —
reports Ŝ⁺ = S₀ on a data event of probability → 1. **Form F (fixed design; GROW's form made primitive):** the three
events follow from Theorem 1's conditions, eigenvalue floors, **(V)**, **(L)** with a leakage set Q, and a lattice
condition **(N)** that is automatic when |Q ∖ S₀| ≤ (1 − δ₀) log n. No block, partition or design family appears.
**Form R (Gaussian rows; polylogarithmic Q):** the same from population versions of (V) and (L) on (Σ_n, θ*), with (L)
carrying a localisation clause, plus a population lattice condition (D). Metric-local designs (UNI-0) and
block-diagonal designs with growing one-factor groups (LOC-BF) are examples, not hypotheses. Premise e4 is replaced by a
code-level lemma (E4). The plain statement "(V) + (L) with |Q| ≤ C log n for arbitrary C, nothing else" is **not**
claimed: see §6.

## 1. Settings, method objects, events

* **Setting F (fixed design)** = GROW `STATEMENT.md` §1 (D0 score, capped BB(1, p) prior w, K = min(p, ⌊n/2⌋),
  Ω = {|S| ≤ K}, F(S) = log w(|S|) + log m(S), block tables r_b, start law γ₀ ∝ w(|S|)∏_b r_b(S ∩ C_b), start mode S̃₀;
  model G: fixed raw design, y^r = α1 + X^rβ + ε, ε ~ N_n(0, σ²I), σ² > 0 fixed; X centred and standardised,
  μ = Xθ*, S₀ = supp θ*, s₀ = |S₀| ≥ 1 fixed, p = p_n ≤ n^A, A ≥ 1 fixed). Notation: P_T projector on span X_T;
  R̂_T := X_TᵀX_T/(n − 1); for l ∉ T with (I − P_T)x_l ≠ 0: u_{T,l} := (I − P_T)x_l/‖(I − P_T)x_l‖,
  **δ_{T,l} := u_{T,l}ᵀμ** (so δ²_{T,l} = ‖(P_{T∪{l}} − P_T)μ‖², the gain in explained mean when l joins T),
  Z_{T,l} := u_{T,l}ᵀε/σ. θ*_min := min_{S₀}|θ*_j|.
* **Setting R (Gaussian rows)** = UNI `STATEMENT.md` §1 design (R) / LOC2 `STATEMENT.md` §1: raw rows iid
  N(m_n, Σ_n), Σ_n unit-diagonal, X centred and sample-standardised, Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of the
  raw design, σ² > 0 fixed [C1-B7], s₀ fixed, |θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞) on S₀, p ≤ n^A (p ≫ n allowed). W denotes a
  population row.
* **Move cap.** ℓ_n := ⌈log₂(n + p + 1)⌉ (the method's base cap); LS0's shipped cap is ℓ_n + |S̃₀| [C1-B4].
* **Blocks.** The method's partition C₁, …, C_J (complete linkage on 1 − |r̂|, cut at B = min(⌊√n⌋, ⌊√p⌋, 16), next-fit
  packing; SoP `Theory_work/State_of_Project/sections/02_method.tex:187-211`): an X-measurable partition with
  |C_b| ≤ 16. Nothing else about the partition is used anywhere below.
* **Events** (GROW L1, L3, L4), for a deterministic Q ⊇ S₀ with |Q| ≤ K and 𝓛 := {T : S₀ ⊆ T ⊆ Q}:
  Sand_n(Q) := {S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω};
  NA(𝓛) := {F(T ∪ {l}) < F(T) for all T ∈ 𝓛 with |T| < K, l ∉ T};
  TL(𝓛) := {F(A) < F(T) for every T ∈ 𝓛 and every feasible neighbour A of T with S₀ ⊄ A};
  𝒦_n := {the deterministic LS0 (complete scans, cap ℓ_n + |S̃₀|) started from the coded start mode scores S₀}
  (a data event: LS0 reads no uniforms); 𝒪 = the run returns output; Ŝ⁺ = reported model; U_n = 𝒪ᶜ.
* **Implementation premises** (named, not proved; as UNI `STATEMENT.md` §1 / FIN §1.4): EX-A, EX-S, SR, GUARD-W,
  OP-LS0, complete scans; IND-T and the c₄ search when R′ > 4 (execution conventions of the method: they do not enter
  the start, lattice, posterior or pathwise-reporting arguments of (C0)–(C2) [R08-20]); CAL only where M5(0) is cited in
  its D_n form.
  **[R01-2] Configuration.** Throughout, OP-LS0 includes the shipped options `ls0 = TRUE`, `ls0_ell = ℓ_n`,
  `ls0_cap = "ell_n_plus_mode"` (the public option; it sets the internal field `ls0_cap_plus_mode`, cap ℓ_n + |S̃₀|)
  [R08-19] and `ls0_tie_dp = TRUE`: every successfully completed SMC output run in
  this configuration executes LS0 from `start_mode(...).S`; the exact branch scores every feasible model, and there 𝒦_n
  refers to the hypothetical deterministic search (PACK `lemmas/I1_e4_replacement.md:150-153`). All quantifiers over
  seeds, N_e, R′ and calibration outcomes range over valid inputs satisfying the implementation and execution premises
  (admissible runs). EX-A is an idealisation (exact arithmetic), not a binary64 theorem.
  **e4 is not a premise here**: it is replaced by Lemma E4 (§4 (C3)), whose hypotheses are N3's encoding and execution
  conditions (H1) — strengthened to include the inverse maps, see (C3) — and (H4), and EX-A for the start-mode
  arithmetic (H2).

## 2. Interface properties (PROTOCOL item 5)

| id | property | consumed by |
|---|---|---|
| [POST] | E[1 − π(S₀)] → 0 | RM-0 |
| [SAND(Q)] | P(Sand_n(Q)) → 1 | RM-0 |
| [TL(Q)] | P(TL(𝓛)) → 1 | RM-0 |
| [NA(Q)] | P(NA(𝓛)) → 1 | RM-0 |
| [E4] | the emitted LS0 centre is a maximiser of γ₀ on Ω, with or without ties | RM-0 |

[R01-4] Each primitive assumption enters through explicitly identified bridge lemmas (§4; the input map is
many-to-many and is shown below the bridge table); the assembly (C0) consumes only the interface properties listed here.

## 3. Assumptions (ids for the registry)

Fixed constants: A ≥ 1, M, φ₀ ∈ (0, 1], g₀ > 0, s₀, κ ≥ 1, δ₀ ∈ (0, 1), η ∈ [0, η_A) with
η_A := (√(2A + 1) − √(2A))² (η and δ₀, h, ρ_n are used by Form F only), and for Setting R: c > 0, θ_lo, θ_hi, a₀ > 0,
C_L, m₀.

### 3.1 Fixed design (conditions on (X, θ*) only)

* **(T1-F) Theorem 1's conditions** = (H0) of GROW `STATEMENT.md` §2 (the T03♯ hypotheses: fixed s₀, p ≤ n^A,
  ‖μ‖² ≤ Mn, SE_λ(j₀) with j₀ = ⌈(2A + 1)s₀⌉ + 1, SE_w(m♯_n; g₀), BM-∞: θ*²_min nφ₀²/(σ² log n) → ∞).
* **(FL) Floors.** (FL-16) λ_min(R̂_T) ≥ φ₀² for every T ⊆ [p] with 1 ≤ |T| ≤ 16.
  (FL-Q) λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p].
* **(V) Visibility.** There is a deterministic M_n → ∞ such that for every j ∈ S₀ and every U ⊆ [p] ∖ {j} with
  |U| ≤ 15: δ²_{U,j} ≥ M_n log n. ("No truth is masked by conditioning on at most 15 variables.")
* **(L) Bounded leakage.** A deterministic Q = Q_n with S₀ ⊆ Q ⊆ [p] such that
  (L-size) |Q| ≤ (log n)^κ; (L-feas) |Q| ≤ K, and Q = [p] or K ≥ 2|Q| + 32s₀ + 1, for n ≥ n₀;
  (L-gain) [P2] for every l ∉ Q and every U ⊆ [p] ∖ {l} with |U| ≤ 15: **δ²_{U,l} ≤ η τ²_U log n**, where
  τ²_U := σ² + ‖(I − P_U)μ‖²/(n − 1) is the residual variance that the set U leaves (noise plus unexplained mean energy).
  ("Outside Q no column gains more than η log n times the residual variance, given any ≤ 15 other columns." Since
  τ²_U ≥ σ², the locked v1.1 form δ²_{U,l} ≤ ησ² log n is a sufficient special case.)
* **(N) Lattice condition.** One of:
  **(N-χ)** |Q ∖ S₀| ≤ (1 − δ₀) log n — nothing else;
  **(N-D)** bounded direction complexity and a signal floor at the lattice scale:
  (i) there are a deterministic finite set 𝒰_n of unit vectors of ℝⁿ and deterministic ρ_n ≥ 0 with
      log|𝒰_n| ≤ log p + h log n for a fixed h < ½ [P1] (v1.1: log p + o(log n)) and ρ_n²(|Q| + log n) = o(log n),
      such that for every T ∈ 𝓛 and l ∉ T some
      v ∈ 𝒰_n ∩ span(X_{Q∪{l}}) has ‖u_{T,l} − v‖ ≤ ρ_n;
  (ii) (BM-Q) θ*²_min nφ₀²/(σ²(|Q| + log n)) → ∞.
  Sufficient for (N-D)(i) — **(N-loc)**: for every l ∈ [p] a set N_l ⊆ Q ∖ {l} with |N_l| ≤ ν_n,
  limsup ν_n/log n < 1/(2 log 2) [P1] (v1.1: ν_n = o(log n)), such
  that ‖(P_T − P_{T∩N_l})x_l‖ ≤ ρ_n‖(I − P_T)x_l‖ for all T ∈ 𝓛 with l ∉ T, with the same deterministic ρ_n and rate
  as in (i) [R01-Q5] (then 𝒰_n := {u_{T∩N_l,l} : T ∈ 𝓛, l ∉ T}, |𝒰_n| ≤ p2^{ν_n}). In particular (N-D)(i) holds with
  ρ_n = 0 whenever limsup |Q|/log n < 1/(2 log 2) (take N_l = Q ∖ {l}), and (N-D)(i) itself (ρ_n = 0, exact directions) contains GROW's
  (G4-dir); (N-loc) is not claimed to contain every low-complexity direction family. Convention [R07-4]: if
  Q = S₀ = [p] there is no pair (T, l); NA(𝓛) is vacuous, 𝒰_n may be any nonempty finite set and, in (D-R), L_n := 0.
* **Block-relative forms (weaker; what the proof consumes).** (V_b) = GROW (G3b): (V) only for U ⊆ C_{b(j)} ∖ {j}.
  (L_b): (L-gain) only for U with S₀ ∩ C_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l} (with σ² in place of τ²_U this is GROW (G3c)).
  (FL_b) = GROW (G3a) + (FL-Q).
  Claim (B1) below: (V), (L), (FL) imply (V_b), (L_b), (FL_b) for **every** partition into blocks of size ≤ 16, and
  conversely the block-relative forms for every such partition imply the partition-free ones (Lemma B1′). The
  block-relative forms refer to the method's blocks for one reason only: (L_b) conditions on the truths of l's own
  block, so it lets Q omit a column whose only gain is un-conditioned on a truth that the method happens to place in
  the same block; a partition-free condition cannot know this and must put such columns in Q.

### 3.2 Gaussian rows (conditions on (Σ_n, θ*) only)

* **(T1-R) Theorem 1's conditions** = (A1-post) of UNI `STATEMENT.md` §2, i.e. the LSF conditions of APP L1_POST(b)
  [R01-opt]: with j₀ = ⌈(2A + 1)s₀⌉ + 1, m̄_n = ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n]/log(3/2)⌉ and
  k̄_n = min{p, s₀ + max(j₀, m̄_n)}: for a fixed φ > 0, λ_min(Σ_{n,S}) ≥ φ² whenever |S| ≤ min(p, s₀ + j₀), and
  λ_min(Σ_{n,S}) ≥ ψ_n whenever |S| ≤ k̄_n, with ψ_n√n/(log n)^{3/2} → ∞. No upper spectral bound.
  Sufficient: λ_min(Σ_n) ≥ c.
* **(FL-R)** λ_min(Σ_{n,S}) ≥ c for every S with |S| ≤ 16 + s₀, and for S = Q ∪ {l}, l ∈ [p].
* **(V-R) Visibility** = PTV(a₀) (APP `lemmas/L3_LOC.md:28`): for every j ∈ S₀ and U ⊆ [p] ∖ {j}, |U| ≤ 15:
  |Cov(W_j, Σ_{k∈S₀}θ*_kW_k | W_U)| ≥ a₀.
* **(L-R) Bounded leakage, localised.** A deterministic Q ⊇ S₀ with (L-size), (L-feas) as in 3.1, and for every
  l ∉ Q a deterministic H_l ⊇ {l} ∪ S₀ with |H_l| ≤ (log n)^κ, such that for every U ⊆ [p] ∖ {l} with |U| ≤ 15,
  writing U₀ := U ∩ H_l:
  (L-gain-R) |Cov(W_l, W_j | W_{U₀})| ≤ C_L n^{−1/2} for every j ∈ S₀ ∖ U₀;
  (L-loc-R) [P3a] |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n for every v ∈ U ∖ H_l,
  j ∈ S₀ ∖ U₀, for a deterministic r_n with r_n(n log n)^{1/4} → 0 (v1.1: r_n = C_L n^{−2}).
  (L-gain-R is "(L)": outside Q the population gain of a column given ≤ 15 others is O(1), not O(log n).
  L-loc-R says a column outside Q, and the truths, are conditionally almost uncorrelated with whatever lies outside a
  polylogarithmic neighbourhood. It is needed because the partition is X-measurable: see ASSUMPTION_MAP.)
* **(D-R) Lattice condition** = hypotheses (R1)–(R3) of Lemma NA-R (LOC2 `lemmas/L2_NAR.md:23-36`) for (Σ_n, Q),
  with its full deterministic latent-extension contract (LOC2 `lemmas/L2_NAR.md:15-20`: a fixed centred jointly Gaussian
  row law on ℝ^{p+p′} extending N(0, Σ_n), rows iid, the whole extension independent of ε; functionals, coefficients,
  L_n, η_n deterministic) [R01-Q2]. Informally:
  every population residual e_{T,l} = W_l − W_Tβ_{T,l} (T ∈ 𝓛, l ∉ T) is a reference in one of ≤ p·n^{o(1)} frames of
  ≤ m₀ fixed linear functionals of an (optionally extended) Gaussian row, minus a combination of atoms of variance at
  most one with coefficient ℓ¹ norm at most L_n, L_n² log(|𝒜_n| + 1) = o(log n) [R08-18], with
  Var(reference) ≤ (1 + η_n)Var(e_{T,l}), η_n → 0.
  Sufficient — **(D-loc)**: every l has N_l ⊆ Q ∖ {l}, |N_l| ≤ ν_n with ν_n = o(log n), such that for all T ∈ 𝓛, l ∉ T:
  ‖β̄_{T,l} − β̄_{T∩N_l,l}‖₁ ≤ L_n with L_n² log(|Q| + 1) = o(log n) (β̄ = zero-padded; a fixed L suffices) and
  Var(W_l | W_{T∩N_l}) ≤ (1 + η_n)Var(W_l | W_T).

## 4. Claims

**(C0) Theorem RM-0 (core; any design, deterministic statement plus one inequality).** Let Q ⊇ S₀ be deterministic
with |Q| ≤ K. Under the implementation premises and Lemma E4:
(a) on Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛), LS0 from the coded start mode S̃₀ performs exactly |S̃₀ ∖ S₀| moves, each deleting one
element of S̃₀ ∖ S₀, stays in 𝓛, and ends at S₀ with a completed scan that finds no strict improvement; the cap
ℓ_n + |S̃₀| is never binding. Hence 𝒦_nᶜ ⊆ Sand_n(Q)ᶜ ∪ NA(𝓛)ᶜ ∪ TL(𝓛)ᶜ. [P7] In archive terms, on that event and on
every completed SMC output run: LS0's `returned` = S₀, `local_certified` = true, `local_limit` = false,
`moves` = |S̃₀ ∖ S₀|, completed scans = moves + 1 (a statement about LS0's archive, not about the public flag of the
reported model).
(b) for n with s₀ ≤ K, pathwise, for every seed, N_e, R′ and calibration outcome:
𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀) ≤ ½} ∪ 𝒦_nᶜ; the right side is a data event. Hence
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀)] + P(Sand_n(Q)ᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ), uniformly in those run parameters, and
under [POST], [SAND(Q)], [NA(Q)], [TL(Q)]: P(there is an output run with Ŝ⁺ ≠ S₀) → 0 and
P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). No delivery claim (P(U_n) → 0 is not asserted).
"There is an output run" is meant in the common-good-event sense [R01-Q7]: there is one data event 𝒢_n :=
𝒦_n ∩ {π(S₀) > ½} with P(𝒢_n) → 1 on which every admissible output run reports S₀ (no measurability question over the
calibration space arises). CAL is not used for (b).
Sources: GROW L1 (C1), L4; DLV `lemmas/L4_delivery.md:65-77` (pathwise claim); [OP] (GEN L5); M5(0).

**(C1) Theorem RM-F (fixed design).** Setting F, the method as coded. Assume (T1-F), (FL), (V), (L), (N). Then
[SAND(Q)], [TL(Q)], [NA(Q)] and [POST] hold, hence all conclusions of (C0):
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 for every seed, N_e, R′ and calibration outcome. The same holds with (V), (L-gain), (FL-16)
replaced by the block-relative (V_b), (L_b), (FL_b) on the method's actual partition (this is GROW's form).
[R01-3] Under (N-χ), on Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛), LS0 makes exactly |S̃₀ ∖ S₀| ≤ |Q ∖ S₀| < log n moves; hence this
bound holds with probability tending to one (on enumeration branches it refers to the hypothetical search). Remark
[C1-B4]: since (1 − δ₀) log n < ℓ_n, under (N-χ) the conclusion of (C1) also holds for runs configured with the old cap
`ls0_cap = "ell_n"` (GROW `lemmas/L4_assembly.md:21-22, 34-37`); beyond (N-χ) the shipped cap is used.

**(C2) Theorem RM-R (Gaussian rows, polylogarithmic Q).** Setting R, the method as coded, any X-measurable partition
with blocks ≤ 16. Assume (T1-R), (FL-R), (V-R), (L-R), (D-R). Then, under the joint law of (X, ε): [SAND(Q)],
[TL(Q)], [NA(Q)], [POST], hence all conclusions of (C0).

**Bridge lemmas** (each delivers one interface property):

| id | statement | status of the engine | new in this ticket |
|---|---|---|---|
| (B1) | (V), (L-gain), (FL-16) ⇒ (V_b), (L_b), (G3a) for every partition with blocks ≤ 16 | — | new (elementary) |
| (B2) SAND-F | Setting F: ‖μ‖² ≤ Mn, p ≤ n^A, (G3a) (the within-block part of (FL_b)), (V_b), (L_b), (L-feas), log\|Q\| = o(log n) ⇒ [SAND(Q)] | GROW L3 (\|Q\| ≤ C log n, σ²-normalised leakage; R02 VERIFIED) | extension to log\|Q\| = o(log n); τ²_U-normalised leakage (Lemma B2τ, `lemmas/L1b_rss.md`) [P2] |
| (B3) TL-F | Setting F: ‖μ‖² ≤ Mn, (FL-Q), \|Q\| ≤ (log n)^κ, \|Q\| ≤ K, (BM-Q) ⇒ [TL(Q)] (under \|Q\| ≤ C log n, BM-∞ suffices) | GROW L2.1; LOC2 L0′ (fixed θ_lo) | BM-Q version |
| (B4) NA-χ | Setting F, ‖μ‖² ≤ Mn, p ≤ n^A, deterministic Q ⊇ S₀ with \|Q\| ≤ K: (N-χ), (FL-Q) ⇒ [NA(Q)] | GROW L2.2–L2.3(a) | none |
| (B5) NA-F | Setting F, ‖μ‖² ≤ Mn, p ≤ n^A, deterministic Q ⊇ S₀ with \|Q\| ≤ K and \|Q\| ≤ (log n)^κ: (N-D)(i), (FL-Q) ⇒ [NA(Q)]; (N-loc) ⇒ (N-D)(i) | GROW L2.3(b) is the case ρ_n = 0, \|Q\| ≤ C log n; score conversion LOC2 L0′ | **new lemma** |
| (B6) POST-F | (T1-F) ⇒ [POST] | T03♯ | none |
| (B7) SAND-R | Setting R: (FL-R), (V-R), (L-R) ⇒ [SAND(Q)], any X-measurable partition with blocks ≤ 16 | GROW L6.2–L6.5 → APP L3.2–L3.5 → LOC2 L4 A.1–A.4 → UNI L2 §3–§6 (proved there for metric-local Σ) | **new abstraction** (the geometric inputs replaced by (L-R)): `lemmas/L3_SANDR.md`; rate r_n: `lemmas/L3b_rate.md` [P3a] |
| (B8a) NA-R | Setting R, deterministic Q ⊇ S₀, \|Q\| ≤ (log n)^κ, \|Q\| ≤ K: (D-R), floor on Q ∪ {l} ⇒ [NA(Q)]; (D-loc) ⇒ (D-R) | LOC2 L2 (NA-R), L1 | (D-loc) ⇒ (R1)–(R3) (elementary) |
| (B8b) TL-R | Setting R (fixed θ_lo > 0), same Q: floor on Q ∪ {l} ⇒ [TL(Q)] ((D-R) not needed) | LOC2 L1 (L0′, L1.2); GROW L2.1 | none |
| (B9) POST-R | (T1-R) ⇒ [POST] | APP L1_POST(b) | none |
| (B10) | UNI-0's class ⇒ (T1-R), (FL-R), (V-R), (L-R), (D-R) with UNI-0's Q; LOC-BF's class likewise (the fixed exponent κ may be enlarged to absorb constants, \|H_l\| and \|Q\|) | UNI L2 §2–§7; LOC2 L4 Part B | bookkeeping |

Input map (many-to-many) [R01-4]: (T1) → B6/B9, and its components also feed other bridges — the energy bound
‖μ‖² ≤ Mn and p ≤ n^A of (T1-F) → B2, B3, B4, B5; BM-∞ of (T1-F) → B3 under (N-χ) (it gives BM-Q there); in Setting R the
energy bound and the fixed beta-min come from the setting itself [C1-A2]; (FL-16)/(FL-R, small sets) → B1, B2, B7; (FL-Q)/(FL-R, Q ∪ {l}) → B3, B4,
B5, B8a, B8b; (V)/(V-R) → B1, B2, B7; (L-gain) → B1, B2, B7; (L-feas) → B2, B7 (ladder end, feasibility of adding a truth) and, through |Q| ≤ K, B3, B4,
B5, B8a, B8b and RM-0 [C1-B3]; (L-size) → B2, B3, B5, B7, B8; (L-loc-R) → B7;
(N-χ) → B4 (and with BM-∞ it gives BM-Q); (N-D)(i) → B5; (BM-Q) → B3; (D-R) → B8a. (B7) is a proof obligation of this
ticket, not an inherited result outside the example classes; its proof must treat the random sample scales as the
source does — uniformly over deterministic response coefficients b_k with |b_k| ≤ 2θ_hi, then evaluated at
b_k = θ*_k/t_k (UNI `lemmas/L2_k0.md:100-105`), never by asserting a law conditional on a sample-scale or
sample-covariance event [R01-Q6]; the spherical-tail step conditions on (W_D, ε), which is legitimate because the
innovation is independent of it (R04 F1). (B7) needs (FL-R) only on sets of size ≤ 16 + s₀ (R04 F3).

**(C3) Lemma E4 (closes premise e4)** [R01-1, R01-2]. For the routine `start_mode` of CORE `cpp/v3_start.h` as on main,
assume N3 (H1) (the `Start` object encodes the ordered actual partition, the tables log r_b, the prior and K),
**strengthened** to require `st.blk` and `st.pos` to be the inverse maps of the ordered actual blocks on every branch
and a valid `D.p` (as in ENG `lemmas/TDP_E.md:28-36`), (H2) (EX-A for the routine's arithmetic) and (H4) (execution
bounds for both the enumeration and the fallback), with enumeration cap 10⁶ as in the integration call (any cap ≥ 1
when `tie_dp` is false, any cap ≥ 2 when it is true; the routine rejects `tie_dp = true` with cap < 2 and nothing is
claimed on rejected inputs). Then on every accepted input and for both values of `tie_dp` the returned set is a
maximiser of γ₀ on Ω — with or without ties, truncated or not. Only this maximiser property is claimed (no lex rule).
Integration: in CORE `cpp/v3_core.cpp:469-476` the LS0 centre is that returned set, unmodified; it is emitted (scored);
under the configuration of §1 (`ls0`, `ls0_ell = ℓ_n`, `ls0_cap = "ell_n_plus_mode"`; option parsing
CORE `cpp/v3_core.cpp:394-404`, gate CORE `cpp/v3_core.cpp:465`, cap CORE `cpp/v3_core.cpp:473`) the cap is ℓ_n + |centre|. Hence [E4] holds on every completed SMC output run in that
configuration. EX-A is an idealisation: in binary64 the statement is N3 (e) / PACK UM-FP, not this lemma.

**(C4) Examples table** (families verifying the assumptions; each with its signal condition) — `lemmas/L7_examples.md`
§7.4, verifications in §7.1–§7.2 [R08-21]. Fixed design: exact-Gram AR(1) (separation); orthogonal-type designs with no leakage.
Gaussian rows: UNI-0 (banded, AR, spatial, graph-local, bounded blocks; PTV); LOC-BF (growing one-factor groups, at
most one truth per group). Results whose own proofs do not go through (V) + (L) at polylogarithmic size and are related
only through (C0) [R06-6, 7]: polynomial decay α > 17/2 (LOC2 L6: polynomial-size relevance envelope); one common factor
with limsup log p/log n < α₀(κ̄) (UNI-1: full lattice Q = [p]) and the family-specific exact compound-symmetry results
(FAC-A/B/X). With (V) failing by construction: masked hubs (PXN), GEN's masked cases.

**(C5) Sharpness record** — `SHARPNESS.md` [R01-5]. It distinguishes proof-route sharpness, uniform class sharpness
and necessity for a particular design/Q, and records for each item what is proved, what is observed and what is open:
(i) "15" is the worst-case conditioning size permitted by the coded block cap (16 − 1); no necessity for
reported-model consistency is implied; (ii) η_A is the sufficient threshold delivered by the present uniform sandwich
argument; whether a worst-case converse holds above it is a question (a converse is claimed only if proved; otherwise
status open); (iii) the size of Q: polylogarithmic is what the engines carry, not a necessity; route obstructions
(APP L5 VN concerns the start/sandwich route, not the full method) are kept distinct from impossibility; (iv) the
status of (N).

## 5. Dependencies (statuses verbatim)

GROW "PROVED-CHECKED" (L0, L1 R03 VERIFIED; L2 R03 VERIFIED-WITH-AMENDMENTS; L3 R02 VERIFIED; L4 R04
VERIFIED-WITH-AMENDMENTS; L6 R07 VERIFIED / R06 VERIFIED-WITH-AMENDMENTS); W2-LOC2 "PROVED-CHECKED" (lemma statuses
"PROVED (by this seat, unchecked)", checks R02/R03/R04 VERIFIED-WITH-AMENDMENTS); W2-UNI UNI-0 and R1–R5
"PROVED-CHECKED" (council Astra 9.0 / Opus 8.9); W2-APP "PROVED-CHECKED"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF
VERIFIED (A-REV2)"; M5(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; [OP] "PROVED (by this seat,
unchecked)" inside GEN "PROVED-CHECKED"; DLV Corollary D′ / pathwise Claim: "PROVED (by this seat); R04 VERIFIED-WITH-AMENDMENTS" (DLV
`lemmas/L4_delivery.md:3-4`), report row "PROVED-CHECKED (pathwise argument supplied by R04; council round 2)" [C1-B1]
(not load-bearing: `lemmas/L0_core.md` re-proves the inclusion with E4); N3 "PROVED-CHECKED" (Theorem N3-code
(a)–(f)); ENG Lemma TDP-E "PROVED (by this seat, unchecked)".

## 6. Not claimed

* **(V) + (L) alone with |Q| ≤ C log n for arbitrary C** (fixed design), or with polylogarithmic Q and no (N-D)/(D-R).
  The proof route needs the whole-lattice event NA(𝓛); (N-χ) gives it for |Q ∖ S₀| ≤ (1 − δ₀) log n, and beyond that a
  condition on the design's direction complexity is used. Whether (N) can be dropped is open (SHARPNESS.md).
* Non-Gaussian rows; growing s₀; θ*_min → 0 in Form R; masked truths ((V) fails); leakage sets beyond polylogarithmic
  size; delivery P(U_n) → 0; finite-n statements; any change to shipped components.
* A binary64 theorem (everything is under EX-A); runs outside the configuration of §1 (`ls0 = FALSE`, or
  `ls0_cap = "ell_n"` — except the (N-χ) sub-case of (C1), where the old cap is covered by the remark there [C2-A2]);
  necessity of (V), of the polylogarithmic size, of (N) or of η_A.
* Form R is not obtained from Form F by conditioning on X: under Gaussian rows the off-block signal acts as extra
  Gaussian noise and the sample version of (L-gain) with the constant η < η_A is not expected to hold in general
  (an order-of-magnitude heuristic, not a proof: ASSUMPTION_MAP) [C1-B6].
