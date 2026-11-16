# Base KL sentence — verdict (post-CP3 task A; lead Claude Opus 5.5; 2026-11-16)

**Sentence.** W3-MISR `STATEMENT.md:191-195` (in Cor-H; proof `lemmas/G_corollaries.md:91-93`): "Kullback–Leibler reading,
in the setting of Corollary G only: there the conditional law of y_i given the candidate covariates x_{𝒞,i} … is
N(α′ + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞), which belongs to the candidate linear-Gaussian class and is therefore the Kullback–Leibler minimiser
within it (SL's f₀, for centred rows)".

**Verdict: FALSE as stated (for a non-deterministic intercept); TRUE for a deterministic intercept.**
- *Scope as written.* Corollary G's setting (`STATEMENT.md:164-165`) writes y^r = α1 + X^r_𝒞β_𝒞 + X^r_𝓜β_𝓜 + ε and lists the
  n-dependent parameters "(m, Σ, β, σ², p)" without α; it does not declare α deterministic, and the parent's standing
  convention (`STATEMENT.md:38`, the definition of GR^c used by Cor-G(a)) is "the intercept may be random and dependent on
  everything". Cor-G(a)'s conclusion (GR^c | σ(X^r_𝒞)) is indeed true for any random α (Uᵀ1 = 0), so the setting admits it.
- *Counterexample (existing, reviewed).* `reviews/L1_statement_lock_sol.md:7` (finding L1-1, Sol statement lock): iid
  standard Gaussian candidate rows, no omitted columns (or add one independent N(0, 1) omitted column, β_𝓜 = 1),
  independent N(0, 1) noise, α := (X^r_𝒞)²_{2,1}. All hypotheses of Cor-G hold (rows iid N(m, Σ), Σ_𝒞𝒞 ≻ 0, ε independent
  of X^r, σ²_𝒞 > 0), but y_1 given x_{𝒞,1} is a Gaussian plus an independent χ²₁ shift, not N(α′ + x_{𝒞,1}ᵀβ^𝒞, σ²_𝒞) for any
  constant α′. Re-confirmed by the second Sol reviewer: `reviews/K1_linecheck_sol.md:7-11` (K1-1, with α(X) = X₁²). The
  proof line `G_corollaries.md:91` ("y_i | x_{𝒞,i} ~ N(α + a + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞) independently over i") silently treats α as
  a constant.
- *Deterministic intercept.* With α a constant the sentence is true; this case is carried by W3-MISR-R:CorH-plus, KL
  reading (ii), `W3-MISR-R/STATEMENT.md:128-130` (proof `lemmas/H1_plus.md` H1.4), council R3 PASS.
- *New mathematics?* None. The counterexample is L1-1 verbatim (reviewed twice by Sol); the only step added here is
  reading the parent's text (`STATEMENT.md:38`, `:164-165`) as admitting a random α, which is a reading of the record, not a
  mathematical argument. Hence no Sol check was run (per the manager's rule for this task).
- *Registry impact.* None on any registered conclusion field: W3-MISR:Cor-H's conclusion ("in-sample average Hellinger
  contraction … around the projected law") does not mention the KL reading; the reader row (READER_VERSIONS.md:404-406) uses it
  only in a fixed-intercept setting (`reviews/V11a_quote_check.md`).

**Tombstone text for the recorder (≤3 lines):**
> Not carried over by W3-MISR-R:CorH-plus: the parent's row-wise Kullback–Leibler reading (W3-MISR STATEMENT.md:191-195) for
> a non-deterministic intercept, which is false there (counterexample W3-MISR-R reviews/L1_statement_lock_sol.md L1-1); with a
> deterministic intercept it is carried (W3-MISR-R STATEMENT.md:128-130). Erratum: W3-MISR-R reviews/post_cp3/ERRATUM_W3-MISR_KL.md.
