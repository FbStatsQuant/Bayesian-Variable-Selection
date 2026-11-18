# W3-RM2-R — CHECKPOINT 1 (hard; 2026-11-15, lead Claude Opus 5.5, Claude Third)

**State.** `STATEMENT.md` **v1.0 LOCKED** (delta over W3-RM2 v1.4 and W3-RM:RM-0). Lock chain, NORMAL mode, both
OpenAI (codex gpt-6.1-sol high, fresh agents): SL1 blind lock `reviews/SL1_statement_lock_sol.md` — DO NOT LOCK,
5 findings, all accepted (`reviews/SL1_disposition.md`) → v0.2; SC1 statement-change check
`reviews/SC1_statement_change_sol.md` — ACCEPT WITH CHANGES, 5 findings applied verbatim (`reviews/SC1_disposition.md`)
→ v1.0. OpenAI reviews used: 2 of ~4–5. HOLDS.md (origin/main): no holds. Files: PLAN.md, TARGET.md, READER_DELTA.md
(draft), DEPS.tsv, LOG.md.

## What changes, in plain words (for HQ's H5 card)
1. **RM2-F (fixed design) needs only standard constant-level signals.** Before: visibility δ²_{U,j} ≥ M_n log n with
   M_n → ∞, and beta-min with θ²_min n/log n → ∞. Now: δ²_{U,j} ≥ M_V log n with a fixed M_V > (σ√(2A) + √((2A+1)C_R))²,
   C_R = 3(M + σ²); the beta-min of Theorem 1 at its own constant level BM(c), c > c₀; and the truth-removal floor in
   additive form, √λ_n ≥ 2(d_n + √(2 log n)) and λ_n ≥ c_TL log n, c_TL > 8(A+1) + 4(2A+1)C_R/σ² (was ratio → ∞).
2. **The reported-model conclusion loses "on output"** (RM2-F and RM2-R). Under the delivery premises (exact
   arithmetic, an idealised machine that also lifts two fixed size ceilings in the code, shipped configuration,
   sufficient allocation) every run on every valid input returns output, and P(Ŝ⁺ = S₀) → 1 for every seed, with
   **P(Ŝ⁺ ≠ S₀) ≤ P(S₀ not the unique score maximiser) + P(local search misses S₀)**.
3. **The posterior input is now mode consistency** ({S₀ unique F-maximiser}); [POST] ⇒ [MODE] by Markov.
4. RM-0(a) holds on any down-closed sub-lattice containing [S₀, S̃₀] (T2(c), one line).
5. Example: one truth with n^b weak proxies and **decaying** θ_n: d_n = O(1); first witness that (BM-W) is strictly
   weaker than (BM-Q) (θ_n² = (log n)²/n).

## Target clauses (HQ decides)
| clause | claim | kind | vs recorded |
|---|---|---|---|
| (C0⁺) RM0-plus (a′), (b⁺), (c⁺) | core, mode form, delivery | NEW-CLAIM | STRONGER than W3-RM:RM-0 |
| (C-D) DLV-0 | every valid non-degenerate input returns output, under (D) incl. IDEAL-W⁺; on a bounded sufficient domain 𝔇 without the lift | NEW-CLAIM | no implication edge to C-DLV:Prop-F (different cap/allocation); recovers its delivery half |
| (C1⁺) RM2-F-plus | headline | **STRONGER** than W3-RM2:RM2-F (weaker hypotheses; conclusions ⊇) | headline change → READER_DELTA |
| (C2⁺) RM2-R-plus | headline | **STRONGER** than RM2-R (same hypotheses; conclusion without "on output") | headline change → READER_DELTA |
| SAND-F-c, TL-F-c; Ex-Proxy-d; Cont-plus | bridges, example, containment | NEW-CLAIM | imply SAND-F-b, TL-F-b, Ex-Proxy, Cont-F/R |

**WEAKER rows at the lock (all on the T2(a) delivery target vs the v0.1 draft, no recorded claim weakened):**
input domain narrowed to inputs passing the code's validators; added premise **IDEAL-W⁺** (lifts `le > 1e6`
`v3_run.R:96` and `cap_ll > INT_MAX` `v3_core.cpp:474`; without it delivery only for ℓ_n ≤ 10⁶, ℓ_n + ⌊n/2⌋ ≤ 2³¹−1).
**Engineering note for HQ:** the `ls0_ell ≤ 1e6` ceiling makes the shipped code refuse astronomically large inputs; a
code change could remove the need for IDEAL-W⁺'s first lift (not requested; method unchanged).

## Plan and hours (PLAN.md)
Lemmas Q1–Q7 (copies of parent lemmas with [R-#] marks + DLV-0 code audit + Ex-Proxy-d) ≈ 6 h; boundary numerics
(Sonnet helper, ~1 h; nice, ≤ 16 cores, TMPDIR per SMC_Theory_Department convention); line checks LC-A (Q1, Q2, Q7),
LC-B (Q4, Q5, Q6); REPORT, citecheck, council R1 (Sol + Opus seats). CP3 target Wed 11-18 well before 18:00 CT.
No new key lemma expected (Tier B holds); DLV-0 is the only medium-risk item (code audit).

## For the manager to decide
- **Optional items:** quantile form of (W) → proposed named open item **O-Wq**; Ex-Equi b = 3/8 (O4′) only if time.
- **Ex-PolyR / Ex-PolyF:** not consumed or restated by this delta (they remain examples via Cont-plus) → your call
  whether they go to this ticket's council or HQ's.
- READER_DELTA.md draft (Theorems 6, 7 of W3-READER) for HQ / W3-READER: new (A1), (A3), (A5)(b) signal texts, master
  replaces NEW bridges B6.6/B7.4; open HQ choices listed at its end.
- Go to proceed to lemmas.
