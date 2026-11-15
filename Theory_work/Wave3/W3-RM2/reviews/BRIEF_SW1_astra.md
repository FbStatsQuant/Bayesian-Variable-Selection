# BRIEF — exhaustive sweep SW1 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are the exhaustive-sweep reviewer of theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable selection
by sequential Monte Carlo; the ticket proves when the coded method **reports the true model S₀** when the set Q of
columns that may "leak" signal has polynomial size n^b). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/SW1_sweep_astra.md`; edit nothing else (scratch files outside the worktree).
This file is your whole brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are
relative to it). **Change no git state.** Do not start subagents. Use no effort setting above high. All results are
asymptotic (n → ∞) by design; do not flag "asymptotic only" or "no finite-n statement" as a defect.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_SW1.txt`; its first line is
`MANIFEST 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd`. **Quote this digest line verbatim at the top of your review.**
Read only files listed in that manifest: the ticket folder `Theory_work/Wave3/W3-RM2/` except `reviews/`, `LOG.md`,
`CHECKPOINT*.md` — i.e. `STATEMENT.md` (v1.4), `REPORT.md`, `SHARPNESS.md`, `ASSUMPTION_MAP.md`, `PLAN.md`, `BRIEF.md`,
`lemmas/L0`–`L6`, `numerics/` — and the external inputs listed in `reviews/INPUTS.txt` (pinned code, the parent
ticket W3-RM, the engines C-GROW / W1-GEN / W2-LOC2 / W2-UNI / W2-APP). Do not read any other file in a `reviews/`
folder, any `LOG.md` or `CHECKPOINT*.md`. Markers such as [SL1-#], [MP1-#], [LC2A-#], [SC2-#] point to earlier
internal rounds whose reports you are not given; judge the text as it stands.

## Task — sweep everything, claim by claim
The ticket claims (C1)–(C6) of `STATEMENT.md` §4 are proved: the fixed-design theorem RM2-F (L0–L3), the
Gaussian-row theorem RM2-R (L4, L5), the width lemmas (L2), the containment of the parent theorems (L3, L5), the
examples (L6) and the sharpness record. Your job is the last line of defence before the council:
1. **Every claim against its proof.** For each of (C1)–(C5) and each bridge (P0)–(P10): is it proved exactly as
   stated (hypotheses used but not stated; conclusions stated but not delivered; quantifiers; uniformity of every
   "n ≥ n₀"; events and their measurability; conditional arguments under Gaussian rows; the import of the parent's
   core theorem RM-0 and of Lemma E4 within their statements)? Re-derive the steps you judge most error-prone, with
   constants. At least: the score toolkit at growing cardinality (L0); the junk-exclusion margins (L1 Step 2(b), L4
   §6(b)); the width lemma and its converse (L2 §1–§2); truth removal (L2 §4); the product-form selection removal
   and the spherical tail with a mean shift (L4 §2–§3); the passage from a joint-law bound to a conditional
   Gaussian width (L5 §2); the examples E2–E5 (L6).
2. **Consistency across files.** STATEMENT vs lemma statements vs REPORT §2–§3 vs the registry block at the end of
   REPORT vs ASSUMPTION_MAP vs SHARPNESS: any mismatch in a hypothesis, constant, range (b, ρ, η, α, δ₀), symbol or
   status; any citation (path:line) that does not say what it is cited for; any status quoted more strongly than
   its source records it (check consumed claims against the cited files; the conditions of (C1) and (C2) on inputs
   that are not "PROVED-CHECKED" must be carried).
3. **Honesty of the record.** Does any sentence in STATEMENT §6, SHARPNESS, REPORT (flags, §1, §5, §6) or
   ASSUMPTION_MAP claim more than is proved or observed — in particular about necessity, sharpness, the numerics
   (LS0-probe scope, nominal classification, counts in `numerics/RESULTS.md`), or the examples' cutoffs?
4. **Code facts.** The statement pins facts about LS0 to `Scripts/SMC_BVS/core/cpp/v3_core.cpp` and `v3_engine.h`
   lines; check the pins say what the statement says.
5. **Design-agnosticism.** No design family may appear in a theorem statement (families only as examples).

## Output format (in your one file)
```
MANIFEST <digest>
Verdict: SWEEP CLEAN | SWEEP WITH FINDINGS (counts: FATAL / MAJOR / MINOR / NIT)
Findings: numbered; each FATAL / MAJOR / MINOR / NIT, with file:line, the problem, and the exact correction or the
  missing argument. FATAL = a claim falls; MAJOR = a claim or a record is wrong as written but repairable.
Claim-by-claim table: (C1)–(C6), (P0)–(P10): VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED.
Independent derivations: what you re-derived, with the outcome.
Not checked.
```
End your reply with the verdict line and the path of your file.
