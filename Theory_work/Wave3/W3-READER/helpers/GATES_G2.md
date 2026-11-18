# GATES_G2 — strength gates (LIFECYCLE §4.2) for card rows 3.1, 3.2, 3.3, 3.5, 3.6 (helper G2, W3-READER leg 2)

Helper G2 (Claude Opus 5.5, effort high), 2026-11-15. Read-only on everything except this file; no new proofs, no
subagents. Task: `BRIEF_LEG2_GATES.md`; gate definitions `Theory_work/INFRA/LIFECYCLE.md:360-375`; rows and reader
statements `CLAIMS_CARD.md:43-48`, `READER_VERSIONS.md` §5–§7. Paths below are relative to `Theory_work/` unless they
start with `Papers/` (= `/home/fb31/Bayesian-Variable-Selection/Papers/Core_bibliography/`, the PDFs are not in this
worktree). Statuses are verbatim from `INFRA/registry/claims.tsv` (council suffixes cut after the first clause, "…",
as on the card).

**Conventions.** *lit* verdicts are from the side of our result: **STRONGER** = ours has a weaker hypothesis, a
stronger conclusion or a wider scope on that item; **WEAKER** = the reverse; **INCOMPARABLE**; **EQUAL**. "(re-read)" =
checked in the PDF text for this file (page numbers are journal/arXiv page numbers); "(recalled, not re-read)" = from
memory or quoted from a reviewer's memory, not checked. Yang–Wainwright–Jordan (2016) and Del Moral (1996/2004) are not
in the bibliography folder; their content is taken from papers that state it (Zhou et al. 2022 for YWJ; Dau–Chopin 2022
for Del Moral), marked accordingly. *necessity* verdicts: NECESSARY (counterexample) / NECESSARY-FOR-ROUTE /
ARTEFACT (improvable) / OPEN; registry verdicts from `INFRA/registry/sharpness.tsv` quoted as `tsv:<line>`.

## Flags (top)

**SUB-PAR SIGNAL: none.** No literature dominance found on any of the five rows; every easy strengthening that a blind
verdict proposed for rows 3.1–3.5 has a recorded triage disposition. Row 3.6 has no complete blind verdict (better
PENDING, SHARP3 g00–g03) and an OPEN necessity item; neither is a sub-par reason.

Cautions for the lead (not sub-par):
1. **Row 3.5 is the classical SMC identity, instantiated for the code.** Mathematically N1 is Del Moral's unbiasedness
   of SMC normalising-constant estimates plus a code bridge and a freezing lemma (`Wave1/W1-N1/lemmas/R_remarks.md:7-10`;
   blind reviewer: "N1 matches it", `Wave3/API_AUDIT/sharp1/results/f01.md` §(b) "Literature"). Not dominance (no
   published result is about the coded fields), but the reader version and the card's "Buys" column must credit
   Del Moral and present the contribution as "for the method as coded, calibration included".
2. **Registry overstatement, row 3.6.** `tsv:208` records `W3-SAMP:LT# / P:POST-CONC = NECESSARY`, but its own source
   says the attained κ₀ term "is sharpness of the bound, not a proof that consistent RB PIPs require κ₀ → 0 (SW1 #7)"
   (`Wave3/W3-SAMP/ASSUMPTION_MAP.md:16`). Read as NECESSARY-FOR-ROUTE below; suggest the recorder correct the row.
3. **Pending riders change the reader hypotheses of rows 3.2 and 3.3** (already marked "Pending delta" in
   `READER_VERSIONS.md` §5, §7 headers): T4 weakens (A1)'s strong-signal/BM-∞ and (A3)'s M_n → ∞ in Theorem 7
   (`Wave3/API_AUDIT/sharp2/TRIAGE.md:45,112`); T10 changes Theorem 5's Gaussian-row rate at C_L = 0 (`:57,65,110`).
4. **RM2's own better-gate is still PENDING in the registry** (`gates … better:PENDING(reviews/BT1_better_theorem_astra.md)`
   on RM2-F/RM2-R): BT2 proposals P1–P5, P7 are "ADOPT in v1.5" by the lead, "HQ decides at CP3"
   (`Wave3/W3-RM2/reviews/BT2_disposition.md:11-17,19-27`). The blind API verdict (sharp2 f03) used for the better gate
   below is separate from BT1/BT2.

---

## Row 3.1 — Main theorem (reported model, Gaussian rows) — `READER_VERSIONS.md` §6

Masters: `W3-RM2:RM2-R@1.0.0` (`Wave3/W3-RM2/STATEMENT.md:216-218`, hypotheses :172-202) "PROVED-CHECKED, conditional
on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, …"; `W3-RM:RM-0@1.0.0` (`Wave3/W3-RM/STATEMENT.md:160-176`)
"PROVED-CHECKED"; `W2-UNI:F-UNI@1.1.0` (`Wave2/W2-UNI/lemmas/L5_delivery.md:15-21`) "PROVED-CHECKED". Registry gates
now: RM2-R `lit:PENDING(ASSUMPTION_MAP.md) ; necessity:PENDING(SHARPNESS.md) ; better:PENDING(…BT1…)`; RM-0
`lit:PENDING; necessity:PENDING; better:PENDING`; F-UNI `lit:PARTIAL(Theory_work/Wave2/W2-UNI/STATEMENT.md:76-80);
necessity:PENDING; better:PENDING`.

### 3.1 lit

