# R01 — Statement-lock review of W2-FAC-XA (STATEMENT v0 + PLAN)

Reviewer: Claude Opus 5.5 (Claude Personal), a fresh cross-family seat (the lead is OpenAI), briefed to break the statement.
Date: 2026-11-09. Scope: statement lock only, so no proof work. The only numerics run were for the norm question
(reviews/R01_scratch/gram_norms.py, output reviews/R01_scratch/gram_norms_out.txt).

Sources read: W2-FAC-XA/STATEMENT.md, PLAN.md, LOG.md; Wave2/PROTOCOL.md, Wave1C/PROTOCOL.md, Wave1/PROTOCOL.md;
W2-FAC-B/STATEMENT.md (v3.1), W2-FAC-B/REPORT.md, W2-FAC-B/reviews/R01_statement_lock_sol.md; W2-FAC-A/STATEMENT.md
(v1.2), W2-FAC-A/REPORT.md (flags + result), W2-FAC-A/lemmas/L5_random_instances.md (norm handling);
State_of_Project/sections/02_method.tex:180-215 (blocks/partition). I did not open or contact W2-FAC-X.

## VERDICT: **LOCK-WITH-CHANGES**

The target is meaningful and honestly framed: it is an open extension, no rate is claimed, and narrowing has to be logged.
It also does not quietly assume FAC-B's missing swap margin. But in its current form it is not lockable, for these reasons:
- C2 is ambiguous: it does not say whether the exact-Gram case and the iid-row case are one target or two.
- The claims are not numbered and no hypotheses are attached to each claim.
- The key lemma's required conclusion (path length within the cap) is never stated.
- "Safe deletion" is used without a definition.
- The random-design transfer of T03♯/(H0) and of the partition has no stated mechanism.
- FAC-A's existing coverage is not quantified, so the genuinely new range is invisible.
- The plan's perturbation step does not yet commit to a norm. The suspected absolute-vs-relative issue is **real**: an
  absolute √(p/n) operator-norm bound is false for these designs (§A).

None of these items is a counterexample to the target. Apply the required changes R1–R12 below and log them in LOG.md.
A fresh lock review is needed only if the lead changes anything beyond R1–R12. R3 and R4 (C2 split and plan) are the
largest changes. If C2 is re-scoped further than R3/R4 allow, re-submit it.

---

## A. The absolute-vs-relative Gram norm issue (investigated; confirmed)

**Claim checked.** "‖R̂ − Σ‖_op ≲ √(p/n)" for iid Gaussian rows with Σ = (1−ρ)I + ρ11ᵀ (or one factor
Σ = diag(1−λ²) + λλᵀ). R̂ is the method's centred and standardised correlation Gram. The plan (step 3) already suspects
this bound. FAC-B's frontier note states it as fact: `W2-FAC-B/REPORT.md:123`, "The sample Gram is not exactly compound
symmetric (‖R̂ − Σ‖ ≈ √(p/n))".

**Verdict: false as an absolute operator-norm statement. The correct absolute order is ≍ p/√n.** Mechanism, for a
one-factor representation x_j = λ_j f + √(1−λ_j²) e_j:
1. **Common factor-variance fluctuation.** The sample variance of f is 1 + O_P(n^{-1/2}). Even after the columns are
   standardised, this leaves an essentially compound-symmetric shift ρ → ρ̂_n = ρ + O_P(n^{-1/2}) along 11ᵀ. Its
   operator norm is ≍ p/√n.
2. **Factor × idiosyncratic cross terms.** Let v_j := n⁻¹Σ_i f_i e_ij ~ N(0, 1/n). The cross term v1ᵀ + 1vᵀ (scaled by
   the loadings) has operator norm ≍ ‖v‖·‖1‖ ≍ √(p/n)·√p = p/√n. It is **not** of compound-symmetric form.
3. **Idiosyncratic Wishart part.** This part has norm ≍ √(p/n), which is the only piece the √(p/n) heuristic captures.

**The relative (whitened) deviation is √(p/n).** In ‖Σ^{-1/2}(R̂ − Σ)Σ^{-1/2}‖_op the spike eigenvalue ≍ ρp divides
terms 1 and 2:
- Term 1 becomes O(n^{-1/2}).
- Term 2 becomes ≍ ‖Σ^{-1/2}v‖·‖Σ^{-1/2}1‖ ≍ √(p/n)·O(1).

