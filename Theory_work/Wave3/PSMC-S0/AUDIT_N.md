# AUDIT_N — T-N premise audit: fixed N per island (OD-1) and general (N, R′)

PSMC-S0 Part 1, Theory Department, 2026-11-15. Lead: Claude Opus 5.5 (high). Premise audit only: no proofs beyond
sketches, no statuses asserted. Code of record: `Scripts/SMC_BVS/core/` on this branch (cut from `origin/main`).

**Change audited (OD-1(b); ENGINEERING_SPEC §4.2 row "fixed N per island").** v3.1 sets
N₀ = max(2500, n, p), H₀ = ⌈512N₀/2500⌉, tier e ∈ {0,1}: (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀)
(`v3_preprocess.R:24-25, :28`; SoP `02_method.tex:152-156`). Production mode fixes N = 2,500 per island for every p
(H = 512, SPEC Note 2), with R′ = 16 islands (OD-9), fixed in the manifest before any final address is read
(SPEC §4.3). Class Δ.

## 0. Verdict (plain words)
- **Nothing that Engineering listed actually needs N ≥ p.** TH01(e)(f) and TH06 are stated with no N at all; TH01(i)
  depends on the number of islands R′, not on N. Only TH08 (work accounting) has N₀ = max(2500, n, p) as a written
  hypothesis, and it restates mechanically (its formulas are already in N_e).
- **RM-0, RM2, LT♯, C, TR, N1 and the finite-sample parts of D hold for any N ≥ 1** (file:line below). OD-1's
  statement "every headline selection and PIP theorem is stated for arbitrary N_e" is **confirmed**.
- **Two consumers Engineering's list misses**, both "production corollaries" that use N₀ ≥ max(n, p):
  (1) **W3-SAMP Theorem D (draw discovery), production corollary of (D-iii)/(D-iv)**: with N fixed, the sufficient
  condition becomes π₀(S₀)·log n → ∞ instead of max(n, p)·log n·π₀(S₀) → ∞, i.e. the draw-discovery route needs
  a start mass about max(n, p) times larger. This is a **WEAKER production corollary** of a headline-flagged claim
  (the theorem's finite-sample clauses are unchanged). The reported-model headline does not rest on it: RM-0/RM2
  reach S₀ through LS0, with no N.
  (2) **W2-APP Lemma ENUM (ii)** ("every fixed p is eventually enumerated", proof uses 4N₀p ≥ 4np): with N fixed the
  exact-branch threshold is (5·512 + 4·2500)p = 12,560p, so only p ≤ 17 is ever enumerated, whatever n. ENUM (i)
  is stated through the coded inequality and stays true.
- **OD-1's text "equals v3.1 exactly for p ≤ 2,500" is true only when also n ≤ 2,500** (N₀ = max(2500, n, p) = n
  when n > 2,500). Every asymptotic statement has n → ∞, so in the limit the old and new laws differ at every p.
  This changes no theorem, but the sentence should read "for n, p ≤ 2,500".
- **Open question for Engineering (through the manager):** under OD-2(c) a tier-0 grid-construction failure still
  escalates to tier 1, where v3.1 uses N₁ = 4N₀ (`v3_preprocess.R:28`, read at `v3_calib.R:185`). Is the escalated
  island size 10,000 or 2,500 in production? Neither choice affects any theorem (N_e is σ(𝓒)-measurable in every
  statement), but "fixed N" should say which.

## 1. Results that use N_e ≥ p, N₀ = max(2500, n, p) or "common N at N_e"

