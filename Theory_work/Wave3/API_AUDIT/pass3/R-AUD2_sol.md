# R-AUD2 — independent review of six GAP findings

Reviewer: Codex gpt-6.1-sol, high reasoning effort. Date: 2026-11-11.
Only this output file was written; no git state was changed. Paths below are relative to the repository root. The brief's FAC-X path is stale: the source is `Theory_work/Wave2/W2-FAC-X/T2/L4r_path.md`, not `.../lemmas/L4r_path.md`.

## Verdicts

| Audit finding | Verdict | Effect |
|---|---|---|
| f20 Finding 1, S5F L0.2 multiplier | **CONFIRMED** | Strengthen the probability event; the asymptotic uses survive. |
| f20 Finding 2, S5F L0.6(b) | **CONFIRMED** | Add the null residual hypothesis; the BCS truth-move argument survives with the corrected L1.6 rate below. |
| f21 Finding 1, S5F L1.6 | **CONFIRMED** | Keep the additive factor term, and weaken the rate required in L0.6 to o(sqrt(n)); no growth restriction on p is necessary for truth exclusion. |
| f21 Finding 2, S5F L1.7 | **CONFIRMED** | Use the strengthened event and specify truth-containing sets. |
| f23 Finding 1, FAC-X L4r.5 | **CONFIRMED** | The all-m intermediate count is false, but the first displayed bound survives by a small-m/big-m split. |
| f23 Finding 2, FAC-X L4r.5 “in particular” | **CONFIRMED-WORDING** | A bounded remainder was omitted in the proof. The cited FACB constants already give strict slack, so the stated bulk conclusion survives unchanged. The alleged missing constant relation is rejected. |

## 1. S5F L0.2: missing lower energy bound

Source: `Theory_work/Wave2/W2-FAC-S5F/lemmas/L0_general_tools.md:25–30`, with the sharpened threshold reused at lines 126–129.

The event imposes an upper bound on total noise energy and a lower bound on the orthogonal residual r, but no near-n lower bound on total energy. Take an orthogonal exact-Gram design, p=floor(n/2), sigma=1, noise orthogonal to the truth columns, r about n/2, and total energy 0.6n. With A=S0 and zero truth-column noise, Phi(A)=0 and RSS_A=0.6n; M_A=5/6. The truth cross term vanishes. All inequalities of E0_n hold for large n, whereas the claimed upper bound tends to 1/2. These choices have neighborhoods of positive Gaussian probability. Their small probability does not rescue a deterministic assertion on E0_n. Thus the audit's counterexample is compatible with the event and model.

Minimal repair: replace E0_n throughout its uses by

    E0_n,* = E0_n intersect {||e||^2/sigma^2 >= n-1-n^(2/3)}.

Since ||e||^2/sigma^2 has chi-square(n-1) law, the extra event has probability tending to one. For A containing S0 with Phi(A)<=n/log n,

    M_A <= n/[2(n-1-n^(2/3)-n/log n)] <= (1+2/log n)/2

for all sufficiently large n. This fixes the sharpened L0.7 threshold and its L1.7 use. It also supplies the near-n lower energy control missing in the stated s^2 lower bound. No stronger assertion on the original E0_n is justified. All otherwise valid probability-tending-to-one downstream arguments can intersect with E0_n,* without loss.

## 2. S5F L0.6(b): TR does not control a null addition

Source: `.../L0_general_tools.md:95–114`. The statement at lines 95–101 assumes TR only; TR-prime first appears as a “provided” condition at lines 111–114. It is a genuine additional hypothesis.

A fully specified version of the audit's counterexample: let Sigma=I, sigma=1, p=floor(n/2), one truth j with theta_j^2=0.1, and T consist of j and one null with zero noise coordinate. For another null l outside T choose g_l^2=0.4n, all remaining design-noise coordinates zero, and r=(n-1-p). Then E0_n holds (total energy about 0.9n), the truth cross term is zero, and TR holds with zero truth residual noise at every relevant A. Nevertheless,

    RSS_(T\j union l) - RSS_T = 0.1(n-1)-0.4n < 0.

The swap has a positive order-n likelihood gain; its same-size determinant term is zero in this orthogonal design. The extra zero-noise null in T gives an improving null deletion, so even the comparison with a best null deletion is nonvacuously false. This verifies the counterexample. Strengthening E0_n alone does not imply TR-prime either: one can increase r so total energy is near n while keeping the same offending null coordinate.

Minimal repair for the printed rate: explicitly assume, for part (b),

    (TR') Z^2(l;T) <= (R'_n)^2

