# W3-MISR-R — REPORT (rider T13; draft for the council manifest; 2026-11-15)

REPORT restates nothing (PROTOCOL_v4 §3): claims, hypotheses and conclusions are in `STATEMENT.md` (v1.2); proofs in
`lemmas/`; evidence for the gates in `TARGET.md`; the reader-version proposal in `READER_DELTA.md`. Any sentence here that
asserts mathematics not in STATEMENT or a checked lemma is labelled HEURISTIC or OPEN.

## 1. What was done
Four claims, each a delta over W3-MISR v1.3 (`STATEMENT.md` §0 table, `:12-23`):
- W3-MISR-R:CorG-min — `STATEMENT.md:48-92`; proof `lemmas/G1_min.md`.
- W3-MISR-R:CorGb-plus — `STATEMENT.md:94-108`; proof `lemmas/G2_corr.md` (copy of BASE G.2 with [R-1]–[R-5]).
- W3-MISR-R:CorH-plus — `STATEMENT.md:110-132`; proof `lemmas/H1_plus.md`.
- W3-MISR-R:CorH-U — `STATEMENT.md:134-155`; proof `lemmas/H2_uniform.md`.
Supersession proposal (HQ with the consultant, v4 H5): each new claim implies the BASE claim it replaces
(`STATEMENT.md:187-197`); the lead proposes that CorG-min, CorGb-plus and CorH-plus supersede W3-MISR:Cor-G(a), Cor-G(b) and
Cor-H once accepted. W3-MISR:Cor-G(b) is the reader version of the headline masters (card row 1.4): see `READER_DELTA.md`.

## 2. Chain record
Statement lock L1 (Sol, NORMAL): `reviews/L1_statement_lock_sol.md`, disposition `reviews/L1_disposition.md`. Line check +
statement-change check K1 (Sol, NORMAL): `reviews/K1_linecheck_sol.md`, disposition `reviews/K1_disposition.md`; re-check of the two repairs K2 (Sol, NORMAL): `reviews/K2_recheck_sol.md`. Changelog (`STATEMENT.md` §10): v1.1a WEAKER (an interpretive sentence of CorH-plus's KL reading restricted to a deterministic intercept; no display changed; tag set by K1), v1.1b EQUAL, v1.2 NEW-CLAIM (CorH-U (G), approved at CP1). Errata: `ERRATA.md`. DEPS:
`DEPS.tsv` (kept by `deps_hand.py`). Citation check: `citecheck.py` → `reviews/CITECHECK.txt`. Boundary numerics:
`numerics/N1_boundary.py` → `numerics/N1_out.txt`. Council: (to be filled at CP3).

## 3. Bears on W3-DIST — HEURISTIC/OPEN (not a claim of this ticket; for the manager to hand to HQ)
HEURISTIC: in the setting of CorG-min (b) with iid rows and deterministic (α, a, γ, τ²) (e.g. (E1), or (E2) with iid
candidate rows), the candidate-only problem satisfies "rows iid; given x_𝒞, y = α′ + x_𝒞ᵀβ^𝒞 + ε′ with ε′ ~ N(0, σ²_𝒞)
independent of the design" (`STATEMENT.md:67-70` gives the conditional law given the whole candidate design), which is the
form of W3-DIST's random-design premise as described in `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md:88-95`. If that
premise is exactly this, W3-DIST's conclusions would apply to a candidate run with f* the Kullback–Leibler projection
(`STATEMENT.md:126-130`). OPEN: (i) W3-DIST's premise was not read or checked here (W3-DIST's folder is out of scope);
(ii) the strict-sparsity caveat of `TRIAGE.md:93-94` (β^𝒞 = β_𝒞 + γ is often dense) applies unchanged; (iii) the removal of
a fixed σ*² in W3-DIST by the scale invariance of Lemma R′ (`TRIAGE.md:96-99`) is a separate pointer, not used here.

## 4. Open items (named)
- Cor-H in expectation with explicit tail rates (BASE BT1-A2; `STATEMENT.md:157-163`).
- CorGb-plus with sub-Gaussian candidate rows (TRIAGE `:41`, class B).
- Robustness of the selection beyond (OV^c) (boundary numerics N1 show no visible change; no claim).

## 5. Registry blocks

