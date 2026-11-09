# W2-LOC2 — STATEMENT (polylogarithmic relevance sets: d ≥ 2 local designs, middle-regime blocks, polynomial decay)

Ticket W2-LOC2, Theory Wave 2. Lead: Claude Opus 5.5. Status of this file: **v1.2** (v1.1 LOCKED 2026-11-09 after R01; v1.2 fills the (D3) stretch slot, logged; post-council
editorial items C1-Opus 1–3, 8 applied) — v1.1 LOCKED after R01 (Codex gpt-6.1-sol high, LOCK-WITH-CHANGES; all six required
changes applied, `reviews/R01_disposition.md`).
Protocol: `Theory_work/Wave2/PROTOCOL.md` (extends Wave1C and Wave1 protocols). All results asymptotic (n → ∞).

Abbreviations. APP = `Theory_work/Wave2/W2-APP/`; GROW = `Theory_work/Wave1C/C-GROW/`; GEN = `Theory_work/Wave1/W1-GEN/`;
FIN = `Theory_work/Wave1C/FINAL/sections/`; FACA = `Theory_work/Wave2/W2-FAC-A/`. Method = production core v3.1 as merged on
main at 4676af6 (LS0 from the start mode, move cap ℓ_n + |S̃₀|; tie-aware start-mode DP; tier-1 calibration fallback).
**No method change is requested**: every claim uses the shipped cap ℓ_n + |S̃₀|, which accommodates start modes with
|S̃₀ ∖ S₀| ≫ log n; the former/smaller cap ℓ_n = O(log n) cannot complete such a deletion path (deterministic fact,
GROW L1.2). Rigorous example of such start modes: APP L5_VN (V2) (growing equicorrelated truth groups with
g_n/log n → ∞, contained in (D2)). Observations only (not rigorous): component-port runs for d = 2
(numerics/D1_SUMMARY.md) [R01-5, C1-Opus-3].

## 1. Setting (random design; as APP STATEMENT §1 / APP L3_LOC §L3.0)

Raw rows iid N(m, Σ_n) (n × p, p = p_n ≤ n^A, A ≥ 1 fixed, p ≫ n allowed), Σ_n unit-diagonal (population correlation
matrix; WLOG by scale invariance), m arbitrary (WLOG m = 0, APP L3.0 zero-mean reduction). X = column-centred,
sample-standardised raw design. Y = Xθ* + Cε, θ* fixed on S₀ (|S₀| = s₀ ≥ 1 fixed, as in GROW [C1-Opus-8]; positions may move with n;
|θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞)), ε ~ N(0, σ²I_n) independent of the raw design, σ² > 0 fixed; response scaled inside
the score. Implementation premises as in APP L3.0 / FIN §1.4: EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans,
IND-T and the c₄ search when R′ > 4, and "the emitted LS0 centre is some maximiser of γ₀" (named, not proved). For
delivery (claim (E)) the premises and allocation of FIN s6 Proposition F / F-GROW / FACA L7 (Proposition F-FAC), CAL not assumed.
Partition: any X-measurable partition with blocks of size ≤ 16 (in particular the coded one); it need not respect any
covariance groups. Model-size cap K_n := min(p, ⌊n/2⌋) (SoP `Theory_work/State_of_Project/sections/02_method.tex:618`); decay-envelope constants are written K_dec
[R01-3].

Events (GROW L1, L3, L4): Sand_n := {S₀ ⊆ S̃ ⊆ Q for every maximiser S̃ of γ₀ on Ω}; NA(𝓛), TL(𝓛) for
𝓛 := {T : S₀ ⊆ T ⊆ Q}; D_n, 𝒪, Ŝ⁺, U_n as in GROW L4 / FIN s5.

## 2. Claims

**(A) Lemma L0′ (quasi-polynomial toolkit).** The event bounds and score/contrast conclusions of GEN L1 / GROW L0 hold,
with the inherited premises (∅ ∈ 𝔉, Gram floor, energy ‖μ‖² ≤ Mn, 𝒱𝒱 ⊇ residuals and contrasts; for random design the
families are fixed after conditioning on the raw design and the failure bounds are uniform) [R01-6], for deterministic families 𝔉_n with
|A| ≤ J_n (A ∈ 𝔉_n), log|𝔉_n| ≤ (log n)^{κ}, log|𝒱𝒱_n| ≤ (log n)^{κ}, J_n ≤ (log n)^{κ} (κ ≥ 1 fixed, WLOG — larger envelopes only weaken the hypothesis; editorial correction R05-1), with
t_n := 4(log|𝔉_n| + 2 log n + J_n), h_n := √(2(log|𝒱𝒱_n| + log n)); hence GROW L2.0–L2.2 (TL and the NA reduction)
hold for |Q| ≤ (log n)^{κ}; here t_n + h_n² = O((log n)^κ) = o(n), J_n/n → 0, (t_n + h_n²)log n/n → 0, and TL uses the fixed
beta-min θ_lo > 0 of §1 (no general BM-∞ version is claimed). File `lemmas/L1_toolkit.md`.

