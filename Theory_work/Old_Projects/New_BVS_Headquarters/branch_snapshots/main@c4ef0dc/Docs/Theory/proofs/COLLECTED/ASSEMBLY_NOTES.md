# ASSEMBLY_NOTES.md: COLLECTED_PROOFS_v1 (2026-10-22)

Assembly work only. No statement or proof was changed, fixed, shortened or paraphrased. FAILED_ATTEMPTS.md of Theory_architecture_v3 was read first; none of its entries concerns this assembly (they concern the council runs of the theory-architecture phase).

## 1. Deliverables and how to rebuild

| item | path (all under `Theory_architecture_v3\proofs\COLLECTED\`) |
|---|---|
| document | `COLLECTED_PROOFS_v1.tex`, `COLLECTED_PROOFS_v1.pdf` (copy of `build\COLLECTED_PROOFS_v1.pdf`) |
| build files | `build\` (latexmk output, logs, `chapters\` = the ten proof bodies as inserted, `helpers\` = three files read by the T12 proof at compile time, `tools\` = the scripts, `*_report.txt/json` = check outputs, `src_lualatex\` = copies of the ten source proofs recompiled for the comparison) |
| SHA-256 of `COLLECTED_PROOFS_v1.tex` | `b1cde0ea1d038f1e0cbcc7628a41d5c4da3dd5aed5be2e84e5d828168a512b96` |
| SHA-256 of `COLLECTED_PROOFS_v1.pdf` | `18a44fe97be9d4ac63d713055d63cddd2d9e3da327a8d49de7068e43dbd944fc` |

Rebuild: `python -I build\tools\assemble.py` (writes the .tex from the inputs), then from `COLLECTED\`:
`latexmk -lualatex -interaction=nonstopmode -file-line-error -outdir=build COLLECTED_PROOFS_v1.tex`, then copy `build\COLLECTED_PROOFS_v1.pdf` up one level. Checks: `python -I build\tools\verify.py`, `bodycheck.py`, `tables.py`. The document uses the Windows fonts Cambria and Consolas for the converted Markdown parts (the proofs themselves are in the standard TeX fonts).

## 2. Build result

| item | result |
|---|---|
| engine | lualatex through latexmk (3 runs, exit code 0), TinyTeX (LuaHBTeX 1.24.0). lualatex is needed because the T13 proof uses fontspec; the other nine proofs were originally pdflatex documents and compile unchanged |
| pages | 157 (Letter; the overview table is on three landscape pages) |
| LaTeX errors | 0 (no line starting with `!`, no file:line:error message in `build\COLLECTED_PROOFS_v1.log`) |
| undefined references / citations | 0 (no "undefined" in the log; no `??` in the PDF text; all 230 `\label`, `\ref` and `\eqref` uses in the proofs resolve) |
| missing glyphs | 0 ("Missing character" absent) |
| warnings left | 47 overfull boxes (mostly inside the proofs, they are in the unchanged source text; the largest ones are long displayed formulas), 9 hyperref "token not allowed in PDF string" (math in section titles of the proofs; bookmarks only), 0 underfull |

## 3. Confirmation of the final proof versions (no mismatch)

For each folder the highest `PROOF_v<k>.tex` was compared with the version FINAL_REPORT.md names as final. All ten agree: T09 v3, T11 v5, T12 v5, T13 v4, T14 v3, T15 v4, T20 v3, T22 v3, T23 v4, T31 v3. Further consistency checks: the SHA-256 printed in the FINAL_REPORT of T09 (`.tex` bab55fdf...76ba6, `.pdf` f0d45334...12234) and of T14 (`.tex` c12954d1...97efdd4, STATEMENT 7e94d7e3...f36ffd) equal the hashes of the files used. The T13 FINAL_REPORT says its PDF was compiled with xelatex; the proof text compiles unchanged with lualatex.

## 4. Structure of the document

Title, status line, table of contents; Overview (table with the seven requested columns, written from FINAL_REPORT.md and STATEMENT.md); Dependencies; Shared definitions (00_COMMON.md); ten chapters (T09, T11(iii), T12, T13, T14(i), T15, T20(i)-(ii), T22(i)(ii)(iv), T23(ii), T31(i)), each with (a) theorem-file text, (b) STATEMENT.md, (c) final proof, (d) review record = the statement-change section and the review-history section of FINAL_REPORT.md plus the whole CLAIMS_OF_FATAL_FLAWS.md. The FINAL_REPORT sections taken (selected by heading) are listed in `build\assembly_manifest.json` (`fr_sections`); they are "Statement changes" and "Review history" under their per-report titles (T09 "2. Statement changes" and "4. Review history"; T13 "2. Changes to the statement, and why" and "4. Review history and my judgments"; and so on). The T22 review-history section includes its sub-sections as they stand under that heading (Stage A, Stage B, numerical sanity check).

## 5. Mechanical edits to the proofs and macro handling

Part (c) of each chapter is the body of `PROOF_v<k>.tex` between `\begin{document}` and `\end{document}`, without the title block (`\maketitle`; `\title`, `\author`, `\date` are in the preamble and are not copied). The preamble lines that define theorem environments, macros, `\lstset` and the fonts are copied into the chapter, inside a LaTeX group, so every macro is local to its chapter. **No macro had to be renamed**: macros defined differently in two proofs never meet, because each definition lives only inside its own chapter's group. The `\usepackage` lines were merged into one preamble (union below).

Edits actually made, all mechanical and verified by undoing them (`bodycheck.py`: after undoing the edits the chapter body and the chapter preamble are character-for-character equal to the source, for all ten proofs):

1. Theorem environments carry a chapter prefix (for example `lemma` becomes `T09lemma`): in the `\newtheorem` lines (name and shared-counter name; the displayed name such as "Lemma" is unchanged) and in every `\begin{...}`/`\end{...}` of those environments. Reason: `\newtheorem` counters are global, and the proofs share a counter in different ways (for example T09 shares one counter across theorem/lemma/proposition/remark, T12 numbers lemmas within sections, T15 and T22 use separate counters). The numbering seen in each chapter is therefore the numbering of the original proof (the proof text refers to "Lemma 3.1" and so on).
2. `\label{x}`, `\ref{x}`, `\eqref{x}` become `\label{T09:x}` etc. (chapter id as prefix). No `\pageref`, `\autoref`, `\cite` occurs in the proofs.
3. Local numbering as in the source: inside each chapter's proof group `\thesection` is `\arabic{section}` (so sections are numbered 1, 2, ... as in the source, not 5.1), `\theequation` is `\arabic{equation}`, and `\appendix` (used by T12 and T13) is the article-class version (A, B, ...). The report class's chapter numbering is not used for the proofs.
4. T12 only: the appendix lists three helper files with `\lstinputlisting{../helpers/p2_exact.py}`, `certify_instance.py` and `certify_iv.log`. The three files were copied unchanged to `build\helpers\` (SHA-256 below) and the three paths were rewritten to `build/helpers/...` so that the document compiles from `COLLECTED\`. These three files are inputs of the T12 proof that were not in the contract's input list; they were only read.
5. The `\maketitle` line was removed (one per proof).

Not copied: `\documentclass` (article, 11pt, in all ten) and `\usepackage` lines (merged), and `\title/\author/\date`.

### Macros defined in more than one proof preamble (from `build\clash.txt`)

| macro | definitions | action |
|---|---|---|
| `\E` | T12 and T14 `\mathbb{E}`; T13 `\mathcal{E}_{\mathrm{grid}}` | different; local to chapters, no rename needed |
| `\Pc` | T15 `\mathbb{P}_{\mathcal C}`; T23 `P_{\C}`; T31 `\mathbb{P}_c` | different; local |
| `\Ec` | T15 `\mathbb{E}_{\mathcal C}`; T23 `E_{\C}`; T31 `\mathbb{E}_c` | different; local |
| `\PIP` | T12 `\mathrm{PIP}`; T23 `\widehat{\mathrm{PIP}}` | different; local |
| `\R` | T12 `\mathbb{R}`; T23 `\mathcal R` | different; local |
| `\Om`, `\Zb`, `\Zh`, `\cC`, `\cF`, `\qh` | identical definitions in each proof that defines them | local; nothing to do |

Macro renames: **none**. (T12 uses `\renewcommand{\P}`; it is applied inside T12's group only.)

### Package union

amsmath, amssymb, amsthm, enumitem, geometry (margin 1in; T12 and T20 had 2.5cm, so their line breaks differ slightly from their stand-alone PDFs), fancyvrb and fontspec (T13), listings (T12, T13), hyperref and xcolor (T12); added for this document: report class, longtable, array, hyperref options, and fontspec fonts Cambria/Consolas for the converted Markdown. The T13 font command `\newfontfamily\qfont{Cambria Math}` is copied as it is.

## 6. Markdown to LaTeX conversion (parts a, b, d, shared definitions)

The sources use Unicode for mathematics (no `$...$` anywhere), so mathematics is copied as Unicode text and typeset with Cambria (fallback Cambria Math). Rules of the converter (`build\tools\md2tex.py`):

- Headings, bold, lists (numbers of numbered items kept), block quotes, horizontal rules and one fenced code block (T20 STATEMENT, typeset in a `Verbatim` block) are translated; LaTeX special characters are escaped. A single newline inside a paragraph is a space; a continuation line that starts with two or more spaces (the display lines of the theorem files, for example `  E_C f_r <= ...`) is kept as a separate line. Inline code uses a monospace font.
- `*` and `_` are literal unless a `*...*` / `**...**` pair opens at a word start and closes before space or punctuation (the sources use `S*`, `e_phi`, `θ*_j` as mathematics). All 33 emphasis spans found are listed in `build\assembly_manifest.json` (`emph`) and are real emphasis; no opener-like `*` is left (`star_audit.py`).
- Tables become `longtable`s. Seven table rows contain a stray `|` that is part of the text (for example `|T|`, `|U_b*|` in 00_COMMON.md rows SE, COH, AGG, ONE, LK_d, WS, and one row of the T31 CLAIMS table, "Table entries with |A| > K"). The extra cells were merged back into the second column with the pipe restored (the surplus cells always lay in the second column); this is recorded as `table row with n surplus pipe(s) merged` in `assembly_manifest.json` (`md_notes`).
- Five CLAIMS files (T11, T12, T13, T14, T20) contain raw LaTeX math between backslash-paren and backslash-bracket delimiters; it is typeset as math. Two of these segments (T11 CLAIMS, items "Location: Section 2 ... Lemma \ref{lem:sampler}" and "Section 3, Remark \ref{rem:full}") contain `\ref` to the reviewer's own labels; they are printed literally (`\ref{lem:sampler}`) instead of being resolved.
- Plain backslashes in the Markdown (for example `N(j) \ S`, Windows paths) are printed as backslashes.
- Nothing needed a verbatim fallback except the real code fence above.
- Hard line breaks by trailing double space: none occur.

## 7. Acceptance checks

Method (`build\tools\verify.py`, output `build\verify_report.txt`, `verify_results.json`): the PDF text of each chapter is extracted with pdftotext (MiKTeX) and compared with the source proof's compiled text.

- Proofs: part (c) of each chapter is compared word by word, in order (difflib), with (i) the source `PROOF_v<k>.tex` recompiled with lualatex in its own folder copy (`build\src_lualatex\`), (ii) the PDF that is in the proof folder (pdflatex; xelatex for T13). Text is taken in content-stream order (`pdftotext -raw`), because the default layout order of pdftotext reorders sub/superscripts and sums depending on where a line breaks, which differs between the stand-alone page (title block, 2.5cm margins for T12/T20) and the chapter. Normalisation: NFKC, ligatures, whitespace, all hyphens and minus signs and line-end hyphenation removed, page-number footers dropped, title block removed. "Match" is the share of the source words matched in order.
- Markdown parts: every non-empty source line (every table cell separately, text around raw-LaTeX math separately) is looked up, with whitespace removed, in the extracted text of the matching part of the chapter. Mathematics spans in the CLAIMS files are checked by the surrounding text only.

### Results

### Proof text match
| chapter | source words compared | match vs source recompiled with lualatex (raw order) | match vs source PDF in its folder (raw order) | match, default layout order (lualatex) |
|---|---|---|---|---|
| T09 (PROOF_v3) | 4662 | 100.00% (0 unmatched) | 100.00% (0 unmatched) | 98.58% |
| T11 (PROOF_v5) | 2688 | 100.00% (0 unmatched) | 99.70% (8 unmatched) | 99.72% |
| T12 (PROOF_v5) | 8537 | 99.66% (29 unmatched) | 99.25% (64 unmatched) | 97.64% |
| T13 (PROOF_v4) | 6274 | 100.00% (0 unmatched) | 98.30% (107 unmatched) | 99.71% |
| T14 (PROOF_v3) | 1762 | 100.00% (0 unmatched) | 100.00% (0 unmatched) | 98.72% |
| T15 (PROOF_v4) | 1823 | 99.95% (1 unmatched) | 99.95% (1 unmatched) | 99.65% |
| T20 (PROOF_v3) | 3178 | 99.65% (11 unmatched) | 98.28% (55 unmatched) | 99.44% |
| T22 (PROOF_v3) | 3063 | 100.00% (0 unmatched) | 100.00% (0 unmatched) | 97.89% |
| T23 (PROOF_v4) | 3219 | 100.00% (0 unmatched) | 100.00% (0 unmatched) | 98.80% |
| T31 (PROOF_v3) | 2948 | 100.00% (0 unmatched) | 99.93% (2 unmatched) | 98.33% |

### Presence of every STATEMENT.md and CLAIMS_OF_FATAL_FLAWS.md entry
| chapter | STATEMENT.md: non-empty lines / headings / list items / units found | CLAIMS: non-empty lines / headings / table data rows / list items / units found |
|---|---|---|
| T09 | 29 / 3 / 4 / 29 of 29 | 21 / 3 / 0 / 4 / 17 of 17 |
| T11 | 62 / 5 / 14 / 62 of 62 | 138 / 12 / 0 / 14 / 126 of 126 |
| T12 | 65 / 7 / 39 / 65 of 65 | 49 / 6 / 0 / 13 / 49 of 49 |
| T13 | 42 / 4 / 21 / 42 of 42 | 57 / 14 / 0 / 15 / 59 of 59 |
| T14 | 31 / 5 / 18 / 31 of 31 | 19 / 6 / 0 / 0 / 23 of 23 |
| T15 | 40 / 6 / 18 / 40 of 40 | 25 / 3 / 10 / 8 / 67 of 67 |
| T20 | 68 / 8 / 28 / 65 of 65 | 55 / 6 / 0 / 14 / 51 of 51 |
| T22 | 47 / 4 / 29 / 47 of 47 | 11 / 4 / 0 / 2 / 11 of 11 |
| T23 | 38 / 6 / 22 / 38 of 38 | 20 / 6 / 0 / 8 / 20 of 20 |
| T31 | 78 / 6 / 15 / 78 of 78 | 35 / 5 / 17 / 0 / 87 of 87 |

### Other Markdown parts (units present / checked)
| chapter | theorem file | FINAL_REPORT statement changes | FINAL_REPORT review history |
|---|---|---|---|
| T09 | 20 / 20 | 6 / 6 | 46 / 46 |
| T11 | 22 / 22 | 8 / 8 | 47 / 47 |
| T12 | 19 / 19 | 9 / 9 | 41 / 41 |
| T13 | 20 / 20 | 12 / 12 | 53 / 53 |
| T14 | 20 / 20 | 4 / 4 | 40 / 40 |
| T15 | 17 / 17 | 9 / 9 | 50 / 50 |
| T20 | 19 / 19 | 17 / 17 | 19 / 19 |
| T22 | 19 / 19 | 14 / 14 | 23 / 23 |
| T23 | 19 / 19 | 11 / 11 | 27 / 27 |
| T31 | 21 / 21 | 7 / 7 | 46 / 46 |
| 00_COMMON | (see below) | | |

### Mechanical edits on the proofs (verified by undoing them)
| chapter | body identical after undo | preamble identical after undo | labels/refs prefixed | theorem-env begin/end renamed | theorem environments renamed | helper paths |
|---|---|---|---|---|---|---|
| T09 | True | True | 37 | 30 | theorem, lemma, proposition, remark | 0 |
| T11 | True | True | 15 | 18 | theorem, lemma, proposition, corollary, remark | 0 |
| T12 | True | True | 40 | 16 | theorem, lemma, corollary, remark | 3 |
| T13 | True | True | 18 | 10 | lemma, proposition, remark | 0 |
| T14 | True | True | 17 | 12 | theorem, lemma, proposition, remark | 0 |
| T15 | True | True | 11 | 8 | theorem, lemma, remark | 0 |
| T20 | True | True | 20 | 10 | lemma, corollary, remark | 0 |
| T22 | True | True | 23 | 32 | lemma, proposition, remark | 0 |
| T23 | True | True | 23 | 16 | theorem, lemma, remark | 0 |
| T31 | True | True | 26 | 26 | theorem, lemma, corollary, remark | 0 |

### SHA-256 of every input file used
26e9f2a6949fea993bc92e0c86f48ff98f946e4441a5fded44009a64df50713a  proofs\PROOFS_STATUS.md
9acbbe1f693d84644ae5bd8d05081fa74878216772baeb798cd1f738f3133fe9  proofs\T09_T7_kernel_validity\CLAIMS_OF_FATAL_FLAWS.md
dabfe946286e696543938018ab682cdac44389a77ce4ce13d624a34ca97d95c6  proofs\T09_T7_kernel_validity\FINAL_REPORT.md
bab55fdf1074bdb509f4409fc08d9b5ed342072da620a2df122bdc8d03276ba6  proofs\T09_T7_kernel_validity\proof\PROOF_v3.tex
da944993732a955086ffe9aaaceb725ff23ff63fa50e923b2881b39a72fcdc75  proofs\T09_T7_kernel_validity\STATEMENT.md
a339a99f410fe9b2a9d61646b20dae1efb7a4c4c6e7f1d29451d56f26935b03a  proofs\T11_LLED_scoring_ledger\CLAIMS_OF_FATAL_FLAWS.md
bc591c2653a8e458f88e8dc8b4d1ff421ed1fa966f4c0dc2c36d047327c3ffcc  proofs\T11_LLED_scoring_ledger\FINAL_REPORT.md
7f4e94c47415f2e4bb64c59038a4193bfbc4fcf71a774fd8c429a74184886260  proofs\T11_LLED_scoring_ledger\proof\PROOF_v5.tex
e18cefd79fe1e452a60c7433a1ef43ef4fd5ee328e731a4172530a9448fd42de  proofs\T11_LLED_scoring_ledger\STATEMENT.md
b2430928865ed787d503a108cd4f146fafd3700b3cfcf1d0ac0b2f228263bc76  proofs\T12_T8_frozen_run_identities\CLAIMS_OF_FATAL_FLAWS.md
a0ce9dbe457f1da084e764cf0331f938a751be5265fb12644874f028e0118797  proofs\T12_T8_frozen_run_identities\FINAL_REPORT.md
17620483869f12fda7c87eb88af30e833d32e47f4058aafaabc7cdfe5aaab263  proofs\T12_T8_frozen_run_identities\helpers\certify_instance.py
52a1fb021e38bcbf6b9428eda00a0fa06ca2e2698be528c5d3de747900539370  proofs\T12_T8_frozen_run_identities\helpers\certify_iv.log
d6e790fcd4e6f2b7871c95fbdf26460aef6dec907a57a223386026d9f0594208  proofs\T12_T8_frozen_run_identities\helpers\p2_exact.py
062e5d2b2c04cb1ea281b597a3dcc77da3d9988d134dab71c528d1fb00bb1236  proofs\T12_T8_frozen_run_identities\proof\PROOF_v5.tex
da90d5b0f6fb192c597b7946d7638d5da0b79ae951bb798d3f91574c46f2a30e  proofs\T12_T8_frozen_run_identities\STATEMENT.md
8b70da8f5cb43dfa96be38014eb1ee5cabacd31a2c11e17de0504632f415ea58  proofs\T13_T10_restricted_ESS\CLAIMS_OF_FATAL_FLAWS.md
2ce6584c0f16cadaab6a62986845e2f7537508ddc35d1026f4abdad4d8e03928  proofs\T13_T10_restricted_ESS\FINAL_REPORT.md
4049019c683731dd56e83c640696bd48fc41335df6bbbbf35c0fed019aa60f2d  proofs\T13_T10_restricted_ESS\proof\PROOF_v4.tex
fb7fde4bac4cace63ecaf380e67c3b44f58c1ab6d79c8421dfc2531723c13b04  proofs\T13_T10_restricted_ESS\STATEMENT.md
6cabd9337b3dac2cfea171f7d176ed9b69bdeea79365b024dd20470278cb7935  proofs\T14_LFM_first_moment_evidence\CLAIMS_OF_FATAL_FLAWS.md
32411d47f9e612d2202d06a979d93e55a879e770cfae93019c0aba0099b58a66  proofs\T14_LFM_first_moment_evidence\FINAL_REPORT.md
c12954d17b7f7383b026b13925c4558e917af95c14e40b844529f490397efdd4  proofs\T14_LFM_first_moment_evidence\proof\PROOF_v3.tex
7e94d7e38de93534d5a65fe31521c18e6d1824fc6d02ba116feedfc771f36ffd  proofs\T14_LFM_first_moment_evidence\STATEMENT.md
60bc1beabe15c19c9b38ad4da997da37073afa78bcb5abd0ad8679a6ff00f832  proofs\T15_LOCC_occupancy\CLAIMS_OF_FATAL_FLAWS.md
eddb3e14cb3ee3e80608122d522e356fcdb7a6f88f794b2b271d5c08634640f5  proofs\T15_LOCC_occupancy\FINAL_REPORT.md
246f07076f0d71fd0f08f9191ae20e999b4370efe75cdfdf7c3e33837ead8b68  proofs\T15_LOCC_occupancy\proof\PROOF_v4.tex
2c6caceb670a0a7aa0a40d396e62a7fc26a45ce43313b7efdd1556a42cf1c056  proofs\T15_LOCC_occupancy\STATEMENT.md
0469e7869b6acaad3d5ad238936dd7f6ee59326aa32b85ce05cd0e80bca4bd50  proofs\T20_T15_local_search\CLAIMS_OF_FATAL_FLAWS.md
e5aaf2ccd9a01cfdb50c6d5d65759cbb2c0dc46d6dbf8836054242584280f9c7  proofs\T20_T15_local_search\FINAL_REPORT.md
2e34a79120c1e92f6738acd97dbd54fb8051fbc47e38931a48d09667d2332b24  proofs\T20_T15_local_search\proof\PROOF_v3.tex
d3507eb4b44d02f57b283f60cc99ca2ff56790f1f70915bde246cd5078d6ffd4  proofs\T20_T15_local_search\STATEMENT.md
8687f5436e75e3113dfa21fd2a26026ca1b2dd802fc08e35d7a584690713f39f  proofs\T22_T16_start_aggregation\CLAIMS_OF_FATAL_FLAWS.md
8e57302a5c7e15e0741f4f7804543946b2a23561b8bae994d682510e79c036cc  proofs\T22_T16_start_aggregation\FINAL_REPORT.md
08c3521c5ad28bc7d2be26f5093b191fcb0596d95eae811b850ed26922f95be1  proofs\T22_T16_start_aggregation\proof\PROOF_v3.tex
4897c22a8bf5e913ec85493236602c79f9b4d6235888cd3cdba2f9e212802eef  proofs\T22_T16_start_aggregation\STATEMENT.md
83f31563ed2b5c887768ba858c459c90070a45bbce3961b7d822d0d26aaf4edb  proofs\T23_T18_basin_prefix\CLAIMS_OF_FATAL_FLAWS.md
3629258a7172da727f6be13980dd62109945329e8cb4af841d20670b312dfb19  proofs\T23_T18_basin_prefix\FINAL_REPORT.md
6be37b070896b872a09d08b232c46adac05815aa1adc75c85d230cc84bf7f80a  proofs\T23_T18_basin_prefix\proof\PROOF_v4.tex
62e7bd8c887cc80949c565474e72a5d8888dc8767217863d334ad0d9f85a7490  proofs\T23_T18_basin_prefix\STATEMENT.md
0803a1a0fd6241a8275b2db9cf399caf250d900e6ea21bc062ea0b7b146ff90c  proofs\T31_T22_certificates\CLAIMS_OF_FATAL_FLAWS.md
d1bfd0ede103452c65401d988f51316a5fb26d4a9c8f858581bd886b58a2a273  proofs\T31_T22_certificates\FINAL_REPORT.md
e140d9b81cd01b54b1b052011975d5d56a2db13dc64095d4fe7a658126e2d4cc  proofs\T31_T22_certificates\proof\PROOF_v3.tex
0ad37b7370555f9385435c77399335bc2f3152c7ade420855c7cfc7703e0649d  proofs\T31_T22_certificates\STATEMENT.md
a7d05134350823efd62add9d66a8ec1e8ff78185f2efc78415a504cc819e023d  theorems\00_COMMON.md
e5c9bf35170e4bb341c87259cc0a0e0535490cefbbdc2c4bc7bc3e52fe537062  theorems\T09_T7_kernel_validity.md
f7718e9332b5072439d06fd78cd2de31e51bb68dc0b7810f63e25081a49d8adf  theorems\T11_LLED_scoring_ledger.md
f8ecb0a3ffbd02ad77589cb4e3f1a4c7884589e2c84036a01979bc323058c63a  theorems\T12_T8_frozen_run_identities.md
fca5fffd886540e9eb16ebdc070ee98374a298bd92686d20858eb131772ee97c  theorems\T13_T10_restricted_ESS.md
6484b29e2870b1620e92ef108c5779fca87ef921a42b471edf02966b6339bbb2  theorems\T14_LFM_first_moment_evidence.md
04e0c764970b835da07f4d3143d86d5dca7ec70832c12b93c5a6fdacd72edac0  theorems\T15_LOCC_occupancy.md
511e08bf50f3a072112c6f090420fc3255454249886aa02f13c5cf5ab0d86d05  theorems\T20_T15_local_search.md
0125dcb79cfd760876ee286ee8ae265b0eee19fc7643a7ea8e1988c44c6a4541  theorems\T22_T16_start_aggregation.md
d1c6696238c7d53c70722d48f006cb0514862cffc1da6a305ebd0baebeacf709  theorems\T23_T18_basin_prefix.md
5c0f889768bec362c6bcd1353b0d1e0b6568af4226609e522d46a74889eb984d  theorems\T31_T22_certificates.md

SHA-256 of the three T12 helper files, copied unchanged to `build\helpers\`, are in the list above (certify_instance.py, certify_iv.log, p2_exact.py). SHA-256 of the ten PDFs that were used as the "own compiled text" of the source proofs (read only):

```
f0d45334bf3210bdaca82b95260fb651096f18fd4f8033c2ebef302f47f12234  T09_T7_kernel_validity\proof\PROOF_v3.pdf
6fee2a4b7a688ac4ac5cecf5836b6458ccf2cecfaeba0e32792ef581b38ee67a  T11_LLED_scoring_ledger\proof\PROOF_v5.pdf
d79db3c687cda2b20f81dfce8feae262cf174bd1a5db1623baeeea4530cfca57  T12_T8_frozen_run_identities\proof\PROOF_v5.pdf
b240ba4daeca2612b421cac26f72955328d9c1b222f7c382c8aacd6bf25ec815  T13_T10_restricted_ESS\proof\PROOF_v4.pdf
a1669fcd81dccd821d8fae2adb4c006cf4d91c0937f831f44155268c42b8dc11  T14_LFM_first_moment_evidence\proof\PROOF_v3.pdf
989c0abee0ce080a29c96f275e44c2fcd13e002f516e4c3caeb587ad9aa2bd4c  T15_LOCC_occupancy\proof\PROOF_v4.pdf
dd79fd38303e1db4aa0f7976e56bbd4b449d07e4aa4fbb4315eb40112ab2bd7e  T20_T15_local_search\proof\PROOF_v3.pdf
c958ddcfa5b6068bc4418d911bbc4a0fbcdf29a0af2746198f4eaf8b292c1fd0  T22_T16_start_aggregation\proof\PROOF_v3.pdf
98277b42359f4ded290fc937828eabc74efde3b74e1ac6ab8cdac0985d73f6b8  T23_T18_basin_prefix\proof\PROOF_v4.pdf
a2390c3a5a7251bf32e4465533861d2162c991136829131665187864e7fa3cdc  T31_T22_certificates\proof\PROOF_v3.pdf
```

### Explanation of every difference in the proof comparison

The match is at least 98% for every proof against both references in content-stream order (lowest: 98.28% for T20 and 98.30% for T13 against the PDFs in the proof folders; against the same-engine recompile the lowest is 99.65%). The differences are:

- **Page numbers.** Footers are dropped before the comparison. Earlier runs without that step differed only by the page numbers of the source (1, 2, ..., one per source page).
- **Text-extraction artefacts of mathematics, not content.** T12: 29 words against the lualatex recompile (64 against its PDF); they are groups with `{j}` braces where pdftotext inserts or omits a blank (`∪ {j}` versus `∪{j}`, `γ(S)|A′| }`) and three formula fragments near the end of the proof (`PIP1] ZPIP1)/Z0.`, `F] Z)/Z0`) where a subscript is spaced differently. T15: 1 word (`EV/s.`). T20: 11 words (`k+1`, `k + 1`, `n λn)+,`). All of these are the same characters with different spacing in the extracted text.
- **Engine differences against the PDFs in the proof folders** (the same source recompiled with lualatex matches in all these cases). T20: 55 words, all `local_certified` / `local_limit` (the text layer of the pdflatex PDF drops the underscore of `\texttt{local\_certified}`). T11: 8 words in a table of status names (`resource limit`, `schedule limit`, `numerical failure`, `FINAL ISLAND(grid,`; same underscore effect, `resource_limit`). T31: 2 words ("a log"). T13: 107 words of the xelatex-compiled PDF: math control glyphs (`\x01`, `\x10`, `P`, `Q`, `X` extracted as separate symbols), and words whose "fi" ligature is missing from the text layer (`irst`, `pro iles`, `inal`); the lualatex recompile of the same source matches 100.00%.
- **Renamed macros and labels.** No macro was renamed, so no difference arises from renames. Prefixed labels and environment names are not visible in the typeset text; numbering is the numbering of the source (the numbers "Lemma 3.1", "(5)", "Appendix B" are among the compared words).
- **Layout order (default pdftotext order).** For completeness the table lists the match in default layout order; it is lower (97.64% for T12, 97.89% for T22, 98.33% for T31, the rest 98.4-99.7%) only because that order depends on line and page breaks (stand-alone page with title block versus chapter), for example the order of the limits of a sum. It is not used for the acceptance statement; the raw-order match above is.

### The title block and the added note

Each chapter's part (c) starts with one added italic note (not part of the proof) saying which file the proof is and that labels carry a prefix. It is excluded from the comparison. The title block of the source (title, author, date) is excluded on the source side.

## 8. Items to report

- No mismatch between the highest proof version and FINAL_REPORT.md for any theorem.
- The three T12 helper files and the three rewritten paths (Section 5, item 4) are the only inputs beyond the contract's list.
- The document is built with lualatex and Windows fonts (Cambria, Consolas); on a machine without them the Markdown parts need another Unicode font with the same coverage (Cambria covers every non-ASCII character in the sources; checked with fontTools, no character missing).
- The stage labels in the Overview table (Stage A/B verdicts, finding counts) are copied from the review-history tables and prose of the FINAL_REPORT files; where a FINAL_REPORT gave "verified" for a round with gap findings (T11 Stage A rounds 1-2, T11 Opus round 1), the table repeats that wording together with the count.
- The Overview's "hypotheses taken from other conjectures" column and the Dependencies chapter come from the STATEMENT.md files: T12 uses START from T09(i); T15 uses H-T12 = T12(i); T31 uses H-T12 = T12(iii); T20 uses H03 = T03(i) (only (ii-C)); T22 uses T03 and T22(iii) only in (iv-c); T09, T11, T13, T14, T23 use none.
- Not done: no Fable/Astra review of the collected document (Stage C is the managing lead's step); no reading of the proofs for correctness (assembly only).
