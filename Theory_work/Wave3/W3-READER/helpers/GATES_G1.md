# GATES_G1 — strength gates (LIFECYCLE §4.2) for card rows 1.1, 1.2, 1.3, 1.4, 3.7 (helper G1, W3-READER leg 2, 2026-11-16)

Helper G1 (Claude Opus 5.5, effort high; no subagents; no new proofs). Brief: `BRIEF_LEG2_GATES.md`. Read-only except this
file; no git state changed. Statuses are verbatim from `Theory_work/INFRA/registry/claims.tsv` (`claims.tsv:N` = line N).
`sharpness.tsv:N` = line N of `Theory_work/INFRA/registry/sharpness.tsv`. "AM" = the ticket's `ASSUMPTION_MAP.md`; "RV" =
`READER_VERSIONS.md` (working copy, 2026-11-16; row numbering of the card v0.4, MISR = row 1.4). Literature not re-read
here is taken from the ticket files (cited); anything from my own memory is marked **(recalled, not re-read)**.

## SUB-PAR SIGNAL: none found

No literature dominance was found in any comparison the files support. No hypothesis is shown unnecessary by an easy
stronger theorem that lacks a disposition: every such proposal has a triage class (A/B) or a ticket. Open items (not
sub-par signals):
1. **lit OPEN, row 1.4:** misspecified-model selection results by Rossell (2022; also Rossell–Rubio 2018), **(recalled, not
   re-read)**, are compared in no file. The input `SOP:TH128` already carries the LIT-STAT verdict "modest extension of
   Rossell 2022" for the well-specified case (`claims.tsv:14`).
2. **lit OPEN, row 3.7:** `W3-SCR` has no literature section. The natural comparators are sure screening (Fan–Lv 2008) and
   guarantees for local optima of L0 / best-subset local search, **(recalled, not re-read)**. Neither is compared anywhere.
3. **Recorder inconsistencies in `sharpness.tsv`** (evidence exists but is not recorded): FIXED-S0 is "NONE"
   (`sharpness.tsv:7, 12, 201`) although W3-PSHARP proves that bounded s₀ is necessary for the rate. ENERGY is "NONE"
   (`:5, :194`) although MISR N5 is a numerical counterexample. P-POLY is "ARTEFACT" for SOP:TH09 (`:2`) but
   "NECESSARY-FOR-ROUTE" for W3-POST:Thm-1 (`:202`); both readings are compatible, see row 1.1. PSHARP:A GAUSS-NOISE is
   "NECESSARY-FOR-ROUTE" (`:230`), which holds for (W-orth) only (sharp2 f02). There are no rows for W3-MISR:Cor-G(b), and
   W3-SCR:A1 is "NONE" (`:226`).
4. Stronger versions of rows 1.1 and 1.2 exist as `W3-POST2:A1/E/C`, status "PROVED (by this seat, unchecked)"
   (`claims.tsv:359,362,365`). They are not at parity because acceptance was stopped on 11-15 (RV:297-299). This is a
   correctness-parity item, not a missing disposition.

---

## Row 1.1 — Thm 1, posterior concentration, fixed design · master `W3-POST:Thm-1@1.0.0` (= `SOP:TH09@1.0.0`)

Statuses: W3-POST:Thm-1 "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (`claims.tsv:344`). SOP:TH09
"T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03:
PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY" (`claims.tsv:11`). Registry gates: TH09
"lit:PENDING; necessity:PARTIAL; better:PENDING". Thm-1 has only `correct:PASS(...)`.

### lit
Ours = `W3-POST/STATEMENT.md:61-100`. SL = Song–Liang 2015. NH14 = Narisetty–He 2014. YWJ16 = Yang–Wainwright–Jordan 2016.

