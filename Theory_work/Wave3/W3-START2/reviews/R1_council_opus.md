# W3-START2 — council round R1, seat `opus` (Claude Opus 5.5, effort high; blind first read)

Frozen content: `reviews/MANIFEST_R1.txt`, digest 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f
(`manifest.py verify`: OK). Files read: everything the brief allows that the delta uses (STATEMENT v1.4.1, P1–P4,
REPORT, PLAN, BRIEF, citecheck.py, numerics/, BASE STATEMENT v1.3.4, BASE L1–L10 in full, W3-SAMP STATEMENT at the
quoted lines, claims.tsv for statuses). Not read: any other `reviews/` file, LOG, CHECKPOINT files, git history.

## Verdict summary

I tried to break every new step and found no error that blocks acceptance. Lemma LEAK-0 is correct as stated. The
split of the nulls into 𝒩_exc/𝒩_prop is a function of X. The bound |𝒩_exc| ≤ max(0, 16 − s₀) holds because all
exceptional nulls sit in the one block that holds j ∈ S₀. The cut-off H satisfies H ≤ z_n exactly when
λ ≤ 15e_κ·2²¹p log n, so the base step bound L3.3 applies to every null. The small-gain premise of L3.3 holds for
proper columns (by J ≤ p𝔏^♯ ≤ p√n) and trivially for exceptional ones (δ = 0). The union bound gives 450e_κ/λ, Markov
adds e_κ/λ, and 1/p ≤ 4𝔏^♯ gives the factor 5. The constants c₀, C and n₀ of BASE L5.2 can be kept: 451ε/2¹⁷ ≤ ε/4, and
log n ≥ 2/ε puts λ = 2¹⁷e_κ/ε in range. F2⁺ really uses p/√log n → ∞ nowhere else. The identity and product bound of
Lemma P2.1 are right. Under (V-m) for the same Q, OVL⁺ follows, because (T1⁺)(a) controls 1/π₀(𝓛(Q)) and step (iii)
of L10.2 uses only the toolkit. The counting lemma, the deterministic witness and every formula of Example P3.3 check
out. I read BASE L9 in full: |Q| is used only at `:161` and `:170`, i.e. in L9.7, which P4 replaces. The case split at
each fixed n in P4.2/P4.3 is valid for an arbitrary oscillating Q_n, and its threshold n_R does not depend on Q. Each
supersession row is a genuine implication. All remaining remarks are about presentation or citation and are
non-blocking.

## Gate table

