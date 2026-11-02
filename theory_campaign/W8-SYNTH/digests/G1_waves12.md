# G1 digest — waves 1–2: W1-EXP, W1-T03R, W1-T24G, W1-T37R, W1-T38E, W2-BOOK, W2-PREM, W2-T26, W2-VT03R, W2-VT24G

Source: `scratchpad/src/<ID>/` (= `theory_campaign/<ID>/` on `origin/theory/<ID>`). Every author marks every result
"candidate pending cross-family review"; statuses below are verbatim from the author and are never upgraded.
Abbreviations: [E] = W1-EXP, [B] = W1-T24G (as W2-PREM cites them), R_d = near-truth region, S° = reference model.

---------------------------------------------------------------------------------------------------------------------
## W1-EXP — head `722bd18` (2026-11-02T17:12Z)
**Task.** Prove EXP′ (log-ratio expansion, O_P(1) remainder) from G, R, within-block SE; replace T27's H2 by a
chain-leakage condition; build ONE design family carrying T27 masking AND T22(i) near-truth start mass (input for
T38(b)); exact computation at p ≤ 20. Files: REPORT.md, PROOF.md, BRIEF.md (no NOTES.md).

Hypotheses named (REPORT table): R-lite(A,M) (p ≤ n^A, ‖μ‖² ≤ Mn); SE-blk(φ₀) (min_b λ_min(R_{C_b}) ≥ φ₀², checkable);
BO (X_{C_b}ᵀX_{C_b′}=0); BM-blk; ZL(S°) (λ_b(S°)=‖(P_{C_b}−P_{S°∩C_b})μ‖²=0 ∀b); NL_C(S°); SPREAD(Δ₀); VIS-lin(S°,c_V);
H1 (fixed chain of c single additions); CL(L_n) (max_i |δ_{T_i,l_i}| ≤ L_nσ); H3 (P(π₀(S^(0)) ≥ c₀)→1).

| Label | Where | Statement (key hyps) | Status (verbatim) |
|---|---|---|---|
| Thm 1 (EXP′) | PROOF §1; REPORT | G, R-lite, SE-blk ⇒ on E_n (P→1), every within-block addition: log r_b(T+l)/r_b(T) = −½log(n+1) − ν log(1−x_{T,l}) + R, \|R\| ≤ κ_EXP (explicit; headline: "\|R\| <= 0.52/c_* + O(1/n), c_* = sigma^2/(8(M+2sigma^2))"). No BO, s₀, β-min, VIS/NL used. | **PROVED** ("complete; checked line by line") |
| Lemmas 1.1–1.4 | PROOF §1 | Q_S vs RSS; determinant ratio; exact decomposition; RSS floor | parts of Thm 1 proof (complete) |
| §1.5 extension (iid Gaussian, X-dependent partition) | PROOF §1.5 | κ₁₇(Σ) ≥ 2φ₀² ⇒ SE-blk w.p.→1 for EVERY ≤16-partition; caveat at n=200,p=1000: √(17 log p/n) ≈ 0.77 "not small, so SE-blk is an *empirical* matter there" | PROOF SKETCH |
| Prop. 2.1 | PROOF §2 | NL_η → NL_C in Lemma quad of locked T22(iii) (any δ² ≤ Cσ² log n) | PROOF SKETCH |
| Prop. 2.2 ("T22(iii)°") | PROOF §2 | S₀ may be replaced by any deterministic feasible reference S° | PROOF SKETCH |
| Lemma 2.3 | PROOF §2 | \|δ_{T,l}\| ≤ √λ_b(S°) on L_n° | **PROVED** |
| Thm 2 (favourable, BO) | PROOF §2 | G, R, SE-blk, BO, BM-blk ⇒ 1−π₀(S₀) = O_P(2^B √(log n) n^{−1/2}) | **PROOF SKETCH** (relies on locked T22(iii) with η=0) |
| Thm 2 extensions (weak cross-block corr.) | PROOF §2 | — | PROOF SKETCH |
| Thm 6 | PROOF §2 | G, R-lite, SE-blk, ZL(S°), SPREAD, VIS-lin(S°) ⇒ 1−π₀(S°) = O_P(2^B n^{−1/2}), e_n° = O_P(e^{−cn}); "S° = S0 is favourable, S° ≠ S0 is masked" | **PROVED** (via wave-1 T22(i)) |
| Thm 3 (two-sided chain law; masked) | PROOF §3 | G, R-lite, SE on chain sets, H1, CL(L_n) ⇒ −1−κ_EXP ≤ log[r(T_i+l_i)/r(T_i)] + ½log n ≤ κ_EXP + 1.01(L_n+\|Z_i\|)²; fixed L ⇒ H2 | **PROVED** |
| Thm 4 (T27(i) from CL) | PROOF §3 | Thm 3 hyps, fixed L, H3, p ≥ 2(s+c) ⇒ log π₀(S₀) + c log p + (c/2) log n = O_P(1); L_n→∞: upper side + 1.01c(L_n+O_P(1))²; masking persists iff η < 1/2.02 when L_n² ≤ η log n (sufficient) | **PROVED** given H3 ("PROOF SKETCH when H3 is discharged through Prop. 2.2") |
| Limit law | PROOF §3 | δ=0, T_i=∅, orthogonal directions: statistic →_d Σlog((s+i+1)/2) + Σ(σ²/(2v_∅))χ²_{1,i} | PROOF SKETCH |
| Lemma 4.1 (LH population algebra) | PROOF §4.1 | — | **PROVED** |
| Lemma 4.2 (method partition, exact Gram) | PROOF §4.1 | blocks = groups | **PROVED** (deterministic) |
| Thm 5 (LH family, exact Gram, p ≤ n−1) | PROOF §4.2 | LH = S3/S4/S6 equicorrelated groups + one "suppressor edge" per masked variable (corr(j_a,j_b)=ψ, θ_{j_b} = −ψθ_{j_a}), \|ψ_i\| < min(ρ), g ≤ B_n < 2g, S° = S₀∖M: (a) 1−π₀(S°) = O_P(2^B n^{−1/2}) ⇒ π₀(R_d) ≥ π₀(R₀) ≥ 1−O_P(2^B n^{−1/2}); (b) π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}; (c) VIS at S₀ fails in each masked block; (d) 1−π(S₀) = O_P(√(log n/n)) (locked T03); (e) start masked, target not | **PROVED** for (a)(b)(c)(e); (d) by citation; limit law in (b) PROOF SKETCH |
| §4.3 iid-Gaussian LH (p > n) | PROOF §4.3 | random-design realisation | PROOF SKETCH |

Regime discipline: "Thms 2 and 5 are never combined on one sequence; on LH the reference used for T22(i) is S°, not S0."

**Numerics** (`scripts/exp_family.py`, `exp_leak.py`, exact normalisation checked vs brute force to 1e-12).
- Config A (p=16, 4 groups of 4, ρ=0.7, ψ=0.5, c=1): med log10 π₀(S₀) −2.05 (n=100) → −4.07 (n=1.6e6), slope −0.30 per ×4
  (predicted −0.301); Mstat median 0.55 vs predicted 0.543 (q95 0.87 vs 0.84); √n·med(1−π₀(S°)) flat ≈1.6 (no √log n);
  med π₀(R₀) 0.844→0.999; med π(S₀) 0.669→0.997; EXP′ max\|R\| 1.06→0.67. iid realisation: Mstat med 0.76, q95 2.66
  (pred 0.73/2.42); √n(1−π₀(S°)) ∈ [2.5,3.0].
- Config B (c=2, p=20): slope −0.99/decade (pred −1); med π₀(R₀) 0.929→0.999; π(S₀) 0.763→0.985.
- Leakage chain: L=0,2,4,√(2 log n) all match predicted (L+Z)²/(2v) law (e.g. L=4, n=1.6e6: obs 0.99/1.90/3.38 vs pred 0.99/1.90/3.29).
- Study size (`study_seblk.py`, n=200, B=14): min_b λ_min(R_{C_b}) = 0.46/0.25/0.17/0.086/0.17/0.064 (S1..S6, p=500);
  0.47/0.25/0.17/0.084/0.16/0.062 (p=1000) — "SE-blk ... holds at the study size in all six scenarios". Population
  leakage λ_b(S0)/(n−1) = 0 in S1,S3,S4,S6; positive in 98/100 S5 blocks; S2 81/100 (index windows, "only indicative").

**What fails.** Packing at study B: at n=200, p≥500, B=14 two groups of 5 share a block; "If a linked pair is packed
together ... masking disappears"; LH needs g ≤ B < 2g or hub-separation hypothesis. Exact Gram needs p ≤ n−1. "NL_eta fails
for random designs at fixed SNR" — locked T22(iii) does not transfer to iid designs; "E(1-x)^{-nu} = inf for a pure-noise
column ... truncation is essential". "S5 and S2 sit in neither clean regime". Crude constant in Thm 3 (loose by 2v/σ²).
Thm 6 SPREAD excludes all-signal-in-one-block.
**Needs escalation.** (1) locked-register update: EXP′ removable from T22(iii) hypothesis list, "Decision Point 2's D1 is
discharged", NL_η → NL_C + NL_avg — "edits to locked statements". (2) T38(b): use S° = S₀∖M ∈ R₀, state masked branch on LH
with hub-separation hypothesis; never T22(iii) at S0 there. (3) n=200 data: S1/S3/S4/S6 asymptotically favourable, so
observed masking "is most plausibly *weak-signal* masking" (CL(L) bounded for weak truths) — **CONJECTURE**, "not checked on
the data here"; "In that mechanism `pi(S0)` is *also* small, unlike LH."
**Outside scope.** T38 itself; bridge transport S°→S₀; T22(iii) for S2/S5; full random-design proof; exact branch (p ≤ 17).
**Confidence cards** (target / P(true) / P(provable) / crux / method change):
T1 EXP′ 0.97 / done / Lemma 1.1, RSS floor / No · random-design ext. 0.93/0.85/17-sparse eigen concentration/No ·
T22(iii) in BO (Thm 2/6) 0.95/0.9/transfer of locked proof/No · T22(iii) iid (S3/S4/S6) 0.8/0.6/truncated Beta average over
X-dependent partition/No · T27(i) from CL 0.97/done (given H3)/—/No · limit law 0.9/0.8 · LH exact Gram 0.95/done except
limit law · LH iid p>n 0.85/0.6 · weak-signal masking explains data 0.6/0.5/needs data/No.
**LS0 / common σ² / n=200:** no LS0 or common-σ² mention. n=200 relevance as above (SE-blk ok; packing; weak-signal conjecture).