| item | ours | Song–Liang 2015 | vs SL | closest BVS (NH14 / YWJ16 / Rossell 2022) | vs closest |
|---|---|---|---|---|---|
| prior | coded BB(1,p) capped at K = min(p,⌊n/2⌋); ridge g = n; IG | independent inclusion r_n/P_n, cap r̄_n with cap condition (10); ridge-prior example V⁻¹ = E(xxᵀ)+c_nI (AM:39-40, 63-66) | **incomparable**: (10) fails for the coded cap when p ≥ n/2 and BB(1,p) has prior mean size ≈ 1; our prior is their ridge example on the sample scale (AM:63-66) | NH14 spike-and-slab with p-dependent slab (AM:72-74); YWJ16 g ≍ p^{2α}, π(γ) ∝ p^{−κ\|γ\|} (AM:90-93) | **incomparable**: neither covers the coded prior |
| design | fixed design. (F_λ): fixed floor on all sets of size ≤ j₀. (F_w): unnormalised floor up to size m♯_n = O(log n). No λ_max | Thm 1: \|x\| ≤ 1. Thm 2: Cond. 1 (exponential moments). Cond. 3: vanishing floor on all (r̄_n+1)-sets (AM:41-61) | **incomparable**: ours is a fixed floor on bounded sets plus a free floor at O(log n); theirs is a vanishing floor on larger sets (AM:58-62) | NH14: Cond. 4.4 residual signal + Cond. 4.5 minimum nonzero eigenvalue (singular sets allowed) + λ^n_M bound (AM:75-87). YWJ16: RE(s) + SI(s) (AM:92) | **incomparable**: ours is stronger on singular null directions (AM:84-86); NH14 needs λ_max control and we do not |
| dimension | 2 ≤ p ≤ n^A | p < exp(Cn^α), P_n ≻ n^θ (map:10-12, 18) | **weaker** (narrower range) | NH14 log p = o(n); YWJ16 p ≥ n, s* ≲ n/log p (AM:87, 94) | **weaker** |
| sparsity | s₀ fixed | r_n-dependent | incomparable | NH14 \|t\| fixed (AM:75) = **equal**; YWJ16 growing s* = **weaker**. For the coded prior, rate r_n forces s₀ = O(√log n) (row 1.3), so growth costs rate | equal / weaker |
| signal | BM(c) at √(log n/n), c > c₀ ≥ 128 | through Cond. 3 and ε_n | same order; constant worse | NH14 log(√n ∨ p) (AM:76-77, 86); YWJ16 C²_β ≥ c₀(L+L̃+α+κ)σ² log p/n (AM:96) | same order; **weaker** constant (f15 (a)) |
| energy | ‖μ‖² ≤ nM, M fixed | analogous only to Cond. 2 (AM:52-53) | incomparable | YWJ16 Assumption A ‖Xβ*‖²/n ≤ gσ₀² log p/n (AM:91) | **weaker** (ours more restrictive) |
| noise | Gaussian, σ*² fixed | Gaussian, σ² ~ IG | equal | Gaussian in all (AM:14); NH14 Thm 4.1 known σ² (AM:81-82) | equal |
| conclusion | 1−π(S₀) = O_P(√(log n/n)); HPM = MPM = S₀; PIP sensitivity and specificity uniform in j | Hellinger contraction (Thms 1–2); sure screening, sensitivity only (Thm 3, "the specificity is not controlled"); ξ_q inclusion; Thm S not inspected (map:16-22; AM:43-46, 67-69) | **stronger** on selection; SL stronger in kind (Hellinger). Overall **incomparable** | NH14 P(Z = t \| Y, σ²) → 1, no rate (AM:81-82): ours **stronger**. YWJ16 1−π ≤ c₁p⁻¹ under its prior (AM:96-100): faster, but a different prior. For the coded prior our rate is exact (W3-PSHARP/STATEMENT.md:79-88): **incomparable** | — |
| Rossell 2022 | — | — | — | project LIT-STAT verdict: T03♯ is "a modest extension"; P(S† ≠ S₀) ≤ 2E[1−π(S₀)] is "his Proposition 1 word for word", credit required (`State_of_Project/sections/05_history.tex:324`; `INFRA/FAILED_ROUTES.md:128` RF130; `claims.tsv:14`) | ours **extends**, not dominated; thin novelty margin, credit required |

**literature dominance: NO.** No compared result covers the coded prior. Note the "modest extension of Rossell 2022" verdict.