| gate | result | what I re-derived |
|---|---|---|
| G1 correctness | PASS | P1.1(a)–(c) from (J0) (τ_U ≥ σ, h_l ≥ 1, ∅ ∈ 𝒰); P1.2(a) (block containing j unique; S₀ ⊔ 𝒩_exc ⊆ C), (b), (c) (μ ∈ span X_{S₀}); P1.3 Steps 0–5 line by line: T₁ ≤ ((s₀+1)/p)Σρ_l since 2p−1−s₀ ≥ p; e^{H²/2} = λ/(15e_κ), e^{z_n²/2} = 2²¹p log n ⇒ H ≤ z_n; P(|Z| > H) ≤ 2e^{−H²/2} for H ≥ 0, ×15 ⇒ 450e_κ/λ; Step 2 small gains via BASE L3:61-62 (needs p ≤ n^A only); Step 3 L3.3 hypotheses (T = U_l ⊆ C_b ∖ {l}, \|Z\| ≤ z_n on 𝓩_h ∩ 𝓗); exceptional ρ_l ≤ (λ/15)(n+1)^{−1/2}; (1.1); E V ≤ 𝔏^♯ (exceptional summands ≥ 0); Markov; 5 = 1 + 4; 451 = 450 + 1; event form (1.2); Consequence with λ = 902e_κ/ε. P1.4: λ = 4c_L/ε = 2¹⁷e_κ/ε; range from log n ≥ 2/ε; n^{−1/2}𝔏^♯ ≤ c₀/(s₀+1); probability budget ε/2 + b_n + ε/4 + ε/4; base on-𝒢 steps (L5:60-64) use 𝓔^blk, 𝓧, 𝓩_h, 𝓜 only (checked against L4.1/L4.2: Ξ needs 𝓔^blk ∩ 𝓧 and c_QU_Q ≤ 1, not 𝓜₀); C^♯ ≥ C′; the L6.0′ variant (451/(2¹⁵ log n) ≤ 1/log n; λ_n in range). P1.5(b) rate → 0. P1.6 (J1) with t² − σ² = Δ_U ≥ φ₀²θ_lo² ⇒ 𝔏^♯_n ≤ C_Fn^{η′/2}; no p → ∞ in L2–L5. P1.7/P1.8 as base L8.2/L10.1. P2.1(a), (b) via (P3) with D = 0 (s₀ + a ≤ \|Q\| ≤ K ≤ p) and (CH); (s₀+1)_a ≤ \|Q\|^a; sum over N = product. P2.2: 𝓨 bound q̄2¹⁶/log n; step (iii) of L10.2 uses no visibility, e_n or U_Q. P3.1 count (17 > 16); witness choice; Example P3.3: B² = diag(r1_s1_sᵀ, s1_r1_rᵀ) ⇒ eigenvalues ±√(sr), sr ≤ 72; XᵀX = (n−1)G_n, centred, unit sample variance; Λ_V, ‖(I−P_V)x_l‖² = (n−1)(1−vρ²), x_lᵀ(I−P_V)μ = (n−1)θ(s−v)ρ, δ² ≥ cτ²_V log n. P4.1 table against L9:22-152 (read in full); P4.2 (4.3), n_R, case (ii) inequality C_nϱ̄ + n^{−1} ≤ a_n via a_n ≥ n^{−1/2}; P4.3 T_ε and both cases. |
| G2 hypotheses used = stated | PASS | For each of the nine claims the proof uses exactly the stated hypotheses. LEAK-0 uses p ≤ n^A, ‖μ‖² ≤ Mn, (GF-16), s₀ ≥ 1, s₀ < K, n ≥ n₂ and n^{−1/2}𝔏^♯ ≤ 1. OVL⁺ uses visibility and (AL) only for π₀(𝓛(Q)) → 1. (N2⁺) uses only (E), (GF-16) and the premise. (T3⁺)(b) uses \|H_l\| ≤ (log n)^{κ_Q} only through N_ref, and \|Q\| ≤ K only for admissibility. Remark 5 below is a wording point. |
| G3 no hidden assumptions | PASS | No independence is used between the Z_l (a union bound and a Markov bound on a sum), between columns, or in 𝓨. s₀ = 0 is explicitly excluded from LEAK-0, F2⁺ and (N2⁺); where s₀ = 0 is covered ((T1⁺)(b),(d), TRANSFER) the proof falls back to the unchanged base result. p → ∞ is not used: F2⁺ allows bounded p, and I checked L2–L6 for hidden uses. The only bound on Q is \|Q\| ≤ K; no rate is assumed to tend to zero in (T3⁺)(b) (the case split). Every conditioning is on 𝒲 = σ(W_D) (base) or on nothing. Witnesses, splits, I_n and levels depend on X alone. |
| G4 imports and supersession | PASS | Every cited base line says what is taken from it, hypotheses included; citecheck reports 216 citations with 0 missing or out of range. No other ticket is used as a premise. W3-START rows are absent from claims.tsv, so "not yet rows of the registry on main" is accurate. The statuses of W3-SAMP:C@1.1.1 and D@2.1.1 ("PROVED-CHECKED") match the registry. P-START (SAMP:76) and P-OVL in the production form (SAMP (D-iv), :103-105) are quoted correctly and receive what (T5⁺) says. All eight supersession rows are implications: 𝔏^♯ ≤ 𝔏⁰; F2⁺ ⊇ F2; a weaker premise in TRANSFER; the new r_n ≤ the old one; (V-c) ⊆ admitted visibility; (N2) is vacuous for s₀ ≤ 15 and identical for s₀ ≥ 16; (L-R) ⇒ (L-R⁺). Remarks 3 and 6 are non-blocking. |
| G5 constants and rates | PASS | 5, 451, H, the λ range, C^♯, the reuse of c₀/C/n₀, C^♯_n of L6.0′, C_F, C_B = 2d̄√(2A+1)/a̲ + 1, C_R = C_B + 1, n_R and T_ε = max(D_ε/c₀, CD_ε + 1) are all traced. Uniformity holds in all three places. In (T1⁺)(d) and LEAK-0 everything depends on (ε, κ, A, M, σ², g_*, s₀, visibility constants) through e_κ = e^{2κ_E+1}, n₂(A) and n₀. In (T3⁺)(b), (4.1)/(4.2) and n_R are free of Q, and \|Q\| + 1 sits inside ϱ_n. The ε-dependence of C in (T1⁺)(d) is disclosed in §4. |
| G6 fidelity to the code | PASS | No new code property is used. The delta needs: the partition is a function of X with blocks ≤ 16; the formula γ₀ = w(\|S\|)∏r_b; T₁'s closed form (BASE STATEMENT:89); and the existence of table entries (\|C_b\| ≤ K). All are base §1 pins and premises. citecheck resolves every `path:line`. |

