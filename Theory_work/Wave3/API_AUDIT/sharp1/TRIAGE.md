# sharp1 — triage of the 13 completed sharpness verdicts

Author: HQ consultant (Fable 5.2, high), 2026-11-11. Read-only triage; no agents, no commit (HQ commits).
Inputs: `sharp1/results/f01,f03–f07,f09,f10,f14–f17.md`, the cited lemma files, and the later statements
`Wave3/W3-POST2/STATEMENT.md` (v1.2.1), `Wave3/W3-RM/STATEMENT.md` (v1.2.1), `W3-RM/SHARPNESS.md`,
`BVS-wt/W3-RM2/.../STATEMENT.md` (in progress), `Wave3/W3-POST/REPORT.md` §4, `Wave3/PROGRAM.md` (stop list, tie-break).

Classes: **A** real and cheap, worth a ticket · **B** real but already known, superseded or out of scope
(**B\*** = known and still undone, cheap enough to ticket) · **C** wrong, or not an improvement (cosmetic).

## 0. Why all 13 say IMPROVABLE-EASY

Not noise, but not 13 findings either.

1. **The scale forces it.** `SYSTEM_SHARP` defines IMPROVABLE-EASY as "a stronger version follows with a modest change
   you can describe". Every statement admits some restatement (drop a redundant premise, state the inequality the proof
   already gives), so the verdict fires on cosmetics. No review found the *core* of a claim cheaply improvable; each
   says the hard restrictions (fixed s₀, p ≤ n^A, Gaussian noise, lattice size, exponents) need new work.
2. **Each request saw one ticket.** The reviewer cannot see later tickets, so it re-proposes what Wave 3 already did:
   8 of 13 verdicts are mostly B for that reason.
3. **The reviews are good.** I found no wrong mathematical proposal in the steps I checked (list in §3).

