# Correction pass (helpers): statement coverage, proof-use edges, kinds

An independent review sampled 27 registry rows and found these systematic defects; you fix them for YOUR tickets.
Work only in `C:\Users\felip\BVS-infra` (read-only except your output file). No git commands, no subagents. You
transcribe and locate; you do not judge mathematics. Use grep and targeted `sed -n 'a,bp'`; do not read files end to end.

Registry: `Theory_work/INFRA/registry/claims.tsv` (tab-separated; columns id, ticket, local_id, kind, name, short,
file, lines, …, status, …, depends_on, …). Print your rows with:
`python Theory_work/INFRA/tools/registry.py show <id>` (or grep the TSV).

## What to check for EVERY claim of your tickets
1. **Statement span** (`file`, `lines`): exactly the statement — label line through its last line, no proof text,
   no editorial/status lines, not cut mid-sentence, not missing sub-items (e.g. X1.1–X1.3 → all of them, or split).
2. **Premises** (new field): if the statement relies on a setting, hypotheses, or event/threshold definitions written
   ELSEWHERE (a "Setting"/"Assumptions" block, the ticket STATEMENT.md common premises, an event defined a few lines
   above, "(6.1)"), list those spans as `path:a-b` (repo-relative, `;`-separated). These spans are hashed with the
   statement, so a silent change to a hypothesis is detected. Keep them tight (the definitions only).
3. **depends_on**: the claims the PROOF actually uses, as use-level edges `id@use`:
   - `id` or `id@stmt` when the proof uses the other claim's statement;
   - `id@proof:<fact>` when it uses something internal to another claim's proof (an event, rate, constant, step,
     e.g. `W1-GEN:L4@proof:L4.1(iii)`, `W2-FAC-B:L3@proof:chi-square argument`).
   Remove spurious edges (a file that says it does NOT use X; a remark; an "independent fallback"; a citation that
   is only a comparison). Add missing inputs that the proof cites ("by L0.2(c)", "as in FAC-B L4.2"). Ids: registry
   ids (`TICKET:local_id`), or `EXT:<name>` for State-of-Project results (T03♯, M5(0), T12, T22 …).
4. **kind**: theorem / lemma / proposition / corollary as the SOURCE labels it ("Theorem S" → theorem; "Corollary
   L3.4" → corollary); `frontier` for an unproved boundary/numerical observation (NOT `obstruction`, which is a
   proved negative result); `counterexample` for a proved counterexample.
5. Do NOT change statuses (handled separately) and do not invent claims; if a file holds several distinct claims
   under one row and the proof of another claim uses one of them separately, note it (`split-needed`) instead.

## Worked examples (from the review; already decided — copy the pattern)
- C-GROW:L2.1 → premises `Theory_work/Wave1C/C-GROW/lemmas/L2_NA_TL.md:5-17`; add `C-GROW:L0.1@proof:L0.2(c)`.
- W1-N3:LFP → remove the L5 edge (the file says it does not use L2–L5).
- W2-FAC-X:X1 → span must include the distributional setup to :24 (or split X1.1–X1.3).
- C-GROW:C6 → kind `frontier`.
- W2-FAC-XA:L8-S → kind `theorem` ("Theorem S").

## Output
`C:\Users\felip\BVS-infra\Theory_work\INFRA\registry\fragments\corrections\<BATCH>.tsv`, tab-separated, header
`id	field	new_value	evidence`, one row per field change; field ∈ {lines, premises, depends_on, kind, notes};
for depends_on give the COMPLETE new list (`;`-separated `id@use` items); evidence = `path:line` that justifies it
(≤ 120 chars). Rows only for claims that need a change. Before finishing, print every new `lines`/`premises` span
to confirm it. Final message ≤ 10 lines: rows written, claims changed, `split-needed` cases.
