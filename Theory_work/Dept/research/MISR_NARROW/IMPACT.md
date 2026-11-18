# IMPACT — manifests that hash W3-MISR/STATEMENT.md (if the Cor-H KL narrow is applied)

2026-11-16 04:24 CST. Search: `git grep` on origin/main c3070591, and `find` over `/home/fb31/BVS-wt/*/` and
`/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/`, for every `*MANIFEST*`, `INPUTS*` and `DEPS.tsv` that
names `W3-MISR/STATEMENT.md` or contains its current sha256 `797bca0e…4b87`. No DEPS.tsv names the file. Copies in other
worktrees (citefix, eng-offload, LEAN, POST2-diff, PSMC-S0, rec-main, record-1115, W3-EDIT, W3-PSHARP-R, W3-READER, W3-RM2-R,
W3-SCR-R2, W3-START2-R, W3-T03ACC, WRITING, W3-MISR-R) of the origin/main manifests are byte-identical to origin/main, or are
older checkouts of the same files (`MANIFEST_R2r.txt` is sha 500ad5b0… everywhere). They are listed once below.

The patch changes the file's sha256 (797bca0e…4b87 → 84eb0f27…). So **every manifest that pins
797bca0e becomes stale** when the patch is applied. W3-MISR's own manifests walk the whole folder, so they pin `STATEMENT.md` as a
relative path.

Precedent (D39/D41, commit 7c45d4b): after the C-MIS citefix, the department ran a PC-style diff check
(`research/PC_CMIS_CITEFIX_opus.md`). It then re-froze `MANIFEST_R2r.txt` as "MANIFEST_R2 with only the drifted hashes changed"
and verified that exactly those differences exist. It added HQ seat carriers `R2r_record_{sol,opus}.md`, each copying its
seat's own per-claim table verbatim and adding one verdict line for the new digest (`manifest.py bind OK`). Finally it
re-pointed the council cell on all rows of the ticket and ran `check.py --acceptance --record`. Here the diff check is the
Sol diff check `DIFF_sol.md` (v4 rule: statement change → OpenAI reviewer). It is not citation-only, so the carriers must
cite it **and** the WEAKER tag.

