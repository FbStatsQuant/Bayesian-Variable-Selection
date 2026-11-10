# W3-SCR — REPORT to Theory HQ (certified screening; PROGRAM item 5)

Lead: Claude Fable 5.2 (Claude Personal, effort high). Date: 2026-11-09. Folder: `Theory_work/Wave3/W3-SCR/`.
No method change is required. No git state was changed; nothing was written outside the folder.

## 1. RESULT
**PROVED-CHECKED.** Council passed in round 1: gpt-6-astra **9.3**, Claude Opus 5.5 **8.9**, all six gates PASS on
both seats (scored on STATEMENT v3.3; the six minor/note-level council findings were applied afterwards as wording
edits, v3.4, not re-scored). The card's theorem is proved (Corollary A1) and strengthened in five directions.

## 2. The statement as proved (`STATEMENT.md`, v3.4) and changes vs the card

**Code check first (`CODE_CHECK.md`, CC1-CC6).** `fit$local_certified = TRUE` means: the fit completed (so 𝒪 holds)
and the **reported HPM Ŝ itself** is a scanned endpoint of the final local search or of LS0 (or, on the enumeration
branch, the enumerated maximiser) with **no strictly better model among all single deletions, all single additions
(only when |Ŝ| < K) and all swaps**. `local_certified_by` says which search; `local_limit` (a move cap was hit in
either search) is *not* its negation. Each search archive also prints its scanned centres with scores, and every
scanned neighbour reaches the ledger, so F(Ŝ) ≥ F(N) for every neighbour N of every scanned centre (CC6).

**Results** (fixed standardised design, Gaussian errors, exact arithmetic EX-A; no premise on the start mode, leakage,
blocks, uniforms or calibration; every seed):
- **SCR-A (screening, non-asymptotic).** If the sparse visibility Γ_n(q) — the noiseless one-step gain of the best
  missing truth, minimised over all models of size ≤ q missing a truth — satisfies the explicit margin MC(q, x), then
  with probability ≥ 1 − 3e^{-x} **every** locally optimal model of size ≤ q ≤ K−1 contains S₀. Hence
  P(𝒪 ∩ {certified} ∩ {|Ŝ| ≤ q} ∩ {S₀ ⊄ Ŝ}) ≤ 3e^{-x}, and the same for every certified search endpoint.
  Asymptotic form (A∞): it suffices that √Γ_n(q_n) ≥ (1+δ)[τ_n√(2 log p + log n) + σ√(2 q_n log p)].
- **Corollary A1 = the card.** Sparse eigenvalue floor κ on sets of size q_n + s₀ (or only the weaker directional
  floor), fixed coefficients (θ_min ≥ b, ‖θ*‖₁ ≤ M), (q_n + 1) log p + log n ≤ c₁n with c₁ = κ²b²/(200(M² + σ²)):
  the probability → 0. Covers p ≤ n^A with any q_n = o(n/log n), and q_n up to order n/log(p ∨ n).
- **SCR-A° / A1° (self-normalised).** Each missing truth competes against the residual scale of the model at hand,
  not the total signal: beta-min θ_min ≥ 16σκ^{-1}√(((q_n+1) log p + log n)/n) suffices (no fixed coefficients).
- **SCR-M (master gap theorem) and SCR-G (uncertified runs).** On one event of probability ≥ 1 − 4e^{-x}, every model
  S of a deterministic family that misses a truth has a truth-addition improving F by at least an explicit
  deterministic gap δ_S; under A1's hypotheses δ_S > c₂n, c₂ = κ²b²/(104(M² + σ²)). Consequences, with probability → 1:
  (i) every **scanned centre** of size ≤ q_n whose score is within c₂n of the reported score contains S₀ — no
  certificate needed; (ii) if a search **stops on its move cap**, its returned model contains S₀ whenever its last
  scanned centre is within c₂n of the best score (so an uncertified reported model can still be covered);
  (iii) the coded search never drops a truth while sizes stay ≤ q_n. The model-count entropy is replaced by a
  geometric complexity (Gaussian width of the witness directions).
- **Excess set and exact recovery.** Lemma L5.1: every locally optimal strict superset of S₀ satisfies an explicit
  inequality (EC′) in the conditional lengths α(S) and the dual-direction factor ω(S) of its excess columns.
  **SCR-C:** with s₀ bounded and a floor φ ≥ 2 log p/(2 log p + log n) + ε on supersets of S₀ of size ≤ q_n (for
  p ≤ n^A: φ ≥ 2A/(2A+1) + ε), a sparse certified model **equals** S₀ with probability → 1.