**(B) Key lemma NA-R (no-addition via references and atoms).** Random design as §1; deterministic Q ⊇ S₀ with
q := |Q| ≤ (log n)^{κ}, q ≤ K_n; population floor λ_min(Σ_{n,Q∪{l}}) ≥ c for all l. For each n fix a centred jointly
Gaussian row law on ℝ^{p+p′} extending N(0, Σ_n) (first p coordinates = the raw row); the n rows (W, Ξ) are sampled iid
from it and the whole extension is independent of the entire noise vector ε. Frame members and atoms are deterministic
linear functionals φ of this row (fixed linear maps, not fitted to data), evaluated rowwise to n-vectors 𝒲φ and centred
by C for sample comparisons; coefficients in r and λ, the bound L_n and η_n are deterministic (they may depend on n, T, l
and the population law); no independence among frame members, atoms or W is assumed [R01-2]. Suppose that for every (T, l), T ∈ 𝓛, l ∉ T, the
population residual e_{T,l} := W_l − W_Tβ_{T,l} (β_{T,l} := Σ_TT⁻¹Σ_{Tl}) splits as
e_{T,l} = r_{T,l} − Σ_{a∈𝒜_n} λ_{T,l,a} 𝒲a (𝒲a the rowwise evaluation of the functional a) [R07-13], where
 (R1) r_{T,l} is a linear combination of the ≤ m₀ (fixed) vectors of a reference frame ι(T, l) taken from a
      deterministic family of N_n frames of linear functionals of the (W, Ξ)-row, log N_n ≤ log p + o(log n);
 (R2) 𝒜_n is a deterministic set of linear functionals with row variance ≤ 1, and L_n² log(|𝒜_n| + 1) = o(log n),
      L_n := max_{T,l} ‖λ_{T,l}‖₁;
 (R3) Var(r_{T,l}) ≤ (1 + η_n)Var(e_{T,l}) with η_n → 0 (row variances; uniform over (T, l)).
Then, with Z_{T,l} := u_{T,l}ᵀε/σ from the SAMPLE normalised residual u_{T,l} of x_l on X_T (GROW L2.0) and
c_n = log(n + 1) + 2 log p − 2 log(q + 1) − 4κ_E − 2 (κ_E of the common score expansion), P(max_{T∈𝓛, l∉T} Z²_{T,l} ≤ c_n) → 1
(vacuous if the pair family is empty), hence P(NA(𝓛)) → 1 (with (A)). File `lemmas/L2_NAR.md`.

**(C) Theorem PLR (polylog relevance assembly)** [R01-1, split]. (C-i) If P(Sand_n) → 1 for a deterministic Q with
|Q| ≤ (log n)^{κ} satisfying the feasibility dichotomy (Q = [p] or K_n ≥ 2|Q| + 32s₀ + 1), the floor of (B), and (R1)–(R3),
then P(NA(𝓛)) → 1, P(TL(𝓛)) → 1 and D_n → 0 (shipped cap). (C-ii) If in addition APP L1_POST's LSF holds (sufficient: a
global population floor λ_min(Σ_n) ≥ c, which (D1) and (D2) supply), then 1 − π(S₀) = O_P(√(log n/n)),
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). File `lemmas/L5_assembly.md`.

**(D1) Theorem LOC-d (main target (a)).** Fixed d ≥ 1. (Σ) LOC_d(c, C, K, a): Σ_n unit-diagonal with spectrum in
[c, C]; sites x_n : [p] → ℝ^d with ‖x_n(j) − x_n(k)‖ ≥ 1 for j ≠ k (Euclidean norm); either |Σ_jk| ≤ K_dec e^{−a‖x(j)−x(k)‖}
(j ≠ k) or the same for Θ = Σ⁻¹; constants fixed, sites may vary with n (grids ℤ^d ∩ box, irregular sites with
minimum separation; increasing-domain asymptotics). (θ) PTV(a₀) as in APP L3.0. (T) Q⁰ := S₀ ∪ {l ∉ S₀ :
min_{k∈S₀}‖x(l) − x(k)‖ ≤ d_n} [R01-3] with d_n of APP L3.0 (with the constants (K₂, t₂) of Lemma CD_d), enlarged to [p] if p < 2|Q⁰| + 32s₀ + 1;
|Q| = O((log n)^d). Conclusion: P(Sand_n) → 1, P(NA(𝓛)) → 1, P(TL(𝓛)) → 1 and all conclusions of (C), with the shipped
LS0 cap. d = 1 with integer sites contains APP Theorem LOC. Files `lemmas/L3_CTd.md` (Lemma CT_d, CD_d, regression
ℓ¹ bound), `lemmas/L4_LOCd.md` (sandwich delta and (R1)–(R3)).

