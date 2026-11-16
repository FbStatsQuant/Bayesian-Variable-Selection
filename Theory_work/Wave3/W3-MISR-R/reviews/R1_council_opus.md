# W3-MISR-R — council R1, seat `opus` (blind first read)

Manifest reviewed: `MANIFEST fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994` (`reviews/MANIFEST_R1.txt`).
Before reading, I recomputed sha256 of every in-ticket file listed there: STATEMENT, REPORT, READER_DELTA and the four lemmas
match the manifest. The working tree was clean before and after the review.
What I read: the ticket files in the manifest (not `LOG.md`, `CHECKPOINT_*`, or other `reviews/` files); BASE `STATEMENT.md`,
`G_corollaries.md`, `M_misr.md` (M.3), `R_reduction.md` (R.1–R.4); [POST2] `STATEMENT.md`, `A_occam.md` (A0), `D_hellinger.md`
(D0, D(b) constants); [W3P] `STATEMENT.md` §0–§2; [L2] `L2_gaussian.md:36-46, 85-106`.
Tool runs: `deps_hand.py` and `citecheck.py` both **write** files (`DEPS.tsv`, `reviews/CITECHECK.txt`), so I did not run
them as they are. Instead I recomputed the DEPS hashes in memory, and ran citecheck through `exec` with its final write
replaced by a print. Result: 151 checks, 0 failures, the same as `reviews/CITECHECK.txt`.

## 1. Per-claim decisions

| id | decision |
|---|---|
| W3-MISR-R:CorG-min | ACCEPT |
| W3-MISR-R:CorGb-plus | ACCEPT |
| W3-MISR-R:CorH-plus | ACCEPT |
| W3-MISR-R:CorH-U | ACCEPT |

All four proofs are correct as stated, and every clause is proved. The blocking findings below are all **F** findings in
derived texts (READER_DELTA and the REPORT registry blocks). None is in a claim or its proof.

## 2. Findings

**F1 (F) — `READER_DELTA.md:57-58`: the reader text says (A0) is "necessary".** The text: "(A0) The response condition is
exactly what the proof needs: when the noise is Gaussian it is necessary and sufficient for the exact reduction to a
well-specified problem". The master `W3-MISR-R:CorG-min` (c) (`STATEMENT.md:71-74`) proves necessity of **(OV^c)**, a
condition on the contrasts that allows design-dependent γ, τ² and an arbitrary random intercept. It does not prove necessity
of (A0), which fixes the full conditional law y | x_𝒞 ~ N(α′1 + x_𝒞β^𝒞, σ²_𝒞I) with constant parameters.
*Failure:* take y^r = α1 + X_𝒞β + ε with ε ~ N(0, σ²I) and α a Cauchy variable independent of everything. Then
(GR^c | σ(X_𝒞)) holds (Uᵀ1 = 0), so the exact reduction holds, but (A0) fails (y_i given x_𝒞 is not normal). The
proof also does not use all of (A0): it uses (N) + (OV) only through (GR^c | σ(X_𝒞)).
*Fix:* "(A0) is a convenient sufficient form. What the proof uses is its contrast version (Gaussian contrasts of the
residual given the candidates); when the noise is Gaussian, that version is necessary and sufficient for the exact
reduction (CorG-min (c))."

**F2 (F) — `READER_DELTA.md:47-51`: the reader text says the posterior contracts "around this law", but the master's
reference has its mean centred.** The text: "the posterior's fitted mean and variance also contract around this law [the (A0) law
N(α′ + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞)] in the in-sample average Hellinger and Kullback–Leibler distances, at rate M_n/√n …". The
masters (CorH-U (G), via H^a_n, K^a_n of `STATEMENT.md:34-39`) measure the distance from N(μ̂_i, v′) to N(μ_i(κ_n), v),
where μ(κ) = Cxβ is **centred** and μ̂ = X_Sθ is centred. BASE `STATEMENT.md:187-194` says the reference is "that law
with its mean centred over the sample".
*Failure:* against the uncentred (A0) law, each coordinate's mean difference carries the constant α′ + x̄_𝒞ᵀβ^𝒞. That
constant is not small in general, so the average Hellinger distance to the (A0) law does not tend to 0. The
plug-in-intercept variant of [POST2] `STATEMENT.md:118-119` is not part of this ticket's STATEMENT, and no bridge for it
is listed.
*Fix:* write "around this law with its mean centred over the sample (the fitted mean carries no intercept)", or add the
plug-in intercept as a listed bridge with a proof.

