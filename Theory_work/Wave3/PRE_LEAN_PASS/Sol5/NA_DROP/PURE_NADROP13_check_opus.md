# PURE check of NA_DROP v1.3 (MANIFEST_NADROP13 91805b68), fresh Opus seat

**Result: PURE.** The coordinator applied the Opus R2 wording findings exactly as written and changed nothing else. The final staged files match the scripted application byte for byte, no claim text changed, and every code citation the seat added is right to the line.

**Manifest verify:** `python3 Theory_work/Wave3/tools/manifest.py verify …/Sol5/NA_DROP/ticket …/MANIFEST_NADROP13.txt` printed `verify: OK MANIFEST 91805b680bd05ba438a8b7b6f3f9d99b382dde70b378772bd7f595597c33f714` (exit 0).

## (1) The Old/New pairs reproduce the final text byte for byte

My script is `.rc_tmp/pure_nadrop13/apply.py`. It takes the quoted strings straight from the review lines `NA_DROP_R2_council_opus.md`:39/41, 47/48, 49/50, 57/58, 64, 65, 71, 78, 83/84 and 89/90. It matches each Old string with whitespace collapsed to `\s+` and applies it to `v1.3_ticket/`.

| pair | file | matches |
|---|---|---|
| F-1 | REPORT.md | 1 |
| C-1a | L3_listR.md | 1 |
| C-1b (insertion: Old + " " + New) | L3_listR.md | 1 |
| C-2 | L3_listR.md | 1 |
| S-1a | L3_listR.md | 1 |
| S-1b | L3_listR.md | 1 |
| S-2 | L3_listR.md | 1 |
| E-1 | L3_listR.md | 1 |
| E-2 | READER_DELTA.md | 1 |
| E-3 | CARD.md | 1 |

The script result equals the final staged text byte for byte in all five files:

| file | sha256 prefix |
|---|---|
| STATEMENT.md | c968e071 (unchanged from pre-R2) |
| lemmas/L3_listR.md | aeead9cb |
| REPORT.md | 7fc48c12 |
| CARD.md | 73beff45 |
| READER_DELTA.md | 88e31037 |

So nothing else changed. Both ticket folders hold exactly these five files.

Between `MANIFEST_NADROP13_pre-R2.txt` and `MANIFEST_NADROP13.txt`, only these lines differ:
- the header line;
- the hashes of the four edited files;
- the new `#EXTRA` line and its `EXT:` hash row.

The STATEMENT hash is unchanged.

**One reading of the review was needed (E-2).** The review gives the old clause (`:83`) with inner single quotes, while the file uses double quotes. The new text (`:84`) ends the sentence with ".", so the Old string has to include the sentence's final `".`. With that reading it matches exactly once and gives the final text byte for byte.

## (2) G4-1: the IMPL_LIST_codeprint.md pin

- `sha256sum Theory_work/Wave3/W3-D5P/reviews/IMPL_LIST_codeprint.md` gives `72a2d781cfe7e3d786fb6640f6109d5a4f22b87cdcf5ec73d84017c61eae6fb2`, the value the seat gave. The file's last commit is df1f5872.
- It is listed once in `MANIFEST_NADROP13_EXT.txt` (`:37`).
- It appears once as an entry in the manifest: the `#EXTRA` line at `:34` and the hash row `72a2d781…  EXT:…` at `:72`. Two lines is the normal form for any extra input.

## (3) No premise or claim is added

- **STATEMENT.md** is byte-identical between the pre-R2 and final tickets. Against v1.2, only line 1 changes (in place: v1.2 to v1.3) and the changelog row `:168` is appended, as before.
- **LIST-R conclusion level:** `bvsreg.conclusion_level({"conclusion": <REPORT:66 text after "conclusion:">})` returns `'reported-model'`, which is in `CONCLUSION_LEVELS`.
- **Converter:** `ingest.py convert` on a scratch copy of the staged REPORT.md (`.rc_tmp/pure_nadrop13/convert/W3-D5P/REPORT.md`, which `cmp` confirms equals the staged file) exits 0 with 3 records and nothing on stderr. The records' levels are LIST-K identity, LIST-CODE identity and LIST-R reported-model.

## (4) The seat's added citations, checked against the code of record

The code of record is the tag `method-v3.1.1-listpip` = 7100bb3b. Its core tree is 61b0a582, and the working-tree core matches the tag file by file. `v3_run.R` has no diff between e9bac478 and 7100bb3b, so E-1's claim holds.

| citation | what is there | right? |
|---|---|---|
| `v3_setup.R:8` | `stopifnot(… !is.unsorted(orig, strictly = TRUE))`, so `orig` (and hence `D.orig`) is strictly increasing | yes |
| `v3_run.R:245-279` | `v3_list_fields` starts at 245; `v3_add_list_fields` is at 269; `v3_exact_list_last` ends at 279 | yes |
| `v3_run.R:276` | `lf <- v3_list_fields(e$top, ctx$orig, names(e$pip))` | yes |
| `v3_run.R:161-162` | `rownames(out$pip_r) <- orig` and `pip_primary <- setNames(rowMeans(P), orig)`: length p | yes |
| `v3_run.R:160, 220` | in `v3_assemble_final`, which `v3_final_run` calls at `:230` with `list_fields` passed through | yes; the "standalone `v3_final_run`" wording is accurate |
| `v3_fit.R:99-102` | `pre$status != "ok"` gives an early `return(finish(fit))` | yes |
| `v3_fit.R:131` | `return(v3_exact_list_last(finish(fit), e, ctx))` | yes |
| `v3_fit.R:162` | `v3_final_run(…, list_fields = FALSE)` | yes |
| `v3_fit.R:176` | sampler-branch `v3_list_fields(fit$top_store, ctx$orig, names(fit$pip_primary))` | yes |
| `v3_preprocess.R:114` | `if (!length(kept)) return(… status = "no_predictors" …)` | yes |
| `cpp/v3_core.cpp:558` | `NumericVector pip(p);` with `p = D.p` (`:526`) | yes |
| `v3_exact.R:9` | `names(r$pip) <- orig` | yes |

None is off by a line. The seat's added (non-code) pointer to `reviews/IMPL_LIST_codeprint.md` §5 is also acceptable: §5 records the discharge at 7100bb3b, and the closing line of that file reads "IMPL-LIST: DISCHARGED at method-v3.1.1-listpip (7100bb3b)".

**Housekeeping:** I changed no tracked file, made no commit and started no subagent. Scratch is under `.rc_tmp/pure_nadrop13/`. Early on I wrote one stray diff file, `.rc_tmp_check.diff`, at the worktree root and deleted it, so `git status` is clean. The `bvsreg` import also added only bytecode to the existing, git-ignored `Theory_work/INFRA/tools/__pycache__/`.

PURE-VERDICT: PURE
