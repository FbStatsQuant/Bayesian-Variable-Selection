# T8 delta after reading walk T6 (§A2 core, §A7 delivery, findings F1, F2, F5)

Source: `walks/T6.md` on `origin/theory/PRE-LEAN-walkB` dc2e7174. This file lists only what changes in `T8.md`.

**No ruling changes.** T8-1, T8-2, T8-3, G1 and G2 stand as written. Walk T6 finds no flaw in RM0-plus or in DLV-0 at its pin, and its §A7 (E5) confirms T8-1's reading independently: both lifted predicates are rejection tests and are false on 𝔇.

## Changes to §2, "Left uncovered"

Replace the second bullet ("the walk … refers the core and delivery to walk T6 §A2 and §A7, which I have not yet been sent") by:

- **Core (RM0-plus), now covered:** walk T6 §A2 re-derives the descent (four neighbour cases, exactly |S̃₀ ∖ S₀| deletions, cap never reached) and the pathwise inclusion 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝓜_nᶜ ∪ 𝒦_nᶜ. No flaw.
- **Delivery (DLV-0), covered in logic only:** walk T6 §A7 walks steps (E1)–(E8) and says in terms that it did **not** check the completeness of the exit inventory. That completeness rests on the two C-DLV code audits, which Sol-1 confirmed at pin 4676af6. So the inventory itself has no walk in this pass.

## Change to §4, Lean item 1

Add a fourth clause to the interface (walk T6 F1): **the search path is a function of the data alone**, so that 𝒦_n is a data event and one event serves every seed. The interface then reads: scored models lie in Ω; on output, the search's scored sets are scored and its path depends only on the data; the reported model maximises F over the scored set.

## One addition for the re-pin (G1), flagged, not verified by me

The duplicate-model `stop()` cannot fire because "a model's value is a deterministic function of the model" (the store's own code comment, `cpp/v3_ledger.h:33-34`; walk T6 cites LIST-CODE D2). Under exact arithmetic (EX-A) that is immediate. In binary64 it needs every source of a score (islands, block tables, models inherited from calibration, the two local searches) to produce the same bits for the same model.
- Before the list fields, a violation would have been a silent duplicate in the store; now it would turn a completed fit into an R error after `finish()`.
- I read the store (`v3_ledger.h:44-56`) and `store_to_list` (`cpp/v3_core.cpp:358-362`), which agree with the walker's three checks. I did not trace the table and inherited score paths.
- Suggestion: when DLV-0 and LIST-CODE are re-pinned to `method-v3.1.1-listpip`, have the unreachability reason for that row cite this invariant by name, and ask Engineering to confirm it across the score sources. This is outside the theory's premises; it changes no statement.
