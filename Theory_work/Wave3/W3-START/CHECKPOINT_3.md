# W3-START — CHECKPOINT 3 (final) — 2026-11-11, revised after council round R2

Lead: Claude Fable 5.2 (Claude Work, effort high). Worktree `C:/Users/felip/BVS-wt/W3-START`, no git state changed.

**RESULT: CP3-PASS (round R2, on the merged tree).** Council round R2 on STATEMENT v1.3.4: seat sol 9.2, seat opus
8.9, all six gates PASS, both on the same frozen manifest (`reviews/MANIFEST_R2.txt`, digest 5e26bb8b…). The
reconciliation reviewer finds every earlier CRITICAL or MAJOR finding resolved. Every claim of STATEMENT v1.3.4 is
proved, line-checked, swept and council-accepted. The statuses below read PROVED-CHECKED; under PROTOCOL rule 10 the
label takes effect only after HQ's acceptance audit.

**Two decisions are HQ's.**
* **§7.1 — the acceptance tool still refuses all 21 claims (A4), for a layout reason, not a mathematical one.** The
  tool requires the council manifest to cover each claim's status source; the status lines are in this file, which
  manifests exclude by design. The first CP3 audit did not reach this check. It needs either a narrow tool change or
  a third council round on a package whose frozen content carries the status lines.
* **§7.4 — the better-theorem review on the final statement returned four credible improvements**, none of the main
  clause.

## 1. What is proved, in plain words

* **Floor (deterministic).** Every unsaturated model gets start mass at most 1 − ⅓(n + 1)^{−1/2}, on every data set.
  With at least one null column, no condition gives a start-mass rate better than n^{−1/2}.
* **Fixed design (START-F).** Under an energy bound, a constant floor on the unnormalised Gram matrix of every set of
  at most 16 columns, visibility of the truths and an averaged leakage condition:
  * the start odds against the truth are O_P(n^{−1/2} × leakage functional) plus a polynomially small term;
  * to first order they equal the prior-weighted sum of the single-null block Bayes factors;
  * the bound is uniform over the class, with explicit constants.
* **Random design.** The uniform bound transfers to any design law with Gaussian noise given the design. For Gaussian
  rows with population visibility and no population leakage, π₀(S₀) ≥ 1 − n^{−1/2}e^{C√log n} with probability → 1, hence
  π₀(S₀) ≥ 1 − n^{−c} for every c < ½, for p ≤ n^A including p ≫ n.
* **Limits.** On the actual partition, one null above the level 1 + 2Ā, or one truth below 1 + 2A̲, sends π₀(S₀) → 0.
* **Interfaces.** P-START with a rate; the production form of P-OVL under a bounded leakage set; the misspecified form.
* **Not covered.** Strong-factor designs at p > K (decision D1) and masked truths stay outside the hypotheses.

## 2. Status per claim (one line per claim; the registry blocks of §10 cite these lines)


- W3-START:AGG — PROVED-CHECKED — Lemma AGG (table identities of the coded start). Line check: LC1-A: VERIFIED-WITH-AMENDMENTS.
- W3-START:FLOOR — PROVED-CHECKED — Theorem FLOOR (deterministic floor n^{-1/2}). Line check: LC1-A: VERIFIED-WITH-AMENDMENTS.
- W3-START:TK — PROVED-CHECKED — Lemma TK (toolkit under the unnormalised Gram floor). Line check: LC1-B: VERIFIED.
- W3-START:LEAK — PROVED-CHECKED — Bridge (B-L): leakage bridge with column levels, Lemma J. Line check: LC1-C: VERIFIED-WITH-AMENDMENTS.
- W3-START:VIS-c — PROVED-CHECKED — Bridge (B-V1): constant-level visibility. Line check: LC1-B: VERIFIED-WITH-AMENDMENTS.
- W3-START:VIS-m — PROVED-CHECKED — Bridge (B-V2): margin visibility. Line check: LC1-B: VERIFIED-WITH-AMENDMENTS.
- W3-START:ASM — PROVED-CHECKED — Lemma ASM (assembly). Line check: LC1-C: VERIFIED.
- W3-START:START-F — PROVED-CHECKED — Theorem START-F (fixed design, uniform form). Line check: LC1-C: VERIFIED.
- W3-START:F1 — PROVED-CHECKED — Corollary F1 (uniform leakage). Line check: LC2-A: VERIFIED.
- W3-START:F2 — PROVED-CHECKED — Corollary F2 (strong signals, exact order n^{-1/2}). Line check: LC2-A: VERIFIED.
- W3-START:F3 — PROVED-CHECKED — Corollary F3 (bounded gains). Line check: LC2-A: VERIFIED.
- W3-START:F4 — PROVED-CHECKED — Corollary F4 (isolated leaking columns). Line check: LC1-C (arithmetic, L3.5): VERIFIED-WITH-AMENDMENTS; LC2-A: VERIFIED.
- W3-START:NEC-b — PROVED-CHECKED — Lemma NEC-b (component diagnostics on the actual partition). Line check: LC2-A: VERIFIED.
- W3-START:NEC — PROVED-CHECKED — Proposition NEC (limits). Line check: LC2-A: VERIFIED.
- W3-START:TRANSFER — PROVED-CHECKED — Theorem START-R(a) (random-design transfer). Line check: LC2-A: VERIFIED-WITH-AMENDMENTS.
- W3-START:BR — PROVED-CHECKED — Bridge (B-R): Gaussian-row bridge. Line check: BR1 (break review): NOT VERIFIED against the literal target of v1.3.1 (scope of (E)); repaired by the statement amendment v1.3.2; SW1: proved as stated.
- W3-START:START-R — PROVED-CHECKED — Theorem START-R(b) (Gaussian rows). Line check: BR1: as for BR; SW1: proved as stated.
- W3-START:IF-START — PROVED-CHECKED — Corollary IF-START (P-START with a rate). Line check: LC2-B: VERIFIED.
- W3-START:OVL — PROVED-CHECKED — Proposition OVL (start mass under a bounded leakage set). Line check: LC2-B: VERIFIED; SW1: hypothesis repaired (uniform bound on the levels).
- W3-START:MIS — PROVED-CHECKED — Corollary MIS (misspecified candidate set). Line check: LC2-B: VERIFIED.
- W3-START:EX — PROVED-CHECKED — Examples: five families verify the hypotheses. Line check: LC2-B: VERIFIED-WITH-AMENDMENTS.

