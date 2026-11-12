# BRIEF — statement change check SC3 (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START` (all paths below are relative to it). **Change no git
state** (read-only git commands such as `git show` and `git diff` are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-START/reviews/SC3_change_check_sol.md`. Do not edit any other file. Do not start subagents. Use no
effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_SC3.txt`. Its first line is
`MANIFEST bf619625bf0880c6dd270771fcd0e9c94c9eeb268e75212cb918c8ab5a24dd61`. **Quote this digest line verbatim at the
top of your review.** You may run `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START
Theory_work/Wave3/W3-START/reviews/MANIFEST_SC3.txt` and report its result.

## Files you may read
Only the files listed in that manifest: `Theory_work/Wave3/W3-START/STATEMENT.md` (v1.3, the object under review),
`PLAN.md`, `ASSUMPTION_MAP.md`, `BRIEF.md`, the `numerics/` folder of the ticket, and the 23 external inputs listed in
`Theory_work/Wave3/W3-START/reviews/INPUTS.txt` (pinned code, wave documents, premise sources and consumers). In
addition you may read the **previous version of the statement** with
`git show HEAD:Theory_work/Wave3/W3-START/STATEMENT.md` (v1.2) and compare (`git diff HEAD --
Theory_work/Wave3/W3-START/STATEMENT.md`). Do not read any other file in any `reviews/` folder (except the manifest
and INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`.

## What this review is
Nothing in STATEMENT.md is proved yet; it fixes the target of the proof work. Version 1.2 was the locked target.
Version 1.3 makes three changes of substance:
1. **Gram floor.** The normalised small-set floor (FL-16), λ_min(R̂_T) ≥ φ₀², is replaced by the constant unnormalised
   floor (GF-16), λ_min(X_TᵀX_T) ≥ g_*, for 1 ≤ |T| ≤ 16. The toolkit is to be re-proved in this ticket (Lemma TK,
   bridge (B-TK)); the registry claims C-GROW:L0.1, L0.2 are no longer consumed.
2. **Column truncation levels.** The leakage functionals J, 𝔏_n(Q; h), 𝔏⁰_n(h), ϱ_n(Q; h) carry a level vector h
   (1 ≤ h_l ≤ z_n, tail budget b_n(h)); (AL), [LEAK(Q)], (C1), (B-L), (T1), (T5) are restated with h; the default
   h ≡ z_n is the v1.2 form; Corollary F4 is new.
3. **Transfer.** (T3)(a), and the random-candidate clause of (T6), allow coefficients, support, leakage set and levels
   that are measurable functions of the design.

You are briefed to break the changed statement. Check, with file:line evidence:
A. **Completeness of the diff.** List every difference between v1.2 and v1.3. Is any change outside the three items
   above (other than the header, the dependency paragraph, the examples table and the "Not claimed" list)? Is any
   place left inconsistent (a leftover use of the old floor, a functional without the level vector where it matters, a
   constant list that still names φ₀ where g_* is meant, a claim whose hypothesis list was not updated)?
B. **Well-posedness of each changed definition and claim.** Level vectors and the tail budget (what they may depend
   on; the default bound b_n ≤ 1/(32 log n)); J_h and the bounds (J0)–(J3) for every h ≥ 1 — verify them by algebra or
   numerical integration; 𝔏^{b,0}_n(h) ≤ 𝔏⁰_n(h) and 𝔏^b_n(Q; h) ≤ 𝔏_n(Q; h), including s₀ = 0 and the term for the
   ≤ 15 nulls sharing a block with all of S₀; the quantifiers of (T1)(d) with the exceptional probability ε + b_n(h);
   the quantifiers and the conditioning in (T3)(a).
C. **Plausibility / quick falsification of each changed claim.**
   * (GF-16): from the pinned scorer (`Scripts/SMC_BVS/core/cpp/v3_score.h:204-224`), verify or refute the two scalar
     bounds displayed in bridge (B-TK) for a Gram matrix with eigenvalues ≥ g_*: the determinant-ratio bound and
     0 ≤ Q_U − RSS^y_U ≤ 1 + 1/g_*. Does any claim of v1.3 still need a **normalised** floor without stating it (for
     example the lower bound on unexplained signal in F2, the Gaussian-row bridge (B-R), (C2)/(T4), Proposition OVL)?
     Does [TK] as now stated (RSS_U = (n − 1)τ²_U(1 + o(1)) uniformly, bounded score remainder) plausibly follow from
     (E) and (GF-16) alone?
   * Levels: does the small-gain consequence quoted under (AL) still follow from (J0) for every admissible h? Is the
     union count behind b_n(h) right (a column has at most 2¹⁵ conditioning sets inside a block of size ≤ 16;
     P(|Z| > h) ≤ 2e^{−h²/2})? Check the arithmetic of F4: b_n(h) → 0 for the stated levels, the exponent
     (1 + 2A̲ − c)/2, and the remark on the default levels. Try a small example or limiting case (p bounded, p ≫ n,
     |I_n| = 1, c close to 1 + 2A̲, Q ≠ S₀).
   * Transfer: is (T3)(a) a correct consequence of a uniform fixed-design statement of the form (T1)(d)? Is anything
     about the response allowed to leak into θ*, S₀, Q or h? Is the new clause of (T6) covered by (T3)(a) and by the
     reduction stated there?
D. **Dependencies and protocol.** With "Consumed: none", is anything below PROVED-CHECKED still used silently
   (`Theory_work/Wave3/PROTOCOL.md` rule 11)? Are the statuses quoted in §7 verbatim from
   `Theory_work/INFRA/registry/claims.tsv`? Do the consumers' interfaces (W3-SAMP P-START, P-OVL) still receive what
   (T5) says?
E. **Design-agnostic form.** No design family in any statement; theorem hypotheses partition-free.

## Output format (in your one file)
```
MANIFEST <digest>            (verbatim first line of the manifest)
Verdict: ACCEPT | ACCEPT WITH CHANGES | REJECT
Required changes: numbered; each with location (file:line), the problem, and the exact change you require.
Optional suggestions: numbered.
Checks performed: what you verified and how (algebra, code reading, numerical integration, counterexample attempts).
Not checked: list.
```
Classify each required change as CRITICAL (a claim is false or ill-defined), MAJOR (a hypothesis or scope must
change) or MINOR (wording, citation, missing definition). Use REJECT only if a CRITICAL change cannot be made by a
local edit of the statement; otherwise use ACCEPT WITH CHANGES and give the exact edits. Do not propose a different
theorem. End your reply with the verdict line and the path of your file.
