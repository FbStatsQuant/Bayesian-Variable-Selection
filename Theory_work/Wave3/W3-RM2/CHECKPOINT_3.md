# W3-RM2 — CHECKPOINT 3 (final): **CP3-PASS** — 2026-11-12

Lead: Claude Fable 5.2 (Claude Work, effort high). Worktree `C:/Users/felip/BVS-wt/W3-RM2`, branch theory/W3-RM2; no
git state changed — everything since c2257ab is uncommitted, HQ commits. Run ends here. Full report: `REPORT.md`.

## 0. Flags (read first)
1. **Council round R1 PASSED on one frozen manifest (00bbeab8…): gpt-6-astra 9.5, Claude Opus 5.5 8.8, all six
   gates PASS in both seats, no REQUIRED finding.** `manifest.py bind` OK. First round; nothing exhausted.
2. **What is proved: the reported model at polynomial leakage |Q| ≤ n^b for every b < ½ (the brief asked b < ¼),
   in both forms — under (V), (L^b) and a lattice-width condition (W).** Not "(V) + (L)" alone: removing (W) is
   path-level and stays open (O1). Both council seats name it the most valuable missing strengthening.
3. **Both HQ riders succeeded.** T6: the Gaussian-row leak condition is in product form — the leak bound at every
   conditioning set, localisation with no rate. P3: leak scale o(√(log n/n)). Consequence: the polynomial-decay
   example needs **α > 2** in Form R, where W2-LOC2:Thm-Poly needs α > 17/2.
4. **Headline-strength pending (rule 10).** The better-theorem review on the final statement (BT2) found 5
   adoptable refinements and 2 ticket-size ones; none changes the headline. I did not adopt them into v1.4 (each
   touches a checked proof). **HQ decision needed:** adopt them in one revision v1.5 with riders T2/T4 (§5).
5. **The tree differs from the council manifest in 7 files** — nine non-required record fixes the seats listed, and
   the council result itself in REPORT. An independent Sol diff check (PC1) attests "editorial/record only — the package
   stands as passed by council round R1". The exact council tree is restorable from
   `reviews/as_reviewed_by_R1/`. HQ's audit therefore takes the rule-15 path, not a bare `verify` on MANIFEST_R1.
6. **Round manifests were frozen but not committed** between CP2 and now (the lead changes no git state). The
   restore points are the `reviews/as_reviewed_by_*` snapshots and HQ's commit at this checkpoint.
7. **Conditional:** (C1) on SOP:TH09@1.0.0 only; (C2) on W2-APP:POST@1.0.1 only; examples E2, E3 also on
   W2-LOC2:Lemma-BC and Lemma-IR ("PROVED (by this seat, unchecked)") — `@hyp` edges in the registry block. W1-GEN:L1
   and W3-RM:B9 are no longer consumed.
8. Statuses in REPORT are "PROVED (by this seat, unchecked)" + check record + the council line; **PROVED-CHECKED,
   ingest and `council-pass` are HQ's after the acceptance audit.** Registry gates `lit`, `necessity`, `better` are
   left PENDING with evidence files.

## 1. Result (`STATEMENT.md` v1.4)
* **(C1) RM2-F, fixed design.** (T1-F), floors, (V), a deterministic leak set |Q| ≤ n^b with b < β(η, A) =
  ½ − η/2 − √(2Aη), the signal floor (BM-W), and (W): the lattice width gap → −∞. Then one data event of
  probability → 1 on which every admissible run reports Ŝ⁺ = S₀; LS0 makes ≤ n^b deletions, certified; the shipped
  cap never binds.
* **(C2) RM2-R, Gaussian rows.** (T1-R), (FL-R), PTV, |Q| ≤ n^b, leak ϖ_n = o(√(log n/n)) at every conditioning set
  of size ≤ 15, neighbourhoods |H_l| ≤ n^ρ with localisation r_n → 0, 15ρ + b < ½, and (W-R) (supplied by population
  reference/atom or local-regression conditions). Same conclusions under the joint law.
* **(C3)** width gap → −∞ ⇒ whole-lattice no-addition (rate exp(−gap²/8)); gap → +∞ ⇒ it fails; five sufficient
  forms. **(C4)** RM2-F ⇒ RM-F, RM2-R ⇒ RM-R. **(C5)** examples: the parent's; polynomial decay α > 2 (both forms);
  one truth with n^b weak proxies (every b < ½); one equicorrelated group (b < 3/10). **(C6)** `SHARPNESS.md`.
No design family in any theorem statement. No delivery claim. No method change requested.

## 2. Kill budgets
| item | budget | used | outcome |
|---|---|---|---|
| Form F key lemma (L2) | 3 attempts | 1 | verified (LC1-B, MP1, SW1, council) |
| (P7) Gaussian-row sandwich (L4) | 2 attempts | 1 | verified (LC2-A, SW1, council) |
| rider P3 | 1 attempt | 1 | **succeeded** (inside L4) |
| rider T6 | 1 attempt | 1 | **succeeded** (inside L4) |
| council | 3 rounds | 1 | **passed** |

