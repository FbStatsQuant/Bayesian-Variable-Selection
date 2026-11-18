# W3-DIST — council round R1, seat `opus` (Claude Opus 5.5, Claude Third, effort high) — blind first read

Frozen content reviewed: `reviews/MANIFEST_R1.txt`, first line `MANIFEST c7d74e49a9e5a05fb4c9457f6ccf3bb7c83cb85ca00bf49e47d3d8f4a7c8834d`.
`python3 -B Theory_work/Wave3/tools/manifest.py verify …` returned `verify: OK` before reading. I read only the files that
the brief allows. I did not open any other file in `reviews/`, any LOG, CHECKPOINT, DEPS, ROUTES, PLAN, `briefs/`,
`work/api_attempts/`, `work/prior_probe/`, `work/C_size/X12.md` or `lemmas/X_route_a.md`, and I used no git command on
the ticket folder.

## Verdict summary

I re-derived, line by line, every step on the path of the headline. That covers Lemma X §0–§7 and Lemma X′ (§9), and
DIST-1 and DIST-2 from Lemmas H, T, X and X′ (`lemmas/DIST12.md`). It also covers Lemma T, including its self-contained
VC inequality (Proposition R), Lemma H, DIST-3, Lemmas S and V, Proposition NEC, the bridges B0, B1, B2-core, B2 and
B3, and the assembly of Theorems A and B. Last, it covers Lemma P6, DIST-C and Corollary C, checked against the pinned
code (`v3_run.R`, `cpp/v3_ledger.h`, `cpp/v3_core.cpp`, `cpp/v3_util.h`, `v3_calib.R`, `v3_preprocess.R`, `cpp/v3_score.h`).

I found no incorrect or unproved step. The key lemma has the following steps, all correct:
- the fractional moment λ = (4A+1)/(4A+2);
- the exponent A(1−λ) − λ/2 = −¼;
- the bound λ(1+ε₃) ≤ 1 − 1/(8A+4);
- the union device through S ∪ S₀, which costs 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2};
- the size tail above m_n(t);
- the far-model bound, which uses Λ ≥ 32C_x, 8C_P, 8B/σ² and 48/log 2;
- the good-model bound;
- the single n₀ that serves the whole range of t.

Lemma T holds exactly as stated, with no condition on the law of x. The transfer is applied at deterministic sparsity
levels d₁ and d₂, and the intercept is controlled by its own event 𝓘_t. The constants are law-free, as Theorem A's
uniformity requires.

The named point holds: Corollary C's conclusion about the reported most probable model is correct for the code as
pinned (details under G6).

I hold one finding of kind S, minor and repairable by one sentence (R1-opus-01). Consequence (c) of DIST-1, and the
proof-file paragraph it rests on, describe the rate as being "of order (1 + s₀^r) log p_raw/n", or
"(1 + s₀^r)(A + 1) log n/n". That makes the rate look linear in A. In fact the radius constant C, which those same
sentences say depends on A, grows like A + 1, so C² grows like (A + 1)². The sparsity dependence that TC3 fixes is
proved exactly as stated. The A-dependence is stated more strongly than the proofs give, unless A is read as fixed.
Because I hold this S finding, the brief requires gates=FAIL. The mathematics is otherwise acceptable as checked
mathematics.

## Gate table

