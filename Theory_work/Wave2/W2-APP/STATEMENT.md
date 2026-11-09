# W2-APP — STATEMENT (applicability map)

Ticket W2-APP, Theory Wave 2. Lead: Claude Opus 5.5 (Claude Personal). Status of this file: **v1.3.1 — LOCKED** (2026-11-09; v1.2 = R03 item 1: enlarged-Q bound added to LOC-B; v1.2.1 = R07 #1: same bound in (E)(f); v1.3 = claim (F) ENUM added after council r1; v1.3.1 = (F) restated with the coded inequality (EXB), council r2) after R01 (Codex gpt-6.1-sol high, LOCK-WITH-CHANGES;
all ten required changes applied, see `reviews/R01_disposition.md`). Later changes are logged in LOG.md.

Abbreviations. FIN = `Theory_work/Wave1C/FINAL/sections/` (consistency chapter v1.0, council-passed);
GROW = `Theory_work/Wave1C/C-GROW/`; GEN = `Theory_work/Wave1/W1-GEN/`; PXN = `Theory_work/Wave1/W1-PXN/`;
PACK = `Theory_work/Wave1C/C-PACK/`; MIS = `Theory_work/Wave1C/C-MIS/`. Method = production core v3.1 as merged on
main at 4676af6 (LS0 from the start mode with move cap ℓ_n + |S̃₀|, i.e. GROW's MR1 is shipped; Wave-2 PROTOCOL
"The method"). All results are asymptotic (n → ∞); no finite-n claims are made or sought.

## 0. Target

An honest, checked map: design family × hypothesis of the paper's consistency results → holds / holds under a
stated condition / fails, each entry with its lemma file and check. Results whose hypotheses are mapped:

* **POST** — posterior level: T03♯ (FIN `s3_posterior.tex:5-15`): R, SE_λ(j₀), SE_w(m♯_n; g₀), beta-min; with its
  random-design transfer (diagonal argument, GROW L6 §7 / GEN L5.3) and the deterministic corollaries SL0/SL1.
* **GEN** — reported model, bounded relevance set: (H0), (H1), (H2) / canonical certificate (C1′) (FIN `s5_hpm.tex:42-56`).
* **GROW** — reported model, growing relevance set: (H0), (G1)–(G4) (FIN `s5_hpm.tex:62-74`), incl. random AR(1) (C5)(c).
* **LOC** — (new, this ticket) reported model for random Gaussian designs with exponentially local correlation:
  a generalisation of GROW (C5)(c) (GROW `lemmas/L6_random_AR1.md`) from AR(1) to every Σ in the class LOC below.
* **MIS** — misspecified candidate sets (FIN `s3_posterior.tex`, Theorem MIS; Prop. P neighbour rule): which families
  keep the projected support fixed.
* **FAC** — factor / equicorrelated designs with growing p: tickets W2-FAC-A/B; this ticket records their status
  verbatim if a result lands, otherwise "pending" (no claim).

## 1. Setting (random design, as GROW (C5)(c))

Raw rows iid N(m, Σ_n) (n × p, p = p_n ≤ n^A, A ≥ 1 fixed; p ≫ n allowed); X = column-centred and sample-standardised
raw design; WLOG Σ_n has unit diagonal (sample standardisation is invariant to column scaling; Σ_n denotes the
population correlation matrix). Signal convention as in the study generator: Y = Xθ* + Cε with fixed nonzero θ* on
the standardised scale on S₀ (|S₀| = s₀ fixed; positions may move with n; |θ*_j| ∈ [θ_lo, θ_hi] ⊂ (0, ∞) fixed),
ε ~ N(0, σ²I_n) independent of the raw design, σ² > 0 fixed, response scaled inside the score. Fixed-design
statements are flagged as such. Implementation premises as in FIN §1.4 (EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, complete scans; IND-T and the
prescribed extra search from c₄ when R′ > 4; for the GROW/LOC route the emitted LS0 centre is some maximiser of γ₀,
which the coded routine satisfies by W1-N3(a); e4′ for GEN/PXN) — named, not proved.

**Three separate questions per table entry (R01 suggestion):** (Σ) does the covariance family satisfy the design
hypotheses; (θ) which signal-dependent hypotheses (beta-min, PTV, visibility, non-cancellation) are additionally
needed — stated, never claimed to hold; (T) does the reported-model theorem then apply.

## 2. Claims to be proved (new) — each in its own lemma file