## Per-claim table (REPORT.md §3)

| id | decision |
|---|---|
| LEAK-0 | accepted with non-blocking remarks (5) |
| START-F (T1⁺) | accepted with non-blocking remarks (2) |
| F2 (F2⁺) | accepted |
| TRANSFER (T3⁺)(a) | accepted |
| IF-START (IF-START⁺) | accepted |
| OVL (OVL⁺) | accepted |
| NEC (T4⁺) | accepted with non-blocking remarks (4) |
| BR (B-R⁺) | accepted |
| START-R (T3⁺)(b) | accepted |

## Issues (all NON-BLOCKING; none must be fixed before acceptance)

1. **NON-BLOCKING, typo.** `lemmas/P1_LEADING.md:16-17`: "(BASE / BASE `lemmas/L3_LEAK.md:12-14`" repeats "BASE".
   Repair: delete one.
2. **NON-BLOCKING, wording.** `STATEMENT.md:108` says clause (c) of (T1⁺) is that of v1.3.4 "word for word". The base
   clause (BASE `STATEMENT.md:251-253`) also carries the gloss "the start odds against the truth are, to first order,
   the prior-weighted sum of the single-null block Bayes factors", which is not reproduced. The mathematics is
   identical. Repair: say "the same statement", or restore the gloss.
3. **NON-BLOCKING, citation outside the frozen content.** `STATEMENT.md:205-206` cites BASE `CHECKPOINT_3.md:241` for
   the base status. That file is not an input of this round (citecheck confirms only that the line exists), so the
   council can check the quoted status only against `BRIEF.md:3-4`, which agrees. The file already makes acceptance
   conditional on the base ticket's acceptance, so nothing is overclaimed. Repair (optional): cite the base status
   through an input that is listed, or mark the CHECKPOINT reference as "for HQ".
4. **NON-BLOCKING, informal summary.** `REPORT.md:27-28` (P3 bullet) says the nulls "gain more than
   (1 + 2Ā)·τ²_V·log n". The claim needs δ²_{V,l} ≥ c·τ²_V·log n with a **fixed** c > 1 + 2Ā (`STATEMENT.md:157-158`).
   A gain of (1 + 2Ā + o(1))τ²_V log n is "more than" that threshold but is not covered. Repair: "at least
   c·τ²_V·log n for a fixed c > 1 + 2Ā".