| # | claim@version (registry id) | where N enters (file:line) | what is used | holds for fixed N = 2,500 (and R′ = 16)? | effort |
|---|---|---|---|---|---|
| 1 | TH01(e) islandwise bound (`SOP:TH01.e`@1.0.0) | stmt `04_theory.tex:117` "(e) Islandwise, every regime and frozen grid: E[W_r·\|H_r(h) − h(S₀)\| \| 𝓒] ≤ 2δ₁"; proof `W1-N1/lemmas/E_corollary.md:15-16` | N enters only as the averaging constant (4N_e)⁻¹; no lower bound on N | **yes, unchanged** (any N_e ≥ 1, `W1-N1/STATEMENT.md:29-30`) | none |
| 2 | TH01(f) finite-R′ bound (`SOP:TH01.f`@1.0.0) | `04_theory.tex:117` "(f) Finite R′, M₂ = E[W_r² \| 𝓒] …" | R′ and M₂ only; N-free | **yes**. R′ = 16 = 4k with k = 4 is in the domain "R′ = 4k declared before stream 10" (`04_theory.tex:116`; `W1-N1/STATEMENT.md:30`). The bound 4(M₂−1)/R′ + 4M₂/(R′ε²) is informative at R′ = 16 only when M₂ is small (a statement about σ̂, not N) | none |
| 3 | TH01(i) asymptotic with R′_n (`SOP:TH01.i`@1.0.0) | `04_theory.tex:117` (i) with R′_n = 4⌈log₂(n+p+1)⌉; chair's note "ℓ, L and N need no edit" `04_theory.tex:111` | stacking R′_n → ∞ at unchanged N_e; N-free | **N: yes.** **R′: no** — production R′ = 16 is fixed, while (i) needs R′_n → ∞ (at n = 200, p = 10⁶, R′_n = 80). So (i) does not describe the production configuration. Not needed for the headline: LT♯/C/TR give PIP/MPM consistency at fixed R′ (W3-SAMP) | candidate T-N-1 (restate (i) for any R′_n → ∞, or label it "stacking configuration only"): 0.5 h |
| 4 | TH06 SEP + Lemma KL (`SOP:TH06`, `.a`, `.b`, `.c`, `.KL`@1.0.0) | `04_theory.tex:558-561` "Comparison experiment: Q ≥ 1 exact iid draws from π₀ … No production-grid, mutation, LS0 or delivery premise enters" | the number Q of iid start draws; N does not appear | **yes, unchanged.** Interpretation only: the method's own draw count per island falls from Θ(max(n,p)·log n) to Θ(log n), i.e. further below the LH scale Q*_n = p²n | none (one remark sentence in the chapter: 0.25 h) |
| 5 | TH08 Prop D (`SOP:TH08`, `.a`–`.e`@1.0.0) | hypotheses `04_theory.tex:714` "the shipped budgets N₀ = max{2,500, n, p}, H₀ = ⌈512N₀/2,500⌉, … R′ = 4k declared"; (b) "I_e ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation)" | N₀, H₀ as written hypotheses; formulas (a)–(c) are in (N_e, H_e, I_e) | **(a)–(c) as formulas: yes** with N_e := N, H_e := H. **(d)** polynomial work: yes, a fortiori (every term is nondecreasing in N, H). **Rebuild count:** under OD-2(c) I_e ≤ I_max (see AUDIT_CAL). **Depth clauses** are island-level v3.1 ("K88's particle-parallel critical path is v3.2 and not claimed", `04_theory.tex:731`): they do not describe the threaded production engine | candidate T-N-2 (restate TH08 for general (N, H, I_max, R′), work clauses only; production depth = Engineering's measured accounting, not a theorem): 1 h |
| 6 | W3-SAMP Theorem D (`W3-SAMP:D`@2.1.1, headline flag; notes "Production corollary: D_r ≥ max(2500,n,p)(L+6)") | `W3-SAMP/STATEMENT.md:102-105` (D-iii) "production corollary: D_r ≥ max(2500, n, p)·(L + 6)", (D-iv) "production corollary: P-OVL may be replaced by max(n, p)·log₂(n+1)·π₀(S₀) → ∞"; proof `W3-SAMP/lemmas/D_theorem.md:53` | N_e ≥ N₀ = max(2500, n, p) | **(D-i)–(D-iv) themselves: yes** (stated for D_r = N_e(1 + T + L + 4), any N_e, `STATEMENT.md:82, :97-105`). **Production corollaries: no — WEAKER.** With N = 2,500: D_r ≥ 2500(L + 6), and P-OVL holds if log₂(n+1)·π₀(S₀) → ∞ (exponent R′·D_r = 16·D_r under IND-T in D-ii/D-iii). The old corollary needed π₀(S₀) ≫ 1/(max(n,p) log n); the new one π₀(S₀) ≫ 1/log n | candidate T-N-3 (restate both corollaries for general (N, R′); one line each, plus the R′ = 16 exponent): 1 h |
| 7 | W2-APP Lemma ENUM (`W2-APP:ENUM`@1.0.0) | `W2-APP/lemmas/L6_ENUM.md:9` (EXB) with N₀ = max(2500, n, p); proof (ii) `:23` "(5H₀ + 4N₀)p ≥ 4N₀p ≥ 4np"; `W2-APP/STATEMENT.md:99-102` | N₀ ≥ n | **(i) yes** (stated via the coded inequality). **(ii) no** for fixed N: (EXB) becomes Σ_{k≤K}C(p,k) ≤ 12,560p, n-free; enumeration only for p ≤ 17 | candidate T-N-4 (restate (ii): "2^{p} ≤ 4Np"; under fixed N this is p ≤ 17): 0.25 h |
| 8 | C-DLV Lemma R / Cor R (`C-DLV:L1-R`, `C-DLV:Cor-R`@1.0.0) | `C-DLV/lemmas/L1_resources.md:9-10, :29, :47-53, :73, :115` (N₀, H₀, N̄ = 4N₀, exact-branch (5H₀+4N₀)p) | polynomial resource envelopes in (N₀, H₀) | **yes, a fortiori** (envelopes are nondecreasing in N₀, H₀; fixed N lowers them). The proof is a v3.1 code count; the production binary needs its own inventory (AUDIT_CAL §2) | none for T-N |
| 9 | Remarks citing the exact-branch scale: W1-GEN L7 (`W1-GEN/lemmas/L7_counterexample.md:87` "threshold (5H₀ + 4N₀)p is O(n²) … so LS0 is actually executed"), C-GROW L5 (`C-GROW/lemmas/L5_instances.md:122` "for p = 100 this happens at n ≳ 2.5·10²⁷"), W1-PXN (`W1-PXN/lemmas/R_branch_repair.md:30`) | as quoted | exact branch reached / not reached | **yes**: with N fixed the exact branch is rarer, so "LS0 is executed" holds a fortiori; C-GROW's remark becomes "never, for p = 100"; W1-PXN's branch repair still covers the (smaller) exact range | none (remark wording only) |
| 10 | Method text and limitation rows (SoP, not claims): `02_method.tex:152-156` (budget table), `:167-169` ("Because the threshold grows with N₀ ≥ n, every fixed-p problem is eventually enumerated"), `:628`, `:635` (settings rows 14, 21), `:672` and `04b_supplement.tex:1144` ("N₀ ≥ p … impose real computational growth"), `A_notation.tex:94, :193` | settings description of v3.1 | — | true of v3.1; for the large-p method they must be re-described (N = 2,500, H = 512; exact branch p ≤ 17; the "N₀ ≥ p" growth row disappears) | writing item for the chapter, not a theory ticket |
| 11 | "Common N at N_e" (stacking): DF12, MD05 (`02_method.tex:374-377` "R′ = 4k, at unchanged N_e … N_e is never split"; `method.tsv:6, :26`) | island count and size | all islands share one N | **yes**: production uses 16 islands of the same N = 2,500, R′ = 16 = 4·4 fixed before final randomness. Islands-as-processes, merge and new streams are T-MERGE / T-STREAM (OD-12 items 2–3), not T-N | none for T-N |

Exact-identity clauses that carry N_e but need no lower bound (checked, no row needed): TH02(b3) "1 + N_e Var(…) =
1 + χ²(q_{φ₁}‖π₀) exactly" (`theory_main.tsv:24`); TH08(a) formulas; W1-N1 accumulator (4N_e)⁻¹
(`W1-N1/STATEMENT.md:51`). Not relevant despite the symbol: "N₀" in W2-FAC-B/S5/X is the set of nulls sharing a block
with S₀ (`W2-FAC-X/STATEMENT.md:40-41`), and "N := n − 1" in `W3-START/lemmas/L11_EXAMPLES.md:10`.

## 2. Confirmations: results stated for arbitrary N (file:line)

| claim@version | quoted scope | file:line |
|---|---|---|
| `W1-N1:Thm-N1`@1.0.0 (N1) | "Parameter domains: N_e ≥ 1 and L ≥ 0 integers; R′ = 4k … all σ(𝓒)-measurable and frozen before stream 10" | `Theory_work/Wave1/W1-N1/STATEMENT.md:29-30` |
| `W3-SAMP:LT#`@2.0.1, `:C`@1.1.1, `:TR`@2.1.1, finite parts of `:D`@2.1.1 | "§2's Lemma ST and the finite-sample parts of Theorems D, LT♯, C and TR hold for **any** frozen parameters … integers N_e ≥ 1 and L ≥ 0" | `Theory_work/Wave3/W3-SAMP/STATEMENT.md:43-50` |
| `W3-SAMP:C`@1.1.1 | "any frozen parameters (any valid grid, any T ≥ 1, any N_e ≥ 1, any L ≥ 0)" | `W3-SAMP/STATEMENT.md:149-150` |
| `W3-SAMP:TR`@2.1.1 | "with no condition on Ẑ, the bridge, N_e or the grid" | `W3-SAMP/STATEMENT.md:171` |
| `W3-SAMP:LT#`@2.0.1 | (LT-e) "with no condition on 𝓒 beyond 𝒜"; registry conclusion "any N_e and frozen schedule" | `W3-SAMP/STATEMENT.md:136-138` |
| `W3-RM:RM-0`@1.0.0 | "(b) … pathwise, for every seed, N_e, R′ and calibration outcome … CAL is not used for (b)" | `Theory_work/Wave3/W3-RM/STATEMENT.md:168-175` |
| `W3-RM2:RM2-F`@1.0.0 (headline selection) | "every admissible output run — every seed, N_e, R′ and calibration outcome — reports Ŝ⁺ = S₀" | `Theory_work/Wave3/W3-RM2/STATEMENT.md:208-209` |
| `SOP:TH01.a–.c`@1.0.0 | "(c) Contract: (a),(b) hold conditionally on any successful frozen 𝓒; any R′ declared before stream 10 keeps them" | `State_of_Project/sections/04_theory.tex:117` |
| W3-POST, W3-POST2, W3-MISR, W3-SCR | posterior-only or "every seed / every completed run" statements; no sampler budget enters | scope column of `claims.tsv` (e.g. `W3-SCR:SCR-G` "every completed run") |
| DIST | no DIST claim is registered yet (W3-DIST is in progress; not read beyond a grep, not touched). DIST-C names the 40p + 1 top store, not N | — |

Caveat carried to T-MERGE (not T-N): W3-SAMP fixes R′ = 4 in its setting (`STATEMENT.md:42`; pip_primary := ¼Σ_r,
LT-d sums over r ≤ 4). The per-island statements are R′-free; the pooled clauses generalise by replacing 4 with R′
(union bounds grow linearly in R′), plus the merge rule of OD-4. That restatement belongs with T-MERGE (O1, O21).

## 3. Candidate T-N restatements (general (N, R′)), with effort

| id | restatement (sketch) | change tag vs parent | effort |
|---|---|---|---|
| T-N-1 | TH01(i): "for any declared R′_n → ∞ with N_e arbitrary" (the proof uses only R′_n → ∞ and M₂ = O_P(1) for a fixed finite declared list; the (n+p)⁶ variant keeps its count for the simultaneous list), or label (i) "stacking configuration only; not the production R′ = 16" | EQUAL in N; scope note on R′ | 0.5 h |
| T-N-2 | TH08: hypotheses "N, H fixed per island (production: 2,500, 512), R′ declared, I ≤ I_max rebuilds per tier"; (a)–(c) unchanged as formulas; (d) unchanged; depth clauses restricted to the island-serial engine | EQUAL (formulas) / scope narrowed on depth | 1 h |
| T-N-3 | W3-SAMP D production corollaries: "D_r ≥ N(L + 6); under IND-T exponent R′·D_r; P-OVL implied by N·(L + 6)·π₀(S₀) → ∞, i.e. π₀(S₀)·log n → ∞ for fixed N" | **WEAKER** (production corollary only; main clauses EQUAL) — needs the headline route (HQ + consultant, PROTOCOL_v4 H5) only if D's production corollary is on a headline card | 1 h |
| T-N-4 | W2-APP ENUM (ii): "(EXB) holds whenever 2^{p} ≤ 4Np; with N = 2,500 fixed, for p ≤ 17" | WEAKER (sufficient condition (ii) only) | 0.25 h |

Total ≈ 3 h, one Tier B rider (no new key lemma). None of these blocks OD-1.