for every relevant T containing S0 and null l outside T, with R'_n=O(sqrt(log p)). For compatibility with all permitted BCS sequences after repairing L1.6, state both R_n=o(sqrt(n)) and R'_n=o(sqrt(n)) instead. These are sufficient for the two subtracted error terms in lines 110–112 to be o(n); part (a) also needs only R_n=o(sqrt(n)). The negative order-n gain and comparison with gains >=-log n remain valid. L1.6 supplies these weaker rates uniformly, without a path hypothesis. This repairs the truth-move input; it does not complete the unfinished S5F path theorem.

## 3. S5F L1.6: omitted factor term and unjustified rate

Source: `Theory_work/Wave2/W2-FAC-S5F/lemmas/L1_bcs_structure.md:97–105`. Its setting, lines 9–11, incorporates BCS and P; P is only p<=floor(n/2), not a lower growth condition. Even the “growing p” target in STATEMENT:12 does not imply the rate used here.

Choose p a multiple of q growing like log n; set eta=L_n and all group/idiosyncratic coordinates zero. This is in E_loc_n for large n, and T=empty gives Z_l(T)=g_l=sqrt(a)L_n. But R_loc is of order sqrt(L_n), so neither Z<=2R_loc(1+o(1)) nor O(sqrt(log p)) holds. Boundary values can be moved inward to give positive-probability neighborhoods. E0_n can also be imposed by choosing the independent r near its mean. Thus the slowly growing-p counterexample works; using fixed p is unnecessary.

Minimal event-preserving repair:

    R_n = R'_n := 2 R_loc + s_max sqrt(a) L_n
               = O(sqrt(log p + L_n) + L_n)
               = O(sqrt(log n)) = o(sqrt(n)).

Here q and the design parameters are fixed, and p<=n/2. The first inequalities in L1.6 prove this directly. Interpret residuals for arbitrary sets as the noise-only standardized residuals, as needed for TR; they are the RSS addition statistics for truth-containing sets and null additions.

Alternatively, (log log n)^2=o(log p) recovers the displayed asymptotic 2R_loc and the remark's 8 log p(1+o(1)). The remark at lines 103–105 must otherwise use the corrected bound or qualify its p regime. This correction preserves truth exclusion through the preceding o(sqrt(n)) repair. It does not, by itself, justify a uniform sharp coefficient 8 log p or complete C2/C3.

## 4. S5F L1.7: inherited event gap and domain

Source: `.../L1_bcs_structure.md:107–110`. The bound on Phi is valid, but the half-multiplier conclusion needs E0_n,* from section 1. State the conclusion for T containing S0 on E0_n,* intersect E_loc_n intersect the displayed max-|g| event. The latter event alone does not control the independent orthogonal noise energy. For sets missing truths the asserted RSS=noise-energy-minus-Phi identity is unavailable.

For a counterexample satisfying even the added coordinate event, use any admissible BCS design and take g=0, r=0.6n, p about n/2, T=S0. With g=0 the BCS representation can take eta=zeta=xi=0. Then Phi(T)=0, every local/coordinate bound holds, and E0_n holds, while M_T=5/6. Choose the independent r in a neighborhood of 0.6n. No orthogonality assumption on Sigma is needed in this construction. The sharpened conclusion survives on the strengthened event.

## 5. FAC-X L4r.5: all-m count is false; the displayed bound is repairable

Source: `Theory_work/Wave2/W2-FAC-X/T2/L4r_path.md:208–225`. The cited source actually exists: `Theory_work/Wave2/W2-FAC-B/lemmas/L4_path.md:95–118`. It explicitly assumes bulk m>=m1; its count argument at lines 113–114 uses this. Quoting it “verbatim” for every class count is invalid.

