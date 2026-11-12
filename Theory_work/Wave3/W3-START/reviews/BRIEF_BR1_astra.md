# BRIEF — break review BR1 of the Gaussian-row bridge (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/BR1_break_review_astra.md`. Do not edit any other file in the repository. Do
not start subagents. Use no effort setting above high. If you run code, keep your scripts outside the repository (a
temporary directory) or inline; the ticket's numerics may be re-run read-only.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_LC2.txt`. Its first line is
`MANIFEST 053bc169c5da3c032943e217e7bd5ddb76d4268ba821b09579be126d9961a155`. **Quote this digest line verbatim at the top of your review.** You may run
`python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START Theory_work/Wave3/W3-START/reviews/MANIFEST_LC2.txt`.

## Files you may read
Only files listed in that manifest: the ticket's `STATEMENT.md` (the locked target, v1.3.1), `PLAN.md`, `BRIEF.md`,
`ASSUMPTION_MAP.md`, the `lemmas/` folder (L1–L11), the `numerics/` folder, and the external inputs listed in
`reviews/INPUTS.txt` (pinned code, wave documents, sources of the argument, consumers' statements). Do not read any
other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`.

## Your task: break review of L9 (the Gaussian-row bridge (B-R) and Theorem (T3)(b))
Object: `lemmas/L9_BR.md`.
The proofs are by the ticket lead and are unchecked. **You are briefed to break them.** Read every line; re-derive
every displayed inequality and every constant; check that each step uses only what is available at that point
(hypotheses of the statement, earlier steps, or a cited result of another lemma file of this ticket, whose statement
you should read; the files L1–L5 may be taken as given where they are cited, but report any mismatch between what is
cited and what they state). The ticket consumes **no** registry claim: nothing may be imported as a premise from
another ticket. In particular check:
This file is the lead's single attempt at the hardest remaining lemma of the ticket; if it does not survive your
review the claim (T3)(b) is narrowed. Read it as an adversary. In particular:
* L9.1: the covariance event (the reduction to N iid rows, polarisation, the chi-square bound, the union count);
  consequences (c1)–(c4), with their constants and the sizes of the index sets on which the population floor
  (FL-R16) is available (≤ 16 + s₀).
* L9.2: (E), the floors, and (V-c) at every fixed level — the identification of N⁻¹x_jᵀ(I − P_U)μ with a sum of sample
  partial covariances and of its population counterpart with the quantity in (V-R).
* L9.3: the representation J_n(δ_{U,l}, τ_U) = F(g_{U,l}, a_U); (F1); (F2).
* L9.4: the two identities for projecting out V after U₀; the bounds on a, d, R⁻¹ from (L-loc-R) and the Schur
  perturbation; the claim ι_n√log n → 0 from r_n(n log n)^{1/4} → 0; is anything needed about covariances between two
  remote columns, or about truths inside U₀?
* L9.5 — the core: the population regression and the bound on γ² from (L-gain-R); the projection Π and its rank; what
  is 𝒲-measurable; independence of e from W_D; the representation (9.1) and the law of (ξ, R) given 𝒲; the events E_R,
  E_ξ; the monotonicity step; the Gaussian integral and the bound Φ_n. **Is any law asserted after conditioning on an
  event that is not W_D-measurable (E_cov, a sample-covariance event, the scale t_l)?** Does the sample scale t_l of
  column l, or the centring, break the identity ρ̂_{U₀,l} = ⟨m + ẽ, v⟩/‖m + ẽ‖? Is a_{U₀} ≥ a̲ available without E_cov?
* L9.6: the event E and its probability (count of reference pairs); the passage from all (l, U) to reference pairs;
  why the maximum over **all** 15-sets — including sets selected by an X-measurable partition — is covered; Markov;
  the constants C_B and C₆; the claim that for C_L = 0 only tightness is obtained (can you prove more, or show that
  no more is true?).
* L9.7: admissibility of the design set for (T1)(d); the use of Proposition L8.2 with ε_n = 4/log n (through
  `lemmas/L6_COROLLARIES.md` L6.0′) — check that step against the proof of Proposition L5.2; the constant C_R; the case
  p = s₀; the clause C_L = 0 (three ε-budgets).
* Hidden hypotheses: is a global spectral bound, A ≥ 1, |Q| bounded, independence between columns, or a normalised
  floor on sets larger than 16 + s₀ used anywhere? Is (L-R) of `STATEMENT.md` §3.2 used exactly as stated?
* Compare the result with `STATEMENT.md` v1.3.1: bridge row (B-R) and (T3)(b), word by word.
Take Proposition L5.2 (`lemmas/L5_ASM_STARTF.md`), Lemma J (`lemmas/L3_LEAK.md`) and Proposition L8.2
(`lemmas/L8_TRANSFER.md`) as given where L9 cites them, but report any mismatch between what is cited and what those
files state. The file `Theory_work/Wave3/W3-RM/lemmas/L3_SANDR.md` (in the inputs) is a source of the route with
author-only status; nothing may be imported from it.
Also: compare what is proved with what `STATEMENT.md` claims for these items (hypotheses, quantifiers, constants); and
attempt a numerical falsification of your own where it is cheap. The lead's attempts are in `numerics/lemmas/`
(`falsify_L6_L11.R`, `RESULTS_LEMMAS.md`, second half): you may re-run or extend them, and should say if a script does
not test what it says.

## Output format (in your one file)
```
MANIFEST <digest>                      (verbatim first line of the manifest)
Verdict: VERIFIED | VERIFIED-WITH-AMENDMENTS | NOT VERIFIED      (one verdict per lemma file checked)
Findings: numbered; each with class (CRITICAL = a step or claim is false; MAJOR = a gap that needs a new argument or a
          changed hypothesis/constant/statement; MINOR = wording, a constant to adjust, a missing remark), location
          (file:line), the problem, and the exact repair you propose (or "no repair known").
Checks performed: per section, what you re-derived and how; numerical checks you ran and their outcome.
Not checked: list.
```
VERIFIED-WITH-AMENDMENTS means every finding has a local repair that leaves the statement of `STATEMENT.md` unchanged.
End your reply with the verdict line(s) and the path of your file.