**F3 (F) — `READER_DELTA.md:51-53`: the reader text weakens the selection premise, and "uniformly" needs (UP).** The text:
"For fixed designs the contraction needs only that the posterior selects S₀^𝒞 with probability tending to one …, and holds
uniformly over such configurations".
(i) The premise of CorH-plus (a′) (A:SEL-P, `STATEMENT.md:114`) is δ_n = 1 − π(S₀) → 0 in probability. "The posterior
selects S₀ with probability → 1" reads naturally as P(HPM = S₀) → 1, which is strictly weaker. For example, π(S₀) = 0.4
with each other model below 0.4 makes S₀ the HPM, but Π(S ≠ S₀) ≥ 0.6 then violates the B^a conclusion.
(ii) "uniformly over such configurations" holds by (U-a) only over classes with the uniform premise (UP), not over
configurations each of which only satisfies selection pointwise (TARGET's own row, `TARGET.md:17`, says the same).
*Fix:* "needs only that the posterior mass of S₀^𝒞 tends to one in probability … and holds uniformly over any class on
which this holds uniformly".

**F4 (F) — `REPORT.md:52` and `REPORT.md:68`: the registry assumption lists omit hypotheses that the claims use.**
- CorGb-plus (`:52`) lists A:GAUSS-CAND-ROWS, A:MISR-OV, A:CORR-FLOOR, A:FIXED-S0 and A:P-POLY. A:MISR-OV is described
  (`:44`) as the omitted-part condition only. The noise hypothesis **(N)** (Gaussian, independent of the design), which
  §3 imposes (`STATEMENT.md:97`) and the proof uses (G2 [R-4] via G1.1), is in no listed id. In `STATEMENT.md:201` it
  belongs to A:MISR-OVC. The population energy and relative beta-min hypotheses (`STATEMENT.md:102-103`) have no id
  either.
- CorH-U (`:68`) lists only the fixed-design ids. Its clause (G) assumes all of §3 (`STATEMENT.md:152`): Gaussian
  candidate rows, (N) + (OV), the correlation floor, energy and beta-min. None of these is listed.
*Fix:* add A:MISR-OVC (or a separate (N) id) and ids for the population energy and beta-min conditions to CorGb-plus.
Add the same ids to CorH-U, marked "clause (G) only".

**E1 (E) — `STATEMENT.md:67-68` / `lemmas/G1_min.md:41-45`: "(OV^c) holds if … (OV)".** (OV^c) includes σ² + τ²(x) > 0
(`STATEMENT.md:59`), and (OV) does not give it. G1.2(i) proves only the conditional-law part. Nothing downstream is
affected: §3 states σ²_𝒞 > 0 separately, and (E1)/(E2) claim only (OV). *Fix:* "(OV), together with σ² + τ² > 0,
implies (OV^c)".

**E2 (E) — `STATEMENT.md:87-88`: (E3) says "(N) + (OV^c) **is** BASE's (GR^c)".** G1.5 proves only one direction (⇒).
The converse needs (N) plus (c). *Fix:* "gives".

**E3 (E) — `REPORT.md` registry record details.**
- CorG-min `depends_on: W3-MISR:MIS(ii)@stmt` (`:46`) sits next to an unconditional status. That is consistent with
  G1's note (`G1_min.md:5-6`), but a reader could misread it; say "pointer only".
- CorG-min premises (`:42`) omit `STATEMENT.md:184-185`, the Cramér input that clause (d) uses.
- CorH-plus `depends_on` (`:62`) omits `W3-MISR-R:CorG-min@stmt`, used by KL reading (ii) (`H1_plus.md:65`).
- CorH-U premises (`:66`) omit §3 (`STATEMENT.md:94-108`), which clause (G) uses.
- `REPORT.md:15`: "Cor-G(b) is the reader version of the headline masters" is garbled.

**E4 (E) — `DEPS.tsv` / `deps_hand.py`.**
- Some `uses` entries are incomplete. S:CorH-U uses §1 directly (B̄^b, H̄^b, K̄^b, 𝒦^F_n(≤s̄), sup ∅ — `STATEMENT.md:36-45`)
  and §2 (`:151, :153`), but lists neither S:notation nor S:CorG-min. L:G1_min uses the §1 conditional-law convention
  (`G1_min.md:24`) but does not list S:notation. No row uses S:inputs-deps (Cramér, the code fact).
- `deps_hand.py:47-49` marks a row DOWNSTREAM only when a direct dependency is not OK, reading the raw `state` dict, which
  is never updated to DOWNSTREAM. So staleness does not propagate transitively: if S:notation went stale, L:G1_min would
  still read OK. *Fix:* list the direct uses, and iterate the DOWNSTREAM marking to a fixed point.

**E5 (E) — `READER_DELTA.md:41-46` (Example).**
- β^𝒞 and σ²_𝒞 are written with Σ_𝒞𝒞⁻¹, but (A2) does not make Σ_𝒞𝒞 invertible. The master (E1) uses Σ_𝒞𝒞⁺. *Fix:*
  "(with Σ_𝒞𝒞 invertible; in general Σ_𝒞𝒞⁺)".
- In "linear function of the candidates plus independent Gaussian noise", the noise rows must be iid across i for (A0)'s
  conditional independence (master (E2)).
- B4.1 (`:73`) gives |T| ≤ k_n only for large n. I checked the arithmetic: s + m♯_n ≤ 2s + 1 + (sA + s/2 + 1)log n/log 2
  < 3(A+1)(s+1)log n eventually. This is enough for the O(·) conclusion, but say "for all large n".

**E6 (E) — `READER_DELTA.md:53-54` / `:76`: the fixed-design sentence has no master in the bridge table.** "A fixed-design
version of the theorem uniform over the residual variance also holds" is BASE MIS-R (i) (v-free constants,
`W3-MISR/STATEMENT.md:114`). It is not CorH-plus or CorH-U, and B4.4 maps "the fixed-design sentence" only to those. Name
MIS-R (i) as its master.