### necessity
Hypotheses as in `claims.tsv:344`: A:GAUSS-NOISE; A:ENERGY; A:SPARSE-EIG; A:FIXED-S0; A:P-POLY; A:BETAMIN. Plus σ*² fixed.
- **Gaussian noise** (reader A1 via S1): **NECESSARY-FOR-ROUTE**. It enters [P1] lem:num (needs the true density) and every χ² law (AM:14: "open … Not probed"; `sharpness.tsv:193` "NONE"). No counterexample. MISR N3(i) shows no deterioration at t₃ (W3-MISR AM:15), which hints at ARTEFACT for the conclusion. Keeps `improvable`.
- **p ≤ n^A** (A1 via S2): **NECESSARY-FOR-ROUTE**. `sharpness.tsv:202`: "NECESSARY-FOR-ROUTE … open (technique); enters via j0 and (C8) rate; E3/Prop D barrier concerns the size-tail technique only". `sharpness.tsv:2` (TH09): "ARTEFACT … p<=n^A comes from the prior and proof technique, e^{Cn^alpha} OPEN". An extension to log p = o(n^{1/3}) costs beta-min (AM:117-122).
- **s₀ fixed** (A2): **NECESSARY** in bounded form, for the stated rate. On every design, rate r_n forces s₀ = O(√log n) (Cor B, B2). On witness designs with log p ≍ log n, which satisfy all of Thm 1's other hypotheses (Remark A3), it forces s₀ = O(1) (Cor A2). Sources: `W3-PSHARP/STATEMENT.md:75-77, 79-88, 99-107`; "PROVED-CHECKED…" (`claims.tsv:409-410`). Registry `sharpness.tsv:201` still reads "NONE … open for Theorem 1" (recorder update).
- **σ*² fixed** (S1): **ARTEFACT**. Removable in SNR form by the scale invariance of the coded posterior: MISR Lemma R′, `sharp1/TRIAGE.md:59-61` ("Theorem 1 itself holds with n-dependent σ*² in SNR form"), `sharp2/TRIAGE.md` §3 item 2.
- **(E)** (A3 ⇒ (E) by B1.1): **NECESSARY in some form** (numerical, finite n). Fixed M is **ARTEFACT** (AM:15 "improvable to sub-linear growth? open"; `sharpness.tsv:194` "NONE"; f15 (a) suggests M_n ≍ log p). The evidence is MISR N5 (W3-MISR AM:17): p = 2 orthogonal, v = 1, θ₁ = n, θ₂² = 200 log n/n gives Eπ(S₀) = 0.87 → 0.003 for n = 100…102400. My reading is that this arm meets the floors and BM(200) > c₀(2,1) = 192 (`W3-MISR/CHECKPOINT_3.md:33`), so it is a numerical counterexample to Thm 1 without (E). **Lead to confirm the scale.**
- **(F_λ)** (A4 by B1.2): the anchored part is **NECESSARY** at the beta-min scale (numerical E4; `sharpness.tsv:196` "FAILED-REMOVAL"). The part off S₀ is **ARTEFACT** (E3, `sharpness.tsv:195` "WEAKENABLE"). W3-POST2:E removes it, status "PROVED (by this seat, unchecked)" (`W3-POST2/REPORT.md:151-154`).
- **(F_w)** (A5 by B1.3): **ARTEFACT**. Evidence: E2 (`sharpness.tsv:197` "WEAKENABLE … numerics, not proved"). W3-POST2:A1 replaces it by (OS), status "PROVED (by this seat, unchecked)". The unweighted feasible part of (OS) is necessary (`sharpness.tsv:218`; `W3-POST2/REPORT.md:147`).
- **(BM)** (A6): the order is **NECESSARY**. Evidence: numerical E1 plus the deletion heuristic (`sharpness.tsv:198` "FAILED-REMOVAL"); without beta-min, specificity fails (E5, `sharpness.tsv:199` "FAILED-REMOVAL"). The constant c₀ is **ARTEFACT** (`sharpness.tsv:200` "ARTEFACT … order necessary by numerics, constant improvable"; `:3` "WEAKENABLE").

### better
Verdict: `API_AUDIT/sharp1/results/f15.md:80` "SHARP W3-POST:Thm-1 VERDICT=IMPROVABLE-EASY" (`sharp1/VERDICTS.tsv:18`).
Triage `sharp1/TRIAGE.md:42`, class **B (A residual)**:
- (F_w) → DG/OS, (F_λ) → margin, and the expectation rate / uniformity are already done by W3-POST2:A1/E/C (unchecked).
- The beta-min constant is POST2 open item 2.
- "(E) with M_n ≍ log p: unclear"; asymmetric PIP bound "real, low value": no ticket.
- Residual A went to **T3 POST-SHARP** (`sharp1/TRIAGE.md:72-80`), which became ticket **W3-PSHARP**, launched in `HQ_DECISIONS.md:152-154` and now PROVED-CHECKED (row 1.3).
- f15 route 2 (an upper rate √((1+log p)/n)) is recorded as open: "Not settled: an upper bound of order √((1 ∨ log p)/n) when log p = o(log n)" (`W3-PSHARP/STATEMENT.md:88`).
- No `better-proposal` labels in `claims.tsv:344` (recorder).

**GATES row 1.1: lit=PASS necessity=PASS better=PASS**

---

## Row 1.2 — Thm 2, random Gaussian design · master `W2-APP:POST@1.0.1` (+ `W3-POST:Thm-1` item 6)

Status "PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied" (`claims.tsv:153`). Registry gates:
"lit:PARTIAL(Theory_work/Wave2/W2-UNI/STATEMENT.md:76-80); necessity:PENDING; better:PENDING".

### lit
W2-APP has no ASSUMPTION_MAP and no literature section; the random-design comparison is `W3-POST/ASSUMPTION_MAP.md:47-61`
(POST-LSF, POST-GR). The registry lit pointer `W2-UNI/STATEMENT.md:76-80` is a mildness paragraph only.