| gate | verdict | justification (what I re-derived; evidence) |
|---|---|---|
| **G1** correctness of every step | **PASS** | **Lemma X** (`lemmas/X.md`). §1, Lemma V(a): both Young bounds and the monotonicity of Q^{(c)}_T in c and in T (`X.md:74-76`). §2: the failure probabilities of N1, N2 and N3 (N3 sums to (2/(e−1))e^{−t}) and the consequences E1–E4 (`:87-98`); E2's two-sided bound on s_y² uses N3 at S = ∅. E4 uses M₀ ≥ (s₀+1)/2, so C_d = 34 is free of s (`:97-98`). §3, Steps 1–5 (`:105-134`): the pointwise bound; det(I − λ₁D′)^{−1/2} ≤ (8A+4)^{(s₀+j)/2}; Jensen with (ND); `lem:prior`(e), for which I re-derived C(p−s₀,j)C(2p−1,s₀)/C(2p−1,s₀+j) ≤ (j+1)^{s₀}; the exponent −¼; the geometric sum ≤ 2n^{−(j₁+1)/8} ≤ 2e^{−4t}; interlacing for D_{S′}/D_S ≤ (n+1)^{\|S′\|−\|S\|}; the multiplicity 2^{s₀} − 1; Markov at power λ with C₅. §4 (`:140-147`): q_{k+1}/q_k = (p−k)/(2p−1−k), so Σ_{k>m}q_k ≤ 2^{−m}; R_m√D√n ≤ 2n^{−1/2}e^{−3t}; the bound Λ″ ≤ t/2 + 1 + B/(2σ²); I checked [P1] `thm:Ta` and the proof of `lem:den` in `PROOF_v3.tex` (lines 255-265, 336-356). §5: Δ ≥ λ_Sσ²t/4 and ν log(1 + Δ/(2b + Q₀)) ≥ 3t. §6: the centre, the scale (C_β), the v-step (\|g\| ≤ ½ through condition (f)) and the θ-step. §7: 6e^{−t} ≤ e^{−t/2} and 7e^{−t} ≤ 2e^{−t/2}. §9 (X′): the t′ = t log n bookkeeping, including t′/n ≤ √(t/n). **DIST12** (`lemmas/DIST12.md:24-88`): d₁ log n ≤ 34t; the η² bounds; the inclusion of the bad sets with C′ = 33; the probability budget 3e^{−t/2}; the predictive bound by convexity. **Lemma T** (`work/B_transfer/T.md`): Cantelli, Hoeffding, Sauer–Shelah and Dudley (T1–T5); the growth bound C(P,d)Φ_{d+1}(m)²; Proposition R Step 1 (≥ ½ by Cantelli, nη² ≥ 25) and Step 2 (13W > 3N + 8nη², exponent 48nη²/169); nη² > 36; the layer cake; the measurability of the supremum. **H**: the affinity A·B and 1 − A ≤ (r−1)²; the identity H-id with dropped columns. **DIST-3** (`DIST3.md`): G2–G4, D1–D6, the S₀-conditional variance and mean, the (TR₀) transfer, Fubini, and the in-probability corollary. **S**: Steps 2–7 and Corollary S.1. **V**: (0.i)–(0.iii), Woodbury, Sylvester, the comparison by FFᵀ/FᵀF and Weyl, and the eigenvalue-wise bounds g_{1/c} ≤ c·g₁ and g₁ ≤ c·g_c. **NEC**: f(Nτ²) = d; the plug-in bound with the bracket = 1 − h; (2.1)–(2.3); the table of event probabilities (total ≥ 0.6); Step A (Σ ≤ e³(1+βL)/√n); Step B (e_k(a) ≥ A^k/(2k!), c₃, c₄); Step C (Cauchy–Schwarz); the Corollary with T = max(M₀, 2/c). **Bridges**: B1 (the three Chernoff exponents 1/512, 1/576, 1/8); B2-core (moments (4)–(5), exponents 1/6400 and 1/768, the net arithmetic 0.5436 ≥ ½, the union bound with c₂ = 10⁻⁵); B2 (λ_min(G_T) ≥ c_ψ/4, D_{S∪j}/D_S ≥ φ(λ_min), the window inequality (d)); B3 Steps 0–6; ASSEMBLY §1–§3. **P6/DIST-C/Cor-C**: Lemma R (all three cases), Lemma M, Corollary R1, Lemmas U and W, (C-0), C-i°, (α-det), (C-iii)(a)(b). No step is wrong or unproved. The only flawed sentence is a dependence remark (R1-opus-01), counted under G5. |
| **G2** hypotheses used = hypotheses stated | **PASS** | *DIST-1.* The proof uses 𝒟_n, (E; M), (C; M′), (ND; c_D, m_n(t)), (RD) and the independence of ε from X^r (`DIST12.md:50-63`), matching `STATEMENT.md:74-77`. (ND) is used only for j₁ < j ≤ min(m_n(t), p − s₀) (`X.md:136`), within its stated range. *DIST-2.* (E) and (C) only; c_D never enters (`X.md:218-222`). *DIST-3.* 𝒟_n, (E), (L₀), (TR₀) and n ≥ 2s₀^r; p ≤ n^A is not used (`DIST3.md:16-17`), as stated. *Lemma S.* Only B_T(ϑ) ≤ B and ‖μ‖² ≤ nM. *Lemma V.* No design condition. *TC3* (`TARGET.md:115`). C_X is free of s (`X.md:38`), and so are C_T (`DIST12.md:34`) and C = (C_X² + C_X/2 + 1 + C_T)^{1/2}. M₀ ≤ 16 + 4(1+s)(A+1) + 3B/(2σ²) (`X.md:39-40`), with s = s₀^r the raw sparsity because the transfer uses supp β*. Proved as fixed. *§1R against TARGET §6.* The texts are byte-identical (diff). Theorem A uses (A1)–(A5) with window q_n (B1, B2, B2-core). The sentence without (A4) uses only single-coordinate (A3) and (A5). Theorem B uses (A1)–(A6) and W3-POST:Thm-1 item 6, whose hypotheses B3 verifies against `W3-POST/STATEMENT.md:63-100` (I checked (F_λ), (F_w), m♯_n and the BM-∞ envelope b_n²nψ/(8 log n)). *TC1–TC9.* Each is matched by what is proved. TC8 is the deterministic parts plus the delivery statements intersected with {completed}. |
| **G3** no hidden assumptions | **PASS** | Transfer event vs interface events: no independence is used, only a union bound (`DIST12.md:61-63`). Conditioning on the design: Lemma X is applied given X^r with e = Uᵀε ~ N_N(0, σ²I), and U is fixed. Moments of x: none in Lemma T; (TR₀) is an explicit event in DIST-3. Intercept: ε̄ is controlled by 𝓘_t (`DIST12.md:39-40`) and in DIST-3 by 𝓔¹. Response scale: B0, through W3-MISR:R′(a′), pathwise with the plug-in intercept. Raw vs retained: d₁ and d₂ use p_raw and s₀^r (deterministic); Lemma X, m_n(t) and (ND) use p_ret and s₀ (design-measurable); a dropped true column is handled in H-id (`H.md` §H.6). True columns constant in the sample: covered. s₀^r = 0: covered (ρ′ = 0, S₀ = ∅; NEC is exactly this case). Small p: d_i = min{p_raw, ·}, B2's window is min{p, ·}, and p_ret < 2 goes to the remainder. Measurability: Ω_T (`T.md` Step 6), 𝒢_n and 𝔈 (`DIST3.md` §4), 𝔅_u by Tonelli, and the cutoff m_n(t) is X-measurable. |
| **G4** imports: status and content | **PASS** | The only premise of the master theorems is T01 ([P1] `thm:T01i`, `lem:spec`, `lem:slab`, `lem:num`, `thm:Ta`, the proof of `lem:den`, `lem:chi`, `lem:prior`). The passages used say what is quoted; I checked `PROOF_v3.tex:40-58, 250-265, 336-356`, and the IG(0.51, b) representation with ν = 0.51 + N/2 = 0.01 + n/2 matches `cpp/v3_score.h:57`. The statuses in `REPORT.md` §1 carry "conditional on SOP:TH09" on every theorem about the coded posterior, "conditional on W3-POST:Thm-1" on Theorem B and on B3's last sentence, and the W3-SAMP conditions on DIST-C's delivery statements. W3-MISR:R′ ("PROVED-CHECKED; council R2") and W3-POST:Thm-1 ("T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)") match `claims.tsv`. The W3-SAMP versions and statuses are quoted in their form before HQ's relabel of 2026-11-16 (E-01). No status is upgraded in effect, because DIST-C already carries SOP:TH09. Cross-family check on file for every new lemma, according to REPORT §1–§2: X, X′ (L1, BR1); DIST12 (L6); H, T, DIST3 (L3); S, V (L5); D_output (L2, D3); bridges (L4); NEC (L7). |
| **G5** constants and rates | **FAIL** | Re-derived: every constant of `X.md` §0. M₀ is bounded through log C₅ ≤ 4(1+s)(A+1) + 3B/(2σ²). Conditions (a)–(g) are monotone in t and imposed at t = n^{1−κ₀}, so one n₀ serves the range. Also checked: C_T and C_T′ (`DIST12.md:34-35`); C_rad and n₀ of DIST-3; c_B, C₁ and C_S of Lemma S; the reader constants (c_A = c_⋆/(2C_⋆²), C₁ = max{C′/C², 1 + s + (sA + s + 5)/log 2}); n_B and n_R; the uniformity in M ≤ √n/log n (n^{−cM} ≥ e^{−c√n}); and the law-free reading (R-a). **Failure:** R1-opus-01. The rate gloss of DIST-1 (c) says ε_n² is of order (1 + s₀^r) log p_raw/n (`STATEMENT.md:85-87`), and `DIST12.md:69` says (1 + s₀^r)(A + 1) log n/n. But C² ≥ C_T = 4[34(A+7) + 8] and C_X ≥ 128(34(A+1) + 2), so C² ≍ (A+1)²: inline computation of the X.md formulas gives C²/(A+1)² ≈ 2.5–4·10⁷ for A = 1…20. The proved bound is therefore of order (1 + s₀^r)(A+1)³ log n/n, which is (1 + s₀^r)(A+1)² log p_raw/n. |
| **G6** fidelity to code; honesty of scope | **PASS** | I verified every code pin of `STATEMENT.md` §2 against `Scripts/SMC_BVS/core/`: `v3_run.R:142` (`out$hpm <- led$hpm$model`), `:154`, `:159-162`, `:163`, `:210`; `cpp/v3_core.cpp:358-366`; `cpp/v3_ledger.h:43-56` (struct to :64), `:49-56`, `:78`. The coded prior and ν = a₀ + n/2 match `cpp/v3_score.h:57-70`, and p = p_ret matches `v3_preprocess.R:111-113`. **Named point (Corollary C, HPM):** see the next paragraph; the reader sentence is proved as worded. NEC's "what this does not say" is accurate. The stretch items are labelled open. The comparisons in `TARGET.md` §2 agree with `SONG_LIANG_MAP.md` rows 1–4 (bounded predictors for Thm 1, Condition 1 for Thm 2, Condition 2 for (16)). REPORT and its registry blocks say no more than the statement, except that TARGET's P3 row repeats the wording of R1-opus-01 (same repair). |

