# W3-START — CHECKPOINT 2 (key lemma proved; mid-point review) — 2026-11-11

Lead: Claude Fable 5.2 (Claude Work, effort high). Worktree `C:/Users/felip/BVS-wt/W3-START`, no git state changed.

**Mid-point verdict: CONTINUE** (independent Astra, blind). The fixed-design theorem START-F and all its components are
written, line-checked by three cross-family reviewers and read as one argument by the mid-point reviewer: every claim
is graded "proved as stated", with no CRITICAL or MAJOR finding in any round. Nothing is PROVED-CHECKED yet: that label
needs the sweep and the council (CP3).

## 1. What was done in this leg

1. **STATEMENT v1.3, LOCKED.** HQ's CP1 decision applied:
   * P1: the normalised floor (FL-16) is replaced by a constant unnormalised Gram floor (GF-16). The toolkit is
     re-proved in this ticket, so **no registry claim is consumed** any more.
   * P3: the random-design transfer and the random-candidate clause of the misspecified form allow coefficients,
     support and leakage set that are functions of the design.
   * P2: a truncation level per null column inside a summable tail budget, with a new Corollary F4. **P2 closed in its
     one attempt**; there is no open item O4.
   * OVL: the deterministic inequality stays; the proposition is marked provisional.
   * Sol change check SC3: ACCEPT WITH CHANGES (1 MAJOR, 1 MINOR, 3 optional), all applied, the two required edits
     verbatim.
2. **Proofs L1–L5** in `lemmas/`, each with falsification numerics in `numerics/lemmas/` (0 violations).
3. **Line checks LC1** (three blind reviewers on one frozen manifest), then the **mid-point MP1** on a fresh manifest.

## 2. What is proved and checked

Status of every lemma file: "PROVED (by this seat)" plus the checks below. None is PROVED-CHECKED.

| file | content | line check | mid-point (MP1) |
|---|---|---|---|
| `L1_AGG_FLOOR.md` | table identities (AGG-a)–(AGG-d), FLOOR, Theorem (T0); deterministic | LC1-A Sol: VERIFIED-WITH-AMENDMENTS (2 MINOR) | (C0), (T0): "proved as stated" |
| `L2_TK.md` | toolkit under (GF-16): events, RSS in τ-form with error O(n^{−1/3}), score expansion with a bounded remainder | LC1-B Sol: VERIFIED | [TK]/(B-TK): "proved as stated" |
| `L3_LEAK.md` | Lemma J, column levels, leakage bridge (B-L), arithmetic of F4 | LC1-C Astra: VERIFIED-WITH-AMENDMENTS (2 MINOR) | [LEAK]/(B-L): "proved as stated" |
| `L4_VIS.md` | visibility bridges (B-V2) (margin form) and (B-V1) (constant level) | LC1-B Sol: VERIFIED-WITH-AMENDMENTS (2 MINOR, one on numerics reporting) | [VIS]/(B-V1), [VIS]/(B-V2): "proved as stated" |
| `L5_ASM_STARTF.md` | assembly (C1); START-F (T1)(a)–(c); uniform form (T1)(d) with explicit constants | LC1-C Astra: VERIFIED | (C1), (T1)(a)–(d): "proved as stated" |

All six line-check amendments were the reviewers' exact local repairs and are applied; the mid-point read the amended
files. The statement did not change after SC3.

What START-F now says, in words: under an energy bound, the constant Gram floor, visibility, and the averaged leakage
condition, the start odds against the truth are O_P(n^{−1/2} × leakage functional) plus a visibility term that is
polynomially small. To first order they equal the prior-weighted sum of the single-null block Bayes factors. The bound
holds uniformly over the class with explicit constants, which is what the random-design transfer will use. The
exponent ½ cannot be improved (deterministic floor).

Numerics (`numerics/lemmas/RESULTS_LEMMAS.md`), observations only:
* AGG and FLOOR: 8,000 random-table cases and 500 data sets, 0 violations; smallest one-step ratio × √(n+1) = 1.0125.
* Toolkit on near-twin designs (Gram eigenvalue down to 0.04): both scalar bounds hold; (E1) is attained to 0.1%.
* Assembly at p = 12 by exact enumeration: o₀√n ≈ 2.2–2.8 (flat in n); o₀/T₁ = 1.19, 1.07, 1.03, 1.02 for n = 100…6400.
* Three errors in my own test scripts were found (two by me, one by LC1-A) and fixed before the recorded runs.

## 3. Review record of this leg

| round | seat | manifest digest | verdict | files |
|---|---|---|---|---|
| SC3 | Sol (blind) | bf619625… | ACCEPT WITH CHANGES: 1 MAJOR, 1 MINOR, 3 optional; all applied | `reviews/SC3_change_check_sol.md`, `SC3_disposition.md` |
| LC1-A | Sol (blind) | 867e1c93… | L1: VERIFIED-WITH-AMENDMENTS | `reviews/LC1_A_line_check.md` |
| LC1-B | Sol (blind) | 867e1c93… | L2: VERIFIED; L4: VERIFIED-WITH-AMENDMENTS | `reviews/LC1_B_line_check.md` |
| LC1-C | Astra (blind) | 867e1c93… | L3: VERIFIED-WITH-AMENDMENTS; L5: VERIFIED | `reviews/LC1_C_line_check.md`, `LC1_disposition.md` |
| MP1 | Astra (blind) | 8e08c109… | **CONTINUE**; 11 claims "proved as stated"; 2 MINOR on the statement | `reviews/MP1_midpoint_astra.md`, `MP1_disposition.md` |