| item | ours (master) | Song–Liang (2015, JRSS-B 77(5)) | vs S–L | closest implementation-level result | vs it |
|---|---|---|---|---|---|
| object of the conclusion | the coded method's **reported model** = S₀ on one data event for every admissible output run, seed and calibration outcome (RM2 :206-218, RM-0 :160-176); P(Ŝ = S₀) → 1 under delivery conventions (F-UNI L5:15-21) | exact posterior only; for the sampler: "it follows from the theory … in Section 2 that the SAM approach will lead to a consistent selection" (§3.1, p. 959, re-read) and SAMC is run with no theorem on its output (§3.2, p. 959, re-read); SONG_LIANG_MAP row 7 (`Wave1C/C-PACK/SONG_LIANG_MAP.md:22`) | STRONGER (object S–L does not address) | YWJ 2016 / Zhou et al. 2022 Thm 1: mixing time of RW-MH / LIT-MH, T_mix ≤ 800 max(nκ₁/c₁, 3s₀) for TV ≤ ¼ (Zhou p. 14, re-read; YWJ bound quoted there, p. 15) | INCOMPARABLE: law of a chain after T_mix steps vs pathwise output of the SMC + LS0 route (`Wave3/W3-RM2/ASSUMPTION_MAP.md:83-92`) |
| dimension | p ≤ n^A, p ≫ n (S2) | P_n < exp(Cn^α) (Cor 1, p. 954) and P_n/n^θ → ∞ (§2.1, p. 950) (`SONG_LIANG_MAP.md:10-12,18`) | WEAKER | Zhou: n = O(p), s₀ log p = O(n) (p. 14, re-read) | WEAKER |
| sparsity | s₀ fixed | r_n may grow (Cor 1 branches, p. 954; map :18) | WEAKER | s₀ may grow with n (Zhou p. 8, re-read) | WEAKER |
| prior | shipped: capped BB(1, p), g = n, IG noise; no tuning (`CLAIMS_CARD.md:12-15`) | λ_n = r_n/P_n → 0, cap r̄_n, V_ξ ≻ 0 (map :7-9; S–L p. 950) | INCOMPARABLE (ours untuned, theirs tuned to the theorem) | π₀(γ) ∝ p^{−κ₀\|γ\|}, 1 + g = p^{2κ₁}, κ = O(s₀) (Zhou eq. (3), pp. 6–7; p. 14) | INCOMPARABLE: their size penalty is chosen large enough to absorb the landscape condition; ours carries the fixed prior's exact constant (RM2 AM:86-91) |
| design | Gaussian rows; population floor on O(log n)-sets and on Q ∪ {l} (reader (A5)) | Thm 1 bounded predictors; Thm 2 Condition 1 (exponential moment) + identifiability Condition 3 (map :16-17,24) | INCOMPARABLE ("descriptively and without an ordering of assumption classes", `Wave2/W2-UNI/REPORT.md:140-141`) | fixed design; RE-type conditions behind Condition 1 (Zhou pp. 8–9, re-read) | INCOMPARABLE |
| signals | θ_lo ≤ \|θ*_j\| ≤ θ_hi fixed (reader (A2)) | through Condition 3 and ε_n (map :24) | INCOMPARABLE | β_min at a constant multiple of σ² log p/n, growing s₀ (YWJ; quoted by the blind reviewer, `API_AUDIT/sharp2/results/f03.md:43-47`; recalled, not re-read) | WEAKER |
| search / landscape conditions | visibility (A3), polynomial leakage set with locality (A4), local regressions (A6) ⇒ width (W-R) | none (posterior-only theorem) | WEAKER (extra hypotheses: the price of an algorithmic conclusion) | Condition 1 = add/delete/swap unimodality, proved in YWJ Lemma 4 under RE, β-min and the sparse projection condition (Zhou p. 8, re-read) | INCOMPARABLE: (W) is the same kind of object as the sparse projection condition, restricted to the lattice [S₀, Q], with a converse (W-conv) (RM2 AM:83-92) |
| rate | none claimed for the reported-model event (registry `rate: none claimed`) | exponential outer and inner rates for Hellinger contraction (Thms 1–2, pp. 952–953; map :16-17) | WEAKER (rate) | computational: T_mix bound (above) | INCOMPARABLE: ours counts LS0 moves only (≤ n^b, RM2 :206-214) |
| SMC on binary spaces | — | — | — | Schäfer–Chopin 2013: adaptive SMC for BVS, computational studies only (abstract, re-read) | STRONGER (no consistency theorem there) |
| informed proposals | — | — | — | Zanella 2020: locally balanced proposals, Peskun optimality (abstract, §3, re-read) | INCOMPARABLE (efficiency ordering, no selection consistency) |

Forward-backward/greedy selection (An et al. 2008, cited at Zhou p. 8; RM2 AM:93-96): path guarantees under RE /
irrepresentable-type conditions, no polynomial set of visible nulls with the BB(1, p) prior (recalled, not re-read).

**literature dominance: NO.**

### 3.1 necessity

