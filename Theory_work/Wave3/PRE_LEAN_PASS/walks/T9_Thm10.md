# T9 — full proof walk: Theorem 10 (card row 3.6; masters `W3-SAMP:C@1.1.6`, `TR@2.1.6`, `LT#@2.0.6`, `D@2.1.6`; assembly `W3-READER:R4@1.0.3`)

Walker: Fable-CT-B (Fable 5.2, Claude Third), 2026-11-18. Brief: `Theory_work/Dept/briefs/PRE_LEAN_WALK_BRIEF.md` (origin/dept/theory).
Sources read at origin/main `668b413f`. Read-only; no theory file edited.
Abbreviations: RDR = `Theory_work/Wave3/W3-READER/READER_VERSIONS.md`; SAMP = `Theory_work/Wave3/W3-SAMP/`;
START2R = `Theory_work/Wave3/W3-START2-R/STATEMENT.md`; APP = `Theory_work/Wave2/W2-APP/`.

## Findings

| # | severity | file:line | claim | why |
|---|---|---|---|---|
| H1 | MINOR (status record, not mathematics) | `Theory_work/INFRA/registry/claims.tsv` rows `SOP:TH110`, `W3-SAMP:MR`; SAMP `lemmas/MR_identities.md:5-19`; CLAIMS_CARD:77 | Row 3.6 is presented as "clean", masters "PROVED-CHECKED" with no condition | Lemma MR — and through it LT♯, C, TR and R4 — consumes T12 (i.a), (i.b), (i.c), (ii), the round path law (R3) and the T12 freezing lemma. T12's registry row `SOP:TH110@1.0.0` reads "PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted …", not PROVED-CHECKED. For `SOP:TH09` the same label was treated as below PROVED-CHECKED and carried as an explicit condition (RM2 `STATEMENT.md:297-300`) until it was discharged. By that rule row 3.6 would read "conditional on SOP:TH110" unless T12's own review record is accepted as equivalent; I found no line that says so. The mathematics I walked does not depend on this; the label on the card does. For the manager to rule on. |
| H2 | NOTE (Lean) | `Theory_work/Wave3/ERRATA_W3-SAMP.md` E1; `Theory_work/Wave3/W3-AUDIT/track_A/T5_CAL/STATEMENT.md:42-54`; RDR:1300-1316, 1320-1322; `W3-READER/lemmas/R4_printed_outputs.md` | 𝒜 := "the sampler branch is taken and calibration succeeds"; conditional steps "given 𝓒 on 𝒜" | By erratum E1 the conditional identities of SAMP hold for the potential pair (𝒜°, 𝓒°) of the uninterrupted run, not for the actual pair (the actual 𝒜 depends on the clock). Theorem 10's conclusions are intersections and indicator-multiplied O_P statements about potential records, so they transfer to the actual 𝒜 ⊆ 𝒜° (CAL-d and the transfer rules). Neither R4 nor the reader's master list cites E1 or `W3-AUDIT-A:CAL-C`; (S5) covers it by convention ("the calibration record is a function of the data and the calibration streams"). A Lean statement must define 𝒜 as 𝒜°. The remark on row 3.5 in the same section ("given the calibration, on 𝒜, E[Ẑ \| calibration] = Z") is a conditional identity and is true only in the potential reading. (E1's recorded date, 2026-11-23, is later than today.) |
| H3 | NOTE (Lean) | SAMP `STATEMENT.md:62-70`; RDR:61-71 | The N1 premises (S5): EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT | These idealise the code (exact arithmetic, ideal uniforms, exact π₀ draws, exact kernels, measurability of the record). They are premises, with code-reading support (CC1–CC7, W3-AUDIT-A:KER, START-X, AW:ISL, AW:FRZ). In Lean they are the definition of the abstract algorithm; the identities MR-a/b/c for that abstract algorithm are then the main formalisation object of this row. Everything above MR (ST, LT♯ Steps 1–2′, C Steps 4–6, TR, R4) is finite-state Markov chain algebra and Markov's inequality. |

(No FATAL, no MAJOR.)

---

## Chain

    reader Thm 10 (RDR:1287-1316)
      └─ bridges B10.1–B10.3 (RDR:1343-1349); R4 (W3-READER/lemmas/R4_printed_outputs.md)          §1
          ├─ posterior input: W2-APP:POST@1.0.7 (recorded) through R1 B2.1                           §1
          ├─ start input: W3-START2-R:IF-START@1.0.0 under (T3⁺⁺)(b), Q = S₀ (recorded)              §1
          └─ Theorem C (C-v) (SAMP STATEMENT:149-163; lemmas/C_theorem.md)                           §2
              ├─ (C-iii) T-free evidence bound ⇐ MR-a                                               §2
              ├─ (C-iv) PIPs, MPM, discovery ⇐ LT♯ Steps 1, 2, 2′, 4; ST; MR-b, MR-c; D-i; CC        §3
              ├─ Lemma MR (lemmas/MR_identities.md) ⇐ T12, W1-N1 (recorded)                         §4
              ├─ Lemma PC, Theorem D §3 (reported fields, reported HPM)                              §5
              └─ alternative route (remark): Theorem TR                                              §6

## 1. Reader statement → R4 → (C-v)

Reader hypotheses: preamble (Gaussian rows, correlation matrix Σ_n, y^r = α1 + Xθ* + ε, θ* deterministic); (A1) (S1),
(S2), (S3), (S5), p > s₀; (A2); (A3) floor on |S| ≤ 5(A + 1)(s₀ + 1) log n; (A4), (A5) = Theorem 5's (A4), (A5) (RDR:581-588).
R4's hypotheses: Setting R (standardised-signal convention), s₀ < p ≤ n^A, the same floor, (V-R), (L-R⁺⁺) with Q = S₀,
the N1 premises.

| R4 / master hypothesis | supplied by | check |
|---|---|---|
| Setting R, s₀ < p ≤ n^A | preamble, (A1), (A2), (S2) | identical. |
| LSF (for POST): floors on \|S\| ≤ k̄_n | (A3), bridge B2.1 | recomputed in `T6.md` §A0: k̄_n ≤ 5(A + 1)(s₀ + 1) log n for n ≥ 3. ✓ |
| (FL-R16): floor on \|S\| ≤ 16 + s₀ | (A3), bridge B6.1 | 16 + s₀ ≤ 5(A + 1)(s₀ + 1) log n for n ≥ 3. ✓ |
| (V-R) | (A4) | identical (PTV(a)). |
| (L-R⁺⁺) with Q = S₀ (START2R:70-81): H_l ⊇ {l} ∪ S₀, \|H_l\| ≤ H̄_n, log H̄_n ≤ κ_H√log n; leak ≤ C_L n^{−1/2} at U₀; localisation ≤ r_n, r_n(n log n)^{1/4} → 0 | (A5) | identical with H̄_n = e^{κ√log n}, C_L = C. \|Q\| = s₀ ≤ K eventually. The reader does not say "deterministic" for H_l; it is a population object and nothing random can enter. ✓ |
| N1 premises | (S5) | identity by reference (RDR:61-71; SAMP STATEMENT:62-70). H3. |

R4's proof, step by step:
1. δ := 1 − π(S₀) = O_P(√(log n/n)) by POST (b) (APP `lemmas/L1_POST.md:30-33`; p ≥ 2 by (S2)); on {δ ≤ ½}, o₁ = δ/(1 − δ) ≤ 2δ,
   and P(δ ≤ ½) → 1, so o₁ = O_P(√(log n/n)). ✓
2. IF-START⁺⁺ (START2R:241-246) under (T3⁺⁺)(b) with Q = S₀: 1_𝒜 o₀ = O_P(n^{−1/2}e^{C_R√log n}) **for every event 𝒜**. Recorded;
   the walk stops there. (Its source clause (T3⁺⁺)(b)(i) gives 1 − π₀(S₀) ≤ (s₀ + 1)n^{−1/2}e^{C_R√log n} with probability → 1;
   o₀ ≤ 2δ₀ on {δ₀ ≤ ½}.) ✓
3. √(log n/n) ≤ ρ_n eventually, so 1_𝒜 δ̄ ≤ max(o₁, 1_𝒜 o₀) = O_P(ρ_n). ✓
4. (C-v) with r_n := ρ_n (deterministic, eventually decreasing to 0). ✓

Conclusions. Reader: 1_𝒜(|Ẑ/Z − 1| + |log Ẑ − log Z| + max_j|PIP̂_j − 1{j ∈ S₀}|) = O_P(ρ_n); P(𝒜 ∩ {MPM̂ ≠ S₀}) → 0;
P(completed and Ŝ ≠ S₀) → 0; the same rate for the printed fields times 1{completed}. (C-v) gives each of the three
errors as O_P(r_n) localised to 𝒜 (a finite sum of O_P terms is O_P), the two probability limits, and — through Lemma PC —
the printed fields on {completed} ⊆ 𝒜. Nothing in the reader's conclusion goes beyond (C-v). ✓
Law: joint law of design, noise and the method's random numbers; final streams independent of data and calibration
streams ((S5); SAMP STATEMENT:35-36). Events: intersections with 𝒜 or with completion; no conditioning; no claim on P(𝒜). ✓
The reading of 𝒜: H2.

**Verdict 1: no flaw. H2 (NOTE).**

## 2. Theorem C: (C-iii) and (C-v) (SAMP `lemmas/C_theorem.md:32-78`)

**(C-iii), re-derived.** a := d − d(S₀); V_t := Ẑ_{r,t}/(Z₀e^{φ_t d(S₀)}), V₀ = 1.
* (1) V_t = V_{t−1}·q̂_{t−1}(e^{Δ_t a}) from Ẑ_{r,t} = Ẑ_{r,t−1}q̂_{t−1}(e^{Δ_t d}). ✓
* (2) rescaled MR-a: E[V_{t−1}q̂_{t−1}(f)] = Σ_S π₀(S)e^{φ_{t−1}a(S)}f(S), for bounded f that may depend on the grid. ✓
  (Z_{t−1}q_{t−1}(f) = m(∅)Σγ₀e^{φ_{t−1}d}f; divide by m(∅)Z̄₀e^{φ_{t−1}d(S₀)}.)
* (3) (V_{t−1} − V_t)⁺ ≤ V_{t−1}q̂_{t−1}((1 − e^{Δ_t a})⁺) (convexity of x ↦ (1 − x)⁺); expectation
  Σ_{a<0}π₀(e^{φ_{t−1}a} − e^{φ_t a}); the sum over t telescopes to b₋ = Σπ₀(1 − e^a)⁺. ✓
* (4) c := Σπ₀e^a = π₀(S₀)/π(S₀) (from π(S₀)/π₀(S₀) = e^{d(S₀)}Z̄₀/Z̄₁); W = V_T/c; E V_T = c (E W = 1); c − 1 = b₊ − b₋;
  E|W − 1| = 2E(1 − W)⁺ = (2/c)E(c − V_T)⁺ ≤ (2/c)(b₋ + (c − 1)⁺) = 2max(b₋, b₊)/c = β. ✓
* (5) b₋ ≤ δ₀, b₊ ≤ c − π₀(S₀) = cδ, δ₀/c = (1 − δ)o₀: β ≤ 2max{δ, (1 − δ)o₀} ≤ 2δ̄. ✓ No dependence on T, N_e or the grid.
* Pooled: Ẑ/Z = ¼Σ_r W_r, so E|Ẑ/Z − 1| ≤ β. Log tail: {|log x| > u} ⊆ {|x − 1| > 1 − e^{−u}}; Markov. ✓

**(C-v).** Integrate the conditional bounds truncated at 1: P(𝒜 ∩ {|Ẑ/Z − 1| > ε}) ≤ E[1_𝒜 min(1, 2δ̄/ε)] → 0 (bounded
convergence, 1_𝒜δ̄ → 0 in probability); likewise the log tail, the PIP error (22δ̄), the MPM (44δ̄). Rate: if
1_𝒜δ̄ = O_P(r_n), then for each of the three errors P(𝒜 ∩ {error > Mr_n}) ≤ P(1_𝒜δ̄ > Kr_n) + CK/M, which is small for K
then M large (for the log error use 1 − e^{−u} ≥ u/2 on u ≤ 1). ✓ These are probability rates, not L¹ rates, as the file says.

Hypotheses used: EX-A, H-U, START, KERNEL, CAL, SI, MEAS, POT through MR-a and E W = 1; nothing about the design.
Constants: 2, 22, 44 (absolute); B ≤ 16 enters 22 and 44 through λ₀ ≤ 19o₁.

**Verdict 2: no finding.**

## 3. (C-iv): PIPs, MPM, discovery (C_theorem Step 5; `lemmas/LT_theorem.md` Steps 1, 2, 2′, 4; `lemmas/ST_stay.md`)

* ST-a: πK = π ⇒ π(S₀)K(S₀, Ω∖S₀) = Σ_{S≠S₀}π(S)K(S, S₀) ≤ π(Ω∖S₀): leave probability ≤ o₁. ✓
* ST-b: the Gibbs-j step leaves S₀ with probability |o_j(S₀) − 1{j ∈ S₀}| ≤ π(S₀ ⊕ j)/π(S₀); the models S₀ ⊕ j are distinct, so
  the sum over j is ≤ o₁; κ₀ ≤ o₁. ✓
* ST-c: first-exit decomposition over the m = p + B + 2 labels of a round, each used once: leave probability ≤ λ₀ ≤ (B + 3)o₁
  ≤ 19o₁ (B ≤ 16). ✓ No reversibility, any order law independent of the state.
* LT Step 1 (pathwise): |p̂_r(j) − 1{j ∈ S₀}| ≤ κ₀ + B̄ + Λ̄ for every j at once (the good/bad split of (round, particle) pairs
  does not depend on j — this is why no factor p appears). ✓
* LT Step 2: E[W·B̄ | 𝓒] = δ (MR-b, h = 1{S ≠ S₀}); E[Λ_q | H_q] ≤ λ₀(1 − B_q) (ST-c). Step 2′: W is H_q-measurable, so
  E[WΛ_q] ≤ λ₀E[W A_{r,q−1}] = λ₀(1 − δ); hence E[W·E_r] ≤ g := min{1, κ₀ + δ + (1 − δ)λ₀} ≤ 21o₁. ✓
* C Step 5: E E_r = E[W E_r] + E[(1 − W)E_r] ≤ g + E(1 − W)⁺ = g + β/2 ≤ 22δ̄ (E_r ∈ [0, 1], E W = 1). ✓
  Pooled: ‖pip_primary − 1_{S₀}‖_∞ ≤ ¼Σ_r E_r. MPM ≠ S₀ forces the pooled error ≥ ½ (strict threshold; tie at ½ covered),
  so P(MPM ≠ S₀ | 𝓒) ≤ 2g + β ≤ 44δ̄. ✓ No union over islands, no independence between islands.
* Discovery: the N_e initial draws are iid π₀ (D-i, START) and evaluated (CC1): P(S₀ ∉ 𝓜_r | 𝓒) ≤ (1 − π₀(S₀))^{N_e} ≤ δ₀ ≤ δ̄. ✓

**Verdict 3: no finding.**

## 4. Lemma MR (SAMP `lemmas/MR_identities.md`; `W3-SAMP:MR@1.1.3`)

For a fixed calibration value c the three identities are T12 (i.a), (i.b), (i.c)/(ii) applied to the coded island,
which is T12's abstract island I(c) by W1-N1 Lemma B; the RB clause uses that o_j(·) is the π-conditional probability of
j ∈ S given S ∖ {j}. Steps 2–4 (joint measurability of the integrand in (c, u); the deterministic bound on Ẑ_t; the
freezing lemma with 𝓒 ⊥ final stream) extend the fixed-c identities to "given 𝓒 on 𝒜" in localised form.
I checked the reduction (which T12 clause gives which identity, and that the functions h used downstream — 1{S ≠ S₀},
1{S = S₀}, (1 − e^{Δ_t a})⁺, o_j — are bounded and free of the final streams). I did not re-prove T12 or W1-N1 Lemma B/F:
they are the recorded inputs of this row (`SOP:TH110`, `W1-N1:Thm-N1`, `W1-N1:B`, `W1-N1:F`, with the line checks
`W3-AUDIT-AW:ISL`, `AW:FRZ`). Status of `SOP:TH110`: **H1**. Reading of (𝒜, 𝓒): **H2**.

**Verdict 4: reduction sound. H1 (MINOR, status), H2, H3 (NOTE).**

## 5. Reported fields and the reported model (SAMP `lemmas/PC_completed.md`; `lemmas/D_theorem.md` §3)

* PC (i)–(ii): on {completed} no island returned early, so each island's record is the potential record; `log_Z`,
  `pip_primary`, `mpm` are the functions of §0 of those records. I checked the assembly lines at main
  (`v3_run.R:150-154`: `log_Z` = log-mean-exp of the island values; `:159-163`: `pip_primary` = row mean, `mpm` = {> 0.5}):
  unchanged by the three list-field commits after the code of record (4676af6; R-only changes, no C++). ✓
* PC (iii) and D §3: Ŝ is the hpm_better-maximum of the ledger's offered set 𝓜 ⊆ Ω, 𝓜 ⊇ ∪_r 𝓜_r; if δ < ½ then S₀ is the
  strict F-maximiser on Ω, so S₀ ∈ 𝓜 ⇒ Ŝ = S₀. Hence
  P(completed ∩ {Ŝ ≠ S₀}) ≤ P(𝒜 ∩ {δ ≥ ½}) + E[1_𝒜 min(1, δ̄)] → 0. ✓

**Verdict 5: no finding.**

## 6. Alternative route (remark): Theorem TR (SAMP `lemmas/TR_theorem.md`; `W3-SAMP:TR@2.1.6`)

Not used by the reader statement; listed on the card. Walked:
* TR-a: the independence step has K_I(x, y) = min{π₀(y), π(y)/w(x)} ≥ π(y)/M with M = max π/π₀; a round containing it is
  minorised by M⁻¹π because every other step is π-invariant; Doeblin gives ‖K₁^L(x, ·) − π‖_TV ≤ (1 − 1/M)^L. ✓
* TR-b/c: per-particle chain from the end of the bridge; stationary badness ≤ δ + (1 − δ)λ₀; burn-in error e_L; concavity of
  min{1, ·}. ✓ TR-d: 1_𝒜 e_L ≤ e^{−L/M} → 0 under P-OVL∞. ✓ P-OVL∞ is not supplied by Theorem 10's hypotheses, and the
  reader does not claim it.

**Verdict 6: no finding.**

---

WALK COMPLETE (T9: Theorem 10), down to the recorded inputs `W2-APP:POST`, `W3-START2-R:IF-START`/`START-R`, `SOP:TH110` (T12),
`W1-N1:Thm-N1`/`B`/`F`, `W3-SAMP:CC`. Findings: 0 FATAL, 0 MAJOR, 1 MINOR (H1, a status-record question), 2 NOTE (H2, H3).
