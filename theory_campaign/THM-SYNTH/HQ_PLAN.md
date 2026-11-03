# THM-SYNTH — HQ_PLAN: per-theorem HQs for the v1 list

Run THM-SYNTH, 2026-11-03. Item 5 of the task. Each HQ = one main theorem or a tight cluster from `THEOREM_LIST.md`,
looping to a referee-checked (cross-family) proof and a Lean certificate for its finite core. Cost classes: **S** ≤ 3
agent runs (assembly, one proof page, one Lean file); **M** 4–8 runs (one real proof obligation + its cross-family
review + Lean); **L** > 8 runs (an open crux). Statuses are those of THEOREM_LIST and are never upgraded here.

## 1. The v1 HQs

### HQ-VALID (G1: V1–V4) — Theorem V, Props W/W-cal/P, Lemmas S/RO
- **Scope.** One statement of fixed-data validity of v3.1 for any declared R (V1), the worker-equivalence propositions
  (V2), the pooling rules and the "R fixed in advance" rule (V3, V4). Main text: V1 as a Proposition with cited proof +
  V3(i)–(v); supplement: V2, V4.
- **Inputs.** T12, T31(i) (locked); Prop 2(a)–(e) (locked; A-REV4 wording GAP); METH-AUDIT PROOFS (Lemma S, Prop W, W-cal,
  Prop P); IND-T; F-MASKPIP M1 (XF VERIFIED); V5 kernel facts (no registry row).
- **First concrete step.** Write the missing V5 lemma (each elementary move is γ_φ-reversible; a uniformly random order of
  reversible kernels is self-adjoint and q_φ-invariant) as a registry row, and restate T12/T31(i) in R-island form with the
  hypothesis list (EX-A, EX-S, CAL, V5, R declared). In parallel: independent code check of Prop W's two facts (scorer
  statelessness; ledger write-only inside an island) and the W-cal bitwise replay (≈ 1 h on Owls per METH-AUDIT).
- **Lean.** Lemma S (top-c order independence; finite); Prop P(iv) (identity with 1 − 1/R); Prop P(iii)'s deterministic
  step; extend T12Core by discharging `hstep` for multinomial resampling + an invariant kernel (L-LEAN `T12_PLAN.md`).
- **Risk.** Low. Only risk: the W-cal replay fails bitwise (then W-cal is downgraded to "law-preserving" and the calibration
  stays serial in the parallel layer).
- **Cost.** S.

### HQ-START (G4: S1, S2) — Theorem 2, Theorem SEP, Lemma KL
- **Scope.** Thm 2 = T22(i)(ii)(iv) + T27(i) (+ DIL identity) in the main text; T22(iii)/FAV in the supplement; Theorem
  SEP (SEP-A/B) + Lemma KL + the Chatterjee–Diaconis corollary as "why one-shot correction fails"; the E-SPINE wording
  discipline ("moving off the start is needed, not tempering").
- **Inputs.** Locked T22, T27; Thm3/4-EXP (XF VERIFIED); DIL-E/E1/R/N (XF VERIFIED; DIL-DM(i) ERROR excluded); SEP-A/B (XF
  VERIFIED); W1-EXP Thm 5 (LH); CD18 Thms 1.1–1.2.
- **First concrete step.** Write Lemma KL with its two-line proof and the corollary "exp(KL(π‖π₀)) ≥ ½Q*^{1−δ₁}e^{O_P(1)} on
  LH"; Lean-certify Lemma KL and the DIL identity (both finite). Then the restatement of Thm 2 with the "never combine (b)
  and (c)" rule.
- **Lean.** Lemma KL (finite KL, log-sum inequality); DIL identity (−log π₀(S₀) = V + C − log A on a finite partition);
  T22(i) product inequality.
- **Risk.** Low; the only live mathematics is Lemma KL (elementary) and the labelling of DIL's verified parts.
- **Cost.** S.