Evidence common to every line: exhaustive sweep `reviews/SW1_sweep_astra.md` (0 CRITICAL, 1 MAJOR, 7 MINOR, all fixed;
per-claim table "proved as stated" or "proved after the listed repairs"); council round R2 on v1.3.4,
`reviews/R2_council_sol.md` (9.2, gates PASS, every id "accepted") and `reviews/R2_council_opus.md` (8.9, gates PASS,
every id "accepted", three with non-blocking remarks); reconciliation `reviews/RC_R2_reconciliation_sol.md` (all
earlier CRITICAL/MAJOR findings resolved); the earlier council round R1 on v1.3.3 (`reviews/R1_council_sol.md` 9.1,
`reviews/R1_council_opus.md` 8.8, gates PASS). L1–L5 also: mid-point `reviews/MP1_midpoint_astra.md` (CONTINUE, each
claim "proved as stated").
Not verified, nothing claimed: the example families UNI-0 and exact-separation AR(1).

## 3. Review trail (whole ticket)

| round | seat | manifest | verdict | files |
|---|---|---|---|---|
| SL1 | Sol, blind | 53849ef3… | DO NOT LOCK: 4 CRITICAL, 3 MAJOR, 1 MINOR (v1.0) | `reviews/SL1_statement_lock_sol.md`, `reviews/SL1_disposition.md` |
| RC2 | Sol, reconciliation | 3c89e73a… | all SL1 CRITICAL/MAJOR resolved | `reviews/RC2_reconciliation_sol.md` |
| SL2 | Sol, blind | 3c89e73a… | LOCK WITH CHANGES (v1.2 locked) | `reviews/SL2_statement_lock_sol.md`, `reviews/SL2_disposition.md` |
| BT1 | Astra, blind | b3fafa79… | better-theorem review: P1, P2, P3 (all adopted by HQ) | `reviews/BT1_better_theorem_astra.md`, `reviews/BT1_disposition.md` |
| SC3 | Sol, blind | bf619625… | ACCEPT WITH CHANGES (v1.3 locked) | `reviews/SC3_change_check_sol.md`, `reviews/SC3_disposition.md` |
| LC1-A/B/C | Sol, Sol, Astra, blind | 867e1c93… | L1, L3, L4: VERIFIED-WITH-AMENDMENTS; L2, L5: VERIFIED | `reviews/LC1_A_line_check.md`, `reviews/LC1_B_line_check.md`, `reviews/LC1_C_line_check.md`, `reviews/LC1_disposition.md` |
| MP1 | Astra, blind | 8e08c109… | mid-point: CONTINUE | `reviews/MP1_midpoint_astra.md`, `reviews/MP1_disposition.md` |
| SC4 | Sol, blind | 26e9e509… | ACCEPT WITH CHANGES (v1.3.1 locked) | `reviews/SC4_diff_check_sol.md`, `reviews/SC4_disposition.md` |
| LC2-A/B | Sol, Sol, blind | 053bc169… | L6, L7, L10: VERIFIED; L8, L11: VERIFIED-WITH-AMENDMENTS | `reviews/LC2_A_line_check.md`, `reviews/LC2_B_line_check.md` |
| BR1 | Astra, blind | 053bc169… | break review of L9: NOT VERIFIED against the literal target; argument survives; rate not to be narrowed | `reviews/BR1_break_review_astra.md`, `reviews/LC2_BR1_disposition.md` |
| SW1 | Astra, blind | 4dabd787… | exhaustive sweep: 0 CRITICAL / 1 MAJOR / 7 MINOR, all fixed | `reviews/SW1_sweep_astra.md`, `reviews/SW1_disposition.md` |
| R1 | sol + opus, blind | 0a6daa2c… | council PASS on v1.3.3: 9.1 and 8.8, gates PASS; acceptance refused by the tool (A4: the manifest listed four wave/registry documents edited on `main` after the round) | `reviews/R1_council_sol.md`, `reviews/R1_council_opus.md`, `reviews/R1_disposition.md`, `reviews/R1_disposition_v134.md` |
| SC5 | Sol, blind | e6d59419… | diff check v1.3.3 → v1.3.4: EDITORIAL ONLY WITH CHANGES (0 CRITICAL / 0 MAJOR / 2 MINOR, both applied) | `reviews/SC5_diff_check_sol.md`, `reviews/SC5_disposition.md` |
| R2 | sol + opus, blind | 5e26bb8b… | **council PASS on v1.3.4: 9.2 and 8.9, gates PASS** | `reviews/R2_council_sol.md`, `reviews/R2_council_opus.md`, `reviews/R2_disposition.md` |
| RC-R2 | Sol, reconciliation | 5e26bb8b… | ALL EARLIER CRITICAL/MAJOR FINDINGS RESOLVED: yes; changes of meaning introduced by v1.3.4: none | `reviews/RC_R2_reconciliation_sol.md` |
| BT2 | Astra, blind | 5e26bb8b… | better-theorem review on the final statement: P1–P4, each rated ADOPT NOW; dispositions proposed, HQ decides (§7.4) | `reviews/BT2_better_theorem_astra.md`, `reviews/BT2_disposition.md` |