---------------------------------------------------------------------------------------------------------------------
## W1-T03R — head `7e14d6f` (2026-11-02T16:56Z)
**Task.** Exact BB(1,p) tail in T02(i) (hoped: m_n from ~200 to s₀+O(s₀ log n/log p)); restate T03 with SE restricted to
comparison unions; n=200 honesty paragraph; numerics.

| Label | Where | Statement | Status |
|---|---|---|---|
| Lemma E1 (exact tail) | PROOF §1 | ρ_i = ½(1−(i−1)/(2p−1−i)); size marginal geometric(½) up to e^{−k²/4p}; two-sided bounds (b),(c) on R_m = ϖ(\|S\|>m)/ϖ(S₀); (d) improves locked 4(2p)^{s₀}2^{−m} by ≥ 4·s₀!·e^{γ_m} | PROVED |
| Lemma E2 / Prop. E3 | PROOF §1 | s₀ ≤ m♯ ≤ min(K, m_n); closed form; in R1 either m♯=K or m♯−s₀ ≥ [s₀ log(p/s₀) + ((s₀+2)/2)log n]/log2 − 1 − o(1): "order s₀ log n, not s₀ log n / log p" (barrier for the technique, not the posterior) | PROVED |
| Thm T02(i♯) | PROOF §2 | G, R: Π(\|S\|>m\|y) = R_m(n+1)^{s₀/2}√n·Θ♯; sup_m P₀(Θ♯>L) ≤ (8+24M/σ*²)/(n−1) + L^{−1/2} + C_Λ/log(√L/c♯) | PROVED (candidate) |
| Lemma den′ | PROOF §2 | locked lem:den body without ϖ(S₀) ≥ ½(2p)^{−s₀} | (used, PROVED) |
| Prop. D | PROOF §3 | G, R, s₀=1, p identical columns, β₁≠0: w.p.→1 Π(\|S\|>m\|y) ≥ 2^{−(m+4)}e^{−m(m−1)/(4(p−m))}; target "m_n = s₀ + O(s₀ log n/log p)" false under G,R | COUNTEREXAMPLE (reproducible) |
| Lemma I (interlacing), Lemma B | PROOF §4 | what the proofs need from SE | Lemma B PROVED |
| SE_λ(j₀), SE_w(m;g₀) | PROOF §4 | anchored at S₀: λ_min(R_{S₀∪J}) ≥ φ₀² for \|J\| ≤ j₀ = ⌈(2A+1)s₀⌉+1; λ_min(G_{S₀∪J}) ≥ g₀ for \|J\| ≤ m♯ | hypotheses |
| Thm T02(ii♯) | PROOF §5 | R1, G, R, SE_w(m♯;g₀) ⇒ Π(S ⊋ S₀\|y) = O_P(√(log n/n)) | PROVED (candidate) |
| Thm T03♯ | PROOF §6 | R1, G, R, SE_λ(j₀), SE_w(m♯;g₀), BM-∞ or BM(c), c > c₀ = L* = max{4C*, 32[s₀(A+1)+2]}: (i) 1−π(S₀)=O_P(√(log n/n)); (ii) PIPs within 1−π(S₀), MPM=S₀ w.p.→1; (iii) P(S†≠S₀) ≤ 2E₀[1−π(S₀)]; (iv) no β-min: J_n(c) gets PIP→1; (v) scale invariance. s₀=⌊√n⌋ NOT covered | PROVED (candidate) ("PROVED as a candidate") |
| Remark 3 (determinant-only SE) | PROOF §7 | geometric-mean eigenvalue condition would suffice for (C4)–(C5) | CONJECTURE |
| True posterior needs m−s₀ ≍ s₀ log p under G,R | REPORT §4 | — | OPEN |
| SE_w at all sizes ≤ K ⇒ m−s₀ = O(log n) | REPORT §4 | — | CONJECTURE |

