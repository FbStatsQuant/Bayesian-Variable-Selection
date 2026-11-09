# L4 — Assembly: Theorem FAC-PK (claims (P4), (P5)) and the reading of Theorem NEG

Status: **PROVED (by this seat, unchecked)** given the cited inputs with their recorded statuses; lemma check R05 (Codex
Sol high, reviews/R05_L4_check_sol.md): VERIFIED-WITH-AMENDMENTS (1 major resource-scope, 4 minor, 2 editorial), applied.

Inputs (statuses verbatim, as recorded in FACB STATEMENT §6 and FACB L5): [M5-0] T38-(0) "PROVED (SF: VERIFIED
(W3-VT38E); XF: VERIFIED* (A-REV5))"; [S-T] T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; [OP]
"PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED" (its argument uses only GUARD-W, OP-LS0, e4 and
that LS0 is deterministic given the data, not the cap value); Lemma CAP (FINAL s7) "PROVED (by this seat)",
council-checked; Proposition F with A1's corrected statement (A1 "HOLDS-WITH-AMENDMENTS"; council round 3 checked the
d315c1e statements) and A2's extension ("PROVED (A2), checked by A3"); the later head-code preflight allocation addition
checked separately in A4 ("OK-WITH-FIXES", fixes applied) [R05-7]; FACB L5
(R05 VERIFIED-WITH-AMENDMENTS) for the form of the (H0) verification and the delivery argument. This folder: L0–L3.

## L4.1 (H0) holds (FACB L5.1, re-read for p ≤ n − 1)
FACB L5.1 uses (CS), (θ) and p ≤ n¹ only: ‖μ‖² = (n − 1)ϑᵀΣ̄_{S₀S₀}ϑ ≤ Mn; every principal submatrix of R̂ = Σ has
λ_min ≥ 1 − ρ, so SE_λ and SE_w hold with φ₀² = g₀ = 1 − ρ (λ_min(X_AᵀX_A) ≥ (n − 1)(1 − ρ) for every nonempty A ⊆ [p]);
A = 1 since p ≤ n − 1; s₀ ≤ K; BM-∞ since |ϑ|_min fixed. Its line "p ≤ n/2 ≤ n¹" is replaced by p ≤ n − 1 ≤ n¹; nothing
else depends on p ≤ n/2. Hence [S-T]: E₀[1 − π(S₀)] → 0.

## L4.2 Theorem FAC-PK (under MR-PK)
**Theorem FAC-PK.** Under G, (CS), (θ) (θ̄ ≠ 0, every ϑ_r ≠ 0), blocks of size ≤ 16, K + 16s₀ + 1 ≤ p_n ≤ n − 1
(eventually), the implementation premises of FACB STATEMENT §1 (with CAL for (ii)) and an LS0 cap rule a = a(data),
a finite-integer-valued measurable function of the admissible data with a ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉) for a fixed δ > 0
and, for (iii) only, (α) the deterministic bound a(data) ≤ ℓ_n + 2K on every admissible input (R02 item 1) and (β) an
evaluation of a(data) whose work and memory are bounded by the implementation constants absorbed in W_G′, M_G′ (a
general measurable rule is an abstract cap parameter; its evaluation cost is not otherwise charged) [R05-1]. The three
proposed rules satisfy (α), (β) (O(1) arithmetic on |S̃₀|, ℓ_n, p, K, computed after the start mode): ℓ_n + 2|S̃₀|;
ℓ_n + ⌈(1 + δ)|S̃₀|⌉ with 0 < δ ≤ 1; and, under (PK), max(ℓ_n + |S̃₀|, p), which is ≤ max(ℓ_n + K, 2K + 1) ≤ ℓ_n + 2K since
p ≤ n − 1 ≤ 2K + 1, and is ≥ max(ℓ_n, ⌈17|S̃₀|/16⌉) on **every** admissible input for n ≥ n₀, because (PK) gives
p ≥ (17/16)K ≥ (17/16)|S̃₀| deterministically (16/15 > 17/16) [R05-5]:
(i) (H0) holds; (ii) D_n(a) ≤ P(𝒦_n(a)ᶜ) → 0, 𝒦_n(a) := {LS0(a) scores S₀}; P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and
liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n); (iii) (delivery) under Proposition F's premises, total tier-1 fallback and
the allocation with the LS0 terms re-charged for caps ≤ ℓ_n + 2K (METHOD_REQUIREMENTS.md): P(no output) = 0 for every
admissible n ≥ 3 and P(Ŝ⁺ = S₀) → 1 (CAL not used).

