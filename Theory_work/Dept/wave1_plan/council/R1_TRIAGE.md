# Plan Council R1: Finding Triage Table (Lead-A → Manager), 2026-11-28

Item: `Theory_work/Dept/wave1_plan/` @ 7197d142. Bars (Handbook v2.0 rule 9): STATEMENTS ≥ 8.5, PLAN ≥ 8.0.
Status: FINAL for Manager ruling. (The Sol seat's first run failed on an infrastructure error, Codex app-server retired, and was relaunched on the same thread.)

## Scores
| Seat | Model | STATEMENTS | PLAN | Blocking |
|---|---|---|---|---|
| OPUS | Opus 5.5 high | 8.1 | 7.9 | 2 |
| NEON | Gemini 4 Neon high | 7.8 | 7.3 | 5 |
| SOL | Sol 6.2 high | 7.9 | 7.6 | 8 |

## Findings and Lead-A recommendations
Rec = ADOPT / DECLINE (with reason). "=" marks a duplicate of the finding named.

| ID | Seat | Sev | Summary | Rec | Rationale |
|---|---|---|---|---|---|
| OPUS-1 = NEON-1 = SOL-4 | O, N, S | BLOCK | Thm S note 5: n_ε cannot depend "only on ε and constants", because n_c of A4–A5 is a property of the law sequence; "T03♯ gives this per n" is wrong (W3P uses the diagonal transfer). Thm D must also say n₀(M) inherits n_c at c = C_qM+1 and √n/log n ≥ M | ADOPT | Both seats have a valid counterexample. Fix: K_ε depends on (ε, constants); n_ε also depends on n_{C_q+1} and on C_β (through (C10)). Delete "per n". Thm D: spell out the dependence of n₀(M). Sol's form is adopted: n_ε = max(n_{C_q+1}, the constants-only threshold); a per-n remark (uniform over laws satisfying the window at that n) only if Lead-S proves S-4alt. |
| OPUS-2 ⊂ NEON-6(1) | O, N | BLOCK | L-RAND interface omits ε ⫫ (X, θ*) and \|supp θ*\| = s₀ on 𝒜_n; "uniform O_P" is not justified | ADOPT | Copy the hypotheses verbatim from W3P l.95–98; drop "uniform". |
| NEON-6(2–5) ∪ SOL-6 ∪ SOL-7 | N, S | BLOCK | L-DES: q′ = min(q, p), A2, n ≥ 3, 1 ≤ \|T\| ≤ q, plus threshold n_B (= OPUS-14). L-SCORE: scales (standardised vs response), explicit NIG parameters, Q_S^c = s_y²Q_S. L-FLOOR: σ_*² dropped and regime hypotheses missing. L-HELL: the in-sample identity (H-id) is missing | ADOPT | All are omissions in a contract the plan calls frozen. The fixes are mechanical: copy each statement from its source. Per SOL-6, L-FLOOR, L-T03♯ and L-RAND are stated on the unit-noise problem, θ* = D_xβ*/σ_*. Per SOL-7, L-SCORE freezes Q_S, the NIG mean nH_S⁻¹X_SᵀY_c, covariance nvH_S⁻¹ and IG(a₀+n/2, b₀s_y² + Q_S^c/2). |
| NEON-2 ∪ SOL-3 | N, S | BLOCK | A9′'s nonsingular Var(x_𝒞) makes the "equivalent to the structural form / holds whenever jointly Gaussian" remark false for a singular Gaussian x_𝒞. Cor M1(ii) conflates S(a)/(b) and omits C_sel(s_𝒞, A) (= OPUS-12) | ADOPT (option b) | Keep nonsingularity in A9′ for Thm M (M-2 uses uniqueness of β^𝒞). Qualify the remark with "with Var(x_𝒞) nonsingular". Split Cor M1(ii) into (a)/(b) with C_β > C_sel(s_𝒞, A). Content unchanged; the remark becomes true. Sol's counterexample (C_β < √2 ⇒ the true model's posterior → 0) shows the candidate threshold must be explicit. |
| NEON-7 | N | BLOCK | M-2 display drops 2b₀: −ν log(Q_S/Q_𝒞) is not literally an upper bound | ADOPT, as NON-BLOCKING | Correct as a literal inequality. But Q_𝒞/n → σ²_𝒞 > 0 a.s., so the difference is ν·O(1/n) = O(1) and is already absorbed by the display's O(1). The route is unaffected. Fix: keep 2b₀ in the display and note the O(1). |
| NEON-8 | N | BLOCK | Lean plan: (1) (F4) Gaussian quadratic-form MGF det(I−A)^{−1/2} is missing (= OPUS-16(i)); exact citations are missing for G1, P2 (lem:chi(b)) and P4. (2) Build order: L-HELL and L-DES live in module 6 but are consumed by modules 4–5. (3) L-SCORE tier mismatch. (4) P5 is not the inequality T.md uses (= OPUS-15) | ADOPT | All correct. Add (F4) to G1. Give exact citations. Create shared modules `BVSCert.Design` and `BVSCert.Hellinger` before module 4. Split L-SCORE into tier 1 (algebra) and tier 2 (NIG via G1). Make T.md's in-house Prop R the default instead of P5 (Hoeffding is in Mathlib; Cantelli and Sauer–Shelah are elementary). |
| SOL-1 = OPUS-3 | S, O | BLOCK (Sol) / NB (Opus) | A7′ plain English "no method can recover below this order" is false (p = 2 counterexample) | ADOPT | Reword: a sufficient threshold for this posterior; the minimax order is √(log p/n); the extra ½log n is the cost of g = n. Plain-English only; no math change. |
| SOL-2 = OPUS-8 | S, O | BLOCK (Sol) / NB (Opus) | Prop LB / sharpness sentence needs 1 ≤ s₀ < p, s₀+1 ≤ K (p = s₀ = 2 counterexample) | ADOPT | Add the hypotheses; describe the established upper/lower gap as at most √log n. |
| SOL-5 | S | BLOCK | L-DES must require A4 on the q-window **at that n** (i.i.d. design, clipped q); the frozen interface ends at a Gram bound, but DIST-1 needs (ND; c_D, m_n(t)) | ADOPT | Correct and not raised by the other seats. Add the B2 consequence: interlacing on clipped unions gives c_D = g₀/(1+g₀), hence (ND); record (E), (C) and the domain event on the same event. |
| SOL-8 | S | BLOCK | L-SIZE freezes O_P(e^{−ω}) without hypotheses; Lemma 1a / 1a′ and Lemma S have different hypotheses and outputs | ADOPT | Split L-SIZE into E1/E2, 1a/1a′ and S sub-interfaces, with hypotheses from S.md:31–41, the t/ω domains and the consumers named. |
| SOL-9 | S | NB | Scope wording: A8(a) needs nonsingular candidate covariance and σ²_𝒞 > 0; "always keeps" = a.s. limit; Cor S1 "fixed size" = fixed standardised lower bound; HPM = MPM w.p. → 1; p_ret < 2 is the proof domain (the engine does retain a single column), counted in the failure event | ADOPT | Update the summaries, the A8 rationale and T-10. |
| SOL-10 | S | NB | A5 plain English = residual-variance floor of order 1/n; A6 permits σ_* → 0; explain the role of full rank in A9′; "used in this proof"; allow τ² = 0; conditional reading of independently chosen 𝒞 | ADOPT | Consistent with NEON-2 option (b) and OPUS-9. |
| SOL-11 | S | NB | Thm M bookkeeping: L-FIX under A8(a); the log-det remainder; variance orders; s_y² in the M-4 odds display; T-2 is D-specific; plug-in intercept convergence in M(i) | ADOPT | All in M-1/M-3/M-4 text. |
| SOL-12 = OPUS-7 | S, O | NB | Cite H.md (checked); add the DIST statement-carrier fidelity comparison to D-1/D-4 | ADOPT | |
| SOL-13 ∪ NEON-8 ∪ OPUS-17 | S, N, O | NB | Lean: shared modules before consumers; Gamma real-shape tails; fixed-b marginal identity by integration; P1 pairwise-orthogonal ranges; **top-level theorem with [LS] hypotheses and a discharge check of every interface (an axiom allowlist alone cannot catch extra hypotheses)** | ADOPT | Acceptance item 6: a top-level theorem per published claim, with [LS] hypotheses verbatim. |
| SOL-14 = OPUS-5 ∪ OPUS-19 | S, O | NB | T-14 (s, A); T-20's two numbers are different regimes; add LB, score-units and score-only-extension checks; make T-24 conditional on the route | ADOPT | Merged into T-25 … T-33. |
| OPUS-4 | O | NB | Cor S1 non-nesting note gives the wrong reason (C_q is narrower than 5(A+1)(s₀+1) except at s₀ = A = 1) | ADOPT | Verified numerically by Opus. The real reason: A4–A5 are assumed on every fixed c. Add the supplement remark (per-n single window: the old hypotheses imply the new ones except at s₀ = A = 1). |
| OPUS-5 | O | NB | C_sel dependence stated three ways; T-14 says (s, A, φ) (= NEON-10(1)) | ADOPT | (s, A) everywhere; note 1 "s = 5". |
| OPUS-6 (+ Sol's S-4 note) | O, S | NB | S-4: the two spines run together; Opus says the per-n spine covers only (b); Sol prefers per-n and sketches (a) from T03♯ (C2), (C5), (C8), (C10) per-n tail bounds + Markov | ADOPT (split) | Main route = L-RAND for (a) and (b), which has a checked source. S-4alt = per-n spine: (b) via C_expectation; (a) needs a new KEY step S-4a (Sol's sketch), with its own cross-family check. Lead-S chooses; the statement is written in sequence form, valid under either route. |
| NEON-11(1) | N | NB | Choose the per-n spine (cleaner; drops A-2); write Π_repl in :91 | PARTIAL: DECLINE the spine choice, ADOPT Π_repl | The per-n spine does not cover (a) without new work (OPUS-6). L-RAND has a checked source for both. |
| OPUS-7 = NEON-9(1) | O, N | NB | L-HELL cites Lemma H as "not line-checked", but it is PROVED-CHECKED (Sol L3_sol_B, sha 1ca0d39c…); Prop LB is also cited with a stale "unchecked" | ADOPT | Our own §5 item 6 rule. Cite claims.tsv:491 / :346 with the checked sha. |
| NEON-9(2) | N | NB | Lead-D risks text still says to fix the headers, which contradicts §5 item 6 | ADOPT | Point to the per-ticket STATUS.md. |
| OPUS-9 | O | NB | A9′ allows a data-split 𝒞; Cor M1 doesn't, and the conditional result needs uniform constants | ADOPT | Move the data-split case to a remark (conditional on 𝒞, with uniform constants). |
| OPUS-10 | O | NB | Quantifier order inside A4–A6 (∃c_ψ ∀c ∃n_c ∀n ∀T) | ADOPT | Statements bar 8.5; cheap. |
| OPUS-11 = NEON-10(2) | O, N | NB | T-23: c = C_qM + 1 | ADOPT | Ceiling. |
| OPUS-12 | O | NB | Cor M1(ii) S(a) vs S(b) | ADOPT | Merged with NEON-2. |
| OPUS-13 ∪ NEON-5 ∪ NEON-3 | O, N | NB | Header v0.1/v0.3 and bar 8.0→8.5; φ(y; ·, σ) should use σ²; define the pseudo-true objects in [LS] (not "draft l.263–281"); "positive finite variance", "nonempty T", S₀∪J ≠ ∅; C₀ → C_sel; T-21 wording; a₀ = b₀ = 0.01 fixed (the sources hard-code 0.01) | ADOPT | Fix a₀ = b₀ = 0.01 (engine v3.1.1) in §0 and Thm D; do not generalise. |
| NEON-4 | N | NB | Thm S(a) "no condition on the other effects" ignores A6 | ADOPT | "no lower bound on the other effects (A6 still applies)". |
| OPUS-14 | O | NB | L-DES threshold n_B, q = q_n(M) | ADOPT | Merged with NEON-6(2). |
| OPUS-15 | O | NB | P5 mismatch | ADOPT | Merged with NEON-8(4). |
| OPUS-16 | O | NB | G1 + (F4); P4 consumers add Thm M; P6 one-sided; L-RAND tier | ADOPT | Merged with NEON-8. |
| OPUS-17 ∪ NEON-11(3) | O, N | NB | Lean acceptance: axiom ↔ citation fidelity review plus a non-vacuity smoke test; the MATCH rule from Lean/BRIEF; Phase-0 check of strong_law_ae | ADOPT | Acceptance item 5. |
| OPUS-18 | O | NB | Lead-M risk is low–medium, 3–4 days (new proof, four care points) | ADOPT | Fair. |
| OPUS-19 ∪ NEON-10(3) | O, N | NB | Missing checklist hazards: label crosswalk paper↔DIST; n_ε/n₀ dependence on n_c; Prop LB hypotheses; one null set in Thm M; Cor M1 units (σ_𝒞); data-free b₋; scale conventions and IG rate b₀s_y²; √n/log n ≥ M; Cor M1 s_𝒞; M-4 raw Z_S + ridge O(1) | ADOPT | Add T-25 … T-33. |
| NEON-11(2) | N | NB | D-4 cites Lemmas S and V, but X.md is self-contained (it proves the V(a)/S instances it uses) | ADOPT | Verified: X.md l.12–13. Cite X as self-contained. |
| NEON-11(4) | N | — | Effort ratings and spot-checks fine | — | No action. |

## Open items ([LS] §5): seat verdicts (unanimous)
1. Anchored A7′(a): OPUS, NEON, SOL keep. → Keep anchored, with a plain sentence and the all-subsets sufficient form.
2. Cor S1 non-nesting: all three say acceptable, with the reason corrected (OPUS-4; Sol: C_q is 54.8 vs 60 at s = 5, A = 1). → Accept, with the note corrected.
3. C_sel: all three say "constant C_sel(s, A), not sharp" in the main text, with 4√c₀ and the numbers in the supplement (Sol: the symbolic value may go in the main text). → Supplement.

## Summary for the Manager
- 9 distinct blocking issues after merging duplicates: (1) n_ε/n₀ dependence on n_c; (2) L-RAND hypotheses; (3) interface gaps in L-DES/L-SCORE/L-FLOOR/L-HELL (scales, NIG, σ_*); (4) the A9′ remark + Cor M1(ii) split; (5) the A7′ plain-English overclaim; (6) Prop LB hypotheses; (7) L-DES at n + the (ND) derivation; (8) L-SIZE split; (9) Lean axiom gaps / build order. NEON-7 is recommended downgraded (absorbed by O(1)).
- Every finding is recommended ADOPT, except the spine choice in NEON-11(1) (the per-n spine is optional, not mandatory).
- No finding challenges a theorem's mathematics or the KEY-step routes. All three seats verified S-2 (c = C_β²/16 > c₀), the anchored floor, M-4 (raw-Z LIL, O(log log n) vs ½log n) and D-2.
