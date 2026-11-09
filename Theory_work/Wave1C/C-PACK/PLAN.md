# C-PACK — PLAN (v2, after R30)

Tracks (historical: drafts and first checks were started 21:2x–21:3x CST before the lock; see LOG.md):
1. Item 1: grep audit (W1-PXN, W1-GEN, T38 W6-FIXREV1) → Lemma UM (uniqueness ⇒ N = 1 ⇒ N3(c)/(a)) → Lemma UM-FP (N3(e) +
   recursive summation, ku < 1) → patches for e4 → e4′ (patches/P_e4_*.md) + METHOD_REQUIREMENTS.md. Numerics: item1_* (done).
   Check: R33 (Codex xhigh).
2. Item 2: Lemma I2 + patch; numerics R35_falsify (partition recovery and λ_min/[CONC′] substitution). Check: R35.
3. Item 3: R31 (SEL), R32 (L8) done; patches P_SEL_L6d.md, P_L8_certificate.md → independent re-check of the patches (R37).
4. Item 4: Lemma SL0/SL1/SL1′/SL2 + SONG_LIANG_MAP.md; numerics R34_falsify (exact enumeration). Check: R34.
5. Item 5: consolidated files (Sonnet helper, done) → fidelity check R36 (Codex xhigh).

Review gates: apply and record the statement-lock changes before further proof work. For each new lemma and each repaired SEL/L8 claim, record falsification evidence (exact small cases or simulations with ≤20 seeds, local compute only) and a fresh cross-family line-by-line check before downstream use. Reused Wave-1 numerical evidence must be named with its exact tested scope; Item 2 also checks the CONC′/operator-error substitution and the relevant onset/domain conditions, not only partition recovery. Numerical experiments are falsification attempts, not proofs of tail bounds. Any SEL/L8 repair is supplied as a patch and independently re-checked; an actual counterexample triggers the protocol's stop-and-report rule.

Once the key lemma is ready, request a fresh independent Codex xhigh mid-point review using only STATEMENT.md and proof files, not the lead's conclusion or log. Continue only on CONTINUE; on REDIRECT/STOP, stop and report to HQ. Before final review, run the citation-check script on every cited path:line/quotation and save reviews/CITECHECK.txt, correcting every miss. Then perform an exhaustive sweep of the whole ticket, including the Item-5 consolidated supplement and its fidelity manifest; fix findings, followed by council review of the same complete package (Sol xhigh and Opus high). Pass requires both scores ≥8.0 and all gates passing in the same round; at most three rounds, with unresolved findings and exact scope reported honestly. R36's dedicated fidelity check is additional evidence, not a substitute for these ticket-wide gates. Preserve all input statuses verbatim, link every verified/checked assertion to its actual review file, and update LOG.md at each step.

Check the local clock at major steps. CHECKPOINT.md is due 01:30 CST and final REPORT.md/final message 04:30 CST; if gates or targets remain open, report PARTIAL with the exact frontier. No edits outside C-PACK and no git state changes.

Note on council scope: HQ's brief says "run one council over items 1–4 together; item 5 needs only its fidelity check".
R30 asks for the council to cover the complete package. Resolution: the sweep covers items 1–5; the council receives
items 1–4 as the scored object and the item-5 package + R36 as context (HQ's instruction prevails on scope; recorded in
reviews/R30_disposition.md).
