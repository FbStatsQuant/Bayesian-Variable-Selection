# CITE-AUDIT: do the cited papers say what we say they say?

Task: HQ → Theory v2, owner-approved (2026-11-28). Lead: fresh Opus 5.5 (independent of the TH-SONG authors).
Scope: every citation claim in `Theory_work/Dept/song_assumptions/` {THEOREM_DEFINITIONS (TD), ASSUMPTIONS_AND_PROOF_PATHS (AP),
OWNER_DEFENSIBILITY_DOSSIER (OD)} at `dept/theory` 448d236a, and Writing's
`Docs/Writing/paper_smcbvs/sections/03_theory.tex` (W3) at `writing/main` 3445496d.
Per-claim table: [`CITE_AUDIT.tsv`](CITE_AUDIT.tsv) (claim, both verdicts, final verdict, who decided, page, short quote, reasoning, fix).

## Result

| final verdict | rows |
|---|---|
| SUPPORTED | 403 |
| PARTIAL | 36 |
| NOT SUPPORTED | 2 |
| CAN'T CHECK | 0 |
| **total** | **441** |

By file (SUPPORTED / PARTIAL / NOT SUPPORTED): TD 172/5/1, AP 70/9/0, OD 112/14/0, W3 49/8/1.
The 38 non-supported rows reduce to **16 fixes in our assumption documents (F1–F16)** and **9 fixes in Writing's Section 3 (W1–W9)**, listed below.
No claim is fabricated; no cited theorem is missing. The errors are of five kinds: a dropped prime (smallest vs largest eigenvalue),
"exponential" for stretched-exponential growth, a wrong paper behind one bib key (Wainwright 2009), scope overstatements
(fixed vs vanishing floors, "every model" vs a size window, "same object" vs analogue), and stale or wrong page locators.

## Method

1. **Claims table** (Sonnet 5.5 high): every sentence attributing content to a paper, one row per fact and location
   (441 rows, 194 distinct facts, 28 papers; TD 178, AP 79, OD 126, W3 58). The lead checked every `\cite` line of W3
   and the extractor's regex self-scan. See `CLAIMS.tsv`, `CLAIMS_SUMMARY.md`.
2. **Sources**: only the papers themselves (no abstracts, citing papers or model memory). Local copies plus open arXiv copies;
   version and pagination per paper in `PAPERS_MANIFEST.tsv`. Two paywalled papers (Chen & Chen 2008; Cramér 1936) were
   supplied by the owner mid-audit. No PDFs or extracted text are committed (they live in git-ignored `.rc_tmp/`).
3. **Double-blind verification**: verifier A = Sonnet 5.5 (high), verifier B = Sol 6.2 (codex, high), separate folders, neither
   could read the other's output nor the earlier authors' precedent/council files (`VERIFIER_BRIEF.md`). Each row: quote, page, verdict,
   one line of reasoning. The 8 rows needing the owner-supplied papers were re-run blind by fresh A and B instances (round 2).
4. **Adjudication**: the verdicts agreed on 408/441 rows (92.5%). The 33 disagreements went to a fresh Opus 5.5 (high), who read each passage
   and ruled with a quote: 15 SUPPORTED, 17 PARTIAL, 1 NOT SUPPORTED; sided with A 13 times, with B 20 times.
5. Lead check of quote fidelity: an automated search found ≈80% of the verifiers' text quotes verbatim in the paper text; the misses inspected
   were math/ligature/OCR formatting or quotes taken from page images, not invented text.

Verdict totals before adjudication: A 412 S / 26 P / 3 NS; B 395 S / 45 P / 1 NS (both after round 2).

## Fix list

Fixes in F1–F16 are to be made by the assumptions authors (not by the verifiers), then synced to Writing via the Theory Manager → Writing Manager.
Line numbers are those of the audited versions. W-fixes give W3 line numbers at 3445496d; `writing/main` 2682a942 inserted 2 lines after line 66, so add 2 for lines ≥ 67 there
(anchor by text, not by number).