| item | ours (`L1_POST.md:8-35`) | Song–Liang Thm 2 (random design) | vs SL | closest BVS | vs closest |
|---|---|---|---|---|---|
| design law | iid N(m,Σ_n) rows, arbitrary means | ν_x with Cond. 1 exponential moments; verified for zero-mean, unit-variance Gaussian processes (AM:47-51) | **incomparable**: ours requires Gaussian rows; ours allows arbitrary means (AM:49-51) | NH14, YWJ16 and CSHvdV15 are fixed-design results (W3-POST AM:71-100); SL is the only random-design comparator in the files | — |
| identifiability | LSF: fixed floor on (s₀+j₀)-sets, ψ_n ≫ (log n)^{3/2}/√n on O(log n)-sets; no λ_max (`L1_POST.md:23-25, 72-77`) | Cond. 3; for Gaussian predictors implied by variance ≻ ε_n² (AM:54-57) | **incomparable** | — | — |
| dimension | p ≤ n^A, p ≥ 2 | P_n ≻ n^θ, P_n < exp(Cn^α) (map:10-12, 18) | **weaker** range; domains differ (map:10-12) | — | — |
| coefficients | fixed s₀, \|β_j\| ∈ [b_lo, b_hi] | strict sparsity (4), r_n ≻ 1 | incomparable | — | — |
| conclusion | Thm 1's three displays under the joint law | Hellinger contraction, exponential form; sure screening (map:17, 20) | **stronger** on selection, weaker in kind: **incomparable** | — | — |

**literature dominance: NO.** SL Thm 2 does not give selection; its prior conditions fail for the coded cap (row 1.1).

### necessity
Hypotheses as in `claims.tsv:153`: A:LSF; A:IID-GAUSS-ROWS; A:P-POLY; A:FIXED-S0; A:GAUSS-NOISE; A:COEF-BOUNDED. All six
read "NONE … no necessity evidence recorded for this pair" (`sharpness.tsv:9-14`), so a recorder update is needed.
- **LSF(i)** (reader A3): the anchored part is **NECESSARY-FOR-ROUTE** for the sample anchored floors (`L1_POST.md:78-82`, Remark 2: "Nothing is claimed necessary for posterior consistency itself"). At posterior level it is necessary numerically (W3-POST E4, AM:18). Quantifying over **all** sets is **ARTEFACT** (R02 example `L1_POST.md:80-81`; f06 item 2 → POST2:E, `sharp1/TRIAGE.md:37`).
- **LSF(ii)** (reader A3; the reader uses a constant floor, stronger than the master): **ARTEFACT**. The Weyl/entrywise step is crude (W3-POST AM:24); a Wishart bound nψ_n > C suffices (f06 item 1; `sharp1/TRIAGE.md:86-88`, T5, B\*).
- **Gaussian rows** (setting): **ARTEFACT**. They are used only for the entrywise event (`L1_POST.md:83-84`, Remark 3; W3-POST AM:25 "improvable (sub-Gaussian rows: Bernstein …)"; f06 item 4; T5 B\*).
- **p ≤ n^A** (A1): **NECESSARY-FOR-ROUTE**. It enters m̄_n (`L1_POST.md:37-42`) and T03♯ (as row 1.1).
- **s₀ fixed** (A2): **NECESSARY** in bounded form for the rate. Witness (ii) of PSHARP Remark A3 is an iid N(0,1)-row design (`W3-PSHARP/STATEMENT.md:79-88`), and on it Cor A2 (`:75-77`) forces s₀ = O(1) when log p ≍ log n.
- **Gaussian noise** (A1): **NECESSARY-FOR-ROUTE**, as row 1.1.
- **coefficient bounds** (A2):
  - b_hi enters (E) (`L1_POST.md:55-56`), so it is **NECESSARY in some form**, as row 1.1 (E).
  - A fixed b_lo is **ARTEFACT**: BM(c) at √(log n/n) suffices (f06 item 3 = BM(c) in W3-POST; `sharp1/TRIAGE.md:37`).
  - The order of the beta-min is NECESSARY, as row 1.1.
  - `sharpness.tsv:14` note: "R01: the inclusion clause is a WEAKER conclusion, not a weakening of beta-min".

### better
Verdict: `sharp1/results/f06.md:73` "SHARP W2-APP:POST VERDICT=IMPROVABLE-EASY" (`sharp1/VERDICTS.tsv:9`).
Triage `sharp1/TRIAGE.md:37`, class **B (B\* residual)**:
- As a posterior theorem it is superseded by W3-POST:Thm-1 item 6 / Cor 1R and W3-POST2. Anchored sets = POST2:E; θ_lo → 0 = BM(c); uniform statement and expectation rate = POST2:C.
- Items 1 and 4 (Wishart bound; sub-Gaussian rows) are "known and undone" and went to **T5 Corollary 1R v2** (`sharp1/TRIAGE.md:86-88`, "Lowest priority").
- T5 was not launched (`HQ_DECISIONS.md:152-154` launched T1 and T3 only).

