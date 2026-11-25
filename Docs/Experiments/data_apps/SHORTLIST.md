# Real-data applications for SMC-BVS at large p: a shortlist (scout, 2026-11-18, Opus 5.5)

**Summary**
1. Best fit: **Arabidopsis flowering time**. Use the Atwell 2010 lines (n ≈ 160–194 per trait) for discovery and the 1001 Genomes FT10/FT16 lines for replication. This gives n ≈ 200 at p from 2·10⁵ up to about 10⁶.
2. The single 10⁶ showcase is 1001G FT10 on all lines (n ≤ 1,135). It is expensive (about 1k+ core-h per fit), and memory at n ≫ 200 is untested.
3. Best "near-truth" set: the yeast BYxRM cross (n = 1,008, p = 11,623, 46 traits, 591 QTL, so about 13 QTL per trait). Fit subsamples of n = 200 and score them against the full-n map.
4. Two open human cases: Geuvadis eQTL (n = 373 EUR, 1000G genotypes), and the epigenetic clock (GSE40279 for discovery, GSE87571 for replication).
5. Cheaper extras: CCLE drug response (NQO1 for 17-AAG as a positive control) and the rat-eye TRIM32 benchmark (n = 120).
6. Common risks: population structure (our model has no kinship term), real LD much stronger than AR(0.6) (near-duplicate columns), and dense signals (clocks).

**Cost basis.** Measured at n = 200 (V mode): 2.4 / 42 / 437 core-h at p = 10⁴ / 10⁵ / 10⁶. I assume cost is linear in p. For n, I use the plan's n-factors from §6.1 (×1.5 at n = 400, ×2.25 at n = 800) and extrapolate to about ×2.5–3 at n ≈ 1,000.
- Every number below is **extrapolated, not measured**.
- T mode costs roughly 20–45× V.
- Real-data correlation (blocks of r ≈ 1) may enlarge the blocks and trigger escalation. Run a 10⁴ pilot first.

---

### 1. Arabidopsis flowering time: Atwell lines for discovery, 1001G for replication (rank 1)
- **Data:** AraPheno study 1, Atwell et al., *Nature* 2010. The study page says "~250k SNPs in 199 accessions".
  - Flowering-time phenotypes with their n: FT10 194, FT16 193, LD 167, SD 162, FLC 167, FRI 164 (counts from the AraPheno study page).
  - FLC and FRI are recorded as "ratio" phenotypes (expression traits): a built-in **cis positive control**.
  - p ≈ 2–2.5·10⁵ on the chip. If the Atwell lines are in the 1135 set, the 1001G SNPs could raise p to about 10⁶ at n ≈ 190, which is our sweet spot (the overlap is **not verified**).
- **Access:**
  - Phenotypes: https://arapheno.1001genomes.org/study/1/ (CSV/JSON/PLINK; whole database at `/static/database.zip`, size not verified). Licence: no formal one. The FAQ says "Data on AraPheno is public. Please cite…".
  - Location of the 250k genotype file: **not verified**.
- **Correlation:** LD decays over about 10 kb, giving AR/block-like structure. There is also strong genome-wide structure (factor-like), outside the proved designs.
- **Validation:**
  - (a) A priori loci: FRI, FLC, and the FLC/FRI expression phenotypes as positive controls.
  - (b) Replicate FT10/FT16 on 1001G accessions that are not in the Atwell set (study 12; a different experiment).
  - (c) Held-out prediction.
- **Compute:** p = 2.2·10⁵ at n ≈ 190: about 90 core-h per fit, about 0.45k for 5 seeds. At p ≈ 10⁶: about 440 per fit, about 1.3k for 3 seeds.
- **Risks:** Confounding by structure is the main one. Atwell report that flowering traits are the most confounded, and a later review says even re-finding FLC/FRI "was not straightforward". Mitigation: project y and X off the top PCs (a preprocessing choice to declare). Also: n per trait is about 160–194; imputation choices.

