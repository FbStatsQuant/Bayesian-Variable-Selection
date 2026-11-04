# Theorem meeting (MEET-THM): the theorem list of paper 1 — dossier (DRAFT, not frozen)

Prepared by HQ ("SMC-BVS New HQ" thread), 2026-11-04. **Status: draft.** It is frozen before Round 1 is dispatched; later evidence is added only as dated files in `theory_campaign/MEET-THM/evidence/`. Round 0 (two fresh-eyes advisors) runs before the freeze and is an input.

## 0. Purpose

Fix the list of **main theorems of paper 1** (Biometrika-grade, about 10–20 theorems, each with as many lemmas as it needs), with precise statements, so that HQ can open **one HQ per theorem**. Each per-theorem HQ loops to a referee-checked proof and, for its finite or algebraic core, a Lean certificate. This thread becomes the meta-HQ. Felipe approves the final list. The chair does not vote; HQ approves the package and brings it to Felipe.

**No open questions may remain** at close: every candidate is in the list (with a fallback statement), deferred to later work with a reason, demoted to a cited lemma, or dropped with a reason.

## 1. Ground rules (Felipe's words; binding on every seat)

1. **Extraction standard.** "Song 2015, for a pre AI paper, pretty much manages to prove everything he is able to given his method, it's not the quality of the theorems, is the degree at which information was extracted from the methodology and into theoretical results. The local to global pdf, while crude - first draft - establishes goals such that, in my opinion, anything that does not have at least those results would look fairly incomplete. So again, it's not copying the theorems, what I want the campaigns you will run to do is extract until the last drop of information the method has into provable results. No rock can remain unturned at the end."
2. **Proposal goals.** "The final theory we write, in its own specific way has to achieve the theoretical results that were set as goals in the local to global pdf draft I gave, and also if possible, be equivalent to Song - 2015 in the sense that we would like to be able to prove important results of our method. But that is just a sanity check reference, we have no restriction and since the nature of our work is different then we have to be open to important results in general."
3. **Provable or nothing.** "We need strategies that work computing wise but also results that can be provable, a fancy heuristic and hypothetically gives me perfect accuracy but cannot be formally proved is as good as nothing to me."
4. **Scope.** The per-theorem HQs are for **paper 1, Biometrika level**. Harder results are recorded as future work with a reason; they get no HQ now.
5. **The method is fixed:** v3.1 as in `theory/MEET-v31:theory_campaign/MEET-v31/METHOD_v3.1_FINAL.md`. The one allowed change (Felipe, 2026-11-03): if a theorem needs a fixed budget (e.g. R, L, ℓ) to grow, the meeting may set that budget as an **explicit function of (n, p)**; growth rates only, nothing else.
6. **Generality.** "Make the final method remains something applicable to all n … hyperparameters being fixed small values, or depending on n, or P_n … like in Song (2015) … no weird arbitrary choice." Theorem hypotheses must be checkable conditions on the model and design, not on the study.
7. **Objectives, in order:** (1) accuracy in recovering the true posterior; (2) parallel scalability ("parallelizable enough so you could scale it to p values that you could not otherwise in sequential MCMC"; "We are not trying to parallelize over variables"; the parallel axis is particles and islands); (3) BVS selection accuracy. It must work under **correlated designs**, unlike Song & Liang (2015) split-and-merge.
8. **Empirical checks** use at most 10–20 seeds.

## 2. Roster

| Role | Who | Account | Rounds |
|---|---|---|---|
| Seat A | Fable 5.1, high | Claude Personal | R1–R3 |
| Seat B | Fable 5.1, high | Claude Work | R1–R3 |
| Seat C | gpt-6-astra, high | Codex | R1–R3 |
| Seat D (fresh eyes) | Fable 5.1, high; Round 0 from the method only, no prior theory | Claude Personal | R0, then R1–R3 as a full seat |
| Advisor E (raw Astra) | gpt-6-astra, high; Round 0 only, method only | Codex | R0 only |
| Chair | Opus 5.5, high, non-voting | Claude Work | all |
| Proof checker 1 | gpt-6.1-sol, high: checks claims of Seats A, B, D and the chair | Codex | each check wave |
| Proof checker 2 | Opus 5.5, high: checks claims of Seat C and Advisor E (cross-family rule) | Claude Work | each check wave |
| Auditor | gpt-6.1-sol, high (moves to Opus if Codex is tight): checks syntheses against seat files, and HQ's approval | Codex | after each synthesis, at close |
| Registrar | Sonnet: IDs, notation, dependency graph, status words vs registry | Claude Work | all |
| Citation checker | Sonnet: every cited paper/theorem number/repo path exists and says what is claimed | Claude Work | each round |
| Clerks | Haiku: verbatim extraction of seat texts, length caps, table formatting | Claude Work | as needed |