The reader version is unaffected except through Gaussian rows. The separate correctness item is the queued Sol line check of `W2-APP:POST@1.0.1` (`HQ_NOW.md:33-35`).

**GATES row 1.2: lit=PASS necessity=PASS better=PASS**

---

## Row 1.3 — Thm 3, the rate cannot be improved · masters `W3-PSHARP:B@1.0.0`, `W3-PSHARP:A@1.0.0`

Both statuses: "PROVED-CHECKED; council R2, MANIFEST 4513e05a…, sol=9.2 PASS, opus=9.3 PASS; …" (`claims.tsv:409-410`).
Registry gates: A "better-proposal:P2(reviews/K01_break_astra.md) ; better-disposition:P2=adopted(reviews/K01_disposition.md)";
B: P1 adopted (same files).

### lit
| item | ours | Song–Liang 2015 | vs SL | closest BVS | vs closest |
|---|---|---|---|---|---|
| object | lower bounds on 1−π(S₀) for the coded prior: (a) design- and data-free; (b) on witness null blocks | no lower bound (upper bounds only, map:16-22) | **stronger** (new kind of result) | YWJ16: upper bound 1−π = O(p⁻¹) for a p^{−κ\|γ\|} prior; CSHvdV15: prior decay p^{−A₄} per variable (as quoted in `sharp1/results/f17.md`, not re-read; PSHARP AM:33-35) | **incomparable**: different priors, and upper rather than lower bounds |
| hypotheses (a) | none beyond \|S\| ≤ min(K−1, p/2) | — | — | — | — |
| hypotheses (b) | Gaussian noise; (E), (C); orthogonal or spherical/Gaussian null block; p → ∞ | — | — | "No published lower bound for this target is known to us; nothing here is dominated" (PSHARP AM:35-36); f02 agrees: comparators make the per-variable penalty grow polynomially in p, unlike the coded prior | — |
| relation to minimax | — | — | — | Wainwright 2009 information-theoretic beta-min limits (cited in W3-POST AM:104-106 as recalled there) bound the signal, not the posterior mass | incomparable |

**literature dominance: NO.**

### necessity
These are sharpness records, so the question is whether the record survives without each hypothesis (PSHARP AM:4-5).

**Corollary B**
- **s₀ ≤ K−1** (A:EXT-FEAS; reader (a) \|S\| ≤ K−1): **NECESSARY**. `sharpness.tsv:231` "NECESSARY"; counterexample `W3-POST/numerics/lb_domain_out.txt` (PSHARP AM:9); RV:218 gives the example S = [p], p = 2.
- **s₀ ≤ p/2** (reader (a)): **ARTEFACT** (cosmetic: it only fixes the constant 1/3; c(p,s₀) is stated exactly, AM:10).

**Proposition A** (reader (b))
- **Gaussian noise** (A:GAUSS-NOISE): **NECESSARY-FOR-ROUTE**. `sharpness.tsv:230` "NECESSARY-FOR-ROUTE" (AM:11: "the constant is noise-specific"). sharp2 f02 (a) shows this holds for (W-orth) only; under (W-sph), mean-zero noise with a finite fourth moment suffices. Triage class B (park), `sharp2/TRIAGE.md:43`. Recorder: qualify `:230`.
- **(E), (C)** (A:ENERGY, A:PSHARP-COEF; reader ‖Xθ*‖² ≤ nM, ‖θ*‖² ≤ nM′): **ARTEFACT**. `sharpness.tsv:228-229` "WEAKENABLE": (M+M′) log N = o(n) suffices (AM:12; f02 agrees).
- **witness block** (A:PSHARP-WORTH / A:PSHARP-WSPH; reader N-orth / N-gauss):
  - Some null-block condition is **NECESSARY** for the in-probability log factor. Duplicated null columns give "No uniform √(log p) gain under G in probability" (f02, Claim B (b)). Equicorrelated nulls lose it in one-step numerics; full-posterior failure is "not established" [K01-F2] (AM:13).
  - Exact orthogonality is **ARTEFACT**: coherence o(1/log N) suffices (f02; triage B park).
  - No `sharpness.tsv` row exists for these.
- **N_n → ∞** (reader p → ∞): **NECESSARY** for the in-probability log factor (AM:15; f02 agrees). It is not needed for the expectation bound (f02 (b), rider T12).
- **(log N)² = o(n)** (reader p ≤ n^A in N-gauss): **ARTEFACT** (a threshold of the route; AM:16).
- **(r₀+1) log N = o(n)**: **ARTEFACT** (single-use bound, AM:17).

