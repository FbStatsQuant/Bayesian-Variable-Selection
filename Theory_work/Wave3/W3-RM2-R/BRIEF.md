# W3-RM2-R — the RM2 rider T4 + T2 (Theory Department, 2026-11-15)

Lead: Claude Opus 5.5, effort high, Claude Third, on Owls. **Tier B**, NORMAL mode. Worktree
`/home/fb31/BVS-wt/W3-RM2-R`, branch `theory/W3-RM2-R`, folder `Theory_work/Wave3/W3-RM2-R/`.
Read first, in full: `RIDER_RULES.md` (this folder; binding), then `Theory_work/Wave3/PROTOCOL_v4.md`,
`Theory_work/Wave3/PROGRAM.md` (presentation rule + Readability).

## Parents (read-only)
- `Theory_work/Wave3/W3-RM2/` v1.4 (recorded on main: 16 checked + Ex-PolyR/Ex-PolyF unchecked; RM2-F/Cont-F/Ex-Proxy/
  Ex-Equi conditional on SOP:TH09; RM2-R/POST-R/Cont-R conditional on W2-APP:POST). `SHARPNESS.md` lists the open items.
- `Theory_work/Wave3/W3-RM/` (RM-0 core; RM-F, RM-R now SUPERSEDED-VALID by RM2-F/RM2-R).
- `Theory_work/Wave1C/C-DLV/` (Theorem D, Lemma S.1, Lemma R; for T2(a)).
- Motivation: `API_AUDIT/sharp1/TRIAGE.md` T2, T4 (§2); `sharp1b/TRIAGE.md` T2(c) and the T4 wording point;
  `sharp2/TRIAGE.md` rows W3-RM2:* and §2 row T4.
- **T6 is already done** (RM2 v1.4, `W3-RM2/STATEMENT.md:4-5,176-184`, `SHARPNESS.md:40-44`). Do not redo it.

## Targets
1. **T4 — constant-level signals in RM2-F.** (V) with a fixed M ≥ M₀(A, σ², C_R) and BM(c), c > c₀, in place of
   M_n → ∞ and BM-∞ (re-read the TL step, GROW L2.1, for the constant; `W3-RM/SHARPNESS.md:28-29`). Plus the sharp2
   additions: the **additive (BM-W) floor** — truth removal needs only √λ_n ≥ 2(d_n + √(2 log n)) and
   λ_n ≥ C(A, M, σ², C_R) log n (`W3-RM2/lemmas/L2_width.md:205-217`); **Ex-Proxy with decaying θ_n** (r²q → 0 ⇒
   d_n = O(1), E4 for nθ_n²/log n → ∞; the first witness that (BM-W) is strictly weaker than (BM-Q),
   `L6_examples.md:360-384`). Optional, same leg: the quantile form of (W) (`L2_width.md:77-86`).
2. **T2 — delivery and mode interface.** (a) DLV-0: under EX-A, IDEAL-W, MACH, CONFIG and the Corollary R allocation,
   every valid non-degenerate input and every seed returns output; no model, no design class (Lemma R holds for every
   valid input, seed and realisation; check against the code as pinned, and note that Lemma R must be re-audited when
   v3.2 freezes — the preflight charge changes). (b) Replace {π(S₀) ≤ ½} in RM-0(b) by {S₀ is not the unique
   F-maximiser on Ω}; [POST] becomes a corollary by Markov; RM-0/RM2 then state P(Ŝ⁺ = S₀) → 1 without "on output",
   with the error split into mode failure + search failure. (c) RM-0(a) for any deterministic down-closed 𝓛′ ⊆ 𝓛 with
   P([S₀, S̃₀] ⊆ 𝓛′) → 1 (one line).
3. Optional, only if CP3 by Wed 18:00 CT stays safe: Ex-Equi threshold b = 3/8 and its converse (O4′). RM2-R aggregated
   leak = named open item, not a target.

Headline effect: RM2-F (C1) premises weaken (T4) and the reported-model conclusion loses "on output" (T2(b)) →
`READER_DELTA.md` required; CHECKPOINT_1 must say in plain words what changes (for HQ's H5 card).

## Also put to the council (no new proof)
RM2's `Ex-PolyR` and `Ex-PolyF` are recorded unchecked and were to be named in RM2's next council round. If they are
consumed or restated in your delta, include them in your manifest and council per-claim tables; if not, list them in
CHECKPOINT_1 and the manager decides. RM2's parked post-council edits stay with HQ (not yours).

## Budget and agents
~8–10 Opus hours. Up to 2 helpers (Claude Third, Opus 5.5 high). Sol reviews per RIDER_RULES §3. Kill budget 3 per
lemma; the constant-level TL step gets 2.

## Start
`cd /home/fb31/BVS-wt/W3-RM2-R`, write `PLAN.md` and the delta `STATEMENT.md`, launch the Sol statement lock, then
`CHECKPOINT_1.md` and end your run.
