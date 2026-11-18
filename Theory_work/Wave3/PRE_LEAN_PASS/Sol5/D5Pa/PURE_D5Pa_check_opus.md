# PURE check: D5P (a) stage D5Pa (MANIFEST 9a70be48…)

I ran this from `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-215eb534-a080473e9c42fff9` at HEAD 36353e8e. Scratch went only to `.rc_tmp/pure_d5pa/`, which git ignores. No tracked file changed, nothing was committed and no subagents were started; `git status` is clean.

## (1) Patch application, scope, line counts, byte identity
- **`git apply --check`:** passes on the tree.
- **`patch -p1 -F0`:** applies to a scratch copy of the four live files with rc=0.
- **Patch headers:** the `index` lines (32e13478..66826992, 827d298f..4e3c885e, 210d8067..2d1d86e2, 8d341c33..ee1f7671) match `git hash-object` of the live files and the patched copies.
- **Exactly these five lines change, and nothing else:**

| file:line | change (character level) |
|---|---|
| `W3-D5P/STATEMENT.md:95` | "on an exact-branch run," → "on a run with status \`exact\`," |
| `W3-D5P/lemmas/L2_listCODE.md:148` | "\*Exact branch.\*" → "\*Exact branch (status \`exact\`).\*" |
| `W3-READER/CLAIMS_CARD.md:71` | a-2: "The PIP errors…" → "When \$p\ge2\$ for all large \$n\$, the PIP errors…"; a-3: "pathwise (on the stated event);" → "pathwise on the part of the stated event where \$\pi(S_0\mid y)\ge n^{-cM/2}\$ (there the list holds at least that mass);" |
| `W3-READER/READER_VERSIONS.md:1441` | "Since \$\varepsilon_n=O_P(…)\$, the two" → "When \$p\ge2\$ for all large \$n\$, \$\varepsilon_n=O_P(…)\$, so the two" |
| `W3-READER/READER_VERSIONS.md:1443` | the same a-3 replacement as the card |

- **Line counts are unchanged:** 163, 154, 181 and 1458.
- **The staged files are byte-identical (`cmp`) to the patched live files:** `ticket/STATEMENT.md`, `ticket/lemmas/L2_listCODE.md`, `staged_reader/CLAIMS_CARD.md` and `staged_reader/READER_VERSIONS.md`.
- **The other 15 ticket files are byte-identical to live `W3-D5P/`.**
- **Unedited ticket:** with the two live files put back and frozen with R3r2's #EXTRA list, the ticket gives `0c313200d171ae6c…`, which is R3r2. Live `W3-D5P` against `MANIFEST_R3r2.txt` also verifies OK.

## (2) Text equalities
- **a-3 sentence:** it is identical in the staged card :71, staged RV :1443 and both "+" lines of `Sol2/Sol2-S2-1_correction.patch` (checked by script; all four strings are equal). Its condition is ERRATA.md:7's: 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}. This also matches COR9C_NOTE (N1) and DIST STATEMENT :229 (π(𝒯) ≥ n^{−cM/2}). So the stage does supersede S2-1 in the same two places. S2-1 left out `Docs/Writing/from_theory/COR6L_9C_NOTE_2026-11-17.md:3`, which still has the old wording and stays with the manager, as before.
- **a-2 qualifier:** "When \$p\ge2\$ for all large \$n\$" matches STATEMENT (C3)(ii) "Rate (p ≥ 2 for all large n)… If p ≥ 2 for all large n" (:116). It sits at the start of the sentence, so it also covers the "without 'on output'" delivery part, matching (C3)(iii) "if moreover p ≥ 2 for all large n" (:124).

## (3) Truth; no added premise or claim; consumers of (v)
- **Code at `Scripts/SMC_BVS/core/v3_fit.R`:**
  - The branch is fixed at :106.
  - The preflight check `if (pf$exceeds) { status <- "resource_limit"; return }` at :117 comes before `ctx`, so it comes before `v3_enumerate` (:121) and before `fit$exact` and `fit$hpm` (:122-123) exist.
  - `estimates_available` becomes TRUE only when `e$status == "exact"` (:125-129).
  - `cpp_enumerate` can also return `numerical_failure` (`cpp/v3_core.cpp:556`), which leaves a partial `hpm` and `top`.
  - So the old exact-branch clause of (v) was not justified for `resource_limit` runs, nor for `numerical_failure` runs. Restricting it to status `exact` is true. Those lines are identical at the code of record 4676af6.
- **Narrower only:** the new (v) is strictly narrower and uses only (iv), which is already stated "On status `exact`" (:91). STATEMENT §1 :54 already defines the exact branch as "(status `exact`, …)". No premise or claim is added.
- **L2 Step F:** the exact clause uses only "S₀ ∈ Ω is the hpm_better-maximum of Ω; by (iv)". (iv) is on status `exact`, so the proof matches the narrowed statement.
- **Consumers of LIST-CODE (v)**, from a grep of W3-D5P, W3-READER and W3-DIST outside reviews/, plus post_cp3:

| consumer | clause of (v) it uses | affected? |
|---|---|---|
| `L3_listR.md:51` | sampler, completed run | no |
| `L3_listR.md:64` | exact clause, on output runs only; :48-49 shows exact-branch 𝒪 = {status "exact"} | no |
| `PLAN.md:9` | sampler | no |
| `CHECKPOINT_3.md:62`, `LOG.md:24` | (i),(v) for Cor 9C, on completed runs | no |
| `post_cp3/COR9C_NOTE.md:35,73,83` and `COR9C_check_opus.md:69` | (i),(v) for Cor 9C, on completed runs; cites `STATEMENT.md:82-95`, unchanged | no |
| `ERRATA.md:7` (E3 fix) | (i),(v) for Cor 9C, on completed runs | no |
| `LOG.md:28` | (i)–(v), a spec consistency check | no |
| STATEMENT §5 remark 3, `TARGET.md:8`, `REPORT.md:10` | (i)–(ii) only | no |
| W3-READER, W3-DIST | cite LIST-CODE as a status only | no |

  No consumer is affected, so the "carrier: no consumer affected" claim holds.
- **a-2 and a-3 are true:** on 𝒢⁺_n, S₀ ∈ 𝒯, so π(𝒯) ≥ π(S₀|y). That is the parenthetical, and it is COR9C_NOTE (N1) verbatim in substance.

## (4) Registry effect
Computed with `bvsreg.claim_hash` over all 553 rows, live and then with the four patched files.

- **Exactly one registered hash changes:** `W3-D5P:LIST-CODE`, span STATEMENT.md:79-95 plus premises :29-38 and :49-57, goes from 90fdaf875ca8 (= the registered value) to fd8450cca0eb.
- **Unchanged:**
  - `W3-D5P:LIST-K` and `W3-D5P:LIST-R`, whose spans and premises do not include :95.
  - `W3-READER:R1` and `W3-READER:R3`, whose RV premise spans end at :320 and :60.
- **No hash for the L2 file:** L2 is not a registered span, and no registry row or fragment hashes it.
- **No reader row or fragment span covers card :71 or RV :1441/:1443.** The highest RV span is :1276-1379.
- **Manifests that verify OK today and stop verifying once the patch lands:**

| manifest | how it pins the changed files |
|---|---|
| `W3-READER/reviews/MANIFEST_R5r8` | card and RV as ticket files |
| `W3-D5P/reviews/MANIFEST_R3r2` | STATEMENT and L2 as ticket files; card and RV as EXT |
| `W3-D2/reviews/MANIFEST_R2f6` | card and RV as EXT |
| `W3-D3/reviews/MANIFEST_R2g5` | card and RV as EXT |
| `W3-FAMC/reviews/MANIFEST_R5r3` | RV as EXT |
| `PRE_LEAN_PASS/Sol5/NA_DROP/MANIFEST_NADROP`, `_v1.2`, `13` | card, RV and live L2 as EXT |

  All other manifests that pin these files were already stale. Each of these needs the usual re-point (row version bump) or a re-freeze at landing.
- **Comparison with the patch headers:** the four files in the headers are exactly the four files whose content changes. Of them, only STATEMENT.md carries a registered span that moves (LIST-CODE).

## (5) Converter and verify
- **Converter:** `ingest.py convert Sol5/D5Pa/ticket/REPORT.md` exits 0 with 3 REGISTRY blocks and nothing on stderr.
- **Verify:** `manifest.py verify …/D5Pa/ticket …/MANIFEST_D5Pa.txt` returns `verify: OK MANIFEST 9a70be48ffe0111214b5d8e67de37b9604ae7f7edd67d458fc45f6e66541bf1d`, rc=0. Re-freezing with `MANIFEST_D5Pa_EXT.txt` gives the same digest.
- **Difference from R3r2:** only the two ticket rows and the swap of the two EXT reader paths for their staged copies.

## Notes that do not block (outside PURE's scope)
1. **NA_DROP conflict.** The NA_DROP stage's `ticket/Theory_work/Wave3/W3-D5P/STATEMENT.md:96` still says "on an exact-branch run". Its manifests also pin live L2, card and RV. Whichever stage lands second must carry a-1 over and re-freeze, or the narrowing will be undone.
2. **DEPS.tsv will go stale.** Unchanged by design, it keeps sha and checked_sha 5dc11132… for STMT-C1..C3 and b023caf… for LIST-CODE. After landing these no longer match the files (e3196041…, 60b391fd…). The recorder needs to update them, along with STATEMENT's changelog (no v1.1.3 row was added, to keep the line count) and the LIST-CODE version bump.
3. **The same rate sentence without "p ≥ 2" also sits in the ticket's own proposal files.** These are `W3-D5P/CARD.md:10` and `READER_DELTA.md:29`. Sol cited only the W3-READER copies. A later reviewer could flag them, so HQ may want to decide whether to align them.
4. **The REPORT summary has a related loose wording.** REPORT's LIST-CODE `conclusion:` says "exact branch: …" without "status exact", which is (iv)'s content. It is not part of this correction.

PURE-VERDICT: PURE