**Named point, line by line (Corollary C, reported most probable model).**

(1) *What "reports" means.* `v3_run.R:142` sets `out$hpm <- led$hpm$model`. This is the final-run ledger's running
best `hpmS`, exported by `cpp/v3_core.cpp:364`. It is the field the method reports as most probable. It is set the same
way with LS0 enabled: LS0 scores go to the same ledger (`v3_core.cpp:465-478`).

(2) *Same offers.* On a completed run, `offer_hpm` is called only inside `offer_stores` (`v3_ledger.h:89-91`), which
also calls `top.offer(F, S)`. Its only other call, `v3_core.cpp:502`, is inside the `catch (NumericalFailure)` block,
which sets status "numerical_failure". The other `top.offer` call, `v3_core.cpp:549`, belongs to the exact-enumeration
branch, which is out of scope. So the store and the running HPM receive exactly the same set 𝓜 of offers.

(3) *Same order.* `TopCmp{true}` (`v3_ledger.h:37-41`) and `hpm_better` (`v3_util.h:121-126`) are the same strict total
order: larger F, then smaller |S|, then `lex_less`. Lemma R's induction (`P6_DISTC.md:186-209`) covers quick-reject,
duplicate, insert and erase, and is correct, so 𝒯 = top_{40p+1}(𝓜) in that order, and `hpmS` is the ≺-first element of
𝓜.

