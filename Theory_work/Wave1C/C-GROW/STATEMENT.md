# C-GROW — STATEMENT (target statement)

Ticket C-GROW, Theory Wave 1C. Lead: Claude Opus 5.5.
Status of this file: **v2.5 — final; council round 1 passed (R09 9.2, R10 9.0)** (v2.5 = council R10 F1 wording: fixed-p caveat; log convention. v2.4 = R08 sweep fixes:
noise model of (C5)(c), minimal (C2) hypotheses, definitions, evidence wording; no claim changed).
Previous: **v2.3** (v2 LOCKED; v2.1 = R04 amendment 2, piecewise AR(1) relevance set in (C5)(a); v2.2 =
R05 wording: S5 certificate and envelope language; v2.3 = **extension** (C5)(c), random-design AR(1), added after
the parallel proof L6 passed two independent checks (R06, R07); all logged and flagged in REPORT). (v1 reviewed by R01, Codex gpt-6.1-sol high, LOCK-WITH-CHANGES; all nine required
changes applied, see `reviews/R01_statement_lock_sol.md` and `reviews/R01_disposition.md`). Later changes are logged
in LOG.md and flagged in REPORT.md.

Abbreviations: SoP = `Theory_work/State_of_Project/sections/`; GEN = `Theory_work/Wave1/W1-GEN/` (Theorem GEN,
"PROVED-CHECKED", council Sol 9.0 / Opus 8.9, GEN/REPORT.md); T37R = `Theory_work/Old_Projects/New_BVS_Headquarters/
branch_snapshots/W1-T37R/PROOF.md`.

## 0. Target, scope and diagnosis

HQ target: reported-HPM consistency P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 (no delivery claim) for design classes whose relevance set
grows with n, covering study scenarios S2 (AR(1), ρ = 0.5) and S5 (compound symmetry: within-group 0.7, between 0.3),
fixed s₀, p ≤ n^A. Route: M5(0) (SoP `04_theory.tex:489`, T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED*
(A-REV5))"): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n, D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) (potential-run notation); S-T/T03♯
gives E₀[1 − π(S₀)] → 0; the new content is D_n → 0 through LS0 (operational closure [OP], GEN/lemmas/L5_assembly.md).

**Scope actually targeted (after R01).** (i) A general growing-relevance theorem (fixed designs; relevance set of
size O(log n)); (ii) an **exact-Gram AR(1)** instance (S2's population covariance; relevance set growing like log n);
(iii) a **fixed-p** illustration on S5's population covariance with a diagnostic layout. (iv) (v2.3) the **iid-row AR(1)** design of the study
generator (`Scripts/Data_generators/gen_dev_data.R:53-61`), p ≤ n^A including p ≫ n, under the separation condition
(which the generator's S2 layouts satisfy) — claim (C5)(c). Random-row S5 is not covered (frontier, (C6)).

Diagnosis (numerics/D1_summary.md, D2_summary.md, D3_summary.md (current individual summaries; the aggregate
SUMMARY_DIAG.md may be an earlier snapshot); Python component diagnostics on the ported score/blocks/start mode —
not the production code — with the port's numerical tie tolerances (10⁻¹⁰ linkage, 10⁻¹² start DP, enumeration cap
2·10⁴; zero start truncations observed); iid rows as in the generator, p = 100, s₀ = 4 diagnostic layout,
n = 200…12800, 20 seeds/row; observations, not proofs): (i) the finite MC3 diagnostics are consistent with posterior
concentration on S₀ (median fraction of MC3 time at S₀ 0.936–0.951 at n = 12800, where S₀ is the best visited model
in every run; 19/20 per row at n = 200); (ii) S2:
from n = 800 on the start mode contains S₀ in every run, |S̃₀ ∖ S₀| ≤ 7, the uncapped LS0 path deletes the extras one
at a time in every run, and the production cap suffices (S₀ scored 120/120 for n ≥ 800; 160/160 including n = 200)
— a **proof gap**; (iii) S5: S̃₀ ⊇ S₀ in
every run from n = 3200 on (not always at n = 800), |S̃₀ ∖ S₀| grows (median 16–37 at n = 3200–12800); the uncapped
path reaches S₀ with at most one move more than |S̃₀ Δ S₀| at p = 100 (occasional swaps; up to three more at
p = 400); with the production cap
ℓ_n = ⌈log₂(n + p + 1)⌉, S₀ is scored in 2/40 and 0/40 runs at n = 3200 and 12800, with the cap ℓ_n + |S̃₀| in 80/80 —
a **method gap (the LS0 cap)** at practical n, closable by an LS0 parameter (LS0 is not shipped; Wave-1C protocol
"Method-side changes"). This is a statement about LS0, not about the full method's D_n (the production core without
LS0 is examined in D4, numerics/D4_summary.md: actual R production core, S₀ the reported HPM in all 25 fits on
data seeds 0–4, S2/S5, n ≤ 3200).

