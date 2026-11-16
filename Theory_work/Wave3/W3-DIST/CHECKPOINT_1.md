# W3-DIST — CHECKPOINT 1, revised (target gate; 2026-11-15, 18:35 CST; lead: Claude Fable 5.2, Claude Third, high)

Revision of the 17:55 checkpoint after HQ steers A5 and the settled note on presentation: the headline theorem now has
a reader version, and the bridges from its assumptions to the master theorem are on the critical path.

**Recommendation: GO.** **Nothing is proved yet**: every statement is a candidate. The master statements had a blind
Astra read (GO-WITH-REPAIRS, all repairs applied). The reader versions and bridges were written afterwards and have
had an Opus same-family pre-check only (REPAIRABLE, all repairs applied); their cross-family check is pending.
Files: `STATEMENT.md` (v1.3), `TARGET.md`, `ROUTES.md`, `ASSUMPTION_MAP.md`, `DEPS.tsv` + `DEPS.md`, `API_CARDS.md`,
`reviews/S1_astra.md`, `reviews/S1_disposition.md`, `reviews/P1_opus_precheck.md`, `reviews/P1_disposition.md`,
`work/prior_probe/REPORT.md`, `work/numerics/RESULTS.md`.

## 1. The headline theorem in reader form (full text with setup and notation table: TARGET.md §6 = STATEMENT.md §1R)
Data: n independent pairs (x, y), x ∈ ℝ^p. The method standardises the data and uses its fixed prior (beta-binomial
BB(1, p) on the set S of included predictors, at most min(p, ⌊n/2⌋) of them; a Gaussian prior on their coefficients with
covariance n × noise variance × (G_S + I)⁻¹; inverse-gamma(0.01, 0.01) on the noise variance). Π(· | D_n) is the posterior
of (S, β, σ²); each draw defines a joint density f of (x, y); f* is the true one; d_H is the Hellinger distance. Fix a
level M ≥ 1 and the window q_n = min{p, ⌈C_q M log n⌉}, of order log n.
- **(A1) Gaussian linear model.** y = α* + xᵀβ* + ε, ε ~ N(0, σ*²) independent of x, any σ* > 0.
- **(A2) Sparsity and dimension.** At most s nonzero coefficients; 2 ≤ p ≤ n^A.
- **(A3) Sub-Gaussian predictors.** For every u with at most q_n nonzero entries and every λ:
  E exp(λuᵀz) ≤ exp(K²λ²Var(uᵀz)/2), z the standardised predictors.
- **(A4) No near-exact collinearity.** λ_min(Corr(x_T)) ≥ c_ψ/n for every set T of at most q_n predictors.
- **(A5) Bounded signal.** |β*_j|·sd(x_j) ≤ b̄σ* for every j.

**Theorem A.** There are constants c > 0, C₁, M₀, n₀ depending only on (s, A, K, c_ψ, b̄) such that, for n ≥ n₀ and
M₀ ≤ M ≤ √n/log n, under (A1)–(A5):

    (i)   P*[ Π( d_H(f, f*) > √(M log n/n) | D_n ) > n^{−cM} ] ≤ n^{−cM},
    (ii)  P*[ Π( |S| > s + C₁M | D_n ) > n^{−cM} ] ≤ n^{−cM}.

The posterior contracts to the true joint distribution at the rate √(log n/n), and concentrates on models with a
bounded number of predictors, without saying they are the true ones. No lower bound on the nonzero coefficients and
no identifiability condition. *Without (A4)* (and with (A3) for single predictors only): (i) holds with radius
√(M log n·log(p ∨ n)/n) and (ii) with s + C₁M log n. *Example:* Gaussian predictors with AR or equal correlation.
Why each assumption is there, and whether it is necessary (one line each, TARGET.md §6): (A3) and (A4) are **not
necessary for consistency** — (A3) only makes sample variances and covariances track the population, (A4) only
protects the sharp rate; (A5) is needed in a weaker form; (A1), (A2) are the model and the regime.
**Companions in the same form:** Theorem B — adding a detectable-signal assumption (A6: a fixed eigenvalue bound on
small sets and a beta-min level), Π(d_H > M_n/√n | D_n) → 0 in probability; conditional on the selection-consistency
theorem W3-POST:Thm-1. Corollary C — the posterior restricted to the sampler's returned list of models satisfies
Theorem A's bound, with n^{−cM/2}, for every completed run whose list carries posterior probability ≥ n^{−cM/2}.