(4) *Ties and exact arithmetic.* Under EX-A, π(S_true) > ½ makes S_true the unique F-maximiser over Ω (Lemma U:
F = log Z + log π). So no tie can arise and the tie rule is irrelevant. In floating point the conclusion holds for the
computed order (Remark 6.3), but it is not claimed there.

(5) *Conclusion.* If S_true ∈ 𝓜, then S_true is first in 𝒯, Ŝ = S_true, and π(𝒯) ≥ π(S_true) > ½. The conclusion is
vacuous when a true column is dropped or |S_true| > K, because then S_true ∉ Ω.

(6) *"Scored".* Under the reading "scored in the final run or carried into it", which is the list's own description,
this is Corollary R1(ii). Under the broader reading "scored anywhere, calibration included", the claim rests on P6
Remark 6.2, which the file marks as a code reading that is not used. I checked it myself:
- `cpp_cal_new` creates one calibration ledger per fit (`v3_core.cpp:603-614`, called once in `v3_calib.R:148`);
- that ledger is shared by the pilot, the diagnostics and the single escalation;
- all calibration score events go through the same `Ledger::event`/`offer_stores`;
- `cpp_cal_export` unions its three stores (`v3_core.cpp:722-735`), and the final run offers that union (`:418-428`);
- `cpp_cal_V` rescoring offers nothing new.

