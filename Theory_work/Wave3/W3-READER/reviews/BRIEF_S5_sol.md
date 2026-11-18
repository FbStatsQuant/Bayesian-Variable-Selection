# BRIEF — S5: Sol diff read of the S4 repairs, W3-READER (2026-11-16)

Fresh independent reviewer (Sol, effort high, one pass). Worktree `/home/fb31/BVS-wt/W3-READER`, branch `theory/W3-READER`
at HEAD (≥ 8676f5f9). **Write exactly one file:** `Theory_work/Wave3/W3-READER/reviews/S5_diffread_sol.md`. No other writes,
no git state changes, no TMPDIR, nothing outside the worktree; scratch only in `/home/fb31/BVS-wt/W3-READER/.rc_tmp/`,
deleted after (D62). No sub-agents.

## Inputs
- S4 findings: `Theory_work/Wave3/W3-READER/reviews/S4_statement_change_sol.md` (S1, C1, F1, S2, F2, E1, S3).
- The repair diff: `reviews/S5_input/DIFF_S4_repairs_c219065b_to_8676f5f9.diff` (verify `sha256sum -c reviews/S5_input/MANIFEST_S5.txt`);
  equivalently `git diff c219065b 8676f5f9 -- Theory_work/Wave3/W3-READER/`.
- Current files at HEAD: `Theory_work/Wave3/W3-READER/{CLAIMS_CARD,READER_VERSIONS,REPORT}.md`, `lemmas/R3_*.md`, `lemmas/R4_*.md`.
- Sources named in S4 (registry `Theory_work/INFRA/registry/claims.tsv` at HEAD; W3-POST2/STATEMENT.md :103-115; W3-SCR-R2
  READER_DELTA §5 at theory/W3-SCR-R2 048b6b23, path `/home/fb31/BVS-wt/W3-SCR-R2/Theory_work/Wave3/W3-SCR-R2/reviews/READER_DELTA.md`;
  F-UNI narrowing `/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/FUNI_NARROW/`).

## Tasks
1. For each S4 finding, say RESOLVED / PARTLY / NOT RESOLVED, with file:line at HEAD; check the repair is faithful to the
   cited source and introduces no new defect (statuses verbatim with full "conditional on" lists; no internal ids in
   reader-facing sentences; asymptotics not framed as a limitation; no n₀-size remarks beyond the mandated code-limit sentence).
2. Check every changed line in the diff for new errors (D71: judge each new or changed interpretive sentence).
3. **Grep check:** no reader text (READER_VERSIONS, CLAIMS_CARD, NOTATION, METHOD_INTUITION, lemmas, REPORT) claims every-n
   delivery / completion under plain IDEAL-W (without A:IDEAL-W⁺ or the domain 𝔇). Report the grep you ran and its hits.
4. Confirm the tags of the repaired statements.

## Closing lines (exactly)
```
S4 FINDINGS: ALL RESOLVED | <list not resolved>
NEW DEFECTS: NONE | <list>
PLAIN-IDEAL-W EVERY-n: NONE | <hits>
FIDELITY: FAITHFUL | NOT-FAITHFUL
VERDICT: PASS | FIXES-NEEDED
```