- **SCR-R** (least-squares refit on a certified model: prediction error ≤ σ²(√k + √(2k log(ep/k) + 4 log n))², no
  floor needed) and **SCR-N** (sharpness: just below the threshold τ_n√(2 log p + log n), the empty model is locally
  optimal with probability → 1 — the constant 1 of (A∞) cannot be lowered at q = 0).

**Changes vs the card** (all strengthenings; the card is Corollary A1): floor on all (q_n+s₀)-sets → visibility /
directional floor (non-true columns may be arbitrarily collinear); q_n = o(n/log n) → c₁n/log(p ∨ n); fixed
coefficients → beta-min at rate σ√(𝐋_n/n); reported model only → every certified endpoint **and uncertified runs**;
"contains S₀" → "= S₀" under a near-orthogonality floor, plus an explicit inequality on the excess set in general.
**Answers to the brief's questions:** "= S₀ up to a controlled set" — yes in the form (EC′) and SCR-C; no general bound
on |Ŝ∖S₀| is possible from the certificate alone (reviewers' constructions of locally optimal strict supersets);
q_n enlarged — yes; floor weakened — yes.

## 3. Status per clause
| Clause | Status | Evidence |
|---|---|---|
| CC1-CC6 (code facts) | CHECKED | R01 (f.7), R05 (f.11, full code), sweep R07, both council seats (G6 PASS); N0: Python score = core F to 6e-13 on 16,004 models |
| L1 (score algebra), L2 (events) | PROVED-CHECKED | R03 all items CORRECT; R07 ledger; council |
| SCR-A, (A∞), SCR-A°, (A°∞), A1, A1° | PROVED-CHECKED | R03; R06 "SCR-A and SCR-M are proved"; R07; council |
| Lemma B (B1, B2, B2°, B2d, B3) | PROVED-CHECKED | R03 (B1-B3, B2°), R05 (B2d), R07 |
| SCR-M, M1-M6, SCR-G | PROVED-CHECKED | R05 (new mathematics correct), R05b/R05c (statement), R06, R07, council; N4: 105,955 gap checks, 0 violations |
| L5.1 (EC′), L5.2, SCR-C, SCR-R | PROVED-CHECKED | R04 (v2 form), R05 (v3 form), R07, council |
| SCR-N and its two consequences | PROVED-CHECKED | R04, R05, R07, council |
| Frequency of {certified, sparse} in practice | NUMERICS ONLY (not a theorem) | §5 |

## 4. Review trail (all reports verbatim in `reviews/`, with dispositions)
| Step | Reviewer | Verdict |
|---|---|---|
| R01 statement lock (v1) | gpt-6.1-sol high | DO-NOT-LOCK: 1 blocker, 3 major → fixed (v2) |
| R01b re-lock (v2) | gpt-6.1-sol high | **LOCK** |
| R02 "better theorem" (sharpness gate) | gpt-6-astra high | strictly better statements exist → proposals 1-5 adopted (v3), 6 not adopted |
| R03 lemma check L1-L4 | gpt-6.1-sol high | 27 items CORRECT (2 with minor fix) |
| R04 lemma check L5-L6 | gpt-6.1-sol high | claimed results correct; an unclaimed remark false → removed |
| R05 v3 delta check | gpt-6.1-sol high | new mathematics correct; 3 overstated summaries + 7 minor → fixed (v3.1) |
| R05b / R05c re-lock | gpt-6.1-sol high | 1 major wording + 3 minor → fixed; **LOCK (v3.2)** |
| R06 independent mid-point | gpt-6-astra high | **CONTINUE** ("SCR-A and SCR-M are proved") |
| R07 exhaustive sweep | gpt-6-astra high | 0 blocker, 3 major (all in ASSUMPTION_MAP labels), 9 minor → all fixed |
| Council C1 | gpt-6-astra high / Claude Opus 5.5 high (claudeAgent) | **9.3 / 8.9, all gates PASS** (round 1); 2 minor + 4 notes applied post-pass |
Citation check: `citecheck.py` → `reviews/CITECHECK.txt` (31 citations, 20/20 content tokens, 0 failures).
Incident: the T3 server restarted mid-run; two lemma reviews had already written their reports; the numerics batches
turned out to be still alive, so my relaunch briefly doubled them — all were stopped, outputs validated
(`numerics/validate_out.py`) and the missing work rerun once.

## 5. Numerics
**How often does the printed condition hold? (N1: production core, main @ 2252d57 = HEAD core, n = 100, p = 400 = 4n,
s₀ = 4, σ = 1, strong = coefficients (1.4, −1.0, 1.8, −1.2), 10 fits per cell launched; `numerics/SUMMARY_N1_N2.md`.)**
| design | signal | fits finished / launched | certified | certified and size ≤ 8 | move cap hit | reported model ⊇ S₀ | = S₀ | certified, sparse, truth missing |
|---|---|---|---|---|---|---|---|---|
| independent | strong | 10 / 10 | 10 | 10 | 0 | 10 | 9 | 0 |
| independent | weak (0.35×) | 10 / 10 | 10 | 10 | 0 | 1 | 1 | 9 |
| AR(0.7) | strong | 10 / 10 | 10 | 10 | 0 | 10 | 10 | 0 |
| AR(0.7) | weak (0.35×) | 10 / 10 | 10 | 10 | 0 | 1 | 1 | 9 |
| equicorrelated 0.5 | strong | 5 / 10 | 5 | 5 | 0 | 5 | 5 | 0 |
| equicorrelated 0.5 | weak (0.35×) | 10 / 10 | 10 | 10 | 0 | 0 | 0 | 10 |
| 3-factor | strong | 7 / 10 | 7 | 7 | 0 | 7 | 7 | 0 |
| 3-factor | weak (0.35×) | 9 / 10 | 9 | 9 | 0 | 0 | 0 | 9 |

Totals: 71 of 80 fits finished, all with status completed; **71/71 certified, all with reported size ≤ 5**; no move cap was hit; start modes had 0-4 variables (no dense start at this size).

Reading. (a) **The condition fires**: every finished fit was certified with a small reported model, in all four
designs, including equicorrelated and 3-factor designs at p = 4n. (b) With strong signals the certified model
contained S₀ in 32/32 fits (= S₀ in 31). (c) With weak signals (below the visibility threshold) certified sparse
models missed truths in 37/39 fits — the certificate alone guarantees nothing; the visibility hypothesis is what
carries the theorem. (d) **Caveat (selection):** 9 fits — 5 of the 10 equicorrelated strong-signal fits, 3 of the 10
factor strong-signal fits and 1 weak factor fit — had not finished after 0.8-3.1 h (their finished siblings took
6-24 min) and were stopped (`numerics/n1_unfinished.txt`); their certification status is unknown, so the frequencies
for these two designs are conditional on finishing. Slow calibration (escalation) is the likely cause, not verified.
(e) No move cap was hit and no start mode was dense at this size, so SCR-G's capped-search case was not exercised by
N1 (it is exercised by the Python search numerics N4).

**Boundary violations (N2: own implementation of the coded search, 24 starts per draw, 10 draws per scenario).**
- Assumptions hold (iid, AR(0.7), strong signals): no locally optimal model of any size missing a truth (0/10, 0/10).
- Visibility violated — weak signals 9/10 draws, masked pair 10/10, twin of each truth at correlation 0.99 / 0.999:
  7/10, 10/10 draws have a sparse locally optimal model missing a truth. The conclusion fails, as it should.
- Sparse floor violated but visibility intact (noise columns pairwise correlated 0.98): 0/10 — the floor of the card
  was improvable, and is now replaced.
- Equicorrelated / 3-factor / duplicated-noise designs with **mixed-sign truths at n = 100**: 1/10 draws each has a
  sparse locally optimal model missing truths (noiseless visibility ratio 0.80-1.23 there: the margin is not met at
  this n because truths mask each other under the common factor). These models are 3-26 score units below S₀, and
  the production fits (N1) did not report them.
- Exact recovery: locally optimal strict supersets of S₀ exist under correlation (9/10 draws with correlated noise
  columns; 2-4/10 in equicorrelated/factor designs; 0/10 iid, AR) — "contains" cannot be upgraded to "equals" without
  a condition like SCR-C's.
**Lemma falsification:** N3 (L1-L6 identities/inequalities, event frequencies) and N4 (SCR-M, M3, M5): no violation.

## 6. Open items and recommended next step
1. **Not covered:** |Ŝ| = K; truths masked by a proxy inside the model; a lower bound for the entropy term when q ≥ 1;
   an asymptotic exact-recovery theorem in terms of (α, ω). R02's proposal 6 (quadratic contrasts over all legal moves,
   including swaps at K) is the route; it needs a primitive corollary before it is worth a ticket.