### Our assumption documents (song_assumptions/)

| fix | rows | where | problem (paper says) | action |
|---|---|---|---|---|
| F1 | C142 C214 C318 | TD 86, AP 109, OD 123 | SL write ch′₁{var(x)} ≻ ε_n² (smallest eigenvalue, pp. 955–956; notation p. 952). We wrote ch₁ = largest. | **Reword**: "ch′₁{var(x)} ≻ ε_n² (smallest eigenvalue; standard normal predictors; SL pp. 955–956)". TD 61 already correct. |
| F2 | C251 C300 C301 | AP 363, OD 91, OD 92 | SL Cor 1 covers P_n < exp(Cn^α), α ∈ (0,1): stretched-exponential, not exponential (TD 59 says so correctly). | **Reword** "exponential p" → "stretched-exponential p (log p = O(n^α), α < 1)" in all three. |
| F3 | C132 (**NOT SUPPORTED**) | TD 82 | SL's (9)–(10) force r̄_n ≺ nε_n²/log P_n; at our radius ε_n² = M log n/n that is much smaller than M log n/log 2. SL's sieve is not of that order. | **Reword**: our prior-tail cutoff ≍ M log n/log 2 "plays the role of SL's sieve r̄_n (p. 951 remark); SL's (9)–(10) would force a much smaller r̄_n at this radius". |
| F4 | C148 C210 C315 | TD 87, AP 108, OD 122 | SLs (26) itself only takes monotone sequences l_n, l′_n; "vanishing lower / growing upper" is the Cor S1 choice; l_n ≫ r̄_n log P_n/n comes from (23). | **Reword**: "(26) is a two-sided sample condition on sets of size r̄_n + |t|; Thm S also needs (23), l_n ≫ r̄_n log P_n/n, and Cor S1 takes a vanishing l_n and a growing l′_n". |
| F5 | C158 | TD 89 | SL's "iff β₀,t ≠ 0" (p. 957) is for true predictors in s only. | **Reword**: "…which SL's prose claims for true predictors in s (a true x_t ∈ s is selected iff β₀,t ≠ 0) but their inclusion-only display does not give". |
| F6 | C358 | OD 270 | SL's setting: y given x Gaussian linear, x of arbitrary law with second moments; misspecification only by omitted predictors (pp. 947–948, 956–957). | **Reword**: "TM-a0 covers arbitrary second-moment misspecification at fixed dimension; SL's own setting (Thm 4) is the fixed-dimension case where misspecification comes from omitting true predictors". |
| F7 | C187 | AP 63 | Thm S (SLs p. 13) assumes "a sparse true model t", not condition (4) by name; Thms 2–3 do cite (4). | **Reword**: "(used by Thms 2–3; Thm S assumes a sparse true model t, SLs p. 13; Thm 4 instead …)". |
| F8 | C185 | AP 57 | GvO show the inconsistency empirically, only under "bad" misspecification (arXiv v3 pp. 4–5). | **Reword** "the mechanism applies" → "the Grünwald–van Ommen mechanism may apply (shown empirically, under bad misspecification)". |
| F9 | C359 C360 C361 | OD 271 | GvO (pp. 46–47) say De Blasi–Walker's covering/summability condition fails for their infinite model union; they say only that KvdV06 needs "substantially stronger regularity conditions". Neither paper states that a fixed model class is necessary. | **Reword**: "…in the spirit of Grünwald & van Ommen's finding that the covering conditions of general misspecification theorems (De Blasi–Walker 2013; cf. Kleijn–van der Vaart 2006) fail for their infinite union of models". |
| F10 | C238 C346 | AP 173, OD 203 | FRG Thm 1 (p. 4) assumes k → ∞ and an i.i.d. Gaussian design; our ≈2σ² log p derivation is right but the regime is missing. | **Add the regime**: "Fletcher–Rangan–Goyal Thm 1 (i.i.d. Gaussian design, k → ∞): ML fails when the weakest coefficient energy is below ≈ 2σ² log p (constant derived by C2 from their (6))". |
| F11 | C224 C327 | AP 124, OD 145 | YWJ (7a): ‖Xβ*‖²/n ≤ gσ₀² log p/n with g ≍ p^{2α}; grows only when p^{2α} log p ≫ n. | **Reword** "grows with n" → "may grow with n" for YWJ (SC11 wording is fine). |
| F12 | C199 C299 | AP 87, OD 90 | NH14 define m_n(ν) = p ∧ n/((2+ν) log p) on p. 6; it is used in Cond 4.5, p. 11. | **Re-cite**: "p. 6 (used in Cond 4.5, p. 11)". |
| F13 | C350 C351 | OD 229 | Rossell's λ_tm and NH14's Δ_n are fixed-design, sample quantities; our R_n(S) is a population projection residual. | **Reword** "the same object as" → "the population analogue of NH14's Δ_n and of Rossell's non-centrality λ_tm". |
| F14 | C255 C383 | AP 404, OD 312 | Status is stale: Chen & Chen (2008) Thm 1, p. 763 now read (owner copy), and it confirms the γ > 1 − 1/(2κ) threshold. SBJ p. 14 cites CC08 for a sparse Riesz condition, not for the threshold. | **Reword**: "Chen & Chen (2008) verified against the journal text (Thm 1, p. 763); Luo & Chen p. 7 attribute the same threshold". Drop "SBJ p. 14" here. |
| F15 | C003 | TD 27 | Only SL Thm 1 assumes standardized, uniformly bounded predictors (p. 952); Thms 2–4 use moment conditions. | **Reword**: "SL Thm 1 is stated for standardized predictors". |
| F16 | C088 | TD 62 | Fan & Lv App. A.7 proves their Property C (extreme singular values of wide n × p̃ submatrices, p̃ > cn, Gaussian design), not the bound on narrow submatrices that SLs (26) needs. | **Reword**: "SLs p. 16 point to Fan & Lv (2008, App. A.7) for Gaussian designs; A.7 is a related concentration result for wide submatrices, not (26) itself". |

