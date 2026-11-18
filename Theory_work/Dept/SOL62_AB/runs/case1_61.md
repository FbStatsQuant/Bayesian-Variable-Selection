# case1 · gpt-6.1-sol (codex, reasoningEffort high), SCORED run

Wrapper: read the file in chunks of 120 lines, read no other file. Run about 19:07 to 19:09 CT (wall time ≈ 2–3 min, from the manager's clock). Full reply: T3 child thread "SOL62 A/B case1 · gpt-6.1-sol (scored)". Header line correct.

**Verdict.** LOCK-VERDICT: NO-LOCK. The stored 6.1 original was LOCK-WITH-AMENDMENTS; the difference comes mostly from L1-6 (sources not supplied).

**Findings:**
- **L1-1 MAJOR:** the row-wise KL(ii) reading fails for design-dependent α. Counterexample: α = X²_{𝒞,2}, giving y₁ | x₁ = t + χ²₁ + N(0,1). Fix: restrict to deterministic α. **This is the known answer: CAUGHT.**
- **L1-2 MAJOR:** the §8 final implication row is wrong because C̄_H = max_t C_H(t,A) can exceed C_H(s,A), so it does not recover CorH-plus(b)'s exact thresholds. Fix: make C_H nondecreasing in s, or prove a fixed-size uniform form. *Not in the known answer and not in the stored 6.1. The manager rates it plausible (a real constant mismatch in a plan-level implication row); adjudication is pending.*
- **L1-3 MINOR:** the conditional-mean remark has no integrability (Cauchy example) → use kernel means. This is stored L1-3: **real, secondary.**
- **L1-4 MINOR:** "neither … omitted-part contrasts non-Gaussian" needs "conditionally" (variance-mixture). This is stored L1-2: **real, secondary.**
- **L1-5 MINOR:** H2_uniform contrast-posterior notation; Borel extension at zero contrast. This is stored L1-4: **real, secondary.**
- **L1-6 MAJOR:** some sources are not supplied. This is correct "not supplied" behaviour, but it was raised as a MAJOR finding. Fidelity: counted as process, not false.

**Q1–Q6.** All answered, and every unverifiable item is marked "not supplied" (correct).

**Score.**
- Known answer: caught.
- Secondaries: 3/3.
- New: 1, plausible.
- False: 0.
- Nitpick: 0.
- Fidelity: good. Its verdict is stricter than the stored one because of the missing sources.
