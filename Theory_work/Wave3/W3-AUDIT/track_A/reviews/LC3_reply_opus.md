# LC3 reply — Claude Opus 5.5 (high), fresh general-purpose agent aa8aa8789cab8df06, 2026-11-16 ~17:43 CST (verbatim)

## T6 · START-X: VERIFIED WITH AMENDMENTS

I checked everything against the code at the pin (`git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core` exits 0).

- **Step 1 (what `build_start` computes).** It matches `v3_start.h:101-151`. Code indices: `logF[b]` is the prefix over blocks 0..b−1, and `cond_cum[b][r]` uses `logprof[b]` with `logF[b][r−j]`, so it normalises to F_{b+1}(r). `cumulative_from_logs` has its last positive entry equal to 1 under exact arithmetic, so a zero-mass index is never returned.
- **Telescoping.** Write s_b = Σ_{c≤b} k_c. Each block draw's factor is e_b(k_b)F_b(s_{b−1})/F_{b+1}(s_b), so the product over b = J−1..0 telescopes to ∏e_b(k_b)·F_0(0)/F_J(k). Blocks the loop does not visit have s_b = 0, and their factor e_b(0)F_b(0)/F_{b+1}(0) equals 1. The e_b terms cancel against the within-size draws because e_b(0) = 1.
- **Normaliser and draw sites.** Z̄₀ is right: a truncated convolution is exact for indices ≤ K. The uniform count is right. The only production π₀ draws are at `v3_engine.h:108/184/289`, with `init_states = nullptr` at `v3_core.cpp:446/632/670`. `cpp_start_draw` (`v3_core.cpp:239-250`) is reached only through `v3_start_draw`, which no fit path calls.

Findings:
1. **S** — `T6_START/STATEMENT.md:27-28`. "This value … initialises every island's log Ẑ" is inexact. The code sets `logZ = D.logm0 + st.logZbar0` (`v3_engine.h:299`), i.e. log Ẑ₀ = log m(∅) + log Z̄₀, which is T12's Ẑ₀ = m(∅)Z̄₀. **Fix:** state the initialisation exactly. Either cite `D.logm0 = log m(∅)` as a separate fact, or say log Z̄₀ enters log Ẑ₀ additively.
2. **F** — `T6_START/PROOF.md:60`. The N9 quote "F_b is the size profile of the first b blocks (indices 0..b−1)" is at N9 `PROOF.md:254-255`, not ":257-258" (those lines are the `cond_cum` bullet). **Fix:** change the citation.
3. **E** — `T6_START/PROOF.md:4`. m_b ≤ K needs both BLK-b (|C_b| ≤ B) and BLK-a (B ≤ K); only BLK-a is cited. **Fix:** cite both, or cite T4 ENC-a, which states |C_b| ≤ B ≤ K directly.
4. **E** — `T6_START/PROOF.md:28-29`. The fit's value goes through `start_summary` (`v3_core.cpp:198`) and `v3_setup.R:72` (`start <- r$start`); "both `st.logZbar0`" skips this hop. **Fix:** add the two citations.
5. **F** — `T6_START/STATEMENT.md:7-10, 36-37`. T12's START asks for "exact iid π₀ draws" and the "same exact sampler". (S) covers only the law of each draw; independence is deferred to CC4. **Fix:** add one line: "START (W1-N1:75; T12:48) = (Z) + (S) + (S′) + CC4", so (S) is not read as the whole of START.
6. **E** — index conventions. The code comments at `v3_start.h:139, 155-156` use 1-based block indices ("F_{b-1}", "b = J..1"), but the code is 0-based (comment at `:147`). T6 rightly follows the code. **Fix:** add a sentence saying this, since the brief singles out index conventions. Also, N9 uses r_b both for the tables and for the partial sums (N9 `PROOF.md:279-282`); T6's s_b avoids the clash, but the comparison paragraph could say so.

## T7 · KER: VERIFIED WITH AMENDMENTS

All four steps match T12 §1 (`T12 STATEMENT.md:25-31`) line by line at the pin. This includes the Gibbs cap rule (`add_ok`, with `oj = 0` and one uniform still read), the self-loop at |S| ∈ {0, p} with no uniform, the neighbour candidate set and `back`, and the independence acceptance `φ(d′−d)`. Each detailed-balance identity is correct:
- Gibbs: γ(A)γ(A∪j)/Σ.
- Uniform swap: q = 1/(k(p−k)) in both directions.
- Neighbour swap: (1/k)·min(γ/|N(j)∖S|, γ′/|N(l)∖S′|).
- Independence: γ₀γ₀′·min(e^{φd}, e^{φd′})/Z̄₀.