### 2. 1001 Genomes FT10/FT16 at p ≈ 10⁶ (rank 2, the showcase)
- **Data:** FT10 has 1,163 values in AraPheno and FT16 has 1,123 (https://arapheno.1001genomes.org/study/12/). Genotyped lines: 1,135, so n is at most 1,135 (the exact overlap is not verified).
  - SNPs: about 10⁷ raw; about 10⁶ after a MAF/LD filter (the filtered count is **not verified**).
- **Access:** https://1001genomes.org/data/GMI-MPI/releases/current/
  - Files: SNP + short-indel VCF, 18 GB; with TAIR10, 132 GB; a `SNP_matrix_imputed_hdf5/` directory (size not verified).
  - Policy (https://1001genomes.org/policy/): "may be freely downloaded and used by all who respect the restrictions". It has a waiting-period clause on redistribution; whether that has lapsed since the Cell 2016 paper is not stated (not verified). It is not a CC licence.
- **Correlation:** As in candidate 1, but at genome scale.
- **Validation:** FLC, SVP, VIN3, FT and DOG1 appear as labelled FT10 peaks in a Nordborg lecture slide (indicative only; confirm against Cell 2016 before using). Also FT10 against FT16, and held-out prediction.
- **Compute:** About 1.1–1.4k core-h per fit at n ≈ 1,000, about 4k for 3 seeds.
  - Memory risk: §6.1 gives about 2·10⁹ table codes at n ≥ 256 against 2·10⁸ at n = 200.
  - Fallback: random n = 200 subsets, about 440 core-h per fit.
- **Risks:** Structure (worse than in candidate 1), cost, the n ≫ 200 memory wall, and redistribution terms.

### 3. Yeast BYxRM segregants (Bloom et al., *Nature* 2013) (rank 3, best validation)
- **Data:** n = 1,008 haploid segregants. Markers: "30,594" SNPs collapsed to "11,623 unique genotypic markers". 46 traits, 591 QTL in total, so about 13 per trait, which matches our 5–14 sparsity.
- **Access:** Supplementary files (NIHMS429465-supplement-1 to 5) at https://pmc.ncbi.nlm.nih.gov/articles/PMC4001867/. Location of the genotype matrix and the licence: **not verified**.
- **Correlation:** Pure linkage: AR(1) with ρ → 1 along each chromosome, and no population structure. This is the cleanest real analogue of our AR design.
- **Validation:** Fit n = 200 subsamples and score them against the published full-n QTL map. That gives something close to a truth-based recovery score. Albert et al. (eLife 2018) has 1,012 segregants of the same cross, but overlapping, so it is not independent.
- **Compute:** About 3 core-h per fit at n = 200, and about 8 at n = 1,008. All 46 traits × 5 seeds at n = 200 is about 0.7k core-h.
- **Risks:** p is only about 10⁴, so this does not show scale. Some traits are partly epistatic (about half the heritable component for some). Marker r ≈ 1 makes "which marker" ill-posed, so score at the interval level.

### 4. Geuvadis LCL eQTL with 1000 Genomes genotypes (rank 4)
- **Data:** RNA-seq on 462 individuals (EUR 373, YRI 89). Response: expression of one gene. X:
  - a cis window, p ≈ 10³–10⁴ (not verified per gene); or
  - genome-wide, p ≈ 10⁶ after a MAF filter.
- **Access:** ArrayExpress E-GEUV-1/2/3; Geuvadis states the data are "freely and openly available with no restrictions" (the ArrayExpress page did not render for me). 1000G (https://www.internationalgenome.org/IGSR_disclaimer): "available without embargo"; EMBL-EBI terms of use.
- **Correlation:** Human LD blocks, the block/AR design.
- **Validation:**
  - The cis location is known a priori. A genome-wide fit should put its mass in cis and find nothing in trans, a natural "null elsewhere" test.
  - Replicate in GTEx/eQTLGen summary statistics (open summaries; GTEx genotypes are controlled).
  - Compare with SuSiE credible sets.
- **Compute:**
  - cis: up to about 4 core-h per gene at n = 373, so hundreds of genes are affordable.
  - Genome-wide: about 650 core-h per fit.
- **Risks:** Expression factors (PEER/batch) need regressing out. Multiple causal SNPs in LD. Most genes have 1–3 signals, sparser than our designs.

### 5. Epigenetic clock: GSE40279 for discovery, GSE87571 for replication (rank 5)
- **Data:**
  - GSE40279 (Hannum 2013): n = 656 whole blood, 450K array (485,577 markers; sex chromosomes dropped, p ≈ 4.7·10⁵). Response: chronological age.
  - GSE87571 (Johansson 2013): N = 421 leukocytes, 476,366 sites. The GEO pages did not load (captcha), so the series sample counts and file sizes are **not verified**.
- **Licence:** NCBI GEO disclaimer: NCBI places no restrictions on use, but submitters may claim rights.
- **Correlation:** Local co-methylation (AR-like along islands) plus strong cell-type-composition factors (factor-like, outside the proved scope except C9).
- **Validation:** Cross-cohort replication, and held-out age MAE against the Hannum/Horvath clocks. Overlap with published clock CpGs: from the literature, not checked here.
- **Compute:** About 200 core-h per fit at n = 200 (subsample), about 450 at n = 656. 3 seeds: 0.6–1.3k.
- **Risks:** **The age signal is not sparse.** Clocks use about 70–350 CpGs, so the posterior may sit at our size cap. Cell-mix confounding, normalisation burden (raw IDATs), batch effects.

### 6. CCLE / DepMap drug response (rank 6)
- **Data:** Barretina et al. 2012: 947 lines, 24 drugs on about 479–500 lines, more than 50k features (expression, CN, mutations). Response: activity area. p ≈ 5·10⁴.
- **Licence:** The DepMap forum says "Generally… CC BY 4.0"; check each file.
- **Correlation:** Strong factor-like modules (lineage).
- **Validation:** Published markers: NQO1 for 17-AAG (as summarised in secondary sources; check the paper). Cross-lab replication in GDSC (its licence is **not verified**: cancerrxgene.org returned HTTP 410 to my fetch).
- **Compute:** About 35 core-h per drug-fit at n ≈ 480. 17-AAG × 3 seeds is about 0.1k.
- **Risks:** Lineage confounding, mixed feature types, CCLE/GDSC response discordance.

### 7. Rat eye TRIM32 (Scheetz et al., PNAS 2006) (rank 7, literature benchmark)
- **Data:** n = 120 F2 rats, p = 18,975 probes (after the 18,976 filter), in GEO GSE5680 (GEO terms). Common subsets have 3k/5k probes; R packages flare and hdrm hold processed versions.
- **Correlation:** F2 linkage plus co-expression (factor-like).
- **Validation:** Weak: comparison with the literature and held-out MSE only.
- **Compute:** At most about 5 core-h per fit.
- **Risks:** n is small; there is no external truth.

**Considered, not shortlisted:**
- NIR spectroscopy and microbiome: p ≲ 10³ after aggregation.
- Text (E2006 10-K tf-idf): n ≫ 200, and the signal is not sparse.
- BXD/GeneNetwork: no data licence stated on genenetwork.org.
- HS rats/mice: data access not checked.
- UK Biobank, dbGaP, GTEx genotypes: controlled access.

**Honest assessment.** The list is moderately exciting, not dull.
- **Arabidopsis 1 → 2 is genuinely good.** It is open data, the native n ≈ 200, p up to 10⁶ (if the 1001G overlap holds), known loci, and a replication set. No other open dataset I found matches our operating point this well.
- **Yeast gives us something close to a recovery score**, but at p ≈ 10⁴ only.
- **The human cases are mostly comparisons** with SuSiE and the clocks, not wins for an exact-posterior method.
- **The weak spot everywhere is the model.** Real structure (kinship, cell mix, lineage) is factor-like, which our theorems do not cover. Our answers will be honest posteriors under a misspecified iid-error model, so the confounding handling must be declared up front.
- **Links not verified are flagged above.** Check them before anyone downloads anything.
