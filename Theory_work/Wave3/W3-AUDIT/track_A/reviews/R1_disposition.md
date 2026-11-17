# Council R1 disposition (lead) — batch T1–T10, MANIFEST 01c268b0… — PART 1 (Sol seat; Opus seat pending)

Sol seat (`R1_council_sol.md`): score 7.7, gates FAIL. ACCEPT: T1, T3, T4, T5, T6, T7, T10. REJECT: T2, T8, T9.
All findings accepted. No repair is applied while the Opus seat reviews the frozen manifest (an edit would break its
`verify`). Repairs go into one diff round (PROTOCOL_v4 §5.5) together with the Opus seat's findings.

| # | tag | item | planned repair |
|---|---|---|---|
| 1 | S | T2 | Define C(X) as the abstract cut-and-pack map (the algorithm of `make_blocks` on IDEAL-W's unbounded-word machine) and prove (BLK-a)–(BLK-c) for it on the whole domain; add (BLK-d): the native binary computes C(X) on executions with representable integer sizes/indices and successful allocation (IDEAL-W/MACH; e.g. `2 * p - 1` needs p < 2³⁰). The binary64 remark refers to the same execution domain. |
| 2 | C | T8 | Replace the consequence proof: on completed runs, pathwise, completed ∩ {Ŝ ≠ S₀} ⊆ {S† ≠ S₀} ∪ (𝒜° ∩ {S₀ ∉ 𝓜°_r}) (T1 GW-iii, W3-SAMP:PC, CC2; completed ⊆ 𝒜 ⊆ 𝒜°); then D-i for the potential island given (data, 𝓒°) and integration give E[1_𝒜°(1 − π₀(S₀))^{D_r}] directly; the exponential and (OVL-b) steps follow. No clock-independence premise. STATEMENT's "Consequence" paragraph and OVL-d's reference updated. |
| 3 | S | T9 | Add (H4) to the native-code setting (integer counters and cap representable, cap a positive `long`, allocations of ModeDP/choice/reach succeed, recursion depth J completes); state the algorithmic result (TDP-a–e, cost) separately from the native-return claim; note that T10's X9 excludes the two explicit start-mode throws when reached, not X5 or process/stack failures. |
| 4 | E | T8, (T4) | Add a status extract file (registry rows of W3-START2-R:IF-START, W3-RM:E4 and the other quoted statuses, with registry sha) to the package so a blind seat can verify quoted statuses. |
