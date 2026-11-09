# R02 / R03 disposition (lemma checks, Codex gpt-6.1-sol; R02 high on L1–L3, R03 xhigh on L4–L5)

## R02 (L1–L3): VERIFIED-WITH-AMENDMENTS
Verdicts: Lemma R VERIFIED; MIS(i) VERIFIED; Lemma DR VERIFIED; MIS(ii) V-W-A; Prop P VERIFIED; GD(a) VERIFIED; GD(b) V-W-A;
Cor H VERIFIED; Cor D VERIFIED; D′ V-W-A.
| Amendment | Disposition |
|---|---|
| MIS(ii): spell out finite-n reading of 𝒜_n, deterministic starting index, BM envelope; thresholds not design hypotheses | APPLIED (L1.4 Hypotheses) |
| E Y_n → 0 via E Y_n ≤ η + P(Y_n > η), not "bounded convergence" | APPLIED (L1.4 proof) |
| Without-beta-min random-design version | APPLIED: (ii′) in L1.4 and STATEMENT §2 |
| GD(b): inherit Σ_𝒞𝒞 ≻ 0 and fixed σ_𝒞² (counterexample otherwise) | APPLIED (L2 GD(b) header, counterexample quoted) |
| GD(b): 𝒜_n by finite-n inequalities; M_n; starting index | APPLIED |
| DS citation: printed two-sided form has factor 2 | APPLIED (factor 2 used: 2k_n n^{−2}) |
| sums over 1 ≤ k ≤ min(p, k_n); K equality | APPLIED |
| D′: leakage needs a rate (h_n grows); simple M_n | APPLIED: δ² = O(n^{−7/6}) uniformly, E_{T,l} = O(n^{−7/12}√log n) → 0, NL_avg with κ = ¼; M_n = √n/(4σ_𝒞² log n) |
| Onset remark keeps "no universal n₀" meaning | Already worded as a disclosure (L1.2 remark (b)); no change of meaning |

## R03 (L4–L5): VERIFIED-WITH-AMENDMENTS for Theorem F, Cor F(a), Cor F(b), Lemma T, Lemmas S/O1/O2; L5 §2 consequence paragraph GAP + FALSE
| Item | Disposition |
|---|---|
| Lemma S reading: actual rate shift is (1 + 2b₀/N)c_n; the proof keeps b_y | APPLIED (L4.1 Reading) |
| "Supersets penalised at least as strongly" is a comparison of bounds, not of posteriors (c_n < 0 with positive prob.) | APPLIED (L4.7) |
| Sequences depend on p_𝒞 via m♯_n; dominating sequences depend only on constants (and C) | APPLIED (L4.3) |
| signalgain domain |S| ≤ m♯_n | APPLIED (L4.6) |
| Cutoff remark: n₀ may depend on C; not an arbitrary-cutoff version of (C9) | APPLIED (L4.9) |
| Cor F(a) empty-family boundary case | APPLIED (L4.8) |
| O1: GR restores well-specification, sparsity only by assumption | APPLIED (L5 §1, with the reviewer's dense example) |
| O2 citation: contrast mixture is IG(0.51, b′) with ridge slab | APPLIED (L5 §2; citations checked in CITECHECK) |
| O2 consequence paragraph: posterior-bound inference GAP; "vacuous for every m ≤ K" FALSE (duplicate-column counterexample at m = K − 1) | ACCEPTED; paragraph replaced by the reviewer's exact wording; "discharged only for bounded p_𝒞" corrected to include Lemma T / Cor F(b). STATEMENT §5 already only claimed the obstruction to the den′ strategy. |
| N3 / N3b are context, not tests of c₀ | Agreed; SUMMARY.md already says "consistent with"; no change |

Inequality-level falsification of L4 (Lemma S identity, ongood^𝒞 cores, Lemma T's uniform denominator and (B3) step):
numerics/check_L4.py (results in numerics/check_L4_summary.md when the run finishes).
