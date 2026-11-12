# SW1 disposition (lead, 2026-11-11) — exhaustive sweep `reviews/SW1_sweep_astra.md`

Reviewer: Codex gpt-6-astra, reasoningEffort high, blind first read (brief `BRIEF_SW1_astra.md`). Manifest
`4dabd787fb4cf1625c352b79c52f153801c8b39ab85af56681df24afa5970868` quoted; `manifest.py bind` OK.
**Counts: 0 CRITICAL / 1 MAJOR / 7 MINOR.** Per-claim table of the reviewer: (C1), (C2), (B1), (B-TK), (B-L), (B-V1),
(B-V2), (B-R), (T0), (T1), F1–F4, (T3)(b), (T4), IF-START "proved as stated"; (C0), (T3)(a), OVL, (T6), (T7) "proved
after the listed repairs". All eight findings are fixed; the result is STATEMENT v1.3.3.

| # | class | finding | action |
|---|---|---|---|
| 1 | MAJOR | Proposition OVL said "fixed a_l" while Q may change with n; the proof needs a uniform bound on the levels | applied (reviewer's exact repair): the statement now assumes deterministic levels a_{n,l} with 0 ≤ a_{n,l} ≤ ā < ∞, uniformly in n and l ∈ Q_n ∖ S₀; E_n uses them; `lemmas/L10_INTERFACES.md` uses ā throughout. No new argument |
| 2 | MINOR | the transfer needs a convention where the start is undefined, off the admissible design sets | applied: convention paragraph in (T3)(a) (also covering (T3)(b) and the random-candidate clause of (T6)) and in `lemmas/L8_TRANSFER.md` L8.0, L8.2 |
| 3 | MINOR | stale wording: "nothing here is proved yet"; OVL "provisional"; examples "proof obligation" | applied: the header says proofs are supplied in L1–L11, author-proved and awaiting acceptance; OVL is a claim (proviso and both "provisionally" removed); the five examples are "verified in `lemmas/L11_EXAMPLES.md` (author-verified, awaiting independent acceptance)". Nothing is upgraded to PROVED-CHECKED |
| 4 | MINOR | W_K undefined; γ₀ changes normalisation between two lines of §1 | applied: W_K := Σ_{k≤K} C(p, k)w(k); a sentence says that from that line on γ₀ is W_K times the coded γ₀ |
| 5 | MINOR | the `leakall` η = 0 satellite simulation was filed under "inside the assumptions" although partition-free (AL) at Q = S₀ fails there | applied: `numerics/RESULTS.md` §2 retitled, the row and reading (i) relabelled as block-relative behaviour outside partition-free (AL); the driver's comment corrected |
| 6 | MINOR | the production report named sharper (AGG-b) checks than `summarise.R` performs | applied: the report now states the relaxed upper form (exp ΣΞ_b, clipped at 700) and the averaged lower form that were actually checked, and points to `lemmas/falsify_L1.R` for the exact checks |
| 7 | MINOR | toolkit maxima in `RESULTS_LEMMAS.md` disagreed with the frozen output | applied: 0.61, 0.20, 0.089, 0.040, identified as the envelope over all sampled sets used |
| 8 | MINOR | the assumption map overstated the necessity of the averaged functional | applied: `ASSUMPTION_MAP.md` §5 — T₁ → 0 is necessary; (AL) is sufficient for this route and the necessity of its functional is not established; "nothing leaks" means zero gains; the scripts do not verify partition-free (AL). The reading (iv) of `numerics/RESULTS.md` corrected the same way |

Statement changes in v1.3.3 (all from this sweep): the OVL hypothesis (1), the off-domain convention (2), the status
wording (3) and the definition of W_K (4). They are read afresh by both council seats (round R1, new manifest).
