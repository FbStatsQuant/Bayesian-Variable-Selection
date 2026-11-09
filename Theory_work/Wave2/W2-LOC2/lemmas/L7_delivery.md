# L7 — Delivery: Proposition F-LOC2

Status: **PROVED (by this seat, unchecked)**. Template: W2-FAC-A `lemmas/L7_delivery.md` (Proposition F-FAC, "PROVED (by
this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS), which re-runs the three steps of HQ audit A2 / FIN s6 Proposition
F-GROW (`Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:54`). Check record: R04 (Codex gpt-6.1-sol high, `reviews/R04_L4L5L7_check_sol.md`): see `reviews/R04_disposition.md` (L4, L5 VERIFIED-WITH-AMENDMENTS, applied; L7 VERIFIED).

**Method, premises, allocation.** Exactly those of Proposition F-FAC (FACA L7, first paragraph): v3.1 with deterministic
complete-scan LS0 from the exact e4 start-mode maximiser (TDP-IMPL), LS0 move cap a_n = ℓ_n + |S̃₀| (the merged cap), all
other caps ℓ_n; total tier-1 fallback with complete fallback-grid freezing; EX-A, IDEAL-W, EX-S, SR, e4, GUARD-W, MACH,
CONFIG (fixed R′ = 4k, fixed worker count), valid declared seed, the complete allocation inequalities of FIN s6
Proposition F (with A1's envelopes W_G, M_G and A4's preflight bounds, LS0 score count ≤ 1 + (ℓ_n + K + 1)q(p)),
evaluated at (n, p_raw). CAL is not assumed.

**Classes.** Iid Gaussian rows satisfying Theorem LOC-d (L4 Part A), Theorem LOC-BF (L4 Part B), or the polynomial-decay
theorem of L6_poly (α > 17/2; added after its checks R06a/R06b).

**Proposition F-LOC2.** Under the method, premises and allocation above, for these classes: for every admissible n ≥ 3,
P(no output) = 0; and along each sequence, P(Ŝ⁺ = S₀) → 1 under the joint design/noise law, together with the
algorithm's randomness.

*Proof.* **Step 1 (input validity; FACA L7 Step 1).** λ_min(Σ_n) ≥ c > 0 (LOC_d and L6: spectrum in [c, C]; LOC-BF: c_B), so
each raw column has iid nondegenerate Gaussian entries and is nonconstant a.s.; no column is dropped, the retained p
equals p_raw a.s., and the allocation depends only on (n, p_raw). A constant centred response is a null event
(conditionally on X, Cε has a nondegenerate law on 1^⊥ for n ≥ 3). The scorer never fails (H = (n + 1)G_S + I ≻ 0,
G_S + I ≻ 0, Q_S ≥ yᵀy/(n + 1) > 0) — no condition on the design. S.3 keeps its AUDITED (code reading) status, as in FACA L7.
**Step 2 (no-output exits; FACA L7 Step 2).** Unchanged and design-independent: the merged cap a_n ≤ ℓ_n + K permits at
most ℓ_n + K + 1 LS0 scans, covered by W_G, M_G; Corollary R's guard/preflight/allocation argument applies; with the
total fallback schedule_limit is empty; Theorem D's exit walk leaves only null exits: P(no output) = 0.
**Step 3 (consistency).** 𝒦_n := {deterministic LS0 with cap a_n, run on the data, scores S₀}. On Sand_n ∩ NA(𝓛) ∩ TL(𝓛)
the exact start mode lies in 𝓛 and by GROW L1.2 LS0 scores S₀ within a_n ≥ |S̃₀ ∖ S₀| moves, so
P(𝒦_nᶜ) ≤ P(Sand_nᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0 by Theorem LOC-d / LOC-BF / L6_poly §§3–6 (not inferred from D_n → 0). Posterior input:
E[1 − π(S₀)] → 0 (L5 (c)). The scored-set argument of Corollary D′ (FACA L7 Step 3; `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:65-77` [R07-15]): on
output and 𝒦_n, S₀ was scored (or exact enumeration scored every feasible model); if π(S₀ | y) > ½ its score strictly
exceeds every competitor, so Ŝ⁺ = S₀. Hence, once s₀ ≤ K, P(output and Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ) → 0, and with
P(no output) = 0, P(Ŝ⁺ = S₀) → 1. ∎

Qualifications inherited verbatim from FACA L7: [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only
"some maximiser" is used for consistency; delivery keeps e4 with TDP-IMPL as in Proposition F); S.3 is a code-reading
audit; the fallback is merged on main (4676af6).
