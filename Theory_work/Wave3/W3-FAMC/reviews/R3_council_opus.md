model: claude-opus-5-5 (claudeAgent_personal, high); round=R3; seat=opus; manifest=68cb694453011ae4ffadfefe921ea5d62f92e8aa25c7a3d8ce281c4b433e498a

# W3-FAMC — council R3, seat `opus`

**Manifest.** `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-FAMC Theory_work/Wave3/W3-FAMC/reviews/MANIFEST_R3.txt`
→ `verify: OK MANIFEST 68cb6944…498a`. I read every frozen file (STATEMENT, lemmas/A_assembly, REPORT, TARGET, PLAN, DEPS,
citecheck.py, deps_hand.py) and the sources named in the brief: [RV] :660-813; [RM2R] :118-182; [RM2] :40-60, :125-225;
[RM] :88-160; [VIS] (all); [L6] :1-120 and :160-263; [L5_formR] :48-130 (D-loc^b, P9); [GROW5] :1-70; [CG] :140-150;
[TB] B8–B11 (:209-302). I also read `reviews/CITECHECK.txt` and `reviews/E2_check_opus_R1.md`. I did not run citecheck.py
or deps_hand.py, because both write files. Instead I recomputed the DEPS spans and sha prefixes in memory, and all 9 rows match `DEPS.tsv`. I used git
read-only to check the v1.3 changelog claim ("§1 unchanged"): `git diff 82fb5122 9862c933 -- STATEMENT.md` touches only
the header, §1R, §2, §4 and the changelog. §1 is byte-identical.

## (a) Per-claim decision

