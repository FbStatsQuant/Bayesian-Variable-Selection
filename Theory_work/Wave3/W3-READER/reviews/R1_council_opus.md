# W3-READER — CP3 council, round R1, seat `opus` (blind first read)

Reviewer: Claude Opus 5.5 (effort high). Content reviewed: `MANIFEST 759a7dfd87ef7b958a0c8140b6cfa0158f4159cac31c62cf3cb0f1a75fdd7e09`.

**Freeze check.** `python3 Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-READER Theory_work/Wave3/W3-READER/reviews/MANIFEST_R1.txt`
→ `verify: OK MANIFEST 759a7dfd87ef7b958a0c8140b6cfa0158f4159cac31c62cf3cb0f1a75fdd7e09`.

**What I read.** Under review: `READER_VERSIONS.md` (all 1379 lines), `NOTATION.md`, `CLAIMS_CARD.md`, `STATEMENT.md`,
`lemmas/R1`–`R4`, `REPORT.md`, `METHOD_INTUITION.md`. Masters/sources: W1-N1 STATEMENT §2–§3; W3-SAMP STATEMENT §0–§3;
W3-POST STATEMENT §0–§2; W3-POST2 STATEMENT :1-140; W3-PSHARP STATEMENT :44-114; W3-PSHARP-R STATEMENT :25-100;
W3-MISR STATEMENT :36-66, :106-175; W3-MISR-R STATEMENT :25-160; W3-START2-R STATEMENT :60-90, :215-250; W3-START
STATEMENT :155-165, :238-245; W3-RM STATEMENT :125-160; W3-RM2 STATEMENT :120-290 and `lemmas/L6_examples.md:110-160`;
W3-RM2-R STATEMENT :36-185; W3-SCR STATEMENT :12-95, :150-165, :212-220; W3-DIST STATEMENT :126-240; W2-UNI
`lemmas/L5_delivery.md:1-45`; `assumptions.tsv` row `A:IDEAL-W+`; `claims.tsv` (status/version/state of ~60 ids);
code `v3_run.R:85-200`, `v3_fit.R:73,118,151`, `v3_calib.R:115-190`, `cpp/v3_core.cpp:465-480, 715-736`, `cpp/v3_ledger.h`.
Not read (as instructed): `GATES.md`, `gates_staged.tsv`, `TRIAGE_SHARP3.md`, `CARD_ROW11_R03b.md`, `SHARP3_REQUEST.md`,
`helpers/`, `api/`, `deltas/`, `tools/` (except running `manifest.py`), `BRIEF*.md`, `LOG.md`, `CHECKPOINT_*.md`, and
everything in `reviews/` except `MANIFEST_R1.txt`.

**Checks run** (scratch: `reviews/R1_scratch_opus/`). `r1_check.py`: grid A ∈ {1,…,20} (non-integer included),
s₀ ≤ 39, n ∈ [3, e^35], p = n^A, with the exact ceilings and log C(p,s₀) (summed logs; a first lgamma version gave
false alarms from floating-point cancellation at p ~ 10¹⁶, fixed). B1.2, B1.3, B2.1, B4.1, B6.1: **0 violations**.
B2.1's sharper bound s₀ + m̄_n ≤ d(As₀ + 1.5s₀ + 2) log n holds (worst ratio 0.99999). The toy example could not be re-run
(no numpy in the sandbox). Its table in `METHOD_INTUITION.md:131-137` matches the recorded `numerics/toy_example_out.txt`.

---

## Per-claim decisions

