# BENCH_DESIGN checker brief (Haiku)

You are a fact-checker. You have a batch of paper keys. For EACH paper you re-open the original source and check whether our write-up matches it.

## What to check

1. **`/home/fb31/SMC_Theory_Department/BENCH_DESIGN/out/PAPERS.md`.** Find the section `### <key>`. Check these fields against the paper:
   - `DOI` / arXiv id: does it resolve to *this* paper (title, authors, year, journal volume/pages)?
   - `X` design: distribution, correlation structure, parameters (ρ, block size, ...)
   - `n` (all values; largest)
   - `p (max)` and the p grid
   - `s0`
   - `β / SNR`: coefficient values, placement, signs, SNR/PVE/σ convention
   - `Metrics`
2. **`/home/fb31/SMC_Theory_Department/BENCH_DESIGN/out/REPORT.md`.** Find every statement that names this paper (search by first-author surname, e.g. `grep -n "Hazimeh" REPORT.md`). Check each of them: tables in §1–§6, dataset n and p in §3, and counts that list the paper. Also check that the paper's row in the §8 Sources table has the correct citation and DOI.

## Where the sources are

- **Local PDFs:** `/home/fb31/SMC_Theory_Department/BENCH_DESIGN/papers/`. Filenames are close to the key, sometimes with a `BVS_` prefix. Examples: `BVS_SuSiE2020.pdf` = Wang2020; `JMLR21_19-536.pdf` = Johndrow2020; `MrASH_arxiv.pdf` = Kim2024; `Friedman2010glmnet.pdf`; `JavanmardMontanari2014.pdf`; `MeinshausenMeierBuhlmann2009.pdf` = Meinshausen2009; `WangLeng2016.pdf` = Wang2016; `WassermanRoeder2009.pdf` = Wasserman2009; `BVS_Carbonetto2012.pdf` = Carbonetto2012; `BVS_Rockova2014thesis.pdf` = Rockova2014 (thesis version).
- **Other local copies:**
  - Clyde2011: `/home/fb31/Papers_local/Papers/Core_bibliography/27_2011_Clyde_Ghosh_Littman_Bayesian_Adaptive_Sampling_for_Variable_Selection_and_Model_Averaging.pdf`
  - Rockova2018: `/home/fb31/Papers_local/Papers/Benchmark_methods/Rockova_George_2018_SSL.pdf`
  - SongLiang2015: `/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015.pdf` (+ `_supplement.pdf`)
- **No local file:** use the `open_url` column of the key's row in `/home/fb31/SMC_Theory_Department/BENCH_DESIGN/scout/S*.tsv` (`grep -h "^<key>	" scout/*.tsv`). Otherwise use arXiv, PMC, or `https://doi.org/<doi>`. For DOI metadata use `https://api.crossref.org/works/<doi>`.
- **Reading PDFs:** extract text with `pdftotext -layout <pdf> <your scratch dir>/<key>.txt`, then grep and read the simulation and real-data sections.

## Rules

- Never copy PDFs anywhere. Never write into any git repository. Do not edit PAPERS.md or REPORT.md; you only report.
- **MISMATCH:** the source clearly contradicts our text. This includes a wrong number, wrong ρ, wrong s0, wrong DOI, or a value we attribute to the wrong setting.
- **UNVERIFIABLE:** you cannot find it in the source, or the source is unreachable.
- **OK:** it matches. Rounding and paraphrase are fine, and so is "≈".
- Be concrete. Quote the source's wording or number, and give the page, section, table or figure.
- Spend your effort on numbers (n, p, s0, ρ, β, SNR, DOI). Do not nitpick wording.

## Output

Write a TSV to `/home/fb31/SMC_Theory_Department/BENCH_DESIGN/check/C<batch>.tsv`. It has the header

`key	where	item	ours	source	verdict	location`

- `where`: PAPERS or REPORT§n
- `item`: doi | X | n | p | s0 | beta | metrics | other
- `verdict`: OK | MISMATCH | UNVERIFIABLE
- Use one row per checked item. Every paper gets at least the 7 PAPERS items: doi, X, n, p, s0, beta, metrics.
- Use `;` inside fields, never tabs or newlines.

Final reply, at most 10 lines: papers checked, OK/MISMATCH/UNVERIFIABLE counts, and each MISMATCH in one line.
