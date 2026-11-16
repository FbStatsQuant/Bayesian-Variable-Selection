# W3-DIST — cross-family line check L7 — Proposition NEC (a counterexample: Lemma X's non-degeneracy hypothesis cannot be dropped) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one
output file `Theory_work/Wave3/W3-DIST/reviews/L7_sol_NEC.md`.** Run no git command that changes state; start no agents.
Any temporary file goes under `/home/fb31/SMC_Theory_Department/tmp/20261115-W3-DIST-L7/` (never `/tmp`); remove it when done.
Proof file: `Theory_work/Wave3/W3-DIST/lemmas/NEC.md` (§0 statement; §1–§6 proof of the Proposition; §7 proof of the
Corollary; §8 remarks). Context: `Theory_work/Wave3/W3-DIST/API_CARDS.md` ("Common definitions": the posterior on models, the
conditional posterior, D_S, M_S, Q^c_S, the prior weights, the interfaces); `Theory_work/Wave3/W3-DIST/STATEMENT.md` §3
(Lemma X, Lemma X′, Proposition NEC) and §0 (interfaces (E), (C), (ND)); the locked [P1] =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`
(`lem:spec`, `lem:slab`). Read nothing else in the ticket folder (no `reviews/`, `LOG.md`, `CHECKPOINT_*.md`, `DEPS.*`,
`work/`), and stop reading STATEMENT.md at "## Changelog".
Check every line and try to break the counterexample:
1. §1: the design (centred columns of squared norm N; the choice of τ; existence for large n; K = p).
2. §2: the exact spectra and determinants in cases (a), (b), (c); the bound (2.1); (2.2); the plug-in bound and (2.3)
   (recompute the bracket (1 − h)² + h²(1/n + 1/(nNτ²)) = 1 − h and the term φ₀²/n).
3. §3: every event and its probability; E a_j, E a_j²; the bound on E Ã′; P(𝓔) ≥ 0.6; consequences (i), (ii).
4. §4 (Step A): the upper bound on Σ_{S≠∅}π(S)/π(∅), the prior-ratio identity, the geometric sum.
5. §5 (Step B): the lower bound on the likelihood factor, D_S ≤ (n+1)d^k, the prior ratio, the elementary symmetric
   polynomial bound, (5.1).
6. §6 (Step C): the conditional law of X_{c,S}θ, the symmetric-perturbation argument, the lower bound on ‖M_Se‖².
7. §0 and §7: does §1–§6 prove the Proposition as stated (quantifiers: for every k, n ≥ n₄(k), probability ≥ 0.6)? Does
   the Corollary follow, for constants allowed to depend on (s₀^r, A, σ*², M, M′, κ₀), and with the outer bound replaced by
   any sequence tending to 0? Does the design violate (ND)?
8. §0 "What this does not say" and §8: is each of these four limits and four remarks correct — in particular that
   Lemma X (with (ND)), Lemma X′ and displays (1.1), (1.2) of STATEMENT are **not** contradicted?
A numerical confirmation is welcome but not required (exact posterior over models of size ≤ 3 on this design at one n).
Output: first line `L7 line check — lemmas/NEC.md sha256 <first 16 hex>`. Findings with id, severity (CRITICAL / MAJOR /
MINOR / NIT), section, the error or gap in full, minimal repair. Verdict per section (§1–§8) and for the Proposition and
the Corollary: VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line: overall verdict. Do not soften findings.
