# W8-SYNTH: Campaign synthesis — one document of what is now established

**Read first:** `theory_campaign/LEDGER.md` (all waves and agents), then `theory_campaign/S-REGISTRY/REGISTRY.md` and `LOCKABLE.md` on branch `theory/S-REGISTRY` (the claims registry: every named result with status and verification), and `theory_campaign/F-REFINE/CARDS.md` + `ARCHITECTURE.md` on `theory/F-REFINE`.

Then `git fetch origin` and read EVERY `origin/theory/*` branch's REPORT.md / REVIEW.md / REFEREE_REPORT.md / RESPONSE_PLAN.md (W1–W7, F-*, O-*, A-*, S-*, L-LEAN), including the ones that landed after the registry was written (O-DILUTE, O-STAGES, F-SIGMA, F-REFEREE, O-VCERT, S-ELS, W7-SEP, W7-PART, W7-SEC, O-LS0 if present, L-LEAN).

**Write `theory_campaign/W8-SYNTH/SYNTHESIS.md`** for Felipe (the PI; new to the field; wants plain, honest language) with these sections:
1. **One-page summary:** the paper's story, what is proved, what is proved only with LS0, what is open; the three decisions Felipe must take (LS0 adoption; common-σ² start; the n = 200 disclosure wording).
2. **Theorem-by-theorem table** for the 8 paper targets: best current statement (one line), status word, same-family verification, cross-family verification (A-REV1–4), repairs applied, remaining premises, source branch.
3. **New results beyond the frozen list** (finite-n certificates, predicted miss rates, dilution masking, weight-stability Theorem W, separation theorem, partition lemma, stage-count theorem, naive-merge proposition, E[h] consistency, PW2) with the same columns.
4. **Conflicts and open disputes:** where agents disagree (e.g. W1 vs verifier, Opus vs Astra), state both positions and what would settle it.
5. **The referee's view** (F-REFEREE): the top objections and the planned responses, each tagged done / in progress / open.
6. **Method-change evidence:** O-LS0 data (if present), O-MIX, F-SIGMA, O-DILUTE: what each fix buys, its cost, and risk, in a comparison table.
7. **Lean:** what L-LEAN formalised sorry-free.
8. **Next 10 tasks**, ranked, as ready-to-run specs.

Never upgrade a status. Where the registry and a report disagree, say so. Quote branch + file + label for every claim.

**Deliverable:** `theory_campaign/W8-SYNTH/SYNTHESIS.md` and a 40-line `BRIEF.md` (the executive version).
