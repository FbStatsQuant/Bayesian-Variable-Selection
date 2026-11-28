# CITE_CHECK brief (Haiku checkers)

The owner fixed our simulation suite to S1–S3. Every paper we cite for a design must ACTUALLY contain that design, or one close to it. Your job is to verify each claimed spec against the paper's full text. Do NOT use abstracts, our notes, PAPERS.md or REPORT.md as evidence: only the paper text counts.

## Sources

**Local copies** (in `/home/fb31/SMC_Theory_Department/BENCH_DESIGN/papers/` unless a full path is given):

| Paper | Local copy | Version |
|---|---|---|
| YWJ 2016 | `BVS_Yang2016.pdf` | arXiv 1505.07925v1 |
| Griffin et al. 2021 | `BVS_Griffin2021.pdf` | arXiv 1708.05678v3 |
| Hastie et al. 2020 | `Hastie2020.pdf` | arXiv 1707.08692v2, 53 pp |
| Dezeure et al. 2015 | `Dezeure2015.pdf` | journal (Stat Sci) |
| George & McCulloch 1993 | `/home/fb31/SMC_Theory_Department/BENCH_DESIGN_papers/George_McCulloch_1993_SSVS_JASA.pdf` | journal |
| Liang et al. 2022 | `BVS_Liang2022.pdf` | arXiv v3 |
| Zanella & Roberts 2019 | `BVS_Zanella2019.pdf` | — |
| Shin et al. 2018 | `BVS_Shin2018.pdf` | arXiv v4 |

**Reading:** extract text with `pdftotext -layout <pdf> <your scratch dir>/<name>.txt`. If formulas are garbled, read the PDF pages directly with your Read tool (`pages` parameter).

**Journal versions.** Where the local copy is an arXiv version, also try to open the journal version online:
- Project Euclid hosts Ann. Statist. and Stat. Sci.; try `https://doi.org/<doi>` and the PDF link on that page.
- Also check whether a later arXiv version exists, at `https://arxiv.org/abs/<id>`.
- If the journal version is not reachable, say so, and verify against the newest arXiv version you can open.
- **Always record which version each quote comes from.**

## For each claimed spec item

Record these fields:
- **location:** page number (the PDF page, plus the printed page if different) and section, example, table or figure;
- **quote:** a VERBATIM quote of the sentence or formula defining the design. Keep it short, but include the numbers. Write math as it appears, e.g. `beta* = SNR sqrt(sigma^2 log p / n) (2,-3,2,2,-3,3,-2,3,-2,3,0,...,0)`;
- **verdict:**
  - EXACT: the paper states this spec.
  - SIMILAR: close, but different. State the difference precisely, e.g. "paper's Σ is e^{-|j-k|}, not 0.6^{|j-k|}" or "paper's grid is n∈{300,900}".
  - NOT FOUND: you searched the whole text and it is not there.

Rules:
- Check each sub-item separately (β vector, scaling, SNR grid, Σ, n, p, s, ...). Do not give one verdict for the whole paper.
- Be skeptical. If the text and a table disagree, report both, with their locations.
- Never copy PDFs. Never write into any git repository. Do not edit any existing file.

## Output

Write a TSV to `/home/fb31/SMC_Theory_Department/BENCH_DESIGN/check/<your output name>.tsv` with the header

`paper	claim_item	claimed	verdict	version	location	quote	difference`

- `version`: e.g. "arXiv v1" or "journal".
- Use `;` inside fields, never tabs or newlines.

Final reply, at most 10 lines: one line per claim item with its verdict, and for SIMILAR the difference.