Fix for sharp1b: (i) ask for the verdict on the *best single* improvement and its kind
(hypothesis / range of p / rate / constant / restatement — the PROGRAM tie-break order); (ii) give the supersession
map (`implies`, `superseded_by`, and each ticket's "what could be strengthened" list) in the user message; (iii) add a
verdict RESTATE-ONLY for "the proof already gives more than the statement says".

## 1. Per-claim triage

| # | claim | class | reason (proposal → disposition) |
|---|---|---|---|
| 1 | W1-N1:Thm-N1 (f01) | **B** (park) | Generality only (drop B_h; condition on all calibration streams V, or on (V, U_{−r}) under IND-T; all post-terminal populations; KERNEL reduced to invariance + state-independent order). Real, about a day. Out of scope for the Wave 3 package (stop list: no M1(i) stacking work); it is exactly what the scaling design's obligations O1/O3 need (merge consistency, census inside 𝒞). **Hand f01 to the track-3 lead; no ticket now.** `R′ = 4k`: C (cosmetic). |
| 2 | C-DLV:Prop-F (f03) | **A** (delivery half) / B (consistency half) | Delivery is a *sure* statement: the data law enters Theorem D only through Lemma S.1 (A3–A5 null), and Lemma R holds "for every valid input, every seed and every realisation" (checked: `L4_delivery.md:24-26`, `L2_degenerate.md:5-17`, `L1_resources.md:70-72,110-113`). So model G and the class restrictions can go → ticket T2(a). Consistency half (pathwise in seeds, explicit inequality): B, superseded by W3-RM:RM-0(b). "Mode suffices instead of π(S₀) → 1": A → T2(b). Estimate quality on the fallback grid, wider s₀/p: B (hard, upstream). |
| 3 | C-GROW:Thm-GROW (f04) | **B** | Superseded as headline by W3-RM:RM-F and W3-RM2. Item 5 (local-rank lattice condition) = RM (N-loc)/(N-D). Items 1–2 (old cap range, deterministic cap ℓ_nω_n): out of scope (old cap is not the shipped configuration; method change). Item 6 (η at limsup log p/log n, A < 1): C (p ≫ n is the regime that matters). Items 7–10: known hard (RM §6). Polynomial failure rate: B, see note R. **Items 3–4 are B\***: fixed-constant visibility M ≥ 4(A+1)σ² + 2C_R(2A+1) in place of M_n → ∞ is correct (checked `L3_sandwich.md:82-84`) and is recorded but not adopted in `W3-RM/SHARPNESS.md:28-29`; RM-F, RM2-F still assume M_n → ∞ and BM-∞ → T4. |
| 4 | C-MIS:Thm-MIS(i) (f05) | **A** | "σ², τ² fixed" is removable by exact scale invariance of the coded posterior (y is standardised; b = b₀s_y²); the fixed-variance requirement is real in the statement (`STATEMENT.md:49,55,83-85`) and the registry notes call MIS "narrower than Song–Liang" because of it. GR needs only the contrast law. → T1. n^{−1/2} for bounded p_𝒞: C (regime irrelevant). Sub-Gaussian noise, growing s₀: B (hard). |
| 5 | C-MIS:Thm-MIS(ii) (f05) | **A** | Same ticket: design-measurable τ²(x), tight (not fixed) envelope constants, s-slicing, and the uniform-over-𝒜_n conclusion the proof already gives (`L1_reduction.md:114`). → T1. |
| 6 | W2-APP:POST (f06) | **B** (B\* residual) | As a posterior theorem it is superseded by W3-POST:Thm-1 item 6 / Cor 1R and W3-POST2. Item 2 (anchored sets) = POST2:E at fixed design. Item 3 (θ_lo,n → 0) = BM(c) in W3-POST. Uniform statement, expectation rate = POST2:C. Items 1 and 4 (nψ_n > 1 by a Wishart bound; sub-Gaussian rows) are **known and undone**: W3-POST REPORT §4 item 6 (R03 §4A). Still consumed by RM-R/RM2-R through (T1-R) → T5. |
| 7 | W2-APP:Thm-LOC (f07) | **B** | Superseded by W2-LOC2 → W2-UNI:UNI-0 → W3-RM:RM-R (an examples row now). Vanishing θ_lo, a₀ in Form R: declared non-claim in RM §6 and RM2; not cheap there (SAND-R is uniform over coefficient boxes). Redundant C under (LOC-Σ), PTV for \|U\| ≤ B − 1: C. d ≥ 2: done (LOC2). Rate: note R. |
| 8 | W2-FAC-A:Prop-F-FAC (f09) | **B** (stop list) | The "underfitted phase" idea (LS0 adds missing truths with gain ≍ n, O(1) such moves, then the descent) looks right where Q = [p], K = p and the full Gram is well conditioned (Corollary U is indeed for every T ⊆ [p], `L1_uniform_add.md:149-154`); it would remove (TV)/(GC-CS). But it is a one-factor, p < n^{1/6} family result: PROGRAM stop list (no design-family tickets, no exponent work for p ≤ K). It does not transfer to p ≫ n: there the start mode has size K and P6 found LS0 never supplies S₀. Park the idea as a remark for the examples table. (AG) slack, polynomial rate: C / note R. |
| 9 | W2-FAC-B:Thm-FAC-CS (f10) | **B** (stop list) | n-dependent ϑ_n at the √(log n/n) scale, (FS) on realisable pairs, ρ_n in a compact set: all plausible and easy, all on the exact-Gram compound-symmetry family (stop list: no exact-Gram factor tickets). Constant c < c_D: C. |
| 10 | W2-UNI:F-UNI (f14) | **B** (A residual) | The three-layer restatement (deterministic core, inequality, path event 𝒦_n instead of a deterministic lattice) is W3-RM:RM-0(a)–(b). Residuals: mode interface → T2(b); law-free delivery → T2(a). λ_min(Σ_n) > 0 redundant, cap slack: C. |
| 11 | W3-POST:Thm-1 (f15) | **B** (A residual) | (F_w) → DG/OS = POST2:A1. (F_λ) → identifiability margin = POST2:E. Expectation rate, uniformity = POST2:C. Beta-min constant = POST2 open item 2 (R03b E+). (E) with M_n ≍ log p: unclear, reviewer unsure. Asymmetric PIP bound: real, low value. **Residual A:** the √(log p) question (W3-POST REPORT §4 item 10, POST2 §6 item 6, both open) now has a concrete short route → T3(a). |
| 12 | W3-POST:Lemma-1a′ (f16) | **B** (A residual) | Approximate reference and exact D_T = POST2:B. Expectation size tail = POST2 Lemma C2 (reference S₀ only). Polynomial L-tail for general T, reference families: real, low value. **Residual A:** a counterexample showing ridge-cost control of the reference cannot be dropped (settles Remark 2, registry flag A:COEF-REP) → T3(c). Plausible on my reading; unchecked numerically. |
| 13 | W3-POST:Prop-LB (f17) | **B** (A residual) | Superseded by POST2:A2 (δ_n ≥ 𝒪⁰/(1 + 𝒪⁰), all supersets, any s₀ ≤ K). n + 1 → n, redundant domain conditions, s₀ = 0 constant: C. **Residual A:** (i) the multiplicity factor the proof discards (`LB:28-31`, checked) gives δ_n ≳ (s₀+1)/(2√n) on every design → T3(b); (ii) the √(log p) lower bound → T3(a). |

**Note R (polynomial failure-probability rates; f04, f07, f09, f10).** All four observe that the 1/log n bounds come
from log log n slacks where ε log n is available. Real, but it touches every lemma chain (re-verification cost), and
the tie-break puts rate third. B: no ticket; state it as a remark only if a chain is reopened anyway.

Counts by main class: A 2 (C-MIS i, ii), A/B split 1 (C-DLV), B 10 of which 4 leave an A residual and 2 a B\* residual.
No claim is class C as a whole; the C entries are cosmetic sub-items.

## 2. Tickets

Ranked by value / cost. Each is one lead session plus the usual lock and council; none needs new ideas.

**T1 — MIS-R: C-MIS v2 (f05).** (a) Lemma R′: scale invariance of the coded posterior, so "σ² fixed, τ² fixed" becomes
any σ²_{𝒞,n} > 0 with ‖μ^𝒞‖² ≤ Mnσ²_{𝒞,n} and beta-min relative to it; GR on the contrast law only. (b) MIS(ii): τ²(x)
design-measurable, tight envelope constants, uniform-over-𝒜_n conclusion. (c) Re-point the input from T03♯ to
W3-POST2 (A1/E/C), so MIS inherits (OS)/(ID^M) and the expectation rate. Also one remark that Theorem 1 itself holds
with n-dependent σ*² in SNR form. Value: PROGRAM item 2; removes the recorded gap to Song–Liang Thm 4. Cost ≈ 1 day.
Check first: confirm the invariance against the code path (standardisation of y, b = b₀s_y²), not only the formulas.

**T2 — RM-0 rider: delivery and mode interface (f03, f14, f09).** (a) DLV-0: under EX-A, IDEAL-W, MACH, CONFIG and
the Corollary R allocation, every valid non-degenerate input and every seed returns output; no model, no design class.
(b) Replace {π(S₀) ≤ ½} in RM-0(b) by {S₀ is not the unique F-maximiser on Ω}; [POST] becomes a corollary by Markov.
Result: RM-0/RM-F/RM-R/RM2 state P(Ŝ⁺ = S₀) → 1 without "on output", on any design, and the error splits into
mode failure + search failure — the two classes P6 measures. Not excluded by the stop list: that bars work on the
*shipped (unpatched)* calibration; main has the fallback grid. Timing: after W3-RM2's council (same files); re-audit
Lemma R when v3.2 freezes (the preflight charge changes). Cost: restatement + one line check.

**T3 — POST-SHARP: three sharpness records for the posterior theorem (f15, f17, f16, f06, f07).**
(a) On orthogonal designs with p = n^a, a ≤ 1: δ_n ≥ (1 − o_P(1))(s₀+1)√(log p/(πn)), by a truncated weak law for
e^{χ²₁/2} (tail 1/(w√(π log w)), truncated mean 2√(log p/π), variance p/√(π log p): I re-derived these). Theorem 1's
rate is then exact; closes the open √(log n) question. (b) Corollary of POST2:A2: δ_n ≳ (s₀+1)/(2√n) on every design,
so π(S₀) → 1 needs s₀ = o(√n) and rate r_n needs bounded s₀. This corrects the recorded target "growing
s₀ = o(log n/log log n)" (W3-POST REPORT §4 item 8): a growing-s₀ ticket must aim at s₀√(log p/n) or at mode
consistency (T2(b)). (c) The f16 counterexample for Lemma 1a″, with a numeric check. Cost ≈ 2 pages + numerics.
Value: closes three open/`improvable` flags and stops rate work that cannot succeed.

**T4 (B\*) — constant-level signals in RM-F / RM2-F (f04).** (V) with a fixed M ≥ M₀(A, σ², C_R) and BM(c), c > c₀,
in place of M_n → ∞ and BM-∞: visibility and beta-min at the standard Cσ² log p scale. Known
(`W3-RM/SHARPNESS.md:28-29`), never adopted. Rider on RM2 after its council; needs the TL step (GROW L2.1) re-read
for the constant. Cheap.

**T5 (B\*) — Corollary 1R v2 (f06).** Gaussian/sub-Gaussian row bridge to the POST2-E interface: anchored population
floors, nψ_n > C by a Wishart lower bound instead of ψ_n√n/(log n)^{3/2} → ∞. Known (W3-POST REPORT §4 item 6).
Gain for RM-R is limited to the logarithmic-size sets, because (FL-R) keeps the small-set floors. Lowest priority.

**No ticket:** f01 (hand to track 3), f09/f10 (stop list), note R (rates), all C sub-items.

## 3. What I checked, and what I did not

Checked against the files: GROW L3 visibility step; C-DLV Theorem D walk, Lemma S.1, Lemma R scope; LB proof steps
(i)–(iii) and the discarded multiplicity; C-MIS fixed-variance hypotheses and the reduction proof; FAC-A Corollary U
scope and L7 Step 3; POST2 claims A–E and Lemma C2; RM-0, RM-F hypotheses, RM §6; RM2 hypotheses; PROGRAM stop list.
Recomputed: the e^{χ²/2} tail, truncated mean and variance; the BB(1,p) one-up prior ratio.
Not checked: the f16 counterexample numerically; the f09 sketch end to end; scale invariance against the code;
f06's Wishart bound constants; any reviewer citation of the outside literature.
