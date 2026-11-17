# W3-D3 — PLAN (v0.1, 2026-11-17 13:05 CST; lead Claude Opus 5.5 high) — track D ticket #3, sub-Gaussian rows for Thm 2

Owner D105/D112 (#3 required; reuse W3-DIST's bridge). Tier B rider. **Plan stage: no proving before the manager's GO.**

**Target (coexisting claim `W3-D3:Thm2SG`; row 1.2, `W2-APP:POST` and their consumers untouched).** Reader Thm 2
(`W3-READER/READER_VERSIONS.md:263-275`) with *one* change: "rows i.i.d. N_p(m_n, Σ_n)" → **rows i.i.d. with mean m_n,
covariance Σ_n a correlation matrix, and (SG) sub-Gaussian sparse directions:** E exp(λuᵀ(x − m_n)) ≤
exp(K²λ²·uᵀΣ_nu/2) for all λ ∈ ℝ and all u with ≤ w_n := ⌊5(A+1)(s₀+1) log n⌋ nonzero entries (K fixed). (A1) (S1)+(S2),
(A2) fixed s₀, b_lo ≤ |β*_j| ≤ b_hi, (A3) floor φ² on |S| ≤ 5(A+1)(s₀+1) log n: **verbatim**. Conclusions verbatim:
1 − π(S₀|y) = O_P(√(log n/n)), P(HPM = MPM = S₀) → 1, max_j|PIP_j − 1{j∈S₀}| = O_P(√(log n/n)). Gaussian rows = K = 1.

**Where Thm 2's proof uses Gaussian rows** (master `W3-POST:Thm-1@1.0.1` item 6 + bridge `W2-APP:POST@1.0.7`(a), `L1_POST.md:27-71`):

| # | Step (L1_POST) | Gaussian use | Covered under (SG) by | Status of the cover |
|---|---|---|---|---|
| G1 | (2)–(3) entrywise event 𝒢_n (`C-GROW:L6.2`) ⇒ sample floors (F_λ; φ²/2), (F_w; 1) | Gaussian entrywise tails | `W3-DIST:B2core` (𝓔₂(q): uᵀΣ̂^z u ≥ ½uᵀΣu on q-sparse u) + `B2`(a) + `B3` Steps 3–4: (F_λ; φ²/4), (F_w; φ²/8) | PROVED-CHECKED (council R2) |
| G2 | raw-scale event ℋ_n (sd ratios in [½, 2], χ² tails) ⇒ θ* = D_xβ* in [b_lo/2, 2b_hi]: (E), BM-∞ | χ² tails | `W3-DIST:B1` (𝓔₁, single-coordinate (SG)) + `B3` Steps 1, 5 | PROVED-CHECKED |
| G3 | no constant column a.s. (p_ret = p) — implicit | continuity of the law | `B1`(b) on 𝓔₁ + `B3` amendment A-2 (replacement off the event) | PROVED-CHECKED |
| G4 | (5) diagonal transfer to the joint law | none (needs ε ⟂ design, Gaussian ε) | `W3-POST:Thm-1` item 6 (unchanged; (A1) keeps Gaussian noise) | PROVED-CHECKED |
| G5 | window sizes: sets S₀ ∪ J with \|J\| ≤ j₀ or ≤ m♯_n lie in the floor/(SG) window | none | `W3-READER:R1@1.0.2` B1.2, B1.3: s₀+j₀ ≤ (2A+2)s₀+2, s₀+m♯_n ≤ 3(A+1)(s₀+1)log n | PROVED-CHECKED |

**Reuse verdict: SUCCEEDS — no step needs new probability theory; TRACK_D's stop condition (energy/beta-min needing more than
(A3) on sparse directions) is not met** (energy from `B1`(c), beta-min from 𝓔₁). Only new text: `B3` re-instantiated on the
window w_n instead of W3-DIST's q_n = min{p, ⌈C_q log n⌉} (needed: at s₀ = A = 1, C_q log n > 5(A+1)(s₀+1) log n, so `B3`
verbatim would ask (SG) and the floor on a slightly larger window than Thm 2's); `B2core`, `B2`(a) are stated for every q.

**Deliverables (after GO).** `STATEMENT.md` (delta over Thm 2 + `W3-DIST` §3; deps/supersession table: COEXIST),
`TARGET.md`, `lemmas/B3w.md` (copy of `B3.md`, changed lines [R-#]: Step 0 → R1 B1.2/B1.3; (vii) → B2core at q = w_n with
w_n log(ep/w_n) ≤ c₂n/K⁴ for n ≥ n₀(s₀, A, K)), `lemmas/ASSEMBLY.md` (B0 → B3w → item 6 → conclusions 1–3; one example
lemma: x = m + Lξ, ξ independent unit-variance K-sub-Gaussian coordinates ⇒ (SG) with K, class 2a), `numerics/` (window
grid; small exact-posterior run with Rademacher/uniform correlated rows), `READER_DELTA.md`, DEPS, REPORT, API card.
≈ 1.5 days with checks (Sol lock; blind Opus line check; council Sol + Opus; Opus diff rounds; CP3 + API blind-audit card).

**D109 classes of the hypotheses.** (SG) with constant K: **class 1** — same assumption and class as Thm 9 (A3)
(`ASSUMPTION_COMPLIANCE.md:31`, PREC B7b: NH14 Lemma 6.1 sub-Gaussian rows; implies SL Condition 1, TRACK_B B7); 2b note:
holds with K = 1 for Gaussian and Rademacher-mixed rows; fails for rare binary predictors (PREC B7b). Window w_n: same as
Thm 2's floor window (class as row 1.2: 1 and 2b). All other hypotheses inherited verbatim from row 1.2 (classes at
`ASSUMPTION_COMPLIANCE.md:27-29`). No new constant besides K.

**Relation to W3-D2 (Thm2X).** Orthogonal axes, no duplication: Thm2X keeps Gaussian rows (its master `W3-MISR-R:CorGb-plus`
uses Gaussian omitted predictors structurally) and upgrades the *conclusion* to expectation rates on a smaller window;
#3 keeps row 1.2's O_P conclusion and widens the *row law*. Sub-Gaussian + expectation is not delivered and not claimed.

**Free options for HQ (default: OFF, no new scope).** (o1) window 3(A+1)(s₀+1)log n (R1 B1.3; matches Thm2X);
(o2) floor c/n on the log window, fixed φ² only on (2A+2)s₀+2 sets (`B2`(a)/`B3` split). Each is one statement line.
