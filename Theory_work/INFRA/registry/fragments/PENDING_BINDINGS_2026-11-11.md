# Pending bindings, 2026-11-11 (ingest gap: `consumes` P:X@B, method pins, binding-map rows)

Context: `tools/ingest.py` drops `consumes`, `method_commit` / `method_components` and the binding-map rows of a
fragment (HQ, 2026-11-11). A tool fix is being made separately. This file lists, per claim, what the 2026-11-11 registry
update (W3-SAMP rebump; W3-POST2, W3-RM, W3-SCR ingest) could not store through ingest, so it can be re-ingested and
checked once the fix lands.

Status per row:
- **STORED-SET**: stored after the ingest with `registry.py set` (logged in `events.log`). Re-ingest should reproduce
  it; a fixed tool may also verify it.
- **PENDING**: not stored anywhere. Needs the tool fix, or a tool for `binding.tsv` / `assumptions.tsv`.

Interim rule applied (HQ item 1): every bridge or interface-property source a claim uses is also an explicit
`depends_on` edge, so propagation reaches it without the binding. Those edges are listed in §1 under "edge".

## 1. `consumes` bindings (P:X@bridge)

| claim | binding | state | explicit `depends_on` edge(s) |
|---|---|---|---|
| W3-SAMP:C | P:POST-CONC@W3-POST:Thm-1 | STORED-SET | W3-POST:Thm-1@stmt:P-CONC (C-v), already present |
| W3-SAMP:LT# | P:POST-CONC@W3-POST:Thm-1 | STORED-SET | W3-POST:Thm-1@stmt:P-CONC (LT-e), already present |
| W3-SAMP:TR | P:POST-CONC@W3-POST:Thm-1 | STORED-SET | W3-POST:Thm-1@stmt:P-CONC (TR-d), already present |
| W3-SAMP:D | P:POST-CONC@W3-POST:Thm-1 (through P-MAP) | STORED-SET | W3-POST:Thm-1@stmt (D-iv), already present; **added** W1-N1:B@proof:B-b control-flow clause (KERNEL) |
| W3-SAMP:C, D | P-START (input from PROGRAM item 2 / W3-START) | PENDING: no registry claim yet | EXT:PROGRAM item 2 (aliased `-`, unregistered) |
| W3-RM:RM-0 | P:POST-CONC; P:SAND; P:NA-TL (interface hypotheses of the core, no bridge) | STORED-SET (plain, no `@`) | — |
| W3-RM:RM-0 | P:E4@W3-RM:E4 | PENDING: no `P:E4` row in assumptions.tsv | W3-RM:E4@stmt |
| W3-RM:RM-F | P:SAND@W3-RM:B2; P:SAND@W3-RM:B2tau; P:NA-TL@W3-RM:B3; P:NA-TL@W3-RM:NA-F; P:NA-TL@C-GROW:L2.3; P:POST-CONC@SOP:TH09 | STORED-SET | B1, B2, B2tau, B3, B3p, NA-F, N-loc, C-GROW:L2.2, C-GROW:L2.3, SOP:TH09 (B6), C-GROW:L3 |
| W3-RM:RM-R | P:SAND@W3-RM:SAND-Rp; P:NA-TL@W3-RM:B8a; P:NA-TL@W3-RM:B8b; P:POST-CONC@W3-RM:B9 | STORED-SET | SAND-R, SAND-Rp, B8a, D-loc, B8b, B9 |
| W3-POST2:A1 | P:OS@W3-POST2:A0 (REPORT.md:209 "consumes: P:OS") | PENDING: no `P:*` row for (OS). (OS) is registered as hypothesis A:POST2-OS | W3-POST2:A0@stmt |
| W3-POST2:E | (ID^M) via bridge W3-POST2:E3.1 | PENDING: no `P:*` row. Registered as hypothesis A:POST2-IDM | W3-POST2:E3.1@stmt |
| W3-POST2:D.D(a) | P:POST-CONC (δ_n → 0 is a hypothesis; no bridge) | PENDING: split parts carry no strength fields | — |
| W3-SCR:SCR-A, SCR-Ao | GAP({\|S\| ≤ q}) via SV / SV° (STATEMENT §4) | PENDING: no `P:*` row for GAP | direct proof (L3); SCR-M ⇒ SCR-A, SCR-Ao is recorded as `implies` on W3-SCR:SCR-M |
| W3-SCR:SCR-G | GAP via W3-SCR:SCR-M (M2, M4, M5) | PENDING (no P row) | W3-SCR:SCR-M@stmt |
| W3-SCR:A1, A1o | SV / SV° via Lemma B | PENDING (no P row) | W3-SCR:B2d, B3 (A1); B2o, B2d, B3 (A1o) |
| W3-SCR:SCR-C | NF and screening | PENDING (no P row) | W3-SCR:L5.1, L5.2, A-inf, Ao-inf |

