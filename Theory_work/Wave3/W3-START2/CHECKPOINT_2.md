# W3-START2 — CHECKPOINT 2 (final) — 2026-11-12

Lead: Claude Fable 5.2, effort high. No git state changed by the lead. Outcome: **council passed in round R1** (the
CP3-PASS form of PROTOCOL rule 10). HQ's acceptance audit and the acceptance of the base ticket are still to come.

## 0. Summary (the lead's final message)

**All four BT2 improvements are proved and council-passed; none was dropped.** Statement `STATEMENT.md` v1.4.1, proofs `lemmas/P1`–`P4`.

* P1: for s₀ ≥ 1 the leading functional loses its 15√(2/π)z_n/p term; F2 needs no growth condition on p.
* P2: OVL under (V-m) or (V-c).
* P3: leaking-null limit with 17 − s₀ nulls for 1 ≤ s₀ ≤ 15, with an example for each s₀.
* P4: (T3)(b) for any |Q| ≤ K.

| round | seat | result |
|---|---|---|
| LC1-A, LC1-B | Sol | all four proof files VERIFIED, no findings |
| R1 | Sol | 9.1, gates PASS |
| R1 | Opus 5.5 | 9.1, gates PASS |

`manifest.py bind` OK and `verify` OK on MANIFEST_R1 (29e07311…). Citecheck: 216 citations, 0 missing. Numerics: 0 violations. Kill budget unused. No holds.

Nine non-blocking council remarks (wording and citations) are listed as errata in §3; none was applied, because the content is frozen.

**For HQ:** registry blocks for nine claims are in §6. Eight supersede W3-START claims by implication. Acceptance must wait until W3-START itself is accepted.

## 1. Status per claim (one line per claim; the registry blocks of §6 cite these lines)

Statuses are **proposed**, for after HQ's acceptance audit and after the acceptance of the base ticket W3-START
(every claim below uses base claims by statement or by proof step). Until then each claim is: council-passed in R1,
acceptance pending. Evidence for every line: `reviews/R1_council_sol.md`, `reviews/R1_council_opus.md` (both: accepted, all
six gates PASS), `reviews/LC1_A_line_check.md`, `reviews/LC1_B_line_check.md`.

* **W3-START2:LEAK-0** — PROVED-CHECKED (proposed). New lemma; for s0 at least 1 the single-null term T1 is O_P(n^{-1/2} L^sharp_n(h)), uniformly. Proof: `lemmas/P1_LEADING.md` P1.1–P1.3.
* **W3-START2:START-F** — PROVED-CHECKED (proposed). Replaces W3-START:START-F; the leading functional conditions on proper subsets of the truth only. Proof: `lemmas/P1_LEADING.md` P1.4–P1.5.
* **W3-START2:F2** — PROVED-CHECKED (proposed). Replaces W3-START:F2; the hypothesis p/sqrt(log n) tending to infinity is removed. Proof: `lemmas/P1_LEADING.md` P1.6.
* **W3-START2:TRANSFER** — PROVED-CHECKED (proposed). Replaces W3-START:TRANSFER; the rate envelope is asked of the sharp functional. Proof: `lemmas/P1_LEADING.md` P1.7.
* **W3-START2:IF-START** — PROVED-CHECKED (proposed). Replaces W3-START:IF-START; the deterministic rate r_n uses the sharp functional. Proof: `lemmas/P1_LEADING.md` P1.8.
* **W3-START2:OVL** — PROVED-CHECKED (proposed). Replaces W3-START:OVL; holds under (V-m) for the same Q as well as under (V-c). Proof: `lemmas/P2_OVL.md`.
* **W3-START2:NEC** — PROVED-CHECKED (proposed). Replaces W3-START:NEC; clause (N2) asks 17 - s0 leaking nulls on proper subsets of the truth when s0 is at most 15. Proof: `lemmas/P3_NEC.md`.
* **W3-START2:BR** — PROVED-CHECKED (proposed). Replaces W3-START:BR; holds under (L-R+), which drops the polylogarithmic bound on the size of Q. Proof: `lemmas/P4_BR.md` P4.1.
* **W3-START2:START-R** — PROVED-CHECKED (proposed). Replaces W3-START:START-R; no size condition on Q beyond size at most K. Proof: `lemmas/P4_BR.md` P4.2–P4.3.

Unchanged base claims (AGG, ASM, NEC-b, FLOOR, TK, LEAK, VIS-c, VIS-m, F1, F3, F4, MIS, EX) are not claims of this
ticket and get no row here.

## 2. Review trail (whole ticket)