## 3. Review record since CP2 (all files in `reviews/`; every review quotes its manifest digest)
| round | seat | object | verdict |
|---|---|---|---|
| PV1 | Sol (prover) | L6 examples | written |
| LC2-A | Astra, blind | L4 | V-W-A, no FATAL/MAJOR; own stress test clean |
| LC2-B | Sol, blind | L5 | VERIFIED (2 MINOR conventions) |
| LC2-C | Opus (Claude Work), blind | L6 | VERIFIED / V-W-A (3 MINOR, 3 NIT) |
| SC2 | Sol | STATEMENT v1.3 → v1.4 | ACCEPT WITH CHANGES (1 MAJOR notational: symbol clash, fixed) |
| RC5 | Sol | the 13 LC2-round fixes | all RESOLVED, editorial/record only |
| SW1 | Astra, blind | exhaustive sweep | (C1)–(C4), (P0)–(P10) VERIFIED; 0 FATAL, 2 MAJOR on records, 4 MINOR, 1 NIT — applied |
| BT2 | Astra, blind | better theorem on v1.4 | 5 ADOPT NOW, 2 WORTH A TICKET, 0 SPECULATIVE |
| RC6 | Sol | the 7 sweep fixes (24 hunks) | all RESOLVED, editorial/record only |
| **R1** | **Astra 9.5; Opus 8.8**, blind | council, six gates | **PASSED, no REQUIRED finding** |
| PC1 | Sol | post-council diff (7 files) | "editorial/record only — the package stands as passed by council round R1" |
Dispositions: `LC2_`, `SW1_`, `BT2_`, `C1_disposition.md`. No review layer skipped. `citecheck.py`: 92 citations,
0 MISS (re-run by RC6). The two sweep MAJORs were records: the energy constant read "M ∈ (0, 1]" while examples use
M > 1 (now "M > 0" with a response-rescaling remark, the remedy the sweep asked for); the width probe B2 was
described as a certified isolated violation (now "nominal width-stress design").

## 4. For HQ's acceptance audit
* Council files: `reviews/C_R1_council_astra.md`, `reviews/C_R1_council_opus.md`; manifest `reviews/MANIFEST_R1.txt`.
  Council cell: `R1; MANIFEST 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a; astra=9.5
  PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)`.
* `verify` against MANIFEST_R1: exactly 7 files CHANGED (STATEMENT, REPORT, SHARPNESS, ASSUMPTION_MAP, L2 and L3
  headers, numerics/RESULTS) — the diff PC1 covers; current tree = `reviews/MANIFEST_PC1.txt` (d2b37949…).
* Registry block: end of `REPORT.md`, 18 claims, one status each; RM2-F and RM2-R are CANDIDATES implying
  W3-RM:RM-F and W3-RM:RM-R (HQ CP1 decision); supersession is HQ's (RM is a package headline — owner).
* Consumed claims to re-check on current main (rule 11): W3-RM:RM-0@1.0.0, W3-RM:E4@1.0.0, W3-RM:RM-F@1.0.0,
  W3-RM:RM-R@1.0.0 (PROVED-CHECKED); SOP:TH09@1.0.0, W2-APP:POST@1.0.1, W2-LOC2:Lemma-BC@1.0.0, Lemma-IR@1.0.0
  (@hyp); proof templates C-GROW:L0.1, L0.2, L2.1–L2.3, L3, L6.4, W2-LOC2:NA-R, W3-RM:SAND-R, D-loc (@proof).
* INPUTS.txt follows rule 15 as amended (no wave documents, no registry tables): 28 inputs.
* HOLDS.md: no holds at any step.

## 5. Decisions asked of HQ
1. **Accept CP3-PASS** for v1.4 (labels, ingest, merge per your audit), labelled headline-strength pending?
2. **Revision v1.5** (recommended, one leg, one change check): BT2 P1 (signal floor as an additive margin), P2
   (exponent gap²/2), P3 (width lemmas for |Q| log n/n → 0), P4 (entropy budget in the Gaussian-row reference
   condition), P5 (quantitative reference budget), P7 (equicorrelated example to b < 3/8, one attempt), the three
   deferred NITs (F8, F9, F11), together with riders **T2** and **T4**. P6 (leak at the exact noise scale, non-sharp
   constant) only if you want it.
3. **Supersession** of RM-F / RM-R by RM2-F / RM2-R: the containments are proved and council-passed; owner's call.
4. **O1** (no lattice condition; b ≥ ½): the next real theorem; separate ticket with a kill budget. A cheap first
   probe is P7's second half: for 3/8 < b < ½ the equicorrelated group would be a proved case where the
   whole-lattice route fails.

## 6. Open items (`SHARPNESS.md` §7)
O1 path-level / no (W) / b ≥ ½ · O2 counting form of (L) (with T2(c)) · O3′ Form R leak at the exact scale ·
O4′ equicorrelated group beyond 3/10 · O5 bounded width gap · O6 polynomial decay α ∈ (1, 2].

## 7. Files and agents
`STATEMENT.md` (v1.4), `REPORT.md`, `SHARPNESS.md`, `ASSUMPTION_MAP.md`, `PLAN.md`, `citecheck.py`, `LOG.md`,
`CHECKPOINT_1–3.md`; `lemmas/` L0–L6; `numerics/` (208 boundary runs, lemma checks K1–K13); `reviews/` (manifests
SL1 … PC1, briefs, replies verbatim, dispositions, reviewed-text snapshots, CITECHECK.txt).
Agents in this leg: lead (Claude Fable 5.2, Claude Work); Sol ×6 (PV1 prover, LC2-B, SC2, RC5, RC6, PC1); Astra ×4
(LC2-A, SW1, BT2, council); Opus ×2 (LC2-C, council; Claude Work, effort high). Ticket total: Sol ×13 + PV1 (prover),
Astra ×6, Opus ×2. Claude tally: CW 3 (lead, 2 Opus) / CP 0. No NOTS use. No effort above high.