## 1. Setting (self-contained; as GEN/STATEMENT.md §1)

* **D0** (SoP `04_theory.tex:69-74`): shipped g = n score, a₀ = b₀ = 0.01: with G_A = X_AᵀX_A, z_A = X_Aᵀy,
  H_A = (n + 1)G_A + I, Q_A = yᵀy − n z_AᵀH_A⁻¹z_A, ν = 0.01 + n/2,
  log m(A) = log c_n − ½[log det H_A − log det(G_A + I)] − ν log(0.02 + Q_A); capped BB(1,p) prior
  w(k) = 1/(2C(2p − 1, k)) (exact ratio w(k + 1)/w(k) = (k + 1)/(2p − 1 − k)); K = min(p, ⌊n/2⌋),
  Ω = {S : |S| ≤ K}; F(S) := log w(|S|) + log m(S); tables r_b(U) = m(U)/m(∅); start γ₀ ∝ w(|S|)∏_b r_b(S ∩ C_b) on
  Ω; start mode S̃₀ = argmax_Ω γ₀ with the size-then-lex tie rule.
* **G**: fixed raw design X^r (n × p, nonconstant columns), y^r = α1 + X^rβ + ε, ε ~ N_n(0, σ²I), σ² > 0 fixed;
  C := I − 11ᵀ/n, D_x := diag of the raw columns' sample standard deviations; X = CX^rD_x⁻¹ (centred, ‖x_j‖² = n − 1); the response is centred (Y = Cy^r) and scaled to yᵀy = n − 1 inside the
  score; μ := CX^rβ = Xθ*, θ* := D_xβ, S₀ := supp β, s₀ := |S₀| ≥ 1 fixed, p = p_n ≤ n^A (A ≥ 1 fixed).
* **Logarithms** are natural unless written log₂ (v2.5).
* **Notation.** P_T := orthogonal projector onto span(X_T) (P_∅ := 0); π(S) := w(|S|)m(S)/Σ_{A∈Ω}w(|A|)m(A) (the
  prior's normaliser cancels in every comparison); Λ_T := ‖(I − P_T)μ‖², Δ_T := Λ_T/(n − 1), R̂_T := X_TᵀX_T/(n − 1), θ*_min := min_{S₀}|θ*_j|;
  for l ∉ T with (I − P_T)x_l ≠ 0: u_{T,l} := (I − P_T)x_l/‖(I − P_T)x_l‖, δ_{T,l} := u_{T,l}ᵀμ,
  Z_{T,l} := u_{T,l}ᵀε/σ (standard normal for fixed (T, l)).
* **Blocks** C₁, …, C_J: the method's actual partition (complete linkage on 1 − |r̂|, top-down cut at
  B = min(⌊√n⌋, ⌊√p⌋, 16), next-fit packing, tie rules as coded; SoP `02_method.tex:187-211`); a deterministic
  function of X; |C_b| ≤ B ≤ 16. All block conditions below are required **on this partition**.
* **Method:** v3.1 with LS0 (SoP `02_method.tex:490-506`); local search M §6.10 (SoP `02_method.tex:463-467`): a
  *move* is a strict improvement to the best scanned neighbour (exact ties: lexicographically smallest set); every
  scanned neighbour is scored; at most ℓ moves, then one further scan; "certified endpoint" = the search ends at a
  scanned centre whose completed scan finds no strict improvement (the public flag `local_certified` refers to the
  finally reported HPM, SoP `02_method.tex:505-506`, and is not claimed).