| master hypothesis (registry id) | reader carrier (§6) | verdict | evidence |
|---|---|---|---|
| A:LSF = (T1-R) → [POST] | (A5) via B6.1 | ARTEFACT | RM-0 needs only "S₀ is the unique F-maximiser among scored models w.p. → 1" (`Wave3/W3-RM/ASSUMPTION_MAP.md:19-20`; `W3-RM/SHARPNESS.md` §5); proposed as T2(b) (`API_AUDIT/sharp1/TRIAGE.md:64-70`) |
| A:IID-GAUSS-ROWS | setting of §6 | ARTEFACT (scope) | `tsv:96` "WEAKENABLE … setting (E) approximate-Gram fixed design is an alternative to iid rows"; RM2-F is the fixed-design counterpart |
| A:RM-FLR (FL-R): small sets | (A5) | NECESSARY-FOR-ROUTE | block tables must behave like regressions (RM2 AM:24); same toolkit step recorded for the start law: `tsv:236` "W3-START:TK A:START-GF NECESSARY-FOR-ROUTE" (by analogy; no RM2 row) |
| A:RM-FLR: floor on Q ∪ {l} | (A5) | NECESSARY-FOR-ROUTE in kind; level ARTEFACT | lattice directions u_{T,l} are defined only under it (`W3-RM2/STATEMENT.md:140`; `INFRA/registry/assumptions.tsv:13`); fixed level stronger than used, φ_n² ≳ q/n suffices (f03:28-31, constants not re-run); Wishart floors immaterial (sharp2 TRIAGE:46, class C) |
| A:PTV = (V-R) | (A3) | ARTEFACT | `tsv:222` "WEAKENABLE … (V) sufficient; not necessary for masked designs covered by GEN/PXN; conclusion in 296/300 with population visibility zero"; B3: weak truth absent from the start mode in 32/32, LS0 adds it (RM2 AM:26); ticket T7 (`API_AUDIT/sharp1b/TRIAGE.md:66-76`) |
| A:RM2-LFEAS (L-feas) | (A4) "\|Q\| ≤ K and (Q = [p] or K ≥ 2\|Q\|+32s₀+1)" | NECESSARY-FOR-ROUTE | FAC-PK (NEG) is a failing class with saturated start modes — "an existential obstruction for LS0, not a necessity statement" (`W3-RM/ASSUMPTION_MAP.md:31`; RM2 AM:29) |
| A:RM2-LGAIN-R (leak ϖ_n = o(√(log n/n))) | (A4)(i) | ARTEFACT | `tsv:259` "WEAKENABLE … exact scale κ√(log n/n) not derived"; aggregated-leak form plausible (f03:74-78; sharp2 TRIAGE:46 class D) |
| A:RM2-LLOC-R (r_n → 0) | (A4)(ii) | NECESSARY-FOR-ROUTE (kind); rate ARTEFACT | `tsv:260` "NONE … needed by this proof at r_n → 0 only"; "without r_n → 0 … the reduction to deterministic reference sets fails" (RM2 SHARPNESS.md:47-49); "without it the reference count is p^{15}" (f03:84-87); fixed r₀ gives a frontier (same) |
| A:RM2-LSIZE-B-R (\|Q\| ≤ n^b, b < ½) | (A4) | ARTEFACT | `tsv:258` "ARTEFACT … sufficient budget; necessity open"; heuristic boundary k̃ ≈ √n, B1 held 48/48 at b ≥ ½ (RM2 AM:28, :53; SHARPNESS.md:10-24, O1) |
| A:RM2-HSIZE-RHO (\|H_l\| ≤ n^ρ, 15ρ + b < ½) | (A4)(ii) | ARTEFACT | `tsv:257` "ARTEFACT … reference counting"; "artefact of counting reference sets" (SHARPNESS.md:45-49); no cheap improvement seen (f03:89-93; BT2_disposition.md:4-8) |
| A:RM2-W-R (width on the realised design) | (A6) ⇒ (D-loc^b) ⇒ (W-R) (B6.3–B6.4) | NECESSARY-FOR-ROUTE | `tsv:256` "positive diverging gaps obstruct whole-lattice no-addition; bounded gaps undetermined"; W-conv (SHARPNESS.md:51-56); reporting without it = O1 |
| (A6) local regressions (reader form, stronger than (W-R)) | (A6) | ARTEFACT | sufficient form of (W-R); "Not known to be necessary for the conclusion" (`READER_VERSIONS.md` §6 "Why each assumption") |
| s₀ fixed, p ≤ n^A, fixed θ box (inherited from [POST]) | (A1), (A2) | ARTEFACT | "inherited restrictions … not created here" (f03:43-47); RM2 lemmas work with a_n ≥ C√(log n/n), θ_lo² ≫ n^{b−1} + log n/n; binding input is W2-APP:POST (f03:95-99) |
| RM-0: P:SAND, P:NA-TL | through RM2-R's conclusions | NECESSARY-FOR-ROUTE | the RM-0 route is Sand ∩ NA ∩ TL (`W3-RM/ASSUMPTION_MAP.md:8-13`); NA obstructed by W-conv as above |
| RM-0: P:POST-CONC | (A5) via B6.5 | ARTEFACT | as A:LSF (T2(b)) |
| F-UNI (P) E[1 − π(S₀)] → 0 | via [POST] | ARTEFACT | "mode interface → T2(b)" (`API_AUDIT/sharp1/TRIAGE.md:41`) |
| F-UNI (V) input validity, λ_min(Σ_n) > 0 | Σ_n positive definite (§6) | ARTEFACT (cosmetic) | "λ_min(Σ_n) > 0 redundant, cap slack: C" (sharp1 TRIAGE:41) |
| A:OP | (S3) | implementation premise, not a statistical hypothesis | `INFRA/registry/assumptions.tsv:19` |
| A:BLOCK-LE-16 | (S3) ("15 = block size − 1") | implementation premise, not a statistical hypothesis | true of the coded partition (`W3-START/ASSUMPTION_MAP.md:25`) |
| A:DELIVERY-ALLOC (F-UNI) | (S4) | implementation premise, not a statistical hypothesis | route note: `tsv:77` "C-DLV:Prop-F A:DELIVERY-ALLOC NECESSARY-FOR-ROUTE … fallback needed on this route" |
| A:MR1-CAP (F-UNI) | (S4)/(S3) | implementation premise, not a statistical hypothesis | cap a_n = ℓ_n + \|S̃₀\| (`assumptions.tsv:21`); never binding on the good event (RM2 :206-214) |
| A:GRAM-OP-BOUND, A:RELEVANCE-SIZE, A:P-POLY (F-UNI registry list) | — | not used by row 3.1 | (E)-branch only / superseded by \|Q\| ≤ n^b in RM2 / = (S2) |

### 3.1 better

- `W3-RM2:RM2-R`: blind API verdict sharp2 f03, "SHARP W3-RM2:RM2-R VERDICT=IMPROVABLE-EASY"
  (`API_AUDIT/sharp2/VERDICTS.tsv`; `results/f03.md:70-117`). Triage **D (rest B/C)** (`sharp2/TRIAGE.md:46`):
  aggregated leak = D ("needs a proof agent"), recorded as a named open problem with no ticket (`Wave3/HQ_NOW.md:37`
  "Named open problems, no tickets: RM2-R aggregated leak"); κ-frontier = O3′ (B); decaying a_n, θ_lo = W2-APP:POST /
  T5 territory (B); Wishart floors (C).
- `W3-RM:RM-0`: sharp1b f19 "VERDICT=IMPROVABLE-EASY"; triage **B (queued)**: T2(a) delivery, T2(b) unique-mode event,
  new T2(c) down-closed sub-lattice (`sharp1b/TRIAGE.md:18-34,49,78-81`).
- `W2-UNI:F-UNI`: sharp1 f14 "VERDICT=IMPROVABLE-EASY"; triage **B (A residual)**: three-layer restatement = RM-0;
  residuals T2(b), T2(a); λ_min > 0 redundant (C) (`sharp1/TRIAGE.md:41`).
- Rider created: **T2** (RM-0 rider: delivery and mode interface), run with T4 as one Opus leg after RM2's council
  (`Wave3/HQ_NOW.md:70-71`; `HQ_DECISIONS.md:152-154`). If T2 lands, the reader's "if output then S₀" + (S4) becomes
  "P(Ŝ⁺ = S₀) → 1 without 'on output'" (sharp1 TRIAGE:64-70).
- Ticket-internal (not the blind gate): BT2 P1–P5, P7 "ADOPT in v1.5", P6 → O3′ (`W3-RM2/reviews/BT2_disposition.md:19-27`).