The bound passes to every principal sub-Gram: for every T ⊆ [p], ‖Σ_TT^{-1/2}Δ_TTΣ_TT^{-1/2}‖ ≤ ‖Σ^{-1/2}ΔΣ^{-1/2}‖
(Rayleigh quotients over a coordinate subspace). The score only uses sub-Grams G_T and H_T, so this is the useful form.

**Numerics** (R01_scratch/gram_norms.py → gram_norms_out.txt; 3 reps each; "1F" is loadings linspace(0.3, 0.9)):

| design | n | p | ‖Δ‖_op | p/√n | √(p/n) | whitened ‖·‖ | max row ℓ₂ | max entry |
|---|---|---|---|---|---|---|---|---|
| CS 0.5 | 4000 | 200 | 1.49 | 3.16 | 0.224 | 0.48 | 0.28 | 0.047 |
| CS 0.5 | 16000 | 400 | 2.06 | 3.16 | 0.158 | 0.32 | 0.25 | 0.026 |
| CS 0.5 | 64000 | 400 | 0.63 | 1.58 | 0.079 | 0.16 | 0.10 | 0.013 |
| 1F | 16000 | 400 | 1.84 | 3.16 | 0.158 | 0.34 | 0.27 | 0.033 |

Reading the table:
- The absolute norm tracks ≈ 0.4–0.65 · p/√n, and is 7–13 × √(p/n).
- The whitened norm tracks ≈ 2√(p/n), the Marchenko–Pastur edge (1+√γ)² − 1.
- The max row ℓ₂ norm is ≈ 1.2–1.7 · √(p/n). The max entry is ≈ 1.2–1.7 · √(log p/n).

The absolute norm exceeds 1 at p/√n ≳ 2 (it is 2.06 in the n = 16000, p = 400 row). So an argument that uses an
absolute √(p/n) bound would be wrong, not just loose.

**Consequences for the plan.**
- For a < 1/2 the absolute norm still → 0, but slower than √(p/n). Quadratic forms in the spike direction are an
  order larger than the absolute √(p/n) bound would allow: 1ᵀΔ1 ≍ p²/√n against the p·√(p/n) that bound gives.
- If a lemma multiplies ‖Δ‖_op by a growing factor, the constraint shifts. Example: FAC-A's (AG) envelope
  δ_n√(p log log n) needs a < 1/3 with δ_n ≍ p/√n, but a < 1/2 with δ_n ≍ √(p/n).
- FAC-A itself is not affected: `W2-FAC-A/lemmas/L5_random_instances.md:34` bounds ‖R̂ − Σ‖_op by the Frobenius norm
  pδ'_n, a valid absolute upper bound.
- On the path every visited T contains S₀. Under the convention Y = Xθ + Cε, μ ∈ col(X_T) exactly, so on the path the
  Gram error enters only through the noise geometry: z | X ~ N(·, σ²(n−1)R̂). That is exactly where the whitened norm
  applies. The signal multiplies Δ only for truth-deleting moves and start tables, where the margins are of order n.

**Required change R1 (binding).** STATEMENT.md and PLAN step 3 must:
- (a) Forbid any absolute-norm bound ‖R̂ − Σ‖_op ≲ √(p/n) for C1/C2 random rows.
- (b) Name, for every perturbation lemma, which norm it uses and prove that bound for R̂ (centred, sample-sd
  standardised): the whitened norm ‖Σ^{-1/2}(R̂−Σ)Σ^{-1/2}‖_op (target O_P(√(p/n))), the max row ℓ₂ norm, the max
  entry norm, or the absolute norm (≍ p/√n).
- (c) Treat the compound-symmetric part of the spike error (ρ → ρ̂_n) separately where convenient: it preserves the
  exact FAC-B reduction with a random ρ̂_n → ρ.
- (d) Not transcribe `W2-FAC-B/REPORT.md:123`'s "‖R̂ − Σ‖ ≈ √(p/n)" as a source fact. It is a frontier remark, inaccurate
  as an absolute statement. Cite FAC-B's actual statement text or this review instead.
- (e) Add to numerics step 1 the norm table above at the planned (n, p, ρ) sizes.

---

## B. Required changes R2–R12

