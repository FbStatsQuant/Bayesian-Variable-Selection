# API audit pass 3 — HQ triage (2026-11-11)

Batch msgbatch_017Qeq255ojPUvhjEePbobwf, Fable 5.2 effort high, blind; 40 requests, 50 author-only PROVED W2-FAC-*
claims (stopped factor-design tickets). Usage ≈ $16.15.

| verdict | claims |
|---|---|
| OK | 42 |
| MINOR | 5 — W2-FAC-A:Lemma-GAP, W2-FAC-PKA:L4, W2-FAC-X:X9, W2-FAC-XA:L2, W2-FAC-XA:L8-S |
| GAP | 3 — W2-FAC-S5F:L0 (f20), W2-FAC-S5F:L1 (f21), W2-FAC-X:L4r.5 (f23) |

GAPs: missing hypotheses / event lower bound / constant relation, each with a stated local repair. HQ registry check:
no consumer outside the two tickets (only W2-FAC-S5F:C1, C4, which are open), no chapter use; both tickets are on the
PROGRAM stop list. → Sol confirmation R-AUD2 (BRIEF_RAUD2_sol.md), then rule 11 if confirmed.

## Disposition (HQ, after R-AUD2 Sol)
Sol: S5F:L0 F1, F2 CONFIRMED; S5F:L1 F1, F2 CONFIRMED; FAC-X:L4r.5 F1 CONFIRMED, F2 CONFIRMED-WORDING. Consumers: S5F
C1–C4 (C2/C3 via local `L0; L1` notation) + two FAC-X ticket summaries (STATEMENT_T2.md:64–72, T2/NOTES.md:27) need
the bulk/static qualifications. No PROVED-CHECKED claim, no FINAL chapter statement affected. Rule 11 applied:
`propagate.py suspect` on the three lemmas (S5F C1–C4 + L1 → SUSPECT; issues under INFRA/issues/2026-11-11_suspect_*).
No running ticket consumes them, so no notifications. Repairs not scheduled (stop list); the issue files carry Sol's
repairs for whoever reopens the route.
