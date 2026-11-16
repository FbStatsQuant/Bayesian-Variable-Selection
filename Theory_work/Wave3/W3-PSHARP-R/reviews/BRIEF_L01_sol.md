# BRIEF L01 — statement-lock review (blind first read) — W3-PSHARP-R

You are an independent reviewer (gpt-6.1-sol, reasoning effort high). Your job is to **break the statement and the
plan** before any proof is written. Find what is wrong, ill-posed, false, unfaithful, or weaker/stronger than it says.
Work in the checkout `/home/fb31/BVS-wt/W3-PSHARP-R` (paths below are relative to it).

## What to read (and nothing else in `Theory_work/Wave3/W3-PSHARP-R/`)
- `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md` (v1.0) — the object under review: a **delta** statement over the parent
  ticket W3-PSHARP. It adds claims `W3-PSHARP-R:AE` (Proposition A-E with Corollaries A1-E, A2-E) and
  `W3-PSHARP-R:A2C`, and corrects two readings of the parent.
- `Theory_work/Wave3/W3-PSHARP-R/PLAN.md` (v1.0) — proof routes; check that they are viable.
- Parent (read-only, already council-checked): `Theory_work/Wave3/W3-PSHARP/STATEMENT.md`,
  `Theory_work/Wave3/W3-PSHARP/lemmas/A_log_factor.md`, `Theory_work/Wave3/W3-PSHARP/lemmas/S_one_step.md`,
  `Theory_work/Wave3/W3-PSHARP/ASSUMPTION_MAP.md` (line 15 is cited).
- Definitions of the coded target π: `Theory_work/Wave3/W3-POST/STATEMENT.md` lines 16-39.
- What motivated the change: `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md` lines 21-22, 43, 80, 111, 121, and the
  audit text `Theory_work/Wave3/API_AUDIT/sharp2/results/f02.md` lines 5-44.
- The cited numerics file `Theory_work/Wave3/W3-PSHARP-R/numerics/ae_fixed_p.py` and its output `ae_fixed_p_out.txt`
  (only if you want to test the statement's §5 remark).
Do not read any other file of this ticket (no LOG, no other reviews). You may run your own small computations (python3,
numpy available; numpy is in the user site, so do not use `-I`) to test claims; keep any script under
`Theory_work/Wave3/W3-PSHARP-R/reviews/L01_scratch/`.

## What to check
1. **Well-posedness.** Every new object (c_n, ℓ_n, Λ^E_n, Setting-E, (W-orth-E), (W-sph-E)) defined; domains (n, p,
   s₀, K, N_n) consistent; each hypothesis satisfiable; quantifiers, uniformity and modes of convergence unambiguous
   (expectation vs in probability). Is "n₀ depends only on …" in Proposition A-E right?
2. **Truth.** For Proposition A-E, Corollaries A1-E (a), (b), A2-E (i), (ii) and Proposition A2C: try to derive or
   refute. In particular: the truncation at T = ϵ/c_n and the second-moment bound E Y² ≤ c²(N T E U + N²(E U)²) in the
   (W-orth) case, where the null scores g_j also enter V (PLAN §2.2 proposes a decoupling E = g_j² + R_j — is the
   independence claim right, and is the resulting bound valid?); the (W-sph) case (independence of the scores from the
   ε-event; the sphere-law bounds at τ = 2 log T); the passage from log T to ℓ_n; the claim "fixed p included"; the
   constants √((a+½)/π) and 1/√(2π) in A1-E; the sub-block argument for A2-E; the multi-step identities and the
   elementary-symmetric bound for A2C, and whether K − s₀ → ∞ holds there. Look for counterexamples, especially with
   N_n bounded, p fixed, p huge relative to n under (W-orth), and s₀ growing.
3. **Faithfulness.** Is each "implies" row of §6 right (does A1-E really imply the parent's Cor A1 second display under
   the parent's hypotheses; does A2C imply what it says)? Do §1's "taken unchanged" line references point at the right
   parent text? Are the corrected readings §4.1, §4.2 correct and are they the right correction of parent
   STATEMENT.md:84-88 and :109? Does the delta claim anything the parent's checked steps, as cited, cannot carry?
4. **Overclaiming / underclaiming.** Anything stated more strongly than can be true; anything obviously true in a
   stronger form at no cost (e.g. are the added hypotheses (log p)² = o(n), (r₀ + 1) log(pn) = o(n) needed?).

## Output
Write your full review to `Theory_work/Wave3/W3-PSHARP-R/reviews/L01_statement_lock_sol.md`:
- a verdict line: `LOCK`, `LOCK-WITH-AMENDMENTS`, or `DO-NOT-LOCK`;
- findings, each labelled FATAL / MAJOR / MINOR / NIT, with the exact place (file:line) and the exact correction you
  propose; say for each claim item whether you derived it, tested it numerically, or could not check it;
- do not change any file other than your review file and your scratch directory. Do not commit.
Reply with the verdict line and the counts of findings by severity.