**R2. Number the claims and give each its hypotheses.** Replace the prose "conclusions sought" with numbered claims,
each listing exactly the hypotheses it uses. Suggested set, modelled on FAC-B §4:
- (X1) start mode
- (X2) path / key lemma
- (X3) D_n → 0 and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0
- (X4) delivery P(Ŝ⁺ = S₀) → 1
- (X5) frontier (evidence only)

Applied to C1 and to each C2 subcase, this makes the claims check-able by lemma reviewers, the sweep and the council
gates "hypotheses used = hypotheses stated". State which premise set each claim uses:
- (X3) uses FAC-B §1 premises including CAL, the [M5-0] route.
- (X4) uses Proposition F's full list as in FAC-B (C4), CAL-free, including the A4 preflight terms.

**R3. Split C2 into two named subtargets.** "Exact standardized Gram … then iid Gaussian rows with this population
covariance" is ambiguous. Use:
- **C2-E**: fixed design, XᵀX = (n−1)Σ_n with Σ_n = diag(1−λ_j²) + λλᵀ; requires p ≤ n−1.
- **C2-R**: iid N(m, Σ_n) rows; the method standardises.

For both, state:
- whether λ = λ(n) may vary with n and whether truth positions vary. If λ_{S₀}(n) varies, "fixed nonzero coefficients"
  does not by itself make the signal pattern fixed, so the visibility bound must be uniform in n, which the statement
  already intends.
