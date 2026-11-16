# L7 — Delivery: Proposition F-FAC (claim (D))

Status: **PROVED (by this seat, unchecked)** — v1.1, 2026-11-09; lemma check R04 (Sol high): VERIFIED-WITH-AMENDMENTS
(applied). Template: HQ audit A2 ("EXTENDS"; "PROVED (A2), checked
by A3"; FINAL s6 Proposition F-GROW), whose three steps are re-run for the classes of (L4) and (L5).

**Method, premises, allocation** (exactly those of FINAL s6 Proposition F / A1's corrected statement with the A4
preflight addition): v3.1 with deterministic complete-scan LS0 from the exact e4 start-mode maximiser (TDP-IMPL), LS0 move
cap a_n = ℓ_n + |S̃₀| (= the merged MR1 (C-GROW) cap), all other caps ℓ_n; total tier-1 fallback with complete
fallback-grid freezing; EX-A (unit-cost exact reals), IDEAL-W, EX-S, SR, e4, GUARD-W, MACH, CONFIG (fixed declared
R′ = 4k, fixed worker count), valid declared seed, and the complete allocation inequalities of FINAL s6 Proposition F (R04 item 6), including
MACH conversion constants, the original preflight/certificate bounds, the memory/time pairing with M_G/W_G, and A4's
P_e + A and P̄_LS0 bounds, evaluated at (n, p_raw); as in A3's amendment the LS0 score count is ≤ 1 + (ℓ_n + K + 1)q(p),
increasing the total by Kq(p). CAL is not assumed. The P1 exit inventory and
Lemma S.3 keep their "AUDITED (code reading)" status; the LS0/worker/fallback paths are covered by premises (FINAL s6
Remark (3)).

**Classes added.** (i) Fixed designs satisfying the hypotheses of Theorem L4.1 (G, (H0), (AG), (P), (TV)), including
(I)(a) exact-Gram compound symmetry under (GC-CS) and exact-Gram S5 / block CS with certified (TV); (ii) iid Gaussian rows
satisfying Proposition L5.1 (incl. (I)(b) and the iid S5 instance (I)(c)).

**Proposition F-FAC.** Under the method, premises and allocation above, for the added classes: (a) for every admissible n ≥ 3 with (n, p_raw) ∈ 𝔇 := {ℓ_raw ≤ 10⁶ and ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1}, ℓ_raw := ⌈log₂(n + p_raw + 1)⌉, P(no output) = 0;
(b) under A:IDEAL-W⁺ in place of IDEAL-W (IDEAL-W, and the two shipped rejection predicates `le > 10⁶` (Scripts/SMC_BVS/core/v3_run.R:96) and `ℓ + |S̃₀| > INT_MAX` (Scripts/SMC_BVS/core/cpp/v3_core.cpp:474) are false; definition at the end of this file): for every admissible n ≥ 3, P(no output) = 0; and along each sequence in the classes, P(Ŝ⁺ = S₀) → 1, under the original unconditioned noise
law (fixed designs) or the joint design/noise law (iid rows), together with the algorithm's randomness.

*Proof.* **Step 1 (Lemma S extends; A2 step 1).** Fixed designs: nonconstant raw columns by G; standardisation gives
centred columns of squared norm n − 1. Iid rows: Σ_n is a correlation matrix with λ_min ≥ ψ₀ > 0, so each raw column has
iid nondegenerate Gaussian entries and is nonconstant a.s.; the finite union of constant-column events is null; no column
is dropped, so the retained p equals p_raw a.s. and the allocation depends only on (n, p_raw). A constant centred response
is a null event (fixed design: ε Gaussian on an affine line has probability 0; iid rows: conditionally on X, Cε has a
nondegenerate law on 1^⊥ for n ≥ 3). The scorer never fails: for every feasible S, H = (n + 1)G_S + I ≻ 0,
G_S + I ≻ 0 and Q_S ≥ yᵀy/(n + 1) > 0 — no rank or relevance-size condition, so pervasive correlation and p = o(n)
cause no numerical obstruction. S.3 keeps its AUDITED status with "successful construction" read as "successful
construction or complete fallback pilot" (A2, A3).
**Step 2 (delivery; A2 step 2).** Unchanged from A2: the merged cap a_n ≤ ℓ_n + K permits at most ℓ_n + K + 1 LS0 scans,
i.e. at most Kq(p) extra score requests, covered by W_G, M_G; Corollary R's guard/preflight/allocation argument applies;
with the total fallback schedule_limit is empty, so Theorem D's exit walk leaves only null exits: P(no output) = 0.
Growing p and factor correlation change none of these exclusions (they are uniform in valid inputs).
**Step 3 (consistency).** Let 𝒦_n := {deterministic LS0 with cap a_n, run on the data, scores S₀} (defined whether or not
the run delivers). On Sand_n ∩ NA(𝓛) ∩ TL(𝓛) the exact start mode lies in 𝓛 (L2; K = p eventually), and by C-GROW L1.2
LS0 deletes one extra per move and scores S₀ within a_n ≥ |S̃₀ ∖ S₀| moves, so
  P(𝒦_nᶜ) ≤ P(Sand_nᶜ) + P(NA(𝓛)ᶜ) + P(TL(𝓛)ᶜ) → 0
by L2, L3 (fixed design) or Proposition L5.1 (iid rows). This is not inferred from D_n → 0 ([OP] bounds D_n in the
opposite direction). Posterior input: T03♯ under (H0) (fixed design), resp. the design events and the every-sequence
argument of L5.1 (iid rows), give E[1 − π(S₀)] → 0. D′'s pathwise scored-set argument (DLV lemmas/L4_delivery.md:65-77;
FINAL s6 Corollary D′): on output and 𝒦_n, S₀ was scored (or exact enumeration scored every feasible model); if
π(S₀ | y) > ½ its score strictly exceeds every competitor, so Ŝ⁺ = S₀. Hence, eventually s₀ ≤ K,
  P(output and Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ) → 0,