| id | decision |
|---|---|
| `W3-READER:PoolZ` | ACCEPT |
| `W3-READER:R1` | ACCEPT |
| `W3-READER:R2` | ACCEPT |
| `W3-READER:R3` | ACCEPT |
| `W3-READER:R4` | ACCEPT |
| `RV/thm1` (Theorems 1, 1′; row 1.1, Form A) | REJECT (finding S3 only; the theorem displays are faithful) |
| `RV/thm2` | ACCEPT |
| `RV/thm3` | ACCEPT |
| `RV/thm4` | ACCEPT |
| `RV/thm5` | REJECT (finding S5, card row 3.3 only; the reader statement is faithful) |
| `RV/thm6` | ACCEPT |
| `RV/thm7` | REJECT (finding S6 only; the statement and Remark (a) are faithful) |
| `RV/thm8` (Theorems 8, 8′; row 3.7 form (a)) | REJECT (finding S4, card row 3.7 "Buys" column only; both statements are faithful) |
| `RV/thm9` | ACCEPT |
| `RV/thm10` (and remark row 3.5) | REJECT (findings S1, S2 in card rows 3.6 / 3.5; the reader statement and R4 are faithful) |

Every REJECT is caused by one interpretive sentence that needs a one-line correction. None is caused by a theorem
statement, a bridge or a status. After the corrections below, I would ACCEPT every row.

---

## Re-derivations (G1, G2)

**PoolZ** (`STATEMENT.md:12-37`). W1-N1 :98-104 gives, for each fixed r, E[W_r | 𝓒] = 1 a.s. on 𝒜 ∩ {r ≤ R′},
in the localised form of :94-96. On 𝒜, R′ = 4 (`W3-SAMP/STATEMENT.md:42`). Taking a finite union of null sets and using
linearity gives E[Ẑ/Z | 𝓒] = 1. Z is constant given the data. The joint-law form follows by the tower property for the
non-negative Ẑ under the H-U/SI idealisation of SAMP :35-36, which the proof states. Code: `v3_run.R:91` (`islands = 4L`),
`:154` (`log_sum_exp(logZr) - log(R)`). Correct. Remark (i): N1 uses no cross-island independence (N1 :80-82). Correct.

**R1.** B1.1: ‖Xθ*‖ ≤ Σ|θ_j|‖x_j‖ ≤ s θ̄ √(n−1). B1.2: ⌈x⌉ ≤ x + 1. B1.3: log C(p,s) ≤ Ast, then
s + m♯ ≤ 2s + 1 + ℓ₂(As + s/2 + 1)t. The final difference 1.55As + 3A + 0.275s + 0.55 > 0 is correct. B2.1: the identity
(1 + d log 2)/log 3 = d is exact, since log 1.5 + log 2 = log 3. Both differences are correct. B4.1 and B6.1
(10.986s + 10.986 > s + 16) are correct. B3.2: centring and scaling an i.i.d. Gaussian column gives a uniform direction
on S(1^⊥), independently across columns, and the two log conditions follow from p ≤ n^A. All verified numerically (above).

**R2.1.** e_T ⊥ W_T gives v_A = v_T + d_Tᵀ Σ_TT d_T. A unit diagonal plus PSD gives |Σ_ik| ≤ 1, so the quadratic form is
at most ‖d‖₁². By the Schur complement and Cauchy interlacing, v_T = 1/(Σ⁻¹_{T∪l})_{ll} ≥ λ_min(Σ_{T∪l}) ≥ c, with
T ∪ {l} ⊆ Q ∪ {l}. Correct. It meets (D-loc)'s variance clause (`W3-RM/STATEMENT.md:154-156`) with η_n = L_n²/c. The
other (D-loc) items (deterministic N_l ⊆ Q∖{l}, |N_l| ≤ ν_n = o(log n), ℓ¹ bound for every lattice T ∌ l,
L_n² log(|Q| + 1) = o(log n)) are stated verbatim in Theorem 6 (A6). **R2.2** is the same argument with ⟨·,·⟩/(n − 1). The
first inequality is in fact an equality, as the lemma says. Its conclusion is what `W3-RM2/STATEMENT.md:164` states.
Correct.

**R3** (history). The premise table matches F-UNI@2.1.0 `L5_delivery.md:8-21` item by item. (S) follows by a union bound
from [SAND(Q)], [NA(Q)], [TL(Q)]. (P) is E δ → 0, which is equivalent to δ → 0 in probability because 0 ≤ δ ≤ 1. The LS0
cap ℓ_n + |S̃₀| in F-UNI's method paragraph (:9) matches the code (`cpp/v3_core.cpp:473-474`). The narrowing to 𝔇 or
A:IDEAL-W⁺ is carried, and the operational premises go into (S4), not derived. The assembly is correct relative to its
master. It is honestly labelled as superseded for the shipped method (method drift, D74).

