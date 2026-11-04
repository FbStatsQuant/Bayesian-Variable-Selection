# F-REFEREE — RESPONSE_PLAN: the authors' best honest response, and the tasks it needs

Companion to `REFEREE_REPORT.md` (same branch, same date). §1 is the response letter the authors could honestly send
after the tasks in §3 are done; it is written point by point against M1–M8, and it promises nothing that is not either
already a candidate on a pushed branch or a bounded task below. §2 is the one tier-raising change. §3 is the ranked list
of concrete tasks as ready-to-run specs in the style of `theory_campaign/tasks/*.md`. §4 says what the response must
concede with no task behind it.

Status words are the campaign's. "Candidate" means a pushed, unreviewed proof on an in-flight branch; nothing is
promised as PROVED in the response until cross-family review says so.

---

## 1. The response, point by point

**M1 (asymptotic theory, n = 200 simulations).** We agree that no theorem quantifies the n = 200 numbers, and we now say
so once, before the theorems, instead of nine times after them. We add (task R2) a scaling study on the family the
theorems are proved for (LH, c ∈ {1, 2, 3}, n from 400 to 25,600, production code), which shows the start-mode miss,
the pilot-stage discovery, and P(Ŝ = S₀) crossing the predicted thresholds at n ≈ 10³–10⁴; the mechanism of Theorems
2, 3 and 5 is therefore visible three orders of magnitude below the proof thresholds of Theorem 1. For Theorem 1 we
give the explicit constant c₀(s₀, A) and the first-n table (task R9); we do not claim the theorem bites at n = 200. We
keep the exact finite-n statements (Theorem 4, Theorem A, Lemma LS-score, the T02 tail, Proposition 2) and say that at
the study's size the error is carried by the posterior term, which we observe (565/2,394 posterior misses, 0 discovery
misses) and do not prove to be small. The posterior-miss rates at n = 200 are the subject of a finite-n analysis
(O-SWAP, candidate) that we will include only if it survives review.

**M2 (LS0).** We agree that the headline theorem must be about the algorithm that produced the tables. The revised
Theorem 5(b) is stated for v3 without LS0 on LH, through the pilot-stage route (O-BGIBBS BG1) or the confinement route
(W5-B2ENV B2-LH), whichever survives cross-family verification (task R1); LS0 becomes a remark: a deterministic,
post-hoc-addable extra search that removes the pilot-stage temperature condition and costs at most
1 + (ℓ+1)max_k[p + k(p−k)] scores. If the O-LS0 pilot on the 2,400 datasets (task R12) shows changed HPMs, we report every
change; LS0 can only reveal posterior misses, never create discovery misses, and we say so with the one-line proof.
We also say plainly that (b1) is "favourable at the reference S°, then c greedy moves", which is a description, not a
weakness: it is exactly what cancellation masking looks like from the start's point of view.

**M3 (no-LS0 routes conditional; n = 200 mechanism unproved).** Agreed as to the draft. The revision has one explicit
family (LH) on which the unmodified method scores S₀ with probability → 1 for every fixed c ≥ 1 (task R1), and the
general conditional routes (b1′)/(b2) move to the supplement as sufficient conditions, with counterexample C1 kept in
the text as the reason confinement, not bridge mass, is the right hypothesis. For the study's own designs we claim no
theorem: the n = 200 behaviour (Gibbs flips deliver, local search repairs nothing) is reported as evidence for the
route, with the E_LS ledger extraction (S-ELS, running) to say whether the final centres were ever in the repairable
region.

