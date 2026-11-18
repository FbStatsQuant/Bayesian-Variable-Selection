# T9 addendum: the consultant's riders 3 and 4 (and riders 1, 2 recorded)

Consultant: AGREE on T9, with riders. Sources read at origin/main (W1-N1, W3-SAMP, W3-READER as at ad29c22e) and the staged MEAS-D ticket at `origin/theory/PRE-LEAN` 43e1b07f (MEASD3).

## Riders 1 and 2, recorded

- **Rider 1.** The T9 verdict reads "**GAPS CLOSED (filter (a))**", not "no flaw": the fixed-data mathematics of rows 3.5, 3.6 and 4.1 is confirmed, and their joint-law clauses are complete only once MEAS-D is recorded. `T9.md` is amended accordingly.
- **Rider 2.** No row cites MEAS-D before its R3 and Sol-5 seats pass. So the PoolZ citation of MEAS-D (T9 card §A) and the MEAS-D pointer in any card row are applied only at MEAS-D's recording, not before.

## Rider 3: row 3.5's second identity, with a model summary h

**Confirmed: the same integrability step works.**

- The identity is (N1) of `W1-N1:Thm-N1` (`W1-N1/STATEMENT.md:102`): E[Ẑ_r·H_r(h) | 𝓒] = Z·π(h), for h with a deterministic bound |h| ≤ B_h (`W1-N1/STATEMENT.md` §1). H_r(h) is an average of values of h, so |H_r(h)| ≤ B_h.
- Hence |1_{𝒜°}Ẑ_r·H_r(h)| ≤ B_h·1_{𝒜°}Ẑ_r, which is integrable with expectation at most κ_n·B_h by Step 6; and |1_{𝒜°}Z·π(h)| ≤ κ_n·B_h.

**Where it goes: MEAS-D's Step 6, not PoolZ's span.** PoolZ is the case h ≡ 1 only. The identity itself lies in N1's span (`W1-N1/STATEMENT.md:98-104`), a fixed-data theorem that is not edited. The sentence belongs to `W3-SAMP/lemmas/MEAS_D.md`, the proof file of `W3-SAMP:MEAS-D`, and one clause is added to MEAS-D's statement.

**Exact sentence** (append to Step 6, before its ∎):

> The same holds with a bounded model summary. For h as in `W1-N1/STATEMENT.md` §1, with a deterministic bound |h| ≤ B_h that does not depend on the data, |H_r(h)| ≤ B_h, so |1_{𝒜°}Ẑ_r·H_r(h)| ≤ B_h·1_{𝒜°}Ẑ_r is integrable with expectation at most κ_n·B_h, and |1_{𝒜°}Z·π(h)| ≤ κ_n·B_h. Hence (N1), and likewise (MR-a)–(MR-c), integrate to E[1_{𝒜°}Ẑ_r·H_r(h)] = E[1_{𝒜°}Z·π(h)], with both sides finite.

**Statement clause** (inside W3 of the widened statement). Old: "so 1_{𝒜°}Z and 1_{𝒜°}Ẑ are integrable under every law of the data." New: "so 1_{𝒜°}Z, 1_{𝒜°}Ẑ and 1_{𝒜°}Ẑ_r·H_r(h), for every bounded h of §2, are integrable under every law of the data."

One condition to keep visible: B_h must be uniform in the data. That is what N1's §1 already requires ("a deterministic bound"), and it holds for every h used in W3-SAMP (indicators and sup-norm errors, bounded by 1).

## Rider 4: the 𝒜 identification (text C), split into a theorem-side sentence and a remark

### In W3-SAMP

**Theorem-side sentence** (`W3-SAMP/STATEMENT.md:36`, appended after MEAS-D's pointer sentence; no clock clause):

> By erratum E1 (`Theory_work/Wave3/ERRATA_W3-SAMP.md`), 𝒜 and 𝓒 are read throughout as the potential pair (𝒜°, 𝓒°) of `W3-AUDIT-A:GW`; on completed runs the actual calibration record equals 𝓒° (GW-iii), and statements about actual runs are obtained through 𝒪 ∩ A ⊆ 𝒪° ∩ A° (GW-iv, `W3-AUDIT-A:CAL-C`).

**Remark sentence** (a new paragraph after `STATEMENT.md:192`, at the end of the file; outside MEAS-D's span 190-192, and it shifts no earlier line):

> *Remark (actual runs; not part of any claim).* The guard's clock is not modelled (`W3-AUDIT-A:GW`, "Not claimed"). A probability of an actual-run event, that is, one intersected with {completed} or with the actual 𝒜, is therefore read as an outer probability unless the clock is taken jointly measurable with the streams; in either reading it is bounded by the probability of the corresponding potential event.

### In the reader (Theorem 10)

**Theorem-side** (`READER_VERSIONS.md:1301-1302`). "its calibration succeeds (fallback ladder included)" → "its calibration succeeds (fallback ladder included), in the run taken as if uninterrupted". Nothing about the clock enters the theorem.

**Remark** (append to the end of line 1322, the row 3.5 remark, which already carries the "as if uninterrupted" sentences; no line is added):

> *Remark (the time guard).* The guard's clock is not part of the probability model. A completed run coincides with the uninterrupted one, so each probability above that concerns the actual run is read as an outer probability and is bounded by the probability of the same event for the uninterrupted run.

### Changelog lines tying the change to erratum E1

- **Reader, Theorem 10 update log:** "- PL-T9 2026-11-18: [E1-TEXT] 𝒜 stated 'in the run taken as if uninterrupted' in Theorem 10's preamble; remark on the time guard added to the row 3.5 remark. Aligns the text with `W3-SAMP` erratum E1 (HQ D111; `Theory_work/Wave3/ERRATA_W3-SAMP.md`) and `W3-AUDIT-A:GW`, `:CAL-C`. Source: pre-Lean pass T9 (Astra T9-2, Sol T9-1, walk H2). CORRECTION-ONLY (EQUAL)."
- **`ERRATA_W3-SAMP.md`, under E1** (W3-SAMP's statement has no changelog table): "Applied to text 2026-11-18 (pre-Lean pass T9, CORRECTION-ONLY): `W3-SAMP/STATEMENT.md:36` now states the potential-pair reading, with a remark on actual runs after §4; `W3-READER/lemmas/R4_printed_outputs.md:17-18`, `W3-READER/STATEMENT.md:15-16` and `READER_VERSIONS.md:1301-1302, 1322` aligned. E1's substance is unchanged."

Note on line stability: a new bullet in the reader's update log would shift the lines of §11. If those line numbers must stay fixed, append the entry to the last existing bullet of that log instead.