### HQ-SELECT (G6: R1–R5) — Theorems 1, 3, 4, 5 and Proposition 1
- **Scope.** Assemble the selection spine for v3.1 = v3 + LS0: R1 (T03♯, disclosed as asymptotic), R2 (remark), R3
  (Theorem A + LS-score + Lemma M), R4 (T21(C1)/T38(0)/N200/Lemma RO), R5 (T38 (0), (a), (b1-LH) headline with LS0,
  (b2-LH) on A-REV7's subfamily without LS0, (c) polynomial cost with the rate GAP disclosed).
- **Inputs.** `T38_STATEMENT.md` v3; `LOCKABLE_v2.md`; W6-FIXREV2 statements; A-REV2/5/7/8 verdicts; API-N200; API-VSTAB;
  O-LS0 (0/2,394); L-LEAN (T21, T07, T11, T37 sorry-free).
- **First concrete step.** HQ/Felipe decide the Thm 5 headline (recommended here: (b1-LH) with LS0 as the method's theorem;
  (b2-LH) subfamily as the no-LS0 corollary covering the study's fits) and the output convention (strict 𝒪). Then one run
  writes the paper-form statements with the premises attached exactly as in LOCKABLE_v2's last column, and one run extends
  Lean: N200 Lemma 1 + Theorem N200 (same finite set argument as t21_C1), LS-score's move count on T37Lattice.
- **Lean.** N200 (finite), LS-score (finite), the (b1-LH) eligibility chain's deterministic parts (S̃₀ = S° given (M1);
  Lat membership).
- **Risk.** Medium on wording only: the c = 2 clause (V18), the T32(i) rate GAP, the "first finite-n" wording
  (Hou–Wang–Atchadé), the D1 positioning sentence (REPORT §4). No open mathematics for the v1 scope.
- **Cost.** M (assembly across many sources + two Lean files + one cross-family read of the assembled statements).

### HQ-ISLAND (G2: A1, A3, A4-P1) — Theorem H (bounded functionals, joint inclusion), Theorem Z𝒯, PIP bias bound
- **Scope.** Prove Theorem H (a)–(c),(e) and state (d) with R_n as a hypothesis; fold Prop P(iii) and the truncation
  variant into it; attach Theorem Z𝒯 (P3) and P1 as the deterministic companions. This is the HQ that closes THM-INV gap
  §5.1 (joint inclusion / general E_π[h]) and objective (1).
- **Inputs.** V1 (HQ-VALID); F-MASKPIP M1/M2 (XF VERIFIED); **M3 is XF ERROR (THM-INV) and must not be cited**: the E[W²] ≥ 1/P(crossing)
  remark uses Cauchy–Schwarz + M2 instead (THEOREM_LIST A1(v)); W2-T26 Lemma 3 (T15 at a terminal-round prefix, VERIFIED);
  MASKZPIP P1, P3; Maurer 2003; Hoeffding; T03♯.
- **First concrete step.** Write and verify the islandwise identity E[W_r ĥ_r | 𝓒] = π(h) for the measured-round plain
  average of a bounded h from locked T12/T15 (this is the crux of Theorem H(a); for h = PIP it is Prop 2's identity). Then
  copy M1's proof with h, and Prop P(iii) with e_r = |ĥ_r − h(S₀)|. Exact-enumeration check at p ≤ 12 on LH with joint
  inclusion of the linked pair.
- **Lean.** The deterministic inequalities of H(a) (|ĥ_r − h(S₀)| ≤ off-fraction) and H(b)'s finite step; the identity
  once T12Core's `hstep` is discharged.
- **Risk.** Medium: the RB version's drift terms (c_h) may need M1's exact bookkeeping; the n → ∞ clause (d) is only as
  good as the R_n hypothesis (E[W²|𝓒] unbounded above). The paper must disclose the lower bound E[W²] ≳ 1/P(crossing) (Cauchy–Schwarz + M2).
- **Cost.** M.

### HQ-DEPTH (G3: D1, D2, D3) — Theorem D (work/depth/width), Theorem STG, Theorem CD
- **Scope.** The cost model in score units; Prop D's depth free of N, H, R; the stage laws (Theorem G, STG-F, STG-M ideal
  grid, item 4 cited) with T ≤ T_e as the as-coded guarantee; the Song–Liang §6 column; the assembled Theorem CD in the
  scope of REPORT §3.
- **Inputs.** METH-AUDIT Prop D and §2; O-STAGES (Theorem G, STG-F/M, item 4; A-REV9 on STG-M); API-T26BUD Theorem G;
  SL digest §4; LIT-PAR §3.3 (units, wording to avoid); the METH-AUDIT §6 measured table (**not yet filled in the branch
  file; must be filled or the measured claims dropped**).
- **First concrete step.** Fill METH-AUDIT §6 (the per-round ms and the island depth at p = 500/1000 from the bitwise
  replay logs) or drop every "measured" sentence; write Theorem D with the SL column in one table; Lean Lemma RS + Lemma 1
  + Theorem G(i)–(ii).
- **Lean.** Lemma RS (log-affinity identity), Lemma 1 (convexity ⇒ monotone frontier), Theorem G(i)–(ii) (greedy
  optimality for a monotone interval predicate); Prop D's counting identity (optional).
- **Risk.** Medium: the as-coded masked T_n law is Conjecture P (OPEN); v1 states STG-M on the ideal two-state grid and
  the deterministic cap. If a referee demands the as-coded law, this becomes HQ-STAGES-2 (v2, L).
- **Cost.** S for D1/D2 as they stand + Lean; M if the measured table must be regenerated (NOTS runs).

### HQ-SL (G5: C1) — Theorem SL (analytic separation from split-and-merge on LH)
- **Scope.** C1(a)–(e): isolation probability, the exact-Gram orthogonal-null lemma, PIP → 0 under SL's priors, SL's
  output cannot contain the hub, v3.1 succeeds on the same family (citing HQ-SELECT and HQ-ISLAND), the clustered-split
  remark; re-run of the numerical seed on the W1-EXP LH family.
- **Inputs.** SL JRSS-B text (Thm 4, Cor 2, eq. (19), Condition 5, §3.1, §6, §7; SL digest); W1-EXP §4 (LH); LIT-PAR note
  09 + `sam_lh_demo.py`; R5 (b1-LH)/(b2-LH); `scripts/check_lemmas.py` (this run: (a) and (e) checked numerically).
- **First concrete step.** (1) Re-run `sam_lh_demo.py` on LH with g ∈ {1, 4}, K ∈ {2, 4, 8}, n ∈ {200, 800}: expect the
  failure rate ≈ P(isolated) × (1 − o(1)) and retention when the group is present (C1(e)). (2) Prove the orthogonal-null
  PIP → 0 lemma for SL's prior (known σ² first, then IG) — one page. (3) Decide the Stage-1 rule in the theorem (fixed
  threshold vs FDR rule) and obtain SL's supplement (Theorem S) if the FDR version needs it.