**M4 (favourable regime trivial; what tempering buys).** We add the Separation Theorem (W7-SEP, running; task R4 is its
verification) as the conceptual spine: on LH with c ≥ 2, start-only discovery needs a super-polynomial budget, one-shot
importance correction has χ² → ∞, and v3 finds S₀ with a polynomial budget. Theorem 5(a) becomes a corollary ("the bridge
is harmless when it is unnecessary"). For the reported quantities in the masked regime we add Proposition M1/M2 of
F-MASKPIP (task R8): evidence-weighted PIP accuracy in every regime, so PIPs can be wrong only on islands whose evidence
is grossly low.

**M5 (2^B; Theorem 6's budgets).** The 2^B-free start rate on iid designs with the actual partition (W3-PXN Lemma B,
W5-FAVIID) becomes the primary clause of Theorem 2(iii) after cross-family verification (task R6); the exact-Gram 2^B
rate becomes a remark with its numerical range stated. For Theorem 6 we replace the premise on the realised T_n by a
theorem on a family (task R5): the calibration's ESS bisection gives T_n ≤ C log(1/Δ_n)-type bounds on ORTH/FAV, so
(T_n + 1)Δ_n → 0 is proved, not assumed. If R5 fails, Theorem 6 is stated with the realised T_n and labelled as such.

**M6 (novelty; mixing-time literature).** We add a paragraph "Relation to computational guarantees for Bayesian variable
selection" (task R3) that states what the mixing results of Yang–Wainwright–Jordan (2016) and Zhou–Yang–Vats–Roberts
(2022) imply on LH (we expect: rapid mixing of an informed MH from any sparse start, hence HPM discovery), and what
Theorem 5 adds: a budget indexed by n with an explicit polynomial score count, an unbiased evidence estimate with an
output-level certificate, an exact start whose masking is proved and repaired, and the separation from start-only
methods. We delete every phrase that could be read as "first consistency theorem for a BVS sampler" and adopt the
wording "a BVS-specific construction and analysis within established SMC principles". If LH violates those papers'
conditions, we say which and why; if it satisfies them, we say that too.

**M7 (evidence and PIPs in the masked regime; Markov bound).** We add Proposition M1/M2 (task R8) and keep Theorem 6 as
the favourable-regime consistency statement. We state in the simulation section that 0.05Ẑ is a one-sided certificate,
that the reported pooled PIP is biased by −Cov/Z (Proposition 2(c)) and we report the islandwise product, which is
unbiased. We do not promise a two-sided band (PW2) unless O-PW2 delivers.

**M8 (verification, cost corollary, implementation facts).** T32(i) is proved as a deterministic count (W7-SEC,
running; task R7 also uses it to make U a model event). SR and GUARD move into the algorithm's definition in the method
section, with the code audit (W5-LOCKBOOK, task R10) cited as the reference-implementation check. The supplement is
written as a self-contained document (task R11), and no verdict word of the campaign appears in the paper.

**Minor points.** All twenty are accepted; m1, m2 (notation clashes), m3–m5 (self-contained statements), m7, m8 (no
campaign bookkeeping in theorem text), m14 (P(U) not a model probability) and m20 (§6 too long) are handled by task R11
and R7; the rest are edits.

---

## 2. The one change that most raises the tier

**Make Theorem 5(b) a theorem about v3 as run, on LH, and show the predicted transition with the production code.**

Why this one: it answers M2 and M3 completely, half of M1 and M4, and it changes what the paper *is*. Tonight the paper
is "a careful asymptotic theory of a modified algorithm, plus simulations of the unmodified one at a size the theory
does not reach". After the change it is "a theory of the algorithm that produced the tables, whose mechanism is
exhibited on the family where it is proved, from n ≈ 10³". That is the difference between a Series B major revision
and a Series B paper.

What it needs: R1 (verify one no-tweak route) and R2 (the scaling study). R1 is cheap (one Astra or Opus review run per
route). R2 is compute (NOTS, roughly 3 × 4 × 2 × 100 fits at n up to 25,600 with p ≈ n^{1.25} capped at the code's limits;
a pilot at n ∈ {400, 1600} first).

What it does not need: LS0, a new family, or any change to the 2,400 fits.

---

## 3. Ranked task specs

Ranking is by value to the response divided by cost. R1–R3 are load-bearing; R4–R8 raise the tier further; R9–R12
are hygiene the referee will check. Each spec follows `theory_campaign/tasks/*.md`: paper role, claim, inputs,
deliverable, status rules. Every task writes only under `theory_campaign/<ID>/` on branch `theory/<ID>`, commits and
pushes early and often, uses the protocol's status words, and never upgrades a status.

### R1. V-NOTWEAK: cross-family verification of the no-LS0 masked instance on LH

**Paper role:** Theorem 5(b) for the algorithm as run. The single most valuable review in the campaign.

**Claim to verify.** On LH (exact Gram, W1-EXP Thm 5 setting), for the unmodified v3 and every fixed c ≥ 1,
P(𝒪 ∩ {Ŝ ≠ S₀}) → 0. Three candidate routes exist; verify them in this order and stop at the first that is VERIFIED:
1. **O-BGIBBS** (`theory/O-BGIBBS`): Lemma R (multi-flip round lemma), Theorem BG1 (pilot first-stage discovery:
   P(z ∉ 𝒮_cal | data) ≤ Hπ₀(𝒜) + e^{−Hπ₀(x°)/8} + 1/K + exp{−Hβ/(1 + 2Kρ_𝒩)}), code fact F (φ₁ ≥ min(1, 1/T_e)),
   Proposition LH (structure PROVED, score estimates PROOF SKETCH). The crux is the score estimates in Proposition LH
   and the condition n/(T_e log(p√n)) → ∞. Check especially that the one-round argument uses SR correctly (both Gibbs
   configurations scored) and that the resampling weights e^{φ₁ d} at the pilot's first stage are handled without
   conditioning on the ESS.
2. **W5-B2ENV** (`theory/W5-B2ENV`): Theorem B2-LH under STAB-LH (confinement Prop. CONF at rate O(log^{3.5} n/√n),
   Lemma R1 one-round scoring at φ = 1 with fixed c₀), and Corollary D2-LH (NB′ PROVED on LH, c = 1, Lemma OF). Check
   the junk non-persistence step and whether STAB-LH is implied by |ψ| < ρ or is a genuine extra hypothesis (the run
   says it fails at (ρ, ψ) = (0.85, 0.5)); if extra, state the restricted LH subfamily on which it holds.
3. **O-MIX** (`theory/O-MIX`): Theorem B3 (mixture of the v3 partition and the linked-merge partition, π₀^mix(S₀) ≥
   ½ − O_P(2^{2g} n^{−1/2})). This is a method change (a different start), so it is a fallback only.

**Inputs.** The three branches; W1-EXP PROOF §4 and W3-VEXP (LH inputs); W4-SHARE Prop. M and Lemma PD; W1-T38E D2;
`v3_calib.h:pilot_next_phi`, `v3_engine.h:run_island_s`; `00_COMMON.md`.

**Deliverable.** `theory_campaign/V-NOTWEAK/REVIEW.md`: a verdict table (VERIFIED / GAP / ERROR per step) for each route
examined, counterexamples as scripts, the exact hypothesis list of the surviving route, and a one-paragraph statement
of Theorem 5(b) as it can be printed. Cross-family (Astra) preferred; if Opus, say so.

### R2. LH-SCALE: the mechanism made visible with the production code

**Paper role:** the simulation that connects the theorems to the method (M1, M2, M4). Not theory; a ready-to-run
compute spec for NOTS.

**Design.** Family LH, two realisations: exact Gram (p ≤ n − 1) and iid Gaussian rows (p = ⌊n^{1.25}⌋ capped by the
code's limits). G groups of size g = 9 (so g ≤ B < 2g holds for B ∈ [9, 16]), equicorrelation ρ ∈ {0.6, 0.85}, linked pairs
c ∈ {1, 2, 3} with ψ ∈ {0.3, 0.5} and |ψ| < ρ, hub coefficients β = 1, suppressor −ψβ, s₀ = 2c + 4 visible truths with
fixed coefficients, σ = 1. n ∈ {400, 1600, 6400, 25600}; 100 replicates per cell (pilot: 20 at n ∈ {400, 1600}).
Methods: v3 as run; v3 + LS0 (post hoc, emit_centre = true); iid-start-only baseline (Q = Q_f draws from π₀ followed by
the production local search from each distinct draw, budget-matched); one-shot IS baseline (weights π/π₀ on the Q_f
draws, report ESS and the IS estimate of 1{S = S₀}).
**Record per fit:** S̃₀ Δ S₀ (start-mode miss), π₀(S₀) and π₀(S°) exact, the first stage and round at which S₀ is
scored, the source of that score (table, iid draw, Gibbs flip, swap, local search, LS0), Ŝ = S₀, F(S₀) − F(Ŝ), Ẑ and the
islandwise PIP error, wall time and score count.
**Predictions to check:** π₀(S₀) ≈ p^{−c} n^{−c/2}; 1 − π₀(S°) ≈ C n^{−1/2} (iid: no 2^B); S₀ first scored in the pilot's
stage 1 once n/(T_e log(p√n)) is large (BG1), otherwise later in the bridge; P(Ŝ = S₀) → 1 for v3 and → 0 for the
start-only baseline at c ≥ 2; IS ESS → 0.
**Deliverable.** `theory_campaign/LH-SCALE/REPORT.md` with the tables, the prediction-vs-observed plot per quantity,
and the SLURM scripts; raw results as `results/*.jsonl` with seeds.

### R3. MIX-POS: positioning against the rapid-mixing literature

**Paper role:** the "Relation to computational guarantees" paragraph (M6). Reading and reasoning only.

**Claim to settle.** Whether LH (exact Gram and iid) satisfies the hypotheses of (a) Yang, Wainwright & Jordan (2016,
AoS 44(6)) and (b) Zhou, Yang, Vats & Roberts (2022, JRSS-B 84(5)); and, if so, what their theorems conclude on LH (mixing
time in n, p; starting state requirements; model-size bound s; the beta-min constant). Then state precisely what
Theorem 5 adds and what it does not. Also check Zanella & Roberts (2019) §4.5 and Griffin, Łatuszyński & Steel (2021,
Biometrika) for the same purpose. Verify every citation against the source PDF (titles, volumes, theorem numbers,
hypothesis names); the referee report quotes them from memory and says so.
**Inputs.** The papers (fetch to `Papers/` if absent and record the source); W1-EXP §4 (LH); T03♯ hypotheses; T38(c).
**Deliverable.** `theory_campaign/MIX-POS/REPORT.md`: a hypothesis-by-hypothesis table (their condition | holds on LH? |
proof or counterexample), their conclusion on LH, a draft of the paper paragraph (≤ 250 words) and a draft of the
one-sentence contribution statement. Honest status: if their results subsume HPM discovery on LH, say so.

### R4. V-SEP: verification of the Separation Theorem

**Paper role:** the conceptual spine (M4). Depends on W7-SEP delivering.

**Claim to verify.** W7-SEP's theorem: (a) start-only methods fail (iid π₀ draws + local search score S₀ with probability
→ 0 for every polynomial budget on LH with c ≥ 2, unless the greedy basin of S₀ contains S̃₀, quantified via Theorem A /
TD′); (b) one-shot importance correction fails (χ²(π‖π₀) → ∞, F-DRAFT Theorem W; O-WSTAB); (c) v3 succeeds (citation of
(b1) with LS0 and of the R1 route). Check the budget exponents, the use of R-T20(i)'s n^{−c/2} law, and that (a) does not
silently assume ℓ < Φ(S̃₀).
**Deliverable.** `theory_campaign/V-SEP/REVIEW.md` with the verdict table and the printable statement.

### R5. T26-BUDGET: Theorem 6 with a proved stage count

**Paper role:** Theorem 6's premise (M5, m15).

**Claim to prove.** On ORTH (and on FAV of W5-FAVIID if R6 verifies it), the calibration's ESS bisection rule produces a
realised stage count T_n with T_n ≤ C₁ + C₂ log(1/Δ_n) (or any bound such that (T_n + 1)Δ_n → 0 in P₀-probability);
hence (P1) holds and Theorem 6(A-i)(A-ii) follow with no premise on the run. Inputs: `v3_calib.h` (the bisection on the
ESS of e^{(φ′−φ)d}), W2-T26 Lemmas 1–3, W1-EXP Thm 1/6, W2-T26 Prop. C (ORTH). If the bound fails because the grid can
over-refine, state the weakest extra rule (e.g. a cap T^max_n = C log n) under which it holds and whether the cap is
ever active in the study (it is not: realised T ∈ {1, 2}).
**Deliverable.** `theory_campaign/T26-BUDGET/REPORT.md` with the statement, proof, and the exact p = 18 numerics
extended with the realised T_n.

### R6. V-FAVIID: cross-family verification of the 2^B-free start rate

**Paper role:** Theorem 2(iii) primary clause, Theorem 5(a)'s relevance for study-like designs (M5).

**Claim to verify.** W3-PXN Lemma B / P1–P4 (exact Beta laws of the per-block ratios independent of y; partition =
groups w.p. → 1; 1 − π₀(S°) = O_P(√(log n/n)) without 2^B) and W5-FAVIID's statements on FAV (block-diagonal iid rows,
groups ≤ 16, S1/S3/S4/S6 instances). W5-VMASK has a same-family check of W3-PXN; this task is the cross-family one.
**Deliverable.** `theory_campaign/V-FAVIID/REVIEW.md` with the verdict table and the hypothesis list that survives.

