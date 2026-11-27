# C2 brief — verify new literature precedents against the papers (Sonnet 5.5, effort high)

Mission TH-SONG-ASSUMPTIONS (Theory Dept Task Lead, 2026-11-27). Every assumption we propose must cite a precedent with
an EXACT, VERIFIED location (paper, theorem/condition label, page). The precedents in
`/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/writing_answers/PRECEDENTS_2026-11-17.md` are already verified (read its
"Verification rule" and copy that method exactly). Your job: verify the NEW candidate precedents below.

## Method (same as PRECEDENTS_2026-11-17)
- Obtain the paper PDF (arXiv preferred; else an open author/university copy; journal pages if open). Save PDFs ONLY under
  `/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/song/papers/` (scratch; never /tmp; never in tracked folders — the repo is public,
  full texts must not be committed). Extract text with `pdftotext -layout`; read formulas off the rendered page image
  (Read tool on the PDF page) when extraction garbles them, and mark "(page image)".
- For each item: quote the condition/theorem verbatim (short), give label, printed page number AND which version (arXiv
  vN / journal), the URL, and status VERIFIED / NOT VERIFIED / NOT FOUND / DIFFERENT TYPE. Never guess a page or label.
  If the content differs from what we expect, say so plainly — negative findings are valuable.
- Output: `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/song_assumptions/PRECEDENTS_NEW.md` (one section per
  assumption family, a summary table at the end). Do not commit/push; do not delete files; do not spawn subagents.

## Items to verify (expected content in brackets — confirm or correct)
A. Identifiability / residual-signal margin (our proposed MARGIN assumption: every model missing a true predictor leaves
   unexplained signal ‖(I−P_S)Xβ*‖² ≥ c σ² (log p + ½ log n) per missed predictor):
   1. Chen & Chen (2008), Biometrika 95(3) 759–771, "Extended Bayesian information criteria for model selection with large
      model spaces" — the identifiability condition used for EBIC consistency [something like
      lim inf_n min_{s: |s| ≤ k p0, s ⊉ s0} (Δ_n(s) / (p0 ln p)) = ∞ with Δ_n(s) = ‖μ − H(s)μ‖²]. Label + page.
   2. Narisetty & He (2014), AoS 42(2) — Condition 4.4 (identifiability, Δ_n(K) type) exact form + page (arXiv 1405.6545).
   3. Shin, Bhattacharya & Johnson (2018 JASA; arXiv 1507.07106) — any identifiability/"beta-min type" assumption
      (Assumption 5?) exact form + page.
   4. Luo & Chen (2013) or Kim, Kwon & Choi (2012) or Wang (2009) "Forward regression for ultra-high dimensional
      variable screening" (JASA) — any residual-signal identifiability condition; optional, one is enough.
B. Information-theoretic necessity of √(log p / n) signals (defends that boundary-scale signals are the hardest regime and a
   margin of that order is necessary for ANY method):
   5. Wainwright (2009), IEEE Trans. Inf. Theory 55(12) 5728–5741, "Information-theoretic limits on sparsity recovery in
      the high-dimensional and noisy setting" (arXiv math/0702301) — the necessary condition (theorem label, page).
   6. Optionally Fletcher, Rangan & Goyal (2009) IEEE-IT "Necessary and sufficient conditions for sparsity pattern recovery".
C. Posterior contraction / density consistency (for the distribution theorem):
   7. Jiang (2007), AoS 35(4) 1487–1511, "Bayesian variable selection for high dimensional generalized linear models:
      convergence rates of the fitted densities" — main theorem(s) and the conditions on r̄_n, ε_n, and its §7 remark on
      removing the model-size cap (Song–Liang p. 951 cite "Section 7 of Jiang (2007)"). Labels + pages.
   8. Ghosal, Ghosh & van der Vaart (2000), AoS 28(2) 500–531 — Theorem 2.1 (general contraction rate) label + page.
   9. Castillo, Schmidt-Hieber & van der Vaart (2015) AoS — the complexity-prior condition (2.2) π_p(s) ≤ A2 p^{−A4} π_p(s−1)
      and Theorem 2/Theorem 3 (dimension, recovery) labels + pages; and whether they need p → ∞ only with log p = o(n).
D. Misspecification (for the misspecification theorem):
   10. Kleijn & van der Vaart (2006), AoS 34(2) 837–877, "Misspecification in infinite-dimensional Bayesian statistics" —
       main theorem (Thm 2.1/2.2) label/page; what plays the role of f0 (KL projection) and the extra testing condition.
   11. De Blasi & Walker (2013), Statistica Sinica 23, 169–187, "Bayesian asymptotics with misspecified models" — Corollary 1
       (Song–Liang's Lemma 1.2) exact statement and page.
   12. Grünwald & van Ommen (2017), Bayesian Analysis 12(4) 1069–1103, "Inconsistency of Bayesian inference for misspecified
       linear models, and a proposal for repairing it" — what exactly is inconsistent (which priors/models, heteroscedastic
       noise?), the key theorem/figure, page. We need to know precisely which conditions exclude their phenomenon.
   13. Rossell (2022), Bayesian Analysis 17(2), "Concentration of posterior model probabilities and normalized L0 criteria"
       (arXiv 1807.08336) — results on posterior model probabilities under MISSPECIFICATION (concentration on the
       KL-optimal model), conditions, labels, pages.
   14. Rossell & Rubio (2018), JASA 113(524), "Tractable Bayesian variable selection: beyond normality" — the result(s) on
       model selection under a misspecified error distribution (label, page).
E. Dimension conventions:
   15. Fan & Lv (2008), JRSS-B 70(5), SIS — condition log p = O(n^ξ) (label, page) and Appendix A.7 (concentration property
       for Gaussian designs; Song–Liang supp. p. 16 cite it).
   16. Johnson & Rossell (2012), JASA 107(498) — their dimension condition (p ≤ n? p = O(n^γ)?) and eigenvalue condition;
       label + page. The PDF is at `/home/fb31/Bayesian-Variable-Selection/Papers/Core_bibliography/17_2012_Johnson_Rossell_Bayesian_Model_Selection_in_High_Dimensional_Settings.pdf` (read-only).
   17. Yang, Wainwright & Jordan (2016, AoS 44(6)) — their dimension condition (log p = o(n)?) and β-min display (8): page.
F. Song & Liang (2015) supplement facts (local copy, read-only:
   `/home/fb31/Bayesian-Variable-Selection/Papers/Core_bibliography/32b_2015_Song_Liang_supplement.pdf`): verify the
   exact statements and printed page numbers of Lemma 1.1, Lemma 1.2, Theorem S, conditions (22)–(26), Corollary S1,
   Lemma S2, Lemma A.2 (Appendix) — quote them.

Priority if time is short: A1, A2, B5, C7, D11, D12, D13, F, then the rest. When done, reply with a ≤ 25-line summary.