## 2. Method pins (`method_commit`, `method_components`)

All STORED-SET. The core is unchanged from 4676af6 and 2252d57 to HEAD (`git diff --stat` is empty).

| claims | method_commit | components | source |
|---|---|---|---|
| W3-SAMP: CC, PC, MR, ST, D, LT#, LT#(f), C, TR, Pkg | 4676af6 | core | STATEMENT.md:38 ("production core on main = 4676af6") |
| W3-RM:RM-0 | 2252d57 | engine; start; runtime | lemmas/L5_E4.md:6-7 (code read at main, commit 2252d57) |
| W3-RM:E4 | 2252d57 | start; engine; runtime | same |
| W3-RM:RM-F, RM-R, Examples | 2252d57 | core | same |
| W3-SCR: CC, SCR-A, A-inf, SCR-Ao, Ao-inf, SCR-M, SCR-G, A1, A1o, SCR-C, SCR-R | 2252d57 | engine; runtime; score | CODE_CHECK.md:3 |
| W3-POST2 (all) | none | — | statements about the coded target π, like W3-POST:Thm-1 (unpinned) |

## 3. Binding-map rows (`binding.tsv`): all PENDING

There is no tool to add binding rows, and none of the four REPORTs carries a `binding:` line in the template's
registry-block format. The rows below are transcribed from the ticket text. Each needs attestation at re-ingest
(LIFECYCLE §5.5: binding mechanisms are attested). Until then the S7-binding WARNs remain: 106 in total, 94 of them
on the claims touched here.

