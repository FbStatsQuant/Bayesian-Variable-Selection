# BRIEF — line check LC-C (seat: Codex gpt-6.1-sol, reasoningEffort high) — underfitting models and assembly; new agent, blind

**Write exactly one file:** `Theory_work/Wave3/W3-T03ACC/reviews/LC_C_line_check_sol.md`.

## Your batch (proof under review: `sources/W1-T03R/PROOF.md`)
| step | lines | notes |
|---|---|---|
| (C6)(a) crude bound, no eigenvalue condition; (C6)(b) | `PROOF.md:187-190` | |
| (C7) `lem:signal`, `lem:signalgain` unchanged | `PROOF.md:192` | |
| (C8) `lem:assemble` modified, with its rate | `PROOF.md:194-197` | uses (C5)(a),(b): take their statements (`:183-185`) as given (checked in another batch) |
| (C9) Step 0 | `PROOF.md:199` | uses T02(i♯) (`:79-84`): take its statement as given (checked in another batch) |
| (C10) Step 1 and (iv): the beta-min constant | `PROOF.md:201` | |
| Assembly and conclusions (i)–(v) | `PROOF.md:168, 203` | every clause of STATEMENT §3 (T03S.1–.5) must follow; say per clause |
| Completeness of the changed / unchanged lists | `PROOF.md:205-207` | is every [P3] use of SE or of H-T02 accounted for? |
| [P3] consumed results | `sources/P3/PROOF_v2.tex`: `lem:signal` with proof (`:146-153`), §`sec:under`: `lem:SvsSp`, `lem:signalgain`, `lem:assemble` (`:280-331`), §`sec:main`: `eq:tail`, Step 0, Step 1, `eq:kappa`, paragraphs (i)–(v) (`:332-396`) | check each proof with the replacements of (C6)–(C10); `cor:diff`, `lem:det`, `lem:prior`, `lem:smoother`, `lem:ongood` are cited from another batch: check that the cited statements cover the uses here |

## Named points to check (the lead asks for an explicit answer on each)
- **N1.** `PROOF.md:168` conclusion (iv): J_n^∞ = {j : θ*_j² ≥ M_nσ*² log n/(nφ₀²)} is written without "j ∈ S₀". Harmless
  because θ*_j = 0 off S₀ and the threshold is positive? Is "J_n^∞ ⊆ J_n(c₀ + 1) eventually" right, and does the
  posterior statement transfer by monotonicity?
- **N2.** (C10): (1 − 1/n)c ≥ L_* for n ≥ c/(c − L_*); BM-∞ ⇒ BM(L_* + 1) eventually; the thresholds then depend on the
  sequence M_n. Correct?
- **N3.** (C8): the multiplicity 2^{s₀}; the e^{ρ_n} factor on the second term; the exponent count
  (j₀ + 1)/2 ≥ s₀(A + ½) + 1 giving the n^{−1} rate. Correct?
- **N4.** Assembly (i): is the split of Ω ∖ {S₀} into {|S| > m♯_n}, supersets of size ≤ m♯_n, and 𝒰 exhaustive, and
  are models S′ = S ∪ S₀ with |S′| > K (outside Ω) handled correctly (ℓ(·) is defined on all of 2^{[p]})?
- **N5.** Clause T03S.3: "P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] → 0" and the strict-maximiser statement on {π(S₀) > ½}.

## Rules (common to LC-A, LC-B, LC-C)
You are an independent, blind line checker for theory ticket W3-T03ACC of the SMC-BVS project. This file is your whole
brief. Work only in the worktree `/home/fb31/BVS-wt/W3-T03ACC` (paths below are relative to
`Theory_work/Wave3/W3-T03ACC/` unless they start with `Theory_work/`). **Change no git state. Write exactly one file**
(named below). Do not edit any other file. Do not start subagents. Effort no higher than high. Scratch files only under
`/home/fb31/SMC_Theory_Department/tmp/20261116-W3-T03ACC-<batch>/` (create it; never /tmp); computations with `nice`,
≤ 4 cores, small and short.

**You may read:** `STATEMENT.md` (the locked statement), this batch's lines of `sources/W1-T03R/PROOF.md` (the proof
under review) and anything they cite in `sources/P1/PROOF_v3.tex` = [P1], `sources/P3/PROOF_v2.tex` = [P3],
`sources/common/00_COMMON.md`, `sources/P1/STATEMENT.md`, `sources/P3/STATEMENT.md`, and the rest of
`sources/W1-T03R/PROOF.md` for definitions. **You may not read:** anything under `reviews/` other than this brief,
`LOG.md`, `CHECKPOINT*.md`, `REPORT.md` files, `sources/W1-T03R/REPORT.md` and `NOTES.md`, `sources/P1/FINAL_REPORT.md`,
`sources/P3/FINAL_REPORT.md`, any other ticket's folder, any earlier verification of this proof, or the web.

**What a line check is.** Check the proof **as written**, line by line. You are briefed to break it. For each step
listed for your batch give one verdict: **VERIFIED** (every line follows, with the hypotheses available at that point),
**GAP** (the conclusion may be true but a line does not follow as written; say exactly which line and what is missing,
and propose the smallest local repair if you see one) or **ERROR** (a line is false; give a counterexample or the
failing computation). Re-derive, do not skim: constants, exponents, index ranges, quantifiers (fixed vs. uniform in m,
J, S; deterministic vs. data-dependent), "for n ≥ n₀" placements, and the exact hypotheses of every cited [P1]/[P3]
result versus what is available where it is cited. A cited [P1]/[P3] result is part of your batch: check its proof
too, unless the batch list says otherwise.

Standing questions for every step: (1) **hidden hypotheses** — is every eigenvalue, rank or full-column-rank fact
supplied by R (λ_min(R_{S₀}) ≥ φ₀²), SE_λ(j₀), SE_w(m♯_n; g₀) or interlacing (Lemma I), for exactly the sets where it
is used? Any use of the locked full SE that survives? Any use of p ≤ n^A, s₀ ≤ K, s₀ ≥ 1, p ≥ 2 or A ≥ 1 not stated
in STATEMENT §2/§4? (2) **uniformity** — is each O_P / probability bound uniform where it is later summed or
maximised? (3) **scope** — is each step's conclusion used downstream only within the range it was proved for?

## Output format (your one file)
```
Batch: <LC-X>   Statement: STATEMENT.md v<version> sha256 <first 16 hex>   PROOF.md sha256 <first 16 hex>
Overall: VERIFIED | GAP | ERROR   (worst step verdict)
| step | file:lines | verdict | note (what you checked; for GAP/ERROR: line, failure, proposed local repair) |
Named points (N1, N2, ...): one paragraph each: confirmed / rejected / moot, with reasoning.
Hidden-hypothesis inventory: every eigenvalue/rank use in the batch → its source hypothesis.
Not checked: list.
```
Tag every GAP/ERROR also C (correctness) / S (strength: uses an unstated hypothesis) / F (faithfulness to a cited
source) / E (editorial: wording or notation only, no mathematical consequence). Give sha256 of STATEMENT.md and
PROOF.md as you read them (`sha256sum`).
