# BRIEF — diff check RC6 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your whole brief. Work
only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state**
(read-only git commands are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/RC6_diffcheck_sol.md`; edit nothing else. Do not start subagents. Use no effort
setting above high. All results are asymptotic.

## Frozen content
`Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt`, first line `MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a`. **Quote this digest line verbatim
at the top of your review.**

## Files you may read
* Current texts (in the manifest), under `Theory_work/Wave3/W3-RM2/`: `STATEMENT.md`, `REPORT.md`, `SHARPNESS.md`,
  `ASSUMPTION_MAP.md`, `lemmas/L1_sandF_b.md`, `lemmas/L5_formR.md`, `lemmas/L6_examples.md`, `numerics/SPEC.md`,
  `numerics/RESULTS.md`, `numerics/rm2_common.R`, `citecheck.py`;
* `Theory_work/Wave3/W3-RM2/reviews/as_reviewed_by_SW1/` — the exact ten texts the exhaustive sweep read (their
  sha256 are the corresponding rows of `reviews/MANIFEST_SW1.txt`: check them);
* the sweep and its disposition: `reviews/SW1_sweep_astra.md`, `reviews/SW1_disposition.md`; and
  `reviews/BT2_disposition.md` (only to check the sentences REPORT now quotes from it);
* to check the new "Energy constant" remark of STATEMENT §3: `lemmas/L0_toolkit_b.md` §0 (how the score uses the
  response), `Theory_work/Wave1C/C-GROW/STATEMENT.md:84-88`, `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:27-29`;
* `Scripts/SMC_BVS/core/cpp/v3_engine.h:392-414` (to check the three departures now stated in `numerics/SPEC.md`).
Do not read any `LOG.md`, any `CHECKPOINT*.md`, or other review files.

## Task (PROTOCOL rule 15: check of a post-review change)
The sweep returned 0 FATAL, 2 MAJOR (both on records), 4 MINOR, 1 NIT. The lead says: current files = the swept
files + exactly those seven items (markers [SW1-1]…[SW1-7]) + record-only hunks: five citation-context fixes found
by the new `citecheck.py` (a ticket abbreviation added before a path), REPORT §1/§4/§6 updated with the sweep and
better-theorem results, two rows of the open-items table in SHARPNESS, and one stale word in ASSUMPTION_MAP.
1. Diff each of the ten pairs (compare content; `diff --strip-trailing-cr`); list every changed hunk.
2. Classify each hunk: (a) required by a sweep finding and applied faithfully (compare with the sweep's exact
   correction); (b) record/editorial; (c) a substantive change (to a hypothesis, claim, lemma statement, proof step,
   constant or code pin).
3. **[SW1-1] is the one hunk with mathematical content**: STATEMENT §3 now says the energy constant M is any fixed
   positive number and gives a response-rescaling argument. Check it: is the method (score, block tables, start law,
   posterior, LS0 path) a function of the standardised response only? Under (Y, θ*, σ) → (aY, aθ*, aσ), which
   hypotheses of (C1) are invariant, and is (V) preserved with a²M_n? Is anything else in (T1-F) scale-dependent? Does
   the change alter the hypothesis domain of (C1) relative to what the sweep verified (the sweep's own correction
   asked for exactly this argument)? `numerics/rm2_common.R`: are the changed lines comments only?
4. [SW1-2], [SW1-3]: are the new wordings in SPEC, RESULTS, SHARPNESS, REPORT accurate and sufficient? Check the
   displayed conditional covariance if you can; check the three stated departures against `v3_engine.h`.
5. Run `python Theory_work/Wave3/W3-RM2/citecheck.py` from the worktree root (it writes only
   `reviews/CITECHECK.txt`, which you may let it overwrite) and report its first line.
6. Give each of the seven items a final verdict (RESOLVED / NOT RESOLVED) and one attestation:
   `ATTESTATION: editorial/record only — the package stands as swept in round SW1` or
   `ATTESTATION: substantive change — needs a fresh review`, with any remaining required change stated exactly.

## Output format (in your one file)
```
MANIFEST <digest>
Hunks: per file, classified (a)/(b)/(c).
Verdicts: one line per item.
ATTESTATION: …
Checks performed / not checked.
```
End your reply with the attestation line and the path of your file.