| round | seat (model, provider) | manifest | verdict | files |
|---|---|---|---|---|
| SL1 | Sol (gpt-6.1-sol, Codex), blind | b86651a9… | LOCK WITH CHANGES: 4 MINOR, 2 optional; all applied → v1.4.1 | `reviews/SL1_statement_lock_sol.md`, `reviews/SL1_disposition.md` |
| SC1 | Sol, diff check | d09644f5… | LOCKED: editorial only, all six items resolved | `reviews/SC1_diff_check_sol.md` |
| LC1-A | Sol, blind line check of P1, P3 | ffeba7a5… | VERIFIED, VERIFIED; no findings | `reviews/LC1_A_line_check.md` |
| LC1-B | Sol, blind line check of P2, P4 | ffeba7a5… | VERIFIED, VERIFIED; no findings | `reviews/LC1_B_line_check.md`, `reviews/LC1_disposition.md` |
| R1 | Sol, council, blind | 29e07311… | 9.1, six gates PASS; 2 NON-BLOCKING remarks | `reviews/R1_council_sol.md` |
| R1 | Opus (Claude Opus 5.5, Claude Personal, effort high), council, blind | 29e07311… | 9.1, six gates PASS; 7 NON-BLOCKING remarks | `reviews/R1_council_opus.md`, `reviews/R1_disposition.md` |

Between LC1 and R1 the statement and the four proof files did not change; the only difference of the R1 manifest is
the added `REPORT.md`, which the council read. One round was enough, so no reconciliation round was needed. No review
layer of the ticket brief was skipped. The sharpness gate of PROTOCOL item 3 (assumption map, boundary numerics, a
fresh better-theorem review) was not part of this ticket's brief: the ticket implements the proposals of the base
ticket's better-theorem review BT2, and no better-theorem review was run on v1.4 itself (hence "headline-strength
pending" in §6).

## 3. Council R1: remarks not applied (errata for a later version)

All nine remarks are NON-BLOCKING and concern wording or citations. The frozen content was not edited (an edit would
need a new round, PROTOCOL rule 15). The lead agrees with each of them.

| # | seat | where | remark | repair for the next version |
|---|---|---|---|---|
| E1 | Sol 1 | `REPORT.md:23` | "for bounded p > s₀ the order n^{−1/2} is exact" omits the conditions η′ = 0 and κ_V > ½ of F2⁺ | add them; `STATEMENT.md:115-117` is correct |
| E2 | Sol 2, Opus 7 | `REPORT.md:89` | the sharpness row is right for the leading term; exact order of o₀ needs the remainder conditions of F2⁺(v) | say so in the row |
| E3 | Opus 1 | `lemmas/P1_LEADING.md:16-17` | "BASE" is written twice | delete one |
| E4 | Opus 2 | `STATEMENT.md:108` | "word for word" for clause (c): the base clause also has a gloss that is not reproduced | "the same statement" |
| E5 | Opus 3 | `STATEMENT.md:205-206` | cites BASE `CHECKPOINT_3.md:241`, a file outside the frozen content | mark it "for HQ" or cite a listed input |
| E6 | Opus 4 | `REPORT.md:27-28` | "gain more than (1 + 2Ā)τ²_V log n" is looser than "at least c·τ²_V·log n for a fixed c > 1 + 2Ā" | use the statement's wording |
| E7 | Opus 5 | `STATEMENT.md:82`, `lemmas/P1_LEADING.md:38` | LEAK-0 is a fixed-n lemma but lists (E), which has asymptotic clauses; the proof uses only the inequalities of (E) at n | "the inequalities of (E) at n" |
| E8 | Opus 6 | `STATEMENT.md:206-208`, `REPORT.md:73-74` | the consumed list names seven base claims and "the proof files"; the registry edges should name the reused proof steps | done in §6 (`depends_on` with `@proof:` facts) |

E4, E5 and E7 touch `STATEMENT.md`; they change no hypothesis and no conclusion. They should be applied together with
the next statement version (one Sol diff check), not now.

## 4. Kill budget and protocol notes

* Kill budget (HQ, CP1 decision): one repair per changed step found broken by a line check. Not used: both line
  checks returned no finding. No P-item was dropped to an open item.