- **Lean.** C1(a) (hypergeometric sharing probability; finite), C1(b)'s identity x′μ = 0 and orthogonality on Σ_LH, C1(e)'s
  equicorrelation inverse entry. The PIP → 0 step stays cited/prose.
- **Risk.** Medium: (i) SL's FDR rule and the α₁ "large to avoid losing true predictors" might select a null-like column
  with small but nonzero probability — the theorem must be for n → ∞ at fixed design, where PIP → 0 beats any fixed
  threshold; (ii) the exact-Gram assumption makes x′μ = 0 exact; LH-iid needs concentration (v2); (iii) a referee may
  object that SL never claimed robustness to cancellation — answer: Condition 5 is their stated condition and we show it
  fails *exactly*, not approximately.
- **Cost.** M.

### HQ-EVID (G2: A2) — Theorem Z (what Ẑ can and cannot do)
- **Scope.** A2(i)–(v): unbiasedness (cited), the exact variance identity (O-PW2 A), the masked lower tail (E1/E2, N(a)),
  the run certificate (C1, E1c), the favourable consistency (T26-ThmA as a remark). No two-sided masked claim.
- **Inputs.** O-PW2 (A XF VERIFIED; B/C candidate); MASKZPIP E1/E2/C1/E1c; F-MASKPIP N(a), M3; W2-T26 Thm A (XF VERIFIED
  actual statement); O-STAGES (T_n for (P1)); Cérou–Del Moral–Guyader 2011 Thm 1.4 (novelty check of Thm A: **must be read**).
- **First concrete step.** Read CDG 2011 Thm 1.4 against O-PW2 Thm A and record KNOWN—CITE or NEW; write Theorem Z as one
  statement with five parts and the honest sentence "two-sided masked accuracy is not claimed"; Lean the identities (ii)
  and (iv) on a finite particle system.
- **Risk.** Low for v1 (all parts exist). The real risk is the referee asking for the two-sided masked bound (v2 HQ-VAR).
- **Cost.** S.

## 2. v2 HQs (deferred; listed so v1 can name them as "future work" honestly)

