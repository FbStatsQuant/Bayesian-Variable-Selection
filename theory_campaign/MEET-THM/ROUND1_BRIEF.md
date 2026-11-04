# MEET-THM · Round 1 brief (identical for Seats A, B, C, D)

Chair (non-voting), 2026-11-04. The agenda is frozen at dispatch.

You are **Seat {SEAT}** of MEET-THM, the meeting that fixes the list of **main theorems of paper 1** of the SMC-BVS project (Biometrika; about 10–20 theorems, each with its lemmas). Round 1 is **independent**: write your own position; no other seat's Round 1 exists for you. {SEAT_NOTE}

You are **read-only**. Do not edit, commit or push anything in the repository. Your **final message is your answer**, in full (not a summary of a file): the chair files it verbatim as `R1_{SEAT}.md`. You may run small local checks (Python, under a minute each, ≤ 20 seeds, in a scratch directory outside the repository; no Owls, no long jobs); quote the script and its output compactly in your answer.

Working directory: `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-THM`. Run `git fetch origin` first; read other branches with `git show origin/<branch>:<path>`.

## Read (in this order; then the rest as needed)

1. `theory_campaign/MEET-THM/DOSSIER.md` — binding ground rules (§1), inclusion criteria IC1–IC7 (§4), the theorem card (§5), agenda (§6), rules (§8), HQ's known issues (§10), IC dry run (§11).
2. `theory_campaign/MEET-THM/R0_DIFF.md` — the merged candidate table: every draft entry, Seat D item, Advisor E package and obligation N1–N17 under one ID **K01, K02, …**. Use K-IDs (and the source IDs in brackets) everywhere.
3. The method (fixed): `git show origin/theory/MEET-v31:theory_campaign/MEET-v31/AMENDMENT_HQ_01.md`, then `…/METHOD_v3.1_FINAL.md`; base `Docs/Methodology/METHODOLOGY_v3.md`. N9 kernel validity: `origin/theory/N9-KERNEL:theory_campaign/N9-KERNEL/REPORT.md`. Independent reviews: `/home/fb31/hq_reviews/HQ_DISPOSITIONS.md` (and `SOL1_proof_check.md`, `SOL2_audit.md`).
4. What exists: the registrar's index `origin/theory/MEET-THM-REG:theory_campaign/MEET-THM/evidence/REGISTRY_INDEX.md` (statuses verbatim, check history, Lean index, **§4 known-false list**, §5 conflicts); the draft list `origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/{THEOREM_LIST.md,REPORT.md,HQ_PLAN.md}`; the inventory `origin/theory/THM-INV:theory_campaign/THM-INV/REPORT.md` (§1 component map, §3 coverage, §5 gaps); obligations `origin/theory/MEET-v31:theory_campaign/MEET-v31/THEOREM_REVISION_INPUTS.md`; the registry `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/REGISTRY_v2.md`.
5. Round 0 plans: `theory_campaign/MEET-THM/R0_D.md` (Seat D), `theory_campaign/MEET-THM/R0_E.md` (Advisor E). Their proposals are on the table; everything in them is an unchecked proposal.
6. Goals: `theory_campaign/inputs/Local_to_Global_proposal.pdf` (§5.1–5.4, §13.1) and `theory_campaign/inputs/SongLiang2015.pdf` (Theorems 1–4, Corollaries 1–2, §6). Literature: `origin/theory/LIT-{PAR,SMC,MCMC,STAT,VENUE}:theory_campaign/LIT-*/REPORT.md`.

## Binding rules (from the dossier and HQ)

