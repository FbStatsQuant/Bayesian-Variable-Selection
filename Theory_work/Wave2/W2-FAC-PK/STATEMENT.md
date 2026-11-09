# W2-FAC-PK — STATEMENT (target statement)

Ticket W2-FAC-PK, Theory Wave 2: compound symmetry with p > K = ⌊n/2⌋. Lead: Claude Opus 5.5 (Claude Work).
Status of this file: **v3.1 — LOCKED** (v3.1 = post-lock narrowing of (P4)(iii) to cheaply evaluated cap rules, R05
item 1, flagged; 2026-11-09; R02 LOCK-WITH-CHANGES, 3 required changes applied —
reviews/R02_relock_sol.md, reviews/R02_disposition.md). v1 was REJECTED by R01 (reviews/R01_statement_lock_sol.md,
10 required changes; disposition reviews/R01_disposition.md). v2 also replaces the dynamic proof route for (P3) by a
static one (lemmas/L3_static.md), which needs weaker hypotheses and claims less path structure.

Abbreviations: FACB = `Theory_work/Wave2/W2-FAC-B/`; FINAL = `Theory_work/Wave1C/FINAL/sections/`; SoP =
`Theory_work/State_of_Project/sections/`. All results asymptotic (Wave-2 scope rule).

## 0. Target, scope narrowing (flagged), diagnosis

HQ target (brief): settle compound symmetry for p > K (exact Gram first; p ≤ n^A including p ≫ n): (a) saturated start
and LS0 path; (b) consistency for the merged method, or a checked counterexample for the merged LS0 route, then whether
the full method still reports S₀; (c) the minimal LS0 cap change that provably works, consistency under it, its cost.

**Scope of this ticket — flagged narrowing [R01-1].** An exact Gram XᵀX = (n − 1)Σ with nonsingular Σ and centred
columns requires p ≤ n − 1. The theorems here are the **exact-Gram stage**: K < p ≤ n − 1. The p ≫ n stage of the brief
is **not settled** here; it is kept as an explicit open deliverable (§5), with the evidence requested from W2-SIM (R3:
iid-row CS including p ≫ n; numerics/SIM_REQUEST.md). Within the exact-Gram stage the negative claim (P2) is proved
only for liminf p/K > 16/15 (frontier: K < p ≤ (16/15)K), and (P1), (P3), (P4) only for p ≥ K + 16s₀ + 1 (frontier:
K < p < K + 16s₀ + 1, e.g. p_n = K_n + 1, where the start need not be saturated — R02 item 3) [R02-3]. The full-method question (P6) is numerical only and pending.

**Diagnosis (numerics, not proofs) [R01-10].** N1 (numerics/N1_raw.jsonl, 60 data sets, ρ = 0.5, n ≤ 2·10⁴,
p/n ∈ {0.6, 0.75, 0.95}): 55 saturated starts (|S̃₀| = K; the 5 others at n = 600, p = 360 have |S̃₀| ∈ [243, 253]);
every uncapped LS0 path is W null–null swaps followed by |S̃₀| − s₀ null deletions ending at S₀ (no swap after the
first deletion, no addition); W grows with n and p/n (p/n = 0.95: 27–46, 87–127, 189–208, 289–381 at n = 600, 2·10³,
6·10³, 2·10⁴); LS0 with the MR1 cap misses S₀ in 53/60 (all 53 saturated), with ℓ_n + 2|S̃₀| in 0/60. N3
(numerics/N3_raw_final360.jsonl, frozen; FROZEN_SNAPSHOTS.sha256; 360 paths, ρ ∈ {0.2, 0.5, 0.8, 0.95}, p up to n − 1,
5 truth layouts): no swap after the first deletion and no addition in any path; the 9 paths not ending at S₀ are the
near-cancelling layout (θ̄ = −0.1) at n = 2000, ρ = 0.95; ℓ_n + 2|S̃₀| scores S₀ in 360/360.

## 1. Setting

As FACB STATEMENT §1 (model G, D0 score, capped BB(1, p) prior, Ω = {|S| ≤ K}, start γ₀, LS0 = one §6.10 search from
the emitted start-mode centre, implementation premises EX-A, EX-S, SR, GUARD-W, OP-LS0, e4′, complete scans), with:
* **Caps.** ℓ_n := ⌈log₂(n + p + 1)⌉; merged MR1 cap a_n := ℓ_n + |S̃₀| (main 4676af6). LS0(a) := the deterministic LS0
  search with nonnegative integer cap a = a(data); "LS0(a) scores S₀" refers to LS0's scored set; by the single-search
  prefix property (FINAL s7, loop rule (L3)) LS0(a) scans exactly the first min(a, m*) + 1 centres of the uncapped path
  (m* its number of moves).
