# AUDITW — blind Fable review of track A_W items W1 (ISL) and W2 (FRZ)

**What it is.** A Message Batches card, prepared by Theory Dept (2026-11-17) for HQ to submit, in the pattern of
`Theory_work/Wave3/API_AUDIT/audit1`. Claude Fable 5.2, effort high, acts as a blind referee of the two lemmas that
re-check, at the code of record 4676af6, the steps of `W1-N1:B` ((B-0), the control-flow clause of (B-b), (B-d)) and
`W1-N1:F` (freezing at general c) that `W3-SAMP:D` and `W3-SAMP:MR` use. Two independent samples (`auditW-s1`, `-s2`;
identical input; the shared context block carries `cache_control`). No API call was made to prepare it; no key was read.

**Blindness.** The referee sees, verbatim with file:line: the W1/W2 statements and proofs (changelogs cut), Lemma B and
Lemma F (older core), the older ticket's premises, T12's freezing lemma, the consumers' passages (Theorem D §1, Lemma MR),
and the code excerpts at 4676af6. Reviews, logs, checkpoints and CHECK files are withheld; status words are replaced by
`[status omitted]` and the builder fails if any survives. Task: "Break the lemmas; findings only." Each reply ends with one
line per item: `AUDITW <item> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>`.

**Items (9).** W:ISL-0, W:ISL-st, W:ISL-d (W1); W:FRZ-a, W:FRZ-b, W:FRZ-c, W:FRZ-d (W2); W:USE-D, W:USE-MR (the consumers'
uses). Map back: `W1_ISL/STATEMENT.md` clauses (ISL-0), (ISL-st), (ISL-d); `W2_FRZ/STATEMENT.md` (FRZ-a)–(FRZ-d); USE-D =
`Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md` §1; USE-MR = `Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md` Steps 2–4.

**Files.** `SYSTEM.md` (system prompt), `REQ_W.md` (the exact user message: context block, then task block),
`requests.json` (audit_batch.py shape: `custom_id`, `file`, `claims`, `params`), `REQUESTS.tsv`, `MANIFEST.tsv` (sha256 of
every source blob at its commit), `USAGE.txt` (offline estimate), builder `build.py`
(`python3 -I Theory_work/Wave3/W3-AUDIT/track_A_W/API_CARD/build.py build <items commit>`, byte-identical while the pins hold).

## How HQ submits (run from the repo root)
```
python Theory_work/Wave3/API_AUDIT/audit_batch.py count  Theory_work/Wave3/W3-AUDIT/track_A_W/API_CARD
python Theory_work/Wave3/API_AUDIT/audit_batch.py submit Theory_work/Wave3/W3-AUDIT/track_A_W/API_CARD
python Theory_work/Wave3/API_AUDIT/audit_batch.py wait   Theory_work/Wave3/W3-AUDIT/track_A_W/API_CARD
```
`wait` keeps only lines starting `AUDIT ` in `VERDICTS.tsv`; the `AUDITW …` lines are in `results/*.md` (grep `^AUDITW `).

## Cost (estimate)
≈ 28.8k input tokens per request (chars / 3.5); 2 requests ≈ $0.23 input; output ≈ 20k tokens/request ≈ $0.80;
worst case at max_tokens 128000 ≈ $5.12 output. **≈ $1 expected, ≤ $5.4 worst case.**