**(D2) Theorem LOC-BF (target (c), middle regime and beyond).** Σ_n block-diagonal w.r.t. a deterministic partition into
groups; every group G is either (i) of size ≤ g₀ (fixed) with λ_min(Σ_GG) ≥ c, or (ii) one-factor: Σ_GG = b_Gb_Gᵀ +
diag(1 − b_v²), b_v ∈ {0} ∪ [b_lo, b̄] with 0 < b_lo ≤ b̄ < 1 fixed (contains compound symmetry with ρ ∈ [b_lo², b̄²]),
of size ≤ g_n with g_n ≤ (log n)^{κ} (κ ≥ 1 fixed, WLOG); at most one truth per group. Q⁰ := ⋃_{j∈S₀} G(j), enlarged as above.
Conclusion: as (D1). This covers the middle regime (log n ≲ g_n with s₀(g_n − 1) > (1 − δ₀) log n, where APP LOC-B
does not apply — failure of LOC-B's sufficient size inequality, not an impossibility for its route) and polylogarithmic
g_n. The class INCLUDES sequences on which APP L5_VN obstructs the GROW/LOC route (|Q| = O(log n)): e.g. compound-symmetric
truth groups with fixed ρ ∈ [b_lo², b̄²], ≤ one truth per group and actual size g_n with g_n/log n → ∞ (VN (V2)); the class
also contains sequences with no visible nulls (e.g. all b_v = 0), where no obstruction is asserted [R01-4]. File
`lemmas/L4_LOCd.md` §B.

**(D3) Polynomial decay (target (b), stretch; NOT locked — a failure of (D3) would leave (A)–(D2) and delivery for (D1)/(D2)
intact and withdraw only the (D3)-specific delivery [R07-11]).** Σ_n with
|Σ_jk| ≤ K_dec(1 + |π(j) − π(k)|)^{−α} (π a bijection onto [p]),
spectrum in [c, C], PTV (APP L3.0), fixed constants: reported-model consistency — the conclusions of (C-i) and (C-ii) —
for α > α₀ := 17/2 [v1.2, C1-Opus-1]. The chosen Q has radius ⌈D n^{1/(2α)}⌉ around S₀ (any fixed D > 0), enlarged as in
(D1), so |Q| = O(n^{1/(2α)}) (an upper bound; the decay is an envelope), and (A)–(C) are re-run with polynomial sizes in
L6. File `lemmas/L6_poly.md`.
**v1.2 (2026-11-09, logged): α₀ filled in (originally "to be determined").** The claimed instance is α > α₀ := 17/2 (one-dimensional sites, π a bijection
onto [p]; Q of radius ⌈D n^{1/(2α)}⌉ around S₀, enlarged as above; all conclusions of (C-i)/(C-ii)). α₀ is the cutoff of
the proof's selection-removal/junk-exclusion counting, not a necessity statement. This fills the declared stretch slot;
no other claim changes. Status: L6 PROVED (by this seat, unchecked); checks R06a (Opus high) and R06b (Sol xhigh)
VERIFIED-WITH-AMENDMENTS, applied; the (D3) class was then added to (E).

**(E) Proposition F-LOC2 (delivery).** Under the method, premises and allocation of FACA L7 (Proposition F-FAC; FIN s6
Proposition F with cap a_n = ℓ_n + |S̃₀|), for the classes of (D1), (D2) and (D3) (the last added after its checks R06a/R06b, v1.2): P(no output) = 0 for every
admissible n ≥ 3 and P(Ŝ⁺ = S₀) → 1 under the joint design/noise law. File `lemmas/L7_delivery.md`.

## 3. Not claimed
Non-Gaussian rows; fixed-domain (infill) spatial asymptotics (correlation range growing in site units: the constants
(K, a) would not be fixed); growing s₀; θ*_min → 0; PTV failures (masking); general growing blocks that are neither
bounded nor one-factor; multi-factor blocks; groups containing ≥ 2 truths; one-factor groups of size > (log n)^κ (e.g.
polynomial); polynomial decay with α ≤ 17/2 (incl. long memory); polynomial decay in d ≥ 2 [C1-Opus-2]; anything about
pervasive (non-block) factor designs (FAC tickets); finite-n statements.

## 4. Dependencies (statuses verbatim)
APP Theorem LOC / LOC-B / Lemma CT/CD / POST: inside W2-APP "PROVED-CHECKED" (lemma statuses "PROVED (by this seat,
unchecked)", checks R02/R03 VERIFIED(-WITH-AMENDMENTS)); C-GROW "PROVED-CHECKED" (L0, L1 R03 VERIFIED; L2 R03
VERIFIED-WITH-AMENDMENTS; L3 R02 VERIFIED; L4 R04 VERIFIED-WITH-AMENDMENTS; L6 R07 VERIFIED / R06
VERIFIED-WITH-AMENDMENTS); GEN L1 "PROVED (by this seat, unchecked)" (R02 VERIFIED-WITH-AMENDMENTS); [OP] "PROVED (by
this seat, unchecked)" inside GEN "PROVED-CHECKED"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; M5(0)
"PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; FACA Proposition F-FAC "PROVED (by this seat, unchecked)"
(R04 VERIFIED-WITH-AMENDMENTS) inside W2-FAC-A "PROVED-CHECKED".
