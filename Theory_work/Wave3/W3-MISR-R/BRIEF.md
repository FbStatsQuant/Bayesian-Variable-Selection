# W3-MISR-R — T13: MISR Cor-G(a) / Cor-H restatements (Theory Department, 2026-11-15)

Lead: Claude Opus 5.5, effort high, Claude Third, on Owls. **Tier B**, NORMAL mode. Worktree
`/home/fb31/BVS-wt/W3-MISR-R`, branch `theory/W3-MISR-R`, folder `Theory_work/Wave3/W3-MISR-R/`.
Read first, in full: `RIDER_RULES.md` (this folder; binding), then `Theory_work/Wave3/PROTOCOL_v4.md`,
`Theory_work/Wave3/PROGRAM.md` (presentation rule + Readability).

## Parent (read-only)
`Theory_work/Wave3/W3-MISR/` v1.3 (recorded on main, 7 claims, six conditional on unchecked inputs).
Motivation: `API_AUDIT/sharp2/TRIAGE.md` rows W3-MISR:Cor-G(a), Cor-G(b), Cor-H and §2 row T13, §3 (DIST hand-offs).

## Targets
1. **Cor-G(a), minimal hypothesis.** The proof uses only "ξ := X_𝓜β_𝓜 − a1 − X_𝒞γ ~ N(0, τ²I) independent of X_𝒞"
   (`W3-MISR/lemmas/G_corollaries.md:26-31`). Restate: X_𝒞 arbitrary; given X_𝒞, X_𝓜β_𝓜 ~ N(a1 + X_𝒞γ, τ²I);
   Σ_𝒞𝒞 ≻ 0 not needed; the Cramér partial converse as a remark.
2. **Cor-H.** (a) under (SZ), (E^σ), (F₀) and δ_n →_P 0 (the margin is used only for δ_n →_P 0, then POST2 D(a)
   whose premise is δ_n → 0; `W3-POST2/STATEMENT.md:107-111`); the uniform-over-class form and the conditional
   random-design form by the freezing argument of `M_misr.md:143-149`; a KL remark. Expectation-rate (b) and BvM: not targets.
3. Cor-G(b) cosmetics (liminf ρ^{BM} > 2c₀/φ₀²; correlation-matrix floor; explicit bound) only if trivial.
Not yours: the MISR `ASSUMPTION_MAP.md:27` cross-cite to PSHARP (editorial ticket).

**Bears on W3-DIST** (HQ's ticket): with the minimal Cor-G(a), a candidate run is itself an (RD) instance (triage §3
item 1). Write that observation in REPORT as a HEURISTIC/OPEN pointer only; do not touch W3-DIST. The manager hands it
to HQ when your CP3 lands.

## Budget and agents
~3 Opus hours. No helper needed. Sol: lock, one line-check batch, council seat. Kill budget 3.

## Start
`cd /home/fb31/BVS-wt/W3-MISR-R`, write `PLAN.md` and the delta `STATEMENT.md`, launch the Sol statement lock, then
`CHECKPOINT_1.md` and end your run.