| id | decision |
|---|---|
| W3-FAMC:Cor-FAMC | ACCEPT (mathematics correct as stated; one F finding on the status-evidence binding, F-1, which blocks the statuses gate but not the claim's content) |

## (b) Findings

### F-1 (F; statuses) — the E2 evidence that the AR half's unconditional status rests on is not in the frozen manifest, although STATEMENT says it is
- `STATEMENT.md:185-188`: "Per HQ, the AR half is recorded **unconditionally**. The evidence is the checked-in report
  `reviews/E2_check_opus_R1.md`; it enters the FAMC manifest at the freeze (pending) [R2-N5]." REPORT `:49` repeats that the AR
  half is recorded "on the strength of reviews/E2_check_opus_R1.md (PASS)".
- The freeze has happened (commit 9862c933, "freeze council manifest R3 (68cb6944)"). `MANIFEST_R3.txt` does not
  list the file. manifest.py skips `reviews/` (`SKIP_DIRS`, `tools/manifest.py:50`), and the file is not among the
  `#EXTRA` lines or in `INPUTS_R3.txt` (grep count 0 in both). So the sentence is false for this freeze, and the
  [R2-N5] disposition (v1.2 said "with this check in the FAMC manifest") was accepted but never carried out. As a result, the
  council digest does not bind the evidence for the status of half the corollary: the file could change after R3 without
  `verify` noticing.
- Related wording (E-level on its own): `lemmas/A_assembly.md:116` still says "The status of this half is that of E2
  together with its inputs (`STATEMENT.md` §4); see DP1", which reads as the conditional status that DP1 replaced.
- **Fix (either):** (i) add `#EXTRA Theory_work/Wave3/W3-FAMC/reviews/E2_check_opus_R1.md` and re-freeze (current
  sha256 `6c65796c31897a3a03881946cf19b907690e91d388de236c1d56d3726f85679d`, last commit 2ba7730a); or (ii) reword
  §4 to pin the evidence by commit and sha256 instead of the manifest. Align A_assembly :116 with §4 as well.
- The content is fine. I checked the E2 report's conclusions where FAMC uses them (see the AR notes below), and they hold.

No C or S findings.

### Step-by-step verification (block half)
- **B.0** (`A_assembly.md:24-33`). Σ_UU is block-diagonal on the U_i := U ∩ G_i, and each block is PD by λ_min ≥ c, so Σ_UU⁻¹ is
  block-diagonal. Σ_lU is supported on U ∩ G(l) and Σ_Uk on U ∩ G(k). (a) If G(l) ≠ G(k), the product vanishes and Σ_lk = 0.
  (b) If G(l) = G(k) = G, the Schur complement reduces to U ∩ G. Correct, including the U ∩ G = ∅ convention.
- **B.1.** Interlacing gives (FL-R) on all S, including Q ∪ {l}. (T1-R) follows by its stated sufficient form [RM] :133. Correct.
- **B.2.** (VIS-0) plus B.0(a) kills the cross-group terms. B.0(b) localises to G(j), and k ∈ G ∩ S₀ ∩ U contributes 0 on both
  sides, so (B.2.1) is right. *(BLK-1):* the margin is θ_lo·Var(W_j | W_{U∩G}) ≥ θ_lo·c. *(BLK-s), |G ∩ S₀| ≥ 2:* (VIS-a) applies to the
  group problem. Σ_GG is a PD correlation matrix, and (Σ_GG)⁻¹ = (Σ⁻¹)_GG, so the sign hypothesis is the one (VIS-a)
  needs. The conditioning set U ∩ G ∌ j has size ≤ 15. Constant d_k·sgn θ*_k on all of G ∩ S₀ implies alignment on each
  connected component. The VIS-a bound transfers back through (B.2.1). Margin θ_lo·c. *(BLK-g):* c₁₆(Σ_n) ≥ λ_min ≥ c
  and δ > 0 give margin c·δ through (VIS-b). The B of §1 :59-62 is VIS's B ([VIS] :22-27) verbatim, over n ≥ n₀.
- **B.3.** If Q = Q₀ (p ≥ 2|Q₀| + 32s₀ + 1), then K ≥ 2|Q| + 32s₀ + 1 once ⌊n/2⌋ ≥ q̄ + 32s₀ + 1 (and q̄ ≥ 2gs₀ ≥ 2|Q|). If Q = [p], then p ≤ q̄
  and K = p. This is (L-feas) exactly as [RM2] :134 states it. (L-gain-R): l ∉ Q₀ ⇒ G(l) ∩ S₀ = ∅ ⇒ B.0(a) with l, j ∉ U, so
  ϖ_n = 0. (L-loc-R): G(l) ⊆ H_l, so v ∉ G(l); and G(j) ⊆ Q₀ ⊆ H_l, so G(v) ≠ G(j). Both are B.0(a) at U₀ (v, l, j ∉ U₀), so r_n = 0.
  |H_l| is bounded, so it is ≤ n^{1/120} eventually. Budget: 15/120 + 1/4 = 3/8 < ½. Correct.
- **B.4.** A = T ∩ N_l = T ∩ G(l) (since T ⊆ Q and l ∉ T). Σ_TT = diag(Σ_AA, Σ_{T∖A}) and Σ_{T∖A,l} = 0, so β̄_{T,l} = β̄_{A,l}
  exactly, and Var(W_l | W_A) = Var(W_l | W_T) by B.0(b). This matches [L5_formR] :108-116 (Lemma D-loc^b):
  N_l ⊆ Q ∖ {l}, ν_n = g − 1 = o(log n), L_n = η_n = 0, (N0^b) from B.3, (N1) from B.1. The argument holds for every T ⊆ Q,
  not only T ∈ 𝓛. Then (W-R) follows through `W3-RM2:D-to-W@1.0.3` ([RM2] :256). Correct.

### Step-by-step verification (AR half)
- **A.0.** The class fits [L6] §0 (:35-38) and E2's class (:170-174): unit diagonal; spectrum [(1−|ρ|)/(1+|ρ|), (1+|ρ|)/(1−|ρ|)]
  by [GROW5] (P1), with the D = diag((−1)^i) reduction for ρ < 0; K_dec < ∞ with α = 3 > 2; π = id. ρ = 0 (Σ = I) is
  included.
- **A.1.** E2 lets b ∈ [γ, ½) with γ = 1/(2α) = 1/6 ([L6] :195), so b = ¼ is admissible. E2's example ϱ = (½ − b)/30 =
  1/120 gives 15ϱ + b = ¼ + b/2 = 3/8 ([L6] :231-232). E2's verified list ([L6] :211-246) is exactly RM2-R's hypotheses
  other than (V-R), which E2 assumes as PTV(a₀) ([L6] :219). The list matches.
- **E2 check (evidence).** I re-derived the AR fallback in `E2_check_opus_R1.md:37-58`. The Markov two-neighbour regression
  has three cases. (i) Both neighbours lie within r, and then β_A = β_T exactly. (ii) One neighbour is beyond r: the gap is
  c_a + (ρ^{d₂} − c_b) ≤ ρ^{d₁} + ρ^{2d₁}, where ρ^{d₂} − c_b = ρ^{d₂+2d₁}(1 − ρ^{2d₂})/(1 − ρ^{2(d₁+d₂)}) ≤ ρ^{2d₁}. (iii) Both are beyond r: the gap is ≤ 2ρ^{r+1}.
  Leakage follows from (P4) at every U. Its conclusion that every FAMC-consumed E2 item holds at α = 3, b = ¼ is correct
  (I did not re-derive BC and IR themselves; for AR the fallback route does not need them).
- **A.2.** *(AR-s), ρ ≠ 0:* the (VIS-e) instance d_l = s^l gives DΣ⁻¹D off-diagonals −|ρ|/(1−ρ²) ≤ 0. The path graph is connected
  for p ≥ 2, and alignment s^k·sgn θ*_k = const is (AR-s) as written in §1 :69-70. *ρ = 0:* the graph has no edges, so
  the condition is vacuous. *(AR-sep):* the population inequality of [GROW5] (G3b) (:58-59) uses only (P3), (P4), (P5)'s
  population identity and separation. It holds for every U ∌ j, so it does not depend on C5a's exact-Gram/p ≤ n − 1 setting.
  The sign reduction θ* → Dθ* preserves |Cov| and the separation sum. ρ ≠ 0 is required, as in C5a. *(AR-g):*
  c̲ ≥ (1−|ρ|)/(1+|ρ|). Correct.
- I also checked the counterexample in §1b(i): for θ = (1, −2) on adjacent truths at ρ = ½ and U to the left (or U = ∅), the covariance
  is Var(W_j | W_a)(1 − 2ρ) = 0. Correct (it is a remark, outside the claim).

### Conclusion vs. masters
§1 :76-80 is exactly the reader conclusion (RV :689-697): the common data event from RM0-plus (b⁺) with [MODE] etc. supplied
by RM2-R-plus ([RM2R] :126-134, :177-181); "in particular" from P(𝒢⁺ᶜ) bound; delivery and P(Ŝ = S₀) → 1 from (c⁺)/DLV-0
under (D) = (S4) (B6.6′), with the qualifications quoted by reference to RV :696-697. Nothing more is claimed. The masters'
setting (Setting R, implementation premises, configuration) is §0 via (S1)–(S3). No hypothesis is used without being stated:
the BLK proof uses only block-diagonality, λ_min ≥ c, the coefficient conditions and (A2); the AR proof uses only ρ fixed,
(A2), and the coefficient conditions.

### E findings (editorial; never block)
- **E-1** `lemmas/A_assembly.md:98`: "bounds hold in this case with K_15 replaced by 1". (P4) gives |ρ|^d, and |ρ|^d ≤ (1+d)^{-3}
  holds only for d ≥ d₀(ρ) (false at d = 1 for ρ = 0.95). It is true for the asymptotic bounds, since R_Q, r₀ → ∞, but only for
  n ≥ n₀. Write "with K_dec in place of K_15" (as the E2 check does) or "for n ≥ n₀". This is a cross-check only and is not load-bearing.
- **E-2** `lemmas/A_assembly.md:3`: "This file proves `STATEMENT.md` §1 (v1.2)". STATEMENT is v1.3. §1 is identical (verified),
  so this is a stale pointer only.
- **E-3** REPORT `:47` depends_on lists `W3-AUDIT-V:VIS@proof:VIS-0,VIS-a,VIS-b,VIS-e`. The registered span cites (VIS-c),
  (VIS-d)(i), (VIS-d)(ii) for its nullity sentences (STATEMENT :63-64, :73-74). Add VIS-c and VIS-d to the part list, or move
  those two sentences to §1b. The edge to VIS itself is present.
- **E-4** REPORT `:44` `status_source: lemmas/A_assembly.md:1`. That line is the file title and carries no status line (the
  convention elsewhere, e.g. W3-DIST REPORT, points to a line that states the status). Add a `Status:` line or re-point it.
- **E-5** REPORT `:46` conclusion: the delivery clause omits "with the same qualifications as Theorem 6" (STATEMENT :79-80).
  The `statement:` pointer covers it, but the conclusion field should carry the qualifier too.
- **E-6** STATEMENT changelog `:201-206`: rows are out of order (v1.0, v1.3, v1.2, v1.1), and the v1.2 row's "§1R corrected (it
  overclaimed)" has no parity word (it is WEAKER for §1R).
