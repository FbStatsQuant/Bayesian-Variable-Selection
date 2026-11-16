# W3-READER — reader versions of the headline theorems (HQ, 2026-11-15)

Lead: Claude Opus 5.5, effort high, Claude Third, on Owls. Tier B (PROTOCOL_v4; no new key lemma expected; if one
appears, stop and report). Worktree `/home/fb31/BVS-wt/W3-READER`, branch `theory/W3-READER` (HQ snapshots
`Theory_work/Wave3/W3-READER/` every 15 min). Write only in that folder. Change no git state.

## Why (owner, 2026-11-15)
The owner's standard: what the method does and what each theorem states must be **clear and intelligible to peers**.
"I don't want a bunch of alien-looking theorems; the proof might be as tough as needed." Read `Theory_work/Wave3/PROGRAM.md`
"Presentation rule" + "Readability", and `PROTOCOL_v4.md` H6.

For the level of clarity meant, the owner points to Song & Liang (2015) Thm 1–2 (`Papers/Core_bibliography/32_*`) and to
his own paper (`Papers/Own_work/`, local only, never commit or quote outside this repo). Borrowing from them is neither
required nor forbidden. You propose the presentation; HQ, the HQ consultant and later the owner weigh in.

## Deliverables (to CP1 of this ticket)
1. `CLAIMS_CARD.md`: the proposed **headline list**, 6–10 results, drawn from the registry
   (`Theory_work/INFRA/registry/claims.tsv`: headline flags, PROVED-CHECKED status) and the 11-13 status briefing
   (`Theory_work/Wave3/BRIEFING/theory_status_2026-11-13.tex`).
   - Candidates: posterior concentration T03♯ / SL1; W2-APP POST (random Gaussian designs); W3-RM2 RM2-R / RM2-F
     (reported model of the coded method); W3-START2; W3-MISR; W3-PSHARP; W3-DIST DIST-1 (in progress; a placeholder
     row).
   - Per row: plain statement in words, status (verbatim), what it buys vs the literature, and whether a clean reader
     version exists.
2. `READER_VERSIONS.md`, one section per headline result:
   - **Reader statement:** numbered assumptions (A1)–(Ak) in standard primitive terms (laws of the rows, tails,
     sparsity, p ≤ n^A, eigenvalue bounds, beta-min), and a conclusion in 1–3 displays with explicit rates.
   - **One line per assumption:** why it is there, and whether it is necessary (from the ticket's ASSUMPTION_MAP /
     SHARPNESS files).
   - **Master theorem:** the registered statement it follows from (id@version, file:line).
   - **Bridges needed:** (A1)–(Ak) ⇒ the master's technical hypotheses (visibility, leakage, lattice width, (F_w), SE_λ,
     LSF, …). For each: EXISTS-CHECKED (cite id and status), EXISTS-UNCHECKED, or NEW (state it precisely; estimate the
     effort).
   - **Honest limits:** where no primitive reader version exists, say so. Example: RM2-F's path conditions on fixed
     designs. Propose how to present the master theorem understandably instead: an intuitive paragraph per condition, and
     where the condition holds, via the examples table.
3. `NOTATION.md`: a complete setup and notation section for the chapter, the paper and the advisor report:
   - the model;
   - the prior as coded;
   - the posterior;
   - what the method outputs;
   - every symbol, index set, norm, asymptotic notation (O_P, ≍, ≪) and constant used in the reader statements;
   - a notation table;
   - no internal ids (ticket names, claim ids, interface tags, code names) in the reader-facing text.
4. `METHOD_INTUITION.md`: an intuitive explanation of the whole method, stage by stage (what problem each stage solves),
   with a pipeline figure sketch and a small toy example. Code facts pinned file:line on `main` (`Scripts/SMC_BVS/core/`).
5. `CHECKPOINT_1.md`: the card, the bridge list ranked by importance and cost, and a plan for proving the NEW bridges.
   Under v4 Tier B: line checks by Sol and a council at CP3. Then end your run.

## Rules
- Read `Theory_work/Wave3/HOLDS.md` at each step.
- Statuses are quoted verbatim; nothing below PROVED-CHECKED is presented as checked; "conditional on …" is carried.
- At most 2 helpers (`delegate_task`, provider `claudeAgent_claude_third`, Opus or Sonnet, effort high).
- One Sol (codex `gpt-6.1-sol`, high) fidelity read at CP1: does each reader statement follow from its master plus the
  bridges listed, with nothing hidden?
- `LOG.md` heartbeat with real local time.
- Do not touch `Theory_work/Wave3/W3-DIST/`, `Docs/Experiments/`, `Lean/`, or `Theory_work/Wave3/PROTOCOL_REVIEW/`.