Also: apply the owner's terminology ruling when these files are touched (no "ultrahigh" in our prose; setting = high-dimensional, p ≤ n^A).

### Writing's Section 3 (`03_theory.tex`)

| fix | rows | W3 line (3445496d) | problem | proposed text |
|---|---|---|---|---|
| W1 | C390 | 68–69 | SBJ allow log p = O(n^α) but give no rates; "slower rates" is SL only. | "…allow $\log p$ of order $n^\alpha$ with $\alpha<1$; in \citet{SongLiang2015} this comes with slower rates." |
| W2 | C393 C394 | 97 | BRT09 (Assumption 2, φ_min > c/log n) and NH14 (Cond 4.5, floor p^{−κ}) allow vanishing floors; a fixed floor is only a special case of theirs. | "Fixed floors on sparse eigenvalues are a special case; \citet{BickelRitovTsybakov2009} and \citet{NarisettyHe2014} use sample floors that may vanish slowly, of order $1/\log n$ and $p^{-\kappa}$." |
| W3 | C410 | 224 | NH14 Cond 4.4 is over models of size below K|t| (fixed K) that miss a true predictor, not every model. | "…ask the residual signal of every model with fewer than $K\sz$ predictors (a fixed $K$) that misses a true predictor to exceed…" |
| W4 | C411 | 226 | LC13's ratio is Δ_n(s)/(p₀ log p): the true model size is in the denominator. | "…and \citet{LuoChen2013} ask its ratio to $\sz\log p$ to diverge;" |
| W5 | C412 (**NOT SUPPORTED**) | 228 | refs.bib `Wainwright2009` is the Lasso paper (TIT 55(5)); "no method recovers" is Thm 2 of Wainwright's *Information-theoretic limits* paper (TIT 55(12)). | **Re-cite**: `\citep{WainwrightIT2009,FletcherRanganGoyal2009}` and add the bib entry below (W9). The old `Wainwright2009` entry is then unused. |
| W6 | C421 | 301 | SL's converse (p. 957) is for true predictors in the candidate set only. | "…and their discussion states the converse for true predictors among the candidates; here…" |
| W7 | C428 | 370 | SL assume y given x Gaussian linear with predictors of arbitrary law (finite second moments), not "Gaussian data". | "…stated there for the Gaussian linear model (Gaussian errors, predictors with finite second moments) with omitted predictors:…" |
| W8 | C434 | 381–382 | RR18 study a misspecified error law: Bayes factors stay consistent for the true model at slower rates. KL-optimal concentration is Rossell (2022). | "…are studied by \citet{RossellRubio2018}, who show that under a misspecified error distribution Bayes factors remain consistent at slower rates, and by \citet{Rossell2022}, who finds that they concentrate on the Kullback--Leibler optimal model under suitable conditions." |
| W9 | (HQ request) | 339 + refs.bib | Cramér's decomposition theorem is used without a citation; refs.bib has no entry. | Add `\citep{Cramer1936}` after "Cram\'er's decomposition theorem" and the entry below. |

