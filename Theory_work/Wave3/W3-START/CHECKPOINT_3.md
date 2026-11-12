# W3-START — CHECKPOINT 3 (final) — 2026-11-11

Lead: Claude Fable 5.2 (Claude Work, effort high). Worktree `C:/Users/felip/BVS-wt/W3-START`, no git state changed.

**RESULT: CP3-PASS.** The council passed in round 1: seat sol 9.1, seat opus 8.8, all six gates PASS, both on the same
frozen manifest. Every claim of STATEMENT v1.3.3 is proved, line-checked, swept and council-accepted. The statuses
below read PROVED-CHECKED; under PROTOCOL rule 10 the label takes effect only after HQ's acceptance audit.

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
per-claim table "proved as stated" or "proved after the listed repairs"); council `reviews/R1_council_sol.md` (9.1,
gates PASS) and `reviews/R1_council_opus.md` (8.8, gates PASS), every id "accepted". L1–L5 also: mid-point
`reviews/MP1_midpoint_astra.md` (CONTINUE, each claim "proved as stated").
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
| R1 | sol + opus, blind | 0a6daa2c… | **council PASS: 9.1 and 8.8, gates PASS** | `reviews/R1_council_sol.md`, `reviews/R1_council_opus.md`, `reviews/R1_disposition.md` |

`manifest.py bind` passes for every round. `manifest.py verify` passes on the current tree for MANIFEST_R1. Citation
check: `reviews/CITECHECK.txt`, 202 citations, 0 missing or out of range.

## 4. Statement changes since CP2 (v1.3 → v1.3.3), for HQ's attention

Approved by HQ at CP2 (v1.3.1): the scope note under (N2) (vacuous for s₀ ≤ 15; the limit is claimed on the actual
partition through (C2)(i)) and the wording of the bridge inputs.
**Made on my own judgment, each put through a blind review, and reported here for HQ's decision:**
1. v1.3.1 — bridge (B-R), clause C_L = 0: stated as tightness (O_P), not as a fixed-constant bound with probability → 1.
   The theorem (T3)(b) is unchanged: its C_L = 0 clause was already an O_P statement.
2. v1.3.1 — examples table: five verified families; UNI-0 and exact-separation AR(1) listed as expected, not verified.
3. v1.3.2 — (B-R) and (T3)(b) carry the explicit hypothesis **p > s₀** (§6 already excluded any claim at p = s₀). This is
   the repair of the break review's finding; it does not narrow the rate.
4. v1.3.3 — Proposition OVL assumes levels **bounded uniformly** by a fixed ā (sweep finding, MAJOR); a convention for
   the transfer off the admissible design sets; W_K defined; status wording brought up to date.
None of these changes a hypothesis or conclusion of (C0), (C1), (T0), (T1) or of the fixed-design bridges.

## 5. Kill budgets

* **(B-R):** one Fable attempt (`lemmas/L9_BR.md`) and one Astra break review (BR1). Outcome: the probabilistic argument
  survived; the bridge row needed the hypothesis p > s₀ made explicit. **(T3)(b) is not narrowed.** No return through
  CP1 was triggered; if HQ reads change 3 above as a narrowing, that is the point to decide.
* Council: passed in round 1 of at most 3.

## 6. Council remarks not applied

Both seats raised only non-blocking issues (ten in all; `reviews/R1_disposition.md`). None is applied: the acceptance
tool refuses a claim whose frozen content changed after the passing round. The two that matter:
* F4 and example F-2 are meaningful only for astronomically large n (the tail budget of the F4 levels is below 1 only
  for log n > 256). The numerics report says so; the statement and the report do not.
* `ASSUMPTION_MAP.md` keeps its old body and corrects it in appended sections.
A version v1.3.4 with these ten edits would need one more council round.

## 7. For HQ's acceptance audit

1. **Registry blocks are here, not in `REPORT.md`.** `manifest.py verify` reports changed and added files, and A4
   requires the council manifest to verify on the final tree. So `REPORT.md` was frozen before the council in a
   review-blind form, and everything that depends on the council is in this file, which the manifest excludes. This
   departs from PROTOCOL rule 8 ("REPORT.md ends with the registry block"). Ingest with
   `ingest.py claims Theory_work/Wave3/W3-START/CHECKPOINT_3.md --staged`.
