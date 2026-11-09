# W2-FAC-B — STATEMENT (target statement)

Ticket W2-FAC-B, Theory Wave 2 (route B: start-mode structure + path-restricted analysis). Lead: Claude Opus 5.5
(Claude Work). Status of this file: **v3.1 — LOCKED** (2026-11-09; R02 LOCK-WITH-CHANGES applied → v3; v3.1 = post-lock flagged
addition (C1-M) and the exhaustive-sweep fixes R07 items 1–17 (reviews/R07_disposition.md); no conclusion strengthened
except (C1-M), which weakens a hypothesis). v1 was REJECTED by R01
(reviews/R01_statement_lock_sol.md: the log-n margin claimed for swaps in (C2)(iii) is false — an analytic O_P(1)
counterexample — plus six further required changes); all seven are applied here (disposition: reviews/R01_disposition.md).

Abbreviations: SoP = `Theory_work/State_of_Project/sections/`; FINAL = `Theory_work/Wave1C/FINAL/sections/`;
GROW = `Theory_work/Wave1C/C-GROW/`; GEN = `Theory_work/Wave1/W1-GEN/`; A1/A2/A3 = `Theory_work/Wave1C/HQ_AUDIT/`.
All results are asymptotic (Wave-2 protocol scope rule).

## 0. Target, diagnosis and scope

HQ target: Theorem FAC — on factor / equicorrelated designs with growing p, D_n → 0 and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0
for the method as merged (v3.1, main 4676af6), then delivery P(Ŝ⁺ = S₀) → 1.

**Diagnosis (component numerics, not proofs; numerics/N1–N5).** On factor designs every null block carries factor
signal through the full-response block tables r_b, so as n grows the start mode fills up: in N1 (exact Gram, S5,
one- and two-factor designs, p ≤ 400) S̃₀ = [p] in most data sets at n ≥ 10⁶ — not all: e.g. F2 p = 200 c = 0.5 at
n = 10⁶ has |S̃₀| = 193 (0/5 full), S5 p = 400 c = 0.5 at n = 10⁶ has |S̃₀| ∈ {396, 397} (0/3 full); all are full at
n = 10⁸ (numerics/N1_summary.md). From a full start, the uncapped LS0 path observed is a pure backward elimination
(p − s₀ deletions). Hence GROW's route (|S̃₀ ∖ S₀| = O(log n)) cannot apply, and the LS0 route needs a cap ≳ |S̃₀|.
For compound symmetry the scan has an exact one-dimensional structure (lemmas/L1). For p > n/2, in one diagnostic data set (N2: exact Gram, one
factor, n = 600, p = 500, aligned truths in different blocks, N₀ = ∅) the start mode is size-saturated (|S̃₀| = K = 300),
the LS0 path begins with 19 null–null swaps and needs 315 moves against the MR1 cap 311 (a cap failure on that data set;
saturation is not claimed in general — e.g. p − |N₀| < K is possible — and no asymptotic impossibility is claimed).

**Scope locked here.** The core case **compound symmetry, exact Gram, p ≤ ⌊n/2⌋** — targeted for proof through the
full review pipeline — named **Theorem FAC-CS**; it is never presented as covering random-row study S5 or general
factor designs. The substantive regime is p ≫ log n (for fixed p, or p growing slower than ≈ log₂ n, the production run
eventually enumerates all models, SoP `02_method.tex:167-170`, and T03♯ alone gives reported-model consistency; the
theorem includes such sequences without adding discovery content there). Delivery on this class is a **new
extension** using Proposition F's machinery and A2's argument. The frontier (S5, general loadings, k ≥ 2, iid rows,
p > n/2) is recorded with evidence, separating obstructions **to this proof technique** from (unproved) obstructions to
consistency.

## 1. Setting

* **D0** (SoP `04_theory.tex:69-74`): log m(A) = log c_n − ½[log det H_A − log det(G_A + I)] − ν log(0.02 + Q_A),
  G_A = X_AᵀX_A, z_A = X_Aᵀy, H_A = (n + 1)G_A + I, Q_A = yᵀy − n z_AᵀH_A⁻¹z_A, ν = 0.01 + n/2; capped BB(1,p) prior
  w(k) = 1/(2C(2p − 1, k)) (exact ratio w(k + 1)/w(k) = (k + 1)/(2p − 1 − k)); K = min(p, ⌊n/2⌋), Ω = {S : |S| ≤ K};
  F(S) := log w(|S|) + log m(S); block tables r_b(U) = m(U)/m(∅); start γ₀(S) ∝ w(|S|)∏_b r_b(S ∩ C_b) on Ω.