* Blocks: any deterministic partition into blocks of size ≤ 16 (claims (P1)(a)(b), (P3)); (PB) below for (P1)(c)(d), (P2).

## 2. Hypotheses

* **(CS)** XᵀX = (n − 1)Υ_n[(1 − ρ)I_p + ρ11ᵀ]Υ_n, ρ ∈ (0, 1) fixed, Υ_n deterministic diagonal ±1.
* **(θ)** s₀ fixed; sign-corrected truth coefficients equal a fixed ϑ ∈ (ℝ ∖ {0})^{s₀}; θ̄ := ϑ(S₀) ≠ 0; σ² fixed.
  By the global flip Υ_n ↦ −Υ_n (FACB L1.0) we take θ̄ > 0.
* **(PK′)** K + 16s₀ + 1 ≤ p_n ≤ n − 1 for all large n.
* **(PK)** (PK′) and liminf_n p_n/K_n > 16/15.
* **(PB)** blocks of size ≤ 16, all but at most J₀ (fixed) of size exactly 16. (Remark L1.4: under EX-A the method's
  partition of an exactly equicorrelated Gram is consecutive with B = min(⌊√n⌋, ⌊√p⌋, 16); argument sketched, checked
  numerically for 5 values of p; (PB) is a hypothesis, not a proved property of the coded partition [R01-5].)