### R7. U-MODEL: make the no-output event a model event

**Paper role:** Theorem 4 and Theorem 5(0) (m14, M8).

**Claim to prove.** (i) T32(i): a deterministic ceiling N_score(n, p, B, 𝓒) on the number of score evaluations of the
potential run under the v3 budgets (W7-SEC is on this; reuse if done). (ii) Define the guard by a score-count budget
N_max(n, p) ≥ N_score; then U ∈ σ(R̄) and U = ∅ on the potential run under EX-A, so Theorem 4 reads
P(Ŝ ≠ S₀) ≤ 2E₀δ₁ + P(S₀ ∉ 𝒮̄) with no P(U) term. (iii) State what changes if the guard stays wall-clock: the result is
conditional on the operational element Ξ, and the stop rate is an empirical fact outside the model. Check with the code
whether a score-count guard is a one-line change (`v3_runtime.h`).
**Deliverable.** `theory_campaign/U-MODEL/REPORT.md` with T32(i)'s proof (or citation), the restated Theorem 4, and the
code note.

### R8. V-MASKPIP: verification of the masked-regime evidence/PIP statements

**Paper role:** Theorem 6′ (M4, M7).

**Claim to verify.** F-MASKPIP Proposition M1 (E_𝓒[(Ẑ_r/Z)·max_j|PIP̂_rj − 1{j∈S₀}|] ≤ δ₁ + ρ̄ + u_π, every regime, every
frozen grid), Corollary M2 (the two tail statements), Proposition M3 (no conditional evidence theorem). Check the use of
locked T12(i.a,i.b), T15 and T23(ii) and that nothing conditions on completion.
**Deliverable.** `theory_campaign/V-MASKPIP/REVIEW.md` and the printable statements.