The graph built at `v3_blocks.h:149-173` is symmetric, loop-free and duplicate-free. Fisher–Yates is a bijection onto the m! orders, and its m−1 uniforms are read before any step. The label map is at `v3_engine.h:205-211`. `v3_engine.h:1-373` and `v3_blocks.h` are unchanged since 39db138 (the only engine hunk is at line 374). N9's comparison is reported correctly.

Findings:
1. **S** — `T7_KER/PROOF.md:8`. "Under EX-A the cached and the fresh log m agree (T3 OPC Step 2)" depends on T3, which is not in the Setting's hypotheses. **Fix:** add T3 to the Setting, or argue it directly. `ScoreCache::find` compares the full sorted model, not just the hash (`v3_score.h:271-279`), and stores the scorer's value; under EX-A that value is the exact log m(S).
2. **E** — `T7_KER/STATEMENT.md:33`. "Has no loops, which the Hastings factor needs" names the wrong property. The factor needs symmetry. The proof also relies on duplicate-freeness, since |N(j)∖S| is a set count and l is drawn uniformly from `cand`. Loop-freeness is not needed (j ∈ S, l ∉ S). **Fix:** "symmetric, loop-free and duplicate-free; symmetry and duplicate-freeness are what the proposal ratio uses."
3. **E** — `T7_KER/STATEMENT.md:37-38` (KER-d). "The scores are built from the data before any island" is inaccurate: proposal scores are computed during the run. **Fix:** "the score function S ↦ log m(S) is fixed by the data; its values do not depend on particles."

## T8 · OVL: VERIFIED WITH AMENDMENTS

- **Budget.** It checks out: N_e = `b$tiers$N[tier+1]` ≥ N₀ = max(2500, n, p) and L = max(4, ⌈log₂(n+1)⌉) (`v3_run.R:90`, `v3_preprocess.R:24-25, 30`), and T ≥ 1. So D_r ≥ N₀(L+6) ≥ 10n.
- **Limit argument.** {π₀ ≤ ½} = {o₀ ≥ 1} is correct. The inclusion holds once 10n ≥ 2c, and the step to (D-iv) via e^{−c} + P(…) is correct.
- **Quotes.** Those from W3-SAMP (`:76-83`, `:102-104`), `D_theorem.md:53-54` and IF-START (`W3-START2-R:241-244`) are accurate.

Findings:
1. **S** — `T8_OVL/STATEMENT.md:14, 31`; `PROOF.md:19`. "(A5)" is not defined in T8 or in any source T8 cites. IF-START's hypotheses are "(T1⁺⁺) with (AL) at Q = S₀", or (T3⁺⁺)(b) with Q = S₀. The label lives only in AUDIT.md, which a reader cannot use to check the clause. **Fix:** define (A5) in the statement by quoting the IF-START hypothesis it stands for.
2. **S** — `T8_OVL/STATEMENT.md:31`. "Under the hypotheses of IF-START, i.e. only under (A5)" treats the full hypothesis set as if it were (A5) alone. PROOF:19 says it correctly ("which include (A5)"). **Fix:** use the PROOF's wording.
3. **S/F** — `T8_OVL/STATEMENT.md:32-34`. Two problems:
   - "Follows … whenever limsup(E_n − max(1, log p/log n)) < 0" leaves out the other hypotheses of OVL⁺/OVL⁺⁺ (`W3-START2:181-185`): setting F, (E), (GF-16), visibility, a deterministic Q ⊇ S₀ with |Q| ≤ K and |Q∖S₀| ≤ q̄, (AL) for Q, and bounded levels a_{n,l}.
   - "Word for word in `W3-START2-R:212-213`" is wrong. That line restates OVL⁺ with two substitutions: (V-cp)/(V-mp) for (V-c)/(V-m), and (T1⁺⁺)(a) for (T1⁺)(a).

   **Fix:** "under the hypotheses of `W3-START2-R:OVL` (OVL⁺ of `W3-START2:181-189` with the substitutions at `W3-START2-R:212-213`), whenever …". Optionally add the one-line derivation: log max(n,p)/log n = max(1, log p/log n).
