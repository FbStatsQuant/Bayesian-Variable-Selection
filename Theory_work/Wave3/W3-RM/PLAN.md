# W3-RM — PLAN

Target: `STATEMENT.md` (C0)–(C5). Pipeline per `Theory_work/Wave3/PROTOCOL.md`.

## Proof architecture
1. **RM-0 (core)**: GROW L1 (descent, exact move count) + DLV pathwise claim + E4. File `lemmas/L0_core.md`. No new
   mathematics; the only change is that e4 is a lemma.
2. **Form F**: `lemmas/L1_fixed.md` — (B1) partition-free ⇒ block-relative (quantifier check); (B2) GROW L3 re-read for
   log|Q| = o(log n) (list every use of |Q| ≤ C log n); (B3) TL with BM-Q (delta to GROW L2.1 / LOC2 L0′); (B4) cite.
   `lemmas/L2_NAF.md` — **new** Lemma NA-F (approximate direction count), (N-loc) ⇒ (N-D)(i).
3. **Form R**: `lemmas/L3_SANDR.md` — **new abstraction** SAND-R: audit GROW L6.2–L6.5, APP L3.2–L3.5, LOC2 L4 A.1–A.4,
   UNI L2 §3–§6; list every population input; show each follows from (FL-R), (V-R), (L-R). Hardest new step:
   **parallel prover** (Codex gpt-6.1-sol, high), then cross-family check (Opus 5.5 on claudeAgent).
   `lemmas/L4_formR.md` — (B8) (D-loc) ⇒ (R1)–(R3); (B9); assembly (C2).
4. **E4**: `lemmas/L5_E4.md` — code-level proof with file:line citations (main): enumeration path = N3(a) (code
   identity by diff against the frozen v2.2.1 routine); fallback path = direct invariant argument (tight path with
   codes in arg ⇒ maximiser), independent of TDP-E's lex claim; integration at `v3_core.cpp:469-476`.
5. **Examples** `lemmas/L7_examples.md` — (B10) and the table. **Sharpness** `SHARPNESS.md`.

## Reviews (each a new delegate task, briefed to break)
| step | reviewer | input |
|---|---|---|
| R01 statement lock | Codex gpt-6.1-sol high | STATEMENT, PLAN, source pointers |
| R02 "better theorem" | Codex gpt-6-astra high | STATEMENT, ASSUMPTION_MAP only |
| N-series numerics | Sonnet 5.5 on claudeAgent | spec `numerics/SPEC.md` |
| R03 lemma check L0, L1, L2 | Codex gpt-6.1-sol high | lemma files |
| R04 lemma check L3 (SAND-R) | Opus 5.5 on claudeAgent (cross-family to the Sol prover) | L3 + sources |
| R05 lemma check L5 (E4, code) | Codex gpt-6.1-sol high | L5 + code |
| R06 mid-point | fresh Codex gpt-6-astra high | STATEMENT + lemma files only |
| R07 exhaustive sweep | Codex gpt-6-astra high | everything |
| C1 council | gpt-6-astra high + Opus 5.5 high (claudeAgent) | everything |

## Sharpness gate (before heavy proving)
`ASSUMPTION_MAP.md` + boundary-violation numerics (`numerics/`): V1 masked truth; L1 leakage count beyond log n /
polylog; L2 gain just above η_A; N1 adversarial lattice (NA(𝓛) fails, does LS0 still reach S₀?). + R02.
Outcome recorded in LOG.md and REPORT; HQ decides on strengthening.

## Risks
* SAND-R abstraction: a hidden geometric input in the delta chain. Mitigation: explicit inventory, two families of
  reviewer, numerics on a non-metric design satisfying (L-R) (block-diagonal one-factor groups).
* NA-F: the remainder must lie in span X_{Q∪{l}} for the χ² charge; stated in (N-D)(i).
* E4: floating point is outside EX-A; state it as such (N3 (e), PACK UM-FP).