* **Implementation premises** (named, not proved; SoP `04_theory.tex:84`): EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, e4
  (emitted LS0 centre = the prescribed start-mode maximiser; N3 OPEN), complete scans; for R′ > 4 IND-T and the
  extra search from c₄. 𝒪 = output event, U_n := 𝒪ᶜ (no output).
* **Method requirement MR1 (LS0 cap; LS0 is not shipped).** LS0 runs with move cap ℓ^{LS0} := ℓ_n + |S̃₀| (all other
  LS0 rules unchanged). Under (G4-χ) the production cap ℓ_n already suffices (claim (C4)(b)). MR1 is recorded in
  METHOD_REQUIREMENTS.md.

Lattice notation: for a deterministic 𝒫 = 𝒫_n ⊆ [p] ∖ S₀: Q := S₀ ∪ 𝒫, 𝓛 := {T : S₀ ⊆ T ⊆ Q} (|𝓛| = 2^{|𝒫|}).

## 2. Hypotheses

* **(H0)** = the hypotheses of S-T/T03♯ (SoP `04_theory.tex` TH09 card), with fixed constants A ≥ 1, M, φ₀ ∈ (0, 1],
  g₀ > 0: R1 (G; fixed s₀; p ≤ n^A; s₀ ≤ K eventually); R (‖μ‖² ≤ Mn; λ_min(R̂_{S₀}) ≥ φ₀²); SE_λ(j₀),
  j₀ := ⌈(2A + 1)s₀⌉ + 1 (λ_min(R̂_{S₀∪J}) ≥ φ₀² for |J| ≤ j₀); SE_w(m♯_n; g₀) (λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ g₀ for
  |J| ≤ m♯_n, m♯_n := min{m ≥ s₀ : R_m ≤ n^{−(s₀+2)/2}}, R_m := Σ_{k=max(m+1,0)}^{K} C(p,k)w(k)/w(s₀)); BM-∞
  (θ*²_min nφ₀²/(σ² log n) → ∞).
* **(G1) growing relevance set.** Deterministic 𝒫_n ⊆ [p] ∖ S₀ with |Q| ≤ C_Q log n (C_Q fixed), |Q| ≤ K, and
  **either** Q = [p] **or** K ≥ 2|Q| + 32s₀ + 1, for n ≥ n₀ (this implies min(p, |Q| + 1) ≤ K).
* **(G2) Gram floor on the lattice.** λ_min(R̂_{Q∪{l}}) ≥ φ₀² for every l ∈ [p].
* **(G3) centre conditions (on the actual blocks).** (G3a) within-block SE: λ_min(R̂_T) ≥ φ₀² for every nonempty
  T ⊆ C_b, every b. (G3b) TV: for a deterministic M_n → ∞, every j ∈ S₀ and every U ⊆ C_{b(j)} ∖ {j}:
  δ²_{U,j} ≥ M_n log n. (G3c) NEG(η): for a fixed η ∈ [0, η_A), η_A := (√(2A + 1) − √(2A))², every l ∉ Q and every
  U with S₀ ∩ C_{b(l)} ⊆ U ⊆ C_{b(l)} ∖ {l}: δ²_{U,l} ≤ ησ² log n.
* **(G4)** either **(G4-χ)** |𝒫_n| ≤ (1 − δ₀) log n for a fixed δ₀ ∈ (0, 1) (no further correlation assumption), or
  **(G4-dir)** the set of add directions 𝒰_n := {u_{T,l} : T ∈ 𝓛, l ∉ T} satisfies |𝒰_n| ≤ pN_n with
  log N_n = o(log n).

## 3. Claims