## 2. The master statements behind it (short form; exact text STATEMENT.md §1–2)
Rows i.i.d. from an **arbitrary** law on ℝ^{p_raw}, p_raw ≤ n^A; Gaussian noise; strict sparsity; prior as coded.
- **DIST-1.** For M₀ log n ≤ t ≤ n^{1−κ₀}: P*[Π(d_H > C√(t/n) or |S| > s₀ + C′t/log n | D_n) > e^{−ct}] ≤ 3e^{−ct} + P*(interfaces
  fail). Interfaces (sample-level): two non-constant columns; energy ‖μ‖² ≤ nM; coefficient cost ‖θ*‖² ≤ nM′; **(ND)**,
  average determinant growth on supersets of S₀ up to size O(log n + t).
- **DIST-2.** The same without (ND), radius C√(t·log(p ∨ n)/n).
- **DIST-3.** Π(d_H > C√(u/n) | D_n) ≤ δ_n + Ce^{−cu} (δ_n = 1 − π(S₀)) under energy, bounded ridge loss of the true model and a
  second-moment comparison on the true support.
- **DIST-C.** The run returns HPM, PIPs, MPM, log Ẑ and a scored top store of 40p + 1 models — **no particles, no (β, σ²)
  draws, no predictive** (`v3_run.R:142-163, 210`; `cpp/v3_ledger.h:43-56, 78`). For any output-defined law Q on models
  with Q ≤ L_nπ: QΠ(B) ≤ L_nΠ(B | D_n). Store BMA and HPM/MPM plug-ins follow; delivery premises (discovery, P-STORE, P-HIT)
  are named, not proved; all jointly with {completed}.

## 3. Key lemmas and bridges (STATEMENT.md §3)
Lemmas: **H** (Hellinger reduction, deterministic); **T** (distribution-free transfer from the sample to the
population on sparse directions, a VC bound on a truncated loss); **X** (in-sample exponential core, fixed design —
**the key lemma**) and **X′** (without (ND)); **S** (size tail with an exponential tail); **V** (design-free moment
bound for supersets; helper-derived); **P6** (domination transfer).
Bridges (reader version = master + bridges): **B0** any σ* reduces to unit noise, pathwise (W3-MISR Lemma R′,
PROVED-CHECKED); **B1** (A3) + (A5) ⇒ no dropped column, energy and coefficient-cost events, probability
≥ 1 − 4p·e^{−cn/K⁴}; **B2-core** one-sided sparse lower bound for sample second moments with an intercept; **B2**
(A3) + (A4) ⇒ (ND), with the eigenvalue floor allowed to be as small as c_ψ/n; **B3** the extra events for Theorem B.

## 4. A1 parity checklist (candidate vs Song–Liang; full table TARGET.md §2)
| item | verdict | why |
|---|---|---|
| **P1 metric** | **matches** | same joint (x, y) Hellinger distance; our sample-to-population step needs no condition on the predictor law |
| **P2 (15) exponential** | **matches in form** (Theorem A (i)) **under (A4); short otherwise** | (A4) is a geometric condition they do not have; without it the exponent is c nε_n²/log p. Reason: the coded size prior is ≈ geometric(½); they hard-cap model size |
| **P2 (16) in probability, second moments** | **short in the reader form** | the master theorem gives it whenever the three sample events have probability → 1, and energy and coefficient cost need only second moments; but no primitive second-moment condition for the non-degeneracy event is claimed (pre-check counterexample with an atom) |
| **P3 rate** | **Theorem A beats; Theorem B beats; no-(A4) version short of their best** | √(log n/n) with no diverging factor (theirs at polynomial p: ω_n log n/n, ω_n → ∞; Cor 1 as printed is slower than both of ours); parametric rate with detectable signal; without (A4) log n·log p/n |
| **P4 sparsity** | **matches** Thm 2; **short** of Thm 1 (approximate) | stretch S-APX |
| **P5 prior** | **matches** (coded prior, no tuning) | their conditions (9), (10), (11) and "r_n ≻ 1" fail for it; route: condition on the design, closed-form marginal likelihoods, Occam factor |
| **P6 coded output** | **beats**, conditional | Corollary C / DIST-C; the code returns no distribution, so this is about distributions reconstructed from its output |
| **Scope** | **matches**; **short** on exponential p | p ≤ n^A, p ≫ n. Stretch S-EXP |
| **Design-agnostic** | no family in any statement; **short** by (A4)/(ND) for the sharp rate | none needed for consistency |

