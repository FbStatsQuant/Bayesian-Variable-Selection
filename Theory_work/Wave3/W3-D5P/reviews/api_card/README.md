# D5P1 — API blind-audit card for HQ: W3-D5P (track D #5′, list-restricted outputs on Theorem 6 designs)

**What it is.** A Message Batches card, prepared by the W3-D5P lead for HQ to submit (pattern: `API_AUDIT/audit1/` on
dept/theory). Claude Fable 5.2, effort high, as a blind referee of the three W3-D5P claims — LIST-K (list algebra),
LIST-CODE (code reading at core 4676af6: the two DIST links and the top store), LIST-R (the corollary on Theorem 6's data
event). Task, verbatim: **"Break the proof; findings only."** Each reply ends with one line per claim clause:
`AUDIT D5P1 <claim> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>` (9 lines: LIST-K, LIST-CODE.i–v, LIST-R.i–iii).
Two independent samples (identical input; the context block carries `cache_control`). No API call was made to prepare
this card, and no key was read.

**Blindness.** The referee sees, verbatim with original line numbers, taken with `git show <commit>:<path>` at one pinned
commit: the statement (without its header record and changelog), the three proof files, the SPEC carrier copy, the
consumed statements (RM2-R-plus/RM0-plus/DLV-0, RM objects and Form R, the RM2 code pins, C-DLV L4 pathwise step and
Lemma S.2, SAMP objects, CC2/CC5, Lemma POST, DIST-C, reader Theorem 6 and its bridges) and the cited code. Status
quotes, review markers and review-record lines are scrubbed; the builder **fails** if any of PROVED, CHECKED,
CODE-READ, council, PASS, VERIFIED, AUDITED, Opus, Fable, Astra, Sol, seat, LC1, SL1-, MANIFEST, REFUTED or
disposition survives in the context. Lines removed by the fallback are listed in `SCRUB_LOG.tsv` (all are status or
review-record lines; none inside a proof file).

**Files.** `d5p_card_build.py` (builder; `build [--commit <sha>]`), `SYSTEM.md`, `REQ_d5p.md` (context + task),
`requests.json` (audit_batch.py shape: `custom_id`, `file`, `claims`, `params`), `REQUESTS.tsv`, `MANIFEST.tsv` (sha256
of every source blob at the commit), `USAGE.txt` (offline cost estimate), `SCRUB_LOG.tsv`.
**Location.** Built inside the ticket's `reviews/` (outside the council manifest, so the frozen content is untouched).
HQ may copy the folder to `Theory_work/Wave3/API_AUDIT/d5p1/` on dept/theory; the builder reads only git blobs, so the
copy rebuilds byte-identically with `--commit` set to the commit recorded in `MANIFEST.tsv`.

## How HQ submits (run from the repo root; same commands as audit1)
```
python Theory_work/Wave3/API_AUDIT/audit_batch.py count  <card dir>   # free token count + cost
python Theory_work/Wave3/API_AUDIT/audit_batch.py submit <card dir>   # writes batch_id.txt
python Theory_work/Wave3/API_AUDIT/audit_batch.py wait   <card dir>   # results/, USAGE.txt, VERDICTS.tsv
```
`wait` collects the lines starting `AUDIT ` into `VERDICTS.tsv` directly (this card's verdict lines start with `AUDIT D5P1`).

## Cost (estimate)
See `USAGE.txt`: ≈ 45k input tokens per request, 2 requests → ≈ $0.36 input; ≈ $0.64 output expected, ≤ $1.28 worst case
at the Fable 5.2 batch rate ($4 / MTok in, $20 / MTok out). **Total ≈ $1.0 expected, ≤ $1.7 worst case.**

## Pin
The card is rebuilt at CP3 on the commit of the passing council round (the committed files are that build); until then
any build in this folder is a draft.
