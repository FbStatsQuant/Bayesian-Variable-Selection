# BRIEF — parallel prover PV1: the examples lemma L6 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are a research prover for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable selection; this ticket
proves when the coded method reports the true model S₀ when the set Q of columns that may "leak" signal has
polynomial size n^b). This file is your whole brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2`
(paths below are relative to it). **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md`. Do not edit any other file (scratch work goes outside the
worktree). Do not start subagents. Use no effort setting above high. All results are asymptotic (n → ∞).

## What exists
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` — the statement. Read §1 (objects), §3.1 (Form F assumptions), §3.2
  (Form R assumptions — **(L-R^b) is in its new v1.4 form**: leak bound ℓ_n = o(√(log n/n)) at every conditioning
  set of size ≤ 15, localisation with any r_n → 0, |H_l| ≤ n^ρ, 15ρ + b < ½), §4 claims (C1)–(C5).
* `Theory_work/Wave3/W3-RM2/lemmas/L2_width.md` §3 (the sufficient forms of the width condition (W): (W-δ), (W-unif),
  (W-χ), (W-ref), (W-loc), each proved to imply (W)), §4 (Lemma d, (BM-Q) ⇒ (BM-W)); `lemmas/L3_assemblyF.md`
  (Theorem RM2-F and "RM-F is a special case of RM2-F").
* The Form R theorem (C2) and "RM-R is a special case of RM2-R" are being written by the lead in parallel
  (`lemmas/L4_sandR_b.md`, `lemmas/L5_formR.md`); treat their statements in STATEMENT §4 as given. In particular
  (W-R) is implied by (D-R^b), and (D-R^b) by (D-loc^b) (STATEMENT §3.2, last bullet).
* Sources you may read and cite by path:line (statuses must be copied verbatim, never upgraded):
  `Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md` (Lemma BC — bounded conditioning preserves the decay exponent;
  Lemma IR — inverse decay; its sections 3–7 verify the polynomial-decay class for the older theorem with cutoff
  α > 17/2), `Theory_work/Wave2/W2-LOC2/STATEMENT.md`, `Theory_work/Wave3/W3-RM/lemmas/L7_examples.md` (the parent
  theorem's examples and their format), `Theory_work/Wave3/W3-RM/STATEMENT.md`, `Theory_work/Wave2/W2-UNI/STATEMENT.md`,
  `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`, `Theory_work/Wave2/W2-APP/lemmas/L3_LOC.md`,
  `Theory_work/Wave1C/C-GROW/STATEMENT.md` and its `lemmas/`. Do not read any `reviews/` folder, `LOG.md` or
  `CHECKPOINT*.md`.

## Your task: write `lemmas/L6_examples.md` — claim (C5), verified examples
For each example: state the design class precisely (as an example — no design family enters any theorem), list
every hypothesis of the theorem it instantiates, and verify each one with a proof or an exact citation (path:line)
whose hypotheses you check. Say plainly when something cannot be verified. Constants must be tracked.

**E1. Inherited examples (no new mathematics).** Every example of RM-F is an example of RM2-F, and UNI-0's class and
LOC-BF's class are examples of RM2-R, by the containment (C4). List them with their sources.

**E2. Form R, polynomial covariance decay — the main new example.** Class: Gaussian rows, Σ with unit diagonal,
|Σ_jk| ≤ K(1 + |π(j) − π(k)|)^{−α} on a line (π injective into ℤ or as in the source), spectrum in [c, C], PTV(a₀),
fixed signals, s₀ fixed, p ≤ n^A. The older theorem (W2-LOC2:Thm-Poly) needed α > 17/2 because its leak set had
to be localised at the rate n^{−ρ}-type radius. Under the **new** (L-R^b): take
Q := {k : d(k, S₀) ≤ R_Q}, with R_Q chosen so that the leak bound ℓ_n = sup over l ∉ Q, |U| ≤ 15, j ∈ S₀ ∖ U of
|Cov(W_l, W_j | W_U)| is o(√(log n/n)) (use Lemma BC with M = 15: the conditional covariance decays with the same
exponent α, uniformly over conditioning sets of size ≤ 15), and H_l := {k : d(k, {l} ∪ S₀) ≤ r₀} with any r₀ → ∞
slowly (e.g. r₀ = log n), so |H_l| ≤ n^ρ for every ρ > 0 and r_n ≤ C r₀^{−α} → 0. Determine:
 (i) the exact size of Q and hence which b are admissible — the claim to test is "any b > 1/(2α), so b < ½ needs
     only α > 1 from this hypothesis";
 (ii) what the other hypotheses need: (T1-R), (FL-R), (V-R), (L-feas), and **(W-R) through (D-loc^b)** (local
     regressions with L_n → 0: STATEMENT §3.2 and RM `STATEMENT.md:154-156`) — use Lemma IR; this is where a larger
     α may be needed (the ℓ¹ tail of regression coefficients). State the resulting cutoff on α honestly: the
     smallest α for which **every** hypothesis of RM2-R is verified with the available lemmas. The target is
     **α > 2** in place of 17/2; if a step needs more (or the lemmas available do not give it), say exactly which
     step and what it needs.
 (iii) a short ledger: which step of the old verification forced 17/2 and why it is no longer needed.

**E3. Form F, exact-Gram polynomial decay on a line** (STATEMENT (C5)): fixed design with X^TX/(n − 1) = G exactly,
G with unit diagonal, spectrum in [c, C], |G_jk| ≤ K(1 + |j − k|)^{−α}, p < n. Verify (T1-F) [the hypotheses of
Theorem 1 as stated in `Theory_work/Wave1C/C-GROW/STATEMENT.md`; cite], (FL), (V), (L^b) (Q a neighbourhood of S₀;
compute the leak level η and the admissible b), (BM-W), and (W) through (W-loc) (Lemma IR applied to G). Specify
the truth-separation and coefficient conditions needed. State the cutoff on α that the verification needs.

**E4. Form F, one truth with n^b weak proxies (a witness that (W) is not vacuous at polynomial |Q|).**
p = ⌊n/3⌋, s₀ = 1, q = ⌊n^b⌋, 0 < b < ½; e₁, …, e_p orthonormal and centred (orthogonal to 1); x₁ = √(n − 1)e₁;
for 2 ≤ j ≤ q, x_j = √(n − 1)(r_n e₁ + √(1 − r_n²)e_j) with r_n² = C₀ log n/n; x_j = √(n − 1)e_j for j > q;
Q = {1, …, q}; θ*₁ a fixed nonzero constant. Verify every hypothesis of (C1): (T1-F) (state which constants are
needed, e.g. on |θ*₁|, and whether a condition on C₀ is needed), (FL-16), (FL-Q), (V), (L-size^b), (L-feas),
(L-gain) with η = 0, (BM-W), and (W) through (W-loc) with N_l = {1} for proxies. Be careful with (W-loc)'s exact
definition (STATEMENT §3.1) and with the Gram matrix of the proxies (they are mutually correlated at level r_n²).

**E5. Candidate: one equicorrelated leak group of size ≍ n^b around one truth** (STATEMENT (C5), "candidate, not
verified"). Either verify (W) by a direct width computation (and all other hypotheses of (C1)) for an explicit
range of parameters, or state precisely why it cannot be verified with the present sufficient forms. A clean
negative answer is acceptable.

End the file with: the examples table (class | theorem | conditions | cutoff | status "PROVED (by this seat,
unchecked)" or "NOT VERIFIED: reason"), a list of every source used with its status copied verbatim, and an
adversarial self-check (what you tried in order to break each verification).

## Output
Header of the file: `Status: PROVED (by this seat, unchecked)` (per example where it applies) and
`Seat: research parallel prover, Codex gpt-6.1-sol, high effort`. End your reply with a five-line summary: the
cutoff obtained for E2 and E3, and the status of E4 and E5.