**E7 (E) — `lemmas/H2_uniform.md:4-6`: clause (G)'s conditional list is broader than what (G) uses.** (G) uses (RD) (its own
freezing argument), (U-a) and MIS-R (i), plus G2 steps 1–5 and [R-4]. It does not use MIS-R (ii). The listed W3-POST2:E,
W3-POST2:A1 and SOP:TH128 enter only through MIS(ii). Listing them is conservative, not wrong; trim if wanted.

**E8 (E) — `STATEMENT.md:193` (§8, CorH-plus ⇒ Cor-H).** BASE Cor-H's row-wise KL reading (generic intercept α′) is
reproduced only for a deterministic intercept (v1.1a, WEAKER). The implies-row could say that it covers clauses (a), (b)
and the interpretive sentence only in its restricted form.

## 3. Sweep duties

**1. Statement copies against lemma statements.** Each clause of §§2–5 is proved as stated:
- **§2:** (a) G1.1; (b) G1.2; (c) G1.3; (d) G1.4; (e) G1.5; Remark G1.5. I re-derived the conditional convolution (P1),
  the characteristic-function step on ℚ^N with continuity, v ≥ σ² from |φ| ≤ 1, the Cramér/Cramér–Wold step with the
  deterministic (b, Σ_ε), the Moore–Penrose step (ker Σ_𝒞𝒞 ⊆ ker Σ_𝓜𝒞, Cov ζ), and the measurability of κ_n.