* Council: passed in round 1 of at most 3.
* Providers: the lead ran on Claude Work (first run) and on Claude Personal (after the limit); the Opus council seat
  ran on Claude Personal at effort high (owner's override of 2026-11-12, HQ message); all Sol seats on Codex at
  reasoningEffort high. No agent above effort high. Claude tally: CP 2 / CW 1.
* One slip, corrected at once: a crashed first run of `numerics/falsify_P.R` wrote an empty `out_P.txt` into the base
  folder `W3-START/numerics/`; it was deleted and the base folder is unchanged (LOG, 09:30 entry).
* Deviation from the wording of the go message: the registry blocks are in this file, not in `REPORT.md`, because each
  block carries the council line and the report is part of the frozen council content (same convention as the base
  ticket).

## 5. For HQ's acceptance audit

* `python Theory_work/Wave3/tools/manifest.py bind Theory_work/Wave3/W3-START2/reviews/MANIFEST_R1.txt <both R1 reviews>`:
  `bind: OK`; council cell: `R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)`.
* `manifest.py verify` on MANIFEST_R1: OK on the current tree (nothing in the frozen content was edited after the round).
* Citecheck: `python Theory_work/Wave3/W3-START2/citecheck.py` → 216 citations, 0 MISSING/OUT-OF-RANGE
  (`reviews/CITECHECK.txt`).
* Numerics: `numerics/falsify_P.R` → `numerics/out_P.txt`, 0 violations.
* **Order of acceptance.** Every claim below depends on W3-START claims that are council-passed but not yet registry
  rows on `main`. Ingest W3-START first; then these blocks. The eight `implies:` relations to W3-START claims are the
  supersession-by-implication edges (LIFECYCLE §5); whether and when the base claims are marked SUPERSEDED-VALID is
  HQ's step.
* New assumption id: A:START2-R-L (declared in the BR block). All other ids are those of the base ticket.
* Interface properties delivered, as in the base ticket (not written as `implies:` items, which take claim ids
  only): IF-START ⇒ A:P-START with a deterministic rate; OVL ⇒ A:P-OVL in its production form.
* **Staged test by the lead** (disposable copy made by `bvsreg.make_stage`, deleted afterwards; the live registry
  was not touched): `ingest.py claims` on BASE `CHECKPOINT_3.md` — 21 claims, 0 problems; then on this file —
  9 claims, 0 problems; `check.py` on that copy: 436 claims, 0 ERROR. `check.py --acceptance` was not run (HQ's step).
* The `depends_on` edges name the base proof step that is reused (council remark E8), as one token without spaces
  (the ingest grammar): L3.3 = step bound with the small-gain remark and the tail budget; L5.2 = Proposition L5.2
  (and L5.3); L6.0 = Lemma L6.0 and Corollary L6.0′; L6.2 = steps (i)–(iii) of F2; L8.2 = L8.1–L8.3; CH = the path
  bound (P3) and the chain bound (CH); L10.1, L10.2 = the interface proofs (L10.2: steps (iii)–(iv)); L7.3 = (N1),
  (N3), (N4); L9.1-L9.6 = the bridge steps; L9.7 = the design set of the base proof.
* Open items (REPORT §7): W3-START2-O1 (fewer than 17 − s₀ leaking nulls), O2 (informative bound beyond
  |Q| ≈ n^{1/2}; reference sets beyond polylogarithmic size), O3 (s₀ = 0 functional; fixed constant in (T1⁺)(d)).
  The base open items W3-START-O4…O7 (BT2-P1…P4) are closed by this ticket.

## 6. Registry blocks (for `ingest.py`; statuses as proposed for after HQ's acceptance audit; spans of STATEMENT v1.4.1)

```
REGISTRY
claim: W3-START2:LEAK-0 | kind: lemma | statement: STATEMENT.md:82-89 | premises: STATEMENT.md:38-39
name: Lemma LEAK-0 (leading term of the start odds, sharp functional)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:34
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: for s0 at least 1, P(T1 > 5 lambda (s0+1) n^{-1/2} L^sharp_n(h)) is at most P(toolkit event fails) + b_n(h) + 451 e^{2 kappa_E + 1}/lambda on the stated range of lambda; hence T1 = O_P(n^{-1/2} L^sharp_n(h)) | rate: n^{-1/2} times the sharp leading functional | scope: fixed design, p at most n^A, s0 at least 1 and below K, uniform in the design, the coefficients and the level vector
depends_on: W3-START:TK@proof ; W3-START:LEAK@proof:L3.3
implies: —
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:START-F | kind: theorem | statement: STATEMENT.md:93-110 | premises: STATEMENT.md:38-39
name: Theorem START-F (fixed design, uniform form, sharp leading functional)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:35
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: start odds against S0 are O_P(n^{-1/2} L^sharp_n(h) + n^{-1} L_n(S0; h)^2) + o_P(n^{-kappa}); lattice mass outside {S0 subset T subset Q} is O_P(rho_n(Q; h)) + o_P(n^{-kappa}); o0/T1 tends to 1 when kappa_V exceeds 1/2; uniform finite-n form with exceptional probability eps + b_n(h) | rate: n^{-1/2} times the sharp leading functional | scope: fixed design, p at most n^A (p much larger than n allowed), s0 fixed, partition-free hypotheses
depends_on: W3-START2:LEAK-0@proof ; W3-START:START-F@proof:L5.2 ; W3-START:F1@proof:L6.0 ; W3-START:AGG@proof ; W3-START:TK@proof ; W3-START:LEAK@proof ; W3-START:VIS-c@proof ; W3-START:VIS-m@proof ; W3-START:ASM@proof
implies: W3-START:START-F (L^sharp_n(h) is at most L^0_n(h); clauses (a) and (c) are identical)
sharpness: A:START-V = NECESSARY (evidence: Theory_work/Wave3/W3-START/lemmas/L7_NEC.md:28)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:F2 | kind: corollary | statement: STATEMENT.md:112-117 | premises: STATEMENT.md:38-39
name: Corollary F2 (strong signals; no growth condition on p)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:36
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: o0 = O_P(n^{-(1-eta')/2}) + o_P(n^{-kappa}) for every kappa below kappa_V; if eta' = 0 and kappa_V exceeds 1/2, o0 is of exact order n^{-1/2} | rate: n^{-(1-eta')/2} | scope: fixed design, s0 at least 1, p greater than s0, bounded p allowed
depends_on: W3-START2:START-F@proof ; W3-START:F2@proof:L6.2 ; W3-START:FLOOR@proof
implies: W3-START:F2 (same conclusion, one hypothesis fewer)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:TRANSFER | kind: theorem | statement: STATEMENT.md:120-133 | premises: STATEMENT.md:38-39
name: Theorem START-R(a) (transfer to random designs, sharp leading functional)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:37
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: under any design law with design-measurable coefficients, support, leakage set and levels, 1 - pi0(L(Q)) = O_P(rhobar_n) + o_P(n^{-kappa}); with Q = S0 and n^{-1/2} L^sharp_n(h) + n^{-1} L_n(S0; h)^2 at most rbar_n on the design sets, o0 = O_P(rbar_n) + o_P(n^{-kappa}) | rate: rhobar_n, rbar_n | scope: Gaussian noise given the design; response-selected targets not covered
depends_on: W3-START2:START-F@proof ; W3-START:TRANSFER@proof:L8.2
implies: W3-START:TRANSFER (a bound for the 1.3.4 rate is a bound for the 1.4 rate)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:IF-START | kind: corollary | statement: STATEMENT.md:176-180 | premises: STATEMENT.md:38-39
name: Corollary IF-START (start interface with the sharp rate)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:38
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1_A o0 = O_P(r_n) with r_n = n^{-1/2} L^sharp_n(h) + n^{-1} L_n(S0; h)^2 + n^{-kappa} tending to 0 (fixed design), or r_n = n^{-1/2} exp(C_R sqrt(log n)) (Gaussian rows, Q = S0); hence P-START with a rate | rate: r_n | scope: only the start interface is supplied
depends_on: W3-START2:START-F@proof ; W3-START2:START-R@proof ; W3-START:IF-START@proof:L10.1
implies: W3-START:IF-START (the new rate is at most the old one)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P1(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P1=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:OVL | kind: proposition | statement: STATEMENT.md:181-189 | premises: STATEMENT.md:38-39
name: Proposition OVL (start mass under a bounded leakage set, either visibility condition)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:39
assumptions: A:START-E ; A:START-GF ; A:START-V ; A:START-AL ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: P(pi0(S0) is at least n^{-E_n - eps}) tends to 1 for every eps > 0, E_n the sum over Q minus S0 of the positive parts of (a_{n,l} - 1)/2 - log p/log n; hence P-OVL in its production form when limsup(E_n - max(1, log p/log n)) is negative | rate: n^{-E_n - eps} | scope: fixed design, bounded number of extra columns in Q with uniformly bounded gain levels
depends_on: W3-START2:START-F@proof ; W3-START:AGG@proof:CH ; W3-START:TK@proof ; W3-START:OVL@proof:L10.2
implies: W3-START:OVL ((V-c) is one of the two admitted visibility conditions)
sharpness: A:START-V = NECESSARY-FOR-ROUTE (evidence: lemmas/P2_OVL.md:66)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P2(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P2=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:NEC | kind: proposition | statement: STATEMENT.md:154-173 | premises: STATEMENT.md:38-39
name: Proposition NEC (limits; partition-free leaking-null limit for every s0 at least 1)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:40
assumptions: A:START-E ; A:START-GF ; A:EX-A ; A:BLOCK-LE-16
conclusion: negative: if max(1, 17 - s0) designated nulls each have gain at least c tau_V^2 log n on every proper subset V of the truth of size at most 15, with fixed c > 1 + 2 Abar, then pi0(S0) is at most n^{-kappa'} with probability tending to 1 for every kappa' below (c - 1 - 2 Abar)/2; (N1), (N3), (N4) as in the base ticket | rate: n^{-kappa'} | scope: fixed design, s0 at least 1; non-vacuous for every s0 from 1 to 15 (example given); fewer than 17 - s0 nulls not claimed
depends_on: W3-START:NEC-b@stmt ; W3-START:NEC@proof:L7.3 ; W3-START:FLOOR@proof ; W3-START2:F2@proof
implies: W3-START:NEC ((N2) is identical for s0 at least 16 and its premise is empty for s0 at most 15; (N1), (N3), (N4) identical)
sharpness: A:BLOCK-LE-16 = NECESSARY-FOR-ROUTE (evidence: lemmas/P3_NEC.md:67)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P3(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P3=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:BR | kind: lemma | statement: STATEMENT.md:147-152 | premises: STATEMENT.md:63-73
name: Bridge B-R (Gaussian rows; leakage set of any size at most K)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:41
assumptions: A:START-R-FL ; A:START-R-V ; A:START2-R-L (new | Localised bounded leakage with a leakage set of any size at most K | as (L-R) of the base ticket [A:START-R-L] without the requirement that the size of Q is at most (log n)^{kappa_Q}; the reference sets H_l stay of size at most (log n)^{kappa_Q} | STATEMENT.md:63-73 | shared no | bridge W3-START2:BR)
conclusion: target: with probability tending to 1 a Gaussian-row design satisfies the energy bound, the normalised floor on sets of size at most 16 (hence the Gram floor), constant-level visibility for every fixed level, and L_n(Q) at most exp(C_B sqrt(log n)); with zero population leakage L_n(Q) = O_P((log n)^{15 kappa_Q + 1/2}) (tightness only) | rate: exp(C_B sqrt(log n)) | scope: Gaussian rows, p at most n^A, p greater than s0, any deterministic Q containing S0 with size at most K
depends_on: W3-START:BR@proof:L9.1-L9.6 ; W3-START:LEAK@proof
implies: W3-START:BR ((L-R) implies (L-R+))
sharpness: A:START2-R-L = NECESSARY-FOR-ROUTE (evidence: lemmas/P4_BR.md:27)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P4(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P4=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```

```
REGISTRY
claim: W3-START2:START-R | kind: theorem | statement: STATEMENT.md:134-145 | premises: STATEMENT.md:63-73
name: Theorem START-R(b) (Gaussian rows; leakage set of any size at most K)
status: PROVED-CHECKED | status_source: CHECKPOINT_2.md:42
assumptions: A:START-R-FL ; A:START-R-V ; A:START2-R-L ; A:EX-A ; A:BLOCK-LE-16
conclusion: target: 1 - pi0(L(Q)) is at most (size of Q + 1) n^{-1/2} exp(C_R sqrt(log n)) with probability tending to 1; with Q = S0, pi0(S0) is at least 1 - n^{-c} for every c below 1/2; with size of Q at most n^{1/2 - eps_Q}, pi0(L(Q)) is at least 1 - n^{-c} for every c below eps_Q; with zero population leakage the rate is O_P((size of Q + 1) n^{-1/2} (log n)^{15 kappa_Q + 1/2}) | rate: (size of Q + 1) n^{-1/2} exp(C_R sqrt(log n)) | scope: Gaussian rows, p at most n^A, p greater than s0, p much larger than n allowed, s0 fixed; the display is trivial where its right side is at least 1
depends_on: W3-START2:BR@proof ; W3-START:TRANSFER@proof:L8.2 ; W3-START:START-F@proof:L5.2(i) ; W3-START:F1@proof:L6.0 ; W3-START:START-R@proof:L9.7
implies: W3-START:START-R ((L-R) implies (L-R+); same conclusions)
sharpness: A:START2-R-L = NECESSARY-FOR-ROUTE (evidence: lemmas/P4_BR.md:101)
gates: correct:PASS(reviews/R1_council_sol.md, reviews/R1_council_opus.md) ; better-proposal:BT2-P4(Theory_work/Wave3/W3-START/reviews/BT2_better_theorem_astra.md) ; better-disposition:BT2-P4=adopted(BRIEF.md)
council: R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)
notes: headline-strength pending (lit gate open; no better-theorem review was run on v1.4 itself); acceptance only after the base ticket W3-START is accepted (PROTOCOL rule 11)
```
