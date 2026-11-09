SCORE 9.1 — gates G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS

# W2-LOC2 — Council round 1, reviewer C1 (Claude Opus 5.5, high)

Scope read: STATEMENT.md, REPORT.md, lemmas/L1–L7, numerics/D1_SUMMARY.md, citecheck.py; upstream GEN L1_lemmaE, GROW
L0/L1/L2/L3/L6 (§§2–4), APP L3_LOC (all), L1_POST/L2_CT/L5_VN (status lines + V2), FACA L7 (status), FIN s5 (status
strings); production core v3_preprocess.R (budgets), v3_run.R (LS0 options), cpp/v3_core.cpp:460–480 (LS0 call),
cpp/v3_score.h:40 (K). Not read (per brief): LOG.md, CHECKPOINT.md, other reviews/.
Scratch: `reviews/C1_scratch_opus/` — `cc.py` (citecheck re-run writing only to scratch: TOTAL MISSES 0), `probe.py`
(falsification probes, all passed; see §3).

I tried to break the result along five lines: (i) the NA-R mechanism (does the lattice of 2^{|Q|} sets leak into the
√(2 log p) scale?); (ii) every |Q| = O(log n) use in the inherited GROW/APP proofs; (iii) the one-factor algebra and
latent extension; (iv) the polynomial-decay counting and α₀ = 17/2; (v) fidelity to the coded cap, K and blocks. I did
not find a counterexample or a broken step. Details below.

## 1. Gates

**G1 (correctness of every step) — PASS.**
* L0′ (L1_toolkit §L1.1): the only J/|𝔉|/|𝒱𝒱| uses of GEN L1 are 𝒟₂ (2^{d/2}e^{−t_n/4} = 2^{d/2}e^{−J_n}|𝔉|⁻¹n⁻² ≤
  |𝔉|⁻¹n⁻²), 𝒟₃, L1.2(a) (h_n² + t_n = o(n)) and L1.3 (J/((n−1)φ₀²) ≤ 1, which also keeps R_A ∈ [−κ_E, κ_E] — I checked
  GEN L1 (E4): R_A ≤ J/((n−1)φ₀²), so κ_E is genuinely size-free). GROW L2.2's excess needs the RATE ω_n log n → 0, which
  is correctly flagged [R02-3]. Correct.
* NA-R (L2): Step 1 identity is exact (P_TC = P_T; CW_Tβ ∈ span X_T). E_a/E_b unions over |𝔓| ≤ p2^{|Q|} with thresholds
  x, v_n = O(q + log n) enter only through δ_n, ω′_n, ϵ_n — correct; E_b uses that e_{T,l} is independent of W_T
  (Gaussian regression), correct. E_d: conditional χ² of a ≤ m₀-dimensional (W,Ξ)-measurable subspace, Chernoff, union
  over N_n frames: N_n·(ex′/m₀)^{m₀/2}e^{−x′/2} = O(1/log n) — correct. E_e: conditional on ε, (C𝒲a)ᵀε ~
  N(0, Var a‖Cε‖²) because rows are iid and the extension is independent of ε — correct, and the adaptive y_n makes
  L_n²y_n² = o(log n) with no cardinality bound — correct. Step 3: the reference part is bounded by ‖Cr‖‖P_𝒮ε‖ (Cr ∈ 𝒮),
  the atom part by L_n y_n‖Cε‖; dividing by ‖g‖ ≥ √(cN/2) gives (2.2). Step 5 exact expansion — correct. The
  conclusion 2 log p + o(log n) < c_n = 2 log p + log n − O(log log n) holds. This is the key new idea and it is sound:
  the lattice only enters through relative/additive errors, while the √(2 log p)-scale union runs over frames and atoms.