**R4.** Step 1: Theorem 2 via W2-APP:POST in the standardised-signal convention (W3-POST Cor-1R(a), :110-112), and
o₁ ≤ 2δ on {δ ≤ ½}. Step 2: (T3⁺⁺)(b) needs Setting R, p > s₀, (FL-R16) (from the floor via B6.1), (V-R) and (L-R⁺⁺) at
Q = S₀. IF-START⁺⁺ (`W3-START2-R/STATEMENT.md:241-243`) then gives 1_𝒜 o₀ = O_P(n^{−1/2}e^{C_R√log n}) for every event 𝒜.
Step 3: √(log n/n) ≤ ρ_n eventually. Step 4: ρ_n is eventually decreasing, because d/dn log ρ_n ∝ −½ + C/(2√log n) < 0.
(C-v) of `W3-SAMP/STATEMENT.md:158-162` applies. Correct. Every hypothesis used, including p > s₀, is in the claim (G2).

---

## Faithfulness, row by row (G3)

- **Thm 1** vs `W3-POST2:C` (i) (:85-91) and W3-POST (:66-75). (A4) gives (F_λ) and (F₀) via B1.2, (A5) gives (F_w) via
  B1.3, and (A3) gives (E) via B1.1. (A6) is BM(c) with c = C_β²φ₀², or BM-∞. "At that n" matches; n₀ and C depend on the
  same constants. The HPM = MPM bound 1 − 4C r_n follows from :91 (2Eδ each). **Thm 1′** vs `W3-POST2:E` + C(iii): (A4′)
  states (ID; c), which implies (ID^M; c), and (A5) gives (OS) via A0 for n ≥ n₀. Faithful. Remark (o): (DG) over a
  range ⊇ [1, m♯_n] is a stronger hypothesis than the master's. Faithful.
- **Thm 2** vs W3-POST item 6 + Cor-1R + W2-APP:POST. LSF holds via B2.1 (verified). Raw-scale b_lo, b_hi are covered.
  Faithful.
- **Thm 3** vs PSHARP:B (:92-99), PSHARP:A Cor A1 (:71-73), PSHARP-R AE / A1-E / A2-E(ii) / A2C (:61-100). (a) renames S₀
  to any S, which is allowed because B is deterministic and truth-free. In (b), (N-orth) ⇒ (W-orth-E) since p ≤ 2n, and
  (N-gauss) ⇒ (W-sph-E) via the random-(X_{S₀}, θ*) clause. The constant claims in "In words" check out:
  (s₀+1)·2(p−s₀)/(2p−1−s₀) ≥ 2 always and ≥ (s₀+1)/2 for s₀ ≤ p/2, and log(p√n/(s₀+1)) ≥ ½ log n. I re-derived B3.8
  myself: a fully orthogonal design gives (A1)–(A6) with A = 1, φ₀ = g₀ = 1 and the second form of (A6). Faithful.
- **Thm 4** vs MISR-R CorGb-plus (:96-108). B4.0 is correct: given X_𝒞, ε := y − α′1 − X_𝒞β^𝒞 ~ N(0, σ²_𝒞 I). This
  gives (N) with deterministic σ² = σ²_𝒞, and (OV) holds with q = 0. The floor comes via B4.1. (A3) is the → ∞ branch of
  the liminf condition. The Example is (E1)/(E2) of CorG-min (:81-86). The remark rests on CorH-plus (ii) (:126-128) and
  CorH-U (G) (:152-155). Faithful.
- **Thm 5** vs START2-R (T3⁺⁺)(b)(i),(iii), (L-R⁺⁺) :70-77, (L-gain-0) :82-86, FLOOR :241-243. Faithful (see E1 for the
  wording of the leakage form).
