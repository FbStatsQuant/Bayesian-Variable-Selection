# BRIEF — lemma check LC2-A: L4, the Gaussian-row sandwich (bridge (P7)) (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are an independent line-by-line checker for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable
selection by sequential Monte Carlo; this ticket proves that the coded method reports the true model S₀ when the set
Q of columns that may "leak" signal has polynomial size n^b). The proof was written by a Claude model; you are the cross-family check. This file is your whole brief. Work only inside
the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state. Write exactly
one file:** `Theory_work/Wave3/W3-RM2/reviews/LC2A_L4_check_astra.md`. Do not edit any other file (scratch files for your own
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
`Theory_work/Wave3/W3-RM2/lemmas/L4_sandR_b.md` — **Lemma SAND-R^b**: under Gaussian rows, small-set eigenvalue floors,
PTV visibility, a deterministic leak set Q with |Q| ≤ n^b, a leak bound ℓ_n = o(√(log n/n)) at **every** conditioning
set of size ≤ 15, a localisation clause with **any** r_n → 0 and neighbourhoods |H_l| ≤ n^ρ, and 15ρ + b < ½, every
maximiser of the start law is sandwiched between S₀ and Q, for any X-measurable partition with blocks ≤ 16.
This is the step of the ticket considered most at risk, and it contains two arguments that are **new** relative to
its templates: (i) §2, the "product form" — the selection-removal cross term is identified with the difference of
the leak covariances at U₀ and at U, so the localisation covariances need no rate; (ii) §3–§4, a spherical tail with
a mean shift of norm o(√log n) and a comparison made on √h with an o(√log n) error.
Context you may use: `STATEMENT.md` (v1.4; §1, §3.2, bridge (P7)); `lemmas/L0_toolkit_b.md` (**take its statements
(T1)–(T5), (E6-tab) as given**; check they are used within their hypotheses); `lemmas/L1_sandF_b.md` (the two
deterministic facts L4 imports: per-block optimality (1.1) and the count (2.1)); the templates
`Theory_work/Wave3/W3-RM/lemmas/L3_SANDR.md`, `L3b_rate.md` and `Theory_work/Wave1C/C-GROW/lemmas/L6_random_AR1.md`
(for comparison only — L4 claims to re-prove every step where a size or a rate enters);
`numerics/formR_checks.R`, `formR_checks_out.txt`, `numerics/RESULTS.md` §6 (K8–K10).

## Task
Try to break the lemma. At least:
1. §1: the covariance event (constants, union bound), the bounded-dimension comparison 1.2(ii) and its uniformity
   over the coefficient box, the identity (1.1) for the add statistic, sample visibility 1.2(v), and the conditional
   use of the toolkit for all sets of size ≤ 16 (is conditioning on W legitimate for a partition chosen from X?).
2. §2 Lemma 2: derive the population identity and the bound (★) yourself. Is it true that (R-G) at U and at U₀ gives
   |c_lᵀS_VV⁻¹c_y| ≤ 4s₀θ_hi ℓ_n with no rate on r_n? Then the sample comparison: is every error term really
   O(ℓ_n + r_nh_n + h_n²)? Look for a term of order h_n·O(1) that would survive when r_n does not tend to 0 fast, a
   denominator that can degenerate, a use of a floor on a set larger than 16 + s₀, or a place where the random
   coefficient vector β* is treated as fixed.
3. §3 Lemma 3: the conditioning (what is measurable w.r.t. σ(W_D, ε), independence of the innovation, no law asserted
   after conditioning on E_cov), the algebra with the mean shift M_n = o(√log n), the range 0 ≤ t ≤ (2A + 3) log n and
   the resulting exponent.
4. §4–§6: the count |I_l| ≤ n^{15ρ}; the passage from J(t) to reference sets; thresholds t_n(k) and T_n and their
   ranges; the ladder (does 15ρ < ½ suffice? uniformity over maximisers); feasibility and truth inclusion; the
   junk-exclusion margin (ε*/2) log n — recompute it.
5. §7 item 1: does the older hypothesis (leak bound only at localised sets, r_n(n/log n)^{1/4} → 0) imply (R-G)?
6. Is the lemma as stated in §0 exactly what `STATEMENT.md` (P7) and (L-R^b) say? Any hypothesis used but not stated?
7. If you can, test numerically a configuration designed to violate (2.1) or (★) (e.g. slowly decaying
   correlations with small neighbourhoods H_l), and report it.

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