2. **Four external inputs of the manifest have changed on `main` since the branch base** (b469719 → c939971):
   `Theory_work/Wave3/PROTOCOL.md`, `Theory_work/INFRA/LIFECYCLE.md`, `Theory_work/INFRA/templates/ASSUMPTION_MAP.md`,
   `Theory_work/INFRA/registry/claims.tsv`. After merging `main` into the ticket branch, `manifest.py verify` on
   MANIFEST_R1 will report these four as CHANGED. None is a proof premise, and the statuses quoted in the statement
   are unchanged on current `main` (checked: C-GROW:L0.1, C-GROW:L0.2, W3-SAMP:C, W3-SAMP:D, W1-PXN:Thm-PXN(S),
   C-MIS:LemR, W3-RM:B1, W3-RM:B2tau, W3-RM:SAND-R). Options: (a) accept under rule 10 ("each diff since the freeze
   went through rule 15"), the diffs being HQ's own wave documents; (b) HQ merges `main` into the branch and I run a
   council round R2 on the merged tree, with the ten non-blocking edits applied (two more council seats).
   I recommend (a) if the tool allows it and (b) otherwise.
3. **Consumed claims: none.** Rule 11 has nothing to compare.
4. **Headline strength: pending.** The better-theorem review (BT1) was run on v1.2 and its three proposals were
   adopted; it was not repeated on the final statement, and the `lit:` gate is open. The claims are submitted as checked
   results, `headline-strength pending`.
5. **Interface bridges for the registry.** A:P-START is delivered by W3-START:IF-START (with a rate); A:P-OVL, in its
   production form, by W3-START:OVL. Setting the `bridge` column of those two existing rows is HQ's edit.
6. **Pre-checks run by the lead** (worktree's copy of the tools, which predates the R04 fix; nothing written to the
   registry): `ingest.py convert` on this file: 21 blocks, exit 0. `ingest.py claims` dry run: "21 claim(s) to add; 0
   problem(s); 7 new assumption(s); 10 sharpness row(s); 2 binding row(s)". `ingest.py claims --staged` (disposable
   copy): "0 ERROR … acceptance … PASS; 0 acceptance ERROR". Current `main`'s `manifest.py` gives `verify: OK` and
   "bind: OK, 2 review(s) give a PASS verdict (>= 8.0)" on this worktree. The staged ingest on the merged tree is HQ's.
7. **Line endings.** `manifest.py` hashes raw bytes. The ticket files in this worktree have LF endings and git warns
   that it will write CRLF the next time it touches them. Run `verify` on this worktree as it stands (as at CP2); a
   fresh checkout with a different line-ending setting would not verify.

## 8. Open items and next steps

* W3-START-O1: Gaussian rows with a population leakage level and an explicit exponent (small follow-up to L9.5).
* W3-START-O2: no Gram floor at all (needs a rank-sensitive aggregation; low priority).
* W3-START-O3: growing s₀.
* A fixed-constant, probability → 1 bound when C_L = 0 (needs concentration across columns).
* UNI-0 and exact-separation AR(1) as verified examples.
* Recommended next: decide 7.2; then, if wanted, the repeat better-theorem review on v1.3.3 for the headline gate.
* What this ticket does not solve: the start on strong-factor designs at p > K. That needs a different mechanism, not
  a sharper analysis of this one.

## 9. Record

* **Agents in leg C:** lead (Claude Fable 5.2, Claude Work, high); SC4, LC2-A, LC2-B, R1-sol (Codex gpt-6.1-sol, high);
  BR1, SW1 (Codex gpt-6-astra, high); R1-opus (Claude Opus 5.5, Claude Work, high). The lead's run was interrupted
  twice by account or provider incidents and resumed from the files on disk; no review had to be repeated.
  Claude tally for the whole ticket: CP 1 / CW 2. No NOTS use.