- **E-7** PLAN `:39-44`: the header says DP1–DP3 are resolved, but DP1 still shows the options with recommendation (a). The actual
  resolution (unconditional, HQ) is not recorded there.
- **E-8** STATEMENT §4 `:175-176`: POST-R's verbatim status names "input versions W2-APP:POST@1.0.1", while the D126 expansion
  quotes @1.0.7. This is consistent with the RV row's own practice (RV :730, :735), but one clause saying "current version" would
  help readers.

### Stronger results provable (not findings)
- (BLK-s) needs alignment only on each connected component of the graph of (Σ_GG)⁻¹ (VIS-a's actual premise), not on the whole group.
- Group sizes could grow slowly (g_n = o(log n), with |Q ∪ G(l)| ≤ n^ϱ). B.0 gives exact zeros independently of g.
- AR: exponential decay allows a logarithmic Q (as in C-GROW (a)), so any b > 0 would do. Banded/MA(q) and Toeplitz decay
  with α > 2 also go through E2 + (VIS-b)/(VIS-d)(ii).

## (c) Interpretive sentences in the registered span (STATEMENT :48-80)

| line | sentence | verdict |
|---|---|---|
| :57-58 | "(for example, equicorrelated groups with correlation in [0, 1) and equal signs inside each group)" | checked: the inverse of an equicorrelation matrix with ρ_b ≥ 0 has off-diagonals −ρ_b/((1−ρ_b)(1+(m−1)ρ_b)) ≤ 0, d = 1; λ_min ≥ c is already in (BLK) |
| :62 | "then B := ∪ ν^⊥, a closed union of hyperplanes through 0" | checked ([VIS] :37-38, 𝒩 compact) |
| :63-64 | "If the labelled local matrices take finitely many values … B is a countable union of hyperplanes, so it is Lebesgue-null and nowhere dense ((VIS-c), (VIS-d)(i)); in general it may have interior" | checked ([VIS] :41-51, :70-72; c_m ≥ c from λ_min). Consider moving it to §1b; see E-3 |
| :66-67 | "This is 'moderate' in the sense of correlation bounded away from ±1; no uniformity in ρ is claimed." | checked (commentary; harmless in the span, could move to §1b) |
| :70 | "There is no condition when ρ = 0." | checked (Σ = I; A.2 ρ = 0 bullet) |
| :73-74 | "For AR, B is a countable union of hyperplanes, so it is null and nowhere dense ((VIS-c), (VIS-d)(ii))." | checked ([VIS] :52-53 lists AR(ρ), r(d) → 0). See E-3 |
| :76 | "Then the conclusion of Theorem 6 holds." | checked (A.1 B.5, A.2 A.3 → RM2-R-plus) |
| :78 | "In particular, P(output and Ŝ ≠ S₀) → 0." | checked ([RM2R] :129, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝒢⁺ᶜ)) |
| :78-80 | "If moreover … (S4) hold, then P(output) = 1 for every admissible n ≥ 3 and P(Ŝ = S₀) → 1, with the same qualifications as Theorem 6" | checked ([RM2R] :135-142, DLV-0; RV :691-697 via B6.6′) |