2. **Decision D1 input:** at n = 100, p = 400 the certificate fired in every *finished* factor and equicorrelated fit
   and, with strong signals, the reported model equalled S₀ (12/12); but 8 of the 20 strong-signal fits in these two
   designs did not finish within 0.8-3.1 h locally. Two things should be run on NOTS (deterministic seeds; scripts in
   `numerics/`): the 9 unfinished fits, and larger p/n (e.g. n = 200, p = 2000), where dense start modes and capped
   LS0 runs — the case SCR-G is for — are expected. The theoretical risk for strong factors at p ≫ n is visibility
   itself (mixed-sign truths under a common factor mask each other at moderate n), not the certificate.
3. **Optional method remark (not required):** printing, for each archive, the score gap `hpm_F − scanned_F` of the
   last scanned centre would make SCR-G(ii) directly readable from the output (the numbers are already in the fit).
4. Paper: state SCR-A/A1 as the theorem, SCR-G as its corollary for uncertified runs, SCR-C as the exact-recovery
   remark, SCR-N as the sharpness remark; SCR-M and (EC′) in the supplement.

## 7. Registry record (PROTOCOL item 7)
**Assumption ids:** G (Gaussian errors, fixed standardised design); EX-A; GAP(𝓗) (positive deterministic gap);
SV(q,x) = MC; SV°(q,x) = MC°; SV∞; ID(q) identifiability margin; DF(q) directional floor; AF(q) anchored floor;
SF(q+s₀) sparse eigenvalue floor; NF(q) near-orthogonality floor on supersets of S₀.
**Implies:** SF(q+s₀) ⇒ AF(q) ⇒ DF(q) (B3, B2d); DF(q) + beta-min/growth conditions ⇒ SV∞ / SV°∞ (A1, A1°);
ID(q) + ‖θ*‖₁ control ⇒ lower bound on Γ_n (B1); SV(q,x) ⇒ GAP({|S| ≤ q}) and SV°(q,x) ⇒ GAP({|S| ≤ q}) (M3, maximising
witness); GAP ⇒ screening of LO models, of near-best scanned centres and of capped endpoints (M1, M2, M5);
NF(q) + screening ⇒ exact recovery (SCR-C). **Relations to existing results:** independent of the start/LS0 theorems
(GROW, UNI-0, PXN, GEN) — no start, leakage or block condition; it does not use and is not implied by posterior
concentration (T03♯/UNI-P); combined with "S₀ is the unique maximiser of F" it gives: the best subset of a sparse
certified Ŝ is S₀ (not coded; remark only). SF is not implied by the posterior theorem's hypotheses: T03♯ needs a
floor only on S₀ ∪ J with |J| ≤ j₀ (`Theory_work/Wave2/SR/CRITIQUE_fable.md:50`), whereas SF asks all sets of size
q_n + s₀ — which is why the bridge was weakened to DF.
**Sharpness record:** visibility threshold sharp at q = 0 with constant 1 (SCR-N, proved, for the statement about LO
models); SF, fixed coefficients, q_n = o(n/log n), p ≤ n^A, s₀ fixed (for screening), the certificate itself, the
model-count entropy and the total scale τ_n were flagged `improvable` and improved; ID/DF/AF/NF are sufficient, not
shown necessary; open: entropy term for q ≥ 1, size K. Details: `ASSUMPTION_MAP.md`.

## 8. Files
`STATEMENT.md` (v3.4), `CODE_CHECK.md`, `ASSUMPTION_MAP.md`, `PLAN.md`, `LOG.md`, `REPORT.md`, `citecheck.py`;
`lemmas/L1_score.md` … `L7_master.md`; `reviews/` (R01, R01b, R02, R03, R04, R05, R05b, R05c, R06, R07, C1 reports,
dispositions, CITECHECK.txt, reviewers' scratch); `numerics/` (`scr_lib.py`, `scr_fit.R`, `n0_fidelity.py`,
`n2_boundary.py`, `n3_lemmas.py`, `n4_master.py`, `summarise.py`, `validate_out.py`, runners, outputs `n0_out.txt`,
`n3_out.txt`, `n4_out.txt`, `n1_raw/`, `n1_unfinished.txt`, `n2_out/`, `SUMMARY_N1_N2.md`, `core_copy/` = production
core with hashes; the compiled build cache was removed).