* CT_d/CD_d/RB/TAIL (L3): packing (2R+1)^d and shell (2m+3)^d correct; Schur test with the shell bound
  e^{−(a−t)m}(1 − e^{−t(m+1)}) correct; Neumann bound ‖A_t⁻¹‖ ≤ 2/α correct; CD_d uses (Θ_HH)⁻¹ with H the FULL complement
  and interlacing for V ⊆ H — correct; RB via β_v = −Ψ_vl/Ψ_ll, Ψ_ll ≥ 1 — correct; TAIL Var D = bᵀM⁻¹b — correct.
* LOC-d (L4 Part A): every APP L3.3–L3.5 size use is now polylog (|H_l| = O((log n)^d), |I_l| = n^{o(1)}, k₀ polylog,
  log k = O(log log n) in junk exclusion, ladder O(log n) indices since K ≤ n/2). (R1) frames (l, T′ ⊆ B_l),
  log N_n ≤ log p + (2 log log n + 3)^d log 2; (R2) λ = β_T − β_{T′} padded, ‖λ‖₁ ≤ 2L₀; (R3) via TAIL with κ(r_n) → 0.
  All correct.
* LOC-BF (L4 Part B): Sherman–Morrison β_A(l) = b_lD⁻¹b/(1 + s₂) and the e_{T,l} expansion are correct; the ℓ¹ bound
  ≤ b_l s₂/(b_lo(1 + s₂)) ≤ 1/b_lo is correct; (R3) with η = 0 by independence of (F_G, ξ_l) from ξ_A is correct; the
  latent extension (conditional draw of (F_G, ξ_G) given W_G with independent auxiliary randomness) preserves the law of
  (X, ε), is jointly Gaussian with iid rows and independent of ε — correct. Selection removal/spherical tail with exact
  zeros (F1) — correct; PTV automatic (F3) — correct.
* PLR (L5) and delivery (L7): the path argument (GROW L1.2(ii) with cap ℓ_n + |S̃₀| ≥ |S̃₀ ∖ S₀|) and the M5(0)
  integration are correct; L7 Step 3 obtains P(𝒦_nᶜ) from the three events directly, not from D_n — correct.
* Polynomial decay (L6): Lemma BC's cofactor-path argument is correct (the i→j component of a monomial's functional
  graph is a simple path; one edge has length ≥ d(i,j)/h; (1 + d/h)^{−α} ≤ h^α(1 + d)^{−α}; 2×2 Schur step with
  det H ≥ C⁻²). Lemma IR (banded truncation + column-weighted Combes–Thomas + resolvent, B ≍ d/log d) gives
  (1+d)^{1−α}log^{α−1}, summable for α > 2 — correct. (P8)–(P9) recursion and rates (ρ > 1/(4α)) correct; (P11)–(P12)
  need 15ρ < ½; (P14)–(P15) need max(2λ, ½) < τ < 1 − 2b; feasibility ⇔ 1/(4α) < (½ − 1/(2α))/15 ⇔ α > 17/2 — I
  re-derived this and checked numerically (feasible at 8.5001, infeasible at 8.5). (P16): coefficient difference on T′
  is −Σ_w β_T(l)_w γ_w by the tower property, so ‖λ‖₁ ≤ (1 + L₀)F(r_n) → 0 — correct; (P17) Var D ≤ ‖λ‖₁² — correct;
  (P18) ϵ_n = O(n^{b−1/2}) → 0; (P19) slack (1 − 2b)log n — correct.

**G2 (hypotheses used = stated) — PASS.** NA-R uses exactly (N0)–(N1), (R1)–(R3) and the latent-extension clause of
STATEMENT (B). PLR uses the local floor for (C-i) and LSF only in (C-ii), as stated. LOC-d uses spectrum [c, C],
separation, decay of Σ or Θ, PTV, p ≤ n^A. LOC-BF uses the global floor c_B, no upper spectral bound (APP L3.8B confirms
C was used only through CD(a)), ≤ 1 truth per group, g_n ≤ (log n)^κ. L6 uses α > 17/2, spectrum [c, C], 1-D bijection.
Small wording mismatches only (issues 3, 6).

