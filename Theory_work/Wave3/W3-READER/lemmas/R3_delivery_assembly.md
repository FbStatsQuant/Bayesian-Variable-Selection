# R3 — (historical) Delivery assembly for the former Theorems 6–7 (thm6 ≤ v0.7, thm7 ≤ v0.5; bridges B6.6, B7.4) (W3-READER bridge leg, 2026-11-16)

**Scope [R1-F2].** This lemma concerns the former reader hypotheses of Theorems 6–7, i.e. the hypotheses of `W3-RM2:RM2-R`
(resp. `W3-RM2:RM2-F`, including BM-∞, diverging visibility and (BM-W)). It is **not** a bridge for the current Theorems
6–7, whose constant-level assumptions do not imply those hypotheses; the current statements use the identities B6.6′ and
B7.5 ((S4) ⇔ the delivery premises (D) of `W3-RM2-R:DLV-0`, with the two code-reading audits carried).

Status: **PROVED (by this seat, unchecked)**. S1 checked the (V)/(S)/(P) part ("B6.6/B7.4 pass only for (V)/(S)/(P)")
and required the operational premises to be carried, with a premise-by-premise table (F2). This file is that table.

**Narrowed 2026-11-16 [FUNI-N]** (F-UNI narrowed to `@2.1.0`, recorder task S2): IDEAL-W does not lift the code's two
rejections (`v3_run.R:96`, `cpp/v3_core.cpp:474`), so A:IDEAL-W⁺ (or the domain $\mathfrak D$) is a hypothesis wherever F-UNI's
delivery is used below.

**Target.** Under the hypotheses of the former Theorem 6 (resp. 7), i.e. those of `W3-RM2:RM2-R` (resp. `W3-RM2:RM2-F`), and the delivery conventions (S4) without the IDEAL-W⁺ clause of
(S4)(i): $P(\text{no output})=0$ for every admissible $n\ge3$ with $(n,p_{\mathrm{raw}})\in\mathfrak D$; if in addition
A:IDEAL-W⁺ (now part of (S4)(i), [RM2R-1]) holds, for every [R1-E3]
admissible $n\ge3$, $P(\text{no output})=0$, and $P(\hat S=S_0)\to1$ under the joint design/noise law (resp. the noise law),
together with the algorithm's randomness.

