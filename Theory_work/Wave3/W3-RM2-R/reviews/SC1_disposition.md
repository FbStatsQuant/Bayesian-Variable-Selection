# SC1 disposition (lead, 2026-11-15) — review `SC1_statement_change_sol.md` (ACCEPT WITH CHANGES)

| # | tag | finding | disposition |
|---|---|---|---|
| 1 | S | St_n = {[S₀, S̃₀] ⊆ 𝓛′} false without truth inclusion | ACCEPTED, reviewer's fix verbatim: St_n(𝓛′) = {S₀ ⊆ S̃₀} ∩ {[S₀, S̃₀] ⊆ 𝓛′} [SC1-1] |
| 2 | F | guard lift open-ended | ACCEPTED: IDEAL-W⁺ = IDEAL-W + exactly two upper-bound predicates (v3_run.R:96 `le > 1e6`; v3_core.cpp:474 `cap_ll > INT_MAX`), everything else kept as coded; reviewer's list of other fixed thresholds (none a no-output exit) recorded in PLAN Q5 for the audit [SC1-2] |
| 3 | F | domain provisional; physical-machine claim unsupported | ACCEPTED: 𝔇 labelled sufficient, stated in ℓ form with its derivation; physical-machine sentence removed [SC1-3] |
| 4 | E | RM0 dependency wording | ACCEPTED verbatim [SC1-4] |
| 5 | E | title, DLV IDEAL-W pointer (:24), changelog tags, v3_fit.R:88-94 | ACCEPTED; changelog rows now carry SC1's per-clause tags |
Classification (SC1 §3) adopted in the changelog: WEAKER rows = narrower input domain, added idealisation IDEAL-W⁺ (delivery clauses), withdrawn DLV-0 implication edge; STRONGER = (a′)/(b⁺) start event; NEW-CLAIM = delivery on 𝔇. All WEAKER rows concern the delivery target T2(a) relative to the v0.1 draft (not a recorded claim) and are reported at CP1. Statement locked as v1.0.