GATES row 3.1: lit=PASS necessity=PASS better=PASS

---

## Row 3.2 — Reported model, fixed design — `READER_VERSIONS.md` §7

Masters: `W3-RM2:RM2-F@1.0.0` (`Wave3/W3-RM2/STATEMENT.md:206-214`, hypotheses :126-170) "PROVED-CHECKED, conditional
on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, …"; RM-0 and F-UNI as in 3.1 (input validity "(E) with
nonconstant raw columns"). Registry gates now: `lit:PENDING(ASSUMPTION_MAP.md) ; necessity:PENDING(SHARPNESS.md) ;
better:PENDING(reviews/BT1_better_theorem_astra.md)`.

### 3.2 lit

Rows "object", "prior", "rate", "SMC on binary spaces", "informed proposals" as in 3.1 (same verdicts). Differences:

| item | ours (master) | Song–Liang (2015) | vs S–L | closest implementation-level result | vs it |
|---|---|---|---|---|---|
| design | fixed design; sample-level conditions on (X, θ*): floors on ≤ 16-sets and Q ∪ {l}, visibility δ²_{U,j} ≥ M_n log n, leakage δ²_{U,l} ≤ ητ²_U log n off Q, η < η_A (reader (A2)–(A4)) | random design only (map :7) | INCOMPARABLE (setting) | YWJ/Zhou treat the design as fixed (Zhou p. 9, re-read) | INCOMPARABLE (Condition 1 vs visibility + leakage + (W)) |
| signals | (T1-F) with BM-∞, θ*_min√(n/log n) → ∞; (BM-W) at the truth-removal width (reader (A1), (A5)(b)) | identifiability Condition 3 (map :24) | INCOMPARABLE | β_min at constant × σ² log p/n (YWJ, via f03:43-47; recalled, not re-read) | WEAKER (T4 pending: constant-level (V) and additive (BM-W), sharp2 TRIAGE:45) |
| size of the leak set | (A5)(a) \|Q∖S₀\| ≤ (1−δ) log n, or (b) \|Q\| ≤ n^b, b < ½ − η/2 − √(2Aη), plus local regressions | — | WEAKER (extra hypotheses) | no leak-set notion; unimodality over all sparse sets | INCOMPARABLE |
| MAP / HPM | reported HPM of the code | Theorem S (MAP consistency, supplement) — "exact statement/hypotheses NOT INSPECTED" (map :22) | not compared (Theorem S not inspected) | — | — |

**literature dominance: NO.**

### 3.2 necessity

| master hypothesis (registry id) | reader carrier (§7) | verdict | evidence |
|---|---|---|---|
| A:T03-HYP (T1-F) → [POST] | (A1) | ARTEFACT | unique-maximiser event suffices (`W3-RM/ASSUMPTION_MAP.md:19`; T2(b)); BM-∞ part: constant-level BM(c) sufficient, T4 (`API_AUDIT/sharp1/TRIAGE.md:81-84`) |
| A:RM-FL: (FL-16) | (A2) | NECESSARY-FOR-ROUTE | as 3.1 small-set floor (RM AM:21 "used; weakening not studied"; `tsv:236` by analogy) |
| A:RM-FL: (FL-Q) | (A2) | NECESSARY-FOR-ROUTE in kind; level ARTEFACT | as 3.1 (`STATEMENT.md:140`; f03:28-31) |
| A:RM-V (V), M_n → ∞ | (A3) | ARTEFACT | `tsv:254` "WEAKENABLE … (V) sufficient; not necessary for masked designs covered by GEN/PXN"; fixed constant M* suffices (f03:26; `W3-RM/SHARPNESS.md:28-29`) → T4 |
| A:RM2-LFEAS-GAIN: (L-feas) | (A4) | NECESSARY-FOR-ROUTE | as 3.1 (FAC-PK obstruction, RM AM:31) |
| A:RM2-LFEAS-GAIN: (L-gain), η < η_A, b < β(η, A) | (A4), (A5)(b) | ARTEFACT | `tsv:255` "NONE … η_A sufficient, converse heuristic only"; β(η, A) is the exact first-moment threshold of junk exclusion under a uniform leak, but the uniform quantifier is not needed (leak-profile, O2/T2(c)) (f03:33-36); B4: LS0 probe fails 4/6 at η = 1, n = 1600 — "the leak condition is not only a proof device" (RM2 AM:56) |
| A:RM2-LSIZE-B (\|Q\| ≤ n^b) | (A5)(a)/(b) | ARTEFACT | `tsv:252` "ARTEFACT … sufficient budget of the junk-exclusion argument; necessity open"; RM2 SHARPNESS.md:10-24 |
| A:RM2-BM-W | (A1)/(A5)(b) "θ*²_min n/(\|Q\| + log n) → ∞" (= BM-Q ⇒ BM-W) | ARTEFACT | `tsv:253` "NONE … sufficient; necessity not studied"; the proof needs only the additive margin √λ_n ≥ 2(d_n + √(2 log n)) (`sharp2/TRIAGE.md:45`, checked against `W3-RM2/lemmas/L2_width.md:205-217`); some floor at scale d_n looks route-necessary (heuristic, f03:21-24) |
| A:RM2-W (𝔴⁰_n → −∞) | (A5)(a) via (W-χ), (A5)(b) via (W-loc) | NECESSARY-FOR-ROUTE | `tsv:251` "gap → +∞ obstructs whole-lattice no-addition; not for reporting; bounded gap undetermined"; quantile form narrows the window to O(1/√log n) (f03:15-19; triage A2) |
| (A5)(a)/(b) sufficient forms | (A5) | ARTEFACT | sufficient forms of (W) (`W3-RM2/STATEMENT.md:147-168`; SHARPNESS.md:57-60) |
| RM-0, F-UNI hypotheses | as 3.1 | as 3.1 | as 3.1 |
| A:OP, A:BLOCK-LE-16, delivery premises | (S3), (S4) | implementation premise, not a statistical hypothesis | as 3.1 |

### 3.2 better

- `W3-RM2:RM2-F`: sharp2 f03 "SHARP W3-RM2:RM2-F VERDICT=IMPROVABLE-EASY" (`results/f03.md:11-67`). Triage
  **A1 → T4** (`sharp2/TRIAGE.md:45`): additive (BM-W) floor (A1, added to T4); quantile form of (W) (A2, same leg);
  constant (V) = T4 (B); search-event rate (B, note R); s²/8 → s²/2, A → log p/log n (C); leak profile = O2/T2(c) (B).
  Rider grouping: "T4 (existing, RM2) + additive (BM-W) floor, Ex-Proxy with decaying θ_n, optionally quantile (W)"
  (`sharp2/TRIAGE.md:74`); listed as a headline change "RM2-F (C1) | (BM-W) additive at the constant level; (V)
  constant (T4) | A1" (`:112`).
- RM-0, F-UNI: as 3.1 (T2).
- Riders created: **T4** (enlarged by sharp2) + **T2**, one Opus leg (`Wave3/HQ_NOW.md:70-71`; "RM2-F (via T4)" in
  "Headline statements that would change (stronger)", `HQ_NOW.md:42-43`). The reader's (A1)/(A3) will change when T4
  lands (READER §7 header: "Pending delta RM2-F (rider T4, via Theory Dept)").

GATES row 3.2: lit=PASS necessity=PASS better=PASS

---

## Row 3.3 — The start law already concentrates — `READER_VERSIONS.md` §5

Masters: `W3-START2:START-R@1.0.0` (`Wave3/W3-START2/STATEMENT.md:134-145`; (L-R⁺) :63-73) "PROVED-CHECKED";
`W3-START:FLOOR@1.0.0` (`Wave3/W3-START/STATEMENT.md:241-243`) "PROVED-CHECKED". Registry notes: both
"headline-strength pending (lit gate open; …)"; START-R gates already carry `better-proposal:BT2-P4 … =adopted(BRIEF.md)`.

### 3.3 lit

| item | ours (master) | Song–Liang (2015) | vs S–L | closest implementation-level / prior-rate result | vs it |
|---|---|---|---|---|---|
| object | start law π₀ of the coded SMC (block-product start): P(π₀(S₀) ≥ 1 − n^{−c}) → 1, c < ½; lattice form (\|Q\|+1)n^{−1/2}e^{C_R√log n} (START2 :134-145) | no start object; Thm 4/Cor 2 screening on a candidate subset (map :25-26; `W3-START/ASSUMPTION_MAP.md:65-67`) | INCOMPARABLE | Schäfer–Chopin 2013: SMC initial/proposal families on binary spaces, no concentration theorem (abstract, re-read) | STRONGER |
| exponent ½ | optimal on every data set: 1 − π₀(S) ≥ ⅓(n+1)^{−1/2}, \|S\| < K (FLOOR :241-243) | — | — | local unit-information priors accrue evidence for a true smaller model at n^{−1/2} (Johnson–Rossell 2010; quoted by the blind reviewer, `sharp2/results/f04.md:18`; recalled, not re-read) | EQUAL (same mechanism; the floor belongs to the prior) |
| faster rates elsewhere | n^{−1/2} forced by the shipped prior | — | — | YWJ (g ≍ p^{2α}, p^{−κ\|γ\|}), Narisetty–He, CSvdV, Johnson–Rossell 2012 non-local priors (f04:19-22; recalled, not re-read; JR2012 PDF `Papers/…/17_2012_Johnson_Rossell…` not re-read) | INCOMPARABLE (different prior; "no design condition helps", f04:24) |
| exact block posteriors | non-orthogonal blocks, rate, leakage functional, floor | — | — | Papaspiliopoulos–Rossell 2017: exact block-diagonal posteriors for orthogonal blocks (`W3-START/ASSUMPTION_MAP.md:67-68`, from SoP TH03; recalled, not re-read) | STRONGER (non-orthogonal blocks; rate) |
| hypotheses | Gaussian rows, floor on ≤ 16+s₀ sets, visibility PTV(a), no leak outside S₀ (or Q) with localisation, s₀ fixed, p ≤ n^A | Condition 5 \|cov(x_t, y)\| > 0 is the analogue of PTV (`Wave2/W2-UNI/REPORT.md:158-159`; map :27) | INCOMPARABLE | — | — |

**literature dominance: NO.**

### 3.3 necessity

| master hypothesis (registry id) | reader carrier (§5) | verdict | evidence |
|---|---|---|---|
| p > s₀ | (A1) | NECESSARY | "at p = s₀ there is no null column and the ratio o₀/T₁ is undefined … NECESSARY for the stated conclusions" (`W3-START/ASSUMPTION_MAP.md:15`) |
| A:START-R-FL (FL-R16) → (GF-16) | (A3) | NECESSARY-FOR-ROUTE | `tsv:236` "W3-START:TK A:START-GF NECESSARY-FOR-ROUTE"; "forced only by the proof route (Lemma TK …)" (START AM:37); necessity of (GF-16) open (`W3-START2/REPORT.md:114`) |
| A:START-R-V (V-R) = PTV(a) | (A4) | NECESSARY (in kind); fixed level a > 0 ARTEFACT | `tsv:246` "W3-START2:START-F A:START-V NECESSARY … L7_NEC.md:28" (one-truth failure threshold (C2)(ii), partition-free (N3); START AM:30-31); decaying a_{V,n}: class D (`sharp2/TRIAGE.md:57`) |
| A:START2-R-L (L-R⁺): T₁ → 0 | (A5) | NECESSARY | o₀ ≥ T₁ deterministic (START AM:19, :32-33) |
| A:START2-R-L: its functional form (leak C_Ln^{−1/2}, \|H_l\| ≤ (log n)^{κ_Q}, r_n(n log n)^{1/4} → 0) | (A5) | NECESSARY-FOR-ROUTE (registry); leak level ARTEFACT | `tsv:250` "W3-START2:START-R A:START2-R-L NECESSARY-FOR-ROUTE … P4_BR.md:101"; "\|H_l\| ≤ (log n)^{κ_Q} NECESSARY-FOR-ROUTE: the count N_ref" (`W3-START2/REPORT.md:96`), but the blind reviewer finds this true only for the C_L = 0 clause (f09 §START-R(a); triage A2 → T10, `sharp2/TRIAGE.md:68`); leak level: "ARTEFACT-threshold" (START AM:23, open O1) |
| Gaussian noise (S1) | standing | NECESSARY-FOR-ROUTE | START AM:20 "route"; binding map :37 |
| s₀ fixed | (A2) | ARTEFACT | "unharvested: the table identities are explicit in s₀ (open item O3)" (START AM:14) |
| p ≤ n^A | (S2) | ARTEFACT (scope) | thresholds sharp in A (START AM:13); log p = o(log² n) "conceivable … hard" (f09 §START-R(a)) |
| FLOOR: \|S\| < K | floor clause, s₀ < K | NECESSARY | "a saturated model … its mass can be exponentially close to 1" (`sharp2/results/f04.md:9`; `W3-START/STATEMENT.md:207-209`) |
| FLOOR: n ≥ 4, valid data | floor clause | implementation premise / domain | — |
| A:EX-A, A:BLOCK-LE-16 (both masters) | (S3) | implementation premise, not a statistical hypothesis | START AM:25-26 |

### 3.3 better

- `W3-START:FLOOR`: sharp2 f04 "VERDICT=SHARP"; triage "Agreed (tight including the constant; exponent ½ belongs to
  the prior)" (`sharp2/TRIAGE.md:49`). No proposal.
- `W3-START2:START-R`: sharp2 f09 "VERDICT=IMPROVABLE-EASY"; triage **A2 → T10**: \|H_l\| ≤ exp(κ√log n) gives the
  main display with C_R + 15κ; factor in log p (C); e^{c√log p} lower-bound remark (D) (`sharp2/TRIAGE.md:68`).
  Related on the base statements: START:START-R f06 **A1 → T10 (apply in START2)** — Q = S₀ leading term needs 2^{s₀}
  reference sets, rate O_P(√(log n/n)) at C_L = 0 (`:57`); START2:IF-START f08 **A1 → T10** (`:65`); START:START-F f04
  **A1 → T8** (visibility at log n + 2 log p; reaches START2 through the base (V-c)/(V-m)) (`:50`).
- Rider created: **START2 v1.5 = T10 + T8** (~8–10 h) (`Wave3/HQ_NOW.md:24-26`); headline change listed
  (`sharp2/TRIAGE.md:109-110`; `HQ_NOW.md:42`). Pending delta recorded in READER §5 header. Note: T10's rate gain is at
  C_L = 0 only; Theorem 5's (A5) allows C_L > 0, where f09 argues e^{C√log p} is unavoidable (heuristic).
- Ticket-internal: BT2-P4 adopted (registry gates field, START2-R row).

GATES row 3.3: lit=PASS necessity=PASS better=PASS

---

## Row 3.5 — Unbiased evidence estimate — `Wave1/W1-N1` (reader version: "to write")

Master: `W1-N1:Thm-N1@1.0.0` (`Wave1/W1-N1/STATEMENT.md:98-104`, premises :68-90) "PROVED-CHECKED". Registry gates
now: `lit:PENDING; necessity:PENDING; better:PENDING`.

### 3.5 lit

| item | ours (master) | Song–Liang (2015) | vs S–L | closest SMC result | vs it |
|---|---|---|---|---|---|
| object | E[Ẑ_r·(1/N_e)Σ_i h(S_{rqi}) \| 𝓒] = Zπ(h) and E[Ẑ_r H_r(h) \| 𝓒] = Zπ(h), every bounded h fixed before the final streams, a.s. on 𝒜 ∩ {r ≤ R′}; the coded `log_Z_r` and `pip_plain` (STATEMENT.md:98-104, :45-66) | SAMC importance-weighted averages; no evidence estimator, no theorem (§3.2, p. 959, re-read; map row 8, :23) | STRONGER | Del Moral (1996): the SMC normalising-constant estimate is unbiased — as stated in Dau–Chopin 2022, Prop. 2 and text after it, p. 7 (re-read; Del Moral itself not re-read) | EQUAL in mathematical content: N1 = T12 (i.b) + code bridge + freezing lemma + linearity (`lemmas/R_remarks.md:7-10`); "N1 matches it, plus the routine post-terminal invariant-kernel" step (`API_AUDIT/sharp1/results/f01.md` §(b)) |
| adaptive calibration | schedule, N_e, L calibrated adaptively on streams 0–9 and frozen (CAL, SI; STATEMENT.md:79-82): conditional unbiasedness | — | — | adaptive-tempering SMC evidence estimators are consistent but not unbiased in general (Beskos–Jasra–Kantas–Thiery 2016; quoted in f01 §(a), "as I recall it"; recalled, not re-read) | INCOMPARABLE (different conditioning; N1 removes adaptivity by stream separation) |
| functionals | any bounded measurable h, per measured round q (STATEMENT.md:62-66, :98-101) | — | — | unnormalised Feynman–Kac measures γ_t(φ) unbiased (Del Moral 2004; recalled, not re-read) | EQUAL |
| hypotheses | implementation premises only; "No regime assumption on X" (STATEMENT.md:104) | — | — | abstract SMC with invariant MCMC moves | EQUAL (KERNEL = invariance; N1 also needs the code bridge N9 "PROVED (candidate)", STATEMENT.md:75-78) |
| model-comparison SMC | — | — | — | Zhou–Johansen–Aston 2016 adaptive SMC for model comparison, extends existing theory to path sampling (abstract, re-read); Schäfer–Chopin 2013 no theorem (abstract, re-read) | INCOMPARABLE / STRONGER |

**literature dominance: NO** — no published result is about the coded fields; but the identity itself is classical
(caution 1 at the top).

### 3.5 necessity

N1 has no statistical hypothesis (no design, signal or dimension condition: STATEMENT.md:104). Every premise is an
implementation premise; necessity evidence is listed because the gate asks for it.

| premise (registry: A:OP, A:N1-KERNEL) | verdict | evidence |
|---|---|---|
| KERNEL: q_φ-invariant kernels at every grid point; final reweighting to φ = 1 | implementation premise, not a statistical hypothesis; NECESSARY | NC1 (non-invariant terminal kernel): discrepancy 3e-3 to 0.77; NC2 (no final reweighting): ≥ 3e-3 (`lemmas/R_remarks.md:15-17`) |
| KERNEL: uniform state-independent order, product-law / iid parts | implementation premise, not a statistical hypothesis; ARTEFACT | only invariance + order independent of the entering state is used (f01 §(a) item 3); `tsv:16` "WEAKENABLE" |
| CAL / h frozen before stream 10 | implementation premise, not a statistical hypothesis; NECESSARY | NC3 (post-hoc h): discrepancy up to +0.17, resolved on 18/20 runs (`R_remarks.md:18-20`) |
| SI | implementation premise, not a statistical hypothesis; ARTEFACT | only U_r ⊥ σ(𝓒) is used (f01 §(a) item 2); `tsv:16` "WEAKENABLE … N1 uses SI, a sufficient premise weaker than the card's IND-T" |
| START, EX-A, potential run (POT) | implementation premise, not a statistical hypothesis; NECESSARY for exactness | the identity is linear in Z̄₀ and exact (f01 §(a); `R_remarks.md:21-22` on completion/diagnostic conditioning) |
| uniform bound B_h on h | implementation premise (class of h), not a statistical hypothesis; ARTEFACT | Ω finite: basis indicators + σ(𝓒)-linearity suffice (f01 §(a) item 1) |
| R′ = 4k | implementation premise, not a statistical hypothesis; ARTEFACT (cosmetic) | only {r ≤ R′} σ(𝓒)-measurable is used (f01 §(a) item 4; sharp1 TRIAGE:32 "C") |
| MEAS, worker equivalence (v3.1) | implementation premise, not a statistical hypothesis | STATEMENT.md:83-90; `tsv:15` A:OP "NONE" |

### 3.5 better

- sharp1 f01 "SHARP W1-N1:Thm-N1 VERDICT=IMPROVABLE-EASY" (`API_AUDIT/sharp1/VERDICTS.tsv`; `results/f01.md`).
  Proposals: drop B_h; condition on all calibration streams V (or (V, U_{−r}) under IND-T); identity for every
  post-terminal population and stage; KERNEL reduced to invariance + state-independent order; R′ = 4k cosmetic.
- Triage **B (park)**: "Generality only … Real, about a day. Out of scope for the Wave 3 package … Hand f01 to the
  track-3 lead; no ticket now. `R′ = 4k`: C (cosmetic)" (`sharp1/TRIAGE.md:32`). HQ: "f01 handed to W3-SCALE"
  (`Wave3/HQ_DECISIONS.md:154`). No rider ticket.
- Suggestion (no gate effect): the reader version is still "to write"; proposals (ii)/(i) of f01 follow from the
  ticket's own lemmas, but stating them in the reader version would exceed the master (READER rule: nothing beyond the
  master), so they need a statement revision first.

GATES row 3.5: lit=PASS necessity=PASS better=PASS

---

## Row 3.6 — Consistency of printed PIP / MPM / HPM / Ẑ — `Wave3/W3-SAMP` (reader version: "to write")

Masters: `W3-SAMP:C@1.1.1` (`Wave3/W3-SAMP/STATEMENT.md:149-163`), `W3-SAMP:TR@2.1.1` (:165-177), `W3-SAMP:LT#@2.0.1`
(:126-140), `W3-SAMP:D@2.1.1` (:97-105): "PROVED-CHECKED" (each). Clause LT♯(f) (`W3-SAMP:LT#(f)`, :141-147): "OPEN;
nothing claimed (finite-target illustrations only)". Interface properties :73-84. Planned reader carriers
(`CLAIMS_CARD.md:48`): P-CONC from Theorem 2 (READER §2), P-START from Theorem 5 with Q = S₀ (READER §5) via
`W3-START2:IF-START@1.0.0` "PROVED-CHECKED".

