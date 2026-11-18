MEASD8 is PURE: all five checks pass and no correction is needed. I changed no tracked file, committed nothing and started no subagents. `git status` is clean, and my scratch work is in `.rc_tmp/pure_measd8/`, which git ignores.

**Manifest verify.** `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/ticket Theory_work/Wave3/PRE_LEAN_PASS/MEAS-D/MANIFEST_MEASD8.txt` printed `verify: OK MANIFEST 8a9c5aca36550e85ac3c614405d4374a2011a72f93f75c12872729cedc76eca4` and exited 0.

**(1) Only the three edits changed — PASS**
- **MEASD7 baseline:** the three ticket files from `git show a2e3a9f1:…` hash to the MANIFEST_MEASD7 values (REPORT d0e9f04e…, STATEMENT 3530caf7…, MEAS_D ecd3bce9…).
- **Script compare** (`.rc_tmp/pure_measd8/cmp.py`): each of the three Old strings occurs exactly once in MEASD7. After replacing them with the New strings, `STATEMENT.md` and `lemmas/MEAS_D.md` are byte-identical to MEASD8 (a38fe147…, 146c2e41…).
- **Where the changes are:** `diff` shows them only at STATEMENT.md:194, MEAS_D.md:3 and MEAS_D.md:50.
- **REPORT.md** is byte-identical between the two (d0e9f04e…).
- **Line counts** are 194 (STATEMENT), 206 (REPORT) and 96 (MEAS_D).
- **Claim span and premises:** STATEMENT.md lines 1-192 are identical between MEASD7 and MEASD8, so the claim span :190-192 and the premises :20-60 are unchanged. `R7_to_R8.diff` and `MEASD8_CLAIMED_EDITS_GREP.txt` agree with this.

**(2) The c-2 and c-3 pins — PASS**
- **c-3:** in `Theory_work/Wave1/W1-N1/STATEMENT.md` (sha 70712d28…, which matches its EXT row in the manifest), line 62 starts "**Summaries h.**" and the definition ends at line 66 ("…special case B_h = 1. π(h) := …"). So `W1-N1/STATEMENT.md:62-66` is the right pin for the h class. The old target, lines 105-108, is the heading and opening of Corollary E, as Sol said.
- **c-2:** `R7_council_sol.md` ends with `COUNCIL-VERDICT round=R7 manifest=951d5a66… seat=sol`, and 951d5a66… is MEASD7. So "bound to the MEASD7 digest" is correct.

**(3) The c-1 sentence — PASS.** It is true, and it adds no premise and no claim.
- **Agreement with GW.** GW's "Not claimed" (T1_GW/STATEMENT.md:99-102) says that if the clock is jointly measurable with the streams, 𝒪 is an event; otherwise the bound holds as an outer-probability bound. GW works with fixed data. W3-SAMP's joint-law reading needs 𝒪 ∩ A to be an event on the joint data-and-stream space. Joint measurability with the data and the streams is therefore the right condition for reading it as an ordinary probability.
- **The "not enough" parenthetical is true.** Measurability in the streams for each fixed data set does not give joint measurability. A ZFC counterexample: the graph of a non-Borel function has Borel sections but is not product-measurable.
- **"(the clock readings)" is accurate.** GW's operational fields also include machine-environment readings, so I checked the code. The `exceeds` Boolean in `v3_fit.R` compares deterministic size estimates and the timing benchmark (a clock reading) with the allocation argument. `RuntimeGuard::check` (`cpp/v3_runtime.h`) uses only steady_clock elapsed time and the allocation. `VmHWM`, `R.version` and `Sys.getenv` are only recorded (`fit$peak_memory_kb`, `timing_procedure$environment`) and feed no Boolean. So the only random inputs to the guard's decisions are clock readings.
- **No premise or claim added.** The sentence sits in a remark headed "not part of any claim". The claim at :190 still says "Nothing is claimed about the actual 𝒜, 𝒪 or the guard". The sentence only says when the ordinary-probability reading applies, and both readings stay bounded by the potential event.

**(4) Converter — PASS.** `Theory_work/INFRA/tools/ingest.py convert` on a scratch copy of REPORT.md exited 0. It gives one record with lines [190, 192] and 12 depends_on items, none with spaces. Status_source is `lemmas/MEAS_D.md:3`, read relative to the copy's folder. The record has no absolute-value bars and no "§" in the conclusion.

**(5) NEXT_BATCH patches — PASS.** I used copies of `Theory_work/Wave3/W3-SAMP` taken from HEAD, which is identical to origin/main f6411c3e.
- **Stacked route:** `MEAS-D_stage_wo_NB-C1.patch`, then `NB-C1v2_correction.patch`, then `NB-C1r_correction.patch` all applied at `patch -p1 -F0` with rc=0.
- **Single patch:** `MEAS-D_stage.patch` alone also applied at `-F0` with rc=0.
- **No leftovers:** neither route produced .rej or .orig files.
- **Same result:** both routes give a `STATEMENT.md`, `lemmas/MEAS_D.md` and `REPORT.md` that are `cmp`-identical to the ticket's.
- **NB-C1r remark:** the remark line in NB-C1r is `cmp`-identical to the ticket's STATEMENT.md:194.

**Optional, outside this freeze.** MEAS_D.md:12 and :87 still paraphrase GW as "if the clock is jointly measurable" without "with the data and the streams". This is not wrong, since they report GW's own statement, but it could be aligned with :194 in a later pass.

PURE-VERDICT: PURE