**(A) POST for random designs — Lemma POST** (`lemmas/L1_POST.md`). LSF: (i) λ_min(Σ_{n,S}) ≥ φ² for |S| ≤ s₀ + j₀
(fixed φ); (ii) λ_min(Σ_{n,S}) ≥ ψ_n for |S| ≤ k̄_n := min(p, s₀ + max(j₀, m̄_n)), ψ_n√n/(log n)^{3/2} → ∞, with the
explicit cutoff m̄_n := ⌈[s₀(A log n + log 2) + log 2 + ((s₀+2)/2) log n]/log(3/2)⌉ ≥ m♯_n (p ≥ 2; p = 1 trivial).
Conclusion: X-measurable events 𝒜_n := {max_{j,k}|R̂_jk − Σ_jk| ≤ D_A√(log n/n)}, P(𝒜_n) → 1, on which EVERY design
satisfies R, SE_λ(j₀), SE_w(m♯_n; 1), BM-∞ with common constants φ₀² = φ²/2, g₀ = 1, M = s₀²θ_hi² + 1 and a common
deterministic BM envelope; by the diagonal TIGHTNESS transfer (C-PACK I4:57-60), 1 − π(S₀) = O_P(√(log n/n)) under the
joint law, and SL1 (a)–(e) hold with r_n = √(log n/n) (SL1(b) for thresholds q_n with r_n = o(min(q_n, 1 − q_n))
only). λ_min(Σ_n) ≥ c gives LSF; λ_max is never needed ("idiosyncratic floor" = a fixed floor of the population
CORRELATION matrix).

**(B) Lemma CT + Lemma CD** (`lemmas/L2_CT.md`). CT: explicit t*(α, K, a) by exponential conjugation. CD (population
statement, two CT applications: Σ → Θ, then Θ_VV → (Θ_VV)⁻¹ on inherited, uncompressed positions):
|Cov(W_j, W_k | W_U)| ≤ K₂e^{−t₂d(j,k)} for ALL U, Var(W_j | W_U) ≥ c; constants depend only on (c, C, K, a); the
Σ-decay and Θ-decay versions are equivalent up to changed constants.

**(C) Theorem LOC** (`lemmas/L3_LOC.md`). (Σ) LOC(c, C, K, a): unit-diagonal Σ_n, spectrum in [c, C], exponential
decay of Σ_n or Σ_n⁻¹ along a bijection π_n with FIXED (c, C, K, a). (θ) PTV(a₀), a separately labelled signal
hypothesis, uniform in n: |Cov(W_j, Σ_kθ*_kW_k | W_U)| ≥ a₀ for every j ∈ S₀, U ⊆ [p] ∖ {j}, |U| ≤ 15; sufficient:
|θ*_j|c − K₂Σ_{k∈S₀∖{j}}|θ*_k|e^{−t₂d(j,k)} ≥ a₀. (T) Q⁰ := S₀ ∪ {l : d(l, S₀) ≤ d_n} first, enlarged to [p] if
p < 2|Q⁰| + 32s₀ + 1; 𝓛 := {T : S₀ ⊆ T ⊆ Q}. The three joint-law events (sandwich incl. global size ladder for every
maximiser, NA(𝓛), TL(𝓛)) are proved DIRECTLY (literal (G3c)/(G4-dir) are NOT claimed), with the gate
**NA lemma L3.6**: window T′ = T ∩ {d(·, l) ≤ r_n}, r_n = ⌈log log n/t₂⌉, ≤ p·2^{2r_n+1} reference innovations, and
an explicit uniform bound max_{T,l}|Z_{T,l} − Z′_{l,T′}| = o_P(1). Then D_n → 0 and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 with the shipped
LS0 cap. **Variant LOC-B** (same file): block-diagonal Σ_n (blocks of size ≤ g_n, possibly growing, unbounded λ_max
allowed) with λ_min ≥ c, ≤ one truth per block, PTV, and |Q ∖ S₀| ≤ (1 − δ₀) log n AFTER the enlargement rule (i.e.
s₀(g_n − 1) ≤ (1 − δ₀) log n, and p − s₀ ≤ (1 − δ₀) log n when Q = [p]) [R03-1, v1.2]: same conclusions, NA via GROW
L2.3(a) (G4-χ) conditionally on X.

**(D) Lemma VN** (`lemmas/L5_VN.md`). Population response V := Σ_kθ*_kW_k + σξ (single row, ξ independent).
(F16) λ_min(Σ_{n,S}) ≥ c for |S| ≤ 16 + s₀; deterministic 𝒩_n ⊆ [p] ∖ S₀ with Corr(W_l, V | W_U)² ≥ κ_n for all l ∈ 𝒩_n,
U ⊆ [p] ∖ (S₀ ∪ {l}), |U| ≤ 15, nκ_n/log n → ∞, uniformly in n. Conclusion: w.p. → 1 every maximiser S̃ of γ₀ has
|S̃ ∖ S₀| ≥ min(K − s₀, |𝒩_n| − 15s₀). GEN route obstructed when |𝒩_n| → ∞; GROW/LOC sandwich obstructed when
min(K, |𝒩_n|)/log n → ∞. An obstruction to the ROUTES, not a statement that the method fails.

