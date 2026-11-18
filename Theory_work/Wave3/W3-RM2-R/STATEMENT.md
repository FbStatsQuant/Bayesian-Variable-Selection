# W3-RM2-R — STATEMENT v1.0 LOCKED (delta over W3-RM2 v1.4 and W3-RM RM-0: constant-level signals, the mode interface, delivery)

Ticket W3-RM2-R (Tier B rider), Theory Wave 3. Lead: Claude Opus 5.5 (Claude Third, effort high). Protocol:
`Theory_work/Wave3/PROTOCOL_v4.md` with `RIDER_RULES.md` of this folder. Status of this file: **v1.0 LOCKED** (2026-11-15) = v0.2 with the five findings of the statement-change
check SC1 applied (`reviews/SC1_statement_change_sol.md`: ACCEPT WITH CHANGES; markers [SC1-#]; `reviews/SC1_disposition.md`).
v0.2 = v0.1.1 with the five
findings of statement-lock review SL1 applied (`reviews/SL1_statement_lock_sol.md`: DO NOT LOCK; disposition
`reviews/SL1_disposition.md`; markers [SL1-#]); v0.1.1 = v0.1 with the C-DLV law-free inputs listed in (C-D) after R-AUD1. All results are asymptotic (n → ∞) unless marked *deterministic*.

**This is a delta statement.** PARENT := `Theory_work/Wave3/W3-RM2/` (STATEMENT v1.4, recorded on main);
RM := `Theory_work/Wave3/W3-RM/` (STATEMENT v1.2.1; claim W3-RM:RM-0@1.0.0 at RM `STATEMENT.md:160-176`).
This file states **in full** every definition, hypothesis and claim that differs from PARENT v1.4 and from RM-0, and
takes everything else from them by `file:line`. It **asserts no proof status**: proofs go in `lemmas/` (plan:
`PLAN.md`); statuses are recorded outside this file. **No method change is requested.**
Other abbreviations as PARENT `STATEMENT.md:27-29`; DLV = `Theory_work/Wave1C/C-DLV/`; FACA = `Theory_work/Wave2/W2-FAC-A/`;
POST = `Theory_work/Wave3/W3-POST/`.

## 0. What changes, in one table

| target | claim of this file (new id) | replaces / extends | what is gained |
|---|---|---|---|
| T2(b), T2(c) | **RM0-plus** (§3) | RM-0 (RM `STATEMENT.md:160-176`) | the posterior input {π(S₀) > ½} becomes the mode event {S₀ is the unique F-maximiser on Ω}; [POST] ⇒ [MODE] by Markov; the error splits into mode failure + search failure; RM-0(a) on any down-closed sub-lattice |
| T2(a) | **DLV-0** (§3) | DLV Theorem D + Proposition F (DLV `lemmas/L4_delivery.md:13-22, 79-91`), W2-UNI:F-UNI Step 2, as shipped | a *deterministic* delivery statement: every valid non-degenerate input and every seed returns output; no data law, no design class |
| T4, T2 | **RM2-F-plus** (§4) | RM2-F (PARENT `STATEMENT.md:206-214`) | (V) with a fixed constant M_V > M_V⁰ instead of M_n → ∞; beta-min of Theorem 1 at the constant level BM(c); the truth-removal floor in additive form at the constant level (BM-W⁺) instead of the ratio → ∞ of (BM-W); conclusion P(Ŝ⁺ = S₀) → 1 without "on output" (under the delivery premises), error = mode failure + search failure |
| T2 | **RM2-R-plus** (§4) | RM2-R (PARENT `STATEMENT.md:216-218`) | same conclusion change; no hypothesis changes |
| T4 | **SAND-F-c**, **TL-F-c** (§4, bridges) | PARENT bridges (P1), (P2) (`STATEMENT.md:248-249`) | the sandwich under (V♭); truth removal under (BM-W⁺) |
| T4 | **Ex-Proxy-d** (§5) | Ex-Proxy (PARENT `STATEMENT.md:265-267`; `lemmas/L6_examples.md:330-384`) | decaying signal θ_n; d_n = O(1); the first witness that (BM-W) is strictly weaker than (BM-Q) |
| — | **Cont-plus** (§6) | — | every hypothesis of RM2-F (resp. RM2-R, RM-0) implies the corresponding one here; every conclusion there is a conclusion here |

Not targeted in this file (named open items, PLAN §4): the quantile form of (W) (PARENT `lemmas/L2_width.md:77-86`);
the equicorrelated threshold b = 3/8 and its converse (O4′); the aggregated Form R leak; T6 (already in PARENT v1.4).

## 1. Base (taken unchanged)

* Settings F and R, method objects, the events Sand_n(Q), NA(𝓛), TL(𝓛), 𝒦_n, 𝒪, U_n, Ŝ⁺, implementation premises
  (EX-A, EX-S, SR, GUARD-W, OP-LS0, complete scans), the configuration (`ls0 = TRUE`, `ls0_ell = ℓ_n`,
  `ls0_cap = "ell_n_plus_mode"`, `ls0_tie_dp = TRUE`), "admissible run": RM `STATEMENT.md:32-68` as imported by
  PARENT `STATEMENT.md:47-58`.
* Code pins of PARENT `STATEMENT.md:60-68` (LS0 centre, scan, stop rules; Lemma E4 = W3-RM:E4@1.0.0); the pins are
  re-read against the core as on this branch (commit 2aeb860; `Scripts/SMC_BVS/core/` last changed at 72785fe) in the
  lemma files; any difference is reported, not assumed away.
* Notation and functionals: PARENT `STATEMENT.md:70-94` — q, 𝓛, 𝔓, β_{B,l}, β(η, A), a⁰_n, 𝔴⁰_n, 𝔴_n(δ), 𝒟ᵀ_n,
  **d_n := E max_{v∈𝒟ᵀ_n}|vᵀg|**; and **λ_n := (n − 1)φ₀²θ*²_min/σ²** (PARENT `lemmas/L2_width.md:185`).
* Interface properties [SAND(Q)], [TL(Q)], [NA(Q)], [POST], [E4]: PARENT `STATEMENT.md:96-104`.
* Assumptions of PARENT §3 not named in §2 below, unchanged: (FL) = (FL-16) + (FL-Q), (L^b) = (L-size^b) + (L-feas) +
  (L-gain) with b < β(η, A), (W) and its sufficient forms, the block-relative forms (PARENT `STATEMENT.md:128-171`,
  except (V), (T1-F), (BM-W)); all of Form R (PARENT `STATEMENT.md:172-202`); the constants of PARENT
  `STATEMENT.md:112-124`.
* **The toolkit constant.** C_R := 3(M + σ²) (PARENT `lemmas/L0_toolkit_b.md:38`), where M is the energy constant of
  (T1-F) (‖μ‖² ≤ Mn).

## 2. Definitions and hypotheses that change

**New event and interface property (T2(b)).** For n with s₀ ≤ K:
  **𝓜_n := {S₀ is the unique maximiser of F on Ω}** (F(S) = log w(|S|) + log m(S), RM `STATEMENT.md:34-37`),
a data event; and
| id | property | consumed by |
|---|---|---|
| [MODE] | P(𝓜_n) → 1 | RM0-plus |
Since π(S) ∝ exp F(S) on Ω, {π(S₀) > ½} ⊆ 𝓜_n; hence P(𝓜_nᶜ) ≤ 2E[1 − π(S₀)] and **[POST] ⇒ [MODE]**.

**Sub-lattice events (T2(c)).** For a deterministic family 𝓛′ ⊆ 𝓛 (𝓛 = {T : S₀ ⊆ T ⊆ Q}, Q ⊇ S₀ deterministic,
|Q| ≤ K) that is **down-closed in 𝓛** (T ∈ 𝓛′ and S₀ ⊆ T′ ⊆ T imply T′ ∈ 𝓛′):
NA(𝓛′) := {F(T ∪ {l}) < F(T) for all T ∈ 𝓛′ with |T| < K and all l ∉ T};
TL(𝓛′) := {F(A) < F(T) for every T ∈ 𝓛′ and every feasible neighbour A of T with S₀ ⊄ A};
St_n(𝓛′) := {S̃₀ ∈ 𝓛′}, S̃₀ the coded start mode (a function of the data, W3-RM:E4@1.0.0) [SL1-3]; sufficient:
Sand_n(𝓛′) := {S̃ ∈ 𝓛′ for every maximiser S̃ of γ₀ on Ω} ⊆ St_n(𝓛′) (E4: S̃₀ is a maximiser). Since 𝓛′ ⊆ 𝓛 and 𝓛′ is
down-closed, St_n(𝓛′) = {S₀ ⊆ S̃₀} ∩ {[S₀, S̃₀] ⊆ 𝓛′} (the BRIEF's form, with truth inclusion made explicit) [SC1-1]. (With 𝓛′ = 𝓛:
NA(𝓛), TL(𝓛), and Sand_n(Q) ⊆ St_n(𝓛).)

**Delivery premises (D) (T2(a)).** In addition to the implementation premises and configuration of §1:
**IDEAL-W⁺** (below), EX-A as a unit-cost model, MACH(τ, τ₀, β, β₀), CONFIG and TDP-IMPL exactly as in DLV
`STATEMENT.md:21-42` [SL1-5],
with CONFIG read at the shipped configuration (the configuration of §1, the tier-1 grid fallback
`grid_fallback = TRUE`, its default under `ls0 = TRUE`, `Scripts/SMC_BVS/core/v3_calib.R:141-144`, `v3_fit.R:151`;
declared R′ = 4k with k fixed; fixed worker count; default 𝓗 list), and the **declared allocation** 𝒜_n: `allocation$mem_gb`
and `allocation$hours` at least the polynomial envelopes of DLV Corollary R (DLV `lemmas/L1_resources.md:129-143`)
re-derived for the shipped code — LS0 cap ℓ_n + |S̃₀| (at most ℓ_n + K + 1 scans of ≤ p + p²/4 score requests each) and
the shipped preflight charge — evaluated at (n, p_raw). CAL is not assumed.
**IDEAL-W⁺ [SL1-2, SC1-2].** DLV's IDEAL-W (DLV `STATEMENT.md:24`) plus the lift of **exactly two upper-bound
predicates**, which are treated as true: (i) `le > 1e6` in the LS0 base-cap validator (`Scripts/SMC_BVS/core/v3_run.R:96`;
with le = ℓ_n = ⌈log₂(n + p + 1)⌉ in the configuration of §1, it would fire once n + p + 1 > 2^{10⁶}); (ii)
`cap_ll > numeric_limits<int>::max()` in the LS0 cap-range guard (`cpp/v3_core.cpp:474`), with `int` read as unbounded.
Every other part of those two validators (type, length, finiteness, integrality, lower bounds) and every other
validator, enumeration cap, fallback and method cap of the code is kept as coded. **Without the lift** (DLV's IDEAL-W
only), DLV-0 holds on the **sufficient domain** 𝔇 := {⌈log₂(n + p_raw + 1)⌉ ≤ 10⁶ and ⌈log₂(n + p_raw + 1)⌉ + ⌊n/2⌋ ≤
2³¹ − 1} (it implies ℓ_n ≤ 10⁶ and ℓ_n + |S̃₀| ≤ 2³¹ − 1, since p ≤ p_raw and |S̃₀| ≤ K ≤ ⌊n/2⌋; the exact branch
does not reach either guard), with all other premises of (D) retained. 𝔇 is bounded, so the asymptotic conclusions
of (c⁺), (C1⁺), (C2⁺) are stated under IDEAL-W⁺, an idealisation of the same kind as EX-A [SC1-3].
**Valid non-degenerate input [SL1-1]:** n ≥ 3; X^r a finite numeric n × p_raw matrix with at least one non-constant
column; y^r a finite numeric vector **of length n** (no dim attribute) that is not constant; a **scalar** seed, a whole
number in [1, 2³¹ − 1]; an allocation that is a list with scalar finite positive `mem_gb`, `hours` — i.e. no input
validator fires (`v3_fit.R:88-94`, `v3_preprocess.R:7-11, 97-115`; DLV `STATEMENT.md:43-44` [SL1-5]).

**(T1-F♭) Theorem 1's conditions at the constant beta-min level (T4).** (H0) of GROW (GROW `STATEMENT.md:84-88`, as
quoted at RM `STATEMENT.md:91-92`) with BM-∞ replaced by **"BM-∞, or BM(c): θ*²_min ≥ cσ² log n/(nφ₀²) for a fixed
c > c₀(s₀, A) := max{4C_*, 32[s₀(A + 1) + 2]}"** (C_* the T03 proof constant). This is the hypothesis list of
SOP:TH09@1.0.0 itself (card `Theory_work/State_of_Project/sections/04_theory.tex:785-788`; restated at POST
`STATEMENT.md:58-75`). (T1-F) ⇒ (T1-F♭).

**(V♭) Visibility at a constant level (T4).** There is a fixed **M_V > M_V⁰ := (σ√(2A) + √((2A + 1)C_R))²** such
that for n ≥ n₀, every j ∈ S₀ and every U ⊆ [p] ∖ {j} with |U| ≤ 15: δ²_{U,j} ≥ M_V log n.
Block-relative form (V_b♭): the same only for U ⊆ C_{b(j)} ∖ {j}. (V) ⇒ (V♭) and (V_b) ⇒ (V_b♭) (M_n → ∞ exceeds any
fixed level eventually). M_V⁰ ≤ 4Aσ² + 2C_R(2A + 1); both sides scale like σ² under Y ↦ aY (PARENT
`STATEMENT.md:118-124`), so the condition is scale-free.

**(BM-W⁺) Truth-removal floor, additive form at the constant level (T4).** For n ≥ n₀:
  √λ_n ≥ 2(d_n + √(2 log n))   and   λ_n ≥ c_TL log n   for a fixed **c_TL > c_TL⁰ := 8(A + 1) + 4(2A + 1)C_R/σ²**.
(BM-W) ⇒ (BM-W⁺): (2(d_n + √(2 log n)))² ≤ 16(d_n² + log n). Sufficient: λ_n ≥ max{c_TL log n, 16(d_n² + log n)}; and,
by d_n² ≤ 2(q + 1) + 4 log(2p) (PARENT `lemmas/L2_width.md:187-188`), **(BM-Q♭)**: λ_n ≥ 32(q + 1) + 64 log(2p) +
max{c_TL, 16} log n. When d_n² ≤ D log n for a fixed D, (BM-W⁺) holds as soon as λ_n ≥ max{c_TL, 8(1 + √(D/2))²}·log n
for large n, a BM(c) condition.

All other hypotheses are PARENT's, unchanged.

## 3. Claims on the core and on delivery (T2)

**(C0⁺) Theorem RM0-plus (core; any design; deterministic statement plus one inequality).** Let Q ⊇ S₀ be
deterministic with |Q| ≤ K. Under the implementation premises and configuration of §1 and the hypotheses of Lemma E4:
(a) RM-0(a) as stated at RM `STATEMENT.md:162-167` (unchanged).
(a′) [T2(c)] For every deterministic 𝓛′ ⊆ 𝓛 down-closed in 𝓛: on St_n(𝓛′) ∩ NA(𝓛′) ∩ TL(𝓛′) [SL1-3], LS0 from the coded
start mode S̃₀ performs exactly |S̃₀ ∖ S₀| moves, each deleting one element of S̃₀ ∖ S₀, visits only sets T with
S₀ ⊆ T ⊆ S̃₀ (all in 𝓛′), and ends at S₀ with a completed scan that finds no strict improvement; the cap ℓ_n + |S̃₀| is
not binding; the archive statement of RM-0(a) holds. Hence 𝒦_nᶜ ⊆ St_n(𝓛′)ᶜ ∪ NA(𝓛′)ᶜ ∪ TL(𝓛′)ᶜ, and
St_n(𝓛′) may be replaced by its sufficient form Sand_n(𝓛′).
(b⁺) [T2(b)] For n with s₀ ≤ K, pathwise, for every admissible run (every seed, N_e, R′ and calibration outcome):
  𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ,
a data event. With 𝒢⁺_n := 𝓜_n ∩ 𝒦_n, every admissible output run reports Ŝ⁺ = S₀ on 𝒢⁺_n, and
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝒢⁺_nᶜ) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ),  P(𝓜_nᶜ) ≤ 2E[1 − π(S₀)],
  P(𝒦_nᶜ) ≤ P(St_n(𝓛′)ᶜ) + P(NA(𝓛′)ᶜ) + P(TL(𝓛′)ᶜ) for every 𝓛′ as in (a′) (in particular 𝓛′ = 𝓛),
uniformly over the run parameters. Under [MODE] and P(St_n(𝓛′) ∩ NA(𝓛′) ∩ TL(𝓛′)) → 1 for some such 𝓛′ (in
particular under [SAND(Q)], [NA(Q)], [TL(Q)]): P(𝒢⁺_n) → 1 and P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1). On enumeration
branches 𝒦_n refers to the hypothetical search, and there 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ. RM-0(b) is the special case that
uses {π(S₀) > ½} ⊆ 𝓜_n.
(c⁺) [T2(a) + (b)] Assume in addition the delivery premises (D). Then for every valid non-degenerate input every
admissible run returns output (DLV-0), so for every admissible run
  {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ  on the set of valid non-degenerate inputs,
and, for any law of the data under which the input is valid and non-degenerate with probability one,
  P(Ŝ⁺ ≠ S₀) ≤ P(𝓜_nᶜ) [mode failure] + P(𝒦_nᶜ) [search failure],
uniformly over seeds, N_e, R′ and calibration outcomes; under the conditions of (b⁺), P(Ŝ⁺ = S₀) → 1, without
"on output". Under Setting F (fixed standardised X with non-constant columns, model G) and Setting R the input is
valid and non-degenerate with probability one.

**(C-D) Lemma DLV-0 (deterministic delivery).** Under the implementation premises and configuration of §1 and the
delivery premises (D): for every valid non-degenerate input, every seed and every realisation of the method's
uniform streams, the coded fit (`v3_fit`, core as pinned in §1) returns with `estimates_available = TRUE`; without
the representability lift of IDEAL-W⁺, the same holds for every such input in the supported domain 𝔇 of §2. No data
law, no model and no design class enters. DLV-0 is a delivery statement only; it asserts nothing about Ŝ⁺.
**Law-free inputs, cited (and only these):** the exit walk of Theorem D (DLV `lemmas/L4_delivery.md:13-42`), in which the
data law enters only through Lemma S.1's null sets for A3–A5 (`lemmas/L2_degenerate.md:5-18`) — replaced here by the
deterministic "valid non-degenerate input" condition; Lemma S.2 (scorer never fails under EX-A, for every input with
yᵀy > 0; `L2_degenerate.md:20-35`); Lemma S.3 and the P1 inventory (AUDITED, code reading); Lemma R and Corollary R
("for every valid input, every seed and every realisation", `lemmas/L1_resources.md:70-81, 129-143`); grid Lemmas 3.3,
3.4 (`lemmas/L3_grid.md:30-56`); and the **delivery half only** of Proposition F, in the restated form of
`Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md:32-35` ("Under the premises of Theorem D, P(𝒰_n) = 0 for every
n ≥ 3"). The standalone sentence of DLV `lemmas/L4_delivery.md:83-84` ("on the classes above … P(Ŝ⁺ = S₀) → 1
unconditionally") is **not** consumed: it imports Corollary D′'s statistical hypotheses (HQ disposition,
`API_AUDIT/pass1/TRIAGE.md:23-28`). Consistency in this file comes only from RM0-plus (b⁺)/(c⁺) with [MODE] and the
lattice properties as explicit hypotheses. Templates (no conclusion consumed beyond their delivery step): FACA
`lemmas/L7_delivery.md` Step 2, W2-UNI `lemmas/L5_delivery.md` Step 2. The proof re-audits the exit walk, the
fallback and the resource bounds against the code as pinned. **Scope note:** DLV-0 refers to the core as pinned; Lemma R (DLV `lemmas/L1_resources.md:70-81`) and the
allocation 𝒜_n must be re-audited when v3.2 freezes (the preflight charge changes).

## 4. Claims on the reported model (T4, T2)

**(C1⁺) Theorem RM2-F-plus (fixed design, polynomial leakage, constant-level signals).** Setting F, the method as
coded, premises and configuration of §1. Assume (T1-F♭), (FL), (V♭), (L^b) with b < β(η, A), (BM-W⁺) and (W).
Then [SAND(Q)], [TL(Q)], [NA(Q)], [POST] and [MODE] hold, hence all conclusions of RM0-plus (a), (b⁺) with 𝓛′ = 𝓛:
there is a data event 𝒢⁺_n = 𝓜_n ∩ 𝒦_n with P(𝒢⁺_n) → 1 on which every admissible output run — every seed, N_e, R′
and calibration outcome — reports Ŝ⁺ = S₀; P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) → 0; on
Sand_n(Q) ∩ NA(𝓛) ∩ TL(𝓛) LS0 makes exactly |S̃₀ ∖ S₀| ≤ n^b moves, all deletions of extras, with the archive
statement of RM-0(a) and a non-binding shipped cap. **Under in addition the delivery premises (D)** (RM0-plus (c⁺)):
every admissible run returns output and **P(Ŝ⁺ = S₀) → 1** for every seed, N_e, R′ and calibration outcome, with
P(Ŝ⁺ ≠ S₀) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ). The same holds with (V♭), (L-gain), (FL-16) replaced by (V_b♭), (L_b), (FL_b) on the
method's partition.

