# supersede W3-MISR:Cor-G(a) (by W3-MISR-R:CorG-min)

- reason: HQ GO real run (task Q, H5 card 10, 2026-11-16): free supersession (CorG-min implies Cor-G(a), STATEMENT §8 row 181, statement lock L1:59)
-  [W3-MISR] v1.0.0 state ACTIVE; status `PROVED-CHECKED, conditional on C-MIS:Prop-P; input versions C-MIS:Prop-P@1.0.0; council R2, MANIFEST 217d6708dfee945fa0416171268e08e359e0e7a`
- replacement W3-MISR-R:CorG-min:  state ACTIVE; status `PROVED-CHECKED, conditional on SOP:TH09, SOP:TH128; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13d`
- axes (Y vs X): {'assumptions': 'incomparable', 'conclusion': 'equal', 'rate': 'equal', 'scope': 'unknown'} -> **undetermined**
- decision-rule class: **free**

## Statement diff

- hypotheses ADDED (each dependent must now verify them or the property it consumes): A:MISR-OV (full-vector omitted-part condition), A:MISR-OVC (omitted contrasts Gaussian given the candidates)
- hypotheses DROPPED: A:IID-GAUSS-ROWS (Iid Gaussian rows)
- conclusion: `identity: jointly Gaussian rows give the contrast-law condition at each n, with deterministic projected coefficient and variance sigma^2 + tau^2, for any n-dependence of the parameters` -> `identity: (N) and the omitted-contrast condition give the contrast-law Gaussian residual condition conditionally on the candidate design, for any law of the candidate design; under Gaussian noise the condition is also necessary; Cramer partial converse; jointly Gaussian rows with singular candidate covariance are an instance`
- scope: `example (Gaussian rows)` -> `every n, any candidate-design law`
- statements: Theory_work/Wave3/W3-MISR/STATEMENT.md:164-170 -> Theory_work/Wave3/W3-MISR-R/STATEMENT.md:48-92

## Rebuild cost

- free: 1 re-point(s) PROPOSED (one cheap check each), no rebase, no re-review

| dependent | uses | action |
|---|---|---|
| W3-MISR:Cor-G(b) | stmt | propose re-point |