### 3.6 lit

| item | ours (master) | Song–Liang (2015) | vs S–L | closest implementation-level result | vs it |
|---|---|---|---|---|---|
| object | printed `pip_primary`, MPM, HPM and `log_Z` of the coded 4-island run: Ẑ/Z → 1, ‖pip_primary − 1_{S₀}‖_∞ → 0, MPM = S₀, HPM = S₀, at the posterior rate (C-v, :158-162); PIP/MPM/HPM without any condition on Ẑ (TR-d, :170-173); HPM by draw discovery (D-iv, :104) | SAMC importance-weighted PIP estimates, no theorem (§3.2, p. 959, re-read); "the method's shipped pooled reported PIPs (R′ = 4) have no in-probability sure-screening theorem" (map :34-35, gap (iii)) | STRONGER (closes the recorded gap) | YWJ 2016 / Zhou 2022: TV mixing of the chain (Zhou Thm 1, p. 14, re-read); ergodic averages then estimate PIPs (standard; recalled) | INCOMPARABLE |
| asymptotic regime | n → ∞ with any fixed N_e ≥ 1, any L ≥ 0, any valid grid (C: :149-150) | — | — | SMC consistency/CLT as the number of particles → ∞ for a fixed target (Dau–Chopin 2022 Prop. 3, p. 8, re-read; Del Moral 2004, recalled) | INCOMPARABLE (different limit; ours holds at N_e = 1) |
| start / overlap conditions | C: P-START (π₀(S₀) → 1 on 𝒜) + P-CONC; TR: P-OVL∞ (production: M ≤ ε log n); D: P-OVL (D_rπ₀(S₀) → ∞) | — | — | from **any** start, polynomial (YWJ) or dimension-free (Zhou) mixing under Condition 1 unimodality, tuned prior p^{−κ\|γ\|}, 1 + g = p^{2κ₁}, s₀ log p = O(n) (Zhou pp. 6–8, 14, re-read); reviewer: "a discovery theorem through the local moves with no overlap condition is therefore plausible, but it needs landscape and mixing input that this ticket excludes" (`API_AUDIT/sharp1b/results/f20.md:24-26`) | INCOMPARABLE (they need unimodality, a tuned prior and run length ≥ T_mix; ours needs start concentration or global overlap, with the shipped prior and the production budget) |
| evidence estimate | Ẑ/Z → 1 (C-iii/C-v) | none | STRONGER | YWJ/Zhou: none (STRONGER); SMC normalising-constant variance bounds under mixing (Cérou–Del Moral–Guyader 2011; quoted in f01 §(b); recalled, not re-read) | INCOMPARABLE |
| other samplers | — | — | — | Zanella 2020 (locally balanced proposals, Peskun optimality), Zanella–Roberts 2019 (importance tempering, robustness to dimension) (abstracts, re-read) | INCOMPARABLE (efficiency, no consistency of printed outputs) |
| SMC on binary spaces | — | — | — | Schäfer–Chopin 2013, no theorem (abstract, re-read) | STRONGER |