No API credit: subscriptions only. On a usage limit, the affected role waits for the reset.

## 3. Inputs (read with `git show origin/<branch>:<path>` after `git fetch origin`)

| What | Where |
|---|---|
| The method (fixed) | `theory/MEET-v31:theory_campaign/MEET-v31/METHOD_v3.1_FINAL.md`; base `Docs/Methodology/METHODOLOGY_v3.md` |
| Method-meeting theory consequences: 17 obligations N1–N17, inherent limitations, what is NOT inherent | `theory/MEET-v31:theory_campaign/MEET-v31/THEOREM_REVISION_INPUTS.md` |
| Draft theorem list (19 items G1–G6, tiers, HQ plan) | `theory/THM-SYNTH:theory_campaign/THM-SYNTH/{THEOREM_LIST.md,HQ_PLAN.md,REPORT.md}` |
| Inventory: component × property map, gap list | `theory/THM-INV:theory_campaign/THM-INV/REPORT.md` (+ `digests/`) |
| Registry of results and statuses | `theory/T38-RECORD:theory_campaign/T38-RECORD/{REGISTRY_v2.md,LOCKABLE_v2.md,T38_STATEMENT.md}` |
| Status vocabulary | `theory_campaign/PROTOCOL.md` (this branch) |
| Round 0 plans (fresh eyes) | `theory_campaign/MEET-THM/R0_D.md`, `R0_E.md` (added when done) |
| Proposal, Song–Liang 2015 | `theory_campaign/inputs/` |
| Literature | `theory/LIT-{PAR,SMC,MCMC,STAT,VENUE}:theory_campaign/LIT-*/REPORT.md` |
| Lean work | to be indexed by the registrar (e.g. T07Bayes.lean, T37Greedy/Lattice.lean, T21HPM.lean, T12Core) |
| Start ablation (confirmatory) | `theory/ABL-CONF` (running; evidence for the start theorems' numerical companion) |

## 4. Inclusion criteria (fixed before Round 1; HQ dry-runs them on the 19-item draft list first)

A theorem enters the paper-1 list only if all hold:
- **IC1 Statement:** precise, with every hypothesis named; about v3.1 as shipped, or the gap to the shipped method is itself stated as a lemma to prove.
- **IC2 Route:** a credible proof route with the key lemma named; difficulty rated.
- **IC3 Non-vacuous:** a concrete design family, including a genuinely correlated one where the theorem is about correlation, satisfies the hypotheses (exhibited, not asserted).
- **IC4 Not merely known:** if it is a published result applied to our setting, it becomes a **cited lemma**, not a theorem.
- **IC5 Serves the goals:** an objective (1)–(3), a proposal goal (§5.1–5.4, §13.1), or the Song–Liang coverage map.
- **IC6 Lean core named:** which finite/algebraic part can carry a Lean certificate, and which rests on cited probability theory.
- **IC7 Fallback:** a weaker statement that still ships if the full proof fails, and a stop rule for its HQ.

## 5. The theorem card (every candidate, every round)

ID · draft statement with hypotheses · the guarantee in one plain sentence · objective / proposal goal / Song–Liang item served · current status, **verbatim** from the registry, and whether it is about v3.1 as shipped (LS0, coded grid, island pooling) or a variant · self-checked only? (flag) · novelty (NEW / NEW-COMP / KNOWN—CITE / MODEST) with checked citations · proof route and key lemma · difficulty · Lean core · dependencies · risk · fallback statement · numerical companion (≤ 20 seeds), if any.

## 6. Agenda

1. **Coverage sweep.** Every proposal goal (§5.1–5.4, §13.1) and every Song–Liang (2015) result (Theorems 1–4, Corollaries 1–2, §6 complexity) maps to one of our theorems or to a written reason it does not apply. Every method component × property cell of THM-INV §1 is filled or marked "nothing provable" with a reason.
2. **The draft list, item by item:** keep / merge / split / demote to cited lemma / defer / drop, with corrected statements.
3. **New candidates:** from Round 0 (fresh eyes), the seats, and the 17 obligations N1–N17.
4. **Proposal §5.3 (weight stability under weak cross-block dependence).** Existing: O-WSTAB WS1–WS8 PROVED (no review), W(a–f) XF VERIFIED, but only under H-ORTH and an ideal grid; THM-SYNTH tiered it v2 (supplement remark). Felipe's ground rule 2 makes a paper-1 result here close to mandatory: decide the strongest provable version with genuinely weak (non-zero) cross-block correlation, or argue irrefutably why not.
5. **Proposal §5.4 (approximation error):** PIP and joint-inclusion errors are covered; TV/KL error and credible-interval coverage are not yet. Decide.
6. **The thesis theorem** ("correlation costs depth and particles, never correctness"): exact formal scope (fixed data vs asymptotic, favourable vs masked).
7. **Growth rates (ground rule 5):** does any theorem need R, L, ℓ or N to grow? If so, fix the rate as a function of (n, p) and record the method edit.
8. **Fidelity:** for every inherited result, is it about v3.1 as shipped? (v3 as run without LS0; ideal vs coded grid; equal-weight vs Ẑ-weighted pooling.)
9. **Scope:** p ≤ n^A in; whether any exponential-p statement is in reach (else future work with a reason).
10. **Novelty risk:** overlaps (e.g. Hou–Wang–Atchadé on finite-n claims; YWJ/ZYVR mixing results), each citation checked.
11. **Paper fit:** main text (about 6–8 theorems) vs supplement.
12. **HQ plan:** dependency graph, launch waves of 3–4 (foundations first), one charter per theorem.

## 7. Procedure

- **Round 0** (before the freeze): Seat D and Advisor E each write a theory plan from the method alone. The chair diffs them against the draft list: independent confirmations / new candidates / items already known false (flagged with the registry entry).
- **Round 1:** independent positions on agenda 1–5 and 8, in fixed tables (one card per candidate; a word cap per item).
- **Check wave 1, statement sanity:** for every candidate statement: true as written (counterexample search on small cases), non-vacuous (exhibit a design), key-lemma route plausible. Verdict per claim; never upgrade.
- **Round 2:** rebuttal against the chair's disagreement table (crux + what settles it per row) and the check verdicts; final statements; agenda 6, 7, 9–11.
- **Check wave 2** on the revised statements.
- **Round 3:** agenda 12 (HQ plan and charters); every seat confirms "nothing missing".
- **Close:** deliverables; auditor pass; HQ approval; Felipe's approval.

## 8. Rules (lessons from MEET-v31, `theory/MEET-v31:theory_campaign/MEET-v31/FORMAT_NOTES.md`)

- The agenda is frozen at dispatch; a late item gets its own independent mini-round.
- Tables per item, not essays; a word cap per item.
- A seat's own argument is "PROVED (by this seat, unchecked)" until a check is filed.
- Seats do not re-derive a result that already has a filed check; they cite the registry entry.
- Known-false results (e.g. SHARE-M(b), FD-NM, general LH locking per A-REV7) are listed and may not be re-proposed without addressing the refutation.
- Any decision rule fixed in advance is dry-run on mock tables first.
- Long compute runs detached; agents only read results.

## 9. Deliverables (under `theory_campaign/MEET-THM/`)

`THEOREM_LIST_FINAL.md` (cards), `COVERAGE_MATRIX.md` (proposal + Song–Liang + component × property → theorems), `HQ_CHARTERS/` (one per theorem), `REGISTRY_PAPER1.md` and `NOTATION.md` (registrar), `FUTURE_WORK.md` (deferred items with reasons), `MINUTES.md` (open questions: none), `FORMAT_NOTES.md`.

## 10. HQ's known issues (to be answered, not inherited)

1. §5.3 sits at v2 in the draft list (agenda 4).
2. §5.4 is only partly covered (agenda 5).
3. Several inherited results are self-checked only (e.g. N200 by its author; ADRAFT-ThmA Astra-on-Astra): flag and route to an independent check.
4. Some inherited proofs concern v3 without LS0, an ideal grid, or equal-weight pooling (agenda 8).
5. Delivery P(U) → 0 has no theorem (THM-INV §5.4); decide whether paper 1 states results joint with delivery or proves a delivery result.
6. The draft list's "depth free of N, H, R" wording was removed by MEET-v31 (decision 6): depth is stated at the island level only (Felipe: paper 1 claims island-level depth).
7. Biometrika length: about 14 candidate main theorems is a lot for one paper.