4. **E** — `T8_OVL/PROOF.md:6`. T ≥ 1 is cited from the definition of `v3_check_grid` (`v3_run.R:77-81`), not from where the final run calls it (`v3_run.R:225`). **Fix:** cite `:225`, or `W3-SAMP/STATEMENT.md:42`.
5. **E** — `T8_OVL/PROOF.md:13-15`. Two small gaps:
   - 1_𝒜°·o₀ needs the convention 0·∞ = 0 off 𝒜° (o₀ = ∞ exactly when S₀ ∉ Ω).
   - "For 𝒜 ⊆ 𝒜° the probabilities are smaller" uses the fact that, on 𝒜, the actual D_r equals the potential one.

   **Fix:** state the convention, and cite T5 CAL-d for the equality.

## T9 · TDP: VERIFIED WITH AMENDMENTS

- **DP (`mode_dp`).** It matches TDP_E: `arg` is reset on a strictly larger value and appended on an equal one, M[b][0] = 0, and k̂ comes from a strict-`>` scan.
- **Enumeration (`rec`).** It follows only tight edges and every code in `arg`, and leaves are distinct sets.
- **Root check.** Every finite M[b][r] has a tight edge down to (0, 0), so the root `feasible()` passes.
- **Feasibility.** Reachability is equivalent to "some S ∈ E fits IN/OUT", because the constraint splits by block.
- **Greedy invariant.** It holds; the next-element argument correctly uses |S| = |S_E| = k̂.
- **Order.** Internal order equals original order (`v3_setup.R:8`).
- **Cost and storage.** Both bounds are correct and fit inside TDP-IMPL's.
- **Precision flags.** `Makevars.v3` has `-ffp-contract=off`.

Findings:
1. **F** — `T9_TDP/PROOF.md:60-63`. "Correct as stated … no error" overstates the re-check. TDP_E (4) (`TDP_E.md:55-57`) claims lex_min E "for every cap ≥ 1". At the pin, `start_mode(st, cap, true)` with cap < 2 throws `invalid_argument` (`v3_start.h:272`; C-PACK MR2 at `:185-186`). TDP_E's line references are also stale (`rec` at "v3_start.h:217-237", `TDP_E.md:17`; it is at `:281-300` at the pin). **Fix:** record that TDP_E (4) holds at the pin only for cap ≥ 2, as (TDP-b) already assumes, and that its line numbers are stale.
2. **F** — `T9_TDP/PROOF.md:47-49` (TDP-c). W1-N3 Theorem N3-code (b) was proved for an earlier `start_mode` (W1-N3 `STATEMENT.md:19`, a campaign copy at `v3_start.h:178-240`). T9 applies it to the pin's refactored `mode_dp` + `rec` without showing the two are the same algorithm. The gap is closable: `git diff 39db138 4676af6` shows the DP and enumeration arithmetic unchanged, only moved into `ModeDP`. Also, "cap = ∞" in the statement is not a valid argument; the proof's cap > |E| is the right form. **Fix:** add that diff fact. Alternatively, prove E = 𝒜* directly under exact arithmetic: a maximiser of size k̂ has each U_b ∈ `arg` and every prefix optimal, hence every edge tight.
3. **F** — `T9_TDP/STATEMENT.md:33-38`. TDP-IMPL (`C-DLV/STATEMENT.md:38-42`) asks for "W1-N3's reference algorithm TDP (L7)". The coded routine is TDP-E (tight-edge reachability on the binary64 DP). T9 discharges TDP-IMPL as "output S* under exact arithmetic, plus the cost and storage bounds", not as the same algorithm as L7; the statement should say so. Separately, in production the fallback runs only after the enumeration has already visited cap = 10⁶ elements. The "cap times a polynomial" claim in Not-claimed is unproved, and the delivery clause needs that cost too. **Fix:** add the bound cap·O(J(K+1) + p log p). Every DFS branch ends at a leaf, so there are at most J internal nodes per leaf. Or name where the delivery budget covers the enumeration.
4. **E** — `T9_TDP/PROOF.md:61-62`. Precision (i) says "assignment, not recomputation", but `mode_tight` and `rec` do recompute v. What makes the equality test exact is that recomputing the same expression on the same doubles is deterministic under (H2-FP), with `-ffp-contract=off`. **Fix:** reword.

No mathematical step failed in any of the four items; every finding is a fix to wording, scope or citations.

LC3-VERDICT: T6=VERIFIED WITH AMENDMENTS; T7=VERIFIED WITH AMENDMENTS; T8=VERIFIED WITH AMENDMENTS; T9=VERIFIED WITH AMENDMENTS