* **G** (as `Theory_work/Wave1/W1-GEN/STATEMENT.md:29-30`): fixed raw design X^r with nonconstant columns, y^r = α1 + X^rβ + ε,
  ε ~ N_n(0, σ²I), σ² > 0 fixed; C := I − 11ᵀ/n, D_x := diag of the raw columns' sample standard deviations,
  X := CX^rD_x⁻¹ (‖x_j‖² = n − 1); **θ* := D_xβ, μ := CX^rβ = Xθ*, Y := Cy^r = μ + Cε**; S₀ = supp θ*, s₀ = |S₀| ≥ 1
  fixed; the score uses y := Y/s, s² := ‖Y‖²/(n − 1), so yᵀy = n − 1 (R07 item 1).
* **Blocks** C₁, …, C_J: the method's actual partition (SoP `02_method.tex:187-211`), blocks of size ≤ 16. The
  statistical claims (C1)–(C3) hold, at indices with K = p, for every deterministic partition into blocks of size ≤ 16
  (so linkage tie rules do not matter); the delivery claim (C4) is for the specified method's partition (B ≤ K), whose
  construction invariants Proposition F inherits (R07 item 3).
* **Method**: v3.1 + LS0 as merged on main 4676af6. LS0 = one §6.10 local search (SoP `02_method.tex:463-470`) from the
  emitted start-mode centre S̃₀ with move cap **a_n := ℓ_n + |S̃₀|** (MR1 (C-GROW); ℓ_n := ⌈log₂(n + p + 1)⌉ is the legacy
  un-augmented cap, used below only for comparison). A search with cap a scans its centre (every feasible flip and
  swap neighbour is scored and joins the scored set), moves to the best scanned neighbour if it strictly increases F
  (exact score ties among scanned neighbours: lexicographically smallest set, `02_method.tex:483`), makes at most a
  moves and then one further complete scan; so for a nonnegative integer cap a, a search whose uncapped path reaches S₀ after d moves scores S₀ if a ≥ d − 1,
  and a search whose uncapped path **terminates** at S₀ after d moves (S₀ has no strictly improving neighbour) ends at S₀ as a
  certified search endpoint (no `local_limit`) if a ≥ d (single-search prefix property from the loop rule (L3) of
  FINAL `s7_impl.tex`, valid for every cap; R07 items 4, 7).
  "Certified search endpoint" does not refer to the public `local_certified` flag of the finally reported HPM.
  The deterministic LS0 search is defined on every admissible data set (exact-branch convention, FINAL `s7_impl.tex`
  Lemma CAP); on the exact-enumeration branch, enumeration supplies discovery. Start-mode / HPM ties use the
  size-then-lex rule (irrelevant here: the start-mode maximiser is unique on the events used).
* **Implementation premises** (named, not proved; as GROW §1 and FINAL s5/s7): EX-A, EX-S, SR, GUARD-W, OP-LS0 (cap a_n),
  e4 read as e4′ (only "the emitted centre is the unique maximiser of γ₀" is used), complete scans; for R′ > 4 IND-T and
  the c₄ search. CAL is a premise of the [M5-0] route in (C3) only; (C4) is CAL-free. 𝒪 = output event, U_n = 𝒪ᶜ,
  D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) (potential-run notation, SoP `04_theory.tex:84`).

## 2. Hypotheses (class CS)

* **(CS) exact-Gram compound symmetry.** XᵀX = (n − 1)Σ_n, Σ_n = Υ_n[(1 − ρ)I_p + ρ11ᵀ]Υ_n with ρ ∈ (0, 1) fixed and
  Υ_n a deterministic diagonal ±1 matrix (column sign flips). Requires p ≤ n − 1.
* **(P)** p = p_n ≤ ⌊n/2⌋ for all large n (so K = p; p_n need not grow).
* **(θ)** s₀ fixed; write S₀ = {i₁(n) < … < i_{s₀}(n)} (positions arbitrary); ((Υ_nθ*)_{i_r(n)})_{r ≤ s₀} equals a fixed
  vector ϑ ∈ (ℝ ∖ {0})^{s₀}, and we write ϑ_{i_r(n)} := ϑ_r, ϑ(V) := Σ_{i∈V}ϑ_i for V ⊆ S₀ (so (FS) is a finite list of
  conditions on ϑ; R07 item 15); σ² fixed.
