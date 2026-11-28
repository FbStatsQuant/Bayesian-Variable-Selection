# SL1 disposition (lead, 2026-11-15) — review `SL1_statement_lock_sol.md` (DO NOT LOCK, 5 findings)

| # | tag | finding | disposition | where (STATEMENT v0.2) |
|---|---|---|---|---|
| 1 | S | input definition omits length(y) = n; scalar seed/allocation | ACCEPTED. "Valid non-degenerate input" now requires y of length n (no dim), scalar seed in [1, 2³¹−1], allocation list with scalar finite positive fields; "no input validator fires" with code pointers | §2 "Valid non-degenerate input [SL1-1]" |
| 2 | F | IDEAL-W does not lift the literal guards `ls0_ell ≤ 1e6` (v3_run.R:95-97) and the INT_MAX cap guard (v3_core.cpp:473-474) | ACCEPTED. New premise IDEAL-W⁺ = IDEAL-W read as also lifting representability guards (explicit comparisons of size-derived quantities with fixed machine limits; the two named, the audit lists all). Without the lift DLV-0 holds on a stated bounded supported domain 𝔇; the asymptotic conclusions are stated under IDEAL-W⁺ (an idealisation of the same kind as EX-A). This is a WEAKER/qualified form of the delivery target relative to v0.1 (an added premise), reported at CP1 | §2 "IDEAL-W⁺ [SL1-2]"; (C-D) last clause; PLAN Q5 (v) |
| 3 | F | T2(c) stated with "every maximiser in 𝓛′" instead of the coded start | ACCEPTED. New event St_n(𝓛′) := {S̃₀ ∈ 𝓛′} = {[S₀, S̃₀] ⊆ 𝓛′}; Sand_n(𝓛′) kept as sufficient; used in (a′) and the bound of (b⁺) | §2 sub-lattice events; (C0⁺)(a′), (b⁺) |
| 4 | F | DLV-0 ⇒ Prop F edge not an implication (different cap/allocation) | ACCEPTED. Row now says: no registry implication edge; DLV-0 recovers Prop F's (and F-UNI Step 2's) delivery conclusion under (D) | §6 dependency table |
| 5 | E | DLV pointers 21-39 → 21-42, 40-41 → 43-44 | ACCEPTED | §2 |

Per-point answers 1–4, 6, 7 (statistical changes, RM0-plus extensions, Ex-Proxy-d, statistical dependency rows): pass; no change.
The v0.1 → v0.1.1 record edit (manager input, R-AUD1: C-DLV law-free inputs listed, Prop F consistency sentence excluded) landed while SL1 ran; it changes no claim and is included in the statement-change check below.
Next: statement-change check SC1 (Sol, new agent) on the diff v0.1 → v0.2 and its dependents (PROTOCOL_v4 §4.2 / §2A), because the verdict was DO NOT LOCK and finding 2 adds a premise.
