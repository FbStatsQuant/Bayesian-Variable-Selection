# Per-claim seat addendum — brief (HQ, 2026-11-12)

Rule: `Theory_work/INFRA/LIFECYCLE.md` §"Seat tables by addendum; carrier files" (INFRA R06, main c3cc7d0). You act as the
**same seat model** as the council seat whose review you complete, in a fresh thread. You do **not** re-review or
rescore. Your only job: for each claim id the ticket submits, decide whether that seat's existing review examined it,
and say where.

For each assigned review file:
1. Read the frozen manifest named in the review's `COUNCIL-VERDICT` line (`reviews/MANIFEST_<round>.txt`) and the review.
2. Take the claim ids from the ticket's CHECKPOINT_3.md registry blocks (W3-MISR: omit Rem-SNR, Rem-P, Rem-U).
3. Append to the END of the review file (never edit anything above it) exactly:

```
## Addendum — per-claim decisions (seat <seat>, round <round>; 2026-11-12; same seat model, fresh thread; no rescoring)

| id | decision |
|---|---|
| <TICKET>:<id> | ACCEPT |
...

Where examined: <one line per id: section/line of this review that examined it>
```
   Decision cells contain exactly `ACCEPT` or `NOT-EXAMINED` and nothing else. ACCEPT only if this seat's review
   examined that claim and raised no blocking finding against it. No second `COUNCIL-VERDICT` line. No other text in the
   table; the "Where examined" list goes below it.
4. Change no other file and no git state.