**History note (v-next, RM2R-2 / HQ D74).** For the shipped method this assembly is superseded by the identities B6.6′ and B7.5
((S4) ⇔ the delivery premises (D) of `W3-RM2-R:DLV-0`); it is kept for the record (it concerns F-UNI's registered method).

**Source.** `W2-UNI:F-UNI@2.1.0` (`Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:15-21`; registry "PROVED-CHECKED";
the file header still says "PROVED (by this seat, unchecked)" — bookkeeping note already reported). Its proof (:23-36)
uses (V) in Step 1, the method/premise/allocation paragraph in Step 2 ("design-free: P(no output) = 0"), and (S), (P)
in Step 3 (via C-GROW L1.2 and C-DLV Corollary D′).

## Premise table
| F-UNI requirement (`L5_delivery.md`) | Supplied by | How |
|---|---|---|
| (V) input validity, random design: "(R) with $\lambda_{\min}(\Sigma_n)>0$ for every n" (:15) | Thm 6 (A1) | Gaussian rows with $\Sigma_n$ a positive definite correlation matrix. |
| (V) input validity, fixed design: "(E) with nonconstant raw columns" (:15) | Thm 7 (A1) via Setting F | Setting F is a fixed raw design **with non-constant columns** (`W3-START/STATEMENT.md:66-67`; RM Setting F = GROW §1). **Statement fix:** Theorem 7 must say "raw columns non-constant" explicitly (added in READER_VERSIONS v0.3). |
| (S) deterministic $Q_n\supseteq S_0$, $\mathcal L_n\subseteq\Omega$ ($|Q_n|\le K_n$), $P(\mathrm{Sand}_n\cap\mathrm{NA}(\mathcal L_n)\cap\mathrm{TL}(\mathcal L_n))\to1$ (:16) | RM2-R (Thm 6) / RM2-F (Thm 7) conclusions [SAND(Q)], [NA(Q)], [TL(Q)] (`W3-RM2/STATEMENT.md:207-208, 217-218`); (L-feas) for $|Q|\le K$ | Union bound: $P(\cdot)\ge1-P(\mathrm{Sand}^c)-P(\mathrm{NA}^c)-P(\mathrm{TL}^c)\to1$. Same $Q$, same lattice; the events are those of RM §1 (`W3-RM/STATEMENT.md:49-54`), which F-UNI imports through "as in GROW L4 / FIN s5" (`W2-UNI/STATEMENT.md:34`). |
| (P) $E[1-\pi(S_0)]\to0$ (:17) | interface [POST] (`W3-RM2/STATEMENT.md:100`), delivered by RM2-R (via `W3-RM2:POST-R`, conditional on `W2-APP:POST`, now "PROVED-CHECKED") / RM2-F (via `SOP:TH09`, PROVED-CHECKED since main 6cd699dd) | identical property. |
| v3.1 with deterministic complete-scan LS0 from the exact e4 start-mode maximiser (:8) | code + (S3)/(S4) | LS0 on by default (`v3_fit.R:73`, `ls0 = getOption("v3.ls0", TRUE)`); complete scans (`cpp/v3_engine.h:394-406`); `start_mode(st, 1e6, tie_dp)` with `ls0_tie_dp` default TRUE (`v3_run.R:99`, `cpp/v3_core.cpp:469`). The **e4** tie rule (the emitted centre is the prescribed smallest-size, lexicographically smallest maximiser) and **TDP-IMPL** (the tie-aware fallback's cost) are carried as premises in (S4); RM's Lemma E4 proves only "a maximiser" and does not discharge them (S1 F2). |
| LS0 move cap $a_n=\ell_n+|\tilde S_0|$; other caps $\ell_n$ (:8) | code | `cpp/v3_core.cpp:473` (default `ell_n_plus_mode`); final local search cap $\ell$ (`cpp/v3_core.cpp:453-458`). Same cap as RM2's configuration (`W3-RM/STATEMENT.md:59-61`). |
| total tier-1 fallback with complete fallback-grid freezing (:8-9) | code | `v3_fit.R:151` passes `isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE))`, so the fallback is on under the shipped defaults (`ls0 = TRUE`, `v3.grid_fallback = TRUE`), both required by the covered configuration (S4)(ii); fallback recorded at `v3_calib.R:120-124`, selected and frozen at `v3_calib.R:163-189` [S2-F8]. |
| EX-A (unit-cost exact reals) (:9) | (S3)(i) + (S4) | exact arithmetic is (S3); its unit-cost reading is in (S4) ("exact unit-cost arithmetic"). |
| IDEAL-W (:9) | (S4) | "no integer or index overflow" (so `unsupported_size` never fires; C-DLV STATEMENT.md:24-26). The two LS0 cap rejections (`le > 10^6`, `cap_ll > INT_MAX`) are **not** lifted by IDEAL-W: on $\mathfrak D$ they do not fire; elsewhere A:IDEAL-W⁺ ((S4)(i), IDEAL-W⁺) [FUNI-N, R1-E3]. |
| EX-S (:9) | (S4) | **added in v0.3**: "ideal independent uniform random numbers". |
| SR (stop/return rule) (:9) | (S3) "the method's execution conventions" | **made explicit in v0.3**: (S4) lists "the method's stop/return rule as coded". |
| e4 (:9) | (S4)(ii) | see the LS0 row. |
| TDP-IMPL (:8) | (S4)(ii) | the tie-aware fallback with $O(p\sum_b(2^{|C_b|}+(K+1)^2))$ operations and $O(\sum_b2^{|C_b|}+J(K+1))$ storage (`C-DLV/STATEMENT.md:38-42`) [S2-F1]. |
| GUARD-W (stop-only guard: operational interruption ⇒ no output) (:9) | (S4) | **added in v0.3**: "the resource guard only stops a run (a stopped run returns no estimates)". |
| MACH (:9) | (S4)(i) | wall time $\le\tau\cdot$(operations)$+\tau_0$, peak memory $\le\beta\cdot$(words)$+\beta_0$; every allocation within the declared memory succeeds; build and dependencies work; no external interruption, no worker crash (`C-DLV/STATEMENT.md:28-31`) [S2-F1]. |
| CONFIG (fixed $R'=4k$, fixed worker count) (:9-10) | (S4)(ii) | production core + LS0 (cap $\ell_n+|\tilde S_0|$) + tie-aware fallback; default summary list only; certificate computations with declared polynomial operation/memory budgets included in the allocation; serial or a fixed number of concurrent workers (memory envelope multiplied by it); fixed number of islands (`C-DLV/STATEMENT.md:32-37`) [S2-F1]. |
| valid declared seed (:10) | (S4) | integer seed in $[1,2^{31}-1]$; allocation a list with finite positive `mem_gb`, `hours` (C-DLV STATEMENT.md:43-44). |
| complete allocation inequalities (FIN s6 Prop. F with A1 envelopes, A4 preflight bounds), LS0 score count $\le1+(\ell_n+K+1)q(p)$, evaluated at $(n,p_{\mathrm{raw}})$ (:10-11) | (S4)(iv), with the source of record `FINAL/sections/s6_delivery.tex:29-62` ($W_G$, $M_G$, $P_0$, $P_1$, $\bar P_t$, certificate budgets, LS0 preflight addition) [S2-F1] | "declared memory and time allocation at least the method's polynomial envelopes in $(n,p_{\mathrm{raw}})$, preflight bounds included"; the explicit inequalities go to the paper's appendix (`Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:29-62`). |
| CAL not assumed (:11) | — | nothing to supply. |
| qualifications: [OP] "PROVED (by this seat, unchecked)"; e4 rests on N3 "OPEN"; P1/S.3 "AUDITED (code reading)" (:11-12, :38-40) | carried | quoted in Theorem 6–7's master paragraph (v0.3). |

## Assembly
Under the former Theorem 6's hypotheses (those of `W3-RM2:RM2-R`): (V) by row 1; (S) and (P) by rows 3–4; every method/premise/allocation item by (S4) or
by the shipped code as pinned. F-UNI (`@2.1.0`) then gives $P(\text{no output})=0$ for every admissible $n\ge3$ with
$(n,p_{\mathrm{raw}})\in\mathfrak D$, and, under A:IDEAL-W⁺, for every admissible $n\ge3$, with
$P(\hat S=S_0)\to1$ under the joint law. The former Theorem 7 (hypotheses of `W3-RM2:RM2-F`): the same with row 2 for (V) and the noise law. The common-data-event
clause of Theorems 6–7 does not use F-UNI (it is RM-0(b) with RM2's interfaces) and needs none of (S4). ∎

**Consequence for READER_VERSIONS (v0.3; v0.5 adds MACH, CONFIG, TDP-IMPL and the allocation by exact source reference, S2-F1):** (S4) gains "ideal independent uniform random numbers", "the method's
stop/return rule and stop-only resource guard as coded", and the e4 tie rule (stated in words: "the local search from
the start mode starts at the smallest, lexicographically first maximiser of the start law"); Theorem 7 (A1) gains
"raw columns non-constant"; the master paragraphs of Theorems 6–7 carry F-UNI's inherited qualifications.
