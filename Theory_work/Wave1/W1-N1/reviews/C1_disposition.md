# C1 · council round 1 · disposition (lead, 2026-11-08)

Reviewers (fresh delegate_tasks, independent, told not to read LOG/reviews):
- Codex gpt-6.1-sol, reasoningEffort high — `C1_council_codex.md`: G1–G6 **PASS**, score **9.3/10**, blocking: none.
- Claude Opus 5.5, effort high (claude-personal) — `C1_council_opus.md`: G1–G6 **PASS**, score **8.9/10**, blocking: none.

**Council PASSED in round 1** (both ≥ 8.0, all gates passing in the same round; PROTOCOL.md layer 3).

Non-blocking items, all addressed after the vote (exposition only; no change of claim):

| Seat | # | Disposition |
|---|---|---|
| Codex | 1 | Localisation convention added as a post-lock exposition note before STATEMENT §3. |
| Codex | 2 | Lean deliverable: unchanged objection (HQ ticket: Lean out of scope unless trivial; no toolchain). Flagged in REPORT §5 as an open FR04 item; the ticket is not Lean-certified. |
| Opus | 1 | "Code version" paragraph added to L1 (v2.1 → v2.2.1 diffs: start/score/blocks identical; engine plain-PIP lines; ledger read-only registry hook), verified by `diff --strip-trailing-cr`. |
| Opus | 2 | (B-0) now lists persistent `Engine` members (`tmpQ`, `rb_acc`, `scratch`, `ms`, `ev`) and why none carries information. |
| Opus | 3 | Success set A_s defined in L1; L3 uses A₀ := A_s ∩ {R′ ≥ r} ∩ A_𝒜. |
| Opus | 4 | (R3): H := F_{τ_1}; tower property noted. |
| Opus | 5 | R_remarks: premise discharged **islandwise**; pooled clauses keep their premises. |
| Opus | 6 | Lemma status headers harmonised to the final status string with premise qualifier and inherited N9/T12 statuses. |
| Opus | 7 | BUILD.md: MC stream labelling and seed-budget reading stated; STATEMENT v2.1 loop citation corrected to `:351-360`. |
| Opus | 8 | Card note for HQ carried in REPORT §5. |
