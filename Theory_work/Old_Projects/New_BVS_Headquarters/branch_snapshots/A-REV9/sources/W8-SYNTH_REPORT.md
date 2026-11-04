# W8-SYNTH — REPORT

Branch `theory/W8-SYNTH`, created from `theory/campaign` at c9982a8. This is a synthesis task: it writes no new mathematics.

**Deliverables**
- `SYNTHESIS.md`: the full synthesis, eight sections.
- `BRIEF.md`: the executive version.
- `SNAPSHOT.md`: the head hash of every branch read.
- `digests/`: five per-group digests written by reading helpers. They are working material, not reviewed. Every load-bearing claim in SYNTHESIS was checked against the source file.

## 1. Headline

1. **No status was upgraded.** SYNTHESIS records every result with its author's status word. It also records the same-family (Claude) and cross-family (Astra) verdicts, and branch · file · label.
2. **The paper's masked-regime headline is fully proved only with LS0, and only same-family.** T38(b1-LH) is PROVED (same-family VERIFIED). Five no-LS0 candidates on LH now exist, none cross-family reviewed: W5-B2ENV, W5-VMASK, O-BGIBBS, F-SHARE and W7-SEP. So the claim "no masked theorem without LS0" in W4-T38FULL and W6-FIXREV1 is out of date. It is OPEN whether any of these routes survives review.
3. **At n = 200 the data settle the search question.** S-ELS, on the real ledgers: 0 search misses; S₀ was scored in every completed fit; the final local search never moved. All errors are posterior misses. No method change aimed at search can improve the study's numbers.
4. **Two task-level conclusions conflict with the earlier plan.**
   - The common-σ² start should be rejected (O-DILUTE, F-SIGMA).
   - W7-SEP refutes "tempering is needed"; the theory supports "moving off the start is needed".
5. **Inconsistencies.** Several cross-branch inconsistencies were found and are listed in SYNTHESIS §4:
   - the T32(i) status;
   - stale registry rows;
   - F-REFEREE not knowing about A-REV3/A-REV4;
   - n = 200 numbers that differ between sources;
   - label collisions.

## 2. Statements

None new. The statements of record that I recommend citing:
- **Thm 1:** `W6-FIXREV2 · STATEMENTS.md §1.2`.
- **Thm 3:** `W6-FIXREV2 · STATEMENTS.md §2.3` (Theorem A), with `W5-VPGD · REPAIRS.md R6.2` (W_Lat).
- **Thm 4, Prop 1, Prop 2, Thm 6:** `W5-LOCKBOOK · STATEMENTS.tex`.
- **Thm 5:** `W6-FIXREV1 · T38_STATEMENT.md`, plus the wave-5–7 updates listed in SYNTHESIS §2 and §8 task 6.

## 3. Proofs

None. This is a synthesis task.

## 4. Evidence

- **Sources read:**
  - every `origin/theory/*` branch's REPORT, REVIEW, REFEREE_REPORT, RESPONSE_PLAN, CARDS, ARCHITECTURE, STATEMENTS and REPAIRS file at the heads in `SNAPSHOT.md`;
  - `HQ/SR_AUDIT.md`;
  - the LEDGER up to the 20:16 UTC wrap-up.
- **Three branches moved during the run** and were re-read at their new heads: W7-SEP (858004e), W7-PART (b2aa940) and L-LEAN (d9c2f2c).
- **Not checked by me:**
  - I did not rebuild the Lean package. "0 sorry" rests on DECL_STATUS.md, AXIOMS_RECORD.txt and a grep.
  - I did not rerun any numerics.

## 5. What fails

- **The registry cannot be used as-is.** `S-REGISTRY` predates about 15 landings: see SYNTHESIS §4.14. It needs one rebuild before Felipe uses LOCKABLE for adoption.
- **The "n where the start turns favourable" cannot be stated as one number.** Three runs give three ranges with different definitions.
- **O-LS0's data could not be used.** There is no report, and the hash check shows 5/7 mismatches that nobody has interpreted.

## 6. Needs escalation

1. Felipe: the three decisions in SYNTHESIS §1, plus the output convention (§4.12).
2. HQ: run §8 tasks 1, 3 and 4 before any further proof work on Thm 5.
3. HQ: settle the W3-VT37R "233/234" claim against S-ELS (§4.6) with case IDs.
4. **Independent check of this synthesis.** It was written by one run, using reading helpers. Spot-check its §2 table against the registry rebuild (task 6).

## 7. Outside scope

- The engine `error_bound()` is not a bound for n ≥ 10⁵ (W7-SEC). It is an implementation fix.
- LS0 `emit_centre` is mandatory (W5-LOCKBOOK).
- Residualised start tables are a candidate method change (O-DILUTE, F-SIGMA).

## 8. Confidence card (the eight targets, as the evidence stands)

| Target | Refined statement (cite) | P(true) | P(provable at reasonable cost) | Crux | Method change |
|---|---|---|---|---|---|
| Thm 1 T03♯ | W6-FIXREV2 §1.2 | high | done (XF verified) | relevance at n = 200 is nil | no |
| Prop 1 T07 | W2-BOOK Prop 1 + W5-LOCKBOOK | high | done (Lean) | data paragraph must cite S-ELS, not the implication (A-REV4 B5) | no |
| Thm 2 T22+T27 | W1-EXP Thms 1–6; W3-PXN; W7-PART | high (exact Gram); medium-high (p ≫ n, A-REV3 GAP) | done / medium | XF review of P6, LH Thm 5; the study's dilution is in no theorem | no |
| Thm 3 repair | Theorem A + W_Lat + B′ + GU | high | done (A, B′); medium-high (W_Lat, GU: SF only) | XF review of W, W_Lat, GU | no |
| Thm 4 T21 | W2-BOOK Thm 4 / W5-LOCKBOOK | high | done (Lean) | GUARD and SR as code facts; output convention | no |
| Thm 5 T38 | W6-FIXREV1 + wave 5–7 | (0)(a)(c): high; (b1-LH) with LS0: high; no-LS0 on LH: medium-high | (b1-LH) done SF, XF pending; no-LS0: medium (task 1 + task 2) | XF review; LH-lock in general | LS0 for (b1); none if the no-LS0 routes pass |
| Thm 6 T26 | W2-T26 Theorem A / W5-LOCKBOOK | high (favourable) | done | premise fails at n = 200 and in the masked regime | no |
| Prop 2 T12+T31(i) | W2-BOOK Prop 2 | high | done, except the A-REV4 GAPs and VAL-FP | GUARD literal claim; VAL-FP replay | no |
