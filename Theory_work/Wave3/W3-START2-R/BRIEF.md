# W3-START2-R — START2 v1.5 rider + START restatements (Theory Department, 2026-11-15)

Lead: Claude Opus 5.5, effort high, Claude Third, on Owls. **Tier B**, NORMAL mode. Worktree
`/home/fb31/BVS-wt/W3-START2-R`, branch `theory/W3-START2-R`, folder `Theory_work/Wave3/W3-START2-R/`.
Read first, in full: `RIDER_RULES.md` (this folder; binding), then `Theory_work/Wave3/PROTOCOL_v4.md`,
`Theory_work/Wave3/PROGRAM.md` (presentation rule + Readability).

## Parents (read-only)
- `Theory_work/Wave3/W3-START2/` v1.4.1 (delta over START v1.3.4; recorded on main, 9 claims).
- `Theory_work/Wave3/W3-START/` v1.3.4 (recorded, 21 claims).
- Motivation, with the lemma lines already checked by the triage reviewer: `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md`
  rows W3-START:* and W3-START2:*, and §2 rows T8, T10 (T9, T11 optional); raw verdicts `sharp2/results/f0*.md`.

Your STATEMENT.md is a delta over START2 v1.4.1 ("version 1.5 of the start-mass statement").

## Targets (in priority order)
1. **T10 — Gaussian-row rate.** Q = S₀ leading term without N_ref (only the 2^{s₀} reference sets U ⊊ S₀,
   `W3-START/lemmas/L9_BR.md:94-96`), so at C_L = 0 under Gaussian rows o₀ = O_P(√(log n/n)) in place of
   (log n)^{15κ_Q+1/2}/√n; carry it into (T3⁺)(b) START-R and IF-START⁺ (r_n → √(log n/n) from n^{−1/2}e^{C_R√log n});
   |H_l| ≤ exp(κ√log n) for the main display (C_R + 15κ, `W3-START2/lemmas/P4_BR.md:25-45`); EX (ii) G-1/G-2 rows at
   the same rate; TRANSFER in self-normalised conditional form (`P1_LEADING.md:147-151`) with the O_P-envelope corollary.
2. **T8 — visibility.** (V-c)/(V-m) at log n + 2 log p pointwise (p ≤ n^A enters only as log(2p) ≤ A log n,
   `W3-START/lemmas/L4_VIS.md:48-50`), so sufficiency and the necessity clause (N3) match for every p_n; keep the
   (a−d)₊ negative price term of Step 5 in (V-m) (EX (i)); NEC (N2⁺)/(N3) and F4 with pointwise log p and drifting c_n.
   Applies to START2 via the base (V-c)/(V-m) → (T1⁺) START-F.
3. **START restatements under START2's hypotheses** (consultant card, cheap): MIS, EX, F1, F3, F4 of START v1.3.4
   restated under the v1.4 hypotheses ((D1), (L-R⁺), no F2 growth condition) and with T8/T10 where they apply; the
   Gaussian-row MIS instance (jointly Gaussian candidate and omitted rows ⇒ (GR) exact; triage row W3-START:MIS, A2 part).
   General deterministic μ ∉ span X_𝒞 = named open item, not a target.
4. **Wording, in your delta:** state LEAK-0 correctly — it sharpens the partition-free 𝔏⁰ only; 𝔏^♯ and 𝔏^{b,0} are
   incomparable (triage §0; parent `STATEMENT.md:87-88` is fixed separately by the editorial ticket). In REPORT, do
   not present the P1 gain as a p ≫ n improvement (rate gain only for p = O(√log n), triage §0).
5. Optional, only if CP3 by Wed 18:00 CT stays safe: T9 (F1 exact Laplace exponent with ā; F3 with G_n = o(log n), no
   growth premise; F4 at n^ι columns), then T11 (factorised OVL⁺; (N2⁺⁺) many leakers). Decide at CP1 with the manager.

Headline effect: (T1⁺) START-F (weaker visibility premise), (T3⁺)(b) START-R and IF-START⁺ (sharper rate) are headline
statements → `READER_DELTA.md` is required, and CHECKPOINT_1 must say in plain words what changes (HQ sends an H5
card to the consultant on that basis).

## Budget and agents
~10–14 Opus hours. Up to 2 helpers (Claude Third, Opus 5.5 high), e.g. one on T8 while you do T10 — the two touch
different lemma files (L4/L7 vs L9/P4). Sol reviews per RIDER_RULES §3 (expect: lock 1, line checks 2–3, council seat 1).
Kill budget: 3 attempts per lemma; the T10 N_ref removal gets 2 (if it fails twice, CP early: it is the target clause).

## Start
`cd /home/fb31/BVS-wt/W3-START2-R`, write `PLAN.md` and the delta `STATEMENT.md`, launch the Sol statement lock, then
`CHECKPOINT_1.md` and end your run.
