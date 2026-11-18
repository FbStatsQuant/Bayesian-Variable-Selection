# H1: brief for the bookkeeping helper (Sonnet 5.5, effort high, Claude Third). Extraction only, no judgement

You are a bookkeeping helper for the W3-EDIT editorial ticket. Work in the git worktree `/home/fb31/BVS-wt/W3-EDIT`
(read only, except for the single output file named below). Do not edit any other file. Do not commit, push, stash or
change branches. Python 3.13 is at `/home/fb31/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13`.

## Task
List every MINOR finding of the API audits, verbatim, with the current text at the location each finding cites.

Sources, all under `Theory_work/Wave3/API_AUDIT/`:
- `pass1/results/f*.md`: the claims marked VERDICT=MINOR in `pass1/VERDICTS.tsv`, **except** requests f17, f18, f26.
  Those three are superseded by `pass1b/results/f17.md`, `f18.md`, `f26.md` (use the MINOR claims in
  `pass1b/VERDICTS.tsv`).
- `pass2/results/f*.md` (MINOR claims in `pass2/VERDICTS.tsv`) and `pass2b/results/f00.md` (MINOR claim
  W1-GEN:Thm-GEN(C4) in `pass2b/VERDICTS.tsv`).
- `pass3/results/f*.md` (MINOR claims in `pass3/VERDICTS.tsv`: W2-FAC-A:Lemma-GAP, W2-FAC-PKA:L4, W2-FAC-X:X9,
  W2-FAC-XA:L2, W2-FAC-XA:L8-S).

The expected total is 39 claims (21 + 13 + 5). Findings appear in several formats: `1. **MINOR — file:line.**`,
`Finding (MINOR), file:line:`, `**Finding 1 — MINOR — file:line.**`, and others. Read each result file's section for
the claim (`## <claim id> ...`) and take every finding labelled MINOR there. If a request file covers several claims,
attribute each finding to the claim whose section contains it. If a MINOR claim's section has no labelled finding,
record one row with finding = "(no labelled finding; verdict-only)" and quote the 1–3 sentences that justify the
verdict. Ignore findings labelled OK, NOTE or observation unless the section calls them MINOR.

For each finding:
1. Resolve the cited `file:line` to a repo-relative path. Files are usually relative to the claim's ticket folder;
   the ticket folder is the `file` column of `Theory_work/INFRA/registry/claims.tsv` for that claim id.
2. Copy the current text of those lines (at most 400 characters; mark a cut with `…`).
3. If the line no longer matches what the finding describes, say so in `notes`.

## Output
Write exactly one file: `Theory_work/Wave3/W3-EDIT/reviews/H1_minors_extract.tsv`. It is tab-separated, with header
`n	pass	request	claim	finding_verbatim	cited	resolved_path:lines	current_text	auditor_repair	notes`.
`finding_verbatim` is the full finding text, with newlines replaced by ` / ` and tabs by spaces. `auditor_repair` is
the auditor's proposed fix, quoted, if it gives one; otherwise empty.

Then reply with: the row count; rows per pass; any claim with no labelled finding; any cite you could not resolve.
Do not classify findings and do not judge whether they are right.
