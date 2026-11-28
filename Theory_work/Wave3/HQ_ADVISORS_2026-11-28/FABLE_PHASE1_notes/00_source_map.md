# Fable Phase 1 — source map (working notes)

Checkout: `_wt/hq_advisors`, detached `dept/theory @ 40febfb6`.

## Where the proofs behind the paper's three theorems actually live

| Paper result | Internal label | Proof files | In this checkout? |
|---|---|---|---|
| Thm 3.1 (density) | `thm:dist` (W3-DIST Thm A) | `Theory_work/Wave3/W3-DIST/STATEMENT.md`, `lemmas/X.md`, `lemmas/NEC.md`, `lemmas/DIST12.md`, `work/*` | yes |
| Thm 3.2 (selection, fixed effects) | `thm:post-random` | chain: `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`, `T03_A2_selection_consistency/PROOF_v2.tex`, `Theory_work/Old_Projects/.../W1-T03R/PROOF.md` (T03-sharp), `Wave3/W3-POST/STATEMENT.md` (fixed design Thm 1), `Wave2/W2-APP/lemmas/L1_POST.md` (Gaussian rows), `Wave3/W3-D3/lemmas/ASSEMBLY.md` + `B3w.md` (sub-Gaussian rows, Thm 2SG) | W3-D3 and W3-D2 are **only on `main`**, not on dept/theory@40febfb6 |
| Thm 3.5 (omitted Gaussian predictors) | `thm:omitted` | `Wave1C/C-MIS/lemmas/L1–L6`, `Wave3/W3-MISR/lemmas/R_reduction.md`, `M_misr.md`, `Wave3/W3-POST2/lemmas/A_occam.md`, `C_expectation.md`, `E_visibility.md` | yes |
| manuscript statements | or5/or6/supplement_or | `Docs/Writing/manuscript/sections/*` | **only on `main`** |

Route map with line anchors: `Theory_work/Dept/prep/TH_PREP_support/W2_ROUTES.md` §R1–R3.

## Audit notes (running)

### T03 `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` (read in full)
- Fixed design, conditional on X. Hyps: G (Gaussian noise), R (p<=n^A, ||mu||^2<=nM, s0<=K), SE (sample floor lambda_min(G_T)>=N*phi0^2 for |T|<=m_n+s0, m_n<=C_m log n, l.35,47,171), BM-C: min theta_j^2 >= M_* sigma^2 log n/(n phi0^2) (l.342-346), H-T02 size tail (l.336-340).
- ALREADY a threshold-scale beta-min theorem (beta_min ~ sqrt(log n/n)) with a large constant M_*=2L_*+1, L_*>=max{4C_*,32[s0(A+1)+2]}, C_*=2s0+3[A j_*+s0+log(j_*+1)+1] (l.194, 346). s0=5,A=2: M_*~1553 -> beta_min >= 39.4 sigma sqrt(log n/n)/phi0.
- Where the fixed floor is really used: (a) Lemma signal l.146-152 on S'=S u S0 with |J'|<=j_*  => sets of size <= s0+j_*, j_*>=(2A+1)s0+1 (l.329); (b) Occam factor Lemma det l.122-128 and smoother (c) l.99,107 on sets up to m_n+s0 -- but there any floor g with (n+1)g >~ 1 (i.e. NEC scale) gives the same bounds up to constants: f(g)>=(n+1)g/(g+1); eta_n=1/((n+1)g); rho_n becomes O(1) not o(1).
- Lossy steps (constants): (G4) l.179,194 crude chi2 union; V_S>=Delta_S/4 l.311; min(V/8sigma^2,n/5) l.287,300.
- Correct as read; no gap found. Lemma chi(b) l.158: truncated exp moment exact.

### KEY FINDING: selection with threshold beta-min + fixed floor on O(s) sets is ALREADY PROVED (fixed-design core + bridges)
- `Theory_work/Wave3/W3-POST/STATEMENT.md` l.61-104, Theorem 1 (council-passed C3): hyps (E) l.67, (F_lambda) fixed floor phi0^2 on S0 u J, |J|<=j0=ceil((2A+1)s0)+1 l.68-70, (F_w) unnormalised floor g0 on S0 u J, |J|<=m#_n=O(log n) l.71-73, (BM) BM-inf or BM(c): theta_min^2 >= c sigma^2 log n/(n phi0^2), c>c0(s0,A)=max{4C_*,32[s0(A+1)+2]} l.74-75. Concl items 1-4 (rate r_n, HPM=MPM=S0, PIPs), item 6 random-design interface l.95-100, item 7 lower bound 1/(1+sqrt(n+1)).
- Proof: `Old_Projects/.../W1-T03R/PROOF.md` §4 Lemma B l.137-142, §5 T02(ii#) l.146-157, §6 T03# (C1)-(C10) l.161-209 (diff against T03 PROOF_v2 and T01_T02 PROOF_v3). Read; sound. Status: "T03#: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)".
- Bridges from population assumptions (variance-relative sub-Gaussian + NEC + bounded signal): `Wave3/W3-DIST/STATEMENT.md` §3 B1, B2-core, B2, B3 (l.~395-417), proofs `W3-DIST/work/E_bridges/B*.md`, all VERIFIED (DEPS.tsv). B3: fixed floor psi on sets <= (2A+3)s+2 => (F_lambda) with phi0^2=psi/4; (F_w) with g0=c_psi/8 from NEC; BM-inf envelope. Needs only a BM(c) variant: theta_j^2 = s_j^2 beta_j^2 >= Var(x_j) beta_j^2/2.
- So paper Thm 3.2's "floor on 5(A+1)(s0+1) log n sets + fixed effects" is WEAKER than what is proved. W3-D3 (sub-Gaussian Thm 2SG; only on main) is not needed.
- Constant: bbmin^2 >= 8 c log n/(n phi^2), c>c0. s=5,A=2: c0=776 -> bbmin >= 78.8 sqrt(log n/n)/phi. Conjectured sharp-ish (Remark, C-ii): (1+eta)(1+sqrt(ubar_s)) sqrt(2 log(2p sqrt(n+1))/n)/phi.
- Lean/BVSCert is a stub (Basic.lean, 10 lines). Old sorry-free snapshot: Old_Projects/.../L-LEAN (hpm_eq_truth, markov_half, T07Bayes...).

### W3-DIST (density) status
- DEPS.tsv: DIST-1, X, X', T, H, S, V, B0-B3, R/Theorem-A all state OK (cross-family line checks). ERRATA E1-E8 editorial only.
- Theorem A = DIST-1 (fixed-design Lemma X under (E),(C),(ND)) + Lemma T (distribution-free VC transfer in-sample -> population Hellinger) + Lemma H + bridges B0 (scale), B1, B2. Includes size clause (ii): Pi(|S|>s+C1 M) <= n^{-cM}.
- Prop NEC: without (ND) exponential form at sharp radius is false (fixed design) -> A5 is needed for Thm 3.1 as stated.
