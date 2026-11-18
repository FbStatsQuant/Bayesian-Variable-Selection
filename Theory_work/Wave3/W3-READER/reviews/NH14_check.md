# NH14 check: Narisetty and He (2014), Lemma 6.1 (anchor of row 1.2 / Theorem 2, H5 card 17)

Requested by the manager (owner's verified-precedent rule): check the anchor against the journal version, Ann. Statist. 42(2), 2014, DOI 10.1214/14-AOS1207. Access date 2026-11-17. No PDF is committed.

## What row 1.2 claims
"For centred rows this contains the isotropic sub-Gaussian rows of Narisetty and He (2014, Lemma 6.1), the case $\Sigma_n=I$." (`CLAIMS_CARD.md` row 1.2; `READER_VERSIONS.md` §2 remark (ii).)

## Journal version: NOT ACCESSED
- `https://doi.org/10.1214/14-AOS1207` redirects (302) to `https://projecteuclid.org/journals/annals-of-statistics/volume-42/issue-2/Bayesian-variable-selection-with-shrinking-and-diffusing-priors/10.1214/14-AOS1207.full`. WebFetch of that URL returned empty content (two attempts, by the fetch subagent and by the editor).
- The `.pdf` variant of the same Project Euclid path also returned empty content (editor, 2026-11-17).
- Consequence: the journal lemma number and page numbers are unverified. The card says "verified against arXiv v1; journal version not accessed".

## arXiv version (arXiv:1405.6545, single version v1): read from the PDF page images
The PDF is typeset in the AoS/IMS layout (running head "N. N. NARISETTY AND X. HE"; its references carry the supplement DOI 10.1214/14-AOS1207SUPP), with printed pages 1–30 (not the journal's 789–817).

Statement, printed p. 16, Section 6 ("Discussion of the conditions"), verbatim (transcribed from the page image):
> LEMMA 6.1 (MNEV for sub-Gaussian random matrices). Suppose that the rows of X_{n×p_n} are independent isotropic sub-Gaussian random vectors in R^{p_n}. Then there exists a ν > 0 such that, with probability greater than 1 − exp(−w′n), inf_{|k|≤m_n(ν)} φ_min(X_k′X_k/n) > 0.

- Lead-in, p. 16: "We now show that this requirement is satisfied with high probability if the design matrix consists of independent sub-Gaussian rows." Follow-up, pp. 16–17: "A proof of Lemma 6.1 is provided in Section 11. …"
- Proof, printed p. 28 (Section 11): "The rows of X_k are n independent sub-Gaussian random isotropic random vectors in R^{|k|}. … Due to Theorem 5.39 of Vershynin (2012) …". The supplement (10.1214/14-AOS1207SUPP) holds Theorems 4.1, 4.2 and Lemma 4.2, not this proof.
- "Isotropic" is not spelled out as Σ = I in the statement; by the usual definition it means identity covariance (second-moment matrix), so independent isotropic sub-Gaussian rows are the case Σ_n = I for centred rows.

## Result for the card
- Lemma number and statement match the claim (arXiv v1): "isotropic sub-Gaussian rows", so "the case Σ_n = I" is right for centred rows (see the Opus check below).
- Pages: statement on arXiv v1 p. 16 (discussion continues p. 17), proof p. 28. Journal pages not known.
- Card wording: "(2014, Lemma 6.1; verified against arXiv v1 pp. 16–17; journal version not accessed)".

## Opus check (fresh, claudeAgent_personal, claude-opus-5-5, effort high; 2026-11-17): CONFIRMED-WITH-CORRECTIONS
Independent read of the arXiv PDF (30 pages, AoS layout, printed pp. 1–30):
- Lemma 6.1 ("MNEV for sub-Gaussian random matrices") is stated on p. 16 in §6; the proof is on p. 28 in §11 (it proves Lemmas 4.1 and 6.1, citing Vershynin 2012, Thm 5.39). The transcription above matches word for word. Page 17 only continues the discussion, so "statement p. 16" is exact.
- "Isotropic" is not defined in the paper; it is used as in Vershynin (second-moment matrix = I, no mean-zero requirement). So "for centred rows" is needed and correct; centred isotropic rows have Σ = I. The card's condition (sub-Gaussian along sparse directions, fixed L) is weaker than the paper's all-direction condition, so the containment holds, with L of the order of the sub-Gaussian norm bound.
- Correction 1 (applied): the paper's rows are independent, not identically distributed, while the card's class is i.i.d. The card now says "contains the i.i.d. case of the isotropic sub-Gaussian rows of Narisetty and He (2014, Lemma 6.1), the case Σ_n = I".
- Correction 2 (applied): a fixed L needs a sub-Gaussian bound uniform in n; the card adds "(with a uniform sub-Gaussian bound)".
- The lemma's conclusion is a design-regularity fact (inf over |k| ≤ m_n(ν) of φ_min(X_k'X_k/n) > 0 with probability > 1 − exp(−w'n), used for their Condition 4.5), not a posterior result; the card claims only containment of the class of rows.
- Journal version: two attempts, no text (Project Euclid `.full` returned empty content; the DOI link redirects to that URL). The journal lemma number and pages remain unverified, as the card says.
