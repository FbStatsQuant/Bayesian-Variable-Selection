# COUNCIL REVIEW — Round 3 (Scoped Fix-Verification) — Seat: NEON (TH-SONG-ASSUMPTIONS)

**Revision checked:** v1.2 (`7c7ca30f`) → v1.3 (`4bacc09d`, branch `dept/theory`), via `council/R2_TO_R3.diff`, `council/RESPONSE_R2.md`, `COUNCIL_RECORD.md`, `scripts/e9b_width_mc_ext.py`, `tables/e9b_width_ext_s1.tsv`, and exact changed/targeted passages in the four package files.
**Charter:** Scoped verification of (a) prior-round substantive/blocking issues and (b) new substantive flaws or regressions in the v1.3 diff only.

---

## 1. Round 2 substantive/blocking issue dispositions

| R2 ID | Issue summary | Status | One-line reason |
|---|---|---|---|
| **Sol 1 (BLOCKER) / Neon S2 / Opus S-1** | TS-b step 3 coded-likelihood bound (`H_Dm`, `−(n/2+a₀)log(1+W/V_n)`, `B_Dm ≤ 0`, monotonicity at `2(1+δ)B_Dm`, `m=0`, `|U| ≤ min(p, s0+J)`, fixed `C`, Linearisation alignment) | **fixed** | Algebra, uniform `RSS_U` lower bound on the step-2 truncation event, `B_Dm ≤ 0` / `B_Dm > 0` branches, `m=0`, `C` definition, and Linearisation are all mathematically exact in `ASSUMPTIONS` ll.290–306, 315; proof obligation logged in `DEFINITIONS` l.153 and `DOSSIER` l.244. |
| **Sol 2 (BLOCKER / B-2) / Neon S3 / Opus S-3** | Limit S1 mixed-rival claim to zero-slack E9 diagnostic; cover `m=2` at `p=5000`, `m≥3` (incl. `m=4`), `C ≍ (s0+1)²`, asymptotic `m*(d)`, E9b, AR(1) Markov minimizer | **not fixed** *(incomplete)* | Main text, E9b (`e9b_width_mc_ext.py`, verified against `e9b_width_ext_s1.tsv`), `C=121` calibration, and AR(1) Markov proof are fixed cleanly, **but** `ASSUMPTIONS` §1 Decision **D4** (l.31, named in Sol 2 and claimed updated in `RESPONSE_R2.md`) was untouched and still says `"for mixed rivals with d = 1, m ≤ 2 ... the margin holds there with surplus ≥ 3.3 at SNR 2"`; `DOSSIER` A-MARGIN-U Q6 (l.191, also named in Sol 2) still writes `"On ordinary correlated designs"`. |
| **Sol 3 (SUBSTANTIVE)** | Exact all-deletion `κ_n` (1,023 `D`), `40/41` supersets & `39/41` one-null, `E K₁` HPM vs MPM | **fixed** | Independently recomputed all 1,023 deletions: `0.62614–0.69269` (SNR 1) and `2.50455–2.77075` (SNR 2), min at `d=6` (`p=500`) and `d=3` (`p=5000`), gap `1.05–1.69%`; accurately carried into all four files, along with `40/41` / `39/41` and HPM/MPM separation. |
| **Sol 4 (SUBSTANTIVE / B-3) / Neon S1 / Opus S-2** | Remove `A-NEC` `"smaller than each"` contradiction; SL (26) vanishing lower & growing upper thresholds; NH14 exact dependence vs SBJ `ν_{k*}` indexing without claiming duplicates | **not fixed** *(incomplete)* | Blanket sentence and SL (26) are fixed in all three files and SBJ is corrected in `ASSUMPTIONS` l.107, **but** `DOSSIER` `A-NEC` Q3 bullet 1 (l.110) was untouched and still asserts `"SBJ Assumption 4, p. 14, and NH14 Cond. 4.5 ... bound the minimum nonzero sample eigenvalue, so they allow exact duplicates that A-NEC excludes"`, contradicting `ASSUMPTIONS` l.107 and `RESPONSE_R2.md` item 3. |
| **Neon S4 / Sol 7 part (SUBSTANTIVE)** | Stale `"the special case"` label for `thm:omitted` | **fixed** | Replaced with `"previously delivered analogue"` (with Gaussian rows, fixed floor on its own window, diverging per-coefficient signal, expectation bound) in `ASSUMPTIONS` l.351 and `DEFINITIONS` l.85. |
| **Sol 5 (SUBSTANTIVE)** | `TD′` exact conjecture (`2 ≤ p`, enlarged window with `(s+1)`, explicit probability display & `M`-range), drop `TS-b′`, stretched-exponential/overlapping envelopes, `TD-A` variance proxy | **fixed** | Exact conjectured display, `(s+1)` window, `2 ≤ p`, `TS-b′` removal, stretched-exponential/overlapping-envelopes wording, and `TD-A` centred-tail variance proxy are cleanly applied in `DEFINITIONS` ll.122–126, 131 and `ASSUMPTIONS` ll.79–85. *(Minor: `DOSSIER` l.81 still says `"cover ... SL Cor 1 for α < ½"`, worth aligning when fixing the two misses above.)* |
| **Sol 6 (SUBSTANTIVE)** | Coded vs raw `b₀`, `A-BS` fixed-endpoint denominator with `n^{-1/2}`, raw `p` on centring event, `ν(dx)dy` Hellinger measure, candidate-set rule, full-rank relaxation | **fixed** | All six conventions are accurately implemented across `DEFINITIONS` ll.29, 107, 154, `ASSUMPTIONS` ll.49, 120, 206, 215, 351, and `DOSSIER` l.196. |
| **Sol 7 rest (SUBSTANTIVE)** | `SL-0` EBIC qualification; `TM-b` nonempty pseudo-support `S0^C ≠ ∅`; form-invariance qualification | **fixed** | Applied accurately in `DEFINITIONS` ll.77, 195, 224 and `ASSUMPTIONS` ll.351, 391. |
| **Sol 8 (SUBSTANTIVE)** | Strict-rounding fixes (`6.696`, `SD 0.121`, `1.175`); `E2` 9/136 residual ratio vs fixed-variance Hellinger max `0.21`; `|S ∪ S0| ≤ min(p, s0+J) ≤ q_n` | **fixed** | All four R2 items fixed across the four files (`SIMULATION` ll.295, 304, 176–178, 203, 351, 357; `ASSUMPTIONS` ll.127, 131, 180, 307; `DOSSIER` ll.27–28, 131, 146). *(See §2 for the same rounding direction recurring in the new E9b text.)* |

