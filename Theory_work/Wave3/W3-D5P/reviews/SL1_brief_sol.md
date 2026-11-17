# SL1 — statement-lock review brief (Sol, gpt-6.1-sol, reasoningEffort high; fresh agent, blind first read)

You are the statement-lock reviewer (PROTOCOL_v4 §3 step 1) for ticket W3-D5P. Repository worktree (read-only for you):
`/home/fb31/BVS-wt/W3-D5P` (branch theory/W3-D5P). **Do not write, create or delete any file anywhere** (no TMPDIR, no
scratch files; if you must run a command, use read-only commands such as cat, sed, grep, git show). Return your whole
review as your final message; the lead saves it verbatim.

## Task
Check `Theory_work/Wave3/W3-D5P/STATEMENT.md` (v0.1) and `Theory_work/Wave3/W3-D5P/PLAN.md` against the sources: right
target, faithfully stated, hypotheses explicit, plan viable. **Break it**: look for a false clause, a missing hypothesis,
a wrong citation, a quantifier that is too strong (in particular "every admissible run", "either branch", the common data
event), an object that is not what the code returns, and any interpretive sentence ("hence", "in particular",
"consequently", "in words") inside a claim span (C1)–(C3) that is not itself proved.

## Target (from the department brief; the lead's paraphrase of the goal)
Track D ticket #5′: on every design inside Theorem 6 (reader version: `Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
§6, lines 660-812; master `W3-RM2-R:RM2-R-plus`), the new output fields `pip_list` (posterior renormalised to the
returned top store `fit$top_store`), `mpm_list`, `log_Z_list` are within 1 − π(S₀ | y) of the truth, jointly with the run's
output. Intended as a short corollary of Theorem 6 + posterior concentration. It must close the two links named as
unchecked at `Theory_work/Wave3/W3-DIST/STATEMENT.md:297-303`. The new fields are defined by
`/home/fb31/BVS-wt/W3-AUDIT/Theory_work/Wave3/W3-AUDIT/SPEC_LIST_PIP.md` (branch theory/W3-AUDIT, commit 523dda23;
read it with `git -C /home/fb31/BVS-wt/W3-AUDIT show 523dda23:Theory_work/Wave3/W3-AUDIT/SPEC_LIST_PIP.md`). They are
not yet implemented; the statement carries their implementation as a named premise.

## Sources to check against (all under /home/fb31/BVS-wt/W3-D5P unless stated)
- `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (RM0-plus :118-143, DLV-0 :144-163, RM2-R-plus :177-182, definitions :52-93)
- `Theory_work/Wave3/W3-RM/STATEMENT.md` :32-68 (objects, events, 𝒪, Ŝ⁺, 𝒦_n), :126-137 ((T1-R)), :160-176 (RM-0)
- `Theory_work/Wave3/W3-RM2/STATEMENT.md` :172-218 (Form R hypotheses, RM2-R)
- `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md` :60-77 (the pathwise claim RM-0 uses)
- `Theory_work/Wave3/W3-SAMP/STATEMENT.md` :36-62 and `Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md` (CC2, CC5)
- `Theory_work/Wave3/W3-DIST/STATEMENT.md` :271-318 (DIST-C)
- `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md` :1-33 (Lemma POST)
- Code of record `Scripts/SMC_BVS/core/` (identical to commit 4676af6): `v3_run.R`, `v3_fit.R`, `v3_exact.R`,
  `cpp/v3_core.cpp` (:358-370, :391-517, :524-570), `cpp/v3_ledger.h`, `cpp/v3_engine.h` (:86-105, :375-425),
  `cpp/v3_score.h` (:55-70, :255-300), `cpp/v3_start.h` (:75-97), `cpp/v3_util.h` (:115-127).
- Registry rows (cite, do not open the registry): W3-RM2-R:RM2-R-plus@1.0.1, RM0-plus@1.0.1, DLV-0@1.0.1 "PROVED-CHECKED;
  council R3, …"; W3-RM:RM-0@1.0.0 "PROVED-CHECKED"; W3-SAMP:CC@1.1.2 "CODE-CHECKED (lead; SL1, LC1, SW1, both council
  seats)"; W2-APP:POST@1.0.7 "PROVED-CHECKED".

## Output format
1. Verdict line: `SL1-VERDICT: LOCK` / `LOCK WITH CHANGES` / `DO NOT LOCK`.
2. Findings, numbered `SL1-1, SL1-2, …`, each: clause or line, what fails (with a counter-scenario or a code line where
   possible), severity (BLOCKING / MAJOR / MINOR / EDITORIAL), and a concrete fix.
3. A list of every interpretive sentence inside (C1)–(C3) with a verdict each (true and proved by the cited step /
   needs a proof / move out of the span).
4. Plan viability: one paragraph (is anything a hidden new key lemma?).