- **Thm 6** vs RM2-R-plus (:177-181) = RM2-R hypotheses (`W3-RM2/STATEMENT.md:172-202`) + RM0-plus (b⁺), (c⁺) + DLV-0.
  (A3) = (V-R); (A4) = (L-R^b) with (L-feas); (A5) = (FL-R) and (T1-R) via B6.1/B2.1; (A6) + (A5) ⇒ (D-loc^b) via R2.1,
  then (D-R^b) ⇒ (W-R) via D-to-W. (S4)(i)–(iv) restate (D) of :71-93, with IDEAL-W⁺ exactly as in `assumptions.tsv`.
  Remark (o) = (c⁺) with 𝓜_n = {S₀ unique maximiser of F} (:55). I checked the delivery-limit arithmetic: INT_MAX ≈
  2.147×10⁹, which forces n ≳ 4.29×10⁹ since |S̃₀| ≤ ⌊n/2⌋. Faithful.
- **Thm 7** vs RM2-F-plus (:166-175): (T1-F♭), (FL), (V♭) with M_V⁰ = (σ√(2A) + √((2A+1)C_R))², and (L^b) with
  b < β(η, A) = ½ − η/2 − √(2Aη); I checked that η < η_A ⇔ β > 0. (BM-W⁺) comes via B7.2′ (d_n² ≤ (2 + 4A) log n + O(1)
  under (A5)(a)) or (BM-Q♭). (W) comes via (W-χ) or (W-loc) ⇒ (W-ref) ⇒ (W-unif) (:159-168, :231-234). The bound
  |N_l| ≤ h log₂ n is ν_n log 2 ≤ h log n. Faithful (see E2 and S6).
- **Thm 8 / 8′** vs SCR A1 (:158-163), A-inf (:87-90), and definitions :49-75. Faithful, including the intersection
  event and the fixed-constant scope.
- **Thm 9 / 9B / 9C** vs DIST Thm-A/B, Cor-C (:136-238). Transcription with renaming. Faithful.
- **Thm 10** vs SAMP C (C-v) + IF-START⁺⁺ + Theorem 2 via R4. Faithful, including the localisation to 𝒜 (no
  conditioning) and the sampler-branch scope.

---

## Findings

### S1 — card row 3.6 asserts, without support, that AR and block designs meet Theorem 6's conditions (S, moderate)
`CLAIMS_CARD.md:70`: "Outside (A5), Theorem 6 (row 3.1, reported model) still applies under its own conditions, **which
AR and block designs meet**, …". `METHOD_INTUITION.md:122` makes the same claim in milder form ("not AR or block
designs; there, 6 for the reported model …").

The master's example classes do not support this sentence (`W3-RM2/STATEMENT.md:259-275`; `W3-RM2/lemmas/L6_examples.md:139-160`):
- **Block designs.** LOC-BF one-factor groups of size up to (log n)^κ are covered with "at most one truth per group",
  and "the lattice condition is supplied by latent-factor frames directly, **not by a claim that (D-loc) holds**"
  (L6 :152-160). Theorem 6's (A6) is exactly (D-loc^b), and an equicorrelated group larger than o(log n) has no
  o(log n)-size N_l with ℓ¹ error → 0.