| headline | assumption | binding claim | mechanism (source) |
|---|---|---|---|
| W3-RM:RM-F | A:RM-V | W3-RM:B2 | visibility of each truth in the block sandwich; input map (V) → B1, B2, B7 (STATEMENT.md:210) |
| W3-RM:RM-F | A:RM-L | W3-RM:B2tau | leakage η < η_A in the uniform sandwich argument; (L-gain) → B1, B2, B7 (STATEMENT.md:210; SHARPNESS (ii)) |
| W3-RM:RM-F | A:RM-N | W3-RM:NA-F | whole-lattice no-addition union over directions; (N-D)(i) → B5, (N-χ) → B4 (STATEMENT.md:212) |
| W3-RM:RM-F | A:RM-FL | W3-RM:B3 | floors on Q ∪ {l}: (FL-Q) → B3, B4, B5; (FL-16) → B1, B2 (STATEMENT.md:209-210) |
| W3-RM:RM-F | A:T03-HYP | SOP:TH09 | (T1) → B6 POST-F via T03♯ (STATEMENT.md:207) |
| W3-RM:RM-F | A:BLOCK-LE-16 | W3-RM:B1 | "15" = block cap − 1 (REPORT.md:129-130) |
| W3-RM:RM-F, RM-R | A:OP | W3-RM:RM-0 | implementation premises enter only the pathwise reporting core (STATEMENT.md:55-58) |
| W3-RM:RM-R | A:PTV | W3-RM:SAND-R | (V-R) → B7 (STATEMENT.md:210) |
| W3-RM:RM-R | A:RM-LR | W3-RM:SAND-Rp | localisation, because the partition is X-measurable; (L-loc-R) → B7 (STATEMENT.md:211; REPORT.md:8-10) |
| W3-RM:RM-R | A:NA-FRAME | W3-RM:B8a | (D-R) → B8a (STATEMENT.md:212) |
| W3-RM:RM-R | A:RM-FLR | W3-RM:B8a | (FL-R, Q ∪ {l}) → B8a, B8b; small sets → B7 (STATEMENT.md:209-210) |
| W3-RM:RM-R | A:LSF | W3-RM:B9 | (T1-R) → B9 POST-R (STATEMENT.md:207) |
| W3-RM:RM-R | A:IID-GAUSS-ROWS, A:BLOCK-LE-16 | W3-RM:SAND-R | setting R; X-measurable partition with blocks ≤ 16 |
| W3-RM:RM-0 | P:POST-CONC, P:SAND, P:NA-TL | — (interface hypotheses) | supplied by RM-F / RM-R; no binding in the core |
| W3-SCR:SCR-A / SCR-Ao | A:SCR-SV / A:SCR-SVo | W3-SCR:SCR-A / SCR-Ao | witness margin in the one-step gain (lemmas/L3_screening.md); M3 ⇒ GAP (STATEMENT.md:241-242) |
| W3-SCR:A1, A1o, SCR-G | A:SCR-DF | W3-SCR:B2d | DF enters only through Lemma B's lower bound for Γ_n / Ψ_n (STATEMENT.md:243-244) |
| W3-SCR:A1 / A1o / SCR-G | A:SCR-A1-COND / A:SCR-A1o-COND / A:SCR-G-GROWTH | W3-SCR:A1 / A1o / SCR-G | coefficient and growth conditions that make MC / MC° hold (STATEMENT.md:156) |
| W3-SCR:SCR-C | A:SCR-NF | W3-SCR:L5.1 | (EC′) is violated under the superset floor (STATEMENT.md:245) |
| W3-SCR (all) | A:GAUSS-NOISE, A:EX-A | — | not transcribed: no binding claim named in the REPORT |
| W3-POST2 (A1, B, C, D, E) | all hypotheses | — | not transcribed: REPORT §8 has no `binding:` lines. Source to use: W3-POST2/ASSUMPTION_MAP.md v1.3 |
| W3-SAMP (C, D, LT#, TR) | all hypotheses | — | not transcribed: REPORT §5 has no binding map. Source to use: W3-SAMP/ASSUMPTION_MAP.md |

## 4. Assumption-row metadata ingest cannot set (assumptions.tsv): PENDING

Ingest creates new `A:` / `P:` rows with shared = no and empty bridge / implies / source.

| id | field | value | source |
|---|---|---|---|
| A:POST2-OS | shared, bridge | yes, W3-POST2:A0 | W3-POST2/REPORT.md:208 |
| A:POST2-OS | implied by | A:SPARSE-EIG's (F_w) part, via (DG) ⇒ (ADG) ⇒ (OS) | STATEMENT.md:46 |
| A:POST2-IDM | bridge; implied by | W3-POST2:E3.1; (F_λ) ∧ BM(c) ⇒ (ID) ⇒ (ID^M) | W3-POST2/REPORT.md:249; STATEMENT.md:47 |
| A:POST2-FLAMBDA | implies | A:POST2-F0 | STATEMENT.md:47 |
| A:SPARSE-EIG | implies | A:POST2-FLAMBDA (A:SPARSE-EIG = (SE_λ) ∧ (SE_w)) | W3-POST STATEMENT §2 |
| A:RM-L | note | (L-gain^σ) ⇒ (L-gain^τ); the registered row is the τ-form | W3-RM/REPORT.md:123 |
| A:RM-N | note | (N-loc) ⇒ (N-D)(i); BM-∞ ∧ \|Q\| = O(log n) ⇒ BM-Q | W3-RM/REPORT.md:123-124 |
| A:NA-FRAME | implied by | (D-loc) (W3-RM:D-loc) | W3-RM/REPORT.md:123 |
| A:SCR-DF | implied by | AF ⇒ DF ⇐ SF (W3-SCR:B3, B2d); no AF / SF rows were created | W3-SCR/REPORT.md:147 |
| A:SCR-SV, A:SCR-SVo | implies | GAP({\|S\| ≤ q}) (M3); no GAP row | W3-SCR/REPORT.md:148-149 |
| P:E4, P:POST2-OS, P:SCR-GAP | new property rows | not created (see §1) | — |
| P:POST-CONC | used as | [POST] of W3-RM (E[1 − π(S0)] → 0, no rate) and P-CONC of W3-SAMP (no rate) | the row's statement carries a rate; consider a no-rate property |

## 5. Relations that the schema cannot hold (item-level): for HQ

- W3-POST2:C ⇒ W3-POST:Thm-1 item 1 only (Markov; REPORT.md:120).
- W3-POST2:E supersedes W3-POST:Thm-1 items 1–4 and A1 items 1–4 for c > c1, and coexists with them for
  c0 < c ≤ c1 (REPORT.md:122). This is a LIFECYCLE §5.3 decision (supersede / coexist), not an `implies` edge.
- W3-RM:RM-F ⇒ GROW's reported-model conclusions, and W3-RM:RM-R ⇒ UNI-0's, each with e4 discharged
  (REPORT.md:126-127). Conclusion-level only, so not recorded as `implies` (that would enable a free supersession of
  C-GROW:Thm-GROW).
- Recorded as `implies`: W3-POST2:A1 ⇒ W3-POST:Thm-1; A2 ⇒ W3-POST:Prop-LB; B ⇒ W3-POST:Lemma-1a′, Lemma-1a
  (REPORT §2); W3-SCR:SCR-M ⇒ SCR-A, SCR-Ao (STATEMENT.md:122-123). All need HQ attestation (LIFECYCLE §5.5).

## 6. Stale sharpness evidence noticed (sharpness.tsv; not changed here)

- (W3-SAMP:TR, A:P-OVL-INF, NONE): the evidence cites STATEMENT.md:161-163 with the old non-nesting wording. In the
  final STATEMENT it is lines 174-177, and the claim is restricted to abstract targets (SW1 #2).
- (W3-SAMP:D, A:N1-KERNEL, NONE): the evidence says "KERNEL itself is not used by D". In v3 final, D names KERNEL
  through the control-flow clause of W1-N1 Lemma B (B-b) (C1 Opus #2).