`manifest.py bind` on the two R2 council reviews: "bind: OK, 2 review(s) give a PASS verdict (>= 8.0)"; council cell
`R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)`.
`manifest.py verify` passes on the current tree for MANIFEST_R2 (52 files: the ticket files and 18 external inputs —
six pinned code files and twelve sources or consumers' statements; no wave document, no registry table). Citation
check: `reviews/CITECHECK.txt`, 203 citations, 0 missing or out of range.

## 4. Statement changes since CP2 (v1.3 → v1.3.4)

Approved by HQ at CP2 (v1.3.1): the scope note under (N2) and the wording of the bridge inputs.
Lead-initiated, each put through a blind review, **accepted by HQ in its CP3 audit** (LOG, 2026-11-11 19:00 CT):
1. v1.3.1 — bridge (B-R), clause C_L = 0: stated as tightness (O_P). (T3)(b) unchanged.
2. v1.3.1 — examples table: five verified families; UNI-0 and exact-separation AR(1) expected, not verified.
3. v1.3.2 — (B-R) and (T3)(b) carry the explicit hypothesis p > s₀. The rate is not narrowed.
4. v1.3.3 — Proposition OVL assumes levels bounded uniformly by a fixed ā; off-domain convention for the transfer;
   W_K defined; status wording.
Ordered by HQ in its CP3 audit:
5. **v1.3.4 — editorial only** (SC5 attests it after two wording repairs; the reconciliation finds no change of
   meaning): (N1) repeats κ_V > ½; Setting F says "s₀ ≥ 0 and any fixed A > 0"; the code pin reads "the CORE tree as of
   commit 72785fe"; "for some constant C" in the Gaussian-row summaries; Lemma L3.3 displays e^{2κ_E+ς_n};
   `ASSUMPTION_MAP.md` rewritten as one map of the final statement; two sentences of `numerics/RESULTS.md` made
   observational; `citecheck.py` takes an output path; `reviews/INPUTS.txt` without wave documents and registry
   tables (rule 15 as amended).
   Not applied, by the owner's rule on asymptotic results: R1's remark on the size of n at which F4 and example F-2
   become informative; it stays in `numerics/lemmas/RESULTS_LEMMAS.md` and is removed from the F4 registry block.
None of these changes a hypothesis or conclusion of (C0), (C1), (T0), (T1) or of the fixed-design bridges.

## 5. Kill budgets

* **(B-R):** one Fable attempt and one Astra break review; the argument survived; (T3)(b) is not narrowed.
* **Council:** round R1 passed on v1.3.3 but could not be accepted (manifest inputs, not mathematics); round R2
  passed on v1.3.4. Two of at most three rounds used.

## 6. Round R2: remarks not applied, and one erratum in the frozen content

Seat sol raised no issue. Seat opus raised six non-blocking issues (`reviews/R2_disposition.md`); the reconciliation
raised none. None is applied: the frozen content must stay unchanged after the passing round (LIFECYCLE §4.1 A4).
* **Erratum (opus issue 1).** The `STATEMENT.md:<line>` references in `REPORT.md` §3–§4 start one line early: v1.3.4
  added one line at `STATEMENT.md:65-66` and the report's references were not shifted. Several single-line references
  therefore point at the neighbouring row (TK at the (B1) row, and so on). The claim ids and names in the report are
  right, and **the registry blocks of §10 carry the corrected spans** (every span shifted by one and re-read against
  the statement). `citecheck.py` checks only that a range exists. Correcting `REPORT.md` is an editorial edit for the
  next version.
* The other five: the P-OVL row of the §4 interface table should say "production form"; two events of L9.5 need a
  convention when a projected mean is zero (it is not zero on the event used); a remark in L6 gives O((log n)²) for a
  constant that is O(log n), as the proofs use; F1's η = 0 sentence should repeat its premise; "every ε > 0" in
  (T1)(d) against ε ∈ (0, 1) in its proof (the bound is trivial for ε ≥ 1).

## 7. For HQ's acceptance audit

1. **Acceptance is refused by the tool (A4-council), 21 of 21 claims — HQ's decision.** Staged ingest of this file
   (item 6): the fragment introduces 0 ERROR, and the only acceptance errors are, for every id,
   "the frozen manifest …/reviews/MANIFEST_R2.txt does not cover …/CHECKPOINT_3.md (statement / premise / status
   source of …): list it in reviews/INPUTS.txt before the freeze".
   * *Cause.* Since the R04 fix (`Theory_work/INFRA/tools/bvsreg.py:1268-1280`) the council manifest must cover the
     file that holds a claim's status line. Here the status lines and the registry blocks are in `CHECKPOINT_3.md`
     (the departure from rule 8 that HQ accepted), and `manifest.py` never covers `CHECKPOINT_*.md`. The frozen
     `REPORT.md` §3 carries the author status "PROVED (by this seat)" only, so no file in the manifest has a
     PROVED-CHECKED line to point at.
   * *Why it was not seen at the first audit.* The tool checks coverage only after `verify` passes; at R1 `verify`
     failed on the four wave documents, so the coverage check was never reached.
   * *What it is not.* Statement and premise spans are covered; bind passes; no other acceptance check fails.
   * *Options.* **(T)** A narrow change of the tool: a status source that is the ticket's own `CHECKPOINT_<k>.md` is
     exempt from manifest coverage (statement and premise files stay required), with the usual INFRA review. No new
     round; v1.3.4 is accepted as it stands. **(R3)** A v1.3.5 whose frozen content carries one status line per
     claim (in `REPORT.md` §3, as the status proposed on council pass), with the six editorial remarks of §6, a Sol
     diff check and council round R3 — the third and last round of this ticket, spent on a formality.
     **The lead recommends (T).** If HQ prefers (R3), §7.4(b) could ride on the same round, at the risk described
     there.
   * Registry blocks stay in this file (HQ, first CP3 audit). Command:
     `ingest.py claims Theory_work/Wave3/W3-START/CHECKPOINT_3.md --staged`.