and with P(no output) = 0, P(Ŝ⁺ = S₀) → 1. ∎

**Qualifications inherited (verbatim spirit of A3 finding 4).** [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3,
"OPEN" (here only "some maximiser" is used for consistency; delivery keeps e4 with TDP-IMPL as in Proposition F); S.3 is a
code-reading audit; the fallback was a change to a shipped component, now merged on main (4676af6).

**IDEAL-W⁺ narrowing note (2026-11-16; HQ D78 correctness event; outside every registered statement span).** Proposition F-FAC (`:22-24`) now states delivery in two clauses, in the form of W2-UNI's Proposition F-UNI v2 (`Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md`): (a) under IDEAL-W, P(no output) = 0 only on the bounded domain 𝔇; (b) for every admissible n, and every asymptotic delivery conclusion, under A:IDEAL-W⁺. Reason (Sol review TR1, `Theory_work/Dept/research/FUNI_transfer/TR1_sol.md` §1–§2): two shipped LS0 cap validators lie outside Theorem D's exit walk and can end an SMC-branch fit without output, independently of resources: `le > 1e6` (`Scripts/SMC_BVS/core/v3_run.R:96-97`; le = ℓ_n in the stated configuration) and `cap_ll > numeric_limits<int>::max()` with cap_ll = ℓ_n + |S̃₀| (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`). IDEAL-W (C-DLV `STATEMENT.md:24-25`, unchanged) excludes overflow, not these application-level rejection predicates. On 𝔇 neither predicate fires: ℓ_n ≤ ℓ_raw ≤ 10⁶ (p ≤ p_raw) and ℓ_n + |S̃₀| ≤ ℓ_raw + K_n ≤ ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1; the exact-enumeration branch reaches neither check. 𝔇 is sufficient, not necessary, and bounded, so clause (a) carries no asymptotic conclusion. Under A:IDEAL-W⁺ both predicates are false. In both clauses the no-output step of the proof (Theorem D's exit walk with the total tier-1 fallback and the stated allocation, which already contains A4's LS0 preflight terms P_e + A and P̄_LS0 (FIN `s6_delivery.tex:37-44`)) is otherwise unchanged (TR1 §1 table). Definition (verbatim; registered assumption A:IDEAL-W⁺):

**A:IDEAL-W⁺ (IDEAL-W with the two LS0 cap ceilings lifted).** IDEAL-W, exactly as defined in C-DLV `STATEMENT.md:24-25`, and the two shipped rejection predicates `le > 10⁶` (`Scripts/SMC_BVS/core/v3_run.R:96`, the LS0 base-cap validator; le = ℓ_n = ⌈log₂(n + p + 1)⌉ in the shipped configuration) and `ℓ + |S̃₀| > INT_MAX` (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`, the disjunct `cap_ll > numeric_limits<int>::max()` of the LS0 cap-range guard, `int` read as unbounded) are false. Nothing else is lifted: the other conditions of those two validators (numeric type, length, finiteness, integrality, `le < 0`, `o.ls0_ell < 0`), every other validator, the 10⁶-maximiser start-mode enumeration cap with its tie-aware DP fallback, and every fallback and method cap are kept as coded. Like IDEAL-W and EX-A, A:IDEAL-W⁺ is an idealisation of the machine and code; a larger allocation does not imply it.