### R9. T03-CONST: explicit constants and first-n table for Theorem 1

**Paper role:** M1(ii), the honest finite-n disclosure of Theorem 1.

**Claim to prove.** An explicit c₀(s₀, A) in BM(c) (the proof gives L* = max{4C_*, 32[s₀(A+1) + 2]}; make C_* explicit in
σ*², M, φ₀), and for the study's (p, s₀) ∈ {(500, 14), (1000, 14)} the smallest n at which each deterministic step of
W1-T03R's proof holds (the q_n ≤ ½ condition and all others), reproducing W2-VT03R R1. Optionally: the sharp-constant
conjecture W′ stated, not pursued.
**Deliverable.** `theory_campaign/T03-CONST/REPORT.md` with the constant, the table and the script.

### R10. CODE-AUDIT: SR, GUARD, emit_centre, scan-before-limit, IND-T stream reading

**Paper role:** the algorithm's definition (M8, m13). Operations, not theory; reuse W5-LOCKBOOK if it reports.

**Claim to check, in code.** SR (`v3_engine.h::step_gibbs`: both configurations evaluated and offered to the ledger
before the accept draw; no call site disables emission); GUARD (`v3_runtime.h`, `v3_engine.h`, `v3_core.cpp`: no guard
path reads an RNG or changes a setting; a run no guard stops is the R̄ computation); the local search's scan-before-limit
rule (`local_search` lines 369–420); LS0's `emit_centre`; IND-T's sequential stream reading (`run_island_s`). VAL-FP:
one replay in extended precision on 10 fits to measure η, ε of Proposition 2(f).
**Deliverable.** `theory_campaign/CODE-AUDIT/AUDIT.md` with line-referenced findings and the VAL-FP numbers.

