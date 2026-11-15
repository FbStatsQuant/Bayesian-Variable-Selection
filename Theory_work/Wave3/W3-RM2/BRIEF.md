# W3-RM2 — reported model under polynomial leakage |Q| ≤ n^b, b < ¼ — lead brief, leg B (HQ, 2026-11-11)

You are the **lead** of ticket W3-RM2 (Claude Fable 5.2, effort high, **Claude Work**). Worktree
`C:/Users/felip/BVS-wt/W3-RM2` (branch `theory/W3-RM2`); folder `Theory_work/Wave3/W3-RM2/`. Work only inside it.
**Change no git state** (HQ commits). Never use effort above high.

## Read first
- `Theory_work/Wave3/PROGRAM.md` (presentation rule) and `Theory_work/Wave3/PROTOCOL.md` (all; **resume rules 9–16 bind
  you**: hard checkpoints, frozen manifests + blind first reads, consumed claims, hold file, heartbeat LOG, kill budgets —
  RM2: 3 failed attempts on the key lemma → STUCK at CP2).
- `Theory_work/INFRA/LIFECYCLE.md` §4.1, `Theory_work/INFRA/templates/ASSUMPTION_MAP.md`, `templates/COUNCIL_BRIEF.md`.
  Consume prior results only by registry id + version from `Theory_work/INFRA/registry/claims.tsv`.
- The parent result: `Theory_work/Wave3/W3-RM/` — STATEMENT v1.2.1 (W3-RM:RM-0, RM-F, RM-R, E4 @1.0.0,
  PROVED-CHECKED), REPORT §6 item 1 (this ticket) and item 2, ASSUMPTION_MAP, SHARPNESS, lemmas/.
- Polynomial-decay precedent: `Theory_work/Wave2/W2-LOC2/`. Metric-local example: `Theory_work/Wave2/W2-UNI/` (UNI-0).
- HQ decision 2026-11-11 (`Theory_work/Wave3/HQ_DECISIONS.md`, memo entry): certified screening (W3-SCR SCR-C) does not
  supersede RM; the two "PL" sketches in the scoping memo
  (`C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM/Theory_work/Wave3/W3-MEMO-SCR-RM/MEMO.md` v2, unreviewed) do **not** give your
  key lemma. Read them as scoping input only; never cite them as a claim.

## Target
Strengthen W3-RM's Theorem 3 from polylogarithmic leakage sets to **polynomial** ones: under primitive, design-agnostic
conditions on (X, θ*) — Theorem 1's conditions, eigenvalue floors, (V), and (L) with a deterministic leakage set
Q ⊇ S₀ of size |Q| ≤ n^b for some b < ¼ (or the largest b you can reach) — the coded method reports Ŝ⁺ = S₀ with
probability → 1, for p ≤ n^A, p ≫ n the regime that matters. Fixed-design form (F) first; the Gaussian-rows form (R)
if it costs little. Face the key difficulty head-on: RM-F's lattice condition (N) is automatic only for
|Q ∖ S₀| ≤ (1 − δ₀) log n, and RM-0's sandwich/NA/TL events were proved at polylog |Q|; say which survive at n^b and
what replaces (N). Removing (N)/(D-R) altogether is NOT this ticket (path-level follow-up). No design family in any
statement (families only in an examples table, e.g. UNI-0, LOC-BF, LOC2 polynomial decay). All results asymptotic.
"The method" = `main` as coded — pin code file:line + commit for any code fact (RM's E4 is the model).

## This leg: up to CP1 only
1. PLAN.md, STATEMENT.md (v1.0) with assumption ids and a registry block; LOG.md heartbeat at every step (real local
   time from the system clock; record every agent you start: model, provider, role; running Claude tally).
2. Statement-lock review: one fresh **Sol** (codex `gpt-6.1-sol`, reasoningEffort high), blind first read; disposition;
   a reconciliation Sol if the lock changes substantively.
3. Sharpness gate: `ASSUMPTION_MAP.md`; boundary-violation numerics (simulate just outside each assumption — in
   particular b at and above ¼ — flag `improvable` if the conclusion survives; local machine only, scripts and RESULTS
   in `numerics/`); one fresh **Astra** (codex `gpt-6-astra`, reasoningEffort high) "better theorem" review, blind,
   asked only for a strictly better provable statement (e.g. b up to ½, or (N) weakened).
4. Before each review round, from the worktree root: `python Theory_work/Wave3/tools/manifest.py freeze
   Theory_work/Wave3/W3-RM2 Theory_work/Wave3/W3-RM2/reviews/MANIFEST_<round>.txt --extra
   Theory_work/Wave3/W3-RM2/reviews/INPUTS.txt`; blind brief to `reviews/BRIEF_<round>_<seat>.md`; each reviewer quotes
   the digest; then `manifest.py bind`.
5. **CP1:** write `CHECKPOINT_1.md` — locked statement, each assumption's necessity reading (with numerics), the
   better-theorem proposals each with a disposition (adopt / reject with evidence / defer as a named open item), what
   you plan for CP2 (the key lemma) with an honest time estimate — and **end your run** with that content as your final
   message. Sketches only past CP1 until HQ replies in this thread.

## Operating rules
- Read `C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave3/HOLDS.md` before each step; a HOLD on any claim
  you consume (transitively) stops its use.
- Subagents via `delegate_task` (T3): Sol/Astra on provider `codex`; any Claude helper (Opus/Sonnet/Haiku, or Fable)
  on provider **`claudeAgent` (Claude Work)** at effort high. **Never use Claude Personal.**
- **Stay in your run while reviewers or numerics are working**: wait for them (delegate_task mode wait, blocking
  waits); do not end your turn until CP1 is written. No NOTS use. Keep replies short; details in files.
