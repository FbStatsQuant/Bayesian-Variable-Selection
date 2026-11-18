# LC1 disposition (lead, 2026-11-16) — reply `LC1_reply_opus.md`

All findings accepted; none rejected. No finding is a failing step (the checker: "The findings below are about the
definitions and the interface with downstream statements, not about a failing step").

## T1 GW (v1 → v2)
| # | tag | action |
|---|---|---|
| 1 | C/S | `fit$peak_memory_kb` and environment readings put in 𝒱_op; premise now "clock and machine-environment readings"; PROOF opening paragraph shows where they go (`v3_fit.R:2-7, 56-57, 80`). |
| 2 | S | "Statistical state" redefined as the complement of 𝒱_op (assigned from clock/environment/check bodies, transitively); Step 1 rewritten in that form. |
| 3 | S | P° now executes every check body and discards its Boolean; termination of the bodies proved (Step 1, last paragraph). |
| 4 | F | New clause (GW-iv) (𝒜 = 𝒜° ∩ {no calibration check fires} ⊆ 𝒜°, 𝒪 ⊆ 𝒪°, 𝒪 ∩ A ⊆ 𝒪° ∩ A°, identifications) + Step 4. Changelog: STRONGER (new clause). |
| 5 | S/F | Added to Not claimed: no probability model for the clock; pathwise statement; outer-probability reading otherwise. |
| 6 | E | Missing clock readings added to Step 1 (`cpp_build_grid`, guard clock, report, `engine.h:336`). |
| 7 | E | Grep sentence now lists every Boolean call site; "read only to compute timing fields". |
| 8 | E | Read/write lists of the check bodies completed. |
| 9 | F | New clause (GW-v) complete scans + Step 5. Changelog: STRONGER. |

## T2 BLK (v1 → v2)
| # | tag | action |
|---|---|---|
| 1 | F | Partition map C(X) defined on the whole setting; code computes it on the sampler branch only; enumeration branch noted. |
| 2 | F | Setting R line (columns non-constant a.s., Borel extension on the null set, independence from ε) + PROOF section. |
| 3 | S/E | Binary64 claim now proved (PROOF last section). |
| 4 | E | Source cited at `C-GROW/STATEMENT.md:65-67`; the registry's stale `:61` noted for the recorder. |
| 5 | E | Downstream uses at `cpp/v3_core.cpp:469, 611, 714` added. |
| 6 | E | Code-comment mismatch (`:144` says 20, enforced 16) recorded as a code note for Engineering; not a lemma defect. |

Re-check of the repair: LC1r, a new Opus agent (the finder's family), on the diff and the new clauses (PROTOCOL_v4 §2A
"re-check of a repaired lemma").