**G3 (no hidden assumptions) — PASS.** The partition is handled uniformly (deterministic reference families; counts
J(t) are partition-free), so even the "X-measurable" premise is stronger than needed. s₀ ≥ 1 is inherited from GROW
(stated explicitly only in L6:41; NIT 8). Increasing-domain asymptotics and fixed constants are explicit.

**G4 (cited statuses verbatim, never upgraded) — PASS.** Spot-checked: APP L1_POST "PROVED (by this seat, unchecked)"
+ R02 V-W-A; APP L2_CT R02 VERIFIED; GROW L0/L1 R03 VERIFIED, L2 R03 V-W-A (2), L4 R04 V-W-A (1), L6 R07 VERIFIED / R06
V-W-A; GEN L1 R02 V-W-A; FACA L7 "PROVED (by this seat, unchecked)" R04 V-W-A; W2-APP and W2-FAC-A "PROVED-CHECKED";
T03♯ and M5(0) strings match FIN. Citecheck re-run in scratch: 0 misses. e4 "OPEN" and S.3 "AUDITED" qualifications
carried in L7.

**G5 (constants/rates tracked) — PASS.** n₀ dependencies listed (L2:107); explicit d_n, R_n, r_n, t*, K₂, t₂, L₀,
κ(r); explicit (ρ, λ, τ) for L6 (L6:469–471); κ_E fixed and size-free. Minor envelope bookkeeping (issue 4).

**G6 (fidelity to v3.1 at 4676af6) — PASS.** Cap: `cpp/v3_core.cpp:473` cap = ls0_ell + |m.S| with ls0_ell = b$ell =
⌈log₂(n + p + 1)⌉ (default "ell_n_plus_mode", `v3_run.R:100–101`) = ℓ_n + |S̃₀|, used by L5(b)/L7 as ≥ |S̃₀ ∖ S₀|.
K = min(p, ⌊n/2⌋) (`v3_preprocess.R:21`, `v3_score.h:40`). Blocks B = min(isqrt n, isqrt p, 16) ≤ 16
(`v3_preprocess.R:22`). LS0 centre from `start_mode(st, 1e6, tie_dp)` — the "some maximiser of γ₀" premise is named, not
proved, as required. No method change requested.

## 2. Overall score: 9.1 / 10

A genuinely new and clean engine (NA-R) whose probabilistic structure I verified line by line; three corollary classes
(LOC-d, LOC-BF, polynomial decay α > 17/2) each with a complete delta ledger against the inherited proofs; delivery
correctly added; scope and non-claims honest (α₀ explicitly a proof cutoff; VN attribution restricted). Deductions are
editorial: stale (D3) text in the locked statement, a STATEMENT/REPORT "not claimed" mismatch, minor envelope and symbol
bookkeeping, one over-strong numerics sentence.

## 3. Falsification probes (scratch, observations only)
* α₀ feasibility: infeasible at α = 8.4, 8.5; feasible at 8.5001, 9, 20.
* One-factor (20 000 random groups, b ∈ {0} ∪ [0.3, 0.95]): identity τ² = ϱ² + ‖λ‖² exact to 1e−9; max ‖λ‖₁·b_lo = 0.33 ≤ 1.
* CT_d on 300 irregular separated 2-D sites (exp(−‖Δ‖/1.5)): max |(Σ⁻¹)_ij| / ((2/λ_min)e^{−t*d_ij}) = 0.34 ≤ 1.
* Lemma BC (Toeplitz 0.5(1+h)^{−3}, p = 400, 3000 random U, |U| ≤ 15): max |Cov(W_j,W_k|W_U)|(1+d)^α = 0.5 (bounded).

## 4. Issues

No FATAL. No MAJOR.

