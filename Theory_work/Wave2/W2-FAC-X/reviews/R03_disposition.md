# R03 disposition (X1–X3 lemma check, Codex gpt-6.1-sol high)

Verdicts: X1 VERIFIED-WITH-AMENDMENTS; X2 VERIFIED-WITH-AMENDMENTS; X3 FAILED as written (one MAJOR); no FATAL.

X1 item 1 (MINOR, ambient f_⊥ vs frame): wording fixed in X1.1 (conditional law of (η, φ) does not depend on e₁).
X2 items 1–4 (MINOR): D6 grid count 3n(H̄ + 1) and Bin(m_all, q) ≤_st Bin(p, q); D6 stated for the finitely many
deterministic widths 𝒲_n = {4.3ϖ_n, 9ϖ_n}; (v) uses (#Band + 17) ≤ 18p; standing assumptions cite D1–D4 with the s²
derivation and ω² ≤ q_T.
X3 item 1 (MAJOR): accepted. The direction-specific bound on L_i and the strict ω < 2L + 2ϖ were false (R03's explicit
configurations). (iii) now reads d_i = min(L_i, R_i) < 2ϖ/(|K_i| − 2 + κ′), ω_i ≤ 2d_i + 2ϖ, proved in both cases
d = L and d = R < L; consequences ω_i < 4ϖ (|K_i| ≥ 3) and ω_i < c(κ′)ϖ (general) are unchanged, so (v)–(ix), X4.3 and
X4.5 are unaffected (X4.3's sentence updated to the d_i form). Note: N3X tested only the width consequence, as R03
observes; the corrected statement's two inequalities are what the downstream proofs use.
X3 item 2 (MINOR): (i) qualified for K_i = ∅ (hole = whole line).
R03's computational checks (Schur residual 1.4e−20; swap identity residual 3.6e−15) recorded as evidence.

## R03b (fresh re-check of the repaired X3, Codex gpt-6.1-sol high): VERIFIED-WITH-AMENDMENTS, no FATAL/MAJOR
All nine claims verified. MINOR 1 (proof of (i) for empty K), 2 (ϖ = 0 endpoint argument in (viii)), 3 (final remark
needs |K| ≥ 3; two-point counterexample) — all applied to X3_softgap.md.
