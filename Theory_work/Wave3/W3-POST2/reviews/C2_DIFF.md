# W3-POST2 — C2 diff round: what changed since council C1

Prepared 2026-11-15 by the C2 review sub-agent (Claude Opus 5.5, high, Claude Third, Owls) for Theory HQ, under
`Theory_work/Wave3/PROTOCOL_v4.md` §5.5. Worktree `theory/W3-POST2-diff` at `origin/main` = `3333e0c`.
Paths are relative to `Theory_work/Wave3/W3-POST2/` unless stated. Line numbers are those at HEAD (= the frozen
`reviews/MANIFEST_C2.txt` content).

## 1. Where the C1 state is, and whether it can be pinned

**The C1 state cannot be pinned exactly.** Evidence:

- `git log --all --follow` on `Theory_work/Wave3/W3-POST2/` shows only two commits:
  - `92f6798` (2026-11-10 21:20, "W3-POST2: council C1 passed (8.6 / 8.6); HQ approvals pending") — the **first** commit
    of the ticket. It already contains `reviews/C1_council_*.md`, `reviews/C1_disposition.md`, STATEMENT **v1.2.1**
    ("v1.2.1 = post-council C1 wording/bookkeeping") and LOG step 17 ("Post-council: STATEMENT v1.2.1, per-file check
    records, Lemma E0, intercept remark …"). So `92f6798` is the **post-disposition** state, not the state C1 read.
  - `eb1f9da` (2026-11-11 09:00) — the PC1/PC2 D(b) repair (plus the two Sol review files).
  - Nothing has touched the ticket since: `git diff eb1f9da HEAD -- Theory_work/Wave3/W3-POST2` is empty.
- No unreachable commit, stash or other worktree holds an earlier copy (`git fsck --unreachable`: none of the 10
  dangling commits differs from `eb1f9da` in this folder). Every `D_hellinger.md` on Owls is byte-identical to HEAD.
- The C1 seats worked on another machine (seat A's review cites a `C:/Users/felip/...` path; the scratch folders
  `reviews/C1_scratch_*` hold only check scripts, no package copy). No session transcript on Owls contains the
  pre-council text.
- What C1 read, per the seats: "STATEMENT v1.2, ASSUMPTION_MAP v1.3", lemmas A–E, numerics, citecheck (120 checks), the
  review trail (both C1 reviews, first paragraph).

**Best-evidence reconstruction.** The diff since C1 has two layers:

| layer | from → to | how it is known | exact? |
|---|---|---|---|
| L1 — C1 dispositions | C1-read state (not in git) → `92f6798` | `reviews/C1_disposition.md` (lead's list), the seats' quotations of the old wording in `C1_council_astra.md` / `C1_council_opus.md`, the `[C1B-k]` tags in the files, LOG step 16–17, and Sol's inventory `reviews/PC1_postcouncil_diff_sol.md` (which reviewed `92f6798` against the same evidence). | **No.** An inventory of every recorded change, located at HEAD lines; not a byte diff. |
| L2 — D(b) repair and P2/P3 propagation | `92f6798` → `eb1f9da` = HEAD | `git diff 92f6798 HEAD`, saved as `reviews/C2_diff.patch` | **Yes.** |

`reviews/C2_diff.patch` is therefore `git diff 92f6798 HEAD -- Theory_work/Wave3/W3-POST2`, with `92f6798` the
best-evidence base: the earliest recorded state, and the state PC1 reviewed. It covers L2 only. L1 is given as the
table in §3, which every seat must treat as part of the diff.

## 2. Files changed since C1

| file | L1 (dispositions) | L2 (repair, in the patch) | in MANIFEST_C2 |
|---|---|---|---|
| `STATEMENT.md` | yes (v1.2 → v1.2.1: header, B relation, intercept sentence, c₀ < c₁ grid) | — | yes |
| `REPORT.md` | yes (council record, scope flag, numbering map, N2/N4/predictive wording, relation labels, registry blocks, E0 pointer, intercept pointer, citecheck pointer) | — | yes |
| `ASSUMPTION_MAP.md` | yes (N2, N4 rows; SL exponent α) | yes (lines 14, 59–60) | yes |
| `lemmas/A_occam.md` | yes (check record; STATEMENT version pointer) | yes (lines 33–34) | yes |
| `lemmas/B_tail_approx.md` | yes (check record; Remark 4 citation) | — | yes |
| `lemmas/C_expectation.md` | yes (check record) | — | yes |
| `lemmas/D_hellinger.md` | yes (check record; D3 cutoff sentence citing E0; D4 Remark 0 intercept; SL exponent α) | yes (lines 53–54: the D(b) cutoff chain; lines 96–98: Remark 2 wording) | yes |
| `lemmas/E_visibility.md` | yes (check record + kill-budget note; **Lemma E0 new**, lines 15–20; E1(b) cites E0, line 46) | — | yes |
| `numerics/post2_checks.py` | yes (N5 header text only) | — | yes |
| `numerics/post2_checks_out.txt` | yes (regenerated; N5 header) | — | yes |
| `LOG.md` | yes (steps 16–17; clock-time erratum) | — | no (excluded by `manifest.py`) |
| `reviews/CITECHECK.txt` | yes (re-run: 120 → 136 checks, 0 failures) | — | no (reviews/) |
| `reviews/C1_disposition.md` | new | — | no (reviews/) |
| `reviews/PC1_postcouncil_diff_sol.md`, `reviews/PC2_repair_check_sol.md` | — | new | no (reviews/) |
| `PLAN.md`, `citecheck.py` | no recorded change | — | yes |

## 3. Every change, located at HEAD

Class: **M** = mathematical content (new or changed proof step, statement, relation or numerical assertion);
**W** = wording / evidential strength; **R** = record / bookkeeping. "Finding" = the C1 finding it answers.

| # | finding | layer | HEAD location | class | change |
|---|---|---|---|---|---|
| 1 | A-1, B-1 | L1 | `REPORT.md:22-35`; `lemmas/E_visibility.md:3` | R | scope flag lists three effects (items 3, 4, and item 5 (ID) → (ID^M) via D+'s ridge lemma); "No other ranked proposal was adopted"; HQ authorisation and kill budget left to HQ; E records v1 = proof attempt, v2 = restatement under K2 |
| 2 | A-2 (N4) | L1 | `REPORT.md:156-158`; `ASSUMPTION_MAP.md:28` | W | N4: achieved margins 3.67–3.99 × log n, δ/r_n 0.75–1.18, no universal constant |
| 3 | A-2 (N2) | L1 | `REPORT.md:149-150, 193`; `ASSUMPTION_MAP.md:27` | W | N2: "consistent with strict weakening (ADG) → (OS); no asymptotic proof for this example" |
| 4 | A-2 (N2), PC1 P2 | **L2** | `lemmas/A_occam.md:33-34`; `ASSUMPTION_MAP.md:14` | W | same N2 qualification propagated (finite-n evidence only, no asymptotic proof) |
| 5 | A-3, B-9a | L1 | `REPORT.md:180`; `reviews/CITECHECK.txt:1` | R | citecheck count from the re-run (now 136 / 0) |
| 6 | B-2 | L1 | `lemmas/A_occam.md:3`, `B_tail_approx.md:3`, `C_expectation.md:3`, `D_hellinger.md:3`, `E_visibility.md:3` | R | per-file check records written; status words unchanged |
| 7 | B-3 | L1 | `STATEMENT.md:3-5`; `REPORT.md:41-42` | R | brief numbering ↔ W3-POST REPORT §4 map |
| 8 | B-4 | L1 | `lemmas/D_hellinger.md:84-88` (D4 Remark 0); `STATEMENT.md:118-119`; `REPORT.md:95-96` | **M** | intercept-inclusive distance h̄_int: h̄²_int ≤ (v/σ*² − 1)² + ‖μ̂ − μ‖²/(4nσ*²) + ε̄²/(4σ*²); "D(a), D(b) hold verbatim" |
| 9 | B-5 | L1 | `lemmas/E_visibility.md:15-20` (**Lemma E0**, new, with proof) | **M** | m♯_n ≥ min(B, K) for n ≥ n₀(s₀, A, B), any fixed B ≥ s₀ + 1, uniformly in 2 ≤ p ≤ n^A |
| 10 | B-5 | L1 | `lemmas/E_visibility.md:46` | **M** | E1(b): \|J′\| ≤ min(j₀, K) ≤ m♯_n by Lemma E0 (B = j₀) |
| 11 | B-5 | L1, then **L2** | `lemmas/D_hellinger.md:52-55` | **M** | D3 cutoff for near underfits, via E0 with B = s₀ + j₀. **L1 text (at `92f6798`):** "…has \|S\| ≤ s₀ + j₀ − 1 ≤ min(s₀ + j₀, K) ≤ m♯_n for n ≥ n₀, by Lemma E0…" — false when K < s₀ + j₀ − 1 (PC1 P1: p = K = 2, s₀ = A = 1 gives 4 ≤ 2). **L2 repair (HQ, 2026-11-11):** "…has \|S\| ≤ s₀ + j₀ − 1, as S₀ ⊄ S and \|S∖S₀\| ≤ j₀, and \|S\| ≤ K, as S ∈ Ω; so \|S\| ≤ min(s₀ + j₀ − 1, K) ≤ min(s₀ + j₀, K) ≤ m♯_n for n ≥ n₀ [HQ repair 2026-11-11, PC1 P1], by Lemma E0…". Checked so far only by one Sol reviewer (`reviews/PC2_repair_check_sol.md`). |
| 12 | B-6 | L1 | `REPORT.md:113-122` | R | one relation label per registry row |
| 13 | B-7 | L1 | `STATEMENT.md:79-80`; `REPORT.md:119, 228` | **M** | Claim B relation strengthened: implies [W3P] Lemma 1a′ **and Lemma 1a** (B ≤ M + M/(2φ₀²), Θ♯ ≤ Θ″) |
| 14 | B-8 | L1 | `STATEMENT.md:136`; `REPORT.md:122` | **M** (numerical) | c₀ < c₁ checked on s₀ ≤ 20, A ∈ [1, 10], min c₁/c₀ = 1.23 (grid observation) |
| 15 | B-9 | L1 | `lemmas/A_occam.md:4`; `numerics/post2_checks.py:263`, `numerics/post2_checks_out.txt:58, 66`; `ASSUMPTION_MAP.md:44`, `lemmas/D_hellinger.md:91-92` | R | STATEMENT v1.2 pointer; N5 header text (output regenerated); SL dimension exponent ξ → α |
| 16 | B-10 | L1 | `REPORT.md:55-56` | W | "rank loss costs nothing in the χ² part; still charged through the determinant ratio" |
| 17 | B-10, PC1 P3 | L1 + **L2** | `REPORT.md:161-162` (L1); `ASSUMPTION_MAP.md:59-60`, `lemmas/D_hellinger.md:96-98` (L2) | W | D(a)'s 1/n mean scale "argued (D4 Remark 2), no lower bound proved" |
| 18 | B-11 | L1 | `REPORT.md:202-254` | R | per-claim registry blocks appended |
| 19 | B-12 | L1 | `lemmas/B_tail_approx.md:54` | R | Remark 4 cites the proof line Σ_{k>m} q_k ≤ 2^{−m} of [P1] `lem:prior`(c) |
| 20 | — | L1 | `REPORT.md:6-20, 168-200`; `STATEMENT.md:1`; `LOG.md:39-46` | R | council result and completion trail; LOG clock times → step numbers (erratum) |

No other change is recorded. No hypothesis, rate or constant of a stated claim changed (the lead's statement in
`C1_disposition.md`; PC1 agrees). The M-class changes (#8–#11, #13, #14) are the ones the seats must check
line by line; the dependents of each are in `reviews/C2_DEPENDENTS.md`.