### better
Verdicts: `sharp2/results/f02.md:71-72`, "SHARP W3-PSHARP:A VERDICT=IMPROVABLE-EASY" and "SHARP W3-PSHARP:B VERDICT=SHARP"
(`sharp2/VERDICTS.tsv:8-9`).
- **A → class A1** (`sharp2/TRIAGE.md:43`): the expectation lower bound holds for every p, with constant √((a+½)/π), plus e^λ − 1 at the critical scale. Ticket: rider **T12 PSHARP-E** (`sharp2/TRIAGE.md:80`; `HQ_NOW.md:27-28`), recorded as RV row thm3 "Pending delta PSHARP Cor A1 (rider T12…)" (RV:196). Dropping G under (W-sph) and the coherence witness: **B (park)**.
- **B: SHARP, "Agreed"** (`sharp2/TRIAGE.md:44`).
- In-ticket better review K01: P1 and P2 adopted (`claims.tsv:409-410` gates).

When T12 lands, Thm 3(b) gets STRONGER (expectation, every p). Update RV §3 then.

**GATES row 1.3: lit=PASS necessity=PASS better=PASS** (A1 proposal adopted, rider T12 pending)

---

## Row 1.4 — Thm 4, omitted variables (was card 3.4) · master `W3-MISR:Cor-G(b)@1.0.0`

Status "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:Prop-P, SOP:TH09,
SOP:TH128, C-MIS:GDb; input versions …; council R2, MANIFEST 217d6708…, sol=9.2 PASS, opus=8.9 PASS; …"
(`claims.tsv:417`). The registry gates hold only `correct:PASS(...)`.

### lit
| item | ours (`W3-MISR/STATEMENT.md:164-174`) | Song–Liang Thm 4 / Cor 2 | vs SL | closest BVS | vs closest |
|---|---|---|---|---|---|
| law | jointly Gaussian rows (candidates, omitted); Gaussian ε | iid-row Gaussian linear model, misspecified subset (MISR AM:43-47) | **weaker** (narrower law: "narrower law (Gaussian contrast residual with scalar covariance…)", AM:46-47) | NH14, YWJ16, CSHvdV15 are well-specified only (AM:48-50) | n/a |
| dimension, sparsity | 2 ≤ p_𝒞 ≤ n^A growing; s fixed | fixed subset s (map:25) | **stronger** (growing candidate set) | — | — |
| variance | any n-dependence of σ², τ² (Cor-G(a)) | — | **stronger** (no fixed τ², `W3-MISR/REPORT.md:71-73`) | — | — |
| prior | shipped prior (BB cap, g = n) | Gaussian/IG with positive mass on every subset (map:25); Cor 2 withdrawn under a binding cap (map:26) | **stronger** (binding cap covered) | — | — |
| conclusion | E[1−π(S₀^𝒞)] = O(√(log n/n)); P(HPM ≠ S₀^𝒞) = O(√(log n/n)) | Thm 4: Hellinger consistency around the KL projection, a.s.; Cor 2: π(s̃ ⊆ ξ) → 1, screening (map:25-26) | **stronger** on selection; SL stronger in mode (a.s., integrated). Overall **incomparable** (AM:43-47) | Rossell 2022 / Rossell–Rubio 2018 (misspecified BVS selection) **(recalled, not re-read)**: compared in **no file** | **OPEN** |

**literature dominance: NO** among the compared results. There is an **OPEN** comparison: Rossell's misspecification results
were never checked, and the input SOP:TH128 is already labelled "modest extension of Rossell 2022" (`claims.tsv:14`).

### necessity
Registry assumptions `claims.tsv:417`: A:IID-GAUSS-ROWS; A:FIXED-S0; A:P-POLY. The rest come from STATEMENT:171-173.
There are no `sharpness.tsv` rows for Cor-G(b); the MIS(i) rows `sharpness.tsv:233-235` cover the inherited chain.
- **Joint Gaussian rows** (setting; reader A-setting):
  - **(i) Omitted part Gaussian given the candidates, with scalar covariance (GR^c).**
    - Scalar covariance is **NECESSARY** for the mean-only target. The C-MIS E2 counterexample (a common random slope; N3(iii) Eπ({0}) → 0.02) is in MISR AM:15. It is not necessary under (PR) [SW1-2].
    - Gaussianity of the residual is **ARTEFACT** (t₃, N3(i), AM:15; `sharpness.tsv:235` MIS(i) A:MISR-GRC "WEAKENABLE").
    - The minimal form is the Cor-G(a) restatement (sharp2 f00, class A1, T13).
  - **(ii) Gaussian candidate rows**: **ARTEFACT**. They are used only for concentration (f01 (a)); sub-Gaussian rows are class B (`sharp2/TRIAGE.md:41`).