**(C2⁺) Theorem RM2-R-plus (Gaussian rows, polynomial leakage).** Setting R, the method as coded, any X-measurable
partition with blocks ≤ 16. Assume the hypotheses of RM2-R (PARENT `STATEMENT.md:216-218`: (T1-R), (FL-R), (V-R),
(L-R^b) with 15ρ + b < ½, (W-R)). Then, under the joint law of (X, ε): [SAND(Q)], [TL(Q)], [NA(Q)], [POST], [MODE],
hence all conclusions of RM0-plus (a), (b⁺) as in (C1⁺); under in addition (D), every admissible run returns output
and P(Ŝ⁺ = S₀) → 1 with P(Ŝ⁺ ≠ S₀) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ).

**Bridge lemmas** (each delivers one interface property under the changed hypotheses; "copy" = the PARENT lemma
copied into `lemmas/` with changed lines marked [R-#]):

| id | statement | source | change |
|---|---|---|---|
| (Q1) SAND-F-c | PARENT bridge (P1) (`STATEMENT.md:248`) with (V_b♭) in place of (V_b): (S0), (S1), (G3a), (V_b♭), (L_b), (L-feas), \|Q\| ≤ n^b, b < β(η, A) ⇒ [SAND(Q)] | PARENT `lemmas/L1_sandF_b.md` (copy) | Step 2(a) only: (δ_{U,j} + σZ_{U,j})² ≥ (√(M_V log n) − σz_n)² and the margin (√M_V − σ√(2A))²/(2C_R) − (A + ½) > 0 |
| (Q2) TL-F-c | PARENT bridge (P2) (`STATEMENT.md:249`) with (BM-W⁺) in place of (BM-W): (P0) for the lattice family, (FL-Q), (BM-W⁺), \|Q\| ≤ K, P(𝒵_n) → 1 ⇒ [TL(Q)] | PARENT `lemmas/L2_width.md` §4 (copy) | the two "n ≥ n₀ (λ_n/log n → ∞)" steps become the explicit inequalities of (BM-W⁺) |
| (Q3) POST/MODE-F | (T1-F♭) ⇒ [POST], [MODE] | SOP:TH09@1.0.0 (BM(c) branch; POST `STATEMENT.md:80-82` items 1–2) | input re-read at the BM(c) branch; [MODE] by Markov |
| (Q4) core | RM0-plus | RM `lemmas/L0_core.md` (copy); GROW `lemmas/L1_descent.md:20-57` | (a′): L1.1–L1.2 use NA and TL only at the visited sets C, C ∖ {e}; (b⁺): the proof of RM-0(b) uses π(S₀) > ½ only through "F(S₀) > F(S) for S ≠ S₀"; (c⁺): DLV-0 |
| (Q5) DLV-0 | claim (C-D) | DLV Theorem D, Proposition F, Lemma S (S.1–S.3), Corollary R; FACA L7 Step 2; C-ENG:Impl-DLV-B, Impl-DLV-A2, Impl-GROW-MR1 | deterministic input conditions in place of model G; code re-audit at the pin |
| (Q6) assembly | (C1⁺), (C2⁺) | PARENT `lemmas/L3_assemblyF.md`, `lemmas/L5_formR.md` (copies) | inputs (Q1)–(Q5); Form R hypotheses and bridges unchanged |

## 5. Example (T4)

**(C5⁺) Ex-Proxy-d (one truth with n^b weak proxies, decaying signal).** The design of PARENT `lemmas/L6_examples.md:334-347`
(0 < b < ½, p = ⌊n/3⌋, q = ⌊n^b⌋, r² = C₀ log n/n, S₀ = {1}, Q = {1, …, q}, φ₀² = ½, A = 1), with μ = θ_n x₁ for a
deterministic sequence θ_n ≠ 0, |θ_n| ≤ θ_hi:
(a) d_n ≤ √(2/π)(1 + r(q − 1))/√(1 − r²) → √(2/π); in particular d_n = O(1).
(b) If nθ_n²/log n → ∞, every hypothesis of RM2-F (PARENT v1.4) holds, with (BM-W) and η = 0; (BM-Q) holds if and only if
n^{1−b}θ_n² → ∞. In particular θ_n² = (log n)²/n satisfies (BM-W) and violates (BM-Q).
(c) If liminf nθ_n²/(σ² log n) > κ₀ := 2 max{c₀(1, 1), c_TL⁰, M_V⁰/σ²} (constants of §2 at A = 1, s₀ = 1,
M = θ_hi² + 1), every hypothesis of RM2-F-plus holds, with BM(c) and (BM-W⁺) at the constant level.

## 6. Containment and dependencies

**(C4⁺) Cont-plus.** (i) The hypotheses of RM2-F (PARENT `STATEMENT.md:206-207`) imply those of RM2-F-plus, and the
conclusions of RM2-F are among those of RM2-F-plus; so RM2-F-plus ⇒ RM2-F. (ii) RM2-R-plus ⇒ RM2-R (same hypotheses;
conclusions contain RM2-R's). (iii) RM0-plus ⇒ RM-0 ((a) unchanged; (b) is (b⁺) with {π(S₀) > ½} ⊆ 𝓜_n). (iv) Through
PARENT (C4) (`STATEMENT.md:236-240`), RM2-F-plus ⇒ W3-RM:RM-F and RM2-R-plus ⇒ W3-RM:RM-R. (v) Ex-Proxy-d(b) with
θ_n ≡ θ is PARENT Ex-Proxy's verification.

### Dependencies and supersession

| new claim | ⇒ parent claim | why (one line) |
|---|---|---|
| W3-RM2-R:RM0-plus | W3-RM:RM-0@1.0.0 | {π(S₀) > ½} ⊆ 𝓜_n; (a) identical; (a′) with 𝓛′ = 𝓛 recovers (a) using Sand_n(Q) ⊆ St_n(𝓛) [SC1-4] |
| W3-RM2-R:DLV-0 | **no registry implication edge** [SL1-4]; it *recovers the delivery conclusion* of C-DLV:Prop-F@1.0.0 (R-AUD1 restatement, first sentence) and of W2-UNI:F-UNI@1.1.0 Step 2 **under (D)** | the method differs from Prop F's (LS0 cap ℓ_n + \|S̃₀\| instead of ℓ_n; allocation re-derived for that cap and the shipped preflight; IDEAL-W⁺), so it is not an implication of the registered parent; every input ⇒ almost every input for the delivery half; Prop F's consistency sentence is neither implied nor consumed |
| W3-RM2-R:RM2-F-plus | W3-RM2:RM2-F@1.0.0 | (T1-F) ⇒ (T1-F♭), (V) ⇒ (V♭), (BM-W) ⇒ (BM-W⁺); conclusions ⊇ |
| W3-RM2-R:RM2-R-plus | W3-RM2:RM2-R@1.0.0 | same hypotheses; conclusions ⊇ |
| W3-RM2-R:SAND-F-c | W3-RM2:SAND-F-b@1.0.0 | (V_b) ⇒ (V_b♭) |
| W3-RM2-R:TL-F-c | W3-RM2:TL-F-b@1.0.0 | (BM-W) ⇒ (BM-W⁺) |
| W3-RM2-R:Ex-Proxy-d | W3-RM2:Ex-Proxy@1.0.0 | θ_n ≡ θ is a special case of (b) |
| W3-RM2-R:Cont-plus | W3-RM2:Cont-F@1.0.0, W3-RM2:Cont-R@1.0.0 | composes with them |

**Consumed** (registry id@version; statuses verbatim; PROTOCOL_v4 §6): PROVED-CHECKED — W3-RM:RM-0@1.0.0,
W3-RM:E4@1.0.0, W3-RM2:RM2-F@1.0.0 and W3-RM2:RM2-R@1.0.0 ("PROVED-CHECKED, conditional on SOP:TH09" resp. "… on
W2-APP:POST"), W3-RM2:Toolkit-b, SAND-F-b, TL-F-b, NA-W, W-suff, SAND-R-b, F-to-R, D-to-W, POST-R @1.0.0;
C-DLV:Thm-D@1.0.0 ("PROVED-CHECKED (relative to the P1/P3 audits)"), C-DLV:Prop-F@1.0.0 ("PROVED-CHECKED for the patched
calibration law (R04; council round 2)"), C-DLV:L1-R@1.0.0, C-DLV:Cor-R@1.0.0, C-DLV:L2-S1@1.0.0, C-DLV:L2-S2@1.0.0,
C-DLV:L3-3.3@1.0.0, C-DLV:L3-3.4@1.0.0, W2-UNI:F-UNI@1.1.0 ("PROVED-CHECKED"). AUDITED (code reading) — C-DLV:P1-Inventory,
C-DLV:L2-S3 (carried as audits). Below PROVED-CHECKED — **explicit conditions, carried into the statuses**:
SOP:TH09@1.0.0 (status as PARENT `STATEMENT.md:298-300`) for (C1⁺) and Ex-Proxy-d; W2-APP:POST@1.0.1 for (C2⁺);
the C-ENG implementation records C-ENG:Impl-DLV-B, Impl-DLV-A2, Impl-GROW-MR1 ("DONE (implemented, tested, …)") and
C-ENG:TDP_E ("PROVED (by this seat, unchecked)") — used only as pointers to the code; DLV-0 re-reads the code itself.
Implementation premises (named, not proved): §1 and (D).

## 7. Not claimed

* Anything about the posterior beyond [POST]/[MODE] as inputs; mode consistency under weaker conditions than (T1-F♭)
  (the interface [MODE] accepts any such result, none is supplied here).
* Sharpness of M_V⁰, c_TL⁰, c₀ or κ₀ (proof constants); necessity of (V♭), (BM-W⁺) for the conclusion.
* Delivery outside (D): binary64 arithmetic, interrupted or resource-limited runs, user-declared 𝓗 functions,
  `grid_fallback = FALSE` or `ls0 = FALSE`, versions of the core other than the pin (v3.2 included).
* Everything PARENT §6 does not claim (`STATEMENT.md:313-330`), except that delivery is now claimed under (D).
* RM-F, RM-R are not restated; their conclusion change follows through Cont-plus (iv) only at the level of RM2's
  hypotheses.

## Changelog (after the lock; PROTOCOL_v4 §4.2)

| version | clause | STRONGER / WEAKER / EQUAL / NEW-CLAIM | reason | trigger (review file) | check (review file) |
|---|---|---|---|---|---|
| v0.1 | all | — | draft for the statement lock | — | — |
| v0.1.1 | (C-D), dependency row DLV-0 | EQUAL | consumed C-DLV steps listed; Prop F consistency sentence excluded (manager input, R-AUD1) | `Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md` | SL1 disposition |
| v0.2 | valid non-degenerate input | WEAKER (narrower input domain) | SL1-1 | `reviews/SL1_statement_lock_sol.md` | `reviews/SC1_statement_change_sol.md` |
| v0.2 | IDEAL-W⁺ in (D); delivery in (C-D), (c⁺), (C1⁺), (C2⁺) | WEAKER (added idealisation) | SL1-2 | `reviews/SL1_statement_lock_sol.md` | `reviews/SC1_statement_change_sol.md` |
| v0.2 | delivery on 𝔇 without the lift | NEW-CLAIM | SL1-2 | `reviews/SL1_statement_lock_sol.md` | `reviews/SC1_statement_change_sol.md` |
| v0.2 | (C0⁺)(a′) with St_n; (b⁺) search bound and criterion | STRONGER | SL1-3 | `reviews/SL1_statement_lock_sol.md` | `reviews/SC1_statement_change_sol.md` |
| v0.2 | (b⁺) pathwise inclusion; (C-D) law-free inventory; output-conditional parts of (C1⁺)/(C2⁺); pointers | EQUAL | SL1-5, R-AUD1 | `reviews/SL1_statement_lock_sol.md` | `reviews/SC1_statement_change_sol.md` |
| v0.2 | DLV-0 dependency row | WEAKER (implication edge withdrawn) | SL1-4 | `reviews/SL1_statement_lock_sol.md` | `reviews/SC1_statement_change_sol.md` |
| v1.0 | St_n interval identity (truth inclusion explicit); IDEAL-W⁺ closed to two predicates; 𝔇 labelled sufficient; RM0 dependency wording; pointers | EQUAL (corrections of v0.2 text; the interval identity is now the reviewer's corrected form) | SC1 findings 1–5 | `reviews/SC1_statement_change_sol.md` | applied verbatim from SC1's fixes; LOCK |
