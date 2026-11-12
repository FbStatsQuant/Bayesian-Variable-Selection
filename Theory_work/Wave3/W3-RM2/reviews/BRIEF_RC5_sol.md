# BRIEF — diff check RC5 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/RC5_diffcheck_sol.md`; edit nothing else (read-only git commands are allowed).
This file is your whole brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are
relative to it). **Change no git state.** Do not start subagents. Use no effort setting above high. All results are
asymptotic (n → ∞) by design; do not flag "asymptotic only" or "no finite-n statement" as a defect.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_SW1.txt`; its first line is
`MANIFEST 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd`. **Quote this digest line verbatim at the top of your review.**

## Files you may read
* Current texts (in the manifest), under `Theory_work/Wave3/W3-RM2/`: `STATEMENT.md`, `ASSUMPTION_MAP.md`,
  `lemmas/L4_sandR_b.md`, `lemmas/L5_formR.md`, `lemmas/L6_examples.md`, `SHARPNESS.md`;
* `Theory_work/Wave3/W3-RM2/reviews/as_reviewed_by_LC2/` — the exact five texts the previous round read (STATEMENT,
  ASSUMPTION_MAP, L4, L5, L6; their sha256 are the corresponding rows of `reviews/MANIFEST_LC2.txt`: check them);
* the four reviews of that round and their disposition: `reviews/LC2A_L4_check_astra.md`, `LC2B_L5_check_sol.md`,
  `LC2C_L6_check_opus.md`, `SC2_statement_change_sol.md`, `LC2_disposition.md`;
* `Theory_work/Wave3/W3-RM2/lemmas/L2_width.md` §4 (only to check the lead's reason for the symbol chosen in
  SC2-1: is λ_n already in use there?).
Do not read any `LOG.md`, any `CHECKPOINT*.md`, or other review files.

## Task (PROTOCOL rule 15: check of a post-review change)
The previous round returned 13 items (no FATAL; one MAJOR, notational: the Gaussian-row leak sequence was written
ℓ_n, the symbol of the LS0 move cap). The lead says: current files = the reviewed files + exactly those items
(markers [LC2A-1], [LC2B-1], [LC2B-2], [LC2C-1]…[LC2C-5], [SC2-1]…[SC2-4]) + record-only hunks (status headers of
L4, L5, L6; one ASSUMPTION_MAP row rewritten for v1.4); `SHARPNESS.md` is a new file, not part of the diff.
1. Diff each of the five pairs (compare content; line endings may differ: `diff --strip-trailing-cr`); list every
   changed hunk (the global rename ℓ_n → ϖ_n / ell_n → varpi_n may be listed once per file, but check it is
   complete and touches no occurrence of the cap ℓ_n in STATEMENT §1, (C1), (C6)).
2. Classify each hunk: (a) required by a review item and applied faithfully (compare with the reviewer's exact
   correction); (b) record/editorial; (c) a substantive change (to a hypothesis, claim, lemma statement, proof step,
   constant or code pin). For the proof-text hunks [LC2A-1], [LC2B-1], [LC2B-2]: decide whether the new text is a
   correct proof of the same step from the same hypotheses.
3. SC2-1: the reviewer proposed λ_n; the lead used ϖ_n. Accept or reject the deviation, with the reason.
4. LC2C-1 was not adopted as a claim (recorded as an open item). Is the wording in L6 E5 and STATEMENT (C5)
   accurate about what is and is not proved?
5. Give each of the 13 items a final verdict (RESOLVED / NOT RESOLVED) and one attestation:
   `ATTESTATION: editorial/record only — L4–L6 and STATEMENT v1.4 stand as reviewed in round LC2` or
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
