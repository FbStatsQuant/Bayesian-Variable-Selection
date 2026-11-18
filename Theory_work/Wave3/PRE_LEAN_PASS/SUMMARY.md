# PRE-LEAN PASS: SUMMARY (template; the coordinator fills it at the end, the manager finalizes)

Method frozen for this pass: `method-v3.1.1-listpip` = 7100bb3b (guard merged); the owner signed the method FINAL.

## 1. Findings (one line per target: Astra / blind Sol / Fable ruling)
_to fill: T1 ... T10, Sol1 ... Sol5, MEAS-D; counts of FLAW / UNSTATED-HYPOTHESIS / LEAN-COMPILE as ruled._

## 2. Changes staged (see `CORRECTIONS.md`, `BATCH_READY_v2.md`)
_to fill: corrections landed by the recorder; recorder-only items; deferred (T4-R4)._

## 3. Declined / not changed
_to fill: points the Fable declined, with the one-line reason._

## 4. Lean-readiness notes (see `BLUEPRINT_NOTES.md`)
_to fill: ranked items per target; for each Level-2 target its first paper-only dependency._

## 5. Coverage statement (HQ a810898a; `Lean/BRIEF.md` on main)
- **Certificates.** Only a MATCH (fidelity check: the Lean statement equals the paper statement) counts as a certificate of a paper theorem, cited by its number. A WEAKER result gets its own lemma label and is never cited as the paper theorem.
- **Level-2 headlines.** Each Level-2 headline names its first paper-only dependency, the first named axiom or hypothesis that Lean assumes without proof (listed per target in `BLUEPRINT_NOTES.md`; `FIDELITY.md` records it with every named axiom).
- **Counterexamples.** A counterexample found during formalization means the target is SUSPECT: escalate to HQ and stop work on that target.