refs.bib additions (DOIs checked against Crossref and the PDF first pages):

```bibtex
@article{WainwrightIT2009,
  author  = {Wainwright, Martin J.},
  title   = {Information-theoretic limits on sparsity recovery in the high-dimensional and noisy setting},
  journal = {IEEE Transactions on Information Theory},
  volume  = {55}, number = {12}, pages = {5728--5741}, year = {2009},
  doi     = {10.1109/TIT.2009.2032816}
}
@article{Cramer1936,
  author  = {Cram{\'e}r, Harald},
  title   = {{\"U}ber eine {E}igenschaft der normalen {V}erteilungsfunktion},
  journal = {Mathematische Zeitschrift},
  volume  = {41}, number = {1}, pages = {405--414}, year = {1936},
  doi     = {10.1007/BF01180430}
}
```

### Side findings (not citation errors in our text)

- Song & Liang's supplement refers to a "Lemma A.2" that is not in the supplement we hold; Thm S's printed proof bounds a max where a min is needed (already recorded in TD 62 as a Sol audit note). Both verifiers saw these; no action beyond the existing notes.
- Version notes: YWJ, GvO, Rossell 2022, SBJ, LC13, SC11, BRT09, Fan–Lv, RZ13 were read on arXiv versions (our documents cite arXiv pages for these). W3 cites journal versions without page locators, so no W3 locator depends on the version.

## All PARTIAL / NOT SUPPORTED rows

A = Sonnet 5.5, B = Sol 6.2; "adj." = decided by the Opus adjudicator.