| # | manifest (path) | pins | state | needed if the patch is applied |
|---|---|---|---|---|
| 1 | origin/main `Theory_work/Wave3/W3-MISR/reviews/MANIFEST_R2r.txt` (digest d84f10be…704b), line 27 `797bca0e… STATEMENT.md` (folder walk) | current | **ACCEPTED**: the council cell of all 7 W3-MISR rows points to it | **Re-freeze** as `MANIFEST_R2s.txt` (= R2r with only the STATEMENT.md line changed; verify shows exactly 1 difference) + **HQ seat carriers** `R2s_record_{sol,opus}.md` citing `Theory_work/Dept/research/MISR_NARROW/DIFF_sol.md` (WEAKER, Cor-H only) + council cell re-point on all 7 rows + Cor-H rehash (`a4f83d8c…`, v1.0.0 → 1.1.0; the other 6 hashes are unchanged, see LINES_CHECK.md) + `check.py --acceptance --record`. Bundle the optional proof-line clarification (`lemmas/G_corollaries.md:91-93`, "with α deterministic", per W3-MISR-R `reviews/post_cp3/ERRATUM_W3-MISR_KL.md`) into the **same** re-freeze if HQ wants it, because it is in the same walked folder. The proof already treats α as a constant, so it proves the narrowed statement as is. |
| 2 | origin/main `Theory_work/Wave3/W3-MISR/reviews/MANIFEST_R1.txt` (4ee71a39…), `MANIFEST_R2.txt` (916852b9…) | already stale (earlier versions v1.1/v1.2) | historical, superseded by R2r | none |
| 3 | origin/main `Theory_work/Wave3/W3-MISR/reviews/INPUTS.txt` | external inputs only; does not list W3-MISR/STATEMENT.md | — | none |
| 4 | origin/main `Theory_work/Wave3/API_AUDIT/sharp2/MANIFEST.tsv`, `sharp2_v1_maxtokens/MANIFEST.tsv` (`916852b9…`) | already stale | historical API-audit send record | none |
| 5 | origin/main `Theory_work/INFRA/paper/generated/MANIFEST.txt` | claim spans MIS(i) 110-123, MIS(i') 127-140, MIS(ii) 144-160 (claim-hash prefixes); no Cor-H block | ACCEPTED (generated) | none: all three hashes unchanged (LINES_CHECK). Re-run `assemble.py` after the recorder step as usual; expect no block diff. |
| 6 | W3-DIST `reviews/MANIFEST_S2.txt` (54cf9123…), EXT line 107 `797bca0e…` (+ `INPUTS_S2.txt`) [`/home/fb31/BVS-wt/W3-DIST/…` = `/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/…`, identical] | current | RUNNING ticket, blind read S2 done (not on origin/main) | If applied before DIST's CP3: re-freeze `MANIFEST_S2r` + carrier citing DIFF_sol.md (DIST consumes W3-MISR:R′, which is unchanged; no DIST file cites :178-197). Simpler: **apply after DIST CP3**, or accept S2 as is with a one-line note. |
| 7 | W3-DIST `reviews/MANIFEST_SW1.txt` (de9ccec7…), EXT line 225 `797bca0e…` (+ `INPUTS_R1.txt` line 6) | current | RUNNING: sweep SW1 (frozen 11-16 01:28); **R1 council freeze imminent** (QUEUE: Mon late a.m.) | Same as #6 for SW1. **R1:** if the patch lands **before** the R1 freeze, R1 simply hashes the new file and needs nothing. If it lands **after**, R1 needs re-freeze + carriers. Recommend: either merge before the R1 freeze, or hold until after DIST CP3 (Wed 18:00). |
| 8 | W3-MISR-R `reviews/MANIFEST_R3.txt` (43b2366b…), EXT line 30 `797bca0e…` | current | council **R3 PASS** (CP3 done), acceptance **not yet recorded** (no rows on origin/main) | If applied before the record: re-freeze `MANIFEST_R3r` + HQ seat carriers citing DIFF_sol.md. Natural fit: this rider *is* the source of the narrowing. Its cites `BASE :187-191`, `:191-195`, `:196-197`, `:181-183` keep their line numbers. Also re-word the tombstone in `reviews/post_cp3/BASE_KL_VERDICT.md`: after the patch the parent no longer asserts the random-α reading, so cite "W3-MISR STATEMENT v1.3 :191-195". |
| 9 | W3-MISR-R `reviews/MANIFEST_R1.txt` (fadb67e8…), `MANIFEST_R2.txt` (227720d3…) + `INPUTS_R1.txt`, `INPUTS_R2.txt` | current | earlier rounds, superseded by R3 | none (historical) |
| 10 | W3-READER `reviews/INPUTS_R1.txt` (line 8) | list only, no hash; no READER manifest frozen yet | RUNNING: CP3 council briefs drafted | If the patch lands before the READER CP3 freeze: nothing (the freeze hashes the new file). After the freeze: re-freeze + carrier. The thm4 row (`READER_VERSIONS.md:404-406`) uses the reading only with a fixed intercept (W3-MISR-R `reviews/V11a_quote_check.md`), so its content is unaffected. |

**Summary for HQ.** One accepted manifest needs a re-freeze plus carriers: W3-MISR `MANIFEST_R2r`. Three running tickets pin the
file: W3-DIST (S2, SW1, and the imminent R1), W3-MISR-R (R3, PASS but unrecorded), and W3-READER (not frozen yet). Two timings
minimise carriers. **(A)** Merge before the DIST R1 and READER freezes. Carriers are then needed for MISR R2r, MISR-R R3, and
DIST S2/SW1 if those are counted. **(B)** Hold until after Wed CP3 and do one post-freeze batch with the W3-EDIT erratum
(MISR R2r + MISR-R R3r + DIST R1/CP3 + READER). Per D41 practice (merge only what touches no frozen manifest), (B) is the default.

**Recorder notes** (outside the patch): Cor-H `version` 1.0.0 → 1.1.0. Cor-H `notes` should name ERR-W3-MISR-KL1 / this narrow.
The header's history paragraph (`STATEMENT.md:5-9`) was **not** extended, because that would shift lines. Line 1 carries the
v1.4 entry in place.
