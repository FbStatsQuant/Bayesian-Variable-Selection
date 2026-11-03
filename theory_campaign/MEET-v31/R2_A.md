All inputs are in hand: ABL-START has no results yet (design fixed, fits running), the chair's calibration-cost fact reproduces from the budget formula within 10%, and the engine constants are located. Writing the Round 2 position now.

# MEET-v31 · Round 2 · Seat A position

Seat A (Claude Personal, Fable 5.1). Read-only; no runs, no subagents. Citations are `path` (this branch) or `branch:path` with section or line; "judgment" marks my reading. ABL-START (`origin/theory/ABL-START:theory_campaign/ABL-START/REPORT.md`, fetched 2026-11-03) is still the design-only draft: `results/` holds only queue files, no `per_fit.csv`; the Owls log says "waiting for 18 fits". So item 1 is not folded in; the decision rule I will accept is fixed in §1 D1 **before** any result is read.

## 1. Disputes D1–D8

**D1 (ABL-START decision rule). HOLD on substance, amend the thresholds.** Chair fact 0.3 changes the arithmetic: the panel is 12 designs × 1 seed, not 20 paired, so my "≥ 15/20" becomes "≥ 9/12". Rule I accept before reading:
- *Keep, settled on evidence:* arm A has strictly fewer final-grid stages **or** fewer rebuilds on ≥ 9/12 designs, with log Ẑ error against the leave-one-arm-out reference not worse on a majority.
- *Keep but reframe (no depth claim in the paper):* no arm dominates on depth; the start is justified by S1/S2 (THM-SYNTH G4) and by the exactly-parallel table stage only.
- *Escalate to Felipe as a WORKHORSE candidate (not "change" by this meeting):* an alternative arm is better on objective 1 (|log Ẑ − ref| and reference PIP error) on ≥ 10/12 **and** not worse on stages or rebuilds on any S4/S5 design. Even then the change needs a 20-seed confirmation before a re-run, because ground rule 5 says "irrefutable" and 12 single-seed fits are not that.
Seat B's "majority ⇒ change" is where I hold: a 7/12 majority on single seeds against a full re-run and the loss of S1, S2 and D2's A₀ input (ground rule 7) is not irrefutable. Two cautions on the reference itself (Seat C's point, which I accept): the leave-one-arm-out pool mixes in the other arms' failures, so a design where the arms' pooled Ẑ_r disagree by more than 1 nat is inconclusive for evidence error and decides on depth only; and the reference's own island spread must be printed. What would move me to "change": the escalation condition above met **and** confirmed on 20 seeds.

**D2 (O-CERT card). CONCEDE to a gate.** Ship Z_𝒯 and the C1 certificate now (all seats agree). The O-CERT card enters the v3.1 output only if the chair's proof check PC1 confirms its P(card item false) ≤ 0.05 claim; until then it is a theorem obligation, not an output.

**D3a (extra local search from the R = 4 centre). CONCEDE.** Seats B and C are right that greedy search from a better centre need not end higher, and the extra search costs one scan (0.17–0.37 s at the study, `origin/theory/T38-RECORD:…/REGISTRY_v2.md` §D LS0-3/4). Keeping it makes "HPM(R′) ⪰ HPM(4) after search" deterministic (Cor W-R) at no cost. Keep.

**D3b (flags when R′ > 4). CONCEDE, Seat C's form.** Report both: baseline flags over islands 1–4 against the baseline HPM reference (for the bitwise claim), and expanded flags over all R′ islands as the run's reported flags, labelled. E1 compares island bests with the HPM (`Scripts/SMC_BVS/core/v3_run.R:149`), so the baseline value needs the baseline HPM kept.

**D3c (LS0 wording). CONCEDE.** The study-path streams and island outputs stay bitwise and the scored set is nested; the near-tie list, the stores, E3 and the certificate can change. The paper says "HPM unchanged 2,394/2,394; stores nested; island outputs bitwise", not "bitwise fit".

**D3d (scope of "scale p", C6). HOLD, merged.** The paper states the implemented execution level exactly as Seat C words it (islands only: depth ∝ N_e·(p + B + 2)·(T + L + 4), setup and reductions counted; no "free of N, H, R"). C6 is implemented and law-checked **iff** the paper demonstrates any p > 2,500 (there N_e = p and depth is quadratic). That is an HQ/Felipe decision on the paper's p range, not a seat vote. What changes my mind: nothing evidential; it is a scope decision.

**D3e (block tables as (h), C11). CONCEDE.** Add the table stage as the explicit parallel local step (bitwise, independent sub-model scores). Clustering is O(p²) memory and time in `cpp/v3_blocks.h:46–108` (full distance matrix, Lance–Williams updates); it enters the v3.2 roadmap with C7.

**D3f (mutable counters). CONCEDE.** v3.1 workers are processes (as in the METH-AUDIT harness); if threads are ever used, per-worker `Data` counters summed deterministically at merge. Spec sentence.

**D4 (calibration cost). CONCEDE, with the formula the chair can check.** My "false in cost" was wrong once rebuilds exceed four. From `v3_preprocess.R:26` (H₀ = ⌈512 N₀/2500⌉) and `cpp/v3_core.cpp:625–640` (4 diagnostic islands per rebuild), calibration work in island-trajectories is (1 + 4I)·H₀ against 4N₀ for the final run, i.e. a ratio ≈ 0.05 + 0.2·I with I ≤ ℓ rebuilds. Against the concurrency log (`evidence/2026-11-03_concurrency_runs.md`):

| design | rebuilds I | predicted ratio | observed cal/serial-final |
|---|---|---|---|
| S1 r001 | 2 | 0.46 | 0.45 |
| S5 r002 | 3 | 0.67 | 0.62 |
| S4 r001 | 8 | 1.69 | 1.76 |

So calibration reaches ≈ 2× the final run at I = ℓ = 10 and the cap grows like log₂(n + p). W-cal is on the critical path of any wall-clock claim (Seat B's Amdahl point stands). The rule itself is unchanged (all agree).

**D5 (primary PIP). HOLD, criterion amended.** Switch to Ẑ-weighted primary on theory (Prop P(ii)–(iii), T31(i)); both reported. Seat B's gate measures MPM closeness to the binary truth, which is objective 3, not objective 1; Seat C is right that it is not posterior accuracy. The check that would reverse me: on the ABL-START designs, the Ẑ-weighted PIP's error against the pooled reference is larger than the equal-weight one on ≥ 7/12 designs; or the chair's rescoring (fact 0.5) shows max_j |Δ| > 0.1 in more than 5% of the masked-cell fits with the Ẑ-weighted MPM worse there. Seat B's table is reported either way.

**D6 (inherent-limitation wording). CONCEDE on all four, with these wordings.** (i) "Every worker needs all of X or G" is inherent to a full-coordinate kernel; "8p² bytes" is not (C7). (ii) Seat C's bound Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} is correct (D_S ≥ 1 and Q_S ≥ yᵀy/(n+1) are both in `Docs/Methodology/METHODOLOGY_v3.md` §5; Σϖ = 1), so the limitation is "no useful upper bound on Z from the run's record alone" (T31(c), O-CERT §1.1). (iii) max{Z_𝒯, 0.05Ẑ} keeps 95% lower coverage because Z ≥ Z_𝒯 always; the limitation is "Markov is the only assumption-free probabilistic bound". (iv) Masked weight variance is a failure mechanism PROVED in kind (E1/E2, SEP-B); its severity on resolved grids is V11, OPEN, a theorem obligation.

**D7 (estimator for general h, joint summaries). CONCEDE as a spec addition.** Define the estimator of E_π[h] for bounded h as the Ẑ-weighted pool of per-island plain averages of h over the measured-round particles, and have the final run archive the measured-round populations (4N_e model keys per island, ≈ 10⁴ keys, cheap). ADDITIVE: no randomness is read. The study fits did not save them, so joint summaries are not claimable for the 2,400 fits (Seat C is right). Seat C's finite-R bound and the measured-round island identity for general h are theorem obligations (my Q6). THM-SYNTH A2's "fails only downward" is literally false (an unbiased non-constant nonnegative estimator cannot sit below its mean a.s.); the correct sentence is "non-crossing islands underestimate (M2); the upper tail is O_P(1) by Markov".

**D8 (6 `resource_limit` fits). CONCEDE that it is not a method question.** It is a (iv) engineering action for HQ: it removes the only measured P(U) mass and exercises Lemma RO under real stops. Not a delivery theorem.

## 2. Chair facts 0.1–0.5

- **0.1** closes my Q9 for Prop W: "bitwise on smoke + 3/3 study designs" may be printed. The 1.9× is a 2-core number; no 4-core speed-up may be printed until measured. W-cal still unexecuted (Q2 stands).
- **0.2** reverses my §2.4 cost sentence; conceded in D4 with the formula above.
- **0.3** removes Seat C's confounding worry (kernel B and graph fixed across arms) and rescales my D1 thresholds to 12 designs. Arm D's start equals arm A's on S5 r002 c050 (start mode empty; Owls log), so that design cannot discriminate A from D.
- **0.4** conceded in D3f.
- **0.5** awaited; my D5 criterion is stated above so the result is read against a rule fixed in advance.

## 3. Procedural rule and sorting of my Round 1 §5

**Accept SYNTH_R1 §3 with one amendment.** Every "theorem obligation" must name the method decision it could overturn and why it does not: rebuild convergence (keep calibration stands because validity is conditional on any frozen 𝓒, T12/Prop 2); masked weight variance (Ẑ-weighted primary stands on Prop P(ii) consistency; only finite-R precision is open); P(schedule_limit) (budgets stand; it is a V13 quantity). Without that line, an obligation can hide a method question, which is Seat C's warning.

Sorting of Q1–Q12:

| bin | items | closes by |
|---|---|---|
| (i) method question still open | Q1 (start) | ABL-START read against the D1 rule |
| | Q4 (primary PIP numbers) | chair's rescoring + ABL-START reference error, read against the D5 criterion |
| | Q11 (C6 in v3.1?) | HQ/Felipe decision on the paper's p range |
| (ii) theorem obligation | Q6 (island identity for general h; Theorem H crux), plus from D6/D7: V11 severity, Seat C's finite-R bound, O-CERT card's 0.05 claim | THEOREM_REVISION_INPUTS.md, status OPEN |
| (iii) inherent limitation | per-round Θ(p) sequential steps (definition of a systematic scan; Prop D remark); masking of any product start (T27(i) PROVED-LOCKED); no run-weight diagnostic sees a never-visited mode (E1c, V12 PROVED; CD Thm 2.1); posterior misses at n = 200 (N200 PROVED); no useful run-only upper bound on Z (T31(c)) | stated in the paper |
| (iv) engineering / spec, no method content | Q2 (W-cal replay, scorer statelessness), Q3 (merged LS0 replay), Q5 (GUARD semantics), Q7 (6 stopped fits), Q8 (R′ rule, flags), Q9 (§6 numbers: partly done), Q10 (VAL-FP at p = 500), Q12 (LS0 placement), D3e/D3f/D7 spec text | checks on the 3 replay designs; spec edits |

## 4. Item 9 — generality in (n, p)

Audit of every setting in `Docs/Methodology/METHODOLOGY_v3.md` (M) and `Scripts/SMC_BVS/core/` (budgets `v3_preprocess.R:19–33`; preflight `v3_fit.R:17–46`; calibration `v3_calib.R`; final `v3_run.R`; C++ as cited). Regimes: p ≪ n, p ≈ n, p ≫ n, tiny n, joint growth. Numbers below were computed by me from the budget formulas (script in my scratchpad; not a repository file).

| setting | value (source) | class | reason | behaviour across regimes | action |
|---|---|---|---|---|---|
| g = n, τ = 1, IG(0.01, 0.01), BB(1, p), cap K = min(p, ⌊n/2⌋) | M §5 | (a) | Felipe's model; reasons in M §5 | K void for p ≤ n/2; binds for p ≳ n/2; K = 1 at n = 3 | keep |
| standardisation, n ≥ 3, p ≥ 1, exact-duplicate drop | M §4; `v3_preprocess.R:106` | (a) | affine invariance; K ≥ 1 and SD need n ≥ 3 | regime-free | keep |
| B = min(⌊√n⌋, ⌊√p⌋, B*) | M §3; `v3_preprocess.R:22` | (a)+(b) | Felipe's rule; B ≤ K for n ≥ 3; judgment: 2^B ≤ 2^{√n} keeps the within-block multiplicity penalty B log 2 = o(n) | √p binds for p < n (p = 50: B = 7), √n for p > n; B = 1 at n = 3, B = 3 at n = 10 | keep |
| **B* = 16** "implementation limit" | M §3, §8.7, §13; `v3_preprocess.R:22` | labelled (e) → **re-classify (c)** | table work p·2^B/B and memory 16·(p/B)·2^B bytes are linear in p only for bounded B (65,536·p bytes at B = 16); **and the theory needs a bounded B**: W7-PART Thm B and every LH theorem require g ≤ B < 2g for a fixed group size g (`origin/theory/THM-INV:…/REPORT.md` §1 row 3, §2 rows Thm 2/5); an unbounded B violates B < 2g for every fixed g and falls into CE2 (packing ≥ 2 groups per block) | binds for n, p ≥ 289; covered families g ∈ {9..16} at B = 16, {8..14} at the study's B = 14 | keep 16; rewrite the label; study unchanged (B = 14) |
| ℓ = ⌈log₂(n+p+1)⌉ | M §3 | (b) | local-search move cap and rebuild cap | 10–11 at the study; 20 at n = 10⁶ | keep |
| L = max(4, ⌈log₂(n+1)⌉) | M §3 | (b) + floor (c) | burn-in grows with n; floor binds for n ≤ 15 | theory gap: t_mix may be polynomial (V10) | keep; V10 obligation |
| N₀ = max(2,500, n, p) | M §3; `:25` | (c)+(b) | floor: per-island RB-PIP Monte Carlo SD ≤ 1/(2√N) = 0.01; N → ∞ with n is a premise of the discovery bounds (`THM-INV digests/API.md` row (1 − c_* + r_n)^N) | floor binds at the study; N₀ = p for p > 2,500 makes per-stage work Θ(p²) (M §8.3); not silent, preflight reports | keep; C6 for p > 2,500 (D3d) |
| H₀ = ⌈512 N₀/2500⌉ (ratio 0.2048) | M §3; `:26` | (c) | calibration/final work = 0.05 + 0.2·I (D4) | ratio ≤ 2.1 at I = ℓ = 10, grows with ℓ | keep; print the formula |
| T₀ = max(1,000, ℓ²) | M §3; `:27` | (c); the ℓ² term is cosmetic (binds only when n + p > 2³¹) | ceiling ≥ 30× any predicted T (O-STAGES: T* = log₂A₀ + 7.7, A₀ ≲ 10³ nats); cost cap of a fully forced pilot (exactly T_e stages, `cpp/v3_calib.h:38–44`) | never binds in practice | keep; say so |
| R = 4 islands, 4 diagnostic islands, 4 measured rounds, tier factor 4, one escalation | M §3, §6.8–6.9; `v3_calib.R:12`, `v3_run.R:87–88`, `cpp/v3_core.cpp:633` | (c) | declared budgets; identities hold for any R, Hm ≥ 1; escalation decided before final randomness | fixed 16× work ceiling; `schedule_limit` beyond | keep; R′ = 4k stacking rule declared; stream map extended to 10..9+R′ (spec) |
| ESS threshold 0.90 (pilot and grid) | M §6.6–6.7; `cpp/v3_calib.h:31, 79` | (a) | per-stage weight CV² ≤ 1/9; same η for pilot and grid so Theorem G (greedy optimal among refinements of the pilot points) applies; any fixed η gives the same regime behaviour with a different constant | T grows like log₂A₀ = O(log log(np)) under masking | keep |
| 60 bisection halvings; 1e-12 snap to 1 | `cpp/v3_calib.h:34, 42, 82, 89` | (d) | 2⁻⁶⁰ below double resolution on [0, 1] | regime-free | keep |
| exploratory floor 1/T_e | M §6.6; `cpp/v3_calib.h:38` | (c)-derived | forced steps are counted and trigger escalation | regime-free | keep |
| V = top 20p by γ₀ ∪ top 20p by γ₁ ∪ ∅; store 40p+1 | M §6.7, §6.10; `cpp/v3_ledger.h:70, 76` | (c) | V must hold the competing pair (V11 premise); size linear in p caps grid cost 60·\|V\|·T_e | stored fraction of scored models shrinks with N·T·p, but only the top few matter; the near-tie list and Z_𝒯 read the store | keep; Z_𝒯 reported (agreed) |
| cache 500p, "clear when full" | M §8.6; `v3_calib.R:138`, `v3_run.R:89`, `cpp/v3_score.h` cache comment | (c), law-free | a hit returns the bits a fresh evaluation would; eviction is deterministic | hit rate falls as N/500 grows; cost only | keep |
| **near-tie window 10⁻⁹ nat** | M §6.10; `v3_run.R:138–140` | (d), but silently loses meaning | the scorer's own error bound η(S) = 64ε[ν(yᵀy/Q)(1 + k·cond) + …] (`cpp/v3_score.h:240–245`) scales with ν = n/2: ≈ 6·10⁻¹⁰ at n = 200, 6·10⁻⁹ at n = 2,000, 3·10⁻⁶ at n = 10⁶ | at n ≥ 2,000 the window is below score noise | keep 10⁻⁹ as the informational window; add the η-based window to the certificate card (POST HOC, reporting only, HPM and tie rule untouched) |
| exact-branch rule Σ_{k≤K} C(p,k) ≤ (5H₀ + 4N₀)·p | M §6.2; `cpp/v3_core.cpp:69–82` | (b)+(c) | enumerate iff it costs at most one SMC stage of all islands (pilot H₀ + 4 diag H₀ + 4 final N₀, each ≈ p scores per particle) | fixed p is eventually enumerated (N₀ ≥ n); tiny n: n ≤ 5 enumerated up to p ≈ 25,000; n = 10 up to p ≈ 36 | keep |
| neighbour threshold r_n = √(2 log p/n), ≤ B partners, always ≥ 1 | M §6.4; `cpp/v3_blocks.h:154–167` | (b) | largest chance correlation of p unrelated columns | r_n ≥ 1 when p > e^{n/2} (n = 10: p > 148): every j keeps only its single largest partner, so the graph degrades to 1-nearest-neighbour; principled fallback, **unstated in M** | keep; state the fallback |
| clustering cut | M §6.3; `cpp/v3_blocks.h:121–144` | (b) | cut by size B only; **there is no correlation threshold** in the cut | regime-free; O(p²) memory and time (C11) | keep; M §10's "between-cluster correlation at the √(log n/n) scale — the same scale as the neighbour threshold" is wrong (threshold is √(2 log p/n)): fix the sentence |
| E1 > 1 nat, E2 SD > 1 nat, E3, low ESS < 0.5N, forced steps, grid flags | M §6.9; `v3_calib.R:101–102`, `v3_run.R:149–152` | (a) | a factor e in odds; triggers define the law of 𝓒 | E1 is scale-free (any missed mode); E2 is a Monte Carlo quantity, not n-scaled | keep (all seats) |
| duplicates \|r\| ≥ 1 − 10⁻¹⁰; Q recompute below 10⁻⁸·yᵀy | M §4.5, §6.13; `cpp/v3_core.cpp:722`, `cpp/v3_score.h:219` | (d) | reporting and cancellation guards | regime-free | keep |
| seed ∈ [1, 2³¹−1], 14 streams, pinned flags | M §2; `v3_preprocess.R:8`, `cpp/Makevars.v3` | (c) | "bitwise" is per binary and BLAS (Seat B) | regime-free | state the scope |
| allocation (mem_gb = 8, hours = 24), preflight, wall-clock guard | M §2, §8.6; `v3_fit.R:16–46, 49, 67`; `cpp/v3_runtime.h:15, 23` | (c) | the allocation decides **delivery only**: the SMC preflight is memory-only; the guard reads no uniforms (Lemma RO), so the potential run is a deterministic function of (X, y, seed, binary) and hardware changes only whether it completes | memory 8·(3np + 3p²) bytes at setup: p ≲ 1.8·10⁴ at 8 GiB, ≲ 5·10⁴ at 64 GiB; reported as `resource_limit`, not silent | keep; paper sentence below |
| Gram-based scorer, O(p²) correlations and distances | M §8.1; `v3_fit.R:27` | (c) | implementation of the exact target | the only hard size limit of v3.1 | v3.2: C7 (LAW-PRESERVING up to fp) and chunked distances with the same ordering rule (bitwise blocks) |

**Every (e) resolved.** None is (e) in substance. Four are (e) by label or wording, and all four fixes are spec text or a reporting field: ADDITIVE, no study value changes, no proof route needed.
1. B* = 16: re-label (c) with the two reasons above. Study: B = 14 at n = 200, unchanged.
2. T₀'s ℓ² term: keep, state that it binds only for n + p > 2³¹.
3. M §10 correlation-scale sentence: correct to √(2 log p/n).
4. Near-tie window: keep 10⁻⁹; add the η-based window to the card (POST HOC; at n = 200, η ≈ 6·10⁻¹⁰ < 10⁻⁹, so study near-tie lists are unlikely to change; the HPM and the exact-equality tie rule never change).
Plus the unstated fallbacks to write into M: the 1-nearest-neighbour graph when p > e^{n/2}; the stream map for R′ > 4.

**Specific points HQ asked.**
- *B* = 16 vs W7-PART's g ≤ B < 2g.* A constant B at large n, p is not merely acceptable; it is what the fixed-g theorems need. B is the method's block size, g the generator's group size; the condition says which families a given B covers. The study generator (g = 5) is outside for any B ≥ 10 (CE2), which is a theorem-scope fact, not a method defect.
- *Floors 2,500 and 1,000, ESS 0.90, 40p+1, 500p, R = 4, tier 4:* classified above; all keep.
- *Exact-branch rule:* a cost crossover with a stated meaning; keep.
- *Neighbour graph and clustering cut:* (b); state the fallback; fix the §10 sentence.
- *`resource_limit` vs "runnable from X, y and one seed alone".* Both hold. The computation is a function of (X, y, seed) and the binary; the allocation is a declared fourth input (M §2) that decides delivery only. The paper states: "A fit either returns the output of the potential run or returns no estimate (`resource_limit`, `schedule_limit`, `numerical_failure`), never a different estimate. Every guarantee is stated for the potential run and the output event 𝒪, as P{𝒪, ·}; P(no output) is an operational frequency that depends on the allocation and hardware and is reported with them (V13)." This is Seat C's output convention, which I adopt.
- *Separate p ≪ n / p ≫ n rules.* Not needed: K, B, N₀, the exact-branch rule and r_n already switch regime implicitly (K void for p ≤ n/2; √p binds for p < n, √n for p > n; fixed p eventually enumerated; 1-NN graph when p > e^{n/2}). The one regime to **state** rather than rule separately is tiny n (n ≲ 20): K ≤ 10, B ≤ 4, the start is close to singleton factors, and the graph is 1-NN; the method runs and its fixed-data guarantees (V6, HPM best-scored) hold, but no asymptotic theorem applies.

**Theory scope per regime, and whether a method choice causes it.**
- p ≤ n − 1 (p ≪ n growing, p ≈ n): (b2-LH) without LS0 and (b1-LH) with LS0, exact-Gram LH, g ≤ B < 2g (`THM-INV` §2 rows Thm 5). Not restricted by a method choice.
- n ≪ p ≤ n^A: (b1-LH-iid) with LS0, XF GAP (A-REV3/6/8). The polynomial restriction comes from the target theory T03 under Felipe's prior (`THM-INV` §1 row Thm 1: "p ≤ n^A"; §3b: "LACK for … p up to e^{Cn^α}; we have p ≤ n^A only"). The partition lemma's bound p²√n·e^{−(n−4)I*} allows log p = o(n), so the local step is not the cause. Cause: the model (a), fixed by Felipe; no sampler choice.
- p ≥ e^{Cn^α}: no theorem; the method runs up to the Gram memory limit (C7 in v3.2). Song–Liang's range is a property of their prior and conditions, not of their sampler; same separation here.
- tiny n: no asymptotic claim; exact target quantities on the exact branch.
- joint growth p = n^A: covered as above; cost Θ(p²) per stage (N₀ = p) and 24p² setup bytes are declared budgets, lifted by C6/C7, not method restrictions.

## 5. Final list

**Settled (my vote):** block start kept, decision rule D1 fixed before ABL-START is read; HPM sole decision rule, LS0 in the shipped core after the final local search; MPM from each named PIP; Z_𝒯 and C1 reported, O-CERT card gated on PC1; parallel layer (a)–(h) with GUARD "any worker stop ⇒ no output", process workers, extra search from the R = 4 centre, baseline and expanded flags, R′ = 4k declared, never split N_e, LS0 claim worded as D3c; calibration unchanged with the contract and the cost formula 0.05 + 0.2·I; Ẑ-weighted PIP primary (D5 criterion stated); flags kept as triggers and labelled heuristics; the general-h estimator and measured-round archive added to the spec; item 9: no (e) in substance, four label fixes, two fallbacks stated, allocation statement as above; all D6 wordings as conceded.

**Still open, with the single closer:**
1. Start: ABL-START read against the D1 rule.
2. Primary PIP numbers: chair's rescoring plus ABL-START reference error, read against the D5 criterion.
3. C6 in v3.1: HQ/Felipe decision on whether the paper shows p > 2,500.
4. W-cal and merged-LS0 bitwise replays, scorer statelessness: the 3 replay designs (engineering; no method content).
5. O-CERT card and Seat C's bounds: proof check PC1.
