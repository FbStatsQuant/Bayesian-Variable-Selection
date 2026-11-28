# CITE-AUDIT Step 1: claims extraction summary

Scope: 4 input files read in full (TD = THEOREM_DEFINITIONS.md 267 lines; AP = ASSUMPTIONS_AND_PROOF_PATHS.md 409 lines; OD = OWNER_DEFENSIBILITY_DOSSIER.md 316 lines; W3 = .rc_tmp/cite_audit/src/03_theory.tex 406 lines). No PDFs opened, nothing verified. Output table: `claims.tsv` (tab-separated, UTF-8, header as specified). Generator scripts: scratch scripts (not committed).

## Conventions

- `claim_id` C001-C441 in file order TD, AP, OD, W3; within a file ordered by first line number.
- `dup_of` = first row with the same fact (same paper, same content). 'Fact' identity is my judgement; rows with the same `dup_of` can differ slightly in detail or page (see notes below).
- paper_full is taken from refs.bib where the key exists there (W3 keys, plus the same papers when cited in TD/AP/OD). The three docs have no reference list of their own; for Jiang07, Jiang05, DBW13, KvdV06, Liang09 (not in refs.bib) paper_full says so and gives no invented details. 'SC11' in AP/OD is resolved to ShangClayton11 (refs.bib key ShangClayton2011); 'MY09' to Meinshausen & Yu 2009 (refs.bib MeinshausenYu2009); 'SBJ' to Shin-Bhattacharya-Johnson 2018.
- Math transliteration: `≻` b_n ≻ a_n (= SL notation: a_n/b_n → 0), `≺` its converse; Greek letters and ≤ ≥ → written as Unicode; ASCII `'` = transpose; `^` = superscript; `ch1`/`ch1'` kept as in TD (ch1 = largest, ch1' = smallest eigenvalue per TD line 62).
- SL15 = Song & Liang 2015 main text (journal pages); SL15supp = its online supplement (SLs).

## Counts

**Total rows: 441** (unique facts, i.e. dup_of empty: **194**; duplicate rows: 247)

| file | rows | unique facts (dup_of empty) |
|---|---|---|
| TD | 178 | 137 |
| AP | 79 | 36 |
| OD | 126 | 8 |
| W3 | 58 | 13 |
| **all** | **441** | **194** |

| paper_key | rows | unique facts |
|---|---|---|
| SL15 | 219 | 91 |
| SL15supp | 77 | 35 |
| NH14 | 39 | 12 |
| YWJ16 | 11 | 4 |
| LC13 | 10 | 5 |
| GvO17 | 9 | 4 |
| SBJ18 | 9 | 5 |
| Jiang07 | 7 | 5 |
| Rossell22 | 7 | 4 |
| ShangClayton11 | 6 | 3 |
| FRG09 | 5 | 3 |
| BRT09 | 5 | 1 |
| ChenChen08 | 4 | 2 |
| Wainwright09 | 4 | 2 |
| Cramer36 | 4 | 1 |
| JR12 | 4 | 1 |
| RZ13 | 4 | 1 |
| DBW13 | 3 | 3 |
| MY09 | 3 | 1 |
| FanLv08 | 2 | 2 |
| CSV15 | 2 | 2 |
| ScottBerger10 | 1 | 1 |
| Jiang05 | 1 | 1 |
| Liang09 | 1 | 1 |
| KvdV06 | 1 | 1 |
| CvdV12 | 1 | 1 |
| BB04 | 1 | 1 |
| RR18 | 1 | 1 |

## Bare bibliographic mentions (no content attributed; NOT in claims.tsv)

- TD:9 : SL = Song & Liang (2015), JRSSB 77(5), 947-972 (journal pagination): abbreviation definition
- TD:10-13 : SLs = online supplement (20 pp., printed page = PDF page; 'main-text journal page = PDF page + 946'; how/where obtained): provenance note
- TD:45 : Section heading 'Every important result in Song & Liang (2015), read directly'
- OD:14 : 'SL means Song & Liang (2015) main text (journal pages) and SLs its supplement (printed pages)': abbreviation definition
- OD:26 : A-NEC score-card cell 'a comparison with SBJ, NH14, BRT09, SL (26), not dominance': mentions only, content is in OD 120-125 (claimed there)
- OD:195 : 'A comparison with NH14, not a dominance claim': lead-in to bullets that are claimed (OD 196-198)
- AP:404, OD:312 : 'Bayesian Analysis 2017 labels / pagination of Grünwald-van Ommen not verified; verified on the 2014 arXiv text': a verification-status note (page/label), no content claim
- W3:10 : 'Table~\ref{tab:sl-map} lists the counterparts in \citet{SongLiang2015}': pointer to the table; content is claimed on W3 398-402 (caption W3:392 also claimed)
- AP:6-7, AP:20, OD:14 : 'PRECEDENTS_2026-11-17' (P17), 'PRECEDENTS_NEW' (PN), 'ASTRA/FABLE R1/R2' advisor files: internal documents; (PN/P17 codes such as 'PN A2', 'P17 B6' appear inside claim rows' locators as the page-source pointers)

## Ambiguous items (unsure whether to count / how to split)

- TD:124, TD:148, TD:202 : Section headings 'TD ... (SL Theorems 1-2, Corollary 1)', 'TS ... (SL Theorem 3, Theorem S, Corollary S1)', 'TM ... (SL Theorem 4, Corollary 2)': mapping labels, not counted; the content they map is claimed in rows TD 57-65 / TD 82-89.
- TD:81 (LC13 rows: C123,C125) : LC13 'threshold concerns EBIC under its own identifiability assumptions' counted as a (vague) LC13 claim; it is mostly our hedge.
- TD:82 : Three derived/consequence statements counted as SL claims, flagged '(derived)': 'SL's (9)-(10) would fail at r̄_n ≍ n'; 'SL's sieve r̄_n ≍ M log n/log 2'; 'does not inherit SL's entropy conditions' (the last NOT counted: no specific content).
- TD:90 : 'We do not split predictors, so there is no screening stage...': implies SL has a screening/split stage; not counted separately (implicit; no theorem/page attributed).
- TD:216 : 'The argument is direct and avoids De Blasi-Walker': implicit claim that De Blasi-Walker is the route for a.s. KL-projection concentration; not counted (covered by DBW13 Cor 1 rows TD 64).
- TD:63 : Audit note that Thm S's printed ≻ condition 'does not follow by substitution' at Cor S1's endpoint: counted (corS1-endpoint) but it is our audit assertion about SL, repeated at OD 299.
- TD:62, TD:61 : 'Sol audit' remarks (max vs min; contrast size r̄_n+|t|-1 vs r̄_n) counted as claims about what SL's proofs print.
- AP:93, AP:103, AP:245, AP:273, AP:288, AP:341, AP:347, AP:350, AP:402-403, TD:131, W3:299, OD:101 : Named classical tools without paper attribution (Paley-Zygmund, Cauchy interlacing, Fubini, Borel-Cantelli, Pareto-like tails, Beta law, SLLN, LIL, Markov inequality): NOT counted. Only 'Cramér's decomposition theorem' (TD 218, AP 204, OD 253, W3 339) is counted as a named-theorem attribution (paper_key Cramer36, no bib entry).
- AP:171 : 'Corollary C-ii is the standard sparse-eigenvalue plus beta-min pair' (genre claim, no paper cited): NOT counted.
- W3:68 : 'which leads to slower rates' after citing SL and SBJ: counted as two rows (SL15 dup of Cor 1 rate; SBJ18 new), but may only be our own remark.
- W3:97 : BRT09 and NH14 cited together for 'fixed floors on sparse eigenvalues' (counted as two rows); see inconsistency note (b) below.
- W3:252-253 : Four papers cited for 'selection consistency under other priors or designs': one row each, content generic (counted).
- W3:392 : Caption 'Results of Section 2 of SL' counted (sl-sec2-contents): Thm S and Cor S1 are in the supplement, not SL Section 2; row text says 'Thms 1-4, Cors 1-2 (and Thm S)'.
- W3:398-402 (table) : Table cells 'Their result' column counted as claims about SL's results (rows dup of earlier facts).
- TD:93, TD:91 : SL-11/SL-13 mapping cells (SAM consistency informal; q̂_j→q_j): internal map, content claimed at TD 67, 69.
- OD:108 : '(P17 B7b note)': internal precedents file, not an external paper.
- OD:271 : KvdV06 and DBW13 rows are content attributed only through GvO17's characterisation ('general theorems need a fixed model class'); locator none.

## Internal-consistency observations noticed while extracting (for the lead; not verified)

- (a) SL Condition 3 Gaussian sufficient form is written two ways: TD 61 'var(x_k + Σ b_i x_{j_i}) ≻ ε_n²' vs TD 86 / AP 109 / OD 123 'ch₁{var(x)} ≻ ε_n²' (ch₁ = largest eigenvalue per TD 62/48 usage; a floor needs the smallest). Page pp. 955-956 in all.
- (b) W3 line 97 says BRT09 and NH14 use *fixed* floors on sparse eigenvalues; AP 106/110 and OD 120/124 describe BRT09 Assumption 2 as a c/log n sample floor and NH14 Cond 4.5 as a floor ≳ p_n^{-κ} on the min nonzero sample eigenvalue (vanishing, not fixed).
- (c) Location of SL's '(22) is hardly satisfied': TD 62 says SLs p. 15; AP 108, OD 122, OD 293 say SLs pp. 15-16.
- (d) SL strict sparsity (4) 'used by': TD 58-59 (Thm 2, Cor 1), AP 63 'Thms 2-3 and Thm S', OD 66 'Thms 2-3'.
- (e) Dimension range of SL Cor 1: TD 59 'P_n < exp(Cn^α), α∈(0,1) (stretched-exponential, not exp(cn))'; AP 363 'excludes exponential p, which SL cover (Cor 1)' and OD 92 'SL's exponential range (Cor 1)'.
- (f) NH14 Cond 4.3, p. 11 is cited both as a Gaussian fixed-design model assumption (AP 53, OD 49) and as 'the size of the true model |t| is fixed' (AP 63, OD 66): possibly the same condition covering both, but two different contents.
- (g) W3 392 caption says Section 2 of SL while the table includes Theorem S (supplement-only per TD 9-13, 62).
- (h) TD 56 attributes the EBIC formula/link to SL pp. 951-952 while TD 81 attributes the consistency threshold γ > 1 − 1/(2A) to Luo & Chen p. 7 'attributed to Chen & Chen 2008' (primary CC08 text unverified, AP 404/OD 312).

## Self-check (regex re-scan of each file)

Pattern: years 19xx/20xx, Thm, Theorem, Lemma, Cor, Corollary, Prop, Proposition, Condition, `Assumption (`, `p.`/`pp.`, `\cite`, `et al`, SL/SLs, and author/abbreviation names (NH14, SBJ, YWJ, JR12, BRT, MY09, RZ, SC11, P17, PN, Luo, Chen, Wainwright, Fletcher, Rossell, Grünwald, Jiang, Blasi, Kleijn, Scott, Fan, Barbieri, Castillo, Rudelson, Johnson, Narisetty, Song, Liang, Cramér). A hit line counts as covered when some claims.tsv row of that file has it in its line span. Also checked the reverse direction: for each row, the cited line span contains a keyword for its paper (8 W3 rows flag only because the sentence says 'they/their' or 'Theorem S' after the author was named on the previous line).

| file | hit lines | covered by claims.tsv | uncovered (all classified) |
|---|---|---|---|
| TD | 69 | 48 | 21 |
| AP | 53 | 40 | 13 |
| OD | 81 | 71 | 10 |
| W3 | 49 | 35 | 14 |

Classification of every uncovered hit line:
- **Internal / metadata, not claims:** TD 1, 3, 16, 34, 176, 251; AP 3, 4, 7, 20, 28, 152, 155, 161, 245, 298, 306, 378 (advisor/council files, Lemma W, 'Engine decision', 'Fubini', title lines); OD 3, 108, 189, 237, 241, 242, 303; W3 4, 5, 7, 130, 231, 249, 250, 295, 303, 377, 378, 384, 385 (`\ref` to our own theorems/assumptions).
- **Table headers / section headings:** TD 24, 45, 54, 73, 79 (headers); TD 124, 148, 202 (mapping headings, ambiguous list).
- **Bare mentions:** TD 9, 10, 11; OD 14, 26, 195; W3 10 (see bare list).
- **Ambiguous, not counted:** TD 90, 91, 93, 216; AP 171.
No hit line is left unclassified.