- **§3:** G2. The [R-1] reduction leaves X, θ, μ, S₀, v, β̌ᵀRβ̌ and ρ^{BM} unchanged. In step 2 the floor is used only
  for |T| ≤ k_n (checked against `[L2]:94-99`). Step 3 needs β^𝒞ᵀΣβ^𝒞 > 0, which holds by the floor on S. In step 4 the
  liminf branch with c = (c₀ + c_RL/16)/2 is correct. The failure bound is a union of the three events.
- **§4:** H1.1–H1.4. The (a′) hypotheses equal [POST2] D(a) (`:107-111`: R1, G, (E), (F₀), δ_n → 0), so (OS) and the
  margin are not needed. I checked the KL closed form, the Taylor bound on |x − 1| ≤ ½, and the KL inclusions with
  M′_n = min(M_n^{1/2}/2, n^{1/4}), M′_n² + M′_n/2 ≤ 3M_n/8 for M_n ≥ 4, and M″_n = √log n (n ≥ 9, log 9/9 < ¼).
- **§5:** H2.0–H2.5:
  - Fillers: (SZ), (E^σ; s), (F₀; 1), (F_λ; 1), (F_w; 1) with λ_min(G) = n − 1, (OS) via A0, and BM all check.
  - Subsequence argument: C_H(s, A) does not depend on (M, φ₀, C_OS); [D] line 72 gives C_H = 8(C_A(s + j₀) + c₂) + 1
    with c₂ = c₁(s, A) + 1. B̄^b ⊆ B^b holds because C̄_H ≥ C_H.
  - (RD) uses freezing with a jointly Borel g_n. No measurability of the class is needed, because 𝒜_n ∈ 𝓕_n is assumed.
  - (G) has φ₀ ≤ 1 since c_R ≤ R_jj = 1, and 𝒜_n ⊆ {X ∈ 𝔛_n(p)} because σ̂_j² ≥ ½.

**2. Quantifiers and uniformity.**
- CorGb-plus: n* and c depend on the sequence (stated). C is the MIS-R (i) constant for (s, A, 2M₀ + 1, (c_R/8)^{1/2},
  C_OS, c) (stated).
- (U-a), (U-b): M_n and η are fixed before the sup over the class. The "lim sup > 0 ⇒ infinite 𝒩" step is correct.
- (RD): ε_n depends on (η, M_n, the class). The η-family form is restricted correctly to the (a)-type sets, because the
  (b)-type sets depend on (s̄, A) through C̄_H.
- Null events: the reference configuration is placed off {X ∉ 𝔛_n(p)}, and the zero-contrast set is N_N(0, I)-null.
- Measurability: Borel strata {p, supp β = T}, Tonelli for g_n, and Borel Ĝ_n. No defect found.

**3. Each lemma's scope against downstream uses.**
- G1 → G2: (a) with constant (γ, τ²).
- G1 → H1: (b)(ii) for KL reading (ii). α must be a design function, and the statement says so.
- G1 → H2 (G): through G2 [R-4].
- H1 → H2: (a′) and (b) are applied to arrays built from fillers whose constants are (M ∨ s, φ₀, C_OS ∨ C_f), inside
  H1's hypotheses.
- G2 → H2 (G): steps 1–5 and the events 𝒜_n ⊆ {κ_n ∈ 𝒦^λ_n}. Class membership of κ_n and of the reduced κ̌_n agree
  ([R-1]), and so do the sets B^a, H^a, K^a.
No use exceeds a lemma's scope.