## 5. Routes, failure points, kill budgets (ROUTES.md §2, §2b)
In-probability versions are assembly; the exponential form is new proof work without new probability theory; the
bridges are standard concentration.
| item | difficulty | where it could fail | kill budget | if it fails |
|---|---|---|---|---|
| H | low | — | 1 attempt | — |
| T | low | constant / reference of the relative-deviation inequality | 2 | constants change; else sub-Gaussian transfer (harmless for the reader version, WEAKER on master TC1) |
| S | low–medium | exponential bound for the response-scale bracket | 2 | in-probability form only → early checkpoint |
| V | low–medium | algebra (helper-derived) | 2 | POST2's truncated-moment route |
| **X** | **medium–high** | truncated Occam moments with unknown variance at a t-scaled truncation; one n₀ for all t | **3**, each with a reviewer verdict | in-probability sharp rate + DIST-2 → early checkpoint |
| X′ | medium | variance displacement | 2 | DIST-2 in probability |
| P6 / DIST-C | low | overclaim of what the code returns | 1 | — |
| **B0** | low | pathwise form with the plug-in intercept | 1 | fixed σ* in the reader version (WEAKER on TC9 → early checkpoint) |
| **B1** | low | — (pre-check: sound) | 1 | — |
| **B2-core** | low–medium | exact constants; ψ₂–L₂ form on sparse directions; intercept | **2** | Gaussian predictors only (WEAKER on TC9 → early checkpoint) |
| **B2** | low | range of the window against m_n(t) | 1 | a larger window constant C_q |
| **B3** | low | matching W3-POST Theorem 1's hypotheses | 1 | Theorem B stated with those hypotheses as assumptions |
| S-FIT (stretch) | high | may be false in exponential form | 1 Fable attempt + 1 Astra break review | (A4) stays |
| S-APX, S-EXP (stretch) | medium | bias out of sample; where p ≤ n^A enters | 1 each, after CP2 | strict sparsity, p ≤ n^A stay |

## 6. Consumes (STATEMENT.md §4)
Self-contained by plan: DIST-1/2/3, Lemmas H, T, S, V, X, X′, P6, bridges B1, B2-core, B2 (inherited premise: locked T01).
W3-MISR:R′@1.0.0 ("PROVED-CHECKED") for B0. W3-POST:Thm-1@1.0.0 ("T03♯: PROVED; SF VERIFIED; XF VERIFIED") is a premise
of Theorem B. W3-POST2 Claim D per HQ's note ("council-passed C1 (11-09); D(b) repaired after the council, single Sol
check (PC2); diff round in progress"): D(a) not consumed; D(b) only in the fallback. DIST-C's delivery statements are
conditional on W3-SAMP D / LT♯ / C / TR and W3-RM2 under their own premises. T04 is a route guide only.

## 7. Sharpness gate
Assumption map and boundary numerics as in the 17:55 checkpoint (`ASSUMPTION_MAP.md`, TARGET.md §1, §3): nothing
contradicts a statement; heavy-tailed predictors and near-duplicate columns show no degradation of the Hellinger
numbers in exact enumeration at p = 12; limits — averaged rather than nested tails, the collinearity scale
τ² ≍ log n/n² and a violation of (A5) are not yet simulated. Better-theorem review (S1): four proposals, all adopted.

## 8. Reviews and dispositions
- **S1** (gpt-6-astra, codex, high; manifest fb6d0dab…b62e), on the master statements: GO-WITH-REPAIRS; 5 major,
  5 minor, 1 nit; all 11 findings and 4 better-theorem proposals adopted (`reviews/S1_disposition.md`).
