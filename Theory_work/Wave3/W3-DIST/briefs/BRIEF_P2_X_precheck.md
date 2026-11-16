# W3-DIST — same-family pre-check P2 of Lemma X and Lemma X′ — Claude Opus 5.5, Claude Third, effort high

You are an independent line checker. Repo clone `/home/fb31/Bayesian-Variable-Selection`. **Read-only except your one
output file `Theory_work/Wave3/W3-DIST/reviews/P2_opus_precheck_X.md`.** Run no git command, start no agents, effort high
at most. This is a same-family pre-check (a filter before the cross-family line check); it is not a review layer.

## Object
`Theory_work/Wave3/W3-DIST/lemmas/X.md` (v0.2): the proof of Lemma X (§0–§8) and of Lemma X′ (§9). The statements to be
proved are in `Theory_work/Wave3/W3-DIST/STATEMENT.md` §3 ("Lemma X", "Lemma X′", with §0 for the interfaces (E), (C),
(ND), the cutoff m_n(t) and the conventions on s₀ and p). Common definitions: `Theory_work/Wave3/W3-DIST/API_CARDS.md`
("Common definitions"). Inherited, locked source that may be cited: [P1] =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`.
Also readable: `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md` (for §4's denominator step).
Comparison material (independent derivations of the same lemma; unchecked; use them to locate discrepancies, not as
authority): `Theory_work/Wave3/W3-DIST/lemmas/X_route_a.md` and
`Theory_work/Wave3/W3-DIST/work/api_attempts/dist1/X-a-1.md`, `X-a-2.md`, `X-b-2.md`, `X-d-1.md`.
Do not read `reviews/`, `LOG.md`, `CHECKPOINT_*.md`, `DEPS.*` of the ticket. Ignore §10 of X.md as evidence (it is the
author's own notes); you may use its list of unchecked items as a to-do list.

## Task: check every line; try to break the proof
1. For each numbered step of §0–§9: is each inequality correct as written, with the stated constants? Recompute the
   key ones: the exponent A(1 − λ) − λ/2; λ₁ ≤ 1 − 1/(8A + 4) from condition (c); det(I − λ₁D′)^{−1/2} ≤ (1 − λ₁)^{−(s₀+j)/2}
   (rank and eigenvalue range of D′_J); Jensen with (ND); the geometric sum and K_s; A_n; C₅; the Markov step at power
   λ with the indicator of 𝓔_t; §4's cutoff arithmetic R_m√(D_{S₀})√n ≤ 2n^{−1/2}e^{−3t} from the definition of m_n(t);
   §5's Δ and the bound ν log(1 + ·) ≥ 3t; §6's bounds on β_S, v and θ.
2. Every citation of [P1]: does the cited statement exist and say what is used (hypotheses included — e.g. `lem:den`'s
   proof is used with R_n replaced by ρ′; `thm:Ta` needs the event 𝓑_n; `lem:num` needs a data-free b)?
3. Uniformity: is there really one n₀ for all t in [M₀ log n, n^{1−κ₀}] (conditions (a)–(g) imposed at t = n^{1−κ₀}: is
   each condition monotone in t)? Do the constants depend only on (s₀^r, A, σ², M, M′, c_D, κ₀)? Is the case s₀ = 0
   covered at every step? Is S₀ ∈ Ω used where needed? Are sets S ∪ S₀ outside Ω handled correctly? Is (ND) used only
   on its stated range?
4. Does §7 prove exactly the statement of Lemma X in STATEMENT §3 (the three-part bad set including |S| > d_t with
   d_t = s₀ + ⌈C′t/log n⌉, the probability 2e^{−ct}, the posterior threshold e^{−ct})?
5. §9 (Lemma X′): check each modified step, in particular the variance step with t′ = t log n and the claim that the
   thresholds may use ℓ_n = log(p_raw ∨ n) ≥ log n.
6. Where X.md and a comparison derivation disagree on a step that both need, say which is right.

## Output (`reviews/P2_opus_precheck_X.md`)
Findings with id, severity (CRITICAL / MAJOR / MINOR / NIT), section and line of X.md, the error or gap in full, and the
minimal repair. A verdict per section (§1 V(a), §2 X1, §3 X4(b,c), §4 X4(a), §5 X3, §6 X2, §7 assembly, §9 X′):
VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Final line: overall verdict. Do not soften findings; if you could
not check something, say exactly what.