None must move out, and none is false.

## (d) Gates

- **correct — PASS.** Every step of B.0–B.4 and A.0–A.2 checks against the cited sources. No C findings.
- **strength — PASS.** §1 claims exactly Theorem 6's conclusion. §1b and §5 are kept out of the claim, and §5's exclusions are accurate.
- **faithful — PASS.** The citations, quotes and parameter lists (E2, VIS, GROW5, RM2/RM, RV) match their sources. Citecheck shows 93/0.
- **statuses — FAIL.** F-1: the evidence for the AR half's unconditional recording is not bound by the frozen manifest, contrary to
  STATEMENT :186-187. The verbatim statuses and the D126 expansion are otherwise correct.
- **sweep — PASS.** REPORT claims nothing beyond STATEMENT. The registry block's spans (48-80, 25-32) are right. DEPS rows and
  shas match. TARGET parity tags (conclusion EQUAL to row 3.1, hypotheses a special case) are right. The changelog's v1.3 "§1
  unchanged" is verified. There are editorial items E-2 to E-7.
- **reader — PASS.** §1R adds nothing beyond §1 and omits no hypothesis: the families, the four coefficient routes (with the AR
  ρ < 0 parity and ρ = 0 cases, and the joint flip-and-sign condition for groups), (A2), (S4) and the qualifications.
  "Partial correlations ≥ 0" is equivalent to the M-matrix condition for Gaussian groups (MTP2).

## (e) Score

Score 9.0: the mathematics is sound and faithful, and one minor F finding (a provenance binding with a one-line fix) costs 1.0.

COUNCIL-VERDICT round=R3 manifest=68cb694453011ae4ffadfefe921ea5d62f92e8aa25c7a3d8ce281c4b433e498a seat=opus score=9.0 gates=FAIL