- the scale on which θ is fixed.
- whether sign flips (FAC-B's Υ_n) are allowed. As written, λ_j ∈ [λ_lo, λ_hi] ⊂ (0, 1) excludes mixed-sign loadings;
  say that this is intended.

C2-E is **not** a perturbation problem. It is FAC-B's frontier (c), `W2-FAC-B/REPORT.md:119-122`: variable-specific
centres break the one-dimensional reduction. Make the order explicit: C2-R is attempted only after C2-E. If that is not
the intent, say how C2-R is reached.

**R4. Plan for C2-E.** PLAN step 3 addresses only perturbation (C1). Add a step for C2-E, or declare C2-E secondary
and conditional on C1 progress. That step must name the obstruction (history-dependent band of width ≈ max|x_T| from
variable-specific centres λ_j x_T) and the intended invariant. One option, as a pointer only and not proof work: the
whitened coordinates x_j/√(1−λ_j²) have Ψ = I and loadings λ_j/√(1−λ_j²), so C2-E is "CS with heterogeneous loadings"
in whitened form. Without such a step, C2 is not a viable planned target. Record it as stretch.

**R5. Define the visibility hypothesis precisely.** Write it as a formula:
c(U, j) := Cov(x_j, μ | x_U) on the Σ_n scale with μ := Σ_{i∈S₀}θ_i x_i, together with inf_n min{|c(U,j)| : |U| ≤ 15,
j ∉ U, (j ∈ S₀ or U ⊉ S₀)} ≥ c₀ > 0.

Also state:
- The diagonal Σ_{jj|U} is bounded in [1−λ_hi², 1], so the absolute bound is equivalent to the normalised bound
  c²/Σ_{jj|U} that the block tables use (FAC-A (TV-pop) form).
- For this one-factor class the condition reduces to finitely many conditions per n:
  - null j, U ⊉ S₀: c(U, j) = λ_j v_U Σ_{i∈S₀∖U}θ_iλ_i, with v_U := Var(f | x_U) ∈ [c, 1];
  - truth j: c(U, j) = (1−λ_j²)θ_j + λ_j v_U Σ_{i∈S₀∖U}θ_iλ_i.

  So the condition is satisfiable and generic. Ask the lead to verify this reduction in a lemma rather than accept it
  from this review. It is offered only as a sanity check that the hypothesis is not vacuous.
- The quantifier "|U| ≤ 15, all U ⊆ [p]" is deliberately stronger than "U ⊆ C_b" (a partition-free form). Keep it,
  but say so.

**R6. State the key lemma's required output, including the cap budget.** "Moves may reorder while remaining safe
deletions" uses an undefined term. Define a **safe move** as the deletion of a null, i ∉ S₀, from a T ⊇ S₀. State the
(X2) requirement as one of these:
- (a) Every move of the uncapped §6.10 search from S̃₀ is a safe move until S₀, and S₀ has no strictly improving
  neighbour; or
- (b) a weaker version that lets non-deletion moves through, with an explicit bound: the number of non-deletion moves
  must fit the slack. On the full-start event S̃₀ = S*, a_n − m₀ = ℓ_n + s₀. A swap uses one move without shrinking.
  An addition costs two.

Also state:
- The conclusion "LS0 scores S₀" needs path length ≤ a_n + 1 (FAC-B's single-search prefix property,
  `W2-FAC-B/STATEMENT.md` §1). Any route that tolerates swaps must **count** them.
- Truth deletions and truth-out swaps must be excluded on the whole path.
- Whether the "certified search endpoint" conclusion of FAC-B (C2) is also sought.

Heuristic only, not proof work, to explain why exact ordering is rightly not required: FAC-B's deletion choice is the
argmin of |ξ_j − x_T|. The minimum spacing of p Gaussian order statistics is ≍ p⁻², while the per-coordinate coupling
error is ≍ √(p log p/n) (max-row norm above). Literal order agreement is therefore plausible only for a below about
1/5. The 1/4 target must not depend on it.

**R7. Quantify FAC-A's baseline and the new range.** State verbatim what FAC-A covers, with status and file:
- `W2-FAC-A/STATEMENT.md:123-127, 143-144`: iid-row compound symmetry under (GC-CS), limsup log p/log n < 1/6.
- `W2-FAC-A/STATEMENT.md:71`: the one-factor class needs κ̄-dependent α₀(κ̄) = 1/(2κ̄(κ̄+2)). For singleton groups,
  κ̄ = max_l(λ_l/√(1−λ_l²)) / min_l(λ_l/√(1−λ_l²)) ≥ 1, so the baseline for C2 is **below** 1/6 whenever the
  loadings differ.
- FAC-A REPORT status line: "PROVED-CHECKED (for the narrowed, flagged target STATEMENT.md v1.2)".

The new content of C1 is then 1/6 ≤ a < 1/4 (and beyond, if achieved). For C2 it is α₀(κ̄) ≤ a < 1/4. Note the
hypothesis difference: FAC-A uses (GC-CS) and (TV-pop) with no full start, while XA uses (FS) or visibility with a full
start. The overlap regime therefore has different hypotheses, and neither result implies the other there.

**R8. Make the rate quantifier explicit.** "Initially seek every p ≤ n^a with fixed a < 1/4" should read: "for every
fixed a < 1/4 and every sequence p_n with p_n ≤ n^a for all large n (bounded, growing or oscillating), …". Say how
bounded and small p are covered (FAC-B's crude regime, or citing FAC-B/T03♯ for p ≲ log n). Mirror FAC-B's "Uniformity
in p_n" paragraph. The research stretch to p = o(n) or p ≤ n/2 must stay outside the locked claims; reaching it needs a
logged revision and a fresh lock, as the statement already says.

**R9. Random-design transfer mechanism (hidden assumption).** T03♯, [OP] and M5(0) are fixed-design results.
Under the joint law the statement must commit to the transfer argument and name its source: FINAL s3 "Random designs" /
GEN (C4) / GROW L6 / C-MIS Lemma DR, as FAC-A L5 does (`W2-FAC-A/lemmas/L5_random_instances.md:13, 58`). The
argument has three parts:
- (H0) and the needed deterministic envelopes hold on design events 𝒜_n with P(𝒜_n) → 1 and constants common over
  𝒜_n;
- convergence is uniform over 𝒜_n, or follows by the every-deterministic-sequence/diagonal argument;
- conditional convergence alone is not used.

Without this, "D_n → 0 under the joint law" contains an unstated uniformity assumption.

**R10. Partition and delivery under random design.**
- The method's partition is computed from X only (complete linkage on 1 − |r_jl|, cut by size B = min(⌊√n⌋, ⌊√p⌋, B*),
  next-fit packing; `State_of_Project/sections/02_method.tex:187-211`), so it is ε-independent.
- State that (X1)–(X3) are proved for every partition into blocks of size ≤ 16, applied conditionally on X. This is
  FAC-B's "every deterministic partition" clause, `W2-FAC-B/STATEMENT.md` §1 "Blocks".
- (X4) uses the method's own partition invariants (B ≤ K).
- For delivery, state (as FAC-A (D) does, `W2-FAC-A/STATEMENT.md:133`) that the retained p equals p_raw almost surely
  for continuous iid rows, so Proposition F's raw-dimension allocation applies unchanged.
- State that the implementation premises are assumed for every design realisation.

**R11. Numerics must be able to reach asymptotic sizes for C1/C2-R.** "At most 20 seeds, local only" with n × p
matrices cannot test a ∈ [1/6, 1/4) meaningfully: n = 10⁶ gives p ≈ 16–32. Add exact sufficient-statistic simulation:
- With centred rows, (n−1)Σ̂ ~ Wishart_p(n−1, Σ). Standardise from its diagonal to get R̂.
- Draw XᵀY = (n−1)R̂θ + XᵀCε, where XᵀCε | X ~ N(0, σ²(n−1)R̂).
- Feed (R̂, XᵀY, n) to FAC-B's general exact-Gram scorer (`W2-FAC-B/numerics/fac_core.py`, read-only reuse).

This reaches n = 10⁸, p = 100–400 locally.

Also:
- FAC-B's cs_gain/cs_core tie handling was flagged in `W2-FAC-B/reviews/R01_statement_lock_sol.md:61`. Use the fixed
  versions or restrict to tie-free runs.
- Record path length against a_n and the count of non-deletion moves (R6).
- State the planned (n, p, ρ, λ, s₀, θ) grid in PLAN.md before running.

**R12. Protocol completeness in PLAN/STATEMENT.**
- CHECKPOINT.md is due when the key lemma is proved **or after ~3 hours**, whichever comes first (Wave2 PROTOCOL
  "Timeline").
- Inherit the Wave1 stop rules: a lemma that fails 3 attempts → STUCK and report; a counterexample to the target →
  stop and report immediately.
- The mid-point reviewer must be cross-family to the lead, i.e. Claude.
- A citation check script runs before the council (reviews/CITECHECK.txt).
- Dependency statuses are transcribed verbatim **at lock**, not only "when actually used": at least FAC-B
  "PROVED-CHECKED" (REPORT §1), FAC-A as in R7, T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)", and
  Proposition F as listed in `W2-FAC-B/STATEMENT.md` §6.
