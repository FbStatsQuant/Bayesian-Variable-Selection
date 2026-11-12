# BRIEF — statement-change check SC2 (seat: Codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your whole brief. Work
only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state**
(read-only git commands are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/SC2_statement_change_sol.md`. Do not edit any other file. Do not start subagents.
Use no effort setting above high. All results are asymptotic.

## Frozen content
`Theory_work/Wave3/W3-RM2/reviews/MANIFEST_LC2.txt`, first line `MANIFEST b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6`. **Quote this digest line verbatim
at the top of your review.**

## Files you may read
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` (current, v1.4) and `Theory_work/Wave3/W3-RM2/reviews/STATEMENT_v1.3_CP2.md`
  (v1.3, the statement that stood at the previous checkpoint; it equals the committed file at git commit c2257ab —
  you may check with `git show c2257ab:Theory_work/Wave3/W3-RM2/STATEMENT.md`);
* `Theory_work/Wave3/W3-RM2/lemmas/L4_sandR_b.md` §0 and §7, `lemmas/L5_formR.md` §3–§5, `lemmas/L6_examples.md`
  (examples table and status lines), `lemmas/L0_toolkit_b.md` (header) — only to check that what v1.4 says about them
  is what they state (another reviewer checks their proofs);
* `Theory_work/Wave3/W3-RM/STATEMENT.md` §3.2 (lines 127-156: the Form R hypotheses of the parent theorem).
Do not read other files in `reviews/`, any `LOG.md` or `CHECKPOINT*.md`.

## Task (PROTOCOL rule 15: a substantive statement change needs a fresh check)
v1.4 changes the Form R leak hypothesis (L-R^b) and several records. The lead says: (1) the only hypothesis that
changes is (L-R^b) in §3.2 (with the constant list in §3); (2) the new (L-R^b) is **implied by** the v1.3 one — so
the v1.3 theorem (C2) is a special case of the v1.4 theorem — through the sufficient form stated in §3.2; (3) no
Form F hypothesis and no claim (C1)–(C4) changes otherwise; (4) (C5), §5, §6 and §7 are updated records.
1. Diff the two files; list **every** changed hunk and classify it: (a) the intended hypothesis change; (b) record /
   editorial; (c) any other substantive change (to a hypothesis, claim, bridge statement, constant or code pin) — these
   must be flagged.
2. Check claim (2) yourself: derive that the v1.3 hypothesis (leak bound C_L n^{−1/2} at the localised sets U₀ only,
   localisation covariances ≤ r_n with r_n(n log n)^{1/4} → 0, under the floors (FL-R)) implies the v1.4 (L-gain-R)
   and (L-loc-R). Also check the stated sufficient form with its constant (ℓ_n = ℓ′_n + 15r_n²/c).
3. Is the new (L-R^b) well posed (quantifiers; does (L-gain-R) quantify over sets U that contain truths; is "ρ > 0
   with 15ρ + b < ½" consistent with H_l ⊇ {l} ∪ S₀)? Is the "in words" paragraph accurate?
4. Check the records against the lemma files: the (P7) and (P10) rows, (C4), (C5) (each example and cutoff against
   `lemmas/L6_examples.md`), §5 (which dependencies are conditions now), §6 (not claimed), §7 (pointer).
5. Verdict: `ACCEPT`, `ACCEPT WITH CHANGES` (list them exactly) or `REJECT` (say what falls).

## Output format (in your one file)
```
MANIFEST <digest>
Verdict: …
Hunks: numbered, classified (a)/(b)/(c).
Derivation of v1.3 ⇒ v1.4.
Findings: numbered; CRITICAL / MAJOR / MINOR, each with the exact correction.
Checks performed / not checked.
```
End your reply with the verdict line and the path of your file.
