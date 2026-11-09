# Transcription brief: claims-registry fragments (helpers)

You transcribe — you do not judge mathematics. Work ONLY in the git worktree `C:\Users\felip\BVS-infra`
(branch theory/infra). Read-only everywhere except your two output files. No git commands. Effort: be efficient —
use grep (`grep -n "^#\|Theorem\|Lemma\|Proposition\|Corollary\|Status\|PROVED\|STATUS"`) to locate statements and
status lines; read only the spans you need; do not read numerics data files or long proofs end to end.

## What counts as a claim
Every named theorem, lemma, proposition, corollary, counterexample, obstruction/negative result (e.g. "Proposition
SHARP", "Theorem NEG", "Lemma VN"), and — for HQ_AUDIT files — the audit verdict, in the tickets assigned to you.
Sources: `REPORT.md` (status per clause, review trail, council scores), `STATEMENT.md` (locked target), `lemmas/*.md`
(one or more claims per file), `CHECKPOINT.md` only if there is no REPORT. Sub-clauses (a)-(e) of one theorem are
ONE claim unless the REPORT gives them different statuses — then one claim per clause (local ids like `Thm-GEN(C6)`).
Do not invent claims for definitions, remarks, or numerics.

## Output 1: `C:\Users\felip\BVS-infra\Theory_work\INFRA\registry\fragments\<BATCH>.jsonl`
One JSON object per line (UTF-8, keep unicode like ♯, 𝔉 as is). Keys (all required; use "" or [] when absent):
- `ticket`: e.g. "W2-FAC-A" (HQ audits: "HQ_AUDIT-W1C" or "HQ_AUDIT-W2"; Wave1C FINAL chapter: "W1C-FINAL").
- `local_id`: short ticket-unique id, no spaces, chars `[A-Za-z0-9._()'+-]`: "Thm-FAC-L", "Prop-SHARP", "L3", "Cor-E",
  "Thm-GEN(C6)", "A1". Use the source's own label (L1 for `lemmas/L1_*.md` etc.).
- `kind`: one of theorem | lemma | proposition | corollary | counterexample | obstruction | audit | implementation.
- `name`: the label verbatim as in the source ("Theorem FAC-L", "Lemma L2 (sandwich)").
- `short`: ≤ 160 chars, plain-language summary of what is claimed (scope included: class, p range, law).
- `file`: repo-relative path (forward slashes, starting `Theory_work/`) of the AUTHORITATIVE statement text:
  STATEMENT.md for the ticket's main target(s); the lemma file for lemmas; the audit file for audits.
- `lines`: [start, end] 1-based inclusive, covering exactly the statement (its heading/label line through the last
  line of the statement), NOT the proof. Verify by printing the span (`sed -n 'S,Ep' file`) before writing it.
- `status`: VERBATIM status words as the ticket records them for this claim (e.g. "PROVED-CHECKED",
  "PROVED (by this seat, unchecked)", "VERIFIED-WITH-AMENDMENTS", "PARTIAL", "OPEN", "COUNTEREXAMPLE (...)"). Never
  upgrade. If the claim has no own status anywhere, put "" and explain in `notes`.
- `status_source`: "path:line" where that status is written (usually REPORT.md §1/§3 or the lemma header).
- `evidence`: list of strings "reviews/<file>: <verdict verbatim>" for reviews that checked THIS claim (statement
  lock, lemma check, sweep, council, citecheck), paths relative to the ticket folder.
- `council`: council scores verbatim if the claim is covered by a council ("Sol 9.2 / Opus 8.9, round 1"), else "".
- `depends_on`: logical dependencies the proof uses: same-ticket claims by local_id ("L2"); other Theory_work
  tickets as "<TICKET>:<local_id>" (e.g. "W1-GEN:Thm-GEN", "C-GROW:Thm-GROW"; guess the obvious local_id); results
  from the State-of-Project / older archive as "EXT:<name verbatim>" (e.g. "EXT:T03♯", "EXT:M5(0)", "EXT:T12",
  "EXT:T22", "EXT:Proposition F", "EXT:TH09"). Take them from the proof map / "uses" lines / REPORT; do not guess
  beyond what the files say.
- `method`: method version the claim is about, verbatim (e.g. "v3.1 as merged, main 4676af6"), else "".
- `falsification`: list of numerics scripts that the lemma file / reviews / LOG explicitly name as this claim's
  numerical falsification check, as repo-relative paths (e.g. "Theory_work/Wave2/W2-FAC-A/numerics/fu_check.py"),
  plus the command if one is given (`"script | cmd"`). [] if none named.
- `notes`: narrowings, scope flags, "statement changed vs card", open amendments — ≤ 300 chars.

## Output 2: `C:\Users\felip\BVS-infra\Theory_work\INFRA\registry\fragments\<BATCH>_routes.jsonl`
Failed routes / obstructions recorded in your tickets (routes shown not to work, counterexamples to a route, STUCK
lemmas, refuted targets, "this route cannot go further"). One object per line:
`{"ticket","route","why_failed","evidence":"path:line","claim_local_id": "<local_id or ''>"}` (≤ 300 chars each).

## Finish
Validate: `python -c "import json;[json.loads(l) for l in open(r'<file>',encoding='utf-8')]"` for both files.
Final message: number of claims and routes per ticket, and anything ambiguous (≤ 15 lines). Do not paste the files.
