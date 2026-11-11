# Decision log

Every SUPERSEDE / COEXIST / DECLINE / REMARK decision, every RETRACT / NARROW / DEPRECATE, and every failed
sharpening attempt (a failed attempt to remove or weaken an assumption counts as weak necessity evidence). Rules:
`LIFECYCLE.md` §5. `propagate.py` appends entries automatically; the human rationale goes into the PR that carries
the registry change. Newest entries at the bottom. Format:

```
## <date> — <KIND> <X> [/ <Y>]
- decided by: Felipe | HQ
- reason: ...
- axes (Y vs X): assumptions=…, conclusion=…, rate=…, scope=…
- class / price / key-step check / restored / failed removal count ...
```

## Seeded entries (narrowing decisions already taken inside Wave 1C–2 tickets; recorded 2026-11-09 by INFRA)

## 2026-11-09 — NARROW (historical) W2-FAC-A:Thm-FAC-L
- decided by: the ticket under the wave protocol, flagged to HQ (REPORT flag 1)
- reason: proved for one global factor + bounded local blocks under limsup log p/log n < α₀(κ̄) (= 1/6 for block
  compound symmetry), not for p ≤ n^A; Proposition SHARP shows 1/6 is optimal for the full-lattice route
- source: Theory_work/Wave2/W2-FAC-A/REPORT.md:3-8

## 2026-11-09 — NARROW (historical) W2-FAC-X:Thm-FAC-CS-iid
- decided by: the ticket, flagged to HQ
- reason: Target 1 holds up to log p/log n < 1/2; uniform-over-n (C2)(ii) is false beyond 1/2; Cor FAC-NCS exact-Gram
  (G) branch withdrawn (imported multiplier bound false for exact Gram)
- source: Theory_work/Wave2/W2-FAC-X/REPORT.md:27; lemmas/X7_near_cs_loadings.md:3

## 2026-11-09 — NARROW (historical) C-MIS:Thm-MIS(i)
- decided by: the ticket ("narrowed form in §2")
- reason: target is the exact sparse projection S₀^𝒞 under (EP); examples E1–E3 show the alternatives fail
- source: Theory_work/Wave1C/C-MIS/REPORT.md:23

## 2026-11-09 — COEXIST (historical) C-DLV:Prop-F / W2-FAC-A:Prop-F-FAC, W2-LOC2:F-LOC2, W2-UNI:F-UNI
- decided by: HQ (delivery results proved per design class)
- reason: the Proposition F family is proved class by class (GROW class via HQ audit A2; FAC-A; LOC2; UNI); none
  implies the others, all are kept
