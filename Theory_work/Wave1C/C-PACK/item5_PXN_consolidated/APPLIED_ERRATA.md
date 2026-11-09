# APPLIED_ERRATA — where each erratum E-1..E-22 was applied, and what was dropped

Files: 00 = 00_statement_and_conventions.md, 01 = 01_tools.md, 02 = 02_design_events.md, 03 = 03_start.md, 04 = 04_search.md,
05 = 05_posterior_output.md, 06 = 06_A_dependence_and_scope.md. "PROOF" = the candidate proof (old file); line numbers refer to it.
(This file, like MAP.md, may contain old-file references; the proof files do not.)

## A. The 22 errata

| # | Applied in | How (resulting text, quoted) |
|---|---|---|
| E-1 | 01 §1.4 (Lemma E; also the "two applications" paragraph) | "P(𝒟ᶜ ∩ ℰ*) ≤ 2e^{−n^{1/3}} + C n^D [n^{−4(D+1)} e^{√(8J(D+1) log n)} + 2n^{−2(D+1)}] → 0"; same bound repeated for 𝒟_start and 𝒟_search with their (J, D, C). Proof (d1): "probability ≥ 1 − 2e^{−n^{1/3}} by [LM]". |
| E-2 | 01 §1.4 (Setting); 02 §2.2 (consequences) | "𝔉 = 𝔉_n is a deterministic (or X-measurable) family … Fix φ₀ > 0 and M. Let ℰ(𝔉, φ₀) := {λ_min(R̂_A) ≥ φ₀² for every nonempty A ∈ 𝔉} (an X-event) and ℰ* := ℰ(𝔉, φ₀) ∩ {‖μ‖² ≤ Mn} (or any X-measurable subevent of ℰ*). The conclusions hold for n ≥ n₀ …". Applications use ℰ♯_n (02 §2.2: "ℰ♯_n ⊆ ℰ(𝔉, φ₀) ∩ {‖μ‖² ≤ Mn} = ℰ*(𝔉) for both families"). |
| E-3 | 01 §1.4 Remark (2) | "The signal-norm bound is used to control ‖Y‖² and hence the standardised RSS floor in (E3), and to obtain the uniform n^{2/3} approximation in (E5). The raw-scale RSS lower bound itself does not require it." |
| E-4 | 01 §1.4 (E5) and its proof | "(E5) … with the admissible explicit constant C₂ = 4σ√(M(D+1)) + σ²[5 + 8(D+1)], for n ≥ n₀"; proof uses √(log n) ≤ n^{1/6}, log n ≤ n^{2/3}, 1, n^{1/3} ≤ n^{2/3}. |
| E-5 | 04 §4.1 Lemma Λ(a), null part | "Indices with A₀ = ∅ or Λ_{A_s} = 0 are removed from the family below: their increments are 0. For n−1 ≥ gs₀, Λ_{A_s} = 0 iff S₀ ⊆ A_s a.s., a deterministic index set. For the remaining indices, (Λ_{A_s} − Λ_A)/Λ_{A_s} ~ Beta(…)" and Lemma Tr-J(c) is applied to those. |
| E-6 | 01 §1.3 (table) | Row renamed "P3′ start mass (§3.2)" (was "P3 start mass (§5)"); sentence "In both rows u is uniformly bounded by a fixed constant, so u ≤ n/4 holds for all large n; J is fixed." (was "u is fixed"). |
| E-7 | 03 §3.1 Lemma B(ii) | "(ii) For A ⊇ S° with A ∖ S° neutral and |A| ≤ n − 3, and a neutral l ∉ A: x_{A,l} … ~ Beta(½, (n−2−|A|)/2)." plus the note "the Haar calculation below requires |U| + |W| ≤ n − 2 in general. Statement (ii) is not used anywhere below." |
| E-8 | 04 §4.5 Lemma LS(i) | "the search makes min(c, ℓ) accepted moves before arrival or cap, and first reaches S₀ as a centre iff ℓ ≥ c, after exactly c moves"; the standing hypothesis includes s₀ ≤ K. |
| E-9 | 04 §4.6 Theorem P6′ | "Choose n₀ with ℓ_n … ≥ c … ; on 𝒯_n := 𝒜_n ∩ Ω_n ∩ 𝒵_n ∩ {S̃₀ = S°}: … N_scores ≤ 1 + Σ_{t=0}^{c}[p + (s+t)(p − s − t)] ≤ 1 + (c+1)(p + s₀p)"; the general bound is "1 + (ℓ_n+1) max_{0≤k≤K}[p + k(p−k)] = O(p² log(n+p))"; (K) read on the joint event 𝒯_n (00 §0.4 (K) and 04 "Conclusions"). The false "max_{k≤K}[p+k(p−k)] ≤ p+s₀p" is not present. |
| E-10 | 03 §3.4 P5 | "This **bypasses** the tie-DP invariant of the start (registry item OB03, "N3") on this event; it does not prove that invariant. Premise retained: EX-A, including exact DP arithmetic; floating-point exactness is not established by the probability argument." |
| E-11 | 05 §6.2 Closure | "The first inclusion is (G2) of GUARD (W6 conventions; Lemma RO) … The second holds because R̄⁺ contains its deterministic LS0 with the emitted centre by definition … the production bridge … remains an implementation obligation, not a step of the proof." |
| E-12 | 04 §4.4 (L), additions | The PROOF step at 363-367 is replaced in full by the corrected step of the replacement lemma: "RSS_{S₀} ≥ nσ²(1 − ε_n) … −ν log(1 − x_l) ≤ Z_l²/2 + (Z_l²/2)κ_n … F(S₀+l) − F(S₀) ≤ … = −½ log n + log log n + O(1) → −∞". |
| E-13 | 04 §4.3, bullet "Swap k → l, l in a different component" | "If the destination is an incomplete pair i′ ∈ I, its gain is at most G_{i′} ≤ G_{i*} (hub: G_{i′}; proxy: G_{i′}η_{i′}; a-group non-hub: zero). In a complete pair, visible component, or null group its gain is zero." (verbatim, with the primed index typeset i′). |
| E-14 | 04 §4.3 (convention) and §4.4 (Remark) | "Convention: min ∅ := +∞ (relevant when v = 0)." and "A first-order heuristic for addition failure is (s₀+1)/√(2π n w_n) with threshold w_n := 2 log((2p−s₀−1)/(s₀+1)) + log(n+1) (W3-PXN, PROOF.md, 330–331; about 2.5% at (n, p, s₀) = (200, 750, 3)); the proof gives only P((L) fails) → 0." (the formula (s₀+1)/√(2πn t_n) and the 2.5% figure are those of the sentence replaced at 368-370; the threshold is renamed w_n to avoid a clash with t_n). |
| E-15 | 02 §2.3 Theorem R | Display split into "(R-a) For every t ∈ (ψ̄, ρ): P(𝒜_nᶜ) ≤ S(t). (R-b) With t = t*: P(𝒜_nᶜ) ≤ S(t*) ≤ K_n … (R-c) …" plus the remark "S(t) ≤ K_n is asserted here only at t = t*". |
| E-16 | 02 §2.3 "Numbers" | The sentence "(≈ 0.17 reported as the rigorous bound in W7)" is deleted; replaced by "At (n, p) = (200, 500) the displayed bound K_n is ≈ 1.13·10⁶, i.e. vacuous". |
| E-17 | 02 §2.3 Lemma R0 and its use | W7 A0(c) is not used; the proof of Lemma R0 is the direct argument: "Under the margin every distance 1 − |r̂| inside an unfinished group is below every distance between different groups, so until all groups are complete an internal merge is available and every cross merge loses … (ties inside either class are allowed)". |
| E-18 | 00 §0.5 (Exact-branch convention); 05 §6.2 (Exact branch (cases)) | "'blocks', the block tables, π₀, S̃₀ and 'LS0 of R̄⁺' denote the deterministic make_blocks / block-table / start-mode / local-search functions of the data computed on **every** branch (hypothetical when the actual run takes the exact branch)"; cases (a)/(b) of 05 §6.2, with the zero extension π(S₀) := 0 for s₀ > K and the sharper D_n bound for s₀ ≤ K only (R21 #1, R30 #1). |
| E-19 | 03 §3.2 Remark; 00 §0.4; 06 (O4) | "and is sharp in order" deleted: "The result is an upper bound; no matching lower bound is claimed (and for slowly growing p the rate √(log p/n) is attainable)."; 00: "In (S) no statement that the rate √(log n/n) is sharp in order is made." |
| E-20 | 03 §3.2 (Statement, Moment, Conclusion) | "on {q < 1}, 1 − π₀(S°) ≤ (s+1)q/(1−q) + s·e; since P(q < 1) → 1, 1 − π₀(S°) = O_P(√(log n/n))"; "By (3.1), ã_hj 1_{𝒢_n} ≤ e^{2κ_E}(n+1)^{−j/2} Σ_{|V|=j}(1 − X_{h,V})^{−ν}1{X_{h,V} ≤ τ_{n,A}}". |
| E-21 | 06 (O3) | "(a first-order heuristic gives order n^{−1/2}(log n)^{−1/2}; the proof gives only P((L) fails) → 0)". |
| E-22 | 06 (O5) | "ρ = 0.7, ψ = 0.5, β = 1, v = 0, c = 1: G = 0.1875, η = 0.3675/0.8775, c₂ = G(1−η) = 0.10897; with σ² = 1 (M = 2θᵀΣθ + 1 = 2.5, 4(σ²+M) = 14) one gets (n/2) log(1 + c₂/14) ≈ 0.775 at n = 200 (≈ 0.904 if σ² = 0.5)" (the old values 0.07 and 0.58 are gone; the conclusion "vacuous against (2A+1) log n ≈ 20" is unchanged). |

## B. Other corrections taken from FINAL_PROOF and the replacement lemma files (not numbered errata)

- Two Lemma-E events (review R30 #2): 𝒟_start (J = g, D = A, C = 2^{16}) in 𝒢_n (03 §3.2) and 𝒟_search (J = s₀+2, D = A(s₀+2), C = 2^{s₀+2}) in Ω_n (04 §4.3); 01 §1.4, last paragraph.
- Tr-J thresholds indexed by the family exponent, t_{n,D}, τ_{n,D} (R30 #5; FINAL_PROOF §1); Mills threshold renamed u_n (04 §4.4).
- [CONC] replaced by the self-contained [CONC′] (Lemma CR) in 02 §2.2 (P8 v2 / R19 #1); the locked T03 replaced by T03♯ (dependency point D1; 05 §5); the superseded event ℰ_n of PROOF P2 is replaced by ℰ♯_n.
- Onset gloss (C1 Codex #1, Opus #5): 00 §0.5, "each onset is an explicit polylog-versus-polynomial condition in n … plus the SIZE onset n₁ … a sufficient envelope … is n/(log n)³ ≥ C(A, fixed parameters)".
- (U3): explicit sufficient onset e_n ≤ c′H/(4H+c′) and the penalty bound "2 log 2 + log(1 + 1/n) < 2 for n ≥ 2" (R17 disposition; FINAL_PROOF §0): 04 §4.2.
- (D_S)/(L): 𝒵_n probability 2/(√(2π)u_n log n) (L_strict_localmax): 04 §4.4; P6′ event 𝒯_n and n ≥ n₀ separation (R30 #4): 05 §6.3 ("For n ≥ n₀ also P(LS0 of R̄⁺ does not score S₀) ≤ P(𝒯_nᶜ) → 0").
- Production LS0 call named concretely (C1 Opus #7): 00 §0.3, Method.
- Lattice reference defined explicitly, Lat(S°) := {S° ∪ 𝓜′ : 𝓜′ ⊆ 𝓜} (C1 Opus #4, replacing the undefined 𝓡₀): 00 §0.1, §0.4 (E).
- P4 finite-n centring remark (C1 Opus #8): 03 §3.3, last parenthesis. The baseline council's finite-n centring remark is included with the additional O(1/p) prior correction; its asserted O_P(√(log n/n)) remainder alone does not hold for arbitrarily slowly growing p (R39 finding 1).

## C. PROOF passages dropped (with the reason)

| PROOF lines | Passage | Reason |
|---|---|---|
| 1-6 | file header (run attribution, "candidate, not reviewed", notation sources) | meta/status text; not mathematics |
| 8-20 | "What this file does" and the repair table of A-REV3/A-REV6 objections | meta commentary; each repair is present in the text itself |
| 22-32 | list "Cited results and their status" ([T22i], [T22ii], [T03], [W7-B], [LM], [CONC], [W6-0]) and the sentence on W1-T37R | replaced by 00 §0.7 (external citations with verbatim statuses); [T03] → T03♯, [CONC] → [CONC′] (FINAL_PROOF §1, §5); [W6-0] re-proved in 05 §6.1 |
| 98-100 | "≈ 0.17" figure | E-16 |
| 117-119 | Remark of Lemma T naming A-REV3/A-REV6 | attribution; the two substantive sentences are retained |
| 155 | Tr-J table row "W5 R1 Step 2 (outside scope)" | not used by the theorem (FINAL_PROOF §1 lists only P3′ and Λ(a)) |
| 201-202 | Remark (1) (provenance: W1-EXP lemmas) | provenance; "needs no block structure" retained |
| 205-206 | Remark (3) ("PXN Lemma U(U1)", "the false ≤ 1 … W5 R2's repair") | cross-reference to a different file and history; replaced by the explicit remainder bounds in 01 §1.4 Remark (4) |
| 213-220 | Lemma P2 (event ℰ_n; (a) size range m_n + s₀) | superseded by ℰ♯_n (FINAL_PROOF §2) with the enlarged size range L_n; its (b), (c) are 02 §2.2 (b), (c) |
| 222, 227, 234 | "(PXN §4 and W5 R6; verified by A-REV3; restated)", "(condensed; PXN §4 has the full version)" | cross-references; replaced by the in-text Haar step (see OPEN_QUESTIONS 5) |
| 270-271 | "and is sharp in order (PXN REPORT §4)" | E-19 |
| 305 | "This is A-REV3's repair" | attribution |
| 363-367 | addition step of (L) | E-12 (superseded) |
| 368-370 | "failure probability is of order (s₀+1)/√(2πn t_n) (PXN §9.3 remark, W5 R4 …)" | E-14 (reworded as heuristic) |
| 372-399 | Lemma LS (i), P6′ statements as written | E-8, E-9 (superseded by the repaired statements); parenthetical "(Lemma LS is W1-T37R Theorem A(A3) …)" dropped (cross-reference) |
| 398 | "max_{k≤K}[p + k(p−k)] ≤ p + s₀p" | false (E-9) |
| 403-417 | §9 input [T03] and its proof | superseded by P8♯ (D1); the de-randomisation lemma (405-410) is retained as Lemma 5.2 |
| 421-446 | headline restatement "PROVED given [T22i], [T22ii], [T03], [CONC], [W7-B]" | status labels; conclusions are in 00 §0.4 |
| 475-477 | "(probability of order n^{−1/2}(log n)^{−1/2})" | E-21 |
| 480-481 | (O4) remark on W5-R1 "remains GAP as reviewed … see REPORT 'Outside scope'" | cross-reference to a different file and status; obsolete cross-reference removed; c = 1 restriction, reviewed GAP status, and the limited effect of Lemma Tr-J retained in the replacement parenthesis |
| 483-484 | old numbers 0.07 / 0.58 | E-22 |
| (STATEMENT.md) | STATEMENT §3 phrase "to be confirmed per item", STATEMENT §4 (dependency points "pending") | superseded by STATEMENT §5; resolved status recorded in 06 |
| lemma files | "Why a repair", "Defects found by R15", "Issue", "Defect", "Downstream impact", "What changed vs PROOF" | repair history; the content they motivate is applied in place |
| P8 remark | "Status of the input … step 4 is this file's own argument and must be checked" | status chatter; step 4 is §5.3 |
| FINAL_PROOF | review/status words ("XF VERIFIED R19" etc.) | recorded once in INDEX.md, not inside proofs |

## D. Notation changes (no mathematical effect)

masked set M → 𝓜 (the constant M = 2θᵀΣθ + 1 keeps its name); in Theorem R, q → q_R (q is the start-mass quantity); score margin m_n(c′) → mar_n(c′) (m_n is the SE cutoff);
Mills threshold t_n → u_n; Tr-J thresholds t_n, τ_n → t_{n,D}, τ_{n,D}; (L) heuristic threshold t_n → w_n; the 2×2 matrix M in Lemma CR → 𝐌; b₀ of P2(c) (the beta-min constant, which clashes with the prior
constant b₀ = 0.01) → b_min; ℰ_n → ℰ♯_n; 𝒟_n → 𝒟_start, 𝒟_search; "Lemma P2" is not used; "[CONC]" → "[CONC′]"; "[T03]" → "T03♯"; Theorem P8′ → Theorem P8♯; Theorem 5(b1) → Theorem PXN.
