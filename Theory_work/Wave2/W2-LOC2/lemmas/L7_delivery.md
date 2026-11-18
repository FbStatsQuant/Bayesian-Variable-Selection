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

**Proposition F-LOC2.** Under the method, premises and allocation above, for these classes: (a) for every admissible n ≥ 3 with (n, p_raw) ∈ 𝔇 := {ℓ_raw ≤ 10⁶ and ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1}, ℓ_raw := ⌈log₂(n + p_raw + 1)⌉, P(no output) = 0; (b) under A:IDEAL-W⁺ in place of IDEAL-W (IDEAL-W, and the two shipped rejection predicates `le > 10⁶` (Scripts/SMC_BVS/core/v3_run.R:96) and `ℓ + |S̃₀| > INT_MAX` (Scripts/SMC_BVS/core/cpp/v3_core.cpp:474) are false; definition at the end of this file): for every admissible n ≥ 3,
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

**IDEAL-W⁺ narrowing note (2026-11-16; HQ D78 correctness event; outside every registered statement span).** Proposition F-LOC2 (`:17-19`; registered at `STATEMENT.md:100-102`) now states delivery in two clauses, in the form of W2-UNI's Proposition F-UNI v2 (`Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md`): (a) under IDEAL-W, P(no output) = 0 only on the bounded domain 𝔇; (b) for every admissible n, and every asymptotic delivery conclusion, under A:IDEAL-W⁺. Reason (Sol review TR1, `Theory_work/Dept/research/FUNI_transfer/TR1_sol.md` §1–§2): two shipped LS0 cap validators lie outside Theorem D's exit walk and can end an SMC-branch fit without output, independently of resources: `le > 1e6` (`Scripts/SMC_BVS/core/v3_run.R:96-97`; le = ℓ_n in the stated configuration) and `cap_ll > numeric_limits<int>::max()` with cap_ll = ℓ_n + |S̃₀| (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`). IDEAL-W (C-DLV `STATEMENT.md:24-25`, unchanged) excludes overflow, not these application-level rejection predicates. On 𝔇 neither predicate fires: ℓ_n ≤ ℓ_raw ≤ 10⁶ (p ≤ p_raw) and ℓ_n + |S̃₀| ≤ ℓ_raw + K_n ≤ ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1; the exact-enumeration branch reaches neither check. 𝔇 is sufficient, not necessary, and bounded, so clause (a) carries no asymptotic conclusion. Under A:IDEAL-W⁺ both predicates are false. In both clauses the no-output step of the proof (Theorem D's exit walk with the total tier-1 fallback and the stated allocation, which already contains A4's LS0 preflight terms P_e + A and P̄_LS0 (FIN `s6_delivery.tex:37-44`)) is otherwise unchanged (TR1 §1 table). Definition (verbatim; registered assumption A:IDEAL-W⁺):

**A:IDEAL-W⁺ (IDEAL-W with the two LS0 cap ceilings lifted).** IDEAL-W, exactly as defined in C-DLV `STATEMENT.md:24-25`, and the two shipped rejection predicates `le > 10⁶` (`Scripts/SMC_BVS/core/v3_run.R:96`, the LS0 base-cap validator; le = ℓ_n = ⌈log₂(n + p + 1)⌉ in the shipped configuration) and `ℓ + |S̃₀| > INT_MAX` (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`, the disjunct `cap_ll > numeric_limits<int>::max()` of the LS0 cap-range guard, `int` read as unbounded) are false. Nothing else is lifted: the other conditions of those two validators (numeric type, length, finiteness, integrality, `le < 0`, `o.ls0_ell < 0`), every other validator, the 10⁶-maximiser start-mode enumeration cap with its tie-aware DP fallback, and every fallback and method cap are kept as coded. Like IDEAL-W and EX-A, A:IDEAL-W⁺ is an idealisation of the machine and code; a larger allocation does not imply it.
