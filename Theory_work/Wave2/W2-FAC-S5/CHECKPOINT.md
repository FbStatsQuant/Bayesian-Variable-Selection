# W2-FAC-S5 — CHECKPOINT (2026-11-09 ~10:30 CST; key lemma of Tier 1 checked)

**Proved and cross-family checked (Tier 1, reduction theorem FAC-BCS-R):**
* L1 exact two-level reduction of the BCS score (per-group CS statistics + one scalar global error e_R; |τ| ≤ |A| + κ₀|e|;
  ridge/leakage/multiplier/determinant bounds) — R02: FAILED as written (leakage rate), repaired; re-confirmed by R03.
* L2 start mode = S* for every p ≤ n/2 under generic no-cancellation (FS-BCS) — R02 V-W-A, applied. S4: 36/36.
* L3 event E_n — R02 V-W-A, applied.
* **L4 key lemma (C2-R)**: for log p/log n < α < 1/2, on E_n ∩ CC_n(δ) the LS0 path from S* is the best-null-deletion
  path to S₀ (δ/8 log n margins; truth moves lose c n) — R03 (Sol xhigh) V-W-A, no fatal/major, applied.
* L5 assembly: D_n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}), P(Ŝ⁺ ≠ S₀) ≤ P̃(CC_n(δ)ᶜ) + o(1) — R04 V-W-A, applied.

**Tier 2 (Lemma KL: P̃(CC_n(δ)) → 1) — open.** Prover round 1 (Codex Sol xhigh): PARTIAL — CC proved in the final
≤ 2-null region of full S5, for whole paths under a restricted partition (null groups singletons), protected-champion
lemma; middle range (genuine 5-null groups, retained sizes between polylog and p^{1−β}) open. Round 2 (Codex Sol max)
running. W2-SIM request (e_T scaling with p up to 2·10⁵) sent.

**Honest estimate.** Tier 1 will close (mid-point → sweep → council). Tier 2 is a genuine research problem (the q-dim
analogue of FAC-CS's static centre argument with path-dependent group states); I estimate < 40% that a checkable proof
of any exponent beyond 1/6 emerges in this ticket. If not, RESULT = PARTIAL with KL as the exact obstruction.

**Narrowing foreseen:** none beyond the locked two-tier statement.
