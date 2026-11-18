The staged v2 is PURE. All five checks pass and I found nothing that needs correcting. I ran everything from HEAD 17953966; the coordinator committed during my run, but the stage folder is unchanged since c90e8692. Scratch went only to `.rc_tmp/pure_d5pa_v2/`, which git ignores. No tracked file changed in either tree, nothing was committed and no subagents were started.

## (1) Patch application, scope, line counts, byte identity

**Patch application.** `git -C /home/fb31/BVS-wt/RECORDER2/.rc_tmp/final apply --check D5Pa_v2_stage.patch` passes. `patch -p1 -F0` applies it to scratch copies of the batch tree's seven files with rc=0. All seven patch `index` lines match `git hash-object` of the batch-tree files and of the patched copies (e.g. CARD 3f8364fe..49f84f39, STATEMENT 32e13478..66826992, card bea744bd..fcaca22e, RV 3c59cfde..16fdbc0a).

**Lines that change.** A diff of the original against the patched copies gives exactly these lines:

| file:line | edit | change |
|---|---|---|
| `W3-D5P/STATEMENT.md:95` | a-1 | "on an exact-branch run," → "on a run with status \`exact\`," |
| `W3-D5P/lemmas/L2_listCODE.md:148` | a-1 | "\*Exact branch.\*" → "\*Exact branch (status \`exact\`).\*" |
| `W3-D5P/REPORT.md:53` | a′-1 | "; exact branch: the enumeration's store" → "; on status exact: the enumeration's store" |
| `W3-D5P/CARD.md:10` | a′-2 | "The PIP errors…" → "When \$p\ge2\$ for all large \$n\$, the PIP errors…" |
| `W3-D5P/CARD.md:13` | a′-2 | inserts " (for the rate: \$p\ge2\$ for all large \$n\$)" after "under the hypotheses of Theorem 6" |
| `W3-D5P/READER_DELTA.md:29` | a′-2 | "Since \$\varepsilon_n=O_P(…)\$, the two" → "When \$p\ge2\$ for all large \$n\$, \$\varepsilon_n=O_P(…)\$, so the two" |
| `W3-READER/CLAIMS_CARD.md:71` | a-2 | the same "When \$p\ge2\$ for all large \$n\$, t…" insertion as CARD:10 |
| `W3-READER/READER_VERSIONS.md:1441` | a-2 | the same rewrite as READER_DELTA:29 |

Nothing else changes.

**Line counts are unchanged:** 23, 44, 72, 163, 154, 181 and 1458.

**Byte identity.** All seven staged files are byte-identical (`cmp`) to the patched batch-tree files: the five `ticket/` files plus `staged_reader/CLAIMS_CARD.md` and `staged_reader/READER_VERSIONS.md`. The other 12 ticket files are byte-identical to the batch tree's `W3-D5P/`. The ticket file set is exactly the 17 files: `reviews/`, `LOG.md` and `CHECKPOINT_*` are left out.

**a-3 is already in the batch tree.** The a-3 sentence ("pathwise on the part of the stated event where \$\pi(S_0\mid y)\ge n^{-cM/2}\$ (there the list holds at least that mass);") is extracted from `Sol2/Sol2-S2-1_correction.patch`. It occurs exactly once in the batch tree's `CLAIMS_CARD.md`, on :71, and exactly once in `READER_VERSIONS.md`, on :1443. The old "pathwise (on the stated event);" occurs zero times. The patch has no a-3 hunk.

## (2) Text

- **a-2 qualifier.** "When \$p\ge2\$ for all large \$n\$" is the qualifier of STATEMENT (C3)(ii), "Rate (p ≥ 2 for all large n)… If p ≥ 2 for all large n" (:116). It opens the sentence, so it also covers the "without 'on output'" part, as (C3)(iii) :124 does ("if moreover p ≥ 2 for all large n").
- **a′-2 wording matches NA_DROP v1.3:**
  - CARD:13 is byte-equal to the NA_DROP v1.3 ticket's `CARD.md:13`.
  - READER_DELTA:29 is byte-equal to NA_DROP's `READER_DELTA.md:29`. The brief cites :30, but :30 is the continuation line; the rate phrase sits on :29 in both files.
  - In CARD:10 the rate clause "When \$p\ge2\$ for all large \$n\$, the PIP errors and the log-evidence error" is the same words as NA_DROP's. The rest of the line differs only by NA_DROP's own edits: "where returned", "(where printed)", and the IMPL-LIST status cell.
- **a′-1 is true.** In `Scripts/SMC_BVS/core/v3_fit.R`:
  - The branch is fixed at :106.
  - `if (pf$exceeds) { fit$status <- "resource_limit"; return(finish(fit)) }` at :117 runs before `v3_enumerate` (:121), so a `resource_limit` exact-branch run has no enumeration store.
  - `pip_primary`, `mpm` and `estimates_available` are set only when `e$status == "exact"` (:125-129).
  - A non-exact enumeration status keeps a partial `e`, sets `hpm_incomplete`, and `v3_exact_list_last` returns early (`v3_run.R:275`).

  So "on status exact: the enumeration's store contains the HPM-order maximum of Omega, pip_primary/mpm are exact" is correct, and it equals (iv)'s "On status `exact`". At the code of record 4676af6 these lines are the same (:117, :120-129). The batch tree's `v3_fit.R` differs from 4676af6 only in the list-field lines.

## (3) No added premise or claim; consumers of LIST-CODE (v)

