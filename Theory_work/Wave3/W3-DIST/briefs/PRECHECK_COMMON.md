# W3-DIST — common rules for same-family pre-checks (Claude Opus 5.5, Claude Third, effort high)

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/`. **Read-only except the one output file named in your brief.** Run no git command, start no
agents, effort high at most. A pre-check is a filter before the cross-family line check; it is not a review layer.
- The statements to be proved are in `STATEMENT.md` (v1.3.1; §0 setting and interfaces, §1–§2 master theorems, §1R reader
  versions, §3 lemmas and bridges) with `API_CARDS.md` "Common definitions". They are targets fixed by HQ.
- Check every line of the proof files named in your brief: each inequality, each constant and its dependence, each
  probability bound and its event, each citation (does the cited statement exist, with its hypotheses met?), the
  uniformity claims (one n₀; constants depending only on the listed quantities), and the edge cases (s₀ = 0, p = 2,
  p ≤ window, singular Gram matrices, columns constant in the sample, sets outside Ω). Recompute the key steps.
- Does the file prove exactly the statement in STATEMENT.md? Assess every "STATEMENT-CHANGE REQUEST" in the file:
  justified or not, and whether it weakens the statement.
- Comparison material named in your brief (independent attempts at the same lemma, unchecked) is for locating
  discrepancies; it is not authority. Where two derivations disagree on a step both need, say which is right.
- Do not read `reviews/`, `LOG.md`, `CHECKPOINT_*.md`, `DEPS.*` of the ticket.
- Output: findings with id, severity (CRITICAL / MAJOR / MINOR / NIT), file and section, the error or gap in full, the
  minimal repair; a verdict per lemma or section: VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED; a final overall
  verdict line. Do not soften findings; if you could not check something, say exactly what.
- **Compute discipline (POLICIES §12).** No files in /home/fb31 outside the ticket folder; any job on Owls runs under `nice`
  with at most 16 cores, nothing large or multi-day; temp files are removed when done (/tmp is on a nearly full root
  disk); numerical arrays stay in a git-ignored folder of the ticket and are not copied elsewhere.
- **Temp convention (POLICIES §12 rules 8–9; /home/fb31/SMC_Theory_Department/INDEX.md).** Temporary files never go in `/tmp`.
  Prefix shell commands that write temp files with
  `export TMPDIR=/home/fb31/SMC_Theory_Department/tmp/<YYYYMMDD>-W3-DIST-<what>; mkdir -p "$TMPDIR";` and remove that folder
  when the job ends. Repo files stay in the ticket folder.