So a unique maximiser scored in calibration is in 𝓜 too. The reader sentence is true under either reading. E-02
suggests making the reading explicit.

## Per-claim table

| id | decision | note |
|---|---|---|
| W3-DIST:DIST-1 | ACCEPT | display (1.1) and consequences (a), (b), (d), (e) proved; the A-dependence wording of (c) needs R1-opus-01 |
| W3-DIST:DIST-2 | ACCEPT | |
| W3-DIST:DIST-3 | ACCEPT | |
| W3-DIST:DIST-C | ACCEPT | |
| W3-DIST:Thm-A | ACCEPT | |
| W3-DIST:Thm-B | ACCEPT | conditional on W3-POST:Thm-1, as labelled |
| W3-DIST:Cor-C | ACCEPT | named point verified (G6) |
| W3-DIST:H | ACCEPT | |
| W3-DIST:T | ACCEPT | |
| W3-DIST:S | ACCEPT | |
| W3-DIST:V | ACCEPT | |
| W3-DIST:X | ACCEPT | |
| W3-DIST:X' | ACCEPT | |
| W3-DIST:NEC | ACCEPT | |
| W3-DIST:P6 | ACCEPT | |
| W3-DIST:B0 | ACCEPT | |
| W3-DIST:B1 | ACCEPT | |
| W3-DIST:B2core | ACCEPT | |
| W3-DIST:B2 | ACCEPT | |
| W3-DIST:B3 | ACCEPT | |

## Findings

**R1-opus-01 — S (minor; rate wording; blocks only by the gate rule).**

*Location.* `STATEMENT.md:84-87` (DIST-1 (c)); `lemmas/DIST12.md:66-70` ("Dependence on the sparsity"); repeated in
`TARGET.md:30` (P3 row: "ε_n² of order (1 + s₀^r)(A + 1) log n/n, i.e. (1 + s₀^r) log p/n for p = n^A (for fixed σ*², M, M′)").