2. **Manifest and `main`.** MANIFEST_R2 was frozen on the merged tree (branch at 49df4a4, which contains `main` up to
   e52382f) and lists no wave document and no registry table, so HQ's edits to those on `main` no longer change it.
   `git diff HEAD main` over the 18 external inputs is empty (`main` at aa6ef7f): merging current `main` changes none
   of them.
3. **Consumed claims: none.** Rule 11 has nothing to compare.
4. **Headline strength — HQ's decision.** The better-theorem review was repeated on the final statement (BT2). It
   returned four improvements, each rated ADOPT NOW by the reviewer, and the lead finds each sketch credible
   (`reviews/BT2_disposition.md`; a reading, not a line check):
   * BT2-P1: the leading functional loses its term of order z_n/p, so F2 needs no growth condition on p;
   * BT2-P2: Proposition OVL also under margin visibility (V-m);
   * BT2-P3: a non-vacuous partition-free leaking-null limit for s₀ ≤ 15 (17 − s₀ leaking nulls);
   * BT2-P4: the lattice clause of (T3)(b) for |Q| up to n^{1/2−ε} instead of polylogarithmic.
   None touches the main clause (Q = S₀, p ≫ n), its rate, or Theorem FLOOR. Each changes a hypothesis or a conclusion
   of a claim, so adopting it needs a fresh review and a new council round.
   **Options.** (a) Accept v1.3.4 now with the four proposals disposed as `ticket` — one short follow-up (statement
   v1.4: statement lock, line checks, council) whose claims supersede START-F, F2, TRANSFER, IF-START, OVL, NEC, BR
   and START-R by implication. (b) Adopt the four inside this ticket: a v1.4, line checks of the changed proofs and
   council round R3, the last one allowed; a failed R3 would leave the whole ticket CP3-EXHAUSTED. **The lead
   recommends (a)**: it keeps a checked result on `main` now, and the improvements do not put it at risk. The registry blocks of §10 record `ticket`; change them if HQ chooses (b).
   The `lit:` gate is still open, so every claim stays `headline-strength pending` either way.
5. **Interface bridges for the registry.** A:P-START is delivered by W3-START:IF-START (with a rate); A:P-OVL, in its
   production form, by W3-START:OVL. Setting the `bridge` column of those two existing rows is HQ's edit.