5. **NON-BLOCKING, fixed-n hypotheses of LEAK-0.** `STATEMENT.md:82` and `lemmas/P1_LEADING.md:38` list "(E)", which
   contains asymptotic clauses (p > s₀ for all large n), in a lemma stated at a fixed n with a uniformity claim. The
   proof uses only the inequalities at n: p ≤ n^A, ‖μ‖² ≤ Mn (through κ_E) and s₀ < K. Repair: write "the inequalities
   of (E) at n", as (T1⁺)(d) does.
6. **NON-BLOCKING, dependency list.** `STATEMENT.md:206-208` and `REPORT.md:73-74` consume seven base claims "by
   statement" plus "the proof files L1–L10". The proofs also reuse proof steps of base START-F (L5.2, L6.0/L6.0′),
   TRANSFER (L8.2), BR (L9.1–L9.6), OVL and IF-START (L10.1–L10.2), and Lemma J/(B1) (L3.1–L3.2). These are covered by
   "the proof files", but the registry `depends_on` would be more exact if it named them, e.g.
   W3-START:START-F@proof:L5.2.
7. **NON-BLOCKING, sharpness row.** `REPORT.md:89`: "leading rate n^{−1/2}𝔏^♯_n(h) sharp in order when 𝔏^♯_n(h) = O(1)"
   is right for the leading term (T0 gives o₀ ≥ ½(n+1)^{−1/2}). For o₀ itself to be of exact order n^{−1/2}, the
   remainder conditions of F2⁺(v) are also needed (κ_V > ½ and n^{−1}𝔏_n(S₀; h)² = O(n^{−1/2})). Repair: add "with the
   remainder conditions of F2⁺(v)" or point to P1.6(v).

## Overall score: 9.1 / 10

The package is acceptable as checked mathematics as it stands. Every new step is correct, the honesty-of-scope items
are adequate, and the remarks above are editorial.
The honesty-of-scope items, all present and accurate: s₀ = 0 is excluded in LEAK-0 and (N2⁺); the ε-dependent C of
(T1⁺)(d) is disclosed with its reason; "fewer than 17 − s₀ nulls: not claimed" (justified by the 16-column block that
holds S₀); the trivial range of (T3⁺)(b) is stated; the C_L = 0 clause is tightness only.

## Checks performed

* `manifest.py verify` on MANIFEST_R1: OK (digest above).
* `citecheck.py` run with its output in the scratchpad (outside the repo): 216 citations, 148 with line ranges,
  0 missing or out of range. I also opened every base line range cited in P1–P4 and compared it with what is taken
  from it.
* P1–P4 re-derived line by line, as listed under G1. BASE L9 read in full to confirm that |Q| is not used in
  L9.1–L9.6; BASE L1–L8 and L10 read at the cited steps and their hypotheses.
* Case checks: an oscillating Q_n in P4.2/P4.3, bounded p in F2⁺/LEAK-0, p = s₀ + 1 with the null in the truth block
  (T₁ = O_P(n^{−1/2}), consistent with LEAK-0), and the edge cases s₀ = 0 and s₀ ≥ 16.
* `numerics/out_P.txt` and `falsify_P.R` read; the REPORT §6 numerics paragraph matches them (checks A–D, 0
  violations; for s₀ ∈ {8, 9, 15} at n = 5000 the example is reported as skipped because G_n is not yet positive
  definite).
* Registry statuses of W3-SAMP:C/D and the absence of W3-START rows checked in claims.tsv; SAMP interface lines checked.

## Not checked

* I did not re-run `falsify_P.R`; I relied on the frozen output.
* The base proofs were not re-verified beyond the cited steps (they are out of scope per the brief).
* BASE `lemmas/L11_EXAMPLES.md` was not read (the delta does not cite it).
* The pinned code files and `lem_common.R` were not re-audited: the delta adds no code property, and G6 rests on the
  base §1 pins.
* BASE `CHECKPOINT_3.md` was not read (forbidden for this blind read; see Issue 3).

COUNCIL-VERDICT round=R1 manifest=29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f seat=opus score=9.1 gates=PASS