- **Method fixed** (v3.1 as amended). The one allowed change: a fixed budget (R, L, ℓ, N) may become an explicit function of (n, p) if a theorem needs it (growth rates only). Anything else you think is needed: put it in §I as an HQ question; do not assume it.
- **Paper 1 claims island-level depth only.** No "depth free of N, H, R" wording.
- **Binding goals** (proposal §5.1–5.4, §13.1): a theorem's fallback may never silently drop one; if it would, say so (it escalates to HQ).
- **Status words**, never upgraded: copy registry statuses verbatim; your own argument is "PROVED (by this seat, unchecked)" at most; otherwise PROOF SKETCH / CONJECTURE / OPEN / COUNTEREXAMPLE (with construction).
- **Do not re-derive** a result that has a filed check; cite its registry ID. **Known-false** results (index §4: e.g. SHARE-M(b), FD-NM, general LH locking per A-REV7) may not be re-proposed without addressing the refutation.
- **Hypotheses** must be checkable conditions on the model and design (not on the study); no arbitrary constants (ground rule 6).
- **IC1–IC7** (dossier §4) decide inclusion. IC4: a published result applied to our setting is a **cited lemma**, not a theorem. IC3: exhibit a design family (a genuinely correlated one when the theorem is about correlation), don't assert one.
- **"No open questions" rule** (MEET-v31 SYNTH_R1 §3, accepted there in Round 2): a *method question* is closed when the method decision no longer depends on it; an unproved *property* of the decided method is a **theorem obligation** (here: a candidate with a status and a fallback), not an open question; an **inherent limitation** is only a statement that is PROVED impossible or follows by definition from the SMC structure, the prior, or the problem. Do not relabel a missing proof as a limitation.

## Agenda for Round 1: items 1–5 and 8 (dossier §6). Answer in these sections, tables only

Free text: **≤ 300 words per theorem card**, **≤ 60 words per table cell**, whole answer **≤ 14,000 words**. No essays.

**§A Coverage sweep (item 1).**
A1: proposal goal (§5.1, §5.2, §5.3, §5.4 split into PIP / joint-PIP / TV / KL / credible-interval coverage, §13.1, §4.4/§8.2 diagnostics) → K-ID(s) that deliver it, or a written reason it cannot be delivered.
A2: Song–Liang 2015 Thm 1, Thm 2, Thm 3, Thm 4, Cor 1, Cor 2, Thm S (MAP), §6 complexity → K-ID(s) or reason it does not apply.
A3: every empty or partial cell of THM-INV §1 (component × property) → K-ID, or "nothing provable" with a reason.

**§B The draft list, item by item (item 2).** All 24 entries (V1–V4, A1–A4, D1–D4, S1–S4, C1, R1–R7): `entry | K-ID | keep / merge (with) / split / demote to cited lemma / defer / drop | corrected statement or reason | IC that decides it`.

**§C New candidates (item 3).** Every K row that is NEW-*, OBLIGATION-ONLY or not yet covered by §B: `K-ID | main / supplement / cited lemma / future work / drop | reason (≤ 40 words)`. Every K-ID of R0_DIFF must appear in §B or §C.

**§D Theorem cards.** One card (dossier §5 fields, as a table) for every candidate you place in **main or supplement**: ID · statement with every hypothesis named · guarantee in one sentence · objective / proposal goal / Song–Liang item · current status verbatim (registry ID) and whether about v3.1 as shipped (LS0, coded grid, Ẑ-weighted island pooling) or a variant · self-checked only? · novelty (NEW / NEW-COMP / KNOWN—CITE / MODEST, citations you checked) · proof route and key lemma · difficulty · Lean core · dependencies · risk · fallback statement + stop rule · IC3 design exhibited · numerical companion (≤ 20 seeds), if any.

**§E Proposal §5.3, weight stability under weak cross-block dependence (item 4).** The strongest provable statement with **genuinely weak, non-zero** cross-block correlation (not H-ORTH, not an ideal grid if avoidable), as a card; the IC3 design family; the key lemma and why its route is credible. Or, if you hold that no such paper-1 theorem exists, an argument a referee would accept, and what then ships against the binding goal (escalation to HQ).

**§F Proposal §5.4, approximation error (item 5).** TV/KL error and credible-interval coverage: for each, a card or the reason it is not provable or not meaningful for this method (note the method corrects exactly; say what "approximation error" then refers to), and what ships against the binding goal.

**§G Fidelity (item 8).** Every inherited result you rely on in §D: `registry ID | about v3.1 as shipped? (LS0 / coded grid / Ẑ-weighted pooling; each yes/no/unknown, with path:line) | the gap | the gap lemma to prove (statement)`.

**§H Your list.** Ranked, ≤ 20 entries: `rank | K-ID | name | main / supplement | one-line reason`.

**§I Questions for HQ.** Only decisions outside the meeting's authority (method changes beyond growth rates; binding-goal escalations). "None" is a valid answer.