| claim | where | paper | final | A / B | page | quote (short excerpt) |
|---|---|---|---|---|---|---|
| C003 | TD:27 | SL15 | **PARTIAL** | PART / PART | p. 952 (Thm 1 intro); pp. 953-957 (Thms 2-4) | all predictors have been standardized and uniformly bounded |
| C088 | TD:62 | FanLv08 | **PARTIAL** | PART / PART | Fan & Lv 2008 (arXiv) Sec 4, p. 24 (Property C, eq (16)); App. A.7, p. 38 | Concentration Property … holds for any n × p̃ submatrix Z̃ of Z with cn < p̃ ≤ p … Property C holds when x has a p-variate Gaussian distribution (see Appendix A.7). |
| C132 | TD:82 | SL15 | **NOT SUPPORTED** | NOT  / PART → adj. | SL15 p. 951 (Sec 2.1.1 remark after (6)) and p. 952, conditions (9)-(10) (page image) | there exists r̄n such that π(\|ξ\| > r̄n) → 0 with an appropriate rate … r̄n ln(1/εn²) ≺ nεn² (9), r̄n ln(Pn) ≺ nεn² (10) |
| C142 | TD:86 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 pp. 955-956, after Condition 3 (page image; SL define ch_i = ith largest, ch′_i = ith | by the same arguments, all predictors are identifiable if ch′1{var(x)} ≻ εn². |
| C148 | TD:87 | SL15supp | **PARTIAL** | PART / PART | SL15supp p. 13 eq (23); p. 15 eq (26); p. 16 Cor S1 | r̄n log Pn ≺ nln  (23); {ln} non-increasing, {l′n} non-decreasing (22) |
| C158 | TD:89 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 957, Cor 2 and following prose (page image) | For any true predictor xt with t ∈ t ∩ s, it will be asymptotically selected under this criterion if and only if β0,t ≠ 0 |
| C185 | AP:57 | GvO17 | **PARTIAL** | PART / SUPP → adj. | GvO17 arXiv v3 pp. 4-5 (Sec 1, Type of Misspecification; Good vs. Bad Misspecification) | we only demonstrate the inconsistency empirically. … Inconsistency can only arise under a ‘bad’ form of misspecification |
| C187 | AP:63 | SL15 | **PARTIAL** | PART / SUPP → adj. | SL15 p. 953 Thm 2; p. 956 Thm 3; SL15supp p. 13 Thm S | Theorem 2. … the model is strictly sparse, i.e. condition (4) holds … Theorem S. … Let Dn be a dataset generated from model (1) of the main text with a sparse true model t. |
| C199 | AP:87 | NH14 | **PARTIAL** | PART / PART | NH14 Sec 2 (Notation), p. 6 (reprint pagination), displayed formula for m_n(ν) | m_n(ν) = p_n ∧ n/((2+ν) log p_n) and λ_m(ν) := inf_{\|k\|≤m_n(ν)} φ#_min(X_k′X_k/n) |
| C210 | AP:108 | SL15supp | **PARTIAL** | PART / PART | SL15supp p. 13 eq (22)-(23), p. 15 eq (26), p. 16 Cor S1 (page images) | nln < ch1′(Xζ^T Xζ) ⩽ ch1(Xζ^T Xζ) < nl′n, {ln} non-increasing, {l′n} non-decreasing; (26): Pr{nln > ch1′ or ch1 > nl′n} < e^{-nC} |
| C214 | AP:109 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 956, top, after Condition 3 (page image; notation p. 952) | by the same arguments, all predictors are identifiable if ch′1{var(x)} ≻ εn². |
| C224 | AP:124 | YWJ16 | **PARTIAL** | SUPP / PART → adj. | YWJ arXiv v1 p. 7, Assumption A (7a); p. 8, Assumption C (7c) | Full β* condition: ‖(1/√n)Xβ*‖₂² ≤ g σ0² log p / n … g ≍ p^{2α} for some α > 0 |
| C238 | AP:173 | FRG09 | **PARTIAL** | SUPP / PART → adj. | FRG09 preprint p. 4, Sec III, Thm 1, display (6); MAR·SNR = (k/m) min\|xj\|² (p. 4); assumes | m(n) < (2−δ)/(MAR·SNR) k log(n − k) + k − 1 … Then even the ML estimator asymptotically cannot detect the sparsity pattern |
| C251 | AP:363 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 954, Cor 1 | Suppose that Pn < exp(Cn^α) for some α ∈ (0, 1) |
| C255 | AP:404 | ChenChen08 | **PARTIAL** | PART / PART | LC13 p. 7; SBJ p. 14 (arXiv v4); CC08 p. 763 Thm 1 and pp. 762-763 (sparse Riesz discussio | SBJ p. 14: "Assumption 4 is called the sparse Riesz condition and is also used in Chen and Chen (2008) and Kim et al. (2012)." LC13 p. 7: "[4] showed that if γ > 1 − 1/(2κ) the EBIC is selection consistent." |
| C299 | OD:90 | NH14 | **PARTIAL** | PART / PART | NH14 p. 6 (notation); Cond 4.5, p. 11 | m_n(ν) = p_n ∧ n/((2+ν) log p_n) |
| C300 | OD:91 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 954, Cor 1 | Suppose that Pn < exp(Cn^α) for some α ∈ (0, 1) |
| C301 | OD:92 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 954, Cor 1 (with Thm 2 conditions (9)-(14), p. 953) | Suppose that Pn < exp(Cn^α) for some α ∈ (0, 1) … Take rn < r̄n ≺ log^k(n) |
| C315 | OD:122 | SL15supp | **PARTIAL** | PART / PART | SL15supp p. 13 eq (22)-(23), p. 15 eq (26), p. 16 Cor S1 (page images) | {ln} non-increasing, {l′n} non-decreasing (22); r̄n log Pn ≺ nln (23); l′n = ln^-1 = √n / log^k2(n) (Cor S1) |
| C318 | OD:123 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 956, top, after Condition 3 (page image) | by the same arguments, all predictors are identifiable if ch′1{var(x)} ≻ εn². |
| C327 | OD:145 | YWJ16 | **PARTIAL** | SUPP / PART → adj. | YWJ arXiv v1 p. 7, (7a); p. 8, (7c) | ‖(1/√n)Xβ*‖₂² ≤ g σ0² log p / n … g ≍ p^{2α} for some α > 0 |
| C346 | OD:203 | FRG09 | **PARTIAL** | SUPP / PART → adj. | FRG09 preprint p. 4, Sec III, Thm 1, display (6); assumes k(n) → ∞, A with i.i.d. N(0,1/m) | m(n) < (2−δ)/(MAR·SNR) k log(n − k) + k − 1 … Then even the ML estimator asymptotically cannot detect the sparsity pattern |
| C350 | OD:229 | Rossell22 | **PARTIAL** | PART / PART | Rossell 2022 arXiv v7 p. 10, eq (8) | λtm = (Xtθt*)′(I − Hm)Xtθt*/φ* |
| C351 | OD:229 | NH14 | **PARTIAL** | PART / PART | NH14 Cond 4.4, p. 11 | Δ_n(K) := inf_{k:\|k\|<K\|t\|, k⊅t} \|\|(I − P_k)X_tβ_t\|\|²_2 |
| C358 | OD:270 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 947-948, (2) (y \| x Gaussian linear, x of arbitrary law νx); pp. 956-957, Sec 2.3, | Assume that Xs does not include all of the true predictors of model (1). Therefore, the model y = Xsβs + ε is misspecified. |
| C359 | OD:271 | GvO17 | **PARTIAL** | PART / PART | Grünwald & van Ommen arXiv v3 pp. 46-47 (Sec 6 'Consistency Theorems') | if, for all ε > 0, the model can be covered by a finite number of ε-Hellinger balls, then the Bayesian posterior eventually concentrates … if pmax = ∞, then the model has no finite Hellinger cover … the conditions for Th |
| C360 | OD:271 | KvdV06 | **PARTIAL** | PART / PART | Grünwald & van Ommen arXiv v3 p. 3 and pp. 46-47 | the strongest actual theorems to this end that we know of (Kleijn and Van der Vaart, 2006, De Blasi and Walker, 2013, Ramamoorthi et al., 2015), hold, as the authors emphasize, under regularity conditions that are substa |
| C361 | OD:271 | DBW13 | **PARTIAL** | PART / PART | Grünwald & van Ommen arXiv v3 pp. 46-47; De Blasi & Walker 2013 p. 174 | Theorem 1 (in particular its Corollary 1) of De Blasi and Walker (2013) implies … if, for all ε > 0, the model can be covered by a finite number of ε-Hellinger balls … |
| C383 | OD:312 | ChenChen08 | **PARTIAL** | PART / PART | LC13 p. 7; SBJ p. 14 (arXiv v4); CC08 p. 763 Thm 1 | SBJ p. 14: "Assumption 4 is called the sparse Riesz condition and is also used in Chen and Chen (2008) and Kim et al. (2012)." CC08 Thm 1: "If γ > 1 − 1/(2κ), then, under the asymptotic identifiability condition, …" |
| C390 | W3:68 | SBJ18 | **PARTIAL** | NOT  / PART → adj. | SBJ arXiv v4 p. 13 (Sec 4 opening) and p. 14, Assumption 1, Thm 1; cf. SL15 p. 954 Cor 1 r | strong model selection consistency … when p increases sub-exponentially with n, i.e., log p = O(n^α) for α ∈ (0, 1). … π(t \| y) converges to one in probability |
| C393 | W3:97 | BRT09 | **PARTIAL** | PART / PART | Bickel, Ritov & Tsybakov arXiv v3 pp. 8-9, Assumptions 1-2 | Assumption 2: Assume m φmin(s+m) > c0² s φmax(m) … φmin(s log n) > c/ log n |
| C394 | W3:97 | NH14 | **PARTIAL** | PART / PART | NH14 Cond 4.5, p. 11; Lemma 6.1, p. 16 | λ^n_m(ν) ≻ (… ∨ p_n^{-κ}); Lemma 6.1: inf_{\|k\|≤m_n(ν)} φ_min(X_k′X_k/n) > 0 for isotropic sub-Gaussian designs |
| C410 | W3:224 | NH14 | **PARTIAL** | PART / PART | NH14 Cond 4.4, p. 11 (page image) | There is K > 1+8/δ such that Δ_n(K) > γ_n := 5σ²\|t\|(1+δ) log(√n ∨ p_n). |
| C411 | W3:226 | LC13 | **PARTIAL** | PART / PART | LC13 arXiv p. 7, Consistency Condition | lim min{Δn(s)/(p0n ln pn) : s0 ⊄ s, ν(s) ⩽ kn} = ∞ |
| C412 | W3:228 | Wainwright09 | **NOT SUPPORTED** | NOT  / NOT  | Wainwright 2009 (Lasso paper, arXiv math/0605740v1), Abstract and Sec 1; refs.bib key Wain | if n > 2(θu+ν) log(p−s)+s+1, then the Lasso succeeds … whereas for n < 2(θℓ−ν) log(p−s)+s+1, then the probability of successful recovery converges to zero |
| C421 | W3:301 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 957, Cor 2 and following prose (page image) | For any true predictor xt with t ∈ t ∩ s, it will be asymptotically selected under this criterion if and only if β0,t ≠ 0 |
| C428 | W3:370 | SL15 | **PARTIAL** | SUPP / PART → adj. | SL15 p. 948 (2) (x has arbitrary law νx); pp. 956-957, Sec 2.3, Condition 4, Thm 4, Cor 2 | f*(y, x) dx dy = φ(y; xᵀβ*, σ*) νx(dx) dy … Assume that Xs does not include all of the true predictors of model (1). |
| C434 | W3:381 | RR18 | **PARTIAL** | PART / PART | Rossell & Rubio 2018 (arXiv) abstract and Sec 4-5 (eq (11)) | Under suitable conditions misspecified Bayes factors are consistent and induce sparsity at the same asymptotic rates than under the correct model. |

## Step 5 status (2026-11-28)

- F1–F16 applied by a separate Step-5 author (Sonnet 5.5; not a verifier) in `dept/theory` **eef1addd** (TH-SONG v1.4.1; the three files only; lead reviewed the diff).
  Owner terminology ruling: our own TD/AP/OD prose never said "ultrahigh"; the only hits in `song_assumptions/` are verbatim paper titles and one PDF path, kept as is.
- W1–W9: [`WRITING_SYNC.md`](WRITING_SYNC.md) + [`WRITING_SYNC.patch`](WRITING_SYNC.patch), against `writing/main` 2682a942. The patched paper builds cleanly (latexmk exit 0, no warnings, 45 pp.). To be applied by Writing via the Theory Manager → Writing Manager.
