# v1.1a WEAKER — quote check against headline rows and reader versions (HQ request, CP3 package; lead, read-only)

Change v1.1a (STATEMENT.md:128-130): BASE's row-wise Kullback–Leibler reading ("y_i | x_{𝒞,i} is N(α + a + x_{𝒞,i}ᵀβ^𝒞,
σ²_𝒞), SL's f₀") is kept only for jointly Gaussian rows with a **deterministic** intercept α; the dropped case is an intercept
α(X^r_𝒞) depending on the whole candidate design (K1-1). Files read: W3-READER worktree at 45d39fb4.

| file:line | text | quotes the row-wise reading? | affected by v1.1a? |
|---|---|---|---|
| `W3-READER/.../READER_VERSIONS.md:404-406` (row thm4 Remark) | "N(α′ + x_𝒞ᵀβ^𝒞, σ²_𝒞) is the conditional law of y given the candidates, hence the Kullback–Leibler projection …" | **Yes in form** (a per-row conditional law, SL's f₀ reading) | **No**: its setting (`:382-385`) is iid jointly Gaussian rows, Σ_𝒞𝒞 ≻ 0, y_i = α + … + ε_i with α a fixed constant and ε independent of the rows — exactly the deterministic-intercept case that v1.1a keeps (STATEMENT.md:128-130; proof `lemmas/H1_plus.md` H1.4(ii)) |
| `W3-READER/.../CLAIMS_CARD.md:41` (row 1.4) | "the posterior concentrates on the support of the best candidate predictor …; Song–Liang Theorem 4 analogue" | No (no KL or conditional-law sentence) | No |
| `W3-MISR-R/READER_DELTA.md:50-51` (proposed Remark) | "The law in (A0) is the conditional law of y given the candidates, hence the Kullback–Leibler projection …" | It states the full-design conditional law; with (A0)'s independent rows it is also per row | **No**: (A0) has a constant α′ and states this law as its hypothesis (STATEMENT.md:126-128, reading (ii), with α′ deterministic) |
| `W3-MISR-R/READER_DELTA.md:17` (summary row) | Hellinger/KL versions "around the (A0) law with its mean centred over the sample" | No | No |

**Verdict.** The manager's reading is confirmed with one refinement: READER_VERSIONS.md:404-406 does state a row-wise
(per-row conditional law / KL projection) reading, but only in a deterministic-intercept setting, which v1.1a retains. No
headline row or reader version relies on the dropped case (an intercept depending on the candidate design). No H5 card is
needed for v1.1a.
