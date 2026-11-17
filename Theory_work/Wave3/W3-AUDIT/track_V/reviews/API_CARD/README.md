# AUDITV — blind Fable review of track V item V1 (Lemma VIS: visibility with a margin uniform in n)

**What it is.** A Message Batches card, prepared by Theory Dept (2026-11-17) for HQ to submit, in the pattern of
`Theory_work/Wave3/API_AUDIT/audit1` and `track_A_W/API_CARD`. Claude Fable 5.2, effort high, acts as a blind referee of
Lemma VIS (`track_V/V1_VIS`, v1.4 as bound in council round V-R3). Two independent samples (`auditV-s1`, `-s2`). No API
call was made to prepare it; no key was read.

**Blindness.** The referee sees, verbatim with file:line: the V1 statement and proof (changelog cut), the reader versions
of Theorems 5, 6, 10 and the notation (main 029bb748), dossier B8, track C's table and design definitions. Reviews, logs,
checkpoints and CHECK files are withheld; status words are replaced by `[status omitted]`; the builder fails if any
survives. Task: "Break the lemma; findings only." One line per item: `AUDITV <item> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>`.

**Items (8).** V:VIS-0, V:VIS-a, V:VIS-b, V:VIS-c, V:VIS-d, V:VIS-e (the clauses), V:UNIF (uniformity in n, not "almost
every θ" at each n), V:SCOPE (which designs are inside by which route).

**Files.** `SYSTEM.md`, `REQ_V.md` (exact user message), `requests.json` (audit_batch.py shape), `REQUESTS.tsv`,
`MANIFEST.tsv` (sha256 of every source blob), `USAGE.txt`, builder `build.py`
(`python3 -I Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD/build.py build <commit>`; built on 7df2d81c).

## How HQ submits (run from the repo root)
```
python Theory_work/Wave3/API_AUDIT/audit_batch.py count  Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD
python Theory_work/Wave3/API_AUDIT/audit_batch.py submit Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD
python Theory_work/Wave3/API_AUDIT/audit_batch.py wait   Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD
```
The `AUDITV …` lines are in `results/*.md` (grep `^AUDITV `).

## Cost (estimate)
≈ 12.1k input tokens per request; 2 requests ≈ $0.10 input; output ≈ 20k tokens/request ≈ $0.80; worst case at
max_tokens 128000 ≈ $5.12 output. **≈ $1 expected, ≤ $5.3 worst case.**
