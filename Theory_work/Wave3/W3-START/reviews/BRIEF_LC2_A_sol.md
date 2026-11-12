# BRIEF — lemma line check LC2-A (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent cross-family reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole
brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START`. Paths below that start with `lemmas/`,
`numerics/`, `reviews/` or are `STATEMENT.md`, `PLAN.md`, `BRIEF.md`, `ASSUMPTION_MAP.md` are relative to the ticket
folder `Theory_work/Wave3/W3-START/`; all other paths are relative to the worktree root. **Change no git state. Write
exactly one file:** `Theory_work/Wave3/W3-START/reviews/LC2_A_line_check.md`. Do not edit any other file in the repository. Do
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

## Your task: line-by-line check of L6, L7 and L8
Object: `lemmas/L6_COROLLARIES.md` (Lemma L6.0, Corollary L6.0′, Corollaries F1–F4), `lemmas/L7_NEC.md` ((C2)(i), (ii); Proposition NEC (T4)) and `lemmas/L8_TRANSFER.md` (Proposition L8.2; Theorem (T3)(a)).
The proofs are by the ticket lead and are unchecked. **You are briefed to break them.** Read every line; re-derive
every displayed inequality and every constant; check that each step uses only what is available at that point
(hypotheses of the statement, earlier steps, or a cited result of another lemma file of this ticket, whose statement
you should read; the files L1–L5 may be taken as given where they are cited, but report any mismatch between what is
cited and what they state). The ticket consumes **no** registry claim: nothing may be imported as a premise from
another ticket. In particular check:
* L6.0 / L6.0′: open `lemmas/L5_ASM_STARTF.md` and check that the proof of Proposition L5.2 uses ε **only** through the
  requirement 2e^{−n^{1/3}} + 2/n + 1/log n ≤ ε/2, so that ε may depend on n as claimed; the constants λ_n, c_{0,n}, C_n, C′_n.
* F1: the exponent of 𝔏_n(Q) from (J2), including the o(1); that (AL) follows; that ϱ_n(Q) ≤ c_{0,n} eventually; the final
  display with probability → 1; the case η = 0. F2: the lower bound Δ_U ≥ φ₀²θ_lo² (Schur complement, also for s₀ > 16);
  the use of (J1) and its prefactor; why p/√log n → ∞ and n^{−1/2}𝔏_n(S₀)² → 0 are needed; (AL); the exact-order claim. F3:
  the constant C₂ and the absorption of C_n. F4: that the arithmetic of `lemmas/L3_LEAK.md` L3.5 is all that is needed.
* L7: in (C2)(i) — feasibility of S₀ ∪ {l}, the prior factor, the lower bound (f1) with gains of arbitrary size, the
  single Gaussian event, the exponent bookkeeping with Ā = limsup; in (C2)(ii) — the prior factor (2p − s₀)/s₀, the
  upper bound (f3) and why the gain is small enough, the exponent bookkeeping with A̲ = liminf. (N2), (N3) as
  consequences, the scope paragraph of (N2) (premise empty for s₀ ≤ 15; give your own check that it is non-empty for
  s₀ ≥ 16), and whether (N3)'s example is right. Does either part use visibility, (AL), or a hypothesis not listed?
* L8: measurability and the identification of the conditional law with Setting F (L8.1); Proposition L8.2 — is the
  bound P(B) ≤ P(X^r ∉ 𝒳) + ε + b̄ correct, are the constants really free of the design-dependent objects, is anything
  about the response allowed to enter θ*, S₀, Q, h; the passage to the O_P/o_P form; that Setting R and a deterministic β
  are special cases. Compare with `STATEMENT.md` (T3)(a) word by word.
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
