# Working notes (W1-T24G) — chronological, unreviewed

## 2026-11-02 first numerics (scripts/bvs_engine.py, simulate.py; seed 20261102; design seed 1)
Small-p mimics: p = 20 (4 groups of 5), s0 = 4 (one truth per group, gen_dev_data.R pattern with step 1),
n = 200, scales c in {1, 0.5}, B = min(14, 4, 16) = 4, m = p + B + 2 = 26 labels, H = L + 4 = 12.

pi0 mass by (#missing, #extra): S1 near S0; S2 supersets with 1-3 extras (pi0(S0) ~ 1e-6);
S3/S4/S6 supersets with 3-7 extras (pi0(S0) ~ 1e-11 .. 1e-36) [double-counted look-alikes across split groups];
S5 missing 2 truths with 2-3 extras (masked; pi0(S0) ~ 1e-16 .. 1e-19). pi(S0) ~ 0.72-0.78 in all.

Uniform sups over R_{2,2} (S5, c=1): sum_e sup_Y P(exit at Y) = 20.95 (most Gibbs labels have sup = 1 at
boundary states |P| = d with a missing truth whose look-alike is then added). => H24's uniform exit input is
false for this design (eta ~ 1 per label). First-change progress P*(x): min 0.098, pi0-weighted 0.139.

Simulation from 3000 raw pi0 draws (not S0), 12 terminal rounds, actual K_1:
| design | P(scored round 1) | within 2 | within 12 |
| S1 c=1 | 0.906 | 0.992 | 1.000 |  S1 c=.5 | 0.852 | 0.977 | 1.000 |
| S2 c=1 | 0.664 | 0.922 | 1.000 |  S2 c=.5 | 0.712 | 0.931 | 1.000 |
| S3 c=1 | 0.429 | 0.840 | 1.000 |  S3 c=.5 | 0.424 | 0.858 | 1.000 |
| S4 c=1 | 0.417 | 0.846 | 1.000 |  S4 c=.5 | 0.437 | 0.831 | 1.000 |
| S5 c=1 | 0.107 | 0.664 | 1.000 |  S5 c=.5 | 0.121 | 0.688 | 1.000 |
| S6 c=1 | 0.390 | 0.821 | 1.000 |  S6 c=.5 | 0.452 | 0.847 | 1.000 |

## 2026-11-02 later
- results/counterexample_H24.json: worst boundary state of R_d (d=1,2) one-round exit probability (simulated,
  20000 reps): S1 0.16-0.22; S2 0.62-0.79; S3 0.83-0.94; S4 0.80-0.98; S5 0.83-0.97; S6 0.72-0.97.
  (L+4) x exit = 1.9 .. 11.8.  => H24's uniform exit input fails at n = 200 in every design (CE1).
- results/compare_cprime.json: per-round progress (actual round, MC) vs constants. Phase 2 worst states:
  actual 0.75-0.89 vs P* 0.53-0.57, c2 0.30-0.46, c_poly 0.27-0.34, floor 1/(B+3) = 0.143.
  Phase 1 (pi0-mode incomplete starts): c1 = 1.000 (uniform addability exact), actual progress ~1.000; eta1 1.2-3.3.
- First scaling runs (single seed): eta2(a=1) 0.37-0.64 (n=200) -> 0.12-0.23 (n=800..12800); heavy-tailed
  (one null with large partial Z dominates); replicate study in results/scaling_reps.json.
- Bug fixed: eps_add quantifier must be over states with the same missing set (Prop. B1); code and PROOF.md fixed.

## 2026-11-02 final stretch
- Gap found and fixed in Prop. B1: truth-for-truth swaps / independence jumps can keep |M| but change the
  missing set; every truth removal is now classified bad (code + PROOF.md). All tables regenerated after this.
- Error found and fixed in the asymptotic table: superset leakage over S_a needs NL0(a) already at a = 1
  (partial-Z inflation Z_{l|S0+l'} for correlated nulls); only leakage at S0 itself is automatic.
- Cor. P1 (distance-one scoring): rigorous a1 >= 0.14..0.44 at n = 200 (results/distance_one.json).
- Prop. D (drift form) added.
- One commit ("classification precedence") lacks the attribution trailer; amend + force-push was refused
  by the environment's safety policy, so it was left as is.