*Problem.* These sentences hold (σ*², M, M′) fixed but let A vary: they write the factor (A + 1) and identify the rate
with (1 + s₀^r) log p_raw/n. That presents the rate as linear in A = log p_raw/log n. The proved radius is
ε_n² = C²M₀ log n/n with C = (C_X² + C_X/2 + 1 + C_T)^{1/2}. Both C_X and C_T grow linearly in A:
- C_X ≥ 4Λ ≥ 128·C_x = 128(34(A+1) + 2) (`X.md:34-36`);
- C_T = 4[34(A+7) + 8] (`DIST12.md:34`).

So C² ≍ (A+1)², and the proved bound is of order (1 + s₀^r)(A+1)³ log n/n = (1 + s₀^r)(A+1)² log p_raw/n. The claim
"of order (1 + s₀^r) log p_raw/n" is therefore not proved as an A-dependence. It is correct only when A is treated as
fixed, which the setting does ("A ≥ 1 fixed", `STATEMENT.md:22`), but the parenthetical "(for fixed (σ*², M, M′))"
explicitly leaves A free.

The C_T part is not an artefact of loose bookkeeping. The transfer runs over d₁ ≈ 32t/log n sparse directions at cost
d₁ log(ep/d₁)/n ≍ A t/n, and the size cut s₀ + 32t/log n with t ≍ (1+s)(A+1) log n admits about (A+1)s extra variables.
So this route cannot give a rate linear in log p_raw.

TC3 itself ("M₀ = O((1 + s₀^r)(A + 1))", with C free of the sparsity) is proved as written. The finding concerns only
the gloss on ε_n².

*Repair (either).*
- (a) Write "for fixed (A, σ*², M, M′)" in STATEMENT (c), DIST12 D.4 and TARGET's P3 row, and say "of order
  (1 + s₀^r) log n/n".
- (b) Keep A free and state what is proved: "C ≤ K(σ*², M, M′)(A + 1), so ε_n² ≤ K′(σ*², M, M′)(1 + s₀^r)(A + 1)³ log n/n".

No statement or target clause changes. The tag would be EQUAL on TC3 (or WEAKER on a descriptive sentence).

**E-01 — E (status quotes).** `STATEMENT.md:432` and `REPORT.md` §5 quote W3-SAMP:D@2.1.1, LT♯@2.0.1, C@1.1.1 and
TR@2.1.1 as "PROVED-CHECKED". The registry now lists D@2.1.3, LT#@2.0.3, C@1.1.3 and TR@2.1.3 as "PROVED-CHECKED,
conditional on SOP:TH09" (HQ relabel, `HQ_CONDITIONAL_STATUSES.md`, 2026-11-16). The effective status of DIST-C is
unchanged, because it already carries "conditional on SOP:TH09". Refresh the versions and quote the conditional form.

**E-02 — E (Corollary C wording).** At `STATEMENT.md:233`, "If a completed run scored the true model" should name the
set: "scored in the final run or carried into it (the offered set of the list's description)". Alternatively, promote
P6 Remark 6.2, which I confirmed in the code (see G6), to a checked lemma so that the broader reading is covered by a
proof.

**E-03 — E (stale annotation).** `STATEMENT.md:325` ends Lemma H's proof sketch with "(not line-checked.)", while
`REPORT.md` §1 records H as line-checked (L3 VERIFIED). Remove the annotation.

**E-04 — E (Lemma V (c) wording).** `STATEMENT.md:352` writes "eᵀD′e ≤ σ*²χ²_{d_J} + ‖P_{S₀}e‖²". The proved statement is
the pathwise bound eᵀD′e ≤ ‖(P_S − P_{S₀})e‖² + ‖P_{S₀}e‖² with an exactly χ²_{d_J}-distributed first term
(`V.md:7-9, 37-39`). Use the proved wording.

**E-05 — E (NEC table).** `NEC.md`, the 𝓔₂ row: P(Σ_{j≤p′}z_j² > 2p′) is bounded by 2(p′+1)/(p′−1)², not exactly 2/p′.
Both are o(1), and nothing downstream changes.

**E-06 — E (B2 chain in STATEMENT).** `STATEMENT.md:401` drops the factor n/(n−1) between Σ̂^z (normalised by n) and the
sample correlation. The displayed lower bound stays true because the omitted factor exceeds 1. `B2.md` (a) has the
clean chain with λ_min ≥ c_ψ/4.

