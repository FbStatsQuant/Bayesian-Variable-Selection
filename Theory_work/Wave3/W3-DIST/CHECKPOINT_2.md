# W3-DIST — CHECKPOINT 2 (soft; key lemma proved, line-checked and break-reviewed) — 2026-11-15 21:05 CST — lead: Claude Fable 5.2

**CP2 gate met.** Lemma X and X′ (key lemma), Lemma S and Lemma V are cross-family line-checked, and the Astra break review
says **CP2: CONTINUE**. No C/S/F-type finding is open and no kill budget is spent (every item passed on its first attempt).
The lead continues (PROTOCOL_v4 §6: CP2 is soft).

## 1. What is proved and checked (files: DEPS.tsv)
| item | proof | cross-family check | result |
|---|---|---|---|
| Lemma X, Lemma X′ (in-sample exponential core) | `lemmas/X.md` v0.3 (fractional-moment route; self-contained modulo locked T01) | L1, Astra | VERIFIED, no findings |
| Lemma S (size tail), Lemma V (superset moment bound) | `work/C_size/S.md`, `V.md` | L5, Astra | VERIFIED; 2 minor, 1 nit, applied |
| Lemma H, Lemma T, Theorem DIST-3 | `work/B_transfer/` | L3, Sol | VERIFIED, no findings (T exactly as stated, self-contained) |
| Bridges B0–B3; assembly of reader Theorems A, B | `work/E_bridges/` | L4, Sol | VERIFIED; 5 minor, applied (conditional on the master displays) |
| Lemma P6, Theorem DIST-C, Corollary C | `work/D_output/` | L2, Sol | VERIFIED; 4 minor, 1 nit, applied |
| Break review of the key lemma and of the passage to (1.1), (1.2) | — | BR1, Astra | NOT BROKEN ×4; 3 minor assembly repairs; **CONTINUE** |
| Reader versions, bridges' statements, changelog tags | STATEMENT §1R | S2, Sol (blind read) | REPAIR REQUIRED → repaired in v1.4 (below) |
Same-family pre-checks (Opus, filters): P2–P6, all VERIFIED or VERIFIED-WITH-AMENDMENTS, no critical or major finding.

## 2. Statement changes since CP1 (STATEMENT v1.3 → v1.4.3; changelog at its foot)
- **No change to the mathematics of TC1–TC8.** (1.1) is proved with c = ½ and C′ = 33; (1.2) with c = ½; DIST-3 with c = 1.
- **TC9 (reader Theorem A): EQUAL for the mathematics** (manager's reading; HQ decides on a headline card): the Setup now
  describes the prior with r, the number of predictors not constant in the sample (v1.3 wrote p — a different prior on
  data sets with a dropped column); the sentence "no identifiability condition" is replaced by "no beta-min and no fixed
  lower bound on eigenvalues". Assumptions (A1)–(A5), displays (i), (ii), the sentence without (A4), rate and constants
  are unchanged.
- **WEAKER, non-target (reported here as required):** companion Theorem B gains "b_n > 0" (it was false as written: S2
  counterexample with b_n = −1); bridge remarks B2/B3 (window inequalities false for small p) and B0 (domain) replaced by
  the weaker true forms the proofs use.
- Honest remark added: with the absolute constants actually proved (c₂ = 10⁻⁵ in the sparse lower bound), Theorem A's
  threshold n₀ is of order 10¹⁵–10¹⁸; the theorem is asymptotic.

## 3. What is left
1. `lemmas/DIST12.md` — the proof of (1.1), (1.2) from Lemmas H, T, X, X′, with the three repairs of the break review —
   is written and in its cross-family line check (L6, Sol).
2. One Sol diff check of STATEMENT v1.3.1 → v1.4.3 and of the small amendments appended to proof files after their line
   checks (DEPS marks S, B3, P6, DIST-C, Corollary C and the two reader theorems STALE until then).
3. REPORT.md with the registry block; sweep (Astra); citation check; council; CP3.
4. Not verified by any reviewer and carried as premises: the locked identification of the coded posterior with the
   contrast model (T01); W3-POST Theorem 1 (for Theorem B); the W3-SAMP delivery premises (for the conditional parts of
   DIST-C).

## 4. Stretch items
- A claimed counterexample (API attempt F-b-r2, in an Opus pre-check with numerics): without the non-degeneracy
  condition, the exponential form at the sharp rate fails for the coded prior (posterior mass ≳ 1/n on fits far at the
  log n/n scale). If confirmed, the condition is necessary for that form — a sharpness result for TC4 — and the
  exponential version of stretch item S-FIT is closed negatively. The in-probability version stays open (partial
  results: supersets done). No second Fable requested.
- S-APX, S-EXP: not started (after CP3 or on request).

## 5. Estimate
L6 and the diff check: hours. REPORT + sweep + council: 1–2 days of wall-clock, depending on Codex.
