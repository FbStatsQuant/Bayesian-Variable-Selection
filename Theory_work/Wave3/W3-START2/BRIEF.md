# W3-START2 — the four BT2 improvements of W3-START (statement v1.4)

Lead: Claude Fable 5.2, effort high, Claude Work. Branch `theory/W3-START2`, created FROM `theory/W3-START` (local ref;
W3-START is council-passed, acceptance pending only on INFRA R05). Folder `Theory_work/Wave3/W3-START2/` — new files
there; do NOT edit `Theory_work/Wave3/W3-START/` (frozen, council-passed). Commit on your branch only; HQ merges.

## Read first
- PROTOCOL.md (rules 9–16), INFRA/LIFECYCLE.md §4.1 (supersession by implication), templates.
- `Theory_work/Wave3/W3-START/` on branch theory/W3-START: STATEMENT.md v1.3.4, lemmas/ (L9_BR, L10_INTERFACES, …),
  REPORT.md, CHECKPOINT_3.md, reviews/BT2_better_theorem_astra.md and **reviews/BT2_disposition.md** (the lead's check
  of each proposal with file:line evidence).

## Target: statement v1.4 with BT2-P1…P4 (open items W3-START-O4…O7)
- P1: leading functional — for s₀ ≥ 1 replace 15√(2/π)z_n/p of 𝔏⁰_n(h) by 1/p in (T1)(b), (T1)(d), (T3)(a), IF-START;
  F2 without p/√log n → ∞.
- P2: Proposition OVL under (V-m) as well as (V-c).
- P3: non-vacuous partition-free leaking-null limit for 1 ≤ s₀ ≤ 15 (17 − s₀ designated nulls) in NEC (N2).
- P4: (T3)(b) with |Q| ≤ n^{1/2−ε_Q} (and |Q| ≤ K) instead of (log n)^{κ_Q}; |H_l| stays polylogarithmic.
New claims supersede START-F, F2, TRANSFER, IF-START, OVL, NEC, BR, START-R by implication (LIFECYCLE). Each change
re-proves only the steps it touches (cite W3-START lemma lines for the rest). Design-agnostic; asymptotic; p ≫ n.

## Legs (pre-approved; advance when reviews are clean — no open FATAL/MAJOR, council ≥ 8.0)
CP1: STATEMENT v1.4 + Sol statement lock (codex gpt-6.1-sol high, blind). CP2/final: proofs of the changed steps, two
Sol line checks, council (Sol + Opus 5.5 on claudeAgent high) on one frozen manifest, CHECKPOINT_2 with registry block.
Manifests per PROTOCOL (`tools/manifest.py freeze/bind`); INPUTS never lists wave documents or registry tables.

## Operating rules
HOLDS.md before each step. Sol/Astra on `codex`; Claude helpers only on `claudeAgent`, effort ≤ high; NEVER
claude-personal. No NOTS. Stay in your run while reviewers work. Be token-efficient (the CW window is shared). End your
run at each checkpoint with a ≤ 200-word summary.
