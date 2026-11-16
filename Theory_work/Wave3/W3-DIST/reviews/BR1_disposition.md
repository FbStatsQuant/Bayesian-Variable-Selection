# W3-DIST — disposition of the CP2 break review BR1 (`reviews/BR1_astra_break.md`; gpt-6-astra, codex, high)
Pins: lemmas/X.md 4c3a657742455bef; STATEMENT.md 7c8fcb7754175acd (v1.4.2 at its final reread).
Verdicts: **Lemma X NOT BROKEN; passage Lemma X → (1.1) NOT BROKEN; Lemma X′ NOT BROKEN; passage Lemma X′ → (1.2) NOT BROKEN.**
0 CRITICAL, 0 MAJOR, 3 MINOR (omissions in the written assembly, each with a complete repair). **CP2: CONTINUE.**
| id | sev. | finding | disposition |
|---|---|---|---|
| BR1-01 | MINOR | Lemma T is for a deterministic d; the sketch chose d through s₀(X), p_ret(X) | ADOPT: deterministic levels d₁ = min{p_raw, 2s + ⌈32t/log n⌉}, d₂ = min{p_raw, s + ⌈C_m t⌉} (`lemmas/DIST12.md` D.1; STATEMENT v1.4.3) |
| BR1-02 | MINOR | the sample mean ε̄ of the noise is not controlled by Lemma X; its event was missing from the probability budget | ADOPT: event 𝓘_t = {ε̄² ≤ 2σ²t/n}, probability ≥ 1 − 2e^{−t}; the prefactor 3 and c = ½ of (1.1) survive (`lemmas/DIST12.md` D.2, D.4) |
| BR1-03 | MINOR | (1.1)'s size clause has no ceiling, Lemma X's has; C′ = 32 would give a wrong inclusion | ADOPT: C′ = 33 in (1.1) (`lemmas/DIST12.md` D.4 Step 2, D.5); (1.1) asserts the existence of C′ |
Not checked by BR1 (its own statement): the proof of Lemma T (outside its packet; verified separately by L3), the reader
bridges, DIST-3, the sampler results, stretch items. BR1 notes that Lemmas X, X′ fix σ*; uniformity over changing σ*_n is the
scale bridge B0's job (verified by L4).
Consequence: the master theorems now have a written proof, `lemmas/DIST12.md` (DIST-1 and DIST-2 from H, T, X, X′), which
goes to a cross-family line check together with the diff check of the statement changes and post-check amendments.