6. **Pre-checks run by the lead** (the worktree's tools, which include the R04 fix; nothing written to the registry):
   * `ingest.py convert` on this file: 21 blocks, exit 0.
   * `ingest.py claims` (dry run): "21 claim(s) to add; 0 problem(s); new tickets ['W3-START']; 7 new assumption(s);
     10 sharpness row(s); 2 binding row(s)".
   * `ingest.py claims --staged` (disposable copy): "ERROR introduced by this claims fragment: 0; ERROR already in
     the live registry: 0"; acceptance REFUSED with 21 A4-council errors, all of the kind of item 1, and no other
     acceptance error (exit 1).
   * `manifest.py verify` on MANIFEST_R2: OK. `manifest.py bind` on the two R2 reviews: OK (worktree's tool and the
     main checkout's tool).
7. **Line endings.** `manifest.py` hashes raw bytes. The ticket files in this worktree have LF endings and git warns
   that it will write CRLF the next time it touches them. Run `verify` on this worktree as it stands; a fresh checkout
   with a different line-ending setting would not verify. Example: two inputs
   (`Theory_work/Wave3/W3-RM/lemmas/L1b_rss.md`, `L3_SANDR.md`) have CRLF here and LF in the main checkout, with
   identical committed content.

## 8. Open items and next steps

* W3-START-O1: Gaussian rows with a population leakage level and an explicit exponent (small follow-up to L9.5).
* W3-START-O2: no Gram floor at all (needs a rank-sensitive aggregation; low priority).
* W3-START-O3: growing s₀.
* W3-START-O4 … O7: the four improvements BT2-P1 … BT2-P4 (§7.4), one follow-up.
* A fixed-constant, probability → 1 bound when C_L = 0 (needs concentration across columns; BT2 found no route).
* UNI-0 and exact-separation AR(1) as verified examples.
* Editorial, for the next version: the six remarks of §6 (the report's line references first).
* What this ticket does not solve: the start on strong-factor designs at p > K. That needs a different mechanism, not
  a sharper analysis of this one.

## 9. Record

* **Agents in leg C:** lead (Claude Fable 5.2, Claude Work, high); SC4, LC2-A, LC2-B, R1-sol (Codex gpt-6.1-sol, high);
  BR1, SW1 (Codex gpt-6-astra, high); R1-opus (Claude Opus 5.5, Claude Work, high).
* **Agents in leg D (after HQ's first CP3 audit):** lead (Claude Fable 5.2, Claude Work, high); SC5, R2-sol, RC-R2
  (Codex gpt-6.1-sol, high); BT2 (Codex gpt-6-astra, high); R2-opus (Claude Opus 5.5, Claude Work, high). The lead's
  run was interrupted twice in this leg (T3 restart; an HQ-side interrupt) and resumed from the files on disk; two
  SC5 launches were cut off and produced no review. A status note of the second pointed the lead at one wrong
  sentence of the rewritten map, corrected before SC5 was re-frozen and re-run (LOG, 19:12 CT).
  Claude tally for the whole ticket: CP 1 / CW 3 (Claude Personal not used since leg B). No NOTS use.
* **Holds:** `HOLDS.md` (main checkout) read before each step: no holds.
* **Files changed since HQ's commit 49df4a4** (all in `Theory_work/Wave3/W3-START/`, uncommitted; HQ commits):
  * modified: `STATEMENT.md` (v1.3.4), `REPORT.md`, `ASSUMPTION_MAP.md`, `lemmas/L3_LEAK.md`, `numerics/RESULTS.md`,
    `citecheck.py`, `reviews/INPUTS.txt`, `reviews/CITECHECK.txt`, `LOG.md`, `CHECKPOINT_3.md`
  * new in `reviews/`: `MANIFEST_SC5.txt`, `MANIFEST_R2.txt`; briefs `BRIEF_SC5_sol.md`, `BRIEF_R2_sol.md`,
    `BRIEF_R2_opus.md`, `BRIEF_RC_R2_sol.md`, `BRIEF_BT2_astra.md`; reviews `SC5_diff_check_sol.md`,
    `R2_council_sol.md`, `R2_council_opus.md`, `RC_R2_reconciliation_sol.md`, `BT2_better_theorem_astra.md`;
    dispositions `SC5_disposition.md`, `R1_disposition_v134.md`, `R2_disposition.md`, `BT2_disposition.md`

## 10. Registry blocks (for `ingest.py`; statuses as proposed for after HQ's acceptance audit; spans of STATEMENT v1.3.4)


```
REGISTRY
claim: W3-START:AGG | kind: lemma | statement: STATEMENT.md:197-211 | premises: none (deterministic)
name: Lemma AGG (table identities of the coded start)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:38
assumptions: A:EX-A ; A:BLOCK-LE-16
conclusion: identity: two-sided bounds of the start odds by the table functionals T1, U, Xi; lattice bound; one-step table ratio at least (n+1)^{-1/2} | scope: every valid data set, n at least 4, any partition with blocks of size at most min(16, K), any reference model
depends_on: —
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:FLOOR | kind: theorem | statement: STATEMENT.md:241-243 | premises: none (deterministic)
name: Theorem FLOOR (deterministic floor n^{-1/2})
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:39
assumptions: A:EX-A ; A:BLOCK-LE-16
conclusion: negative: 1 - pi0(S) is at least (1/3)(n+1)^{-1/2} for every unsaturated model on every data set; with a null column the start odds are at least T1 and T1 is at least (1/2)(n+1)^{-1/2} | rate: n^{-1/2} cannot be improved | scope: every valid data set, n at least 4
depends_on: W3-START:AGG@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:TK | kind: lemma | statement: STATEMENT.md:233 | premises: STATEMENT.md:135-139
name: Lemma TK (toolkit under the unnormalised Gram floor)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:40
assumptions: A:START-E (new | Energy bound and polynomial dimension | squared norm of mu at most Mn, p at most n^A with A positive, s0 fixed, p greater than s0 for all large n | STATEMENT.md:135 | shared no | bridge W3-START:TK) ; A:START-GF (new | Constant unnormalised Gram floor on sets of size at most 16 | smallest eigenvalue of X_T'X_T at least g_* for every set T of size 1 to 16 | STATEMENT.md:136 | shared no | bridge W3-START:TK) ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: toolkit event of probability at least 1 - 2exp(-n^{1/3}) - 2/n on which RSS_U = (n-1) tau_U^2 (1 + O(n^{-1/3})) and every block-table score has an expansion with a bounded remainder kappa_E(g_*, M, sigma^2) | scope: fixed design, s0 at least 0, uniform over the class
depends_on: —
implies: —
sharpness: A:START-GF = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100) ; A:START-E = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:LEAK | kind: lemma | statement: STATEMENT.md:234 | premises: STATEMENT.md:135-139 ; STATEMENT.md:152-157
name: Bridge (B-L): leakage bridge with column levels, Lemma J
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:41
assumptions: A:START-E ; A:START-GF ; A:START-AL (new | Averaged leakage with a level vector | there is a level vector h for Q with tail budget b_n(h) tending to 0 and rho_n(Q; h) tending to 0 | STATEMENT.md:152 | shared no | bridge W3-START:LEAK) ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: U_Q = O_P(n^{-1/2} L^b_n(Q; h)) and T1 = O_P(n^{-1/2} L^{b,0}_n(h)), with explicit Markov bounds; small gains follow from the averaged condition | scope: fixed design, any partition with blocks of size at most 16, uniform
depends_on: W3-START:TK@proof
implies: —
sharpness: A:START-AL = NECESSARY-FOR-ROUTE (evidence: ASSUMPTION_MAP.md:32)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:VIS-c | kind: lemma | statement: STATEMENT.md:235 | premises: STATEMENT.md:135-151 ; STATEMENT.md:152-157
name: Bridge (B-V1): constant-level visibility
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:42
assumptions: A:START-E ; A:START-GF ; A:START-V (new | Visibility of the truths | constant level (V-c) with c_V greater than 1 + 2A, or the margin form (V-m) with constants c_m and eps_0 | STATEMENT.md:140 | shared no | bridge W3-START:VIS-m) ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: P(Xi(Q) greater than n^{-kappa}) tends to 0 for every kappa below (c_V - 1 - 2A)/2 | scope: fixed design, uniform
depends_on: W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:AGG@proof
implies: —
sharpness: A:START-V = WEAKENABLE (evidence: lemmas/L11_EXAMPLES.md:41)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:VIS-m | kind: lemma | statement: STATEMENT.md:236 | premises: STATEMENT.md:135-151
name: Bridge (B-V2): margin visibility
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:43
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: P(Xi(Q) greater than n^{-kappa}) tends to 0 for every kappa below c_m/2 | scope: fixed design, uniform
depends_on: W3-START:TK@proof
implies: —
sharpness: A:START-V = NECESSARY (evidence: lemmas/L7_NEC.md:28)
binding: A:START-V forced by W3-START:AGG via the deterministic lower bound of the start odds by c_s times Xi (Xi tending to 0 is necessary when s0 + 16 is at most K)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:ASM | kind: lemma | statement: STATEMENT.md:213-219 | premises: STATEMENT.md:174-191
name: Lemma ASM (assembly)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:44
assumptions: A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1 - pi0(L(Q)) = O_P((size of Q + 1) n^{-1/2} L^b_n(Q; h)) + O_P(n^{-kappa}); at Q = S0 the odds bound and the first-order form o0/T1 tends to 1 | scope: fixed design, given the interface properties
depends_on: W3-START:AGG@proof ; W3-START:FLOOR@proof ; W3-START:TK@stmt ; W3-START:LEAK@stmt ; W3-START:VIS-c@stmt ; W3-START:VIS-m@stmt
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:START-F | kind: theorem | statement: STATEMENT.md:245-264 | premises: STATEMENT.md:135-157
name: Theorem START-F (fixed design, uniform form)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:45
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: start odds against S0 are O_P(n^{-1/2} L^0_n(h) + n^{-1} L_n(S0; h)^2) + o_P(n^{-kappa}); lattice mass outside {S0 subset T subset Q} is O_P(rho_n(Q; h)) + o_P(n^{-kappa}); o0/T1 tends to 1 when kappa_V exceeds 1/2; uniform finite-n form with exceptional probability eps + b_n(h) | rate: n^{-1/2} times the leakage functional | scope: fixed design, p at most n^A (p much larger than n allowed), s0 fixed, partition-free hypotheses
depends_on: W3-START:AGG@proof ; W3-START:FLOOR@proof ; W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:VIS-c@proof ; W3-START:VIS-m@proof ; W3-START:ASM@proof
implies: —
sharpness: A:START-AL = NECESSARY-FOR-ROUTE (evidence: ASSUMPTION_MAP.md:32) ; A:START-V = NECESSARY (evidence: lemmas/L7_NEC.md:28) ; A:START-GF = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100) ; A:START-E = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100)
binding: A:START-V forced by W3-START:NEC-b via one truth below the level 1 + 2A sends pi0(S0) to 0
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:P1(reviews/BT1_better_theorem_astra.md) ; better-disposition:P1=adopted(reviews/BT1_disposition.md) ; better-proposal:P2(reviews/BT1_better_theorem_astra.md) ; better-disposition:P2=adopted(reviews/BT1_disposition.md) ; better-proposal:P3(reviews/BT1_better_theorem_astra.md) ; better-disposition:P3=adopted(reviews/BT1_disposition.md) ; better-proposal:BT2-P1(reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=ticket(reviews/BT2_disposition.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:F1 | kind: corollary | statement: STATEMENT.md:268-271 | premises: STATEMENT.md:135-157
name: Corollary F1 (uniform leakage)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:46
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under uniform gains at most eta tau^2 log n with eta below eta_A, 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-kappa} + n^{-kappa} with probability tending to 1, for kappa below min(kappa_L, kappa_V) | rate: n^{-kappa_L(eta, A)} | scope: fixed design
depends_on: W3-START:START-F@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:F2 | kind: corollary | statement: STATEMENT.md:272-275 | premises: STATEMENT.md:135-157
name: Corollary F2 (strong signals, exact order n^{-1/2})
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:47
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under strong signals and gains at most eta' Delta_U log n given truth subsets, o0 = O_P(n^{-(1-eta')/2}) + o_P(n^{-kappa}); exact order n^{-1/2} when eta' = 0 and kappa_V exceeds 1/2 | rate: n^{-(1-eta')/2} | scope: fixed design, Q = S0
depends_on: W3-START:START-F@proof ; W3-START:FLOOR@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:F3 | kind: corollary | statement: STATEMENT.md:276-277 | premises: STATEMENT.md:135-157
name: Corollary F3 (bounded gains)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:48
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under gains bounded by C0 tau^2, 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-1/2} exp(C2 sqrt(log n)) + n^{-kappa} with probability tending to 1 | rate: n^{-1/2} exp(C2 sqrt(log n)) | scope: fixed design
depends_on: W3-START:START-F@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:F4 | kind: corollary | statement: STATEMENT.md:278-287 | premises: STATEMENT.md:135-157
name: Corollary F4 (isolated leaking columns)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:49
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: a bounded number of columns may leak at any constant level below 1 + 2 liminf(log p/log n): with reduced levels on those columns the averaged leakage condition holds and START-F applies | scope: fixed design
depends_on: W3-START:START-F@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:NEC-b | kind: lemma | statement: STATEMENT.md:221-226 | premises: STATEMENT.md:135-139
name: Lemma NEC-b (component diagnostics on the actual partition)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:50
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: negative: on the actual partition, one null with gain at least c tau^2 log n given the truths of its block, c above 1 + 2 limsup(log p/log n), or one truth with gain at most c tau^2 log n given the other truths of its block, c below 1 + 2 liminf(log p/log n), gives pi0(S0) at most n^{-kappa'} with probability tending to 1 | scope: fixed design
depends_on: W3-START:TK@proof ; W3-START:AGG@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:NEC | kind: proposition | statement: STATEMENT.md:316-331 | premises: STATEMENT.md:135-139
name: Proposition NEC (limits)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:51
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: negative: the exponent 1/2 is optimal; partition-free forms of the one-column limits: the leaking-null form is vacuous for s0 at most 15 and has content for s0 at least 16; the weak-truth form shows that the visibility constant 1 + 2A cannot be lowered | scope: fixed design
depends_on: W3-START:NEC-b@proof ; W3-START:FLOOR@proof ; W3-START:F2@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:BT2-P3(reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P3=ticket(reviews/BT2_disposition.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:TRANSFER | kind: theorem | statement: STATEMENT.md:290-305 | premises: STATEMENT.md:135-157
name: Theorem START-R(a) (random-design transfer)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:52
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: for any design law with Gaussian noise given the design and coefficients, support, leakage set and levels measurable in the design, the fixed-design bounds hold under the joint law on design sets of probability tending to 1 | scope: random design; response-selected targets not covered
depends_on: W3-START:START-F@proof ; W3-START:F1@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:BR | kind: lemma | statement: STATEMENT.md:237 | premises: STATEMENT.md:160-167
name: Bridge (B-R): Gaussian-row bridge
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:53
assumptions: A:START-R-FL (new | Population floor on sets of size at most 16 + s0 | smallest eigenvalue of every principal submatrix of Sigma_n of size at most 16 + s0 is at least c_Sigma | STATEMENT.md:160 | shared no | bridge W3-START:BR) ; A:START-R-V (new | Population visibility PTV(a_V) | conditional covariance of each truth with the signal given any 15 other columns is at least a_V in absolute value | STATEMENT.md:162 | shared no | bridge W3-START:BR) ; A:START-R-L (new | Localised bounded population leakage | leakage set Q and neighbourhoods H_l of polylogarithmic size with conditional covariances at most C_L n^{-1/2} with the truths and at most r_n with remote columns | STATEMENT.md:163 | shared no | bridge W3-START:BR)
conclusion: target: with probability tending to 1 the Gaussian-row design satisfies the energy bound, the normalised floor on sets of size at most 16, visibility at every fixed level and L_n(Q) at most exp(C sqrt(log n)); with exactly zero population leakage L_n(Q) = O_P((log n)^{15 kappa_Q + 1/2}) (tightness) | scope: Gaussian rows, p at most n^A, p greater than s0, p much larger than n allowed
depends_on: W3-START:LEAK@proof
implies: —
sharpness: A:START-R-L = NECESSARY-FOR-ROUTE (evidence: lemmas/L9_BR.md:175)
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:START-R | kind: theorem | statement: STATEMENT.md:306-314 | premises: STATEMENT.md:160-167
name: Theorem START-R(b) (Gaussian rows)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:54
assumptions: A:START-R-FL ; A:START-R-V ; A:START-R-L ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-1/2} exp(C_R sqrt(log n)) with probability tending to 1; with Q = S0, pi0(S0) is at least 1 - n^{-c} for every c below 1/2; with zero population leakage the rate is O_P((size of Q + 1) n^{-1/2} (log n)^{15 kappa_Q + 1/2}) | rate: n^{-1/2} exp(C_R sqrt(log n)) | scope: Gaussian rows, p at most n^A, p greater than s0, p much larger than n allowed, s0 fixed
depends_on: W3-START:BR@proof ; W3-START:TRANSFER@proof ; W3-START:START-F@proof ; W3-START:F1@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:BT2-P4(reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P4=ticket(reviews/BT2_disposition.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:IF-START | kind: corollary | statement: STATEMENT.md:334-338 | premises: STATEMENT.md:135-157
name: Corollary IF-START (P-START with a rate)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:55
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1_A o0 = O_P(r_n) with a deterministic rate r_n tending to 0, under START-F at Q = S0 or under START-R at Q = S0; this is the premise P-START of W3-SAMP with a rate | rate: r_n | scope: start interface only; P-CONC, P-MAP and the algorithm premises of W3-SAMP are not supplied
depends_on: W3-START:START-F@proof ; W3-START:START-R@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:OVL | kind: proposition | statement: STATEMENT.md:339-344 | premises: STATEMENT.md:135-157
name: Proposition OVL (start mass under a bounded leakage set)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:56
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: with a leakage set of bounded excess size and leak levels bounded uniformly, pi0(S0) is at least n^{-E_n - eps} with probability tending to 1; hence the production form of P-OVL when limsup(E_n - max(1, log p/log n)) is negative | scope: fixed design, constant-level visibility (V-c)
depends_on: W3-START:AGG@proof ; W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:VIS-c@proof
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md) ; better-proposal:BT2-P2(reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P2=ticket(reviews/BT2_disposition.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:MIS | kind: corollary | statement: STATEMENT.md:346-357 | premises: STATEMENT.md:135-157
name: Corollary MIS (misspecified candidate set)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:57
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under a Gaussian-residual omitted part the candidate data follow the model with truth supp(beta^C) and noise variance sigma^2 + tau^2, so every claim holds for the start of the method re-run on the candidate data provided its hypotheses hold after the substitution | scope: fixed candidate design; random candidate design through the transfer
depends_on: W3-START:START-F@stmt ; W3-START:TRANSFER@proof ; W3-START:NEC@stmt ; W3-START:IF-START@stmt ; W3-START:OVL@stmt
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```

```
REGISTRY
claim: W3-START:EX | kind: proposition | statement: STATEMENT.md:359-371 | premises: STATEMENT.md:135-167
name: Examples: five families verify the hypotheses
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:58
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:START-R-FL ; A:START-R-V ; A:START-R-L
conclusion: target: five example families satisfy the partition-free hypotheses: orthogonal designs; near-duplicate null columns; one truth with fifteen correlated nulls (margin visibility holds, constant-level visibility fails, default-level leakage condition fails and F4 applies); Gaussian rows with independent columns; block-diagonal covariance with one truth per group | scope: fixed-design examples have p at most n - 1; UNI-0 and exact-separation AR(1) are not verified and not claimed
depends_on: W3-START:START-F@stmt ; W3-START:F1@stmt ; W3-START:F2@stmt ; W3-START:F4@stmt ; W3-START:START-R@stmt
implies: —
gates: correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md)
council: R2; MANIFEST 5e26bb8b58f98718959378cff18789927c6a8a1e881e3d77af06ae1ccb2e9885; sol=9.2 PASS(reviews/R2_council_sol.md); opus=8.9 PASS(reviews/R2_council_opus.md)
notes: headline-strength pending (lit gate open; better-theorem review BT2 repeated on v1.3.4, proposals disposed in reviews/BT2_disposition.md)
```