| HQ | Target | Crux | Cost |
|---|---|---|---|
| HQ-VAR | single-island E[W²\|𝓒] (or M_𝓒(ε)) upper bound in the masked regime; two-sided masked Ẑ (V11) | L² mixing constant of the φ = 1 round restricted to V; resolved-grid mechanism (E3/Lemma J); O-PW2 Thm C made non-vacuous | L |
| HQ-STAGES-2 | as-coded masked T_n law (Conjecture P) | candidate grid refines pilot points on V, not Ω; COVER(V); pilot H finite | L |
| HQ-DELIV | DELIV-POP, general DELIV, P(U) → 0 | population-level delivery through the crossing; P(schedule_limit), P(grid_unconverged) | L |
| HQ-GEN | T38 on the study's generator (groups of 5, p ≫ n), LH-iid | partition law for 2g ≤ B packing (W7-PART CE2); Λ(a)/Tr(c) GAP of (b1-LH-iid) | L |
| HQ-FINN | finite-n upper bound on Π(X) | convexity "shell" sketch (API-N200 §3) | M–L |
| HQ-MIX | a YWJ/ZYVR-style mixing or discovery statement for the paper's prior (D1) | prior-side constants (g = n, κ_eff ≈ 1, cap ⌊n/2⌋); R > M fails on the study designs, so a different sufficient condition is needed | L |
| HQ-SL-iid | Theorem SL on LH-iid | concentration replacing exact orthogonality | M |
| HQ-DIAG | a positive diagnostic (Biswas–Jacob–Vanetti eq. (7) from independent islands) | an estimated, not certified, TV bound; its relation to E1c | M |
| HQ-WS | weight stability for the actual partition (proposal §5.3) | O-WSTAB beyond H-ORTH; WS6e/WS8d | L |

## 3. Dependency graph and start order

```
HQ-VALID ──────────┬──────────────▶ HQ-ISLAND ──▶ HQ-EVID
   │               │                    ▲
   │               └──▶ HQ-DEPTH        │ (T03♯ for δ₁ → 0; S₀ ∈ 𝒯 for Z𝒯)
   │                      ▲             │
HQ-START ─────────────────┘ (A₀)        │
   │  (LH masking law, Q*)              │
   └──────────────▶ HQ-SL ◀─────────── HQ-SELECT  (v3.1 success half; T38 (b1-LH)/(b2-LH))
```
- **Wave 1 (start now, in parallel; no inputs from other HQs):** HQ-VALID, HQ-START, HQ-SELECT. All three are assembly
  plus small Lean files; they fix notation (registry IDs: T12/T31(i)/Prop P; T22/T27/DIL/SEP; T03♯/TheoremA/T38) for the rest.
- **Wave 2:** HQ-ISLAND (needs V1's R-island form and T03♯'s restated premises), HQ-DEPTH (needs A₀'s definition from
  HQ-START and the measured table decision).
- **Wave 3:** HQ-SL (needs the LH statement of record from HQ-START and R5's paper form from HQ-SELECT), HQ-EVID (needs
  HQ-ISLAND's identity conventions and HQ-DEPTH's T_n for (P1)).
- **Critical path:** HQ-VALID → HQ-ISLAND → HQ-EVID (objective 1). HQ-SL is the thesis's first half and can slip one wave
  without blocking the rest.
- **Shared notation.** Every HQ uses `00_COMMON.md` and `REGISTRY_v2.md` IDs; new symbols introduced by this run and to be
  registered: W_r := Ẑ_r/Z (METH-AUDIT), M_𝓒(ε) (truncation level, A1), A₀ (masking depth, O-STAGES), Q* (W7-SEP), E_n
  (isolation event, C1), Z_𝒯 / PIP^𝒯 (MASKZPIP).

## 4. Lean certificate plan (what each HQ certifies; all finite cores)

| HQ | Lean targets | Builds on (L-LEAN) |
|---|---|---|
| HQ-VALID | Lemma S; Prop P(iv); Prop P(iii) finite step; T12 island identity via `hstep` | T12Core.lean, Basic.lean |
| HQ-START | Lemma KL; DIL identity; T22(i) product inequality | new file `StartMass.lean` |
| HQ-SELECT | N200 Lemma 1 + Theorem N200; LS-score move count; Lat eligibility | T21HPM.lean, T37Lattice.lean |
| HQ-ISLAND | Thm H(a) deterministic bound; H(b) finite step; Z𝒯 sandwich (P3) | Basic.lean (post, post_sum) |
| HQ-DEPTH | Lemma RS; Lemma 1 (monotone frontier); Theorem G(i)–(ii) | new file `Grid.lean` |
| HQ-SL | isolation probability; x′μ = 0 on Σ_LH; equicorrelation inverse entry | new file `SplitMerge.lean` |
| HQ-EVID | O-PW2 Thm A identity; certificate C1 (Ẑ/Z ≤ Ẑ/Z_𝒯) | T12Core.lean extension |

Everything probabilistic (SLLN, Maurer/Hoeffding, Gaussian concentration, SMC CLTs, T03♯) stays cited or in prose; the
paper should say so in one sentence per theorem ("the finite core is machine-checked; the probabilistic inputs are cited").