- **AR/banded designs.** These are covered via UNI-0 with "the PTV/separation qualifications … retained" (L6 :149-151).
  That is, visibility (A3) depends on θ* and is not automatic. Their lattice condition is (D-R), not (D-loc^b). The
  polynomial-decay example is "example status unchecked" (Theorem 6 remark (iii); `W3-RM2:Ex-PolyR` "PROVED;
  line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat").

The reader statement (`READER_VERSIONS.md:1274-1277`) correctly says only "still applies under its own conditions".
**Correction:** in `CLAIMS_CARD.md:70`, replace ", which AR and block designs meet," with ". Its master covers
banded/AR and block-design example classes under their own visibility and separation qualifications (not as instances
of (A6))". In `METHOD_INTUITION.md:122`, replace "there, 6 for the reported model" with "there, Theorem 6 for the
reported model, under its own conditions".

### S2 — card row 3.5 calls the *printed* Ẑ unbiased (S, minor)
`CLAIMS_CARD.md:69`: "each island's evidence estimate, and hence the printed (equal-weight pooled) Ẑ, is unbiased for
Z". PoolZ and N1 concern the potential (uninterrupted) record on 𝒜. The printed field exists only on completed runs, and
N1 states "No statement conditional on completion is made (clause (c), CEX-guard)" (`W1-N1/STATEMENT.md:86-88`; PoolZ
remark (iii)). **Correction:** "… and hence their equal-weight mean Ẑ, computed from the four uninterrupted island
records (equal to the printed field on completed runs), is unbiased for Z; nothing is claimed conditional on
completion".

### S3 — Theorem 1: "on every design" the miss is ≳ n^{−1/2} (S, minor)
`READER_VERSIONS.md:148-149`, remark (vi): "on every design the posterior miss is at least of order n^{−1/2} (Theorem
3(a))". Also `:161-162`, (A2) line: "on *every* design the rate √(log n/n) forces s₀ = O(√log n), and π(S₀ | y) → 1
forces s₀ = o(√n) (Theorem 3)".

Theorem 3(a) and Corollary B hold only for s₀ ≤ min(K − 1, p/2) (`W3-PSHARP/STATEMENT.md:98`). Prop. LB needs
1 ≤ s₀ < p and s₀ + 1 ≤ K, and its registry row says "Can fail at p = s₀". Theorem 1 allows p = s₀ (for example
s₀ = p = 2). **Correction:** in (vi), write "on every design with s₀ ≤ min(K − 1, p/2) (Theorem 3(a); s₀ < p suffices
by Prop. LB)". In (A2), write "on every design with s₀ ≤ min(K − 1, p/2)".