**literature dominance: NO.**

### 3.6 necessity

| master hypothesis (registry id) | claim(s) | reader carrier | verdict | evidence |
|---|---|---|---|---|
| P:POST-CONC (δ → 0) | C, TR, LT♯ | Thm 2 (planned) | NECESSARY-FOR-ROUTE | `tsv:208` "NECESSARY … κ0 term attained exactly (RB PIPs need κ0→0); sharp in form"; but the source says "This is sharpness of the bound, not a proof that consistent RB PIPs require κ₀ → 0 (SW1 #7)" (`W3-SAMP/ASSUMPTION_MAP.md:16`) — caution 2; `tsv:215` (C) "NONE" |
| A:P-START (1_𝒜o₀ → 0, no rate) | C (only route to Ẑ/Z → 1) | Thm 5, Q = S₀ (planned) | **OPEN** (for the Ẑ clause); ARTEFACT for the PIP/MPM/HPM clauses | `tsv:213` "FAILED-REMOVAL … some start condition necessary in kind (trap example π0(S0)=1.5e-8 with P-CONC true fails at fixed small L; finite-n only)"; `tsv:214` "ARTEFACT … the T·δ̄ factor is not needed … removed in v3"; PIP/MPM/HPM also follow without it from TR under P-OVL∞ (:170-173), which at the level of abstract targets neither implies nor is implied by π₀(S₀) → 1 (:174-177); TR "does not repair Ẑ" (:177) |
| A:NC-R (NC_r, every r ≤ 4) | LT♯ | none (computational) | ARTEFACT | `tsv:210` "WEAKENABLE … complemented by Theorem TR and weakened to a vanishing threshold (LT-e′)"; `tsv:209` "NONE … necessity open"; LT♯(f) "OPEN; nothing claimed"; discharged by C, replaced by TR (:144-147); reviewer: pooled non-collapse may suffice for HPM (sharp1b TRIAGE:90-91, unconfirmed) |
| A:P-OVL∞ | TR | none | ARTEFACT | `tsv:216` "WEAKENABLE … sufficient, not necessary: in the 'near' example M=1.3e6 (TR vacuous) while local moves repair the PIPs"; `tsv:217` |
| A:P-OVL (Q_D → ∞) | D | none | NECESSARY-FOR-ROUTE | `tsv:204` "equality for the draw mechanism (sharp); only sufficient for the reported HPM (S0 reached as particle endpoint in 94-97% of islands with no draw hit)" |
| A:P-MAP (S† = S₀) | D | via P-CONC | NECESSARY (essentially); quantifier ARTEFACT | `tsv:206` "NONE … weakened from δ<1/2 to the MAP condition"; reviewer: "P-MAP itself is essentially necessary for 'Ŝ = S₀': Ŝ is the maximum of 𝓜 ⊆ Ω, so if S† ≠ S₀ then Ŝ = S₀ only when S† was missed" (sharp1b f20:18, not triaged); localisable to 𝒜 (sharp1b TRIAGE:88-89, "to be confirmed by the re-run") |
| s₀ ≤ K | all | (A1) | NECESSARY | "S₀ ∈ Ω | yes | sharp" (`W3-SAMP/ASSUMPTION_MAP.md:14`) |
| A:N1-KERNEL (START, KERNEL, MEAS, SI, POT) | all | — | implementation premise, not a statistical hypothesis | `tsv:212` "NECESSARY-FOR-ROUTE … KERNEL invariance necessary for MR (N1 control NC1 breaks it)" (LT♯); D uses only the control-flow clause (`tsv:207`) |
| A:CAL, A:EX-A-HU | all | — | implementation premise, not a statistical hypothesis | `W3-SAMP/ASSUMPTION_MAP.md:12` |
| A:IND-T | D-ii only | — | implementation premise, not a statistical hypothesis (optional) | `tsv:205` "WEAKENABLE … not needed for D-i or any other claim; optional" |
| A:BLOCK-LE-16 | LT♯ (constant 19 = B + 3) | — | implementation premise, not a statistical hypothesis | `tsv:211` "ARTEFACT … constant 19=B+3 loose (λ0 1.37 vs 13.6), harmless" |

