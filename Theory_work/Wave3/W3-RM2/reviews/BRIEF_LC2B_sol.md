# BRIEF — lemma check LC2-B: L5, the Form R bridges and Theorem RM2-R (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent line-by-line checker for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable
selection by sequential Monte Carlo; this ticket proves that the coded method reports the true model S₀ when the set
Q of columns that may "leak" signal has polynomial size n^b). The proof was written by a Claude model; you are the cross-family check. This file is your whole brief. Work only inside
the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state. Write exactly
one file:** `Theory_work/Wave3/W3-RM2/reviews/LC2B_L5_check_sol.md`. Do not edit any other file (scratch files for your own
checks go outside the worktree). Do not start subagents. Use no effort setting above high. All results are
asymptotic (n → ∞); do not flag "asymptotic only" as a defect.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_LC2.txt`; its first line is
`MANIFEST b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6`. **Quote this digest line verbatim at the top of your review.**
Read only files listed in that manifest (the ticket folder except `reviews/`, `LOG.md`, `CHECKPOINT*.md`; and the
external inputs of `reviews/INPUTS.txt`). Do not read any other file in a `reviews/` folder, any `LOG.md` or
`CHECKPOINT*.md`. Markers such as [SL1-#], [MP1-#], [CP2-T6] point to earlier internal rounds whose reports you are
not given; judge the text as it stands.

## Object under review
`Theory_work/Wave3/W3-RM2/lemmas/L5_formR.md`: Lemma P8 (no-addition and truth removal under Gaussian rows from the
width condition (W-R)), Lemma P9a (joint-law bound max Z² ≤ 2 log p + o(log n) on a lattice of polynomial size),
Lemma P9 (joint bound ⇒ conditional Gaussian width; (D-R^b) ⇒ (W-R)), Lemma D-loc^b, Lemma P10 (posterior input, with
the p = 1 endpoint), Theorem RM2-R (claim (C2)) and the containment of the parent theorem RM-R (claim (C4), second
half).
Context you may use: `STATEMENT.md` (v1.4; §1, §3.2, §4 (C2), (C4), bridges (P8)–(P10), §5);
`lemmas/L2_width.md` (**take its lemmas NA-conv, NA-W, TL-W, Lemma d as given** — they were checked in an earlier
round; check that L5 uses them within their hypotheses and that the thresholds n₀ really depend only on
deterministic envelopes); `lemmas/L0_toolkit_b.md` (statements); `lemmas/L4_sandR_b.md` — **take Lemma SAND-R^b and
its §1.1, 1.2(iii), §7 item 1 as given** (another reviewer checks them); the templates
`Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md` and `Theory_work/Wave3/W3-RM/lemmas/L4_formR.md`;
`Theory_work/Wave2/W2-APP/lemmas/L1_POST.md`; `Theory_work/Wave3/W3-RM/STATEMENT.md` (RM-0 at 160-176, RM-R at
187-189, §3.2 at 127-156) and `Theory_work/Wave3/W3-RM/lemmas/L0_core.md`; statuses quoted in L5 §5 are to be
checked against `STATEMENT.md` §5; `numerics/formR_checks.R`, `formR_checks_out.txt` (K11).

## Task
Try to break each lemma. At least:
1. §0 (S2): sample floors on Q ∪ {l} from the entrywise event — is b < ½ enough, is anything else needed?
2. Lemma P8: the conditional application of fixed-design lemmas — is every n₀ uniform over W in the conditioning
   event? Is (BM-W) really available with a deterministic rate? Does TL(𝓛) need anything not supplied?
3. Lemma P9a: go through the five steps of the template at q ≤ n^b: which events use the size, are the union bounds
   over ≤ p·2^q pairs correct with x, v_n = O(q + log n), and is ϵ_n = O((q + log n)/√n) the only place where b < ½ is
   needed? Is the bound (2.1) deterministic on the event, with a deterministic ς_n?
4. Lemma P9: the passage from the joint law to the conditional mean — Markov over W, the level algebra
   (recompute s̲_n), the use of lower-tail concentration only. Is 𝔴_n(δ₀) the mean of the functional used? Is the
   restriction δ₀ < 1 − 2b where it should be?
5. Lemma D-loc^b; Lemma P10 (recompute the p = 1 formula from the D0 score definition in `lemmas/L0_toolkit_b.md` §0;
   is the cited posterior lemma applicable with exactly (T1-R)?).
6. Theorem RM2-R: does the chain deliver every conclusion of (C2) as stated in `STATEMENT.md`? Is the core theorem
   RM-0 of the parent ticket applied within its statement? Containment of RM-R: check each hypothesis implication.

## Output format (in your one file)
```
MANIFEST <digest>
Verdict per lemma/claim: VERIFIED | VERIFIED-WITH-AMENDMENTS | NOT VERIFIED (say which statement falls).
Findings: numbered; each FATAL / MAJOR / MINOR / NIT, with file:line, the problem, and the exact correction or the
  missing argument. A counterexample or a failing numerical test counts as FATAL.
Independent derivations: what you re-derived yourself, step by step, with constants.
Not checked: what you did not verify.
```
End your reply with one line per lemma/claim giving its verdict, and the path of your file.