*Proof.* (i) L4.1. (ii) Theorem PATH (L3) gives P(𝒦_n(a)) → 1 (LS0(a) ends certified at S₀; S₀ is scanned, hence
scored). [OP] gives D_n(a) ≤ P(𝒦_n(a)ᶜ) (cap-free argument). [M5-0] with (i): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[1 − π(S₀)] + D_n → 0.
(iii) As FACB L5.4 / A2, step by step [R01-9]. (1) *Lemma S extends:* a fixed exact-Gram CS design is a fixed
standardised design with nonconstant raw columns (model G), so no column is dropped and p_raw = p; the centred response
is nonconstant with probability one (ε Gaussian); Q_S ≥ yᵀy/(n + 1) > 0 for every S, so the scorer never fails (no
relevance or rank condition is used, A2 step 1); S.3 keeps its AUDITED (code reading) status. (2) *No output has
probability 0:* Proposition F's walk over the exit inventory (P1, AUDITED) with total tier-1 fallback (so 𝒮ℒ_n = ∅),
EX-A (unit cost), IDEAL-W, EX-S, SR, e4, GUARD-W, TDP-IMPL, MACH, CONFIG, valid declared seed and the allocation built
from the re-charged envelopes. For cap rules satisfying (α), (β) the only count that changes is LS0's: at most a + 1 ≤ ℓ_n + 2K + 1 complete
scans, hence at most 1 + (ℓ_n + 2K + 1)q(p) LS0 score requests (q(p) = p + p²/4), i.e. Kq(p) more than A2's
1 + (ℓ_n + K + 1)q(p), or 2Kq(p) more than the legacy bound 1 + (ℓ_n + 1)q(p) underlying W̄ [R05-6]; Lemma R's envelopes with this LS0 term (W_G′ := W̄ + C·2Kq(p)[n³ + p(n + 2)],
M_G′ := M̄ + C·2K(2K + 1)) and the head-code preflight terms with s′ := ℓ_n + 2K + 1 (time
P̄_LS0′ := s′q(p)(τU_K + τ₀)/100 ≥ 2s′q(p)ŝ_K under MACH; archive bytes (2s′ + 4)(12K + 256) + 96s′ + 4(8W + 4K + 96) + 4096)
bound every resource path. Explicitly, the sufficient allocation (FINAL s6:33–44, A4:7–25, with the re-charged terms) is
  mem_n ≥ max{βM_G′ + β₀, P₀ + A′, P₁ + A′},  time_n ≥ max{2(τW_G′ + τ₀), P̄_t, P̄_LS0′},
  allocation$mem_gb ≥ mem_n/2³⁰,  allocation$hours ≥ time_n/3600,
with A′ the archive bytes above (W = ⌈p/64⌉, raw dimensions, p_raw = p) and U_K bounding the whole 200-score timed
interval (model construction, sorting, scoring) [R05-7]; so the guard and the preflight never fire under that allocation
(strict-inequality rejection tests, as in s6_delivery.tex). Hence P(no output) = 0 for every admissible n ≥ 3. (3) *Consistency (not inferred from D_n → 0):* D′'s pathwise inclusion
𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ {π(S₀ | y) ≤ ½} ∪ 𝒦_n(a)ᶜ, P(𝒪) = 1, Markov: P(Ŝ⁺ ≠ S₀) ≤ 2E₀[1 − π(S₀)] + P(𝒦_n(a)ᶜ) → 0. The
exact-arithmetic/unit-cost and code-audit qualifications of Proposition F are inherited; (iii) refers to the method with
the METHOD_REQUIREMENTS plumbing added (the head code cannot select the proposed rules), whose changed lines are not
covered by the existing code audits [R09-M1]. ∎

## L4.3 Reading of Theorem NEG for the merged method (MR1)
Under (CS), (PK), (PB), (θ): P(𝒦_n(a_n)) → 0 for a_n = ℓ_n + |S̃₀| (L2). Hence [OP] yields only D_n ≤ 1 − o(1): **the
LS0 route to (C3)/(C4) is unavailable for the merged method on this class.** Whether D_n → 0 for MR1 depends on the SMC
run and the final local search (from the HPM, cap ℓ_n), about which no discovery theorem exists; production-code
evidence: numerics/full_method/ (claim (P6)) and W2-SIM R2. The legacy cap ℓ_n fails a fortiori (Lemma CAP(b)).

## L4.4 Cost (P5)
LS0's worst-case number of complete scans is a + 1 ≤ ℓ_n + 2K + 1 under MR-PK versus ℓ_n + K + 1 under MR1, each scan
≤ q(p) = p + p²/4 score requests (FINAL s7 "What does not transfer verbatim"); so, for cap rules with a ≤ ℓ_n + 2K, each LS0 worst-case charge (scan-proportional work, preflight time
2(·)q(p)ŝ_K, requests 1 + (·)q(p), archive memory c·s + d) is **at most** r := (ℓ_n + 2K + 1)/(ℓ_n + K + 1) ≤ 2 times its
MR1 charge (with equality only for the scan-proportional terms) [R05-2]. These are statements about LS0's charges; the
conservative delivery envelope increments (e.g. C·2K(2K + 1) vs C·K(K + 1)) and total fit runtime are not claimed to
scale by r. For rules with a ≥ ℓ_n + |S̃₀|,
realised LS0 work is unchanged on every data set where the MR1 search already ends certified (Lemma CAP(a)); not for
smaller rules (R02 item 2).