```
REGISTRY
claim: W3-MISR-R:CorG-min | kind: corollary | statement: STATEMENT.md:48-92 | premises: STATEMENT.md:25-46
status: PROVED (by this seat, unchecked) | status_source: lemmas/G1_min.md:4
assumptions: A:MISR-OVC (new | omitted contrasts Gaussian given the candidates | (N) Gaussian noise independent of the design and the omitted columns, and conditionally on the candidate design the contrasts of the omitted part minus a linear candidate predictor are N(0, tau^2(X) I) | STATEMENT.md:56-59 | shared no | bridge W3-MISR-R:CorG-min) ; A:MISR-OV (new | full-vector omitted-part condition | conditionally on the candidate design the omitted part is N(a 1 + X gamma, tau^2 I) | STATEMENT.md:67-68 | shared no | bridge W3-MISR-R:CorG-min)
conclusion: identity: (N) and the omitted-contrast condition give the contrast-law Gaussian residual condition conditionally on the candidate design, for any law of the candidate design; under Gaussian noise the condition is also necessary; Cramer partial converse; jointly Gaussian rows with singular candidate covariance are an instance | scope: every n, any candidate-design law
depends_on: W3-MISR:MIS(ii)@stmt
implies: W3-MISR:Cor-G(a) (jointly Gaussian rows with positive definite candidate covariance are instance (E1), with the parent's projected coefficient and variance)

REGISTRY
claim: W3-MISR-R:CorGb-plus | kind: corollary | statement: STATEMENT.md:94-108 | premises: STATEMENT.md:48-92 ; STATEMENT.md:164-186
status: PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, SOP:TH09, SOP:TH128, C-MIS:GDb | status_source: lemmas/G2_corr.md:4
assumptions: A:GAUSS-CAND-ROWS (new | iid Gaussian candidate rows | rows of the candidate design iid N(m, Sigma) with positive variances | STATEMENT.md:96-97 | shared no | bridge W3-MISR-R:CorGb-plus) ; A:MISR-OV ; A:CORR-FLOOR (new | sparse floor on the candidate correlation matrix | lambda_min(R_TT) >= c_R for every T of size at most s + max(j0, m#_n) | STATEMENT.md:102 | shared no | bridge W3-MISR-R:CorGb-plus) ; A:FIXED-S0 ; A:P-POLY
conclusion: posterior: E delta_n <= C r_n + (2 + 2 k_n) n^-2 + n^-1 and the same order for P(HPM != supp of the projected coefficient), under population conditions relative to the projected variance | rate: r_n = sqrt(log n / n) | scope: Gaussian candidate rows, 2 <= p <= n^A, s >= 1 fixed
depends_on: W3-MISR-R:CorG-min@stmt ; W3-MISR:MIS(ii)@stmt ; W3-MISR:Cor-G(b)@proof:G2-steps-1-5 ; C-MIS:GD(b)@proof:steps-1-2-and-failure-bound ; W3-POST2:A0@hyp
implies: W3-MISR:Cor-G(b) (jointly Gaussian rows give (OV); the covariance floor and variance bound give the correlation floor c_pop/C0; the diverging beta-min is one branch)

REGISTRY
claim: W3-MISR-R:CorH-plus | kind: corollary | statement: STATEMENT.md:110-132 | premises: STATEMENT.md:25-46 ; STATEMENT.md:164-186
status: PROVED (by this seat, unchecked), conditional on W3-POST2:D | status_source: lemmas/H1_plus.md:4
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY ; A:SEL-P (new | selection premise | 1 - posterior mass of the target tends to 0 in probability | STATEMENT.md:114 | shared no | bridge W3-MISR-R:CorH-plus)
conclusion: posterior: in-sample average Hellinger and Kullback-Leibler contraction of the parameter posterior around the projected law; with only the energy bound, the floor on the target and selection consistency: distance M_n / sqrt(n), KL M_n / n; without a margin (with the Occam-sum condition): squared Hellinger and KL at log n / n | rate: Hellinger M_n / sqrt(n) ; KL M_n / n ; squared Hellinger and KL log n / n | scope: fixed designs, sequences in the class; in probability
depends_on: W3-MISR:R'@stmt ; W3-POST2:D@hyp
implies: W3-MISR:Cor-H (the parent's class is contained in the floor-only class; with the parent's margin, MIS(i) gives selection consistency)

REGISTRY
claim: W3-MISR-R:CorH-U | kind: corollary | statement: STATEMENT.md:134-155 | premises: STATEMENT.md:25-46 ; STATEMENT.md:164-186
status: PROVED (by this seat, unchecked), conditional on W3-POST2:D, W3-POST2:C, W3-POST2:A0; clause (G) also conditional on W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128, C-MIS:GDb | status_source: lemmas/H2_uniform.md:4
assumptions: A:MISR-GRC ; A:MISR-ESNR ; A:POST2-F0 ; A:POST2-OS ; A:FIXED-S0 ; A:P-POLY ; A:SEL-P
conclusion: posterior: the contraction statements of CorH-plus hold uniformly over configuration classes (no-margin form over the Occam-sum class; selection form over any class with uniform selection consistency) and conditionally for random designs, with the Gaussian-row instance | rate: as W3-MISR-R:CorH-plus | scope: fixed designs uniformly; random designs by conditioning on any sigma-field
depends_on: W3-MISR-R:CorH-plus@stmt ; W3-MISR:MIS(i)@stmt ; W3-MISR-R:CorGb-plus@proof:G2-design-events ; W3-MISR:MIS(ii)@proof:M3-freezing ; W3-POST2:A0@hyp ; W3-POST2:D@hyp
implies: W3-MISR-R:CorH-plus (singleton classes)
```
