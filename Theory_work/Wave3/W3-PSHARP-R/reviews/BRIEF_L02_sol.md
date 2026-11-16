# BRIEF L02 — line check (blind) — W3-PSHARP-R, lemmas AE_expectation and A2C_critical

You are an independent reviewer (gpt-6.1-sol, reasoning effort high). Your job is to **check two proofs line by line and
break them**. Work in the checkout `/home/fb31/BVS-wt/W3-PSHARP-R` (paths relative to it).

## What to read (and nothing else in `Theory_work/Wave3/W3-PSHARP-R/`)
- Under check: `Theory_work/Wave3/W3-PSHARP-R/lemmas/AE_expectation.md` and
  `Theory_work/Wave3/W3-PSHARP-R/lemmas/A2C_critical.md`.
- What they must prove: `Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md` (v1.1, locked), §2 and §3 (claims
  `W3-PSHARP-R:AE` = Proposition A-E with Corollaries A1-E, A2-E; `W3-PSHARP-R:A2C`).
- What they consume (parent ticket, already council-checked; read the cited lines and enough context to judge them):
  `Theory_work/Wave3/W3-PSHARP/STATEMENT.md`, `Theory_work/Wave3/W3-PSHARP/lemmas/A_log_factor.md`,
  `Theory_work/Wave3/W3-PSHARP/lemmas/S_one_step.md`, and line 15 of `Theory_work/Wave3/W3-PSHARP/ASSUMPTION_MAP.md`.
- Definition of the coded target π: `Theory_work/Wave3/W3-POST/STATEMENT.md` lines 16-39.
Do not read LOG.md, PLAN.md, CHECKPOINT files or anything under `reviews/` other than this brief. You may run small
computations (python3 with numpy; numpy is in the user site, so do not use `-I`); keep scripts under
`Theory_work/Wave3/W3-PSHARP-R/reviews/L02_scratch/`. If you write temporary files, use
`export TMPDIR=/home/fb31/SMC_Theory_Department/tmp/20261115-W3-PSHARP-R-L02; mkdir -p "$TMPDIR"` and delete it at the end.

## What to check
1. Every line: each inequality, identity, independence claim and limit. In AE: Lemma T (incl. its use of
   independence), the truncated means §2 (and that the cited parent lines really give them for τ = 2 log T), the
   truncation level and (3.1)-(3.2), Lemma F, the (W-orth) decoupling and the bound e_n, the (W-sph) independence of the
   score vector from ε and the event G, the rates and the choice of x_n, the uniformity claim (what n₀ depends on), the
   random-(X_{S₀}, θ*) step, Cor A1-E (a), (b), and Cor A2-E (Step 0 via the parent's (B1), the sub-block step, (i), (ii)).
   In A2C: the multi-step identities from Lemma S, the prior ratio, (2.1), the truncation from the parent, the collision
   bound, the limit argument (order of choosing J₀, ϵ, ϵ′), the equivalence and the expectation consequence.
2. **Citations**: each cited parent line says what the lemma uses it for, and the parent step is used within its own
   hypotheses (in particular: no use of N_n → ∞ where the new claim drops it).
3. **Statement match**: each lemma proves exactly the STATEMENT clause it claims (hypotheses, quantifiers, uniformity,
   mode of convergence), no more and no less.

## Output
Write the full review to `Theory_work/Wave3/W3-PSHARP-R/reviews/L02_line_check_sol.md`:
- per lemma, a verdict line `LEMMA <name>: CORRECT | CORRECT-WITH-FIXES | GAP | WRONG`;
- findings, each labelled C (correctness: a step wrong or unproved), S (strength: claims more than proved, or uses an
  unstated hypothesis), F (faithfulness to STATEMENT or a citation) or E (editorial), with file:line and the exact fix;
- say which steps you re-derived and which you tested numerically.
Change no other file; no git operations. Reply with the two verdict lines and the counts of findings by tag.