**4. REPORT and registry blocks against STATEMENT.**
- Statuses are verbatim from `G1_min.md:4`, `G2_corr.md:4`, `H1_plus.md:4` and `H2_uniform.md:4`.
- Statement line ranges (48-92, 94-108, 110-132, 134-155) are correct.
- Conditional-on lists are complete. CorH-plus drops W3-POST2:C correctly, since (a′) takes selection as a premise. (G)'s
  list is conservative (E7).
- The implies rows are true (with the E8 caveat on BASE's interpretive KL sentence).
- The W3-DIST paragraph (`REPORT.md:23-31`) is labelled HEURISTIC/OPEN, and its one mathematical sentence follows from
  §2(b).
- Assumption ids are incomplete (F4). Premises and depends_on have record gaps (E3).

**5. DEPS spot-check.** I recomputed every row in memory (same hashing as `deps_hand.py:29-35`). All ten sha values equal
their checked_sha, for example S:CorG-min 97b1ed2602f41b3b, S:CorH-U 533cc312b9632e27 and L:H2_uniform 7757a8986d5306c9.
Some `uses` entries are incomplete, and DOWNSTREAM does not propagate transitively (E4).

**6. READER_DELTA.**
- The conclusion display and (A1)–(A3) follow from CorGb-plus.
- Bridges: B4.0 is correct (ε := y − α′1 − X_𝒞β^𝒞 gives (N) with q = 0 and (OV) with a = γ = τ² = 0). B4.1 holds for
  large n (E5). B4.2 is an identity. B4.4 is correct and is clause (G).
- The text claims beyond the masters in three places: F1 ("necessary"), F2 ("around this law", where the masters use a
  centred reference) and F3 (selection premise and uniformity).
- One sentence has no listed master (E6).

## 4. Better-theorem proposals (not findings)

- **(G) without beta-min, in the (b) form.** G2's steps 1–3 and 5 do not use the beta-min condition. Under §3's
  hypotheses minus the ρ^{BM} condition, the events 𝒜_n (SD ∩ eigenvalue ∩ energy) satisfy
  𝒜_n ⊆ {κ_n ∈ 𝒦⁰_n(s, A, 2M₀ + 1, (c_R/8)^{1/2}, C_OS)}. (RD) with (U-b) then gives
  Π(B̄^b_n(κ_n) | X_𝒞, y^r), Π(H̄^b_n(κ_n) | ·), Π(K̄^b_n(κ_n) | ·) → 0 in probability: a Gaussian-row
  contraction at rate log n/n with no beta-min condition.
- **CorGb-plus in conditional form.** MIS-R (ii)(a) already gives E[δ_n | X_𝒞] ≤ C r_n almost surely on 𝒜_n, which is
  stronger than the unconditional display.
- **CorG-min (d), converse direction.** If additionally Σ_ε = σ²I_N, (d) returns exactly (OV^c) with τ² = v − σ². This
  extends the (c)-equivalence to any noise law whose contrast covariance is scalar.

## 5. Gates

- `correct`: **PASS** — every proof of the four claims checks line by line; no C finding.
- `strength`: **PASS** — no claim states more than its proof gives, and every hypothesis used is stated (E1 and E2 are
  wording only).
- `faithful`: **FAIL** — the derived texts are not faithful to STATEMENT: READER_DELTA (F1, F2, F3) and the registry
  assumption lists (F4).
- `statuses`: **PASS** — statuses are verbatim and conditional lists are complete (conservative for (G)).
- `sweep`: **FAIL** — all six duties are done, but blocking F findings were found (F1–F4).
- `reader`: **FAIL** — READER_DELTA claims beyond the masters and bridges (F1, F2, F3).

## 6. Score and verdict

Score 8.5. The four claims are correct and as strong as stated. Points are lost only for the faithfulness of derived
texts (three READER_DELTA sentences and the registry assumption lists). Each is fixable by a wording change and needs no
new mathematics.

COUNCIL-VERDICT round=R1 manifest=fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994 seat=opus score=8.5 gates=FAIL