## Better-theorem proposals

1. *Explicit A-dependence of DIST-1.* Record C = O(A + 1) and ε_n² = O((1 + s₀^r)(A + 1)³ log n/n) for fixed
   (σ*², M, M′). The A² in C_v (variance clause) is loose: |Q_S − ‖e‖²|/n ≤ C_Q t/n ≪ √(t/n), so C_v can be made free
   of A. The radius would then be driven by C_X and C_T alone.
2. *Corollary C, broader retention.* Prove Remark 6.2 (unique F-maximiser scored by the calibration ⇒ in 𝓜) as a code
   lemma. The code supports it: one persistent calibration ledger, the export of the union of its stores, and the
   offer to the final ledger.

(The proofs already give the strengthenings that SW1 listed in `TARGET.md` §4; not repeated.)

## Overall score

**8.6 / 10** (C, S and F only). No C or F finding. One minor S finding (R1-opus-01), about how the rate depends on A,
repairable by one sentence. The mathematics of every claim is otherwise correct as written. Under the brief's rule the
gates fail on that finding alone.

## Checks performed

- Manifest verified (`verify: OK`).
- Full re-derivation of `lemmas/X.md` §0–§7 and §9, `lemmas/DIST12.md`, `work/B_transfer/{H,T,DIST3}.md`,
  `work/C_size/{S,V}.md`, `lemmas/NEC.md`, `work/E_bridges/{B0,B1,B2core,B2,B3,ASSEMBLY}.md`,
  `work/D_output/{P6_DISTC,COR_C}.md`.
- [P1] passages actually used: setting and contrast model (`PROOF_v3.tex:40-58`), `thm:Ta` (:255-265), the `lem:den`
  proof (:336-356).
- W3-POST Theorem 1 definitions and item 6 (`W3-POST/STATEMENT.md:30-100`), against B3.
- `SONG_LIANG_MAP.md` rows 1–4 and 9, against `TARGET.md` §2.
- Code: `cpp/v3_ledger.h` (whole file); `v3_run.R:110-215`; `cpp/v3_core.cpp:336-512, 596-735`; `cpp/v3_util.h:115-126`;
  `v3_calib.R` (calibration state creation and export, by grep); `v3_preprocess.R:105-118`; `cpp/v3_score.h:36-72`.
- Registry statuses (`claims.tsv`) of SOP:TH09, W3-POST:Thm-1, W3-MISR:R′, W3-SAMP:CC/PC/D/LT#/C/TR, W3-RM2:RM2-F/R and
  W3-POST2:D, and `HQ_CONDITIONAL_STATUSES.md` for the W3-SAMP relabel.
- Byte-identity of the reader text in STATEMENT §1R and TARGET §6 (diff).
- One inline `nice` Python computation (no files) of C for A = 1…20 from the X.md constant definitions.

## Not checked

- `cpp/v3_engine.h` (eval, cache and `held`; Lemma M (a)–(b) and pins P15–P17, P33). Lemma M's cache argument and
  `v3_fit.R` (P28–P30) were not re-read.
- The numerics scripts and outputs (`work/F_numerics`, `work/numerics`); evidence only, and not run.
- [P1] beyond the passages listed; W3-SAMP's proofs (D-i, PC, LT♯, C, TR) and W3-POST Theorem 1's proof (consumed
  premises, not re-derived); W3-MISR R′'s proof (consumed, PROVED-CHECKED).
- `ASSUMPTION_MAP.md` §3 numeric readings against the raw outputs.
- The commit identity of the code (no git on the code by choice; the pinned lines were read in the working tree).

COUNCIL-VERDICT round=R1 manifest=c7d74e49a9e5a05fb4c9457f6ccf3bb7c83cb85ca00bf49e47d3d8f4a7c8834d seat=opus score=8.6 gates=FAIL
