# W3-MEMO-SCR-RM — scoping memo: can certified screening supersede RM's leakage condition? (HQ, 2026-11-11)

You are the **lead** (Claude Fable 5.2, effort high, Claude Personal). Worktree `C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM`
(branch `theory/W3-MEMO-SCR-RM`); folder `Theory_work/Wave3/W3-MEMO-SCR-RM/`. **Change no git state.** Effort never above
high. Read `Theory_work/Wave3/PROGRAM.md` and `PROTOCOL.md` (resume rules 9–16: frozen manifests, blind reads, LOG).

## Question
Can W3-SCR's SCR-C (certified sparse model = S₀) plus a theorem "P(certified ∧ |Ŝ| ≤ q_n) → 1" give a reported-model
theorem **without** W3-RM's leakage condition (L) (and/or without the lattice condition (N)/(D-R)), and so supersede or
strengthen W3-RM? HQ's unreviewed prior: not as stated — SCR-C needs s₀ = O(1) and a near-orthogonality floor
φ_n(q_n) ≥ 2 log p/(2 log p + log n) + ε (`W3-SCR/STATEMENT.md` l.171–178), violated by strong-factor/correlated designs
(CS ρ: φ ≈ 1 − ρ); and P(certified ∧ sparse) → 1 is exactly the search claim RM proves under (V)+(L)+(N). Test this
prior; do not assume it.

Sources: `Theory_work/Wave3/W3-SCR/` (STATEMENT, REPORT, CODE_CHECK — coded meaning of `local_certified`),
`Theory_work/Wave3/W3-RM/` (STATEMENT v1.2.1, REPORT §6 follow-ups A/B, ASSUMPTION_MAP, SHARPNESS), registry rows in
`Theory_work/INFRA/registry/claims.tsv` (cite by id + version).

## Deliverable
`MEMO.md` (≤ 4 pages): (1) side-by-side hypothesis sets of SCR-C/SCR-G and RM-0/RM-F/RM-R, with which implies which;
(2) the exact missing link(s) for supersession, each with the best route you see and a difficulty estimate; (3) regimes
(as conditions on (X, θ*), families only as examples) where SCR-C gives something RM does not, and vice versa;
(4) recommendation among: (a) SCR-C as a corollary / examples row, (b) merge into W3-RM2 (polynomial leakage |Q| ≤ n^b,
b < ¼) with a named lemma, (c) a new ticket — with what each would change in the paper's headline.

Review: freeze a manifest (`python Theory_work/Wave3/tools/manifest.py freeze Theory_work/Wave3/W3-MEMO-SCR-RM
.../reviews/MANIFEST_B1.txt --extra <inputs list>`), then one fresh **Astra** (`delegate_task`, codex `gpt-6-astra`,
reasoningEffort high), blind first read, briefed to break the memo's implications and recommendation; brief saved to
`reviews/BRIEF_B1_astra.md`; it quotes the digest. Write `reviews/B1_disposition.md`, revise the memo (substantive changes
listed), then **end your run** with a ≤ 15-line summary (recommendation, Astra verdict, open points). LOG.md heartbeat
throughout. No other agents.