- **a-1 and a′-1 only narrow.** They limit the exact clause of (v) and of the REPORT summary to status `exact`. That is the condition (iv) already states (:91) and that STATEMENT §1 :54 uses to define the exact branch. L2 Step F's exact clause uses only (iv), so the proof matches.
- **a-2 and a′-2 only restore (C3)(ii)'s qualifier.** CARD:13's "(for the rate: …)" limits only the rate in the Option B text (:14-15).
- **Nothing in the batch tree changes the consumers.**
  - `git diff f6411c3e 330b87b4` on `W3-D5P/` outside `reviews/` is empty.
  - The batch's edits to W3-DIST and W3-READER contain no LIST-CODE reference. The only list-related lines are the a-3 card and RV lines.
  - A fresh grep of LIST-CODE (v) and "exact-branch run" consumers gives exactly the v1 consumer table: `L3_listR.md:51/:64`, `PLAN.md:9`, `CHECKPOINT_3.md:62`, `LOG.md:24/:28`, `ERRATA.md:7`, `post_cp3/COR9C_*`, `REPORT.md:10`, STATEMENT §5, `TARGET.md:8`.
  - Each of these uses the sampler/completed-run clause, the exact clause on output runs (status exact), or (i)–(ii) only. None is affected.

## (4) Registry effect on the batch tree

I imported the clone's `bvsreg` (its ROOT is the clone) and computed `claim_hash` for all 553 rows, first on the batch tree and then with the seven patched files substituted.

- **Before the patch, all 553 hashes match the registered `sha256`.**
- **Exactly one registered hash changes:** `W3-D5P:LIST-CODE` (STATEMENT.md:79-95, premises :29-38 and :49-57) goes from 90fdaf875ca8 (the registered value) to fd8450cca0eb.
- **Unchanged:**
  - `W3-D5P:LIST-K` (:67-75) and `W3-D5P:LIST-R` (:99-125, premises :29-63), whose spans do not include :95.
  - `W3-READER:R1` (highest RV premise line :1388) and `W3-READER:R3` (RV :32-60).
  - No row hashes `REPORT.md`, `CARD.md`, `READER_DELTA.md`, `L2_listCODE.md`, card :71 or RV :1441.
- **The REPORT `conclusion` is not hashed.** It is a plain registry field; claims.tsv still holds "exact branch: the enumeration's store…" until re-ingest. It is not in `sha256` and not in the fp2 `ACCEPT_FIELDS`.
- **Accept stamps will go stale.** Because `sha256` is an fp2 field, the accept stamps of LIST-CODE and of anything that consumes it (LIST-R `@stmt` and downstream) go stale and need the usual re-point or re-accept.
- **Manifests that verify OK on the batch tree today and stop verifying when this lands:**
  - `W3-D5P/reviews/MANIFEST_R3r3` (pins the ticket files)
  - `W3-READER/reviews/MANIFEST_R5r9` (pins card and RV)
  - `W3-D2/reviews/MANIFEST_R2f7` and `W3-D3/reviews/MANIFEST_R2g6` (card and RV as EXT)
  - `W3-FAMC/reviews/MANIFEST_R5r4` (RV as EXT)

  The `PRE_LEAN_PASS` freezes were not checked.

## (5) Converter and verify

- **Converter.** `ingest.py convert Sol5/D5Pa_v2_b330/ticket/REPORT.md` exits 0 with 3 REGISTRY blocks, nothing on stderr, and the LIST-CODE conclusion carrying "on status exact:". The worktree's and the clone's `ingest.py` are byte-identical, and the clone's also exits 0.
- **Verify.** I built a scratch git repo at `.rc_tmp/pure_d5pa_v2/vrepo`. It holds the 26 non-reader EXT files from the clone, the two staged reader files from the worktree, and the ticket at `Theory_work/Wave3/PRE_LEAN_PASS/Sol5/D5Pa_v2_b330/ticket`. `manifest.py verify` returns `verify: OK MANIFEST 0475345043894a0bcdaab8bc58e84b4e2debc60c98a635f8d6be37c5ca2e1d09`, rc=0.
- **Re-freeze.** Re-freezing with `MANIFEST_D5Pa_v2_b330_EXT.txt` gives a file byte-identical to the staged manifest (45 files, 28 extra inputs).
- **Check of the coordinator's method.** The unedited ticket (the five batch-tree files put back, the clone's W3-READER files, R3r3's #EXTRA) freezes to `e550e999…`, which is R3r3. The clone's own `MANIFEST_R3r3` also verifies OK.
- **Difference from R3r3.** Only the five ticket rows and the swap of the two reader EXT paths for their staged copies.

## Notes that do not block (outside PURE's scope)

1. **The NA_DROP stage still has the old wording.** Its v1.3 ticket has "on an exact-branch run" at `STATEMENT.md:96` (a-1) and "exact branch:" in the `REPORT.md:53` conclusion (a′-1). Whichever stage lands second must carry both narrowings over and re-freeze.
2. **DEPS.tsv will go stale.** It keeps 5dc11132… (STATEMENT) and b023caf… (L2), which will no longer match the landed files (e3196041…, 60b391fd…). The recorder needs to update them, along with STATEMENT's changelog row and the LIST-CODE version bump.
3. **`v3_fit.R` is not in the EXT list.** LIST-CODE (iv)/(v) cite it (:117-129), but the list (inherited unchanged from R3r3) does not freeze it. This is a pre-existing coverage gap, not something this stage introduced.

PURE-VERDICT: PURE
