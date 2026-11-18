# LINES_CHECK — W2-UNI `lemmas/L5_delivery.md` patch v2 (F-UNI delivery narrow)

Run on 2026-11-16 at 05:47 CST against origin/main 967313dd. The registry `claims.tsv` is byte-identical to its state at e1e98f1d,
and the target file and code are unchanged between the two commits.
Patch: `L5_delivery_F-UNI_v2.patch` (sha256 `574dbf66b90a318c6441848a3f4299f232021358df1ff7f81455b3d27be27131`).

**Method.** I took the origin/main file and a copy patched with the diff; both lived in `.rc_tmp/`, since deleted. `git apply --check` passes on origin/main.
Hashes follow the registry's own rule. The span hash is `bvsreg.text_hash`: lines rstripped, LF-joined, sha256. The claim hash
reproduces `bvsreg.claim_hash`: the statement span, then each premise span preceded by its `--premise path--` marker line, all
through `text_hash`. Recomputed before the patch, it equals F-UNI's stored `sha256`, which validates the method.

**Result: PASS. No registered or cited span moves.**
- Lines in place (1–40): only **1** (title-line changelog, outside every span) and **15–21** (inside F-UNI's span) change.
- New lines: the remark is appended as **41–49** after the old last line 40. The file grows 40 → 49 lines, all at the end, so no
  existing line number shifts.
- The proof (23–34), the Instances/Qualifications paragraph (36–40) and the premise span 8–13 are byte-identical.
- Only W2-UNI:F-UNI changes hash.

## A. Rows with file = W2-UNI/lemmas/L5_delivery.md (only one exists)
| id | lines | span sha256 before | span sha256 after | same? | claim_hash before (= stored?) | claim_hash after | same? |
|---|---|---|---|---|---|---|---|
| W2-UNI:F-UNI | 15-21 | 8ab5c3f3dcca005131ddcd30d92483fc8979fb00909ad2ad61761a1e3e6a52c5 | 7fd7589e29781fc74fd47892ce26ea596dce5556ecb251179ae881a773cb19be | NO | b0a0f3c2cf20d781e33802533bce42f4e2b74385920048616248a1bc1ff8cf97 (= stored) | 05c4cdf65a209b212d4207d8bac7a1df2dcbedde1cd14331f948f444925ad2cf | NO |

## B. Every cite `W2-UNI/lemmas/L5_delivery.md:a-b` in claims.tsv (any column)
| cited span | cited by | sha256 before | sha256 after | same? |
|---|---|---|---|---|
| 8-13 | W2-UNI:F-UNI [premises] | fe1bf8a74e6cd430fe483fd861e203b87f27329f30e8090dd1f31be531e7d9e5 | fe1bf8a74e6cd430fe483fd861e203b87f27329f30e8090dd1f31be531e7d9e5 | YES |

The fragments/corrections files cite `:8-13`, `:23-34` and `:24-37` in `c6_w2_misc.tsv` and `c7_w2uni_closed.tsv`. All three are unchanged.

## C. Line cites into this file outside the registry (checked so that nothing drifts)
Short hashes are the first 16 hex digits of the same `text_hash`.

| cite | where | before | after | same? |
|---|---|---|---|---|
| :4, :5, :12, :29, :30, :33, :39 | W2-UNI `reviews/CITECHECK*.{txt,md}` (status / citation checks) | df8058eb…, f193228e…, fea6cbd0…, a6a07b0d…, fcab6f4c…, 6ebc4162…, 9d3af6a1… | identical | YES |
| :7-12, :39-40 | W3-READER `READER_VERSIONS.md:50, :686` (running ticket) | 054e4888…, 2b0b3838… | identical | YES |
| :8-13, :23-27 | `Dept/research/FUNI_transfer/TR1_sol.md` | fe1bf8a7…, b6ce4ade… | identical | YES |
| :15-21 | W3-READER `READER_VERSIONS.md:682`; paper `generated/MANIFEST.txt:20` | 8ab5c3f3… | 7fd7589e… | NO (intended: F-UNI's span) |
| :16, :17-18, :19, :15-34, :32-33 | `Wave3/API_AUDIT/{pass1,sharp1}/results/f30.md`, `f14.md`, `R-AUD1_sol.md` | — | — | historical audit records. Each is pinned to the old file by its MANIFEST.tsv (9b50e358…). Inside 15–21 the rewrap moves (V) to line 15, (S) to 16 and (P) to 17, so these cites resolve only against the pinned version. :32-33 is unchanged. |

**Whole file:** sha256 `9b50e358f5b6c6b037f81dda8f7a8ddb78fdb6083e80021d5297e321c42fb056` → `b6b2465c1813ffd0df5ce9482d562a26eab5e9ff881027893bd40f86ee0f2295`.

## For the recorder (outside the patch)
On apply, F-UNI is rehashed to sha256 `05c4cdf65a209b212d4207d8bac7a1df2dcbedde1cd14331f948f444925ad2cf`. Its span stays 15-21 and its premises stay 8-13. Version goes **1.1.0 → 2.0.0**: a major bump, because the hypotheses get stronger, for the WEAKER tag.

Recorder actions:
- Add **A:IDEAL-W+** (`A_IDEALW_PLUS.md`) to F-UNI's `assumptions`, next to A:DELIVERY-ALLOC.
- Update `conclusion` to: "P(no output)=0 for (n,p_raw) in 𝔇 under IDEAL-W; every n and P(S+=S0)->1 under A:IDEAL-W+".
- Add to `notes`: "v2.0.0 NARROW (HQ correctness event 11-16; TR1 TRANSFER: NO, EVERY-N UNDER IDEAL-W: NO; DIFF_sol)".
- Clear SUSPECT on F-UNI only.
- Regenerate the paper block `generated/blocks/W2-UNI_F-UNI.tex` (`assemble.py`). Its MANIFEST line 20 prefix goes b0a0f3c2cf20d781 → 05c4cdf65a209b21.