- The council composition is as the protocol requires (Codex gpt-6.1-sol + Claude Opus 5.5). The Codex seat being
  same-family as the lead is protocol-mandated, and that is acceptable.

---

## C. Checked and found acceptable (no change needed)

- **Target correctness and meaning.** C1 (iid compound symmetry beyond FAC-A's 1/6) is exactly FAC-B's open item 4
  (`W2-FAC-B/REPORT.md:138`) and a natural next step. Every conclusion is under the joint law. Nothing is asserted as
  proved, and the rate is a target, not a claim.
- **Response convention.** Y = Xθ + Cε with θ fixed on the standardised scale. This gives μ ∈ col(X_{S₀}) exactly for
  every design draw, so FAC-B's "null increments vanish for U ⊇ S₀" holds exactly, and the N₀ nulls carry pure noise
  increments in random design too. The convention matches FAC-A (`W2-FAC-A/STATEMENT.md:49-51`).
- **Method.** No method change is proposed, and the cap a_n = ℓ_n + |S̃₀| is used as merged.
- **The delivery clause** correctly forbids inferring discovery from D_n and requires Lemma S inputs plus the pathwise
  inclusion, as in FAC-B (C4) and A2 step 3.
- **The statement does not import FAC-B's swap margin.** This is correct: FAC-B R01 proved that a log-n swap margin
  is false.
- **(FS) for C1** is FAC-B's (FS) with Υ_n = I. It is sufficient for null visibility. Sample partial covariances match
  their population values to O_P(√(log p/n)) entrywise (numerics above). The start-mode margins are of order n, so
  transferring them is plausible. That transfer is proof work, not a statement defect.
- **No contact with W2-FAC-X.** The plan says so, and I did not open it.

## D. Lock conditions

LOCK once R1–R12 are applied to STATEMENT.md/PLAN.md (versioned, e.g. v1) and logged with a disposition file. A fresh
lock review is not required unless:
- C2 is re-scoped beyond R3/R4;
- the target exponent changes; or
- a claim is strengthened beyond the numbered list in R2.
