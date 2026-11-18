# W3-FAMC — REPORT (design-family corollary for core 3; draft for the council manifest; 2026-11-17)

Lead: Claude Opus 5.5 (claudeAgent_personal, high). Branch theory/W3-FAMC from main f0b8246c (cited files unchanged at
a779c1df). Tier B assembly, with no new lemma, no theorem change and not a Lean target. Statuses quoted here are as of this
report; claims.tsv governs.

## 1. What was done
- Step 0: not recorded as a corollary (`PLAN.md` table: W2-APP Family-map, RM2 L6 E1/E2, C-GROW C5a/C5c, TRACK_B B8–B10).
- `STATEMENT.md` v1.3: Corollary FAMC (§1), reader version (§1R), remarks outside the claim (§1b), D109 classes (§2),
  proof map (§3), inputs with verbatim statuses and D126 expansion (§4), not claimed (§5).
- `lemmas/A_assembly.md` v1.1: the block half is proved by explicit linear algebra (B.0–B.4: cross-group partial
  covariances vanish; ϖ_n = r_n = L_n = η_n = 0). The AR half is an instantiation of RM2 Example E2 (α = 3, b = ¼,
  ϱ = 1/120). Visibility comes from Lemma VIS (VIS-0/a/b/e) and C-GROW (G3b).
- Reviews: Sol R1 line check (11 findings, 11 accepted), Sol R2 diff round (5 findings, 5 accepted), and an independent Opus
  check of E2 with BC and IR (PASS; `reviews/E2_check_opus_R1.md`). Citecheck: 0 failures.

## 2. Caveats (plainly)
- The AR half rests on `W3-RM2:Ex-PolyR`, `W2-LOC2:Lemma-BC` and `W2-LOC2:Lemma-IR`, whose registry statuses are not
  PROVED-CHECKED. HQ DP1: record the AR half unconditionally on the strength of this ticket's E2 check (PASS), which goes
  to W3-RM2 through the manager. The C-GROW facts (P1)–(P4) also close the AR leakage independently.
- (BLK-g)/(AR-g) need dist(ϑ_n, B) ≥ δ > 0. B is null only when the local patterns are countable (fixed AR; group
  matrices from a finite list); in general it may have interior.
- Constants degrade as |ρ| → 1; no uniformity in ρ. Group size g is fixed.
- Theorems 5 and 10 are not extended (their no-leakage (A5) fails on these families when a null–truth covariance is
  bounded away from 0).

## 3. Card text (for the H5 card / Writing; = STATEMENT §1R)
See `STATEMENT.md` §1R (verbatim source). Writing's wording "any fixed AR correlation" is handled after recording (HQ).

## 4. Chain record
Corollary FAMC ⇐ `W3-RM2-R:RM2-R-plus@1.0.1` (master of Theorem 6) with hypotheses verified by: B.1–B.4 (block),
`W3-RM2:Ex-PolyR@1.0.3` (AR; conditions `W2-APP:POST@1.0.7`, `W2-LOC2:Lemma-BC@1.0.0`, `W2-LOC2:Lemma-IR@1.0.0`),
`W3-AUDIT-V:VIS@1.0.0` and `C-GROW:C5a@1.0.0` (visibility), `W3-RM2:D-to-W@1.0.3` ((W-R), block), `W3-RM2:POST-R@1.0.3`.

## 5. Open items (named)
- O1: class-1 search for the two families (PLAN P5; optional; 2b stands).
- O2: three wording notes on RM2/LOC2 files from the E2 check (for W3-RM2, via the manager).

## 6. Registry blocks

```
REGISTRY
claim: W3-FAMC:Cor-FAMC | kind: corollary | statement: STATEMENT.md:48-80 | premises: STATEMENT.md:25-32
status: PROVED (by this seat, unchecked) | status_source: lemmas/A_assembly.md:1
assumptions: A:IID-GAUSS-ROWS ; A:GAUSS-NOISE ; A:P-POLY ; A:FIXED-S0 ; A:COEF-BOUNDED ; A:OP ; A:BLOCK-LE-16 ; A:DELIV-D ; A:FAMC-DESIGN (new | design family: block or AR | Sigma_n block-diagonal on a deterministic partition into groups of size <= g fixed with lambda_min(Sigma_n) >= c fixed, or Sigma_n,lk = rho^|l-k| with rho in (-1,1) fixed | STATEMENT.md:52-75 | shared no | bridge W3-FAMC:Cor-FAMC) ; A:FAMC-COEF (new | no cancellation among the true coefficients | (BLK-1) one truth per group, (BLK-s) aligned signs within groups, (BLK-g) inf dist(theta_S0, B) > 0; (AR-s) aligned signs, (AR-sep) separation sum_{k!=j}|theta_k||rho|^|j-k| <= (1/2)|theta_j|(1-rho^2)/(1+rho^2), (AR-g) inf dist(theta_S0, B) > 0 | STATEMENT.md:52-75 | shared no | bridge W3-FAMC:Cor-FAMC)
conclusion: reported-model: conclusion of reader Theorem 6 (row 3.1): data events G_n with P(G_n) -> 1 on which every admissible output run reports S-hat = S0; P(output and S-hat != S0) -> 0; under (S4): output for every admissible n >= 3 and P(S-hat = S0) -> 1 | rate: n/a | scope: Gaussian rows; (BLK) or (AR) design with a coefficient condition; 2 <= p <= n^A; s0 fixed; theta_lo <= |theta_j| <= theta_hi
depends_on: W3-RM2-R:RM2-R-plus@stmt ; W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:DLV-0@stmt ; W3-AUDIT-V:VIS@proof:VIS-0,VIS-a,VIS-b,VIS-e ; C-GROW:C5a@proof:P1-P4,G3b ; W3-RM2:Ex-PolyR@proof:E2-verification ; W3-RM2:D-to-W@stmt ; W3-RM2:POST-R@stmt
implies:
notes: Additive special case of row 3.1 (reader Theorem 6) on two design families; replaces (A3)-(A6) by primitive conditions. AR half recorded unconditionally per HQ DP1 on the strength of reviews/E2_check_opus_R1.md (PASS). Ex-PolyR, Lemma-BC, Lemma-IR statuses quoted unchanged in STATEMENT §4.
```