Changed locked steps listed in REPORT §2 table (C1)–(C10); unchanged steps cited by label ([P3] lem:red, lem:smoother, …).
**Numerics** (`tail_bound.py` etc.). n=200: m_old 201/215, m♯ = K = 100 ("cap binds"), uncapped 146/168 (p=500/1000);
saving ≈ 36 sizes = log₂(14!) = 36.3 for p=n^A; locked bound overstates R_m by 10^{11.6}–10^{14.2}; T02(i♯) prefactor
min over m<K = 10^{15.8} (p=500), 10^{21.3} (p=1000) — "vacuous at n = 200"; first n with m♯<K: 342 vs 464 (locked).
Prop. D: 2^m·Π(\|S\|>m\|y) ∈ [0.70,1.00]; cutoff for n^{−1/2} tail 4/6/8/9 at n=200…2e5 ≈ ½log₂n; 200/200 data sets.
SE at n=200 p=500 (one draw): SE_λ random J 0.16–0.21 (S1), greedy ≤ 0.033; S4 0.046–0.060, greedy ≤ 0.0125; SE_w
λ_min(G) random 11.3–13.1 (S1), greedy ≤ 0.40; S4 2.9–3.7, greedy ≤ 0.22 (upper bounds on minima, not verified).
β-min: c₀ = L* = 1037.5/1153.2; θ² ≥ 27.5/φ₀², 30.6/φ₀² vs executed 0.64 (c=1), 0.16 (c=0.5); shortfall 43×/48× (φ₀²=1),
≈1,300× with φ₀² ≈ 0.033; "The failure is in the proof constant, not in the signal." Proof thresholds: δ_n ≤ ½ from
n ≈ 115,000 (new) vs 127,000 (old) — **flagged as ERROR by W2-VT03R** (see below).
**What fails.** "The frozen-plan sentence 'cuts m_n from about 200 to s₀ + O(s₀ log n / log p) ...' is wrong on both
counts"; exact tail saves ~36–55 sizes not ~180; "What does make SE meaningful at n = 200 is the **cap**: m♯ ≤ K always."
"At n = 200 no finite-n guarantee follows from T01–T03."
**n=200 disclosure paragraph** (REPORT §5, quoted in substance): "they are not numerical guarantees at n = 200 ..."; SE now
over 62/66 (normalised) and 114 columns; "in correlated designs the normalised constant can be as small as φ₀² ≈ 0.01–0.03";
"The empirical recovery rates at n = 200 are therefore evidence in their own right, not an instance of the theorem."
Surviving finite-n statements: (F1) deterministic max_j\|PIP_j − 1\{j∈S₀\}\| ≤ 1−π(S₀), π(S₀)>½ ⇒ HPM = MPM = S₀;
(F2) exact identities (T01(i), Markov identity); (F3) T02(i♯) inequality (vacuous at n=200); (F4) Prop. D.
**Needs escalation.** (1) Correct FROZEN_LIST "Restatement notes — T03/T02" and FABLE_REVIEW Thm 1: "ratio ≈ k/2p, not ½"
is the per-model ratio; class ratio is ½. (2) Adopt split SE_λ + SE_w? (3) T04 cites H-T02 with old m_n (not checked).
(4) finite-n at n=200 needs a different route (e.g. T37); "even c₀ → 0 leaves the T02(i♯) prefactor vacuous".
**Outside scope.** Growing s₀; sharp β-min constants; true-posterior lower bound (OPEN); determinant-only SE
(CONJECTURE); T04; verifying SE_w/SE_λ exactly on realised designs.
**Confidence card** (status/P(true)/P(provable)/crux): E1 PROVED .99/.99 · E2/E3 PROVED .97/.97 · T02(i♯) PROVED
(candidate) .97/.96 · Prop. D COUNTEREXAMPLE .96/.95 · T02(ii♯) .93/.92 · T03♯ .90/.88 ("every SE use falls in
(B1)/(B2)/(B3)") · brief's target COUNTEREXAMPLE 0.02 · true posterior needs s₀ log p OPEN 0.3/0.3 · O(log n) under SE_w
CONJECTURE 0.6/0.4. (No "method change" column.)
**Disagreement:** with FROZEN_LIST/FABLE_REVIEW premise ("ratio ≈ k/2p").

---------------------------------------------------------------------------------------------------------------------
## W1-T24G — head `9e210a3` (2026-11-02T17:39Z)
**Task.** Gibbs-path terminal repair: model one φ=1 round exactly; restated T24 with polynomial c′; resolve EXIT_d; premises
under G,R,SE,BM-∞; exact p ≤ 20 numerics; discharge H24 in T21 route (e).

Setting: rounds of m = p+B+2 labels in uniform order (G_j, U, N₁..N_B, I); (R1) order independent of state, (R2) each label
once, (R3) SR every visited state scored, (R4) Gibbs evaluation adjacent to S₀ scores it, (R5) terminal trajectories
conditionally independent. Potential V = \|M\| + a while M ≠ ∅ (look-alike budget a = \|A\|+c), V = \|P\| on supersets;
steps bad / progress / neutral.

| Label | Where | Statement | Status |
|---|---|---|---|
| Lemma F, O, C | PROOF §1 | first-failure union; order facts; binomial domination P(Bin(H,c)<v) ≤ v(1−c)^{⌊H/v⌋} | PROVED |
| Lemma P | PROOF §2 | exact first-change progress P*(x) ≥ s_g[1−Q_D/(\|D\|+2)]/(\|D\|+1); c′ ≥ s_g[1−Q_𝔊/(B+4)]/(B+3) | PROVED |
| Cor. P1 (distance-one scoring) | PROOF §2 | x△S₀={j} ⇒ P(S₀ scored next round) ≥ a₁(x) = ∫₀¹∏_{e≠G_j}(1−t q_e)dt; N₁ particles ≤ ∏(1−a₁) | PROVED |
| Prop. U (undo / EXIT_d) | PROOF §3 | Gibbs can't undo within round; truth removal / V-raising I-jump = bad (η); extra-for-extra swap V-neutral, charged to slot term h(l) in c₂ | PROVED |
| **Theorem B (restated T24)** | PROOF §4 | EX-A, EX-S, SR, φ=1: P_x(S₀ not scored within H) ≤ P(Bin(H,c_*)<v) + Hη ≤ v(1−c_*)^{⌊H/v⌋} + Hη; c₂ ≥ 1/(B+3) − ε_del; c₁ = 1−ε_add; deterministic given data; constants ε_add, η₁, ε_del(a), h(l), H_a, η₂(a) exact definitions | PROVED ("deterministic given the data; EX-A, EX-S, SR") |
| Prop. B1 / B2 | PROOF §4 | phase-1 ≤ ε_add; phase-2 ≤ ε_del(a)+H_a | PROVED |
| Cor. B-unif | PROOF §4 | uniform over eligible set fixed before selection | PROVED |
| Cor. B-M | PROOF §4 | ∏ over particles of min{1, bound}, given (R5) | PROVED given (R5) |
| Prop. D (drift form) | PROOF §4 | η = η_ex + η_in; bound Hη_ex + inf_z ρ(z)^H z^{v−1}; internal increases need only η→0 | PROVED |
| Prop. A (one-round sweep) | PROOF §5 | — | "PROVED; numerically vacuous" (ε₂ ≈ 2.6) |
| §6 asymptotic premises table | PROOF §6 | under G,R,SE,BM-∞: τ₂ yes; leakage at S₀ yes; NL0(a) needed for a ≥ 1 ("equicorrelated nulls (S5) fail in rate for p ≳ n^{0.58}"); ε_del yes a=1, UDEL(a) for a≥2; ε_add yes one missing, else BTP; TS(𝒵), TL(𝒵,A), IND(𝓕) needed; conclusion c_* ≥ 1/(B+3)−o_P(1), rate ~ n^{−0.07} | PROOF SKETCH |
| CE1 | PROOF §7 | H24's uniform exit input false in correlated designs; boundary state exits w.p. ≥ (1−o(1))/(B+d+4) | COUNTEREXAMPLE (numerical, reproducible) + PROOF SKETCH (asymptotic) |
| CE2 | PROOF §7 | brief's (1−c′)^{⌊H/(s₀+d)⌋} not implied; needs factor v | COUNTEREXAMPLE |
| Layered version (cancellation); state-averaged drift | PROOF §8 | — | OPEN |
| c₂ → 1−H_a at production B | PROOF §8 | — | CONJECTURE |
| T21 route (e′), (e-M) | REPORT §5 | (e′): replace (1−a_n)^H + Hη_n by P(Bin(H,c_*)<v)+Hη; "H24′" only definitions | "PROVED (candidate) as an implication; it inherits T21's own conditional status" |

**Numerics** (p=20, 4 groups of 5, s₀=4, β=(1.4,−1.0,1.8,−1.2), n=200, c ∈ {1,0.5}, B=4, H=12; numpy re-draws, not R).
π₀: S1 near S₀; S2 supersets 1–3 extras; S3/S4/S6 supersets 3–7 extras (π₀(S₀) 1e-11..1e-36, "double counting of group-mates
across split blocks"); S5 masked (mode {0,2,13,14} misses 6,15). π(S₀) ≈ 0.71–0.78. Repair from 3000 π₀ draws: 100% within 12
rounds all designs; round 1: S1 0.84–0.89, S5 0.11–0.12; by round 2: 0.66–0.99. Phase-2 (T4a): actual progress 0.75–0.89 vs
P* 0.53–0.57, c₂ 0.25–0.47, c_poly 0.27–0.34, floor 1/(B+3)=0.143 ("floor < c_poly < c₂ ≤ P* < actual"). T4b phase 1:
c₁ = 1.000 except S4 c=0.5 (0.503); η₁ 1.2–3.3. T4c Cor. P1: min a₁ 0.139–0.439 ("≤ 0.86^{N₁}", "the one rigorous bound ...
non-vacuous at n = 200"). η₂(a=1) 0.37–0.64 per round; scaling (10 seeds, c=0.5): (L+4)·median η₂(1) still 1.1–1.8 at
n=12800; c₂ → ½. CE1 worst boundary exit: S1 0.16–0.22, S2 0.62–0.79, S3 0.83–0.94, S4 0.80–0.98, S5 0.83–0.97, S6
0.72–0.97; (L+4)·exit 1.9–11.8.
**What fails.** Uniform-over-R_d formulations (H24, LK_d, EXIT_d) (CE1); Prop. A; P* small at incomplete states; finite n
"π(S₀) ≈ 0.72, so leakage-type bad events have O(1) rate per round, and H·η is vacuous although repair is fast"; drift
argument OPEN; cancellation: BTP, TS fail, layered version OPEN; production B=14–16 floor 1/(B+3) ≈ 0.06.
**Needs escalation.** (1) "Retire H24, and rewrite T21 route (e) as (e′) plus (e-M)". (2) Retire LK_d, EXIT_d, GAIN_d; new
inventory codes NL0, UDEL, TS, TL(𝒵,A), BTP, IND. (3) Make multi-particle route explicit; confirm (R5) vs implementation
("no resampling in burn-in or measured rounds, and per-particle streams"). (4) Confirm SR reading with Felipe.
**Outside scope.** PIP repair (T24(iii)); pilot repair; drift refinement; layered version; actual p=500/1000 datasets; T38
delivery.
**Confidence cards:** round model .97/done/R1,R3 readings/no · Theorem B .90/done (review needed)/classification, B2 slot
step/no · Prop. U .93/done · asymptotic premises .75 overall (0.85 automatic items)/0.5/IND, TL(𝒵,A), NL0(a), UDEL(a≥2)/no
· CE1 0.9 (asymptotic 0.85)/0.8 · CE2 .99/done · T21 (e′),(e-M) .9/.9/(R5)/"no (confirm the implementation's streams)" ·
useful finite-n single-particle bound at n=200 0.2/0.3 (drift)/O(1) superset leakage/no.
**Notes.** NOTES: one commit lacks attribution trailer (force-push refused). H = L+4 used throughout (later runs: L+5).
Disagreement: brief/Fable's (1−c′)^{⌊H/(s₀+d)⌋} form (CE2); H24 (CE1).

---------------------------------------------------------------------------------------------------------------------
## W1-T37R — head `3bcc429` (2026-11-02T17:36Z)
**Task.** Diagnose literal TD failure; weakest TD′ for greedy local-search repair; finite-n bound without 2^{s₀}; asymptotics;
n=200-like numerics; view on Gibbs vs local search. Notation m(S), e(S), Φ = \|SΔS₀\|, R_{a,d} = {S ∈ R_d : m(S) ≤ a};
moves progress 𝒫 / neutral 𝒩 / regressive ℛ.

| Label | Where | Statement | Status |
|---|---|---|---|
| Lemma 0 (monotonicity obstruction) | PROOF | F strictly increases along search; search can make Ŝ=S₀ only on E_LS = {S₀ ∉ 𝒮_pre, F(S₀) > max_{𝒮_pre}F}; certified stop at S₀ ⇒ Ŝ = S₀ (π(S₀)>½ not needed) | PROVED |
| Prop 1 | PROOF | s₀≥1, d≥1, s₀+1≤K, p>s₀: TD(d,m) ⇒ m=0 and F(S₀+l)=F(S₀) ∀ null l; under G, P₀(TD(d,0)) = 0. "Literal TD(d, m) **cannot hold for any d ≥ 1**" | PROVED |
| Swap identity (SW) | PROOF | F(S−i+j)−F(S) = g(S,j) + h(S+j,i) | PROVED ("one line") |
| Lemma 2 | PROOF | progress moves keep Lat(S), R_{a,d} closed; on NA_d ∩ TL_d S₀ local max and best move at supersets deletes an extra | PROVED |
| Lemma 3 | PROOF | SE on S∪S₀ ⇒ max_{j∈S₀∖S} δ²_{S,j} ≥ (n−1)φ₀⁴‖θ*_{S₀∖S}‖²/m(S) | PROVED |
| Theorem A (refined T37(i)) | PROOF | (A1) TD′_∞(𝓡) iff greedy path from every S∈𝓡 stays in 𝓡 and ends at S₀; (A2) TD′_P(R_{a,d}) ⇒ path in Lat(S), τ(S) = m+e−#(extra→truth swaps) moves; (A3) TD′_P(R_{a,d}) and ℓ ≥ a+d ⇒ certified S₀ from every centre ("cap only has to satisfy ℓ ≥ a + d, not ℓ ≥ s₀ + d"); (A5) TD ⇒ TD′_P ⇒ TD′_∞ | PROVED |
| Theorem B (refined T37(ii)) | PROOF | G; class 𝒞 ⊆ R_{a,d} fixed: P(fail) ≤ P(S_c∉𝒞) + P₀(NA_dᶜ) + P₀(TL_dᶜ) + Σ_{Lat(𝒞)} P₀(D_Sᶜ); 2^{Φ(S_c)} states or (2s₀)^a(p+1)^d; no 2^{s₀} | "PROVED for the inclusions and the union bound, PROOF SKETCH for the form of each single event" |
| Theorem C (refined T37(iii)) | PROOF | (C1) TL_d w.p.→1; NA_d under LD(d) (else p^d = o(√(n log n))); (C2) PGD(η) ⇒ TD′_P(R_{a,d}) w.p.→1; (C3) SE+BM-∞ ⇏ PGD; (C4) without PGD TD′_∞ on R_{a,d+d₁} | PROOF SKETCH (C1–C2); COUNTEREXAMPLE (C3); CONJECTURE (C4) |

New hypotheses: NA_d, TL_d, PGD(η) (population greedy dominance), LD(d) (local dependence of nulls; COH ⇒ LD). "These
statements replace GAIN_d, LK_d and EXIT_d **only for the local-search route, and only on E_LS**."
**Numerics.** Exp 2 (n=200, p=500, s₀=14, ℓ=10, S1–S6 × c∈{1,0.5} × 6 = 72 datasets, numpy not R streams): S₀ flip/swap
local max in 35/36 (c=1; exception S2) and 23/36 (c=0.5; S4–S6 worst: 0.50/0.33/0.50); otherwise greedy from S₀ gains
0.2–4.8 nats (median 1.3) = certified posterior misses. "In the 58 datasets where S₀ is a local max, 1160/1160 centres were
repaired and certified, using 1–3 moves"; 99.0% all-progress; moves: 1156 extra→truth swaps, 584 truth adds, 236 deletions,
11 truth→truth, 1 null→null. Other 14 datasets 0/280 (forced by Lemma 0). d=0, m≤2: greedy = add truth 3732/3780 (c=1), only
2472/3780 (c=0.5; truth→truth swaps 1239) — "This is why literal TD(0) fails." Exp 1 (p=20, s₀=4, 50 reps, true prior / pm500):
literal TD(1,0) 0/1800; TD′_∞(R_{s₀,2}) 0.92/0.94; TD′_P(R_{s₀,2}) 0.71/0.71; TD′_P(R_{1,1}) 1.00; TD′_P(R_{2,2}) 0.78/0.83;
TD′_∞(R_{2,2}) 0.97/0.98; ≤ 6 moves. c=0.25: S₀ local max only 2–48%. Exp 1b (p=25, s₀=5): TD(0) 0.70–0.80 at c=1; TD′_P(R_{s₀,2})
0.25, TD′_∞ 0.90. Exp 3 (PGD counterexample): x₃ = 0.85(x₁+x₂)/√2 + …, φ₀²=0.15, n=3000: first greedy move "add x₃" 200/200;
reaches S₀ in 3 moves vs Φ=2.
**What fails.** (1) literal TD d≥1 self-contradictory; extra→truth swap is "the main repair move in practice". (2) TD(0)/TD′_P
on large regions: missing truth inflates residual variance, masking weak truths (√(2·pen) ≈ 3.7 at n=200, p=500). (3) all of R_d
"is the wrong object". (4) SE+BM-∞ don't give progress; NA_d with d≥2 needs LD. (5) "At n = 200 the binding constraint is
posterior dominance, not search"; "T37 ... cannot explain the masked-regime successes, which (by Lemma 0 and the 98% Gibbs
share) were scored before the search." (6) cap ℓ=10 < 15 "a non-issue" on R_{a,d} with a+d ≤ 10; T37(i)'s "exactly \|SΔS₀\|
moves" wrong.
**Needs escalation.** C(C1) NA_d under LD perturbation bound; C(C2) uniform linearisation incl. ridge H=(n+1)G+I; Theorem B
≤4-dim event exact only without ridge (O(1/n) correction); C4; independent recheck of Exp 2 on R streams (needs R).
**Outside scope / views.** "The Gibbs route is the right repair statement for this method (my view ...)"; T37 "a backup that
matters only on E_LS"; Lemma 0(c) ⇒ T21's π(S₀)>½ unnecessary for local-search delivery; posterior misses at c=0.5 in S4–S6
"contradict the 'correlated-design advantage' margin story of T37's Why".
**Confidence cards:** Prop 1 .99/done/no · Lemma 0 .98/done/"centre = led.hpmS" confirmed in v3_core.cpp/no · Theorem A
.97/done/no · Theorem B .95/.9/ridge correction/no · Theorem C .8/.6/NA_d without COH, uniform linearisation/no · C4 .6/.3 ·
"T37 explains the n = 200 masked-regime successes" 0.1/—/Lemma 0/"rely on Gibbs (T24)".
**Disagreement:** brief's decision D18 ("literal TD fails generically") reframed as "an internal contradiction".

---------------------------------------------------------------------------------------------------------------------
## W1-T38E — head `436a712` (2026-11-02T17:10Z)
**Task.** T38(b) delivery of a near-truth particle/centre; local-search eligibility (or LS0); compose T38(b); check joint
compatibility (Astra's rule) of T27 masking + T22(i) near-truth mass.

| Label | Where | Statement | Status |
|---|---|---|---|
| Lemma A | PROOF §1 | γ_φ = γ₀^{1−φ}γ₁^φ; Gibbs change prob at any φ ≤ max{κ₀,κ₁} | PROVED |
| C0 | PROOF §2.1 | naive set version of T22(iv) false: q₀(A)=q₁(A)=0.993, q_{1/2}(A)=9·10⁻⁵ | COUNTEREXAMPLE |
| Lemma B | PROOF §2.2 | structured bridge mass sup_φ q_φ(R_d^c) ≤ θ/(1−θ) + … (deterministic) | PROVED (deterministic); asymptotic reading PROOF SKETCH (needs start-extras tail "not proved here"; d+1 > c(A+½)/κ) |
| Lemma S (ESS share lemma) | PROOF §3 | ESS ≥ eH, subset fraction f ⇒ weighted share ≥ f − √(f(1−f)(1/e−1)); population ESS non-increasing in φ | PROVED ("tight") |
| Theorem D2 (pilot one-flip discovery) | PROOF §4 | EX-A, EX-S, SR; x°ΔS₀={j}; π₀(x°) ≥ b > 1/10; Dep over l ∉ 𝒟∪{j}; NB: P(S₀∉𝒮_cal) ≤ e^{−2Ht²} + P(NB^c) + exp{−H(1−Dep)₊g(b−t)/(k_D+B+3)}, H=H₀ ≥ 0.2max(n,p); "covers one-cancellation masking at every p ≲ n^A, including p ≫ √n" | PROVED |
| Cor. D2-∞ | PROOF §4 | asymptotic version | PROVED given the hypotheses |
| Theorem D1 (T15 route) | PROOF §5.1 | P(no R_d particle) ≤ π(R_d^c)/c + P(Ẑ_r/Z < c) | PROVED (from locked T15) |
| Prop. D3 (forward chain) | PROOF §5.2 | P(no R_d particle after stage T) ≤ (1−π₀(R_d))^N + Σ(ζ_t+η_t), under SHARE(ζ), EXIT-end(η) | PROVED (conditional on SHARE) |
| C1 | PROOF §5.3 | abstract 4-state SMC: π₀(A)=0.99995, bridge mass ≥0.9997, zero exits, yet A extinct in 0.480 (N=1e5) / 0.995 (N=1e6) of 200 islands; log Ẑ/Z ≈ −1817/−1930 | COUNTEREXAMPLE (reproducible); whether a BVS design realises it: OPEN |
| Prop. E1 | PROOF §6.1 | F(S∪P) − F(S) ≥ −\|P\|[log 2p + ½log(n+1)]; brief's eligibility F(S°) > sup_{R_d^c}F fails w.p.→1 under omission masking (CF2: by 38–172 nats) | PROVED (deterministic part); margin PROOF SKETCH |
| Remark E2 (proxy-only masking S° ⊇ S₀) | PROOF §6.2 | {F ≥ F(S°)} ⊆ R_{d′}, d′ ≈ d(1+2A) | PROOF SKETCH |
| Theorem E3 (LS0 eligibility) | PROOF §6.3 | TD′(𝔅,ℓ), S̃₀ ∈ 𝔅 ⇒ LS0 scores S₀; π₀(x°) > ½, x° ∈ R_d ⇒ S̃₀ = x°; cost ≤ (ℓ+1)max_k[p+k(p−k)] | PROVED |
| §6.4 T37's TD(d,0) | PROOF §6.4 | CF1: TD(1,0) fails 248/352, 728/1004 states (margin −7.5, −9.2 nats); CF2 TD(2,0) fails 26,019/29,936; swap gap ≈ ½log n + log p; GP(2) fails at 4 states but reach S₀ in 3 moves | COUNTEREXAMPLE (reproducible) |
| Theorem T38(b)-R (composition) | PROOF §7 | routes (b1) ELIG+TD′ (LS0), (b1′) D2, (b2) DELIV+REPAIR(a_n, L+4), each + H-T03 ⇒ liminf P(Uᶜ, Ŝ⁺=S₀) ≥ 1 − limsup P(U); "The brief's 'P(Ŝ = S₀) → 1 − limsup P(U)' is not a well-formed limit" | PROVED given the named inputs |
| Corollary (c) cost | PROOF §7 | O((n+p)(p+B)log²n + p²log²n) | PROVED given T32(i) ("itself an unlocked conjecture") |
| CF(c) compatibility family | PROOF §8 | p = ⌊n^{3/4}⌋, cross-block cancellation x_jᵀμ=0, B−1 copies per truth; satisfies G,R,SE (λ_min 0.024/0.015; exact for n ≥ 1,626), BM-∞, T27 masking, π₀(R₀) 0.927/0.964, S̃₀={1}∈R₀, TD′; route (b2) SHARE/EXIT-end OPEN | table; p ≫ n version CONJECTURE |

**Numerics.** CF2: π₀(S₀) = 5.9e-7 (n=400), 1.5e-8 (n=1600); π₀({1}) 0.926/0.964; iid miss ≥ 0.0026 and 0.86; LS0 scores S₀
in all 4 configs; D2 bound 3e-9 (n=400), 1e-6 (n=1600); E1 margins F(S₀)−F({1}) = 44.5, 180 ≫ κ_n(d) = 16–30; Lemma S worst
slack −1.1e-13 over 2e5 cases. π not enumerated (p=89, 252) — π(S₀)→1 rests on locked T03.
**What fails.** T15/LT in masked regime (Ẑ/Z ≈ 0 even when delivery holds); "Bridge mass ⇒ delivery. False (C1)"; Lemma A for
exits at states missing a truth with proxies; ESS share over many stages compounds; brief's eligibility condition false (E1);
T37 TD(d,0) d≥1 false; D2 beyond distance 1 needs a crossing temperature.
**Needs escalation.** (1) W1-T37R: replace TD(d,0) by TD′ (or GP(d)). (2) HQ/Felipe: adopt LS0 "as the masked-regime route"
— "a method change, but deterministic, cheap and post-hoc applicable. Label any fits rerun with it." (3) route (b2) needs SHARE
or LT; keep conditional or drop. (4) SR "still lists ... 'to be confirmed'" (engine does it in `step_gibbs`). (5) T38 text:
limit form; cost formula; "ℓ_n < s₀ + d" → "path length \|S̃₀ Δ S₀\| ≤ ℓ_n + 1"; "T27-H3 already implies π₀(𝓡_d) ≥ c₀".
**Recommendation.** "(b1)+LS0 as the main masked-regime route, and D2 as the no-tweak route for one-flip masking"; "T39
(repair tracks) is not needed for the HPM if LS0 is accepted".
**Outside scope.** masked evidence/PIP; proof of TD′/REPAIR; T32(i); p ≫ n family; n=200 data review ("consistent with
D2/C1-type reasoning ... unverified").
**Confidence cards:** Lemma A .99/done/no · Lemma B .95/done (asymptotic 0.5)/start extras tail · Lemma S .99/done · D2 .9/done
(statistical instance 0.6)/Dep, NB/no · D1 .98/done/LT fails in masked regime · D3+SHARE 0.6 (SHARE holds)/0.15/C1/"no (but
unprovable as is)" · E1 .95/done (margin .85) · E3+LS0 .97/done/needs TD′ and π₀(x°)>½/**"yes, minor (LS0)"** · T38(b)-R .97
given inputs/done/"(b1) yes-minor; (b1′), (b2) no" · CF compatibility .85/.7/uniform TD′ on CF, p≫n/no · T37 TD(d,0) d≥1 0.05.
**Astra answer:** T27 masking and T22(i) near-truth mass "are **compatible**, and in fact aligned" (disjoint coordinates).

---------------------------------------------------------------------------------------------------------------------
## W2-BOOK — head `57eb3d0` (2026-11-02T17:35Z)
**Task.** Bookkeeping restatements (P5): T12 + T31(i), run/output split, T07(+T06(i)), T21. Files incl. STATEMENTS.tex
(uncompiled LaTeX fragment).

New codes: **GUARD** (stop-only coupling: on 𝒢 = {status = resource_limit} the run stops; on 𝒢ᶜ outputs = those of the
potential uninterrupted run R̄); **VAL-FP(η, ε)** (floating point within η of exact outside prob ε).

| Label | Where | Statement | Status |
|---|---|---|---|
| Lemma RO (run/output split) | PROOF §0.2 | under GUARD: 1_𝒪g = 1_𝒪ḡ; P(𝒪, g∈A) ≤ P(𝒪̄, ḡ∈A); P(𝒪ᶜ∪{g∉A}) ≤ P(𝒢)+P(𝒪̄ᶜ)+P(𝒪̄, ḡ∉A); E[1_𝒪g] ≤ E[1_𝒪̄ḡ] | PROVED |
| Guard counterexample | PROOF §0.3 | stylised cost: stop share 0.22% ⇒ E[Ẑ\|output]/Z = 0.974; 0.93% ⇒ 0.798; 3.9% ⇒ 0.011 | COUNTEREXAMPLE ("in a stylised cost model") |
| Proposition 2 (restated T12 + T31(i)) | PROOF §1 | (a) islandwise E[Ẑ_r\|𝓒]=Z, E[Ẑ_rPIP̂_rj\|𝓒]=Z·PIP_j; (b) pooled + pooled island product unbiased; (c) NOT: E[Ẑ·P̄_j\|𝓒] = Z·PIP_j − ¾Cov(PIP̂_1j, Ẑ₁\|𝓒) (< −0.1275Z in instance; P̄₁ bias < −0.17); (d) Markov/Jensen; (e) output level P(reported ∧ 0.05Ẑ > Z) ≤ 0.05·P(𝒜); (f) VAL-FP ⇒ ≤ 0.05e^η + ε; secondary PIP removed | PROVED (candidate; corollary of locked T12, T31(i) and Lemma RO) |
| Split for T11(iii), T14(i), T15, T23(ii), T25(iv), T31, T34 | PROOF §2 | statement changes only; T34 new clause (v) = Lemma RO | statement edits; T34 (v) PROVED, rest CONJECTURE |
| Proposition 1 (T07 + T06(i)) | PROOF §3 | Bayes rules; plug-in excess risk ≤ 2‖p̂−PIP‖₁; (i′) sharp ceiling: some positive size-only prior has HPM S₀ iff S*_{s₀} = S₀; (iii′) certificate: scored S′, \|S′\|=s₀, F(S′)>F(S₀) ⇒ no size-only prior recovers S₀; T06(i) wording "equal outer products X_SX_Sᵀ, not equal projections" | PROVED (locked parts + (i′), (iii′) new PROVED) |
| Theorem 4 (restated T21) | PROOF §4 | (C1) P(no output or Ŝ≠S₀) ≤ P(U) + 2E₀δ₁ + P(Ūᶜ, S₀∉𝒮̄), P(U) ≤ P(resource_limit)+P(Ū); routes (a) iid draws, (d) tables/scans, (e′) Theorem B β_H(X_sel) with H ≤ L+5, (e-M) product | "PROVED (candidate) as an implication; (e′) conditional on W1-T24G Theorem B (unreviewed)" |
| (d⁺) T37 wiring | PROOF §4.3 | P₀(TD*ᶜ) + P(E_LSᶜ ∩ TD*) + 1{ℓ < s₀+d} | "PROVED as an implication; T37 itself is OPEN" |
| (e′) asymptotic form | PROOF §4.1 | H = L+4 or L+5 | PROOF SKETCH |

**Numerics.** `frozen_run_exact.py` (mpmath 50 digits) reproduces locked T12(iv.b): D = 8.14676240634, π₀({1,2}) =
0.0279141173179, PIP₁ = 0.990618012243, E[P̄₁]−PIP₁ = −0.173974177850; identities to 1e-50; pooled×pooled relative bias
−0.13172 = ¾ closed form. Stops: 6/2,400 = 0.25% (Wilson [0.11%, 0.54%]); S5 6/400 = 1.5% [0.69%, 3.2%]; S5 p=1000 5/200 =
2.5% [1.1%, 5.7%]; "The 6/2,400 PROD-H stops were this guard, all in S5." Code reading: v3_runtime.h guard reads only clock;
guard after every final bridge stage and after final local search; burn-in/measured loops have no resampling, no check.
**What fails.** treating resource_limit as σ(𝓒) launch event (T12(iv.d)); "E[Ẑ | completed] = Z" (counterexample);
pooled Ẑ × primary PIP unbiased (−¾Cov); NUM-only FP validity; uniform-over-R_d (e) via H24 (W1-T24G CE1); "T37 as route (e)
is a category error: the local search is a scan route, so T37 belongs with (d)"; T07 sharpness is data-dependent.
**Needs escalation.** (1) GUARD is an implementation fact (code review; D61 same-seed check). (2) W1-T24G Theorem B / Cor. B-M
unreviewed — "on the critical path for Thm 4". (3) VAL-FP replay study (HQ/OPS). (4) 541-fit interpretation must be confirmed by
ANALYSIS-H2 owners. (5) **Label clash:** "FABLE_REVIEW's '(e′ = T37)' conflicts" — proposes (d⁺)=T37, (e′)=Theorem B. (6)
T06(i) wording in THEORY_PRIORITIES.
**Data remark (541 fits).** If they refer to the final local search, "the 541 fits ... should be posterior-miss fits"; "'local
search repaired 0 fits' is not evidence against the T37 mechanism". (Interpretation, needs confirmation.)
**Outside scope.** Stopped fits concentrated in hardest cell (S5 p=1000 2.5%) — "exact among successful" columns biased;
T26 must use 1_𝒪 inside; the 541 reading.
**Confidence card:** Lemma RO+GUARD .97 (lemma .99; GUARD .95)/done (GUARD needs code check)/no · Prop 2 .97/done/¾-cov uses
locked island independence (iv.c)/no · split .97/done · T34(v) .97/done · Prop 1 .98/done · Thm 4 .90 for (C1)/(a)/(d) (.97
given GUARD), .85 for (e′)/(e-M)/done as implication/Theorem B correctness, (R5)/no · (e′) useful at n=200 0.2/0.3 · T37 →
(d⁺) .95/done (T37 OPEN)/E_LS/"LS0 tweak optional".
**LS0:** "E_LS is T38's crux. Its natural sufficient tweak is LS0"; "With LS0, E_LS ⊇ {S̃₀ ∈ 𝓡_d}".

---------------------------------------------------------------------------------------------------------------------
## W2-PREM — head `988c5f5` (2026-11-02T18:02Z)
**Task.** Discharge the premises of W1-T24G Theorem B ([B]) under G, R, SE, BM-∞; unify with EXP′ ([E]); LH family.
NOTE: uses the status word **"PROVED UNDER"** (an explicit extra condition) — not in the PROTOCOL list; "Never upgraded."

| Label | Where | Statement | Status |
|---|---|---|---|
| Lemma S (shift at a stopping time) | PROOF §1.2 | (label clash with W1-T38E "Lemma S") | PROVED |
| Theorem IND-T | PROOF §1 | EX-S, EX-A: given everything up to stage-T resampling, the N particles' outputs over **L+5** φ=1 rounds are independent Markov chains (K̄₁); across islands too; from engine's one-sequential-stream-per-island discipline | PROVED (EX-S, EX-A) |
| Lemma U(𝔉) | PROOF §2 | uniform log-BF expansion over any n^{A′} family of bounded-size additions with SE: \|R\| ≤ κ_n → 4.16(M+2σ²)/σ²; EXP′ is its within-block instance ("[E] Lemmas 1.1–1.4 are block-free") | PROVED |
| Prop. T2 (τ₂) | PROOF §3.1 | truth removal at 𝒮_a by Gibbs/U/N labels n^{−ω(1)} under SE(s₀+a+2), BM-∞ | PROVED |
| Lemma CMP | PROOF §3.2 | comparison / partial-correlation recursion | PROVED |
| Prop. NL0 / UDEL | PROOF §3.3 | under PG(a) (partner graph, degree D_n, (eD_n+1)^a log^{3/2}n/√n → 0): Λ₂(a) = O_P(...); ε_del(1) = O_P(log n/√n) always; ε_del(a) under PG(a−1) | UDEL(1) PROVED; NL0(a), UDEL(a≥2) PROVED UNDER PG |
| Counterexample EQ | PROOF §3.4 | exact Gram, equicorrelated nulls r, p = n^β, rβ > ½ (r=0.8, β=0.9; G,R,SE,BM-∞ hold): Λ₂(1) ≥ 1−o_P(1), ε_del(2) → 1 | COUNTEREXAMPLE ("asymptotic; PROVED modulo the standard extreme-value facts cited") |
| Prop. B1′ (pointwise addability) | PROOF §4 | P_W(no bad, no progress) ≤ 1 − (1−ε_pt)/\|M(W)\|; BTP unnecessary | PROVED (EX-S, EX-A) (label clash with W2-VT24G "B1′") |
| Prop. PA | PROOF §4 | ε_pt = n^{−ω(1)} under G, R-lite, SE(k), BM-∞ | PROVED |
| §5.1 [B]-family defect | PROOF §5.1 | A = method's neighbour graph includes useless group-mates of the PRESENT hub ⇒ η₁ = O(1) on LH (P_{W*}(U bad)=0.088 at n=1600) | COUNTEREXAMPLE (numerical, reproducible; asymptotic PROOF SKETCH) |
| Theorem B♯ | PROOF §5.2 | Theorem B with monotone look-alike map 𝔄; c₁♯ = max{1−ε_add♯, (1−ε_pt♯)/\|M(x)\|} | PROVED (as modification of [B]'s proof) |
| Prop. TS | PROOF §6.1 | Gibbs truth removal at incomplete states super-polynomially small under TS(𝒲) | PROVED UNDER TS(𝒲); COUNTEREXAMPLE without (cancellation pair θ₂ = −θ₁/r; P(G₁ deletes truth 1) 0.996→0.99993); layered fix OPEN |
| Prop. SW | PROOF §6.2 | swap truth removal O(D′/p)+e^{−Ω(n)} | PROVED UNDER FS(D′, c₀) + p_n/log n → ∞ |
| Prop. TL (TL♯) | PROOF §6.3 | junk additions O_P(2^{g₀}√(log n/n)) | PROVED UNDER ZJL + CS(g₀); bounded-leakage relaxation PROOF SKETCH; random designs OPEN |
| Prop. ULR | PROOF §6.4 | keep useful look-alikes, e^{−Ω(n)} | PROVED UNDER ULR(c₀) |
| Prop. IM (reference bound) | PROOF §7 | β_I(W) ≤ (1−π₀(S°)) + 1{S° bad at W}π(S°)/(π(W)π₀(S°)) | PROVED |
| Prop. IND-M | PROOF §7 | under SCR(S°) (1−π₀(S°) = o_P(1/log n), S° ⊆ S₀) + GS(S°), starts x ⊇ S°: β_I = o_P(1/log n); superset starts S° ⊋ S₀ "**OPEN** (plausibly false at finite n)" | PROVED UNDER SCR + GS |
| Theorem L (LH) | PROOF §8 | all premises on LH (exact Gram, p/log n → ∞), starts S° ⊆ x ⊆ S₀ ∪ 𝔄_LH(M); c_*♯ ≥ min{1/\|M(x)\|, 1/(B+3)} − o_P(1), (L+5)η → 0; N particles ⇒ bound^N | PROOF SKETCH (every component PROVED except FS-neighbour gap and ULR, verified numerically for config B, and cited candidate [E] Thm 5(a)); ULR general LH CONJECTURE |
| Corollary A | PROOF §9 | assembly under PG, TS, FS, TL♯, ULR, SCR+GS: sup_x P_x(S₀ not scored in L+5) → 0 | PROVED UNDER the listed premises |

**Numerics.** IND-T toy: χ² 13.2/9 df (crit 16.9), TV 0.0035. Lemma U (p=24, AR(0.5), 49,152 pairs): max\|R\| 0.63–0.80 vs
κ_n ≈ 20. NL0 EQ vs BLK (s₀=2, r=0.8, p=n^0.9): EQ Λ₂(1) 4.40 → 14.63 (no decay), ε_del(2) 0.3–0.87; BLK Λ₂(1) 1.58 → 0.37,
ε_del(2) 0.34 → 0.051; single-pair EQ divergence "needs n ≳ 10¹¹". LH config B (p=20, five groups of 4, ρ=0.7, ψ=0.5; 6,112
phase-1, 14,893 phase-2 states): TS min loss 0.168; ULR 0.0137; ZJL max \|δ\|/(n−1) = 2e-16; [B] family U-part of η₁ 0.43
(n=1600), 0.437 (n=102400) — no decay; 𝒵♯ U-part = 0.0625 = 4/64 at every n (D′/p term). SH table: 1−π₀(S°) 0.083 (n=400) →
0.0013 (n=1.6e6) (n^{−1/2}); P(Bin(H′,c_*)<8) 0.998–1 (n=400), 0.66–0.88 (1600), 0.139–0.149 (1e5), 0.015–0.031 (1.6e6);
H′η 25–47 → 2.2–3.5.
**What fails.** NL0/UDEL without design condition ("inflated by up to a factor (1+r)"; "same phenomenon [B] saw in S5");
state-averaged drift OPEN; TS under cancellation (potential's accounting, not repair); [B]'s family with neighbour graph;
swap substitutes at fixed p; IND-M for superset starts OPEN; TL♯ in random designs OPEN; rates slow (binomial factor).
**Needs escalation.** (1) Naming: split IND into IND-T (PROVED) and IND-M; "The task file's description of IND as 'open in the
masked regime' conflates them." (2) Independent review of B1′ and B♯ (J* independence; closure (F3)). (3) Lemma CMP + EQ
extreme-value step. (4) LH population inequalities symbolically. (5) Implementation: IND-T rests on EX-S (xoshiro256**
seeded by SplitMix64 of seed·2³²+stream, no jump-ahead); confirm stage-T round counts as terminal (H′ = L+5).
**Outside scope.** [B]'s (R5) "per-particle fresh randomness" — "The code does not use per-particle streams"; "At n = 200 in
S3/S4/S6 [B] saw π₀ concentrating on supersets of S₀. That is exactly the case where IND-M is OPEN" (may bear on T38(b)
delivery); cross-pair substitutes suggest a "missing residual signal" potential.
**Confidence cards:** IND-T .97/done/no · Lemma U .97/done/no · τ₂ .95/done · NL0/UDEL .9/.9 (CE)/done (review CMP) · BTP removal
.92/done (review) · B♯ .9/done (review) · TS .95/done/"no (layered potential would need new proof, not a method change)" ·
FS, TL♯, ULR .85/.7 general · IND-M .9/done; superset starts 0.3/"possibly (... e.g. no independence move at φ = 1 in
terminal rounds)" · Theorem L .85/.75 · Corollary A as useful finite-n —/0.2 single particle/"multi-particle route is the
operative one".
**Disagreement:** with the task file (IND naming) and with [B]'s family A and (R5) wording.

---------------------------------------------------------------------------------------------------------------------
## W2-T26 — head `0e4f1e7` (2026-11-02T17:49Z)
**Task.** T26(i)–(ii): consistency of evidence and PIPs, favourable regime only; premises (T_n+1)Δ_n → 0 and (L_n+4)ρ*_n → 0;
drop secondary PIP; never condition on completion. Files: REPORT.md, PROOF.md only.

| Label | Where | Statement | Status |
|---|---|---|---|
| Theorem A (premise form) | PROOF §1, §3 | EX-A, EX-S, CAL, START, OUT, (Ω) s₀ ≤ K, (P1) (T_n+1)Δ_n → 0 [sufficient (T^max+1)Δ_n → 0], (P1-ex): Ẑ/Z → 1, Ẑ_r/Z → 1, log Ẑ − log Z → 0, max_j\|PIP̂_j − 1\{j∈S₀\}\| → 0, MPM̂ = S₀, all as P(𝒪_n ∧ error > ε) → 0; (A-0) finite-n bounds with b(𝓒) = 2(T+1)Δ_n/(1−Δ_n). No G, R, SE, BM, EXP | PROVED (candidate composition) |
| Lemma 1 (Δ identity) | PROOF §2 | Δ_n = max{1−π₀(S₀), 1−π(S₀)} exactly (T22(iv-b)) | PROVED |
| Lemma 2 (departure) | PROOF §2 | ρ̄ = 1−∏_e(1−K_e(S₀,·ᶜ)) ≤ (B+3)u_π | PROVED |
| Lemma 3 | PROOF §2 | round-start occupancy controls bad-round fraction ⇒ frozen premise (L_n+4)ρ*_n → 0 "redundant — PROVED" | PROVED |
| Theorem B (discharged form) | PROOF §4 | add T03's G, R, SE, BM and T22(iii)'s EXP′, VIS, NL_η, NL_avg(κ): (T^max+1)Δ_n = O_P(log²n[2^B√(log n)n^{−κ} + e_n + √(log n/n)]) → 0; "EXP′ is used only for (T^max+1)(1 − π₀(S₀)) → 0" | "PROVED as a composition, CONDITIONAL" |
| Proposition C (ORTH) | PROOF §6 | XᵀX = (n−1)I_p, p ≤ min(n−1, n^A): G, R, SE, BM-C, VIS, NL_η (η=0), NL_avg (κ ≤ ½), strict EXP′ jointly | PROOF SKETCH |

Key quote: "(T_n+1)(1 − π₀(S₀)) → 0, the only genuinely open input and the only place EXP′ enters (via T22(iii))."
**Numerics** (p=18, B=4, s₀=3; smallest p taking SMC branch). Lemma 1: grid min = endpoint min in 246/246 runs. fav_iid:
(T_ideal+1)Δ_n 6.18 (n=40) → 0.0225 (n=163,840); (T^max+1)Δ_n still 44.9 at n=163,840 ("With T^max = 4,000 it is ≥ 44 even at
n = 163,840", "needs n of order 10⁸–10⁹"); frozen (L+4)ρ* ≈ 1.75 at 163,840 vs ρ̄+u_π ≈ 0.03. masked: 1−π₀(S₀) → 1, T_ideal grows
to 27; (P1) fails. ORTH (p=n/2): max\|R\| 0.164 → 0.113; 1−π₀(S₀) ~ √(log n/n); (T^max+1)(1−π₀(S₀)) 758 → 139. Final-run sims:
every (A-0) bound holds, loose 30–200× (evidence), 50–80× (PIPs); N=50 too. ρ̄ check 0.1162 vs 0.1155.
**What fails.** frozen (L+4)ρ* route "valid but wasteful"; removing (T+1) factor impossible on locked evidence route (T14(i-d));
no locked bound on realised T ⇒ T^max = 4,000 "makes (P1) practically vacuous"; masked: Δ_n → 1, no claim; "Study scale
(n = 200, p ∈ {500, 1000}): ... Δ_n ≈ 1, and SE is impossible. The theorem explains the mechanism only."
**Needs escalation.** (1) Lemma 3's use of T15 at position (b) = T12(i.b) — independent check. (2) Prop. C sketch ("It overlaps
W1-EXP"). (3) OUT: can resource_limit / numerical_failure return partial outputs ≠ potential run? (Felipe). (4) T03 + T02(i)
combined not separately reviewed.
**Outside scope.** masked design: sampler still estimates Z within 1.4–2.1% (N=2500), 16% at N=50 — "T26 is sufficient only";
ORTH κ=½ rate attained, relevant to T38(a) via T11(iii); exact ρ̄ could replace ρ* in T24/T37 statements.
**Confidence card** (qualitative words, not numbers): T26(i) high/high/none inside/no · T26(ii) high/high (Lemma 3 check)/T15 at
terminal prefixes/no · (P1) in R1 high (asymptotic)/medium/EXP′ for actual partition in p≫n designs/no · ORTH compatibility
high/high/χ² tail bookkeeping/no · finite-n relevance "true but loose; vacuous at n = 200 and whenever T^max is used"/—/Δ_n ≈ 1
at study scale/"no (would need a different evidence theorem)".
**Note:** W2-T26 still carries EXP′ as an open hypothesis of Theorem B and does not invoke W1-EXP Thm 1 (only "overlaps W1-EXP").

---------------------------------------------------------------------------------------------------------------------
## W2-VT03R (verifier of W1-T03R) — head `b9f6d9b` (2026-11-02T17:40Z)
Verdict words: VERIFIED / GAP / ERROR ("single-referee verdict from one model family. It is not an adoption").
**Overall verdict:** "**No GAP and no ERROR in the mathematics.**" "Every step is **VERIFIED**." One ERROR in a numerical claim.

Per-result verdicts (REPORT §1 table): E1(a)(b)(c)(d) VERIFIED (exact rationals, 2,779 triples; max R_m/ub = 0.998); m♯ ≤ K
VERIFIED; E2(i)–(iii) VERIFIED (129 cases; needs s₀ ≥ 1 or s₀=0 with n≥5); Prop. E3 VERIFIED ("not a lower bound for the
posterior"); Lemma den′ VERIFIED; T02(i♯) VERIFIED; **Prop. D VERIFIED** (constant √(2/3)/(½+e^{1.01}) = 0.25157 ≥ ¼, margin
0.0016; reproduced); SE_λ, SE_w implied by locked SE VERIFIED; Lemma I, B (B1–B3) VERIFIED; T02(ii♯) VERIFIED; (C1)–(C10)
VERIFIED ((G4) needs no eigenvalue condition — W1's attribution "unnecessary but harmless"); assembly VERIFIED; threshold/R_m
tables VERIFIED; β-min numbers VERIFIED; **row 29: "Deterministic steps ... hold from n ≈ 1.2·10⁵; other thresholds bind earlier"
— ERROR**; row 30 "SE restricted to the comparison unions actually used" — "imprecise wording, not a mathematical error".
No status downgrade of any W1 theorem; confidence card keeps "PROVED (W1); VERIFIED here".

New results:
| Label | Statement | Status |
|---|---|---|
| Lemma A1 | anchored SE_w(m) ⇔ λ_min(G_T) ≥ g for EVERY nonempty T with \|T∖S₀\| ≤ m (interlacing); "Anchoring therefore saves only s₀ columns"; at n=200 SE_w needs "every 100 columns of X to be linearly independent" (spark(X) > 100); SE_λ(j₀) fails for any fixed φ₀ if a null pair has corr 1−1/n | PROVED |
| Prop. W | SE_λ(j₀) needed only in [P3] lem:signal; T03♯(i)–(iii) under R, SE_w(m♯;g₀), SIG(c ≥ L*) | PROOF SKETCH ((iv) needs per-coordinate SIG, not written) |
| Prop. D′ | under T03♯ hyps Π(\|S\|>s₀\|y) ≤ 1−π(S₀) = O_P(r_n): Prop. D refutes the target "only as a size-tail statement under G and R alone" | PROVED |

**Repairs.** R1 (threshold table): δ_n ≤ ½ 115,150 / 130,328; n/5 ≥ … 1,142 / 1,217; **q_n ≤ ½ 2,116,048 / 2,457,025**;
e^{2ε_n} ≤ 4 25,571,897 / 29,755,302 (p = n^{1.17} / n^{1.30}); locked m_n: 127,302 / 2,268,667 / 27,055,513. Replacement
sentence: "…and the proof's own deterministic thresholds (as written) hold only from n ≈ 2×10⁶ (p = n^{1.17}) to 2.5×10⁶
(p = n^{1.30}); the O_P constants are unspecified." "The error makes the n = 200 disclosure *stronger*, not weaker." R2: add
interlacing-equivalence sentence; replace W1 headline 1 by "false for the SE-free size-tail route (T02(i)); under G and R alone
it is false outright (Prop. D)."
**Hidden SE uses:** "none found" (audit of [P3] l. 119, 220, 282).
**Numerics.** W1 scripts reproduce "byte for byte"; Prop. D brute force vs closed form ≤ 1.1e-13; 108/108 on E_n incl. 50
adversarial y; cutoffs 3,4,4,6,8,9 = ⌈½log₂n⌉; deterministic inequalities on 60 designs (iid, equi 0.9, near-collinear), worst
slacks all ≤ 0 (B3 −4.8e-10, C6a −0.096, …).
**Needs escalation.** (1) HQ: correct n=200 disclosure (R1, R2). (2) Paper should not "advertise anchoring as the main
relaxation". (3) Prop. W write-out. (4) T03♯ chain still to cross-family review.
**Outside scope.** se_n200.py not rerun; g₀ size at n=200 open; T04 not checked.
**Confidence card:** E1 .99/.99 · E2/E3 .98/.98 · T02(i♯) .97/.97 · T02(ii♯) .95/.95 · T03♯ .93/.92 · Prop. D .98 · anchored SE
.95 · thresholds "W1 claim: ERROR" .97 · Prop. W PROOF SKETCH .85/.85. All "Method change? no".

---------------------------------------------------------------------------------------------------------------------
## W2-VT24G (verifier of W1-T24G) — head `dba6ff4` (2026-11-02T17:42Z)
Verdict words: VERIFIED / GAP / ERROR. Independent engine `ref_engine.py`, `exact_laws.py` (no W1 code), validated
(π-reversible, residual ≤ 1e-3; fast vs slow TV within MC noise).
**Overall:** "**Theorem B (restated T24): PROVED (candidate), after one repair.**" "There is one GAP, and I fixed it." "I found no
ERROR in Theorem B, Props. U/B1/B2/D/A, Lemmas O/C/P, or Cors. B-unif/B-M/P1."

Per-claim verdicts: round model (R1)(R2) VERIFIED (`draw_order` Fisher–Yates before any step); kernels VERIFIED; (R3)(R4) SR
"VERIFIED in the implementation" (`held` + `eval`), still "to be confirmed by Felipe"; (R5) "VERIFIED under EX-S" (one shared
stream, fresh at stopping times; "not literally 'per-particle streams'"; "there are L+5 rounds at φ = 1 after the last
resampling ... so H = L+4 is conservative"); **Lemma F: "GAP, fixable, fixed"** (closure hypothesis fails in Prop. B2 slot step
and Theorem B (a) at S₀) → Lemma F′; Lemma O, C, P VERIFIED; Cor. P1 VERIFIED (proof), numerics CONFIRMED, "Caveat: shown only at
B = 4" (order factor ~1/17 at B=14); Prop. U "VERIFIED as bookkeeping" ("It does not make η small"); Prop. B1 VERIFIED; Prop. B2
"VERIFIED after the Lemma F′ fix"; c₂ ≥ 1/(B+3)−ε_del VERIFIED; **Theorem B VERIFIED (PROVED, candidate) after the Lemma F′ fix**;
Prop. D VERIFIED; Cor. B-unif VERIFIED; Cor. B-M "VERIFIED; wording GAP" ("'No η → 0 needed' is misleading ... at n = 200 ... B-M is
vacuous unless used with Cor. P1"); Prop. A VERIFIED (proof); **CE1 CONFIRMED (COUNTEREXAMPLE at n = 200); wording GAP**; CE1
asymptotic sketch "PROOF SKETCH, reduced" (Lemma E); **CE2 CONFIRMED**; **§6 NL0 row: ERROR (inside a PROOF SKETCH)**; §6 other rows
"plausible; PROOF SKETCH, not upgraded"; T4a CONFIRMED; **T4b / "S5 masked mode" / π₀-draw repair table: GAP (evidence):
non-production π₀**; scaling table not rechecked; T21 (e′)/(e-M) "VERIFIED with three edits".
No downgrade of Theorem B's status; one wording correction downgrades the scope of CE1's claim (see below).

New / repaired results (PROOF.md):
| Label | Statement | Status |
|---|---|---|
| Lemma F′ (§1) | union-bound form of Lemma F, no closure hypothesis, same bounds | PROVED |
| Prop. B2′ / B1′ (§2) | at \|P\|=1 no deletability premise: c′₂ = 1−H₁ ≥ 1/(B+3); ε′_add excludes S₀∖{j} | PROVED (label clash with W2-PREM B1′) |
| Theorem B′ | Theorem B with ε′_del(1) := 0, ε′_add; c′_* ≥ c_*; x = S₀∪{l}: ≤ P(Bin(H,1−H₁)<1) + Hη₂(1) | PROVED (candidates) |
| Lemma E (§3) | deterministic exit lower bound: exit ≥ o*·[1−Q_T/(B+d+5)]/(B+d+4); limits o* → 1, Q_T → 0 | PROVED; the two limits PROOF SKETCH |
| §4 NL0 correction | equicorrelated inflation is 1+r = 1.3, not (1+r)/(1−r) = 1.86; NL0(1) fails in rate only for p ≫ n^{1/(2r)} = n^{5/3} (not n^{0.58}) | correction; row still PROOF SKETCH |
| §5 structural limit | bound trivially ≥ 1 whenever v(x) > H (H=12 at n=200) | "observation, PROVED"; multi-step-per-round bound OPEN |

**Wording repair:** "H24 'as written' is satisfiable, trivially, with a_n = 0 and η_n = 1. What fails is its *asymptotic*
input (L+4)η_n → 0." Escalation: "Do not cite 'H24 is false'; cite 'H24's asymptotic input is false in correlated designs (CE1,
Lemma E)'."
**Numerics.** CE1 (20000 reps): seed 1 S1 0.16–0.22, S2 0.62–0.78, S3 0.90–0.96, S4 0.89–0.96, S5 0.93–0.97, S6 0.72–0.95;
seeds 2–4 S2–S6 0.67–0.98; exact lower bound P*_exit ≥ 0.39 in every S2–S6 cell (≥ 0.53 S3–S6); (L+4)·exit 7.5–11.8 (S2–S6).
CE1 scaling: S2 0.61–0.85 (n=200) → 0.95–0.97 (n=3200), S3 → 0.98 — exit does not decay. CE2: brief's form fails in 395/1050
(v,H,c) cases (e.g. v=2, H=12, c=1/20: 0.88 > 0.74). Cor. P1 min a₁ 0.139–0.439 (all ≤ simulated). Repair from π₀ draws with
production packing: 100% within 12 rounds; S5 round 1 0.19–0.25 (W1: 0.11–0.12); v at π₀ draws: median 2 (S1–S2), 5 (S3/S4/S6),
8 (S5), max 17; v > 12 in 10% of S5 c=0.5 draws. B2 at a=1: c₂ 0.326–0.469 (= W1), c′₂ 0.431–0.500; η₂(1) 0.37–0.64; simulated
P(no exit, not scored) 0.040–0.094 ≤ bound. NL0 inflation: median ratio 1.08 → 1.21 for p = 1e2 → 1e6 (→ 1.3). Production packing:
S5 π₀ mode misses truth 6 (c=1) or 6 and 15 (c=0.5).
**T21 route (e′) edits (§6).** (1) statement: "select a particle at a state x ≠ S₀ using only the available past"; β(x)
replaces (1−a_n)^H + Hη_n; delete H24. (2) asymptotic paragraph: Hc_*(x) → ∞, v bounded, Hη(x) → 0, or via Prop. D. (3) (e-M)
and one-round Cor. P1 product. "**No uniformity over an eligible set is needed**". "Status of (e′). VERIFIED as an implication."
**What fails (referee routes).** slot argument (only Lemma F closure); B1 truth-for-truth swaps — no break; V at phase boundary
— no break; (R5) shared stream — holds under EX-S; useful at n=200 fails: Hη ≥ 12 × 0.37 > 1, and v > H.
**Needs escalation.** (1) retire H24 (wording above). (2) independent check of Lemma F′ and B2′. (3) Lemma E's two limits.
(4) non-vacuous finite-n single-particle bound "genuinely OPEN, and is the real obstacle to Thm 3 at n = 200". (5) Felipe:
confirm SR. (6) "W1's Python block packing ≠ production" — use `v3_blocks.h` rule.
**Outside scope.** Cor. P1 at production B=14 unmeasured — "'0.86^{N₁}' should not be quoted for production until it is
measured"; final run may use H = L+5; Theorem B "not the operative mechanism at n = 200" — data point to drift with averaged rates.
**Confidence cards:** Theorem B/B′ .95/done (needs F′/B2′ check)/no · Prop. U .95/done/"it only relocates the problem into η" ·
Cor. P1 .98 (proof)/done/a₁ at B=14 · Cor. B-M / (e-M) .95/done/delivery (T38) · CE1 .93/.8/o* → 1, Q_T → 0 · CE2 1.0/done · T21
(e′) .93/done (text edits) · asymptotic premises (with NL0 fix) .7/.45/IND masked, TS/BTP cancellation, NL0 dense correlation ·
useful finite-n single-particle repair at n=200 0.6 (some bound exists)/0.2/"v > H vacuity and O(1) leakage"/"no (H = L + 5 is
free)". All "method change? no".

---------------------------------------------------------------------------------------------------------------------
## Cross-branch notes: agreements, disagreements, inconsistencies

1. **Literal TD(d,0), d ≥ 1.** W1-T37R Prop 1 (PROVED): unsatisfiable on every design, P₀ = 0. W1-T38E §6.4 COUNTEREXAMPLE
   (swap dominance, ≈ ½log n + log p) and confidence 0.05. Consistent in direction; T37R's is the stronger (exact) statement;
   T38E's "0.05" card is looser than T37R's PROVED impossibility. Both: replace by TD′ (T37R: TD′_∞/TD′_P/lattice; T38E: TD′ or
   GP(d); GP(2) fails at 4 states in CF2 — same "truth deleted by two proxies / combination look-alike" phenomenon as T37R Exp 3).
2. **Cap ℓ < s₀+d.** T37R: needs only ℓ ≥ a+d; T38E: "path length \|S̃₀ Δ S₀\| ≤ ℓ_n + 1"; W2-BOOK (d⁺) keeps the term
   1{ℓ < s₀ + d} (older form).
3. **H = L+4 vs L+5.** W1-T24G and W1-T38E (REPAIR(a_n, L+4)) use L+4; W2-PREM (IND-T, H′=L+5), W2-VT24G ("H = L+4 is
   conservative"), W2-BOOK (H ≤ L+5) all say L+5 rounds at φ=1 after the last resampling.
4. **(R5) / IND.** W1-T24G asks for "per-particle streams"; W2-PREM and W2-VT24G: code uses ONE sequential stream per island,
   (R5) holds under EX-S (IND-T PROVED). W2-PREM: W1-T24G's "IND(𝓕)" (independence-move bad acceptance = IND-M) ≠ task file's
   IND (trajectory independence = IND-T).
5. **NL0 threshold.** W1-T24G §6: equicorrelated nulls fail "for p ≳ n^{0.58}" (inflation 1.86) — W2-VT24G: ERROR, inflation
   1+r = 1.3, threshold p ≫ n^{5/3}. W2-PREM independently: inflation "up to a factor (1+r)", EQ counterexample when p^r ≫ √n
   (r=0.8, p=n^0.9) — consistent with VT24G's corrected form. All agree NL0 is a genuine design condition.
6. **W1-T24G evidence on non-production π₀** (W2-VT24G GAP): W1-T24G's start-law claims ("S5 masked", T4b, S3/S4/S6 π₀ on
   supersets via double counting) used scipy pre-order packing ≠ `v3_blocks.h`. W2-PREM's Outside-scope remark ("At n = 200 in
   S3/S4/S6 [B] saw π₀ concentrating on supersets") rests on those non-production numbers (and on p=20 mimics, not n=200 data).
7. **W1-T24G's repair family 𝒵(x)**: W2-VT24G VERIFIED Theorem B as a finite inequality, but W2-PREM shows (COUNTEREXAMPLE, §5.1)
   that with A = neighbour graph η₁ = O(1) on LH (useless look-alikes); fix Theorem B♯. Not a contradiction (VT24G checked
   correctness, PREM usefulness), but VT24G did not flag the family defect.
8. **H24.** W1-T24G: "H24 as written is false"; W2-VT24G: wording GAP — only its asymptotic input fails. W2-BOOK cites "the
   false H24". Use VT24G's wording.
9. **Cor. P1 "0.86^{N₁}"**: W1-T24G calls it non-vacuous at n=200; W2-VT24G: shown only at B=4, not to be quoted for production
   B=14. W2-BOOK relies on Cor. P1 for the non-vacuous (e-M).
10. **Label clashes.** "Lemma S": W1-T38E (ESS share) vs W2-PREM (stopping-time shift). "B1′": W2-PREM (pointwise addability)
    vs W2-VT24G (scoring sharpening). "Prop. D": W1-T03R (counterexample) vs W1-T24G (drift form). "E1": W1-T03R Lemma E1 vs
    W1-T38E Prop. E1. "Theorem A/B": W1-T24G B (T24), W1-T37R A/B/C (T37), W2-T26 A/B (T26), W1-EXP Thm 1–6. "(e′)": FABLE_REVIEW
    (= T37) vs W1-T24G/W2-BOOK (= Theorem B). "IND" two meanings (W2-PREM).
11. **EXP′ status.** W1-EXP Thm 1 PROVED (candidate) EXP′ (any regime, SE-blk); W2-PREM Lemma U generalises it (constants agree:
    0.52/c_* = 4.16(M+2σ²)/σ²); W2-T26 Theorem B still lists EXP′ as an open hypothesis ("the only genuinely open input") and
    proves ORTH only as a PROOF SKETCH — not yet integrated with W1-EXP.
12. **n = 200 / study relevance.** All runs: theory is asymptotic only at n=200. W1-T03R: SE rank obstruction removed by cap K,
    β-min fails 43–48×, thresholds (corrected by VT03R) n ≈ 2×10⁶. W1-EXP: SE-blk holds at n=200 (φ₀² ≥ 0.06); masking
    explained by weak-signal masking (CONJECTURE); S2/S5 in neither regime. W1-T37R: binding constraint at n=200 is posterior
    dominance; 13/36 c=0.5 datasets S₀ not a local max. W1-T24G/W2-VT24G: Theorem B vacuous at n=200 (Hη ≥ 4.4; v > H); repair in
    simulation 100% by 12 rounds. W2-T26: Δ_n ≈ 1 at study scale. W2-BOOK: 541-fit reading = posterior-miss fits (if final
    search); stops 0.25% all in S5.
13. **LS0.** Only W1-T38E (Theorem E3, recommends (b1)+LS0 as main masked route; "yes, minor" method change) and W2-BOOK (E_LS
    crux; "LS0 tweak optional"). **Common σ²:** not mentioned in any of these ten branches.
14. **Packing caveats agree:** W1-EXP (LH needs linked hubs in different blocks; at n=200, B=14, two groups per block) and
    W2-VT24G (W1-T24G's packing ≠ production) both show π₀ conclusions are sensitive to the partition rule.
15. **Status-word deviations.** W2-PREM uses "PROVED UNDER"; W1-T24G/W1-T38E/W2-BOOK/W2-T26 use "PROVED ... as an implication /
    given inputs / CONDITIONAL"; W1-T03R "PROVED (candidate)"; verifiers use VERIFIED/GAP/ERROR/CONFIRMED. W2-T26's confidence
    card uses words ("high/medium") instead of probabilities.