### S4 — card row 3.7: "the only coded-method guarantee that needs no visibility, leakage, start or block condition" (S, minor)
`CLAIMS_CARD.md:71`, "Buys" column. Row 3.5 (PoolZ / N1: "no condition on the design") and Corollary 9C (row 2.1, the
sampler's returned list) are coded-method guarantees with none of these conditions. **Correction:** "the only
guarantee *about the reported model's support* that needs no visibility, leakage, start or block condition".

### S5 — card row 3.3 drops "with probability tending to one" (S, minor)
`CLAIMS_CARD.md:67`: "π₀ puts mass ≥ 1 − n^{−c} on S₀ for every c < ½; with a leakage set … mass ≥ 1 − n^{−c} on the
lattice of Q". As written this reads as a sure statement. The master (`W3-START2-R/STATEMENT.md:229-231`) and Theorem 5
(`READER_VERSIONS.md:585-601`) give it with probability → 1. **Correction:** insert "with probability tending to one"
after "puts mass" (both clauses). `METHOD_INTUITION.md:69-72` has the same omission (advisory).

### S6 — Theorem 7 honest limits (ii) overstate what Theorem 6 shows (S, minor)
`READER_VERSIONS.md:888-889`: "(ii) Theorem 6, which shows the same conditions hold with probability → 1 under
population analogues". RM2-R does not prove that Theorem 7's (A3)–(A5) hold w.p. → 1 on Gaussian designs. Its route
transfers floors, energy and (BM-W) (P8, `W3-RM2/STATEMENT.md:255`). It proves [SAND(Q)] directly from population
conditions (P7), and it takes (W-R) on the realised design as a hypothesis (:194-197). Sample visibility (V♭) and the
η-form leakage are never shown to hold. **Correction:** "(ii) Theorem 6, which gives the same conclusion under population
analogues of these conditions".

### Editorial (E) — not counted in the score
- **E1** `READER_VERSIONS.md:598`: "If (A5) holds with S₀ replaced by a deterministic Q ⊇ S₀". Read literally, this
  replaces S₀ inside H_l ⊇ {l} ∪ S₀ and j ∈ S₀∖U₀ as well. Then |Q| ≤ |H_l| ≤ e^{κ√log n}, which contradicts the next
  sentence's |Q| ≤ n^{1/2−ε}. The master (L-R⁺⁺) (:70-76) changes only "l ∉ Q". Write "(A5) with 'l ∉ S₀' replaced by
  'l ∉ Q' (H_l and the truths j unchanged), and |Q| ≤ K".
- **E2** `READER_VERSIONS.md:841-842`: Remark (a), "the clause of (A5)(b) holds as soon as (n−1)φ₀²θ*²_min/σ*² ≥ …", gives
  the master's (BM-Q♭), not the threshold for C_Q that (A5)(b) refers to. State it, e.g.
  C_Q > max{32, 64A + max(16, 8(A+1) + 4(2A+1)C_R/σ*²)}, which suffices for large n. Or reword as "(A5)(b)'s signal clause
  may be replaced by (BM-Q♭): …".
- **E3** `lemmas/R3_delivery_assembly.md:10-13, 34, 49-50` and `lemmas/R4_printed_outputs.md:105-106` still refer to
  "(S4)(i)–(iv)" with IDEAL-W⁺ as a separate "(S4)(v)". Since v0.8, IDEAL-W⁺ is inside (S4)(i) (`READER_VERSIONS.md:34-35`,
  :799). Update the references.
- **E4** `REPORT.md`: the R3 block says "1-54" but the file has 57 lines, and the R4 block says "1-49" but the file has 51.
  The R1 premises "(Thms 1, 2, 4, 6)" omit Thm 3 (B3.2) and Thm 10 (B2.1/B6.1 via R4); compare `STATEMENT.md:42`.
- **E5** `READER_VERSIONS.md:23-24` and `CLAIMS_CARD.md:28` give the status base as "base c04db8b". The statuses are now
  requoted at main 14892123. Update the base line.
- **E6** `READER_VERSIONS.md:300`: B2.1 row "(2.47As₀ + 3.7s₀ + 5.9) log n" vs R1's 4.9327. Both are valid; harmonise.
- **E7** `READER_VERSIONS.md:696-697`: remark (i) "On 𝒢_n the local search … only deletes …". This is proved on
  Sand ∩ NA ∩ TL (RM2-R-plus :171). The master's 𝒢⁺_n = 𝓜_n ∩ 𝒦_n is larger. Say "𝒢_n can be chosen
  (𝓜_n ∩ Sand_n(Q) ∩ NA ∩ TL) so that on it …".
- **E8** `READER_VERSIONS.md:890-891` (Thm 7 examples) paraphrases statuses ("checked, conditional on the posterior
  theorem"; "unchecked"). The registry has `W3-RM2:Ex-Proxy`/`Ex-Equi` "PROVED-CHECKED; council R1, …" (no condition) and
  `Ex-PolyF` "PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat …". Quote these verbatim. The
  paraphrase errs on the conservative side.
- **E9** `STATEMENT.md:21-22` (PoolZ): put "data fixed (probability over the final streams)" into the Claim line. Change
  "Equivalently" to "Consequently" for the joint-law form, which needs the extra H-U/SI idealisation used in the proof.
- **E10** `METHOD_INTUITION.md:102`: "(Theorem 8: certified small models contain S₀)" is the reading that Theorem 8's
  own honest limit rules out ("not a guarantee conditional on certification"). Write "(Theorem 8: the chance that a run
  certifies a small model missing a truth tends to zero)". At :78, the fallback ladder is "the last successful
  construction, else the pilot schedule", and only at tier 1 (`v3_calib.R:120-124`). The phrase "the run always
  proceeds" should say "unless the allocation preflight stops it".
- **E11** B3.8's check record is outside this manifest
  (`/home/fb31/BVS-wt/W3-PSHARP-R/…/BRIDGE_orth_thm1.md`). I re-derived it, but copy it into `lemmas/` or cite it from
  an input in the manifest.

---

## Interpretive sentences (D71)

| # | where | sentence (abridged) | verdict |
|---|---|---|---|
| 1 | Thm 1 display | "consequently … P(HPM = MPM = S₀) ≥ 1 − 4C√(log n/n)" | SUPPORTED (POST2 :91) |
| 2 | Thm 1 rem (i) | "sensitivity and specificity of all PIPs at rate √(log n/n), uniformly in j" | SUPPORTED (W3-POST :84; POST2 :91) |
| 3 | Thm 1 rem (ii) | "(no over-fitting mass)"; "specificity can fail without beta-min (numerical counterexample)" | SUPPORTED (W3-POST :87-94, labelled numerical) |
| 4 | Thm 1 rem (o) | "Theorem 1′ contains Theorem 1 when C_β²φ₀² > c₁; … coexist" | SUPPORTED (POST2 :47, :135-136) |
| 5 | Thm 1 rem (v) | models above 3(A+1)(s₀+1) log n carry O_P(n^{−1/2}) with no eigenvalue condition | SUPPORTED (W3-POST :52-58 + B1.3) |
| 6 | Thm 1 rem (vi), (A2) line | "on every design the miss is ≳ n^{−1/2}"; "on every design … forces s₀ = O(√log n)" | **OVERSTATED** (S3) |
| 7 | Thm 1 rem (vii) | moderate-n mixture; "the theorem describes the limit" | SUPPORTED as description (D-17; consistent with PSHARP Lemma S) |
| 8 | Thm 1′ title | "no eigenvalue condition off S₀ beyond the vanishing floor (A5)" | SUPPORTED (POST2 :133) |
| 9 | Thm 3 "In words" | "rate of Theorem 1 cannot be improved under its assumptions"; c free of s₀ when s₀ ≤ p/2 | SUPPORTED (B3.8 + AE; arithmetic checked) |
| 10 | Thm 3 rem (i) | named exactness cases; "√log n … from rare large gains of a single extra variable" | SUPPORTED (A1-E(b) at bounded p; Rem A3) |
| 11 | Thm 4 remark | "KL projection …: the posterior concentrates on the support of the best candidate predictor" | SUPPORTED (MISR-R :89-91, :126-128; CorGb-plus) |
| 12 | Thm 4 remark | contraction "at rate M_n/√n in Hellinger and M_n/n in KL"; fixed-design "needs only δ_n → 0" | SUPPORTED (CorH-U (G); CorH-plus (a′), class 𝒦^F implicit) |
| 13 | Card 1.4 | "uniformly over the residual variance (fixed candidate design)" | SUPPORTED (MIS(i) :114) |
| 14 | Thm 5 | "so the rate under (A6) is optimal up to the factor √log n" | SUPPORTED (START2-R :237) |
| 15 | Card 3.3 | "π₀ puts mass ≥ 1 − n^{−c} on S₀ …" (no probability qualifier) | **OVERSTATED** (S5) |
| 16 | Thm 6 | "in particular P(output and Ŝ ≠ S₀) → 0" | SUPPORTED (RM0-plus (b⁺)) |
| 17 | Thm 6 rem (o)/Thm 7 rem (b) | error split; "posterior-mode error plus search error" (labelled not part of theorem) | SUPPORTED (RM2-R :55, :139) |
| 18 | Thm 6 rem (i) | on 𝒢_n LS0 only deletes, ≤ n^b moves, certifies, cap never binds | SUPPORTED with a suitable choice of 𝒢_n (E7) |
| 19 | Thm 6/7 delivery | "neither limit can bind unless n + p + 1 > 2^{10⁶} or n ≳ 4 × 10⁹" | SUPPORTED (arithmetic checked) |
| 20 | Thm 6 (A4)/(A6) lines | b < ½ "expected to fail (heuristic)"; width condition "forced by this route" | SUPPORTED (RM2 C6, C3(b)) |
| 21 | Thm 7 intuition | (A5)(a) "holds automatically when Q has fewer than log n extra columns" | SUPPORTED ((W-χ) ⇒ (W)) |
| 22 | Thm 7 honest limits (ii) | "Theorem 6 … shows the same conditions hold w.p. → 1 under population analogues" | **UNSUPPORTED** (S6) |
| 23 | Thm 8 honest limits | intersection, not conditional; certification not claimed w.p. → 1 | SUPPORTED (SCR :83, :217-218) |
| 24 | Card 3.7 Buys | "the only coded-method guarantee that needs no visibility, leakage, start or block condition" | **OVERSTATED** (S4) |
| 25 | Thm 9 "In words" | "the posterior contracts at the rate √(log n/n)" | SUPPORTED (DIST :193-195) |
| 26 | Thm 10 "Which designs" | "(A5) holds only for designs with no leakage …, such as independent predictors; AR and block not covered" | SUPPORTED |
| 27 | Thm 10 (A4)–(A5) line | "vanishing mass to transport and Ẑ/Z → 1, independently of the ladder length" | SUPPORTED (SAMP :161-163) |
| 28 | Card 3.6 | "Theorem 6 … still applies under its own conditions, which AR and block designs meet" | **UNSUPPORTED** (S1) |
| 29 | Card 3.5 | "hence the printed (equal-weight pooled) Ẑ, is unbiased for Z" | **OVERSTATED** (S2) |
| 30 | Thm 10 rem (row 3.5) | "E[Ẑ \| calibration] = Z for every design and data set" | SUPPORTED (PoolZ) |

---

## Gates

- **G1 correctness — PASS.** Every step of PoolZ and R1–R4 is re-derived above. The arithmetic was also checked
  numerically (0 violations).
- **G2 hypotheses used = stated — PASS.** Each bridge proves exactly what its row consumes from its stated hypotheses.
  R4's p > s₀, R2's floor on Q ∪ {l} and R3's operational premises (carried as (S4)) are all explicit.
- **G3 faithfulness — FAIL.** All reader statements (Thms 1, 1′, 2–7, 8, 8′, 9, 9B, 9C, 10) are faithful to their
  masters: hypotheses are implied via listed bridges or (S1)–(S5), and no conclusion is stronger. But six interpretive
  sentences are overstated or unsupported (S1–S6). Four of them are in card rows (3.3, 3.5, 3.6, 3.7) and two in
  READER_VERSIONS remarks or honest limits.
- **G4 statuses and citations — PASS.** About 60 ids were checked against `claims.tsv` (version, status, state). The
  quoted statuses are verbatim, and the "conditional on …" clauses are carried (POST2 C/E/A1, MISR, MISR-R, RM2-R-plus,
  DIST Thm-B / Cor-C). Nothing below PROVED-CHECKED is called checked: PoolZ, R1–R4, Cor-1R, Prop-LB and [L1a′] are
  labelled as unchecked. The cited line ranges say what is claimed. Editorial notes: E4, E5, E8.
- **G5 no hidden finite-n or scope claims — PASS.** The finite-n display of Thm 1 is the master's uniform "for every
  n ≥ n₀". No two-sided rate is claimed on every design (Thm 1 rem (vi), Thm 3 (iv)), and Thm 8 has no n-dependent
  signals. S5 (card 3.3) is counted under G3.
- **G6 fidelity to the code — PASS.** The NOTATION / METHOD_INTUITION code facts agree with the pinned code: the prior
  w(k), K and ν; the score; the start law and start mode with its 10⁶ cap and tie DP; LS0 with cap ℓ_n + |S̃₀|
  (`cpp/v3_core.cpp:473-474`) and `le ≤ 1e6` (`v3_run.R:96`); equal-weight pooling (`v3_run.R:154,162`); MPM; the
  calibration's persistent stores and inherited HPM (`v3_calib.R:141`, `cpp/v3_core.cpp:725-735`, so Ŝ is the best over
  everything scored); and estimates becoming NA on non-completion. Minor wording is in E10.

**Score: 7.6 / 10** (C, S and F only). There are no C or F findings. The mathematics, bridges and statuses are sound.
The deduction is for six S findings, all interpretive sentences, the largest being the card-row 3.6 claim about
AR/block designs. Each needs a one-line text change. After those changes I would expect to score ≥ 9.

`COUNCIL-VERDICT round=R1 manifest=759a7dfd87ef7b958a0c8140b6cfa0158f4159cac31c62cf3cb0f1a75fdd7e09 seat=opus score=7.6 gates=FAIL`
