# BRIEF — line check LC-A (seat: Codex gpt-6.1-sol, reasoningEffort high) — size tail; new agent, blind

**Object:** `STATEMENT.md` v1.1 (LOCKED), sha256 a2e399a8d30873713a950f5c16de58614901dbf6f8ad9d6e40285f8556ae6bef; `sources/W1-T03R/PROOF.md` sha256 1497376391655759bb8d0479b4f344c10f3c9e1a476182cd1881ee28868e9bd4.

**Write exactly one file:** `Theory_work/Wave3/W3-T03ACC/reviews/LC_A_line_check_sol.md`.

## Your batch (proof under review: `sources/W1-T03R/PROOF.md`; definitions at `:9` and STATEMENT §1)
| step | lines | notes |
|---|---|---|
| E1 (a), (b), (d) | `PROOF.md:13-40` | (c) is used only by E2(iii)/E3: confirm that, do not check (c) |
| Definition of m♯_n(ω); existence and m♯_n ≤ K | `PROOF.md:44-47` | |
| E2(i) | `PROOF.md:49-59` (statement `:52`, proof `:59`) | E2(ii),(iii), E3 (`:63-70`) are not used by T03♯: confirm by reading `:160-207`, do not check them |
| Lemma den′ | `PROOF.md:89-91` | extracted from the **proof** of [P1] `lem:den`, not its statement: re-derive it from `PROOF_v3.tex:324-361` |
| Theorem T02(i♯) and its proof | `PROOF.md:74-101` | the quantifier is sup_m P₀(·); the consequence for deterministic ω_n |
| [P1] consumed results | `sources/P1/PROOF_v3.tex`: §1 setting `:40-59`; `lem:slab`, `lem:IGint`, `lem:spec`, `lem:prior`, `lem:chi` `:60-152`; `prop:closed`, `thm:T01i` `:153-210`; `thm:T01ii` `:213-222` (used by `thm:Ta`; chain `thm:Ta` ← `thm:T01i`, `thm:T01ii`; `thm:T01i` ← `prop:closed` ← `lem:slab`, `lem:IGint`); `lem:spec`(a)–(e) all count ((c) is used inside `lem:den`); `thm:T01iii` `:232-252`; `thm:Ta` `:253-268`; `lem:num`, `lem:den`, `thm:T02i` `:313-384` | check each proof; `thm:T01iv`, `thm:Tb1`, `thm:Tb` and §T02(ii) (`:385-476`) are **not** in this batch |

## Named points to check (the lead asks for an explicit answer on each)
- **N1.** `PROOF.md:9` says "for p = 1 every statement below is trivial or void". E1(b) and E2(i) divide by p − 1. Is the
  p = 1 case (s₀ = 1, K = 1) genuinely covered for what T03♯ needs from §1 (m♯_n ≤ min{K, m_n(½ log n)})? Proposed
  local repair: for p = 1, K = 1, so m♯_n ≤ K = 1 ≤ m_n(½ log n) directly. Confirm or reject, and say whether anything
  else in §§1–2 needs p ≥ 2.
- **N2.** `PROOF.md:79-80` with `:16`: R_m is written as Σ_{k=m+1}^K q_k/w(s₀) "for every integer m", but q_k is defined
  only for 0 ≤ k ≤ p. For m < 0 the sum must be read with lower limit max(m + 1, 0) (STATEMENT §2), i.e.
  R_m = ϖ(Ω)/ϖ(S₀). Does T02(i♯) hold for every integer m under that reading, and is the sup over m affected?
- **N3.** E2(i)'s side condition (n ≥ 5 if s₀ = 0): irrelevant under STATEMENT's s₀ ≥ 1? Confirm.
- **N4 (same A).** STATEMENT §4 item 3: the record allows any fixed $A$. Does any step of this batch (including [P1])
  use $p\le n^A$ or $A\ge1$? (`PROOF.md:99` says $p\le n^A$ is not used by T02(i♯): confirm.)

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