`manifest.py bind` passes for every review; `manifest.py verify` passes on the current tree for MANIFEST_MP1.

## 4. Mid-point findings (both MINOR, both on the locked statement; not yet applied)

1. **(N2) is vacuous when s₀ ≤ 15.** Its premise asks a null to gain given every subset of the truth, including the
   whole truth, where the gain is zero. So the partition-free "one leaking null destroys the start mass" clause says
   nothing for the usual support sizes. The working statement is the component diagnostic (C2)(i), on the actual
   partition. The CP1 summary of the limits overstated this point. I checked the finding and accept it.
2. The bridge table writes the inputs of (B-L), (B-V1), (B-V2) as [TK]; their proofs use the quantitative toolkit of
   L2. Wording only; (T1) is unaffected.

Proposed handling: STATEMENT v1.3.1 with these two edits and one Sol diff check, as step 0 of the next leg.

## 5. What is left (to CP3)

| item | content | reading after the mid-point |
|---|---|---|
| step 0 | STATEMENT v1.3.1 (two MINOR edits above) + Sol diff check | short |
| L6 | corollaries F1–F4 | viable as planned (F4's arithmetic is done) |
| L7 | necessity: (C2)(i),(ii), (T4) | viable; the toolkit gives both directions |
| L8 | random-design transfer (T3)(a) | viable; immediate from (T1)(d) |
| L9 | Gaussian-row bridge (B-R) and (T3)(b) | **main risk**: the averaged leakage bound over conditioning sets selected by the partition is new work |
| L10 | P-START interface, Proposition OVL, misspecified form (T6) | viable; OVL looks short |
| — | examples table (T7), exhaustive sweep, council (≤ 3 rounds), REPORT with registry block | — |

Two cautions from the mid-point that I take into the plan:
* For (B-R), a bound on the largest partial correlation is not a bound on the averaged functional; an integration step
  is needed, conditioning only on the columns of the reference set.
* The zero-leakage clause of (T3)(b) (C_L = 0, polylogarithmic rate) may hold only as an O_P statement, not with a
  fixed constant with probability → 1. If so, that clause is restated and goes back through a statement check.

**Honest estimate.** This leg took about 50 minutes of run time against my CP1 estimate of 7–10 hours, so my earlier
figures were far too high for writing and review turnaround. For the rest I expect 1.5–3 hours of lead run time:
* about 1 hour for L6–L8 and L10 with their line checks;
* (B-R) is the uncertain part: one attempt plus one Astra break review, then either it closes or (T3)(b) is narrowed
  to what the transfer clause gives and returns through CP1 (PROTOCOL rule 10);
* sweep and council: 1 + 2 reviewer runs per round, up to 3 rounds.
Expected agent runs: 3–4 line checks, 1 break review, 1 sweep, 2–6 council seats (one of them Claude, on Claude Work).

## 6. Decisions requested from HQ

1. Greenlight for the next leg (to CP3).
2. Approve STATEMENT v1.3.1 with the two mid-point edits and one Sol diff check (recommended). The first edit narrows
   what the headline may say about necessity of the leakage level: sharpness is then claimed on the actual partition
   ((C2)(i)), and partition-free only for s₀ ≥ 16.
3. Confirm the kill budget for (B-R): one Fable attempt and one Astra break review; on failure narrow (T3)(b).

## 7. Record

* **Agents in this leg:** lead (Claude Fable 5.2, Claude Work, effort high); SC3, LC1-A, LC1-B (Codex gpt-6.1-sol,
  high); LC1-C, MP1 (Codex gpt-6-astra, high). Three LC1 launches and the lead's run were interrupted once by the
  provider handoff and re-launched; the interrupted runs produced no output. Claude tally: CP 1 / CW 1. No NOTS use.
* **Holds:** `HOLDS.md` (main checkout) read before each step: no holds.
* **Consumed claims:** none.
* **Kill budgets:** key lemma: one attempt, closed. P2: one attempt, closed.
* **Files** (all in `Theory_work/Wave3/W3-START/`, uncommitted; HQ commits):
  * modified: `STATEMENT.md` (v1.3 LOCKED), `PLAN.md`, `ASSUMPTION_MAP.md` (§3 added), `LOG.md`
  * new: `lemmas/L1_AGG_FLOOR.md`, `L2_TK.md`, `L3_LEAK.md`, `L4_VIS.md`, `L5_ASM_STARTF.md`
  * new: `numerics/lemmas/` (3 scripts, helper, 4 outputs, `RESULTS_LEMMAS.md`)
  * new: `reviews/`: 5 briefs, 3 manifests (SC3, LC1, MP1), 5 reviews, 3 dispositions
  * new: `CHECKPOINT_2.md`
* The status lines inside the lemma files still read "PROVED (by this seat, unchecked)": they were left untouched so
  that the tree verifies against MANIFEST_MP1. The check record is this file and the dispositions.
