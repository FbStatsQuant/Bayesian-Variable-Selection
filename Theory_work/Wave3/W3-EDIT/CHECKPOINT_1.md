# W3-EDIT — CHECKPOINT_1 (final) — 2026-11-15 21:54 CST

Branch `theory/W3-EDIT` at the commit that adds this file. It has merged origin/main 86191e1; main's later commit 1810eca touches
none of the edited files. Ledger: `LEDGER.tsv`, 113 rows. Editorial only (v4 §0.1). Routes follow the manager's
decision (a)+(b) and its C-DLV correction. HOLDS on origin/main: none (re-read 21:53 CST).

## 1. Ledger summary
| route | rows | what |
|---|---|---|
| IN-PLACE (applied) | 29 | item 6 C6-01..11 (C-MIS cites, citecheck fixes; already on main, 66b67f7); item 7 E7-01 (02_method.tex:452); PSHARP E1, E2, E4, E5, E6, E8, E9 (REPORT, PLAN); MISR S1, S2, F5, X1 (ASSUMPTION_MAP :17 :27 :41 :54, REPORT :76, N5 docstring); START2 E1, E2, E6 (REPORT); MINOR M17 (W2-APP L4_families:145), M45 (W1-N3 LFP:63), M47 (W1-PXN CR_corr_tails:46) |
| CHAPTER-ONLY, to a rider | 11 | see §4 |
| CHAPTER-ONLY, Writing Dept | 1 | M03 (W1-N1 L2_post_terminal:20, cite KERNEL rows 1–5 + T12) |
| NO CHANGE | 10 | START2 E8 (done in CP2 §6); 9 MINORs that rest on material missing from the audit bundle (M18, M19, M33, M36, M38, M43, M52, M66, M68) |
| NOT-EDITORIAL, not applied | 62 | see §5 |

## 2. Editorial-only diff check
- **S1, Sol gpt-6.1-sol high** (`reviews/S1_editorial_check_sol.md`): `EDITORIAL-CHECK verdict=FAIL rows=29
  changes_math=0 incorrect=1`. 28 rows EDITORIAL. **No hunk changes mathematics**; no orphan or missing edits. The one
  INCORRECT row (I4-S1) left "weakenable, not removable" at W3-MISR ASSUMPTION_MAP:17 (S). Plus E1 (a wrong ledger
  note). Both accepted and applied in c870ccc (`reviews/S1_disposition.md`).
- **S1b re-check of that one line, fresh Opus 5.5 high** (overnight rule: Codex congested;
  `reviews/S1b_recheck_opus.md`): `RECHECK verdict=PASS S1=RESOLVED math_changed=NO`: the text is identical to Sol's, no remaining overclaim, no W3-MISR statement, lemma, proof or numerics file changed. Out-of-scope note: ASSUMPTION_MAP:54 and REPORT:76 keep "weakenable" (no non-removability claim; not a finding).

## 3. Recording (HQ recorder)
Item 6 is already on main: citefix + rehash of C-MIS:Thm-MIS(i), Thm-MIS(ii), Cor-N → 1.0.1 (66b67f7), then PR #10
(86191e1). This branch has merged origin/main (98ccc5f; merge, not rebase). One row is left for
`registry.py rehash --bump patch`:

| claim id | file | old sha256 (claims.tsv) | new sha256 | lines touched | ledger rows |
|---|---|---|---|---|---|
| W1-PXN:CR.R-prime | Wave1/W1-PXN/lemmas/CR_corr_tails.md:42-51 (premises :9, :12-15) | 3aea15c16d21f6cb7b38b2ac4993e1e281e30bb8b53bf87070caa07ec292f306 | 04f39068fc4f6d69d90c80810e31af74df11fa08887dc12e2492c274decd33e2 | 46 | I1-M47 |

`check.py --quiet` on this branch vs origin/main: the only new finding is that 1 `C2-changed` ERROR (468 claims; 1 ERROR,
296 WARN, 159 INFO on the branch; main has 0 ERROR and the same WARN/INFO). `assemble --check`: current. Every other
edited file is outside all registered spans; `02_method.tex` has no registry row. CI (`run_ci.py --steps
check,paper,cite`, TMPDIR in SMC_Theory_Department/ci) on HEAD: cite PASS (25/25), paper PASS, check FAIL on that one
row only. So the rehash goes in the same merge.
Diff vs main: 10 files (02_method.tex; W1-N3 LFP; W1-PXN CR_corr_tails; W2-APP L4_families; W3-MISR ASSUMPTION_MAP,
REPORT, N5 docstring; W3-PSHARP PLAN, REPORT; W3-START2 REPORT). The grep of all 4 rider folders (ticket-relative paths
and basenames) found no rider citing any of these files.