**(E) Family map** (`lemmas/L4_families.md`), separate rows, each entry (Σ)/(θ)/(T) with positive / conditional /
obstructed / unproved status:
 (a) iid; (b) bounded spectrum: POST always; reported model under LOC-locality + PTV; STAR (explicit, spectrum
 [½, 3/2], m_n = ⌊n^{1/3}⌋ leaves) obstructed by VN — a counterexample to the ROUTES, not to all non-local designs;
 (c) AR(1) (cited GROW (C5)(c)); stationary Toeplitz with |γ(h)| ≤ K′ρ^h and spectral density in [m, M] (uniform
 constants): LOC; summable polynomial decay: POST if spectral density ≥ m > 0; reported model unproved (no claim of
 obstruction); (d) banded Σ or Σ⁻¹ with FIXED bandwidth and spectrum in [c, C]: LOC; (e) bounded blocks (any fixed g,
 incl. g > 16) with spectra in [c, C]: LOC (Σ); PTV automatic with ≤ one truth per block, may fail with several
 (explicit cancellation example); study S1/S3/S4/S6 (GEN (C5)(d), cited, production cap) and S2 (GROW (C5)(c), cited);
 role of make_blocks (none for LOC; SEL uses containment of whole groups in actual blocks; PXN needs SIZE);
 (f) growing equicorrelated blocks, fixed ρ ∈ (0, 1), ≤ one truth per block: POST; LOC-B if s₀(g_n − 1) ≤ (1 − δ₀) log n and, when the enlargement gives Q = [p],
 p − s₀ ≤ (1 − δ₀) log n [R07-1];
 VN-obstructed (with explicit κ, truths with θ_lo > 0) if g_n/log n → ∞ (GEN route already when g_n → ∞); intermediate
 regime unproved; (g) equicorrelation / factor models: POST (fixed floor of the correlation matrix); VN-obstructed
 only under a quantified visible-null floor (equicorrelation with |Σ_kθ*_k| ≥ θ̄₀ > 0; one-factor with |b_l| ≥ b₀ on 𝒩_n,
 |b_{S₀}ᵀθ*| ≥ β₀, idiosyncratic floor); cancellation/weak exposure: no claim; reported model per FAC (FAC-A PROVED-CHECKED for its narrowed class, synced after council r3).
 MIS column: only (i) AR(1) (Prop. P, cited) and (ii) block-diagonal with bounded blocks under MIS's own
 jointly-Gaussian raw-slope model (projected support inside the omitted variable's block); general banded precision
 NOT settled (marginalisation fill-in, R01 item 9); factor designs: Prop. P remark (can grow; can also cancel).

**(F) Lemma ENUM** (`lemmas/L6_ENUM.md`; v1.3, restated v1.3.1): for every sequence on which the coded exact-branch
inequality (EXB) Σ_{k≤K}C(p,k) ≤ (5H₀ + 4N₀)p holds eventually, under EX-A, POST's conclusion implies
P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0. Sufficient: 2^{p_n} ≤ 4np_n (e.g. fixed p; p_n ≤ c log n with c < 1/log 2; 2^{p_n} ≤ n). It overrides
'unproved'/'route-obstructed' reported-model entries on all such sequences.

## 3. Empirical part (descriptive; no theorem is "verified" on a finite data set)

Design-only diagnostics on public designs (sources recorded): correlation spectrum / factor strength, partner
counts before/after factor removal, sparse minimum eigenvalues (exact small k; search upper bounds; rigorous
Gershgorin/interlacing lower bounds), m♯_n, the method's actual partition (core v3_blocks) and between-block
leakage. Output: classification local vs pervasive and the theorem class each design *resembles* (design-only).
Signal-dependent conditions (beta-min, PTV, visibility) are not checkable; any plug-in is labelled as such. Sparse
eigenvalue searches give UPPER bounds on sparse minima (witnesses of badness); only exact enumeration, Gershgorin
and interlacing give lower bounds — each number is labelled.

## 4. Not claimed

Finite-n statements; non-Gaussian rows (sub-Gaussian extension is an open remark); index sets with more than
one-dimensional neighbourhood growth (spatial lattices in d ≥ 2) for LOC; delivery P(𝒪) → 1; anything about FAC
beyond the W2-FAC reports.

## 5. Dependencies (statuses verbatim)

T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF:
VERIFIED* (A-REV5))"; GEN "PROVED-CHECKED"; C-GROW "PROVED-CHECKED" (L6 random AR(1): R07 VERIFIED, R06
VERIFIED-WITH-AMENDMENTS); W1-PXN "PROVED-CHECKED"; C-MIS "PROVED-CHECKED"; SL0/SL1 "PROVED (by this seat,
unchecked)", C-PACK council passed; [OP] "PROVED (by this seat, unchecked)" inside GEN.
