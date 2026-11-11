# BRIEF_B1_astra — blind first read of the scoping memo W3-MEMO-SCR-RM (review B1)

You are a fresh, independent reviewer (gpt-6-astra, reasoning effort high — never above). This file is your whole
brief. You have seen no earlier review of this memo; none exists. **Your job is to break the memo**: its implications
(§1), its list of missing links (§2), its regime map (§3) and its recommendation (§4). Agreement is worth nothing
unless you tried to refute first.

## Where
Worktree: `C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM` (branch `theory/W3-MEMO-SCR-RM`). Work only there, with absolute paths.
**Change no git state.** Write exactly one file: `Theory_work/Wave3/W3-MEMO-SCR-RM/reviews/B1_review_astra.md`.
Edit nothing else. Start no other agents. No web.

## Frozen content
Manifest: `Theory_work/Wave3/W3-MEMO-SCR-RM/reviews/MANIFEST_B1.txt`,
digest `cd0ebff97cc6e2fc04afd31d45b1abd90527762f3fae73e76c8d66330fca3c20`.
First run, from the worktree root:
`python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-MEMO-SCR-RM Theory_work/Wave3/W3-MEMO-SCR-RM/reviews/MANIFEST_B1.txt`
and **quote the line `MANIFEST <digest>` as the first line of your review file and of your final message.** If verify
fails, stop and report that.

## What is under review
`Theory_work/Wave3/W3-MEMO-SCR-RM/MEMO.md` (version 1). It answers the question in
`Theory_work/Wave3/W3-MEMO-SCR-RM/BRIEF.md`: can the certified-screening theorem SCR-C (a certified sparse reported
model equals S₀) plus a theorem "P(certified ∧ |Ŝ| ≤ q_n) → 1" give a reported-model theorem without W3-RM's leakage
condition (L), and/or without its lattice condition (N)/(D-R), and so supersede or strengthen W3-RM? BRIEF.md contains
an unreviewed prior of the project lead ("HQ's prior"). Treat it as one more claim to test, not as guidance.

## Files you may read
* This ticket: `MEMO.md`, `BRIEF.md`, `reviews/MANIFEST_B1.txt`, `reviews/INPUTS_B1.txt`, this brief.
* Every file listed in `reviews/INPUTS_B1.txt` (the memo's sources), and, to check a claim at its origin, any other
  file under `Theory_work/Wave3/W3-SCR/`, `Theory_work/Wave3/W3-RM/`, `Theory_work/Wave2/W2-FAC-PK/`,
  `Theory_work/Wave2/W2-APP/`, `Theory_work/Wave1C/C-GROW/`, `Theory_work/Wave3/PROTOCOL.md`,
  `Scripts/SMC_BVS/core/`, and `Theory_work/INFRA/registry/`.
* Token efficiency: grep and targeted reads; do not paste long files.

## Ground rules of the project (not open to challenge)
* All results are asymptotic (n → ∞). Do not list "asymptotic only" or "no finite-n statement" as a weakness.
* Theorems are stated under conditions on (X, θ*) only; design families appear only as examples.
* The method is the code as on main; a method change is outside scope.
* Tie-break between incomparable theorems: design-agnosticism > range of p > rate > constants.
* The memo's tags: [SRC] registered claim, [DED] deduced in the memo, [SK] sketch. A [SK] item is not claimed as
  proved; attack it on whether the sketch can be right, and on whether the memo leans on it more than a sketch allows.

## What to do
1. **Implications I1–I5 (§1).** For each: verdict CORRECT / CORRECT-WITH-FIX / WRONG / UNSUPPORTED, with the failing
   step or a concrete counterexample. In particular:
   * I1: check the flag logic against `Scripts/SMC_BVS/core/v3_run.R` (and the core it calls): on RM-0's good event,
     is `local_certified` really TRUE on every completed admissible run? Order of the two searches, ties, the
     enumeration branch, the `identical(...)` comparison.
   * I2: do FAC-PK's hypotheses really satisfy every hypothesis of SCR-C when ρ < 1/3 (visibility, the floor, the
     coefficient and growth conditions)? Does NEG + PATH really make the LS0 archive uncertified? Is "open" the right
     status for the final-search half?
   * I3: does NF really give every item of T1-F (GROW (H0))? Is the set identity {Ŝ = S₀} = {S₀ scored} right, and
     the inclusion from SCR-C?
   * I4, I5: the direction of each implication and each non-implication; give a counterexample where the memo says
     "does not imply" and you think it does, or the reverse.
2. **Missing links (§2).** Is the decomposition ML1–ML3 complete and exact? Find a route to supersession the memo
   missed (for example through SCR-G's uncapped/capped statements, SCR-M with a special family, the final local
   search, or a different use of (EC′)), or show that none exists. Test the potential-lemma sketch PL: the per-move
   gain, the budget, the constant C = φ/ε, the claim C − 1 ≥ 2 log p/log n, and the comparison with the shipped caps
   and with (N-χ). Is the "on RM's own lattice" paragraph sound?
3. **Regimes (§3).** Is each row a correct statement about conditions on (X, θ*)? Is any example misplaced?
4. **Recommendation (§4).** Make the strongest case for (b) and for (c), then say whether either beats (a). State
   what in the paper's headline would be wrong, weaker than provable, or misleading if HQ follows (a) with Corollary
   CERT. Say whether Corollary CERT is true as stated and worth stating.
5. **The prior.** Did the memo test HQ's prior or assume it? Are its three "corrections" right?

## Reply format (in `B1_review_astra.md`, and a ≤ 25-line summary as your final message)
Line 1: `MANIFEST <digest>`. Then: verdict **ACCEPT / ACCEPT-WITH-CHANGES / REJECT** (of the memo's implications and
recommendation); a table of I1–I5 verdicts; numbered findings graded CRITICAL / MAJOR / MINOR / NIT, each with the
memo line, the evidence (file:line), and the smallest fix; your answer to "is there a missed route?"; your own
recommendation among (a), (b), (c) with one paragraph of reasons.