* **(FS) full start — a sufficient generic no-cancellation condition.** With ϑ(V) := Σ_{i∈V}ϑ_i:
  (a) ϑ(V) ≠ 0 for every nonempty V ⊆ S₀; (b) ϑ_l + ρϑ(V)/(1 + (u − 1)ρ) ≠ 0 for every V ⊆ S₀, l ∈ V, u ∈ {0, …, 15}.
  For sign-corrected columns, U ∌ l, u = |U|, V = S₀ ∖ U, the population partial covariance (Σ scale) is
  c(U, l) = Cov(x_l, μ | x_U) = (1 − ρ)[ϑ_l + ρϑ(V)/(1 + (u − 1)ρ)] (ϑ_l := 0 for a null); (FS) makes every c(U, l)
  with |U| ≤ 15 nonzero **except** when U ⊇ S₀ and l is null, where c = 0. (FS) excludes finitely many hyperplanes of
  ϑ; it is sufficient, not necessary, for the conclusions on a given partition.

**(H0) is automatic on this class** (claim (C3)(i)): with Σ̄ := (1 − ρ)I + ρ11ᵀ, the T03♯ hypotheses hold with A = 1,
φ₀² = 1 − ρ, fixed g₀ ∈ (0, 1 − ρ], any fixed M > ϑᵀΣ̄_{S₀S₀}ϑ (= θ*ᵀ(Σ_n)_{S₀S₀}θ* = ‖μ‖²/(n − 1)), and BM-∞.
Bounded or O(log n) relevance-set hypotheses (GEN, GROW) are not automatic on this class and do not cover the
substantive regime p ≫ log n (for bounded p the trivial relevance set [p] does satisfy their size requirement).

## 3. Definitions used in the claims (precise forms in lemmas/L1)

Write (after the sign correction) g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ) and represent g = √ρ η1 + √(1 − ρ)ξ with
η ~ N(0, 1), ξ ~ N(0, I_p) independent (L1.1). For S₀ ⊆ T ⊆ [p], k = |T|, the **centre** is
x_T := (Σ_{j∈T}ξ_j − ϱ_n)/(k + κ_n), with κ_n := (1 − ρ)/ρ + 1/(ρ(n² − 1)) and the k-free offset
ϱ_n := [√(n − 1)ρθ̄/(σ√(1 − ρ)) + √(ρ/(1 − ρ))αη]/β (θ̄ = ϑ(S₀), α = (n² − 1)(1 − ρ) + 1, β = (n² − 1)ρ). For every
null j, the deletion (j ∈ T) or addition (j ∉ T) gain is a strictly monotone function of |ξ_j − x_T| (L1.3–L1.4).
Let N₀ := ⋃{C_b ∖ S₀ : S₀ ⊆ C_b} (nulls sharing a block with all truths; |N₀| ≤ 15), S* := [p] ∖ N₀,
𝒩* := S* ∖ S₀ and m₀ := |𝒩*|. For **every** retained set T (S₀ ⊆ T ⊆ S*):
a_T := max({ξ_j : j ∈ T ∖ S₀, ξ_j ≤ x_T} ∪ {−∞}), b_T := min({ξ_j : j ∈ T ∖ S₀, ξ_j > x_T} ∪ {+∞})
(one-sided and empty configurations included; exact equalities are excluded on a probability-one nondegeneracy event).

## 4. Claims

* **(C1) Start mode.** Under G, (CS), (P), (θ), (FS): P(S* is the unique maximiser of γ₀ on Ω) → 1. On this event S̃₀ = S* ⊇ S₀
  and |S̃₀ ∖ S₀| = m₀ = p − s₀ − |N₀|.
* **(C1-M) Masked truths — added after lock, flagged (HQ note on FAC-A open item 4; lemmas/L2.5).** (C1)–(C4) also hold
  with (FS) replaced by (FS′): (FS-a); (FS-b) only for u ∈ {1, …, 15}; and every block containing a truth j with
  (1 − ρ)ϑ_j + ρϑ(S₀) = 0 also contains a null. This weakens a hypothesis only; no conclusion changes.