* **(C1) Deterministic lattice descent.** Events NA(𝓛) := {F(T ∪ {l}) < F(T) for all T ∈ 𝓛 with |T| < K and all
  l ∉ T} and TL(𝓛) := {every feasible neighbour A of every T ∈ 𝓛 with S₀ ⊄ A has F(A) < F(T)}. On NA ∩ TL, from
  every centre C ∈ 𝓛 the uncapped §6.10 greedy path deletes one element of C ∖ S₀ per move, stays in 𝓛, reaches S₀
  after exactly |C ∖ S₀| moves and stops there; the capped search scores S₀ if ℓ ≥ |C ∖ S₀| − 1 and has certified
  endpoint S₀ without `local_limit` if ℓ ≥ |C ∖ S₀|.
* **(C2) Descent events.** Under G, ‖μ‖² ≤ Mn, p ≤ n^A, |Q| ≤ C_Q log n, |Q| ≤ K, (G2) and BM-∞: P(TL(𝓛)) → 1. Under
  the same without BM-∞, plus (G4-χ) or (G4-dir): P(NA(𝓛)) → 1. ((H0) and (G1) imply these lists; R08 item 9.) (Uniform null-add expansion with the exact BB ratio: 2[F(T ∪ {l}) − F(T)] ≤ Z²_{T,l} − log(n + 1)
  − 2 log((2p − 1 − k)/(k + 1)) + O(1) uniformly on a high-probability event; separate arguments for (G4-χ)
  (Pythagorean bound with one common χ²) and (G4-dir) (direction count).)
* **(C3) Centre sandwich.** Under ‖μ‖² ≤ Mn, p ≤ n^A, (G1), (G3): P(S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω)
  → 1. Explicit proof obligation: a **global size ladder** (all maximisers simultaneously, including near-saturated
  ones with |S̃| close to K), then truth inclusion (TV) and exclusion of outside variables (NEG).
* **(C4) Main theorem (Theorem GROW).** Under (H0), (G1)–(G4), the premises of §1 and MR1:
  D_n ≤ P(sandwich fails) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0; hence P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and
  liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). (b) Under (G4-χ) the same holds with the production cap ℓ_n in place
  of MR1. No delivery claim.
* **(C5) Instances.**
  (a) **AR(1), exact Gram.** XᵀX = (n − 1)Σ, Σ_ij = ρ^{|i−j|}, fixed ρ ∈ (−1, 1) ∖ {0}, any p = p_n ≤ n − 1 (fixed or
  growing), fixed s₀ and nonzero θ*, σ² fixed, separation Σ_{k∈S₀∖{j}}|θ*_k||ρ|^{|j−k|} ≤ ½|θ*_j|(1 − ρ²)/(1 + ρ²)
  for every j ∈ S₀; any block partition with blocks of size ≤ 16. Then, with the explicit radius
  d_n := ⌈log n/(2 log(1/|ρ|))⌉, 𝒫⁰_n := {l ∉ S₀ : min_{k∈S₀}|l − k| ≤ d_n}, Q⁰_n := S₀ ∪ 𝒫⁰_n, and 𝒫_n := 𝒫⁰_n
  if Q⁰_n = [p] or p ≥ 2|Q⁰_n| + 32s₀ + 1, else 𝒫_n := [p] ∖ S₀ (v2.1), the hypotheses (H0), (G1)–(G3), (G4-dir) hold and (C4) applies (with MR1). |Q| ≤
  4s₀d_n + 34s₀ + 1 = O(log n) and |𝒫_n| ≥ min(d_n, p − s₀) − s₀, so 𝒫_n grows like log n whenever p_n ≥ d_n + 2s₀ —
  a growing relevance **envelope** (what is proved is S₀ ⊆ S̃₀ ⊆ Q; it is not claimed that the start mode itself
  has an unbounded number of extras on this instance).
  (b) **S5 population covariance, fixed p (illustration).** Exact Gram with Σ = 0.3·11ᵀ + 0.4·H + 0.3I (H = block
  diagonal of 1₅1₅ᵀ; within 0.7, between 0.3), p = 100, diagnostic layout s₀ = 4 (truth indices and coefficients
  c·(1.4, −1.0, 1.8, −1.2), c ∈ {0.5, 1}, exactly as in numerics/d_common.py and GEN/numerics/study_common.py at
  p = 100, s₀ = 4, step 5 — **not** the production generator's declared truth, which exists only at p ∈ {30, 500,
  1000}), σ² = 1, coded partition. With 𝒫 = [p] ∖ S₀ (Q = [p]): (H0), (G1), (G2), (G3a), (G3c) (vacuous) and (G4-χ)
  hold for n large; (G3b) holds iff the finite quantity τ₀ (minimal partial signal over truths and within-block
  conditioning sets, independent of n) is > 0; τ₀ = 4/25 (c = 1), 1/25 (c = 0.5) by an exact rational certificate
  written out in lemmas/L5_instances.md (b) (v2.2 wording, after R05); then (C4) applies. **Caveat (v2.5, R10 F1):**
  for fixed p the production run enumerates all models (SoP `02_method.tex:167`) from n ≳ 2.5·10²⁷ on, before the
  (G4-χ) onset, so there S₀ is scored by enumeration and T03♯ alone gives the conclusion; (b) shows only that the
  hypotheses hold, not that LS0 is the operative mechanism. The same applies to fixed-p sequences in (a) and (c);
  Theorem GROW adds content beyond T03♯ + enumeration in the regime p ≫ log n.