The audit's small-m counterexample checks out. In one class let the ten largest absolute coordinates be positive and the eleventh negative, with K consisting of ranks 1 and 11. This sign event has probability 2^-11. Write their magnitudes u1>u11. Then a=-u11, b=u1, K=N\(a,b), m=2, J=11>5m. For a polynomially growing class, u1-u11 tends to zero in probability. Independently choose rho<=-1 (its bounded truth/factor-noise distribution gives a fixed positive probability); then

    X = [ell' epsilon (u1-u11)-rho]/(kappa'_S+2ell'^2)
      >= 1/(kappa'_S+2ell'^2).

For large n the centre ell X lies between a and b and 0<a+b<4ell X. The last inequality is exactly X>|2ell X-(a+b)|/(2ell)=Delta/(2ell). E_n and the actual E5 bounds have probability tending to one, so intersecting them does not remove this fixed-probability obstruction. Finite-rank sign imbalance is allowed by E5 as L_n grows. Thus the counterexample respects the full static hypotheses, not merely an arbitrary top-rank selection.

Minimal repair preserving the FIRST DISPLAY FOR ALL m: insert the following argument separately for each class (write m=m_c, x_u=2log(u+1)+L_n).

* If m<=10x_(5m), E3' gives sum_K xi <= m Hbar <= Hbar sqrt(10m x_(5m)). No claim about J is needed.
* If m>10x_(5m) and J>5m, x_J/J <= x_(5m)/(5m)<1/50; x_u/u is decreasing for u>=1 once L_n>=2. E5's exact count bound (`FAC-B/lemmas/L3_event.md:26–27`) implies the negative count in Top(J) is at least J/2-sqrt(Jx_J/2)>0.4J>m. But these are precisely the kept negatives, at most m. Contradiction. Hence J<=5m, and sum_K xi<=D_J<=Hbar sqrt(2Jx_J)<=Hbar sqrt(10m x_(5m)).

The a>=0 case, weighted sum, and division already printed remain valid. Thus the first display and its bulk consequence survive. Restricting the lemma to m_c>=m1 would also work, but would unnecessarily discard the valid all-m first display. The standing event E_n must accompany E5_c. Probability tending to one for the per-class sign totals requires diverging class sizes; this holds in the polynomial counterexample, and in every nonvacuous bulk application.

## 6. FAC-X L4r.5: bounded remainder is absorbed by existing constants

The proof at lines 224–225 omits the contribution

    B_n = C_rho L_n/(kappa'_S + sum_c ell'_c^2 m_c).

With every m_c>=ceil(K1 L_n), B_n=O(1), not necessarily o(1). The audit is correct about this intermediate estimate. It is not a counterexample to the final bound.

The allegation that K1 and epsilon_b are undefined/unconstrained in the cited material is false. `FAC-B/lemmas/L3_event.md:14` specifies epsilon_bal=1/50 and K1=100/epsilon_bal^2=250000; `FAC-B/lemmas/L4_path.md:97` sets epsilon_b=epsilon_bal. FAC-X L4r.5:216 explicitly says “FACB constants,” and line 225 cites that very proof. Therefore

    sqrt(11/K1) = (sqrt(11)/10) epsilon_b
                < 0.34 epsilon_b.

Minimal proof repair: retain B_n and write

    X_T <= sqrt(11/K1) Hbar/ell'_lo + O(1).

Since ell'_lo=ell_lo(1+O(n^-2)), Hbar=O(sqrt(log n)) and Hbar tends to infinity, the strict gap (0.34-sqrt(11)/10)epsilon_b Hbar/ell_lo absorbs the bounded term and the ridge correction for large n. In fact X_T<=0.34 epsilon_b Hbar/ell_lo eventually, so the stated +o(1) version follows. No new constant hypothesis is required. If one replaces “FACB constants” by arbitrary constants, then strict slack must indeed be added; equality would not justify this absorption. Verdict: CONFIRMED-WORDING, not a substantive GAP in the bulk conclusion.

## 7. Dependency and chapter impact

I inspected `Theory_work/INFRA/registry/claims.tsv` in both depends_on and premises, normalized ticket-local references, and searched Theory_work source references (including FINAL). `git grep` was used read-only; `git ls-files --others --exclude-standard -- Theory_work` returned no additional untracked sources before this output was created. Search terms included S5F, L4r.5, L4r_path, and both S5F source filenames; FINAL was also checked for FAC-S5, FAC-GL and L4r. No FINAL chapter source references these inputs. Forward dependencies on FAC-B are not reverse dependencies of FAC-B on the stopped tickets.

### Registry claims

| Claim(s) and registry lines | Reliance and impact |
|---|---|
| S5F:L0, line 217; S5F:L0.L0.2, .6, .7, lines 294, 298–299 | Direct affected components. L0.2 event, L0.6 hypothesis/rate, L0.7 sharpened threshold need the repairs above. |
| S5F:L0.L0.3, line 295 | Uses L0.2's event for the general RSS/gain bridge; strengthening the event preserves it. This finding does not invalidate the general multiplier bound. |
| S5F:L0.L0.1, .4, .5, lines 293, 296–297 | Same aggregate lemma file but not dependent on the defective sharpened bound or missing TR-prime; exact identities survive. |
| S5F:L1, line 218; S5F:L1.L1.6 and .7, lines 306–307 | L1.6 rate and L1.7 event/domain need repair. |
| S5F:L1.L1.0 through .5, lines 300–305 | Structural/noise identities and configuration counting are in the aggregate input; these findings do not damage those statements. L1.3's jump identity uses the sound L0.4. |
| **S5F:C1, line 213** | Explicit depends_on L0;L1 and FAC-B:L2.4. The start-mode claim uses structural inputs, not the defective sharp multiplier or truth-out swap step. Repairs preserve the relevant tools; this review does not certify the still-unlocked claim. |
| **S5F:C2, line 214; S5F:C3, line 215** | depends_on is the local shorthand **`L0; L1`**, not fully qualified IDs. These are additional consumers missed by an exact-ID-only search. Bulk/end claims rely on gain thresholds and truth exclusion. Repairs preserve those inputs, but L2–L5 proofs are absent and R01 rejected the statement lock; these claims remain unfinished. |
| **S5F:C4, line 216** | Explicit L0/L1 dependency and method assembly from C2/C3. H0 part (i) uses the eigenvalue lower bound and is unaffected by these findings; parts (ii)–(iii) still await the unfinished path/start assembly. |
| FAC-X:L4r.5, line 230 | Directly affected proof, repaired above. **No other registry row depends on L4r.5**, including through premises. |

All S5F C1–C4 status fields are empty; L0/L1 and their split rows are author-only/unchecked. FAC-X:L4r.5 explicitly says unchecked and not used by FAC-GL. No PROVED-CHECKED registry claim is reachable as a consumer of these three inputs. The parent rows include their split subclaims as statement dependencies; the split rows should be inspected as components, not treated as independent checked results. The premises field confirms their source locations and introduces no hidden checked consumer. FAC-X:L4r.4 premises point to lines 173–178, not L4r.5.

### Source passages and restatements

* **S5F STATEMENT.md:14–26, 54–72, 76–104:** route/tools, thresholds, C1–C4, and C5's configuration-bound frontier discussion. The half-multiplier use and claimed uniform trivial-centre rate require the repairs above. C5's 1/6 discussion needs the p-regime qualification from section 3. C2/C3/C4 are targets, not established consequences. `PLAN.md:6–24` and `CHECKPOINT.md:16–64` repeat the intended tool/path/assembly route; `LOG.md` records work, not a new theorem. Existing `reviews/R01_statement_lock_sol.md`, especially items 7–9, already identifies unfinished path and slow-p obligations. Repairing these six findings does not resolve those independent objections.
* **FAC-X T2/STATEMENT_T2.md:64–72:** section 4 restates L4r.5 as a small-constant max bound but omits **every m_c>=m1** as well as some full static hypotheses. **This passage needs qualification:** retain the full E_n/E5_c, interval-hole and two-sided hypotheses, and add the bulk condition; otherwise state the all-m first display instead. It is an author-only ticket statement, not a FINAL chapter theorem.
* **FAC-X T2/NOTES.md:27:** same abbreviated max bound and same omitted bulk restriction; restore the full conditions. `T2/NOTES.md:37–40` and `T2/L4r_path.md:227–241` use the conditional centre-bound route to diagnose failure of the path induction. That obstruction survives; these passages cannot assert an unrestricted small-constant bound outside the bulk/static domain.
* **FAC-X REPORT.md:170:** status summary of L4r.4/L4r.5, explicitly not used by FAC-GL. Its L4r.5 proof certification needs the repairs, but the repaired lemma survives. `REPORT.md:183–193` discusses the failed per-class route; it does not use L4r.5 to prove FAC-GL. `T2/numerics/N_T2_summary.md:51` describes the conditional bound as numerically unhelpful, not an independent proof; retain the hypothesis qualification there too.
* **FAC-X FAC-GL / L4r-S, X9, X10:** the theorem's actual cited path inputs are L4r.0–L4r.3 (`STATEMENT_T2.md:83`, `REPORT.md:168`, X9's proof transfer). They do not consume L4r.5. `reviews/R11_L4rS_X9_check_sol.md:4` excludes L4r.4–6; `reviews/R17_T2_council_sol.md:7` likewise excludes these extensions from accepted theorem inputs. Thus neither the checked earlier sections nor the FAC-GL assembly inherit this gap.
* **Theory_work/INFRA/FAILED_ROUTES.md:100,104–106**, SR critiques/adjudication, SIM/S5's brief, UNI's frontier table (`W2-UNI/lemmas/L6_frontier.md:42`), UNI's prospective assembly discussion, and Wave3/PROGRAM.md:37 mention these stopped tickets or the failed route. These are inventories, planning, conditional mappings or negative diagnoses, not proofs importing L0/L1/L4r.5. No additional proved consumer is present there. Registry/falsification and historical review references similarly do not create theorem dependencies.

**Impact conclusion:** genuine gaps are confined to unchecked tools and unfinished ticket claims. HQ's C1/C4 list must be expanded to C2/C3 because of local dependency notation. Two FAC-X ticket summaries need the omitted bulk/static qualifications. No PROVED-CHECKED claim and no FINAL chapter statement is affected by these findings. All six local uses can be repaired as specified, but that does not upgrade the stopped S5F programme or prove the failed general-loading path extension.