---

## 2. New substantive flaws or regressions introduced by the v1.3 diff

1. **Upward-rounded strict `≥` bounds on new E9b surpluses (minor regression of Sol 8).**
   - *Locations:* `SIMULATION_DATA_ANALYSIS.md` l.27, l.321; `OWNER_DEFENSIBILITY_DOSSIER.md` l.176; `THEOREM_DEFINITIONS.md` l.147.
   - *Flaw:* In `tables/e9b_width_ext_s1.tsv`, minimum SNR-2 `surplus_C121` is `2.3862` (row 8: `500, 500, d=1, m=2, D={3}`), which is strictly `< 2.39`; minimum SNR-3 surpluses are `6.7098` (`C=1`), `5.8065` (`C=121`), and `5.9091` (no credit), whereas `SIMULATION` l.321 prints `≥ 6.71 | ≥ 5.81 | ≥ 5.91` and `SIMULATION` l.27 / `DOSSIER` l.176 / `DEFINITIONS` l.147 print `≥ 2.39`.
   - *Fix:* Report `≈ 2.39 (min 2.386)` or `≥ 2.38` for `C = 121` (`≥ 2.48` for no credit), and `≥ 6.70 | ≥ 5.80 | ≥ 5.90` (or `min 6.710 / 5.807 / 5.909`) in `SIMULATION` l.321.

*(No mathematical or logical regressions in TS-b step 3, `e9b_width_mc_ext.py`, exact `κ_n`, `TD′`, `A-NEC`, or `A-MIS(iii)`. Note: `e9b_width_mc_ext.py` uses `NEAR = [10..49]` for `d = 1, 2, 3`, and the AR(1) Markov screening property holds for all `d ≥ 1` since `10 ∈ A` screens all nulls and `10 ∈ D` is minimized at `x_11`.)*

---

## 3. Gate verdict

**NOT CLEAR** — solely because two explicit R2 substantive/blocking passages were inadvertently missed during the v1.3 pass despite being reported fixed in `RESPONSE_R2.md` (`ASSUMPTIONS` §1 Decision D4 l.31 for Sol 2 / B-2, plus `DOSSIER` l.191; and `DOSSIER` `A-NEC` Q3 l.110 for Sol 4 / B-3), plus the upward-rounded `≥` signs on the new E9b numbers (§2). Every underlying mathematical, statistical, and computational issue from Round 2 — including TS-b step 3, E9b (`C = 121` / no credit), exact `κ_n`, `TD′`, `A-NEC` non-ordering, `A-MIS(iii)`, and conventions — is **genuinely fixed and sound**. Patching those three one-line text spots clears the gate immediately.

---

## 4. Optional D / R scores on assumptions touched by the diff

| Assumption | D | R | One-line reason |
|---|---:|---:|---|
| **A-GL** | 9.5 | 9.5 | Coded `b₀` vs raw `b₀s_y²` cleanly distinguished. |
| **A-DIM′** *(conj.)* | 9.5 | 9.5 | Exact conjectured display, `(s+1)` window, `2 ≤ p`, and `TS-b′` removal complete. |
| **A-NEC** | 9.0 | 9.5 | Blanket contradiction and SL (26) fixed everywhere; `-0.5` D only for the missed SBJ duplicates clause in `DOSSIER` l.110. |
| **A-BS** | 9.5 | 9.5 | Fixed-endpoint denominator (`n^{-1/2}`) and `1.175` rounding cleanly updated. |
| **A-MARGIN-H** | 9.5 | 9.5 | `E2` residual vs Hellinger ratios cleanly separated; `min(p, ...)` window covers bounded `p`. |
| **A-MARGIN-U** | 9.0 | 9.5 | Step 3 coded-likelihood bound, E9b (`C=121`), AR(1) Markov minimizer, and exact `κ_n` are solid; `-0.5` D only for untouched Decision D4 (`ASSUMPTIONS` l.31), `DOSSIER` l.191, and E9b `≥` rounding. |
| **A-MIS(iii)** | 9.5 | 9.5 | Candidate-set rule, `thm:omitted` analogue label, `S0^C ≠ ∅`, and full-rank relaxation all cleanly stated. |