- **σ²_𝒞 > 0** (reader definition): **NECESSARY-FOR-ROUTE**. The reduction standardises by √v (MISR AM:15-16, Lemma R′).
- **s fixed** (A1): **NECESSARY** in bounded form for the rate. Cor B is design-free and so applies to the candidate run (`W3-PSHARP/STATEMENT.md:90-107`); `sharp2/TRIAGE.md:37` says the matching lower bound is PSHARP's.
- **p_𝒞 ≤ n^A** (A1): **NECESSARY-FOR-ROUTE** (inherited; MISR AM:22 "inherited (hard)").
- **floor λ_min(Σ_TT) ≥ c_pop with max Σ_jj ≤ C₀** (A2):
  - The anchored part is **NECESSARY** at the beta-min scale (inherited, W3-POST E4).
  - The covariance-scale form is **ARTEFACT**: a correlation-matrix floor suffices, since only c_pop/C₀ enters (f01 (a); class A2, `sharp2/TRIAGE.md:41`).
  - Non-anchored sets are **ARTEFACT** (f01: a sufficient route to (OS)).
- **energy β^𝒞ᵀΣβ^𝒞 ≤ M₀σ²_𝒞** (A3): **NECESSARY in some form**. MISR AM:17: "**cannot be dropped** (BT1 "Limits", confirmed by N5 …)". Bounded M₀ is **ARTEFACT**: "weakenable, not removable" (N4, AM:17), and f01 suggests M_n may grow slowly (upstream).
- **relative beta-min → ∞** (A3):
  - The order is **NECESSARY**: N2, "the margin must be **relative to v**" (AM:20); f01: "the order … cannot be lowered for this method".
  - "→ ∞" is **ARTEFACT**: liminf ρ^{BM} > 2c₀/φ₀² suffices (f01; class A2).
  - The constant is **ARTEFACT** (`sharpness.tsv:234` MIS(i) A:MISR-IDM-SNR "ARTEFACT").

### better
Verdict: `sharp2/results/f01.md:108` "SHARP W3-MISR:Cor-G(b) VERDICT=IMPROVABLE-EASY" (`sharp2/VERDICTS.tsv:6`).
- Triage `sharp2/TRIAGE.md:41`, class **A2**: liminf beta-min, correlation floor, explicit uniform bound. "It is an example corollary: low value." These go into rider **T13 MISR-G/H** as "Cor-G(b) cosmetics (A2)" (`sharp2/TRIAGE.md:81`; `HQ_NOW.md:29`), recorded as RV row thm4 "Pending delta MISR Cor-G(a)/Cor-H (rider T13…)" (RV:253).
- Sub-Gaussian candidate rows: B.
- HPM rate (n log n)^{−1/2} and growing M₀: upstream POST2, class B (`sharp2/TRIAGE.md:37`, MIS(i) row).
- In-ticket blind better review BT1 (astra) dispositioned: `W3-MISR/reviews/BT1_disposition.md:7-12`.

**GATES row 1.4: lit=OPEN(Rossell 2022 / Rossell–Rubio 2018 misspecified-selection results not compared in any file; input TH128 labelled "modest extension of Rossell 2022") necessity=PASS better=PASS**

---

## Row 3.7 — Thm 8, certified screening · master `W3-SCR:A1@1.0.0`

Status "PROVED-CHECKED" (`claims.tsv:401`). Registry gates: "lit:PENDING; necessity:PENDING; better:PENDING".

### lit
W3-SCR has **no literature section**. Its REPORT relates A1 only to project results (`W3-SCR/REPORT.md:150-155`).

| item | ours (`W3-SCR/STATEMENT.md:158-163`) | Song–Liang 2015 | vs SL | closest BVS / screening | vs closest |
|---|---|---|---|---|---|
| object | certified local optima of the coded score F (the search output) | posterior PIP sure screening (Thm 3); SAM's algorithmic screening via Cond. 5 with no theorem (map:20, 27) | **incomparable** (algorithm output vs posterior) | none in the ticket files. Natural comparators: SIS (Fan–Lv 2008); support guarantees for local optima of L0 / best-subset local search **(recalled, not re-read)** | **OPEN** |
| design | directional floor κ on \|T\| ≤ q_n (+s₀) only; null-null correlations free | Thm 2 conditions + identifiability (map:20) | incomparable | — | — |
| dimension | only log p enters; p ≤ n^A not needed (AM:24) | P_n < exp(Cn^α) | incomparable (budget (q_n+1) log p + log n ≤ c₁n) | — | — |
| conclusion | P(output, certified, \|Ŝ\| ≤ q_n, S₀ ⊄ Ŝ) → 0: one-sided | P*[π(t ∈ ξ \| D_n) < 1 − e^{−c₁nε²}] < e^{−c₁nε²} per true predictor; sensitivity only (map:20) | incomparable; both are sensitivity-only | — | — |

