# W3-DIST — cross-family line check L5 — Lemma S (size tail) and Lemma V (superset moment bound) — gpt-6-astra, codex, reasoningEffort high

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one
output file `Theory_work/Wave3/W3-DIST/reviews/L5_astra_SV.md`.** Run no git command that changes state; start no agents.
Proof files: `Theory_work/Wave3/W3-DIST/work/C_size/S.md` (including its final "Amendments" section) and `V.md`.
Statements: "Lemma S" and "Lemma V" in `Theory_work/Wave3/W3-DIST/STATEMENT.md` §3 (with §0 for the interfaces, the cutoff
m_n(t) and the conventions on s₀ and p; note for Lemma V that Q means the contrast-scale Q^c and
ρ′ := θ*ᵀ(G_{S₀} + I)θ*/n = (‖μ‖² + ‖θ*‖²)/n). Common definitions: `Theory_work/Wave3/W3-DIST/API_CARDS.md` ("Common
definitions"). Inherited, locked source that may be cited: [P1] =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`.
Also readable: `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md`, `Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md`, and the
check script and output in `work/C_size/`. Read nothing else in the ticket folder (no `reviews/`, `LOG.md`,
`CHECKPOINT_*.md`, `DEPS.*`, `lemmas/`, other `work/` folders, `work/C_size/X12.md`).
Check every line and try to break each lemma:
1. Lemma S: the reduction through [P1] `thm:Ta` on the response-scale bracket event 𝓑_n (its definition and endpoints
   b₋, b₊ in [P1]); the exponential bound P(𝓑_nᶜ) ≤ 4e^{−c_Bn} and the constant c_B; the numerator expectation with a
   data-free rate ([P1] `lem:num`) — in particular with a **design-measurable** reference (T, ϑ) and for models of size
   up to K = min(p, ⌊n/2⌋), singular Gram matrices included; the denominator bound (re-derivation of the proof of
   [P1] `lem:den` with the reference cost B_T(ϑ)); the tails of Λ″; the Markov step; the final inequality and the
   hypothesis on m; the corollary for T = S₀, ϑ = θ* (m = m_n(t), s₀ = 0 included, the cap m = K) in both forms (the
   original and amendment A-1); Corollary S.2. Does the file prove Lemma S as stated in STATEMENT §3 (the file claims
   a stronger form: every n ≥ 3, every t > 0, constants free of κ₀)?
2. Lemma V: (a) the variational split and the constant (1 + 2/η); (b) the moment bound
   E[(D_{S₀}/D_S)^{1/2} exp(eᵀD′e/(2σ*²))] ≤ (1 + η)^{s₀+|J|/2} — definition of D′, eigenvalues strictly below 1, the
   determinant identity, the eigenvalue-wise comparisons; (c) D′ ⪯ (P_S − P_{S₀}) + R₀; singular Gram matrices, duplicated
   columns, s₀ = 0, J = ∅, |S| up to K.
3. Look for a counterexample to either statement (a fixed design, truth and reference satisfying the hypotheses).
Output: first line `L5 line check — sha256 S.md <16 hex> V.md <16 hex>`. Findings with id, severity (CRITICAL / MAJOR /
MINOR / NIT), file and section, the error or gap in full, minimal repair. Verdict per item (Lemma S; Corollary S.1;
Corollary S.2; Lemma V (a), (b), (c)): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line: overall verdict.
Do not soften findings; say exactly what you could not check.
