# RETRIEVAL status (2026-11-24)

All files are in /home/fb31/SMC_Theory_Department/SMC_LIT/papers/ (outside any git repository). Each PDF was checked with `file`, `pdfinfo` and by viewing page 1. Requests were paced and sent with a generic client User-Agent. No bot challenge (Cloudflare, Incapsula, Anubis) was solved or bypassed.

## 1. Duan, "Variable selection with big data based on zero norm and via sequential Monte Carlo" (NUS working paper; versions Oct 2018, Apr 2019; SSRN 3377038, 24 pp., written 22 Apr 2019, posted 21 May 2019)

Status: FULL PAPER NOT OBTAINED. A SECONDARY SOURCE WAS OBTAINED (author's 30-slide talk).

Obtained instead:
- `Duan2018_VariableSelection_SMC_IMS_slides.pdf` (30 pp., slide deck, dated September 2018, NUS Institute for Mathematical Sciences Bayesian workshop 2018). Source: https://imsarchives.nus.edu.sg/oldwww2/events/2018/bay/files/duan.pdf. This is slides, not the paper. The saved 111-byte `Duan2019_VariableSelection_SMC.pdf` (an S3 AccessDenied XML error) was deleted.

Routes tried:
- d.nuscri.org PDF (April 2019 version): HTTP 403, S3 AccessDenied XML. No Wayback copy. The October 2018 file name is also not archived.
- SSRN abstract page: Cloudflare "Just a moment" (403). The Wayback copy of the abstract page (snapshot 2026-10-19) loads, but the Delivery.cfm PDF link in it returns an Incapsula bot page. Not obtained.
- IDEAS/RePEc: no record under ssrnwps/3377038 (404).
- Semantic Scholar and OpenAlex: both say green OA only via SSRN (no PDF URL). Semantic Scholar gave the abstract.
- Published later version: none found. Duan's later work is Duan, Li, Xu (2022), "Sequential Monte Carlo optimization and statistical inference", WIREs Comput. Stat., DOI 10.1002/wics.1598. It is a review, listed as hybrid OA, but the Wiley pdfdirect link returns a Cloudflare 403 and it is not in the Wayback. Not obtained. I found no journal article of the variable-selection paper itself. The only citing work that uses the method is Wang, Zhu, Yu (Econometrics and Statistics 2020; arXiv 2007.10160).
- The Duan, Fulop, Hsieh "Data-cloning SMC" paper was not pursued, because nothing links it to this variable-selection theory.
- rmi.nus.edu.sg/duanjc: 212-byte stub. variableselection.nuscri.org (DeepSelect product page): 403.

Human route: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3377038 (free download in a normal browser), DOI 10.2139/ssrn.3377038. Or ask the author or the NUS RMI/CRI working-paper list.

Abstract (SSRN, via Semantic Scholar):
"Selecting a subset from many potential explanatory variables in linear regressions has long been the subject of research interest, and the matter is made more important in the era of big data when many more variables become available/accessible. Of late, the l_1-norm penalty based techniques such as Lasso of Tibshirani (1996) have become very popular. However, the variable selection problem in its natural setting is a zero-norm penalty problem, i.e., a penalty on the number of variables as opposed to the l_1-norm of the regression coefficients. The popularity of the l_1-norm penalty or its variants has more to do with computational considerations, because selection with the zero-norm penalty is a highly demanding combinatory optimization problem when the number of potential variables becomes large. We devise a sequential Monte Carlo (SMC) method as a practical and reliable tool for zero-norm variable selection problems, and selecting, say, best 20 out of 1,000 potential variables can, for example, be completed with a typical multi-core desktop computer in a couple of minutes. The methodological essence is to understand that the selection problem is equivalent to the task of sampling from a discrete probability function defined over all possible combinations comprising, say, k regressors out of p>=k potential variables, where the peak of this function corresponds to the optimal combination. The solution technique sets out to sequentially generate samples, and after a while the final sample represents the target probability function. With the final SMC sample in place, we deploy the extreme value theory to assess how likely and to what extent the maximum R2 has been achieved. We also demonstrate through a simulation study the method's reliability and superiority vis-a-vis the adaptive Lasso."

Does the obtained text state theorems? The full paper was not seen, so this is unverified. The evidence available is:
- The Sept 2018 slides (30 pp.) contain NO theorem, proposition or lemma. They have only an informal importance-sampling identity, algorithm steps (density tempering from an R^2-weighted start law, ESS-adaptive schedule, resample, MH "support boosting", k-fold duplication) and a CDS application. The only "theoretical justification" is the importance-sampling identity E_f[H] = E_g[H f/g].
- The abstract promises an extreme-value-theory assessment of whether the maximum R^2 was attained (a statistical statement about the final sample's maximum). It does not mention a selection-consistency or an SMC convergence result.
- Wang, Zhu, Yu (arXiv 2007.10160, Sec. 3.4) describe the method as a non-Bayesian meta-heuristic and refer readers to "Duan (2019) for its theoretical properties". That is probably the EVT part. No explicit theorem is quoted.
- The target is f(U) proportional to exp(-SSE(U)) over k-subsets (permutations), tempered from f0 (R^2-proportional sampling without replacement). It is an optimisation/search heuristic. Selection consistency is unlikely to be proved. I would rate this "no selection-consistency theorem, possibly an EVT bound", pending a human check of the SSRN PDF.

## 2. Shi and Dunson (2011), Stat. & Prob. Letters 81(2):283-291, DOI 10.1016/j.spl.2010.10.011

Status: OBTAINED (open preprint, not the typeset journal version).
- File: `ShiDunson2011_particle_stochastic_search_preprint.pdf`, 21 pp., author manuscript titled "Bayesian Variable Selection via Particle Stochastic Search" (Shi and Dunson). It is the pre-publication Duke manuscript, a CiteSeerX copy fetched through a Wayback snapshot (2019-04-27) of citeseerx doc 10.1.1.161.819. Page 1 viewed and matches the title, authors and abstract. The text cites "Theorem 1 (Liu 2001)" (an importance-sampling result), not an original theorem.
- The earlier ~1.8 KB bot-page file did not exist in papers/ when I started. The PMC PDF route (pmc.ncbi.nlm.nih.gov/articles/PMC3029030/pdf/nihms249355.pdf, which is the NIH author manuscript) returns a 1.8 KB bot-check page. The same happens on www.ncbi.nlm.nih.gov. Europe PMC render and ptpmcrender give a 403. These were not saved.
- Differences from the journal version are possible (pagination, edits), so use the DOI for page-level citation.

## 3. Schäfer (2012) PhD thesis, Université Paris-Dauphine

Status: OBTAINED.
- File: `Schafer2012_PhD_thesis_MC_binary_vectors.pdf`, 154 pp., HAL tel-00767163v1 (submitted 19 Dec 2012), NNT 2012PA090039. Page 1 viewed (HAL cover). It was fetched from the Wayback snapshot (2024-12-04) of https://theses.hal.science/tel-00767163v1/file/Schafer.pdf. The live HAL site now serves an Anubis "Making sure you're not a bot" page, which was not bypassed.
- Contents: Ch. 2 SMC sampler, Ch. 3 parametric families on binary spaces, Ch. 4 BVS for normal linear models, Ch. 5 BVS for binary-response models, Ch. 6 pseudo-Boolean optimisation. Theorems and propositions found are in Ch. 3 only (binary-family algebra, e.g. Props 3.2.1-3.2.8, Thm 3.3.2, Props 3.5.1-3.5.12). I found no SMC convergence or selection-consistency theorem.
- Dead routes: basepub.dauphine.fr (host did not resolve), theses.fr document (not archived), arXiv (no thesis version; only the arXiv papers 1101.6037, 1111.0574, 1111.0576 and 1008.0055).

## 4. Rockova (2018), "Particle EM for variable selection", JASA 113(524):1684-1697, DOI 10.1080/01621459.2017.1360778

Status: NOT OBTAINED.
Routes tried:
- arXiv API searches (title, "particle EM", author plus EM): no preprint exists.
- OpenAlex and Semantic Scholar: the only "green OA" location is the Taylor & Francis figshare record 5286289 (CC-BY). Its single file (`uasa_a_1360778_sm7000.pdf`, 3 MB, ndownloader.figshare.com/files/9055600) is the SUPPLEMENTARY MATERIAL, not the article. I did not save it, since the request is the article.
- Author pages: veronikarockova.github.io returns 404. The Chicago Booth faculty page was fetched but exposes no PDF link.
- tandfonline.com/doi/pdf/...1360778 is the paywalled publisher link (not fetched).
Human route: https://doi.org/10.1080/01621459.2017.1360778 via library access. The supplement is at https://tandf.figshare.com/articles/journal_contribution/Particle_EM_for_Variable_Selection/5286289.

## 5. Clyde and Ghosh (2012), Biometrika 99(4):981-988, DOI 10.1093/biomet/ass040

Status: OBTAINED (published version, open in the Duke repository).
- File: `ClydeGhosh2012_finite_population_SSVS_Biometrika.pdf`, 8 pp., the published Biometrika version (pp. 981-988, Advance Access 30 Sep 2012; header shows it was downloaded from biomet.oxfordjournals.org). Page 1 viewed and matches. Source: DukeSpace item 326fd88a-cf51-4d06-8182-4b899e3d165d (handle 10161/11723, licence CC BY-NC-ND), reached via the public DukeSpace REST API bitstream endpoint, because the DukeSpace HTML pages are behind an Anubis bot check.
- The summary states that they prove renormalised posterior probabilities over sampled models are generally biased, and propose a ratio-of-Horvitz-Thompson estimator.