**literature dominance: NO** found, but the screening / local-optimum literature is unchecked (**OPEN**).

### necessity
Registry assumptions `claims.tsv:401`: A:GAUSS-NOISE; A:EX-A; A:SCR-DF; A:SCR-A1-COND.
- **Gaussian noise** (S1): **ARTEFACT**. W3-SCR AM:28: "Sub-Gaussian errors would give analogous statements with other constants (not proved here) … `improvable` (not pursued…)".
- **EX-A** (S3): **NECESSARY-FOR-ROUTE**. It is the named idealisation that identifies coded comparisons with exact ones (AM:29); it is not a data hypothesis.
- **directional floor κ** (A:SCR-DF; reader A1 is a full floor, stronger): **ARTEFACT** as a bridge. `sharpness.tsv:226`: "NONE … ID/DF/AF/NF are sufficient, not shown necessary". The hypothesis actually consumed is visibility, which is sharp at q = 0 with constant 1 (SCR-N, "PROVED-CHECKED", `claims.tsv:407`; `sharpness.tsv:225` "NECESSARY" for SCR-A). Some identifiability is **NECESSARY** numerically: `twin999` and `masked` give 10/10 draws with a sparse LO model missing a truth (AM:18). The full floor of the reader version is not needed (`noisecs98` 0/10, AM:19).
- **fixed signals θ_min ≥ b, ‖θ*‖₁ ≤ M** (A2): **ARTEFACT**. A1° ("PROVED-CHECKED", `claims.tsv:402`) has beta-min at σκ⁻¹√(𝐋_n/n) (AM:21; `STATEMENT.md:165-169`). A1° is incomparable rather than strictly stronger, because it adds ‖μ‖ = o(nσ) and ‖θ*‖₂/θ_min. ‖θ*‖₁ control is **NECESSARY-FOR-ROUTE** for the ID bridge (AM:18, "Not sufficient without ‖θ*‖₁ control (SCR-N Consequence 2)").
- **budget (q_n+1) log p + log n ≤ c₁n** (A:SCR-A1-COND; A3): **ARTEFACT**. SCR-M replaces the model-count entropy by a Gaussian width (AM:16), and c₁ is a proof constant. A lower bound for q ≥ 1 is **open** (AM:16, 41).
- **q_n ≤ K−1** (A3): **NECESSARY-FOR-ROUTE** (AM:22: "(i) needed for the addition argument; otherwise open").
- p ≤ n^A and s₀ fixed are not hypotheses of A1 (AM:24-25).

### better
**better: PENDING (SHARP3).**
- sharp1 f21: "STOP=max_tokens" (`sharp1/VERDICTS.tsv:24`).
- sharp1b f21: "STOP=max_tokens", no text (`sharp1b/VERDICTS.tsv:16`; `sharp1b/TRIAGE.md:83-86`).
- Requested as g04 in `SHARP3_REQUEST.md:29`.
- In-ticket evidence only (not a blind API verdict): R02 better-theorem review (astra, 2026-11-09, on STATEMENT v2), "Strictly better provable statements exist" (`W3-SCR/reviews/R02_better_theorem_astra.md:7`). Its proposals 1–5 were adopted (W3-SCR AM:32-37, 45); proposal 6 was not adopted (AM:41-42).

**GATES row 3.7: lit=OPEN(no literature comparison in W3-SCR; screening / L0-local-optimum literature unchecked) necessity=PASS better=PENDING (SHARP3)**

---

## Staged lines (for the lead's `gates_staged.tsv`; id | lit | necessity | better | better-proposals | refs)
```
W3-POST:Thm-1 | PASS | PASS | PASS | f15: B (POST2:A1/E/C), A-residual→T3=W3-PSHARP (done) | GATES_G1 §1.1; sharp1/TRIAGE.md:42
W2-APP:POST | PASS | PASS | PASS | f06: B, B*→T5 (not launched) | GATES_G1 §1.2; sharp1/TRIAGE.md:37,86-88
W3-PSHARP:A | PASS | PASS | PASS | f02: A1→T12 (pending); G under W-sph, coherence: B park | sharp2/TRIAGE.md:43,80
W3-PSHARP:B | PASS | PASS | PASS | f02: SHARP (agreed) | sharp2/TRIAGE.md:44
W3-MISR:Cor-G(b) | OPEN(Rossell) | PASS | PASS | f01: A2→T13 (pending); sub-Gaussian rows B | sharp2/TRIAGE.md:41,81
W3-SCR:A1 | OPEN(no lit section) | PASS | PENDING(SHARP3) | — | SHARP3_REQUEST.md:29
```