### 3.6 better

**better: PENDING (SHARP3).** No complete blind verdict exists:
- sharp1 f20 (claims D, LT♯, C, TR in one request): no text, "stop_reason: max_tokens"
  (`API_AUDIT/sharp1/results/f20.md:1-3`; `sharp1/VERDICTS.tsv` "f20 - STOP=max_tokens").
- sharp1b f20: partial, "stop_reason: max_tokens" (`sharp1b/results/f20.md:3`); it reviewed D and started LT♯. D:
  "The core equality is sharp. The method-level strengthening is real but not cheap" (`:39`); cheap items: localise
  P-MAP to 𝒜 (`:17`), a set version of D-i (`:32`), record TR-d/C-v HPM clauses as corollaries of D-iv (`:33`);
  substantive: neighbour-scoring bound, iterated-ascent discovery under a YWJ-type unimodality premise (`:36-37`).
  LT♯: "'NC_r for every r ≤ 4' (`STATEMENT.md:136`) is stronger than each conclusion needs … non-collapse of the
  reported pooled evidence suffices" (`:47-48`, text stops mid-argument).
- sharp1b TRIAGE §3: "f20 returned the review of Theorem D and the start of LT♯; two items there look real and cheap,
  to be confirmed by the re-run, not ticketed yet: D: P-MAP can be localised to the completed-run event 𝒜 … P(𝒜) → 1
  is never assumed, so this matters. LT♯: 'NC_r for every r ≤ 4' is more than the HPM clause uses; non-collapse of the
  pooled evidence appears to suffice … This touches the recorded open item 'NC_r necessity'" (`sharp1b/TRIAGE.md:83-91`).
- Requested in SHARP3 as g00 (C), g01 (TR), g02 (LT♯, confirm/deny the NC_r item), g03 (D, confirm/deny the P-MAP item)
  (`W3-READER/SHARP3_REQUEST.md:19,25-28`). No rider ticket exists for W3-SAMP.

GATES row 3.6: lit=PASS necessity=OPEN(P-START: necessity for the Ẑ/Z → 1 clause of C not settled — finite-n trap only, `tsv:213`; C is the only Ẑ route, TR "does not repair Ẑ") better=PENDING
