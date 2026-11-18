# W3-DIST — diff check D6 (one clause after D5, and the `uses` column of six DEPS rows) — gpt-6.1-sol, codex, reasoningEffort high

You are an independent checker, new to this ticket. Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/` (paths below are relative to it). **Read-only except your one output file
`reviews/D6_sol_diff.md`.** Run no git command that changes state; start no agents; no cluster jobs; any computation small
and `nice`. **Do not write any file outside the repo clone and set no TMPDIR.** Prefer inline computation with no files;
if you need scratch, use only `/home/fb31/Bayesian-Variable-Selection/.rc_tmp/W3-DIST-D6/` (never inside the ticket folder,
never `/tmp`) and delete it at the end. Never run a command that asks for an approval. This is a very short task. The
exact diff is `reviews/DIFF_D6.patch`.

1. `lemmas/DIST12.md`: the diff check `reviews/D5_sol_diff.md` raised **D5-01 (MINOR)**: a bracketed remark identified A
   with log p_raw/log n although the setting assumes only p_raw ≤ n^A. The lead deleted the equality. Resolved? Is the
   sentence correct as it now reads, and is anything else in the file changed since the version D5 checked
   (sha256 first 16 hex: a786d3fc80069520)? Give the verdict for the file as it now stands (DIST-1, DIST-2), taking D5's
   verification of everything else as given.
2. `DEPS.tsv`, column `uses`, rows S, V, X, X', NEC and TC/DIST-3: each now names the exact items of the locked proof
   [P1] = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`
   that its proof file cites (`work/C_size/S.md`, `work/C_size/V.md`, `lemmas/X.md` §0–§8 and §9, `lemmas/NEC.md`,
   `work/B_transfer/DIST3.md`). For each row: is every item listed really cited or used in the file, and is any [P1]
   item that the file cites or uses missing from the row? (Search the files for `lem:`, `thm:` and "[P1]".)

Output (`reviews/D6_sol_diff.md`): first line `D6 diff check — lemmas/DIST12.md <16 hex>; DEPS.tsv <16 hex>`. Findings with id
(D6-xx), severity, place, the error, minimal repair. Verdict lines: D5-01 RESOLVED / NOT RESOLVED; `lemmas/DIST12.md`
(DIST-1, DIST-2): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED; per DEPS row (six): CORRECT / give the corrected
list. Final line: overall verdict. Say exactly what you could not check.
