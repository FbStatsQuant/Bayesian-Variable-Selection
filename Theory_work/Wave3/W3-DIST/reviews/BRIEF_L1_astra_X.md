# W3-DIST — cross-family line check L1 of Lemma X and Lemma X′ — gpt-6-astra, codex, reasoningEffort high

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one
output file `Theory_work/Wave3/W3-DIST/reviews/L1_astra_X.md`.** Run no git command that changes state; start no agents.

Object: `Theory_work/Wave3/W3-DIST/lemmas/X.md` (v0.3): the proof of Lemma X (§0–§7) and of Lemma X′ (§9). §8 is
commentary and §10 is the author's own notes: neither is part of the proof. The statements to be proved are
"Lemma X" and "Lemma X′" in `Theory_work/Wave3/W3-DIST/STATEMENT.md` §3 (with §0 of that file for the interfaces (E), (C),
(ND), the cutoff m_n(t), and the conventions on s₀ and p); common definitions in `Theory_work/Wave3/W3-DIST/API_CARDS.md`
("Common definitions"). Inherited, locked source that may be cited: [P1] =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`.
Also readable: `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md`. You may read nothing else in the ticket folder
(no `reviews/`, `LOG.md`, `CHECKPOINT_*.md`, `DEPS.*`, `work/`, other files of `lemmas/`).

Check every line and try to break the proof:
1. Each inequality, with its constants: recompute. In particular §3 (the pointwise bound on the Bayes factor on the
   noise event; the moment E exp(λ₁zᵀD′z/2) = det(I − λ₁D′)^{−1/2} and its bound, using the rank and eigenvalue range of
   D′_J; λ₁ ≤ 1 − 1/(8A + 4); Jensen with (ND); the exponent A(1 − λ) − λ/2 = −¼; the geometric sum; the union device
   through S ∪ S₀ and sets outside Ω; Markov at power λ with the indicator of the event), §4 (the size tail above
   m_n(t): numerator expectation with a data-free rate b₋, denominator bound from the proof of [P1] `lem:den` with R_n
   replaced by ρ′, `thm:Ta` on the event 𝓑_n, the cutoff arithmetic), §5, §6, §7.
2. Every citation of [P1]: existence, exact content, hypotheses met.
3. Uniformity: one n₀ for all t in [M₀ log n, n^{1−κ₀}] and all n ≥ n₀; constants depending only on
   (s₀^r, A, σ², M, M′, c_D, κ₀) for Lemma X and on (s₀^r, A, σ², M, M′, κ₀) for Lemma X′; the case s₀ = 0; p = 2; S₀ ∈ Ω.
4. Does §7 prove exactly Lemma X as stated, and §9 exactly Lemma X′ as stated (note: X′'s statement uses
   ℓ_n = log(p_raw ∨ n) in the mean threshold)?
5. Look for a counterexample to Lemma X itself: a fixed design and truth satisfying (E; M), (C; M′), (ND; c_D, m_n(t)) for
   which the conclusion fails.

Output: first line `L1 line check — lemmas/X.md sha256 <first 16 hex of the file's sha256>`. Findings with id, severity
(CRITICAL / MAJOR / MINOR / NIT), section and line, the error or gap in full, minimal repair. A verdict per section
(§1, §2, §3, §4, §5, §6, §7, §9): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line: overall verdict for
Lemma X and for Lemma X′. Do not soften findings; say exactly what you could not check.