* **(C2) Path lemma (key lemma).** Under the same hypotheses there are events with probability → 1 on which the
  uncapped §6.10 search from S* has the following properties at every visited set T ≠ S₀ (T_0 = S*, T_{i+1} = the
  chosen neighbour of T_i):
  (i) the chosen move deletes a null j_i ∈ argmin_{j∈T∖S₀}|ξ_j − x_T|; it has positive gain;
  (ii) every addition has gain ≤ −c log n (c = c(ρ, s₀) > 0); every truth deletion and truth-out swap has negative gain;
  every null-out swap and every other null deletion has gain **strictly below the chosen deletion's gain** (no sign or
  log-n margin is claimed for swaps relative to F(T));
  (iii) before each move, including at T_0 (empty interval), the deleted nulls 𝒩* ∖ T are exactly the nulls j ∈ 𝒩*
  with a_T < ξ_j < b_T (an open gap / rank interval of the sorted configuration of 𝒩*, with the extended endpoints of
  §3, which may be ±∞), and a_T < x_T < b_T;
  (iv) after exactly m₀ moves the search is at S₀, where every feasible neighbour has strictly smaller F.
  Consequently the deterministic LS0 search with any nonnegative integer cap a ≥ m₀ − 1 scores S₀; with a_n = ℓ_n + |S̃₀| ≥ m₀ it ends at S₀
  as a certified search endpoint. With the legacy cap ℓ_n the deterministic LS0 scored set does not contain S₀ whenever
  m₀ ≥ ℓ_n + 2 (a statement about LS0's scored set, not about the full fit).
* **(C3) Theorem FAC-CS.** Under G, (CS), (P), (θ), (FS), the implementation premises of §1 (with CAL) and MR1:
  (i) (H0) holds; (ii) D_n ≤ P(𝒦_nᶜ) → 0, where 𝒦_n := {deterministic LS0 with cap a_n scores S₀}; (iii)
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n).
* **(C4) Delivery (new class extension of Proposition F).** Under G, (CS), (P), (θ), (FS) and **all** premises,
  method changes and the amended allocation of Proposition F as stated in FINAL `s6_delivery.tex` (total tier-1 fallback;
  LS0 cap a_n; EX-A with its unit-cost interpretation, IDEAL-W, EX-S, SR, e4, GUARD-W, TDP-IMPL, MACH, OP-LS0 with cap
  a_n, valid declared seed/allocation, envelopes W_G, M_G, and the current-head LS0 preflight time/archive terms of
  `s6_delivery.tex:37-44`) — CAL not assumed: for every admissible n ≥ 3, P(no output) = 0, and P(Ŝ⁺ = S₀) → 1 under the
  original noise law. Proof obligation: verify Lemma S's inputs for CS designs and combine T03♯ with the deterministic
  discovery event 𝒦_n through D′'s pathwise inclusion (as A2 step 3); discovery is **not** inferred from D_n → 0. The
  exact-arithmetic/unit-cost and code-audit qualifications of Proposition F are inherited, not removed.
* **(C5) Frontier (evidence; not proved).** (a) p > n/2: in one diagnostic data set the start is size-saturated and the
  MR1 cap fails (N2); saturation in general needs hypotheses not studied here; no asymptotic counterexample is claimed; a larger LS0 cap is a proposed response, not a proved remedy.
  (b) S5 (block compound symmetry, p/5 blocks), general one-/two-factor loadings, k ≥ 2: the same start/path mechanism is
  observed (N1), but the exact one-dimensional reduction is lost — an obstruction to this proof technique only.
  (c) iid rows: the sample Gram is not exactly compound symmetric — obstruction to the technique only. Each is stated
  precisely in REPORT.md.

**Uniformity in p_n.** (C1)–(C4) are claimed for every sequence p_n ≤ ⌊n/2⌋ (bounded, divergent or neither): the
proofs give, for each n, events and thresholds n₀ that do not depend on which regime p_n is in — a crude regime
p ≤ n^{1/200} (squared null statistics O(log(p + 1) + L_n²), bounded by a small fixed multiple of log n for n ≥ n₀; no
balance argument; covers bounded p) and a growing regime
p > n^{1/200} (order statistics, sign symmetry, end-phase balance) — so no subsequence argument is needed (the onset applies at indices with p ≤ ⌊n/2⌋; R07 item 6).

## 5. Not claimed

Finite-n statistical discovery/recovery bounds (the finite-n ideal-machine statement P(no output) = 0 of (C4) is
claimed); anything for p > n/2; random (iid-row) designs; S5 or general factor loadings; changes to
shipped components (the fallback of (C4) is the already-merged finding of A1/A2).

## 6. Dependencies (statuses verbatim)

M5(0)/T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; S-T/T03♯ "PROVED; SF VERIFIED (W2-VT03R);
XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma CAP (FINAL s7)
"PROVED (by this seat)", council-checked; Proposition F (A1 corrected statement, council round 3 passed; preflight
addition checked in A4 "OK-WITH-FIXES") and F-GROW (A2 "PROVED (A2), checked by A3").