### R11. SUPP-WRITE: the self-contained supplement and the notation pass

**Paper role:** M8(iii), m1–m8, m20. Sonnet-level editorial work with an Opus check of each transcribed statement.

**Task.** Produce `supplement.tex` with complete proofs transcribed from the source branches (S.1 T02/T03♯; S.2 T07;
S.3 T22/EXP′/CL/LH; S.4 Theorem A, LS-score, Lemma M, LH-LAT, Theorem W; S.5 Theorem B′, IND-T; S.6 Lemma RO, T21;
S.7 T38 (W6-FIXREV1 version); S.8 T26; S.9 T12/T31), with every hypothesis defined in the paper's notation, the two
clashes (m(S), D_S) resolved globally, branch names and verdict words removed, the conditional routes and §6 items 4–9
moved in, and a cross-reference table (paper label | source branch | source label) kept as a non-typeset appendix for
the authors.
**Deliverable.** `theory_campaign/SUPP-WRITE/supplement.tex` compiling, plus `XREF.md`.

### R12. LS0-DIFF: the LS0 pilot on the 2,400 datasets

**Paper role:** M2 option (2), or the LS0 remark if option (1) succeeds. Compute (Owls, O-LS0 is running it).

**Task.** Complete O-LS0; report for every fit whether the reported HPM changes, in which direction (correct→wrong,
wrong→correct, wrong→wrong), F(old) − F(new), scores added, wall time; confirm the one-line claim that LS0 never creates a
discovery miss (every change has F(new) > F(old)).
**Deliverable.** `theory_campaign/LS0-DIFF/REPORT.md` with the table by scenario and signal scale.

---

## 4. What the response must concede with no task behind it

1. No theorem will describe the study's dilution masking at n = 200 with s₀ = 14 (fixed-s₀ theory makes it vanish;
   a sharp-constant T03 for growing s₀ is CONJECTURE W′ at P(provable) ≈ 0.3). The paper says so once.
2. Theorem 1's constants will remain far from the executed signal; the first-n table (R9) makes this precise, not
   smaller.
3. Route (b2) in general (DELIV for an arbitrary BVS family) stays OPEN; only LH instances are claimed.
4. Masked-regime consistency of Ẑ and PIPs is not claimed; Prop. M1/M2 are accuracy-weighted-by-evidence statements,
   not consistency.
5. No comparative superiority over SuSiE, SSL or an informed MH is claimed from any theorem; the tables are evidence
   about targets as much as algorithms.
6. If R1 fails on all three routes, Theorem 5(b) stays an LS0 theorem, the method is presented as v3 + LS0 from the
   first page, and R12's diff is reported in full. That is still a publishable paper; it is a lower tier.
