# BRIEF — line check LC-B (seat: Codex gpt-6.1-sol, reasoningEffort high) — anchored eigenvalues and supersets; new agent, blind

**Object:** `STATEMENT.md` v1.1 (LOCKED), sha256 a2e399a8d30873713a950f5c16de58614901dbf6f8ad9d6e40285f8556ae6bef; `sources/W1-T03R/PROOF.md` sha256 1497376391655759bb8d0479b4f344c10f3c9e1a476182cd1881ee28868e9bd4.

**Write exactly one file:** `Theory_work/Wave3/W3-T03ACC/reviews/LC_B_line_check_sol.md`.

## Your batch (proof under review: `sources/W1-T03R/PROOF.md`)
| step | lines | notes |
|---|---|---|
| Hypotheses SE_λ(j₀), SE_w(m; g₀) and the claim that the locked SE implies them | `PROOF.md:127-134` | |
| Lemma I (interlacing) | `PROOF.md:136` | |
| Lemma B (B1), (B2), (B3) | `PROOF.md:138-145` | |
| (C1) Setting | `PROOF.md:170-172` | uses E2(i) (`:52`) and [P3] `eq:mn` — take E2(i)'s statement as given (it is checked in another batch) |
| (C2) Ranks and laws; 𝒢_n and `lem:Gprob` unchanged | `PROOF.md:174` | |
| (C3) `lem:ongood`(c) restricted; (a), (b), (d) unchanged | `PROOF.md:176` | |
| (C4) `lem:onesup` modified | `PROOF.md:178-181` | |
| (C5) `prop:sup` modified | `PROOF.md:183-185` | |
| [P3] consumed results | `sources/P3/PROOF_v2.tex:1-279`: setting and `eq:mn` (`:36-50`), `lem:red`, `eq:score` (`:53-86`), `lem:smoother`, `cor:diff`, `lem:det`, `lem:prior`, `lem:chi` (`:87-168`; `lem:signal` `:146-153` statement only — its proof is in LC-C), §`sec:good` with `lem:Gprob`, `lem:ongood` (`:169-224`), §`sec:sup` with `lem:onesup`, `prop:sup` (`:225-279`) | check each proof, with every SE use replaced as (C2)–(C5) say. For [P1] `lem:spec`(e) and `lem:chi` (cited by (B1)/(C5)) check that the cited statement covers the use; their proofs are in another batch |

## Named points to check (the lead asks for an explicit answer on each)
- **N1.** `PROOF.md:9`: p = 1 dismissed as "trivial or void". Does anything in §4 or (C1)–(C5) need p ≥ 2? For p = 1
  (s₀ = 1, K = 1) is (C1)'s m♯_n ≤ m_n(½ log n) ≤ C_m log n available directly (m♯_n ≤ K = 1)?
- **N2.** `PROOF.md:172` with `:50`, `:59`: (C1) cites E2(i) without its side condition n ≥ 5 when s₀ = 0. Moot under
  STATEMENT's s₀ ≥ 1? Otherwise absorbed in n ≥ n₀?
- **N3.** (C2)/(C3)/(C4): [P3] states `lem:ongood`(a),(b),(d) and (G1),(G2) "under SE". Confirm from their proofs that
  no eigenvalue condition is used, and that (G2) covers |T| ≤ m♯_n + s₀ as (C4) needs.
- **N4.** (C5)(b): with g₀ fixed, is q_n ≤ ½ placeable in n₀, and is q_n² = c_q² r_n² · n/(n+1) · e^{2ε_n}/4 right?
- **N5 (same A).** The record allows any fixed $A$ (STATEMENT §4 item 3); the inherited bundles say $A\ge1$. Check
  every step of the batch at the recorded $A$, with $j_0$, $C_*$, $c_0$ as defined at that $A$: in particular the
  polynomial union bounds of [P3] `lem:Gprob` (`PROOF_v2.tex:190-194`), $C_m$ in `eq:mn`, and (C1). Does any step use
  $A\ge1$ (or $p\ge n$, or $\log p\ge\log n$)? If yes, name the line and whether it is repairable locally.

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
