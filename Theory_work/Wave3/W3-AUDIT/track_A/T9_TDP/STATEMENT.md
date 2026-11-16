# T9 · Lemma TDP (the coded tie-aware start-mode fallback) — STATEMENT v2 (draft, not locked)

Track A item T9 (`AUDIT.md` §6; CHECKPOINT_1 annex order 9). Tier B (second-seat re-check of `C-ENG:TDP_E`, "PROVED (by
this seat, unchecked)"). **Lean target: yes** (DP correctness and the greedy lex-min argument are finite statements).
Blocks row 3.1, delivery clause only (`W2-UNI:F-UNI` via `A:DELIVERY-ALLOC` ↳ TDP-IMPL).

## Source of the premise
- **TDP-IMPL**: "the e4 tie-aware fallback is implemented as W1-N3's reference algorithm TDP …, with
  O(p·Σ_b(2^{|C_b|} + (K+1)²)) operations (W1-N3 L7:20), implemented with O(Σ_b 2^{|C_b|} + J(K+1)) storage"; "e4 itself
  only fixes WHICH maximiser is emitted; TDP-IMPL fixes HOW (its cost)" (`Theory_work/Wave1C/C-DLV/STATEMENT.md:38-42`).
- The claim re-checked: "TDP-E returns lex_min E, in binary64, for every input on which `start_mode` runs … Under EX-A
  … E = 𝒜* …, so TDP-E returns S*" (`Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md:38-40`), with proof
  (`Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md:42-60`) and cost (`Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md:62-64`).
- S* (the prescribed start mode: among maximisers of γ₀ on Ω, the smallest size, then lexicographically smallest) and
  𝒜* (the maximisers of smallest size): `Theory_work/Wave1/W1-N3/STATEMENT.md:78-82`.

## Code of record
`Scripts/SMC_BVS/core/cpp/v3_start.h:178-305` (`mode_dp`, `mode_tight`, `mode_tie_dp`, `start_mode`) at pin 4676af6.

## Setting
`st` as in T4 (ENC) (so N3 (H1) strengthened holds), cap ≥ 2, `tie_dp = true` (the shipped call is
`start_mode(st, 1000000, true)`, T3 OPC). Notation of TDP_E: t_b = min(|C_b|, K); `mb`, `arg`, `M`, k̂ = `kbest`; tight
edges; E := the sets built from a tight path (J, k̂) → (0, 0) and codes in `arg` (`Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md:15-20`).

## Lemma TDP
- **(TDP-a) Enumeration.** The recursion `rec` visits elements of E only, each at most once; without truncation it
  visits all of E and `res.S` = lex_min E.
- **(TDP-b) Fallback.** `mode_tie_dp` returns lex_min E (under (H2-FP) as in TDP_E, and under EX-A). Hence
  `start_mode(st, cap, true).S` = lex_min E for every cap ≥ 2, truncated or not.
- **(TDP-e) Nonempty, root check passes.** k̂ ≥ 0, E ≠ ∅, and `feasible()` with IN = OUT = ∅ returns true, so the
  `runtime_error` at `cpp/v3_start.h:261` never fires (under (H2-FP) as in TDP_E, and under EX-A).
- **(TDP-c) Under EX-A** E = 𝒜* (proved directly in PROOF, for the code at the pin), so the returned set is S*.
- **(TDP-d) Cost.** The fallback performs O(p·(Σ_b (K + 1)(t_b + 1) + max_b 2^{|C_b|})) ⊆ O(p·Σ_b(2^{|C_b|} + (K + 1)²))
  elementary operations after `mode_dp` (which costs O(Σ_b 2^{|C_b|} + Σ_b (K + 1)(t_b + 1))), and uses
  O(Σ_b 2^{|C_b|} + J(K + 1)) storage: TDP-IMPL's bounds. The enumeration fast path that precedes it costs
  O(min(|E|, cap)·(J(B + 2) + p log p)).
- **How TDP-IMPL is discharged.** The coded routine is TDP-E (tight-edge reachability on the computed DP), not literally
  L7's reference TDP; TDP-IMPL is met as "returns S* under EX-A (TDP-c) within TDP-IMPL's operation and storage bounds
  (TDP-d)", which is what its users need ("e4 itself only fixes WHICH maximiser …; TDP-IMPL fixes HOW (its cost)").

## Not claimed
- That lex_min E is the lex-minimum of all rounded maximisers in binary64 (TDP_E's own disclaimer, `Theory_work/Wave1C/C-ENG/lemmas/TDP_E.md:34-36`).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (re-states `C-ENG:TDP_E` + TDP-IMPL's cost for the pin) | track A T9 | `AUDIT.md` §6 T9 | `CHECK.md` |
| v1.1 | (TDP-e) | STRONGER (states what (TDP-b)'s proof already shows; used by T10) | LC2 #14 | `reviews/LC2_reply_opus.md` | pending (gate) |
| v2 | (TDP-c) direct proof; enumeration cost; how TDP-IMPL is met | STRONGER (enumeration cost added) / EQUAL | LC3 T9 #2, #3 | `reviews/LC3_reply_opus.md` | pending (gate) |
