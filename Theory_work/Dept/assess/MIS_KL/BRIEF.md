# Assessment brief: Song–Liang-type misspecification (KL projection) — should we pursue it, and is it feasible? (HQ, 2026-11-24; owner's order)

**Type:** assessment only. No proofs, no new claims, no registry changes. The break stays in force for everything else.

## The question
Our misspecification line is W3-MISR and the rider W3-MISR-R:
- MIS-R (i), (i′), (ii): exact recovery of the projected support S₀ at rate √(log n/n), for p ≤ n^A;
- Cor-G, CorG-min: the Gaussian-design instances;
- Cor-H, CorH-plus, CorH-U: Hellinger contraction around the projected law.

It covers only **omitted-variable** misspecification. Given the candidates, the omitted part must be linear in the
candidates plus Gaussian noise: hypothesis (OV^c) of `W3-MISR-R/STATEMENT.md` §2. CorG-min (c) shows this is
necessary under Gaussian noise. Non-Gaussian residuals enter only through the total-variation term of R′(c). The
non-claims are in `W3-MISR/STATEMENT.md` §9 and `W3-MISR-R/STATEMENT.md` §6.

Song & Liang (2015, JRSS-B 77(5)), §2.3, p. 957, are broader on this point:
- **Theorem 4:** for an arbitrary true joint law f*, the posterior concentrates in Hellinger distance around the
  Kullback–Leibler projection f₀ of f* onto the Gaussian linear family on the subset. This holds even when
  E[y | x_s] is non-linear or the residual is non-Gaussian.
- **Corollary 2** (screening, s̃ ⊂ ξ) then follows. Song–Liang have no rate, keep the subset size s fixed, and need
  iid random rows.
- The paper is `Papers/Core_bibliography/32_2015_Song_Liang_*.pdf`, with the supplement in 32b (§1.3, the proof of
  their Theorem 2.4, via De Blasi–Walker 2013).

**The owner asks:** should we pursue a version of our results that covers this broader misspecification, and how
feasible is it given all the theory we already have?

## What each assessor delivers (≤ 2 pages, plain words; statements in LaTeX)
1. **Value.** What would such a result add to the paper and thesis? Is it a headline, a supplement, or not worth it?
   Who would ask for it (referees, competitors)? Does Song–Liang's Theorem 4 actually say more than ours in a way a
   reader cares about?
2. **Target statement.** Give the most natural candidate theorem or theorems. Possible targets:
   - selection consistency to the support of the KL / population-projection coefficient;
   - Hellinger or KL contraction to f₀;
   - both.

   State the hypotheses at the level of our design-agnostic assumptions, and say what we would have to give up:
   rate, exactness, p ≤ n^A, the coded prior.
3. **Feasibility, given the theory we have.**
   - Which of our lemmas carry over: the R′ reduction, the [POST2] Claim C machinery, (OS)/(ID) and the W3-DIST
     contraction tools.
   - What breaks: the exact Gaussian marginal likelihood under non-Gaussian residuals; heteroscedastic and non-linear
     residuals; the random intercept.
   - The main obstacle, and whether there is a known route (De Blasi–Walker, Kleijn–van der Vaart, sub-Gaussian
     quadratic-form concentration).
4. **Cost and risk.** Give the size in ticket terms (tier, number of key lemmas, rough lead-weeks), the risk of
   failure or of a weak result, and the cheapest version worth doing.
5. **Recommendation.** One of: pursue (with scope), pursue a narrow version, or do not pursue. Give the reasons.

## Staffing (owner's order, binding)
- **One Fable 5.2 agent:** Claude Personal, effort **high**, inside the Theory Department.
- **One Astra agent** (`gpt-6-astra`, codex, effort high), inside the Theory Department.
- The two work **independently**. Neither sees the other's output before both are done. Give each the same brief: this
  file plus the paths above.
- Each agent runs once, with a kill budget: one round, no re-spawn.
- Codex rules (POLICIES §14): Astra writes only to `<worktree>/.rc_tmp/`, never deletes anything, and never redirects
  output outside its worktree. The manager copies its output.
- No Sol, no council, no other agents.

## Output
- `Theory_work/Dept/assess/MIS_KL/ASSESS_fable.md` and `ASSESS_astra.md`, verbatim.
- A synthesis of at most 10 lines in `SYNTHESIS.md`: where the two agree, where they differ, and the manager's own
  recommendation.
- Push to main, then send HQ (thread mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e, environment 1fde6176) one line with
  the commit and the two verdicts.
