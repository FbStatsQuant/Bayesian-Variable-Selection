# SOL62_AB — gpt-6.2-sol vs gpt-6.1-sol, replay mini-experiment (D124) — RUN 2026-11-17 (both arms, same inputs)

Prepared by the Theory helper (Sonnet 5.5) 2026-11-17. **Evaluation only; no registry/record change; no Codex/API call made.** The manager runs the 6.2 calls (≤ 4; one at a time). Folder: `Theory_work/Dept/SOL62_AB/` (per case: BRIEF.md = original brief verbatim; INPUTS.md = excerpts with commit+path:lines+sha; KNOWN_ANSWER.md; STORED_61.md; RUN.md; PROMPT_6.2.txt = the exact text to send; `build_inputs.py` regenerates all from git).

**Method.** Replay only 6.2 on the exact original 6.1 brief + the excerpted inputs the original saw (at that commit), same effort (high). Compare the 6.2 reply with the stored 6.1 reply and the known answer. A fixed REPLAY NOTICE (inputs are inline; no file writing) is the only text added to the brief; each RUN.md lists what was omitted for size.

## Results (run 2026-11-17, 19:03–19:26 CT; owner change: same inputs to 6.1 and 6.2)

**Method as run.** Each case's PROMPT (`caseN/PROMPT_6.2.txt`, which is model-neutral despite the name) was copied byte-identical to `/home/fb31/SMC_Theory_Department/tmp/sol62ab/`. Both models got the same wrapper, which told them to read the file in chunks of 120 lines, read no other file, and leave the repo off-limits. Each run used codex at reasoningEffort high, as a fresh child thread, run one at a time. **7 Codex calls:** the first (case1 6.1) is VOID, because a single `cat` let the shell truncate its input (`runs/case1_61_PILOT_VOID.md`). After that the wrapper was fixed for every scored run in both arms. Per-run records are in `runs/`. Times are wall time on the manager's clock; token counts were not exposed by the harness.

| case | known answer | 6.1 (same inputs) | 6.2 (same inputs) | real caught 6.1 / 6.2 | false · nitpick 6.1 / 6.2 | brief fidelity 6.1 / 6.2 | wall 6.1 / 6.2 |
|---|---|---|---|---|---|---|---|
| **1 · L1 statement lock** | KL(ii) row-wise false for design-dependent α (MAJOR) + 3 secondaries | NO-LOCK; KL caught; 3/3 secondaries; +1 plausible (C̄_H vs C_H(s,A)) | LOCK-WITH-AMENDMENTS (= stored); KL caught; 3/3; +2 plausible (C̄_H, shared; singular s̃ support) +1 verified (D_hellinger owner mis-cited) | Y / Y (6.2 more new) | 0·0 / 0·0–1 | weaker (missing sources inflated to MAJOR → NO-LOCK) / good | ≈ 2–3 / ≈ 5 min |
| **2 · W3-D2 R1 sol seat** | F1 lgamma cancellation (m♯ 95 vs 76; max 0.3942 vs 0.3928); both claims ACCEPT | 8.0 gates=FAIL; F1 caught (76 vs 95); +1 verified (TARGET "P=0" vs 0/300); decisions NOT-EXAMINED ×2 | 8.5 gates=FAIL; F1 caught (exact 0.392839); same "P=0" point with a proof; +1 plausible (parity table); **Thm2X REJECT** on a null-event domain caveat; Cor2X ACCEPT | Y / Y | 0·0 / **1 false decision**·1 | weaker (no decisions) / mixed (decisions, one wrong) | ≈ 3–4 / ≈ 4 min |
| **3 · K2 re-check (clean control)** | 2 RESOLVED, 0 new, 2 VERIFIED | exact match | exact match | — / — | 0·0 / 0·0 | exact / exact | ≈ 3 / ≈ 2 min |

**Reading (indicative only: n = 3, one sample each).**
- **Real findings:** both models catch every known-true finding.
- **Depth:** 6.2 goes deeper. It found 1 extra verified real finding, 2 extra plausible ones, and gave more rigorous arguments.
- **False positives:** 6.2 made the only false call in the A/B, a REJECT on a probability-zero domain caveat that 6.1 noted as a caveat only.
- **Fidelity:** 6.1 repeatedly turned "not supplied" inputs into verdict-level failures (NO-LOCK; NOT-EXAMINED); 6.2 handled them per item.
- **Clean control:** both models were clean.
- **Speed:** about the same, with 6.2 slower once.

**Open adjudications (not needed for the comparison):**
- C̄_H vs C_H(s,A) (both models);
- singular s̃ support (6.2);
- the parity table (6.2).

**Total estimated input:** ≈ 33.9k tokens for 3 calls (12.3k + 11.3k + 10.3k; chars/3.5). Output not estimated.

**Scoring conventions (fill the empty columns).** *Real findings caught* = the known-answer item(s) in each KNOWN_ANSWER.md (case 1: L1-1; case 2: F1; case 3: none expected). *False* = a finding whose claimed failure does not occur; *nitpick* = wording-only, no mathematical content; give counts as "false/nitpick". For case 3 any FATAL/MAJOR/MINOR/NIT is a false finding or a nitpick. *Brief fidelity* = how the 6.2 handled the brief's format/requirements (verdict line, per-question answers, "not supplied" for omitted files, no invention). *Tokens/time* = input tokens, output tokens, wall time from the run USAGE. Log each run per D123 in SOL62_QUALITY.md (BETTER/SAME/WORSE on F, N, B, S) as usual.

**Limits to state in the conclusion.** n = 3 cases (one per type), single sample each, no repeat runs: indicative only. Case 3 is an easy narrow control (K2 re-check), not a council seat — council-seat clean controls were all contaminated (WR1/WSL1 later contradicted; PSHARP readings later corrected; D2/D5P Sol reviews all had findings). Case 2 substitutes for the requested TRACK_B label case: no 6.1 review of TRACK_B exists (its checker was Opus: `AUDITCALC_check_opus.md`; the labels were refuted by the API audits AUDIT1/AUDIT2, triaged in TRACK_B §T/§T3), so the allowed fallback (a 6.1 council finding later confirmed) was used. In case 1 the 6.2 sees the input as excerpts, so questions about omitted files are not scored.
