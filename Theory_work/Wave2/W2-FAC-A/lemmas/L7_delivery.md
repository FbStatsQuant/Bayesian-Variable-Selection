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

**Proposition F-FAC.** Under the method, premises and allocation above, for the added classes: for every admissible
n ≥ 3, P(no output) = 0; and along each sequence in the classes, P(Ŝ⁺ = S₀) → 1, under the original unconditioned noise
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