1. **MINOR — STATEMENT.md:3, :85–91, :92–97.** Header still reads "v1.1 — LOCKED" while §2 carries the v1.2 fill; the
   (D3) paragraph still says "explicit α₀ to be determined … If not proved, the report gives the exact failing step (no
   claim)", immediately followed by the v1.2 claim. A reader of the locked statement sees two incompatible (D3) texts.
   *Fix:* header "v1.2 (v1.1 locked; v1.2 fills the (D3) stretch slot, logged)"; rewrite (D3) as the claim actually
   proved (α > 17/2, radius ⌈Dn^{1/(2α)}⌉, conclusions of (C-i)/(C-ii)), keeping the "not a necessity statement" and the
   "failure would withdraw only (D3)-specific delivery" sentences.

2. **MINOR — REPORT.md:164–166 vs STATEMENT.md:102–106.** REPORT §2 attributes to "STATEMENT §3" the non-claims "groups with
   ≥ 2 truths, polynomially growing groups", which STATEMENT §3 does not list (it also omits polynomial decay with
   α ≤ 17/2 and long memory). *Fix:* add to STATEMENT §3: "groups containing ≥ 2 truths; one-factor groups of size
   > (log n)^κ (e.g. polynomial); polynomial decay with α ≤ 17/2 (incl. long memory); polynomial decay in d ≥ 2".

3. **NIT — STATEMENT.md:12–13.** "Rigorous examples of such start modes: APP L5_VN (V2) …; component-port observations for
   d = 2" — the colon list puts observations under "Rigorous examples". *Fix:* "Rigorous example: APP L5_VN (V2) …
   Observations only (not rigorous): component-port runs for d = 2 (numerics/D1_SUMMARY.md)."

4. **NIT — L1_toolkit.md:47 (also :57).** Gram-floor paragraph fixes J_n := (log n)^κ, but it is applied to |Q ∪ {l}| up to
   (log n)^{κ+1} (L4:101, :158) and to the lattice family with envelope κ + 1 (L1:31). Harmless (any fixed polylog
   exponent works since J_nħ_n → 0) but the exponent is inconsistent. *Fix:* "|S| ≤ (log n)^{κ′} for any fixed κ′".

5. **NIT — REPORT.md:140–141.** "Component-port runs in d = 2 show growth faster than log n" — four n values with
   extras/log n = 0.8 → 3.4 suggest, not show (L4:150 and D1_SUMMARY:37–40 say "suggest"/"do not prove"). *Fix:* "suggest".

6. **NIT — L5_assembly.md:15.** Hypothesis "(ii) (R1)–(R3) of Lemma NA-R hold for Q" omits that (R1)–(R3) are relative to
   a latent extension as in STATEMENT (B) (needed for LOC-BF). *Fix:* "(ii) for some latent extension as in Lemma NA-R,
   (R1)–(R3) hold for Q".

7. **NIT — L4_LOCd.md:111.** "|I_l| ≤ … =: L_n" reuses L_n, which in the same file's §A.5 (via NA-R) is the atom ℓ¹ bound.
   *Fix:* rename the reference count (e.g. N^ref_n).

8. **NIT — L4_LOCd.md:96, :156.** s₀ ≥ 1 is used implicitly (H_l, d_n, Q⁰ definitions follow GROW) but is stated only in
   L6:41. *Fix:* add "s₀ ≥ 1 (as in GROW)" to STATEMENT §1.

9. **NIT — L6_poly.md:293–295.** The extension of (P10) to "any fixed B_A" is asserted from the source's proof shape; it
   is not needed: all thresholds used (t_n(k) ≤ log(n+1) + 2 log p, and 2 log p + τ log n with τ < 1) lie in GROW
   L6.4's stated range [½ log n, (2A + 3) log n]. *Fix:* replace the B_A sentence by this observation.

10. **NIT — numerics/poly_check.py:155–158 / poly_out.txt.** The printed "rate envelope" is smaller than the printed error
    (e.g. 5.77 vs 3.70 at n = 1e8) because the assert is error ≤ 4·envelope; a reader may take it as a falsification.
    Also the decay at α = 9 is extremely slow (error ≈ 2 at n = 1e64), worth one sentence noting that only O(1) is used
    (L6:272–273 already says so). *Fix:* print "≤ 4×envelope" and the ratio.
