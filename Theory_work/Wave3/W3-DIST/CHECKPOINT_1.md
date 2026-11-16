# W3-DIST — CHECKPOINT 1 (target gate; 2026-11-15, 17:55 CST; lead: Claude Fable 5.2, Claude Third, high)

**Recommendation: GO.** The blind Astra read returned GO-WITH-REPAIRS; all repairs are applied (STATEMENT v1.1) and none
weakens a target clause. **Nothing is proved yet**: every statement below is a candidate. Files: `STATEMENT.md` (v1.1),
`TARGET.md`, `ROUTES.md`, `ASSUMPTION_MAP.md`, `DEPS.tsv` + `DEPS.md`, `API_CARDS.md`, `reviews/S1_astra.md`,
`reviews/S1_disposition.md`, `work/prior_probe/REPORT.md`, `work/numerics/RESULTS.md`.

## 1. The candidate statements (short form; exact text in STATEMENT.md §1–2)
Setting: rows i.i.d. from an **arbitrary** law ν_x on ℝ^{p_raw}, p_raw ≤ n^A (p ≫ n allowed); Gaussian noise independent
of the design; strict sparsity (s₀^r true predictors, fixed); the exact posterior of (S, β, σ²) under the prior **as
coded**; d_H = Hellinger distance between the joint (x, y) laws ([SL]'s d² = 2d_H²).
- **DIST-1 (sharp rate, exponential form).** For all t with M₀ log n ≤ t ≤ n^{1−κ₀}:
  P*[Π(d_H(f, f*) > C√(t/n) or |S| > s₀ + C′t/log n | D_n) > e^{−ct}] ≤ 3e^{−ct} + P*(interfaces fail).
  Interfaces (sample-level, design-agnostic): at least two non-constant columns; energy ‖μ‖² ≤ nM; coefficient cost
  ‖θ*‖² ≤ nM′; and **(ND)**, "no degeneracy on average" (POST2's average determinant growth on supersets of S₀ up to size
  O(log n + t)), which fails only under near-exact linear dependence. Best rate ε_n² ≍ (1 + s₀)(A + 1) log n/n ≍
  (1 + s₀) log p/n. No beta-min, no identifiability, no moment condition on x beyond the probability of the interfaces.
- **DIST-2 (no geometric condition on the design).** Same display without (ND), radius C√(t·log(p ∨ n)/n): one logarithm
  slower, exponent c nε_n²/log(p ∨ n).
- **DIST-3 (oracle / parametric).** Under energy, bounded ridge loss of the true model and a second-moment comparison
  on the true support: Π(d_H > C√(u/n) | D_n) ≤ δ_n + Ce^{−cu} outside a noise event of probability Ce^{−cu}
  (δ_n = 1 − π(S₀)); hence Π(d_H > M_n/√n | D_n) → 0 in probability whenever δ_n → 0.
- **DIST-C (coded output).** The run returns HPM, PIPs, MPM, log Ẑ and a scored top store of 40p + 1 models — **no
  particles, no (β, σ²) draws, no predictive** (`v3_run.R:142-163, 210`; `cpp/v3_ledger.h:43-56, 78`). For any law Q on
  models built from the output with Q ≤ L_nπ, the reconstructed parameter law satisfies QΠ(B) ≤ L_nΠ(B | D_n)
  (deterministic). So DIST-1/2 transfer to the **store BMA** when the store holds posterior mass ≥ e^{−λt} (λ < c), and
  to the **HPM plug-in** when the ledger contains one model of mass > e^{−ct/2}. With selection (S₀ discovered, δ_n < ½)
  both hold and the HPM/MPM plug-ins get DIST-3's oracle bound. Without beta-min these are named premises about the
  run (P-STORE, P-HIT), not proved and not certified by the output. All statements jointly with {completed}.

## 2. Key lemmas (STATEMENT.md §3)
- **H** (deterministic): d_H² ≤ (v/σ*² − 1)² + E_x min{1, Δ(x)²/(4σ*²)}. Five-line proof written.
- **T** (distribution-free transfer): for any law of x, w.p. ≥ 1 − δ, uniformly over intercepts and d-sparse directions
  (1 ≤ d ≤ min(p_raw, n − 1)): E_x min{1, (a + uᵀx)²/c} ≤ 2·(sample mean) + (4/n)[d log(ep_raw/d) + 2(d+1) log(2en/(d+1)) +
  log(4/δ)]. Classical VC relative-deviation bound on a **truncated** loss; no moments.
- **X** (in-sample exponential core, fixed design; **the key lemma**): under energy, coefficient cost and (ND),
  P_ε[Π(‖μ̂ − μ‖² > Cσ*²t or |v/σ*² − 1| > C√(t/n) or |S| > s₀ + C′t/log n | y) > e^{−ct}] ≤ 2e^{−ct}. **X′**: without (ND),
  with t·log(p ∨ n) and the size cut m_n(t) = O(log n + t).
- **S** (size tail with an exponential tail, reference-adaptive, no p ≤ n^A): re-run of POST2 Claim B's proof with χ²
  tails in place of Markov/Chebyshev.
- **V** (helper-derived, unchecked): design-free moment bound for supersets,
  E[(D_{S₀}/D_S)^{1/2}e^{eᵀD′e/2σ*²}] ≤ (1 + η)^{s₀+|J|/2}.
- **P6** (deterministic): the domination transfer and a Markov bound over models.

## 3. A1 parity checklist (candidate vs Song–Liang; full table with PROGRAM goals and our best registered result: TARGET.md §2)
| item | verdict | why |
|---|---|---|
| **P1 metric** | **matches** | the same joint (x, y) Hellinger distance, x integrated. The sample-to-population step needs no condition on the predictor law, where [SL] need bounded predictors or Condition 1/2 |
| **P2 (15) exponential** | **matches in form under (ND); short otherwise** | DIST-1 is their display with remainder P*(interfaces fail), for all ε_n² between C log n/n and n^{−κ₀}. Short because (ND) is a geometric condition [SL] do not have; without it (DIST-2) the exponent is c nε_n²/log p. Reason: the coded size prior is ≈ geometric(½); [SL] hard-cap model size |
| **P2 (16) in probability** | **matches** (given (ND) w.p. → 1) | the energy and coefficient-cost events need only second moments of the true signal coordinates |
| **P3 rate** | **DIST-1 beats; DIST-3 beats; DIST-2 short of their best** | DIST-1: (1 + s₀) log p/n with no diverging factor; [SL] Thm 2 at polynomial p gives ω_n log n/n with ω_n → ∞ tied to their cap, and Cor 1 as printed (fixed α > 0) is slower than both of ours. DIST-3: parametric given selection ([SL] have none). DIST-2: log n·log p/n, short of ω_n log n/n by log n/ω_n |
| **P4 sparsity** | **matches** Thm 2 (strict); **short** of Thm 1 (approximate) | stretch S-APX |
| **P5 prior** | **matches** (coded prior, no tuning) | [SL]'s own conditions (9), (10), (11) and "r_n ≻ 1" **fail** for it (cap ⌊n/2⌋, mean prior size O(1)), and their sieve route cannot work with a geometric size prior when log p → ∞. The route that works conditions on the design and uses the closed-form marginal likelihoods and the slab's Occam factor |
| **P6 coded output** | **beats** (beyond [SL]), conditional | deterministic transfer to the store BMA and HPM/MPM plug-ins; delivery premises explicit; the code returns no distribution, so P6 concerns distributions reconstructed from its output |
| **Scope** | **matches** the required scope; **short** on exponential p | p ≤ n^A, p ≫ n; no lower growth bound on p. Stretch S-EXP |
| **Design-agnostic** | DIST-2 **matches**; DIST-1 **short** by (ND) | no design family, no identifiability, no beta-min anywhere |

## 4. Routes, failure points, kill budgets (ROUTES.md)
In-probability versions are **assembly**; the exponential form is **new proof work without new probability theory**
(χ² tails, conjugate formulas, Markov on truncated moments). Why it is reachable: models that overfit by a few
variables are Hellinger-good, so the inner threshold can be exponentially small although 1 − π(S₀) ≥ n^{−1/2}.
| lemma | difficulty | where it could fail | kill budget | if it fails |
|---|---|---|---|---|
| H | low | — | 1 attempt | — |
| T | low | exact constant / reference of the relative-deviation inequality (to verify or prove) | 2 attempts | constants change (EQUAL); if no distribution-free form survives: sub-Gaussian or small-ball transfer — WEAKER on TC1 → early checkpoint |
| S | low–medium | exponential bound for the s_y bracket; t/√n term | 2 attempts | only the in-probability (16)-form for DIST-1/2 — WEAKER on TC2 → early checkpoint |
| V | low–medium | algebra of the variational split (helper-derived) | 2 attempts | X4 falls back to POST2's truncated-moment route |
| **X** | **medium–high** | step X4: truncated Occam moments with unknown variance at a t-scaled truncation; one n₀ for all t; the three factors of S1-06 | **3 attempts**, each with a reviewer verdict | fallback: in-probability sharp rate (POST2 D(b) + H + T, conditional on D(b)) and DIST-2 — WEAKER on TC2/TC3 → early checkpoint |
| X′ | medium | variance displacement t log p/n | 2 attempts | DIST-2 in probability only |
| P6 / DIST-C | low | overclaim of what the code returns | 1 attempt | — |
| S-FIT (stretch) | high | may be false in exponential form | 1 Fable attempt + 1 Astra break review | (ND) stays |
| S-APX (stretch) | medium | out-of-sample part of the bias | 1 attempt after CP2 | strict sparsity stays |
| S-EXP (stretch) | medium | where p ≤ n^A enters | by-product only | p ≤ n^A stays |

## 5. Consumes (STATEMENT.md §4)
DIST-1, DIST-2, DIST-3 and Lemmas H, T, S, V, X, X′, P6 are planned **self-contained**: their only inherited premise is
the identification of the coded posterior with the contrast model (locked T01). W3-POST2 Claim D: per HQ's note
("council-passed C1 (11-09); D(b) repaired after the council, single Sol check (PC2); diff round in progress") —
D(a) is no longer consumed (DIST-3 was rebuilt without it); D(b) is used only in the fallback, which is conditional
on it. DIST-C's delivery statements are conditional on W3-SAMP D / LT♯ / C / TR ("PROVED-CHECKED") and W3-RM2
("PROVED-CHECKED, conditional on SOP:TH09 / W2-APP:POST") under their own premises. T04 is not in the registry and is
used as a route guide only.

## 6. Sharpness gate
- **Assumption map** (`ASSUMPTION_MAP.md`): (ND) enters one step (large models) and is **not needed for consistency**;
  flagged `improvable`. Strict sparsity and p ≤ n^A enter through constants. Beta-min and identifiability are not
  assumed.
- **Boundary numerics** (helper, exact enumeration at p = 12, n = 50…800, 40 replications per cell; p ≫ n on a
  restricted family; scripts not audited): nothing contradicts a statement. Heavy tails (t₂.₅, Pareto 2.1, spike
  columns): no degradation, transfer ratio ≤ 1.004 over all draws. (ND) violated by near-duplicates: selection
  fails (true column picked ≈ 25% of the time), Hellinger numbers unchanged. Limits: the tails measured are averaged
  over data sets, not the nested statement; the dangerous collinearity scale (τ² ≍ log n/n²) is not yet tested.
- **Better-theorem review** (S1; its brief asked for a strictly better statement): four proposals, all adopted —
  DIST-3 without the floor on S₀; the oracle exponential bound with additive δ_n; a reference-adaptive size lemma
  without p ≤ n^A; one domination transfer for any output-defined law.

## 7. Blind read S1 (gpt-6-astra, codex, high; manifest fb6d0dab…b62e) and dispositions
Verdict **GO-WITH-REPAIRS**: 0 critical, 5 major, 5 minor, 1 nit; no counterexample to DIST-1 on its stated interfaces.
Major findings: Lemma T false outside the range of its growth bound (repaired: d ≤ n − 1); raw vs retained dimension
conflated (repaired); a false blanket impossibility remark after DIST-3 (deleted); the comparison with [SL] overstated
in places (corrected — the table above is the corrected one); bridge B1's exponential clause false (repaired). All
11 findings and 4 proposals adopted, none disputed (`reviews/S1_disposition.md`). Not checked by S1: the VC
inequality's source, the numerics scripts, code beyond the three pinned files, the RM2/START proofs. Helper H1's
report (Opus) agrees with the route and corrected the lead on [SL] (11).
**Pending:** the PROTOCOL_v4 §4.2 statement-change check of the v1.0.2 → v1.1 tags (one Sol read of the diff); the
two WEAKER rows are non-target (remainder gains P(p_ret < 2); bridge B1).

## 8. Target clauses proposed for HQ to fix (TARGET.md §5)
TC1 metric (joint (x, y) Hellinger, ν_x arbitrary) · TC2 DIST-1's display · TC3 DIST-1's rate · TC4 DIST-1's
hypotheses · TC5 the coded prior · TC6 DIST-2 · TC7 DIST-3's oracle display · TC8 DIST-C's deterministic transfers
with labelled premises. Bridges, stretch items and the internal form of lemmas are not target clauses.

## 9. GO plan (proof leg; Fable lead on Claude Third)
**Order (DEPS.tsv):** H, T → S, V → X → DIST-1 → X′ → DIST-2; DIST-3 and P6/DIST-C in parallel; bridges B1, B2 in
parallel; stretch after CP2 (S-FIT may start earlier through the API attempts).
**Workstreams.**
| stream | content | model |
|---|---|---|
| A | Lemma X (X3, X4), integration, statement control; S-FIT attempt | Fable (lead) |
| B | Lemmas H, T with exact constants and the VC inequality verified or proved; DIST-3 | Opus |
| C | Lemma S and Lemma V; Lemma X steps X1–X2 from the lead's skeleton | Opus |
| D | P6 / DIST-C: code pins, retention, wiring to W3-SAMP / RM2 premises | Opus |
| E | bridges B1, B2 (small-ball transfer, (ND) from population conditions), examples table | Opus |
| F | numerics and falsification (nested tails, τ² ≍ log n/n², per-lemma checks), citecheck, DEPS upkeep, LaTeX block | Sonnet |
**Reviews.** Each lemma: Opus same-family pre-check as a filter, then the cross-family line check on codex (Sol; Astra
for X and S). **CP2** = Lemma X and what it consumes (S, V) proved and line-checked, then the Astra break review, whose
brief also asks CONTINUE / REDIRECT / STOP. Then sweep, citation check, council, CP3.
**API attempts (H3).** `API_CARDS.md` has, for X, S, T, V and S-FIT, a self-contained statement, the context files and
the routes worth attacking in parallel (for X: the lead's route; an untruncated-moment route; a fit-based route; an
adversarial search).
**Time (lead's estimate, uncertain):** CP2 in 1–2 days of wall-clock with the team; CP3 3–5 days.
**Second Fable.** Not material for the main line (P1–P3, P5 under (ND)): the risk there is bookkeeping in X4, which
reviews address better than a second prover. It would be material for **S-FIT** only — the one item that could remove
both "short" rows ((ND) in DIST-1, the logarithm and exponent in DIST-2) — because it is open-ended and independent
of the main line. Suggestion: decide after the API attempts on S-FIT return.

## 10. What this buys the paper vs Song–Liang
Song–Liang prove Hellinger consistency for the exact posterior of a prior family tuned to the rate (a hard cap on
model size, inclusion probability r_n/P_n with r_n → ∞), under bounded or exponential-moment predictors, at a rate that
carries a diverging factor at polynomial p. The candidate package gives the same kind of theorem **for the prior the
method actually uses**, with no tuning, at the rate (1 + s₀) log p/n in the same exponential form, with the passage to
the population distance free of any condition on the predictor law, plus a parametric-rate oracle bound once selection
holds and a statement about what the coded sampler returns — none of which they have. The price is one mild
non-collinearity condition for the sharp rate ([SL] need none), a logarithm without it, strict sparsity only, and
p ≤ n^A. It also turns PROGRAM item 1b from an in-sample corollary into an out-of-sample theorem.

## 11. For HQ
1. Fix the target clauses (§8) and the kill budgets (§4), or amend them.
2. Order the statement-change check of the v1.1 tags (§7).
3. P6 is about reconstructed distributions because the code returns none; if the paper should claim more, that is a
   method change (returning particles or draws), outside this ticket.
4. `work/numerics/arrays/` holds 68 MB of regenerable arrays; a `.gitignore` was added there at 16:10, but an earlier
   snapshot may have taken them.
5. PROTOCOL_v4 names the trace file `DEPS.tsv` and puts the changelog at the foot of STATEMENT.md; both done.
