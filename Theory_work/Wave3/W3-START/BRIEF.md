# W3-START — start-mass rate (PROGRAM item 2) — lead brief (HQ, 2026-11-11)

You are the **lead** of ticket W3-START (Claude Fable 5.2, effort high, Claude Personal). Your worktree is
`C:/Users/felip/BVS-wt/W3-START` (branch `theory/W3-START`). Work only inside it; ticket folder
`Theory_work/Wave3/W3-START/`. **Change no git state** (HQ commits). Never use effort above high.

## Read first
- `Theory_work/Wave3/PROGRAM.md` (item 2; presentation rule) and `Theory_work/Wave3/PROTOCOL.md` (all of it, **resume
  rules 9–16 bind you**: hard checkpoints, frozen manifests, blind first reads, consumed claims, heartbeat LOG).
- `Theory_work/INFRA/LIFECYCLE.md` §4.1 (council record format) and `Theory_work/INFRA/templates/ASSUMPTION_MAP.md`
  (registry block). Consume prior results only by registry id + version from `Theory_work/INFRA/registry/claims.tsv`.
- Consumers of your result: `Theory_work/Wave3/W3-SAMP/STATEMENT.md` l.76 (P-START: π₀(S₀) → 1 on 𝒜, no rate) and
  l.82 (P-OVL), W3-SAMP Theorems C/TR; W3-RM. Prior start-mass work: SOP:TH03 (M3 Theorem START), W1-PXN:Thm-PXN(S)
  (masked regime, start mass collapses), `Theory_work/Wave1C/C-MIS/` (misspecification/sandwich), W3-SAMP REPORT §6.

## Target
Prove a **start-mass rate** for the method as coded: under primitive, design-agnostic conditions on (X, θ*) with **no
leakage**, π₀(S₀) ≥ 1 − n^{−c} w.p. → 1 (or the sharpest rate you can get), for p ≤ n^A, p ≫ n the regime that matters;
plus the primitive conditions that deliver W3-SAMP's P-START (and, if cheap, P-OVL). Include the misspecified/sandwich
form (C-MIS) where it costs little. State honestly where it fails: W3-P6 shows that on strong-factor designs at p > K the
start mode excludes S₀ (W1-PXN(S) is the masked-regime law), so the theorem is for no-leakage designs and is not expected
to cover decision D1. No design family in any statement; families only in an examples table. All results asymptotic.
"π₀" means the start distribution exactly as `main` computes it — pin the code (file:line, commit) you rely on.

## This leg: up to CP1 only
1. PLAN.md, STATEMENT.md (v1.0) with assumption ids; LOG.md heartbeat (timestamp each step; record every agent you start:
   model, provider, role; keep a running Claude tally).
2. Statement-lock review: one fresh **Sol** (codex `gpt-6.1-sol`, reasoningEffort high), blind first read.
3. Sharpness gate: `ASSUMPTION_MAP.md`; boundary-violation numerics (simulate just outside each assumption; flag
   `improvable` if the conclusion survives; scripts and RESULTS in `numerics/`); one fresh **Astra** (codex
   `gpt-6-astra`, reasoningEffort high) "better theorem" review, blind, asked only for a strictly better provable statement.
4. Before each review round: `python Theory_work/Wave3/tools/manifest.py freeze Theory_work/Wave3/W3-START
   Theory_work/Wave3/W3-START/reviews/MANIFEST_<round>.txt --extra <list of external inputs>`; save each reviewer's blind
   brief to `reviews/BRIEF_<round>_<seat>.md`; each reviewer quotes the digest; review files go to `reviews/`.
5. **CP1:** write `CHECKPOINT_1.md` — locked statement, each assumption's necessity reading (with numerics), the
   better-theorem proposals each with a disposition (adopt / reject with evidence / defer as a named open item), what you
   plan for CP2 with an honest time estimate — and **end your run** with that content as your final message. Do no proof
   work beyond sketches past CP1 until HQ replies in this thread.

Subagents: use `delegate_task` (T3). Providers: Sol/Astra on `codex`; any Opus/Sonnet/Haiku helper on `claudeAgent`
(Claude Work) at effort high; Fable only for yourself. No NOTS use. Keep replies short; details in files.