- **P1** (Claude Opus 5.5, Claude Third; a same-family filter, not a review layer), on the reader versions and
  bridges: REPAIRABLE; no reader clause false under its faithful reading; 3 major wording repairs (Theorem B must say
  "(A4) and in addition"; a second-moment claim in the assumption notes was false and is removed; the level M is now
  fixed before the assumptions), 6 minor (a wrong determinant formula in B2 with a correct conclusion; B0 must be
  pathwise; B2-core needs min(q, p); setup wording), 7 nits (among them the range M ≤ √n/log n). All applied
  (`reviews/P1_disposition.md`).
- **Pending, for HQ to order:** one cross-family read of STATEMENT §1R and the bridges, which can also do the
  PROTOCOL_v4 §4.2 statement-change check of the changelog tags (v1.1–v1.3).

## 9. Target clauses proposed for HQ to fix (TARGET.md §5, §6)
TC1 metric · TC2 DIST-1's display · TC3 its rate · TC4 its hypotheses · TC5 the coded prior · TC6 DIST-2 · TC7 DIST-3's
oracle display · TC8 DIST-C's deterministic transfers with labelled premises · **TC9 reader Theorem A** ((A1)–(A5),
displays (i), (ii), the sentence without (A4)) · **TC10 reader Theorem B and Corollary C, if HQ makes them headline**.

## 10. GO plan (proof leg; Fable lead on Claude Third)
**Order (DEPS.tsv):** H, T → S, V → X → DIST-1 → X′ → DIST-2, **with the bridges B0, B1, B2-core, B2 in parallel from the
start** (they are independent of X and now on the critical path of Theorem A); DIST-3, B3 and P6/DIST-C in parallel;
stretch after CP2.
| stream | content | model |
|---|---|---|
| A | Lemma X (X3, X4), integration, statement control; S-FIT attempt | Fable (lead) |
| B | Lemmas H, T (VC inequality verified or proved); DIST-3 | Opus |
| C | Lemmas S and V; Lemma X steps X1–X2 | Opus |
| D | P6 / DIST-C; Corollary C | Opus |
| **E (critical path)** | bridges B0, B1, B2-core, B2, B3; assembly Theorem A = master + bridges; the example | Opus |
| F | numerics and falsification (nested tails, τ² ≍ log n/n², (A5) violated, per-lemma checks), citecheck, DEPS upkeep, LaTeX block, notation table | Sonnet |
**Reviews.** Each lemma and bridge: Opus pre-check as a filter, then the cross-family line check on codex (Sol; Astra
for X and S). **CP2** = Lemma X with S and V proved and line-checked, then the Astra break review (CONTINUE / REDIRECT /
STOP). Sweep, citation check, council (gate F: reader version = master + bridges), CP3.
**API attempts.** `API_CARDS.md`: cards for X, S, T, V, bridge B2-core and S-FIT, each with a self-contained statement,
context files and parallel routes.
**Time (lead's estimate, uncertain):** CP2 in 1–2 days of wall-clock; CP3 in 3–5 days.
**Second Fable.** Not material for the main line or the bridges. Material only for S-FIT, the one item that could
remove (A4) from Theorem A; decide after the API attempts on S-FIT return.

## 11. What this buys the paper vs Song–Liang
One theorem a reader can take in at once: under a Gaussian sparse linear model with sub-Gaussian predictors, a very
weak non-collinearity condition and bounded signal, the posterior **of the prior the method actually uses, untuned**,
recovers the joint distribution of predictors and response at the rate √(log n/n), with polynomially small exceptional
probabilities, and uses a bounded number of predictors — with no beta-min and no identifiability condition.
Song–Liang prove the same kind of statement for a prior family tuned to the rate, at a rate with a diverging factor
at polynomial p, and nothing for sampler output; ours adds the parametric rate under detectable signal and a
statement for what the sampler returns. The price: the non-collinearity condition for the sharp rate (one logarithm
without it), exact sparsity, p ≤ n^A, and — in the reader form — sub-Gaussian predictors, where their in-probability
result needs second moments only.

## 12. For HQ
1. Fix the target clauses (§9), including whether Theorem B and Corollary C are headline, and the kill budgets (§5).
2. Order the cross-family read of the reader versions and bridges (§8).
3. P6 is about reconstructed distributions because the code returns none; claiming more is a method change.
4. The presentation of the reader version is my choice under the settled note; the owner can redirect it.
5. `work/numerics/arrays/` holds 68 MB of regenerable arrays, ignored by a local `.gitignore` since 16:10.
