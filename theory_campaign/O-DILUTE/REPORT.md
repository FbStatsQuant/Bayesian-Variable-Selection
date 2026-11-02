# O-DILUTE — why π₀(S₀) is tiny but π₀(R_d) is large at n = 200

Run of 2026-11-02, branch `theory/O-DILUTE` (from `theory/campaign`), Opus 5.5, Felipe's laptop (Python 3.12; R not
available). Statements and proofs: `THEORY.md`. Scripts: `scripts/` (fixed seeds). Raw output: `results/study_*.jsonl`;
tables: `results/summary.txt`, `results/predict.txt`, `results/propS.txt`. Every proof here is a **candidate**: it has not
been reviewed or adopted. Status words follow the campaign PROTOCOL.

## 1. Headline

@@HEADLINE@@

## 2. Statements (full text and proofs in `THEORY.md`)

| Label | Statement (short) | Hypotheses | Status |
|---|---|---|---|
| Thm E | π₀(S) = ∏_b π_b^t(S_b)·A_t(\|S\|) for every t > 0; at S₀, A_t(s₀) = 1/E_t[e^{g_t(N)}1{N≤K}] | any data, any partition, positive tables | PROVED |
| Cor E1 | −log π₀(S₀) = V_t (visibility, Σ softplus(−λ_b)) + C_t (competition) − log A_t (size) | as Thm E | PROVED |
| Cor E2 | t ∈ I₀ ⇒ log π₀(S₀) ≤ −V_t − C_t − log P_t(N ≤ K) ≤ −Σ_b softplus(−λ_b) + o(1) (sharpens W3-VEXP Prop D) | as Thm E | PROVED |
| Thm R | exact joint law of (#truths, #non-truths) under π₀; π₀(R_d), π₀(B_d), Markov bound π₀(R_d) ≥ 1 − E M/(d+1) | as Thm E | PROVED |
| Lemma N | in Gaussian designs a null independent of y has r_ly² ~ Beta(½, (n−2)/2) exactly: the v3 table scores it as in pure noise, at every signal scale | x_l^r Gaussian, independent of (y, X_{−l}) | PROVED |
| Cor N1 | expected null inclusions under P_t = Θ(s₀√(log p)/√n) ≈ 1 at the study size | Lemma N | PROVED (expectation); PROOF SKETCH (constant) |
| Lemma L | a common plug-in σ² multiplies every null's exponent by v/σ̂²; with the oracle σ² the start fills to the cap K; F-DRAFT Lemma W1 needs **in-sample** BO, the study has only **population** BO | Lemma N | PROVED (identity) / PROOF SKETCH (extreme value) |
| Prop S | π₀(S₀) ≤ 1/∏_i(1 + [M_(i) − i + 1]₊) for v3 tables **and every common σ²** | any data and partition | PROVED |
| Prop D′ | λ_j ≈ ½χ²₁(nρ_j²) − ½log n − log((2p−s₀−1)/(s₀+1)), ρ_j² = (1 − κ_j)x_j ≤ ω_j (saturating in c); assembled formula for log π₀(S₀) | population BO, Gaussian design | PROOF SKETCH; numerically checked |
| Prop DM | paper proposition (wording in THEORY §7) | (i)–(iii) any data; dilution clause population BO | (i)–(iii) PROVED; dilution clause PROOF SKETCH |
| Conj DM-asy | with s₀ = s_n → ∞ truths of comparable share and n/(s_n log(pn)) → κ ∈ (0, ∞), the start-visible fraction converges to a deterministic limit in (0, 1), π₀(S₀) → 0 while π₀(R_d) stays bounded below | population BO | CONJECTURE |

## 3. The mechanism, quantified (items 1–2 of the task)

@@MECH@@

## 4. Verification on regenerated study datasets (item 3)

@@VERIF@@

## 5. The common-plug-in-σ² variant (item 4; pilot evidence only, no method change decided)

@@VARIANT@@

## 6. Paper proposition and connections (item 5)

@@PAPER@@

## 7. What fails and why

@@FAILS@@

## 8. Needs escalation

@@ESC@@

## 9. Outside scope

@@OUT@@

## 10. Confidence card

@@CARD@@
