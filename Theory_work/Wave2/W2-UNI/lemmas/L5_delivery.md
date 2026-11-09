# L5 — Proposition F-UNI (design-agnostic delivery reduction, R4)

Status: **PROVED (by this seat, unchecked)** — v1, 2026-11-09. Template: W2-FAC-A `lemmas/L7_delivery.md` (Proposition F-FAC,
"PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS) and W2-LOC2 `lemmas/L7_delivery.md` (Proposition F-LOC2,
"PROVED (by this seat, unchecked)", R04 VERIFIED), both inside "PROVED-CHECKED" tickets; FIN s6 Proposition F / F-GROW.
Check record: R03 (Codex gpt-6.1-sol xhigh, `reviews/R03_L3L6_check_sol.md`): VERIFIED-WITH-AMENDMENTS (item 4), applied.

**Method, premises, allocation.** Exactly those of Proposition F-FAC (FACA L7, first paragraph): v3.1 with deterministic
complete-scan LS0 from the exact e4 start-mode maximiser (TDP-IMPL), LS0 move cap a_n = ℓ_n + |S̃₀|, other caps ℓ_n; total
tier-1 fallback with complete fallback-grid freezing; EX-A, IDEAL-W, EX-S, SR, e4, GUARD-W, MACH, CONFIG (fixed R′ = 4k, fixed
worker count), valid declared seed, the complete allocation inequalities of FIN s6 Proposition F with A1's envelopes and A4's
preflight bounds, LS0 score count ≤ 1 + (ℓ_n + K + 1)q(p), evaluated at (n, p_raw). CAL not assumed. P1/S.3 keep "AUDITED
(code reading)".

**Proposition F-UNI.** Let a design sequence satisfy:
 (V) input validity: (R) with λ_min(Σ_n) > 0 for every n, or (E) with nonconstant raw columns;
 (S) for a deterministic Q_n ⊇ S₀ with 𝓛_n := {T : S₀ ⊆ T ⊆ Q_n} ⊆ Ω (|Q_n| ≤ K_n):
     P(Sand_n(Q_n) ∩ NA(𝓛_n) ∩ TL(𝓛_n)) → 1;
 (P) E[1 − π(S₀)] → 0 (under the law of the setting).
Then, under the method, premises and allocation above: for every admissible n ≥ 3, P(no output) = 0; and P(Ŝ⁺ = S₀) → 1
(joint design/noise law under (R), noise law under (E)), together with the algorithm's randomness.

*Proof.* Step 1 (input validity) — FACA L7 Step 1 uses only (V): under (R) each raw column has iid nondegenerate Gaussian
entries (Var = Σ_jj = 1 > 0) [R03-4], so no column is dropped, retained p = p_raw a.s., and the allocation depends on
(n, p_raw); a constant centred response is null; the scorer never fails — for every feasible S, H_S = (n + 1)G_S + I ≻ 0,
G_S + I ≻ 0 and Q_S ≥ yᵀy/(n + 1) > 0 — so no full-column-rank condition is needed (rank-deficient subsets are allowed).
Under (E) as FACA (fixed designs). Step 2 (no-output exits) — FACA L7 Step 2, design-free: P(no output) = 0.
Step 3 — 𝒦_n := {deterministic LS0 with cap a_n, run on the data, scores S₀}. On Sand_n(Q_n) ∩ NA(𝓛_n) ∩ TL(𝓛_n) the exact
start mode lies in 𝓛_n (Sand) and, by C-GROW L1.2 (hypotheses S₀ ⊆ Q_n, |Q_n| ≤ K; "PROVED (by this seat, unchecked)", R03
VERIFIED, inside C-GROW "PROVED-CHECKED"), LS0 deletes one extra per move and scores S₀ within a_n ≥ |S̃₀ ∖ S₀| moves. So
P(𝒦_nᶜ) → 0 by (S) — not inferred from D_n → 0. On output and 𝒦_n, S₀ was scored (or exact enumeration scored every feasible
model); if π(S₀ | y) > ½ its score strictly exceeds every competitor, so Ŝ⁺ = S₀ (Corollary D′, C-DLV
`lemmas/L4_delivery.md:65-77`, as used in FACA L7 Step 3). Hence P(output, Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ) → 0 (s₀ ≤ K
eventually), and with P(no output) = 0, P(Ŝ⁺ = S₀) → 1. ∎

**Instances.** UNI-0: (V) from λ_min(Σ_n) ≥ c; (S) with Q of STATEMENT (ii) (L2_k0); (P) from UNI-P (global floor ⇒ LSF).
UNI-1: (V) from λ_min(Σ_n) ≥ c (R) or by (E); (S) with Q_n = [p] (L4_k1; K = p eventually); (P) from T03♯ under (H0)
(fixed design, FACA L4 Note (5)) or UNI-P / FACA L5.1's every-sequence argument (R).
Qualifications inherited verbatim from FACA L7: [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only "some
maximiser" is used for consistency; delivery keeps e4 with TDP-IMPL as in Proposition F); S.3 is a code-reading audit.