* **(C5)(c) (v2.3 extension) AR(1), iid rows (study S2).** Raw rows iid N(0, Σ), Σ_ij = ρ^{|i−j|}, fixed
  ρ ∈ (−1, 1) ∖ {0}, columns centred and standardized, p ≤ n^A (any fixed A ≥ 1; p ≫ n allowed), fixed s₀ and fixed
  nonzero θ* on the standardized scale: Y = Xθ* + Cε with ε ~ N(0, σ²I_n) **independent of the raw design** (as in
  the generator), and y = Y/(‖Y‖/√(n − 1)) inside the score (R08 item 2), σ² fixed, separation as in (a); any
  X-measurable partition with blocks of size ≤ 16 (in particular the coded one); relevance set as in (a). Then under
  the joint law of (X, ε): P(S₀ ⊆ S̃ ⊆ Q for every maximiser) → 1, P(NA(𝓛)) → 1, P(TL(𝓛)) → 1, and with the
  premises of §1 and MR1, D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n). The
  generator's S2 layouts (p = 500, 1000; 14 truths; ρ = 0.5) satisfy separation for every signal scale c > 0, so the
  result covers asymptotic sequences extending them (not the generator's fixed n = 200). Proof: lemmas/L6 (the
  fixed-design hypotheses NEG and (G4-dir) are NOT verified; the three events are proved directly under the joint
  law).
* **(C6) Frontier (with evidence, not proved).** iid-row S5 / factor designs; factor designs with p → ∞ faster than
  log n (observed, not proved: at c = 1, n = 3200 the median start size is 23, 43, 74 at p = 100, 200, 400; a growth
  law for |S̃₀| is a conjecture, and |S̃₀| ≤ K ≤ n/2 always; with MR1, LS0 scored S₀ in 47/47 S5 p = 400 runs and
  reached it as a search state in 45/47 (all 27 runs at n ≥ 800); numerics/D2_summary.md, D3_summary.md — component
  observations, not a guarantee); finite-n onsets (all statements are asymptotic; violations of the asymptotic events
  occur at tested finite sizes: numerics/SUMMARY_FALSIF.md incl. S5 NA failures in 10/20 runs at n = 12800 despite
  successful MR1 searches; G1_summary.md for iid AR(1) at n ≤ 800; successful LS0 paths are not NA validation).

## 4. Not claimed

Delivery P(𝒪) → 1 (P(U_n) → 0); finite-n statements; masked truths at block level (TV excludes them; GEN covers
masking with a bounded 𝒱); anything about v3/v3.1 without LS0; changes to shipped components; random-design S5.

## 5. Dependencies (statuses verbatim)

M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; S-T/T03♯ "PROVED; SF VERIFIED (W2-VT03R);
XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" in GEN L5 (inside Theorem GEN "PROVED-CHECKED");
GEN L1 (score expansion; GEN R02 VERIFIED-WITH-AMENDMENTS) re-proved for sets of size O(log n) (lemmas/L0, with the
χ²-rank factor and event thresholds adjusted); T37R Lemma 2(b) ("PROVED") as the model of (C1).
