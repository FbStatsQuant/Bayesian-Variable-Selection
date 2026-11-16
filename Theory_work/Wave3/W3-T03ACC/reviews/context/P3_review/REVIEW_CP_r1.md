# CP reviewer (Claude Personal, Opus 5.5 xhigh, Plan agent), round 1 — final reply, verbatim

# Review report — T03 (A2) PROOF_v1, packet `<PC_HOME>\Documents\T03_review_packets\CP_r1\`

**Overall verdict: verified.** Every step of PROOF_v1 was checked by hand against STATEMENT.md; the proof establishes exactly conclusions (i)–(v) from G, R, SE, H-T02 and BM-C (or BM-∞), with (iv) using no beta-min. No fatal error and no gap was found; four exposition findings follow. Small single-seed Python checks (described at the end) agree with every identity and inequality tested.

Files read: only the four packet files. No files were written. PROOF_v1.pdf was spot-checked (pages 5–10) and matches the .tex; lemma/equation numbers below follow the PDF.

## Findings

**F1** — Location: throughout (most visibly Lemma 1, eq. (3), Lemma 10, Lemma 13). Severity: exposition. Claim: notation clashes — `w` denotes both the prior weight w(k) (also inside ℓ(S) = w(|S|)m(S)) and the contrast response vector w = Uᵀyʳ; also M (the bound on ‖μ‖²/n) vs M_S, M_*, M_n; N = n−1 vs N_S; U vs U_n vs 𝒰; K vs K_{s0,j1}; J as J(S) and as a generic index set. Evidence: e.g. the proof of Lemma 13 uses w(|S|)/w(|S'|) and ‖w‖² side by side. Every occurrence is disambiguable from context; no mathematical consequence. Verdict on this step: verified.

**F2** — Location: §7 (ii), "This holds for every data set", written under the blanket "Throughout n ≥ n_0". Severity: exposition. Claim: STATEMENT (ii) asserts the PIP bound deterministically for every data set (hence every n); the proof states it under n ≥ n_0. Evidence: the argument uses only S_0 ∈ Ω (s_0 ≤ K), so it holds verbatim for every n with s_0 ≤ K; when s_0 > K, Reading 2 sets π(S_0) := 0 and the bound reads |PIP_j − 1{j∈S_0}| ≤ 1, which is trivially true. The proof treats this case explicitly for (iii) but not for (ii). Verdict on this step: verified.

**F3** — Location: Step 0 (eq. (6)) and the second "elementary fact" at the start of §7. Severity: exposition. Claim: H-T02 and the removal of the 𝒢_n restriction only control lim_L limsup_n; Reading 1 defines O_P as tightness (sup over all n). The proof does not say why finitely many small n are harmless. Evidence: for each fixed n the quantities X_n/a_n are bounded (e.g. n^{1/2}Π(|S|>m_n|y) ≤ n^{1/2}; 1−π(S_0), Π(S ⊉ J_n|y), 1−min PIP are ≤ 1 while r_n > 0), so limsup-tightness implies tightness. One-line fix. Verdict on this step: verified.

**F4** — Location: §1 "Asymptotic conventions"; Lemma 10(b) ("δ_n ≤ 1/2 for n ≥ n_0 since δ_n → 0"); Proposition 12(b). Severity: exposition. Claim: n_0 is said to depend only on (s_0, A, φ_0, σ², M), but δ_n, ε_n, q_n depend on p_n through m_n; the needed uniformity is not stated. (Under BM-∞, the eventual M_n ≥ M_* threshold also depends on the sequence (M_n); the proof handles this separately.) Evidence: by (2), δ_n ≤ 3√(log n/N) + C_A(C_m log n + s_0)log n/N, a function of (s_0, A, n) only, and the ε_n, q_n bounds follow. In any case the conclusions are asymptotic along a single sequence, so sequence-dependent thresholds are harmless. Verdict on this step: verified.

## Steps checked (all verified)

§1–2: eq. (1) (W_K cancels); eq. (2) (ceiling + 1 ≤ log n for n ≥ 3); s_0 ≤ K threshold (n ≥ 2s_0, since s_0 ≤ p always); Lemma 1(a) — G_S = X_{c,S}ᵀX_{c,S}, s_y z_S = X_{c,S}ᵀw, ‖w‖² = N s_y², s_y²Q_S = Q^c_S, log m(S) decomposition giving (3); Lemma 1(b) — w = μ_c + e, e ~ N_N(0,σ²I), ‖μ_c‖ = ‖μ‖, μ_c ∈ col(X_{c,S_0}); forward reference to Lemma 2(b) is non-circular.

§3: Lemma 2 (push-through identity; h increasing, < n/(n+1); h(g) ≥ (n/(n+1))(1−η_n) at g = Nφ_0²; operator monotonicity via antitonicity of inverse); Corollary 3 (both inequalities, S = ∅ case); Lemma 4 (f increasing, 1 ≤ f < n+1, interlacing index bookkeeping, both ratio bounds); Lemma 5 (ratio (k+1)/(2p−1−k); in (b) each factor ≤ 1/2 iff s_0+i ≥ 1, factor 2 for s_0 = 0; binom(s_0+j,j) ≤ (j+1)^{s_0}); Lemma 6 (S' = S ⊔ J, min over γ); Lemma 7(a) (Chernoff algebra gives exponent −s² with λ = s/(a+2s); lower tail exp(−t²/(4d))), 7(b) ((τ/2)^{d/2}/Γ(d/2+1); Γ(z+1) ≥ z^z e^{−z}) — both proved from scratch, so nothing rests on the Laurent–Massart citation.

§4: ranks (SE ⇒ full column rank up to m_n+s_0, so χ²_J ~ χ²_{|J|} exactly, N_S/σ² ~ χ²_{|J(S)|}); (G1) 2/n with 2 log n ≤ √(N log n) once N ≥ 4 log n; (G2),(G3) union bounds Σ_k e^{−k}/n = 0.582/n ≤ 1/n and 2k+3x_k ≤ (8+3A)k log n; (G4) count (j_*+1)p^{j_*}·2^{s_0} and threshold 2s_0+3x ≤ C_* log n; total 5/n. Lemma 10(a) (‖w‖² ≤ 4n(M+σ²), b ≤ 6b_0(M+σ²) using n/(n−1) ≤ 3/2), (b) (Q^c_S ≥ ‖(I−P_S)e‖²), (c) (I−M_S ⪯ (I−P_S) + ((1+nη_n)/(n+1))P_S; Pythagoras through S'; E_n bounds), (d) (n³ ≤ (n+1)²(n−1) ⟺ n²−n−1 ≥ 0).

§5: eq. (4); Lemma 11 (exact ratio formula; νn/((n+1)N) = ½(1 + (0.02n+1)/(n²−1)); θ_n − 1 ≤ 2(δ_n + c_n); ε_n → 0); Proposition 12(a) (e^{(θ_n−1)τ_j/2} = e^{jε_n}), (b) (exact combination of factors into q_n^j; tail sum ≤ K_{s0,j1}q_n^{j1+1}; q_n ≤ √(eC_A)r_n eventually), (c) Markov.

§6: Lemma 13 (prior (2p)^{|J|}; determinant (n+1)^{|J|/2}; (1−x)^ν ≤ e^{−νx}, 0 ≤ x < 1; denominator-enlargement case split; V/(E+V) ≥ min(V/2E, 1/2); n²/(n²−1) factor; n²/(4(n+1)) ≥ n/5 for n ≥ 4); Lemma 14 (√V_S ≥ √Δ_S − √N_S; N_S ≤ Δ_S/4; log 2 + ½log(n+1) ≤ log n for n ≥ 5, fails at n = 4 so n ≥ 5 is needed); Lemma 15 (≤ 2^{s_0}−1 preimages of each S'; |J'| ≤ |S| ≤ m_n; j_* ≥ (2A+1)s_0+1 ⇒ (j_*+1)/2 ≥ s_0(A+½)+1 ⇒ rate (log n)^{(j_*+1)/2}/n).

§7: Step 0 (2^{−m_n} ≤ (2p)^{−s_0}n^{−(s_0+2)/2} ⇒ (1+1/n)^{s_0/2}n^{−1/2}Θ); Step 1 (Lemma 6 + BM-C ⇒ Δ_S ≥ (1−1/n)M_*σ² log n ≥ L_*σ² log n; L_* ≥ 4C_* and L_*/32 ≥ s_0(A+1)+2 ⇒ κ_n ≤ e^{ρ_n}n^{−2}; BM-∞ ⇒ BM-C eventually); (i) exhaustive three-way split of Ω∖{S_0}, each piece O_P(r_n), removal of 𝒢_n; (ii) PIP bound and MPM = S_0 on {π(S_0) > ½}; (iii) strict maximiser on {π(S_0) > ½}, Markov, bounded convergence; (iv) no beta-min used, 𝒰_j are underfitting, Δ_S ≥ L_*σ² log n from θ_j alone, union over |J_n| ≤ s_0, J_n = ∅ case; (v) division by c².

H-T02 is used only in Step 0, with a deterministic m = m_n, matching its quantifiers. No result beyond the stated hypotheses and standard linear algebra/probability (Cauchy interlacing, operator antitonicity of the inverse, Gaussian projection ⇒ χ², bounded convergence) is used. The constants j_*, C_*, L_*, M_*, C_A are used exactly as defined.

## Numerical evidence (local, single seed each)

- Seed 1, n = 12, p = 6: max |s_y²Q_S − Q^c_S| = 1.6e−14; max |M_S − h(YYᵀ)| = 7.4e−14; Lemma 2(b),(c), Lemma 4, Corollary 3 hold on all subsets/nested pairs checked.
- Exact rational checks: Lemma 5(a),(b) no violations for p ≤ 39 / p ≤ 29 (Lemma 5(b) attained with equality: max lhs/mid = 1.0).
- Lemma 7(a) against exact χ² tails: no violations; Lemma 7(b) matches numerical integration (rel. error 4e−11); n³ ≤ (n+1)²(n−1), n/5 step, ν identity verified.
- Grid over A, s_0, n, p ≤ n^A: eq. (2), Step 0 bound, (G2) and (G4) thresholds — no violations; constant relations j_*, C_*, L_*, M_* verified.
- Seed 7, n = 200, p = 8, s_0 = 2: deterministic cores of Lemma 11 and Lemma 13 (before the good-event substitutions) and Lemma 10(c)'s first claim hold for all 192 underfitting S.

**Overall verdict: verified.** (F1–F4 are presentation issues with no mathematical consequence.)