No truth-keeping or sign-alignment hypothesis is used (v1's (TK) is dropped).

## 3. Claims

* **(P1) Start mode.** Under G, (CS), (θ), (PK′), blocks ≤ 16: w.p. → 1 every maximiser S of γ₀ on Ω has |S| = K and, in
  every truth-free block, every kept null has larger ξ (FACB L1.1 coordinates) than every excluded null. Under (PK),
  (PB) in addition: kept counts of any two full-size truth-free blocks differ by ≤ 1, and no full-size truth-free block is
  entirely kept (so each such block's minimum-ξ null is excluded).
* **(P2) Theorem NEG — the merged LS0 route fails.** Under G, (CS), (θ), (PK), (PB) and the LS0 premises, for every fixed
  β ∈ (0, ½): w.p. → 1 the first ⌊n^β⌋ moves of the uncapped LS0 path from the emitted centre are swaps (Lemma L2.3), and
  consequently LS0(a) does not score S₀ for any nonnegative integer cap a ≤ |S̃₀| − s₀ − 2 + ⌊n^β⌋; in particular
  P(LS0(a_n) scores S₀) → 0 for the MR1 cap and for the legacy cap ℓ_n. Reading: [OP]'s upper bound
  D_n ≤ P(LS0(a_n) misses S₀) is asymptotically uninformative on this class; (P2) gives no lower bound on D_n and says
  nothing about the full method.
* **(P3) Theorem PATH — LS0 with a larger cap.** Under G, (CS), (θ), (PK′), blocks ≤ 16 and the LS0 premises, for every
  fixed δ > 0: w.p. → 1 the uncapped LS0 path from the emitted centre ends at S₀, S₀ is a strict local maximum (every
  feasible neighbour has strictly smaller F), and m* ≤ (1 + δ)|S̃₀|. Hence LS0(a) ends at S₀ as a certified search
  endpoint for every cap a ≥ (1 + δ)|S̃₀|. No two-phase (swap, then deletion) structure is claimed; it is observed only.
* **(P4) Theorem FAC-PK (proposed cap).** For any cap rule a (finite-integer-valued measurable function of the admissible
  data) with a ≥ max(ℓ_n, ⌈(1 + δ)|S̃₀|⌉) for a fixed δ > 0, under the hypotheses of (P3) and the implementation
  premises: (i) (H0) holds with A = 1; (ii) D_n ≤ P(LS0(a) misses S₀) → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 (with CAL);
  (iii) delivery, **only for cap rules with the deterministic bound a(data) ≤ ℓ_n + 2K on every admissible input and an
  evaluation whose cost is absorbed in the implementation constants (e.g. O(1) arithmetic after the start mode)**
  [R02-1; post-lock narrowing R05-1, flagged] (e.g. ℓ_n + 2|S̃₀|; ℓ_n + ⌈(1 + δ)|S̃₀|⌉ with 0 < δ ≤ 1; max(ℓ_n + |S̃₀|, p), which is ≤ ℓ_n + 2K since
  p ≤ n − 1 ≤ 2K + 1, and satisfies the lower bound with δ = 1/16 eventually under (PK)): under Proposition F's premises, total tier-1 fallback, Lemma S extended
  to these fixed designs, and the allocation with LS0 terms re-charged for caps ≤ ℓ_n + 2K (score requests
  ≤ 1 + (ℓ_n + 2K + 1)q(p), q(p) = p + p²/4; work, archive memory and measured-score preflight terms as in
  METHOD_REQUIREMENTS.md): P(no output) = 0 for every admissible n ≥ 3 and P(Ŝ⁺ = S₀) → 1, obtained from
  P(LS0(a) scores S₀) → 1 and posterior concentration through D′'s pathwise inclusion (not from D_n → 0). The
  exact-arithmetic/unit-cost and code-audit qualifications of Proposition F are inherited.
  The head code cannot yet select these rules (v3_run.R:101 maps every non-legacy value to MR1; v3_fit.R:44 charges
  ℓ_n + K + 1 scans): (iii) is about the method with the plumbing of METHOD_REQUIREMENTS added, and the changed lines
  are not covered by the existing code audits [R09-M1].
* **(P5) What "minimal" means [R01-7].** Proved: allowances (over |S̃₀|) of size ≤ n^β, β < ½, fail ((P2): for fixed
  β < ½ pick β′ ∈ (β, ½); then |S̃₀| + n^β ≤ |S̃₀| − s₀ − 2 + ⌊n^{β′}⌋ eventually and (P2) applies with β′ [R06-3]); allowances
  ≥ δ|S̃₀| (any fixed δ > 0) suffice ((P3)). No optimality claim within this gap. Cost of a cap ≤ ℓ_n + 2K: every LS0
  worst-case charge (scans, score requests, archive memory, measured-score preflight time) grows by at most the factor
  (ℓ_n + 2K + 1)/(ℓ_n + K + 1) ≤ 2; this is an upper-bound statement about LS0's worst-case terms, not about total fit
  time. For cap rules with a ≥ ℓ_n + |S̃₀| (all three examples of (P4)(iii)), realised LS0 work is identical wherever the
  MR1 search already ends certified (Lemma CAP(a)); for smaller admissible rules (e.g. max(ℓ_n, ⌈1.001|S̃₀|⌉)) this identity is
  false in general (R02 item 2: N1 row n = 600, p = 360, seed 0) [R02-2].
* **(P6) Full method (numerical; pending) [R01-8].** Whether the production fit under MR1 reports S₀ on these designs:
  local attempts did not complete (the merged preflight charges LS0's worst case at ≈ 1.5·10² h for n = 600, p = 450,
  so the 2 h attempts returned `resource_limit` before any SMC — the same charge would also reject 24 h, an extrapolation,
  not an observed run; a 1000 h attempt timed out after a 20-min wall clock) [R07-5] — numerics/full_method/NF_summary.md. Completed runs are requested from W2-SIM (R2). No claim is made
  until completed, attributable runs exist; no full-method theorem is claimed.

## 4. Not claimed

Finite-n bounds; p ≫ n or any non-exact-Gram design; (P2) for K < p ≤ (16/15)K; an exact description of the LS0 path
(swap count W, phase structure); optimality of any cap; SMC discovery; S5, general loadings, k ≥ 2.

## 5. Open deliverables (frontier)

(F1) p ≫ n (iid rows or other designs): NEG mechanism and cap question — W2-SIM R3 + heuristics in REPORT.
(F2) (P2) for K < p ≤ (16/15)K; (F2′) (P1), (P3), (P4) for K < p < K + 16s₀ + 1 (start possibly unsaturated). (F3) The full-method question (P6). (F4) Generalisation to the W2-UNI assumptions
(design-agnostic ingredients listed in REPORT.md).

## 6. Dependencies (statuses verbatim)

FACB L1 (closed forms; FACB reviews/R03_L1L2L3_check_sol.md VERIFIED-WITH-AMENDMENTS), FACB L2.1–L2.3 (block
increments; same R03), FACB L4.0(d) — only its small-energy refinement M_T ≤ ½(1 + C/log n) when Σ_Tξ² + kL_n² ≤ n/log n,
not its p ≤ n/2 bulk bound — and L4.0(e) (truth moves) (FACB reviews/R04_L4_check_sol.md VERIFIED-WITH-AMENDMENTS),
FACB L5.1/L5.4 (FACB reviews/R05_L5_check_sol.md VERIFIED-WITH-AMENDMENTS); FAC-CS council round 1 passed; [M5-0] T38-(0) "PROVED (SF: VERIFIED (W3-VT38E);
XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat,
unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma CAP "PROVED (by this seat)", council-checked; Proposition F
(A1 corrected statement; A2 "PROVED (A2), checked by A3"; A4 "OK-WITH-FIXES").