## 4. CHAPTER-ONLY, grouped by parent → rider (absorb in the delta where the clause is restated; else post-freeze IN-PLACE after the rider's CP3 + merge)
- **W3-PSHARP → W3-PSHARP-R:** I3-E3 (STATEMENT:73, Cor A1 domain remark); I3-E7 (ASSUMPTION_MAP:16, inside rows 9-17 used by TARGET.md:7).
- **W3-MISR → W3-MISR-R:** I4-F2 (STATEMENT:231-234 statuses in full); I4-F3 (M_misr.md:78 citation); I4-F4 (STATEMENT:8 changelog wording).
- **W3-START2 → W3-START2-R:** I5-E3 (P1_LEADING:16-17 typo); I5-E4 (STATEMENT:108); I5-E5 (STATEMENT:205-206 cite); I5-L0 (STATEMENT:86-88 LEAK-0 "sharpens" → only the partition-free 𝔏⁰).
- **C-DLV + W2-UNI → W3-RM2-R:** I2-01 (L4_delivery:83-84, Prop-F → Sol's R-AUD1 restatement; reverted 78d18c5); I1-M25 (W2-UNI L5_delivery:32-33, cite the inline pathwise step, not Cor D′).
- **No rider (Writing Dept, chapter transcription):** I1-M03.

## 5. NOT-EDITORIAL (not applied; for the manager)
- Council/sweep items: I4-F1 (MISR §3(a): new quantifier and constant relations), I5-E7 (START2 LEAK-0 hypothesis "(E)" → "the inequalities of (E) at n"), I4-R13 (MISR better-theorem).
- 59 API-audit MINORs (HQ: "claim unaffected"; each fills a proof step, fixes a constant or changes statement text,
  so v4 §0.1 keeps them out of this pass). Full triage table: `TRIAGE_MINORS.md`, with (iii) first and ★ for headline
  candidates (`HEADLINE_CANDIDATES.md`, recorder/staging-1115 ac5754d).
  - **(iii) could affect a stated hypothesis or conclusion: 20.** Six are ★: M61 (W1-GEN Thm-GEN(C4): "the
    conclusions of (C3)" include a rate L5.4 does not transfer), M35 (FAC-B (C1) lacks premise e4′), M27
    (F-UNI (S) needs "eventually"), M30 (SAMP "no output certifies" label), M57 and M58 (POST J_n(c) sub-clause; raw-scale
    parenthetical). The other 14: C-DLV M05 M08 M10 M11 M13; W2-APP M16 (stale Family-map cell inside a registered span)
    and M59; FAC-PK M37 (unproved liminf identity); FAC-XA M69 M70; UNI M23; C-ENG M48; C-PACK M50 M55.
  - **(ii) real local proof slip, claim unaffected: 30** (one-line fix + line check; 8 ★: N1 M01 M02, GROW M14, POST
    M56, FAC-B M34, FAC-X M39 M40, SAMP M31).
  - **(i) wording only, an E finding after all: 9** (M12, M15, M26 ★, M29, M32, M42, M44, M64, M73).
  - Nothing applied; routing is the manager's.

## 6. Process notes
- Revert: e1988ea (C-DLV) and the E7 part of 92124b5 (PSHARP ASSUMPTION_MAP), restored by the new commit 78d18c5. My first rider cross-check grepped only full repo paths; the redo grepped ticket-relative paths and basenames.
- Hand-typed timestamps (LOG line 3, CITEFIX header, two manager messages) are flagged in LOG.md; all stamps now come from `date`.
- Agents: H1 (Sonnet 5.5 high, Claude Third: MINOR extraction, bookkeeping only); S1 (Sol gpt-6.1-sol high: diff check);
  S1b (Opus 5.5 high, Claude Third: one-line re-check, overnight rule). All three have finished and are settled. Briefs and
  replies are in `reviews/`.

## 7. Addendum (2026-11-15 21:56 CST): manager's CP1 answer (manifest-impact check)
Four accepted council manifests list in-place files: W2-APP MANIFEST_PC1 (L4_families.md); W3-MISR MANIFEST_R1/R2
(ASSUMPTION_MAP, REPORT, N5 script); W3-PSHARP MANIFEST_R1/R2 (PLAN, REPORT); W3-START2 MANIFEST_R1 (REPORT). I checked
this myself against every MANIFEST_* on origin/main. Those 15 rows are now **POST-FREEZE (manifest)**: still applied on
`theory/W3-EDIT`, held from the merge until the manifest re-freeze / EXT-at-freeze batch. **Merge now** (branch
`theory/W3-EDIT-now`, cut from origin/main): 02_method.tex (E7-01), W1-N3 LFP:63 (M45), W1-PXN CR_corr_tails:46 (M47), and
this folder. Routes now: 14 IN-PLACE (11 of them already on main), 15 POST-FREEZE, 12 CHAPTER-ONLY, 10 NO CHANGE,
62 NOT APPLIED. The rehash row is unchanged (W1-PXN:CR.R-prime).