* **Holds:** `HOLDS.md` (main checkout) read before each step: no holds.
* **Files** (all in `Theory_work/Wave3/W3-START/`, uncommitted since b469719; HQ commits):
  * modified: `STATEMENT.md` (v1.3.3), `PLAN.md`, `ASSUMPTION_MAP.md`, `LOG.md`, `numerics/RESULTS.md`,
    `numerics/run_start.R` (one comment), `numerics/lemmas/RESULTS_LEMMAS.md`, and `lemmas/L1_AGG_FLOOR.md` …
    `lemmas/L5_ASM_STARTF.md` (their status line only)
  * new: `REPORT.md`, `citecheck.py`, `lemmas/L6_COROLLARIES.md` … `lemmas/L11_EXAMPLES.md`,
    `numerics/lemmas/falsify_L6_L11.R`, `numerics/lemmas/out_L6_L11.txt`
  * new in `reviews/`: 7 briefs, 4 manifests (SC4, LC2, SW1, R1), 7 reviews, 4 dispositions, `CITECHECK.txt`
  * new: `CHECKPOINT_3.md`

## 10. Registry blocks (for `ingest.py`; statuses as proposed for after HQ's acceptance audit)


```
REGISTRY
claim: W3-START:AGG | kind: lemma | statement: STATEMENT.md:196-210 | premises: none (deterministic)
name: Lemma AGG (table identities of the coded start)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:28
assumptions: A:EX-A ; A:BLOCK-LE-16
conclusion: identity: two-sided bounds of the start odds by the table functionals T1, U, Xi; lattice bound; one-step table ratio at least (n+1)^{-1/2} | scope: every valid data set, n at least 4, any partition with blocks of size at most min(16, K), any reference model
depends_on: —
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:FLOOR | kind: theorem | statement: STATEMENT.md:240-242 | premises: none (deterministic)
name: Theorem FLOOR (deterministic floor n^{-1/2})
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:29
assumptions: A:EX-A ; A:BLOCK-LE-16
conclusion: negative: 1 - pi0(S) is at least (1/3)(n+1)^{-1/2} for every unsaturated model on every data set; with a null column the start odds are at least T1 and T1 is at least (1/2)(n+1)^{-1/2} | rate: n^{-1/2} cannot be improved | scope: every valid data set, n at least 4
depends_on: W3-START:AGG@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:TK | kind: lemma | statement: STATEMENT.md:232 | premises: STATEMENT.md:134-138
name: Lemma TK (toolkit under the unnormalised Gram floor)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:30
assumptions: A:START-E (new | Energy bound and polynomial dimension | squared norm of mu at most Mn, p at most n^A with A positive, s0 fixed, p greater than s0 for all large n | STATEMENT.md:134 | shared no | bridge W3-START:TK) ; A:START-GF (new | Constant unnormalised Gram floor on sets of size at most 16 | smallest eigenvalue of X_T'X_T at least g_* for every set T of size 1 to 16 | STATEMENT.md:135 | shared no | bridge W3-START:TK) ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: toolkit event of probability at least 1 - 2exp(-n^{1/3}) - 2/n on which RSS_U = (n-1) tau_U^2 (1 + O(n^{-1/3})) and every block-table score has an expansion with a bounded remainder kappa_E(g_*, M, sigma^2) | scope: fixed design, s0 at least 0, uniform over the class
depends_on: —
implies: —
sharpness: A:START-GF = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100) ; A:START-E = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:LEAK | kind: lemma | statement: STATEMENT.md:233 | premises: STATEMENT.md:134-138 ; STATEMENT.md:151-156
name: Bridge (B-L): leakage bridge with column levels, Lemma J
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:31
assumptions: A:START-E ; A:START-GF ; A:START-AL (new | Averaged leakage with a level vector | there is a level vector h for Q with tail budget b_n(h) tending to 0 and rho_n(Q; h) tending to 0 | STATEMENT.md:151 | shared no | bridge W3-START:LEAK) ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: U_Q = O_P(n^{-1/2} L^b_n(Q; h)) and T1 = O_P(n^{-1/2} L^{b,0}_n(h)), with explicit Markov bounds; small gains follow from the averaged condition | scope: fixed design, any partition with blocks of size at most 16, uniform
depends_on: W3-START:TK@proof
implies: —
sharpness: A:START-AL = NECESSARY-FOR-ROUTE (evidence: ASSUMPTION_MAP.md:72)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:VIS-c | kind: lemma | statement: STATEMENT.md:234 | premises: STATEMENT.md:134-150 ; STATEMENT.md:151-156
name: Bridge (B-V1): constant-level visibility
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:32
assumptions: A:START-E ; A:START-GF ; A:START-V (new | Visibility of the truths | constant level (V-c) with c_V greater than 1 + 2A, or the margin form (V-m) with constants c_m and eps_0 | STATEMENT.md:139 | shared no | bridge W3-START:VIS-m) ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: P(Xi(Q) greater than n^{-kappa}) tends to 0 for every kappa below (c_V - 1 - 2A)/2 | scope: fixed design, uniform
depends_on: W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:AGG@proof
implies: —
sharpness: A:START-V = WEAKENABLE (evidence: lemmas/L11_EXAMPLES.md:41)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:VIS-m | kind: lemma | statement: STATEMENT.md:235 | premises: STATEMENT.md:134-150
name: Bridge (B-V2): margin visibility
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:33
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: P(Xi(Q) greater than n^{-kappa}) tends to 0 for every kappa below c_m/2 | scope: fixed design, uniform
depends_on: W3-START:TK@proof
implies: —
sharpness: A:START-V = NECESSARY (evidence: lemmas/L7_NEC.md:28)
binding: A:START-V forced by W3-START:AGG via the deterministic lower bound of the start odds by c_s times Xi
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:ASM | kind: lemma | statement: STATEMENT.md:212-218 | premises: STATEMENT.md:173-190
name: Lemma ASM (assembly)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:34
assumptions: A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1 - pi0(L(Q)) = O_P((size of Q + 1) n^{-1/2} L^b_n(Q; h)) + O_P(n^{-kappa}); at Q = S0 the odds bound and the first-order form o0/T1 tends to 1 | scope: fixed design, given the interface properties
depends_on: W3-START:AGG@proof ; W3-START:FLOOR@proof ; W3-START:TK@stmt ; W3-START:LEAK@stmt ; W3-START:VIS-c@stmt ; W3-START:VIS-m@stmt
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:START-F | kind: theorem | statement: STATEMENT.md:244-263 | premises: STATEMENT.md:134-156
name: Theorem START-F (fixed design, uniform form)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:35
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: start odds against S0 are O_P(n^{-1/2} L^0_n(h) + n^{-1} L_n(S0; h)^2) + o_P(n^{-kappa}); lattice mass outside {S0 subset T subset Q} is O_P(rho_n(Q; h)) + o_P(n^{-kappa}); o0/T1 tends to 1 when kappa_V exceeds 1/2; uniform finite-n form with exceptional probability eps + b_n(h) | rate: n^{-1/2} times the leakage functional | scope: fixed design, p at most n^A (p much larger than n allowed), s0 fixed, partition-free hypotheses
depends_on: W3-START:AGG@proof ; W3-START:FLOOR@proof ; W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:VIS-c@proof ; W3-START:VIS-m@proof ; W3-START:ASM@proof
implies: —
sharpness: A:START-AL = NECESSARY-FOR-ROUTE (evidence: ASSUMPTION_MAP.md:72) ; A:START-V = NECESSARY (evidence: lemmas/L7_NEC.md:28) ; A:START-GF = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100) ; A:START-E = NECESSARY-FOR-ROUTE (evidence: lemmas/L2_TK.md:100)
binding: A:START-V forced by W3-START:NEC-b via one truth below the level 1 + 2A sends pi0(S0) to 0
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:P1(reviews/BT1_better_theorem_astra.md) ; better-disposition:P1=adopted(reviews/BT1_disposition.md) ; better-proposal:P2(reviews/BT1_better_theorem_astra.md) ; better-disposition:P2=adopted(reviews/BT1_disposition.md) ; better-proposal:P3(reviews/BT1_better_theorem_astra.md) ; better-disposition:P3=adopted(reviews/BT1_disposition.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:F1 | kind: corollary | statement: STATEMENT.md:267-270 | premises: STATEMENT.md:134-156
name: Corollary F1 (uniform leakage)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:36
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under uniform gains at most eta tau^2 log n with eta below eta_A, 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-kappa} + n^{-kappa} with probability tending to 1, for kappa below min(kappa_L, kappa_V) | rate: n^{-kappa_L(eta, A)} | scope: fixed design
depends_on: W3-START:START-F@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:F2 | kind: corollary | statement: STATEMENT.md:271-274 | premises: STATEMENT.md:134-156
name: Corollary F2 (strong signals, exact order n^{-1/2})
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:37
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under strong signals and gains at most eta' Delta_U log n given truth subsets, o0 = O_P(n^{-(1-eta')/2}) + o_P(n^{-kappa}); exact order n^{-1/2} when eta' = 0 and kappa_V exceeds 1/2 | rate: n^{-(1-eta')/2} | scope: fixed design, Q = S0
depends_on: W3-START:START-F@proof ; W3-START:FLOOR@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:F3 | kind: corollary | statement: STATEMENT.md:275-276 | premises: STATEMENT.md:134-156
name: Corollary F3 (bounded gains)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:38
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under gains bounded by C0 tau^2, 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-1/2} exp(C2 sqrt(log n)) + n^{-kappa} with probability tending to 1 | rate: n^{-1/2} exp(C2 sqrt(log n)) | scope: fixed design
depends_on: W3-START:START-F@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:F4 | kind: corollary | statement: STATEMENT.md:277-286 | premises: STATEMENT.md:134-156
name: Corollary F4 (isolated leaking columns)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:39
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: a bounded number of columns may leak at any constant level below 1 + 2 liminf(log p/log n): with reduced levels on those columns the averaged leakage condition holds and START-F applies | scope: fixed design, asymptotic (the tail budget of the reduced levels is below 1 only for log n above 256)
depends_on: W3-START:START-F@proof ; W3-START:LEAK@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:NEC-b | kind: lemma | statement: STATEMENT.md:220-225 | premises: STATEMENT.md:134-138
name: Lemma NEC-b (component diagnostics on the actual partition)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:40
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: negative: on the actual partition, one null with gain at least c tau^2 log n given the truths of its block, c above 1 + 2 limsup(log p/log n), or one truth with gain at most c tau^2 log n given the other truths of its block, c below 1 + 2 liminf(log p/log n), gives pi0(S0) at most n^{-kappa'} with probability tending to 1 | scope: fixed design
depends_on: W3-START:TK@proof ; W3-START:AGG@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:NEC | kind: proposition | statement: STATEMENT.md:315-330 | premises: STATEMENT.md:134-138
name: Proposition NEC (limits)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:41
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: negative: the exponent 1/2 is optimal; partition-free forms of the one-column limits: the leaking-null form is vacuous for s0 at most 15 and has content for s0 at least 16; the weak-truth form shows that the visibility constant 1 + 2A cannot be lowered | scope: fixed design
depends_on: W3-START:NEC-b@proof ; W3-START:FLOOR@proof ; W3-START:F2@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:TRANSFER | kind: theorem | statement: STATEMENT.md:289-304 | premises: STATEMENT.md:134-156
name: Theorem START-R(a) (random-design transfer)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:42
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: for any design law with Gaussian noise given the design and coefficients, support, leakage set and levels measurable in the design, the fixed-design bounds hold under the joint law on design sets of probability tending to 1 | scope: random design; response-selected targets not covered
depends_on: W3-START:START-F@proof ; W3-START:F1@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:BR | kind: lemma | statement: STATEMENT.md:236 | premises: STATEMENT.md:159-166
name: Bridge (B-R): Gaussian-row bridge
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:43
assumptions: A:START-R-FL (new | Population floor on sets of size at most 16 + s0 | smallest eigenvalue of every principal submatrix of Sigma_n of size at most 16 + s0 is at least c_Sigma | STATEMENT.md:159 | shared no | bridge W3-START:BR) ; A:START-R-V (new | Population visibility PTV(a_V) | conditional covariance of each truth with the signal given any 15 other columns is at least a_V in absolute value | STATEMENT.md:161 | shared no | bridge W3-START:BR) ; A:START-R-L (new | Localised bounded population leakage | leakage set Q and neighbourhoods H_l of polylogarithmic size with conditional covariances at most C_L n^{-1/2} with the truths and at most r_n with remote columns | STATEMENT.md:162 | shared no | bridge W3-START:BR)
conclusion: target: with probability tending to 1 the Gaussian-row design satisfies the energy bound, the normalised floor on sets of size at most 16, visibility at every fixed level and L_n(Q) at most exp(C sqrt(log n)); with exactly zero population leakage L_n(Q) = O_P((log n)^{15 kappa_Q + 1/2}) (tightness) | scope: Gaussian rows, p at most n^A, p greater than s0, p much larger than n allowed
depends_on: W3-START:LEAK@proof
implies: —
sharpness: A:START-R-L = NECESSARY-FOR-ROUTE (evidence: lemmas/L9_BR.md:175)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:START-R | kind: theorem | statement: STATEMENT.md:305-313 | premises: STATEMENT.md:159-166
name: Theorem START-R(b) (Gaussian rows)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:44
assumptions: A:START-R-FL ; A:START-R-V ; A:START-R-L ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-1/2} exp(C_R sqrt(log n)) with probability tending to 1; with Q = S0, pi0(S0) is at least 1 - n^{-c} for every c below 1/2; with zero population leakage the rate is O_P((size of Q + 1) n^{-1/2} (log n)^{15 kappa_Q + 1/2}) | rate: n^{-1/2} exp(C_R sqrt(log n)) | scope: Gaussian rows, p at most n^A, p greater than s0, p much larger than n allowed, s0 fixed
depends_on: W3-START:BR@proof ; W3-START:TRANSFER@proof ; W3-START:START-F@proof ; W3-START:F1@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:IF-START | kind: corollary | statement: STATEMENT.md:333-337 | premises: STATEMENT.md:134-156
name: Corollary IF-START (P-START with a rate)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:45
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1_A o0 = O_P(r_n) with a deterministic rate r_n tending to 0, under START-F at Q = S0 or under START-R at Q = S0; this is the premise P-START of W3-SAMP with a rate | rate: r_n | scope: start interface only; P-CONC, P-MAP and the algorithm premises of W3-SAMP are not supplied
depends_on: W3-START:START-F@proof ; W3-START:START-R@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:OVL | kind: proposition | statement: STATEMENT.md:338-343 | premises: STATEMENT.md:134-156
name: Proposition OVL (start mass under a bounded leakage set)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:46
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: with a leakage set of bounded excess size and leak levels bounded uniformly, pi0(S0) is at least n^{-E_n - eps} with probability tending to 1; hence the production form of P-OVL when limsup(E_n - max(1, log p/log n)) is negative | scope: fixed design, constant-level visibility (V-c)
depends_on: W3-START:AGG@proof ; W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:VIS-c@proof
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:MIS | kind: corollary | statement: STATEMENT.md:345-356 | premises: STATEMENT.md:134-156
name: Corollary MIS (misspecified candidate set)
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:47
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under a Gaussian-residual omitted part the candidate data follow the model with truth supp(beta^C) and noise variance sigma^2 + tau^2, so every claim holds for the start of the method re-run on the candidate data provided its hypotheses hold after the substitution | scope: fixed candidate design; random candidate design through the transfer
depends_on: W3-START:START-F@stmt ; W3-START:TRANSFER@proof ; W3-START:NEC@stmt ; W3-START:IF-START@stmt ; W3-START:OVL@stmt
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```

```
REGISTRY
claim: W3-START:EX | kind: proposition | statement: STATEMENT.md:358-370 | premises: STATEMENT.md:134-166
name: Examples: five families verify the hypotheses
status: PROVED-CHECKED | status_source: CHECKPOINT_3.md:48
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:START-R-FL ; A:START-R-V ; A:START-R-L
conclusion: target: five example families satisfy the partition-free hypotheses: orthogonal designs; near-duplicate null columns; one truth with fifteen correlated nulls (margin visibility holds, constant-level visibility fails, default-level leakage condition fails and F4 applies); Gaussian rows with independent columns; block-diagonal covariance with one truth per group | scope: fixed-design examples have p at most n - 1; UNI-0 and exact-separation AR(1) are not verified and not claimed
depends_on: W3-START:START-F@stmt ; W3-START:F1@stmt ; W3-START:F2@stmt ; W3-START:F4@stmt ; W3-START:START-R@stmt
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md)
council: R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (better-theorem review not repeated on v1.3.3; lit gate open)
```
